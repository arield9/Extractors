import fitz
import re
import sys
import os
from pathlib import Path

import requests
import webbrowser
import argparse

import pyfiglet



class PDFExtractor:

    def __init__(self, file_path):
        self.file_path = file_path
        
    def pdf_text_reader(self):
        try:
            with fitz.open(self.file_path) as pdf:
                # Gets the pages range that the user wants to print
                pages_range = pdf.pages(int(input("The page to start from: ")),int(input("The page to end with: ")))
                text = chr(12).join([page.get_text() for page in pages_range])
                print(text)
        except FileNotFoundError:
            print(f"File not found, please make sure it's the right path: {self.file_path}")

    def pdf_file_extractor(self):
        try:
            with fitz.open(self.file_path) as pdf:
                embedded_files = pdf.embfile_count()
                for emb_file in range(embedded_files):
                    file_name = str(pdf.embfile_names())
                    dir = Path(os.environ.get('USERPROFILE')) / 'Desktop'
                    suffix = ".bin"
                    save_path = os.path.join(dir, file_name + suffix)
                    with Path.open(save_path, "wb") as file:
                        file_data = pdf.embfile_get(0)
                        file.write(file_data)
                        print("The extracted file created on your Desktop")
        except FileNotFoundError:
            print(f"File not found, please make sure it's the right path: {self.file_path}")

    def pdf_metadata(self):
        try:
            with fitz.open(self.file_path) as pdf:
                last_mod = pdf.metadata["modDate"]
                creat_date = pdf.metadata["creationDate"]
                print(f"""
                    The date that the file was created: {creat_date}
                    The last date the file was modified: {last_mod}""")
        except FileNotFoundError:
            print(f"File not found, please make sure it's the right path: {self.file_path}")

    def pdf_url_extractor(self):
        try:
            with fitz.open(self.file_path) as pdf:
                content = chr(12).join([page.get_text() for page in pdf])
                url_matches = re.findall(r"(https?://[a-zA-Z0-9.=-]+(?:/[^\"\']*?)?)", content)

                if url_matches:
                    for url in url_matches:
                        print(url)
                        PDFExtractor.process_url(url)
                else:
                    print("No URLs were extracted from the PDF")
        except FileNotFoundError:
            print(f"File not found, please make sure it's the right path: {self.file_path}")

    def process_url(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"Browsing into {url}")
                webbrowser.open(url)
        except Exception as err:
            print(err)


def main():
    
    ascii_banner = pyfiglet.figlet_format("PDF Extractor")
    print(ascii_banner)

    parser = argparse.ArgumentParser(prog="PDF Extractor", description="Extracting Text, URLs, Metadata and embedded files from PDFs")
    parser.add_argument("file_path", type=Path, help="Enter your file path to extract")
    parser.add_argument("-t", "--text", action="store_true", help="Extracts the text from the PDF")
    parser.add_argument("-e", "--embedded", action="store_true", help="Extracts the embedded files from the PDF")
    parser.add_argument("-m", "--metadata", action="store_true", help="Extracts Metadata of the PDF")
    parser.add_argument("-u", "--urls", action="store_true", help="Extracts URLs from the PDF")
    options = parser.parse_args()   
    pdf_extractor = PDFExtractor(options.file_path)

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    if options.text:
        pdf_extractor.pdf_text_reader()
    if options.embedded:
        pdf_extractor.pdf_file_extractor()
    if options.metadata:
        pdf_extractor.pdf_metadata()
    if options.urls:
        pdf_extractor.pdf_url_extractor()


if __name__ == "__main__":
    main()
    