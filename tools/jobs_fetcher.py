from pydantic import BaseModel, Field
from jobspy import scrape_jobs
import csv
import json

# Define the input schema for the tool
class JobScraperInput(BaseModel):
    search_term: str = Field(..., description="The job title or keywords to search for.")
    location: str = Field(..., description="The location to search for jobs (e.g., 'San Francisco, CA').")
    site_name: list[str] = Field(
        default=["indeed", "linkedin", "glassdoor", "google"],
        description="List of job boards to scrape from.",
    )
    results_wanted: int = Field(20, description="Number of job results to retrieve for each site.")
    hours_old: int = Field(72, description="Filter jobs posted within the last 'n' hours.")
    proxies: list[str] = Field(
        default=None,
        description="List of proxies in the format 'user:pass@host:port'."
    )
    country_indeed: str = Field(
        default="USA",
        description="Country filter for Indeed (e.g., 'USA', 'Canada', etc.)."
    )
    distance: int = Field(50, description="The maximum distance (in miles) for job location.")
    job_type: str = Field(None, description="The type of job (fulltime, parttime, internship, contract).")
    is_remote: bool = Field(False, description="Whether the job is remote.")
    easy_apply: bool = Field(False, description="Whether to filter for easy apply jobs.")
    description_format: str = Field("markdown", description="Format of the job description ('markdown' or 'html').")
    offset: int = Field(0, description="Offset to start the search from (useful for pagination).")
    linkedin_fetch_description: bool = Field(False, description="Whether to fetch full LinkedIn job description.")
    linkedin_company_ids: list[int] = Field(default=None, description="List of LinkedIn company IDs to filter jobs.")
    enforce_annual_salary: bool = Field(False, description="Whether to convert hourly rates to annual salary.")
    ca_cert: str = Field(None, description="Path to the CA certificate file for proxy use.")

# Define the tool function
@tool(args_schema=JobScraperInput)
def scrape_jobs_tool(
    search_term: str,
    location: str,
    site_name: list[str] = ["indeed", "linkedin", "glassdoor", "google"],
    results_wanted: int = 20,
    hours_old: int = 72,
    proxies: list[str] = None,
    country_indeed: str = "USA",
    distance: int = 50,
    job_type: str = None,
    is_remote: bool = False,
    easy_apply: bool = False,
    description_format: str = "markdown",
    offset: int = 0,
    linkedin_fetch_description: bool = False,
    linkedin_company_ids: list[int] = None,
    enforce_annual_salary: bool = False,
    ca_cert: str = None,
) -> str:
    """
    Scrapes job postings from various job boards.
    """
    try:
        # Perform the job scraping
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed,
            proxies=proxies,
            distance=distance,
            job_type=job_type,
            is_remote=is_remote,
            easy_apply=easy_apply,
            description_format=description_format,
            offset=offset,
            verbose=0,
            linkedin_fetch_description=linkedin_fetch_description,
            linkedin_company_ids=linkedin_company_ids,
            enforce_annual_salary=enforce_annual_salary,
            ca_cert=ca_cert,
        )

        # Convert the job data to JSON format and return
        return jobs.to_json(orient='records')

    except Exception as e:
        # Return a structured JSON error message
        return json.dumps({"error": "Job scraping failed", "details": str(e)})
