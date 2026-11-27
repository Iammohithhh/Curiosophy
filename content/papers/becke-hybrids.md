---
title: "Becke's hybrid: why mix in exact exchange?"
date: 2026-11-27
tags: [paper, dft, hybrids]
---

**Paper:** Axel D. Becke, *Density-functional thermochemistry. III. The role of exact exchange* (1993). [DOI](https://doi.org/10.1063/1.464913).

## TL;DR

A hybrid introduces orbital-based exact exchange into an approximate density functional. Becke's three-parameter construction showed that this could substantially improve molecular thermochemistry. It also exposed the trade-off at the heart of our investigation: useful nonlocal information costs more to compute.

## The problem

An electron's exchange hole is not always well represented by a local picture. In a molecule, occupied orbitals extend across bonds and sometimes across much larger regions. Semilocal exchange has to infer this behaviour from limited local descriptors.

Hartree–Fock provides an exact expression for the exchange energy of a Slater determinant, but lacks the remaining correlation energy. Simply choosing between Hartree–Fock and a local approximation throws away a potentially useful combination.

## The key idea

Imagine continuously turning on the electron–electron interaction while adjusting an external potential to keep the density fixed. Let its strength be $\lambda$, from zero to one. The **adiabatic connection** expresses

$$E_{\mathrm{xc}}[n]=\int_0^1 W_\lambda[n],d\lambda.$$

$W_\lambda$ is the interaction contribution beyond the classical Hartree term at that interaction strength. The zero-coupling endpoint is exact exchange of the noninteracting reference. The integral also accounts for the kinetic part of correlation through this coupling-constant construction.

This gives a physical reason to include exact exchange. It does not uniquely derive a universal percentage. The practical mixture still requires choices about how the curve between the endpoints is approximated.

## How it works

Becke's form can be written

$$E_{\mathrm{xc}}=E_{\mathrm{xc}}^{\mathrm{LSDA}}
+a_0(E_x^{\mathrm{exact}}-E_x^{\mathrm{LSDA}})
+a_x\Delta E_x^{\mathrm{B88}}+a_c\Delta E_c^{\mathrm{PW91}}.$$

Start with local spin-density exchange and correlation. Replace a fraction of its exchange with exact exchange. Then add scaled gradient corrections to exchange and correlation. The fitted values were $a_0=0.20$, $a_x=0.72$ and $a_c=0.81$.

The paper is associated with **B3PW91**, using Perdew–Wang correlation. The familiar B3LYP substitutes a different correlation ingredient; it is misleading to identify this paper's actual formula as B3LYP.

What makes exact exchange nonlocal? In spin-orbital notation, for occupied orbitals,

$$E_x=-\frac12\sum_\sigma\sum_{ij}^{\mathrm{occ}}
\iint\frac{\phi_{i\sigma}^*(\mathbf r)\phi_{j\sigma}(\mathbf r)
\phi_{j\sigma}^*(\mathbf r')\phi_{i\sigma}(\mathbf r')}{|\mathbf r-\mathbf r'|}
,d\mathbf r,d\mathbf r'.$$

There are two spatial positions and two occupied-orbital indices. Exchange connects the orbital structure at $\mathbf r$ with that at $\mathbf r'$. Only same-spin orbitals exchange in this expression. A one-electron system has one occupied spin orbital; substituting it shows that exchange cancels that electron's Hartree self-repulsion.

In an atomic-orbital basis, the same structure creates four-index electron-repulsion integrals. This is where conventional quartic cost discussions arise. Screening, density fitting and other implementations change the practical cost substantially.

## Results that matter

The parameters were determined from a collection containing 56 atomization energies, 42 ionization potentials, eight proton affinities and ten atomic energies. The reported average absolute deviation for atomization energies was about $2.4\ \mathrm{kcal\,mol^{-1}}$.

That number belongs to the paper's fitting and assessment protocol. It is not an independent modern GMTKN55 result, and it does not mean every molecule is within 2.4 kcal/mol. Its historical importance is that a small, physically motivated mixture produced a useful improvement in molecular thermochemistry.

## Limitations

Exact exchange is exact for the determinant, not for the entire interacting electronic energy. Mixing it into a functional does not solve static correlation when several electronic configurations become essential. More exact exchange can improve delocalization errors while worsening other cases.

The coefficient is also global: the same fraction applies everywhere. Local hybrids allow spatially varying mixing; range-separated hybrids vary treatment with electron separation. Those are distinct extensions, not different names for the same idea. See [[learnings/nonlocality-and-cost|the guide to nonlocality and cost]].

## My take

The hybrid question becomes more interesting when phrased as: *what information did exact exchange supply that the semilocal approximation was missing?* That takes us toward [[papers/dm21|DM21]], which learns a local hybrid, and [[papers/cider|CIDER]], which tries to learn exchange more cheaply.

> [!todo] Things to check
> - Work through one-electron cancellation, including the factors of one half.
> - Keep the fitted-data result separate from evidence on genuinely unseen chemistry.
