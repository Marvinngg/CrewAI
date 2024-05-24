from crewai import Task
from textwrap import dedent
from job_manager import append_event
from models import PositionInfo, PositionInfoList
from utils.logging import logger
import global_config  # 引用全局常量

class IndustryAnalysisTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)

    def collect_industry_information_task(self, agent, industry_name):
        return Task(
            description=dedent(global_config.industry_analyse_searchTask.format(industry_name=industry_name)),
            agent=agent,
            callback=self.append_event_callback,
            output_json=PositionInfoList,
            expected_output="A JSON object containing the researched information.",
            async_execution=True
        )

    def analyze_industry_task(self, agent, task):
        return Task(
            description=dedent(global_config.industry_analyse_analyseTask),
            agent=agent,
            context=[task],
            callback=self.append_event_callback,
            expected_output="A JSON object containing the researched information and analyse.",
            output_json=PositionInfo
        )
