class OCRProcessingError(Exception):
    """
    Excepción personalizada para errores durante el procesamiento de OCR.
    """
    def __init__(self, message: str = "An error occurred during the OCR process"):
        super().__init__(message)
        self.message = message

class ScrapingError(Exception):
    """
    Excepción personalizada para errores durante el proceso de scraping.
    """
    def __init__(self, message: str = "An error occurred during the scraping process"):
        super().__init__(message)
        self.message = message
