"""
Tests for DocParse-Pro.
"""

import pytest
from pathlib import Path
from docparse_pro import DocumentParser, OutputFormatter
from docparse_pro.parser import ParsedContent


class TestDocumentParser:
    """Tests for DocumentParser class."""

    def test_supported_formats(self):
        """Test that supported formats are returned."""
        parser = DocumentParser()
        formats = parser.supported_formats

        assert ".pdf" in formats
        assert ".png" in formats
        assert ".jpg" in formats

    def test_unsupported_format(self, tmp_path):
        """Test that unsupported format raises error."""
        parser = DocumentParser()
        test_file = tmp_path / "test.xyz"
        test_file.write_text("test")

        with pytest.raises(ValueError, match="Unsupported file format"):
            parser.parse(test_file)

    def test_file_not_found(self):
        """Test that missing file raises error."""
        parser = DocumentParser()

        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/file.pdf")


class TestOutputFormatter:
    """Tests for OutputFormatter class."""

    def test_supported_formats(self):
        """Test that supported formats are returned."""
        formats = OutputFormatter.get_supported_formats()

        assert "json" in formats
        assert "text" in formats
        assert "markdown" in formats
        assert "csv" in formats

    def test_unsupported_format(self):
        """Test that unsupported format raises error."""
        with pytest.raises(ValueError, match="Unsupported format"):
            OutputFormatter("invalid_format")

    def test_json_format(self):
        """Test JSON output formatting."""
        content = ParsedContent(
            text="Test content",
            tables=[],
            images=[],
            metadata={"title": "Test"},
            pages=[{"page_number": 1}],
            bounding_boxes=[],
        )

        formatter = OutputFormatter("json")
        output = formatter.format(content)

        assert '"text": "Test content"' in output
        assert '"title": "Test"' in output

    def test_text_format(self):
        """Test text output formatting."""
        content = ParsedContent(
            text="Test content",
            tables=[],
            images=[],
            metadata={"filename": "test.pdf"},
            pages=[{"page_number": 1}],
            bounding_boxes=[],
        )

        formatter = OutputFormatter("text")
        output = formatter.format(content)

        assert "Test content" in output
        assert "test.pdf" in output

    def test_markdown_format(self):
        """Test Markdown output formatting."""
        content = ParsedContent(
            text="Test content",
            tables=[[["Header1", "Header2"], ["Data1", "Data2"]]],
            images=[],
            metadata={"title": "Test Document"},
            pages=[{"page_number": 1}],
            bounding_boxes=[],
        )

        formatter = OutputFormatter("markdown")
        output = formatter.format(content)

        assert "# Document Analysis Report" in output
        assert "Test content" in output
        assert "| Header1 | Header2 |" in output


class TestParsedContent:
    """Tests for ParsedContent dataclass."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        content = ParsedContent(
            text="Sample text",
            tables=[],
            images=[],
            metadata={"key": "value"},
            pages=[],
            bounding_boxes=[],
        )

        result = content.to_dict()

        assert result["text"] == "Sample text"
        assert result["metadata"]["key"] == "value"
        assert result["image_count"] == 0
