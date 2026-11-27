---
title: Can we make quantum chemistry both fast and accurate?
date: 2026-11-27
tags:
  - investigation
  - dft
  - exchange-correlation
description: A visual investigation of the DFT speed–accuracy problem, from electron density and physical constraints to learned functionals.
---

I don't have a supercomputer or a room full of GPUs. I do have a question that seems worth getting lost in: **why is it still so difficult to predict what a molecule will do?**

The laws are not the mystery. We know the basic quantum mechanics. The difficulty is turning those laws into an answer, at a useful level of accuracy, before the computation becomes impractical.

The [Discovered Materials speed–accuracy challenge](https://grandchallenges.discoveredmaterials.com/speed-accuracy-barrier/) makes this concrete. It asks for a better exchange–correlation functional: the central approximation in ordinary Kohn–Sham density functional theory. It wants improved molecular predictions without sacrificing computational efficiency. Public evidence comes from GMTKN55; a hidden evaluation concerns reaction chemistry relevant to thin-film manufacturing.

I want to understand this problem before trying to improve anything. This page follows the literature as a sequence of questions. The separate [[papers/index|paper notes]] examine particular breakthroughs; the [[learnings/index|learning notes]] slow down where the mathematics needs more room.

> [!info] Looking for the paper deep dives?
> **[[papers/index|Open all 13 paper deep dives →]]** Each is a separate, detailed page. Start with [[papers/pbe|PBE]], or jump ahead to [[papers/dm21|DM21]] and [[papers/skala|Skala]]. The article below connects their ideas into one story.

## A small energy difference can change the chemistry

Imagine two reactants approaching. Their electrons rearrange. One bond weakens, another forms, and eventually the system reaches a new configuration. A calculation can assign an electronic energy to each arrangement of the nuclei. Together, those energies describe a **potential-energy surface**.

The difference between product and reactant energies tells us about the electronic contribution to reaction energetics. The height of a saddle point above the reactants contributes to the activation barrier. Those are different questions: a downhill reaction can still be slow if it has a substantial barrier.

![[reaction-landscape.png]]

*An original schematic, not a calculated reaction. The horizontal coordinate represents progress along a path through molecular geometries, not time. Real reactions live on a surface with many coordinates.*

Why worry about an error of one kilocalorie per mole? As an illustration, transition-state theory gives a rate of the form

$$
k\approx\frac{k_B T}{h}\exp\left(-\frac{\Delta G^\ddagger}{RT}\right).
$$

Here $\Delta G^\ddagger$ is the activation **free energy**, $R$ is the molar gas constant, and $T$ is temperature. Holding the prefactor fixed, raising the barrier by $1\ \mathrm{kcal\,mol^{-1}}$ at $298\ \mathrm K$ changes the predicted rate by a factor of about $\exp(1/0.592)\approx5.4$. This is an illustrative sensitivity calculation, not a claim that a DFT electronic barrier is already a complete free-energy barrier. Entropy, temperature, solvent and sampling can matter too.

That is the attraction of this problem. A modest numerical improvement can change a chemical conclusion. But an expensive calculation repeated for thousands of geometries or candidates can become the limiting step.

## The many-electron problem hides inside a small molecule

For fixed nuclei, an electronic wavefunction depends on the coordinates and spins of all the electrons:

$$
\Psi(\mathbf r_1,\sigma_1,\ldots,\mathbf r_N,\sigma_N).
$$

For ten electrons, its spatial argument already has thirty coordinates. It is not ten independent three-dimensional clouds. Electrons interact, and the probability of one configuration depends on what all the others are doing.

This does not mean every quantum-chemistry algorithm literally stores a thirty-dimensional grid. Practical methods use orbitals, basis sets, determinants and structured approximations. It does explain why the exact many-electron description becomes difficult so quickly.

The density is a much smaller object. Fix a position, average the probability over all other electron coordinates and spins, and count all the indistinguishable electrons that could be there. The resulting $n(\mathbf r)$ is an expected number per unit volume. It obeys

$$
\int n(\mathbf r)\,d\mathbf r=N.
$$

Ground-state density functional theory establishes that this density can be the basic variable of an exact energy theory, under the usual conditions. That is a profound reduction in the description. It does **not** hand us a simple formula for the energy.

One caution will follow us throughout: knowing that a map exists is different from having a compact, accurate way to evaluate it. Machine learning changes how we approximate the map. It does not remove the distinction.

If the square brackets and integrals feel like a jump, pause at [[learnings/functionals-and-derivatives|What is a functional, and why do its derivatives matter?]] We will need that distinction repeatedly.

## The bargain Kohn–Sham DFT makes

The Kohn–Sham construction introduces an auxiliary system of noninteracting electrons with the same ground-state density. Its orbitals make the noninteracting kinetic energy $T_s$ calculable. In atomic units, the electronic energy is written

$$
E[n]=T_s[n]+\int v_{\mathrm{ext}}(\mathbf r)n(\mathbf r)\,d\mathbf r
+E_H[n]+E_{\mathrm{xc}}[n].
$$

The nuclear repulsion is added for the total energy at a fixed nuclear geometry. The terms above have separate jobs:

| Term | What it accounts for |
|---|---|
| $T_s$ | Kinetic energy of the auxiliary noninteracting electrons |
| $\int v_{\mathrm{ext}}n$ | Interaction with the nuclei and other external fields |
| $E_H$ | Classical Coulomb repulsion of the electron density with itself |
| $E_{\mathrm{xc}}$ | What remains: exchange, electron correlation and the kinetic-energy difference $T-T_s$ |

Atomic units set quantities including $\hbar$, the electron mass and the Coulomb constant times the squared elementary charge to one. This simplifies the notation; it does not remove physical units from the answers.

The troublesome classical term is

$$
E_H[n]=\frac12\iint\frac{n(\mathbf r)n(\mathbf r')}{|\mathbf r-\mathbf r'|}\,d\mathbf r\,d\mathbf r'.
$$

The factor $1/2$ avoids counting each pair twice. But this expression also assigns a self-repulsion to a one-electron cloud. Exact exchange cancels that one-electron Hartree energy. Approximate functionals need not cancel it correctly. That gives us a first, very small diagnostic: if a method struggles even with one electron, more training molecules do not automatically fix its underlying behaviour.

Exchange is a consequence of fermionic antisymmetry. Correlation describes additional electron coordination beyond the independent-particle reference. Both influence the chance of finding another electron near a chosen electron. The useful picture is a **hole** in that conditional probability, not a literal cavity in the molecule.

The [[learnings/orbitals-density-and-holes|orbital, density and exchange-hole detour]] derives the orbital equation, explains what a basis matrix means and shows why the missing probability around an electron integrates to one electron. Those details make “exchange” much less of a label to memorize.

The exact XC functional would complete this energy expression. In practice we also make numerical and modelling choices: finite basis sets, grids, pseudopotentials where used, convergence thresholds and usually the fixed-nuclei approximation. XC is the major unknown functional, not the only possible source of error.

## Why predicting an energy is only half the job

The density is not supplied by an oracle. The functional helps determine it.

For a density-only functional, its functional derivative gives the XC potential:

$$
v_{\mathrm{xc}}(\mathbf r)=\frac{\delta E_{\mathrm{xc}}}{\delta n(\mathbf r)}.
$$

That potential enters an orbital equation. The occupied orbitals give a new density. We then rebuild the potential and repeat until input and output agree. This is **self-consistency**. Orbital-dependent functionals such as hybrids require a more general treatment, often through a generalized Kohn–Sham operator.

![[self-consistency.png]]

*The energy model participates in a feedback loop. A small error in its value need not imply a small error in its slope, and a poor slope can alter the density found by the solver.*

A one-variable analogy makes the issue visible. Start with a smooth energy $f(x)$ and add $\epsilon\sin(\omega x)$. The energy perturbation never exceeds $\epsilon$, but its derivative has amplitude $\epsilon\omega$. Tiny wiggles can have steep slopes.

That is why a learned functional cannot be judged only by predictions on fixed, convenient densities. Does it produce sensible potentials? Does the calculation converge? Does the resulting density support accurate forces and response properties? These questions will lead us to differentiable DFT.

Try the first experiment below. Keep the energy ripple small, then increase its frequency. The derivative can become poor while the energy curves remain deceptively close. The other two experiments will connect to fractional charge and scaling later in the story.

<iframe src="../images/dft-playground.htm" title="Interactive laboratory: energy derivatives, fractional charge and scaling" loading="lazy" style="width:100%;height:930px;border:1px solid #c2d2cc;border-radius:12px" sandbox="allow-scripts"></iframe>

[Open the laboratory on its own](../images/dft-playground.htm). All three experiments use explicitly stated toy formulas; none reports a molecular calculation.

There is another subtlety. A poor energy can come from the formula itself, the density supplied to it, or both. [[papers/density-corrected-dft|Kim, Sim and Burke's error decomposition]] makes this separation precise. It is worth learning before deciding what a new model should optimize.

## First idea: understand each point using its neighbourhood

The local-density approximation, LDA, replaces a complicated environment with a uniform electron gas at the same density. We evaluate an energy contribution at each point and integrate:

$$
E_{\mathrm{xc}}^{\mathrm{LDA}}[n]=\int n(\mathbf r)\,
\varepsilon_{\mathrm{xc}}^{\mathrm{uniform}}(n(\mathbf r))\,d\mathbf r.
$$

A molecule is not a uniform gas. The density rises near nuclei and falls between fragments. A generalized gradient approximation, GGA, adds the local rate of change, $\nabla n$. **PBE** is the landmark example of choosing that dependence using physical constraints.

A meta-GGA adds more information, commonly the orbital kinetic-energy density $\tau$. **SCAN** uses this richer description to distinguish local electronic environments while satisfying conditions that an admissible approximation should obey.

The [[papers/pbe|PBE close reading]] works through its exchange enhancement curve and limiting behaviour. The [[papers/scan|SCAN close reading]] derives the environment indicator $\alpha$. Read them as two answers to successive questions: *what constraints should the formula obey, and what additional information would help it tell environments apart?*

![[functional-information.png]]

*An original map of common ingredients. These are families of approximations, not a guarantee that every step improves every property. Machine learning can be used at several places on this map.*

The limitation is informational. A semilocal model sees quantities at one point, including a limited set of derivatives or orbital-derived descriptors. A more complicated function of those same inputs cannot recover every dependence on distant regions. Two situations that look identical through the chosen descriptors are indistinguishable to the model.

## Second idea: bring in exact exchange

A hybrid combines approximate density-functional ingredients with a fraction of exact exchange evaluated from orbitals. A simple global-hybrid form is

$$
E_{\mathrm{xc}}^{\mathrm{hyb}}=aE_x^{\mathrm{exact}}
+(1-a)E_x^{\mathrm{DFA}}+E_c^{\mathrm{DFA}}.
$$

$a$ is the exchange mixing fraction; DFA means density-functional approximation. Actual constructions can be more elaborate. Becke's 1993 work is an important turning point in this strategy.

Why is this useful? The exact-exchange expression involves pairs of occupied orbitals at two positions. It carries nonlocal electronic information that a simple local environment lacks. Why is it expensive? Evaluating those orbital-pair interactions introduces substantial work.

“Exact” modifies **exchange**, not the whole prediction. A hybrid still approximates correlation and can still fail badly when a single-reference picture is inadequate. Nor is more exact exchange always better: a coefficient that improves one error can worsen another.

Range-separated hybrids treat different distance ranges differently. Double hybrids add a perturbative correlation contribution. Each is a way to acquire more useful information, with a computational bill attached. Efficient integral algorithms can reduce that bill; the functional family alone does not determine the runtime.

The [[papers/becke-hybrids|Becke paper note]] connects the mixture to the adiabatic connection and writes out the two-position exchange integral. The [[learnings/nonlocality-and-cost|nonlocality and cost guide]] then separates screened exchange, range separation, double hybrids and dispersion. They solve different pieces of the problem.

## What kind of scaling are we talking about?

There are at least three distinct expenses: the cost of one XC evaluation, the cost of a complete self-consistent calculation, and the cost of the many calculations needed for a scientific prediction.

![[scaling-is-not-runtime.png]]

*Illustrative power laws normalized to the same cost at one arbitrary reference size. These are not measured timings or predictions for particular software. Real prefactors, sparsity, basis choices and crossover sizes matter.*

Dense diagonalization of an $M\times M$ matrix is commonly cubic in $M$. Conventional exact-exchange construction is often discussed in terms of quartic operation counts. Canonical CCSD(T) has a much steeper leading cost. But screening, density fitting, localization and hardware change practical performance. A statement such as “$O(N)$” also needs a definition of $N$ and the accuracy maintained as it grows.

The physics behind locality is encouraging: in suitable systems, distant changes have limited influence on local electronic properties. **Nearsightedness** supports methods with sparse or localized representations. It is not permission to discard long-range electrostatics or dispersion.

For the challenge, the useful question is not just “what is the exponent?” It is “how long does the whole calculation take, at comparable accuracy, on the relevant molecules?”

In the laboratory's scaling experiment, replace an expensive component with a lower-power expression but give it a large prefactor. It initially becomes slower. At larger sizes it wins, yet the untouched cubic component remains. This is why neither an exponent nor the speed of one neural-network evaluation is enough to describe a complete calculation.

## Third idea: learn the missing functional

It is tempting to write $E_{\mathrm{xc}}=\mathrm{neural\ network}(n)$ and declare the problem solved. But that leaves almost everything important unspecified.

What does the network see? A density grid? Local descriptors? Orbital information? A density matrix? How does it respect rotations, spin, electron count and size consistency? Is it trained on energies alone, densities as well, or the behaviour of a self-consistent calculation? What happens outside the chemistry used for training?

The breakthroughs become easier to follow when separated by the question each asks:

| Idea | The question it changes |
|---|---|
| [Learning a functional from examples](../papers/learning-density-functionals.md) | Can a flexible model approximate a map from a density to an energy? |
| [Training through Kohn–Sham iterations](../papers/kohn-sham-regularizer.md) | Can the solver supply physical structure during learning? |
| [DM21](../papers/dm21.md) | Can fractional-charge and fractional-spin examples address known failure modes? |
| [CIDER](../papers/cider.md) | Can constrained nonlocal descriptors replace costly exchange information? |
| [Equivariant graph functionals](../papers/equivariant-functionals.md) | Can density information be compressed and communicated efficiently? |
| [Skala](../papers/skala.md) | Can learned nonlocal representations and diverse accurate data improve the accuracy–cost trade-off? |

These are not interchangeable approaches. DM21 is a learned local hybrid and still uses exact-exchange ingredients. CIDER's earlier papers focus on learning exchange. Skala learns XC with a different nonlocal representation. A model that predicts energies directly from atomic coordinates is another category again: it can bypass DFT, but it is not necessarily an XC functional.

This is where the investigation becomes especially interesting. We can ask whether the important advance comes from better data, better physical constraints, a more informative representation, a better training objective, or a faster implementation. Usually several of these interact.

## The first lesson from learning: a good fit is not yet a good functional

Snyder and colleagues' 2012 model learned a kinetic-energy functional for a one-dimensional system. The values looked promising. The derivative needed to find a density was much harder. The model had seen a restricted family of densities, not every possible way of changing a density grid. It could interpolate familiar examples without knowing how to guide a search in every direction.

There are several responses to this difficulty. [[papers/bypassing-kohn-sham|Brockherde et al.]] learned the map to the density directly, bypassing that search. [[papers/neuralxc|NeuralXC]] built a differentiable correction from atom-centred density projections. [[papers/kohn-sham-regularizer|Li et al.]] trained through the solver, so the network was judged by the densities and energies its own approximation produced.

These are different interventions. It helps to draw the computational pipeline and mark exactly which arrow is learned. Is the network predicting an energy, a density, an XC correction, or a potential? Does it run before the electronic calculation, inside every iteration, or after convergence?

The [[learnings/architectures-without-mystery|architecture guide]] starts with a real paper diagram and explains projections, hidden layers, convolutions and message passing one operation at a time. The network becomes easier to understand when we ask what information each operation receives and what symmetry it preserves.

## A fractional electron is a very useful question

Ordinary training molecules tend to have integer electron counts. Yet a functional's behaviour between those integers reveals whether it artificially rewards spreading charge. The exact ensemble energy follows straight segments between adjacent integer states. Many approximations bow below those segments.

For two far-separated identical fragments sharing an extra electron, downward curvature can make a half-electron on each fragment artificially too favourable. The laboratory's fractional-charge experiment isolates this effect. Set the curvature to zero, then restore it and move the charge slider. The model develops a preference that was absent from the reference.

This is why [[papers/dm21|DM21's fractional-charge and fractional-spin training]] is more than a larger dataset. It targets specific failures of the energy surface. The spin condition addresses another difficulty, connected to degenerate states and stretched bonds. Charge and spin constraints should not be collapsed into one generic claim about “physical correctness.”

DM21 still pays for exact-exchange features. That leaves the next question open: can we obtain useful nonlocal information more cheaply?

## From handcrafted neighbourhoods to learned representations

[[papers/cider|CIDER]] chooses nonlocal density summaries whose length scales transform correctly when the electron cloud is compressed. A learned exchange model then works with those physically organized inputs. The [[papers/cider-molecules-and-solids|2024 extension]] tests the strategy in molecules and solids, including semiconductor defects. This gives the cost discussion a concrete materials setting.

[[papers/equivariant-functionals|EG-XC]] compresses density near nuclei and lets the representations communicate through a graph. [[papers/skala|Skala]] uses a fine-to-coarse-to-fine architecture and a much larger accurate training collection. Both show why it can be more productive to improve the representation than merely deepen a network acting on the same local inputs.

The distinction is easy to miss. A local input feature does not force a local final prediction if later layers exchange information across space. Conversely, a large network evaluated independently at each point remains restricted by the information available at that point.

Skala's revised paper reports a strong main-group benchmark result, but some subsets remain difficult and its reported comparisons include a dispersion correction. Its useful lesson is that learned nonlocal information can shift the trade-off. Its evidence does not imply that every class of electronic problem is now solved.

The [[learnings/frontier-2026|2026 frontier]] continues along three related directions: supervising derivatives more directly, extending coverage to surfaces and solids, and representing the density matrix more explicitly. Those recent results are worth following with the same questions we have developed here.

## What would convince me?

A result needs a denominator. “Chemical accuracy” is often shorthand for errors around $1\ \mathrm{kcal\,mol^{-1}}$, but on which quantities? Atomization energies of selected molecules? A particular class of barriers? A weighted average across many tasks? These are different tests.

GMTKN55 is valuable because it contains varied main-group chemistry. Its weighted aggregate, WTMAD-2, prevents some subsets from dominating merely because their energy scales are large. Still, a single average can hide a systematic failure, and a molecular benchmark does not certify performance for solids or strongly correlated materials.

Training overlap matters too. With learned methods, a benchmark can become part of the development process. I want to know what was excluded, whether similar structures remain, and whether entirely different chemistry was tested. A held-out geometry is not the same challenge as a held-out element or bonding regime.

The source of the reference energies matters. Coupled-cluster methods provide excellent references for many single-reference molecules, but CCSD(T) is not universally exact. Basis extrapolation reduces one source of error without removing every other one.

The [[learnings/reading-benchmarks|benchmark-reading detour]] derives WTMAD-2, works through a small weighting example and separates different kinds of generalization. This is part of understanding a paper, not an optional exercise after looking at its best number.

Finally, I want the timing boundary stated. The revised Skala paper's computational-cost experiment evaluates XC energy and potential from a supplied density matrix. That is useful evidence about a component of the calculation. It is not identical to timing a full calculation from an initial guess, including all iterations and any convergence recovery. [Skala, computational details](https://arxiv.org/html/2506.14665v6)

## Where this leaves the investigation

I am not starting with a proposed new functional. I am starting with a more precise problem: **how much of the electronic information needed for accurate chemistry can we represent, learn and evaluate cheaply, while keeping the resulting calculation physically sensible?**

The productive next step is a close reading of the breakthroughs, with a notebook open beside the equations. The [[papers/index|paper pages]] separate the original problem, the method, the reported evidence and the remaining limitations. The [[learnings/index|learning pages]] build the mathematical connections rather than assuming them.

There is room for small experiments later: one-electron cancellation, a dissociation curve, a grid-convergence check, a toy functional with accurate values and poor derivatives. Those would be investigations of specific ideas. Nothing on this page reports a new molecular benchmark or a solved challenge.

For now, a useful test of understanding costs no GPU: explain why a hybrid is nonlocal, derive how exchange scales when a density is compressed, and explain how a model can have accurate energies but poor self-consistent behaviour. If those answers are still hazy, the linked detours are the next step. If they are clear, the newest architectures become much less mysterious.

The [[learnings/figure-sources|figure-source note]] distinguishes reused paper figures, original schematics and reported numerical results. The aim is to make both the explanation and its evidence traceable.

## Sources and scope

- [Discovered Materials: official challenge](https://grandchallenges.discoveredmaterials.com/speed-accuracy-barrier/), checked 27 November 2026. Its leaderboard is provisional; consult the live page for current comparisons.
- Perdew, Burke & Ernzerhof, [PBE](https://doi.org/10.1103/PhysRevLett.77.3865), 1996; Becke, [The role of exact exchange](https://doi.org/10.1063/1.464913), 1993; Sun, Ruzsinszky & Perdew, [SCAN](https://arxiv.org/abs/1504.03028), 2015.
- Kim, Sim & Burke, [Understanding and reducing errors](https://doi.org/10.1103/PhysRevLett.111.073003), 2013.
- Prodan & Kohn, [Nearsightedness](https://arxiv.org/abs/cond-mat/0503124), 2005; Bowler & Miyazaki, [linear-scaling review](https://arxiv.org/abs/1108.5976), 2012.
- Goerigk et al., [GMTKN55](https://doi.org/10.1039/C7CP04913G), 2017. The [authors' dataset and evaluation code](https://github.com/grimme-lab/GMTKN55) are useful companions.
- Li et al., [Kohn–Sham equations as regularizer](https://arxiv.org/abs/2009.08551), 2021; Kirkpatrick et al., [DM21](https://doi.org/10.1126/science.abj6511), 2021.
- Bystrom & Kozinsky, [CIDER](https://doi.org/10.1021/acs.jctc.1c00904), 2022, and [nonlocal exchange](https://arxiv.org/abs/2303.00682), 2024; Luise et al., [Skala](https://arxiv.org/abs/2506.14665), revised 2026.

> [!todo] Things to check
> - Recheck the official challenge protocol before doing a formal comparison; the live requirements can change.
> - Treat the diagrams here as explanations, not measured performance or molecular calculations.
> - Keep electronic energies, free energies and experimental predictions distinct when following the next paper.
