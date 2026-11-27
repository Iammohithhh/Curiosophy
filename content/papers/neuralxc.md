---
title: "NeuralXC: turn a density correction into a self-consistent method"
date: 2026-11-27
tags: [paper, machine-learning, representation]
---

**Paper:** Dick and Fernandez-Serra, *Machine learning accurate exchange and correlation functionals of the electronic density* (2020). [Open-access paper](https://doi.org/10.1038/s41467-020-17265-7).

## TL;DR

NeuralXC projects the electronic density into atom-centred descriptors, learns an energy correction to a baseline functional, and differentiates that correction to obtain a potential. The resulting correction can participate in a self-consistent DFT calculation.

## The problem

A density grid can contain many thousands of values. A network needs a manageable representation, and the predicted energy must not change when the whole molecule rotates or identical atoms are relabelled.

There is also a practical integration problem. A correction to the final energy alone does not tell a DFT program how to update the density. To become part of the electronic calculation, the model needs a consistent potential.

## The key idea

Project the density onto localized functions around each atom, remove orientation dependence, predict atomic energy contributions and sum them. Then follow the derivatives back through those same operations.

![[neuralxc-architecture.png]]

*Figure 1 from Dick & Fernandez-Serra (2020), [source](https://doi.org/10.1038/s41467-020-17265-7), © the authors, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cropped from the article to show the complete diagram; the original caption is omitted. Read left to right for energy prediction, and right to left along the bottom for the potential.*

## How it works

An atom-centred projection has the form

$$c^I_{nlm}=\int\rho(\mathbf r)\psi^I_{nlm}(\mathbf r-\mathbf R_I)\,d\mathbf r.$$

$I$ labels the atom. $n$ labels a radial function, while $l,m$ label spherical harmonics describing angular structure. This $n$ is an index, not the electron density. The coefficients summarize how much density occupies different shapes around the atom.

Under a rotation, coefficients with the same $l$ mix. Summing their squares gives an invariant descriptor,

$$d^I_{nl}=\sum_{m=-l}^{l}(c^I_{nlm})^2.$$

The correction is a sum of outputs from networks shared among atoms of the same element:

$$E_{\mathrm{ML}}[\rho]=\sum_I\epsilon_{\alpha_I}(\mathbf d^I[\rho]),\qquad
E_{\mathrm{NXC}}=E_{\mathrm{base}}+E_{\mathrm{ML}}.$$

$\alpha_I$ denotes the element. Shared networks and summation make the result insensitive to how equivalent atoms are numbered. For sufficiently separated fragments with local descriptors, the sum also gives a natural route to additivity.

Now apply the chain rule. Group all projection indices into $\beta$. Because the projection is linear in density,

$$\frac{\delta E_{\mathrm{ML}}}{\delta\rho(\mathbf r)}
=\sum_\beta\frac{\partial E_{\mathrm{ML}}}{\partial c_\beta}\psi_\beta(\mathbf r).$$

The network supplies ordinary derivatives with respect to coefficients. The projection supplies the spatial basis functions. Together they give a potential that is added to the baseline potential. The model is connected to the SCF loop through a derivative of its own energy, rather than a separate unrelated potential predictor.

## Results that matter

The paper constructs a collection of specialized corrections, including water and molecular datasets. It demonstrates transfer from smaller to larger systems within related chemistry, and a water-focused model that performs well in tests including liquid structure. These are useful examples of a correction learning transferable electronic information within a domain.

The authors also report that improved energies do not generally produce comparably improved full densities, apart from selected moments. That observation is as important as the energy successes: energy supervision alone does not settle density quality.

## Limitations

The paper explicitly presents dataset-specific functionals, not one universal functional. The atom-centred representation depends on nuclear positions and, as implemented, species. That differs from a purely universal density-only form with no explicit nuclear reference.

Rotational invariance can discard information when a descriptor is too compressed. Local cutoffs limit what separated environments can communicate. Later equivariant models retain directional features during processing and only make the final energy invariant.

## My take

Trace one arrow in each direction through the figure. If the forward projection makes sense and the reverse chain rule makes sense, the architecture stops being a mysterious block called “ML.” It becomes a sequence of physically interpretable operations. Continue to [[papers/equivariant-functionals|equivariant graph functionals]] for a different way to exchange information between regions.

> [!todo] Things to check
> - Verify rotational invariance of the squared coefficients for a complete $m$ multiplet.
> - Keep the water-specific and broader molecular models separate when reading their reported results.
