import json
import numpy as np
import time

def parse(path):
    with open(path, 'rb') as file:
        for line in file:
            yield json.loads(line)

def get_unique_asin_products(path):
    products = {}
    for data in parse(path):
        asin = data['asin']
        if asin not in products:
            products[asin] = data
    return list(products.values())

def get_reviews(path):
    reviews = []
    for data in parse(path):
        reviews.append(data)
    return reviews

def similitud(p1, p2):
    sp1, sp2 = set(), set()
    for items in p1['also_view']:
        sp1.add(items)
    for items in p1['also_buy']:
        sp1.add(items)
    for items in p2['also_view']:
        sp2.add(items)
    for items in p2['also_buy']:
        sp2.add(items)
    if len(sp2) != 0:
        x = len(sp1.intersection(sp2)) / len(sp1.union(sp2))
    else:
        x = 0
    return x*10

start = time.time()

productos_data = get_unique_asin_products('meta_Software.json')
reviews_data = get_reviews('Software.json')

orevall_scores = {}
for review in reviews_data:
    asin = review['asin']
    if asin in orevall_scores:
        orevall_scores[asin][0] += review['overall']
        orevall_scores[asin][1] += 1
    else:
        orevall_scores[asin] = [review['overall'], 1]

for producto in productos_data:
    asin = producto['asin']
    if asin in orevall_scores:
        producto['score'] = orevall_scores[asin][0] / orevall_scores[asin][1]
    else:
        producto['score'] = 0.0

for producto in productos_data:
    for producto2 in productos_data:
        if producto['asin'] != producto2['asin']:
            if similitud(producto, producto2) > 5:
                print("----------------------------------------")
                print(producto['asin'], " vs ", producto2['asin'])
                print(similitud(producto, producto2))

end = time.time()

print(end - start)