from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.quantum_info import Operator
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.passes import CommutativeInverseCancellation

_MAX_BLOCK_SIZE = 256
_MIN_BLOCK_REPEATS = 4
_MAX_GLOBAL_SCAN_SIZE = 50000
_MAX_IDENTITY_CHECK_QUBITS = 10


def _build_circuit_from_instructions(template_circuit, instructions):
    rebuilt_circuit = template_circuit.copy_empty_like()
    rebuilt_circuit.global_phase = template_circuit.global_phase
    for instruction in instructions:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )
    return rebuilt_circuit


def _normalize_param(param):
    if isinstance(param, (int, float)):
        return round(float(param), 12)
    return str(param)


def _instruction_signature(circuit, instruction):
    return (
        instruction.operation.name,
        tuple(
            _normalize_param(param) for param in instruction.operation.params
        ),
        tuple(circuit.find_bit(qubit).index for qubit in instruction.qubits),
        tuple(circuit.find_bit(clbit).index for clbit in instruction.clbits),
    )


def _inverse_instruction_signature(circuit, instruction):
    try:
        inverse_operation = instruction.operation.inverse()
    except Exception:
        return None

    return (
        inverse_operation.name,
        tuple(_normalize_param(param) for param in inverse_operation.params),
        tuple(circuit.find_bit(qubit).index for qubit in instruction.qubits),
        tuple(circuit.find_bit(clbit).index for clbit in instruction.clbits),
    )


def _run_commutative_inverse_cancellation(circuit):
    try:
        return PassManager([CommutativeInverseCancellation()]).run(circuit)
    except Exception:
        return circuit


def _simplify_single_block(block_circuit):
    if (
        block_circuit.data
        and block_circuit.num_qubits <= _MAX_IDENTITY_CHECK_QUBITS
    ):
        try:
            if Operator(block_circuit).equiv(
                Operator(block_circuit.copy_empty_like())
            ):
                return block_circuit.copy_empty_like()
        except Exception:
            pass

    return _run_commutative_inverse_cancellation(block_circuit)


def _find_repeated_prefix(
    circuit,
    max_block_size=_MAX_BLOCK_SIZE,
    min_repeats=_MIN_BLOCK_REPEATS,
):
    instruction_count = len(circuit.data)
    max_candidate_size = min(max_block_size, instruction_count // min_repeats)
    if max_candidate_size < 1:
        return None

    signatures = [
        _instruction_signature(circuit, instruction)
        for instruction in circuit.data
    ]
    best_match = None
    best_coverage = 0

    for block_size in range(1, max_candidate_size + 1):
        prefix = signatures[:block_size]
        repeat_count = 1
        while (repeat_count + 1) * block_size <= instruction_count:
            start_index = repeat_count * block_size
            end_index = start_index + block_size
            if signatures[start_index:end_index] != prefix:
                break
            repeat_count += 1

        coverage = repeat_count * block_size
        if repeat_count < min_repeats:
            continue

        if coverage > best_coverage or (
            coverage == best_coverage
            and (best_match is None or block_size > best_match[0])
        ):
            best_match = (block_size, repeat_count)
            best_coverage = coverage

    return best_match


def _find_repeated_run(
    circuit,
    max_block_size=_MAX_BLOCK_SIZE,
    min_repeats=_MIN_BLOCK_REPEATS,
):
    instruction_count = len(circuit.data)
    max_candidate_size = min(max_block_size, instruction_count // min_repeats)
    if max_candidate_size < 1:
        return None

    signatures = [
        _instruction_signature(circuit, instruction)
        for instruction in circuit.data
    ]
    best_match = None
    best_coverage = 0

    for block_size in range(1, max_candidate_size + 1):
        start_index = 0
        while start_index + min_repeats * block_size <= instruction_count:
            block = signatures[start_index : start_index + block_size]
            repeat_count = 1
            while (
                start_index + (repeat_count + 1) * block_size
                <= instruction_count
            ):
                candidate_start = start_index + repeat_count * block_size
                candidate_end = candidate_start + block_size
                if signatures[candidate_start:candidate_end] != block:
                    break
                repeat_count += 1

            coverage = repeat_count * block_size
            if repeat_count < min_repeats:
                start_index += coverage if repeat_count > 1 else 1
                continue

            if coverage > best_coverage or (
                coverage == best_coverage
                and (best_match is None or block_size > best_match[1])
            ):
                best_match = (start_index, block_size, repeat_count)
                best_coverage = coverage

            start_index += coverage if repeat_count > 1 else 1

    return best_match


def _find_adjacent_inverse_blocks(
    circuit, max_block_size=_MAX_BLOCK_SIZE
):
    instruction_count = len(circuit.data)
    max_candidate_size = min(max_block_size, instruction_count // 2)
    if max_candidate_size < 1:
        return None

    signatures = [
        _instruction_signature(circuit, instruction)
        for instruction in circuit.data
    ]
    inverse_signatures = [
        _inverse_instruction_signature(circuit, instruction)
        for instruction in circuit.data
    ]
    best_match = None
    best_coverage = 0

    for block_size in range(1, max_candidate_size + 1):
        for start_index in range(0, instruction_count - 2 * block_size + 1):
            block = signatures[start_index : start_index + block_size]
            inverse_block = list(
                reversed(
                    inverse_signatures[
                        start_index + block_size : start_index + 2 * block_size
                    ]
                )
            )
            if any(signature is None for signature in inverse_block):
                continue
            if block != inverse_block:
                continue

            coverage = 2 * block_size
            if coverage > best_coverage:
                best_match = (start_index, block_size)
                best_coverage = coverage

    return best_match


def _simplify_repeated_prefix(circuit):
    repeated_prefix = _find_repeated_prefix(circuit)
    if repeated_prefix is None:
        return circuit

    block_size, repeat_count = repeated_prefix
    run_end = block_size * repeat_count
    block_circuit = _build_circuit_from_instructions(
        circuit, list(circuit.data[:block_size])
    )
    simplified_block = _simplify_single_block(block_circuit)

    if len(simplified_block.data) >= block_size:
        return circuit

    rebuilt_circuit = circuit.copy_empty_like()
    rebuilt_circuit.global_phase = circuit.global_phase
    for _ in range(repeat_count):
        for instruction in simplified_block.data:
            rebuilt_circuit.append(
                instruction.operation,
                instruction.qubits,
                instruction.clbits,
            )

    for instruction in circuit.data[run_end:]:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )

    if len(rebuilt_circuit.data) >= len(circuit.data):
        return circuit

    return rebuilt_circuit


def _simplify_repeated_run(circuit):
    repeated_run = _find_repeated_run(circuit)
    if repeated_run is None:
        return circuit

    start_index, block_size, repeat_count = repeated_run
    run_end = start_index + block_size * repeat_count
    block_circuit = _build_circuit_from_instructions(
        circuit, list(circuit.data[start_index : start_index + block_size])
    )
    simplified_block = _simplify_single_block(block_circuit)

    if len(simplified_block.data) >= block_size:
        return circuit

    rebuilt_circuit = circuit.copy_empty_like()
    rebuilt_circuit.global_phase = circuit.global_phase
    for instruction in circuit.data[:start_index]:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )

    for _ in range(repeat_count):
        for instruction in simplified_block.data:
            rebuilt_circuit.append(
                instruction.operation,
                instruction.qubits,
                instruction.clbits,
            )

    for instruction in circuit.data[run_end:]:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )

    if len(rebuilt_circuit.data) >= len(circuit.data):
        return circuit

    return rebuilt_circuit


def _cancel_adjacent_inverse_blocks(circuit):
    inverse_block = _find_adjacent_inverse_blocks(circuit)
    if inverse_block is None:
        return circuit

    start_index, block_size = inverse_block
    rebuilt_circuit = circuit.copy_empty_like()
    rebuilt_circuit.global_phase = circuit.global_phase

    for instruction in circuit.data[:start_index]:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )

    for instruction in circuit.data[start_index + 2 * block_size :]:
        rebuilt_circuit.append(
            instruction.operation,
            instruction.qubits,
            instruction.clbits,
        )

    return rebuilt_circuit


def popqc_optimize(
    circuit,
    iterations=3,
    max_global_scan_size=_MAX_GLOBAL_SCAN_SIZE,
):
    simplified_circuit = circuit
    for _ in range(iterations):
        previous_instruction_count = len(simplified_circuit.data)
        prefix_simplified_circuit = _simplify_repeated_prefix(
            simplified_circuit
        )
        if len(prefix_simplified_circuit.data) < len(simplified_circuit.data):
            simplified_circuit = prefix_simplified_circuit
        elif len(simplified_circuit.data) <= max_global_scan_size:
            simplified_circuit = _simplify_repeated_run(simplified_circuit)
            simplified_circuit = _cancel_adjacent_inverse_blocks(
                simplified_circuit
            )
        simplified_circuit = _run_commutative_inverse_cancellation(
            simplified_circuit
        )
        if len(simplified_circuit.data) >= previous_instruction_count:
            break
    return simplified_circuit


class PopQCTransformationPass(TransformationPass):
    """Structure-aware cancellation for large patterned circuits.

    PopQC is designed to cheaply simplify circuits that contain repeated exact
    blocks, adjacent inverse blocks, and commuting inverse chains before more
    expensive synthesis runs. It is most effective on structured circuits with
    repeated `U` / `U†` patterns, and is not expected to help all inputs.
    """

    def __init__(self, iterations=3):
        super().__init__()
        self.iterations = iterations

    def run(self, dag):
        circuit = dag_to_circuit(dag)
        simplified_circuit = popqc_optimize(
            circuit, iterations=self.iterations
        )
        return circuit_to_dag(simplified_circuit)
