# Research: C8 / DEFECT-CANDIDATE reconciliation across research files 01-06 (GF-1)
**Investigation type:** Doc Analyst
**Scope:** the six research files in research/; origin/master SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`; snapshot `docs/designs/orchestrator-mode.md` (lines 493, 636, 841, 877); snapshot CHANGELOG.md:170 and docs/user-guide/commands.md:619-620; snapshot cli/sweep/classify.py and models.py
**Status:** Complete
**Date:** 2026-11-20
---

Paths. SNAPSHOT = `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6, confirmed by `git log -1 origin/master`). SPEC = `origin/master:.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`, read through `git show ... | cat -n` only (no scratch copy written anywhere). DESIGN = `SNAPSHOT/docs/designs/orchestrator-mode.md`. ORCH = `SNAPSHOT/docs/designs/orchestrator.md`. Code lives under `SNAPSHOT/src/superclaude/cli/sweep/` (the brief's "cli/sweep/..." path). Nothing was run. This file states facts and one labelling rule; it does not recommend how Clay's orchestrator design is unified with these tools.

## 1. Verified source text (what the labels rest on)

### 1.1 SPEC lines (read this pass; line numbers are `cat -n` of the origin/master blob)

- SPEC:106 (FR-012): "Safe-to-close is a separate two-part REVIEW value (terminal, worktree), each `yes`, `no` or `could not determine`. Phase 1 never prints `worktree removable: yes`."
- SPEC:103 (FR-009): "Stalled (proved) only from Orca's own exit proof with no `worker_done` and no fencing evidence ..."; its acceptance is two fixture cases, not a live case.
- SPEC:111 and :167: `safe_to_close` "never yes in Phase 1".
- SPEC:231: `fenced_evidence: str` is "`present`, `absent` or `unreadable`; always `unreadable` on live rows in Phase 1, REPORT step 1.3 rule 3".
- SPEC:232: "`worker_done_seen` is None on live rows, because no named live source establishes its absence. Stalled (proved) stays fixture-only until a source mapping exists. Missing proof never becomes False. [V1R3:41, V2R3:43, V3R3:52; INV-006; Change 10]". The phrase "source mapping" occurs nowhere else in the SPEC (grep over the blob: one hit, line 232).
- SPEC:238: "Waiting (a) age is `now - t`, where `t` is the earliest of the contract file's `st_mtime` for a blocked contract and the `agentWait` timestamp field captured in step 1.0a (UNVERIFIED field). With no `t`, the row is in the unknown-age group. [SP-15]".
- SPEC:251 (rule 3 `fenced`): "`fenced_evidence == "present"` (synthetic fixtures only in Phase 1)".
- SPEC:274: terminal releasable needs `reclaimable`, `release` and the result already read; "the read is not observable, so Phase 1 prints `could not determine (result read not observable)` plus the Orca values; `retained` is never releasable. Worktree removable prints `no` with the first observed condition from FR-013, else `could not determine (report read, open PR and unmerged commits not observable)`."
- SPEC:338: "Unmerged commits and open PRs are not observed in Phase 1; that is acceptable because worktree removable is never `yes` (FR-012)."
- SPEC:75 and :208 (B3): Phase 2 `/sc:close` "Act on safe-to-close REVIEW rows after the person confirms" and must re-collect before acting. This is the only place the SPEC names a later phase for acting on Safe to close.

### 1.2 DESIGN lines (Read this pass)

- DESIGN:493 (Rule 5, SP-24): four-condition rule 5; restored 2026-11-16 from a read-only capture (`q24-orca-capture2-20261116.md`); "A non-null `agentWait` was never captured, so what it looks like and what it means are UNVERIFIED; such a row is taken by rule 4 ... and is never `working`"; "`worker_done_seen` is None on every live row; `fenced_evidence` is `unreadable` on every live row (SPEC line 231)."
- DESIGN:494: a waiting timestamp later than `now` is unknown age (SP-26, D5). DESIGN:649: waiting (a) rows "oldest first, then rows of unknown age".
- DESIGN:636 (report footnote text): "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred. (SP-24, D7)".
- DESIGN:841 (deviation table row D7): "the report adds the footnote that stalled and fenced are not observed in Phase 1 and a zero count does not mean none occurred. Update 2026-11-16: ... Rule 5 is active. The footnote covers stalled and fenced only ... What a non-null `agentWait` means stays UNVERIFIED". Source SP-24, applied in 7.2 and 7.5.
- DESIGN:877 (panel-notes row): "SP-24 | Applied as D7; Rule 5 restored with the captured names on 2026-11-16".
- DESIGN:1003 (open item 6): resolved 2026-11-16 for a running worker; "Still UNVERIFIED: what a non-null `agentWait` looks like and means".
- DESIGN:794-795: traceability rows FR-012 (`safe_to_close`; `worktree` never `yes`) and FR-013 (`removable` with the named condition).
- D7 location correction (GF-1): research file 04 "Stale Documentation Found" item 2 and Gaps item 1 cite `origin/master:.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md:813`. That is a real, different file: line 813 of that blob is the D7 row (checked with `git show ... | cat -n`). The shipped design file in the snapshot has the D7 row at **DESIGN:841**, not :813 (snapshot DESIGN:813 is a different row, as 04 itself notes). So 04's citation is accurate for design-base.md and must not be read as a line of the snapshot design; the snapshot citations for D7 are :841 (row), :636 (footnote text), :877 (panel-notes row).

### 1.3 Code (SNAPSHOT/src/superclaude/cli/sweep/)

- `models.py:108-109`: `worker_done_seen: bool | None = None`; `fenced_evidence: str = "unreadable"`. `models.py:111-112`: comment "Reserved: the agentWait time. No code sets it: no captured field names a wait time." and `agent_wait_since: datetime | None = None`. `models.py:100-101`: `agent_wait`, `agent_wait_present`. `models.py:71`: `SAFE_VALUES = ("yes","no","could not determine")`.
- `classify.py:191-208` `_exit_proof` (rule 2): matches only with `liveness_verdict == "exited"`, `worker_done_seen is False`, `fenced_evidence == "absent"` and `transcript_readable is not False` (:196-200); otherwise declines and attaches `NOTE_EXITED_UNREADABLE` when `fenced_evidence == "unreadable"` or `transcript_readable is False` (:205-208).
- `classify.py:219-223` `_rule_fenced` needs `fenced_evidence == "present"`.
- `classify.py:226-236` `_rule_waiting_signal`: any non-null `agent_wait` gives waiting (a); `since = orca.agent_wait_since  # reserved: no captured field names a wait time` (:229).
- `classify.py:251-269` `_rule_working`: four conditions of DESIGN 7.2 (so `working` is produced from live data; this matters for the stale-doc note in 3.2).
- `classify.py:479-504` `safe_to_close`: no branch returns `"yes"`; the `reclaimable` + `release` branch returns `could not determine` with "result read not observable" (:491-493). `classify.py:88-90` `REASON_NOT_OBSERVABLE = "report read, open PR and unmerged commits not observable"`.
- `probes.py:458-468` `_agent_wait`; `probes.py:471-515` `parse_worker_show`: sets `agent_wait`, `agent_wait_present` (:493-494) and never sets `worker_done_seen`, `fenced_evidence` or `agent_wait_since` (:481 comment "stays unset: no captured field names a wait time"). Grep over the whole snapshot for `worker_done_seen|fenced_evidence|agent_wait_since` finds only: DESIGN, `classify.py`, `models.py`, `probes.py` (comments only for `agent_wait_since`), `report.py` and three test files. So the only producers of `worker_done_seen=False`, `fenced_evidence="absent"/"present"` and a non-None `agent_wait_since` are test fixtures (`tests/sweep/test_classify.py:300-301, 308, 314, 383-386, 589-639, 699, 766-767`; `tests/sweep/test_report.py:308, 715-730`); `tests/sweep/test_probes_allowlist.py:1651, 1687` assert `agent_wait_since is None` after parsing.
- `report.py:120-133` `_wait_age_s`: takes the earlier of a blocked contract's `mtime` and `orca.agent_wait_since` when `agent_wait` is non-null; returns None when neither is known. So a waiting (a) row from a blocked contract has an age (contract mtime); a waiting (a) row from `agentWait` alone has unknown age in production.
- `report.py:42-49`: `SP24_LINE` and `SAFE_TO_CLOSE_LINE` ("Safe to close never prints yes in Phase 1 ...").

### 1.4 Public statements

- `CHANGELOG.md:170` (under `#### Known limits (sweep, Phase 1)`; the last `## ` heading above it is `## [6.0.0] - 2026-11-18` at line 69): "The classes `stalled (proved)` and `fenced` are never observed, and `working` is never produced, because the live `agentWait` names were never captured (design open item 6). Healthy workers read `could not determine`." `CHANGELOG.md:171`: "`Safe to close` and `Removable` never say `yes`; remote hosts are never scanned; totals are a lower bound."
- `docs/user-guide/commands.md:619`: "The classes `stalled (proved)` and `fenced` are never observed in Phase 1, so a zero there means nothing. The counts carry the mark `(not observed in Phase 1)`." (no reason given). `:620`: "The class `working` is never produced yet, because the live names of Orca's `agentWait` field were never captured. Healthy workers read `could not determine`, and a waiting-on-a-person row from an agent wait cannot match on live data. Rows waiting because of a blocked contract or a frozen plan still work." `:621`: "`Safe to close` and `Removable` never say `yes`."

Key Takeaways
- Every sweep limit in the brief has a specific SPEC line (231, 232, 238, 251, 274, 338, FR-012 at 106) and the design carries stalled/fenced into 493, 636, 841 and 877.
- The only producers of the inputs for stalled, fenced and a wait time are test fixtures; `parse_worker_show` never sets them.
- 04's `design-base.md:813` and the snapshot's `docs/designs/orchestrator-mode.md:841` are the same D7 row in two different files; the snapshot citation is :841.

<!-- END S1 -->

## 2. The single rule (applied to every item below, in all six research files)

**Rule R-C8.** A capability that a spec, design, skill, command or user doc names as shipped, enabled or required, and that has no producer, writer or reachable path at its runtime entrypoint, is labelled by one test:

1. If a cited spec-level or design-level text states, for that specific capability, that the shipped build does not deliver it (it names it deferred, fixture-only, not observed, not observable, UNVERIFIED with a stated fallback outcome, or assigns it to a named later piece of work), the label is **KNOWN LIMIT (cited)**. The citation is printed with the label. A report footnote, a CHANGELOG line or a user-guide line shows the limit is disclosed to users; by itself it is not the scope decision.
2. If no such text exists, the label is **DEFECT-CANDIDATE**. A text that only records the absence ("not built", "cannot run as written", "UNVERIFIED") without stating that the build is meant not to deliver the capability does not meet step 1.
3. Either label carries the residual owner facts that the citation does not settle (who owns an "until" condition, whether the cited text is a dated owner ruling or a spec/review-input statement). Residual facts never change the label.
4. "Remediation task not created (read-only brief); flagged for the owner" is printed on every DEFECT-CANDIDATE and on every KNOWN LIMIT whose cited text has no tracked owner for its "until" condition.

Why this rule and not 04's: research file 03 section 8 applied step 1 and found a cited decision for each sweep item. Research file 04 applied "an owner decision declaring the capability out of scope" (a stricter test than step 1) to the same three items and labelled them DEFECT-CANDIDATE although it cited the same D7 and design:493 text. The two files cannot both stand. R-C8 uses 03's test because the brief for this task (the C8 sentence "without an on-record, cited scope decision") asks for a cited scope decision, not for a dated owner ruling; 03 point 2 (below, 3.1) records that the sweep decision is attributed to review inputs and not to a dated owner ruling, which is a residual fact under step 3.

Key Takeaways
- One test decides all items: a cited text, specific to the capability, saying the build does not deliver it.
- The test turns on the existence of such text, not on its authority level; authority level is carried as a residual fact.

## 3. Determinations

### 3.1 stalled (proved), rule 2 `orca_exit_proof`

- Label: **KNOWN LIMIT (cited)**. Replaces 04 section 5 row "Stalled (proved) class", 04 Gaps item 1 and 04 Summary (all say DEFECT-CANDIDATE). Agrees with 03 section 8.1.
- Rule applied: R-C8 step 1.
- Cited decision: SPEC:232 ("Stalled (proved) stays fixture-only until a source mapping exists"), SPEC:231, SPEC:103 (acceptance is fixture cases); carried to DESIGN:493, DESIGN:636, DESIGN:841 (D7) and DESIGN:877 (SP-24).
- Code evidence it cannot fire on live data: `models.py:108-109` defaults; `probes.py:471-515` never sets the fields; `classify.py:196-200` needs `False` and `"absent"`. Fixture-only reach: `tests/sweep/test_classify.py:300-301, 599-614, 766-767`.
- Observable effect on live rows: an exited worker gets `could not determine` plus the note `Orca: exited; fenced evidence not readable` (`classify.py:205-208`), as SPEC:250 describes.
- Residual owner facts (statements of fact): (a) no work item owns the "source mapping" of SPEC:232: the phrase appears once in the SPEC; 03 8.1 point 1 reports `gh search issues --repo IronbellyOrg/IronClaude "worker_done_seen"` and `"sweep stalled fenced"` returned nothing (a search, not a scan) and issue #534 does not name stalled or fenced; (b) the decision is attributed to review inputs (V1R3, V2R3, V3R3, INV-006, Change 10), not to a dated owner ruling; (c) the reason on the SPEC ("no named live source establishes its absence") differs from the reason in `CHANGELOG.md:170` (see 3.6). Remediation task not created (read-only brief); flagged for the owner.

### 3.2 fenced, rule 3

- Label: **KNOWN LIMIT (cited)**. Replaces 04 section 5 row "Fenced class", 04 Gaps item 1, 04 Summary. Agrees with 03 section 8.2.
- Rule applied: R-C8 step 1.
- Cited decision: SPEC:251 ("`fenced_evidence == "present"` (synthetic fixtures only in Phase 1)"), SPEC:231 ("always `unreadable` on live rows in Phase 1"); DESIGN:493, :636, :841, :877.
- Code evidence: `models.py:109` default `"unreadable"`; `classify.py:221` needs `"present"`; no producer (1.3). Fixture-only reach: `tests/sweep/test_classify.py:308`, `tests/sweep/test_report.py:353`.
- Residual owner facts: unlike stalled, SPEC:231 and :251 give no "until" condition, so there is no named future source for fenced; the same attribution fact as 3.1(b). WC-16 (`WORKER-CONTRACT.md:289`) names the stalled behaviour and not `fenced` (03 8.1). Remediation task not created (read-only brief); flagged for the owner.

### 3.3 `agent_wait_since`

- Label: **KNOWN LIMIT (cited)**. Replaces 04 section 5 "second note", 04 Gaps item 2 ("DEFECT-CANDIDATE (low)") and the 04 Summary clause. Agrees with 03 section 8.5.
- Rule applied: R-C8 step 1. The SPEC text is SPEC:238: the `agentWait` timestamp field is "captured in step 1.0a (UNVERIFIED field). With no `t`, the row is in the unknown-age group." That names the capability's input as UNVERIFIED and states the outcome when it is missing, which is step 1's "UNVERIFIED with a stated fallback outcome". Supporting design text: DESIGN:493 and :1003 (item 6: what a non-null `agentWait` looks like and means is still UNVERIFIED), DESIGN:494 and :649 (unknown-age group).
- Code evidence: field exists (`models.py:111-112`, comment "Reserved ... No code sets it"), is read (`classify.py:229-235`, `report.py:127-128`), and is never set (`probes.py:481`); `tests/sweep/test_probes_allowlist.py:1651, 1687` pin `is None`. Effect: a waiting (a) row from a non-null `agentWait` with no blocked contract has unknown age (`report.py:130-131`); a waiting (a) row from a blocked contract has an age from the contract mtime (`report.py:125-126`).
- Note on 04's reasoning: 04 wrote "no cited decision names the wait time as out of scope"; it did not cite SPEC:238, which it never read (04 reads no SPEC; GF-1 evidence). SPEC:238 is the text.
- Residual owner facts: the 2026-11-16 capture recorded `agentWait` present and null for a running worker only (`classify.py:251-256` comment; DESIGN:493); no capture of a non-null value exists, so no field is known to carry a wait time and rule 4(a) has not been shown to fire on live data. Remediation task not created (read-only brief); flagged for the owner.

### 3.4 Safe to close

- Label: **KNOWN LIMIT (cited)**. Agrees with 03 section 8.3 and 04 section 5 row "Safe to close".
- Rule applied: R-C8 step 1.
- Cited decision: SPEC:106 (FR-012), SPEC:111 and :167 (never yes in Phase 1), SPEC:274 (terminal: `could not determine (result read not observable)`; the read "is not observable"); DESIGN:794 (traceability row FR-012). The only later-phase named is Phase 2 `/sc:close` (SPEC:75, :208), which acts on these rows; the SPEC does not state that Phase 2 will add a `yes` source.
- Code evidence: `classify.py:479-504`, no branch returns `"yes"`; `:491-493` the closest branch returns `could not determine`; `models.py:71` lists `yes` as a legal value; pinned at `tests/sweep/test_classify.py:246-248` and `:1613-1633`, `tests/sweep/test_report.py:1172`, `tests/sweep/test_cli_contract.py:1038`.
- Residual owner facts: only the report footnote (`report.py:46-49`), `CHANGELOG.md:171` and `commands.md:621` say "never yes"; `commands/sweep.md:16` and `SKILL.md:66` name `Safe to close` without that statement (03 8.3).

### 3.5 Removable

- Label: **KNOWN LIMIT (cited)**. Agrees with 03 section 8.4 and 04 section 5 row "Removable".
- Rule applied: R-C8 step 1.
- Cited decision: SPEC:106 (FR-012), SPEC:274 (worktree removable prints `no` plus the first FR-013 condition, else `could not determine (report read, open PR and unmerged commits not observable)`), SPEC:338 (unmerged commits and open PRs "are not observed in Phase 1; that is acceptable because worktree removable is never `yes`"); DESIGN:795 (FR-013 row).
- Code evidence: `classify.py:455-476` `removable` returns only `no` or `could not determine`; `classify.py:88-90` constant reason; `models.py:208` default `"could not determine"`; tests `test_classify.py:247-248, 1679-1695`.
- Residual owner facts: the missing sources are named in SPEC:338 (`git log`, `git branch`, `git rev-parse`, `gh` reads excluded); no later piece of work that adds them is named.

### 3.6 Public wording of the stalled/fenced/working reason (CHANGELOG.md:170, commands.md:619-620)

This is GF-2's subject; the facts are stated here only because the brief names these lines.
- `CHANGELOG.md:170` is the only line that gives a reason covering all three of `stalled (proved)`, `fenced` and `working`: "because the live `agentWait` names were never captured (design open item 6)". For `stalled` and `fenced` that reason does not match SPEC:232 ("no named live source establishes its absence") and SPEC:231/251. For `working` the statement is out of date: design open item 6 is resolved for a running worker on 2026-11-16 (DESIGN:1003), Rule 5 is active (DESIGN:493, :841) and `classify.py:251-269` produces `working`. The CHANGELOG section it sits in is `## [6.0.0] - 2026-11-18`. **[STALE DOC]** (reason misattributed for stalled/fenced; `working` and "Healthy workers read `could not determine`" no longer true on live data).
- `docs/user-guide/commands.md:619` gives no reason for stalled/fenced (it states only "never observed in Phase 1" and the mark). `:620` gives the `agentWait`-capture reason, for `working` only; that sentence is **[STALE DOC]** for the same 2026-11-16 reason, except its second half ("a waiting-on-a-person row from an agent wait cannot match on live data"), which is still consistent with DESIGN:493 (a non-null `agentWait` was never captured). So the claim in research file 03 that commands.md:619-620 gives the capture gap as the reason for stalled/fenced is narrowed to `CHANGELOG.md:170` alone.

### 3.7 Living-report entry writer (research file 05)

- Label: **KNOWN LIMIT (cited), sequenced to PR B**. Replaces the DEFECT-CANDIDATE label on 05 Gaps item 1 (05 text at lines 317 and 578). 05's own wording leaves the question open ("whether it counts ... is for the owner"); R-C8 settles it as below.
- Rule applied: R-C8 step 1 (assigns the capability to a named later piece of work).
- Cited decision: ORCH line 3 (design "approved by the owner (Clay) on 2026-11-19 ... (ruling 37)"); ORCH:510 (`src/superclaude/cli/orchestrator/` is "package, new, PR B" and its verbs include `report-entry`); ORCH:791 ("the report entry is written only by the verb `superclaude orchestrator report-entry`"); ORCH:1020 (PR B row lists `src/superclaude/cli/orchestrator/` and its registration in `main.py`); ORCH:1021 (PR C row moves `agent-work-report` with `exclude.py` and `run.py refresh`, the reader side); ORCH:1041 (PR B waits for PR A and PR P); ORCH:1013 (`enabled: false` stays).
- Code evidence of the gap: no code outside tests writes `orchestrated/*.json`; `superclaude orchestrator` is absent from `SNAPSHOT/src/superclaude/cli/` (directory listing: no `orchestrator` entry; `main.py` has no match, 05 section 15); `refs/settle.md:99` of `sc-closeout-protocol` says "The command does not exist in this repository, so the entry item is `escalated why=surface_absent` until it does." PR state at the snapshot (05 section 18, `gh` read-only): PR C (#684, reader side) merged 2026-11-20T02:01:07Z and is in the snapshot (`exclude.py` exists); PR A (#686) and PR P (#690) open; PR B: no PR found by three searches.
- Residual owner facts: (a) `agent-work-report/SKILL.md:14-16` and `:115-116` describe the entry files and `exclude.py` in the present tense ("The orchestrator keeps one entry file per issue it holds") while the writer does not exist; as a statement of current state that text is **[CODE-CONTRADICTED]** by the missing verb, although the cited design places the writer in the unmerged PR B; (b) ORCH states no interim behaviour for the shared page between PR C and PR B (grep of ORCH for "until PR B", "before PR B", "without PR B": no hit); the observed interim behaviour is 05 section 15 (`exclude.py` excludes nothing; `refresh` renders no "Held by the orchestrator" block); (c) the decision is a PR-sequencing line, not a statement that the writer is out of scope; if the owner holds that a sequencing line is not a scope decision, this label becomes DEFECT-CANDIDATE with no change to any fact above. Remediation task not created (read-only brief); flagged for the owner.
- Same test applied to the other two 05 items (outside the requested list; stated so the standard is even): 05 Gaps item 3 (`orchestrator_repo` rejected by the master poll) meets step 1: ORCH:372 and :374 (`cycle.py` `_TOP_KEYS` and `Config` reshaped to add `orchestrator_repo`) place it in the `issue_watch` work of PR A (ORCH:1018), PR A (#686) is open (05 section 19); label KNOWN LIMIT (cited), sequenced to PR A, and the **[CODE-CONTRADICTED]** tag on SKILL.md:14 stands until PR A merges. 05 Gaps item 2 (a "Needs you" session entry cannot be answered because `prefs.check_url` accepts only GitHub and ClickUp URLs, `prefs.py:20, 30-32`) has no cited text in what was read; label stays DEFECT-CANDIDATE (05's label stands).

### 3.8 D-1 of research file 06 (fixture replay of the question ledger and Decision Desk)

- Label: **DEFECT-CANDIDATE** (06's label stands). The rule gives a different result here than for 3.1 to 3.7 because the only text found is a record of absence.
- Rule applied: R-C8 step 2.
- Declaring lines (read from origin/master blobs under `.dev/issues/409/bmad/spec-orca-observer/`): `SPEC.md:32` (CAP-1: "A reviewer can replay synthetic fixtures (R0) to see the Signal Bridge, Attention Ledger and Decision Desk directions at 160, 116 and 80 columns ... before any live Orca call"); `release-gates.md:9` (R0: "A, B, C renders at 160/116/80 marked 'synthetic fixture, not live evidence'"); `acceptance-tests.md:25` (AC-3, T7: `base` "in fixture mode lists every question oldest first with requester/owner and affected IDs").
- Code evidence: `SNAPSHOT/src/superclaude/cli/observe/commands.py:77-78` (`QUESTIONS_NEED_LIVE_TEXT = "--questions needs a live source; it cannot be combined with --fixture"`), `:183-188` (`_question_refusal` returns exit 2 when `options.questions` and `options.fixture`), `:414` (checked before any Orca call); `collector.py:125-129` (`FixtureSource.read_questions` always returns `SourceResult("FAILED", code="no-question-fixture")`); only test hit for that code: `tests/observe/test_collector.py:675`.
- Text found and why it does not meet step 1: `acceptance-tests.md:25` says T7 is "not built / no automated test: spec test T7 cannot run as written, because `_question_refusal` ... refuses `--questions` with `--fixture`". It records that the test cannot run; it does not state that the build is meant not to replay question fixtures. The refusal string exists only in code (grep of `*.py` and `*.md` over the snapshot: `commands.py:77-78, 188`); a grep of the SPEC folder for "needs a live source", "cannot be combined with --fixture" and "refus" finds no spec line that adopts the refusal; the owner records (`owner-decisions-20261108`, `-20261111`, `-20261112`, `owner-direction-record-20261116`, `owner-pass-record-20261112`) contain no line mentioning fixtures. `release-gates.md:9` R0 lists the A, B, C renders as design material "None from Orca; offline only"; the R0 renders in the design package (`.dev/design/orca-observer-20261106/`) are a separate thing from the observer CLI's `--fixture` mode and are the subject of GF-5; this file does not decide whether they satisfy R0's wording.
- Scope of D-1: the observer CLI path `superclaude observe --fixture ... --questions` only. Live `--questions` is wired (section 4). Text-only views B and C are exercised by tests through a fake runner (06 section 9), not through the fixture CLI.
- Question for the owner (fact, not a recommendation): is fixture replay of the question ledger and Decision Desk through `superclaude observe --fixture` still wanted, or is the fake-runner test route the accepted substitute? Remediation task not created (read-only brief); flagged for the owner.

Key Takeaways
- stalled (proved), fenced, `agent_wait_since`, Safe to close, Removable: KNOWN LIMIT (cited). The three that 04 labelled DEFECT-CANDIDATE (stalled, fenced, `agent_wait_since`) change to KNOWN LIMIT; 03's four labels stand.
- Living-report writer: KNOWN LIMIT sequenced to PR B (ORCH:510, :791, :1020, :1041; ruling 37 at ORCH:3), with the SKILL.md present-tense wording contradicted by the missing verb and no stated interim behaviour in ORCH.
- D-1: DEFECT-CANDIDATE stands; the only text is a record of absence (`acceptance-tests.md:25`).
- CHANGELOG.md:170's reason for stalled/fenced differs from the SPEC's; its `working` clause is stale since 2026-11-16; commands.md:619 has no reason and only :620 (for `working`) is stale.

<!-- END S3 -->

## 4. Scope of the "no DEFECT-CANDIDATE" lines in research files 01 and 02

- Statements: 01 section 5.2 (line 153) ends "No in-scope-but-unwired capability found for R2/R3. [no DEFECT-CANDIDATE]"; 01 Gaps item 9 (line 356) repeats "No DEFECT-CANDIDATE" for the question gate and link; 02 section on the C8 check (line 173) says "**No unwired-capability DEFECT found for R2, R3, snapshot or `--once`.** DEFECT-CANDIDATES: none for these."; 02 Gaps item 10 (line 291) says "no DEFECT-CANDIDATE to report".
- Determination: those lines cover the **live** R2 (`--questions`) and R3 (link, Decision Desk) wiring, and the snapshot and `--once` paths, and nothing else. Evidence for what they cover: the chain `--questions` (`commands.py:487-496`) -> `Options.questions` -> `_questions_on` (`:173-175`) and `_link_on` (`:178-180`) -> `Collector(... questions=, link=)` (`:247-253`, `:388-395`) -> `LiveSource.read_questions` (`collector.py:205-245`, `adapter.py:469-512`), with both gate constants `True` (`commands.py:67, 70`) as 01 and 02 record. Section 3.8 does not contradict the live finding; it adds a path that live wiring does not reach.
- What they do not cover: fixture replay of the question ledger and Decision Desk (D-1, section 3.8). 02 already contains the facts (02 line 171: "`FixtureSource.read_questions` returns `FAILED` code `no-question-fixture` ..., but `_question_refusal` blocks `--questions --fixture` with exit 2 first (commands.py:187-188). So the fixture path never reaches it"), but 02 line 173 then says "no DEFECT" in a sentence a reader can take to cover all R2/R3 paths. The two lines are consistent only under the scope stated here.
- Wording for the synthesis (minor finding M-1): "R2/R3 live path wired; fixture replay of the question ledger and Decision Desk is refused (D-1, DEFECT-CANDIDATE)".

Key Takeaways
- "None" in 01 and 02 means: live R2/R3, snapshot and `--once` wiring. It does not mean fixture replay of B and C.
- 06 D-1 is the one DEFECT-CANDIDATE on the observer side; it does not overturn 01 or 02.

<!-- END S4 -->

## 5. Corrections to carry into the research files and the synthesis (facts only)

| Where | Current text | Reconciled text |
|---|---|---|
| 04 section 5 rows "Stalled (proved) class" and "Fenced class", 04 Gaps item 1, 04 Summary | DEFECT-CANDIDATE | KNOWN LIMIT (cited): SPEC:231-232, :251; DESIGN:493, :636, :841, :877 |
| 04 section 5 "second note", 04 Gaps item 2, 04 Summary | DEFECT-CANDIDATE (low) for `agent_wait_since` | KNOWN LIMIT (cited): SPEC:238; DESIGN:493, :1003 |
| 04 Stale Docs item 2 | D7 "lives at `design-base.md:813`" and QA cites it as the design | `design-base.md:813` is correct for that file; the snapshot design has D7 at DESIGN:841 (also :636, :877) |
| 05 lines 317 and 578 (Gaps item 1) | DEFECT-CANDIDATE (R5) | KNOWN LIMIT (cited), sequenced to PR B (ORCH:510, :791, :1020, :1041; ORCH:3) with residual facts in 3.7 |
| 03 section 8.1 point 3 and Takeaways, 03 Gaps 4 | commands.md:619-620 gives the capture gap as the reason for stalled/fenced | only `CHANGELOG.md:170` does; commands.md:619 gives no reason; :620 is stale only for `working` (GF-2) |
| 01 line 153, 356; 02 line 173, 291 | "no DEFECT-CANDIDATE" | scope = live R2/R3, snapshot, `--once`; D-1 is separate (section 4) |
| 06 section 9 | D-1 DEFECT-CANDIDATE | stands (3.8) |

<!-- END S5 -->

## Gaps and Questions

1. **UNVERIFIED: owner of the "source mapping".** SPEC:232 makes stalled (proved) fixture-only "until a source mapping exists"; no work item owning that mapping was found (03 8.1 point 1; the `gh search` there is a search, not an exhaustive scan; this pass made no `gh` call). Flagged for the owner; remediation task not created (read-only brief).
2. **Attribution level.** The sweep scope text (SPEC:231-232, :251) cites review inputs (V1R3, V2R3, V3R3, INV-006, Change 10), not a dated owner ruling naming stalled or fenced (03 8.1 point 2). Under R-C8 that still yields KNOWN LIMIT; if the owner requires a dated owner ruling, stalled and fenced revert to DEFECT-CANDIDATE with no change to the facts.
3. **Sequencing line as scope decision (3.7).** Whether ORCH's PR split (approved by ruling 37) is a scope decision for the living-report writer is the one judgment in this file; the label flips with the owner's answer and no fact changes.
4. **No fixture-replay decision found (3.8).** Only the observer spec folder and the five owner records named above were searched for it, by grep on the origin/master blobs; other owner records or chat decisions outside the repo were not available.
5. **Interim behaviour of the shared page (3.7).** ORCH states none; 05 section 15 observed it in code.
6. **GF-2's wording of the CHANGELOG and commands.md fix** is not made in the research files by this pass (the brief asks for a reconciliation file); the appended "see gapfill" line is the requester's step.

## Stale Documentation Found

- **[STALE DOC]** `CHANGELOG.md:170` (`## [6.0.0] - 2026-11-18`, "Known limits (sweep, Phase 1)"): `working` "is never produced" and "Healthy workers read `could not determine`" are out of date (Rule 5 active since 2026-11-16, `classify.py:251-269`, DESIGN:493, :841); its reason for stalled/fenced differs from SPEC:232.
- **[STALE DOC]** `docs/user-guide/commands.md:620`: `working` "is never produced yet" (same reason); `:619` is accurate and gives no reason.
- **[STALE DOC]** `agent-work-report/SKILL.md:14-16, 115-116`: entry files and the orchestrator's living report are described as current while the writer verb does not exist (`superclaude orchestrator report-entry`); `[CODE-CONTRADICTED]` as a statement of current state; ORCH places it in PR B.
- **[STALE DOC, location]** research file 04 "Stale Documentation Found" item 2: the D7 line number in the snapshot design is :841 (`design-base.md:813` is the task-package copy).
- Not stale (checked): DESIGN:636 footnote text and `report.py:42-45` `SP24_LINE` match; DESIGN:493, :841, :877 match the code on the four rule-5 conditions (`classify.py:251-269`) and on `worker_done_seen`/`fenced_evidence` being unproduced.

## Summary

One rule (R-C8): a cited spec- or design-level text, specific to the capability, saying the build does not deliver it, gives KNOWN LIMIT (cited); no such text gives DEFECT-CANDIDATE. Applied to every item: stalled (proved), fenced and `agent_wait_since` are KNOWN LIMIT (SPEC:231-232, :238, :251; DESIGN:493, :636, :841, :877), which reverses file 04's labels and agrees with file 03; Safe to close and Removable are KNOWN LIMIT (SPEC:106, :274, :338); the living-report writer (file 05) is KNOWN LIMIT sequenced to PR B (ORCH:510, :791, :1020, :1041, ruling 37 at ORCH:3), with the SKILL.md present-tense text contradicted by the missing verb; D-1 (file 06) stays DEFECT-CANDIDATE because its only text, `acceptance-tests.md:25`, records an absence and states no decision. The "no DEFECT-CANDIDATE" lines in files 01 and 02 cover live R2/R3, the snapshot and `--once` only. Residual owner facts kept: no work item owns the "source mapping" (SPEC:232), the stalled/fenced reason in `CHANGELOG.md:170` differs from the SPEC, and file 04's D7 location is :841 in the snapshot design. Nothing recommends how Clay's orchestrator design is unified with these tools.

