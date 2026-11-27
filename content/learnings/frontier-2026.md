---
title: "The 2026 frontier: better derivatives, broader chemistry, different representations"
date: 2026-11-27
tags: [learning, frontier, machine-learning]
---

**Literature checkpoint: 27 November 2026.** This is a selective view of consequential directions, not a claim to list every paper published this year. Recent preprints are treated as emerging evidence, not already established breakthroughs.

## What happens around the minimum?

Eberhard et al., [*Derivative Informed Learning of Exchange-Correlation Functionals*](https://proceedings.mlr.press/v306/eberhard26a.html), ICML 2026, study a precise target: distilling **B3LYP/def2-SVP**, rather than learning exact or coupled-cluster chemistry.

Their loss supervises first and second energy derivatives on the Grassmannian of admissible density matrices. Informally, the Grassmannian describes occupied orbital subspaces: rotating orbitals within an occupied subspace does not create a new physical occupied space. The derivative information describes how the energy changes along allowed electronic variations, beyond its value at a minimum.

Across four architectures, the paper reports a 66% average relative reduction in total-energy MAE over energy-and-density supervision alone. Dipole and density-norm errors do not improve uniformly. Improved initial densities also reduce the iterations needed for subsequent hybrid calculations in the reported tests.

The conceptual advance is the training objective: learn local response as well as a fixed point. It extends the derivative lesson from [[papers/learning-density-functionals|Snyder]] and [[papers/kohn-sham-regularizer|solver-aware training]]. Its reference level limits what “accuracy” means here; reproducing B3LYP more faithfully is not the same as surpassing it against exact chemistry.

## Can molecules, solids and surfaces share a useful approximation?

Abdallah et al., [*Machine-learned exchange-correlation functionals for molecules, solids, and reactive surfaces*](https://arxiv.org/abs/2608.21525v2), introduce CIDER26SS. The preprint was posted in August and revised on 29 October 2026.

This continues [[papers/cider-molecules-and-solids|the CIDER programme]] toward combined XC modelling and heterogeneous catalysis. The difficult example is CO adsorption on Pt(111): predicting an adsorption site is not enough if adsorption energy, bulk lattice constant and surface energy are inconsistent.

The authors report a balanced improvement on those properties and a test excluding Pt bulk and surface data from training. That exclusion is valuable evidence about transfer, while remaining a particular experiment rather than a proof across all transition metals and adsorbates.

For our investigation, the important question is **consistency across environments**. A molecular leaderboard cannot answer it alone. This is a recent preprint; independent replication and wider application will determine how durable the result is.

## Should we represent the density matrix more directly?

Kulaev et al., [*ROSE: Deep Learning exchange-correlation functional from reduced density-matrix representations*](https://arxiv.org/abs/2611.00826v1), was posted on 31 October 2026.

ROSE builds a learned XC model from the occupied-state density matrix. Its motivation connects to exact exchange: two-point orbital information is more directly expressed by a density matrix than by a finite set of local density derivatives. This is a representational advantage, not a contradiction of the ground-state density theorems.

The authors report competitive molecular benchmark results and comparisons with neural functionals trained under matched protocols. That matched-training comparison helps separate representation effects from differences in data, although the entire evaluation protocol still matters.

The result is recent and preliminary. The useful reading question is whether the representation captures relevant nonlocal physics efficiently and remains stable when used self-consistently—not whether its newest headline number settles the field.

## A more useful comparison than “which network won?”

| Direction | What changes? | What would strengthen the evidence? |
|---|---|---|
| Derivative supervision | Information in the training objective | Wider references and reliable response properties |
| CIDER26SS | Chemical environments covered together | Independent surface and materials evaluations |
| ROSE | Electronic representation | Reproducible full-workflow cost and transfer tests |

The revised [[papers/skala|Skala paper]] belongs in this 2026 view too, even though its first version appeared in 2025. It illustrates why versioned papers and model releases must be cited explicitly. A claim made about one release should not quietly migrate to another.

> [!todo] Things to check
> - Revisit publication status and model versions before treating these as settled reference methods.
> - Check whether each claimed advance concerns representation, training supervision, data coverage or implementation.
