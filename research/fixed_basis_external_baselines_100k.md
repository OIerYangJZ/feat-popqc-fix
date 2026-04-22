# Fixed-Basis External Baselines

Target basis: `['cx', 'rx', 'ry', 'rz', 'h']`

## qft_inverse

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 400,000 | 142,500 | 170,000 | 0.206 s |
| qiskit_opt0 | ok | 400,000 | 142,500 | 170,000 | 0.204 s |
| qiskit_opt1 | ok | 365,002 | 130,002 | 140,000 | 0.538 s |
| qiskit_opt3 | timeout | - | - | - | > 120 s |
| qiskit_commutative_inverse | ok | 0 | 0 | 0 | 1.794 s |
| tket_full_peephole | unavailable | - | - | - | - |
| baseline_ucc | ok | 968,784 | 276,266 | 135,004 | 4.885 s |
| optimized_ucc | ok | 0 | 0 | 0 | 14.51 s |

## qft_control

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 400,000 | 140,000 | 170,000 | 0.208 s |
| qiskit_opt0 | ok | 400,000 | 140,000 | 170,000 | 0.203 s |
| qiskit_opt1 | ok | 400,000 | 140,000 | 170,000 | 0.413 s |
| qiskit_opt3 | ok | 347,500 | 125,000 | 170,000 | 1.603 s |
| qiskit_commutative_inverse | ok | 400,000 | 140,000 | 170,000 | 1.724 s |
| tket_full_peephole | unavailable | - | - | - | - |
| baseline_ucc | ok | 1,207,504 | 317,501 | 170,000 | 5.521 s |
| optimized_ucc | ok | 347,500 | 125,000 | 170,000 | 4.954 s |

## qpe_style

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 396,000 | 296,001 | 156,000 | 0.208 s |
| qiskit_opt0 | ok | 396,000 | 296,001 | 156,000 | 0.208 s |
| qiskit_opt1 | ok | 396,000 | 296,001 | 156,000 | 0.404 s |
| qiskit_opt3 | timeout | - | - | - | > 120 s |
| qiskit_commutative_inverse | ok | 396,000 | 296,001 | 156,000 | 1.545 s |
| tket_full_peephole | unavailable | - | - | - | - |
| baseline_ucc | ok | 456,013 | 236,011 | 60,002 | 2.567 s |
| optimized_ucc | ok | 167,800 | 110,001 | 60,200 | 19.675 s |

## qaoa_ring

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 100,000 | 62,000 | 40,000 | 0.025 s |
| qiskit_opt0 | ok | 100,000 | 62,000 | 40,000 | 0.025 s |
| qiskit_opt1 | ok | 100,000 | 62,000 | 40,000 | 0.063 s |
| qiskit_opt3 | ok | 100,000 | 62,000 | 40,000 | 0.301 s |
| qiskit_commutative_inverse | ok | 100,000 | 62,000 | 40,000 | 0.435 s |
| tket_full_peephole | unavailable | - | - | - | - |
| baseline_ucc | ok | 300,055 | 163,055 | 40,000 | 1.281 s |
| optimized_ucc | ok | 100,000 | 62,000 | 40,000 | 1.543 s |

## grover_mirrored

| Method | Status | Output Gates | Output Depth | CX Count | Runtime |
|---|---|---:|---:|---:|---:|
| translation_only | ok | 1,370,000 | 840,009 | 492,000 | 1.928 s |
| qiskit_opt0 | ok | 1,370,000 | 840,009 | 492,000 | 1.905 s |
| qiskit_opt1 | ok | 1,184,009 | 772,009 | 468,000 | 3.213 s |
| qiskit_opt3 | ok | 1,158,011 | 762,010 | 468,000 | 7.733 s |
| qiskit_commutative_inverse | ok | 1,334,004 | 836,009 | 492,000 | 2.308 s |
| tket_full_peephole | unavailable | - | - | - | - |
| baseline_ucc | ok | 4,122,006 | 2,166,021 | 468,000 | 22.798 s |
| optimized_ucc | ok | 1,158,011 | 762,010 | 468,000 | 9.395 s |
