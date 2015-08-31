
import numpy
import csv
import nltk
import os
import operator
import re
import string

from collections import Counter
from nltk.corpus import stopwords

#remove punctuation from a string
def removePunc(line):

	replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	line = line.translate(replace_punctuation)
	return line

# noise removal
# cleaning filler words, punctuation from data
# sorting it in such a way so that it is ready to be processed

class cleanData():

	def extractData(self):

		#read the csv file
		csvReader = csv.reader(open('yelp_academic_dataset_review.csv', 'r+'))
		
		oneStar = list()
		twoStar = list()
		threeStar = list()
		fourStar = list()
		fiveStar = list()
		index = 0

		#traversing through each row in the csv file
		for row in csvReader:

			# we are currently using 50 rows of data since it takes a shorter amount of time
			# as index goes up sample size is larger and the algorithm is more accurate
			# keep in mind this is not extremly accurate, the Yelp dataset contains over 500000+ rows
			# of reviews... takes more than 10 hours to train so...

			if index == 50:

				break
			
			index+=1
			
			#review
			review = row[2].upper()
			# number of stars
			stars = row[6]
			# checking if it is actually a review		
			typeOf = row[8].upper()
			
			#if the type isn't a review we don't want to analyze it
			if not (typeOf == "REVIEW"):
				continue

			#one star reviews
			if int(stars) == 1:
				oneStar.append(review)
			
			#two star reviews
			elif int(stars) == 2:
				twoStar.append(review)
			
			#three star reviews
			elif int(stars) == 3:
				threeStar.append(review)
			
			#four star reviews
			elif int(stars) == 4:
				fourStar.append(review)
			
			#five star reviews
			else:
				fiveStar.append(review)

		data = (oneStar, twoStar, threeStar, fourStar, fiveStar)
			
		return data

	# organize data into a list of tuples based off review/stars
	# we can now apply this to scikit's classifiers to create a predictor model

	def organizeData(self, reviewData):

		#currently the dictionary keys arent hasing properly...
		one, two, three, four, five = reviewData

		frequency = list()
		#represents the star nunber for the review
		index = 1;
		numberWords = 0
		numberReviews = 0

		data = []
		stars = []

		# iterate through the corresponding lists with the reviews
		for i in [one, two, three, four, five]:

			numReviews = 0

			#dictionary to store the corresponding number of reviews in it
			store = dict()

			for reviews in i:

				# removes the punctuation
				reviews = removePunc(reviews)

				#split the values up by word (based off spacing)
				reformatReview = re.split(' ', reviews)

				stop = set(stopwords.words('english'))

				stop = [x.upper() for x in stop]

				reformatReview = [i for i in reformatReview if i not in stop]

				for word in reformatReview:

					for s in string.punctuation:

						word = word.replace(s, "")

					if word in store:

						store[word] += 1

					else:

						store[word] = 1

					#tuple of word and star rating
					data.append((word, index))

					numberWords += 1

				numReviews += 1

			print "Total Reviews for " + str(index) + " stars..."
			
			print str(numReviews)
			
			numberReviews += numReviews

			frequency.append((store, index))
			index += 1

		# print the statistics for the words analyzed
		# get most common word for each star rating
		for i in frequency:
			print str(i[1]) + " star review frequency.."
			d = Counter(i[0])
			for k, v in d.most_common(10):
				print '%s: %i' % (k, v)

		print "Total words analyzed: " + str(numberWords)
		print "Total stars:" + str(len(data))

		return 	data

if __name__ == "__main__":

	m = cleanData()
	data = m.extractData()
	wordDict, starDict = m.organizeData(data)

