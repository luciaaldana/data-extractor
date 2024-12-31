from urllib.parse import urlparse
from utils.scraping import scrape_all
from services.exceptions import ScrapingError
import logging

logger = logging.getLogger(__name__)

def validate_url(url: str):
    logger.debug(f"Validating URL: {url}")
    parsed = urlparse(url)

    # Verify that it has a valid scheme (http or https) and a domain
    if parsed.scheme not in ["http", "https"] or not parsed.netloc:
        logger.warning(f"Invalid URL detected: {url}")
        raise ScrapingError("The provided URL is not valid")

def scrape_website(url: str):
    """
    Performs scraping on a given webpage.

    Args:
        url (str): URL of the webpage to analyze.

    Returns:
        dict: Relevant content extracted from the webpage.

    Raises:
        ScrapingError: If an error occurs during the scraping process.
    """
    try:
        logger.info(f"Starting scraping for URL: {url}")
        
        validate_url(url)
        logger.debug(f"Validation completed for URL: {url}")
        
        result = scrape_all(url)
        logger.info(f"Scraping successfully completed for URL: {url}")
        return result

    except ScrapingError as e:
        logger.error(f"Error during scraping for URL {url}: {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during scraping for URL {url}: {str(e)}")
        raise ScrapingError(f"Unexpected error during scraping: {str(e)}")
