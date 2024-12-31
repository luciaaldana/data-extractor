import pytesseract
import cv2

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def adjust_contrast(image, alpha=1.8, beta=10):
    """
    Ajusta el contraste y el brillo de la imagen.
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def preprocess_image_advanced(image):
    """
    Preprocesa la imagen ajustando el contraste para mejorar la legibilidad.
    """
    # Ajustar contraste
    processed_image = adjust_contrast(image, alpha=1.8, beta=10)
    return processed_image

def extract_text(image):
    """
    Preprocesa la imagen y extrae el texto con Tesseract.
    """
    # Preprocesar la imagen
    processed_image = preprocess_image_advanced(image)
    
    # Configurar parámetros de Tesseract
    custom_config = r'--oem 3 --psm 6 -l spa+eng'  # OCR con segmentación de bloques y soporte para español e inglés
    return pytesseract.image_to_string(processed_image, config=custom_config)

def extract_lines(details):
    """
    Extrae un array con un elemento por cada línea de texto de la imagen.
    """
    lines = {}
    for i, line_num in enumerate(details['line_num']):
        if line_num not in lines:
            lines[line_num] = []
        lines[line_num].append(details['text'][i])

    # Convertir líneas en un array de strings
    return [" ".join(words).strip() for words in lines.values() if words]

def group_by_lines(details):
    """
    Agrupa las palabras por líneas usando el número de línea.
    """
    lines = {}
    for i, line_num in enumerate(details['line_num']):
        if line_num not in lines:
            lines[line_num] = []
        lines[line_num].append(details['text'][i])
    
    # Convertir las líneas en texto unificado
    grouped_lines = {line: " ".join(words).strip() for line, words in lines.items() if words}
    return grouped_lines

def extract_details(image):
    """
    Preprocesa la imagen y extrae el texto con Tesseract.
    """
    # Preprocesar la imagen
    processed_image = preprocess_image_advanced(image)
    
    """
    Extrae texto y detalles adicionales de la imagen usando el formato TSV.
    """
    # Configurar parámetros de Tesseract
    custom_config = r'--oem 3 --psm 6 -l spa+eng'  # OCR con segmentación de bloques y soporte para español e inglés
    tsv_data = pytesseract.image_to_data(processed_image, config=custom_config, output_type=pytesseract.Output.DICT)

    # grouped_lines = group_by_lines(tsv_data)

    return tsv_data



