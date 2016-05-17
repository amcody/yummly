from __future__ import division
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
import numpy as np


def clean(ingreds,wordlist):
 for i in range(len(ingreds)):
  if ('scallion' in ingreds[i]): ingreds[i] = 'green onion'
  if ('tumeric' in ingreds[i]): ingreds[i] = 'turmeric'
  if ('chicken stock' in ingreds[i]): ingreds[i] = 'chicken broth'
  for word in wordlist:
   if (word in ingreds[i]): 
     ingreds[i] = word
 return ingreds

def main():

 json1_file = open('train.json')
 json1_str = json1_file.read()
 json1_data = json.loads(json1_str)

# Do some clean-up of the ingredients, replacing longer names with simplifications
# Then get a list of the ingredients 

 file =  open('cleaningreds_cleaned.txt','r')
 keywords = file.readlines()
 keywords = [w.strip() for w in keywords]

 cuisines = []
 ingreds = []
 for dict in json1_data:

   dict['ingredients'] = clean(dict['ingredients'],keywords)

   cuisines.append(dict['cuisine'])
   ingreds.append(dict['ingredients'])

 ingreds = [item for sublist in ingreds for item in sublist]
 ingreds = [item.lower() for item in ingreds]

 uniqcuisines = set(cuisines)
 uniqcuisines = list(uniqcuisines)

 alluniqingreds = set(ingreds)
 alluniqingreds = list(alluniqingreds)

# Find out how many times each cuisine appears:
 cuisinecount = dict.fromkeys(uniqcuisines,0)
 for cuisine in cuisines:
   cuisinecount[cuisine] = cuisinecount[cuisine] + 1


# For each cuisine, get list of all ingredients:
# i.e., {'italian':['tomatoes','pasta'...]}
# Use default dict:

 ingredsdict = defaultdict(list)

 for id in json1_data:
  ingredsdict[id["cuisine"]].append(clean(id['ingredients'],keywords))

# Now flatten these ingredient lists:
 for key in ingredsdict.keys():
  ingredsdict[key] = [item.lower() for sublist in ingredsdict[key] for item in sublist]


# Get the [fractional] number of times each ingredient appears in each cuisine; then make a word cloud:
# Then stick them together in one big dictionary
 alldict = {}
 alldictfrac = {}

 for key in ingredsdict.keys():
  cuisdict = dict.fromkeys(alluniqingreds,0)
  cuisdictfrac = dict.fromkeys(alluniqingreds,0)

  for el in ingredsdict[key]:
    cuisdict[el] = cuisdict[el] + 1
    cuisdictfrac[el] = cuisdict[el]/cuisinecount[key.lower()]

  alldict[key] = cuisdict
  alldictfrac[key] = cuisdictfrac


# Find most important ingredients

 featureingreds = []
 for key in ingredsdict.keys():

  topingreds = (alldictfrac[key].values())
  topingreds.sort()
  toplevel = topingreds[-50]   

  for ingred in alluniqingreds:
   if (alldictfrac[key][ingred] >= toplevel):
      freq = alldictfrac[key][ingred]
      freqother = 0.
      for cuis in alldictfrac.keys():
        if (cuis != key):
         freqother = freqother + alldictfrac[cuis][ingred]    
      freqother = freqother/(len(alldictfrac.keys())-1)
      if (freq > freqother): featureingreds.append(ingred)

 uniqfeaturewords = set(featurewords)
 uniqfeaturewords = list(uniqfeaturewords)

# Generate feature vectors:
 print json1_data[0]
# for dict in json1_data:

#   dict['ingredients'] = clean(dict['ingredients'],keywords)


# Now do the machine learning:
# clf = BernoulliNB()
# clf.fit(X, Y)

# print(clf.predict(X[2:3]))

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()

