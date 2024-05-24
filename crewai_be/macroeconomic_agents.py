from crewai import Agent
from langchain_community.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()
# tool1 = WebsiteSearchTool(website='https://example.com')
# tool2 = WebsiteSearchTool(website='https://example.com')   # 预留权威网站地址，实现在网站内容中进行语义搜索
class MacroeconomicAnalysisAgents:

    def macroeconomic_information_collector(self):
        return Agent(
            role='Macroeconomic Information Collector',
            goal='Collect comprehensive macro economic information and data for analysis,The data is preferably cutting-edge,latest (2024), authoritative, and significant',
            backstory='Experienced in gathering and organizing macroeconomic data for analysis',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
            ],    #如果要加入设置权威网站地址，可以这里加入tool1,tool2。
            verbose=True
        )

    def macroeconomic_analyst(self):
        return Agent(
            role='Macroeconomic Analyst',
            goal='Analyze macroeconomic data and trends, and provide insights and macroeconomic analysis report',
            backstory='Experienced in analyzing macroeconomic trends and forecasting',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
            ],
            verbose=True
        )


