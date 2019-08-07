import cirq
from cirq.devices import GridQubit
class Xmon10Device(cirq.Device):

#"""Next nearest neighbor is not valid"""

    def __init__(self):
        self.qubits = [GridQubit(i, 0) for i in range(10)]

    def duration_of(self, operation):
        #Wouldn't it be nice if everything to0k 10ns?
        return cirq.Duration(nanos=10)

    def validate_operation(self, operation):
        if not isinstance(operation, cirq.GateOperation):
            raise ValueError('{!r} is not a supported operation mother licker'.format(operation))
        if not isinstance(operation.gate, (cirq.CZPowGate,
                                            cirq.XPowGate,
                                            cirq.PhasedXPowGate,
                                            cirq.YPowGate)):
            raise ValueError('{!r} is not a supported operation mother licker'.format(operation.gate))
        if len(operation.qubits) ==2:
            p, q = operation.qubits
            if not p.is_adjacent(q):
                raise ValueError('Non-local interaction: {}'.format(repr(operation)))

    def validate_scheduled_operation(self, schedule, scheduled_operation):
        self.validate_operation(scheduled_operation.operation)

    def validate_circuit(self, circuit):
        for moment in circuit:
            for operation in moment.operations:
                self.validate_operation(operation)

    def validate_schedule(self, schedule):
        for scheduled_operation in schedule.scheduled_operations:
            self.validate_scheduled_operation(schedule, scheduled_operation)




device = Xmon10Device()
circuit =cirq.Circuit()
circuit.append([cirq.CZ(device.qubits[0], device.qubits[2])])
try:
    device.validate_circuit(circuit)
except ValueError as e:
    print(e)

#//with scheduling

import cirq

circuit = cirq.Circuit()
circuit.append([cirq.CZ(device.qubits[0], device.qubits[1]), cirq.X(device.qubits[0])])
print(circuit)

#convert into a scheduled_operation

schedule = cirq.moment_by_moment_schedule(device, circuit)
print(schedule[cirq.Timestamp(nanos=15)])


#slice and device?

slice = schedule[cirq.Timestamp(nanos=5):cirq.Timestamp(nanos=15)]
slice_schedule = cirq.Schedule(device, slice)
print(slice_schedule ==schedule)
