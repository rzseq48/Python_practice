import os
import requests
import json
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to read PDF document
def read_pdf(file_path):
    """
    Reads a PDF document and extracts questions and options.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        list: A list of dictionaries containing questions and their respective options.
    """
    document = fitz.open(file_path)
    data = []
    question = None
    options = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('Q:') or line[0].isdigit() and line[1] == ')':
                if question:
                    data.append({'question': question, 'options': options})
                question = line[2:].strip() if line.startswith('Q:') else line
                options = []
            elif line.startswith('A:') or line[0].islower() and line[1] == ')':
                options.append(line[2:].strip() if line.startswith('A:') else line)

    if question:
        data.append({'question': question, 'options': options})

    return data

def send_to_google_apps_script(url, title, questions_and_options):
    """
    Sends data to a Google Apps Script.

    Args:
        url (str): URL of the Google Apps Script Web App.
        title (str): Title of the form.
        questions_and_options (list): A list of dictionaries containing questions and their options.

    Returns:
        Response: Response object from the POST request.
    """
    payload = {
        'title': title,
        'questionsAndOptions': questions_and_options
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response

# Read the document and send the data
file_path = r'FILE_PATH '
file_extension = file_path.split('.')[-1].lower()

if file_extension == 'pdf':
    questions_and_options = read_pdf(file_path)
else:
    raise ValueError("Unsupported file type")

title = 'Sample Quiz'
google_apps_script_url = os.getenv('GOOGLE_APPS_SCRIPT_URL')
response = send_to_google_apps_script(google_apps_script_url, title, questions_and_options)
print(response.text)
