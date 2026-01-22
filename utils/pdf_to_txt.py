import pdfplumber
from pathlib import Path

# Define directories
RAW_DIR = Path("data/raw")
EXTRACTED_DIR = Path("data/extracted")

# Ensure extracted folder exists
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a single PDF file
    """
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text:
                full_text += f"\n\n--- Page {page_number} ---\n"
                full_text += text

    return full_text


def process_all_pdfs():
    """
    Process all PDFs in data/raw and save text files
    """
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/")
        return

    for pdf_file in pdf_files:
        print(f"Extracting: {pdf_file.name}")

        extracted_text = extract_text_from_pdf(pdf_file)

        output_file = EXTRACTED_DIR / f"{pdf_file.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Saved text to: {output_file}")


if __name__ == "__main__":
    process_all_pdfs()
