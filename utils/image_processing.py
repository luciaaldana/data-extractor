import cv2

def preprocess_image(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Aplicar umbral binario
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Opcional: aplicar morfología para mejorar caracteres
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    processed_image = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return processed_image
