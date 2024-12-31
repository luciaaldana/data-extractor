from fastapi import APIRouter, UploadFile, File
from services.ocr_service import process_and_extract_text
from services.scraping_service import scrape_website

router = APIRouter()

@router.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    Endpoint para procesar una imagen y extraer texto utilizando OCR.

    Args:
        file (UploadFile): Imagen cargada por el usuario en formato JPEG o PNG.

    Returns:
        dict: Contiene el texto extraído de la imagen.
    """
    extracted_text = await process_and_extract_text(file)
    return {"text": extracted_text}

@router.get("/scrape/")
def scrape(url: str):
    """
    Endpoint para realizar scraping en una página web.

    Args:
        url (str): URL de la página web que se desea analizar.

    Returns:
        dict: Contiene el contenido relevante obtenido de la página web, 
              o un mensaje de error si el scraping falla.

    Raises:
        HTTPException: Si ocurre un error durante el proceso de scraping 
                       o si la URL no es válida.
    """
    return scrape_website(url)
