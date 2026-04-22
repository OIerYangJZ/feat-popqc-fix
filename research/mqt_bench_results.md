# Public Benchmark Suite Baselines (MQT Bench)

Target basis: `['cx', 'rx', 'ry', 'rz', 'h']`

## mqt_qpeexact_32

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 2,620 | 367 | 1,037 | 0.005 s |
| qiskit_opt1 | ok | 2,619 | 367 | 1,037 | 0.008 s |
| qiskit_opt3 | ok | 1,891 | 307 | 904 | 0.018 s |
| qiskit_commutative_inverse | ok | 2,620 | 367 | 1,037 | 0.075 s |
| baseline_ucc | ok | 5,494 | 818 | 764 | 0.058 s |
| optimized_ucc | ok | 1,891 | 307 | 904 | 0.046 s |

## mqt_qaoa_32

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 1,422 | 213 | 884 | 0.004 s |
| qiskit_opt1 | ok | 1,422 | 213 | 884 | 0.005 s |
| qiskit_opt3 | ok | 1,422 | 213 | 884 | 0.012 s |
| qiskit_commutative_inverse | ok | 1,422 | 213 | 884 | 0.026 s |
| baseline_ucc | ok | 6,310 | 597 | 884 | 0.057 s |
| optimized_ucc | ok | 1,422 | 213 | 884 | 0.036 s |

## mqt_grover_20

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 4,099,297 | 3,300,108 | 1,546,096 | 4.695 s |
| qiskit_opt1 | ok | 3,908,448 | 3,269,433 | 1,546,096 | 9.619 s |
| qiskit_opt3 | ok | 3,848,810 | 3,269,433 | 1,546,096 | 27.292 s |
| qiskit_commutative_inverse | ok | 4,099,297 | 3,300,108 | 1,546,096 | 4.662 s |
| baseline_ucc | ok | 14,046,115 | 8,500,182 | 1,544,960 | 77.823 s |
| optimized_ucc | ok | 3,848,810 | 3,269,433 | 1,546,096 | 27.515 s |
