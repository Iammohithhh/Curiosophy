---
title: "CIDER in molecules and solids: replacing an expensive ingredient"
date: 2026-11-27
tags: [paper, machine-learning, solids]
---

**Paper:** Bystrom and Kozinsky, *Nonlocal Machine-Learned Exchange Functional for Molecules and Solids* (2024). [DOI](https://doi.org/10.1103/PhysRevB.110.075130) · [full text](https://arxiv.org/abs/2303.00682).

## TL;DR

This work turns the CIDER approach toward a practical objective: replace the expensive exact-exchange contribution in hybrid-like calculations with an efficient learned exchange model, while retaining useful molecular and solid-state accuracy.

## The problem

Hybrids can improve both molecular energetics and electronic properties of solids, but exact exchange is particularly costly in many plane-wave calculations. Large defect supercells make the trade-off concrete: a more accurate treatment may become too expensive at the cell sizes needed to reduce finite-size errors.

The [[papers/cider|original CIDER paper]] supplied constrained nonlocal descriptors. The next question is whether such descriptors can support accurate and efficient self-consistent calculations across more than one class of system.

## The key idea

Treat orbital dependence and nonlocality as two separate sources of information. A meta-GGA ingredient can depend on occupied orbitals without being an explicit two-point exchange integral. A nonlocal density descriptor can communicate across space without evaluating conventional exact exchange. The paper examines the contribution of both.

This matters because “contains orbitals” is not a sufficient description of cost. Kohn–Sham DFT already has occupied orbitals. The expensive operation is what we ask the algorithm to do with them.

## How it works

The model learns an exchange approximation from physically constrained descriptors and substitutes it into functional combinations that otherwise use exact exchange. In schematic global-hybrid notation, the substitution is

$$aE_x^{\mathrm{exact}}+(1-a)E_x^{\mathrm{semilocal}}+E_c
\quad\longrightarrow\quad
aE_x^{\mathrm{learned}}+(1-a)E_x^{\mathrm{semilocal}}+E_c.$$

This equation explains the role of the learned ingredient; it is not a claim that every tested functional uses one identical formula or mixing fraction.

Efficient evaluation of nonlocal descriptors is central. Naively considering every pair of grid points could erase the speed advantage. The numerical representation and implementation therefore matter alongside the regression error. The paper develops the model for both molecular and periodic calculations and evaluates performance in those settings.

Orbital dependence also changes how the functional contributes to the generalized Kohn–Sham equations. An improvement in a calculated eigenvalue gap is consequently not equivalent to proving that a purely local multiplicative potential has recovered every aspect of the exact derivative discontinuity.

## Results that matter

The authors report hybrid-like accuracy on the molecular thermochemical benchmarks considered, improved band-gap predictions over semilocal methods, and charged-defect transition levels in silicon supercells. The latter demonstration ties improved electronic structure to a concrete materials calculation.

These are three distinct pieces of evidence: molecular energy differences, bulk electronic gaps and defect energetics. Read them separately. A method can perform well in one without guaranteeing the others, so testing all three is more informative than announcing one broad “accuracy” number.

The cost claim is especially relevant to plane-wave implementations, where the work reports substantial savings relative to conventional hybrid DFT. It should not be converted into one universal speedup for every basis, code, machine or system size.

## Limitations

Learning exchange does not remove all correlation errors. The paired correlation, mixing strategy, reference data and available descriptors still constrain the result. Band gaps also have multiple definitions: a generalized Kohn–Sham eigenvalue gap, a total-energy fundamental gap and an optical excitation energy should not be interchanged.

The work points toward more accurate inexpensive XC functionals. “Post-hybrid accuracy at semilocal cost” is a research direction, not a demonstrated guarantee across all chemistry.

## My take

This paper earns its place because it connects representation design with a practical computational bottleneck. It also widens the investigation beyond molecular leaderboards. The [[learnings/frontier-2026|2026 CIDER surface work]] asks whether the same broad strategy can handle molecules, bulk solids and adsorption consistently.

> [!todo] Things to check
> - Identify the precise correlation partner and exchange fraction for each reported result.
> - For every timing comparison, record the basis representation, cell size and measured part of the calculation.
