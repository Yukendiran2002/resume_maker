from main_content_extractor import MainContentExtractor
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
# Define the input schema
class ContentExtractorInput(BaseModel):
    url: str = Field(..., description="The URL of the web page to extract content from.")


# Define the Content Extractor tool
@tool(args_schema=ContentExtractorInput)
def extract_content(url: str) -> str:
    """Extract textual content from a given URL."""
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Error fetching URL: HTTP {response.status_code}"
        extracted_markdown = MainContentExtractor.extract(response.text, output_format="markdown")
        return extracted_markdown

    except Exception as e:
        return f"Error extracting content: {e}"
