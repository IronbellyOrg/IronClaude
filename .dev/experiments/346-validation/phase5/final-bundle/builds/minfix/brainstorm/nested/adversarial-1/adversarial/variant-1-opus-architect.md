# Variant 1 (opus, architect): per-finding fix budget with a stdlib checker for `/sc:spec-panel-minfix`

Issue #346, theme minfix. Builds on PR 427 (`## Review Loop`, `src/superclaude/commands/spec-panel.md:256-264`). Written 2026-11-08.

## 1. Problem and evidence

**Problem in one sentence.** Each fix cycle adds far more text than the blocking findings need, the next review attacks that added text, and nothing outside the reviser's own judgment limits the addition.

**What 427 did and did not do** (`exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`, `ARMB-REPORT.md`): on scenario S1 (Orca worker-contract spec, 57,763 bytes, 2 replicates per arm) growth after two fix cycles fell from 63.5% (control) to 29.7% (427) and 30.0% (427 plus `--re-review/--baseline`, "Arm B"). The review-3 critical+major proxy stayed at 6.0 / 5.5 / 3.5 (bar: 3 or fewer, every replicate better than every control). No run reached PASS. In 427 reports 89% (R2) and 100% (R3) of new findings carry `origin=changed`.

**Measured reviser behaviour (this variant's own measurement).** Stdlib `difflib` over sentence units (lines split at `. ! ? ;` and at table-cell ` | `), word-level diff inside replaced units, on the spec history copies in the six A/B worktrees (byte counts read as text, so they differ from `wc -c` by a few bytes):

| run | cycle | words added | words removed | changed sites | new headings | net normative words | net condition words (if/unless/when/except/otherwise/before/after/until) |
|---|---|---|---|---|---|---|---|
| ctl-r1 | 1 / 2 | 2351 / 3004 | 361 / 197 | 45 / 46 | 0 / 1 | +4 / +8 | +29 / +38 |
| ctl-r2 | 1 / 2 | 2936 / 3269 | 366 / 161 | 69 / 49 | 1 / 1 | +10 / +21 | +43 / +50 |
| trt-r1 | 1 / 2 | 1147 / 1062 | 201 / 84 | 39 / 32 | 4 / 1 | +4 / +9 | +10 / +12 |
| trt-r2 | 1 / 2 | 2181 / 1278 | 257 / 155 | 50 / 50 | 7 / 6 | +11 / +2 | +21 / +18 |
| flg-r1 | 1 / 2 | 1600 / 1004 | 132 / 229 | 46 / 68 | 0 / 0 | +6 / +3 | +18 / +7 |
| flg-r2 | 1 / 2 | 1997 / 955 | 193 / 94 | 49 / 25 | 1 / 0 | +7 / +2 | +28 / +13 |

The draft has 8,148 words and 68 condition words. Three facts follow:

1. **Revisers almost never delete.** Added-to-removed word ratio is 4.4:1 to 20:1 in every cycle. "Narrow" is not a move they make unprompted.
2. **427 made revisers smaller but not small.** 427 arms still add 955-2181 words per cycle; the lowest (flg-r2 cycle 2: 955 words, 25 sites) is also the only run whose review 3 came close to PASS (1 blocking). Sites in cycle 2 against the R3 proxy: 25 -> 1, 32 -> 6, 46 -> 8, 49 -> 4, 50 -> 5, 68 -> 6 (weak, n = 6).
3. **Per finding, most 427 fixes are already small; the tail and the unattributed text are the problem.** Attributing added words to the finding id cited in the same sentence (427 requires inline ids): median added words per finding 38 / 23 / 20 / 20.5 / 12 (flg-r2 c1, flg-r2 c2, trt-r1 c1, trt-r2 c1, trt-r2 c2); 62-79% of findings added 40 words or fewer; the top quartile reaches 71-146 words and 5-16 sites. Words in changed sentences that cite no finding id: 1028 / 419 / 586 / 1669 / 719 (44-77% of the cycle's additions; an upper bound, since a fix may cite its id in a neighbouring sentence).

**Where the review-3 blocking findings came from (traced in the reports).**
- flg-r2 (closest to PASS): its one R3 blocking finding N12 sits on text the reviser added for R2 finding N5, and N5 sits on text added for R1 finding **F22, a non-blocking finding** the reviser applied anyway ("bound at most 30 s ... checked by AC-0.4 step 1", `exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md:37`; N5 quotes "(F22)", `spec-panel-round2.md:120`). R3 minor N13 came from an unrequested "Related fix" (`disposition-round2.md:21`), minor N14 from the applied minor N9.
- flg-r2 R2: all six blocking findings N1-N6 are `origin=changed` and each attacks a site an R1 fix added: N1 <- F10 (WC-7 Skill call), N2 <- F1 (new `worker_status` field; "The F1 fix assumed flat contracts"), N3 <- F11 and the new section 2.4, N4 <- F12 (new SA-2 sentence), N5 <- F22 (minor), N6 <- F2 (new 2.4 path check in 7.2 step 3). The reviser applied 21 of 22 R1 findings, 8 of them non-blocking, because "the coordinator brief says to apply confirmed findings" (`disposition.md:10`).
- trt-r1 R3: 5 of 6 blocking findings are FR-8 GAP rows on guards the round-2 revision created (`exp346-ab-trt-r1/.dev/orca-command-refactor/review/spec-panel-round3.md:143-148`). New condition clauses are new guards, and FR-8 makes their GAP rows MAJOR.

**Why 427 cannot stop this by itself.** Bullet 6 is prose: "revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for". A blocking finding "calls for" almost any mechanism, minor findings get applied when the coordinator's brief says so, and 427's own inline finding-id tags add 25-61 id citations per cycle (in the 427-arm cycles whose reviser used F/N ids), which the next review then citation-checks. 427's design rejected a size limit because "nothing could check it from text" (`docs/designs/spec-panel-review-loop.md:73`). A script can check it.

## 2. Mechanism (each loop step, in order)

Three parts, nothing else: a **budget class** the reviewer writes per blocking finding, a **ledger** the reviser writes outside the spec, and one **stdlib checker** (`fixcheck.py`) that both the reviser and the next re-review run. The coordinator gets no new duty, so the S1 briefs change only by the command name.

### 2.1 Review N (N = 1 or 2): reviewer writes the inputs

1. Review as 427 does (grading, verdict, `review: N of 3`, re-review scope when flagged).
2. Copy the file it reviewed, byte for byte (`cp -p`), to the report path with `-reviewed.md` in place of `.md` (for `review/spec-panel.md`: `review/spec-panel-reviewed.md`). This is the exact text the findings refer to and the checker's baseline. 427's coordinator copy for `--baseline` stays as it is; the two should be equal.
3. In the `Reviser brief` (427 bullet 6), write three machine lines and the filled-in checker command:
   ```text
   reviewed-copy: review/spec-panel-reviewed.md
   fix-budget: F1=B F2=L F5=C F10=B F11=B
   fix-budget-override: F2 the spec states no contract path for 5 commands; no class-C fix can state one
   check: uv run --no-project python "$HOME/.claude/skills/fix-budget/scripts/fixcheck.py" --report review/spec-panel.md --revised specs/orca-worker-contract-spec.md
   ```
   The checker rejects (exit 3) an override line whose id is not `L`, an `L` without an override line, and a second `L`. Classes: `C` = CRITICAL; `B` = every other blocking finding, FR-8/FR-9 included; `L` = override, at most one per report, only with a reason, never for an `origin=changed` finding (its first remedy is to narrow or revert the change that caused it). Minor findings are not listed, so their budget is zero.

### 2.2 Fix cycle: reviser

4. **Preflight.** Run the `check:` command before editing. With no edits it exits 0 and prints each listed finding's limits and the ledger line format. Exit 3 here (missing copy, no `fix-budget:` line, malformed override) means: edit nothing, report the checker output.
5. **Edit, delete or narrow first.** Edit only sentences a listed finding names; prefer deleting or narrowing the faulty sentence over adding one; add no heading and no finding id to the spec.
6. **Ledger.** For every changed sentence write one JSON line to `<report stem>-ledger.jsonl` (for `review/spec-panel.md`: `review/spec-panel-ledger.jsonl`):
   ```text
   {"id": "N3", "old": "<exact baseline sentence, or empty for a pure insert>", "new": "<exact revised sentence, or empty for a deletion>", "why_not_narrow": "<one line; required when the site adds net words>"}
   {"id": "N5", "escalate": "<one line: the smallest fix found and why it cannot fit class B>"}
   ```
   An escalated finding gets no edit and stays open. Escalate, never expand.
7. **Check.** Run the `check:` command again. Exit 0 ends the revision. Exit 2 lists each breach with the measured value, the limit and `revert_to` (the baseline text of the site). One cut-down attempt (narrow, or drop the site), then re-run; if it still exits 2, restore each breaching finding's sites to `revert_to`, replace that finding's ledger lines with one `escalate` line, and re-run. Restoring baseline text removes the site, so this always reaches exit 0 unless a site is unattributed and not restored. At most 3 checker runs after editing.

### 2.3 Review N+1: re-review uses the checker, not the reviser's word

8. Before the 427 prior-blocking table, the re-review runs the same checker with `--report <prior-findings-file> --revised <file under review>` and writes its one-line summary under the `review: N of 3` header, for example `fixcheck: pass; sites 14; words +212/-96; bytes 70,255 -> 71,903; escalated N5; over-budget none; unattributed 0`. This run is authoritative: it does not matter whether the reviser ran the checker.
9. In the prior-blocking table, a finding the checker reports over budget is `open` (over budget): an over-budget fix is never credited. A finding the ledger escalates is `open` (escalated) with the reviser's reason. Unattributed sites are counted in the summary and reviewed like every other changed line (427 bullet 5); they are not graded blocking for being unattributed.
10. The re-review reads the checker report (which carries each finding's verified old/new sentences), not the raw ledger, and only for the prior-blocking table. The new-findings pass keeps 427's changed-lines scope and does not use the ledger.
11. At review 3 (`verdict: FAIL`) the escalation to the user lists the open blocking findings with the ledger's escalation reasons. Cap unchanged: 2 fix cycles, 3 reviews.

### 2.4 Budget per finding (the checker's constants are the only source)

| class | set by | added words | net words (added - removed) | changed sites | new sentences | new normative words | new condition words | new ids | new headings |
|---|---|---|---|---|---|---|---|---|---|
| not listed (minor, non-blocking MAJOR) | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `B` blocking MAJOR, FR-8/FR-9 | reviewer | 40 | 30 | 2 | 1 | 1 | 1 | 0 | 0 |
| `C` CRITICAL | reviewer | 80 | 60 | 3 | 2 | 2 | 2 | 0 | 0 |
| `L` override (at most 1 per report) | reviewer, with reason | 150 | 120 | 4 | 4 | 3 | 3 | 1 | 0 |

Definitions the checker computes: a **site** is one run of consecutive changed sentence units; words removed are free (delete or narrow costs nothing but a site); an identical single-token substitution repeated across sites for one finding (a rename) counts as one site; **normative words** are `MUST SHALL must shall never always required forbidden`; **condition words** are `if unless when whenever except otherwise` (new conditions are new guards, which FR-8 turns into MAJOR GAP rows); a **new id** is a token like `WC-12`, `AC-0.6` or any finding id from `fix-budget:` that is absent from the baseline; a **new heading** is a new line starting `#`. Whitespace-only changes are ignored, as in 427 bullet 5.

Calibration: 62-79% of 427-arm per-finding additions already fit 40 words (section 1), so class `B` lets ordinary fixes through and cuts the tail (new fields, new tables, new check steps). Two sites lets a fix change a rule and the one check that depends on it. One condition word per `B` fix bounds new guards. Expected cycle-1 ceiling at 13 blocking findings (2 `C`, 11 `B`, 1 `L`): 160 + 440 + 150 = 750 added words, against 1,147-2,181 in the 427 arms.

### 2.5 Checker report and exit codes

`fixcheck.py` writes `<report stem>-fixcheck.json` and prints the summary line plus one line per breach.

```text
{
  "tool": "fixcheck", "version": 1, "result": "pass|breach|input-error",
  "report": "...", "baseline": "...", "revised": "...", "ledger": "...",
  "bytes_before": 70255, "bytes_after": 71903, "words_before": 9980, "words_after": 10096,
  "findings": [{"id": "N3", "class": "B", "sites": 2, "words_added": 34, "words_removed": 9,
                "bytes_added": 241, "new_sentences": 1, "new_normative": 1, "new_conditions": 0,
                "new_ids": 0, "new_headings": 0, "escalated": false, "escalate_reason": null,
                "override_reason": null, "over": [],
                "changes": [{"old": "...", "new": "...", "why_not_narrow": "..."}]}],
  "unattributed": [{"site": 7, "baseline_text": "...", "revised_text": "..."}],
  "ledger_errors": [{"line": 3, "error": "old-not-in-baseline|new-not-in-revised|bad-json|unknown-id|add-without-reason"}],
  "breaches": [{"id": "N3", "metric": "sites", "value": 3, "limit": 2, "revert_to": ["..."]}],
  "summary": "fixcheck: breach; sites 17; words +412/-96; ..."
}
```

| exit | meaning | who acts |
|---|---|---|
| 0 | every site attributed to a listed finding, every finding within its class, escalations allowed | reviser stops; re-review records `pass` |
| 2 | breach: a finding over a limit, an edit attributed to an unlisted (minor) id, an unattributed site, or a ledger error | reviser cuts down or reverts (step 7); re-review marks over-budget findings `open` |
| 3 | input error: missing or empty file, no `reviewed-copy:` or `fix-budget:` line, more than one `L`, an `L` without reason or a reason without `L`, unreadable ledger | reviser edits nothing further and reports; re-review records `fixcheck: input-error <message>` and continues without it |
| 1 | the checker crashed (Python traceback) | treated as exit 3 |

### 2.6 What changes against 427's Reviser contract (bullet 6)

| 427 bullet 6 says | minfix bullet 6 says | why |
|---|---|---|
| revise only text a blocking finding names | same, and the checker breaches any site attributed to an unlisted id or to no id | turns the rule into a computed check; removes minor-fix chains (F22 -> N5 -> N12) |
| add no rule, mechanism or section no blocking finding calls for | per-class limits on words, sites, sentences, headings, ids, normative and condition words | "calls for" is judgment; limits are counts |
| each added paragraph or table cites its finding id | the spec carries no finding id; attribution lives in the ledger | ids in the spec are added text the next review citation-checks |
| the reviser reports the byte size before and after | the checker report gives it | computed, not self-reported |

## 3. Causes removed and causes left

| measured cause | effect of this mechanism | enforcement | residual |
|---|---|---|---|
| Edits for minor findings (flg-r2 applied 8 of 9 minor in cycle 1; F22 -> N5 -> N12 is the only R3 blocking chain in the best run) | **Removed.** An unlisted id has budget 0; any site attributed to it, or to no id, is a breach | checker exit 2 at the reviser; credited nowhere at the re-review | A reviser can attribute a minor edit to a blocking id with spare budget (section 7, gaming) |
| Mechanism and section additions (new fields, tables, sections: F1 `worker_status`, F2 section 2.4; 0-7 new headings per cycle) | **Removed for headings and ids; cut for the rest.** 0 new headings in every class, 0 new ids in `B`/`C`; a new field or table no longer fits 40 words and 1 new sentence | checker counts | A mechanism can still be packed into one long sentence within 40 words |
| Unattributed "related fixes" (N13; 44-77% of added words cite no id) | **Removed.** Every site must match a ledger line whose quotes are found in the baseline and the revised file | checker | Ledger lines can be honest about the text and dishonest about the reason |
| Fix-induced `origin=changed` findings (89-100% of new findings) | **Reduced, not removed.** With 427's `--re-review` the next review attacks only changed lines, so the attack surface is the number of sites. Expected cycle-2 sites: about 12 (6 blocking x 2) against 25-68 measured; added words about 150-250 against 955-1,278 | checker caps per finding; the cycle total follows | A 30-word fix can still be wrong; a smaller surface lowers the count, it does not make fixes right |
| New guards from added conditions (5 of 6 trt-r1 R3 blocking findings are FR-8 GAPs on revision-made guards; +7 to +50 condition words per cycle) | **Reduced.** At most 1 new condition word per `B` fix, 2 per `C` | checker | A guard written without a listed condition word ("in that case", "where") is not counted |
| 427's inline finding-id tags (25-61 per cycle where the reviser used F/N ids) | **Removed.** The spec gets no finding id; attribution lives in the ledger | checker counts finding ids as new ids | none |
| Upward severity drift between rounds (a MAJOR non-blocking at R2 re-graded blocking at R3) | **Left.** Grading is unchanged | - | Needs a frozen rubric (stoprule theme) |
| Whole-document re-attack | **Left as 427 left it.** Only `--re-review` scopes the review; minfix shrinks what it scopes to | - | Without the flags (treatment-A briefs) the re-review still reads the whole document |
| No mechanical stop | **Partly.** Fix size now has a mechanical stop; the verdict still does not. The 3-review cap is the only verdict stop | checker for size; cap for rounds | A FAIL at review 3 still escalates; minfix makes that escalation carry reasons |
| Under-fixed blocking findings (new risk this mechanism creates) | **Introduced risk.** A budget too tight leaves a finding `open` or escalated | measured: `open` and `escalated` counts at R3 | section 7 |

Net claim: minfix removes the three sources the traces show grow the next round's blocking count (minor-fix chains, unattributed edits, mechanism-sized fixes) and shrinks the fourth (surface), and leaves grading drift and the verdict untouched. Whether that is enough to reach 3 or fewer at review 3 is what section 6 tests.

## 4. Exact changes (file by file, with the new text or script outline)

Five new files and one optional test edit, nothing else. `spec-panel.md`, its plugin copy, `HOW-WE-WORK.md`, `pragmatic.md` and the 427 pin tests are not touched.

| # | File | Change |
|---|---|---|
| 1 | `src/superclaude/commands/spec-panel-minfix.md` | New. Derived copy of `spec-panel.md` (section 4.1) |
| 2 | `src/superclaude/skills/fix-budget/SKILL.md` | New. Short contract for the checker (section 4.3) |
| 3 | `src/superclaude/skills/fix-budget/scripts/fixcheck.py` | New. Stdlib checker (section 4.2) |
| 4 | `tests/skills/test_fixcheck.py` | New. Behaviour tests on temporary files (section 4.4) |
| 5 | `tests/skills/test_spec_panel_minfix.py` | New. Derivation and pin tests (section 4.4) |
| 6 | `tests/unit/test_cli_install.py` | Optional: add the three new paths to `_PACKAGE_RESOURCES` `commands`/`skills` (presence-only lists, lines 111-121 and 187+); the suite passes without it |

**Why a skill folder and not a `superclaude` subcommand.** A subcommand reaches a worker only after a package reinstall, which an additive experiment cannot do (D9; `~/.local/bin/superclaude` is 5.0.0). The skill-script pattern `uv run --no-project python "<skill base>/scripts/<name>.py"` is established (`src/superclaude/skills/sc-issue-protocol/SKILL.md:72`), needs no package import, and installs as a new folder. The folder is named `fix-budget`, not `sc-...`: `install_skills.py:40-59` removes an `sc-<x>` skill when `commands/<x>.md` exists and does not activate it, so `sc-spec-panel-minfix` would be swept away at install. A command cannot use `<skill base>` (it has none), so the command names the installed path, then the project `.claude/` copy, in the order the project rule gives skills (home first).

**Why not a fixed Bash/`diff` sequence in the command text.** `diff` counts lines, and S1's lines are whole paragraphs (section 1: "a line diff hides size"); per-finding attribution and the class table need code.

### 4.1 `spec-panel-minfix.md`: derived copy, five regions differ

The file is `spec-panel.md` (current master, 486 lines) with exactly these regions changed, and byte-identical elsewhere (pinned by test 5):

1. Frontmatter: `name: spec-panel-minfix`; `description: "Experimental variant of /sc:spec-panel with a per-finding fix budget checked by a script (issue 346); use /sc:spec-panel for normal work"`.
2. H1: `# /sc:spec-panel-minfix - Expert Specification Review Panel (fix-budget variant)`.
3. Usage: both lines start `/sc:spec-panel-minfix `; line 2 drops `[--unattended] [--report-dir <dir>]`.
4. The `## Unattended mode` section (master lines 451-461) is removed. Reason: `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal its list exactly, the variant is never run as an unattended worker, and the 427 file Arm B ran had no such section, so dropping it also keeps the variant closer to the comparator.
5. `## Review Loop` bullets 2, 5 and 6 replaced by the literal lines below; bullets 1, 3, 4 and 7 unchanged; still seven one-line bullets in 427's order.

Bullet 2 (427 text plus one clause):

```markdown
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision; each blocking finding also gets a fix budget class, `C` for CRITICAL and `B` for any other, and at most one per report may get `L` with a stated reason that no class-C fix can close it, never an `origin=changed` finding, whose first remedy is to narrow or revert the change that caused it.
```

Bullet 5 (427 text, then appended):

```markdown
5. **Re-review output**: <427 bullet 5 text unchanged> A re-review first runs the fix checker named in the prior report's `check:` line (bullet 6) and puts its summary line under the `review: N of 3` header; a prior blocking finding the checker reports over budget is `open` (over budget) whatever its text now says, one the ledger escalates is `open` (escalated) with the reviser's reason, and the checker report, not the raw ledger, is used only for this table; checker exit 1 or 3 is recorded and the re-review continues without it.
```

Bullet 6 (replaces 427 bullet 6):

```markdown
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line and omits it at `review: 3`, where the run escalates instead; before writing it the run copies the reviewed file byte for byte to the report path with `-reviewed.md` in place of `.md`, and the brief holds the lines `reviewed-copy: <that copy>`, `fix-budget: <id>=<C|B|L> ...` (every blocking id, nothing else), `fix-budget-override: <id> <reason>` for an `L`, and `check: uv run --no-project python "$HOME/.claude/skills/fix-budget/scripts/fixcheck.py" --report <this report> --revised <the reviewed file>` with both paths filled in (if that script is absent, use the project `.claude/skills/fix-budget/scripts/fixcheck.py`), then restates this bullet (the reviser reads the report, not the command): run `check:` before editing (it prints each finding's budget and the ledger format) and after; edit only sentences a listed finding names, delete or narrow before adding, and add no heading and no finding id to the file; quote every changed sentence, old and new, with its finding id in the ledger the checker names; a finding no in-budget fix can close gets an `escalate` ledger line with the reason and no edit, never a larger fix; on exit 2 cut down or revert the listed sites once and re-run, and if it still exits 2 restore each breaching finding's sites to the `revert_to` text, mark it escalated and re-run; exit 0 ends the revision; on exit 1 or 3 edit nothing further and report the checker output; the checker's report gives the byte size before and after.
```

Budget numbers are deliberately not in the command: the checker prints them (preflight) and its constants are the only source, so the command cannot drift from the script. Bullet 7 (Precedence) already forbids a coordinator brief from widening the reviser's scope ("apply all confirmed findings"); the checker now makes that hold.

### 4.2 `fixcheck.py` outline (stdlib only: `argparse`, `difflib`, `json`, `re`, `pathlib`, `sys`)

```text
CLASSES = {  # the only source of the budget numbers; SKILL.md table pinned equal by test
  "B": dict(added=40,  net=30,  sites=2, sentences=1, normative=1, conditions=1, ids=0, headings=0),
  "C": dict(added=80,  net=60,  sites=3, sentences=2, normative=2, conditions=2, ids=0, headings=0),
  "L": dict(added=150, net=120, sites=4, sentences=4, normative=3, conditions=3, ids=1, headings=0),
}
MAX_L = 1
NORMATIVE = r"\b(MUST|SHALL|must|shall|never|Never|always|Always|required|forbidden)\b"
CONDITION = r"\b(if|If|unless|Unless|when|When|whenever|except|otherwise|Otherwise)\b"
NEW_ID    = r"\b[A-Z][A-Z0-9]*-[A-Z]?\d+(?:\.\d+)*\b"   # plus every id named in fix-budget:

units(text)        # per non-blank line: split table rows at " | ", then sentences at (?<=[.!?;])\s+;
                   # whitespace-normalised; same unitiser as the section 1 calibration
parse_report(p)    # -> reviewed-copy path, {id: class}, {id: reason}; InputError (exit 3) on any rule in 2.5
parse_ledger(p)    # JSON lines; missing file = no entries; bad JSON -> ledger_errors
sites(base, rev)   # SequenceMatcher over units (autojunk=False); one site per non-equal opcode;
                   # per site: old/new text, words added/removed (word-level opcodes inside),
                   # new sentences, normative/condition/new-id counts in added words,
                   # single-token substitution pair (for the rename rule)
                   # headings: new lines starting "#" via a line-level multiset diff
attribute(sites, entries)
                   # entry matches a site if normalised new (or old, for a deletion) is a
                   # substring of the site's new (old) text or the reverse; a site matched by k
                   # ids splits its words evenly; no match -> unattributed
                   # entry checks: old found in baseline, new found in revised, id listed or
                   # escalate-only, why_not_narrow present when the site adds net words
judge(findings)    # compare each finding to CLASSES[class]; unlisted id with any site -> breach;
                   # identical substitution pairs across one finding's sites count as one site
main(argv)         # --report, --revised, optional --baseline/--ledger/--out (for adopters);
                   # writes <report stem>-fixcheck.json; prints summary + one line per breach;
                   # with zero sites prints each listed finding's limits and the ledger line format;
                   # exit 0 pass, 2 breach, 3 input error (1 is left to uncaught exceptions)
```

Expected size about 200 lines. S1 has 1,124 sentence units in the draft and 1,525 in the largest revision (ctl-r2 v3); the unit-level `SequenceMatcher` took 3 ms on that pair in the calibration run, so a checker run is dominated by `uv` start-up (under a second; the full script's runtime is UNVERIFIED until test 4 times it).

### 4.3 `fix-budget/SKILL.md` (about 30 lines)

Frontmatter `name: fix-budget`, description "Per-finding fix budget checker for review -> fix loops (used by /sc:spec-panel-minfix): compares the reviewed copy, the revised file and a ledger; exit 0 pass, 2 breach, 3 input error." Body: the run line; the three report lines a caller writes (`reviewed-copy:`, `fix-budget:`, `fix-budget-override:`); the ledger line format; the class table of section 2.4; the exit-code table of section 2.5. No `src/superclaude` path.

### 4.4 Tests

`tests/skills/test_fixcheck.py` (behaviour, loads the script with `importlib.util.spec_from_file_location` and calls `main(argv)` on files in `tmp_path`):

| case | expect |
|---|---|
| no edits, valid report | exit 0; stdout lists each finding's limits and the ledger format |
| one `B` fix of 30 words in 2 sites, ledgered | exit 0; JSON per-finding counts exact |
| edit ledgered to a minor id | exit 2, metric `unlisted-id` |
| edit with no ledger line | exit 2, `unattributed`, `revert_to` equals the baseline sentence |
| `B` fix with 3 sites; same fix as a 3-site rename | exit 2 / exit 0 |
| new `### ` heading; new `WC-12` id; finding id written into the spec | exit 2 each |
| `old` quote not in baseline | exit 2, `old-not-in-baseline` |
| net-add site without `why_not_narrow` | exit 2, `add-without-reason` |
| escalate-only finding, no edit | exit 0, `escalated: true` |
| two `L`; `L` without override; no `fix-budget:` line; missing copy | exit 3 each |
| whitespace-only change | exit 0, zero sites |
| S1-sized input (generated 1,500 units) | finishes under 5 s |

`tests/skills/test_spec_panel_minfix.py` (static):
- **Derivation pin**: build the expected variant from `src/superclaude/commands/spec-panel.md` by the five region rules of 4.1 (literal bullet constants in the test) and assert byte equality with the variant. Any later edit to `spec-panel.md` fails this test until the variant is regenerated, so the copy cannot drift silently.
- Seven one-line bullets in 427's order (imports `BULLET_NAMES` from `tests/skills/test_spec_panel_review_loop.py`); bullet 4 still contains `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]`.
- `$HOME/.claude/skills/fix-budget/scripts/fixcheck.py` appears before `.claude/skills/fix-budget/scripts/fixcheck.py`; no `src/superclaude` in the section.
- The SKILL.md class table equals `fixcheck.CLASSES`.

Keep green (run, not edit): `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_review_severity_rule.py` (scans every command file: the new text avoids its banned phrases and the old-cap regex), `tests/skills/test_worker_contract.py`, `tests/skills/test_model_alias_policy.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/unit/test_cli_install.py`, then the full `uv run pytest`. Whether any other test requires a `plugins/superclaude/commands/` mirror of every `src` command is UNVERIFIED; the variant is not mirrored to the plugin until promotion.

Sync: `make sync-dev`, `make verify-sync`; stage `src/`, `tests/`, never `.claude/`.

### 4.5 Later adopters (assessment, not part of this change)

The checker contract is document-agnostic: any loop that writes `reviewed-copy:` and `fix-budget:` lines in its report and has a reviser write the ledger can call it.
- **rf-qa Fix Cycle** (`src/superclaude/agents/rf-qa.md:379-416`): good fit; rf-qa fixes prose documents in place under a 2-cycle cap. Adoption is two report lines and one checker call after its fix step.
- **`/sc:reflect`**: weak fit; reflect audits and hands remediation to `/sc:workflow`, it has no reviser step of its own. Adopt only where a reflect loop revises a document.
- **`/sc:implement` final review**: the ledger and budget-line contract transfer, the metrics do not: code needs hunks, changed lines and new public symbols instead of sentences, headings and normative words. That is a second unitiser, out of scope.
Promotion of minfix itself = fold bullets 2, 5 and 6 into `spec-panel.md` (both copies), update 427's T5 vocabulary pin only if a pinned literal moves (`Reviser brief` and `byte size before and after` stay), add a one-line note under `docs/designs/spec-panel-review-loop.md` section 5 that the size limit it rejected is now checked by script, then delete the variant.

## 5. Variant command name and install note

**Name.** File `spec-panel-minfix.md`, invoked as `/sc:spec-panel-minfix`. Skill folder `fix-budget` (not `sc-`-prefixed; reason in section 4, "Why a skill folder").

**Install for the experiment (additive, two paths, nothing overwritten).** From the checkout that holds the implemented change, after checking that neither target exists:

```bash
test ! -e ~/.claude/commands/sc/spec-panel-minfix.md && test ! -e ~/.claude/skills/fix-budget
cp -p src/superclaude/commands/spec-panel-minfix.md ~/.claude/commands/sc/spec-panel-minfix.md
cp -rp src/superclaude/skills/fix-budget ~/.claude/skills/fix-budget
```

No `superclaude install` (it would touch every installed file, and skips existing ones without `--force`). `~/.claude/commands/sc/spec-panel.md` is not edited. The install watcher records the sha256 of all three files (the original, the variant, `fixcheck.py`) for the whole arm; a change mid-arm voids it (V6 as in D10).

**How the checker reaches a worker on repo base 2cb683f5.** That base has neither file and does not need them. The worker loads `/sc:spec-panel-minfix` from `~/.claude/commands/sc/` (D9: the user copy is the one a worker loads). The reviewer writes the `check:` line with `$HOME/.claude/skills/fix-budget/scripts/fixcheck.py`; `uv run --no-project python` runs it with no project, no package and no dependency, in any worktree. The project fallback `.claude/skills/fix-budget/...` is for dev checkouts after `make sync-dev` and is simply absent at 2cb683f5.

**The one-line brief substitution.** Same briefs as Arm B (D11: T05, T06, T07-template, T08-template, T09-template, with Arm B's `--re-review ... --baseline ...` flags on the R2 and R3 review invocations), and in every brief:

```bash
sed -E 's#/sc:spec-panel([^-]|$)#/sc:spec-panel-minfix\1#g'
```

It changes every `/sc:spec-panel` not already followed by a hyphen (including at line end) to `/sc:spec-panel-minfix`; in a brief that does not name the command it changes nothing, so it is safe on the revise briefs too. Which brief file carries which invocation was not re-read here (UNVERIFIED); the substitution does not depend on it. The revise briefs need no change: the reviser reads the report, and the report carries the budget lines and the `check:` command.

**Parallel runs.** Because the variant has its own command name and the checker its own folder, a minfix arm can run while other teams' variants are installed (the D9/AB-REPORT lesson). Other variants must not reuse the folder name `fix-budget`. Keep `~/.claude/WORKER-CONTRACT.md` moved aside as in D10/D11: the spec under review is about that file.

**Side effect while installed.** `fix-budget` appears in every session's skill list on the machine (one description line). **Rollback:** `rm ~/.claude/commands/sc/spec-panel-minfix.md` and `rm -r ~/.claude/skills/fix-budget`.

## 6. Measurement plan and predicted numbers

**Arm MFX.** Scenario S1, repo base 2cb683f5 with the D4a overlay, model claude-opus-5-5, same worker setup, Arm B briefs (with `--re-review/--baseline` on R2 and R3) plus the substitution of section 5, `~/.claude/WORKER-CONTRACT.md` moved aside, two replicates in fresh worktrees `exp346-ab-mfx-r1` and `exp346-ab-mfx-r2`. The `--re-review` flags are required: the re-review checker run (step 8) and the changed-lines scope that turns fewer sites into a smaller surface both live in the re-review.

**Comparators.** Primary, for the pre-registered bar: control ctl-r1/ctl-r2 (D10, reused; time separation stated as in D11). Secondary, to isolate minfix from 427 plus flags: Arm B flg-r1/flg-r2. If budget allows, one concurrent Arm B replicate removes the time-separation caveat (optional).

**Metrics.** D5 M1-M5 unchanged (rounds to clean pass, critical+major proxy per round, `origin=changed` share from 427 tags, size per round and growth, tool calls per round), counted the same way as the A/B recorders. Added:

| id | metric | source |
|---|---|---|
| M6 | checker exit per run and runs per cycle (reviser), and the re-review's `fixcheck:` summary | `*-fixcheck.json`, report headers, session logs |
| M7 | words added/removed, sites, new headings, normative and condition words per cycle | the section 1 unitiser on the spec history copies (same numbers the checker computes) |
| M8 | prior blocking findings `open` (over budget), `open` (escalated), overrides used, per review | report tables, `fix-budget:` lines |
| M9 | review-3 open blocking split: carried from R2 (unfixed or escalated) vs new on cycle-2 sites | R3 prior-blocking table and `origin=` tags |
| M10 | extra tool calls and wall time per step against Arm B | session logs |

**Validity (in addition to D10 V1-V6).** V-M1: R1 and R2 reports carry `reviewed-copy:`, `fix-budget:` and `check:` lines. V-M2: a ledger and a `fixcheck.json` exist for each cycle. V-M3: R2 and R3 headers carry the re-review's `fixcheck:` line. A replicate that fails one is "variant not honoured" and is re-run, not counted.

**Predicted numbers.**

| quantity | control mean | Arm B mean | MFX prediction |
|---|---|---|---|
| growth after two fix cycles (bytes) | 63.5% | 30.0% | **7%** (range 4-12%); hard ceiling about 16% (every finding at its full class budget plus one `L` per report: at most 870 added words in cycle 1 at 17 blocking findings (2 `C`, 14 `B`, 1 `L`; Arm B's R1 proxy was 16-17), 390 in cycle 2 (6 `B`, 1 `L`), against an 8,148-word draft) |
| words added per cycle | 2,351-3,269 | 955-1,997 | cycle 1: 250-500; cycle 2: 100-250 |
| sites per cycle | 45-69 | 25-68 | cycle 1: 15-25; cycle 2: 6-14 |
| review-3 open critical+major (proxy) | 6.0 (8, 4) | 3.5 (6, 1) | **2.5** (per replicate 1-4): new findings on cycle-2 sites 0-2, plus 1-2 carried blocking findings left open by escalation or under-fixing |
| clean PASS at review 3 | 0 of 2 | 0 of 2 | at least 1 of 2: about 35% (judgment, not computed) |
| escalations per run | - | - | 1-3 over both cycles |
| `origin=changed` share of new findings | not comparable | 89-100% | still high (70-100%): fewer findings, same origin; the share is not the target, the count is |

**The bar, applied honestly to the prediction.** Seed-brief criteria: R3 proxy mean 3 or fewer with every replicate better than every control (so each replicate at 3 or fewer, since ctl-r2 is 4), and growth 44.4% or less. Predicted: growth met with a wide margin (near-certain, it is close to mechanical); R3 met with probability about 45%. The D10/D11 bar also needs (c), effect larger than the larger within-arm spread: control spread is 4, so the MFX mean must be below 2.0 with a smaller spread (for example 1 and 2). At the predicted 2.5 that fails; probability of the full D11 bar about 25-30%. n = 2 per arm is a screen for a large effect only.

**What would mean the idea failed** (fixed now, before any run):
1. **Minimality is not enough.** The checker ended `pass` in both cycles of both replicates (fixes were in budget and attributed) and the R3 proxy is above 3 in either replicate. Then fix size is not what keeps review 3 blocking; drop minfix as a standalone fix and test it only in combination with a verdict-side change (stoprule theme).
2. **The budget converts fix-induced findings into unfixed ones.** Carried open blocking findings at R3 (M9: escalated, over budget or unresolved) are 3 or more in either replicate. The budget is too tight as tuned; no retune inside this run.
3. **Surface is not the driver.** Cycle-2 sites at 14 or fewer, yet 3 or more new critical+major findings on those sites at R3 in either replicate.
4. **Only growth improves.** Growth is met but the R3 proxy is not better than Arm B's mean (3.5). 427 already meets the growth bar, so minfix's extra cost buys nothing; reject it.

Not a test of the idea (re-run instead): V-M1 to V-M3 fail, the checker exits 3 or 1 in any cycle, or growth exceeds the 16% ceiling while the checker reports `pass` (that is a checker bug).

## 7. Risks, costs and what would falsify it

### 7.1 Cost per loop (3 reviews, 2 fix cycles; estimates, UNVERIFIED until M10)

| step | extra tool calls | extra model output |
|---|---|---|
| review 1 | +1 Bash (`cp -p` of the reviewed file) | 4 report lines |
| fix cycle 1 | +1 preflight, +1 or 2 ledger writes, +1 check, 0-2 retry checks and revert Edits | ledger: two quoted sentences per site, about 15-25 sites, roughly 1,000-2,000 output tokens |
| review 2 | +1 checker run, +1 `cp -p`; reads a 5-15 KB JSON | 1 header line, status notes |
| fix cycle 2 | as cycle 1, about 6-14 sites | about 500-1,000 output tokens |
| review 3 | +1 checker run | 1 header line |
| **total** | **about +9 to +15 tool calls, 0 extra sessions, about +5 to +12 min wall time** | ledger writing dominates; the checker itself runs in about a second |

Against that, the reviser writes far less spec text (section 6 predicts 70-85% fewer added words than Arm B), so part of the ledger cost is paid back in the reviser's and reviewers' reading.

### 7.2 Ways the mechanism could make the loop worse

1. **Under-fixing.** A fix cut to 40 words or 2 sites may not close its finding; it stays `open` at the next review, or is escalated. This is the main trade: fewer fix-induced findings for more unfixed ones. Mitigations: class `C` (3 sites), the rename rule, one `L` per report, and a cycle-1 escalation reason the review-2 reviewer can answer by granting `L` in cycle 2. Measured by M9; falsifier 2 in section 6.
2. **Cross-site inconsistency.** Two sites lets a fix change a rule and one dependent check. If a third place (an AC, a table row) still states the old behaviour, review 2 flags it as an `origin=unchanged` finding that quotes the changed line, which 427 bullet 5 grades blocking. This is the likeliest way minfix raises a count. Mitigation: narrow the rule instead of rewriting dependents; `C`/`L` for genuinely cross-cutting fixes.
3. **Gaming the counter.** (a) Attributing a site to another listed finding with spare budget: the checker cannot see meaning; the re-review's prior-blocking table shows each finding's quoted changes, so a mismatch is visible to a reader, not to the script. (b) Packing a mechanism into one long comma-joined sentence: the word and sentence caps bound it. (c) Synonyms for normative or condition words ("has to", "in that case"): the counts are proxies and miss these. (d) Laundering across cycles: not possible, each cycle is measured against its own reviewed copy. (e) Editing the report's `fix-budget:` line before preflight to raise a class: the report is the trust anchor and nothing hashes it (residual; detectable by comparing the report with the reviewer's session log).
4. **Escalations replacing fixes.** A reviser can escalate hard findings to avoid work. The loop then ends in escalation, not PASS. Escalation needs a reason naming the smallest fix found; M8 counts escalations; more than 3 per run is a signal to read.
5. **Checker false positives on legitimate edits.** Ledger quotes that differ by backticks or smart quotes (matching is whitespace-normalised only; each costs a retry), a three-place rename that is not a single-token substitution, or a GAP fill whose behaviour sentence needs two condition words. Each produces exit 2 and one retry; the worst case is a reverted good fix. Before the experiment, a dry run of the checker on one real cycle (flg-r2 cycle 2, 25 sites, its disposition table turned into a ledger by hand) measures the false-breach rate on real edits (planned, not done).
6. **A missing reviewer line stops the cycle.** If the report has no `fix-budget:` or `reviewed-copy:` line, the reviser edits nothing (exit 3). That is worse than 427 for that cycle, by design: falling back to unbudgeted fixing would reopen the loophole. In the experiment it is a validity failure and the replicate is re-run.
7. **Anchoring the re-review.** Reading the checker report (with the reviser's quoted changes) may make a reviewer credit a change as `resolved` too easily. Limited to the prior-blocking table; the new-findings pass does not read it.

### 7.3 What is prose and what is mechanical

| rule | enforcement | residual risk |
|---|---|---|
| no edit for a minor or unlisted finding; no unattributed edit | computed (exit 2) | wrong-id attribution (7.2.3a) |
| per-class limits: words, sites, sentences, headings, ids, normative and condition words | computed | synonyms, dense sentences |
| at most one `L`, with a reason line | computed (exit 3) | the reason's quality |
| `L` never for an `origin=changed` finding | prose (reviewer) | reviewer ignores it; at most one per report limits the damage |
| reviser runs the checker and obeys exit 2 | prose, backstopped by the re-review's own run | one review spent on an over-budget fix that is then not credited |
| re-review marks over-budget findings `open` | prose reading a computed report | reviewer ignores the report; visible in M8 |
| `why_not_narrow` and `escalate` reasons are true | presence computed, content prose | plausible-sounding reasons |
| reviewer's copy is the file it reviewed | `cp -p` by the reviewer; the checker's preflight shows zero sites when it is | a copy taken after someone edited the spec |

Falsification criteria are fixed in section 6 ("What would mean the idea failed").

## 8. Open questions

1. **Budget numbers.** `B` 40 words / 2 sites and `C` 80 / 3 are calibrated on one scenario and five 427-arm cycles. A second scenario (rf-qa or a PRD loop) is needed before treating them as defaults. Relative budgets (a share of the cited span) were rejected here because the span a finding cites is often a whole paragraph-line, which would make the budget large exactly where fixes grow.
2. **Should unattributed sites be blocking at the re-review?** This variant reviews them like other changed lines and only counts them. Making each one a blocking `U<n>` finding (remedy: restore the baseline text) gives the rule teeth when a reviser skips the checker, at the price of process-only FAILs. Decide after M6 shows how often revisers skip it.
3. **Who else may grant `L`?** Only the reviewer here. A human coordinator can edit the report's `fix-budget:` line, which the checker cannot tell from forgery. A signed or hashed override is possible but is more machinery than the theme allows.
4. **Does reading the checker report anchor the re-review?** Testable by comparing `resolved` rates against Arm B; not separable at n = 2.
5. **Should the reviewer's own copy replace the coordinator's `--baseline`?** It is exact and needs no coordinator duty, which would remove a 427 failure mode (a dropped or late copy). Out of scope: it changes 427 bullet 1.
6. **Composition with the other themes.** minfix acts on the reviser; stoprule on the verdict; diffgate on the review surface; ledger overlaps (a finding ledger with separate find and verify phases). minfix's ledger is per changed sentence, not per finding, and could feed the ledger theme's verify phase. If falsifier 1 fires, the next test is minfix plus stoprule.
7. **Should `fix-budget` be hidden from the skill list?** It is a script holder, not a model-facing skill. Whether a frontmatter field can keep it out of every session's list is UNVERIFIED.
8. **A code unitiser** (hunks, changed lines, new public symbols) for the `/sc:implement` final review is the obvious second adopter and is not designed here.
