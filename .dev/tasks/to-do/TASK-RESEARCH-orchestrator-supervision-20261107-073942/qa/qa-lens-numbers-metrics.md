## Numbers-Metrics QA Report

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Date:** 2026-11-07
**Phase:** report-lens-numbers-metrics (one dimension only)
**Fix authorization:** false (report only; nothing in the report was edited)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | §10 (`:1650`) | Says "`qa/` (24 files)". `qa/` held 43 files at assembly, before any lens report existed, and the 18 Phase 5 synthesis QA files are not listed. This is a false count. | Recount `qa/` at assembly time and state that number. List the synthesis QA files, or say that the list is partial. |
| 2 | IMPORTANT | §7 step 6 (`:1075`), `:935`, [CONTRADICTION] `:1078` | Gives the HOW-WE-WORK "Other commands" range as `:314-337`. The `other-commands` markers are at `HOW-WE-WORK.md:318` and `:337`, and step 1.21 (`:1214`) itself uses `:318`/`:337`. The [CONTRADICTION] marker at `:1078` is real, and the code settles it. | Resolve `:1078` in favour of `:318-337` (Component B). Correct `:935` and `:1075` to `:318-337`. |
| 3 | IMPORTANT | §5 (`:817`) vs §4.8 (`:602`) | `:817` says four external patterns contradict WC-10. `:602` says "Only D1 contradicts WC-10; D3 is naming and D4 an action (synth-03 5.9)". The two counts disagree. | Use one count everywhere. synth-03 5.9 supports one (D1), so change `:817` to say only D1 contradicts WC-10 and the others are naming or action notes. |
| 4 | IMPORTANT | §1 (`:36`), OQ-13 (`:1342`), 98a (`:1561`), step 1.2, step 1.9 / X-7 | The class count is stated inconsistently. `:36` counts fenced among the question's six classes plus idle. `:1342` and `:1561` say the question lists six, without fenced, and that Section C adds fenced as a seventh. Step 1.2 says "seven canonical class names", and steps 1.9 and X-7 say "rules 1-7 plus idle" (eight labels). Section C (`research-notes.md:188-202`) has seven precedence rules plus idle. | Give one count in every place, and say whether idle is included: for example, "seven precedence classes (rules 1-7, fenced is rule 2 at `:194`) plus idle". Correct `:36` so that fenced is the class Section C adds. |
| 5 | IMPORTANT | §6 / §7 option comparison (A1-A4) | Checklist (b): the effort grades (A1 L, A2 M, A3 M-L, A4 M) and risk grades (Medium-low / High / Medium / High) have no sizing basis. They are not tied to the issue's ~40 h total / ~20 h sweep estimate (`issue-summary.md:6`) or to the 29 plan steps (1.1-1.29). The recommendation depends on them. | Add a basis for each grade, such as plan steps, files and tests touched per option, mapped to the issue's ~20 h sweep estimate. Otherwise tag the grades [UNVERIFIED] judgment. |
| 6 | MINOR | §4.3 title | The title says "four known non-critical gaps", but every row (K1-K4) is rated Important. | Retitle it "four known Important gaps (K1-K4)". |
| 7 | MINOR | Section C citations (several places) | The Section C range is cited four different ways: `:188-200`, `:190-202`, `:188-204` and `:194`. `:188-200` leaves out idle (`research-notes.md:202`). | Cite `research-notes.md:184-204` for the whole section, `:192-200` for the rules and `:202` for idle. |
| 8 | MINOR | §4.6 C4 (`:555`), S-09 (`:583`) vs §4.8 (`:597`) | The 72 h default is cited as `SKILL.md:25-27` in one place and `:26` in another. The default is at `:26` (and repeated at `:29`). `:25` is the path line. | Cite `:26` for 72 h and `:25` for the path. |
| 9 | MINOR | `:157`, S-09 (`:583`) | Lists the hardcoded `~/workspace` paths at `SKILL.md:4` and `:53` (S-09 adds `:25-27`). The path also appears at `:25` and `:36`. The count of places is incomplete. | List `:4`, `:25`, `:36` and `:53`. |
| 10 | MINOR | `:1133` vs `:509`, `:1455` | The bootstrap bug lines are given as `:31/:73/:82/:136` in one place and `:31/:73/:136` in the others. | Use one list everywhere, with `:82` either included or explained. |
| 11 | MINOR | `:88`, `:1167`, `:1477` | The capture CLI version is worded three ways: "between 1.4.237 and 1.4.245", "predate 1.4.245" and "Orca CLI 1.4.245 read verbs". | Use one statement, for example "captures predate 1.4.245; verbs verified on 1.4.245". |
| 12 | MINOR | `:900` | Cites `timeout=10` to `reflect/config.py:64-78,103-109`. The timeout is only in `_git` (`:64-78`, at `:76`). `:103-109` is the merge-base fallback, which raises ValueError and sets no timeout. | Cite `reflect/config.py:76`, and describe `:103-109` separately as the raising fallback. |
| 13 | MINOR | §10 vs §8.3 | §10 says web-01 has "14 sources", which matches its 14-row source table. §8.3 attributes about 16 URLs to web-01. | Reconcile §8.3 with the web-01 table, or note which URLs come from outside the table. |
| 14 | MINOR | `:319` | "gaps-and-questions.md:22-70 (GQ-01 to GQ-47)" is a partial range, while GQ IDs run to GQ-100 (`gaps-and-questions.md:125`). It can read as the full log. | Say that this range is partial, or cite the whole log. |
| 15 | MINOR | §3.1 / C10, GQ-99 | Checklist (d): the worst-case cost "ceil(N/100) + N calls" has no per-call time or token cost, and the per-sweep call bound (GQ-99) has no value. It is honestly marked open, so it is not presented as fact, but the cost cannot be quantified. | Add a placeholder that it is unmeasured, plus the probe that will measure it (time one `worker-show` call). |
| 16 | MINOR | §4.6 | The corrections table lists C1-C7, C9 and C13 only. It skips C8, C10-C12, C14 and C15, while other sections cite C1-C15. C10-C12 and C15 are not code-contradicted, but the table gives no note on where they went. | Add one line saying where C8, C10-C12, C14 and C15 are handled (4.2 / 4.8 / 9). |
| 17 | MINOR | §9.2 | The title says "no GQ row", but rows 65 and 74 duplicate GQ-14 and GQ-28. | Remove the two duplicates, or retitle the section. |

### Judged markers (not removed)

- **[CONTRADICTION] `:1078`:** a real numeric contradiction. The code resolves it in favour of `:318-337` (finding 2).
- **[CONTRADICTION] `:1507`:** colon versus space pattern syntax. It has no numeric content and is outside this lens, so no finding.
- **NB-4 exception:** no numeric claim in it. The resolved-row count it causes (Open 75 / Resolved 25) matches `gaps-and-questions.md:125`.
- **6 h window:** presented as the research question's value with an open owner decision (GQ-61, OQ-7). It is sourced to `analyze-worker-contract.md:42` and not stated as an established fact. No finding.
- **~40 h / ~20 h estimates:** sourced to `issue-summary.md:6`. No finding.
- **Code fence `:390-395`:** this is fenced content, and no metric in it was flagged.

### Metrics verified correct

These were checked with `wc -l`, Grep or Read:

- **Line counts:**
  - WORKER-CONTRACT.md: 203
  - crash-recovery SKILL.md: 157
  - bootstrap_scan.sh: 170
  - parse_session_log.py: 128
  - ccsession: 1975
  - test_how_we_work_routing_table.py: 1202
  - HOW-WE-WORK.md: 405
  - test_worker_contract.py: 2265
  - all 10 research files and 6 synthesis files
  - gaps-and-questions.md: 359
  - the report: 1651
- **test_worker_contract.py contents:** 41 `def test_` functions. NEVER_AS_WORKER has 8 entries (`:245-254`).
- **Commands:** 46 command files (47 `.md` files including README), of which 14 set allowed-tools.
- **Other values:**
  - sc-issue-command.md has 20 sections.
  - `ruff==0.15.20` (`pyproject.toml:54`).
  - GQ total is 100 (75 open, 25 resolved), and all 75 open IDs are present in §9.1.
  - `main.py` has 11 `add_command` lines and the `__main__` guard at `:564-565`.
  - The lc16 projection has 16 keys.
  - The scope-01 tally is 54/12/4.
  - The research directory has 10 files (8 codebase, 2 web).

### Summary

- CRITICAL: 0
- IMPORTANT: 5 (findings 1-5: a false file count, three internal count contradictions and unjustified effort/risk grades)
- MINOR: 12 (findings 6-17: citation ranges, wording, partial lists)
- Total: 17

### Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied, so nothing was relied on. Every count above was checked directly.

**(b) Independent semantic checks:**

- `qa/` file count: Glob found 43 files, against the report's 24 (finding 1).
- HOW-WE-WORK markers: Grep found them at `:318` and `:337` (finding 2).
- `reflect/config.py`: Read showed `timeout=10` only in `_git`, at `:64-78` (finding 12).
- The web-01 source table: Read found 14 rows (finding 13).
- The `issue-summary.md:6` and `analyze-worker-contract.md:42` sources for the 40 h and 6 h figures: Read.

Web research: none was needed. No Tavily or WebSearch call was made.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The checklist items were (a) internal consistency, (b) effort and risk basis, (c) size and count metrics and (d) unsourced statistics.

**Tool engagement:** Read: ~18 | Grep: 5 | Glob: 2 | Bash: 2 (one batch, BATCH_OK).

Verdict: FAIL
