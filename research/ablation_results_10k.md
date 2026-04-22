# Ablation Study (10,000 gates)

## qft_inverse

| Ablation | Output Gates | Output Depth | 2Q Gates | Runtime |
|---|---:|---:|---:|---:|
| full | 0 | 0 | 0 | 4.984 s |
| candidate_selection_only | 0 | 0 | 0 | 5.04 s |
| commutative_only | 0 | 0 | 0 | 4.961 s |
| no_prefix | 0 | 0 | 0 | 5.037 s |
| no_run | 0 | 0 | 0 | 4.954 s |
| no_adjacent_inverse | 0 | 0 | 0 | 4.99 s |
| no_candidate_selection | 0 | 0 | 0 | 5.031 s |

## qft_control

| Ablation | Output Gates | Output Depth | 2Q Gates | Runtime |
|---|---:|---:|---:|---:|
| full | 34,750 | 12,500 | 17,000 | 0.146 s |
| candidate_selection_only | 34,750 | 12,500 | 17,000 | 0.15 s |
| commutative_only | 34,750 | 12,500 | 17,000 | 0.147 s |
| no_prefix | 34,750 | 12,500 | 17,000 | 0.148 s |
| no_run | 34,750 | 12,500 | 17,000 | 0.147 s |
| no_adjacent_inverse | 34,750 | 12,500 | 17,000 | 0.148 s |
| no_candidate_selection | 34,750 | 12,500 | 17,000 | 0.148 s |

## qpe_style

| Ablation | Output Gates | Output Depth | 2Q Gates | Runtime |
|---|---:|---:|---:|---:|
| full | 21,206 | 14,002 | 6,002 | 2.132 s |
| candidate_selection_only | 21,206 | 14,002 | 6,002 | 2.098 s |
| commutative_only | 21,206 | 14,002 | 6,002 | 2.184 s |
| no_prefix | 21,206 | 14,002 | 6,002 | 2.079 s |
| no_run | 21,206 | 14,002 | 6,002 | 2.166 s |
| no_adjacent_inverse | 21,206 | 14,002 | 6,002 | 2.151 s |
| no_candidate_selection | 21,206 | 14,002 | 6,002 | 2.204 s |

## qaoa_ring

| Ablation | Output Gates | Output Depth | 2Q Gates | Runtime |
|---|---:|---:|---:|---:|
| full | 10,000 | 6,200 | 4,000 | 8.886 s |
| candidate_selection_only | 10,000 | 6,200 | 4,000 | 1.419 s |
| commutative_only | 10,000 | 6,200 | 4,000 | 1.514 s |
| no_prefix | 10,000 | 6,200 | 4,000 | 8.915 s |
| no_run | 10,000 | 6,200 | 4,000 | 8.031 s |
| no_adjacent_inverse | 10,000 | 6,200 | 4,000 | 2.523 s |
| no_candidate_selection | 30,055 | 16,355 | 4,000 | 7.703 s |

## grover_mirrored

| Ablation | Output Gates | Output Depth | 2Q Gates | Runtime |
|---|---:|---:|---:|---:|
| full | 115,811 | 76,210 | 46,800 | 0.772 s |
| candidate_selection_only | 115,811 | 76,210 | 46,800 | 0.747 s |
| commutative_only | 115,811 | 76,210 | 46,800 | 0.731 s |
| no_prefix | 115,811 | 76,210 | 46,800 | 0.729 s |
| no_run | 115,811 | 76,210 | 46,800 | 0.73 s |
| no_adjacent_inverse | 115,811 | 76,210 | 46,800 | 0.804 s |
| no_candidate_selection | 115,811 | 76,210 | 46,800 | 0.752 s |
