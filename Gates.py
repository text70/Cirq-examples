import cirq

from cirq.ops import CNOT
from cirq.devices import GridQubit
q0, q1 = (GridQubit(0,0), GridQubit(0, 1))
print(CNOT.on(q0, q1))
print(CNOT(q0, q1))


#is it unitary
print(cirq.unitary(cirq.X))

#the square root of an X(NOT) gate, true or false
sqrt_x = cirq.X**0.5
print(cirq.unitary(sqrt_x))


#the xmon gates
