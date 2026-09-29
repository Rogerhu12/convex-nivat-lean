import Mathlib

/-! An independent statement of the two-dimensional convex Nivat theorem.
This file depends only on mathlib and contains no proof imported from the
Nivat formalization. The release audit proves this statement separately. -/

namespace ConvexNivatStatement

universe u

abbrev Site := ℤ × ℤ

def latticePoint (z : Site) : ℝ × ℝ := ((z.1 : ℝ), (z.2 : ℝ))

/-- Exactly the lattice points in the real convex hull of the finite window. -/
def IsConvexLatticeWindow (S : Finset Site) : Prop :=
  latticePoint ⁻¹' convexHull ℝ (latticePoint '' (S : Set Site)) = (S : Set Site)

/-- Restrict an actual translate of the colouring to the finite window. -/
def pattern {A : Type*} (θ : Site → A) (S : Finset Site) (u : Site) : S → A :=
  fun s => θ (u + s)

/-- Only patterns attained by actual integer translates are counted. -/
def occurringPatterns {A : Type*} (θ : Site → A) (S : Finset Site) : Set (S → A) :=
  Set.range (pattern θ S)

noncomputable def complexity {A : Type*} (θ : Site → A) (S : Finset Site) : ℕ :=
  Nat.card (occurringPatterns θ S)

/-- A genuine nonzero full-plane period. -/
def HasNonzeroPeriod {A : Type*} (θ : Site → A) : Prop :=
  ∃ h : Site, h ≠ 0 ∧ ∀ u : Site, θ (u + h) = θ u

/-- The standalone problem statement, independent of implementation names. -/
def ConvexNivat : Prop :=
  ∀ (A : Type u) [Fintype A] (θ : Site → A) (S : Finset Site),
    S.Nonempty → IsConvexLatticeWindow S →
      complexity θ S ≤ S.card → HasNonzeroPeriod θ

end ConvexNivatStatement
