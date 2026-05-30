"""
DocParse-Pro - A powerful document parsing tool with OCR, table extraction, and multi-format output support.
"""

__version__ = "1.0.0"
__author__ = "DocParse-Pro Team"

from docparse_pro.parser import DocumentParser
from docparse_pro.ocr import OCREngine
from docparse_pro.output import OutputFormatter

__all__ = ["DocumentParser", "OCREngine", "OutputFormatter", "__version__"]
