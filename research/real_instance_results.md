# Real Algorithm-Family Baselines

Target basis: `['cx', 'rx', 'ry', 'rz', 'h']`

## phase_estimation_real

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 159,838 | 121,214 | 67,608 | 0.063 s |
| qiskit_opt1 | ok | 159,838 | 121,214 | 67,608 | 0.125 s |
| qiskit_opt3 | ok | 166,805 | 119,204 | 58,491 | 0.975 s |
| qiskit_commutative_inverse | ok | 159,838 | 121,214 | 67,608 | 0.335 s |
| baseline_ucc | ok | 471,819 | 328,271 | 58,491 | 62.844 s |
| optimized_ucc | ok | 166,805 | 119,204 | 58,491 | 1.045 s |

## grover_real

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 85,403 | 55,892 | 33,408 | 0.08 s |
| qiskit_opt1 | ok | 80,718 | 54,307 | 32,544 | 0.14 s |
| qiskit_opt3 | ok | 79,029 | 54,163 | 32,544 | 0.398 s |
| qiskit_commutative_inverse | ok | 85,403 | 55,892 | 33,408 | 0.081 s |
| baseline_ucc | ok | 287,047 | 152,298 | 32,544 | 1.433 s |
| optimized_ucc | ok | 79,029 | 54,163 | 32,544 | 0.404 s |

## qaoa_real

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 36,512 | 2,416 | 23,808 | 0.019 s |
| qiskit_opt1 | ok | 36,512 | 2,416 | 23,808 | 0.035 s |
| qiskit_opt3 | ok | 36,512 | 2,416 | 23,808 | 0.21 s |
| qiskit_commutative_inverse | ok | 36,512 | 2,416 | 23,808 | 0.298 s |
| baseline_ucc | ok | 167,833 | 7,133 | 23,808 | 0.754 s |
| optimized_ucc | ok | 36,512 | 2,416 | 23,808 | 0.207 s |
