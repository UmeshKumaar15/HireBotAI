import PyPDF2

def extract_pdf_text(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)  # No need to open separately, FileStorage can be used directly
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"  # Extract text from each page
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text.strip()
