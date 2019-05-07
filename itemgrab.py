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


read = pd.read_csv('computercat.csv', header=0, usecols=['Name','Size','Link'])

for a in read.values:
	cat = a[0]
	links = a[2]
	nu = a[1]
	yx = (nu/64)
	if yx > 15:
		y = 16
	else:
		y = round(yx) + 1
	x = 0
	for cyle in range(1, y):
		x = x + 1
		url = "https://allegro.pl" + links + "&bmatch=baseline-n-cl-dict-ele-1-2-0424&p=" + str(x)
		print(url)
		findall = make_soup(url)
		finddiv = findall.find_all("div",{"class":"_407d8ae"})
		ok = []
		for i in finddiv:
			price = str(i.find("span",{'class':'fee8042'}).text).replace("zł",'').replace(',','.').replace(" ","")
			link = i.find('h2',class_='ebc9be2').a['href']
			title = str(i.find('h2',class_='ebc9be2').a.text).strip()
			print(title)
			sold = str(i.find('span',class_='_41ddd69').text).split(' ')[0]
			if sold is None:
				sold = "0"
			elif sold == "nikt":
				sold = "0"
			elif sold == "":
				sold = "0"
			else:
				sold = sold			
			product_no+=1
			npo_products[product_no] = [cat, title, price, sold, link]
			npo_products_df = pd.DataFrame.from_dict(npo_products, orient = "index", columns = ["Category","Title", "Price", "Sold","link"])
			print(npo_products_df)
			npo_products_df.to_csv("computersend2.csv")			
	print(cat)

