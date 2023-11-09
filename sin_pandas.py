import json

def parse(path):
    with open(path, 'rb') as file:
        for line in file:
            yield json.loads(line)

def get_unique_asin_products(path):
    products = {}
    for data in parse(path):
        asin = data.get('asin')
        if asin not in products:
            products[asin] = data
    return list(products.values())

def get_reviews(path):
    reviews = []
    for data in parse(path):
        reviews.append(data)
    return reviews

productos_data = get_unique_asin_products('meta_Software.json')
reviews_data = get_reviews('Software.json')

for producto in productos_data[:10]:
    print(producto.get('asin'))

print("\n-----\n")

productos_data = sorted(productos_data, key=lambda x: x.get('asin'))

for producto in productos_data[:5]:
    print(producto)

for review in reviews_data[:5]:
    print(review)
