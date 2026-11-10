---
adversarial_status: partial
adversarial_convergence: 0.99
adversarial_gate: BLOCKED_BY_INVARIANTS (7 HIGH items, each resolved in the merge by adopting the invariant probe resolution; see nested/adversarial-1/adversarial/refactor-plan.md)
source: nested/adversarial-1/merged-output.md
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:refactorer) -->
<!-- Merge date: 2026-11-08T16:00:16Z -->

<!-- Source: Base (original, modified) - title renamed to the merged design -->
# Proposal: diffgate for /sc:spec-panel re-reviews, variant command `spec-panel-diffgate` (merged design)

Issue #346. Additive variant command `spec-panel-diffgate`. Lens: technical debt, simplification, minimal-risk transformation.

<!-- Source: Base (original, modified) - adjusted per Changes #4 and #28 -->
## 1. Problem and evidence

**The debt in 427.** PR 427's `## Review Loop` bullet 5 asks a model to do four mechanical jobs in prose: find the changed lines, tag each finding `origin=changed|unchanged`, keep the review count, and say `PASS` or `FAIL`. Bullet 6 asks a second model to touch only text a blocking finding names. Nothing computes or checks any of it (design doc section 12: "Prose only"; section 9: "The tests prove the text is present"). The Arm B reports show the prose is obeyed in form (status table, `origin=` tags, `review: N of 3`) and still does not converge.

**What was measured (S1, 2 replicates per arm; `AB-REPORT.md`, `ARMB-REPORT.md`):**

| # | Cause | Evidence | Removed by this proposal? |
|---|---|---|---|
| 1 | Fix-induced findings on changed lines | 89% of review-2 and 100% of review-3 new findings are `origin=changed`. In `flg-r2` all six review-2 blockers (N1-N6) and the only review-3 blocker (N12) sit on lines the previous fix changed | **No.** Those lines are in scope by design. The proposal only bounds how many lines a fix may change (the next row) and stops a line being reviewed twice (section 5). It cannot stop a mapped fix from being wrong |
| 2 | Revisers add work no blocking finding asked for | `disposition-round2.md`: "Minor findings were applied too"; all 15 rows applied; two extra "related defects" fixed (E5, AC-1.2). Of the 25 spec lines the round-2 revision changed (the `Changed lines` list in `spec-panel-round3.md`), some trace to blocking ids N1-N6 and the rest only to minor or citation rows (line 5 carries both an N1 and an N11 id). The gate removes the minor-only and citation lines and keeps every line that carries a blocking id | **Yes, mechanically.** A fix hunk with no blocking id in the fix map is rejected (section 5) |
| 3 | Severity drift between rounds | 427 grading relabels some MAJOR findings as minor (flg-r1 R3-7, R3-8: proxy 6, blocking 4) | **Partly.** The script derives blocking from fields it can check (`outcome=` present, anchor present, in scope); the reviewer's severity word is still judgement |
| 4 | Re-review re-attacks the whole document | Review 3 of `flg-r2` spends Part 1 (15 rows) and Part 2 (20 citation groups) before Part 3; the reviewer derived its own `git diff --no-index -w` and judged its own scope | **Yes.** The surface is computed; a finding that anchors to nothing is deferred (sections 3, 4, 6) |
| 5 | Nothing mechanical stops the loop or checks the count | The count lives in a header the coordinator must carry; "a coordinator that drops the flags starts a fresh first review" | **Yes.** The count and the order of steps live in a ledger file; `begin` refuses out-of-order steps and a fourth review |

**Retrofit evidence for the gate (one real case).** Replaying the fix-map gate over the round-2 revision of `flg-r2`: of the five review-3 items (N12, N13, N14, N15, C-R3-15), N14 (line 62, from the minor row N9) and C-R3-15 (line 11, a citation row) sit on minor-only lines and would not exist; N15 is `origin=unchanged` and would be deferred; N12 (lines 60 and 220, from the N5 fix) and N13 (line 223, from the N3 related fix) stay. Total 5 to 2, blocking 1 to 1. Honest reading: the gate removes noise and growth and leaves the induced blocker that a mapped fix produced. This replay used one replicate's reports; the `flg-r1` composition was read later (`debate/evidence-flg-r1.md`) and does not share it (section 9).

**What stays unfixed (said up front).** If the real cause is that a correct-looking fix to a blocking finding creates a new defect at a rate near 0.2 to 0.5 per mapped fix (round 2: six induced blockers from thirteen round-1 blocking fixes; round 3: one from six), then no scope rule reaches PASS in three reviews on a spec this size. Diffgate bounds that and makes it measurable; it does not remove it. The `flg-r1` evidence (`debate/evidence-flg-r1.md`) shows this case: all 4 review-3 blockers sit on text written by blocking fixes, and no mechanism inside the diffgate theme lowers that count without relabelling or hiding it. The design's claim is therefore "escalate with an interpretable record", not "converge". Section 9 states which result would say so.

<!-- Source: Base (original, modified) - adjusted per Changes #5, #6, #12, #19, #21 and #22 -->
## 2. Mechanism: the loop step by step

Notation. `DG` = `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py` (else the project copy `.claude/skills/sc-diffgate/scripts/diffgate.py`; skills resolve home first, per the project CLAUDE.md; if neither exists the command stops with `E-DIFFGATE-MISSING` and never falls back to a plain review). `<dir>` = the loop directory, `--diffgate-dir <dir>` (under `--unattended` it defaults to `<report-dir>/diffgate`). `<spec>` = the document under review. The loop has two kinds of worker (reviewer, reviser) and one coordinator (an Orca coordinator or a human). The script is run by the worker that owns the step; it never edits `<spec>`.

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
| `fixmap-r<N>.txt` | reviser (candidates pre-filled by `fixcheck`) | first line `doc_sha: <sha>`; one line per fix hunk: `H<k>.<n> R<N>.<j>[,R<N>.<m>...]`; `declined R<N>.<j> <reason>` for a finding it will not fix |
| `deferred.md` | script (`check`) | cumulative list of findings recorded `deferred: pre-existing` or `deferred: unanchored`; never read by a reviser |

**Steps, in order:**

| # | Step | Who | Command / action | Reads | Writes |
|---|---|---|---|---|---|
| 1 | Review 1 starts | coordinator | dispatches `/sc:spec-panel-diffgate @<spec> --mode critique ... --diffgate-dir <dir>` | brief | none |
| 2 | Open the loop | reviewer command | `DG begin --dir <dir> --doc <spec>`; prints one JSON object whose `review` field is 1 (`review: 1 of 3`, a full review) | `<spec>` | `ledger.json`, `doc-r1.md` |
| 3 | Review 1 | reviewer | today's full-document review; adds `FINDING` lines (grammar in section 4) and writes no verdict line (the command appends the script's `verdict_line` after step 4) | `<spec>` | report |
| 4 | Check 1 | reviewer command | `DG check --dir <dir> --report <report>`; on exit 1 the reviewer repairs the report once and reruns | report, `ledger.json`, `doc-r1.md` | `result-r1.json`, `reviser-brief-r1.md` if FAIL, `deferred.md`, or `reject-r1.txt` |
| 5 | Fix cycle 1 | reviser | reads `reviser-brief-r1.md` (not the whole report); edits `<spec>`; confirms the candidates `fixcheck` pre-fills in `fixmap-r1.txt` or writes `declined`; runs `DG fixcheck --dir <dir> --doc <spec>` until exit 0 (at most 3 runs; after the third failure the ledger records `fix-rejected`, the reviser stops and the coordinator escalates to the user) | brief, `<spec>`, `doc-r1.md` | `<spec>`, `fixmap-r1.txt`, ledger fix record |
| 6 | Review 2 starts | coordinator | same brief as step 1 | | |
| 7 | Open review 2 | reviewer command | `DG begin ...`; refuses (exit 5) unless fixcheck 1 is accepted for the current doc sha, and re-runs that check (exit 1 on an unmapped hunk); computes the delta; prints one JSON object with `review` 2 (`review: 2 of 3`), `hunks` and `priors` | `<spec>`, `doc-r1.md`, `result-r1.json`, ledger | `surface-r2.md`, `doc-r2.md`, ledger |
| 8 | Review 2 | reviewer | reads `surface-r2.md` and, as read-only context, `<spec>`; writes a `PRIOR` row per prior blocking id and `FINDING` lines; no whole-document pass | `surface-r2.md`, `<spec>` | report |
| 9 | Check 2 | reviewer command | as step 4 | | `result-r2.json`, brief, `deferred.md` |
| 10 | Fix cycle 2 | reviser | as step 5, with `reviser-brief-r2.md`, baseline `doc-r2.md` | | `<spec>`, `fixmap-r2.txt` |
| 11 | Review 3 | coordinator, reviewer | as steps 6 to 9; `review: 3 of 3`; baseline `doc-r2.md` | | `result-r3.json`, `deferred.md`; no reviser brief |
| 12 | End | reviewer command, coordinator | after check 3 the command writes, in this order: the findings block, the open blocking ids with their fix chains, `## Deferred (pre-existing, not looped on)` with the contents of `deferred.md`, the scoped-PASS line if any, then the verdict line as the report's last non-blank line; FAIL says `halt: escalate`; the coordinator escalates to the user. A later `begin` exits 4 | `result-r3.json`, `deferred.md` | none |

Early exit. If `check` derives `PASS` at review 1 or 2, the ledger is `closed`, no reviser brief is written, the command writes `deferred.md` once above the verdict line (the verdict line stays the last non-blank line), and a later `begin` exits 4 with `halt: pass`. <!-- Source: Invariant probe INV-027 - merged per Change #22 (adopted, not debated) -->

**Where a model could skip a step, and what then happens** (the lock points; the aim is that skipping is loud, not that skipping is impossible):

- Reviewer skips `begin`: it has no `surface-r<N>.md`, and the command text says to stop without one; if it reviews anyway, `check` exits 5 (no round open).
- Reviewer skips `check`: no `result-rN.json`, so no `reviser-brief-rN.md`; the reviser's step 5 starts with "if the brief is missing, run `check` first", and `fixcheck` exits 5 without an accepted check.
- Reviser skips `fixcheck`: `begin` for the next review exits 5. The loop stops visibly instead of reviewing an unchecked edit.
- Anyone edits `<spec>` after `fixcheck`: the doc sha differs, `begin` exits 5.
- Anyone hand-edits `ledger.json` or a recorded report: `begin` replays `check` on the recorded report and exits 6 on any difference; a second writer in the same directory is refused by the exclusive-create lock. <!-- Source: Variant A (opus:architect), Section 4.4 and Variant C (haiku:qa), Section 3 - merged per Change #21 -->
- The coordinator drops `--diffgate-dir`: the variant refuses `--mode critique` without it (it is the variant's only reason to exist), so the failure is loud, not a silent fresh review as in 427.
- The coordinator points a later review at a fresh or wrong directory: that starts as `review: 1 of 3`. The brief can pass `--expect-round N` through to `begin`, which exits 5 when the ledger-derived round differs. The S1 briefs use one directory throughout and pass `--expect-round`. Residual risk: a coordinator that omits it (section 10, R9).

<!-- Source: Base (original, modified) - adjusted per Changes #5, #6, #7, #8, #9, #15, #16, #17, #19, #20 and #21 -->
## 3. Who computes the diff, and the script interface

**Decision: a Python stdlib script shipped in a skill folder, run by the worker that owns each step. Not a fixed command sequence.**

Why not `git diff --no-index -w` as a fixed sequence (what the Arm B reviewer ran by hand): it yields a diff but not stable hunk ids, section names, a reflow filter, an anchor Read-back, a ledger or a lock between steps. Every one of those would again be a sentence a model is asked to obey. Why not "the coordinator runs it": an Orca coordinator or a human is also a prose follower, and the reviewer cannot wait on it. Placement is solved by locks instead (section 2): each step's output is the next step's only input, so a skipped step stops the loop.

Host skill: `sc-diffgate`, a delegate-only infrastructure skill like `sc-bare-review`, called by path (needs a `SKILL.md` for `install_skills.py` to install it; verified at `install_skills.py:167-170` and `Makefile` `sync-dev`, which copies every file of a skill folder except `__init__.py`). The name is not the command's name on purpose: `install_skills.py` lines 40-62 skip a skill whose name, with `sc-` stripped, matches a file in `commands/`, so a skill named after the command would not install. Script path in the command: `~/.claude/skills/sc-diffgate/scripts/diffgate.py`, else the project `.claude/skills/sc-diffgate/scripts/diffgate.py`; if neither exists the command stops with `E-DIFFGATE-MISSING` and never falls back to a plain review. Script: `scripts/diffgate.py`, Python 3.10+, stdlib only (`argparse`, `difflib`, `hashlib`, `json`, `os`, `pathlib`, `re`, `sys`); `difflib` is already used in `src/superclaude/cli/eval/expect.py:33`.

<!-- Source: Variant A (opus:architect), Section 3.3 and Variant C (haiku:qa), Section 3 - merged per Change #7 -->
Every subcommand prints exactly one JSON object on stdout, with the fields `ok`, `exit`, `message` and `review`, plus the per-subcommand fields in the table below. Verdict and execution success are separate fields: never read exit 0 alone as a review PASS.

**Subcommands**

| Subcommand | Inputs | Writes | Stdout fields (one JSON object) |
|---|---|---|---|
| `begin --dir D --doc F [--expect-round N]` | spec `F`, loop dir `D` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N>=2); for N of 2 or more, recompute the fix-map check against `doc-r<N-1>.md` and the current spec; any unmapped hunk exits 1 with the unmapped list and opens nothing | `surface`, `hunks`, `ignored`, `coverage`, `priors` |
| `check --dir D --report R` | review report `R` | `result-r<N>.json`, `reviser-brief-r<N>.md`, `deferred.md`; or `reject-r<N>.txt` | `accepted`, `verdict`, `verdict_line`, `acceptance`, `blocking`, `deferred`, `degraded`, `halt` |
| `fixcheck --dir D --doc F [--map M]` | spec after the fix; map defaults to `D/fixmap-r<N>.txt` | ledger fix record; pre-fills map candidates from inline `R<N>.<j>` tags; exits 1 when the map's `doc_sha` line differs from the spec; the third failure in a cycle records `fix-rejected` | `hunks`, `mapped`, `declined`, `withdrawn` candidates, `bytes_by_id`, `hunks_by_id`, `unmapped` (on exit 1 the unmapped hunks with their lines) |
| `status --dir D` | ledger | nothing | `state` (one of `open`, `checked`, `fixed`, `closed`, `invalid`), `next` (the one command that should run next) |

**Exit codes** (all subcommands; the model must act on the code, so each has one meaning):

| Code | Meaning | Who acts |
|---|---|---|
| 0 | done; includes an accepted review whose verdict is FAIL; read `verdict`, never the exit code, for the review result | continue |
| 1 | the input was rejected (`check`: bad report; `fixcheck`: unmapped or unknown hunks); reasons on stdout and in `reject-r<N>.txt` | the caller fixes its own file and reruns, at most twice |
| 2 | usage error, or an input over the limits (2 MiB, 100,000 lines, 1,000 machine lines) | fix the command line or the input |
| 3 | an input file is missing, unreadable or empty (427 bullet 1: "stop and say which") | stop, say which |
| 4 | the loop is closed: `halt: pass`, `halt: escalate` (cap reached, or a fourth review requested) or `halt: invalid` (a second structural stop in one review, section 4) | stop, report; on `halt: invalid` escalate to the user |
| 5 | steps out of order: no open round, no accepted check or fixcheck for the current doc sha, or `--expect-round` differs | run the step the `next` field names |
| 6 | the ledger is corrupt, does not parse, or disagrees with the replay of the recorded report | stop, escalate to the user (the script never repairs it) |

**Diff computation (deterministic; the same code serves `begin` and `fixcheck`).**

1. `old` = lines of `doc-r<N-1>.md`; `new` = lines of the spec. A line's comparison key is `" ".join(line.split())` (whitespace collapse, so indentation and trailing space never count).
2. `difflib.SequenceMatcher(None, keys_old, keys_new, autojunk=False)`. `autojunk=False` matters: the default heuristic switches on at 200 lines and the S1 spec has about 317, so without it popular lines (table separators, blank lines) are junked and the diff degrades.
3. Each non-`equal` opcode is a candidate hunk. Drop it when `" ".join(old_part).split() == " ".join(new_part).split()` (whitespace, blank-line and re-wrap only; this is the reflow filter) and the count of lines that start with a Markdown list marker, heading marker or table pipe is the same on both sides; count it under `ignored`. Otherwise keep a word-identical block as a hunk with `structural: yes`, which needs an owner in the fix map and is eligible in the next review. <!-- Source: Invariant probe INV-025 and debate round2-C.md New evidence 2 - merged per Change #20 --> Second pass (token level): inside each remaining non-`equal` block, split the old and new parts into whitespace tokens with line and offset, and run a second `SequenceMatcher` on the tokens; inserted and replaced new-side tokens are the changed span, deleted and replaced old-side tokens are the removed span. Only the changed span (or the removed span, for `side=old`) is eligible for a finding. <!-- Source: Variant A (opus:architect), Section 3.5 steps 3-4 - merged per Change #9 -->
4. Merge changed lines whose new-side gap is 2 lines or less (`MERGE_GAP = 2`) into one hunk id, so one logical edit that touches a line and the line after the blank is one hunk. The merge groups lines for the fix map and the display only: gap lines and display context are never eligible (context is read-only and cannot widen eligibility). A renumbered list merges into one block hunk with one owner; there is no separate `renumber` line. Line ranges are 1-based and inclusive everywhere.
5. Number surviving hunks `H<k>.<n>` in document order, where k is the review the surface feeds; ids never repeat across reviews. The reviewable range of a hunk is the new lines that hold its changed span; for a pure deletion the surface shows the line before and the line after the deletion point as display context, and a finding on the deleted requirement anchors to its removed tokens with `side=old`. `section` = the nearest Markdown headings above the range, joined with `>`.
6. Because the fix cycle's diff and the next review's diff are the same two files (`doc-r<N>.md` and the spec, sha-locked), **hunk ids in `fixmap-r<N>.txt` and in `surface-r<N+1>.md` are the same ids.** The surface can therefore print "H2.2 = the fix for R1.3".

**Surface file (`surface-r2.md`), format and example**

```text
# diffgate surface: review 2 of 3
doc: specs/orca-worker-contract-spec.md   doc_sha: 3f9a1c20d4be   baseline_sha: 91be07a5c3d2 (doc-r1.md)
hunks: 7   ignored (whitespace or re-wrap only): 2   merge_gap: 2   coverage: 9% of lines
Rule: a new finding must cite one of the hunks below (hunk=H<k>.<n>, at= inside it) or a prior id under "Prior blocking findings". Anything else is recorded "deferred: pre-existing".

## H2.2   new lines 60-60 (old 58-58)   section: 2. Worker rules > WC-1   fixes: R1.5
ctx  59: <unchanged line, read-only>
-    58: <old text>
+    60: <new text>
ctx  61: <unchanged line, read-only>

## H2.3   ...

# Prior blocking findings (from result-r1.json)
R1.5  sev=major  at=60 (was 58)  fix hunks: H2.2
  anchor: "WC-1 ... session-name question"
  outcome: "a vacuous pass is recorded for WC-1"
R1.9  sev=critical  at=66  fix hunks: none
```

**Ledger (`ledger.json`) sketch** (written atomically: temp file, then `os.replace`):

```json
{"version": 1, "doc": "specs/x.md", "closed": null, "degraded": false,
 "rounds": {"1": {"doc_sha": "91be...", "snapshot": "doc-r1.md",
                  "check": {"accepted": true, "verdict": "FAIL", "report_sha": "...", "blocking": ["R1.5", "R1.9"]},
                  "fix":   {"accepted": true, "doc_sha": "3f9a...", "map": {"H2.2": "R1.5"}, "declined": {"R1.4": "evidence does not hold"}, "bytes_by_id": {"R1.5": 410}, "hunks_by_id": {"R1.5": 1}}},
            "2": {"doc_sha": "3f9a...", "state": "open", "attempts": 0, "surface": {"hunks": [{"id": "H2.2", "new": [60, 60], "old": [58, 58], "section": "..."}], "ignored": 2}, "check": null, "fix": null}},
 "deferred": [{"round": 2, "id": "R2.7", "at": 211, "reason": "pre-existing", "anchor": "..."}]}
```

The ledger holds hashes and ranges, not document text, except the short anchors it needs to print the deferred list. Each round carries a `state` and an `attempts` counter for structural stops; a second structural stop in one review sets the terminal state `invalid` (section 4, tier 3). <!-- Source: Invariant probe INV-001 - merged per Change #15 (adopted, not debated) -->

<!-- Source: Variant A (opus:architect), Section 4.4 and Variant C (haiku:qa), Sections 3 and 10 - merged per Change #21 -->
**Replay, lock and limits.** `begin` re-runs `check` on the recorded report (its `report_sha` must still match) against the recorded surface and recomputes the verdict and the blocking ids; any difference with `ledger.json` exits 6. All writes take an exclusive-create lock file in `<dir>`; symlinked state paths are refused. Inputs over 2 MiB, 100,000 lines or 1,000 machine lines exit 2 before the diff.

<!-- Source: Base (original, modified) - adjusted per Changes #9, #10, #11, #12, #13, #14, #15, #16 and #18 -->
## 4. The checker

**Model (borrowed from `sc-implement-protocol/refs/qa.md`): the reviewer proposes, the script derives.** In `qa.md` the reviewer writes `at=`, `anchor=`, the parent Reads the anchor back, writes `origin=` and derives the verdict ("nobody rewrites a recorded verdict"). Diffgate does the same for a document: the reviewer writes anchors, the script reads them back against the saved snapshot, computes `origin`, decides in scope or deferred, and derives `blocking` and `verdict`. The reviewer's prose (experts, guard table, adversarial analysis) is untouched; the contract is one machine block in the report.

<!-- Source: Variant A (opus:architect), Section 4.1 - merged per Change #10 -->
**Report block (ASCII, one line per item, a line starts with its keyword at column 1). The block sits under the heading `## Diffgate findings`:**

```text
review: 2 of 3                                   (427 literal, kept; must equal the ledger round)
## Diffgate findings
PRIOR R1.5 resolved by=H2.2
PRIOR R1.9 open quote="still lets WC-7 skip the command file"
FINDING R2.1 sev=major at=60-63 hunk=H2.2 anchor="appears in that worker's worker-read output" outcome="correct launcher runs are recorded as WC-1 not exercised" :: AC-0.4 reads the wrong source
FINDING R2.2 sev=minor at=223 hunk=H2.6 anchor="--output <dir> by default" :: index-repo has no such flag
FINDING R2.3 sev=major at=312 via=H2.3 via_quote="7.2 step 1 --worktree current" anchor="places the worker in the current worktree" outcome="..." :: H2.3 now assumes an own worktree
FINDING R2.4 sev=minor at=140 cites=R1.9 anchor="..." :: more evidence for R1.9
```

The line forms are: `PRIOR <id> resolved by=H<k>.<n>`, `PRIOR <id> open quote="..."`, `PRIOR <id> regressed by=H<k>.<n> quote="..."`, `PRIOR <id> withdrawn quote="..." reason="..."` (Change 18), `FINDING <id> sev=<s> at=<line or a-b> hunk=H<k>.<n> anchor="..." outcome="..." :: text`, with optional `via=H<k>.<n> via_quote="..."`, `cites=<id>`, `fr=8|9|10` and `side=old` (a finding that anchors through `via=` or `cites=` instead of a hunk omits `hunk=`, as rule C11 allows), and the single line `FINDINGS none` when there is no finding. The reviewer writes no `verdict:` line (Change 12).

Keys: `sev` (`critical|major|minor`), `at` (line or range in the snapshot the reviewer read, `doc-r<N>.md`), `hunk` (a surface hunk), `via` + `via_quote` (an unchanged line broken by a changed hunk), `cites` (a prior id), `fr` (`8|9|10`, kept from 427's Guard Condition Boundary Table rule), `side=old` (the anchor is removed text in the baseline), `anchor`, `outcome`, `quote` and `reason` (JSON strings, so any character can be quoted and parsing is unambiguous: `json.loads` on the token), then `::` and a short text. Finding ids are `R<round>.<j>` with `j` counting from 1 with no gap; the script owns the format so ids never collide across rounds.

**Rules, in the order the script applies them.** "Hard" = the report is rejected (exit 1). "Soft" = the script fixes it by itself and records it in `result-r<N>.json`.

| # | Rule | Kind | On violation |
|---|---|---|---|
| C1 | The report has `review: N of 3` equal to the ledger round, and either FINDING lines or the single line `FINDINGS none` (the reviewer writes no verdict; Change 12) | hard | `E-ROUND`, `E-FORMAT` |
| C2 | Every `FINDING` and `PRIOR` line parses; no unknown key; ids are `R<N>.<j>` contiguous | hard | `E-FORMAT` |
| C2b | Every `R<N>.<j>` token anywhere in the report (prose included) is the id of a `FINDING` line, so a finding written only in prose cannot slip past the reviser's list | hard | `E-FORMAT` |
| C3 | The spec's sha equals the sha `begin` recorded (nobody edited the spec during the review) | hard | exit 5 |
| C4 | `at` lies inside the snapshot (1..number of lines) | hard | `E-AT` |
| C5 | **Anchor Read-back**: the whitespace-collapsed `anchor` (12 to 200 characters, no shorter waiver) occurs on the lines `at` names, in the snapshot side named by `side` (new side unless `side=old`). Every `anchor` and `via_quote` in a line is checked; one failing anchor fails the line <!-- Source: Variant A (opus:architect), rule C5 and Variant C (haiku:qa), Section 4 step 4 - merged per Change #11 --> | hard | `E-ANCHOR` |
| C6 | `hunk=H<k>.<n>` names a hunk of this round's surface; from review 2, the occurrence C5 found on the `at=` lines overlaps at least one changed token (or removed token for `side=old`) of the cited hunk, and `via_quote` must overlap a changed token of the `via` hunk; in review 1 there is no surface and `hunk`, `via` are not allowed <!-- Source: Variant A (opus:architect), rule C5 and Variant C (haiku:qa), Section 4 step 4 - merged per Change #11 --> | hard | `E-HUNK` |
| C7 | `via=H<k>.<n>` names a surface hunk and `via_quote` is a substring of that hunk's new text | hard | `E-VIA` |
| C8 | `cites=` names a prior blocking id in the ledger (or an earlier finding id of the same report) | hard | `E-CITES` |
| C9 | The `PRIOR` rows are exactly the ledger's prior blocking ids, once each; `regressed` is allowed only for an id an earlier round marked `resolved`; `withdrawn` is allowed only for an id with a `declined` line in `fixmap-r<N-1>.txt`. A withdrawn id leaves the open blocking set, stays in `R3-proxy-all` at its recorded label (section 9), and sets `acceptance: scoped` <!-- Source: Invariant probe INV-004 - merged per Change #18 (adopted, not debated) --> | hard | `E-PRIOR` |
| C10 | `PRIOR <id> resolved` carries `by=H<k>.<n>`, a hunk of this surface; with an empty surface nothing can be resolved. `PRIOR` lines carry no severity field: a prior keeps the severity and blocking status recorded when it was raised, and `regressed` re-opens an earlier id at its recorded severity <!-- Source: Variant A (opus:architect), rules C8 and V4 - merged per Change #16 --> | hard | `E-PRIOR` |
| C11 | Scope (review >= 2): a finding is in scope iff it has a valid `hunk=`, or a valid `via=` (at most 2 per review). Else if it has a valid `cites=` it is attached to that prior id as evidence and adds no blocking count. Else it is recorded `deferred: pre-existing` | soft | `deferred` |
| C12 | Blocking: an in-scope finding is blocking iff `sev=critical`, or `fr` is 8 or 9, or `sev=major` with an `outcome` other than `-`; otherwise it is minor (427 grading, bullet 2, made checkable; no length constant) <!-- Source: Variant A (opus:architect), Section 4.1 - merged per Change #13 --> | soft | `downgraded: no-outcome` |

<!-- Source: Variant A (opus:architect), Section 8.1 bullets 3 and 8 and Variant C (haiku:qa), Section 4 step 8 - merged per Change #12 -->
**The reviewer writes no verdict; the script prints it.** The derived verdict is `FAIL` iff any in-scope blocking finding or any prior with `open` or `regressed` exists; else `PASS`. `check` prints it as `verdict_line`; the command removes any `verdict:` line the reviewer wrote and appends `verdict_line` as the report's last non-blank line (placement in Change 22).

**Origin is computed, never typed.** `origin=changed` when C11 accepts the finding through `hunk=`; `origin=unchanged` for `via`, `cites` and deferred findings. The reviewer no longer writes `origin=`. The 427 vocabulary (`origin=changed|unchanged`, `resolved|open|regressed`) is kept in `result-r<N>.json` and in the command text.

**What happens on a reject (one answer, three tiers).**

1. Citing neither a hunk nor a prior id is not a reject. It is a normal soft outcome: the finding goes to `deferred.md` (rule C11) and can never be blocking after review 1.
2. A hard violation (C1 to C10): `check` exits 1, writes `reject-r<N>.txt` with one line per violation (`E-ANCHOR R2.3: anchor text not found on lines 211-212`) and changes nothing else. The reviewer repairs only those lines in the same session and reruns `check` once. That costs one tool call and no new session.
3. Still hard violations on the rerun: a finding-level violation (C2, C4 to C8) moves that finding to `deferred: unanchored`; a missing `PRIOR` row counts as `open`; `degraded: yes` is recorded (written to the ledger, printed by `check`, and repeated in the end-of-loop summary). A structural failure (no parseable `## Diffgate findings` block, no `FINDING` lines and no `FINDINGS none`, an `R<k>.<j>` id in the prose missing from the block (C2b), or a `review:` line that disagrees with the ledger) ends the run with no verdict. State after a structural stop: round N stays in state `open` with `attempts: 1`; one more `begin` for the same N is allowed and reuses `doc-r<N>.md` and `surface-r<N>.md` unchanged; a second structural stop sets the terminal state `invalid`; every later subcommand exits 4 with `halt: invalid`; the coordinator escalates to the user; the recorder counts the replicate as a failed attempt (section 9). <!-- Source: Invariant probe INV-001 - merged per Change #15 (adopted, not debated) --> Fail-safe means a lazy report can add an `open` prior (a spurious blocker) but can never smuggle in an unanchored blocker. <!-- Source: Variant A (opus:architect), Section 4.3 and Variant C (haiku:qa), Section 6 - merged per Change #14 -->

**Scoped acceptance.** `check` sets `acceptance: scoped` and prints the line `scoped PASS: <n> deferred, degraded or withdrawn blocking-grade findings are listed below` above the Reviser brief and verdict whenever the derived verdict is PASS and any finding labelled critical or major, or blocking-grade under the profile, was deferred, degraded, demoted, over the `via` cap (`reason=via-cap`), or withdrawn (Change 18); otherwise `acceptance: clean`. The verdict line is exactly `verdict: PASS` in both cases. Only `acceptance: clean` can earn the bar's clean-PASS alternative. <!-- Source: Variant C (haiku:qa), Section 6 and debate round2-B.md A-W3 and C-W3 - merged per Change #14 (resolves INV-028) -->

**What the checker proves, and what it does not.** It proves the reviewer's findings point at text that exists, inside a region the script computed, and that the counts and the verdict follow from those pointers. It does not prove the finding is true, that the `outcome` sentence is a real wrong outcome (only that it is present), or that a `resolved` mark is correct (only that it names a hunk of this surface). Those stay judgement, with the residual risks listed in sections 7 and 10.

<!-- Source: Base (original, modified) - adjusted per Changes #4, #8, #17, #18, #19 and #28 -->
## 5. Convergence rule for fix-induced defects on changed lines

Fix-induced defects on changed lines are in scope: a fix that breaks something must be caught. The design does not hide them. It makes four things true so they cannot regenerate without limit.

**5.1 Reviewed once, by construction (no rule to obey).** Review N+1's surface is the diff between the document review N saw (`doc-r<N>.md`) and the document after fix N. So:

| Line state | Where it can be reviewed |
|---|---|
| changed by fix N | review N+1 only |
| unchanged since the document review N saw | never again, unless a later fix changes it (then in that later review only) |
| in the original document and never changed | review 1 only; a defect found later is `deferred: pre-existing` (section 6) |

A defect on a line fix N changed that review N+1 misses is not reopened in review N+2. That is a deliberate loss: it is what stops the loop from re-attacking text it has already judged. Cost of the loss: section 10, R2.

**5.2 The fix gate: every hunk owned by a blocking id (mechanical).** `fixcheck` runs the same diff as the next `begin`, then reads `fixmap-r<N>.txt`. <!-- Source: Base (original, modified) - adjusted per Change #19 (debate round2-B.md; invariant probe INV-024, INV-003, INV-009) --> The first line of the map is `doc_sha: <sha>` as printed by the last `fixcheck`; a mismatch with the current spec exits 1 ("the map was written against another document"). The other lines are `H<k>.<n> R<N>.<j>[,R<N>.<m>...]` (one hunk may name several blocking ids) and `declined R<N>.<j> <reason>`. `fixcheck` pre-fills the map's candidates from inline `R<N>.<j>` tags in added text; the reviser confirms them or writes `declined`, and the file stays the authority. It exits 1 unless all hold:

- M1. Every fix hunk is claimed by at least one id, and each id is a blocking id of the round (a new blocking finding or a prior `open|regressed`). A hunk that fixes a minor finding, a citation note or a "related defect" has no valid id, so it is rejected. The reviser reverts it by hand, or maps it to the blocking id it genuinely repairs (a root cause that appears in several places is several hunks mapped to one id, so the 427 "root cause once, in every section that states the rule" practice stays allowed).
- M2. Every blocking id has at least one hunk or a `declined` line with a reason. A declined or untouched id stays `open` and is printed on the next surface. A declined id is the only id the next reviewer may mark `PRIOR <id> withdrawn quote="..." reason="..."` (rule C9); a withdrawal leaves the open blocking set but turns a PASS into a scoped PASS that cannot earn clean-PASS credit. <!-- Source: Invariant probe INV-004 - merged per Change #18 (adopted, not debated) -->
- M3. Ids and hunk ids exist; a hunk appears on one map line only (several owners go on that one line).

After the third failing `fixcheck` in one fix cycle the ledger records `fix-rejected` for that cycle, the reviser stops, the coordinator escalates to the user, and no review is consumed.

On exit 0 the script records and prints `bytes_by_id` and `hunks_by_id` as figures only; there is no byte budget and no size gate. The next surface header prints the largest fix so the reviewer looks harder at it. A size gate would not have fired where it mattered: in flg-r1, R2-2 and R2-3 changed three lines each and each produced a review-3 blocker. A hunk that adds a Markdown heading is printed as `new_section: H<k>.<n>`, because 427 bullet 6 forbids a section no blocking finding calls for (warning only). <!-- Source: Variant A (opus:architect), Section 5 and Section 3.3 - merged per Change #17 -->

This removes cause 2 of section 1. The reviser's task list is `reviser-brief-r<N>.md`, which holds only blocking ids, so minors never reach it.

**5.3 Chains are recorded, so a regenerating defect is visible.** The surface prints `fixes: R1.5` on the hunk that repaired R1.5. A review-2 finding anchored in that hunk is stored as a child: `chain: R1.5 -> R2.1`. A review-3 finding on a fix-2 hunk extends it: `R1.5 -> R2.1 -> R3.2`. The end-of-loop summary prints every chain. A chain of length 3 is the signature of a defect that automatic fixes cannot close; the summary then says "revise this region by hand" instead of "run another cycle". This is reporting, not a stop rule, and is cheap (`fixes` is already in the ledger).

**5.4 What stops regeneration (the honest list).**

1. The cap, unchanged and pinned: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` (`tests/skills/test_review_severity_rule.py:215`). `begin` enforces it (exit 4 for a fourth review).
2. The surface shrinks with the fix. Review N+1 can raise a blocker only on the lines fix N changed (plus at most 2 `via` findings). With the fix gate, those lines are at most the hunks mapped to blocking ids, not the whole 76 KB document. In the `flg-r2` replay the round-2 revision changed 25 lines; the gate removes the minor-only and citation lines and keeps every line that carries a blocking id.
3. No "exposed by" route except `via`, which is capped and logged.
4. No severity ceiling at review 3. I considered "a review-3 finding that cites no prior id cannot be blocking" and rejected it: it would turn the last review into a rubber stamp for exactly the fixes with the least review, and it would improve the measured metric by relabelling rather than by converging. If the fix gate and the surface are not enough, the data should say so (section 9).

**5.5 Not claimed.** Diffgate does not lower the per-fix rate of induced defects. It lowers the number of fixes (cause 2), removes re-review noise (cause 4) and makes the remainder countable. In `flg-r1` the gate removes only R3-7 from the review-3 proxy; the four blockers on blocking-fix text stay (section 9). <!-- Source: debate/evidence-flg-r1.md and Round 2 consensus - merged per Change #28 -->

<!-- Source: Base (original, modified) - adjusted per Changes #10, #14, #22, #23 and #34 -->
## 6. Pre-existing defects review 1 missed

**Rule.** In review 1 the whole document is in scope. From review 2 on, a finding that cites no valid hunk, no valid `via` and no prior blocking id is recorded `deferred: pre-existing` by the script (rule C11), is never blocking whatever its `sev` label, and never enters a surface, a reviser brief or a later `PRIOR` table.

**Format (`deferred.md`, written by every `check`, cumulative):**

<!-- Source: Variant C (haiku:qa), Section 6 - merged per Change #23 -->
```text
# diffgate deferred list (not looped on)
PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated.
loop: <dir>   spec: <spec>   rounds checked: 3   items: 4   degraded: no
D1  round 2  R2.7  sev=major(label)  at=211  reason=pre-existing   seen: rounds 2,3
    anchor: "AC-C1 regex still matches README.md:216"
    note:   <the reviewer's :: text>
D2  round 3  R3.5  sev=minor  at=96   reason=unanchored (degraded report)
...
```

**Surfaced once.** `check` prints only a count (its `deferred` field) while the loop is open, so no worker in the loop reads the text. At the closing review (a derived `PASS`, or review 3) the command writes `deferred.md` in full, once, under the heading `## Deferred (pre-existing, not looped on)`, above the Reviser brief and the verdict line. Report order at a closing review: findings block, `## Deferred (pre-existing, not looped on)`, the scoped-PASS line if any, the Reviser brief (reviews 1 and 2 only), then the verdict line. The last non-blank line of every report is the verdict line. <!-- Source: Invariant probe INV-027 - merged per Change #22 (adopted, not debated) --> The coordinator passes that block to the user together with the open blocking findings. When `check` reports `acceptance: scoped`, the scoped-PASS line of section 4 is printed with the list, so a PASS that left blocking-grade findings deferred, degraded or withdrawn is never presented as clean. A deferred id is not a legal `cites=` target (rule C8 accepts blocking priors only), so a later reviewer cannot launder a deferred item into a blocker by citing it. The same finding deferred in two rounds is one entry with `seen: rounds 2,3`; the deduplication key is the anchor text plus the whitespace-collapsed `::` text, so distinct issues on the same quote stay separate rows. The R3 proxy never reads this deduplicated list (section 9). <!-- Source: Variant C (haiku:qa), Section 6 - merged per Change #23 -->

**What the user can do with it.** Fix by hand, or start a new loop with a new `--diffgate-dir`: its review 1 is a full-document review, so those defects return as ordinary first-review findings. That is the only road back in, and it needs a human decision, which is the point.

**What keeps this from blinding the reviewer.** 427's one safety valve is kept in a bounded form: an unchanged line may be raised as a blocker only through `via=H<k>.<n>`, where the finding quotes the changed text it depends on and the quote is checked against the hunk (rule C7), at most 2 per review. Everything else about untouched text is deferred, not lost: the full list is shown, with the reviewer's own severity label, so a human can see if the loop is hiding something that matters. Expected size: 89% of review-2 findings were `origin=changed` in the S1 reports, so roughly one in nine findings lands here, about one or two items per review.

**Residual risk (prose, not mechanical).** The reviewer decides whether a defect "depends on" a changed line (`via`); the script checks the quote exists, not that the dependency is real. A reviewer can under-use `via` (miss a real cross-reference regression) or over-use it (the cap of 2 bounds the damage). Section 9 measures it with the blindness audit, a fresh whole-document review of the final spec.

<!-- Source: Base (original, modified) - adjusted per Changes #4, #13, #16 and #25 -->
## 7. Comparison with PR 427's --re-review and --baseline flags

427 (`## Review Loop` bullets 1 to 7 plus the `--re-review <prior-findings-file> --baseline <saved-copy>` Usage flags) gives a model the rules. Diffgate keeps all seven bullets and their literals and moves the mechanical parts into a script. Arm B (427 plus its own flags) showed the flags are honoured in form (status table, `origin=` tags, `review: N of 3`), so the comparison below is about who computes and who checks, not about wording.

<!-- Source: Variant A (opus:architect), Section 7 - merged per Change #25 (427 bullet column; rows changed by Changes #12 and #16) -->
| 427 bullet | Concern | 427 with flags | Diffgate | Still prose after diffgate (residual risk) |
|---|---|---|---|---|
| 1 Mode | Saved baseline | The coordinator saves a copy and passes `--baseline`; a dropped flag silently starts a fresh first review | `begin` snapshots the spec to `doc-r<N>.md`; the coordinator carries only the directory | Coordinator may pass a wrong or fresh directory; `--expect-round` catches it only if the brief includes it (R9) |
| 5 Re-review output | The diff | The reviewer runs its own `git diff --no-index -w` and may skip or misread it | Computed once by the script, with hunk ids, section names and a reflow filter; the reviewer reads `surface-r<N>.md` | The reviewer can still read the whole document as context and be influenced by it |
| 5 Re-review output | `origin=` | The reviewer self-tags | Computed from the anchors (rule C11) | None for the tag; the reviewer chooses which hunk to cite |
| 5 Re-review output | Scope of a finding | Bullet 5: an `origin=unchanged` finding is a minor note unless it quotes the changed line it depends on; reviewer judges | A finding with no valid hunk, `via` or prior id is deferred; `via` is quote-checked and capped at 2 | Whether a real dependency exists (judgement) |
| none | Findings point at real text | Not checked | Anchor Read-back against the snapshot (C5) | A finding can be anchored and wrong |
| 5 Re-review output | Prior-findings table | Reviewer writes `resolved\|open\|regressed` | Rows must equal the ledger's prior set; `resolved` must name the fix hunk with `by=H<k>.<n>`; severity is pinned when a finding is raised (C9, C10) | A named hunk did not really fix the finding: `resolved` is still the reviewer's call |
| 2 Grading, 3 Verdict | Blocking and verdict | Reviewer grades and writes the last line | Script derives blocking from checkable fields (C12) and prints the verdict line; the reviewer writes no verdict and the command appends the script's `verdict_line` as the last line | Whether `outcome` is a true wrong outcome (only presence is checked) |
| 4 Cap | Review count and cap | A header the coordinator carries; "nothing enforces the count" (design doc section 12) | Ledger round; `begin` exits 4 for a fourth review or after PASS | None for the count; the cap text stays pinned |
| 6 Reviser contract | Reviser contract | Bullet 6: "revise only text a blocking finding names", restated in a brief | `fixcheck` rejects any fix hunk without a blocking id; the reviser's task list is script-written (M1 to M3) | The reviser can map an unrelated edit to a blocking id (the map is auditable, not verified), and can skip `fixcheck`, which stops the next `begin` |
| none | Order of steps | None | Each step's output is the next step's only input; out-of-order calls exit 5 | A coordinator that hand-edits `ledger.json` or the files in `<dir>` |
| 5 Re-review output | Pre-existing defects | Minor note in the report | `deferred.md`, shown once at the end | Deferred severity labels are the reviewer's |
| 5 Re-review output | Re-check of prior blocking findings | rf-qa Fix Cycle steps 1 to 5 followed "first" | Kept as is in bullet 5 of the variant; the script checks only the table's shape | Same as 427 |

**What 427 leaves to prose that this makes mechanical:** the diff, the tag, the baseline copy, the review count, the verdict, the "resolved" sanity check, the reviser's scope, and the step order. **What stays prose:** whether a finding is true, whether a fix is good, whether a `via` dependency is real, whether a coordinator hands over the right directory, and whether any worker obeys the command at all before the first lock point (a reviewer that never runs `begin` is caught only at `check`, a reviser that never runs `fixcheck` only at the next `begin`).

**Net, in lines of prose.** The variant replaces bullet 5's "lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`" with a pointer to the surface file, and adds one `## Diffgate` section of single-line steps. Prose goes down in bullet 5 and 6 and up by the new section; the net rule count the model must obey drops from about eleven judgement duties to three (grade honestly, quote honestly, map honestly). That count is my estimate, not a measurement.

<!-- Source: Base (original, modified) - adjusted per Changes #26 and #32 -->
## 8. Exact changes, file by file

Transformation path (minimal risk, each stage independently revertible):

- **Stage A, inert:** add the skill folder, script and script tests. Nothing references them. Revert: delete the folder.
- **Stage B, the experiment arm:** add the variant command, its text tests and the one test-helper exception. `/sc:spec-panel` and the user-level `~/.claude/commands/sc/spec-panel.md` are not touched. Revert: delete the variant file.
- **Stage C, decided on the result class of section 9, never on the bar alone (a separate PR, not part of this change):** <!-- Source: Invariant probe INV-036 - merged per Change #32 (adopted, not debated) --> fold the `## Diffgate` section into `spec-panel.md`, delete the `--re-review/--baseline` prose, and retire the variant. Not specified here.

Every file, subcommand, flag, constant and test named in sections 2 to 8 and 13 is PROPOSED and does not exist yet; existing files are cited with line numbers. <!-- Source: Variant C (haiku:qa), Sections 1 and 8 - merged per Change #26 -->

Everything below is Stage A and B. All paths are repo-relative to the checkout; every installed text names installed paths, never `src/superclaude/...` (project CLAUDE.md rule; checked by the grep in the last table row).

<!-- Source: Base (original, modified) - adjusted per Changes #1, #4, #5, #10, #12, #22 and #24 -->
### 8.1 New: `src/superclaude/commands/spec-panel-diffgate.md`

A copy of `src/superclaude/commands/spec-panel.md` (486 lines, read in this worktree) made with `sed 's#/sc:spec-panel#/sc:spec-panel-diffgate#g'`, then these edits. Every other line is byte-identical to the original except the edits listed here, which keeps drift reviewable with `diff`.

1. Frontmatter line 2 `name: spec-panel` becomes `name: spec-panel-diffgate`; `description:` gains "with a computed re-review surface (diffgate variant)". Title line 10 becomes `# /sc:spec-panel-diffgate - Expert Specification Review Panel (diffgate variant)`.
2. Usage line 22: replace `[--re-review <prior-findings-file> --baseline <saved-copy>]` with `[--diffgate-dir <dir> [--expect-round N]]`. Line 23 only gets the renamed command.
<!-- Source: Variant A (opus:architect), Section 8.1 and Variant C (haiku:qa), Section 8 - merged per Change #24 -->
3. `## Review Loop` (line 256): bullet 2 and bullet 7's prefix stay literal. New or changed text (each bullet stays ONE physical line, like 427, so line-based matchers still see it whole):

```markdown
1. **Mode**: `--diffgate-dir` applies to `--mode critique` only and is required there; `begin` on an empty directory makes the run a first review of the full document and any later `begin` makes it a re-review; if a named file is unreadable or empty (script exit 3), stop and say which, and never fall back to a first review.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open), copied from the `verdict_line` that `check` prints; the reviewer never composes its own.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the round `begin` prints; a `begin` that exits 4 means do not review, HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--diffgate-dir` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps only the directory; the ledger keeps the count.
5. **Re-review output**: the reviewer reads `surface-r<N>.md` and does not re-review the document; context is read-only and cannot widen eligibility; first a `PRIOR` row per prior blocking finding `resolved|open|regressed` (`resolved by=H<k>.<n>`, `open quote="..."`, `regressed by=H<k>.<n> quote="..."`, where `regressed` = a finding the prior report marked resolved that fails again), or `withdrawn quote="..." reason="..."` for a finding the reviser declined; then `FINDING` lines whose `origin=changed|unchanged` the script computes, each anchored by a quote that overlaps a changed token of its hunk; a finding with no valid `hunk=`, `via=` or prior id is recorded `deferred: pre-existing` and is never blocking; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards inside the surface hunks only; an empty surface leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the script writes `reviser-brief-r<N>.md` (blocking finding ids only; omitted at `review: 3`, where the run escalates instead) and the report carries a `Reviser brief` just above the final `verdict:` line that names that file; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; write `fixmap-r<N>.txt` starting with the `doc_sha` line that `fixcheck` prints, map every changed hunk to the blocking ids it repairs, write a `declined` line with a reason for a blocking finding you will not fix, and run `fixcheck` to exit 0; the next review refuses to open while any hunk maps to no listed finding; each added paragraph or table cites its finding id; the reviser reports the byte size before and after.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the surface hunks and the prior blocking findings, and may not grade a minor finding as blocking.
```

The 427 literals pinned by `tests/skills/test_spec_panel_review_loop.py` stay: `CANONICAL_CAP_TEXT`, `HALT and escalate to the user with the open blocking findings`, `resolved|open|regressed`, `origin=changed|unchanged`, `verdict: PASS`, `verdict: FAIL`, `review: N of 3`, `Reviser brief`, `byte size before and after`, the rf-qa lookup order (project first).

4. New section inserted right after `## Review Loop` and before `## Output Formats` (single-line numbered items):

```markdown
## Diffgate

1. **Script**: run it as `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py <subcommand> ...`, else the project copy `.claude/skills/sc-diffgate/scripts/diffgate.py` (skills resolve the home copy first); if neither exists, stop with `E-DIFFGATE-MISSING` and never fall back to a plain review; it reads the specification and writes only inside the `--diffgate-dir`, never the specification. Under `--unattended` the directory defaults to `<report-dir>/diffgate`.
2. **Begin**: before any review run `begin --dir <dir> --doc <spec> [--expect-round N]`; exit 5 means a step was skipped, run the step `status` names; with no `surface-r<N>.md` in a re-review, stop.
3. **Review surface**: in a re-review read `surface-r<N>.md` and, as read-only context, the specification; findings may anchor only to a listed hunk (`hunk=H<k>.<n>`), to an unchanged line a listed hunk breaks (`via=H<k>.<n> via_quote="..."`, at most 2), or to a prior blocking id (`cites=`).
4. **Finding lines**: write the `## Diffgate findings` block exactly as `~/.claude/skills/sc-diffgate/SKILL.md` defines (`PRIOR`, `FINDING`, `FINDINGS none`), with `anchor="verbatim text"` and, for a blocking `major`, `outcome="the concrete wrong outcome"`; every quoted value is a JSON string.
5. **Check**: run `check --dir <dir> --report <report>` last; on exit 1 repair only the lines it names and run it once more; remove any `verdict:` line the reviewer wrote and append the `verdict_line` that `check` prints, which is the verdict.
6. **Close**: at a derived PASS or at `review: 3`, write the open blocking findings with their `chain:`, then the whole `deferred.md` once under `## Deferred (pre-existing, not looped on)`, then the scoped-PASS line if `check` printed one, then the Reviser brief if any, and the verdict line last; a FAIL says `halt: escalate`.
```

5. `## Unattended mode` (line 451 onward): byte-identical apart from the command name. Its text is pinned for `spec-panel` by `tests/skills/test_worker_contract.py` (`UNATTENDED_EXPECT["spec-panel"]`, line 576); keeping it equal means the variant inherits a section already reviewed.
6. `## Boundaries`: unchanged ("Modify specifications without explicit user consent" stays true; the script cannot write the specification).

<!-- Source: Variant C (haiku:qa), Section 8 "Command text to add or replace" - merged per Change #1 -->
7. `## Tool Coordination`: delete the line that reads `src/superclaude/examples/release-spec-template.md`; add no replacement path.

<!-- Source: Base (original, modified) - adjusted per Changes #4, #5, #13, #17 and #27 -->
### 8.2 New: `src/superclaude/skills/sc-diffgate/`

```text
sc-diffgate/
  SKILL.md              (frontmatter name: sc-diffgate; description "Infrastructure skill ... Delegate-only, no slash command"; allowed-tools: Read, Bash; about 60 lines: purpose, subcommands, exit codes, report grammar, file formats of section 3)
  scripts/diffgate.py   (about 420 lines, stdlib only)
```

<!-- Source: Variant A (opus:architect), Sections 8.3 and 3.6 - merged per Change #27 -->
Script outline (names are proposals, not yet existing):

```python
#!/usr/bin/env python3
"""diffgate: computed re-review surface, anchor checker and fix gate. Stdlib only."""
import argparse, difflib, hashlib, json, os, re, sys
from pathlib import Path

CAP_REVIEWS = 3; MERGE_GAP = 2; VIA_CAP = 2; FORMAT = "diffgate/1"
PROFILES = {"spec-panel": {"sev": ("critical", "major", "minor"), "blocking": _spec_panel_blocking}}
EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = 0, 1, 2, 3, 4, 5, 6

def key(line): return " ".join(line.split())
def sha(text): return hashlib.sha256(text.encode()).hexdigest()[:12]
def read_text(path): ...                 # exit 3 on missing/unreadable/empty, names the path
def load_ledger(d): ...                  # exit 6 on parse error; {} -> fresh
def save_ledger(d, led): ...             # exclusive-create lock, tmp file + os.replace
def replay(ledger) -> None: ...          # re-run check on the recorded report; exit 6 on any difference

def tokens(lines) -> list: ...           # (text, line, start, end) per whitespace token
def diff(old_lines, new_lines, review):  # section 3 steps 1-5, both passes: line blocks, then tokens; returns (hunks, ignored)
    sm = difflib.SequenceMatcher(None, [key(l) for l in old_lines], [key(l) for l in new_lines], autojunk=False)
    ...                                  # reflow filter with structural check, token pass, merge gap<=2, number H<k>.<n>, ranges, section names
def quote_spans(doc, quote) -> list: ... # whitespace-normalized occurrences, for C5 and C6
def render_surface(n, hunks, ignored, priors, ctx=2): ...
def cmd_begin(a): ...                    # order checks, replay, fix-gate re-run, round number, snapshot, surface; exit 1/4/5/6
def parse_report(text): ...              # PRIOR / FINDING / FINDINGS none / review:; json.loads for quoted values
def check_report(parsed, led, n, snapshot_lines, hunks): ...   # rules C1-C12; returns (result, hard_errors)
def derive(parsed, profile, prior): ...  # blocking, statuses, verdict_line, acceptance, deferred
def cmd_check(a): ...                    # reject once, then degrade finding-level failures; structural stop sets attempts or invalid
def cmd_fixcheck(a): ...                 # rules M1-M3, doc_sha, pre-fill, bytes_by_id, hunks_by_id, new_section; fix-rejected after 3 failures
def cmd_status(a): ...
def main(argv=None): ...                 # argparse subparsers; prints one JSON object; returns exit code
if __name__ == "__main__": sys.exit(main())
```

Rough size by part: diff and surface 90 lines, report parser and rules 140, begin/fixcheck/status 80, ledger and I/O 40, raised by the token pass and replay to about 420 lines in total. If review of the diff exceeds 450 lines, cut `status` and the `new_section` warning first.

<!-- Source: Base (original, modified) - adjusted per Changes #1, #2, #3, #4, #17, #22 and #39 -->
### 8.3 Tests

| File | Status | Content |
|---|---|---|
| `tests/skills/test_diffgate_script.py` | new | Loads the script by `importlib.util.spec_from_file_location` (pattern of `tests/skills/test_workflow_archive.py:22-27`) and also runs it as a subprocess for exit codes. Cases: section 13, P0 <!-- Source: Base (original, modified) - case list moved to section 13 per Change #39 --> |
| `tests/skills/fixtures/diffgate/` | new | Three small synthetic documents (v1, v2, v3, about 60 lines each) and four reports (good, bad anchor, unanchored, degraded). A miniature replay of the `flg-r2` shape: five review-3 items of which two sit on minor-only lines and one is unchanged; the flg-r1-shaped fixture and the structural list-merge fixture of section 13 |
| `tests/skills/test_spec_panel_diffgate_command.py` | new | The variant file exists; has `name: spec-panel-diffgate`; its Usage names `--diffgate-dir` and not `--re-review`; `## Review Loop` has the seven bullets in order with the literals listed in 8.1 (imports `CANONICAL_CAP_TEXT`, `AT_CAP_CLAUSES` from `test_review_severity_rule.py` like `test_spec_panel_review_loop.py:15`); `## Diffgate` sits between `## Review Loop` and `## Output Formats` and names both script paths, home first; no `src/superclaude` string anywhere in the variant or in `sc-diffgate/` (`grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` check from project CLAUDE.md); `## Unattended mode` equals `spec-panel.md`'s after replacing the name; `spec-panel.md` still has its 427 Usage flags (guards "additive"); the last non-blank line of a closing report is exactly `verdict: PASS` or `verdict: FAIL` (Change 22); drift guard: every `## ` section body other than `Review Loop`, `Diffgate` and the frontmatter and Usage block equals `spec-panel.md`'s after the name replacement, with `## Tool Coordination` compared after the one deletion of 8.1 item 7 (R10); full P1 case list in section 13 |
| `tests/skills/test_worker_contract.py` | edit, additive | `_check_no_unattended_sections` (line 831) compares the set of command files that carry `## Unattended mode` with `UNATTENDED_COMMANDS` (set equality at line 837); a copied command would fail it (verified: lines 831-838, called at 1011 and 1124). Add `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}`; in `_check_no_unattended_sections` assert `set(have) == set(UNATTENDED_COMMANDS) \| set(UNATTENDED_VARIANTS)`; add the parametrized `test_variant_unattended_section_matches_parent`, which compares the variant's section from `_unattended_section(name: str) -> str` (line 853) with the parent's after the name swap. `UNATTENDED_COMMANDS` and `assert len(expect) == 31` (line 1564) stay untouched. The negative test at 1118-1126 (a scratch command with a section) still fails as before <!-- Source: Variant A (opus:architect), Section 8.6 - merged per Change #3 --> |
| `tests/recommend/test_routing_refresh.py` | edit, 1 line | `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-diffgate"}` (line 33), because line 648 asserts the shipped command files minus that set equal the refresh inventory's active commands <!-- Source: Variant A (opus:architect), Section 8.6 - merged per Change #2 --> |

Existing tests that scan the new files and must keep passing without edit (the two existing tests that need an edit, `test_worker_contract.py` and `test_routing_refresh.py`, are the rows above): `tests/skills/test_review_severity_rule.py` (scans `src`, `plugins`, `commands`, `agents`, `skills` for banned any-severity phrases and for a cap number above 2; the new text uses only "(3 reviews)" and "review: N of 3"). `tests/skills/test_spec_panel_review_loop.py` is parametrised over the two `spec-panel.md` copies only and is not affected. `tests/unit/test_cli_install.py` lists command names at lines 118 and 404; I did not verify whether it counts files in `src/superclaude/commands` (UNVERIFIED), so the implementer runs it first.

<!-- Source: Base (original, modified) - adjusted per Change #2 -->
### 8.4 Docs, mirror, sync

- New `docs/designs/spec-panel-diffgate.md`: a short design record (decision, files, exit codes, residual risks, measurement bar) that points at this spec. `docs/designs/spec-panel-review-loop.md` (427) is not edited.
- No edit to `HOW-WE-WORK.md` or the level-table test; one line in `test_routing_refresh.py` (8.3): the variant is an experiment arm, not a routed workflow. Adding a row would force the byte copy to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and the level-table test.
- Plugin mirror: none. `plugins/superclaude/commands/` holds 28 files against 48 in `src/superclaude/commands/` (counted), and `plugins/superclaude/skills/` holds four skills, so mirroring is not the rule for newer primitives. Whether any test requires a mirror for a new command is UNVERIFIED.
- `make sync-dev` copies the command and the whole skill folder (script included) into `.claude/`; `make verify-sync` then passes. `.claude/` stays unstaged (project rule).

<!-- Source: Base (original, modified) - adjusted per Changes #5, #33 and #36 -->
### 8.5 Install note and the brief substitution an experiment needs

Workers load `/sc:<name>` from `~/.claude/commands/sc/`; the project copy is ignored (AB-REPORT "Machine facts"). The experiment adds files and edits none:

```bash
cp src/superclaude/commands/spec-panel-diffgate.md ~/.claude/commands/sc/spec-panel-diffgate.md
mkdir -p ~/.claude/skills/sc-diffgate
cp -R src/superclaude/skills/sc-diffgate/. ~/.claude/skills/sc-diffgate/
sha256sum ~/.claude/commands/sc/spec-panel-diffgate.md ~/.claude/skills/sc-diffgate/scripts/diffgate.py   # record in the run log
sha256sum ~/.claude/commands/sc/spec-panel.md   # must equal the value recorded before the run; check after each step
```

<!-- Source: Variant A (opus:architect), Section 8.9 - merged per Change #36 -->
The untouched `spec-panel.md` hash is recorded before the run and checked after each step; the pre-run gate of section 9 also checks permissions, one checkout per replicate, and command resolution after restart.

`superclaude install` would also add the new names (it keeps existing files unless `--force`; UNVERIFIED for skills), but `cp` is explicit and cannot touch `spec-panel.md`; never pass `--force` during an experiment. Brief changes, with `<DIR>` one directory for the whole loop (for example `<report-dir>/diffgate`):

```bash
# review briefs 2 and 3 (they carry 427's flags today): name and flags
sed -E -e 's#/sc:spec-panel( |$)#/sc:spec-panel-diffgate\1#g' \
       -e 's#--re-review [^ ]+ --baseline [^ ]+#--diffgate-dir <DIR> --expect-round <N>#g' brief.md
# review brief 1 (no flags today): rename and append by hand
#   /sc:spec-panel-diffgate @<spec> --mode critique ... --diffgate-dir <DIR> --expect-round 1
```

Reviser brief (both fix cycles), one added line: "Your task list is `<DIR>/reviser-brief-r<N>.md`, not the whole report; after editing write `<DIR>/fixmap-r<N>.txt` and run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py fixcheck --dir <DIR> --doc <spec>` until it exits 0." Record the substitution in the coordinator log, as AB-REPORT requires for a name change, and publish the exact before and after text of every changed brief line in the run log (the S1 treatment is the script plus this brief diff, section 9). <!-- Source: Invariant probe INV-034 - merged per Change #33 (adopted, not debated) --> Whether the S1 workers may run `uv run` from the home skill folder under their permission mode is UNVERIFIED; the pre-run gate (section 9) settles it before any replicate.

Check before commit (installed primitives name installed paths only): `grep -rn 'src/superclaude' src/superclaude/commands/spec-panel-diffgate.md src/superclaude/skills/sc-diffgate` must print nothing.

<!-- Source: Base (original, modified) - adjusted per Changes #18 and #28 to #37 -->
## 9. Measurement plan on scenario S1

**Design.** Scenario S1 exactly as in `AB-REPORT.md` and `ARMB-REPORT.md`: Orca worker-contract spec (57,763 bytes), base commit 2cb683f5, model claude-opus-5-5, three reviews, two fix cycles, the same verbatim briefs with the substitution of section 8.5 and the reviser line. Two replicates (`dg-r1`, `dg-r2`). Compared with the existing control (R3 proxy 8 and 4, mean 6.0; growth 57.7 and 69.3%, mean 63.5%) and Arm B (R3 proxy 6 and 1; growth 27.8 and 32.1%). Same caveats as Arm B: control not concurrent, n = 2 against 2, a screen for a large effect only. `WORKER-CONTRACT.md` moved aside as in the earlier arms. The bar is the one already pre-registered (D10, D11) and is not changed here. The treatment is the script plus the brief diff published in 8.5. A pass does not support "mechanical over prose"; that claim needs a briefs-only arm with the same brief lines and no script. <!-- Source: Invariant probe INV-034 - merged per Change #33 (adopted, not debated) -->

<!-- Source: Variant A (opus:architect), Section 8.9, Variant C (haiku:qa), Section 8, base question 12.1, invariant probe INV-010 and INV-006 - merged per Change #36 -->
**Pre-run gate (before any replicate).** (1) One worker in the experiment's permission mode runs `status` through the installed path without a prompt. (2) The reviewer and reviser workers of a replicate run in one checkout and pass the same `--doc` real path, checked by a dry `begin` and `status`. (3) A worker resolves `/sc:spec-panel-diffgate` after restart. Record `sha256sum` of `~/.claude/commands/sc/spec-panel.md` before the run and check it after each step; record the hashes of the new command and `diffgate.py`; never run `superclaude install --force`. Per replicate, the transcript must show the variant command and each `diffgate.py` call in step order.

**Counting rules fixed before the run.**

- Primary metric `R3-proxy-all`: one function applied to every arm's review-3 report and ledger: CRITICAL or MAJOR labels on (a) findings first raised in review 3, deferred and demoted included, and (b) prior blocking findings marked open or regressed in review 3, at their recorded label, each id counted once within review 3 only. Withdrawn priors (Change 18) count at their recorded label. The control (8, 4) and Arm B (6, 1) are recomputed with the same function, and the recomputed values are published beside the historical ones before any treatment replicate is scored. This keeps the reviewer-label reading of the AB reports and stops the arm from winning by deferring. Secondary: `R3-blocking-derived` (the script's blocking list) and 427-grade blocking. <!-- Source: Invariant probe INV-015 - merged per Change #31 (adopted, not debated) -->
- Withdrawn priors (`PRIOR <id> withdrawn`) leave the open blocking set but still count in `R3-proxy-all` at their recorded label. <!-- Source: Invariant probe INV-004 - merged per Change #18 (adopted, not debated) -->
- Growth: bytes of the spec after fix cycle 1 and 2 against the starting spec, as before.
- Validity gate (new): a replicate is valid only if `ledger.json` shows an accepted `check` for rounds 1 to 3 and an accepted `fixcheck` for rounds 1 and 2, the installed file hashes did not change (install watcher), and no worker read `origin/master`. Attempt slots are fixed before the run (two per arm). A replicate is void when the transcript and the ledger disagree, the state directory or run changes mid-loop, a state file was hand-edited (replay exit 6), plain `/sc:spec-panel` ran, or the run ended `invalid`. A void replicate is reported with its cost as a failed attempt, never scored and never silently replaced; any rerun is a separately declared decision. If a valid replicate's review-1 blocker count falls outside 13 to 17, the result is still scored but labelled "review 1 not comparable" and cannot be credited as evidence for the mechanism. Report the completion rate per arm. <!-- Source: Invariant probe INV-038, INV-039, INV-033, INV-019 and debate round2-C.md New evidence 5 - merged per Change #35 -->
- Extra recordings: rejects and `degraded` per review; deferred count and text; `via` use; fix hunks mapped, rejected and reverted; hunks per fix cycle; the F1 share of all-discovered review-3 critical+major findings by ledger ancestry (blocking-fix hunk, minor or unmapped edit, unchanged text); chain lengths; script calls and tool calls per step; wall time per step; reviewer session length; correction turns per rejected report; `fixcheck` failures per cycle and their reviser turns; the blindness-audit session; void or `invalid` attempts and their cost; coordinator dispatch time (section 10 cost table).
- Blindness audit (mandatory, out of loop, not counted in the bar): after the loop, one fresh `/sc:spec-panel --mode critique` review 1 of the final document per replicate, in a new session with no ledger, for every arm. Classify each blocker by ledger history: fix-written text the loop closed (what diffgate hides; feeds F3) or text present since the original. Report the second class beside the deferred count and compare it with the same audit on the control and Arm B final documents, so a drop in raised pre-existing defects is visible. Record findings per changed token per review (density). <!-- Source: Variant A (opus:architect), Section 9 "Blindness audit" - merged per Change #34 -->

<!-- Source: Debate round2-A.md, round2-B.md and round2-C.md, sections "flg-r1 evidence: revised prediction and any in-theme lever", and debate/evidence-flg-r1.md - merged per Change #28 -->
**Predictions, with reasoning (Round 2 consensus).**

| Metric | Control mean | Bar | Prediction | Reasoning |
|---|---|---|---|---|
| R3-proxy-all (critical+major in review 3) | 6.0 | 3 or fewer in both replicates, or a clean PASS | **about 3.0 to 3.5 mean** (a flg-r1-like replicate about 4 to 5: four blockers on blocking-fix text plus R3-8's MAJOR label, R3-7 removed; a flg-r2-like replicate about 1 to 2) | In flg-r1 all 4 review-3 blockers sit on text written by blocking fixes, and a blocking-only gate removes only R3-7 (`debate/evidence-flg-r1.md`). In flg-r2 the gate removes the minor-only and citation lines (section 1). Deferred items still count in the primary metric |
| Spec growth after two cycles | 63.5% | 44.4% or less | **about 20% to 27%** (P about 0.9 for the 44.4% bar) | Arm B was 27.8 and 32.1%; the fix gate removes minor-only edits. Early PASS: the terminal document is carried forward to the scheduled endpoint for growth |
| Clean PASS by review 3 | 0 of 6 runs so far (2 control, 2 treatment A, 2 Arm B) | not required | about 10% per replicate | A mapped fix still induced the blocker N12 in the flg-r2 replay and four blockers in flg-r1 |

Probability that both replicates are at 3 or fewer: about 0.2 to 0.25. Probability that F1 fires in at least one replicate: about 0.5 to 0.55. Probability the growth bar is met in both: about 0.9 (427 alone already met it).

No mechanism inside the diffgate theme (computed surface, anchor checker, fix gate, ledger) lowers the count of blocking-fix-induced blockers without relabelling or hiding them. In flg-r1 all 4 review-3 blockers sit on text written by blocking fixes, and a blocking-only gate removes only R3-7.

The experiment's most likely product is therefore a measured per-blocking-fix defect rate under scope control. The design's claim is "escalate with an interpretable record", not convergence.

**What result would mean the idea failed** (declared before the run):

<!-- Source: Base (original, modified) - F1 re-based and F3 replaced per Change #29 (Variant A (opus:architect), Section 9 conditions 3 to 5; debate round2-B.md) -->
1. **F1, wrong lever.** The R3 proxy is above 3 in a replicate and at least 70% of that replicate's review-3 critical+major findings sit on blocking-fix hunks by ledger ancestry (computed as below). The scope and fix gates worked as designed and the metric did not move: the driver is the per-fix defect rate, and the next idea must act on fix quality (for example a reviser self-check), not on scope.
2. **F2, no growth win beyond 427.** Growth above 44.4%, or mean growth not below Arm B's 30.0%: the fix gate did not constrain the reviser.
3. **F3, blinding.** The blindness audit finds 2 or more blockers in fix-written text the loop closed, in either replicate. Stop and revisit `via`.
4. **F4, too heavy.** In either replicate more than one review needs a second `check` run or ends `degraded: yes`, or a loop stalls on a script error: the grammar costs more than it returns.
5. **F5, demotion.** More than a quarter of new findings in reviews 2 and 3 are demoted or degraded, or the gate fails more than once per fix cycle on average.
6. **F6, stall.** A replicate stalls (no review 3 delivered).

The label proxy (`R3-proxy-all`) and the 427-blocking count are reported side by side for every replicate.

<!-- Source: Invariant probe INV-016 - merged per Change #30 (adopted, not debated) -->
**F1 share (pre-registered).** Compute the F1 share over all-discovered review-3 critical+major findings (blocking, deferred and demoted), each classified by ledger ancestry as on a blocking-fix hunk, on a minor or unmapped edit, or on unchanged text. In the treatment arm every blocking new finding sits on a mapped fix hunk by construction (the gate admits no unmapped hunk), so the blocking-only share is 100% and is not a diagnostic. The ancestry classification uses the ledger's per-hunk owners; for control and Arm B it uses the `disposition*.md` changed-line lists, as in `debate/evidence-flg-r1.md`.

Only F1 to F6 absent together and both replicates at 3 or fewer count as success. A mixed result (growth bar met, R3 bar missed) is reported as such, not rounded up.

<!-- Source: Invariant probe INV-036 - merged per Change #32 (adopted, not debated) -->
**Result classes (pre-registered).** Before any replicate: S1 at n=2 returns only one of three result classes (bar met; bar missed with F1; bar missed without F1). The spread check (Variant C, section 9: the reduction must exceed the larger within-arm spread, historical control spread 4) is reported; it can be met only if the treatment mean is below 2.0. A claim that diffgate has a proven effect requires a replicate count fixed before the first run.

<!-- Source: Base (original, modified) - adjusted per Changes #2, #13, #17, #21, #27, #34 and #37 -->
## 10. Costs and risks

**Costs per loop (three reviews, two fix cycles).**

| Item | Estimate | Basis |
|---|---|---|
| Extra tool calls, reviewer side | 3 per review (`begin`, read the surface, `check`), plus at most 1 rerun of `check` per review: 9 to 12 | counted from the steps in section 2 |
| Extra tool calls, reviser side | read the brief, write the map, `fixcheck` once or twice: 4 to 5 per cycle, 8 to 10 | same; the first `fixcheck` often rejects an unmapped hunk |
| Extra sessions | 0. Same three reviewers and two revisers | rejects are repaired in the same session |
| Script run time | well under 1 second each (a few hundred lines diffed with `difflib`) | S1 spec is about 317 lines |
| Correction turns per rejected report | 1 extra reviewer response and 1 `check` each <!-- Source: Variant C (haiku:qa), Section 10 "Cost envelope" - merged per Change #37 --> | section 4, tier 2 |
| `fixcheck` failures per cycle | each failure costs one reviser turn and one `fixcheck`; at most 3 runs per cycle, then `fix-rejected` | section 5.2 |
| Blindness-audit session | 1 fresh review session per replicate, for every arm | section 9 |
| Void or `invalid` attempts | each is reported with its full cost as a failed attempt | section 9 validity gate |
| Coordinator dispatch time | per review and per fix cycle, recorded per step | section 9 extra recordings |
| Wall time | a range: about 3 to 5 extra minutes per loop at 10 to 15 seconds per tool round trip with no correction turns, more for each correction turn, `fixcheck` failure and the blindness audit; UNVERIFIED until the step times are recorded | estimate, not measured. Parent Read-back and correction turns can cost more than the helper itself; this is not free and is not only Python run time |
| Offsetting saving | reviews 2 and 3 skip the whole-document pass and the prior-report re-read; `flg-r2` review 3 spent Part 1 (15 rows) and Part 2 (20 citation groups) first | UNVERIFIED that it saves more than it costs; section 9 records step times |
| Build cost | about 420 lines of script, about 60 lines of `SKILL.md`, about 25 script tests, one 490-line variant file, two small edits to existing tests (8.3) | section 8 |
| Debt added | a forked command (drift) and a ledger format | see R10 and R11 |
| Debt removed (on Stage C) | bullet 5 and 6 prose, `baseline: missing`, the coordinator's saved-copy duty, the self-typed `origin=` | section 7 |

**Ways the mechanism could make the loop worse, and what limits each.**

- **R1. Blinding the reviewer to a real regression.** A fix breaks text it did not touch (a cross-reference in another section). Limits: the specification stays readable as context; `via=` lets a blocker anchor to an unchanged line through a quote-checked hunk (2 per review); every deferred item is printed once with the reviewer's own label; the blindness audit (section 9) measures what was hidden. Residual: a reviewer that does not think to use `via`.
- **R2. Missed once is missed for good.** A defect on a fix-changed line that review N+1 overlooks is never reopened (section 5.1). That is the price of convergence; it is also why the end-of-loop deferred list and the blindness audit exist.
- **R3. A reviewer gaming the anchors.** It can cite a nearby changed hunk to make a pre-existing issue count. Limits: `at` must lie inside the hunk's range and the quote must be present on those lines; merge gap is only 2. Residual: semantic fit of the finding to the anchor is not checked.
- **R4. Diff noise.** A re-wrapped paragraph is dropped only when its words are identical; a re-wrapped and edited paragraph is one big hunk. A moved block appears as a deletion plus an insertion. A rewrite that changes most of the file makes the surface nearly the whole document. Limit: `begin` prints `coverage: <percent of new lines inside hunks>`, and above 50% the surface header says so (a 2-line addition to the script), so the coordinator sees the loop has degenerated into a full review. Residual: the script does not detect moves.
- **R5. The reviser gaming the fix map.** It can map an unrelated edit to a blocking id. Limits: the map is written down and printed with `bytes_by_id` and `hunks_by_id`; the next surface prints `fixes: R1.5` on each hunk, so the next reviewer sees what each edit claims to repair. Residual: nothing verifies the claim.
- **R6. Machine lines and prose drifting apart.** A finding written only in prose never reaches the reviser, because the reviser's list comes from the machine lines. Limit: an extra rule C2b, every `R<N>.<j>` token anywhere in the report must exist as a `FINDING` line (hard, `E-FORMAT`). Residual: a prose finding with no id at all.
- **R7. The script itself.** A bug, a missing `uv`, a worker permission mode that blocks `uv run` from `~/.claude/skills/...`, or a missing skill install stops the loop. There is deliberately no silent fallback to prose review, since that is today's failure; the command stops and says which path was missing. Limits: unit tests, the fixture replay, the install hash record, and exit 6 for a corrupt ledger (the script never repairs it).
- **R8. Report-format tax.** The machine block is new work for the reviewer; F4 in section 9 is the pre-registered check that it does not cost more than it returns. Fail-safe degrading can add a spurious `open` prior but never an unanchored blocker.
- **R9. Wrong or dropped directory.** A fresh directory restarts at `review: 1 of 3`. Limit: `--expect-round N` in the brief (exit 5 on mismatch). Residual: a brief without it.
- **R10. A forked command drifts from `spec-panel.md`.** Limit: the command test compares every `## ` section body that this change does not touch against `spec-panel.md` (added to row `test_spec_panel_diffgate_command.py` in 8.3), so an upstream edit breaks the variant's test instead of silently diverging.
- **R11. Ledger as new state.** Hand edits are detected by replay; concurrent writers are refused by the lock. <!-- Source: Variant A (opus:architect), Section 4.4 and Variant C (haiku:qa), Section 10 - merged per Change #21 -->
- **R12. Derived severity versus the reviewer's label.** A true major with no `outcome` becomes minor and cannot fail the loop. This is 427 grading bullet 2 made literal, but it can look like severity drift in reverse. Limit: the primary metric in section 9 uses the reviewer's labels, not the derived ones.

<!-- Source: Base (original, modified) - adjusted per Changes #4, #32 and #38 -->
## 11. Later adopters

The script is document-agnostic (text lines in, hunks and a ledger out), so it can serve other loops. None of the adoptions below is part of this change; each lists what it would need.

| Adopter | Fit | What it would need | Order |
|---|---|---|---|
| rf-qa agents (Fix Cycle, `~/.claude/agents/rf-qa.md`) | High. Same shape: a QA pass, a fix, a re-check of prior findings. Bullet 5 of the Review Loop already points the re-check at its steps 1 to 5 | rf-qa calls `begin` and `check` with its own report grammar (the `PRIOR`/`FINDING` block can be shared); the fixer calls `fixcheck`. rf-qa also checks task files and research output, so a second input kind (a file set) is likely. Adds an `rf-qa` profile (CRITICAL and IMPORTANT blocking, MINOR a note); must not weaken rf-qa's regression and monotonicity guards <!-- Source: Variant A (opus:architect), Section 11 and Variant C (haiku:qa), Section 11 - merged per Change #38 --> | first, after Stage C |
| `/sc:reflect` UC-2 (post-execution deviation audit) | Medium. The baseline is a git tree, not a saved copy, and the unit is several files | Multi-file surfaces: hunk ids prefixed by path, `--baseline-ref <sha>` instead of `doc-r<N>.md`; the deviation taxonomy (Authorized, Necessary, Drift, Regression) maps onto `origin` and `fixes:` | second |
| `/sc:implement` final review (`sc-implement-protocol/refs/qa.md`, archive gate in `refs/managed-workspace.md`) | Low as a replacement, medium as a shared checker. `qa.md` already has the parent derive the verdict, Read anchors back, cap inherited text from `git diff` hunk headers and track `resolved\|open\|regressed` | Do not replace the final review; at most a checked delta surface for a narrowly authorized repair after it, with a fresh full final review kept for archive acceptance. A later cleanup could let `qa.md` call the same anchor Read-back and hunk code instead of its prose description, which would remove duplicate rules <!-- Source: Variant C (haiku:qa), Section 11 - merged per Change #38 --> | last |
| `/sc:spec-panel` itself | The target of Stage C | fold `## Diffgate` into `spec-panel.md`, drop the 427 flags, move the pins in `tests/skills/test_spec_panel_review_loop.py`, and mirror into `plugins/superclaude/commands/spec-panel.md` (which differs from `src/`: it lacks the second Usage line, the `--target-release` paragraph and the whole `## Unattended mode` section, and line 219 reads `Native reasoning` where `src/` line 221 reads `Sequential`) | after the S1 result class (section 9) |

Reach, for scale: the AB report records that 427 reaches only `/sc:spec-panel`, and that of five recreated incidents only S1 used it (in 3 of 7 reviews, with no `--re-review` in the briefs); four of five incident types (`/sc:reflect`, plain agents, rf-qa agents, the `/sc:implement` final review) never call it. A script that rf-qa and `/sc:reflect` can also call is the only route in this proposal that reaches them, and it is worth little until the S1 result is in.

<!-- Source: Base (original, modified) - every question given a default or closed per Change #41 (Variant C (haiku:qa), Section 12) -->
## 12. Open questions

These questions do not leave the initial interface undefined. The default stated with each one governs the first experiment; changing it creates a recorded new treatment.

1. **Worker permissions: moved into the pre-run gate (section 9, item 1).** Whether an S1 worker can run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py` under its permission mode, and whether `uv` resolves offline with no dependencies, is settled by the gate's one-worker `status` run before any replicate. <!-- Source: invariant probe INV-010 - merged per Change #36 -->
2. **Does `Skill sc:spec-panel-diffgate` load a command the user-level folder holds only as an additive file?** The round-3 reviewer observed `Skill sc:spec-panel` loading `~/.claude/commands/sc/spec-panel.md`; the same for a new name is expected but not observed here. Default: the pre-run gate (section 9, item 3) checks that a worker resolves `/sc:spec-panel-diffgate` after restart; if it does not, no replicate runs.
3. **Hunk granularity.** Lines are the unit, merged at a gap of 2, with a section name; eligibility is token-level inside the changed lines. Section-level hunks would give more context and fewer false findings but a larger surface; paragraph-level units would help hard-wrapped specs. Default: line hunks with token-level eligibility (section 3); S1's spec has long single-line paragraphs, so lines fit, and no paragraph unit is used in S1.
4. **Closed: the byte budget is removed (section 5.2, Change 17).** `fixcheck` records `bytes_by_id` and `hunks_by_id` as figures only. `VIA_CAP = 2` is kept as a constant and its use is recorded in S1.
5. **Closed: the script owns the verdict (Change 12).** The reviewer writes no verdict; the command appends the `verdict_line` that `check` prints.
6. **Reviser sees blocking ids only.** The reviser no longer reads minors, which is the point, but a minor that is a typo-class fix is then left for a human. Default: no minor sweep inside the loop in S1; whether a separate sweep after the loop is wanted is a human decision.
7. **Closed: rejected reports (Change 14).** A report is repaired once; on the rerun, finding-level failures degrade and a structural failure stops the run with no verdict (section 4, tier 3).
8. **Reflow and moves.** Re-wrapped paragraphs are filtered when word-identical and the Markdown structure is unchanged (Change 20); moved blocks are not detected. Default: no move detector in S1; a moved block is a deletion plus an insertion.
9. **Does the fix map belong in the spec?** Mapping lives in a side file so the specification carries no review ids. In the S1 runs revisers wrote ids inline anyway ("every spec change carries its finding id inline"). Default: the side file is the authority, and `fixcheck` pre-fills its candidates from inline `R<N>.<j>` tags (Change 19).
10. **Where the script's ledger lives under `--unattended`.** `<report-dir>/diffgate` keeps `artifacts` in `return-contract.yaml` unchanged; whether WC-4's rule about git-ignored paths would want these files listed is UNVERIFIED. Default: `<report-dir>/diffgate`, not listed in `artifacts`.
11. **Unverified read of the existing test list.** `tests/unit/test_cli_install.py` names `spec-panel.md` in command lists at lines 118 and 404; I did not establish whether a new command file in `src/superclaude/commands/` changes any expected count there. Default: the implementer runs it first, as section 8.3 says.
12. **Answered: `flg-r1` composition.** `debate/evidence-flg-r1.md` shows that `flg-r1` does not share `flg-r2`'s composition: all 4 review-3 blockers sit on text written by blocking fixes, and a blocking-only gate removes only R3-7. The forecast in section 9 uses it.

<!-- Source: Variant C (haiku:qa), Section 13, with Variant A (opus:architect), Section 8.4 cases and the base 8.3 case list - merged per Change #39 -->
## 13. Test plan

Tests check behaviour, not only the presence of rule sentences. They use temporary directories and small byte-exact fixtures, and never touch the real user HOME. The file list is in section 8.3. Run every test with `uv run pytest`.

### P0: script cases (`tests/skills/test_diffgate_script.py`)

Diff and surface:

- A whitespace-only change is ignored; a word-identical re-wrapped paragraph is ignored.
- One changed word in a 300-character line yields one hunk whose changed span is that word.
- An edited line gives one hunk with the right new range; ranges are 1-based and inclusive.
- A pure deletion gives a hunk whose removed tokens can be anchored with `side=old`; the lines before and after are display context only.
- Two edits 2 lines apart merge into one hunk id, 3 apart do not; gap lines are never eligible.
- A 320-line input keeps the diff exact (the `autojunk=False` regression).
- Hunk ids are `H<k>.<n>` in document order and never repeat across reviews.
- Structural list merge: `1. First\n2. Second\n` to `1. First 2. Second\n` is kept as a hunk with `structural: yes` and needs an owner (Change 20).

Order and state:

- `begin` round 1 writes the snapshot and no surface; `begin` round 2 without an accepted fixcheck exits 5; a spec changed after fixcheck exits 5.
- `begin` round 2 re-runs the fix gate and exits 1 on an unmapped hunk (Change 6).
- A fourth review and a review after PASS exit 4; a wrong `--expect-round` exits 5.
- The structural-stop sequence: a first structural stop leaves the round `open` with `attempts: 1`; the second sets `invalid`; every later subcommand exits 4 with `halt: invalid` (Change 15).
- Replay detects a hand-edited `ledger.json` and exits 6 (Change 21); a corrupt ledger exits 6; a second writer is refused by the lock; inputs over the limits exit 2.
- The script never modifies the spec (sha equal before and after every subcommand).
- Every subcommand prints exactly one JSON object; an accepted FAIL review exits 0 with `verdict` FAIL (Change 7).

Checker:

- A valid report is accepted; `FINDINGS none` is accepted.
- An anchor not on the cited lines exits 1 `E-ANCHOR`; a fabricated hunk exits 1 `E-HUNK`; an anchor outside the changed span of its hunk is rejected.
- A quote that occurs in both changed and unchanged text counts only by its occurrence on the `at=` lines, which must overlap a changed token (Change 11).
- A line with one good and one bad anchor fails as a whole.
- A finding with neither a hunk nor a prior id is deferred and never blocking, even with `sev=critical`.
- `cites` attaches evidence and adds no blocker; `via_quote` not overlapping a changed token of its hunk exits 1 `E-VIA`; a third `via` is deferred with `reason=via-cap`.
- A missing `PRIOR` row exits 1 `E-PRIOR`; `resolved` without `by=` exits 1 `E-PRIOR` (Change 16).
- A major with outcome `-` or no outcome becomes minor (Change 13).
- A second failing submission degrades finding-level violations, sets `degraded: yes` and exits 0; a report with no findings block stops with no verdict.
- `acceptance: scoped` and the scoped-PASS line appear when a blocking-grade finding was deferred, degraded, over the `via` cap or withdrawn; the verdict line stays exactly `verdict: PASS`.
- `withdrawn` is legal only after a `declined` line in the previous fix map (Change 18).

Fix gate:

- `fixcheck`: an unmapped hunk exits 1; an unknown id exits 1; a hunk on two map lines exits 1; a blocking id with no hunk and no `declined` exits 1; `declined` is accepted; a new heading is flagged `new_section`.
- A two-owner hunk (`H<k>.<n> R<N>.<j>,R<N>.<m>`) is accepted (Change 19).
- A map whose `doc_sha` line differs from the spec exits 1; candidates are pre-filled from inline `R<N>.<j>` tags; the third failing `fixcheck` in a cycle records `fix-rejected`.
- `bytes_by_id` and `hunks_by_id` are reported as figures only; no budget is enforced.

flg-r1-shaped fixture (four mapped blocking fixes, four new blockers on them, one MAJOR graded minor on a shared line, one minor-only line). Expected: all four fix hunks allowed, the minor-only line rejected, chains of length 3, F1 fires, label proxy 5, blocking 4.

### P1: command, install and regression

- Command text test (`tests/skills/test_spec_panel_diffgate_command.py`): the literals of 8.1; both script paths, home first; no `src/superclaude` string; the last non-blank line of a closing report is exactly `verdict: PASS` or `verdict: FAIL` (Change 22); the drift guard with the `## Tool Coordination` exemption.
- The two existing-test edits: `tests/recommend/test_routing_refresh.py` (Change 2) and `tests/skills/test_worker_contract.py` (Change 3).
- An isolated temporary-HOME install test installs the command and `sc-diffgate`, runs the script's `--help` outside the repository, and asserts that a sentinel `spec-panel.md` is byte-unchanged.
- Run `uv run pytest tests/skills/test_diffgate_script.py tests/skills/test_spec_panel_diffgate_command.py tests/skills/test_worker_contract.py tests/recommend/test_routing_refresh.py` after implementation.

<!-- Source: Variant C (haiku:qa), Section 14, adapted to the merged design - merged per Change #40 -->
## 14. Acceptance criteria

Implementation acceptance is separate from experimental success. An implementer can check the following without reading the forecast in section 9 as evidence.

1. **Additive delivery without plugin mirrors.** The new command, the `sc-diffgate` skill folder with its script, the tests and the design record of section 8 exist. The source, plugin and installed `spec-panel.md` bytes stay unchanged. No plugin mirror is added (C-032). No real user installation is modified by tests.
2. **Portable invocation.** The script runs through `uv run --no-project python` at the installed `sc-diffgate` path from a temporary non-repository working directory, stdlib only. Lookup is home first, project copy second; with neither, the command stops with `E-DIFFGATE-MISSING`.
3. **Deterministic surface.** Repeated `begin` on identical state produces byte-identical surface and JSON output. Hunk ids `H<k>.<n>` never repeat. Saved snapshots, not Git refs or file times, decide eligibility.
4. **Strict scope, with deferral rather than report rejection for unanchored findings.** A finding with no valid hunk, `via` or prior id is deferred and never blocking (C-012). A gap or context line is not eligible. Deferred findings cannot authorize a fix or change the verdict.
5. **Deletion correctness.** A finding on a deleted requirement anchors its removed tokens with `side=old`. A deleted line cited as current is rejected.
6. **Report integrity.** Bad anchors, unknown hunks, missing or extra `PRIOR` rows, and prose ids missing from the block are rejected with diagnostics. `FINDINGS none` is a valid report.
7. **Script-derived verdict as the last line.** The reviewer writes no verdict. The last non-blank line of every report is exactly `verdict: PASS` or `verdict: FAIL`, copied from `verdict_line`.
8. **Fix ownership by explicit map.** Every fix hunk maps to at least one open blocking id, or `fixcheck` exits 1. The map carries the `doc_sha` line and `declined` lines with reasons. No footprints are required.
9. **One-look rule.** A changed line is reviewable only in the next review unless a later fix changes it again (section 5.1).
10. **Bounded execution.** At most three reviews and two fix cycles. One report repair per review. A second structural stop sets `invalid`; a third failing `fixcheck` in a cycle records `fix-rejected`; a later `begin` exits 4.
11. **Safe state.** The exclusive-create lock, symlink refusal, replay (exit 6) and input limits (exit 2) pass their tests. The script never writes the specification.
12. **Deferred disclosure.** The deferred list, with the sentence "PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated.", is shown once at an early PASS and at a capped FAIL. `acceptance: scoped` is set whenever section 4 requires it.
13. **Unattended compatibility.** The variant's `## Unattended mode` equals the parent's after the name swap; the loop directory defaults to `<report-dir>/diffgate`.
14. **Regression evidence.** The new test modules and the listed existing modules pass with `uv run pytest`, including the edits to `test_worker_contract.py` and `test_routing_refresh.py`. The `src/superclaude` scan of installed primitives finds no new reference. No static assertion is described as proof of live compliance.

Variant C's criterion 15 (the S1 screen) is not an implementation criterion; it is the pre-registered result classes of section 9.
