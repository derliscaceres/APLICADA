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

def calcular_ratings(usuario, reviews, productos, rating_code):
    
    asin_buscar = set()
    ps_buy = {}
    ps_view = {}

    j = 0 # Indice de reviews
    for id in reviews['reviewerID']:
        if usuario == reviews['reviewerID'].iloc[j]:
            if reviews['asin'].iloc[j] not in asin_buscar:
                asin_buscar.add(reviews['asin'].iloc[j])
    
    for id in asin_buscar:
        k = 0 # Indice de productos
        for id2 in productos['asin']:
            if id == id2:
                buy = set()
                if len(productos['also_buy'].iloc[k]) > 0:
                    for m in range(len(productos['also_buy'].iloc[k])):
                        if productos['also_buy'].iloc[k][m] not in buy:
                            ps_buy[productos['also_buy'].iloc[k][m]] = rating_code[productos['also_buy'].iloc[k][m]][0] / rating_code[productos['also_buy'].iloc[k][m]][1]
                            buy.add(productos['also_buy'].iloc[k][m])

                if len(productos['also_view'].iloc[k]) > 0:
                    for m in range(len(productos['also_view'].iloc[k])):
                        if productos['also_view'].iloc[k][m] not in buy:
                            ps_view[productos['also_view'].iloc[k][m]] = rating_code[productos['also_view'].iloc[k][m]][0] / rating_code[productos['also_view'].iloc[k][m]][1]
            k += 1
        if len(ps_buy) > 0 or len(ps_view) > 0:
            break

    print(ps_buy)
    print(ps_view)        

antes = time.time()

productos = getDF('meta_Software.json')
productos.drop_duplicates(subset=['asin'])
reviews = getDF('Software.json')

# Rating score
rating_code = {}
j=0
for asin in reviews['asin']:
    if asin not in rating_code:
        rating_code[asin] = [reviews['overall'].iloc[j],1]
    else:
        rating_code[asin] = [rating_code[asin][0] + reviews['overall'].iloc[j], rating_code[asin][1] + 1]
    j += 1

k=0
unicos = set()
for asin in productos['asin']:
    if len(productos['also_buy'].iloc[k]) > 0:
        print(productos['also_buy'].iloc[k])
        for m in range(len(productos['also_buy'].iloc[k])):
            if productos['also_buy'].iloc[k][m] not in unicos:
                unicos.add(productos['also_buy'].iloc[k][m])
    k += 1

print(len(unicos))
despues = time.time()
print(despues - antes)