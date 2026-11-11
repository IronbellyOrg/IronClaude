# Synthesis 02: Target State, Gap Analysis, External Research Findings

- **Topic:** L2 guard that refuses a governed AI agent's push to `refs/heads/main` or `refs/heads/master`
- **Date:** 2026-11-08
- **Sources synthesized:** `research/01-identity-selector-ancestry.md`, `research/02-l1-guard-push-bypass-coverage.md`, `research/03-design-and-claim-code-crossvalidation.md`, `research/04-empirical-git-prepush-experiments.md`, `research/web-01-git-official-docs-and-versions.md`, `research/web-02-linux-atomic-publication-and-exec-bit.md`, `gaps-and-questions.md`
- **Tag conventions:** [CODE-VERIFIED] means confirmed in this repo's code or observed with real git 2.47.3 in a `/tmp` sandbox (file 04 uses the tag for observed git behaviour). [CODE-CONTRADICTED] means the code or observation disagrees with the claim. [STALE DOC] means a document that disagrees with the code. [UNVERIFIED] means nothing confirmed it. Web findings are external context and carry their URLs.
- **Editorial corrections applied** (from `gaps-and-questions.md` line 55): the G-6 remedy uses the corrected wording (an absolute uv path alone is not enough), not the superseded sentence at file 04 line 1530 (N-3). The refusal evidence cites E19, not "E9-E11" (N21/M4).

---

## 3. Target State

### 3.1 Goal

When a governed agent pushes, the L2 guard is a git `pre-push` hook. It refuses the whole push, with a nonzero exit, whenever any stdin record has field 3 (the remote ref) exactly equal to `refs/heads/main` or `refs/heads/master`. This holds for an update, a forced update, a create and a delete, and for every push form that reaches the hook. Every other push is allowed. The L2 layer is not built today: there is no production hook and no installer (file 03 section 4; D19-8, D19-71, D19-81 [CODE-VERIFIED] absence). Everything in this section is the target, not the current state.

### 3.2 Behaviour the guard must have

| # | Target behaviour | Evidence that makes it achievable | Tag |
|---|---|---|---|
| T-1 | Refuse a governed update, forced update, create or delete of `refs/heads/main` / `refs/heads/master` | Field 3 is always the fully qualified destination: `feature:main` (E2), `HEAD:main` (E6), `+alt:main` and `--force` with no force marker (E5a/E5b), `:main` and `--delete main` as `(delete) <zero-oid> refs/heads/main <old>` (E3b, E4b), create of `refs/heads/master` (E25), `remote.origin.push` mapping (E20), `push.default=upstream` (E21), `--mirror` (E11) | [CODE-VERIFIED] (file 04) |
| T-2 | One protected record refuses the whole push, mixed or not | E19, E24a/E24b (protected last or first), E26a (`--atomic`), E27b, F1 (fast-forward update and delete forms): exit 1 and remote refs unchanged | [CODE-VERIFIED] (file 04) |
| T-3 | Compare field 3 exactly and case-sensitively. Do not normalize `//` or case | `refs//heads/main` is rejected by git as `fatal: invalid refspec` before the hook runs (web-01 G1). `refs/heads/Main` is a valid, distinct ref (E25, web-01 G2). Look-alikes `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/ma` reach the hook as their own field 3 (E25, F3a), and the design leaves them unprotected (D19-27) | git part [CODE-VERIFIED]; design choice [UNVERIFIED] (no code) |
| T-4 | Parse each record by right-splitting into four fields: `line.rstrip("\n").rsplit(" ", 3)`. Decide only on field 3 | git itself sends a six-field record for `'HEAD@{0 days ago}:refs/heads/main'`. A naive four-variable `read` puts "ago}" in field 3 and lets the protected push through (web-01 G5, Area I). Only fields 2-4 are guaranteed free of spaces (git-check-ref-format rule 4) | external, local test (web-01) |
| T-5 | Empty stdin allows (exit 0) | The hook runs with EMPTY stdin for an up-to-date push (E12), a locally known non-fast-forward (E23b) and a stale lease (E27a). transport.c starts the hook before its filtering loop (web-01 Area I) | [CODE-VERIFIED] (file 04) |
| T-6 | Stdin rule (one rule for every file): governed, unknown and no-verdict paths read stdin to EOF before an allow; a refusal may exit as soon as it sees a protected record; ordinary and released verdicts exit 0 without reading (T-10) | Design D19-24 "Stream until EOF". 01 §4 says reading to EOF is needed to know whether the push is protected. Early refusal exit is safe because git tolerates EPIPE (web-01 Area I, transport.c lines 1327-1329). Gap G-42: a hook that never reads stdin exited 0 with 3001 branches | design [UNVERIFIED]; git part external |
| T-7 | `--dry-run` is refused the same way when protected | `--dry-run +alt:main` delivered the real record and moved no refs (E13b). git-push documents dry-run as "Do everything except actually send the updates" (web-01 B2) | [CODE-VERIFIED] (file 04) |
| T-8 | A "fetch first" non-fast-forward to main is refused by the hook | E23a: the `refs/heads/main` record reached the hook before git rejected the push. `REF_STATUS_REJECT_FETCH_FIRST` is not in transport.c's skip list (web-01 Area I) | [CODE-VERIFIED] (file 04); corrects D19-47 |
| T-9 | Hash-length independent | SHA-256 create, update and delete gave 64-hex oids with the same field 3 text (E22) | [CODE-VERIFIED] (file 04) |
| T-10 | Allow ordinary and released pushes with no output and no stream inspection: exit 0 without reading stdin (the T-6 rule) | Design D19-26; 01 §4 mapping: ordinary/released exit 0 silently without reading stdin | design [UNVERIFIED] (no code) |
| T-11 | Restrict pushes only. Local commits and merges stay unaffected | F4: a commit and a `--no-ff` merge into local main succeeded under a refusing hook, which never ran (D19-29 git part) | [CODE-VERIFIED] (file 04) |

### 3.3 Actor selection and the unknown policy (DECIDED)

The hook calls `~/.claude/hooks/launch-job-identity.sh identify` (01 §8). That command prints one JSON line `{"status": "..."}` and exits 0, and a nonzero exit means no verdict (01, `launch-job-identity.sh` lines 530-537) [CODE-VERIFIED].

**Unknown handling is DECIDED, not open.** On 2026-11-08 the owner decided that `unknown` refuses only pushes to `main` or `master`, with its own diagnostic, and allows everything else. Source: file 01 line 186, citing `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` line 73 ("Orca answer to msg_60b98182bb31").

| `identify` result | Protected push (field 3 = `refs/heads/main` or `refs/heads/master`) | Other pushes | Reads stdin |
|---|---|---|---|
| `{"status": "governed", "session_id": "<id>"}` | refuse | allow | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |
| `{"status": "ordinary"}` or `{"status": "ordinary", "reason": "released"}` | allow | allow | no; silent exit 0 |
| `{"status": "unknown"}` | refuse, with a diagnostic distinct from the governed one (DECIDED) | allow (DECIDED) | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |
| No verdict: nonzero exit (for example exit 2 when uv is absent), empty or unparseable output, unexpected status | treat as `unknown` (01 §4 target requirement; not yet written in the design, gap G-7) | allow | to EOF before an allow; a refusal may exit at the first protected record (EPIPE tolerated) |

```text
git push  ──►  pre-push hook (common-dir hooks/pre-push, also for linked worktrees)
                   │
                   ▼
        launch-job-identity.sh identify   (kernel session sid -> HOME store jobs/<sid>.json)
                   │
     ┌─────────────┼───────────────────────────┬─────────────────────────────┐
     ▼             ▼                           ▼                             ▼
 governed     ordinary / released          unknown                 no verdict (exit != 0,
     │             │                           │                    empty, bad JSON, other)
     │        exit 0, no read                  │                             │
     │                                         ◄─────── mapped to unknown ───┘
     ▼                                         ▼
 read stdin record by record; rsplit(" ", 3) each line; field 3 in {refs/heads/main, refs/heads/master}?
 (allow only after EOF; a refusal may exit at the first protected record, EPIPE tolerated)
     │ yes                                     │ yes
     ▼                                         ▼
 exit nonzero (governed diagnostic)       exit nonzero (unknown diagnostic)
     │ no                                      │ no
     ▼                                         ▼
 exit 0                                    exit 0
```

Sources for the diagram: 01 §4 (verdict mapping), 01 §7 (the hook, git and supervisor share one kernel session; `identify`, `identify $$` and `identify $PPID` agreed in every case), E1/E30 (common-dir hook), web-01 G5 (right-split).

Consequences the target accepts or must decide (detail in Section 4):

- The DECIDED policy means some humans are refused main/master: HOME unset or relative, a group-writable home, a stale record after a killed supervisor, and no uv on PATH (01 §4; G-11). This narrows design line 493, "never restricted" (D19-1 [UNVERIFIED]).
- The no-uv human case needs a remedy. File 01 §4 item 5 offers three options: (i) the hook sets a fixed PATH holding the uv directory recorded at install time; (ii) the hook applies the no-store early exit itself, which does not help a human on a machine that also has a store; (iii) a pure-shell hook. An absolute uv path alone is not enough, because the script resolves uv through PATH twice (lines 25 and 566) (corrected G-6 remedy, N-3). The choice is open (G-6).

### 3.4 Hook location and publication

| # | Target | Evidence | Tag |
|---|---|---|---|
| L-1 | git finds the hook from a linked worktree | A linked worktree runs `<common-dir>/hooks/pre-push`; a hook in the worktree-private git dir is ignored (E30, E1). gitrepository-layout: "This directory is ignored if $GIT_COMMON_DIR is set and "$GIT_COMMON_DIR/hooks" will be used instead" (web-01 D1). transport.c finds the hook through `find_hook`, and path.c lists `hooks` in `common_list` (web-02 Area 1c) | [CODE-VERIFIED] (file 04) + external |
| L-2 | The installer resolves the target path with git, run from the target worktree: `git rev-parse --path-format=absolute --git-path hooks/pre-push` | It returns the common dir, honours `core.hooksPath`, resolves a relative value against the worktree root, and reflects `-c` (web-01 D3, local check in `/tmp/web01-exp.PR24RB14`). `--git-path` has honoured hooksPath since 2.10.0. Never use `--git-dir`/hooks (04 Key Takeaways). Design D19-11 "never assume `.git` is a directory" ([CODE-VERIFIED] read side only, `orca_worktree.py` line 1020) | external + [CODE-VERIFIED] read side |
| L-3 | The installer also checks a per-worktree `core.hooksPath`: `git config --worktree --get core.hooksPath` when `extensions.worktreeConfig` is true | E31: a per-worktree hooksPath moved the lookup for that worktree only (web-01 recommendation 4, C4) | [CODE-VERIFIED] (file 04) + external |
| L-4 | Publish without replacing an existing hook | Temp file opened with `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, write, `fchmod`, `fsync`, `linkat` to the final name (EEXIST if it exists), `unlinkat` the temp, `fsync` the directory. This is the `publish()` shape of `launch-job-identity.sh` lines 164-174, plus an executable mode and fsync (01 §6; web-02 recommendation 1; web-02 experiment 8) | pattern [CODE-VERIFIED] in 01; recipe external, sandbox-tested |
| L-5 | Set the executable bit with `fchmod` (0755 or 0700), not with the open mode | Under umask 077 an open mode of 0755 became 0700; `fchmod` gave 0755 (web-02 experiments 1a/1b). `publish()` uses mode 0400, which is not executable, so it cannot be reused unchanged (01 §6) | external, sandbox-tested |
| L-6 | Do not use `rename`/`os.replace`. Do not depend on `O_TMPFILE` or `renameat2` | `rename` replaced the existing file silently (web-02 experiment 5). `O_TMPFILE` returned ENOTSUP on overlayfs (experiment 4x; overlayfs support needs kernel 6.10). `renameat2 RENAME_NOREPLACE` is not in Python `os` (web-02 Area 2) | external, sandbox-tested |
| L-7 | On EEXIST: compare full content, `O_NOFOLLOW` regular-file type, same dev/ino, owner and mode, and run a self-test. Identical owned content is reused. Anything else is preserved and reported as `W-L2-ABSENT` with the reason | 01 §6; design line 514 (D19-16); web-02 recommendation 4 | design [UNVERIFIED]; current code [CODE-CONTRADICTED] (D19-16) |
| L-8 | After install, verify `access(X_OK)` as the pushing user, including a noexec-mount check | git skips a hook that fails `access(X_OK)` and the push goes through (fail-open; `hook.c` lines 13-49 at v2.47.3; E29c). A noexec mount gives EACCES (web-02 Area 1b, recommendation 5) | [CODE-VERIFIED] (E29) + external |
| L-9 | Leave other hooks untouched; do not enable `extensions.worktreeConfig` or migrate `core.hooksPath` | D19-12 and D19-15 | [CODE-VERIFIED] (vacuous/absence; no code writes git hooks today) |
| L-10 | Never set `advice.ignoredHook=false` | It silences the only signal that a non-executable hook was skipped (E29b; web-02 recommendation 7) | [CODE-VERIFIED] (file 04) + external |

### 3.5 Success criteria (testable pass/fail)

Each criterion runs against a disposable local bare remote in a `mktemp -d` sandbox (design D19-45; file 04 method). "Refused" means push exit status nonzero AND the remote ref unchanged. "Allowed" means exit 0 AND the remote ref changed (or `--dry-run` exit 0).

| ID | Criterion | Pass condition | Evidence basis |
|---|---|---|---|
| SC-1 | Governed agent, linked worktree, `git push origin feature:main` | refused; stderr carries the governed diagnostic | E1, E2, E19 |
| SC-2 | Governed: `HEAD:main`, `+alt:main`, `--force feature:main`, `:main`, `--delete main`, create `refs/heads/master`, `--force-with-lease` matching | each refused | E3b, E4b, E5a, E5b, E6, E25, E27b |
| SC-3 | Governed: bare `git push origin` with `remote.origin.push=feature:main`; `-c push.default=upstream push origin` with upstream `origin/main` | each refused | E20, E21 |
| SC-4 | Governed: `--mirror` to a remote holding `refs/heads/main` that would change | refused | E11 |
| SC-5 | Governed: mixed push with a protected ref first and last, with and without `--atomic` | refused; the unprotected ref also unchanged | E24a/E24b, E26a, F1 |
| SC-6 | Governed: "fetch first" non-fast-forward to main | refused by the hook (record observed in hook log) | E23a |
| SC-7 | Governed: `--dry-run +alt:main` | exit nonzero | E13b |
| SC-8 | Governed: `'HEAD@{0 days ago}:refs/heads/main'` (six-field record) | refused, not mis-parsed | web-01 G5 |
| SC-9 | Governed, SHA-256 repository: create, update and delete of main | each refused | E22 |
| SC-10 | Governed: `feature:refs/heads/side`, `refs/heads/mainline`, `refs/heads/feature/main`, `refs/heads/main2`, `refs/tags/main`, `refs/heads/Main`, `refs/heads/ma` | each allowed | E25, F3a, D19-27 |
| SC-11 | Governed: up-to-date push (empty stdin) | exit 0 | E12, D19-23 |
| SC-12 | Governed: 3001-branch push with no protected ref | exit 0, and the hook read stdin to EOF before allowing (T-6 rule) | G-42, D19-24 |
| SC-13 | Ordinary (no record in the store) and released (`rm sessions/<id>`): push to main | allowed, no hook output, stdin not read (T-6/T-10 rule) | 01 §4, §7; D19-26 |
| SC-14 | Unknown (for example `env -u HOME`, bogus level content, killed supervisor): push to main | refused with the unknown diagnostic, different from the governed one | 01 §4, §7; seed-brief line 73 |
| SC-15 | Unknown: push to `refs/heads/side` | allowed | seed-brief line 73 (DECIDED) |
| SC-16 | `identify` exits nonzero, prints nothing, prints non-JSON, or prints an unexpected status | treated as unknown (SC-14 and SC-15 behaviour) | 01 §4 |
| SC-17 | `git rev-parse --path-format=absolute --git-path hooks/pre-push` from a linked worktree prints the installed path, and a push from that worktree runs the hook | both hold | E30, web-01 D3 |
| SC-18 | Installing over an existing foreign `pre-push` | foreign file bytes, mode and inode unchanged; install reports `W-L2-ABSENT` with a reason | 01 §6, D19-14, D19-16, web-02 experiment 3a |
| SC-19 | Installing twice | the second install reuses the identical owned file; no temp file remains | web-02 experiment 8 |
| SC-20 | Installed hook mode under umask 077 | `access(X_OK)` true for the pushing user (mode 0700 or 0755) | web-02 experiments 1a/1b, 7 |
| SC-21 | `pre-commit`, `commit-msg` and other hooks before/after install | byte-identical | D19-12 |
| SC-22 | Governed: local commit and merge into local main | succeed (L2 restricts pushes only) | F4, D19-29 |
| SC-23 | Human whose PATH lacks uv, no store record, push to main | allowed if the remedy for G-6 is adopted; otherwise refused as unknown. The remedy choice is open | E28c, 01 §4 item 5 |

### 3.6 Constraints from design section 19 (`docs/designs/sc-issue-launch-level-hook.md` lines 489-578)

The verification tags come from file 03's claim table, as updated by file 04 Step 2.5 and web-01.

| D19 | Line | Constraint | Verification status |
|---|---|---|---|
| D19-1 | 493 | Ordinary human push in the same worktree is never restricted by launch policy | [UNVERIFIED] (no L2 code). Narrowed by the DECIDED unknown policy (G-11) |
| D19-2 | 493 | git's inputs are remote name/URL and ref records; no Claude session id from git | [CODE-VERIFIED] (04 E1, E11, E18, E28) |
| D19-3 | 493 | A marker is only an eligibility hint; env values, pane key, branch or path are never authority | [UNVERIFIED] (no L2 selector). The environment passes through unchanged (E28) |
| D19-11 | 510 | Resolve git paths with git; never assume `.git` is a directory | [CODE-VERIFIED] read side only (`orca_worktree.py` line 1020) |
| D19-12 | 510 | Other hooks remain untouched | [CODE-VERIFIED] (vacuous) |
| D19-13 | 512 | Install only at default lookup, no foreign pre-push, publication and self-test succeed | [UNVERIFIED] (no installer) |
| D19-14 | 512 | Publish a complete executable without replacing an existing file; recheck owned content; a header alone is no proof of ownership | [UNVERIFIED] (no installer); recipe tested externally (web-02 experiment 8) |
| D19-15 | 512 | Do not enable worktreeConfig, migrate hooksPath, shadow, stub or replay foreign hooks | [CODE-VERIFIED] (absence) |
| D19-16 | 514 | Conflict or unsupported lookup: preserve, report `W-L2-ABSENT` with the reason | [CODE-CONTRADICTED] (foreign hook gives `present-unverified`, no warning) |
| D19-18 | 514 | Do not launch a governed pipeline advertised as protected when L2 is absent | [CODE-CONTRADICTED] (code warns and launches); design IR-7 line 355 and line 514 [STALE DOC] |
| D19-19 | 514 | Ordinary/no-pipeline claim unaffected | [CODE-VERIFIED] |
| D19-20, 22, 25 | 518 | Record format; zero oids and `(delete)` ordinary; no SHA-1 length | [CODE-VERIFIED] (04 Step 2.5) |
| D19-21 | 518 | Refuse the entire push if field 3 is exactly main/master | git part [CODE-VERIFIED] (E19, E24, E26a, F1); guard [UNVERIFIED] |
| D19-23 | 518 | Empty stream allows; malformed governed stream refuses with a distinct diagnostic | empty part [CODE-VERIFIED]; malformed part [UNVERIFIED]; must be reconciled with the six-field form (web-01 G5, recommendation 1) |
| D19-24 | 518 | Stream until EOF; no truncation | [UNVERIFIED] |
| D19-26 | 518 | Unselected ordinary pushes allowed without output or stream inspection | [UNVERIFIED] |
| D19-27 | 520 | `refs/tags/main`, `mainline`, `ma`, `feature/main` not protected | git part [CODE-VERIFIED] (E25, F3a) |
| D19-28 | 520 | A mapped source-only refspec is protected because field 3 is authoritative | [CODE-VERIFIED] (E20, E21, E6) |
| D19-29 | 520 | No local commit/merge restriction | git part [CODE-VERIFIED] (F4) |
| D19-30 | 520 | `--no-verify`, hooksPath overrides, send-pack and API writes bypass pre-push | local forms [CODE-VERIFIED] (E14-E17); API part: documented externally (web-01 H/J); not confirmed at runtime |
| D19-31 | 520 | Visible bypass forms remain checked by L1 | [CODE-VERIFIED] partial (`launch-level-guard.sh` lines 528, 532); file 02 lists ALLOWED/PARTIAL forms |
| D19-32 | 520 | Same-user modification and detachment remain limitations | [CODE-VERIFIED] (disclaimer, `launch-job-identity.sh` lines 2, 7-9) |
| D19-35 | 524 | The shared hook may remain installed after one worktree is removed | [CODE-VERIFIED] (F2) |
| D19-36 | 526 | Deleting level/approval files is the release route | [CODE-VERIFIED] (identity side only) |
| D19-37, 39 | 526 | A retained marker must not restrict humans; no shared-hook deletion on single-session release | [CODE-VERIFIED] (absence) |
| D19-46 | 534 | Check effective hook presence, executable ownership and process membership | [UNVERIFIED]; `l2_status` covers presence and X_OK only |
| D19-47 | 534 | Fixture refs must reach pre-push (not up-to-date/non-fast-forward rejection) | [CODE-CONTRADICTED] in part (E23a "fetch first" reaches the hook) |
| D19-48 | 534 | Dry-run supplements, does not replace, ref-state assertions | [CODE-VERIFIED] (E13) |
| D19-59 | 549 | Identity body runs through uv on Linux | [CODE-VERIFIED] (`launch-job-identity.sh` line 566) |
| D19-66 | 557 | `identify [PID]` emits governed/ordinary/unknown | [CODE-VERIFIED] |
| D19-67 | 559 | Fresh Bash shell; `cd` does not persist; `setsid` escapes | [CODE-VERIFIED] |
| D19-81 | 576 | The L2 layer is pending and needs its own plan | [CODE-VERIFIED] (absence) |

Other §19 claims (D19-4 to D19-10, D19-17, D19-33, D19-34, D19-38, D19-40 to D19-45, D19-49 to D19-58, D19-60 to D19-65, D19-68 to D19-80, D19-82, D19-83) are about history, process, the identity adapter or L1 rather than L2 push behaviour. Their tags are in file 03's claim table and are not repeated here. D19-82 (no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass) is [UNVERIFIED]: `cmd_launch` has no OB check.

---

## 4. Gap Analysis

**Severity rule.** Gaps G-1 to G-43 keep the severity recorded in `gaps-and-questions.md`, unchanged. Rows added from the research (prefixes BP, L1, DOC) are rated as follows. Critical: a governed push to main or master succeeds with no layer refusing it, and needs no capability beyond ordinary same-user file access or an ordinary command. Important: the target needs a decision, code or a doc correction, or a layer still refuses the push. Minor: a precision or wording issue, or a future-version risk. Note that no G-row is rated Critical in `gaps-and-questions.md`. The Critical rows below are new ratings by this synthesis, based on file 02 verdicts and file 04/web results, and are not taken from the gap file.

### 4.1 Gaps compiled in `gaps-and-questions.md`

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-1: API/programmatic ref writes (hosting ref API, `gh api`, curl to smart-HTTP `git-receive-pack`) | No local test (04 D19-30 API part [UNVERIFIED]) | Recorded as an L2 limitation; L1 refuses the visible forms | Important | **Documented externally (web-01 H/J); not confirmed at runtime.** Per the documentation none of them runs pre-push (gitprotocol-http, GitHub REST refs docs, gh api manual); web-01 J11 rates design line 520 CONFIRMED on that documentary basis. Nothing was run |
| G-2: Do pygit2/libgit2, dulwich, GitPython, JGit run pre-push? | Untested locally; none installed (04 Gaps) | Each library classified; in-process pushes recorded as a stated limitation | Important | **Documented externally (web-01 H/J); not confirmed at runtime.** Per the documentation and source reading, libgit2, pygit2, dulwich, isomorphic-git do not; JGit (since 4.2) and GitPython (shells out to `git push`) do. No library was installed or run. See BP-9 |
| G-3: git version of each behaviour | Hints only | Version table with release-note citations | Important | **Answered by web-01 F2** (Section 5.3 version table) |
| G-4: Linux no-replace publication | `publish()` pattern exists (`launch-job-identity.sh` lines 164-174) but is mode 0400 and inside a heredoc (01 §6) | `O_EXCL` temp, `fchmod` 0755/0700, `fsync`, `linkat`, `unlinkat`, directory `fsync` | Important | **Answered by web-02** Areas 2-3, experiment 8 (Section 5.2) |
| G-5: git's executable check | E29 observed the fail-open | Source-level explanation | Important | **Answered by web-02 Area 1:** `find_hook` in `hook.c` line 21 uses `access(X_OK)`; `transport.c` lines 1295-1296 `if (!hook_path) return 0;` |
| G-6: Human whose PATH lacks uv | `identify` exits 2 (lines 25, 52-53, 566), which maps to unknown, so the human is refused main/master (E28c) | That human can push to main/master (D19-1) | Important | Options: fixed PATH with the install-time uv directory, a hook-side no-store exit (does not help on a machine with a store), or a pure-shell hook. An absolute uv path alone is not enough (corrected remedy, N-3). Design choice open |
| G-7: "No verdict" maps to unknown, but this is not written in the design | 01 §4 states it as a hook requirement only | Design states it; the hook implements it | Important | `identify` prints default-separator JSON (`{"status": "ordinary"}`, with a space after the colon) while `publish()` uses compact separators. The hook must parse JSON rather than compare compact text (01 line 44) |
| G-8: Install-integrity holes with no push flag: exec bit cleared (E29) and per-worktree `core.hooksPath` (E31) | `l2_status` checks only `is_file` and `X_OK` (`orca_worktree.py` lines 1012-1029), and only before a launch | Integrity checked at install AND before each governed launch (open decision) | Important | web-02 recommendation 8: the executable bit makes L2 easy to disable, so a pre-flight X_OK check or another layer is needed. See BP-5, BP-6 |
| G-9: Ordinary escapes: `setsid` and a different valid HOME | Both give `ordinary` (01 §7); HOME escape listed nowhere | Escape acknowledged in the design, or closed | Important | `setsid` is listed (header lines 7-8, design 559, seed brief line 45); L1 refuses `HOME=` and `env -u HOME` (02) |
| G-10: Stale job records after a killed supervisor are never pruned | After `kill -9`, the verdict is unknown and `jobs/<sid>.json` stays (01 §7) | Prune, or accept and document | Important | PID reuse turning a human into unknown is inferred, not observed |
| G-11: Humans restricted by unknown | HOME unset/relative, group-writable home, stale record, no uv on PATH give unknown (01 §4) | Accepted consequence of the DECIDED policy, documented against design line 493 | Important | The DECIDED policy (seed brief line 73) makes this a documentation gap, not a policy question |
| G-12: No git-hooks tamper token in L1 | Line 706 tokens omit `.git/hooks`; Write/Edit/rm/chmod/ln on `pre-push` ALLOWED (02) | Token added at line 706 | Important | See L1-3, L1-4 |
| G-13: L1 command-position bypass via an underscore env prefix | W has no `_` (lines 421-438), so `A_B=1 git ...` moves command position off `git` (line 637) | Prefix handled | Important | Contradicts LL-UNKNOWN Why line 80 (DOC-2). See L1-5 |
| G-14: Config written without a git word | `.git/config`, `config.worktree`, `/etc/gitconfig` writes set `core.hooksPath`, `alias.*`, `remote.origin.push` unrefused | Refused, or L2 covers the result | Important | Line 532 config tokens apply only when LL_GIT=1. See L1-1 |
| G-15: Destination from configuration invisible to L1 | L1 canonical regex (line 661) sees only the command text | L2 sees it as field 3 (E20) | Minor | Resolved for L2; L1 gap stays |
| G-16: Smart-HTTP `git-receive-pack` on `github.com` and non-literal API hosts | L1 ALLOWED/PARTIAL (02) | Refused by L1, or stated as a limitation | Important | web-01 H: a smart-HTTP POST does not run pre-push. See BP-7, L1-6, L1-7 |
| G-17: IR-7/D19-18 refusal vs warning | Code warns `W-L2-ABSENT` and launches (`orca_worktree.py` lines 1305-1312, Remedy 789-792) | Default DECIDED by the owner (seed-brief line 77): off, so `W-L2-ABSENT` stays a warning; the refusal path is built behind a switch in a separate, clearly marked commit and is tested (seed-brief line 68); the change is one line (comment at the call site). Open: the switch mechanism and when it turns on (after #442) | Important | DOC-5 |
| G-18: D19-16 foreign executable hook gives `present-unverified`, no warning | `test_issue_orca_worktree.py` lines 1691, 1727 | `W-L2-CONFLICT` or a reason field | Important | [CODE-CONTRADICTED] |
| G-19: `l2_status` cannot tell an owned guard from any executable | No marker, version line or hash; git-missing, timeout and not-a-repo fold into `absent` | Full-content ownership check (01 §6) | Important | L1 has a version line, `GUARD_VERSION_LINE` (`orca_worktree.py` line 804), as a precedent |
| G-20: `install_hooks.py` has no git-hook path | 612 lines, no pre-push code (03) | New per-repo install code; natural point in `cmd_launch` before `l2_status` (design 565) | Important | The whole L2 layer is unbuilt (D19-81) |
| G-21: §19.6 artifacts absent | `.dev/brainstorms/20261106-l2-prepush-decisions/` missing; D19-10, 17, 33, 49, 52-56 unverifiable | Committed, or the citations removed | Minor | DOC-6 |
| G-22: Line-487 corpus wrongly reported absent | Resolved in Gate 1 | — | Important (resolved) | `.dev/brainstorms/20261105-170229-launch-level-hook/` is present |
| G-23: 04 lacked Key Takeaways | Resolved in Gate 1 | — | Important (resolved) | 04 lines 2233-2245 |
| G-24: Stdin record order | Undocumented; observed both ways: command-line order in E7 and web-01 G3 (one `--dry-run` run of creates), not command-line order in E9, E19 and E24 (E24: two runs, same stream whichever position the protected ref had) | Guard scans every record and does not depend on order | Minor | web-01 G3/Area I: no documented order; code does not sort. Design §19.3 already says not to depend on order. Resolved only in that sense |
| G-25: Case folding of `Main` | Distinct field 3 (E25) | Compare case-sensitively | Minor | web-01 G2: valid and distinct ref. Hosting-service folding not answered [UNVERIFIED] |
| G-26: `--path-format=absolute --git-path` not exercised in 04 | 04 measured plain `--git-path` only | Installer uses the absolute form | Minor | **Answered by web-01 D3** (local check) |
| G-27: Network transports | File transport only | — | Minor | Open [UNVERIFIED] |
| G-28: Malformed governed stream | 04: git never produced one | Guard handles git's legitimate more-than-four-field record | Minor | **Contradicted in part by web-01 G5** (six-field record from `git push`). See DOC-8. Severity of the six-field risk is higher than this row: see BP-14 |
| G-29: `refs//heads/main` passes the L1 regex | — | — | Minor | **Answered by web-01 G1:** `fatal: invalid refspec`, hook never runs |
| G-30: `remote.<name>.mirror` with an explicit refspec | — | — | Minor | **Answered by web-01 G4:** `fatal: --mirror can't be combined with refspecs` |
| G-31: Is `extensions.worktreeConfig` enabled in this repo? | Not checked | Known | Minor | Open (local read-only check) |
| G-32: §19.1 actor selection lifecycle variants | One data point (E1) | — | Minor | 01 §7 adds real-git cases (setsid, HOME, background child, release, kill -9) |
| G-33: PID namespace / container boot_id | [UNVERIFIED] | Scope decision | Minor | 01 §5 |
| G-34: Non-dumpable/setuid Python making `/proc/<sid>` root-owned | [UNVERIFIED] | Scope decision | Minor | 01 Gaps 6 |
| G-35: Self-test scope of the installed hook | Undecided | Decided (governed fixture or ordinary only) | Minor | 01 Gaps 7 |
| G-36: Script lookup and missing-script behaviour from the hook | Undecided | A missing script gives no verdict, which maps to unknown (G-7) | Minor | 01 Gaps 8 |
| G-37: Orca's worktree-removal path | Plain `git worktree remove` tested (F2) | — | Minor | D19-34 self-declared unverified |
| G-38: `cd` persistence between Bash calls; mid-session `~/.bashrc` edits | [UNVERIFIED] | — | Minor | D19-67 [CODE-VERIFIED] says `cd` does not persist inside the identity adapter's fresh shell |
| G-39: L1 section 9 evasions are static readings | Not executed | Confirmed in the L1 test suite | Minor | See L1-5, BP-11 |
| G-40: Local-path remotes changed by `update-ref`/`fetch` in the remote dir | — | — | Minor | Not relevant to GitHub (02 Gap 14) |
| G-41: The only real-git pre-push code is a TEST policy that crashes on malformed records | `tests/hooks/test_launch_job_identity.py` lines 1175-1232 (ValueError at 1204) | Production hook with right-split parsing | Minor | |
| G-42: Large push, hook never reads stdin | Exit 0 with 3001 branches (QA sandbox, not in 04) | The T-6 rule: governed, unknown and no-verdict paths read stdin to EOF before an allow; a refusal may exit at the first protected record; ordinary and released exit 0 without reading | Minor | web-01 Area I: EPIPE tolerated, so an early refusal exit is safe |
| G-43: Unverified design statements | D19-1, 3, 9, 13, 14, 21, 23, 24, 26, 27, 29, 35, 38 have no code; others untested or uncheckable | — | Minor | git parts of 21, 23, 27, 29, 35, 41 settled by 04 Step 2.5 |

### 4.2 Bypasses that skip the pre-push hook

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| BP-1: `git push --no-verify` | Hook not run, remote changed (E14) | L1 refuses | Important | L1 REFUSED (02). Documented "the hook is bypassed completely" (web-01 B1). Code 1.8.2, docs 1.8.4 |
| BP-2: `-c core.hooksPath=/dev/null` or a directory without pre-push | Hook not run (E15, E16) | L1 refuses | Important | L1 REFUSED `-c core.hooksPath` and `git config core.hooksPath` (02) |
| BP-3: `--config-env` and `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`, `GIT_CONFIG_PARAMETERS` | Not tested in 04; documented (web-01 C2) | L1 refuses these forms (web-01 recommendation 5) | Critical | 02 §9 static evasion `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=$'core.hooks\x50ath' GIT_CONFIG_VALUE_0=/dev/null` was not executed (G-39) |
| BP-4: Persistent `core.hooksPath` written to `.git/config` or `config.worktree` | Effective for the next push (E31 for config.worktree) | L1 refuses; install-integrity check detects it | Critical | L1 PARTIAL (02, line 706). See L1-1, G-8, G-14 |
| BP-5: Per-worktree `core.hooksPath` via `extensions.worktreeConfig` | Lookup moved for that worktree only (E31a) | Detected before each governed launch | Important | web-01 C4. G-8 |
| BP-6: Executable bit cleared on the hook | Hook skipped with a hint; real push to main succeeded (E29c). `-c advice.ignoredHook=false` silences the hint (E29b) | Detected (X_OK pre-flight) | Critical | L1 ALLOWED for `chmod -x` (02). `hook.c` line 21 `access(X_OK)` (web-02). See L1-4 |
| BP-7: Raw smart-HTTP POST to `.../git-receive-pack` | Does not run pre-push (web-01 H, gitprotocol-http) | L1 refuses `curl` to `git-receive-pack` | Critical | L1 ALLOWED for `github.com/<o>/<r>.git/git-receive-pack` (02) |
| BP-8: `git send-pack` | Hook not run; `--force alt:refs/heads/main` rewrote main (E17c) | L1 refuses | Important | L1 REFUSED (02) |
| BP-9: In-process library push (libgit2/pygit2, dulwich, isomorphic-git) | Does not run pre-push (web-01 J) | Stated limitation (web-01 recommendation 5) | Critical | L1 PARTIAL for `uv run python -c` with these libraries; ALLOWED for `uv run python <script>` (02, line 678) |
| BP-10: GitHub REST refs API / `gh api` | Does not run pre-push (web-01 J) | L1 refuses; server-side protection | Important | L1 REFUSED `curl` to api.github.com, `gh api -X`/`--method`; PARTIAL for hidden host and `gh $'\x61pi'` (02). See L1-7, L1-8 |
| BP-11: Hook file removed, replaced or symlinked | Not tested; L1 ALLOWED `rm`, `mv`, `ln -sf`, `printf >`, Write/Edit (02) | Detected by the ownership check; L1 token at line 706 | Critical | G-12. L1-3, L1-4 |
| BP-12: `hook.pre-push.enabled=false` (future) | Not in 2.47.3; in the unreleased 2.98.0 draft it also disables hooks-directory hooks (web-01 F) | L1 covers `-c hook.pre-push.*` | Minor | Future-version risk |
| BP-13: Config-defined hooks (2.54.0) and parallel hooks (2.55.0); remote groups (on the 2.55.0 git-push page) | Absent from 2.47.3 | Version assumption pinned (web-01 recommendation 7) | Minor | Remote groups: git "continues pushing to the remaining remotes" after a failure (web-01 B7) |
| BP-14: Naive parsing of a more-than-four-field record | Six fields for `'HEAD@{0 days ago}:refs/heads/main'` (web-01 G5) | `rsplit(" ", 3)` parsing (T-4) | Important | Not a hook skip but a guard bypass if the hook parses with a four-variable `read` |

### 4.3 L1 verdicts of ALLOWED or PARTIAL (file 02)

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| L1-1: Persistent `core.hooksPath` via a direct config-file write (`cd .git && >> config`, `config.worktree`) | PARTIAL (line 706) | Refused | Critical | BP-4, G-14 |
| L1-2: `cd <dir>`, then a canonical push | ALLOWED | L2 refuses if the destination is main/master | Important | L2 sees field 3 regardless of `cd` |
| L1-3: Write or Edit of `.git/hooks/pre-push` | ALLOWED (lines 679, 706, 743) | Refused (`.git/hooks` token) | Critical | G-12 |
| L1-4: `rm`, `mv`, `chmod -x`, `ln -sf`, `printf >` on the hook | ALLOWED | Refused | Critical | G-12, BP-6, BP-11 |
| L1-5: Alias by file write, then `<VAR_WITH_UNDERSCORE>=1 git <x> origin main` | ALLOWED (lines 435, 556-557, 637, 706) | Refused | Critical | G-13. 02 §9: `A_B=1 git $'\x70ush' --no-verify origin main` passes at every level (static reading, G-39) |
| L1-6: `curl` POST to `github.com/<o>/<r>.git/git-receive-pack` | ALLOWED | Refused | Critical | BP-7, G-16 |
| L1-7: `curl` to `api.github.com` with the host hidden | PARTIAL | Refused or stated limitation | Important | BP-10 |
| L1-8: `gh $'\x61pi'` hidden api | PARTIAL | Refused | Important | BP-10 |
| L1-9: `uv run python -c` with pygit2, dulwich or GitPython | PARTIAL | Stated limitation | Important | BP-9. GitPython goes through `git push`, so L2 sees it unless `no_verify=True` (web-01 J) |
| L1-10: `uv run python <script>` that pushes | ALLOWED (line 678) | Stated limitation | Critical | BP-9 |

### 4.4 [CODE-CONTRADICTED] and [STALE DOC] findings

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| DOC-1: D19-47 (design line 534) says non-fast-forward refs are rejected before pre-push | [CODE-CONTRADICTED] in part: a "fetch first" non-ff reaches the hook (E23a) | Line 534 says only non-fast-forward, stale, remote-updated and up-to-date refs are filtered (web-01 recommendation 8) | Important | Source: `transport.c` lines 1315-1319 skip list (web-01 Area I). 04 calls the sentence "incomplete rather than wrong" |
| DOC-2: LL-UNKNOWN Why text (`launch-level-guard.sh` line 80): "an alias cannot commit, push or merge" | [CODE-CONTRADICTED]/[STALE DOC] (G-13) | Text corrected or the bypass closed | Important | 02 Stale Documentation |
| DOC-3: LL-TAMPER Blocked text (line 95): "a git configuration file" | [CODE-CONTRADICTED] (partial): only some config paths are tokens | Text matches the tokens | Minor | 02 Stale Documentation |
| DOC-4: `launch-job-identity.sh` header line 4 "descendants" | [CODE-CONTRADICTED] (wording): the code uses kernel session membership | Header says session membership | Minor | 01 Gaps 9 |
| DOC-5: Design IR-7 line 355 and §19.2 line 514 say refuse | [STALE DOC]: code warns `W-L2-ABSENT` and launches (D19-18 [CODE-CONTRADICTED]) | Design and code agree: the design records the DECIDED default (off; warning stays; refusal path built, tested and switched off, seed-brief lines 68, 77) | Important | G-17. §19.8 line 574 itself records the warning choice (D19-79) |
| DOC-6: Design §19.6 lines 538-543 cite `.dev/brainstorms/20261106-l2-prepush-decisions/` | [STALE DOC]: absent | Present, or citation removed | Minor | G-21 |
| DOC-7: D19-16 (design line 514) conflict reported as `W-L2-ABSENT` | [CODE-CONTRADICTED]: `present-unverified`, no warning | Conflict reported | Important | G-18 |
| DOC-8: D19-42 (design line 530) "Git does not normally send malformed or padded records" and D19-23 "malformed governed stream refuses" | file 04 F3: CONFIRMED for the tested scope. web-01 G5: `git push` sends a six-field record for an expression source | Design accepts more than four fields when fields 2-4 are valid (web-01 recommendation 1), or names this form in a distinct refusal diagnostic | Important | **Contradiction between files.** web-01 G5 is stronger evidence here: a direct local test of an input form that file 04 never tried. File 04's result remains true for the refspecs it tested |
| DOC-9: LL-PUSH-FORM text (line 56) omits `--set-upstream` | Canonical regex (line 661) accepts `-u|--set-upstream` | Text lists both | Minor | 02 Stale Documentation |
| DOC-10: Design line 493 "never restricted" (D19-1) | The DECIDED unknown policy restricts some humans (G-11) | Line 493 narrowed | Important | 01 §4. No code contradicts it today because no L2 code exists |
| DOC-11: git-scm git-hook page (2.55.0) on `hook.<event>.enabled` vs the 2.98.0 draft release note | The page reads as if it already disables hookdir hooks; the release note says that is unreleased | — | Minor | External discrepancy (web-01 F). Relevant to BP-12 |

### 4.5 Other cross-file contradictions

| Topic | File A | File B | Stronger evidence |
|---|---|---|---|
| Is `--path-format=absolute --git-path hooks/pre-push` verified? | 04 Gaps: not exercised | web-01 D3: exercised locally from a linked worktree; returned the common dir and honoured `core.hooksPath` | web-01 D3 (direct later test). G-26 resolved |
| Do API, smart-HTTP and library pushes bypass pre-push? | 04 Gaps: [UNVERIFIED], not testable locally | web-01 Areas H and J: official docs and maintainer statements | web-01. Status: documented externally (web-01 H/J); not confirmed at runtime |
| Which rejected refs reach the hook | Design D19-47 (line 534) | 04 E23a and web-01 Area I (`transport.c` skip list) | 04 + web-01 (observation plus source). See DOC-1 |
| Malformed records from git | 04 D19-42: none observed, "CONFIRMED for the tested scope" | web-01 G5: six fields from `'HEAD@{0 days ago}:refs/heads/main'` | web-01 G5. See DOC-8 |

---

## 5. External Research Findings

Everything in this section is **external context**. The sources are web pages, man pages, git source at tag v2.47.3, and two local sandbox checks run by the web researchers (`/tmp/web01-exp.*` and `/tmp/web02-sandbox.pVSjes6U`, both removed). web-01 used WebSearch and WebFetch because tavily was unavailable (web-01 header). The "Relation to 04" column says whether a finding SUPPORTS, EXTENDS or CONTRADICTS what file 04 observed on git 2.47.3.

### 5.1 git official documentation and release notes (web-01)

| # | Finding | Source URL | Relevance | Relation to 04 |
|---|---|---|---|---|
| W1-1 | githooks pre-push contract. argv holds the remote name and the URL. stdin holds `<local-ref> SP <local-oid> SP <remote-ref> SP <remote-oid> LF`. A nonzero exit aborts the push "without pushing anything". The installed 2.47.3 man page matches the web page | https://git-scm.com/docs/githooks | HIGH | SUPPORTS E19, E24, E26 |
| W1-2 | Docs say field 1 is "supplied as it was originally given". They do not say field 3 is fully qualified. The code guarantees it: `transport.c` writes `r->name` in field 3 (lines 1322-1324) | https://git-scm.com/docs/githooks; https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | EXTENDS (explains 04's "field 3 is authoritative") |
| W1-3 | "Hooks that don't have the executable bit set are ignored" | https://git-scm.com/docs/githooks | HIGH | SUPPORTS E29 |
| W1-4 | The wording "after it has checked the remote status, but before anything has been pushed" is not in githooks. The code shows the same timing: the hook runs after ref matching and the lease and status checks, and before any pack is sent | https://github.com/git/git/blob/v2.47.3/transport.c | MEDIUM | EXTENDS |
| W1-5 | `transport.c` lines 1315-1319 skip four statuses: non-fast-forward, stale lease, remote-updated and up-to-date. "Fetch first" is not skipped. The hook starts before the loop, so empty stdin is normal. EPIPE is tolerated (lines 1327-1329) | https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS E12, E23b, E27a; EXPLAINS E23a; CONTRADICTS design D19-47 |
| W1-6 | `--no-verify`: "the hook is bypassed completely" | https://git-scm.com/docs/git-push | HIGH | SUPPORTS E14 |
| W1-7 | `--dry-run`: "Do everything except actually send the updates" | https://git-scm.com/docs/git-push | HIGH | SUPPORTS E13 |
| W1-8 | `--atomic` is a remote-side transaction. The local whole-push abort comes from githooks and does not depend on `--atomic` | https://git-scm.com/docs/git-push | MEDIUM | SUPPORTS E19, E24, E26 |
| W1-9 | git-push says "rejected: Git did not try to send the ref at all". It does not document the E23a/E23b split | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (source code, W1-5, is the stronger evidence) |
| W1-10 | REMOTE GROUPS appear on the 2.55.0 page: git "continues pushing to the remaining remotes". The section is absent from 2.47.3 | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (future risk, BP-13) |
| W1-11 | `core.hooksPath`; a relative path resolves against the worktree root | https://git-scm.com/docs/git-config | HIGH | SUPPORTS E15, E16, E30 |
| W1-12 | `-c`, `--config-env` and `GIT_CONFIG_COUNT`/`KEY`/`VALUE` set config for one process | https://git-scm.com/docs/git-config | HIGH | EXTENDS (not tested in 04; BP-3) |
| W1-13 | `advice.ignoredHook` controls the skipped-hook hint | https://git-scm.com/docs/git-config | MEDIUM | SUPPORTS E29b |
| W1-14 | `extensions.worktreeConfig` lets `config.worktree` override shared config | https://git-scm.com/docs/git-config, https://git-scm.com/docs/git-worktree | HIGH | SUPPORTS E31 |
| W1-15 | gitrepository-layout: the private hooks dir "is ignored if $GIT_COMMON_DIR is set and "$GIT_COMMON_DIR/hooks" will be used instead". git-worktree says to use `rev-parse --git-path` | https://git-scm.com/docs/gitrepository-layout, https://git-scm.com/docs/git-worktree | HIGH | SUPPORTS E30 |
| W1-16 | Local check: from a linked worktree, `git rev-parse --path-format=absolute --git-path hooks` returns the common dir. It honours `core.hooksPath`, resolves a relative value against the worktree root, and reflects `-c` | https://git-scm.com/docs/git-rev-parse (+ local test) | HIGH | EXTENDS (closes 04 gap G-26) |
| W1-17 | `git hook run --to-stdin` exists in 2.47.3 and can feed synthetic stdin in tests | https://git-scm.com/docs/git-hook | MEDIUM | EXTENDS |
| W1-18 | Config-defined hooks (2.54.0) and parallel hooks (2.55.0). Whether `hook.<event>.enabled=false` acts as a bypass is not settled | https://git-scm.com/docs/git-hook | MEDIUM | EXTENDS (future risk; see W1-27) |
| W1-19 | `refs//heads/main` is an invalid ref. `git push` fails with `fatal: invalid refspec` and the hook never runs (local test) | https://git-scm.com/docs/git-check-ref-format | MEDIUM | EXTENDS (closes G-29) |
| W1-20 | `refs/heads/Main` is valid and distinct from `main` (local test) | https://git-scm.com/docs/git-check-ref-format | LOW-MEDIUM | SUPPORTS E25 |
| W1-21 | In one dry-run test of creates, records came in command-line order. No order is documented and the code does not sort | https://github.com/git/git/blob/v2.47.3/transport.c | MEDIUM | Agrees with 04 E7; CONTRADICTS the order seen in 04 E9, E19 and E24 (E24 is the stronger evidence: two runs, same stream whichever position the protected ref had). Order is undocumented and was observed both ways, so the guard must scan every record and not depend on order |
| W1-22 | `--mirror` together with a refspec, or with `remote.origin.mirror=true`, fails: `fatal: --mirror can't be combined with refspecs` (local test) | https://git-scm.com/docs/git-push | MEDIUM | EXTENDS (closes G-30) |
| W1-23 | `'HEAD@{0 days ago}:refs/heads/main'` produces a six-field record. Only fields 2-4 are free of spaces. The fix is `line.rstrip("\n").rsplit(" ", 3)` (local test) | https://git-scm.com/docs/githooks, https://git-scm.com/docs/git-check-ref-format | HIGH | CONTRADICTS 04's "four fields every time" for an input 04 did not test (DOC-8) |
| W1-24 | `git send-pack` does not run pre-push. receive-pack runs on the server. A smart-HTTP POST to `$GIT_URL/git-receive-pack` does not run it | https://git-scm.com/docs/git-send-pack, https://git-scm.com/docs/gitprotocol-http | HIGH | SUPPORTS E17; EXTENDS (smart-HTTP untested in 04) |
| W1-25 | These do not run pre-push: libgit2 ("We will not be executing any hooks directly."), pygit2, dulwich ("✗ pre-push"), isomorphic-git (`onPrePush` callback only), the GitHub REST refs API and `gh api`. These do: JGit (`PrePushHook`, since 4.2) and GitPython (it shells out to `git push`, and `no_verify=True` maps to `--no-verify`) | https://github.com/libgit2/libgit2/issues/964; https://www.pygit2.org/remotes.html; https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt; https://isomorphic-git.org/docs/en/push; https://github.com/eclipse-jgit/jgit/blob/master/org.eclipse.jgit/src/org/eclipse/jgit/hooks/PrePushHook.java; https://github.com/gitpython-developers/GitPython/blob/main/git/remote.py; https://docs.github.com/en/rest/git/refs; https://cli.github.com/manual/gh_api | HIGH (JGit and isomorphic-git MEDIUM) | EXTENDS (04 could not test libraries; G-2) |
| W1-26 | The bypass list at design line 520 is CONFIRMED (J11) but imprecise. "Programmatic" pushes are not uniform, since JGit and GitPython run the hook. The list omits `--config-env`/`GIT_CONFIG_COUNT`, a worktreeConfig hooksPath and `hook.pre-push.enabled` | web-01 Area J (sources above) | HIGH | SUPPORTS D19-30 local forms (E14-E17); EXTENDS the list |
| W1-27 | Discrepancy: the 2.55.0 git-hook page reads as if `hook.<event>.enabled` already disables hookdir hooks. The 2.98.0 draft release note says that change is unreleased | https://git-scm.com/docs/git-hook; https://github.com/git/git/blob/master/Documentation/RelNotes/2.98.0.adoc | MEDIUM | EXTENDS (future bypass BP-12; DOC-11) |
| W1-28 | Community search: no primary mailing-list thread on hook behaviour. The closest hit is about message wording. A Stack Overflow question on empty pre-push stdin exists but could not be fetched | https://lore.kernel.ime.usp.br/git/d6161449aa19aebeb4c3bea1a751e8b5%40manjaro.org/T/; https://stackoverflow.com/questions/55112847/git-pre-push-hook-stdin-is-empty | LOW | Neither (source code and 04 are stronger) |

### 5.2 Linux publication primitives and git's executable check (web-02)

| # | Finding | Source URL | Relevance | Relation to 04 |
|---|---|---|---|---|
| W2-1 | git v2.47.3 decides that a hook is present only through `access(path, X_OK)` (`hook.c` line 21). A missing or non-executable hook makes `find_hook` return NULL, and `transport.c` lines 1295-1296 (`if (!hook_path) return 0;`) let the push proceed | https://github.com/git/git/blob/v2.47.3/hook.c; https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS and EXPLAINS E29 |
| W2-2 | The `advice.ignoredHook` hint prints only on EACCES with the advice enabled, once per hook name per process (`hook.c` lines 34-44). Turning the advice off never changes the outcome. A missing hook prints nothing | https://github.com/git/git/blob/v2.47.3/hook.c; https://github.com/git/git/blob/v2.47.3/Documentation/config/advice.txt | HIGH | SUPPORTS E29a, E29b |
| W2-3 | `access()` checks the real UID/GID. Root needs at least one execute bit. A noexec mount gives EACCES. Mode 0700 owned by a different user also fails open | https://man7.org/linux/man-pages/man2/access.2.html | HIGH | EXTENDS E29 (further fail-open causes) |
| W2-4 | An executable hook that exits nonzero, or that git cannot start, aborts the push (`transport.c` lines 1305-1307; line 1410 is `TRANSPORT_PUSH_NO_HOOK`). Failures inside the hook fail closed. Only the path and X_OK check fails open | https://github.com/git/git/blob/v2.47.3/transport.c | HIGH | SUPPORTS E19 |
| W2-5 | The hook path is the git-path `hooks/pre-push`. `core.hooksPath` redirects it (`path.c` lines 402-405); otherwise `path.c` line 104 (`common_list`) sends it to the common dir | https://github.com/git/git/blob/v2.47.3/path.c | HIGH | SUPPORTS E30, E31 |
| W2-6 | On ENOEXEC git retries the hook with `sh` (`run-command.c` lines 415-419 and 850-854). The `.exe` fallback applies only on Windows (`config.mak.uname`) | https://github.com/git/git/blob/v2.47.3/run-command.c; https://github.com/git/git/blob/v2.47.3/config.mak.uname | MEDIUM | EXTENDS |
| W2-7 | `link`/`linkat`: "If newpath exists, it will not be overwritten." Errors include EXDEV across mounts and EPERM where hard links are unsupported | https://man7.org/linux/man-pages/man2/link.2.html | HIGH | EXTENDS (publication is not covered by 04) |
| W2-8 | Writing in place with `O_CREAT|O_EXCL` gives EEXIST on a lost race, but readers can see a partly written file | https://man7.org/linux/man-pages/man2/open.2.html | MEDIUM | EXTENDS |
| W2-9 | `O_TMPFILE` + `linkat` needs Linux 3.11 and, on overlayfs, kernel 6.10. It returned ENOTSUP on this host's overlay `/tmp` (kernel 6.8.0-147) | https://man7.org/linux/man-pages/man2/open.2.html; https://lkml.iu.edu/hypermail/linux/kernel/2405.2/05667.html | HIGH | EXTENDS |
| W2-10 | `rename`/`os.replace` replaces an existing file silently, so a lost race gives no error | https://man7.org/linux/man-pages/man2/rename.2.html; https://docs.python.org/3/library/os.html | HIGH | CONTRADICTS the no-replace requirement (not a 04 observation) |
| W2-11 | `renameat2 RENAME_NOREPLACE` needs kernel 3.15 and glibc 2.28. It worked on this host's overlay. Python `os` does not expose it | https://man7.org/linux/man-pages/man2/rename.2.html; https://docs.python.org/3/library/os.html | MEDIUM | EXTENDS |
| W2-12 | The creation mode is `mode & ~umask`, while `fchmod` sets the mode exactly. Observed: 0755 under umask 077 became 0700, and `fchmod(0755)` gave 0755 | https://man7.org/linux/man-pages/man2/chmod.2.html; https://man7.org/linux/man-pages/man2/umask.2.html | HIGH | EXTENDS |
| W2-13 | Crash durability needs `fsync` of the file before publication and `fsync` of the directory after. `publish()` does neither. For a hook, a name lost in a crash is an E29-style fail-open | https://man7.org/linux/man-pages/man2/fsync.2.html; https://lwn.net/Articles/323412/; https://lwn.net/Articles/323170/; https://www.kernel.org/doc/mirror/ols2009.pdf | MEDIUM | EXTENDS |
| W2-14 | Discrepancy: open(2) BUGS says kernels without `O_TMPFILE` return EISDIR or ENOENT, but the glibc manual says EINVAL. Any use of `O_TMPFILE` must treat all of these, plus EOPNOTSUPP, as "unsupported" | https://man7.org/linux/man-pages/man2/open.2.html; https://snapshots.sourceware.org/glibc/trunk/latest/manual/html_node/Open_002dtime-Flags.html | LOW | Neither |
| W2-15 | End-to-end sandbox on git 2.47.3. Publication was temp file with `O_EXCL`, `fchmod 0755`, `fsync`, `link`, unlink, then directory `fsync`, and it installed the hook. A second install raised EEXIST, left the hook unchanged and left no temp file. A push to main was refused with rc 1 and "L2 guard: push to refs/heads/main refused". A feature push succeeded with rc 0. The same hook at mode 0644 was skipped with the hint, and main was pushed | local experiment (`/tmp/web02-sandbox.pVSjes6U`, removed) | HIGH | SUPPORTS E19, E29c |

Primitive comparison (condensed from web-02's primitive comparison table):

| Primitive | Replaces existing target | Atomic for readers | Lost-race error | Requirement |
|---|---|---|---|---|
| `open(final, O_CREAT|O_EXCL)` in place | no | no | EEXIST | any Linux |
| temp `O_EXCL` + `link`/`linkat` (the `publish()` pattern) | no | yes | EEXIST | same mount; hard-link support |
| `O_TMPFILE` + `linkat` | no | yes | EEXIST | Linux 3.11+; overlayfs 6.10 |
| `rename` / `os.replace` | yes, silently | yes | none | any |
| `renameat2 RENAME_NOREPLACE` | no | yes | EEXIST | Linux 3.15, glibc 2.28; ctypes from Python |
| `fchmod(fd, mode)` | n/a | n/a | EPERM, EROFS | umask does not apply |

### 5.3 Version table

Release-note URLs have the form `https://github.com/git/git/blob/master/Documentation/RelNotes/<version>.adoc` (web-01 F2).

| Behaviour | Introduced in | Release-note URL | Present in 2.47.3 |
|---|---|---|---|
| pre-push hook run by `git push`; a nonzero exit aborts the push | 1.8.2 | https://github.com/git/git/blob/master/Documentation/RelNotes/1.8.2.adoc (line 167) | yes (E1-E31) |
| `git push --no-verify` bypasses pre-push | 1.8.2 in code; documented from 1.8.4 | No release note. Source `v1.8.2:builtin/push.c` line 439; commit https://github.com/git/git/commit/90d32d1ffa36390177990cb92e4e2a68c5ec4092 | yes (E14) |
| `git worktree` (linked worktrees share refs, objects and hooks) | 2.5.0 (inferred: the note does not name the command) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.5.0.adoc (line 45) | yes (E30) |
| `core.hooksPath` | 2.9.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.9.0.adoc (line 127) | yes (E15, E16) |
| `rev-parse --git-path hooks/<hook>` honours `core.hooksPath` | 2.10.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.10.0.adoc (line 122) | yes (web-01 D3) |
| Per-worktree config (`config.worktree`, `extensions.worktreeConfig`) | 2.20.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.20.0.adoc (line 159) | yes (E31) |
| `git hook run` and the hook.c execution rewrite | 2.36.0 (inferred: no 2.36.0 bullet) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.37.0.adoc (line 285); https://git-scm.com/docs/git-hook change list | yes |
| Fixes for hook stdout regressions after the rewrite | 2.37.0, 2.38.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.38.0.adoc (line 295) | yes |
| `core.hooksPath` clone protection added, then reverted | added 2.39.4, reverted 2.39.5 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.4.adoc (line 55); https://github.com/git/git/blob/master/Documentation/RelNotes/2.39.5.adoc (line 20) | reverted state: yes |
| `core.hooksPath=/dev/null` documented as "disable hooks" | 2.50.0 (documentation only) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.50.0.adoc (line 313) | behaviour yes (E15); doc sentence no |
| pre-push in `transport.c` moved to the hook API | 2.54.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.54.0.adoc (line 213) | no (2.47.3 uses `find_hook` + `start_command`) |
| Hooks defined in configuration | 2.54.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.54.0.adoc (line 67) | no |
| Parallel configured hooks | 2.55.0 | https://github.com/git/git/blob/master/Documentation/RelNotes/2.55.0.adoc (line 7) | no |
| Remote groups in `git push` (keep pushing after a failure) | after 2.47.3 (exact version not found) | not found; https://git-scm.com/docs/git-push "REMOTE GROUPS" | no |
| `hook.<event>.enabled=false` also disables hooks-directory hooks | unreleased (master draft 2.98.0) | https://github.com/git/git/blob/master/Documentation/RelNotes/2.98.0.adoc (line 104) | no |

### 5.4 External recommendations and where this synthesis uses them

| Source | Recommendation (short) | Used in |
|---|---|---|
| web-01 R1 | Parse by right-splitting. Do not refuse records with more than four fields, or name that form in the diagnostic | T-4, SC-8, BP-14, DOC-8 |
| web-01 R2 | Compare field 3 exactly and case-sensitively; no normalisation | T-3, SC-10 |
| web-01 R3 | Empty stdin allows; an early nonzero exit is safe | T-5, T-6, SC-11 |
| web-01 R4 | Install and check through `rev-parse --path-format=absolute --git-path`, and check `git config --worktree` | L-2, L-3, SC-17 |
| web-01 R5 | L1 coverage list: `--no-verify`, `-c core.hooksPath`, `-c hook.pre-push.*`, `--config-env`, `GIT_CONFIG_*`, `send-pack`, `gh api` writes to refs, curl to `git-receive-pack`; in-process library pushes recorded as a limitation | 4.2 and 4.3 |
| web-01 R6 | Tests for "fetch first", the six-field record, SHA-256, a linked worktree and a `config.worktree` hooksPath | SC-6, SC-8, SC-9, SC-17 |
| web-01 R7 | Pin the git version assumption | BP-12, BP-13 |
| web-01 R8 | Revise design line 534 | DOC-1 |
| web-02 R1 | `publish()` shape with an executable `fchmod` and fsync of the file and the directory | L-4, SC-19 |
| web-02 R2 | Set the mode with `fchmod`, not with the open mode | L-5, SC-20 |
| web-02 R3 | Resolve the path with `rev-parse --path-format=absolute`; fail if the directory is missing | L-2 |
| web-02 R4 | Treat `FileExistsError` as "compare", never as success | L-7, SC-18 |
| web-02 R5 | Verify X_OK after install and check for noexec | L-8, SC-20 |
| web-02 R6 | No rename or replace; do not depend on `O_TMPFILE` or `renameat2` | L-6 |
| web-02 R7 | Never set `advice.ignoredHook=false` | L-10 |
| web-02 R8 | The executable bit makes L2 easy to disable, so a pre-flight check is needed | G-8, BP-6 |

### 5.5 External Research Summary

- **The contract is confirmed at source level.** githooks(5) for 2.47.3 matches the web page. `transport.c` at v2.47.3 explains file 04's observations:
  - Field 3 is `r->name`, so it is always fully qualified.
  - Exactly four rejection statuses are filtered, so "fetch first" reaches the hook. This corrects D19-47.
  - The hook starts even when there are no records.
  - EPIPE is tolerated.

  An exact, case-sensitive compare of field 3 is enough. The one parsing trap is that git itself can send more than four fields for an expression source, so the guard must right-split (web-01 G5, against D19-42/D19-23).
- **Placement uses a path that git resolves.** `rev-parse --path-format=absolute --git-path hooks/pre-push` covers linked worktrees, `core.hooksPath` (since 2.10.0) and the per-worktree override (since 2.20.0).
- **The hook is easy to skip.** Ways around it:
  - For one command: `--no-verify`, or a hooksPath set through `-c`, `--config-env` or `GIT_CONFIG_*`.
  - Persistently: a hooksPath in a config file, or a cleared executable bit. git fails open on the second and prints a hint that can be silenced.
  - Outside the git CLI: `send-pack` (observed, E17), and, documented externally (web-01 H/J) but not confirmed at runtime, smart-HTTP POSTs, the GitHub REST refs API, `gh api`, and in-process libraries (libgit2/pygit2, dulwich, isomorphic-git). Per the same documentation JGit and GitPython do run the hook.

  Several of these are ALLOWED or PARTIAL in L1 (4.3). So L1 plus L2 does not refuse "every push form" from a same-user agent, which matches design D19-32 and file 02's conclusion that server-side protection is the real control.
- **Publication has a tested standard-library recipe.** It is the existing `publish()` shape with `fchmod` to an executable mode and fsync of the file and the directory. It never replaces an existing file, and it was proven end to end on git 2.47.3 (W2-15). `rename`/`os.replace` must not be used, and `O_TMPFILE` fails on this host's overlay `/tmp`.
- **Version risk.** All of the above was tested on 2.47.3 only; it is not claimed for later versions. Re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (the pre-push hook API rewrite and configured hooks, 5.3; parallel configured hooks from 2.55.0) and when 2.98.0 ships (its draft makes `hook.pre-push.enabled=false` another bypass, which L1 would then have to cover). The guard tests record `git --version`.
- **Coverage.** Every Key External Finding and Recommendation of web-01 and web-02 appears in 5.1, 5.2 or 5.4. The Summary, Key Takeaways and Recommendations of files 01-04 are reflected in Sections 3 and 4.
