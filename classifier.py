import sys
import os
import time
import clean
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.metrics import classification_report

# Linear SVM and Multionomial Naive Bayes models for text classification

class Classifier:
	
	def __init__(self, dataset, training = 0.8):

		
		CUTPOINT = int(len(dataset)*training)
		
		# split the data by this point
		self.trainData, self.trainStars = zip(*dataset[:CUTPOINT])
		self.testData, self.testStars = zip(*dataset[CUTPOINT:])


		# vectorizer that uses document frequency, inverse document frequency method
		# requires words to be in ATLEAST 3 reviews to use, and if its in more than 80% 
		# of all reviews, it doesn't use it
		self.vectorizer = TfidfVectorizer(min_df = 3,
										 max_df = 0.8,
									 	sublinear_tf = True,
									 	use_idf = True)

		# classifier
		self.classifier = None

	def trainSVM(self):

		#fit the training/testing data into the appropriate vector space
		trainVectors = self.vectorizer.fit_transform(self.trainData)
		testVectors = self.vectorizer.transform(self.testData)

		#train the kernelized linear SVM
		self.classifier = svm.SVC(kernel = 'linear')
		self.classifier.fit(trainVectors, self.trainStars)

		# check prediction on test vectors
		prediction = self.classifier.predict(testVectors)
		print classification_report(self.testStars, prediction)

	def trainMNB(self):

		#fit the training/testing data into the appropriate vector space
		trainVectors = self.vectorizer.fit_transform(self.trainData)
		testVectors = self.vectorizer.transform(self.testData)

		# training the multinomial NB model
		# small alpha value because data set is small/ change as we increase number of reviews
		self.classifier = MultinomialNB(alpha = 0.001)
		self.classifier.fit(trainVectors, self.trainStars)
		prediction = self.classifier.predict(testVectors)
		print classification_report(self.testStars, prediction)

if __name__ == "__main__":
	cd = clean.cleanData()
	requiredData = cd.extractData()
	dataset = cd.organizeData(requiredData)
	random.shuffle(dataset)
	c = Classifier(dataset)
	c.trainSVM()
	c.trainMNB()
