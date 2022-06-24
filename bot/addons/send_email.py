from bot import settings
import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from platform import python_version
	
server = settings.SERVER_MAIL
user = settings.LOGIN_MAIL
password = settings.PASSWORD_MAIL
recipients = settings.SEND_MAIL
sender = settings.LOGIN_MAIL

def email_scripts(result_anketa):
	logging.info('Starting anketa sending')
	email_format_text(result_anketa)

def email_format_text(info):
	subject = f"Кандидат: {info['user_name']}"
	text = f"Кандидат: {info['user_name']}, вакансия: {info['vacan']}"
	html = '<html><head></head><body><p>'+text+'</p></body></html>'
	route = f"userfile/{info['userfile']}"
	basename,filesize = email_format_route_file(route)
	email_format_info_msg(subject,text,html,basename,filesize, route)

def email_format_route_file(route):
	basename = os.path.basename(route)
	filesize = os.path.getsize(route)
	return basename, filesize

def email_format_info_msg(subject,text,html,basename,filesize,route):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = 'BOT tech interview <' + sender + '>'
	msg['To'] = recipients
	msg['Reply-To'] = sender
	msg['Return-Path'] = sender
	msg['X-Mailer'] = 'Python/'+(python_version())
	part_text = MIMEText(text, 'plain')
	part_html = MIMEText(html, 'html')
	part_file = open_encode_file(route,basename,filesize)
	email_add(msg,part_text,part_html,part_file)

def open_encode_file(route, basename, filesize):
	open_file = open(route,"rb")
	part_file = MIMEApplication(open_file.read(),
					Name=basename,_subtype="docx")
	part_file.add_header('Content-Disposition', f'attachment; filename="{basename}"; size={filesize}')
	encoders.encode_base64(part_file)
	return part_file

def email_add(msg,part_text,part_html,part_file):
	msg.attach(part_text)
	msg.attach(part_html)
	msg.attach(part_file)
	send_email(msg)

def send_email(msg):
	try:
		mail = smtplib.SMTP_SSL(server)
		mail.login(user, password)
		mail.sendmail(sender, recipients, msg.as_string())
		mail.quit()
	except (smtplib.SMTPException, RuntimeError) as err:
		logging.error(f'{err} from SEND_EMAIL|fail send anketa.')
	logging.info('Done anketa sending')