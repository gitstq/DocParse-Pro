"""
OCR Engine Module - Text recognition from images and scanned documents.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from PIL import Image

from docparse_pro.utils.helpers import get_file_extension


@dataclass
class OCRResult:
    """Represents OCR result with text and bounding boxes."""

    text: str
    confidence: float
    bounding_boxes: List[Dict[str, Any]]
    language: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_boxes": self.bounding_boxes,
            "language": self.language,
        }


class OCREngine:
    """
    OCR Engine using Tesseract for text recognition.
    Supports multiple languages and provides confidence scores.
    """

    # Common language codes mapping
    LANGUAGE_MAP = {
        "en": "eng",
        "english": "eng",
        "zh": "chi_sim",
        "chinese": "chi_sim",
        "zh-cn": "chi_sim",
        "zh-tw": "chi_tra",
        "japanese": "jpn",
        "ja": "jpn",
        "korean": "kor",
        "ko": "kor",
        "french": "fra",
        "fr": "fra",
        "german": "deu",
        "de": "deu",
        "spanish": "spa",
        "es": "spa",
    }

    def __init__(
        self,
        language: str = "eng",
        tesseract_cmd: Optional[str] = None,
        tessdata_path: Optional[str] = None,
    ):
        """
        Initialize OCR engine.

        Args:
            language: Language code for OCR (e.g., 'eng', 'chi_sim')
            tesseract_cmd: Path to tesseract executable
            tessdata_path: Path to tessdata directory
        """
        self.language = self._normalize_language(language)

        if tesseract_cmd:
            import pytesseract

            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        if tessdata_path:
            os.environ["TESSDATA_PREFIX"] = tessdata_path

    def _normalize_language(self, language: str) -> str:
        """Normalize language code to Tesseract format."""
        lang_lower = language.lower()
        return self.LANGUAGE_MAP.get(lang_lower, language)

    def recognize(
        self,
        image: Union[str, Path, Image.Image],
        lang: Optional[str] = None,
        config: str = "",
        return_confidence: bool = True,
    ) -> OCRResult:
        """
        Perform OCR on an image.

        Args:
            image: Image file path or PIL Image object
            lang: Language for OCR (overrides default)
            config: Tesseract configuration string
            return_confidence: Whether to return confidence scores

        Returns:
            OCRResult object with recognized text and metadata
        """
        import pytesseract

        # Load image if path provided
        if isinstance(image, (str, Path)):
            image = Image.open(image)

        # Use provided language or default
        ocr_lang = self._normalize_language(lang) if lang else self.language

        # Perform OCR
        try:
            if return_confidence:
                # Get detailed data with confidence
                data = pytesseract.image_to_data(
                    image, lang=ocr_lang, config=config, output_type=pytesseract.Output.DICT
                )

                # Extract text and bounding boxes
                text_parts = []
                bounding_boxes = []
                confidences = []

                for i, txt in enumerate(data["text"]):
                    if txt.strip():
                        text_parts.append(txt)
                        bounding_boxes.append(
                            {
                                "text": txt,
                                "x": data["left"][i],
                                "y": data["top"][i],
                                "width": data["width"][i],
                                "height": data["height"][i],
                                "confidence": data["conf"][i],
                            }
                        )
                        if data["conf"][i] > 0:
                            confidences.append(data["conf"][i])

                text = " ".join(text_parts)
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            else:
                # Simple text extraction
                text = pytesseract.image_to_string(image, lang=ocr_lang, config=config)
                bounding_boxes = []
                avg_confidence = 0.0

            return OCRResult(
                text=text.strip(),
                confidence=avg_confidence,
                bounding_boxes=bounding_boxes,
                language=ocr_lang,
            )

        except Exception as e:
            raise RuntimeError(f"OCR failed: {str(e)}")

    def recognize_pdf(
        self,
        pdf_path: Union[str, Path],
        pages: Optional[List[int]] = None,
        dpi: int = 300,
        lang: Optional[str] = None,
    ) -> List[OCRResult]:
        """
        Perform OCR on a PDF document.

        Args:
            pdf_path: Path to PDF file
            pages: List of page numbers to process (1-indexed)
            dpi: Resolution for rendering PDF pages
            lang: Language for OCR

        Returns:
            List of OCRResult objects, one per page
        """
        import pdfplumber

        pdf_path = Path(pdf_path)
        results = []

        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            target_pages = pages if pages else range(1, page_count + 1)

            for page_num in target_pages:
                if page_num < 1 or page_num > page_count:
                    continue

                page = pdf.pages[page_num - 1]

                # Convert page to image
                im = page.to_image(resolution=dpi)
                pil_image = im.original

                # Perform OCR
                result = self.recognize(pil_image, lang=lang)
                results.append(result)

        return results

    def get_available_languages(self) -> List[str]:
        """Get list of available OCR languages."""
        import pytesseract

        try:
            langs = pytesseract.get_languages()
            return sorted(langs)
        except Exception:
            return ["eng"]  # Default fallback

    @staticmethod
    def check_tesseract_installed() -> Tuple[bool, str]:
        """
        Check if Tesseract is installed and accessible.

        Returns:
            Tuple of (is_installed, version_or_error_message)
        """
        import pytesseract

        try:
            version = pytesseract.get_tesseract_version()
            return True, str(version)
        except Exception as e:
            return False, str(e)
