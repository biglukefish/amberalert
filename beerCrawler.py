'''module to crawl the website ratebeer.com and extract stats about beers'''

import requests
import lxml
from bs4 import BeautifulSoup
import re
import random



class Beer():
	'''represents a beer page, and pulls the stats for that beer off the page'''

	def __init__(self, url):
		self.url = url

		r = requests.get(url)
		self.soup = BeautifulSoup(r.text, 'lxml')
		self.canonical = self.soup.find('link').get('href')
		self.stats = {}
		try:
			self.stats['beer'] = self.soup.find(itemprop='name').string
			self.stats['brewer'] = self.soup.find(itemprop='brand').string
			self.stats['style'] = self.soup.find(string=re.compile('Style:')).next_element.string
			self.stats['number of ratings'] = self.soup.find(itemprop='ratingCount').string
			self.stats['weighted avg'] = self.soup.find('span', itemprop='ratingValue').string
			self.stats['overall rating'] = self.soup.find(itemprop='ratingValue').string
			self.stats['abv'] = self.soup.find(title='Alcohol By Volume').next_sibling.next_element.string
			self.stats['calories'] = self.soup.find(title='Estimated calories for a 12 fluid ounce serving').next_sibling.next_element.string
			self.stats['description'] = self.soup.find('span', itemprop='description').string
		except AttributeError:
			print 'attribute exception within Beer class'


	def get_stats(self):
		
		try:
			if self.stats['beer'] != None:
				print('-------------new beer-----------')
				for key in (self.stats):
					print(key + ': ' + self.stats[key])
		except:
			pass




class Spider():

	def __init__(self, beers_desired):
		'''beers_desired is the number of results you want'''

		self.num_beers_desired = beers_desired
		self.beers = []

	def generate_links(self, seed_url):
		'''formats seed url and adds it to the list of valid_pages
		:param seed_url: string
		'''
		if len(self.beers) >= self.num_beers_desired:
			return
		else:
			try:
				r = requests.get(seed_url)
			except requests.exceptions.MissingSchema:
				return 'fail'
			bs = BeautifulSoup(r.text, 'lxml')
			new_links = []

			for tag in bs.find_all('a'):
				link = tag.get('href')
				full_link = 'https://www.ratebeer.com' + str(link)
				if '/beer/' not in full_link:
					continue
				beer = Beer(full_link)
				new_links.append(beer.canonical)
				if beer.canonical not in self.beers:
					self.beers.append(beer.canonical)
					beer.get_stats()
			
			while True:
				status = self.generate_links(random.choice(new_links))
				if status != 'fail':
					break


if __name__ == '__main__':
	beerspider = Spider(500)
	beerspider.generate_links('https://www.ratebeer.com/beer/samuel-adams-barrel-room-collection-new-world-tripel/112477/2/1/')
