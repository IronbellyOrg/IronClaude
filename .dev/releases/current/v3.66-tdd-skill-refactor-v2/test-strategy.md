---
complexity_class: LOW
validation_philosophy: continuous-parallel
validation_milestones: 1
work_milestones: 4
interleave_ratio: "1:3"
major_issue_policy: stop-and-fix
spec_source: tdd-command-layer-spec.md
generated: "2026-04-03T20:14:21.294250+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy: TDD Command Layer Refactor

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

| Phase | Type | Validation Activities |
|-------|------|----------------------|
| Phase 1: Preparation & Template Study | Work | Inline: confirm SKILL.md line count (438), confirm migration block locations (lines 48–63, 82–88), record baseline snapshot |
| Phase 2: Command File Creation | Work | Inline: `wc -l` within 100–170, grep for prohibited keywords returns 0 |
| Phase 3: Content Migration | Work | Inline: SKILL.md `wc -l` within 400–440, grep for duplication returns 0 |
| **Phase 4: Fidelity Verification** | **Validation** | **Full gate: 26 parallel verification checks (grep/diff/wc). Hard stop on any failure.** |
| Phase 5: Sync, Evidence & Commit | Work | Inline: `make verify-sync` exit 0, `test -f` on both file locations |

**Ratio justification**: At LOW complexity (0.25), a 1:3 interleave ratio is appropriate. One dedicated validation milestone (Phase 4) gates three implementation work phases (Phases 2, 3, 5). Phase 1 is preparatory and Phase 4 catches all accumulated issues before the irreversible commit in Phase 5. The inline checks in Phases 2–3 provide early feedback without adding formal gate overhead.

---

## 2. Test Categories

### 2.1 Structural Tests (13 checks) — Unit-equivalent

These verify the command file's internal correctness in isolation.

| ID | Test | Method | Phase | SC |
|----|------|--------|-------|----|
| ST-01 | Command file exists at `src/superclaude/commands/tdd.md` | `test -f` | 2, 5 | SC-1 |
| ST-02 | Command file line count 100–170 | `wc -l` | 2 | SC-2 |
| ST-03 | Frontmatter contains `name: tdd` | grep | 2 | FR-TDD-CMD.1b |
| ST-04 | Frontmatter contains `category: documentation` | grep | 2 | FR-TDD-CMD.1b |
| ST-05 | Frontmatter contains `complexity: advanced` | grep | 2 | FR-TDD-CMD.1b |
| ST-06 | Options table contains `--tier` | grep | 2 | SC-3 |
| ST-07 | Options table contains `--prd` | grep | 2 | SC-3 |
| ST-08 | Options table contains `--resume` | grep | 2 | SC-3 |
| ST-09 | Options table contains `--output` | grep | 2 | SC-3 |
| ST-10 | Options table contains `--focus` | grep | 2 | SC-3 |
| ST-11 | Options table contains `--from-prd` | grep | 2 | SC-3 |
| ST-12 | Options table contains `<component>` | grep | 2 | SC-3 |
| ST-13 | Activation section contains `Skill tdd` | grep | 2 | SC-4 |

### 2.2 Migration Tests (7 checks) — Integration-equivalent

These verify content moved correctly between files.

| ID | Test | Method | Phase | SC |
|----|------|--------|-------|----|
| MT-01 | Strong example 1 (all four inputs) present in command | grep for distinctive string | 4 | SC-6 |
| MT-02 | Strong example 2 (PRD-to-TDD) present in command | grep for distinctive string | 4 | SC-6 |
| MT-03 | Strong example 3 (design from scratch) present in command | grep for distinctive string | 4 | SC-6 |
| MT-04 | Weak example 1 present in command (annotated) | grep for distinctive string | 4 | SC-6 |
| MT-05 | Weak example 2 present in command (annotated) | grep for distinctive string | 4 | SC-6 |
| MT-06 | Tier table: Lightweight/Standard/Heavyweight rows with 5 columns | grep | 4 | SC-7 |
| MT-07 | SKILL.md post-migration line count 400–440 | `wc -l` | 3, 4 | SC-9 |

### 2.3 Non-Regression Tests (6 checks) — Integration-equivalent

These verify zero collateral damage to existing behavior.

| ID | Test | Method | Phase | SC |
|----|------|--------|-------|----|
| NR-01 | SKILL.md Stage A section identical pre/post | diff against Phase 1 snapshot | 4 | SC-10 |
| NR-02 | SKILL.md Stage B section identical pre/post | diff against Phase 1 snapshot | 4 | SC-10 |
| NR-03 | SKILL.md critical rules section identical pre/post | diff against Phase 1 snapshot | 4 | SC-10 |
| NR-04 | SKILL.md session management section identical pre/post | diff against Phase 1 snapshot | 4 | SC-10 |
| NR-05 | SKILL.md Phase Loading Contract table identical pre/post | diff against Phase 1 snapshot | 4 | SC-10 |
| NR-06 | All 5 refs/ files zero diff | `git diff` on each file | 4 | SC-11 |

### 2.4 Boundary Tests (3 checks) — Acceptance-equivalent

These verify architectural constraints are satisfied.

| ID | Test | Method | Phase | SC |
|----|------|--------|-------|----|
| BT-01 | Zero protocol leakage: grep for `Stage A`, `Stage B`, `rf-task-builder`, `subagent` returns 0 | grep | 2, 4 | SC-5 |
| BT-02 | No content duplication: migrated strings appear in exactly one file | grep both files | 4 | SC-8 |
| BT-03 | `make verify-sync` exits 0 | exit code | 5 | SC-12 |

---

## 3. Test-Implementation Interleaving Strategy

```
Phase 1 (Prep)     ──► Phase 2 (Create)  ──► Phase 3 (Migrate) ──► Phase 4 (GATE) ──► Phase 5 (Sync+Commit)
  │                      │                      │                     │                    │
  ├─ Baseline snap       ├─ ST-01..ST-13       ├─ MT-07              ├─ ALL 26 checks     ├─ BT-03
  └─ wc -l confirm       └─ BT-01 (early)     └─ BT-02 (early)     └─ HARD STOP         └─ ST-01 (dev copy)
                                                                       on failure
```

**Why 1:3 is correct here**: The 26 formal verification checks concentrate in Phase 4 because:
- Phases 2 and 3 produce artifacts that are meaningless to verify in isolation against the full fidelity matrix — you need both the command file and the modified SKILL.md before cross-file checks make sense.
- Phase 4 is cheap (~10 min of parallel grep/diff/wc) and catches everything before the irreversible Phase 5 commit.
- Inline checks in Phases 2–3 catch obvious structural errors early (wrong line count, protocol leakage) without the overhead of a full gate.

A 1:1 ratio would add unnecessary ceremony for a LOW-complexity task. A 1:3 ratio concentrates verification at the single point where it matters most: after all content changes are complete and before commit.

---

## 4. Risk-Based Test Prioritization

Tests are prioritized by the risk they mitigate:

**P0 — Run first in Phase 4** (mitigate RISK-02, RISK-01):
1. BT-01: Protocol leakage (RISK-02, Medium severity)
2. NR-01..NR-05: Behavioral protocol unmodified (RISK-03)
3. NR-06: Refs files unmodified (RISK-03)

**P1 — Run second in Phase 4** (mitigate RISK-01):
4. MT-01..MT-06: Migrated content present in command (RISK-01)
5. BT-02: No duplication (RISK-01)
6. MT-07: SKILL.md line count (RISK-01)

**P2 — Run in Phase 5** (mitigate RISK-04):
7. BT-03: `make verify-sync` (RISK-04)
8. ST-01 on dev copy paths (RISK-04)

**Rationale**: Protocol leakage (RISK-02) is the highest-severity risk. Content loss (RISK-01) is lower severity but has more checks. Sync failure (RISK-04) is caught by the build pipeline. Running P0 checks first in Phase 4 means the most dangerous defects are caught earliest.

---

## 5. Acceptance Criteria Per Milestone

### Phase 1 Milestone: "Ready to implement"
- [ ] `adversarial.md` read and section ordering internalized
- [ ] SKILL.md confirmed at 438 lines (`wc -l`)
- [ ] Migration blocks confirmed at lines 48–63 and 82–88
- [ ] Baseline snapshot saved: `wc -l`, copies of migration blocks, `git diff --stat`

**Gate**: Informational only. Proceed if all items confirmed.

### Phase 2 Milestone: "Command file structurally correct"
- [ ] `src/superclaude/commands/tdd.md` exists
- [ ] Line count 100–170 (ST-02)
- [ ] All 7 flags present (ST-06..ST-12)
- [ ] Activation contains `Skill tdd` (ST-13)
- [ ] Zero protocol leakage (BT-01)

**Gate**: Soft. A failure here is MAJOR — fix before proceeding to Phase 3.

### Phase 3 Milestone: "Content migrated, no duplication"
- [ ] SKILL.md line count 400–440 (MT-07)
- [ ] Migrated strings absent from SKILL.md (BT-02 early check)
- [ ] 4-input description retained in SKILL.md (lines 34–46)
- [ ] "What to Do If Prompt Is Incomplete" retained (lines 65–76)
- [ ] Tier selection rules retained (lines 90–94)

**Gate**: Soft. A failure here is MAJOR — fix before Phase 4.

### Phase 4 Milestone: "Fidelity verified — zero collateral damage" (HARD GATE)
- [ ] All 13 structural tests pass
- [ ] All 7 migration tests pass
- [ ] All 6 non-regression tests pass
- [ ] All 3 boundary tests pass (BT-01, BT-02 confirmed)
- [ ] Total: 26/26 checks green

**Gate**: HARD. Any failure is CRITICAL. Do not proceed to Phase 5. Fix and re-run all 26 checks.

### Phase 5 Milestone: "Shipped"
- [ ] `make sync-dev` completes without error
- [ ] `make verify-sync` exits 0 (BT-03)
- [ ] Both file locations exist: `src/superclaude/commands/tdd.md` and `.claude/commands/sc/tdd.md`
- [ ] Key Phase 4 checks re-run on `.claude/` dev copies pass
- [ ] Single atomic commit created

**Gate**: Soft. A `make verify-sync` failure is CRITICAL — do not commit.

---

## 6. Quality Gates Between Phases

| Gate | Between | Type | Pass Criteria | Failure Action |
|------|---------|------|---------------|----------------|
| G1 | Phase 1 → 2 | Informational | Baseline snapshot exists, line counts confirmed | Re-read files, re-measure |
| G2 | Phase 2 → 3 | Soft | ST-02 + ST-06..ST-13 + BT-01 all pass | MAJOR: fix command file before migration |
| G3 | Phase 3 → 4 | Soft | MT-07 + BT-02 early check pass | MAJOR: fix migration before verification |
| **G4** | **Phase 4 → 5** | **Hard** | **26/26 checks pass** | **CRITICAL: stop-and-fix. Re-verify after fix.** |
| G5 | Phase 5 → Commit | Soft | `make verify-sync` exit 0, dev copies exist | CRITICAL: do not commit until sync passes |

**Escalation policy**: If a CRITICAL issue is found at G4, the implementer must:
1. Identify which specific check(s) failed
2. Trace failure to the originating phase (2 or 3)
3. Fix in canonical source (`src/superclaude/`)
4. Re-run all 26 Phase 4 checks (not just the failed one — fixes can have side effects)
5. Only proceed to Phase 5 when 26/26 pass
