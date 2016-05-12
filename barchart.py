from __future__ import division
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

json1_file = open('train.json')
json1_str = json1_file.read()
json1_data = json.loads(json1_str)

cuisines = []
for dict in json1_data:
  cuisines.append(dict['cuisine'])
uniqcuisines = set(cuisines)
uniqcuisines = list(uniqcuisines)

lengthdict = defaultdict(list)

for id in json1_data:
 lengthdict[id["cuisine"]].append(len(id['ingredients']))


# Make new dictionary with just the average number of ingredients
avlengthdict = dict.fromkeys(uniqcuisines,0)

for el in uniqcuisines: 
  avlengthdict[el] = np.mean(np.array(lengthdict[el]))

shortkeys = [el[0:3] for el in avlengthdict.keys()]

plt.clf()
plt.bar(range(len(avlengthdict)), avlengthdict.values(), align='center')
plt.xlim(-1,20)
plt.xticks(range(len(avlengthdict)), shortkeys)
plt.ylabel('Average number of ingredients')
plt.savefig('Num_ingreds.png')
