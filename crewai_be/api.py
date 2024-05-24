# Standard library imports
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

# Related third-party imports
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Local application/library specific imports
from crew import CompanyResearchCrew
from analysecrew import CompanyCrew,IndustryCrew,MacroeconomicCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger
import global_config
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def kickoff_crew(job_id, companies: list[str], positions: list[str]):
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        company_research_crew = CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(
            companies, positions)
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
def kickoff_crew_analyse(job_id, inputs: str):
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        intent = identify_intent(inputs)
        if intent:
          if intent == 'company':
            company_name = ' '.join(inputs.split()[1:])
            company_analyse_crew = CompanyCrew(job_id)
            company_analyse_crew.setup_crew(
            company_name)
            results = company_analyse_crew.kickoff()
            logger.info(f"Crew for job {job_id} is complete", results)
          elif intent == 'industry':
            industry_name = ' '.join(inputs.split()[1:])
            industry_analyse_crew = IndustryCrew(job_id)
            industry_analyse_crew.setup_crew(
            industry_name)
            results = industry_analyse_crew.kickoff()
            logger.info(f"Crew for job {job_id} is complete", results)
          elif intent == 'macroeconomic':
            country = ' '.join(inputs.split()[1:])
            macro_analyse_crew = MacroeconomicCrew(job_id)
            macro_analyse_crew.setup_crew(
            country)
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

@app.route('/api/crew', methods=['POST'])
def run_crew():
    logger.info("Received request to run crew")
    # Validation
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']

    thread = Thread(target=kickoff_crew, args=(
        job_id, companies, positions))
    thread.start()

    return jsonify({"job_id": job_id}), 202

@app.route('/api/crew-analyse', methods=['POST'])
def run_crew_analyse():
    logger.info("Received request to run crew")
    # Validation
    data = request.json
    if not data or 'inputData' not in data :
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    inputData = data ['inputData']
    inputData = ' '.join(map(str, inputData))
    
    thread = Thread(target=kickoff_crew_analyse, args=(
        job_id, inputData))
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
     # Parse the job.result string into a JSON object
    try:
        result_json = json.loads(job.result)
    except json.JSONDecodeError:
        # If parsing fails, set result_json to the original job.result string
        result_json = job.result

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })
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
    """Return the current configuration for the research manager."""
    config = {
        "role": global_config.research_manager_role,
        "goal": global_config.research_manager_goal,
        "backstory": global_config.research_manager_backstory
    }
    return jsonify(config), 200

@app.route('/api/config/research-agent', methods=['GET'])
def get_research_agent_config():
    """Return the current configuration for the research agent."""
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
    """Return the current configuration for the company analyse."""
    config = {
        "searchTask": global_config.company_analyse_searchTask,
        "analyseTask": global_config.company_analyse_analyseTask
    }
    return jsonify(config), 200

@app.route('/api/config/industry-analyse', methods=['GET'])
def get_industry_analyse_config():
    """Return the current configuration for the industry analyse."""
    config = {
        "searchTask": global_config.industry_analyse_searchTask,
        "analyseTask": global_config.industry_analyse_analyseTask
    }
    return jsonify(config), 200

@app.route('/api/config/macroeconomy-analyse', methods=['GET'])
def get_macroeconomy_analyse_config():
    """Return the current configuration for the macroeconomy analyse."""
    config = {
        "searchTask": global_config.macroeconomy_analyse_searchTask,
        "analyseTask": global_config.macroeconomy_analyse_analyseTask
    }
    return jsonify(config), 200

if __name__ == '__main__':
    app.run(debug=True, port=3001)
