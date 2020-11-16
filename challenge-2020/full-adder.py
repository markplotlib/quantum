from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute

##### build quantum circuit
q = QuantumRegister(10)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

# Initialize inputs: A=1, B=0, X=1
qc.x(q[0]) # A = q0
qc.x(q[2]) # X = q2

# for the Sum qubit: q4
# q0=A, q1=B, q2=X
# q3 = q2 ⊕ q1 (XOR)
qc.cx(q[1], q[3])
qc.cx(q[2], q[3])
qc.barrier()

# Sum qubit: q4
# q4 = q0 ⊕ q3
qc.cx(q[0], q[4])
qc.cx(q[3], q[4])
qc.barrier()

# for the Carry out qubit: q5
# OR: q6 = B (q1) + X (q2)
qc.cx(q[2], q[6])
qc.cx(q[1], q[6])
qc.ccx(q[2], q[1], q[6])
qc.barrier()
# AND: q7 = q0 * q6
qc.ccx(q[0], q[6], q[7])
qc.barrier()
# NOT: q0 = q0! (= A!)
qc.x(q[0])
# AND: q8 = q2 * q1 (= B * X)
qc.ccx(q[2], q[1], q[8])
qc.barrier()
# AND: q9 = q0 * q8 (= A! * B * X)
qc.ccx(q[0], q[8], q[9])
qc.barrier()
# OR: q5 = q7 + q9
qc.cx(q[7], q[5])
qc.cx(q[9], q[5])
qc.ccx(q[7], q[9], q[5])

# Map quantum measurement to classical bits
# the sum output S to c[0] 
qc.measure(q[4], c[0])
# and carry output C to c[1].
qc.measure(q[5], c[1])

# execute the circuit by qasm_simulator
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
count =result.get_counts()
print(count)
qc.draw(output='mpl')
