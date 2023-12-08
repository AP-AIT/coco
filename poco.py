import streamlit as st
import imaplib
import email
import base64
import io
import fitz  # PyMuPDF

# Streamlit app title
st.title("PDF Attachment Extractor")

# Create input fields for the user, password, and search criteria
user = st.text_input("Enter your email address")
password = st.text_input("Enter your email password", type="password")
search_criteria = st.text_input("Enter search criteria")

# Function to extract PDF attachments from emails
def extract_pdf_attachments(user, password, search_criteria):
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
        key = 'SUBJECT'
        value = search_criteria
        _, data = my_mail.search(None, key, value)

        mail_id_list = data[0].split()

        pdf_list = []

        # Iterate through messages and extract PDF attachments
        for num in mail_id_list:
            typ, msg_data = my_mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            for part in msg.walk():
                if part.get_content_type() == 'application/pdf':
                    pdf_content = part.get_payload(decode=True)
                    pdf_list.append(pdf_content)

        return pdf_list

    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Allow the user to trigger the PDF extraction
if st.button("Extract PDFs"):
    pdfs = extract_pdf_attachments(user, password, search_criteria)

    if pdfs:
        st.success(f"Found {len(pdfs)} PDF attachments.")
        
        # Extract text from PDFs (modify as needed)
        for idx, pdf_content in enumerate(pdfs, start=1):
            pdf_stream = io.BytesIO(pdf_content)
            pdf_doc = fitz.open(pdf_stream)
            pdf_text = ""
            for page in pdf_doc.pages():
                pdf_text += page.get_text()

            st.write(f"Text from PDF {idx}:")
            st.write(pdf_text)

    else:
        st.warning("No PDF attachments found.")
