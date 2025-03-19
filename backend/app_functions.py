import os
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(file):
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        return extract_text(filepath)
    except Exception as e:
        return f"Error: {str(e)}"