from langchain.tools import tool
from typing import List
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import playwright.sync_api
import time
import subprocess
# Define the input schema for GoogleSearchTool
class GoogleSearchInput(BaseModel):
    query: str = Field(..., description="The search query to be executed on Google.")


# Define the Google Search tool
@tool(args_schema=GoogleSearchInput)
def google_search(query: str) -> List[dict]:
    """Fetch Google search results for a given query."""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://www.google.co.in/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    params = {
        'q': query,
        'hl': 'en',
        'lr': 'lang_en',
        'gl': 'in',
        'num': 100
    }

    response = requests.get('https://www.google.com/search', params=params, headers=headers)
    if response.status_code != 200:
        return [{"error": f"Failed to fetch results. HTTP Status: {response.status_code}"}]

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        try:
            link = g.find('a', href=True)
            title = g.find('h3')
            description = g.select_one(".Hdw6tb")
            if link and title:
                results.append({
                    'title': title.get_text(),
                    'link': link['href'],
                    'description': description.get_text() if description else ''
                })
                # time.sleep(5)
        except Exception as e:
            results.append({"error": f"Parsing error: {str(e)}"})

    return results
