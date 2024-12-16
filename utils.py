import logging
import imaplib
import email
from email.header import decode_header
import numpy as np

def connect_to_gmail_imap(user: str, password: str):
    """
    Connect to Gmail IMAP server.

    Args:
        user (str): The email address.
        password (str): The password for the email account.

    Returns:
        imaplib.IMAP4_SSL: A connection object to interact with Gmail IMAP.

    Raises:
        Exception: If the connection or login fails.
    """
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('inbox')  # Connect to the inbox.
        return mail
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        raise

def fetch_emails(mail: str, num_emails: int =None):
    """
    Fetch a specified number of emails from the inbox.

    Args:
        mail (imaplib.IMAP4_SSL): The IMAP connection object.
        num_emails (int, optional): Number of emails to fetch. If None, fetch all emails.

    Returns:
        numpy.ndarray: A numpy array containing the content of each email as a string.

    Raises:
        Exception: If there is an issue with fetching or processing emails.
    """
    try:
        # Search for all emails in the inbox
        status, messages = mail.search(None, 'ALL')
        if status != "OK" or not messages[0]:
            logging.warning("No emails found in the inbox.")
            return np.array([])

        # Get all email IDs
        email_ids = messages[0].split()
        if num_emails:
            email_ids = email_ids[-num_emails:]  # Fetch only the last `num_emails` emails

        email_contents = []
        for email_id in email_ids:
            # Fetch the email by ID
            _, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode the subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            # Get the sender's address
            from_ = msg.get("From")

            # Extract the email content
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            # Combine the subject, sender, and body into a single string
            email_content = f"Subject: {subject}\nFrom: {from_}\nBody: {body}"
            email_contents.append(email_content)

        return np.array(email_contents)

    except Exception as e:
        logging.error(f"Error reading emails: {e}")
        raise

def fetch_email_content(user: str, passwd: str, num_emails=None) -> np.ndarray:
    """
    Fetch email content from Gmail inbox.

    Args:
        user: account of user
        passwd: password of user
        num_emails (int, optional): Number of emails to fetch. If None, fetch all emails.

    Returns:
        numpy.ndarray: A numpy array containing email contents.
    """
    mail = connect_to_gmail_imap(user, passwd)
    return fetch_emails(mail, num_emails)
