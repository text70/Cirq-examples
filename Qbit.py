import cirq

#define the length of the grid, ie the 'GridQubit'
length = 3
qubits = [cirq.GridQubit(i,j) for i in range (length) for j in range (length)]
print(qubits)
#prints

#making a 'Moment', a circuit on the 'GridQubit'
circuit = cirq.Circuit()
circuit.append(cirq.H(q) for q in qubits if (q.row + q.col) % 2 == 0)
#H(Hadmard 'Gate' object) can be changed to foment this row+column even 'Operation'
circuit.append(cirq.X(q) for q in qubits if (q.row + q.col) % 2 == 1)
#X "Gate' object can be changed to foment this row+column odd 'Operation'
print(circuit)


#changing a 'Moment' to two 'Moments'
circuit = cirq.Circuit()
circuit.append([cirq.H(q) for q in qubits if (q.row + q.col) % 2 == 0],
#H(Hadmard 'Gate' object) can be changed to foment this row+column even 'Operation'
                strategy=cirq.InsertStrategy.EARLIEST)  #places H gate at earliest moment
circuit.append([cirq.X(q) for q in qubits if (q.row + q.col) % 2 == 1],
#X "Gate' object can be changed to foment this row+column odd 'Operation'
                strategy=cirq.InsertStrategy.NEW_THEN_INLINE) #places X gate at new individual moment
print(circuit)

#itterating over a 'Circuit's 'Moments'
for i, m in enumerate(circuit):
        print ('Moment {}: {}'.format(i, m))






#creating Anstaz (subcircuit) from the Circuit
def rot_x_layer(length, half_turns):
        #"""Yields X rotations by half_turns on a square grid of a given length."""
        rot = cirq.XPowGate(exponent=half_turns)
        for i in range(length):
            for j in range(length):
                yield rot(cirq.GridQubit(i,j))
circuit = cirq.Circuit()
circuit.append(rot_x_layer(2, 0.1))
print (circuit)

import random
def rand2d(rows, cols):
        return [[random.choice([+1, -1]) for _ in range(cols)] for _ in range(rows)]

def random_instance(length):
    #transverse field terms
    h = rand2d(length, length)
    #links within rows
    jr = rand2d(length - 1, length)
    #links within column
    jc = rand2d(length, length -1)
    return (h, jr, jc)

h, jr, jc = random_instance(3) #defines the number of transverse fields and matrix size
print('transverse fields: {}'.format(h))
print('row j fields: {}'.format(jr))
print('column j fields: {}'.format(jc))
#prints random instances



#introducing the Anstaz
def rot_z_layer(h, half_turns):
    #Yields Z rotations by half_turns conditioned on the field hself.
    gate = cirq.ZPowGate(exponent=half_turns)
    for i, h_row in enumerate(h):
        for j, h_ij in enumerate(h_row):
            if h_ij == 1:
                yield gate(cirq.GridQubit(i,j))


#Apply CZPowGate for J +1 if field -1 :: X Gates
def rot_11_layer(jr, jc, half_turns):
    #Yields rotation about |11> conditioned on the jr and jc fields
    gate = cirq.CZPowGate(exponent=half_turns)
    for i, jr_row in enumerate(jr):
        for j, jr_ij in enumerate(jr_row):
            if jr_ij == -1:
                yield cirq.X(cirq.GridQubit(i, j))
                yield cirq.X(cirq.GridQubit(i + 1, j))
            yield gate(cirq.GridQubit(i, j),
                    cirq.GridQubit(i + 1, j))
            if jr_ij == -1:
                yield cirq.X(cirq.GridQubit(i, j))
                yield cirq.X(cirq.GridQubit(i + 1, j))

    for i, jc_row in enumerate(jc):
        for j, jc_ij in enumerate(jc_row):
            if jc_ij == -1:
                yield cirq.X(cirq.GridQubit(i, j))
                yield cirq.X(cirq.GridQubit(i, j + 1))
            yield gate(cirq.GridQubit(i, j),
                cirq.GridQubit(i, j +1))
            if jc_ij == -1:
                yield cirq.X(cirq.GridQubit(i, j))
                yield cirq.X(cirq.GridQubit(i, j +1))

# yield and step it up
def one_step(h, jr, jc, x_half_turns, h_half_turns, j_half_turns):
    length =len(h)
    yield rot_x_layer(length, x_half_turns)
    yield rot_z_layer(h, h_half_turns)
    yield rot_11_layer(jr, jc, j_half_turns)

h, jr, jc = random_instance(3)#defines number of random circuits and moments

circuit = cirq.Circuit()
circuit.append(one_step(h, jr, jc, 0.1, 0.2, 0.3), #parameters
                strategy=cirq.InsertStrategy.EARLIEST)

print(circuit)

simulator =cirq.Simulator()
circuit = cirq.Circuit()
circuit.append(one_step(h, jr, jc, 0.1, 0., 0.3))
circuit.append(cirq.measure(*qubits, key='x'))
results = simulator.run(circuit, repetitions=100)
print(results.histogram(key='x'))


import numpy as np

def energy_func(length, h, jr, jc):
    def energy(measurements):
        #reshape measurement into array that matches grid reshape
        meas_list_of_lists = [measurements[i * length:(i+1) * length]
                                for i in range(length)]
        #convert true/false to +1/-1
        pm_meas = 1 - 2 * np.array(meas_list_of_lists).astype(np.int32)

        tot_energy = np.sum(pm_meas * h)
        for i, jr_row in enumerate(jr):
            for j, jr_ij in enumerate(jr_row):
                tot_energy += jr_ij * pm_meas[i, j] * pm_meas[i + 1, j]
        for i, jc_row in enumerate(jc):
            for j, jc_ij in enumerate(jc_row):
                tot_energy += jc_ij * pm_meas[i, j] * pm_meas[i, j + 1]
        return tot_energy
    return energy
print(results.histogram(key='x', fold_func=energy_func(3, h, jr, jc)))
#prints counter, duh

#expectation value over all repetitions
def obj_func(result):
    energy_hist = result.histogram(key='x', fold_func=energy_func(3, h, jr, jc))
    return np.sum([k * v for k,v in energy_hist.items()]) / result.repetitions
print('Value of the objective function {}'.format(obj_func(results)))
#prints value of function :p


#optimizing looping and parameterizing the Anstaz
import sympy
circuit =cirq.Circuit()
alpha = sympy.Symbol('alpha')
beta = sympy.Symbol('beta')
gamma = sympy.Symbol('gamma')
circuit.append(one_step(h, jr, jc, alpha, beta, gamma))
circuit.append(cirq.measure(*qubits, key='x'))
print(circuit)
#this parameterizes the circuit's Gates

resolver = cirq.ParamResolver({'alpha': 0.1, 'beta': 0.3, 'gamma': 0.7})
resolved_circuit = cirq.resolve_parameters(circuit, resolver)
print(circuit)


#creates a sweep of paramter resolvers
sweep = (cirq.Linspace(key='alpha', start=0.1, stop=0.9, length=5)
        * cirq.Linspace(key='beta', start=0.1, stop=0.9, length=5)
        * cirq.Linspace(key='gamma', start=0.1, stop=0.9, length=5))
results = simulator.run_sweep(circuit, params=sweep, repetitions=100)
for result in results:
    print(result.params.param_dict, obj_func(result))



#finding the minimum
sweep_size = 10
sweep =(cirq.Linspace(key='alpha', start=0.0, stop=1.0, length=10)
        * cirq.Linspace(key='beta', start=0.0, stop=1.0, length=10)
        * cirq.Linspace(key='gamma', start=0, stop=1.0, length=10))
results = simulator.run_sweep(circuit, params=sweep, repetitions=100)

min= None
min_params = None
for result in results:
    value = obj_func(result)
    if min is None or value < min:
        min = value
        min_params = result.params
print('Minumum objective value is {}.'.format(min))
