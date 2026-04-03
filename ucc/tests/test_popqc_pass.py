from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager

from ucc.transpilers.ucc_popqc import PopQCTransformationPass


def repeated_qft_inverse_block(repeats=6):
    qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[3];
    h q[0];
    cp(1.5707963267948966) q[1], q[0];
    h q[1];
    cp(0.7853981633974483) q[2], q[0];
    cp(1.5707963267948966) q[2], q[1];
    h q[2];
    swap q[0], q[2];
    h q[0];
    cp(-1.5707963267948966) q[1], q[0];
    h q[1];
    cp(-0.7853981633974483) q[2], q[0];
    cp(-1.5707963267948966) q[2], q[1];
    h q[2];
    swap q[0], q[2];
    """
    base_block = QuantumCircuit.from_qasm_str(qasm)
    circuit = QuantumCircuit(3)
    for _ in range(repeats):
        circuit.compose(base_block, inplace=True)
    return circuit


def test_popqc_transformation_pass_cancels_repeated_qft_pairs():
    circuit = repeated_qft_inverse_block()

    simplified_circuit = PassManager([PopQCTransformationPass()]).run(circuit)

    assert len(circuit.data) > 0
    assert len(simplified_circuit.data) == 0
