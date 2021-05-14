#Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage

class email_notifier:
    def __init__(self, smtp_server, subject, email_address):
        self.subject = subject
        self.email_address = email_address
        self.smtp_server = smtp_server

    def notify(self, text):
        msg = EmailMessage()
        msg.set_content(text)

        msg['Subject'] = self.subject
        msg['From'] = self.email_address
        msg['To'] = self.email_address

        # Send the message via our own SMTP server.
        s = smtplib.SMTP(self.smtp_server)
        s.send_message(msg)
        s.quit()