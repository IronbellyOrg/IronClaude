# Refactor Plan Re-review (after fix cycle 1)

## Verdict

**FAIL**: 1 BLOCKING finding, 11 MINOR.

The three earlier BLOCKING findings are fixed as the first review asked:

- B-1: the load rule and its two parts.
- B-2: the trigger bullet and FR-094.
- B-3: §1.4, FR-005, T-12, the FR-042 text and NFR-001.

All 61 diff points are still handled exactly once, no new id collides with the base, and the seed constraints hold. The FAIL comes from one finding the first review missed: the same stale meaning of "pending" that B-2 removed from FR-056 is still in FR-062's definition of the commit set. Following the plan as written, every boundary would be settled as "skipped, empty" and never committed. The fix is one sentence (R2-B1).

## Checks run and results

Read in full:

- `refactor-plan.md`, including the revision note;
- `refactor-plan-review.md`;
- `blind/variant-A.md`, and the parts of `variant-B.md` the plan copies (Path notation, RC-1..RC-7);
- `base-selection.md`, `debate/scoring-matrix.md` and `invariant-probe.md`;
- `debate/round3-A.md`, `round3-B.md` and `round3-C.md`;
- `seed-brief.md`.

Repository facts were checked read-only:

- `SKILL.md:36-151`;
- `refs/ledger.md:30-164`;
- `refs/retry.md:20-48` and `:504`;
- `refs/managed-workspace.md:30-95`;
- `WORKER-CONTRACT.md:42-47` and `:245`;
- `routing_refresh_cases.json:312-331`;
- `.gitignore:125-136`;
- `git ls-files .claude/`.

### Check 1: are the three earlier BLOCKING findings really fixed?

| Finding | Result | Evidence in the plan text |
|---|---|---|
| B-1 | Fixed | Change 21 (line 293): the ref loads when the flag is present or `commits.md` exists. Its "Reconcile and settle" part lists FR-051, FR-077, FR-100..FR-108, FR-113, FR-114..FR-116 and FR-120..FR-126 for unflagged runs. "Commit procedure" and the Wave 0 preflight stay flag-only. T-09, NFR-018 (line 505), T-16 (line 516) and AC-08 (line 528) are updated. This matches Round 3 INV-001 items 1 and 7 (`round3-C.md:28`, `:34`). Side effects: R2-M2, R2-M3, R2-M4. |
| B-2 | Fixed as specified, but incomplete | Change 23 item 3 (line 327) replaces FR-056's trigger bullet and FR-094's phrase. The same stale "pending" survives in FR-062 bullet 1 (`variant-A.md:215`), which no change replaces (R2-B1). The new trigger's parenthetical also overstates (R2-M6). |
| B-3 | Fixed | Change 30 items 6, 8 and 9 (lines 453-456) and Change 31 (line 466) now say "never fetches on its own; `submodule update` may clone or fetch from the `.gitmodules` URL only as FR-041/FR-044 authorize". D4 (Change 38) matches. FR-004's STOP of a `fetch` operation and the §3 "forbidden" row are about operations, so they stay consistent. This matches Round 3 INV-009 and INV-010. |

### Check 2: did the fix-cycle edits introduce defects?

- **Regions re-read:** every region the revision note names, which is Changes 2, 4, 5, 6, 8, 11, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 28, 30, 31, 34, 35 and 36, plus Risk Summary row 4.
- **Diff points:** a script tallied the ids on all **Diff points** lines plus the "Changes NOT Being Made" rows. All 61 ids appear exactly once, with none missing and none extra. There are 39 change headings, matching the plan's count.
- **New ids:**
  - FR-018, FR-019, FR-023, FR-035, FR-036, FR-038, FR-039, FR-044..FR-046, FR-073..FR-079, FR-100..FR-109, FR-110..FR-118, FR-120..FR-126 and FR-130..FR-133;
  - NFR-012..NFR-018, T-19..T-27, AC-16..AC-21 and D9..D11.

  None collides with the base blocks (FR 001-017, 020-022, 030-034, 040-043, 050-072, 080-082, 090-094; NFR-001..011; T-01..T-18; AC-01..AC-15; D1..D8), and none is defined twice. The revision note's claim that no new id was created holds.
- **Base locations:** every base location the plan names exists in `variant-A.md`. These include:
  - FR-016's sentence (line 140) and the §1.5 `conventional-pre-commit` row (line 64);
  - FR-013's "§2.2" (line 124) and the §3 table row "§4" (line 155);
  - FR-094's phrase (line 289), the FR-062 managed sentence (line 216) and FR-020's "reached any other way" (line 158).
- **Vote counts:** the vote counts fixed under M-1 match the scoring matrix. Spot checks of eight other rationale vote counts also match.
- **Contradictions found:** R2-B1 (with B-2's fix), R2-M3 (AC-08/NFR-018 against FR-107/FR-126/AC-18) and R2-M5 (FR-032 against FR-043). The other findings are gaps or wording.

### Check 3: can the executor apply Change 20's FR-062 "managed sentence" target?

Only with its own judgment, so this is MINOR (R2-M1).

- Change 20 names the sentence as a target but gives no text for it.
- The executor has to infer from FR-076 and the new S definition ("S is `commit_paths` plus, for a managed run, the FR-076 expansion", line 284) that the sentence must stop adding the package directory to `commit_paths`.
- If the executor keeps it with only Change 1's alias edit, FR-062 would contain both the package directory and its literal expansion. It would also keep a stale "step 3" (staging is step 5 in Change 25).
- No safety boundary breaks:
  - INV-018's package residual is already accepted;
  - other packages stay out;
  - the frozen-candidate check still applies.

### Check 4: seed constraints and vendor names

| Constraint | Result |
|---|---|
| No push, merge or PR creation in `/sc:git` | Holds (FR-004, FR-005, D7, NFR-001; NFR-001's only exception is a clone or fetch) |
| No relay | Holds (FR-072, D2) |
| PRs stay with `/sc:pr-submit` | Holds (§1.4) |
| Reuse of local branch cleanup only | Holds (FR-080 routing, FR-081) |
| No remote branch deletion | Holds (FR-081, AC-11) |
| No staging of the dev-copy folder | Holds (FR-013, FR-016, FR-031 refusal with no staging hint, FR-062 exclusion, FR-033's index refusal kept) |
| No installed primitive names a source-tree path | Holds (FR-009, FR-019 resolves `<home>` then `<dev>` with no `src/` fallback, NFR-010, AC-21) |
| No model or vendor names in the merged document | Holds. `grep -inE 'claude\|opus\|sonnet\|haiku\|gpt\|gemini\|anthropic\|superclaude'` over the plan hits only the executor-only grep on line 10. The copied Variant B text is clean once Change 3 drops RC-7's tool names (`variant-B.md:114-116`). Variant B's other "Aider" mention (`:291`) is not taken into FR-075. Refs are written `refs/<package>/...`. |

## Findings

### R2-B1 (BLOCKING): FR-062 still defines the commit set over "pending tasks"

**Evidence**

- Base FR-062, bullet 1 (`variant-A.md:215`): "`commit_paths` is the sorted union of the `files=` fields on the pending tasks' latest `complete` lines."
- No change replaces that bullet:
  - Change 1 edits only "the package directory";
  - Change 13 appends items (a)-(e);
  - Change 20 adds the S definition *after* the bullet (line 284).
- Change 23 item 3 (line 327) redefines "pending" for the whole document as an FR-107 state: prepared, no terminal line, HEAD = parent. Change 2's Terms row says the same (line 60: "Pending, unsettled: FR-107").
- At first preparation, `vcs stage-plan` computes S at step (1) of FR-061 (Change 25, line 371), before the prepared line is appended at step (3). So the boundary is **due**, not pending.

**Consequence**

- Read with the merged definitions, `commit_paths` is empty at every first preparation.
- FR-062 then returns `nothing`, and FR-060 (Change 22 item 2) appends `T<ids>: commit skipped key=<key> reason=empty`. That is a settling line (FR-107).
- So every boundary is settled permanently with no commit, silently. That defeats FR-057, FR-107's "due, crash-explained → Prepare now", AC-05 and AC-16.
- This is the same defect as B-2, which was graded BLOCKING, now in the requirement that defines S. The revision note's "B-2 FIXED" is true only for FR-056 and FR-094.

**Suggested fix**

In FR-062, replace "on the pending tasks' latest `complete` lines" with "on the anchor `complete` lines (FR-103) of the members of the boundary being prepared".

- A re-review `complete` repeats the same verdict fields (`refs/ledger.md:84-86`), so the files are unchanged.
- The anchor is also the line the accepted pin is bound to (FR-073, FR-104).

### R2-M1 (MINOR): Change 20 names FR-062's managed sentence as a target with no replacement text

**Evidence:** Change 20's Target (line 276) names it, but its edit instructions (lines 281-284) contain no text for it. The base sentence (`variant-A.md:216`) is "For a managed run, it also includes the package directory … They stay staged by step 3."

**Consequence:**

- If the executor keeps the sentence, `commit_paths` contains the package directory as a directory entry, next to FR-076's literal-file expansion.
- "Step 3" then points at the wrong step (staging is step 5 in Change 25).
- No data or safety effect.

**Suggested fix:** give the text: "For a managed run, S also contains the FR-076 expansion of `<pkg-dir>` (literal files, never the directory). It does not include all of `.dev/tasks`, so other packages stay out of the commit; they stay staged by FR-061 step 5."

### R2-M2 (MINOR): the two-part split of `refs/commit-step.md` leaves several FRs without a stated part or home

**Evidence**

- Change 5 (line 107) makes FR-072 hold "§6.3-§6.6 and §7".
- Change 21 (line 293) assigns "Reconcile and settle" FR-051, FR-077, FR-100..FR-108, FR-113, FR-114..FR-116 and FR-120..FR-126. It assigns "Commit procedure" "§6.3-§6.6 apart from FR-077".
- That leaves these unassigned:
  - FR-109..FR-112, FR-117, FR-118 and FR-130..FR-133;
  - FR-050's revocation and grant-continuation rules (§6.1, which is outside both §6.3-§6.6 and the `SKILL.md` additions list).
- FR-131 says it applies "on any run, flagged or not" (line 373) but is not in "Reconcile and settle".
- FR-117 is a `/sc:git` rule, and the plan names no `sc-git-protocol` ref for FR-110..FR-117.

**Consequence:**

- The executor must guess the split.
- After an unflagged run records `recovered`, it could leave pins in place. They are listed in the summary, so nothing is lost.

**Suggested fix:**

- Add FR-131 and FR-133 to "Reconcile and settle".
- State that FR-050's in-run rules, FR-110..FR-112, FR-130 and FR-132 are in "Commit procedure", and that the tests (FR-109, FR-118, FR-126) are spec-only.
- Place FR-110..FR-117's `/sc:git` side in `sc-git-protocol/refs/commit.md`.

### R2-M3 (MINOR): AC-08 and NFR-018 say an unflagged run appends "only" an `off` line, but FR-107 and FR-120..FR-126 let it append more

**Evidence**

- AC-08 (line 528) says an unflagged run "appends only an `off` run line, reconciles and makes no commit". NFR-018 (line 505) says the same.
- FR-107's "Any other run" column (line 342) "may record a proved existing commit as `recovered`".
- FR-126 and AC-18 (lines 416, 529) require `abandon` (a `resolved` line plus `update-ref -d` calls) in unflagged runs.
- This wording was introduced by the B-1 fix.

**Consequence:** AC-08 and AC-18 cannot both be met literally.

**Suggested fix:** "… appends one `off` run line, plus any `recovered` or `resolved` line that reconcile (FR-107) or an owner answer (FR-120) produces, and makes no commit."

### R2-M4 (MINOR): no stop is defined when the helper is missing in an unflagged run that has a `commits.md`

**Evidence**

- With B-1's fix, an unflagged run must run `vcs reconcile` (FR-106) whenever `commits.md` exists.
- FR-019 (line 122) says only that writes stop with `helper-missing` "and reads still run".
- The `helper-missing` stop exists only in the flagged Wave 0 preflight (FR-054).
- NFR-016 (line 503) demands "a refusal" but names no code for this path.

**Consequence:** an executor could skip reconcile and start tasks while a boundary is due. That boundary then turns into the out-of-protocol case and needs the owner to resolve it. No commit and no data loss result.

**Suggested fix:** "When `commits.md` exists and the helper is missing or `vcs_contract` ≠ "1", Wave 0 stops `E-COMMIT-REFUSED reason=helper-missing` before task selection, with or without the flag." Add `helper-missing` to FR-070's reason list.

### R2-M5 (MINOR): the "detached superproject HEAD" wording (M-15 fix) blurs FR-043

**Evidence**

- Change 11 (line 174): "A detached superproject HEAD is refused for every local-history write; a submodule's own detached HEAD follows FR-042."
- FR-043 (`variant-A.md:265`, kept) relies on FR-032 refusing a detached HEAD *inside* a submodule's work tree, so that a branch is created first.
- FR-042 (line 466) says "A detached HEAD at a contained target is eligible".

**Consequence:** a reader can conclude that `/sc:git commit` run inside a detached submodule is allowed. That makes commits on no branch, the stop-and-ask case of the seed research.

**Suggested fix:** "A detached HEAD in the repository that receives the commit is refused, including inside a submodule's work tree (FR-043). Only `commit-pointer` reads the submodule's detached HEAD, under FR-042."

### R2-M6 (MINOR): the new trigger bullet says a due boundary "is then prepared and attempted"

**Evidence:** Change 23 item 3 (line 327) says that. FR-107's "due, out-of-protocol" row instead STOPs with no preparation, as do the branch, foreign-change and changed-after-review refusals.

**Consequence:** the parenthetical contradicts the state table. FR-107 is cited, so the table governs.

**Suggested fix:** "a boundary is due (FR-107 decides whether it is prepared or stops)".

### R2-M7 (MINOR): stale helper names survive outside the regions Change 6 edits

**Evidence**

- FR-060 still runs "`<cli> vcs stage-plan`" (`variant-A.md:201`). Changes 22 and 25 edit only its record forms and `ok` branch.
- FR-081 tests "`<pkg>/cli/vcs/`" (`:280`).
- T-13 and NFR-003 still say `rules.py` (`:309`, `:320`). FR-013 now says `vcs_rules.py`.

**Consequence:** these contradict §2.3 (a skill script and `vcs_rules.py`) and point a test at a directory that will not exist.

**Suggested fix:** add the four sites to Change 6:

- FR-060: the FR-019-resolved `vcs.py` call;
- FR-081: `<pkg>/skills/sc-git-protocol/scripts/`;
- T-13 and NFR-003: `vcs_rules.py`.

### R2-M8 (MINOR): plan-internal change numbers inside text meant for the merged document

**Evidence**

- Change 1's `<dev>` row: "(tracked exceptions, see Change 4)" (line 31).
- Change 4 item 4's quoted residual: "(Change 15, INV-029)" (line 82).
- Change 25 step (2): "(FR-061 step 1 of Change 14)" (line 371). This points at a step that Change 25 itself replaces.

**Consequence:** the merged document would cite change numbers that its readers cannot resolve.

**Suggested fix:** replace them with §1.5, Risk 2/FR-036 and "the message file of FR-061 step (2)". Fold Change 14 item 1's text into Change 25 step (2).

### R2-M9 (MINOR): the `run` line form needs a branch on a detached HEAD

**Evidence:**

- FR-100's `run` form requires `branch=<full symbolic ref>` (line 306).
- Only a flagged run refuses a detached HEAD (FR-054).
- With B-1's fix, an unflagged run on a detached HEAD with an existing `commits.md` must append a `run` line, but `git symbolic-ref -q HEAD` prints nothing there.

**Consequence:** the parser rejects the line, or the executor invents a value.

**Suggested fix:** allow `branch=-` (detached) on `off` lines only. A `-` branch never satisfies FR-054 or the branch check.

### R2-M10 (MINOR): the 200-entry path-list cap can truncate S

**Evidence:**

- Base NFR-007 (`variant-A.md:324`, kept): "path lists hold at most 200 entries with a `truncated` flag".
- `commit_paths` is a path list in `stage-plan` JSON.
- FR-076 expands a managed package to literal files, which can exceed 200.
- Change 34 (line 496) exempts only display lists and comparisons.

**Consequence:** the commit set could be cut short. The cut files stay uncommitted but are not lost.

**Suggested fix:** "The cap never applies to S, the pathspec file or `paths=`; `stage-plan` writes the full list to the pathspec file, and a truncated S refuses."

### R2-M11 (MINOR): two small accuracy slips

**Evidence:**

- The Overview (line 9) says four changes are High risk (5, 22, 23, 25). Change 26 is also High (line 385; Risk Summary row 26).
- Change 18's INV-023 bullet (line 257) cites `refs/managed-workspace.md:48` for "archive gate step 1". Line 48 is the dispatch paragraph; step 1 is line 52.

**Consequence:** audit trail only.

**Suggested fix:** say five High-risk changes, including Change 26, and cite `:52` (or `:48-52`).
