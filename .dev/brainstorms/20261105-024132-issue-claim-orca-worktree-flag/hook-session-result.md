# Result: launch-level enforcement hook spec (issue #394)

Written 2026-11-05 by the hook-launch-level-394 session.

## Status: partial

All four steps of the brief ran: brainstorm, design, commit and push, issue comment. The deliverable exists and is pushed, but the spec is a DRAFT THAT IS NOT APPROVED: the final plan review failed, and the owner stopped review rounds, so the last amendments were never re-reviewed. No hook code was written (design only, as the brief says). No PR was opened and `/sc:pr-submit` was not run.

| Item | Value |
|---|---|
| Branch | `ironbelly/hook-launch-level-394` (pushed to `origin`, tracking set) |
| Commit | `9aa7b4f9168a9d5e4ab56a5ae1d81aaaa63227d8` (`docs(hook): spec for the launch-level enforcement hook (#394)`, 28 files, 8,261 lines added) |
| Issue comment | https://github.com/IronbellyOrg/IronClaude/issues/394#issuecomment-6671207777 (starts with `<!-- sc:hook-spec -->`, full spec inside a details block, 47,188 characters; issue body, state and labels untouched) |
| Design doc | `docs/designs/sc-issue-launch-level-hook.md` in the worktree `/home/coder/workspaces/worktrees/IronClaude/hook-launch-level-394` (43,862 characters, 18 sections) |
| Spec link | https://github.com/IronbellyOrg/IronClaude/blob/ironbelly/hook-launch-level-394/docs/designs/sc-issue-launch-level-hook.md |
| Brainstorm folder | `.dev/brainstorms/20261105-170229-launch-level-hook/` in the same worktree (committed) |
| Requirements document | `.dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md` (66 requirements FR-L-01 to FR-L-66) |

## Brainstorm contract

- Adversarial status: **partial**. Brainstorm status: partial.
- Convergence score: **1.00** by the protocol rule (44 of 44 diff points and shared assumptions agreed, counting a 2-of-3 majority as agreement). Counting only identical verdicts it is **0.70** (31 of 44).
- The convergence gate was blocked by the invariant probe: 40 findings, 22 HIGH and unaddressed during the debate. Each got a planned change or owner decision afterwards, but none was debated.
- Scores: Variant 1 (opus architect) 0.911, Variant 2 (sonnet refactorer) 0.911, Variant 3 (haiku QA) 0.837. Variant 1 was the base by the debate tiebreaker, 7 points to 4.
- Plan reviews: three reviews, two fix cycles. Review 1 failed with 8 blocking findings, review 2 with 8, review 3 with 10. The owner then ordered no more review rounds; no fourth review was run. The 10 findings of review 3 are applied in the spec as amendments, marked unreviewed, and listed as OPEN.
- Acceptance criteria as the final review judged the plan: AC-1, AC-2, AC-3, AC-5, AC-6 NOT MET; AC-4 and AC-8 MET WITH CAVEAT; AC-7 MET.
- Contracts on disk: `.dev/brainstorms/20261105-170229-launch-level-hook/return-contract.yaml` and `.../adversarial/adversarial/return-contract.yaml`.

## What I could not do, and why

- **No review of the final amendments** (owner decision, 2026-11-05). The spec says so in its front matter and banner.
- **No hook code, no real launch.** Every UNVERIFIED item below needs a real `orca agent launch` session; the spec makes the first observed check (OB-H1) the gate.
- **Hook behaviour I could not read from the official docs** (the page's last 86 KB and the `Skill` tool input keys were not found): see U1 to U8 below.
- **The Markdown was not rendered on GitHub**; the comment's tables and details block are unchecked visually.
- **The design doc was copied by hand from the requirements document** by an agent. Run a diff of its regexes and rule text against `merged-requirements.md` before implementing.
- **Not run:** the 142-row attack and benign corpus against any real script (the reviewers ran prototypes in /tmp, since deleted); `gh` against GitHub (stubs only); BSD `sed`.
- This result file is written in the main checkout because the brief names that path; it is not staged or committed.
- One harness note: the diff-analysis agent's reply was flagged by the harness for mentioning `settings.json` (an instruction-shaped pattern). It was a finding about a tamper route, not an instruction, and nothing acted on it.
- A typo in the design-writer prompt (`worktrines`) was followed by the correct path; the agent verified every repository path it named.

## Checked by me during the run (VERIFIED)

- A PreToolUse exit 2 blocked `python3 --version` in this bypassPermissions session (so blocks hold with permission prompts off).
- Real skill names are `sc:implement-protocol`, `sc:pr-submit-protocol`, `task`, `sc:task-protocol` (the earlier variants used `sc-implement-protocol`).
- git 2.47.3: an alias set through `--config-env` or `GIT_CONFIG_COUNT` commits; `git -c remote.origin.push=...` sends a push to remote `main`; `--attr-source` takes a separate value; bash pattern substitution takes 1.6 s on 100 KB while `tr` takes 4 ms.

## Open decisions (copied from the spec, section 15)

## 15. Open decisions

### 15.1 Owner decisions O-1 to O-22 (default is in force)

| Id | Question | Default | Alternative |
|---|---|---|---|
| O-22 | add a structural git-level layer (L2, `pre-push` per worktree refusing `main`, `master`)? | orchestrator: yes as step 7a, text layer kept; owner decides; open: install place (U28), hook chaining, removal, tests | text classifier only (R1) |
| O-21 | quoted-text over-match | accept; LL-TEXT; OB-H3 counts | drop `am` after OB-H3 |
| O-1 | `cwd` check at bind | no | mismatch binds `degraded` |
| O-2 | `--force` at `FS` | blocked | admit `--force-with-lease` |
| O-3 | `gh pr ready` | SUBMIT | never |
| O-4 | UserPromptExpansion | no | exact `command_name` |
| O-5 | issue number in header | no | store it |
| O-6 | approval lifetime | session | expire or bind to plan |
| O-7 | built names and scripts uncovered | accept | `$` in command position is UNKNOWN; or O-22 |
| O-8 | gate source edits at `W` | no | `.dev/` only |
| O-9 | subagent id differs | stop | reserve `cwd` fallback |
| O-10 | sync merge at `FS` | blocked | allow `--no-commit`, `--abort` |
| O-11 | Orca worker commands | none | allowlist them |
| O-12 | compare `--repo` to `origin` | no | read at bind |
| O-13 | more IMPL skills | no | add names |
| O-14 | MCP writes at `FS` | blocked | allow non-`main` |
| O-15 | old state files | person removes | prune on re-claim |
| O-16 | deleted file is ordinary | accept | read `transcript_path` (U27) |
| O-17 | self-started turns | allowed | block at `W` |
| O-18 | compound push at `FS` | blocked | widen form |
| O-19 | non-canonical `gh api` | blocked | admit GET variants |
| O-20 | strict marker, no record | block prompt | ignore |

### 15.2 Blocking findings of the three plan reviews

Status as in MR 11.2 (which names the confirming review). Default for all: keep the rule now in force.

| Id | Finding | Rule now | Status | Alternative |
|---|---|---|---|---|
| OD-R1-B1 | backtick hid a refspec to `main` | FR-L-33 | closed | reopen if T-PSH-12 fails |
| OD-R1-B2 | backslash-newline split a push | FR-L-33, FR-L-25 | closed | reopen if T-NRM-5 fails |
| OD-R1-B3 | dashed built-ins unseen | FR-L-28 | closed | reopen if T-GIT-12 fails |
| OD-R1-B4 | `gh api` writes read as reads | FR-L-36 | closed | O-19 |
| OD-R1-B5 | normalisation unnamed, boundaries lost | FR-L-25 to 27 | closed | none |
| OD-R1-B6 | background subagent turns uncovered | FR-L-19, O-17 | closed | O-17 alternative |
| OD-R1-B7 | deleted file ordinary, unstated | FR-L-56, R3 | closed | O-16 alternative |
| OD-R1-B8 | false "messages pass" claim | FR-L-29, R8 | closed | O-21 alternative |
| OD-R2-F1 | nested alias pushed to `main` | G1, G2, G4 | closed | none |
| OD-R2-F2 | option after `origin` moved `main` | FR-L-33 | closed | none |
| OD-R2-F3 | shell-built `gh api` flag | FR-L-36 | closed | O-19 |
| OD-R2-F4 | `rm -rf ~/.claude/state` allowed | FR-L-49, R3 | fixed in a fix cycle but NOT confirmed by any later review | O-16 alternative |
| OD-R2-F5 | `$GIT push` gap unstated | R1, O-7 | fixed in a fix cycle but NOT confirmed by any later review | O-7 (a), O-22 |
| OD-R2-F6 | quoted `>` deleted git word | FR-L-26, 27 | closed | none |
| OD-R2-F7 | quoted value shifted subcommand | G1 | closed | none |
| OD-R2-F8 | PR title blocked as git | FR-L-31, 37 | closed | none |
| OD-R3-B1 | in-word continuation hides names | FR-L-24 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B2 | `$''` splices hide words | FR-L-25 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B3 | hidden command position, `send-pack`, redirects, gh merges | FR-L-28 to 31, 37 | OPEN (amended, not re-reviewed) | drop; O-22 |
| OD-R3-B4 | `~/.config/git/config` redirect | FR-L-49 | OPEN (amended, not re-reviewed) | drop; R11 |
| OD-R3-B5 | glob and brace spellings unlisted | R1, R3, T-GAP-1 | OPEN (amended, not re-reviewed) | O-22 (push part) |
| OD-R3-B6 | segment split skipped | FR-L-27 | OPEN (amended, not re-reviewed) | none |
| OD-R3-B7 | `curl` PATCH moves `main` | FR-L-39 | OPEN (amended, not re-reviewed) | drop; R10 |
| OD-R3-B8 | versioned `npx` Claude Code | FR-L-48 | OPEN (amended, not re-reviewed) | drop; R5 |
| OD-R3-B9 | reinstall by module name | FR-L-50 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B10 | `/sc:implement` retry block UNKNOWN | FR-L-31 | OPEN (amended, not re-reviewed) | drop; AC-2 breaks |

Counts: 26; 14 closed, 2 fixed but not confirmed, 10 open.


## UNVERIFIED items and residual risks (copied from the spec, section 16)

## 16. Residual risks and UNVERIFIED items

| R | Not stopped | Tolerated by |
|---|---|---|
| R1 | scripts; names from variables, escapes, globs | pinned allow; O-7, O-22 |
| R2 | timeout or crash allows | 1 s budget at 5 s |
| R3 | indirect store delete | direct names TAMPER; O-16 |
| R4 | person's bypass flags | person's choice; IR-4 |
| R5 | `claude` started without tmux | terminal tools ESCAPE |
| R6 | malformed late marker | OB-H2 |
| R7 | startup-file alias | accepted |
| R8 | over-blocks (a) to (i) | LL-TEXT; O-21 |
| R9 | local plumbing commits | local only |
| R10 | GitHub writes by programs, unmatched MCP | `curl` GHWRITE |
| R11 | pre-set push config | agent cannot set one |
| R12 | hostile agent | out of scope |
| R13 | person pastes a marker | `rm` releases |
| R14 | U1 or U8 false, checks skipped | OB gates |
| R15 | other session types `approved` | agent cannot |
| R16 | bare self-started turn | OB-H1 5; O-17 |
| R17 | aliases from non-tamper config | needs setup first |

UNVERIFIED (MR 12): U1 subagent id (ship gate); U2 Skill key; U3 `Task` name; U4 turn wrapping; U5 queued prompt; U6 `--bare`; U7 Orca preamble; U8 bind timing (OB-H2 mandatory); U9 `command_name` (moot); U10 `/sc:implement` git use; U11 Monitor fields; U12 MCP names; U13 `isolation` key; U14 `claude` without `-p`; U15 matcher anchors (names re-checked); U16 push options (moot); U17 subagent prompts (ignored); U18 `/clear` id; U19 `/` escapes (moot); U20 blocked prompt visible; U21 tool names; U22 BSD tools (T-NRM-6); U23 `send-pack` https (moot); U24 gh alias (R17); U25 `orca -h`; U26 tmux pane; U27 `transcript_path`; U28 Orca hooks (O-22).

