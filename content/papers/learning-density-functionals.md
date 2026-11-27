---
title: "Snyder et al.: accurate energies, troublesome derivatives"
date: 2026-11-27
tags: [paper, machine-learning, orbital-free]
---

**Paper:** Snyder, Rupp, Hansen, Müller and Burke, *Finding Density Functionals with Machine Learning* (2012). [DOI](https://doi.org/10.1103/PhysRevLett.108.253002) · [full text](https://www.mrupp.info/Data/2012srhmb_prl.pdf).

## TL;DR

Learning a density-to-energy map can work remarkably well on familiar densities. Finding the ground-state density with that map is a harder task. This early demonstration makes the derivative problem impossible to ignore.

## The problem

Kohn–Sham orbitals make the noninteracting kinetic energy calculable, but solving for them costs time. If we had a sufficiently accurate density-only approximation to $T_s[n]$, we could seek the density without an orbital solver. This is an orbital-free motivation: the target here is **kinetic energy**, not XC.

The authors study a controlled one-dimensional system of noninteracting fermions in a family of external potentials. That restriction permits accurate reference densities and kinetic energies. It is not a universal three-dimensional molecular functional.

## The key idea

Represent each density by its values on a grid and use kernel ridge regression. A simplified notation for the predictor is

$$T^{\mathrm{ML}}[n]=\sum_{j=1}^{M}\alpha_j k(n,n_j),\qquad
k(n,n_j)=\exp\!\left[-\frac{\|n-n_j\|^2}{2\sigma^2}\right].$$

$n_j$ are training densities. The kernel measures similarity between densities; $\sigma$ controls how rapidly that similarity decays. The fitted weights $\alpha_j$ combine the influence of the examples. A regularization term discourages unstable fitting.

This is a model of a **functional** because its input is the entire sampled density, even though the implementation ultimately operates on a finite vector. It does not learn just the value of the density at one spatial point.

## How it works

For training targets $\mathbf t$, the usual ridge solution has the structure

$$\boldsymbol\alpha=(K+\lambda I)^{-1}\mathbf t,$$

where $K_{ij}=k(n_i,n_j)$ and $\lambda$ controls regularization. Numerically, one solves the linear system rather than explicitly forming an inverse.

Predicting $T_s$ on a held-out reference density is straightforward. To find the density itself, however, we must minimize the total energy at fixed electron number. The Euler equation contains

$$\frac{\delta T_s}{\delta n(x)}+v(x)=\mu.$$

The derivative must be sensible in directions taken by the optimization. Training densities occupy a thin, structured region of the enormous space of all grid vectors. Good interpolation of values on that region does not constrain every derivative away from it.

![[energy-and-derivative.png]]

*Original toy illustration: adding $0.01\sin(100x)$ barely changes a value but changes its derivative by up to one. This is not a reproduction of the paper's data.*

The authors use local principal-component information to project the search into directions supported by nearby training densities. Intuitively, the data suggest which coordinated changes in the grid values resemble physically encountered densities. Restricting the derivative/search to those directions avoids trusting every direction in the ambient grid space equally.

## Results that matter

For the model problem, errors below one kcal/mol on test densities similar to training densities are achieved with fewer than 100 training densities. The paper also demonstrates accurate self-consistent densities using projected derivatives and an indicator of interpolation reliability.

Both qualifications matter: this is a restricted one-dimensional family, and the successful density search requires more care than differentiating a good energy predictor and hoping for the best.

## Limitations

Nearest training examples and a local low-dimensional structure are helpful only where relevant data exist. A good interpolation detector is not a proof of general chemical transferability. Nor does accurate kinetic energy on these examples resolve the orbital-free problem for molecules, metals and surfaces.

## My take

This is the cleanest early warning against evaluating a learned functional only as a regression model. [[papers/kohn-sham-regularizer|The Kohn–Sham regularizer]] later puts the solver inside training. [[papers/bypassing-kohn-sham|Brockherde et al.]] explore a different route: learn the potential-to-density map and avoid the difficult minimization step.

> [!todo] Things to check
> - Distinguish errors on supplied densities from errors after minimizing the learned energy.
> - Identify which density variations the local projection retains and which it discards.
