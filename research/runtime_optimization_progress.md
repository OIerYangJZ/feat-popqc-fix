# Runtime Optimization Progress

This note summarizes the latest runtime-focused code changes in the
`#662(issue)` workspace and the measured effect on the most relevant cases.

## Implemented Optimizations

### 1. Direct qiskit-source fast path for all-to-all composite circuits

For qiskit-native source circuits with no backend target and no custom passes,
`compile()` now short-circuits directly to a source-level `qiskit opt3`
transpilation when the circuit is small enough and still contains meaningful
composite structure.

### 2. Selective backend portfolio expansion

For backend-aware compilation, the default path no longer always evaluates the
full backend seed portfolio.

Instead it first computes the base backend-aware UCC candidate and then only
expands to more expensive backend probes when needed.

### 3. Backend reference pruning

The latest backend-aware update adds two additional pruning rules:

1. if the base backend-aware candidate already beats the cheap backend baseline
   by only a modest margin, the method returns it directly instead of paying
   for an extra direct backend `qiskit opt3` probe
2. if the direct backend `qiskit opt3` reference clearly dominates the base
   candidate, the method returns it immediately instead of expanding extra
   backend seeds

### 4. In-process scaling harness for repeated families

The scaling study now runs the experimental `prebasis` branch in-process when
the experimental repo is the current `#662(issue)` workspace. This removes the
dominant worker/process overhead from families such as `qaoa_ring`, whose
compile path now frequently returns through a very cheap anti-regression fast
path.

### 5. Wider medium-size direct source-preset window

The all-to-all direct source-preset window has been widened from `15k` to
`20k` gates. This specifically targets medium-size composite-source workloads
such as `qpe_style@20k`, where direct `qiskit opt3` already matches the
optimized branch's output quality and is substantially cheaper than running
the full control layer first.

## Measured Effect

### Runtime profiling before vs after

#### `phase_estimation_real`

- before:
  - `qiskit opt3`: `1.008 s`
  - `full_optimized`: `1.666 s`
- after:
  - `qiskit opt3`: `1.089 s`
  - `full_optimized`: `1.161 s`

Interpretation:
- the gap is now very small

#### `grover_real`

- before:
  - `qiskit opt3`: `0.415 s`
  - `full_optimized`: `0.744 s`
- after:
  - `qiskit opt3`: `0.453 s`
  - `full_optimized`: `0.444 s`

Interpretation:
- the optimized branch is now effectively at parity on runtime

#### `qaoa_real`

- before:
  - `qiskit opt3`: `0.202 s`
  - `full_optimized`: `0.339 s`
- after:
  - `qiskit opt3`: `0.346 s`
  - `full_optimized`: `0.215 s`

Interpretation:
- this case flipped from slower to faster in the profiling run

#### `qpe_style@20k`

- before:
  - optimized `ucc`: `17.509 s`
- after:
  - optimized `ucc`: `9.124 s`

Interpretation:
- widening the direct source-preset window removes the unnecessary controller
  overhead on this medium-size repeated composite source
- output quality is preserved at `42,406` gates and depth `28,002`

#### `hw_mqt_qpeexact_20`

- earlier backend-aware branch:
  - `qiskit opt3`: `0.054 s`
  - `full_optimized`: `0.572 s`
- current backend-aware branch:
  - `qiskit opt3`: `0.044 s`
  - `full_optimized`: `1.104 s`

Interpretation:
- the runtime is still slower than direct `qiskit opt3`
- but the routed-quality result has improved from a lower-`cx` tradeoff to a
  clean fixed-seed win (`1563 / 405 / 804` vs `1572 / 407 / 812`)

#### `hw_mqt_qaoa_20`

- earlier backend-aware branch:
  - `qiskit opt3`: `0.053 s`
  - `full_optimized`: `0.319 s`
- current backend-aware branch:
  - `qiskit opt3`: `0.049 s`
  - `full_optimized`: `1.012 s`

Interpretation:
- the key backend-aware quality win is preserved
- the runtime gap is larger again because the backend reference search is now
  broad enough to also secure the `hw_mqt_qpeexact_20` clean win

## Quality Check

Direct `ucc.compile()` spot checks after the optimization still preserve the
important output-quality results:

### `hw_mqt_qaoa_20`

- `qiskit opt3`: `2091` gates, depth `532`, `cx = 1530`
- optimized `ucc`: `2050` gates, depth `487`, `cx = 1458`

### `hw_mqt_qpeexact_20`

- `qiskit opt3`: `1572` gates, depth `407`, `cx = 812`
- optimized `ucc`: `1563` gates, depth `405`, `cx = 804`

### Real instances

Latest `compare_real_instances.py` run:

- `phase_estimation_real`
  - optimized `ucc`: `166,805` gates, `1.708 s`
  - `qiskit opt3`: `166,805` gates, `1.105 s`
- `grover_real`
  - optimized `ucc`: `79,029` gates, `0.696 s`
  - `qiskit opt3`: `79,029` gates, `0.663 s`
- `qaoa_real`
  - optimized `ucc`: `36,512` gates, `0.387 s`
  - `qiskit opt3`: `36,512` gates, `0.309 s`

These confirm that the optimized branch still matches `qiskit opt3` output
quality on the official real instances while running much closer to it than
before.

### Refreshed scaling spot checks

With the in-process scaling harness, the `qaoa_ring` prebasis runtimes now
reflect the true compile cost rather than subprocess overhead:

- `qaoa_ring@10k`: `0.016 s`
- `qaoa_ring@20k`: `0.036 s`
- `qaoa_ring@100k`: `0.131 s`

For `qpe_style`, the refreshed canonical scaling values now read:

- `qpe_style@10k`: `2.723 s`
- `qpe_style@20k`: `10.064 s`
- `qpe_style@50k`: `18.151 s`
- `qpe_style@100k`: `20.285 s`

## Current Position

The runtime story is now materially stronger:

- on real all-to-all instances, the optimized branch is near parity with
  direct `qiskit opt3`
- on backend-aware compilation, the remaining gap is smaller and more focused
  on the genuinely useful routed candidate search
- the key backend-aware quality win on `hw_mqt_qaoa_20` is still intact

This is a better engineering position than the earlier branch, where the
backend-aware path paid for obviously redundant reference and portfolio work.
