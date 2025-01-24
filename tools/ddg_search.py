from langchain.tools import tool
from typing import List, Optional
from pydantic import BaseModel, Field
import duckduckgo_search as ddg


# General Search
class DuckDuckGoSearchInput(BaseModel):
    query: str = Field(..., description="The search query to be executed on DuckDuckGo.")
    max_results: int = Field(10, description="Maximum number of results to return.")
    region: str = Field("us-en", description="Region for the search (e.g., 'us-en', 'in-en').")
    safesearch: str = Field("moderate", description="Level of safe search ('off', 'moderate', 'strict').")
    time: Optional[str] = Field(None, description="Time filter for search results (e.g., 'd', 'w', 'm', 'y').")


@tool(args_schema=DuckDuckGoSearchInput)
def duckduckgo_general_search(query: str, max_results: int, region: str, safesearch: str, time: Optional[str]) -> List[dict]:
    """
    Perform a general search using the DuckDuckGo search module.
    """
    results = ddg.search(query, max_results=max_results, region=region, safesearch=safesearch, time=time)
    if not results:
        return [{"error": "No results found."}]
    return results


# Image Search
class DuckDuckGoImageSearchInput(BaseModel):
    query: str = Field(..., description="The image search query to be executed on DuckDuckGo.")
    max_results: int = Field(10, description="Maximum number of image results to return.")
    safesearch: str = Field("moderate", description="Level of safe search ('off', 'moderate', 'strict').")


@tool(args_schema=DuckDuckGoImageSearchInput)
def duckduckgo_image_search(query: str, max_results: int, safesearch: str) -> List[dict]:
    """
    Perform an image search using the DuckDuckGo search module.
    """
    results = ddg.images(query, max_results=max_results, safesearch=safesearch)
    if not results:
        return [{"error": "No image results found."}]
    return results


# News Search
class DuckDuckGoNewsSearchInput(BaseModel):
    query: str = Field(..., description="The news search query to be executed on DuckDuckGo.")
    max_results: int = Field(10, description="Maximum number of news results to return.")
    region: str = Field("us-en", description="Region for the news search (e.g., 'us-en', 'in-en').")
    safesearch: str = Field("moderate", description="Level of safe search ('off', 'moderate', 'strict').")


@tool(args_schema=DuckDuckGoNewsSearchInput)
def duckduckgo_news_search(query: str, max_results: int, region: str, safesearch: str) -> List[dict]:
    """
    Perform a news search using the DuckDuckGo search module.
    """
    results = ddg.news(query, max_results=max_results, region=region, safesearch=safesearch)
    if not results:
        return [{"error": "No news results found."}]
    return results


# Video Search
class DuckDuckGoVideoSearchInput(BaseModel):
    query: str = Field(..., description="The video search query to be executed on DuckDuckGo.")
    max_results: int = Field(10, description="Maximum number of video results to return.")
    region: str = Field("us-en", description="Region for the video search (e.g., 'us-en', 'in-en').")
    safesearch: str = Field("moderate", description="Level of safe search ('off', 'moderate', 'strict').")


@tool(args_schema=DuckDuckGoVideoSearchInput)
def duckduckgo_video_search(query: str, max_results: int, region: str, safesearch: str) -> List[dict]:
    """
    Perform a video search using the DuckDuckGo search module.
    """
    results = ddg.videos(query, max_results=max_results, region=region, safesearch=safesearch)
    if not results:
        return [{"error": "No video results found."}]
    return results
