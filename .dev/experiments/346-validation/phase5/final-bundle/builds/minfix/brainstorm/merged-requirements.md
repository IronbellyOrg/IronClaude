---
source: nested/adversarial-1/merged-output.md
adversarial_status: partial
convergence_score: 0.96
note: "debate convergence blocked by 10 HIGH invariants at depth standard; base (sonnet:analyzer) force-selected by score; invariants carried into the merge"
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:analyzer) -->
<!-- Merge date: 2026-11-08T16:25:36Z -->

# Variant 2 (analyzer): fix-minimality budget with a mechanical checker (theme minfix, issue #346)

<!-- Source: Base (original, modified) — definitions line added per Change #35 -->
Persona: analyzer. Built on PR 427 (`## Review Loop`, 7 bullets). Evidence base: the six S1 loops (ctl-r1, ctl-r2, trt-r1, trt-r2, flg-r1, flg-r2), their reviews and dispositions, and word-level diffs of their spec history copies (analysis scripts were stdlib `difflib` run read-only; numbers below are mine unless a report is cited). Every claim I could not verify is marked UNVERIFIED.

Terms: D5 = metrics M1-M5 of the earlier A/B experiment design (rounds to clean pass, critical+major proxy per round, `origin=changed` share, size and growth, tool calls); D9 = the finding that parallel arms need different command names; D10/D11 = the earlier A/B experiment designs whose bar and validity checks V1-V6 this arm reuses; D12 = a record of the same experiment series (no gloss in any source, UNVERIFIED); FR-8/FR-9 = spec-panel's hard gates for guard-table rows and blank behaviour.

## 1. Problem and evidence

<!-- Source: Base (original); 1.6 minor-cap sentence modified per Change #3 / PR-M4 -->
### 1.1 What 427 fixed and what it left

427 (AB-REPORT, ARMB-REPORT, D10/D11/D12) cut spec growth after two fix cycles from 63.5% (control mean) to 29.7% (arm A) and 30.0% (Arm B). It did not move review-3 critical+major: control mean 6.0, arm A 5.5, Arm B 3.5 (r1 = 6, r2 = 1); no loop of the six reached PASS. Word-level diffs of the spec history copies confirm the growth picture and give the unit the budget needs (v1 = 8,148 words, 57,763 bytes, about 7.1 bytes per word):

| run | cycle 1 added / deleted / net words | cycle 2 added / deleted / net words | net growth after 2 cycles (words) | new headings (c1 + c2) | net normative words (c1 + c2) |
|---|---|---|---|---|---|
| ctl-r1 | 2,366 / 362 / +2,004 | 3,087 / 197 / +2,890 | +60.1% | 0 + 1 | +4 + 8 |
| ctl-r2 | 2,961 / 379 / +2,582 | 3,327 / 162 / +3,165 | +70.5% | 0 + 1 | +10 + 21 |
| trt-r1 | 1,152 / 201 / +951 | 1,064 / 84 / +980 | +23.7% | 4 + 0 | +4 + 7 |
| trt-r2 | 2,244 / 258 / +1,986 | 1,283 / 160 / +1,123 | +38.2% | 7 + 3 | +11 + 2 |
| flg-r1 | 1,610 / 133 / +1,477 | 1,021 / 235 / +786 | +27.8% | 0 + 0 | +6 + 3 |
| flg-r2 | 2,025 / 193 / +1,832 | 955 / 94 / +861 | +33.1% | 1 + 0 | +7 + 2 |

Reading: 427 halves the words added and leaves deletions small (84 to 379 words per cycle against 955 to 3,327 added). Every 427 cycle still adds 955 to 2,244 words, a net 8% to 24% of the document per cycle. (Normative-word columns are the seed brief's; my regex also counted capitalised variants and differs only for trt-r1 cycle 2.)

### 1.2 Where the added words go (flg-r2, the loop whose reviser tagged every change with a finding id)

Per-finding words added, attributed from the inline `(F<n>)` / `(N<n>)` tags in `specs/history/spec-v2-after-round1.md` and `spec-v3-after-round2.md` against the previous copy (cycle 1 untagged: 260 words, mostly the new section 2.4 table):

| cycle | blocking fixes | words | non-blocking fixes (applied anyway) | words | share of tagged words spent on non-blocking |
|---|---|---|---|---|---|
| 1 (F1-F22) | F1-F13 (13) | 1,409 (mean 108, min 58, max 186) | F14, F15, F17-F22 (8 of 9) | 356 | 20% |
| 2 (N1-N11, C9, C12-C14) | N1-N6 (6) | 539 (158, 26, 138, 55, 102, 60) | N7-N11 and four citation notes | 417 | 44% |

Two facts matter for the design.

1. The non-blocking spend is not a lapse the contract forbids in practice. `disposition.md` (flg-r2) section 0 says "Non-blocking findings that correct an existing wrong or unmeasurable statement were applied in the same pass (the coordinator brief says to apply confirmed findings)"; flg-r1 `disposition.md` section 1 says "the review's reviser brief limits revision to blocking findings (PANEL:188-189); the Task 6 brief says to apply every confirmed finding. The Task 6 brief wins". The S1 reviser brief (T06, `phase2/S1/briefs/task-text/T06-R1-reviser-L10-3bb70411.txt`) reads "apply confirmed findings ... write disposition.md with one row per finding: applied (where) or rejected (cited reason)". So 427 bullets 6 and 7 ("a brief may narrow this scope; it may not widen it") are prose that a task brief outranks in practice. A mechanical rule that does not depend on which brief wins is the only kind that holds in S1.
2. The reviser answers with several times the text the reviewer asked for. The reviewer's `Recommendation:` lines for N1-N6 total 150 words; the reviser added 539 (3.6 times; per finding 4.1, 0.9, 8.1, 4.6, 3.6, 2.5). For N7-N11 the ratio is 4.3 (73 recommended words, 311 added). The extra text is citation annotation, a second site brought in line, an example, or a new check.

### 1.3 Which reviser additions produced which next-round findings

Method: for each blocking (or MAJOR-graded-minor) finding in the next report I read the finding and the disposition row of the fix it attacks, and compared the fix with the reviewer's own recommendation. One analyst, one pass; UNVERIFIED by a second reader. Files: `exp346-ab-flg-r2/.dev/orca-command-refactor/review/` (`spec-panel.md`, `disposition.md`, `spec-panel-round2.md`, `disposition-round2.md`, `spec-panel-round3.md`), the same folder in `exp346-ab-flg-r1` and `exp346-ab-ctl-r1`.

flg-r2, review 1 to review 2 (every new finding is `origin=changed`: N1-N11, 11 of 11; review 3: N12-N14 changed, N15 unchanged):

| next-round finding | parent fix (grade of the parent finding) | what the reviser added (words, this analysis) | relation to the reviewer's recommendation |
|---|---|---|---|
| N5 MAJOR blocking, AC-0.4 step 1 "proves" WC-1 without the launcher | F22 (MAJOR "FR-8 GAP minimum", **non-blocking**, "Priority Low", `spec-panel.md:63-66`) | 66: a 30 s bound, an owner, and AC-0.4 step 1 "also proving WC-1" | recommendation was "state the bound ... and name the owner"; the "also proving" claim is the reviser's |
| N12 MAJOR blocking, review 3's only blocking finding | the N5 fix (102 words: record the agent command, look for the question in `worker-read`) | followed the recommendation of N5 | N12 opens "The N5 fix: ..." (`spec-panel-round3.md:84-85`) |
| N4 MAJOR blocking, "SA-2 now says only two files may name Orca" | F12 (blocking, 58 words) | a universal claim: "Only two files may name Orca" | the recommendation offered a narrower alternative: "or state that those two files may name only the preamble's commands" |
| N6 MAJOR blocking, 7.2 step 3 fails the P0 smoke runs | F2 (blocking, 83 tagged words plus a new section 2.4 table) | a new check clause in step 3 plus a new section | recommendation: "a 'Contract path' column" in section 3 and a WC-4 rewording; no new step, no new section |
| N3 MAJOR blocking, contract paths have no root | F2 table plus F11 rule (130 words) | own-worktree rule and a relative-path table | cross-fix interaction; both followed their recommendations |
| N1 CRITICAL blocking, WC-7 names the protocol skill | F10 (blocking, 186 words, the largest fix) | WC-7 text with an example `sc:troubleshoot-protocol` | the recommendation itself said "or the command file's named skill" |
| N2 MAJOR blocking, step 4 reads top-level keys | F1 (CRITICAL blocking, 115 words) | `worker_status` field plus a change to 7.2 step 4 | the recommendation asked for the step 4 change |

flg-r1, review 2 to review 3 (`disposition-round2.md`, `spec-panel-round3.md`): the four R3 blocking findings and the two MAJOR-graded-minor ones trace to R2 fixes:

| next-round finding | parent fix | what happened |
|---|---|---|
| R3-3, R3-4 (blocking), R3-8 (MAJOR FR-9, graded minor), R3-10 (minor) | R2-1 (blocking, 141 words) | the R2-1 recommendation offered "add `--report-dir` to the cleanup-audit and index-repo P1 fixes, **or drop 'The only command changes' from SPEC2:82**". The reviser took the addition: a rewritten WC-4 report-directory rule, `--report-dir` on more rows, and the human-readable report relocated to the coordinator's directory. R3-4 attacks that relocation ("WC-4 now sends each `--report-dir` row's human-readable report into the coordinator's directory too"). A one-sentence deletion was on offer. |
| R3-2 (blocking) and R3-9 (minor) | R2-3 (blocking, 73 words) | the recommendation offered "`git status --porcelain --untracked-files=all` plus content hashes ... **or run each acceptance worker in a fresh worktree**". The reviser added the hash recipe; R3-2 found ignored paths invisible to it, R3-9 found rename and quoting defects in it. |
| R3-1 (blocking), R3-5 (minor) | R2-2 (blocking, 112 words) | a closed pass list ("the transcript holds only preamble lifecycle calls ... and reads of the brief's inputs"), attacked as a closed list against WC-7's open one. |
| R3-7 (MAJOR FR-8, graded minor) | R2-7 (MAJOR "graded minor", non-blocking, 82 words) | the tick mechanism for Monitor waits; R3-7 attacks its two UNVERIFIED assumptions. |

ctl-r1, review 2 to review 3 (`spec-panel-round3.md` Part 1, N1-N9): N1's fix wrote "total: every own value a command documents today has a row" (a 13-row adapter table, `SPEC:64,78-94`) and R3-1 found four commands without a row; N3's fix (a `find -newer` plus per-file porcelain recipe, `SPEC:221,227`) drew R3-3 ("`find -newer` lists gitignored caches"). Same two shapes as above.

### 1.4 The five classes the chains fall into (flg-r1 + flg-r2: the 13 critical+major items at R2/R3 traced above)

| class | items | count |
|---|---|---|
| A. the parent fix answered a non-blocking (or MAJOR-graded-minor) finding | N5, N12 (via F22), R3-7 (via R2-7) | 3 |
| B. fix added a universal or closed claim ("only two files", "holds only ...") | N4, R3-1 (outside the count: ctl-r1 R3-1, "total: every ...") | 2 |
| C. fix added or changed an executable check recipe or acceptance step | N2, N6, R3-2 (outside the count: ctl-r1 R3-3) | 3 |
| D. a deletion was on offer and a mechanism was added instead | R3-3, R3-4, R3-8 | 3 |
| E. the reviewer's own recommendation was the flawed part, or two fixes interacted | N1, N3 | 2 |

Concentration of the attack surface: acceptance-check text (section 7 of the spec) is 14% to 16% of the document and receives 17% to 34% of the added words (approximate, bag-of-words attribution by section), yet 11 of the 15 blocking findings at R2/R3 in flg-r1 and flg-r2 sit on a check, a step or an AC row (my classification; N1 spans WC-7 and step 5). The same defect family recurs across independent loops: "`git status` check is too weak" appears as ctl-r1 N3/R3-3 and flg-r1 R2-3/R3-2/R3-9.

### 1.5 What does not predict a blocking child (the honest part)

Of the 13 blocking fixes in flg-r2 cycle 1, five had a blocking child in review 2 (F1, F2, F10, F11, F12) and eight did not (F3-F9, F13); one more blocking child came from a non-blocking fix (F22). Features of the added text of each fix (my script, n = 13, no significance claimed):

| feature per fix | five fixes with a blocking child | eight without |
|---|---|---|
| words added | 114 | 105 |
| backtick code spans | 9.0 | 7.1 |
| file:line or path citations | 2.1 | 0.8 |
| new normative words | 0.0 | 0.8 |
| ids defined (WC-, AC-, section numbers) | 1.5 | 3.4 |

Size and normative-word count do not separate the groups; only reference density (code spans, citations) leans the expected way. The branching picture agrees: critical+major transitions (review 2 over review 1, review 3 over review 2) average 0.72 in the four control transitions and 0.66 in the eight 427 transitions (arm A r1 0.56 and 1.20, r2 0.78 and 0.71; flg-r1 0.31 and 1.20; flg-r2 0.35 and 0.17), although 427 halved the words added. A pure size cap will therefore cut growth and will not, by itself, cut review-3 blocking. That is why this design pairs the size budget with gates on the five classes above and claims no more than they support (section 6).

### 1.6 Replay of candidate caps on the real 427 fixes (flg-r2: 17 MAJOR-blocking fixes, 2 CRITICAL, 17 non-blocking)

| cap on words added per MAJOR blocking fix | MAJOR fixes over cap (of 17) | words that would have to be cut |
|---|---|---|
| 60 | 13 | 696 |
| 80 (proposed) | 11 | 449 |
| 100 | 8 | 264 |
| 120 | 5 | 126 |

CRITICAL cap 120: one of two over (N1, 158 words; F1 was 115). Minor budget 0: all 17 non-blocking fixes are refused (they ran 14 to 124 words). Applying 80/120 to blocking fixes and dropping the minor ones would have removed 46% of the tagged words of the two cycles (2,721 to about 1,461) before any net-cap or delete-first effect. That is a strong bite: 11 of 17 MAJOR fixes would need a cut-down, which is why section 7 lists under-fixing first.

## 2. Mechanism (each loop step, in order)

<!-- Source: Base (original, modified) — receipt sentence removed per PR-B4; coordinator sentence from Variant A (opus:architect), Section 2 (A:37) — merged per Change #9 -->
Shape in one paragraph: the reviewer writes, next to its findings, a machine-readable `fixbudget` block that gives every finding a budget class. The reviser answers each blocking finding by the ladder delete, narrow, replace, add, writes a ledger that quotes the exact sentence it changes and the finding id it answers, and runs a stdlib script (`fixcheck.py`). The script diffs baseline against revised at sentence level, attributes every changed span to a ledger entry, measures words, bytes, headings, ids, normative, universal and condition words, table rows and check recipes per finding, and returns an exit code. Over-budget fixes are cut down once; whatever is still over budget (or unattributed) is reverted to the baseline text by the script itself and the finding is listed `escalated`. The next review runs the same check itself before it looks at the text. Nothing about the 3-review cap, the grading rule or the `verdict:` line changes. The coordinator gets no new duty, so the S1 briefs change only by the command name.

<!-- Source: Base (original, modified) — heading per Change #9; steps regrouped by actor per Change #1 (Variant A, Section 2.1-2.3) -->
### Step 0 — one-time setup and availability (owner, before the experiment)
- Keep 427's coordinator duties unchanged (review count, prior report, saved copy; bullet 4).
- `spec-panel-minfix` stops with `E-FIXCHECK-MISSING` at the start of every run if `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" hash --file <spec>` cannot run, naming the two install paths. It never falls back to plain 427 behaviour silently (same spirit as 427 bullet 1, "never fall back to a first review").

<!-- Source: Base (original, modified) — re-review items moved to Step 3 per Change #1; block per Changes #5, #14, #17, #19, #20, #24 -->
### Step 1 — Review N, reviewer (`/sc:spec-panel-minfix`, critique mode; 427 bullets 1-5 unchanged)
1. First review: run `hash` on the spec; write `reviewed_sha256: <64 hex>` in the report header.
2. Write the `fixbudget` block (format below) and, if the verdict is `FAIL` and the review is not `review: 3`, the Reviser brief (literal text in section 4.2).

`fixbudget` block, fenced, inside the report, one line per finding of this review, plus one line per prior blocking id still open, with its prior severity and grade:

```fixbudget
review: 1 of 3
reviewed_sha256: <64 hex>
refs: SPEC
# id | severity | grade | budget
F1 | CRITICAL | blocking | std
F2 | MAJOR | blocking | std
F3 | MAJOR | blocking | override
F14 | MAJOR | minor | -
F22 | MINOR | minor | -
override-reason: F3 <why no in-budget fix can close it>
```

`grade` is 427's blocking or minor. `severity` may read `MAJOR/FR-8` or `MAJOR/FR-9`, so the checker can see a hard gate. `budget` is `std`, `override`, `gap:<n>` or `-` for minor. `override` is set by the reviewer when its own recommendation exceeds the class gross cap: at most one per report, blocking findings only, never an `origin=changed` finding, and only with an `override-reason: <id> <reason>` line in the block. `gap:<n>` marks a blocking `MAJOR/FR-8` or `MAJOR/FR-9` gap fill, n = the guard-table rows the finding names. `override` and `gap:<n>` are exclusive. FR-8 / FR-9 findings are blocking MAJOR as in 427 bullet 2 and get the blocking MAJOR class. A line whose severity is `CRITICAL`, `MAJOR/FR-8` or `MAJOR/FR-9` with grade `minor` is not an input error: the checker prints `GRADE-CONFLICT <id>`, keeps the budget the grade gives (zero for `minor`), and the exit code is unaffected. `refs` names the line-reference prefix the report uses (`SPEC`, `SPEC2`, ...), so the checker can compute the informational `named` flag.

<!-- Source: Base (original, modified) — baseline per Change #18 as corrected by PR-B2; minor rule per Change #3; check sequence per Changes #4, #21 as corrected by PR-B1; old Step 4 folded in as `check --enforce` per Changes #1, #4, #23, #32 (PR-B6) -->
### Step 2 — Reviser (separate agent; reads the report, as 427 bullet 6 already says)
1. Baseline: the saved copy, when the review brief supplies its path (not true of the S1 review briefs T05, T07 and T09 today); otherwise Reviser brief step 1 runs `snapshot --spec <spec> --report <report>`, which writes only `<report dir>/.fixcheck/base-<N>.md` and refuses a changed spec (exit 4, `STALE-BASE`). `check` compares the baseline's sha256 with `reviewed_sha256` (exit 4 on mismatch: someone edited between review and revise). The script, not the model, writes the `snapshot` copy (hidden folder `.fixcheck/`), because the S1 reviser brief says "Ownership: write ONLY your output file(s)" and the spec and `disposition.md` are the only files it may author.
2. For each blocking id, in this order: **delete** the wrong, unmeasurable or contradicting sentence or clause; else **narrow** (replace by fewer or equal words: turn a universal into a conditional, drop an adjective, point to text that exists); else **replace** (more words, within the gross cap); else **add**, and only after writing `considered:` in the ledger (the delete or narrow option tried and why it fails, at least 8 words). A finding that none of these can answer inside its budget is listed `escalated`, never expanded.
3. Non-blocking findings: no edit (minor budget 0; any hunk attributed to a minor id is a policy failure, exit 1). Their disposition row reads `deferred (minor, fixcheck budget 0)`, which fits the S1 brief's "rejected (cited reason)". This is where 427's bullet 7 meets the T06 brief ("apply confirmed findings"): the checker, not the brief, decides.
4. Write the ledger as a fenced `fixledger` block at the end of the reviser's own disposition file (the file the task brief already requires, so no new authored file):

````markdown
```fixledger
# fix ledger for review 1
## L1
finding: F10
op: replace
old: "WC-7 requires the worker to run the command directly."
new: "WC-7 requires a Skill tool call naming sc:<name>, the command"
considered: -
## L2
finding: F3
op: add
anchor: "Under --unattended the pre-creation STOP writes no package."
new: "Its contract goes to the fallback directory."
considered: "narrowing the STOP sentence cannot name a location, so one clause must be added after it"
## deferred
F14: deferred-minor
F7: escalated: needs a new field and a mapping, about 140 words, budget 80
```
````

   Rules: `op` is `delete | narrow | replace | add`; `old` is an exact baseline sentence (whitespace and markdown emphasis are normalised for comparison; a quote shorter than the sentence is accepted if it is at least 40 characters and unique); an `add` quotes the baseline sentence it follows as `anchor`; `new` is the first 10 words of the new text; `finding` names one id, and an edit that also answers another finding is charged to its owner only; an entry may carry `depends: L<n>`. Every blocking id of the `fixbudget` block must appear either in an entry or under `## deferred`.
5. `check --baseline <baseline> --revised <spec> --report <report> --ledger <disposition file>`; it prints its report to stdout and writes no file. Read the exit code (table below). On exit 1: cut the named entries down or add the missing entry or `## deferred` line, once, and run `check` again; if the second run still exits 1, run `check --enforce` with the same arguments. On exit 2: correct the call once and re-run; nothing is counted. On 3, 4, 5 or 70, at any run: edit nothing further and paste the output (step 3 then ends the run as an escalation). At most one cut-down pass; `--enforce` runs only after a second exit 1 and is the termination guarantee, so the loop cannot spin.
6. `check --enforce` (the only part that does not rely on the model) restores the baseline text for every finding with an exit-1 reason and for every unattributed hunk; a failing finding is reverted whole (all its hunks, so no half-fix remains). When it reverts a finding, it also reverts, whole, every finding that owns an entry that `depends:` on one of the reverted finding's entries. When the cycle cap is exceeded, it reverts whole findings until the cycle is within 600 words and 6,144 bytes: blocking MAJOR before CRITICAL; within a class, largest gross first, then by finding id. Each reverted finding is listed `escalated` with its gross as the need. It writes the file atomically (temp file and rename) and re-runs the check. It refuses to run without a ledger that has at least one entry (exit 3), so a reviser who forgot the ledger cannot lose the whole edit. Only `check --enforce` ever writes the spec; `hash`, `snapshot` and `check` without `--enforce` are read-only for the spec, and `spec-panel-minfix` itself still never edits it (427 design C6).
7. Disposition and report: bytes before and after (427 bullet 6) plus the `result:`, `escalated:` and last `FIXCHECK` lines of the final run, and of the first run when it was not exit 0.

<!-- Source: Base (original, modified) — B Step 1 items 2-3 and B Step 5 moved here per Change #1; checker run from Variant A (opus:architect), Section 2.3 — merged per Change #8; fail-closed from Variant C (haiku:backend), Step 6 — merged per Change #15; escalation per Changes #20, #22, PR-B4, PR-M9 -->
### Step 3 — Review N+1, re-review (reviewer)
1. Re-review (`--re-review <prior report> --baseline <saved copy>`): before the prior-blocking table, run `check` without `--enforce`: `--baseline <the saved copy passed as --baseline> --revised <spec> --report <prior report> --ledger <disposition file>`. It prints to stdout and writes no file. Put its summary in the header as `fixcheck: <exit> ...`. This run is authoritative: it counts whether or not the reviser ran the checker. If the saved copy, the prior report's block or the disposition file's ledger is missing or malformed, or this `check` exits 3, 4, 5 or 70, stop with the named input error; never fall back to a first review. Otherwise the review follows 427: prior-blocking table (`resolved|open|regressed`), then findings on changed lines with `origin=`.
2. Two additions to the re-review output, copied from this run and never from ledger prose (the reviewer stays blind to the reviser's reasons; copy only numbers and ids): (a) a prior blocking id the run reports over budget is `open (over budget)`, and one listed under `## deferred` as escalated is shown `open (escalated: budget)` with its one-line need from the run's `escalated:` line ("needs about 140 words, budget 80"); (b) every `origin=changed` finding carries `attacks: L<n>/<finding id>`, found by looking up the finding's quoted line in this run's hunks. This makes the fix-to-child chains of section 1.3 a computed field instead of a hand trace.
3. Then step 1 item 2 with `review: N+1 of 3`. At `review: 3` the run still escalates instead of briefing (427 bullet 6). The escalation message now also lists each blocking id that was `escalated` for budget with its stated need, from the disposition file's `## deferred` lines and the pasted `--enforce` output, and each `GRADE-CONFLICT` id. That is the "justified escalation": the user decides about a bigger change that the loop refused to make on its own.
4. If the re-review stops on an input (item 1), or the disposition's last `FIXCHECK` line shows exit 3, 4, 5 or 70, the run ends as an escalation to the user that lists the open blocking findings and the named input error. A stop with `E-FIXCHECK-MISSING` (step 0) is an install error reported to the owner, not a loop state. The 3-review cap, the grading rule and the verdict line are untouched.

<!-- Source: Base (original, modified) — reference section without a step number per Change #1; word rule per Change #7; bytes per Change #12; condition words from Variant A (opus:architect), Section 2.4 (A:80) — merged per Change #26; rename rule from Variant A (A:80) — merged per Change #34 -->
### What the checker computes (stdlib `difflib`, `hashlib`, `re`, `json`, `argparse`)
1. Normalise both texts (line endings, runs of whitespace, table alignment padding, emphasis marks). Split into units: one per line, then per sentence (`(?<=[.!?;])\s+(?=[A-Z`(\[|])`), and per table cell.
2. `difflib.SequenceMatcher(autojunk=False)` on the unit lists gives hunks. Inside each hunk a word-level `SequenceMatcher` gives added and deleted words. Words exclude `path:line` citation tokens, table pipes and heading marks, so a fix is not penalised in words for citing its evidence; bytes are counted on the raw added text, `path:line` tokens included. A finding-id tag written into the spec (`(F10)`, `(N3, N4)`) counts as a new id: a policy failure. Units that are deleted in one place and re-added identically elsewhere are `moved` and counted as zero.
3. Attribution: a hunk belongs to the ledger entry whose `old` quote is contained in the hunk's old text, or (for an `add`) whose `anchor` is the baseline unit just before the hunk, and whose `new` words start the hunk's new text. The checker also derives the real `op` of the hunk (empty new text is `delete`; no more words than before is `narrow`; more is `replace`; empty old text is `add`) and refuses a mislabelled entry. A hunk with no entry is `unattributed`.
4. Per finding it totals: `gross` (added words), `net` (added minus deleted), `add_only` (words of pure insertions), `entries`, `new_headings`, `new_ids`, `new_rows`, `new_norm` (net MUST, SHALL, must, never, always, shall), `new_univ` (net `only`, `every`, `exactly`, `none`, `total`, `closed`), `new_cond` (net new `if`, `unless`, `when`, `whenever`, `where`, `except`, `otherwise`; `only when` is caught by `when`; each counted word is a new guard charged to its finding), `new_exec` (added fenced blocks, and added backtick spans that contain a shell word such as `grep`, `git `, `diff`, `cmp`, `find `, `jq`, `uv `, `python`, `awk`, `sed `, `test ` or that contain a pipe or `$(`; a bare `--flag` or `--flag <value>` does not count, because the S1 spec names flags on nearly every line and would trip the gate on every fix). An identical single-token substitution repeated across units for one finding counts as one entry.
5. Informational, never failing: `named` (the entry's old text is quoted in the finding's report text, or on a line the finding cites through `refs`), so 427's "revise only text a blocking finding names" is measured per entry.

<!-- Source: Base (original, modified) — minor row 0 from Variant A (opus:architect), Section 2.4 (A:75) per Change #3; labels per Change #17; condition column per Change #26; cycle cap from Variant C (haiku:backend), Step 2 (C:62) per Change #12; override per Change #5; gap:<n> per Change #24 -->
### Budget table (first values; derivation in section 1.6 and section 6)

| class | applies to | gross (narrow/replace) | net | add-only | entries | new heading | new id | new table row | new normative | new universal | new condition | new exec recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRITICAL | CRITICAL blocking | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 2 | 1 |
| blocking MAJOR | MAJOR blocking, FR-8, FR-9 | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| minor | every non-blocking finding | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Cycle level: all findings together, overrides included, at most 600 gross added words and 6,144 gross added bytes. `delete` entries are free of the gross cap. Any hunk attributed to a minor id is a policy failure. `override` (set by the reviewer in the block, step 1) doubles gross, net, add-only and entries for that one finding and never lifts a heading or id limit; a second override, an override without a reason, or one on a minor finding is bad input (exit 3). `gap:<n>` sets that finding's condition-word limit to n instead of 1; every other limit is its class limit. Overrides are printed in the report, and the next review gets no exemption for override text.

<!-- Source: Base (original, modified) — receipt removed per Change #18 / PR-B4; cycle cap line per Change #12 (PR-M8); labels per Change #17; GRADE-CONFLICT per Change #20 (PR-M10) -->
### Checker report (stdout; `check` writes no file)

```text
FIXCHECK cycle=1 exit=1 base=sha:3f2a..c1 revised=sha:90be..77 ledger=sha:51d0..a8
hunks=41 attributed=39 unattributed=2 moved=2 net=340 cycle_words=512/600 cycle_bytes=3790/6144
id   cls             op-mix         ent gross net add head id row norm univ cond exec budget   named status
F1   CRITICAL        replace,narrow 2   74    41  0   0    0  0   0    0    0    0    std      2/2   OK
F2   blocking MAJOR  replace        1   131   88  0   0    0  1   0    0    0    1    std      1/1   OVER gross 131>80, net 88>50
F14  minor           replace        1   56    56  0   0    0  0   0    0    0    0    -        0/1   MINOR-EDIT (minor budget 0)
unattributed: h17 +22 words "The coordinator ..."; h33 +9 words "..."
override: F3 (+142 gross)
escalated: F7 (needs about 140 words, budget 80)
GRADE-CONFLICT F16 (MAJOR/FR-8 graded minor)
result: OVER-BUDGET F2; MINOR-EDIT F14; UNATTRIBUTED h17,h33
FIXCHECK exit=1
```

<!-- Source: Variant C (haiku:backend), exit table (C:259-267) — merged per Change #13; action column per Change #21 as corrected by PR-B1 -->
### Exit codes (`hash`, `snapshot` and `check`; `check --enforce` returns 0 only if its re-run check is 0)

| code | meaning | reviser / reviewer action |
|---|---|---|
| 0 | accept: all hunks attributed, every finding within budget, every blocking id fixed or under `## deferred` (may carry declared escalations) | reviser stops; reviewer records it |
| 1 | policy failure: unattributed hunk, quote not found in baseline, `op` mislabelled, a blocking id neither fixed nor under `## deferred`, edit on a minor id, finding-id tag in the spec, over budget, forbidden element (heading, id, row, normative, universal, condition, exec recipe), cycle cap | reviser cuts the named entries down or adds the missing entry or `## deferred` line, once, and runs `check` again; if the second run still exits 1, `check --enforce`. Reviewer marks the named findings `open (over budget)` |
| 2 | usage error (argparse) | correct the call once and re-run; nothing is counted |
| 3 | bad input: missing or empty file, no `fixbudget` block, malformed or extra override, a Reviser brief id that is not a blocking id of the block, ledger missing for `--enforce` | reviser edits nothing further and pastes the output; reviewer stops with the named input error and escalates (step 3) |
| 4 | hash conflict (`STALE-BASE`: the baseline or spec sha256 differs from `reviewed_sha256`) | as exit 3 |
| 5 | `--enforce` cannot write the spec safely | as exit 3 |
| 70 | internal error | as exit 3 |

Inside exit 1 the checker reports attribution reasons (unattributed hunk, quote, `op`, ledger completeness) before size reasons, so attribution is settled before size is judged.

## 3. Causes removed and causes left

<!-- Source: Base (original, modified) — rows 2, 6, 7, 9 and the F22 paragraph per Changes #3, #8, #12, #30 -->
Target (constraint 1): reach a clean PASS, or a justified escalation, inside the 3-review cap. Based on section 1 I do not claim the mechanism makes the loop converge on its own; I claim it removes the chain classes below and makes every remaining open blocking finding either a reviewer-recommendation problem or a visible, reasoned escalation.

| # | measured cause (evidence) | removed? | by what | what stays |
|---|---|---|---|---|
| 1 | Fix-induced findings: 89% (R2) and 100% (R3) of new findings in 427 reports are `origin=changed` (AB-REPORT); flg-r2 R2 11 of 11, flg-r1 R2 12 of 12 and R3 10 of 10 | Not removed. Any fix is changed text, so the share of new findings that are `origin=changed` stays near 100%. The number of fixes and the claims each carries go down | classes A, B, C, D of section 1.4 (11 of 13 traced items) are each cut by a rule; expected removal about half (section 6) | class E (N1, N3: the reviewer's own recommendation is the flawed part, or two fixes interact); every replacement child the leaner fix creates |
| 2 | Mechanism or text added for non-blocking findings: 8 of 9 non-blocking findings applied in flg-r2 cycle 1, 773 words (28%) over two cycles; F22 (MAJOR non-blocking, Priority Low) became N5 then N12, the only R3 blocking finding of flg-r2; R2-7 (graded minor) became R3-7 | **Removed**, by the script; zero edits. Any hunk attributed to a minor id is a policy failure that `check --enforce` reverts, whatever brief the task carries | minor class; `deferred-minor` disposition | the disposition row still exists |
| 3 | Mechanism or section added when a deletion or narrow option was on offer (class D: R2-1 gave "or drop 'The only command changes'" and produced R3-3, R3-4, R3-8, R3-10) | Reduced, not removed. The ladder is an incentive plus tiered caps: `add` gets the net cap (50) instead of the gross cap (80), needs a `considered:` sentence, and new headings and ids are capped at 0 | `op` check, add-only cap, heading and id gates | `considered:` is prose and its truth is unverifiable; a reviser can still pick `replace` where `delete` existed |
| 4 | Universal or closed claims (class B: "Only two files may name Orca", "total: every own value ... has a row", "holds only ...") and new executable check recipes or acceptance steps (class C: N2, N6, R3-2, ctl-r1 R3-3; the same `git status` recipe family recurs in three loops) | Reduced. At most one new universal token and one new exec recipe per MAJOR blocking fix, none for minor | `new_univ`, `new_exec` gates | the detectors are regex heuristics (precision UNVERIFIED); a necessary recipe needs the override or an escalation |
| 5 | Upward severity drift. Share of critical+major among findings per review (AB/ARMB tables): ctl-r1 58, 60, 73%; ctl-r2 57, 41, 57%; trt-r1 56, 56, 55%; trt-r2 56, 44, 56%; flg-r1 73, 42, 60%; flg-r2 77, 55, 25%. R3 share is above R2 share in 4 of 6 loops and the absolute count stays at 5 to 6. On one topic: F22 MAJOR non-blocking, then N5 MAJOR blocking, then N12 MAJOR blocking; N12 cites the earlier grading as precedent ("the panel graded a false P0 record blocking in round 2", `spec-panel-round3.md`, N12 text) | Partly. Text a minor finding names is left untouched, so it stays `origin=unchanged`, and 427 bullet 5 caps an unchanged finding at minor: touching minor text is what made it blocking-eligible. | minor budget 0 | the grading of text the reviser did change; the forced MAJOR of FR-8/FR-9 (R3-7, R3-8 were MAJOR by rule and graded minor by the concrete-outcome test); precedent citing between reports. Now measurable: `attacks:` plus the parent's grade give child severity against parent severity per chain |
| 6 | No mechanical stop: the only stop is the cap, and a cycle can explode (ctl-r2 +3,165 net words in cycle 2) | Partly. Three computed stops are added: the cycle cap (600 gross words and 6,144 gross bytes, overrides included), the override limit (one per report), and `check --enforce` termination (one cut-down pass, then script revert). The reviser can no longer iterate | exit codes 1 and 3, `check --enforce` | the cap of 3 reviews is still the only loop-level stop; I add no early-escalation rule (open question 3) |
| 7 | Growth: 63.5% control, 29.7% 427 | **Removed**, as arithmetic, if the checker is honoured: upper bound 14.7% in words and 21.3% in bytes (section 6.2) | per-finding and cycle caps | none beyond non-compliance |
| 8 | Task briefs outrank 427 prose (flg-r1: "The Task 6 brief wins") | Removed in effect: the script does not read the task brief. Residual is in the next row | script instead of bullet text | |
| 9 | The reviser may simply not run the checker | Detectable, not preventable. The re-review runs `check` itself; its run is authoritative whether or not the reviser ran the checker, and the command text is the reviewer's instruction (higher authority than the report), so the check always runs | the re-review's own `check` run (step 3) | prose compliance of the reviser with "run these commands"; tests of prose prove the text exists, not obedience |
| 10 | Whole-document attack on changed text; reviewer recommendations that are themselves flawed (N1, R3-2's hash recipe) | Not removed | | this is the territory of the diffgate and stoprule themes |

What the F22 chain looks like under the budget: F22 is minor, so it gets no edit, neither N5 nor N12 exists, and the minor note stays a minor note.

## 4. Exact changes (file by file, with the new text or script outline)

<!-- Source: Base (original, modified) — section regrouped as file table plus one H3 per artifact per Change #2 (Variant A, Section 4); rows per Changes #6, #28, #29 -->
### 4.1 File list

| action | path (in the repository) | note |
|---|---|---|
| new | `src/superclaude/commands/spec-panel-minfix.md` | a copy of `spec-panel.md` (486 lines in `src/` at 0423fe5f; it carries what the 472-line 427 text of Arms A and B lacks: a third Usage line, a `--target-release` sentence, "Native reasoning" at line 221 and a 12-line `## Unattended mode` section; the `plugins/` copy still has the 472-line text) with the region changes of section 4.2: frontmatter and command name, Usage line 2 without the unattended flags, no `## Unattended mode` section, the template lookup replaced, bullet 6 of `## Review Loop` amended, and a new `## Fix Budget` section between `## Review Loop` and `## Output Formats`. Bullets 1 to 5 and 7 stay byte-identical to `spec-panel.md` |
| new | `src/superclaude/skills/sc-fixcheck/SKILL.md` | section 4.4 |
| new | `src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py` | stdlib only (`argparse difflib hashlib json re sys os tempfile pathlib`), no import from the `superclaude` package, run as `uv run --no-project python "<base>/scripts/fixcheck.py"` like `sc-issue-protocol/scripts/origin_repo.py` |
| new | `tests/skills/test_sc_fixcheck.py` | behaviour tests of the script (section 4.5) |
| new | `tests/skills/test_spec_panel_minfix.py` | pins of the variant command (section 4.5) |
| not changed | `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `~/.claude/commands/sc/spec-panel.md` | the original stays the control; `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_review_severity_rule.py` and `tests/skills/test_worker_contract.py` run unchanged |
| not changed | `HOW-WE-WORK.md` (both copies), `pragmatic.md` S1-S5, `docs/guides/*` | the variant is experimental and is not offered in routing until it has results |
| check, may need a row | tests that enumerate commands or skills: `tests/core/test_how_we_work_routing_table.py`, `tests/skills/test_sc_recommend_routing_contract.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/unit/test_cli_install.py`, `tests/recommend/test_routing_refresh.py` | UNVERIFIED whether any of them fails on one extra command file and one extra skill folder; the first implementation task runs them and adds the plugin mirror only if a parity test demands it |

No project `.claude/` file is staged (`make sync-dev` copies the command and skill into the untracked dev copy). No `src/superclaude/` path appears in either new installed primitive; they name `~/.claude/skills/sc-fixcheck/` first and the project `.claude/skills/sc-fixcheck/` second, the order the dual-surface rule gives for skills.

<!-- Source: Base (original, modified) — one H3 per artifact per Change #2 (Variant A, Section 4.1); regions from Variant A (A:161-163, A:177-180) per Changes #6, #29 and Variant C (haiku:backend), C:160 per Change #28; `## Fix Budget` literal per Changes #3-#5, #7, #8, #12, #13, #15, #17-#19, #21, #24, #26, #31-#33 with PR-B1, PR-B2, PR-B4, PR-M2, PR-M3 -->
### 4.2 `spec-panel-minfix.md`: every changed region

The repository file is the current `src/` `spec-panel.md` with the regions below changed and byte-identical elsewhere; the experiment file is the same change applied to the 472-line 427 text (section 5), which has no unattended Usage flags and no `## Unattended mode` section, so regions 2 and 3 do not apply to it.

1. Frontmatter `name: spec-panel-minfix` and an "experimental" description; the command name in the Usage lines and the title.
2. Usage line 2 drops `[--unattended] [--report-dir <dir>]` (repository file only).
3. The `## Unattended mode` section is removed (repository file only): `tests/skills/test_worker_contract.py` asserts the exact set of commands that carry that heading.
4. The template lookup that names `src/superclaude/examples/release-spec-template.md` becomes "use a caller-supplied release template; if none is supplied, use the inline output schema", in both files, because both are installed. The install watcher records that the experiment file differs from Arm B's text on this line too (UNVERIFIED whether S1 exercises it).
5. `## Review Loop` keeps seven bullets. Bullets 1-5 and 7 stay byte-identical. Bullets 2 and 5 are not amended: the class lives in the `fixbudget` block and the re-review duty in `## Fix Budget`. Bullet 6 is 427's bullet-6 text minus its clause that each added paragraph or table cites its finding id, plus one appended clause, so its pins (`Reviser brief`, `byte size before and after`) stay valid:

   ```markdown
   ; the Reviser brief carries the `## Fix Budget` steps, and a blocking finding the reviser cannot fix within budget is listed `escalated` with what it needs, never expanded.
   ```

   Bullet 7 (a brief may narrow, never widen) is what makes the minor budget binding over a task brief that says "apply every confirmed finding".
6. A new `## Fix Budget` section between `## Review Loop` and `## Output Formats` (literal text):

```markdown
## Fix Budget

Applies to a critique-mode report that ends `verdict: FAIL` below `review: 3`, and to the `--re-review` that follows it. The script is `fixcheck.py` in `~/.claude/skills/sc-fixcheck/scripts/` first, else the project `.claude/skills/sc-fixcheck/scripts/`, run as `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" <subcommand> ...` (`hash`, `snapshot`, `check`; `check --enforce` reverts). If `hash --file <spec>` cannot run, stop with `E-FIXCHECK-MISSING`, name both paths, and do not review.

Words are counted without `path:line` citations; bytes are counted on the raw added text. A finding id written into the spec, such as `(F3)`, is a new id. Budget per finding:

| class | applies to | gross | net | add-only | entries | heading | id | table row | MUST/SHALL/must/never/always | only/every/exactly/none/total/closed | if/unless/when/whenever/where/except/otherwise | check recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRITICAL | CRITICAL blocking | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 2 | 1 |
| blocking MAJOR | MAJOR blocking, FR-8, FR-9 | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| minor | every non-blocking finding | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Whole cycle, overrides included: at most 600 gross added words and 6,144 gross added bytes. `override` (at most one per report, blocking findings only, never an `origin=changed` finding, with an `override-reason: <id> <reason>` line) doubles gross, net, add-only and entries for that finding and never lifts a heading or id limit. `gap:<n>` (a blocking `MAJOR/FR-8` or `MAJOR/FR-9` gap fill, n = the guard-table rows it names) sets the condition-word limit to n. `override` and `gap:<n>` are exclusive.

Exit codes of `hash`, `snapshot` and `check`: 0 accept; 1 policy failure (over budget, forbidden element, cycle cap, unattributed hunk, ledger incomplete, edit on a minor id); 2 usage; 3 bad input; 4 hash conflict; 5 cannot write the spec safely; 70 internal error.

Add to the report: a `fixbudget` block (`review: N of 3`, `reviewed_sha256: <hex from hash>`, `refs: <prefix>`, then `<id> | <severity> | <grade> | std|override|gap:<n>|-` per finding of this review and per prior blocking id still open, with its prior severity and grade; severity may read `MAJOR/FR-8` or `MAJOR/FR-9`). On a `--re-review`, first run `check` without `--enforce` (`--baseline <the saved copy passed as --baseline> --revised <spec> --report <prior report> --ledger <disposition file>`) and put its summary in the header as `fixcheck: <exit> ...`; if an input is missing or malformed, or that run exits 3, 4, 5 or 70, stop with the named input error, never fall back to a first review, and escalate with the open blocking findings. Show each prior blocking id that run reports over budget as `open (over budget)`, each escalated id as `open (escalated: budget)` with its one-line need, and `attacks: L<n>/<finding id>` on each `origin=changed` finding. Copy only numbers and ids from that run, never the reviser's reasons.

Reviser brief (place above the final `verdict:` line; fill `<...>`):
> Reviser brief, fix budget on. Fix only these blocking ids: <ids>. Every other finding is a minor note: change nothing for it and write `deferred (minor, fixcheck budget 0)` in its disposition row; a task brief that says to apply every finding is narrowed to this list (Review Loop bullet 7).
> 1. Baseline: <the saved copy, when this review's brief supplied its path>. If none is named, before the first edit run `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" snapshot --spec <spec> --report <this report>` (the script writes only `<report dir>/.fixcheck/base-<N>.md` and exits 4 if the spec changed since this review).
> 2. Answer each id by deleting the wrong sentence, else narrowing it, else replacing it; add text only after writing in the ledger why none of those fits. Per finding: CRITICAL 120 words added (net 80), blocking MAJOR 80 (net 50), blocking MAJOR at most 4 ledger entries, no new heading, id or section, no finding id in the spec, at most one new table row, one new MUST/SHALL/must/never/always, one new only/every/exactly/none/total/closed, one new if/unless/when/whenever/where/except/otherwise (CRITICAL two, `gap:<n>` n) and one new check recipe.
> 3. Write, as a fenced `fixledger` block at the end of your disposition file (it is one of your output files; do not create others), per change one entry with `finding` (one id), `op` (delete|narrow|replace|add), the exact baseline sentence as `old` (for an add, as `anchor`), the first 10 new words as `new`, `considered` for an add, and `depends: L<n>` when the entry only works together with entry L<n>. A finding you cannot fix inside its budget goes under `## deferred` as `<id>: escalated: <what it needs>`. Do not expand it to fit.
> 4. Run `... check --baseline <baseline> --revised <spec> --report <this report> --ledger <your disposition file>`. Exit 0 is required. On exit 1: cut the named entries down or add the missing entry or `## deferred` line, once, and run `check` again; if the second run still exits 1, run `check --enforce` with the same arguments. On exit 2: correct the call once and re-run. On 3, 4, 5 or 70, at any run: edit nothing further and paste the output.
> 5. In your report give the byte size before and after and paste the `result:`, `escalated:` and last `FIXCHECK` lines of the final run, and of the first run when it was not exit 0.
```

<!-- Source: Base (original, modified) — subcommands per Change #4 with `snapshot` kept per PR-B2; constants per Changes #3, #5, #12, #13, #26; parsing per Changes #14, #33; revert order per Change #23; `depends:` per Change #32 (PR-B6); receipt removed per Change #18 -->
### 4.3 Script outline (`fixcheck.py`, about 350 lines, stdlib only)

```python
BUDGETS = {  # the command's table must equal this: test M4 (C = CRITICAL, M = blocking MAJOR, m = minor)
  "C": dict(gross=120, net=80, add_only=80, entries=6, heading=0, id=0, row=1, norm=2, univ=1, cond=2, exec=1),
  "M": dict(gross=80,  net=50, add_only=50, entries=4, heading=0, id=0, row=1, norm=1, univ=1, cond=1, exec=1),
  "m": dict(gross=0,   net=0,  add_only=0,  entries=0, heading=0, id=0, row=0, norm=0, univ=0, cond=0, exec=0),
}
CYCLE_GROSS_WORDS, CYCLE_GROSS_BYTES, MAX_OVERRIDES = 600, 6144, 1
EXIT = {"OK": 0, "POLICY": 1, "USAGE": 2, "INPUT": 3, "HASH": 4, "WRITE": 5, "INTERNAL": 70}

main(argv)                       # argparse subcommands: hash snapshot check (check --enforce)
read_text(path)                  # exit 3 with a named message if unreadable or empty
parse_fixbudget(report_text)     # fenced ```fixbudget block -> {id: (severity, grade, budget)}, override-reason lines, reviewed_sha256, refs; prints GRADE-CONFLICT for CRITICAL, MAJOR/FR-8 or MAJOR/FR-9 graded minor; a Reviser brief id that is not a blocking id of the block -> exit 3
classify(severity, grade, budget)  # 'C' | 'M' | 'm', with the override doubling or the gap:<n> condition limit
parse_ledger(text)               # takes the fenced ```fixledger block when the file has one (the disposition file), else the whole file; '## L<n>' entries (key: value lines, optional depends: L<n>) and '## deferred' lines
units(text)                      # normalise; split on lines, sentences, table cells; keep (unit, line_no)
words(unit_list)                 # drop path:line citations, pipes, heading marks, emphasis
diff_hunks(base_units, new_units)  # SequenceMatcher(autojunk=False) -> hunks (i1,i2,j1,j2); mark moved units
hunk_counts(old, new)            # word-level SequenceMatcher -> added, deleted, raw added bytes, op in {delete,narrow,replace,add}
attribute(hunks, entries)        # old-quote containment / anchor match / 'new' prefix; derive real op; mismatch -> policy failure
element_counts(old, new)         # headings (ratio<0.8 vs every baseline heading), ids (regex, finding-id tags included), rows, norm, univ, cond, exec; one rename counts as one entry
score(findings, classes, overrides)   # per finding gross/net/add_only/entries/forbidden -> status + reasons
cycle_checks(totals)             # 600 gross words and 6,144 gross bytes, overrides included; override count
check(args) -> int               # prints the report, returns the exit code; inside exit 1, attribution reasons before size reasons
                                 # --enforce: reverts whole failing findings, the findings that depend: on them and unattributed hunks;
                                 # over the cycle cap, blocking MAJOR before CRITICAL, largest gross first, then by id; writes atomically, re-runs the check
snapshot(args) -> int            # writes only <report dir>/.fixcheck/base-<N>.md; exit 4 if the spec's sha256 differs from reviewed_sha256
render_report(result)            # format of section 2
```

Properties the tests pin: `check --enforce` followed by `check` returns 0 for every input that `check` can score; `check` without `--enforce` never writes the spec; `moved` text counts zero; the same inputs give the same output (no clock, no randomness); a 60 KB specification is checked in well under a second (UNVERIFIED, expected from the word-level diffs run for this analysis, which took seconds for 12 pairs).

<!-- Source: Base (original, modified) — the 4.1 file-table note moved here as the body per Change #2 -->
### 4.4 `sc-fixcheck/SKILL.md`

Frontmatter and one page: purpose, subcommands, formats, exit codes. Not user-invocable by design (the description says it is run by commands). Installs as `~/.claude/skills/sc-fixcheck/` through `install_skills.py`; the `sc-` name is safe because its served-by-command rule (strip `sc-`, look for `commands/fixcheck.md`) finds no such command, so the folder is installed standalone like the `sc-*-protocol` skills.

<!-- Source: Base (original, modified) — tests per Changes #3, #4, #5, #7, #13, #18, #23, #32 (PR-B6); M2 per PR-B5 with Changes #28, #29; M3 per Change #6; M7 per Changes #6, #29; evidence line per Change #8 -->
### 4.5 Tests

`tests/skills/test_sc_fixcheck.py` (loads the script by `importlib.util.spec_from_file_location`, `tmp_path` fixtures, no network):
1. clean within-budget fix: exit 0. 2. MAJOR fix of 81 added words: exit 1, reason `gross`. 3. net 51 with gross 60: exit 1, reason `net`. 4. a 1-word minor edit: exit 1. 5. new heading, new id, new table row beyond 1, a second MUST, a second condition word on a `std` blocking MAJOR fix: each exit 1 with its own reason. 6. a hunk with no ledger entry: exit 1. 7. a quote that is not in the baseline: exit 1. 8. mislabelled `op`: exit 1. 9. a blocking id neither fixed nor under `## deferred`: exit 1. 10. one override accepted; a second override, an override without a reason, or one on a minor finding: exit 3; an override never lifts a heading limit. 11. moved sentence counts zero. 12. a `path:line` token adds zero words; a `(F3)` tag exits 1 with reason `id`. 13. `check --enforce` restores baseline text for the over-budget finding and the unattributed hunk, leaves the within-budget finding, and reverts, whole, a finding that owns an entry with `depends:` on a reverted entry (its other entries too); then `check` returns 0; running it twice changes nothing more. 14. `check --enforce` without a ledger: exit 3 and the spec unchanged. 15. `snapshot` refuses a changed spec, and `check` refuses a baseline whose hash differs from `reviewed_sha256` (exit 4 each). 16. a cycle above 600 gross words reverts blocking MAJOR before CRITICAL, largest gross first, then by finding id. 17. a property test: random edits of a fixed spec with random ledgers always satisfy "after `check --enforce`, `check` is 0".

`tests/skills/test_spec_panel_minfix.py` (text pins, honest about what they prove):
- M1 frontmatter `name: spec-panel-minfix`; usage lines start `/sc:spec-panel-minfix `.
- M2 faithful copy: after excluding the frontmatter, the command-name substitution, bullet 6 (compared by M3), the Usage line 2 change, the template-lookup line, the `## Unattended mode` section and the `## Fix Budget` section, the file equals `src/superclaude/commands/spec-panel.md` line for line (so a later edit of the original that is not mirrored fails the test).
- M3 exactly seven bullets; bullets 1 to 5 and 7 equal the original's; bullet 6 is one line starting `6. **Reviser contract**` that contains `Reviser brief`, `byte size before and after` and `## Fix Budget`; the `## Fix Budget` heading sits between `## Review Loop` and `## Output Formats`.
- M4 number sync: the budget table in the command equals `BUDGETS` (script keys `C`, `M`, `m` map to `CRITICAL`, `blocking MAJOR`, `minor`), the cycle limits equal the constants, and the exit-code line equals `EXIT` (prose and script cannot drift apart silently).
- M5 literal `~/.claude/skills/sc-fixcheck/scripts/` before `.claude/skills/sc-fixcheck/scripts/`; the literal `E-FIXCHECK-MISSING`; no `src/superclaude` in the command or the skill.
- M6 the Reviser brief template contains the five numbered steps and the words `deferred (minor, fixcheck budget 0)`.
- M7 stays green without edit: `test_spec_panel_review_loop.py`, `test_review_severity_rule.py`, `test_worker_contract.py`. The severity test scans every command file for old-cap and any-severity phrases; whether the amended bullet 6 or the `## Fix Budget` numbers ("at most one per report", "at most 4 ledger entries") trip its cap-number matcher is UNVERIFIED and is the first thing the implementer runs; reword the numbers into the table if it does.

What these tests do not prove: that a reviser runs the commands, or that a reviewer writes a correct `fixbudget` block. The re-review's own `check` run and its `fixcheck:` header line are the runtime evidence.

<!-- Source: Variant A (opus:architect), Section 4.5 (A:256-261) — merged per Change #11; last sentence Base (original) -->
### 4.6 Later adopters (not part of this change)

The script is keyed on (baseline, revised, ledger, findings block), not on `spec-panel`.
- rf-qa Fix Cycle (`rf-qa.md` lines 379-416, 2-cycle cap): good fit; it fixes prose documents in place, so adoption is a reviewer-side `fixbudget` block and one checker call after its fix step.
- `/sc:reflect`: weak fit; it has no reviser step of its own.
- `/sc:implement` final review: changes code, where words are the wrong unit; it needs a code unitiser, out of scope.

Each adopter runs its own S1-style measurement first; I claim nothing for them.

## 5. Variant command name and install note

<!-- Source: Base (original, modified) — pre-flight probe from Variant C (haiku:backend), Section 5 (C:289) per Change #16; base-text paragraph per Changes #6, #28, #29 -->

**Name:** command `spec-panel-minfix`, invoked as `/sc:spec-panel-minfix` (Skill target `sc:spec-panel-minfix`). Checker skill folder `sc-fixcheck`. The original `spec-panel` is not edited anywhere: the variant is a new command file plus a new skill folder, so the control arm keeps running the original text beside it (D9: parallel arms need different command names).

**Installing beside the original, in the repository (after merge):** `superclaude install` already copies every `commands/*.md` into `~/.claude/commands/sc/` and every skill directory into `~/.claude/skills/`, and skips an existing command file unless `--force` (`install_commands.py` lines 60-90, `install_skills.py` directory copy). A new `spec-panel-minfix.md` and a new `sc-fixcheck/` therefore land next to `spec-panel.md` and do not touch it.

**Installing before merge, for the experiment (additive, no package reinstall, no `--force`; run by the owner or coordinator, not by a worker; the command file is the experiment build described under "Base text" below):**

```bash
cp -n <variant checkout>/src/superclaude/commands/spec-panel-minfix.md ~/.claude/commands/sc/spec-panel-minfix.md
mkdir -p ~/.claude/skills && cp -rn <variant checkout>/src/superclaude/skills/sc-fixcheck ~/.claude/skills/
sha256sum ~/.claude/commands/sc/spec-panel.md ~/.claude/commands/sc/spec-panel-minfix.md ~/.claude/skills/sc-fixcheck/scripts/fixcheck.py   # log in the install watcher
```

(Which of `install_skill.py` or `install_skills.py` performs the directory copy on the install path is UNVERIFIED; both appear under `cli/`.) `cp -n` never overwrites; `~/.claude/commands/sc/spec-panel.md` is not an argument of any command above. Per D9 a fresh worker loads commands from `~/.claude/commands/sc/` (personal beats project), so this is the only copy that matters on this machine. The existing install watcher (phase4 `install-watch.log`) gets two more sha256 lines; a change of either file during an arm voids V6 as before.

**How the checker reaches a worker whose repo base (commit 2cb683f5) has none of the new code:** it does not come from the repository at all. The command text points at `~/.claude/skills/sc-fixcheck/scripts/fixcheck.py` (the home directory, outside every worktree) and the script is stdlib only and run as `uv run --no-project python "<path>"`, which needs no `pyproject.toml`, no virtual environment and no `superclaude` import. Precedent for exactly this pattern: `sc-issue-protocol/SKILL.md:72,84` runs `origin_repo.py` that way in any project. The project copy `.claude/skills/sc-fixcheck/` (from `make sync-dev` in a dev checkout) is the second surface, read only if the home copy is absent. Before a measured loop, a fresh worker loads `/sc:spec-panel-minfix` and runs the installed checker on a tiny valid and a tiny invalid fixture (exit 0 and exit 1); reading the command file is not proof of invocation. If a worker's home copy is missing the command stops with `E-FIXCHECK-MISSING` instead of silently reviewing without the budget.

**Base text for the experiment file.** Arms A and B ran the exact 427 text (472 lines, sha256 c8d80346a96c, `git show 95f2c6e4:src/superclaude/commands/spec-panel.md`). The current `src/` file (486 lines) adds unattended-mode lines that S1 does not exercise (no brief passes `--unattended`, and `WORKER-CONTRACT.md` is moved aside), but D10/D11 changed one thing at a time and this arm should too. So the file installed for Arm C is the same change (frontmatter name, command-name tokens, the template-lookup line, bullet 6, `## Fix Budget`) applied to the 472-line 427 text, and the repository file is the same change applied to current `src/`, which also drops the `## Unattended mode` section and its Usage flags. The added hunks are byte-identical in both; a plain `diff` of the two variant files must show only the lines in which `spec-panel.md` itself differs between the two bases, except the removed section. Record both sha256 values in the install watcher.

**The one-line substitution an experiment brief needs.** Arm C briefs are Arm B's briefs (D11) with this single substitution applied to the review briefs T05, T07-template and T09-template; reviser briefs T06 and T08 stay verbatim (the reviser learns the budget from the report):

```text
s#/sc:spec-panel @#/sc:spec-panel-minfix @#
```

R2 and R3 review briefs keep Arm B's appended `--re-review <prior report> --baseline <saved copy>` flags, because the variant is built on 427's re-review. Record the substitution in the coordinator log as D9 requires. Nothing else in any brief changes; in particular no brief mentions the checker, the ledger or the budget.

## 6. Measurement plan and predicted numbers

<!-- Source: Base (original, modified) — 6.1 metrics per Changes #3, #18, #25, #27; 6.2 bound from Variant C (haiku:backend), C:62 and C:317 per Change #12; 6.3 conditional per Change #25 (PR-M1); 6.4 from Variant A (opus:architect), Section 6 (A:324-330) per Change #10 as corrected by PR-B3 -->

### 6.1 Design (Arm C, same shape as D10/D11)

Scenario S1 (Orca worker-contract spec, 57,763 bytes, 8,148 words), base commit 2cb683f5, same overlay, same verbatim briefs, same model (claude-opus-5-5), `WORKER-CONTRACT.md` moved aside, same loop (3 reviews, 2 fix cycles), two fresh worktrees `exp346-ab-min-r1` and `exp346-ab-min-r2`. Briefs: Arm B's, with the single substitution of section 5. Comparators: ctl-r1, ctl-r2 (reused as in D11), arm A (trt-r1, trt-r2) and Arm B (flg-r1, flg-r2) as secondary. Because the command names differ, the arm can run at the same time as new control replicates (D9), which removes the time-separation limit D11 had to state.

Bar, fixed now and the same as D11: (a) review-3 critical+major proxy mean at most 3 (50% of the control mean 6.0) **and** every replicate better than every control replicate, which with control values 8 and 4 means each replicate at most 3; or a clean pass sooner; (b) growth after two fix cycles at most 44.4% (70% of 63.5%), every replicate below both controls; (c) effect larger than the larger within-arm spread. Validity V1-V6 as in D10/D11, plus V7 below.

Metrics, per round, as D5, plus these that only this arm can produce:
- V7 (mechanism honoured): each cycle's disposition ends with a `FIXCHECK exit=0` line (or lists the ids `check --enforce` reverted), and the next review's own `check` run does not exit 3, 4, 5 or 70. A replicate whose reviser never ran the checker is recorded "mechanism not honoured" and does not count as treatment (the D11 rule for ignored flags).
- Growth in bytes and in words, from the re-review's `check` runs and from the history copies.
- Per cycle, from the pasted check lines and the re-review's run: blocking ids, ids `escalated` for budget, overrides used, hunks unattributed before `--enforce`, hunks reverted by `--enforce`, reviser tool calls and wall minutes, and the cut-down success rate (findings over budget at the first `check` that pass at the second).
- Chain data: from `attacks: L<n>/<id>` on every `origin=changed` finding, children per ledger entry by `op`, gross words, class and by whether the parent finding was blocking. This turns the hand trace of section 1.3 into a column and lets the second experiment fit the child rate against the five classes of section 1.4 with more than 13 items. Reported before the bar: within-budget parents with blocking children, as the count and share of within-budget ledger entries whose finding has a blocking `origin=changed` child.
- Severity: for each chain, parent grade against child grade (the drift measure the 427 data could only show as a per-round share).
- Review 3: the critical+major proxy and the blocking count, reported as two numbers; the blocking count split into carried (open from review 2: unfixed, escalated or reverted) and new (on cycle-2 hunks), reported before the bar is applied.

### 6.2 Predicted growth after two fix cycles (bar: at most 44.4%)

Measured inputs: flg-r2 tagged words by class (section 1.2, 1.6), 427 mean net growth 30.7% in words across the four 427 loops (23.7, 38.2, 27.8, 33.1).

- Replay on flg-r2 (the only loop with every change tagged): capping blocking fixes at 80/120 and dropping the 773 minor words removes 1,260 of 2,721 tagged words; the 260 untagged words of the new section 2.4 table fall under F2's 80 and are not additional. New gross about 1,461, deletions kept at the measured 287, net about 1,174 words, 14.4% against the actual 33.1%. The same ratio (0.435) on the four 427 loops gives 13.4%. The net caps (50 and 80) and delete-first push this lower; an override pushes it up a little.
- Arithmetic upper bound if the checker is honoured: two cycles add at most 1,200 gross words (14.7% of 8,148) and 12,288 gross bytes (21.3% of 57,763), overrides included, so net growth cannot exceed these. That bound needs no judgement about model behaviour, only that the script runs.
- **Prediction: 13% (range 8% to 14.7%), both replicates below 20%.** Bar (b) is met by a wide margin if V7 holds. If V7 fails the number is meaningless and the replicate is discarded.

### 6.3 Predicted review-3 critical+major proxy (bar: at most 3; control mean 6.0; 427 5.5; Arm B 3.5)

This is the hard number, and the data say size alone does not move it (section 1.5), so the derivation goes through the chain classes.

| input | value | status |
|---|---|---|
| review-1 proxy (the variant does not change the first review) | 12 (control 11.5; arm A 9, 9; Arm B 16, 17) | measured |
| transition ratio R2/R1 and R3/R2 per fix cycle, 427 | 0.66 (control 0.72) | measured, 8 and 4 transitions |
| fix-induced critical+major items by class A, B, C, D, E | 3, 2, 3, 3, 2 of 13 | measured by one analyst, UNVERIFIED by a second reader |
| probability that the rule removes an item of class A, D, B, C | 0.9, 0.6, 0.5, 0.3 | **assumed**: A is mechanical (the text is not touched), D depends on the reviser picking the deletion, B and C are caps rather than bans |
| share of removed items that reappear as another child of the leaner fix | 0.25 to 0.75 | **assumed** |

Expected removal of fix-induced items: (3 x 0.9 + 3 x 0.6 + 2 x 0.5 + 3 x 0.3) / 13 = 0.49. After replacement the net cut in the transition ratio is 0.37 (replacement 25%), 0.25 (50%) or 0.12 (75%), so r = 0.66 x (1 - cut) = 0.42, 0.50 or 0.58, and the review-3 proxy is about 12 x r squared = 2.1, 3.0 or 4.0.

**Prediction: review-3 proxy band 1.1 to 5.6 (A's estimate, about 4.1, lies inside it); central 3.3 (judgment).** If the two assumed rows hold (removal 0.49; replacement 25% to 75%), the mean is 2.1 to 4.0, about 3.0 at R1 = 12. The budget alone is not claimed to reach 3 or fewer (section 1.5). The two assumed rows decide the outcome and the experiment measures both (`attacks:` chains): that is the second use of Arm C.

Other predictions, each with the measured number it starts from:
- Escalated blocking ids at review 2: 1 to 3 of about 6 to 13, conditional on the cut-down success rate, which is not yet measured (section 6.1) (the replay put 11 of 17 MAJOR fixes over the 80-word cap and the reviewer's recommendations are 7 to 39 words, so most need a cut-down, a few an escalation).
- Blocking children per blocking fix: 0.30 (427: 0.46 for flg-r2 R1 to R2, 0.17 for R2 to R3).
- Share of new findings that are `origin=changed`: still 85% to 100%. This is expected and is not a success measure; do not read it as a failure either.
- Clean PASS within the cap: at most one of two replicates (flg-r2 would have passed at review 3 without the F22 chain; I treat that as luck, not a prediction).

### 6.4 What result would mean the idea failed

Fixed now, before any run, for valid (V7) replicates:
1. **Minimality is not enough.** The checker ended exit 0 in both cycles of both replicates (fixes were in budget and attributed) and the review-3 proxy is above 3 in either replicate. Then fix size is not what keeps review 3 blocking; drop minfix as a standalone fix and test it only in combination with a verdict-side change (stoprule theme).
2. **The budget converts fix-induced findings into unfixed ones.** Carried open blocking findings at review 3 (section 6.1: unfixed, escalated or reverted) are 3 or more in either replicate. The budget is too tight as tuned; no retune inside this run.
3. **Surface is not the driver.** Cycle-2 hunks at 14 or fewer, yet 3 or more new critical+major findings on those hunks at review 3 in either replicate.
4. **Only growth improves.** Growth is met but the review-3 proxy is not better than Arm B's mean (3.5). 427 already meets the growth bar, so minfix's extra cost buys nothing; reject it.

Not a test of the idea (re-run instead): any of V1-V7 fails (V7 as stated in section 6.1), the checker exits 3, 4, 5 or 70 in any cycle, or net growth exceeds the section 6.2 bound (14.7% words, 21.3% bytes) while the checker reports exit 0 (a checker bug).

Cost of the measurement: the same sessions as Arm B (5 worker sessions per replicate: 3 reviews and 2 revisions; the checker adds tool calls, not sessions), plus the analyst time to read the checker output.

## 7. Risks, costs and what would falsify it

<!-- Source: Base (original, modified) — 7.1 per Change #18 (PR-B2, PR-B4); 7.2 rows per Changes #3, #5, #8, #14, #15, #18, #26, #32, #33, #36 and likelihood / impact column per PR-B7; 7.3 per Changes #5, #8; 7.4 per Change #10 -->

### 7.1 Cost per loop (honest, mostly UNVERIFIED because tool-call counts of the S1 sessions were not measured)

| item | reviser (per fix cycle) | reviewer (per review) | per loop of 3 reviews and 2 cycles |
|---|---|---|---|
| extra tool calls | `snapshot` 0 or 1 (only when no saved-copy path is named), ledger append 1, `check` 1, cut-down edits 2 to 6, second `check` 1, `check --enforce` 0 or 1: 4 to 11 | `hash` (first review) or `check` (re-review), one call; `fixbudget` block is part of the report write: about 1 to 2 | about 11 to 28 |
| extra sessions | 0 | 0 | 0 (cut-down is inside the reviser session; no separate retry session) |
| extra wall time | 3 to 8 minutes of model time (ledger of 6 to 20 entries, one shortening pass); each script call under a second (UNVERIFIED, expected from the diff runs for this analysis) | 1 to 2 minutes | about 8 to 18 minutes on a loop that took about 78 minutes for control (05:05 to 06:23Z), so 10% to 23% |
| extra context | a ledger of about 2 to 4 KB, a check report of about 1 KB | its own check report, about 1 to 3 KB | small against 40 to 50 KB review reports |
| new files | none authored by the model; `.fixcheck/` is script output | the report gains a block | one hidden folder per report folder |

### 7.2 Ways the mechanism can make the loop worse

| # | failure | why it can happen (evidence) | detection | mitigation | residual | likelihood / impact (judgment, UNVERIFIED) |
|---|---|---|---|---|---|---|
| 1 | Under-fixing leaves blocking findings open | the replay put 11 of 17 MAJOR fixes over the 80-word cap (section 1.6); a fix cut to fit may lose its content; `check --enforce` reverts whole findings | `escalated` ids and `--enforce` reversions in the pasted check lines; review-2 table `open (escalated: budget)` | the 80-word cap is about twice the longest reviewer recommendation in flg-r2 round 2 (39 words; median 24); one override per report | a finding that needs a real mechanism is left to the user at review 3, by design; the review-3 count includes it, so this failure shows up in the very metric the bar uses | high / high: 11 of 17 MAJOR fixes were over the cap |
| 2 | Consistency residue from not propagating a rule | ctl-r1 R2 has findings labelled "Residue of round-1 finding 5" (N4: AC-4.3 contradicts WC-10's new exemption) and "Residue of round-1 finding 8" (N2); flg-r2's fixes touched 3 to 5 sites each (F1: WC-4, WC-5, 7.2 step 4, Decisions; F10: five sites) | `attacks:` children whose parent entry has `named: no` or fewer entries than sites | 4 entries per MAJOR, one override per report, `depends:` coupled revert | one override per report may be too few; open question 2. Undeclared dependencies remain: the coupled revert covers only declared `depends:` entries. This is the real tension of the theme: the ctl-r1 residue findings are what propagation prevents, and the flg-r2 N3/N6 findings are what propagation causes | medium / medium: fixes touched 3 to 5 sites each |
| 3 | Gaming the counter by rewording | gross counts changed tokens, not sentences, so rewording burns budget; `moved` needs exact equality; a split of one addition over two findings' entries is possible; synonyms ("solely", "each", "exclusively") evade the universal-token list; padding deletions can buy net room (gross still binds) | `named` flags, `attacks:` data, reviewer re-raising a deleted statement as a gap | per-finding gross cap, entries cap, minor budget 0 | the lexical gates (universal tokens, check recipes) are tripwires, not proofs; their precision is UNVERIFIED. Free in-scope deletions may remove required behaviour; they are measured, not capped | medium / medium: synonyms evade the token list |
| 4 | Escalation replaces fixes | escalating is cheaper than fixing; the reviser decides what is "over budget" | escalated share per cycle in the pasted check lines | the ledger must state what the fix needs in words (checkable against the cap by a reader); the reviewer re-lists the id as `open` | no automatic cap on the escalated share in v1 (open question 3); a high share is read as "budget too tight" (6.4) or "reviser dodging" and the two look alike | medium / high: escalating is cheaper than fixing |
| 5 | Checker false positives on legitimate edits | renumbering or inserting a numbered item creates "new ids" (AC-1.4 becomes AC-1.5); a table column change touches every row; heading rewording; curly quotes or changed backticks make a ledger quote fail to match (exit 1); the exec detector may fire on a spec that documents shell commands; `when` and `where` are common in prose, so the condition-word counter will flag ordinary sentences | exit 1 on an edit the reader judges legitimate | heading ratio 0.8; whitespace, emphasis, quote and table-padding normalisation; 40-character unique-substring quote match; the id gate counts only ids absent from the baseline | renumbering is not overridable in v1 and must be escalated; a `renumber: yes` ledger field is the likely first change (open question 4); the condition-word false-positive rate is measured by the replay harness (open question 9) | high / medium: `when` and `where` are common in prose |
| 6 | The reviser does not run the checker, or the task brief outranks the Reviser brief | flg-r1 `disposition.md`: "The Task 6 brief wins" (scope, not tools) | the re-review's own `check` run; a missing or malformed input stops the review with a named error (step 3); V7 fails | a one-replicate pilot before the n = 2 arm: if the pilot reviser skips the commands, the Reviser brief text is changed, not the design; the commands are procedural and do not contradict the task brief | prose compliance, and the cost of a wasted replicate. Tests prove the text exists, not that a model obeys it | medium / high: "The Task 6 brief wins" |
| 7 | Ownership clause of the reviser brief ("write ONLY your output file(s)") read to forbid running a script that writes a file | the `snapshot` copy in `.fixcheck/` when no saved-copy path is named | worker asks or skips; the re-review's `check` exits 3 or 4 | the ledger lives in the disposition file the brief requires; the baseline is the saved copy when the review brief names its path, else the script writes the `snapshot` copy; the Reviser brief says so | a literal-minded reviser may still refuse to run a script. Mitigated, not closed, until the one-replicate pilot shows that a saved-copy path can be named or that a reviser obeying the ownership clause runs `snapshot`; a failed pilot ends as a justified escalation (step 3), not a silent stop | medium / high: no S1 review brief names the saved-copy path today |
| 8 | Wrong `fixbudget` block | the reviewer mislabels a grade or id; budgets then apply to the wrong class | `snapshot` and `check` validate that every id of the block appears in the report body, that every id in the Reviser brief's id list is a blocking id of the block, and that classes parse; mismatch is exit 3; a `CRITICAL`, `MAJOR/FR-8` or `MAJOR/FR-9` line graded minor prints `GRADE-CONFLICT` | the block is generated from the same finding list the report already has | a consistently wrong grade is a grading error, which the budget cannot see | low / medium: the block comes from the report's own finding list |
| 9 | Minor corrections of real errors are left in the spec | minor budget is 0; flg-r1 R2-5 (`--output` should be `--output-dir`) and R2-6 are real wrong statements | the minor note stays in each later report | none, by design | every minor correction, one-token ones included (R2-5), waits for a separate task, which is 427's own rule ("minor findings never trigger a revision") now enforced | high / low: R2-5 and R2-6 are real wrong statements |
| 10 | The reviewer anchors on `attacks:` and attacks changed text harder | the tag invites a look at ledger entries | `origin=changed` share rising above the 427 level | the tag is written after the finding, from the hunks of the re-review's own `check` run; the reviewer never sees ledger prose | prose | low / medium: the tag invites a look at ledger entries |
| 11 | The pasted `FIXCHECK` line forged by hand | a model can write text | the re-review's own `check` run recomputes everything from the saved copy, the spec and the ledger | stdlib only, deterministic | an agent set on cheating can edit the base copy too; this is not a security boundary | low / low: the re-review recomputes everything |

### 7.3 What is prose only, and the residual risk

- "Delete before narrow before replace before add": the ladder is enforced only by tiered caps (add-only 50 against gross 80) and by a `considered:` sentence whose truth nothing checks. Residual: the reviser can choose `replace` where `delete` existed.
- "Reviser runs the checker": procedural prose in the report; the authoritative record is the re-review's own `check` run.
- "Reviewer writes `fixbudget` and `attacks:` from its own `check` run, not from ledger prose": prose; measured by the format of the report.
- "Never an override on an `origin=changed` finding": a reviewer rule; the checker cannot see `origin` in the block.
- Lexical gates (universal tokens, condition words, check recipes): heuristics.

### 7.4 What would falsify the idea

Section 6.4 lists the four results, fixed before any run, that would mean the idea failed.

## 8. Open questions

<!-- Source: Base (original, modified) — questions 1-3, 6, 7, 9-11 per Changes #3, #5, #6, #20, #27, #36 (PR-B4, PR-M5); question 4 and new question 12 per Change #36 -->
1. **Are 80/50 and 120/80 the right first values?** They come from one fully tagged loop (flg-r2: the replay of section 1.6) and from reviewer recommendations of 7 to 39 words. A relative budget (for example the larger of 40 and three times the words of the reviewer's recommendation) would track the reviewer's ask better, but needs the recommendation size in the `fixbudget` block, and the 3.6 times reviser ratio of section 1.2 suggests that a factor of 2 to 3 would still bind. I chose absolute numbers because the script can check them without parsing recommendations. Calibrate on the other five loops before the experiment (question 9).
2. **Is one override per report enough for propagation?** The tension in 7.2 row 2 (ctl-r1 residue findings against flg-r2 N3/N6) is unresolved by data. If the override sits at the limit in both cycles of both replicates, the entry cap (4 per MAJOR) is probably what is too low, not the override count.
3. **Should the loop get an early, computed escalation?** The checker could print `ESCALATE-NOW` when escalated ids exceed 40% of blocking ids after cycle 1, letting the run escalate before review 3. It would shorten hopeless loops but change the cap semantics that 427 pins; not added in v1. Related: a cycle whose fixes `check --enforce` reverts entirely still spends a review, because an empty diff counts as a review in 427.
4. **Renumbering and the id gate.** Inserting AC-1.4 renames later ids and looks like new ids. A `renumber: yes` ledger field that exempts ids shifted within an existing prefix is the likely first fix; not in v1 because it creates a loophole that needs its own test. Also open: a table-column fix (F2's "Contract path" column) touches every row and may need more than 4 entries; the rename rule covers only single-token substitutions.
5. **Should `named` become a hard gate?** It measures 427's "revise only text a blocking finding names" per entry; I kept it informational because propagation (question 2) is legitimate. Decide after Arm C shows the share of `named: no` entries among the parents of blocking children.
6. (Removed: the minor budget is 0.)
7. **Ledger visibility for the next review.** I chose: the reviewer sees its own `check` run (ids, numbers, hunks), never the ledger prose, to avoid anchoring on the reviser's reasons (flg-r2 round 3 explicitly decided each status "by reading the spec text at the cited line, not `disposition-round2.md`"). The alternative, an attack map, may raise `origin=changed` findings. Untested.
8. **A reviewer-side companion rule.** In flg-r1 R2-1 and R2-3 the reviewer offered the deletion or narrow option second. A one-line instruction "list the deleting or narrowing option first and give each option a word count" would cost nothing and addresses class D and part of class E, but it is a change to the reviewer, so it stays outside this theme's scope; flagged for the merge with the other variants.
9. **First implementation task: replay harness.** Run the finished script over the six recorded loops (baseline = previous history copy, ledger synthesised from each disposition table) and compare its per-finding gross words and over-cap counts with section 1.6; a deviation above 10% means the tokenisation rules (citations, pipes) need work before any worker sees them. The harness also reports, per recorded loop, the blocking fixes over cap at the first check (the denominator of the cut-down success rate; recorded loops contain no cut-down attempts, so the rate itself comes from the pilot and the replicates) and the false-positive rate of the condition words `when` and `where`; the ceiling on mis-attributed hunks is set from its output. Also decide whether `uv run --no-project` is acceptable offline (UNVERIFIED; the `sc-issue-protocol` precedent suggests yes, as no dependency is resolved).
10. **Folding into `spec-panel` after a pass.** The variant exists so the original and its 427 pin (T3 requires exactly seven bullets) stay untouched. If Arm C passes, merging bullet 6 and the `## Fix Budget` section into `spec-panel.md` is a separate change that must update the pin test and the plugin mirror; and `/sc:reflect`, rf-qa and `/sc:implement` adoption (section 4.6) each need their own measurement, because the unit (sentences of a spec) does not carry over to code.
11. **FR-8 and FR-9 classes.** The blocking MAJOR class applies to every finding the report grades blocking, FR-8 and FR-9 findings included when graded blocking (427 bullet 2). A GAP the reviewer grades minor under the concrete-outcome test (flg-r1 R3-7, R3-8) gets the minor budget and is not fixed; the checker prints `GRADE-CONFLICT` and the review-3 escalation lists it. Whether that matches what the owner wants from FR-8/FR-9 "hard gates" is a question for the owner, not for this design. Also for the owner: should the bar count the blocking grade instead of severity (section 6.1 reports both)?
12. **Moved text.** Text deleted in one place and re-added identically elsewhere counts zero, yet it is changed text the next review attacks. Should a move be charged?
