import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

posicao = ctrl.Antecedent(np.arange(-10, 11, 1), 'posicao')
velocidade = ctrl.Antecedent(np.arange(-10, 11, 1), 'velocidade')
acao = ctrl.Consequent(np.arange(-10, 11, 1), 'acao')

posicao.automf(3, names=['N', 'Z', 'P'])
velocidade.automf(3, names=['N', 'Z', 'P'])
acao['N'] = fuzz.trimf(acao.universe, [-10, -10, 0])
acao['Z'] = fuzz.trimf(acao.universe, [-10, 0, 10])
acao['P'] = fuzz.trimf(acao.universe, [0, 10, 10])

regra1 = ctrl.Rule(posicao['N'] & velocidade['N'], acao['P'])
regra2 = ctrl.Rule(posicao['N'] & velocidade['Z'], acao['P'])
regra3 = ctrl.Rule(posicao['N'] & velocidade['P'], acao['Z'])
regra4 = ctrl.Rule(posicao['Z'] & velocidade['N'], acao['P'])
regra5 = ctrl.Rule(posicao['Z'] & velocidade['Z'], acao['Z'])
regra6 = ctrl.Rule(posicao['Z'] & velocidade['P'], acao['N'])
regra7 = ctrl.Rule(posicao['P'] & velocidade['N'], acao['Z'])
regra8 = ctrl.Rule(posicao['P'] & velocidade['Z'], acao['N'])
regra9 = ctrl.Rule(posicao['P'] & velocidade['P'], acao['N'])

controlador = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9])
simulacao = ctrl.ControlSystemSimulation(controlador)

simulacao.input['posicao'] = 1.2
simulacao.input['velocidade'] = -0.5
simulacao.compute()
print(simulacao.output['acao'])
