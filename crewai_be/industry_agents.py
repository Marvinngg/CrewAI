from crewai import Agent
from langchain_community.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()
# tool1 = WebsiteSearchTool(website='https://example.com')
# tool2 = WebsiteSearchTool(website='https://example.com')   # 预留权威网站地址，实现在网站内容中进行语义搜索
class IndustryAnalysisAgents:

    def industy_information_collector(self):
        return Agent(
            role='Industry Information Collector',
            goal='Collect comprehensive industry information and data for analysis,The data is preferably cutting-edge,latest (2024), authoritative, and significant',
            backstory='Experienced in gathering and organizing industy-related data for analysis',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
            ],    #如果要加入设置权威网站地址，可以这里加入tool1,tool2。
            verbose=True
        )

    def industy_analyst(self):
        return Agent(
            role='Industry Analyst',
            goal='According to the data obtained from the search, analyze the industry status and form the industry analysis report',
            backstory='Experienced in analyzing industry data to identify trends, forecast market movements',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
            ],
            verbose=True
        )


