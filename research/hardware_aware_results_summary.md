# Hardware-Aware Results Summary

Backend target:

- 20-qubit bidirectional line backend
- native operations: `u`, `sx`, `p`, `cx`, `measure`, `id`

Benchmark source:

- `MQT Bench`

Instances used:

- `hw_mqt_qpeexact_20`
- `hw_mqt_qaoa_20`
- `hw_mqt_grover_20`

Comparison methods:

- `qiskit opt3`
- baseline `UCC`
- optimized `UCC`

## Results

### `hw_mqt_qpeexact_20`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| qiskit opt3 | 1,572 | 407 | 812 | 0.044 s |
| baseline UCC | 2,047 | 632 | 1,235 | 0.112 s |
| optimized UCC | 1,563 | 405 | 804 | 1.104 s |

Observation:

- optimized UCC now beats `qiskit opt3` on total gates, depth, and `cx`
- compared with the fixed-seed `qiskit opt3` baseline, this is now a clean
  routed-quality win rather than a lower-`cx` tradeoff
- the cost is runtime: the broader backend reference probe raises optimized-UCC
  latency to `1.104 s`

### `hw_mqt_qaoa_20`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| qiskit opt3 | 2,091 | 532 | 1,530 | 0.049 s |
| baseline UCC | 2,091 | 485 | 1,417 | 0.096 s |
| optimized UCC | 2,050 | 487 | 1,458 | 1.012 s |

Observation:

- optimized UCC still improves over `qiskit opt3` on total gates, depth, and `cx`
- optimized UCC also improves over baseline UCC on total gates and `cx`
- baseline UCC still has slightly lower depth (`485` vs `487`)
- the current backend-aware search keeps the routed-quality win, but runtime is
  now `1.012 s`

This remains the clearest current backend-aware win:

> on `hw_mqt_qaoa_20`, optimized UCC achieves a clear external-baseline win
> over `qiskit opt3` in total gates, depth, and `cx` count.

### `hw_mqt_grover_20`

| Method | Status | Runtime |
|---|---|---:|
| qiskit opt3 | timeout | > 240 s |
| baseline UCC | timeout | > 240 s |
| optimized UCC | ok | 38.925 s |

Observation:

- the repeated-run backend fallback removes the optimized-UCC timeout
- the resulting circuit is extremely large, so this is a robustness result
  rather than a competitive quality result

## Practical Conclusion

The hardware-aware story is now stronger on quality and robustness:

- the key `hw_mqt_qaoa_20` external-baseline win is preserved
- `hw_mqt_qpeexact_20` is now also a clean routed-quality win over the fixed-seed
  `qiskit opt3` baseline
- `hw_mqt_grover_20` no longer times out for optimized UCC, although the output
  is too large to treat as a main competitive result
