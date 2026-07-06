# Research: Core Modules Current State

**Topic type:** File Inventory
**Scope:** `src/superclaude/pr_submit/` — models.py, classifier.py, detection.py, run_log.py, loop_guard.py, __init__.py + adjacency check of recovery.py & severity_router.py; fsm.py top-level symbols only.
**Status:** Complete
**Date:** 2026-06-12

---

## Quick reference: line counts (verified `wc -l`, 2026-06-12)

| Module | Lines | V1.1 touched? |
|---|---|---|
| `models.py` | 205 | YES — EventType+4, MonitorState+2, SkillResult+6 fields |
| `classifier.py` | 86 | YES — STATE_DECLINED + decline branch + `is_decline()` |
| `detection.py` | 193 | YES — 3 contract fields + `from_yaml` extend |
| `run_log.py` | 239 | YES — IDEMPOTENCY_SETS+1, rebuild_state folds |
| `loop_guard.py` | 78 | adjacency — `should_halt(fallback_round_counter, 1)` reused as-is (NO source change required; clamp lives in fsm) |
| `__init__.py` | 60 | YES — re-export wiring decision (see §INIT) |
| `recovery.py` | 135 | adjacency — touches EventType/MonitorState; see §RECOVERY |
| `severity_router.py` | 156 | adjacency — does NOT reference MonitorState/EventType; see §SEVROUTER |
| `fsm.py` | 802 | YES (R2 owns control-flow) — top-level symbols listed §FSM |

**CRITICAL re-grep note for the builder:** every line number below is a 2026-06-12 snapshot. Builder items must instruct the executor to RE-GREP the symbol (e.g. `grep -n 'round_counter += 1' fsm.py`) rather than trust the frozen `:NNN`. The `:793` increment in particular is load-bearing and must be located by content, not line.

---

## models.py (`src/superclaude/pr_submit/models.py`, 205 lines)

**Purpose:** Canonical pure data models — closed run-log event enum, severity tiers, single-FSM state lexicon, `Finding`/`SkillResult`/`PushDecision` dataclasses. NFR-6 core-purity: NO `anthropic` SDK, ZERO `gh`/`git` tokens. Module docstring (`models.py:1-11`) literally asserts "exactly 33 members".

**Imports (`models.py:13-16`):** `from __future__ import annotations`; `from dataclasses import dataclass, field`; `from enum import Enum`. NO intra-package imports (leaf module).

### `EventType(str, Enum)` — `models.py:19-70` — **VERIFIED EXACTLY 33 members**
Docstring at `:20-26` says "EXACTLY 33 members". Counted assignments = **33** (confirmed via awk). Full member list (identifier = value):
1. `RUN_STARTED = "run_started"` (:29)
2. `ENVIRONMENT_CHECK = "environment_check"` (:30)
3. `PR_CREATE_ATTEMPTED = "pr_create_attempted"` (:31)
4. `PR_CREATED = "pr_created"` (:32)
5. `MONITOR_ARMED = "monitor_armed"` (:33)
6. `BASELINE_CAPTURED = "baseline_captured"` (:34)
7. `POLL_ATTEMPT = "poll_attempt"` (:36)
8. `POLL_RESULT = "poll_result"` (:37)
9. `API_BACKOFF = "api_backoff"` (:38)
10. `CLASSIFIER_UNKNOWN_SHAPE = "classifier_unknown_shape"` (:39)
11. `REVIEW_DETECTED = "review_detected"` (:40)
12. `FINDINGS_NORMALIZED = "findings_normalized"` (:41)
13. `FINDING_VERIFIED = "finding_verified"` (:43)
14. `FINDING_UNVERIFIED = "finding_unverified"` (:44)
15. `ROUND_INCREMENTED = "round_incremented"` (:46)
16. `ROUTE_DECISION = "route_decision"` (:47)
17. `TROUBLESHOOT_STARTED = "troubleshoot_started"` (:49)
18. `TROUBLESHOOT_COMPLETED = "troubleshoot_completed"` (:50)
19. `FIX_APPLIED = "fix_applied"` (:51)
20. `VALIDATION_STARTED = "validation_started"` (:53)
21. `VALIDATION_COMPLETED = "validation_completed"` (:54)
22. `PUSH_DECISION = "push_decision"` (:56)
23. `PUSH_INITIATED = "push_initiated"` (:57)
24. `PUSH_COMPLETED = "push_completed"` (:58)
25. `REPLY_POSTED = "reply_posted"` (:60)
26. `THREAD_RESOLVED = "thread_resolved"` (:61)
27. `IDEMPOTENCY_SKIP = "idempotency_skip"` (:62)
28. `TERMINAL_CLEAN = "terminal_clean"` (:64)
29. `TERMINAL_TIMEOUT = "terminal_timeout"` (:65)
30. `TERMINAL_MAX_ROUNDS = "terminal_max_rounds"` (:66)
31. `TERMINAL_HALTED = "terminal_halted"` (:67)
32. `TERMINAL_FAILED = "terminal_failed"` (:68)
33. `PUSH_ABORTED_OR_NOT_LANDED = "push_aborted_or_not_landed"` (:70)

**V1.1 delta (addendum §6.1):** += 4 members → docstring must change `33 → 37`. New: `REREVIEW_REQUESTED="rereview_requested"`, `DECLINE_DETECTED="decline_detected"`, `AUGGIE_FALLBACK_INVOKED="auggie_fallback_invoked"`, `MAX_ROUNDS_CLAMPED="max_rounds_clamped"`. **Builder item must update BOTH the class docstring count AND `run_log.py`'s "33" prose** (see run_log §). NOTE: the docstring at `:20` and the run_log error string both hardcode "33" — re-grep for `33` across `models.py` + `run_log.py`.

### `Severity(str, Enum)` — `models.py:73-80` — 5 members (UNCHANGED by V1.1)
`CRITICAL="Critical"`, `HIGH="High"`, `MEDIUM="Medium"`, `LOW="Low"`, `NIT="Nit"`.

### `MonitorState(str, Enum)` — `models.py:83-113` — **VERIFIED 19 members**
Working states (`:94-106`): `S0_IDLE`, `S2_CLASSIFY`, `S2B_VERIFY="S2b_VERIFY"`, `S3_DIAGNOSE`, `S3_FIXING`, `S7_VALIDATING`, `S4_PUSHING`, `S4_HALT_BEFORE_PUSH` (spec's `S4'_HALT_BEFORE_PUSH`, prime dropped), `S6_REPLYING`, `RESOLVING`, `S5_AWAITING_REREVIEW`, `PROPOSED`, `REPORT_ONLY`.
Terminals (`:108-113`): `TERMINAL_CLEAN`, `HALT_MAX_ROUNDS`, `HALT_HUMAN`, `VALIDATION_FAIL`, `TERMINAL_TIMEOUT`, `TERMINAL_FAILED`.

**V1.1 delta (§6.1):** += 2 NON-terminal: `S5A_RETRIGGER_REVIEW="S5a_RETRIGGER_REVIEW"`, `S5B_AUGGIE_FALLBACK="S5b_AUGGIE_FALLBACK"`. Must be OMITTED from `TERMINAL_STATES`.

### `TERMINAL_STATES = frozenset({...})` — `models.py:117-126`
Exact members: `TERMINAL_CLEAN`, `HALT_MAX_ROUNDS`, `HALT_HUMAN`, `VALIDATION_FAIL`, `TERMINAL_TIMEOUT`, `TERMINAL_FAILED` (6). V1.1: NO new terminals added (new states are non-terminal) → frozenset UNCHANGED.

### `@dataclass Finding` — `models.py:129-162` — UNCHANGED by V1.1
Fields (with defaults): `path:str`, `line:int`, `body:str`, `severity_hint:str|None=None`, `category:str|None=None`, `confidence:str|None=None`, `in_diff:bool=True`, `comment_id:int|None=None`, `remapped_severity:Severity|None=None`, `verification_status:str="unverified"`, `needs_human_decision:bool=False`. Property `fix_key` (`:151-162`): `sha256(path\nline\nbody)`, lazy `import hashlib`.

### `@dataclass SkillResult` — `models.py:165-187` — **V1.1 ADDS 6 FIELDS**
Current fields (with defaults): `state:MonitorState=S0_IDLE` (:176), `round_counter:int=0` (:177), `push_count:int=0` (:178), `reply_count:int=0` (:179), `summary_posted:bool=False` (:180), `applied_edits:int=0` (:181), `findings:list[Finding]=field(default_factory=list)` (:182), `validation_status:str="pending"` (:183), `push_decision:"PushDecision|None"=None` (:184), `proposal:str|None=None` (:187).
**V1.1 delta (§6.1):** += `rereview_request_count:int=0`, `fallback_engaged:bool=False`, `auggie_review_invoked:bool=False`, `decline_detected:bool=False`, `effective_max_rounds:int|None=None`, `fallback_round_counter:int=0`.

### `@dataclass PushDecision` — `models.py:190-205` — UNCHANGED by V1.1
Fields: `predicate_1_ordinal:bool=False`, `predicate_2_validated:bool=False`, `predicate_3_no_human:bool=False`, `predicate_4_under_cap:bool=False`, `predicate_5_applied_edits:int=0`, `authorized:bool=False`.

---

## classifier.py (`src/superclaude/pr_submit/classifier.py`, 86 lines)

**Purpose:** Pure 3-state review classifier (`"polling"`/`"clean"`/`"findings"`). Keys ONLY on `contract.augment_bot_login`. NFR-6: no review-fetch tokens.
**Imports (`:12-14`):** `from __future__ import annotations`; `from typing import Any`. NO intra-package imports.

**STATE_* constants (`:17-19`):** `STATE_POLLING="polling"`, `STATE_CLEAN="clean"`, `STATE_FINDINGS="findings"`.
**Helpers:** `_login_of(entry:dict)->str|None` (:22-36, dual author/user shape), `_augment_entries(entries, bot_login)->list[dict]` (:39-43), `_entry_has_findings(review:dict)->bool` (:46-57, checks `has_findings` flag or `findings_count>0`).

**`classify(payload:dict, contract:Any)->str`** — `:60-86`. Return branches:
- no augment_reviews → `STATE_POLLING` (:75-77)
- any `_entry_has_findings` → `STATE_FINDINGS` (:82-83)
- augment-authored comments present → `STATE_FINDINGS` (:84-85)
- else → `STATE_CLEAN` (:86)

**V1.1 delta (§6.2):** += `STATE_DECLINED="declined"`; `classify()` returns it when an Augment comment matches decline regexes — **the decline check must run BEFORE the clean/findings branch** (so decline never miscounted as findings). New pure `is_decline(comment, contract, *, watermark)->bool`. NOTE: `classify()` currently takes `(payload, contract)` only — no watermark param; builder must decide whether decline detection is inside `classify` (needs watermark threading) or a separate `is_decline` the FSM calls. Addendum lists `is_decline` under §6.2 as a sibling pure fn.

---

## detection.py (`src/superclaude/pr_submit/detection.py`, 193 lines)

**Purpose:** Detection-contract loader + poll surface. `poll_augment_review` + `DetectionContract` + `DetectionContractLocked`. T-210 lock gate.
**Imports (`:13-21`):** `from __future__ import annotations`; `import re`; `from dataclasses import dataclass, field`; `from pathlib import Path`; `import yaml`; `from .classifier import classify`.

**Module constants:** `_CONTRACT_PATH` (:27-33, the shipped `skills/sc-pr-submit-protocol/refs/detection-contract.md`), `_LOCAL_OVERRIDE_PATH` (:37-39, gitignored `.dev/pr-monitor/detection-contract.locked.md`).

**`DetectionContractLocked(RuntimeError)`** — `:47-52`. T-210 gate exception.

**`@dataclass DetectionContract`** — `:55-143`. Current fields (with defaults):
`augment_bot_login:str|None=None` (:64), `augment_author_association:list[str]=field(default_factory=list)` (:65), `augment_app_slug:str|None=None` (:66), `emission_shape:str|None=None` (:67), `findings_locus:str|None=None` (:68), `severity_field_path:str|None=None` (:69), `review_completeness_signal:str|None=None` (:70), `probe_evidence:str|None=None` (:71), `locked:bool=False` (:72).
**NO existing regex/trigger-phrase fields** — V1.1's `decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases` are all NET-NEW.
Methods: `from_yaml(cls, data:dict)` (:74-89, reads each field via `data.get(...)`), `load(cls, path=None, *, require_locked=True, prefer_local_override=False)` (:91-132), `for_arming(cls)` (:134-143).
Helper `_extract_yaml_block(markdown_text)->str|None` (:146-149, regex matching a fenced yaml block).

**Poll seam:** `_fetch_payload(pr_num)->dict` (:158-160, returns `{"reviews":[],"comments":[]}`), `poll_augment_review(pr_num, payload=None, contract=None)->str` (:163-193, delegates to `classify`).

**V1.1 delta (§6.2):** `DetectionContract` += `decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases:list[str]` (defaults baked, probe-lockable). Extend `from_yaml` (add 3 `data.get(...)` lines). Also update shipped `refs/detection-contract.md` YAML block (stays `locked:false`). NOTE the `from_yaml` is positionally a single `cls(...)` call returning all fields — builder adds 3 kwargs there.

---

## run_log.py (`src/superclaude/pr_submit/run_log.py`, 239 lines)

**Purpose:** Write-ahead JSONL run-log; JSONL authoritative, snapshot rebuildable. NFR-7 redaction. Core-pure I/O.
**Imports (`:16-24`):** `from __future__ import annotations`; `hashlib`, `json`, `os`, `re`; `from pathlib import Path`; `from .models import EventType`.

**`IDEMPOTENCY_SETS` (`:26-33`)** — exact tuple (5 members): `("processed_review_ids", "processed_finding_ids", "replied_comment_ids", "resolved_thread_ids", "pushed_commit_shas")`. Comment on `processed_finding_ids` notes "keyed on fix_key".
**`_VALID_EVENT_VALUES = frozenset(e.value for e in EventType)`** (:35) — derives directly from EventType so the 4 new events validate automatically once models.py changes.
**Redaction:** `_REDACTION_PATTERNS` (:38-49, 5 regexes), `_REDACTED="[REDACTED]"` (:50). `fix_key(path,line,body)->str` (:53-55). `_redact(value)` recursive (:58-69).

**`class RunLog`** — `:72-239`. `__init__(self, pr_number, output_dir)` (:75-84). Key methods:
- `append(event:dict)->dict` (:100-122): validates `event_type in _VALID_EVENT_VALUES` else `ValueError` — **error string at `:108-110` hardcodes "33"** ("not one of the 33 §11.3 events"); docstring `:104` says "33 closed enum values". **Builder must update both "33"→"37".** RE-GREP `33` in run_log.py.
- `write_ahead(event)` (:124-130, alias of append).
- `read_events()->list[dict]` (:134-143).
- **`rebuild_state()->dict`** (:145-190): returns dict with keys `pr_number`, `state`, `round_counter`, `push_count`, `reply_count`, `last_event_id`, **+ one key per IDEMPOTENCY_SET** (`:152-160` builds `{s:[] for s in IDEMPOTENCY_SETS}`). Folds: `ROUND_INCREMENTED`→round_counter (:167-168), `PUSH_COMPLETED`→push_count + pushed_commit_shas (:169-172), `REPLY_POSTED`→reply_count + replied_comment_ids (:173-176), `THREAD_RESOLVED`→resolved_thread_ids (:177-178), `FINDINGS_NORMALIZED`→processed_review_ids (:179-185), `FIX_APPLIED`→processed_finding_ids (:186-187). Sets sorted at `:188-189`.
- `materialize_snapshot()->dict` (:192-196).
- `record_idempotent(set_name, key)->bool` (:200-219): validates `set_name in IDEMPOTENCY_SETS` else `ValueError` (:207-208); appends `IDEMPOTENCY_SKIP` if present (:211-217). Signature: `(self, set_name:str, key)`.
- `default_output_dir(pr_number, timestamp)` staticmethod (:223-231).
- `round_dirs(round_n)` (:233-239).

**V1.1 delta (§6.3):** `IDEMPOTENCY_SETS += ("auggie_review_invoked",)` → **6 sets**. Because `rebuild_state` builds the per-set keys from the tuple AND `record_idempotent` validates against it, adding the tuple member auto-wires the snapshot key + idempotency validation. NEW folds required in `rebuild_state`: fold `AUGGIE_FALLBACK_INVOKED.pr_number`→`auggie_review_invoked` set; fold `MAX_ROUNDS_CLAMPED.effective_max_rounds`→rebuilt `effective_max_rounds` (take **min** seen, monotone); count `REREVIEW_REQUESTED`→`rereview_request_count`. **The rebuilt-state dict gains new top-level keys** (`effective_max_rounds`, `rereview_request_count`) not currently present — builder adds them to the `state={...}` init at `:152-160`. Plus the two "33"→"37" prose updates noted above.

---

## loop_guard.py (`src/superclaude/pr_submit/loop_guard.py`, 78 lines)

**Purpose:** INV-001 round-counter fence-post (P0 module). Pure arithmetic, ZERO shell tokens.
**Imports (`:15-17`):** `from __future__ import annotations`; `from dataclasses import dataclass`.
**Constants:** `DEFAULT_MAX_ROUNDS=2` (:19), `HARD_CAP_MAX_ROUNDS=5` (:20). (NOTE: fsm.py re-declares these same two at fsm:30-31.)
**`should_halt(round_counter:int, max_rounds:int)->bool`** (:23-30): returns `round_counter >= max_rounds` (INV-5 `>=`).
**`user_label(round_counter)->int`** (:33-35): `round_counter + 1`.
**`@dataclass RoundCounter`** (:38-78): fields `value:int=0`, `max_rounds:int=DEFAULT_MAX_ROUNDS`. Methods `on_rereview(*, review_observed, sha_attributed_to_our_push)->bool` (:50-61, single increment edge), `vanished_rereview()->None` (:63-69, no-op monotonic), `should_halt()->bool` (:71-73), `label` property (:75-78).

**V1.1 delta:** Addendum §6.4 says the fallback sub-loop *uses* `loop_guard.should_halt(fallback_round_counter, 1)` — this is a CALL from fsm.py with the existing signature. **`should_halt` already accepts arbitrary `(round_counter, max_rounds)` → NO source change to loop_guard.py is required** for the clamp-to-1 fallback budget. `clamp_max_rounds` lives in fsm.py (§6.4), not here. Builder item for loop_guard.py is likely a NO-OP (or doc-only via `refs/loop-guard.md`). Mark: loop_guard.py source is **unchanged**; only the ref doc gets INV-R1/R2/R3 + `fallback_round_counter` mention (§6.5).

---

## __init__.py (`src/superclaude/pr_submit/__init__.py`, 60 lines) — §INIT

**Purpose:** Package facade. Re-exports the public API.
**Current imports (`:21-32`):**
- `from .classifier import classify`
- `from .detection import DetectionContract, DetectionContractLocked, poll_augment_review`
- `from .fsm import RunConfig, evaluate_push_decision, parse_args, run_skill, transition`
- `from .models import (EventType, Finding, MonitorState, PushDecision, Severity, SkillResult)`
- `from .severity_router import remap_severity, route`

**Current `__all__` (`:38-60`):** `classify`, `poll_augment_review`, `DetectionContract`, `DetectionContractLocked`, `run_skill`, `transition`, `parse_args`, `evaluate_push_decision`, `RunConfig`, `remap_severity`, `route`, `EventType`, `Finding`, `MonitorState`, `PushDecision`, `Severity`, `SkillResult`.

**Re-export wiring decision for new V1.1 symbols:**
- `STATE_DECLINED` (classifier) — NOT currently re-exported (existing `STATE_POLLING/CLEAN/FINDINGS` are also NOT in `__all__`), so consistency says leave STATE_DECLINED out of `__init__` unless tests import it from the package root. **Builder should grep tests/ for `from superclaude.pr_submit import STATE_` to decide.**
- `is_decline` (classifier/detection) — new pure fn; re-export only if tests import it at package root.
- `clamp_max_rounds` (fsm) — new pure fn; the existing fsm re-export line (`:23`) lists `evaluate_push_decision, parse_args, run_skill, transition` but NOT all fsm helpers — so `clamp_max_rounds` re-export is OPTIONAL, driven by test import style.
- New EventType/MonitorState members are auto-exported via the existing `EventType`/`MonitorState` re-export (enums carry their members) — **NO `__init__` change needed for the enum deltas**.
- New SkillResult fields auto-exported via existing `SkillResult` re-export.
**Conclusion:** `__init__.py` changes are CONDITIONAL on test import style (R5/R6 own the test mapping). The enum/dataclass-field deltas need NO `__init__` edit; only newly-introduced top-level *functions/constants* (`is_decline`, `clamp_max_rounds`, `STATE_DECLINED`) might need wiring IF a test does `from superclaude.pr_submit import <name>`. Mark as **Unverified until test-import audit (R5/R6)**.

---

## recovery.py (`src/superclaude/pr_submit/recovery.py`, 135 lines) — §RECOVERY (adjacency)

**Purpose:** Crash-window recovery (§12.1/INV-007). Reconstructs from JSONL; 3-way branch on remote reachability.
**Imports (`:21-22`):** `from .models import EventType, MonitorState`; `from .run_log import RunLog`.
**References MonitorState/EventType — YES, materially:**
- `resume(run_log_path)->dict` (:30-44): calls `rl.rebuild_state()`.
- `detect_crash_window(run_log)->dict|None` (:47-70): keys on `EventType.PUSH_INITIATED`, `PUSH_COMPLETED`, `PUSH_ABORTED_OR_NOT_LANDED` values.
- `resolve_crash_window(...)->tuple[str, MonitorState]` (:73-135): returns `MonitorState.S5_AWAITING_REREVIEW` (Branch A, :111), `S4_PUSHING` (Branch B, :123), `HALT_HUMAN` (Branch C, :135); appends `PUSH_COMPLETED`/`PUSH_ABORTED_OR_NOT_LANDED`/`TERMINAL_HALTED`.
- Branch constants: `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS` (:25-27).

**V1.1 impact:** The addendum §6 does NOT list recovery.py as a build target. The new states `S5A_RETRIGGER_REVIEW`/`S5B_AUGGIE_FALLBACK` are non-terminal working states; if a crash occurs while in them, `rebuild_state` reads `state_after` straight from JSONL (string), so recovery resumes into them WITHOUT a code change. **BUT** Branch A currently hard-resumes to `S5_AWAITING_REREVIEW` (:111) — with V1.1's `RESOLVING→S5A_RETRIGGER_REVIEW` edge change, a crash recovered as "landed" might now need to resume at `S5A_RETRIGGER_REVIEW` (re-trigger not yet posted) rather than `S5_AWAITING_REREVIEW`. **This is a POSSIBLE seam the addendum did not call out** — flag for the builder as a review/risk item (Branch A resume target vs. the new re-trigger step). Mark: recovery.py likely UNCHANGED per the spec, but the Branch-A→S5 hardcode is a latent interaction worth a checklist note. **Unverified whether spec intends a recovery change.**

---

## severity_router.py (`src/superclaude/pr_submit/severity_router.py`, 156 lines) — §SEVROUTER (adjacency)

**Purpose:** Severity re-grade + troubleshoot routing (C3). Pure.
**Imports (`:15-17`):** `from .models import Finding, Severity`. **Does NOT import MonitorState or EventType.**
**Surface:** `_RANK`/`_BY_RANK` (:21-28), `_CATEGORY_TABLE` (:32-51), routes `ROUTE_FIX`/`ROUTE_DEEP_FIX`/`ROUTE_REPORT_ONLY` (:54-56), `remap_severity(finding, *, deep=False)->Finding` (:88-137), `route(finding)->str` (:140-156).
**V1.1 impact:** NONE. Not a §6 build target; touches only `Finding`/`Severity` (both unchanged by V1.1). **severity_router.py is UNCHANGED.** No new-state/new-event coupling.

---

## fsm.py top-level symbols (`src/superclaude/pr_submit/fsm.py`, 802 lines) — §FSM (R2 owns deep control-flow)

Per scope I list top-level symbols only (R2 traces transition()/run_skill() + the :793 increment + RunConfig seams).
**Constants:** `DEFAULT_MAX_ROUNDS=2` (:30), `HARD_CAP_MAX_ROUNDS=5` (:31), `MIN_POLL_INTERVAL=30` (:32), `DEFAULT_TIMEOUT=1800` (:33), `POLL_INTERVAL_ERROR` (:35), `MAX_ROUNDS_ERROR` (:36), `PROPOSE_PROMPT="fix these? y/n"` (:39), `NO_CODE_CHANGE_TEXT` (:267), `TRIVIAL_FIX_MAX_LINES=10` (:268), `VALIDATION_GATES` (:416), `MANDATORY_GATES` (:422), `PR_TARGET_REPO="IronbellyOrg/IronClaude"` (:449), `BACKOFF_BASE` (:520), `BACKOFF_CAP=300` (:521).
**Classes:** `SkillArgs` (@dataclass, :47-68), `DispatchPlan` (@dataclass, :374-382), `RunConfig` (@dataclass, :653-677).
**Functions (top-level):** `build_arg_parser` (:69), `parse_args` (:90), `gate_arm` (:125), `gate_edit` (:130), `should_halt_rounds` (:135), `evaluate_push_decision` (:145), `push_fail_state` (:179), `push_idempotency_key` (:199), `build_push_triad` (:210), `is_groundable` (:271), `audit_validated_not_verified` (:282), `is_trivial_fix` (:302), `build_reply` (:307), `seed_troubleshoot` (:344), `batch_by_file` (:363), `plan_dispatch` (:383), `run_validation_gates` (:425), `pr_target_ok` (:452), `origin_ok` (:467), `needs_rebase` (:478), `is_cross_cutting` (:483), `next_backoff` (:524), `timed_out` (:536), `poll_outcome` (:541), `transition` (:560), `_noop` (:627), `_default_verify` (:631), `_default_apply_edits` (:642), `run_skill` (:679).

**Key V1.1 seam facts (for R2 handoff):**
- `transition(state, event, context=None)->MonitorState` (:560-625) is a flat `if edge == (...)` lookup table — new edges are added as more `if edge ==` branches.
- `run_skill(config=None, **overrides)->SkillResult` (:679-802). **The optimistic increment `result.round_counter += 1` is at fsm.py:793** (VERIFIED — under the `# Re-review attributed to our push` comment at :792, inside the cycle loop). §6.4 [MOD]: REMOVE this, tick only on an injected attributed-re-review outcome.
- `RunConfig` (:653-677) current seams: `monitor_ordinal`, `max_rounds`, `poll_interval`, `timeout`, `pr_number`, `resume`, `findings`, `rereview_findings`, `review_state`, `arm_monitor=_noop`, `verify=_default_verify`, `apply_edits=_default_apply_edits`, `run_validation`, `do_push=_noop`, `do_reply=_noop`, `do_resolve=_noop`. §6.4 adds: `do_retrigger:Callable=_noop`, `invoke_auggie_review:Callable=_noop`, a per-cycle `rereview_outcome` sequence (`"attributed"|"declined"|"timeout"`).
- `_noop(*_args, **_kwargs)->None` (:627-628) is the existing seam-default — the new `do_retrigger`/`invoke_auggie_review` reuse it.
- `clamp_max_rounds(effective, hard=1)->int` is NET-NEW (§6.4), `min(effective, hard)`, lives in fsm.py.

---

## Summary for the builder (one checklist item per file-delta)

**Source changes REQUIRED (6 modules):**
1. `models.py` — EventType +4 members (docstring "33"→"37"); MonitorState +2 non-terminal (NOT in TERMINAL_STATES); SkillResult +6 fields. Leaf module, no import changes.
2. `classifier.py` — STATE_DECLINED const; decline branch BEFORE clean/findings in `classify`; `is_decline(comment, contract, *, watermark)` pure fn.
3. `detection.py` — DetectionContract +3 fields (`decline_phrase_regex`, `decline_retrigger_regex`, `accepted_trigger_phrases`); extend `from_yaml` (+3 `data.get`); update shipped `refs/detection-contract.md` YAML (stays locked:false).
4. `run_log.py` — IDEMPOTENCY_SETS +1 → 6 (auto-wires snapshot key + record_idempotent validation); `rebuild_state` +new folds (AUGGIE_FALLBACK_INVOKED, MAX_ROUNDS_CLAMPED min-monotone, REREVIEW_REQUESTED count) + 2 new state keys; "33"→"37" in docstring + ValueError string.
5. `fsm.py` (R2 deep) — new transition edges; REMOVE `:793` optimistic `round_counter += 1`; RunConfig +`do_retrigger`/`invoke_auggie_review`/`rereview_outcome`; NEW `clamp_max_rounds`.
6. `__init__.py` — CONDITIONAL re-export of `is_decline`/`clamp_max_rounds`/`STATE_DECLINED` (only if a test imports them at package root — enum/field deltas auto-export). **Unverified until R5/R6 test-import audit.**

**Source UNCHANGED (adjacency):**
- `loop_guard.py` — `should_halt(fallback_round_counter, 1)` reuses existing signature; clamp lives in fsm. Source NO-OP; only `refs/loop-guard.md` doc delta.
- `severity_router.py` — no coupling to new states/events; UNCHANGED.
- `recovery.py` — not a §6 target; resumes into new string-states via rebuild_state without change. **RISK NOTE:** Branch-A hard-resume to `S5_AWAITING_REREVIEW` (:111) may semantically need `S5A_RETRIGGER_REVIEW` post-V1.1 (re-trigger not yet posted on recovery). Flag as a builder review item — **Unverified whether spec intends a recovery edit.**

**Verified counts:** EventType=33 (→37), MonitorState=19 (→21), TERMINAL_STATES=6 (unchanged), IDEMPOTENCY_SETS=5 (→6), SkillResult fields=10 (→16), DetectionContract fields=9 (→12). All confirmed by reading the source 2026-06-12.
