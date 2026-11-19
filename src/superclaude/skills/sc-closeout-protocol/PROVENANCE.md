# sc-closeout-protocol: Provenance of the adopted files

This skill adopts and adapts two files written by Jay Wedgeworth, used with the owner's approval. This file records the source, the pinned commits and hashes, the licence, and what was changed in each part of each file. The Apache License text is kept verbatim in `LICENSE` in this folder, and the root `NOTICE` lists the component.

## 1. Source

| Field | Value |
|---|---|
| Upstream repository | https://github.com/Simple-With-Us/AI-Fleet-Coordinator |
| Author and copyright | Jay Wedgeworth, Copyright 2026 Jay Wedgeworth |
| Licence | Apache License, Version 2.0 (Apache-2.0); text kept verbatim in `LICENSE` in this folder |
| Upstream NOTICE file | none (the repository has no `NOTICE` file, so there is nothing to carry under section 4(d) of the licence) |
| Date adopted | 2026-11-19 |
| Fetched automatically later | never; a drift review compares the pins below by hand |

| Upstream file | Lines | Git blob | Last commit | Last changed | Where it went |
|---|---|---|---|---|---|
| `skills/closeout/SKILL.md` | 110 | `905bfbe5b670b1ebcb22c2e6ee16e189c6b13410` | `ec86182d70d5a77410774392439090f1e36ca367` | 2026-11-05 | `SKILL.md` in this folder |
| `scripts/branch-landed.sh` | 85 | `d18608c2a5f51419fd7e0bbc641a6d31b2c92fcf` | `b7f695084cc27e8cc5b424d957fbd684d176d7cd` | 2026-09-17 | `scripts/branch-landed.sh` in this folder |
| `LICENSE` | 190 | `4b14cf3c9bae0ab156f3979e3e5d0048be2f7e23` | not recorded | not recorded | `LICENSE` in this folder, byte for byte |

Files in this folder that are new and not derived from Jay Wedgeworth's files (`scripts/settle.sh`, the templates, `refs/`, `scripts/deny-names.txt`, and the command file) carry no notice from him.

## 2. Notices in the adopted files

| File | Notice |
|---|---|
| `scripts/branch-landed.sh` | a five-line comment after the shebang: source, commit `b7f695084c`, copyright, Apache License, Version 2.0, what IronClaude changed, pointer to this file |
| `SKILL.md` | a two-line visible quotation directly under the title: source, commit `ec86182d70`, copyright, licence, and "Changed by IronClaude: see `PROVENANCE.md`" |
| `LICENSE` | the licence text, verbatim |

## 3. What changed

Each upstream element has one row. The label is one of three words. `kept as is` means the text or logic carries over unchanged, except for the dash and spelling rules of this repository. `changed` means only the part that this setup needs is different, or the text itself changed. `dropped` means it names a surface this setup does not have or a step the issue does not ask for. The "Lines" column holds the upstream line numbers.

### 3.1 `skills/closeout/SKILL.md`

| Lines | Upstream element | Label | What happens here, and why |
|---|---|---|---|
| 1-4 | Frontmatter: `name: closeout`; description; "Never silently walk away from In Progress" | changed | The name is `sc:closeout-protocol` and an `allowed-tools` line is added. The description names the three items. The last sentence becomes "Never leave an item silently in progress", because "In Progress" is a Linear status and this setup has no board. |
| 6-8 | Title "Closeout (Universal)" and the opening paragraph | changed | Same idea with these surfaces: the end of work is the issue, the work report entry, the worker's task and the pull request that links the issue. |
| 10-12 | `## 1. Truth check`, first bullet: merged to `main`? no commit ancestry after a squash merge; use pull request state, then a three-dot diff | changed | The rule is kept (no ancestry after a squash, state first, then a three-dot diff). The text changes: the branch name `main` becomes the pull request's base branch. |
| 14-19 | Code block: MCP pull request listing, fetch, three-dot diff, helper `branch-landed.sh [repo] [branch]` | changed | A pull request view by number replaces the MCP tool; the fetch stays; the three-dot diff uses the base the pull request names and the head GitHub kept at `refs/pull/<N>/head`, because a person who runs this has no lane whose `HEAD` is the branch; the helper takes `<PR>`. |
| 21 | Two-dot diff on a stale lane is "actively misleading"; ancestry is correct only for "does this exact SHA exist on live/main" | changed | The two-dot warning is kept as is and is a Will Not Do. The ancestry exception is dropped: this version writes no deploy claim, so nothing needs it. |
| 22 | "Production verified? (`deploy-verify`) Completed is not Deployed" | changed | Kept in meaning: two words, two meanings. The `deploy-verify` skill is Jay Wedgeworth's and is not adopted. |
| 23 | "Uncommitted files? Commit or explicitly report why not" | dropped | This skill starts after a merge from any checkout and never touches a worker's worktree. |
| 25-30 | `## 2. Linear`: `linear_status` and `linear_comment` "Landed in #<PR>. <one line>." | changed | The GitHub issue replaces the Linear issue: one note, then a close with the reason completed. Only "completed" is written. The note keeps the shape "Landed in <PR>" plus one line, and adds who merged. |
| 32 | `Fixes <ID>` moves the issue to Done on merge; `Refs <ID>` never closes it; seat-verified writes | changed | The link is read as data (`closing`, `refs` or `none`) and decides nothing: a model decides whether the issue is done, and only a `done` verdict closes it. The seat and bearer rules are dropped; every write is made as the person's own `gh` login. "Safe to repeat" is kept. |
| 34-35 | "Completed = merged to main. Deployed = released and verified (say how)." | changed | The two fixed meanings are kept: completed means merged, and deployed means verified in the place it runs. The branch name `main` is not used and the text is reworded; this version never writes the word "deployed". |
| 36 | Correct a wrong status with a new comment or status, never by editing another seat's comment | kept as is | Becomes a Will Not Do: the skill never edits or deletes any comment or any other text on GitHub. |
| 38 | Every imported GitHub issue has a Linear twin; close the Linear one | dropped | There is no twin. The GitHub issue is the issue. |
| 40 | No effort log to update | dropped | No such log. |
| 42-44 | `## 3. The PR`: the body names the issue; branch name `<seat>/<id>-<slug>`; say which keyword you used | changed | The body link is checked and printed; the note and the result say which kind it was. The branch naming rule is dropped. |
| 46 | Pull request writes only through `git-relay` and its MCP tools; a personal `gh` credential is not the route | dropped | The opposite holds here: every write is a `gh` call that names `--repo <R>`, as the fork rule requires. |
| 48-58 | `## 4. Zulip` | dropped | No Zulip. Notices to ClickUp are not part of this skill. |
| 60-62 | `## 5. Apple Notes` | dropped | The work report entry takes its place as its own item. That item is new: neither of Jay Wedgeworth's files has it. |
| 64-68 | `## 6. Mac local processes` | dropped | No such inventory. |
| 70-79 | `## 7. Retire the lane` | dropped | The orchestrator leaves the worktree in place and never removes one. Not asked for in the issue. |
| 81-83 | `## 8. Default-off features` | dropped | No enablement backlog. |
| 85-87 | `## Parked, not done` | dropped | The skill is limited to merged pull requests. For any other verdict it stops, writes nothing and says why. Its principle, never silently in progress, stays. |
| 89-97 | `## Fleet recall (every closeout)` | dropped | Jay Wedgeworth's own memory service. |
| 99-103 | `## Canon` | changed | A short pointer list to this skill's own files. |
| 105-110 | `## Living Handoff Morphing to Closeout` | dropped | The orchestrator keeps the report as a living document, and pickup of another seat's work is not needed. |

### 3.2 `scripts/branch-landed.sh`

| Lines | Upstream part | Label | What happens here, and why |
|---|---|---|---|
| 1-18 | Header comment: purpose, why ancestry lies after a squash with branch deletion, usage, five tokens, "Exit 0 only for MERGED", two-dot warning | changed | The purpose, the "ancestry lies" reason, the five tokens, "exit 0 only for MERGED" and the two-dot warning stay. The usage line becomes `branch-landed.sh <PR>`. The incident dates and the board id in lines 5-8 are Jay Wedgeworth's own references and are dropped. The notice block is added at the top. |
| 19 | `set -euo pipefail` | changed | `set -u -o pipefail`, so a failed call cannot exit before the one stdout line is printed. |
| 21-27 | Arguments: repo path (default `.`), branch (default the current branch) | changed | One argument, the pull request number or URL; the checkout is always the current directory. A branch is not needed because the number names exactly one pull request. |
| 29-32 | Detached-`HEAD` guard | dropped | No branch is read. A missing or bad argument prints `UNKNOWN reason=usage`. |
| 34-45 | Parse `origin` into `owner/repo` | changed | The same parse (it strips `.git`, `git@github.com:`, `https://github.com/` and `ssh://git@github.com/`), with the text adapted. A URL argument for another repo is refused. A failed parse prints `UNKNOWN reason=no_origin`, one stdout line instead of a stderr line. |
| 47-48 | Pull request listing by head branch, errors swallowed | changed | A pull request view by number with the extra fields the settle steps need. Errors are no longer swallowed: "no such pull request" is `NONE`, any other failure is `UNKNOWN`. |
| 50-63 | Embedded `python3`: parse the JSON, treat bad JSON as no pull request, `NONE` with exit 3 | changed | `jq` replaces `python3`. Bad JSON is `UNKNOWN reason=bad_json`, not `NONE`, because "I could not read it" and "there is none" are different facts. |
| 64-66 | Prefer a merged pull request when several share a head | dropped | A pull request number names one pull request. |
| 67-78 | Map state: MERGED exit 0; OPEN exit 1; anything else `CLOSED` exit 4 | changed | Same tokens and the same exit codes (0, 1, 4); the output line gains key=value fields, so the text changes. |
| 79-80 | Capture the heredoc's exit status | dropped | No heredoc. |
| 82-84 | Print the three-dot diffstat of `<origin/HEAD>...HEAD` as evidence for a person | changed | Still evidence only, and never part of the verdict. It becomes the held-versus-merged comparison, printed as one `match=` field. |
| 85 | `exit "$status"` | kept as is | The exit code equals the verdict. |

## 4. What this version adds

Only what the issue asks for: `scripts/settle.sh` (the three settle steps, the evidence read and the check), the templates, the refs, `scripts/deny-names.txt`, the done-check by a model's judgment, the command file, the never-as-worker entry, the registration edits and the tests.

## 5. Drift review

Nothing is fetched automatically. To review drift, read the two upstream files at the commits above and compare them with the "Where it went" files by the rows in section 3. A later pin updates the table in section 1 in the same change that updates the adopted file.
