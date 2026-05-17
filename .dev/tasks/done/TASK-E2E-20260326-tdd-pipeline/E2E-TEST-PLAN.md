# End-to-End Test Plan: TDD Pipeline Integration

## Context

We made extensive changes across two work streams:
1. **CLI layer** (TASK-RF-20260325-cli-tdd): 9 Python files modified — auto-detect + `--input-type` flag, `build_extract_prompt_tdd()`, executor branching, fidelity prompt generalization, tasklist `--tdd-file` flag
2. **Skills layer** (TASK-RF-20260325-001): 6 markdown files modified — extraction Steps 9-15, 7-factor scoring formula, spec-panel Steps 6a/6b, sc-tasklist `--spec` implementation, PRD-to-TDD handoff

All testing so far was unit-level. Nothing tested the actual pipeline flow. We need three end-to-end tests to confirm everything works:

1. **TDD in modified repo** — does the new TDD path work?
2. **Spec in modified repo** — did we break the existing spec path?
3. **Spec in original repo** — baseline comparison to prove #2 produces identical results

---

## Test Fixtures

### Fixture 1: Populated TDD (created first)

**Source template:** `src/superclaude/examples/tdd_template.md` (1300+ lines, 28 numbered sections, all pipeline frontmatter fields we added)

Copy template to `.dev/test-fixtures/test-tdd-user-auth.md` and populate for a "User Authentication Service". Replace ALL placeholder brackets with real content. The sentinel self-check requires: `feature_id` not `[FEATURE-ID]`, `spec_type` is a valid enum, `target_release` not `[version]`.

**Frontmatter to populate:**
- `id: "AUTH-001-TDD"`, `title: "User Authentication Service - Technical Design Document"`
- `type: "📐 Technical Design Document"` (already in template)
- `feature_id: "AUTH-001"`, `spec_type: "new_feature"`, `target_release: "v1.0"`, `authors: ["test-engineer"]`
- `complexity_score: ""`, `complexity_class: ""` (leave empty — computed by pipeline)

**Key sections to populate (these are what our extraction changes target):**

| Section | Content | Tests |
|---|---|---|
| §5 Technical Requirements | 5 FRs (`FR-AUTH-001`–`FR-AUTH-005`) + 3 NFRs | EXTRACT_GATE `functional_requirements` count, `spec_parser.py` FR-xxx matching |
| §6 Architecture | ASCII diagram + 2 design decisions | Architectural Constraints extraction |
| §7 Data Models | TypeScript interfaces (`UserProfile`, `AuthToken`) + field table | New "Data Models and Interfaces" extraction section |
| §8 API Specifications | 4 endpoints (login, register, me, refresh) in endpoint table + request/response | New "API Specifications" extraction section |
| §10 Component Inventory | Route table + 3 components (`LoginPage`, `RegisterPage`, `AuthProvider`) | New "Component Inventory" extraction section |
| §15 Testing Strategy | Test pyramid table + 3 test cases | New "Testing Strategy" extraction section |
| §19 Migration & Rollout | 3-phase rollout table + rollback steps + feature flags | New "Migration and Rollout Plan" extraction section |
| §20 Risks | 3 risks in risk table | Risk Inventory extraction |
| §24 Release Criteria | 5-item DoD + release checklist | Success Criteria extraction |
| §25 Operational Readiness | 2 runbook scenarios + on-call table | New "Operational Readiness" extraction section |

Other sections: populate minimally (1-2 sentences). §9, §16, §17, §26 brief but real.

**Fingerprint coverage:** Key identifiers as backticked names: `UserProfile`, `AuthToken`, `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `LoginPage`, `RegisterPage`, `AuthProvider`. Roadmap must mention ≥70% for ANTI_INSTINCT_GATE.

### Fixture 2: Spec from the release-spec-template (created second)

**Source template:** `src/superclaude/examples/release-spec-template.md` — the standard spec template the pipeline has always used.

Copy the release-spec-template to `.dev/test-fixtures/test-spec-user-auth.md` and populate it for the SAME "User Authentication Service" feature. This is the standard spec format — the kind of document the pipeline was originally built to consume.

- Use the release-spec-template's YAML frontmatter structure exactly (with `{{SC_PLACEHOLDER:...}}` sentinels replaced with real values)
- Use the release-spec-template's section structure (NOT TDD numbered sections)
- Write requirements as behavioral "shall/must" statements — the format `build_extract_prompt()` was designed for
- Cover the same auth feature scope (login, register, token refresh, user profile) so the roadmap output is comparable to Test 1
- Include `FR-001` through `FR-005` and `NFR-001` through `NFR-003` as the pipeline's `spec_parser.py` expects

This spec must:
- NOT trigger auto-detection as TDD (it uses the spec template structure, not numbered TDD sections)
- Work in BOTH the modified repo AND the original unmodified repo (it's a standard spec — nothing about it depends on our changes)
- Cover the same feature scope as the TDD so roadmap comparison is meaningful

**The same spec file is used for Test 2 and Test 3.**

---

## Three Tests

### Test 1: TDD in Modified Repo

**What it proves:** The new TDD extraction path works end-to-end — auto-detection routes to `build_extract_prompt_tdd()`, all 14 sections are extracted, the roadmap covers TDD-specific content, and all gates pass.

**Command:**
```bash
superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --output .dev/test-fixtures/results/test1-tdd-modified/
```

No `--input-type` flag — auto-detection should detect TDD and route correctly.

**Verify:**

| Artifact | What to check |
|---|---|
| stderr output | "[roadmap] Auto-detected input type: tdd" printed. TDD warning about DEVIATION_ANALYSIS_GATE printed. |
| `extraction.md` | All 13 required YAML fields present (passes EXTRACT_GATE). All 14 body sections present including 6 new TDD sections: "Data Models and Interfaces", "API Specifications", "Component Inventory", "Testing Strategy", "Migration and Rollout Plan", "Operational Readiness". `data_models_identified > 0`, `api_surfaces_identified > 0`. |
| `roadmap-*.md` (2 files) | Reference TDD content: `UserProfile`, `AuthToken`, endpoint paths, component names. |
| `roadmap.md` | Merged roadmap contains milestones for auth endpoints, data models, testing, migration. Key backticked identifiers from TDD appear. |
| `anti-instinct-audit.md` | `fingerprint_coverage >= 0.7`. `undischarged_obligations == 0`. `uncovered_contracts == 0`. |
| `test-strategy.md` | Has `complexity_class`, `validation_philosophy: continuous-parallel`, `interleave_ratio`. |
| `spec-fidelity.md` | Uses "source-document fidelity analyst" language. Has comparison dimensions: API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness. |
| `diff-analysis.md`, `debate-transcript.md`, `base-selection.md` | Exist and pass their respective gates. |

### Test 2: Spec in Modified Repo

**What it proves:** Our modifications did not break the existing spec path. The same spec file produces a valid roadmap through the standard 8-section extraction, with no TDD content leaking in.

**Command:**
```bash
superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --output .dev/test-fixtures/results/test2-spec-modified/
```

No `--input-type` flag — auto-detection should detect spec and route to `build_extract_prompt()`.

**Verify:**

| Artifact | What to check |
|---|---|
| stderr output | "[roadmap] Auto-detected input type: spec" printed. NO TDD warning. |
| `extraction.md` | Standard 8 body sections ONLY. NO "Data Models and Interfaces", NO "API Specifications", NO "Component Inventory". Only 13 frontmatter fields (NO `data_models_identified` etc.). |
| `roadmap.md` | Valid roadmap covering auth requirements. |
| `anti-instinct-audit.md` | Passes — `fingerprint_coverage >= 0.7`. |
| All gates | Pass through the full pipeline including deviation-analysis (spec path is fully compatible). |

### Test 3: Spec in Original Unmodified Repo

**What it proves:** Baseline comparison. The original pipeline (before our changes) produces valid output from the same spec. We compare Test 2 output against Test 3 output to confirm our modifications didn't alter spec-path behavior.

**Setup:** Use a git worktree or checkout of the `master` branch (commit `4e0c621` — before our feature branch changes).

```bash
# Create a worktree at the pre-change commit
git worktree add ../IronClaude-baseline master

# Copy the spec fixture into the baseline repo
cp .dev/test-fixtures/test-spec-user-auth.md ../IronClaude-baseline/.dev/test-fixtures/test-spec-user-auth.md

# Run the pipeline in the baseline repo
cd ../IronClaude-baseline
superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --output .dev/test-fixtures/results/test3-spec-baseline/
```

**Verify:**

| Artifact | What to check |
|---|---|
| `extraction.md` | Standard 8 body sections, 13 frontmatter fields. Should be structurally identical to Test 2's extraction. |
| `roadmap.md` | Valid roadmap. Content will differ (different Claude runs produce different text) but structure and coverage should be comparable. |
| All gates | Pass through full pipeline. |

### Comparison: Test 2 vs Test 3

After both complete, compare:

| Comparison Point | Test 2 (Modified) | Test 3 (Baseline) | Expected |
|---|---|---|---|
| extraction.md section count | 8 | 8 | Same |
| extraction.md frontmatter field count | 13 | 13 | Same |
| extraction.md has TDD sections | No | No | Same |
| Prompt used | `build_extract_prompt()` | `build_extract_prompt()` | Same function (unmodified) |
| fidelity prompt language | "source-document fidelity analyst" | "specification fidelity analyst" | Different — this is the one expected diff |
| Anti-instinct passes | Yes | Yes | Same |
| Pipeline completes fully | Yes | Yes | Same |

The ONLY expected difference between Test 2 and Test 3 is the fidelity prompt language ("source-document" vs "specification"). If any other structural difference appears, our changes broke something.

---

## Files to Create

| File | Purpose |
|---|---|
| `.dev/test-fixtures/test-tdd-user-auth.md` | Populated TDD from template — used in Test 1 |
| `.dev/test-fixtures/test-spec-user-auth.md` | Spec derived from TDD content — used in Tests 2 and 3 |
| `.dev/test-fixtures/results/test1-tdd-modified/` | Test 1 output directory |
| `.dev/test-fixtures/results/test2-spec-modified/` | Test 2 output directory |
| `.dev/test-fixtures/results/test3-spec-baseline/` | Test 3 output directory (in worktree) |

## Execution Order

1. Create the TDD fixture (from template)
2. Create the spec fixture (derived from TDD)
3. Run Test 1 (TDD in modified repo)
4. Run Test 2 (spec in modified repo)
5. Set up baseline worktree, run Test 3 (spec in original repo)
6. Compare Test 2 vs Test 3 outputs
7. Write verification report

## Expected Duration

- Fixture creation: ~15 minutes
- Test 1 (TDD pipeline): ~30-60 minutes
- Test 2 (spec pipeline, modified): ~30-60 minutes
- Test 3 (spec pipeline, baseline): ~30-60 minutes
- Comparison + report: ~15 minutes

Total: ~2-3 hours wall-clock, mostly waiting for Claude subprocesses.

## Success Criteria

1. **Test 1:** TDD auto-detected, 14-section extraction produced, roadmap references TDD content, all gates pass through spec-fidelity
2. **Test 2:** Spec auto-detected, standard 8-section extraction, no TDD content leaks, full pipeline completes
3. **Test 3:** Baseline produces valid output from same spec
4. **Test 2 vs 3:** Structurally identical extraction and pipeline behavior, only fidelity prompt language differs
5. No Python errors or crashes in any test
6. Deviation-analysis may fail for Test 1 only (known TDD limitation, warning printed)
