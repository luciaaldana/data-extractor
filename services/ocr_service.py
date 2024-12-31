import cv2
import numpy as np
from utils.image_processing import preprocess_image
from utils.ocr import extract_text
from services.exceptions import OCRProcessingError
import logging

logger = logging.getLogger(__name__)

async def process_and_extract_text(file):
    """
    Processes an image and extracts text using OCR.

    Args:
        file (UploadFile): Image provided by the client.

    Returns:
        str: Text extracted from the image.

    Raises:
        OCRProcessingError: If an error occurs during processing or text extraction.
    """
    try:
        logger.info(f"Starting file processing for OCR: {file.filename}")

        # Read the image bytes
        image_bytes = await file.read()
        np_image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        if image is None:
            logger.warning(f"The file {file.filename} is not a valid image.")
            raise OCRProcessingError("The provided file is not a valid image")

        # Preprocess the image
        logger.debug("Starting image preprocessing.") 
        processed_image = preprocess_image(image)
        logger.info("Image preprocessing completed.")

        # Extract text with OCR
        logger.debug("Starting text extraction with OCR.")
        extracted_text = extract_text(processed_image)

        if not extracted_text:
            logger.warning(f"Text could not be extracted from the file {file.filename}.")
            raise OCRProcessingError("No text could be extracted from the image")

        logger.info(f"Text successfully extracted: {extracted_text[:50]}...")
        return extracted_text

    except OCRProcessingError:
        # Re-raise controlled errors
        logger.error(f"Known error during OCR for file {file.filename}.")
        raise
    except Exception as e:
        # Capture any unexpected error
        logger.critical(f"Unexpected error during OCR for file {file.filename}: {str(e)}")
        raise OCRProcessingError(f"Unexpected error during OCR: {str(e)}")
