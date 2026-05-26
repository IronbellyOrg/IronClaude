# D-0010 — Spec: B-10 packaging deferral for `sc-validate-roadmap-protocol`

**Task:** T04.01
**Roadmap Item:** R-010
**Decision:** Defer (Option 2 / defer per `design-decision.md:40`).

## Decision

For this release, the packaging shape of `sc-validate-roadmap-protocol`
remains **unchanged**. The skill continues to ship as a single
`SKILL.md` file under `src/superclaude/skills/sc-validate-roadmap-protocol/`
with no `refs/`, `rules/`, or `templates/` subdirectories.

No `refs/`, `rules/`, or `templates/` split is authorized by B-10 in
this release.

## Revisit condition

Revisit only if B-9 follow-up review finds measured load or token pain.

Specifically: a structure-only factor of `SKILL.md` into `refs/` is only
warranted if a future review surfaces empirical evidence that the
single-file shape is causing measurable cost — e.g., load-time tokens,
on-disk size, or maintenance friction — that outweighs the cost and
risk of factoring. Absent that evidence, no factoring work is to be
performed under B-10.

## Scope boundary

- **In scope for this release (B-9, handled by T03.01/D-0009):**
  Relationship-to-CLI header + crosswalk inserted into `SKILL.md`;
  deep-validation protocol preserved intentionally.
- **Out of scope for this release (B-10, this artifact):** any
  `refs/`-style decomposition, content migration, or structural
  refactor of `SKILL.md`.

## Source of truth

- `.dev/releases/current/roadmap-cli-skill-converge/design-decision.md:40`
  — B-10 = Option 2 / defer.
- `.dev/releases/current/roadmap-cli-skill-converge/design-decision.md:54`
  — "Leave B-10 unchanged unless B-9 follow-up review finds measured
  load/token pain."
- `.dev/releases/current/roadmap-cli-skill-converge/solutions.md:363`
  — "Solution 2 — defer until B-9 design is settled; structure-only
  refactor is premature."
- `.dev/releases/current/roadmap-cli-skill-converge/release-scope.md:166`
  — Option 2 update: "Leave as-is. Single-file packaging is
  functional."
