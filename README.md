# Convex Nivat — Lean formalization

This private repository contains a Lean formalization of the convex Nivat statement in Theorem B (Theorem 8.18) of a candidate manuscript hosted by Apex Intelligence for public verification, together with the proof dependencies used by that endpoint.

## Manuscript and verification campaign

The source manuscript is **Paper 03**, [*The convex Nivat conjecture: a complexity lower bound for star configurations, and a reduction from low convex complexity to star configurations*](https://math.apexin.net/), in the **Apex Math candidate-proof verification campaign** organized by **Apex Intelligence (超衍智能)**. The campaign announcement is dated **2026-09-29**. Its other two candidate arguments concern incompressible Seifert surface complexes and the genus-two case of Souto's problem.

The platform presents the manuscripts as AI-proposed candidate proofs and invites independent mathematical scrutiny. Its announcement expressly leaves their correctness open and solicits gaps, counterexamples, verification of key steps, formalization results, repairs, and improvements. This repository was developed in that verification context.

The announced prize pool totals **RMB 100,000**: RMB 90,000 for nine professional awards across the three papers and RMB 10,000 for community awards. Each paper has separate categories for a major gap (重大漏洞), key verification (关键验证), and a breakthrough contribution (突破贡献), with RMB 10,000 allocated to each professional award. The contribution documented here is intended for consideration as **key verification (关键验证)**: an executable formal proof of the final convex Nivat statement, its required dependencies, and an explicit connection to a separately stated mathematical target. The organizer's expert review and award decisions are separate from the technical checks recorded here.

Campaign details in this section follow the supplied announcement dated 2026-09-29. See the [official announcement and rules](https://math.apexin.net/announcement) for submission requirements, expert review, deadlines, and current updates. This repository remains private; reviewers need repository access to inspect its source and CI evidence.

## Mathematical target

For a configuration `ξ : ℤ × ℤ → A` over a finite alphabet and a nonempty finite lattice-convex set `S`, if the number of actual translated `S`-patterns is at most `S.card`, then `ξ` has a nonzero global integer period.

The endpoint is `NivatTrial.TheoremB.periodic_of_low_convex_complexity`. It has no external-result parameter. The needed integer decomposition and regional results are proved in the project. Only Lean's standard `propext`, `Classical.choice`, and `Quot.sound` are allowed by the axiom audit.

## Reproduce

Install [elan](https://github.com/leanprover/elan), Git and Python 3, then run from the repository root:

```sh
python3 check.py
python3 -m unittest discover -s tests -v
lake exe cache get
lake build
lake env lean Audit.lean
```

`lean-toolchain` pins Lean 4.33.0. `lakefile.toml` and `lake-manifest.json` pin mathlib to `db584cd6d46c92f209a44c0f1c829460d327499d` and record its transitive dependencies. These commands do not depend on the development machine's Windows cache paths.

`Statements.lean` states the mathematical target using Mathlib alone, including the actual pattern set, lattice-convexity, and a nonzero period. `Audit.lean` checks the connection from the proof to that independent statement and checks transitive axioms of the project declarations.

## CI and evidence

The GitHub Actions workflow builds the project on a fresh Ubuntu runner, runs the source checker and its negative tests, and checks the independent statement and axioms. It retrieves upstream mathematical dependency caches; it does not restore cached project proofs. Build logs and audit output are stored as private workflow artifacts.

The first successful remote verification completed on **2026-09-30**: [CI run 36665504290](https://github.com/Rogerhu12/convex-nivat-lean/actions/runs/36665504290) checked commit [`5674e77aabc7235b733b7111ad71c18b3fe5c74b`](https://github.com/Rogerhu12/convex-nivat-lean/commit/5674e77aabc7235b733b7111ad71c18b3fe5c74b). The fresh Linux build, all five checker tests, source provenance checks, and independent statement audit passed. The axiom audit covered **3,791 release declarations, including 3,182 theorem declarations**, allowing only `propext`, `Classical.choice`, and `Quot.sound`. This is a completed technical verification record for that commit; campaign expert review is a separate process.

CI status is authoritative for the exact commit shown by the workflow run. The original local audit is retained separately in `evidence/`: 219 mathematical modules, 221 checks, 3,777 project declarations including 3,176 theorem declarations, with stable source hashes and only the three standard axioms. This historical local result is not a substitute for a completed remote workflow run.

`source-provenance.json` records the original hashes of all 219 mathematical source files. They were copied byte-for-byte from the successful local snapshot. `.gitattributes` preserves those bytes across Windows and Linux checkouts. The final mathematical source closure has 27,091 nonblank, noncomment lines (32,107 total lines). New release checks, the independent statement, scripts, and Mathlib are outside that historical count. Exploratory modules outside the terminal closure are omitted.

## Scope and attribution

The candidate argument and prior mathematical results are credited to the manuscript's authors and its cited literature; the project's source-correspondence documents record how those arguments are used. The contribution of this repository is the Lean implementation, the documented adaptations of the proof, and reproducible verification materials. Rights in the original candidate manuscript remain with its respective rightsholders, as stated in the campaign announcement.

This is a formalization contribution based on the supplied candidate paper and its cited mathematics, not a claim to have independently discovered the original theorem. It proves the final target through a partly reorganized proof. It does not certify each original lemma verbatim or all results in every cited paper.

In particular, the Colle Case 1 implementation fixes the original aperiodic configuration, merges finite long-faced agreement windows, takes their directed union, and reflects the resulting boundary problem into the already proved second-boundary argument. See `PROOF_MAP.md` and the source-correspondence reviews for the exact scope.

Implementation and internal source reviews were produced using Codex agents, including GPT-6-sol / xhigh subagents, under the repository maintainer's direction. Internal AI cross-checks and successful compilation do not constitute independent third-party mathematical peer review. The independent statement audit makes the intended endpoint explicit; experts can inspect the statement and replay the proof.

Historical documentation copied from development includes references to earlier snapshots and omitted exploration files. Current repository contents, `source-provenance.json`, the final local evidence, and the actual CI run identify this release precisely.
