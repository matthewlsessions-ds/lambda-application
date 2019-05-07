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



x=0

for cyle in range(1, 72):
	x = x + 1
	url = "https://allegro.pl/kategoria/do-domu-oczyszczacze-powietrza-256842?order=qd&bmatch=baseline-n-cl-dict-ele-1-2-0424&p=" + str(x)
	
	user_agent = UserAgent()
	get = requests.get(url)
	findall = BeautifulSoup(get.content, 'lxml')
	finddiv = findall.find_all("div",{"class":"_407d8ae"})

	ok = []
	for i in finddiv:
		price = str(i.find("span",{'class':'fee8042'}).text).replace("zł",'').replace(',','.').replace(' ','')
		specs = i.find_all('dd')

		if len(specs) == 3:
			
			noise = specs[0].text
			maxim = str(specs[1].text).replace("m³/h", "m3h")
			power = specs[2].text	
		else:
			noise = "NA"
			maxim = "NA"
			power = "NA"			
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
		npo_products[product_no] = [title, price, sold, noise, maxim, power, link]
		npo_products_df = pd.DataFrame.from_dict(npo_products, orient = "index", columns = ["Title", "Price", "Sold", "noise level", "Maximum Performance", "Power", "link"])
		print(npo_products_df)
		npo_products_df.to_csv("airclear.csv")			

