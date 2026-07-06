# Research: Test & Verification Infrastructure (pr_submit V1.1)

**Track:** R5 — Test Infrastructure / Patterns / Fixtures / Markers
**Scope:** `tests/pr_submit/` + `pyproject.toml [tool.pytest.ini_options]`
**Status:** IN PROGRESS
**Date:** 2026-06-12

---

## File Inventory

`tests/pr_submit/` (21 test modules + conftest + fixtures/):

- conftest.py (2448 bytes)
- __init__.py (empty)
- fixtures/ (18 JSON fixtures)
- test_autonomy_gates.py, test_crash_recovery.py, test_detection_contract.py,
  test_edge_cases.py, test_finding_verify.py, test_hook_update.py,
  test_idempotency.py, test_loop_guard.py, test_monitor_arm.py,
  test_pre_pr_checks.py, test_rate_limit.py, test_reply_resolve.py,
  test_run_log.py, test_severity_router.py, test_skill_parse.py,
  test_static_grep.py, test_timeout.py, test_troubleshoot_seed.py,
  test_validated_not_verified.py, test_validation_gate.py

---

## 1. conftest.py — shared fixtures & the injected-seam pattern

File: `tests/pr_submit/conftest.py` (header cites spec §6.3; in-process monkeypatch
preferred over PATH-shim per `research/04 §D`).

Five shared fixtures (`conftest.py:20-81`):

| Fixture | Lines | Purpose |
|---|---|---|
| `load_fixture` | 20-27 | Loader: `load_fixture("name.json")` → parsed JSON from `fixtures/`. Returns a `_load(name)` closure that reads `FIXTURES_DIR / name`. |
| `mock_gh` | 30-51 | Monkeypatches the **detection poll seam** `superclaude.pr_submit.detection._fetch_payload` to a fake. Returns a recorder with `.payload` (settable poll payload, default `{"reviews":[],"comments":[]}`) and `.calls` (list of `pr_num` args). In-process, no subprocess. |
| `mock_monitor` | 54-65 | Stand-in for the Monitor-arming seam; `.calls` counter increments per `__call__`. |
| `fixture_findings` | 68-73 | Loads the default `finding-medium-high.json` (the AC-2 medium+high set). |
| `tmp_skill_dir` | 76-81 | `tmp_path/"pr-monitor"` dir for run-log / artifact writes. |

`FIXTURES_DIR = Path(__file__).parent / "fixtures"` (`conftest.py:17`).

### The RunConfig injected-seam pattern (THE driving mechanism)

The deterministic core is driven WITHOUT real gh/git via the `RunConfig` dataclass
(`src/superclaude/pr_submit/fsm.py:653-677`) passed to `run_skill(config)`
(`fsm.py:679`). RunConfig carries **inputs** + **side-effect seams** (each default
keeps the core pure / recording-only):

Inputs (`fsm.py:657-668`):
- `monitor_ordinal:int=0`, `max_rounds:int`, `poll_interval`, `timeout`,
  `pr_number`, `resume:str|None`
- `findings: list[Finding]` — the (first) cycle's classified/normalized findings
- `rereview_findings: list[list[Finding]]` — each entry = residual finding set at
  the next re-review (this drives the loop-guard off-by-one tests)
- `review_state: str = "findings"` — one of `"polling"|"clean"|"findings"`

Side-effect seams (`fsm.py:670-676`) — all default to `_noop` / pure recorders:
- `arm_monitor: Callable[...,None]=_noop`
- `verify: Callable[[Finding],bool]=_default_verify`
- `apply_edits: Callable[[list[Finding]],int]=_default_apply_edits`
- `run_validation: Callable[...,str]=lambda **_:"validated"`
- `do_push`, `do_reply`, `do_resolve` = `_noop`

`run_skill(config|None, **overrides)` (`fsm.py:679-693`): tests either pass a
`RunConfig(...)` or kwargs that build one; overrides `setattr` onto an existing
config. **Tests inject outcomes by setting `findings`/`rereview_findings`/
`review_state` and (when asserting side effects) swapping a seam callable for a
recorder.** No real `gh`/`git` ever runs. `SkillResult` (returned) exposes
`.state`, `.round_counter`, `.push_count`, `.reply_count`, `.applied_edits`,
`.summary_posted`, `.findings`.

V1.1 builder note: NEW seams for decline + auggie-fallback (decline-poll callable,
fallback-findings provider, fallback_round_counter) will be ADDED to RunConfig in the
same default-pure style — mirror the existing `Callable=_noop` / list-input pattern.
Confirm exact new field names against R1-R4 core-source research before writing items.

---

## 2. fixtures/ — JSON schema (verified shapes)

`tests/pr_submit/fixtures/` holds 18 JSON files. Three distinct schemas:

### (a) Review/poll payload schema (gh-API-shaped)
Used by `mock_gh.payload` and detection-contract tests. Verified files:
`review-clean.json`, `review-with-findings.json`, `review-interleaved.json`,
`review-non-augment.json`. Shape:
```json
{
  "reviews": [
    {"author": {"login": "augment-code[bot]"},
     "authorAssociation": "NONE", "state": "COMMENTED",
     "body": "...", "has_findings": true}
  ],
  "comments": [
    {"user": {"login": "augment-code[bot]"}, "path": "src/app/db.py",
     "line": 88, "body": "...", "id": 3002}
  ]
}
```
Key fields: `reviews[].author.login` (the bot-login the classifier matches),
`reviews[].has_findings` (bool driving polling/clean/findings), `reviews[].state`,
`comments[].user.login`, `comments[].path/line/body/id`. NOTE the canonical bot
login in fixtures is `"augment-code[bot]"` (`review-with-findings.json:4`), distinct
from the production override login `"augmentcode[bot]"` used in detection-contract
tests (`test_detection_contract.py:118` / `:106`). **V1.1 decline fixtures (decline
comments / re-review attribution) extend THIS payload schema** — a decline comment is
a `comments[]` (or a review `body`) carrying the decline marker text the new decline
regex matches.

### (b) Finding-set schema
`{"findings": [ {...} ]}`. Each finding (verified `finding-high.json`,
`finding-medium-high.json`, `finding-needs-human.json`, `finding-ungroundable.json`):
```json
{"path": "src/app/db.py", "line": 88, "body": "...",
 "severity_hint": "high", "category": "resource-leak",
 "confidence": "high", "in_diff": true, "comment_id": 3002}
```
Optional flags seen: `needs_human_decision: true` (`finding-needs-human.json`),
`verification_status: "verified"` (`finding-ungroundable.json`, round-sequence files).
These map onto the `Finding` model (path/line/body/in_diff/verification_status/
comment_id/severity_hint/category/confidence/needs_human_decision). The
`fix_key`/idempotency hash is `fix_key(path, line, body)` — **comment_id-independent**
(`test_idempotency.py:67`).

### (c) Round-sequence / scenario schema (multi-cycle + expected block)
`round-sequence-2.json`, `round-sequence-residual-x3.json`. Shape:
```json
{"max_rounds": 2,
 "note": "...",
 "cycles": [ {"round": 0, "findings": [ {finding...} ]}, ... ],
 "expected": {"round_counter": 2, "push_count": 2, "terminal": "HALT_MAX_ROUNDS"}}
```
The `expected` block is asserted for parity against the computed `SkillResult` (see
`test_loop_guard.py:62-64` reading `round-sequence-residual-x3.json`). Crash fixtures
(`crash-after-push-before-completed.json`) use `{"note","events":[...],"expected":{...}}`
where `events[]` are run-log JSONL fragments with `event_type` + idempotency keys.
`behavioral-drift.json` uses `{"note","finding":{...},"validation_status",
"behavioral_test_failures":[...]}`.

### V1.1 NEW fixtures — schema each must follow (§9.1)
All 7 are decline/re-review/auggie scenarios → most extend schema (a) (poll payload)
or (c) (scenario+expected). The builder MUST specify shape per file:
- `decline-comment.json` — schema (a): a `comments[]`/review carrying the decline
  marker text; the new decline regex (R4 source) must match it. Add an `expected`
  block (state stays/transitions to the decline 4th-state).
- `rereview-attributed.json` — schema (a)/(c): a re-review whose head SHA is
  attributed to our push → INV-R1 increments the (real) round_counter.
- `rereview-then-decline.json` — schema (c): cycle sequence re-review→decline;
  `expected` asserts deferred-increment + decline terminal.
- `rereview-then-decline.json` / `decline-twice.json` — schema (c): two decline
  observations; `expected` asserts resume strict-once (decline recorded once).
- `decline-initial-poll.json` — schema (a): decline present on the FIRST poll (no
  prior re-review) → exercises the decline path without a round tick.
- `stale-decline-pre-watermark.json` — schema (a)/(c): a decline comment older than
  the watermark → ignored (not classified as a fresh decline); `expected` shows no
  state change. Watermark field shape TBD — confirm vs R4 detection-source research.
- `auggie-fallback-findings.json` — schema (b) finding-set: the findings the auggie
  fallback path produces when the primary Augment review is unavailable; drives
  `test_auggie_fallback.py` T-1110..T-1125. Include `fallback`/provenance marker if
  the core distinguishes fallback-sourced findings (confirm vs R3/R4).

---

## 3. Existing test patterns to mirror (per-module, with assertion style)

### test_loop_guard.py (INV-001 / round_counter) — the P0 surface
- Imports: `from superclaude.pr_submit.fsm import RunConfig, run_skill`;
  `from superclaude.pr_submit.loop_guard import RoundCounter, should_halt, user_label`;
  `from superclaude.pr_submit.models import Finding, MonitorState` (`:14-16`).
- Local helpers `_f(line)` builds a verified in-diff `Finding` (`:19-27`); `_run(max_rounds,
  residual_cycles)` builds `rereview_findings=[[_f(...)] for ...]` and calls
  `run_skill(RunConfig(...))` (`:30-40`).
- Markers: `@pytest.mark.loop_guard` + `@pytest.mark.p0` (`:43-44`).
- Assertion style: direct equality on `result.round_counter`, `result.push_count`,
  `result.state == MonitorState.HALT_MAX_ROUNDS`, `result.summary_posted` (`:55-58`).
- **Fixture-parity pattern**: load `round-sequence-residual-x3.json`, assert
  `fixture["expected"]["round_counter"] == result.round_counter == 2` (`:62-64`).
- `@pytest.mark.parametrize` fence-post matrix `(max_rounds,residual,exp_counter,exp_pushes)`
  (`:69-114`).
- Pure-unit on RoundCounter: `should_halt(2,2) is True` (`>=` semantics), `user_label(0)==1`
  (`:118-123`); monotonicity via `RoundCounter(max_rounds=2)` + `.on_rereview(review_observed,
  sha_attributed_to_our_push)` + `.vanished_rereview()` asserting `.value` never decrements
  (`:128-140`).
- V1.1 EXT: INV-R1/R3 (deferred increment), `fallback_round_counter` cap-1 → mirror the
  `RoundCounter(...)` direct-unit style AND the `_run`/parametrize scenario style.

### test_idempotency.py (idempotency sets)
- Imports `Finding`, `from superclaude.pr_submit.run_log import RunLog, fix_key` (`:11-12`).
- Pattern: `rl = RunLog(pr_num, tmp_path)`; `rl.record_idempotent("replied_comment_ids", id)`
  returns `True` first time, `False` on replay (`:20-23`); count events via list-comp filter
  `[e for e in rl.read_events() if e["event_type"]=="reply_posted"]` then `assert len(...)==1`
  (`:25-29`). Idempotency SET NAMES used: `"replied_comment_ids"` (`:20`),
  `"processed_finding_ids"` (`:72`). Persistence: second `RunLog` over same dir
  `.rebuild_state()` shows the id (`:38-42`). NO marker decorator on these tests (plain
  `def test_*`).
- `fix_key` is comment_id-independent: `original.fix_key == fresh.fix_key ==
  fix_key("src/auth.py",42,"missing authz check")` (`:64-68`).
- V1.1 EXT: 6th idempotency set (decline) + resume strict-once → mirror the
  `record_idempotent(<new_set_name>, key)` True-then-False pattern; confirm the new set
  name against R3 run_log source.

### test_run_log.py (EventType enum + events)
- Imports `RunConfig, run_skill`, `Finding`, `from ...run_log import RunLog, fix_key`
  (`:15-17`). Some tests `@pytest.mark.recovery`, others plain.
- `RunLog(pr_num, tmp_path).append({"event_type": ..., ...})`; assert `rl.jsonl_path.exists()`,
  `rl.read_events()` populated with timestamp/round_counter/state_after (`:21-47`).
- JSONL well-formedness: read `jsonl_path.read_text().splitlines()`, `json.loads` each, assert
  `event_id` monotonic `== list(range(1,n+1))` and unique (`:61-79`).
- Redaction (T-N51): append a body with `ghp_...`/`Bearer ...`/`GITHUB_TOKEN=...`, assert no
  raw token in `jsonl_path.read_text()` and `"[REDACTED]" in raw` (`:83-100`).
- Determinism (T-N52): `run_skill(make_config())` twice, assert the 5-tuple
  `(state, round_counter, push_count, reply_count, applied_edits)` equal (`:103-143`).
- **EventType enum**: `EventType(str, Enum)` lives in `src/superclaude/pr_submit/models.py:19-70`,
  docstring "EXACTLY 33 members" (`:20`). NO existing test asserts the count numerically
  (verified: only the docstring/module-comment say 33). The 33 members are listed
  `models.py:29-70` (the 32 from spec §11.3 + `push_aborted_or_not_landed`).
  **V1.1 "37-member enum" assertion is NEW** — the builder should add a test
  `assert len(EventType) == 37` (or `len(list(EventType))`) plus assert the 4 new members
  exist by name. The 4 new event types come from R3/R6 — pattern to mirror for "EXACTLY N
  members": there is NO existing numeric-count test, so the builder establishes it; the
  closest precedent is `_VALID_EVENT_VALUES = frozenset(e.value for e in EventType)`
  (`run_log.py:35`) which the writer validates against. Recommend: named-member existence
  assertions + `len(EventType)==37`. Also update the docstring "EXACTLY 33"→"EXACTLY 37"
  (a static-grep / parity check could catch staleness — see T-1105/T-1115 below).
- V1.1 EXT: 4 new events, clamp/min fold → mirror the `append`+`read_events`+filter pattern.

### test_detection_contract.py (DetectionContract / classify)
- Imports `from superclaude.pr_submit import (DetectionContract, DetectionContractLocked,
  classify, poll_augment_review)` (`:20-25`). `AUGMENT = "augment-code[bot]"` (`:27`).
- `@pytest.fixture contract` builds a synthetic locked `DetectionContract(augment_bot_login=...,
  augment_author_association=[...], emission_shape="review", findings_locus="comments[]",
  locked=True)` (`:30-40`).
- `classify(payload, contract)` returns `"polling"|"clean"|"findings"`; assertions are
  `assert classify(payload, contract) == "findings"` (`:43-72`). **Payloads are PROVISIONAL
  inline dicts** (header `:10-13` says Phase 10 swaps them for `load_fixture(...)`).
- Locked gate: `with pytest.raises(DetectionContractLocked): DetectionContract.load()` (`:75-97`);
  override-arming via `monkeypatch.setattr(detection,"_LOCAL_OVERRIDE_PATH", override)` +
  `DetectionContract.for_arming()` (`:99-124`).
- V1.1 EXT: decline regexes, 4th state, watermark. **4th classify return value** — today
  `classify` returns 3 strings; the decline state ADDS a 4th. Mirror the
  `assert classify(payload, contract) == "<decline-state>"` pattern with a decline payload.
  Confirm the decline state's literal string token against R4 detection source. Watermark:
  a new field on the contract or a poll-time arg; the stale-decline-pre-watermark fixture
  exercises it.

### test_static_grep.py (T-N50 NFR-6 core-purity)
- Path anchors (`:17-21`): `REPO_ROOT = Path(__file__).resolve().parents[2]`;
  `SKILL_DIR = REPO_ROOT/"src"/"superclaude"/"skills"/"sc-pr-submit-protocol"`;
  `HOOK = .../hooks/scripts/offer-pr-review.sh`;
  `PR_SUBMIT_PKG = REPO_ROOT/"src"/"superclaude"/"pr_submit"`.
- `CORE_PURE_FILES` (`:27-34`): the refs `state-machine.md`, `severity-routing.md`,
  `loop-guard.md` AND `fsm.py`, `severity_router.py`, `loop_guard.py`.
- **T-N50 grep** (`:98-109`): `token = re.compile(r"\bgh\b|\bgit\b")`; iterate
  `CORE_PURE_FILES`, assert each exists, scan every line, collect `f"{path}:{lineno}: {line}"`
  offenders, `assert not offenders`.
- T-104 fork-scope (`:86-95`): `_GH_CMD = re.compile(r"\bgh\s+(pr|api|repo|release|run|auth|
  search|workflow)\b")`; `_command_lines(path)` yields only real command lines (`.sh`: skip
  `#`-comments, join `\`-continuations; `.md`: only inside fenced code blocks — `:45-78`);
  `_fork_scoped(line)` = FORK in line OR `--repo` OR `graphql` (`:81-83`).
- T-N41 anthropic-import ban (`:130-139`): scan `PR_SUBMIT_PKG.glob("*.py")` for
  `^\s*(import|from)\s+anthropic\b`.
- T-105 runtime pin (`:148-186`): scans `poll-augment-review.sh` for `gh pr`/`gh api` lines.
- V1.1 EXT: **T-N50 must scan the NEW core refs** (decline/fallback state-machine additions) —
  add the new ref `.md` files + any new `*.py` core modules to `CORE_PURE_FILES`.
  **T-1105/T-1115 static parity**: new static-grep tests asserting decline/auggie skill prose
  parity with core — mirror the `read_text().splitlines()` + regex + offenders-list +
  `assert not offenders` idiom.

---

## 4. pyproject.toml markers & collection

`[tool.pytest.ini_options]` (`pyproject.toml:104-144`):
- `testpaths=["tests"]`, `python_files=["test_*.py"]`, `python_classes=["Test*"]`,
  `python_functions=["test_*"]` (`:105-108`).
- `addopts = ["-v","--strict-markers","--tb=short"]` (`:109-113`). **`--strict-markers`
  means EVERY marker must be registered in the `markers=[...]` list or collection ERRORS.**
- pr_submit-relevant markers ALREADY registered (`:139-143`):
  - `inv` (INV-001/002/003/005/007/010/014) `:139`
  - `loop_guard` (Loop-guard / round-counter fence-post, INV-001) `:140`
  - `autonomy` (Autonomy-tier gate) `:141`
  - `recovery` (Crash-recovery / resume reconstruction, FM-1..12) `:142`
  - `p0` (P0 priority acceptance) `:143`
- There is NO `detection`, `decline`, `auggie`, or `fallback` marker today.
- **V1.1 builder action**: if new tests use a NEW marker (e.g. `@pytest.mark.decline` or
  `@pytest.mark.auggie`), it MUST be added to `markers=[...]` or `--strict-markers` fails the
  whole suite. SAFEST: reuse existing markers — decline/re-trigger tests fit `loop_guard`/`inv`;
  auggie-fallback tests fit `recovery`/`inv` or plain (no marker, like test_idempotency.py).
  Recommend the builder add an explicit task item gating any new marker on a `pyproject.toml`
  edit. Collection is path-based (`tests/pr_submit/test_*.py` auto-collected); `tests/pr_submit/
  __init__.py` exists (empty) so it's a package.

---

## 5. Verification commands (project convention)

Per CLAUDE.md + memory (`make test`=`uv run pytest`; tests in `tests/`, NO inline `python -c`):

```
uv run pytest tests/pr_submit/ -v                         # whole pr_submit suite
uv run pytest tests/pr_submit/test_review_retrigger.py -v # NEW V1.1 module
uv run pytest tests/pr_submit/test_auggie_fallback.py -v  # NEW V1.1 module
uv run pytest tests/pr_submit/test_loop_guard.py -v       # EXT (INV-R1/R3)
uv run pytest tests/pr_submit/ -m loop_guard              # by marker
uv run pytest tests/pr_submit/ -m "loop_guard or recovery"
```

CI parity (memory `make lint ≠ CI ruff format`) — BOTH must pass before push:
```
make lint                                    # ruff check only
uv run ruff format --check src/ tests/       # CI runs this SEPARATELY — green make lint ≠ green CI
```
So every new/edited test file under `tests/pr_submit/` must be `ruff format`-clean. Builder
should add a final "run `uv run ruff format --check src/ tests/`" verification item.

---

## 6. V1.1 test-delta map (§9.1) — infrastructure view

Both NEW modules confirmed NET-NEW (do not exist today):
`test_review_retrigger.py`, `test_auggie_fallback.py` (verified via `ls` — absent).
Core has ZERO `decline`/`fallback`/`watermark`/`fallback_round_counter` tokens today
(verified `grep -rln` over `src/superclaude/pr_submit/` → empty) — these are all R1-R4
core additions the tests will exercise.

| File | Type | IDs | Mirror pattern | New fixtures |
|---|---|---|---|---|
| test_review_retrigger.py | NEW | T-1101..T-1106, T-PUSH-WITHOUT-REREVIEW-NO-TICK | test_loop_guard.py `_run`/RoundCounter + parametrize | rereview-attributed.json, decline-comment.json |
| test_auggie_fallback.py | NEW | T-1110..T-1118, T-1120..T-1125, T-AUGGIE-AT-MOST-ONCE | test_idempotency.py (at-most-once True/False) + test_run_log.py (event filter) | auggie-fallback-findings.json |
| test_detection_contract.py | EXT | decline regexes, 4th state, watermark | `classify(payload,contract)==<state>` | decline-comment.json, decline-initial-poll.json, stale-decline-pre-watermark.json |
| test_idempotency.py | EXT | 6th set, resume strict-once | `record_idempotent(<set>,k)` True-then-False | decline-twice.json |
| test_loop_guard.py | EXT | INV-R1/R3, deferred increment, fallback_round_counter cap-1 | RoundCounter direct-unit + `_run` | rereview-then-decline.json |
| test_run_log.py | EXT | 4 new events, 37-member enum, clamp/min fold | `append`+`read_events` filter + NEW `len(EventType)==37` | (uses inline RunConfig) |
| test_static_grep.py | EXT | T-N50 scans new refs, T-1105/T-1115 static parity | regex + offenders-list | (none) |

Key infra facts for the builder:
- **Enum count today = 33** (`models.py:20` docstring; members `:29-70`). V1.1 → **37**
  (4 new events). The 37-member test is NET-NEW (no numeric count test exists). Also flip
  the docstring "EXACTLY 33"→"EXACTLY 37" and the module-level comment at `models.py:3`.
- **classify return set today = 3** (`polling/clean/findings`). V1.1 adds a 4th (decline).
- **idempotency sets today = EXACTLY 5** [CORRECTED — this section originally miscounted as 4
  by dropping `processed_review_ids`; re-verified against source by the A.8 gate]. The full
  tuple at `run_log.py:27-33` is: `processed_review_ids`, `processed_finding_ids` (keyed on
  fix_key), `replied_comment_ids`, `resolved_thread_ids`, `pushed_commit_shas` (rebuilt at
  `:159-189`). The module comment literally reads "The 5 idempotency sets". V1.1 adds the **6th**
  set `auggie_review_invoked` (spec §6.3/§9.1) → **5 → 6**. There is NO contradiction and NO
  phantom "5th set" — the test assertion is `"auggie_review_invoked" in run_log.IDEMPOTENCY_SETS`
  (now len 6) + True-then-False `record_idempotent("auggie_review_invoked", pr_number)`. Builder:
  anchor on **5→6**; do NOT propagate any "4"/"reconcile"/"maybe a 5th" framing into a test.
- **CORE_PURE_FILES (`test_static_grep.py:27-34`) must grow** to include new decline/fallback
  core refs + modules, else T-N50 won't cover them.
- Bot login: fixtures use `augment-code[bot]`; production override login is
  `augmentcode[bot]` (`test_detection_contract.py:106,118`). Decline fixtures should use the
  fixture convention `augment-code[bot]` to match existing review fixtures.

---

## Status: COMPLETE

### Summary
Documented the full pr_submit test infrastructure for V1.1 task authoring. The deterministic
core is driven via the `RunConfig` injected-seam dataclass (`fsm.py:653-677`) → `run_skill`
(`fsm.py:679`): tests set `findings`/`rereview_findings`/`review_state` inputs and swap
`Callable=_noop` side-effect seams for recorders — no real gh/git. conftest.py supplies
`load_fixture`, `mock_gh` (monkeypatches `detection._fetch_payload`), `mock_monitor`,
`fixture_findings`, `tmp_skill_dir`. Three fixture schemas verified: (a) gh-shaped poll payload
`{reviews[],comments[]}`, (b) finding-set `{findings:[{path,line,body,severity_hint,...}]}`,
(c) scenario `{max_rounds,cycles[],expected{}}`. All 7 V1.1 fixtures mapped to a schema.
Five mirror-pattern modules profiled with file:line assertion idioms. Markers: `loop_guard/
recovery/p0/inv/autonomy` are registered; `--strict-markers` is ON so any NEW marker must be
added to `pyproject.toml:114-144`. Verified: both new test modules are net-new; core has no
decline/fallback/watermark tokens yet; EventType is EXACTLY 33 today (→37) with NO existing
numeric-count test (37-member assertion is net-new). CI requires BOTH `make lint` and
`uv run ruff format --check src/ tests/`.
