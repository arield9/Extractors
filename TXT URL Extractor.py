import http.client
import re
import requests
import webbrowser
# import beautifulsoup4

def URLExtractor(file_path):
    try:
        with open(file_path, "r", errors='ignore') as file:
            content = file.read()

            global url_matches
            url_matches = re.findall(r"['\"](https?://[a-zA-Z0-9.=-]+(?:/[^\"\']*?)?)['\"]", content)

            if url_matches:
                for url in url_matches:
                    print(url)
                    process_url(url)
            else:
                print("No URLs were extracted from the file")
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


# Get user input for the file path
file_path = input("Put your file full path here: ")

# Call the function with user input
URLExtractor(file_path)

