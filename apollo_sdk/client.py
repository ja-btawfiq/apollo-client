import functools
import logging
import os
import requests
import json
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)

def log_api_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as he:
            logger.error("API request failed. Code: %s, Response: %s", he.response.status_code, he.response.text)
            raise
    return wrapper


class ApolloClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Apollo API key must be provided via parameter or .env")

        self.base_url = "https://api.apollo.io/v1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            }
        )

    @log_api_exception
    def _post(self, path: str, body: dict):
        """Helper for POST requests."""
        url = f"{self.base_url}/{path}"
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()

    @log_api_exception
    def _get(self, path: str, params: dict = None):
        """Helper for GET requests."""
        url = f"{self.base_url}/{path}"
        if params is None:
            params = {}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_company_id(self, name: str):
        path = "mixed_companies/search"
        params = {"q_organization_name": name}

        resp = self._get(path, params)
        for company in resp["organizations"]:
            if name.lower() == company["name"].lower():
                return company["id"]
        raise ValueError(f"No company found for name: {name}")

    def search_people_by_company_id(self, company_id: str, page=1, title_filter=None):
        path = "mixed_people/search"
        ta_ground_level_titles = [
            "Recruiter",
            "Technical Recruiter",
            "Corporate Recruiter",
            "Contract Recruiter",
            "University Recruiter",
            "Campus Recruiter",
            "Talent Acquisition Specialist",
            "Talent Acquisition Partner",
            "Talent Acquisition Recruiter",
            "Technical Sourcer",
            "Sourcer",
            "Recruiting Coordinator",
            "Staffing Recruiter",
            "HR Recruiter",
            "IT Recruiter",
            "Engineering Recruiter",
            "Healthcare Recruiter",
            "Sales Recruiter",
            "Full-Cycle Recruiter",
        ]
        seniorities = [
            "entry",
            "senior",
            "associate",
            "partner",
            "owner",  # Some individual recruiters are "Owners" of small firms.
        ]
        params = {
            "organization_ids[]": company_id,
            "page": page,
            "person_titles[]": ta_ground_level_titles,
            "seniorities[]": seniorities,
        }
        resp = self._get(path, params)
        return resp["people"]

    def get_emails(self, person_ids: list[str]) -> list[str]:
        """
        Searches for a person's email based on first name, last name, and company.

        Returns the email address if found.
        """
        path = "people/bulk_match"
        data = []
        for id in person_ids:
            data.append({"id": id})
        body = {"details": data}
        resp = self._post(path, body)
        if not len(resp.get("matches", [])):
            raise ValueError("No emails found")
        emails = []
        for person in resp['matches']:
            if 'email' in person:
                emails.append(person['email'])
        return emails

