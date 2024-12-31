from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.image_processing import preprocess_image
from utils.ocr import extract_text
from utils.ocr import extract_details
from utils.ocr import extract_lines
import cv2
import numpy as np
from utils.scraping import scrape_all

app = FastAPI()

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen (ajústalo en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Rutas y lógica del backend
@app.get("/")
def root():
    return {"message": "El backend está funcionando correctamente"}

@app.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    # Leer la imagen desde el archivo recibido
    image_bytes = await file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Preprocesar la imagen
    processed_image = preprocess_image(image)

    # Extraer texto con Tesseract
    extracted_text = extract_text(processed_image)

    print("Texto extraído:", extracted_text)


    return {"text": extracted_text}

@app.post("/extract-details/")
async def extract_details_from_image(file: UploadFile = File(...)):
    # Leer la imagen desde el archivo recibido
    image_bytes = await file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Preprocesar la imagen
    processed_image = preprocess_image(image)

    # Extraer texto con detalles en formato TSV
    details = extract_details(processed_image)

    print("Detalles extraídos:", details)

    return {"details": details}

@app.post("/extract-lines/")
async def extract_lines_from_image(file: UploadFile = File(...)):
    # Leer la imagen desde el archivo recibido
    image_bytes = await file.read()
    np_image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Preprocesar la imagen
    processed_image = preprocess_image(image)

    # Extraer texto con detalles en formato TSV
    details = extract_details(processed_image)

    # Extraer líneas de texto
    lines = extract_lines(details)

    print("Líneas extraídas:", lines)

    return {"lines": lines}



@app.get("/scrape/")
def scrape(url: str):
    """
    Endpoint para hacer scraping y obtener todo el contenido relevante de una página web.
    """
    result = scrape_all(url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


