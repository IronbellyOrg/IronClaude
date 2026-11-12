<!-- merge input for reviewer 3: calibrated confidence C=0.71 (calibrator class haiku); self-reported value is NOT used. Weight this card by calibrated C in the debate. Calibration notes: reviewer-cards/reviewer-3-card-calibrated.yaml -->
<!-- Parent-persisted from the reflect-reviewer's returned card (agent ad5119f29b27d9bbc, opus slot claude-gw-tier1a). The reviewer has no write tool. Text below is the reviewer's own; no verdict changed. Path alias TL = .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md ; ADD = .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md -->
# Reflect reviewer 3: refactorer (UC-1 pre-execution)

**Reviewer persona**: refactorer
**Grounding root**: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
**Timestamp**: 2026-11-10
**Self-reported confidence C**: 0.75

## Findings
| ID | Severity | Class | Location (file:line) | What is wrong | Evidence (file:line, quote) | Smallest fix and verifier | Confidence |
|---|---|---|---|---|---|---|---|
| R3-F1 | MEDIUM | stale-text | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1986` (also 1292-1404, 1993-2091, 2320-2425, 2613-2746) | The same Context sentence appears in 59 revised items. It is true only when item 7.10 runs. The other 58 items run after 7.10 has rewritten line 22, so for them the sentence is false. Adversarial lenses are told to assume the work is wrong. Fixers 7.30, 7.34, 11.14, 13.18 and 14.25 may edit `pragmatic.md`. Those lenses and fixers are told that line 22 is the unqualified rule, which invites a finding against the delivered exception or a fix that reverts it. Item 11.5 contradicts itself in one line: it gives the stale anchor and also says "actual canonical style". | TL:1986 "Current source anchor for the style scope: `src/superclaude/output-styles/pragmatic.md:22` (unqualified table mandate, not an implemented exception)". The planning QA accepted the sentence as a planning-time fact: `revisions/chat-output-exception-20261109-133150/qa/qa-task-validation-consolidated.md:15` "STYLE:22 remains the current unconditional rule". | Keep the sentence at 7.10 (TL:1209). In the other 58 items, replace it in place (the line count does not change) with "Pre-7.10 source anchor: `pragmatic.md:22` held the unqualified table mandate; after item 7.10 it holds the scoped sweep exception." Verifier: `grep -c 'not an implemented exception' TL` returns 1, and that one hit is line 1209. | 0.75 |
| R3-F2 | MEDIUM | partial (refines T1 F5) | TL:1210 (7.10 Branch 2); TL:1973 (11.3); TL:1980 (11.4) | Items 7.10, 11.3 and 11.4 each restate the common rule in their own lossy wording. The addendum says the style definition is that rule itself. 7.10 leaves out several addendum clauses: (a) the table-omission request and the word "coordinator", which do not establish the role (ADD:15); (b) "loaded skill and style ... do not themselves assign" (ADD:15); (c) the same-message case (ADD:17); (d) "Formatting never authorizes advice prohibited by the sweep skill" (ADD:19); (e) the list of things the exception does not change (ADD:21). 11.3 words several of these differently. 11.4 pins one "common" rule across the style and the skill. Two paraphrases will not match it, and the only failure path at 11.4 is "stop incomplete" (T1 F2). | ADD:27 "The future style definition is the common rule above." TL:1210 names only "a request in an independently assigned coordinator does not remove or grant assignment"; it has no same-message clause and no table-request clause. TL:1973 includes "operative assignment plus a separate request in the same message qualifies only if applicable before execution". | Remove the paraphrases. In the 7.10 Branch 2 and 11.3 Actions, write ADD:13-21 word for word as the rule block, adapting only the heading level. In 11.4, add one assertion that the whitespace-normalized block is a substring of both the style file and the skill file. I checked that ADD:13-21 contains no `src/superclaude` and none of stop, retry, release, merge or removal, so the existing 11.3 greps and the 11.4 banned-word test still pass. Verifier: that one 11.4 assertion. | 0.7 |
| R3-F3 | LOW | authority (pattern inconsistency) | TL:1363 (7.30), TL:1391 (7.34) | Fixers 14.25, 14.29, 14.38 and 14.42 take sha256 sums of the addendum and the revision BUILD-REQUEST before and after they run. Fixers 7.30 and 7.34 are the only fixers allowed to edit both DESIGN (the R5 sections) and `pragmatic.md`. They protect the design append, the addendum and BUILD-REQUEST with a prose ban only. | TL:1363 "Never change revision authority/design append/decision choice"; only TL:2614, 2642, 2705 and 2733 contain `sha256sum`. | Reuse the 14.25 pattern in 7.30 and 7.34. Hash the addendum and BUILD-REQUEST before and after the run, and run `grep -c '^## Scoped normative addendum: sweep final chat-summary exception$' docs/designs/orchestrator-mode.md` (expect 1); the whole DESIGN file cannot be hashed because its R5 sections legitimately change. Write each result to the fix log as a PASS line. | 0.6 |
| R3-F4 | LOW | stale-text (existing before this revision) | TL:2761, TL:2763 (14.46) | 14.46 says to keep "the three entries already there" and checks for "three original entries". The Follow-Up section already holds four entries; the fourth was added by reflect run 2. This revision did not create the problem (baseline:2761 and 2763 are identical), but adding an install follow-up as T1 F8 recommends would make the count harder to check. | TL:2996-2999 hold four `- [` entries; TL:2763 "still holds its three original entries plus one line per new follow-up". | Change "three" to "four" at both places (in-place edit). Verifier: count the `- [` lines under `### Follow-Up Items Identified` before 14.46 runs; the count is 4. | 0.8 |

## Tier-1 findings reviewed
| T1 id | Verdict (confirmed / refined / refuted / not in my slice) | Evidence (file:line) |
|---|---|---|
| F1 | confirmed. Item 13.1 is not part of this revision, but it is in my routing-row slice. | `docs/designs/orchestrator-mode.md:716` "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside"; TL:2267 greps "The coordinator sweeps on every wake, at most once every 5 minutes\." |
| F2 | confirmed. The revision makes a failing check harder to recover from: the fix moves out of 11.4 into already-ticked items. | baseline/task.md:1982 "A failure is fixed in the primitive"; TL:1982 "fixed in its owning source item or authorized serialized fixer ... stop incomplete"; the first fixer is 11.14 (TL:2050) |
| F3 | confirmed, but outside my slice | TL:1270 writes `OQ-17-cursor-template-decision.md` and `OQ-18-...`; TL:1293 and TL:1363 expect the `OQ-*-decision.md` count to be 8 |
| F4 | confirmed in substance, but outside my slice (owner gates) | TL:1210 names no file or path for the "separate direct execution authorization"; BUILD-REQUEST.md:55 "user decides execution separately" |
| F5 | refined to R3-F2. The 7.10 gap covers more of ADD:15, 17, 19 and 21 than T1 found; the smaller fix is to copy the text word for word, not to add one clause. | TL:1210; ADD:15-21; ADD:27 |
| F6 | confirmed. Items 8.19 and 10.5 are not part of this revision, and the wording was already stale under the OQ-6 record. | TL:1551 "the layout follows the recorded GQ-35 and GQ-63 decisions"; TL:1812 "follows the OQ-4 (GQ-35) and OQ-6 (GQ-63) records" |
| F7 | confirmed | TL:1143 Branch 2 "resets the task `status` to "🟠 Doing""; the override appears only in the appended note, which says it "is not an executable checklist" |
| F8 | confirmed | `Makefile` has no `output-styles` match; `src/superclaude/cli/install_user_setup.py:140` `install_output_styles`; `src/superclaude/hooks/scripts/pragmatic-subagent.js:7` reads the HOME copy |
| F9 | confirmed (LOW) | The severity modules first run at TL:1987 (11.5); the 7.10 edit area is `pragmatic.md` lines 22-90 |
| F10 | confirmed | `src/superclaude/output-styles/pragmatic.md:25` "The required DONE / NEXT table does not count toward this limit" is an eighth mention and is not one of the seven sites |

## Slice coverage
Rows audited: 45 of 45. Adherent: 42. Gaps found: 3.
- INF-A06 is partial (R3-F2).
- INF-A15 is partial: 7.10 does not name the length budget (ADD:27).
- INF-A29 is missing but harmless: it is a future-only rollback rule and no item contradicts it.

INF-A14 (the explicit precedence statement) is covered in substance by 7.10's "ordinary label gloss", but 11.4 does not pin gloss precedence.

I checked D1-D10 only at the mapping level: the DESIGN rows exist at `docs/designs/orchestrator-mode.md:828-837` and their items are not part of this revision. I did not re-audit the bodies of items 8.x to 10.x.

## Notes
- **Preservation (T1 V1), partly checked.** I confirmed four things:
  - Both files have 137 `- [x]` and 218 `- [ ]` items.
  - Baseline ends at line 3008, and the task file adds only the note after it.
  - Item 11.4 changed from baseline in exactly the way T1 F2 describes.
  - The original start sha does not appear in either task file; it is stored in `baseline/progress.md` and `history-manifest.json`.

  I did not byte-compare lines 1-1208, because I had no diff tool.
- **Stale Open Questions entry, left as history.** TL:2980 still says "OQ-6 ... OWNER DECISION PENDING". The revision kept it unchanged on purpose. The POST runner (14.48) appends to this section, so a POST reviewer may flag it. A one-line note pointing to the RESOLVED record would be enough; this is a matter of taste.
- **Copied lens wording in verifier items.** Items 7.31, 7.32, 7.35 and 7.36 contain the lens sentence "apply this lens to actual (b) ...", but they are verifiers. This is copy-paste and does no harm.
- **House patterns are reused correctly.** `tests/commands/test_graph_command.py:16-18` (`_REPO`, `_COMMAND`, `_SKILL`) and the `sc-graph-protocol/SKILL.md:1-11` frontmatter exist as cited. Putting style assertions in `tests/commands/` rather than `tests/skills/`, where `test_review_severity_rule.py:26` already reads STYLE, is what ADD:31 requires ("No separate test file").
- **No other copy of the rule needs editing.** `src/superclaude/output-styles/pragmatic.md` is the only source of the DONE / NEXT rule under `src/` and `plugins/`. The SPEC (`merged-requirements.md`) never mentions DONE, pragmatic or GQ-63, so the exception needs no SPEC deviation row.
- **The POST diff will include the style edit.** 14.47 (TL:2768-2770) diffs tracked files against BASE and checks for the `pragmatic.md` hunks and the design append.
- **Not checked.** I did not re-read 13.9-13.24 or the Phase 14 lens bodies beyond 13.12, 13.18, 14.1, 14.25, 14.46, 14.47 and 14.48.
