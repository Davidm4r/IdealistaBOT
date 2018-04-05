import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pymongo
import configparser
import telebot


config = configparser.ConfigParser()
config.read('config')

class House(object):

	def __init__(self):
		
		self.address = None
		self.price = None
		self.phone = None
		self.url = None

	def get_price(self,sourcecode):
		'''
		Return the price of a house
		'''
		try:
			price = sourcecode.find('span', {'class_', 'item-price h2-simulated'})
			self.price = ''.join(filter(lambda x: x.isdigit(), price.text))
		except:
			pass

	def get_link(self,sourcecode):
		'''
		Return the href of the house
		'''
		try:
			link = sourcecode.find('a', {'class_', 'item-link'})
			self.url = 'http://idealista.com'+link['href']
		except:
			pass

	def get_address(self,sourcecode):
		'''
		Return the address of a house
		'''
		try:
			address = sourcecode.find('a', {'class_', 'item-link'})
			self.address = address.text
		except:
			pass

	def get_phone(self,sourcecode):
		'''
		Return the phone number of the house
		'''
		try:
			phone = sourcecode.find('span', {'class_', 'icon-phone item-not-clickable-phone'})
			self.phone = phone.text
		except:
			pass

	def send_email(self):
		'''
		TODO
		If we find a new flat. Send an email
		'''
		TOKEN =str(config['TELEGRAM']['Token'])
		bot = telebot.TeleBot(TOKEN)
		bot.send_message(config['TELEGRAM']['ChatID'],self.url)


	def save_into_db(self):
		if db.find_one({'url': self.url}) is None:
			print("INSERTADO")
			s = json.dumps(self.__dict__,ensure_ascii=False)
			db.insert(json.loads(s))
			self.send_email()


def houselist(url):
	'''
	Return a list of houses given and url
	'''

	#Experimental headers. Withouth them, Idealista will ban us.
	headers = {
        'Accept' : 'application/json', 
        'Content-Type' : 'application/json',
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
    }	
	session = requests.Session()
	r = session.get(url, headers=headers)
	print(r)
	soup = BeautifulSoup(r.text, 'html.parser')
	houselist=soup.findAll('article')
	return houselist


if __name__ == "__main__":
	#Connect to DB
	client = pymongo.MongoClient()
	db = client.idealista['alcala']

	#Generate the list of houses
	houselist=houselist(str(config['IDEALISTA']['url']))
	#houselist=houselist('https://www.idealista.com/')
	for house in houselist:
		h = House()
		h.get_link(house)
		h.get_address(house)
		h.get_phone(house)
		h.get_price(house)
		h.save_into_db()
		