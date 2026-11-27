---
title: "CIDER: teach exchange with a physically scaled view of the density"
date: 2026-11-27
tags: [paper, machine-learning, nonlocality]
---

**Paper:** Bystrom and Kozinsky, *CIDER: An Expressive, Nonlocal Feature Set for Machine Learning Density Functionals with Exact Constraints* (2022). [DOI](https://doi.org/10.1021/acs.jctc.1c00904) · [preprint](https://arxiv.org/abs/2109.02788).

## TL;DR

CIDER learns exchange using nonlocal density descriptors designed around a known scaling law. The central contribution is the representation: look beyond one point, but make that view change correctly when the entire density is compressed.

## The problem

Exact exchange contains information about orbitals at two positions. A semilocal model receives much less information. It is therefore plausible that a more expressive model needs a wider view of the density—but a generic wider view can violate exact physical behaviour.

Suppose we compress the whole electron cloud. A descriptor that always samples a fixed radius in ångströms now sees a different relative portion of the cloud. The network would have to relearn that transformation from examples. CIDER tries to remove this burden through construction.

## The key idea

Uniform coordinate scaling defines

$$n_\gamma(\mathbf r)=\gamma^3 n(\gamma\mathbf r).$$

For $\gamma>1$, the density is squeezed into a smaller region. The factor $\gamma^3$ preserves electron number: substituting $\mathbf u=\gamma\mathbf r$ in the integral cancels it against the volume element.

Exact exchange obeys

$$E_x[n_\gamma]=\gamma E_x[n].$$

Write the exchange energy as a uniform-gas factor multiplied by a learned enhancement factor,

$$E_x[n]=-C_x\int n^{4/3}(\mathbf r)F_x[ n ](\mathbf r)\,d\mathbf r,
\qquad C_x=\frac34\left(\frac3\pi\right)^{1/3}.$$

If the descriptors feeding $F_x$ are scale-invariant at corresponding points, then $n^{4/3}$ contributes $\gamma^4$ and the integration measure contributes $\gamma^{-3}$. The required net factor $\gamma$ follows automatically. This is the same kind of structural reasoning encountered in [[papers/pbe|PBE]], now used to organize learning.

## How it works

The nonlocal descriptors integrate density around a reference point with Gaussian-like radial functions and angular components. Schematically,

$$G_{nlm}(\mathbf r)=\int g_{nlm}(\mathbf r';\mathbf r)
n(\mathbf r+\mathbf r')\,d\mathbf r'.$$

This is not the full paper formula: it shows the operation. The kernel's length scale depends on local electronic quantities so that the descriptor transforms correctly under coordinate scaling. Several widths capture different neighbourhoods. Angular components are contracted into rotational invariants, so rotating a molecule does not change its energy.

These features join semilocal quantities such as the reduced gradient and the orbital-environment indicator $\alpha$. A Gaussian-process model predicts the exchange enhancement. The descriptors and reference construction support constraints including uniform scaling and the uniform-electron-gas limit.

A Gaussian process here is a flexible regression model built from similarities between descriptors. It is not a neural network, and machine-learned DFT should not be treated as synonymous with neural DFT. The model is trained from integrated exchange-energy information; it need not be given a unique “true exchange energy density” at every point.

## Results that matter

The learned exchange is more accurate than the semilocal exchange models tested in the paper and transfers across the studied main-group molecular chemistry. Comparisons between feature sets show that the nonlocal descriptors supply useful information beyond a semilocal baseline.

The result is specifically about approximating **exchange**. It should not be reported as having learned all correlation or as solving every error in a complete XC functional. The reference being imitated and the correlation paired with the exchange remain part of the calculation.

## Limitations

A finite descriptor set still compresses information. Satisfying selected constraints does not guarantee good derivatives, convergence or accuracy in every chemical regime. Nonlocal descriptors also have a computational cost that must be evaluated in a real implementation.

The 2022 demonstration establishes the representation and its promise. The separate [[papers/cider-molecules-and-solids|2024 paper]] is the more direct bridge to efficient hybrid replacements in molecules and periodic solids.

## My take

The best exercise is the scaling derivation. It shows how a physical law can be guaranteed for every input through the representation, instead of rewarded only on a finite collection of training examples. That distinction helps make sense of the entire constraint-versus-data discussion.

> [!todo] Things to check
> - Verify electron-number preservation and the $\gamma^4\gamma^{-3}$ exchange scaling.
> - Keep exchange approximation error separate from the error of a full exchange–correlation calculation.
