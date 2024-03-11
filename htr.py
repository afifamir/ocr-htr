import streamlit as st
import cv2
import pytesseract
import sqlite3
import numpy as np
import re
import os
import json
import pandas as pd
from io import BytesIO

# Path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def extract_data(image):
    data = {}

    # Convert image bytes to NumPy array
    nparr = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use Tesseract OCR to extract text from the image
    text = pytesseract.image_to_string(gray)

    print("Extracted Text:")
    print(text)

    # Define regular expressions for extracting information
    aircraft_model_regex = re.compile(r'Aircraft\s*Model\s*:?\s*(\w+\s+\w+)', re.IGNORECASE)    
    registration_number_regex = re.compile(r'Registration\s*Number\s*:?(\w+-\w+)', re.IGNORECASE)
    departure_airport_regex = re.compile(r'Departure\s*Airport\s*:?(\w+\s+\w+)', re.IGNORECASE)
    arrival_airport_regex = re.compile(r'Arrival\s*Airport\s*:?([^\n]+)', re.IGNORECASE)
    crew_regex = re.compile(r'Crew\s*:?(\d+)', re.IGNORECASE)
    fuel_regex = re.compile(r'Fuel\s*:?(\d+k)', re.IGNORECASE)
    load_regex = re.compile(r'Load\s*:?(\d+)', re.IGNORECASE)

    # Extract information using regular expressions
    matches = aircraft_model_regex.findall(text)
    data['Aircraft Model'] = matches[0].strip() if matches else None

    matches = registration_number_regex.findall(text)
    data['Registration Number'] = matches[0].strip() if matches else None

    matches = departure_airport_regex.findall(text)
    data['Departure Airport'] = matches[0].strip() if matches else None

    matches = arrival_airport_regex.findall(text)
    data['Arrival Airport'] = matches[0].strip() if matches else None

    matches = crew_regex.findall(text)
    data['Crew'] = int(matches[0]) if matches else None

    matches = fuel_regex.findall(text)
    data['Fuel'] = int(matches[0][:-1]) if matches else None

    matches = load_regex.findall(text)
    data['Load'] = int(matches[0]) if matches else None

    print("Extracted Data:")
    print(data)

    return data

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS form_data
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       aircraft_model TEXT,
                       registration_number TEXT,
                       departure_airport TEXT,
                       arrival_airport TEXT,
                       crew INTEGER,
                       fuel INTEGER,
                       load INTEGER)""")
    conn.commit()

def save_to_database(conn, data):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO form_data
                      (aircraft_model, registration_number, departure_airport, arrival_airport, crew, fuel, load)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (data.get('Aircraft Model'), data.get('Registration Number'),
                    data.get('Departure Airport'), data.get('Arrival Airport'),
                    data.get('Crew'), data.get('Fuel'), data.get('Load')))
    conn.commit()

def main():
    st.title("Form Data Extractor")

    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        if st.button('Process Image'):
            # Process the uploaded image
            data = extract_data(uploaded_file)

            # Create a pandas DataFrame from the extracted data
            df = pd.DataFrame([data])

            st.write("### Extracted Data:")
            st.write(df)
            print("Extracted Data (Before Writing to Streamlit):")
            print(data)

            # Prepare a JSON file to save the data
            json_data = df.to_json(orient='records')

            if st.button('Save to Database'):
                # Connect to SQLite database
                conn = sqlite3.connect('form_data.db')

                # Create table if not exists
                create_table(conn)

                # Save data to database
                save_to_database(conn, data)

                # Close database connection
                conn.close()

                # Save the JSON data to a file
                with open('form_data.json', 'w') as f:
                    f.write(json_data)

                st.success("Data saved to the database and JSON file!")

if __name__ == "__main__":
    main()
