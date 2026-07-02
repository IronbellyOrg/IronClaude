# Research 02: Test & Verification Conventions + Fixture Format + Contract-Table/Parity Design

Status: Complete

Topic: Test & Verification conventions + fixture format + contract-table/parity design
Scope: `tests/sprint/test_monitor.py`, `tests/sprint/fixtures/exhaustion/`, `tests/sprint/test_recovery_policy.py` (read-only), offline parity target `_classify_transcript`.
Spec: `/config/workspace/IronClaude/.dev/brainstorms/20260702-165220-sprint-429-detector-hardening/merged-requirements.md`

All citations verified against source on 2026-07-02.

---

## 1. `test_monitor.py` — existing detector test conventions

File: `/config/workspace/IronClaude/tests/sprint/test_monitor.py` (344 lines).

### Imports + fixture-path constant (`:8-21`)
```python
from superclaude.cli.sprint.monitor import (
    FILES_CHANGED_PATTERN,
    TASK_ID_PATTERN,
    TOOL_PATTERN,
    OutputMonitor,
    ProviderFailure,
    ProviderFailureSignal,
    _provider_failure_from_text,
    count_turns_from_output,
    detect_error_max_turns,
    detect_provider_failure,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "exhaustion"
```
- The fixture-path constant is `_FIXTURES` (module-level, `:21`). Same identical constant exists in `test_rerun_tasks.py:57`. New parametrized rows reuse `_FIXTURES / "<name>.jsonl"`.
- `ProviderFailureSignal` is imported and available for parity/type assertions.
- `_provider_failure_from_text` (the shared inner) is imported alongside the `detect_provider_failure` path wrapper — both surfaces are already in scope for parity asserts.

### The test class the new parametrized test should live in / match (`:243-344`)
Class `TestDetectProviderFailure` (`:243`), docstring calls out "four-way discrimination over the six exhaustion fixtures". Every test method:
- Is decorated `@pytest.mark.unit` (`:253`, and on EVERY method in the class).
- Calls `detect_provider_failure(_FIXTURES / "<file>.jsonl")` → asserts `sig.kind is ProviderFailure.<KIND>` (identity `is`, not `==`).

Representative existing methods (copy this style for the contract table):
```python
@pytest.mark.unit
def test_single_account_429(self):
    sig = detect_provider_failure(_FIXTURES / "single_account_429.jsonl")
    assert sig.kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT

@pytest.mark.unit
def test_all_account_cooldown_captures_model(self):
    sig = detect_provider_failure(_FIXTURES / "all_account_cooldown.jsonl")
    assert sig.kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN
    assert sig.resolved_model == "claude-opus-4-8"
```
Note: `resolved_model` is asserted with `==` and a plain string (`:262`); `kind` with `is`. The contract-table rows must mirror this: `kind` via `is`, `resolved_model` via `==` (incl. `== None` on non-cooldown rows per OQ4/§6.2).

### Inline-transcript convention for synthetic rows (`:307-333`)
For rows without a fixture file, the class already uses `tmp_path` + `output.write_text('{...json...}\n')` inline. Two examples the builder can mirror for synthetic contract rows 5/6/8:
```python
@pytest.mark.unit
def test_subtype_trap_keys_on_is_error_not_subtype(self, tmp_path):
    output = tmp_path / "output.txt"
    output.write_text(
        '{"type":"result","subtype":"success","is_error":true,'
        '"api_error_status":429,'
        '"result":"API Error: Request rejected (429) · This request would '
        "exceed your account's rate limit. Please try again later.\"}\n"
    )
    assert detect_provider_failure(output).kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT
```
So the builder can choose per-row: real fixture file (rows 1-4,7,9-12 with a file) OR inline `tmp_path.write_text` (synthetic rows 5,6,8). Both call the SAME `detect_provider_failure` surface.

### The existing shared-inner parity assert (`:336-343`)
```python
@pytest.mark.unit
def test_text_core_matches_path_wrapper(self):
    path = _FIXTURES / "all_account_cooldown.jsonl"
    from_text = _provider_failure_from_text(path.read_text())
    from_path = detect_provider_failure(path)
    assert from_text == from_path
    assert isinstance(from_text, ProviderFailureSignal)
    assert from_text.kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN
```
This is the template for parity assertion #1 (§6.3.1): the Shape-2 version replaces the fixture with `all_account_cooldown_apierror429.jsonl` and asserts `.kind is ALL_ACCOUNT_COOLDOWN` + `.resolved_model == "gpt-5.5"`. `ProviderFailureSignal` is a dataclass — `==` compares `(kind, resolved_model)` structurally, so the equivalence assert covers the captured model too.

---

## 2. The 6 existing fixtures — filenames + exact `result`-line JSON shape

Dir: `/config/workspace/IronClaude/tests/sprint/fixtures/exhaustion/`. Format = NDJSON (one JSON object per line; trailing blank line). The classifier keeps the LAST `{"type":"result"}` event. Verbatim contents:

**`all_account_cooldown.jsonl`** → Row 1 (ALL_ACCOUNT_COOLDOWN, `claude-opus-4-8`)
```
{"type":"assistant","message":{"usage":{"output_tokens":120}}}
{"type":"assistant","message":{"usage":{"output_tokens":340}}}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · All credentials for model claude-opus-4-8 are cooling down via provider claude"}
```

**`single_account_429.jsonl`** → Row 2 (SINGLE_ACCOUNT_LIMIT, None)
```
{"type":"system","subtype":"api_retry","error_status":429,"error":"rate_limit","attempt":3,"max_retries":10}
{"type":"assistant","message":{"model":"<synthetic>","usage":{"output_tokens":12}},"error":"rate_limit"}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · This request would exceed your account's rate limit. Please try again later."}
```

**`api_retry_maxed.jsonl`** → Row 3 (SINGLE_ACCOUNT_LIMIT, None; attempt==max==10 corroborating only)
```
{"type":"system","subtype":"api_retry","error_status":429,"error":"rate_limit","attempt":10,"max_retries":10}
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"result":"API Error: Request rejected (429) · This request would exceed your account's rate limit. Please try again later."}
```

**`operation_timeout.jsonl`** → Row 10 (OPERATION_TIMEOUT, None)
```
{"type":"assistant","message":{"usage":{"output_tokens":88}}}
{"type":"result","subtype":"success","is_error":true,"api_error_status":null,"result":"API Error: The operation timed out."}
```

**`task_failure_real.jsonl`** → Row 11 (NONE — real task fail, no 429)
```
{"type":"assistant","message":{"usage":{"output_tokens":210}}}
{"type":"result","subtype":"error_during_execution","is_error":true,"result":"Tool execution failed: pytest exited 1"}
```

**`clean_pass.jsonl`** → Row 12 (NONE — clean pass)
```
{"type":"assistant","message":{"usage":{"output_tokens":150}}}
{"type":"result","subtype":"success","is_error":false,"api_error_status":null,"result":"Task complete."}
```

**Confirmed: all 6 are Shape 1.** Every one that is a 429 carries `"api_error_status":429` present, and the all-account body contains "cooling down **via provider**". `operation_timeout`/`clean_pass` use `"api_error_status":null`; `task_failure_real` omits the field entirely. This is exactly the shape the current detector predicate (`monitor.py:323`, `is_error and api_error_status == 429`) requires — hence the Shape-2 gap.

**Fixture-authoring rule (from these 6):** result line is a single-line JSON object, keys in order `type, subtype, is_error, api_error_status, result` (api_error_status omitted only in the real-failure fixture). File ends with a trailing newline. No BOM, no frontmatter (these are `.jsonl`, so MD025/markdownlint gotchas do NOT apply).

---

## 3. VERBATIM Shape-2 `result` line for the new load-bearing fixture

From spec §3 (grounding table) and §6.1. Shape-2 all-account distinguishing facts:
- `is_error` = `true` (shared with Shape 1 — the one token that survives)
- `api_error_status` = **absent** (NOT null — the field is not emitted at all)
- result prefix = `API Error: 429 {…}` (not "Request rejected (429) · ")
- all-account body = `All credentials for model gpt-5.5 are cooling down` (**no** "via provider" suffix)
- nested envelope = `{"error":{"message":"b'{…rate_limit_error…}'","code":"429"}}`
- model = `gpt-5.5`
- shape-robust tokens present: `is_error:true` + `rate_limit_error` ∈ body + `All credentials for model gpt-5.5 are cooling down`

**Authoring instruction for the builder (AUTHORITATIVE — supersedes any "raw logs / ground-truth" pointer below):** The byte-exact Shape-2 source now exists in this task folder at `research/shape2-verbatim-transcript.jsonl` — a REAL captured transcript (3 lines: `system/init`, synthetic `assistant`, `result`; real `session_id` `0a06b2fc-…`, `duration_ms:181906`). **The builder MUST author `all_account_cooldown_apierror429.jsonl` by copying the LAST `{"type":"result"}` line of `research/shape2-verbatim-transcript.jsonl` VERBATIM (byte-for-byte).** Do NOT hand-fabricate or paraphrase it — fabricating the expected shape is precisely the failure that caused the original incident (§10 "against under-engineering"). Note: `.dev/troubleshoot/429-signature-ground-truth.md` contains Shape 1 ONLY (no `gpt-5.5`, no `API Error: 429`) — do NOT source the Shape-2 fixture from it.

The following is a **NON-AUTHORITATIVE illustration ONLY** (it drops the real `"type":"None","param":"None"` envelope fields and telemetry, so it is NOT byte-equal to the capture — do NOT copy it into the fixture):
```
{"type":"result","subtype":"success","is_error":true,"result":"API Error: 429 {\"error\":{\"message\":\"b'{\\\"type\\\":\\\"error\\\",\\\"error\\\":{\\\"type\\\":\\\"rate_limit_error\\\",\\\"message\\\":\\\"All credentials for model gpt-5.5 are cooling down\\\"}}'\",\"code\":\"429\"}}"}
```
Key invariants that MUST hold in the copied verbatim line: (a) NO `api_error_status` key; (b) substring `rate_limit_error` present in `result`; (c) substring `All credentials for model gpt-5.5 are cooling down` present with NO "via provider"; (d) `is_error":true`. These four are what R1+R2 key on. The builder MUST verify the authored fixture classifies to ALL_ACCOUNT_COOLDOWN/gpt-5.5 by running the new test (RED before the monitor.py fix, GREEN after). VERIFIED this turn: the current unpatched detector returns `ProviderFailure.NONE` on `research/shape2-verbatim-transcript.jsonl` (the bug), and the loosened C8 regex captures `gpt-5.5`.

### The 3 new fixtures the spec names (§6.1)
1. **`all_account_cooldown_apierror429.jsonl`** — verbatim Shape 2 all-account (`gpt-5.5`, no `api_error_status`, no "via provider", nested LiteLLM envelope). Load-bearing regression fixture → Row 4. Expected `(ALL_ACCOUNT_COOLDOWN, "gpt-5.5")`.
2. **`provider_429_incidental_ratelimit_text.jsonl`** — FP guard. `"is_error":false`, result body contains literal `429`/`rate limit` prose → expected `NONE`. → Row 9.
3. **`single_account_apierror429_SYNTHESIZED.jsonl`** — Shape-2 single-account assumption-breakpoint (OQ2; no verbatim capture exists). Name MUST include `_SYNTHESIZED`. Documents assumed `would exceed your account's rate limit` phrasing WITHOUT `api_error_status`. → Row 7. Expected `(SINGLE_ACCOUNT_LIMIT, None)`. Add an in-test comment marking it as a synthesized assumption that "flips to a loud failure if a real capture later contradicts it."

---

## 4. Offline parity target — `_classify_transcript`

### Import path + call form
- Defined: `/config/workspace/IronClaude/src/superclaude/cli/sprint/rerun_tasks.py:552`, `def _classify_transcript(text: str) -> TaskStatus`.
- Takes a **text string** (the transcript body), NOT a path. Call form: `_classify_transcript(text)` where `text = (_FIXTURES / "<file>.jsonl").read_text()`.
- Delegates to the shared inner at `rerun_tasks.py:592`: `_sig = _provider_failure_from_text(text)`; if `_sig.kind in (SINGLE_ACCOUNT_LIMIT, ALL_ACCOUNT_COOLDOWN)` → returns `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (unless a prior success envelope → `PASS_RECOVERED`, `:603-605`). **This is why hardening the one inner fixes both live and offline** (R6).

### Existing test pattern to match (the seam to extend)
File: `/config/workspace/IronClaude/tests/sprint/test_rerun_tasks.py`, class `TestClassifyTranscriptProviderExhaustion` (`:794-828`). Imports at `:33-49`:
```python
from superclaude.cli.sprint.models import (GateOutcome, Phase, SprintConfig, TaskEntry, TaskResult, TaskStatus)
from superclaude.cli.sprint.rerun_tasks import (_classify_transcript, ...)
```
`_FIXTURES` const at `:57` (identical to test_monitor's). Existing methods (copy this exact form for the new parity asserts):
```python
def test_all_account_cooldown_classifies_provider_exhausted(self):
    text = (_FIXTURES / "all_account_cooldown.jsonl").read_text()
    assert _classify_transcript(text) is TaskStatus.FAIL_PROVIDER_EXHAUSTED

def test_real_failure_not_over_captured(self):
    text = (_FIXTURES / "task_failure_real.jsonl").read_text()
    assert _classify_transcript(text) is TaskStatus.FAIL_TERMINAL

def test_completed_then_trailing_429_recovers_not_exhausted(self):
    success_line = '{"type":"result","subtype":"success","is_error":false,"result":"Task complete."}\n'
    text = success_line + (_FIXTURES / "single_account_429.jsonl").read_text()
    assert _classify_transcript(text) is TaskStatus.PASS_RECOVERED
```
Note the class methods here are NOT `@pytest.mark.unit`-decorated (unlike test_monitor's) — match the surrounding class's convention when adding to it.

### The 4 live/offline parity assertions (§6.3), mapped to the exact surfaces
1. **§6.3.1** — extends `test_monitor.py:336-343`: on `all_account_cooldown_apierror429.jsonl`, assert `_provider_failure_from_text(path.read_text()) == detect_provider_failure(path)` and `.kind is ALL_ACCOUNT_COOLDOWN` and `.resolved_model == "gpt-5.5"`. Lives in `test_monitor.py` (`TestDetectProviderFailure`).
2. **§6.3.2 (the untested seam)** — in `test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion`: `_classify_transcript((_FIXTURES / "all_account_cooldown_apierror429.jsonl").read_text()) is TaskStatus.FAIL_PROVIDER_EXHAUSTED`.
3. **§6.3.3** — same class: `_classify_transcript((_FIXTURES / "provider_429_incidental_ratelimit_text.jsonl").read_text()) is not TaskStatus.FAIL_PROVIDER_EXHAUSTED` (use `is not`; the FP fixture is `is_error:false` so it should be `PASS`/`NONE`-classified, never provider-exhausted).
4. **§6.3.4** — same class: Shape-2 body with a prior `success` envelope prepended → `PASS_RECOVERED` (mirror the existing `test_completed_then_trailing_429_recovers_not_exhausted` at `:815-828` but with the Shape-2 fixture as the trailing terminal), proving R-gate ordering survives the new shape.

---

## 5. The ~12-row contract-table matrix (parametrize-ready)

Matrix dimensions (spec §6.2): `api_error_status {429 | absent | null} × via-provider {present | absent} × prefix {Request-rejected | API-Error-429}`. Each row asserts `(kind, resolved_model)`. Empty/impossible cells → explicit `pytest.param(..., marks=pytest.mark.xfail(reason=...))` or skip — NEVER silent omission (so a THIRD future drift maps to exactly one visible failing row). Per-row `resolved_model` (incl. `None`) is asserted per OQ4/§6.2.

Enum members (verified `monitor.py:272-275`): `ProviderFailure.NONE`, `.SINGLE_ACCOUNT_LIMIT`, `.ALL_ACCOUNT_COOLDOWN`, `.OPERATION_TIMEOUT`.

| # | is_error | api_error_status | body signature | Expected kind | Expected model | Source (fixture or inline) |
|---|---|---|---|---|---|---|
| 1 | true | 429 | Shape1 all-account (via provider) | ALL_ACCOUNT_COOLDOWN | `"claude-opus-4-8"` | fixture `all_account_cooldown.jsonl` |
| 2 | true | 429 | Shape1 single-account | SINGLE_ACCOUNT_LIMIT | `None` | fixture `single_account_429.jsonl` |
| 3 | true | 429 | Shape1 api_retry_maxed (single) | SINGLE_ACCOUNT_LIMIT | `None` | fixture `api_retry_maxed.jsonl` |
| 4 | true | **absent** | **Shape2 all-account (no via provider)** | ALL_ACCOUNT_COOLDOWN | **`"gpt-5.5"`** | **NEW fixture `all_account_cooldown_apierror429.jsonl` (load-bearing)** |
| 5 | true | 429 | all-account **without** "via provider" | ALL_ACCOUNT_COOLDOWN | model X | synthetic inline (C8 ⟂ aes) |
| 6 | true | **absent** | Shape1 all-account **with** "via provider" | ALL_ACCOUNT_COOLDOWN | `"claude-opus-4-8"` | synthetic inline (C1 text gate) |
| 7 | true | absent | Shape2 single-account (`rate_limit_error` + "would exceed…") | SINGLE_ACCOUNT_LIMIT | `None` | NEW fixture `single_account_apierror429_SYNTHESIZED.jsonl` (OQ2) |
| 8 | true | absent | `rate_limit_error` present, neither all/single body | SINGLE_ACCOUNT_LIMIT | `None` | inline default (`monitor.py:332-333`); INV-001 residual |
| 9 | **false** | null/absent | "429"/"rate limit" incidental prose | **NONE** | `None` | NEW fixture `provider_429_incidental_ratelimit_text.jsonl` |
| 10 | true | null | `"API Error: The operation timed out."` | OPERATION_TIMEOUT | `None` | fixture `operation_timeout.jsonl` |
| 11 | true | absent | `error_during_execution` "pytest exited 1" (no `rate_limit_error`) | NONE | `None` | fixture `task_failure_real.jsonl` |
| 12 | false | null | "Task complete." | NONE | `None` | fixture `clean_pass.jsonl` |

**Rows 5 & 6 are the cross-product proof rows** for the two new independent gates: row 5 = 429-present but no "via provider" (proves R2 regex loosening is independent of api_error_status); row 6 = api_error_status-absent but "via provider" present (proves R1 text disjunct opens the gate without the structured field). Row 8 encodes the accepted INV-001 residual (neither-body default). No matrix cell is currently expected to be `xfail` after the fix lands — but the builder should mark any genuinely impossible cross-product cell (e.g. a prefix/body combination that can't co-occur) with `pytest.mark.xfail(reason="...")` per the "never silent omission" rule.

**Parametrize shape (match test_recovery_policy's style, §6 below):**
```python
@pytest.mark.unit
@pytest.mark.parametrize(
    ("source", "expected_kind", "expected_model"),
    [
        # fixture-backed rows use a filename; inline rows use a literal transcript str
        ...
    ],
)
def test_detection_contract_table(source, expected_kind, expected_model, tmp_path):
    sig = detect_provider_failure(<path>)          # is-identity on kind
    assert sig.kind is expected_kind
    assert sig.resolved_model == expected_model    # == incl. None
```
The builder must decide a uniform `source` encoding — simplest is: fixture rows pass a filename → `_FIXTURES / name`; inline rows write to `tmp_path` first. Two parametrize lists (one fixture-driven, one inline) is also acceptable and keeps each call form clean, matching the existing split between fixture tests and inline `tmp_path` tests in `TestDetectProviderFailure`.

---

## 6. Scope-boundary note — `test_recovery_policy.py` owns `decide()` (C3)

File: `/config/workspace/IronClaude/tests/sprint/test_recovery_policy.py` (27 lines, complete). It is the sole owner of the `SessionResetPolicy.decide` truth table:
```python
from superclaude.cli.sprint.monitor import ProviderFailure
from superclaude.cli.sprint.recovery_policy import Action, SessionResetPolicy

@pytest.mark.unit
@pytest.mark.parametrize(("signal", "attempt", "expected"), [
    (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 0, Action.HALT_MODEL_SWITCH),
    (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 5, Action.HALT_MODEL_SWITCH),
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 0, Action.RETRY_NEW_SESSION),
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 7, Action.RETRY_NEW_SESSION),
    (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 8, Action.HALT_MODEL_SWITCH),
    (ProviderFailure.OPERATION_TIMEOUT, 0, Action.CONTINUE),
    (ProviderFailure.NONE, 0, Action.CONTINUE),
])
def test_session_reset_policy_decide_truth_table(signal, attempt, expected):
    policy = SessionResetPolicy(max_session_resets=8)
    assert policy.decide(signal, attempt) is expected
```
**C3 constraint (spec §6.4 + R5):** the new detector contract-table test must NOT duplicate this policy truth table. The detector suite maps `transcript → (kind, resolved_model)`; the policy suite maps `(kind, attempt) → Action`. They compose but must stay separate files/tests. The detector tests never call `SessionResetPolicy.decide` or assert `Action.*` values. This is a clean seam: the 7-row policy table is byte-unchanged by this work (R3 — it only depends on the enum members, which don't change).

---

## 7. Verification commands (repo convention)

Per CLAUDE.md + spec §9 AC6. Run from repo root `/config/workspace/IronClaude` with UV (never bare `pytest`/`python`):

- **Scoped detector + parity + policy tests (fast inner loop):**
  ```
  uv run pytest tests/sprint/test_monitor.py tests/sprint/test_rerun_tasks.py tests/sprint/test_recovery_policy.py -v
  ```
- **Full sprint suite (regression, incl. R3 back-compat of all 6 fixtures):**
  ```
  uv run pytest tests/sprint/ -v
  ```
- **Single new contract-table test node (during authoring):**
  ```
  uv run pytest tests/sprint/test_monitor.py::TestDetectProviderFailure -v
  ```
- **Ruff format gate (CI runs this SEPARATELY from `make lint`; green make lint ≠ green CI — memory `reference_make_lint_vs_ci_ruff_format`):**
  ```
  uv run ruff format --check src/ tests/
  ```
  If it flags files, scope any actual formatting to changed files only (`uv run ruff format tests/sprint/test_monitor.py ...`) — a broad `ruff format src/ tests/` can reformat ~100 unrelated files if the worktree ruff ≠ CI ruff (memory `reference_ruff_version_mismatch_worktree`).
- **Lint:**
  ```
  make lint
  ```
- **Sync check (mandatory before commit per CLAUDE.md):**
  ```
  make verify-sync
  ```
  NOTE: this task touches only `src/superclaude/cli/sprint/monitor.py` + `tests/` + `tests/sprint/fixtures/` — none of which are sync-dev mirrored components (`skills/agents/commands`). `make verify-sync` should be a no-op pass here, but AC6 requires it be run clean. Do NOT stage anything under `.claude/`.

**RED→GREEN discipline:** author the 3 fixtures + contract table + parity asserts FIRST and confirm the Shape-2 rows (4, 6, 7) FAIL against the current unpatched `monitor.py` (proving they exercise the real gap), then apply researcher-01's two `monitor.py` hunks (predicate `:323`, regex `:41-43`) and confirm all rows GREEN + all 6 legacy fixtures still pass (R3).

---

## Summary

- `test_monitor.py` class `TestDetectProviderFailure` (`:243-344`) is the home for the contract-table test: every method is `@pytest.mark.unit`, calls `detect_provider_failure(_FIXTURES / "x.jsonl")`, asserts `sig.kind is ProviderFailure.X` (identity) and `sig.resolved_model == <str|None>` (equality). Synthetic rows use inline `tmp_path.write_text('{...}\n')`. The shared-inner parity template is at `:336-343`.
- All 6 existing fixtures confirmed Shape 1 (`api_error_status:429` present; all-account body has "via provider"); exact JSON reproduced above with each row's expected `(kind, model)`. Fixtures are single-line-result NDJSON with a trailing newline.
- The 3 new fixtures (`all_account_cooldown_apierror429.jsonl` load-bearing, `provider_429_incidental_ratelimit_text.jsonl` FP-`is_error:false`, `single_account_apierror429_SYNTHESIZED.jsonl` OQ2 breakpoint) — the byte-exact Shape-2 source is `research/shape2-verbatim-transcript.jsonl` (a real captured transcript in this task folder). The builder MUST copy its LAST `{"type":"result"}` line VERBATIM into `all_account_cooldown_apierror429.jsonl` (do NOT source from `.dev/troubleshoot/429-signature-ground-truth.md` — that file is Shape 1 only). See §3 (AUTHORITATIVE authoring instruction) and `research/04-gapfill-clarifications.md`.
- Offline parity target `_classify_transcript(text: str) -> TaskStatus` (`rerun_tasks.py:552`, delegates to shared inner `:592`); test seam is `test_rerun_tasks.py::TestClassifyTranscriptProviderExhaustion` (`:794-828`); assert `is TaskStatus.FAIL_PROVIDER_EXHAUSTED` on Shape-2, `is not` on the FP fixture, `PASS_RECOVERED` on prior-success+trailing-Shape-2.
- The ~12-row matrix is reproduced parametrize-ready with per-row source/kind/model; rows 5/6 prove the two gates are independent; empty cross-product cells → explicit `pytest.mark.xfail(reason=...)`, never silent omission.
- Scope boundary confirmed: `test_recovery_policy.py` (27 lines) solely owns the 7-row `decide()` truth table (kind×attempt→Action); the detector suite must NOT duplicate it (C3/R5).
- Verify with `uv run pytest tests/sprint/ -v` + `uv run ruff format --check src/ tests/` + `make lint` + `make verify-sync`; never bare pytest; never stage `.claude/`.
