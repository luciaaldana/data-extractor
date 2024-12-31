from utils.image_processing import preprocess_image
from utils.ocr import extract_text
import cv2
import numpy as np

async def process_and_extract_text(file):
    # Leer la imagen desde el archivo recibido
    image_bytes = await file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Preprocesar la imagen
    processed_image = preprocess_image(image)

    # Extraer texto con Tesseract
    extracted_text = extract_text(processed_image)

    return extracted_text
