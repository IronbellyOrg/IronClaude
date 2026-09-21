# Research 07 — Gap-fill: R-19 Test Harness Design (round 1)

**Task:** TASK-RF-troubleshoot-generalize-20260919-015257
**Topic:** Builder-ready design for the LLM-free Python harness that R-19 implies but v2 never designs (`03-spec-extraction.md` I-23/I-24; `04-test-verification.md` §3 "Architecture forced by No LLM in CI")
**Status:** Complete
**Researcher:** gap-fill agent (read-only on repo; writes only this file)
**Date:** 2026-09-19

**Inputs read:** `04-test-verification.md` (all), `03-spec-extraction.md` §R-14 (:618-660), §R-19 (:803-875), §3 rows I-8/I-9/I-10/I-11/I-22/I-23/I-24, `merged-report-v2.md` (`v2:`) R-01..R-14, R-16, R-19 (:208-471, :506-512, :543-592), `refs/calibrator-eval-cases.md` (81 lines), `agents/confidence-calibrator.md:47-63`, `refs/escalation-rubric.md:20`, `pyproject.toml` `[tool.pytest.ini_options]` + `[tool.ruff]`, the three Coder worktree artifact sets (trigger lines re-verified 2026-09-19, quoted in §5).

## 0. Authority and the 06 contradiction

- **Authoritative for test names, fixture layout, counts:** `v2:543-592` (R-19 T-table + layout) and `04-test-verification.md` §2-§3. This file follows them exactly.
- **Superseded:** `06-template-examples.md` §5 Phase 3 items 3.1-3.22 (`test_r19_<nn>_<name>.py` naming, `fixtures/{io,nonio}/`, `fixtures/regression-sysbox/`, "test 12 non-regression"). Those were a shorthand written before 04 landed. The builder must use the spec filenames in §3 below (e.g. `test_validator_assertions.py`, not `test_r19_01_validator.py`) and the layout `assertions/<ID>/{io,nonio}/…`, `regression/sysbox-20260918/…` (`v2:551-565`). 06's *phase shape* (one item per fixture group, one item per test file, L3 pytest/lint item, L5 verdict) still applies; only its 3.x names/paths are wrong.
- **Why the gate failed:** "No LLM in CI" (`v2:547`) + T13 "agent flag set == inline flag set" means something executable must produce a flag set from a fixture. Neither agent prose nor SKILL prose executes. The executable thing is the two modules designed in §1-§2. T13 parity then reduces to *markdown table ⇔ Python registry ⇔ fixture `expected_flags`* (04 §4 item 3) — stated in the T13 docstring so nobody looks for a second engine.

## 1. `tests/troubleshoot/_assertions.py` — module design

Stdlib only (`re`, `dataclasses`, `datetime`, `pathlib`). Underscore prefix ⇒ not collected (matches `backtest/_impl_guard.py` precedent, 04 §2). Imported as `from tests.troubleshoot._assertions import ...` (package `__init__.py` files exist, 04 §2).

### 1.1 Public API

```python
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---- registry ------------------------------------------------------------

@dataclass(frozen=True)
class Flag:
    id: str          # "A1" … "A10", "C1" … "C8", "C3b"
    flag: str        # token written to the report/Notes, verbatim from v2:468-469
    severity: str    # see §1.3 enum
    trigger: str     # ONE sentence, verbatim-derived from v2:468-469; T13 compares this

FLAGS: tuple[Flag, ...]                      # §1.2, 19 entries
FLAG_BY_ID: dict[str, Flag] = {f.id: f for f in FLAGS}
VALIDATOR_IDS = ("A1", ..., "A10")
CALIBRATOR_IDS = ("C1", "C2", "C3", "C3b", "C4", "C5", "C6", "C7", "C8")

# ---- inputs (mirror the R-14 agent input lists, v2:467) -------------------

@dataclass
class ValidatorInputs:
    report: str                              # REPORT.md(.draft) text
    calibration_texts: list[str] = field(default_factory=list)   # VAL calibration_paths
    diff_text: str = ""                      # VAL diff_path (None → "")
    artifact_mtimes: dict[str, datetime] = field(default_factory=dict)  # VAL artifact_mtimes
    producers_text: str = ""                 # VAL producers_path
    tasklist_text: str = ""                  # VAL tasklist_path
    locus_text: str = ""                     # I-11: execution-locus.md (VAL needs locus_path)
    observation_text: str = ""               # tier1-observation.md (A9 observed reference value)
    candidate_fixes_text: str = ""           # candidate-fixes.md (A5)
    card_texts: list[str] = field(default_factory=list)          # hypothesis cards (A5)
    files_present: tuple[str, ...] = ()      # output-dir listing (A8 job-*.log; VAL has Glob)

@dataclass
class CalibratorInputs:
    card: str
    calibrated: float | None = None          # the calibrator's own Stage-2 result (or fixture-declared)
    card_mtime: datetime | None = None       # CAL card_mtime
    locus_text: str = ""                     # CONTROL-PROOF lines (C3)  — I-11 for CAL
    bracket_text: str = ""                   # bracket.md (C6)
    behaviour_text: str = ""                 # behaviour-definitions.md (C8)
    tasklist_text: str = ""                  # diagnosability-tasklist.md (C4, C7 2x2 rows)

@dataclass
class CalibratorResult:
    flags: set[str]                          # flag tokens fired (e.g. {"unproven_exclusion:auth-denied"})
    ids: set[str]                            # assertion ids fired (e.g. {"C2"})
    dims: dict[str, float]                   # dimension overrides: {"Runtime check": 0.0, ...}
    cap: float | None                        # min of caps fired (0.5 / 0.3), None if none
    verdict: str | None                      # "ESCALATE" when C1 fired, else None

@dataclass
class ValidatorResult:
    flags: set[str]
    ids: set[str]
    status: str | None                       # "partial" | "blocked" | "FAIL" | None
    dropped_lines: list[str]                 # A3
    suspect_probes: list[str]                # A9
    headline_prefix: str | None              # "UNDETERMINED — CI verdict unobserved" (A8)

# ---- evaluators ----------------------------------------------------------

def evaluate_validator(inp: ValidatorInputs) -> ValidatorResult: ...
def evaluate_calibrator(inp: CalibratorInputs) -> CalibratorResult: ...

# ---- fixture loader (used by T1, T2, T11, T13, T15) ----------------------

@dataclass
class Fixture:
    path: Path
    meta: dict[str, object]                  # frontmatter: assertion, domain, polarity, expected_flags, artifact_mtime, files_present
    files: dict[str, str]                    # "REPORT.md" -> text, from `--- file: <name> ---` blocks

def load_fixture(path: Path) -> Fixture: ...
def validator_inputs(fx: Fixture) -> ValidatorInputs: ...   # role mapping §4.1
def calibrator_inputs(fx: Fixture) -> CalibratorInputs: ...
def fired_ids(fx: Fixture) -> set[str]:      # runs the evaluator the fixture's `assertion` prefix selects
    ...
```

Design choices (ponytail): dataclasses instead of 10-positional-arg functions because T13/T15 need to build inputs from a fixture dict by role; `ids` and `flags` are both returned because the spec names flags (`deduced_headline`) but T-table rows name ids (`{A1,A3,…}`); `fired_ids` is the one-call form every parametrized test uses. No plugin, no class hierarchy, no YAML dependency — frontmatter is parsed with `re` (keys are flat, lists are `[a, b]`).

Shared helpers (private, one-liners):

```python
_ISO = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_TS_LINE = re.compile(r"(?im)^.*\b(Timestamp|Date|pushed_at)\b.*$")
_MIDNIGHT = re.compile(r"T00:00:00Z")
ENUM_TOKEN = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")   # backticked hyphenated word, no `/ . _ =`
_HEADLINE_SECTIONS = ("Summary", "Diagnosis")
CONTRACT_ENUM = {"pass", "blocked", "advisory", "not_applicable", "blocked-on-authorization"}
FIVE_MIN = timedelta(minutes=5)

def _section(text, name) -> str:      # body under `## <name>` up to next `## `
def _headline(report) -> str:         # frontmatter `root_cause_summary`, any `**Root cause**`/`Root cause:` line, `## Summary` body, first non-empty line of `## Diagnosis`
def _calibrated(texts) -> float|None: # max of r"(?i)\bcalibrated\b[^0-9\n]{0,40}(\d\.\d{1,2})" over texts
def _confidence(report) -> float|None:# r"(?im)^\**confidence\**:\s*\**(\d\.\d+)" (frontmatter or bold line)
def _ts_violations(text, mtime) -> list[str]:  # lines matching _TS_LINE whose ISO > mtime+5min or matching _MIDNIGHT; mtime None ⇒ midnight clause only
def _card_fm(card, key) -> str|None:  # r"(?im)^\**%s\**:\s*`?([\w-]+)`?" % key
```

`ENUM_TOKEN` deliberately excludes `_`, `/`, `.`, `=` so identifiers (`aidev_seed_now`), paths (`/proc/uptime`) and filenames (`tier1-observation.md`) are not "enum tokens". Verified against Fable-D3 `## Diagnosis` (:22-30): zero matches; GLM `REPORT-RUN2.md:17,21`: `clone-failed`. This is the A1/C1 "definite headline" proxy (see NOT_MECHANICAL notes).

### 1.2 `FLAGS` registry — id → trigger → flag → severity → predicate

Trigger sentences are the T13 parity text (§6): the markdown surfaces must carry them verbatim. Predicates are stdlib one-liners over the input texts. `NM` = NOT_MECHANICAL (judgment in the spec wording); the narrowest proxy follows and is what the predicate implements.

| id | trigger sentence (parity text) | flag | severity | predicate (one line; `r` = report, `c` = card, etc.) | NM? proxy |
|---|---|---|---|---|---|
| A1 | definite enum token in Summary/Diagnosis and (max calibrated < 0.50 or token in Grounding Gaps with unobserved/deduced/pending or token absent from every artifact and job-*.log) | `deduced_headline` | partial | `tok = ENUM_TOKEN.findall(_headline(r)); conf = _calibrated(cal) or _confidence(r) or 0.0; fire = tok and (conf < 0.5 or any(re.search(rf"`{t}`[^\n]*\b(unobserved\|deduced\|pending)\b", _section(r,"Grounding Gaps")) for t in tok) or any(all(t not in a for a in artifacts) for t in tok))` where `artifacts = calibration_texts + card_texts + [observation, candidate_fixes] + job logs in files` | **NM** ("definite"). Proxy: token = `ENUM_TOKEN` in headline lines; "probable" is NOT exempted (R-10 forbids the word). |
| A2 | diff touches a collector or invocation site and no falsifier sentence names a row | `instrumentation_without_falsifier` | partial | `fire = re.search(r"(?m)^\+.*\b(echo\|printf\|print\|log\|tee\|write\|>>)\b", diff) and not re.search(r"The report stays `partial` until \S+=\S+", r)` | **NM** ("collector/invocation site"). Proxy: any added (`+`) diff line containing an emit verb. |
| A3 | Timestamp/Date/pushed_at later than artifact mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop-line | `dropped = _ts_violations(r, mtimes.get("REPORT.md")) + [l for t in cal for l in _ts_violations(t, mtimes.get("calibration"))]; fire = bool(dropped)` | mechanical |
| A4 | pipeline_hardening_verdict not in {pass, blocked, advisory, not_applicable, blocked-on-authorization} | `verdict_not_in_contract` | partial | `m = re.search(r"(?i)(?:pipeline_hardening_verdict\|\bVerdict)\**:\s*\**([a-z_-]+)", _section(r,"Pipeline Hardening Closure") or r); fire = m and m.group(1).lower() not in CONTRACT_ENUM`; absent key with `pipeline_hardening_applicable: false` ⇒ pass (04 §3.4 Fable) | mechanical |
| A5 | candidate-fixes.md says consensus and adversarial_invoked is false and a card with evidence_class in {source_static, doc_static, none} makes a dynamic claim | `consensus_on_unobserved` | partial | `fire = re.search(r"\bconsensus\b", cf) and re.search(r"adversarial_invoked:\s*false\|Adversarial:\s*not invoked", r) and any(_card_fm(c,"evidence_class") in {"source_static","doc_static","none"} and _card_fm(c,"claim_class") in {"runtime_behavior","environment_dependent"} for c in cards + cal)` (calibration reports restate the classes — GLM `calibration.md:13,46`) | **NM** ("dynamic claim_class"). Proxy: `claim_class ∈ {runtime_behavior, environment_dependent}`; absent ⇒ default `runtime_behavior` (CAL step 2a). |
| A6 | Reference-context value is not a single literal (matches if, only, /, or comma) | `reference_value_not_literal` (I-10 name) | FAIL | `v = re.search(r"(?m)^Reference-context value:\s*(.+)$", r+obs); fire = v and (re.search(r"\b(if\|only)\b\|[/,]", v.group(1)) or v.group(1).strip() not in {"true","false","n/a"})` | mechanical |
| A7 | RUN-SITE is pending-producers at finalize while producers.md has at least one producer row | `run_site_unresolved` (I-10 name) | FAIL | `fire = re.search(r"(?m)^RUN-SITE:\s*pending-producers", locus) and producer_rows(producers) >= 1` (`producer_rows` from `_procedures`, counts `## Producers` table body rows only) | mechanical |
| A8 | OBSERVE-VIA is artifact-file and no job-*.log exists for the failing arm at finalize | `ci_verdict_unobserved` (name needed; status token `UNDETERMINED — CI verdict unobserved`) | blocked | `fire = re.search(r"(?m)^OBSERVE-VIA:\s*artifact-file", locus) and not any(re.fullmatch(r"job-[^/]+\.log", Path(f).name) for f in files_present)` | mechanical |
| A9 | Reference-context value differs from the value observed in the reference context | `probe_suspect` (name needed; effect: probe row `suspect`, outcome table skipped) | probe-suspect | `ref = Reference-context value; obsv = re.search(r"(?m)^(?:reference\|control)[^\n]*?\b%s=(true\|false)" % observable, obs); fire = ref in {"true","false"} and obsv and obsv.group(1) != ref` where `observable = re.search(r"(?m)^Observable that differs:\s*`?([\w-]+)", form)` | **NM** ("observed reference value" needs to know which arm is the reference). Proxy: an `observation_text` line that starts with `reference`/`control` and carries `<observable>=<v>`. |
| A10 | capability-verdict is blocked without an Emitter search block recording emitters-found: 0 and already-read-files: 0 | `capability_block_unproven` | partial | `fire = re.search(r"(?i)capability-verdict\**:\s*\**blocked\|blocked on capability", tl) and not (re.search(r"(?m)^## Emitter search", tl) and re.search(r"emitters-found:\s*0", tl) and re.search(r"already-read-files:\s*0", tl))` | mechanical (prose form `blocked on capability` included for Astra-A3, 04 §3.4) |
| C1 | headline enum token and calibrated < 0.50 | `headline_definite_low_confidence` | verdict=ESCALATE | `fire = ENUM_TOKEN.search(_headline(c)) and (calibrated if calibrated is not None else 0.0) < 0.5` (missing ⇒ 0.0, GB-05) | NM as A1; same proxy |
| C2 | card excludes an enum without a file:line for that enum's exit statement | `unproven_exclusion:<token>` | dim Runtime check := 0.0 | `excl = [l for l in c.splitlines() if re.search(r"(?i)\bexcluded\b", l)]; toks = {t for l in excl for t in ENUM_TOKEN.findall(l)}; bad = {t for t in toks if not re.search(rf"`{t}`[^\n]*exit statement[^\n]*\b[\w./-]+:\d+", c)}; fire = bool(bad)` — one flag per token | **NM** ("that enum's exit statement" is a code fact). Proxy: the structured exclusion line `Excluded: \`<token>\` — exit statement <file>:<line>` (R-02 step 2 output form). GLM-RUN2 hypothesis `:33` says "All excluded." with no `exit statement` phrase ⇒ fires. |
| C3 | control arm cited without CONTROL-PROOF: yes | `control_unproven` | dim Symptom coverage ≤ 0.5 | `fire = re.search(r"(?i)\bcontrol (run\|arm)s?\b", c) and not re.search(r"(?m)^CONTROL-PROOF:\s*yes:\s*\S+:\d+", locus)` | **NM** ("cited as a control"). Proxy: the phrase `control run`/`control arm`. GLM `:5` "two control runs" ⇒ fires; locus absent ⇒ fires. |
| C3b | runs-in is unknown | `locus_unknown` | dim Runtime check ≤ 0.5 | `fire = re.search(r"(?m)^runs-in[=:]\s*unknown\b", c)` | mechanical |
| C4 | instrumentation row without both falsifier values | `no_prereg_falsifier` | dim Fix directness ≤ 0.5 | `rows = table_rows(_section(c,"Proposed instrumentation") or _section(tl,"Discriminator rows")); fire = any(len(r) < 3 or not r[1].strip() or not r[2].strip() for r in rows)` (columns `row \| value-if-true \| value-if-false`) | mechanical given the R-06 column contract |
| C5 | Timestamp later than card_mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop-line | `fire = bool(_ts_violations(c, card_mtime))` | mechanical |
| C6 | numeric threshold or bracket asserted in the headline without a bracket= line in bracket.md | `bracket_unproven` (name needed; I-9: cap calibrated 0.3) | cap 0.3 | `fire = re.search(r"(?i)\b(above\|below\|over\|under\|more than\|less than\|at least\|at most\|>=?\|<=?)\s*\d+\|\b\d+\s+(layers\|messages\|bytes\|rows\|items\|retries\|connections\|files)\b", _headline(c)) and not re.search(r"(?m)^bracket=\[\d+,\d+\] width=\d+", bracket)` | **NM** ("asserts a threshold"). Proxy: comparative word + integer, or integer + count noun. |
| C7 | card names an environment property without citing a 2x2 row | `uncited` | cap 0.5 | `fire = (_card_fm(c,"claim_class") == "environment_dependent" or re.search(r"(?m)^environment-property:", c)) and not re.search(r"(?i)2[x×]2 row\|## Discriminator rows", c)` | **NM** ("names an environment property"). Proxy: `claim_class: environment_dependent` OR an explicit `environment-property:` card line (add to HCT). |
| C8 | behaviour-definition: row N missing or the row's Status is empty | `behaviour-cite: missing` | cap 0.5 | `m = re.search(r"behaviour-definition:\s*row\s*(\d+)", c); row = table_row_by_index(_section(bd,"")) ; fire = not m or row is None or not row[-1].strip()` (6-col table, Status = col 6) | mechanical |

I-9 resolution (C6 "evidence quality ≤0.3"): implement as a **calibrated-output cap of 0.3** (`CalibratorResult.cap`), not a dimension override — dimensions are 0.0/0.5/1.0 and no "evidence quality" dimension exists (`CAL:55`). Record in the builder's R-14 text as "calibrated ≤ 0.3".
I-8 resolution (T16 "cap 0.4" for `comparator=none`): that cap is an **orchestrator (Wave 5 / R-05 step 3) cap**, not a C-rule; it lives in `_procedures.differential_decision` (§2) and never in `FLAGS`. T13 parity therefore does not expect it in the agent tables.
I-10 resolution: A6/A7 get flag names `reference_value_not_literal` / `run_site_unresolved`; A8/A9 get `ci_verdict_unobserved` / `probe_suspect`; C6 gets `bracket_unproven`. These names must be written into the agent tables and SKILL fallback list by the R-14 build item, or T13 fails by design.
I-11 resolution: `locus_text` / `files_present` are harness inputs; the R-14 build item must add `locus_path` and `output_dir` to `VAL` inputs and `locus_path` to `CAL` inputs (C3 needs `CONTROL-PROOF`).

### 1.3 Severity enum and result mapping

`severity ∈ {partial, blocked, FAIL, drop-line, probe-suspect, dim, cap, verdict}`.
`ValidatorResult.status` = `"FAIL"` if any FAIL id fired, else `"blocked"` if A8, else `"partial"` if any partial id, else `None`. `dropped_lines` = A3 lines. `headline_prefix` = `"UNDETERMINED — CI verdict unobserved"` iff A8.
`CalibratorResult.dims` = `{"Runtime check": 0.0}` (C2) / `{"Runtime check": 0.5}` (C3b; min with C2) / `{"Symptom coverage": 0.5}` (C3) / `{"Fix directness": 0.5}` (C4); `cap` = `min` over {0.5 (C7, C8), 0.3 (C6)}; `verdict = "ESCALATE"` iff C1.

### 1.4 Fixture loader grammar (`load_fixture`)

```
---
assertion: A7            # id; "P-<name>" for procedure fixtures if any use this loader
domain: io               # io | nonio
polarity: neg            # pos | neg
expected_flags: [run_site_unresolved]     # [] for neg
artifact_mtime: 2026-09-18T18:36:00Z      # optional; applies to every file block
files_present: [REPORT.md, job-105704643590.log]   # optional; A8
calibrated: 0.42         # optional; CalibratorInputs.calibrated when no calibration.md block
---
--- file: REPORT.md ---
<text until next `--- file:` or EOF>
--- file: execution-locus.md ---
...
```

Role mapping by block name (`validator_inputs` / `calibrator_inputs`): `REPORT.md`→`report`; `calibration*.md`→`calibration_texts`; `*hypothesis*.md`/`card*.md`→`card_texts` / `card`; `diff.patch`→`diff_text`; `diagnosability-tasklist.md`→`tasklist_text`; `producers.md`; `execution-locus.md`→`locus_text`; `tier1-observation.md`→`observation_text`; `candidate-fixes.md`; `bracket.md`; `behaviour-definitions.md`; `job-*.log`→appended to `files_present` and to the A1 artifact set. Regex: `re.split(r"(?m)^--- file: (\S+) ---\n", body)`.

## 2. `tests/troubleshoot/_procedures.py` — procedure re-implementations for T3-T19

One module (not split): every function is ≤15 lines of `re`/`str` work, they share `table_rows`/`_section`, and a split would only add import lines. `_assertions.py` imports `producer_rows` and `table_rows` from here (A7, C4, C8) — dependency direction `_assertions → _procedures`, never the reverse. All functions are pure (text in, value out); the only writers take an explicit `tmp_path`-derived `Path`.

```python
# shared
def _section(text: str, heading: str) -> str            # body under `## <heading>`; "" if absent
def table_rows(md: str) -> list[list[str]]               # pipe-table body rows (skips header + |---| line), cells stripped
def table_row_by_index(md: str, n: int) -> list[str]|None # row whose first cell == str(n)
```

| # | function (signature) | algorithm (≤5 lines) | called by |
|---|---|---|---|
| P1 | `enumerate_producers(sources: dict[str, str], value: str, var: str) -> Producers` (`Producers` = dataclass `observation_kind, rows: list[dict], count_unknown: bool, grep_hits: int`) | 1. hits = `re.finditer(rf"(?m)^.*(?:{re.escape(value)}\|{re.escape(var)}=).*$", src)` per non-`.md` file (R-02 step 1). 2. `count_unknown = any(re.search(rf"{var}=\$\w+-", src))` (computed enum `rc=$prefix-unavailable`). 3. per hit inside a `function`/`def` block: list `return\|exit\|break` lines between header and hit (step 2). 4. rows = 7-cell dicts `line, statement, exit_statement, marker, walltime, observable, surviving` with `surviving="yes"` unless the hit is in a comment (`^\s*#`) or in text after `## Mechanism rows`. 5. `grep_hits = len(hits)`; return. | T3, T19 |
| P2 | `write_producers_md(p: Producers, out: Path) -> str` | header `observation-kind: <kind>` + `producer-count: unknown` when flagged; `## Producers` table with the 7 columns; if rows ≥1 and no `surviving=yes` ⇒ rewrite every row `surviving=re-opened` and set `producer-count: unknown` (AD-02); audit line `rows=<n> grep-hits=<n>`; write, return text. | T3, T19 |
| P3 | `producer_rows(producers_md: str) -> int` | `len(table_rows(_section(md, "Producers")))` — `## Mechanism rows` excluded by construction. | T3, A7 |
| P4 | `surviving_yes(producers_md: str) -> int` | count rows whose last cell == `surviving=yes` or `yes`. | T3, T19, T17 |
| P5 | `menu_equal(prompt: str, producers_md: str) -> bool` | `len(set(ENUM_TOKEN.findall(prompt))) == surviving_yes(md)` (R-02 step 6). | T19 |
| P6 | `primitive_grep(files: dict[str, str], producer_files: set[str], patterns: dict[str, str]) -> list[tuple[str,int,str]]` | for `(name, text)` with `name in producer_files` only; for each `kind, pat` in `patterns` (`read/parse` = `/proc/\|/sys/\|/dev/`): every line matching `pat` and not `re.search(r"/dev/(null\|stdout\|stderr\|tty\|zero)\|[0-9]*>\s*/dev/", line)`; emit `(name, lineno, kind)`; truncate to 8. | T4 |
| P7 | `overwrite_run_site(locus: str, file_line: str) -> str` | `re.sub(r"(?m)^RUN-SITE:\s*pending-producers", f"RUN-SITE: {file_line}", locus, count=1)`. | T4 |
| P8 | `parse_locus(card: str) -> dict[str, str]` | keys `PRINT-SITE, RUN-SITE, SAME-ENV, OBSERVE-VIA` from `^KEY:\s*(.*)$`; `CONTROL-PROOF` list; missing key ⇒ absent from dict. | T5, A7, A8 |
| P9 | `locus_complete(card: str) -> tuple[bool, list[str]]` | missing = the four keys not in `parse_locus`; blank value counts as missing (`unknown` legal); if ≥2 arm blocks (`^## Arm` or `^Arm:`), each passing arm needs `CONTROL-PROOF:`; return `(not missing, missing)`. | T5 |
| P10 | `derive_same_env(issue_text: str, grounding_text: str = "") -> str` | labels = `set(re.findall(r"(?im)\b(?:runs-on\|host\|job\|runner\|env(?:ironment)?\|machine\|pod\|worker)\b[:=\s]+([\w./-]+)", issue+grounding))` ∪ `re.findall(r"(?m)^\s*-\s*(\w[\w-]*)$", matrix block)`; `len>1 ⇒ "no"`, `==1 ⇒ "yes"`, else `"unknown"` (R-01 rule 3). | T5 |
| P11 | `requires_runs_in(card: str, same_env: str) -> bool` | `same_env != "yes" and not re.search(r"(?m)^runs-in[=:]\s*\S+", card)` ⇒ True = "card returned". | T5, T15-Astra |
| P12 | `verdict_from_log(log: str, marker: str = r"^RESULT:\s*(\w+)") -> str` | `m = re.findall(marker, log, re.M)`; `m[-1]` if m else `"unobservable"`; `"unobservable"` ⇒ treated as FAIL by caller (`verdict_is_fail(v) = v != "PASS"`). Never reads `conclusion:`. | T5b |
| P13 | `parse_discriminator_form(text: str) -> Form` (`Form`: `hyp_a, hyp_b, observable, probe, reference_value, table: dict[str, tuple[str,str]], falsifier`) | regex each labelled line (`v2:365-378`); table rows via `table_rows`; raise `ValueError` on a missing label. | T6, A6, A9 |
| P14 | `outcome_match(form: Form, observed: dict[str, str]) -> tuple[str, str] \| None` | `row = form.table[observed[form.observable]]`; return `("A","consistent")`… i.e. the single row; caller asserts exactly one matched row for the truth vector; `A/B verdict` = the hypothesis whose cell is `consistent` when the other is `refuted`. | T6 |
| P15 | `bracket_trigger(error_text: str, producers_md: str, passes_smaller: bool) -> str \| None` | `"limit-in-text"` if `re.search(r"\b(limit\|max(?:imum)?\|too many\|exceed\w*)\b[^\n]*\b\d+\|\b\d+\b[^\n]*\b(limit\|max(?:imum)?)\b", error+producers)`; `"passes-smaller"` if `passes_smaller`; else None. | T7 |
| P16 | `bracket(results: dict[int, str], n: int) -> dict` | vec sorted desc from `n`: `n, n-2, n-4, n-6` (+`n-8..n-12` if no pass, cap two rounds); monotone check: no `P` at a value above an `F`… i.e. `all(results[a]!="P" or results[b]!="F" for a>b)` fails ⇒ `{"status":"UNDETERMINED"}`; pass = highest `P`, fail = lowest `F` above it; return `{"bracket":[pass,fail],"width":fail-pass,"guard":pass}`; never touches `diagnosability-rounds.json`. | T7 |
| P17 | `cosmetic_counter(calls: list[str], output_dir: str = "out/") -> list[int]` | walk one call per line `"<Tool> <path>"`; hit if Tool in {Read, Glob} and path startswith output_dir and not exempt (`re.search(r"job-[^/]*\.log$\|\.stream\.jsonl$\|/artifacts/", path)`); `ls`/`Write`/Bash-persist never counted; Read/Bash on non-output path resets to 0; return the list of call indexes where count hits a multiple of 5 (`cosmetic_overrun=<count>`). | T8 |
| P18 | `counter_key(branch: str, venue_label: str) -> str` | `f"{branch}:{re.sub(r'\d+', '', venue_label)}"`. | T9 |
| P19 | `bump_rounds(counter_path: Path, key: str, tasklist_md: str) -> int` | load JSON (or `{}`); if `re.search(r"discriminator-required:\s*yes", tasklist)` ⇒ `d[key] = d.get(key,0)+1`; write; return `d[key]`; caller asserts round-3 tasklist still written and `status_for_round(3) == "blocked"`. | T9 |
| P20 | `hardstop_verdict(tasklist_md: str, read_log: list[str]) -> dict` | `n = int(re.search(r"emitters-found:\s*(\d+)"))`; `perm = re.search(r"re-run permitted:\s*(yes\|no\|unknown)")`; `n>=1 and perm=="no"` ⇒ `{"verdict":"blocked-on-authorization","status":"blocked","written":True}`; `n>=1` else ⇒ `{"status":"partial","task_rows_required":True}` (and A10 must fire on `capability-verdict: blocked`); `n==0 and eligible` (`eligible = [f for f in read_log if re.search(r"\.(log\|md\|txt\|jsonl)$", f) and not re.search(r"\.(sh\|py\|go\|ts\|js)$", f)]`) ⇒ `{"append_to": eligible[-1]}`; `n==0 and not eligible` ⇒ `{"capability_verdict":"blocked","status":"blocked","source_edit":False}`. | T10 |
| P21 | `timestamp_ok(ts: str, mtime: datetime) -> bool` | `not _MIDNIGHT.search(ts) and datetime.fromisoformat(ts.replace("Z","+00:00")) <= mtime + FIVE_MIN`. Shared with `_assertions._ts_violations`. | T12 |
| P22 | `differential_decision(table_md: str) -> dict` | rows `env \| exact \| ref` (2 envs expected, one `failing`, one `passing`); any cell `unobserved` or `<2` rows ⇒ `{"comparator":"none","headline":"UNDETERMINED — no comparator","cap":0.4}`; `failing.exact != failing.ref and passing.exact == passing.ref` ⇒ `{"cause_class":"substituted primitive"}`; else `{"cause_class":None}`. | T16 |
| P23 | `check_rows(tasklist_md: str, producers_md: str) -> dict` | pairs = rows under `## Discriminator rows` grouped by `<name>-(exact\|ref)`; `invalid` if any name lacks a half, or `producer_rows(p)>=1 and surviving_yes(p)>=1 and not pairs`; `control = any(r[0]=="control" or "control" in r[0])`; `truncated = header "probe-rows-truncated: <n>"`; `len(pairs) <= 8` else invalid unless truncated; `distinguishing = any(r[1]!=r[2])` else header `indistinguishable:` required; `verdict = "partial"` when input verdict ∈ {sufficient, unknown} and `discriminator-required: yes`. | T17 |
| P24 | `behaviour_row(card: str, log: list[str]) -> dict` | table row from `behaviour-definitions.md` = `# \| Primitive \| Asserted behaviour \| Defining artifact \| Fetch query \| Status`; `query_ok = set(query.split()) ⊆ set(asserted.split()) ∪ {"the","code","or","clause","that","implements","specifies"}` and no `format\|output\|appearance` word; `order_ok = log.index("write-row") < log.index("fetch")`; `Status startswith "recalled"` ⇒ `{"probe_row_appended": True}`; missing row ⇒ `{"c8_cap": 0.5}`. | T18 |
| P25 | `hc_rename_hits(paths: list[Path]) -> list[str]` | `grep -nE '\bH[0-5]\b'` in Python: lines matching `r"\bH[0-5]\b"` excluding the allow-list `calibrator-eval-cases.md:(49\|54)`, `escalation-rubric.md:35` (04 §1b option a); return `file:line` list, expected `[]`. | `test_hc_rename_guard.py` (03 R-17 coverage gap; one assert) |

`_procedures.py` self-check: the module ends with `if __name__ == "__main__": demo()` running one fixed vector per function (ponytail rule: one runnable check). It is not collected by pytest and is exercised by T3-T19 anyway; keep `demo()` ≤30 lines or drop it — the tests are the check.

## 3. Complete test file list (20 files, spec T-table order; names verbatim `v2:567-588`)

All files under `/config/workspace/IronClaude/tests/troubleshoot/`. `FIX = Path(__file__).parent / "fixtures"`. No pytest markers (04 §2). `ids=` on every parametrize so `-v` output names the case.

| T | filename | what it proves | fixtures used (`fixtures/…`) | pos/neg pairing | parametrization | harness function |
|---|---|---|---|---|---|---|
| T1 | `test_validator_assertions.py` | each A-id fires exactly its flag on `pos*`, nothing on `neg*`; status mapping (§1.3) | `assertions/A1..A10/{io,nonio}/{pos,neg}*.md` | every `pos*.md` ↔ `neg*.md` in the same dir | `sorted(FIX.glob("assertions/A*/*/*.md"))` → 40 base + 6 variants (§4.1) = 46 ids like `A7-io-neg-empty-producers` | `load_fixture`, `validator_inputs`, `evaluate_validator` |
| T2 | `test_calibrator_assertions.py` | C-id fires with flag; C1 ⇒ `verdict=="ESCALATE"`; C2 ⇒ `dims["Runtime check"]==0.0`; C7/C8 ⇒ `cap==0.5`; C6 ⇒ `cap==0.3` | `assertions/C1..C8,C3b/{io,nonio}/{pos,neg}*.md` | same | `FIX.glob("assertions/C*/*/*.md")` → 36 base + 6 variants = 42 | `evaluate_calibrator` |
| T3 | `test_producers_enumeration.py` | header always present; 7 columns; `rows == grep_hits`; computed enum ⇒ `producer-count: unknown`; zero-surviving ⇒ every row `surviving=re-opened`; `## Mechanism rows` not counted | `procedures/producers/{io.sh,nonio.py}` | io (computed enum ⇒ unknown) / nonio (literal ⇒ known) | `@pytest.mark.parametrize("src,value,var,expect_unknown", [("io.sh","runner-unavailable","rc",True),("nonio.py","DEAD_LETTER","status",False)])` | P1-P4 |
| T4 | `test_primitivegrep_targeting.py` | hits only from `sink.sh`; `decoy.sh` never hit; `/dev/null` + `2>/dev/null` excluded; ≤8; sentinel overwritten | `procedures/primitivegrep/{sink.sh,decoy.sh}` + inline producers.md text | in-file: positive lines vs excluded lines | none (one test, 4 asserts) | P6, P7 |
| T5 | `test_locus_card.py` | complete ⇒ ok; missing RUN-SITE ⇒ Wave-1 FAIL; SAME-ENV yes/no/unknown; card without `runs-in=` returned | `procedures/locus/{complete,missing-run-site,one-env,two-env,no-env}.md` | complete ↔ missing-run-site; one-env ↔ two-env ↔ no-env | `parametrize("name,expect", [("one-env","yes"),("two-env","no"),("no-env","unknown")])` | P8-P11 |
| T5b | `test_verdict_source.py` | last marker wins (`FAIL`); no marker ⇒ `unobservable`; conclusion-only never `PASS` | `procedures/verdict-source/{marker,no-marker,conclusion-only}.log` | marker ↔ no-marker | `parametrize("log,expect", [("marker.log","FAIL"),("no-marker.log","unobservable"),("conclusion-only.log","unobservable")])` | P12 |
| T6 | `test_discriminator_form.py` | both forms parse; exactly one row matches the truth vector; A/B verdict; A9 marks probe suspect on reference mismatch | `procedures/discriminator/{io,nonio}.md` | io ↔ nonio; within each, matching vs mismatching reference | `parametrize("form,vector,winner", [("io","false","A"),("nonio","true","A")])` | P13, P14, `evaluate_validator` (A9) |
| T7 | `test_threshold_bracket.py` | trigger both clauses; guard == highest pass, width 2; non-monotone ⇒ UNDETERMINED; counter file untouched | inline table (no file) | monotone `{80:F,78:F,76:P}` ↔ non-monotone `{80:F,78:P,76:F}` | `parametrize("results,n,expect", [...3 rows incl. N=82/85 absorbed row...])` | P15, P16 |
| T8 | `test_cosmetic_counter.py` | fires at 5 with `cosmetic_overrun=5`; re-fires at 10; exemptions; reset on source Read | `counters/cosmetic-log.txt` | one log: hits vs exempt lines | none | P17 |
| T9 | `test_counter_key.py` | key persists across slugs; only `=yes` increments; round 3 ⇒ still written + `blocked` | two tasklists written to `tmp_path` (text inline) | `discriminator-required: yes` ↔ `no` | none (uses `tmp_path`) | P18, P19 |
| T10 | `test_hardstop_verdicts.py` | four verdict outcomes | `procedures/tasklist/{authorized,refused,no-emitter-no-file,source-only-read}.md` | refused ↔ authorized; no-emitter-no-file ↔ source-only-read | `parametrize("name,expect_key", 4 rows)` | P20, `evaluate_validator` (A10 on authorized) |
| T11 | `test_headline_threshold.py` | `max(neg calibrated) < 0.5 <= min(pos calibrated)` over C1 fixtures; missing confidence ⇒ `UNDETERMINED` (0.0) | derived from `assertions/C1/**` + `assertions/A1/**` | pos ↔ neg calibrated values (0.42 / 0.72; boundary neg 0.50) | none | `load_fixture`, `_calibrated` |
| T12 | `test_timestamp_tolerance.py` | `+4m59s` ok, `+5m01s` fail, `T00:00:00Z` always fail | synthetic datetimes | ok ↔ fail | `parametrize("delta,ok", [(299,True),(301,False)])` + midnight case | P21 |
| T13 | `test_inline_fallback_parity.py` | §6 | all `assertions/**` + `regression/**` + the markdown surfaces | — | over every fixture file | `FLAGS`, `fired_ids`, `parse_flag_table` (§6) |
| T14 | `test_calibrator_eval_cases.py` (pinned by `refs/calibrator-eval-cases.md:81`) | §7 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` | expectation lines; formula grid | `parametrize` over the 9 expectation strings + 3 property grids | inline `rubric(dims, claim, verdict)` |
| T15 | `test_regression_sysbox.py` | §5 | `regression/sysbox-20260918/{GLM-RUN2,Fable-D3,Astra-A3}/**` + `MANIFEST` | — | `parametrize("param", ["GLM-RUN2","Fable-D3","Astra-A3"])` | `load_regression`, evaluators, P11 |
| T16 | `test_primitive_differential.py` | substituted primitive; `comparator=none` + cap 0.4 on unobserved cell or single env | `procedures/differential/table.md` (three tables under `## substituted`, `## all-unobserved`, `## single-env`) | substituted ↔ the two none cases | `parametrize("section,expect", 3 rows)` | P22 |
| T17 | `test_discriminator_rows.py` | pair completeness; distinguishing or `indistinguishable` header; control row; ≤8 + truncated header; verdict forced `partial` | `procedures/rows/{distinguishing,indistinguishable,exact-only,overflow}.md` | distinguishing ↔ exact-only; indistinguishable ↔ distinguishing; overflow ↔ distinguishing | `parametrize("name,expect", 4 rows)` | P23, P3, P4 |
| T18 | `test_behaviour_definition_row.py` | row before fetch; query from column 3 only; `recalled` ⇒ probe row appended; missing ⇒ C8 cap | `procedures/behaviour/{fetched,recalled,missing}.md` | fetched ↔ recalled ↔ missing | `parametrize("name,expect", 3 rows)` | P24, `evaluate_calibrator` (C8) |
| T19 | `test_menu_equality.py` | prompt enum count == `surviving=yes`; mismatch ⇒ FAIL | derived from T3 (`procedures/producers/io.sh` → producers.md in `tmp_path`) + two inline prompts | equal prompt ↔ prompt missing one token | `parametrize("prompt,ok", 2 rows)` | P1, P2, P4, P5 |
| extra | `test_hc_rename_guard.py` (03 R-17 gap, one assert; NOT in the spec's 20 — builder may fold into T14 file if a 21st file is undesired) | `\bH[0-5]\b` zero hits outside allow-list | skill + refs | — | none | P25 |

Existing-test updates (from 04 §1a/1b, not new files): `test_hardening_h1.py:46` `"satisfy h1"` → `"satisfy hc1"`; `test_hardening_verdict.py:51` tighten to the 5-token string; `test_hardening_verdict.py:27` keep `{blocked, advisory}` (R-16 should not extend the latch set) or update in the same commit.

## 4. Fixture tree and verbatim fixture content

### 4.1 Tree (spec layout `v2:551-565` + resolutions)

```
tests/troubleshoot/fixtures/
  assertions/
    A1/{io,nonio}/{pos,neg}.md
    A2/{io,nonio}/{pos,neg}.md
    A3/{io,nonio}/{pos,pos-late,neg}.md          # second pos: mtime+5m01s   (04 §3.1)
    A4/{io,nonio}/{pos,neg,neg-na}.md            # second neg: not_applicable (04 §3.1)
    A5/{io,nonio}/{pos,neg}.md
    A6/{io,nonio}/{pos,neg}.md
    A7/{io,nonio}/{pos,neg,neg-empty-producers}.md   # spec T1: two negs (v2:569)
    A8/{io,nonio}/{pos,neg}.md
    A9/{io,nonio}/{pos,neg}.md
    A10/{io,nonio}/{pos,neg}.md
    C1/{io,nonio}/{pos,neg,neg-boundary}.md      # neg-boundary: calibrated exactly 0.50 (T11)
    C2/{io,nonio}/{pos,neg}.md
    C3/{io,nonio}/{pos,neg}.md
    C3b/{io,nonio}/{pos,neg}.md                  # I-22: C3b gets its own dir
    C4/{io,nonio}/{pos,neg}.md
    C5/{io,nonio}/{pos,pos-late,neg}.md          # second pos: +5m01s
    C6/{io,nonio}/{pos,neg}.md
    C7/{io,nonio}/{pos,neg}.md
    C8/{io,nonio}/{pos,pos-empty-status,neg}.md  # second pos: row exists, Status empty
  procedures/
    producers/{io.sh,nonio.py}
    primitivegrep/{sink.sh,decoy.sh}             # decoy.sh added (04 §3.3 T4)
    locus/{complete,missing-run-site,one-env,two-env,no-env}.md
    verdict-source/{marker,no-marker,conclusion-only}.log
    discriminator/{io,nonio}.md
    rows/{distinguishing,indistinguishable,exact-only,overflow}.md
    differential/table.md
    behaviour/{fetched,recalled,missing}.md
    tasklist/{authorized,refused,no-emitter-no-file,source-only-read}.md
  counters/cosmetic-log.txt
  regression/sysbox-20260918/
    MANIFEST
    GLM-RUN2/{REPORT-RUN2.md,run2-tier2-root-cause-analyst-calibration.md,run2-tier2-root-cause-analyst-hypothesis.md,candidate-fixes.md}
    Fable-D3/{REPORT.md,candidate-fixes.md}
    Astra-A3/{diagnosability-tasklist.md,tier1-observation.md,REPORT.md}
```

**Variant-file rule (resolves "layout allows one neg"):** extra polarity files are siblings named `<polarity>-<reason>.md`; the loader's `polarity` is the frontmatter field, and the tests glob `*.md` per dir. This keeps the spec's `{pos,neg}.md` base names literally present in every dir (coverage rule `v2:590` satisfied by inspection) and avoids a `neg/` subdir that would break `assertions/<ID>/<domain>/<file>` three-level globs. Counts: A = 40 base + 6 variants (A3 pos-late ×2, A4 neg-na ×2, A7 neg-empty-producers ×2) → **46 T1 cases**; C = 36 base + 6 variants (C1 neg-boundary ×2, C5 pos-late ×2, C8 pos-empty-status ×2) → **42 T2 cases**.

**Shared frontmatter conventions:** `artifact_mtime: 2026-09-18T18:36:00Z` on every A/C fixture (so A3/C5 negs at `18:40:59Z` = +4m59s pass and `18:41:01Z` = +5m01s fail); io domain = CI shell script `startup.sh` / `/proc/uptime` / enum `clone-failed`; nonio domain = queue consumer `consumer.py` / `redelivered` / enum `dead-lettered` (R-07 worked example 2, `v2:383`). Fixture texts are minimal on purpose — each contains exactly the lines the predicate reads plus one line of harmless context so a false-positive regex would show up in the neg twin.

### 4.2 Validator fixtures A1-A10 (write verbatim)

Every file starts with the frontmatter block; `expected_flags` is the flag token from §1.2.

#### A1 — `deduced_headline`

`assertions/A1/io/pos.md`
```
---
assertion: A1
domain: io
polarity: pos
expected_flags: [deduced_headline]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.42
## Summary
Root cause: the recorded seed outcome is `clone-failed`, a fast network-level git failure.
## Diagnosis
The §8 assertion rejects any outcome other than `cloned`.
## Grounding Gaps
- `clone-failed` is deduced from source logic, not read from the artifact.
--- file: calibration.md ---
calibrated: 0.42
```

`assertions/A1/io/neg.md`
```
---
assertion: A1
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.72
## Summary
Root cause: the recorded seed outcome is `clone-failed`, read from the seed artifact.
## Diagnosis
The §8 assertion rejects any outcome other than `cloned`.
## Grounding Gaps
- none for the headline token.
--- file: calibration.md ---
calibrated: 0.72
--- file: job-105704643590.log ---
seed-outcome-observed=clone-failed
RESULT: FAIL
```

`assertions/A1/nonio/pos.md`
```
---
assertion: A1
domain: nonio
polarity: pos
expected_flags: [deduced_headline]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.42
## Summary
Root cause: the invoice message ends `dead-lettered` after the consumer crashes between send and ack.
## Diagnosis
The consumer acks after the side effect.
## Grounding Gaps
- `dead-lettered` is pending observation; the DLQ was not queried in this run.
--- file: calibration.md ---
calibrated: 0.42
```

`assertions/A1/nonio/neg.md`
```
---
assertion: A1
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.72
## Summary
Root cause: the invoice message ends `dead-lettered` after the consumer crashes between send and ack.
## Diagnosis
The consumer acks after the side effect.
## Grounding Gaps
- none for the headline token.
--- file: calibration.md ---
calibrated: 0.72
--- file: tier1-observation.md ---
SELECT state FROM consumed_log WHERE invoice_id=4711; -- dead-lettered
```

#### A2 — `instrumentation_without_falsifier`

`assertions/A2/io/pos.md`
```
---
assertion: A2
domain: io
polarity: pos
expected_flags: [instrumentation_without_falsifier]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Push the collector change and re-run the CI job.
--- file: diff.patch ---
--- a/test-startup-boot.sh
+++ b/test-startup-boot.sh
@@ -443,0 +444,1 @@
+echo "seed-diag-uptime-regex=${uptime_regex:-unobserved}" >> "$DIAG_OUT"
```

`assertions/A2/io/neg.md`
```
---
assertion: A2
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Push the collector change and re-run the CI job.
The report stays `partial` until uptime-regex=false.
--- file: diff.patch ---
--- a/test-startup-boot.sh
+++ b/test-startup-boot.sh
@@ -443,0 +444,1 @@
+echo "seed-diag-uptime-regex=${uptime_regex:-unobserved}" >> "$DIAG_OUT"
```

`assertions/A2/nonio/pos.md`
```
---
assertion: A2
domain: nonio
polarity: pos
expected_flags: [instrumentation_without_falsifier]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Deploy the consumer with the extra log line and wait for the next duplicate.
--- file: diff.patch ---
--- a/consumer.py
+++ b/consumer.py
@@ -41,0 +42,1 @@
+    log.info("redelivered=%s", getattr(msg, "redelivered", "unobserved"))
```

`assertions/A2/nonio/neg.md`
```
---
assertion: A2
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Deploy the consumer with the extra log line and wait for the next duplicate.
The report stays `partial` until redelivered=false.
--- file: diff.patch ---
--- a/consumer.py
+++ b/consumer.py
@@ -41,0 +42,1 @@
+    log.info("redelivered=%s", getattr(msg, "redelivered", "unobserved"))
```

#### A3 — `timestamp_invalid` (drop line)

`assertions/A3/io/pos.md`
```
---
assertion: A3
domain: io
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Date**: 2026-09-19T00:00:00Z
## Summary
The CI job log was fetched to job-105704643590.log.
```

`assertions/A3/io/pos-late.md`
```
---
assertion: A3
domain: io
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Date**: 2026-09-18T18:41:01Z
## Summary
The CI job log was fetched to job-105704643590.log.
```

`assertions/A3/io/neg.md`
```
---
assertion: A3
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Date**: 2026-09-18T18:40:59Z
## Summary
The CI job log was fetched to job-105704643590.log.
```

`assertions/A3/nonio/pos.md`
```
---
assertion: A3
domain: nonio
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Evidence
- pushed_at: 2026-09-19T00:00:00Z — broker admin API snapshot of queue `invoices`.
```

`assertions/A3/nonio/pos-late.md`
```
---
assertion: A3
domain: nonio
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Evidence
- Timestamp: 2026-09-18T18:41:01Z — broker admin API snapshot of queue `invoices`.
```

`assertions/A3/nonio/neg.md`
```
---
assertion: A3
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Evidence
- Timestamp: 2026-09-18T18:40:59Z — broker admin API snapshot of queue `invoices`.
```

#### A4 — `verdict_not_in_contract`

`assertions/A4/io/pos.md`
```
---
assertion: A4
domain: io
polarity: pos
expected_flags: [verdict_not_in_contract]
---
--- file: REPORT.md ---
pipeline_hardening_applicable: true
## Pipeline Hardening Closure
pipeline_hardening_verdict: blocked_pending_retry_run
```

`assertions/A4/io/neg.md`
```
---
assertion: A4
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
pipeline_hardening_applicable: true
## Pipeline Hardening Closure
pipeline_hardening_verdict: blocked-on-authorization
```

`assertions/A4/io/neg-na.md`
```
---
assertion: A4
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
pipeline_hardening_applicable: false
## Summary
No verdict key is rendered when hardening is not applicable.
```

`assertions/A4/nonio/pos.md`
```
---
assertion: A4
domain: nonio
polarity: pos
expected_flags: [verdict_not_in_contract]
---
--- file: REPORT.md ---
pipeline_hardening_applicable: true
## Pipeline Hardening Closure
**Verdict: needs_review** — consumer deploy pipeline has no runtime witness yet.
```

`assertions/A4/nonio/neg.md`
```
---
assertion: A4
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
pipeline_hardening_applicable: true
## Pipeline Hardening Closure
**Verdict: advisory** — closure relies on waived proof.
```

`assertions/A4/nonio/neg-na.md`
```
---
assertion: A4
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
pipeline_hardening_applicable: true
## Pipeline Hardening Closure
pipeline_hardening_verdict: not_applicable
```

#### A5 — `consensus_on_unobserved`

`assertions/A5/io/pos.md`
```
---
assertion: A5
domain: io
polarity: pos
expected_flags: [consensus_on_unobserved]
---
--- file: REPORT.md ---
## Audit
- Adversarial: not invoked — consensus
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Bulk-read /proc/uptime at all clock sites | rca, devops | **consensus** | 0.72 |
--- file: card-rca.md ---
claim_class: runtime_behavior
evidence_class: source_static
verdict_direction: AFFIRM
```

`assertions/A5/io/neg.md`
```
---
assertion: A5
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
## Audit
- Adversarial: not invoked — consensus
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Bulk-read /proc/uptime at all clock sites | rca, devops | **consensus** | 0.72 |
--- file: card-rca.md ---
claim_class: runtime_behavior
evidence_class: runtime_repro
verdict_direction: AFFIRM
```

`assertions/A5/nonio/pos.md`
```
---
assertion: A5
domain: nonio
polarity: pos
expected_flags: [consensus_on_unobserved]
---
--- file: REPORT.md ---
adversarial_invoked: false
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Ack before the side effect, make send idempotent | rca, backend | consensus | 0.70 |
--- file: card-rca.md ---
claim_class: environment_dependent
evidence_class: doc_static
verdict_direction: AFFIRM
```

`assertions/A5/nonio/neg.md`
```
---
assertion: A5
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
adversarial_invoked: true
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Ack before the side effect, make send idempotent | rca, backend | consensus | 0.70 |
--- file: card-rca.md ---
claim_class: environment_dependent
evidence_class: doc_static
verdict_direction: AFFIRM
```

#### A6 — `reference_value_not_literal` (FAIL)

`assertions/A6/io/pos.md`
```
---
assertion: A6
domain: io
polarity: pos
expected_flags: [reference_value_not_literal]
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true if seekable, false otherwise
```

`assertions/A6/io/neg.md`
```
---
assertion: A6
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true
```

`assertions/A6/nonio/pos.md`
```
---
assertion: A6
domain: nonio
polarity: pos
expected_flags: [reference_value_not_literal]
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false/true
```

`assertions/A6/nonio/neg.md`
```
---
assertion: A6
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false
```

#### A7 — `run_site_unresolved` (FAIL; two negs per spec)

`assertions/A7/io/pos.md`
```
---
assertion: A7
domain: io
polarity: pos
expected_flags: [run_site_unresolved]
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: pending-producers @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| startup.sh:583 | aidev_seed_now \|\| return 1 | return 1 | before | yes | started-line absent | surviving=yes |
```

`assertions/A7/io/neg.md`
```
---
assertion: A7
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: startup.sh:583 @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| startup.sh:583 | aidev_seed_now \|\| return 1 | return 1 | before | yes | started-line absent | surviving=yes |
```

`assertions/A7/io/neg-empty-producers.md`
```
---
assertion: A7
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: pending-producers @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
--- file: producers.md ---
observation-kind: categorical
producer-count: 0
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
```

`assertions/A7/nonio/pos.md`
```
---
assertion: A7
domain: nonio
polarity: pos
expected_flags: [run_site_unresolved]
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: consumer pod stdout, worker-pod-b
RUN-SITE: pending-producers @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: remote-command
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| consumer.py:41 | status = "DEAD_LETTER" | return | after | yes | dlq depth | surviving=yes |
```

`assertions/A7/nonio/neg.md`
```
---
assertion: A7
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: consumer pod stdout, worker-pod-b
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: remote-command
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| consumer.py:41 | status = "DEAD_LETTER" | return | after | yes | dlq depth | surviving=yes |
```

`assertions/A7/nonio/neg-empty-producers.md`
```
---
assertion: A7
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: consumer pod stdout, worker-pod-b
RUN-SITE: pending-producers @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: remote-command
--- file: producers.md ---
observation-kind: categorical
producer-count: 0
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
```

#### A8 — `ci_verdict_unobserved` (status blocked)

`assertions/A8/io/pos.md`
```
---
assertion: A8
domain: io
polarity: pos
expected_flags: [ci_verdict_unobserved]
files_present: [REPORT.md, execution-locus.md]
---
--- file: REPORT.md ---
## Diagnosis
The workflow-level conclusion was `success`.
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log
RUN-SITE: startup.sh:583 @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
```

`assertions/A8/io/neg.md`
```
---
assertion: A8
domain: io
polarity: neg
expected_flags: []
files_present: [REPORT.md, execution-locus.md, job-105704643590.log]
---
--- file: REPORT.md ---
## Diagnosis
The job log's last marker reads `RESULT: FAIL`.
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log
RUN-SITE: startup.sh:583 @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
```

`assertions/A8/nonio/pos.md`
```
---
assertion: A8
domain: nonio
polarity: pos
expected_flags: [ci_verdict_unobserved]
files_present: [REPORT.md, execution-locus.md]
---
--- file: REPORT.md ---
## Diagnosis
The nightly consumer smoke job was reported green by the scheduler.
--- file: execution-locus.md ---
PRINT-SITE: scheduler job log, job smoke-consumer
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: artifact-file
```

`assertions/A8/nonio/neg.md`
```
---
assertion: A8
domain: nonio
polarity: neg
expected_flags: []
files_present: [REPORT.md, execution-locus.md, job-7781.log]
---
--- file: REPORT.md ---
## Diagnosis
The job log's last marker reads `RESULT: FAIL`.
--- file: execution-locus.md ---
PRINT-SITE: scheduler job log, job smoke-consumer
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: artifact-file
```

#### A9 — `probe_suspect`

`assertions/A9/io/pos.md`
```
---
assertion: A9
domain: io
polarity: pos
expected_flags: [probe_suspect]
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true
--- file: tier1-observation.md ---
reference arm (dind-public): uptime-regex=false
failing arm (sysbox-public): uptime-regex=false
```

`assertions/A9/io/neg.md`
```
---
assertion: A9
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true
--- file: tier1-observation.md ---
reference arm (dind-public): uptime-regex=true
failing arm (sysbox-public): uptime-regex=false
```

`assertions/A9/nonio/pos.md`
```
---
assertion: A9
domain: nonio
polarity: pos
expected_flags: [probe_suspect]
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false
--- file: tier1-observation.md ---
control consumer (known-good, worker-pod-a): redelivered=true
failing consumer (worker-pod-b): redelivered=true
```

`assertions/A9/nonio/neg.md`
```
---
assertion: A9
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false
--- file: tier1-observation.md ---
control consumer (known-good, worker-pod-a): redelivered=false
failing consumer (worker-pod-b): redelivered=true
```

#### A10 — `capability_block_unproven`

`assertions/A10/io/pos.md`
```
---
assertion: A10
domain: io
polarity: pos
expected_flags: [capability_block_unproven]
---
--- file: REPORT.md ---
status: blocked
--- file: diagnosability-tasklist.md ---
**Round**: 1 of 3  **re-run permitted**: unknown  **capability-verdict**: blocked
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-regex | false | true |
```

`assertions/A10/io/neg.md`
```
---
assertion: A10
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: blocked
--- file: diagnosability-tasklist.md ---
**Round**: 1 of 3  **re-run permitted**: unknown  **capability-verdict**: blocked
## Emitter search
emitters-found: 0
already-read-files: 0
channels searched: startup.sh seed function, test-startup-boot.sh caller, job log, REPORT.md.draft
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-regex | false | true |
```

`assertions/A10/nonio/pos.md`
```
---
assertion: A10
domain: nonio
polarity: pos
expected_flags: [capability_block_unproven]
---
--- file: REPORT.md ---
status: blocked
--- file: diagnosability-tasklist.md ---
**Round**: 1 of 3  **re-run permitted**: no  **capability-verdict**: blocked
- Blocked on capability, not permission: no consumer log line exposes the redelivered flag.
```

`assertions/A10/nonio/neg.md`
```
---
assertion: A10
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: blocked
--- file: diagnosability-tasklist.md ---
**Round**: 1 of 3  **re-run permitted**: no  **capability-verdict**: blocked
## Emitter search
emitters-found: 0
already-read-files: 0
channels searched: consumer.py handle(), worker entrypoint, scheduler job log
```

### 4.3 Calibrator fixtures C1-C8 + C3b (write verbatim)

Each fixture's main block is `card.md` (hypothesis card). `calibrated:` in frontmatter feeds `CalibratorInputs.calibrated` when no `calibration.md` block exists. `card_mtime` = `artifact_mtime`.

#### C1 — `headline_definite_low_confidence` (verdict ESCALATE)

`assertions/C1/io/pos.md`
```
---
assertion: C1
domain: io
polarity: pos
expected_flags: [headline_definite_low_confidence]
calibrated: 0.42
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: source_static
## Claim
Root cause: the recorded outcome is `clone-failed`; the clone fails fast under the CI runtime.
```

`assertions/C1/io/neg.md`
```
---
assertion: C1
domain: io
polarity: neg
expected_flags: []
calibrated: 0.72
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: runtime_repro
## Claim
Root cause: the recorded outcome is `clone-failed`; the clone fails fast under the CI runtime.
```

`assertions/C1/io/neg-boundary.md`
```
---
assertion: C1
domain: io
polarity: neg
expected_flags: []
calibrated: 0.50
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: runtime_repro
## Claim
Root cause: the recorded outcome is `clone-failed`; the clone fails fast under the CI runtime.
```

`assertions/C1/nonio/pos.md`
```
---
assertion: C1
domain: nonio
polarity: pos
expected_flags: [headline_definite_low_confidence]
calibrated: 0.42
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: doc_static
## Claim
Root cause: the invoice message is `dead-lettered` after the third redelivery.
```

`assertions/C1/nonio/neg.md`
```
---
assertion: C1
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.72
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: log_evidence
## Claim
Root cause: the invoice message is `dead-lettered` after the third redelivery.
```

`assertions/C1/nonio/neg-boundary.md`
```
---
assertion: C1
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.50
---
--- file: card.md ---
claim_class: runtime_behavior
evidence_class: log_evidence
## Claim
Root cause: the invoice message is `dead-lettered` after the third redelivery.
```

#### C2 — `unproven_exclusion:<token>` (Runtime check := 0.0)

`assertions/C2/io/pos.md`
```
---
assertion: C2
domain: io
polarity: pos
expected_flags: ["unproven_exclusion:auth-denied"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `auth-denied` (unreachable for an anonymous public clone).
- startup.sh:583 is the first statement of the attempt.
```

`assertions/C2/io/neg.md`
```
---
assertion: C2
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `auth-denied` — exit statement startup.sh:663 (`return 1` after the askpass prompt).
- startup.sh:583 is the first statement of the attempt.
```

`assertions/C2/nonio/pos.md`
```
---
assertion: C2
domain: nonio
polarity: pos
expected_flags: ["unproven_exclusion:retry-exhausted"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `retry-exhausted` (the producer never retries on 5xx in this deployment).
- consumer.py:41 sets the terminal status.
```

`assertions/C2/nonio/neg.md`
```
---
assertion: C2
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `retry-exhausted` — exit statement producer.py:88 (`raise PublishError` before any retry loop).
- consumer.py:41 sets the terminal status.
```

#### C3 — `control_unproven` (Symptom coverage ≤ 0.5)

`assertions/C3/io/pos.md`
```
---
assertion: C3
domain: io
polarity: pos
expected_flags: [control_unproven]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The DinD control arm passed the same script, so the producer is proven passing there.
--- file: execution-locus.md ---
RUN-SITE: startup.sh:583 @ ci-runner
CONTROL-PROOF: no: startup.sh:753
```

`assertions/C3/io/neg.md`
```
---
assertion: C3
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The DinD control arm passed the same script, so the producer is proven passing there.
--- file: execution-locus.md ---
RUN-SITE: startup.sh:583 @ ci-runner
CONTROL-PROOF: yes: startup.sh:583
```

`assertions/C3/nonio/pos.md`
```
---
assertion: C3
domain: nonio
polarity: pos
expected_flags: [control_unproven]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The control run on worker-pod-a delivered every invoice exactly once with the same consumer build.
--- file: execution-locus.md ---
RUN-SITE: consumer.py:41 @ worker-pod-b
```

`assertions/C3/nonio/neg.md`
```
---
assertion: C3
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The control run on worker-pod-a delivered every invoice exactly once with the same consumer build.
--- file: execution-locus.md ---
RUN-SITE: consumer.py:41 @ worker-pod-b
CONTROL-PROOF: yes: consumer.py:41
```

#### C3b — `locus_unknown` (Runtime check ≤ 0.5)

`assertions/C3b/io/pos.md`
```
---
assertion: C3b
domain: io
polarity: pos
expected_flags: [locus_unknown]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
runs-in=unknown
## Claim
The clock read fails before the clone starts.
```

`assertions/C3b/io/neg.md`
```
---
assertion: C3b
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
runs-in=sysbox-runc-runner
## Claim
The clock read fails before the clone starts.
```

`assertions/C3b/nonio/pos.md`
```
---
assertion: C3b
domain: nonio
polarity: pos
expected_flags: [locus_unknown]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
runs-in=unknown
## Claim
The consumer acks after the side effect.
```

`assertions/C3b/nonio/neg.md`
```
---
assertion: C3b
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
runs-in=worker-pod-b
## Claim
The consumer acks after the side effect.
```

#### C4 — `no_prereg_falsifier` (Fix directness ≤ 0.5)

`assertions/C4/io/pos.md`
```
---
assertion: C4
domain: io
polarity: pos
expected_flags: [no_prereg_falsifier]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Proposed instrumentation
| row | value-if-true | value-if-false |
|---|---|---|
| dns-github | | |
```

`assertions/C4/io/neg.md`
```
---
assertion: C4
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Proposed instrumentation
| row | value-if-true | value-if-false |
|---|---|---|
| dns-github | true | false |
```

`assertions/C4/nonio/pos.md`
```
---
assertion: C4
domain: nonio
polarity: pos
expected_flags: [no_prereg_falsifier]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Proposed instrumentation
| row | value-if-true | value-if-false |
|---|---|---|
| redelivered | true | |
```

`assertions/C4/nonio/neg.md`
```
---
assertion: C4
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Proposed instrumentation
| row | value-if-true | value-if-false |
|---|---|---|
| redelivered | true | false |
```

#### C5 — `timestamp_invalid`

`assertions/C5/io/pos.md`
```
---
assertion: C5
domain: io
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
**Timestamp**: 2026-09-19T00:00:00Z
## Claim
The clock read fails before the clone starts.
```

`assertions/C5/io/pos-late.md`
```
---
assertion: C5
domain: io
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
**Timestamp**: 2026-09-18T18:35:01Z
## Claim
The clock read fails before the clone starts.
```

`assertions/C5/io/neg.md`
```
---
assertion: C5
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
**Timestamp**: 2026-09-18T18:34:59Z
## Claim
The clock read fails before the clone starts.
```

`assertions/C5/nonio/pos.md`
```
---
assertion: C5
domain: nonio
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
Timestamp: 2026-09-19T00:00:00Z
## Claim
The consumer acks after the side effect.
```

`assertions/C5/nonio/pos-late.md`
```
---
assertion: C5
domain: nonio
polarity: pos
expected_flags: [timestamp_invalid]
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
Timestamp: 2026-09-18T18:35:01Z
## Claim
The consumer acks after the side effect.
```

`assertions/C5/nonio/neg.md`
```
---
assertion: C5
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:30:00Z
calibrated: 0.70
---
--- file: card.md ---
Timestamp: 2026-09-18T18:34:59Z
## Claim
The consumer acks after the side effect.
```

#### C6 — `bracket_unproven` (cap 0.3)

`assertions/C6/io/pos.md`
```
---
assertion: C6
domain: io
polarity: pos
expected_flags: [bracket_unproven, uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
## Claim
Root cause: container create fails above 73 layers on this runner.
--- file: bracket.md ---
```

`assertions/C6/io/neg.md`
```
---
assertion: C6
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
## Claim
Root cause: container create fails above 73 layers on this runner.
2x2 row: layers-exact=1 layers-ref=0 (failing) / 0,0 (passing)
--- file: bracket.md ---
bracket=[72,74] width=2
```

`assertions/C6/nonio/pos.md`
```
---
assertion: C6
domain: nonio
polarity: pos
expected_flags: [bracket_unproven, uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
## Claim
Root cause: the consumer stalls above 512 in-flight messages.
--- file: bracket.md ---
```

`assertions/C6/nonio/neg.md`
```
---
assertion: C6
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
## Claim
Root cause: the consumer stalls above 512 in-flight messages.
2x2 row: prefetch-exact=1 prefetch-ref=0 (failing) / 0,0 (passing)
--- file: bracket.md ---
bracket=[510,512] width=2
```

Note: C6 cards are `environment_dependent`, so C7 also evaluates on them: the neg carries a `2x2 row:` line so C7 stays silent; the pos cards declare `expected_flags: [bracket_unproven, uncited]` because T13 fixture-wide parity asserts the *whole* fired set == `expected_flags`. The T2 per-id assertion is "the named flag ∈ fired" for pos and "named flag ∉ fired" for neg; only T13 uses set equality.

#### C7 — `uncited` (cap 0.5)

`assertions/C7/io/pos.md`
```
---
assertion: C7
domain: io
polarity: pos
expected_flags: [uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: /proc/uptime is served non-seekable under this runtime
## Mechanism
The shell's 1-byte read fallback fails on the non-seekable node.
```

`assertions/C7/io/neg.md`
```
---
assertion: C7
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: /proc/uptime is served non-seekable under this runtime
## Mechanism
The shell's 1-byte read fallback fails on the non-seekable node.
2x2 row: uptime-exact=1 uptime-ref=0 (failing) / 0,0 (passing)
```

`assertions/C7/nonio/pos.md`
```
---
assertion: C7
domain: nonio
polarity: pos
expected_flags: [uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: the broker requeues with redelivered=true when the channel closes before ack
## Mechanism
A crash between send and ack requeues the message.
```

`assertions/C7/nonio/neg.md`
```
---
assertion: C7
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: the broker requeues with redelivered=true when the channel closes before ack
## Mechanism
A crash between send and ack requeues the message.
2x2 row: redelivered-exact=1 redelivered-ref=0 (failing) / 0,0 (passing)
```

#### C8 — `behaviour-cite: missing` (cap 0.5)

`assertions/C8/io/pos.md`
```
---
assertion: C8
domain: io
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The FUSE handler returns EOF at offset>0.
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | procUptime read | returns EOF at offset>0 | handler read function | the code that implements returns EOF at offset>0 | fetched:gh-api |
```

`assertions/C8/io/pos-empty-status.md`
```
---
assertion: C8
domain: io
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The FUSE handler returns EOF at offset>0. behaviour-definition: row 2
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | procUptime read | returns EOF at offset>0 | handler read function | the code that implements returns EOF at offset>0 | fetched:gh-api |
| 2 | bash read builtin | falls back to 1-byte reads on ESPIPE | read.def zread branch | the code that implements falls back to 1-byte reads on ESPIPE | |
```

`assertions/C8/io/neg.md`
```
---
assertion: C8
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The FUSE handler returns EOF at offset>0. behaviour-definition: row 1
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | procUptime read | returns EOF at offset>0 | handler read function | the code that implements returns EOF at offset>0 | fetched:context7 |
```

`assertions/C8/nonio/pos.md`
```
---
assertion: C8
domain: nonio
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The broker requeues with redelivered=true when the channel closes before ack.
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | broker ack | requeues with redelivered=true on channel close | broker doc Consumer acknowledgements | the clause that specifies requeues with redelivered=true on channel close | fetched:context7 |
```

`assertions/C8/nonio/pos-empty-status.md`
```
---
assertion: C8
domain: nonio
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The broker requeues with redelivered=true when the channel closes before ack. behaviour-definition: row 2
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | broker ack | requeues with redelivered=true on channel close | broker doc Consumer acknowledgements | the clause that specifies requeues with redelivered=true on channel close | fetched:context7 |
| 2 | producer retry | publishes again on HTTP 5xx | producer client retry policy | the code that implements publishes again on HTTP 5xx | |
```

`assertions/C8/nonio/neg.md`
```
---
assertion: C8
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The broker requeues with redelivered=true when the channel closes before ack. behaviour-definition: row 1
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | broker ack | requeues with redelivered=true on channel close | broker doc Consumer acknowledgements | the clause that specifies requeues with redelivered=true on channel close | fetched:context7 |
```

C8 scope note: C8 must only evaluate when the card asserts a primitive behaviour or `behaviour_definitions_path` is supplied; in these fixtures the `behaviour-definitions.md` block is always present, so "missing cite" fires on pos and the neg cites row 1. For fixtures of *other* C-ids (which carry no `behaviour-definitions.md` block) C8 must stay silent: predicate guard `if not behaviour_text: return False`. Same guard pattern for C6 (`bracket_text is None` ⇒ silent; empty string from an empty block ⇒ evaluate) — the loader must distinguish "block absent" (`None`) from "block present but empty" (`""`). Likewise C3 evaluates only when the card mentions a control run/arm; C4 only when an instrumentation table exists; C7 only when the claim is environment_dependent or has `environment-property:`. This is what keeps every fixture's full flag set equal to its `expected_flags` (T13).

### 4.4 Procedure and counter fixtures (write verbatim)

`procedures/producers/io.sh` (12 lines; three `rc=` sites, one computed enum, one decoy in a comment)
```
#!/usr/bin/env bash
# ## Mechanism rows — decoy heading inside a comment: rc=runner-unavailable must not count
aidev_seed_now() {
  IFS=' ' read -r up _ </proc/uptime || return 1
  prefix=runner
  rc=$prefix-unavailable
  [ -x "$(command -v git)" ] || { rc=runner-unavailable; return 1; }
  timeout 120 git clone "$REPO_URL" || { rc=runner-unavailable; exit 2; }
  rc=cloned
}
aidev_seed_now
echo "seed-repo-outcome=$rc"
```
Expected by T3: `grep_hits` for value `runner-unavailable` ∪ `rc=` = 6 lines (lines 6,7,8,9 + the comment line 2 + `$rc` echo? — no: `rc=` regex `\brc=` matches 6,7,8,9 and line 2; `echo "...=$rc"` has no `rc=` ⇒ 5 hits; comment hit ⇒ `surviving=no` row). Rows = 5, `count_unknown = True` (line 6). The builder pins the exact numbers in the test after running P1 once; the invariant `rows == grep_hits` is what matters.

`procedures/producers/nonio.py` (ruff-clean; not collected)
```python
"""Fixture for T3: two literal DEAD_LETTER producers + one return."""

from __future__ import annotations


def handle(msg: dict) -> str:
    status = "PENDING"
    if msg.get("attempts", 0) >= 3:
        status = "DEAD_LETTER"
        return status
    if not msg.get("payload"):
        status = "DEAD_LETTER"
    return status
```

`procedures/primitivegrep/sink.sh`
```
#!/usr/bin/env bash
read -r u _ </proc/uptime
cat /sys/class/net/eth0/mtu
exec 2>/dev/null
echo x >/dev/null
: </dev/tty
stat -c %s /proc/self/status
```
Expected hits (kind `read/parse`): lines 2, 3, 7 only.

`procedures/primitivegrep/decoy.sh`
```
#!/usr/bin/env bash
cat /proc/cpuinfo
```

`procedures/locus/complete.md`
```
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: startup.sh:583 @ ci-runner-sysbox
SAME-ENV: no
OBSERVE-VIA: artifact-file
## Arm: sysbox-public (failing)
runs-in=ci-runner-sysbox
## Arm: dind-public (passing)
CONTROL-PROOF: yes: startup.sh:583
```

`procedures/locus/missing-run-site.md`
```
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
SAME-ENV: no
OBSERVE-VIA: artifact-file
## Arm: dind-public (passing)
CONTROL-PROOF: yes: startup.sh:583
```

`procedures/locus/one-env.md`
```
The seed step fails on runner ci-runner-sysbox with exit 1 at startup.sh:583.
```

`procedures/locus/two-env.md`
```
strategy:
  matrix:
    runner:
      - ci-runner-sysbox
      - ci-runner-dind
```

`procedures/locus/no-env.md`
```
Traceback (most recent call last):
  File "consumer.py", line 41, in handle
    status = "DEAD_LETTER"
KeyError: 'payload'
```

`procedures/verdict-source/marker.log`
```
step: seed checkout
RESULT: PASS
step: seed assert
RESULT: FAIL
conclusion: success
```

`procedures/verdict-source/no-marker.log`
```
step: seed checkout
step: seed assert
```

`procedures/verdict-source/conclusion-only.log`
```
conclusion: success
```

`procedures/discriminator/io.md` — the R-07 form (`v2:364-379`) filled with worked example 1 (`v2:382`):
```
# Discriminator: uptime-regex
Hypothesis A: the pseudo-file is served non-seekable so the shell's 1-byte read fallback fails
Hypothesis B: temp dir unwritable at mktemp
Observable that differs: uptime-regex — emitted at test-startup-boot.sh:444 as seed-diag-uptime-regex
Exact probe: IFS=' ' read -r up _ < /proc/uptime; [[ $up =~ ^[0-9] ]]
Primitive under dispute, fetched verbatim: procUptime.go Open() sets nonSeekable=true; bash read.def lseek ESPIPE -> zread(fd,&c,1)
Reference-context value: true
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | refuted | consistent |
| false | consistent | consistent |
Falsifier sentence: "If uptime-regex=true on the next run, A is false."
Self-consistency: if Reference-context value ≠ the value actually observed in the reference context, mark THIS PROBE `suspect` under Grounding Gaps; do not read the outcome table for it.
```
T6 io truth vector: `uptime-regex=false, uptime-bulk=true, tmp-writable=true` ⇒ row `false` ⇒ A consistent, B consistent; B refuted by its own probe `tmp-writable=true` ⇒ winner A.

`procedures/discriminator/nonio.md` — worked example 2 (`v2:383`):
```
# Discriminator: redelivered
Hypothesis A: consumer acks after side-effect, so a crash between send and ack redelivers
Hypothesis B: producer publishes twice on HTTP retry
Observable that differs: redelivered — message header flag, logged at consumer.py:42
Exact probe: SELECT bool_or(redelivered) FROM consumed_log WHERE invoice_id=:id
Primitive under dispute, fetched verbatim: broker doc "Consumer acknowledgements": "If a consumer's channel closes before an ack is received, the message is requeued with redelivered=true."
Reference-context value: false
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | consistent | refuted |
| false | refuted | consistent |
Falsifier sentence: "If redelivered=false on the next duplicate, A is false."
Self-consistency: if Reference-context value ≠ the value actually observed in the reference context, mark THIS PROBE `suspect` under Grounding Gaps; do not read the outcome table for it.
```
T6 nonio truth vector: `redelivered=true` ⇒ A consistent, B refuted ⇒ winner A.

`procedures/rows/distinguishing.md`
```
**Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-exact | 1 | 0 |
| uptime-ref | 0 | 0 |
| tmp-writable-exact | 0 | 1 |
| tmp-writable-ref | 0 | 0 |
| control | 0 | 0 |
```

`procedures/rows/indistinguishable.md`
```
**Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a  **indistinguishable**: a,b
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-exact | 1 | 1 |
| uptime-ref | 0 | 0 |
| dns-exact | 1 | 1 |
| dns-ref | 0 | 0 |
| control | 0 | 0 |
```

`procedures/rows/exact-only.md`
```
**Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-exact | 1 | 0 |
| control | 0 | 0 |
```

`procedures/rows/overflow.md` (9 pairs + control; header must carry `probe-rows-truncated: 1`)
```
**Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: n/a  **probe-rows-truncated**: 1
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| p1-exact | 1 | 0 |
| p1-ref | 0 | 0 |
| p2-exact | 1 | 0 |
| p2-ref | 0 | 0 |
| p3-exact | 1 | 0 |
| p3-ref | 0 | 0 |
| p4-exact | 1 | 0 |
| p4-ref | 0 | 0 |
| p5-exact | 1 | 0 |
| p5-ref | 0 | 0 |
| p6-exact | 1 | 0 |
| p6-ref | 0 | 0 |
| p7-exact | 1 | 0 |
| p7-ref | 0 | 0 |
| p8-exact | 1 | 0 |
| p8-ref | 0 | 0 |
| control | 0 | 0 |
```
(T17 asserts: 8 pairs kept, header value 1 = the 9th pair dropped; a copy without the header and with 9 pairs is built inline in the test as the invalid twin.)

`procedures/differential/table.md`
```
## substituted
| env | exact | ref |
|---|---|---|
| sysbox (failing) | 1 | 0 |
| dind (passing) | 0 | 0 |

## all-unobserved
| env | exact | ref |
|---|---|---|
| sysbox (failing) | unobserved | unobserved |
| dind (passing) | unobserved | unobserved |

## single-env
| env | exact | ref |
|---|---|---|
| sysbox (failing) | 1 | 0 |
```

`procedures/behaviour/fetched.md`
```
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | procUptime read | returns EOF at offset>0 | the function that opens/reads the node | the code that implements returns EOF at offset>0 | fetched:context7 |
```

`procedures/behaviour/recalled.md`
```
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | kernel FUSE reply | rejects oversize replies with EIO | fuse dev read path | the code that implements rejects oversize replies with EIO | recalled, not load-bearing |
```

`procedures/behaviour/missing.md`
```
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
```

`procedures/tasklist/authorized.md`
```
**Round**: 1 of 3  **re-run permitted**: yes  **discriminator-required**: yes  **capability-verdict**: blocked
## Emitter search
emitters-found: 1
- test-startup-boot.sh:444 `echo "seed-diag-uptime-regex=..." >> "$DIAG_OUT"`
already-read-files: 2
```
(T10: `hardstop_verdict` ⇒ `status: partial`, task rows required; `evaluate_validator` A10 fires because `capability-verdict: blocked` with `emitters-found: 1`.)

`procedures/tasklist/refused.md`
```
**Round**: 1 of 3  **re-run permitted**: no  **discriminator-required**: yes  **capability-verdict**: n/a
## Emitter search
emitters-found: 1
- test-startup-boot.sh:444 `echo "seed-diag-uptime-regex=..." >> "$DIAG_OUT"`
already-read-files: 2
```

`procedures/tasklist/no-emitter-no-file.md`
```
**Round**: 1 of 3  **re-run permitted**: unknown  **discriminator-required**: yes  **capability-verdict**: blocked
## Emitter search
emitters-found: 0
already-read-files: 0
channels searched: startup.sh seed function, test-startup-boot.sh caller
```

`procedures/tasklist/source-only-read.md`
```
**Round**: 1 of 3  **re-run permitted**: unknown  **discriminator-required**: yes  **capability-verdict**: blocked
## Emitter search
emitters-found: 0
already-read-files: 0
read-log: startup.sh, test-startup-boot.sh
```
(T10 passes `read_log=["startup.sh","test-startup-boot.sh"]` for this case and `["startup.sh","out/job-1.log"]` for the "N=0 + already-read log ⇒ append row" case, which reuses `no-emitter-no-file.md` text with `already-read-files: 1` substituted inline.)

`counters/cosmetic-log.txt` (one call per line; `out/` is the output dir)
```
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Glob out/*.md
Read out/evidence-validation.md
Read out/REPORT.md.draft
ls out/
Write out/x.md
Read out/job-1.log
Read src/a.sh
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
Read out/REPORT.md.draft
```
Expected P17 result: fires at line 5 (`cosmetic_overrun=5`); lines 6-8 exempt (no count change); line 9 resets; lines 10-14 ⇒ fires again at line 14 (count 5), and at line 19 (count 10, `cosmetic_overrun=10`). Returned indexes `[5, 14, 19]` (1-based).

## 5. Regression set (T15) — MANIFEST + expected flags

### 5.1 `regression/sysbox-20260918/MANIFEST`

Format: one record per vendored file, four tab-separated columns `path<TAB>sha256<TAB>bytes<TAB>source`, `#` comment lines allowed. `path` is relative to the MANIFEST's directory; `source` is the absolute origin path (informational only — T15 never reads it; it lets a reviewer re-vendor with `cp`). Hashes/bytes below are 04 §3.4's recorded values (verified present 2026-09-19 with `ls`; the builder re-runs `sha256sum` when copying and must get these exact values or the copy is not a byte copy).

```
# path	sha256	bytes	source
GLM-RUN2/REPORT-RUN2.md	3e6a9902b80cb6fcf133ffc356cc1824d3f5c6dd972a018ecf706c2a276aaabb	7016	/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/REPORT-RUN2.md
GLM-RUN2/run2-tier2-root-cause-analyst-calibration.md	62acf9283e3a1134b65113e021b582a0a9dba1813557fa42263b06c2a6cd0df8	4060	/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-calibration.md
GLM-RUN2/run2-tier2-root-cause-analyst-hypothesis.md	d8bef2f015603ab800a455a192be38c2d734c306f7542b1aa17415a36f6708da	8358	/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/run2-tier2-root-cause-analyst-hypothesis.md
GLM-RUN2/candidate-fixes.md	76cf294c9fae7e940101b1dd4d453197905e70e971c35ce5c519154e7fca6bdf	2157	/config/workspace/Coder/.claude/worktrees/sysbox-retry-glm/.dev/troubleshoot/sysbox-deep/candidate-fixes.md
Fable-D3/REPORT.md	4910ffa683c357ba23d5b002f2ef8ba501d7da06fad4f1361b359872e3ef037d	6869	/config/workspace/Coder/.claude/worktrees/sysbox-retry-fable/.dev/troubleshoot/sysbox-deep-3/REPORT.md
Fable-D3/candidate-fixes.md	1fde1d0f936d5cbd40303424628a1993483827c92512bbbfc7f5a2bac900ecf6	2820	/config/workspace/Coder/.claude/worktrees/sysbox-retry-fable/.dev/troubleshoot/sysbox-deep-3/candidate-fixes.md
Astra-A3/diagnosability-tasklist.md	967cede52133387697b8d7458f7a2384619575e703126ea9b6e8be7d67ba93fd	4446	/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/diagnosability-tasklist.md
Astra-A3/tier1-observation.md	3eca299bf79d6107019f2125720872097b344f3061684977a01bee3d67f916ed	11565	/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/tier1-observation.md
Astra-A3/REPORT.md	54a4205c0333e9a63614f156a94698efd555a6e88788876c238ab4e412502895	6633	/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.dev/troubleshoot/sysbox-deep/retry3-internal-runner/REPORT.md
```

Nine files (the 04 table's 9 hashed entries; GLM `candidate-fixes.md` is run-1 vintage — vendored for completeness, A5 fires without it). Fable's hypothesis cards are **not** vendored (see 5.2). T15 step 1: `for path, sha, n, _ in manifest: assert sha256(read_bytes(path)) == sha and len == n` — byte-copy guard before any evaluation. I-24 (source availability): all nine sources exist on this machine today; if the Coder worktrees are gone when the builder runs, the vendored copies + MANIFEST are self-sufficient and the `source` column is documentation only.

### 5.2 `expected_flags` table and the in-scope input set per parameter

`load_regression(param) -> (ValidatorInputs, CalibratorInputs | None)` builds inputs from the vendored files only; `artifact_mtimes = {}` and `card_mtime = None` because vendored mtimes are meaningless ⇒ A3/C5 evaluate the `T00:00:00Z` clause only (§1.1 `_ts_violations` with `mtime=None`). Test asserts `fired_ids == expected` (set equality on ids, not flags, because C2 flags carry a token suffix).

| param | validator inputs (roles) | calibrator inputs | expected ids | evidence line (verified 2026-09-19) |
|---|---|---|---|---|
| GLM-RUN2 | `report=REPORT-RUN2.md`, `calibration_texts=[…calibration.md]`, `card_texts=[…hypothesis.md]`, `candidate_fixes_text=candidate-fixes.md`, `files_present=` the 4 vendored names (no `job-*.log`; locus absent ⇒ A8 silent) | `card=…hypothesis.md`, `calibrated=0.42` (from calibration `:28`/`:34`), `locus_text=""` | **{A1, A3, A4, A5, C2, C3}** (`v2:471,588`) | A1: `REPORT-RUN2.md:6` `**Confidence**: 0.42`, `:21` `**Root cause** (probable, pending enum): … \`clone-failed\``, `:57` "`clone-failed` is source-logic-deduced". A3: `calibration.md:6` `**Timestamp**: 2026-09-19T00:00:00Z`. A4: `REPORT-RUN2.md:63` `**Verdict: blocked_pending_retry_run**` inside `## Pipeline Hardening Closure` (`:61`). A5: `REPORT-RUN2.md:72` `- Adversarial: not invoked — consensus`; `candidate-fixes.md:5` `**consensus**`; `calibration.md:13,46` `claim_class defaults runtime_behavior, evidence_class none`. C2: `hypothesis.md:33` "…All excluded." — exclusion lines name `` `skipped` ``, `` `rejected-input` ``, `` `destination-conflict` `` (and `:5` `` `timed-out` ``, `` `runner-unavailable` ``, `` `checkout-unverified` ``) with no `exit statement` phrase ⇒ one `unproven_exclusion:<token>` per token. C3: `hypothesis.md:5` "by the two control runs" and no `CONTROL-PROOF: yes` anywhere in GLM artifacts (grep → 0). |
| Fable-D3 | `report=REPORT.md`, `candidate_fixes_text=candidate-fixes.md`, `calibration_texts=[]`, `card_texts=[]`, `files_present=` the 2 vendored names | **None — calibrator not run** | **{}** and `_confidence(report) == 0.72` (`REPORT.md:4` `confidence: 0.72`) | A1: `## Diagnosis` first line (`:23`) has no `ENUM_TOKEN` match (only `tier1-observation.md`, `aidev_seed_now`, `aidev_seed_outcome=runner-unavailable` — all excluded by the regex); confidence 0.72 ≥ 0.5. A4: no `pipeline_hardening_verdict` key, `:10` `pipeline_hardening_applicable: false` ⇒ pass. A5: `candidate-fixes.md:8` says `**consensus on site**` but REPORT has no `adversarial_invoked`/`Adversarial:` line (grep → 0) ⇒ silent. A3: no `Timestamp`/`Date`/`pushed_at` line (grep → 0). A2/A6-A10: no diff, form, locus, tasklist ⇒ silent. |
| Astra-A3 | `report=REPORT.md` (optional; carries no verdict/timestamp/enum headline — grep → 0), `tasklist_text=diagnosability-tasklist.md`, `observation_text=tier1-observation.md` | **None** (no card vendored); instead T15 asserts `requires_runs_in(tier1_observation, same_env="no") is True` (P11 — "cards lacking `runs-in=` returned at Wave 1.7") | **{A10}** (T-table "T10 emitter rule fires"; A7 silent) | A10: `diagnosability-tasklist.md:24` `- **Blocked on capability, not permission**: …` and no `## Emitter search` (grep → 0). A7: no `execution-locus.md`, no `producers.md` in the Astra dir ⇒ `locus_text=""` ⇒ silent (AD-04). `runs-in=` grep over `tier1-observation.md` → 0. |

**Why C7/C8 are scoped out of Fable-D3 (and Fable cards are not vendored):** the spec claim is "none fire, 0.72 kept" (`v2:471`). Fable's `tier2-*-hypothesis.md` cards predate R-05/R-09 (no `2x2 row`, no `behaviour-definition: row N`) and are `environment_dependent`; fed to `evaluate_calibrator` they trip C7 and C8 by construction (04 §3.4 caveat), which would make the spec's falsifiable claim false for reasons unrelated to the incident. The claim is about the *report-level* outcome (validator A-rules + the confidence value), so T15-Fable runs the validator only and records `calibrator: not run (pre-R-05/R-09 cards)` in its docstring. This is the narrowest reading that keeps `v2:471` true and is what 04 §3.4 recommended.

**A10 regex decision:** `re.compile(r"(?i)capability-verdict\**:\s*\**blocked\b|\bblocked on capability\b")`. Both alternatives are needed: the R-03 header form for T1/T10 fixtures, the prose form for Astra (`:24`). Case-insensitive because Astra bolds and capitalises. The `\b` after `blocked` prevents `blocked-on-authorization` (R-16 contract value) from matching the header alternative.

**C5 on GLM:** `calibration.md:6` also satisfies C5, but C5 is evaluated on the *card* (`card_text`), not the calibration report, so it does not fire on the GLM parameter; A3 catches the same line on the validator side. Recorded so nobody "fixes" the expected set to include C5.

## 6. T13 `test_inline_fallback_parity.py` — exact assertions

Three deterministic assertions (04 §4), all in one file, no LLM:

1. **Table parity.** Parse every markdown surface that carries the assertion list and assert the `(id, flag, trigger)` triples are identical across all of them and equal to `_assertions.FLAGS`:
   - `src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md` — **recommended single source** (04 §4 item 1 "lazy design"); the R-14 build item creates it with one table `| id | trigger | flag | severity |`.
   - `src/superclaude/agents/evidence-validator.md` `## Structural assertions` (R-14: `VAL:63-97` gains it) — either the same table verbatim or the single line `See refs/agent-assertions.md` (T13 accepts either: a cite line counts as parity).
   - `src/superclaude/agents/confidence-calibrator.md` step 5b / Notes — same rule.
   - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` inline-fallback paragraph (next to `SKILL:282` / `:452`) — same rule.

   Extraction regex (applied to each file; rows outside a table are ignored):
   ```python
   ROW = re.compile(
       r"^\|\s*(?P<id>A(?:10|[1-9])|C(?:3b|[1-8]))\s*\|\s*(?P<trigger>[^|]+?)\s*\|\s*`(?P<flag>[^`]+)`\s*\|",
       re.M,
   )
   CITE = re.compile(r"refs/agent-assertions\.md")
   def parse_flag_table(text: str) -> dict[str, tuple[str, str]]:
       return {m["id"]: (m["trigger"], m["flag"]) for m in ROW.finditer(text)}
   ```
   Assertion: `for surface in SURFACES: t = parse_flag_table(read(surface)); assert t == REF_TABLE or CITE.search(read(surface)), surface`, and `REF_TABLE == {f.id: (f.trigger, f.flag) for f in FLAGS}`. Trigger sentences must be byte-identical after `str.strip()` — no normalisation, so the builder writes the §1.2 trigger column into both the markdown and `FLAGS` from the same clipboard. Keys must be exactly the 19 ids `{A1..A10, C1..C8, C3b}`.

2. **Evaluator ⇔ fixture parity (fixture-wide).** For every file under `fixtures/assertions/**/*.md`: `fx = load_fixture(p); assert fired_flags(fx) == set(fx.meta["expected_flags"])`, where `fired_flags` returns the flag tokens (C2 tokens included, e.g. `unproven_exclusion:auth-denied`). For every `regression/` param: `fired_ids == expected ids` from §5.2. Docstring must say: "There is one executable assertion engine; 'agent path == inline path' is satisfied by construction when that engine's output equals every fixture's declared expectation and its registry equals every prose surface (assertion 1)."

3. **Name coverage.** `{f.flag.split(":")[0] for f in FLAGS} ⊆ tokens that appear in the SKILL fallback paragraph`, i.e. the SKILL must mention every flag token at least once (or cite the ref) — guards the case where the SKILL keeps a stale hand-written list.

## 7. T14 `test_calibrator_eval_cases.py` — non-regression on fixtures 1-9 / P1-P5

The ref is a spec of expected scores, not a corpus (04 §5). Two halves:

**(a) Pinned expectation lines** — `REF = read("refs/calibrator-eval-cases.md")`; one parametrized case per line, exact substring:

| fixture | asserted substring (verbatim from the ref, line) |
|---|---|
| F1 | `**Expected calibrated**: ≤ 0.70 (M3a cap fires).` (`:10`) |
| F2 | `**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80).` (`:16`) |
| F3 | `**Expected calibrated**: 1.0. **Asserts**: refactor does NOT over-correct.` (`:22`) |
| F4 | `**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80).` (`:27`) |
| F5 | ``calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM``` (`:32`) |
| F6 | `**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0.` (`:38`) |
| F7 | `**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a).` (`:45`) |
| F8 | `**Expected calibrated**: ≤ 0.70.` (`:50`) |
| F9 | `**Expected calibrated**: 0.70-0.85 range; NO hard cap fires.` (`:55`) |
| P1-P5 | the five table rows `:61-65` as substrings (`| P1 | M1 gate | \`evidence_grounding ≤ 0.5\` ⟹ \`calibrated ≤ 0.80\` |` …) |
| suite | `A regression on any fixture or hard property (P1-P4) blocks merge.` (`:77`) and `tests/troubleshoot/test_calibrator_eval_cases.py` (`:81`) |

Deliberately NOT asserted: lines `:49` and `:54` ("Replays actual H2/H1 card") — the R-17 allow-list lines (04 §1b); T14 is semantic, not byte-identical.

**(b) Formula reproduction** — inline in the test (no `src/` module; ponytail):
```python
def rubric(eg, rc, sc, rf, fd, dc, claim, verdict):
    base = min(sum([eg, rc, sc, rf, fd, dc]) / 6, eg + 0.30, rc + 0.30)   # RUB:20
    if claim == "runtime_behavior" and rc < 1.0:                              # CAL step 5a
        base = min(base, 0.70 if verdict in ("REFUTE", "REJECT") else 0.84)
    return round(base, 2)
```
Cases: F1 `rubric(1,0,1,1,1,1,"runtime_behavior","REFUTE") <= 0.70`; F2 `(1,.5,1,1,1,1,"runtime_behavior","AFFIRM") <= 0.80`; F3 `(1,1,1,1,1,1,"static_defect","AFFIRM") == 1.0`; F4 `(.5,.5,1,1,1,1,"static_defect","AFFIRM") <= 0.80`; F6 `(1,1,1,1,1,1,"runtime_behavior","REFUTE") == 1.0`; F7/F8 `(1,0,*,*,*,*,"runtime_behavior","REFUTE") <= 0.70` for any other four dims; F9 `(1,1,1,.5,1,.5,"runtime_behavior","AFFIRM")` in `[0.70, 0.85]` (mean 0.833, no cap). Properties over the grid `{0,.5,1}^2` for `(eg, rc)` with the other four fixed at 1.0: P1 `eg<=.5 ⇒ <=.80`; P2 `rc<=.5 and claim in {runtime_behavior, environment_dependent} ⇒ <=.80`; P3 `REFUTE and runtime_behavior and rc<1 ⇒ <=.70`; P4 determinism: 5 calls equal. P5 is warn-only in the ref and has no numeric input in a formula test — record `pytest.skip("P5 soft")` or omit. Then the R-14 layering check: `apply_caps(rubric(...), CalibratorResult(cap=0.5)) == min(...)` — proves C6/C7/C8 caps sit **after** the formula and `RUB:20` is untouched.

## 8. Commands and the known-red baseline

Run from `/config/workspace/IronClaude`, in this order:

```bash
uv run pytest tests/troubleshoot/ -v                 # new + existing troubleshoot tests
uv run pytest -q                                     # FULL suite — required, see below
uv run ruff check tests/troubleshoot/ && make lint   # ruff on the new files, then repo-wide
make verify-sync                                     # after any src/superclaude edit (R-14 tables)
```

- **Full suite is mandatory**, not optional: 05 found the content gate `tests/agents/test_tavily_tool_parity.py` rglobs `agents/` and `skills/`; adding `refs/agent-assertions.md` and editing the two agents can trip it (and `tests/skills/test_tier2_tavily_consistency.py:16` reads the troubleshoot SKILL — 04 §1). Any new red there is a defect of this track.
- **Known-red baseline (record, do not fix):** `tests/troubleshoot/backtest/test_backtest_e4.py:105` (`assert "gate_passed" in low and "_evaluate_gate" in low` against `refs/contract-enumeration.md`) — pre-existing, unrelated (04 §0: baseline 1 failed / 70 passed). The Phase 3 L5 verdict item must state "1 known-red (e4), 0 new reds"; the acceptance count for R-19 excludes it. Do not touch `contract-enumeration.md` to green it.
- Expected new totals: existing 71 (70 pass + e4) + T1 46 + T2 42 + T3 2 + T4 1 + T5 5 + T5b 3 + T6 2 + T7 3 + T8 1 + T9 1 + T10 4 + T11 2 + T12 3 + T13 3 + T14 ~20 + T15 3 + T16 3 + T17 4 + T18 3 + T19 2 + hc-guard 1 ≈ **153 new cases**. The builder records the actual count in `test-results/test-summary.md`.
- Writes: only `tmp_path` (T3, T9, T19). `tests/conftest.py::_pollution_snapshot` (04 §2) fails the session if anything under `docs/mistakes/` or `docs/memory/` changes — never write there.

## 9. Ruff constraints for the new Python files

`pyproject.toml:191-211`: `line-length = 88`, `select = ["E","F","I","N","W","TID"]`, `ignore = ["E501","N818"]`, `extend-exclude = [".dev/", "tests/audit/fixtures/syntax_error.py"]`, `target-version = "py310"`.

- **Files linted:** `tests/troubleshoot/_assertions.py`, `_procedures.py`, all 20-21 `test_*.py`, and `tests/troubleshoot/fixtures/procedures/producers/nonio.py` (`fixtures/**` is NOT excluded). `nonio.py` as written in §4.4 is ruff-clean (docstring, `from __future__ import annotations`, no unused names). Do **not** add a `fixtures/**` exclusion — the `syntax_error.py` precedent is per-file and this fixture has no reason to be malformed.
- **Decision: procedure fixtures are `.md`/`.sh`/`.log`/`.txt`, except `nonio.py`** (spec-named, `v2:554`). Everything else is not Python and not linted. No `.py` fixtures elsewhere.
- `I` (isort): `from __future__ import annotations` first, then stdlib (`hashlib`, `json`, `re`, `dataclasses`, `datetime`, `pathlib`), blank line, `pytest`, blank line, `from tests.troubleshoot._assertions import …` / `from tests.troubleshoot._procedures import …` (first-party; `tests` resolves because `tests/__init__.py` exists and `_impl_guard` is imported the same way at `backtest/test_waiver_regreen.py:22`).
- `N`: function names `snake_case`; dataclass names `CapWords` (`ValidatorInputs`); regex constants `UPPER` (`ENUM_TOKEN`, `FLAGS`); no `N806` issues if locals stay lowercase (`ROW`, `CITE` in T13 are module-level constants, fine).
- `E501` is ignored, so long trigger strings and long fixture globs on one line are legal; `W291/W293` (trailing whitespace) are NOT ignored — fixture `.md` files are not linted, but do not leave trailing spaces in the `.py` string literals that embed inline tables (T7, T9, T17 twin).
- `TID` (banned relative imports / `anthropic` ban, `pyproject:213+`): use absolute `tests.troubleshoot.*` imports; nothing here imports `anthropic`.
- Format: `uv run ruff format --check tests/troubleshoot/` is in the 06 skeleton item 3.30 — run it; `make format` if it complains.

## Status: Complete

**Summary**
1. Harness = two stdlib modules: `tests/troubleshoot/_assertions.py` (19-entry `FLAGS` registry, `evaluate_validator`, `evaluate_calibrator`, `load_fixture`, `fired_ids`) and `tests/troubleshoot/_procedures.py` (25 functions P1-P25). Dependency direction `_assertions → _procedures`.
2. Tests: 20 spec files (T1-T14, T5b, T15-T19) + 1 optional `test_hc_rename_guard.py`; ≈153 new cases (T1 46, T2 42).
3. Fixtures: 88 assertion files (19 ids × 2 domains × 2 base + 12 variants), 31 procedure/counter files, 9 vendored regression files + MANIFEST — all bodies given verbatim in §4-§5.
4. NOT_MECHANICAL (proxy implemented): **A1/C1** ("definite" → `ENUM_TOKEN` backticked hyphenated word in headline lines), **A2** ("collector/invocation site" → added diff line with an emit verb), **A5** ("dynamic claim" → `claim_class ∈ {runtime_behavior, environment_dependent}`, absent ⇒ runtime_behavior), **A9** ("observed reference value" → `reference|control`-prefixed observation line), **C2** ("that enum's exit statement" → structured `Excluded: \`tok\` — exit statement file:line`), **C3** ("cited as a control" → phrase `control run|arm`), **C6** ("asserts a threshold" → comparative+integer or integer+count-noun), **C7** ("names an environment property" → `claim_class: environment_dependent` or `environment-property:` line). Mechanical as specified: A3, A4, A6, A7, A8, A10, C3b, C4, C5, C8.
5. Decisions recorded: I-8 (0.4 cap is orchestrator-side, in P22, not a C-rule), I-9 (C6 = calibrated cap 0.3), I-10 (flag names for A6/A7/A8/A9/C6), I-11 (`locus_path`/`output_dir` inputs), I-22 (`C3b/` dir), I-23 (this file), I-24 (sources present; MANIFEST self-sufficient); Fable-D3 calibrator not run (C7/C8 scoped out, reason §5.2); A10 regex `(?i)capability-verdict\**:\s*\**blocked\b|\bblocked on capability\b`; 06 §5 3.x names superseded by the spec T-table.
