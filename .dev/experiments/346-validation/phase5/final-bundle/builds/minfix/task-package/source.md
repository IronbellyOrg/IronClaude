# SPEC: spec-panel-minfix (issue #346, theme "minfix": fix-minimality on the reviser side)

Status: design only, nothing implemented. Produced by team minfix from `/sc:brainstorm` (artifacts in this folder). Builds on PR 427 (`## Review Loop` in `src/superclaude/commands/spec-panel.md`).

Review status: three independent reviews, the cap (`spec-review.md` FAIL with 6 blocking, all resolved; `spec-review-round2.md` FAIL with 2 new blocking, 1 resolved; `spec-review-round3.md` FAIL with 2 blocking: the leftover SR2-B1 case and SR3-B1). The reviewer's exact one-sentence corrections for those two were applied after review 3 (section 2.2) and are NOT reviewed. They are escalated as open: both concern how `fixcheck.py` scores entries after `--enforce`, and the replay harness (open question 1) is the first place they would be tested.

## 1. Problem and evidence
- PR 427 halves growth (control +63.5%, 427 +29.7%, 427 with its flags +30.0% after two fix cycles) but not review-3 open critical+major (control 6.0, 427 5.5, flags 3.5; bar 3 or fewer); no run passed. 89-100% of new findings sit on text the last fix changed.
- Under 427, revisers still add 955-2,244 words per cycle against 84-258 deleted (control: up to 3,327 added), about 3.6 times the words the reviewer recommended, and spend 20-44% of their words on non-blocking findings (flg-r2), because the task brief ("apply confirmed findings") outranks 427's prose bullet 6 ("The Task 6 brief wins", flg-r1 disposition).
- In the 13 traced fix-to-child chains (flg-r1, flg-r2; one analyst, UNVERIFIED by a second reader), 11 come from four fix shapes: A fixing a non-blocking finding (3), B adding a universal or closed claim (2), C adding a check recipe or acceptance step (3), D adding a mechanism where the reviewer offered a deletion (3). The other 2 (shape E) are flawed reviewer recommendations or two fixes interacting.
- Size alone does not predict a blocking child (fixes with one average 114 added words, fixes without 105), so a pure size cap cuts growth but not review-3 blocking. The design therefore caps size AND gates the four shapes.
- 427's own design rejected a size limit because "nothing could check it from text" (`docs/designs/spec-panel-review-loop.md:73`). This spec adds the script that checks it.

## 2. Mechanism
One sentence: the reviewer gives every finding a budget class in a machine-readable block; the reviser fixes blocking findings only, by delete, then narrow, then replace, then add, and records each change in a ledger; a stdlib script (`fixcheck.py`) diffs the saved copy against the revised spec at sentence and word level, charges every changed span to a finding, enforces the budget, and itself reverts whatever is still over budget; the next review re-runs the script and never credits an over-budget fix. 427's 3-review cap, grading rule, `verdict:` line and re-review flags stay as they are. The coordinator gets no new duty.

### 2.1 Loop steps, in order

**Step 0, availability (every critique-mode run).** `spec-panel-minfix` first runs `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" hash --file <spec>`. If that fails it stops with `E-FIXCHECK-MISSING`, naming both install paths (`~/.claude/skills/sc-fixcheck/`, then project `.claude/skills/sc-fixcheck/`). It never falls back silently to plain 427 behaviour.

**Step 1, review N (reviewer).** It reviews as 427 says (bullets 1-5). It runs `hash` on the spec it reviews, at EVERY review (first review and re-review), and writes the result as `reviewed_sha256` in the report. (The merged brainstorm text runs `hash` only at the first review; that would leave review 2's block without a hash and stop cycle 2 with exit 3. This spec corrects it.) It writes a fenced `fixbudget` block: one line per finding of this review, plus one line per prior blocking id still open or regressed (so a finding escalated in cycle 1 gets a budget again in cycle 2). `refs` names the citation prefix the report uses for spec lines (`SPEC`, `SPEC2`, ...):

```fixbudget
review: 1 of 3
reviewed_sha256: <64 hex>
refs: SPEC
# id | severity | grade | budget
F1 | CRITICAL | blocking | std
F2 | MAJOR | blocking | std
F3 | MAJOR/FR-8 | blocking | gap:2
F4 | MAJOR | blocking | override
F14 | MAJOR | minor | -
override-reason: F4 <why no in-budget fix can close it>
```

`grade` is 427's blocking or minor. `budget` is `std`, `override` (at most one per report, blocking only, never on an `origin=changed` finding, needs an `override-reason` line), `gap:<n>` (a blocking FR-8/FR-9 gap fill naming n guard-table rows), or `-` (minor). A `CRITICAL`, `MAJOR/FR-8` or `MAJOR/FR-9` line graded minor prints `GRADE-CONFLICT <id>` and keeps budget 0; it is not an input error. If the verdict is FAIL below `review: 3`, the report carries the Reviser brief (literal text in section 3.2, item 5).

**Step 2, fix cycle (reviser, a separate agent reading the report).**
1. Baseline: before the first edit the reviser runs `snapshot --spec <spec> --report <report>`. The script, not the model, writes `<report dir>/.fixcheck/base-<N>.md` and refuses (exit 4, `STALE-BASE`) if the spec's sha256 differs from this report's `reviewed_sha256`. The `--baseline` passed to a re-review is the text the PREVIOUS review saw and is never this cycle's baseline: in Arm B's briefs the review before cycle 1 (T05) names no copy, and the review before cycle 2 (T07) names v1 while cycle 2 needs v2; no reviser brief names a copy. `snapshot` is therefore the normal path in both cycles.
2. Per blocking id: delete the wrong sentence or clause; else narrow it (no more words); else replace it (within the gross cap); else add, only after writing a `considered:` line (why delete or narrow fails). A finding that cannot be answered within budget goes under `## deferred` as `<id>: escalated: <what it needs>`. It is never expanded.
3. Non-blocking findings: no edit (budget 0). Their disposition row reads `deferred (minor, fixcheck budget 0)`. The checker, not the task brief, decides this.
4. Ledger: a fenced `fixledger` block at the end of the reviser's own disposition file (a file the brief already requires, so no new authored file). Its first line is `report: <file name of the review report it answers>`. Entries are numbered `## L1`, `## L2`, ...; one entry per change: `finding` (one id), `op` (delete|narrow|replace|add), `old` (the exact baseline sentence; for an add, `anchor`, the sentence it follows), `new` (first 10 new words), `considered` (for add), optional `depends: L<n>`.
5. Run `check --baseline <b> --revised <spec> --report <report> --ledger <disposition>`. It prints to stdout and writes nothing. Exit 1: cut the named entries down once and run `check` again; if it still exits 1, run `check --enforce`. That reverts each failing finding whole (plus findings whose entries `depends:` on it, plus unattributed hunks) to baseline text, lists each reverted finding as `escalated`, and re-checks. Exit 2: correct the call once and re-run. Exit 3, 4, 5 or 70, or a non-zero exit from `--enforce`: edit nothing more, paste the output.
6. Report the byte size before and after (427 bullet 6) and paste the final `FIXCHECK`, `result:` and `escalated:` lines.

**Step 3, review N+1 (re-review, 427 flags `--re-review <prior report> --baseline <saved copy>`).** After 427's own input and cap checks (bullets 1 and 4) and before the prior-blocking table, the reviewer runs `check` itself on (the saved copy passed as `--baseline`, which is exactly the text the prior review saw, the spec, the prior report) with no `--ledger` argument: the script then finds the one file in the prior report's directory whose `fixledger` block starts `report: <prior report's file name>` (none or more than one is exit 3). The reviewer puts `fixcheck: <exit> ...` in the header. This run is authoritative whether or not the reviser ran the script. A missing or malformed input, an exit 3, 4, 5 or 70, or a disposition whose last `FIXCHECK` line shows exit 3, 4, 5 or 70, stops the review with the named error and escalates to the user with the open blocking findings. It never falls back to a first review. An exit 2 from the reviewer's own call is corrected once and re-run. In the prior-blocking table an over-budget id shows `open (over budget)`, an escalated or reverted id `open (escalated: budget)` with its stated need, and an unanswered id `open (unanswered)`. Every `origin=changed` finding carries `attacks: L<n>/<finding id>`, taken from the run's per-hunk line whose revised line range contains the line the finding quotes, so fix-to-child chains become a computed column. The reviewer copies only ids and numbers from the run, never the reviser's prose reasons. Then step 1 again with `review: N+1 of 3`. At `review: 3` the run escalates as 427 says, now also listing each budget escalation with its need and each `GRADE-CONFLICT`: that is the justified escalation.

### 2.2 What the checker computes (stdlib `argparse difflib hashlib json re os tempfile pathlib`)

Normalise (line endings, whitespace, table padding, emphasis). Split into units per line, sentence and table cell. `difflib.SequenceMatcher(autojunk=False)` on units gives hunks; a word-level matcher inside each hunk counts added and deleted words. `path:line` citations, pipes and heading marks are not words (bytes count raw text). Identical moved units count zero. Attribution: a hunk belongs to the entry whose `old` quote it contains (or whose `anchor` precedes it) and whose `new` words start it. The script derives the real op and refuses a mislabelled one. A hunk that matches no entry is unattributed (policy failure), including one whose entry quotes text not in the baseline; the report prints the reason (`quote not in baseline`) on that hunk's line. Before attribution, a diff hunk that spans units claimed by more than one ledger entry is split per entry (each entry's `old`/`anchor` unit range), so two edits to neighbouring sentences are credited to both entries. An entry to which no hunk is attributed is `reverted` (status escalated, not a failure), whatever its text, and a reverted entry counts toward no per-finding total (entries, words, elements), so a plain `check` after `--enforce` scores cleanly. (These two sentences were added after review 3, the last review the cap allows; they are unreviewed, see open blocking items in `spec-review-round3.md`.) A blocking id with neither an entry nor a `## deferred` line is `unanswered`: it stays open and is reported, but is not an exit-1 reason (it adds no text). The report prints one line per hunk: `h<k> L<n>|unattributed <finding id> revised:<first line>-<last line> +<added words>/-<deleted words>`. A finding id written into the spec, such as `(F3)`, is a new id. Per finding it totals gross, net, add-only words, entries, new headings, ids, table rows, normative words (MUST SHALL must never always shall), universal words (only every exactly none total closed), condition words (if unless when whenever where except otherwise: each a new guard) and new check recipes (fenced blocks; backtick spans containing a shell word such as `grep`, `git `, `diff`, `find `, `uv `, a pipe or `$(`; bare `--flags` do not count). Output is deterministic (no clock, no randomness).

### 2.3 Budget (first values, calibrated on flg-r2: 11 of 17 MAJOR fixes there exceeded 80 words)

| class | gross | net | add-only | entries | heading | id | table row | normative | universal | condition | check recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CRITICAL (blocking) | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 2 | 1 |
| blocking MAJOR (incl. FR-8/FR-9) | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 (gap:n gives n) | 1 |
| minor (any non-blocking) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Cycle cap, overrides included: 600 gross added words and 6,144 gross added bytes, plus a raw file-size check (revised size minus baseline size at most 6,144 bytes, so whitespace or padding the normaliser ignores is still capped). Over the cap, `--enforce` reverts whole findings (blocking MAJOR before CRITICAL, largest first, then by id) and lists each as escalated. `delete` entries are free of the gross cap. `override` doubles gross, net, add-only and entries for one finding and never lifts the heading or id limit.

Exit codes (one list for every actor, pinned to the script constants): 0 accept; 1 policy failure, every reason tied to a hunk (over budget, forbidden element, cycle cap, unattributed hunk including a quote not in the baseline, mislabelled op on an attributed hunk, edit on a minor id); 2 usage; 3 bad input (missing or empty file, no `fixbudget` block, malformed or second override, ledger missing, not found or ambiguous); 4 hash conflict; 5 cannot write a file safely (the spec for `--enforce`, the copy for `snapshot`); 70 internal error. `--enforce` without `--ledger` uses the same lookup as `check`. `--enforce` exits 0 when its re-check is 0. That holds by construction: every exit-1 reason is a hunk that `--enforce` reverts, and if the raw size check still fails after the reverts (changes the normaliser ignores), `--enforce` restores the whole baseline file and lists every blocking id as escalated. Only `check --enforce` writes the spec, atomically. `spec-panel-minfix` itself never edits the spec (427 design C6).

### 2.4 Causes removed and causes left (constraint 1)

| measured cause | effect of this mechanism |
|---|---|
| fix-induced findings (`origin=changed` 89-100%) | NOT removed: any fix is changed text, so the share stays near 100%. The NUMBER of fix-induced findings should fall, because fewer, smaller fixes carry fewer new claims (shapes A-D gated); shape E (flawed recommendations, interacting fixes) is untouched |
| mechanisms and sections added for minor findings | REMOVED mechanically: minor budget 0, any hunk charged to a minor id fails and `--enforce` reverts it, whatever the task brief says |
| mechanism added where a deletion was on offer | REDUCED: tiered caps favour delete and narrow, `add` needs `considered:` (prose, unverifiable) |
| universal claims and new check recipes | REDUCED: at most one each per blocking fix (regex tripwires, precision unverified) |
| upward severity drift | PARTLY: text a minor finding names stays untouched, so it stays `origin=unchanged` and 427 bullet 5 caps it at minor. Drift on text the reviser did change, and FR-8/FR-9's forced MAJOR, remain. `attacks:` makes drift measurable per chain |
| no mechanical stop | PARTLY: computed stops added (cycle cap, one override, one cut-down then script revert, fail-closed inputs). The 3-review cap is still the only loop-level stop |
| growth | REMOVED as arithmetic if the script runs: at most 1,200 gross words (14.7% of 8,148) and 12,288 bytes (21.3%) over two cycles |
| whole-document attack on changed text | NOT removed (other themes) |

Prose-only parts and their residual risk: the delete-first order beyond the caps, the `considered:` line, "reviser runs the script", "reviewer copies only numbers from the run", and "no override on an `origin=changed` finding". The authoritative record is the re-review's own `check` run, so a reviser who skips the script is caught; a reviewer who skips its own run is not.

## 3. Exact changes
### 3.1 Files

| action | path | content |
|---|---|---|
| new | `src/superclaude/commands/spec-panel-minfix.md` | copy of the current `src/superclaude/commands/spec-panel.md` with only the regions of 3.2 changed |
| new | `src/superclaude/skills/sc-fixcheck/SKILL.md` | one page: purpose, subcommands, formats, exit codes; described as run by commands, not by users |
| new | `src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py` | about 350 lines, stdlib only, no `superclaude` import; run as `uv run --no-project python "<base>/scripts/fixcheck.py"` (precedent: `sc-issue-protocol/scripts/origin_repo.py`, `SKILL.md:72`) |
| new | `tests/skills/test_sc_fixcheck.py` | behaviour tests of the script (3.4) |
| new | `tests/skills/test_spec_panel_minfix.py` | text pins of the variant command (3.4) |
| unchanged | `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `~/.claude/commands/sc/spec-panel.md`, `HOW-WE-WORK.md`, `pragmatic.md`, `WORKER-CONTRACT.md` | the original stays the control; `test_spec_panel_review_loop.py`, `test_review_severity_rule.py`, `test_worker_contract.py` run unchanged |
| check first | `tests/core/test_how_we_work_routing_table.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/unit/test_cli_install.py`, `tests/skills/test_sc_recommend_routing_contract.py` | UNVERIFIED whether one extra command and one extra skill folder trip them; the first implementation task runs them and adds a plugin mirror only if a parity test demands it |

Never stage `.claude/` (`make sync-dev` creates the dev copy). Neither new installed primitive names a `src/superclaude/` path. Both look in `~/.claude/skills/sc-fixcheck/` first, then the project `.claude/skills/sc-fixcheck/` (dual-surface rule for skills).

### 3.2 `spec-panel-minfix.md`: the changed regions (everything else byte-identical)

1. Frontmatter `name: spec-panel-minfix`, description marked experimental; the command name in the title and Usage lines.
2. Repository file only: Usage line 2 drops `[--unattended] [--report-dir <dir>]`, and the `## Unattended mode` section is removed. `_check_no_unattended_sections` in `tests/skills/test_worker_contract.py` asserts the exact set of commands carrying that heading.
3. `## Review Loop` keeps seven bullets; bullets 1-5 and 7 are byte-identical. Bullet 6 is 427's text minus the clause "each added paragraph or table cites its finding id" (finding ids now live in the ledger; an id written into the spec fails the check), with this appended before its final period: `; the Reviser brief carries the ## Fix Budget steps, and a blocking finding the reviser cannot fix within budget is listed escalated with what it needs, never expanded`. The pins `Reviser brief` and `byte size before and after` stay. Bullet 7 (a brief may narrow, never widen) is what makes the minor budget outrank "apply every confirmed finding".
4. A new `## Fix Budget` section between `## Review Loop` and `## Output Formats`, literal text below.

Not changed: the existing Tool Coordination line that names `src/superclaude/examples/release-spec-template.md` (line 220) stays byte-identical. It is a pre-existing defect of `spec-panel.md` and out of this theme's scope. The new regions add no `src/superclaude/` path, but the new installed command inherits this one reference. The project rule says not to add such references to a primitive, so the owner must accept this known inherited hit, or fix line 220 in both commands as a separate change.

```markdown
## Fix Budget

Applies to every critique-mode run. The script is `fixcheck.py` in `~/.claude/skills/sc-fixcheck/scripts/` first, else the project `.claude/skills/sc-fixcheck/scripts/`, run as `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" <subcommand> ...` (`hash`, `snapshot`, `check`; `check --enforce` reverts). If `hash --file <spec>` cannot run, stop with `E-FIXCHECK-MISSING`, name both paths, and do not review.

Words are counted without `path:line` citations; bytes are counted on the raw added text. A finding id written into the spec, such as `(F3)`, is a new id. Budget per finding:

| class | applies to | gross | net | add-only | entries | heading | id | table row | MUST/SHALL/must/shall/never/always | only/every/exactly/none/total/closed | if/unless/when/whenever/where/except/otherwise | check recipe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRITICAL | CRITICAL blocking | 120 | 80 | 80 | 6 | 0 | 0 | 1 | 2 | 1 | 2 | 1 |
| blocking MAJOR | MAJOR blocking, FR-8, FR-9 | 80 | 50 | 50 | 4 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| minor | every non-blocking finding | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Whole cycle, overrides included: at most 600 gross added words and 6,144 gross added bytes, and the revised file at most 6,144 bytes larger than the baseline. `override` (at most one per report, blocking findings only, never an `origin=changed` finding, with an `override-reason: <id> <reason>` line) doubles gross, net, add-only and entries for that finding and never lifts a heading or id limit. `gap:<n>` (a blocking `MAJOR/FR-8` or `MAJOR/FR-9` gap fill, n = the guard-table rows it names) sets the condition-word limit to n. `override` and `gap:<n>` are exclusive.

Exit codes of `hash`, `snapshot` and `check`: 0 accept; 1 policy failure, every reason tied to a hunk (over budget, forbidden element, cycle cap, unattributed hunk including a quote not in the baseline, mislabelled op on an attributed hunk, edit on a minor id); 2 usage; 3 bad input (missing or empty file, no `fixbudget` block, malformed or second override, ledger missing, not found or ambiguous); 4 hash conflict; 5 cannot write a file safely; 70 internal error.

In every critique-mode review, run `hash --file <spec>` and add to the report a `fixbudget` block (`review: N of 3`, `reviewed_sha256: <hex from hash>`, `refs: <the citation prefix the report uses for spec lines>`, then `<id> | <severity> | <grade> | std|override|gap:<n>|-` per finding of this review and per prior blocking id still open or regressed, with its prior severity and grade; severity may read `MAJOR/FR-8` or `MAJOR/FR-9`). On a `--re-review`, after the checks of Review Loop bullets 1 and 4 and before the prior-blocking table, run `check` without `--enforce` and without `--ledger` (`--baseline <the saved copy passed as --baseline> --revised <spec> --report <prior report>`; the script uses the one file in the prior report's directory whose `fixledger` block starts `report: <prior report's file name>`) and put its summary in the header as `fixcheck: <exit> ...`; if an input is missing or malformed, or that run exits 3, 4, 5 or 70, or the disposition's last `FIXCHECK` line shows exit 3, 4, 5 or 70, stop with the named input error, never fall back to a first review, and escalate with the open blocking findings. Show each prior blocking id that run reports over budget as `open (over budget)`, each escalated or reverted id as `open (escalated: budget)` with its one-line need, each unanswered id as `open (unanswered)`, and `attacks: L<n>/<finding id>` on each `origin=changed` finding, taken from the run's hunk line whose revised range contains the line the finding quotes. Copy only numbers and ids from that run, never the reviser's reasons.

Reviser brief (place above the final `verdict:` line; fill `<...>`):
> Reviser brief, fix budget on. Fix only these blocking ids: <ids>. Every other finding is a minor note: change nothing for it and write `deferred (minor, fixcheck budget 0)` in its disposition row; a task brief that says to apply every finding is narrowed to this list (Review Loop bullet 7).
> 1. Baseline: before the first edit run `uv run --no-project python "<fixcheck base>/scripts/fixcheck.py" snapshot --spec <spec> --report <this report>`. The script writes only `<report dir>/.fixcheck/base-<N>.md` and exits 4 if the spec changed since this review. Do not use a `--baseline` copy named in a review brief: that is the text the previous review saw.
> 2. Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for. Answer each id by deleting the wrong sentence, else narrowing it, else replacing it; add text only after writing in the ledger why none of those fits. Per finding: CRITICAL 120 words added (net 80, add-only 80, at most 6 ledger entries), blocking MAJOR 80 (net 50, add-only 50, at most 4 ledger entries), no new heading, id or section, no finding id in the spec, at most one new table row, one new MUST/SHALL/must/never/always, one new only/every/exactly/none/total/closed, one new if/unless/when/whenever/where/except/otherwise (CRITICAL two, `gap:<n>` n) and one new check recipe.
> 3. Write, as a fenced `fixledger` block at the end of your disposition file (it is one of your output files; do not create others), first the line `report: <this report's file name>`, then per change one entry `## L1`, `## L2`, ... with `finding` (one id), `op` (delete|narrow|replace|add), the exact baseline sentence as `old` (for an add, as `anchor`), the first 10 new words as `new`, `considered` for an add, and `depends: L<n>` when the entry only works together with entry L<n>. A finding you cannot fix inside its budget goes under `## deferred` as `<id>: escalated: <what it needs>`. Do not expand it to fit.
> 4. Run `... check --baseline <baseline> --revised <spec> --report <this report> --ledger <your disposition file>`. Exit 0 is required. On exit 1: cut the named entries down or add the missing entry or `## deferred` line, once, and run `check` again; if the second run still exits 1, run `check --enforce` with the same arguments. On exit 2: correct the call once and re-run. On 3, 4, 5 or 70 at any run, or if `--enforce` exits non-zero: edit nothing further and paste the output.
> 5. In your report give the byte size before and after and paste the `result:`, `escalated:` and `FIXCHECK` lines of the first run when it was not exit 0, then those of the final run last, above the `fixledger` block.
```

### 3.3 Script outline (`fixcheck.py`)

Constants `BUDGETS` (keys C, M, m = the table), `CYCLE_GROSS_WORDS=600`, `CYCLE_GROSS_BYTES=6144`, `MAX_OVERRIDES=1`, `EXIT={OK:0, POLICY:1, USAGE:2, INPUT:3, HASH:4, WRITE:5, INTERNAL:70}`. Functions: `main` (argparse subcommands `hash`, `snapshot`, `check [--enforce]`); `read_text` (exit 3 if unreadable or empty); `parse_fixbudget` (block, overrides, `reviewed_sha256`, `refs`, GRADE-CONFLICT, Reviser-brief ids must be blocking ids, else exit 3); `parse_ledger` (the fenced `fixledger` block of the disposition file: `report:` line, `## L<n>` entries, `## deferred`); `find_ledger` (without `--ledger`: the one file in the report's directory whose block starts `report: <report file name>`, else exit 3); `units`, `words`, `diff_hunks` (moved units zero), `hunk_counts`, `attribute` (derive real op), `element_counts`, `score`, `cycle_checks`; `check` (prints the report, attribution reasons before size reasons); `--enforce` (whole-finding revert, `depends:` coupling, cycle-cap order, whole-file restore if the raw size check still fails, atomic temp-file-and-rename write, re-check; exit 3 without a ledger file or with an empty ledger); `score` marks `reverted` and `unanswered` entries as described in 2.2; `snapshot` (writes only `.fixcheck/base-<N>.md`, exit 4 on hash mismatch); `render_report` (summary, one line per hunk, one line per finding). Report example:

```text
FIXCHECK cycle=1 exit=1 base=sha:3f2a..c1 revised=sha:90be..77 ledger=sha:51d0..a8
hunks=41 attributed=39 unattributed=2 moved=2 net=340 cycle_words=512/600 cycle_bytes=3790/6144 raw_size=+3612/6144
h1  L1 F1 revised:63-63 +18/-11
h2  L2 F2 revised:80-93 +131/-43
h17 unattributed - revised:118-118 +22/-0
...
id   cls             op-mix  ent gross net ... budget status
F2   blocking MAJOR  replace 1   131   88  ... std    OVER gross 131>80, net 88>50
F14  minor           replace 1   56    56  ... -      MINOR-EDIT (minor budget 0)
unattributed: h17 +22 words "The coordinator ..."
escalated: F7 (needs about 140 words, budget 80)
result: OVER-BUDGET F2; MINOR-EDIT F14; UNATTRIBUTED h17
FIXCHECK exit=1
```

### 3.4 Tests

`tests/skills/test_sc_fixcheck.py` (loads the script with `importlib.util.spec_from_file_location`, `tmp_path` fixtures): clean in-budget fix exits 0; 81 added words on a MAJOR fix exits 1 (`gross`); net 51 at gross 60 exits 1; a one-word minor edit exits 1; a new heading, id, second table row, second MUST or second condition word each exit 1 with its own reason; an unattributed hunk, a quote not in the baseline and a mislabelled op each exit 1; a blocking id neither fixed nor deferred is reported `unanswered` and does not change the exit code; a raw size growth above 6,144 bytes from whitespace only exits 1; a second or reason-less override exits 3; without `--ledger`, the lookup finds the one disposition file whose block names the report, and none or two such files exit 3; the per-hunk lines exist, carry the right `L<n>` and line range, and are identical across two runs; edits to two neighbouring sentences by two entries are credited to both entries; a finding reverted for exceeding its entries limit scores 0 entries afterwards; moved text counts zero; a `path:line` token adds zero words and a `(F3)` tag fails with `id`; `--enforce` restores the over-budget and unattributed text, keeps in-budget fixes, reverts `depends:` partners whole, and a second `--enforce` changes nothing; `--enforce` without a ledger exits 3 and leaves the spec unchanged; `snapshot` on a changed spec and `check` on a mismatched baseline exit 4; the cycle cap reverts in the stated order; after `--enforce`, a plain `check` on the same four inputs exits 0 and scores the reverted entries `reverted`; a property test (random edits, random ledgers) always satisfies that rule.
`tests/skills/test_spec_panel_minfix.py`: name and Usage lines; faithful copy (outside the listed regions the file equals `spec-panel.md` line for line, so an unmirrored edit of the original fails); seven bullets, 1-5 and 7 equal to the original's, bullet 6 contains `Reviser brief`, `byte size before and after` and `## Fix Budget`; `## Fix Budget` between `## Review Loop` and `## Output Formats`; the budget table, cycle limits and exit line equal the script constants; the `~/.claude/` path precedes the `.claude/` path; `E-FIXCHECK-MISSING` present; no `src/superclaude` in the `## Fix Budget` section, the amended bullet 6 or the skill (the pre-existing line 220 is outside the change). These prove text exists and numbers agree, not that a model obeys.

### 3.5 Later adopters (not part of this change)

The script is keyed on (baseline, revised, findings block, ledger), not on spec-panel. The rf-qa Fix Cycle (`rf-qa.md:379-416`) is a good fit: it fixes prose documents in place, so it needs a findings block plus one `check` call after its fix step. `/sc:reflect` is a weak fit, because it has no reviser step of its own. The `/sc:implement` final review changes code, where words are the wrong unit, so it would need a code unitiser. Each adopter needs its own S1-style measurement first.

## 4. Variant command name and install note
**Name.** Command `spec-panel-minfix`, invoked as `/sc:spec-panel-minfix` (Skill target `sc:spec-panel-minfix`). Checker skill folder `sc-fixcheck`. Nothing about `spec-panel` changes. Workers load commands from `~/.claude/commands/sc/` (personal beats project, D9), so arms with different command text need different command names (`phase4/AB-REPORT.md`, "Machine facts").

**Experiment file.** Arms A and B ran the exact 427 text (472 lines, sha256 prefix c8d80346a96c, `git show 95f2c6e4:src/superclaude/commands/spec-panel.md`). To change one thing at a time, the experiment's `spec-panel-minfix.md` is the 3.2 change applied to that 472-line text (regions 1, 3 and 4; region 2 does not apply because that text has no unattended lines). The implementer builds it from `git show 95f2c6e4:src/superclaude/commands/spec-panel.md` into the experiment folder under `.dev/` (for example `.dev/experiments/346-minfix/build/spec-panel-minfix.md`), never under `src/`. The repository file applies the same hunks to the current 486-line `src/` file.

**Install for the experiment (owner or coordinator, never a worker; additive, no `--force`, no package reinstall):**

```bash
set -e
V=<variant checkout>
test ! -e ~/.claude/commands/sc/spec-panel-minfix.md && test ! -e ~/.claude/skills/sc-fixcheck || { echo "stale copy present: stop"; exit 1; }
cp -n "$V/.dev/experiments/346-minfix/build/spec-panel-minfix.md" ~/.claude/commands/sc/spec-panel-minfix.md
mkdir -p ~/.claude/skills && cp -rn "$V/src/superclaude/skills/sc-fixcheck" ~/.claude/skills/
cmp "$V/.dev/experiments/346-minfix/build/spec-panel-minfix.md" ~/.claude/commands/sc/spec-panel-minfix.md
cmp "$V/src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py" ~/.claude/skills/sc-fixcheck/scripts/fixcheck.py
sha256sum ~/.claude/commands/sc/spec-panel.md ~/.claude/commands/sc/spec-panel-minfix.md ~/.claude/skills/sc-fixcheck/SKILL.md ~/.claude/skills/sc-fixcheck/scripts/fixcheck.py
```

`cp -n` never overwrites, and `~/.claude/commands/sc/spec-panel.md` is only hashed, never written. The existing D10 install watcher logs only the spec-panel sha256 and the `WORKER-CONTRACT.md` state; it must be extended to the three new files, and a change of any of them during an arm voids V6 as before. After merge, `superclaude install` copies the new command and skill beside the originals in the same way (it skips existing command files unless `--force`).

**How the checker reaches a worker whose repo base (2cb683f5) has none of the new code.** It does not come from the repo. The command points at `~/.claude/skills/sc-fixcheck/scripts/fixcheck.py` in the home directory, outside every worktree. The script is stdlib only and runs as `uv run --no-project python "<path>"`, with no `pyproject.toml`, virtual environment or `superclaude` import. A missing home copy stops the run with `E-FIXCHECK-MISSING`, never a silent plain-427 review. Before measured runs, a fresh worker loads `/sc:spec-panel-minfix` through the Skill tool and runs the installed checker on one valid and one invalid fixture (exit 0, exit 1). The same probe checks that the worker's permission mode runs `uv run --no-project python ~/.claude/skills/...` without a prompt (UNVERIFIED today).

**The one-line substitution an experiment brief needs.** Arm C briefs = Arm B's briefs (D11, which already append `--re-review <prior report> --baseline <saved copy>` to the R2 and R3 review briefs), with this one substitution applied to the review briefs T05, T07 and T09:

```text
s#/sc:spec-panel @#/sc:spec-panel-minfix @#
```

Verified on the S1 brief texts in `phase2/S1/briefs/task-text/` and on the templates Arm B actually used (`phase2/S1/briefs/templates/T07-R2-reviewer.TEMPLATE.txt`, `T09-R3-reviewer.TEMPLATE.txt`; `T08-R2-reviser.TEMPLATE.txt` has none): each of T05, T07 and T09 contains the command exactly once, in the form `/sc:spec-panel @.dev/...`, and the substitution leaves the report file names (`review/spec-panel*.md`) unchanged. The reviser briefs T06 and T08 stay verbatim (the reviser learns the budget from the report). No brief mentions the checker, ledger or budget. Record the substitution in the coordinator log.

## 5. Measurement plan and predicted numbers
**Design (Arm C, same shape as D10/D11).** Scenario S1 (Orca worker-contract spec, 57,763 bytes, 8,148 words), base commit 2cb683f5, same overlay, same verbatim briefs plus the substitution of section 4, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, 3 reviews and 2 fix cycles, two fresh worktrees (for example `exp346-ab-min-r1`, `-r2`). First, one pilot replicate runs BOTH fix cycles and checks that the reviser runs `snapshot` and `check` under the S1 ownership clauses (T06 "write ONLY your output file(s)"; T08, stricter, "edit ONLY the spec and write ONLY disposition-round2.md"). A failed pilot changes the Reviser brief wording, not the design. If wording cannot fix it, the fallback is to name the cycle's own saved copy as the baseline in T06 (`spec-v1-draft.md`) and T08 (`spec-v2-after-round1.md`), declared as a second brief change. The pilot is not one of the two measured replicates. Comparators: ctl-r1 and ctl-r2 (reused, as in D11), then arm A and Arm B as secondary. A new concurrent control would need its own command name holding the pre-427 text, because the owner's `spec-panel.md` is the 486-line master text.

**Bar (unchanged from D11).** (a) review-3 critical+major proxy mean at most 3 and every replicate better than every control replicate (with controls 8 and 4, each replicate at most 3), or a clean pass sooner; (b) growth after two fix cycles at most 44.4%, every replicate below both controls; (c) effect larger than the larger within-arm spread. Validity V1-V6 as before, plus V7: each cycle's disposition ends with `FIXCHECK exit=0` (or lists what `--enforce` reverted) and the next review's own `check` does not exit 3, 4, 5 or 70. A replicate failing V7 is "mechanism not honoured" and is not treatment.

**Extra metrics only this arm produces** (from the pasted check lines and the re-review runs): escalated ids, overrides, unattributed hunks before `--enforce`, reverted findings, cut-down success rate (over budget at the first check, within at the second), reviser tool calls and minutes, `attacks:` chains (children per ledger entry by op, size, class and parent grade; parent-to-child severity for drift), and review 3 reported as proxy and blocking count, with blocking split into carried (open from review 2: unfixed, escalated, reverted) and new (on cycle-2 hunks), before the bar is applied.

**Predicted growth after two fix cycles: about 13% in bytes (range 8% to 21.3%), against control 63.5% and bar 44.4%.** The growth metric is D5's M4 byte growth (the recorders' `growth_percent_cumulative_vs_v1`, from which the 63.5% and 44.4% figures come). Supporting word replay on flg-r2 (the only loop with every change tagged): capping blocking fixes at 80/120 words and refusing the 773 minor-fix words cuts 1,260 of 2,721 tagged words, which gives net 14.4% in words instead of the actual 33.1% in words (32.1% in bytes); the same ratio on the four 427 loops gives 13.4%. Words and bytes moved together in that loop, so about 13% in bytes is expected. The hard ceiling, if the script runs, is 21.3% in bytes (two cycles of at most 6,144 bytes of raw size growth), and 14.7% in the checker's own word count (citations, pipes and heading marks excluded, so the recorders' `wc -w` growth may be higher). This bar is met by a wide margin as long as V7 holds.

**Predicted review-3 open critical+major proxy: about 3.3 (per-replicate band about 1 to 6), against control 6.0 and bar 3.** In plain terms: expected to land at the bar, not safely below it; roughly even odds for the mean and lower odds for the every-replicate rule. Derivation: review-1 proxy about 12; 427's critical+major transition ratio per cycle 0.66 (the plain mean of eight per-cycle ratios). Of the 13 traced fix-induced items (shapes A to E of section 1), the assumed removal probabilities (A 0.9, D 0.6, B 0.5, C 0.3, E 0) give (3x0.9 + 3x0.6 + 2x0.5 + 3x0.3) / 13 = 0.49 expected removal. If 25%, 50% or 75% of removed items reappear as another child of the leaner fix, the ratio becomes 0.42, 0.50 or 0.58 and review 3 about 12 x r squared = 2.1, 3.0 or 4.0 (derived central 3.0). The stated 3.3 is a judgment adjustment upward: the derivation counts only fix-induced items, and ignores blocking findings the budget leaves open (escalated, reverted, unanswered) and carries into review 3. Partly offsetting this, the derivation's zero-removal baseline (12 x 0.66 squared = 5.2) is above the 427 loops' actual review-3 mean (4.5). The band of about 1 to 6 per replicate is judgment from n = 2 spreads (Arm B's replicates were 6 and 1). The two assumed inputs (removal and replacement) decide the outcome, and the arm measures both through `attacks:`. Other predictions: 1 to 3 blocking ids escalated for budget at review 2 (conditional on the unmeasured cut-down rate); share of new findings that are `origin=changed` still 85-100% (not a success measure); a clean pass in at most one of two replicates.

**What result means the idea failed (fixed before any run, valid replicates only).**
1. Minimality is not enough: the script ends exit 0 in both cycles of both replicates and review 3 is above 3 in either. Then drop minfix as a standalone fix and test it only combined with a verdict-side change.
2. The budget converts fix-induced findings into unfixed ones: carried open blocking findings at review 3 are 3 or more in either replicate.
3. Surface is not the driver: 14 or fewer cycle-2 hunks, yet 3 or more new critical+major findings on them at review 3 in either replicate.
4. Only growth improves: growth is met but the review-3 proxy is not better than Arm B's mean 3.5. 427 already meets the growth bar, so the extra cost buys nothing; reject it.
Not a test of the idea (re-run instead): any V1-V7 failure, any check exit 3, 4, 5 or 70, or byte growth above 21.3% (raw `wc -c`, which the raw size check bounds) while the script reports exit 0 in both cycles (a checker bug).

## 6. Risks, costs and what would falsify it
**Cost per loop (3 reviews, 2 fix cycles; tool-call counts of the S1 sessions were not measured, so these are estimates).**

| item | estimate |
|---|---|
| extra tool calls | reviser 3 to 11 per cycle (`snapshot` 1, ledger 1, `check` 1-2, cut-down edits 0-6, `--enforce` 0-1); reviewer 1-2 per review; about 9 to 28 per loop |
| extra sessions | 0 (the cut-down happens inside the reviser session) |
| extra wall time | about 8 to 18 minutes on a loop of about 78 minutes (control 05:05 to 06:23Z), so 10% to 23%; each script call is expected under a second (UNVERIFIED) |
| one-time | the pilot replicate; implementing a 350-line script and two test files |

**Ways it can make the loop worse** (likelihood and impact are judgement, UNVERIFIED):

| risk | evidence | mitigation and residual |
|---|---|---|
| under-fixing: blocking findings stay open (high/high) | in flg-r2, 11 of 17 MAJOR fixes exceeded 80 words; `--enforce` reverts a failing finding whole | 80 words is about twice the longest reviewer recommendation in flg-r2 round 2 (39 words); one override per report. Residual: a fix that needs a real mechanism goes to the user at review 3, and it counts in the very metric the bar uses (falsifier 2) |
| escalation replaces fixing (medium/high) | escalating is cheaper for the reviser than fixing | the escalation must state its need in words; the re-review lists it `open`. No cap on the escalated share in v1 |
| false positives on legitimate edits (high/medium) | `when` and `where` are common prose words; renumbering AC-1.4 to AC-1.5 looks like a new id; a column change touches every row; curly quotes break a ledger match | normalisation, 40-character unique-substring quote match, ids counted only if absent from the baseline. Renumbering must be escalated in v1; the replay harness measures the false-positive rate first |
| consistency residue: a rule fixed in one place but not propagated (medium/medium) | ctl-r1 R2 "Residue of round-1 finding 5"; flg-r2 fixes touched 3 to 5 sites each | 4 entries per MAJOR, `depends:` coupled revert, one override. Undeclared dependencies remain |
| reviser skips the script, or reads its ownership clause as forbidding `snapshot` (medium/high) | `snapshot` is needed in both cycles (no reviser brief names a baseline; T07's `--baseline` is the previous cycle's copy); T06 says "write ONLY your output file(s)" and T08 "edit ONLY the spec and write ONLY disposition-round2.md"; flg-r1: "The Task 6 brief wins" | the re-review's own `check` is authoritative and stops the loop on bad input; the two-cycle pilot tests this, with the T08 baseline line as fallback. Residual: a wasted replicate |
| the S1 review briefs keep "any finding of any severity is FAIL" (medium/medium) | T07 and T09 templates; this contradicts 427 bullet 7 and is the same in Arm B | not a minfix defect, but it can block the predicted clean pass; 427 bullet 7 should prevail, and the arm reports both the proxy and the blocking count |
| gaming by rewording (medium/medium) | synonyms ("solely", "each") evade the universal-word list; one addition can be split across two findings | per-finding gross cap, entries cap, minor budget 0; lexical gates are tripwires, not proofs |
| real minor errors stay in the spec (high/low) | flg-r1 R2-5 (`--output` should be `--output-dir`) is a real one-token error graded minor | none, by design: 427's own rule "minor findings never trigger a revision", now enforced |
| the reviewer attacks changed text harder because of `attacks:` (low/medium) | the tag points at ledger entries | the tag is written after the finding, from the script's hunks; the reviewer never sees ledger prose |
| forged `FIXCHECK` lines (low/low) | a model can type text | the re-review recomputes everything; not a security boundary |

**What stays prose (residual risk):** the delete-first order beyond the tiered caps, the truth of `considered:`, the reviser actually running the commands, the reviewer copying only numbers, and "no override on an `origin=changed` finding". Tests of the command text prove the text exists, not that a model obeys it.

**Falsification:** the four results in section 5, fixed before any run. The most likely failure mode, given the measured data, is falsifier 1 or 4: growth collapses (already true of 427) while review 3 stays at 4 to 6, because small fixes still produce blocking children (flg-r2: F12, a 58-word fix with one universal "only", produced N4).

## 7. Open questions
1. **Budget values.** 80/50 and 120/80 come from one fully tagged loop (flg-r2). A budget relative to the reviewer's recommendation (for example the larger of 40 and three times its words) may track the ask better, but needs that size in the `fixbudget` block. First implementation task: a replay harness runs the finished script over the six recorded loops (baseline = previous history copy, ledger synthesised from each disposition). It checks the per-finding counts within 10% of section 2.3's calibration and measures the false-positive rate of `when`/`where` and the over-cap count per loop.
2. **Is one override per report enough?** Propagation fixes (ctl-r1 residue findings) want more; flg-r2 N3/N6 show propagation causing findings. Unresolved by data.
3. **Early computed escalation.** Should the script print `ESCALATE-NOW` when escalated ids exceed, say, 40% of blocking ids after cycle 1? That would shorten hopeless loops but change 427's cap semantics. Not in v1.
4. **Renumbering and the id gate.** A `renumber: yes` ledger field could exempt ids shifted within an existing prefix, but it is a loophole that needs its own test. Not in v1.
5. **Should `named` (the entry's old text is quoted by the finding) become a hard gate?** Kept informational because legitimate propagation edits unnamed text.
6. **FR-8/FR-9 graded minor.** A GAP graded minor under 427's concrete-outcome test gets budget 0 and is not fixed (`GRADE-CONFLICT`, listed at the review-3 escalation). Is that what the owner wants from "hard gates"? Should the bar count the blocking grade rather than severity (section 5 reports both)?
7. **Moved text** counts zero, yet it is changed text the next review may attack. Should a move be charged?
8. **Reviewer-side companion (outside this theme).** In flg-r1 R2-1 and R2-3 the reviewer offered the deletion second. "List the deleting or narrowing option first, with a word count" costs one line and targets shape D; flagged for the cross-team merge.
9. **Saved-copy path.** `snapshot` is the normal baseline path in both cycles. Should the coordinator instead name the cycle's own saved copy (v1 for cycle 1, v2 for cycle 2) in the reviser briefs T06 and T08? That costs a second brief change. The two-cycle pilot decides.
10. **Per-hunk lines for edge hunks.** A pure-deletion hunk has no revised line range. Two findings' edits in adjacent units can merge into one diff opcode. Proposed v1 rule: print a deletion hunk with the revised line it sits before; merged opcodes are split per entry (section 2.2). Confirm both in the replay harness.
11. **Folding back.** If Arm C passes, merging bullet 6 and `## Fix Budget` into `spec-panel.md` is a separate change that must update the 427 pin test and the plugin mirror; the other adopters (section 3.5) each need their own measurement.

Brainstorm artifacts (all kept): `seed-brief.md`, `enrichment/codebase-context.md`, `merged-requirements.md` (the full merged design this spec condenses), `nested/adversarial-1/` (three variants, diff analysis, two debate rounds, invariant probe, forced surface round, scoring, base selection, refactor plan and its review, merge log), `return-contract.yaml`. Differences from `merged-requirements.md`, each fixing a defect found while condensing it or by the independent review `spec-review.md`:
- every review runs `hash`;
- the re-review's `check` runs after 427's input and cap checks;
- the reviser always uses `snapshot`, because a re-review's `--baseline` is the previous cycle's copy;
- the ledger names its report and the re-review finds it without a new flag;
- `reverted` and `unanswered` statuses, so a plain `check` after `--enforce` exits 0;
- one line per hunk, so `attacks:` can be computed;
- a raw file-size check, so the byte ceiling is strict;
- growth predicted in bytes;
- the review-3 derivation shown with its judgment adjustment;
- the pre-existing template-path line left unchanged.
