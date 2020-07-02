import sys
import datetime as dt
import time
import smtplib
from chain import password
from chain import text as body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from find_emails import filename
import pandas as pd
from pandas import *



sender_check = 'merrychristmast@gmail.com'
fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'

def open_emails_file(file):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    dic = df.to_dict()
    em = []
    for key,value in dic['email'].items():
        em.append(value)
    return set(em)



def send_email(target):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(sender_check, password)
	msg = MIMEMultipart()
	msg['To'] = target
	msg['From'] = sender_check
	msg['Subject'] = "👋️ Если вы вдруг ищете веб-дизайнера на аутсорс"
	msg.attach(MIMEText(body, 'html', _charset='utf-8'))
	text = msg.as_string()
	server.sendmail(sender_check, target,text)
	server.quit()

def sender():
    emails = open_emails_file(filename)
    for email in emails:
        send_email(email)
        time.sleep(3)
        print('sended to {}'.format(email))



sender()