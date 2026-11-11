# Proposal: diffgate for /sc:spec-panel re-reviews (variant 2, refactorer lens)

Issue #346. Additive variant command `spec-panel-diffgate`. Lens: technical debt, simplification, minimal-risk transformation.

## 1. Problem and evidence

**The debt in 427.** PR 427's `## Review Loop` bullet 5 asks a model to do four mechanical jobs in prose: find the changed lines, tag each finding `origin=changed|unchanged`, keep the review count, and say `PASS` or `FAIL`. Bullet 6 asks a second model to touch only text a blocking finding names. Nothing computes or checks any of it (design doc section 12: "Prose only"; section 9: "The tests prove the text is present"). The Arm B reports show the prose is obeyed in form (status table, `origin=` tags, `review: N of 3`) and still does not converge.

**What was measured (S1, 2 replicates per arm; `AB-REPORT.md`, `ARMB-REPORT.md`):**

| Cause | Evidence | Removed by this proposal? |
|---|---|---|
| Fix-induced findings on changed lines | 89% of review-2 and 100% of review-3 new findings are `origin=changed`. In `flg-r2` all six review-2 blockers (N1-N6) and the only review-3 blocker (N12) sit on lines the previous fix changed | **No.** Those lines are in scope by design. The proposal only bounds how many lines a fix may change (the next row) and stops a line being reviewed twice (section 5). It cannot stop a mapped fix from being wrong |
| Revisers add work no blocking finding asked for | `disposition-round2.md`: "Minor findings were applied too"; all 15 rows applied; two extra "related defects" fixed (E5, AC-1.2). Of the 25 spec lines the round-2 revision changed (the `Changed lines` list in `spec-panel-round3.md`), 13 trace to blocking ids N1-N6 and 12 only to minor or citation rows (line 5 carries both an N1 and an N11 id; I counted it with the minor group, UNVERIFIED) | **Yes, mechanically.** A fix hunk with no blocking id in the fix map is rejected (section 5) |
| Severity drift between rounds | 427 grading relabels some MAJOR findings as minor (flg-r1 R3-7, R3-8: proxy 6, blocking 4) | **Partly.** The script derives blocking from fields it can check (`outcome=` present, anchor present, in scope); the reviewer's severity word is still judgement |
| Re-review re-attacks the whole document | Review 3 of `flg-r2` spends Part 1 (15 rows) and Part 2 (20 citation groups) before Part 3; the reviewer derived its own `git diff --no-index -w` and judged its own scope | **Yes.** The surface is computed; a finding that anchors to nothing is deferred (sections 3, 4, 6) |
| Nothing mechanical stops the loop or checks the count | The count lives in a header the coordinator must carry; "a coordinator that drops the flags starts a fresh first review" | **Yes.** The count and the order of steps live in a ledger file; `begin` refuses out-of-order steps and a fourth review |

**Retrofit evidence for the gate (one real case).** Replaying the fix-map gate over the round-2 revision of `flg-r2`: of the five review-3 items (N12, N13, N14, N15, C-R3-15), N14 (line 62, from the minor row N9) and C-R3-15 (line 11, a citation row) sit on minor-only lines and would not exist; N15 is `origin=unchanged` and would be deferred; N12 (lines 60 and 220, from the N5 fix) and N13 (line 223, from the N3 related fix) stay. Total 5 to 2, blocking 1 to 1. Honest reading: the gate removes noise and growth and leaves the induced blocker that a mapped fix produced. Only one replicate's reports were read; the `flg-r1` composition is UNVERIFIED (its folder was not in the evidence given).

**What stays unfixed (said up front).** If the real cause is that a correct-looking fix to a blocking finding creates a new defect at a rate near 0.2 to 0.5 per mapped fix (round 2: six induced blockers from thirteen round-1 blocking fixes; round 3: one from six), then no scope rule reaches PASS in three reviews on a spec this size. Diffgate bounds that and makes it measurable; it does not remove it. Section 9 states which result would say so.

## 2. Mechanism: the loop step by step

Notation. `DG` = `uv run --no-project python ~/.claude/skills/sc-diffgate-protocol/scripts/diffgate.py` (else the project copy `.claude/skills/sc-diffgate-protocol/scripts/diffgate.py`; skills resolve home first, per the project CLAUDE.md). `<dir>` = the loop directory, `--diffgate-dir <dir>` (under `--unattended` it defaults to `<report-dir>/diffgate`). `<spec>` = the document under review. The loop has two kinds of worker (reviewer, reviser) and one coordinator (an Orca coordinator or a human). The script is run by the worker that owns the step; it never edits `<spec>`.

**Files in `<dir>`** (all written by the script unless the owner says otherwise):

| File | Owner | Content |
|---|---|---|
| `ledger.json` | script | the only state: per round the doc sha, hunks, priors, accepted check, accepted fixcheck; the deferred list; flags `degraded` and `closed` |
| `doc-r<N>.md` | script (`begin`) | byte copy of `<spec>` as review N saw it; baseline for review N+1 |
| `surface-r<N>.md` | script (`begin`, N>=2) | the review surface: diff hunks with ids and section names, then the prior blocking findings with ids and anchors |
| `<report>` | reviewer | the review report (path given by `--output` or `<report-dir>`); holds a `## Diffgate findings` block of machine lines |
| `result-r<N>.json` | script (`check`) | accepted findings with computed `origin`, blocking flag, deferral reason, prior-status rows, derived verdict |
| `reject-r<N>.txt` | script (`check`) | rejection reasons, one per line; deleted on acceptance |
| `reviser-brief-r<N>.md` | script (`check`, FAIL and N<3) | the blocking ids with anchors and outcomes, and the fix-map rules; the reviser's only task list |
| `fixmap-r<N>.txt` | reviser | one line per fix hunk: `H<i> R<N>.<j>`; `declined R<N>.<j> <reason>` for a finding it will not fix |
| `deferred.md` | script (`check`) | cumulative list of findings recorded `deferred: pre-existing` or `deferred: unanchored`; never read by a reviser |

**Steps, in order:**

| # | Step | Who | Command / action | Reads | Writes |
|---|---|---|---|---|---|
| 1 | Review 1 starts | coordinator | dispatches `/sc:spec-panel-diffgate @<spec> --mode critique ... --diffgate-dir <dir>` | brief | none |
| 2 | Open the loop | reviewer command | `DG begin --dir <dir> --doc <spec>`; prints `review: 1 of 3`, `mode: full` | `<spec>` | `ledger.json`, `doc-r1.md` |
| 3 | Review 1 | reviewer | today's full-document review; adds `FINDING` lines (grammar in section 4) and ends with `verdict:` | `<spec>` | report |
| 4 | Check 1 | reviewer command | `DG check --dir <dir> --report <report>`; on exit 1 the reviewer repairs the report once and reruns | report, `ledger.json`, `doc-r1.md` | `result-r1.json`, `reviser-brief-r1.md` if FAIL, `deferred.md`, or `reject-r1.txt` |
| 5 | Fix cycle 1 | reviser | reads `reviser-brief-r1.md` (not the whole report); edits `<spec>`; writes `fixmap-r1.txt`; runs `DG fixcheck --dir <dir> --doc <spec>` until exit 0 (at most 3 runs, then stops and says so) | brief, `<spec>`, `doc-r1.md` | `<spec>`, `fixmap-r1.txt`, ledger fix record |
| 6 | Review 2 starts | coordinator | same brief as step 1 | | |
| 7 | Open review 2 | reviewer command | `DG begin ...`; refuses (exit 5) unless fixcheck 1 is accepted for the current doc sha; computes the delta; prints `review: 2 of 3`, `mode: delta`, hunk and prior counts | `<spec>`, `doc-r1.md`, `result-r1.json`, ledger | `surface-r2.md`, `doc-r2.md`, ledger |
| 8 | Review 2 | reviewer | reads `surface-r2.md` and, as read-only context, `<spec>`; writes a `PRIOR` row per prior blocking id and `FINDING` lines; no whole-document pass | `surface-r2.md`, `<spec>` | report |
| 9 | Check 2 | reviewer command | as step 4 | | `result-r2.json`, brief, `deferred.md` |
| 10 | Fix cycle 2 | reviser | as step 5, with `reviser-brief-r2.md`, baseline `doc-r2.md` | | `<spec>`, `fixmap-r2.txt` |
| 11 | Review 3 | coordinator, reviewer | as steps 6 to 9; `review: 3 of 3`; baseline `doc-r2.md` | | `result-r3.json`, `deferred.md`; no reviser brief |
| 12 | End | reviewer command, coordinator | after check 3 the command prints the derived verdict, the open blocking ids with their fix chains, and `deferred.md` once; FAIL says `halt: escalate`; the coordinator escalates to the user. A later `begin` exits 4 | `result-r3.json`, `deferred.md` | none |

Early exit. If `check` derives `PASS` at review 1 or 2, the ledger is `closed`, no reviser brief is written, the command prints `deferred.md` once, and a later `begin` exits 4 with `halt: pass`.

**Where a model could skip a step, and what then happens** (the lock points; the aim is that skipping is loud, not that skipping is impossible):

- Reviewer skips `begin`: it has no `surface-r<N>.md`, and the command text says to stop without one; if it reviews anyway, `check` exits 5 (no round open).
- Reviewer skips `check`: no `result-rN.json`, so no `reviser-brief-rN.md`; the reviser's step 5 starts with "if the brief is missing, run `check` first", and `fixcheck` exits 5 without an accepted check.
- Reviser skips `fixcheck`: `begin` for the next review exits 5. The loop stops visibly instead of reviewing an unchecked edit.
- Anyone edits `<spec>` after `fixcheck`: the doc sha differs, `begin` exits 5.
- The coordinator drops `--diffgate-dir`: the variant refuses `--mode critique` without it (it is the variant's only reason to exist), so the failure is loud, not a silent fresh review as in 427.
- The coordinator points a later review at a fresh or wrong directory: that starts as `review: 1 of 3`. The brief can pass `--expect-round N` through to `begin`, which exits 5 when the ledger-derived round differs. The S1 briefs use one directory throughout and pass `--expect-round`. Residual risk: a coordinator that omits it (section 10, R9).

## 3. Who computes the diff, and the script interface

**Decision: a Python stdlib script shipped in a skill folder, run by the worker that owns each step. Not a fixed command sequence.**

Why not `git diff --no-index -w` as a fixed sequence (what the Arm B reviewer ran by hand): it yields a diff but not stable hunk ids, section names, a reflow filter, an anchor Read-back, a ledger or a lock between steps. Every one of those would again be a sentence a model is asked to obey. Why not "the coordinator runs it": an Orca coordinator or a human is also a prose follower, and the reviewer cannot wait on it. Placement is solved by locks instead (section 2): each step's output is the next step's only input, so a skipped step stops the loop.

Host skill: `sc-diffgate-protocol` (needs a `SKILL.md` for `install_skills.py` to install it; verified at `install_skills.py:167-170` and `Makefile` `sync-dev`, which copies every file of a skill folder except `__init__.py`). Script: `scripts/diffgate.py`, Python 3.10+, stdlib only (`argparse`, `difflib`, `hashlib`, `json`, `os`, `pathlib`, `re`, `sys`); `difflib` is already used in `src/superclaude/cli/eval/expect.py:33`. Output is plain `key: value` lines on stdout so a model reads it without parsing JSON.

**Subcommands**

| Subcommand | Inputs | Writes | Stdout (success) |
|---|---|---|---|
| `begin --dir D --doc F [--expect-round N]` | spec `F`, loop dir `D` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N>=2) | `review: N of 3`, `mode: full\|delta`, `surface: <path>`, `hunks: n`, `ignored: n`, `coverage: n%`, `priors: n` |
| `check --dir D --report R` | review report `R` | `result-r<N>.json`, `reviser-brief-r<N>.md`, `deferred.md`; or `reject-r<N>.txt` | `accepted: yes`, `verdict: PASS\|FAIL`, `blocking: <ids>`, `deferred: n`, `degraded: yes\|no`, plus at the last review `halt: escalate` |
| `fixcheck --dir D --doc F [--map M]` | spec after the fix; map defaults to `D/fixmap-r<N>.txt` | ledger fix record | `fix: accepted`, `hunks: n`, `mapped: n`, `declined: n`, `added_bytes: <per id>`; on exit 1 the unmapped hunks with their lines |
| `status --dir D` | ledger | nothing | `round`, `state` (one of `open`, `checked`, `fixed`, `closed`), `next:` the one command that should run next |

**Exit codes** (all subcommands; the model must act on the code, so each has one meaning):

| Code | Meaning | Who acts |
|---|---|---|
| 0 | done | continue |
| 1 | the input was rejected (`check`: bad report; `fixcheck`: unmapped or unknown hunks); reasons on stdout and in `reject-r<N>.txt` | the caller fixes its own file and reruns, at most twice |
| 2 | usage error | fix the command line |
| 3 | an input file is missing, unreadable or empty (427 bullet 1: "stop and say which") | stop, say which |
| 4 | the loop is closed: `halt: pass` or `halt: escalate` (cap reached, or a fourth review requested) | stop, report |
| 5 | steps out of order: no open round, no accepted check or fixcheck for the current doc sha, or `--expect-round` differs | run the step `next:` names |
| 6 | the ledger is corrupt or does not parse | stop, escalate to the user (the script never repairs it) |

**Diff computation (deterministic; the same code serves `begin` and `fixcheck`).**

1. `old` = lines of `doc-r<N-1>.md`; `new` = lines of the spec. A line's comparison key is `" ".join(line.split())` (whitespace collapse, so indentation and trailing space never count).
2. `difflib.SequenceMatcher(None, keys_old, keys_new, autojunk=False)`. `autojunk=False` matters: the default heuristic switches on at 200 lines and the S1 spec has about 317, so without it popular lines (table separators, blank lines) are junked and the diff degrades.
3. Each non-`equal` opcode is a candidate hunk. Drop it when `" ".join(old_part).split() == " ".join(new_part).split()` (whitespace, blank-line and re-wrap only; this is the reflow filter). Count it under `ignored`.
4. Merge candidate hunks whose new-side gap is 2 lines or less (`MERGE_GAP = 2`), so one logical edit that touches a line and the line after the blank is one hunk.
5. Number the surviving hunks `H1`, `H2` in document order. The reviewable range of a hunk is its new lines; for a pure deletion it is the line before and the line after the deletion point (so a deleted requirement can still be anchored). `section` = the nearest Markdown headings above the range, joined with `>`.
6. Because the fix cycle's diff and the next review's diff are the same two files (`doc-r<N>.md` and the spec, sha-locked), **hunk ids in `fixmap-r<N>.txt` and in `surface-r<N+1>.md` are the same ids.** The surface can therefore print "H2 = the fix for R1.3".

**Surface file (`surface-r2.md`), format and example**

```text
# diffgate surface: review 2 of 3
doc: specs/orca-worker-contract-spec.md   doc_sha: 3f9a1c20d4be   baseline_sha: 91be07a5c3d2 (doc-r1.md)
hunks: 7   ignored (whitespace or re-wrap only): 2   merge_gap: 2   coverage: 9% of lines
Rule: a new finding must cite one of the hunks below (hunk=H<i>, at= inside it) or a prior id under "Prior blocking findings". Anything else is recorded "deferred: pre-existing".

## H2   new lines 60-60 (old 58-58)   section: 2. Worker rules > WC-1   fixes: R1.5
ctx  59: <unchanged line, read-only>
-    58: <old text>
+    60: <new text>
ctx  61: <unchanged line, read-only>

## H3   ...

# Prior blocking findings (from result-r1.json)
R1.5  sev=major  at=60 (was 58)  anchor_untouched: no   fix hunks: H2
  anchor: [[WC-1 ... session-name question]]
  outcome: [[a vacuous pass is recorded for WC-1]]
R1.9  sev=critical  at=66  anchor_untouched: yes (no fix hunk touches it; cannot be marked resolved)
```

**Ledger (`ledger.json`) sketch** (written atomically: temp file, then `os.replace`):

```json
{"version": 1, "doc": "specs/x.md", "closed": null, "degraded": false,
 "rounds": {"1": {"doc_sha": "91be...", "snapshot": "doc-r1.md",
                  "check": {"accepted": true, "verdict": "FAIL", "report_sha": "...", "blocking": ["R1.5", "R1.9"]},
                  "fix":   {"accepted": true, "doc_sha": "3f9a...", "map": {"H2": "R1.5"}, "declined": {"R1.4": "evidence does not hold"}, "added_bytes": {"R1.5": 410}}},
            "2": {"doc_sha": "3f9a...", "surface": {"hunks": [{"id": "H2", "new": [60, 60], "old": [58, 58], "section": "..."}], "ignored": 2}, "check": null, "fix": null}},
 "deferred": [{"round": 2, "id": "R2.7", "at": 211, "reason": "pre-existing", "anchor": "..."}]}
```

The ledger holds hashes and ranges, not document text, except the short anchors it needs to print the deferred list.

## 4. The checker

**Model (borrowed from `sc-implement-protocol/refs/qa.md`): the reviewer proposes, the script derives.** In `qa.md` the reviewer writes `at=`, `anchor=`, the parent Reads the anchor back, writes `origin=` and derives the verdict ("nobody rewrites a recorded verdict"). Diffgate does the same for a document: the reviewer writes anchors, the script reads them back against the saved snapshot, computes `origin`, decides in scope or deferred, and derives `blocking` and `verdict`. The reviewer's prose (experts, guard table, adversarial analysis) is untouched; the contract is one machine block in the report.

**Report block (ASCII, one line per item, a line starts with its keyword at column 1):**

```text
review: 2 of 3                                   (427 literal, kept; must equal the ledger round)
PRIOR R1.5 resolved
PRIOR R1.9 open :: fix hunk H4 still lets WC-7 skip the command file
FINDING R2.1 sev=major at=60-63 hunk=H2 anchor=[[appears in that worker's worker-read output]] outcome=[[correct launcher runs are recorded as WC-1 not exercised]] :: AC-0.4 reads the wrong source
FINDING R2.2 sev=minor at=223 hunk=H6 anchor=[[--output <dir> by default]] :: index-repo has no such flag
FINDING R2.3 sev=major at=312 via=H3 via_quote=[[7.2 step 1 --worktree current]] anchor=[[places the worker in the current worktree]] outcome=[[...]] :: H3 now assumes an own worktree
FINDING R2.4 sev=minor at=140 cites=R1.9 anchor=[[...]] :: more evidence for R1.9
verdict: FAIL                                    (427 literal: last line)
```

Keys: `sev` (`critical|major|minor`), `at` (line or range in the snapshot the reviewer read, `doc-r<N>.md`), `hunk` (a surface hunk), `via` + `via_quote` (an unchanged line broken by a changed hunk), `cites` (a prior id), `fr` (`8|9|10`, kept from 427's Guard Condition Boundary Table rule), `anchor` and `outcome` (verbatim text between `[[` and `]]`), then `::` and a short text. Finding ids are `R<round>.<j>` with `j` counting from 1 with no gap; the script owns the format so ids never collide across rounds.

**Rules, in the order the script applies them.** "Hard" = the report is rejected (exit 1). "Soft" = the script fixes it by itself and records it in `result-r<N>.json`.

| # | Rule | Kind | On violation |
|---|---|---|---|
| C1 | The report has `review: N of 3` equal to the ledger round, a last non-blank line `verdict: PASS\|FAIL`, and either FINDING lines or the single line `FINDINGS none` | hard | `E-ROUND`, `E-FORMAT` |
| C2 | Every `FINDING` and `PRIOR` line parses; no unknown key; ids are `R<N>.<j>` contiguous | hard | `E-FORMAT` |
| C2b | Every `R<N>.<j>` token anywhere in the report (prose included) is the id of a `FINDING` line, so a finding written only in prose cannot slip past the reviser's list | hard | `E-FORMAT` |
| C3 | The spec's sha equals the sha `begin` recorded (nobody edited the spec during the review) | hard | exit 5 |
| C4 | `at` lies inside the snapshot (1..number of lines) | hard | `E-AT` |
| C5 | **Anchor Read-back**: the whitespace-collapsed `anchor` (12 to 200 characters) is a substring of the whitespace-collapsed text of the lines `at` names | hard | `E-ANCHOR` |
| C6 | `hunk=H<i>` names a hunk of this round's surface and `at` lies inside that hunk's reviewable range; in review 1 there is no surface and `hunk`, `via` are not allowed | hard | `E-HUNK` |
| C7 | `via=H<i>` names a surface hunk and `via_quote` is a substring of that hunk's new text | hard | `E-VIA` |
| C8 | `cites=` names a prior blocking id in the ledger (or an earlier finding id of the same report) | hard | `E-CITES` |
| C9 | The `PRIOR` rows are exactly the ledger's prior blocking ids, once each; `regressed` is allowed only for an id an earlier round marked `resolved` | hard | `E-PRIOR` |
| C10 | A `PRIOR ... resolved` whose anchor line no fix hunk touched (`anchor_untouched: yes` in the surface) is set to `open` | soft | `overridden: untouched` |
| C11 | Scope (review >= 2): a finding is in scope iff it has a valid `hunk=`, or a valid `via=` (at most 2 per review). Else if it has a valid `cites=` it is attached to that prior id as evidence and adds no blocking count. Else it is recorded `deferred: pre-existing` | soft | `deferred` |
| C12 | Blocking: an in-scope finding is blocking iff `sev=critical`, or `fr` is 8 or 9, or `sev=major` with an `outcome` of at least 25 characters; otherwise it is minor (427 grading, bullet 2, made checkable) | soft | `downgraded: no-outcome` |
| C13 | Verdict: `FAIL` iff any in-scope blocking finding or any prior with `open` or `regressed` exists; else `PASS`. The report's `verdict:` line must equal it | hard once, then derived wins | `E-VERDICT` |

**Origin is computed, never typed.** `origin=changed` when C11 accepts the finding through `hunk=`; `origin=unchanged` for `via`, `cites` and deferred findings. The reviewer no longer writes `origin=`. The 427 vocabulary (`origin=changed|unchanged`, `resolved|open|regressed`) is kept in `result-r<N>.json` and in the command text.

**What happens on a reject (one answer, three tiers).**

1. Citing neither a hunk nor a prior id is not a reject. It is a normal soft outcome: the finding goes to `deferred.md` (rule C11) and can never be blocking after review 1.
2. A hard violation (C1 to C9, C13): `check` exits 1, writes `reject-r<N>.txt` with one line per violation (`E-ANCHOR R2.3: anchor text not found on lines 211-212`) and changes nothing else. The reviewer repairs only those lines in the same session and reruns `check` once. That costs one tool call and no new session.
3. Still hard violations on the rerun: the script does not fail the run and does not loop. It degrades fail-safe and says so: a finding-level violation (C2, C4 to C8) moves that finding to `deferred: unanchored`; a missing `PRIOR` row counts as `open`; the derived verdict replaces the report's. `degraded: yes` is written to the ledger, printed by `check`, and repeated in the end-of-loop summary. Fail-safe means a lazy report can add an `open` prior (a spurious blocker) but can never smuggle in an unanchored blocker.

**What the checker proves, and what it does not.** It proves the reviewer's findings point at text that exists, inside a region the script computed, and that the counts and the verdict follow from those pointers. It does not prove the finding is true, that the `outcome` sentence is a real wrong outcome (only that it is present and long enough), or that a `resolved` mark is correct (only that a fix hunk touched the anchor). Those stay judgement, with the residual risks listed in sections 7 and 10.

## 5. Convergence rule for fix-induced defects on changed lines

Fix-induced defects on changed lines are in scope: a fix that breaks something must be caught. The design does not hide them. It makes four things true so they cannot regenerate without limit.

**5.1 Reviewed once, by construction (no rule to obey).** Review N+1's surface is the diff between the document review N saw (`doc-r<N>.md`) and the document after fix N. So:

| Line state | Where it can be reviewed |
|---|---|
| changed by fix N | review N+1 only |
| unchanged since the document review N saw | never again, unless a later fix changes it (then in that later review only) |
| in the original document and never changed | review 1 only; a defect found later is `deferred: pre-existing` (section 6) |

A defect on a line fix N changed that review N+1 misses is not reopened in review N+2. That is a deliberate loss: it is what stops the loop from re-attacking text it has already judged. Cost of the loss: section 10, R2.

**5.2 The fix gate: one hunk, one blocking id (mechanical).** `fixcheck` runs the same diff as the next `begin`, then reads `fixmap-r<N>.txt` (lines `H<i> R<N>.<j>` and `declined R<N>.<j> <reason>`). It exits 1 unless all hold:

- F1. Every fix hunk is claimed by exactly one id, and that id is a blocking id of the round (a new blocking finding or a prior `open|regressed`). A hunk that fixes a minor finding, a citation note or a "related defect" has no valid id, so it is rejected. The reviser reverts it by hand, or maps it to the blocking id it genuinely repairs (a root cause that appears in several places is several hunks mapped to one id, so the 427 "root cause once, in every section that states the rule" practice stays allowed).
- F2. Every blocking id has at least one hunk or a `declined` line with a reason. A declined or untouched id stays `open` and is printed on the next surface.
- F3. Ids and hunk ids exist; a hunk is not claimed twice.

On exit 0 the script records, per id, the bytes the fix added, and prints `over_budget: R1.5 (2210 > 1500)` when a fix exceeds `FIX_BUDGET_BYTES = 1500`. The budget is advisory, not a gate (a hard gate would push revisers to under-fix and leave the blocker open). It is recorded on the next surface header so the reviewer looks harder at the largest fix. The 1500 comes from the S1 data: round-1 growth of 21.6% on a 57.7 KB spec is about 12.5 KB for 13 blockers, about 960 bytes each; 1500 is about 1.5 times that (calibration UNVERIFIED, see section 12). A hunk that adds a Markdown heading is printed as `new_section: H4`, because 427 bullet 6 forbids a section no blocking finding calls for (warning only).

This removes cause 3 of section 1. The reviser's task list is `reviser-brief-r<N>.md`, which holds only blocking ids, so minors never reach it.

**5.3 Chains are recorded, so a regenerating defect is visible.** The surface prints `fixes: R1.5` on the hunk that repaired R1.5. A review-2 finding anchored in that hunk is stored as a child: `chain: R1.5 -> R2.1`. A review-3 finding on a fix-2 hunk extends it: `R1.5 -> R2.1 -> R3.2`. The end-of-loop summary prints every chain. A chain of length 3 is the signature of a defect that automatic fixes cannot close; the summary then says "revise this region by hand" instead of "run another cycle". This is reporting, not a stop rule, and is cheap (`fixes` is already in the ledger).

**5.4 What stops regeneration (the honest list).**

1. The cap, unchanged and pinned: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (`tests/skills/test_review_severity_rule.py:215`). `begin` enforces it (exit 4 for a fourth review).
2. The surface shrinks with the fix. Review N+1 can raise a blocker only on the lines fix N changed (plus at most 2 `via` findings). With the fix gate, those lines are at most `blocking ids x budget`, not the whole 76 KB document. In the `flg-r2` replay the round-2 revision changed 25 lines; the gate would have allowed 13.
3. No "exposed by" route except `via`, which is capped and logged.
4. No severity ceiling at review 3. I considered "a review-3 finding that cites no prior id cannot be blocking" and rejected it: it would turn the last review into a rubber stamp for exactly the fixes with the least review, and it would improve the measured metric by relabelling rather than by converging. If the fix gate and the surface are not enough, the data should say so (section 9).

**5.5 Not claimed.** Diffgate does not lower the per-fix rate of induced defects. It lowers the number of fixes (cause 3), removes re-review noise (cause 4) and makes the remainder countable.

## 6. Pre-existing defects review 1 missed

**Rule.** In review 1 the whole document is in scope. From review 2 on, a finding that cites no valid hunk, no valid `via` and no prior blocking id is recorded `deferred: pre-existing` by the script (rule C11), is never blocking whatever its `sev` label, and never enters a surface, a reviser brief or a later `PRIOR` table.

**Format (`deferred.md`, written by every `check`, cumulative):**

```text
# diffgate deferred list (not looped on)
loop: <dir>   spec: <spec>   rounds checked: 3   items: 4   degraded: no
D1  round 2  R2.7  sev=major(label)  at=211  reason=pre-existing   seen: rounds 2,3
    anchor: [[AC-C1 regex still matches README.md:216]]
    note:   <the reviewer's :: text>
D2  round 3  R3.5  sev=minor  at=96   reason=unanchored (degraded report)
...
```

**Surfaced once.** `check` prints only a count (`deferred: 2`) while the loop is open, so no worker in the loop reads the text. At the closing review (a derived `PASS`, or review 3) the command prints `deferred.md` in full as the last block of its output, once, under the heading "Deferred, not looped on". The coordinator passes that block to the user together with the open blocking findings. A deferred id is not a legal `cites=` target (rule C8 accepts blocking priors only), so a later reviewer cannot launder a deferred item into a blocker by citing it. The same quote deferred in two rounds is one entry with `seen: rounds 2,3`.

**What the user can do with it.** Fix by hand, or start a new loop with a new `--diffgate-dir`: its review 1 is a full-document review, so those defects return as ordinary first-review findings. That is the only road back in, and it needs a human decision, which is the point.

**What keeps this from blinding the reviewer.** 427's one safety valve is kept in a bounded form: an unchanged line may be raised as a blocker only through `via=H<i>`, where the finding quotes the changed text it depends on and the quote is checked against the hunk (rule C7), at most 2 per review. Everything else about untouched text is deferred, not lost: the full list is shown, with the reviewer's own severity label, so a human can see if the loop is hiding something that matters. Expected size: 89% of review-2 findings were `origin=changed` in the S1 reports, so roughly one in nine findings lands here, about one or two items per review.

**Residual risk (prose, not mechanical).** The reviewer decides whether a defect "depends on" a changed line (`via`); the script checks the quote exists, not that the dependency is real. A reviewer can under-use `via` (miss a real cross-reference regression) or over-use it (the cap of 2 bounds the damage). Section 9 measures it with a blind whole-document audit of the final spec.

## 7. Comparison with PR 427's --re-review and --baseline flags

427 (`## Review Loop` bullets 1 to 7 plus the `--re-review <prior-findings-file> --baseline <saved-copy>` Usage flags) gives a model the rules. Diffgate keeps all seven bullets and their literals and moves the mechanical parts into a script. Arm B (427 plus its own flags) showed the flags are honoured in form (status table, `origin=` tags, `review: N of 3`), so the comparison below is about who computes and who checks, not about wording.

| Concern | 427 with flags | Diffgate | Still prose after diffgate (residual risk) |
|---|---|---|---|
| Saved baseline | The coordinator saves a copy and passes `--baseline`; a dropped flag silently starts a fresh first review | `begin` snapshots the spec to `doc-r<N>.md`; the coordinator carries only the directory | Coordinator may pass a wrong or fresh directory; `--expect-round` catches it only if the brief includes it (R9) |
| The diff | The reviewer runs its own `git diff --no-index -w` and may skip or misread it | Computed once by the script, with hunk ids, section names and a reflow filter; the reviewer reads `surface-r<N>.md` | The reviewer can still read the whole document as context and be influenced by it |
| `origin=` | The reviewer self-tags | Computed from the anchors (rule C11) | None for the tag; the reviewer chooses which hunk to cite |
| Scope of a finding | Bullet 5: an `origin=unchanged` finding is a minor note unless it quotes the changed line it depends on; reviewer judges | A finding with no valid hunk, `via` or prior id is deferred; `via` is quote-checked and capped at 2 | Whether a real dependency exists (judgement) |
| Findings point at real text | Not checked | Anchor Read-back against the snapshot (C5) | A finding can be anchored and wrong |
| Prior-findings table | Reviewer writes `resolved\|open\|regressed` | Rows must equal the ledger's prior set; `resolved` on an untouched anchor is set to `open` (C9, C10) | A fix hunk touched the anchor but did not fix it: `resolved` is still the reviewer's call |
| Blocking and verdict | Reviewer grades and writes the last line | Script derives both from checkable fields; mismatch is rejected once, then the derived value wins (C12, C13) | Whether `outcome` is a true wrong outcome (only presence and length are checked) |
| Review count and cap | A header the coordinator carries; "nothing enforces the count" (design doc section 12) | Ledger round; `begin` exits 4 for a fourth review or after PASS | None for the count; the cap text stays pinned |
| Reviser contract | Bullet 6: "revise only text a blocking finding names", restated in a brief | `fixcheck` rejects any fix hunk without a blocking id; the reviser's task list is script-written (F1 to F3) | The reviser can map an unrelated edit to a blocking id (the map is auditable, not verified), and can skip `fixcheck`, which stops the next `begin` |
| Order of steps | None | Each step's output is the next step's only input; out-of-order calls exit 5 | A coordinator that hand-edits `ledger.json` or the files in `<dir>` |
| Pre-existing defects | Minor note in the report | `deferred.md`, shown once at the end | Deferred severity labels are the reviewer's |
| Re-check of prior blocking findings | rf-qa Fix Cycle steps 1 to 5 followed "first" | Kept as is in bullet 5 of the variant; the script checks only the table's shape | Same as 427 |

**What 427 leaves to prose that this makes mechanical:** the diff, the tag, the baseline copy, the review count, the verdict, the "resolved" sanity check, the reviser's scope, and the step order. **What stays prose:** whether a finding is true, whether a fix is good, whether a `via` dependency is real, whether a coordinator hands over the right directory, and whether any worker obeys the command at all before the first lock point (a reviewer that never runs `begin` is caught only at `check`, a reviser that never runs `fixcheck` only at the next `begin`).

**Net, in lines of prose.** The variant replaces bullet 5's "lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`" with a pointer to the surface file, and adds one `## Diffgate` section of single-line steps. Prose goes down in bullet 5 and 6 and up by the new section; the net rule count the model must obey drops from about eleven judgement duties to three (grade honestly, quote honestly, map honestly). That count is my estimate, not a measurement.

## 8. Exact changes, file by file

Transformation path (minimal risk, each stage independently revertible):

- **Stage A, inert:** add the skill folder, script and script tests. Nothing references them. Revert: delete the folder.
- **Stage B, the experiment arm:** add the variant command, its text tests and the one test-helper exception. `/sc:spec-panel` and the user-level `~/.claude/commands/sc/spec-panel.md` are not touched. Revert: delete the variant file.
- **Stage C, only if the S1 bar is met (a separate PR, not part of this change):** fold the `## Diffgate` section into `spec-panel.md`, delete the `--re-review/--baseline` prose, and retire the variant. Not specified here.

Everything below is Stage A and B. All paths are repo-relative to the checkout; every installed text names installed paths, never `src/superclaude/...` (project CLAUDE.md rule; checked by the grep in the last table row).

### 8.1 New: `src/superclaude/commands/spec-panel-diffgate.md`

A copy of `src/superclaude/commands/spec-panel.md` (486 lines, read in this worktree) made with `sed 's#/sc:spec-panel#/sc:spec-panel-diffgate#g'`, then these edits. Every other line is byte-identical to the original, which keeps drift reviewable with `diff`.

1. Frontmatter line 2 `name: spec-panel` becomes `name: spec-panel-diffgate`; `description:` gains "with a computed re-review surface (diffgate variant)". Title line 11 becomes `# /sc:spec-panel-diffgate - Expert Specification Review Panel (diffgate variant)`.
2. Usage line 22: replace `[--re-review <prior-findings-file> --baseline <saved-copy>]` with `[--diffgate-dir <dir> [--expect-round N]]`. Line 23 only gets the renamed command.
3. `## Review Loop` (line 256): bullets 2, 3 and 7's prefix stay literal. New or changed text (each bullet stays ONE line, like 427, so line-based matchers still see it whole; wrapped here for reading):

```markdown
1. **Mode**: `--diffgate-dir` applies to `--mode critique` only and is required there; `begin` on an empty directory makes the run a first review of the full document and any later `begin` makes it a re-review; if a named file is unreadable or empty (script exit 3), stop and say which, and never fall back to a first review.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the round `begin` prints; a `begin` that exits 4 means do not review, HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--diffgate-dir` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps only the directory; the ledger keeps the count.
5. **Re-review output**: the reviewer reads `surface-r<N>.md` and does not re-review the document; first a `PRIOR` row per prior blocking finding `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again); then `FINDING` lines whose `origin=changed|unchanged` the script computes; a finding with no valid `hunk=`, `via=` or prior id is recorded `deferred: pre-existing` and is never blocking; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards inside the surface hunks only; an empty surface leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the script writes `reviser-brief-r<N>.md` (blocking finding ids only; omitted at `review: 3`, where the run escalates instead) and the report carries a `Reviser brief` just above the final `verdict:` line that names that file; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; map every changed hunk to one blocking id in `fixmap-r<N>.txt` and run `fixcheck` to exit 0 before the next review; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the surface hunks and the prior blocking findings, and may not grade a minor finding as blocking.
```

Bullet 3 (Verdict) gets one clause appended: "; the script derives the verdict and a differing last line is rejected". The 427 literals pinned by `tests/skills/test_spec_panel_review_loop.py` stay: `CANONICAL_CAP_TEXT`, `HALT and escalate to the user with the open blocking findings`, `resolved|open|regressed`, `origin=changed|unchanged`, `verdict: PASS`, `verdict: FAIL`, `review: N of 3`, `Reviser brief`, `byte size before and after`, the rf-qa lookup order (project first).

4. New section inserted right after `## Review Loop` and before `## Output Formats` (single-line numbered items):

```markdown
## Diffgate

1. **Script**: run it as `uv run --no-project python ~/.claude/skills/sc-diffgate-protocol/scripts/diffgate.py <subcommand> ...`, else the project copy `.claude/skills/sc-diffgate-protocol/scripts/diffgate.py` (skills resolve the home copy first); it reads the specification and writes only inside the `--diffgate-dir`, never the specification. Under `--unattended` the directory defaults to `<report-dir>/diffgate`.
2. **Begin**: before any review run `begin --dir <dir> --doc <spec> [--expect-round N]`; exit 5 means a step was skipped, run the step `status` names; with no `surface-r<N>.md` in a re-review, stop.
3. **Review surface**: in a re-review read `surface-r<N>.md` and, as read-only context, the specification; findings may anchor only to a listed hunk (`hunk=H<i>`), to an unchanged line a listed hunk breaks (`via=H<i> via_quote=[[...]]`, at most 2), or to a prior blocking id (`cites=`).
4. **Finding lines**: write the `## Diffgate findings` block exactly as `~/.claude/skills/sc-diffgate-protocol/SKILL.md` defines (`PRIOR`, `FINDING`, `FINDINGS none`), with `anchor=[[verbatim text]]` and, for a blocking `major`, `outcome=[[the concrete wrong outcome]]`.
5. **Check**: run `check --dir <dir> --report <report>` last; on exit 1 repair only the lines it names and run it once more; the script's `verdict:` is the verdict.
6. **Close**: at a derived PASS or at `review: 3`, print the verdict, the open blocking findings with their `chain:` and the whole `deferred.md` once under "Deferred, not looped on"; a FAIL says `halt: escalate`.
```

5. `## Unattended mode` (line 451 onward): byte-identical apart from the command name. Its text is pinned for `spec-panel` by `tests/skills/test_worker_contract.py` (`UNATTENDED_EXPECT["spec-panel"]`, line 576); keeping it equal means the variant inherits a section already reviewed.
6. `## Boundaries`: unchanged ("Modify specifications without explicit user consent" stays true; the script cannot write the specification).

### 8.2 New: `src/superclaude/skills/sc-diffgate-protocol/`

```text
sc-diffgate-protocol/
  SKILL.md              (frontmatter name: sc:diffgate-protocol; about 60 lines: purpose, subcommands, exit codes, report grammar, file formats of section 3; says it is invoked by commands, never by users)
  scripts/diffgate.py   (about 350 lines, stdlib only)
```

Script outline (names are proposals, not yet existing):

```python
#!/usr/bin/env python3
"""diffgate: computed re-review surface, anchor checker and fix gate. Stdlib only."""
import argparse, difflib, hashlib, json, os, re, sys
from pathlib import Path

MAX_ROUNDS = 3; MERGE_GAP = 2; VIA_CAP = 2; FIX_BUDGET_BYTES = 1500; OUTCOME_MIN = 25
EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = 0, 1, 2, 3, 4, 5, 6

def key(line): return " ".join(line.split())
def sha(text): return hashlib.sha256(text.encode()).hexdigest()[:12]
def read_text(path): ...                 # exit 3 on missing/unreadable/empty, names the path
def load_ledger(d): ...                  # exit 6 on parse error; {} -> fresh
def save_ledger(d, led): ...             # tmp file + os.replace

def build_hunks(old_lines, new_lines):   # section 3 steps 1-5; returns (hunks, ignored)
    sm = difflib.SequenceMatcher(None, [key(l) for l in old_lines], [key(l) for l in new_lines], autojunk=False)
    ...                                  # drop equal-token hunks, merge gap<=2, number H1.., ranges, section names
def render_surface(n, hunks, ignored, priors, ctx=2): ...
def cmd_begin(a): ...                    # order checks, round number, snapshot, surface; exit 4/5
def parse_report(text): ...              # PRIOR / FINDING / FINDINGS none / review: / verdict:
def check_report(parsed, led, n, snapshot_lines, hunks): ...   # rules C1-C13; returns (result, hard_errors)
def cmd_check(a): ...                    # reject once, then degrade; writes result, brief, deferred.md
def cmd_fixcheck(a): ...                 # rules F1-F3, budget, new_section; records fix map
def cmd_status(a): ...
def main(argv=None): ...                 # argparse subparsers; returns exit code
if __name__ == "__main__": sys.exit(main())
```

Rough size by part: diff and surface 90 lines, report parser and rules 140, begin/fixcheck/status 80, ledger and I/O 40. If review of the diff exceeds 450 lines, cut `status` and the `new_section` warning first.

### 8.3 Tests

| File | Status | Content |
|---|---|---|
| `tests/skills/test_diffgate_script.py` | new | Loads the script by `importlib.util.spec_from_file_location` (pattern of `tests/skills/test_workflow_archive.py:22-27`) and also runs it as a subprocess for exit codes. Cases: whitespace-only change ignored; re-wrapped paragraph ignored; edited line gives one hunk with the right new range; pure deletion gives before and after lines; two edits 2 lines apart merge, 3 apart do not; a 320-line input keeps the diff exact (the `autojunk=False` regression); `begin` round 1 writes snapshot and no surface; `begin` round 2 without an accepted fixcheck exits 5; changed spec after fixcheck exits 5; fourth review and review after PASS exit 4; wrong `--expect-round` exits 5; `check`: valid report accepted; anchor not on the cited lines exits 1 `E-ANCHOR`; fabricated hunk `E-HUNK`; `at` outside the hunk; neither hunk nor prior id is deferred and never blocking even with `sev=critical`; `cites` attaches evidence and adds no blocker; `via_quote` not in hunk `E-VIA`; third `via` deferred; missing `PRIOR` row `E-PRIOR`; `resolved` on an untouched anchor becomes `open`; major without `outcome` becomes minor; `verdict:` mismatch rejected then derived wins on the rerun; second failing submission degrades, `degraded: yes`, exit 0; `FINDINGS none` accepted; `fixcheck`: unmapped hunk exit 1, unknown id, hunk claimed twice, blocking id with no hunk and no `declined`, `declined` accepted, over-budget printed, heading flagged; ledger corrupt exits 6; the script never modifies the spec (sha equal before and after every subcommand) |
| `tests/skills/fixtures/diffgate/` | new | Three small synthetic documents (v1, v2, v3, about 60 lines each) and four reports (good, bad anchor, unanchored, degraded). A miniature replay of the `flg-r2` shape: five review-3 items of which two sit on minor-only lines and one is unchanged |
| `tests/skills/test_spec_panel_diffgate_command.py` | new | The variant file exists; has `name: spec-panel-diffgate`; its Usage names `--diffgate-dir` and not `--re-review`; `## Review Loop` has the seven bullets in order with the literals listed in 8.1 (imports `CANONICAL_CAP_TEXT`, `AT_CAP_CLAUSES` from `test_review_severity_rule.py` like `test_spec_panel_review_loop.py:14`); `## Diffgate` sits between `## Review Loop` and `## Output Formats` and names both script paths, home first; no `src/superclaude` string anywhere in the variant or in `sc-diffgate-protocol/` (`grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` check from project CLAUDE.md); `## Unattended mode` equals `spec-panel.md`'s after replacing the name; `spec-panel.md` still has its 427 Usage flags (guards "additive"); drift guard: every `## ` section body other than `Review Loop`, `Diffgate` and the frontmatter and Usage block equals `spec-panel.md`'s after the name replacement (R10) |
| `tests/skills/test_worker_contract.py` | edit, 3 lines | `_check_no_unattended_sections` (line 831) compares the set of command files that carry `## Unattended mode` with `UNATTENDED_COMMANDS`; a copied command would fail it (verified: lines 831-838, called at 1011 and 1124). Add `VARIANT_COMMANDS = frozenset({"spec-panel-diffgate"})` and subtract it from `have`; the new command test above pins that the variant's section equals the original's. The negative test at 1118-1126 (a scratch command with a section) still fails as before |

Existing tests that scan the new files and must keep passing without edit: `tests/skills/test_review_severity_rule.py` (scans `src`, `plugins`, `commands`, `agents`, `skills` for banned any-severity phrases and for a cap number above 2; the new text uses only "(3 reviews)" and "review: N of 3"). `tests/skills/test_spec_panel_review_loop.py` is parametrised over the two `spec-panel.md` copies only and is not affected. `tests/unit/test_cli_install.py` lists command names at lines 118 and 404; I did not verify whether it counts files in `src/superclaude/commands` (UNVERIFIED), so the implementer runs it first.

### 8.4 Docs, mirror, sync

- New `docs/designs/spec-panel-diffgate.md`: a short design record (decision, files, exit codes, residual risks, measurement bar) that points at this spec. `docs/designs/spec-panel-review-loop.md` (427) is not edited.
- No edit to `src/superclaude/core/HOW-WE-WORK.md` or the routing tests: the variant is an experiment arm, not a routed workflow. Adding a row would force the byte copy to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and the level-table test.
- Plugin mirror: none. `plugins/superclaude/commands/` holds 28 files against 48 in `src/superclaude/commands/` (counted), and `plugins/superclaude/skills/` holds four skills, so mirroring is not the rule for newer primitives. Whether any test requires a mirror for a new command is UNVERIFIED.
- `make sync-dev` copies the command and the whole skill folder (script included) into `.claude/`; `make verify-sync` then passes. `.claude/` stays unstaged (project rule).

### 8.5 Install note and the brief substitution an experiment needs

Workers load `/sc:<name>` from `~/.claude/commands/sc/`; the project copy is ignored (AB-REPORT "Machine facts"). The experiment adds files and edits none:

```bash
cp src/superclaude/commands/spec-panel-diffgate.md ~/.claude/commands/sc/spec-panel-diffgate.md
mkdir -p ~/.claude/skills/sc-diffgate-protocol
cp -R src/superclaude/skills/sc-diffgate-protocol/. ~/.claude/skills/sc-diffgate-protocol/
sha256sum ~/.claude/commands/sc/spec-panel-diffgate.md ~/.claude/skills/sc-diffgate-protocol/scripts/diffgate.py   # record in the run log
```

`superclaude install` would also add the new names (it keeps existing files unless `--force`; UNVERIFIED for skills), but `cp` is explicit and cannot touch `spec-panel.md`; never pass `--force` during an experiment. Brief changes, with `<DIR>` one directory for the whole loop (for example `<report-dir>/diffgate`):

```bash
# review briefs 2 and 3 (they carry 427's flags today): name and flags
sed -E -e 's#/sc:spec-panel( |$)#/sc:spec-panel-diffgate\1#g' \
       -e 's#--re-review [^ ]+ --baseline [^ ]+#--diffgate-dir <DIR> --expect-round <N>#g' brief.md
# review brief 1 (no flags today): rename and append by hand
#   /sc:spec-panel-diffgate @<spec> --mode critique ... --diffgate-dir <DIR> --expect-round 1
```

Reviser brief (both fix cycles), one added line: "Your task list is `<DIR>/reviser-brief-r<N>.md`, not the whole report; after editing write `<DIR>/fixmap-r<N>.txt` and run `uv run --no-project python ~/.claude/skills/sc-diffgate-protocol/scripts/diffgate.py fixcheck --dir <DIR> --doc <spec>` until it exits 0." Record the substitution in the coordinator log, as AB-REPORT requires for a name change. Whether the S1 workers may run `uv run` from the home skill folder under their permission mode is UNVERIFIED (section 12).

Check before commit (installed primitives name installed paths only): `grep -rn 'src/superclaude' src/superclaude/commands/spec-panel-diffgate.md src/superclaude/skills/sc-diffgate-protocol` must print nothing.

## 9. Measurement plan on scenario S1

**Design.** Scenario S1 exactly as in `AB-REPORT.md` and `ARMB-REPORT.md`: Orca worker-contract spec (57,763 bytes), base commit 2cb683f5, model claude-opus-5-5, three reviews, two fix cycles, the same verbatim briefs with the substitution of section 8.5 and the reviser line. Two replicates (`dg-r1`, `dg-r2`). Compared with the existing control (R3 proxy 8 and 4, mean 6.0; growth 57.7 and 69.3%, mean 63.5%) and Arm B (R3 proxy 6 and 1; growth 27.8 and 32.1%). Same caveats as Arm B: control not concurrent, n = 2 against 2, a screen for a large effect only. `WORKER-CONTRACT.md` moved aside as in the earlier arms. The bar is the one already pre-registered (D10, D11) and is not changed here.

**Counting rules fixed before the run.**

- Primary metric `R3-proxy-all`: critical plus major `FINDING` lines in the review-3 report plus open or regressed critical/major priors, **including findings the script deferred** (their `sev` label counts). This is the same reading the AB reports used (reviewer labels) and it stops the arm from winning by deferring. Secondary: `R3-blocking-derived` (the script's blocking list) and 427-grade blocking.
- Growth: bytes of the spec after fix cycle 1 and 2 against the starting spec, as before.
- Validity gate (new): a replicate is valid only if `ledger.json` shows an accepted `check` for rounds 1 to 3 and an accepted `fixcheck` for rounds 1 and 2, the installed file hashes did not change (install watcher), and no worker read `origin/master`. An invalid replicate is rerun, not scored.
- Extra recordings: rejects and `degraded` per review; deferred count and text; `via` use; fix hunks mapped, rejected and reverted; hunks per fix cycle; share of review-3 blockers sitting on mapped fix hunks; chain lengths; script calls and tool calls per step; wall time per step; reviewer session length.
- Blind audit (report only, not a bar): after review 3, one independent whole-document review of the final spec outside the loop, run the same way for control, Arm B and diffgate if budget allows, counting blocking-grade findings on lines the loop never surfaced. This measures what diffgate hides.

**Predictions, with reasoning.**

| Metric | Control mean | Bar | My prediction | Reasoning |
|---|---|---|---|---|
| R3-proxy-all (critical+major in review 3) | 6.0 | 3 or fewer in both replicates, or a clean PASS | **3.5 mean** (replicates about 5 and 2; plausible range 1.5 to 5.5) | Arm B's two replicates were 6 and 1 with scope already honoured in form, so the surface alone adds little. What diffgate adds is the fix gate. The one replay (section 1) removed 3 of 5 review-3 items (2 on minor-only lines, 1 unchanged) and 0 of 1 blockers. If `flg-r1` (6) has the same composition, about 40% of its items vanish or defer, giving 3 to 4, and `flg-r2` stays at 1. Deferred items still count in the primary metric, so I do not bank them |
| Spec growth after two cycles | 63.5% | 44.4% or less | **23% mean** (range 17 to 30%) | Arm B was 27.8 and 32.1%. The 25 changed lines of `flg-r2`'s round 2 split 13 blocking and 12 minor-only; if bytes follow lines, the second cycle's 8.6% growth falls to about 5%, and the first cycle's 17.5 to 21.6% to about 13 to 16%. Compounded: about 19 to 23% |
| Clean PASS by review 3 | 0 of 6 runs so far (2 control, 2 treatment A, 2 Arm B) | not required | 10% per replicate | A mapped fix still induced the blocker N12 in the replay |

Probability that both replicates meet the R3 bar: about 0.25. Probability the growth bar is met in both: about 0.9 (427 alone already met it).

**What result would mean the idea failed** (declared before the run):

1. **F1, wrong lever.** Either replicate has R3-proxy-all of 5 or more while 70% or more of its review-3 blockers sit on mapped fix hunks. The scope and fix gates worked as designed and the metric did not move: the driver is the per-fix defect rate, and the next idea must act on fix quality (for example a reviser self-check), not on scope.
2. **F2, no growth win beyond 427.** Growth above 44.4%, or mean growth not below Arm B's 30.0%: the fix gate did not constrain the reviser.
3. **F3, blinding.** The blind audit finds two or more blocking-grade defects per replicate on lines diffgate deferred or never surfaced, and the control audit finds fewer: diffgate hides real regressions. Stop and revisit `via`.
4. **F4, too heavy.** In either replicate more than one review needs a second `check` run or ends `degraded: yes`, or a loop stalls on a script error: the grammar costs more than it returns.

Only F1 to F4 absent together and both replicates at 3 or fewer count as success. A mixed result (growth bar met, R3 bar missed) is reported as such, not rounded up.

## 10. Costs and risks

**Costs per loop (three reviews, two fix cycles).**

| Item | Estimate | Basis |
|---|---|---|
| Extra tool calls, reviewer side | 3 per review (`begin`, read the surface, `check`), plus at most 1 rerun of `check` per review: 9 to 12 | counted from the steps in section 2 |
| Extra tool calls, reviser side | read the brief, write the map, `fixcheck` once or twice: 4 to 5 per cycle, 8 to 10 | same; the first `fixcheck` often rejects an unmapped hunk |
| Extra sessions | 0. Same three reviewers and two revisers | rejects are repaired in the same session |
| Script run time | well under 1 second each (a few hundred lines diffed with `difflib`) | S1 spec is about 317 lines |
| Wall time | about 3 to 5 extra minutes per loop at 10 to 15 seconds per tool round trip | estimate, not measured |
| Offsetting saving | reviews 2 and 3 skip the whole-document pass and the prior-report re-read; `flg-r2` review 3 spent Part 1 (15 rows) and Part 2 (20 citation groups) first | UNVERIFIED that it saves more than it costs; section 9 records step times |
| Build cost | about 350 lines of script, about 60 lines of `SKILL.md`, about 25 script tests, one 490-line variant file, one 3-line test edit | section 8 |
| Debt added | a forked command (drift) and a ledger format | see R10 and R11 |
| Debt removed (on Stage C) | bullet 5 and 6 prose, `baseline: missing`, the coordinator's saved-copy duty, the self-typed `origin=` | section 7 |

**Ways the mechanism could make the loop worse, and what limits each.**

- **R1. Blinding the reviewer to a real regression.** A fix breaks text it did not touch (a cross-reference in another section). Limits: the specification stays readable as context; `via=` lets a blocker anchor to an unchanged line through a quote-checked hunk (2 per review); every deferred item is printed once with the reviewer's own label; the blind audit (section 9) measures what was hidden. Residual: a reviewer that does not think to use `via`.
- **R2. Missed once is missed for good.** A defect on a fix-changed line that review N+1 overlooks is never reopened (section 5.1). That is the price of convergence; it is also why the end-of-loop deferred list and the blind audit exist.
- **R3. A reviewer gaming the anchors.** It can cite a nearby changed hunk to make a pre-existing issue count, or pad `outcome` to 25 characters. Limits: `at` must lie inside the hunk's range and the quote must be present on those lines; merge gap is only 2. Residual: semantic fit of the finding to the anchor is not checked.
- **R4. Diff noise.** A re-wrapped paragraph is dropped only when its words are identical; a re-wrapped and edited paragraph is one big hunk. A moved block appears as a deletion plus an insertion. A rewrite that changes most of the file makes the surface nearly the whole document. Limit: `begin` prints `coverage: <percent of new lines inside hunks>`, and above 50% the surface header says so (a 2-line addition to the script), so the coordinator sees the loop has degenerated into a full review. Residual: the script does not detect moves.
- **R5. The reviser gaming the fix map.** It can map an unrelated edit to a blocking id. Limits: the map is written down and printed with `added_bytes` per id and `over_budget`; the next surface prints `fixes: R1.5` on each hunk, so the next reviewer sees what each edit claims to repair. Residual: nothing verifies the claim.
- **R6. Machine lines and prose drifting apart.** A finding written only in prose never reaches the reviser, because the reviser's list comes from the machine lines. Limit: an extra rule C2b, every `R<N>.<j>` token anywhere in the report must exist as a `FINDING` line (hard, `E-FORMAT`). Residual: a prose finding with no id at all.
- **R7. The script itself.** A bug, a missing `uv`, a worker permission mode that blocks `uv run` from `~/.claude/skills/...`, or a missing skill install stops the loop. There is deliberately no silent fallback to prose review, since that is today's failure; the command stops and says which path was missing. Limits: unit tests, the fixture replay, the install hash record, and exit 6 for a corrupt ledger (the script never repairs it).
- **R8. Report-format tax.** The machine block is new work for the reviewer; F4 in section 9 is the pre-registered check that it does not cost more than it returns. Fail-safe degrading can add a spurious `open` prior but never an unanchored blocker.
- **R9. Wrong or dropped directory.** A fresh directory restarts at `review: 1 of 3`. Limit: `--expect-round N` in the brief (exit 5 on mismatch). Residual: a brief without it.
- **R10. A forked command drifts from `spec-panel.md`.** Limit: the command test compares every `## ` section body that this change does not touch against `spec-panel.md` (added to row `test_spec_panel_diffgate_command.py` in 8.3), so an upstream edit breaks the variant's test instead of silently diverging.
- **R11. Ledger as new state.** Hand edits break the locks by design; two workers writing one directory at once are not locked (atomic replace only). The loop is sequential in S1 and in every Orca flow I read.
- **R12. Derived severity versus the reviewer's label.** A true major with no `outcome` becomes minor and cannot fail the loop. This is 427 grading bullet 2 made literal, but it can look like severity drift in reverse. Limit: the primary metric in section 9 uses the reviewer's labels, not the derived ones.

## 11. Later adopters

The script is document-agnostic (text lines in, hunks and a ledger out), so it can serve other loops. None of the adoptions below is part of this change; each lists what it would need.

| Adopter | Fit | What it would need | Order |
|---|---|---|---|
| rf-qa agents (Fix Cycle, `~/.claude/agents/rf-qa.md`) | High. Same shape: a QA pass, a fix, a re-check of prior findings. Bullet 5 of the Review Loop already points the re-check at its steps 1 to 5 | rf-qa calls `begin` and `check` with its own report grammar (the `PRIOR`/`FINDING` block can be shared); the fixer calls `fixcheck`. rf-qa also checks task files and research output, so a second input kind (a file set) is likely | first, after Stage C |
| `/sc:reflect` UC-2 (post-execution deviation audit) | Medium. The baseline is a git tree, not a saved copy, and the unit is several files | Multi-file surfaces: hunk ids prefixed by path, `--baseline-ref <sha>` instead of `doc-r<N>.md`; the deviation taxonomy (Authorized, Necessary, Drift, Regression) maps onto `origin` and `fixes:` | second |
| `/sc:implement` final review (`sc-implement-protocol/refs/qa.md`, archive gate in `refs/managed-workspace.md`) | Low as a replacement, medium as a shared checker. `qa.md` already has the parent derive the verdict, Read anchors back, cap inherited text from `git diff` hunk headers and track `resolved\|open\|regressed` | Nothing to replace. A later cleanup could let `qa.md` call the same anchor Read-back and hunk code instead of its prose description, which would remove duplicate rules | last |
| `/sc:spec-panel` itself | The target of Stage C | fold `## Diffgate` into `spec-panel.md`, drop the 427 flags, move the pins in `tests/skills/test_spec_panel_review_loop.py`, and mirror into `plugins/superclaude/commands/spec-panel.md` (which already drifts from `src/` by one word at line 219) | after the S1 bar |

Reach, for scale: the AB report records that 427 reaches only `/sc:spec-panel`, and that of five recreated incidents only S1 used it (in 3 of 7 reviews, with no `--re-review` in the briefs); four of five incident types (`/sc:reflect`, plain agents, rf-qa agents, the `/sc:implement` final review) never call it. A script that rf-qa and `/sc:reflect` can also call is the only route in this proposal that reaches them, and it is worth little until the S1 result is in.

## 12. Open questions

1. **Worker permissions (UNVERIFIED, blocks the experiment).** Can an S1 worker run `uv run --no-project python ~/.claude/skills/sc-diffgate-protocol/scripts/diffgate.py` under its permission mode, and does `uv` resolve offline with no dependencies? A one-worker smoke run of `status` settles it before any replicate.
2. **Does `Skill sc:spec-panel-diffgate` load a command the user-level folder holds only as an additive file?** The round-3 reviewer observed `Skill sc:spec-panel` loading `~/.claude/commands/sc/spec-panel.md`; the same for a new name is expected but not observed here.
3. **Hunk granularity.** Lines are the unit, merged at a gap of 2, with a section name. Section-level hunks would give more context and fewer false findings but a larger surface; paragraph-level units would help hard-wrapped specs. S1's spec has long single-line paragraphs, so lines fit; a hard-wrapped spec may need `--unit para`.
4. **`via` cap of 2 and `FIX_BUDGET_BYTES = 1500` are guesses.** The budget comes from about 960 bytes per blocker in S1 round 1; neither is calibrated. Keep them as constants in the script and record actual use in S1.
5. **Verdict ownership versus 427 bullet 3.** The script derives the verdict and the report's last line must agree. If a maintainer wants the reviewer to remain the owner, the script can instead warn on a mismatch. I chose derive because 427's reviewer-owned verdict is one of the measured drifts.
6. **Reviser sees blocking ids only.** The reviser no longer reads minors, which is the point, but a minor that is a typo-class fix is then left for a human. Is a separate "minor sweep" after the loop wanted (a human decision, outside the loop)?
7. **Rejected reports: redo once, then degrade.** Is silent degrading acceptable, or should a second failure stop the run with exit 1 and escalate? I chose degrade so a format error can never block a document review, at the price of possible spurious `open` priors.
8. **Reflow and moves.** Re-wrapped paragraphs are filtered when word-identical; moved blocks are not detected. Is a move detector worth 20 lines?
9. **Does the fix map belong in the spec?** Mapping lives in a side file so the specification carries no review ids. In the S1 runs revisers wrote ids inline anyway ("every spec change carries its finding id inline"). Accepting inline ids as an alternative map would save a tool call but pollute the document.
10. **Where the script's ledger lives under `--unattended`.** `<report-dir>/diffgate` keeps `artifacts` in `return-contract.yaml` unchanged; whether WC-4's rule about git-ignored paths would want these files listed is UNVERIFIED.
11. **Unverified read of the existing test list.** `tests/unit/test_cli_install.py` names `spec-panel.md` in command lists at lines 118 and 404; I did not establish whether a new command file in `src/superclaude/commands/` changes any expected count there.
12. **`flg-r1` composition.** Only the `flg-r2` reports were read. The prediction in section 9 assumes `flg-r1` looks similar; reading its review-3 report for the share of findings on minor-only lines would tighten or break the prediction before any run is paid for.
