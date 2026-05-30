"""
Document Parser Module - Core parsing functionality for various document formats.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pdfplumber
from PIL import Image

from docparse_pro.utils.helpers import detect_encoding, get_file_extension


@dataclass
class ParsedContent:
    """Represents parsed content from a document."""

    text: str
    tables: List[List[List[str]]]
    images: List[Image.Image]
    metadata: Dict[str, Any]
    pages: List[Dict[str, Any]]
    bounding_boxes: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "text": self.text,
            "tables": self.tables,
            "metadata": self.metadata,
            "pages": self.pages,
            "bounding_boxes": self.bounding_boxes,
            "image_count": len(self.images),
        }


class BaseParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def parse(self, file_path: Union[str, Path], **kwargs) -> ParsedContent:
        """Parse a document and return structured content."""
        pass

    @abstractmethod
    def get_page_count(self, file_path: Union[str, Path]) -> int:
        """Get the number of pages in a document."""
        pass


class PDFParser(BaseParser):
    """Parser for PDF documents using pdfplumber."""

    def parse(
        self,
        file_path: Union[str, Path],
        pages: Optional[List[int]] = None,
        extract_images: bool = True,
        extract_tables: bool = True,
        **kwargs,
    ) -> ParsedContent:
        """
        Parse a PDF document.

        Args:
            file_path: Path to the PDF file
            pages: List of page numbers to parse (1-indexed). If None, parse all pages.
            extract_images: Whether to extract images from the PDF
            extract_tables: Whether to extract tables from the PDF

        Returns:
            ParsedContent object containing all extracted data
        """
        file_path = Path(file_path)
        all_text = []
        all_tables = []
        all_images = []
        all_pages = []
        all_bounding_boxes = []

        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            target_pages = pages if pages else range(1, page_count + 1)

            for page_num in target_pages:
                if page_num < 1 or page_num > page_count:
                    continue

                page = pdf.pages[page_num - 1]
                page_data = {
                    "page_number": page_num,
                    "width": page.width,
                    "height": page.height,
                }

                # Extract text
                text = page.extract_text() or ""
                all_text.append(text)
                page_data["text"] = text

                # Extract bounding boxes for text
                chars = page.chars
                for char in chars:
                    all_bounding_boxes.append(
                        {
                            "page": page_num,
                            "text": char.get("text", ""),
                            "x0": char.get("x0", 0),
                            "y0": char.get("top", 0),
                            "x1": char.get("x1", 0),
                            "y1": char.get("bottom", 0),
                        }
                    )

                # Extract tables
                if extract_tables:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                        page_data["tables"] = len(tables)

                # Extract images
                if extract_images:
                    images = page.images
                    for img in images:
                        try:
                            # Get image dimensions
                            page_data.setdefault("images", []).append(
                                {
                                    "x0": img.get("x0", 0),
                                    "y0": img.get("top", 0),
                                    "width": img.get("width", 0),
                                    "height": img.get("height", 0),
                                }
                            )
                        except Exception:
                            pass

                all_pages.append(page_data)

        # Get metadata
        metadata = self._extract_metadata(file_path)

        return ParsedContent(
            text="\n\n".join(all_text),
            tables=all_tables,
            images=all_images,
            metadata=metadata,
            pages=all_pages,
            bounding_boxes=all_bounding_boxes,
        )

    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from PDF file."""
        metadata = {
            "filename": file_path.name,
            "file_size": file_path.stat().st_size,
        }

        try:
            with pdfplumber.open(file_path) as pdf:
                if pdf.metadata:
                    metadata.update(
                        {
                            "title": pdf.metadata.get("Title", ""),
                            "author": pdf.metadata.get("Author", ""),
                            "subject": pdf.metadata.get("Subject", ""),
                            "creator": pdf.metadata.get("Creator", ""),
                            "producer": pdf.metadata.get("Producer", ""),
                            "creation_date": pdf.metadata.get("CreationDate", ""),
                            "modification_date": pdf.metadata.get("ModDate", ""),
                        }
                    )
        except Exception:
            pass

        return metadata

    def get_page_count(self, file_path: Union[str, Path]) -> int:
        """Get the number of pages in a PDF document."""
        with pdfplumber.open(file_path) as pdf:
            return len(pdf.pages)


class ImageParser(BaseParser):
    """Parser for image files."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

    def parse(
        self,
        file_path: Union[str, Path],
        **kwargs,
    ) -> ParsedContent:
        """
        Parse an image file.

        Args:
            file_path: Path to the image file

        Returns:
            ParsedContent object containing image data
        """
        file_path = Path(file_path)
        image = Image.open(file_path)

        metadata = {
            "filename": file_path.name,
            "file_size": file_path.stat().st_size,
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height,
        }

        return ParsedContent(
            text="",  # Text will be filled by OCR
            tables=[],
            images=[image],
            metadata=metadata,
            pages=[{"page_number": 1, "width": image.width, "height": image.height}],
            bounding_boxes=[],
        )

    def get_page_count(self, file_path: Union[str, Path]) -> int:
        """Images always have 1 page."""
        return 1


class DocumentParser:
    """
    Main document parser that handles multiple file formats.
    Routes to appropriate parser based on file extension.
    """

    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {
            ".pdf": PDFParser(),
        }

        # Add image parser for all supported formats
        image_parser = ImageParser()
        for ext in ImageParser.SUPPORTED_FORMATS:
            self._parsers[ext] = image_parser

    def parse(
        self,
        file_path: Union[str, Path],
        pages: Optional[List[int]] = None,
        extract_images: bool = True,
        extract_tables: bool = True,
        **kwargs,
    ) -> ParsedContent:
        """
        Parse a document file.

        Args:
            file_path: Path to the document
            pages: Specific pages to parse (for multi-page documents)
            extract_images: Whether to extract images
            extract_tables: Whether to extract tables

        Returns:
            ParsedContent object with all extracted data

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = get_file_extension(file_path).lower()

        if ext not in self._parsers:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {list(self._parsers.keys())}"
            )

        parser = self._parsers[ext]
        return parser.parse(
            file_path,
            pages=pages,
            extract_images=extract_images,
            extract_tables=extract_tables,
            **kwargs,
        )

    def get_page_count(self, file_path: Union[str, Path]) -> int:
        """Get the number of pages in a document."""
        file_path = Path(file_path)
        ext = get_file_extension(file_path).lower()

        if ext not in self._parsers:
            raise ValueError(f"Unsupported file format: {ext}")

        return self._parsers[ext].get_page_count(file_path)

    @property
    def supported_formats(self) -> List[str]:
        """Return list of supported file formats."""
        return list(self._parsers.keys())
