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
    Endpoint para procesar una imagen y extraer texto utilizando OCR.

    Args:
        file (UploadFile): Imagen proporcionada por el cliente.

    Returns:
        dict: Contiene el texto extraído de la imagen.

    Raises:
        HTTPException: Si ocurre un error durante el procesamiento o extracción de texto.
    """
    logger.info("Endpoint /extract-text llamado.")
    try:
        logger.info(f"Procesando archivo: {file.filename}")

        extracted_text = await process_and_extract_text(file)

        logger.info(f"Texto extraído correctamente: {extracted_text[:50]}...")
        return {"text": extracted_text}
    except OCRProcessingError as e:
        logger.error(f"Error durante el procesamiento OCR: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.critical(f"Error inesperado durante el OCR: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during OCR.")

@router.get("/scrape/")
def scrape(url: str):
    """
    Endpoint para realizar scraping en una página web.

    Args:
        url (str): URL de la página web que se desea analizar.

    Returns:
        dict: Contiene el contenido relevante obtenido de la página web.

    Raises:
        HTTPException: Si ocurre un error durante el proceso de scraping.
    """
    logger.info(f"Scraping iniciado para URL: {url}")
    try:
        result = scrape_website(url)
        logger.info(f"Scraping exitoso para URL: {url}")
        return result
    except ScrapingError as e:
        logger.error(f"Error durante el scraping para URL {url}: {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.critical(f"Error inesperado durante el scraping para URL {url}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during scraping.")