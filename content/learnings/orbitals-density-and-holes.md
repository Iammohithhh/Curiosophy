---
title: "From orbitals to a density—and the hole around an electron"
date: 2026-11-27
tags: [learning, mathematics, quantum-chemistry]
---

This is the algebra behind several claims in the [[challenge/index|main investigation]]. We do not need to read the original foundational papers separately to use their ideas carefully.

## An orbital is an auxiliary object

The interacting many-electron wavefunction is not generally a product of independent electron waves. Kohn–Sham theory nevertheless introduces an auxiliary noninteracting system whose density matches the target ground-state density. Its occupied spin orbitals give

$$n(\mathbf r)=\sum_{i\sigma}f_{i\sigma}|\phi_{i\sigma}(\mathbf r)|^2.$$

Each normalized spin orbital integrates to one, and its occupation is between zero and one. An alternative spatial-orbital convention uses occupations up to two. Mixing these conventions silently creates factor-of-two errors.

The orbital energy eigenvalues are useful mathematical outputs, but should not all be interpreted as exact physical excitation or removal energies. The density and total-energy construction are the immediate target here.

## Why an eigenvalue equation appears

The noninteracting kinetic energy in atomic units is

$$T_s=\frac12\sum_i f_i\int |\nabla\phi_i|^2\,d\mathbf r.$$

For a density-only XC approximation, minimize the energy with respect to the orbitals while enforcing their orthonormality. The overlap constraints are $\langle\phi_i|\phi_j\rangle=\delta_{ij}$. Lagrange multipliers enforce these constraints; variation of the kinetic term gives $-\nabla^2/2$ after integration by parts with suitable boundary conditions.

Variation of the density-dependent terms gives the external, Hartree and XC potentials. After a choice of orbitals that diagonalizes the multiplier matrix, the result is

$$\left[-\frac12\nabla^2+v_{\mathrm{ext}}(\mathbf r)+v_H(\mathbf r)+v_{\mathrm{xc}}(\mathbf r)\right]
\phi_i(\mathbf r)=\epsilon_i\phi_i(\mathbf r).$$

Here

$$v_H(\mathbf r)=\int\frac{n(\mathbf r')}{|\mathbf r-\mathbf r'|}\,d\mathbf r',
\qquad v_{\mathrm{xc}}=\frac{\delta E_{\mathrm{xc}}}{\delta n}.$$

The factor $1/2$ in the Hartree energy disappears in its derivative because either occurrence of the density can vary. The [[learnings/functionals-and-derivatives|functional derivative note]] explains the underlying variation explicitly.

The equation looks like a one-particle Schrödinger equation, but its potential depends on the density made from its solutions. That circular dependence is why we iterate. Orbital-dependent XC forms can produce a generalized Kohn–Sham operator; they should not all be forced into the simple multiplicative-potential expression above.

## How this becomes matrix algebra

Choose basis functions $\chi_\mu$ and expand $\phi_i=\sum_\mu C_{\mu i}\chi_\mu$. Project the equation onto each basis function. The result is

$$FC=SC\varepsilon,\qquad
S_{\mu\nu}=\int\chi_\mu^*\chi_\nu\,d\mathbf r.$$

$F$ contains matrix elements of the effective operator; $S$ accounts for nonorthogonal basis functions. If the basis were orthonormal, $S$ would be the identity. The density matrix, using occupations consistently, is

$$P_{\mu\nu}=\sum_i f_i C_{\mu i}C_{\nu i}^*,\qquad
n(\mathbf r)=\sum_{\mu\nu}P_{\mu\nu}\chi_\mu(\mathbf r)\chi_\nu^*(\mathbf r).$$

This matrix is a compact representation of the occupied orbitals. It is not the full many-electron density operator. Changing the orbital basis changes its entries, so an ML model that consumes those entries needs a plan for basis dependence and symmetry.

## The exchange–correlation hole is conditional probability

Let $n_2(\mathbf r,\mathbf r')$ be the spin-summed ordered pair density. Given an electron at $\mathbf r$, the conditional density of the **other** electrons is

$$n_{\mathrm{cond}}(\mathbf r'|\mathbf r)=\frac{n_2(\mathbf r,\mathbf r')}{n(\mathbf r)}.$$

It integrates over $\mathbf r'$ to $N-1$, whereas the ordinary density integrates to $N$. Define the hole by subtracting the ordinary density:

$$n_{\mathrm{xc}}(\mathbf r,\mathbf r')=n_{\mathrm{cond}}(\mathbf r'|\mathbf r)-n(\mathbf r'),
\qquad\int n_{\mathrm{xc}}(\mathbf r,\mathbf r')\,d\mathbf r'=-1.$$

This deficit of one electron is not a claim that the hole is negative at every point. Correlation can redistribute probability, reducing it in some places and increasing it in others. Exchange alone already creates a hole due to antisymmetry; correlation further changes the conditional distribution.

The Coulomb interaction of the density with the **physical**, fully interacting hole describes the interaction-energy correction beyond Hartree. To obtain the full $E_{\mathrm{xc}}$, including kinetic correlation, use the hole averaged along the density-preserving adiabatic connection:

$$E_{\mathrm{xc}}=\frac12\iint\frac{n(\mathbf r)\overline n_{\mathrm{xc}}(\mathbf r,\mathbf r')}
{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'.$$

The bar matters. Dropping the coupling-constant average while calling the expression the full XC energy loses the kinetic-correlation distinction. This is the connection between the hole picture and [[papers/becke-hybrids|Becke's adiabatic-connection argument]].

For one electron there are no other electrons, so the conditional density is zero and the hole is $-n(\mathbf r')$. Its interaction exactly cancels Hartree self-repulsion. That is the simplest possible check of the picture.

These derivations use standard Kohn–Sham and pair-density definitions. The constraint and hole viewpoint is developed in [[papers/pbe|PBE]], [[papers/scan|SCAN]] and the [orbital-free DFT review](https://doi.org/10.1021/acs.chemrev.2c00758).

> [!todo] Things to check
> - Check electron-count and spin conventions before comparing density matrices between papers.
> - Explain why a physical pair-density hole and a coupling-constant-averaged hole play different roles in the energy.
