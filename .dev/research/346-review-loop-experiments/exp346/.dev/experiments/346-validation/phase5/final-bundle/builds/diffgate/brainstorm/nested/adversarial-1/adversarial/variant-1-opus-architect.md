# Variant 1 (architect): `spec-panel-diffgate`, a ledger-driven delta gate for spec re-reviews

## 0. Summary

The loop's state moves out of prose and into one file the reviewer cannot write by hand: a ledger kept by a stdlib Python script, `diffgate.py`, shipped in a new infrastructure skill `sc-diffgate`. The script takes the snapshot each review sees (so nobody has to remember the "saved copy"), computes the next review's surface as a token-level diff against the last reviewed snapshot, checks every finding line in the report against that surface, derives blocking status and the verdict itself, and refuses to open the next review while the reviser's edits contain a hunk that no blocking finding of the last review accounts for. The reviewer, the reviser and the coordinator each run one script step. Each step checks the ledger's state, so a skipped step stops the next one with a non-zero exit, and nothing quietly falls back to a fresh whole-document review.

Design priorities, in order: (1) fail closed: a missing step stops the loop visibly instead of degrading it; (2) one data format (the `DG` finding line) that any reviewer command can emit, so `/sc:reflect`, rf-qa and the `/sc:implement` final review can adopt the same script later without changing it; (3) the smallest change to the reviewer: review 1 is unchanged apart from writing `DG` lines.

## 1. Problem and evidence

Measured on S1 (`AB-REPORT.md`, `ARMB-REPORT.md`; 2 replicates per arm, model claude-opus-5-5):

| Arm | R3 critical+major proxy | Growth after 2 fix cycles | Clean pass |
|---|---|---|---|
| Control (pre-427) | 8, 4 (mean 6.0) | 57.7%, 69.3% (mean 63.5%) | no |
| 427 text | 6, 5 (mean 5.5) | 23.1%, 36.3% (mean 29.7%) | no |
| 427 + `--re-review --baseline` (Arm B) | 6, 1 (mean 3.5) | 27.8%, 32.1% (mean 30.0%) | no |

Causes this proposal removes, each with the evidence that it exists:

1. **Fix-induced findings on changed lines are re-reviewed by a fresh whole-document review.** 89% of review-2 and 100% of review-3 new findings in the 427 arm carry `origin=changed` (`AB-REPORT.md` line 30). In the best run (flg-r2), all six review-2 blockers (N1 to N6) and the one review-3 blocker (N12) are fix-induced (`spec-panel-round2.md` lines 95-120; `spec-panel-round3.md` line 84). This proposal keeps those findings in scope (they are real) but limits them to the hunks the last fix wrote, and stops a line from being re-opened once a review has seen it unchanged.
2. **Revisers change text no blocking finding names.** Round 1 disposition applied 21 of 22 findings, 8 of 9 non-blocking ones included (`disposition.md` line 39); round 2 applied all 15 rows, 5 minor findings and 4 citation notes included ("Minor findings were applied too", `disposition-round2.md` line 12), plus two "related defects found while applying" (line 13). N5, which produced review 3's only blocker N12, is itself the fix of F22, a non-blocking round-1 finding (`spec-panel-round2.md` line 48; `spec-panel-round3.md` line 35). This proposal makes the next review refuse to open while any reviser hunk is not mapped to a blocking finding of the last review.
3. **Severity is reviewer judgement, and the verdict follows it.** The 427 grading relabels some MAJOR findings as minor in one replicate and nowhere else (`ARMB-REPORT.md` line 37); the panel itself split on N12 (Nygard minor, Adzic and Wiegers blocking, `spec-panel-round3.md` line 144). This proposal removes the reviewer's say over three parts: whether a MAJOR has the `outcome=` field that makes it blocking, whether a prior blocker is `resolved` without a change, and the verdict line. The severity label itself stays judgement (section 7).
4. **Nothing mechanical stops or scopes the loop.** Design doc section 12 says it outright: "a coordinator that drops the flags or the saved copy starts a fresh first review, and nothing enforces the count". The Arm B reviewer computed its own `git diff --no-index -w -U0` and judged scope itself (`spec-panel-round3.md` line 25). This proposal moves the count, the snapshot, the surface and the verdict into the ledger.

Causes this proposal leaves in place:

- A fix can still be wrong. A reviser who fixes a blocker with new text can introduce a new blocker in that text (N12 is exactly that). The design bounds this to one review per fix (section 5) and to blocker-mapped hunks; it does not make fixes correct.
- Severity labels on new findings stay the reviewer's call. The checker requires the fields; it cannot judge whether a stated wrong outcome is real.
- Review 1 quality and breadth are untouched: review 1 is still a full-document review.
- The 3-review cap is unchanged; a loop that still has a blocker at review 3 escalates, as today.

## 2. Mechanism: the loop, step by step

Actors: the **reviewer** is `/sc:spec-panel-diffgate` (the command file running in a worker or a person's session); the **script** is `diffgate.py` (section 3), always run by one of the other actors through Bash; the **reviser** is whatever agent or person edits the document; the **coordinator** is the Orca coordinator or person who dispatches steps. `D` is the ledger directory the coordinator names once with `--ledger D` and passes unchanged to every review (default `.dev/diffgate/<document stem>/`, relative to the working directory).

| Step | Actor | Action | Reads | Writes |
|---|---|---|---|---|
| R1.a | reviewer | `diffgate.py open --ledger D --doc <doc>`. No ledger yet, so this is review 1. | `<doc>` | `D/ledger.json` (state `reviewing`, review 1), `D/snap-r1.md` (byte copy), `D/surface-r1.md` (says "review 1 of 3: full document; no prior findings") |
| R1.b | reviewer | Full critique review, exactly as `/sc:spec-panel` does today. The report adds one section, `## Diffgate findings`, with one `DG` line per finding (`anchor=doc`, `quote=` exact text) and no verdict line yet. | `<doc>`, `D/surface-r1.md` | report (`--output` file or `<report-dir>/spec-panel-report.md`, unchanged rule) |
| R1.c | reviewer | `diffgate.py close --ledger D --report <report>`. The script reads back every quote, derives `blocking` and the verdict, and prints `verdict: PASS` or `verdict: FAIL`; the command appends that line as the report's last line. On exit 3 (reject) the reviewer corrects the listed lines once and re-runs; a second reject runs `close --demote` (section 4). | report, `D/ledger.json`, `D/snap-r1.md` | `D/review-r1.json` (parsed findings, derived fields), `D/brief-r1.md` (reviser brief), ledger state `reviewed` |
| F1.a | reviser | Reads the report's `Reviser brief`, which points to `D/brief-r1.md`: the blocking ids `R1.<n>`, each one's quote and the reviser rules. Edits only what those findings need; every edit either rewrites text inside a blocking finding's quote or carries that finding's id (for example `(R1.4)`) in its added text, which is 427's existing "each added paragraph or table cites its finding id" rule. | report, `D/brief-r1.md`, `<doc>` | `<doc>` |
| F1.b | reviser | `diffgate.py gate --ledger D` (read-only self-check) until it exits 0; reports the bytes before and after that it prints. | `<doc>`, `D/snap-r1.md`, `D/review-r1.json` | nothing |
| R2.a | reviewer | `diffgate.py open --ledger D --doc <doc>`. Requires state `reviewed`, verdict FAIL, review below 3. Runs the fix gate authoritatively: an unmapped hunk is exit 4, the command stops, writes no report and the review does not count. Otherwise it snapshots and computes the surface from `snap-r1.md` to the current document. | `<doc>`, `D/*` | `D/snap-r2.md`, `D/surface-r2.md` and `D/surface-r2.json` (hunks `H2.<n>` plus the prior blocking table), ledger review 2 `reviewing` |
| R2.b | reviewer | Reviews the surface. It may Read the whole document as read-only context, but every new finding anchors to a hunk `H2.<n>` with a quote inside that hunk's changed span, or declares `anchor=none` (recorded `deferred: pre-existing`). One `DG-STATUS` line per prior blocking finding: `resolved by=H2.<n>`, `open`, or `regressed`. | `D/surface-r2.md`, `<doc>` | report |
| R2.c | reviewer | `close` as in R1.c. | as R1.c | `D/review-r2.json`, `D/brief-r2.md` |
| F2.a/b | reviser | As F1, with ids `R2.<n>`. | as F1 | `<doc>` |
| R3.a-c | reviewer | As R2, surface from `snap-r2.md`. At `close`, review 3 with FAIL sets ledger state `capped` and prints `escalate: <open blocking ids>`; the report carries no Reviser brief (427 bullet 6) and the escalation instead. | as R2 | `D/review-r3.json`, ledger `capped` |
| End | reviewer | On PASS at any review, or at the cap, the command runs `diffgate.py final --ledger D` and appends its output to the report under `## Deferred (pre-existing, not looped on)`. | `D/review-r*.json` | `D/deferred.md`, ledger state `passed` or `capped` |
| End | coordinator | Reads the report's last line (or `diffgate.py status --ledger D`): PASS is done; `capped` escalates to the user with the open blocking findings. | `D/ledger.json` | nothing |

What the coordinator no longer keeps: the review count, the prior-findings file and the saved copy. 427 bullet 4 makes these the coordinator's job; here the ledger holds all three, and `open` derives N from the ledger instead of from the prior report's header.

What happens when an actor skips its step:

| Skipped step | What stops it |
|---|---|
| Reviewer never runs `open` | `close` exits 2 (`no review is open`); the report has no verdict line, so the coordinator sees an incomplete review. |
| Reviewer never runs `close` | The next `open` exits 2 (`review N is still reviewing`): the loop stops visibly instead of becoming a fresh review. |
| Reviser skips the gate | The next `open` runs the same gate and exits 4. |
| Coordinator runs plain `/sc:spec-panel` instead | Not stopped by the script; the variant can only govern runs that use it. Prose only (section 7). |
| Coordinator passes a new `--ledger` path mid-loop | `open` on an empty ledger starts review 1: a fresh full review. Residual risk; mitigated only by the brief naming one path (section 10). |

## 3. Who computes the diff: the `sc-diffgate` script and its interface

### 3.1 Choice: a script, not a fixed command sequence

A fixed sequence (`cp` the spec, then `git diff --no-index -w -U0`) is what the Arm B reviewer already ran by itself. It fails on three counts here:

- **Granularity.** The S1 spec keeps one paragraph per line (317 lines, 76,328 bytes after round 2, `spec-panel-round3.md` line 25: about 240 bytes a line). A line diff turns a one-word citation fix into a whole paragraph of surface. The review-3 changed-line list in flg-r2 already covered 27 lines, each a paragraph (line 25). The script diffs at word level inside changed lines, so the surface is the changed words, shown in their line.
- **Reflow noise.** `-w` ignores whitespace inside a line but not a paragraph rewrapped across lines. The script compares whitespace-split token streams, so a pure reflow yields no hunk.
- **State.** Counting reviews, holding snapshots, checking finding lines and deriving the verdict need a program; a command sequence cannot refuse a step taken out of order.

### 3.2 Where it lives and how it is called

- Source: `src/superclaude/skills/sc-diffgate/scripts/diffgate.py`, Python 3.10 stdlib only (`argparse`, `difflib`, `hashlib`, `json`, `re`, `shutil`, `pathlib`, `datetime`). `difflib` is already used in `src/superclaude/cli/eval/expect.py` (line 33), so no new dependency.
- Host skill: `src/superclaude/skills/sc-diffgate/SKILL.md` (infrastructure, delegate-only, like `sc-bare-review`). A script reaches `~/.claude/skills/` only inside a folder that has a `SKILL.md` (`make sync-dev` and the installer both test for it, `Makefile` line 115, `src/superclaude/cli/install_skill.py` line 104).
- Name check: the installer skips an `sc-<x>` skill when `src/superclaude/commands/<x>.md` exists and the command does not activate it (`src/superclaude/cli/install_skills.py` lines 40-59, 88-98). There is no `commands/diffgate.md`, so `sc-diffgate` installs. A skill named `sc-spec-panel-diffgate` would be silently skipped and its stale copy deleted, because `commands/spec-panel-diffgate.md` exists and calls the script by path, not through a `Skill` line. This is why the skill is not named after the command.
- Call form, same as `sc-issue-protocol` (`refs/claim.md` lines 14-17): `uv run --no-project python "<diffgate base>/scripts/diffgate.py" <subcommand> ...`, where `<diffgate base>` is `~/.claude/skills/sc-diffgate` when that folder exists, else the project `.claude/skills/sc-diffgate` copy (skills read `~/.claude/skills/` first, project `CLAUDE.md` dual-surface rule). If neither exists the command stops with `E-DIFFGATE-MISSING` and never falls back to a plain review.

### 3.3 Subcommands

Every subcommand prints exactly one JSON object on stdout (`ok`, `exit`, `message`, plus the fields below) and nothing else, so a model or a coordinator script can read it the same way.

| Subcommand | Run by | Arguments | Effect | Output fields |
|---|---|---|---|---|
| `open` | reviewer, first Bash call | `--ledger D --doc PATH [--profile spec-panel]` | No ledger: create it, review 1. Else require state `reviewed`, verdict FAIL, review below 3; run the fix gate; snapshot; compute the surface. | `review`, `surface_md`, `surface_json`, `snapshot`, `hunks`, `prior_blocking` |
| `gate` | reviser (self-check), and inside `open` | `--ledger D [--doc PATH]` | Read-only. Diff the last snapshot against the document; map each hunk to an open blocking id. | `hunks`, `unmapped` (id, lines, added text), `bytes_before`, `bytes_after`, `bytes_by_id` |
| `check` | reviewer (dry run) | `--ledger D --report PATH` | Read-only. Parse and validate the report's `DG` lines against the open review's surface. | `errors` (line number, rule, text), `findings` |
| `close` | reviewer, last Bash call | `--ledger D --report PATH [--demote]` | `check`; on pass record the findings, derive `blocking`, compute the verdict, write the brief. `--demote` records failing findings as `deferred: unanchored` instead of rejecting. | `verdict_line`, `blocking`, `deferred`, `demoted`, `escalate` (review 3 FAIL), `brief` |
| `final` | reviewer, on PASS or cap | `--ledger D` | Collect the deferred and minor findings of all reviews, deduplicated by normalized quote. | `deferred_md` (path), `count` |
| `status` | coordinator | `--ledger D` | Read-only summary. | `state`, `review`, `verdict`, `open_blocking` |

Exit codes (one table, used by every subcommand):

| Code | Meaning | Who acts |
|---|---|---|
| 0 | done | |
| 2 | usage, I/O or state error: ledger missing or corrupt, step out of order, snapshot hash changed, `--doc` differs from the ledger's document, non-UTF-8 input | the caller stops and reports the message; never falls back to a fresh review |
| 3 | report rejected: a `DG` line fails a rule of section 4 | reviewer corrects once, then `close --demote` |
| 4 | fix gate failed: at least one hunk maps to no open blocking id | reviewer stops without reviewing; coordinator sends the `unmapped` list back to the reviser |
| 5 | cap reached: review 3 closed FAIL; no further review | coordinator escalates to the user with the open blocking findings |
| 6 | the loop already passed | nothing to do |

### 3.4 Files in the ledger directory

| File | Written by | Content |
|---|---|---|
| `ledger.json` | `open`, `close`, `final` | `{"format": "diffgate/1", "doc": <path>, "doc_realpath": <path>, "profile": "spec-panel", "state": "reviewing" or "reviewed" or "passed" or "capped", "reviews": [{"n", "snapshot", "snapshot_sha256", "opened_utc", "surface", "report", "report_sha256", "verdict", "open_blocking": [ids], "demoted", "fix_gate": {"hunks", "bytes_before", "bytes_after", "bytes_by_id"}}]}`. Written atomically (temp file and `os.replace`). |
| `snap-r<k>.md` | `open` | Byte copy of the document as review k saw it. `open` and `close` re-hash it and exit 2 if it changed. |
| `surface-r<k>.json` | `open` | `{"review", "base", "base_sha256", "current_sha256", "hunks": [{"id": "H<k>.<n>", "new_lines": [a, b], "old_lines": [c, d], "heading": <nearest preceding # line>, "added": [{"line", "start", "end", "text"}], "removed": [{"text"}], "maps_to": [ids]}], "prior": [{"id", "sev", "quote", "outcome"}]}`. Review 1 has `"hunks": []` and `"scope": "document"`. |
| `surface-r<k>.md` | `open` | What the reviewer reads: a 6-line rules block (section 4), the prior blocking table (id, severity, quote, outcome), then one block per hunk: `### H2.4  lines 60-60  under "### 2.2 Worker contract"  fixes R1.22`, followed by a fenced copy of the current lines with added words wrapped `{+ ... +}` and removed words `[- ... -]`. |
| `review-r<k>.json` | `close` | Every parsed `DG` and `DG-STATUS` line with the derived fields (`blocking`, `status`, `deferred`). |
| `brief-r<k>.md` | `close` | The reviser brief: open blocking ids only, each with quote and outcome, the four reviser rules (section 5) and the exact `gate` command line. Minor and deferred findings are absent, so the brief cannot invite fixing them. |
| `deferred.md` | `final` | The end-of-loop list (section 6). |

### 3.5 The diff algorithm

1. Read both texts as UTF-8; split into lines; normalize each line for comparison as `" ".join(line.split())`.
2. `difflib.SequenceMatcher(None, old_norm, new_norm, autojunk=False)` at line level; keep the non-equal opcodes.
3. For each non-equal block, split the old and new block into whitespace tokens (remembering each token's line and character offset) and run a second `SequenceMatcher` on the token lists. Inserted and replaced tokens are the **changed span** on the new side; deleted and replaced tokens on the old side are the **removed span**. A block with no token change (reflow, whitespace) is dropped.
4. A hunk is a maximal run of adjacent new-side lines that hold changed tokens (context 0). A pure deletion becomes a hunk with an empty changed span, positioned at the new line where the text used to be, and keeps its removed text.
5. Hunk ids are `H<k>.<n>` in document order, where k is the review the surface feeds, so ids never repeat across reviews.

Cost: the line pass is linear-ish on a few hundred lines; the token pass runs only inside changed blocks. Expected well under a second for S1 (not measured).

### 3.6 Extension seam

One dict, `PROFILES`, holds the severity vocabulary and the blocking rule. v1 ships one entry, `spec-panel`: severities `critical|major|minor`, blocking = `critical`, or `rule=FR-8|FR-9`, or `major` with a non-empty `outcome`. An adopter (section 11) adds an entry; nothing else in the script knows which reviewer produced the report. The review cap is a module constant (`CAP_REVIEWS = 3`), not a flag, so no caller can raise it and the pinned cap text stays true.

## 4. The checker: proving the reviewer stayed inside the surface

### 4.1 The finding lines

The report keeps its prose (expert analysis, boundary table, Whittaker attacks) and adds one machine section, `## Diffgate findings`. Each finding id in the prose must be one of these lines. Quotes and outcomes are JSON strings, so any character can be quoted and parsing is unambiguous (`json.loads` on the token).

```text
## Diffgate findings
DG-COVER H2.1 H2.2 H2.3 H2.4
DG-STATUS R1.4 resolved by=H2.2
DG-STATUS R1.9 open quote="WC-4 requires `status` to be one of"
DG-STATUS R1.2 regressed by=H2.3 quote="the coordinator opens the contract at the reported path"
DG R2.1 sev=major anchor=H2.4 quote="Before step 1, record whether Orca's Claude agent command" outcome="a correct launcher run is recorded as WC-1 not exercised": WC-1 proof reads the wrong channel
DG R2.2 sev=minor anchor=H2.1 quote="AC-1.2 runs each P1 command" outcome=-: AC-1.2 includes load
DG R2.3 sev=major anchor=none quote="7.2 step 1: worker-start --task" outcome="source-editing workers start in the shared worktree": step 1 placement
```

The reviewer never writes `blocking=`, a verdict or a review number; the script derives all three (the parent-derives rule of `~/.claude/skills/sc-implement-protocol/refs/qa.md`, "the parent runs the closed order ... over the parent-confirmed blocking findings only", line 97). Blocking under the `spec-panel` profile: `sev=critical`; or `rule=FR-8` or `rule=FR-9`; or `sev=major` with an `outcome` that is not `-`. Everything else is a note. `anchor=none` is always a note, recorded `deferred: pre-existing`, whatever its severity.

### 4.2 Rules `check` applies

| Rule | Check | Demotable on second reject |
|---|---|---|
| C1 | Exactly one `## Diffgate findings` section; every non-blank line in it parses as `DG`, `DG-STATUS` or `DG-COVER`. | no |
| C2 | New ids are `R<k>.<n>` with k = the open review; no id already in the ledger. | no |
| C3 | Every token matching `R<k>.<n>` (k = this review) in the report outside the section is an id inside it, so a blocker cannot sit in the prose and be missing from the verdict. | no |
| C4 | Quote read-back: the whitespace-normalized quote occurs in the current document (`side=new`, default) or in the base snapshot (`side=old`, for a finding about removed text); at least 20 characters unless it is the whole changed span. | yes |
| C5 | Anchor: review 1 allows `anchor=doc` only. From review 2, `anchor=H<k>.<n>` names a hunk of this surface and at least one occurrence of the quote overlaps at least one changed token (or removed token for `side=old`) of that hunk; `anchor=doc` is rejected; `anchor=none` is accepted as deferred. | yes |
| C6 | `sev` is in the profile's vocabulary; `outcome` is present (`-` allowed). | no |
| C7 | Exactly one `DG-STATUS` line per open blocking finding of the last review, and no other ids except optional `regressed` lines for earlier ids that were resolved. | yes (missing or bad line counts as `open`) |
| C8 | `resolved` carries `by=<hunk of this surface>`. With an empty surface nothing can be resolved, so 427's "an empty diff leaves every prior blocking finding open" is now a parse rule. | yes (counts as `open`) |
| C9 | `open` carries a quote present in the current document. | yes (counts as `open`) |
| C10 | `regressed` carries `by=` and a quote overlapping that hunk's changed span; it re-opens the earlier id at its recorded severity. | yes (dropped) |
| C11 | The report header has `review: <k> of 3` with k from the ledger. | no |
| C12 | Any `verdict:` line already in the report equals the computed verdict. | no |
| C13 | `DG-COVER` lists exactly the surface's hunk ids (from review 2). Weak evidence: it proves the reviewer named every hunk, not that it read each one. | no |

### 4.3 On reject

1. `close` exits 3 with every error as `{line, rule, text}`; the ledger does not change.
2. The reviewer command corrects those lines once, in the same session (no new worker), and re-runs `close`.
3. A second exit 3 runs `close --demote`: findings failing a demotable rule are recorded `deferred: unanchored` (never blocking), failing `DG-STATUS` lines count as `open`, and `demoted=<n>` is written to the ledger and the report. Demotion can only move toward FAIL for prior findings and toward "note" for new ones; it never invents a PASS from a broken status line.
4. A non-demotable failure after the second try ends the run without a verdict: under `--unattended` the contract is `failed`, the review does not count, and the coordinator re-dispatches the reviewer. A missing or empty section can never become PASS.

Why demote instead of failing the run: anchoring mistakes are the expected failure, and a failed run costs a session and wastes the review. The cost is a blind spot (a real blocker the reviewer could not anchor ends up deferred); it is bounded by `final` showing every demoted finding with its severity label and by counting demotions in the measurement (section 9).

### 4.4 Hand-edited ledgers

The reviewer has Write access, so it could edit `ledger.json` directly. The next `open` therefore replays the check: it re-runs `check` on the recorded report (`report_sha256` must still match) against the recorded surface and recomputes the verdict and open blocking ids; any difference with the ledger is exit 2. A forged ledger buys nothing unless the report itself passes the rules, and then it is just a valid report.

## 5. Convergence rule for fix-induced defects on changed lines

Fix-induced defects are in scope: they are the real defects of S1 (N1 to N6, N12). The goal is not to hide them but to make each piece of new text get exactly one look, and to keep the amount of new text proportional to the open blockers. Five rules, all enforced by the script:

| # | Rule | Enforced by |
|---|---|---|
| V1 | **One look per change.** Review k+1's surface is the diff from `snap-r<k>` (what review k saw) to the current document. A span written by fix k is anchorable in review k+1 only. Text unchanged since the last review is closed: no new finding can anchor to it, whoever wrote it and whenever. A later fix that changes it again opens it again, for one review. | `open` computes the surface from the last snapshot; C5 |
| V2 | **Every fix hunk maps to one open blocker.** A hunk of fix k is mapped when its added text carries the id of an open blocking finding of review k, or its removed or replaced words overlap that finding's quote in `snap-r<k>`. Any unmapped hunk stops the next `open` with exit 4. | `gate`, run by the reviser and again inside `open` |
| V3 | **Minor findings never reach the reviser.** The brief lists open blocking ids only; a minor or deferred id written into the document does not map a hunk (V2), so fixing a minor finding fails the gate. This is what stops the round-2 pattern of 15 applied rows for 6 blockers. | `close` writes the brief; `gate` |
| V4 | **Severity is pinned once recorded.** A prior finding is re-checked through `DG-STATUS` only, which has no severity field: it stays at the severity and blocking status of the review that raised it. A `regressed` line re-opens an earlier id at its recorded severity. Upward drift on carried findings is therefore impossible; drift can only occur on new text, once. | parser grammar; C7 to C10 |
| V5 | **The cap is a constant.** `CAP_REVIEWS = 3`; review 3 closed FAIL sets `capped`; `open` then exits 5. | `close`, `open` |

Why this should converge where 427 did not: under V2 the hunks of fix k are bounded by the open blockers of review k, and under V1 the new blockers of review k+1 can only sit in those hunks. The best Arm B run shows the ratio: fix 1 applied 21 rows and produced 6 new blockers; fix 2 applied 15 rows and produced 1 (`disposition.md` line 39, `disposition-round2.md` line 35, `spec-panel-round3.md` line 165). Under V3, fix 2 would have applied 6 rows (N1 to N6), and N5, the parent of review 3's only blocker, would never have existed because it is the fix of the non-blocking F22. A pre-existing defect cannot enter after review 1 at all (section 6). So the surface shrinks each cycle unless the reviser's fixes are themselves defective, and each defective fix gets one review, not a cascade of whole-document reviews.

What it does not do: if review k+1 misses a defect in a fix-k span, V1 closes that span and no later review re-opens it. That is the price of convergence; section 9 measures it with an out-of-loop audit.

Rejected alternatives:

- A severity ceiling at review 3 (for example "a review-3 finding is blocking only if CRITICAL"). It would lower the measured count by relabelling, not by fixing, and would hide real regressions in the last fix.
- A byte budget per fix cycle. The design doc already rejects a size limit because it conflicts with FR-8/FR-9 gap filling (`docs/designs/spec-panel-review-loop.md` line 73). `gate` reports `bytes_by_id` instead, so a reviser that spends 4 KB on one finding is visible.

## 6. Pre-existing defects review 1 missed

- From review 2 on, a defect in text the surface does not cover is recorded with `anchor=none`. The script records it `deferred: pre-existing`, whatever its severity label. It never blocks, never appears in the reviser brief, never gets a `DG-STATUS` line in a later review and never counts toward the verdict. Findings demoted by a second reject (`deferred: unanchored`) follow the same path.
- Giving the reviewer a legal outlet matters: a reviewer that sees a real problem in unchanged text and has nowhere to put it is the one most tempted to force an anchor (section 10).
- `final` runs once, when the loop ends (PASS at any review, or the cap). It writes `D/deferred.md` and the command appends it to that last report under `## Deferred (pre-existing, not looped on)`: one row per finding with id, review, severity label, quote, outcome and kind (`pre-existing` or `unanchored`), deduplicated by normalized quote (the earliest id wins). Minor notes from all reviews follow in a second table.
- Acting on the list is a person's decision, outside the loop: starting a fresh loop on the finished document (a new ledger, which is a new review 1) is the explicit way to do it. The loop itself never cycles on them.

## 7. Comparison with PR 427's `--re-review --baseline`

| 427 bullet | What 427 asks in prose | What diffgate makes mechanical | What stays prose, and its residual risk |
|---|---|---|---|
| 1 Mode | Without both flags the run is a first review; stop on an unreadable file. | The ledger decides first review or re-review; a missing or out-of-order step is exit 2, never a fresh review. | A coordinator can still pass a new ledger path (a new review 1) or call plain `/sc:spec-panel`. Risk: one brief line. |
| 2 Grading | CRITICAL and FR-8/FR-9 block; a MAJOR blocks only with a concrete wrong outcome. | `blocking` is derived from `sev`, `rule` and the presence of `outcome`; prior severities are pinned (V4). | Whether the outcome is real and the label right is judgement. Risk: a reviewer adds a thin outcome to make a MAJOR block. |
| 3 Verdict | Last line `verdict: PASS` or `FAIL`. | Computed by `close`; C12 rejects a disagreeing line; the next `open` replays it. | None beyond the inputs above. |
| 4 Cap | `review: N of 3` from the prior header; coordinator keeps count, prior file and saved copy. | N, snapshots and prior findings live in the ledger; `open` exits 5 at the cap. | None for runs that use the ledger. |
| 5 Re-review output | Status table; findings on lines changed against the baseline, self-tagged `origin`; `unchanged` is minor unless it quotes the changed line. | The surface is computed (word level, reflow-proof); C5 checks every anchor against it; `resolved` needs a hunk (C8); an empty surface keeps every prior blocker open. | Whether a `resolved` hunk truly fixes the finding, and whether the reviewer read every hunk (C13 only checks it named them). Risk: a lazy `resolved by=` on the right hunk. |
| 6 Reviser contract | Revise only blocking-named text; add no unrequested mechanism; cite ids; report bytes. | Every hunk must map to an open blocker (V2); minor ids cannot map (V3); `gate` prints the bytes. | The reviser can put a valid id on an unrelated edit. Risk: bounded by the next review seeing every such hunk and by `bytes_by_id`. |
| 7 Precedence | A brief may narrow, not widen. | A brief cannot widen the surface: the checker ignores the brief. | A brief can still tell the reviewer to skip the script; the command then fails closed at the next step. |

What 427's flags actually bought on S1 (Arm B vs plain 427: same growth, R3 proxy 3.5 vs 5.5 from one replicate, `ARMB-REPORT.md` line 29) shows the limit of prose: the reviewer honoured the format and still judged scope itself. Diffgate keeps 427's literal cap text and grading sentence and moves the scope, the count and the verdict out of the reviewer's hands.

## 8. Exact changes, file by file

Summary: three new source files, two new test files, two one-line test edits, one design note. `/sc:spec-panel` (both copies), `HOW-WE-WORK.md` and `WORKER-CONTRACT.md` are not edited.

### 8.1 `src/superclaude/commands/spec-panel-diffgate.md` (new)

A byte copy of `src/superclaude/commands/spec-panel.md` with these changes only:

- Frontmatter: `name: spec-panel-diffgate`; `description: "spec-panel with a computed re-review surface: a ledger script snapshots each review, diffs it, checks every finding's anchor and derives the verdict"`.
- Title: `# /sc:spec-panel-diffgate - Expert Specification Review Panel (delta-gated re-reviews)`.
- Usage line 22: replace `[--re-review <prior-findings-file> --baseline <saved-copy>]` with `[--ledger <dir>]`.
- `## Review Loop` (line 256): replace the seven bullets with the nine one-line bullets below. Each is one physical line, as in 427, so line matchers see them whole. The canonical cap text and the at-cap clause are kept verbatim (`tests/skills/test_review_severity_rule.py` lines 215-219); no cap number above 2 appears.

```markdown
## Review Loop

1. **Mode**: the review loop applies to `--mode critique` only; every critique run first runs the script's `open` step on the ledger (`--ledger <dir>`, default `.dev/diffgate/<document stem>/`), which decides whether this is review 1 (no ledger yet: a full review of the document) or a re-review of the computed surface; `--re-review` and `--baseline` are ignored with the note `re-review flags ignored: ledger in use`; any non-zero exit of the script stops the run with the script's message, and the run never falls back to a first review.
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision; the script derives blocking from each `DG` line (`sev=critical`, `rule=FR-8` or `rule=FR-9`, or `sev=major` with an `outcome` other than `-`), and the reviewer never writes it.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open), copied from the `verdict_line` that the `close` step prints; the reviewer never composes its own.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, with N taken from the `open` output; when `open` exits 5, do not review, HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and a re-review skips the Improve step and writes no revised specification.
5. **Re-review output**: read the surface file `open` names; write one `DG-STATUS` line per prior blocking finding (`resolved by=<hunk>`, `open quote="..."`, or `regressed by=<hunk> quote="..."`) and one `DG-COVER` line naming every hunk; anchor each new finding to a hunk with a quote that overlaps its changed words, or write `anchor=none`, which the script records as `deferred: pre-existing` and never treats as blocking; FR-8 to FR-10 and the Guard Condition Boundary Table cover guards whose location lies in a changed span; an empty surface leaves every prior blocking finding open and still counts as a review.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line that points to `<ledger>/brief-r<N>.md` and restates this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding in that brief names; add no rule, mechanism or section no blocking finding calls for; each edit either changes words inside a listed finding's quote or carries that finding's id in its added text; run the script's `gate` step until it exits 0 and report the bytes before and after that it prints; the next review refuses to open while any edit maps to no listed finding.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the computed surface and the prior blocking findings, and may not grade a minor finding as blocking.
8. **Diffgate steps**: run `uv run --no-project python "<diffgate base>/scripts/diffgate.py"` where `<diffgate base>` is `~/.claude/skills/sc-diffgate` if it exists, else the project `.claude/skills/sc-diffgate` copy, and stop with `E-DIFFGATE-MISSING` if neither exists; call `open --ledger <dir> --doc <file>` before reading the document, write the report with a `## Diffgate findings` section of `DG` lines and no verdict line, call `close --ledger <dir> --report <report>`, and on exit 3 correct the listed lines once and call `close` again, then `close --demote` if it still exits 3; append the printed `verdict_line` as the last line.
9. **Deferred list**: when `close` prints `verdict: PASS`, or prints `escalate:` at review 3, call `final --ledger <dir>` and add its list under `## Deferred (pre-existing, not looped on)` above the verdict line; deferred findings are shown once there and never enter a reviser brief.
```

- `## Unattended mode` (line 451): copied verbatim except `/sc:spec-panel` becomes `/sc:spec-panel-diffgate` on line 453. The report path stays `<report-dir>/spec-panel-report.md`, so coordinator scripts that read it need no change. The ledger is not an artifact of the command's contract; it is listed nowhere in `artifacts`.
- Nothing else changes (experts, flow, FR-8 to FR-10, output formats, Boundaries). The Will Not item "Modify specifications without explicit user consent" stays true: the script writes only into the ledger directory.

### 8.2 `src/superclaude/skills/sc-diffgate/SKILL.md` (new)

```markdown
---
name: sc-diffgate
description: Infrastructure skill holding diffgate.py, the ledger script that computes a re-review surface (word-level diff of the last reviewed snapshot against the current document), checks every finding's anchor against it, derives blocking findings and the verdict, and gates reviser edits to open blocking findings. Called by /sc:spec-panel-diffgate. Delegate-only, no slash command.
allowed-tools: Read, Bash
---

# sc-diffgate
<diffgate base> is the directory that holds this SKILL.md (~/.claude/skills/sc-diffgate/ when installed; the project .claude/skills/sc-diffgate/ copy in a dev checkout).
## Call form          (uv run --no-project python "<diffgate base>/scripts/diffgate.py" <subcommand>)
## Subcommands        (table of section 3.3)
## Exit codes         (table of section 3.3)
## Finding lines      (grammar of section 4.1, rules C1-C13)
## Ledger files       (table of section 3.4)
## Adding a profile   (the PROFILES dict: vocabulary + blocking rule; nothing else changes)
```

### 8.3 `src/superclaude/skills/sc-diffgate/scripts/diffgate.py` (new, outline, about 400 lines)

```python
#!/usr/bin/env python3
"""diffgate: ledger, surface, anchor checker and fix gate for document re-reviews. Stdlib only."""
CAP_REVIEWS = 3                       # pinned cap: 2 fix cycles; not a flag on purpose
FORMAT = "diffgate/1"
PROFILES = {"spec-panel": {"sev": ("critical", "major", "minor"), "blocking": _spec_panel_blocking}}
EXIT_OK, EXIT_STATE, EXIT_REJECT, EXIT_GATE, EXIT_CAP, EXIT_PASSED = 0, 2, 3, 4, 5, 6

def read_text(path) -> str                       # UTF-8 strict, else EXIT_STATE
def tokens(lines) -> list[Token]                 # (text, line, start, end) per whitespace token
def diff(old: str, new: str, review: int) -> list[Hunk]   # section 3.5, two SequenceMatcher passes
def quote_spans(doc: str, quote: str) -> list[(start, end)]   # whitespace-normalized occurrences
def map_hunks(hunks, open_blocking, snapshot) -> (mapped, unmapped)   # rule V2
def render_surface_md(surface) -> str             # rules block, prior table, {+ +} / [- -] marks
def parse_report(text) -> Parsed                  # DG, DG-STATUS, DG-COVER; json.loads for quoted values
def check(ledger, parsed, surface, doc, base) -> list[Error]      # C1-C13
def derive(parsed, profile, prior) -> Outcome     # blocking, statuses, verdict, deferred
def replay(ledger) -> None                        # section 4.4, EXIT_STATE on mismatch
def load_ledger(dir) / save_ledger(dir, data)     # atomic: temp file + os.replace
def cmd_open / cmd_gate / cmd_check / cmd_close / cmd_final / cmd_status
def main(argv) -> int                             # argparse subparsers; prints one JSON object
```

### 8.4 `tests/skills/test_diffgate_script.py` (new)

Loads the script with `importlib.util.spec_from_file_location`, as `tests/skills/test_workflow_archive.py` does (lines 22-27), plus one CLI test through `subprocess` with `sys.executable`. Cases, all in `tmp_path`:

1. A paragraph reflowed across lines yields no hunk; a whitespace-only change yields no hunk.
2. One changed word in a 300-character line yields one hunk whose changed span is that word.
3. A pure deletion yields a hunk with an empty changed span and its removed text.
4. Hunk ids are `H<k>.<n>` in document order.
5. `open` without a ledger creates review 1 and `snap-r1.md`; a second `open` while `reviewing` exits 2.
6. `close` derives blocking per the profile (critical; FR-8; major with outcome; major with `-` is not).
7. C5: a quote that occurs only outside the cited hunk's changed span is rejected (exit 3).
8. `anchor=none` is recorded `deferred: pre-existing` and never blocks, even at `sev=critical`.
9. C8: `resolved` without `by=` is rejected; under `--demote` it counts as `open` and the verdict is FAIL.
10. A report with no `## Diffgate findings` section never yields PASS, with or without `--demote`.
11. C3: an id `R2.5` in the prose and missing from the section is rejected.
12. `gate` exits 4 for an unrelated edit, 0 when the edit carries an open blocking id, 0 for an edit inside a blocking quote, 4 when the edit carries only a minor id.
13. An empty surface keeps every prior blocking finding open.
14. Review 3 closed FAIL sets `capped`; the next `open` exits 5. A PASS makes the next `open` exit 6.
15. A hand-edited `ledger.json` verdict, or a changed snapshot, makes the next `open` exit 2.
16. `final` deduplicates by normalized quote and lists demoted findings as `unanchored`.

### 8.5 `tests/skills/test_spec_panel_diffgate_command.py` (new)

Text-presence pins on the new command, in the style of `tests/skills/test_spec_panel_review_loop.py`: frontmatter name; Usage carries `--ledger <dir>`; the `## Review Loop` section has the nine bullets in order, each on one line; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` (imported from `test_review_severity_rule`) are in it; both script locations, `~/.claude/skills/sc-diffgate` and the project `.claude/skills/sc-diffgate`, are named; the string `src/superclaude` is absent; the exit codes 3, 4 and 5 and `E-DIFFGATE-MISSING` are named; `anchor=none` and `deferred: pre-existing` are present.

### 8.6 Existing tests that the new command file would otherwise break

- `tests/skills/test_worker_contract.py`: `_check_no_unattended_sections` (line 831) requires the set of commands with a `## Unattended mode` heading to equal `UNATTENDED_COMMANDS`, which must equal P1 plus P2 with exactly 31 entries (line 1564). Adding the variant to that dict would break the count, so add a separate map and use it in the one check:

  ```python
  # Additive experiment variants: same Unattended section as their parent, name swapped.
  UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}
  ...
  assert set(have) == set(UNATTENDED_COMMANDS) | set(UNATTENDED_VARIANTS), (...)

  @pytest.mark.parametrize(("variant", "parent"), sorted(UNATTENDED_VARIANTS.items()))
  def test_variant_unattended_section_matches_parent(variant, parent):
      assert _unattended_section(variant) == _unattended_section(parent).replace(
          f"/sc:{parent}`", f"/sc:{variant}`"
      )
  ```
  (`_unattended_section(cmd)` is used at line 1016; its exact signature was not read, UNVERIFIED beyond that call.)
- `tests/recommend/test_routing_refresh.py` line 33: `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` becomes `{"graph", "impact", "issue", "spec-panel-diffgate"}`, because line 648 asserts the shipped command files minus that set equal the refresh inventory's active commands.
- `tests/skills/test_review_severity_rule.py` scans tracked files under `src/` (line 28); the bullets above avoid its banned phrases and cap patterns (no "3 fix cycles", no "if findings exist"). No edit needed.

### 8.7 `docs/designs/spec-panel-diffgate.md` (new)

This proposal, trimmed to decisions, formats and the measurement plan, with a "Promotion" section: if S1 passes, a later PR folds `--ledger` into `/sc:spec-panel` itself (both copies, with the 427 tests updated) and retires the variant.

### 8.8 Not changed, and why

- `plugins/superclaude/commands/`: the plugin tree is a subset; `tests/commands/test_routing_plugin_parity.py` (lines 42-45) mirrors only the commands `src/superclaude/commands/README.md` lists, so a new command needs no mirror.
- `src/superclaude/core/HOW-WE-WORK.md`: an experimental variant gets no routing row until it is promoted.
- `.claude/`: produced by `make sync-dev`; never staged.

### 8.9 Install note and brief substitution for an experiment

Install, without touching `~/.claude/commands/sc/spec-panel.md`:

```bash
cp src/superclaude/commands/spec-panel-diffgate.md ~/.claude/commands/sc/spec-panel-diffgate.md
mkdir -p ~/.claude/skills && cp -R src/superclaude/skills/sc-diffgate ~/.claude/skills/sc-diffgate
sha256sum ~/.claude/commands/sc/spec-panel.md   # must equal the value recorded before the run
```

Never `superclaude install --force` for this (it rewrites every command file, `spec-panel.md` included). `superclaude install-skill sc-diffgate` should also work (function `install_skill` in `src/superclaude/cli/main.py` line 444; the dashed subcommand name is click's default naming, UNVERIFIED here), but `cp` is enough.

The one-line substitution in every review brief (reviews 1, 2 and 3):

```text
/sc:spec-panel   ->   /sc:spec-panel-diffgate --ledger .dev/orca-command-refactor/review/diffgate
```

Any `--re-review` and `--baseline` left in the round-2 and round-3 briefs are then ignored by bullet 1. The diffgate step line the reviser briefs gain:

```text
Before you finish, run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py gate --ledger .dev/orca-command-refactor/review/diffgate` and change your edits until it exits 0; fix only the ids in the brief file it names.
```

## 9. Measurement plan on scenario S1

**Design.** Same scenario, base commit, model, briefs and loop as Arm B (`ARMB-REPORT.md` lines 5-6), 2 replicates, with only the brief changes of section 8.9 and the install of section 8.9. Controls are reused (`ctl-r1`, `ctl-r2`), as Arm B did, with the same caveat that they were not run at the same time.

**Primary metrics (unchanged definitions):**

- R3 critical+major proxy: every CRITICAL or MAJOR label in the review-3 report, counted the way the control is counted: new findings, open or regressed prior blockers, **and** deferred or demoted findings. Counting deferred findings too means diffgate cannot pass the bar by moving findings out of the verdict. The gated count (blocking findings only) is reported beside it, not used for the bar.
- Spec growth after fix cycle 2, in bytes, against the 57,763-byte original.

**Predictions and reasoning:**

| Metric | Control mean | Arm B | Bar | Predicted per replicate | Predicted mean |
|---|---|---|---|---|---|
| R3 critical+major proxy | 6.0 | 6, 1 | 3 or fewer in both | 1 to 3 | 2.0 |
| Growth after 2 fix cycles | 63.5% | 27.8%, 32.1% | 44.4% or less | 15% to 25% | 20% |
| Clean PASS by review 3 | none | none | (alternative to the proxy bar) | one replicate in two | |

- Review 1 is unchanged, so expect 13 to 17 blockers as in Arm B. Fix 1 then touches only those (Arm B also fixed 8 non-blocking findings in flg-r2), so the fix-1 surface is about 13 of 21 rows' worth of text.
- Review 2 sees only fix-1 hunks. In flg-r2, 5 of the 6 review-2 blockers came from fixes of blocking findings and 1 (N5) from the fix of a non-blocking one, so expect 3 to 5 review-2 blockers.
- Fix 2 touches 3 to 5 ids instead of 15 rows. Arm B's fix 2 produced 1 (flg-r2) to about 5 (flg-r1) new blockers from 15 rows; scaled to a third of the rows, expect 0 to 2 new blockers, plus 0 or 1 prior blocker left open, plus 0 to 1 deferred MAJOR (the review-3 surface is small, so the reviewer has little unchanged text in front of it). That gives 1 to 3, mean about 2.
- Growth: Arm B's 30% includes the non-blocking fixes and the "related defects found while applying" (`disposition-round2.md` line 13). Removing them cuts roughly a third; the inline ids add a few hundred bytes. Expect about 20%. The growth bar was already met by 427, so this is the low-risk half.
- Confidence: about 60% that both replicates meet the proxy bar; about 95% for growth.

**Secondary metrics (needed to read the result):** checker rejects per review (exit 3) and demotions; gate failures (exit 4) per fix cycle and the extra reviser sessions they cost; deferred findings per review and their labels; hunks and changed words per surface; tool calls, sessions and wall time per loop, against Arm B's logs.

**Blindness audit (out of loop, not counted in the bar).** After the loop ends, one fresh `/sc:spec-panel --mode critique` review 1 of the final document per replicate, in a new session with no ledger. Every blocker it finds is classified by the script's history: text written by fix 1 or fix 2 that the loop closed, or text present since the original. Only the first kind measures what diffgate hides.

**What would mean the idea failed:**

1. Either replicate's R3 proxy is above 3 and neither reached a clean PASS: the bar fails, as 427 and Arm B did.
2. The R3 proxy mean is 3.5 or higher (no better than Arm B): the mechanism adds cost without effect.
3. The blindness audit finds 2 or more blockers in fix-written text the loop closed, in either replicate: diffgate converges by not looking, not by fixing.
4. More than a quarter of new findings in reviews 2 and 3 are demoted, or the gate fails more than once per fix cycle on average: the anchoring or the mapping rule is unworkable for a model, whatever the counts say.
5. A replicate stalls (no review 3 delivered) because of a script exit that the briefs cannot recover from.

## 10. Costs and risks

**Costs per loop (estimates, not measured):**

| Item | Added |
|---|---|
| Reviewer tool calls | 2 Bash per review (`open`, `close`), 1 Read of the surface, 1 more Bash on an anchoring reject, 1 `final` at the end: about 7 to 10 per loop |
| Reviser tool calls | 1 to 3 `gate` runs per fix cycle |
| Sessions | none on the normal path; 1 extra reviser session per gate failure at `open`, 1 extra reviewer session per non-demotable reject |
| Wall time | seconds per script call; reviews 2 and 3 should be shorter, because the surface is smaller and the reviewer no longer derives its own diff (the flg-r2 reviewer ran `git diff` and re-read 20 to 28 citation groups) |
| Disk | three snapshots of the document plus small JSON files |
| Maintenance | one 400-line stdlib script with its own tests, one more command file to keep in step with `spec-panel.md` until promotion |

**Ways the mechanism could make the loop worse:**

| Risk | How it happens | Mitigation | Residual |
|---|---|---|---|
| Blind to a real regression | A defect in fix-k text is missed in review k+1; V1 then closes it for good. | One look is guaranteed; the blindness audit measures misses. | Real. This is the trade the design makes. |
| Action at a distance | A fix to line A makes unchanged line B wrong. | Anchor on A's changed words and cite B in the text; the reviewer may Read the whole document. | A reviewer that reads only the surface may not notice B. |
| Anchor gaming | A reviewer quotes a few changed words plus the unchanged sentence it wants to attack. | C5 needs overlap with changed words; the 20-character minimum; `anchor=none` as a legal outlet. | A long quote straddling a change passes. Not mechanically closable without rejecting legitimate context. |
| Id gaming by the reviser | A valid id pasted onto an unrelated edit passes the gate. | `bytes_by_id`; the next review sees every such hunk. | The edit is reviewed once, so gaming adds surface, not hidden text. |
| Renumbering noise | Renumbering headings or lists makes many one-token hunks, each needing an id. | None in v1; the gate output names them, so the reviser adds the id once per hunk. | Possible extra reviser work; open question 3. |
| Inline ids clutter the spec | `(R2.4)` tokens accumulate. | 427 already requires ids on added text; the finished document can drop them in a final pass outside the loop. | Cosmetic. |
| Forced FAIL from a broken status line | Demotion counts a broken `DG-STATUS` as `open`. | One correction round before demotion. | A sloppy reviewer can keep a resolved blocker open until the cap. |
| False PASS from demotion | A real blocker that could not be anchored ends up deferred. | Shown with its label in the deferred list; counted in the proxy. | The loop can stop with a real blocker in the deferred list. |
| Fail-closed stalls | A script error or a permission prompt for `uv run` stops a worker. | Every stop prints a reason; nothing silently degrades. | Whether Orca workers can run `uv run --no-project python` without a prompt is UNVERIFIED. |
| Wrong ledger | A coordinator passes a new `--ledger` path mid-loop: a fresh review 1. | One path in every brief; `status` shows the review number. | Prose only. |

## 11. Later adopters

The script knows nothing about spec-panel beyond its `PROFILES` entry, and the `DG` line is the only interface. Adoption cost differs:

- **`/sc:reflect`** (UC-2 post-execution audits): it audits code changes across many files against a spec, not one document. The surface concept fits (review k+1 sees only what fix k changed), but the script diffs one text file. Adoption needs a multi-file surface (a list of file pairs, or a git tree pair) and a `reflect` profile mapping Drift and Regression to blocking. Medium effort; worth doing only if S1 passes.
- **rf-qa agents** (Fix Cycle phase, `src/superclaude/agents/rf-qa.md` line 379): the Fix Cycle already re-checks prior blocking issues one by one. For single-file gates (a task file, a final report) it can adopt diffgate as is with an `rf-qa` profile (CRITICAL and IMPORTANT blocking, MINOR a note). Low effort. Multi-file research gates need the same multi-file surface as reflect.
- **`/sc:implement` final review**: no. It already has the stronger version: pinned review trees, parent-written `origin=` from `git diff` hunk headers, an inherited cap at note, and parent-derived verdicts (`~/.claude/skills/sc-implement-protocol/refs/qa.md` lines 137-196). Diffgate copies that model to documents; porting it back would duplicate machinery.
- **`/sc:spec-panel` itself**: the intended end state. If S1 passes, fold `--ledger` into `spec-panel.md` and its plugin mirror, update the 427 tests, and retire the variant (section 8.7).

## 12. Open questions

1. Should the coordinator, not the reviewer, run `open` and `close`? It separates powers more cleanly (the reviewer could not touch the ledger at all), but adds a coordinator step per review, and the replay check (section 4.4) already removes most of the reason.
2. Should there be a hard cap on hunks or bytes per blocking id? This proposal only reports `bytes_by_id`; a cap would conflict with FR-8/FR-9 gap filling.
3. Should hunks whose only change is digits (renumbering) be exempt from the fix gate? Cheap to add; it opens a small hole (a changed number can be a real change).
4. Should a `sev=critical` finding with `anchor=none` escape the deferred list and force an escalation? This proposal says no (never blocking after review 1), at the cost of possibly ending on PASS with a known critical defect listed under Deferred.
5. Is a 20-character minimum quote right for short table cells and identifiers?
6. Can an Orca worker run `uv run --no-project python ~/.claude/skills/...` without a permission prompt under the experiment's settings? UNVERIFIED; it decides whether the unattended path works at all.
7. Is `superclaude install-skill` the subcommand's real name? UNVERIFIED (click default naming); the install note uses `cp` instead.
8. Should the ledger directory default live under `.dev/diffgate/` and be staged like `.dev/tasks/`? No repo rule covers it today.
9. Pre-registration: the bar counts deferred findings in the R3 proxy (section 9). The owner should confirm this counting before any run, so the result cannot be argued either way afterwards.
