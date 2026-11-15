from pypdf import PdfReader
from pathlib import Path


def scan_pdf(file_path):
    """
    Extract metadata from a PDF locally.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        return {"error": "File does not exist"}

    try:
        reader = PdfReader(str(file_path))

        metadata = reader.metadata

        result = {
            "filename": file_path.name,
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "metadata": {}
        }

        if metadata:
            for key, value in metadata.items():
                result["metadata"][str(key)] = str(value)

        return result

    except Exception as error:
        return {"error": str(error)}
    
