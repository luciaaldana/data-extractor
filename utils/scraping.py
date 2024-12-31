import requests
from bs4 import BeautifulSoup

def scrape_all(url):
    """
    Extracts content from a webpage: titles, paragraphs, images, links, and tables.

    Args:
        url (str): URL of the webpage to scrape.

    Returns:
        dict: Dictionary with the extracted data from the page or an error message.

    Raises:
        Exception: If an error occurs during the request or page processing.
    """
    try:
        # Perform a GET request to the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception if there's an HTTP error

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract different types of content
        data = {
            "titles": [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            "paragraphs": [p.get_text(strip=True) for p in soup.find_all(['p', 'span'])],
            "images": [img['src'] for img in soup.find_all('img', src=True)],
            "links": [a['href'] for a in soup.find_all('a', href=True)],
            "tables": extract_tables(soup)
        }

        return data

    except requests.exceptions.MissingSchema as e:
        # Invalid URL (e.g., missing or incorrect schema)
        raise Exception(f"Error retrieving the page: Invalid schema in the URL ({e})")

    except requests.exceptions.RequestException as e:
        # Other HTTP request-related errors
        raise Exception(f"Error performing the HTTP request: {e}")

    except Exception as e:
        # General errors during page processing
        raise Exception(f"Error processing the page: {e}")

def extract_tables(soup):
    """
    Extracts tables from a BeautifulSoup object and returns their rows and columns.
    """
    tables = soup.find_all('table')
    extracted_tables = []

    for table in tables:
        # Extract the rows
        rows = table.find_all('tr')
        table_data = []

        for row in rows:
            # Extract cells (<th> or <td>)
            cells = row.find_all(['th', 'td'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            table_data.append(row_data)

        extracted_tables.append(table_data)

    return extracted_tables
