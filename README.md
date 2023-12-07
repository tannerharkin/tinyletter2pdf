# tinyletter2pdf

## Introduction

TinyLetter, a popular email newsletter service, has announced its shutdown in Q1 2024. As part of the shutdown process, users have the option to download their data, including sent newsletters, in a CSV file format. However, this CSV file presents several challenges for archiving and future accessibility:

1. **Human-Unfriendly Format**: The CSV file, while machine-readable, is not formatted for easy human reading, making it difficult for users to browse through their newsletter content.
2. **Dependent on External Hosting**: The newsletters often contain images hosted on TinyLetter's servers. With the service shutting down, there is a risk of these images being lost forever, breaking the visual integrity of past newsletters.

## Purpose of the Tool

The tinyletter2pdf aims to address these challenges by converting the exported CSV file into a more accessible and enduring format. Specifically, it:

1. **Converts Newsletters to PDF**: The tool processes each newsletter entry in the CSV and converts it into an individual PDF document. This format is more user-friendly for reading and archiving.
2. **Downloads and Embeds Images**: To preserve the visual content of the newsletters, the tool downloads all images referenced in the newsletters and embeds them directly into the PDFs. This ensures that the newsletters retain their original appearance and remain visually intact, independent of external hosting.

## Archiving Your TinyLetter Content

With the tinyletter2pdf, users can create a lasting archive of their newsletters in a format that is not only easy to read but also self-contained. This tool is especially valuable for those looking to preserve their newsletters as a part of their digital legacy, ensuring that their content remains accessible and intact long after the TinyLetter service is gone.

---

# Installation Instructions

## Prerequisites

Before running the script, you need to have Python installed on your system. This script has been tested and designed with Python 3.8 and above.

## Step 1: Clone the Repository

First, clone the repository to your local machine:

```
git clone https://github.com/tannerharkin/tinyletter2pdf.git
cd tinyletter2pdf
```

## Step 2: Install Python Dependencies

Install the required Python packages using `pip`:

```
pip3 install -r requirements.txt
```

This will install `requests`, `beautifulsoup4`, `pdfkit`, and `PyPDF2`.

## Step 3: Install wkhtmltopdf

The script uses `pdfkit`, which in turn requires `wkhtmltopdf` to function correctly. 

### For Windows:

1. Download `wkhtmltopdf` from [the official site](https://wkhtmltopdf.org/downloads.html).
2. Install `wkhtmltopdf` on your system.
3. Add the path to the `wkhtmltopdf` binary to your system's PATH environment variable:
    - Right-click on 'This PC' or 'My Computer' and select 'Properties'.
    - Click on 'Advanced system settings' and then 'Environment Variables'.
    - Under 'System variables', find and select the 'Path' variable, then click 'Edit'.
    - Click 'New' and add the path to the folder where `wkhtmltopdf` is installed (e.g., `C:\Program Files\wkhtmltopdf\bin`).
    - Click 'OK' to save your changes.

### For Linux and macOS:

In most cases, you can install `wkhtmltopdf` via your package manager.

For Debian/Ubuntu:

```
sudo apt-get install wkhtmltopdf
```

For macOS (using Homebrew):

```
brew install wkhtmltopdf
```

## Step 4: Running the Script

With all dependencies installed, you can now run the script:

```
python3 run.py
```

Follow any on-screen prompts to select the CSV file provided by TinyLetter and generate the archive PDF. The final PDF will be placed in the root directory of the script, named `merged_emails.pdf`.