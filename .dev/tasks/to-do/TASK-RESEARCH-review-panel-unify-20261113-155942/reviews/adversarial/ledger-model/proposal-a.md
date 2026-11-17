# Proposal A: Re-find and cluster every round (the master ledger, with D2, D3 and D16 fixed) for C13

**Side and option.** Side A argues for Option A of conflict C13 (slug `ledger-model`, `synthesis/synth-04-options-conflicts.md` section C-13): keep `merge_round` as the round engine, so every review round parses, annotates, clusters and row-matches the reviewers' reports again, and fix the three defects that make that engine unsafe: D2 (clearing ignores `block_ok`), D3 (a round passes on one valid reviewer) and D16 (round 4 accepted, `--cap` ignored on an existing ledger).

**One-paragraph case.** The round engine already exists in `src/`, is pinned by 24 ledger tests, and its measured behaviour (E2 audit D, round 1) is deterministic and faithful. Its three defects are small, local and fixable in `ledger.py` and `merge_cmd.py` without a new protocol that models must comply with. The alternative that Options B and C add, a find-once then verify-only code mode, rests on a plan-answer protocol that no effort has run in a multi-reviewer panel, that is XL to build, and that conflicts with two already-decided conflicts (C02 and C15). Verify-only stays what it is today, a reviewer-brief convention, and Option A leaves the door to C open because A is C's first half.

**Citation key.** `NN §x` is a section of `research/NN-*.md`; `web-NN` is `research/web-NN-*.md`; `C-nn` and `Dnn` are the conflict and defect rows of `synthesis/synth-04-options-conflicts.md`; `G-nn`/`D-nn` are rows of `gaps-and-questions.md`. Evidence tags: `[CODE-VERIFIED]` means re-read in this pass on branch `ironbelly/shadow-runs` (HEAD `792cf8c52`); `[DOC-SOURCED]` comes from a report, not re-derived; `[INFERENCE]` is this proposal's reasoning from cited facts; `[external]` carries its URL. E2 means the other session's tasklist review-panel study, read only at commit `4a22d74213f93837d00c2c314075dd967b9a98e3` (`E2:` prefix = `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>`).


## Design

### The rule in one sentence

The ledger stays a deterministic, script-kept record of rows and rounds. Reviewers (one panel at review 1, by default one anchor reviewer at reviews 2 and 3) report what they find in the current candidate; the script clusters, matches against existing rows, applies one decider for blocking, and the verdict is computed only from a round that was a real review. Fixing D2, D3 and D16 means the script refuses to treat an invalid, thin or out-of-cap round as evidence.

### Core changes (all inside the round engine)

All five changes live in `src/superclaude/cli/review/ledger.py` (`merge_round`) and `merge_cmd.py`. None of them needs a new subcommand, a new exit code, or a new reviewer protocol.

1. **Cap by refusal (D16a).** `merge_round` raises `LedgerError` when `n > ledger["cap_reviews"]`, before anything is recorded. Today only `n == len(rounds) + 1` is checked (`ledger.py:114-118`) and the cap is only a label in `_decision` (`ledger.py:93-96`). Round 3 of 3 still merges and still returns FAIL/ESCALATE (exit 11 from `ledger verdict`), so the existing escalation path and `test_escalate_still_prints_verdict_fail` are unchanged.
2. **`--cap` on an existing ledger is an error when it differs (D16b).** `merge_cmd.py` changes `--cap` from `default=3` to `default=None`. Round 1 creates the ledger with `cap or 3`; a later round that passes a `--cap` different from the stored `cap_reviews` is a `ClickException`; a later round that omits `--cap`, or passes the same value, is unchanged. The `--round` help text ("1, 2 or 3") becomes "1 up to the ledger's cap" (`merge_cmd.py:40-41`).
3. **Quorum of valid blocks (D3).** `merge_round` computes `panel_size` (the larger of the number of `--report` options and the number of reviewers in `--resolution` when given; a resolved reviewer with no report is an abstention) and `quorum = min(2, panel_size)`. `valid` is the set of reviewers whose block was complete (`block_ok`). `degraded = len(valid) < quorum`. A single-reviewer round (every re-review by default, and `review merge` "also for a single reviewer" per `document_review_loop_prompts.md:70`) has quorum 1, which is today's behaviour exactly.
4. **Clearing only from a real review (D2).** The clearing loop (`ledger.py:254-258`) runs only when the round is not degraded. A `resolved_check` row that a degraded round does not clear stays `resolved_check`, and the round result lists it under `not_cleared` with the reason. This makes the docstring at `ledger.py:112` true (an invalid reviewer is skipped for clearing) instead of contradicted. Prior lines keep their present role: notes that never change a status (`ledger.py:259-272`, pinned by `test_prior_lines_never_change_a_status`).
5. **A degraded round can fail but cannot pass.** If `degraded` and the computed verdict would be PASS, the merge is refused and nothing is recorded (same mechanism and message family as the zero-valid-block refusal at `ledger.py:150-157`), so only the missing reviewer is re-run. If `degraded` and the verdict is FAIL, the round is recorded with `degraded: true` and the merged report says so. A round also cannot PASS while a rejected line carried `blocking: true` (this needs C15's `rejected[]` record; see seams).

One bookkeeping addition that gates nothing: when a reviewer's valid block lacks a `prior` line for a prior blocking row, the round result and round entry list it under `unanswered_priors`. It is recorded as telemetry, because gating on it would make Option A depend on reviewers complying with a protocol nobody has measured (see Risks).

### Seams to the other conflicts (what A needs, what A does not decide)

The ledger calls four functions that C01, C02, C12 and C15 replace: parse (`fnd.parse_block`, `ledger.py:128`), annotate (`fnd.annotate`, `:136`), cluster (`fnd.cluster`, `:165`) and row match (`fnd.same_defect`, `:169`). C13 Option A does not choose their implementation; it needs the following contract from them and nothing more.

| Seam | What the round engine reads | Owning conflict |
|---|---|---|
| Parse | per reviewer: `ok` (complete), `partial`, annotated findings kept from a bad block, `priors`, `rejected[] = {line, id, reason, blocking}` | C01, C02, C15 (decided) |
| Cluster and match | groups of members with `blocking_any`, `support`, `disputed`, `chained`; row views that can hold citations; `same_defect_v2`-style match | C12 (decided) |
| Decider | one function replaces `any(m["blocking"])` at `ledger.py:187` and `:213-218` | C05 (undecided), C16 (decided: reviewer flag kept as input, effective blocking recorded) |
| Verdict mapping | the core returns PASS/FAIL with decision PASS/REVISE/ESCALATE; modules map to advisory or blocking | C19 (decided) |

Until C05 is decided the decider is the existing `any(...)`. Because Option A keeps blocking in one place, whichever C05 option wins (quorum, calibrated support, blind grader) lands there without touching the round model. The multi-file persistence the research found missing (rows keyed by a citation set, a per-path diff map in `apply_revision`, 02 §5.3 items 3-4) is needed by every C13 option, so it is attributed to C01/C12 and not charged to A alone [INFERENCE; see Cost].

### Consumer modules

| Consumer | What it does under Option A |
|---|---|
| Spec review loop (`/sc:spec-panel --mode critique`, the only caller of `review merge` and `ledger revise` today, 09 §7) | Same flow. The rules prompt keeps the RE-REVIEW prompt (evidence block, one `prior` line per prior blocking finding). One sentence in `document_review_loop_prompts.md:70` is extended: a merge refuses a round with fewer valid blocks than the quorum that would pass, and a round above the cap. The "no fourth review" rule at `document_review_loop_prompts.md:13` becomes enforced by code, not only by prose. |
| Tasklist review module (workflow Wave 4, tasklist Stage 10.5, post gate) | A thin module over the shared brief and dispatch reference (D14, C09, C10). If the module wants a loop it calls the same CLI with its own `--cap`. Advisory or blocking is the module's mapping of the core verdict (C19). |
| Reflect module (pre and post) | Unchanged by C13. Reflect is single-pass, keeps the debate and contract 1.8.0 (C11), and does not call `merge_round`. This matches the E1 position that reflect has no ledger (C-13 table, E1 row). If a later reflect tier adds a re-review loop it calls the same engine. |
| PR review (`pr_submit`) | Its reviewers are external bots that are re-triggered after each push (`retrigger_phrase`, `reviewer_activity` adapters, 10 §1.2 seam A), so every round is a re-find by construction. A maps PR dedup groups to ledger rows by the unified location key and reuses cross-round row matching as the "dedupe against earlier runs" step. |
| rf-qa replacement | rf-qa's fix cycle is already a verify-with-new-issues pass written in its prompt (`src/superclaude/agents/rf-qa.md:381-398`). Under A the module keeps that prompt and records rows in the ledger. Adopting rf-qa's monotonicity and regression halts is C19 Option B and stays out of C13. |

### What Option A explicitly does not do

- It does not add a verify-only code mode. D16c is closed as "by design": the re-review prompt is the verify protocol, and the ledger is its bookkeeping.
- It does not add positive (evidenced) clearing. Clearing stays "a valid, quorate round did not re-find the row", plus two independent prior conditions described under Evidence.
- It does not choose the blocking decider (C05), the rf-qa halts (C19 B), or a `PENDING` verdict.

## How it works

### Data flow of one loop (default templates)

1. `superclaude review panel resolve --run-id <loop> --kind first` resolves the review-1 panel. All 8 packaged templates carry `apply_to: ["first"]`, so `--kind re-review` resolves only the fixed anchor reviewer, count forced to 1 (`panel.py:600-605,616`; `src/superclaude/cli/review/data/review-panel.*.json:7`; 04 §3 and line 255) [CODE-VERIFIED].
2. The module dispatches the reviewers with one brief (first-review prompt at review 1; the RE-REVIEW prompt at reviews 2 and 3, `document_review_loop_prompts.md:27-49`). Each reviewer ends its report with a findings block (`## Findings block`, one JSON object per line).
3. `superclaude review merge --ledger L.json --doc <candidate> --round n --report rid=path ... [--resolution res.json] --out merged-n.md [--cap k]` runs the round engine:
   - parse each report, keep the valid lines of a bad block, mark the reviewer partial, store `rejected[]` (C15, C02);
   - annotate against the candidate, cluster all members (C12), match each cluster to an existing row;
   - decide blocking per cluster (C05 hook; `any(...)` today);
   - apply cap, quorum and degraded rules (changes 1-5 above);
   - clear `resolved_check` rows only in a non-degraded round; mark `regressed` any `resolved_check`/`resolved` row that is re-found (`ledger.py:235-238`, unchanged);
   - compute verdict (`FAIL` iff an open or regressed blocking row exists, `ledger.py:273-274`) and decision (`PASS`, `REVISE`, `ESCALATE` at the cap, `ledger.py:93-96`).
4. `merge` writes the merged report and saves the ledger atomically (`ledger.py:52-67`). A refusal writes neither.
5. On FAIL with decision REVISE, a reviser repairs only the Reviser-brief ids and writes a fix map; `superclaude review ledger revise --old --new --fixmap` moves a row to `resolved_check` only when the fix map says `applied` and a diff hunk touches the row's span (`ledger.py:328-339`), and it refuses an `--old` that is not the text the last round reviewed (`ledger.py:308-314`).
6. The next round returns to step 1 with `--kind re-review`. On ESCALATE the merged report carries `## Escalation` and no Reviser brief (`ledger.py:475-486`); `ledger verdict` exits 11.

### Contract fields (additive; schema string `review-ledger/1` unchanged)

`load` checks only the `schema` value (`ledger.py:41-49`), so new keys that readers default are backward compatible and old ledgers keep loading [CODE-VERIFIED].

| Where | New field | Meaning |
|---|---|---|
| round entry (`rounds[]`) | `panel_size`, `quorum`, `valid` (reviewer ids), `degraded` (bool) | what the engine counted for this round |
| round entry, per reviewer (`reviewers[]`) | `partial` (bool), `rejected` (`[{line, id, reason, blocking}]`) | C15/C02 record; today only `block_ok` is stored (`ledger.py:141-149`) |
| round entry | `unanswered_priors` (`[lid]`) | prior blocking rows a valid reviewer gave no `prior` line for; telemetry only |
| merge result | `degraded`, `quorum`, `not_cleared` (`[{lid, reason}]`), `unanswered_priors` | printed by `review merge` as JSON beside the existing keys |
| merged report | one header line `degraded: yes (<valid> of <quorum> valid blocks)` when degraded | the next reviewer and the reviser can see it |

Unchanged: row fields, statuses (`ledger.py:19`), `defer`, `capture`, `review-capture/1`, `fixmap-v1`, `prior` lines.

### CLI surface

| Command | Change |
|---|---|
| `review merge` | `--cap` default `None` (round 1 creates with 3 when omitted); error on a conflicting `--cap` for an existing ledger; `--round` help text corrected; refusals (round above cap, degraded would-be PASS, no valid block) are `ClickException`, exit 1, nothing written |
| `review ledger revise / defer / verdict / capture` | none; `verdict` still exits 0/10/11 (`ledger_cmd.py:13`) |
| `review panel resolve` | none; `--kind first\|re-review` stays; a verify-only kind would be a later additive value (04 line 266 already proposes keeping `kind` as the round axis) |

### A three-round example under the default templates

Review 1: panel of 3 resolves, quorum 2. Reviewers A and B return complete blocks, C returns a truncated block. `valid = {A, B}`, not degraded, C's parsable lines still join clusters and C abstains from the quorum. Review 1 FAILs, decision REVISE. Review 2: the anchor reviewer alone, quorum 1; it re-checks each prior blocking row, emits `prior` lines, and may report new findings. A row the reviser fixed and that the anchor reviewer does not re-report clears to `resolved`; a row it re-reports becomes `regressed` or stays `open`. Review 3: same; any open blocking row gives FAIL with decision ESCALATE, and a fourth `merge` is refused.

## Evidence

Each item gives the claim, its source in the research files, and the code or document location. Items marked `[CODE-VERIFIED]` were re-read in this pass.

### 1. The engine exists, is small to fix, and its defects are exactly the three A fixes

- **D2 clearing ignores `block_ok`.** The clearing loop tests only `row["status"] == "resolved_check" and row["lid"] not in members_by_lid` (`src/superclaude/cli/review/ledger.py:254-258`); `block_ok` is built at `:123,:129` and never read after `:150`. The docstring at `:112` says the opposite. Source: 02 §1.4 D2 row; synthesis D2 row. [CODE-VERIFIED]
- **D3 a round passes on one valid reviewer.** The only validity refusal is `not any(block_ok.values())` (`ledger.py:150-157`); PASS is computed at `:273-274` from open or regressed blocking rows only. Source: 02 §1.4 D3 row. [CODE-VERIFIED]
- **D16a, D16b.** `merge_round` checks only `n == len(rounds)+1` (`ledger.py:114-118`); `_decision` labels ESCALATE at `n >= cap_reviews` (`:93-96`) but the merge still appends the round; `--cap` reaches the ledger only through `new_ledger` on round 1 (`merge_cmd.py:101-104`); `--round` help says "1, 2 or 3" while the type is `IntRange(min=1)` (`merge_cmd.py:40-41`). Source: 02 §1.4 D16 rows, §2.1. [CODE-VERIFIED]
- **The tests pin the defects, and the fixes are local.** `tests/review/test_review_ledger.py:376-385` pins D3 and D2 together (final assertion `:385`, `status(led)["L1"] == "resolved"`); no test covers round 4 or `--cap` on an existing ledger (12 §3.1, §4 D16 row; `grep -n cap` over the ledger and CLI tests finds only `test_review_ledger.py:136`). The fix therefore rewrites one test and adds new ones; it does not unwind a suite. [CODE-VERIFIED for `:376-385`; the grep is in 12 §4]
- **The call seams the fixes need already exist.** `block_ok` per reviewer is built at `ledger.py:129`; `merge_cmd` already reads the resolution file per reviewer (`merge_cmd.py:74-83`); `_decision` already has the cap (`ledger.py:93-96`). Quorum, cap refusal and the clearing gate are conditions added to code that already computes their inputs. [CODE-VERIFIED] [INFERENCE on size]

### 2. Rounds 2 and 3 are already one reviewer by default, so "re-find" is cheap and low-risk

- Every packaged template has `apply_to: ["first"]` (`src/superclaude/cli/review/data/review-panel.{default,live7,reflect-lite,reflect-pre,reflect-pre-x2,reflect-post,reflect-post-x2,reflect-enterprise}.json:7`), and `resolve` expands slots only when `review_kind in panel["apply_to"]`, otherwise only fixed slots with count 1 (`panel.py:600-605,616`). So `--kind re-review` always yields the single anchor. Source: 04 lines 56, 101, 255. [CODE-VERIFIED]
- The CLI round-trip test already runs review 2 with one `--report` and no `--resolution` (`tests/review/test_review_cli.py:277-292`), which is quorum 1 under A, so the CLI contract of the default loop is untouched. [CODE-VERIFIED]
- Consequence [INFERENCE]: the clustering weakness that the E2 study measured (C12) bites at review 1 with a panel. At reviews 2 and 3 there is one reviewer, so the cluster step is the reviewer's own findings plus row matching. The cost that Option B saves by not re-clustering is small in the default configuration.

### 3. Verify-only already exists as a reviewer protocol; A keeps it and does not duplicate it in code

- The RE-REVIEW prompt makes the reviewer produce a diff evidence block (`diff -w BASELINE CANDIDATE`), re-check each prior blocking finding as resolved, open or regressed against the AFTER text only, run a `grep -nF` self-check, and end with one `prior` line per prior blocking finding (`src/superclaude/rules/prompts/document_review_loop_prompts.md:44-49,61`). [CODE-VERIFIED]
- rf-qa's fix cycle is the same shape in its own prompt: re-verify each blocking issue from the previous report, flag new issues the fix introduced, do not recheck minor findings (`src/superclaude/agents/rf-qa.md:381-398`), and the Rigorflow pattern "lens agents, consolidate, one fix agent, verification round" is the review loop's shape (10 §3). [CODE-VERIFIED]
- `prior` lines are already parsed and carried (`findings.py:175-187`; `ledger.py:139-140,259-272`) and are an invariant by design: a reviewer's lines are notes and never change a status (`ledger.py:3-4` docstring; `test_prior_lines_never_change_a_status`, `tests/review/test_review_ledger.py:318-338`). B's clearing makes a reviewer's answer change status; A keeps the stronger invariant "only the script changes a status, from mechanical evidence".

### 4. What guards clearing in A (more than silence)

A row reaches `resolved` only through all of these, each a separate mechanical or recorded signal [CODE-VERIFIED]:
1. the reviser's fix map says `applied` for that row;
2. a diff hunk touches the row's span (`ledger.py:328-339`), computed from the actual old and new text, with `--old` refused unless its sha256 equals the last reviewed round's `doc_sha256` (`ledger.py:308-314`);
3. a later round that is not degraded (new, change 4) with no valid or partial reviewer re-reporting the row (`members_by_lid`, `ledger.py:239,254-258`; a partial reviewer's parsable lines still join clusters, so it can prevent clearing but not cause it, 02 §1.4 last bullets);
4. any later re-find sets the row to `regressed` and it blocks again (`ledger.py:235-238`; `test_refound_resolved_row_becomes_regressed_and_fails`, `test_review_ledger.py:220-252`).

### 5. E2 evidence: the merge engine is faithful at round 1, and its per-round record is what made the audit possible

All E2 statements below are read at `4a22d74213f93837d00c2c314075dd967b9a98e3`, `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/`. Raw `score.json` and `cost.json` files were not re-aggregated (gaps log G-82). [DOC-SOURCED, outputs re-read]
- `summary.md:3`: 89 rows x 3 packages = 264 merged first reviews, "all use ledger round 1 only". So E2 has no evidence about rounds 2 and 3, D2 or D16 (`summary.md:34`, X6; 02 §4.4).
- `summary.md:33` (X5): row blocking equals any member blocking and verdict FAIL iff a blocking row, "0 violations over 264 merges" apart from the dropped-finding effect. The engine implements its rules faithfully; the defects are in the rules. Under A the rules are corrected where C13 owns them (D2, D3, D16) and elsewhere by C02, C05, C12, C15.
- `summary.md:10` (C5): `report_sha256` in the ledger let the audit detect 16 stale merges (reports re-run after the merge). That field is written by the per-round entry that A keeps and extends (`ledger.py:141-149`).
- **A's D3 rule would have blocked the three measured verdict flips.** `summary.md:20` names three merges whose verdict was PASS where the reviewer said FAIL, because a dropped blocking line left no blocking row. The audit's own flip test is "dropped blocking lines exist and no row blocks" (`audit2.py:126-136`, read at the same commit). Change 5 withholds PASS exactly under that condition. Count check: `flags.tsv` has 49 `3-dropped-blocking` lines (re-run in this pass), 48 of them length rejections (02 §4.2). The replay was not re-run; this is [INFERENCE] from the audit's criterion. The length loss itself is removed upstream by C02 (decided); change 5 is the belt for the structural rejections that remain.

### 6. B and C: what the verify-only design is, what it costs, and where it collides with decided conflicts

Facts about the installed experiment ledger `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` (2,668 lines, not in `src/`; 02 §6). Lines spot-checked in this pass. [CODE-VERIFIED]
- **One input per find.** `cmd_find` runs only in phase `find` and refuses a second find for review 1 (`:912-924`, `E-PHASE`); rows come from one report's `ledger-input` block; the script has no clustering and no multi-reviewer merge (02 §6.1). A panel at review 1 therefore needs a merge layer that does not exist in either stack.
- **All-or-nothing input.** Any bad row refuses the whole input, "nothing was written" (`:844-847`); an anchor not found is `E-ANCHOR` (`:855-857`) and a repeated anchor is `E-ANCHOR-AMBIGUOUS` (`:863`). Decided conflict C15 keeps the valid lines of a bad block and marks the reviewer partial; decided conflict C02 flags a missing anchor instead of letting it block silently or refusing it. B's input rule is the opposite of both.
- **Blocking is computed in the ledger and the reviewer has no blocking key.** `ROW_INPUT_KEYS = {"grade","rule","wrong_outcome","anchor","finding","label"}` (`:64`); `make_row` sets `blocking = profile["blocking"](row) and scope == "in" and rnd != "sweep"` (`:889`). Decided conflict C16 keeps the reviewer's flag as an input and records the effective flag; undecided C05 is the decider choice. Adopting B as the round model would pre-empt C05 and contradict C16.
- **Scope rule hides findings until a sweep.** A new row at review 2 or 3 outside a changed hunk is stored `deferred` with scope `outside` (`:1856-1881`); a sweep after the loop records them with `would_block` (`:2245-2268`). The bundle's Ledger loop shows the effect: 12 deferred or demoted CRITICAL+MAJOR labels counting nine sweep rows, and the delivery outcome "ESCALATE; sweep FAIL" (`.dev/experiments/346-validation/phase5/FINAL-REPORT.md:105,118`). [CODE-VERIFIED]
- **Cost and reuse.** Effort XL, risk High, reuse Medium: new code in `src/`, spec-panel prompt rewrite and its text pins (`tests/skills/test_review_loop_extension.py:120-127`) (synthesis C-13 table; 12 §9).
- **Compliance is unmeasured.** Whether the E2 models would comply on re-ask when input is refused is `[UNVERIFIED]`, no data in any effort (02 Gaps 9). The plan-answer protocol has the same gap.

### 7. The only loop-level evidence does not favour the verify-only design over re-find

- The bundle states "Convergence not proven; no validated winner" and "None of the completed, measured loops reached a clean PASS" (`FINAL-REPORT.md:42,75`); one completed loop per proposed variant (`:41,79`); `SNAPSHOT-STATE.txt:3` "No valid-success verdict is implied" (02 §8). [CODE-VERIFIED for `FINAL-REPORT.md`]
- The Ledger (find once, verify-only) arm: new CRITICAL+MAJOR labels 13 / 9 / 3 over reviews 1 to 3, growth 22.16%, outcome "ESCALATE; sweep FAIL" (`FINAL-REPORT.md:105`); at its final review three prior MAJOR labels were unresolved and its sweep found nine MAJOR findings (`:79,116`). The pre-427 controls ended 11 / 9 / 8 and 12 / 7 / 4 (`:97-98`). One loop each; the report itself says "observations from one completed loop each, not a ranking" (`:79`). Honest reading: the Ledger arm's final-review count (3) is lower than the two pre-427 controls (8 and 4); it still ended FAIL by escalation and by sweep. No claim of a measured gap between re-find and verify-only follows. [CODE-VERIFIED]
- No research file records a live multi-round run of the master `ledger.py` either; for A, rounds 2 and 3 are covered by unit tests only (24 tests in `test_review_ledger.py`, including rounds 1 to 3 at `:277-304` and `:476-490`) [CODE-VERIFIED for tests; the absence claim is by the research files' silence, 02 Gaps 10].

### 8. Consumers outside the spec loop re-find by nature

- PR review: Augment and Codex are GitHub bots with re-trigger phrases and silence timers (`pr_submit/reviewers.py:41,395-424`; adapters `retrigger_phrase`, `reviewer_activity`), so a verify-only plan-answer protocol cannot be imposed on them; the internal verify seam S2b checks one finding at a time (`fsm.py:941`; 10 §1.1 step 5, §1.2 seam B). [CODE-VERIFIED via 10 §1]
- Single-reviewer-per-round consumers: reflect is single-pass (E1 position; synthesis C-13 table). rf-qa verifies by prompt (item 3).

### 9. External context

None of this chooses between A, B and C; it supports carrying rows across rounds and verifying singletons, which all three options do.
- Cursor Bugbot: the pipeline ends with "dedupe against bugs posted in earlier runs", the same job as cross-round row matching (`ledger.py:166-171`). https://cursor.com/blog/building-bugbot [external, vendor blog, extracted 2026-11-13; web-01 §3.1]
- LinkedIn: findings from a single model are passed back for verification rather than dropped. https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale [external, vendor blog; web-01 §3.3]
- A Zenodo preprint reports 56.8% of confirmed defects found by exactly one model (167 of 294), which argues against any rule that drops singletons in either round model. https://zenodo.org/records/21328807 [external, preprint, not peer reviewed, single-team corpus, read from the abstract; web-01 §3.4]

## Correctness argument

Properties A guarantees, each tied to code that can be checked, followed by what it does not guarantee.

**P1. Reviews are bounded by the cap.** After change 1, `merge_round` refuses `n > cap_reviews` before recording anything, and `n` must equal `len(rounds)+1` (`ledger.py:114-118`). So a ledger holds at most `cap_reviews` rounds (3 by default), and the existing ESCALATE path at `n == cap` (`ledger.py:93-96`, render `:475-486`) is the last review. After change 2 the cap cannot be silently different from the one the first round stored.

**P2. A PASS needs a real, quorate review and no known blocker.** The verdict is computed in one place, `ledger.py:273-274`, and a PASS is returned only if (a) `valid >= quorum` (changes 3 and 5), (b) no row is `open` or `regressed` with `blocking` true, and (c) no rejected line carried `blocking: true` (change 5, with C15's record). The only other route to PASS is `defer`, a human command (`ledger.py:350-360`). A round with zero valid blocks is refused today and stays refused (`ledger.py:150-157`); quorum generalises that refusal.

**P3. Status is truthful.** A row reaches `resolved` only by the four-step chain in Evidence item 4: fix map `applied`, a hunk touching the span, a later non-degraded round with no re-report, and it returns to `regressed` on any later re-find. No path reaches `resolved` through an invalid reviewer, a reviewer's `prior` line, or the reviser's claim alone.

**P4. Strictly safer than today.** Every change either refuses a merge (1, 2, 5) or withholds clearing or PASS (3, 4, 5). None adds a way to reach PASS or `resolved`. The set of inputs that return PASS under A is a subset of those that return PASS today; D2's clearing gate does not change a verdict by itself because `resolved_check` rows are not in `_brief_ids` (`ledger.py:99-104`), and it is the quorum rule that protects the verdict (D3) [INFERENCE from the cited code; the proof is by reading `merge_round`, not by a test run]. This is why the conflict's minimum fixes can land without waiting for C05 or the clusterer.

**P5. Backward compatible.** New keys are additive under the same schema string; `load` checks only `schema` (`ledger.py:41-49`); readers default missing keys. The default loop (one anchor reviewer from review 2) has quorum 1 and the same observable behaviour; the CLI round-trip test needs no change (`test_review_cli.py:196-327`).

**P6. No scope rule hides a finding.** Every valid finding in the current candidate becomes or joins a row in the round it is found. The RE-REVIEW brief already tells the reviewer to cite the changed line for inherited text (`document_review_loop_prompts.md:48`), so a contradiction a fix creates in untouched text can be found and can block. The verify-only design stores such a finding `deferred` unless it falls inside a changed hunk (`review_ledger.py:1856-1881`). A chooses surfacing over loop termination; the cap bounds the price.

**What A does not guarantee.** Convergence. A reviewer that reports a new blocking finding every round keeps the loop open until the cap, and then the loop escalates to the user with the open rows. A single reviewer's flag still decides blocking until C05 is settled (D4). Silence from a valid reviewer still clears a row that passed the earlier checks; A records the unanswered priors but does not gate on them.

## Risks and mitigations

**Weakest point: late findings.** Because every round re-finds, a defect the reviewer notices only at review 2 or 3 can reopen a loop that the verify-only design would have kept closed. The evidence cannot settle it: no effort ran the master ledger across rounds 2 and 3 with a panel, E2 ran round 1 only (`audit-D/summary.md:3,34`), and every completed bundle loop ended FAIL, ESCALATE or with a failed sweep, including the Ledger arm (`FINAL-REPORT.md:75,105`). A's worst case is repeated escalations to the person who owns the loop. This proposal does not claim a measured advantage in convergence over B or C.

| Risk | Why it matters | Mitigation |
|---|---|---|
| Late findings reopen loops | The weakest point above | The cap by refusal bounds the cost to `cap_reviews` reviews. Measure before adding a rule: the round in which a row opened is already stored (`row["history"][0]["round"]`, `ledger.py:201`) and the reviewer in `members`, so the late-row rate is computable from existing ledgers. To tell in-hunk from out-of-hunk rows, store the changed new-text ranges when `apply_revision` computes `ops` (`ledger.py:315`), observation only. If late blocking rows outside changed hunks turn out to be the main cause of ESCALATE, add a deferral policy inside `merge_round`. That is Option C's second half built on the same engine, not a second ledger. |
| Silence still clears | A lazy but valid reviewer could omit a prior row | Four checks precede clearing (Evidence item 4); `unanswered_priors` is recorded; gating on it is deferred because it would make A depend on prior-line compliance that is not measured (the same gap that blocks B's plan-answer protocol, 02 Gaps 9). If the recorded rate is high, adding the gate is a small change plus a fixture update. |
| Refusal wastes a reviewer run | A degraded would-be PASS is refused | The merge is deterministic and the valid reports stay on disk; only the invalid or missing reviewer is re-run, then `merge` is called again with all reports. A degraded FAIL is recorded, not refused. A degraded FAIL consumes one of the three review numbers [INFERENCE on cost; accepted as the price of never certifying a thin review]. |
| `--cap` default change breaks a caller | Callers that pass `--cap` each round | The prompts file and the CLI tests do not pass `--cap` on later rounds (`document_review_loop_prompts.md:70`; `test_review_cli.py:196-327`). A caller that passes the same value is unaffected. |
| Quorum denominator is wrong | A coordinator could drop a failing reviewer from `--report` | `--resolution`, when given, supplies the panel size and a reviewer with no report is an abstention. When a coordinator gives neither, the denominator is the report count, which is today's behaviour; a module that wants the guarantee passes the resolution. |
| Seams not ready | The engine still calls the v1 parse, annotate, cluster and match functions, and is single-document (02 §5.1) | The five changes touch round logic only and sit around calls at `ledger.py:128,136,165,169`, so they can land before C01/C12 and survive their replacement. Multi-file rows are work for C01/C12 under any C13 option. |
| Decider pre-empted | C05 is undecided | A adds no decider; blocking stays in one place (`ledger.py:187,213-218`). Un-blocking by one reviewer's non-blocking re-report (`:216-218`, `test_refound_as_nonblocking_stops_failing_the_review`) is a D4/C05 behaviour and is untouched. |
| Prompt and code drift | The loop prompt names refusal rules in prose | One sentence at `document_review_loop_prompts.md:70` is updated in the `src/superclaude/rules/prompts/` copy and the `plugins/superclaude/rules/prompts/` copy found in the repo; a skill-text test pins it (see Test coverage). |

## Test coverage needed

Gate commands (12 §8, G2 and G10): `uv run pytest tests/review/test_review_ledger.py tests/review/test_review_cli.py` (37 tests today) and the skill-text group G10 (178 tests) for the prompt sentence.

### Existing tests that change

| Test | Today | Change |
|---|---|---|
| `tests/review/test_review_ledger.py:376-385` `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` | round 2 with one valid and one broken reviewer merges, and `status(led)["L1"] == "resolved"` (`:385`) pins D2 and D3 together | Replace with two tests. (a) Two resolved reviewers, one broken, no blocking finding: the merge raises `LedgerError`, the ledger JSON is byte-identical to before, `L1` stays `resolved_check`. (b) Same panel where the valid reviewer reports a blocking finding: the round is recorded, `degraded is True`, verdict FAIL, `L1` not cleared and listed under `not_cleared`. |
| `tests/review/test_review_ledger.py:128-130` and `test_review_cli.py:236` | assert `block_ok` and `brief_ids` for a two-reviewer first round | No change expected; they stay green because both reviewers are valid. They also pin that the result keeps `block_ok`. |

Tests that must stay green as the positive and invariant cases: `:193-217` (clearing when every reviewer is valid), `:220-252`, `:255-274`, `:277-304`, `:318-338` (prior lines never change a status), `:345-373` (no valid block refused), `:388-393`, `:476-490`, `:518-566`.

### New tests

1. `merge_round(..., 4, ...)` raises when `cap_reviews == 3`; the ledger is unchanged (D16a; 12 §9 D16).
2. A ledger created with cap 2: review 2 with an open blocking row gives FAIL and decision ESCALATE; review 3 is refused.
3. CLI: `review merge --round 4` exits nonzero and writes neither the ledger nor the report (twin of `test_review_cli.py:425`).
4. CLI: `--cap 2` on an existing cap-3 ledger errors; `--cap 3` and omitted `--cap` succeed; round 1 with `--cap 2` creates cap 2; round 1 without `--cap` creates cap 3 (`test_review_ledger.py:136` stays).
5. Quorum boundary: a three-reviewer panel with one valid block is degraded; two valid is not (k-1 versus k).
6. A single-reviewer round (no resolution) and a one-reviewer re-review resolution both use quorum 1 and pass as today.
7. `--resolution` lists three reviewers, one report is missing: the missing reviewer counts as an abstention and the panel size is three.
8. A degraded would-be PASS is refused with nothing written; the same round with the missing reviewer's valid report added merges.
9. A degraded round that FAILs is recorded with `degraded: true`, the merged report carries the `degraded:` header line, and `ledger verdict` still exits 10 or 11 by decision.
10. Clearing: all reviewers valid and none re-reports `L1` gives `resolved` with a `cleared` event (the positive case, `:193-217`); an invalid reviewer whose parsable line re-reports `L1` leaves it `open` or `regressed`; below quorum nothing clears.
11. A round cannot PASS while a rejected line carried `blocking: true`. Conditional on C15's `rejected[]` field. Include a replay-shaped fixture for the E2 flip pattern (a blocking line with an over-length anchor, no other blocking row).
12. `unanswered_priors` lists a prior blocking row a valid reviewer did not answer, changes no status, and does not stop a clearing round (guards the choice not to gate).
13. Backward compatibility: a ledger JSON written by the current code (fixture generated at HEAD `792cf8c52`, no new keys) loads and accepts review 2.
14. Rendering: `review: n of cap` never prints `4 of 3` because round 4 is refused; the `degraded:` line appears only when degraded.
15. Skill-text test in the G10 style: the rules prompt names the three refusal conditions (round above the cap, below-quorum would-be PASS, no valid block) and keeps the sentence `Only these scripts change a finding's status` (`document_review_loop_prompts.md:70`); check that `test_review_rules_text.py:34-42` (no new line between a brief and its findings-block bullet) is not violated because the edit is in the Review panel paragraph, not in a brief.

Not needed: any change to the 353 reflect CLI tests, the 271 legacy reflect tests, or the panel golden files, because C13 Option A does not touch `panel.py`, `cluster.py`, reflect contract code or templates (12 §8 G9).

## Cost

| Item | Estimate | Basis |
|---|---|---|
| C13-specific code | about 50 to 70 added lines in `ledger.py`, about 15 in `merge_cmd.py`, one sentence in two copies of the loop prompts file | [INFERENCE] from the five changes above; no new module, no new CLI command, no new exit code |
| Tests | 1 rewritten into 2, about 14 new, mostly small fixtures built from the existing `seeded.md`, `clean.md` and helpers at `test_review_ledger.py:22-93` | list above |
| Effort and risk (synthesis rating) | M effort, Medium risk | synthesis C-13 Option A row. This proposal's reading: the C13 part alone is S to M and low risk because P4 holds (no change adds a way to PASS); the Medium belongs to the parse, cluster and multi-file seams that C01 and C12 own and every option needs |
| Compared with B and C | B is XL and High (new code in `src/`, port or rewrite of a 2,668-line installed script with no multi-reviewer merge, prompt rewrite and its text pins); C is XL and High (needs B's half plus the unified clusterer, both halves unmeasured in combination) | synthesis C-13 Options B and C rows |
| Run cost per loop | Review 1: N reviewers by template. Reviews 2 and 3: one anchor reviewer each. Merge is deterministic and makes no model call. Extra cost only on a refused degraded PASS (re-run of one reviewer) | `panel.py:600-616`; `ledger.py` has no model call. Token cost per round was not measured by any effort for either model; whether re-find at review 2 or 3 costs more than answering a plan is [UNVERIFIED] |
| Sequencing | Land changes 1 to 5 first. They do not depend on C01, C02, C05 or C12 and survive their replacement. Then the seams, then, only if the late-row measurement says so, a deferral policy | Risks table |
| Not costed here | The decider (C05), rf-qa halts (C19 B), multi-file rows (C01/C12), contract bump (C11) | owned by those conflicts |

**Bottom line for the adversarial round.** Option A resolves C13 now at M effort with every change one-directional (it can only refuse or withhold), preserves the invariants that only the script changes a status and that the reviewer keeps its flag as input, and keeps the verify-only half available as a later policy on the same engine if the late-row measurement shows it is needed. The honest cost is that A does not reduce the chance that late findings keep a loop open, and no evidence in the research says whether that chance is high.
