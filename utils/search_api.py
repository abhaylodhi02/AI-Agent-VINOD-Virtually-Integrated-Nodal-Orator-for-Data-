import requests
from config.config import SERPAPI_KEY

def search_web(query):
    params = {
        "api_key": SERPAPI_KEY,
        "q": query,
        "engine": "google",
    }
    response = requests.get("https://serpapi.com/search", params=params)
    return response.json().get("organic_results", [])
