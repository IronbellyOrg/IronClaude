# D-0108 — Notes

## Design notes

1. **Why the README is the authoritative source, not `decisions.md`.**
   DOC-OQ6's AC text is literal: *"cli/eval/suites/README.md records
   naming convention; `quick.yaml` plan recorded as follow-up."* The
   roadmap names the README as the satisfaction site. `decisions.md`
   §"DOC-OQ6 Closure" is the ADR-log entry that closes OQ-6 against
   the OPS-001 §B audit trail, but it points *to* the README rather
   than duplicating it. A future suite author opens the directory,
   reads the README, and learns the rules; they should not have to
   chase an ADR file across a sibling release tree to author a
   manifest. The README is the working surface; the ADR is the
   change-log entry.

2. **Why ratify a convention when only one manifest exists at v1
   ship.** Three options were considered:
   (a) defer the convention to whichever release lands the second
       manifest (`quick.yaml` or otherwise);
   (b) ratify the convention now, with `real.yaml` as the worked
       example, even though no second manifest exists;
   (c) ratify a minimal subset (just §1 the extension rule) and
       leave the rest to ad-hoc judgement.
   Option (a) was rejected because DOC-OQ6 names the README as a
   v1 deliverable; a future-tense "we'll write this when we need
   it" closes nothing. Option (c) was rejected because the §3
   stem-equals-`name:` rule is the load-bearing one — without it,
   `--suite <token>` resolution is the "trap" described in the
   README §3 paragraph, and a future author surprised by it would
   re-open OQ-6 immediately. Option (b) — ratifying the full
   convention with `real.yaml` as the worked example — keeps the
   surface fenced before the second manifest lands. The cost is
   five rules of prose; the benefit is that the next suite author
   does not have to re-derive them from the loader source.

3. **Why `quick.yaml` is deferred with a documented trigger rather
   than (a) shipped now, (b) deleted from the design, or (c) left
   as an unscoped wish.** Three options were considered:
   (a) ship a curated `quick` subset alongside `real.yaml` at v1;
   (b) excise `quick.yaml` from the design entirely and rely only
       on `--eval <id>` for subsetting;
   (c) record `quick.yaml` as a deferred follow-up with a shape +
       trigger contract.
   Option (a) was rejected because the v1 eval roster (E1..E15) is
   frozen at T05.01 (OQ-2 resolution); landing a curated subset
   requires choosing 3-5 of the 15, and that choice has no
   demand-signal yet. Splitting maintenance across two manifests
   without operator demand also blurs the SC2 / SC4 coverage and
   LOC budgets recorded against `real.yaml` only. Option (b) was
   rejected because the R6 risk-mitigation row (roadmap row 339)
   explicitly names `quick.yaml` as the documented fast-loop path
   if `real.yaml` walltime exceeds the 10-minute adoption ceiling
   on reference hardware; excising it would lose that hedge.
   Option (c) — record the shape and the trigger — preserves the
   hedge without committing v1 work. The contract in the README
   §"Planned follow-up" is sufficiently specific that when the
   trigger materialises, the suite owner has the spec without
   needing a new ADR.

4. **Why the convention is documentation-layered, not schema-layered.**
   `suite.schema.json` only requires `name:` to be a non-empty
   string; it does not constrain the charset or casing. Encoding
   the snake_case stem rule into the schema was considered and
   rejected because (i) the schema validates the *body* of a
   manifest, not its on-disk filename, so a schema-level rule
   cannot enforce rule §3 (stem == `name:`) without a custom
   loader-side check; (ii) the existing loader already enforces
   rule §1 (the `*.yaml` glob) by exclusion, so schema duplication
   adds nothing; (iii) keeping the schema layer suite-agnostic
   means `quick.yaml` validates against the same file as
   `real.yaml` with zero schema edits — preserved as an explicit
   property in the README §"What's NOT in scope for the follow-up".
   The convention is therefore documentation-layered: humans read
   the README before authoring a manifest, and the loader silently
   rejects anything that violates rule §1. The other rules (§2-§5)
   are convention-only.

5. **Why `real.yaml` is treated as conforming without an explicit
   migration step.** A pre-check against the rules:
   - Rule §1 (`*.yaml`): satisfied — extension is `.yaml`.
   - Rule §2 (`[a-z][a-z0-9_]*`): satisfied — stem `real` matches.
   - Rule §3 (stem == `name:`): satisfied — `real.yaml` line 1
     reads `name: real`.
   - Rule §4 (uniqueness): satisfied — it is the only manifest.
   - Rule §5 (reserved stems): satisfied — `real` is neither
     `suite` nor leading-underscore.
   No migration is required; this is recorded explicitly in
   `artifacts/D-0108/spec.md` §"Out of scope for T06.04" to
   foreclose a future maintainer asking whether `real.yaml`
   itself triggers any rename.

6. **Why the R8 update note sits in OPS-001 §B rather than
   inserting OQ-6 into the §B table.** OPS-001 §B was authored
   against M1-scoped open questions (OQ-1, OQ-3, OQ-7, OQ-8,
   OQ-10). OQ-6 was opened against M5 (roadmap row 332), not M1.
   Editing the §B table to add OQ-6 would (a) misrepresent its
   provenance and (b) drift the §B table from its T01.25 charter.
   The R8 update note is the lower-disruption path: it records
   OQ-6's RESOLVED status, names its actual provenance ("opened
   against M5 not M1; roadmap row 332"), and cross-references
   §"DOC-OQ6 Closure" for the full rationale. The §B table itself
   is untouched.

7. **What changes if `quick.yaml` lands later.** No part of this
   ADR is invalidated. The README §"Planned follow-up" is the
   implementation contract; the convention §"Filename rules"
   applies verbatim to the new manifest. The follow-up task
   amends the README's "What lives in this directory" inventory
   table to add the `quick.yaml` row, and may add a one-line
   `Outcome:` to the DOC-OQ6 closure section recording the
   landing date — but no new ADR is required.

8. **What changes if the rules need amendment later.** A new ADR
   row (R9+) records the amendment; the README is updated to
   match; OQ-6 stays RESOLVED but the §"Filename rules" diff is
   tracked through the same revision-log mechanism as the rest
   of `decisions.md`. The rules are forward-amendable without
   re-opening OQ-6.

## Edge cases considered

- **What if a future maintainer drops a `.yml` (no `a`) manifest
  by mistake.** Loader silently ignores it; `eval list` does not
  surface the file; `eval doctor` does not flag it. The README §1
  paragraph names this explicitly as a one-spelling rule with the
  loader-glob citation; the maintainer's next debugging step is
  re-reading the README. No code change required.
- **What if a future suite has stem == `name:` but the stem is
  upper-case (e.g., `Quick.yaml` with `name: Quick`).** Rule §2
  fails (leading upper-case). The loader still finds the file
  (the glob is case-sensitive on Linux but case-insensitive on
  macOS / Windows; the glob itself uses `*.yaml` literal extension
  match). Rule §2 is convention-only; the loader does not enforce
  it. The README's recommended remedy is rename to lower-case;
  the maintainer learns this from the §"Authoring checklist".
- **What if two manifests have the same stem on a
  case-insensitive filesystem (`real.yaml` + `Real.yaml`).** Glob
  returns both; sorted deterministically by filename; loader
  errors on duplicate `name:` when both validate. Rule §4
  pre-fences this — convention-only enforcement, but the failure
  surface is loud (schema-validation error on the duplicate
  `name:`), so the maintainer sees the problem at `eval list`
  time.
- **What if `quick.yaml` lands with `name: quick_smoke` instead
  of `name: quick`.** Rule §3 violated. Loader still resolves
  `--suite quick_smoke` (rule (c)) but `--suite quick` (rule (b))
  also works because the stem matches. Operators reaching for
  the stem succeed; operators reaching for the schema `name` also
  succeed; but `eval list` prints `quick_smoke` while the file is
  called `quick.yaml`. The README §3 paragraph names this
  exact trap.
- **What if a contributor proposes loosening the convention
  (e.g., to allow hyphens in stems).** The proposal is filed as
  a new ADR; the README is amended; OQ-6 stays RESOLVED. The
  convention is amendable but the amendment is tracked through
  the same ADR mechanism as the original.
- **What if a future RF task touches the README without an ADR
  update.** The README header names `decisions.md §"DOC-OQ6
  Closure"` as the source-of-truth ADR; a maintainer reading the
  README sees the cross-reference and routes any meaningful
  convention edit through a new ADR row. A pure typo / formatting
  edit does not require an ADR.

## Validation steps performed

1. Read `roadmap.md` row 351 (DOC-OQ6 / R-107) to confirm the
   exact AC text: *"cli/eval/suites/README.md records naming
   convention; `quick.yaml` plan recorded as follow-up."* The
   README has both halves; the ADR closure section in
   `decisions.md` points to the README for both.
2. Read `roadmap.md` row 332 (OQ-6 M5 Open Question) and row 339
   (R6 risk mitigation, original `quick.yaml` surfacing) to
   confirm provenance of OQ-6 (M5, not M1) and the original
   surfacing of the `quick.yaml` plan.
3. Read `src/superclaude/cli/eval/commands.py:591-606`
   (`discover_suite_manifests`) and `:1008-1044`
   (`resolve_suite_manifest`) to confirm the loader behaviour the
   README documents. The `*.yaml` glob is at line 606; the
   stem-resolution branch is at lines 1030-1032; both line ranges
   are cited verbatim in the README and in `decisions.md` §"DOC-OQ6
   Closure" §Context.
4. Read `src/superclaude/cli/eval/suites/suite.schema.json` to
   confirm the schema only requires `name:` as a non-empty string
   with no charset / casing constraint. The README §3 paragraph
   names the schema explicitly as the second half of the rule.
5. Read `src/superclaude/cli/eval/suites/real.yaml` line 1 to
   confirm `name: real` matches the stem — i.e., `real.yaml`
   already satisfies the convention with no migration step.
6. Confirmed the §"DOC-OQ6 Closure" section in `decisions.md`
   follows the structural template of §"DOC-OQ7 Closure",
   §"DOC-OQ8 Closure", and §"DOC-OQ9 Closure" (Context →
   Decision → Rationale → Closure → Cross-references →
   Consequences). The R8 revision-log entry mirrors the R5 / R6 /
   R7 format.
7. Confirmed the R8 update note in §B OPS-001 names OQ-6's M5
   provenance explicitly so a future reader does not expect to
   find OQ-6 in the §B table itself.
