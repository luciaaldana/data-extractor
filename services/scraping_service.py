from utils.scraping import scrape_all
from fastapi import HTTPException

def scrape_website(url: str):
    result = scrape_all(url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
