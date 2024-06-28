import requests
import json
import fitz  # PyMuPDF

# Function to read PDF document
def read_pdf(file_path):
    try:
        document = fitz.open(file_path)
        data = []
        question = None
        options = []
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text("text")
            
            print(f"Page {page_num + 1} content:")
            print(text)
            print("=" * 40)
            
            lines = text.splitlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line[0].isdigit() and ')' in line:
                    if question:
                        data.append({'question': question, 'options': options})
                    question = line
                    options = []
                elif line[0] in ['a', 'b', 'c', 'd'] and line[1] == ')':
                    options.append(line)
        
        if question:
            data.append({'question': question, 'options': options})
        
        return data
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

# Function to send data to Google Apps Script
def send_to_google_apps_script(url, title, questions_and_options):
    try:
        payload = {
            'title': title,
            'questionsAndOptions': questions_and_options
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response
    except Exception as e:
        print(f"Error sending data to Google Apps Script: {e}")
        return None

# Read the document and send the data
file_path = r'C:\Users\91890\Desktop\New folder\IndustrialPharmacySession.pdf'
file_extension = file_path.split('.')[-1].lower()

if file_extension == 'pdf':
    questions_and_options = read_pdf(file_path)
else:
    raise ValueError("Unsupported file type")

# Print extracted questions and options
print("Extracted questions and options:")
print(json.dumps(questions_and_options, indent=2))

title = 'Sample Quiz'
google_apps_script_url = 'https://script.google.com/macros/s/AKfycbwRl4y49GkMykaFdTG9BCdFe1MMiQ3KVwcA_bcf8lo3Jq9SmZi5zgm6A2R08B7g7cY0/exec'
response = send_to_google_apps_script(google_apps_script_url, title, questions_and_options)

if response:
    print("Response from Google Apps Script:")
    print(response.text)
else:
    print("No response received from Google Apps Script.")
