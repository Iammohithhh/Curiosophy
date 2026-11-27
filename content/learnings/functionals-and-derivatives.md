---
title: What is a functional, and why do its derivatives matter?
date: 2026-11-27
tags:
  - mathematics
  - dft
description: From a function of a few numbers to an energy functional, a local potential and a self-consistent calculation.
---

The word *functional* looks like an unnecessary complication until we ask what goes into the calculation.

A function such as $f(x)=x^2$ accepts a number and returns a number. The density $n(\mathbf r)$ is already a function: give it a position and it returns an electron number per unit volume. An energy functional accepts that entire density function and returns one energy.

$$
n(\mathbf r)\quad\longmapsto\quad E[n].
$$

The square brackets remind us what the input is. They are not a new arithmetic operation.

## Begin with a finite list

Imagine recording the density at three points, giving a vector $\mathbf n=(n_1,n_2,n_3)$. A deliberately simple discretized energy is

$$
E(\mathbf n)=\sum_{i=1}^{3}w_i A n_i^2.
$$

$w_i$ represents the volume associated with sample $i$. Changing $n_i$ a little changes the energy by approximately $2w_i A n_i\,\Delta n_i$. Changing all entries gives

$$
\Delta E\approx\sum_i w_i\underbrace{(2An_i)}_{v_i}\Delta n_i.
$$

The derivative with respect to the raw vector entry is $\partial E/\partial n_i=w_i v_i$. The quantity that becomes a potential is $v_i$, after accounting for the integration weights. Forgetting the weights is an easy mistake when turning continuous formulas into code.

## Now let the grid become a continuum

The analogue is

$$
E[n]=\int A n(\mathbf r)^2\,d\mathbf r.
$$

Perturb the density by a small function $\eta(\mathbf r)$, with amplitude $\epsilon$:

$$
\begin{aligned}
E[n+\epsilon\eta]
&=\int A(n+\epsilon\eta)^2\,d\mathbf r\\
&=E[n]+\epsilon\int 2An\eta\,d\mathbf r+O(\epsilon^2).
\end{aligned}
$$

The coefficient multiplying the arbitrary perturbation is the functional derivative:

$$
\frac{\delta E}{\delta n(\mathbf r)}=2An(\mathbf r).
$$

More generally, the definition is the first-order relation

$$
\delta E=\int\frac{\delta E}{\delta n(\mathbf r)}\,\delta n(\mathbf r)\,d\mathbf r.
$$

It is a spatially varying answer to a practical question: **where would moving a little density raise or lower the energy?**

## Why a gradient-dependent energy needs another derivative

Take a GGA-like mathematical form $E[n]=\int f(n,\nabla n)\,d\mathbf r$. Its variation has two terms:

$$
\delta E=\int\left[\frac{\partial f}{\partial n}\delta n+
\frac{\partial f}{\partial(\nabla n)}\cdot\nabla\delta n\right]d\mathbf r.
$$

Integrating the second term by parts, and assuming the boundary term vanishes or is handled by the boundary conditions, gives

$$
\frac{\delta E}{\delta n}=
\frac{\partial f}{\partial n}-\nabla\cdot\frac{\partial f}{\partial(\nabla n)}.
$$

The minus sign comes from integration by parts. Even when evaluating an energy only requires $n$ and its first derivatives, evaluating the associated potential can involve further spatial derivatives. Smoothness is not just a cosmetic property of a fitted curve.

For the toy choice $f=An^2+B|\nabla n|^2$, the potential is $2An-2B\nabla^2 n$. The gradient penalty discourages rapid spatial variation. This example is a derivation, not a proposed physical XC functional.

## Electron number is a constraint

We cannot minimize energy by casually adding or removing electrons. At fixed electron number we impose $\int n=N$, introducing a Lagrange multiplier $\mu$:

$$
\frac{\delta}{\delta n}\left(E[n]-\mu\left[\int n-N\right]\right)=0.
$$

At a stationary density, the derivative equals the constant $\mu$, for the allowed variations. The actual Kohn–Sham problem also handles orbitals and their orthonormality; this density-level equation shows the role of the electron-count constraint.

## Small value error, large slope error

Let $g(x)=x^2+\epsilon\sin(\omega x)$. The extra term is bounded by $\epsilon$, but

$$
g'(x)=2x+\epsilon\omega\cos(\omega x).
$$

At $\epsilon=0.01$ and $\omega=100$, the value error is at most $0.01$ while the derivative error can be $1$. A model can look excellent on an energy plot and still steer an optimizer poorly.

This is the issue behind learning a functional for use inside a solver. Accurate predictions on known densities are useful. Stable minimization on densities the model encounters for itself is an additional requirement.

[[challenge/index|Return to the investigation.]] The early ML paper by [Snyder et al.](https://doi.org/10.1103/PhysRevLett.108.253002) makes the derivative problem explicit; [Li et al.](https://doi.org/10.1103/PhysRevLett.126.036401) train through the Kohn–Sham calculation itself. The elementary examples on this page are original pedagogical constructions, not reproductions of their experiments.

> [!todo] Things to check
> - Track quadrature weights when comparing a continuous derivative with an array gradient.
> - Check boundary conditions before dropping an integration-by-parts boundary term.
> - Orbital-dependent functionals need more machinery than the simple density-only formulas shown here.
