from crewai import Task
from textwrap import dedent
from job_manager import append_event
from models import PositionInfo, PositionInfoList
from utils.logging import logger
import global_config  # 引用全局常量

class CompanyAnalysisTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)

    def collect_company_information_task(self, agent, company_name):
        return Task(
            description=dedent(global_config.company_analyse_searchTask.format(company_name=company_name)),
            agent=agent,
            callback=self.append_event_callback,
            output_json=PositionInfo,
            expected_output="A JSON object containing the researched information.",
            async_execution=True
        )

    def analyze_task(self, agent, task):
        return Task(
            description=dedent(global_config.company_analyse_analyseTask),
            agent=agent,
            context=[task],
            callback=self.append_event_callback,
            expected_output="A JSON object containing the researched information and analyse.",
            output_json=PositionInfoList
        )

    
