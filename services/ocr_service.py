import cv2
import numpy as np
from utils.image_processing import preprocess_image
from utils.ocr import extract_text
from services.exceptions import OCRProcessingError
import logging

logger = logging.getLogger(__name__)

async def process_and_extract_text(file):
    """
    Procesa una imagen y extrae texto utilizando OCR.

    Args:
        file (UploadFile): Imagen proporcionada por el cliente.

    Returns:
        str: Texto extraído de la imagen.

    Raises:
        OCRProcessingError: Si ocurre un error durante el procesamiento o extracción de texto.
    """
    try:
        logger.info(f"Iniciando procesamiento de archivo para OCR: {file.filename}")

        # Leer los bytes de la imagen
        image_bytes = await file.read()
        np_image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        if image is None:
            logger.warning(f"El archivo {file.filename} no es una imagen válida.")
            raise OCRProcessingError("The provided file is not a valid image")

        # Preprocesar la imagen
        logger.debug("Iniciando preprocesamiento de la imagen.") 
        processed_image = preprocess_image(image)
        logger.info("Preprocesamiento de la imagen completado.")

        # Extraer texto con OCR
        logger.debug("Iniciando extracción de texto con OCR.")
        extracted_text = extract_text(processed_image)

        if not extracted_text:
            logger.warning(f"No se pudo extraer texto del archivo {file.filename}.")
            raise OCRProcessingError("No text could be extracted from the image")

        logger.info(f"Texto extraído con éxito: {extracted_text[:50]}...")
        return extracted_text

    except OCRProcessingError:
        # Re-lanzar errores controlados
        logger.error(f"Error conocido durante el OCR para archivo {file.filename}.")
        raise
    except Exception as e:
        # Capturar cualquier error inesperado
        logger.critical(f"Error inesperado durante el OCR para archivo {file.filename}: {str(e)}")
        raise OCRProcessingError(f"Unexpected error during OCR: {str(e)}")
