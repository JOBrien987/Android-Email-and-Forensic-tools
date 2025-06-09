import imaplib
import email
from email.header import decode_header
import os

# Configuration
EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_app_password'
IMAP_SERVER = 'imap.gmail.com'
DOWNLOAD_FOLDER = './pdf_attachments'

# Create folder if not exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Search all emails
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

print(f"Scanning {len(email_ids)} emails for PDF attachments...\n")

for eid in reversed(email_ids[-50:]):  # You can change the number of emails scanned
    status, msg_data = mail.fetch(eid, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else 'utf-8')

    date = msg.get("Date")

    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", "")
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename and filename.lower().endswith(".pdf"):
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode()

                    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

                    # Save the PDF
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))

                    print(f"Downloaded: {filename}")
                    print(f"  Subject: {subject}")
                    print(f"  Date: {date}\n")

mail.logout()
