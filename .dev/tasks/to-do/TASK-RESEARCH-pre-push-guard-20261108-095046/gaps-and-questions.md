# Gaps and Questions: git pre-push hook semantics for the L2 guard

- Compiled: 2026-11-08 (Step 3.4, after Gate 1 PASS at cycle 0)
- Sources: research files 01-04 (Gaps and Questions, Stale Documentation Found), `qa/analyst-completeness-report.md`, `qa/qa-research-gate-report.md`, `qa/qa-research-qualitative-report.md`, `qa/qa-consolidated-findings-phase3-cycle0.md` (B1-B4, N1-N24), `qa/qa-research-fix-log.md`, `qa/qa-research-fix-verification-cycle0.md` (M1-M4), `qa/qa-research-fix-verification-qualitative-cycle0.md` (N-1 to N-4).
- Duplicates are merged; the Source column names every place a gap appears. Nothing here is new evidence.

## Gap table

| ID | Gap or question | Severity | Source (file and section) | Status | Suggested resolution |
|---|---|---|---|---|---|
| G-1 | Do API/programmatic ref writes (hosting-service ref API, `gh api`, curl to smart-HTTP `git-receive-pack`) bypass the local pre-push hook? (design line 520, D19-30 API part) | Important | 04 Gaps (`ROUTE web-01: D19-30`); 03 Gaps D19-30; 04 Step 2.5 table | open | web-01 |
| G-2 | Do pygit2/libgit2, dulwich, GitPython and JGit run the client-side pre-push hook, and from which hooks dir? (sub-question (b) "other tools") | Important | Consolidated B2; 04 Gaps (`ROUTE web-01: (b) other tools`); 02 Gap 6 and line 190; research-notes line 73 | routed in Gate 1 (B2 fixed by routing); answer open | web-01 |
| G-3 | Git version that introduced each behaviour: pre-push and `--no-verify` (hint 1.8.2), `core.hooksPath` (2.9.0), `git worktree` (2.5), `extensions.worktreeConfig` (2.20), `git hook run` (2.36); any change up to 2.47.3 (hook.c) | Important | Research question (f); research-notes web-01 scope; analyst m-14 (N14) | open | web-01 |
| G-4 | Linux no-replace publication: `link(2)` EEXIST, `O_EXCL`, `O_TMPFILE`+`linkat`, `rename` replaces, `renameat2 RENAME_NOREPLACE` kernel/fs support; compare with `publish()` in launch-job-identity.sh lines 164-174 | Important | Research question (e); 01 Summary (`publish()` pattern); analyst m-14 (N14) | open | web-02 |
| G-5 | Git's hook executable check (`find_hook`, `access(X_OK)`, `advice.ignoredHook`) in v2.47.3 source, explaining the fail-open in E29 | Important | Research question (e); 04 E29 and Key Takeaways; 04 open question (E29/E31) | open | web-02 |
| G-6 | Human whose PATH lacks uv: `identify` exits 2 (lines 25, 52-53, 566), mapped to `unknown`, so the human cannot push to main/master; absolute uv path is not enough. Options: fixed PATH with install-time uv dir, hook-side no-store exit, pure-shell hook | Important | Consolidated B4; 01 §4 item 5 (lines 195-196), 01 Gaps 1; 04 E28c, line 1530, open question line 2259 | resolved in Gate 1 (documented); design choice open | brainstorm decision |
| G-7 | "No verdict" (exit 2) mapping to `unknown` is not written in the design | Important | 01 Gaps 1 | open | brainstorm decision |
| G-8 | Install-integrity holes a same-user agent can open with no push flag: clearing the exec bit (fail-open, hint silenced by `-c advice.ignoredHook=false`, E29) and per-worktree `core.hooksPath` via `extensions.worktreeConfig` (E31). Check only at install, or before each governed launch? | Important | 04 open question (line 2258); 04 Key Takeaways bypass set | open | brainstorm decision (web-02 for exec-bit source) |
| G-9 | `ordinary` escapes: `setsid` and a different valid HOME make a governed push ordinary; HOME escape listed nowhere | Important | 01 Gaps 2 | open | brainstorm decision |
| G-10 | Stale job records after a killed supervisor are never pruned; with PID reuse an unrelated human can become `unknown` and be refused main/master. Prune or accept? (PID-reuse consequence is inferred) | Important | 01 Gaps 3; analyst m-14 (N14) | open | brainstorm decision |
| G-11 | Humans restricted by `unknown` (HOME unset/relative, group-writable home, stale records, no uv on PATH) vs design line 493 "never restricted" | Important | 01 Gaps 4, Gaps 10; qualitative verification N-2 | open | brainstorm decision |
| G-12 | No git-hooks tamper token in L1 (line 706): Write/Edit/rm/chmod/ln on `.git/hooks/pre-push` allowed | Important | 02 Gaps 1, Summary | open | brainstorm decision |
| G-13 | L1 command-position bypass: underscore env prefix moves command position off `git`, so aliases/obfuscated subcommands pass (LL-UNKNOWN Why line 80 contradicted) | Important | 02 Gaps 2; 02 Stale Documentation | open | brainstorm decision |
| G-14 | Config written without a git word (`.git/config`, `config.worktree`, `/etc/gitconfig`) sets `core.hooksPath`, `alias.*`, `remote.origin.push` unrefused | Important | 02 Gaps 3, 10; 02 Stale Documentation (LL-TAMPER partial) | open | brainstorm decision |
| G-15 | Destination from configuration (`remote.origin.push`) invisible to L1; L2 sees it as field 3 (E20) | Minor | 02 Gaps 4; 04 E20 | resolved for L2 (E20); L1 gap open | synthesis |
| G-16 | Smart-HTTP `git-receive-pack` on `github.com` and non-literal API hosts not refused by L1 | Important | 02 Gaps 5 | open | web-01 (does it bypass pre-push) + brainstorm decision |
| G-17 | IR-7 / D19-18: design says refuse the governed launch when L2 absent; code warns (W-L2-ABSENT). Once L2 exists, does IR-7 become the refusal? | Important | 03 Code contradictions; 03 Stale Documentation (lines 355, 514) | open | brainstorm decision |
| G-18 | D19-16: a foreign executable `pre-push` yields `present-unverified` with no warning; add `W-L2-CONFLICT` or a reason field? | Important | 03 Code contradictions | open | brainstorm decision |
| G-19 | `l2_status` cannot tell an owned guard from any executable (no marker, version line or hash); folds git-missing/timeout/not-a-repo into `absent` | Important | 03 Design gaps for an L2 installer; 01 Summary | open | brainstorm decision |
| G-20 | `install_hooks.py` has no git-hook path; per-repo install needs new code (natural point: `cmd_launch` before `l2_status`, design 565) | Important | 03 Design gaps | open | synthesis + brainstorm decision |
| G-21 | 19.6 source artifacts (`.dev/brainstorms/20261106-l2-prepush-decisions/`) absent; D19-10, 17, 33, 49, 52-56 unverifiable. Committed elsewhere or never? | Minor | 03 Gaps (source artifact absent); 03 Stale Documentation | open | brainstorm decision (ask owner) |
| G-22 | Line-487 corpus wrongly reported absent | Important | Consolidated B3; 03 lines 22, 301, 319, 328 | resolved in Gate 1 | none |
| G-23 | 04 lacked Key Takeaways | Important | Consolidated B1 | resolved in Gate 1 | none |
| G-24 | Stdin record order is not command order; "existing refs first" is inferred | Minor | 04 Gaps; analyst m-10 (N10) | open | web-01 |
| G-25 | Case folding: `refs/heads/Main` reaches the hook distinct (E25); hosting-service or case-insensitive FS behaviour, and whether GitHub treats `Main` as `main` | Minor | 04 Gaps; 02 Gaps 8; N10 | open | web-01 |
| G-26 | `git rev-parse --path-format=absolute --git-path hooks/pre-push` not exercised | Minor | 04 Gaps; analyst m-9 (N9) | open | web-01 |
| G-27 | Network transports (SSH/HTTPS): hook timing, "fetch first" filtering (E23), remote advertisement untested | Minor | 04 Gaps; N10 | open | web-01 |
| G-28 | Malformed governed stream: git never produced one; "never in any version or transport" not provable locally (D19-42 beyond scope) | Minor | 04 Gaps (two items) | open | web-01 |
| G-29 | `refs//heads/main` passes the L1 regex; git probably rejects consecutive slashes (untested) | Minor | 02 Gaps 9; N8 | open | web-01 (git-check-ref-format) |
| G-30 | `remote.<name>.mirror` default interaction with an explicit refspec | Minor | 02 Gaps 11; N7 | open | web-01 |
| G-31 | Whether `extensions.worktreeConfig` is enabled in this repo | Minor | 02 Gaps 10 | open | synthesis (local read-only check) |
| G-32 | Design §19.1 actor selection (process ancestry, B-CTX): one data point only (E1); no lifecycle variants | Minor | 04 Gaps; 01 Summary | open | synthesis |
| G-33 | PID-namespace/container behaviour and boot_id in containers | Minor | 01 Gaps 5 | open | brainstorm decision (scope) |
| G-34 | Non-dumpable/setuid Python making `/proc/<sid>` root-owned | Minor | 01 Gaps 6 | open | brainstorm decision (scope) |
| G-35 | Self-test scope for the installed hook (governed fixture or ordinary only) | Minor | 01 Gaps 7 | open | brainstorm decision |
| G-36 | Script lookup and missing-script behaviour from the hook | Minor | 01 Gaps 8 | open | brainstorm decision |
| G-37 | Orca's worktree-removal path untested (plain `git worktree remove` tested, F2) | Minor | 04 Gaps (Step 2.5 resolution line) | open | synthesis |
| G-38 | Whether `cd` persists between Bash calls in a governed session; mid-session `~/.bashrc` edits (`GIT_CONFIG_PARAMETERS`) | Minor | 02 Gaps 7, 12; N16 | open | brainstorm decision |
| G-39 | L1 section 9 evasions are static readings, not executed | Minor | 02 Gaps 13 | open | synthesis (confirm in L1 test suite) |
| G-40 | Local-path remotes can be changed by `update-ref`/`fetch` in the remote dir (not relevant to GitHub) | Minor | 02 Gaps 14 | open | synthesis |
| G-41 | The only real-git pre-push code is a TEST policy (tests/hooks/test_launch_job_identity.py:1175-1232) that crashes on malformed records | Minor | 03 Design gaps | open | synthesis |
| G-42 | Large push with a hook that never reads stdin: QA observed exit 0 with 3001 branches on 2.47.3 (QA sandbox, not in 04) | Minor | Consolidated N24 (qualitative F8) | open | synthesis (hook should drain stdin) |
| G-43 | Unverified design statements with no code: D19-1, 3, 9, 13, 14, 21, 23, 24, 26, 27, 29, 35, 38; no tests/observations: D19-40, 41, 43-46, 50; uncheckable: D19-6, 34, 51, 57, 82; partial: D19-31, 65, 70, 72, 77 | Minor | 03 Unverified design statements | open (the git parts of 21, 23, 27, 29, 35, 41 are settled by 04 Step 2.5) | synthesis |

Editorial MINOR notes carried for synthesis (not gaps in knowledge): N1-N6, N11-N13, N15, N17-N23 (consolidated cycle 0), M1-M4 (rf-qa verification), N-1, N-3, N-4 (qualitative verification). The synthesis must use the corrected remedy for G-6, not the superseded sentence at 04 line 1530 (N-3), and E19 rather than "E9-E11" (N21/M4).

## [UNVERIFIED] and [CODE-CONTRADICTED] claims

| Tag | Claim | Source |
|---|---|---|
| [CODE-CONTRADICTED] in part | D19-47 (design line 534): non-fast-forwards are rejected before pre-push. A "fetch first" non-ff DOES reach pre-push (E23a) | 04 Gaps, Step 2.5 table |
| [CODE-CONTRADICTED] / [STALE DOC] | LL-UNKNOWN Why (guard line 80): aliases/renamed commands cannot push | 02 Stale Documentation |
| [CODE-CONTRADICTED] (partial) | LL-TAMPER Blocked text (guard line 95): "a git configuration file" | 02 Stale Documentation |
| [CODE-CONTRADICTED] (wording) | launch-job-identity.sh header line 4 "descendants" vs session membership | 01 Gaps 9 |
| [STALE DOC] | Design IR-7 line 355 and 19.2 line 514 refusal vs warning in code | 03 Stale Documentation |
| [STALE DOC] | Design 19.6 lines 538-543 cite absent `20261106-l2-prepush-decisions/` files | 03 Stale Documentation |
| [UNVERIFIED] | D19-30 API/programmatic ref writes bypass pre-push | 04 Gaps (ROUTE web-01) |
| [UNVERIFIED] | pygit2/libgit2, dulwich, GitPython, JGit run pre-push | 04 Gaps (ROUTE web-01 (b)); 02 Gap 6 |
| [UNVERIFIED] | Stdin record order rule | 04 Gaps |
| [UNVERIFIED] | Case folding of `Main` on remotes/hosting | 04 Gaps; 02 Gaps 8 |
| [UNVERIFIED] | `--path-format=absolute --git-path` | 04 Gaps |
| [UNVERIFIED] | Network transport behaviour | 04 Gaps |
| [UNVERIFIED] | Malformed governed stream refuses; git never sends malformed records (D19-42 beyond scope) | 04 Gaps |
| [UNVERIFIED] | §19.1 actor selection lifecycle variants | 04 Gaps |
| [UNVERIFIED] | PID-namespace/container behaviour; boot_id in containers | 01 Gaps 5 |
| [UNVERIFIED] | Non-dumpable/setuid Python and `/proc/<sid>` ownership | 01 Gaps 6 |
| [UNVERIFIED] | `cd` persists between Bash calls | 02 Gaps 7 |
| [UNVERIFIED] | `refs//heads/main` rejected by git | 02 Gaps 9 |
| [UNVERIFIED] | `extensions.worktreeConfig` enabled in this repo | 02 Gaps 10 |
| [UNVERIFIED] | `remote.<name>.mirror` with explicit refspec | 02 Gaps 11 |
| [UNVERIFIED] | Mid-session `~/.bashrc` edits picked up | 02 Gaps 12 |

All `ROUTE web-01:` lines from file 04 (D19-30 and (b) other tools) appear above as G-1 and G-2 with Suggested resolution web-01.
