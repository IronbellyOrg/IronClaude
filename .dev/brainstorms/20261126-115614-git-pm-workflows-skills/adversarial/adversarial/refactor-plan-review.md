# Refactor Plan Review

## Verdict

**FAIL**: 3 BLOCKING findings, 16 MINOR.

The plan covers every diff point once. It carries all 16 ACCEPT-FIX rulings, all 3 ACCEPT-RISK residuals and the three HIGH resolutions, and it keeps the seed constraints. The FAIL comes from three internal contradictions that an executor following the plan word for word would write into the merged spec:

- B-1: the implement commit ref loads only with the flag, but unflagged runs must follow the rules inside it.
- B-2: the commit trigger keeps a stale meaning of "pending".
- B-3: the X-015 network contradiction is fixed only in NFR-001.

Each one has a small fix (see Findings).

## Checks run and results

Sources read in full: `refactor-plan.md`, `base-selection.md`, `blind/variant-A.md`, `variant-B.md`, `variant-C.md`, `debate/scoring-matrix.md`, `invariant-probe.md` (including "Round 3 Resolution"), `debate/round3-A.md`, `round3-B.md`, `round3-C.md` and `seed-brief.md`. I also checked repository facts read-only.

### Check 1: coverage and the winner of each diff point

- I tallied all 61 ids (S-001..S-013, C-001..C-021, X-001..X-021, A-001..A-006):
  - 51 appear on exactly one change's **Diff points** line.
  - 10 appear in "Changes NOT Being Made": S-001, S-004, S-012, C-001, C-002, X-002, X-003, X-009, X-011, X-012.
  - None is missing and none is duplicated. The plan has 39 change headings, which matches its own count.
- I compared each planned treatment with the final-round winner in the scoring matrix. All agree except A-005.
  - Some changes add minority HYBRID elements next to a single-variant winner: C-003 adds C's grant scope (FR-023), C-020 adds C's "no implicit install", and X-005 adds the INV-018 and INV-024 fixes. Each addition fits the winner's text, so none is a disagreement.
- **A-005: following Round 3 over the matrix is right.**
  - The matrix row's evidence text ("fixed by the `unstaged-outside` refusal") is copied from Variant A's own Round 3 vote (`round3-A.md:230`).
  - Variant B's vote says "fixed by the worktree pin and outside-S check" (`round3-B.md:255`). Variant C votes HYBRID for the Round 3 snapshot design (`round3-C.md:184`).
  - `invariant-probe.md:46` records that INV-021 was resolved by B's snapshot design replacing A's refusal, with C agreeing.
  - The winner is NONE, so no variant's text binds the merge. Two of three advocates plus the recorded resolution support the snapshot design.
- Two vote counts in the plan's rationale text are wrong; see M-1.

### Check 2: invariant rulings and HIGH resolutions

All 16 ACCEPT-FIX findings are present:

| Finding | Change |
|---|---|
| INV-002 | 17 |
| INV-003 | 19 (FR-073) |
| INV-004 | 25 (FR-132) |
| INV-007, INV-008 | 13 (FR-062 a-c) |
| INV-009, INV-010 | 30 |
| INV-012 | 13 (FR-035) |
| INV-014 | 23 (FR-058) |
| INV-015 | 14 |
| INV-020 | 15 |
| INV-022 | 16 (FR-077) |
| INV-023 | 18 |
| INV-024 | 20 (FR-038) |
| INV-025 | 19 (FR-074) |
| INV-030 | 31 |

All three ACCEPT-RISK residuals are present: INV-011 (Change 23, item 6), INV-018 (FR-076), INV-029 (Change 15 Risk 2 and Change 37 row 19).

The HIGH resolutions follow `round3-C.md` item by item:

- INV-001 items 1-9 map to FR-100..FR-109, plus FR-073, FR-077 and FR-131.
- INV-021 items 1-9 map to FR-110..FR-118.
- INV-027 items 1-7 map to FR-120..FR-126.

Specific details I checked and found faithful:

- the first-`complete` anchor;
- counting an unterminated last line;
- `out-of-protocol`;
- the PLAN check before reconcile;
- pinning the outside-S comparison before the new `run` line;
- full 64-hex keys;
- create-once sibling pins;
- the 600000 ms commit call;
- `abandon` always offered;
- a reply counts only after the disclosure;
- no `branch-unproven` fallback.

One ACCEPT-FIX rendering is internally impossible (INV-023, see M-2).

### Check 3: are the base defects really fixed?

| Defect | Result |
|---|---|
| FR-052/T-15 vs FR-091 | Fixed. Change 24 adds `WORKER-CONTRACT.md` to the allowed list. Verified that no plugin copy of `WORKER-CONTRACT.md` exists (`find plugins -name WORKER-CONTRACT.md` prints nothing), so the list is complete. |
| X-015 | Not fully fixed. NFR-001 is amended, but §1.4, FR-005 and the new FR-042 text still say `/sc:git` never fetches (B-3). |
| X-019 | Fixed. `<pkg-dir>` and `<run-dir>` are added. All task-package uses of `<pkg>` in the base (FR-060, FR-061, FR-062, FR-064, T-01) are rewritten or replaced. |
| Crash recovery | Fixed in substance: FR-108, FR-130 and T-22 replace the base's false `COMMIT: none` after a crash. Two gaps remain: the candidate-build step and the `reconcile` verb are not specified (M-7). |
| Section order | Fixed, apart from missed and mislabelled cross-references (M-3). |
| Undefined terms | Mostly fixed by §1.7. "S" (the commit set) is still never defined for the implement step, and the Terms row points at the wrong FRs (M-3). |
| Risk ratings | Fixed by Change 37. |

### Check 4: internal consistency (ten riskiest changes)

I reviewed Changes 5, 15, 17, 18, 19, 22, 23, 25, 26 and 27, plus Change 21's load rule and Change 34's NFR-018.

- **Requirement ids:** no new FR, NFR, T, AC or D id collides with the base (base FR blocks: 001-017, 020-022, 030-034, 040-043, 050-072, 080-082, 090-094).
- **Base locations named by the plan:** they exist in `variant-A.md`, except these:
  - Change 4 targets a §1.5 `<dev>` row that does not exist (M-4).
  - Change 5 labels FR-013's "§2.2" reference as FR-007's (M-3).
- **Contradictions found:** B-1, B-2, M-5, M-6, M-8 and M-9.

### Check 5: seed constraints and vendor names

All of these hold:

- no push, merge or PR in `/sc:git` (FR-004, FR-005, D7);
- no relay (D2, FR-072);
- PRs stay with `/sc:pr-submit`;
- local branch cleanup only by reuse (FR-080, FR-081);
- no remote branch deletion;
- no installed primitive names a `src/<package>/` path (FR-019 resolves `<home>` then `<dev>`; NFR-010).

Two items need wording fixes:

- **Dev-copy staging:** nothing in the plan stages a `<dev>/` path, but one refusal message invites the person to do it (M-12).
- **Model and vendor names:** `grep -inoE 'claude|opus|sonnet|haiku|gpt|gemini|anthropic'` finds none in `variant-A.md`. In the plan the only hits are the excluded grep on line 10. The Change 3 rewording correctly removes RC-7's tool names. AC-21, however, extends the vendor-name rule to primitives in a way that conflicts with the installed paths they must contain (M-11).

### Repository facts the plan cites (spot-checked, all hold)

- `SKILL.md`: lines 40-51 (`E-RESUME-NEEDED`, `E-PLAN-CHANGED`, `E-ARCHIVE-BLOCKED`, the closed-list sentence at 51), 57-59, 79, 110, 118, 121-150 and 124-129.
- `refs/ledger.md`: lines 3, 62-72, 84-86, 127, 134, 139, 149, 157, 158 and 239.
- `refs/retry.md`: lines 28, 40, 41, 212 and 504.
- `refs/qa.md`: lines 178, 182, 248, 254 and 311.
- `refs/managed-workspace.md`: lines 36, 44, 48 and 94.
- `WORKER-CONTRACT.md`: lines 23, 32, 41-47 and 57.
- `launch-level-guard.sh`: lines 58-60, 691-701 (global options are skipped before the subcommand, so `git --literal-pathspecs commit` still classes as COMMIT), 713, 716, 720, 724, 777, 786 and 816.
- `.gitignore:127-135`. `git ls-files .claude/` lists `settings.json` and `cache/sc-recommend-lookup.yaml`.
- The common hooks directory holds only `pre-push`, `pre-push.launch-level` and samples; `core.hooksPath` is unset.
- `.pre-commit-config.yaml`: lines 9-45, 78-91 and 130-134.
- `worktrees.md`: lines 17, 37 and 45.
- `test_routing_refresh.py:224-243`.
- `test_worker_contract.py`: lines 1894-1897, 2945-2960 and 3227.
- `archive_workspace.py`: its `_digest` treats a missing `files=` path as `absent` and does not fail, so FR-062(b) (deleted paths in `files=`) does not break archiving.
- `git ls-files commands/ | wc -l` prints 21, so AC-04's 20 after deletion is right.

## Findings

### B-1 (BLOCKING): the implement commit ref loads only with the flag, but unflagged runs must follow the rules inside it

**Evidence**

- Base FR-072 says the implement commit ref "is loaded only when `--commit-tasks` is present" (`variant-A.md:241`). Base T-09 checks that it is "loaded only with the flag" (`variant-A.md:305`).
- The plan renames the ref to `refs/commit-step.md` (Change 21, plan line 292). It keeps that load rule. Change 5 makes the ref hold "§6.3-§6.6 and §7".
- Change 21 says `SKILL.md` gains only "the Q8a line, the Wave 0 option and step, the two STOP rows and the load rule". The Wave 0 step is the flag-only preflight.
- Yet the merged §7 binds runs **without** the flag:
  - FR-051: "if `commits.md` exists it appends an `off` run line and reconciles";
  - FR-101: every later invocation appends a `run` line;
  - FR-106: the reconcile order;
  - FR-107: the "Any other run" column;
  - FR-077: settle before advance;
  - FR-120..FR-126: owner resolution in unflagged runs.
- NFR-018 also says an unflagged run "adds no Bash call", while FR-106 and FR-113 require reconcile and snapshot calls.

**Consequence**

An unflagged run never loads those rules, so it writes no `off` line and does not stop on an unsettled boundary. Its `complete` lines then fall into the previous `on` segment (FR-102). In the next flagged run, FR-105 marks only boundaries followed by a later `start` as `out-of-protocol`. The last task completed in the unflagged run is therefore "crash-explained" and gets committed. That is a commit of work done without the flag, which breaks X-006, A-003 and the seed constraint "no commit without authorization". It also reopens the INV-022 and INV-023 hazards that settle-before-advance was meant to close.

**Fix**

- Change the FR-072 load rule to: "loaded when `--commit-tasks` is present or a `commits.md` exists in the ledger directory".
- Adjust T-09 to match.
- Count the one new `SKILL.md` line in the NFR-012 budget.
- Reword NFR-018 to "no Bash call and no file when no `commits.md` exists; otherwise one `off` run line plus reconcile".

### B-2 (BLOCKING): the commit trigger keeps a stale meaning of "pending"

**Evidence**

- Change 23, item 3, tells the executor to keep FR-056's last bullet: "The commit step runs when, and only when, the flag is present, the pending set is not empty, and no task is open" (`variant-A.md:189`).
- The same item replaces the old "pending" definition with the new state words.
- FR-107 (Change 23) now defines **pending** as "prepared, no terminal line, HEAD = parent". A boundary that has just become eligible is **due** (FR-105), not pending.

**Consequence**

Read with the new definitions, the kept bullet lets the commit step run only on an already-prepared attempt. A due boundary would never be prepared at Q8a, R0 or L0, so the feature would never make its first commit. That contradicts FR-057, FR-107's "due, crash-explained → Prepare now" and AC-05.

**Fix**

Replace the last bullet with: "The commit step runs at Q8a, R0 and L0 only when the flag is present, no task is open, and a boundary is due or FR-107 allows a new attempt on a pending or refused one." Also replace "the pending-set rule" in FR-094 (`variant-A.md:289`).

### B-3 (BLOCKING): the X-015 contradiction survives outside NFR-001

**Evidence**

- Change 30 rewrites FR-041. `update` now runs `git submodule update --init` for an uninitialized module (a clone) and for `target-not-local` ("the fetch is disclosed first").
- FR-044 binds the clone URL, and NFR-001 gains a stated exception for this.
- The plan does not touch three other places that say the opposite:
  - §1.4 lists "Push, fetch, pull, merge, rebase" as out of scope (`variant-A.md:38`);
  - FR-005 Boundaries Will Not lists "fetch" (`variant-A.md:93`), and T-12 tests that Will Not text;
  - the new FR-042 refusal text (Change 31) says "`/sc:git` never pushes or fetches".

**Consequence**

The merged spec would state in four places that `/sc:git` never fetches, while FR-041 and FR-044 fetch and clone under a person's grant. This is the defect base-selection named, now spread across the command's Boundaries (copied into `git.md` and pinned by T-12). An implementer cannot meet both the `git.md` text and FR-041.

**Fix**

Amend §1.4, FR-005 and the FR-042 message to: "never pushes; never fetches on its own; `submodule update` may clone or fetch from the `.gitmodules` URL only as FR-044 authorizes". Add FR-005 and §1.4 to Change 30's Target.

### M-1 (MINOR): two vote counts in the rationale are wrong

**Evidence**

- Change 8 says for S-009 "(A in Round 2 voted A)". In fact the A advocate voted A in Round 3 (`round3-A.md:179`; the matrix shows A/HYBRID/HYBRID).
- Change 31 says for A-004 "all HYBRID". The C advocate voted C (`round3-C.md:183`; the matrix shows HYBRID/HYBRID/C).

**Consequence:** none on the planned treatment; only the audit trail is wrong.

**Fix:** correct both rationale sentences.

### M-2 (MINOR): the INV-023 archive gate cannot detect a due boundary as written

**Evidence**

Change 18 says the archive gate refuses "while `commits.md` has a due, pending, refused or uncertain boundary. It reads `commits.md` only". But FR-105 defines a due boundary as one with no prepared or settling line, and eligibility comes from the ledger's anchors (FR-103). So `commits.md` alone cannot reveal a due boundary. Round 3 requires the check to include due states, "without adding commit record kinds to the task ledger" (`round3-C.md:101`). It does not say "reads commits.md only".

**Consequence:** the second line of defence misses the INV-001 crash state.

**Fix:** "It reads the ledger and `commits.md`, and adds no record kind to the task ledger."

### M-3 (MINOR): cross-reference and definition errors

**Evidence**

- FR-073 (Change 19) and Change 23 item 3 cite FR-102 for eligibility. Eligibility is defined in FR-103.
- Change 2's Terms row says "Boundary, S, unsettled, due: defined in §7 (FR-101, FR-105, FR-106)":
  - "unsettled" is defined in FR-107;
  - FR-101 and FR-106 define neither "Boundary" nor "S";
  - "S" is never defined for the implement step: FR-062 names the set `commit_paths`, and FR-076 only says "S includes".
- Change 5 says "FR-007 '§2.2' stays", but the "§2.2" reference is in FR-013 (`variant-A.md:124`).
- Change 5's renumbering list misses the §3 authorization table row "Between-task commit … | §4" (`variant-A.md:155`), which must become §6.

**Fix**

- Define S once, for example in FR-062: "S = `commit_paths` plus, for a managed run, the FR-076 expansion".
- Correct the FR ids above.
- Add the §3 table row to Change 5's list.

### M-4 (MINOR): Change 4, item 2, edits a base row that does not exist

**Evidence:** `variant-A.md` §1.5 has no row about `<dev>`. The "only tracked file" claim sits in the §1.1 table (line 19), which Change 1 already replaces, and in FR-016.

**Fix:** say "add a new §1.5 row" and also correct FR-016's sentence.

### M-5 (MINOR): `index-locked` has two STOP codes with no rule for which applies

**Evidence:** FR-054 (Change 17) stops `E-COMMIT-PRECONDITION reason=index-locked`. FR-116 and Change 18 stop `E-RESUME-NEEDED reason=index-locked` for the same lock file.

**Fix:** state that the Wave 0 preflight of a flagged run uses `E-COMMIT-PRECONDITION`, and that reconcile and an interrupted commit use `E-RESUME-NEEDED`.

### M-6 (MINOR): FR-065 allows a retry that FR-107 forbids

**Evidence:** FR-065 (Change 15) allows a new attempt "after `hook-rewrite` or `hook-rewrite-committed`" once the paths are restored. But `hook-rewrite-committed` means HEAD has moved, and FR-107's row "refused with HEAD ≠ parent" offers only the owner choices.

**Fix:** drop `hook-rewrite-committed` from FR-065's retry clause and point to FR-121 instead.

### M-7 (MINOR): helper verbs are under-specified

**Evidence**

- FR-061 step (4) says "helper builds the frozen candidate". This must run after the prepared line is appended, because the candidate includes the sidecar's prepared bytes, so it cannot be step (1)'s `stage-plan`. No verb is named for it.
- Change 6 says `reconcile` is "specified in §7", but no FR gives its inputs or outputs.
- AC-03 fixes the verb count at seven.

**Fix:** name the verb or mode that builds the candidate (for example `stage-plan --candidate`), and add a short `reconcile` input/output sentence to FR-106.

### M-8 (MINOR): it is unclear whether unflagged runs record the branch at Q0

**Evidence:** the INV-002 rule (Change 17) says "At every new Q0 the executor records … `q0-branch`", but it is appended to FR-054, which applies only "When `--commit-tasks` is present". If unflagged runs record it too, that contradicts NFR-018 ("no file") and AC-08 ("behavior unchanged").

**Fix:** state that recording is flag-only, and that a task started in an unflagged run refuses `branch-unproven`, which fails safe and matches Round 3's "missing historical branch proof".

### M-9 (MINOR): FR-013 and NFR-011 disagree on the minimum git version

**Evidence:** FR-013 still holds `MIN_GIT = (2, 23)` (`variant-A.md:122`). Change 34's NFR-011 says `MIN_GIT` holds the higher `--pathspec-from-file` version.

**Fix:** edit FR-013's last bullet to match.

### M-10 (MINOR): one stored file name uses a short key prefix

**Evidence:** FR-100 saves `commit-paths-<key12>-a<n>.txt`. FR-103 says "every stored key and machine reference uses all 64 hex characters".

**Fix:** use the full key in the file name.

### M-11 (MINOR): AC-21's vendor-name scan of primitives is unsourced and likely unsatisfiable

**Evidence**

- AC-21 (Change 36) scans "new and edited primitives for model and vendor names", with the word list left to T-13.
- Primitives must name installed paths `~/.claude/...` (root rule; seed constraint). They also write pins `refs/superclaude/implement/...`, which `sc-implement-protocol` already does 9 times.
- A list like the plan's own grep (`claude|...`) matches both. The repository already has a narrower model-alias policy (`tests/skills/test_model_alias_policy.py`).
- No debate point asks for this check.

**Fix:** drop the vendor-name half of AC-21 and keep only the `src/<package>/` check. Or define the list as full model ids only, consistent with the existing policy test.

### M-12 (MINOR): a refusal message invites staging a dev-copy path

**Evidence:** Change 4 item 3's `dev-copy-path` refusal "says the person may stage it themselves". The root instructions forbid suggesting that any `.claude/` path other than `settings.json` be staged without an explicit instruction in the session.

**Fix:** the refusal names the file and stops, with no staging suggestion.

### M-13 (MINOR): `/sc:git` recovery pins are never released

**Evidence:** FR-117 applies FR-110..FR-116 to `/sc:git commit` with refs `refs/<package>/git/boundary-wt/<timestamp>`. The release rule (FR-131) covers only the implement step, and FR-115 keeps a pin "until the owner directs its release".

**Consequence:** every `/sc:git commit` leaves one ref behind, even when the comparison is clean.

**Fix:** delete the pin with a visible `git update-ref -d` call after a clean comparison; keep it only while an outside-change report is outstanding.

### M-14 (MINOR): a credential-bearing URL can never match FR-044

**Evidence:** FR-044 displays the `.gitmodules` URL "with any credentials removed" but requires the typed `--url` to match it "byte for byte". If the real URL contains credentials, the person can only type the redacted form, so the match always fails. This fails safe, but the requirement is ambiguous.

**Fix:** compare against the displayed, credential-free form, or refuse credential-bearing URLs with a named token.

### M-15 (MINOR): "detached HEAD refused everywhere" reads against FR-042

**Evidence:** Change 11 adds "A detached HEAD is refused everywhere" to FR-032. FR-042 (Change 31) says "A detached HEAD at a contained target is eligible", meaning the submodule's HEAD.

**Fix:** write "a detached superproject HEAD".

### M-16 (MINOR): Change 28 misdescribes the S23 fixture

**Evidence:** Change 28 says S23's "mode_flags stay `["--smart-commit"]`". In the fixture the top-level `mode_flags` is `[]` (`routing_refresh_cases.json:318`). `--smart-commit` is in the repeat's `mode_flags` (`:327`).

**Fix:** reword to match the fixture.
