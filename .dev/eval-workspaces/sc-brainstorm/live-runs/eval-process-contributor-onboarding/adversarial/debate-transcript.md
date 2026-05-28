---
phase: debate
variants: 3
convergence_target: 0.75
created: 2026-05-27T00:00:00Z
---

# Adversarial Debate Transcript — Contributor Onboarding

## Round 1 — Opening Critiques

### Variant 1 (Scribe) critiques Variant 2 (PM)

- "Cohort threads risk being performative without sustained newcomer volume. A 4-volunteer minimum is a real gate; will OSS rosters actually sustain that?"
- "Auto-comment on first PRs is good, but without the QUICKSTART doc it points to, the action is pointing at vapor."

### Variant 1 (Scribe) critiques Variant 3 (Architect)

- "`make onboard` is great until it fails — and then docs are the fallback. You can't tooling your way out of needing a glossary."
- "Devcontainer is a 30%-of-contributors solution; what about the other 70% on local machines?"

### Variant 2 (PM) critiques Variant 1 (Scribe)

- "QUICKSTART without a maintainer SLA leaves first PRs sitting for two weeks. Docs without process = docs nobody trusts."
- "Worked-example PR is great content, but maintenance burden is real. Who updates it when the skill template changes?"

### Variant 2 (PM) critiques Variant 3 (Architect)

- "`superclaude doctor --contributor` is excellent but a tool nobody runs is shelfware. Needs PR-template prompting to actually surface."
- "Codespaces lock-in: what about contributors who refuse a Microsoft IDE? Need a local-friendly path too."

### Variant 3 (Architect) critiques Variant 1 (Scribe)

- "Failure-mode appendix is reactive. By the time someone reads it, they've already hit the wall. The architectural fix is to make the hook output self-explanatory at the moment of failure."
- "Three-doc rule risks adding more docs to read before reading any docs. Onboarding paradox."

### Variant 3 (Architect) critiques Variant 2 (PM)

- "Cohort cadence is heavy ceremony for a 3-person-a-month newcomer pipeline. Process scales with volume; we don't have the volume."
- "Maintainer-of-the-week rotation assumes a maintainer pool large enough to rotate. We need to verify that assumption."

## Round 2 — Steelmanning + Synthesis Probes

### Where do all three agree?

- The first 30 minutes are the highest-leverage window.
- Pre-commit hook failures are a known pain point with broad agreement on remediation surfaces.
- `good-first-issue` curation matters in all three plans (implicitly in scribe's glossary, explicitly in PM, and via doctor in architect).
- Async-first is non-negotiable.

### Where do they conflict?

- Scribe favors **explanation**; Architect favors **prevention**; PM favors **escalation paths**.
- Scribe's QUICKSTART overlaps but doesn't conflict with Architect's `make onboard` — they can compose.
- PM's cohort rituals tension with Architect's "process scales with volume" critique. Probably defer cohort threads until volume justifies them.
- All three want issue-template improvements but for different reasons (Scribe = link to docs; PM = ping shepherd; Architect = run doctor).

### Round-2 synthesis question

"What is the minimum set of changes that yields measurable improvement in one sprint without depending on volume the project doesn't yet have?"

- Tooling fixes (Architect) are independent of volume.
- Docs fixes (Scribe) are independent of volume.
- Process fixes (PM) need volume — pick the lightweight subset (PR template, shepherd) and defer the rest.

## Round 3 — Convergence Probe

### Convergence assessment

- Agreement on: tooling + docs are sprint-ship-able now; PR template improvements compose cleanly; hook UX is the highest-impact single fix.
- Tension on: cohort cadence (defer), worked-example PR (include but mark as stretch), maintainer-of-the-week (downgrade to "shepherd availability" rather than formal rotation).
- Convergence score estimate: **0.82** — high agreement on the must-have set, low-stakes disagreement on optional rituals.

### Unresolved conflicts

- Whether to launch cohort threads in sprint 1 or defer to sprint 2 (PM wants in, Architect+Scribe want defer).
- Whether worked-example skill PR is a sprint-1 deliverable or a sprint-2 follow-up (Scribe wants in, PM+Architect want defer).

Both are scope decisions, not architectural disagreements — merge-log will resolve by deferring both to a Phase-2 sprint while keeping the foundational fixes in Phase-1.
