# QA Report - Research Depth

**Topic:** issue #339 Phase 1 (orchestrator mode) research for MDTM task build
**Date:** 2026-11-08
**Phase:** research-depth (lens: research-depth)
**Fix cycle:** N/A
**Fix authorization:** false
**Assigned files:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-design-fixes-r3.md, 05-test-verification.md, 06-template-examples.md

---

## Progress log

(Findings are appended as each file is read.)

### 04-design-fixes-r3.md (232 lines, read in 2 chunks)

Depth: high. It explains behaviour, not just names. It traces the Orca data path from the
`worker-show` CLI handler to the runtime handler, the `hG` projection and the
`dispatch_contexts` insert paths, and from that derives why two rows on one pane are normally
sequential and where overlap can still occur. Edge cases (seconds cut, inclusive bounds, a
terminal row with no end time, row order, shared terminal handle, note order) each get a
fixture. UNVERIFIED items are listed per finding, which is honest.

Spot checks against source (sed/grep on the current design, Read on review 3):
- Line-drift table: lines 60, 398, 455, 457, 468, 494, 495, 497, 504, 505, 739, 764, 815, 853,
  885, 990, 991, 1011 all hold the content 04 says. Verified.
- The quoted replacement anchors in edit R3-B1 #4 match line 494 byte for byte. Verified.
- R3-B2 edit #1 anchor ("...because a person rerun inside the window cannot be told apart.")
  is the last sentence of line 494, so it survives R3-B1 #4. Order works.
- R3-B3 edit #1 anchor "the four incomplete cases" is in line 739. Verified.
- Model fields the R3-B3 rule reads (`orca_available`, `truncated`, `sources` with
  `unscanned`, `total_is_lower_bound`, `WORKER_LIST_PAGE = 100`) exist at design lines 454,
  465, 543, 566, 584. Verified.
- Review 3 exact fixes (lines 92-123) and minor notes m2, m3, m4, m5, m11 are all carried.

Finding D-1 (IMPORTANT, blocking). R3-B1 has no numbered edit for design section 11. Review 3
line 98 requires "Section 11: add a reader case `read_transcript_tail` sets `first_record_ts`".
04 section 2.3 lists 6 reader/parser fixtures for `test_probes_allowlist.py` (row 738) and 4
window fixtures for `test_classify.py` (row 739), but section 2.2 edits 1 to 9 never insert
those names into rows 738 or 739. R3-B2 has such an edit (3.3 #2); R3-B1 does not. Effects:
(a) a task builder applying 2.2 verbatim leaves section 11 unchanged while the cycle 3 log row
(edit #9) claims "reader, parser and window fixtures (11)"; (b) the R3-B1 QA gate in 04
section 5 greps `first_record_ts` in section 11 and would FAIL. Fix: add edit 2.2 #10 with the
exact text to append to row 738 (the 6 reader and parser fixture names) and to row 739 after
"a row with no observable start time never joins by path B;" (the 4 window fixture names, with
the m5 note `Dispatch time window not observable`), ordered before R3-B2 3.3 #2, which anchors
on the same phrase.

Finding D-2 (MINOR). Edit R3-B1 #1 says "Replace the parenthesis at the end of the row", but
its replacement starts with "plus `dispatch: str`", so it really replaces everything after
"SPEC list (line 231) ". Edits #1 and #2 also write `str | None` and `datetime | None` with a
bare pipe inside a Markdown table row; the existing rows escape it as `\|` (lines 455, 457).
Applied literally, the bare pipe splits the cell. Restate the anchor and escape the pipes.

Finding D-3 (MINOR). R3-B3 edit #2 introduces a per-Run source row name `orca worker-list
<run>` that section 7.4 does not define. 04 says so and asks for gate approval; the task item
must carry that approval step explicitly.

### 01-file-inventory.md (354 lines, 3 chunks)

Depth: high for an inventory. Every new file has purpose, the exact signatures from design 7.1,
its step and gate. Every existing file has a verified line anchor plus the exact edit text.
It flags real gaps (1.4a test before conftest and collect, CHANGELOG heading form, R2 anchor
shift after R1). Anchors re-checked in one batch script: `main.py:559-564`,
`WORKER-CONTRACT.md:23` and `:154-158`, `test_worker_contract.py:245-254`, `:545-546`, `:865`,
`HOW-WE-WORK.md:333`, `:403-404`, `test_how_we_work_routing_table.py:27-40`,
`test_routing_refresh.py:33`, `:647-648`, `.gitignore:252-257`, `CHANGELOG.md:5-9`. All hold.

Finding X-1 (IMPORTANT, blocking; contradiction 01 vs 03). 01 C11 and its "edit counts per
existing file" line give `test_worker_contract.py` 4 edits and say nothing about
`RULE_PHRASES["never-as-worker"]`. 03 IP-2 shows a fifth required edit: lines 86-92 pin the old
never-as-worker text word for word (verified: line 89 is the literal
"`/sc:agent`, ... `/sc:spawn` and `/sc:swarm-wizard`, "), so the line-23 change breaks
`test_contract_states_rule[never-as-worker]` unless line 89 changes in the same step. A builder
that uses 01's checklist-ready table (section D) will write a step 1.19 that fails. Fix: add
the line 89 edit to 01 C11 and set the count to 5, or state in 01 that 03 IP-2 supersedes C11.

Finding G-1 (IMPORTANT, blocking). The "ten #409 dimensions" of `SessionRow` are left open.
01 lines 45 and 354 defer them to "researcher 3/4 scope"; neither 03 nor 04 covers them, so the
hand-off dropped. Design line 459 and SPEC line 235 only say "the ten #409 dimensions", and the
report's Sessions table (design line 634) prints them, so the `models.py` (1.2) and
`report.py` (1.5) items cannot be written without re-reading sources or inventing names. They
are findable: the prior research report names them at
`.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md:277`
(lifecycle, phase, health, approval, freshness, result, admission, evidence, policy,
tests/review), each a closed value set defaulting to `unknown` (SPEC line 235). Fix: record the
ten names, their value sets (from `PKG/data-dictionary.md` as that report cites) and the
`unknown` default in 01 B2. The `OrcaObservation` SPEC field list (SPEC line 231) is one line;
copy it into 01 B2 too.

Finding M-1 (MINOR). `ClassifiedRow` has no field list in the design (line 466). 01 flags it as
a builder choice; the task item should name its fields explicitly so tests and `to_json` agree.

### 02-patterns-conventions.md (169 lines, 2 chunks)

Depth: high. Patterns are copyable: the exact `noqa` comment, the lazy `__getattr__` body
(verified `recommend/__init__.py:12-20`), click option and error style, seam mocking by module
attribute, the AST guard template, and a careful comparison of the repo's atomic-write helpers
against design 3.2 (verified design lines 99-117 and `sprint/recovery.py:412-434`). It explains
why reflect's eager `__init__` is the wrong model and why `os.replace` helpers do not fit.

Finding M-2 (MINOR, contradiction resolved elsewhere). 02 section 9 names the test location
`tests/cli/sweep/`; the design, 01 and 05 use `tests/sweep/`. 02 marks its own value as an
inference and defers to researcher 5, and 05 section 3 settles `tests/sweep/` with an
`__init__.py`. The builder should follow 05.

Finding M-3 (MINOR). The `Bash(...:*)` versus `Bash(... *)` allowlist form is left as an open
decision. The design test asserts the literal, so the task should keep the design literal unless
the owner changes both.

### 03-integration-points.md (120 lines, 1 chunk)

Depth: high, the best file for the "how is a routing edit caught" question. For each of R1 to R8
it names the test, what it asserts (set equality, live command reference, byte parity, set
difference over shipped commands) and the ordering this forces (R5 is triggered by creating
`sweep.md`, not by the guide). It found the fifth pin the design missed (verified, see X-1), the
AC-0.9 write-verb audit that will scan the new command and skill, and that `make sync-dev` does
not copy `core/`. No blocking finding in this file on its own.

### 05-test-verification.md (157 lines, 2 chunks)

Depth: high. It explains failure modes, not only names: the basename collision that makes
`tests/sweep/__init__.py` mandatory (verified: `tests/cli/__init__.py` does not exist), the
plugin auto-marker that adds `integration` from the absolute path (so the guard must read the
function's own `pytestmark`), the `from subprocess import run` hole in the guard, CI running
under xdist, and that local venv has no `pytest-xdist`. Each test file maps to a precedent
`file:line` and an exact `uv run pytest` command. `integration` marker verified at
`pyproject.toml:119`.

Finding M-4 (MINOR). 05 section 6 calls the test rename "optional"; the design (line 679) and 03
require it. Follow the design.

### 06-template-examples.md (164 lines, 2 chunks)

Depth: high. It resolves template-versus-builder conflicts with a stated rule (5-field items,
anti-orphaning final phase, per-gate `qa/<gate>/` prefixes), and gives a concrete human-gate
encoding with prior-art line citations. Verified the key danger it names: `task/SKILL.md:183-184`
says an unrecoverable item is ticked and execution continues, so an owner-decision item written
with the default clause would pass. It also flags the skill-mode POST reflect `--diff BASE..HEAD`
risk for uncommitted work.

Finding M-5 (MINOR). Neither 06 nor any other file traces the sweep run end to end in one place
(`commands.run` checks, `bind_run`, `collect` to `SweepInput`, `classify_all` to `SweepResult`,
`render` and `to_json`, `_publish`, stdout JSON, skill reads `report_path`). The pieces are
present across 01 B3 to B8 and 02 section 7, and the design holds the flow, so this does not
block item writing. Also 01 B6 deferred design 3.2 to researcher 4, who did not read it; 02
section 7 covers it instead.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Files explain how components work, not only what they are | PASS | 02 publish analysis, 03 test assertions per row, 04 Orca bundle trace, 05 collision and marker mechanics |
| 2 | Data flows traced end to end | PASS with note | Routing edit to test traced in 03 IP-4 (verified anchors); Orca time fields traced in 04 1.2; sweep run flow scattered (M-5) |
| 3 | Edge cases, error handling, failure modes documented | PASS | 04 fixtures for bounds, row order, missing fields; 05 guard holes; 06 human-gate failure path |
| 4 | Patterns specific enough to copy | PASS | 02 exact snippets and file:line precedents, verified `recommend/__init__.py:12-20`, `main.py:559-561` |
| 5 | One checklist item per file without re-reading sources | FAIL | X-1 (step 1.19 undercount), G-1 (#409 dimensions missing for 1.2 and 1.5) |
| 6 | 04 edits and fixtures concrete enough to apply verbatim as first three items | FAIL | D-1 (R3-B1 has no section 11 edit; its own gate would fail); D-2 minor formatting |
| 7 | Cross-file consistency within the assigned set | FAIL | X-1 (01 vs 03); M-2 (02 vs 05, resolved) |

## Summary

- Checks passed: 4 / 7
- Checks failed: 3
- Critical issues: 0
- Important issues: 3 (D-1, X-1, G-1)
- Minor issues: 7 (D-2, D-3, M-1 to M-5)
- Issues fixed in-place: 0 (fix_authorization false)

Overall the research is deep, not superficial. Each file explains mechanisms and cites
verified anchors. The failure comes from three specific gaps, two of them dropped hand-offs
between researchers, and all three are cheap to fix.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| D-1 | IMPORTANT | 04 section 2.2 | R3-B1 edits never add the 2.3 fixture names to design section 11 rows 738 and 739, though review 3 line 98 asks for it, edit #9 claims it, and the 04 section 5 gate greps for it | Add edit 2.2 #10 with exact text for rows 738 and 739, ordered before R3-B2 3.3 #2 |
| X-1 | IMPORTANT | 01 C11 and section D vs 03 IP-2 | 01 lists 4 edits to `test_worker_contract.py`; the line 89 `RULE_PHRASES["never-as-worker"]` edit is also required | Add the line 89 edit to 01 C11, count 5 |
| G-1 | IMPORTANT | 01 B2 (lines 45, 354) | Ten #409 `SessionRow` dimensions and the SPEC `OrcaObservation` list not resolved by any researcher | Copy names from the prior research report line 277 and SPEC lines 231, 235 into 01 B2 |
| D-2 | MINOR | 04 2.2 edits #1, #2 | "Replace the parenthesis" anchor is wrong; bare `|` inside a table cell | Restate anchor; escape as `\|` |
| D-3 | MINOR | 04 4.2 edit #2 | New source name `orca worker-list <run>` not in design 7.4 | Task item must carry the explicit approval step |
| M-1 | MINOR | 01 B2 | `ClassifiedRow` fields undefined | Name them in the task item |
| M-2 | MINOR | 02 section 9 | `tests/cli/sweep/` vs `tests/sweep/` | Follow 05 and the design |
| M-3 | MINOR | 02 8.1 | Allowlist form decision left open | Keep design literal |
| M-4 | MINOR | 05 section 6 | Rename called optional | Follow design line 679 |
| M-5 | MINOR | all | No single end-to-end sweep run trace | Optional summary in the task's Execution Context |

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied; no rf-qa PASS items were relied on.

**(b) Independent semantic checks:**
- 04 line-drift table: 18 design lines printed with sed and compared with 04's stated content.
- 04 replacement anchors: full text of design lines 494, 497, 739 printed and matched against the quoted "replace" strings.
- 04 against review 3: Read review 3 lines 83-142 to compare each exact fix with 04's edits; this is how D-1 was found.
- 03 fifth-pin claim: `test_worker_contract.py:86-92` printed; the old literal is there.
- 01 and 02 anchors: 13-command batch script (BATCH_OK, failures 0).
- G-1: grepped design, SPEC and the prior research report to find where the ten dimensions are named.
- 05 collision claim: `tests/cli/__init__.py` absent. 06 human-gate claim: `task/SKILL.md:183-184` read.

1. Claims verified against source: about 45.
2. Files read: the six research files, research-notes.md, `docs/designs/orchestrator-mode.md`, `orchestrator-mode-review-3.md`, `merged-requirements.md` lines 231 and 235, `main.py`, `WORKER-CONTRACT.md`, `test_worker_contract.py`, `HOW-WE-WORK.md`, `test_how_we_work_routing_table.py`, `test_routing_refresh.py`, `.gitignore`, `CHANGELOG.md`, `recommend/__init__.py`, `pyproject.toml`, `sprint/recovery.py`, `task/SKILL.md`, the prior RESEARCH-REPORT.
3. Issues were found, so the zero-issue question does not apply.
4. No web research was done.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 12 | Grep: 0 | Glob: 0 | Bash: 7 (one batch script of 13 reads; the other Bash calls were single sed/grep reads)

[PARTITION NOTE: cross-file checks covered only the six assigned files.]

## Recommendations

- Fix D-1, X-1 and G-1 in the research files (or carry them as explicit corrections in the
  BUILD_REQUEST) before task building. Then the first three task items can apply 04 verbatim.

## QA Complete

VERDICT: FAIL
