from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools.youtube_search_tools import YoutubeVideoSearchTool
import global_config  # 导入全局配置

class CompanyResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_manager(self, companies: List[str], positions: List[str]) -> Agent:
        return Agent(
            role=global_config.research_manager_role,
            goal=f"{global_config.research_manager_goal}\n\nCompanies: {companies}\nPositions: {positions}",
            backstory=global_config.research_manager_backstory,
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
            allow_delegation=True
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role=global_config.research_agent_role,
            goal=global_config.research_agent_goal,
            backstory=global_config.research_agent_backstory,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            llm=self.llm,
            verbose=True
        )
from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools.youtube_search_tools import YoutubeVideoSearchTool
import global_config  # 导入全局配置

class CompanyResearchAgents():

    def __init__(self):
        self.searchInternetTool = SerperDevTool()
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_manager(self, companies: List[str], positions: List[str]) -> Agent:
        return Agent(
            role=global_config.research_manager_role,
            goal=f"{global_config.research_manager_goal}\n\nCompanies: {companies}\nPositions: {positions}",
            backstory=global_config.research_manager_backstory,
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            verbose=True,
            allow_delegation=True
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role=global_config.research_agent_role,
            goal=global_config.research_agent_goal,
            backstory=global_config.research_agent_backstory,
            tools=[self.searchInternetTool, self.youtubeSearchTool],
            llm=self.llm,
            verbose=True
        )
