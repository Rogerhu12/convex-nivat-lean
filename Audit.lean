import NivatTrial
import Statements
import Lean.Util.CollectAxioms

/-! Compare the independent mathlib-only target with the project's actual
definitions, then audit every imported project declaration and the final
standalone conclusion for additional axioms. -/

namespace ReleaseAudit

open ConvexNivatStatement

theorem latticePoint_eq_project (z : Site) :
    latticePoint z = NivatTrial.Zonotope.embed z := rfl

theorem convexWindow_iff_project (S : Finset Site) :
    IsConvexLatticeWindow S ↔ NivatTrial.LatticePolygon.IsLatticeConvex S := by
  rw [NivatTrial.LatticePolygon.isLatticeConvex_iff_preimage]
  rfl

theorem pattern_eq_project {A : Type*} (θ : Site → A)
    (S : Finset Site) (u : Site) :
    pattern θ S u = NivatTrial.patternAt θ S u := rfl

theorem complexity_eq_project {A : Type*} [Fintype A]
    (θ : Site → A) (S : Finset Site) :
    complexity θ S = NivatTrial.patternComplexity θ S := rfl

theorem period_iff_project {A : Type*} (θ : Site → A) :
    HasNonzeroPeriod θ ↔ NivatTrial.Periodicity.IsPeriodic θ := Iff.rfl

/-- The independent statement follows from the project's final theorem,
with the actual convexity, pattern count and period definitions bridged. -/
theorem convex_nivat : ConvexNivat := by
  intro A _ θ S hne hconv hlow
  have hS : NivatTrial.LatticePolygon.IsLatticeConvex S :=
    (convexWindow_iff_project S).mp hconv
  rw [complexity_eq_project] at hlow
  exact (period_iff_project θ).mpr
    (NivatTrial.TheoremB.periodic_of_low_convex_complexity θ S hne hS hlow)

end ReleaseAudit

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut checked : Nat := 0
  let mut theorems : Nat := 0
  for (name, info) in env.constants do
    if name.toString.startsWith "NivatTrial." ||
        name.toString.startsWith "ConvexNivatStatement." ||
        name.toString.startsWith "ReleaseAudit." then
      match info with
      | .axiomInfo _ => throwError "Release axiom: {name}"
      | .thmInfo _ => theorems := theorems + 1
      | _ => pure ()
      let axioms ← collectAxioms name
      for ax in axioms do
        unless ax == ``propext || ax == ``Classical.choice || ax == ``Quot.sound do
          throwError "Unexpected transitive axiom in {name}: {ax}"
      checked := checked + 1
  if checked == 0 || theorems == 0 then
    throwError "No release declarations were audited"
  logInfo m!"PASS: {checked} release declarations, including {theorems} theorems. All transitive axioms are among propext, Classical.choice, Quot.sound."

#check @ConvexNivatStatement.ConvexNivat
#check @ReleaseAudit.convex_nivat
#print axioms ReleaseAudit.convex_nivat
#print axioms NivatTrial.TheoremB.periodic_of_low_convex_complexity
