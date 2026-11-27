---
title: "Bypassing Kohn–Sham: learn the density instead of finding it iteratively"
date: 2026-11-27
tags: [paper, machine-learning, density]
---

**Paper:** Brockherde et al., *Bypassing the Kohn–Sham equations with machine learning* (2017). [Open-access paper](https://doi.org/10.1038/s41467-017-00839-3).

## TL;DR

Learn the map from external potential to density, then the map from density to energy. This avoids the unstable derivative-based minimization that troubled earlier learned orbital-free models. It is a different intervention from designing a new XC functional.

## The problem

[[papers/learning-density-functionals|A learned kinetic-energy functional]] can have accurate values but unreliable derivatives outside the training-density region. Minimizing it then asks the model precisely the questions its training did not answer well.

Rather than repairing every derivative direction, can we predict the density that the electronic calculation would have found?

## The key idea

Use the ground-state potential-to-density relationship as the learning target. A compact density expansion makes the output manageable:

$$n^{\mathrm{ML}}[v](\mathbf r)=\sum_{l=1}^{L}u_l[v]\,\varphi_l(\mathbf r).$$

Here $\varphi_l$ are density-representation basis functions, not necessarily occupied molecular orbitals. Each $u_l[v]$ is a predicted expansion coefficient. Predicting coefficients is much cheaper than fitting an independent output for every point of a large three-dimensional grid.

![[bypassing-kohn-sham.png]]

*Figure 1 from Brockherde et al. (2017), [source](https://doi.org/10.1038/s41467-017-00839-3), © the authors, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cropped to the complete figure; original caption omitted. All panels and axes are retained.*

## How it works

In panel **a**, follow the red diagonal arrow: potential directly to density. The blue route goes through a kinetic-energy functional and an Euler-equation minimization. The red route avoids that minimization. The predicted density can then feed an energy functional.

Panel **c** shows the practical representation: molecular geometry defines a smooth representation of the potential; independent kernel models predict coefficients; those coefficients reconstruct the density. The paper explores representations including Fourier components and kernel principal components.

Panel **b** contains two different tests. The upper plot concerns density-driven energy errors in a one-dimensional model. Its vertical axis is logarithmic, so one major interval represents a factor of ten. The lower plot concerns an energy curve for a three-dimensional hydrogen molecule. Do not merge the two panels into one universal accuracy claim.

## Results that matter

The work demonstrates accurate density prediction for test systems and molecular examples, and uses the learned framework in molecular dynamics of malonaldehyde, including intramolecular proton transfer. It shows that predicting the density can be a useful computational shortcut rather than merely an intermediate visualization.

For the molecular DFT-generated training examples, agreement with the reference means learning that reference approximation. It does not automatically improve its unknown error against the exact many-electron answer. A surrogate can reproduce a DFT method extremely well while inheriting its chemistry errors.

## Limitations

The map is learned over the systems and configurations represented by data. It is not a proof that the model handles arbitrary elements, charge states or new bonding regimes. Compact basis representations also limit the density detail that can be recovered.

There is a distinction between avoiding the derivative with respect to density and avoiding all derivatives. Molecular dynamics still requires forces with respect to nuclear coordinates and a sufficiently smooth energy surface.

## My take

This paper belongs on the map because “use ML to accelerate DFT” can mean very different things. A learned XC model improves an ingredient inside the solver; this approach learns a map that bypasses the solver. Both can save time, but their reference accuracy, transfer requirements and failure modes differ.

> [!todo] Things to check
> - Identify whether a plotted error is relative to an exact model solution, PBE or another reference.
> - Explain why a density basis function need not be an occupied Kohn–Sham orbital.
