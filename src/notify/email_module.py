# Import smtplib for the actual sending function
# import smtplib
#
# class email_notification:
#     def __init__(self, subject, email_address):
#         self.subject = subject
#         self.email_address = email_address
#
#     def notify(self, text):
#
#         # Import the email modules we'll need
#         from email.message import EmailMessage
#
#         # Open the plain text file whose name is in textfile for reading.
#
#         msg = EmailMessage()
#         msg.set_content(text)
#
#         # me == the sender's email address
#         # you == the recipient's email address
#         msg['Subject'] = self.subject
#         msg['From'] = self.email_address
#         msg['To'] = self.email_address
#
#         # Send the message via our own SMTP server.
#         s = smtplib.SMTP('localhost')
#         s.send_message(msg)
#         s.quit()