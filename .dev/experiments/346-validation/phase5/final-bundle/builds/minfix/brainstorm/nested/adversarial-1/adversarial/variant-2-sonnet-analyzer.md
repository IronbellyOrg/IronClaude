# Variant 2 (analyzer): fix-minimality budget with a mechanical checker (theme minfix, issue #346)

Persona: analyzer. Built on PR 427 (`## Review Loop`, 7 bullets). Evidence base: the six S1 loops (ctl-r1, ctl-r2, trt-r1, trt-r2, flg-r1, flg-r2), their reviews and dispositions, and word-level diffs of their spec history copies (analysis scripts were stdlib `difflib` run read-only; numbers below are mine unless a report is cited). Every claim I could not verify is marked UNVERIFIED.

## 1. Problem and evidence

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

CRITICAL cap 120: one of two over (N1, 158 words; F1 was 115). Minor cap 12: 17 of 17 non-blocking fixes over (they ran 14 to 124 words). Applying 80/120 to blocking fixes and dropping the minor ones would have removed 46% of the tagged words of the two cycles (2,721 to about 1,461) before any net-cap or delete-first effect. That is a strong bite: 11 of 17 MAJOR fixes would need a cut-down, which is why section 7 lists under-fixing first.

## 2. Mechanism (each loop step, in order)

Shape in one paragraph: the reviewer writes, next to its findings, a machine-readable `fixbudget` block that gives every finding a budget class. The reviser snapshots the spec, answers each blocking finding by the ladder delete, narrow, replace, add, writes a ledger that quotes the exact sentence it changes and the finding id it answers, and runs a stdlib script (`fixcheck.py`). The script diffs baseline against revised at sentence level, attributes every changed span to a ledger entry, measures words, headings, ids, normative and universal words, table rows and check recipes per finding, and returns an exit code. Over-budget fixes are cut down once; whatever is still over budget (or unattributed) is reverted to the baseline text by the script itself and the finding is listed `escalated`. The script leaves a receipt; the next review verifies the receipt before it looks at the text. Nothing about the 3-review cap, the grading rule or the `verdict:` line changes.

### Step 0 — one-time setup and availability (coordinator or owner)
- Keep 427's coordinator duties unchanged (review count, prior report, saved copy; bullet 4).
- `spec-panel-minfix` stops with `E-FIXCHECK-MISSING` at the start of every run if `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" hash --file <spec>` cannot run, naming the two install paths. It never falls back to plain 427 behaviour silently (same spirit as 427 bullet 1, "never fall back to a first review").

### Step 1 — Review N (`/sc:spec-panel-minfix`, critique mode; 427 bullets 1-5 unchanged)
1. First review: run `hash` on the spec; write `reviewed_sha256: <64 hex>` in the report header.
2. Re-review (`--re-review <prior report> --baseline <saved copy>`): before reading the spec, run `verify --receipt <report dir>/.fixcheck/receipt-<N-1>.json --revised <spec>`. Header line `fixcheck: OK | STALE | MISSING`. STALE (spec bytes changed after the receipt) and MISSING do not stop the review; the loop records them and the replicate is invalid for the measurement (section 6). The review then follows 427: prior-blocking table (`resolved|open|regressed`), then findings on changed lines with `origin=`.
3. Two additions to the re-review output, both copied from the receipt and never from ledger prose (the reviewer stays blind to the reviser's reasons): (a) a prior blocking id listed `escalated` in the receipt is shown `open (escalated: budget)` with the receipt's one-line need ("needs about 140 words, budget 80"); (b) every `origin=changed` finding carries `attacks: L<n>/<finding id>`, found by looking up the finding's quoted line in `hunks[].new_lines` of the receipt. This makes the fix-to-child chains of section 1.3 a computed field instead of a hand trace.
4. Write the `fixbudget` block (format below) and, if the verdict is `FAIL` and the review is not `review: 3`, the Reviser brief (literal text in section 4).

`fixbudget` block, fenced, inside the report, one line per finding of this review:

```fixbudget
review: 1 of 3
reviewed_sha256: <64 hex>
refs: SPEC
# id | severity | grade | budget
F1 | CRITICAL | blocking | std
F2 | MAJOR | blocking | std
F3 | MAJOR | blocking | large
F14 | MAJOR | minor | -
F22 | MINOR | minor | -
```

`grade` is 427's blocking or minor. `budget` is `std`, `large` (the reviewer's own recommendation exceeds the class gross cap; at most `ceil(25%)` of the blocking ids may carry it, extra `large` flags are ignored and reported) or `-` for minor. FR-8 / FR-9 findings are blocking MAJOR as in 427 bullet 2 and get class M. `refs` names the line-reference prefix the report uses (`SPEC`, `SPEC2`, ...), so the checker can compute the informational `named` flag.

### Step 2 — Reviser (separate agent; reads the report, as 427 bullet 6 already says)
1. `snapshot --spec <spec> --report <report>`: copies the spec to `<report dir>/.fixcheck/base-<N>.md` and refuses (exit 1, `STALE-BASE`) if its sha256 differs from `reviewed_sha256` (someone edited between review and revise). The script, not the model, writes this copy and the receipt (hidden folder `.fixcheck/`), because the S1 reviser brief says "Ownership: write ONLY your output file(s)" and the spec and `disposition.md` are the only files it may author. This copy is also the saved copy the coordinator needs for the next `--baseline`; a coordinator copy with the same hash is equivalent.
2. For each blocking id, in this order: **delete** the wrong, unmeasurable or contradicting sentence or clause; else **narrow** (replace by fewer or equal words: turn a universal into a conditional, drop an adjective, point to text that exists); else **replace** (more words, within the gross cap); else **add**, and only after writing `considered:` in the ledger (the delete or narrow option tried and why it fails, at least 8 words). A finding that none of these can answer inside its budget is listed `escalated`, never expanded.
3. Non-blocking findings: no edit beyond the minor budget (12 words, net 0, one entry). Their disposition row reads `deferred (minor, fixcheck budget 0)`, which fits the S1 brief's "rejected (cited reason)". This is where 427's bullet 7 meets the T06 brief ("apply confirmed findings"): the checker, not the brief, decides.
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
override: none
## L2
finding: F3
op: add
anchor: "Under --unattended the pre-creation STOP writes no package."
new: "Its contract goes to the fallback directory."
considered: "narrowing the STOP sentence cannot name a location, so one clause must be added after it"
override: none
## deferred
F14: deferred-minor
F7: escalated: needs a new field and a mapping, about 140 words, budget 80
```
````

   Rules: `op` is `delete | narrow | replace | add`; `old` is an exact baseline sentence (whitespace and markdown emphasis are normalised for comparison; a quote shorter than the sentence is accepted if it is at least 40 characters and unique); an `add` quotes the baseline sentence it follows as `anchor`; `new` is the first 10 words of the new text; `finding` may list two ids (the words are split equally); `override` is `none` or `<code>: <reason>`. Every blocking id of the `fixbudget` block must appear either in an entry or under `## deferred`.
5. `check --baseline <report dir>/.fixcheck/base-<N>.md --revised <spec> --report <report> --ledger <disposition file>`; the script writes the receipt `<report dir>/.fixcheck/receipt-<N>.json` itself. Read the exit code (table below). On 2, 3 or 4: cut the named entries down or add the missing entry, then run `check` once more. If it is still not 0, run `enforce ... --in-place` and then `check` a last time. At most one cut-down pass; `enforce` is the termination guarantee, so the loop cannot spin.
6. Disposition and report: bytes before and after (427 bullet 6) plus the last `FIXCHECK` line pasted.

### Step 3 — What the checker computes (stdlib `difflib`, `hashlib`, `re`, `json`, `argparse`)
1. Normalise both texts (line endings, runs of whitespace, table alignment padding, emphasis marks). Split into units: one per line, then per sentence (`(?<=[.!?;])\s+(?=[A-Z`(\[|])`), and per table cell.
2. `difflib.SequenceMatcher(autojunk=False)` on the unit lists gives hunks. Inside each hunk a word-level `SequenceMatcher` gives added and deleted words. Words exclude finding-id tags such as `(F10)` or `(N3, N4)`, `path:line` citation tokens, table pipes and heading marks, so a fix that cites its evidence as the README demands is not penalised for the citation. Units that are deleted in one place and re-added identically elsewhere are `moved` and counted as zero.
3. Attribution: a hunk belongs to the ledger entry whose `old` quote is contained in the hunk's old text, or (for an `add`) whose `anchor` is the baseline unit just before the hunk, and whose `new` words start the hunk's new text. The checker also derives the real `op` of the hunk (empty new text is `delete`; no more words than before is `narrow`; more is `replace`; empty old text is `add`) and refuses a mislabelled entry. A hunk with no entry is `unattributed`.
4. Per finding it totals: `gross` (added words), `net` (added minus deleted), `add_only` (words of pure insertions), `entries`, `new_headings`, `new_ids`, `new_rows`, `new_norm` (net MUST, SHALL, must, never, always, shall), `new_univ` (net `only`, `every`, `exactly`, `none`, `total`, `closed`), `new_exec` (added fenced blocks, and added backtick spans that contain a shell word such as `grep`, `git `, `diff`, `cmp`, `find `, `jq`, `uv `, `python`, `awk`, `sed `, `test ` or that contain a pipe or `$(`; a bare `--flag` or `--flag <value>` does not count, because the S1 spec names flags on nearly every line and would trip the gate on every fix).
5. Informational, never failing: `named` (the entry's old text is quoted in the finding's report text, or on a line the finding cites through `refs`), so 427's "revise only text a blocking finding names" is measured per entry.

### Budget table (first values; derivation in section 1.6 and section 6)

| class | applies to | gross (narrow/replace) | net | add-only | entries | new heading | new id | new table row | new normative | new universal | new exec recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CRITICAL blocking | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 1 |
| M | MAJOR blocking, FR-8, FR-9 | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 |
| m | every non-blocking finding | 12 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

Cycle level: all `m` fixes together at most 36 words; net growth of the whole document at most 10% of the baseline word count (`CYCLE-GROWTH`; a computed stop for runaway cycles). `delete` entries are free of the gross cap. Override (ledger `override: gap-fill | multi-site | contradiction: <reason of at least 10 words>`) doubles gross, net, add-only and entries for that one finding, never lifts a heading or id limit, only applies to a blocking finding, and at most 2 per cycle; a third, an override on a minor finding or an unknown code is exit 4. A `large` flag from the reviewer has the same doubling effect without using an override. Overrides are printed in the report and in the receipt, and the next review gets no exemption for override text.

### Checker report (stdout; the same data in the JSON receipt)

```text
FIXCHECK cycle=1 exit=2 base=sha:3f2a..c1 revised=sha:90be..77 ledger=sha:51d0..a8
hunks=41 attributed=39 unattributed=2 moved=2 gross=912 net=640 growth=7.9% cap=10.0%
id   cls op-mix        ent gross net add head id row norm univ exec ovr  named status
F1   C   replace,narrow 2  74    41  0   0    0  0   0    0    0    -    2/2   OK
F2   M   replace        1  131   88  0   0    0  1   0    0    1    -    1/1   OVER gross 131>80, net 88>50
F14  m   replace        1  56    56  0   0    0  0   0    0    0    -    0/1   OVER minor budget (gross 56>12, net 56>0)
unattributed: h17 +22 words "The coordinator ..."; h33 +9 words "..."
overrides: 1/2 (F3 gap-fill, +142 gross)
escalated-by-ledger: F7 (needs about 140 words, budget 80)
result: OVER-BUDGET F2,F14; UNATTRIBUTED h17,h33
FIXCHECK exit=2
```

JSON receipt `.fixcheck/receipt-<N>.json` keys: `schema` ("fixcheck/1"), `cycle`, `exit`, `baseline_sha256`, `revised_sha256`, `ledger_sha256`, `report_sha256`, `bytes_before`, `bytes_after`, `words_before`, `words_after`, `growth_pct`, `findings[]` (`id`, `class`, `entries`, `gross`, `net`, `add_only`, `new_headings`, `new_ids`, `new_rows`, `new_norm`, `new_univ`, `new_exec`, `override`, `named`, `status` = `ok | over | reverted | escalated | deferred-minor`, `reasons[]`), `hunks[]` (`id`, `entry`, `finding`, `old_lines`, `new_lines`, `gross`, `net`), `unattributed[]`, `overrides[]`, `escalated[]` (`id`, `need`).

### Exit codes (`check`; `enforce` returns 0 only if its final `check` is 0)

| code | meaning | reviser action |
|---|---|---|
| 0 | all hunks attributed, every finding within budget or overridden, every blocking id fixed or escalated | proceed |
| 1 | input error: unreadable or empty file, `STALE-BASE`, hash mismatch, no `fixbudget` block, ledger missing for `enforce` | repair the call; never treat as OK |
| 2 | over budget, forbidden element (heading, id, row, normative, universal, exec recipe), or `CYCLE-GROWTH` | cut the named entries down once, else `enforce` |
| 3 | ledger incomplete: unattributed hunk, quote not found in baseline, `op` mislabelled, a blocking id neither fixed nor under `## deferred` | add the entry or the deferral |
| 4 | override refused (third override, minor finding, unknown code, reason too short) | drop it, cut down or escalate |

If several apply, the checker reports them in the order 1, 3, 4, 2, so attribution is settled before size is judged.

### Step 4 — `enforce` (the only part that does not rely on the model)
`enforce --baseline --revised --report --ledger --in-place` restores the baseline text for every hunk of every finding that fails (exit 2 or 4 reasons) and for every unattributed hunk; a failing finding is reverted whole (all its hunks, so no half-fix remains), and for `CYCLE-GROWTH` the findings with the highest gross are reverted first until growth is under the cap. It writes the file atomically (temp file and rename), lists the reverted ids as `escalated` with the words they needed, re-runs `check`, and writes the receipt. It refuses to run without a ledger that has at least one entry (exit 1), so a reviser who forgot the ledger cannot lose the whole edit. Only `enforce --in-place` ever writes the spec; `hash`, `snapshot`, `check` and `verify` are read-only for the spec, and `spec-panel-minfix` itself still never edits it (427 design C6).

### Step 5 — Next review, cap and escalation
Back to step 1 with `review: N+1 of 3`. At `review: 3` the run still escalates instead of briefing (427 bullet 6). The escalation message now also lists, from the receipts, each blocking id that was `escalated` for budget with its stated need. That is the "justified escalation": the user decides about a bigger change that the loop refused to make on its own. The 3-review cap, the grading rule and the verdict line are untouched.

## 3. Causes removed and causes left

Target (constraint 1): reach a clean PASS, or a justified escalation, inside the 3-review cap. Based on section 1 I do not claim the mechanism makes the loop converge on its own; I claim it removes the chain classes below and makes every remaining open blocking finding either a reviewer-recommendation problem or a visible, reasoned escalation.

| # | measured cause (evidence) | removed? | by what | what stays |
|---|---|---|---|---|
| 1 | Fix-induced findings: 89% (R2) and 100% (R3) of new findings in 427 reports are `origin=changed` (AB-REPORT); flg-r2 R2 11 of 11, flg-r1 R2 12 of 12 and R3 10 of 10 | Not removed. Any fix is changed text, so the share of new findings that are `origin=changed` stays near 100%. The number of fixes and the claims each carries go down | classes A, B, C, D of section 1.4 (11 of 13 traced items) are each cut by a rule; expected removal about half (section 6) | class E (N1, N3: the reviewer's own recommendation is the flawed part, or two fixes interact); every replacement child the leaner fix creates |
| 2 | Mechanism or text added for non-blocking findings: 8 of 9 non-blocking findings applied in flg-r2 cycle 1, 773 words (28%) over two cycles; F22 (MAJOR non-blocking, Priority Low) became N5 then N12, the only R3 blocking finding of flg-r2; R2-7 (graded minor) became R3-7 | **Removed**, by the script. Minor budget is 12 words and net 0, 36 per cycle, enforced by `enforce` whatever brief the task carries | minor class `m`; `deferred-minor` disposition | up to 36 words of one-token corrections per cycle; the disposition row still exists |
| 3 | Mechanism or section added when a deletion or narrow option was on offer (class D: R2-1 gave "or drop 'The only command changes'" and produced R3-3, R3-4, R3-8, R3-10) | Reduced, not removed. The ladder is an incentive plus tiered caps: `add` gets the net cap (50) instead of the gross cap (80), needs a `considered:` sentence, and new headings and ids are capped at 0 | `op` check, add-only cap, heading and id gates | `considered:` is prose and its truth is unverifiable; a reviser can still pick `replace` where `delete` existed |
| 4 | Universal or closed claims (class B: "Only two files may name Orca", "total: every own value ... has a row", "holds only ...") and new executable check recipes or acceptance steps (class C: N2, N6, R3-2, ctl-r1 R3-3; the same `git status` recipe family recurs in three loops) | Reduced. At most one new universal token and one new exec recipe per MAJOR blocking fix, none for minor | `new_univ`, `new_exec` gates | the detectors are regex heuristics (precision UNVERIFIED); a necessary recipe needs the override or an escalation |
| 5 | Upward severity drift. Share of critical+major among findings per review (AB/ARMB tables): ctl-r1 58, 60, 73%; ctl-r2 57, 41, 57%; trt-r1 56, 56, 55%; trt-r2 56, 44, 56%; flg-r1 73, 42, 60%; flg-r2 77, 55, 25%. R3 share is above R2 share in 4 of 6 loops and the absolute count stays at 5 to 6. On one topic: F22 MAJOR non-blocking, then N5 MAJOR blocking, then N12 MAJOR blocking; N12 cites the earlier grading as precedent ("the panel graded a false P0 record blocking in round 2", `spec-panel-round3.md`, N12 text) | Partly. Text a minor finding names is left untouched, so it stays `origin=unchanged`, and 427 bullet 5 caps an unchanged finding at minor: touching minor text is what made it blocking-eligible. | minor budget 0 | the grading of text the reviser did change; the forced MAJOR of FR-8/FR-9 (R3-7, R3-8 were MAJOR by rule and graded minor by the concrete-outcome test); precedent citing between reports. Now measurable: `attacks:` plus the parent's grade give child severity against parent severity per chain |
| 6 | No mechanical stop: the only stop is the cap, and a cycle can explode (ctl-r2 +3,165 net words in cycle 2) | Partly. Three computed stops are added: the 10% cycle growth cap (`CYCLE-GROWTH`), the override limit (2 per cycle), and `enforce` termination (one cut-down pass, then script revert). The reviser can no longer iterate | exit codes 2 and 4, `enforce` | the cap of 3 reviews is still the only loop-level stop; I add no early-escalation rule (open question 3) |
| 7 | Growth: 63.5% control, 29.7% 427 | **Removed**, as arithmetic, if the checker is honoured: upper bound about 16% (section 6) | per-finding and cycle caps | none beyond non-compliance |
| 8 | Task briefs outrank 427 prose (flg-r1: "The Task 6 brief wins") | Removed in effect: the script does not read the task brief. Residual is in the next row | script instead of bullet text | |
| 9 | The reviser may simply not run the checker | Detectable, not preventable. A missing or stale receipt is printed in the next report header and invalidates the replicate; the command text is the reviewer's instruction (higher authority than the report) so the verification at least always runs | `verify` in step 1 | prose compliance of the reviser with "run these commands"; tests of prose prove the text exists, not obedience |
| 10 | Whole-document attack on changed text; reviewer recommendations that are themselves flawed (N1, R3-2's hash recipe) | Not removed | | this is the territory of the diffgate and stoprule themes |

What the F22 chain looks like under the budget: F22 is non-blocking, so class `m` applies (12 words, net 0, one entry). The reviser may replace "well inside the readiness limit" by "within 30 s" (3 words added, 3 deleted: a legal `narrow`), which is exactly the bound the reviewer recommended. The second change that started the chain, AC-0.4 step 1 "also proving WC-1", would need a second entry on a different sentence; the minor class allows one entry and no new check recipe, so it is refused. Neither N5 nor N12 exists, and the WC-1 line is the only text that changed. If the reviser skips even that, the minor note simply stays a minor note.

## 4. Exact changes (file by file, with the new text or script outline)

### 4.1 File list

| action | path (in the repository) | note |
|---|---|---|
| new | `src/superclaude/commands/spec-panel-minfix.md` | a copy of `spec-panel.md` (486 lines in `src/` at 0423fe5f; it carries what the 472-line 427 text of Arms A and B lacks: a third Usage line, a `--target-release` sentence, "Native reasoning" at line 221 and a 12-line `## Unattended mode` section; the `plugins/` copy still has the 472-line text) with: frontmatter `name: spec-panel-minfix` and an "experimental" description; the command name in the Usage lines and the title; bullet 8 in `## Review Loop`; a new `## Fix Budget` section between `## Review Loop` and `## Output Formats`. Bullets 1 to 7 stay byte-identical to `spec-panel.md` |
| new | `src/superclaude/skills/sc-fixcheck/SKILL.md` | frontmatter and one page: purpose, subcommands, formats, exit codes. Not user-invocable by design (the description says it is run by commands). Installs as `~/.claude/skills/sc-fixcheck/` through `install_skills.py`; the `sc-` name is safe because its served-by-command rule (strip `sc-`, look for `commands/fixcheck.md`) finds no such command, so the folder is installed standalone like the `sc-*-protocol` skills |
| new | `src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py` | stdlib only (`argparse difflib hashlib json re sys os tempfile pathlib`), no import from the `superclaude` package, run as `uv run --no-project python "<base>/scripts/fixcheck.py"` like `sc-issue-protocol/scripts/origin_repo.py` |
| new | `tests/skills/test_sc_fixcheck.py` | behaviour tests of the script (section 4.5) |
| new | `tests/skills/test_spec_panel_minfix.py` | pins of the variant command (section 4.5) |
| not changed | `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `~/.claude/commands/sc/spec-panel.md` | the original stays the control; `tests/skills/test_spec_panel_review_loop.py` and `tests/skills/test_review_severity_rule.py` run unchanged |
| not changed | `HOW-WE-WORK.md` (both copies), `pragmatic.md` S1-S5, `docs/guides/*` | the variant is experimental and is not offered in routing until it has results |
| check, may need a row | tests that enumerate commands or skills: `tests/core/test_how_we_work_routing_table.py`, `tests/skills/test_sc_recommend_routing_contract.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/unit/test_cli_install.py`, `tests/recommend/test_routing_refresh.py` | UNVERIFIED whether any of them fails on one extra command file and one extra skill folder; the first implementation task runs them and adds the plugin mirror only if a parity test demands it |

No project `.claude/` file is staged (`make sync-dev` copies the command and skill into the untracked dev copy). No `src/superclaude/` path appears in either new installed primitive; they name `~/.claude/skills/sc-fixcheck/` first and the project `.claude/skills/sc-fixcheck/` second, the order the dual-surface rule gives for skills.

### 4.2 Review Loop: bullets 1-7 unchanged, one new bullet (literal)

Bullet 6 (the Reviser contract) is kept byte for byte, so its pins (`Reviser brief`, `byte size before and after`) and the 427 tests that read it stay valid in the variant. It stays the scope rule in prose ("revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for"). Bullet 8 adds what bullet 6 could not do, a size and attribution rule a script can check. Bullet 7 (a brief may narrow, never widen) is what makes the minor budget binding over a task brief that says "apply every confirmed finding".

The line to append after bullet 7 (one line, like the others):

```markdown
8. **Fix budget**: the report carries a `fixbudget` block (one line per finding: id, severity, grade, `std|large|-`) and `reviewed_sha256`, and the `Reviser brief` also restates this bullet and the `## Fix Budget` section; the reviser answers a blocking finding by deleting, then narrowing, then replacing, and adds text only after writing in the ledger why none of those fits, changes a minor finding by at most 12 words and never grows the text, quotes the exact baseline sentence and the finding id of every change in a `fixledger` block of its disposition file, runs `fixcheck.py check` until it returns 0 or, after one cut-down pass, `enforce`, which restores the baseline text of whatever is still over budget or unattributed; a blocking finding it cannot fix within budget is listed `escalated` with what it needs, never expanded; a `--re-review` first runs `verify` on the receipt, shows each `escalated` id as `open`, and tags each `origin=changed` finding with `attacks: L<n>/<finding id>`.
```

### 4.3 The `## Fix Budget` section (literal text for the command file)

```markdown
## Fix Budget

Applies to a critique-mode report that ends `verdict: FAIL` below `review: 3`, and to the `--re-review` that follows it. The script is `fixcheck.py` in `~/.claude/skills/sc-fixcheck/scripts/` first, else the project `.claude/skills/sc-fixcheck/scripts/`, run as `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" <subcommand> ...` (`hash`, `snapshot`, `check`, `enforce`, `verify`). If `hash --file <spec>` cannot run, stop with `E-FIXCHECK-MISSING`, name both paths, and do not review.

Words are counted without finding-id tags such as `(F3)` and without `path:line` citations. Budget per finding:

| class | applies to | gross | net | add-only | entries | heading | id | table row | MUST/SHALL/must/never/always | only/every/exactly/none/total/closed | check recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CRITICAL blocking | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 1 |
| M | MAJOR blocking, FR-8, FR-9 | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 |
| m | every non-blocking finding | 12 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

All minor fixes together: 36 words. Net growth of the document per cycle: 10% of the baseline word count. At most 2 overrides per cycle (`override: gap-fill | multi-site | contradiction: <reason of at least 10 words>`, blocking findings only, doubles gross, net, add-only and entries for that finding, never lifts a heading or id limit). A finding the reviewer marks `large` has the doubled limits without using an override; at most a quarter of the blocking ids (rounded up) may carry it.

Exit codes of `check`: 0 within budget and every hunk attributed; 1 input error; 2 over budget or forbidden element; 3 ledger incomplete; 4 override refused.

Add to the report: a `fixbudget` block (`review: N of 3`, `reviewed_sha256: <hex from hash>`, `refs: <prefix>`, then `<id> | <severity> | <grade> | std|large|-` per finding); on a `--re-review`, a header line `fixcheck: OK|STALE|MISSING` from `verify`, the status `open (escalated: budget)` and its one-line need for each escalated id, and `attacks: L<n>/<finding id>` on each `origin=changed` finding. Copy only numbers and ids from the receipt, never the reviser's reasons.

Reviser brief (place above the final `verdict:` line; fill `<...>`):
> Reviser brief, fix budget on. Fix only these blocking ids: <ids>. Every other finding is a minor note: change nothing for it beyond 12 words and write `deferred (minor, fixcheck budget 0)` in its disposition row; a task brief that says to apply every finding is narrowed to this list (Review Loop bullet 7).
> 1. Before the first edit run `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" snapshot --spec <spec> --report <this report>` (the script writes `<report dir>/.fixcheck/base-<N>.md` and stops if the spec changed since this review).
> 2. Answer each id by deleting the wrong sentence, else narrowing it, else replacing it; add text only after writing in the ledger why none of those fits. Per finding: CRITICAL 120 words added (net 80), MAJOR 80 (net 50), MAJOR at most 4 ledger entries, no new heading, id or section, at most one new table row, one new MUST/SHALL/must/never/always, one new only/every/exactly/none/total/closed and one new check recipe.
> 3. Write, as a fenced `fixledger` block at the end of your disposition file (it is one of your output files; do not create others), per change one entry with `finding`, `op` (delete|narrow|replace|add), the exact baseline sentence as `old` (for an add, as `anchor`), the first 10 new words as `new`, and `considered` for an add. A finding you cannot fix inside its budget goes under `## deferred` as `<id>: escalated: <what it needs>`. Do not expand it to fit.
> 4. Run `... check --baseline <report dir>/.fixcheck/base-<N>.md --revised <spec> --report <this report> --ledger <your disposition file>`. Exit 0 is required. On 2, 3 or 4 cut the named entries down or add the missing entry, then run it once more; if it is still not 0 run `enforce` with the same arguments plus `--in-place`, then `check` again.
> 5. In your report give the byte size before and after and paste the last `FIXCHECK` line.
```

### 4.4 Script outline (`fixcheck.py`, about 350 lines, stdlib only)

```python
BUDGETS = {  # the command's table must equal this: test M4
  "C": dict(gross=120, net=80, add_only=80, entries=6, heading=0, id=0, row=1, norm=2, univ=1, exec=1),
  "M": dict(gross=80,  net=50, add_only=50, entries=4, heading=0, id=0, row=1, norm=1, univ=1, exec=1),
  "m": dict(gross=12,  net=0,  add_only=0,  entries=1, heading=0, id=0, row=0, norm=0, univ=0, exec=0),
}
MINOR_CYCLE_GROSS, CYCLE_GROWTH_PCT, MAX_OVERRIDES, LARGE_SHARE = 36, 10.0, 2, 0.25
EXIT = {"OK": 0, "INPUT": 1, "OVER": 2, "LEDGER": 3, "OVERRIDE": 4}

main(argv)                       # argparse subcommands: hash snapshot check enforce verify
read_text(path)                  # exit 1 with a named message if unreadable or empty
parse_fixbudget(report_text)     # fenced ```fixbudget block -> {id: (severity, grade, budget)}, reviewed_sha256, refs
classify(severity, grade, budget)  # 'C' | 'M' | 'm'
parse_ledger(text)               # takes the fenced ```fixledger block when the file has one (the disposition file), else the whole file; '## L<n>' entries (key: value lines) and '## deferred' lines
units(text)                      # normalise; split on lines, sentences, table cells; keep (unit, line_no)
words(unit_list)                 # drop (F3)/[N2] tags, path:line citations, pipes, heading marks, emphasis
diff_hunks(base_units, new_units)  # SequenceMatcher(autojunk=False) -> hunks (i1,i2,j1,j2); mark moved units
hunk_counts(old, new)            # word-level SequenceMatcher -> added, deleted, op in {delete,narrow,replace,add}
attribute(hunks, entries)        # old-quote containment / anchor match / 'new' prefix; derive real op; mismatch -> LEDGER error
element_counts(old, new)         # headings (ratio<0.8 vs every baseline heading), ids (regex), rows, norm, univ, exec
score(findings, classes, overrides, large_flags)   # per finding gross/net/add_only/entries/forbidden -> status + reasons
cycle_checks(totals)             # minor total 36, growth 10%, override count, large share
check(args) -> int               # builds the report and the receipt, returns the exit code by the order 1, 3, 4, 2
enforce(args) -> int             # reverts whole failing findings and unattributed hunks, writes atomically, re-runs check
verify(args) -> int              # sha256 of --revised against receipt.revised_sha256, and (when --ledger is given) a silent re-run of check compared with the receipt totals, so a hand-written receipt is caught: 0 OK, 2 STALE or MISMATCH, 1 MISSING
render_report(result) / receipt_json(result)       # formats of section 2
```

Properties the tests pin: `enforce` followed by `check` returns 0 for every input that `check` can score; `check` never writes the spec; `moved` text counts zero; the same inputs give the same output (no clock, no randomness; the receipt carries no timestamp); a 60 KB specification is checked in well under a second (UNVERIFIED, expected from the word-level diffs run for this analysis, which took seconds for 12 pairs).

### 4.5 Tests

`tests/skills/test_sc_fixcheck.py` (loads the script by `importlib.util.spec_from_file_location`, `tmp_path` fixtures, no network):
1. clean within-budget fix: exit 0. 2. MAJOR fix of 81 added words: exit 2, reason `gross`. 3. net 51 with gross 60: exit 2, reason `net`. 4. minor fix of 13 words, or of 12 words with net +1: exit 2. 5. new heading, new id, new table row beyond 1, a second MUST: each exit 2 with its own reason. 6. a hunk with no ledger entry: exit 3. 7. a quote that is not in the baseline: exit 3. 8. mislabelled `op`: exit 3. 9. a blocking id neither fixed nor under `## deferred`: exit 3. 10. override accepted once and twice, refused third (exit 4), refused on a minor finding (exit 4), never lifts a heading limit. 11. `large` flag doubles the limits; a fifth flag among four blocking ids is ignored. 12. moved sentence counts zero. 13. a tag `(F3)` and a `path:line` token add zero words. 14. `enforce` restores baseline text for the over-budget finding and the unattributed hunk, leaves the within-budget finding, then `check` returns 0; running `enforce` twice changes nothing more. 15. `enforce` without a ledger: exit 1 and the spec unchanged. 16. `snapshot` refuses a changed spec (exit 1, `STALE-BASE`). 17. `verify`: OK, STALE after one byte appended, MISSING. 18. cycle growth above 10% reverts the largest finding first. 19. a property test: random edits of a fixed spec with random ledgers always satisfy "after `enforce`, `check` is 0".

`tests/skills/test_spec_panel_minfix.py` (text pins, honest about what they prove):
- M1 frontmatter `name: spec-panel-minfix`; usage lines start `/sc:spec-panel-minfix `.
- M2 faithful copy: after removing the frontmatter, the command-name substitution, bullet 8 and the `## Fix Budget` section, the file equals `src/superclaude/commands/spec-panel.md` line for line (so a later edit of the original that is not mirrored fails the test).
- M3 bullets 1 to 7 equal the original's; bullet 8 is one line starting `8. **Fix budget**`; the `## Fix Budget` heading sits between `## Review Loop` and `## Output Formats`.
- M4 number sync: the budget table in the command equals `BUDGETS`, the cycle limits equal the constants, and the exit-code line equals `EXIT` (prose and script cannot drift apart silently).
- M5 literal `~/.claude/skills/sc-fixcheck/scripts/` before `.claude/skills/sc-fixcheck/scripts/`; the literal `E-FIXCHECK-MISSING`; no `src/superclaude` in the command or the skill.
- M6 the Reviser brief template contains the five numbered steps and the words `deferred (minor, fixcheck budget 0)`.
- M7 stays green without edit: `test_spec_panel_review_loop.py`, `test_review_severity_rule.py`. The severity test scans command text for old-cap and any-severity phrases; whether bullet 8's numbers ("at most 2 overrides", "at most 4 ledger entries") trip its cap-number matcher is UNVERIFIED and is the first thing the implementer runs; reword the numbers into the table if it does.

What these tests do not prove: that a reviser runs the commands, or that a reviewer writes a correct `fixbudget` block. The receipt and the `fixcheck:` header line are the runtime evidence.

### 4.6 Later adopters (not part of this change)

The script is keyed on (baseline, revised, ledger, findings block), not on `spec-panel`. `/sc:reflect` Tier-3 remediation and rf-qa's Fix Cycle (`rf-qa.md` lines 379-416, 2-cycle cap) would need only a reviewer-side `fixbudget` block and a reviser-side instruction to run the same five commands; rf-qa's CRITICAL/IMPORTANT/MINOR map to classes C/M/m through a `--class-map CRITICAL=C,IMPORTANT=M,MINOR=m` option that does not exist yet. The `/sc:implement` final review changes code, where words are the wrong unit: it needs a `--unit line` mode (UNVERIFIED design). Each adopter runs its own S1-style measurement first; I claim nothing for them.

## 5. Variant command name and install note

**Name:** command `spec-panel-minfix`, invoked as `/sc:spec-panel-minfix` (Skill target `sc:spec-panel-minfix`). Checker skill folder `sc-fixcheck`. The original `spec-panel` is not edited anywhere: the variant is a new command file plus a new skill folder, so the control arm keeps running the original text beside it (D9: parallel arms need different command names).

**Installing beside the original, in the repository (after merge):** `superclaude install` already copies every `commands/*.md` into `~/.claude/commands/sc/` and every skill directory into `~/.claude/skills/`, and skips an existing command file unless `--force` (`install_commands.py` lines 60-90, `install_skills.py` directory copy). A new `spec-panel-minfix.md` and a new `sc-fixcheck/` therefore land next to `spec-panel.md` and do not touch it.

**Installing before merge, for the experiment (additive, no package reinstall, no `--force`; run by the owner or coordinator, not by a worker; the command file is the experiment build described under "Base text" below):**

```bash
cp -n <variant checkout>/src/superclaude/commands/spec-panel-minfix.md ~/.claude/commands/sc/spec-panel-minfix.md
mkdir -p ~/.claude/skills && cp -rn <variant checkout>/src/superclaude/skills/sc-fixcheck ~/.claude/skills/
sha256sum ~/.claude/commands/sc/spec-panel.md ~/.claude/commands/sc/spec-panel-minfix.md ~/.claude/skills/sc-fixcheck/scripts/fixcheck.py   # log in the install watcher
```

(Which of `install_skill.py` or `install_skills.py` performs the directory copy on the install path is UNVERIFIED; both appear under `cli/`.) `cp -n` never overwrites; `~/.claude/commands/sc/spec-panel.md` is not an argument of any command above. Per D9 a fresh worker loads commands from `~/.claude/commands/sc/` (personal beats project), so this is the only copy that matters on this machine. The existing install watcher (phase4 `install-watch.log`) gets two more sha256 lines; a change of either file during an arm voids V6 as before.

**How the checker reaches a worker whose repo base (commit 2cb683f5) has none of the new code:** it does not come from the repository at all. The command text points at `~/.claude/skills/sc-fixcheck/scripts/fixcheck.py` (the home directory, outside every worktree) and the script is stdlib only and run as `uv run --no-project python "<path>"`, which needs no `pyproject.toml`, no virtual environment and no `superclaude` import. Precedent for exactly this pattern: `sc-issue-protocol/SKILL.md:72,84` runs `origin_repo.py` that way in any project. The project copy `.claude/skills/sc-fixcheck/` (from `make sync-dev` in a dev checkout) is the second surface, read only if the home copy is absent. Pre-flight before dispatch, from inside one experiment worktree: `uv run --no-project python ~/.claude/skills/sc-fixcheck/scripts/fixcheck.py hash --file README.md` must print a 64-hex hash and exit 0. If a worker's home copy is missing the command stops with `E-FIXCHECK-MISSING` instead of silently reviewing without the budget.

**Base text for the experiment file.** Arms A and B ran the exact 427 text (472 lines, sha256 c8d80346a96c, `git show 95f2c6e4:src/superclaude/commands/spec-panel.md`). The current `src/` file (486 lines) adds unattended-mode lines that S1 does not exercise (no brief passes `--unattended`, and `WORKER-CONTRACT.md` is moved aside), but D10/D11 changed one thing at a time and this arm should too. So the file installed for Arm C is the same change (frontmatter name, command-name tokens, bullet 8, `## Fix Budget`) applied to the 472-line 427 text, and the repository file is the same change applied to current `src/`. The added hunks are byte-identical in both; a plain `diff` of the two variant files must show only the lines in which `spec-panel.md` itself differs between the two bases. Record both sha256 values in the install watcher.

**The one-line substitution an experiment brief needs.** Arm C briefs are Arm B's briefs (D11) with this single substitution applied to the review briefs T05, T07-template and T09-template; reviser briefs T06 and T08 stay verbatim (the reviser learns the budget from the report):

```text
s#/sc:spec-panel @#/sc:spec-panel-minfix @#
```

R2 and R3 review briefs keep Arm B's appended `--re-review <prior report> --baseline <saved copy>` flags, because the variant is built on 427's re-review. Record the substitution in the coordinator log as D9 requires. Nothing else in any brief changes; in particular no brief mentions the checker, the ledger or the budget.

## 6. Measurement plan and predicted numbers

### 6.1 Design (Arm C, same shape as D10/D11)

Scenario S1 (Orca worker-contract spec, 57,763 bytes, 8,148 words), base commit 2cb683f5, same overlay, same verbatim briefs, same model (claude-opus-5-5), `WORKER-CONTRACT.md` moved aside, same loop (3 reviews, 2 fix cycles), two fresh worktrees `exp346-ab-min-r1` and `exp346-ab-min-r2`. Briefs: Arm B's, with the single substitution of section 5. Comparators: ctl-r1, ctl-r2 (reused as in D11), arm A (trt-r1, trt-r2) and Arm B (flg-r1, flg-r2) as secondary. Because the command names differ, the arm can run at the same time as new control replicates (D9), which removes the time-separation limit D11 had to state.

Bar, fixed now and the same as D11: (a) review-3 critical+major proxy mean at most 3 (50% of the control mean 6.0) **and** every replicate better than every control replicate, which with control values 8 and 4 means each replicate at most 3; or a clean pass sooner; (b) growth after two fix cycles at most 44.4% (70% of 63.5%), every replicate below both controls; (c) effect larger than the larger within-arm spread. Validity V1-V6 as in D10/D11, plus V7 below.

Metrics, per round, as D5, plus these that only this arm can produce:
- V7 (mechanism honoured): `.fixcheck/receipt-1.json` and `receipt-2.json` exist, `exit` = 0, and the next review's header says `fixcheck: OK`. A replicate with a MISSING or STALE header, or whose reviser never ran the checker, is recorded "mechanism not honoured" and does not count as treatment (the D11 rule for ignored flags).
- Growth in bytes and in words, from the receipts and from the history copies.
- Per cycle: blocking ids, ids `escalated` for budget, overrides used, hunks unattributed before `enforce`, hunks reverted by `enforce`, minor words applied (must be at most 36), reviser tool calls and wall minutes.
- Chain data: from `attacks: L<n>/<id>` on every `origin=changed` finding, children per ledger entry by `op`, gross words, class and by whether the parent finding was blocking. This turns the hand trace of section 1.3 into a column and lets the second experiment fit the child rate against the five classes of section 1.4 with more than 13 items.
- Severity: for each chain, parent grade against child grade (the drift measure the 427 data could only show as a per-round share).

### 6.2 Predicted growth after two fix cycles (bar: at most 44.4%)

Measured inputs: flg-r2 tagged words by class (section 1.2, 1.6), 427 mean net growth 30.7% in words across the four 427 loops (23.7, 38.2, 27.8, 33.1).

- Replay on flg-r2 (the only loop with every change tagged): capping blocking fixes at 80/120 and dropping the 773 minor words removes 1,260 of 2,721 tagged words; the 260 untagged words of the new section 2.4 table fall under F2's 80 and are not additional. New gross about 1,461, deletions kept at the measured 287, net about 1,174 words, 14.4% against the actual 33.1%. The same ratio (0.435) on the four 427 loops gives 13.4%. The net caps (50 and 80) and delete-first push this lower, the ten percent per cycle cap and the `large` flags push it up a little.
- Arithmetic upper bound if the checker is honoured and every fix sits exactly at its cap: cycle 1 at most 17 blocking ids (the highest proxy seen at review 1) times net 50, plus the two CRITICAL extras, plus 2 overrides, is above the 10% cycle cap, so cycle 1 is capped at 815 words; cycle 2 at most 8 ids times 50 plus 100 for overrides is 500 words; total 1,315 words, **16.1%**. That bound needs no judgement about model behaviour, only that the script runs.
- **Prediction: 13% (range 8% to 17%), both replicates below 20%.** Bar (b) is met by a wide margin if V7 holds. If V7 fails the number is meaningless and the replicate is discarded.

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

**Prediction: mean review-3 proxy 3.0, band 2.1 to 4.0.** With the 427 per-replicate spread (1 to 6), P(mean at most 3) is about 0.5, P(both replicates at most 3, which is bar (a)) about 0.3, and P(mean below the 427 value of 5.5) about 0.85. I state these because the bar is set at the edge of the plausible range, not inside it. The two assumed rows decide the outcome and the experiment measures both (`attacks:` chains): that is the second use of Arm C.

Other predictions, each with the measured number it starts from:
- Escalated blocking ids at review 2: 1 to 3 of about 6 to 13 (the replay put 11 of 17 MAJOR fixes over the 80-word cap and the reviewer's recommendations are 7 to 39 words, so most need a cut-down, a few an escalation).
- Blocking children per blocking fix: 0.30 (427: 0.46 for flg-r2 R1 to R2, 0.17 for R2 to R3).
- Share of new findings that are `origin=changed`: still 85% to 100%. This is expected and is not a success measure; do not read it as a failure either.
- Clean PASS within the cap: at most one of two replicates (flg-r2 would have passed at review 3 without the F22 chain; I treat that as luck, not a prediction).

### 6.4 What result would mean the idea failed

| result in valid (V7) replicates | reading |
|---|---|
| mean review-3 proxy 5 or more, or both replicates 4 or more with growth under 20% | The central claim fails: minimal fixes do not lower review-3 blocking, they only repeat 427's growth cut. Stop this theme; the size budget is then a growth tool 427 already provides. |
| any replicate review-3 proxy 8 or more, or mean open blocking including escalated at review 3 at or above the control mean 6.0 | The mechanism makes the loop worse (under-fixing). Stop. |
| growth above 30% in a valid replicate | The caps did not bind: an implementation or honouring failure, not a test of the idea. Fix and rerun. |
| ids `escalated` for budget exceed 40% of review-1 blocking ids in both replicates | Budget too tight. One pre-registered retry at 100/60 (CRITICAL 150/100) and report both settings; do not average them. |
| growth bar met, mean proxy 3.5 to 4.5, both replicates below 6 | Promising, not proven: extend to four replicates per arm before any adoption. |
| mean proxy at most 3 and each replicate at most 3, growth under 20%, V7 holds | Bar met on S1 (n = 1 scenario, 2 replicates); adoption by other review commands is a separate measurement. |

Cost of the measurement: the same sessions as Arm B (5 worker sessions per replicate: 3 reviews and 2 revisions; the checker adds tool calls, not sessions), plus the analyst time to read the receipts.

## 7. Risks, costs and what would falsify it

### 7.1 Cost per loop (honest, mostly UNVERIFIED because tool-call counts of the S1 sessions were not measured)

| item | reviser (per fix cycle) | reviewer (per review) | per loop of 3 reviews and 2 cycles |
|---|---|---|---|
| extra tool calls | `snapshot` 1, ledger append 1, `check` 1, cut-down edits 2 to 6, second `check` 1, `enforce` and last `check` 0 to 2: 5 to 11 | `hash` or `verify` 1, `Read` of the receipt 1 (re-review), `fixbudget` block is part of the report write: about 2 to 3 | about 20 to 31 |
| extra sessions | 0 | 0 | 0 (cut-down is inside the reviser session; no separate retry session) |
| extra wall time | 3 to 8 minutes of model time (ledger of 6 to 20 entries, one shortening pass); each script call under a second (UNVERIFIED, expected from the diff runs for this analysis) | 1 to 2 minutes | about 8 to 18 minutes on a loop that took about 78 minutes for control (05:05 to 06:23Z), so 10% to 23% |
| extra context | a ledger of about 2 to 4 KB, a check report of about 1 KB | the receipt, about 3 to 5 KB | small against 40 to 50 KB review reports |
| new files | none authored by the model; `.fixcheck/` is script output | the report gains a block | one hidden folder per report folder |

### 7.2 Ways the mechanism can make the loop worse

| # | failure | why it can happen (evidence) | detection | mitigation | residual |
|---|---|---|---|---|---|
| 1 | Under-fixing leaves blocking findings open | the replay put 11 of 17 MAJOR fixes over the 80-word cap (section 1.6); a fix cut to fit may lose its content; `enforce` reverts whole findings | `escalated` ids and `status: reverted` in the receipt; review-2 table `open (escalated: budget)` | the 80-word cap is about twice the longest reviewer recommendation in flg-r2 round 2 (39 words; median 24); `large` and 2 overrides per cycle; one pre-registered retry at 100/60 (section 6.4) | a finding that needs a real mechanism is left to the user at review 3, by design; the review-3 count includes it, so this failure shows up in the very metric the bar uses |
| 2 | Consistency residue from not propagating a rule | ctl-r1 R2 has findings labelled "Residue of round-1 finding 5" (N4: AC-4.3 contradicts WC-10's new exemption) and "Residue of round-1 finding 8" (N2); flg-r2's fixes touched 3 to 5 sites each (F1: WC-4, WC-5, 7.2 step 4, Decisions; F10: five sites) | `attacks:` children whose parent entry has `named: no` or fewer entries than sites | 4 entries per MAJOR, `multi-site` and `contradiction` overrides | two overrides per cycle may be too few; open question 2. This is the real tension of the theme: the ctl-r1 residue findings are what propagation prevents, and the flg-r2 N3/N6 findings are what propagation causes |
| 3 | Gaming the counter by rewording | gross counts changed tokens, not sentences, so rewording burns budget; `moved` needs exact equality; a split of one addition over two findings' entries is possible; synonyms ("solely", "each", "exclusively") evade the universal-token list; padding deletions can buy net room (gross still binds) | `named` flags, `attacks:` data, reviewer re-raising a deleted statement as a gap | per-finding gross cap, entries cap, 36-word minor total | the lexical gates (universal tokens, check recipes) are tripwires, not proofs; their precision is UNVERIFIED |
| 4 | Escalation replaces fixes | escalating is cheaper than fixing; the reviser decides what is "over budget" | escalated share per cycle in the receipts | the ledger must state what the fix needs in words (checkable against the cap by a reader); the reviewer re-lists the id as `open` | no automatic cap on the escalated share in v1 (open question 3); a high share is read as "budget too tight" (6.4) or "reviser dodging" and the two look alike |
| 5 | Checker false positives on legitimate edits | renumbering or inserting a numbered item creates "new ids" (AC-1.4 becomes AC-1.5); a table column change touches every row; heading rewording; curly quotes or changed backticks make a ledger quote fail to match (exit 3); the exec detector may fire on a spec that documents shell commands | exit 2 or 3 on an edit the reader judges legitimate | heading ratio 0.8; whitespace, emphasis, quote and table-padding normalisation; 40-character unique-substring quote match; the id gate counts only ids absent from the baseline | renumbering is not overridable in v1 and must be escalated; a `renumber: yes` ledger field is the likely first change (open question 4) |
| 6 | The reviser does not run the checker, or the task brief outranks the Reviser brief | flg-r1 `disposition.md`: "The Task 6 brief wins" (scope, not tools) | `fixcheck: MISSING` or `STALE` in the next header; V7 fails | a one-replicate pilot before the n = 2 arm: if the pilot reviser skips the commands, the Reviser brief text is changed, not the design; the commands are procedural and do not contradict the task brief | prose compliance, and the cost of a wasted replicate. Tests prove the text exists, not that a model obeys it |
| 7 | Ownership clause of the reviser brief ("write ONLY your output file(s)") read to forbid new files | `.fixcheck/` files | worker asks or skips | the ledger lives in the disposition file the brief requires, and the script writes the other files; the Reviser brief says so | a literal-minded reviser may still refuse to run a script; pilot catches it |
| 8 | Wrong `fixbudget` block | the reviewer mislabels a grade or id; budgets then apply to the wrong class | `snapshot` and `check` validate that every id of the block appears in the report body and that classes parse; mismatch is exit 1 | the block is generated from the same finding list the report already has | a consistently wrong grade is a grading error, which the budget cannot see |
| 9 | Minor corrections of real errors are left in the spec | minor budget is 12 words; flg-r1 R2-5 (`--output` should be `--output-dir`) and R2-6 are real wrong statements | the minor note stays in each later report | one-token corrections fit the budget (R2-5 is 2 words) | longer minor corrections are deferred by design, which is 427's own rule ("minor findings never trigger a revision") now enforced |
| 10 | The reviewer anchors on `attacks:` and attacks changed text harder | the tag invites a look at ledger entries | `origin=changed` share rising above the 427 level | the tag is written after the finding, from the receipt's line map; the reviewer never sees ledger prose | prose |
| 11 | Receipt forged by hand | a model can write JSON | `verify` re-runs `check` on the base copy, the spec and the disposition's ledger and compares totals | stdlib only, deterministic | an agent set on cheating can edit the base copy too; this is not a security boundary |

### 7.3 What is prose only, and the residual risk

- "Delete before narrow before replace before add": the ladder is enforced only by tiered caps (add-only 50 against gross 80) and by a `considered:` sentence whose truth nothing checks. Residual: the reviser can choose `replace` where `delete` existed.
- "Reviser runs the checker": procedural prose in the report; evidence is the receipt.
- "Reviewer writes `fixbudget` and `attacks:` from the receipt, not from ledger prose": prose; measured by the format of the report.
- Lexical gates (universal tokens, check recipes): heuristics.

### 7.4 What would falsify the idea

Section 6.4 lists the result thresholds. In one sentence: if valid replicates show growth under 20% and review-3 critical+major at 5 or more (or any replicate at 8 or more), minimal fixes do not remove the fix-induced findings that matter, and the next lever is on the review side (diffgate, stoprule, ledger themes), not on the reviser side.

## 8. Open questions

1. **Are 80/50, 120/80 and 12/0 the right first values?** They come from one fully tagged loop (flg-r2: the replay of section 1.6) and from reviewer recommendations of 7 to 39 words. A relative budget (for example the larger of 40 and three times the words of the reviewer's recommendation) would track the reviewer's ask better, but needs the recommendation size in the `fixbudget` block, and the 3.6 times reviser ratio of section 1.2 suggests that a factor of 2 to 3 would still bind. I chose absolute numbers because the script can check them without parsing recommendations. Calibrate on the other five loops before the experiment (question 9).
2. **Is 2 overrides per cycle enough for propagation?** The tension in 7.2 row 2 (ctl-r1 residue findings against flg-r2 N3/N6) is unresolved by data. If the override count sits at the limit in both cycles of both replicates, the entry cap (4 per MAJOR) is probably what is too low, not the override count.
3. **Should the loop get an early, computed escalation?** The checker could print `ESCALATE-NOW` when escalated ids exceed 40% of blocking ids after cycle 1, letting the coordinator stop before review 3. It would shorten hopeless loops but change the cap semantics that 427 pins; not added in v1.
4. **Renumbering and the id gate.** Inserting AC-1.4 renames later ids and looks like new ids. A `renumber: yes` ledger field that exempts ids shifted within an existing prefix is the likely first fix; not in v1 because it creates a loophole that needs its own test.
5. **Should `named` become a hard gate?** It measures 427's "revise only text a blocking finding names" per entry; I kept it informational because propagation (question 2) is legitimate. Decide after Arm C shows the share of `named: no` entries among the parents of blocking children.
6. **Minor budget 12 or 0?** One-token corrections fix real errors (R2-5), but each changed citation is a new attack surface (flg-r2 Part 2 flagged 4 of 28 changed citations; flg-r1 R3-5, R3-6 are minor children of citation edits). A strict 0 would be a cleaner mechanical rule; 12 keeps the spec from carrying known wrong examples.
7. **Ledger visibility for the next review.** I chose: the reviewer sees the receipt (ids, numbers, line map), never the ledger prose, to avoid anchoring on the reviser's reasons (flg-r2 round 3 explicitly decided each status "by reading the spec text at the cited line, not `disposition-round2.md`"). The alternative, an attack map, may raise `origin=changed` findings. Untested.
8. **A reviewer-side companion rule.** In flg-r1 R2-1 and R2-3 the reviewer offered the deletion or narrow option second. A one-line instruction "list the deleting or narrowing option first and give each option a word count" would cost nothing and addresses class D and part of class E, but it is a change to the reviewer, so it stays outside this theme's scope; flagged for the merge with the other variants.
9. **First implementation task: replay harness.** Run the finished script over the six recorded loops (baseline = previous history copy, ledger synthesised from each disposition table) and compare its per-finding gross words and over-cap counts with section 1.6; a deviation above 10% means the tokenisation rules (tags, citations, pipes) need work before any worker sees them. Also decide whether `uv run --no-project` is acceptable offline (UNVERIFIED; the `sc-issue-protocol` precedent suggests yes, as no dependency is resolved).
10. **Folding into `spec-panel` after a pass.** The variant exists so the original and its 427 pin (T3 requires exactly seven bullets) stay untouched. If Arm C passes, merging bullet 8 and the `## Fix Budget` section into `spec-panel.md` is a separate change that must update the pin test and the plugin mirror; and `/sc:reflect`, rf-qa and `/sc:implement` adoption (section 4.6) each need their own measurement, because the unit (sentences of a spec) does not carry over to code.
11. **FR-8 and FR-9 classes.** Class M applies to every finding the report grades blocking, FR-8 and FR-9 findings included when graded blocking (427 bullet 2). A GAP the reviewer grades minor under the concrete-outcome test (flg-r1 R3-7, R3-8) gets the minor budget and is not fixed. Whether that matches what the owner wants from FR-8/FR-9 "hard gates" is a question for the owner, not for this design.
