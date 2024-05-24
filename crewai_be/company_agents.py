from crewai_tools import WebsiteSearchTool
from crewai_tools import FileReadTool
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from crewai import Agent
from tools.search_one_website import SearchWebsiteTools
class CompanyAnalysisAgents:


    def company_information_collector(self):
        return Agent(
            role='Company Information Collector',
            goal='Collect comprehensive company information and data for analysis,The data is preferably cutting-edge,latest (2024), authoritative, and significant',
            backstory='Experienced in gathering and organizing company-related data for analysis',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                #SearchWebsiteTools.search_authoritative_websites
            ],
            verbose=True
        )

    def company_analyst(self):
        return Agent(
            role='Company Analyst',
            goal='Based on the data obtained from the search, analyze the company condition and form an analysis report',
            backstory='Proficient in analyzing company profiles and assessing corporate health',
            tools=[
                BrowserTools.scrape_and_summarize_website,
                SearchTools.search_internet,
                #SearchWebsiteTools.search_authoritative_websites
            ],
            verbose=True
        )
