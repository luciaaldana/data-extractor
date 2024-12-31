import requests
from bs4 import BeautifulSoup

def scrape_all(url):
    """
    Extrae contenido de una página web: títulos, párrafos, imágenes, enlaces y tablas.
    """
    try:
        # Realiza la solicitud GET a la URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP

        # Analiza el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer diferentes tipos de contenido
        data = {
            "titles": [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'h3'])],
            "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
            "images": [img['src'] for img in soup.find_all('img', src=True)],
            "links": [a['href'] for a in soup.find_all('a', href=True)],
            "tables": extract_tables(soup)
        }

        return data
    except requests.RequestException as e:
        return {"error": f"Error al obtener la página: {e}"}
    except Exception as e:
        return {"error": f"Error al procesar la página: {e}"}


def extract_tables(soup):
    """
    Extrae las tablas de un objeto BeautifulSoup y devuelve sus filas y columnas.
    """
    tables = soup.find_all('table')
    extracted_tables = []

    for table in tables:
        # Extraer las filas
        rows = table.find_all('tr')
        table_data = []

        for row in rows:
            # Extraer las celdas (<th> o <td>)
            cells = row.find_all(['th', 'td'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            table_data.append(row_data)

        extracted_tables.append(table_data)

    return extracted_tables
