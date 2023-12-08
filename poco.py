import streamlit as st
import imaplib
import email
from bs4 import BeautifulSoup
import re
import pandas as pd
import base64
import os
import mimetypes
import PyPDF2

# Streamlit app title
st.title("Automate2Excel: Simplified Data Transfer")

# Create input fields for the user and password
user = st.text_input("Enter your email address")
password = st.text_input("Enter your email password", type="password")

# Create input field for the email address to search for
search_email = st.text_input("Enter the email address to search for")

# Create input fields for sender's email and date range for PDF extraction
pdf_sender_email = st.text_input("Enter the sender's email for PDF extraction")
start_date = st.date_input("Enter the start date for PDF extraction")
end_date = st.date_input("Enter the end date for PDF extraction")

# Function to extract information from HTML content
def extract_info_from_html(html_content):
    # ... (unchanged)

# Function to extract text content from PDF
def extract_text_from_pdf(pdf_content):
    text = ""
    pdf_reader = PyPDF2.PdfFileReader(pdf_content)
    num_pages = pdf_reader.numPages

    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()

    return text

if st.button("Fetch and Generate Excel"):
    try:
        # URL for IMAP connection
        imap_url = 'imap.gmail.com'

        # Connection with GMAIL using SSL
        my_mail = imaplib.IMAP4_SSL(imap_url)

        # Log in using user and password
        my_mail.login(user, password)

        # Select the Inbox to fetch messages
        my_mail.select('inbox')

        # Define the key and value for email search
        key = 'FROM'
        value = search_email  # Use the user-inputted email address to search
        _, data = my_mail.search(None, key, value)

        mail_id_list = data[0].split()

        info_list = []

        # Iterate through messages and extract information from HTML content and PDF attachments
        for num in mail_id_list:
            typ, data = my_mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            sender_email = msg["From"]
            received_date = msg["Date"]

            if sender_email.lower() == pdf_sender_email.lower() and start_date <= pd.to_datetime(received_date) <= end_date:
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        html_content = part.get_payload(decode=True).decode('utf-8')
                        info = extract_info_from_html(html_content)

                        # Extract and add the received date
                        info["Received Date"] = received_date

                        info_list.append(info)

                    elif part.get_content_type() == 'application/pdf':
                        pdf_content = part.get_payload(decode=True)
                        pdf_text = extract_text_from_pdf(pdf_content)

                        # You can process the PDF text as needed

    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Create a DataFrame and display it using Streamlit
    if info_list:
        df = pd.DataFrame(info_list)
        st.dataframe(df)
