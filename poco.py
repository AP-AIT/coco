import imaplib
import email
from PyPDF2 import PdfFileReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Connect to your email account
mail = imaplib.IMAP4_SSL('your_mail_server.com')
mail.login('your_email@gmail.com', 'your_password')
mail.select('inbox')

# Search for emails with PDF attachments
status, messages = mail.search(None, '(FROM "sender@example.com" SUBJECT "Your Subject" UNSEEN)')

for mail_id in messages[0].split():
    # Fetch the email
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    raw_email = msg_data[0][1]

    # Parse the email
    msg = email.message_from_bytes(raw_email)
    
    # Iterate over the attachments
    for part in msg.walk():
        if part.get_content_type() == 'application/pdf':
            # Extract text from PDF
            pdf_reader = PdfFileReader(part.get_payload(decode=True))
            pdf_text = ""
            for page_num in range(pdf_reader.numPages):
                pdf_text += pdf_reader.getPage(page_num).extractText()

            # Summarize the text
            parser = PlaintextParser.from_string(pdf_text, Tokenizer('english'))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 3)  # You can adjust the number of sentences in the summary

            # Print or save the summary
            print("Summary:", ' '.join(str(sentence) for sentence in summary))

# Logout
mail.logout()
