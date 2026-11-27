---
title: "How to read a benchmark without being fooled by the average"
date: 2026-11-27
tags: [learning, benchmarks, reproducibility]
---

A benchmark number is the last line of a long experimental protocol. Before comparing two numbers, reconstruct the experiment that produced them.

## Start with the quantity

An atomization energy compares a molecule with its separated atoms. A reaction energy compares products with reactants. A barrier compares a transition state with its reactants. They use differences of large total energies, and the pattern of error cancellation is different in each case.

For individual errors $e_i=E_i^{\mathrm{method}}-E_i^{\mathrm{reference}}$, mean absolute error is

$$\mathrm{MAE}=\frac1N\sum_i|e_i|.$$

Mean signed error can reveal systematic over- or underestimation, but opposite errors cancel. Root mean square error emphasizes large errors. The maximum error or a distribution plot can expose a small group of severe failures hidden by an average.

## GMTKN55 is a collection of questions

[Goerigk et al. (2017)](https://doi.org/10.1039/C7CP04913G) organize diverse main-group thermochemistry, kinetics and noncovalent interactions into 55 subsets. WTMAD-2 balances their different energy scales. Using the standard notation,

$$\mathrm{WTMAD\mbox{-}2}=\frac1{\sum_s N_s}
\sum_s N_s\frac{56.84\ \mathrm{kcal\,mol^{-1}}}
{\overline{|\Delta E|}_s}\mathrm{MAD}_s.$$

$N_s$ is the number of energy differences in subset $s$, $\overline{|\Delta E|}_s$ its mean absolute reference energy and $\mathrm{MAD}_s$ the method's mean absolute error there. The common reference scale makes subsets with small energies count meaningfully. Use the [authors' dataset and evaluation implementation](https://github.com/grimme-lab/GMTKN55) for a formal calculation.

As a made-up example, consider two equally sized subsets with mean reference magnitudes 100 and 5 kcal/mol. Errors of 2 and 0.5 kcal/mol look smaller on the second subset in absolute terms. After dividing by each subset's energy scale, they are 0.02 and 0.10: the second is relatively worse. That is the kind of imbalance the weighting addresses.

WTMAD-2 is still one aggregate. It does not mean every reaction has that error or that a method passes a one-kcal/mol threshold everywhere. [[papers/skala|Skala's subset comparison]] makes this concrete.

## Reference accuracy is part of the experiment

CCSD(T) includes coupled-cluster singles and doubles plus a perturbative triples contribution. It is a strong reference for many single-reference molecules, but can fail when several electronic configurations are essential. A complete-basis-set extrapolation addresses basis incompleteness; it does not repair every limitation of the electronic method.

[Bartlett & Musiał's coupled-cluster review (2007)](https://doi.org/10.1103/RevModPhys.79.291) is the major background reading here. For our immediate purpose, retain the distinction between an accurate reference within its domain and an exact answer.

Experimental values require further care. An electronic calculation at fixed nuclei may need zero-point, thermal, relativistic, solvent or other corrections before it predicts the measured quantity. A discrepancy cannot automatically be assigned entirely to XC.

## What was held out?

There are progressively harder tests: new geometries of a known molecule, new molecular connectivity within familiar chemistry, unfamiliar functional groups, new charge/spin regimes, and new elements or phases. A random geometry split mainly measures the first kind of generalization.

Learned methods also need a development history. Was the benchmark used to select hyperparameters or model versions? Were near-duplicates excluded? Did labels come from the same source and protocol? A test set can influence development even if its energies were never directly included in gradient updates.

For a comparison, record the functional version, basis, integration grid, dispersion treatment, reference method, convergence rules and failures. Report failures rather than silently dropping them from the mean. These details are scientific content, not administrative footnotes. [Lejaeghere et al. (2016)](https://doi.org/10.1126/science.aad3000) demonstrate why agreement between implementations must itself be assessed.

## A speed number also needs a protocol

Distinguish a model forward pass, XC energy plus potential evaluation, one SCF iteration, a converged single-point calculation and a geometry optimization. Record hardware and parallelism. A speedup measured on a GPU does not immediately describe the experience on a laptop CPU.

This matters directly to the [Discovered Materials challenge](https://grandchallenges.discoveredmaterials.com/speed-accuracy-barrier/): public benchmark performance and the intended hidden reaction evaluation are related but different evidence. The live protocol governs a submission; this notebook is a literature investigation, not a submission report.

> [!todo] Things to check
> - Recalculate the toy weighting example before interpreting the real aggregate.
> - Read the hardest subsets and convergence failures alongside the headline score.
