import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
import base64

# Streamlit app title
st.title("PDF Data Extractor")

# Create input fields for the user and password
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Function to extract information from PDF content
def extract_info_from_pdf(pdf_content):
    doc = fitz.open(pdf_content)
    
    info = {
        "Name": None,
        "Email": None,
        "Workshop Detail": None,
        "Date": None,
        "Mobile No.": None
    }

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Use regular expressions to extract information (modify as needed)
        name_match = re.search(r'Name: (.+)', text, re.IGNORECASE)
        if name_match:
            info["Name"] = name_match.group(1).strip()

        email_match = re.search(r'Email: (.+)', text, re.IGNORECASE)
        if email_match:
            info["Email"] = email_match.group(1).strip()

        workshop_match = re.search(r'Workshop Detail: (.+)', text, re.IGNORECASE)
        if workshop_match:
            info["Workshop Detail"] = workshop_match.group(1).strip()

        date_match = re.search(r'Date: (.+)', text, re.IGNORECASE)
        if date_match:
            info["Date"] = date_match.group(1).strip()

        mobile_match = re.search(r'Mobile No.: (.+)', text, re.IGNORECASE)
        if mobile_match:
            info["Mobile No."] = mobile_match.group(1).strip()

    return info

if pdf_file is not None and st.button("Extract and Generate Excel"):
    try:
        pdf_content = pdf_file.read()
        info = extract_info_from_pdf(pdf_content)

        # Create a DataFrame from the extracted info
        df = pd.DataFrame([info])

        # Display the extracted data
        st.write("Data extracted from the PDF:")
        st.write(df)

        if st.button("Download Excel File"):
            excel_file = df.to_excel('extracted_data.xlsx', index=False, engine='openpyxl')
            if excel_file:
                with open('extracted_data.xlsx', 'rb') as file:
                    st.download_button(
                        label="Click to download Excel file",
                        data=file,
                        key='download-excel'
                    )

        st.success("Excel file has been generated and is ready for download.")

    except Exception as e:
        st.error(f"Error: {e}")
