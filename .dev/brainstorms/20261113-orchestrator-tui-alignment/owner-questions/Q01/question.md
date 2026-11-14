# Q1: the git-config hole in the sweep's `git status` calls (INV-008)

## Owner update (2026-11-13, relayed by the team lead)

Part (a) is ANSWERED: "fix" (not accept, not F3). Still open, and now the real question:
- (a2) which fix shape: F1 neutralise (every worktree is still scanned, and no program that git configuration names can run), or F2 refuse and report (a worktree whose configuration could start a program is not scanned and is shown as `unscanned`), or a stated combination;
- (b) channel scope: `filter.<driver>.process`, `include.path`/`includeIf`, `GIT_CONFIG_*` and other inherited environment, per-worktree config (with `core.fsmonitor` and `filter.<driver>.clean`, all six measured running on 2026-11-13).

The first debate (proposals A, B, C and `adversarial/`) compared fix against accept; it is kept as the record of part (a). The debate for (a2) and (b) is in `a2/` (proposals and `a2/adversarial/`). The fix's code is never specified here.

### Facts added for (a2), read-only checks on this host, 2026-11-14

| Fact | Source |
|---|---|
| The system git configuration (`/etc/gitconfig`, scope "system") defines a git-lfs filter for every repository on this host: `filter.lfs.clean`, `filter.lfs.smudge`, `filter.lfs.process` and `filter.lfs.required`. git-lfs 3.6.1 is installed. So every worktree inherits a configured filter program. | `git config --show-origin --show-scope --get-regexp` in this checkout (read-only) |
| A configured filter runs during `git status` only for files whose `.gitattributes` select it. This IronClaude checkout has no `.gitattributes` that selects `filter=lfs`; whether any of the other listed worktrees (other repositories) use LFS is UNVERIFIED. | `grep` for `filter=lfs` in this checkout; worker brief ("`.gitattributes` alone ran nothing"; a program runs only if config names it) |
| Consequence for F2 read literally ("refuse any worktree that defines them"): every worktree on this host defines a filter through the system config, so every worktree would be reported `unscanned` unless the refusal rule counts only programs that could actually run for that worktree, or the owner names trusted programs. | inference from the two rows above (PLAN INFERENCE) |
| Consequence for F1: in a repository that does use LFS, disabling the filter could make `git status` report LFS files as changed when they are not. Not measured; UNVERIFIED. | inference (PLAN INFERENCE) |
| The environment channel is routinely non-empty: this session's environment carries `GIT_CONFIG_COUNT=2` with keys `credential.interactive` and `credential.guiPrompt` (values not read). These do not name a program `git status` runs, but a rule that refuses on any `GIT_CONFIG_*` variable would refuse every sweep run from such a session. Whether the coordinator's environment is the same is UNVERIFIED. | `env` key names in this session (read-only) |

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q1 (line 528).

> (a) INV-008: fix the `git status` hole (F1 neutralise both keys, F2 refuse and report `unscanned`) or accept the risk with caveats (F3); (b) does your ruling cover `filter.<driver>.process`, config pulled in by `include.path`/`includeIf`, and inherited `GIT_*`/`GIT_CONFIG_*` variables? (part (b) widened by this debate, R25-INV-004)

Original wording (ADJ Part 7, line 771): "The Codex security thread on PR #539: fix the `git status` hole (neutralise both `core.fsmonitor` and `filter.*.clean`, or refuse any worktree that defines them and show it as `unscanned`) or accept the risk and add a caveat to four "read-only" texts?"

## Recommended answer in the spec

(a) Fix by F1 or F2 (about 70 percent; marked PLAN INFERENCE in ADJ, derived from the probe; a default, not a debate verdict); (b) yes to all, and the ruling names any channel it leaves out. (`merged-requirements.md:528`; ADJ line 771, line 206)

## Default if unanswered

ADJ: PR #539 stays open and no caveat is added (SEED Batch 3 item 9). (`merged-requirements.md:528`)

## What it gates (work items, in words)

- SW-01 (record the owner's ruling as a reply on the Codex security thread on PR #539 and as a ledger row). Its acceptance criteria require the ruling to state which premise it relies on, whether the allow-list edit is authorised, and which config channels are in scope. (`merged-requirements.md`, section 2, SW-01 row)
- SW-02 (implement the ruling inside PR #539: for a fix, a regression test that reproduces the probe experiment and covers every channel the ruling puts in scope; for acceptance, a caveat on every "read-only" or "changes nothing" statement in #539's files). (section 2, SW-02 row)
- SW-05 (refresh PR #539's merge reference and merge it), and through it everything behind the merge: the post-merge sweep fixes, the contract note links, the one real-id comparison between the observer and the sweep (XC-04, which must never run the unfixed sweep), the v2 start gate, and the sweep becoming runnable on this host. (section 2, SW-05 row "blocks" column; XC-04 row)
- Wave needed by: W0 (the first wave: owner answers before any code). Q1 is asked first of all owner questions. (`merged-requirements.md:523`)

## Facts the question depends on

| Fact | Source |
|---|---|
| Measured on 2026-11-13 with git 2.47.3: the sweep's `git status` call ran a command configured in `core.fsmonitor`, in `filter.<driver>.clean`, in `filter.<driver>.process`, in config pulled in by `include.path`, in per-worktree config, and from `GIT_CONFIG_*` environment variables. | Worker brief, hard rule on Q1 (measurement of 2026-11-13) |
| Passing `-c core.fsmonitor=false` stopped only the fsmonitor hook; the clean filter still ran. So the remedy the Codex thread suggests (filter to the selected repository and disable executable git config) is not one flag. | Worker brief; ADJ Part 2.2 action 1 (line 206); ADJ Part 8 row INV-008 (line 817) |
| A clone cannot ship config, and a `.gitattributes` file alone ran nothing. A program runs only if some config on this host (shared repo config, per-worktree config, an included file, or the environment) names it. | Worker brief |
| At least 18 of the 29 listed worktrees share one `.git/config`, so a filter to one repository does not protect them. | ADJ line 206; INV-008 row (line 456) |
| Severity was judged Medium in practice on this single-owner, single-host setup (the probe labelled the finding HIGH in the abstract). | Worker brief; ADJ line 456 (HIGH) |
| A fix is not a one-liner: the git allow-list `ALLOWED_GIT` is an exact one-entry list under the owner-signed allow-list (NFR-014), and three tests pin the git argument prefix. | ADJ line 206; INV-009 (line 460) |
| Narrowing which paths `git status` scans also changes the contract allow-list and transcript scans, which share the same path list; the git-status scope has to be separated from them. | ADJ line 206; INV-039 (line 469) |
| Under acceptance (F3), at least 16 statements in #539's files call the sweep read-only or say it changes nothing, not four; two of them sit in a mirror that must stay byte-equal. | Probe INV-011 (`adversarial/adversarial/invariant-probe.md` line 19); `merged-requirements.md:562` |
| The adopted regression test idea covered only fsmonitor and `.clean`; a fix that blanks only `.clean` would pass it while a `.process` driver still runs. Part (b) of Q1 exists to close that gap. | Probe INV-004 (`invariant-probe.md` line 12) |
| Every Claude session launched on this host runs with permission checks off, so the "lower-privileged agent" premise behind treating this as an escalation may not hold here. | ADJ E-11 (line 137); ADJ line 206 |
| An acceptance is reversible only before merge; a fix choice is reversible. | SW-01 row "undo"; ADJ line 456 |
| Q1's risk choice does not authorise arbitrary git allow-list edits (NFR-014). | `merged-requirements.md:571` |
| The design of the fix belongs to the #539 author and the owner; no document in this program specifies the code. | ADJ line 206; probe INV-018 (line 26) |
