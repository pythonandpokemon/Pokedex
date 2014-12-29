import requests
from bs4 import BeautifulSoup
import csv

f = open('C:/PandP/Pokedex/GenIPokedex2.csv','wb')
writer = csv.writer(f)

writer.writerow(['Number','Name','Pokedex'])

url = ("http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon"
	   "_by_National_Pok%C3%A9dex_number")
page = requests.get(url)
soup = BeautifulSoup(page.text)

styleString = ("border-radius: 10px; -moz-border-radius: 10px; "
			   "-webkit-border-radius: 10px; -khtml-border-radius: "
			   "10px; -icab-border-radius: 10px; -o-border-radius: "
			   # The magic is really in the background color ----v
			   "10px;; border: 2px solid #FF1111; background: #FF1111;")

table = soup.find(style=styleString)
rows = table.find_all('tr')

pkmn = {}

for r in rows:
	cells = r.find_all('td')
	if len(cells)>2:
		num = cells[0].text.strip()[1:]
		if num not in ['029','032']:
			name = cells[2].find('a').get('title')
		elif num == '029':
			name = 'Nidoran_F'
		elif num == '032':
			name = 'Nidoran_M'	
		link = cells[2].find('a').get('href')	
		data = {'name':name,'link':link}
		pkmn[num] = data
#print(pkmn)
		
# find the hrefs and follow them, then find the pokedex based on red roundtangle

for n in xrange(1,152):		

	num = str(n).zfill(3)
	poke = pkmn[num]
	
	url = "http://bulbapedia.bulbagarden.net" + str(poke['link'])
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	styleString = ("vertical-align: middle; border: 1px solid #9DC1B7; padding-left:3px;")

	roundtangles = soup.find_all(style = styleString)
	redBlue = roundtangles[0].text.strip()
	yellow = roundtangles[1].text.strip()

	pokedex = redBlue + " " + yellow
	pokedex = pokedex.replace(u'\xe9','e')
	pokedex = pokedex.replace(u'\u2014','-')

	print(poke['name'])
	
	writer.writerow([num,poke['name'],pokedex])

f.close()	