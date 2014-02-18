#!/usr/bin/python
import sys, os, operator, smtplib, re




from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText





def send_email(addr, subject, msg_body):	
	email_subject = subject
	from_addr="confer@csail.mit.edu"
	to_addr = [addr, 'confer@csail.mit.edu']
	
	msg = MIMEMultipart()
	msg['From'] = 'Confer Team <confer@csail.mit.edu>'
	msg['To'] = addr
	msg['Subject'] = email_subject
	msg.attach(MIMEText(msg_body))	
	print msg
	username = 'anantb'
	password = 'JcAt250486'
	smtp_conn = smtplib.SMTP_SSL('cs.stanford.edu', 465)
	smtp_conn.login(username, password)	
	
	smtp_conn.sendmail(from_addr, to_addr, msg.as_string())
	
	smtp_conn.close() 





def send_survey_email():
	f = open(sys.argv[1]).read()
	names = re.split('\n', f)
	subject = "Meet at CSCW"
	for name in names:
		tokens = re.split(',', name.strip())
		tokens = map(lambda x: x.strip(), tokens)
		print tokens
		msg_body = """
Dear %s,

Welcome to CSCW!  We're glad you've been using Confer to mark the papers that interest you. While you're here, we'd like to help you also meet some new interesting people.

Based on your paper selections, we've identified some other CSCW attendees who share your interests and listed them in your Meetups tab on Confer. If you don't know them, the next few days are the perfect opportunity to meet them. Like you, they've opted in to this connection service, so don't be shy -- use the Meetup tab's one-click option to send them an email suggesting a meeting.

Have fun building bridges!
-The Confer Team

		""" %(tokens[1])
		send_email(tokens[0], subject, msg_body)
		
	
	






def main():
	send_survey_email()
	

if __name__ == '__main__':
    main()
