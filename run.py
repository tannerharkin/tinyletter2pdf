import csv
import os
import requests
from bs4 import BeautifulSoup
import pdfkit
import html
from PyPDF2 import PdfMerger, PdfReader
import concurrent.futures
import tkinter as tk
from tkinter import filedialog

# Ensure the images and pdfs directories exist
os.makedirs('images', exist_ok=True)
os.makedirs('pdfs', exist_ok=True)

def download_image(url):
    """Download an image and save it locally, if it doesn't already exist."""
    file_name = url.split('/')[-1]
    file_path = f'images/{file_name}'
    if not os.path.exists(file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
    return file_path

def process_html(subject, content, created_at):
    """Process the HTML content to download images, replace their paths, add CSS, and structure the content."""
    content = html.unescape(content)
    soup = BeautifulSoup(content, 'html.parser')

    for img in soup.find_all('img'):
        image_url = img['src']
        local_path = download_image(image_url)
        if local_path:
            img['src'] = os.path.abspath(local_path)

    new_html = BeautifulSoup("", 'html.parser')
    head = new_html.new_tag('head')
    link = new_html.new_tag('link', href='style.css', rel='stylesheet', type='text/css')
    head.append(link)
    new_html.append(head)

    body = new_html.new_tag('body')
    new_html.append(body)

    # Add structured content
    div_subject = new_html.new_tag('div', id='email-subject')
    h1_subject = new_html.new_tag('h1')
    h1_subject.string = subject
    div_subject.append(h1_subject)
    body.append(div_subject)

    div_date = new_html.new_tag('div', id='email-date')
    subtitle_date = new_html.new_tag('h2')
    subtitle_date.string = f"Sent on {created_at}"
    div_date.append(subtitle_date)
    body.append(div_date)

    div_content = new_html.new_tag('div', id='email-content')
    div_content.append(soup)
    body.append(div_content)

    return str(new_html)

def create_pdf_threaded(subject, content, created_at, email_id, css_path, output_dir):
    """Function to create a PDF, designed to be used in a thread."""
    file_name = f'{output_dir}/email_{email_id}.pdf'
    processed_content = process_html(subject, content, created_at)
    options = {
        "enable-local-file-access": "",
        "encoding": "UTF-8",
        "page-size": "Letter",
        "margin-top": "0.25in",
        "margin-right": "0.5in",
        "margin-bottom": "0.25in",
        "margin-left": "0.5in",
    }
    pdfkit.from_string(processed_content, file_name, options=options, css=css_path)
    return file_name

def process_emails_multithreaded(csv_file, output_dir, css_path):
    """Process all emails in the CSV file using multi-threading and maintain order, skipping existing PDFs."""
    pdf_file_info = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        emails = list(reader)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i, email in enumerate(emails):
            pdf_file_path = f'{output_dir}/email_{i}.pdf'
            if os.path.exists(pdf_file_path):
                print(f"PDF for message {i + 1} already exists. Skipping...")
                pdf_file_info.append((pdf_file_path, i))
                continue

            future = executor.submit(create_pdf_threaded, *(email + [i, css_path, output_dir]))
            futures.append((future, i))

        for future, email_order in futures:
            try:
                pdf_file = future.result()
                pdf_file_info.append((pdf_file, email_order))
                print(f"Completed PDF: {pdf_file}")
            except Exception as exc:
                print(f"Error processing email: {exc}")

    pdf_file_info.sort(key=lambda x: x[1])
    return [info[0] for info in pdf_file_info]

def merge_pdfs(pdf_files, subjects, output_file):
    """Merge all PDF files into a single PDF, starting with a cover page, and add bookmarks for each email."""
    print("Combining PDFs...")
    merger = PdfMerger()

    with open('coverpage.pdf', 'rb') as cover_page:
        merger.append(PdfReader(cover_page))

    total_pages = len(PdfReader('coverpage.pdf').pages)

    for i, pdf_file_path in enumerate(pdf_files):
        subject = subjects[i]
        with open(pdf_file_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            merger.append(reader)
            merger.add_outline_item(subject, total_pages)
            total_pages += len(reader.pages)
    
    metadata = {
        '/Title': 'My TinyLetter Archive',
        '/Creator': 'tinyletter2pdf v1'
    }

    merger.add_metadata(metadata)

    with open(output_file, 'wb') as outfile:
        merger.write(outfile)

    merger.close()
    print("Done!")

def select_csv_file():
    """Open a dialog to select a CSV file."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select your TinyLetter Export CSV File",
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path

def validate_csv_file(file_path):
    """Check if the CSV file contains the required columns."""
    required_columns = {'Subject', 'Content', 'Created_At'}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            if not required_columns.issubset(set(headers)):
                print(f"The CSV file is missing one or more required columns: {required_columns}")
                return False
            return True
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

csv_file = select_csv_file()
if csv_file and validate_csv_file(csv_file):
    css_path = os.path.abspath('style.css')
    subjects = [row[0] for row in csv.reader(open(csv_file, 'r', encoding='utf-8'))][1:]
    pdf_files = process_emails_multithreaded(csv_file, 'pdfs', css_path)
    merge_pdfs(pdf_files, subjects, 'merged_emails.pdf')
else:
    print("No CSV file selected.")
