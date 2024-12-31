# Usa una imagen base de Python
FROM python:3.9-slim

# Instala dependencias del sistema necesarias para OpenCV y Tesseract
RUN apt-get update && apt-get install -y \
  tesseract-ocr \
  tesseract-ocr-spa \
  libsm6 libxext6 libxrender-dev \
  && apt-get clean

# Configura la variable de entorno para que Tesseract encuentre los datos del idioma
# ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Crea un directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
