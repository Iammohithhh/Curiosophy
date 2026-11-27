---
title: Speed–Accuracy Challenge
date: 2026-11-27
tags:
  - dft
  - exchange-correlation
  - quantum-chemistry
---

## Documenting learnings on my journey to solve (or attempt to solve) this challenge

[Discovered Materials, Grand Challenge 03](https://discoveredmaterials.com/grand-challenges/speed-accuracy-barrier/): *Breaking the Speed–Accuracy Barrier in Quantum Chemistry*.

## The problem

> *"Develop a more accurate exchange-correlation functional that improves DFT predictions without sacrificing computational efficiency."*

Density functional theory (DFT) is the workhorse of computational chemistry because it's cheap.
Its accuracy depends entirely on one approximated piece, the **exchange-correlation (XC) functional**.
Cheap functionals often get reaction chemistry wrong (energies, barriers, bond breaking).
Coupled-cluster theory, CCSD(T), gets it right but costs far too much to use at scale.

The challenge: **coupled-cluster-like accuracy at roughly the cost of ordinary DFT.**
It was written with input from Stefan Grimme (University of Bonn).

## What a submission needs
- **Method:** the approach and the science behind it.
- **Implementation:** working code someone else can run.
- **Results:** accuracy and cost on the public GMTKN55 benchmark.

## How it's scored
- **Accuracy:** error (WTMAD-2, in kcal/mol) on a **hidden** test set of reaction energies, activation barriers, binding energies and bond dissociation energies "representative of atomic layer deposition (ALD) and chemical vapor deposition (CVD) precursor chemistry".
  The reference values are CCSD(T) extrapolated to the complete basis set limit.
- **Speed:** time per molecule with the def2-QZVP basis, on one CPU core and separately on one A100 GPU (median of 3 runs).
- **Reproducibility:** enough documentation for someone else to verify the results.

The challenge's plot sorts methods by cost (**≤ 2× PBE**, 2–5×, > 5×) and by error (**< 1 kcal/mol**, which is chemical accuracy; 1–3; > 3).
The goal is the empty corner: about PBE cost with an error near 1 kcal/mol.

## Where things stand (provisional leaderboard, Nov 2026)

| Functional | Error (kcal/mol) | CPU s/molecule | A100 s/molecule |
|---|---|---|---|
| LDA | 26.35 | 2.4 | 1.33 |
| PBE | 12.47 | 3.0 | 1.47 |
| B3LYP | 16.16 | 4.0 | 1.50 |
| PBE0 | 8.37 | 3.9 | 1.41 |
| HSE06 | 8.29 | 12.2 | 1.94 |
| ωB97M-V | **3.81** | 43.5 | 3.94 |

The best functional listed, ωB97M-V, is still about 4× off chemical accuracy and about 14× slower than PBE on a CPU.
r²SCAN and Skala (a deep-learned functional from Microsoft) are still being evaluated.

## What I want to understand first
- What exactly *is* exchange-correlation, and why is it the only thing we approximate?
- Why has more accuracy always cost more compute?
- What do the hidden-set molecules (ALD/CVD precursors) look like, and are they harder than GMTKN55?
- How does Skala get its accuracy, and what does it cost?

> [!todo] Things to check
> - Leaderboard numbers are from the challenge page and marked "provisional". Recheck them before relying on them.
> - The prize amount, deadline and training-data rules aren't stated on the challenge page.

## References
- [Challenge page](https://discoveredmaterials.com/grand-challenges/speed-accuracy-barrier/)
- Goerigk et al., *Phys. Chem. Chem. Phys.* 19, 32184 (2017): GMTKN55 and WTMAD-2. [doi:10.1039/C7CP04913G](https://doi.org/10.1039/C7CP04913G)
- *Accurate and scalable exchange-correlation with deep learning* (Skala), Microsoft Research AI for Science. [arXiv:2506.14665](https://arxiv.org/abs/2506.14665)
