---
title: "PBE: build the approximation around what cannot be wrong"
date: 2026-11-27
tags: [paper, dft, constraints]
---

**Paper:** Perdew, Burke and Ernzerhof, *Generalized Gradient Approximation Made Simple* (1996). [DOI](https://doi.org/10.1103/PhysRevLett.77.3865) · [author-hosted full text](https://dft.uci.edu/pubs/PBE96.pdf).

## TL;DR

PBE is a compact example of a powerful design strategy: choose an inexpensive functional form, then use known properties of the exact theory to restrict its behaviour. The interest here is not that PBE is the most accurate molecular functional. It is that we can understand why its formula has the shape it does—and carry that reasoning into machine learning.

## The problem

The uniform electron gas gives a natural local approximation. At each point in a molecule, pretend the surrounding electrons form a uniform gas at that point's density. But a bond and an atomic tail contain spatial variation that this replacement ignores.

A GGA adds the gradient. That sounds simple until we ask which function of the density and gradient to use. An unrestricted fit can improve selected molecules while behaving badly elsewhere. PBE asks how far exact conditions can guide the choice without fitting molecular reference energies.

## The key idea

Start with exchange. For an unpolarized density, write

$$E_x^{\mathrm{PBE}}=\int n(\mathbf r)\varepsilon_x^{\mathrm{unif}}(n)F_x(s)\,d\mathbf r.$$

The uniform-gas exchange energy per electron is negative and proportional to $n^{1/3}$. The **enhancement factor** $F_x$ changes its magnitude according to how quickly the density varies. PBE uses the dimensionless reduced gradient

$$s=\frac{|\nabla n|}{2k_Fn},\qquad k_F=(3\pi^2n)^{1/3}.$$

$|\nabla n|/n$ measures relative variation per unit length. Dividing by $k_F$, an inverse length set by the local density, compares that variation with an electronic length scale. A gradient measured in arbitrary units would not provide the same physical comparison across densities.

## How it works

PBE's exchange enhancement is

$$F_x(s)=1+\kappa-\frac{\kappa}{1+\mu s^2/\kappa},\qquad \kappa=0.804,\quad\mu\approx0.21951.$$

![[pbe-enhancement.png]]

*Original plot of the published exchange formula; not benchmark data.*

Three quick calculations reveal the design.

At $s=0$, $F_x=1$: the uniform-density limit returns uniform-gas exchange. For small $s$, expanding $1/(1+x)\approx1-x$ gives $F_x\approx1+\mu s^2$. For very large $s$, the factor approaches $1+\kappa=1.804$ rather than growing without bound.

The cap is a sufficient local construction used to satisfy the relevant exchange bound with spin scaling; it is not a claim that the exact exchange energy density must satisfy that pointwise cap in every possible gauge. Energy densities are less uniquely defined than their integrals.

The coefficient $\mu$ is chosen in relation to the correlation gradient coefficient to recover the desired linear response of the uniform gas. It is **not** simply the exact second-order slowly varying exchange coefficient. This is an early lesson in functional design: desirable conditions can compete within a restricted form.

Correlation receives its own gradient correction. It recovers the uniform limit, has the appropriate high-density behaviour and is constructed to switch off the local correlation contribution in the rapidly varying limit. The full functional is more than the single exchange curve above. Spin dependence is also essential for open-shell systems.

## Results that matter

The paper demonstrates a simple GGA with selected exact constraints, proper limiting behaviour and useful tests on atoms and molecules. Its lasting contribution is a reusable, inexpensive construction. The plotted enhancement factor explains a piece of that construction; it does not establish that PBE will predict a particular reaction barrier accurately.

Read the paper with two separate questions: which properties follow from the formula, and which are only supported by the numerical examples? This distinction becomes even more important when a learned functional has thousands of parameters.

## Limitations

PBE is semilocal. It cannot in general reconstruct distant electronic arrangements from $n$ and $\nabla n$ at one point. Fractional-charge errors, some reaction barriers and asymptotic dispersion remain serious issues. Constraint satisfaction restricts mistakes but cannot compensate for every limitation in the input information.

“Nonempirical” also does not mean “exact.” It describes how parameters and forms are chosen. An approximation constructed without molecular fitting can still have sizeable molecular errors.

## My take

The most useful exercise is to reproduce the three limits of $F_x$. Once those make sense, “put physics into a network” becomes a concrete question: is the condition built into the output transformation, encoded in descriptors, or merely encouraged by examples?

Next, [[papers/scan|SCAN]] asks what a semilocal model can do with one more informative ingredient. [[papers/cider|CIDER]] later combines physical constraints with learned, nonlocal exchange descriptors.

> [!todo] Things to check
> - Derive the small-$s$ expansion and distinguish its coefficient from the exact slowly varying exchange coefficient.
> - Read PBE's correlation construction alongside exchange before treating the plotted curve as the whole functional.
