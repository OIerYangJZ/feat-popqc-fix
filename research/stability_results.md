# Repeated-Run Stability Study

Each selected benchmark/method pair was rerun 5 times on the current branch.

Hardware-aware seed: `12345`

The goal is to check:

- whether output metrics are deterministic across runs
- how much runtime variance remains on the key real-instance and hardware-aware cases

## Real Instances

### phase_estimation_real

| Method | Runs | Gates | Depth | CX | Runtime Mean | Runtime Std | Runtime Min | Runtime Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qiskit_opt3 | 5 | 166,805 | 119,204 | 58,491 | 1.166 s | 0.017 s | 1.144 s | 1.188 s |
| optimized_ucc | 5 | 166,805 | 119,204 | 58,491 | 1.235 s | 0.023 s | 1.195 s | 1.256 s |

### grover_real

| Method | Runs | Gates | Depth | CX | Runtime Mean | Runtime Std | Runtime Min | Runtime Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qiskit_opt3 | 5 | 79,029 | 54,163 | 32,544 | 0.491 s | 0.006 s | 0.482 s | 0.5 s |
| optimized_ucc | 5 | 79,029 | 54,163 | 32,544 | 0.497 s | 0.015 s | 0.472 s | 0.514 s |

### qaoa_real

| Method | Runs | Gates | Depth | CX | Runtime Mean | Runtime Std | Runtime Min | Runtime Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qiskit_opt3 | 5 | 36,512 | 2,416 | 23,808 | 0.257 s | 0.013 s | 0.243 s | 0.279 s |
| optimized_ucc | 5 | 36,512 | 2,416 | 23,808 | 0.25 s | 0.008 s | 0.24 s | 0.263 s |

## Hardware-Aware Cases

### hw_mqt_qpeexact_20

| Method | Runs | Gates | Depth | CX | Runtime Mean | Runtime Std | Runtime Min | Runtime Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qiskit_opt3 | 5 | 1,572 | 407 | 812 | 0.043 s | 0.004 s | 0.038 s | 0.049 s |
| optimized_ucc | 5 | 1,563 | 405 | 804 | 0.429 s | 0.03 s | 0.379 s | 0.472 s |

### hw_mqt_qaoa_20

| Method | Runs | Gates | Depth | CX | Runtime Mean | Runtime Std | Runtime Min | Runtime Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qiskit_opt3 | 5 | 2,091 | 532 | 1,530 | 0.075 s | 0.007 s | 0.067 s | 0.085 s |
| optimized_ucc | 5 | 2,050 | 487 | 1,458 | 0.447 s | 0.02 s | 0.434 s | 0.487 s |
