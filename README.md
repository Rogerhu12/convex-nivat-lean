# Convex Nivat — Lean formalization

This private repository contains the Lean proof of the convex Nivat statement in Theorem B (Theorem 8.18) of the supplied Apex Intelligence manuscript, together with the proof dependencies used by that endpoint.

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

`lean-toolchain` pins Lean 4.33.0. `lakefile.toml` and `lake-manifest.json` pin mathlib to `db584cd6d46c92f209a44c0f1c829460d327499d` and record its transitive dependencies. These commands do not depend on the original author's Windows cache paths.

`Statements.lean` states the mathematical target using Mathlib alone, including the actual pattern set, lattice-convexity, and a nonzero period. `Audit.lean` checks the connection from the proof to that independent statement and checks transitive axioms of the project declarations.

## CI and evidence

The GitHub Actions workflow builds the project on a fresh Ubuntu runner, runs the source checker and its negative tests, and checks the independent statement and axioms. It retrieves upstream mathematical dependency caches; it does not restore cached project proofs. Build logs and audit output are stored as private workflow artifacts.

CI status is authoritative for the exact commit shown by the workflow run. The original local audit is retained separately in `evidence/`: 219 mathematical modules, 221 checks, 3,777 project declarations including 3,176 theorem declarations, with stable source hashes and only the three standard axioms. This historical local result is not a substitute for a completed remote workflow run.

`source-provenance.json` records the original hashes of all 219 mathematical source files. They were copied byte-for-byte from the successful local snapshot. `.gitattributes` preserves those bytes across Windows and Linux checkouts. The final mathematical source closure has 27,091 nonblank, noncomment lines (32,107 total lines). New release checks, the independent statement, scripts, and Mathlib are outside that historical count. Exploratory modules outside the terminal closure are omitted.

## Scope and attribution

This is a formalization contribution based on the supplied candidate paper and its cited mathematics, not a claim to have independently discovered the original theorem. It proves the final target through a partly reorganized proof. It does not certify each original lemma verbatim or all results in every cited paper.

In particular, the Colle Case 1 implementation fixes the original aperiodic configuration, merges finite long-faced agreement windows, takes their directed union, and reflects the resulting boundary problem into the already proved second-boundary argument. See `PROOF_MAP.md` and the source-correspondence reviews for the exact scope.

Implementation and internal source reviews were produced using Codex agents, including GPT-6-sol / xhigh subagents, under the submitter's direction. Internal AI cross-checks and successful compilation do not constitute independent third-party mathematical peer review. The independent statement audit makes the intended endpoint explicit; experts can inspect the statement and replay the proof.

Historical documentation copied from development includes references to earlier snapshots and omitted exploration files. Current repository contents, `source-provenance.json`, the final local evidence, and the actual CI run identify this release precisely.
