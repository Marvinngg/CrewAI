from crewai import Crew
from company_agents import CompanyAnalysisAgents
from company_tasks import CompanyAnalysisTasks
from industry_agents import IndustryAnalysisAgents
from industry_tasks import IndustryAnalysisTasks
from macroeconomic_agents import MacroeconomicAnalysisAgents
from macroeconomic_tasks import MacroEconomicTasks
from trip_agents import TripAgents
from trip_tasks import TripTasks
from job_manager import append_event
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
class CompanyCrew:
    """Handles the orchestration of company analysis tasks"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, company_name: str):
        agents = CompanyAnalysisAgents()
        tasks = CompanyAnalysisTasks(job_id=self.job_id)

        company_information_agent = agents.company_information_collector()
        company_analyst_agent = agents.company_analyst()

        collect_company_task = tasks.collect_company_information_task(
            agent=company_information_agent,
            company_name=company_name,
        )
        analyze_task = tasks.analyze_task(
            agent=company_analyst_agent,
            task=collect_company_task
        )

        self.crew = Crew(
            agents=[company_information_agent, company_analyst_agent],
            tasks=[collect_company_task, analyze_task],
            verbose=True
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)


class IndustryCrew:
    """Manages the execution of tasks related to industry analysis."""
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, industry_name: str):
        agents = IndustryAnalysisAgents()
        tasks = IndustryAnalysisTasks(job_id=self.job_id)

        industry_information_collector_agent = agents.industry_information_collector()
        industry_analyst_agent = agents.industry_analyst()

        collect_industry_task = tasks.collect_industry_information_task(
            agent=industry_information_collector_agent,
            industry_name=industry_name,
        )
        analyze_task = tasks.analyze_industry_task(
            agent=industry_analyst_agent,
            task=collect_industry_task
        )

        self.crew = Crew(
            agents=[industry_information_collector_agent, industry_analyst_agent],
            tasks=[collect_industry_task, analyze_task],
            verbose=True
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)


class MacroeconomicCrew:
    """Coordinates tasks for macroeconomic analysis based on country-specific data."""
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, country: str):
        agents = MacroeconomicAnalysisAgents()
        tasks = MacroEconomicTasks(job_id=self.job_id)

        macroeconomic_information_collector_agent = agents.macroeconomic_information_collector()
        macroeconomic_analyst_agent = agents.macroeconomic_analyst()

        collect_macroeconomic_task = tasks.collect_macroeconomic_task(
            agent=macroeconomic_information_collector_agent,
            country=country,
        )
        analyze_task = tasks.analyze_task(
            agent=macroeconomic_analyst_agent,
            task=collect_macroeconomic_task
        )

        self.crew = Crew(
            agents=[macroeconomic_information_collector_agent, macroeconomic_analyst_agent],
            tasks=[collect_macroeconomic_task, analyze_task],
            verbose=True
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)

class TripPlannerCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, location:str,travelto:str,date:str,hobby:str):
        agents = TripAgents()
        tasks = TripTasks(job_id=self.job_id)

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()
    
    # 在创建任务时传递 job_id 参数
        identify_task = tasks.identify_task( city_selector_agent, location, travelto, date, hobby)
        gather_task = tasks.gather_task( local_expert_agent, location, hobby, date)
        plan_task = tasks.plan_task( travel_concierge_agent, location, hobby, date)
    
        self.crew = Crew(
        agents=[
        city_selector_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[identify_task, gather_task, plan_task],
      verbose=True
    )


    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)