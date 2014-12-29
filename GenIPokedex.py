# Imports
import requests
from bs4 import BeautifulSoup
import csv

# Save the data here
f = open('C:/PandP/Pokedex/GenIPokedex.csv','wb')
writer = csv.writer(f)
writer.writerow(['Number','Name','Pokedex'])

# Loop throught the different Pokemon
for n in xrange(1,152):

	# 1 -> '001'
	num = str(n).zfill(3)

	# Find the page
	url = ("http://www.serebii.net/pokedex/" + num + ".shtml")
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# Search through the page
	cells = soup.find_all('td')
	name = cells[14].text.strip()

	# Pokedex for Red/Blue games
	red = soup.find_all(color="FF0000")
	redPokedex = red[2].text.strip()
	
	# Pokedex for Yellow
	yellow = soup.find_all(color="FFFF00")
	yellowPokedex = yellow[1].text[8:].strip()
	
	# Combine them
	pokedex = redPokedex + " " + yellowPokedex
	# Replace e' in Poke'mon with e to get Pokemon
	pokedex = pokedex.replace(u'\xe9','e')
	#print(pokedex)
	
	# Catches for the Nidorans
	if num == '029':
		name = 'Nidoran_F'
	if num == '032':
		name = 'Nidoran_M'	
		
	# Print out name to keep track of progress
	print(name)	
	
	# Write out the data
	writer.writerow([num,name,pokedex])

# Close it down
f.close()

# Fin
print('Done')