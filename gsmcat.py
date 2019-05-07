from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from translate import Translator



npo_products = {}

product_no = 0


def make_soup(url):
	user_agent = UserAgent()
	get = requests.get(url,headers={'user-agent':user_agent.chrome})
	soup = BeautifulSoup(get.content, 'lxml')
	return(soup)


url = "https://allegro.pl/kategoria/komputery?order=qd&bmatch=baseline-n-cl-dict-ele-1-2-0329"
findall = make_soup(url)
finddiv = findall.find("div",{"data-box-name":"categories container"})
findalldiv = finddiv.find_all("li")

for yes in findalldiv:
	link = yes.span.a['href']
	plname = str(yes.span.a.text)
	number = str(yes.find('span',{'class':'bd73fb0'}).text)
	traslator = Translator(from_lang="pl",to_lang="en")
	name = traslator.translate(plname)
	print(name)

	product_no+=1
	npo_products[product_no] = [name, number, link]
	npo_products_df = pd.DataFrame.from_dict(npo_products, orient = "index", columns = ["Name", "Size", "Link"])
	print(npo_products_df)
	npo_products_df.to_csv("computercat.csv")