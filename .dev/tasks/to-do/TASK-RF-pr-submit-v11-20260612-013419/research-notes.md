# Research Notes: pr_submit V1.1 — Post-Push Re-Trigger + Oversized-PR Auggie Fallback

**Date:** 2026-06-12
**Scenario:** A (Explicit — driven by a precise, code-grounded V1.1 design addendum)
**Depth Tier:** Deep (6 deterministic-core .py modifications + skill SKILL.md/refs/scripts + ~8 new/extended test files; FSM with hard invariants INV-001/INV-R1/R2/R3; NFR-6 core purity)
**Track Count:** 1 (single cohesive feature extension on a strict dependency DAG: models → classifier/detection → run_log → fsm → skill/refs/scripts → tests)
**Spec Path:** `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec-v1.1-addendum.md` (EXTENDS `merged-spec.md` V1.0 — every V1.0 FR/NFR/AC/INV/EC remains binding)
**Status:** Complete

---

## Context: This is an EXTENSION, not a from-scratch build

V1.0 (`merged-spec.md`) was already implemented — prior task folder
`.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/` shows `status: "🟢 Done"`. The 6
deterministic-core `.py` files, the `sc-pr-submit-protocol` skill package (SKILL.md + 8 refs +
2 scripts), and `tests/pr_submit/` (21 test modules) all EXIST. This V1.1 task MODIFIES/EXTENDS
them per the addendum's FR-8 (post-push re-trigger), FR-9 (oversized-PR decline fallback), and
FR-10 (fallback strict-once + budget clamp), adding two FSM states (S5a/S5b), three invariants
(INV-R1/R2/R3), one idempotency set (`auggie_review_invoked`), four EventType members, and a
small closed-enum + run-log delta.

### Orchestrator grounding pass (anchors VERIFIED against current code, 2026-06-12)

| Spec anchor | Current state | Verdict |
|---|---|---|
| `fsm.py:793` optimistic `round_counter += 1` (FR-8.2 [MOD] REMOVE) | `result.round_counter += 1` at **fsm.py:793** | ✅ exact |
| `fsm.py` `transition()` / `run_skill()` | `transition` at :560, `run_skill` at :679 | ✅ |
| `run_log.IDEMPOTENCY_SETS` (5 sets → add 6th) | 5 members at run_log.py:27 (`processed_review_ids`, `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas`) | ✅ |
| `run_log.rebuild_state` / `record_idempotent` | :145 / :200 | ✅ |
| `models.EventType` "EXACTLY 33 members" (→37) | docstring says "EXACTLY 33 members" at models.py:20 | ✅ |
| `models.MonitorState` S5_AWAITING_REREVIEW present; NO S5a/S5b | `S5_AWAITING_REREVIEW` at models.py:104; no S5a/S5b | ✅ |
| `models.SkillResult` | class at models.py:166 | ✅ |
| `classifier.classify()` returns polling/clean/findings (add `declined`) | STATE_POLLING/CLEAN/FINDINGS; `classify()` at classifier.py:60 | ✅ |
| `detection.DetectionContract` + `from_yaml` + `augment_bot_login` | class at detection.py:56, `from_yaml` at :75 | ✅ |
| `loop_guard.should_halt(round_counter, max_rounds)` | def at loop_guard.py:23 | ✅ |
| 8 skill refs present | augment-poll, detection-contract, finding-verify, loop-guard, severity-routing, state-machine, thread-reply, troubleshoot-dispatch | ✅ |
| 2 skill scripts present | poll-augment-review.sh, reply-resolve-thread.sh | ✅ |
| `commands/auggie-review.md` R2 fallback flags (§2 table) | `--depth quick|standard|deep`:49, `--remediation-offer`:52, `--auggie-model claude-sonnet-4-6`:55, `--post-pr` default true for PR:50 | ✅ all valid |
| MDTM template 02 | `.claude/templates/workflow/02_mdtm_template_complex_task.md` (120KB) | ✅ |

The spec's line citations are CURRENT (code has not drifted since the addendum was authored
~today). Researchers must still RE-VERIFY current line numbers at research time and tag
doc/spec-sourced claims [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED].

---

## EXISTING_FILES

Paths relative to repo root `/config/workspace/IronClaude/`.

### Deterministic core (MODIFY — `src/superclaude/pr_submit/`)
- **`models.py`** (~7.4KB) — `EventType` (closed enum, "EXACTLY 33 members", :20), `MonitorState`
  (:83, has `S5_AWAITING_REREVIEW`, `TERMINAL_STATES` frozenset :117), `SkillResult` (:166).
  **V1.1 delta (§6.1):** EventType += `REREVIEW_REQUESTED`, `DECLINE_DETECTED`,
  `AUGGIE_FALLBACK_INVOKED`, `MAX_ROUNDS_CLAMPED` (→37, update docstring count);
  MonitorState += `S5A_RETRIGGER_REVIEW`, `S5B_AUGGIE_FALLBACK` (neither terminal);
  SkillResult += `rereview_request_count`, `fallback_engaged`, `auggie_review_invoked`,
  `decline_detected`, `effective_max_rounds`, `fallback_round_counter`.
- **`classifier.py`** (~3.7KB) — `STATE_POLLING/CLEAN/FINDINGS` (:17-19), `classify(payload, contract)`
  (:60). **V1.1 delta (§6.2):** add `STATE_DECLINED = "declined"`; `classify()` returns it when an
  Augment-authored comment matches decline regexes; decline check runs BEFORE clean/findings branch.
- **`detection.py`** (~8.3KB) — `DetectionContract` (:56), `from_yaml` (:75), `augment_bot_login`,
  `DetectionContractLocked`. **V1.1 delta (§6.2):** add `decline_phrase_regex`,
  `decline_retrigger_regex`, `accepted_trigger_phrases: list[str]` (defaults baked, probe-lockable);
  extend `from_yaml`; add pure `is_decline(comment, contract, *, watermark) -> bool`.
- **`run_log.py`** (~9.6KB) — `IDEMPOTENCY_SETS` (5-tuple, :27), `rebuild_state()` (:145),
  `record_idempotent()` (:200), closed-enum validation in `append`. **V1.1 delta (§6.3):**
  `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` (→6); `rebuild_state()` folds
  `AUGGIE_FALLBACK_INVOKED.pr_number`→`auggie_review_invoked`, `MAX_ROUNDS_CLAMPED.effective_max_rounds`
  →min, counts `REREVIEW_REQUESTED`→`rereview_request_count`.
- **`fsm.py`** (~33KB) — `transition()` (:560), `run_skill()` (:679), optimistic
  `result.round_counter += 1` (**:793** — FR-8.2 REMOVE), `RunConfig`. **V1.1 delta (§6.4):**
  new edges (RESOLVING→S5A [MOD was →S5], S5A→S5, S5→S5B on declined, S2_CLASSIFY→S5B on declined,
  S5B→S2 fallback re-enter, S5B→HALT/CLEAN on fallback_skip); remove :793 increment, tick only on
  injected attributed-re-review; new RunConfig seams `do_retrigger`, `invoke_auggie_review`,
  `rereview_outcome` sequence; `clamp_max_rounds(effective, hard=1)` pure; fallback sub-loop uses
  `loop_guard.should_halt(fallback_round_counter, 1)`. **NFR-6:** NO gh/git token in core.
- **`loop_guard.py`** (~3KB) — `should_halt(round_counter, max_rounds)` (:23). **V1.1 delta:**
  reused for fallback sub-loop (cap 1); INV-R1/R3 documented in `refs/loop-guard.md` (not core code).
- (Out of explicit target list but adjacent: `recovery.py`, `severity_router.py`, `__init__.py` —
  `__init__.py` may need new export wiring for `clamp_max_rounds`/`is_decline`/`STATE_DECLINED`.)

### Skill package (MODIFY/ADD — `src/superclaude/skills/sc-pr-submit-protocol/`)
- **`SKILL.md`** (~10.6KB) — Wave/Phase structure (:70), Wave 6 (L3 push+reply+resolve), Wave 7
  (loop/terminate). **V1.1 delta (§6.5):** Wave 6 [MOD] post `auggie review` comment (S5a) then poll
  (S5); new Wave 6b (decline fallback) strict-once gate → `> Skill sc:auggie-review-protocol` with §2
  flags → re-enter Waves 2-6 once under clamp.
- **`refs/augment-poll.md`** [MOD] — document 4th `declined` state + decline surfaces.
- **`refs/loop-guard.md`** [MOD] — add INV-R1/R2/R3 + independent `fallback_round_counter`.
- **NEW `refs/review-retrigger.md`** (R1) — re-trigger comment surface + watermark + INV-R1.
- **NEW `refs/auggie-fallback.md`** (R2/R3) — decline detection, strict-once, clamp, re-entry
  contract, §2 flag table, "do NOT take the App's bait" rationale.
- **NEW `scripts/retrigger-review.sh`** — one `gh api …/issues/<N>/comments` POST of trigger token,
  pins `--repo`/path to the fork (IronbellyOrg/IronClaude).

### Tests (ADD/EXTEND — `tests/pr_submit/`)
- **NEW `test_review_retrigger.py`** — T-1101..T-1106, T-PUSH-WITHOUT-REREVIEW-NO-TICK.
- **NEW `test_auggie_fallback.py`** — T-1110..T-1118, T-1120..T-1125, T-AUGGIE-AT-MOST-ONCE.
- **EXT `test_detection_contract.py`** — decline regexes, 4th `declined` state, watermark.
- **EXT `test_idempotency.py`** — `auggie_review_invoked` 6th set, resume strict-once.
- **EXT `test_loop_guard.py`** — INV-R1/R3, deferred increment, `fallback_round_counter` cap-1.
- **EXT `test_run_log.py`** — 4 new events, 37-member enum, clamp/min fold.
- **EXT `test_static_grep.py`** — T-N50 scans new refs; T-1105/T-1115 static parity.
- **NEW fixtures** — `decline-comment.json`, `rereview-attributed.json`, `rereview-then-decline.json`,
  `decline-initial-poll.json`, `decline-twice.json`, `stale-decline-pre-watermark.json`,
  `auggie-fallback-findings.json` (in `tests/pr_submit/fixtures/`).
- Existing conftest at `tests/pr_submit/conftest.py`; fixtures dir at `tests/pr_submit/fixtures/`.

### Reuse / reference surfaces
- `src/superclaude/commands/auggie-review.md` — the R2 fallback command (§2 flags VALIDATED).
- Prior V1.0 research: `.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/research/` (8 files) +
  `research-notes.md` — V1.0 context (component inventory, conventions, integration points).

## PATTERNS_AND_CONVENTIONS
- **Source-of-truth = `src/superclaude/`**; never edit `.claude/` directly; `make sync-dev`
  copies src→.claude; `make verify-sync` gates. `.claude/{skills,commands,agents,hooks}` is
  gitignored sync-dev output (only `.claude/settings.json` tracked).
- **NFR-6 core purity (HARD):** the deterministic core (`superclaude.pr_submit.*`) holds NO
  `gh`/`git` token and makes NO I/O — it only DECIDES. All `gh api` posts + `> Skill` invocations
  live in the SKILL. T-N50 (static grep) enforces this across the new refs/scripts.
- **INV-001 verbatim (HARD):** the `round_counter` edge (`S5_AWAITING_REREVIEW → S2_CLASSIFY` on
  attributed re-review), the `>=` HALT gate, monotonicity, and `max_rounds=N ⇒ N pushes` are
  unchanged. V1.1 only RELOCATES the increment from the optimistic `fsm.py:793` site to the real
  attributed re-review. Two counters (`round_counter`, `fallback_round_counter`) are independent.
- **Closed-enum discipline:** EventType validated in `run_log.append`; the "EXACTLY N members"
  docstring is load-bearing (tests assert the count) — update 33→37 atomically with the additions.
- **Idempotency pattern:** `record_idempotent(set_name, key)` returns True on first record, False on
  repeat; sets rebuild from JSONL via `rebuild_state()` (survives `--resume`).
- **gh/git discipline (CLAUDE.md ABSOLUTE):** every `gh`/`gh api` pins `--repo IronbellyOrg/IronClaude`;
  push `origin` never `upstream`; commit trailer `Co-Authored-By: Claude Opus 4.8 (1M context)`.
- **Test conventions:** pytest under `tests/pr_submit/`, JSON fixtures in `fixtures/`, deterministic
  core driven via injected `RunConfig` seams (no real gh/git in tests). `make test` = `uv run pytest`.
- **CI two-gate gotcha (memory):** `make lint` = `ruff check` only; CI ALSO runs
  `uv run ruff format --check src/ tests/`. Run BOTH before declaring green.

## GAPS_AND_QUESTIONS
- Exact current line numbers WILL shift as edits land — researchers capture the CURRENT anchors;
  the builder must phrase items so the executor re-greps rather than trusting a frozen line.
- `__init__.py` export surface: does adding `clamp_max_rounds`/`is_decline`/`STATE_DECLINED`/new
  EventType members require `__all__` / re-export edits? (Researcher 1 must check `__init__.py`.)
- `state-machine.md` ref: the spec §3 diagrams new edges — does an existing `refs/state-machine.md`
  need a [MOD]? (Spec §6.5 lists augment-poll/loop-guard [MOD] + 2 new refs, but the state diagram
  itself may live in state-machine.md — Researcher 2 confirms whether it needs updating.)
- `recovery.py` / `severity_router.py`: do the new states/events touch crash-recovery rebuild or
  severity routing? (Spec implies fallback findings re-enter the SAME pipeline incl. re-grade —
  Researcher 3 traces whether recovery.py's rebuild must learn the new states.)
- Status enum granularity (spec §11 open decision 1): reuse `terminal_clean`/`terminal_max_rounds`
  vs add `terminal_fallback_*`. Spec RECOMMENDS reuse (non-blocking). → AMBIGUITIES_FOR_USER.

## RECOMMENDED_OUTPUTS
Research files in `${TASK_DIR}research/` (codebase is source of truth; spec is the design intent):
1. `01-core-modules-current-state.md` — File Inventory of the 6 core .py + __init__ + adjacent.
2. `02-fsm-transition-runskill-anatomy.md` — Data Flow Tracer: transition table + run_skill loop +
   the :793 increment + RunConfig seams (the highest-risk surface).
3. `03-runlog-idempotency-enum-patterns.md` — Patterns: idempotency sets, rebuild_state fold,
   closed-enum validation, the "EXACTLY N" docstring contract.
4. `04-skill-refs-scripts-conventions.md` — File Inventory + Conventions of SKILL.md waves, the 8
   refs, 2 scripts, hook conventions, gh/repo-pin discipline.
5. `05-test-infra-fixtures-markers.md` — Test & Verification: conftest, fixture JSON shape, existing
   test patterns for FSM/idempotency/static-grep, pyproject markers.
6. `06-spec-delta-extraction.md` — Solution/Spec mapping: the FR-8/9/10 → file → test matrix, INV
   text verbatim, the §6 build-target deltas, EC table, coverage matrix (the builder's spec index).
7. `07-doc-crossvalidate-anchors.md` — Doc Cross-Validator: verify EVERY spec line citation
   (fsm.py:793, 33-member enum, 5 idempotency sets, S5 states, auggie-review.md flags) against
   current code; tag [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED].

## SUGGESTED_PHASES (researcher assignments — 7 researchers, Deep tier)
- **R1 (File Inventory):** `src/superclaude/pr_submit/{models,classifier,detection,run_log,loop_guard}.py`
  + `__init__.py` + `recovery.py`/`severity_router.py` adjacency. Per-symbol exports, line counts,
  current enum/set membership. Output `01-core-modules-current-state.md`. (R2 owns fsm.py deep-trace;
  R3 owns run_log fold detail — R1 does the breadth pass incl. fsm.py's symbol list only.)
- **R2 (Data Flow Tracer):** `fsm.py` — `transition()` edge table, `run_skill()` loop control flow,
  the `:793` increment site + surrounding cycle, `RunConfig` fields/seams, how outcomes drive states.
  Output `02-fsm-transition-runskill-anatomy.md`. (R1 owns the other 5 modules' inventory.)
- **R3 (Patterns & Conventions):** `run_log.py` idempotency/rebuild/enum-validation + `models.py`
  enum/SkillResult patterns; the "EXACTLY N members" docstring contract; closed-enum append guard.
  Output `03-runlog-idempotency-enum-patterns.md`. (R1 lists the symbols; R3 explains the PATTERNS.)
- **R4 (File Inventory + Conventions):** `skills/sc-pr-submit-protocol/{SKILL.md,refs/*,scripts/*}`
  — wave structure, each ref's role, script shape, gh/repo-pin + fail-open conventions; whether
  state-machine.md needs a [MOD]. Output `04-skill-refs-scripts-conventions.md`.
- **R5 (Test & Verification):** `tests/pr_submit/` — conftest, fixture JSON schema, FSM/idempotency/
  static-grep test patterns, how RunConfig seams are driven in tests, `pyproject.toml` markers.
  Output `05-test-infra-fixtures-markers.md`.
- **R6 (Solution/Spec mapping = Template & Examples surrogate):** Read the addendum + the V1.0
  `merged-spec.md` cross-refs; produce the FR-8/9/10 → §6 file-delta → §9 test matrix, INV-R1/R2/R3
  verbatim, EC-17..24 table, coverage matrix. Also read MDTM template 02 PART 1 (A3/A4/B2 rules) +
  the prior V1.0 task file as a granularity exemplar. Output `06-spec-delta-extraction.md`.
- **R7 (Doc Cross-Validator):** Verify EVERY spec line citation against current source (the grounding
  table above is the seed — extend & re-verify). Tag each [CODE-VERIFIED]/[CODE-CONTRADICTED]/
  [UNVERIFIED]. Output `07-doc-crossvalidate-anchors.md`.

## TEMPLATE_NOTES
- **MDTM template: 02 (Complex).** Discovery (read current code) → modify core (DAG: models →
  classifier/detection → run_log → fsm) → skill/refs/scripts → tests → per-phase QA → source-fidelity
  gate. Conditional flows, parallel QA spawning, hard invariants.
- **Tier: Deep.** 6 core .py modifications + 5 skill artifacts (2 MOD, 2 new refs, 1 new script) + 8
  test files (2 new, 5 ext, fixtures) across 3 subsystems with INV-001/INV-R1/R2/R3 + NFR-6.
- **Granularity (A3/A4):** ONE item per file-delta and per test module. The §6 build-targets and §9
  test matrix already enumerate per-file work — the builder maps each to its own checklist item.
- **QA gates:** Template-02 ⇒ PER_PHASE. QA_INTENSITY: full (regression-class FSM/invariant work).
  Source-fidelity gate (M4/I21) applies — the task transforms a design spec into code+tests and the
  generated task file will exceed 500 lines; fidelity agents read BOTH the addendum AND the produced
  task file.
- **POST_REFLECT_GATE: ENABLED** — spec explicitly names `/sc:reflect --mode pre` to catch the
  INV-001 deferred-increment + strict-once predicates; the templated POST item audits executed work.
- **Validation:** `make lint` + `uv run ruff format --check src/ tests/` + `make verify-sync` +
  `make test` (the full pr_submit suite + new tests). **Testing:** UNIT (deterministic core) — the
  whole feature is test-driven via injected RunConfig seams.

## AMBIGUITIES_FOR_USER
- **Status enum granularity (spec §11.1, non-blocking):** reuse `terminal_clean`/`terminal_max_rounds`
  for fallback outcomes (spec's recommended default, smaller surface) vs add
  `terminal_fallback_clean`/`terminal_fallback_residual`. The task file will follow the spec's
  RECOMMENDATION (reuse) and flag the alternative in Open Questions — not a build blocker.
- Everything else: intent is clear from the addendum + V1.0 spec + verified codebase anchors.
