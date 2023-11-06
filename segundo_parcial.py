import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define the input variables
rating = ctrl.Antecedent(np.arange(0, 11, 1), 'rating')
popularity = ctrl.Antecedent(np.arange(0, 11, 1), 'popularity')

# Define the output variable
recommendation = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

# Define the membership functions for each variable
rating['low'] = fuzz.trimf(rating.universe, [0, 0, 5])
rating['medium'] = fuzz.trimf(rating.universe, [0, 5, 10])
rating['high'] = fuzz.trimf(rating.universe, [5, 10, 10])

popularity['low'] = fuzz.trimf(popularity.universe, [0, 0, 5])
popularity['medium'] = fuzz.trimf(popularity.universe, [0, 5, 10])
popularity['high'] = fuzz.trimf(popularity.universe, [5, 10, 10])

recommendation['low'] = fuzz.trimf(recommendation.universe, [0, 0, 5])
recommendation['medium'] = fuzz.trimf(recommendation.universe, [0, 5, 10])
recommendation['high'] = fuzz.trimf(recommendation.universe, [5, 10, 10])

# Define the rules
rule1 = ctrl.Rule(rating['low'] & popularity['low'], recommendation['low'])
rule2 = ctrl.Rule(rating['low'] & popularity['medium'], recommendation['low'])
rule3 = ctrl.Rule(rating['low'] & popularity['high'], recommendation['medium'])
rule4 = ctrl.Rule(rating['medium'] & popularity['low'], recommendation['low'])
rule5 = ctrl.Rule(rating['medium'] & popularity['medium'], recommendation['medium'])
rule6 = ctrl.Rule(rating['medium'] & popularity['high'], recommendation['high'])
rule7 = ctrl.Rule(rating['high'] & popularity['low'], recommendation['medium'])
rule8 = ctrl.Rule(rating['high'] & popularity['medium'], recommendation['high'])
rule9 = ctrl.Rule(rating['high'] & popularity['high'], recommendation['high'])

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