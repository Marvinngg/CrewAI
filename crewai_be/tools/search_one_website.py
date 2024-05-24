from crewai_tools import WebsiteSearchTool
import json
import os

import requests
from langchain.tools import tool


class SearchWebsiteTools():

  @tool("Search on authoritative websites")
  def search_authoritative_websites(query):
    """Useful to search on authoritative websites
    about  a company's condition"""
    url = f"https://secsearch.sec.gov/search?utf8=%3F&affiliate=secsearch&query={query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
          return response.text
        else:
          print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
          return None
    except Exception as e:
        print(f"Error occurred while fetching content from {url}: {e}")
        return None



