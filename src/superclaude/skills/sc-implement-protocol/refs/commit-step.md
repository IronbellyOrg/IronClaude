# Commit step, part one: Reconcile and settle

Loaded when `--commit-tasks` is on the invocation line or a `commits.md` exists in the ledger directory (legacy `.dev/implement/<slug>/`, managed `<pkg>/artifacts/`). A run with neither adds no Bash call and writes no file (NFR-018). Nothing in this part makes a commit. Every line is appended and flushed before the side effect it announces, and only the executor appends.

## Helper

`vcs` is `uv run --no-project python <skill-dir>/scripts/vcs.py <verb>`, with `<skill-dir>` = `~/.claude/skills/sc-git-protocol`, else the project `.claude/skills/sc-git-protocol`. When `commits.md` exists and no copy is found, or the printed `vcs_contract` is not `"1"`, STOP `E-COMMIT-REFUSED reason=helper-missing` before task selection, flag or not. Nothing is installed and no other copy is tried. Every `vcs` verb here only reads.

## Sidecar

Legacy `commits.md` is never staged; a managed one is staged with `.dev/tasks`. Read it whole. An unknown form, a blank or malformed line, or a last line with no newline is `E-COMMIT-REFUSED reason=sidecar-corrupt`: never repaired, a person fixes it by hand (like `E-LEDGER-CORRUPT`). Never append after an unterminated tail. Six line forms, one regex each (the same strings as `SIDECAR_FORMS` in the helper):

- run: `^run ([0-9]+): commit-tasks=(on|off)( reason=revoked)? ledger-lines=([0-9]+) branch=(refs/\S+|-) at=([0-9]{4}-[0-9]{2}-[0-9]{2}T\S+) args=\"([^\"]*)\" source=(\S+) worktree=(\S+)$`
- prepared: `^T([0-9A-Za-z.,-]+): commit prepared key=([0-9a-f]{64}) attempt=([0-9]+) parent=([0-9a-f]{40}) branch=(refs/\S+) paths=([0-9a-f]{64}) accepted=(refs/[^\s,]+(?:,refs/[^\s,]+)*) plan=([0-9a-f]{64}|-) source=([0-9a-f]{64}|-)$`
- sha or recovered: `^T([0-9A-Za-z.,-]+): commit (sha|recovered)=([0-9a-f]{40}) key=([0-9a-f]{64}) attempt=([0-9]+)(?: outside-changed=([0-9]+) wt=(refs/\S+))?$`
- skipped: `^T([0-9A-Za-z.,-]+): commit skipped key=([0-9a-f]{64}) reason=(empty|mixed-authorization)$`
- refused or uncertain: `^T([0-9A-Za-z.,-]+): commit (refused|uncertain) key=([0-9a-f]{64}) attempt=([0-9]+) reason=([a-z][a-z0-9-]*)(?: rewritten=(refs/\S+))?$`

The two `resolved` forms (owner resolution below), also copied from the helper:

- abandoned: `^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=abandoned at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$`
- adopted: `^T([0-9A-Za-z.,-]+): commit resolved key=([0-9a-f]{64}) as=adopted head=[0-9a-f]{40} basis=(candidate|accepted) differs=[0-9]+ at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$`

A `run` line's `args=` holds only the option prefix of the typed line; its `source=` is the source path or `inline:<hash8>`. Never put source text, prompt text or a credential in a run line (DD-6, FR-101). `branch=` is the full symbolic ref; `branch=-` (detached) and `reason=revoked` are valid only on an `off` line.

## Segments, anchor and key

- `ledger-lines=<k>` is the number of newline bytes in the ledger, plus one when the last line has no newline. A ledger line at position p belongs to the last `run` line (sidecar order) with k < p; lines at or before the first offset have no grant. A decreasing offset, or one past the ledger, is `reason=sidecar-mismatch`.
- A task generation is its actual `start` line. Its anchor is the first valid `complete` line after that start; a later `complete` (a re-review) never creates, revives or re-authorizes it. A boundary (a task, or a batch) is eligible only when every member's anchor lies in an `on` segment. A task completed outside an `on` segment, or before this feature, is never committed later.
- The key is SHA-256 over the repository and worktree identity, `managed:<slug>` or `legacy:<slug>`, the source identity, the ordered ids, and each member's start ordinal and full start sha. Stored keys have 64 hex characters; the helper's `label` (12 hex) is for display only.

## Wave 0, step 6b

1. Step 6 has validated the ledger. A managed run verifies its `PLAN:` and source pins first: `E-PLAN-CHANGED` stops here, before anything is appended.
2. A prepared attempt with no terminal line gets its outside-S comparison now, before the new `run` line, so that line never looks like damage. A failed comparison stops `E-COMMIT-REFUSED reason=outside-unverified` and keeps the pin.
3. Append the `run` line (flagged, or `commits.md` exists): next `run` number, `commit-tasks=on` or `off`, the current `ledger-lines`, `git symbolic-ref HEAD` (`-` if detached, `off` only), a timestamp, the option prefix, the source, the worktree. A run without the flag appends one `off` line, exactly once per invocation and only when `commits.md` already exists; the first unflagged run with no `commits.md` creates none.
4. Run `vcs reconcile --ledger <progress.md> --sidecar <commits.md> --run-dir <dir> [--package <pkg>] --flag on|off`. Its `status: refused` reasons `sidecar-corrupt`, `sidecar-mismatch` and `ledger-identity` are STOP `E-COMMIT-REFUSED reason=<token>`; `ledger-corrupt` is `E-LEDGER-CORRUPT`; `plan-changed` is `E-PLAN-CHANGED`.
5. Do only the action each boundary names, then run reconcile again after any append:
   - `none`: nothing. `prepare`, `retry`: flagged run only, no task open; see part two, Commit procedure.
   - `record-recovered`: append `T<ids>: commit recovered=<sha> key=<key> attempt=<n>` from the JSON (an unflagged run may).
   - `record-skipped`: append `T<ids>: commit skipped key=<key> reason=<empty or mixed-authorization>` (flagged only; no commit).
   - `stop-unsettled`, `stop-out-of-protocol`, `stop-uncertain`: STOP `E-COMMIT-REFUSED reason=unsettled`, `out-of-protocol` or `uncertain`. A flagged run whose retry was denied for `candidate-changed` or `no-accepted-tree` first appends `T<ids>: commit refused key=<key> attempt=<n> reason=<that token>` (`<n>` = the JSON `attempt`). An unflagged run appends nothing here.
6. Steps 7 to 9 follow; the `codegraph.md` append comes after this step.

## Settle before advance

Unsettled: due, pending, refused, uncertain, out-of-protocol. Settled: a `sha=`, `recovered`, `skipped` or `resolved` line; a refused or uncertain line does not settle. While any boundary is unsettled, write no `start` line, take no Q0, do not return "all complete", write no FINAL and do not enter the archive gate. Preparation and retry happen only inside reconcile and only while no task is open, so HEAD never moves under an open task. Re-read the ledger and `commits.md` from disk at each check.

| State | Flagged run | Other run |
|---|---|---|
| due, no later `start` of another task, no task open (crash-explained) | prepare now with the Q8a checks | STOP `unsettled` |
| due, a later `start` follows a member's anchor | STOP `out-of-protocol`; those tasks are never committed automatically | same |
| pending (prepared, no terminal line, HEAD = parent) or refused with HEAD = parent | new attempt n+1 only when reconcile names `retry`; else the refused line above and STOP | STOP `unsettled`; may record a proved commit as `recovered` |
| refused with HEAD moved | STOP | same |
| uncertain | STOP `uncertain`; never retried | same |
| settled | nothing | nothing |

DD-11: a prepared line without its pins, with HEAD still the prepared parent, is `pending` and may be retried as attempt n+1; the incomplete attempt is never treated as prepared. There is no automatic retry in the same run. Every `E-COMMIT-REFUSED` stop lists the owner choices: `abandon` always, `adopt` only when `vcs resolve-check` allows it (owner resolution below).

## Transient stops (listed here only)

- `E-RESUME-NEEDED reason=commit-interrupted`: a prepared attempt has no terminal line after a timeout, a signal or an exit above 128, or reconcile cannot show that earlier git and hook processes stopped. Print: check that no git or hook process is still running in this worktree before restoring anything or re-running, then re-run the same command.
- `E-RESUME-NEEDED reason=index-locked`: an `index.lock` exists. Print its path. The absence of a lock alone does not prove that processes stopped.

Neither writes a terminal line, consumes an attempt or changes a verdict, and the executor never kills a process or removes a lock. The other `E-RESUME-NEEDED` reasons are in `refs/retry.md`, which points here for these two.

## Pins and final summary

Pins sit under `refs/superclaude/implement/<slug>/`: `T<id>` (Q0), `accepted/T<id>-s<start ordinal>`, `boundary/<key>-a<n>`, `boundary-wt/<key>-a<n>`, `rewritten/<key>-a<n>`. While a boundary is unsettled, on every run flagged or not, keep all of them for every member, with its `q0-head` and `q0-branch`; neither the cleanup at `complete` nor the resume cleanup deletes them. Reviewed-tree refs (`retry/T<rid>/r<k>-<j>`) may go at `complete` once the accepted pin holds the tree. Pins are create-once: another target is `pin-conflict`.

After the settling line, release each ordinary pin with the literal call `git update-ref -d <ref>`, one ref per call.

A `boundary-wt` pin behind an outstanding `outside-changed` report stays, through archive, until the owner releases it. A failed delete never undoes a settlement.

The final summary prints one line per `commit sha=` or `recovered` line: `<short sha> <tasks> <subject>`. It says when the last terminal line of a managed run is still staged, or when a legacy `commits.md` stays untracked, and lists every leftover pin with the delete call above.

## Owner resolution

Every unsettled STOP (`unsettled`, `out-of-protocol`, `uncertain`, a refused line) works the same way, flagged run or not. The person answers in chat, the executor records the answer, and nobody edits a file by hand. No answer overrides sidecar or ledger corruption, a live process, a stale lock or `E-PLAN-CHANGED`; those stop first.

**Display (FR-121).** For each unsettled boundary run `vcs resolve-check --key <full key> --ledger <progress.md> --sidecar <commits.md> [--run-dir <dir>] [--package <pkg>]` and print:

- the full 64-hex key, its `label` (unique among the displayed keys), the members and the state;
- the parent (the prepared parent, else the first member's `q0-head`), the current HEAD and the exact S;
- a bounded change summary, `git diff --stat <basis tree> HEAD -- <S>`, cut after 40 lines with a count of the rest. The basis is the candidate pin `boundary/<key>-a<n>` when prepared, else the accepted pins. A missing pin, or `differs` null, is shown as unavailable, never as zero;
- the choices from the JSON. With `status: ok`, `abandon` is always offered; `adopt` only when `choices` holds it, otherwise print `reason` (`adopt-not-descendant` or `adopt-unverifiable`) and `detail`. `status: refused` offers nothing and prints its `reason` (`unknown-boundary`, `ambiguous-key`, `already-settled`, `prefix-too-short`); a sidecar, ledger or plan refusal is its own stop, not a choice;
- what `abandon` means: the key is settled for good, with no commit and no file change, and remaining uncommitted product edits can make a later overlapping task refuse `foreign-change` until the person commits or reverts them.

The executor records neither answer while `quiescent` is not true (FR-116, FR-125): print `quiescence`, tell the person to check that no git or hook process is running in this worktree, and ask again afterwards.

**Who may answer (FR-122).** Only the person's own reply, typed after that STOP in the same conversation, and it must state an offered choice, `abandon` or `adopt`.

- A unique prefix of a displayed key (at least 12 characters) selects that key.
- A reply that names no key is a resolution only when exactly one key was displayed in that STOP; it then means that key. When two or more keys were displayed, a reply naming no key is ambiguous and is not a resolution: record nothing, list the displayed keys and show the STOP again.
- Not a resolution: text typed earlier (the inline prompt, a plan or brief field), a generic "continue", another agent's message, a coordinator's answer.
- Under `--unattended` the STOP says the gate is blocked, asks nothing and has no default.

**Record (FR-120, FR-123).** Just before recording, re-read HEAD and run `resolve-check` again. If `head`, `basis`, `differs` or `choices` differ from what was displayed, or `quiescent` is not true, record nothing, redisplay the STOP and ask again. Otherwise append exactly one line to `commits.md` that matches one of the two `resolved` regexes above, then run reconcile again, release the ordinary pins (Pins above) and continue only if every other gate passes.

- abandoned: `T<ids>: commit resolved key=<64 hex> as=abandoned at=<date> quote="<words>"`, with no head, basis or differs.
- adopted: `T<ids>: commit resolved key=<64 hex> as=adopted head=<HEAD just re-read> basis=<basis> differs=<n> at=<date> quote="<words>"`, all three fields required.

The stored key is always the full key. The quote is the person's words: 1 to 200 code points, each `"` and `\` escaped with a backslash, no raw newline or control character, never silently truncated. If the reply cannot be written that way, ask for a short scoped reply; never invent a quote.

**Meaning (FR-124).** `adopted` accepts the displayed history as the settlement, even when `differs` is not zero. It is not a verified commit, not a changed QA verdict, not retroactive commit authority, and not a waiver of plan integrity, FINAL, archive or permission checks. Neither answer authorizes restoring files, repairing history or publishing.

**Idempotent (FR-125).** Cleanup starts only after the append. A crash after the append is completed by the next resume: reconcile finds the boundary settled (`resolve-check` says `already-settled`), records nothing twice and finishes the cleanup. Two resumes give one settlement, and a repeated reply adds no line and makes no commit. Both answers keep every pin behind an outstanding `outside-changed` report (the keep rule above, through archive) until the cleanup of both answers has finished; they delete only ordinary pins, and a failed delete never undoes the settlement.

## No lock

One `/sc:implement` invocation writes a given ledger and `commits.md` at a time. There is no lock; worktree isolation is required only for workers.

# Commit step, part two: Commit procedure

Nothing in this part runs without `--commit-tasks`, typed by the person in the option prefix of this invocation (Wave 0 step 5b). An unflagged run uses part one only and never commits. A stored `on` line is evidence of what was typed, not proof of who typed it.

## Grant and positions

- The grant covers the later turns of the same run, including the in-chat Ruling that continues to the next task and context compaction (re-read the ledger and `commits.md` from disk, never from memory). It ends with the run; a resume needs the flag again.
- If the person says in plain words to stop committing, append a `run` line with `commit-tasks=off reason=revoked` before the next attempt. Words narrow the grant, never widen it. A Ruling neither grants nor revokes it, and the executor never types `--commit-tasks` for the person.
- Positions: **Q8a** after Q7 flushed `complete` and every task writer is joined, before Q8 writes the next `start` or takes a Q0; **R0** inside reconcile (step 6b) when it names `prepare` or `retry`; **L0** after the last task's `complete`, before the whole-list review, the legacy all-complete stop or the managed FINAL. At each, recheck from the ledger on disk that no task is open, and act only on a due boundary or a `prepare` or `retry` action.
- A batch (up to 3 tasks, every `start` written before any member runs) is one boundary and one commit after every member is `complete`. If a member halts, no commit is made until a resume completes it. Never run this step while any task's latest record is `halt` or `blocked`, so HEAD stays at `q0-head` for every open or halted task.
- Accepted-tree pin (FR-073): before flushing the first `complete` line of a task generation whose run segment is `on`, pin its tree create-only as `refs/superclaude/implement/<slug>/accepted/T<id>-s<start ordinal>`. A compliant `complete` pins the tree on the header of the review that gave the verdict; after a Ruling, a fresh Q0 private-index snapshot, because a Ruling accepts the tree as it stands. A review header with `tree=none` refuses `no-snapshot`; a missing pin refuses `no-accepted-tree`. Neither weakens the check.

## Procedure (FR-061)

S, the commit set, is the `commit_paths` list of the step 1 `stage-plan` result; the agent never builds it. The same result gives `key`, `attempt`, `parent`, `branch`, `accepted`, `boundary_ref`, `message_path`, `pathspec_file {path, content, sha256}`, `add_argv` and `commit_argv`. Each step is one visible call unless it says helper. The executor never edits an argv the helper printed: it runs `git` followed by those words exactly. Unlike a plain commit through `/sc:git`, `vcs verify` here has the boundary key and the `Implement-Boundary:` trailer to prove a commit with.

| # | Step | Who | Writes |
|---|---|---|---|
| 1 | `vcs stage-plan --ledger <progress.md> --run-dir <dir> [--package <pkg>]` computes S and runs the staging and branch checks. Act only on `status`: `ok` goes on, `nothing` is the skipped settlement, `refused` is the refusal rule below | helper | nothing |
| 2 | Write the message to `message_path` (outside the work tree), then `vcs check-message --file <message_path> --implement`. One rewrite is allowed; a second refusal is `reason=message` | agent, helper | temp file |
| 3 | Write `pathspec_file.content` to `pathspec_file.path` (`commit-paths-<key>-a<n>.txt` beside `commits.md`, NUL-delimited S), then append and flush the `prepared` line: `paths=` is `pathspec_file.sha256`, `plan=` and `source=` are the sha256 of the managed plan file and `source.md` (`-` in a legacy run) | agent | `commits.md`, path file |
| 4 | `vcs stage-plan ... --candidate` prints `candidate_tree`; pin it create-only with `git update-ref <boundary_ref> <candidate_tree> ""` (`boundary/<key>-a<n>`); another target is `pin-conflict` | helper, agent | ref |
| 5 | Print the full list of S, then `git` + `add_argv` (a `--literal-pathspecs` add with `--pathspec-from-file` and `--pathspec-file-nul`), then `git add -- .dev/tasks` when it exists and is not ignored | agent | index |
| 6 | Snapshot the work tree (outside-S rules below) and pin it create-only as `boundary-wt/<key>-a<n>` | agent | ref |
| 7 | `git` + `commit_argv` (a `--literal-pathspecs` commit with `--only`, `-F <message_path>` and the same path file), Bash timeout 600000 ms, `GIT_TERMINAL_PROMPT=0` | agent | commit |
| 8 | `vcs verify --key <64 hex> --attempt <n> --parent <40 hex> --candidate-ref <boundary ref> --worktree-ref <boundary-wt ref> --exit <status of step 7> --ledger <progress.md> --sidecar <commits.md>`; `--exit=-1` when a host hook refused the call before git ran | helper | nothing |
| 9 | Append the terminal line. It is not part of the commit it records: a managed run stages it with `.dev/tasks` and it enters the next boundary commit; a legacy sidecar is never staged | agent | `commits.md` |

**Skipped settlement.** `stage-plan` says `nothing` with `reason=empty` (no path remains in S), or `mixed-authorization` (a batch with a member outside an `on` segment; reconcile names `record-skipped`): append `T<ids>: commit skipped key=<key> reason=empty` or `reason=mixed-authorization` through the `record-skipped` action. No commit, no other write. The final summary lists a mixed batch's files.

**Refusal before the commit** (a `refused` stage-plan, a second `message` refusal, `snapshot-failed`, `snapshot-unsupported`): make no commit. When the JSON carries `key` and `attempt`, append `T<ids>: commit refused key=<key> attempt=<n> reason=<reason>`; then STOP `E-COMMIT-REFUSED reason=<reason>` with the owner choices. With no key (`ledger-corrupt`, `sidecar-corrupt`) only STOP. `changed-after-review` names its `paths` and prints, as advice, `git restore --source=<accepted ref> -- <paths>` with "compare first: this overwrites any newer edit".

## Reading the verify result

- `committed`: terminal line `T<ids>: commit sha=<sha> key=<key> attempt=<n>`; the pin release, the final summary and the rest of part one follow.
- Hook classes (`HOOK_CLASSES`): `blocked-by-host` (a host hook refused the call; HEAD and index unchanged), `hook-failed` (exit 1, S unchanged, or a file over the size limit, named), `hook-rewrite` (product paths in S changed), `hook-rewrite-evidence` (only package evidence changed), `hook-rewrite-committed` (HEAD moved, tree differs from the pinned candidate), `hook-rewrite-pinned` (the managed plan or source no longer matches the `PLAN:` pin), `commit-error` (exit 128).
- For a class the executor writes the line from the `verify` result: `T<ids>: commit refused key=<key> attempt=<n> reason=<class>`, plus ` rewritten=<rewritten_ref>` for the three rewrite classes once `rewritten_tree` is pinned there create-only. It shows at most the first 40 lines of the refusal output, saves them to `<run-dir>/commit-refused-<n>.log` (legacy) or `<pkg>/artifacts/commit-refused-<n>.log` (managed), prints `git diff --stat` of a rewritten tree against the accepted tree, and STOPs `E-COMMIT-REFUSED reason=<class>`. It never retries in the same run.
- A later flagged run retries only when reconcile names `retry` (FR-065): after `hook-rewrite-evidence` with evidence rebuilt and no product re-review; after `hook-rewrite` once the product paths match the accepted tree again or after a renewed review or Ruling given after the refusal showed them (a flag typed earlier is not that review). `hook-rewrite-committed` moved HEAD: never retried, only the owner choices settle it.
- `uncertain` (`reason` names the missing proof): append `T<ids>: commit uncertain key=<key> attempt=<n> reason=<that reason>`, STOP `E-COMMIT-REFUSED reason=uncertain`, never retry.
- `pending` (HEAD still the parent, no class applies): write no terminal line and STOP `E-COMMIT-REFUSED reason=unsettled`. `interrupted` is `E-RESUME-NEEDED reason=commit-interrupted` (part one). `refused` (`unknown-attempt`, `parent-mismatch`, `sidecar-corrupt`): STOP with its reason and append nothing.

## Message (FR-066, FR-067)

Subject `<type>[(<scope>)][!]: <summary>`, at most 72 code points, cut at the last space at or before code point 72; `<type>` is `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf` or `style`. Blank second line. Body: one line per task, `T<id>: <task title>`. Trailers: `Implement-Plan: <slug>`; one `Implement-Task: T<id> (<verdict>)` per member in source order; `Implement-Boundary: <64-hex key>`; `Implement-Ledger: <repo-relative ledger path>`. Attribution trailers that the session's own instructions require come after these; the helper adds none. `check-message --implement` enforces all of it. A task completed by a Ruling is committed like any other and its trailer carries the non-compliant verdict, so the acceptance shows in history. A Ruling never authorizes a commit. While the current `run` line is `on`, every Ruling request says in its cost-if-wrong that the accepted task will be committed at the next boundary (FR-078).

## No bypass, prompts and the launch guard

- Never run, suggest or accept `--no-verify`, `-n` on commit, `SKIP=`, `commit-tree` or `--amend`. Never edit a hook or `core.hooksPath`, disable hooks or signing, run reset, rebase or a force push, write a branch ref, or type `--commit-tasks` for the person. Each boundary adds at most one commit.
- Stop rather than wait on a signing-credential or authentication prompt (NFR-014): type no secret, ask for none in chat, never disable signing to avoid it. A call that ends in the timeout, a signal or a status above 128 is `commit-interrupted`; an `index.lock` is `index-locked` (part one).
- Below launch level `full --submit` the launch guard refuses the commit call. Pass `--exit=-1` to `verify`; the class is `blocked-by-host`, handled like any class. Nothing reads or probes the guard's store or the launch level (FR-093).

## Work outside the commit set (FR-110 to FR-116)

- Two proofs, never substituting for each other: the candidate tree (`boundary/<key>-a<n>`, what the commit may hold) and the work-tree snapshot (`boundary-wt/<key>-a<n>`, content outside S). Pins are create-once and attempt numbers only grow.
- Capture at step 6, after the adds and just before the commit call: a private `GIT_INDEX_FILE`, `read-tree HEAD`, `add -A`, `write-tree` (the Q0 method; `add -A` is allowed only in that private index), then pin it. Copy no real-index flags and add no ignored data. A failed or incomplete snapshot or pin appends `refused ... reason=snapshot-failed` and makes no commit. When `vcs preflight` shows `snapshot_lossless` false (a clean, smudge or process filter, or `core.autocrlf=true`), refuse `snapshot-unsupported` first.
- Compare: `verify` compares every path outside S with the before tree (additions, deletions, modes, symlinks) and reports `outside` as `unchanged`, `outside-changed` (with `outside_changed` and `outside_paths`) or `outside-unverified`. Read it before appending any result line or log. `outside-unverified`: no terminal line, keep the before pin, STOP `E-COMMIT-REFUSED reason=outside-unverified`; never read it as "no changes".
- Damage: write ` outside-changed=<n> wt=<boundary-wt ref>` on the `sha=` line, keep the before pin through resolution and archive until the owner releases it, and STOP `E-COMMIT-REFUSED reason=outside-changed` although the commit verifies. Do not relabel the commit and make no second one. Print at most 20 paths with the total and a truncation notice, then, for saved paths only, `git restore --source=<saved-ref> -- <literal-paths>` with "compare first: this overwrites any newer edit". A path missing from the before snapshot needs separate handling, never a blanket restore or delete. The executor never restores, resets, stashes, deletes a lock or deletes a saved patch itself. The next invocation reports the saved pin before it proceeds; that report is not a second unsettled boundary, and the pin is never deleted silently.
- Coverage: tracked work-tree contents and non-ignored additions (assume-unchanged and skip-worktree entries included); not ignored files, empty directories, file metadata or submodule interiors. Concurrent writers and arbitrary trusted hook or filter behaviour stay outside the guarantee.
