# monitor.py Insertion-Point Inventory (P1, Step 2.1)

**File:** `src/superclaude/cli/sprint/monitor.py`
**Verified:** 2026-06-15, read directly from current file.

| Concern | Research cite | Verified line(s) | Drift | Notes |
|---------|---------------|------------------|-------|-------|
| Import-block end | 8-19 | 8-19 | none | `from __future__`, `json`, `logging`, `re`, `threading`, `time`, `pathlib.Path`, then 3 local imports. **No `enum`, no `dataclasses`** imported — both must be added (Steps 2.3). |
| `detect_error_max_turns` range | 37-61 | 37-61 | none | OSError-tolerant `read_text(errors="replace")` (47-49), empty guard (51-52), last-non-empty-line reversed scan (54-59). Mirror for `detect_provider_failure`. |
| Regex-constant block | 33-34 | 33-34 | none | `ERROR_MAX_TURNS_PATTERN` (33), `PROMPT_TOO_LONG_PATTERN` (34). New `_RE_ALL_ACCOUNT`/`_RE_SINGLE_ACCOUNT` go alongside (file uses both `*_PATTERN` and will use `_RE_*` private convention). |
| `count_turns_from_output` → `OutputMonitor` boundary | ~250 / ~253 | `return count` at **250**; `class OutputMonitor` at **253**; insertion zone = blank lines **251-252** | none | All new P1 symbols (`ProviderFailure`, `ProviderFailureSignal`, `_provider_failure_from_text`, `detect_provider_failure`) insert in this zone. |
| `_process_chunk` json.loads idiom | ~389 | **389** | none | `try: event = json.loads(line) except (json.JSONDecodeError, ValueError):` — the parse-tolerance idiom the text-core mirrors. |

**Conclusion:** Every research-cited line number matches the current file exactly. Insertion zone (251-252) and the `detect_error_max_turns` mirror shape (37-61) are confirmed. Proceeding to fixtures (Step 2.2) and imports/symbols (Steps 2.3-2.4).
