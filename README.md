# Construcción backend con Python en Docker

## 1. Preparar tu entorno de desarrollo

### 1.1. Crea una carpeta para tu proyecto

```bash
mkdir data-extractor && cd data-extractor
```

Empezamos construyendo un POST para extraer texto de una imagen con Tesseract.

### 1.2. Estructura del proyecto: Extraer texto de una imagen (Tesseract)

```python
data-extractor/
  ├── Dockerfile
  ├── docker-compose.yml  # Opcional (Si lo usaremos)
  ├── requirements.txt
  ├── main.py
  └── utils/
      ├── image_processing.py
      ├── ocr.py
      └── __init__.py
```

`Dockerfile`: contiene instrucciones para crear una imagen de Docker con todas las dependencias necesarias para ejecutar tu aplicación.

```python
# Usa una imagen base de Python
FROM python:3.9-slim

# Instala dependencias del sistema necesarias para OpenCV y Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 libxext6 libxrender-dev \
    && apt-get clean

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
```

`docker-compose.yml`: es un archivo opcional que define y ejecuta aplicaciones Docker de múltiples contenedores.

```python
version: "3.8"
services:
  data-extractor:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
```

`requirements.txt`: lista de dependencias de Python que se instalarán en la imagen de Docker.

```python
fastapi
uvicorn
python-multipart
opencv-python-headless
pytesseract
```

`main.py`: punto de entrada para tu aplicación.

`utils/`: carpeta que contiene módulos de utilidad para tu aplicación.

## 2. Construir y ejecutar el contenedor

Construir la imagen:

```bash
docker build -t data-extractor .
```

Ejecutar el contenedor:

```bash
docker run -d -p 8000:8000 data-extractor
```

Si usas (en este caso si) `docker-compose`:

```bash
docker-compose up -d
```

```bash
## Para parar y borrar un contenedor de Docker:

## Lista de contenedores, de donde sacaremos el ID del contenedor que nos interesa
docker ps a

## Parar el contenedor
docker stop ID_CONTENEDOR

## Borrar la contenedor
docker rm ID_CONTENEDOR
```

## 3. Probar en Postman

Abre Postman y, con el contenedor corriendo:

- Haz una petición `POST` a `localhost:8000/extract_text` con una imagen adjunta en el formulario:
- Ve a la pestaña Body y selecciona form-data.
- Añade un campo con `Key: file` y en `Value: Haz clic en "Select File" y elige una imagen de tu sistema`.
- Envía la solicitud y revisa la respuesta.

## 4. Agregar Español a la configuración de Tesseract

### 4.1 Pasos para la instalación

- Abre la terminal de tu sistema operativo y ejecuta:

  ```bash
  docker ps
  ```

Esto te listará los contenedores. Busca el nombre del contenedor que neccesitas. Ejemplo del resultado:

```bash
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                  NAMES
abcdef123456   data-extractor   "uvicorn main:app --…"   10 minutes ago   Up 10 minutes   0.0.0.0:8000->8000/tcp    de-container
```

De aquí obtenemos el nombre `de-container`.

- Accede al contenedor. Ahora que sabes el nombre del contenedor, usa este comando para abrir una terminal dentro de él:

```bash
docker exec -it de-container /bin/bash
```

Este comando abrirá una sesión interactiva dentro del contenedor, como si estuvieras en una máquina Linux.

- Dentro del contenedor, descarga los datos necesarios para el idioma español en Tesseract:

```bash
apt-get update && apt-get install -y tesseract-ocr-spa
```

- Sigue en la terminal del contenedor y verifica que el idioma español esté instalado:

```bash
tesseract --list-langs
```

- Sal del contenedor: Una vez hecho, escribe `exit` para salir de la terminal del contenedor y volver a la terminal de tu sistema.

- Ve al archivo `ocr.py` y agrega los idiomas que usarás. Por ejemplo: -l spa+eng.

```diff
import pytesseract
import cv2

def extract_text(image):
++ custom_config = r'--oem 3 --psm 6 -l spa+eng'
   return pytesseract.image_to_string(image, config=custom_config)
```

### 4.2 Qué debes hacer después de instalar el idioma dentro del contenedor

¿Requieres volver a ejecutar el build del contenedor? Depende:

- Si hiciste cambios manuales (como instalar el idioma dentro del contenedor):

  Los cambios realizados manualmente dentro del contenedor no son persistentes. Si detienes y vuelves a iniciar el contenedor, perderás esos cambios.

  Para que los cambios sean permanentes añade los comandos de instalación de Tesseract y del idioma español en el archivo Dockerfile:

  ```python
  RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa
  ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/
  ```

  Luego, reconstruye la imagen del contenedor:

  ```bash
  docker-compose up --build
  ```

- Si no necesitas persistencia inmediata:

  Puedes seguir usando el contenedor actual, ya que los cambios que hiciste manualmente seguirán funcionando mientras el contenedor no se detenga.

  Para mantener el contenedor corriendo:

  - No lo bajes con `docker-compose down`.

  - Solo detén temporalmente el contenedor si necesitas reiniciar algo con:

  ```bash
  docker-compose stop
  ```

  - Y vuélvelo a iniciar con:

  ```bash
  docker-compose start
  ```

Si bajas el contenedor (por ejemplo, con docker-compose down), perderás los cambios manuales que hiciste dentro de él. Por eso, la mejor práctica es agregar los cambios al Dockerfile y reconstruir el contenedor. Esto garantiza que los cambios estén reflejados en la imagen y sean persistentes.

### 4.3 Error en la ubicación de archivos de idiomas de Tesseract

Ejemplo de error al probar el endpoint de OCR:

```bash
| pytesseract.pytesseract.TesseractError: (1, 'Error opening data file /usr/share/tesseract-ocr/4.00/spa.traineddata Please make sure the TESSDATA_PREFIX environment variable is set to your "tessdata" directory. Failed loading language \'spa\' Tesseract couldn\'t load any languages! Could not initialize tesseract.')
```

Este error ocurre porque, a pesar de haber configurado la variable TESSDATA_PREFIX, Tesseract no encuentra el archivo de datos del idioma español (spa.traineddata) en la ubicación esperada. Aquí está cómo resolverlo paso a paso:

1. Verifica la ubicación real de los archivos `*.traineddata`

- Accede al contenedor Docker:

```bash
docker exec -it de-container /bin/bash
```

- Busca dónde están los archivos de idioma instalados:

```bash
find / -name "spa.traineddata"
```

Este comando buscará el archivo `spa.traineddata` en todo el sistema de archivos del contenedor. Algunas ubicaciones comunes son:

/usr/share/tesseract-ocr/4.00/tessdata/
/usr/local/share/tessdata/
Anota la ruta exacta donde se encuentra spa.traineddata.

2. Ajusta la variable TESSDATA_PREFIX

Con la ubicación exacta de spa.traineddata, actualiza la variable de entorno `TESSDATA_PREFIX`.

Si estás en el contenedor, configúrala temporalmente:

```bash
export TESSDATA_PREFIX=/ruta/encontrada/tessdata/
#Reemplaza /ruta/encontrada/tessdata/ con la ruta real que obtuviste en el paso anterior.
```

Verifica que Tesseract puede listar los idiomas:

```bash
tesseract --list-langs
#Si ves spa, significa que ya está configurado correctamente.
```

3. Hacer la configuración persistente
   Para que esta configuración sea permanente y no tengas que configurarla manualmente cada vez, actualiza tu archivo `Dockerfile` con la ruta correcta.

Abre tu Dockerfile y edita la línea ENV TESSDATA_PREFIX:

```dockerfile
ENV TESSDATA_PREFIX=/ruta/encontrada/tessdata/
```

Reconstruye el contenedor:

```bash
docker-compose up --build
```

## 5. Agregar endpoint para Web Scraping

Vamos a integrar un web scraping al backend usando `BeautifulSoup` (de la biblioteca `bs4`).

1. Instalar las dependencias necesarias

Abre tu archivo `requirements.txt` y añade las siguientes líneas al final:

```text
beautifulsoup4
requests
```

2. Crear un archivo para el scraping

En la carpeta utils de tu proyecto, crea un archivo nuevo llamado `scraping.py`.

```python
import requests
from bs4 import BeautifulSoup

def scrape_titles(url):
    """
    Extrae los títulos <h1> y <h2> de una página web dada.
    """
    try:
        # Realiza la solicitud GET a la URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP

        # Analiza el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra todos los <h1> y <h2>
        titles = [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2'])]

        return {"titles": titles}
    except requests.RequestException as e:
        return {"error": f"Error al obtener la página: {e}"}
    except Exception as e:
        return {"error": f"Error al procesar la página: {e}"}
```

3. Añadir el endpoint al backend

- Abre tu archivo `main.py`.

- Importa la función `scrape_titles` desde `utils/scraping.py`. Añade esta línea cerca de los otros imports:

  ```python
  from utils.scraping import scrape_titles
  ```

- Añade el nuevo endpoint al archivo main.py justo debajo de los otros endpoints:

  ```python
  @app.get("/scrape/")
  def scrape(url: str):
      """
      Endpoint para hacer scraping y obtener títulos <h1> y <h2> de una página web.
      """
      result = scrape_titles(url)
      if "error" in result:
          raise HTTPException(status_code=400, detail=result["error"])
      return result
  ```

4. Levantar el backend

Guarda todos los cambios y ejecuta el siguiente comando para reconstruir tu contenedor con las nuevas dependencias:

```bash
docker-compose up --build
```

5. Probar el nuevo endpoint

Usando Postman, configura una nueva solicitud:

- Método: GET
- URL: http://localhost:8000/scrape/?url=https://example.com
- Haz clic en "Send" y revisa la respuesta.
