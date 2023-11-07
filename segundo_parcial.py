import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import pandas as pd
import json

def parse(path):
    with open(path, 'r') as file:
        for line in file:
            yield json.loads(line)

def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')

#df = getDF('Software.json')
# Define the input variables
rating = ctrl.Antecedent(np.arange(0, 6, 1), 'rating')
similarity = ctrl.Antecedent(np.arange(0, 11, 1), 'similarity')

# Define the output variable
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

# Define the membership functions for each variable
rating['Poor'] = fuzz.trimf(rating.universe, [0, 0, 2.5])
rating['Average'] = fuzz.trimf(rating.universe, [2.3, 3, 3])
rating['Good'] = fuzz.trimf(rating.universe, [2.8, 4, 4])
rating['Excellent'] = fuzz.trimf(rating.universe, [3.8, 5, 5])
rating.view()
input("puto el que lea")

similarity['Poor'] = fuzz.trimf(similarity.universe, [0, 0, 3])
similarity['Average'] = fuzz.trimf(similarity.universe, [2.5, 5.5, 5.5])
similarity['Good'] = fuzz.trimf(similarity.universe, [5, 8, 8])
similarity['Excellent'] = fuzz.trimf(similarity.universe, [7, 10, 10])
similarity.view()
input("puto el que lea")

recommendation['Not recommend'] = fuzz.trimf(recommendation.universe, [0, 0, 3])
recommendation['Likely to recommend'] = fuzz.trimf(recommendation.universe, [2.5, 5.5, 5.5])
recommendation['Recommended'] = fuzz.trimf(recommendation.universe, [5, 8, 8])
recommendation['Highly Recommended'] = fuzz.trimf(recommendation.universe, [7, 10, 10])
recommendation.view()
input("puto el que lea")

# Define the rules
rule1 = ctrl.Rule(rating['Excellent'] & similarity['Excellent'], recommendation['Highly Recommended'])
rule2 = ctrl.Rule(rating['Excellent'] & similarity['Good'], recommendation['Highly Recommended'])
rule3 = ctrl.Rule(rating['Good'] & similarity['Good'], recommendation['Highly Recommended'])
rule4 = ctrl.Rule(rating['Average'] & similarity['Excellent'], recommendation['Highly Recommended'])
rule5 = ctrl.Rule(rating['Average'] & similarity['Good'], recommendation['Recommended'])
rule6 = ctrl.Rule(rating['Average'] & similarity['Average'], recommendation['Recommended'])
rule7 = ctrl.Rule(rating['Excellent'] & similarity['Good'], recommendation['Recommended'])
rule8 = ctrl.Rule(rating['Average'] & similarity['Average'], recommendation['Likely to recommend'])
rule9 = ctrl.Rule(rating['Average'] & similarity['Average'], recommendation['Recommended'])
rule10 = ctrl.Rule(rating['Average'] & similarity['Average'], recommendation['Not recommend'])
rule11 = ctrl.Rule(rating['Poor'] & similarity['Average'], recommendation['Not recommend'])
rule12 = ctrl.Rule(rating['Excellent'] & similarity['Good'], recommendation['Recommended'])


# Create the control system and define the simulation
recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

# Set input values
recommendation_sim.input['rating'] = 7
recommendation_sim.input['similarity'] = 9

# Compute the recommendation
recommendation_sim.compute()

# Print the recommendation
print("Recommendation:", recommendation_sim.output['recommendation'])