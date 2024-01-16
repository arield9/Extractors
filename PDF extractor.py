import fitz
import re
import requests
import webbrowser
from pathlib import Path
import argparse
import sys
import os


def pdf_text_reader(file_path):
    try:
        with fitz.open(file_path) as pdf:
            # Gets the pages range that the user wants to print
            pages_range = pdf.pages(int(input("The page to start from: ")),int(input("The page to end with: ")))
            text = chr(12).join([page.get_text() for page in pages_range])
            print(text)
    except FileNotFoundError:
        print(f"File not found, please make sure it's the right path: {file_path}")



def pdf_file_extractor(file_path):
    try:
        with fitz.open(file_path) as pdf:
            embedded_files = pdf.embfile_count()
            for emb_file in range(embedded_files):
                file_name = "extracted"
                dir = Path(os.environ.get('USERPROFILE')) / 'Desktop'
                suffix = ".bin"
                save_path = os.path.join(dir, file_name + suffix)
                with Path.open(save_path, "wb") as file:
                    file_data = pdf.embfile_get(0)
                    file.write(file_data)
                    print("The extracted file created on your Desktop")
    except FileNotFoundError:
        print(f"File not found, please make sure it's the right path: {file_path}")



def pdf_metadata(file_path):
    try:
        with fitz.open(file_path) as pdf:
            last_mod = pdf.metadata["modDate"]
            creat_date = pdf.metadata["creationDate"]
            print(f"""
                  The date that the file was created: {creat_date}
                  The last date the file was modified: {last_mod}""")
    except FileNotFoundError:
        print(f"File not found, please make sure it's the right path: {file_path}")


def pdf_url_extractor(file_path):
    try:
        with fitz.open(file_path) as pdf:
            content = chr(12).join([page.get_text() for page in pdf])
            url_matches = re.findall(r"(https?://[a-zA-Z0-9.=-]+(?:/[^\"\']*?)?)", content)

            if url_matches:
                for url in url_matches:
                    print(url)
                    process_url(url)
            else:
                print("No URLs were extracted from the PDF")
    except FileNotFoundError:
        print(f"File not found, please make sure it's the right path: {file_path}")

def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Browsing into {url}")
            webbrowser.open(url)
    except Exception as err:
        print(err)



def path():
    global file_path
    file_path = Path("Put your file full path here: ")
    

def main():
    print(r''' Welcome to:
          
  _____  _____  ______   ______      _                  _             
 |  __ \|  __ \|  ____| |  ____|    | |                | |            
 | |__) | |  | | |__    | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __ 
 |  ___/| |  | |  __|   |  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|כ
 | |    | |__| | |      | |____ >  <| |_| | | (_| | (__| || (_) | |   
 |_|    |_____/|_|      |______/_/\_\\__|_|  \__,_|\___|\__\___/|_|   
                                                                      
                                                                      
''')
    parser = argparse.ArgumentParser(prog="PDF Extractor", description="Extracting Text, URLs, Metadata and embedded files from PDFs")
    parser.add_argument("file_path", type=Path, help="Enter your file path to extract")
    parser.add_argument("-t", "--text", action="store_true", help="Extracts the text from the PDF")
    parser.add_argument("-e", "--embedded", action="store_true", help="Extracts the embedded files from the PDF")
    parser.add_argument("-m", "--metadata", action="store_true", help="Extracts Metadata of the PDF")
    parser.add_argument("-u", "--urls", action="store_true", help="Extracts URLs from the PDF")
    options = parser.parse_args()   
    file_path = options.file_path

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    if options.text:
        pdf_text_reader(file_path)
    if options.embedded:
        pdf_file_extractor(file_path)
    if options.metadata:
        pdf_metadata(file_path)
    if options.urls:
        pdf_url_extractor(file_path)



if __name__ == "__main__":
    main()
    