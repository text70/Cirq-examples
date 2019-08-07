import cirq

qubits = [cirq.GridQubit(x,y) for x in range(3) for y in range(3)]

print (qubits[0])



#Turning a gate into a 'GateOperation'
#Pauli X gate. obj
x_gate =cirq.X
#apply that motherfucker to, uh, the above qubits
x_op = x_gate(qubits[0])
print(x_op)#now that motherfucker is a "GateOperation"



#Moment: make that operation a threesome with the Pauli Gate and a CZ gate
cz = cirq.CZ(qubits[0], qubits[1])
x =cirq.X(qubits[2])
moment = cirq.Moment([x, cz])

print (moment)

#Circuit and iterable of Moments
cz01 = cirq.CZ(qubits[0], qubits[1])
x2 = cirq.X(qubits[2])
cz12 = cirq.CZ(qubits[1], qubits[2])
moment0 = cirq.Moment([cz01, x2])
moment1 = cirq.Moment([cz12])
circuit = cirq.Circuit((moment0, moment1))

print (circuit)

#Making some motherfucking circuits
from cirq.ops import CZ, H
q0, q1, q2 = [cirq.GridQubit(i, 0) for i in range(3)]
circuit = cirq.Circuit()
circuit.append([CZ(q0, q1), H(q2)])

print(circuit)


#Add a precious moment
circuit.append([H(q0), CZ(q1, q2)])

print(circuit)


#do it live
circuit = cirq.Circuit()
circuit.append([CZ(q0, q1), H(q2), H(q0), CZ(q1, q2)])

print (circuit)

#More insert strategies
#feedback to earlier moments
from cirq.circuits import InsertStrategy
circuit = cirq.Circuit()
circuit.append([CZ(q0, q1)])
circuit.append([H(q0), H(q2)], strategy=InsertStrategy.EARLIEST)

print(circuit)

#new moments, no feedback to other moments, single operation
circuit =cirq.Circuit()
circuit.append([H(q0), H(q1), H(q2)], strategy=InsertStrategy.NEW)

print(circuit)

#this seems like a shell of Hadmard gates around entagled qubits
circuit = cirq.Circuit()
circuit.append([CZ(q1, q2)])
circuit.append([CZ(q1, q2)])
circuit.append([H(q0), H(q1), H(q2)], strategy=InsertStrategy.INLINE)

print (circuit)

#default strategy
circuit = cirq.Circuit()
circuit.append([H(q0)])
circuit.append([CZ(q1, q2), H(q0)], strategy=InsertStrategy.NEW_THEN_INLINE)

print(circuit)



#more than just list values
def my_layer():
    yield CZ(q0, q1)
    yield [H(q) for q in (q0, q1, q2)]
    yield [CZ(q1, q2)]
    yield [H(q0), [CZ(q1, q2)]]

circuit = cirq.Circuit()
circuit.append(my_layer())

for x in my_layer():
    print(x)

print(circuit)

#make a circuit from an OP_tree
circuit = cirq.Circuit.from_ops(H(q0), H(q1))
print(circuit)


#SLice and dice
circuit = cirq.Circuit.from_ops(H(q0), CZ(q0, q1))
for moment in circuit:
    print(moment)

circuit = cirq.Circuit.from_ops(H(q0), CZ(q0, q1), H(q1), CZ(q0, q1))
print(circuit[1:3])  #"""drop the last moment with circuit[:-1], to reverse a circuit [::-1]"""
#cirq.contrib.quirk
