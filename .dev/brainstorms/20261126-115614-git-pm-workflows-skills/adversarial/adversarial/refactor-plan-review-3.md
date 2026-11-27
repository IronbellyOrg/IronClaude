# Refactor Plan Review 3 (final, after fix cycle 2)

## Verdict

**PASS, with notes.** 0 BLOCKING findings, 10 MINOR.

- The four earlier BLOCKING findings (B-1, B-2, B-3, R2-B1) are fixed in the text of the planned changes, not only in the revision notes.
- The central commit path can be followed end to end, and every failure branch reaches a state the run can continue from.
- All 61 diff points are handled exactly once.
- The three HIGH resolutions and the 16 + 3 other rulings match Round 3.
- The seed constraints hold.

The MINOR findings are wording gaps, term edges and misplaced table cells. None of them changes a requirement, an outcome or a safety boundary. M3-1 (misnumbered acceptance observations) is the most visible and the cheapest to fix before the merge.

## Sources read

- In full: `refactor-plan.md` (686 lines, both revision notes), `refactor-plan-review.md`, `refactor-plan-review-2.md`, `blind/variant-A.md`, `base-selection.md`, `debate/scoring-matrix.md`, `invariant-probe.md`, `debate/round3-B.md`, `debate/round3-C.md` and `seed-brief.md`.
- In part: `debate/round3-A.md` (final position and the three HIGH sections) and `blind/variant-B.md` (Path notation, §2 RC-1..RC-7, §4.1, §13).
- Repository, read-only: `sc-implement-protocol/SKILL.md:36-151`, `refs/ledger.md` (header, re-review line, Resume and the per-task table), `refs/managed-workspace.md:44-95`, and `.pre-commit-config.yaml` (markdownlint excludes `.dev/.*`, line 97).

## Check 1: earlier BLOCKING findings and the central path

### 1a. Are the four fixes in the plan text?

| Finding | Where the fix is in the plan text | Result |
|---|---|---|
| B-1 (unflagged runs must load the settle/reconcile rules) | Change 21 (line 296): the ref loads when the flag is present or `commits.md` exists, and its "Reconcile and settle" part binds unflagged runs. Also FR-051 (line 329), NFR-018 (line 508), T-16 (line 519), AC-08 (line 531) and T-09 (line 296). | Fixed |
| B-2 (the trigger must fire for a newly due boundary) | FR-056's trigger bullet (line 330): "a boundary is due (FR-107 decides whether it is prepared or stops) or FR-107 allows a new attempt on a pending or refused one". FR-094's phrase is replaced on the same line. | Fixed |
| B-3 (the fetch contradiction) | §1.4 and FR-005 (line 458), T-12 (line 459), NFR-001 (line 456), FR-042's refusal text (line 469) and D4 (line 554) all say "never fetches on its own", with the one `submodule update` exception. FR-004's STOP on a `fetch` operation and the §3 "forbidden" row are about operations, so they stay consistent. | Fixed |
| R2-B1 (the commit set defined over "pending" tasks) | FR-062 bullet 1 (line 285) uses the anchor `complete` lines (FR-103) of the boundary's members. Bullet 2 (line 286) and the single definition of S (line 287) follow it. T-01's old "Pending set" cases move to T-19 (line 519). | Fixed |

A sweep of every "pending" in the plan finds only the FR-107 meaning. Two kinds of hit are not uses of the term:

- matches inside the word "appending";
- the base-text quotes that the edits replace.

### 1b. The central path, as the merged document would define it

**Wave 0 of a flagged run.**

1. FR-050 checks that the flag came from the person; FR-054's preflight runs between steps 5 and 6.
2. Step 6 opens the ledger.
3. FR-106 then runs in this order: the managed `PLAN:` and source check; any outstanding outside-S comparison (FR-113); the `run` line (FR-101, which creates `commits.md` on a first flagged run); reconcile; then steps 7-9 and task selection.

**One task.**

1. Q0 records `q0-head`, and the flag-only INV-002 rule records `q0-branch`.
2. Before Q7 flushes the first `complete`, the accepted tree is pinned (FR-073, FR-104).
3. FR-131 stops the Q7 cleanup from deleting the Q0 pin or the accepted pin while the boundary is unsettled.

**The boundary becomes due.** At Q8a:

- every writer has been joined (FR-057);
- every member's anchor lies in an `on` segment, so the boundary is eligible (FR-103);
- there is no prepared line and no settling line, so it is due (FR-105);
- no later `start` line exists and no task is open, so FR-107's "due, crash-explained" row says to prepare now.

**Prepare and commit (FR-061 steps 1-9).**

1. `stage-plan` computes S from the anchors plus the FR-076 package expansion, and runs the checks of FR-073..FR-075 and the branch check.
2. The message goes to a temporary file outside the work tree, and `check-message` validates it.
3. The prepared line is appended (FR-108).
4. `stage-plan --candidate` builds the frozen candidate tree, including the managed sidecar's prepared bytes, and the agent pins it.
5. The agent stages S and runs `git add -- .dev/tasks`.
6. The agent takes the worktree snapshot and pins it (FR-111).
7. The agent runs `git commit --only`, with the 600000 ms timeout.
8. `verify` applies the FR-108 predicate and the FR-113 comparison (FR-130).
9. The terminal line is appended.

After step 9:

- the `sha=` line settles the boundary;
- FR-131 releases the pins;
- the terminal line is not part of the commit and enters the next boundary commit (FR-100).

I checked that the candidate, the commit and the recovery predicate all use the same S. The new `run` line of a later invocation cannot disturb the predicate, because the candidate tree lives in an external ref (FR-106, FR-108).

**Failure branches.** Each one reaches a state the run can continue from:

| Branch | What happens |
|---|---|
| Hook failure | `hook-failed` → a `refused` line → STOP with the FR-121 choices; `abandon` is always offered. A later flagged run may make a new attempt as FR-107 allows. |
| Hook rewrite | `hook-rewrite` or `hook-rewrite-evidence` → the `rewritten/` pin and the refusal. Evidence-only rewrites are retried with fresh evidence. Product rewrites need restoration or a renewed review; see M3-9 for the gap there. |
| Hook rewrite that committed | `hook-rewrite-committed` → "refused with HEAD ≠ parent" → choices, including `adopt` when FR-123 holds. |
| Crash after `complete`, before the prepared line | Due and crash-explained: a flagged run prepares it; any other run STOPs `unsettled` with the choices; no pin is lost (FR-104, FR-131). |
| Crash after the prepared line, before the commit | Pending or uncertain, depending on whether the pins exist; see M3-2. Both fail safe. |
| Crash after the commit, before the terminal line | The FR-108 predicate gives `recovered` (settles) or `uncertain`. The comparison is taken before the new `run` line. See M3-3 for the missing table row. |
| Interrupted commit (timeout or exit above 128) | `E-RESUME-NEEDED reason=commit-interrupted`, with no terminal line (FR-116). |
| Uncertain | STOP `uncertain`; `abandon` is always offered, `adopt` only when FR-123 holds. |

**Terms.**

- "due", "prepared", "settled" and "unsettled" each have one meaning.
- "pending" has one meaning, apart from one overlap with "uncertain" (M3-2).
- "eligible" and "crash-explained" have edge uses (M3-4).
- "uncertain" is used for a state, a line form, a `verify` result and a `/sc:git` report outcome. These are consistent in spirit.

No step depends on a rule the plan removed: FR-055, FR-068, FR-069, the `dirty` reason, the old FR-065 and the `commit-failed` token. Stale base text that still names removed items sits only in Risk 2, NFR-002 and FR-033 (M3-8).

## Check 2: diff-point coverage (by reading and by a tally)

- I read every **Diff points** line and the "Changes NOT Being Made" table.
  - 51 ids are assigned to planned changes, each on exactly one change. No id repeats across the 39 change headings.
  - 10 ids are kept as base: S-001, S-004, S-012, C-001, C-002, X-002, X-003, X-009, X-011, X-012.
  - The two sets do not overlap, and their union is the 61 ids S-001..S-013, C-001..C-021, X-001..X-021 and A-001..A-006.
- A read-only tally script agreed.
- Changes 2, 5, 27, 38 and 39 carry no diff point, as their headings say.
- A-005 follows the Round 3 resolution, not the matrix's stale evidence text. That is correct for the reason review 1 gave.

## Check 3: the HIGH resolutions and the other 19 rulings against Round 3

**INV-001** (`round3-C.md` items 1-9) maps to:

| Round 3 item | Plan |
|---|---|
| 1 | FR-100, FR-101 |
| 2 | FR-102 |
| 3 | FR-103, plus FR-058 for batch membership |
| 4 | FR-104, FR-073, FR-131 |
| 5 | FR-105 |
| 6 | FR-106 |
| 7 | FR-107, FR-077 |
| 8 | FR-108 |
| 9 | FR-109 |

Details that match: the first-`complete` anchor, counting an unterminated tail, out-of-protocol, the `PLAN:` check before any recovery commit, and the outside-S comparison before the new `run` line.

**INV-021** items 1-9 map to FR-110..FR-118. Details that match:

- create-once sibling pins;
- the snapshot built from HEAD;
- `snapshot-unsupported`;
- `outside-unverified`;
- a stop after detected damage, even on a verified commit;
- 600000 ms;
- quiescence;
- the shared `/sc:git` scope.

**INV-027** items 1-7 map to FR-120..FR-126. Details that match:

- two distinct regexes and the full 64-hex key;
- a reply counts only after the disclosure;
- `abandon` is always offered;
- `basis=` and `differs=`;
- idempotent cleanup that keeps the outside-S pins.

**The 16 ACCEPT-FIX rulings** are all present and match their one-line requirements:

| Finding | Plan |
|---|---|
| INV-002 | FR-054 rule |
| INV-003 | FR-073 |
| INV-004 | FR-132 |
| INV-007 | FR-062 a/b |
| INV-008 | FR-062 c |
| INV-009 | FR-041 |
| INV-010 | FR-044 |
| INV-012 | FR-035 |
| INV-014 | FR-058 |
| INV-015 | FR-066 |
| INV-020 | FR-036 and FR-065 |
| INV-022 | FR-077 |
| INV-023 | Change 18 |
| INV-024 | FR-038 |
| INV-025 | FR-074 |
| INV-030 | FR-042(4) |

**The three ACCEPT-RISK residuals** are present:

- INV-011: FR-050 residual and Risk 17;
- INV-018: FR-076 and Risk 18;
- INV-029: Risk 2 and Risk 19.

## Check 4: seed constraints and names

All seed constraints hold:

| Constraint | Kept by |
|---|---|
| `/sc:git` never pushes, merges or opens a PR | FR-004, FR-005, D7, NFR-001 |
| No relay | FR-072's "never invokes `/sc:git` or `Skill sc:git-protocol`", D2 |
| PRs stay with `/sc:pr-submit` | §1.4 |
| Local branch cleanup by reuse only | FR-080, FR-081, FR-082 |
| No remote branch deletion | FR-081, AC-11 |
| No staging of `<dev>/` beyond `settings.json` | FR-013, FR-016, FR-031 (refusal with no staging hint), FR-033, FR-062 |
| `.dev/tasks` always staged | FR-061 step 5, FR-038 |
| No installed primitive names `src/<package>/` | FR-009, FR-019, NFR-010, AC-21 |

On names:

- A grep of the plan for model and vendor names (claude, anthropic, opus, sonnet, haiku, gpt, gemini, openai, codex, augment, aider, cline, cursor, copilot, superclaude) hits only the executor-only check on line 10.
- Change 3 removes the tool names from Variant B's RC-7, its only vendor or tool names (`variant-B.md:114-116`).
- D6's "Orca task" names the repository's own orchestration tool, the same wording `/sc:closeout` uses. It is not a model or vendor name in the sense of this check.

## Check 5: what fix cycle 2 introduced

- No new id was created, and no id collides with the base blocks. I checked every repeated bold id in the plan: each pair is one change's Target line plus its definition.
- No dangling reference. Every FR, NFR, T and AC reference resolves. FR-024..FR-029, FR-037 and FR-139 appear only inside ranges or as citations of Variant B or C ids.
- The cycle-2 text is consistent with its own fixes, with one gap introduced by the R2-M2 split (M3-6).

## Findings

### M3-1 (MINOR): the acceptance Observation cells use Variant B's numbering

**Evidence**

- Change 36 (line 530) gives:
  - AC-03 the plugin-parity `cmp` and `diff -r`;
  - AC-04 the `commands/` file count;
  - AC-05 `make verify-sync exits 0`.
- Those are Variant B's AC-03, AC-04 and AC-05 (`variant-B.md:510-512`).
- In the base:
  - AC-03 is the helper's verb list and allow-list (`variant-A.md:366`; the plan's own AC-03 text is in Change 6 item 7);
  - AC-04 is source, plugin and dev-copy sync plus the `sc-git.md` removal (`:367`);
  - AC-05 is the between-task commit criterion (`:368`).

**Consequence**

- The core commit criterion would carry an observation that does not test it.
- AC-03 would carry one that belongs to AC-04.
- Behaviour does not change, because the Check column keeps T-01, T-02 and T-09 for AC-05, and the plan says "a behavioural test outranks a text count".

**Suggested fix**

- Put the parity `cmp`/`diff -r` and `make verify-sync` under AC-04.
- Give AC-03 the `vcs.py --help` observation from Change 6 item 7.
- Give AC-05 a fixture observation adapted from Variant B's AC-09: two flagged tasks give two commits and two `commit sha=` lines in `commits.md`.

### M3-2 (MINOR): a prepared attempt without its pins and with HEAD = parent is both "pending" and "uncertain"

**Evidence**

- FR-107 (line 345): pending is "prepared, no terminal line, HEAD = parent".
- FR-108 (line 351): "HEAD equal to the parent is pending … Any other history, or incomplete proof (a prepared line without its pins), is `uncertain`".
- FR-111 (line 391): such an attempt "is never retried as if preparation had succeeded".
- A crash between FR-061 steps 3 and 6 produces exactly this state. The text is copied faithfully from `round3-C.md:35` and `:49`.

**Consequence**

The two readings give different outcomes:

- pending: a flagged run makes a new attempt;
- uncertain: the run stops and never retries; `adopt` is not available while HEAD = parent, so only `abandon` remains.

Both fail safe. T-22 expects only "at most one commit per key" for this crash point.

**Suggested fix**

Add to FR-108: "With HEAD = parent the attempt is pending whether or not its pins exist; a missing pin only forbids reusing that attempt, and the next attempt prepares anew with a new number. Incomplete proof is `uncertain` only when HEAD ≠ parent." Also state the expected result for each T-22 crash point.

### M3-3 (MINOR): the FR-107 state table has no row for the crash-after-commit state

**Evidence**

- No row of the table (lines 341-348) covers "prepared, no terminal line, HEAD ≠ parent".
- Its handling comes only from FR-108 ("or `recovered` on a later run").
- The pending row's "Any other run" cell says "may record a proved existing commit as `recovered`", which cannot apply while HEAD = parent.

**Consequence:** the most common recovery case is defined outside the table that is meant to cover every state. FR-109, T-22 and AC-16 still pin the behaviour.

**Suggested fix:** add the row "prepared, no terminal line, HEAD ≠ parent: apply FR-108; if proved, append `recovered` (both columns; settles); otherwise `uncertain`", and move the "may record … `recovered`" clause there.

### M3-4 (MINOR): three term edges

**Evidence**

- **(a) "crash-explained".** FR-105 (line 337) says "late preparation is crash-explained only when …", but every ordinary Q8a boundary meets the same condition and is prepared through the "due, crash-explained" row.
- **(b) A refusal before any prepared line.** When `stage-plan` itself refuses (`foreign-change`, `changed-after-review`, `branch-changed`, `no-accepted-tree` and so on), FR-060 sends the refusal to FR-064's form `refused … attempt=<n>` (line 222), although no attempt exists yet. The boundary then matches both "due" (FR-105: no prepared or settling line) and "refused".
- **(c) "Eligible".** It is defined for boundaries (FR-103) but used for anchors (FR-058, "every member's anchor is eligible") and for task generations (FR-073).

**Consequence:** a reader can stumble over the terms. In every case the two candidate rows lead to the same prepare-or-stop result, so no outcome changes.

**Suggested fix**

- Define crash-explained as the condition itself, and say it holds at every Q8a.
- Say a refusal before preparation uses the next attempt number without pins and counts as "refused", not "due".
- Add "an anchor is eligible when it lies in an `on` segment".

### M3-5 (MINOR): revocation does not say what happens to a boundary that is already due

**Evidence**

- FR-050 (line 328) appends the revocation `run` line "before the next attempt".
- The FR-056 trigger and FR-107's left column both test "the flag is present", which stays literally true after a revocation.
- A boundary whose anchor was flushed before the revocation line is eligible and due. Round 3 has the same wording (`round3-C.md:28`).

**Consequence:** read literally, a revoked run could still commit that boundary. That reading is unlikely, but the rule is "plain words can narrow the grant, never widen it".

**Suggested fix:** "After a revocation line, the run counts as 'any other run' for FR-056 and FR-107; a boundary that is already due stops `unsettled` with the choices."

### M3-6 (MINOR, from fix cycle 2): the two-part split leaves the resumed outside-S comparison without its tool

**Evidence**

- Change 21 (line 296) puts FR-113 (the outside-S comparison of a resumed attempt) in "Reconcile and settle", which also binds unflagged runs.
- The only verb that performs the comparison, `verify` (FR-130, line 375), and the snapshot method it reuses (FR-111) are in "Commit procedure", which "applies only with the flag".
- No line form records `outside-changed` for an attempt that never got a result line, that is, a pending or interrupted one:
  - FR-100 puts `outside-changed=` only on `sha=` and `recovered` lines;
  - AC-08 lets an unflagged run append no `refused` line.
- The cycle-2 note says every FR now has a stated part. Three still have none:
  - FR-019's implement clause, which also sits in §2.2, the `/sc:git` section;
  - FR-071;
  - FR-078.

**Consequence**

An unflagged executor may believe it may not call `verify`. Data stays protected anyway: FR-113's "a failed or incomplete comparison stops `outside-unverified` and keeps the before pin" still applies, and FR-125 keeps pins whose damage report is outstanding.

**Suggested fix**

- Say that `verify` (or `reconcile`) performs the FR-113 comparison in any run that loads the ref, and that FR-111's snapshot method is shared.
- Place FR-019's implement clause and FR-071 in "Reconcile and settle", and FR-078 in "Commit procedure".
- Say that damage found on an attempt without a result line is recomputed from its pin on every run until the owner releases it.

### M3-7 (MINOR): plugin-only installs never find the helper

**Evidence**

- `<skill-dir>` (line 32) and FR-019 (line 122) look for the helper only at `<home>/skills/sc-git-protocol/` and then at `<dev>/skills/sc-git-protocol/`.
- A plugin-only install has neither:
  - `<home>` is what `<cli> install` writes;
  - `<dev>` exists only in a development checkout.
- So every write in both protocols stops `helper-missing`, even though the mirrored script ships with the plugin.
- This undercuts two things in the plan:
  - Change 6's rationale for C-020: "a mirrored skill script ships everywhere";
  - Risk Summary row 6: "loses plugin-only support".
- The precedent Change 6 cites (`refs/managed-workspace.md:54`) uses the base directory the loaded skill announces, as defined at `:72`.

**Consequence**

- It fails safe: reads still run and nothing is committed.
- The project instructions say the plugin system is not yet available in 6.1.0, so this is MINOR.

**Suggested fix**

- The git protocol runs `<skill base>/scripts/vcs.py` from its own announced base.
- The implement protocol tries the sibling `<skill base>/../sc-git-protocol/scripts/vcs.py` first, then `<home>`, then `<dev>`.
- Keep the rule that there is no `src/` fallback.

### M3-8 (MINOR): stale base text that no change edits

**Evidence**

- **NFR-002** keeps "The helper performs no write" (`variant-A.md:319`). Change 7 only appends to it (line 138). This contradicts:
  - FR-011's disclosed loose-object writes (line 137, the X-017 resolution);
  - NFR-007's "`stage-plan` writes the full list to the pathspec file" (line 499).
- **Risk 2's mitigation** keeps "Classified `commit-failed`; STOP; resume plans again (FR-064, FR-065)" (`variant-A.md:335`). It names a removed token and the removed automatic re-plan. Changes 4, 15 and 37 touch only Risk 2's residual and its rating.
- **FR-033** keeps "Hook refusal follows FR-064, but without ledger lines" (`:272`). FR-064 now pins `refs/<package>/implement/<slug>/rewritten/…`, and `/sc:git` has no slug.
- **The commit-paths file** (`commit-paths-<key>-a<n>.txt`, line 316): its writer and its step in FR-061 are not stated. If the helper wrote it beside a managed sidecar, it would write a work-tree file, which FR-011 forbids.

**Consequence:** three sentences in the merged document would contradict newer requirements, and one file has no named writer.

**Suggested fix**

- NFR-002: "The helper writes no ref, no user index, no work-tree file and no config (FR-011)."
- Risk 2 mitigation: "FR-036 classes; STOP; a later flagged run retries only as FR-065 and FR-107 allow."
- FR-033: "follows FR-036 and FR-064's no-retry rules, printing the report instead of a sidecar line, with any rewritten pin under `refs/<package>/git/`."
- FR-061 step (3): "the agent writes `commit-paths-<key>-a<n>.txt`, then appends the prepared line."

### M3-9 (MINOR): three mechanisms on failure branches are left to judgment (inherited from Round 3)

**Evidence**

- **Quiescence.** It is not said how a later invocation "establishes" that the earlier git and hook processes have stopped (FR-116). FR-123's `adopt` depends on it.
- **Renewed review.** FR-065, FR-074 and FR-107 require a "renewed review or Ruling given after the refusal displayed" a hook rewrite of product paths. No loop step provides that review in a later run.
- **Mixed batches.** FR-058's `skipped reason=mixed-authorization` line has no step that writes it. The FR-056 trigger fires only for a due boundary, and a mixed batch is never eligible, so never due.

**Consequence**

- Nothing becomes a dead end: `abandon` is always offered, and a mixed batch is never unsettled.
- In practice, though, a product-path hook rewrite ends in `abandon`, or in a manual commit followed by `adopt`.

**Suggested fix**

- Quiescence: name the evidence, for example no `index.lock` plus a process listing that shows no git or hook process running in this worktree, or the person's confirmation after the STOP.
- Renewed review: define it as a fresh reviewer run on the `rewritten=` tree at R0, which the person asks for after the STOP; or drop it and require restore-or-abandon.
- Mixed batches: say that Q8a or L0 appends the mixed-authorization line when a batch becomes all-complete.

### M3-10 (MINOR): debate finding ids remain in text meant for the merged document

**Evidence:** examples of INV ids inside merged text:

- FR-035 ends "(INV-012)";
- FR-066 "(INV-015)";
- the FR-074 heading "INV-025";
- FR-077 "INV-022";
- FR-058 "**INV-014:**";
- Change 18 "**INV-023.**";
- Change 4 item 4 "the INV-029 residual".

R2-M8 removed plan change numbers for the same reason.

**Consequence:** readers of the merged document cannot resolve these ids.

**Suggested fix:** keep the INV ids only in the provenance comments (`<!-- Source: debate Round 3 … -->`).

## Counts

BLOCKING: 0. MINOR: 10 (M3-1..M3-10). M3-6 is the only finding introduced by fix cycle 2; the others were present before it, or were inherited from Round 3 text.
