###############################################################
#	This Code comes from http://neuro.imm.dtu.dk/wiki/LabMT	  #
###############################################################

import pandas

url = 'http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0026752.s001'
labmt = pandas.read_csv(url, skiprows=3, sep='\t', index_col=0)
#print(labmt)

# Five is the neural amount (from the article)
# This is different from the code list on the site above
happiness = (labmt.happiness_average - 5).to_dict()
 
def score(text):
    words = text.split()
    return sum([happiness.get(word, 0.0) for word in words]) / len(words)
 
##################################################

# My code

import numpy

# Score for only text that is found in the labMT database
def scoreNoMiss(text):
	words = text.split()
	words = pandas.Series([happiness.get(word, 999) for word in words])
	words = words[words!=999]
	return words.mean()

stdDevs = (labmt.happiness_standard_deviation).to_dict()

# Score that is weighted by standard deviation
def scoreWeighted(text):
	words = text.split()
	avgs = pandas.Series([happiness.get(word, 0.0) for word in words])
	# No clue if 1 is a good std
	stds = pandas.Series([stdDevs.get(word, 1) for word in words])
	# Normal dist prob at mean
	weights = numpy.power(stds*numpy.pi*2,-.5)
	totalWeights = sum(weights)
	weights = weights / totalWeights
	return sum(avgs*weights)

# Score for only text that is found in the labMT database that is weighted by standard deviation
def scoreWeightedNoMiss(text):
	words = text.split()
	avgs = pandas.Series([happiness.get(word, 999) for word in words])
	avgs = avgs[avgs!=999]
	stds = pandas.Series([stdDevs.get(word, 999) for word in words])
	stds = stds[stds!=999]
	weights = numpy.power(stds*numpy.pi*2,-.5)
	totalWeights = sum(weights)
	weights = weights / totalWeights
	return sum(avgs*weights)
	
# Get the number of positive words 
def numPos(text):
	words = text.split()
	pos = 0
	for word in words:
		if happiness.get(word,0.0) > 0:
			pos = pos + 1
	return pos

# Get the number of negative words
def numNeg(text):
	words = text.split()
	neg = 0
	for word in words:
		if happiness.get(word,0.0) < 0:
			neg = neg + 1
	return neg	

# Get the number of words with 0 score (neutral or missing)
def numNeut(text):
	words = text.split()
	words = pandas.Series([happiness.get(word, 0.0) for word in words])
	return sum(words==0.0)

# Get the standard deviation of the words
def stdDev(text):
	words = text.split()
	words = pandas.Series([happiness.get(word, 0.0) for word in words])
	words = words[words!=0.0]
	return words.std()

# Read in the Pokedex data	
pokedex = pandas.read_csv("C:\PandP\Pokedex\GenIPokedexClean.csv")

# Run the Pokedex data through the functions above

def scorePokedex(dexEntry):
	return(score(dexEntry['pokedex']))
pokedex['SCORE'] = pokedex.apply(scorePokedex,axis=1)

def scoreNoMissPokedex(dexEntry):
	return(scoreNoMiss(dexEntry['pokedex']))
pokedex['SCORENOMISS'] = pokedex.apply(scoreNoMissPokedex,axis=1)

def scoreWeightedPokedex(dexEntry):
	return(scoreWeighted(dexEntry['pokedex']))
pokedex['SCOREwithWeights'] = pokedex.apply(scoreWeightedPokedex,axis=1)

def scoreWeightedNoMissPokedex(dexEntry):
	return(scoreWeightedNoMiss(dexEntry['pokedex']))
pokedex['SCOREwithWeightsNoMiss'] = pokedex.apply(scoreWeightedNoMissPokedex,axis=1)

def numPosPokedex(dexEntry):
	return(numPos(dexEntry['pokedex']))
pokedex['Positives'] = pokedex.apply(numPosPokedex,axis=1)	

def scorePokedex(dexEntry):
	return(score(dexEntry['pokedex']))
pokedex['SCORE'] = pokedex.apply(scorePokedex,axis=1)

def numNegPokedex(dexEntry):
	return(numNeg(dexEntry['pokedex']))
pokedex['Negatives'] = pokedex.apply(numNegPokedex,axis=1)	

def numNeutPokedex(dexEntry):
	return(numNeut(dexEntry['pokedex']))
pokedex['Other'] = pokedex.apply(numNeutPokedex,axis=1)	

def stdDevPokedex(dexEntry):
	return(stdDev(dexEntry['pokedex']))
pokedex['Std Dev'] = pokedex.apply(stdDevPokedex,axis=1)	

# Print out and finish
pokedex.to_csv("C:\PandP\Pokedex\GenIPokedexScores.csv")
print('Done')