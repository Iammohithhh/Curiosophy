---
title: "SCAN: a better local description of the electronic environment"
date: 2026-11-27
tags: [paper, dft, meta-gga]
---

**Paper:** Sun, Ruzsinszky and Perdew, *Strongly Constrained and Appropriately Normed Semilocal Density Functional* (2015). [DOI](https://doi.org/10.1103/PhysRevLett.115.036402) · [full text and supplement](https://arxiv.org/abs/1504.03028).

## TL;DR

SCAN adds orbital kinetic-energy information to a semilocal functional, uses it to distinguish electronic environments, and imposes 17 known exact constraints applicable at the meta-GGA level. It asks how much accuracy is available before paying for explicit nonlocal exchange.

## The problem

Density and gradient do not fully describe an electronic environment. A covalent bond, a metallic region and overlapping tails from weakly bound fragments can require different treatment. A GGA must handle those differences through a restricted set of ingredients.

Adding parameters to the same inputs cannot distinguish situations those inputs make identical. SCAN adds an ingredient that carries information from the orbitals already present in a Kohn–Sham calculation.

## The key idea

The positive orbital kinetic-energy density is

$$\tau(\mathbf r)=\frac12\sum_i f_i|\nabla\phi_i(\mathbf r)|^2.$$

$f_i$ is the occupation of orbital $i$. Integrating $\tau$ gives the noninteracting kinetic energy in the usual setting. This quantity is not the full interacting kinetic-energy density.

Compare it with two reference expressions:

$$\tau_W=\frac{|\nabla n|^2}{8n},\qquad
\tau_{\mathrm{unif}}=\frac3{10}(3\pi^2)^{2/3}n^{5/3}.$$

$\tau_W$ is the von Weizsäcker expression. For a region described by a single real spatial orbital, it matches $\tau$. The second expression is the spin-unpolarized uniform-gas value. SCAN uses their dimensionless combination

$$\alpha=\frac{\tau-\tau_W}{\tau_{\mathrm{unif}}}.$$

Now the local environment comes with a useful diagnostic. Single-orbital regions give $\alpha=0$. A uniform gas gives $\alpha=1$. Weakly overlapping closed-shell regions can give large $\alpha$. These are informative limiting behaviours, not a perfect classifier that labels every bond from one number.

## How it works

The functional interpolates and extrapolates between forms appropriate to different $\alpha$ regimes, while keeping exchange and correlation consistent with selected exact properties. Think of $\alpha$ as a coordinate along which the approximation can change its behaviour.

The “strongly constrained” part refers to all 17 constraints then known that could be satisfied by a meta-GGA. These include requirements associated with scaling, spin and limiting densities. It does not mean SCAN satisfies every property of the exact universal functional. Some exact behaviours cannot be represented by any semilocal form.

The “appropriately normed” part matters just as much. Remaining choices are guided by systems where semilocal approximations are expected to work well, including rare-gas atoms and suitable nonbonded interactions. A norm here is a reference used to calibrate behaviour; it is not a vector norm or an assertion of universality.

This is a richer form than PBE, but it remains inexpensive relative to conventional hybrids because it avoids evaluating an explicit two-point exact-exchange integral. Since $\tau$ depends on orbitals, implementations commonly use a generalized Kohn–Sham operator rather than treating the entire expression as an elementary density-only local potential.

## Results that matter

The paper reports strong performance across diverse tests, particularly lattice constants and weak interactions, and relates that success to systems with localized exchange–correlation holes. Its useful demonstration is that improving local environment recognition can yield substantial gains without adding exact exchange.

Read the molecular, solid-state and nonbonded tests separately. Success on an equilibrium lattice constant does not establish the same accuracy for a reaction barrier. A broad evaluation is more informative than a single overall ranking, but still finite.

## Limitations

SCAN can describe important intermediate-range weak interactions without reproducing the exact long-distance dispersion tail between separated fragments. “Good for weak interactions” and “contains complete long-range dispersion” are different statements.

Numerical sensitivity is another lesson. A formally attractive expression can require careful integration grids and derivatives. Later regularized SCAN variants address practical smoothness and numerical behaviour; they should not be silently substituted when reproducing results for the original SCAN.

Semilocal information also leaves fundamental problems with fractional charge and strongly correlated regimes. The 17 constraints are a carefully chosen foundation, not a guarantee against those failures.

## My take

Before reading a neural architecture, understand $\alpha$. It shows exactly why a descriptor can matter more than a larger fitting function. [[papers/cider|CIDER]] extends this discussion to nonlocal descriptors; [[papers/skala|Skala]] goes further toward learning the representation itself.

> [!todo] Things to check
> - Substitute a single real orbital into $n$, $\tau$ and $\tau_W$ to verify $\alpha=0$.
> - Separate original SCAN results from results for regularized variants or added dispersion corrections.
