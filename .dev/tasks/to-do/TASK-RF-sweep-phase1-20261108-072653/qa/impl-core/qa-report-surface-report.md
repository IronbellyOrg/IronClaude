# QA Report - Report-surface lens (T184)

**Reviewer lens:** report.py rendering vs DESIGN 7.5, GQ-35 / GQ-63 decisions
**Date:** 2026-11-12
**fix_authorization:** false (report-only)
**Phase:** task-qualitative (code gate, report-surface lens). The Axis column is not used; findings carry file:line evidence.
**Scope read:** `src/superclaude/cli/sweep/report.py` (all 692 lines, 5 chunks), `models.py`, the `classify_all` / `removable` / `safe_to_close` / rule bodies of `classify.py`, the `probes.py` source-row and version readers, `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, `.gitignore:252-259`, DESIGN `docs/designs/orchestrator-mode.md` 7.1, 7.2, 7.4, 7.5, 6 and the addendum, SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` section 9, FR-011, FR-016, NFR-015 and line 238, the OQ-4, OQ-5, OQ-6 decision records, and the Phase 8 test-result files.
**Method:** every claim below was checked against the file on disk. Two scratch probes (`uv run --frozen --no-sync python -B`, script in a private `/tmp` dir, removed afterwards) built `SweepResult` objects by hand and called `report.render`, `report.to_json`, `sanitize`, `cell` and `_version_line`. Nothing under the repository was written.

---

## Findings

### F-1 (MAJOR) Waiting (a) age ignores the blocked contract's mtime, so the first-listed waiting source can never be aged or sorted oldest-first

- Evidence: `report.py:129-138` (`_wait_age_s` reads only `orca.agent_wait`; a row with no Orca `agent_wait` returns None). `models.py:78-86` (`ContractRecord` has `path`, `worker_status`, `blocked_question`, `reason`, `report_path`, `artifacts`, `command` and no time field). SPEC `merged-requirements.md:238`: "Waiting (a) age is `now - t`, where `t` is the earliest of the contract file's `st_mtime` for a blocked contract and the `agentWait` timestamp field ... With no `t`, the row is in the unknown-age group. [SP-15]". SPEC FR-011 (`:105`) sorts (a) "oldest first (age as section 7 defines it [SP-15])". DESIGN 7.2 line 451 says the design "keeps every SPEC field", DESIGN 7.5 line 642 sorts (a) "oldest first, then rows of unknown age", and DESIGN section 13 (D1-D10) lists no deviation from SP-15 (grep for `SP-15` in `orchestrator-mode.md` returns nothing).
- Probe: three (a) rows, two of them `blocked_contract` (rule 1) with no `agent_wait`, rendered as `Age = unknown` for both and sorted by ID; only the `waiting_signal` row got `2h 0m`.
- What is wrong: rule 1 (`blocked_contract`) is the first classification rule and the main source of "waiting on a person (a)". Under this implementation every such row has unknown age, so the FR-011 oldest-first sort only works for the unverified `agentWait` path (open item 6: the `agentWait` timestamp key was never captured live; `1.0a-facts.md:35`, `readonly-probe.md:505`). The builder disclosed this in the task file's Phase 8 findings ("a blocked contract has no age because `models.py` carries no contract mtime") but it is not a recorded design deviation and was not put to the owner.
- Smallest fix, either one: (a) add `mtime: datetime | None = None` to `ContractRecord`, set it in `probes.read_contract` from the `os.stat` it already takes, and make `_wait_age_s` use the earlier of the contract mtime and the `agentWait` time (report.py stays pure); or (b) add a Deviation row (D11, "Waiting (a) age uses agentWait only; SP-15 contract mtime dropped") to DESIGN section 13 and the owner-visible Findings, with the SPEC FR-011 test changed to match.

### F-2 (MINOR) The Waiting (b) column "Policy reason" holds the rule name, not a reason

- Evidence: `report.py:291` (header `("ID", "Policy reason", "Evidence")`) and `report.py:293` (cell is `r.classification.rule`). Probe output: `| orca:f | waiting_signal | e |`.
- Every (b) row therefore shows `waiting_signal`, which says nothing about why the policy blocks it; the real reason sits in the Evidence column (`classify.py:269` frozen plan, `classify.py:274` ready Task). SPEC section 9 item 4 asks for "the policy reason and evidence".
- Smallest fix: rename the column to `Rule`, or fill it with `frozen plan` / `ready Task needing ownership review`.

### F-3 (MINOR) `sanitize` neutralises Markdown link syntax but not bare URLs

- Evidence: `report.py:587-595` (replacement table). Probe: `[l](http://e.com)` becomes `\[l\](http://e.com)`; `![x](http://e/p.png)` becomes `!\[x\](http://e/p.png)`. A GitHub-flavoured renderer auto-links the bare `http://e.com`.
- No hidden link text is possible (the deceptive `[text](url)` form is closed), the report is local and never posted, so this is MINOR. FR-016 says "no untrusted text becomes an active tag or link"; the fixture only tests the bracket form.
- Smallest fix, optional: also break `://` or document the limit in the `sanitize` docstring.

### F-4 (MINOR) A 200-character cut can split a backslash escape and leave a lone `\` before `...`

- Evidence: `report.py:599-602`. Probe: `cell("|" * 150)[-8:]` is `\|\|\...`. The orphan backslash escapes the first dot in Markdown and no unescaped `|` can appear, so the column count is safe; the look is only slightly off.
- Smallest fix: after the cut, drop one trailing backslash if the kept text ends in an odd number of backslashes.

### F-5 (MINOR) The lock-line version match strips only after the first `-`

- Evidence: `report.py:165` (`observed.split("-", 1)[0] == CHECKED_ORCA_VERSION`). SPEC NFR-015 (`merged-requirements.md:144`) says "leading MAJOR.MINOR.PATCH part". Probe: `1.4.245-aidev02.780594c521aa` gives `unlikely`, `1.4.246` gives `UNVERIFIED ... observed 1.4.246`, `None` gives `observed unknown` (all three NFR-015 test cases hold). A value such as `1.4.245+build` or `1.4.245.1` prints UNVERIFIED although its leading part matches. That errs on the safe side, so MINOR.
- Smallest fix: compare against a `^\d+\.\d+\.\d+` match of the observed value.

### F-6 (MINOR) JSON `safe_to_close.reason` echoes "release" vocabulary

- Evidence: `classify.py:507` (`terminal_state=..., next_action=...`) and `classify.py:516` (`not releasable (...)`). These reach only the JSON `reason` (`report.py:652-655`); the Markdown Sessions cell prints just `terminal / worktree` values (`report.py:436`). It quotes Orca's own field values and states "no", so it is not advice. A future test that greps the JSON for `release` would trip on it.
- Smallest fix: none needed now; keep the DESIGN test word-scan limited to the `next inspection` map as written.

### F-7 (MINOR) `_wait_time` and `_WAIT_TIME_KEYS` are duplicated between report.py and classify.py

- Evidence: `report.py:41` and `report.py:108-126` against `classify.py:97` and `classify.py:130-138`. They agree today (same six keys, same `min` rule, same future-timestamp handling), but the key list is itself UNVERIFIED (`report.py:40` comment, open item 6); a fix to one copy will silently split the "Age" column from the evidence text "waiting since ...".
- Smallest fix: keep one copy (a shared helper in `models.py`) when open item 6 is closed.

### F-8 (MINOR) "Every count over sessions" is read as "every count line"; two count displays have no Distinct line

- Evidence: the Scope line (`report.py:195-197`, `sessions <shown>/<total>`) and the Sessions heading (`report.py:411`) print session counts with no `Distinct affected sessions:` line; the line is printed under Waiting (a), Waiting (b), Could not determine and the Shift Brief (`report.py:276`, `:323`, `:349`, `:511`). DESIGN 7.5 line 645 and the layout block (lines 606-628) put both counts there themselves, so the reading is defensible; the builder recorded it as choice (7). Also `SECTIONS` is an untyped tuple (`report.py:542`) where DESIGN 7.1 line 428 types it `tuple[Callable[...], ...]`.
- Smallest fix: pin the reading in `test_report.py` (item 10.x) so a later change cannot drift; add the `Callable` annotation if the type is wanted.

---

## Check details (what was run, per check)

- C1 Heading order: `report.py:542-555` lists 12 functions in the DESIGN 7.1/7.5 order (header, source coverage, waiting a, waiting b, could not determine, retained problems, sessions, worktrees, historical, shift brief, what I could not determine, footer). Probe heading dump from an empty result printed the 11 `##`/`###` headings in the DESIGN 7.5 order, including the `### Ready Tasks needing ownership review (creator not observable in Phase 1)` sub-heading and `Ready Tasks: <N>` line (`report.py:302`, `:321`).
- C2 Header block: probe output matched DESIGN 7.5 lines 606-616 line for line (READ ONLY line, Scope line with `(lower bound: remote hosts not scanned)` and `window 6h`, `Orca binary:`, `Sources:`, `Messages coverage: partial`, lock line, `Untracked paths:` line); the three bracketed conditional lines print in the DESIGN order only when their condition holds (`report.py:205-210`; probe with `avail=False`, `bound_reached=2`, `truncated=True` printed all three, the empty probe none).
- C3 Empty-section string: `report.py:29`; the empty probe printed it 9 times (every section that can be empty).
- C4 200-character cut: `cell("x"*300)` has length 200 and ends `...`; `cell("x"*200)` and `cell("x"*201)` both have length 200 (probe); `report.py:599-602`. JSON values are not cut (`report.py:613-692` call `sanitize` only).
- C5 Sanitize: probes show ESC/CSI/OSC (including an OSC 8 hyperlink and an unterminated OSC), NUL, DEL, a C1 byte, CR, tab, U+2028, BOM, bidi isolates/overrides removed or folded to a space; `|` and `\` escaped (backslash first, `report.py:587`); `<`, `>`, `[`, `]` neutralised; a newline cannot start a heading or table row (`"\n# H\n| x |"` became one line with `\|`). Residual limit: F-3.
- C6 Version line: `report.py:164-171`; the three NFR-015 cases hold (probe). Residual: F-5.
- C7 `bound_reached`, page and worktree-lower-bound lines: strings at `report.py:31-33` equal DESIGN 7.5 lines 614-616 byte for byte; the `bound_reached >= 1` and full-page conditions are at `report.py:207-210`. `classify.py:966-971` computes `bound_reached` and `visible = total - historical`, and the Sessions heading count (`report.py:410-411`) equals `summary.visible`.
- C8 SP-24 footnote: `report.py:36-39` equals DESIGN 7.5 line 629; probe shows it directly under the `## Sessions (n/total)` heading, also when there are zero rows.
- C9 Last line: probe `out[-20:]` is `...\nReport complete\n`; `render` joins with a blank line and appends one newline (`report.py:607`). No untrusted text can create a line (newlines folded), so a forged `Report complete` is not possible.
- C10 Dimensions and policy: `_SESSION_DIMENSIONS` (`report.py:59-70`) has the ten names in the #409 order from research `scope-04-409-layout.md:293`; they are used only in `_sessions` (`report.py:415-424`) and `_dimension_cells`; `to_json` has no dimension key (`policy` is the one the DESIGN 7.4 row set pins, `report.py:647`). The Policy cell is `frozen` or `unknown` (`report.py:400`); the only `not frozen` text in the package is the comment on that line (grep).
- C11 No recommendation text: grep of `report.py` for stop/retry/release/merge/remov/delete/should/recommend/consider returns only the `Removable` column heading and the `removable` cells and JSON keys that DESIGN 7.4/7.5 require; `removable()` returns only `no` or `could not determine` and `safe_to_close()` never returns `yes` (`classify.py:476-525`); every `NEXT_INSPECTION` value begins with `read` (`report.py:44-56`) and the keys equal the nine `Rule(...)` names (`classify.py:367-375`). Classify evidence strings quoting a contract ("STOP code", `classify.py:269`) describe, not advise. No command, action control or `.dev/tasks/` delete advice appears in any output I rendered. Residual: F-6.
- C12 Waiting (a) sort: ordering logic is right (oldest first, ties by ID, unknown group last; probe order `d1 (2h 0m), d0, d2`), but the age source is incomplete: F-1.
- C13 Waiting (b): frozen rows first, then the Ready Tasks sub-heading and count line, no question text (probe). Residual: F-2.
- C14 Sessions columns/labels: header row = `ID` + ten dimensions + `Class`, `Rule`, `Evidence`, `Safe to close (terminal / worktree)`, `Notes`, `Next inspection` (probe), matching DESIGN 7.5 line 643 and the OQ-4 decision text. Waiting (a) table header equals DESIGN 7.5 line 620 exactly.
- C15 GQ-35 and GQ-63: OQ-4 (`OQ-4-GQ-35-409-pin-decision.md:40-43`) chooses to pin `495eb96d` and keep DESIGN 7.5 ordering and labels unchanged; the layout above is the 7.5 layout with no change. OQ-6 (`OQ-6-GQ-63-done-next-decision.md:12`, `:33`) says the chat exception affects only the sweep skill's chat reply and "the Python-generated report format is unaffected". `report.py` contains no DONE / NEXT table or chat-summary text (grep for `DONE|NEXT` finds only the `NEXT_INSPECTION` map). OQ-5 (6h) is shown as `window 6h` by `_window_text`; the 6h default itself belongs to `commands.py`, which does not exist yet (item 9.1).
- C16 Purity: imports are `re`, `unicodedata` and `.models` only (`report.py:11-21`); no `os`, `time`, `subprocess`, `datetime.now`, file open or `write_report`; the wait-time parser uses `now.fromisoformat` on the context's own datetime, so no `datetime` import is needed.
- C17 JSON v1 (secondary): probe key set equals the 12 top-level keys of DESIGN 7.4 (`collected` included); counts include zeros (`report.py:684`); two renders of one fixture are equal (probe `True`).
- C18 `Distinct affected sessions`: printed as a set union of row ids (probe: 6 for the Shift Brief over 6 distinct rows); string equals DESIGN 7.5 line 645. Reading note: F-8.
- C19 `.gitignore`: `.gitignore:255-256` hold the comment and `.dev/sweeps/`, equal to DESIGN section 10 (`orchestrator-mode.md:736`); `gitignore-check.md` records `.dev/sweeps/x.md` ignored (exit 0), `.dev/tasks/` not ignored (exit 1), two insertions only.
- C20 Phase 8 validation: `step-1.4-pytest.txt`, `step-1.4a-pytest.txt` and `phase8-validation.md` each show 4 passed (all in `test_readonly.py`), `ruff check` and `ruff format --check` exit 0. There is no `tests/sweep/test_report.py` yet (planned in DESIGN section 11), so none of the strings above is pinned by a test at this gate; every statement in this report rests on my probes and reading, not on the project's tests.
- C21 Shift Brief, Retained problems, Source coverage content vs SPEC section 9: Retained problems lists interrupted archives, conflict packages, shared active packages, WC-13 rows and the show-cap line (`report.py:353-383`); `remote hosts` source row exists (`probes.py:1209`) and prints in Source coverage; the Scope line always carries the remote-hosts lower-bound text (`report.py:197`).
- C22 `NEXT_INSPECTION` coverage: keys `blocked_contract`, `orca_exit_proof`, `fenced`, `waiting_signal`, `working`, `finished`, `idle`, `person_active`, `fallback` equal the nine rule names; `_force_unknown` rows carry rule `fallback` (`classify.py:385`) so the map never misses.

## Checks

| Check | Result |
|---|---|
| C1 Heading order = DESIGN 7.5, 12 functions | PASS |
| C2 Header block and conditional lines | PASS |
| C3 Empty-section string | PASS |
| C4 200-character cell cut (JSON uncut) | PASS |
| C5 Sanitize rules (FR-016, GQ-107) | PASS (MINOR F-3, F-4) |
| C6 Version line for CHECKED_ORCA_VERSION | PASS (MINOR F-5) |
| C7 bound_reached, page and worktree lines; Sessions count equals summary.visible | PASS |
| C8 SP-24 footnote | PASS |
| C9 `Report complete` last line | PASS |
| C10 Ten dimensions only in the Sessions table; policy never `not frozen` | PASS |
| C11 No stop / retry / release / merge / removal recommendation | PASS (MINOR F-6) |
| C12 Waiting (a) oldest-first sort and age source | FAIL (F-1) |
| C13 Waiting (b) layout, no question text | PASS (MINOR F-2) |
| C14 Sessions columns and labels | PASS |
| C15 Layout follows GQ-35; GQ-63 limited to chat reply; GQ-61 window text | PASS |
| C16 report.py purity (imports, clock, files) | PASS |
| C17 JSON v1 key set and determinism | PASS |
| C18 `Distinct affected sessions` rule | PASS (MINOR F-8) |
| C19 `.gitignore` lines and check record | PASS |
| C20 Phase 8 validation records | PASS (no report test exists yet; noted) |
| C21 Shift Brief, Retained problems, Source coverage content | PASS |
| C22 `NEXT_INSPECTION` keys equal rule names | PASS |

## Summary

- Checks passed: 21 / 22. Checks failed: 1 (C12).
- BLOCKING: 0. MAJOR: 1 (F-1). MINOR: 7 (F-2 to F-8), recorded as notes; they do not fail the gate and are not re-checked in later rounds.
- Not applicable lens notes: no BUILD_REQUEST.GOAL text was in the prompt; the drift axis was not used and this report does not use the Axis column.

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict block was in the prompt, so no rf-qa PASS was relied on; every check was done standalone.

**(b) Independent semantic checks:**
- Rendered output vs DESIGN 7.5: `uv run --frozen --no-sync python -B` probe over a hand-built `SweepResult` (empty and populated) compared heading order, header lines, bracket lines, tables, SP-24 line and the final line against `orchestrator-mode.md:601-647`.
- Sanitize and cell: second probe with 14 hostile strings plus length-boundary cases, compared against SPEC FR-016 (`merged-requirements.md:110`).
- Age source: compared `report.py:129-138` and `models.py:78-86` with SPEC line 238, then grep-confirmed DESIGN has no SP-15 entry; this is the defect behind F-1 and no structural check would have found it.
- Words scan: grep of `report.py` and `classify.py` for recommendation vocabulary, plus a read of `removable()` and `safe_to_close()` to confirm they cannot return `yes`.

**Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Caveat: 100% is the share of my 22 checks I ran, not a claim that the report is defect-free; the open item 6 `agentWait` keys and live Orca shapes could not be checked here.
**Tool engagement:** Read: 27 | Grep: about 30 | Glob: 1 | Bash: 7 (two scratch probes, five read-only listings and greps). Tavily/web research: none performed.

Verdict: FAIL
Blocking count: 1
