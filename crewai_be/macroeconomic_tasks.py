from crewai import Task
from textwrap import dedent
from job_manager import append_event
from models import MacroEconomicData, MacroEconomicReport
from utils.logging import logger
import global_config

class MacroEconomicTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)

    def collect_macroeconomic_task(self, agent, country):
        return Task(
            description=dedent(global_config.macroeconomy_analyse_searchTask.format(country=country)),
            agent=agent,
            callback=self.append_event_callback,
            output_json=MacroEconomicData,
            expected_output="A JSON object containing the GDP, inflation rate, unemployment rate, interest rate, trade balance, and fiscal deficit for the country.",
            async_execution=True
        )

    def analyze_task(self, agent, task):
        return Task(
            description=dedent(global_config.macroeconomy_analyse_analyseTask),
            agent=agent,
            context=[task],
            callback=self.append_event_callback,
            output_json=MacroEconomicReport,
            expected_output="A JSON object containing the researched information and analysis, including GDP, inflation rate, unemployment rate, interest rate, trade balance, fiscal deficit, and a detailed analysis.",
        )
