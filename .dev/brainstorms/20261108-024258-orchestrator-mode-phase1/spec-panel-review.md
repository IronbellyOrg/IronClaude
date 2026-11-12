---
spec: .dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md
review_date: 2026-11-08
mode: critique
focus: requirements,architecture
protocol: ~/.claude/commands/sc/spec-panel.md
panel:
  requirements: [Karl Wiegers (lead), Gojko Adzic, Alistair Cockburn]
  architecture: [Martin Fowler (lead), Sam Newman, Gregor Hohpe, Michael Nygard]
  always_active: [James Whittaker]
review_order: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
spec_edited: false
---

# Spec Panel Review: Orchestrator Mode Phase 1 (#339)

## Summary

This review covers the merged Phase 1 spec (616 lines) for the read-only, coordinator-only `/sc:sweep` command and the WC-14 "Coordinator loop" rule. The spec was not edited. Every improvement is given as recommended spec text inside its finding.

**Counts by severity:** 29 findings. CRITICAL 3, MAJOR 17, MINOR 9.

**Top 5 findings:**

1. **SP-01 (CRITICAL).** The section 8 Orca allowlist (lines 289-296) names `task-list` (two templates) and `worktree ps`, which the owner's INV-005 condition 1 (line 470) does not permit, and it omits `worktree list` and `worktree current`, which the condition names. Rule 4(b), the gate policy line (rule 1) and worktree discovery all depend on the forbidden verbs, and no replacement source is named.
2. **SP-05 (CRITICAL, dimensional mismatch under FR-19).** The FR-005 AC (line 99) expects "6 rows in JSON" from 3 workers, 2 worktrees and 1 person session. JSON `rows` holds session rows that each carry a session `class` (4 rows here), and the JSON key list (line 162, line 369) has no worktree key at all. Worktree state, package states and shared flags never reach JSON.
3. **SP-04 (CRITICAL).** NFR-009 (line 138) allows additions within v1, but its AC fails on any change to the key set unless `schema_version` changes. An allowed addition fails the test.
4. **SP-08 (MAJOR).** Each call's timeout is the lesser of 10 s and the remaining budget (line 283), and any call timeout is classified `unavailable` (line 280). Budget exhaustion or one slow `worker-show` therefore reports a false global Orca outage and stops every later Orca read.
5. **SP-29 (MAJOR).** With `--run R1`, the transcripts of workers that belong to another Run in the same tree join no scoped Orca row, so FR-010 (line 104) can mark them person-started `True`, and old ones become idle and Historical.

Verdict: not ready for `/sc:design` until SP-01, SP-04 and SP-05 are fixed in the spec, because each one makes a requirement and its acceptance criterion, or two sections, provably disagree.

## Quality scores

| Dimension | Score (0-10) | Basis |
|---|---|---|
| Clarity | 6.5 | Most requirements are precise and carry a test. Several key terms have no definition: the Age column, `last_activity`, the stable row ID, the collision suffix and when the cap counts as "reached" (SP-06, SP-10, SP-15, SP-16). Rule 5 is hard to read (SP-24). |
| Completeness | 6.0 | Outage, partial-read and sanitising paths are well covered. Gaps: JSON has no worktree data (SP-05), git porcelain parsing (SP-17), input bounds on `--window`, `--run` and `--root` (SP-09, SP-18), the wall-clock bound on disk and git work (SP-10), and the transcript tail rule (SP-28). |
| Testability | 7.5 | Nearly every FR and NFR has an AC, with exact argv counts and named fixtures. Lost points: two ACs contradict their requirements (SP-04, SP-05), and NFR-005 is unclear about `report_path` and the collection interval (SP-06). |
| Consistency | 4.5 | The owner sign-off was added to section 13, but the rest of the spec was not brought into line with it: the allowlist (SP-01), the always-printed UNVERIFIED line (SP-02), and the gating text in the frontmatter, section 13 and section 17.1 (SP-03). FR-002 and FR-019 repeat each other word for word (SP-19). |
| **Overall** | **6.1** | Strong safety intent and test discipline. The INV-005 follow-through is the main gap. |

## Panel notes

- The experts reviewed in the protocol's sequence: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. The protocol file also gives Whittaker "Review Order: 11" in his own entry. That conflicts with the sequence list, and this review follows the sequence list.
- Lisa Crispin is not on the requested panel. Nygard carries out the Guard Condition Boundary Table completeness check (FR-8 to FR-10 of the protocol) in her place.
- Items decided before this review were not raised as new findings: the INV-005 sign-off, G-1 and GQ-101 to GQ-113. The review checks only whether the rest of the spec is consistent with them. G-1 receives a recommended answer under Hohpe and is not re-graded.
- Line numbers refer to the SPEC as read on 2026-11-08 (616 lines).
- Severity rule: CRITICAL means provably wrong or self-contradictory. MAJOR means a real defect or gap that design must close. MINOR means wording or hygiene.

## === REQUIREMENTS ANALYSIS ===

The experts below reviewed in protocol order (Wiegers, Adzic, Cockburn). Whittaker's sixth-position findings are grouped in their own section further down, as the required headings ask.

### Karl Wiegers (lead): requirement quality

**SP-03. The release gate text was not updated after the owner signed off.**
- **Issue:** The frontmatter `gate_status` (line 9) records sign-off with two conditions. Several other lines still describe the pre-sign-off state:
  - The Status row (line 26): "release gated on INV-005 owner sign-off".
  - Section 13 (line 460): "no requirement in this spec depends on it being resolved". This is now false, because condition 1 changes the allowlist (SP-01) and condition 2 changes the header (SP-02).
  - Section 17.1 (line 590): "Release precondition, not a test: the owner signs off on INV-005". The checklist (lines 582-588) has no item for the two conditions.
- **Severity:** MAJOR. **Expert:** Wiegers. **Location:** Frontmatter and Status, lines 9 and 26; section 13, line 460; section 17.1, lines 582-590.
- **Recommendation:** Replace line 26 with "Merged spec after adversarial debate; INV-005 signed off 2026-11-08 with two conditions (section 13), which are release preconditions." Replace line 460 with "This section holds one accepted risk. The owner accepted it on two conditions; those conditions are requirements of this spec (NFR-014, NFR-015 below) and release preconditions." Replace line 590 with "Release precondition: NFR-014 (five-verb allowlist pin) and NFR-015 (version-scoped lock line) pass." Add these checklist items:
  - "[ ] INV-005 condition 1: the five-verb allowlist pin test and the `--include-remote` negative test pass."
  - "[ ] INV-005 condition 2: the version-scoped lock-line tests pass for the checked version and for a different version."
- **Rationale:** A gate that is described three different ways will be read in the most convenient way. The conditions must become testable items, or they will be lost between this spec and design.
- **Priority:** High. **Quality impact:** Consistency +1.0, completeness +0.3.

**SP-04. NFR-009's AC forbids what NFR-009 allows.**
- **Issue:** NFR-009 (line 138) says "a key is never removed or renamed within v1; additions only". FR-017 (line 111) and section 5.2 (line 162) both say "additive-only compatibility". The AC says "a change to the key set fails unless `schema_version` changes". An addition is a change to the key set, so an allowed addition fails the test unless the version is bumped. The rule and its test contradict each other.
- **Severity:** CRITICAL (self-contradictory). **Expert:** Wiegers. **Location:** NFR-009, line 138; also FR-017 line 111 and section 5.2 line 162.
- **Recommendation:** Replace the NFR-009 AC with: "Golden key-set test: the pinned v1 key set (top level, `rows[]`, `waiting`, `summary`, `sources[]`) is a subset of the emitted key set at every level, and each pinned key keeps its JSON type. Removing or renaming a pinned key fails unless `schema_version` changes. A new key passes and must be added to the pinned set in the same change."
- **Rationale:** A subset test with a type check is the usual way to pin additive compatibility. An equality test makes every Phase 2 to 6 addition a schema bump, which defeats the "Additive keys only" extension point (line 217).
- **Priority:** High. **Quality impact:** Consistency +0.5, testability +0.5.

**SP-05. The FR-005 AC counts worktrees as JSON rows, but JSON has no place for them (dimensional mismatch).**
- **Issue:** FR-005 (line 99) says the fixture "with 3 workers, 2 worktrees, 1 person session yields 6 rows in JSON and in the report". The quantities do not match:
  - JSON `rows` holds session rows. Each one has a session `class` (FR-006, line 100; section 5.2, line 165).
  - Under FR-006, a worktree cannot be a row: it has no session class.
  - The required JSON keys (line 162, line 369) have no worktree or package key. So `WorktreeState`, package states, shared flags and the removable reason (lines 233-234, FR-013, FR-014, FR-015) never reach JSON, even though section 9 says "Phases 2, 5 and 6 read `rows`" and Phase 2 acts on the worktree part of safe-to-close.
  - The FR-005 requirement also says "visible, historical and omitted counts must reconcile" but gives no formula.
  - `<shown>/<total>` is a session count (header line 333; Sessions heading, line 358). The AC compares it with a 6-row count that includes worktrees.
- **Severity:** CRITICAL (dimensional mismatch, protocol FR-19). **Expert:** Wiegers, with Fowler. **Location:** FR-005, line 99; section 5.2, line 162; section 9, line 369.
- **Recommendation:**
  - Replace the FR-005 AC with: "Fixture with 3 workers, 2 worktrees, 1 person session yields 4 entries in JSON `rows` and 2 entries in JSON `worktrees`; the report's Sessions heading reads `(4/4)` and its Worktrees section has 2 rows."
  - Add `worktrees` to the required top-level keys in section 5.2 and section 9: "`worktrees`: list of `{path, status_read, uncommitted, unpushed, dev_tasks_unsaved, frozen, packages[{id, location, state}], shared_package_ids, removable, removable_reason}`; every key always present."
  - Add the reconciliation rule to FR-005: "`summary.total` = `summary.visible` + `summary.historical`. `summary.bound_reached` counts rows included in `visible` that were not enriched. Rows never discovered are not counted, and when any list is truncated or unscanned, `summary.total_is_lower_bound` is true."
- **Rationale:** The protocol treats a unit mismatch between producer and consumer as CRITICAL, because an implementer will satisfy one side and break the other. Leaving worktree data out of JSON also removes Phase 2's main input.
- **Priority:** High. **Quality impact:** Testability +0.5, completeness +0.7, consistency +0.5.

**SP-15. The sources of the "Age" column and of `last_activity` are not defined.**
- **Issue:** FR-011 (line 105) sorts waiting (a) by age, "oldest first", but never says what the age is measured from. Candidates include the contract's mtime, the time `agentWait` was set, the Task creation time and the transcript's last record. `SessionRow.last_activity` (line 232) has no source either. FR-007's AC (line 101) uses "transcript mtime", which implies mtime, but a tab map refresh or log rotation could touch a transcript without any person activity (UNVERIFIED).
- **Severity:** MAJOR. **Expert:** Wiegers. **Location:** FR-011 line 105, section 7 line 232, FR-007 line 101.
- **Recommendation:** Add to section 7: "`last_activity` is the timestamp of the last complete JSONL record in the transcript tail when that record carries one, else the transcript file's `st_mtime`; the source used is recorded in `evidence`. Waiting (a) age is `now - t`, where `t` is the earliest of: the contract file's `st_mtime` for a blocked contract, or the `agentWait` timestamp field captured in step 1.0a (UNVERIFIED); with no `t`, the row is in the unknown-age group."
- **Rationale:** An undefined sort key makes the "oldest first" test meaningless, and it decides which question the person answers first.
- **Priority:** Medium. **Quality impact:** Clarity +0.3, testability +0.2.

**SP-19. FR-002 and FR-019 repeat the same text word for word.**
- **Issue:** FR-002 (line 96) and FR-019 (line 113) both hold the full Run-binding and outage paragraph, and their ACs repeat the same three tests. Section 5.1 (lines 154-157) states it a third time. If one copy is edited, the copies will drift apart.
- **Severity:** MINOR. **Expert:** Wiegers. **Location:** FR-002 line 96, FR-019 line 113, section 5.1.
- **Recommendation:** Keep the full text in section 5.1 only. FR-002 becomes "Run selection: `--run` repeatable; without `--run`, call `run-current`; outcomes per section 5.1." FR-019 becomes "Orca unavailable after a binding: disk-only continuation per section 5.1; every unscanned Orca source prints `unscanned: orca unavailable`." Each AC cites the same named tests once.
- **Priority:** Low. **Quality impact:** Consistency +0.2.

**SP-25. FR-022 does not name its "both literals", and two different bounds share one reason string.**
- **Issue:**
  - FR-022's AC (line 116) asserts "both `allowed-tools` literals", but the requirement never says what they are.
  - Section 11 (line 422) and FR-020 (line 114) print one reason, `unscanned: call bound reached`, for two different causes: the cap of 50 `worker-show` calls and the 90 s time budget.
- **Severity:** MINOR. **Expert:** Wiegers. **Location:** FR-022 line 116; FR-020 line 114; section 11 line 422.
- **Recommendation:** In FR-022, name the literals, for example: "`allowed-tools` in the command is exactly `Skill`; in the skill it is exactly `Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`" (the final form is fixed at design). In FR-020, use two reasons: `unscanned: show cap reached (50)` and `unscanned: time budget reached (90 s)`.
- **Priority:** Low. **Quality impact:** Clarity +0.2.

### Gojko Adzic: specification by example

**SP-09. The `--run` input has no examples for bad values, and a typo looks like an Orca outage.**
- **Issue:**
  - **Typo:** With an explicit `--run`, any nonzero exit on the first call is classified `unavailable` (line 280). A mistyped Run id therefore gives exit 0 and a report saying "Orca unavailable" (FR-002 test 2, line 96) instead of a usage error.
  - **Regex failure:** A Run id that fails the id regex (line 287) is an argv the allowlist rejects with `ValueError`, which section 8 (line 279) and FR-018 (line 112) make exit 1 "internal". It should be exit 2, a usage error.
  - **Repeated `--run`:** With `--run A --run B`, a first-call failure on A stops every later Orca read, so B is never asked.
  - **Undefined values:** `--run ""` and `--run R1 --run R1` are not specified.
- **Severity:** MAJOR. **Expert:** Adzic. **Location:** FR-002 line 96, section 8 lines 279-280 and 287, FR-018 line 112.
- **Recommendation:** Add to FR-002 and to the section 5.1 contract:
  - "Each `--run` value is validated against the Run id regex in `commands.py` before any `_orca` call; an empty or non-matching value exits 2 with `invalid --run value: <sanitized value>`."
  - "Duplicate `--run` values are collapsed, keeping first-seen order."
  - "With an explicit `--run`, the first call per Run is `worker-list --run <run>`. A nonzero exit whose stderr matches the captured unknown-Run shape (step 1.0a) is `call_failed` for that Run (reason `orca call failed (unknown run)`), not `unavailable`, and later Runs are still read."
  - Add example rows to the AC: `--run ""` gives exit 2; `--run 'r;x'` gives exit 2; `--run R1 --run R1` gives one `worker-list` argv; `--run BAD --run R2`, where BAD gives the unknown-Run shape, gives `worker-list` for R2 and exit 0.
- **Rationale:** Concrete key examples expose the gap between "Orca is down" and "you typed the wrong id". At present the person cannot tell these apart.
- **Priority:** High. **Quality impact:** Testability +0.3, clarity +0.2.

**SP-18. `--window` and `--root` have no upper bound, no formula and no rule for invalid paths.**
- **Issue:**
  - **No maximum:** FR-003 (line 97) gives "positive integer plus `h` or `d`". `--window 999999999d` passes the parser, then `now - timedelta(days=999999999)` raises `OverflowError`, giving exit 1 instead of 2 (Python date range, UNVERIFIED against the final code).
  - **Unicode digits:** If the parser uses `int()` or a regex `\d` without ASCII mode, Python also accepts digits from other scripts, such as Arabic-Indic digits, so `٦h` could pass.
  - **No formula:** `window_start` (line 227) is never defined; presumably it is `now - window`.
  - **No `--root` validation:** FR-004 (line 98) does not say what happens when `--root` does not exist or is not a directory, or when the root walk reaches `/` without finding `.git`.
- **Severity:** MAJOR. **Expert:** Adzic. **Location:** FR-003 line 97, FR-004 line 98, section 7 line 227.
- **Recommendation:**
  - Amend FR-003: "`--window` matches `^[1-9][0-9]{0,3}[hd]$` (ASCII only) and is at most `720h` or `30d`; else exit 2. `window_start = now - window`." AC additions: `721h`, `31d`, `999999999d` and `٦h` each give exit 2.
  - Amend FR-004: "An explicit `--root` must resolve to an existing directory that holds `.git` (file or folder); else exit 2 with `invalid --root: <path>`. Without `--root`, a walk that reaches the filesystem root without finding `.git` exits 2 with `no git checkout found above <cwd>`."
- **Priority:** Medium. **Quality impact:** Completeness +0.3, testability +0.2.

**SP-21. Exit 2 without `--run` hides the reason Orca is unavailable.**
- **Issue:** INV-017's review 3 note (line 505) already records this: the exit-2 message omits the cause, so `binary not found: orca-ide` is invisible on the default path. No requirement fixes it.
- **Severity:** MINOR. **Expert:** Adzic. **Location:** Section 14, INV-017, lines 503-505; FR-002 line 96; section 5.1 line 156.
- **Recommendation:** In section 5.1, change the message to `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>`, where `<reason>` is the sanitized unavailable cause, for example `binary not found: orca-ide`. Add an example to FR-026 test 1: the launch `OSError` case asserts that stderr contains `binary not found: orca-ide`.
- **Priority:** Medium. **Quality impact:** Clarity +0.1.

**SP-26. A `last_activity` in the future gives a negative age.**
- **Issue:** Clock skew, or a transcript copied from another host, can give `last_activity > now`. Classification is still defined (not idle, because the strict `<` rule fails), but the Age cell would print a negative value.
- **Severity:** MINOR. **Expert:** Adzic. **Location:** Section 7, line 232; FR-011, line 105.
- **Recommendation:** Add: "A timestamp later than `now` is treated as unknown age and adds note `timestamp in the future`; it is never idle."
- **Priority:** Low. **Quality impact:** Clarity +0.1.

### Alistair Cockburn: goals and use

**SP-14. Normal states crowd the "who needs me" view.**
- **Issue:** Rule 8 (line 250) sends every active person session to could not determine, with the note "person session, active". The Could not determine section is placed second, ahead of Sessions (line 356). Rule 4(b) (line 246) sends every ready Task whose creator is unknown to waiting (b). In Phase 1 the creator is always unknown, so every ready Task is listed as waiting on a person. The success metric (line 54) is "who needs me, and what is safe to close" from one report. A person running 6 sessions will see all 6 as "could not determine" and every queued Task as waiting on them, which buries the real requests.
- **Severity:** MAJOR. **Expert:** Cockburn. **Location:** Rule 8 line 250; rule 4(b) line 246; section 9 lines 355-356; success metric line 54.
- **Recommendation:**
  - Add a class `person session (active)` as a new rule 8 before the fallback, matching `person_started is True` and `last_activity >= window_start`. It is printed in Sessions only, never in Could not determine.
  - For rule 4(b), print ready Tasks under a sub-heading `Ready Tasks needing ownership review (creator not observable in Phase 1)` inside Waiting (b), with a count line, so it is clear they are not individual questions.
  - NFR-010's pinned list changes accordingly. Section 6 (line 214) says later phases extend `RULES` by inserting named rules, and NFR-010 pins the order, so a class added after v1 shows as a reorder; making the change now avoids that.
- **Rationale:** A use case succeeds when its main actor reaches the goal quickly. A known, healthy state labelled "could not determine" trains the reader to skip that section, which is the section meant to catch hidden waits.
- **Priority:** High. **Quality impact:** Clarity +0.4.

**SP-27. The WC-14 end condition cannot be observed.**
- **Issue:** WC-14 (line 384) ends the loop when "every result has been inspected and its admission or rejection recorded". Those records are in the coordinator's run notes, which the sweep does not read. The sweep also cannot observe "result read" (line 267). Neither the coordinator nor a reviewer can check the condition from the sweep's output.
- **Severity:** MINOR. **Expert:** Cockburn. **Location:** Section 10, line 384.
- **Recommendation:** Append to the WC-14 text: "The coordinator records each admission or rejection in its run notes; the sweep does not observe them." This makes the condition the coordinator's own record, and adds no pin.
- **Priority:** Low. **Quality impact:** Clarity +0.1.

## === ARCHITECTURE ANALYSIS ===

The experts below reviewed in protocol order (Fowler, Nygard, then Newman and Hohpe after Whittaker). Nygard also covers boundary-table completeness because Crispin is absent.

### Martin Fowler (lead): structure and interfaces

**SP-01. The Orca allowlist breaks INV-005 condition 1.**
- **Issue:** The owner's condition 1 (line 470) allows only five verbs: `run-current`, `worker-list` (never with `--include-remote`), `worker-show`, `worktree list` and `worktree current`, pinned by a test. The section 8 allowlist (lines 289-296) also lists `task-list` (lines 294-295) and `worktree ps` (line 296), omits `worktree list` and `worktree current`, and defers `--include-remote` to "Phase 2 or later" (line 307) with no negative test. Requirements built on those extra verbs have no source once they are removed:
  - Rule 4(b) (line 246) reads ready Tasks from `task-list`.
  - `gate_policy` on rule 1 (line 243) and GQ-103(3) (line 521) come "from the Task spec", which is read through `task-list`.
  - Line 460 says no requirement depends on INV-005, which is now false (see SP-03).
  - NFR-003's exact-allowlist recording test (line 132) pins the wrong set, and its negative cases do not include `task-list`, `worktree ps` or `--include-remote`.
- **Severity:** CRITICAL (the spec contradicts a signed-off owner condition). **Expert:** Fowler, with Newman. **Location:** Section 8, lines 289-296 and 307; section 13, lines 460 and 470; rule 4(b), line 246; rule 1, line 243; NFR-003, line 132.
- **Recommendation:** Replace the section 8 allowlist with exactly these templates (flags UNVERIFIED until step 1.0a captures them):
  - `orca orchestration run-current --json`
  - `orca orchestration worker-list --run <run> --json` (the argv never contains `--include-remote`)
  - `orca orchestration worker-show --dispatch <dispatch> --json`
  - `orca worktree list --json`
  - `orca worktree current --json`

  Then:
  - Name the replacement sources: `agentWait` and any Task spec text come from `worker-show` (UNVERIFIED field names, captured at step 1.0a).
  - Either drop rule 4(b) from Phase 1 with the note "ready Tasks are not observable under INV-005 condition 1", or name a `worker-show` field that carries them.
  - Extend NFR-003's AC with: "An exact-set pin test asserts `ALLOWED_ORCA` holds the five templates above and nothing else; negative tests assert that `task-list`, `worktree ps` and any argv containing `--include-remote` raise `ValueError` before launch."
  - Rewrite line 460 as recommended in SP-03.
- **Rationale:** An owner condition that the allowlist does not encode is not met, whatever the prose says. The pin test is the condition's only enforcement.
- **Priority:** High. **Quality impact:** Consistency +1.0, completeness +0.3.

**SP-02. INV-005 condition 2 has no data source and conflicts with "always printed".**
- **Issue:** Condition 2 (line 471) asks for a version-scoped lock line, for example "unlikely (checked for Orca 1.4.245)", that falls back to UNVERIFIED on any other version. Section 9 says the UNVERIFIED line is "always printed" (line 344, also line 337). None of the five allowed verbs is known to return the Orca version, so the sweep cannot tell which line to print.
- **Severity:** MAJOR. **Expert:** Fowler. **Location:** Section 9, lines 337 and 344; section 13, line 471.
- **Recommendation:** Replace line 344 with: "The lock line reads `Orca lock risk: unlikely (checked for Orca <checked_version>)` when the observed Orca version equals `CHECKED_ORCA_VERSION` in `report.py`, and `Orca lock risk: UNVERIFIED (checked for Orca <checked_version>; observed <observed or unknown>)` otherwise." Name the version source, choosing one at design: a version field in `run-current --json` (UNVERIFIED), or one fixed disk read of the Orca package metadata added to the section 8 disk-read list (line 317). If neither exists, record that condition 2 cannot be met as written and return it to the owner. Add two tests: matching version gives "unlikely"; other or unknown version gives UNVERIFIED.
- **Priority:** High. **Quality impact:** Consistency +0.4, testability +0.2.

**SP-06. NFR-005's byte identity is unclear about values that differ by design.**
- **Issue:** NFR-005 (line 134) asks for a byte-identical report and JSON from the same `SweepInput` and `SweepContext`, and its AC injects `now` and the output path. Two gaps remain:
  - JSON carries `report_path`, which `write_report` sets after the collision check. FR-017 (line 111) requires that two runs with the same `now` produce two files, so the second run's `report_path` has a suffix and its JSON differs. The AC only renders twice, so it never meets this case.
  - The header's `collected <start> to <end>` interval (line 332) is not named as a field of `SweepInput` or `SweepContext` (lines 227-237), so it is unclear whether it is injected or read from the clock during render.
  - The collision rule in section 5.3 (line 172) gives no suffix format and no loop bound.
- **Severity:** MAJOR. **Expert:** Fowler. **Location:** NFR-005, line 134; section 5.3, lines 171-177; section 7, lines 227-237.
- **Recommendation:** Amend NFR-005: "Same `SweepInput` (including `collected_start` and `collected_end`, both captured by `collect`) and same `SweepContext` give a byte-identical rendered report, and a byte-identical JSON object apart from `report_path`." Add `collected_start: datetime` and `collected_end: datetime` to `SweepInput`. Amend section 5.3: "On collision, try `<stem>-2.md` to `<stem>-99.md` in order with exclusive create; after 99, exit 1 with `report name space exhausted: <dir>`."
- **Priority:** Medium. **Quality impact:** Testability +0.3.

**SP-13. Rule 1 hides rule 4(a) when `gate_policy` is missing.**
- **Issue:** Rule 1 (`blocked_contract`, line 243) "returns could not determine" when a blocked contract sits on a live row with `gate_policy` None. Rules apply in order, so such a row never reaches rule 4(a) (line 246) even when its `agent_wait` is non-null, and it never appears in Waiting (a). With no Orca row at all (Orca unavailable, or the contract not named by any row), rule 1's condition "Orca row settled" has no defined value. Under SP-01, `gate_policy` has no source, so it is always None and every blocked contract on a live row lands in could not determine.
- **Severity:** MAJOR. **Expert:** Fowler. **Location:** Section 7, rules 1 and 4(a), lines 243 and 246.
- **Recommendation:** Narrow rule 1: "With `gate_policy` None on a live row, rule 1 declines (no match) and adds its note, instead of returning could not determine, so a non-null `agent_wait` still reaches rule 4(a). With no Orca row for the contract, rule 1 matches only on a Ruling halt; otherwise it declines with note `blocked contract; Orca state not observed`." Add rule-table tests for: `gate_policy` None with `agentWait` set (expect waiting (a)); Orca None (expect rule 2 onward).
- **Priority:** High. **Quality impact:** Consistency +0.3, testability +0.2.

**SP-20. `write_report` needs `os`, but the AST test forbids `os` in report.py.**
- **Issue:** The module table (line 197) places `write_report` in `report.py`, whose "May import" column lists `models` only and whose "Must not import" column names `subprocess`. Exclusive create, fsync and link (the G-1 answer below) all need `os`, which is outside that allowed list. NFR-004 (line 133) forbids `os` in `classify.py` and `report.render`, checked by an AST import test over both modules. Imports are per module, not per function, so an `os` import for `write_report` in `report.py` fails that test.
- **Severity:** MINOR. **Expert:** Fowler. **Location:** Section 6, line 197; G-1, lines 600-608.
- **Recommendation:** Move `write_report` to `probes.py` or to a new `writer.py` that holds the only file write. Say in section 6: "`report.py` renders strings only; `writer.py` holds the single write path and is the only sweep module allowed to open a file for writing."
- **Priority:** Low. **Quality impact:** Consistency +0.1.

### Michael Nygard: operations, failure and limits

**SP-10. Time and call budgets do not cover all work and are not fair across Runs.**
- **Issue:**
  - The `Budget` (line 283) bounds Orca calls: 50 `worker-show` calls, 10 s per call, 90 s in total. `_git` calls pass a per-call timeout (line 279), but the spec gives no value for it and does not say whether git time counts toward the 90 s. Disk reads (line 317) have byte limits but no time bound.
  - FR-020 says "every call counts toward the 90 s total", but in a list about `worker-show` it is unclear whether "every call" includes `_git` calls.
  - The 120 s skill timeout (NFR-007, line 136) is claimed as enough but not shown: 90 s of probes plus git and disk work outside the budget can exceed it, and the skill's Bash call is then killed with no report.
  - The cap of 50 is shared across Runs. With `--run A --run B`, Run order decides which Run is enriched.
  - "Cap reached" is undefined: it could mean 50 calls were made, or at least one row was denied a call.
- **Severity:** MAJOR. **Expert:** Nygard. **Location:** Section 8, line 283; FR-020, line 114; NFR-007, line 136.
- **Recommendation:** Add to section 8:
  - "Every `_git` call has a 10 s timeout and counts against the same 90 s total; disk reads are bounded by the byte limits and are not timed."
  - "The cap of 50 is split evenly across selected Runs (remainder to the first Run), and unused share passes to the next Run."
  - "`bound_reached` is the count of rows that needed a `worker-show` call and did not get one; the cap line prints only when it is at least 1."
  - NFR-007 AC: "With a fake `_orca` and fake `_git` that each use their full timeout, total wall time stays under 120 s and a report is published."
- **Priority:** High. **Quality impact:** Testability +0.3, completeness +0.2.

**SP-12. The `uv run` fallback may change the environment.**
- **Issue:** The skill's fallback (FR-022, line 116) runs `uv run superclaude sweep run`. By uv's documented default, `uv run` syncs the project environment before running, which can install or update packages and write a lockfile (behavior not run here; UNVERIFIED for this repo's uv version). That breaks NFR-001's read-only rule (line 130) and can use up the 120 s timeout (NFR-007).
- **Severity:** MAJOR. **Expert:** Nygard. **Location:** FR-022, line 116; NFR-001, line 130.
- **Recommendation:** Use `uv run --frozen --no-sync superclaude sweep run` in the skill and in the allowed-tools literal, and add to FR-022: "The fallback never syncs or locks; `tests/commands/test_sweep_command.py` asserts the literal contains `--no-sync`." Confirm the flag behavior at design (the flags exist in `uv run --help`; their effect was not run).
- **Priority:** Medium. **Quality impact:** Consistency +0.2.

**SP-22. `.dev/sweeps/` grows without limit.**
- **Issue:** Each run writes a new report (section 5.3). Nothing removes old ones.
- **Severity:** MINOR. **Expert:** Nygard. **Location:** Section 5.3, lines 171-177.
- **Recommendation:** Add to Out of scope (line 83): "Retention of `.dev/sweeps/` reports; the person deletes old reports by hand." This states the limit without adding code.
- **Priority:** Low. **Quality impact:** Completeness +0.1.

**SP-23. Sanitized cells have no length cap.**
- **Issue:** Sanitizing removes control characters, but a long `body_text` or note can fill a table cell with thousands of characters and make the report unreadable.
- **Severity:** MINOR. **Expert:** Nygard. **Location:** Section 9, sections list, lines 350-363.
- **Recommendation:** Add: "Every report cell is cut to 200 characters after sanitizing, ending with `...` when cut; JSON values are not cut."
- **Priority:** Low. **Quality impact:** Clarity +0.1.

### Sam Newman: service boundaries and integration

**SP-16. The join between Orca rows and transcripts is not specified.**
- **Issue:** `waiting.a` and `waiting.b` entries and Phase 2 refer to rows, but the spec gives no stable row ID and no join key between an Orca worker row, its tab map entry and its transcript. If the tab map is empty or stale, every worker transcript fails to join, so each one is classed `person_started` True (FR-010, line 104) and a coordinator sees its own workers as person sessions.
- **Severity:** MAJOR. **Expert:** Newman, with Hohpe. **Location:** FR-010, line 104; section 7, line 232.
- **Recommendation:** Add to section 7: "`row_id` is `orca:<dispatch>` for Orca rows and `transcript:<session_id>` for transcript-only rows; it is stable across runs for the same inputs. The join key is the transcript's session id recorded in the tab map." Add: "If Orca returned at least one worker row and no transcript joined any Orca row, print `could not join Orca workers to transcripts (tab map empty or stale)` in Could not determine, and set `person_started` to None, not True, for unjoined transcripts in the window."
- **Priority:** High. **Quality impact:** Completeness +0.3, consistency +0.2.

**SP-17. Git output parsing misses common shapes.**
- **Issue:** The git allowlist (lines 309-313) reads `git status --porcelain` and the branch header without `-z`. The spec does not say how to handle:
  - quoted paths (spaces, non-ASCII) and rename entries (`R old -> new`);
  - collapsed untracked entries such as `?? .dev/` or `?? .dev/tasks/`, which hide individual package folders;
  - branch headers: `## No commits yet on <b>`, `## HEAD (no branch)`, `[gone]`, and ahead and behind together.
- **Severity:** MAJOR. **Expert:** Newman. **Location:** Section 8, lines 309-313; FR-015, line 109.
- **Recommendation:** Use `git --no-optional-locks status --porcelain=v1 -z --branch --untracked-files=all` and state: "Entries are NUL-separated; a rename entry consumes the next NUL field. `--untracked-files=all` lists each untracked file, so `.dev/tasks/<id>/` is never collapsed. Branch header cases: `No commits yet` gives unpushed unknown; detached HEAD gives unpushed unknown with note `detached HEAD`; `[gone]` gives unpushed unknown with note `upstream gone`; `ahead N, behind M` gives unpushed N." Add one fixture per case. Note that `--untracked-files=all` can be slow on large trees, which is bounded by the SP-10 git timeout.
- **Priority:** Medium. **Quality impact:** Testability +0.3.

### Gregor Hohpe: messages, results and flow

**SP-24. Rule 5 and the package states are hard to read and partly unreachable.**
- **Issue:**
  - Rule 5's wording (line 247) is hard to parse.
  - The sources of `worker_done_seen` and `fenced_evidence` on exited rows are not stated.
  - The stalled and fenced classes cannot occur in production data in Phase 1, but the report does not say so, so a reader may think a zero count means "none happened".
- **Severity:** MINOR. **Expert:** Hohpe. **Location:** Section 7, lines 243-250.
- **Recommendation:** Rewrite rule 5 as one condition per line. State the source of each input field. Add a report footnote: "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred."
- **Priority:** Low. **Quality impact:** Clarity +0.2.

**G-1 (decided as an open gap; recommended answer, not graded).** Section 5.3 (line 177) leaves open what a run that exits 1 leaves on disk. Hohpe recommends a publish step with one visible commit point:
1. Create a temporary sibling `<dir>/.<stem>.tmp-<pid>` with exclusive create (`O_CREAT | O_EXCL`), write the full report, `fsync` it.
2. `os.link` the temporary file to the final name. The link is atomic and fails if the name exists, so it never overwrites; on that failure, try the next collision suffix (SP-06). Then unlink the temporary file.
3. Print the success JSON only after step 2 succeeds (as section 5.2 already requires).
4. On any handled failure, remove only this invocation's temporary file and exit 1.
5. A killed process can leave an orphan temporary file. It has no `Report complete` footer and a dotted name, so it is never mistaken for a report.

Recommended spec text for section 5.3: "Publication writes a dot-prefixed temporary file with exclusive create, fsyncs it, and hard-links it to the final name; a run that exits 1 removes its own temporary file and leaves no file at a report name. A killed run may leave one dot-prefixed temporary file." This needs `os`, so it depends on SP-20 moving `write_report` out of `report.py`. `os.link` needs a filesystem that supports hard links (UNVERIFIED for every user setup); on failure the fallback is exclusive create of the final name, accepting a partial file without the footer.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

### James Whittaker: adversarial attacks

Whittaker ran the five attacks (zero and empty, divergence, sentinel collision, sequence, accumulation) against every guard in section 8, section 7 and FR-002 to FR-004. Each finding below is in the required format. Attacks that found nothing new are listed at the end.

**SP-07. Sentinel collision: marker strings are matched as substrings anywhere in untrusted text.**

I can break this specification by **sentinel collision**. The invariant at **section 8, line 280** ("`runtime_unavailable` in stdout or stderr" means unavailable) fails when **a successful `worker-show` body quotes the marker inside a field such as `body_text`**. Concrete attack: **Before: binding R1 is established; `orca_available` true; rows 1 to 3 are being enriched. A worker's last message says "if you see runtime_unavailable, retry". Call 2 (`worker-show` for row 1) exits 0 with that text in its JSON. After: the classifier sees the substring, sets unavailable, stops all Orca reads, prints the `Orca unavailable` banner and `orca_available: false`, and rows 2 and 3 go to could not determine with `unscanned: orca unavailable`, although Orca is healthy.**

The same attack works on two other markers:
- Rule 6 (line 248) classifies "a `guard refused:` body" as finished. A body that only quotes the phrase, for example a worker discussing a guard message, is finished when it should be working.
- Package state `archive-blocked` (line 262) matches "a `FINAL:` line". A ledger note such as `- step 3: will write FINAL: later` matches if the test is a substring test.

- **Severity:** MAJOR. **Expert:** Whittaker. **Location:** Section 8, line 280; section 7, lines 248 and 262.
- **Recommendation:** Replace the three matches with anchored forms fixed at step 1.0a:
  - "`runtime_unavailable` counts only as the captured error field value (for example a JSON `error.code` equal to `runtime_unavailable`, UNVERIFIED shape) or as the whole first line of stderr; a match inside any other JSON string field is ignored."
  - "`guard refused:` matches only when the body's first line starts with `guard refused:`."
  - "A `FINAL:` line is a `progress.md` line that starts with `FINAL:` after optional leading whitespace."
  - Add one negative fixture per marker, each with the marker inside ordinary text.
- **Priority:** High. **Quality impact:** Testability +0.2, consistency +0.2.

**SP-08. Divergence: the shrinking per-call timeout turns a slow but healthy Orca into a global outage.**

I can break this specification by **divergence between the budget and the classifier**. The invariant at **section 8, lines 280 and 283** (each call's timeout is the lesser of 10 s and the remaining budget; a call timeout is unavailable) fails when **the remaining total budget is small, such as 0.5 s, and a call that would take 1 s times out**. Concrete attack: **Before: binding R1 established; 40 `worker-show` calls done; 89.5 s used; `orca_available` true. Call 41 gets timeout 0.5 s and times out. After: the result is unavailable, all Orca reads stop, the report says `Orca unavailable` and `orca_available: false`, and the 10 unenriched rows print `unscanned: orca unavailable` instead of `unscanned: call bound reached`. The person is told Orca is down when it was the sweep's own budget that ran out. FR-020's "no new probe starts" once the budget is reached also does not stop a call that starts with 0.001 s left.**

- **Severity:** MAJOR. **Expert:** Whittaker, with Nygard. **Location:** Section 8, lines 280 and 283; FR-020, line 114; section 11, line 422.
- **Recommendation:** Add to section 8: "A call whose timeout was cut below 10 s by the remaining budget, and that times out, is `call_failed` with reason `unscanned: time budget reached (90 s)`, never `unavailable`; `orca_available` stays true. No call starts when less than 1 s of budget remains." Add a fixture: 89.5 s used, next call times out; assert `orca_available` true and the time-budget reason.
- **Priority:** High. **Quality impact:** Consistency +0.3, testability +0.2.

**SP-11. Sequence: an allowed `--output` makes the sweep dirty its own input.**

I can break this specification by **choosing an output directory the check allows but the inputs read**. The invariant at **FR-004, line 98** (output inside `<root>/.dev/`, not overlapping an input package or transcript directory) fails when **`--output` is `<root>/.dev/tasks/`, `<root>/.dev/tasks/to-do/`, `<root>/.dev/` itself or any other `<root>/.dev/<x>/`**. None of these equals a package directory, which is the only overlap case in the AC, and only `.dev/sweeps/` is gitignored (FR-025). Concrete attack: **Before: the root worktree is clean; `removable: could not determine`. Run 1 writes `<root>/.dev/tasks/to-do/20261108-060000-sweep.md`. After: `git status` shows an untracked file under `.dev/tasks/`; run 2 reports the root worktree `removable: no (unsaved path under .dev/tasks/)` and, if the file falls inside a package folder pattern, marks a package active. The sweep has changed what it measures (the R10 self-dirtying risk).**

- **Severity:** MAJOR. **Expert:** Whittaker. **Location:** FR-004, line 98; FR-025, line 119.
- **Recommendation:** Replace the FR-004 rule with: "`--output` must resolve to `<root>/.dev/sweeps/` or a directory below it; anything else exits 2 and writes nothing." Add AC cases: `--output <root>/.dev/`, `<root>/.dev/tasks/` and `<root>/.dev/other/` each exit 2 and write nothing; `<root>/.dev/sweeps/archive/` is accepted.
- **Priority:** High. **Quality impact:** Consistency +0.2, testability +0.2.

**SP-28. Zero and boundary: the byte limits give the wrong answer at and above the limit.**

I can break this specification by **feeding inputs at and above each byte limit**. The invariant at **section 8, line 283 and FR-020, line 114** ("a read that hits a limit marks that source unscanned") fails when **a normal transcript is larger than 256 KiB**. Concrete attack: **Before: a person session has a 3 MiB transcript and was active 10 minutes ago. The reader takes the last 256 KiB, which "hits" the tail limit. After: the transcript is marked unscanned, `transcript_readable` is not True, and the session lands in could not determine instead of Sessions, on every run, for every long session.**

Further cases from the same attack:
- Equality is undefined: is a file of exactly 1 MiB a hit or not?
- A 256 KiB tail can start mid-line or inside a multi-byte UTF-8 character, so the first record fails to parse.
- `subprocess.run(capture_output=True)` (line 279) reads all output into memory before returning, so it cannot enforce the 8 MiB limit; it can only check the size afterwards.
- A head read of a `progress.md` over 1 MiB never sees a `FINAL:` line near the end, so an archive-blocked package reads as unfinished, or as unknown if the limit makes it unscanned.

- **Severity:** MAJOR. **Expert:** Whittaker. **Location:** Section 8, lines 279 and 283; FR-020, line 114; section 7, line 262.
- **Recommendation:** Replace the byte-limit sentence with:
  - "A transcript tail read of the last 256 KiB is the normal case, not a limit hit: drop bytes up to and including the first newline, decode as UTF-8 with `errors="replace"`, and parse the remaining complete lines."
  - "A contract or ledger read is a hit when the file size is greater than 1 MiB; a hit marks that source unscanned with reason `over 1 MiB`. A ledger over 1 MiB is read as head and tail, and the tail is searched for `FINAL:`."
  - "Subprocess output is read with `Popen` in chunks; reading stops and the process is killed once 8 MiB is exceeded, giving `call_failed` with reason `output over 8 MiB`."
  - Add fixtures at limit minus 1, at the limit and at limit plus 1 for each limit.
- **Priority:** High. **Quality impact:** Testability +0.3, completeness +0.2.

**SP-29. Accumulation: workers of Runs outside the scope become person sessions.**

I can break this specification by **running the sweep with a subset of Runs while other Runs have workers in the same tree**. The invariant at **FR-010, line 104** (an unjoined transcript is True only when every scoped Run's list is complete and the join completed) fails when **a transcript belongs to a worker of Run R2 and only `--run R1` is scoped**. The guard checks completeness of the scoped Runs only, so the R2 transcript joins no row and is True. Concrete attack: **Before: R1 has 2 workers, R2 has 3 workers, all in the same worktree tree; the tab map lists all 5. Sweep with `--run R1`. After: the 3 R2 worker transcripts are `person_started` True; active ones go to could not determine with "person session, active", and those older than 6 h go to Historical sessions as if a person had started them. Over several Runs these false person sessions accumulate.**

- **Severity:** MAJOR. **Expert:** Whittaker. **Location:** FR-010, line 104; section 7, line 232.
- **Recommendation:** Add to FR-010: "A transcript that the tab map marks as an Orca worker session (any Run), or whose session id appears in any Orca row returned by `worker-list` for any Run, is never True. If the tab map records the Run id and it is outside the scope, the row is `person_started` False with note `worker of Run <id>, outside scope` and is not classified further." Add the R1/R2 fixture above. The tab map fields that carry this are UNVERIFIED until design reads the ccsession tab map format.
- **Priority:** Medium. **Quality impact:** Consistency +0.2.

**Attacks that found nothing new.**
- Zero and empty on the result classifier: empty first-call stdout is already unavailable (line 413), and an empty later body is `call_failed` (FR-026 test 3).
- Sequence on report publication: exclusive create (line 173) already prevents an overwrite race between two concurrent sweeps.
- Symlink escape on disk reads: covered by the `resolve()` rule and the F9 fixture (line 317, line 427).
- Duplicate Dispatch rows: covered by the one-identity rule (line 303, line 429).
- Window boundary: rule 7 uses strict `<` (line 249), so a session exactly at `window_start` is not idle. This is defined and testable.

## Guard Condition Boundary Table

Nygard built this table in place of Crispin. It has 16 guards with 6 rows each. Status is OK (the spec states the behaviour), GAP (the spec is silent) or CONFLICT (two parts of the spec disagree). Every GAP and CONFLICT row cites a finding of at least MAJOR severity.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--window` parse | FR-003, line 97 | Zero | `0h` | Reject | Exit 2 (AC) | OK |
| G1 `--window` parse | FR-003, line 97 | Minimum valid | `1h` | Accept | Window 1 h | OK |
| G1 `--window` parse | FR-003, line 97 | Default | `6h` | Accept | Window 6 h | OK |
| G1 `--window` parse | FR-003, line 97 | Huge | `999999999d` | Accept, then `OverflowError` | Not stated; likely exit 1 | GAP (SP-18) |
| G1 `--window` parse | FR-003, line 97 | Odd forms | `06h`, `6H`, Arabic-Indic digit | Unknown | Not stated | GAP (SP-18) |
| G1 `--window` parse | FR-003, line 97 | Equal spans | `72h` and `3d` | Accept both | Same window | OK |
| G2 Run selection | FR-002, line 96 | No `--run` | none | `run-current` | Binding, or exit 2 | OK |
| G2 Run selection | FR-002, line 96 | One Run | `--run R1` | Accept | Read R1 | OK |
| G2 Run selection | FR-002, line 96; line 280 | Two Runs, first fails | `--run A --run B`, A nonzero | Unavailable | All Orca reads stop; B never read; exit 0 | CONFLICT (SP-09) |
| G2 Run selection | Line 287; FR-018, line 112 | Id fails regex | `--run 'r;x'` | `ValueError` | Exit 1 (internal), not usage | CONFLICT (SP-09) |
| G2 Run selection | FR-002, line 96 | Duplicate | `--run R1 --run R1` | Unknown | Not stated | GAP (SP-09) |
| G2 Run selection | FR-002, line 96 | Empty | `--run ""` | Unknown | Not stated | GAP (SP-09) |
| G3 Result classifier | Line 280; FR-026, line 120 | Empty stdout, call 1 | zero exit, `""` | Unavailable | Exit 2 without `--run` | OK |
| G3 Result classifier | Line 280 | Empty stdout, later call | zero exit, `""` | `call_failed` | Row unscanned | OK |
| G3 Result classifier | Line 280 | Middle call nonzero | exit 1 on row 2 of 3 | `call_failed` | Others continue | OK |
| G3 Result classifier | Lines 279, 283 | Output over limit | 9 MiB stdout | Read whole, then checked | Limit not enforceable as written | GAP (SP-28) |
| G3 Result classifier | Line 280 | Marker in body | `body_text` holds `runtime_unavailable` | Unavailable | Global stop, false outage | CONFLICT (SP-07) |
| G3 Result classifier | Lines 280, 283 | Budget-cut timeout | 0.5 s timeout expires | Unavailable | False outage banner | CONFLICT (SP-08) |
| G4 Show cap 50 | FR-020, line 114 | Zero rows | 0 | No show calls | Empty sections print fixed text | OK |
| G4 Show cap 50 | FR-020, line 114 | One row | 1 | 1 show call | Normal | OK |
| G4 Show cap 50 | FR-020, line 114 | Exactly at cap | 50 rows | 50 calls | Whether the cap line prints is not stated | GAP (SP-10) |
| G4 Show cap 50 | FR-020, line 114 | Over cap | 60 rows | 50 calls, 10 bound | `bound_reached == 10` (AC) | OK |
| G4 Show cap 50 | FR-020, line 114 | Two Runs | 40 rows in A, 40 in B | Order-dependent | A gets 40, B gets 10; fairness not stated | GAP (SP-10) |
| G4 Show cap 50 | Line 300 | Duplicate Dispatch | same id twice | Deduplicated | One show call | OK |
| G5 Time budget 90 s | Line 283 | Zero remaining | 0 s | No new call | Remaining rows CND | OK |
| G5 Time budget 90 s | Line 283; FR-020 | Almost zero | 0.001 s | Call starts, times out | Unavailable | CONFLICT (SP-08) |
| G5 Time budget 90 s | FR-020 AC | Partial | 20 s remaining | Timeout at most 20 s | As AC | OK |
| G5 Time budget 90 s | FR-020; line 279 | Git and disk time | 30 worktrees, slow disk | Unknown | Not stated whether counted | GAP (SP-10) |
| G5 Time budget 90 s | Lines 280, 283 | Slow single call | 10 s exactly | Timeout | Unavailable on any call | CONFLICT (SP-08) |
| G5 Time budget 90 s | NFR-007, line 136 | Over skill timeout | 125 s total | Bash call killed | No report; not stated | GAP (SP-10) |
| G6 Page of 100 | Line 304 | Zero rows | 0 | Not truncated | Normal | OK |
| G6 Page of 100 | Line 304 | Under page | 99 | Not truncated | Normal | OK |
| G6 Page of 100 | Line 304 | Full page | 100 | `truncated` | Lower-bound line | OK |
| G6 Page of 100 | Line 304 | Over page, before capture | 101 | 100 seen, `truncated` | Lower-bound line | OK |
| G6 Page of 100 | Line 305 | Over page, after capture | 101 | Two list calls | Gated AC | OK |
| G6 Page of 100 | Line 303 | Duplicate on page | same Dispatch, two states | One identity | Conflict reason | OK |
| G7 `--output` check | FR-004, line 98 | Empty | `--output ""` | Resolves to cwd | Outside `.dev/`: exit 2 | OK |
| G7 `--output` check | FR-004, line 98 | `.dev` itself | `<root>/.dev` | Accept | Report not gitignored; self-dirtying | GAP (SP-11) |
| G7 `--output` check | FR-004, line 98 | Default | `<root>/.dev/sweeps/` | Accept | Gitignored (FR-025) | OK |
| G7 `--output` check | FR-004, line 98 | Other `.dev` child | `<root>/.dev/other/new/` | Accept, creates dirs | Not gitignored | GAP (SP-11) |
| G7 `--output` check | FR-004, line 98 | Tasks tree | `<root>/.dev/tasks/` | Accept (not equal to a package dir) | Dirties `.dev/tasks/` | CONFLICT (SP-11) |
| G7 `--output` check | FR-004, line 98 | Symlink escape | link to `/tmp` | Reject | Exit 2 (AC) | OK |
| G8 Report collision | Section 5.3, line 172 | No collision | new name | Create | Write | OK |
| G8 Report collision | Section 5.3, line 172 | One collision | name exists | Suffix | Suffix format not stated | GAP (SP-06) |
| G8 Report collision | Section 5.3, line 172 | Many collisions | 100 runs, same `now` | Suffix loop | No bound stated | GAP (SP-06) |
| G8 Report collision | Section 5.3, line 173 | Concurrent writers | two sweeps race | Exclusive create | One wins, other suffixes | OK |
| G8 Report collision | FR-017, line 111 | Same `now` twice | 2 runs | Two files | As AC | OK |
| G8 Report collision | Section 5.3, line 177 | Exit 1 after reserve | write fails midway | Unknown | Open gap G-1 (recommended answer below) | OK |
| G9 Idle rule | Rule 7, line 249 | No timestamp | `last_activity` None | Not idle | Never idle | OK |
| G9 Idle rule | Rule 7, line 249 | Equal | `last_activity == window_start` | Not idle (strict `<`) | Defined | OK |
| G9 Idle rule | FR-010, line 104 | Old | 8 h, window 6 h | Idle | Historical | OK |
| G9 Idle rule | FR-003; line 227 | Huge window | `999999999d` | Overflow | Not stated | GAP (SP-18) |
| G9 Idle rule | Rule 7, line 249 | Future | `last_activity > now` | Not idle | Age display negative (SP-26, MINOR) | OK |
| G9 Idle rule | FR-007, line 101; line 232 | Source of time | mtime or last record | Unknown | Not stated | GAP (SP-15) |
| G10 `person_started` | FR-010, line 104 | No transcripts | 0 | None to classify | Normal | OK |
| G10 `person_started` | FR-010, line 104 | One unjoined, complete join | 1 | True | Person session | OK |
| G10 `person_started` | FR-010, line 104 | Truncated list | 100-row page | None | CND with reason | OK |
| G10 `person_started` | FR-010, line 104 | Outage | Orca unavailable | None | CND with reason | OK |
| G10 `person_started` | FR-010, line 104 | Empty tab map | read, zero entries | Every worker True | No consistency check | GAP (SP-16) |
| G10 `person_started` | FR-010, line 104 | Other-Run worker | `--run R1`, R2 transcript | True | False person session | CONFLICT (SP-29) |
| G11 Byte limits | Line 283 | Empty file | 0 bytes contract | Read | Parse as empty | OK |
| G11 Byte limits | Line 283 | Under limit | 500 KiB contract | Read | Normal | OK |
| G11 Byte limits | Line 283 | Large transcript | 3 MiB | Tail "hits" limit | Unscanned every time | CONFLICT (SP-28) |
| G11 Byte limits | Line 283 | Exactly at limit | 1 MiB contract | Unknown | Hit or not, not stated | GAP (SP-28) |
| G11 Byte limits | Line 283 | Partial line | tail starts mid-record or mid-UTF-8 | Parse error | Not stated | GAP (SP-28) |
| G11 Byte limits | Lines 262, 283 | Large ledger | 2 MiB, `FINAL:` at end | Head read misses it | Wrong package state | GAP (SP-28) |
| G12 Rule 1 `blocked_contract` | Line 243 | No contract | None | Decline | Later rules | OK |
| G12 Rule 1 `blocked_contract` | Line 243 | Settled row | blocked, settled | Match | Waiting (a) | OK |
| G12 Rule 1 `blocked_contract` | Line 243 | Policy report blocked | `gate_policy == "report blocked"` | Match | Waiting (a) | OK |
| G12 Rule 1 `blocked_contract` | Line 243 | Ruling halt | `E-HALT-QA` | Match | Waiting (a) | OK |
| G12 Rule 1 `blocked_contract` | Lines 243, 246 | Policy None, wait set | live, `agent_wait` non-null | CND | Rule 4(a) never reached | CONFLICT (SP-13) |
| G12 Rule 1 `blocked_contract` | Line 243 | No Orca row | contract only | Unknown | "Orca row settled" undefined | GAP (SP-13) |
| G13 Package state | Lines 260-265 | Empty package dir | no files | Unknown | Ledger unreadable: unknown | OK |
| G13 Package state | Line 265 | Missing ledger | no `progress.md` | Unknown | Prints CND | OK |
| G13 Package state | Line 263 | Unfinished | ledger, no `FINAL:` | Unfinished | Blocks removal | OK |
| G13 Package state | Lines 262, 283 | Large ledger | over 1 MiB | Unscanned or wrong | Not stated | GAP (SP-28) |
| G13 Package state | Line 262 | Marker in note | `- will write FINAL: later` | Archive-blocked | False state | CONFLICT (SP-07) |
| G13 Package state | Lines 260-261 | Both locations and marker | `to-do/`, `done/`, `.archiving` | Conflict first | Precedence stated | OK |
| G14 Shared package | FR-015, line 109 | None active | 0 | Not shared | Normal | OK |
| G14 Shared package | FR-015, line 109 | One worktree | 1 | Not shared | Normal | OK |
| G14 Shared package | FR-015, line 109 | Three worktrees | 3 | Shared | One line naming all 3 | OK |
| G14 Shared package | FR-015; line 309 | Collapsed untracked | `?? .dev/` | Package not seen | Activity hidden | GAP (SP-17) |
| G14 Shared package | Line 309 | Quoted path | `"\303\251 x/"` | Parse unknown | Not stated | GAP (SP-17) |
| G14 Shared package | FR-015, line 109 | Change in `done/` | `M .dev/tasks/done/<id>/x` | Active | Counts as activity | OK |
| G15 Branch header | Line 309 | Unborn branch | `## No commits yet on b` | Unknown | Not stated | GAP (SP-17) |
| G15 Branch header | FR-013, line 107 | In sync | `## b...origin/b` | Not unpushed | Normal | OK |
| G15 Branch header | FR-013, line 107 | Ahead | `[ahead 2]` | Unpushed | `removable: no` | OK |
| G15 Branch header | FR-013, line 107 | Ahead and behind | `[ahead 1, behind 3]` | Unpushed | `removable: no` | OK |
| G15 Branch header | Line 309 | Upstream gone | `[gone]` | Unknown | Not stated | GAP (SP-17) |
| G15 Branch header | Line 309 | Detached | `## HEAD (no branch)` | Unknown | Not stated | GAP (SP-17) |
| G16 `--root` walk | FR-004, line 98 | No `.git` above cwd | walk reaches `/` | Unknown | Not stated | GAP (SP-18) |
| G16 `--root` walk | FR-004, line 98 | cwd is root | `.git` folder here | Root = cwd | Normal | OK |
| G16 `--root` walk | FR-004, line 98 | Subdirectory | cwd 3 levels down | Walk up | First `.git` | OK |
| G16 `--root` walk | FR-004, line 98 | Submodule | `.git` file in submodule | Submodule is root | First `.git` wins (stated) | OK |
| G16 `--root` walk | FR-004, line 98 | Linked worktree | `.git` file | Accept | AC | OK |
| G16 `--root` walk | FR-004, line 98 | Bad explicit root | `--root /nonexistent` | Unknown | Not stated | GAP (SP-18) |

## Pipeline Dimensional Analysis: Quantity Flow Diagram

This traces each quantity from its producer to every consumer and checks that the unit matches at each step (protocol FR-17 to FR-21).

```text
ORCA SIDE (per scoped Run)
  worker-list --run R            N rows       unit: Orca row (Task/Dispatch)   cap: 100 per call (line 304)
     | dedupe Dispatch ids (line 300)
     v
  N' distinct rows               unit: Orca row
     | worker-show, at most 50 in total across all Runs (FR-020)
     v
  min(N', 50) enriched + max(0, N' - 50) unenriched   -> summary.bound_reached  (unit: Orca row)

DISK SIDE
  transcripts in scanned keys    T files      unit: transcript (session)
     | join through tab map to Orca rows (FR-010)
     v
  J joined (worker sessions)  +  P unjoined (person_started True / False / None)
     | window test (rule 7, line 249)
     v
  P_visible + P_historical       unit: session

  worktrees under root           W            unit: worktree
     | one git status each (line 309)
     v
  WorktreeState x W, PackageRecord x K        unit: worktree, package

CONSUMERS
  JSON rows[]                    SessionRow    unit: session     = N' + P (rows each carry a session class)
  JSON summary.total             count         unit: session
  JSON summary.bound_reached     count         unit: Orca row (subset of sessions)
  JSON (no key)                  -             worktrees W and packages K never reach JSON   <-- SP-05
  Report header sessions <s>/<t> count         unit: session
  Report Worktrees section       W rows        unit: worktree
  FR-005 AC                      "6 rows in JSON"  unit: session + worktree                   <-- MISMATCH
```

**Checks:**

| Step | Producer unit | Consumer unit | Result |
|---|---|---|---|
| `worker-list` to dedupe | Orca row | Orca row | Match |
| Dedupe to `worker-show` cap | Orca row | Call count | Match; the cap counts calls, one per row |
| Cap to `summary.bound_reached` | Orca row | Count | Match; "reached" undefined at exactly 50 (SP-10) |
| Join to `rows[]` | Session | Session | Match, provided the join key is defined (SP-16) |
| Worktree scan to JSON | Worktree | none | **No consumer in JSON**: Phase 2 cannot read worktree state (SP-05) |
| Fixture to FR-005 AC | 3 sessions + 1 session + 2 worktrees | "6 rows in JSON" | **CRITICAL dimensional mismatch**: 4 session rows, plus 2 worktrees that JSON cannot hold (SP-05) |
| Header `<shown>/<total>` vs AC | Session | Session + worktree | **Mismatch**: the AC's "equal" compares a 4 with a 6 (SP-05) |
| Page cap 100 to `summary.total` | Orca row (lower bound) | Session total | Match, but `total` gives no lower-bound flag in JSON; SP-05 recommends `summary.total_is_lower_bound` |

The only dimensional mismatch is SP-05. It is CRITICAL under the protocol rule.

## Section 15 consistency check

GQ-101 to GQ-113 were decided before this review. The panel checked section 15 (lines 515-530) only for consistency with the rest of the spec and with the INV-005 conditions.

| GQ | Section 15 says | Consistent? | Note |
|---|---|---|---|
| GQ-103(1) | `--no-optional-locks` plus `GIT_OPTIONAL_LOCKS=0`, built first (line 517) | Yes | Matches section 8 line 278 and NFR-002 |
| GQ-101 | Only packages active in a worktree count (line 518) | Yes | FR-015 parsing gaps are SP-17, not a conflict with GQ-101 |
| GQ-102 | `conflict` state (line 519) | Yes | Matches line 260 |
| GQ-103(2) | Window in `SweepContext` (line 520) | Yes | The `window_start` formula is missing (SP-18) |
| GQ-103(3) | `gate_policy` "from the Task spec" (line 521) | **No** | The Task spec is read through `task-list` (line 295), which INV-005 condition 1 forbids. Without it `gate_policy` has no source (SP-01, SP-13). Recommended text: "`gate_policy` (source: a `worker-show` field captured at step 1.0a, UNVERIFIED; None when absent)". |
| GQ-104 | No `run-list` fallback (line 522) | Yes | |
| GQ-105 | `archive-blocked` from a `FINAL:` line (line 523) | Yes | Matching rule is SP-07 |
| GQ-106 | `.dev/sweeps/` ignored (line 524) | Yes | Only that path is ignored, which is why SP-11 restricts `--output` to it |
| GQ-107 | `sanitize()` escapes pipes (line 525) | Yes | |
| GQ-108 | Person-started definition (line 526) | Yes | SP-29 adds an out-of-scope Run rule without changing GQ-108 |
| GQ-109 | `gate-list`, `worker-read` and stash removed (line 527) | **Incomplete** | Condition 1 also removes `task-list` (both templates) and `worktree ps`. Recommended text: "`gate-list`, `worker-read` and stash removed (GQ-109); `task-list` and `worktree ps` removed under INV-005 condition 1 (section 13)". Covered by SP-01. |
| GQ-110 | One `git status --porcelain --branch` per worktree (line 528) | Yes | SP-17 recommends adding `-z` and `--untracked-files=all` to that one call, which keeps it one call |
| GQ-111 to GQ-113 | Carried, not fixed (line 530) | Yes | |

## Expert consensus and disagreements

**Consensus.**
- The safety stance is right: read-only, coordinator-only, unknown stays unknown, and no action is ever suggested. No expert asked to weaken it.
- The three-stage split (collect, classify, render) with pure functions over frozen values is the spec's strongest design choice and makes almost every finding cheap to test.
- The owner's INV-005 conditions must become testable requirements before design, not prose (SP-01, SP-02, SP-03).
- Machine output must carry everything a later phase acts on, including worktree state (SP-05).

**Disagreements.**
- **Person sessions in could not determine (SP-14).** Cockburn wants a separate `person session (active)` class, because a known healthy state labelled "could not determine" trains the reader to skip that section. Fowler prefers to keep the class set fixed for v1 and only move the note. Outcome: the panel recommends the new class now, because section 6 (line 214) extends `RULES` only by insertion and a later insertion shows as a reorder under NFR-010.
- **Timeout classification (SP-08).** Nygard first argued that any timeout should stop Orca reads, since a hung Orca can cost the whole budget. Hohpe answered that a timeout the sweep caused by cutting the budget says nothing about Orca's health. Outcome: only a full 10 s timeout counts as unavailable; a budget-cut timeout is `call_failed`.
- **Severity of SP-01.** Adzic noted that section 8 already says a template that fails the step 1.0a capture is dropped (line 307), so design could fix it. Wiegers answered that the conflict is with a signed-off owner condition, not with an unverified shape, and that design should not have to resolve a contradiction in its input. Outcome: CRITICAL.

## Improvement roadmap

**Immediate (spec owner, before `/sc:design`):**
1. SP-01: replace the Orca allowlist with the five INV-005 verbs; name replacement sources or drop rule 4(b); add the exact-set pin and negative tests.
2. SP-02: name the Orca version source for the lock line, or return condition 2 to the owner.
3. SP-03: bring lines 26, 460 and 590 and the section 17.1 checklist into line with the sign-off.
4. SP-04: change the NFR-009 AC to a subset-and-type test.
5. SP-05: add `worktrees` to JSON, fix the FR-005 AC to 4 rows plus 2 worktrees, and state the reconciliation formula.

**At `/sc:design`:**
- Input and result handling: SP-07, SP-08, SP-09, SP-11, SP-18, SP-28.
- Budgets and runtime: SP-10, SP-12.
- Classification and joins: SP-13, SP-14, SP-15, SP-16, SP-29.
- Parsing and output: SP-06, SP-17.
- Record the G-1 answer and the SP-20 module move together, because one depends on the other.

**Later (before release, low risk):**
- MINOR findings: SP-19, SP-20 (unless taken with G-1), SP-21, SP-22, SP-23, SP-24, SP-25, SP-26, SP-27.

## Findings index

| ID | Severity | Expert | Section and line | Issue |
|---|---|---|---|---|
| SP-01 | CRITICAL | Fowler, Newman | Section 8, lines 289-296, 307; section 13, line 470 | Orca allowlist contradicts INV-005 condition 1 |
| SP-02 | MAJOR | Fowler | Section 9, lines 337, 344; section 13, line 471 | Version-scoped lock line has no version source; "always printed" conflicts |
| SP-03 | MAJOR | Wiegers | Lines 9, 26, 460, 582-590 | Gate text and checklist not updated after sign-off |
| SP-04 | CRITICAL | Wiegers | NFR-009, line 138 | AC forbids the additions the requirement allows |
| SP-05 | CRITICAL | Wiegers, Fowler | FR-005, line 99; lines 162, 369 | Dimensional mismatch: rows vs sessions plus worktrees; no worktree data in JSON |
| SP-06 | MAJOR | Fowler | NFR-005, line 134; section 5.3, lines 171-177 | Byte identity vs `report_path` and collection interval; no suffix format or bound |
| SP-07 | MAJOR | Whittaker | Line 280; lines 248, 262 | Substring sentinels: `runtime_unavailable`, `guard refused:`, `FINAL:` |
| SP-08 | MAJOR | Whittaker, Nygard | Lines 280, 283; FR-020, line 114 | Budget-cut timeout reported as a global Orca outage |
| SP-09 | MAJOR | Adzic | FR-002, line 96; lines 279-280, 287 | `--run` typo looks like an outage; regex failure is exit 1; empty and duplicate values undefined |
| SP-10 | MAJOR | Nygard | Line 283; FR-020, line 114; NFR-007, line 136 | Git and disk time unbudgeted; 120 s not shown; cap not fair across Runs; "reached" undefined |
| SP-11 | MAJOR | Whittaker | FR-004, line 98; FR-025, line 119 | `--output` inside `.dev/` but outside `.dev/sweeps/` dirties the sweep's own input |
| SP-12 | MAJOR | Nygard | FR-022, line 116; NFR-001, line 130 | `uv run` fallback can sync the environment |
| SP-13 | MAJOR | Fowler | Rules 1 and 4(a), lines 243, 246 | Rule 1 hides rule 4(a); no branch when no Orca row |
| SP-14 | MAJOR | Cockburn | Rule 8, line 250; rule 4(b), line 246; line 54 | Healthy person sessions and ready Tasks crowd the "who needs me" view |
| SP-15 | MAJOR | Wiegers | FR-011, line 105; line 232; FR-007, line 101 | Age and `last_activity` sources undefined |
| SP-16 | MAJOR | Newman, Hohpe | FR-010, line 104; line 232 | No stable row ID or join key; empty tab map makes workers person sessions |
| SP-17 | MAJOR | Newman | Lines 309-313; FR-015, line 109 | Porcelain parsing and branch header cases unspecified |
| SP-18 | MAJOR | Adzic | FR-003, line 97; FR-004, line 98; line 227 | No `--window` maximum or ASCII rule; no `window_start` formula; no `--root` validation |
| SP-19 | MINOR | Wiegers | FR-002, line 96; FR-019, line 113 | Same paragraph repeated three times |
| SP-20 | MINOR | Fowler | Section 6, line 197; NFR-004, line 133 | `write_report` needs `os`, which the AST test forbids in `report.py` |
| SP-21 | MINOR | Adzic | Line 505; section 5.1 | Exit-2 message hides the unavailable reason |
| SP-22 | MINOR | Nygard | Section 5.3; line 83 | No retention rule for `.dev/sweeps/` |
| SP-23 | MINOR | Nygard | Section 9, lines 350-363 | No length cap on report cells |
| SP-24 | MINOR | Hohpe | Section 7, lines 243-250 | Rule 5 wording; field sources; unreachable classes not footnoted |
| SP-25 | MINOR | Wiegers | FR-022, line 116; FR-020, line 114; line 422 | `allowed-tools` literals unnamed; one reason for two bounds |
| SP-26 | MINOR | Adzic | Line 232; FR-011, line 105 | Future timestamp gives a negative age |
| SP-27 | MINOR | Cockburn | Section 10, line 384 | WC-14 end condition not observable by the sweep |
| SP-28 | MAJOR | Whittaker | Lines 279, 283; FR-020, line 114; line 262 | Byte limits wrong at and above the limit; large transcripts always unscanned |
| SP-29 | MAJOR | Whittaker | FR-010, line 104 | Workers of out-of-scope Runs become person sessions |

Totals: CRITICAL 3 (SP-01, SP-04, SP-05), MAJOR 17, MINOR 9.

## Self-audit

**Checked.**
- The SPEC was read in full, in chunks of at most 150 lines. Sections cited in findings (3, 4, 5.2, 5.3, 6, 7, 8, 9, 11, 15, 17.1) were re-read before their findings were finalised.
- `tests/skills/test_worker_contract.py`: `NEVER_AS_WORKER` holds 8 entries today (lines 245-254), so FR-023's "9-entry" list after adding `/sc:sweep` is consistent.
- `WORKER-CONTRACT.md` lines 101-160 (ready Task at line 129, refusal condition at line 108) and WC-9 at line 44 match the SPEC's citations.
- `src/superclaude/cli/recommend/__init__.py` lines 12-20 hold the lazy `__getattr__` pattern the SPEC cites for `sweep/__init__.py`.
- `uv run --help` lists `--no-sync`, `--locked` and `--frozen`.
- Every GAP and CONFLICT row in the boundary table cites a finding of MAJOR severity or higher.
- The SPEC and every other file were left unchanged; only this review file was written.

**UNVERIFIED.**
- `~/.claude/skills/orca-cli/SKILL.md` exists, but lines 24-27 (bare `orca` and the screen reader) were not read; the SPEC's citation of them is taken as given.
- uv's default sync behaviour for `uv run` (SP-12) is from uv's documentation as the panel knows it; it was not run in this repo.
- Orca JSON shapes: the `runtime_unavailable` field, `agentWait`, the version field, `worker-show` field names and the unknown-Run error shape (SP-01, SP-02, SP-07, SP-09). All wait on step 1.0a.
- The ccsession tab map format and whether it records a Run id (SP-16, SP-29).
- Python `OverflowError` for a huge `timedelta` (SP-18) was not run against the final parser.
- Hard-link support on every user filesystem (G-1 answer).
- The variant files (V1, V2, V3 and their reviews) and the REPORT and GAPS line citations inside the SPEC were not opened; the review treats the SPEC's text as the claim under review.

**Limits of this review.** No code exists yet, so every finding is about the text. Line numbers refer to the 616-line SPEC as read on 2026-11-08 and will move when the SPEC is edited.
