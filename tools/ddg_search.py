from langchain.tools import tool
from typing import List, Optional
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS


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
    Perform a general text search using the updated DuckDuckGo search module.
    """
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            region=region,
            safesearch=safesearch,
            timelimit=time,  # new API uses 'timelimit' instead of 'time'
            max_results=max_results,
            backend="auto"
        )
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
    Perform an image search using the updated DuckDuckGo search module.
    """
    with DDGS() as ddgs:
        results = ddgs.images(
            keywords=query,
            safesearch=safesearch,
            max_results=max_results
        )
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
    Perform a news search using the updated DuckDuckGo search module.
    """
    with DDGS() as ddgs:
        results = ddgs.news(
            query,
            region=region,
            safesearch=safesearch,
            timelimit=None,
            max_results=max_results
        )
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
    Perform a video search using the updated DuckDuckGo search module.
    """
    with DDGS() as ddgs:
        results = ddgs.videos(
            query,
            region=region,
            safesearch=safesearch,
            timelimit=None,
            max_results=max_results
        )
    if not results:
        return [{"error": "No video results found."}]
    return results
