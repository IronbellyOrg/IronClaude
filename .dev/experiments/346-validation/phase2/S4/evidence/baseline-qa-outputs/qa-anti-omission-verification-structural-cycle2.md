# QA Report - Gate 5 Anti-Omission Verification (Structural), Fix Cycle 2

**Status:** Complete
**Date:** 2026-11-08

---

Scope: consolidated findings cycle 2 (BLOCKING_COUNT 3, rows 1 to 3), fix log cycle 2 (first line is not SKIPPED; 3 fixes, 0 not fixed), report `RESEARCH-REPORT-bmad-first-use.md`. This cycle has no RECOVER or JUSTIFIED omission rows; its 3 rows are fixes of findings from the cycle-1 verification. Check (a)/(b) therefore apply to the fixed rows and to the 4 cycle-1 recoveries; check (c) applies to the whole report.

## Check 1 - Row 1: step 5.3 case (d) (report l.1542)

PASS. Read l.1542 in full. It now says "(c), (e) and the `bmad-x` fixture of (d) leave P byte-identical", and that the `bmad-os-x` fixture is a first use (a `bmad-os-*` entry alone does not block it, step 3.2 condition 3), the install runs, the same creation as (a) is asserted with the user's `bmad-os-x` entry preserved, "not byte-identical", and that under the stricter glob (Section 9 row 20) P stays byte-identical. Read l.1465 (step 3.2 condition 3: counts `bmad-*` other than `bmad-os-*`): agrees. Read l.298-300 and l.1718 (Section 9 row 20 (b) names the "fixture assertion in step 5.3 case (d)"): agree. Grep `byte-identical`: hits at l.337, 613, 1513, 1542 (x4), 1556, 1559, 1572; l.1556, 1559, 1572 concern other cases (f, seed guards, deselection), none states (d)'s os fixture is byte-identical. The self-contradiction of the finding is gone.

## Check 2 - Row 2: `--output-folder` "every command" wording (l.406, 681, 910)

PASS. Read l.406, 681, 910 in full: each now qualifies the rule to commands that pass `--user-name` and says the flagless `--yes` alternative passes none of the four core flags and needs no `--output-folder` (step 3.1, Section 9 row 20). Grep `every (first-use )?command|every first-use|--output-folder` over the report: the "every ... command" wording occurs at l.121, 406, 568, 681, 910, 1438, all qualified (l.121, 568, 1438 read). l.68, 192, 480, 509, 565, 1056 only quote the manual command or the diagram. l.1021 says "whenever `--user-name` is passed". l.549, 708, 767, 1689 are about "without `--output-folder`" outcomes (R-9), not a rule. No unqualified wording remains.

## Check 3 - Row 3: W01-18 (l.867) and step 4D.4 (l.1526)

PASS. Read l.864-867, l.1526, and web-01 l.120-164 (the source). The l.867 text now states only what web-01 states: the web-01:127 quote is about `-p` runs (matches web-01:127), web-01:155 says `-p` already trusts the folder (matches), so the quote shows only that skill-frontmatter hooks run in untrusted `-p` folders; it says it is UNVERIFIED - doc-only and UNVERIFIED for a user-level stub; the further step is labelled `[synthesis inference: ...]` and UNVERIFIED - doc-only. l.1526 carries the same content, labelled the same way, and no longer asserts that no hook option escapes the hold-back for frontmatter hooks. The sentence "a stub (4B) is not gated by hook trust" matches web-01 recommendation 2 (web-01:224) and web-01:157. Other mentions (l.975, 1141, 1249, 1354, 1491, 1713) talk about settings-file hooks and the interactive hold-back and do not contradict l.867 and l.1526.

## Check 4 - The 4 cycle-1 recoveries are still intact (by meaning)

PASS, all four.

| Recovery | Where it lives now | Evidence |
|---|---|---|
| O-5 flagless `--yes` alternative | l.121, step 3.1 (l.1464), Section 9 row 20(a) (l.1718), l.292 | Read each: seeds all five core keys via `ui.js:838-861`, any ONE of four flags selects the partial-seed branch `ui.js:807`, cost (OS username, divergence from `install.sh:42`), plan default unchanged, UNVERIFIED - never run |
| O-8a `bmad-os-*` and re-install rules | l.292, l.294, l.298-299, step 3.2 (l.1465), Section 9 row 20(b) (l.1718) | Read each: cleanup preserves `bmad-os-*` (`_config-driven.js:789-790`), `isBmadOwnedEntry` false (`installed-skills.js:45`), pre-copy removal of `<canonicalId>` (`_config-driven.js:445-448`), `_cleanupSkillDirs` (`installer.js:97-101, 406-425`) |
| OM-1 managed-settings source ranking and `first-wins` | step 4D.6 (l.1528), Section 6 Option D row (l.1141), Section 9 row 15 (l.1713) | Read each: ranking remote, MDM/OS, managed files; default `first-wins`; `managedSourcesBehavior: "merge"`; drop-in ignored when a higher source delivers any policy key; `[UNVERIFIED - doc-only]`; matches web-01:143 (read) |
| OM-2 skill-frontmatter hooks in untrusted `-p` folders | l.867 (W01-18) and step 4D.4 (l.1526) | Read: still present, now corrected by cycle 2 row 3 (Check 3) |

## Check 5 - No new blocking issue from the cycle-2 edits (structure)

PASS.

- Table of Contents (l.10-55): read in full; all Section 1 to 10 and subsection headings match the heading list from Grep `^#{1,4} ` (l.59-1795). No heading was added or removed.
- Tables: the edited table rows (l.406, 681, 1464, 1465, 1526, 1528, 1542, 1718) have the same unescaped pipe count as their neighbours (4-column rows 5 pipes, the l.681 row 6 pipes for its 5 columns). Line count 1804, matching the consolidated findings.
- Duplicated content: the l.867 and l.1526 corrections each occur once; no repeated paragraph found in the edited areas.
- Placeholders: Grep `TODO|TBD|FIXME|PLACEHOLDER|lorem|<fill|???` hits only l.612 and l.653, where "placeholder" is a legitimate noun ("placeholder trees", a quoted term), not an unfinished stub.
- Contradictions between sections: step 5.3 (l.1542) vs step 3.2 (l.1465) vs l.300 vs Section 9 row 20 (l.1718): consistent. `--output-folder` rule: l.121, 406, 568, 681, 910, 1021, 1438 consistent. Hold-back wording: l.864, 867, 1526, 1713 consistent.
- Owner questions Q1 and Q2 remain unanswered in the report (Section 9 rows 1, 2 untouched per fix log); no owner decision invented.

## Check 6 - JUSTIFIED rows

N/A in this cycle: the consolidated findings of cycle 2 contain no RECOVER or JUSTIFIED omission rows; the 4 cycle-1 JUSTIFIED rows were confirmed valid by both cycle-1 verification reports per the cycle-2 consolidated findings (I did not re-derive them: UNVERIFIED by me this cycle, not in scope of the 3 rows).

## Notes (MINOR, not blocking)

- N-1 (MINOR): step 5.3 (l.1542) tells the `bmad-os-x` fixture to assert "the same creation as in (a) ... the `bmad-*` skill count", but the (a) assertion compares the number of `P/.claude/skills/bmad-*` directories with the installer's `<N>`; the user's own `bmad-os-x` directory also matches that glob, so an implementer must exclude `bmad-os-*` from the count for that fixture. The text is loose, not contradictory; not rechecked per the MINOR rule.

## Self-Audit

What I actively checked (tool calls, each tied to a claim):

- Read the embedded prompt (task file l.467), the cycle-2 consolidated findings (25 lines) and fix log (34 lines) in full.
- Read report l.119-121, 292-300, 404-406, 679-681, 862-867, 908-910, 1021, 1141, 1249, 1354, 1455-1579 (Phases 3, 4, 5 including steps 3.1 to 3.6, 4B to 4D, 5.1 to 5.6 and Table 5.1), 1713 and 1716-1718, and the Table of Contents (l.1-58).
- Read the source web-01 l.120-164 (sections 3.1 to 4.2) and l.221-230 (recommendations) to reproduce the `-p` quote (l.127), the `-p` trust statement (l.155), the interactive hold-back (l.154, 156), the skills-not-gated line (l.157) and the source ranking (l.143).
- Grep runs on the report: `every (first-use )?command|every first-use|--output-folder`; `hold-back|held back|untrusted|trusted`; `byte-identical`; `bmad-os`; `O-5|O-8a|OM-1|OM-2`; `case (d)|bmad-x`; `--user-name`; heading list; placeholder words; `row 20`. One Bash read-only pipe count of table pipes on 8 edited rows plus `wc -l`.
- Tool engagement: Read 22, Grep 12, Glob 0, Bash 1 (all mapped to the checks above).

Why I believe 0 blocking findings is correct: each of the 3 cycle-2 rows was reproduced at its report line from the text itself, not from the fix log, and I searched the whole report for the same wording elsewhere (Row 2: the six "every command" sites are all qualified; Row 1: every "byte-identical" hit was classified; Row 3: all hold-back mentions were compared with web-01). I looked for a new defect created by the fixes (test assertion mismatch, ToC, table width, duplicates, placeholders, cross-section contradiction) and found one loose wording (N-1, MINOR). Limits: I did not run any test or command from the report (nothing was executed; the report's own UNVERIFIED labels stand), and I relied on the cycle-1 reports for the 4 JUSTIFIED rows.

## Verdict

**VERDICT: PASS**

Counts: unrecovered 0; wrongly justified 0; newly introduced blocking 0; Critical 0; Important 0; Minor 1 (N-1, note only). Cycle-1 recoveries intact: 4 of 4. Cycle-2 fixes verified: 3 of 3.

Confidence: Verified: 5/6 | Unverifiable: 1 (Check 6, N/A this cycle) | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 22 | Grep: 12 | Glob: 0 | Bash: 1

## QA Complete
