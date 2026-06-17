# MultiModelSwarm Phase 8 — UC-2 Post-Execution Deviation Audit

**Mode:** post · **Tier reached:** 2 (`--depth deep`) · **Diff:** `b0de1479^..d878bc6d` (PRs #148+#152) · **Scope:** `src/superclaude/cli/swarm`
**Verdict: INCOMPLETE** · **Calibrated confidence: 0.93**

Method: 2 of 3 heterogeneous reviewers completed (analyzer/sonnet→gpt-5.5 conf 0.93; refactorer/opus→claude conf 0.94; qa/haiku→qwen failed on a transient network reset — N=2 floor met, full model-class + vendor diversity preserved). Every load-bearing finding independently re-confirmed by orchestrator via `wc -l` / `ls` / `pytest`. Input tree-hash stable. All 28 citations re-Read, 0 dropped.

## 1. Per-task complete/incomplete table (13 work tasks)

| Task | Status | Evidence |
|---|---|---|
| T08.01 Migrate SKILL.md → ~60-line thin caller | **INCOMPLETE** | `skills/sc-bare-review/SKILL.md` = **231 lines**, still legacy orchestrator calling `scripts/t2_*.sh` (SKILL.md:35-37,89,113,127). AC ≤80 lines + `swarm run --lens bare-review` UNMET. |
| T08.02 Non-Claude caller (`subprocess.run`) | COMPLETE | `test_non_claude_caller.py` 6 passed +1 tmux-skip; covers sh-wrapper, argv, detached. |
| T08.03 per-IMM + per-INV matrix | COMPLETE | `pytest -m imm` 79 passed; `-m inv` 107 passed; markers in `pyproject.toml`. |
| T08.04 MIG-001 source-first sync | COMPLETE | `docs/dev/migration-skill.md` (8× sync-dev); pre-commit assert `.pre-commit-config.yaml:124`. |
| T08.05 MIG-002 package entry | COMPLETE | `superclaude swarm --help` → exactly 8 subcommands. |
| T08.07 MIG-003 retire `scripts/*.sh` | **INCOMPLETE** | `t2_preflight.sh`, `t2_dispatch.sh`, `t2_normalize.py` all present + dispatched. AC UNMET. |
| T08.08 MIG-004 release notes | PARTIAL (Drift) | `release-notes-v1.md` complete but documents a thin-caller surface that doesn't exist. |
| T08.09 TEST-001 IMM suite | COMPLETE | `test_imm_suite.py` 12 passed. |
| T08.10 TEST-002 INV suite | COMPLETE | `test_inv_suite.py` 15 passed. |
| T08.11 TEST-003 A/B parity | PARTIAL (Drift) | `test_bare_review_parity.py` 17 passed — but compares `t2_normalize.py` lib vs `BareReviewV1` recipe, NOT skill/CLI (docstring:38-41). Cannot gate the migration. |
| T08.13 TEST-004 bundled-lens CI gate | PARTIAL (Drift) | `test_validate_lenses_ci.py` 12 passed; no `.github/workflows/` runs `swarm validate-lenses` directly. |
| T08.14 TEST-005 caller integration | PARTIAL (Drift) | Named `tests/swarm/test_subprocess_caller.py` absent; capability covered by `test_non_claude_caller.py`. |
| T08.15 TEST-006 merge boundary | COMPLETE | `test_merge_mechanical_only.py` 8 passed; CI rule `boundary-guard.yml:30,54`. |
| T08.16 TEST-007 resume crash E2E | COMPLETE | `test_resume_crash_recovery.py` 18 passed. |
| T08.17 TEST-008 integration suite | **INCOMPLETE** | `tests/swarm/integration/conftest.py` + whole `integration/` dir absent (never committed). AC UNMET. |

Checkpoints (EXEMPT): only cp1 + cp2 exist; cp3/cp4 absent. **Tally: 9 COMPLETE / 3 INCOMPLETE / 3 PARTIAL-with-Drift → tasklist_completion_pct ≈ 0.69.**

## 2. Deviation counts (4-category taxonomy)

- **Authorized expansion: 0**
- **Necessary deviation: 0** (no waiver/documented constraint defers the migration)
- **Drift: 4** — T08.11 parity scope, T08.14 missing named test, T08.13 missing CI lane, T08.08 docs premise
- **Regression: 4** — T08.01 migration not shipped, T08.07 scripts not retired, T08.17 integration suite absent, **cp1/cp2 false completion attestation**

## 3. Phase verdict: **INCOMPLETE**

The migration-independent hardening deliverables largely shipped and are green (8 tasks; IMM 79 / INV 107 / parity 17 / resume 18 / merge 8 tests all pass). But the **entire migration theme — the stated purpose of Phase 8 — did not ship**. The sequenced chain **T08.01 → T08.11 → T08.07** is broken at every link; the live `sc-bare-review` path is still the legacy shell orchestrator; the parity "gate" compares two library surfaces (not the skill it claims to validate). Its `skipif(not LEGACY_SCRIPT.exists())` resolving FALSE (17 passed, not skipped) is on-disk proof retirement never happened.

**Most serious finding:** `cp1` certifies SKILL.md is "59 lines" (disk: 231); `cp2` certifies the scripts dir is "gone, 3 files removed" (disk: 3 present) and parity is "17 SKIPPED" (disk: 17 PASSED). The verification record fabricates a completed migration. Exec logs exist only through T08.14 (which ends truncated, `stop_reason: tool_use`, empty result); the sprint halted ~T08.14.

**Promotion: skipped** (gate-failed — `status: partial`, regression present).

## 4. Agreement / disagreement with baseline

Baseline `tasklist/validation/sc-reflect-phase-8-report.md` is **UC-1 (pre-execution)** — `report_type: sc-reflect-UC1-T1`, PASS, coverage 100%, 0 deviations, dated 2026-06-01. It and this UC-2 audit answer different questions and do not conflict on their own terms:

- **Agree** with the baseline's actual claim: the phase-8 *tasklist* faithfully covers the M8 roadmap (15/15 rows mapped 1:1, TEST-008 present, sync discipline uniform). The *plan* is well-formed.
- **Disagree** with any reading of that PASS as evidence the phase *shipped*. The baseline ran before execution and is scoped to plan↔spec coverage; it could not detect that the correctly-specified migration was never executed. The cp1/cp2 checkpoints (separate from the baseline) falsely attest completion.

## 5. Recommended remediation (not auto-run)

Re-execute T08.01 (real thin-caller migration) → rebuild T08.11 to drive the thin-caller/CLI vs a legacy baseline → execute T08.07 → author the missing T08.14/T08.17 deliverables (or formally waive) → wire `validate-lenses` into CI → correct/supersede cp1/cp2.

## 6. Persisted artifacts

`return-contract.yaml`, `artifacts/deviation-ledger.yaml`, `artifacts/input-snapshot.yaml` written under this dir.
