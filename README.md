# Data Extractor

## Descripción

Este proyecto es una api construida con **FastAPI** que incluye dos funcionalidades principales:

1. **Procesamiento OCR**: Extrae texto de imágenes subidas utilizando Tesseract.
2. **Web Scraping**: Realiza scraping y extrae datos (títulos, párrafos, imágenes, enlaces y tablas) de una URL proporcionada.

La aplicación está diseñada para ser modular, escalable y fácil de mantener. Incluye manejo de errores y logging para facilitar la depuración y el monitoreo.

Quieres ver cómo fue el incio del proyecto? ve al archivo [DEVELOPMENT.md](DEVELOPMENT.md)

## Índice

1. [Descripción](#descripción)
2. [Funcionalidades](#funcionalidades)
3. [Tecnologías Utilizadas](#tecnologías-utilizadas)
4. [Requisitos](#requisitos)
5. [Configuración y Uso](#configuración-y-uso)
6. [Documentación de la API](#documentación-de-la-api)
   - [OCR: /extract-text/ (POST)](#ocr-extract-text-post)
   - [Scraping: /scrape/ (GET)](#scraping-scrape-get)
7. [¿Por qué usar Python en lugar de NestJS?](#por-qué-usar-python-en-lugar-de-nestjs)
8. [Contribuciones](#contribuciones)
9. [Licencia](#licencia)

## Funcionalidades

[Volver arriba](#)

- **OCR (Reconocimiento Óptico de Caracteres)**:

  - Soporte para preprocesamiento de imágenes para mejorar los resultados del OCR.
  - Extracción de texto en idiomas español e inglés.
  - Proporciona datos estructurados a partir de la extracción de texto.

- **Web Scraping**:

  - Extrae contenido estructurado de páginas web, incluyendo:
    - Títulos
    - Párrafos
    - Imágenes
    - Enlaces
    - Tablas
  - Manejo de URLs inválidas y errores de forma controlada.

- **Manejo de Errores**:

  - Excepciones personalizadas para los procesos de OCR y scraping.
  - Respuestas HTTP claras para diferentes casos de error.

- **Logging**:
  - Registra todas las acciones y errores para facilitar la depuración y el monitoreo.

---

## Tecnologías Utilizadas

[Volver arriba](#)

Este proyecto utiliza las siguientes tecnologías y herramientas:

### **Backend**

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework rápido y moderno para construir APIs con Python, basado en los estándares de OpenAPI.
- **[Python](https://www.python.org/)**: Lenguaje de programación utilizado para implementar la lógica de OCR, scraping y el backend.

### **OCR (Reconocimiento Óptico de Caracteres)**

- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)**: Herramienta de código abierto para el reconocimiento de texto en imágenes.
- **[Pytesseract](https://pypi.org/project/pytesseract/)**: Wrapper de Python para interactuar con Tesseract OCR.
- **[OpenCV](https://opencv.org/)**: Librería para procesamiento de imágenes, utilizada para preprocesar las imágenes antes de aplicar OCR.

### **Web Scraping**

- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)**: Herramienta poderosa para analizar documentos HTML y extraer datos estructurados.
- **[Requests](https://docs.python-requests.org/)**: Librería HTTP para realizar solicitudes GET y obtener datos de páginas web.

### **Despliegue**

- **[Docker](https://www.docker.com/)**: Herramienta de contenedores utilizada para empaquetar y desplegar la aplicación de manera consistente en cualquier entorno.

### **Logging**

- **[Logging (módulo estándar de Python)](https://docs.python.org/3/library/logging.html)**: Módulo para registrar información y errores durante la ejecución de la API.

### **Extras**

- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI rápido y ligero para ejecutar aplicaciones FastAPI.

## Requisitos

[Volver arriba](#)

Asegúrate de tener instalados los siguientes elementos:

- Python 3.9 o superior
- Tesseract OCR (requerido para la funcionalidad OCR)

Instala las dependencias de Python desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuración y Uso

[Volver arriba](#)

1. Clona el Repositorio

```bash
git clone <url-del-repositorio>
cd <carpeta-del-proyecto>
```

2. Instala las Dependencias. Si decides no usar Docker, instala las dependencias manualmente:

```bash
Copiar código
pip install -r requirements.txt
```

3. Ejecuta la Aplicación localmente. Utiliza uvicorn para ejecutar la aplicación FastAPI:

```bash
uvicorn main:app --reload
```

4. Ejecuta la Aplicación con Docker
   Si prefieres usar Docker, sigue estos pasos:

   1. Construye la Imagen de Docker

   ```bash
   docker build -t nombre-del-proyecto .
   ```

   2. Ejecuta el Contenedor

   ```bash
   docker run -d -p 8000:8000 nombre-del-proyecto
   ```

La aplicación se ejecutará en `http://localhost:8000`.

## Documentación de la API

[Volver arriba](#)

### Endpoints

1. `OCR: /extract-text/ (POST)`

- Descripción: Procesa una imagen subida y extrae el texto utilizando OCR.
- Parámetro:
  - file: Imagen en formato UploadFile.
- Respuesta:

```json
{
  "text": "Texto extraído de la imagen"
}
```

2. `Scraping: /scrape/ (GET)`

- Descripción: Realiza scraping en la URL proporcionada y extrae datos estructurados.
- Parámetro:
  - url: La URL de la página web.
- Respuesta:

```json
{
  "titles": ["Título 1", "Título 2"],
  "paragraphs": ["Párrafo 1", "Párrafo 2"],
  "images": ["url-imagen1.jpg", "url-imagen2.png"],
  "links": ["http://enlace1.com", "http://enlace2.com"],
  "tables": [
    ["Celda1", "Celda2"],
    ["Celda3", "Celda4"]
  ]
}
```

## ¿Por qué usar Python en lugar de NestJS?

[Volver arriba](#)

1. **Procesamiento de Imágenes (OCR)**:

   - Python cuenta con librerías maduras y bien soportadas para procesamiento de imágenes y OCR, como `OpenCV` y `pytesseract`.
   - Estas herramientas están diseñadas para integrarse fácilmente con scripts en Python y ofrecen un rendimiento robusto en tareas de procesamiento de datos.

2. **Web Scraping**:

   - Python es reconocido por sus librerías especializadas para web scraping, como `BeautifulSoup` y `requests`, que hacen que estas tareas sean más simples y menos propensas a errores.
   - NestJS, al ser más orientado al backend web, no tiene tantas herramientas dedicadas para web scraping como Python.

3. **Simplicidad y Productividad**:

   - Python permite implementar soluciones de manera rápida y concisa, especialmente en proyectos pequeños como esta API.
   - La curva de aprendizaje para las librerías mencionadas es mucho más corta en Python que configurar herramientas equivalentes en NestJS.

4. **Facilidad para Integración con Tesseract**:

   - Tesseract OCR se integra de manera nativa con Python mediante `pytesseract`, lo que facilita la implementación del reconocimiento óptico de caracteres.

5. **Naturaleza del Proyecto**:
   - Este proyecto se centra más en procesamiento de datos y menos en la estructura compleja de un backend escalable, donde NestJS sería más apropiado.
   - Python es ideal para proyectos rápidos y específicos que requieren muchas herramientas listas para usar.

## Contribuciones

[Volver arriba](#)

Si deseas contribuir al proyecto, por favor abre un pull request o crea un issue para discutir los cambios. Igualmente si tienes competarios para mejorar la app, estoy abierta a sugerencias. ¡Gracias por tu interés!

## Licencia

[Volver arriba](#)

Este proyecto está bajo la licencia [MIT](./LICENSE).
