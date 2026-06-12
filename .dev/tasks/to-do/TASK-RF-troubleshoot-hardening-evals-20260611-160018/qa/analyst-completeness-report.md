# Research Completeness Verification (Completeness / Breadth Lens)

**Track:** task-builder single track — troubleshoot-hardening differential backtest harness
**Goal:** Executable differential backtest harness under `tests/troubleshoot/backtest/` replaying 5 pipeline escapes (E1-E5) against pre-fix commits, asserting OLD-protocol=MISS vs NEW-H0-H5-gate=CATCH, emitting machine-readable catch-rate report that sets `backtest_status` per spec NFR-1.
**Date:** 2026-06-11
**Lens:** Completeness / Breadth — does every sub-system the builder needs have actionable research?
**Files assigned:** 01-07 (7 files)

---

## Sub-system coverage map (the 7 areas the builder needs)

| # | Sub-system | Primary file |
|---|-----------|--------------|
| 1 | eval-framework mirror | 01-eval-framework-inventory.md |
| 2 | pytest/xfail conventions | 02-test-patterns-and-xfail.md |
| 3 | git-replay isolation | 03-git-replay-helpers.md |
| 4 | spec contracts (E1-E5 + backtest_status) | 04-spec-contract-deepdive.md |
| 5 | per-escape replay differential | 05-replay-targets.md |
| 6 | impl-tasklist coordination / NEW-gate seam | 06-impl-tasklist-crossref.md |
| 7 | MDTM template + report model | 07-mdtm-template-and-report-model.md |

---

## Sub-system coverage verdict (BREADTH gate)

| # | Sub-system | Primary file | Coverage | Notes |
|---|-----------|--------------|----------|-------|
| 1 | eval-framework mirror | 01 | COVERED | Full API surface cataloged (models/run_report/loader/runner/orchestrator/config/exit_codes/pty/schemas/suites) with import-reusable vs mirror-shape verdict per symbol |
| 2 | pytest/xfail conventions | 02 | COVERED | xfail-absence finding + skip-guard convention + subprocess seam + schema-validation idiom + conftest patterns |
| 3 | git-replay isolation | 03 | COVERED | Live-verified worktree roundtrip + subprocess mock seam + try/finally contract + all 5 commits resolvable |
| 4 | spec contracts (E1-E5 + backtest_status) | 04 | COVERED | Verbatim §3.1 matrix + backtest_status triple-sourced + per-escape §8.3 oracles + E4 HEAD-drift |
| 5 | per-escape replay differential | 05 | COVERED | Per-escape (a)-(e) OLD=MISS / NEW=CATCH characterization for E1-E5 + harness assertion table |
| 6 | impl-tasklist coordination / NEW-gate seam | 06 | COVERED | NEW=CATCH seam RESOLVED (pure-markdown proxy) + collision boundary + skipif strategy |
| 7 | MDTM template + report model | 07 | COVERED | Template 02 PART 1 rules (A-M) + CatchRateReport dataclass tree + schema + suite-vs-pytest decision |

**All 7 sub-systems have actionable, evidenced research. No breadth gap.**

---

## Findings per criterion (lens = completeness/breadth)

### Criterion 1 — Source files identified with paths and exports? → PASS

- **Eval framework API** (01): every module's `__all__` and key symbols cited with `file:line` — `models.py` DM-001..012 with field lists, `run_report.py` (`render_summary_json:233`, `write_aggregated_report:413`, `_write_artifact_set:366`), `loader.py` (`validate_manifest:298`, `SuiteLoader:454`), `exit_codes.py` (4 constants :21-24), `config.py` (`resolve_scratch_root:165`), `schemas/__init__.py` (`load_summary_schema:30`). Import-reusable vs mirror-shape verdict per symbol.
- **Git helpers** (03): `process.py:17` (`import subprocess as _subprocess` seam), `get_git_diff_context:371-393`, `drift.py:262-297` `_git` prior-art, plus the verified absence of any existing `git worktree` Python helper (grep result documented).
- **Report model** (07): full `models.py`/`run_report.py` chain cited line-by-line (`RunSummary:835-946`, `_RUN_SUMMARY_FIELDS:820-832`, `__post_init__:905-921`, `_check_invariant:96-108`).
- **E4 substrate symbols** (04, 05): `_evaluate_gate@executor.py:823/859`, `gate_passed@gates.py:23/94`, `SemanticCheck.advisory@models.py:82-94` — all CODE-VERIFIED.

**Evidence: criterion fully satisfied — paths + exports + line numbers present across all relevant files.**

### Criterion 2 — Output paths/formats clear (tests/troubleshoot/backtest/, catch-rate report JSON + schema)? → PASS

- **Harness location** fixed to `tests/troubleshoot/backtest/**` (06 §D.4), with explicit collision boundary vs impl-owned `tests/troubleshoot/test_*.py`.
- **Report format** (07 PART B): `catch-rate.json` (+ optional `catch-rate.md`) via `render_catch_rate_json` / `write_catch_rate_report`; schema at `src/superclaude/cli/eval/schemas/catch_rate.schema.json` loaded via `load_catch_rate_schema()`. Full `required` field list, `backtest_status` enum, per-escape `verdict` enum CATCH|MISS all specified.
- **Schema placement** (01, 02, 07): `importlib.resources` loader convention + fixtures-dir layout (`tests/troubleshoot/backtest/fixtures/<schema>/` with valid_*/invalid_* JSON).
- **§4.7 src/ vs tests/ placement rule** surfaced (01 §4.7, 04 §5): report MODEL + writer under `src/`, scenario specs + pytest harness under `tests/`.

**Evidence: output destinations and formats are unambiguous.**

### Criterion 3 — Logical breakdown of phases/steps present (research→skeleton→git-replay→per-escape runner→report→pytest)? → PASS

- **07 PART A** maps the build onto Template 02's L-pattern lifecycle: `L1→L2→M3→L3→L5→L4→L6→M3` (TEMPLATE:1002-1027), with each verb bound to a concrete harness step (L1 discovery, L2 build-from-discovery, L3 pytest run, L5 conditional backtest_status, L6 aggregate per-escape results).
- **A4 iterative skeleton** (enumerate-all → one-item-each → consolidate) explicitly mapped onto E1-E5 (07 PART A Section A).
- **04 §5** gives the spec-ordered placement: backtest is M5/step-7 (LAST, after H0-H5 gates exist) — consistent with NFR-1 "predicted until built".
- **02 §6** gives the OLD-green-now vs NEW-skip-guarded file split order.

**Evidence: ordered, multi-source build sequence present.**

### Criterion 4 — Patterns documented with examples (subprocess mock seam, skip-guard, frozen-dataclass report)? → PASS

- **Subprocess mock seam** (02 §4, 03 §1): copy-pasteable `patch("superclaude.cli.sprint.process._subprocess.run")` + `MagicMock(returncode=, stdout=)` with exact call-sites (`test_process.py:399,434,446,453,460,471`).
- **Skip-guard** (02 §2): full `_t0410_missing()` / `_skip_unless_t0410_landed()` exemplar reproduced verbatim from `test_exit_codes.py:92-123`; plus `inspect.getsource` variant for closure branches.
- **Frozen-dataclass report** (07 PART B): complete proposed `EscapeResult` + `CatchRateReport` dataclass tree with `__post_init__` invariant + `_derive_status` + writer + schema.
- **git worktree roundtrip** (03 §3): live-executed and verified, with a ready contextmanager `checkout_worktree` implementation.

**Evidence: every named pattern has a concrete, copyable example.**

### Criterion 5 — MDTM template notes present (02 PART 1 rules)? → PASS

- **07 PART A** is a complete enumeration of Template 02 PART 1 rules grouped A-M with `TEMPLATE:line` citations: A3/A4 granularity, B2 six-element items, C1-C4 embedding, D3 ordering, E1-E4 flat/forward-only, F2a parallel-spawn, I15/I16/I19/I20 QA floors, I18 mandatory L3 test item, I21/M4 fidelity, I22 intensity, L1-L6 verbs, M3/M4 gate sequences, and the PART 2 `## Execution Context` requirement.
- A fully-populated sibling frontmatter example is cited (`…023739.md:1-62`).

**Evidence: PART 1 rules are comprehensively documented — this is the strongest single coverage of the builder's own contract.**

### Criterion 6 — Granularity sufficient for per-escape (E1..E5) + per-component items? → PASS

- **05** gives a self-contained (a)-(e) characterization for EACH of E1-E5 (file/function changed, buggy pre-fix behavior, OLD=MISS observable, NEW=CATCH target, §8.3 confirmation) plus a consolidated per-escape harness assertion table — enough for one checklist item per escape.
- **01/07** give per-component granularity (one item per dataclass/writer/schema/loader/runner-skeleton).
- **A3/A4** (07) explicitly direct "one item per ref/test/harness file, one item per E1-E5 scenario."

**Evidence: granularity supports both the 5 per-escape items and the per-component harness items.**

### Criterion 7 — Doc-sourced claims tagged [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]? → PASS

- **04** is a dedicated cross-validator with an explicit legend and a Cross-Validation Tally. Greenfield gate logic correctly tagged `[UNVERIFIED — EXPECTED]` (H0-H5 gates, 8 output fields, 6 refs, `tests/troubleshoot/` suite, the enum). E4 substrate `[CODE-VERIFIED]`. The narrative state ("E4 fix unmerged") correctly flagged `[CODE-CONTRADICTED]` because the fix landed via sibling commit.
- **03** marks CI-fetch-depth and `--no-checkout` assumptions `[Unverified]`.
- The UNVERIFIED-is-expected-for-greenfield posture is correctly applied — this matches the track goal's explicit note ("NEW gate logic = UNVERIFIED greenfield is expected").

**Evidence: tagging discipline is present and correctly reasoned.**

### Criterion 8 — NEW=CATCH seam resolution: HOW is CATCH asserted given impl artifacts don't exist yet? → PASS (resolved)

This is the highest-risk seam and **06 §B resolves it definitively**:
- The hardening gates are **pure markdown** (`src/.../sc-troubleshoot-protocol/refs/*.md` + SKILL.md) — there is **no importable Python gate function**. Verified on disk (skill dir = SKILL.md + refs/ only, no .py).
- Therefore NEW=CATCH is asserted as a **documentation-presence/content proxy**: assert the NEW ref documents the specific catch mechanism (per-escape mapping given in 06 §B), mirroring the impl's own `tests/skills/` content-assertion pattern.
- Guard = `pytest.mark.skipif` keyed on impl-ref path existence (`pipeline-hardening-closure.md` + `hardening-output-contract.md`), NOT importorskip (nothing importable).
- 07 PART C cross-checks with an in-process angle (parametrized pytest over the built gates) and explains why a suite YAML is the wrong surface. Note a mild framing tension between 06 (markdown-proxy CATCH) and 07 PART C (in-process gate replay) — see Minor observation below — but both converge on "OLD=MISS runs green now; NEW=CATCH is skip-guarded until impl lands," which is the load-bearing answer.

**Evidence: the seam is explicitly resolved with a concrete, guarded assertion mechanism.**

### Criterion 9 — Unresolved ambiguities documented (E4 HEAD-drift, parents[3], backtest_status derivation)? → PASS

- **E4 HEAD-drift** (04 §4.2, 05 E4): `b97c9960` unmerged vs `20693bb8` (the same fix landed on HEAD) is explicitly surfaced as the load-bearing nuance, with both replay options (pre-`20693bb8` tree for a literal negative witness, OR frame E4 as ledger-completeness per §8.3). Coordination with R5 flagged.
- **parents[3]** (02 §3c, 06 §C): reasoned to `parents[3]` for `tests/troubleshoot/backtest/<file>` with explicit "verify at build time via `pyproject.toml` existence assert." The impl's `parents[2]` vs our `parents[3]` depth difference is called out.
- **backtest_status derivation** (04 §2.3, 07 PART B): all-5→complete; 1-4→partial (+ list missing escape IDs); 0/not-run→not_run — triple-sourced from spec §4.5/§5.4/§5.5 and encoded in the `_derive_status` helper.
- **Fix-commit vs parent reading** (03 §4): the "is the listed SHA the fix or the parent" ambiguity flagged and resolved (05 confirms listed = fix, replay `<sha>^`).

**Evidence: every named ambiguity is documented with a resolution path.**

---

## Contradictions / tensions found (surfaced, not resolved)

1. **NEW=CATCH mechanism framing (06 vs 07 PART C).** 06 §B concludes the gate is pure-markdown so NEW=CATCH must be a documentation-presence proxy (`skipif` on ref existence). 07 PART C recommends parametrized pytest that "imports the built H-gate functions and asserts PASS/FAIL." These are not strictly contradictory (07's in-process replay targets the *product* fixes E1-E5, which ARE real Python; 06's markdown-proxy targets the *hardening ref* documentation), but the builder must reconcile WHICH surface NEW=CATCH asserts against. Both agree OLD=MISS is green-now and NEW=CATCH is guarded-until-landed. **Recommend the builder explicitly pick: markdown-presence proxy (06) is the lower-risk, lands-with-refs choice; the in-process gate replay (07) presumes callable gate code that 06 verified does not exist.** Not a blocker — both halves are independently actionable — but the task should state the chosen NEW=CATCH surface to avoid the implementer guessing.

2. **xfail vs skipif (02 vs track goal wording).** Track goal says "NEW=CATCH half may stay skip-guarded"; 02 proves xfail has ZERO occurrences repo-wide and recommends skip. 06 also recommends skipif over xfail. Consistent across research; the builder should use skipif (the established convention), not introduce xfail despite the task title's "xfail" phrasing. Documented, not a gap.

---

## Minor observations (non-blocking)

- 02 header still shows `Status: In Progress` at line 2 but `Status: Complete` at line 275 (the summary is present). The completeness markers (Summary, gaps, takeaways) are all present, so this is a cosmetic frontmatter inconsistency, not a depth gap.
- 04 header line 3 shows `Status: In Progress` but line 225 shows `Status: Complete` with a full Summary. Same cosmetic inconsistency. Both files are substantively complete.
- 07 cites a sibling `research/07-release-spec-structure.md` and `08-v1.1.0-deliverable-reconciliation.md` (from the impl task), not files in THIS task's research dir — these are cross-task references, correctly attributed, not fabrications.

---

## Depth assessment

Expected: research sufficient for a Deep-tier builder to author per-escape + per-component MDTM items.
Actual: **Exceeds.** Each file carries live-verified evidence (03 executed a real git worktree roundtrip; 04/05 re-read pre-fix bodies via `git show <parent>:<file>`; 06 verified on-disk skill state + origin branch absence). The two highest-risk unknowns (NEW=CATCH seam, E4 HEAD-drift) are both explicitly resolved rather than left open. No missing depth elements for the breadth lens.

---

## VERDICT: PASS

All 9 criteria PASS. All 7 sub-systems the builder needs (eval-framework mirror, pytest/xfail conventions, git-replay isolation, spec contracts, per-escape differential, impl-tasklist/NEW-gate seam, MDTM template + report model) have actionable, evidenced, cross-validated research. The two load-bearing risks (NEW=CATCH seam given greenfield impl; E4 advisory bug already healed on HEAD via `20693bb8`) are explicitly surfaced and resolved.

**No breadth gaps. No critical or important gaps.**

### Advisory items for the builder (not gaps — encode as task constraints)
1. State the chosen NEW=CATCH assertion surface explicitly (markdown-presence proxy per 06 §B is the lower-risk choice; reconcile with 07 PART C's in-process framing).
2. Use `skipif` on impl-ref existence (NOT xfail) for the NEW=CATCH half — established repo convention (02 §2, 06 §C).
3. Encode `parents[3]` with a build-time `pyproject.toml` existence assert.
4. For E4, decide pre-`20693bb8` negative-witness replay vs §8.3 ledger-completeness framing (04 §4.2 / §6 item 11).
5. Honor the collision boundary: write ONLY under `tests/troubleshoot/backtest/**`; create parent `tests/troubleshoot/__init__.py` only-if-absent (06 §D).
6. Resolve the cosmetic `Status: In Progress` frontmatter line in research files 02 and 04 (cosmetic only; both are substantively complete).
