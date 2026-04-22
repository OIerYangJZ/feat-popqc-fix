# 实验结果总览（`#662(issue)`）

本文档汇总 `#662(issue)` 工作区中当前冻结后的主要实验结果与结论，供论文、grant、reviewer 回复和内部讨论统一引用。

对应的 canonical 结果文件主要包括：

- `real_instance_results_summary.md`
- `mqt_bench_results_summary.md`
- `supermarq_results_summary.md`
- `hardware_aware_results_summary.md`
- `runtime_optimization_progress.md`
- `runtime_overheads_issue_summary.md`

## 1. 当前工作的核心问题

当前工作的目标不是提出一个“全面优于 Qiskit 的新编译器”，而是研究：

- UCC 默认流水线在结构化电路上会出现怎样的退化；
- 这种退化是否只是简单的 pass 顺序问题；
- bounded pre-basis structural preprocessing 加上 candidate selection / short-circuiting 是否能稳定修复这些退化；
- 在真实算法族实例、公共 benchmark 和 hardware-aware 条件下，这种修复是否仍然成立。

当前最准确的定位是：

> 这套优化是一个面向 UCC 的 anti-regression / quality-recovery layer，能够在多个真实或公开 benchmark 场景下把 UCC 的输出质量拉回到接近 `qiskit opt3` 的水平，并在部分 hardware-aware case 上取得明确的 external-baseline win。

## 2. 官方真实实例（Qiskit circuit library）

固定 target basis：

- `['cx', 'rx', 'ry', 'rz', 'h']`

使用的官方实例：

- `PhaseEstimation`
- `GroverOperator`
- `QAOAAnsatz`

### 2.1 `phase_estimation_real`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 159,838 | 121,214 | 67,608 | 0.100 s |
| qiskit opt3 | 166,805 | 119,204 | 58,491 | 1.254 s |
| baseline UCC | 471,819 | 328,271 | 58,491 | 75.538 s |
| optimized UCC | 166,805 | 119,204 | 58,491 | 1.989 s |

结论：

- 相比 baseline UCC，门数下降约 `64.6%`。
- 输出质量与 `qiskit opt3` 完全追平。
- runtime 已压到与 `qiskit opt3` 同一量级。

### 2.2 `grover_real`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 85,403 | 55,892 | 33,408 | 0.084 s |
| qiskit opt3 | 79,029 | 54,163 | 32,544 | 0.521 s |
| baseline UCC | 287,047 | 152,298 | 32,544 | 1.688 s |
| optimized UCC | 79,029 | 54,163 | 32,544 | 0.955 s |

结论：

- 相比 baseline UCC，门数下降约 `72.5%`。
- 输出质量与 `qiskit opt3` 追平。
- runtime 在小常数因子范围内落后于 `qiskit opt3`，但已远好于早期分支。

### 2.3 `qaoa_real`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 36,512 | 2,416 | 23,808 | 0.020 s |
| qiskit opt3 | 36,512 | 2,416 | 23,808 | 0.273 s |
| baseline UCC | 167,833 | 7,133 | 23,808 | 0.904 s |
| optimized UCC | 36,512 | 2,416 | 23,808 | 0.420 s |

结论：

- 相比 baseline UCC，门数下降约 `78.2%`。
- 输出质量与 `qiskit opt3` 追平。
- runtime 与 `qiskit opt3` 接近。

### 2.4 真实实例总论

在这 3 个官方真实实例上，当前工作已经证明：

- baseline UCC 的退化是真实且严重的；
- optimized UCC 能稳定把输出质量拉回到 `qiskit opt3` 水平；
- 当前 runtime 已不再是数量级落后，而是小常数差距。

## 3. 公共 benchmark source 1：MQT Bench

实例：

- `mqt_qpeexact_32`
- `mqt_qaoa_32`
- `mqt_grover_20`

### 3.1 `mqt_qpeexact_32`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 2,620 | 367 | 1,037 | 0.007 s |
| qiskit opt3 | 1,891 | 307 | 904 | 0.023 s |
| baseline UCC | 5,494 | 818 | 764 | 0.089 s |
| optimized UCC | 1,891 | 307 | 904 | 0.425 s |

### 3.2 `mqt_qaoa_32`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 1,422 | 213 | 884 | 0.004 s |
| qiskit opt3 | 1,422 | 213 | 884 | 0.014 s |
| baseline UCC | 6,310 | 597 | 884 | 0.071 s |
| optimized UCC | 1,422 | 213 | 884 | 0.327 s |

### 3.3 `mqt_grover_20`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| translation only | 4,099,297 | 3,300,108 | 1,546,096 | 6.106 s |
| qiskit opt3 | 3,848,810 | 3,269,433 | 1,546,096 | 36.028 s |
| baseline UCC | timeout | - | - | > 120 s |
| optimized UCC | 3,848,810 | 3,269,433 | 1,546,096 | 58.424 s |

### 3.4 `MQT Bench` 总论

- 在 `mqt_qpeexact_32` 和 `mqt_qaoa_32` 上，optimized UCC 与 `qiskit opt3` 输出质量追平，并显著优于 baseline UCC。
- 在 `mqt_grover_20` 上，optimized UCC 也达到 `qiskit opt3` 质量，但 runtime 仍更慢。
- 这组结果说明：当前方法并不局限于官方 Qiskit library 样例，在外部公共 benchmark source 上仍成立。

## 4. 公共 benchmark source 2：SupermarQ

实例：

- `supermarq_hamiltonian_sim_8`
- `supermarq_mermin_bell_8`
- `supermarq_qaoa_vanilla_12`

### 4.1 代表性结论

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

### 4.2 `SupermarQ` 总论

- 这组结果继续支持“anti-regression / quality-recovery layer”的主张。
- 但也暴露边界：当前方法并不是每个 family 都优于强 Qiskit baseline。
- 因此目前最稳的论文口径不是“全面超过 Qiskit”，而是“在多组真实和公共 benchmark 上显著修复 baseline UCC 的退化，并在部分 case 上取得更强结果”。

## 5. Hardware-aware 结果

固定后端：

- 20-qubit bidirectional line backend
- native operations: `u`, `sx`, `p`, `cx`, `measure`, `id`

实例：

- `hw_mqt_qpeexact_20`
- `hw_mqt_qaoa_20`
- `hw_mqt_grover_20`

### 5.1 `hw_mqt_qpeexact_20`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| qiskit opt3 | 1,572 | 407 | 812 | 0.044 s |
| baseline UCC | 2,047 | 632 | 1,235 | 0.112 s |
| optimized UCC | 1,563 | 405 | 804 | 1.104 s |

结论：

- optimized UCC 现在在 **总门数、深度、CX 数** 三项上都优于固定 seed 的 `qiskit opt3`。
- 这说明 `hw_mqt_qpeexact_20` 已从“lower-`cx` tradeoff”升级为一个 clean routed-quality win。
- 代价是 runtime 上升到 `1.104 s`。

### 5.2 `hw_mqt_qaoa_20`

| Method | Output Gates | Output Depth | CX Count | Runtime |
|---|---:|---:|---:|---:|
| qiskit opt3 | 2,091 | 532 | 1,530 | 0.049 s |
| baseline UCC | 2,091 | 485 | 1,417 | 0.096 s |
| optimized UCC | 2,050 | 487 | 1,458 | 1.012 s |

结论：

- optimized UCC 在 **总门数、深度、CX 数** 三项上都优于 `qiskit opt3`。
- 这是当前最明确的 hardware-aware external-baseline win。
- 相比 baseline UCC，optimized UCC 在总门数和 CX 数上也更好，但 depth 略高（`487` vs `485`）。
- 当前代码冻结版本里，runtime 为 `1.012 s`。

### 5.3 `hw_mqt_grover_20`

- `qiskit opt3` 与 baseline UCC 仍然在当前 timeout 设置下超时。
- optimized UCC 现在可以在 `38.925 s` 内返回结果。
- 但该结果电路极大，因此它更适合作为“robustness / timeout recovery”证据，而不是主质量对比图。

### 5.4 Hardware-aware 总论

当前 hardware-aware 结果表明：

- 我们的工作不只是“追平 Qiskit 输出质量”；
- 至少在两个公开 hardware-aware case 上，已经取得固定-seed 的明确胜场；
- 并且在 `hw_mqt_grover_20` 上，optimized UCC 还修复了原先的 timeout 问题；
- 这使得当前工作从“只修 UCC 退化”进一步提升到“在部分 routed case 上可超过 `qiskit opt3`，并在更难 case 上提供 robustness”。

## 6. Runtime 结论

runtime profiling 的主结论如下：

### 6.1 all-to-all 路径

对于：

- `phase_estimation_real`
- `grover_real`
- `qaoa_real`

当前 optimized 分支的 runtime 已经与 `qiskit opt3` 接近。主要原因是：

- qiskit-source direct fast path
- source-level short-circuiting

已经把早期分支中的额外 wrapper overhead 明显压掉。

### 6.2 backend-aware 路径

backend-aware 剩余 runtime gap 主要来自：

- backend candidate search
- direct backend reference probe
- seed portfolio

当前又做了一轮 pruning：

- 当 base backend-aware candidate 只比 cheap baseline 小幅更优时，直接返回，不再额外跑 direct backend `qiskit opt3`。
- 当 direct backend `qiskit opt3` 已明显支配 base candidate 时，直接返回它，不再扩 seed portfolio。
- 当 canonical direct reference 和 base candidate 不能分出胜负时，再扩小型 exploratory seed set。
- 对 `hw_mqt_grover_20` 这类 dominant repeated composite-run，增加 repeated-run backend fallback。

结果：

- `hw_mqt_qpeexact_20`：质量从 lower-`cx` tradeoff 提升为 clean routed-quality win，当前 runtime `1.104 s`
- `hw_mqt_qaoa_20`：quality win 保持，当前 runtime `1.012 s`
- `hw_mqt_grover_20`：optimized UCC 不再 timeout，当前 runtime `38.925 s`

## 7. 当前最稳的实验结论

当前最稳的、最适合对外表述的结论是：

1. baseline UCC 的结构化退化是真实存在的。
2. 这种退化不能仅用“简单 UCCDefaults 顺序修复”完全解释。
3. 在官方真实实例上，optimized UCC 已能稳定追平 `qiskit opt3` 的输出质量。
4. 在两个公共 benchmark source（`MQT Bench`、`SupermarQ`）上，optimized UCC 继续表现为有效的 anti-regression / quality-recovery layer。
5. 在至少一个 hardware-aware 公共 benchmark（`hw_mqt_qaoa_20`）上，optimized UCC 取得了相对于 `qiskit opt3` 的明确 external-baseline win。
6. runtime 方面，all-to-all 已接近 `qiskit opt3`，backend-aware 路径也经过剪枝显著缩小了差距。

## 8. 对论文和立项的含义

### 对论文

这组结果支持把论文写成：

- UCC default pipeline redesign / bounded structural preprocessing study
- anti-regression and quality-recovery for structured quantum circuits
- with at least one hardware-aware external-baseline win

这比“玩具结构消除例子”或“只改 pass 顺序”的故事更强。

### 对 grant / 立项

这组结果也足以支持把项目立成：

- 默认流程重设计
- bounded pre-basis structural preprocessing
- anti-regression benchmark / artifact project

而不是“一个全新独立 pass”的狭义提案。

## 9. 当前工作区推荐查看顺序

如果要快速理解整篇工作，建议按这个顺序看：

1. `quantum_paper_draft.md`
2. `experiment_results_overview_cn.md`（本文档）
3. `real_instance_results_summary.md`
4. `hardware_aware_results_summary.md`
5. `runtime_optimization_progress.md`

如果只看一句结论：

> 当前 optimized UCC 已经在多组真实和公共 benchmark 上把 baseline UCC 的严重退化拉回到接近 `qiskit opt3` 的质量水平，并在 `hw_mqt_qaoa_20` 上取得了明确的 hardware-aware external-baseline win。
