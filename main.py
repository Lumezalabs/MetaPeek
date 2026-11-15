from pathlib import Path
from metapeek.scanner import scan_file


def main():
    print("\033[92m")
    print("=" * 50)
    print("              METAPEEK")
    print("          METADATA SCANNER")
    print("=" * 50)
    print("\033[0m")

    file_path = input("\n[?] Enter file path to scan: ").strip()
    file_path = file_path.strip('"').strip("'")

    if not file_path:
        print("[!] No file path provided.")
        return

    scan_file(Path(file_path))


if __name__ == "__main__":
    main()
