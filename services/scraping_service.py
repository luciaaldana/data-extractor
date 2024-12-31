from urllib.parse import urlparse
from utils.scraping import scrape_all
from services.exceptions import ScrapingError
import logging

logger = logging.getLogger(__name__)

def validate_url(url: str):
    logger.debug(f"Validando la URL: {url}")
    parsed = urlparse(url)

    # Verificar que tenga un esquema válido (http o https) y un dominio
    if parsed.scheme not in ["http", "https"] or not parsed.netloc:
        logger.warning(f"URL no válida detectada: {url}")
        raise ScrapingError("The provided URL is not valid")

def scrape_website(url: str):
    """
    Realiza el scraping de una página web dada.

    Args:
        url (str): URL de la página web que se desea analizar.

    Returns:
        dict: Contenido relevante extraído de la página web.

    Raises:
        ScrapingError: Si ocurre un error en el proceso de scraping.
    """
    try:
        logger.info(f"Iniciando scraping para URL: {url}")
        
        validate_url(url)
        logger.debug(f"Validación completada para URL: {url}")
        
        result = scrape_all(url)
        logger.info(f"Scraping completado con éxito para URL: {url}")
        return result

    except ScrapingError as e:
        logger.error(f"Error durante el scraping para URL {url}: {e.message}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado durante el scraping para URL {url}: {str(e)}")
        raise ScrapingError(f"Unexpected error during scraping: {str(e)}")
