# Bounded Pre-Basis Structural Preprocessing for UCC on Structured Quantum Circuits

## Abstract

Quantum compilation pipelines often lower structured circuits into basis gates
before higher-level structure can be exploited. In UCC, this can lead to large
regressions on workloads with repeated, mirrored, or inverse-related structure.
We study this phenomenon as a compiler-systems problem rather than as a claim
of a universally superior optimizer. Our method combines bounded pre-basis
structural preprocessing, conservative candidate selection, source-level
short-circuiting, and limited backend-aware portfolio search.

The main result is not that the method dominates strong Qiskit baselines on all
workloads. Instead, we show a narrower and more defensible claim: it acts as an
anti-regression and quality-recovery layer for UCC. On three official Qiskit
circuit-library instances (`PhaseEstimation`, `GroverOperator`, and
`QAOAAnsatz`), the optimized branch recovers `qiskit opt3`-level output quality
while greatly improving over baseline UCC. On public benchmark suites (`MQT
Bench` and `SupermarQ`), it repeatedly matches strong Qiskit output quality and
substantially reduces baseline-UCC regressions. On a 20-qubit line-connectivity
backend, it also produces a stable external-baseline win on `hw_mqt_qaoa_20`,
beating `qiskit opt3` in total gates, depth, and `cx` count across five fixed
transpiler seeds. These results support a pipeline-redesign claim: bounded
structure-aware preprocessing before basis lowering is a meaningful
optimization opportunity for UCC.

## 1. Introduction

Quantum compilation often destroys useful high-level structure early. When a
circuit contains repeated blocks, mirrored subroutines, or inverse-related
patterns, lowering to a basis too early can erase information that later local
passes cannot cheaply recover. This is especially relevant for unified
compilation frameworks such as UCC, where the default pipeline must remain
conservative but should also avoid severe regressions on structured workloads.

This paper studies that issue in UCC. The goal is not to claim a globally
stronger compiler than Qiskit. The goal is to determine whether bounded
pre-basis structural preprocessing can materially improve UCC's default
behavior, recover strong external-baseline quality on real instances, and avoid
pathological growth on structured families.

The resulting contribution is best understood as a compiler-systems redesign:
it changes where structure is exploited in the pipeline, how candidate outputs
are compared, and when the optimizer should short-circuit to cheaper or stronger
reference paths.

## 2. Contributions

The paper makes four claims.

1. Large-circuit regressions in UCC are not explained only by basis conversion;
   missed simplification before basis lowering is also a real source of growth.
2. A bounded pre-basis preprocessing stage can exploit repeated, inverse, and
   mirrored structure before default lowering destroys it.
3. The strongest practical gains come from combining preprocessing with
   conservative candidate selection and short-circuiting rather than from any
   single rewrite rule.
4. On real algorithm-family circuits, public benchmark suites, and one
   hardware-aware public case, this design recovers or exceeds strong external
   baseline quality while substantially improving over baseline UCC.

## 3. Method

### 3.1 Structured patterns

We focus on bounded detection of the following patterns in the pre-lowering
instruction stream:

- exact inverse blocks: `U U^dagger`
- repeated exact blocks
- mirrored blocks such as `U M U^dagger`
- dominant repeated prefixes followed by a short tail

### 3.2 Pre-basis preprocessing

For a bounded number of outer iterations, the method applies:

1. repeated-prefix detection and reuse
2. repeated-run detection and reuse
3. adjacent exact inverse-block cancellation
4. commutative inverse cancellation
5. adjacent parameterized-gate merging when legal

If one full outer iteration does not shrink the circuit, preprocessing stops.

### 3.3 Candidate-selection policy

The method does not trust a single optimization path. Instead, it compares a
small set of candidates depending on the compilation regime:

- pure basis translation
- the default UCC path
- source-level or pre-simplified `qiskit opt3` references where justified
- limited backend-aware portfolio candidates when routing instability is known
  to matter

The output with the lowest conservative structural cost is returned.

### 3.4 Positioning

This is not a claim that exact inverse cancellation is novel. Nor is it a claim
that the branch already dominates strong external baselines on every workload.
The intended claim is narrower: bounded structure-aware preprocessing plus
careful candidate control can materially improve UCC's default behavior on
structured circuits.

## 4. Experimental Setup

### 4.1 Controlled fixed-basis studies

We use a fixed target basis

- `['cx', 'rx', 'ry', 'rz', 'h']`

for all all-to-all comparisons. This isolates structural effects from arbitrary
gateset differences.

### 4.2 Real and public benchmarks

We evaluate on:

- official Qiskit circuit-library instances:
  - `phase_estimation_real`
  - `grover_real`
  - `qaoa_real`
- `MQT Bench`:
  - `mqt_qpeexact_32`
  - `mqt_qaoa_32`
  - `mqt_grover_20`
- `SupermarQ`:
  - `supermarq_mermin_bell_8`
  - `supermarq_qaoa_vanilla_12`
  - `supermarq_hamiltonian_sim_8`

### 4.3 Hardware-aware setup

We also evaluate a routed setting using a fixed 20-qubit bidirectional line
backend with native operations:

- `u`
- `sx`
- `p`
- `cx`
- `measure`
- `id`

The main backend-aware cases are:

- `hw_mqt_qpeexact_20`
- `hw_mqt_qaoa_20`

### 4.4 Metrics

We report:

- total gate count
- depth
- `cx` count
- runtime

We also include repeated-run and fixed-seed stability measurements.

## 5. Results

### 5.1 Controlled fixed-basis structural results

#### Repeated `QFT + QFT^-1` (100k gates)

| Method | Output Gates | Output Depth |
|---|---:|---:|
| translation only | 400,000 | 142,500 |
| baseline UCC | 968,784 | 276,266 |
| optimized branch | 0 | 0 |

#### Repeated `QFT + QFT` control (100k gates)

| Method | Output Gates | Output Depth |
|---|---:|---:|
| translation only | 400,000 | 140,000 |
| baseline UCC | 1,207,504 | 317,501 |
| optimized branch | 347,500 | 125,000 |

These results show that after controlling for the final target basis, a strong
simplification opportunity remains before basis lowering.

### 5.2 Fixed-basis external baselines at 100k gates

The most important canonical observations are:

- repeated `QFT + QFT^-1`
  - `Qiskit CommutativeInverseCancellation`: `0`
  - optimized UCC: `0`
- repeated `QFT + QFT`
  - `qiskit opt3`: `347,500`
  - optimized UCC: `347,500`
- `qpe_style`
  - baseline UCC: `456,013`
  - optimized UCC: `167,800`
  - `qiskit opt3`: timeout at `> 120s`
- `qaoa_ring`
  - baseline UCC: `300,055`
  - optimized UCC: `100,000`
  - strong fixed-basis baselines: `100,000`
- `grover_mirrored`
  - baseline UCC: `4,122,006`
  - optimized UCC: `1,158,011`
  - `qiskit opt3`: `1,158,011`

The fixed-basis study supports three points:

1. exact inverse cancellation by itself is not novel;
2. baseline UCC can be dramatically worse than strong external baselines;
3. the optimized branch often recovers the strongest fixed-basis quality and in
   `qpe_style` remains stronger than the timed-out `qiskit opt3` reference.

### 5.3 Official real instances

| Instance | baseline UCC | optimized UCC | qiskit opt3 |
|---|---:|---:|---:|
| `phase_estimation_real` | `471,819` gates, `75.538s` | `166,805` gates, `1.989s` | `166,805` gates, `1.254s` |
| `grover_real` | `287,047` gates, `1.688s` | `79,029` gates, `0.955s` | `79,029` gates, `0.521s` |
| `qaoa_real` | `167,833` gates, `0.904s` | `36,512` gates, `0.420s` | `36,512` gates, `0.273s` |

Interpretation:

- optimized UCC strongly improves over baseline UCC on all three official
  instances;
- on all three, output quality matches `qiskit opt3` exactly;
- runtime is now within a small constant factor of `qiskit opt3`.

### 5.4 Public benchmark suites

#### `MQT Bench`

Representative canonical results:

- `mqt_qpeexact_32`
  - baseline UCC: `5,494`
  - optimized UCC: `1,891`
  - `qiskit opt3`: `1,891`
- `mqt_qaoa_32`
  - baseline UCC: `6,310`
  - optimized UCC: `1,422`
  - `qiskit opt3`: `1,422`
- `mqt_grover_20`
  - baseline UCC: timeout `> 120s`
  - optimized UCC: `3,848,810`
  - `qiskit opt3`: `3,848,810`

#### `SupermarQ`

Representative canonical results:

- `supermarq_mermin_bell_8`
  - baseline UCC: `386` gates, depth `135`
  - optimized UCC: `76` gates, depth `44`
  - `qiskit opt3`: `76` gates, depth `44`
- `supermarq_qaoa_vanilla_12`
  - baseline UCC: `947` gates, depth `225`
  - optimized UCC: `222` gates, depth `80`
  - `qiskit opt3`: `222` gates, depth `80`
- `supermarq_hamiltonian_sim_8`
  - baseline UCC: `71` gates, depth `36`
  - optimized UCC: `71` gates, depth `36`
  - `qiskit opt3`: `51` gates, depth `24`

Interpretation:

- the quality-recovery story generalizes beyond official Qiskit-library
  instances;
- the branch is clearly useful on multiple public benchmark families;
- but the method is not uniformly superior on every family.

### 5.5 Hardware-aware results

#### Canonical fixed-seed results (`seed_transpiler = 12345`)

| Instance | qiskit opt3 | baseline UCC | optimized UCC |
|---|---:|---:|---:|
| `hw_mqt_qpeexact_20` | `1572 / depth 407 / cx 812 / 0.044s` | `2047 / depth 632 / cx 1235 / 0.112s` | `1563 / depth 405 / cx 804 / 1.104s` |
| `hw_mqt_qaoa_20` | `2091 / depth 532 / cx 1530 / 0.049s` | `2091 / depth 485 / cx 1417 / 0.096s` | `2050 / depth 487 / cx 1458 / 1.012s` |

Interpretation:

- `hw_mqt_qpeexact_20` is now a clean fixed-seed routed-quality win:
  optimized UCC improves over `qiskit opt3` on total gates, depth, and `cx`,
  at the cost of higher runtime.
- `hw_mqt_qaoa_20` is the clearest hardware-aware win: optimized UCC improves
  over `qiskit opt3` in total gates, depth, and `cx`.
- `hw_mqt_grover_20` remains too large to use as a main routed-quality table,
  but optimized UCC no longer times out on that case.

#### Five-seed sweep

Across seeds `0`, `1`, `42`, `12345`, and `54321`, the `hw_mqt_qaoa_20`
external-baseline win persists. Representative pairs are:

- seed `0`
  - `qiskit opt3`: `2107 / depth 536 / cx 1468`
  - optimized UCC: `2046 / depth 457 / cx 1430`
- seed `42`
  - `qiskit opt3`: `2085 / depth 513 / cx 1487`
  - optimized UCC: `2061 / depth 466 / cx 1438`
- seed `54321`
  - `qiskit opt3`: `2127 / depth 523 / cx 1442`
  - optimized UCC: `1992 / depth 425 / cx 1387`

So the hardware-aware QAOA result is not a single-seed artifact.

### 5.6 Scaling and ablation

The scaling study covers `4k`, `10k`, `20k`, `50k`, and `100k` input sizes for:

- `qft_inverse`
- `qpe_style`
- `qaoa_ring`
- `grover_mirrored`

The most important scaling conclusions are:

- `qft_inverse` is solved maximally strongly at every tested size (`0` gates)
- `qpe_style` remains one of the strongest wins; at `100k`, optimized UCC
  reaches `167,800` gates in `20.285s`, and at `20k` the latest direct
  source-preset widening reduces runtime to `10.064s` while preserving the
  same `42,406`-gate output
- `qaoa_ring` consistently avoids baseline-UCC inflation; at `100k`, output
  remains `100,000`, and the refreshed in-process scaling harness shows that
  the earlier mid-scale runtime spike was dominated by worker/process overhead
- `grover_mirrored` improves strongly over baseline UCC but remains runtime
  heavy at scale

The ablation study shows that the current branch is now concentrated around a
systems contribution rather than a single rewrite rule. In particular,
**candidate selection** remains the dominant practical component on the
anti-regression families, especially `qaoa_ring`, where removing candidate
selection regresses the `10k` output from `10,000` to `30,055` gates.

## 6. Discussion

The current evidence supports four main conclusions.

First, pipeline placement matters. Exploiting structure before basis lowering
is meaningfully stronger than trying to recover it only after the default flow.

Second, the current gains are not explained by a simple pass-ordering fix
alone. A minimal `UCCDefaults`-level bundle explains part of the story, but not
the full improvements seen on real instances and large structured workloads.

Third, the branch is best understood as a bounded systems redesign for UCC:
pre-basis preprocessing, candidate selection, short-circuiting, and limited
backend-aware portfolio search interact to deliver the current behavior.

Fourth, the strongest claim is selective rather than universal. The branch does
not dominate strong external baselines on every family, but it repeatedly
recovers `qiskit opt3`-level output quality and achieves a stable
hardware-aware win on `hw_mqt_qaoa_20`.

## 7. Limitations

This study has several limitations.

1. The evaluation is centered on UCC and Qiskit-flavored workflows.
2. Some benchmark families are intentionally structured and may not represent
   all realistic workloads.
3. The method is bounded and heuristic rather than globally optimal.
4. Strong external baselines still match or exceed the method on some families,
   for example `supermarq_hamiltonian_sim_8` and the mixed
   `hw_mqt_qpeexact_20` case.
5. The strongest external-baseline story is selective rather than dominant
   across all workloads.

## 8. Reproducibility

The frozen research directory includes a standardized artifact entry point:

- `run_frozen_artifact.py`

plus supporting documentation:

- `artifact_environment_snapshot.md`
- `artifact_output_manifest.md`
- `artifact_reproducibility_guide.md`

These provide:

- the local environment and package snapshot
- canonical output files for each experiment family
- one-command reproduction of the frozen suite

## 9. Conclusion

This work supports a compiler-systems claim rather than a sweeping algorithmic
one. Bounded pre-basis structural preprocessing can materially improve UCC's
default behavior on structured circuits, recover `qiskit opt3`-level quality on
real and public benchmark instances, and exceed `qiskit opt3` on at least one
stable hardware-aware public case. The most accurate interpretation is that the
optimized branch is a strong anti-regression and quality-recovery layer for UCC,
not a universally dominant replacement for direct Qiskit transpilation.
