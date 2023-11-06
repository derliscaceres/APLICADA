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

df = getDF('Software.json')
# Define the input variables
rating = ctrl.Antecedent(np.arange(0, 6, 1), 'rating')
popularity = ctrl.Antecedent(np.arange(0, 11, 1), 'popularity')

# Define the output variable
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

# Define the membership functions for each variable
rating['Poor'] = fuzz.trimf(rating.universe, [0, 0, 2.5])
rating['Average'] = fuzz.trimf(rating.universe, [2.3, 3, 3.8])
rating['Good'] = fuzz.trimf(rating.universe, [2.8, 4, 4])
rating['Excellent'] = fuzz.trimf(rating.universe, [3.8, 5, 5])
rating.view()
input("puto el que lea")

popularity['Poor'] = fuzz.trimf(popularity.universe, [0, 0, 3])
popularity['Average'] = fuzz.trimf(popularity.universe, [2.5, 5.5, 5.5])
popularity['Good'] = fuzz.trimf(popularity.universe, [5, 8, 8])
popularity['Excellent'] = fuzz.trimf(popularity.universe, [7, 10, 10])
popularity.view()
input("puto el que lea")

recommendation['Not recommend'] = fuzz.trimf(recommendation.universe, [0, 0, 3])
recommendation['Likely to recommend'] = fuzz.trimf(recommendation.universe, [2.5, 5.5, 5.5])
recommendation['Recommended'] = fuzz.trimf(recommendation.universe, [5, 8, 8])
recommendation['Highly Recommended'] = fuzz.trimf(recommendation.universe, [7, 10, 10])
recommendation.view()
input("puto el que lea")

# Define the rules
rule1 = ctrl.Rule(rating['Excellent'] & popularity['Excellent'], recommendation['Highly Recommended'])
rule2 = ctrl.Rule(rating['Excellent'] & popularity['Good'], recommendation['Highly Recommended'])
rule3 = ctrl.Rule(rating['Good'] & popularity['Good'], recommendation['Highly Recommended'])
rule4 = ctrl.Rule(rating['Average'] & popularity['Excellent'], recommendation['Highly Recommended'])
rule5 = ctrl.Rule(rating['Average'] & popularity['Good'], recommendation['Recommended'])
rule6 = ctrl.Rule(rating['Average'] & popularity['Average'], recommendation['Recommended'])
rule7 = ctrl.Rule(rating['Excellent'] & popularity['Good'], recommendation['Recommended'])
rule8 = ctrl.Rule(rating['Average'] & popularity['Average'], recommendation['Likely to recommend'])
rule9 = ctrl.Rule(rating['Average'] & popularity['Average'], recommendation['Recommended'])
rule10 = ctrl.Rule(rating['Average'] & popularity['Average'], recommendation['Not recommend'])
rule11 = ctrl.Rule(rating['Poor'] & popularity['Average'], recommendation['Not recommend'])
rule12 = ctrl.Rule(rating['Excellent'] & popularity['Good'], recommendation['Recommended'])


# Create the control system and define the simulation
recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

# Set input values
recommendation_sim.input['rating'] = 7
recommendation_sim.input['popularity'] = 9

# Compute the recommendation
recommendation_sim.compute()

# Print the recommendation
print("Recommendation:", recommendation_sim.output['recommendation'])