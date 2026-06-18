# Research: File Inventory

**Topic type:** File Inventory
**Scope:** monitor.py, models.py, recovery_policy.py(new), aienv.py(new), scripts/ic
**Status:** Complete
**Date:** 2026-06-15

---

## FILE 1 — `src/superclaude/cli/sprint/monitor.py` (MODIFY, P1)

**Length:** 571 lines (verified via research-notes; structural reading confirms detector block ends at L250, `OutputMonitor` class at L253).

### Existing symbols the spec touches (verified, with exact line/signature)

| Symbol | Line | Signature / what's there now |
|---|---|---|
| `TASK_ID_PATTERN` | L24 | `re.compile(r"T\d{2}\.\d{2}")` — module-level regex constant (template for placing new `_RE_*` constants). |
| `ERROR_MAX_TURNS_PATTERN` | L33 | `re.compile(r'"subtype"\s*:\s*"error_max_turns"')` — budget-exhaustion pattern; **spec §5.8: detector must NOT collide with this** (429 ≠ max_turns). |
| `PROMPT_TOO_LONG_PATTERN` | L34 | `re.compile(r'"Prompt is too long"')` |
| `detect_error_max_turns(output_path: Path) -> bool` | L37–61 | **Sibling template.** `try: content = output_path.read_text(errors="replace") except (FileNotFoundError, OSError): return False`; empty→False; scans LAST non-empty line; returns `bool(PATTERN.search(line))`. New `detect_provider_failure` mirrors this read+tolerance shape. |
| `detect_prompt_too_long(output_path, *, error_path=None) -> bool` | L64–107 | Inner `_scan(path)`; scans **last-10** non-empty lines (pattern may not be in final line). Relevant because a 429 `result` event is the LAST line, so last-1 (like `detect_error_max_turns`) suffices — but a torn transcript may push it up; reading guidance below. |
| `_TURN_INDICATOR_PATTERN` | L112 | `re.compile(r'"type"\s*:\s*"assistant"')` |
| `_NONZERO_EXIT_CODE_RE` | L143–145 | exit-code regex (unrelated to 429, do not touch). |
| `count_turns_from_output(output_path: Path) -> int` | L223–250 | **NOTE: spec/research-notes call this `count_turns_from_stream_json` — the actual name is `count_turns_from_output`.** This is the stream-json line-iteration idiom to mirror: `content = output_path.read_text(errors="replace")` (OSError-tolerant), `for line in content.splitlines(): line=line.strip(); if line and PATTERN.search(line): ...`. It does NOT `json.loads` per line (it regex-scans). For `detect_provider_failure` the spec wants STRUCTURED-field parsing (`is_error`, `api_error_status`), so the new core must `json.loads` the LAST `{"type":"result"}` line (the `OutputMonitor._process_chunk` at L389 does `json.loads(line)` in try/except — that is the in-class JSON-parse idiom to mirror). |
| `OutputMonitor` class | L253 | First symbol after the free-function detector block — **upper bound of the insertion zone**. |

**`json.loads` per-line idiom** (to reuse in `_provider_failure_from_text`): `monitor.py:389` `event = json.loads(line)` inside `OutputMonitor._process_chunk` (L365–396), wrapped in try/except for `json.JSONDecodeError`.

### NEW symbols to add (P1) — exact insertion point + proposed signatures

**Insertion zone:** between L250 (end of `count_turns_from_output`) and L253 (start of `class OutputMonitor`). All new free functions/enums/regexes/dataclass live with the other module-level detectors here. New `_RE_*` constants go alongside `ERROR_MAX_TURNS_PATTERN`/`PROMPT_TOO_LONG_PATTERN` near L33–34 (or immediately above `detect_provider_failure` per detector-local convention).

Per-symbol checklist items (one Edit each):

1. **`ProviderFailure(Enum)`** — string-valued enum. Members per spec §4 L144–148:
   ```python
   class ProviderFailure(Enum):
       NONE = "none"
       SINGLE_ACCOUNT_LIMIT = "single_account_limit"
       ALL_ACCOUNT_COOLDOWN = "all_account_cooldown"
       OPERATION_TIMEOUT = "operation_timeout"
   ```
   Requires `from enum import Enum` import — **verify monitor.py import block (L8–19 currently has NO `enum` import).** One item: add `from enum import Enum`.
2. **`ProviderFailureSignal`** — return type carrying `(kind, resolved_model|None)`. Spec names it but does not define; propose a `@dataclass(frozen=True)`:
   ```python
   @dataclass(frozen=True)
   class ProviderFailureSignal:
       kind: ProviderFailure
       resolved_model: str | None = None
   ```
   Requires `from dataclasses import dataclass` import — currently NOT imported in monitor.py (import block L8–19). One item: add `dataclass` import.
3. **`_RE_ALL_ACCOUNT`** = `re.compile(r"All credentials for model (?P<model>.+?) are cooling down via provider")` (spec §4 L150). Named group `model` captures the RESOLVED model for the suggester.
4. **`_RE_SINGLE_ACCOUNT`** = `re.compile(r"would exceed your account's rate limit")` (spec §4 L151).
5. **`_provider_failure_from_text(text: str) -> ProviderFailureSignal`** — TEXT-accepting core (so `rerun_tasks._classify_transcript` can call it on its existing in-memory `text`, per spec §4 L168–177). Logic:
   - `json.loads` each `{`-prefixed line in try/except; capture the LAST `{"type":"result"}` event's `is_error`, `api_error_status`, `result` (string).
   - `is_error==True && api_error_status==429`: `_RE_ALL_ACCOUNT` match → `ALL_ACCOUNT_COOLDOWN` (+resolved model from group); `_RE_SINGLE_ACCOUNT` match → `SINGLE_ACCOUNT_LIMIT`; neither → `SINGLE_ACCOUNT_LIMIT` (conservative default for 429).
   - `api_error_status==null && result=="API Error: The operation timed out."` → `OPERATION_TIMEOUT`.
   - else → `NONE`. **Do NOT key on `subtype`** (it is `"success"` even when `is_error` is true — spec §2 L70, §5.10).
6. **`detect_provider_failure(output_path: Path) -> ProviderFailureSignal`** — PATH wrapper. `try: text = output_path.read_text(errors="replace") except (FileNotFoundError, OSError): return ProviderFailureSignal(ProviderFailure.NONE)`; empty→NONE; else `return _provider_failure_from_text(text)`. Mirrors `detect_error_max_turns` read/tolerance.

> **Detail for builder:** items 1–6 are six distinct Edit/insert operations, plus two import-add items (`Enum`, `dataclass`). The path wrapper reads stdout only (stderr is 0 bytes for 429s — spec §2 L59). Torn/partial transcript → NONE (spec §5.5).

---

## FILE 2 — `src/superclaude/cli/sprint/models.py` (MODIFY, P2 + P5)

**Length:** 1121 lines (verified). Import block (L8–16) **already imports** `dataclass, field` (L12) and `Enum` (L14) — **no new imports needed** for P2/P5.

### Existing symbols the spec touches (verified)

| Symbol | Line | What's there now |
|---|---|---|
| `TaskStatus(Enum)` | L46–66 | Members L49–54: `PASS="pass"`, `PASS_RECOVERED="pass_recovered"`, `FAIL_TERMINAL="fail"`, `FAIL_RECOVERABLE="fail_recoverable"`, `INCOMPLETE="incomplete"`, `SKIPPED="skipped"`. `is_success` property L56–58 = `(PASS, PASS_RECOVERED)`. `is_failure` property L60–66 = `(FAIL_TERMINAL, FAIL_RECOVERABLE, INCOMPLETE)`. |
| `TaskResult` dataclass | L171–240 | Fields L179–188: `task`, `status=TaskStatus.SKIPPED`, `turns_consumed=0`, `exit_code=0`, `started_at`, `finished_at`, `output_bytes=0`, `gate_outcome=GateOutcome.PENDING`, `reimbursement_amount=0`, `output_path=""`. |
| `TaskResult.to_dict` | L190–216 | Flat dict; returns keys: `task` (nested dict), `status`(`.value`), `turns_consumed`, `exit_code`, `started_at`(isoformat), `finished_at`(isoformat), `output_bytes`, `gate_outcome`(`.value`), `reimbursement_amount`, `output_path`(str). |
| `TaskResult.from_dict` | L218–240 | **HARD-KEYED for result-level fields** (VERIFIED): `data["status"]` L231, `data["turns_consumed"]` L232, `data["exit_code"]` L233, `data["started_at"]` L234, `data["finished_at"]` L235, `data["output_bytes"]` L236, `data["gate_outcome"]` L237, `data["reimbursement_amount"]` L238, `data["output_path"]` L239. (Nested `task` fields use `.get()` with defaults L226–229 — but the result-level fields do NOT — so new fields MUST use `.get(default)` to keep old `phase-N-result.json` readable.) |
| `PhaseStatus(Enum)` | L385–443 | Members L388–407 (incl. `HALT="halt"` L404, `TIMEOUT="timeout"` L405, `ERROR="error"` L406, `SKIPPED="skipped"` L407). **THREE** properties: `is_terminal` L409–423, `is_success` L425–434, `is_failure` L436–443 (`= (INCOMPLETE, HALT, TIMEOUT, ERROR)`). |
| `SprintOutcome(Enum)` | L446–452 | `SUCCESS`, `HALTED`, `INTERRUPTED`, `ERROR`. (`HALTED` is the outcome `executor.py:2103` halt path produces.) |
| `SprintConfig.index_path` | L531 | `Path = field(default_factory=lambda: Path("."))` — first arg of the resume command. |
| `SprintConfig.model` | L537 | `model: str = ""  # empty = claude default` — the model the halt builder names as exhausted + feeds the alias suggester. |
| `SprintRun.resume_command()` | L821–828 | Emits `superclaude sprint run {index} --start {halt_phase} --end {end}` — **no `--model`** (spec §0/§3.6). |
| `build_resume_output(config, halt_task_id, remaining_tasks, diagnostic_path=None, ledger=None) -> str` | L1017–1071 | Fall-through halt UX. Resume command line L1050: `superclaude sprint run {config.index_path} --resume {halt_task_id} --max-turns {budget_suggestion}` — **carries `--max-turns`, NOT `--model`** (confirms the new builder must add `--model`). |

### NEW / MODIFIED symbols (per-item checklist)

**P2 — TaskStatus:**
1. Add member `FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"` to `TaskStatus` (insert after L54 `SKIPPED` line — or grouped with the FAIL_* members after L53; keep enum-value lowercase string).
2. Add `TaskStatus.FAIL_PROVIDER_EXHAUSTED` to the `is_failure` tuple at **L62–66** (one item: extend the tuple). It is a *failure* (so `planner.py:160-164` resume re-runs it) but flagged infra (skips remediation). Do NOT add to `is_success`.

**P2 — TaskResult fields (3 new):**
3. Add field `failure_class: str = ""` to dataclass body (after L188 `output_path: str = ""`).
4. Add field `session_resets: int = 0` (same block).
5. Add field `exhausted_model: str = ""` (same block).
6. Add the 3 fields to `to_dict` return (after L215 `"output_path"` entry): `"failure_class": self.failure_class, "session_resets": self.session_resets, "exhausted_model": self.exhausted_model`.
7. Add the 3 fields to `from_dict` constructor (after L239 `output_path=...`) using **`.get()` defaults** for back-compat: `failure_class=data.get("failure_class", "")`, `session_resets=data.get("session_resets", 0)`, `exhausted_model=data.get("exhausted_model", "")`. (Items 6+7 may be one Edit each, or split per field for finest granularity.)

**P4 — PhaseStatus:**
8. Add member `PROVIDER_EXHAUSTED = "provider_exhausted"` to `PhaseStatus` (insert near L404 `HALT`).
9. Add `PhaseStatus.PROVIDER_EXHAUSTED` to `is_terminal` tuple (L411–423).
10. Add `PhaseStatus.PROVIDER_EXHAUSTED` to `is_failure` tuple (L438–443). **Do NOT add to `is_success`.** (Spec §4 Layer 2 says "routes to halt" — treat as terminal failure so the sprint halts cleanly.)

> **3-property caveat (not in research-notes):** PhaseStatus has THREE membership properties (`is_terminal` L409, `is_success` L425, `is_failure` L436). Builder must touch `is_terminal` + `is_failure` (2 items) — research-notes only flagged the member add.

**P5 — new halt-UX builder:**
11. **`build_account_exhaustion_halt(config: SprintConfig, halt_task_id: str, exhausted_model: str, suggested_model: str, remaining_tasks: list[TaskEntry], ledger: TurnLedger | None = None) -> str`** (signature per spec §4 Layer 5 L270–272). Insert as a free function **immediately after `build_resume_output` (after L1071), before the `ShadowGateMetrics` dataclass at L1074.** Must produce a **single-line** resume command `superclaude sprint run {config.index_path} --resume {halt_task_id} --model {suggested_model}` (spec §3.6, terminal-cannot-paste-multiline), name the exhausted model, and embed a one-line CLIProxyAPI re-route rationale. Mirror `build_resume_output`'s `lines = [...]; return "\n".join(lines)` shape but keep the resume command itself on ONE line. Wired into halt output when `halt_reason == provider_exhaustion`, else fall through to `build_resume_output` (wiring lives in executor.py — R3 scope).

> **`TurnLedger` reference:** `build_resume_output` already takes `ledger: TurnLedger | None`, so the type is already importable/usable in models.py scope (used at L1064–1069). New builder reuses it the same way.

---

## FILE 3 — `src/superclaude/cli/sprint/recovery_policy.py` (CREATE, P3)

**Status:** Does NOT exist (verified — only `recovery.py` exists in the sprint dir). New module, lives at `src/superclaude/cli/sprint/recovery_policy.py`.

**Imports it will need:** `from enum import Enum`, `from dataclasses import dataclass, field`, `import threading` (if the latch carries its own lock; but spec §4 Layer 3 says the latch is guarded by the **existing `lock` param** threaded through `_run_one_task`, so the policy object itself may not own a lock — see R3 for the threading contract). `from .monitor import ProviderFailure` (consumes the P1 enum).

### Symbols to create (per spec §4 Layer 3 L205–232)

1. **`Action(Enum)`** — string-valued enum, members:
   ```python
   class Action(Enum):
       RETRY_NEW_SESSION = "retry_new_session"
       HALT_MODEL_SWITCH = "halt_model_switch"
       FAIL_TASK = "fail_task"
       CONTINUE = "continue"
   ```
   (Spec lists them bare: `RETRY_NEW_SESSION; HALT_MODEL_SWITCH; FAIL_TASK; CONTINUE`. Propose lowercase string values per the project enum convention — see patterns research R2.)
2. **`SessionResetPolicy`** `@dataclass`:
   ```python
   @dataclass
   class SessionResetPolicy:
       max_session_resets: int = 8          # Q5: ≈ pool size (~8 accounts)
       _exhaustion_attempts: int = 0
       _latch_tripped: bool = False         # sprint-wide halt latch, lock-guarded by caller
   ```
3. **`SessionResetPolicy.decide(self, signal: ProviderFailure, attempt: int) -> Action`** — pure decision (spec §4 L214–218):
   - `signal is ProviderFailure.ALL_ACCOUNT_COOLDOWN` → `Action.HALT_MODEL_SWITCH` (fast path, any attempt).
   - `signal is ProviderFailure.SINGLE_ACCOUNT_LIMIT` → `RETRY_NEW_SESSION if attempt < self.max_session_resets else HALT_MODEL_SWITCH`.
   - else (`NONE` / `OPERATION_TIMEOUT`) → `Action.CONTINUE` (existing paths).
   - `FAIL_TASK` is in the enum but `decide` as specified never returns it directly — reserved for the shifting-failure edge (spec §5.2: a single-429 attempt that becomes a real bug is classified by the *last* attempt via the normal ladder, not by `decide`). Builder note: keep `FAIL_TASK` member; do not wire a `decide` branch unless a later phase needs it.

> **Note on the latch:** `_latch_tripped` is a field on the policy instance shared across K>1 workers; it is **checked/tripped under the executor's `lock`** (spec §4 L221–232), NOT inside `decide`. `decide` stays pure (testable via the §6 truth table). The latch read/write helpers (if any) belong with the executor wiring (R3), or as thin lock-free accessors here — design decision deferred to R3/builder. Storm bound: `≤ cap + (K−1)`, strictly `< K × cap` (spec §5.3).

### Unit-test surface (R5 scope, noted for completeness)
`decide` truth table over (signal × attempt) incl. cooldown-on-first-attempt → `HALT_MODEL_SWITCH` (spec §6 "Policy").

---

## FILE 4 — `src/superclaude/cli/sprint/aienv.py` (CREATE, P5)

**Status:** Does NOT exist (verified). New module at `src/superclaude/cli/sprint/aienv.py`.

### `~/.aienv` resolution convention (documented from `src/superclaude/scripts/ic` + `src/superclaude/cli/swarm/config.py`)

**`scripts/ic` (bash wrapper, the canonical alias convention) — VERIFIED:**
- `AIENV="${AIENV:-$HOME/.aienv}"`, `source`d into the shell (ic:25–31).
- **Three model SLOTS:** `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` (ic:61–63, 75–77, exported at ic:98).
- **Alias resolution = bash indirect expansion** (ic:37–46): a token `key` resolves to `$key` (the env var of that name) **only if** `key` matches `^[a-zA-Z_][a-zA-Z0-9_]*$` AND that var is set; otherwise the literal value passes through. Literal model IDs (`qwen3.6-plus`, `claude-opus-4-8`) contain `.`/`-` so they fall through unchanged.
- **Presets:** `IC_PRESET_<name>` = space-separated `slot=value` pairs (ic:48–67) — `opus=`/`sonnet=`/`haiku=` only.
- **`IC_ALIASES`** is mentioned in the spec/research-notes but **does NOT appear in `scripts/ic`** — `ic`'s comment block (ic:13) refers to "`$IC_ALIASES`" loosely but the actual mechanism is per-token `export kimi=...` indirect expansion, NOT a single `IC_ALIASES` map. **Mark spec's `IC_ALIASES` token as Unverified / likely a loose alias for "the set of `export <name>=<model>` lines in ~/.aienv".**

**`swarm/config.py` (the canonical Python convention) — VERIFIED:**
- `T2_MODEL_ENV_PREFIX = "T2Model0"` (config.py:57); `T2_MODEL_MAX_SLOTS = 9` (config.py:63).
- Numbered slots `T2Model01`..`T2Model09` (config.py:54–55, 82).
- `_collect_t2_models(env_map)` (config.py:178–185): `for index in range(1, T2_MODEL_MAX_SLOTS+1): value = env_map.get(f"{T2_MODEL_ENV_PREFIX}{index}"); if value: models.append(value)` → returns ordered tuple.
- **KEY: Python reads from `os.environ` (`env_map`), NOT by parsing the `~/.aienv` FILE** (config.py:125 `env_map = env if env is not None else os.environ`). No Python in the repo opens/parses `~/.aienv` as text (verified: 0 hits for file-open of `.aienv`).

> **Design decision for `aienv.py` (surface to builder, do not silently pick):** the spec §4 Layer 5 says "parse `~/.aienv`", but the existing Python convention (`swarm/config.py`) reads **already-exported `os.environ`**, because `~/.aienv` is a bash file `source`d only by the `ic` wrapper. Two viable designs:
> - **(A) os.environ reader** (matches `swarm/config.py`): read `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` + `T2Model01..09` from `os.environ`. Simpler, convention-consistent, but only works if the sprint process inherited the exports (it does — `process.py` `env_vars` merges into `os.environ.copy()`, spec §0).
> - **(B) file parser**: open `~/.aienv` and regex `export NAME=value` lines. Matches the spec's literal "parse" wording and works even when vars aren't exported into the current process, but is new machinery with no prior art in the repo.
> Recommend **(A)** for convention-consistency with a fallback note; the builder should encode (A) and document (B) as the fallback, per `feedback_human_decision_items_must_halt`. R5/test plan authors a fixture `~/.aienv` (spec §6 "aienv.py"), which leans toward (B) being testable — reconcile in the test item.

### Symbols to create (per spec §4 Layer 5 L261–268)

1. **Module constants** mirroring `swarm/config.py`: e.g. `_ANTHROPIC_SLOTS = ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL")`; reuse `T2Model0`/`9` (import from `swarm.config` or redeclare — prefer import to avoid drift: `from superclaude.cli.swarm.config import T2_MODEL_ENV_PREFIX, T2_MODEL_MAX_SLOTS`).
2. **A loader** — `_load_aliases(env=None) -> dict[str,str]` (or list) enumerating the three Anthropic slots + `T2Model01..NN` (design A) **or** `_parse_aienv(path=Path.home()/".aienv") -> dict` (design B).
3. **`suggest_alternate_model(failed_model_or_alias: str) -> str | None`** (spec §4 L263–264): returns the next DISTINCT alias/slot — `opus→sonnet`, `T0Model01→T0Model02` (note spec uses `T0Model0N` in §3.6 but swarm uses `T2Model0N`; the prefix is operator-config — the suggester should be prefix-agnostic / iterate the numbered slots it finds). Matches against the **resolved** model (the cooldown body embeds the resolved model, e.g. `claude-opus-4-8`), so the suggester must map resolved-model → slot → next slot. **None-safe** when no alternate exists (spec §5.7: message must NOT fabricate an alias).

> **Caveat to surface in the halt message (spec §4 L265–268, §5.7):** alias→account-pool mapping is operator knowledge; the suggester assumes "the next slot routes to a different pool." If no alternate alias is found, return None and let `build_account_exhaustion_halt` show the exhausted model + generic guidance (wait for window / add accounts / switch alias if available).

### Unit-test surface (R5 scope)
Parse a fixture `~/.aienv`; `suggest_alternate_model` returns next distinct alias for opus and for `T0Model01`; returns None-safe when no alt (spec §6 "aienv.py").

---

## FILE 5 — `src/superclaude/scripts/ic` (REFERENCE ONLY — not modified)

**Status:** Exists (4051 bytes, executable bash). **NOT a modify target** — read ONLY to extract the `~/.aienv` alias-resolution convention for `aienv.py` (documented in FILE 4 above). Companion `src/superclaude/cli/ic.py` also exists (separate Python CLI; not the alias resolver — out of scope here).

**Env-var names + resolution order (authoritative, from `ic` + `swarm/config.py`):**
1. `AIENV` env var → else `$HOME/.aienv` (file location).
2. Model slots: `ANTHROPIC_DEFAULT_OPUS_MODEL` / `ANTHROPIC_DEFAULT_SONNET_MODEL` / `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
3. Proxy worker slots: `T2Model01..T2Model09` (prefix `T2Model0`, max 9).
4. Alias resolution: indirect expansion of `$<token>` when token is a valid identifier and set; literal pass-through otherwise.
5. Presets: `IC_PRESET_<name>` = `slot=value ...` pairs (opus/sonnet/haiku slots only).
6. `IC_ALIASES` — Unverified as a literal var; treat as the loose set of `export <alias>=<model>` lines.

---

## SUMMARY

**Scope verified (5 files):** monitor.py (571L, MODIFY P1), models.py (1121L, MODIFY P2+P5), recovery_policy.py (CREATE P3), aienv.py (CREATE P5), scripts/ic (REFERENCE only).

**Per-symbol edit count for the builder (one checklist item each):**
- **monitor.py (P1):** 6 new symbols (`ProviderFailure` enum, `ProviderFailureSignal` dataclass, `_RE_ALL_ACCOUNT`, `_RE_SINGLE_ACCOUNT`, `_provider_failure_from_text` core, `detect_provider_failure` path wrapper) + **2 import-adds** (`from enum import Enum`, `from dataclasses import dataclass` — neither currently imported). Insertion zone: L250–L253 (between `count_turns_from_output` end and `OutputMonitor` class).
- **models.py (P2):** `FAIL_PROVIDER_EXHAUSTED` member (after L54) + add to `is_failure` tuple (L62–66); 3 TaskResult fields (`failure_class`/`session_resets`/`exhausted_model` after L188) + to_dict (after L215) + from_dict with `.get()` back-compat (after L239). **Imports already present.**
- **models.py (P4):** `PhaseStatus.PROVIDER_EXHAUSTED` member (near L404) + add to `is_terminal` (L411–423) AND `is_failure` (L438–443) — **2 properties, not 1** (research-notes under-counted).
- **models.py (P5):** `build_account_exhaustion_halt(...)` free function after L1071.
- **recovery_policy.py (P3):** `Action` enum (4 members), `SessionResetPolicy` dataclass (3 fields), `decide()` method. Imports `ProviderFailure` from monitor.
- **aienv.py (P5):** slot constants (reuse `T2_MODEL_ENV_PREFIX`/`T2_MODEL_MAX_SLOTS` from swarm.config), a loader, `suggest_alternate_model()`.

**Key findings / corrections to upstream notes:**
1. **Name correction:** spec/research-notes reference `count_turns_from_stream_json`; the actual monitor.py symbol is **`count_turns_from_output`** (L223). The closest LAST-result `json.loads` idiom to mirror is `OutputMonitor._process_chunk` (L389), not a turn-counter.
2. **monitor.py needs 2 new imports** (`Enum`, `dataclass`) — not flagged in research-notes. models.py needs none.
3. **PhaseStatus has THREE membership properties** (`is_terminal` L409, `is_success` L425, `is_failure` L436); research-notes only mentioned the member add. PROVIDER_EXHAUSTED must go in `is_terminal` + `is_failure`.
4. **No Python in the repo parses the `~/.aienv` FILE** — `swarm/config.py` reads exported `os.environ`. `aienv.py` faces a design choice (os.environ reader [convention-consistent] vs. file parser [matches spec's "parse" wording + testable fixture]). Flagged as `needs_human_decision`-adjacent; recommend os.environ reader (A) with file-parse fallback (B) documented.
5. **`IC_ALIASES` token is Unverified** — does not exist as a literal var in `scripts/ic`; the real mechanism is per-token `export <name>=<model>` indirect expansion + `IC_PRESET_<name>` presets.
6. **`build_resume_output` (L1050) carries `--max-turns` but no `--model`** and `resume_command()` (L821–828) carries `--start/--end` but no `--model` — confirms the new builder is the only path that emits `--model`.
7. `SprintConfig.model: str = ""` (L537) and `SprintConfig.index_path` (L531) are the fields the halt builder + suggester consume.
