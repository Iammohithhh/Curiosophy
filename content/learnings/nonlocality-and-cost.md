---
title: "Nonlocality and cost: what the functional families actually buy"
date: 2026-11-27
tags: [learning, scaling, dft]
---

“A more expensive functional” is not a complete explanation. We need to know what extra information it uses, which operation supplies that information, and whether that operation is the bottleneck in the intended calculation.

## First, two meanings of nonlocal

A density-only semilocal functional uses the density and a finite set of derivatives at the current point. A nonlocal functional can depend on separated regions. An orbital-dependent approximation can also carry information beyond elementary local density ingredients. These categories overlap, but their implementation costs differ.

Long-range electrostatics is already present in the Hartree term. Long-range exchange and long-range correlation are different pieces. A learned finite-range density descriptor does not automatically reproduce all of them.

## Range separation changes how distance is treated

The Coulomb kernel can be divided exactly:

$$\frac1r=\frac{\operatorname{erfc}(\omega r)}r+
\frac{\operatorname{erf}(\omega r)}r.$$

The first term is short-ranged and the second long-ranged. $\omega$ sets the crossover length; a larger $\omega$ moves it toward shorter distances. A functional designer can then use different exchange treatments in the two ranges.

Screened hybrids such as HSE use short-range exact exchange, reducing the long-range exchange burden that is particularly awkward in periodic systems. Other range-separated hybrids use substantial or full exact exchange at long range to improve properties affected by charge transfer and the asymptotic potential. These are different design goals. See [Heyd, Scuseria & Ernzerhof (2003)](https://doi.org/10.1063/1.1564060).

A **local hybrid** instead allows exchange mixing to vary spatially with the electronic environment. Distance separation and spatial mixing can coexist, as in [[papers/dm21|DM21]], but they are not synonyms.

## Double hybrids add a different kind of correlation

A schematic double hybrid is

$$E_{\mathrm{xc}}=a_xE_x^{\mathrm{HF}}+(1-a_x)E_x^{\mathrm{DFA}}
+a_cE_c^{\mathrm{PT2}}+(1-a_c)E_c^{\mathrm{DFA}}.$$

The additional second-order perturbative term sums over occupied **and virtual** orbitals. Virtual orbitals are the unoccupied orbitals available to describe electronic excitations. Their appearance brings more correlation information, more basis sensitivity and extra computational cost.

The influential [B2PLYP paper by Grimme (2006)](https://doi.org/10.1063/1.2148954) combines this strategy with density-functional ingredients. Canonical second-order perturbation theory is commonly associated with fifth-order scaling in basis size. Small orbital-energy denominators and multireference situations can make perturbative approximations unreliable; higher cost is not a universal accuracy certificate.

## Dispersion is not the same as exact exchange

Two neutral closed-shell fragments can attract through correlated charge fluctuations even when their densities barely overlap. At long distance, the leading pairwise contribution often behaves as $-C_6/R^6$. A strictly semilocal model cannot generally reconstruct the correlation between separated fluctuations.

There are several remedies. An atom-pair dispersion correction adds distance-dependent contributions with damping at short range. A nonlocal density correlation functional uses a two-point kernel, schematically

$$E_c^{\mathrm{nl}}=\frac12\iint n(\mathbf r)\Phi(\mathbf r,\mathbf r')
n(\mathbf r')\,d\mathbf r\,d\mathbf r'.$$

The [Dion et al. vdW-DF paper (2004)](https://doi.org/10.1103/PhysRevLett.92.246401) is a landmark in this route. The kernel is not simply the Hartree Coulomb kernel: it approximates nonlocal correlation. A double integral need not be evaluated by a naive all-pairs algorithm; fast convolution techniques can change practical cost.

This is why benchmark labels must include dispersion corrections. “SCAN” and “SCAN plus a dispersion treatment” are different protocols. [[papers/skala|Skala's v6 results]] likewise include a fixed D3 correction.

## Where cubic scaling enters

In a finite basis, orbitals are expanded as $\phi_i=\sum_\mu C_{\mu i}\chi_\mu$. A typical orbital equation becomes

$$FC=SC\varepsilon.$$

$F$ is the effective Hamiltonian matrix, $S$ the overlap matrix of a nonorthogonal basis, $C$ the orbital coefficients and $\varepsilon$ the diagonal matrix of orbital energies. Dense diagonalization has a common cubic scaling in matrix dimension. Making XC evaluation cheaper does not remove this operation.

The number of basis functions is also not simply the number of atoms. Changing elements, basis quality, diffuse functions or polarization functions changes the workload. A meaningful comparison specifies those choices and the accuracy being maintained.

## Why linear-scaling methods are possible—and conditional

For suitable insulating systems, the occupied-state density matrix decays with separation. That supports locality, sparse matrices and truncation. Metals at zero temperature generally have slower decay, making the same approximations more demanding. Temperature, dimensionality and the required accuracy matter.

[Prodan & Kohn's nearsightedness paper (2005)](https://arxiv.org/abs/cond-mat/0503124) supplies the physical viewpoint. [Bowler & Miyazaki's review (2012)](https://arxiv.org/abs/1108.5976) connects it to linear-scaling electronic-structure algorithms. These are the main readings for the scaling branch; they are not claims that every DFT calculation can cheaply become $O(N)$.

There is also a different escape route: approximate $T_s[n]$ and eliminate orbitals. [Mi et al.'s orbital-free review (2023)](https://doi.org/10.1021/acs.chemrev.2c00758) explains both the attraction and the difficulty. [[papers/learning-density-functionals|Learning kinetic functionals]] and [[papers/bypassing-kohn-sham|learning potential-to-density maps]] belong to this broader branch.

## More physics outside this main thread

Two important branches deserve a place on the map without interrupting the XC-learning story. The random-phase approximation uses electronic response to construct nonlocal correlation; [Ren et al. (2012)](https://arxiv.org/abs/1203.5536) is a substantial guide. DFT+U addresses selected localized orbital subspaces with a corrective interaction and a double-counting subtraction; [Himmetoglu et al. (2014)](https://arxiv.org/abs/1309.3355) explains the method and its limits. Neither is interchangeable with a general molecular XC functional.

> [!todo] Things to check
> - For a cost claim, identify the size variable, basis, accuracy target and measured operations.
> - Keep electrostatics, exact exchange and dispersion separate when a paper says “nonlocal.”
