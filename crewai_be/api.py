# 标准库导入
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

# 相关第三方库导入
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 本地应用/库特定导入
from crew import CompanyResearchCrew
from analysecrew import CompanyCrew, IndustryCrew, MacroeconomicCrew,TripPlannerCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger
import global_config
from database_model import db,Job,JobResult,Agent,Task,Crew,CrewAgent,CrewTask
# 加载环境变量
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/crewai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
db.init_app(app)



# 启动研究团队的函数
def kickoff_crew(job_id, companies: list[str], positions: list[str]): 
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        company_research_crew = CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(companies, positions)
        results = company_research_crew.kickoff()
        logger.info(f"Crew for job {job_id} is complete", results)

    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))

# 启动分析团队的函数
def kickoff_crew_analyse(job_id, inputs: str):
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        intent = identify_intent(inputs)
        if intent:
            if intent == 'company':
                company_name = ' '.join(inputs.split()[1:])
                company_analyse_crew = CompanyCrew(job_id)
                company_analyse_crew.setup_crew(company_name)
                results = company_analyse_crew.kickoff()
                logger.info(f"Crew for job {job_id} is complete", results)
            elif intent == 'industry':
                industry_name = ' '.join(inputs.split()[1:])
                industry_analyse_crew = IndustryCrew(job_id)
                industry_analyse_crew.setup_crew(industry_name)
                results = industry_analyse_crew.kickoff()
                logger.info(f"Crew for job {job_id} is complete", results)
            elif intent == 'macroeconomic':
                country = ' '.join(inputs.split()[1:])
                macro_analyse_crew = MacroeconomicCrew(job_id)
                macro_analyse_crew.setup_crew(country)
                results = macro_analyse_crew.kickoff()
                logger.info(f"Crew for job {job_id} is complete", results)
            else:
                logger.info(f"Crew for job {job_id} can not intent")
        else:
            logger.info(f"Crew for job {job_id} can not intent")
    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


def kickoff_crew_trip(job_id, location:str, travelto:str, date:str, hobby:str):
    logger.info(f"Crew for job {job_id} is starting")
    results = None

    try:
        with app.app_context():  # 确保在应用上下文中执行
            trip_planner_crew = TripPlannerCrew(job_id)
            trip_planner_crew.setup_crew(location, travelto, date, hobby)
            results = trip_planner_crew.kickoff()
            logger.info(f"Crew for job {job_id} is complete")

    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:  # 确保对 jobs 字典的访问是线程安全的
            # 这里应该在应用上下文里执行，因为我们需要访问 Flask 的 db.session
            job = Job.query.filter_by(job_id=job_id).first()
            if job:
                job.status = 'ERROR'
                db.session.commit()

            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    else:
        with jobs_lock:  # 确保对 jobs 字典的访问是线程安全的
            job = Job.query.filter_by(job_id=job_id).first()
            if job:
                job.status = 'COMPLETE'
                # 确保在添加新的 JobResult 之前，job_result 实例与数据库会话关联
                job_result = JobResult(job_id=job_id, result=json.dumps(results))
                db.session.add(job_result)
                db.session.commit()
                logger.info(f"Database updated for job {job_id}")

            jobs[job_id].status = 'COMPLETE'
            jobs[job_id].result = results
            jobs[job_id].events.append(
                Event(timestamp=datetime.now(), data="Crew complete")
            )

    # 确保在所有数据库操作完成后，关闭应用上下文
    finally:
        with app.app_context():
            # 这里可以放置任何需要在应用上下文结束时执行的代码
            pass

# 识别用户意图的函数
def identify_intent(user_input):
    keyword = user_input.split()[0].lower()

    if keyword in ['company', '公司']:
        return 'company'
    elif keyword in ['industry', '行业']:
        return 'industry'
    elif keyword in ['macroeconomic', '宏观经济']:
        return 'macroeconomic'
    else:
        return None

# 定义API路由和处理函数
@app.route('/api/crew', methods=['POST'])
def run_crew():
    logger.info("Received request to run crew")
    # 验证请求数据
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']

    thread = Thread(target=kickoff_crew, args=(job_id, companies, positions))
    thread.start()

    return jsonify({"job_id": job_id}), 202

@app.route('/api/crew-analyse', methods=['POST'])
def run_crew_analyse():
    logger.info("Received request to run crew")
    # 验证请求数据
    data = request.json
    if not data or 'inputData' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    inputData = data['inputData']
    inputData = ' '.join(map(str, inputData))
    
    thread = Thread(target=kickoff_crew_analyse, args=(job_id, inputData))
    thread.start()

    return jsonify({"job_id": job_id}), 202

@app.route('/api/crew-trip', methods=['POST'])
def run_crew_trip():
    logger.info("Received request to run crew")
    # 验证请求数据
    data = request.json
    if not data or 'travel_from' not in data or 'travel_to' not in data or 'date' not in data or 'hobby' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    travel_from = data['travel_from']
    travel_from = ' '.join(map(str, travel_from))
    travel_to = data['travel_to']
    travel_to = ' '.join(map(str, travel_to))
    date = data['date']
    date = ' '.join(map(str, date))
    hobby = data['hobby']
    hobby = ' '.join(map(str, hobby))
    new_job = Job(job_id=job_id, status='PENDING')
    db.session.add(new_job)
    db.session.commit()
    thread = Thread(target=kickoff_crew_trip, args=(job_id, travel_from,travel_to,date,hobby))
    thread.start()
 
    return jsonify({"job_id": job_id}), 202
@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")
        if job.result is None:
            return jsonify({"status": "ERROR", "message": "Job result is None"}), 500
        # 解析job.result字符串为JSON对象
        try:
            result_json = json.loads(job.result)
        except json.JSONDecodeError:
            # 如果解析失败，将result_json设置为原始job.result字符串
            result_json = job.result

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })
@app.route('/api/job-results/<job_id>', methods=['GET'])
def get_job_result(job_id):
    job_result = JobResult.query.filter_by(job_id=job_id).first()
    if job_result is None:
        abort(404, description="Job result not found")
    return jsonify({
        "job_id": job_id,
        "result": job_result.result,
        "created_at": job_result.created_at,
        "updated_at": job_result.updated_at
    })

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    jobs = Job.query.all()
    return jsonify([{
        "job_id": job.job_id,
        "status": job.status,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    } for job in jobs])
@app.route('/api/update-research-manager', methods=['PUT'])
def update_research_manager():
    data = request.json
    if not data:
        abort(400, "Invalid data provided")
    
    if 'role' in data:
        global_config.research_manager_role = data['role']
    if 'goal' in data:
        global_config.research_manager_goal = data['goal']
    if 'backstory' in data:
        global_config.research_manager_backstory = data['backstory']
    
    return jsonify({"message": "Research manager configuration updated successfully"}), 200

@app.route('/api/update-research-agent', methods=['PUT'])
def update_research_agent():
    data = request.json
    if not data:
        abort(400, "Invalid data provided")
    
    if 'role' in data:
        global_config.research_agent_role = data['role']
    if 'goal' in data:
        global_config.research_agent_goal = data['goal']
    if 'backstory' in data:
        global_config.research_agent_backstory = data['backstory']
    
    return jsonify({"message": "Research agent configuration updated successfully"}), 200

@app.route('/api/config/research-manager', methods=['GET'])
def get_research_manager_config():
    """返回研究经理的当前配置。"""
    config = {
        "role": global_config.research_manager_role,
        "goal": global_config.research_manager_goal,
        "backstory": global_config.research_manager_backstory
    }
    return jsonify(config), 200

@app.route('/api/config/research-agent', methods=['GET'])
def get_research_agent_config():
    """返回研究代理的当前配置。"""
    config = {
        "role": global_config.research_agent_role,
        "goal": global_config.research_agent_goal,
        "backstory": global_config.research_agent_backstory
    }
    return jsonify(config), 200

@app.route('/api/update-company-analyse', methods=['PUT'])
def update_company_analyse():
    data = request.json
    if not data:
        abort(400, "Invalid data provided")
    
    if 'searchTask' in data:
        global_config.company_analyse_searchTask = data['searchTask']
    if 'analyseTask' in data:
        global_config.company_analyse_analyseTask = data['analyseTask']
    
    return jsonify({"message": "Company analyse configuration updated successfully"}), 200

@app.route('/api/update-industry-analyse', methods=['PUT'])
def update_industry_analyse():
    data = request.json
    if not data:
        abort(400, "Invalid data provided")
    
    if 'searchTask' in data:
        global_config.industry_analyse_searchTask = data['searchTask']
    if 'analyseTask' in data:
        global_config.industry_analyse_analyseTask = data['analyseTask']
    
    return jsonify({"message": "Industry analyse configuration updated successfully"}), 200

@app.route('/api/update-macroeconomy-analyse', methods=['PUT'])
def update_macroeconomy_analyse():
    data = request.json
    if not data:
        abort(400, "Invalid data provided")
    
    if 'searchTask' in data:
        global_config.macroeconomy_analyse_searchTask = data['searchTask']
    if 'analyseTask' in data:
        global_config.macroeconomy_analyse_analyseTask = data['analyseTask']
    
    return jsonify({"message": "Macroeconomy analyse configuration updated successfully"}), 200

@app.route('/api/config/company-analyse', methods=['GET'])
def get_company_analyse_config():
    """返回公司分析的当前配置。"""
    config = {
        "searchTask": global_config.company_analyse_searchTask,
        "analyseTask": global_config.company_analyse_analyseTask
    }
    return jsonify(config), 200

@app.route('/api/config/industry-analyse', methods=['GET'])
def get_industry_analyse_config():
    """返回行业分析的当前配置。"""
    config = {
        "searchTask": global_config.industry_analyse_searchTask,
        "analyseTask": global_config.industry_analyse_analyseTask
    }
    return jsonify(config), 200

@app.route('/api/config/macroeconomy-analyse', methods=['GET'])
def get_macroeconomy_analyse_config():
    """返回宏观经济分析的当前配置。"""
    config = {
        "searchTask": global_config.macroeconomy_analyse_searchTask,
        "analyseTask": global_config.macroeconomy_analyse_analyseTask
    }
    return jsonify(config), 200

if __name__ == '__main__':
    app.app_context().push()
    app.run(debug=True, port=3001)
