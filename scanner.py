from pathlib import Path

from metapeek.image_scanner import scan_image
from metapeek.pdf_scanner import scan_pdf
from metapeek.risk_checker import check_risks
from metapeek.reporter import display_report


def scan_file(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        print("Error: File does not exist.")
        return

    extension = file_path.suffix.lower()

    print("\n[*] Starting MetaPeek scan...")

    if extension in [".jpg", ".jpeg", ".png", ".tiff", ".tif"]:
        scan_result = scan_image(file_path)

    elif extension == ".pdf":
        scan_result = scan_pdf(file_path)

    else:
        print("[!] Unsupported file type.")
        return

    risk_result = check_risks(scan_result)

    display_report(scan_result, risk_result)
    
