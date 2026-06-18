# Research: Patterns & Conventions
**Status:** In Progress
**Date:** 2026-06-15

**Scope:** Reusable code idioms/conventions the implementation MUST mirror, each with a concrete `file:line` exemplar so build items can say "mirror X at file:line" rather than re-deriving. All paths under `src/superclaude/cli/sprint/` (source-of-truth; `.claude/` is sync-dev output). Verified against source 2026-06-15.

---

## Pattern A — Pure detector function (monitor.py)

**Canonical exemplar:** `detect_error_max_turns` at `monitor.py:37-61`. The new `detect_provider_failure` MUST mirror this shape exactly.

**Idiom (4 mandatory elements):**

1. **Module-level compiled regex constant** above the function. Exemplars: `ERROR_MAX_TURNS_PATTERN = re.compile(r'"subtype"\s*:\s*"error_max_turns"')` (`monitor.py:33`), `PROMPT_TOO_LONG_PATTERN` (`monitor.py:34`). New: `_RE_ALL_ACCOUNT` / `_RE_SINGLE_ACCOUNT` declared module-level (the spec's leading-underscore naming matches the file's private-constant convention, e.g. `_TURN_INDICATOR_PATTERN` at `:112`, `_NONZERO_EXIT_CODE_RE` at `:143`).
2. **Signature `(output_path: Path) -> bool|signal`** — pure, no side effects, no logging on the hot path. `detect_prompt_too_long` adds an optional keyword-only second path: `(output_path: Path, *, error_path: Path | None = None)` (`monitor.py:64-66`) — but the spec explicitly says stderr is 0 bytes for 429s, so `detect_provider_failure` takes only `output_path` (no `error_path`).
3. **OSError-tolerant read → neutral return:**
   ```python
   try:
       content = output_path.read_text(errors="replace")
   except (FileNotFoundError, OSError):
       return False        # neutral value; for the new detector → ProviderFailure.NONE
   if not content.strip():
       return False
   ```
   Exact pattern at `monitor.py:46-52`. **The neutral return for `detect_provider_failure` is `NONE`** (spec §4 Layer 1, edge case #5 "torn/partial transcript → degrades to NONE, no false re-spawn"). `read_text(errors="replace")` (not bytes) and the `(FileNotFoundError, OSError)` tuple are both load-bearing — `count_turns_from_output` uses the identical guard (`monitor.py:236-239`).
4. **Last-line / last-N-line reverse scan:** `detect_error_max_turns` scans only the LAST non-empty line:
   ```python
   lines = content.strip().splitlines()
   for line in reversed(lines):
       line = line.strip()
       if line:
           return bool(ERROR_MAX_TURNS_PATTERN.search(line))
   ```
   (`monitor.py:55-59`). `detect_prompt_too_long` scans the **last 10** non-empty lines with a counter break (`monitor.py:89-101`) for patterns "that may not be in the final line." **Caveat for `detect_provider_failure`:** the 429 signal is in the LAST `{"type":"result"}` event, but the all-account-cooldown fixture (T03.13) has num_turns=25 of prior real work, so the result event may not be the literal last *line*. The detector must parse the LAST *result event* (Pattern B), NOT just regex the last raw line — so it follows the stream-json-parse idiom (B), then regexes the `result` string field of that event. Pattern A governs the read/OSError/empty-guard wrapper; Pattern B governs the event location.

**Why a text-core split (spec §4 Layer 1 "Signature reconciliation"):** `detect_error_max_turns` reads a path; `_classify_transcript` (Pattern D consumer) already has `text: str` in memory. To avoid double-reading, the spec factors `_provider_failure_from_text(text) -> ProviderFailureSignal`; the path wrapper does the OSError-guarded `read_text` (Pattern A elements 2-3) then delegates to the text core. This split has **no existing exemplar in monitor.py** (all monitor detectors are path-only) but is forced by the `_classify_transcript(text: str)` signature at `rerun_tasks.py:547` — Unverified that any current monitor detector uses a text-core; this is a net-new factoring the builder introduces.

---

## Pattern B — Stream-json (NDJSON) line-iteration parse: last result event + token accumulation + subtype trap

**Two canonical exemplars (nearly identical), pick by what you need:**

1. **`count_turns_from_stream_json` at `process.py:32-76`** — the simplest last-result-event finder. This is the spec's named "LAST-result-event parse mirror." NOTE: it lives in **`process.py`, NOT `monitor.py`** (spec/research-notes say "mirror `count_turns_from_stream_json`" — the symbol is in process.py; `monitor.py` only has `count_turns_from_output` which counts `"type":"assistant"` lines, a *different* semantic — see the explicit "two distinct turn-count contracts" docstring at `process.py:42-50`). Do NOT confuse them.

2. **`_classify_transcript` at `rerun_tasks.py:547-593`** — the same parse PLUS output-token accumulation PLUS the subtype handling. This is the richer exemplar and the one `_provider_failure_from_text` should mirror (it shares the text-string input and produces a `TaskStatus`).

**The canonical loop (verbatim from `rerun_tasks.py:555-574`):**
```python
result_event: Optional[dict] = None
total_output_tokens = 0
for raw in text.splitlines():
    line = raw.strip()
    if not line.startswith("{"):          # skip non-JSON / human lines
        continue
    try:
        event = json.loads(line)
    except (json.JSONDecodeError, ValueError):   # tolerate partial/malformed lines
        continue
    if not isinstance(event, dict):
        continue
    message = event.get("message")
    usage = message.get("usage") if isinstance(message, dict) else None
    if usage is None:
        usage = event.get("usage")
    if isinstance(usage, dict) and isinstance(usage.get("output_tokens"), int):
        total_output_tokens += usage["output_tokens"]
    if event.get("type") == "result":
        result_event = event              # keep the LAST result event (overwrite, no break)
```

**Five load-bearing idioms in this loop:**
- **`if not line.startswith("{"): continue`** — cheap pre-filter before `json.loads` (`rerun_tasks.py:559`; `process.py:62`). The monitor's live parser uses the same `line.strip()` + skip-empty guard (`monitor.py:375-378`).
- **`json.loads` in `try/except (json.JSONDecodeError, ValueError)`** — never let a torn line raise (`rerun_tasks.py:561-564`; `process.py:64-67`; `monitor.py:388-394` uses the same except tuple). Mirrors Pattern A's OSError tolerance at the line granularity.
- **Keep the LAST result event by overwrite, no `break`** — `result_event = event` inside the loop, evaluated after the loop (`rerun_tasks.py:573-574`; `process.py:68-69`). This is why a trailing-429 after real work is found, and why num_turns=25 transcripts still resolve correctly.
- **output_tokens accumulation across turns** — `usage` may sit under `event["message"]["usage"]` (assistant events) OR `event["usage"]` (result events); the code probes message-first then top-level (`rerun_tasks.py:567-572`). The monitor live-parser accumulates the same field (`monitor.py:445-451`, summing `input_tokens`/`output_tokens` when `isinstance(..., int) and > 0`). `detect_provider_failure` does NOT need token sums (it keys on `is_error`+`api_error_status`), but `_classify_transcript`'s existing logic does, so the shared text-core must not disturb the surrounding token accounting.
- **The `subtype` trap — DO NOT key on `subtype` for 429 detection.** `_classify_transcript` currently does `is_error = bool(result_event.get("is_error")) or subtype.startswith("error")` (`rerun_tasks.py:579-580`). The spec (§2 event #3, edge case #10) pins that for a **429 the `subtype` is `"success"` even though `is_error` is true**. So the 429 branch must read `is_error` + `api_error_status` (structured fields), NEVER `subtype`. The new `FAIL_PROVIDER_EXHAUSTED` branch goes **above** the `:582` `is_error` branching so it intercepts the 429 before the legacy `subtype.startswith("error")` logic can mis-route it.

**Result-field extraction for the new detector:** after the loop, read `result_event.get("is_error")`, `result_event.get("api_error_status")`, and the `result_event.get("result")` string, then apply `_RE_ALL_ACCOUNT` / `_RE_SINGLE_ACCOUNT` to the result string (spec §2 pinned predicates). `api_error_status` is the field name for the load-bearing line (NOT `error_status`, which is the `api_retry` event's field — spec §2 event #1 vs #3). Unverified against a live transcript field-by-field (fixtures not reachable from this worktree per spec §2), but the field names are pinned in the reflect-validated spec.

---

## Pattern C — String-valued Enum + `is_success`/`is_failure`/`is_terminal` @property tuples (models.py)

**Canonical exemplar:** `TaskStatus` at `models.py:46-66`; `PhaseStatus` at `models.py:385-423`.

**Idiom (3 mandatory elements):**

1. **String-valued members** — every member is `NAME = "snake_case_string"`. `TaskStatus.FAIL_TERMINAL = "fail"` (note value ≠ name here — historical), `PASS_RECOVERED = "pass_recovered"` (`models.py:49-54`). New member: `FAIL_PROVIDER_EXHAUSTED = "fail_provider_exhausted"` (spec §4 Layer 2; matches the snake_case value convention). `PhaseStatus.PROVIDER_EXHAUSTED = "provider_exhausted"` (new, `models.py:385-407` block).
2. **Classification via `@property` returning `self in (…)` membership tuple** — NOT a stored field, NOT an if-ladder:
   ```python
   @property
   def is_failure(self) -> bool:
       return self in (
           TaskStatus.FAIL_TERMINAL,
           TaskStatus.FAIL_RECOVERABLE,
           TaskStatus.INCOMPLETE,
       )
   ```
   (`models.py:60-66`). `is_success` is the sibling at `:56-58` returning `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)`. **The new-member edit is purely additive to the relevant tuple** — add `TaskStatus.FAIL_PROVIDER_EXHAUSTED` to the `is_failure` tuple (`models.py:62-66`) and do NOT add it to `is_success`. Spec §4 Layer 2 rationale: it's a *failure* so `planner.py:160-164` re-runs it on resume, but flagged-infra so it skips remediation.
3. **`PhaseStatus.is_terminal` is a separate, larger membership tuple** (`models.py:410-423`) listing ALL terminal states (every PASS_* + HALT/TIMEOUT/ERROR/SKIPPED/INCOMPLETE). New `PhaseStatus.PROVIDER_EXHAUSTED` MUST be added to the `is_terminal` tuple (`models.py:411-423`) — it routes to halt, so it is terminal — and MUST NOT be added to `is_success` (`models.py:426+`). Forgetting the `is_terminal` add would make a `PROVIDER_EXHAUSTED` phase non-terminal → the phase loop wouldn't stop. This is the single most error-prone enum edit (a membership-tuple omission is silent).

**Adjacent enums following the same idiom (for reference, not edited):** `GateOutcome` (`models.py:69-79`, `is_success` property), `GateDisplayState` (`models.py:82-115`, but uses dict-lookup `@property` for color/icon/label rather than membership — a different sub-idiom).

---

## Pattern D — Serialization: `to_dict` flat + `from_dict` back-compat (hard-key vs `.get()`) — THE compare the spec calls out

**Two divergent `from_dict` styles coexist in `models.py`. The spec's P2 instruction hinges on knowing which one `TaskResult` uses.**

**`TaskResult` — HARD-KEYED `from_dict` (the back-compat hazard):**
- `to_dict` at `models.py:190-216` emits a **flat dict** (nested `task` is inlined as a dict literal; enums via `.value`; datetimes via `.isoformat()`).
- `from_dict` at `models.py:218-240` reads **result-level fields by HARD subscript**: `data["status"]`, `data["turns_consumed"]`, `data["exit_code"]`, `data["started_at"]`, `data["finished_at"]`, `data["output_bytes"]`, `data["gate_outcome"]`, `data["reimbursement_amount"]`, `data["output_path"]` (`models.py:231-239`). Verified: these are bare `data[...]` subscripts, so a missing key raises `KeyError`.
- **Inconsistency to note:** the NESTED `task` sub-dict already uses `.get()` defaults — `task_data.get("description", "")`, `.get("dependencies", [])`, `.get("command", "")`, `.get("classifier", "")` (`models.py:226-229`) — while `task_id`/`title` are hard-keyed (`:224-225`). So the file already MIXES styles within one method.
- **P2 requirement:** the THREE new fields (`failure_class: str = ""`, `session_resets: int = 0`, `exhausted_model: str = ""`) MUST be:
  - added as dataclass fields with defaults after `output_path` (`models.py:188` is the last current field),
  - serialized in `to_dict` (`models.py:198-216` return dict),
  - read with **`.get(default)`** in `from_dict` — e.g. `failure_class=data.get("failure_class", "")`, `session_resets=data.get("session_resets", 0)`, `exhausted_model=data.get("exhausted_model", "")`. This is the ONLY way an old `phase-N-result.json` (written before these fields existed) round-trips through `from_dict` without `KeyError`. The spec's back-compat test (§6) exercises exactly this.

**`HandoffRecord` — the FORWARD-COMPAT contrast (the pattern to copy for new fields):**
- `from_dict` at `models.py:328-350` uses `data.get(key, default)` for **EVERY** field (`models.py:337-349`). Docstring (`models.py:330-336`) states the intent verbatim: "Uses `data.get(key, default)` for every field so a dict carrying an UNKNOWN extra key round-trips without raising … This lets an old reader consume a record written by a newer `schema_version`."
- **This is the reference pattern** the new `TaskResult` fields must imitate. The builder item can cite "use `.get()` defaults exactly as `HandoffRecord.from_dict` does at `models.py:337-349`, NOT the hard-key style of the surrounding `TaskResult.from_dict`."
- HandoffRecord also carries a `schema_version: int = 1` field (`models.py:294`) — the new TaskResult fields do NOT introduce a version bump (the `.get()` default IS the versioning mechanism here, consistent with how TaskResult has never had a schema_version).

**`build_*` output-builder convention (for P5's `build_account_exhaustion_halt`):** the existing halt/resume UX builder is `build_resume_output` (research-notes cites `models.py:1017-1071`; `models.py:821-828` is the fall-through). New `build_account_exhaustion_halt(config, halt_task_id, exhausted_model, suggested_model, remaining_tasks, ledger)` should mirror its signature shape and single-string return. NOTE: I verified `from_dict`/`to_dict`/enum sections directly; the `build_resume_output` line range is from research-notes/spec and NOT re-Read in this pass — **Unverified line numbers for `build_resume_output`** (R1/R3 own that surface).

---

## Pattern E — Concurrency: spawn UNLOCKED, reconcile LOCKED, shared state threaded as params

**Canonical exemplar:** `_run_one_task` at `executor.py:963-1045`, called from TWO sites.

**The lock contract (docstring at `executor.py:976-985`, verified verbatim):** "The SPAWN runs UNLOCKED (the slow part — concurrency here is the source of the wall-clock win). The budget reconcile and the post-task hooks run under `lock` when provided (K>1) … With `lock=None` (K=1) there is no locking and behavior is identical."

**Three structural elements:**

1. **Shared mutable state is threaded as keyword-only params, NOT module globals.** Signature (`executor.py:963-975`):
   ```python
   def _run_one_task(task, config, phase, *, started_at, prior_context="",
                     ledger: TurnLedger | None = None, subprocess_factory=None,
                     shadow_metrics: ShadowGateMetrics | None = None,
                     remediation_log: DeferredRemediationLog | None = None,
                     lock=None) -> tuple[TaskResult, TrailingGateResult | None]:
   ```
   `ledger`, `shadow_metrics`, `remediation_log` are the shared objects; `lock` is the guard. **The new `SessionResetPolicy`/latch is added as a new keyword-only param here** (spec §4 Layer 3 "passed into `_run_one_task` as a new shared param alongside `ledger`/`shadow_metrics`"), e.g. `reset_policy: SessionResetPolicy | None = None`.

2. **Spawn unlocked, then a single `with guard:` block for ALL shared mutation.** The spawn (`executor.py:986-993`, via `subprocess_factory` seam or `_run_task_subprocess`) and the status classification (`executor.py:999-1015`) run with NO lock held. Then:
   ```python
   guard = lock if lock is not None else contextlib.nullcontext()
   with guard:
       if ledger is not None: ...   # debit/credit reconcile
       result = TaskResult(...)
       result = run_post_task_wiring_hook(...)
       result, gate_result = run_post_task_anti_instinct_hook(...)
   ```
   (`executor.py:1017-1044`). **The `lock if lock is not None else contextlib.nullcontext()` idiom is the load-bearing trick** — one code path serves both K=1 (nullcontext, zero overhead) and K>1 (real lock). The new latch follows this: check the latch under `guard`, trip it under `guard`, but keep the spawn itself outside the `with`.
   - **Spec §4 Layer 3 / edge case #3 nuance:** because the spawn is OUTSIDE the lock, the latch is "checked under lock immediately before each spawn and tripped under lock after a worker classifies HALT_MODEL_SWITCH"; up to `K−1` workers may be mid-spawn when it trips → storm bound is `≤ cap + (K−1)`, strictly `< K × cap`, **NOT** strictly `≤ cap`. The builder must NOT assert `≤ cap` under K>1 (the test asserts `< K × cap AND ≤ cap + (K−1)`).

3. **Both call sites pass the SAME params; only `lock=` differs.** This is the proof that the new param must be threaded at BOTH sites:
   - **K>1 parallel** (`executor.py:1134-1145`): passes `lock=lock` (a real lock). Preceded by the atomic budget gate `ledger.try_launch()` (`executor.py:1120`) and the env-capture under `with lock:` (`executor.py:1131-1133`).
   - **K=1 sequential** (`executor.py:1337-1348`): passes `lock=None`. Inline comment (`executor.py:1335-1336`): "Shared with the K>1 parallel path via _run_one_task; lock=None here (sequential, no race)."
   - **Builder consequence:** adding `reset_policy=` to `_run_one_task` requires editing BOTH `executor.py:1134-1145` AND `executor.py:1337-1348` to pass it (the same `SessionResetPolicy` instance constructed once per sprint, shared across all workers — that's how the latch is sprint-wide). Missing either site = the policy is `None` on that path = no recovery on that K mode. This is a per-call-site item in the tasklist, not one batch edit.

**Single-session phase path is a DIFFERENT spawn (separate wrap point):** `ClaudeProcess(config, phase, env_vars=…)` at `executor.py:1815` (per research-notes; NOT re-Read in this pass — **Unverified line**), classified by `_determine_phase_status` at `~:1993`. This path does NOT go through `_run_one_task`, so P4's re-spawn loop is a separate mirror of the same policy/detector usage, not a reuse of the per-task loop. R3 owns the exact wiring.

---

## Pattern F — Source-of-Truth (SoT) discipline + toolchain conventions

**Authority:** CLAUDE.md (project + global) + spec §7. These are HARD gates the implementation MUST satisfy; encode them as VALIDATION items in the tasklist.

1. **Edit `src/superclaude/` ONLY, then sync:** all detection/taxonomy/policy/executor edits land in `src/superclaude/cli/sprint/` (and new files `recovery_policy.py`, `aienv.py` there). Then `make sync-dev` (copies `src/superclaude/{skills,agents,commands}` → `.claude/`) then `make verify-sync` (CI-friendly drift check). NEVER edit `.claude/` directly; NEVER stage `.claude/skills,commands,agents,hooks,templates` (only `.claude/settings.json` is tracked). Note: the sprint *code* lives under `src/superclaude/cli/`, which is normal Python packaging (not subject to the `.claude/` mirror rule) — the SoT mirror rule bites only if the task also touches skills/agents/commands. **Templates live at `src/superclaude/templates/workflow/`, NOT `.claude/templates/`** (research-notes line 15).
2. **UV-only Python:** every test/run uses `uv run pytest` (and `uv run pytest tests/<path> -v` for targeted). NEVER `python -m pytest`, bare `pip`, or `python script.py` (CLAUDE.md "Python Environment Rules", global rule 1).
3. **ruff format check before push (the CI gap):** `make lint` runs only `ruff check`; CI SEPARATELY runs `ruff format --check src/ tests/`. Run **`uv run ruff format --check src/ tests/`** before pushing or a green `make lint` will still fail CI (memory `reference_make_lint_vs_ci_ruff_format.md`; spec §7). Both `make lint` AND the format check are mandatory VALIDATION items.
4. **Feature branch only:** never commit to `master`/`main`; branch off `master` (global rule 4; current branch `SprintRun429` is already a feature branch).
5. **PR to the FORK with explicit `--repo`:** `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> …`. NEVER bare `gh pr create` (defaults to upstream `SuperClaude-Org`). Pre-PR: `git remote -v` confirms `origin = IronbellyOrg/IronClaude`; rebase onto `origin/master` if the fork is ahead; verify the returned URL is `github.com/IronbellyOrg/IronClaude/pull/N` (CLAUDE.md "PR Target = Fork"; memory `feedback_pr_target_fork_only.md`).
6. **Finish-what-you-start + scope discipline:** no TODO stubs for core logic (global rule 7); build exactly the spec'd P1–P6 surface, no speculative additions (global rule 8). The (G) recovery.py nominator-exclusion is a `needs_human_decision`-adjacent item — encode the documented default + HALT-on-nontrivial, do NOT silently auto-resolve (research-notes AMBIGUITIES; memory `feedback_human_decision_items_must_halt`).

---

## Quick-reference: "mirror X at file:line" table (for builder item Context fields)

| New code | Mirror this exemplar | At | Phase |
|---|---|---|---|
| `detect_provider_failure` wrapper (read/OSError/empty-guard) | `detect_error_max_turns` | `monitor.py:37-61` | P1 |
| `_RE_ALL_ACCOUNT`/`_RE_SINGLE_ACCOUNT` module-level regex | `ERROR_MAX_TURNS_PATTERN` | `monitor.py:33` | P1 |
| Last-result-event parse + token accum + `try/except json` | `_classify_transcript` loop | `rerun_tasks.py:555-574` | P1 |
| Simplest last-result-event finder | `count_turns_from_stream_json` | `process.py:32-76` (in process.py, NOT monitor) | P1 |
| Subtype-trap avoidance (key on `is_error`+`api_error_status`) | the `subtype.startswith("error")` line to insert ABOVE | `rerun_tasks.py:579-580` | P1/P2 |
| `FAIL_PROVIDER_EXHAUSTED` member + add to `is_failure` tuple | `TaskStatus` / `is_failure` | `models.py:46-66` | P2 |
| `PROVIDER_EXHAUSTED` member + add to `is_terminal` tuple | `PhaseStatus` / `is_terminal` | `models.py:385-423` | P4 |
| New `TaskResult` fields `.get()` back-compat in `from_dict` | `HandoffRecord.from_dict` (`.get()` every field) | `models.py:337-349` | P2 |
| `to_dict` flat-serialize new fields | `TaskResult.to_dict` | `models.py:198-216` | P2 |
| New `_classify_transcript` 429 branch ABOVE is_error branching | insertion point | `rerun_tasks.py:582-591` | P2 |
| `reset_policy`/latch as keyword-only shared param | `_run_one_task` signature | `executor.py:963-975` | P3 |
| Spawn-unlocked / `with guard:` reconcile-locked | `_run_one_task` body | `executor.py:986-1044` | P3 |
| `lock if lock is not None else contextlib.nullcontext()` | guard idiom | `executor.py:1017` | P3 |
| Thread new param at K>1 call site | parallel call | `executor.py:1134-1145` | P3 |
| Thread new param at K=1 call site | sequential call | `executor.py:1337-1348` | P3 |
| Provider-failure status branch (ABOVE `:1012`, BELOW `:1003` gate) | status ladder | `executor.py:999-1015` | P3 |

---

## Status: Complete

**Summary — six reusable patterns documented with verified `file:line` exemplars:**

- **A. Pure detector** (`monitor.py:37-61`): module-level compiled regex + `(output_path: Path)` signature + `try/except (FileNotFoundError, OSError)` → neutral return (`NONE` for the new detector) + last-/last-N-line reverse scan. `read_text(errors="replace")` and the OSError tuple are load-bearing. The new detector adds a `_provider_failure_from_text` core (net-new factoring forced by `_classify_transcript`'s text input — no monitor exemplar).
- **B. Stream-json parse** (`rerun_tasks.py:555-574`, also `process.py:32-76`): `startswith("{")` pre-filter, `json.loads` in `try/except (JSONDecodeError, ValueError)`, keep LAST `{"type":"result"}` by overwrite-no-break, accumulate `usage.output_tokens` (message-first then top-level). **Subtype trap pinned:** 429 has `subtype=="success"` while `is_error` true → key on `is_error`+`api_error_status`, never `subtype`; insert the 429 branch ABOVE `rerun_tasks.py:579-580`.
- **C. String-Enum + `@property` membership tuples** (`models.py:46-66`, `:385-423`): `NAME="snake_case"` members; `is_success`/`is_failure`/`is_terminal` as `self in (…)` properties. Add `FAIL_PROVIDER_EXHAUSTED` to `is_failure` only; add `PhaseStatus.PROVIDER_EXHAUSTED` to `is_terminal` (the silent-omission hazard).
- **D. Serialization back-compat** — the spec's key compare resolved: **`TaskResult.from_dict` is HARD-KEYED** (`models.py:231-239`, bare `data[...]`), so new fields MUST use `.get(default)` like **`HandoffRecord.from_dict`** (`models.py:337-349`, `.get()` every field, forward-compat by design). `to_dict` is flat (`models.py:198-216`).
- **E. Concurrency** (`executor.py:963-1045`): shared state (`ledger`/`shadow_metrics`/`remediation_log`) threaded as keyword-only params; spawn UNLOCKED; single `with guard:` (`lock if … else contextlib.nullcontext()`, `:1017`) for all shared mutation. New `reset_policy`/latch threaded at BOTH call sites (`:1134-1145` K>1 lock=lock; `:1337-1348` K=1 lock=None). Storm bound is `≤ cap + (K−1)`, NOT `≤ cap`.
- **F. SoT discipline** (CLAUDE.md + spec §7): `src/superclaude/` → `make sync-dev` → `make verify-sync`; UV-only; `uv run ruff format --check src/ tests/` before push (CI gap vs `make lint`); feature branch; PR `--repo IronbellyOrg/IronClaude`.

**Verified directly this pass:** `monitor.py:1-572`, `models.py:40-350` + `:385-429`, `executor.py:963-1045` + `:1115-1159` + `:1330-1353`, `rerun_tasks.py:540-599`, `process.py:32-131`.

**Unverified (delegated / not Read this pass):** `build_resume_output` line range (R1/R3); `executor.py:1815`/`:1993` single-session spawn + `_determine_phase_status` (R3); `_provider_failure_from_text` text-core has no existing monitor exemplar (net-new). All marked inline above.
