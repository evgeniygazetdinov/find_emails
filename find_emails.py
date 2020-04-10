import urllib
import requests
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers = {"user-agent" : MOBILE_USER_AGENT}
resp = requests.get(URL, headers=headers)
if resp.status_code == 200:
	print('here')
	soup = BeautifulSoup(resp.content, "html.parser")
	results = []
	if soup.find("div",{"class":"n-rating_table-row-column__name __link"}):
		f = soup.find("div",{"class":"n-rating_table-row-column__name __lin"})
		print(f)
