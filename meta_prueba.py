import pandas as pd
import json
import time
def parse(path):
  g = open(path, 'rb')
  for l in g:
    yield json.loads(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

productos = getDF('meta_Software.json').drop_duplicates(subset=['asin'])
reviews = getDF('Software.json')

# Rating score
j=0
rating_code = {}
for asin in reviews['asin']:
    if asin not in rating_code:
        rating_code[asin] = [reviews['overall'].iloc[j],1]
    else:
        rating_code[asin] = [rating_code[asin][0] + reviews['overall'].iloc[j], rating_code[asin][1] + 1]
    j += 1

for rating in rating_code:
    print(rating, rating_code[rating][0]/rating_code[rating][1])

# Similarity
antes = time.time()
pepe = 0
for code in rating_code.keys():
    j=0
    for producto in productos['asin']:
        if producto == code:
            if len(productos['also_view'].iloc[j]) != 0:
                print(productos['also_view'].iloc[j])
            if len(productos['also_buy'].iloc[j]) != 0:
                print(productos['also_buy'].iloc[j])
        j += 1
        pepe += 1
despues = time.time()
print(pepe)
print(despues - antes)