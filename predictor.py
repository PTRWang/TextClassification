from nltk import NaiveBayesClassifier, classify
import loadData
import random

class predictor():

	def extractData(self):
		maleNames, femaleNames = loadData.getNames()
		dataset = list()

		#adding male names
		for mName in maleNames:
			data = self.nameFactor(mName)
			dataset.append((data, 'M'))
		
		#adding female names
		for fName in femaleNames:
			data = self.nameFactor(fName)
			dataset.append((data, 'F'))

		return dataset

	def nameFactor(self, name):
		name = name.upper()

		#the last two letters are probably the most important
		#factors in determining gender of a name so...

		important = {
			'last': name[-1],
			'lastTwo': name[-2],
			'vowel' : (name[-1] in 'AEIOUY')
		}
		
		return important

if __name__ == "__main__":
	tool = predictor()
	tool.extractData()