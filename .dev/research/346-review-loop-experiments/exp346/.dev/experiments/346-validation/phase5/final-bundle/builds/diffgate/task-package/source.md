# SPEC: diffgate, a computed re-review surface for `/sc:spec-panel` (issue #346)

Status: specification only, nothing implemented. Variant command: `spec-panel-diffgate`.
Source: `/sc:brainstorm` run in `.dev/brainstorms/346-diffgate/` (seed brief, enrichment, three proposals, adversarial debate and merge under `nested/adversarial-1/`).

## 1. Problem and evidence

- On scenario S1 (Orca worker-contract spec, 3 reviews, 2 fix cycles, 2 replicates per arm) no arm reached PASS. Review-3 critical+major proxy: control 8 and 4 (mean 6.0), PR 427 text 6 and 5, 427 plus `--re-review --baseline` (Arm B) 6 and 1; growth after two fix cycles 63.5%, 29.7%, 30.0% (AB-REPORT.md, ARMB-REPORT.md).
- In the 427-text arm, new findings sit on lines the previous fix changed (89% in review 2, 100% in review 3). In Arm B the reviewer still ran its own `git diff --no-index -w` and judged its own scope; under 427 the diff, the review count, the verdict and the reviser's scope are all prose.
- Revisers fix minor findings too: Arm B applied 21 of 22 and 14 of 14 rows (flg-r1) and all 15 rows (flg-r2), "Minor findings were applied too".
- Verified for this spec (`nested/adversarial-1/adversarial/debate/evidence-flg-r1.md`): in flg-r1 all 4 review-3 blockers sit on text written by fixes of review-2 blockers, which sit on fixes of review-1 blockers: one new blocker per blocking fix in cycle 2 (4 of 4), against about 1 in 6 in flg-r2.
- Diffgate removes the scope, count, verdict and minor-fix causes mechanically. It does **not** change the defect rate of blocking fixes, and this spec makes S1 measure that rate instead of hiding it.

## 2. Mechanism

One stdlib Python script, `diffgate.py`, owns the loop's state in a directory `<dir>` passed as `--diffgate-dir <dir>` (under `--unattended` the default is `<report-dir>/diffgate`). The reviewer and the reviser each run it at fixed points, and each step's output is the next step's only input, so a skipped step stops the loop with a non-zero exit instead of turning into a fresh whole-document review. The script never writes the specification. Every subcommand prints one JSON object (`ok`, `exit`, `message`, `review`, plus its own fields); an accepted review whose verdict is FAIL still exits 0, so the review result is read from `verdict`, never from the exit code.

Files in `<dir>`: `ledger.json` (the only state: per review the document hash, hunks, prior findings, accepted check, accepted fix map, attempt counter, deferred list, flags `degraded`, `closed`, `invalid`); `doc-r<N>.md` (byte copy of what review N saw); `surface-r<N>.md` (review N's surface, N of 2 or more); `result-r<N>.json` (accepted findings with derived origin, blocking and verdict); `reject-r<N>.txt`; `reviser-brief-r<N>.md` (blocking ids only); `fixmap-r<N>.txt` (written by the reviser); `deferred.md`.

The loop, in order:

| Step | Who | What happens | Reads | Writes |
|---|---|---|---|---|
| 1. Open review 1 | reviewer command | `diffgate.py begin --dir <dir> --doc <spec> --expect-round 1`. Empty ledger, so review 1: full document. | spec | `ledger.json`, `doc-r1.md` |
| 2. Review 1 | reviewer | Today's full critique, unchanged, plus one machine block `## Diffgate findings` with one `FINDING` line per finding (or `FINDINGS none`) and no `verdict:` line. | spec | report |
| 3. Check 1 | reviewer command | `diffgate.py check --dir <dir> --report <report>`: parses the block, reads every quoted anchor back against `doc-r1.md`, derives blocking (CRITICAL; FR-8 or FR-9; MAJOR with an `outcome` other than `-`) and the verdict, writes the reviser brief, prints `verdict_line`, which the command appends as the report's last line. On a reject (exit 1) the reviewer repairs only the named lines once and reruns. | report, ledger, `doc-r1.md` | `result-r1.json`, `reviser-brief-r1.md`, `deferred.md` |
| 4. Fix cycle 1 | reviser | Reads `reviser-brief-r1.md` only (blocking ids; minors never reach it). Edits the spec. `diffgate.py fixcheck` pre-fills `fixmap-r1.txt` from inline `R1.<j>` tags; the reviser confirms each line `H2.<n> R1.<j>[,R1.<m>]` or writes `declined R1.<j> <reason>`; the map's first line is `doc_sha: <sha>`. `fixcheck` exits 0 only when every changed hunk is owned by an open blocking id and every blocking id has a hunk or a `declined` line. Three failing runs in one cycle record `fix-rejected`, stop the reviser and escalate without spending a review. | brief, spec, `doc-r1.md` | spec, `fixmap-r1.txt`, ledger fix record |
| 5. Open review 2 | reviewer command | `begin ... --expect-round 2` re-runs the fix check authoritatively (an unmapped hunk exits 1 and opens nothing), replays check 1 against the ledger (a hand-edited ledger exits 6), snapshots `doc-r2.md` and computes `surface-r2.md`: the diff of `doc-r1.md` against the spec, with hunk ids `H2.<n>`, section names, the owner ids from the fix map, and the prior blocking table. | spec, ledger, `doc-r1.md`, `fixmap-r1.txt` | `doc-r2.md`, `surface-r2.md` |
| 6. Review 2 | reviewer | Reads the surface; may read the spec as read-only context, which cannot widen what is reviewable. One `PRIOR` line per prior blocking id: `resolved by=H2.<n>`, `open quote="..."`, `regressed by=H2.<n> quote="..."`, or `withdrawn` (only for an id the reviser declined). New findings anchor by quoted text on a changed token of a cited hunk (`hunk=H2.<n>`), or through `via=H2.<n>` with a quote of the changed text an unchanged line depends on (at most 2 per review), or attach to a prior id with `cites=`. Anything else is recorded `deferred: pre-existing` and is never blocking. | `surface-r2.md`, spec | report |
| 7. Check 2 | reviewer command | As step 3, against `doc-r2.md` and the surface. Prior findings keep their recorded severity (the `PRIOR` grammar has no severity field). An empty surface leaves every prior blocker open. | | `result-r2.json`, brief, `deferred.md` |
| 8. Fix cycle 2 | reviser | As step 4, with `R2.<j>` ids and baseline `doc-r2.md`. | | spec, `fixmap-r2.txt` |
| 9. Review 3 | reviewer | As steps 5 to 7 with `--expect-round 3`; surface = diff of `doc-r2.md` against the spec. No reviser brief at review 3. | | `result-r3.json` |
| 10. End | reviewer command, coordinator | At a derived PASS (any review) or at review 3, the report carries, above the verdict line: the open blocking findings with their fix chains (for example `R1.5 -> R2.1 -> R3.2`), `## Deferred (pre-existing, not looped on)` with `deferred.md` shown once, and, when any blocking-grade finding was deferred, demoted or withdrawn, the line `scoped PASS: ...`. The last line is exactly `verdict: PASS` or `verdict: FAIL`. A FAIL at review 3 prints `halt: escalate`; any later `begin` exits 4. | ledger | report |

Rules this enforces mechanically:
- **One look per change.** Review k+1's surface is the diff from what review k saw to the current spec. Text written by fix k is anchorable in review k+1 only; text unchanged since the last review is closed unless a later fix changes it again. The diff runs at line level with `difflib.SequenceMatcher(autojunk=False)` and then at token level inside changed blocks; only changed tokens are eligible (adjacent lines merge into one hunk id within 2 lines, but gap and context lines never become eligible). A pure reflow is dropped, unless it changes the count of list, heading or table lines, in which case it is a `structural: yes` hunk that needs an owner.
- **Every fix hunk has a blocking owner.** Minor findings, citation notes and "related defects" cannot own a hunk, so fixing them fails `fixcheck`. This removes the measured minor-fix route (flg-r1 R3-7, flg-r2 F22 to N5 to N12).
- **The script, not the reviewer, decides blocking, origin, the verdict and the review count.** The cap stays `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`.
- **Reject handling.** One repair turn. Then finding-level violations become `deferred: unanchored` and a missing `PRIOR` line counts as `open` (`degraded: yes`). A structural failure (no parseable block, an `R<k>.<j>` id in the prose missing from the block, a wrong `review:` line) ends the run with no verdict. The ledger allows one more `begin` for the same review on the same snapshot. A second structural failure sets the terminal state `invalid`, which is escalated and never replaced.
- **Pre-existing defects review 1 missed** go to `deferred.md`: never blocking, never in a reviser brief, never citable, shown once at the end with the reviewer's own severity label and the sentence "PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated."

**Measured causes: removed or left.**

| Cause (measured on S1) | Diffgate |
|---|---|
| Re-review attacks the whole document; the reviewer derives its own diff and scope | Removed: the surface is computed; out-of-surface findings are deferred, never blocking |
| Revisers apply minor findings and "related defects" | Removed: `fixcheck` refuses any hunk without a blocking owner |
| Severity drift between rounds | Partly: carried findings keep their recorded severity; a new finding's label is still the reviewer's |
| Nothing mechanical holds the count, the order of steps or the verdict | Removed: ledger count, locks between steps, script-derived verdict, cap as a constant |
| Fixes of blocking findings introduce new blockers on the fixed text (flg-r1: 4 of 4) | **Left.** In scope by design, reviewed once, recorded as chains; no in-theme rule lowers it without hiding defects |

**Compared with 427's `--re-review --baseline`.**

| 427 bullet | What 427 leaves to prose | What diffgate makes mechanical |
|---|---|---|
| 1 Mode | The coordinator must pass both flags and keep a saved copy; dropping them silently starts a fresh first review | `begin` snapshots each review itself; the variant refuses critique without `--diffgate-dir`; `--expect-round` catches a fresh or wrong directory |
| 2 Grading | The reviewer grades and decides what blocks | Blocking is derived from checkable fields; carried severity is pinned |
| 3 Verdict | The reviewer writes the last line | The script prints it; the reviewer writes none |
| 4 Cap | `review: N of 3` copied from the prior header | Ledger count; `begin` exits 4 at the cap; the cap is a constant |
| 5 Re-review output | The reviewer finds changed lines (ignoring whitespace) and self-tags `origin=` | Line plus token diff, hunk ids, reflow filter, anchor read-back, computed `origin`; `resolved` needs a hunk; an empty surface keeps every prior blocker open |
| 6 Reviser contract | "Revise only text a blocking finding names" | Every changed hunk needs a blocking owner in the fix map; the reviser's task list is script-written and has no minors |
| 7 Precedence | A brief may not widen scope | The script ignores the brief; scope is the surface |

What stays prose, with its residual risk: whether a finding is true and its severity label right; whether a `resolved by=` hunk really fixes the finding; whether a `via` dependency is real; whether a reviser's id on an edit is honest (the next review sees every such hunk once); and whether the coordinator uses the variant and one directory at all (caught by `--expect-round` and the experiment's validity rules, not by the script).

## 3. Exact changes

Every file, subcommand, flag and test below is PROPOSED; existing files are cited with the line read in this worktree on 2026-11-08. `/sc:spec-panel` (`src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`), `src/superclaude/core/HOW-WE-WORK.md`, `WORKER-CONTRACT.md` and the installer are not edited. Delivery in two stages: Stage A (inert: skill, script, script tests) and Stage B (the variant command and its tests). Folding diffgate into `/sc:spec-panel` (Stage C) is a later, separate decision taken on the S1 result class (section 5), never on the bar alone.

**3.1 `src/superclaude/commands/spec-panel-diffgate.md` (new).** A copy of `src/superclaude/commands/spec-panel.md` (486 lines) with `/sc:spec-panel` renamed to `/sc:spec-panel-diffgate` and only these edits:
1. Frontmatter `name: spec-panel-diffgate`; `description:` gains "with a computed re-review surface (diffgate variant)". Title (line 10): `# /sc:spec-panel-diffgate - Expert Specification Review Panel (diffgate variant)`.
2. Usage line 22: replace `[--re-review <prior-findings-file> --baseline <saved-copy>]` with `[--diffgate-dir <dir> [--expect-round N]]`.
3. `## Tool Coordination` (heading line 218; the `**Read**` bullet on line 220): keep the bullet as `- **Read**: Specification content analysis and parsing` and delete only its clause that names `src/superclaude/examples/release-spec-template.md`, with no replacement path, because an installed primitive may not name a `src/superclaude/` path (project CLAUDE.md rule).
4. `## Review Loop` (line 256): bullets 2 and 7 keep 427's text with the small additions shown; bullets 1, 3, 4, 5 and 6 are replaced. Each bullet is ONE physical line (wrapped here only by the viewer):

```markdown
1. **Mode**: `--diffgate-dir <dir>` applies to `--mode critique` only and is required there, except under `--unattended`, where it defaults to `<report-dir>/diffgate`; the script's `begin` step decides the review: an empty directory makes this review 1 of the full document, any later `begin` makes it a re-review of the computed surface; `--re-review` and `--baseline` are not accepted; a non-zero exit of the script stops the run with the script's message, except where `## Diffgate` names the next step (`check` exit 1: one repair and one rerun; `begin` exit 5: run the step `status` names), and the run never falls back to a first review.
2. **Grading**: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor; minor findings are notes and never trigger a revision; the script derives blocking from each `FINDING` line (`sev=critical`, `fr=8` or `fr=9`, or `sev=major` with an `outcome` other than `-`) and the reviewer never writes it.
3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open), copied from the `verdict_line` that the script's `check` step prints; the reviewer never composes its own, and the deferred list, the scoped-PASS line and the Reviser brief all sit above it.
4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the review number `begin` prints; a `begin` that exits 4 means do not review, HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--diffgate-dir` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps only the directory; the ledger keeps the count.
5. **Re-review output**: read `surface-r<N>.md` and treat the specification as read-only context that cannot widen what may be reviewed; write one `PRIOR` line per prior blocking finding, `resolved by=<hunk>`, `open quote="..."`, `regressed by=<hunk> quote="..."` (`regressed` = a finding the prior report marked resolved that fails again), the 427 vocabulary `resolved|open|regressed`, or in addition `withdrawn quote="..." reason="..."` (only for an id the reviser declined); anchor each new finding by a quote on a changed token of a listed hunk, or by `via=<hunk>` for an unchanged line that a listed hunk breaks (at most 2), or attach it to a prior id with `cites=`; the script computes `origin=changed|unchanged` and records any other finding as `deferred: pre-existing`, never blocking; FR-8 to FR-10 and the Guard Condition Boundary Table cover guards inside the surface hunks only; an empty surface leaves every prior blocking finding open and still counts as a review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line that names `reviser-brief-r<N>.md` (blocking finding ids only) and restates this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; write `fixmap-r<N>.txt` with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's `fixcheck` until it exits 0; each added paragraph or table cites its finding id; the reviser reports the byte size before and after, which `fixcheck` prints; the next review refuses to open while any hunk maps to no listed finding.
7. **Precedence**: a brief may narrow this scope; it may not widen it past the surface hunks and the prior blocking findings, and may not grade a minor finding as blocking; an instruction to apply all confirmed findings cannot authorize an edit to a minor finding.
```

5. New section `## Diffgate`, between `## Review Loop` and `## Output Formats`, one physical line per item:

```markdown
## Diffgate

1. **Script**: run `uv run --no-project python "<diffgate base>/scripts/diffgate.py" <subcommand> ...`, where `<diffgate base>` is `~/.claude/skills/sc-diffgate` if it exists, else the project `.claude/skills/sc-diffgate` copy; if neither exists, stop with `E-DIFFGATE-MISSING` and never run a plain review; the script writes only inside `--diffgate-dir`, never the specification; under `--unattended` the directory defaults to `<report-dir>/diffgate`.
2. **Begin**: before reading the specification run `begin --dir <dir> --doc <file> [--expect-round N]` and read its JSON; exit 1 lists unmapped fix hunks (send them back to the reviser, do not review); exit 4 means the loop is closed (`halt: pass`, `halt: escalate` or `halt: invalid`); exit 5 means a step was skipped (run the step `status` names); exit 3 names a missing or empty input; exit 6 means the ledger is corrupt or was edited by hand (stop and escalate).
3. **Review surface**: in a re-review read the `surface` file `begin` names and review only it; findings anchor only as Review Loop bullet 5 says.
4. **Finding lines**: end the findings with a `## Diffgate findings` block exactly as `~/.claude/skills/sc-diffgate/SKILL.md` defines it (`PRIOR`, `FINDING`, or the single line `FINDINGS none`), with values in double quotes as JSON strings (`anchor="..."`, and for a blocking `major` an `outcome="..."`), and write no `verdict:` line.
5. **Check**: run `check --dir <dir> --report <report>` last; on exit 1 repair only the lines `reject-r<N>.txt` names and run it once more; the script's `verdict_line` is the verdict and becomes the report's last line.
6. **Close**: at a derived PASS or at `review: 3`, write above the Reviser brief and the verdict line the open blocking findings with their fix chains, `## Deferred (pre-existing, not looped on)` with the whole `deferred.md` once, and the `scoped PASS:` line when `check` reports `acceptance: scoped`; a FAIL at review 3 says `halt: escalate`.
```

6. `## Unattended mode` (line 451): byte-identical apart from the command name.

**3.2 `src/superclaude/skills/sc-diffgate/SKILL.md` (new).** Infrastructure skill, delegate-only, no slash command, frontmatter `name: sc-diffgate`, `allowed-tools: Read, Bash`. About 60 lines: call form, subcommands and their JSON fields, exit codes, the finding grammar, file formats, the `PROFILES` extension point. Named `sc-diffgate`, not after the command: `install_skills.py` (`_has_corresponding_command`, line 40) strips `sc-` and skips, then deletes, a skill whose name matches an existing command file that does not activate it, so `sc-spec-panel-diffgate` would never install. SKILL.md carries these two definitions verbatim:

Subcommands (each prints one JSON object with `ok`, `exit`, `message`, `review` plus the fields shown):

| Subcommand | Writes | Extra stdout fields |
|---|---|---|
| `begin --dir D --doc F [--expect-round N]` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N of 2 or more); for N of 2 or more it first re-runs the fix-map check against `doc-r<N-1>.md` and the current spec, and any unmapped hunk exits 1 with the unmapped list and opens nothing | `surface`, `hunks`, `ignored`, `coverage`, `priors` |
| `check --dir D --report R` | `result-r<N>.json`, `reviser-brief-r<N>.md`, `deferred.md`; or `reject-r<N>.txt` | `accepted`, `verdict`, `verdict_line`, `acceptance` (`clean` or `scoped`), `blocking`, `deferred`, `degraded`, `halt` |
| `fixcheck --dir D --doc F [--map M]` | ledger fix record; pre-fills map candidates from inline `R<N>.<j>` tags; exits 1 when the map's `doc_sha` line differs from the spec; the third failure in one cycle records `fix-rejected` | `hunks`, `mapped`, `declined`, `withdrawn` candidates, `bytes_by_id`, `hunks_by_id`, `unmapped` |
| `status --dir D` | nothing | `state` (`open`, `checked`, `fixed`, `closed`, `invalid`), `next` (the one command that should run next) |

Exit codes: 0 done (includes an accepted review whose verdict is FAIL); 1 input rejected (`check`: bad report; `fixcheck` or `begin`: unmapped or unknown hunks); 2 usage error or an input over the limits; 3 an input file missing, unreadable or empty; 4 loop closed (`halt: pass`, `halt: escalate`, `halt: invalid`); 5 steps out of order (no accepted check or fix map for the current spec hash, spec edited during a review, or `--expect-round` differs); 6 ledger corrupt or disagreeing with the replay of the recorded report.

Report block, under the heading `## Diffgate findings`, one line per item, keyword at column 1:

```text
PRIOR R1.5 resolved by=H2.2
PRIOR R1.9 open quote="still lets WC-7 skip the command file"
PRIOR R1.7 withdrawn quote="..." reason="declined in fixmap-r1.txt: the cited rule does not exist"
FINDING R2.1 sev=major at=60-63 hunk=H2.2 anchor="appears in that worker's worker-read output" outcome="correct launcher runs are recorded as WC-1 not exercised" :: AC-0.4 reads the wrong source
FINDING R2.2 sev=major at=312 via=H2.3 via_quote="7.2 step 1 --worktree current" anchor="places the worker in the current worktree" outcome="..." :: H2.3 now assumes an own worktree
FINDING R2.3 sev=minor at=140 cites=R1.9 anchor="..." :: more evidence for R1.9
```

Line forms: `PRIOR <id> resolved by=H<k>.<n>`; `PRIOR <id> open quote="..."`; `PRIOR <id> regressed by=H<k>.<n> quote="..."`; `PRIOR <id> withdrawn quote="..." reason="..."`; `FINDING <id> sev=<critical|major|minor> at=<line or a-b> hunk=H<k>.<n> anchor="..." [outcome="..."] :: text`, with optional `via=H<k>.<n> via_quote="..."`, `cites=<id>`, `fr=8|9|10` and `side=old` (a finding that anchors through `via=` or `cites=` omits `hunk=`); or the single line `FINDINGS none`. Quoted values are JSON strings (`json.loads` on the token). `at=` refers to lines of `doc-r<N>.md`, 1-based and inclusive. Finding ids are `R<N>.<j>`, `j` from 1 with no gap. The reviewer writes no `verdict:` line.

**3.3 `src/superclaude/skills/sc-diffgate/scripts/diffgate.py` (new, about 420 lines, stdlib only).** Outline:

```python
CAP_REVIEWS = 3; MERGE_GAP = 2; VIA_CAP = 2; FORMAT = "diffgate/1"   # cap is a constant, never a flag
PROFILES = {"spec-panel": {"sev": ("critical", "major", "minor"), "blocking": _spec_panel_blocking}}
EXIT_OK, EXIT_REJECT, EXIT_USAGE, EXIT_INPUT, EXIT_CLOSED, EXIT_ORDER, EXIT_LEDGER = 0, 1, 2, 3, 4, 5, 6
LIMITS: 2 MiB per document, 100,000 lines, 1,000 machine lines per report (exit 2 before the diff)

def read_text(path) -> str                       # UTF-8 strict; exit 3 names a missing or empty file
def tokens(lines) -> list[Token]                 # (text, line, start, end) per whitespace token
def build_hunks(old, new, review) -> (hunks, ignored)   # line pass + token pass; reflow filter; structural flag; ids H<k>.<n>
def render_surface(review, hunks, priors) -> str
def parse_report(text) -> Parsed                 # PRIOR / FINDING / FINDINGS none; json.loads on quoted values
def check_report(parsed, ledger, snapshot, hunks) -> (result, errors)   # rules C1-C12 below
def derive(parsed, profile, priors) -> Outcome   # blocking, origin, statuses, verdict, acceptance clean|scoped
def check_fixmap(map, hunks, open_blocking, doc_sha) -> (accepted, unmapped)   # rules M1-M3
def replay(ledger) -> None                       # re-run check on the recorded report; exit 6 on mismatch
def load_ledger(d) / save_ledger(d, data)        # exclusive-create lock file; temp file + os.replace; refuse symlinks
def cmd_begin / cmd_check / cmd_fixcheck / cmd_status
def main(argv) -> int                            # one JSON object on stdout
```

Checker rules (hard = exit 1 with `reject-r<N>.txt`): C1 the `review: N of 3` line equals the ledger review, and the block has `FINDING` lines or `FINDINGS none`; C2 every line parses, ids are `R<N>.<j>`, contiguous; C2b every `R<N>.<j>` token in the prose is a `FINDING` id; C3 the spec hash equals the one `begin` recorded (on a mismatch `check` exits 5, steps out of order, and writes no `reject-r<N>.txt`, because a report repair cannot fix an edited spec); C4 `at=` lies inside the snapshot; C5 the whitespace-collapsed anchor (12 to 200 characters) occurs on the `at=` lines of the named side; C6 from review 2, a `hunk=` finding's anchor occurrence overlaps a changed token of that hunk (or a removed token with `side=old`); a `via=` finding's `via_quote` overlaps a changed token of the `via` hunk and its anchor sits on the unchanged line `at=` names; every anchor and `via_quote` in a line is checked; C7 `via` names a hunk and its quote overlaps a changed token, at most 2 per review (a third is deferred with `reason=via-cap`); C8 `cites=` names a prior blocking id; C9 the `PRIOR` lines are exactly the ledger's prior blocking ids, once each, `withdrawn` only after a `declined` map line; C10 `resolved` carries `by=` a hunk of this surface. Soft (recorded in `result-r<N>.json`): C11 scope and deferral; C12 blocking derivation. Fix-map rules: M1 every hunk is owned by one or more open blocking ids of the review (several ids per hunk allowed); M2 every blocking id has a hunk or a `declined` line; M3 ids and hunks exist, the `doc_sha` line matches the spec.

**3.4 Tests.**
| File | Status | Content |
|---|---|---|
| `tests/skills/test_diffgate_script.py` | new | Loads the script with `importlib.util.spec_from_file_location` (pattern of `tests/skills/test_workflow_archive.py:22-28`) and runs it as a subprocess for exit codes. Cases: whitespace-only and reflow change give no hunk; a list-merge reflow gives a `structural` hunk; one changed word in a 300-character line gives one hunk whose changed span is that word; pure deletion gives a `side=old` anchorable hunk; merge gap 2 versus 3; a 320-line input keeps an exact diff (`autojunk=False`); `begin` review 1 writes a snapshot and no surface; `begin` review 2 without an accepted fix map exits 5 and with an unmapped hunk exits 1; spec edited after `fixcheck` exits 5; fourth review and review after PASS exit 4; wrong `--expect-round` exits 5; a valid report is accepted; anchor not on the cited lines; quote present in both changed and unchanged text cited on the unchanged occurrence; fabricated hunk; neither hunk nor prior id is deferred and never blocking even at `sev=critical`; `cites` adds no blocker; third `via` deferred; missing `PRIOR` line; `resolved` without `by=`; `withdrawn` legal only after `declined`; major with `outcome="-"` is minor; prose id missing from the block is structural; a second structural failure sets `invalid`; second failing submission degrades; `FINDINGS none`; two-owner hunk; map with a stale `doc_sha`; third failing `fixcheck` records `fix-rejected`; hand-edited ledger exits 6 on replay; the spec's hash is unchanged by every subcommand; the flg-r1-shaped fixture (four mapped blocking fixes with four new blockers on them, one MAJOR graded minor on a shared line, one minor-only fix): all four fix hunks allowed, the minor-only hunk rejected, chains of length 3, label proxy 5, blocking 4. |
| `tests/skills/fixtures/diffgate/` | new | Small synthetic v1, v2, v3 documents and good, bad-anchor, unanchored, structural-failure and degraded reports; the flg-r1-shaped fixture. |
| `tests/skills/test_spec_panel_diffgate_command.py` | new | Frontmatter name; Usage names `--diffgate-dir` and not `--re-review`; the seven Review Loop bullets in order, one line each; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` imported from `tests/skills/test_review_severity_rule.py` are present; `## Diffgate` sits between `## Review Loop` and `## Output Formats` and names `~/.claude/skills/sc-diffgate` before `.claude/skills/sc-diffgate`; no `src/superclaude` string anywhere in the command or the skill folder; drift guard: every other `## ` section equals `spec-panel.md`'s after the name swap, `## Tool Coordination` equal after removing the clause that names `src/superclaude/examples/release-spec-template.md` from its `**Read**` bullet; `spec-panel.md` still carries its 427 Usage flags (guards "additive"); an isolated temporary-HOME install of the command and `sc-diffgate` runs `diffgate.py --help` outside the repository and leaves a sentinel `spec-panel.md` byte-unchanged. |
| `tests/skills/test_worker_contract.py` | edit | `_check_no_unattended_sections` (line 831) asserts `set(have) == set(UNATTENDED_COMMANDS)` (line 837), which the copied `## Unattended mode` heading breaks. Add `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}`, compare against `set(UNATTENDED_COMMANDS) | set(UNATTENDED_VARIANTS)`, and add a parametrized test that `_unattended_section(variant)` (line 853) equals the parent's after the name swap. `assert len(expect) == 31` (line 1564) is untouched. |
| `tests/recommend/test_routing_refresh.py` | edit, 1 line | Line 33 becomes `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-diffgate"}`; line 648 asserts shipped commands minus this set equal the frozen inventory. |

Kept green without edit: `tests/skills/test_review_severity_rule.py` (scans the new files under `src/`; the text keeps the canonical cap, avoids its banned any-severity phrases, and must not describe the `fixcheck` retry limit with a digit pattern its `CAP_REGRESSION` matcher catches, such as "up to 3 fix attempts": write "three failing `fixcheck` runs in one fix cycle"), `tests/skills/test_spec_panel_review_loop.py` (parametrized over the two `spec-panel.md` copies only), `tests/unit/test_cli_install.py` (`_assert_present`, line 501, is a presence check), `tests/commands/test_routing_plugin_parity.py` (mirrors only README-listed commands).

**3.5 Docs and sync.** New `docs/designs/spec-panel-diffgate.md`: this SPEC trimmed to decisions, formats, residual risks and the measurement plan. No plugin mirror (the plugin tree mirrors only README-listed commands). No `HOW-WE-WORK.md` row until promotion. `make sync-dev` copies the command and the skill folder into `.claude/`, which is never staged; `make verify-sync` must pass. Before commit, `grep -rn 'src/superclaude' src/superclaude/commands/spec-panel-diffgate.md src/superclaude/skills/sc-diffgate` prints nothing.

**3.6 Later adopters.** The script reads text and a `PROFILES` entry; nothing else knows which reviewer wrote the report. rf-qa agents are the closest fit (an `rf-qa` profile, CRITICAL and IMPORTANT blocking; must not weaken rf-qa's own regression and monotonicity guards). `/sc:reflect` needs a multi-file surface (hunk ids prefixed by path, a git-tree baseline) and applies only to a repair re-review, never to its first audit. The `/sc:implement` final review already has the stronger parent-checked model (`refs/qa.md`) and must not be replaced; at most it could reuse the anchor and hunk code. All of these wait for the S1 result.

## 4. Variant command name and install note

**Name:** `/sc:spec-panel-diffgate` (file `spec-panel-diffgate.md`), with its script in the infrastructure skill `sc-diffgate`. It installs next to `/sc:spec-panel` and replaces nothing.

**Install for an experiment** (adds two things, edits nothing; never `superclaude install --force`, which rewrites every command file, `spec-panel.md` included):

```bash
sha256sum ~/.claude/commands/sc/spec-panel.md              # record; must be unchanged after every step
cp src/superclaude/commands/spec-panel-diffgate.md ~/.claude/commands/sc/spec-panel-diffgate.md
mkdir -p ~/.claude/skills/sc-diffgate && cp -R src/superclaude/skills/sc-diffgate/. ~/.claude/skills/sc-diffgate/
sha256sum ~/.claude/commands/sc/spec-panel-diffgate.md ~/.claude/skills/sc-diffgate/scripts/diffgate.py   # record in the run log
```

`superclaude install-skill sc-diffgate` also exists (`src/superclaude/cli/main.py` line 444), but `cp` is explicit and cannot touch `spec-panel.md`. Workers load commands from `~/.claude/commands/sc/` (decision D9 in `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/DECISIONS.md`), so a worktree-only copy is inert.

**The one-line substitution in every review brief (reviews 1, 2 and 3):**

```text
/sc:spec-panel <args>   ->   /sc:spec-panel-diffgate <args> --diffgate-dir <one directory per replicate> --expect-round <N>
```

Any `--re-review ... --baseline ...` in a brief is removed (the variant refuses them). The worker must invoke the command through the Skill tool, and its transcript must show the call (rule WC-7 of `~/.claude/WORKER-CONTRACT.md`: reading the command file and following it from memory does not count).

**The one line the reviser briefs gain (both fix cycles):**

```text
Your task list is <DIR>/reviser-brief-r<N>.md, not the whole report; after editing, run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py fixcheck --dir <DIR> --doc <spec>`, confirm or decline each line of <DIR>/fixmap-r<N>.txt, and repeat until it exits 0.
```

These brief lines are part of the treatment: they are prose that could act on their own (all three debate advocates rejected the assumption that they do not), so the experiment claims the combined treatment, publishes the exact before and after text of every changed brief line in its run log, and does not claim "mechanical beats prose" without a briefs-only arm (section 5).

## 5. Measurement plan and predicted numbers

**Design.** S1 exactly as in AB-REPORT.md and ARMB-REPORT.md: the Orca worker-contract spec (57,763 bytes), base commit 2cb683f5, model claude-opus-5-5, three reviews and two fix cycles, the same verbatim briefs with only the section 4 substitutions, `WORKER-CONTRACT.md` moved aside, two replicates (`dg-r1`, `dg-r2`) in fresh worktrees. Comparators are the existing control (`ctl-r1`, `ctl-r2`) and Arm B (`flg-r1`, `flg-r2`), not run at the same time (stated limitation). The treatment is the script plus the published brief diff.

**Pre-run gate (before any replicate).** (1) A worker in the experiment's permission mode runs `diffgate.py status` through the installed path with no permission prompt. (2) The reviewer and reviser of a replicate run in one checkout and pass the same `--doc` real path, checked by a dry `begin` and `status`. (3) A worker resolves `/sc:spec-panel-diffgate` after a restart. (4) Hashes recorded as in section 4.

**Metrics (one counting function for every arm, fixed before the run).**
- `R3-proxy-all` (the bar metric): CRITICAL or MAJOR labels on (a) findings first raised in review 3, deferred, demoted and over-`via`-cap findings included, and (b) prior blocking findings marked `open`, `regressed` or `withdrawn` in review 3, at their recorded label; each id counted once within review 3. The control and Arm B are recomputed with this function and published beside their historical values before any treatment replicate is scored. Arm B stays 6 and 1 under it (every prior blocker was `resolved` at review 3 in both replicates); the control is to be recomputed.
- Reported beside it, never instead of it: the script's blocking count and the 427-grade blocking count (in flg-r1, 2 of the 6 proxy items were MAJOR labels graded minor).
- Growth: bytes of the spec after fix cycle 2 against 57,763. An early PASS carries its document forward to the endpoint without an extra fix.
- Recorded per review: rejects and repair turns, `degraded`, deferred count and labels, `via` use, hunks and changed tokens per surface, fix hunks mapped, declined and rejected, `fixcheck` runs per cycle, chains and their lengths, tool calls, sessions and wall time per step.
- Ancestry of every review-3 critical+major finding (blocking, deferred and demoted alike): on a blocking-fix hunk, on a minor or unmapped edit, or on unchanged text, from the ledger owners (and, for control and Arm B, from their disposition changed-line lists, as in `evidence-flg-r1.md`). In the treatment every blocking new finding sits on a mapped fix hunk by construction, so the blocking-only share is 100% and is not a diagnostic.
- Blindness audit, mandatory for every arm: after the loop, one fresh `/sc:spec-panel --mode critique` review 1 of the final document in a new session with no ledger. Each blocker it finds is classified as fix-written text the loop closed (what diffgate hides) or text present since the original.

**Predicted numbers (debate consensus, refined by the flg-r1 evidence).**

| Metric | Control mean | Arm B | Bar | Prediction |
|---|---|---|---|---|
| R3 critical+major (`R3-proxy-all`) | 6.0 | 6 and 1 (mean 3.5) | 3 or fewer in BOTH replicates, or a clean PASS sooner | **mean about 3.0 to 3.5**: a flg-r1-like replicate about 4 to 5 (its 4 blockers sit on blocking-fix text and survive; only R3-7, on a minor fix, disappears; R3-8's MAJOR label sits on a line blocking fixes also wrote), a flg-r2-like replicate about 1 to 2 (the F22 to N5 to N12 chain started on a minor fix and may never exist). P(both replicates 3 or fewer) about **0.2 to 0.25** |
| Growth after two fix cycles | 63.5% | 27.8% and 32.1% (mean 30.0%) | 44.4% or less | **about 20% to 27%**: minor and "related defect" edits are refused (in flg-r2 about half of the 25 lines the round-2 fix changed carried no blocking id; in flg-r1 10 of the 14 applied round-2 rows were non-blocking). P(both at or under the bar) about **0.9** |
| Clean PASS by review 3 | 0 of 6 runs | 0 | alternative to the count bar | about 10% per replicate |
| F1 ("wrong lever") fires in at least one replicate | | | | about 0.5 to 0.55 |

**Expected verdict on the pre-registered bar: likely NOT met on the review-3 count, likely met on growth.** No part of the diffgate theme (computed surface, anchor checker, fix gate, ledger) lowers the number of blockers that fixes of blocking findings introduce, without relabelling or hiding them; all three debate advocates checked each part against flg-r1 and agreed. The experiment's most likely product is a measured per-blocking-fix defect rate under scope control: a clean record of where the remaining blockers come from, not convergence.

**Result classes (pre-registered; S1 at n=2 returns exactly one):**
1. **Bar met:** both replicates at 3 or fewer (or a clean PASS sooner) and growth at or under 44.4%, with no failure condition in section 6.
2. **Bar missed, F1 fires:** a replicate is above 3 and at least 70% of its review-3 critical+major findings sit on blocking-fix hunks by ancestry. The scope and fix gates worked; the driver is fix quality, which needs a different lever.
3. **Bar missed, F1 does not fire:** the mechanism itself did not do what it claims (or the deferred and unchanged-text share is large), which is the stronger negative.

The spread check (effect larger than the larger within-arm spread, 4 for the control) is reported; it can be met only if the treatment mean is below 2.0, so at n=2 it is not expected to be met, and any claim of a proven effect needs a replicate count fixed before the first run. A "mechanical beats prose" claim additionally needs a briefs-only arm: the same brief lines, the plain `/sc:spec-panel` command, no script.

**Validity.** Attempt slots are fixed in advance (two per arm). A replicate is valid only if the ledger shows an accepted `check` for every review the loop ran (reviews 1 to 3, or up to the review that reached a derived PASS) and an accepted `fixcheck` for every fix cycle that ran, the installed hashes did not change, and no worker read `origin/master` (ctl-r2 did in every step and flg-r1 in 7 Bash calls, so peeks are recorded for every arm). Report the completion rate per arm. A replicate is void, reported with its cost and never silently replaced, when its transcript and ledger disagree, its directory or run changes mid-loop, the ledger was hand-edited (replay exit 6), plain `/sc:spec-panel` ran, the installed hashes changed, or it ended `invalid`. Review 1 now also writes a machine block, so its comparability is checked: a valid replicate whose review-1 critical+major proxy falls outside 9 to 17 (the range across all six earlier runs: control 11 and 12, 427 9 and 9, Arm B 16 and 17) is scored but labelled "review 1 not comparable" and cannot be credited to the mechanism. This is a deliberate change from the merged design, which used "review-1 blocker count outside 13 to 17": that range came from a proposal's unverified estimate, while flg-r1's review 1 had 11 blockers (`disposition.md` line 39), so the merged rule would have marked a real Arm B run "not comparable".

## 6. Risks, costs and what would falsify it

**Costs per loop (estimates, UNVERIFIED until the step times are recorded).**

| Item | Added |
|---|---|
| Reviewer tool calls | 3 per review (`begin`, read the surface, `check`), plus 1 repair turn and 1 `check` per rejected report: about 9 to 12 per loop |
| Reviser tool calls | read the brief, confirm the pre-filled map, 1 to 3 `fixcheck` runs: about 4 to 6 per fix cycle |
| Sessions in the loop | none on the normal path (rejects are repaired in the same session); a structural stop costs one re-dispatched review; `fix-rejected` or `invalid` ends the loop and escalates |
| Sessions for measurement | one blindness-audit review per replicate, for every arm |
| Wall time | about 3 to 8 extra minutes per loop at 10 to 15 seconds per tool round trip, partly offset by reviews 2 and 3 no longer re-reading the whole document and the prior report (flg-r2's review 3 spent 15 status rows and 20 citation groups before its new findings) |
| Build and upkeep | about 420 lines of stdlib script, a 60-line `SKILL.md`, about 35 script tests, a 490-line command copy that can drift from `spec-panel.md` (pinned by the drift-guard test), two one-place edits to existing tests |

**Ways it could make the loop worse.**

| Risk | How | Limit | Residual |
|---|---|---|---|
| Blind to a real regression | A defect in fix-k text that review k+1 misses is never re-opened (one look per change). | The blindness audit measures it; deferred items are listed. | Real; it is the price of a bounded loop. |
| Action at a distance | A fix to line A makes unchanged line B wrong. | `via=` with a checked quote of A, at most 2 per review; A's changed words remain anchorable. | A reviewer that does not think of `via`; a third `via` is deferred. |
| Scoped PASS with a known serious defect | A real blocker review 1 missed lands in `deferred: pre-existing`. | Shown once with its label; `acceptance: scoped`; counted in `R3-proxy-all`. | The loop can end on PASS with a critical defect in the deferred list; unfit for a release gate that must block on every discovered defect. |
| Anchor gaming | A quote that straddles a changed word to attack the sentence around it. | C6 needs overlap with a changed token at the cited line; 12-character minimum. | Semantic fit of finding to anchor is not checked. |
| Reviser id gaming | A valid blocking id on an unrelated edit passes `fixcheck`. | Every such hunk is surfaced to the next review with its claimed owner; bytes and hunks per id are printed. | The edit is reviewed once, so gaming adds surface, not hidden text. |
| Under-fixing | A strict gate pushes revisers to `declined`; a declined real blocker stays `open`. | `withdrawn` only after `declined`, counted in the proxy, forces `scoped`. | Counts move from "new" to "open"; the proxy sees both. |
| Fail-closed stalls | `uv run` blocked by a permission prompt, a script bug, a missing install, a wrong directory. | Pre-run gate; every stop names its reason; no silent fallback to a plain review. | A stall costs a replicate (recorded as a failed attempt). |
| Format tax on reviewers | The machine block and anchors are new work; review-1 behaviour may shift. | One repair turn, then degrade; review-1 comparability label. | Measured, not prevented. |
| Diff noise | A rewrite touching most of the file turns the surface back into the whole document; moved blocks show as delete plus insert. | `coverage:` printed, with a warning above 50%. | No move detection in v1. |

**What would falsify it (any one, declared before the run).**
1. **F1, wrong lever:** a replicate has `R3-proxy-all` above 3 and at least 70% of its review-3 critical+major findings (blocking, deferred and demoted) sit on blocking-fix hunks by ledger ancestry. Diffgate worked as designed and did not move the count; the driver is the per-fix defect rate. Predicted about 0.5 to 0.55.
2. **F2, no growth win beyond 427:** growth above 44.4%, or mean growth not below Arm B's 30.0%: the fix gate did not constrain the reviser.
3. **F3, blinding:** the blindness audit finds 2 or more blockers in fix-written text the loop closed, in either replicate.
4. **F4, too heavy:** in either replicate more than one review needs a second `check` run or ends `degraded: yes`, or a loop stalls on a script error: the grammar costs more than it returns.
5. **F5, demotion:** more than a quarter of new findings in reviews 2 and 3 are demoted or degraded, or `fixcheck` fails more than once per fix cycle on average.
6. **F6, stall:** a replicate stalls before review 3 without a derived PASS.
Only F1 to F6 absent together, with both replicates at 3 or fewer, count as success. The label proxy and the 427-blocking count are reported side by side. Reported but not part of the pre-registered rule: a `R3-proxy-all` mean of 3.5 or higher means no gain over Arm B on the count. A mixed result (growth met, count missed) is reported as such, never rounded up to a pass.

## 7. Open questions

Each has the default S1 uses, so none blocks the first experiment.

1. **Can an Orca worker run `uv run --no-project python ~/.claude/skills/...` without a permission prompt?** UNVERIFIED; decides whether the unattended path works at all. Default: settled by the pre-run gate (section 5) before any replicate.
2. **Who runs the script?** Default: the reviewer and the reviser at fixed points, with locks (each step's output is the next step's only input) and `begin` re-running the fix check. Alternative: the coordinator runs every step, so the reviewer cannot touch the ledger; cleaner separation, one more coordinator step per review. Decide after S1 shows how often a step was skipped.
3. **Second structural reject: degrade or stop?** Default: finding-level failures degrade after one repair; structural failures stop, with one more attempt on the same snapshot, then `invalid`.
4. **Is `VIA_CAP = 2` right?** Uncalibrated. Default 2; record every `via` use and every over-cap deferral.
5. **Should a deferred CRITICAL force escalation instead of a scoped PASS?** Default: no (never blocking after review 1), disclosed and counted; revisit if the blindness audit or the deferred list shows serious misses.
6. **Is the 12-character anchor minimum right for short table cells and identifiers?** Default 12; record rejects caused by it.
7. **Does the variant need a separate "minor sweep" after the loop for typo-class minors the reviser no longer touches?** Default: no; the deferred and minor lists go to the person, who decides outside the loop.
8. **Should the loop directory be staged like `.dev/tasks/`?** No repo rule covers it. Default: under the report directory for S1, not staged by workers.
9. **The lever this theme cannot reach.** If S1 lands in result class 2 (F1 fires), the next design must act on fix quality for blocking fixes (in flg-r1, 4 blocking fixes produced 4 new blockers). Combining diffgate with another team's reviser-side mechanism is the natural follow-up; diffgate's ledger then supplies the ancestry needed to measure it.
10. **Owner confirmation of the counting rule.** `R3-proxy-all` counts deferred, demoted and withdrawn critical+major findings. The owner should confirm this function, and the recomputed control values, before any run, so the result cannot be argued either way afterwards.
