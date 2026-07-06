---
title: Remediation Spec — PR #197 (rf-harness sync) review findings
type: architecture
format: spec
source_review: .dev/reviews/pr-197-20260620223934/REVIEW.md
target_pr: https://github.com/IronbellyOrg/IronClaude/pull/197
target_branch: feat/rf-harness-sync
target_head_at_review: a3f3f0cb8aa7b57b83c70614dde96168ddbcfe90
generated_by: /sc:design (remediation chain Phase A)
date: 2026-06-21
---

# Remediation Specification — PR #197

## Purpose

Translate the `/sc:auggie-review` findings on PR #197 into an executable, evidence-backed
remediation plan. Source of truth for every requirement below is
`.dev/reviews/pr-197-20260620223934/REVIEW.md` and the grounded line citations in
`audit.log`. All edits land under `src/superclaude/` and MUST be followed by
`make sync-dev` + `make verify-sync` (the `.claude/` mirror is gitignored sync output).

## Scope & ground rules

- **Apply on the PR branch** `feat/rf-harness-sync`, in an isolated worktree
  (`git worktree add .dev/worktrees/pr197-remediation feat/rf-harness-sync`) — never on
  `master`, and never sharing the index with another session.
- **Source-of-truth discipline**: edit `src/superclaude/…` only; run `make sync-dev` after.
  Do NOT stage any `.claude/` path.
- **Two findings block merge** (R1, R2). R3–R5 are cheap correctness/clarity fixes worth
  bundling. R6 is explicitly out of scope (pre-existing). Nits optional.
- **R2 contains a human-decision gate** — see HD-1. The task MUST NOT auto-pick the design
  resolution; it applies the always-safe disclosure and HALTS for RyanW on the default-mode
  question.

---

## R1 — [HIGH, blocks merge] Revert the Tavily MCP tool-id rename (hyphen is canonical)

**Finding**: REVIEW.md H1. The 8 `rf-*` agents were renamed to the underscore form
`mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract`, which does NOT resolve.
The resolving / canonical id in this harness is the **hyphen** form
`mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` (the literal registered tool
id; every other Tavily consumer on the branch keeps the hyphen).

**Change**: In each of the 8 files below, replace every occurrence of
`mcp__tavily__tavily_search` → `mcp__tavily__tavily-search` and
`mcp__tavily__tavily_extract` → `mcp__tavily__tavily-extract`
(frontmatter `tools:` lists **and** all body prose / examples). This is a pure mechanical
reversal of the PR's rename; no other edits.

**Affected files** (`src/superclaude/agents/`):
`rf-analyst.md`, `rf-assembler.md`, `rf-qa.md`, `rf-qa-qualitative.md`,
`rf-task-builder.md`, `rf-task-executor.md`, `rf-task-researcher.md`, `rf-team-lead.md`.

**Acceptance criteria**:
1. `git grep -nE 'mcp__tavily__tavily_(search|extract)' src/superclaude/agents/` returns **zero** matches. (NOTE: the grep MUST be anchored to the `mcp__tavily__` prefix — a bare `tavily_(search|extract)` also matches 3 unrelated prose report-field labels at `rf-qa.md:119,506` and `rf-qa-qualitative.md:127`, which are NOT tool-ids and MUST NOT be changed.)
2. All 8 agents' `tools:` entries read `mcp__tavily__tavily-search` / `…-extract`, byte-matching
   the form in `src/superclaude/agents/deep-research.md:6-7`.
3. No non-tavily line changed (diff is hyphen-restoration only).
4. `make sync-dev && make verify-sync` clean.

**Rollback**: `git checkout feat/rf-harness-sync -- src/superclaude/agents/rf-*.md`.

---

## R2 — [HIGH, blocks merge] Disclose + decide the unvalidated default POST-reflect path

**Finding**: REVIEW.md H2. `task-builder/SKILL.md` (lines 1668, 2218, 2370) asserts nested
Skill-tool fan-out is "confirmed," while the PR body states the skill-default POST path is
"NOT yet validated end-to-end," and memory `reference_subagent_cannot_nest_skill_fanout.md`
records that pattern degrading to a hand-rolled fixture.

**R2a — always-safe (apply unconditionally)**: Add an in-SKILL disclosure on the default
(`reflect_post_mode: skill`) arm of Rule 20 (near `task-builder/SKILL.md:2370`) and at the
`#6 --cli` input definition, stating plainly that the skill-default POST path is not yet
session-validated end-to-end and that `--cli` is the validated path. The "confirmed" wording
MUST be softened to match reality (e.g. "expected to hold; not yet session-validated — see
disclosure") OR carry a citation to the run that proves it.

**R2b — HUMAN DECISION (HD-1): default-mode resolution**. One of these is a design choice for
RyanW and MUST NOT be auto-selected:
  - (i) Keep skill-mode default; attach a concrete validating run id/artifact to the
    "confirmed" claim; or
  - (ii) Invert the default to `--cli` (make the wrapper the default; skill-mode opt-in)
    until nesting is re-proven; or
  - (iii) Keep skill default but mark it EXPERIMENTAL with the R2a disclosure as the only guard.

**Acceptance criteria**:
1. (R2a) `task-builder/SKILL.md` contains an explicit "not yet session-validated" disclosure
   on the default arm AND at the `--cli` input definition; no remaining bare "capability are
   confirmed" assertion without either softening or a cited validating run.
2. (R2b/HD-1) The task writes a PENDING human-decision record and HALTS the default-inversion
   decision; it does NOT flip `--cli` default or edit O4 floors without RyanW's selection.
3. `make sync-dev && make verify-sync` clean.

**Rollback**: `git checkout feat/rf-harness-sync -- src/superclaude/skills/task-builder/SKILL.md`.

---

## R3 — [MEDIUM] Test + document the runner.py FR-INLINE directive

**Finding**: REVIEW.md M1. `cli/reflect/runner.py:367-380` appends an inline-execution
directive; `tests/cli/reflect/` is unchanged, so nothing asserts it.

**Change**:
1. Add a unit test in `tests/cli/reflect/` asserting `RunnerConfig`/`_build_prompt()` output
   ends with the directive, that it appears exactly once, and that it contains the load-bearing
   phrases "INLINE", "Do NOT delegate", and "Wave 3"/"Wave 4".
2. Add a one-line code comment (or docstring note) at the directive site stating that EV-1
   (the on-disk adversarial-merge gate in sc-reflect 1.5.1) is the structural enforcement and
   this prose directive is best-effort defense-in-depth.

**Acceptance criteria**:
1. New test present and passing under `uv run pytest tests/cli/reflect/ -v`.
2. The test fails if the directive is removed or doubled (verify by local mutation).
3. `runner.py` `py_compile` / existing reflect tests still green.

**Rollback**: delete the new test; revert the comment.

---

## R4 — [MEDIUM] Add a mode-bifurcation summary + key-binding rule to task-builder

**Finding**: REVIEW.md M2. CLI vs skill POST modes diverge across form, frontmatter keys,
O4 floor, and validator clause with no single enumerating section.

**Change**: Add a compact "Mode Bifurcation Table" to `task-builder/SKILL.md`
(columns: Field/Rule · CLI mode · Skill-only mode · Justification) covering: POST item form,
`start_commit`/`executor_model_class` presence, O4 depth floor, validator clause. Add a
validation rule: `reflect_post_mode: cli` ⇒ `start_commit` + `executor_model_class` MUST be
present; `skill` ⇒ MUST be absent.

**Acceptance criteria**:
1. Table present; the key-presence rule is stated and referenced by the §3.3 checklist.
2. `make sync-dev && make verify-sync` clean.

---

## R5 — [LOW] Fix the dangling "§4.2 clause 4" reference

**Finding**: REVIEW.md L1. `task-builder/SKILL.md:2276` cites "§4.2 clause 4"; no §4.2 heading
exists (clauses live in the unnumbered note at ~2246-2248).

**Change**: Either number that note `§4.2` or rewrite the citation to name it literally
("clause (4) of the CLI-mode anti-self-confirmation note"). Apply the same fix to any sibling
reference (also covers L2: add a one-clause mode qualifier to the `spec_path`-threading
statements so they are not read as unconditional).

**Acceptance criteria**:
1. No reference to a non-existent `§4.2` remains; the anchor resolves.
2. `spec_path` threading statements carry a skill-vs-CLI qualifier.

---

## R6 — [OUT OF SCOPE] Pre-existing stale §11.3 line citations

REVIEW.md L3 — `reflection-rubric.md:126,142,163` hardcoded line numbers are pre-existing drift
NOT introduced by this PR. **Do not fix in this remediation.** Track as a separate follow-up
(replace absolute line numbers with section anchors).

## Nits (optional, non-blocking)

- Extract `inline_directive` in `runner.py` to a module-level constant `_INLINE_EXECUTION_DIRECTIVE`.
- `task-builder/SKILL.md:159` — prefer positive framing over "does NOT class-exclude".

---

## Execution notes for task-builder

- Independent items (parallelizable): R1 (agents) and R3 (runner test) touch disjoint files.
- Sequential: R2a → HD-1 halt; R4 and R5 both edit `task-builder/SKILL.md` (serialize to avoid
  conflicting edits).
- Every code/markdown item ends with `make sync-dev` + `make verify-sync`; Python items add
  `uv run ruff format --check src/ tests/` before declaring done (CI runs it separately).
- Final gate before commit is `/sc:reflect --type task --validate` (chain Phase E), not this spec.
