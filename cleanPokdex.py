# Imports
import csv
import string

# List of Stop Words
# Comes from http://www.textfixer.com/resources/common-english-words.txt
stopWords ="a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(',')

# Open file to save to
cleanPokedex = open('C:/PandP/Pokedex/GenIPokedexClean.csv','wb')
writer = csv.writer(cleanPokedex)

# Read through the Pokedex data
with open('C:/PandP/Pokedex/GenIPokedex2.csv','rb') as pokedex:
    reader = csv.reader(pokedex)
	# For each of the Pokemon
    for row in reader:
		# Get the number
		zero = row[0]
		# Get their name
		one = row[1].upper()
		# Get the Pokedex entry, lower caps
		two = row[2].lower()
		# Remove punctuation
		two = two.translate(None, string.punctuation)
		# Remove any of the stop words listed above
		allWords = two.split(' ')
		notStopWord = []
		for word in allWords:
			if word not in stopWords:
				notStopWord.append(word)
		# Combine them back together		
		two = " ".join(notStopWord)
		# Write it out
		writer.writerow([zero,one,two])

# Done		
cleanPokedex.close()		
print('Done')