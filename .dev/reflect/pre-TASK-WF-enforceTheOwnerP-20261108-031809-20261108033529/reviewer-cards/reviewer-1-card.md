# Tier-2 reviewer 1 (analyzer, sonnet): UC-1 audit of TASK-WF-enforceTheOwnerP-20261108-031809

<!-- Returned by reflect-reviewer (read-only), persisted by orchestrator on receipt 2026-11-08T03:46Z. Self-reported confidence 0.7. -->

Plan and source paths are relative to the repo root `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`.

## 1. best_practice_grade: 3/5

The plan covers the source scope, and the central deviation (Task 3 closes the plain tab instead of putting `--agent` on the claim's create) is documented and mostly justified. The grade is held down by thin Task 1 acceptance cases for the one piece the source calls deterministic enforcement, a timing race and unstated failure mode in Task 3, and an incomplete Task 4 edit list for `--pipeline none`.

## 2. Coverage verdict

| Source item | Verdict | Plan refs |
|---|---|---|
| (1) New hook (exit 0 / exit 2 / fail open, exact form printed, `--help` allowed) | Covered, with gaps (R1-1, R1-2) | Task 1 (:29-36) |
| (1) Register in `hooks.json` and the plugin mirror; install and unit tests | Covered | Task 2 (:38-47). Touchpoints confirmed: `install_hooks.py:85`, `hooks.json:86-95`, `test_install_hooks.py:102,760-793`, `test_cli_install.py:139`, `test_freshness_subagent_start_policy.py:112`. |
| (2) `/sc:issue`: agent comes with the create, keep `agent launch` only for existing worktrees | Covered by documented deviation | Constraints :20, Task 3 (:51-58), Task 5 (:71-80). D2/FO-18 updates replaced by "they stay" notes. |
| (2) Pending record before the agent starts | Covered | Constraints :20. Existing flow: `orca_worktree.py:941`, then `orca agent launch` at `:954`. |
| (3) `CLAUDE.md:307-324` and the bare example at `:320` | Covered, with gaps (R1-7) | Task 6 |
| (3) `core/CLAUDE.md` 45-53 and `ccsession-tag/README.md` 228-237; keep the 12 pinned phrases | Covered | Task 7. Ranges confirmed; appending leaves the 12 phrases in `test_orca_session_launch_guidance.py:17-30` intact. |
| Out of scope: WORKER-CONTRACT / WC-13, `worker-start`, any Orca change | Covered | Constraints :22. Minor tension in R1-10. |
| Out of scope: closing existing empty tabs | Covered, borderline | Task 3 closes only the plain tab of a newly created worktree (documented deviation). |
| Respect: Orca-only creation, no link flags | Covered | Constraints :23; Task 3 tests keep `NEVER_FLAGS`. |
| Respect: no hardcoded `src/superclaude/` paths in installed text | Covered | Task 7 acceptance :103 |
| Respect: `make sync-dev` + `make verify-sync` | Covered | Task 7 |
| Added by the plan: `--pipeline none` creates no worktree (Tasks 4, 5) | Not in the source; owner decision | Section 4 |

## 3. Findings

| id | sev | task | claim | evidence | recommended plan change | vs T1 |
|---|---|---|---|---|---|---|
| R1-1 | HIGH | 1 | The scanner cannot be copied as is: `endword` returns at `if (!need[o]) return` once the command word is set; it records only `cmd[o] = b` and prints and exits on the first python match; `sep()` resets per-command state. The hook needs per-command collection of `orca`'s arguments (`worktree`, `create`, `--agent`, `--help`), cleared at each separator, respecting wrappers, heredocs and subshells. Acceptance (:34) lacks `sudo orca …`, `env X=1 orca …`, `command orca …`, `orca … ; orca worktree create --agent x` (flag from one command satisfying another), `--agent` inside a `bash <<EOF` heredoc, `orca` after `|`. A naive implementation passes all 12 listed tests. | block-bare-python.sh:97, :106, :132-134 | State that the scanner is extended with per-command word collection; add wrapper, separator-isolation, heredoc-into-shell and pipe cases; add a "Known ceilings" header block like :48-61 (`bash -c`, `eval`, `xargs`, `claude --bare`, scripts calling orca, human shells). | Agrees F1 |
| R1-2 | MEDIUM | 1 | Matching rule under-specified: adjacency of `worktree create`, options between `orca` and `worktree` (global flags not checked), `--prompt "--agent"` falsely allowing after quote stripping, `orca worktree list --name create` falsely blocking under a loose reading. | plan Task 1 | State: `worktree` and `create` are the first two non-option arguments after `orca`; check orca global flags and test the result; add `orca worktree list --name create` (allow); record the `--prompt "--agent"` hole as a ceiling. | New |
| R1-3 | MEDIUM | 3 | Close-step timing race: create awaits `createTerminal`, but N8 shows the daemon session starting ~2.3 s after the create call began; the seeded terminal may not be listed when create returns. Count 0 gives a one-shot warning and leaves the plain tab. | runtime-local-worktree-terminal-startup.ts:209-210; tier1-observation.md:116, :121 | For count 0, bounded re-list (e.g. 3 tries over ~5 s) before warning; make the Task 8 live `/sc:issue --claim` check a ship gate. | Extends F5 |
| R1-4 | MEDIUM | 3 | Reply handling: current code never parses `created.out`; a timed-out create has no reply; reply is an envelope so `setup`/`defaultTabs` sit under `result`; `setup` is reported only when not spawned, and the setup branch creates no plain seed. | orca_worktree.py:594-613, :611, :628; test_issue_orca_worktree.py:970; startup.ts:187-201, :215-222 | Read `result.setup`/`result.defaultTabs`; unparseable/missing reply or timed-out create → `W-FIRST-TAB-LEFT`, no close; tests for both. | Agrees F5 |
| R1-5 | LOW | 3 | `terminal close --terminal` without `--tab` closes the whole tab only when it is the last pane; `--tab` is the explicit form and waits for durable persistence. `agentIdentity` is absent when unknown, not "empty". | explicit-terminal-close-stops.ts:226, :246-249; help.ts:88-89; terminal-close.ts:12-13; runtime-terminal-contracts.ts:38-39 | Choose `--tab` deliberately and pin it in the FO-18 call list; say "absent or empty"; fakes omit the key. | New |
| R1-6 | MEDIUM | 4 | `--pipeline none` edit set incomplete; acceptance grep (:68) checks one phrase. Unnamed stale statements: `claim.md:93` ("run Wave 7, then Wave 8"), `claim.md:131, :136` (Final output "Worktree: <path>", "Open <wt> and run next-steps there"), `SKILL.md` :17, :89, :92, :150, :170, `issue.md:64`. (:17/:89/:92 are leads; lines truncated in grep.) | as cited | List those lines; acceptance grep for "create or reuse the Orca worktree" and "Open <wt>"; test that Final output item 1 has a no-worktree branch. | New |
| R1-7 | MEDIUM | 6 | `CLAUDE.md:305` "give each session its own worktree" and `:333-337` Usage contradict "no session creates a worktree for its own use"; Task 6 touches only :307-324. | CLAUDE.md:305, :333-337 | Add both to Task 6 and the new tests/core assertion. | Agrees F4 |
| R1-8 | MEDIUM | 3, 5 | Failed claim launch (`W-LAUNCH-FAILED`) leaves a worktree with no agent and, after Task 3, no tab. Not named or accepted. | orca_worktree.py:954-975; claim.md:123 | Constraint accepting it, pointing at the re-run remedy; mention in Task 5 note. | Agrees F6 |
| R1-9 | LOW | 3 | Module docstring says the script runs only listed commands ("no link flag, no agent flag"); Task 3 adds `terminal list`/`terminal close` without updating it. Existing created-worktree tests may see unlisted fake calls (fixture not read). | orca_worktree.py:20-30 | Add the docstring and fake-orca `terminal-list`/`terminal-close` responders to Task 3. | New |
| R1-10 | LOW | 7 | New paragraph ("the session that creates a worktree becomes its orchestrator") conflicts for workers with WC-13, which forbids `worktree create --agent` from a worker session. | WORKER-CONTRACT.md:62 | Add "unless the session is a supervised worker (see its contract)", or note the tension in the delivery file. | New |
| R1-11 | LOW | 1, 6, 7 | Only the `--agent` half is deterministic; "no own-use" and "human-created worktree needs an agent" stay instruction-only. Constraints :19 presents both as enforced. | plan :19 | Say in Constraints that only the `--agent` requirement is enforced. | New |
| R1-12 | LOW | 8 | Humans, Codex/other agents, `claude --bare`, shell scripts calling orca are not covered; the hook takes effect only after `superclaude update`. | block-bare-python.sh:61 | "Not covered" section in `t8-delivery.md`; word CLAUDE.md "once the hook is installed". | Agrees F10 |
| R1-13 | LOW | 2 | `launch-job-identity.sh` rewrites the whole input via `updatedInput`; ordering of other hooks unspecified. Same-matcher hooks seeing the original command is unverified. | launch-job-identity.sh:14-15 | Require Claude Code hook-doc evidence (context7) in `t2-launch-identity-interaction.md`. | New |

No refutations of T1. F1, F4, F5, F6, F10 confirmed. INF-014/015 covered only through the Constraints deviation (confirmed). Task 3 line ranges `:594-613`, `:614-640` match the code.

## 4. Deviation classification

| Departure | Class | Reason |
|---|---|---|
| /sc:issue keeps create → copy → `agent launch` (plan :20) | Necessary deviation | `finish()` fails the claim on copy error (`orca_worktree.py:521-524`); `cmd_launch` refuses a stale `launch-prompt.md` (`:934-936`); the prompt reads a path inside the worktree (`:950`). An agent started by `create --agent` would run before those checks. The plan should name this as the real constraint; the pending record only needs a nonce. |
| First-tab close in `cmd_worktree` (Task 3) | Necessary deviation | Only way to meet the intent under the deviation above; limited to new worktrees with one agentless terminal. Hazards R1-3, R1-8. |
| D2 and FO-18 stay with dated notes (Task 5) | Necessary deviation | Follows from the deviation above. |
| `--pipeline none` creates no worktree (Tasks 4, 5) | Authorized expansion | Source silent; otherwise `none` would create an agentless worktree. Owner decision cited at Constraints :19 (not verifiable from files). |
| Human-created and creator-owns rules in instruction text (Tasks 6, 7) | Authorized expansion | Source states ownership; human clause is instruction-only (R1-11). |
| Task 2 interaction check | Authorized expansion | Keeps enforcement deterministic. |
| `t8-delivery.md` operator steps | Authorized expansion | Packaging. |
| No Drift or Regression found. | | |

## 5. Confidence and unverified items

Self-reported confidence: 0.7.

Unverified: installed Orca binary (1.4.245-aidev02) vs local IronOrca checkout (HEAD dc57b3d6e8); whether `terminal list` shows the seed when create returns (R1-3); orca global flags (R1-2); same-matcher PreToolUse input ordering (R1-13); `fake_orca` defaults (R1-9); owner decisions; truncated SKILL.md :17/:89/:92 (R1-6); the T1 card file itself, REPORT.md, and test line numbers in Tasks 3/4 (:794, :336-370).
