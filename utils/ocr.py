import pytesseract
import cv2

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def adjust_contrast(image, alpha=1.8, beta=10):
    """
    Adjusts the contrast and brightness of the image.
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def preprocess_image_advanced(image):
    """
    Preprocesses the image by adjusting contrast to improve readability.
    """
    # Adjust contrast
    processed_image = adjust_contrast(image, alpha=1.8, beta=10)
    return processed_image

def extract_text(image):
    """
    Preprocesses the image and extracts text using Tesseract.
    """
    # Preprocess the image
    processed_image = preprocess_image_advanced(image)
    
    # Configure Tesseract parameters
    custom_config = r'--oem 3 --psm 6 -l spa+eng'  # OCR with block segmentation and support for Spanish and English
    return pytesseract.image_to_string(processed_image, config=custom_config)
