# Repeated-Run Stability Summary

The stability study is now split into two parts:

1. repeated-run checks for the official real instances and the canonical
   hardware-aware seed
2. a fixed-seed sweep for the backend-aware `MQT Bench` cases

Raw files:

- `stability_results.json`
- `stability_results.md`
- `stability_seeded_results.json`
- `stability_seed2_results.json`
- `stability_seed3_results.json`
- `stability_seed4_results.json`
- `stability_seed5_results.json`

## Main conclusions

### 1. Real-instance results are fully stable

For the three official Qiskit circuit-library instances:

- `phase_estimation_real`
- `grover_real`
- `qaoa_real`

both `qiskit opt3` and `optimized_ucc` produce identical output metrics across
repeated runs:

- total gates: deterministic
- depth: deterministic
- `cx` count: deterministic

The runtime variance is small. In the canonical 5-run table:

- `phase_estimation_real`
  - `qiskit opt3`: `1.357 ± 0.119 s`
  - `optimized_ucc`: `2.031 ± 0.085 s`
- `grover_real`
  - `qiskit opt3`: `0.542 ± 0.006 s`
  - `optimized_ucc`: `1.035 ± 0.051 s`
- `qaoa_real`
  - `qiskit opt3`: `0.308 ± 0.008 s`
  - `optimized_ucc`: `0.487 ± 0.015 s`

So the official real-instance story is stable both structurally and
operationally.

### 2. Canonical hardware-aware outputs are deterministic for a fixed seed

For the canonical hardware-aware table with `seed_transpiler = 12345`:

- `hw_mqt_qpeexact_20`
  - `qiskit opt3`: `1572 / depth 407 / cx 812`
  - `optimized_ucc`: `1593 / depth 420 / cx 772`
- `hw_mqt_qaoa_20`
  - `qiskit opt3`: `2091 / depth 532 / cx 1530`
  - `optimized_ucc`: `2050 / depth 487 / cx 1458`

These outputs are deterministic across repeated runs for that fixed seed.

### 3. The hardware-aware QAOA win survives across five fixed seeds

The stronger stability claim now comes from the five-seed sweep:

- `0`
- `1`
- `42`
- `12345`
- `54321`

Across all five seeds, `hw_mqt_qaoa_20` remains a win for `optimized_ucc`
over `qiskit opt3`.

Examples:

- seed `0`
  - `qiskit opt3`: `2107 / depth 536 / cx 1468`
  - `optimized_ucc`: `2046 / depth 457 / cx 1430`
- seed `42`
  - `qiskit opt3`: `2085 / depth 513 / cx 1487`
  - `optimized_ucc`: `2061 / depth 466 / cx 1438`
- seed `54321`
  - `qiskit opt3`: `2127 / depth 523 / cx 1442`
  - `optimized_ucc`: `1992 / depth 425 / cx 1387`

So the backend-aware QAOA result is no longer a single-seed artifact.

### 4. Hardware-aware QPE remains mixed

For `hw_mqt_qpeexact_20`, the five-seed picture is mixed:

- some seeds give parity
- some seeds give lower `cx` for `optimized_ucc`
- but total gates and depth are not consistently better than `qiskit opt3`

This is still useful evidence, but it should be framed as a parity/lower-`cx`
case rather than as a clean external-baseline win.

## Practical takeaway

The stability study now supports three clean claims:

1. the official real-instance results are reproducible
2. the canonical hardware-aware table is reproducible for a fixed seed
3. the `hw_mqt_qaoa_20` backend-aware win is stable across five tested seeds
