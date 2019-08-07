import cirq
import numpy as np

q0 = cirq.GridQubit(0, 0)
q1 = cirq.GridQubit(1, 0)

def basic_circuit(meas=True):
    sqrt_x = cirq.X**0.5
    yield sqrt_x(q0), sqrt_x(q1)
    yield cirq.CZ(q0, q1)
    yield sqrt_x(q0), sqrt_x(q1)
    if meas:
        yield cirq.measure(q0, key='q0'), cirq.measure(q1, key='q1')

circuit =cirq.Circuit()
circuit.append(basic_circuit())

print(circuit)


from cirq import Simulator
simq = Simulator()
result = simq.run(circuit)

print(result)


#Ciruit Stepping

circuit = cirq.Circuit()
circuit.append(basic_circuit())
for i, step in enumerate(simq.simulate_moment_steps(circuit)):
    print('state at step %d: %s' % (i, np.around(step.state_vector(), 3)))


#monte carlo noise
q = cirq.NamedQubit('a')
circuit = cirq.Circuit.from_ops(cirq.bit_flip(p=0.2)(q), cirq.measure(q)) #PauliXGate
simq = cirq.Simulator()
result = simq.run(circuit, repetitions=100)
print(result.histogram(key='a'))


"""Paramatarized values for setting up Studies"""
import sympy
rot_w_gate=cirq.X**sympy.Symbol('x')
circuit = cirq.Circuit()
circuit.append([rot_w_gate(q0), rot_w_gate(q1)])
for y in range(5):
    resolver = cirq.ParamResolver({'x': y / 4.0})
    result = simq.simulate(circuit, resolver)
    print(np.round(result.final_state, 2))

resolvers =[cirq.ParamResolver({'x': y / 2.0}) for y in range(3)]
circuit = cirq.Circuit()
circuit.append([rot_w_gate(q0), rot_w_gate(q1)])
circuit.append([cirq.measure(q0, key='q0'), cirq.measure(q1, key='q1')])
results = simq.run_sweep(program=circuit,
                                params=resolvers,
                                repetitions=2)
for result in results:
    print(result)

#The mixed state simulator """__magic__"""

q = cirq.NamedQubit('a')
circuit = cirq.Circuit.from_ops(cirq.H(q), cirq.amplitude_damp(0.2)(q), cirq.measure(q))
simq = cirq.DensityMatrixSimulator()
result =simq.run(circuit, repetitions=100)
print(result.histogram(key='a'))

q = cirq.NamedQubit('a')
circuit = cirq.Circuit.from_ops(cirq.H(q), cirq.amplitude_damp(0.2)(q))
simq = cirq.DensityMatrixSimulator()
result = simq.simulate(circuit)
print(np.around(result.final_density_matrix, 3))
