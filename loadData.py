import os
import re

#Creates two separate lists that are the male/female names
def getNames():
		compNames = extractNames()
		male = list()
		female = list()

		#SORTING NAMES:
		#counts[0] represents the male names
		#counts[1] represnets teh female names
		#we are traversing through all the names in the
		#dictionary
		
		for n in compNames:
			
			counts = compNames[n]
			
			#tuple that holds the name, # of Males, # of Females
			tuple=(n, counts[0], counts[1])
				
			if counts[0] > counts[1]:
				male.append(tuple)
			elif counts[1] > counts[0]:
				female.append(tuple)

		data = (male, female)

		return data

# store name/gender data in a dictionary
# returns the dictionary for analysis
def extractNames():

	filename = "names/yob"
	
	#data is a dictionary structure that
	#holds a name as a key
	#a size 2 int array as the value pair
	#int array has the first value to indicate gender
	#second value indicates the count

	data = dict()

	genderMap = {'M': 0, 'F':1}

	# traversing through the files
	for i in range(1880,2015): 
		
		text_file = open(filename + str(i) + ".txt")
		
		# read line by line
		for line in text_file: 
			#logic to grab the necessary data from txtfile
			line = line.split(',')
			name = line[0]
			gender = genderMap[line[1]]
			count = int(line[2])

			if not data.has_key(name):
				data[name]=[0,0]
			data[name][gender]=data[name][gender]+count
			
		text_file.close()
		
	return data

if __name__ == "__main__":
	getNames()
