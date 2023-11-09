import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
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
    for item in p1['also_view']:
        sp1.add(item)
    for item in p1['also_buy']:
        sp1.add(item)
    for item in p1['category']:
        sp1.add(item)
    for item in p2['also_view']:
        sp2.add(item)
    for item in p2['also_buy']:
        sp2.add(item)
    for item in p2['category']:
        sp2.add(item)

    if len(sp2) != 0:
        x = len(sp1.intersection(sp2)) / len(sp1.union(sp2))
    else:
        x = 0
    return x*10

# Cargamos las estructuras
productos_data = get_unique_asin_products('meta_Software.json')
reviews_data = get_reviews('Software.json')

# Calculo de ratings
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
# Logica difusa
rating = ctrl.Antecedent(np.arange(0, 6, 1), 'rating')
similarity = ctrl.Antecedent(np.arange(0, 11, 1), 'similarity')

# Define the output variable
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

# Define the membership functions for each variable
rating['Poor'] = fuzz.trimf(rating.universe, [0, 0, 2.5])
rating['Average'] = fuzz.trimf(rating.universe, [2.3, 3, 3])
rating['Good'] = fuzz.trimf(rating.universe, [2.8, 4, 4])
rating['Excellent'] = fuzz.trimf(rating.universe, [3.8, 5, 5])

similarity['Poor'] = fuzz.trimf(similarity.universe, [0, 0, 3])
similarity['Average'] = fuzz.trimf(similarity.universe, [2.5, 5.5, 5.5])
similarity['Good'] = fuzz.trimf(similarity.universe, [5, 8, 8])
similarity['Excellent'] = fuzz.trimf(similarity.universe, [7, 10, 10])

recommendation['Not recommend'] = fuzz.trimf(recommendation.universe, [0, 0, 3])
recommendation['Likely to recommend'] = fuzz.trimf(recommendation.universe, [2.5, 5.5, 5.5])
recommendation['Recommended'] = fuzz.trimf(recommendation.universe, [5, 8, 8])
recommendation['Highly Recommended'] = fuzz.trimf(recommendation.universe, [7, 10, 10])

# Define the rules
rule1 = ctrl.Rule(rating['Excellent'] & similarity['Excellent'], recommendation['Highly Recommended'])
rule2 = ctrl.Rule(rating['Excellent'] & similarity['Good'], recommendation['Highly Recommended'])
rule3 = ctrl.Rule(rating['Excellent'] & similarity['Average'], recommendation['Recommended'])
rule4 = ctrl.Rule(rating['Excellent'] & similarity['Poor'], recommendation['Recommended'])
rule5 = ctrl.Rule(rating['Good'] & similarity['Excellent'], recommendation['Highly Recommended'])
rule6 = ctrl.Rule(rating['Good'] & similarity['Good'], recommendation['Highly Recommended'])
rule7 = ctrl.Rule(rating['Good'] & similarity['Average'], recommendation['Recommended'])
rule8 = ctrl.Rule(rating['Good'] & similarity['Poor'], recommendation['Likely to recommend'])
rule9 = ctrl.Rule(rating['Average'] & similarity['Excellent'], recommendation['Highly Recommended'])
rule10 = ctrl.Rule(rating['Average'] & similarity['Good'], recommendation['Recommended'])
rule11 = ctrl.Rule(rating['Average'] & similarity['Average'], recommendation['Recommended'])
rule12 = ctrl.Rule(rating['Average'] & similarity['Poor'], recommendation['Not recommend'])
rule13 = ctrl.Rule(rating['Poor'] & similarity['Excellent'], recommendation['Likely to recommend'])
rule14 = ctrl.Rule(rating['Poor'] & similarity['Good'], recommendation['Not recommend'])
rule15 = ctrl.Rule(rating['Poor'] & similarity['Average'], recommendation['Not recommend'])
rule16 = ctrl.Rule(rating['Poor'] & similarity['Poor'], recommendation['Not recommend'])

# Create the control system and define the simulation
recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16])
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

x=1000
#x = len(productos_data)
recomendados = set()
puntaje = {}
for producto in productos_data[:x]:
    for producto2 in productos_data[:x]:
        if producto['asin'] != producto2['asin']:
            recommendation_sim.input['rating'] = producto['score']
            recommendation_sim.input['similarity'] = similitud(producto, producto2)
            recommendation_sim.compute()

            k = recommendation_sim.output['recommendation']
            #if k > 7.0 and producto['asin'] not in recomendados:
            recomendados.add(producto['asin'])
            puntaje[producto['asin']] = k

recomendados = list(recomendados)
recomendados = sorted(recomendados, key=lambda x: puntaje[x], reverse=True)

for item in recomendados:
    print(item, " Puntaje:", puntaje[item])
print("Productos recomendados:", len(recomendados))