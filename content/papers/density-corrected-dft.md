---
title: "Density-corrected DFT: which mistake are we trying to fix?"
date: 2026-11-27
tags: [paper, dft, density]
---

**Paper:** Kim, Sim and Burke, *Understanding and Reducing Errors in Density Functional Calculations* (2013). [DOI](https://doi.org/10.1103/PhysRevLett.111.073003) · [author-hosted full text](https://dft.uci.edu/pubs/KSB13.pdf).

## TL;DR

A DFT energy can be wrong because the approximate functional is wrong on a good density, or because self-consistency supplies it with a poor density. Separating those contributions changes both the diagnosis and the possible remedy.

## The problem

Suppose PBE gives a poor reaction energy. It is natural to conclude that its energy formula needs improvement. But the formula also generated the density used in the calculation. Changing the density while retaining the functional can sometimes make a large difference.

This matters for learned functionals too. A model can look excellent on reference densities yet perform poorly when it must find its own density. Conversely, a promising energy formula can be judged too harshly because of a particularly troublesome self-consistent density.

## The key idea

Let $E$ be the exact energy functional, $n$ its minimizing density, $\widetilde E$ an approximation and $\widetilde n$ its minimizing density. Add and subtract the same quantity, $\widetilde E[n]$:

$$\underbrace{\widetilde E[\widetilde n]-E[n]}_{\Delta E}
=\underbrace{\widetilde E[n]-E[n]}_{\Delta E_F}
+\underbrace{\widetilde E[\widetilde n]-\widetilde E[n]}_{\Delta E_D}.$$

The first term tests the approximate formula on the exact density. The second measures the energy change caused by using the approximate density instead. This is an algebraic identity, not a new functional.

For a strictly variational minimization over the same admissible densities, the second term is nonpositive because $\widetilde n$ minimizes $\widetilde E$. That does not mean the total error improves: the two error contributions can cancel or reinforce in magnitude. Practical constrained, orbital-based and non-self-consistent evaluations need care when applying this idealized picture.

## How it works

Most ordinary Kohn–Sham calculations in the paper's discussion are “normal”: functional error dominates. In “abnormal” cases, the density contribution becomes large. These words classify a calculation, not a molecule forever or a functional in every use.

The response of the density helps explain why. Schematically,

$$\delta n(\mathbf r)=\int\chi_s(\mathbf r,\mathbf r')\delta v_s(\mathbf r'),d\mathbf r'.$$

$\chi_s$ is the noninteracting density response. Its orbital expression contains energy differences in denominators. A small gap can therefore make the density unusually sensitive to an error in the potential. A small gap is a warning sign, not a sufficient universal diagnosis: matrix elements, symmetry and the structure of the perturbation also matter.

An exact density is usually unavailable. The practical move is sometimes to evaluate the approximate DFT energy on Hartree–Fock orbitals/density. That can correct a serious density problem without replacing the XC formula. This procedure is often called HF-DFT.

## Results that matter

The paper examines two-electron ions, stretched NaCl and reaction barriers. In its two-electron example, lowering nuclear charge makes a semilocal calculation lose part of the second electron. The energy evaluated on an accurate density behaves much better, exposing the origin of the large error.

For the symmetric hydrogen-transfer barrier discussed in the paper, a reference value of $0.43$ eV is compared with $0.16$ eV from PBE and $0.25$ eV from HF-PBE. The density change improves the result but does **not** make it exact. That is a particularly useful example because it prevents the story from turning into “use HF densities and everything is solved.”

## Limitations

Hartree–Fock densities are not uniformly better. Spin contamination and strong correlation can make them poor choices. Even a perfect density leaves the functional error. Non-self-consistent energies also require appropriate derivative treatment before being used for forces or geometry optimization.

“Density error” is not a single observable. A small error under one spatial norm need not imply a small error in a dipole or another density-sensitive property. The useful question is which error matters for the intended prediction.

## My take

This is a diagnostic paper worth reading before trying to optimize an XC model. It teaches us to test both the energy map and the density produced by the solver. That naturally connects to [[papers/kohn-sham-regularizer|training through self-consistency]] and the [[learnings/frontier-2026|2026 work on derivative supervision]].

> [!todo] Things to check
> - Reproduce the error decomposition by adding and subtracting $\widetilde E[n]$.
> - For any claimed HF-DFT improvement, check spin quality, the reference density and whether forces are treated consistently.
