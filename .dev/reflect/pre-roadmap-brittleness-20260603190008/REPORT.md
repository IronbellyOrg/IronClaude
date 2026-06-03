# /sc:reflect — Pre-Execution Audit (UC-1)

**Mode:** pre (coverage/gap + correctness audit)
**Tier reached:** 1 (rationale below)
**Tasklist:** `.dev/tasks/to-do/TASK-RF-20260603-180207/TASK-RF-20260603-180207.md`
**Spec:** `.dev/tasks/to-do/TASK-RF-20260603-180207/research-notes.md`
**Date:** 2026-06-03
**Calibrated confidence:** 0.95
**Status:** partial (1 HIGH actionable finding before execution)

---

## Headline

Coverage is **complete (9/9, 1.0)** and the spec-literal tokens that would break execution if wrong are all **verified TRUE against live source/git**. One **HIGH** finding blocks a clean go: the **base-branch premise** (Step 1.3 "work on `integration`") is unsafe because `integration` does not exist and every prerequisite commit lives only on the current `refactor/...` branch.

---

## Coverage Matrix (spec → tasklist)

| Spec requirement (research-notes) | Tasklist location | Status |
|---|---|---|
| A — delete `test_wiring_pipeline.py` + re-home unique NFR-007 guard; `WIRING_GATE` preserved | Phase 2 (Steps 2.1–2.4) | ✅ mapped |
| B — generation-time phantom-ID prevention: source `_spec_ids` from `spec_id_registry.json` `union_of_known()`, fail-shut, optional `require_spec_ids`, regression test, preserve merge-gate catch | Phase 3 (Steps 3.1–3.3) | ✅ mapped |
| C — behavior-neutral comment (inert `timeout_seconds=600` under convergence); live gate `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`; genuine fixes → follow-up | Phase 4 (Step 4.1) | ✅ mapped |
| D — markdown-path deletion precondition-check-then-HALT (cutover NOT-MET) | Phase 5 (Step 5.1) | ✅ mapped |
| E1 — `spec_id_registry.json` writer removal HALT + document Contract #9 reader-repoint prerequisite | Phase 6 (Step 6.1) | ✅ mapped |
| E2 — `remediate_parser.py` deletion HALT | Phase 6 (Step 6.2) | ✅ mapped |
| E3 — MD-family reconciliation verify-only (guard test) | Phase 6 (Step 6.3) | ✅ mapped |
| Constraints — UV-only; src/+tests only; no sync-dev; PER_PHASE QA | Phase 1, all gates, Exec Context | ✅ mapped |
| Verification — full `uv run pytest` green + 0 collection errors + `make lint` | Phase 7 | ✅ mapped |

**coverage_pct = 1.0**, `unmapped_requirements: []`.

---

## Spec-literal grounding (fresh re-Read — NOT trusting prior inline gates)

| Literal (would break execution if wrong) | Verified against | Verdict |
|---|---|---|
| Cutover SoT fields `release_marker_count` / `cutover_eligible` / `cutover_at_count_default: 3` | `.dev/migrations/r1-4-cutover-counters.yaml` (13×`false`, 0×`true`; comment confirms "premature cutover (count<3) HALT-blocked") | ✅ exact |
| Area B `SpecIdRegistry.union_of_known() -> frozenset[str]` (incl. accepted_deviation_ids) | `id_registry.py:94` | ✅ exact |
| Area B executor test idiom `patch("superclaude.cli.roadmap.executor.ClaudeProcess")` | `tests/roadmap/test_file_passing.py:58` | ✅ exists |
| Area C live gate `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (NOT deleted `gate=None`) | `executor.py:2675`, `gates.py:1363` | ✅ exact |

All four decisive literals hold. The tasklist's Area D/E precondition predicate (`cutover_eligible == true`) matches the yaml's own derivation rule exactly.

---

## Findings

### F1 — HIGH — Base-branch premise is unsafe (Step 1.3) — `needs_human_decision`

**Claim (Grounded).** Step 1.3 instructs working on branch `integration`. Git evidence:
- `git rev-parse --verify integration` → `fatal: Needed a single revision` (no local branch).
- `git rev-parse --verify origin/integration` → `fatal` (no remote branch). Existing branches: `master`, `refactor/roadmap-pipeline-r0-r1-rewrite` (current), `fix/master-ci-invoke-sonnet-stale-tests`, `docs/octocode-...`.
- `git branch --contains 17b8ee94` (R1.6 `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`) → **only** `refactor/roadmap-pipeline-r0-r1-rewrite`. **Not** on `master`.
- The cutover yaml, `union_of_known`, the stale test, and the dual-write flags are all committed on the `refactor/...` line, absent from `master`.

**Why it matters.** Step 1.3's fallback (`git checkout -b integration` from current HEAD) lands on a *correct* code state **only if execution starts from `refactor/roadmap-pipeline-r0-r1-rewrite`**. Three failure modes:
1. `git checkout integration` is attempted first and **errors** (branch absent) before the create-fallback fires — clumsy, recoverable, but noisy.
2. It silently creates a **phantom `integration`** branch that is really a copy of the refactor branch — diverging from the repo's real topology and muddying any later PR (CLAUDE.md PR rules target fork `master`).
3. **Asymmetric-cost failure:** if execution ever starts from `master` (fresh clone / different session), the fallback creates `integration` **off master**, which lacks **all** R1.4/R1.5/R1.6 prerequisites → every one of the 5 items mis-executes (the stale test/import differs, `union_of_known`/`SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`/cutover yaml may be absent).

**Why the inline gates missed it.** rf-qa (A.10) explicitly noted Step 1.3 targets `integration` but rated it "non-blocking — self-contains checkout/create, matching the documented branch model." It verified the working-tree state (the refactor branch) and accepted the user's literal "branch off integration" + CLAUDE.md's aspirational `master←integration←feature` model — without checking that `integration` exists or carries the prerequisite commits. This is the canonical parent-vs-head blindspot.

**Recommended remediation (surgical, tasklist-only — no code change):** rewrite Step 1.3 to pin the base to the SoT branch for this work and forbid a silent base-off-master:
- Base explicitly off the current work branch: `git checkout -b fix/roadmap-brittleness-followups refactor/roadmap-pipeline-r0-r1-rewrite` (or simply continue on `refactor/...` if the user prefers no new branch), AND
- Add a hard guard asserting a prerequisite is reachable from the chosen base (e.g. `git merge-base --is-ancestor 17b8ee94 HEAD` OR `test -f .dev/migrations/r1-4-cutover-counters.yaml && grep -q SPEC_FIDELITY_GATE_CONVERGENCE_AWARE src/superclaude/cli/roadmap/gates.py`), **HALT** if the guard fails.
- Update the 2 prose references ("work on the `integration` branch" in Execution Context Key constraints L138; any objective-line branch mention) to match.

### F2 — LOW (informational) — Areas D & E are no-ops this cycle

The cutover precondition is decisively NOT-MET (13×`cutover_eligible: false`), so Phases 5–6 will write PENDING markers and HALT without doing work. This is **expected and correctly authored** (the items are written as the gated form and recorded in Open Questions). Surfaced only so the operator isn't surprised that ~Phases 5–6 produce no code change this run.

---

## Tier rationale

Pinned at **T1**. The §5.3 rubric would escalate on multi-domain (rule 4), but: (a) the single blocking finding is a **deterministic git fact** (`integration` absent; commits only on refactor) that multi-model debate cannot overturn; (b) the input was already reviewed by a large heterogeneous ensemble during the build (7 researchers + 2 rf-analyst + 2 rf-qa research-gate + rf-qa task-integrity + 2 rf-qa-qualitative). A full T2 fan-out is not cost-justified for a fact re-confirmable by one `git` command. Recorded transparently per §5.1.

---

## Verdict

**1 HIGH actionable finding (F1) — remediation recommended before `/task`.** Fixing Step 1.3's base-branch premise is a surgical, tasklist-only edit. All other dimensions pass: coverage 1.0, all decisive literals verified, corrected-fact discipline intact (Area C live gate, Area E repoint template, D/E HALT design), PER_PHASE QA + halt-precedence guards present.
