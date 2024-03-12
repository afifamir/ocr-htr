# ocr-htr

# Form Data Extractor

This repository contains a Streamlit application that extracts form data from uploaded images using Optical Character Recognition (OCR) with Tesseract. The extracted data is displayed in the application, and users can save it to a SQLite database and a JSON file.
![Screenshot 2024-03-12 at 9 08 54 AM](https://github.com/afifamir/ocr-htr/assets/14154490/c59d2adf-2b80-47cb-95ba-3881f471a756)
![Screenshot 2024-03-12 at 9 09 10 AM](https://github.com/afifamir/ocr-htr/assets/14154490/ffc88128-486d-46a0-a360-d5ebc2e3467d)


## Features

- Upload images in JPG or PNG format
- Extract form data using OCR with Tesseract
- Display extracted data in a tabular format
- Save extracted data to a SQLite database
- Save extracted data to a JSON file

## Prerequisites

- Python 3.x
- Required Python packages: streamlit, cv2, pytesseract, sqlite3, numpy, re, os, json, pandas

## Installation

1. Clone the repository:
git clone https://github.com/your-username/ocr-htr.git


Copy code

2. Navigate to the project directory:
cd form-data-extractor


Copy code

3. Install the required packages:
pip install -r requirements.txt


Copy code

4. Install Tesseract OCR engine:

- On Windows, download and install the Tesseract executable from the [UB-Mannheim repository](https://github.com/UB-Mannheim/tesseract/wiki).
- On macOS, you can install Tesseract using Homebrew: `brew install tesseract`.
- On Linux, you can install Tesseract using your package manager (e.g., `apt-get install tesseract-ocr` on Ubuntu).

5. Update the `pytesseract.pytesseract.tesseract_cmd` variable in the code with the path to your Tesseract executable.

## Usage

1. Run the Streamlit application:
streamlit run app.py


Copy code

2. The application will open in your default web browser.

3. Upload an image containing form data by clicking the "Upload Image" button.

4. Click the "Process Image" button to extract the form data using OCR.

5. The extracted data will be displayed in a table.

6. Click the "Save to Database" button to save the extracted data to a SQLite database and a JSON file.

## Contributing
