---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: 1:1
major_issue_policy: stop-and-fix
spec_source: TDD_TASK_DIRECTIONAL_MERGE.md
generated: "2026-05-17T02:20:58.673412+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — Task Directional Merge (/sc:task → /task)

## 1. Validation Milestones Mapped to Roadmap

Per HIGH complexity 1:1 interleaving, each work milestone (M1–M5) is paired with a co-located validation milestone (V1–V5) that gates exit. Validation runs continuously in parallel within each milestone window, not as a downstream phase.

| Validation Milestone | Paired Work Milestone | Duration | Exit Gate |
|---|---|---|---|
| V1: Foundation Atomicity & Ordering Verification | M1 (Foundation 7-row + CR-7 sentinel) | T+0 → T+5d (parallel with M1) | Step-1 pre-commit gate=0; AC-SM-07 ordering PASS; AC-SM-12 100% resume PASS on 136-file floor; CR-FM-04 grep returns 3 names monotonic; M1 atomicity verified via `git log --name-only` (single commit, 7 rows) |
| V2: TFEP Cluster Byte-Preservation Verification | M2 (TU-5..TU-8) | T+5d → T+10d | AC-ATK-03 4-state observer PASS; AC-ATK-12(b) 7-field schema PASS; AC-CR-TASK-09-F04 over-escalate PASS; CR-TASK-12 verbatim-diff returns 0 against frozen fixtures at corrected anchors `:133-135` and `:157-161`; donor `:232` Outcome enum byte-identical |
| V3: CLI Re-Route & Rebase-Split Resistance Verification | M3 (CLI Re-Route + Stubification) | T+10d → T+15d | AC-ATK-15 Step-5 atomicity PASS; AC-ATK-17 server-side pre-receive hook rejects rebase-split fixture; AC-SM-09 commit roster set-equal to `final-merge-plan.md:375`; CR-TASK-12 7-diff returns 0; all 6 CLI emission sites assert `prompt.startswith("/task ")` and `"/sc:task" not in prompt` |
| V4: Hard-Delete Destructive-by-Default & Flock Verification | M4 (Hard-Delete + Flock-Guarded Sync) | T+15d → T+17d | AC-SM-10 commit roster PASS; `make verify-sync` returns 0; donor `sc-task-protocol/` absent from both `src/` and `.claude/` (find -type d returns nothing); CR-DEP-06 manifest residual count outside authorized buckets = 0; AC-ATK-16 concurrent worktree flock PASS (0 flakes across 30 CI runs); AC-ATK-07 rf-qa F-07 chain verifier PASS; AC-ATK-18 4 sub-bindings closed |
| V5: Production-Readiness Audit Closure | M5 (Validation + Manifest + Docs) | T+17d → T+27d | All 18 AC-ATK + 12 AC-SM PASS or downgraded per R-DOC-01 reframe; K-01..K-08 baseline measured; Phase 7.5 traceability matrix returns 0 OPEN/PARTIAL rows; mkdocs build 0 broken-link warnings; R-RULE-11 audit clean |

## 2. Test Categories

### 2.1 Unit Tests (@pytest.mark.unit)
| Category | Target Coverage | Tooling |
|---|---|---|
| Helper modules | >90% per module | `uv run pytest --cov=superclaude.skills.task` |
| `path_override_check()`, `tier_field_validate()`, `gate_1_dispatch()` | 100% branch | pytest-cov; parametrize critical/trivial/none cases |
| CR-FM-03 shim (default-to-STANDARD) | 100% branch | parametrize absent/present/malformed Tier |
| 4-state baseline observer | 100% branch | parametrize {absent, empty, parse-fail, schema-fail} |

### 2.2 Integration Tests (@pytest.mark.integration)
| Category | Scope | Tooling |
|---|---|---|
| F1 loop dispatch | Full READ→IDENTIFY→EXECUTE→UPDATE→REPEAT under each tier | pytest tmp_path fixtures |
| Phase-Gate QA + Post-Completion Validation | All 4 rf-qa invocation points | subprocess spawn fixtures |
| TFEP escalation flow | 6-step end-to-end (halt → 9-field YAML → forensic → consume → tasklist → resume) | mocked subagent harness |
| CR-FM-03 shim across 136-file live floor | Parametrized over live `grep -rl` recount at gate-execution time (never hardcoded) | live fixture iterator |

### 2.3 End-to-End Tests (@pytest.mark.e2e)
| Category | Scope |
|---|---|
| Sprint pipeline → /task invocation | `superclaude sprint run` against fixture tasklist; assert all 6 emission sites use `/task ` prefix |
| Cleanup-audit pipeline → /task invocation | `superclaude cleanup-audit` covering G-001..G-006 caller bindings |
| In-flight MDTM resume | Resume `TASK-RESEARCH-20260403-sprint-task-exec` (48 refs/10 files) post-Step-6; verify Gate-1.5 emissions + warn-and-continue + no HALT |
| Rebase-split bypass attack | Fabricate intermediate SHA where `task.md` stubified but CLI sites still emit `/sc:task`; assert AC-ATK-17 rejects |

### 2.4 Acceptance Tests (Persona-Based)
| Persona | Scenario |
|---|---|
| P-01 MDTM Task Author | Author new TASK-*.md with `Tier: STRICT`; invoke /task; verify path-override + classification header + Gate 1 dispatch emission |
| P-02 Sprint Executor | Invoke /task on STRICT item; verify pre-flight + baseline + F1 monotonicity; trigger TFEP; verify rf-qa mid-phase invocation |
| P-03 Framework Maintainer | Execute 10-step commit chain; verify each pre-commit gate exits 0 in correct sequence |
| P-04 Downstream Task-Runner | Read in-flight TASK with deprecated refs; verify Gate-1.5 warn-and-continue + one-shot ack; never HALT |

### 2.5 Compliance & Contract Tests
| Category | Scope |
|---|---|
| API Contract — 3 row-1 functions | Signature + return-type + side-effect contracts per API-001..003 |
| API Contract — 6 CLI emission sites | Per-site emission-boundary contract per API-004..009 |
| API Contract — 4 rf-qa spawn envelopes | YAML envelope contract per API-010..013 |
| Schema Validation | DM-001..005 closed-enum + field-cardinality + observation-order |
| Migration Rollback | Per-step revert tests for fine-grained Steps 2/3/4/7-10; destructive-by-default forward-roll for Steps 5/6 |

### 2.6 Security Tests
| Category | Scope |
|---|---|
| Critical Path Override bypass attempt | Tag `auth/foo.py` as `Tier: LIGHT`; verify path_override_check forces STRICT |
| Rebase-split atomic-commit bypass (H-2) | AC-ATK-17 server-side hook fixture |
| `--no-verify` bypass attempt | Verify local pre-push cannot circumvent server-side enforcement |
| Per-item marker consumer drift | AC-ATK-05 closed-enum register fails on undeclared consumer |
| Flock concurrency safety | AC-ATK-16 worktree race fixture (2 parallel make sync-dev) |

### 2.7 Operational Readiness Tests
| Category | Scope |
|---|---|
| Runbook validation | R1-R5 dry-run walkthroughs (Critical Path Override, Gate-1.5 triage, Tier mis-classification, TFEP escalation, In-flight resume) |
| Alert firing | Trigger each alert condition (pre-receive reject, Step-5 gate fail, legacy-surface match, sync drift, incident schema drift) |
| Monitoring emission | Verify all Task Log emission prefixes match canonical BNF grammar |

## 3. Test-Implementation Interleaving Strategy (Ratio Justification)

**Ratio: 1:1 (HIGH complexity)** — Each work milestone has a co-located validation milestone gating exit. Justification:

1. **INV-04 highest-exposure risk** — Semantic resumability of 136-file live floor (monotonic upward) requires per-milestone resume verification; deferring validation past M2 risks silent semantic degradation that compounds across milestones.
2. **Atomic commits at M1/M3/M4** — ME-6 (7-row foundation), S-2 (Step-5 atomic), S-3 (Step-6 atomic) cannot be tested post-hoc; validation must gate the atomic boundary itself.
3. **Byte-preservation at M2** — CR-TASK-12 verbatim-diff audit requires frozen fixtures captured before donor hard-delete; cannot retroactively reconstruct.
4. **Rebase-split bypass (H-2)** — AC-ATK-17 server-side hook must be live before M3 commits; testing post-merge cannot catch intermediate broken SHAs.
5. **Destructive-by-default M4** — Donor hard-delete is irreversible; rf-qa F-07 chain verifier must PASS at pre-commit, not post-commit.

Within each milestone window, tests are authored **in parallel** with implementation rows using TDD red-green-refactor; the validation milestone gates the exit, not the start.

## 4. Risk-Based Test Prioritization

| Priority | Risk | Test Investment |
|---|---|---|
| P0 (gating) | INV-04 semantic resumability (R-OPS-02; 136-file floor) | TEST-030 AC-SM-12 live-count fixture + TEST-018 AC-ATK-18 4 sub-bindings; runs in V1/V3/V4 |
| P0 (gating) | Rebase-split bypass H-2 (R-ATK-17) | TEST-017 AC-ATK-17 server-side hook fixture; runs in V3 |
| P0 (gating) | ME-6 M1 atomicity violation (7-row split) | TEST-027 AC-SM-09 + git log --name-only single-commit assertion; runs in V1 |
| P0 (gating) | S-3 mirror-sync drift / worktree race (R-ATK-16) | TEST-016 AC-ATK-16 concurrent worktree (0 flakes/30 runs); runs in V4 |
| P0 (gating) | R-DRIFT-03 anchor off-by-43 (M3-blocking) | Pre-V2 patch verification of `:200-210` → `:157-161` in 3 artifacts + CR-TASK-12 anchors |
| P1 | CR-7 ORDERING markdown discipline weakness (R-ATK-01) | TEST-001 + TEST-013 + TEST-025 (3 layers: AST + grep + sentinel) |
| P1 | F-04 over-escalation queue flood (R-RES-03) | TEST-003 AC-ATK-03 4-state observer + rf-qa queue depth monitoring |
| P1 | TU-3 quality-engineer companion spawn correctness | Integration test asserting rf-qa always present, quality-engineer additive on STRICT only |
| P1 | CR-FM-03 shim sunset binding (R-ATK-12) | TEST-012 AC-ATK-12 + gate-1.4 emission test |
| P2 | R-DRIFT-02 anchor off-by-2 (LOW) | Pre-V3 patch verification |
| P2 | `flock` portability on macOS/BSD (Q-GAP-04) | Cross-platform fixture matrix (Linux/macOS via brew/BSD via lockfile-create) |
| P2 | mkdocs version drift (R-FM-05) | Pin mkdocs version in pyproject.toml; verify Step-8 gate |
| P3 | UTF-16 grep evasion (R-FM-07) | Surfaced as residual; document UTF-8-only authoring discipline |
| P3 | Donor file-rename evasion (R-FM-08) | CR-DEP-04 enforces directory absence via find -type d |

## 5. Acceptance Criteria Per Milestone

### V1 (paired with M1)
- AC-ATK-01 (Row1 call order AST/grep) PASS
- AC-ATK-05 (Closed-enum consumer register published) PASS
- AC-ATK-10 (Pre-loop HALT policy 2-category) PASS
- AC-ATK-12(c) (CR-FM-01 canonical table) PASS
- AC-ATK-13 (Row1 ordering executable grep) PASS
- AC-SM-07 (CR-FM-04 ordering — 6 monotonic hits) PASS
- AC-SM-12 (Step-1 gate=0 + 100% in-flight resume on live 136-floor) PASS
- M1 atomicity: `git log --name-only` shows single commit with all 7 foundation rows
- OQ-TIER-VOCABULARY + OQ-FM-03-SUNSET + Q-GAP-02/05/06 resolved

### V2 (paired with M2)
- R-DRIFT-03 patch applied to 3 artifacts + CR-TASK-12 anchors (PRE-COMMIT BLOCKER)
- AC-ATK-03 (4-state baseline observer, order pinned) PASS
- AC-ATK-12(b) (7-field incident schema, Outcome enum byte-identical to donor `:232`) PASS
- AC-CR-TASK-09-F04 (over-escalate on absent/empty/malformed baseline) PASS
- CR-TASK-12 (verbatim diff 7-zero at corrected anchors) PASS — deferred PASS to V3 close
- 4th rf-qa invocation point (mid-phase TFEP) live; ME-2 preserved
- F2 catalog cardinality: 10 → 13 (additive only)

### V3 (paired with M3)
- R-DRIFT-02 patch applied (PRE-STEP-4 BLOCKER)
- S-1 in-flight discharge attested (named targets `TASK-PRD-20260514-121039` + `TASK-TDD-20260514-121250` discharged OR snapshot-frozen OR --max-wait 14d expired with auto-invoke option (b))
- AC-ATK-15 (Step-5 atomic, commit roster includes CR-DEP-01 + CR-DOC-01 + CR-REF-01..05 atomically) PASS
- AC-ATK-17 (server-side pre-receive hook rejects rebase-split fixture) PASS
- AC-SM-08 (CR-TASK-12 7 zero-diffs) PASS
- AC-SM-09 (Step-5 commit roster set-equal to `final-merge-plan.md:375`) PASS
- All 6 CLI emission sites assert `prompt.startswith("/task ")` and no `/sc:task` substring
- `tests/cleanup_audit/test_prompts.py` authored (Q-GAP-01 closure)

### V4 (paired with M4)
- AC-ATK-07 (rf-qa F-07 chain verifier) PASS (PRE-HARD-DELETE)
- AC-ATK-16 (concurrent worktree flock, 0 flakes across 30 CI runs) PASS
- AC-ATK-18 (4 sub-bindings: content grep + sprint-emit + ack gate + CR-DEP-06 manifest) PASS
- AC-SM-10 (Step-6 commit roster set-equal to `final-merge-plan.md:381`) PASS
- `make verify-sync` returns 0
- Donor `sc-task-protocol/` absent from both `src/` and `.claude/` (find -type d returns nothing)
- CR-DEP-06 manifest: residual count outside authorized buckets = 0
- 144 known residuals dispositioned (61 backlog + 83 docs/generated)

### V5 (paired with M5)
- All 18 AC-ATK rows PASS or PARTIAL with documented residuals
- AC-SM-01 (V/C/K byte-match) PASS
- AC-SM-02 (ME traceability 9/9) PASS
- AC-SM-03 (INV walkthrough 5/5) PASS
- AC-SM-04 (F-findings cite anchors 8/8) PASS
- AC-SM-05 (S-constraints cite HZ 3/3) PASS
- AC-SM-06 (67 rows + 10 steps) PASS
- AC-SM-11 (Zero ledger re-proposal) PASS
- K-01..K-08 baseline measurements taken
- mkdocs build returns 0 broken-link warnings
- R-RULE-11 audit clean (0 ledger re-introductions)
- R-DOC-01 cascade-downgrade applied per Q-R-DOC-01

## 6. Quality Gates Between Milestones

**Issue Classification Applied:**

| Severity | Action | Gate Impact |
|---|---|---|
| CRITICAL | stop-and-fix immediately | Blocks current milestone |
| MAJOR | stop-and-fix before next milestone | Blocks next milestone |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

**Inter-Milestone Quality Gates:**

| Gate | Between | Required Conditions | Major Issue Triggers Stop-and-Fix |
|---|---|---|---|
| G1→2 | V1 closure → M2 entry | V1 exit criteria met; R-DRIFT-03 patch applied; OQ-TIER-VOCABULARY resolved; AC-ATK-05 register published | Any V1 AC-ATK failure; M1 split into multiple commits (ME-6 violation); CR-FM-04 grep returns wrong order |
| G2→3 | V2 closure → M3 entry | V2 exit criteria met; R-DRIFT-02 patch applied; Q-GAP-07 donor-block fixtures authored; S-1 in-flight discharge attested | CR-TASK-12 diff non-zero; 4th rf-qa invocation absent; F2 catalog deletion/weakening detected; live in-flight target uncompleted past --max-wait without snapshot-freeze decision record |
| G3→4 | V3 closure → M4 entry | V3 exit criteria met; rf-qa F-07 chain verifier authored; CR-DEP-06 manifest emitter ready; flock portability fallback documented | AC-ATK-17 hook absent or bypassable; CLI emission site missed; Step-5 commit roster mismatch; AC-ATK-15 atomicity violation |
| G4→5 | V4 closure → M5 entry | V4 exit criteria met; donor absent from both src/ and .claude/; CR-DEP-06 manifest residual count = 0 outside authorized buckets | `make verify-sync` non-zero; donor file persists (rename evasion); flock flakes detected; AC-ATK-07 F-07 chain verifier FAIL |
| Release Gate | V5 closure → Production | All 18 AC-ATK + 12 AC-SM PASS or documented residuals; K-01..K-08 baseline measured; traceability matrix returns 0 OPEN/PARTIAL | Any LR-REJECT-* ledger entry re-introduced; mkdocs build broken-link warnings; R-RULE-11 audit dirty |

**Continuous Quality Signals (parallel to all milestones):**
- Pre-commit gate at every step exit-code 0
- Live in-flight floor recount at each gate-execution time (never hardcoded; iterate via `grep -rl`)
- `[CODE-VERIFIED]` tags carry 40-char SHA suffix (AC-ATK-08 drift discipline)
- No new HIGH/CRITICAL R-DRIFT-NN open against input artifacts
- Server-side AC-ATK-17 hook active from M3 push-time onward (indefinite CLI surveillance)
- Weekly CR-DEP-06 manifest re-emit post-V5 archived to docs/generated/
