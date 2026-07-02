# BUILD REQUEST

Source: user
TASK_ID_PREFIX: TASK-RF
TEMPLATE: 02
QA_INTENSITY: standard
QA_GATE_REQUIREMENTS: FINAL_ONLY
TESTING_REQUIREMENTS: UNIT
SPEC: /config/workspace/IronClaude/.dev/brainstorms/20260702-165220-sprint-429-detector-hardening/merged-requirements.md

GOAL: Harden the sprint 429/account-exhaustion provider-failure detector so recovery ALWAYS
engages for the real CLIProxyAPI "API Error: 429" transcript shape (Shape 2), instead of the
phase silently cascading to FAIL_TERMINAL. Implement the two mandated hunks in ONE file
(`src/superclaude/cli/sprint/monitor.py`) exactly as the merged-requirements spec specifies, then
add the fixtures + detection-contract table test + live/offline parity tests that would have caught
the incident. This is a narrow production change (2 hunks) + a medium verification surface.

The two mandated production hunks (see spec §4 R1/R2, confirmed live by research/01):
  - HUNK 1 (C1, monitor.py:323): widen the entry predicate from
      `if is_error and api_error_status == 429:`
    to
      `if is_error and (api_error_status == 429 or "rate_limit_error" in body):`
    INLINE the disjunct — NO new helper, NO regex, NO nested-JSON parse. `body`, `is_error`,
    `api_error_status` locals already exist at :319-321.
  - HUNK 2 (C8, monitor.py:41-43): loosen `_RE_ALL_ACCOUNT` from
      r"All credentials for model (?P<model>.+?) are cooling down via provider"
    to
      r"All credentials for model (?P<model>.+?) are cooling down"
    (drop `via provider`; keep the non-greedy model capture). `_RE_SINGLE_ACCOUNT` at :44 is unchanged.

Everything else in monitor.py — the timeout branch (:335-338), the neither-body default (:332-333),
the enum, the dataclass — stays BYTE-UNCHANGED. Do NOT touch the offline mirror
(`rerun_tasks.py`), the policy (`recovery_policy.py`), the executor, `models.py`, or `aienv.py`:
they are correct and one inner-function edit fixes both live and offline paths (research/01 confirmed
`_classify_transcript` at rerun_tasks.py:592→:605 delegates to the shared inner).

WHY: PR #183 shipped a full 429 recovery subsystem, but on the real July incident the detector's
entry predicate required a structured `api_error_status == 429` field the transcript does not carry
(Shape 2 has `is_error:true` but NO `api_error_status`; the 429 is text-only + a nested
`rate_limit_error`). So the classifier returned NONE, recovery never engaged, and every task in the
phase cascaded to FAIL_TERMINAL. EMPIRICALLY VERIFIED this turn: the current detector returns
`ProviderFailure.NONE` on the verbatim Shape-2 transcript; the loosened regex captures `gpt-5.5`.

BYTE-EXACT SHAPE-2 FIXTURE SOURCE (ANTI-FABRICATION — CRITICAL):
The load-bearing new fixture MUST be built from the VERBATIM real transcript at
`${TASK_DIR}research/shape2-verbatim-transcript.jsonl` (3 lines: init, synthetic assistant, result).
The fixture `tests/sprint/fixtures/exhaustion/all_account_cooldown_apierror429.jsonl` MUST reproduce
that file's `result` line BYTE-FOR-BYTE. Do NOT hand-fabricate or paraphrase the JSON — fabricating
the shape is precisely what caused the original incident (the 6 existing fixtures encode the WRONG
assumed shape). The detector keys on the LAST `{"type":"result"}` line.

DELIVERABLES (each its own granular checklist item per A3/B2):
1. HUNK 2 (regex loosening) in monitor.py — its own item.
2. HUNK 1 (predicate widening) in monitor.py — its own item.
3. Fixture `all_account_cooldown_apierror429.jsonl` (verbatim Shape-2 all-account) — its own item,
   built from the reference transcript above.
4. Fixture `provider_429_incidental_ratelimit_text.jsonl` (FP guard: `is_error:false`, body contains
   literal "429"/"rate limit" prose → expected NONE) — its own item.
5. Fixture `single_account_apierror429_SYNTHESIZED.jsonl` (Shape-2 single-account assumption
   breakpoint; name MUST contain `_SYNTHESIZED`; header/comment documents it is synthesized because no
   verbatim capture exists; assumes `would exceed your account's rate limit` phrasing) — its own item.
6. The detection-contract table test in `tests/sprint/test_monitor.py` — a `pytest.mark.parametrize`
   over the ~12-row matrix from spec §6.2 (api_error_status {429|absent|null} × via-provider
   {present|absent} × prefix {Request-rejected|API-Error-429}); each row asserts
   `(kind, resolved_model)`; empty/impossible cells are explicit `xfail`/skip with a reason (never
   silent). Assert `resolved_model` on EVERY row incl. `None` on non-cooldown rows (OQ4). Its own item
   (may be split: author the parametrize table, then the test body).
7. Four live/offline parity assertions (spec §6.3) — each its own item:
   (a) `detect_provider_failure(path)` == `_provider_failure_from_text(text)` on the Shape-2 fixture
       (extends the existing `test_text_core_matches_path_wrapper` at test_monitor.py:336-343);
   (b) `_classify_transcript(shape2_text)` → `TaskStatus.FAIL_PROVIDER_EXHAUSTED`
       (import/call form per research/02; test seam
       `test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion`);
   (c) `_classify_transcript` on the FP fixture → NOT `FAIL_PROVIDER_EXHAUSTED`;
   (d) Shape-2 transcript with a prior success envelope then trailing 429 →
       `completed_before_overrun_from_text` intercept → PASS_RECOVERED (unchanged).
8. Timeout unreachability guard test (F5): assert a 429 body never reaches the timeout branch (every
   is_error 429 returns inside the 429 block before :335) — its own item.
9. Regression verification: all 6 existing Shape-1 fixtures + existing `test_monitor.py` +
   `test_recovery_policy.py` assertions still pass unchanged (R3) — its own item.

SCOPE DISCIPLINE (do NOT do — from spec §5 "CHANGES WE ARE NOT MAKING"): no new ProviderFailure kind /
TaskStatus; no config knob/flag; no `_is_rate_limited()` helper/registry; no nested-JSON unescaping; no
sibling-detector (`detect_error_max_turns`/`detect_prompt_too_long`) refactor; no policy/executor edit;
no timeout-branch edit; no property/fuzz suite. Do NOT duplicate the `decide()` truth table (it lives
in `test_recovery_policy.py`; C3 applies to tests too).

VALIDATION_REQUIREMENTS: After code+tests land: `uv run pytest tests/sprint/test_monitor.py
tests/sprint/test_recovery_policy.py tests/sprint/test_rerun_tasks.py -q` all green; the full
`uv run pytest tests/sprint/ -q` green; `uv run ruff check src/superclaude/cli/sprint/monitor.py
tests/sprint/` clean; `uv run ruff format --check src/ tests/` clean (NOTE: `make lint` only runs ruff
check — CI separately runs ruff format --check; run BOTH). `make verify-sync` clean (this task touches
`cli/` + `tests/` only — no skills/agents/commands, so no sync-dev needed, but verify-sync must stay
green). Scope ruff to changed files to avoid the worktree-ruff-version reformat footgun.

EXECUTION_CONTEXT_INSTRUCTION: Populate `## Execution Context`:
  - References: this GOAL; the merged-requirements spec; research/01 (change surface), research/02
    (test conventions), research/03 (template), and the shape2 verbatim reference.
  - Source areas: `sprint monitor detector`, `sprint exhaustion fixtures`, `sprint monitor tests`
    (module/dir names only — NO file:line in the block).
  - Key constraints: two hunks only in monitor.py; back-compat (old-match ⊆ new-match); build fixtures
    from the verbatim transcript, never fabricate; C3 scope discipline.

POST_REFLECT_GATE: ENABLED
  TASK_FILE: ${TASK_DIR}${TASK_ID}.md

FRONTMATTER GATE KEYS (contract §6):
  start_commit: 156f28292b4ddba09cefb89e5f160cbd2475e875   # git merge-base HEAD origin/master, this build
  executor_model_class: opus                                # user's default session model class
  task_type: static

DOCUMENTATION STALENESS WARNINGS: None. research/01 CODE-VERIFIED every monitor.py / rerun_tasks.py /
recovery_policy.py / executor.py / models.py / aienv.py citation against current source (2026-07-02);
all line numbers in the spec hold exactly.

RESEARCH DIR: ${TASK_DIR}research/  (read ALL .md + the shape2 .jsonl reference)
  - 01-detector-change-surface.md — exact monitor.py expressions + read-only consumer confirmation
  - 02-test-and-fixture-conventions.md — test_monitor.py structure, fixtures, contract-table + parity
  - 03-template-examples.md — MDTM 02 rules + prior TASK-RF structural patterns
  - shape2-verbatim-transcript.jsonl — BYTE-EXACT fixture source (anti-fabrication)

OPEN QUESTIONS: OQ2 (no verbatim Shape-2 single-account transcript) — RESOLVED by the
`_SYNTHESIZED` breakpoint fixture (deliverable 5). Document as an assumption/risk, not a blocker.

GRANULARITY: one item per hunk, per fixture, per test group. NO batch items. NO one-shot file writes.
