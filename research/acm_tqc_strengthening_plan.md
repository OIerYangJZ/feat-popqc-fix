# ACM/TQC Strengthening Plan

## Target Positioning

The current work is **not yet strong enough** to be pitched as:

- a universally better compiler than existing strong baselines, or
- a novel exact-inverse cancellation algorithm.

The strongest defensible positioning is:

> A bounded pre-basis structural preprocessing stage can materially improve
> UCC's default behavior on large repeated and inverse-structured circuits,
> while also reducing runtime on repeat-heavy workloads.

For an ACM Transactions on Quantum Computing (TQC) submission, the paper
should be framed as a **compiler systems / design automation** contribution
about **pipeline placement, structure-aware preprocessing, and empirical
compiler behavior**, not as a broad "new best compiler" claim.

## What ACM/TQC Will Likely Care About

The paper should be strengthened along four dimensions:

1. Originality
2. Correctness and technical precision
3. Strength of empirical comparison
4. Reproducibility / artifact quality

In practice, this means:

- define exactly what structural opportunity is being exploited
- compare against strong existing baselines
- show where the method helps and where it does not
- make the experimental pipeline easy to rerun

## Completed In This Round

The following ACM-style strengthening items have now been turned into concrete
research documents in this workspace:

- paper draft:
  - `quantum_paper_draft.md`
- reproducibility note:
  - `artifact_reproducibility_guide.md`
- existing algorithm/research note:
  - `prebasis_structural_simplification.md`

These documents now cover:

- abstract
- contribution statements
- problem definition
- algorithm description
- integration story
- experimental setup
- current result tables
- threats to validity
- artifact plan

The following experiment bundles have also been completed and saved:

- fixed-basis external baselines:
  - `fixed_basis_external_baselines_100k.json`
  - `fixed_basis_external_baselines_100k.md`
- scaling study:
  - `scaling_results.json`
  - `scaling_results.md`
- ablation study:
  - `ablation_results_10k.json`
  - `ablation_results_10k.md`

## Current Strongest Evidence

The current implementation already supports the following concrete claims.

### Fixed-basis controlled result

Using the same final target basis:

- `["cx", "rx", "ry", "rz", "h"]`

the current branch gives:

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

### Runtime improvements on large repeated structures

#### Repeated QFT (100k gates)

- previous prototype: `347,500` gates, depth `125,000`, `20.005s`
- current version: `347,500` gates, depth `125,000`, `6.368s`

Improvement:

- runtime reduced by about `68.2%`

#### Dominant repeated prefix + small tail (100k gates)

- previous version: `399,840` gates, depth `139,944`, `19.425s`
- current version: `347,401` gates, depth `124,990`, `8.705s`

Improvement:

- gate count reduced by about `13.1%`
- depth reduced by about `10.7%`
- runtime reduced by about `55.2%`

#### QAOA ring

- earlier UCC behavior: `290,092` gates, depth `170,189`
- current version: `100,000` gates, depth `62,000`, `1.763s`

Improvement:

- gate count reduced by about `65.5%`
- depth reduced by about `63.6%`

## What Must Be Strengthened Before ACM/TQC

### 1. Tighten the Core Claim

Do **not** claim:

- "we solve inverse cancellation"
- "we outperform all existing compilers"
- "UCC had a bug"

Do claim:

- UCC has a **pipeline optimization opportunity**
- structure-aware preprocessing before basis lowering can improve both
  output quality and runtime on selected structured workloads
- pipeline placement matters

### 2. Add a Formal Problem Definition

The paper should define:

- what counts as a repeated block
- what counts as an inverse-structured block
- what bounded preprocessing means
- what cost function is optimized when selecting candidates

This section should also explicitly distinguish:

- gate-set translation overhead
- missed structural simplification opportunities

### 3. Add Algorithmic Detail

The paper needs pseudocode for:

- pre-basis structural preprocessing
- repeated-prefix detection
- repeated-run detection
- adjacent `block + inverse(block)` cancellation
- candidate selection among:
  - basis translation
  - UCC default pipeline
  - preset-reference candidate

Also add a complexity discussion:

- best case
- worst case
- why the large-circuit fast path is needed

### 4. Strengthen the Baseline Comparison

The paper should include a uniform comparison table against:

- basis translation only
- baseline UCC
- `Qiskit` `optimization_level=0`
- `Qiskit` `optimization_level=1`
- `Qiskit` `optimization_level=3`
- `Qiskit` `CommutativeInverseCancellation`
- `TKET` if available and stable enough to run
- optimized UCC branch

All comparisons should use the **same final target basis**.

### 5. Expand Beyond Exact Inverse Cases

Exact inverse cancellation alone is not enough for novelty.

The strongest remaining direction is:

- structured workloads beyond exact inverse cancellation

Minimum benchmark families to keep:

- repeated `QFT + QFT^-1`
- repeated `QFT + QFT`
- `QPE-style`
- mirrored `Grover`-like circuits
- `QAOA` ring

### 6. Add Scaling Results

ACM/TQC reviewers will likely want scaling, not only one 100k point.

Current study sizes:

- `4k`
- `10k`
- `20k`
- `50k`
- `100k`

Metrics:

- gate count
- depth
- `cx` or multi-qubit gate count
- runtime

This is needed to show whether the method is only a single-point heuristic or
actually scales in a controlled way.

### 7. Add Ablation Studies

At minimum, separate the benefit of:

- inverse cancellation only
- repeated-prefix reuse only
- repeated-run detection
- adjacent inverse-block cancellation
- candidate selection only
- full method

Without ablation, the paper will read like an engineering bundle rather than a
clear research contribution.

### 8. Add Failure Cases

The paper must explicitly show where the method does **not** win.

Current examples already suggest:

- exact inverse cancellation is already handled by existing Qiskit techniques
- strong baselines may still match or beat the method on some workloads

This is a strength, not a weakness, if written clearly.

## Recommended Paper Structure

1. Introduction
2. Background and motivation
3. Problem definition
4. Pre-basis structural preprocessing algorithm
5. Integration into UCC
6. Experimental setup
7. Results
8. Ablation study
9. Threats to validity
10. Artifact and reproducibility package
11. Conclusion

## Recommended Contribution Statements

The paper should aim to defend contributions like these:

1. We identify that part of the large-circuit blow-up in UCC is due to missed
   structural simplification opportunities before basis lowering, not only to
   gate-set translation.

2. We design a bounded pre-basis structural preprocessing stage that combines
   inverse-aware cancellation, repeated-block detection, and candidate
   selection for large structured circuits.

3. We show that this preprocessing improves UCC's default behavior on large
   repeated and inverse-structured workloads, and can also reduce runtime on
   repeat-heavy circuits.

4. We provide a reproducible evaluation separating exact inverse cases from
   non-exact structured workloads and comparing against strong Qiskit-based
   baselines.

## Artifact Package Required for an ACM-Style Submission

To make the paper materially stronger, prepare an artifact package containing:

- exact benchmark generation scripts
- exact commands used to run all experiments
- raw result files in JSON or CSV
- plotting scripts
- environment file / lockfile
- one-command reproduction script
- README with expected runtime and hardware notes

Minimum folder structure:

```text
artifact/
  README.md
  requirements.txt or uv.lock
  scripts/
    generate_benchmarks.py
    run_all_experiments.py
    plot_results.py
  data/
    raw/
    processed/
  results/
    tables/
    figures/
```

## What To Do Next

The most important next steps are:

1. Convert the completed JSON/Markdown tables into publication-ready figures.
2. Package the artifact so another reviewer can rerun the results.
3. Decide whether to further optimize the slow `QPE-style` / `Grover` paths or
   to frame them explicitly as current limitations.
4. Rewrite the abstract and conclusion around the now-finished baseline,
   scaling, and ablation story.

## Updated Assessment After The New Experiments

The three previously missing experiment classes are now present:

1. fixed-basis external-baseline comparison
2. scaling study
3. ablation study

The main remaining gap is therefore no longer "missing experiments", but
"how strong the experimental story is against external baselines".

In particular:

- the branch looks strong on UCC-relative quality improvements
- it is strongest on repeated exact inverse structure
- it still scales poorly on `QPE-style` runtime
- it does not yet dominate strong Qiskit baselines on every family

## Submission Reality Check

If the paper stops at the current evidence, it is probably **below** what is
needed for a strong ACM TQC submission.

If the paper adds:

- stronger baseline comparison
- scaling plots
- ablations
- a reproducible artifact package
- a carefully limited claim

then it becomes much more plausible as an ACM-style systems/design-automation
submission in quantum compilation.
