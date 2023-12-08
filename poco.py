import imaplib
import email
from email.header import decode_header
import os

def download_attachments(username, password, from_email, since_date, save_dir):
    # Connect to the Gmail server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    
    # Log in to your Gmail account
    mail.login(username, password)
    
    # Select the mailbox you want to search (e.g., 'inbox')
    mail.select("inbox")

    # Search for emails from a specific sender since a particular date
    result, data = mail.search(None, f'(FROM "{from_email}" SINCE "{since_date}")')

    # Iterate through the list of email IDs
    for num in data[0].split():
        # Fetch the email by ID
        result, message_data = mail.fetch(num, "(RFC822)")
        raw_email = message_data[0][1]

        # Parse the raw email
        msg = email.message_from_bytes(raw_email)

        # Iterate through the email parts
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # Save the attachment
            filename, encoding = decode_header(part.get_filename())[0]
            if isinstance(filename, bytes):
                filename = filename.decode(encoding or 'utf-8')
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
            
            print(f"Attachment saved: {filepath}")

    # Logout from your Gmail account
    mail.logout()

if __name__ == "__main__":
    # Replace these with your Gmail credentials and search parameters
    gmail_username = "your_username@gmail.com"
    gmail_password = "your_password"
    sender_email = "example@gmail.com"
    since_date = "01-Jan-2023"
    save_directory = "attachments"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    download_attachments(gmail_username, gmail_password, sender_email, since_date, save_directory)
