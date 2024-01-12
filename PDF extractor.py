import fitz
import re
import requests
import webbrowser


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
                save_path = input("Type the path you want to save the file to: ")
                with open(save_path, "wb") as file:
                    file_data = pdf.embfile_get(0)
                    file.write(file_data)
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
    file_path = input("Put your file full path here: ")
    

def quiz():
    print(r''' Welcome to:
          
  _____  _____  ______   ______      _                  _             
 |  __ \|  __ \|  ____| |  ____|    | |                | |            
 | |__) | |  | | |__    | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __ 
 |  ___/| |  | |  __|   |  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|כ
 | |    | |__| | |      | |____ >  <| |_| | | (_| | (__| || (_) | |   
 |_|    |_____/|_|      |______/_/\_\\__|_|  \__,_|\___|\__\___/|_|   
                                                                      
                                                                      
''')
    decision = input(''' Please choose which extractor do you need:
                     1. Text Extractor.
                     2. Embedded Files Extractor.
                     3. MetaData Extractor (only dates for now).
                     4. URL Extractor and Crawler
                     
                     Extractor number: ''')
    path()
    if decision == '1':
        pdf_text_reader(file_path)
    elif decision == '2':
        pdf_file_extractor(file_path)
    elif decision == '3':
        pdf_metadata(file_path)
    elif decision == '4':
        pdf_url_extractor(file_path)
    else:
        print("Invalid extractor, please choose an available one.")

quiz()