# Variant 2 (refactorer): ponytail fix audit for the spec-panel Review Loop

Persona: refactorer. Angle: technical debt, simplification, minimal-risk transformation. Design only, nothing implemented. Issue 346, theme "ponytail".

## 1. Position in one page
**What I recommend building.** The owner's idea, placed after fix cycle 2 and before review 3, run once, with three simplifications that remove risk instead of adding machinery:
1. **A script does everything that can be done without judgment.** `fix_audit.py` (stdlib only) splits the fix into numbered hunks, maps each hunk to the finding ids it cites, reads each id's severity from the prior report itself, and flips the default: a hunk that cites only minor findings, or no finding, is a revert candidate. The ponytail reviewer only has to answer the two questions a script cannot: is the claimed severity real, and is there a smaller fix.
2. **The auditor never edits. The script edits, all-or-nothing.** It reuses the old/new row pattern of `apply_rows.py` (every `old` must occur exactly once, else `STOP, nothing written`). If anything fails, the loop falls back to plain 427 behaviour. The mechanism can waste time; it cannot corrupt the spec.
3. **The audit runs before review 3, inside the review 3 run of a new variant command.** Review 3 then reviews the text that will ship, and review 3's own prior-blocking table is the safety net for any bad shrink. The 3-review cap is untouched; no fourth review exists.

**What it costs the brief.** One line of the review-3 dispatch brief changes: `/sc:spec-panel` becomes `/sc:spec-panel-ponytail` and ` --apply-audit` is appended. Review 1, review 2 and both reviser briefs are unchanged, so those steps stay byte-comparable to the Arm B runs.

**What I predict (derived in section 9).** Review-3 open critical+major mean about 2.4 on the Arm B base (range 1.5 to 3.2), growth about 26% (bar 44.4%, already met by 427 alone). The mean bar (3 or fewer) is likely met; the stricter "both replicates better than both controls" is likely not met, because replicate r1 starts at 6 and no placement brings 6 down to 3. The honest summary: this trims noise (minor-fix text and its derived defects) and shrinks the changed-line set; it does not touch defects born from necessary fixes of blocking findings (flg-r2's N12 came from the N5 fix). Do not expect a clean PASS from it.

**Why this placement and not the others.** The two alternatives (audit after every cycle, triage before the first fix) are predicted to do about as well or slightly better on review-3 count (2.0 and 1.9, against 2.4) at higher cost or with no necessity test. Because the script is generic over (baseline, current, report), the "after every cycle" placement is the same script called a second time after cycle 1: a pre-registered follow-up, not a redesign. Build the cheap thing first, measure, then extend.

**What I deliberately did not add.** No new flag except the consent flag. No fourth review. No retry loop for a malformed audit table. No new report format beyond three machine lines. No change to bullets 1-7 of the 427 text. No edit to `/sc:spec-panel`, the plugin mirror, `HOW-WE-WORK.md` or `/sc:implement`.

## 2. Evidence the design rests on
Each row was read on disk this session unless marked UNVERIFIED.

| # | Fact | Source |
|---|---|---|
| E1 | The 427 Review Loop is seven one-line bullets; bullet 6 already forces "each added paragraph or table cites its finding id", bullet 2 gives the blocking rule, bullet 4 the 3-review cap. | `src/superclaude/commands/spec-panel.md:256-264` |
| E2 | In the real flg-r2 loop every spec edit carries its finding id inline, and the cycle-2 table had 15 rows, all applied, 9 of them minor (N7-N11, C9, C12, C13, C14); N1-N6 were blocking. | `exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition-round2.md:12-34` |
| E3 | The coordinator's brief told the reviser to "apply confirmed findings". So the minor fixes were applied because the brief asked, not only because 427 failed to forbid them. A rule in the report cannot beat an instruction in the brief; a check after the fact can. | `disposition-round2.md:12` |
| E4 | Review 3 of flg-r2 found 1 blocking (N12) and 4 minor notes. N12 came from the N5 fix (N5 was a blocking row). N14 came from the N9 fix and the citation note C-R3-15 from the N11 fix (both minor rows). N13 touches AC-1.2, edited by both a blocking row (N3) and a minor row (N7). N15 is `origin=unchanged`. | `spec-panel-round3.md:13-17, 35, 39, 41, 91-103` |
| E5 | Growth: cycle 1 added about 19 points and cycle 2 about 11 points in the 427 arms (flg-r2 21.6 then 32.1; flg-r1 17.5 then 27.8; trt-r1 11.6 then 23.1; trt-r2 23.3 then 36.3). flg-r2 cycle 2 added 6,073 bytes (70,255 to 76,328; base 57,763). Cycle 2 is about 37% of growth. | `AB-REPORT.md:14-15`, `ARMB-REPORT.md:13-16`, `spec-panel-round3.md:25` |
| E6 | 427 already meets the growth bar (23.1% to 36.3% against 44.4%); it misses the review-3 bar (proxy 5.5 for 427, 3.5 for 427+flags; bar 3). The problem to solve is review-3 count, not growth. | `AB-REPORT.md:19-25`, `ARMB-REPORT.md:20-24` |
| E7 | 89% of review 2 and 100% of review 3 new findings sit on changed lines. Fewer changed lines at review 3 means fewer new findings. | `AB-REPORT.md:30` |
| E8 | `ponytail-review` lists findings in prose groups (Must fix, Should fix, Nice to have), each with four parts; ends with `Verdict:`, `Lean: -N lines possible.`, `Not checked:`; "Lists findings, changes no code"; no table, no severity column. | `~/.claude/plugins/cache/ironclaude/ponytail/5.3.3/skills/ponytail-review/SKILL.md:69-101` |
| E9 | `/sc:implement` QA forbids a ponytail judgment from changing a severity or verdict and says the protocol never invokes the plugin. | `src/superclaude/skills/sc-implement-protocol/refs/qa.md:91` |
| E10 | Prior art for a safe text apply: rows with `old`/`new`/`occurrences`; a row whose `old` does not occur the expected number of times prints `STOP, nothing written` and exits 1; an applied row is reported `already`. | `.dev/review-severity-rule/implement-tools/apply_rows.py:1-40` (uses PyYAML; I use JSON so `uv run --no-project python` needs no dependency) |
| E11 | Skills ship scripts in `scripts/` (`sc-implement-protocol/scripts/archive_workspace.py`); commands have none. Workers load the user-level command, so a variant needs its own name (`AB-REPORT.md:46-47`). The 427 static test pins only the two original copies (`test_spec_panel_review_loop.py:15-19`), so a new file cannot break it. | `ls` of that folder; the two files named |

**The key refactoring observation.** E1 + E2 + E3: the data needed to decide "minor-only hunk" is already in the files (ids cited in the text, severity in the prior report). A script can nominate every minor-only hunk with no model call. The ponytail reviewer is then a veto and shrink layer on top of a deterministic base, not the whole mechanism. That shrinks the unreliable part.

## 3. Primary mechanism (owner's idea): placement, scope, flow
### 3.1 Where exactly: after fix cycle 2, before review 3, inside the review 3 run
Timeline of the loop: review 1, fix cycle 1, review 2, fix cycle 2, **[audit]**, review 3, escalate or stop. The audit runs as the first step of the `--re-review` run that would otherwise be review 3, and review 3 then reviews the audited text.

Why before review 3 and not after it:
- Text that ships must be text a reviewer saw. An audit after review 3 reverts or shrinks lines no panel ever read, and the final verdict then describes a different document.
- Review 3 is the existing safety net. A shrink that damages a blocking fix shows up as `open` in review 3's own prior-blocking table. After review 3 there is no net.
- E7: 89% to 100% of new findings sit on changed lines. Removing minor-fix hunks before review 3 removes the lines it would have attacked; after review 3 the same removal only hides findings already written. What I give up is review 3's findings as evidence (N5's fix bred N12): the rejected variant "P-post" in section 9.4.

"Never re-reviewed" is kept in the sense that matters: nothing reviews the audit table itself and the audit runs once per loop. Review 3 is the existing third review of the document.

### 3.2 Scope: the fixes of cycle 2 only
The audited unit is every hunk between `--baseline` (the copy saved before cycle 2, which the 427 loop already requires) and the current document. It needs no new saved copy or flag; Arm B briefs already pass both files at review 3. Cycle-1 fixes were re-reviewed by review 2, and reverting them would touch vetted lines and break the diff review 3 is built on. The cost is real: cycle 2 is only about 37% of growth (E5). Passing the original copy as `--baseline` widens the scope to both cycles with no code change.

### 3.3 The nine steps inside the review 3 run
Trigger (all must hold, else the variant behaves exactly like `/sc:spec-panel`): `--re-review` and `--baseline` given; the prior report header is `review: 2 of 3` and its last line is `verdict: FAIL`; the diff against the baseline, ignoring whitespace-only changes, is not empty. Steps 1 to 4 then run as a dry audit. Step 5 (the only edit) additionally needs `--apply-audit`, the consent token (section 3.4).

1. **Prepare.** `uv run --no-project python <skill>/scripts/fix_audit.py prepare --baseline B --current S --report R2 --out D` where `D` is `<dir of R2>/fix-audit/`. It records sha256 of `S`, saves `D/current-before-audit.md`, writes `D/fix-list.md` (hunks, cited ids, severity read from `R2`, bytes) and `D/state.json`.
2. **Audit.** The review session starts one fresh subagent (Agent tool) with the brief of section 4. The subagent returns the table as text. The session writes it to `D/fix-audit.md`. One pass. No retry.
3. **Check.** `fix_audit.py check --dir D`. It validates shape and rules (section 10) and that `S` still has the recorded hash (the auditor did not edit). On failure: write the reasons to `D/apply-log.md`, apply nothing, go to step 7 with `audit: skipped(check failed)`.
4. **Plan.** `fix_audit.py plan --dir D` writes `D/apply-rows.json`: one row per reverted hunk (old = current text with the minimum unique context, new = baseline text) and one per shrink row.
5. **Apply.** `fix_audit.py apply --dir D`. All-or-nothing. Writes `D/apply-log.md` and `D/closed-minor.txt`. On `STOP`: nothing written, `audit: skipped(apply stopped)`.
6. **Record.** The session notes `audit: applied(reverted=<n>, shrunk=<n>, kept=<n>)` and `audit-closed-minor: <ids>` in the review 3 report (two machine lines, section 8).
7. **Review 3 proper.** Unchanged 427 behaviour on the (possibly audited) text: prior-blocking table of `resolved|open|regressed`, findings on changed lines against the same baseline, `origin=` tags. One difference: the prior-blocking table leaves out ids listed in `closed-minor.txt` (they are minor and closed, not open, section 8).
8. **Verdict file.** The session adds `open-blocking: <ids or none>` above the final `verdict:` line, then runs `fix_audit.py verdict --dir D --report R3` which writes `D/final-verdict.md` (section 8).
9. **Stop.** Review 3 is the cap. FAIL escalates to the user with the open blocking findings exactly as bullet 4 says. The audit table is not read again by anyone but the user.

Every step before 7 fails open to plain 427 behaviour. The failure modes are therefore "no benefit" and "wasted minutes", not "corrupt spec".

### 3.4 Consent (C6)
`/sc:spec-panel` never modifies a specification without consent. The variant never edits on its own: the edit happens only when the brief passes `--apply-audit`, the edit is made by a script, it is limited to hunks the diff against the baseline already shows, and a full copy of the pre-audit text is saved in `D`. Without the flag the variant writes `fix-audit.md` and `apply-rows.json` and stops before step 5 (`audit: skipped(no consent flag)`); a coordinator may then run `apply` itself. UNVERIFIED: whether the owner accepts "flag in the brief" as consent (section 16, Q1).

## 4. The brief handed to the ponytail reviewer
The text lives in one file, `~/.claude/skills/sc-fix-audit/refs/auditor-brief.md`, which the command tells the review session to read and pass verbatim (placeholders `<D>`, `<S>`, `<B>`, `<R>` are filled by the session). One source means one place to test and one place to change. Verbatim text:

````text
You are the fix auditor. You run once. You never edit any file: your whole answer is the
audit table described below, returned as your final message.

STEP 0. Load the skill ponytail:ponytail-review with the Skill tool and use its lenses
(correct, lean: "is every line needed, is there a smaller change or a deletion"). If the
skill cannot be loaded, write "auditor: inline-rubric" as your first line and use only this
brief. Otherwise write "auditor: ponytail-review". Ignore the skill's own output format,
its "Verdict:" line and its "Lean:" line. Do not write them.

WHAT YOU AUDIT. A document was reviewed (report <R>), then a reviser changed it. The changed
text is split into numbered hunks in <D>/fix-list.md. Each hunk is one fix. You do not
review the document again and you do not report new problems.

READ, in this order:
1. <R>   the findings report with each finding id and its severity.
2. <D>/fix-list.md   hunk ids, line ranges, finding ids cited, severity read from <R>, bytes.
3. <B>   the saved copy before the fixes.   4. <S>   the current document.
5. Dispositions or reviser notes if the brief names a file; otherwise none.
For each hunk, compare the lines of <B> and <S> it covers and read the sections of <S> that
the hunk refers to (the document's connected text), not only the hunk.

ANSWER TWO QUESTIONS PER FINDING ID.
Q1 Severity. Validated severity is "blocking" only if you can write ONE sentence of the form
   "An implementer or tester who follows the text WITHOUT this fix will <concrete wrong
   result>". Blocking means: wrong behaviour, a false claim that leads to a wrong result, a
   missing deliverable the document itself requires, a security or data-loss risk. All else is
   "minor": a wrong line number or citation whose claim is still true, wording, an extra check
   for a rule the document already states, a gap nobody would trip over. You may lower a
   claimed severity, or raise one only with the sentence.
Q2 Necessity. Is the added or changed text needed to fix the finding? Try, in order: delete
   it; merge it into a sentence that already exists; reuse a rule the document already has;
   a shorter wording. "Necessary" means none of these fully solves the finding.

VERDICT PER FINDING (default is deletion):
- validated minor            -> revert, unless Q2 shows the text is needed (then keep).
- validated blocking, necessary, no smaller text -> keep.
- validated blocking, a smaller text fully solves it -> shrink (give the exact old and new
  text, the new text shorter and still citing the same finding id).
You may not revert a hunk whose finding the report grades CRITICAL, FR-8 or FR-9; the checker
will refuse it. A hunk citing no finding id is unattributed: revert it unless you can write
the Q1 sentence for a real finding it fixes.

OUTPUT, exactly this, nothing else:
auditor: <ponytail-review|inline-rubric>
inputs: <S> sha256=<value from <D>/state.json>

| finding | hunks | claimed | validated | necessary | smaller alternative | verdict | evidence |
|---|---|---|---|---|---|---|---|
| N7 | H4,H5 | MINOR | minor | no | delete both sentences | revert | no wrong result: the duty is already in WC-4 |
...one row per finding id in fix-list.md, plus one row with finding "-" per unattributed hunk...

Cells: finding = id as written in <R> or "-". hunks = comma list of hunk ids. claimed =
CRITICAL|MAJOR|MINOR|FR-8|FR-9|- as printed in <R>. validated = blocking|minor. necessary =
yes|no. smaller alternative = one short sentence or "none". verdict = keep|shrink|revert.
evidence = for blocking, your Q1 sentence; for minor, why no wrong result follows.
Every hunk id in fix-list.md must appear in at least one row. No pipes inside cells.

If and only if you wrote shrink rows, add after the table one fenced json block:
```json
{"shrink": [{"finding": "N5", "hunk": "H7", "old": "<exact text>", "new": "<shorter text>"}]}
```
"old" must be copied exactly from <S> and occur once in it.

Style: no opinions, no new findings, no advice about the process. If a hunk is too tangled to
judge in one pass, give it verdict keep and evidence "not judged: <why>".
````

Notes on the text, as a refactorer:
- The default flip ("default is deletion") is the ponytail stance and lifts the revert rate (`r`, section 9) from about 0.5 under a literal reading of the owner's rubric to about 0.8. The risk is a demoted real blocking finding; section 10 lists the guards (K6, K8).
- The Q1 sentence reuses 427 bullet 2's own MAJOR test, not a new scale. "False claim" alone is not enough: a citation off by one line is false, yet no implementer produces a wrong result from it. Under the owner's literal "false claim" the audit would validate most of the 9 minor flg-r2 rows (C9, C12, C13, C14 are citation and wording fixes) as blocking and revert almost nothing.
- A reverted citation fix leaves a known-wrong citation. That is accepted debt, recorded as `closed-minor`, and is what bullet 2 says minor findings are: notes.

## 5. Invoking ponytail-review: who, where, what if absent, how the output is adapted
**Can it be called as a skill from the loop?** Yes in principle. `ponytail:ponytail-review` appears in this session's skill list as an invocable skill, and it is installed on this host at `~/.claude/plugins/cache/ironclaude/ponytail/5.3.3/skills/ponytail-review/SKILL.md` (the installer pins it, `docs/getting-started/installation.md:363-366`). A command file cannot call a skill by itself; the review session reads the command text and then calls the Skill tool, the same way `Skill sc:spec-panel` is already called in dispatched workers (the round 3 report observed that call working in a dispatched worker, `spec-panel-round3.md:80`).

**Who invokes it and in which session.** The review 3 session spawns one fresh subagent (Agent tool, type `general-purpose`, which has the Skill tool) with the brief. The subagent's first action is `Skill ponytail:ponytail-review`. I chose a fresh subagent over loading the skill in the review session for one reason: the session that audits and then reviews would anchor on its own audit. The cost is one extra subagent session. UNVERIFIED: that a subagent can load a plugin skill in a dispatched Orca worker. If it cannot, the brief's Step 0 makes it fall back to the inline rubric, and the header line `auditor: inline-rubric` records it.

**If the plugin is absent.** The brief carries the full severity and necessity rubric, so the skill is a lens, not a dependency. Absent plugin means `auditor: inline-rubric`; the mechanism still runs. For the experiment this matters: an `inline-rubric` run does not test the ponytail idea, so the S1 plan voids any run whose `fix-audit.md` header is not `auditor: ponytail-review` (section 14). On a host without the plugin the installer's default is to install it (`installation.md:355`); a user who disabled it gets the inline rubric.

**Default output versus what the loop needs.**

| ponytail-review default | What the brief does with it |
|---|---|
| `What this change does:` paragraph | dropped; not needed |
| findings in groups Must fix / Should fix / Nice to have, four parts each, numbered | replaced by one table row per finding id; the four-part prose is cut to the `evidence` cell |
| "Reads the connected code, not only the diff" | kept: the brief tells the auditor to read the sections of the current document that each hunk refers to |
| lean lens: delete, reuse, merge, "is every line needed" | kept as Q2 and as the order of tries (delete, merge, reuse, shorter) |
| `Verdict: Ship.` / `fix 1 and 3 first.` | forbidden. A ship verdict for code has no meaning for a document fix, and the loop's verdict comes from section 8. This also keeps the spirit of `qa.md:91`: the ponytail judgment does not directly set a verdict |
| `Lean: -N lines possible.` | forbidden in the output; the script computes bytes and lines removed itself |
| `Not checked:` | allowed only as an `evidence` cell text `not judged: <why>` on a keep row |

What stays valuable from the skill is its discipline ("no case, no finding", "prefer fixes that delete code"), which is the same discipline as Q1's wrong-result sentence. What I add on top is only the table and the machine shape.

## 6. Files the loop writes and reads, and their machine shapes
All files sit in one folder, `D = <dir of the prior-findings file>/fix-audit/`, so a loop's audit evidence is in one place next to its reports.

| File | Written by | Read by | Shape |
|---|---|---|---|
| `D/state.json` | `prepare` | `check`, `plan`, `apply`, `verdict` | JSON: paths of `S`, `B`, `R`; sha256 of `S` before audit; list of finding ids found in `R`; per id the severity token and a `blocking` flag read from the id's line in `R` |
| `D/current-before-audit.md` | `prepare` | user, `apply` (rollback) | byte copy of the document before the audit |
| `D/fix-list.md` | `prepare` | auditor, `check` | header lines then one pipe table: `hunk | lines in current | lines in baseline | bytes added | bytes removed | ids cited | claimed (from report) | class` where `class` is `minor-only`, `blocking-involved`, `unattributed` or `foreign-id` |
| `D/fix-audit.md` | review session (writes the auditor's returned text) | `check`, `plan` | the table and optional JSON block of section 4 |
| `D/check.log` | `check` | review session, user | one line per rule: `OK <rule>` or `FAIL <rule>: <reason>`; last line `CHECK_OK` or `CHECK_FAIL n` |
| `D/apply-rows.json` | `plan` | `apply`, user | JSON list of rows `{id, hunk, kind: revert|shrink, old, new}` |
| `D/apply-log.md` | `apply` (and `check` on failure) | `verdict`, user | one line per row `applied|already|SKIP|STOP`, then `APPLY_OK reverted=n shrunk=n skipped=n` or `APPLY_STOP: nothing written` |
| `D/closed-minor.txt` | `apply` | review session, `verdict` | one finding id per line; empty if nothing applied |
| `D/final-verdict.md` | `verdict` | coordinator, user | open ids, the audit state, a consistency line, last line `verdict: PASS` or `verdict: FAIL` |

Three machine lines are added to the review 3 report only (no other report changes), each on its own line directly above the `Reviser brief` slot, which review 3 omits anyway (bullet 6):

```text
audit: applied(reverted=3, shrunk=1, kept=5)   | audit: skipped(<reason>)
audit-closed-minor: N7, N9, C12                | audit-closed-minor: none
open-blocking: N12                             | open-blocking: none
```

**Table cell rules** (`check` enforces them, section 10): `hunks` and `finding` ids must exist in `fix-list.md` and `R`; `validated` is `blocking` or `minor`; `necessary` is `yes` or `no`; `verdict` is `keep`, `shrink` or `revert`; `revert` needs `validated=minor` and `necessary=no`; `shrink` needs a JSON shrink entry for the same finding and hunk; `keep` with `validated=blocking` needs an `evidence` cell of at least 20 characters.

**Hunk building rules** (`prepare`): compare line by line after collapsing runs of whitespace (so whitespace-only edits are not hunks, as bullet 5 says); use Python `difflib.SequenceMatcher` opcodes `replace`, `insert`, `delete`; keep exact original text for apply. A finding id is an id that `R` itself defines: the first token at the start of a line, a table row or a bold span (for example `N12`, `C9`, `F16`, `C-R3-15`); regex for the id set is built from `R`, not hard-coded. A hunk cites an id when the id occurs in the hunk text as a whole word. `class`:
- `minor-only`: cites at least one id and every cited id is minor in `R` (a revert candidate).
- `blocking-involved`: cites any id that is CRITICAL, FR-8, FR-9, or MAJOR-and-blocking in `R`, or an id whose line the script could not parse (fail safe: treated as blocking). Never reverted whole; may be shrunk.
- `unattributed`: cites no id-like token at all (a revert candidate; bullet 6 says every added paragraph cites its id).
- `foreign-id`: cites an id-like token that is not in `R` (for example a cycle-1 id). Treated as keep; the auditor may still shrink.

## 7. The safe apply step
**Who reverts.** Only `fix_audit.py apply`. The auditor subagent returns text and edits nothing; `check` proves it by comparing the sha256 of the document before and after the audit (an edit by the auditor fails the check and the whole audit is skipped). The review session runs the script but writes no spec text itself.

**How a revert is expressed.** A revert row is an exact old/new pair derived from the diff, never typed by a model:
- `old` = the hunk's lines in the current document, plus the smallest number of unchanged neighbouring lines (0 to 3, previous lines first) that makes `old` occur exactly once in the current document.
- `new` = the same lines as they stand in the baseline (the hunk's baseline lines, same neighbours).
- An insert hunk reverts to nothing but its neighbours; a delete hunk restores the baseline lines.
- If no context length up to 3 makes `old` unique, that row is `SKIP` (not unique) and its finding is not closed. The fix simply stays.

A shrink row comes from the auditor's JSON block (`old` copied from the current text, `new` shorter). `check` additionally requires: `old` occurs exactly once in the current document; `len(new) < len(old)`; every finding id that occurs in `old` also occurs in `new`; `new` contains no id-like token that is absent from `old`.

**Apply order and atomicity** (the `apply_rows.py` pattern, E10):
1. Load the current document. Count occurrences of each `old`. A row passes when `count == 1`. A row whose `old` is absent and `new` present is reported `already` (re-running `apply` is harmless).
2. Verify rows do not overlap (their `old` spans are disjoint in the current text) and no `new` contains another row's `old`.
3. If any row fails steps 1 or 2 for a reason other than a plain `SKIP (not unique)`, print `STOP, nothing written` and exit 1. A plain `SKIP` drops that row only and the rest apply (a skipped revert is a safe no-op).
4. Build the new text in memory, write it to `S.tmp` in the same folder, `os.replace` it onto `S`. A crash cannot leave a half-written spec.
5. Re-read `S`, confirm every applied row's `new` is present and every `old` absent, then write `apply-log.md` and `closed-minor.txt`.

**Check and log.** `apply-log.md` has one line per row and a final `APPLY_OK` or `APPLY_STOP` line. `current-before-audit.md` plus `apply-rows.json` let a human undo everything with `cp`. `check.log` records which rule rejected an audit.

**How a revert avoids reopening the finding.** Two guards, one mechanical and one by text rule.

- Mechanical: `apply` writes a finding id to `closed-minor.txt` only if (a) every hunk that cites it was reverted (none skipped, none shrunk), (b) the script's own parse of `R` marks the id minor, and (c) the table says `validated=minor`. An id that is blocking in `R` can never be closed here, because a `blocking-involved` hunk is never reverted whole (section 6). So the audit can close only findings the panel already graded minor.
- Text rule in the variant (bullet 8): the review 3 prior-blocking table lists only the blocking ids of the prior report; closed-minor ids are minor, so they were never in that table. Bullet 7 of the 427 text already says a brief may not grade a minor finding as blocking, so review 3 may not reopen a closed minor finding as blocking either. A reverted minor fix that review 3 notices is at most an `origin=changed` minor note.

**What happens when an apply row fails.** `STOP` leaves the document as it was before the audit, `audit: skipped(apply stopped)` goes in the report, `closed-minor.txt` is empty, and review 3 is plain 427 review 3 on the unaudited text. No retry, no repair attempt. A `SKIP` of a single row leaves that fix in place and that finding unclosed; the report counts it in `kept`.

**A shrink that breaks its fix.** Not prevented by the script (it cannot know). It is caught by review 3: the shrunk hunk is a changed line, so the finding it answered shows `open` or `regressed` in the prior-blocking table, and the final verdict is FAIL as it would have been without the audit. The cost of a bad shrink is a FAIL that plain 427 might not have had; section 15 lists it.

## 8. Verdict effect and exact verdict computation
**Difference from the owner's wording, stated plainly.** The owner wrote that the audit "decides the final verdict". In this variant the audit decides what is *in* the verdict's input: which fix text exists and which minor findings are closed. A script then computes PASS or FAIL from files. The audit cannot turn a FAIL into a PASS by declaration, only by having removed text or closed minor findings before review 3. Reason: one unreviewed judge holding the final verdict is the pattern `qa.md:91` rejects, and a verdict set after the last review is a verdict about text nobody read.

**What a revert does to the finding's record.** A finding whose fix is reverted because it was minor is recorded as `minor`, `closed`, with the line `audit-closed-minor: <id>` in the review 3 report and the id in `closed-minor.txt`. It is not open and is not counted in `open-blocking`. It is not "resolved" either: the text it asked for is gone on purpose. It stays visible so a reader can see what was dropped.

**The exact computation** (`fix_audit.py verdict --dir D --report R3`). Inputs are files only.

1. `closed` = ids in `D/closed-minor.txt` (empty if `apply-log.md` ends in `APPLY_STOP` or is absent).
2. `reported_open` = ids on the report's `open-blocking:` line (`none` means empty). If the line is missing, the script prints `FAIL verdict-line-missing` and writes verdict FAIL.
3. `open` = `reported_open` minus `closed`. (Review 3 should not list closed ids; the subtraction is defensive and every removed id is printed.)
4. `report_verdict` = the last non-empty line of `R3`, which must be `verdict: PASS` or `verdict: FAIL`; anything else is FAIL.
5. `expected` = FAIL if `open` is not empty, else PASS.
6. `final` = FAIL if `expected` is FAIL or `report_verdict` is FAIL; PASS only when both are PASS.
7. If `expected` and `report_verdict` disagree, `final-verdict.md` carries `consistency: DISAGREE` and the script exits 2. The verdict is still FAIL if either side is FAIL (fail closed). A PASS in the report with an open id is never accepted.
8. Output file: `open: <ids>`, `closed-minor: <ids>`, `audit: <state from the report>`, `consistency: OK|DISAGREE`, and the last line `verdict: PASS` or `verdict: FAIL`.

Properties: the script never lowers a FAIL; it cannot create a PASS that the review 3 report did not already state; the only judged inputs are review 3's own blocking classification (as in 427) and the audit table's effect on `closed-minor.txt`, which is limited to ids the prior report already graded minor. So the audit cannot hide a blocking finding. The worst thing the audit can do to a verdict is cause a shrink or revert that review 3 then flags as a new blocking finding, turning a would-be PASS into FAIL.

**Review 3's prior-blocking table is unchanged**: it lists the blocking ids of `R2` as `resolved|open|regressed`. Because closed ids were minor, no row disappears. The audit never touches this table.

## 9. Three placements compared, with predicted numbers
### 9.1 The three placements
| | **P (primary, owner's idea)** | **A (after every fix cycle)** | **B (triage before the first fix)** |
|---|---|---|---|
| When | once, after cycle 2, before review 3 | after cycle 1 (before review 2) and after cycle 2 (before review 3) | after review 1 and after review 2, before each reviser runs |
| What the auditor sees | the finished fix text | the finished fix text, twice | findings only; no fix text exists yet |
| Questions answered | severity and necessity, shrink | same, twice | severity only ("which findings deserve a fix") |
| Enforcement | script reverts/shrinks hunks | same script, called twice | cannot edit text that does not exist; a script after the reviser reverts hunks that cite ids outside the approved list |
| Brief lines changed in S1 | 1 (review 3) | 2 (review 2 and review 3) | 3 or more (each reviser brief gets the approved list; reviewers unchanged) |
| Necessity / shrink test | yes | yes | no |
| Beats a brief that says "apply confirmed findings" (E3) | yes, it checks the result | yes | only through the post-fix id check; the triage list itself is another instruction the brief can override |
| Extra subagents per loop | 1 | 2 | 2 (triage) |

### 9.2 Prediction model, with every input marked
Target: review-3 open critical+major, `R3_after = R3_base x (1 - f)`, with `f = s x (m x r + (1 - m) x h)` for one audited cycle.

| Symbol | Meaning | Value | Basis |
|---|---|---|---|
| `R3_base` | review-3 proxy of the 427 + flags arm | 3.5 (replicates 6 and 1) | `ARMB-REPORT.md:20`. A 427-without-flags base (5.5) is also shown |
| `s` | share of new findings that sit on changed lines | 0.95 | mean of 89% (review 2) and 100% (review 3), `AB-REPORT.md:30` |
| `m` | share of a cycle's added bytes that come from minor-finding fixes | 0.35 (range 0.2 to 0.5) | **UNVERIFIED.** In flg-r2 cycle 2, 9 of 15 rows (60%) were minor, but minor rows are one-clause corrections, so I put their byte share below their row share. Bytes per row were not measured |
| `r` | share of those minor bytes the mechanism removes | P and A: 0.8 (0.5 to 1.0); B: 1.0 | P and A: the default-is-deletion brief with a model veto; B: script, no veto. An assumption |
| `h` | share of blocking-fix bytes saved by shrink | P and A: 0.10 (0 to 0.2); B: 0 | **UNVERIFIED** assumption; B cannot shrink |
| compounding | an audited cycle 1 means fewer review-2 findings, so a smaller cycle 2 | multiply by `(1 - f/2)` for each earlier audited cycle | assumption: half strength |

Growth model: points saved in a cycle = (points that cycle adds) x `(m x r + (1 - m) x h)`. Points added: cycle 1 about 19, cycle 2 about 11 (E5). Base growth for the 427 + flags arm: 30.0% (27.8 and 32.1).

Two honest limits of the model. First, it assumes the review-3 proxy scales with changed lines, which E7 supports (89% to 100% on changed lines) but does not prove; E4 shows the blocking R3 finding of flg-r2 (N12) came from a *blocking* row, which none of the three placements removes. Second, `m` and `h` are guesses; the ranges below come from varying them.

### 9.3 Predictions
| | Review-3 open critical+major, 427+flags base (mean; r1 = 6 and r2 = 1 scaled) | Same on 427-only base (5.5) | Growth after 2 cycles (base 30.0%) |
|---|---|---|---|
| **P** | `f = 0.95 x (0.35 x 0.8 + 0.65 x 0.10) = 0.328`; `3.5 x 0.672` = **2.4** (range 1.5 to 3.2); r1 = 4.0, r2 = 0.7 | 3.7 | saved `11 x 0.345 = 3.8` points: **26%** (24 to 29) |
| **A** | `3.5 x 0.672 x (1 - 0.164)` = **2.0** (range 1.1 to 3.0); r1 = 3.4, r2 = 0.6 | 3.1 | saved `19 x 0.345 + 11 x 0.345 x 0.84 = 9.8` points: **20%** (17 to 25) |
| **B** | `f = 0.95 x 0.35 x 1.0 = 0.3325`; `3.5 x 0.6675 x (1 - 0.166)` = **1.9** (range 1.4 to 2.6); r1 = 3.3, r2 = 0.6 | 3.1 | saved `30 x 0.35 = 10.5` points: **19.5%** (16 to 25) |
| Control (measured) | 6.0 | | 63.5% |
| Bar | 3 or fewer | | 44.4% or less |

Reading the table:
- Growth: all three pass the bar by a wide margin, as 427 alone already does (E6). Growth is not a differentiator, and it must not get worse: that is a guard, not a goal.
- Review-3 mean: all three land near 2 to 2.4 at the central estimate, under the bar of 3. P's upper range (3.2) crosses the bar. The differences between P, A and B (0.5 at most) are far smaller than the observed spread between replicates (5 points in Arm B) and cannot be told apart with 2 replicates.
- Per replicate: r1 starts at 6. No placement brings it under 3 (4.0, 3.4, 3.3). So "both replicates better than both controls" (control replicates 8 and 4, i.e. 3 or fewer) is predicted to fail for all three. Expect the mean bar to pass and the per-replicate bar to fail.
- Effect bigger than spread (rule (c) in `ARMB-REPORT.md:25`): predicted unreachable for the review-3 metric with n = 2. Section 14 therefore adds mechanism-level metrics that are not noisy.

### 9.4 Recommendation: P first, with A as the pre-registered follow-up
Reasons, in order:
1. P is the only placement that tests the owner's actual claim (a necessity and severity audit of finished fix text, with shrink). B cannot test it. A tests it twice.
2. P costs one brief line and one subagent. A needs two trigger points and two applies, with a second saved baseline handled by the coordinator.
3. The model says A and B are at best 0.4 to 0.5 better on review-3 count, inside the noise. Paying double for an unmeasurable gain is bad trade before there is a measurement of P.
4. The script is placement-agnostic: moving to A later is the same call after cycle 1. **Layer 0 insurance:** `fix_audit.py plan --auto-minor` reverts every `minor-only` and `unattributed` hunk with no model call. Off by default, but it is the one-flag ablation arm for S1 (section 14) and the cheapest test of whether the model adds anything over the script.

Rejected variant **P-post** (audit after review 3, audit decides the verdict). Pro: it can use review 3's findings as evidence (N5's fix bred N12). Cons: ships text no panel read; no net for a bad shrink; one judge sets the verdict after the last review; and counting a finding as gone because its line was reverted improves the metric without improving the document.

## 10. Mechanical enforcement versus prose
### 10.1 What a script computes (files in, pass or fail out)
Script: `~/.claude/skills/sc-fix-audit/scripts/fix_audit.py` (second path: project `.claude/skills/sc-fix-audit/scripts/fix_audit.py`), run as `uv run --no-project python "<skill base>/scripts/fix_audit.py" <subcommand> ...`. Standard library only.

| Check | Subcommand | Rule | Catches |
|---|---|---|---|
| K1 | `check` | sha256 of the document now equals `state.json` | an auditor (or anyone) edited the spec during the audit |
| K2 | `check` | the table parses: exact header, 8 columns, no empty cell | free-form prose instead of a table |
| K3 | `check` | every hunk in `fix-list.md` is covered by at least one row; no unknown hunk id | an auditor that skipped fixes |
| K4 | `check` | every non-`-` finding id occurs in `state.json` ids (defined by the report) | invented ids |
| K5 | `check` | `claimed` equals the severity token the script read from the report for that id | an auditor misreading the report |
| K6 | `check` | `revert` requires `validated=minor`, `necessary=no`, and none of the row's hunks is `blocking-involved` | the auditor burying a CRITICAL, FR-8, FR-9 or MAJOR-blocking fix |
| K7 | `check` | where two rows share a hunk, the strongest verdict wins (keep over shrink over revert) | a conflict hiding a revert of a needed hunk |
| K8 | `check` | `keep` with `validated=blocking` needs an `evidence` cell of 20 or more characters; `revert` with `validated=minor` needs one too | a blocking claim or a deletion with no stated reason |
| K9 | `check` | each shrink entry: `old` occurs once, `new` shorter, ids in `old` kept in `new`, no new id-like token | a shrink that adds text or drops the finding id |
| K10 | `plan` | revert rows are built from the diff, not from the table | typed or hallucinated old/new text |
| K11 | `apply` | all-or-nothing, exact-once, atomic replace, post-write readback | partial or corrupt writes |
| K12 | `verdict` | the section 8 computation, fail closed | a PASS with an open id; a missing `open-blocking:` line |
| K13 | `verdict` | the report carries `audit:`, `audit-closed-minor:` and `open-blocking:` lines, and the `audit:` state equals what `apply-log.md` says | a review session that skipped or faked the audit step |

K13 closes most of the "did the session really run the script" gap: if `apply-log.md` ends `APPLY_OK` but the report says `audit: skipped`, or the reverse, the verdict file says `consistency: DISAGREE`.

### 10.2 What only prose can do, and the residual risk
| Prose-only item | Where it lives | Residual risk |
|---|---|---|
| The review session starts the subagent, passes the brief verbatim, writes the returned table to `fix-audit.md` unedited | bullet 8 of the variant | the session paraphrases or trims the brief. K5 and K8 catch some of the damage; nothing proves the brief was verbatim |
| The auditor's severity judgment (Q1) and necessity judgment (Q2) | `auditor-brief.md` | wrong in either direction. Guards limit the damage to minor-only hunks (K6) and to shrink of blocking fixes (caught by review 3). They do not make the judgment right |
| Review 3 treats closed-minor ids as closed and does not re-grade them as blocking | bullet 8, bullet 7 | the reviewer re-opens a closed finding as blocking anyway. `verdict` K12 would then show it in `open-blocking:` and the run is FAIL; the effect is visible but not prevented |
| Review 3 writes the three machine lines honestly | bullet 8 | a made-up `open-blocking: none`. K12 compares it with the report's own last line, but if both are wrong together nothing catches it |
| The `--apply-audit` consent | the brief | consent is a flag in a brief, not a user prompt (Q1) |

**Tests of prose prove text exists, not obedience.** `tests/skills/test_spec_panel_ponytail.py` pins that the sentences are present and that bullets 1 to 7 are untouched. It cannot show that a reviewer follows bullet 8. The only evidence of obedience is the S1 run: K13 and the machine lines make it checkable per run (section 14).

Deliberately not mechanized: dangling cross-references after a revert (review 3's job; a script rule would be a new rule set for free text) and a cap on "too much reverted" (K6 is the only brake; a percentage would be a number with no evidence).

## 11. Measured causes removed and left
| Measured cause | Removed? | How, or why not |
|---|---|---|
| Revisers apply minor findings (flg-r2 cycle 2: 15 of 15, 9 minor) | **Mostly, for cycle 2** | the script nominates minor-only hunks and the default is revert; works even when the brief says "apply confirmed findings" (E3). Not for cycle 1: out of scope in P, in scope in A |
| Revisers add mechanisms for minor findings | **Partly** | unattributed hunks (text with no finding id) default to revert; the necessity question (Q2) asks for deletion first. Mechanisms added for *blocking* findings stay unless a smaller text fully solves them |
| Severity labels drift upward | **Partly, without changing the reviewer** | Q1 re-validates only to decide revert versus keep. The script protects hunks of CRITICAL, FR-8, FR-9, MAJOR-blocking findings from whole revert, so label drift on *those* is not corrected, only shrunk. The reviser's and reviewer's labelling behaviour itself is untouched |
| 89% to 100% of new findings sit on lines the last fix changed | **Reduced, not removed** | model: about a third fewer changed lines at review 3 (`f` = 0.33). The remaining changed lines are fixes for blocking findings; they keep breeding defects (N12 from N5) |
| Review 3 ends with open critical+major (control 6.0, 427 5.5, 427+flags 3.5) | **Reduced by about 30% (model)** | predicted 2.4 on the 427+flags base; not a guarantee of PASS |
| Growth after two cycles (control 63.5%, 427 29.7%) | **Slightly (about 4 points)** | cycle 2 is 37% of 427-arm growth; P trims about a third of it. Already under the bar |
| Nothing mechanical stops the loop | **Not changed** | the 3-review cap remains the only stop. The script adds a mechanical *check* at one point (before review 3) and a fail-closed verdict computation, not a new stop rule |
| No clean PASS in any run | **Not addressed** | defects from necessary fixes remain; a PASS needs zero open blocking at review 3 |

What the mechanism leaves, in one line: every fix for a blocking finding, its derived defects, all of cycle 1, the reviewer's own findings volume (total findings per round fall only modestly, `AB-REPORT.md:31`), and any instruction in a brief that widens the work.

## 12. Exact file changes, file by file
All paths are in this repo. Source of truth is `src/superclaude/`; `make sync-dev` makes the `.claude/` dev copies; nothing under `.claude/` is staged (project CLAUDE.md). Nothing is committed by this design.

| # | File | Action | Content |
|---|---|---|---|
| 1 | `src/superclaude/commands/spec-panel-ponytail.md` | **new** | byte copy of the current `src/superclaude/commands/spec-panel.md` (486 lines) with exactly these differences: (a) front matter `name: spec-panel-ponytail` and a description ending "Variant: audits the cycle-2 fixes before review 3."; (b) H1 `# /sc:spec-panel-ponytail - ...`; (c) Usage line tail ` [--apply-audit]` (the first Usage code line); (d) one new bullet 8 at the end of `## Review Loop`; (e) one new section `## Fix Audit (review 3 only)` placed right after `## Review Loop`. Bullets 1 to 7 stay byte-identical |
| 2 | `src/superclaude/skills/sc-fix-audit/SKILL.md` | **new** | thin carrier skill: frontmatter `name: sc-fix-audit`, a one-sentence description saying "script and brief carrier for /sc:spec-panel-ponytail, not a user workflow", a short note on the five subcommands. Frontmatter shape copied from an existing small skill (UNVERIFIED which; pick one at implement time) |
| 3 | `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py` | **new** | stdlib only (`argparse`, `difflib`, `hashlib`, `json`, `os`, `re`, `pathlib`). Subcommands `prepare`, `check`, `plan` (flag `--auto-minor` for the ablation: revert all `minor-only` and `unattributed` hunks with no table), `apply`, `verdict`. Exit codes: 0 ok, 1 check or apply failure, 2 verdict inconsistency. Target size about 250 lines |
| 4 | `src/superclaude/skills/sc-fix-audit/refs/auditor-brief.md` | **new** | the verbatim brief of section 4 |
| 5 | `tests/skills/test_spec_panel_ponytail.py` | **new** | static pins (see below) |
| 6 | `tests/skills/test_fix_audit_script.py` | **new** | unit tests of the script on small temp-dir fixtures (see below) |
| 7 | `docs/designs/spec-panel-ponytail.md` | **new** | the merged design note, the template for which is this file after the debate; states the one-line substitution and the install steps |

**Text of the additions to the variant command** (installed-path rule: no `src/superclaude/` string):
- Bullet 8 (one line, like bullets 1 to 7): `**Fix audit** (variant only): at a --re-review run whose prior report is review: 2 of 3 with verdict: FAIL and a non-empty diff against the baseline, run the Fix Audit section before reviewing; the audit may revert or shrink only hunks the diff shows, never edits without --apply-audit, and its outputs are the three report lines audit:, audit-closed-minor: and open-blocking:; review 3 still grades by bullets 2 to 7.`
- Section `## Fix Audit (review 3 only)`: the nine steps of 3.3 as a numbered list, the script path with the dual-surface rule (installed `~/.claude/skills/sc-fix-audit/scripts/fix_audit.py` first, else the project `.claude/skills/sc-fix-audit/scripts/fix_audit.py`), the instruction to read `refs/auditor-brief.md` from the same skill folder and pass it verbatim, and the fail-open rule ("any failed step: record `audit: skipped(<reason>)` and review 3 proceeds as in bullets 1 to 7").

**Install for an experiment** (the original is never edited): `cp src/superclaude/commands/spec-panel-ponytail.md ~/.claude/commands/sc/spec-panel-ponytail.md` and copy the folder `src/superclaude/skills/sc-fix-audit/` to `~/.claude/skills/sc-fix-audit/`. `~/.claude/commands/sc/spec-panel.md` is not touched. `superclaude install` would also copy both for every user; if that is not wanted before the experiment ends, keep the variant uncommitted until the S1 result is in, or gate it (Q5).

**Static tests (`test_spec_panel_ponytail.py`):**

T1 front matter name is `spec-panel-ponytail`. T2 **refactor-safety**: the variant with the five known differences removed equals `spec-panel.md` byte for byte (the core guard against drift). T3 bullets 1 to 7 equal the original's; bullet 8 names `--apply-audit`, `audit:`, `audit-closed-minor:`, `open-blocking:`. T4 canonical cap text and at-cap clause present once (imports `CANONICAL_CAP_TEXT`, `AT_CAP_CLAUSES` from `test_review_severity_rule.py`). T5 no `src/superclaude/` string in the variant or the brief. T6 the script is named by installed path with the dual-surface fallback. T7 the brief file holds the behaviour-carrying sentences (Step 0 load and fallback header, Q1 wrong-result sentence, "default is deletion", the CRITICAL/FR-8/FR-9 revert ban). T8 the original `spec-panel.md` has no `--apply-audit` or `Fix Audit` text. UNVERIFIED: whether `test_review_severity_rule.py` scans every file under `commands/` and would flag the new file; run it first at implement time and adapt the text, not the test.

**Unit tests (`test_fix_audit_script.py`):** `prepare` finds expected hunks and ignores a whitespace-only change; class `minor-only`, `blocking-involved`, `unattributed`, `foreign-id` assigned on a four-hunk fixture; `check` rejects a table missing a hunk, an invented id, a revert of a CRITICAL id, a revert of a hunk shared with a blocking id, a mismatched `claimed`, and a changed document hash; `plan` builds revert rows from the diff; `apply` is all-or-nothing (a non-unique `old` gives `STOP`, file bytes unchanged), idempotent (`already`), atomic (no `.tmp` left), and closes only fully reverted minor ids; `verdict` fails closed on a PASS with an open id, a missing `open-blocking:` line and a `DISAGREE`.

**Substitution an experiment brief needs (one line).** In the review-3 dispatch brief only, replace

`/sc:spec-panel @<spec> --mode critique ... --re-review <R2 report> --baseline <spec before cycle 2>`

with

`/sc:spec-panel-ponytail @<spec> --mode critique ... --re-review <R2 report> --baseline <spec before cycle 2> --apply-audit`.

Review 1, review 2 and the reviser briefs keep `/sc:spec-panel`. Pre-run checks the recorder logs: sha256 of the installed variant and of `fix_audit.py`, and that `~/.claude/commands/sc/spec-panel.md` is unchanged.

**Not changed:** `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md` (no plugin mirror for the variant at this stage; plugin parity of the new file is UNVERIFIED and left until the variant earns promotion), `HOW-WE-WORK.md` and its plugin copy (no routing row), `tests/skills/test_spec_panel_review_loop.py`, `sc-implement-protocol/refs/qa.md`.

## 13. Later adoption by other loops
The script is generic: it needs a baseline copy, a current document, and a report whose finding ids carry a severity word. Its severity vocabulary is a constant (`CRITICAL`, `FR-8`, `FR-9`, and `MAJOR` with `blocking`), which would become a `--blocking-tokens` option on adoption.

| Loop | Could it adopt the audit later? | What stands in the way |
|---|---|---|
| `/sc:reflect` (UC-2 post-execution, heterogeneous reviewers) | Possibly, as a step after a remediation loop | reflect grades divergences by a 4-category taxonomy, not by blocking and minor, so ids would need a severity mapping first. Its reviewers are read-only by design (`reflect-reviewer`), which fits "auditor never edits". Not evaluated here |
| rf-qa Fix Cycle (CRITICAL, IMPORTANT, MINOR) | Yes with `--blocking-tokens CRITICAL,IMPORTANT` | rf-qa fixes in place, so the baseline must be saved by whoever runs the cycle; the apply step would need rf-qa's consent rules (UNVERIFIED) |
| `/sc:implement` final review | **Not without reversing a written rule** | `src/superclaude/skills/sc-implement-protocol/refs/qa.md:91`: a ponytail-style judgment never changes a severity or a verdict, and the protocol never invokes the plugin. Adopting the audit there means editing that sentence on purpose, with the owner's decision recorded. My variant respects the rule in spirit (the ponytail table does not set a verdict; a script does) but the line is still a hard stop for any direct reuse |
| Plain agents and document loops that never call `/sc:spec-panel` | No | four of five incident types are outside spec-panel (`AB-REPORT.md:43`) |

Recommendation: do not adopt anywhere until S1 shows the mechanism works as written. The script's generic shape is the only provision made now; nothing is built for other loops.

## 14. Measurement plan on S1 and the falsification statement
### 14.1 Design
- **Scenario S1**: the Orca worker-contract spec (57,763 bytes), base commit 2cb683f5, model claude-opus-5-5, loop of 3 reviews and 2 fix cycles, the same verbatim briefs as Arm B (which pass `--re-review` and `--baseline` at review 2 and review 3) with the single line change of section 12. Recorder folders `exp346-ab-ptl-r1` and `exp346-ab-ptl-r2`, metrics in the same `metrics.json` schema.
- **Arms**: the new arm (2 replicates) against the reused controls ctl-r1, ctl-r2 and Arm B flg-r1, flg-r2 (the same non-simultaneous caveat as `ARMB-REPORT.md:35`). Optional third arm, if budget allows 2 more runs: **ablation** with `plan --auto-minor` and no subagent. If the ablation matches the full arm, the ponytail model call adds nothing and should be dropped.
- **Run validity (void and re-run once if any fails)**: the installed variant and script sha256 recorded before the run; `~/.claude/commands/sc/spec-panel.md` unchanged (install watcher); `fix-audit.md` header says `auditor: ponytail-review`; `check.log` ends `CHECK_OK`; `apply-log.md` ends `APPLY_OK`. A run that fails only because of the mechanism (check failure, apply STOP) is recorded as an implementation defect, not as evidence against the idea.
- **Primary metrics** (the pre-registered bar of D10 and D11): review-3 critical+major proxy; growth after fix cycle 2 (bytes, `wc -c` against the 57,763-byte original); clean pass.
- **Mechanism metrics** (low noise, so they can show "works as written" even if the primary metric is lost in spread): hunks total, reverted, shrunk, kept, skipped; bytes removed by the audit and as a share of cycle-2 added bytes (model `m x r` predicts about 0.28); number of `closed-minor` ids; how many `minor-only` hunks the auditor vetoed with a Q1 sentence; share of review-3 findings with `origin=changed` (E7 says 89% to 100%) and the count of review-3 findings that quote a hunk the audit shrank (audit-caused findings); `consistency` result of `verdict`; cost: tool calls, tokens and wall time of the audit step.

### 14.2 Predictions, written before any run
- Review-3 critical+major mean 2.4 (range 1.5 to 3.2; control 6.0, Arm B 3.5, bar 3); per replicate about 4 and 1 if the Arm B profiles repeat.
- Growth after two cycles 26% (24% to 29%; control 63.5%, Arm B 30.0%, bar 44.4%).
- Share of cycle-2 added bytes removed 0.28 (0.12 to 0.5). Audit-caused review-3 findings 0 to 1 per run. Clean PASS: no (none in 6 prior runs).
- Extra cost 14 to 18 tool calls, 1 subagent, 4 to 8 minutes (UNVERIFIED estimate, no timing data read).

### 14.3 What counts as failure (stated now)
The idea failed, and should not be promoted, if any of these holds on valid runs:
- **F1** the review-3 mean is 4.0 or more (no better than Arm B plus noise), or in either replicate the audited run is worse than the matching Arm B replicate by 2 or more;
- **F2** an audit-caused blocking finding appears in review 3 in both replicates (the mechanism breaks about as much as it fixes), or in any replicate a shrink or revert reopens a prior blocking finding (`open` or `regressed` in review 3 on a hunk the audit touched);
- **F3** growth after two cycles is not at least 1 point lower than the Arm B mean of 30.0%, with at least 3 hunks reverted (the mechanism ran and did nothing measurable);
- **F4** a blind re-grade of an audited final text by an independent reviewer (a `reflect-reviewer` agent with the 427 grading rule and no knowledge of the audit) finds a blocking defect that sits in or depends on a reverted hunk and that review 3 did not report (the audit buried something);
- **F5** the ablation arm (if run) matches the full arm: the model call is dead weight and is removed.

Even if F1 to F4 are all clear, the **pre-registered D11 bar can still be missed** (rule (c), effect larger than spread, and "every replicate better than both controls"; section 9.3 predicts both fail). In that case the honest report is: mechanism works as written, effect on the review-3 count is inside the noise, decision for the owner. Do not retune the bar after the run.

## 15. Honest cost and how this could make the loop worse
**Cost per loop** (estimates; no timing or token data for an audit step was read, UNVERIFIED):

One extra subagent session; about 7 extra tool calls in the review 3 session (five script calls, one Agent call, one file write) plus 6 to 8 reads inside the subagent; 40k to 70k extra input tokens (the auditor reads the spec of about 76 KB, roughly 19k tokens, plus baseline sections and the report); 4 to 8 extra minutes; 8 extra files in `fix-audit/`; 1 brief line in S1.

**How it could make the loop worse** (each with the check that would show it):
1. **A shrink breaks a blocking fix.** The smaller text no longer solves the finding. Review 3 flags it `open`; plain 427 would have shown `resolved`. Net effect: a FAIL the loop would not have had. Check: F2.
2. **A revert removes text something else relied on.** A minor-only hunk is referenced by a blocking fix's wording (a section pointer, a defined term). The script protects hunks that *cite* a blocking id; it cannot see an *unstated* dependency. Review 3 may report a dangling reference as a new blocking finding with `origin=changed`. Check: audit-caused findings metric.
3. **Known-wrong citations are left in the spec.** Reverting citation fixes (C13-style) restores a false line number. That is accepted by the minor rule, but a human reading the final spec finds more small errors than before. This is deliberate debt; it is recorded in `closed-minor`.
4. **The auditor buries a real problem as minor.** Guarded by K6 for CRITICAL, FR-8, FR-9 and MAJOR-blocking; unguarded for a finding the panel graded MINOR that was in fact blocking. That is the same exposure 427 bullet 2 already accepts for MINOR.
5. **Anchoring.** Review 3 sees an audited document and the three machine lines; it may defer to "the audit already looked". Mitigation in design: the auditor is a separate subagent, and review 3's table of prior blocking findings is unchanged. Residual risk is prose only.
6. **The fail-open path hides a broken mechanism.** A missing plugin, malformed table or apply stop makes the run quietly plain 427 plus wasted minutes. The `audit:` line, `check.log` and the run-validity rules of section 14 make it visible.
7. **The ablation could show the model adds nothing.** Then ponytail review is decoration over a script. A valid result, and the reason the ablation arm is in the plan.
8. **The mean bar passes while the per-replicate bar fails**, and a reader takes the mean as proof. Section 14.3 states the expected outcome in advance.

## 16. Open questions
1. **Q1 Consent (C6).** Is a `--apply-audit` flag in the dispatch brief enough consent for the variant to edit the spec through a script? If not, the variant must stop at `apply-rows.json` and the coordinator must run `apply` itself, which makes the S1 change two brief lines instead of one.
2. **Q2 Subagent plugin access.** Can a subagent started inside a dispatched Orca worker load `ponytail:ponytail-review`? UNVERIFIED. If not, every run is `inline-rubric` and the experiment tests the rubric, not the plugin. A one-call probe before S1 settles it.
3. **Q3 Scope.** Cycle 2 only (this design), cumulative (pass the original as `--baseline`), or also a cycle-1 trigger (placement A)? The model says A is worth 0.4 to 0.5 on review-3 count and about 6 more points of growth; cost doubles.
4. **Q4 Severity rubric.** I narrowed "false claim" to "a false claim that leads to a wrong result" (the 427 MAJOR test). The owner's literal list may have meant any false claim. Under the literal list the audit would keep most flg-r2 minor rows and revert little. Which does the owner want?
5. **Q5 Distribution.** `superclaude install` copies every command and skill to every user's `~/.claude/`. Ship the variant and the `sc-fix-audit` folder before S1 reads out, or keep them uncommitted until the result is in? Is a plugin-mirror copy needed for parity tests (UNVERIFIED)?
6. **Q6 Report format change.** Is requiring three machine lines in the review 3 report acceptable, given 427 pins the report shape in `test_spec_panel_review_loop.py` only for the original command?
7. **Q7 One format retry.** None is allowed (single pass, fail open). Add one format-only resend if more than one in five audits fails `check` in S1?
8. **Q8 Unverified model inputs.** The prediction rests on `m`, `h` and `r`. `m` can be measured now without a run: diff `specs/history/spec-v2-after-round1.md` against `spec-v3-after-round2.md` in flg-r2 and sum the bytes of hunks citing only N7-N11 and C9-C14. Do it before the S1 budget is spent.
9. **Q9 Ablation first?** `--auto-minor` alone may deliver most of the effect at zero model cost. Run it as the first S1 arm and the ponytail arm only if it leaves room?
10. **Q10 Review-3 parsing.** `verdict` relies on the `open-blocking:` line because report formats vary (flg-r2 uses `**N12.** MAJOR, blocking`). Accept the extra line, or parse headers (more fragile)?

## 17. Verification status of what I claimed
Read this session: seed brief, enrichment, `spec-panel.md` lines 230-290 and 445-455, the design note lines 1-120, ponytail SKILL.md in full, `AB-REPORT.md`, `ARMB-REPORT.md`, `disposition-round2.md` lines 1-40, `disposition.md` lines 1-30, `spec-panel-round3.md` lines 1-130, `qa.md:85-96`, `apply_rows.py` lines 1-60, the head of `test_spec_panel_review_loop.py`, and `installation.md` grep for ponytail. UNVERIFIED and flagged inline: bytes per disposition row (`m`), subagent plugin access, plugin parity and severity-rule test scope for a new command file, timing and token cost, severity token formats of reports other than flg-r2's round 2 and round 3, and whether the round-1 disposition (22 findings, 13 blocking) had minor rows applied in a share like round 2.
