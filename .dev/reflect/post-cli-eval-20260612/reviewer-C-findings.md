# Reviewer C — Design-Contract Completeness + Deviation Classification

**Scope**: HEAD (09f7d487) vs HEAD~1. Lens: delivered-vs-promised against
`.dev/eval-workspaces/cli-eval/design/merge-decision.md` + `candidate-B.md`.
**Adversarial stance**: a clean pass is suspect; every "DELIVERED" was re-Read for evidence.

## Verdict summary

- **Component set**: 100% DELIVERED. All 9 promised new SoT files present + correct.
- **5 invariants**: all 5 DELIVERED (encoded with quotable evidence in SKILL.md and refs).
- **REUSE table**: all 4 reuse targets wired (spec-panel, adversarial, document, evidence-validator).
- **Drift**: 1 trivial (`__init__.py`) — classified **necessary** (package convention, matches peers).
- **Known deviation (COMMANDS.md/ORCHESTRATOR.md not updated)**: classified **necessary** with one
  caveat (cleanup-audit IS registered → precedent is mixed, not unanimous). See C9.
- **Worked-example suites + docs (8 of 17 files)**: NOT in the design component set, but are the
  legitimate *output* of dogfooding the create pipeline → **authorized** (commit declares them).

No regressions. No unmapped drift. One LOW-severity nuance on the registration rationale.

---

## Findings

### C1 — Component set: all 9 promised SoT files DELIVERED
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**:
  - command: `src/superclaude/commands/cli-eval.md:1-2` (`name: cli-eval`), `:67-72` `## Activation` → `Skill sc:cli-eval-protocol`. Matches merge-decision.md:16.
  - skill: `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:1-6` (front-matter `name: sc:cli-eval-protocol`).
  - refs (all 4): `refs/eval-contracts.md`, `refs/create-pipeline.md`, `refs/run-pipeline.md`, `refs/integration-map.md` — all present and substantive (matches merge-decision.md:17).
  - templates (both): `templates/suite-manifest.yaml`, `templates/run-report.md` (matches merge-decision.md:18).
  - 3 agents: `agents/eval-docs-loader.md`, `agents/eval-suite-author.md`, `agents/eval-run-reporter.md` (matches merge-decision.md:19-21).
- **is_real**: yes
- **suggested_fix**: none.

### C2 — Invariant 1 (fresh-context-first Wave 0 via eval-docs-loader) ENCODED
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**: `SKILL.md:46-62` — "Wave 0 — Shared: Mandatory Fresh-Context Load (BOTH pipelines)",
  ":48` "non-negotiable and runs before any create/run action", ":51-52` delegates to `eval-docs-loader`
  via Task, ":56-58` gate: "do NOT substitute a remembered value… If you ever need a flag/field not in
  the digest, re-invoke the loader; never hardcode." Agent itself: `eval-docs-loader.md:20-23`.
- **is_real**: yes. **suggested_fix**: none.

### C3 — Invariant 2 (schema-first done-ness: `eval describe` exit 0) ENCODED + VERIFIED LIVE
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**: `SKILL.md:99-103` W5 "A suite is DONE only when `uv run superclaude eval describe
  --suite <stem>` returns loader exit 0… Do not mark create complete on an unvalidated manifest."
  Author agent `eval-suite-author.md:23-24`, `:51-53`. Reinforced `create-pipeline.md:42-51`.
  **Independently re-tested**: all 3 worked-example suites return `eval describe` exit 0
  (cli_eval_skill_contract, eval_cli_doc_parity, suite_schema_guard), and stem == `name:` for each.
- **is_real**: yes. **suggested_fix**: none.

### C4 — Invariant 3 (NO new CLI flags) ENCODED (4 places)
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**: `SKILL.md:33` "adds NO flags to the `superclaude eval` CLI"; `:217` Will-Not "Add or
  modify any flag on the `superclaude eval` CLI"; command `cli-eval.md:28` "adds **no new flags**";
  `run-pipeline.md:4-5` "It adds NO flags to `superclaude eval`". Selection/monitoring is
  AskUserQuestion + background Bash + Monitor (`SKILL.md:126-151`).
- **is_real**: yes. **suggested_fix**: none.

### C5 — Invariant 4 (surface failures / no silent pass) ENCODED
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**: `SKILL.md:159` "Surface any non-zero exit / FAIL / ERRORED / TIMEOUT as a result —
  never a silent pass. SKIPPED ≠ PASS." Plus the *authoritativeness* extension (`:160-163`, NULL
  executor → NON-AUTHORITATIVE) which EXCEEDS the design (merge-decision.md:47-48 named only
  failure-surfacing; the stubbed-executor honesty layer is an authorized expansion, also present in
  candidate-B.md context). Reporter agent `eval-run-reporter.md:18-28`, `run-report.md:10-16`.
- **is_real**: yes. **suggested_fix**: none. (Note: this is *additive*, not drift — see C8.)

### C6 — Invariant 5 (FR-G5 + --no-pty gotchas owned) ENCODED
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**: `SKILL.md:139-144` (FR-G5 exit-2 empty-HOME workaround + `--no-pty`→SKIPPED);
  `run-pipeline.md:32-44` full gotcha detail incl. the `TMPHOME=$(mktemp -d) HOME=$TMPHOME …`
  workaround; `eval-contracts.md:54-63`. Matches merge-decision.md:49-51 exactly.
- **is_real**: yes. **suggested_fix**: none.

### C7 — REUSE-vs-CREATE table: all reuse targets wired
- **Severity**: info
- **delivered/missing**: DELIVERED
- **Evidence**:
  - **evidence-validator** (design merge-decision.md:27,38) → wired `SKILL.md:178` (delegation table),
    `:109`, `integration-map.md:54-57`. Optional doc-citation re-check, as designed.
  - **/sc:document** (merge-decision.md:26,37) → `SKILL.md:108`, `:177`, `create-pipeline.md:52-57`,
    `integration-map.md:42-52`.
  - **/sc:spec-panel** (create) → `create-pipeline.md:21-24`, `integration-map.md:7-16`.
  - **/sc:adversarial** (create, Mode-A + Mode-B) → `create-pipeline.md:26-33`, `integration-map.md:18-40`.
  All 4 REUSE rows in merge-decision.md's justification table are honored; none reinvented.
- **is_real**: yes. **suggested_fix**: none.

### C8 — DRIFT scan: only `__init__.py` is unlisted; classified NECESSARY
- **Severity**: low
- **deviation-class**: **necessary**
- **file:line**: `src/superclaude/skills/sc-cli-eval-protocol/__init__.py:1` (`# sc-cli-eval skill package`)
- **Evidence**: merge-decision.md:17 lists `SKILL.md + refs/ + templates/` but not `__init__.py`.
  HOWEVER this is an established package convention: 12 of 28 skill dirs carry an `__init__.py`,
  including every recent protocol skill (sc-adversarial-protocol, sc-roadmap-protocol,
  sc-reflect-protocol, sc-cli-portify-protocol, sc-tasklist-protocol, …). It is a 1-line marker, no
  logic. Forced by Python-package convention + documented-by-precedent → **necessary**, not drift.
- **is_real**: yes (it is an unlisted file) but benign. **suggested_fix**: none required; optionally
  note in the design that skill packages carry an `__init__.py`.

### C9 — COMMANDS.md / ORCHESTRATOR.md NOT updated — committer's claim VERIFIED, classify NECESSARY (with caveat)
- **Severity**: low
- **deviation-class**: **necessary** (forced-consistency) — *not* regression, *not* drift
- **file:line**: `src/superclaude/core/COMMANDS.md` (no `cli-eval` entry); `ORCHESTRATOR.md` (no entry).
- **Committer's claim** ("adversarial/roadmap/spec-panel aren't registered either"): **verified by grep**:
  - `COMMANDS.md`: adversarial **0**, roadmap **0**, spec-panel **0**, cli-portify **0**, tasklist **0**,
    reflect **0**, **cli-eval 0**. → Following the dominant precedent (none of the modern skill-commands
    are catalogued in COMMANDS.md). NOT updating is internally consistent → **necessary**.
  - `ORCHESTRATOR.md`: only generic `troubleshoot` routing rows; no per-command registry of
    adversarial/roadmap/spec-panel. → consistent.
  - The design's instruction was conditional: "update COMMANDS.md/ORCHESTRATOR.md **if present**" — the
    registry pattern for these commands is NOT present, so the conditional is correctly not triggered.
- **CAVEAT (the reason this is low-sev, not info)**: the claim is *slightly* overstated. `cleanup-audit`
  IS registered in COMMANDS.md (`:71`, full flag signature, wave-profile). So precedent is **mixed**,
  not unanimous — one peer skill-command (cleanup-audit) chose to register. This does not make the
  omission a regression (no invariant requires it; the majority precedent is non-registration), but the
  rationale "they aren't registered either" should read "the *majority* aren't registered; cleanup-audit
  is the lone exception."
- **is_real**: yes. **suggested_fix**: OPTIONAL (not blocking) — if cataloguing is desired for
  discoverability parity with cleanup-audit, add one COMMANDS.md row for `/sc:cli-eval`. Otherwise the
  omission is defensible under the majority precedent. Recommend documenting the choice explicitly so it
  is not re-litigated.

### C10 — Worked-example suites + docs (8 files) are pipeline OUTPUT, not component-set scope — AUTHORIZED
- **Severity**: info
- **deviation-class**: **authorized**
- **files**: `cli/eval/suites/{cli_eval_skill_contract,eval_cli_doc_parity,suite_schema_guard}.yaml`,
  `cli/eval/suites/README.md`, `cli/eval/suites/cli_eval_skill_contract.yaml`,
  `docs/eval/suites-guide.md`, `cli/eval/suites/README.md`. (8 of 17 changed files.)
- **Evidence**: merge-decision.md does NOT list these as component-set deliverables (grep: none
  mentioned). The commit body explicitly declares them as **worked examples**: "3 suites authored +
  schema-validated (eval describe exit 0) and run in parallel… Docs: suites-guide inventory +
  suites/README table updated." This is the create pipeline (W4-W6) dogfooded on itself — exactly the
  "schema-first + document" path the skill prescribes. All 3 validate live (see C3). → **authorized**
  output, not scope creep.
- **is_real**: yes. **suggested_fix**: none.

---

## Counts

| Class | Count | IDs |
|---|---|---|
| DELIVERED (component/invariant/reuse) | 7 | C1, C2, C3, C4, C5, C6, C7 |
| PARTIAL | 0 | — |
| MISSING | 0 | — |
| necessary | 2 | C8 (__init__.py), C9 (COMMANDS/ORCHESTRATOR omission) |
| authorized | 1 | C10 (worked-example suites/docs) |
| drift | 0 | — |
| regression | 0 | — |

**Severity**: 0 critical · 0 high · 2 low (C8, C9) · 8 info.

## One-liners
- **C1** All 9 SoT files (command + skill + 4 refs + 2 templates + 3 agents) DELIVERED.
- **C2** Invariant 1 fresh-context Wave 0 encoded (SKILL.md:46-62, hardcode-ban :56-58).
- **C3** Invariant 2 schema-first done-ness encoded AND verified live (3 suites `eval describe` exit 0).
- **C4** Invariant 3 no-new-flags encoded in 4 places.
- **C5** Invariant 4 surface-failures encoded + authorized authoritativeness extension.
- **C6** Invariant 5 FR-G5 + --no-pty gotchas owned (SKILL.md:139-144, run-pipeline.md:32-44).
- **C7** All 4 REUSE targets wired (spec-panel, adversarial, document, evidence-validator) — none reinvented.
- **C8** `__init__.py` unlisted but matches 12-peer package convention → necessary, benign.
- **C9** COMMANDS.md/ORCHESTRATOR.md omission VERIFIED & defensible (majority precedent), but claim overstated — cleanup-audit IS registered.
- **C10** 8 suite/doc files are authorized create-pipeline worked-output, not component-set drift.

## COMMANDS.md-registration verdict
**NECESSARY (defensible omission), with a documentation caveat.** The committer's claim is factually
correct for adversarial/roadmap/spec-panel/cli-portify/tasklist/reflect (all 0 hits in COMMANDS.md) —
so not registering `/sc:cli-eval` follows the dominant precedent and the design's "if present"
conditional. It is NOT a regression (no invariant mandates registration) and NOT drift (it is a
reasoned, precedent-aligned choice). The single caveat: `cleanup-audit` IS registered (COMMANDS.md:71),
so the precedent is mixed, not unanimous. Recommend the committer either (a) add a one-line COMMANDS.md
entry for parity with cleanup-audit, or (b) note explicitly that the majority of skill-commands are
deliberately uncatalogued. Either resolves the LOW-severity caveat; neither blocks the commit.
