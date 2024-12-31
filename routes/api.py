from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ocr_service import process_and_extract_text
from services.scraping_service import scrape_website
from services.exceptions import ScrapingError, OCRProcessingError
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    Endpoint to process an image and extract text using OCR.

    Args:
        file (UploadFile): Image provided by the client.

    Returns:
        dict: Contains the text extracted from the image.

    Raises:
        HTTPException: If an error occurs during processing or text extraction.
    """
    logger.info("Endpoint /extract-text called.")
    try:
        logger.info(f"Processing file: {file.filename}")

        extracted_text = await process_and_extract_text(file)

        logger.info(f"Text successfully extracted: {extracted_text[:50]}...")
        return {"text": extracted_text}
    except OCRProcessingError as e:
        logger.error(f"Error during OCR processing: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.critical(f"Unexpected error during OCR: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during OCR.")


@router.get("/scrape/")
def scrape(url: str):
    """
    Endpoint to perform scraping on a webpage.

    Args:
        url (str): URL of the webpage to analyze.

    Returns:
        dict: Contains the relevant content obtained from the webpage.

    Raises:
        HTTPException: If an error occurs during the scraping process.
    """
    logger.info(f"Scraping started for URL: {url}")
    try:
        result = scrape_website(url)
        logger.info(f"Scraping successful for URL: {url}")
        return result
    except ScrapingError as e:
        logger.error(f"Error during scraping for URL {url}: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.critical(f"Unexpected error during scraping for URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during scraping.")
