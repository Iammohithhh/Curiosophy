---
title: "Reading an XC architecture without treating the network as magic"
date: 2026-11-27
tags: [learning, architecture, mathematics]
---

The most useful first question about a neural functional is very plain: **what can one output see?** Everything else follows from that information boundary.

## Begin with a local network

![[nagai-network.png]]

*Figure 1 from Nagai, Akashi & Sugino, [*Completing density functional theory by machine learning hidden messages from molecules* (2020)](https://doi.org/10.1038/s41524-020-0310-0), © the authors, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cropped to the diagram, with the original caption omitted.*

The diagram shows a meta-GGA-type network. Density $n$, spin polarization $\zeta$, a reduced gradient $s$ and an orbital kinetic descriptor $\tau$ feed hidden layers. In an elementary dense layer,

$$\mathbf h_{k+1}=f(W_k\mathbf h_k+\mathbf b_k).$$

$W_k$ mixes the input features, $\mathbf b_k$ shifts them, and the nonlinear activation $f$ allows the result to be more expressive than a linear combination. Repeating layers composes transformations. Training adjusts the weights and biases to reduce a chosen loss.

At a grid point, the network predicts an energy-per-electron contribution. Integration converts those local outputs into an energy:

$$E_{\mathrm{xc}}\approx\sum_g w_g n_g\varepsilon_{\mathrm{xc},\theta}(\mathbf x_g).$$

$g$ indexes grid points and $w_g$ are quadrature weights. The same learned function is applied at all points; a bigger molecule does not require a new network for every extra point.

That construction can be very flexible **as a function of its inputs**. But if two environments produce the same $\mathbf x_g$, it must predict the same local output for them. Adding hidden layers does not provide missing observations.

The Nagai paper also studies a near-region density descriptor and trains on energies and densities from three molecules, H₂O, NH₃ and NO. Its comparison across local and more informative inputs is useful context for the later nonlocal architectures. The cropped diagram above depicts the meta-GGA variant, not every variant in the paper.

## How to enlarge the view

A convolution summarizes a neighbourhood:

$$h(\mathbf r)=\int K(\mathbf r,\mathbf r')n(\mathbf r')\,d\mathbf r'.$$

The kernel determines which positions influence the result and with what weights. A fixed-length kernel, a density-scaled kernel and a learned kernel encode different assumptions. [[papers/cider|CIDER's scaling construction]] makes one of those assumptions explicit.

A projection compresses a density field into coefficients. A graph network then passes messages between compact representations. In schematic form,

$$\mathbf m_i=\sum_{j\in\mathcal N(i)}M(\mathbf h_i,\mathbf h_j,\mathbf r_j-\mathbf r_i),
\qquad \mathbf h_i'=U(\mathbf h_i,\mathbf m_i).$$

$M$ constructs messages and $U$ updates a node. Neighbour definitions and repeated layers control the receptive field. For an equivariant model, these operations must respect the rotation rules of their features. The equation illustrates message passing generally; the precise tensor operations differ among architectures.

[[papers/neuralxc|NeuralXC]] uses atom-centred projections and invariant atomic networks. [[papers/equivariant-functionals|EG-XC]] communicates through equivariant graph features. [[papers/skala|Skala]] uses a fine-to-coarse-to-fine representation. Reading the diagrams becomes easier once these operations have names and concrete roles.

## The output must still behave like an energy

Rotating or translating an isolated molecule should not change its total energy. Relabelling identical atoms should not matter. For noninteracting distant fragments, the total energy should become the sum of fragment energies. These are different properties; one does not imply the others.

An additive construction helps size behaviour, but any global normalization or global feature must be checked. A network that divides by the total atom count can unintentionally turn an extensive energy into an intensive quantity. A finite interaction cutoff can improve locality while missing important long-range physics. Architecture choices have scientific consequences.

Finally, the derivative of the energy enters the electronic solver. Smooth activations help, but smoothness alone does not guarantee the right potential. Accurate values, physically sensible derivatives and reliable self-consistency are separate tests. The [[learnings/functionals-and-derivatives|functional-derivative note]] gives the mathematics behind that statement.

> [!todo] Things to check
> - For each architecture, trace one output back to all spatial regions that can influence it.
> - Identify which symmetries and size properties are guaranteed by construction and which are merely tested.
