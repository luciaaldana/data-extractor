class OCRProcessingError(Exception):
    """
    Custom exception for errors during the OCR processing.
    """
    def __init__(self, message: str = "An error occurred during the OCR process"):
        super().__init__(message)
        self.message = message

class ScrapingError(Exception):
    """
    Custom exception for errors during the scraping process.
    """
    def __init__(self, message: str = "An error occurred during the scraping process"):
        super().__init__(message)
        self.message = message
