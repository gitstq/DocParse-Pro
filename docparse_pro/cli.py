"""
Command Line Interface for DocParse-Pro.
"""

import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from docparse_pro import DocumentParser, OCREngine, OutputFormatter, __version__

console = Console()


def print_banner():
    """Print application banner."""
    banner = Text()
    banner.append("📄 DocParse-Pro ", style="bold cyan")
    banner.append(f"v{__version__}", style="dim")
    banner.append("\n")
    banner.append("A powerful document parsing tool with OCR support", style="italic")

    console.print(Panel(banner, border_style="cyan"))


def print_supported_formats():
    """Print supported file formats."""
    parser = DocumentParser()
    table = Table(title="Supported Formats", show_header=True)
    table.add_column("Category", style="cyan")
    table.add_column("Extensions", style="green")

    formats = parser.supported_formats
    pdf_formats = [f for f in formats if f == ".pdf"]
    image_formats = [f for f in formats if f != ".pdf"]

    table.add_row("PDF", ", ".join(pdf_formats))
    table.add_row("Images", ", ".join(image_formats))

    console.print(table)


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version information")
@click.option("--formats", "-f", is_flag=True, help="Show supported formats")
@click.pass_context
def main(ctx, version, formats):
    """DocParse-Pro - Document parsing tool with OCR support."""
    if version:
        console.print(f"DocParse-Pro version {__version__}")
        return

    if formats:
        print_supported_formats()
        return

    if ctx.invoked_subcommand is None:
        print_banner()
        console.print(ctx.get_help())


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "text", "markdown", "csv"]),
    default="text",
    help="Output format",
)
@click.option("--pages", "-p", help="Pages to parse (e.g., '1-5,10,15-20')")
@click.option("--ocr", is_flag=True, help="Enable OCR for scanned documents")
@click.option("--lang", "-l", default="eng", help="OCR language (e.g., eng, chi_sim)")
@click.option("--tables", is_flag=True, default=True, help="Extract tables")
@click.option("--no-tables", is_flag=True, help="Skip table extraction")
@click.option("--verbose", "-V", is_flag=True, help="Verbose output")
def parse(
    input_file: str,
    output: Optional[str],
    format: str,
    pages: Optional[str],
    ocr: bool,
    lang: str,
    tables: bool,
    no_tables: bool,
    verbose: bool,
):
    """
    Parse a document and extract text, tables, and metadata.

    INPUT_FILE: Path to the document to parse
    """
    print_banner()

    input_path = Path(input_file)

    # Parse page range
    page_list = None
    if pages:
        page_list = parse_page_range(pages)

    extract_tables = tables and not no_tables

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Parsing {input_path.name}...", total=None)

        try:
            # Initialize parser
            parser = DocumentParser()

            # Parse document
            content = parser.parse(
                input_path,
                pages=page_list,
                extract_tables=extract_tables,
            )

            # Perform OCR if requested
            if ocr:
                progress.update(task, description="[cyan]Performing OCR...")
                ocr_engine = OCREngine(language=lang)
                ocr_results = ocr_engine.recognize_pdf(input_path, pages=page_list)

                # Merge OCR text
                ocr_text = "\n\n".join(r.text for r in ocr_results)
                if ocr_text.strip():
                    content.text = ocr_text

            progress.update(task, description="[cyan]Formatting output...")

            # Format output
            formatter = OutputFormatter(format)
            output_text = formatter.format(content)

            progress.remove_task(task)

        except FileNotFoundError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            if verbose:
                console.print_exception()
            sys.exit(1)

    # Output results
    if output:
        output_path = formatter.save(content, output)
        console.print(f"[green]✓ Output saved to: {output_path}[/green]")
    else:
        console.print("\n")
        console.print(Panel(output_text[:2000] + "..." if len(output_text) > 2000 else output_text,
                          title="Parsed Content", border_style="green"))

    # Print summary
    if verbose:
        print_summary(content)


@main.command()
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("output_dir", type=click.Path())
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "text", "markdown", "csv"]),
    default="json",
    help="Output format",
)
@click.option("--ocr", is_flag=True, help="Enable OCR")
@click.option("--lang", "-l", default="eng", help="OCR language")
@click.option("--recursive", "-r", is_flag=True, help="Process directories recursively")
@click.option("--extension", "-e", multiple=True, help="File extensions to process")
def batch(
    input_dir: str,
    output_dir: str,
    format: str,
    ocr: bool,
    lang: str,
    recursive: bool,
    extension: List[str],
):
    """
    Batch process multiple documents in a directory.

    INPUT_DIR: Directory containing documents to process
    OUTPUT_DIR: Directory to save parsed outputs
    """
    print_banner()

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find files to process
    extensions = list(extension) if extension else [".pdf", ".png", ".jpg", ".jpeg"]
    files = []

    if recursive:
        for ext in extensions:
            files.extend(input_path.rglob(f"*{ext}"))
    else:
        for ext in extensions:
            files.extend(input_path.glob(f"*{ext}"))

    if not files:
        console.print("[yellow]No files found to process.[/yellow]")
        return

    console.print(f"[cyan]Found {len(files)} files to process.[/cyan]\n")

    # Process files
    parser = DocumentParser()
    ocr_engine = OCREngine(language=lang) if ocr else None
    formatter = OutputFormatter(format)

    success_count = 0
    error_count = 0

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=len(files))

        for file in files:
            progress.update(task, description=f"[cyan]Processing {file.name}...")

            try:
                content = parser.parse(file)

                if ocr and ocr_engine:
                    ocr_results = ocr_engine.recognize_pdf(file)
                    content.text = "\n\n".join(r.text for r in ocr_results)

                # Save output
                output_file = output_path / f"{file.stem}{formatter.formatter.get_extension()}"
                formatter.save(content, output_file)

                success_count += 1

            except Exception as e:
                console.print(f"[red]Error processing {file.name}: {e}[/red]")
                error_count += 1

            progress.advance(task)

    # Print summary
    console.print("\n")
    summary_table = Table(title="Batch Processing Summary", show_header=True)
    summary_table.add_column("Status", style="cyan")
    summary_table.add_column("Count", style="green")

    summary_table.add_row("✓ Successful", str(success_count))
    if error_count:
        summary_table.add_row("✗ Failed", str(error_count))

    console.print(summary_table)


@main.command()
@click.option("--check", is_flag=True, help="Check Tesseract installation")
def ocr(check: bool):
    """OCR-related commands and configuration."""
    print_banner()

    if check:
        is_installed, info = OCREngine.check_tesseract_installed()
        if is_installed:
            console.print(f"[green]✓ Tesseract is installed (version: {info})[/green]")
            engine = OCREngine()
            langs = engine.get_available_languages()
            console.print(f"\n[cyan]Available languages:[/cyan] {', '.join(langs)}")
        else:
            console.print(f"[red]✗ Tesseract is not installed or not in PATH[/red]")
            console.print(f"[yellow]Error: {info}[/yellow]")
            console.print("\n[yellow]Install Tesseract:[/yellow]")
            console.print("  macOS: brew install tesseract")
            console.print("  Ubuntu: sudo apt-get install tesseract-ocr")
            console.print("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")


def parse_page_range(page_str: str) -> List[int]:
    """
    Parse page range string into list of page numbers.

    Examples:
        "1-5" -> [1, 2, 3, 4, 5]
        "1,3,5" -> [1, 3, 5]
        "1-5,10,15-20" -> [1, 2, 3, 4, 5, 10, 15, 16, 17, 18, 19, 20]
    """
    pages = []
    for part in page_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def print_summary(content):
    """Print parsing summary."""
    table = Table(title="Parsing Summary", show_header=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Pages", str(len(content.pages)))
    table.add_row("Text Length", f"{len(content.text):,} characters")
    table.add_row("Tables Found", str(len(content.tables)))
    table.add_row("Images Found", str(len(content.images)))

    console.print(table)


if __name__ == "__main__":
    main()
