import requests
from bs4 import BeautifulSoup
import csv

f = open('C:/PandP/Pokedex/GenIPokedex.csv','wb')
writer = csv.writer(f)

writer.writerow(['Number','Name','Pokedex'])

for n in xrange(1,152):

	num = str(n).zfill(3)

	url = ("http://www.serebii.net/pokedex/" + num + ".shtml")
	page = requests.get(url)
	soup = BeautifulSoup(page.text)


	cells = soup.find_all('td')
	name = cells[14].text.strip()

	print(name)

	red = soup.find_all(color="FF0000")
	redPokedex = red[2].text.strip()
	
	yellow = soup.find_all(color="FFFF00")
	yellowPokedex = yellow[1].text[8:].strip()
	
	pokedex = redPokedex + " " + yellowPokedex
	pokedex = pokedex.replace(u'\xe9','e')
	#print(pokedex)
	
	if num == '029':
		name = 'Nidoran_F'
	if num == '032':
		name = 'Nidoran_M'	
	
	writer.writerow([num,name,pokedex])

f.close()