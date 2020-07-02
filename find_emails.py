import urllib
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from writecsv import write_to_csv,FILE
import numpy as np
from collections import namedtuple
import re
import xlwt
import pandas as pd
from openpyxl import load_workbook
import os
filename  = "emails.xlsx"


def create_file():
	writer = pd.ExcelWriter(filename, engine='xlsxwriter')
	writer.save()

	df = pd.DataFrame({'link': [],
					'email': []})
	writer = pd.ExcelWriter(filename, engine='xlsxwriter')

	df.to_excel(writer, sheet_name='Sheet1', index=False)
	writer.save()

def to_file(emails,link):
	df = pd.DataFrame({'link': [link],'email': [emails]})
	writer = pd.ExcelWriter(filename, engine='openpyxl')
	writer.book = load_workbook(filename)
	writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
	reader = pd.read_excel(r'{}'.format(filename))
	df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)
	writer.close()



def clean_name(name):
	if name is not None:
		clean= (str(name).split('<u>'))
		clean_name = (clean[1]).split('</u>')
		return clean_name[0]
	return None


def read_links_from_csv(file):
	lines = np.genfromtxt(file, delimiter=",", dtype=None)
	my_dict = dict()
	for i in range(len(lines)):
	   my_dict[lines[i][0]] = lines[i][1]
	return my_dict


def emailExtractor(link):
	getH=requests.get(link)
	h=getH.content
	soup=BeautifulSoup(h,'html.parser')
	mailtos = soup.select('a[href^=mailto]')
	for i in mailtos:
		href=i['href']
		try:
			str1, str2 = href.split(':')
		except ValueError:
			break
		
		return str2





def check_link_on_email(link):
	if not os.path.exists(filename):
		create_file()
	email = emailExtractor(link)

	if email is not None:
		to_file(email,link)




def check_links(links):
	emails_with_names = OrderedDict()
	for studio_address,studio_name in links.items():
		if not re.match(r'http',studio_address):
				continue
		email = check_link_on_email(studio_address)
		emails_with_names[studio_name] = email
	return emails_with_names



def find_links():
	#TODO add condtion by check csv file
	URL = 'https://ratingratingov.ru/web-studios-ratings-ratingratingov-web-2019'
	USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
	# mobile user-agent
	MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
	headers = {"user-agent" : MOBILE_USER_AGENT}
	resp = requests.get(URL, headers=headers)
	if resp.status_code == 200:
		soup = BeautifulSoup(resp.content, "html.parser")
		res = OrderedDict()
		if soup.findAll("a",{"class":"tn-atom"}):
			links = soup.findAll("a",{"class":"tn-atom"})
			for link in links:
				name = link.find('u')
				name_without_tags = clean_name(name)
				if (name_without_tags) is not None:
					url = link['href']
					res['url'] = url
					res['studio_name'] = name_without_tags
					write_to_csv(res)
					print(res)
				else:
					continue

def find_emails_on_links():
	links = read_links_from_csv('out.csv')
	emails = check_links(links)


if __name__ == '__main__':
    #if out not exists execute find_links	
	find_emails_on_links()
	