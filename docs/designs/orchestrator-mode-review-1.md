# Orchestrator mode design: adversarial review 1

## Verdict

**FAIL.** 3 blocking findings (B1 to B3) and 11 minor notes.

**What was reviewed.** `docs/designs/orchestrator-mode.md` (DESIGN), checked against these sources:

- `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (SPEC)
- GAPS lines 124-138
- REPORT section 8 Phase 1
- the inv-005 evidence

The review was done on 2026-11-08 by an independent reviewer who did not write the design. No file other than this one was changed.

**What is sound.** The G-1 publish (temp file, `fsync` and `os.link`), the eight-template and seven-verb allowlist, the lock-free `_git` seam and the JSON v1 set. Almost every claim about existing code checks out.

**Why it fails.** There are three problems:

- One publish path breaks NFR-001 and the design's own test (B1).
- The design silently narrows FR-010 (B2).
- A set of SPEC behaviours and acceptance fixtures never reaches the design (B3). `/task-builder` builds from section 11, so it would drop them.

## Traceability check

Section 12 (lines 727-773) maps all 26 FRs, all 15 NFRs, G-1 and the GQ rows to a design element and a test file. No requirement ID is missing. However, a requirement having a row does not mean its acceptance criteria are covered:

- Several SPEC ACs and failure-mode fixtures named under a mapped requirement do not appear in the section 11 case lists (B3).
- NFR-001 maps to `sweep/test_readonly.py`, but the DESIGN permits an exit-0 state that the same test forbids (B1).
- FR-010 maps to `sweep/test_classify.py`, but the design narrows the FR-010 definition (B2).
- FR-020 maps to `test_probes_allowlist.py` only, although `test_report.py` (line 716) also covers the FR-020 header line (m4).

## Deviations check

D1 to D8 (lines 779-790) each name the SPEC text they change, give a source (SP-20, G-1/PANEL, SP-21, SP-23, SP-26, SP-27, SP-24, M7) and give a section.

| Deviation | Finding |
|---|---|
| D1 (`write_report` removed; the only write is `commands._publish`) | Consistent with section 3 and with the AST import test (line 715), and recorded in the REPORT differences row for step 1.5. OK. |
| D2 (temp file plus link as the commit point) | Stricter than SPEC line 453, and it closes G-1. But it introduces a post-commit unlink-failure state that leaves two names on disk with exit 0, and that state is not recorded (B1). |
| D3 (the reason is added inside the parentheses of the FR-002 and FR-019 message) | Declared, but no test is named that pins the new literal (m7). |
| D4, D5, D7, D8 | Consistent with sections 7.2, 7.4 and 7.5. OK. |
| D6 (a sentence appended to WC-14 saying the coordinator records each admission or rejection in its run notes) | Declared, with "No new pin". The sentence adds a coordinator duty to a shared contract, and SPEC section 10 says owner approval of this text is still required. Step 1.17 is gated on 1.0b (GQ-11), which is acceptable, but the D6 sentence is not pinned (m8). |

Silent deviations, not in D1 to D8:

- **Section 7.2 lines 487-488.** A transcript with any tab-map entry is never `person_started` True. This narrows FR-010 (SPEC line 104). Line 795 records only the False path (B2).
- **Section 3.2 line 122.** A failed unlink after the commit point exits 0 and leaves a second file. This breaks the NFR-001 AC (SPEC line 130) (B1).
- **Line 794.** It calls the nesting of `summary.counts` an "addition". It is really a structural choice inside a new v1 schema. NFR-009 allows that, so it is not a deviation, but the wording is loose (m9).

## G-1 mechanism

Section 3 (lines 96-149) publishes in this order:

1. `makedirs`, then re-resolve the escape check.
2. Open the temp file with `O_EXCL`.
3. Write, `fsync`, close.
4. `os.link` to `stem.md`, then `stem-2.md` up to `stem-99.md`; `FileExistsError` moves to the next name.
5. Unlink the temp file.

**Correct parts.**

- The crash table (lines 129-134) and the reuse argument (lines 138-141) are correct.
- `O_EXCL` refuses a pre-planted symlink at the temp name (line 101).
- A link error other than `FileExistsError` exits 1 with no fallback (line 120).
- No run deletes a file it did not create.
- The exit-1 rule (line 147) closes SPEC G-1 (lines 637-645) for every exit-1 path before the commit point.

**One defect, at line 122:** "Unlink of the temp file fails after the commit point ... the report is published and the run exits 0".

- On that exit-0 path the disk holds the report plus `.<stem>.<pid>.tmp`, which is two added names. NFR-001 says "exactly one added file" (SPEC line 130).
- It contradicts the design's own `test_readonly.py` case "no temp file remains after exit 0" (line 713).
- The section 3.4 rule (line 147) does not cover it.
- No `test_cli_contract.py` case covers it (line 718).
- Line 7 ("The only runtime filesystem write is one dated report") is also inaccurate, because the temp file and the link are runtime writes.

This is B1.

Filesystems without hard links get a permanent exit 1. The design marks that as UNVERIFIED (m10).

## GQ resolutions

- The GQ-101 to GQ-113 rows (DESIGN lines 50-64) match GAPS lines 124-138 one for one. Each row names a design element and a SPEC anchor.
- GQ-111 to GQ-113 are carried with no REPORT edit, which follows the GAPS carry rule.
- These rows are reflected in sections 7, 10 and 11:
  - GQ-102: conflict is checked first.
  - GQ-105: a line starting `FINAL:` after optional leading whitespace, and the head and tail ledger read.
  - GQ-106: the `.gitignore` line.
  - GQ-107: the pipe escape.
  - GQ-109: no `gate-list`, `worker-read` or `stash`, plus the forbidden tokens.
- GQ-108 (the join) is resolved in section 7.2, but that resolution carries the B2 narrowing.
- Nothing in the design contradicts the GAPS row count (113 rows, 88 open, 25 resolved, GAPS line 138).

## Allowlist and live-run check

**Allowlist: no findings.**

- `ALLOWED_ORCA` (lines 497-506) has 8 templates and 7 verbs.
- `worktree list` and `worktree current` are pinned but never called.
- This matches the SPEC section 13 seven-verb condition (SPEC lines 495-504).
- `FORBIDDEN_TOKENS` (line 508) holds `--include-remote` and `--agent-wait`, and they are rejected in any position.
- The FR-021 forbidden verb list is held in the test, as the SPEC asks.
- `ALLOWED_GIT` holds one template, `status --porcelain=v1 -z --branch --untracked-files=all`, run as `git --no-optional-locks -C <path>` with `GIT_OPTIONAL_LOCKS=0`. This matches NFR-002 and the inv-005 evidence that optional locks are the source of the index lock.
- The negative cases (line 714) cover all of these:
  - `check`, `inbox`, `worker-read` and `gate-list`
  - an extra flag
  - both forbidden tokens
  - `run-list`
  - the git negatives, including every `stash` form

**Live-run check.**

- **Step 1.0a** reads only through the 8 templates, against an existing Run that the person names (line 877).
- **The REPORT differences row for 1.0a** (line 801) drops `worker-read` and the throwaway Run. That is correct under SPEC section 17.1, which leaves out the live disposable-Run check.
- **Step 1.4** keeps a live check, saved to `artifacts/sweep-live-check-1.4.json`, and drops only the `--include-remote` timing (lines 802 and 883).
- **The design gives no pass rule for the step 1.4 check.** Line 873 lets the REPORT text apply where the design is silent, so it inherits the pass rule from REPORT step 1.4:
  - exit 0, inside the 120000 ms budget;
  - every row has a class;
  - each class matches the recorded `worker-list` state;
  - no probe-error rows.

  It can be built, but the pass rule should be stated rather than left to inference (m6).

## Interfaces consistency

Consistent:

- These agree with each other and with the section 5 exit codes:
  - the section 7.1 signatures
  - the section 7.2 models and constants (line 461)
  - the section 7.3 seams
  - the section 7.4 JSON v1 key set (lines 534-566)
- The worktrees keys match SPEC line 392 exactly. The additions (`collected`, `waiting_kind`, `policy`, `person_started` and the nested `summary.counts`) are declared at line 794.
- `PACKAGE_STATES` precedence starts with `conflict`, as GQ-102 requires.

Inconsistent:

- Line 41 says "Callers pass only `cwd`". That disagrees with the `commands.run` signature at line 379 (m1).
- The section 7.2 joins carry the B2 narrowing.
- Several SPEC behaviours have no home in any interface or rule (B3):
  - the `parent` note
  - the SP-16 literal
  - the re-read when an input changes
  - the duplicate-Dispatch conflict
  - "show wins"
  - the outside-root rejection for discovered paths

## Existing-system claims

Each claim was checked on 2026-11-08 with grep or reads of 150 lines or fewer.

| Claim (DESIGN line) | Result | Evidence |
|---|---|---|
| `src/superclaude/cli/sweep/` does not exist (21) | VERIFIED | `ls` reports no such directory |
| `main.py` deferred registrations at 519-561; reflect at 559 and 561; `__main__` at 564 (22) | VERIFIED | sprint import at 519, reflect import with noqa at 559, `add_command` at 561, guard at 564-565 |
| `recommend/__init__.py:12-20` lazy `__getattr__` (23) | VERIFIED | `def __getattr__` at 12, raise at 18, `__all__` at 21 |
| The tab map is one file per pane, three lines, no Run id (26) | VERIFIED | `src/superclaude/skills/ccsession-tag/ccsession` lines 562-604 write `session`, `folder`, `ORCA_TERMINAL_HANDLE`; README line 359 |
| `graph.md` line 9 is `allowed-tools: Skill, ...` and line 41 is `## Activation` (623) | VERIFIED | Both lines as stated |
| `issue.md` has the headings Triggers, Usage, Options (623) | VERIFIED | Lines 22, 26, 33 |
| WORKER-CONTRACT never-as-worker list at 23, fan-in paragraph at 156, worked example at 158 (639, 662) | VERIFIED | Lines 23, 154-156, 158 |
| `test_worker_contract.py` pins at 25, 155, 245-254 (8 entries), 398, 470, 545, 624, 865 (653-662) | VERIFIED | All lines as stated |
| `pyproject.toml` has `--strict-markers` and registers `integration` (707) | VERIFIED | Lines 114 and 119 |
| `tests/cli/reflect/conftest.py` is the precedent for patching seams (706) | VERIFIED | The file exists |
| HOW-WE-WORK `other-commands:v1` at 318, `/sc:spawn` at 333, `## Orca coordination` at 396, never-workers bullet at 403 (670-671) | VERIFIED | Lines as stated |
| Plugin copy, and `test_routing_plugin_parity.py` line 38 `filecmp.cmp(..., shallow=False)` (672) | VERIFIED | Line 38 as stated |
| `_OTHER_COMMANDS` at line 27; `_POST_REFRESH_ADDITIONS` at line 33 with its assertion at 648 (673-674) | VERIFIED | Current value `{"graph", "impact", "issue"}` |
| User guide `### 8. UTILITIES` at 105 and `/sc:issue` row at 115 (675) | VERIFIED | Lines as stated |
| Developer guide line 991 copies the never-as-worker list (676) | VERIFIED | Line 991 as stated |
| `CHANGELOG.md` `## [Unreleased]` at line 5 (677) | VERIFIED | Line 5 |
| `.gitignore` has `.dev/sprint-state/` at 254 and no `sweeps` entry (688) | VERIFIED | Line 254; grep finds no `sweeps` entry |
| "The only runtime filesystem write is one dated report" (7) | FALSE as worded | The temp file and `os.link` are runtime writes, and line 122 can leave the temp file behind (B1) |
| The SP-29 False path cannot occur because the tab map holds no Run id (795) | VERIFIED as a fact | `ccsession` line 563. The conclusion drawn from it at line 487 is B2 |

## Primitive path rule

- Section 7.6 (lines 618-633) keeps every `src/superclaude/` path out of the text of the two new primitives.
- The command's Activation block names `~/.claude/skills/sc-sweep-protocol/SKILL.md` first and the project `.claude/` copy second. That is the dual-surface precedence for skills.
- R2's bullet names `~/.claude/WORKER-CONTRACT.md`.
- `test_sweep_command.py` asserts that no `src/superclaude/` substring appears, and step 1.28 runs the CLAUDE.md grep.
- Every `src/superclaude/` hit in DESIGN is a place a maintainer edits, not text that goes into a primitive.

No violation.

## Step mapping

**Coverage.** Section 15.2 (lines 871-911) keeps the REPORT numbering and maps every step:

- 1.0a and 1.0b
- 1.1 to 1.13, including the new step 1.4a
- 1.14 to 1.16, then 1.16a
- 1.17 to 1.24, then 1.24a and 1.24b
- 1.25 to 1.29

The brief says the REPORT steps run from 1.0a to 1.26. The REPORT also has 1.27 (tests), 1.28 (the primitive path grep) and 1.29 (pipx help), and the design maps those as well. Not a defect.

**Gates.**

| Step | What it is | Check |
|---|---|---|
| 1.0a | Pre-implementation, read-only, against an existing Run that the person names. Gates step 1.4 (parsers and regexes) and step 1.8 (captured fixtures). | Correct |
| 1.0b | Owner decisions recorded in `artifacts/owner-decisions.md`. Gates step 1.17. | Correct |
| 1.16a | `gh pr view 422 --repo IronbellyOrg/IronClaude`, which names the fork as required. Must finish before step 1.17. | Correct |
| 1.4a | Puts the `.gitignore` lines in with the first real-git test (reason given at line 913). | Correct |
| 1.21 and 1.23 | R1 and R3 land in one commit. | Correct |
| 1.25 | `make sync-dev` and `make verify-sync`; no `.claude/` path staged. | Correct |

**Problems.**

- Step 1.0a is described as writing only its own notes file, but it also produces the captured fixtures that step 1.8 uses (m3).
- Step 1.4 has no stated pass rule (m6).

## Blocking findings

### B1. A failed temp unlink after the commit point exits 0 with two names on disk

This breaks NFR-001 and contradicts the design's own test.

**Where:** section 3.2 line 122, section 3.4 line 147, section 11 lines 713 and 718, and line 7.

**What is wrong:**

- Line 122 says the run exits 0 while `.<stem>.<pid>.tmp`, a second link to the report bytes, is still on disk.
- The NFR-001 acceptance criterion (SPEC line 130) is "exactly one added file (plus the `--output` dir if new)".
- The design's own test says "no temp file remains after exit 0".
- The state is not a recorded deviation, is not covered by section 3.4, and is not tested.

The leftover file does no harm to readers, because the skill reads only `report_path`. But an exit 0 that breaks the read-only contract is wrong behaviour, and it leaves `/task-builder` with contradictory rules.

**Exact fix:**

1. Change row 122 to: "Unlink of the temp file fails after the commit point: stderr `[sweep publish] could not remove temp file <path>`, no success JSON, exit 1; the complete report stays."
2. Change the after-commit sentence at line 147 to: "A run that exits 1 after the commit point, because the success JSON could not be printed or its own temp file could not be removed, leaves exactly one complete report that ends in `Report complete`, plus in the second case its own dot-prefixed temp file, and prints no success JSON."
3. Add a `test_cli_contract.py` publication case. Patch `os.unlink` to raise after a successful `os.link`, then assert:
   - exit code 1;
   - no success JSON;
   - one complete report;
   - a stderr line naming the temp path.
4. Reword line 7 to: "A successful run leaves one filesystem change: one dated report under `<root>/.dev/sweeps/`, plus that directory when it is new. A dot-prefixed temp file exists only during publication (section 3)."

### B2. A person session started in an Orca pane can never be person-started

Section 7.2 narrows FR-010 without recording it.

**Where:** section 7.2 lines 487-488, line 795, and SPEC FR-010 (line 104).

**What the SPEC says.**

- FR-010 defines a person-started session as a transcript "that the ccsession tab map joins to no Orca row".
- SP-29 excludes only a transcript that the tab map "marks as an Orca worker session".

**What the tab map actually records.**

- The ccsession hook writes a tab-map entry for every Claude session in any Orca pane. That includes the person's own sessions and the coordinator's (`ccsession` lines 562-604, run at each session start and each prompt).
- So the tab map records which pane a session ran in, not whether it was a worker.

**What the design does.**

- Line 487 treats every tab-map entry as a worker mark.
- Line 488 allows True only when there is no tab-map entry at all.
- So every person session launched through `ccsession-orca` gets None. That is the usual way to start a session in this workflow.
- A None session is never idle and never goes to Historical. The FR-010 positive class therefore almost never fires in practice.

**Why it is blocking.**

- It contradicts a requirement, and it is not listed in D1 to D8. Line 795 records only the False path.
- No fixture has a person session in an Orca pane, so the existing tests still pass:
  - the SP-29 two-Run fixture;
  - the FR-010 complete-negative fixture.

**Exact fix.** Choose one option and write it into the design.

- **(a) Keep the conservative None and record it.**
  1. Add **D9**: "SPEC FR-010 and SP-29 (line 104): never True for a transcript the tab map marks as an Orca worker session. Design: the tab map cannot tell a worker pane from a person pane, so a tab-map entry that joins no scoped Orca row gives None with note `Orca pane session, not in scoped Runs`. Consequence: person sessions started in Orca panes are never idle or Historical in Phase 1."
  2. Get the owner's sign-off at step 1.0b.
  3. Add a `test_classify.py` fixture: a person session with a tab-map entry and no Orca row gives None with that note.
- **(b) Tell worker panes from person panes.**
  1. Define "marked as an Orca worker session" as: the tab-map entry's `terminal_handle` or pane key equals the terminal handle or pane of a row that `worker-list` returns for any Run. The field is named at step 1.0a.
  2. An entry that matches no worker row is a person pane. It may be True when the FR-010 guard holds.
  3. Until step 1.0a names the field, keep None with a distinct note.
  4. Add two fixtures: a worker pane gives None or False, and a person pane gives True when the guard holds.

### B3. SPEC behaviours and acceptance fixtures are missing from the design, so `/task-builder` would drop them

**Where:**

- the rules in sections 7.2, 7.3 and 7.5;
- the test cases in section 11 (lines 711-718).

A grep of DESIGN finds none of these terms:

- `parent`, `WC-13 violation`, `GQ-40`
- `guard refused`, `could not join`, `show wins`
- `re-read`, `outside root`
- `minus 1`, `limit plus`, `extra key`
- `admitted`, used as an acceptance criterion

**What is wrong.** Section 12 claims full coverage, but each item below is a SPEC requirement or a named SPEC fixture with no design rule and no test case.

Behaviours with no rule:

- **WC-13 note.** A non-null `parent` adds "WC-13 violation, review" (SPEC line 261, GQ-40), and the violation is listed under Retained problems (SPEC line 380).
- **SP-16 literal.** "could not join Orca workers to transcripts (tab map empty or stale)" (SPEC line 236).
- **Input changed between reads.** One plain re-read within budget; otherwise the row gets a conflict reason (SPEC line 451).
- **Duplicate Dispatch.** Duplicate Dispatch rows with contradictory state become one identity with a conflict reason, never last-row-wins (SPEC lines 319 and 452).
- **List and show disagree.** Show wins (SPEC line 443).
- **Symlink out of the root.** A discovered input path whose `resolve()` escapes the root is rejected and reported as `unscanned: outside root` (SPEC line 450 and REPORT step 1.6). Line 253 only says "bounded, resolve()".

Acceptance fixtures missing from section 11:

- **Byte limits.** Fixtures at limit minus 1, at the limit and at limit plus 1, for each of the three limits (SPEC line 297). The design tests only an over-limit contract and an over-limit ledger.
- **SP-07 negative.** A later body line that quotes `guard refused:` is not finished (SPEC line 259).
- **Rule 6.** A finished row's JSON and text never say admitted or accepted (SPEC line 259).
- **`FINAL:` negative.** `FINAL:` inside other text does not count (SPEC line 269).
- **Failure-mode fixtures** from SPEC section 11:
  - worktree removed mid-sweep (line 440)
  - unreadable transcript and unreadable contract (line 442)
  - list and show disagree (line 443)
  - one missing and one extra `worker-show` key (line 446)
  - F9 symlink-out (line 450)
  - a contract that changes between two reads (line 451)
  - duplicate Dispatch (line 452)
  - remote coverage (line 454)

**Exact fix:**

1. In section 7.2, add each rule with its SPEC line:
   - the `parent` cross-cutting note, plus its Retained problems entry;
   - the SP-16 literal as the coverage note when `session_join` is None;
   - the re-read rule;
   - the duplicate-Dispatch conflict rule;
   - the "show wins" merge rule;
   - the `unscanned: outside root` rule.
2. In section 11, add the fixtures to these files:
   - `test_probes_allowlist.py`:
     - the nine byte-limit boundary cases
     - worktree removed mid-sweep
     - list and show disagree
     - the missing and extra key
     - symlink-out
     - the changed contract
     - duplicate Dispatch
   - `test_classify.py`:
     - the SP-07 later-line `guard refused:` case
     - the `FINAL:` inside-text negative
     - unreadable transcript and unreadable contract
     - the WC-13 `parent` note
   - `test_report.py`:
     - the rule 6 wording check (no "admitted" or "accepted")
     - the remote-coverage Source coverage row with a lower-bound count
     - the WC-13 Retained problems line
     - the SP-16 literal
3. Name these cases in the section 12 rows for FR-010, FR-013, FR-014, FR-020, NFR-007 and the failure modes.

## Minor notes

- **m1.** Line 41 says "Callers pass only `cwd`", which conflicts with the `commands.run` signature at line 379. Say which parameters the CLI passes.
- **m2.** The `time` and `typing` imports that the design adds to the module may-import lists are not mentioned in D1. Add them there, or list them under "Not counted as deviations".
- **m3.** Step 1.0a is described as writing only its own notes file, but it also produces the captured fixtures used at step 1.8. Name both outputs.
- **m4.** The FR-020 traceability row should also name `sweep/test_report.py`, which has the header-line case at line 716.
- **m5.** Line 917 repeats the SPEC rollback phrase "its only runtime write is the report file". After the B1 fix, qualify it the same way as line 7.
- **m6.** Step 1.4 should state its pass rule inline:
  - it is the REPORT step 1.4 rule without the remote timing;
  - it runs against an existing Run and launches nothing;
  - it uses only allowlisted verbs.

  Then the task file does not depend on the default rule at line 873.
- **m7.** D3 should name the test that pins the new `Orca unavailable (<reason>); ...` literal: the FR-002 and FR-019 cases in `test_cli_contract.py`.
- **m8.** The D6 sentence has no phrase pin. Either add a phrase from it to the `"WC-14"` entry of `RULE_PHRASES` (line 653), or say why it stays unpinned. Also record at step 1.0b that the owner's approval covers the D6 sentence (SPEC section 10).
- **m9.** Line 794 calls the `summary.counts` nesting an addition. It is a structural choice made in the first v1 release, which NFR-009 allows. Say that plainly.
- **m10.** On a filesystem without hard links, every run exits 1 (line 120 and open item 14). Leaving this UNVERIFIED is acceptable, but add one line to the command's user-facing text so the error makes sense when it appears.
- **m11.** The developer guide copy at line 991 (R7) is checked only by manual review. A one-line parity assert in `test_worker_contract.py`, next to the rename at line 545, would catch drift.

## Self-audit

**Basis of the findings.** Every cited line was checked against its source in this session. Each blocking finding names both the DESIGN line and the SPEC line it conflicts with.

**Limits of the evidence.**

- B3 rests on grep finding none of the listed terms in DESIGN. The terms come from the SPEC wording, and the section 11 case lists (lines 711-718) were read in full to confirm the gaps. A requirement worded very differently could still have been missed.
- B2 assumes the ccsession hook writes a tab entry for every session in an Orca pane. That comes from `ccsession` lines 562-604: `orca_tab_session` runs whenever `ORCA_PANE_KEY` and `ORCA_TERMINAL_HANDLE` are set. Whether every person session has them set was not observed in a live session.

**Not checked:**

- the D6 and WC-14 text compared word for word with SPEC section 10;
- REPORT steps 1.14 to 1.24a, beyond their mapping;
- the inv-005 evidence, beyond its conclusion about optional locks;
- sections 2 and 4 to 6 of DESIGN, line by line.
