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

productos = getDF('meta_Software.json')
productos.drop_duplicates(subset=['asin'])
reviews = getDF('Software.json')

for i in range(len(productos)):
    print(productos['category'][i])
