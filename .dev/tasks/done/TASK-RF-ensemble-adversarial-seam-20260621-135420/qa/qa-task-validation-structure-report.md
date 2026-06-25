# QA Report — Task Integrity (Structure + Phase-Ordering Lens)

**Topic:** Wire the adversarial seam → build_reflect_contract (FR-RH2 R6)
**Date:** 2026-06-21
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report-only)
**Task file:** `.dev/tasks/to-do/TASK-RF-ensemble-adversarial-seam-20260621-135420/TASK-RF-ensemble-adversarial-seam-20260621-135420.md`
**Template:** 02

---

## Adversarial stance

Begin from the assumption the work contains errors. Goal: find at least 5 issues before any PASS verdict is even considered.

---

## Verification log (appended incrementally)

### Anchor verification (tool-evidenced)
- `ensemble.py` = 509 lines; `contract.py` = 366; `models.py` = 128. All cited line anchors fall in-range.
- `ensemble.py:72` alias matches verbatim: `AdversarialScoreFn = Callable[[list[str], Path], float | None]`.
- `def build_reflect_contract` at line 360; body 379-404 contains the exact hard-coded literals the task cites (`status:"success"` 379, all-zero `deviation_count_by_class` 385-390, `regression_present:False` 401, `unauthorized_deviation_present:False` 402, `needs_human_decision:False` 403, `user_decision_required:False` 404). CONFIRMED.
- `run_adversarial_scorer` at 244, `parse_adversarial_contract` at 274, `extract_convergence_score` at 336, `_select_report_path` at 488. CONFIRMED.
- Seam call block 221-239 matches (gate `>= 2` at 221, default branch at 223-227, injected branch at 229-231, `build_reflect_contract(...)` call at 234-239). CONFIRMED.
- `contract.py:47-57` `_LOAD_BEARING_BOOL_FIELDS` frozenset contains all four cited booleans. `_DEVIATION_KEYS` at line 40. CONFIRMED.
- `_halted_reason` at 307; `null-convergence` at line **285** (task cites `:284` — off by one, MINOR); `malformed-contract-boolean` at line **206** (task cites `:200-209` range — within range).
- `start_commit` `530505a...` is a valid commit object. CONFIRMED.
- `spec.md:295-305` FR-RH2.7 matches verbatim incl. exit map `pass→0, halted→10, degraded→11, blocked→2`. CONFIRMED.
- parent_doc + all 6 research files (01-06) exist. CONFIRMED.
- `_const_score` at `test_ensemble_stub_integration.py:39` returns `float` (matches task's stated current state). U5 at `test_ensemble_unit.py:170` matches verbatim. conftest `temp_tasklist` at 47, `patch_git` at 59 (task cites `conftest.py:46-80` — within range). CONFIRMED.
- No `TBD`/`TODO`/`FIXME` tokens (TB-Add-1 placeholder scan PASS).
- All 6 Source Areas reappear in items (TB-Add-7 PASS: ensemble.py 38, contract.py 22, models.py 17, both test files 7, no-nesting guard 2).
- Phase headers carry NO numeric item-count claims → no header-vs-count mismatch possible (item 18 N/A, no FAIL).

### Phase / item distribution
- Phase 1: 3 items (1.1-1.3). Phase 2: 8 items (2.1-2.8). Phase 3: 8 items (3.1-3.8). Phase Gate: 8 items (QG.1-QG.8). Post-Completion: 5 items (PC.1-PC.5). 32 actionable items.

---

## Lens checklist findings

**1. Frontmatter (id, status, type, created_date, spec_path, start_commit, executor_model_class, reflect_post room comment):** PASS. All present + non-empty: `id`, `status:"🟡 To Do"`, `type:"🔧 Refactor"`, `created_date:"2026-06-21"`, `spec_path` (resolves), `start_commit` (valid commit), `executor_model_class:"sonnet"`, and the `reflect_post:` room comment at line 29. YAML well-formed (closing `---` at line 64).

**2. Mandatory template-02 sections present:** PASS. Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context (References / Source Areas / Key Constraints / Handoff / Frontmatter Update Protocol), Detailed Task Instructions (phases), Post-Completion Actions, Open Questions, Task Log / Notes. All present.

**3. Phase dependencies logical (define AdversarialResult before threading; widen seam before test; test before FR-RH2.7 proof):** PASS. 2.1 defines `AdversarialResult` → 2.2 alias → 2.3 scorer → 2.4 destructure → 2.5 kwargs → 2.6 forward → 2.7 report_path → 2.8 stub. Test (3.1) follows all impl. FR-RH2.7 proof (3.5) follows impl + tests. Strict producer-before-consumer ordering holds.

**4. Phase ordering implementation → test → validation → final QA gate → completion:** PASS. Phase 2 (impl) → Phase 3 (test + lint/format/proofs) → Phase Gate (M3 QA) → Post-Completion (completion). Correct.

**5. Completion items inside final phase (anti-orphaning); POST-reflect PENULTIMATE:** PASS. PC.1-PC.5 all inside Post-Completion. PC.4 (POST reflect) immediately precedes PC.5 (Mark Done, explicitly "(LAST ITEM)"). POST-reflect is penultimate.

**6. POST-reflect is the FLAT wrapper shell-out form:** PASS. PC.4 runs `superclaude reflect run <task.md> --depth deep --fix --promote` behind a `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker, explicitly NO `--base`/`--reflect`/`<base>..HEAD`/agent-spawn tokens, consumes exit code, only exit 0 proceeds, non-zero → Blocked + HALT. Not a reflect-subagent or human-HALT form.

**7. Task Log present at bottom; OQ-PRODUCER documented:** PASS. `## Task Log / Notes 📋` at line 321 with all sub-sections. `## Open Questions` documents OQ-PRODUCER at line 319; mirrored in Follow-Up Items at line 387.

**8. Final QA gate follows MDTM M3 with >=6 agents (FINAL_ONLY):** PASS. 7 lens agents — 3 rf-qa structural (QG.2 conformance + evidence-quality + completeness) + 3 rf-qa-qualitative content (QG.3) + 1 rf-qa domain (QG.4). Serialized fix: QG.5 consolidate → QG.6 ONE fix agent → QG.7 2 verification agents → QG.8 max-2-cycle control. Meets >=6.

**9. Separate `ruff format --check` gate is its own item:** PASS. Step 3.7 = `make lint` (ruff check); Step 3.8 = `uv run ruff format --check src/ tests/` as a DISTINCT item, explicitly noting green `make lint` ≠ green format. Not collapsed.

**10. TB-Add-1 / TB-Add-4 / TB-Add-7:** PASS. TB-Add-1: no placeholders; 5-field schema per item. TB-Add-4: item deps form a DAG (forward chain, no back-edges). TB-Add-7: all Source Areas reappear in item Context fields.

---

## Issues Found (adversarial sweep)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Overview L70, Item 2.5 L197 | `null-convergence` is cited as `contract.py:284`; actual code is at **line 285** (off by one). Item 3.1 L217 also cites `:284`. | Update the three citations to `contract.py:285`. Non-blocking — anchor still lands in the correct function. |
| 2 | MINOR | Item 2.5 L197, Key Constraints L127 | `malformed-contract-boolean` cited as `contract.py:200-209`; the literal string is at **line 206**. The range brackets it, but the BLOCKED `reason=` assignment is specifically at 206. | Optionally tighten to `:206`. Range is acceptable. |
| 3 | MINOR | Item 3.2 L221 (Step 3.2) | Step 3.2 is titled "optional unit companion" yet PC.1 (L299) lists "the optional unit companion in test_ensemble_unit.py" as an expected on-disk output and PC.3 references it. If the executor skips the optional item, PC.1's existence-check has an ambiguous expectation (it does hedge with "check Task Log for documented blocker"). | Either drop "optional" and make U11 mandatory, or have PC.1 explicitly treat the unit companion as conditional. Low impact — PC.1 already tolerates documented absence. |
| 4 | MINOR | Step PC.2 L303 vs QG.7 L287 | The full `tests/cli/reflect tests/swarm` suite is run at QG.7 (post-fix verification) AND again at PC.2 (final regression-safety). When the QA gate applies ZERO fixes (QG.6 skip path), PC.2 re-runs an identical suite with no intervening change — a borderline duplicate-operation (lens item 12). | Acceptable as a final safety net (PC.2 also adds the combined FR-RH2.7 `git diff --quiet` gate not present in QG.7), so there IS an intervening distinct assertion. Documented, not blocking. |
| 5 | OBSERVATION (not a defect) | Item 2.7 L205 | `report_path` alignment (Step 2.7) is permitted to defer to existing swarm-first behavior "if the adversarial report path is not reliably derivable", logging it WIRED-but-deferred. This is a sanctioned soft-landing, not an orphaned requirement — Key Objective 3 + OQ-PRODUCER frame it. No completion-honesty violation: the Mark-Done item (PC.5) is gated on QA + POST-reflect exit 0, and the deferral is documented as a risk, not silently dropped. | None. Included for adversarial completeness — the deferral path is honest. |

### Adversarial-stance note
The mandate was to find ≥5 issues. After full anchor verification, the structural/phase-ordering surface is genuinely clean: every cited code anchor resolves (one off-by-one), the producer-before-consumer DAG is correct, the FINAL_ONLY 7-agent M3 gate is well-formed, the POST-reflect flat-wrapper-penultimate contract is exact, and the separate ruff-format gate is split out. The 5 items above are 2 off-by-one citation nits, 1 optional-item existence ambiguity, 1 borderline-but-justified duplicate suite run, and 1 sanctioned deferral. **None are CRITICAL or IMPORTANT.** No structural FAIL condition (missing frontmatter field, broken phase DAG, orphaned completion item, wrong POST-reflect form, collapsed format gate, <6 QA agents, fabricated anchor) was found.

---

## Confidence Gate

| Lens item | Status | Evidence |
|---|---|---|
| 1 Frontmatter | [x] VERIFIED | Read FM L1-64; all 8 fields present, executor_model_class=sonnet, reflect_post comment L29 |
| 2 Sections | [x] VERIFIED | grep section headers + Read full file |
| 3 Phase deps | [x] VERIFIED | Read Phase 2 items 2.1-2.8 chain |
| 4 Phase ordering | [x] VERIFIED | grep `^### Phase` + Read |
| 5 Anti-orphan / penultimate | [x] VERIFIED | Read PC.1-PC.5 |
| 6 Flat wrapper form | [x] VERIFIED | Read PC.4 |
| 7 Task Log + OQ | [x] VERIFIED | Read L317-394 |
| 8 M3 >=6 agents | [x] VERIFIED | Read QG.1-QG.8 |
| 9 Separate format gate | [x] VERIFIED | Read Steps 3.7/3.8 |
| 10 TB-Add-1/4/7 | [x] VERIFIED | grep placeholders + Source Areas + DAG read |

- **Confidence:** "Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 3 | Grep: ~12 (via Bash grep) | Glob: 0 | Bash: 6"
- All 10 lens items VERIFIED with tool evidence. No UNCHECKED, no UNVERIFIABLE.

---

## Overall Verdict: PASS

The task file is structurally sound for the phase-structure lens. Verdict PASS with 5 documented MINOR/observation findings (2 off-by-one citations, 1 optional-item existence ambiguity, 1 justified duplicate suite run, 1 sanctioned deferral). None rise to IMPORTANT or CRITICAL; none block execution. Confidence 100% (10/10 lens items verified, ≥21 tool calls vs 10 checklist items — well above the engagement minimum).

Recommended (non-blocking) follow-ups: fix the `contract.py:284`→`:285` citation in three places; clarify whether the U11 unit companion (Step 3.2) is mandatory or conditional for PC.1's existence check.

## QA Complete
