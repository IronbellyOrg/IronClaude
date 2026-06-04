# BUILD_REQUEST — Remediate Ataraxy-Labs Eval Plan (reflect UC-1 findings)

## Goal
Author an MDTM task file that **patches the planning document**
`.dev/releases/backlog/AtaraxyLabs/merged-requirements.md` to close the 6 HIGH + 5 MED
findings from the `/sc:reflect --mode pre` audit at
`.dev/reflect/pre-ataraxy-eval-plan-20260604015505/REPORT.md`.

## Scope & constraints
- **This is a DOCUMENTATION/planning-spec edit task**, not a code task. The only file
  modified is `merged-requirements.md` (a backlog planning artifact). No `src/superclaude/`
  changes, no `make sync-dev`, no `.claude/` staging.
- Each checklist item maps to exactly one finding and states the concrete edit + an
  acceptance check (a grep/section assertion).
- Preserve the document's existing structure, provenance tags ([V1]/[V2]/[V3]/[MERGE]),
  and frontmatter; these are surgical additions/reconciliations, not a rewrite.
- Output the task file under `.dev/tasks/` (task-builder default). Template: documentation.
- Source-of-truth: the fixes below are authoritative (verified against the real file via
  grep during the audit). Do NOT re-derive them; task-builder may add per-item acceptance
  detail but must not change the intended fix.

## Findings → required edits (each becomes one checklist item)

### HIGH
- **H1 — Reconcile between-tool gating contradiction.** §3 (L95-96) says "weave S0 blocked
  until inspect S4 live + KEEP"; §8.2 (L200) says "inspect KILL does not block weave."
  EDIT: redefine the between-tool gate to require the prior tool to reach a **terminal
  state (KEEP-and-live OR explicit KILL)**, and add one sentence stating weave depends on
  `sem-core`, not inspect — so an inspect KILL lets weave's S0 proceed directly.
  ACCEPT: §3 and §8.2 no longer contradict; both reference the terminal-state rule.
- **H2 — Add owner / decision authority / tie-break.** EDIT: add an `Owner` field to the §5
  scorecard template and a short "Decision Authority & Tie-Break" subsection (who calls
  keep/kill; what happens on a borderline/ambiguous gate). Restore V2's decision-record
  `Owner:` field (variant-2 §10.5).
  ACCEPT: `grep -i owner merged-requirements.md` returns a real assignment; tie-break rule present.
- **H3 — Add Security & Data-Handling section.** EDIT: new section covering (a) inspect
  `review` pipes changed entities to external LLM providers — egress policy + provider
  retention stance; (b) tools read the whole repo — secret-scrubbing before any external
  call; (c) routing private-fork code to third-party endpoints — explicit allow/deny.
  ACCEPT: `grep -i "security\|egress\|secret" merged-requirements.md` returns the new section.
- **H4 — Specify solo-operator blind adjudication.** EDIT: §7 must state HOW a single
  operator blinds judging — randomized tool naming + an LLM adjudicator with stripped
  provenance (reflect's own evidence-validator pattern), OR explicitly staff + budget human
  adjudication. Remove the implicit assumption of a multi-person panel.
  ACCEPT: §7 names a concrete solo-blinding mechanism.
- **H5 — Make corpus inventory the first Phase-0 action + specify synthetic backfill.**
  EDIT: G0-1 must (a) require an actual fork PR/merge-count inventory as the first action,
  and (b) specify the synthetic-backfill construction (seed from the §11 curated-defect
  list) for when counts fall short. Note the corpus is NOT empty (~30 merges exist).
  ACCEPT: G0-1 has a concrete inventory step + a defined backfill method.
- **H6 — Restore concrete, runnable harness artifacts + runner contract.** EDIT: §4 must
  include (a) the runner I/O contract (input fields → normalized JSON output schema), and
  (b) restore the concrete buildable artifacts compressed in the merge — V3's bash latency
  harness and the install matrix. The Phase-0 1-2 day estimate must reference these as the
  deliverables.
  ACCEPT: §4 contains a runner contract + references the concrete harness artifacts.

### MED
- **M1 — Give the generalization appendix a skeleton.** Add at least a scenario inventory +
  thresholds for the multi-repo/multi-language breadth (honors the user's "broad variety of
  scenarios"), or explicitly rescope "broad" to native-first with a stated rationale.
- **M2 — Define the token-vs-Auggie isolation method.** Specify how to separate Auggie's
  token contribution from the surrounding multi-wave prompt so "≥30% vs Auggie" is measurable.
- **M3 — Define sample-size confidence interpolation.** Add the banding for counts between
  the 5PR/3merge (shadow) and 20PR/10merge (graduate) tiers (e.g., 12 PRs → which label).
- **M4 — Clarify weave's value-surface sizing.** State that weave acts on Python only
  (`.md` correctly falls back to git — not a measurability flaw) and add a Phase-0 check that
  enough Python worktree merges exist to populate the gate.
- **M5 — Elevate the Markdown-ceiling assumption + add a tie-break resolver.** Promote the
  `.md`-substrate risk (most-probable sem-KILL → CP-1 archive) to a first-class plan
  assumption; add the borderline-confidence resolver referenced in H2.

## Post-task gate (for the task file's closing note)
After the operator runs `/task` on the produced file, they re-run:
`/sc:reflect --mode pre @.dev/releases/backlog/AtaraxyLabs/merged-requirements.md`
to confirm the HIGH findings are closed and coverage/grade improved.
