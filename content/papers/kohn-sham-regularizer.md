---
title: "Train through the calculation: Kohn–Sham equations as a regularizer"
date: 2026-11-27
tags: [paper, differentiable-physics, machine-learning]
---

**Paper:** Li et al., *Kohn–Sham Equations as Regularizer: Building Prior Knowledge into Machine-Learned Physics* (2021). [DOI](https://doi.org/10.1103/PhysRevLett.126.036401) · [full text](https://arxiv.org/abs/2009.08551).

## TL;DR

Instead of fitting an XC energy on fixed examples and testing the solver afterwards, differentiate through the Kohn–Sham iterations during training. The solver becomes part of the learning problem and supplies useful physical structure.

## The problem

A direct neural prediction of molecular energy from geometry must learn a great deal from data. An XC model inside DFT has a different opportunity: keep the known physics and learn only the missing approximation.

Even then, an energy fit can give bad derivatives and densities. [[papers/learning-density-functionals|Snyder's example]] showed that mismatch. This paper asks whether training through the computation can steer the model toward functionals that actually work when deployed.

## The key idea

Write one self-consistent iteration as a differentiable map,

$$n_{k+1}=\mathcal M_\theta(n_k).$$

$\theta$ are the network parameters. The map includes constructing the potential from the learned energy, solving the orbital problem, forming a new density and mixing it with the previous density. Unroll several iterations to form one larger computation.

The same functional is reused at each iteration. This resembles a recurrent network, but most operations are established physics and numerical linear algebra. The trainable component is the XC approximation.

## How it works

The paper's loss combines a final-density error with errors in the energy trajectory. Schematically, for each training system,

$$L=\frac1{N_e}\int|n_K(x)-n_{\mathrm{ref}}(x)|^2\,dx
+\frac1{N_e}\sum_{k=1}^{K}w_k(E_k-E_{\mathrm{ref}})^2.$$

$N_e$ is the electron count and $w_k$ are nonnegative iteration weights. This notation shows the structure; the paper also averages over training systems. Intermediate energies give gradients to earlier parts of the calculation, instead of supervising only the final answer.

For a parameter change, the density change propagates recursively:

$$\frac{d n_{k+1}}{d\theta}
=\frac{\partial\mathcal M_\theta}{\partial\theta}
+\frac{\partial\mathcal M_\theta}{\partial n_k}\frac{d n_k}{d\theta}.$$

The first term changes the current update directly. The second carries the effect of all previous updates. Automatic differentiation computes these chain-rule contributions through the unrolled graph.

Information range still matters. The authors compare local, near-local and global network receptive fields. A global convolution summarizes density over different length scales; local layers then process those features. Smooth activations support the derivatives the solver and training require. A separate gate enforces one-electron self-interaction cancellation in their construction.

## Results that matter

The memorable demonstration learns the dissociation curve of a **one-dimensional analogue** of hydrogen from two training separations. A third separation is used for model selection. The global model reaches the paper's chemical-accuracy band across the tested curve, including the stretched region; local models do not achieve the same behaviour far from the training points.

Read Figure 1 carefully: the training points are red diamonds, the validation point is a black triangle, and the error panels underneath matter more than the apparent agreement of the large total-energy curves.

The interaction is an exponential model potential, not the ordinary three-dimensional Coulomb interaction. Accurate references come from density matrix renormalization group calculations. This is a strong controlled demonstration of an idea, not evidence that two real molecules suffice for universal chemistry.

## Limitations

Differentiating through iterations has memory and computational costs. Difficult convergence or nearly degenerate eigenproblems can complicate gradients. A finite training trajectory is not a proof of convergence from arbitrary initial guesses.

Most importantly, the results show that both **solver-aware training and sufficient nonlocal information** matter. The same training strategy cannot make an informationally limited local model represent everything.

## My take

The network learns what its approximation causes the calculation to do. That is the conceptual advance. [[papers/skala|Skala]] uses a different two-stage strategy at a much larger scale, including self-consistent fine-tuning without backpropagating through the full SCF loop. It is useful to understand why a later method might keep the lesson while changing the implementation.

> [!todo] Things to check
> - Distinguish the two training separations from the additional validation separation.
> - Track where the energy loss and density loss enter the unrolled computation.
