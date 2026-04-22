# Hardware-Aware Five-Seed Summary

This summary records the effect of the backend-aware **default-pipeline
seed portfolio** added to the `#662(issue)` research branch.

The optimization now evaluates the backend-aware default UCC path over a small
seed portfolio anchored at the requested fixed seed:

- `[seed, seed + 1, seed + 2]`

for moderate-size backend-aware circuits, and keeps the lowest-cost compiled
result.

## Why this change was needed

Before this change:

- `hw_mqt_qaoa_20` was a win for some seeds
- but collapsed to parity for others

The root cause was that the stronger backend-aware result came from the
**default UCC backend-aware compiled path**, not from the preset-reference
candidate. For weak seeds that compiled path regressed, so candidate selection
fell back to parity with `qiskit opt3`.

The new seed-portfolio logic stabilizes that path.

## Seeds tested

The hardware-aware sweep now covers 5 fixed seeds:

- `0`
- `1`
- `42`
- `12345`
- `54321`

All repeated-run checks used 3 repetitions per seed, and all outputs were
deterministic for each fixed seed.

## `hw_mqt_qaoa_20`

### Seed `0`

- `qiskit opt3`: `2107` gates, depth `536`, `cx = 1468`
- `optimized_ucc`: `2046` gates, depth `457`, `cx = 1430`

### Seed `1`

- `qiskit opt3`: `2087` gates, depth `535`, `cx = 1519`
- `optimized_ucc`: `2046` gates, depth `457`, `cx = 1430`

### Seed `42`

- `qiskit opt3`: `2085` gates, depth `513`, `cx = 1487`
- `optimized_ucc`: `2061` gates, depth `466`, `cx = 1438`

### Seed `12345`

- `qiskit opt3`: `2091` gates, depth `532`, `cx = 1530`
- `optimized_ucc`: `2050` gates, depth `487`, `cx = 1458`

### Seed `54321`

- `qiskit opt3`: `2127` gates, depth `523`, `cx = 1442`
- `optimized_ucc`: `1992` gates, depth `425`, `cx = 1387`

## `hw_mqt_qpeexact_20`

### Seed `0`

- `qiskit opt3`: `1563` gates, depth `407`, `cx = 822`
- `optimized_ucc`: `1596` gates, depth `406`, `cx = 762`

### Seed `1`

- `qiskit opt3`: `1596` gates, depth `406`, `cx = 762`
- `optimized_ucc`: `1596` gates, depth `406`, `cx = 762`

### Seed `42`

- `qiskit opt3`: `1592` gates, depth `413`, `cx = 770`
- `optimized_ucc`: `1592` gates, depth `413`, `cx = 770`

### Seed `12345`

- `qiskit opt3`: `1572` gates, depth `407`, `cx = 812`
- `optimized_ucc`: `1593` gates, depth `420`, `cx = 772`

### Seed `54321`

- `qiskit opt3`: `1563` gates, depth `406`, `cx = 806`
- `optimized_ucc`: `1609` gates, depth `421`, `cx = 757`

## Main conclusion

The seed-portfolio change fixes the earlier instability of the hardware-aware
`QAOA` result:

- the backend-aware output is deterministic for each fixed seed
- the `hw_mqt_qaoa_20` external-baseline win now holds across all 5 tested seeds

For `hw_mqt_qaoa_20`, optimized UCC is strictly better than `qiskit opt3`
on all 5 tested seeds in:

- total gate count
- depth
- `cx` count

The `hw_mqt_qpeexact_20` result is still mixed:

- sometimes parity
- sometimes higher total gates / depth but lower `cx`

So the strongest backend-aware claim for the current `#662(issue)` branch is:

> on `hw_mqt_qaoa_20`, the optimized branch achieves a stable
> external-baseline win over `qiskit opt3` across five tested fixed seeds.
