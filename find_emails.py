import urllib
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from writecsv import write_to_csv


def clean_name(name):
	if name is not None:
		clean= (str(name).split('<u>'))
		clean_name = (clean[1]).split('</u>')
		return clean_name[0]
	return None

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
				else:
					continue

def find_emails_on_links():
	pass


if __name__ == '__main__':
	find_links()