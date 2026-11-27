---
title: Figure sources and what the visuals mean
date: 2026-11-27
tags: [sources, figures]
---

Original illustrations and reproduced paper figures serve different purposes. Schematics explain an idea; only identified research plots contain reported scientific results. No original diagram on this site should be mistaken for a new DFT calculation.

## Reproduced figures

The copyright and license statements were checked in the full published articles. Each of these articles licenses its included images under **Creative Commons Attribution 4.0**, except where a separate credit says otherwise. No separate restrictive credit was found for the figures below. Each crop retains the complete selected figure, including panel labels and axes where present; article text and the original caption are omitted. Captions on this site credit the authors and link the source and [license](https://creativecommons.org/licenses/by/4.0/).

| Asset | Original figure | Where it is explained |
|---|---|---|
| `neuralxc-architecture.png` | Dick & Fernandez-Serra (2020), Figure 1, article p. 3, [DOI](https://doi.org/10.1038/s41467-020-17265-7) | [[papers/neuralxc|NeuralXC]] |
| `bypassing-kohn-sham.png` | Brockherde et al. (2017), Figure 1, article p. 2, [DOI](https://doi.org/10.1038/s41467-017-00839-3) | [[papers/bypassing-kohn-sham|Bypassing Kohn–Sham]] |
| `nagai-network.png` | Nagai, Akashi & Sugino (2020), Figure 1, article p. 2, [DOI](https://doi.org/10.1038/s41524-020-0310-0) | [[learnings/architectures-without-mystery|Architecture guide]] |

## Original visuals

The reaction landscape, self-consistency loop, ingredient map and scaling curves are explanatory schematics. The derivative plot and fractional-charge plot use explicit toy functions. The PBE enhancement plot evaluates the published exchange formula, not benchmark observations. Their reproducible plotting source is `site/illustrations.py` in the [Curiosophy repository](https://github.com/Iammohithhh/Curiosophy).

The Mermaid architecture diagrams are original summaries of the cited methods. The interactive laboratory uses toy formulas whose purpose and limits are stated beside the controls. It runs entirely in the browser and does not perform an electronic-structure calculation.

The numerical table on the Skala page transcribes identified values from Table 1 of arXiv v6. Those values are reported by the paper's authors, not reproduced experimentally here.

> [!todo] Things to check
> - Preserve captions and credits if a figure is reused elsewhere.
> - Keep measured results, formula plots and conceptual schematics visibly distinguished.
