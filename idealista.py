import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pymongo

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
		pass

	def save_into_db(self):

		if db.find_one({'url': self.url}) is None:
			s = json.dumps(self.__dict__,ensure_ascii=False)
			db.insert(json.loads(s))
			self.send_email()


def houselist(url):
	'''
	Return a list of houses given and url
	'''

	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	houselist=soup.findAll('article')
	return houselist


if __name__ == "__main__":
	#Connect to DB
	client = pymongo.MongoClient()
	db = client.idealista['alcala']

	#Generate the list of houses
	houselist=houselist('https://www.idealista.com/alquiler-viviendas/alcala-de-henares-madrid/?ordenado-por=fecha-publicacion-desc')
	for house in houselist:
		h = House()
		h.get_link(house)
		h.get_address(house)
		h.get_phone(house)
		h.get_price(house)
		h.save_into_db()
		