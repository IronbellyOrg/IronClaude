# QA Report — Research Gate: Gaps, Depth, Integration, Patterns, Incremental Writing (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339) — read-only coordinator `/sc:sweep`
**Date:** 2026-11-07
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report only; no research file edited)
**Depth tier:** Deep
**Assigned files:** `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/06-orca-open-questions.md`
**Input only:** `research/research-notes.md`
**Checklist items applied:** 6 (gap severity, incl. whether G-B is answered), 7 (depth appropriateness), 8 (integration point coverage), 9 (pattern documentation), 10 (incremental writing compliance)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Pre-review checksums (md5) of the assigned files, re-checked at the end to prove no research file was modified:

- `scope-03-cli-patterns.md` 11ae48052f171505d23a4aa36c80a8f9
- `scope-04-409-layout.md` 924801984e4c13865000ef6ba0d7f456
- `06-orca-open-questions.md` 6997f04c6493272b29fa954b89b19ea0

Gap G-B as defined in the input (`research-notes.md:216`, `:245`, `:303`, `:306`): "no established non-consuming read of pending questions" — the gap-fill file must give "a read-only, non-consuming way to list pending `ask` questions for the needs-person class, or a stated fallback (`agentWait`, `blocked_question`, Ruling halt, frozen plan)". Severity in the notes: Critical.

---

## Verification log (appended as checks run)

### Item 6: gap severity and G-B

Sources checked against 06's citations: `orca orchestration check --help` (:3-8, :24, :28, :35-37), `ask --help` (:16, :23-24), `reply --help` (:3, :5), `inbox --help` (:3, :5), the bundled orchestration guide (:113, :130-135, :140) and messaging guide (:12-19, :26-27, :49-53, :60-70), and `WORKER-CONTRACT.md` lines 30, 45, 52-58, 61-62, 133-136. Every quote 06 cites from these matched the source text.

- **Consumption question: answered.** 06 Q2 table (06:55-63) and "Consequence" (06:69-74) say plain `check`/`check --wait` is the consuming mode, `--ack` drains, and `--peek`/`--all` are documented as non-marking. The help agrees (`check` :4-7, :37; messaging guide :17-19, :26-27). 06 correctly tags read-marking by plain `check` as [UNVERIFIED] (06:55, gap 1) and says nothing was exercised live (06:15, gap 2).
- **Pending-question enumeration: not answered, and one claim overreaches.** Questions land in the Run mailbox `run:<id>` (messaging guide :49-53; 06:19, :42). `check --all` is documented as "return every message for the handle" (`check` :7), i.e. scoped to the caller's handle; only "a Run --peek" is named as Run-scoped (`check` :37), and `--peek` returns only unread rows (`check` :6). 06:73 states "only `--all` can show it" for a read-but-unreplied question without tagging the premise that `--all` reaches the `run:<id>` mailbox. Whether `check --all --run <id>` lists the Run mailbox is not stated in any cited help line, and it is absent from 06's 16-item gap list (06:155-170; the only `--run` mentions concern `reply` and `worker-list`, 06:27, :93, :151). 06 also does not say whether the 100-row cap (gap 7) keeps the oldest or the newest rows, which decides whether a long-running Run's open questions are inside the window at all. A synthesis reading 06 could present `check --all` as a working non-consuming question list. Graded IMPORTANT (finding 1).
- **Fallbacks:** 06 Q4 (06:124-142) carries the contract-based fallbacks the G-B definition lists (`agentWait`, WC-3 `blocked_question`, frozen plan at `WORKER-CONTRACT.md:133-136`), each correctly cited. They are not explicitly named as THE answer to G-B when Orca enumeration is unproven; the synthesis must make that link (folded into finding 1's fix).
- Other 06 gaps (3, 4, 6, 8-14) are honestly tagged [UNVERIFIED] and lower-impact for a read-only report. Gap 15 (`--format` contradiction, `check` :28 vs :36) verified and correctly tagged [CODE-CONTRADICTED].
- 06 Q1 (06:19-45) frames pending `ask` questions under the needs-person class, but an `ask` waits on the coordinator agent's `check --wait` + `reply` (orchestration guide :133-135, :140), not a person; only escalations a coordinator cannot settle reach a person. MINOR (finding 2).
- `gate-create` / `gate-resolve` / `gate-list --task` (messaging guide :65-70) are a documented pending-decision surface; 06 never evaluates `gate-list` as a read-only source for decisions waiting. MINOR (finding 3).
- scope-03 gaps (scope-03:188-200) and scope-04 gaps (scope-04:71-74, :93, :129): all tagged; none blocks synthesis.

### Item 8: integration points

- `src/superclaude/cli/main.py:513-565` read: deferred import + `main.add_command(...)` pairs for sprint (519/521) through reflect (559/561), `__main__` guard 564-565. scope-03's registration recipe matches.
- `tests/cli/test_cli_registration.py`: `EXPECTED_TOP_LEVEL_COMMANDS` at :31-49 is used only at :102 in a `--help` loop (grep of `EXPECTED_TOP_LEVEL_COMMANDS|main\.commands` in tests: only :31, :102, plus per-group checks in `tests/swarm/test_cli_registration.py:74-95` and `tests/test_cleanup_audit_structure.py:160`). Subset check, so adding `sweep` does not break it, as scope-03 says.
- `tests/recommend/test_routing_refresh.py:33` `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` and :647-648 `shipped - _POST_REFRESH_ADDITIONS == active` verified; scope-03's statement that a new shipped command must be reflected there is correct.
- `tests/core/test_how_we_work_routing_table.py:27-40` (`_OTHER_COMMANDS`, 12 entries) and :291-311 (membership test, excluded set :299-309) verified against scope-03:137 and :192.
- `src/superclaude/commands/README.md:10` step 4 reads "add its row to the routing table at the end of `src/superclaude/core/HOW-WE-WORK.md` (or to its "Other commands" table)". scope-03:137 and :192 say step 4 requires a row in "Other commands" and frame the choice as Other-commands vs excluded set; the routing-table option and the routing-table tests it would trigger (test_how_we_work_routing_table.py:186-259, :314-340) are not analysed. MINOR (finding 4).
- Command-file globs not listed by scope-03: `tests/skills/test_worker_contract.py:464-472` requires the set of command files with a `^## Unattended mode` section to equal `UNATTENDED_COMMANDS` (:379), and :476/:519 apply `_ORCA_NAME_RE` to those sections; `tests/skills/test_model_alias_policy.py:86` scans command frontmatter `model:`. Both bite only if `sweep.md` gains an unattended section or a `model:` field; a sweep command that calls Orca is a likely candidate for the first. MINOR (finding 5).
- Plugin parity (`tests/commands/test_routing_plugin_parity.py:29-38`), the CLAUDE.md level-table copy rule, `recommend.md:52-58` Activation block, `issue.md` section skeleton, `docs/user-guide/commands.md:115` and `:347`: verified. No `src/superclaude/cli/sweep/` exists yet, consistent with scope-03.
- #409 layout (scope-04): header (canvas.py:73-77), footer (:78-81), Attention Ledger, Shift Brief, data dictionary, fixtures (fixtures.py:11-111) and the [CODE-CONTRADICTED] sort finding (scope-04:93) are documented with path:line; the fixture-metrics-to-header link is explicit (scope-04:41-74).

### Item 7: depth (Deep tier)

- scope-04 traces fixture record -> `metrics()` derived counts -> `header()`/`footer()` text -> rendered export (`agent-focus/exports/116/attention-ledger.txt:41-42`), scope-04:41-74. End-to-end.
- 06 traces worker `ask` -> `run:<id>` mailbox -> coordinator `check --wait --types ...question` -> `reply --id`, with timeout resume (06:19-28, :42). End-to-end at the documented level (not exercised).
- At least one file traces a complete flow. PASS.

### Item 9: patterns

- scope-03 documents the naming and registration convention; the single subprocess seam `_git(cwd, *args)` (reflect/config.py:64-78) with fail-closed `(OSError, subprocess.SubprocessError)` handling (config.py:103-109, :151-152, :182-183); `CliRunner` tests against the live root group (tests/recommend/test_cli_registration.py:1-39); the read-only proof via `side_effect=AssertionError` inside `CliRunner.isolated_filesystem()` (tests/cli/reflect/test_contract_status_cli.py:18-22, :44-66); the subprocess-free pure classifier (scope-03:195). scope-04 documents the header/freshness and "seen is not resolved" conventions. PASS.

### Item 10: incremental writing

- scope-03 carries per-row "(re-verified 2026-11-07)" stamps (scope-03:17-28) and a line-range column showing partial reads (scope-03:35); scope-04 carries per-file line counts and section-by-section [CODE-VERIFIED] tags. Both show iterative build-up.
- 06 has uniform structure (Q1-Q5 answer/evidence/consequence blocks, summary table, gap list) and no iteration or re-verification markers; it reads as one pass. Its citations all checked out, so no data loss is evident. MINOR (finding 6).

### Integrity re-check

md5 after review: scope-03 11ae48052f171505d23a4aa36c80a8f9, scope-04 924801984e4c13865000ef6ba0d7f456, 06 6997f04c6493272b29fa954b89b19ea0. Identical to the pre-review values: no research file was modified.

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 6 | Gap severity (incl. G-B) | FAIL | G-B consumption half answered (06:55-63, :69-74 vs `check --help` :4-7, :37); enumeration half not answered: `--all` is handle-scoped (`check` :7) while questions go to `run:<id>` (messaging guide :49-53), 06:73 relies on it untagged, and the gap list (06:155-170) omits it. 1 IMPORTANT, 2 MINOR. |
| 7 | Depth appropriateness (Deep) | PASS | scope-04:41-74 fixture -> metrics -> header -> export; 06:19-28, :42 ask -> `run:<id>` -> `check --wait` -> `reply`. |
| 8 | Integration point coverage | PASS (with notes) | main.py:513-565; test_cli_registration.py:31-49, :102; test_routing_refresh.py:33, :647-648; test_how_we_work_routing_table.py:27-40, :291-311; README.md:10; test_worker_contract.py:379, :464-476, :519; test_model_alias_policy.py:86. 2 MINOR. |
| 9 | Pattern documentation | PASS | scope-03:80-99, :195 against reflect/config.py:64-78, tests/cli/reflect/test_contract_status_cli.py:18-22, :44-66. |
| 10 | Incremental writing compliance | PASS (with notes) | scope-03:17-35 re-verified stamps; 06 shows no iteration markers. 1 MINOR. |

## Summary

- Checks passed: 4 / 5 (two with notes)
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 5
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `research/06-orca-open-questions.md` Q2 table (:55-63), "Consequence for a read-only sweep" (:69-74, esp. :73), Gaps list (:155-170) | G-B is only half answered. Consumption is settled from help text, but no non-consuming way to list pending questions is established: `check --all` is documented as "every message for the handle" (`check --help` :7), questions are delivered to the Run mailbox `run:<id>` (messaging guide :49-53), the only Run-scoped non-consuming read is `--peek`, which hides already-read rows (`check` :6, :37). 06:73 ("only `--all` can show it") rests on the untagged premise that `--all` reads the Run mailbox; the gap list omits both that question and which end of the 100-row cap is kept. Nothing was exercised live. | Add a gap: "Whether `check --all` (with or without `--run <id>`) returns the `run:<id>` mailbox rows, and whether the 100-row cap keeps oldest or newest rows" [UNVERIFIED], and tag 06:73 [UNVERIFIED]. Either resolve it by reading the check handler under `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/` (read-only) or a throwaway-Run test run by the user, or state explicitly that the sweep reports Orca question enumeration as "could not determine" and uses the contract fallbacks of 06 Q4 (WC-3 `blocked_question`, `agentWait`, frozen plan at `WORKER-CONTRACT.md:133-136`) as the G-B answer. |
| 2 | MINOR | 06 Q1 (:19-45) | Pending `ask` questions wait on the coordinator agent (`check --wait` + `reply`, orchestration guide :133-135, :140), not a person; 06 files them under the needs-person class. | Note that `ask` questions are coordinator-owned and only unresolved escalations become needs-person. |
| 3 | MINOR | 06 (whole file) | `gate-list --task` (messaging guide :65-70) is a documented pending-decision surface and is not assessed as a read-only source. | Add a line on whether `gate-list` is read-only and useful to the sweep, or why it is excluded. |
| 4 | MINOR | `research/scope-03-cli-patterns.md` registries item 3 (:137) and open question 2 (:192) | `commands/README.md:10` step 4 allows the routing table OR "Other commands"; scope-03 says "Other commands" is required and does not analyse the routing-table option or its tests (test_how_we_work_routing_table.py:186-259, :314-340). | Quote step 4 exactly and list the routing-table option among the choices. |
| 5 | MINOR | scope-03 registries list (:130-140) | Omits two command-file globs: `tests/skills/test_worker_contract.py:464-472` (`## Unattended mode` set must equal `UNATTENDED_COMMANDS`, :379; Orca-name regex :476, :519) and `tests/skills/test_model_alias_policy.py:86` (frontmatter `model:`). | Add both as conditional registries (triggered if `sweep.md` gets an unattended section or a `model:` field). |
| 6 | MINOR | 06 (structure) | No iteration or re-verification markers; reads as one-shot. Citations verified, so no evident loss. | None required; future gap-fill files should carry re-verification stamps like scope-03. |

## Actions Taken

None. Fix authorization is false; no research file was edited (md5 unchanged, see Integrity re-check).

## Recommendations

- Resolve finding 1 before synthesis (gap-fill on 06, or an explicit "could not determine" plus contract-fallback ruling recorded in research-notes).
- Synthesis must keep 06's [UNVERIFIED] tags on every Orca read mode and must not describe `check --all` as a pending-question list.
- MINOR findings 2-6 are notes; fold them in if 06 or scope-03 is reopened for finding 1.

## Confidence and tool engagement

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 9 | Glob: 1 | Bash: 10 (read-only `--help` captures, `sed -n` line checks, `md5sum`; no state-changing Orca, ccsession, sweep or close command). No web research performed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- UNCHECKED items: none. UNVERIFIABLE items: none (live Orca behaviour is out of scope for a read-only QA pass and is itself the subject of finding 1).

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

## QA Complete

## Verdict: FAIL

