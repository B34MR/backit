#!/usr/bin/env python3

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from utils.colors import Colors as c
import smtplib
import os


class Mailer():
	''' SMTP Mail Relay Class. '''


	def __init__(self, smtp_host, smtp_port, debuglevel):
		self.smtp_host = smtp_host
		self.smtp_port = smtp_port
		self.server = smtplib.SMTP(f'{self.smtp_host}:{self.smtp_port}')
		self.debuglevel = debuglevel
		# Set debug level.
		self.server.set_debuglevel(self.debuglevel)


	def login(self, username, password):
		'''Authenticate to SMTP Server'''

		try:
			self.server.ehlo()
			self.server.starttls()
			self.server.login(username, password)
		except Exception as e:
			print(f'[{c.RED}-{c.END}] E-mail Authentication: Failed')
			print(f'[{c.RED}-{c.END}] Error: \n{e}')


	def send_msg_attachment(self, sender, recipient, subject, filepath, body=None):
		'''Populate SMTP headers and send msg /w attachment'''
		
		# Create message object.
		message = MIMEMultipart()

		# SMTP Headers.
		message['From'] = Header(sender)
		message['To'] = Header(recipient)
		message['Subject'] = Header(subject)
	 
		# Attach message body as MIMEText.
		message.attach(MIMEText(body, 'plain', 'utf-8'))
		
		# Attachment name.
		attachment_name = os.path.basename(filepath)

		# Attach file to message.
		try:
			with open(filepath, 'rb') as f1:
				msg_attachment = MIMEApplication(f1.read(), _subtype="txt")
				msg_attachment.add_header('Content-Disposition', 'attachment', filename=attachment_name)
				message.attach(msg_attachment)
		except Exception as e:
			print(f'{e}')

		# Send Message.
		try:
			self.server.sendmail(sender, recipient, message.as_string())
			print(f'[{c.GREEN}*{c.END}] E-mail Status: SUCCESS')
		except Exception as e:
			print(f'[{c.RED}-{c.END}] E-mail Status: FAILED')
			print(f'[{c.RED}-{c.END}] Error: \n{e}')
		self.server.quit()
