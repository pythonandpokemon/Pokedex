# Imports
import requests
from bs4 import BeautifulSoup
import csv

# Save data
f = open('C:/PandP/Pokedex/GenIPokedex2.csv','wb')
writer = csv.writer(f)

# Write header
writer.writerow(['Number','Name','Pokedex'])

# Find page with list of links
url = ("http://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon"
	   "_by_National_Pok%C3%A9dex_number")
page = requests.get(url)
soup = BeautifulSoup(page.text)

# Grab the Gen I table
styleString = ("border-radius: 10px; -moz-border-radius: 10px; "
			   "-webkit-border-radius: 10px; -khtml-border-radius: "
			   "10px; -icab-border-radius: 10px; -o-border-radius: "
			   # The magic is really in the background color ----v
			   "10px;; border: 2px solid #FF1111; background: #FF1111;")
table = soup.find(style=styleString)
rows = table.find_all('tr')

# Dictionary for Pokemon data
pkmn = {}

# Loop through the rows of that table
for r in rows:
	# Collect the data in each row
	cells = r.find_all('td')
	if len(cells)>2:
		num = cells[0].text.strip()[1:]
		# Get the name
		if num not in ['029','032']:
			name = cells[2].find('a').get('title')
		# Catches for Nidorans
		elif num == '029':
			name = 'Nidoran_F'
		elif num == '032':
			name = 'Nidoran_M'	
		# Get the link to each Pokemon's page
		link = cells[2].find('a').get('href')	
		# Save the data
		data = {'name':name,'link':link}
		pkmn[num] = data
#print(pkmn)

# Loop through the Pokemon		
for n in xrange(1,152):		

	# Get that Pokemon 
	num = str(n).zfill(3)
	poke = pkmn[num]
	
	# Grab that Pokemon's page
	url = "http://bulbapedia.bulbagarden.net" + str(poke['link'])
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# Find the roundtangles that have the Pokedex data
	styleString = ("vertical-align: middle; border: 1px solid #9DC1B7; padding-left:3px;")
	roundtangles = soup.find_all(style = styleString)
	
	# Red/Blue games Pokedex
	redBlue = roundtangles[0].text.strip()
	# Yellow game Pokedex
	yellow = roundtangles[1].text.strip()

	# Combine the Pokedex
	pokedex = redBlue + " " + yellow
	# e' to e, Poke'mon to Pokemon
	pokedex = pokedex.replace(u'\xe9','e')
	# Large dash to dash, -- to - (in Alakazam's Pokedex)
	pokedex = pokedex.replace(u'\u2014','-')

	# Print out the name to keep track of progress
	print(poke['name'])
	
	# Write the data
	writer.writerow([num,poke['name'],pokedex])

# Done
f.close()	
print('Done')