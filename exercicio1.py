import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

ângulo = ctrl.Antecedent(np.arange(-50, 51, 1), 'ângulo')
velocidade_angular = ctrl.Antecedent(np.arange(-10, 11, 1), 'velocidade_angular')
força = ctrl.Consequent(np.arange(-100, 101, 1), 'força')

ângulo['N'] = fuzz.trimf(ângulo.universe, [-50, -50, 0])
ângulo['Z'] = fuzz.trimf(ângulo.universe, [-10, 0, 10])
ângulo['P'] = fuzz.trimf(ângulo.universe, [0, 50, 50])

velocidade_angular['N'] = fuzz.trimf(velocidade_angular.universe, [-10, -10, 0])
velocidade_angular['Z'] = fuzz.trimf(velocidade_angular.universe, [-1, 0, 1])
velocidade_angular['P'] = fuzz.trimf(velocidade_angular.universe, [0, 10, 10])

força['forte_esquerda'] = fuzz.trimf(força.universe, [-100, -100, -50])
força['leve_esquerda'] = fuzz.trimf(força.universe, [-50, -25, 0])
força['não_empurre'] = fuzz.trimf(força.universe, [-10, 0, 10])
força['leve_direita'] = fuzz.trimf(força.universe, [0, 25, 50])
força['forte_direita'] = fuzz.trimf(força.universe, [50, 100, 100])

regra1 = ctrl.Rule(ângulo['N'] & velocidade_angular['N'], força['forte_esquerda'])
regra2 = ctrl.Rule(ângulo['N'] & velocidade_angular['Z'], força['leve_esquerda'])
regra3 = ctrl.Rule(ângulo['N'] & velocidade_angular['P'], força['não_empurre'])
regra4 = ctrl.Rule(ângulo['Z'] & velocidade_angular['N'], força['leve_esquerda'])
regra5 = ctrl.Rule(ângulo['Z'] & velocidade_angular['Z'], força['não_empurre'])
regra6 = ctrl.Rule(ângulo['Z'] & velocidade_angular['P'], força['leve_direita'])
regra7 = ctrl.Rule(ângulo['P'] & velocidade_angular['N'], força['não_empurre'])
regra8 = ctrl.Rule(ângulo['P'] & velocidade_angular['Z'], força['leve_direita'])
regra9 = ctrl.Rule(ângulo['P'] & velocidade_angular['P'], força['forte_direita'])

sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9])
simulação = ctrl.ControlSystemSimulation(sistema_controle)

simulação.input['ângulo'] = -30  
simulação.input['velocidade_angular'] = 5  

simulação.compute()

print(f"Força recomendada: {simulação.output['força']}")

ângulo.view()
velocidade_angular.view()
força.view()
