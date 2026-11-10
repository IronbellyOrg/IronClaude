# Synthesis 03: Options, Recommendation and Implementation Plan (Sections 6-8)

- **Topic:** L2 pre-push guard that refuses a governed AI agent's push to `refs/heads/main` or `refs/heads/master`
- **Date:** 2026-11-08
- **Sources read:** `research/01-identity-selector-ancestry.md`, `research/02-l1-guard-push-bypass-coverage.md`, `research/03-design-and-claim-code-crossvalidation.md`, `research/04-empirical-git-prepush-experiments.md`, `research/web-01-git-official-docs-and-versions.md`, `research/web-02-linux-atomic-publication-and-exec-bit.md`, `gaps-and-questions.md` (G-1..G-43). No synth file was read.
- **Design constraint quoted from source:** `docs/designs/sc-issue-launch-level-hook.md` lines 510-514 (re-read 2026-11-08). Line 510: "one owned shared `hooks/pre-push` plus a private-worktree marker, no config change, and no push-hook forwarding". Line 512: "Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow foreign hooks, generate name-only stubs, or buffer/replay someone else's push hook in this increment." Line 514: "Conflict or unsupported lookup: preserve all existing files/configuration; report `W-L2-ABSENT` with the reason."
- **Nature of this document:** proposals for a brainstorm. Nothing here changes code.
- **Evidence tags used:** `[CODE-VERIFIED]` (current architecture), `[CODE-CONTRADICTED]` (corrected), `[UNVERIFIED]` (only in Open Questions), `[EXTERNAL]` (web research, with source URL), `[OBSERVED 2.47.3]` (file 04 or a web-file sandbox run on the installed git).

---

## 6. Options Analysis

The options differ on three axes: **where the hook lives** (placement), **how it is published** (no-replace install) and **how it identifies the actor** (selector call). Placement is the axis that decides design 19.2 compliance; publication and identity are shared sub-choices described once after the three placement options.

```
                      git push (from main checkout or linked worktree)
                                        |
            git resolves hooks/pre-push through the git-path machinery
            (path.c line 104 common dir; lines 402-403 core.hooksPath)  [EXTERNAL web-02]
                                        |
      +---------------------------------+----------------------------------+
      |                                 |                                  |
 Option A                          Option B                           Option C
 default lookup                    core.hooksPath set (global/local)  extensions.worktreeConfig=true
 <common>/.git/hooks/pre-push      <dir>/pre-push, e.g. under         + core.hooksPath in
 (E30: linked worktree uses it;    ~/.claude/hooks                    .git/worktrees/<id>/config.worktree
 private-dir hooks/ ignored)       (E15/E16, web-01 C1)               (E31, web-01 C4)
      |                                 |                                  |
 19.2 COMPLIANT                    EXCLUDED by 19.2                   EXCLUDED by 19.2
```

### Option A: Owned shared hook in the default common-dir lookup

**Placement.** One owned `pre-push` at the path printed by `git rev-parse --path-format=absolute --git-path hooks/pre-push`, run from the target worktree, installed only when `core.hooksPath` is unset (the "supported default" of design line 512).

| Evidence | Source |
|---|---|
| A linked worktree's default lookup is the common dir `clone/.git/hooks/pre-push`; a hook in the worktree-private git dir is ignored | [OBSERVED 2.47.3] 04 E30; [EXTERNAL] gitrepository-layout(5) `hooks` entry, https://git-scm.com/docs/gitrepository-layout (web-01 D1) |
| `--path-format=absolute --git-path hooks` resolves the common dir from a linked worktree and honours `core.hooksPath` (since 2.10.0) | [OBSERVED 2.47.3] web-01 D3a, D3c-e; [EXTERNAL] RelNotes 2.10.0 line 122, https://github.com/git/git/blob/master/Documentation/RelNotes/2.10.0.adoc |
| `--git-path` is relative in the main clone and absolute in a linked worktree; `l2_status` joins a relative answer to the worktree | [OBSERVED 2.47.3] 04 E30; [CODE-VERIFIED] `orca_worktree.py` lines 1012-1029 (03) |
| `git worktree remove` deletes a private-dir marker; the shared hook stays | [OBSERVED 2.47.3] 04 F2 |
| One hook file serves every worktree, so the hook decides per push which actor it serves | [EXTERNAL] web-01 D1 (design 19.4 "shared hook file") |

**Publication.** A new raw-bytes, executable-mode variant of the `publish()` pattern (see "Shared sub-choice 1" below).

**Identity.** `~/.claude/hooks/launch-job-identity.sh identify` with no PID (see "Shared sub-choice 2").

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | Medium. New code: hook body, raw-bytes publisher, ownership check, self-test, reason-bearing `W-L2-ABSENT`; `install_hooks.py` has no git-hook path today | [CODE-VERIFIED] 03 "Design gaps for an L2 installer"; 01 §6 |
| Risk | Medium. Same-user agent can still edit, delete or `chmod -x` the hook file (no `.git/hooks` tamper token in L1 line 706), and per-process bypasses remain | [CODE-VERIFIED] 02 Gap 1; [OBSERVED 2.47.3] 04 E14-E17, E29, E31 |
| Reuse: `publish()` | Pattern reused, function not: `publish()` JSON-encodes the payload, sets mode 0400 and sits inside the heredoc, so it is not importable | [CODE-VERIFIED] 01 §6, `launch-job-identity.sh` lines 164-174; web-02 Discrepancy 1 |
| Reuse: `identify` | Reused unchanged; selector returns governed/ordinary/unknown on stdout with exit 0; hook must map "no verdict" to `unknown` | [CODE-VERIFIED] 01 §4 items 1-3 (lines 225, 241, 242, 244, 536) |
| Reuse: `l2_status` | Reused as the probe; it already resolves the path with `rev-parse --git-path hooks/pre-push` | [CODE-VERIFIED] 03, ow:1020 |
| Files affected | `src/superclaude/hooks/scripts/` (new hook body), `src/superclaude/cli/install_hooks.py` (`_FRESHNESS_SCRIPTS`), `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (`cmd_launch`, `l2_status`, `L2_ABSENT_WHY`), `src/superclaude/hooks/scripts/launch-level-guard.sh` (line 706 token), plugin mirrors, tests | 01 §8; 03 Summary; 02 line 168 |
| Pros | Matches the git default with no config change; covers linked worktrees through the common dir; probe code already uses the same path resolution; no-replace publish proven end to end | 04 E30; web-02 Area 3 steps 8a-8f |
| Cons | Shared with the person's own pushes in every worktree of the repository; fails open when the exec bit is cleared; bypassed by `--no-verify`, `-c core.hooksPath`, `send-pack`, library and API pushes; L1 does not protect the file | 04 Key Takeaways; web-02 Area 1; 02 Summary; historical rejection at `.dev/brainstorms/20261105-170229-launch-level-hook/refactor-plan.md:1158` (03) |
| **Design 19.2 compliance** | **Compliant.** One owned shared hook in the default lookup; no `extensions.worktreeConfig`; no `core.hooksPath` migration; no forwarding or shadowing (a foreign `pre-push` or a set `core.hooksPath` leads to `W-L2-ABSENT`, never to installation) | design lines 510-514 |

### Option B: Dedicated `core.hooksPath` directory (for example under `~/.claude/hooks`)

**Excluded by design 19.2; would reopen the decision.** Kept only as a comparison point.

**Placement.** Set `core.hooksPath` (repository or global scope) to a directory owned by the installer, for example under `~/.claude/hooks/`, and put the guard there.

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | Medium-high. Needs the same hook body and publisher as A, plus a config write and a plan for every other hook name that the redirected directory would now hide | [EXTERNAL] git-config(1) core.hooksPath: hooks are looked up "in that directory ... instead of in $GIT_DIR/hooks", https://git-scm.com/docs/git-config (web-01 C1) |
| Risk | High for coexistence: redirecting the hooks directory hides every existing hook (`pre-commit`, `commit-msg`) unless they are forwarded, which 19.2 forbids. Per-process `-c core.hooksPath=` still overrides it | web-01 C1, C2; [OBSERVED 2.47.3] 04 E15/E16 |
| Reuse: `publish()` | Same as A (pattern only) | 01 §6 |
| Reuse: `identify` | Same as A | 01 §4 |
| Files affected | As A, plus a git-config writer (new code) | 03 "Design gaps" |
| Pros | The existing L1 `*.claude/hooks*` tamper token (line 706) would already protect the hook files from Edit/Write and spelled Bash paths, and the `hookspath` token (line 532) already refuses changing `core.hooksPath` through git | [CODE-VERIFIED] 02 line 169 |
| Cons | Config migration; hides other hooks; a relative `core.hooksPath` resolves per worktree root inside the agent-editable working tree; `hookspath` token applies only when a git word is present (line 525), so a direct config-file write escapes it | [OBSERVED 2.47.3] 04 E30d, web-01 D3d; [CODE-VERIFIED] 02 Gap 3 |
| **Design 19.2 compliance** | **Not compliant: "migrate `core.hooksPath`" is forbidden (line 512). Excluded by design 19.2; would reopen the decision.** | design line 512 |

### Option C: Per-worktree `core.hooksPath` with `extensions.worktreeConfig`

**Excluded by design 19.2; would reopen the decision.** Kept only as a comparison point.

**Placement.** Enable `extensions.worktreeConfig` and write `core.hooksPath` into the governed worktree's `config.worktree`, so only that worktree uses the guard directory.

| Criterion | Assessment | Evidence |
|---|---|---|
| Effort | High. Enabling a repository extension plus per-worktree config writes and cleanup on release | [EXTERNAL] git-worktree(1) CONFIGURATION FILE: "Older Git versions will refuse to access repositories with this extension", https://git-scm.com/docs/git-worktree (web-01 D1) |
| Risk | High. The extension changes how every git in the repository reads config; a per-worktree value "will override settings from any other config files", which is also the very bypass an agent can use against Option A | [EXTERNAL] git-config(1) extensions.worktreeConfig (web-01 C4); [OBSERVED 2.47.3] 04 E31 |
| Reuse: `publish()` | Same as A (pattern only) | 01 §6 |
| Reuse: `identify` | Same as A; per-worktree placement would not remove the need for actor selection because a human can push from the same worktree (design 19.5 actor cases) | 01 §4; design line 532 |
| Files affected | As A, plus extension enablement and `config.worktree` writer (new code) | 03 "Design gaps" |
| Pros | Scopes the guard to one worktree; human pushes from sibling worktrees and the main checkout are untouched | [OBSERVED 2.47.3] 04 E31 |
| Cons | `config.worktree` is not an L1 tamper token (line 706), so the agent can rewrite it; enabling the extension is repository-wide | [CODE-VERIFIED] 02 Gap 10, Stale Documentation (LL-TAMPER partial) |
| **Design 19.2 compliance** | **Not compliant: "Do not enable `extensions.worktreeConfig`" and "migrate `core.hooksPath`" (line 512). Excluded by design 19.2; would reopen the decision.** | design line 512 |

### Shared sub-choice 1: how the hook is published (applies to A, B and C)

| Primitive | Replaces an existing file | Reader-atomic | Verdict for the hook | Evidence |
|---|---|---|---|---|
| Copy of `publish()` pattern with raw bytes, `fchmod` to an executable mode, `fsync` file and directory, `linkat` no-replace, temp unlink in `finally` | no (EEXIST) | yes | **Use.** Proven on this host: installed mode 0755 with X_OK, second install raised EEXIST and left the hook unchanged, no temp left, push to main refused (rc 1), feature push allowed (rc 0) | [OBSERVED 2.47.3] web-02 Area 3 steps 8a-8f; [CODE-VERIFIED] `publish()` lines 164-174 (01 §6) |
| `publish()` unchanged | no | yes | **Do not use.** Mode 0400 fails `access(X_OK)`, so git skips the hook (fail-open); payload is JSON-encoded | web-02 Area 3 step 7; 01 §6 |
| `os.rename` / `os.replace` | yes, silently | yes | **Do not use** (violates "without replacing an existing file", design line 512) | web-02 Area 3 step 5; [EXTERNAL] https://man7.org/linux/man-pages/man2/rename.2.html |
| `O_TMPFILE` + `linkat` | no | yes | **Do not depend on it.** EOPNOTSUPP on this host's overlay `/tmp` (overlayfs needs 6.10; kernel is 6.8) | web-02 Area 3 step 4x; [EXTERNAL] https://man7.org/linux/man-pages/man2/open.2.html |
| `renameat2(RENAME_NOREPLACE)` | no | yes | **Not needed.** Worked here, but needs ctypes and can return EINVAL on unsupported filesystems; no gain over `linkat` | web-02 Area 3 step 6a/6b, Recommendation 6 |

Mode must be set with `fchmod` on the fd, because creation mode is masked by umask (0755 under umask 077 became 0700) [OBSERVED] web-02 Area 3 steps 1a/1b.

### Shared sub-choice 2: how the hook identifies the actor

The verdict mapping is DECIDED by the owner (2026-11-08, seed brief line 73, recorded in 01 §4): governed refuses protected; ordinary and released allow without reading the stream; `unknown` refuses only `main`/`master` with a distinct diagnostic and allows the rest. The hook must also map "no verdict" (non-zero exit, empty or unparseable stdout, unexpected `status`) to `unknown` [CODE-VERIFIED] 01 §4 item 3.

| Variant | How | Human without uv on PATH | Effort / reuse | Evidence |
|---|---|---|---|---|
| A-i: uv-backed `identify` with a fixed PATH | Hook sets PATH to include the uv directory recorded at install time, then calls `~/.claude/hooks/launch-job-identity.sh identify` with no PID | Covered (uv resolvable at script lines 25 and 566) | Lowest: selector reused unchanged; uv and Python start per push (cost not measured) | 01 §4 item 5 option (i), §8; 04 E28c |
| A-ii: hook-side no-store early exit | Hook treats an absent `$HOME/.claude/state/launch-level` as `ordinary` without calling `identify` | Covered only on machines with no store; does NOT help a human on a machine that also runs governed sessions | Small, but insufficient alone | 01 §4 item 5 option (ii) |
| A-iii: pure-shell hook | Hook does not depend on uv | Covered | Highest: research gives no design for re-implementing the selector's validation in shell; the three byte-identical copies of the selector would need a second implementation kept in step | 01 §4 item 5 option (iii), §8 Key Takeaways |
| Absolute uv path only | Hook calls uv by absolute path | **Not covered:** the script itself resolves uv through PATH at lines 25 and 566 | n/a | 01 §4 item 5; gaps note N-3 (superseded sentence at 04 line 1530) |

**Note on the stdin parser (applies to every variant).** git can itself send a record with more than four space-separated fields: `git push --dry-run origin 'HEAD@{0 days ago}:refs/heads/main'` gave a six-field record [OBSERVED 2.47.3] web-01 G5. A four-variable `read` puts `ago}` in field 3 and lets the protected push through. Fields 2-4 never contain spaces (`r->name` and hex oids, git v2.47.3 `transport.c` lines 1322-1324, [EXTERNAL] https://github.com/git/git/blob/v2.47.3/transport.c, web-01 Area I), so the exact parse is a right-split into four parts. This **contradicts** design 19.3's "A malformed governed stream (missing/extra fields) refuses" for the extra-fields case: web-01 G5 (local run) is the stronger evidence; file 04 never produced a malformed record (04 Gaps; its F3 follow-up tested space/tab/trailing-space in destination names only, which git refuses before the hook).

### Options Comparison

| Criterion | Option A: default common-dir hook | Option B: dedicated `core.hooksPath` dir | Option C: per-worktree `core.hooksPath` + `extensions.worktreeConfig` |
|---|---|---|---|
| **Design 19.2 compliance** | **Compliant** (lines 510-514) | **Excluded by design 19.2; would reopen the decision** (migrates `core.hooksPath`) | **Excluded by design 19.2; would reopen the decision** (enables `extensions.worktreeConfig`, migrates `core.hooksPath`) |
| Config change | None | Repository or global `core.hooksPath` | Repository extension + `config.worktree` |
| Effect on existing hooks (`pre-commit`, `commit-msg`) | Untouched (design line 510) | Hidden unless forwarded (forwarding forbidden) | Hidden in that worktree unless forwarded |
| Linked worktree coverage | Yes, common dir (E30) | Yes for an absolute path; a relative path resolves per worktree root (E30d, web-01 D3d) | Only the configured worktree (E31) |
| Path resolution already in code | Yes, `l2_status` uses `rev-parse --git-path hooks/pre-push` (ow:1020) | Same call honours `core.hooksPath` (2.10.0) | Same call honours it (web-01 D3c-e) |
| Publication | Raw-bytes executable variant of `publish()` pattern (web-02 Area 3 step 8) | Same | Same |
| Actor identification | `identify` + fixed PATH (A-i) | Same | Same (still needed: human and agent can share a worktree, design line 532) |
| L1 protection of the hook file today | None (no `.git/hooks` token, line 706) | Yes, `*.claude/hooks*` token and `hookspath` token (02 line 169) | None (`config.worktree` not a token) |
| Per-process bypass (`--no-verify`, `-c core.hooksPath=`, `--config-env`, `GIT_CONFIG_COUNT`) | Bypassable (E14-E16, web-01 C2) | Bypassable | Bypassable (`-c` beats `config.worktree`, web-01 C4) |
| Exec-bit fail-open (E29) | Yes | Yes | Yes |
| `send-pack`, libgit2/pygit2, dulwich, isomorphic-git, REST/`gh api`, raw smart-HTTP | Bypass (E17, web-01 J10) | Bypass | Bypass |
| Effort | Medium | Medium-high | High |
| Coexistence risk | Low (refuses to install on conflict) | High | High |

Reading of the table: A and B have the same bypass surface for pushes; B's only advantage is that L1 already protects `~/.claude/hooks`. That advantage can be obtained for A by adding `*.git/hooks*` and `*hooks/pre-push*` to L1 line 706 (02 line 168), without a config migration. C adds risk (repository extension) and gains only per-worktree scoping, which the identity selector already provides by actor.

---

## 7. Recommendation

**Recommended: Option A (owned shared hook in the default common-dir lookup), with identity variant A-i (uv-backed `identify` called under a fixed PATH that holds the install-time uv directory) and the raw-bytes executable `publish()`-pattern installer.** No reopening of design 19.2 is recommended.

| Reason | Comparison-table row | Evidence |
|---|---|---|
| A is the only option that complies with 19.2; B and C would reopen it | "Design 19.2 compliance" | design lines 510-514 |
| A, B and C have an identical push-bypass surface, so B and C buy no extra protection for the push itself | "Per-process bypass", "Exec-bit fail-open", "`send-pack` ... smart-HTTP" | 04 E14-E17, E29; web-01 J10 |
| B's one real advantage (L1 already protects `~/.claude/hooks`) is reachable for A by a token change in L1, not a config migration | "L1 protection of the hook file today" | 02 lines 168-169 |
| A leaves `pre-commit`, `commit-msg` and every other hook untouched; B and C hide them unless forwarded, which 19.2 forbids | "Effect on existing hooks" | design line 510, 512 |
| A already matches the path resolution the claim code uses | "Path resolution already in code" | `l2_status` ow:1012-1029 [CODE-VERIFIED] |
| A's installer pattern is proven end to end on this host | "Publication" | web-02 Area 3 steps 8a-8f |
| A-i is the only identity variant that covers a human without uv on PATH with no second selector implementation | Shared sub-choice 2 table | 01 §4 item 5; 04 E28c |

**Status of the identity choice.** G-6 lists the uv-PATH remedy as "design choice open: brainstorm decision". The recommendation is A-i; the brainstorm owns the final pick between A-i and A-iii.

**What L2 under Option A does NOT stop, and who must close it.** The design already accepts that "`--no-verify`, per-process hooksPath overrides, direct send-pack and API/programmatic ref writes can bypass local pre-push; visible forms remain checked by L1" (line 520). The research confirms each class and adds more.

| Bypass | L2 result | L1 today | Proposed owner | Evidence |
|---|---|---|---|---|
| `git push --no-verify` | hook never runs | refused (not canonical form) | L1 (keep) | 04 E14; 02 Summary; [EXTERNAL] git-push(1), https://git-scm.com/docs/git-push |
| `git -c core.hooksPath=...`, `--config-env=core.hooksPath=VAR`, `GIT_CONFIG_COUNT/KEY/VALUE` env | hook never runs | `-c` form refused (`hookspath` token); `\x50` spelling and env forms evade (02 line 249) | L1 (extend: `--config-env`, `GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`) | 04 E15/E16; [EXTERNAL] web-01 C2, https://git-scm.com/docs/git-config |
| `git send-pack` | hook never runs; force-rewrote main | refused | L1 (keep) | 04 E17; [EXTERNAL] web-01 H1 |
| Edit/Write/rm/mv/ln on `.git/hooks/pre-push` | guard removed or replaced | **allowed** (no token at line 706) | L1 (add `*.git/hooks*`, `*hooks/pre-push*`) | 02 Gap 1 |
| `chmod -x` on the hook (+ `-c advice.ignoredHook=false`) | git skips it (fail-open) | allowed | L1 token above + launch-time `access(X_OK)` recheck (L2 installer) | 04 E29; web-02 Area 1 (`hook.c` lines 21, 34-46) |
| Per-worktree `core.hooksPath` via `config.worktree` | different hooks dir | allowed (`config.worktree` not a token) | L1 (add `*config.worktree*`) + launch-time effective-path recheck | 04 E31; 02 Gap 10 |
| Direct write to `.git/config` without a git word (`cd .git && >> config`) setting `core.hooksPath`, `alias.*`, `remote.origin.push` | `core.hooksPath` removes L2; `remote.origin.push` is still seen as field 3 (E20) | allowed | L1 (move `hookspath`/`alias.` out of the `LL_GIT` gate, line 525) | 02 Gap 3, line 170 |
| Underscore env prefix moving command position off `git` (`A_B=1 git $'\x70ush' --no-verify origin main`) | `--no-verify` part removes L2 | allowed at every level | L1 (fix W/command-position at lines 435, 556-557) | 02 Gap 2, Summary |
| `setsid` or a different valid HOME | selector returns `ordinary`, push allowed | n/a | Accepted limit (design 19.7 line 559 lists `setsid`; HOME escape listed nowhere) | 01 §4 item 4, Gaps 2 |
| libgit2/pygit2, dulwich, isomorphic-git (no `onPrePush`) in a script | hook never runs | allowed (library and script pushes pass) | Stated limitation; only server-side protection covers in-process pushes | [EXTERNAL] web-01 J1, J2, J4, J5 (https://github.com/libgit2/libgit2/issues/964, https://github.com/jelmer/dulwich/blob/main/docs/c-git-compatibility.txt); 02 Gap 6 |
| GitHub REST refs API / `gh api` | hook never runs | `gh api` writes and literal `api.github.com` refused; non-literal hosts not | L1 (keep; extend hosts) + server-side | [EXTERNAL] web-01 J7/J8, https://docs.github.com/en/rest/git/refs; 02 Gap 5 |
| `curl` to smart-HTTP `git-receive-pack` on `github.com` | hook never runs | **allowed** | L1 (add) | [EXTERNAL] web-01 H3, https://git-scm.com/docs/gitprotocol-http; 02 Gap 5 |
| GitPython `Remote.push(no_verify=True)` | hook never runs (maps to `--no-verify`, convention untested) | allowed (script) | Stated limitation | [EXTERNAL] web-01 J6 |
| Future git: `-c hook.pre-push.enabled=false` (unreleased 2.98.0 draft) | would disable hookdir hook | no token | L1 (add when the runtime git has it) | [EXTERNAL] web-01 F1, RelNotes 2.98.0 line 104 |

Neither layer closes the in-process library push or the API write in general; 02's Summary and web-01 J11 both conclude that server-side branch protection is the only control that does. The design's own disclaimer ("Neither layer guarantees universal AC-6 or a hostile-agent sandbox", line 520) stands.

**Launch refusal versus warning.** Design lines 355 and 514 say the governed launch must not proceed when accepted L2 is absent; the code warns and continues (`W-L2-ABSENT`, ow:1311-1312) by a documented choice (design line 574) [CODE-CONTRADICTED vs design: D19-18]. The owner has DECIDED the default (seed brief line 77): it stays off, so `W-L2-ABSENT` remains a warning. The refusal path must still be built in its own clearly marked commit, tested, and shipped switched off (seed brief line 68). Two points stay open (G-17, OQ-7): the switch mechanism (constant, environment variable or file) and the criterion for turning it on (after #442). Phase 4.4 below builds the refusal behind that switch.

---

## 8. Implementation Plan

Proposed steps for the brainstorm; nothing here has been changed. File paths marked **(new)** do not exist today. Every other path was cited as existing by research files 01-03 [CODE-VERIFIED]. Line numbers are those the research recorded on 2026-11-08 and must be re-read before any edit.

```
 cmd_launch (orca_worktree.py 1253-1388)
   |
   +-- IR-4 enforcement_preflight ............ 1287-1304   (unchanged)
   +-- [new] l2_install(worktree)  ........... Phase 4.1
   |       resolve  git rev-parse --path-format=absolute --git-path hooks/pre-push
   |       check    core.hooksPath unset (repo + --worktree)       --> conflict: keep files, W-L2-ABSENT(reason)
   |       check    no foreign pre-push                            --> conflict: keep files, W-L2-ABSENT(reason)
   |       publish  O_EXCL temp -> fchmod 0755 -> fsync -> link -> unlink -> fsync dir
   |       verify   full bytes == installed source, X_OK, owner, mode, not noexec
   |       selftest ordinary+protected -> 0 ; empty stream -> 0
   +-- l2_status (1012-1029), now reason-bearing ............ Phase 4.2
   +-- W-L2-ABSENT note (1311-1312) / refusal, switch off by default ... Phase 4.3 / 4.4
   +-- publish_pending (1315) -> launch (1330-1334) -> session_report (1376)

 git push (any actor)  -->  <common-dir>/hooks/pre-push  (Phase 1 body)
   fixed PATH -> ~/.claude/hooks/launch-job-identity.sh identify
   verdict: governed | unknown | no-verdict(=unknown) -> refuse if any field 3 == refs/heads/main|master
            ordinary | released                       -> allow
```

### Phase 1: Hook body

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Create the guard script source | `src/superclaude/hooks/scripts/launch-pre-push-guard.sh` **(new)**; mirror `plugins/superclaude/hooks/scripts/launch-pre-push-guard.sh` **(new)** | The name is a proposal. Mirrors the three-copy layout of `launch-job-identity.sh` (src, plugin, installed; 01 §5). The bytes of this file are what the publisher writes as `pre-push` (Phase 2), so the ownership check compares against them. |
| 1.2 | Set a fixed PATH before any lookup | same file | Variant A-i: `PATH` set to the install-time uv directory plus `/usr/bin:/bin`. Reason: with `PATH=/usr/bin:/bin` uv is absent and `identify` exits 2 (04 E28c; 01 lines 25, 52-53). An absolute uv path alone is not enough (01 §4 item 5). Resolves G-6 if the brainstorm accepts A-i. |
| 1.3 | Call the selector by its installed entry point (proposed; conditional on OQ-20) | same file | Proposed location: `~/.claude/hooks/launch-job-identity.sh identify` (01 §5; ow:803 `IDENTITY_COMMAND`). The environment reaches the hook unchanged (04 E28), so the selector sees the pusher's session. Bound the call with a timeout; a timeout is "no verdict". Missing script is "no verdict" (G-36). |
| 1.4 | Map verdicts | same file | `governed` and `unknown` restrict; `ordinary` and `released` allow (01 lines 225, 241-244). "No verdict" (exit 2, bad args line 564, missing script, timeout) maps to `unknown` (01 Gaps 1; G-7). Owner decision 2026-11-08: `unknown` refuses main/master only, with a diagnostic, and allows every other ref (seed brief line 73, cited by 01). |
| 1.5 | Parse stdin records by right-splitting | same file | Split each line from the right into 4 fields (`rsplit(" ", 3)` semantics) because field 1 can contain spaces: `HEAD@{0 days ago}:refs/heads/main` produced 6 whitespace fields and a naive `read` let the protected push through ([EXTERNAL] web-01 G5, https://git-scm.com/docs/githooks). Malformed = fewer than 4 fields, or fields 2/4 not hex object names → refuse when restricted. This replaces design 19.3's "extra fields refuse" (line 518), which would refuse a legitimate push (web-01 G5 is the stronger, executed evidence). |
| 1.6 | Compare field 3 exactly | same file | Refuse the whole push if any field 3 is byte-equal to `refs/heads/main` or `refs/heads/master`. Field 3 is fully qualified by code (`r->name`, transport.c v2.47.3 1322-1324; [EXTERNAL] web-01) and authoritative for every spelling tried (04 E3-E6, E11, E20, E21). Case-sensitive (web-01 G2; 04 E25); prefix names such as `refs/heads/ma` are not protected (04 F3a). One nonzero exit aborts the whole push (04 E19, E24, E26, F1). |
| 1.7 | Apply the stdin rule per verdict | same file | `governed`, `unknown` and "no verdict" read stdin to EOF before any allow, so every record is checked (design 19.3 "stream until EOF"). A refusal may exit as soon as it sees a protected record; git tolerates the resulting EPIPE (transport.c 1327-1329, [EXTERNAL] web-01 Area I). `ordinary` and `released` exit 0 without reading the stream (T-10; D19-26). A hook that never read stdin still exited 0 with 3001 branches (G-42, QA sandbox). |
| 1.8 | Empty stdin allows | same file | Empty streams occur for up-to-date pushes (04 E12, E23b, E27a; web-01: the hook starts even with empty stdin). Matches design line 518. |
| 1.9 | Distinct diagnostics on stderr | same file | One message for `governed`, one for `unknown` (including the "no verdict" cause), one for malformed. Include the guard version line so `l2_status` can read it (Phase 4.2; `GUARD_VERSION_LINE` already exists at ow:804, 03). The header is not ownership proof by itself (design line 512). |

### Phase 2: Publisher and ownership check

| Step | Action | Files | Details |
|---|---|---|---|
| 2.1 | Add an executable no-replace publisher | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (new function, proposed name `publish_pre_push`) | Pattern proven by web-02 step 8 (`publish_exec`): `O_CREAT\|O_EXCL\|O_NOFOLLOW` temp at 0600 in the hooks dir → write → `fchmod 0755` → `fsync` → `link` to `pre-push` → `unlink` temp → `fsync` the directory. `link`/`linkat` fails with EEXIST and never replaces; readers see all or nothing ([EXTERNAL] web-02 primitives table, https://man7.org/linux/man-pages/man2/link.2.html). `fchmod` is not masked by umask (web-02 1a/1b). Do not use `rename` (replaces) or `O_TMPFILE` (ENOTSUP on overlay /tmp, kernel 6.8; web-02). `publish()` in `launch-job-identity.sh` (164-174) cannot be reused unchanged: it writes JSON at 0400, has no fsync and sits in a heredoc, so it is not importable (01 §3). |
| 2.2 | Resolve the target path with git | same | `git rev-parse --path-format=absolute --git-path hooks/pre-push` from the worktree: resolves the common dir and honours `core.hooksPath` ([EXTERNAL] web-01 D3a-e; rev-parse honours hooksPath since 2.10.0). Shared placement in the common dir is what git runs from every linked worktree (04 E30). `l2_status` already calls `rev-parse` (ow:1020, 03). Resolves G-26. |
| 2.3 | Refuse unsupported lookup | same | If `git config --get core.hooksPath` is set, or `extensions.worktreeConfig` is on and `git config --worktree --get core.hooksPath` is set, do not install: report reason `hookspath-set` (web-01 rec 4; C4: `config.worktree` overrides everything but `-c`). A relative hooksPath resolves per worktree root (04 E30d), so any set value is unsupported. Never migrate or forward (design 512). |
| 2.4 | Handle an existing `pre-push` (marker proposed; conditional on OQ-19) | same | Proposed marker: full-byte equality (a hash is the alternative, OQ-19). On EEXIST: if the file is an `O_NOFOLLOW` regular file whose full bytes equal the installed guard source, reuse it; otherwise keep it and report reason `foreign-pre-push` (01 §3 ownership check; web-02 rec "treat FileExistsError as already there, then compare"). Never shadow, wrap, stub or replay (design 512). |
| 2.5 | Verify the file git will run (content check conditional on OQ-19) | same | On the path from 2.2: full-content equality (proposed marker, OQ-19), regular file, same dev/ino as opened, owner = current user, mode not group/other-writable, `access(X_OK)` true as the pushing user, mount not `noexec` (01 §3; web-02: `find_hook` in hook.c v2.47.3 lines 13-49 uses only `access(X_OK)`; missing, non-executable, wrong-owner or noexec hooks are skipped and the push proceeds). Failure reason `not-executable` or `not-owned`. |
| 2.6 | Self-test the installed hook | same | Run the installed hook with a synthetic ordinary actor: a protected record → exit 0, empty stream → exit 0 (01 §3). Feeding records via `git hook run --to-stdin` (2.36+) is an option ([EXTERNAL] web-01 E1). Governed self-test scope is open (G-35). Failure reason `self-test-failed`. |
| 2.7 | Install the guard source globally (proposed; conditional on OQ-18 and OQ-20) | `src/superclaude/cli/install_hooks.py` | Proposal: add the new script to `_FRESHNESS_SCRIPTS` (42-94, next to identity at 90 and the guard at 93) so `_copy_scripts` (251-290) installs it to `~/.claude/hooks/`, and update the verify-sync listing comment (62-64) (03). `install_hooks()` stays user-global; it gains no per-repo git-hook code (G-20, design 565). |

### Phase 3: Registration and mirrors

| Step | Action | Files | Details |
|---|---|---|---|
| 3.1 | Decide whether the guard needs a `hooks.json` entry | `src/superclaude/hooks/hooks.json` (identity at line 130), `plugins/superclaude/hooks/hooks.json` (identity at line 100) | The pre-push body is a git hook, not a Claude Code hook; it needs no PreToolUse entry. Only the identity entry is registered for this feature today (01 line 267). The existing PreToolUse matcher at src hooks.json:116 already includes MCP `update_ref`/`create_ref` tools (03 D19-31), so MCP ref writes stay with L1. Record "no entry" explicitly so `make verify-sync` and reviewers do not expect one. |
| 3.2 | Run `make sync-dev` and `make verify-sync` | `.claude/` (generated, never staged) | Per project CLAUDE.md; stage only the `src/` and `plugins/` sides. |

### Phase 4: `cmd_launch` integration and conflict handling

| Step | Action | Files | Details |
|---|---|---|---|
| 4.1 | Call the installer before `l2_status` (proposed install point; conditional on OQ-18) | `orca_worktree.py`, `cmd_launch` (1253-1388) | Proposal (the install command and target repository are open, U28, OQ-18): insert between IR-4 `enforcement_preflight` (1287-1304) and the `l2_status` call (1311) (03 order; design 565 "next integration"). Runs on every governed launch, so an exec-bit clear or a later hooksPath is caught before each launch (G-8 recommended answer: before each launch, not only at install). |
| 4.2 | Make `l2_status` reason-bearing | `orca_worktree.py` `l2_status` (1012-1029) | Today it returns `absent` or `present-unverified` from `is_file` + `X_OK` and folds git-missing, timeout and not-a-repo into `absent` (03; G-19). Return `present-owned` only after Phase 2.4-2.5 checks pass; otherwise `absent` with one reason from: `no-hook`, `foreign-pre-push`, `hookspath-set`, `not-executable`, `not-owned`, `self-test-failed`, `git-missing`, `timeout`, `not-a-repo`. A foreign hook stops returning a silent `present-unverified` (fixes D19-16 [CODE-CONTRADICTED], G-18). |
| 4.3 | Put the reason into W-L2-ABSENT | `orca_worktree.py` REMEDY 789-792, WHY 796-799, call 1311-1312 | **Conflict case "foreign pre-push present":** keep the foreign file and all configuration unchanged; emit `W-L2-ABSENT` with reason `foreign-pre-push` and the resolved path. **Conflict case "core.hooksPath already set":** keep the config and every file unchanged; emit `W-L2-ABSENT` with reason `hookspath-set` and the configured value. No migration, no forwarding, no stub (design line 514 "preserve all existing files/configuration; report `W-L2-ABSENT` with the reason"; line 512). A separate `W-L2-CONFLICT` code is the alternative raised by G-18; the reason field covers it without a new code. |
| 4.4 | Build the launch refusal behind a switch that defaults off, in its own clearly marked commit | `orca_worktree.py` 1309-1310 | Owner decision (seed brief lines 68, 77): the refusal path must exist, be tested and ship off. When the switch is on: `if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))` (one line, 03). When it is off (default): keep the `W-L2-ABSENT` warning (design 574). The switch mechanism (constant, environment variable or file) and the turn-on criterion (after #442) are open (OQ-7). Phase 6.11 tests both switch states; Phase 7.5 documents it. |
| 4.5 | Leave release and worktree removal alone | none | The shared hook stays on release; no whole-hook deletion (design 524-526). `git worktree remove` deletes the private marker and keeps the shared hook (04 F2). Orca's removal path is untested (G-37, Phase 6.9). |

### Phase 5: L1 hardening (closes the bypasses in Section 7)

| Step | Action | Files | Details |
|---|---|---|---|
| 5.1 | Add hook-file tamper tokens | `src/superclaude/hooks/scripts/launch-level-guard.sh` line 706 | Add `*.git/hooks*`, `*hooks/pre-push*`, `*config.worktree*` (02 Gap 1, Gap 10, line 168). Covers Write/Edit/rm/mv/ln/chmod on the hook and the per-worktree config route (04 E29, E31). Closes G-12 and the L1 part of G-8. |
| 5.2 | Ungate config tokens | same, lines 525, 532 | Move the `hookspath` and `alias.` tokens out of the `LL_GIT=1` gate so `cd .git && >> config` and `/etc/gitconfig` writes are seen (02 Gap 3, line 170). Closes G-14. |
| 5.3 | Fix command-position detection | same, line 435 (W drops `_`), 556-557 | Underscore env prefixes move the command position off `git` (02 Gap 2). Closes G-13. |
| 5.4 | Extend push-bypass coverage | same, push regex 661, PROTECTED 663-665 | Add `--config-env`, `GIT_CONFIG_COUNT/KEY/VALUE`, `GIT_CONFIG_PARAMETERS`, `-c hook.pre-push.*`, `curl` to `git-receive-pack` on `github.com`, non-literal API hosts (L1-7), and the obfuscated `gh` subcommand `gh $'\x61pi'` (L1-8, PARTIAL in 02 §5) (web-01 rec 5; 02 Gap 5). Closes G-16, L1-7 and L1-8. `remote.origin.push` (G-15) stays an L1 gap but L2 sees it as field 3 (04 E20). |
| 5.5 | Correct the stale texts | same, line 80 (LL-UNKNOWN Why), line 95 (LL-TAMPER Blocked), line 56 (LL-PUSH-FORM) | Lines 80 and 95 are [CODE-CONTRADICTED]; line 56 omits `--set-upstream`, which the regex at line 661 accepts (DOC-9) (02 Stale Documentation). |
| 5.6 | Keep the self-declared limit | same, lines 710-711 | L1 is text-only and advisory (02 Summary); in-process library pushes are a stated limitation (web-01 J11). |

### Phase 6: Tests

| Step | Action | Files | Details |
|---|---|---|---|
| 6.1 | New hook tests in a pytest temp bare remote | `tests/hooks/test_launch_pre_push_guard.py` **(new)** | Bare remote + clone + linked worktree in `tmp_path`; assert remote refs before/after (design 530-534). |
| 6.2 | Record-shape cases | same | Protected refspec spellings (04 E3-E6, E11, E20, E21), `HEAD@{0 days ago}:refs/heads/main` 6-field record (web-01 G5), empty stream, malformed line, `refs/heads/Main` allowed, `refs/heads/ma` allowed, mixed push refused whole (04 F1), dry-run runs the hook (04 E13), "fetch first" record delivered (04 E23a), 3001-branch push under each stdin rule of Phase 1.7 (G-42), SHA-256 repo (web-01 rec 6). |
| 6.3 | Verdict cases | same | `governed`, `unknown`, `ordinary`, `released`, and each "no verdict" cause (no uv on PATH with the fixed PATH in place, exit 2, missing script, timeout) (01; 04 E28c). |
| 6.4 | Publisher cases | `tests/skills/test_issue_orca_worktree.py` | Fresh install 0755 and reuse on identical bytes; foreign `pre-push` kept and reason `foreign-pre-push`; `core.hooksPath` set (repo and `config.worktree`) kept and reason `hookspath-set`; mode 0644 → `not-executable` (web-02 step 8f); no temp file left (web-02 step 8). Extend `test_ir6_l2_status_follows_the_git_hook_path` (1686-1729). |
| 6.5 | Linked-worktree placement | same | Hook in common dir runs from every worktree (04 E30); relative hooksPath resolves per worktree root (04 E30d); `config.worktree` override (web-01 C4). |
| 6.6 | Replace the crashing test policy | `tests/hooks/test_launch_job_identity.py` 1175-1232 (`LocalPushFixture`) | It crashes on malformed records (03; G-41). Point it at the real guard script or make it refuse malformed input. |
| 6.7 | L1 token tests | `tests/hooks/test_launch_level_guard_with_identity.py` (the L1 test file research 01 names; any other L1 test file was not listed by the research) | One case per new token in Phase 5, plus the section-9 evasions 02 read statically (G-39). |
| 6.8 | Install script list | `tests/cli/test_install_hooks.py` (934-1003) | Assert the new script is installed with identity and guard. |
| 6.9 | Orca worktree removal | `tests/skills/test_issue_orca_worktree.py` | Shared hook survives Orca's removal path (G-37); plain `git worktree remove` is already observed (04 F2). |
| 6.10 | Pin the git version assumption | test module docstring or a skip guard | Tested on 2.47.3 only (04); version floors from web-01 F2 (pre-push 1.8.2, hooksPath 2.9.0, worktreeConfig 2.20.0, `git hook run` 2.36.0). The guard tests record `git --version` in their output. Re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks; parallel hooks 2.55.0) and when 2.98.0 ships (`hook.pre-push.enabled`) (web-01 rec 7, F1). |
| 6.11 | IR-7 switch states | `tests/skills/test_issue_orca_worktree.py` | One case per switch state with L2 absent: switch off (default) → launch proceeds with `W-L2-ABSENT`; switch on → `launch_result("failed", ...)` (Phase 4.4; seed brief line 68). |

### Phase 7: Design document updates

| Step | Action | Files | Details |
|---|---|---|---|
| 7.1 | Rewrite the malformed-record rule | `docs/designs/sc-issue-launch-level-hook.md` line 518 | Right-split into 4 fields; "extra fields refuse" is wrong (web-01 G5). |
| 7.2 | Correct the non-fast-forward statement | same, line 534 | "Fetch first" records reach pre-push (04 E23a; D19-47 [CODE-CONTRADICTED] in part; web-01 rec 8). |
| 7.3 | Extend the bypass list | same, line 520 | Add `--config-env`, `GIT_CONFIG_*` env, exec-bit clear, `config.worktree`, smart-HTTP, library pushes, future `hook.pre-push.enabled` (web-01 line-520 verdict "CONFIRMED with three precision additions"; 04 E29, E31). |
| 7.4 | Record the "no verdict" → `unknown` mapping and its human exceptions | same, lines 493, 557 | Line 493 "never restricted" conflicts with humans restricted by `unknown` (G-11); state the accepted cases or the chosen remedy. |
| 7.5 | Settle IR-7 wording | same, lines 355, 514, 574 | State that the refusal path exists, is tested, and ships switched off, so `W-L2-ABSENT` stays a warning by default (seed brief lines 68, 77); name the switch and turn-on criterion once OQ-7 is answered. |
| 7.8 | Record the tested git version and re-test triggers | same, §19 | Tested on 2.47.3; re-run the Phase 6 real-git suite before relying on any version at or above 2.54.0 (hook API rewrite, configured hooks) and when 2.98.0 ships (web-01 F1, rec 7). |
| 7.6 | Fix the identity header wording | `src/superclaude/hooks/scripts/launch-job-identity.sh` line 4 (+ plugin mirror) | "descendants" vs session membership ([CODE-CONTRADICTED] wording, 01 Gaps 9). |
| 7.7 | Note the absent 19.6 artifacts | same, lines 538-543 | They cite `.dev/brainstorms/20261106-l2-prepush-decisions/`, which does not exist ([STALE DOC], 03); wording depends on G-21. |

### Gap mapping (G-1 to G-43)

| Gap | Disposition | Where |
|---|---|---|
| G-1 | Documented externally (web-01 H/J); not confirmed at runtime: API writes, `gh api`, smart-HTTP bypass the hook | Section 7 bypass table; Phase 5.4; Phase 7.3 |
| G-2 | Documented externally (web-01 H/J); not confirmed at runtime (libraries not installed): libgit2/pygit2, dulwich, isomorphic-git do not run it; JGit and GitPython do | Section 7 bypass table; Phase 5.6 (stated limitation) |
| G-3 | Resolved by web research (web-01 F2 version table) | Phase 6.10 |
| G-4 | Resolved by web research (web-02 primitives table, step 8) | Phase 2.1 |
| G-5 | Resolved by web research (`find_hook`, hook.c 13-49) | Phase 2.5, 4.1 |
| G-6 | Recommendation A-i; final pick is a brainstorm decision | Phase 1.2; Open Questions OQ-1 |
| G-7 | Mapping proposed (no verdict = `unknown`) | Phase 1.4, 7.4; Open Questions OQ-2 (confirm) |
| G-8 | Proposed: recheck before each governed launch, plus L1 tokens | Phase 4.1, 5.1; Open Questions OQ-3 (confirm) |
| G-9 | Accepted limit unless decided otherwise | Section 7; Open Questions OQ-4 |
| G-10 | Deferred | Open Questions OQ-5 |
| G-11 | Deferred; design text change follows the decision | Phase 7.4; Open Questions OQ-6 |
| G-12 | Step | Phase 5.1, 6.7 |
| G-13 | Step | Phase 5.3, 6.7 |
| G-14 | Step | Phase 5.2, 6.7 |
| G-15 | L2 part resolved (04 E20); L1 part left as an L1 gap covered by L2 | Phase 5.4 note |
| G-16 | Step (bypass confirmed by web-01 H3) | Phase 5.4 |
| G-17 | Default DECIDED off (seed brief line 77); switch mechanism and turn-on criterion open | Phase 4.4, 6.11, 7.5; Open Questions OQ-7 |
| G-18 | Step proposed (reason field); new code `W-L2-CONFLICT` left as the alternative | Phase 4.2, 4.3; Open Questions OQ-8 |
| G-19 | Step | Phase 4.2 |
| G-20 | Step | Phase 2.7, 4.1 |
| G-21 | Deferred (ask owner) | Phase 7.7; Open Questions OQ-9 |
| G-22 | Resolved in Gate 1 | none |
| G-23 | Resolved in Gate 1 | none |
| G-24 | Order is undocumented (web-01 Key Findings) and was observed both ways: command-line order in 04 E7 and web-01 G3, not command-line order in 04 E9, E19, E24. Resolved only in the sense that the hook scans every record and does not depend on order | Phase 1.6 (check every record) |
| G-25 | Git side resolved (case-sensitive, web-01 G2); hosting-service behaviour deferred | Phase 1.6; Open Questions OQ-10 |
| G-26 | Resolved by web research (D3a-e) | Phase 2.2 |
| G-27 | Partly resolved (FETCH_FIRST delivered, transport.c 1315-1319); real SSH/HTTPS remote untested | Phase 6.2; Open Questions OQ-11 |
| G-28 | Partly resolved: field 1 can hold spaces (web-01 G5), so the parser right-splits and treats fewer than 4 fields as malformed; that git never emits a short record in any version or transport stays unproven (D19-42) | Phase 1.5, 7.1 |
| G-29 | Resolved by web research: git refuses `refs//heads/main` before the hook (web-01 G1) | none needed for L2 |
| G-30 | Resolved by web research: `--mirror` with a refspec is fatal (web-01 G4) | none needed for L2 |
| G-31 | Deferred (local read-only check not run here) | Phase 2.3 handles either value; Open Questions OQ-12 |
| G-32 | Deferred | Open Questions OQ-13 |
| G-33 | Deferred (scope) | Open Questions OQ-14 |
| G-34 | Deferred (scope) | Open Questions OQ-14 |
| G-35 | Deferred | Phase 2.6; Open Questions OQ-15 |
| G-36 | Proposed: missing script = no verdict = `unknown` | Phase 1.3; Open Questions OQ-2 |
| G-37 | Step | Phase 6.9 |
| G-38 | Deferred | Open Questions OQ-16 |
| G-39 | Step | Phase 6.7 |
| G-40 | Not relevant to GitHub remotes; no step | none |
| G-41 | Step | Phase 6.6 |
| G-42 | Step | Phase 1.7, 6.2 |
| G-43 | The git-behaviour parts of D19-21, 23, 27, 29, 35, 41 are settled by 04; the rest stay unverified design statements | Phase 6 covers the testable ones; Open Questions OQ-17 |

### Gap mapping (BP-, L1- and DOC- families, synth-02 §4.2-§4.4)

| Gap | Disposition | Where |
|---|---|---|
| BP-1 `--no-verify` | No step: L1 already refuses (02) | Section 7 bypass table ("L1 (keep)") |
| BP-2 `-c core.hooksPath` | No step: L1 already refuses (02) | Section 7 bypass table |
| BP-3 `--config-env`, `GIT_CONFIG_*` | Step | Phase 5.4, 6.7, 7.3 |
| BP-4 persistent `core.hooksPath` | Covered by G-8, G-14 | Phase 2.3, 4.1, 5.2 |
| BP-5 `extensions.worktreeConfig` | Covered by G-8 | Phase 2.3, 5.1, 6.5 |
| BP-6 executable bit cleared | Covered by G-8 | Phase 2.5, 4.1, 5.1 |
| BP-7 raw smart-HTTP | Covered by G-16 | Phase 5.4 |
| BP-8 `git send-pack` | No step: L1 already refuses (02) | Section 7 bypass table |
| BP-9 in-process library push | Covered by G-2 (stated limitation) | Phase 5.6 |
| BP-10 REST refs API / `gh api` | Covered by G-1; L1 refuses, PARTIAL forms in L1-7, L1-8 | Phase 5.4 |
| BP-11 hook file removed or replaced | Covered by G-12 | Phase 2.4-2.5, 5.1 |
| BP-12 `hook.pre-push.enabled=false` (future) | Step | Phase 5.4 (`-c hook.pre-push.*`), 6.10, 7.3, 7.8 |
| BP-13 config-defined and parallel hooks, remote groups | Version pin | Phase 6.10, 7.8 |
| BP-14 more-than-four-field record | Covered by G-28 | Phase 1.5, 6.2 |
| L1-1 config-file write of `core.hooksPath` | Covered by G-14 | Phase 5.2 |
| L1-2 `cd`, then canonical push | No L1 step: L2 refuses by field 3 | Phase 1.6 |
| L1-3 Write/Edit of the hook | Covered by G-12 | Phase 5.1 |
| L1-4 `rm`/`mv`/`chmod -x`/`ln -sf` on the hook | Covered by G-12 | Phase 5.1 |
| L1-5 underscore env prefix with alias | Covered by G-13 | Phase 5.3 |
| L1-6 `curl` to `git-receive-pack` | Covered by G-16 | Phase 5.4 |
| L1-7 hidden `api.github.com` host | Step | Phase 5.4 |
| L1-8 `gh $'\x61pi'` | Step | Phase 5.4, 6.7 |
| L1-9 `uv run python -c` with push libraries | Covered by G-2 (stated limitation) | Phase 5.6 |
| L1-10 `uv run python <script>` that pushes | Covered by G-2 (stated limitation) | Phase 5.6 |
| DOC-1 design line 534 (D19-47) | Step | Phase 7.2 |
| DOC-2 LL-UNKNOWN text line 80 | Covered by G-13 | Phase 5.5 |
| DOC-3 LL-TAMPER text line 95 | Step | Phase 5.5 |
| DOC-4 identity header line 4 | Step | Phase 7.6 |
| DOC-5 IR-7 design text | Covered by G-17 | Phase 7.5 |
| DOC-6 §19.6 artifacts | Covered by G-21 | Phase 7.7 |
| DOC-7 D19-16 conflict reporting | Covered by G-18 | Phase 4.2, 4.3 |
| DOC-8 D19-42 malformed rule | Covered by G-28, BP-14 | Phase 1.5, 7.1 |
| DOC-9 LL-PUSH-FORM text line 56 | Step | Phase 5.5 |
| DOC-10 design line 493 | Covered by G-11 | Phase 7.4 |
| DOC-11 git-hook page vs 2.98.0 note | Covered by BP-12 (external discrepancy, no repo text to change) | Phase 6.10, 7.8 |

### Integration Checklist

- [ ] Guard source exists in `src/superclaude/hooks/scripts/` and the plugin mirror, byte-identical (Phase 1.1; `make verify-sync`).
- [ ] Install command and target repository settled (OQ-18); if the proposal stands, `_FRESHNESS_SCRIPTS` lists the guard, and `tests/cli/test_install_hooks.py` asserts it installs to `~/.claude/hooks/` (Phase 2.7, 6.8).
- [ ] Identity-script location settled (OQ-20); hook calls the selector (proposed: `~/.claude/hooks/launch-job-identity.sh identify`) under a fixed PATH; "no verdict" maps to `unknown` (Phase 1.2-1.4).
- [ ] Parser right-splits to 4 fields, compares field 3 exactly, allows empty stdin; `governed`/`unknown`/no-verdict read stdin to EOF before an allow, a refusal may exit at the first protected record, `ordinary`/`released` exit 0 without reading (Phase 1.5-1.8).
- [ ] Publisher uses `O_EXCL` temp + `fchmod 0755` + `fsync` + `link` + `unlink` + directory `fsync`; never `rename` (Phase 2.1).
- [ ] Target path comes from `git rev-parse --path-format=absolute --git-path hooks/pre-push` (Phase 2.2).
- [ ] `core.hooksPath` set (repo or `config.worktree`): nothing changed, `W-L2-ABSENT` reason `hookspath-set` (Phase 2.3, 4.3).
- [ ] Foreign `pre-push`: nothing changed, `W-L2-ABSENT` reason `foreign-pre-push` (Phase 2.4, 4.3).
- [ ] Ownership marker settled (OQ-19); proposed ownership = full bytes + regular file + owner + mode + `X_OK` + not noexec + self-test (Phase 2.5-2.6).
- [ ] Installer runs in `cmd_launch` after IR-4 and before `l2_status`, on every governed launch (Phase 4.1).
- [ ] `l2_status` returns a reason; a foreign hook is no longer `present-unverified` (Phase 4.2).
- [ ] IR-7 refusal built behind a switch that defaults off, in its own clearly marked commit, tested in both states, and documented as shipping off (Phase 4.4, 6.11, 7.5; seed brief lines 68, 77).
- [ ] No `core.hooksPath` write, no `extensions.worktreeConfig`, no forwarding, no other hook touched (design 510-512).
- [ ] L1 tokens and ungating land with tests (Phase 5, 6.7).
- [ ] All git tests run in pytest temp dirs with a local bare remote only (design 530-534).
- [ ] Design text updated (Phase 7).
- [ ] Only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/` staged; never `.claude/` except `settings.json` (project CLAUDE.md).

---

## Open Questions (deferred from Sections 6-8)

| ID | Question | Gap | Why it is not decided here |
|---|---|---|---|
| OQ-1 | Identity variant: A-i fixed PATH with install-time uv dir, or A-iii pure-shell hook? | G-6 | Brainstorm decision; A-i recommended (Section 7). |
| OQ-2 | Write "no verdict" (exit 2, missing script, timeout) = `unknown` into the design? | G-7, G-36 | Not in the design today (01 Gaps 1). |
| OQ-3 | Recheck install integrity before each governed launch (proposed) or only at install? | G-8 | Brainstorm decision. |
| OQ-4 | Accept the `setsid` and different-HOME `ordinary` escapes, and list the HOME escape in the design? | G-9 | HOME escape is listed nowhere (01 Gaps 2). |
| OQ-5 | Prune stale job records, or accept PID-reuse `unknown` for humans? | G-10 | PID-reuse consequence is inferred, not observed (01 Gaps 3) [UNVERIFIED]. |
| OQ-6 | Which human cases restricted by `unknown` are accepted against design line 493? | G-11 | Owner choice. |
| OQ-7 | IR-7 switch: which mechanism (constant, environment variable or file), and what criterion turns it on (after #442)? | G-17 | The default is DECIDED off (seed brief line 77) and the refusal must exist and be tested (line 68); only the mechanism and turn-on criterion are open. |
| OQ-8 | Reason field in `W-L2-ABSENT` (proposed) or a new `W-L2-CONFLICT` code? | G-18 | Brainstorm decision. |
| OQ-9 | Were the 19.6 artifacts committed elsewhere or never? | G-21 | Ask owner; D19-10, 17, 33, 49, 52-56 stay unverifiable. |
| OQ-10 | Does the hosting service treat `Main` as `main`? | G-25 | [UNVERIFIED]; git itself is case-sensitive. |
| OQ-11 | Network transports (SSH/HTTPS) hook timing and remote advertisement | G-27 | [UNVERIFIED]; only local transports were run (04). |
| OQ-12 | Is `extensions.worktreeConfig` enabled in this repo? | G-31 | [UNVERIFIED]; Phase 2.3 handles both values. |
| OQ-13 | §19.1 actor-selection lifecycle variants beyond the single E1 data point | G-32 | [UNVERIFIED]. |
| OQ-14 | PID namespaces, containers, boot_id; non-dumpable/setuid Python and `/proc/<sid>` ownership | G-33, G-34 | [UNVERIFIED]; scope decision. |
| OQ-15 | Self-test with a governed fixture, or ordinary only? | G-35 | Brainstorm decision. |
| OQ-16 | Does `cd` persist between Bash calls in a governed session; are mid-session `~/.bashrc` edits (`GIT_CONFIG_PARAMETERS`) picked up? | G-38 | [UNVERIFIED]. |
| OQ-17 | Remaining unverified design statements (D19-1, 3, 9, 13, 14, 24, 26, 38, 40, 43-46, 50; uncheckable D19-6, 34, 51, 57, 82; partial D19-31, 65, 70, 72, 77) | G-43 | No code or tests (03) [UNVERIFIED]. |
| OQ-18 | U28: which command installs the hook (`superclaude install`, `launch`, or a dedicated subcommand), and into which repository? | none (seed brief line 75; synth-04 row 15) | Owner decision open; Phases 2.7 and 4.1 are proposals. |
| OQ-19 | Ownership/version marker: full-byte equality or a hash? | none (seed brief line 76; synth-04 row 14) | Owner decision open; Phases 2.4-2.5 propose byte equality. |
| OQ-20 | How does the hook find the identity script at run time, and what happens when it is missing? | G-36 (seed brief line 78; synth-04 row 2) | Owner decision open; Phase 1.3 proposes `~/.claude/hooks/launch-job-identity.sh` and missing = no verdict. |

---

## Source coverage

| Source | Summary / Key Takeaways / Key External Findings | Reflected in |
|---|---|---|
| 01 identity selector | Selection by kernel session, no PPID walk; verdict lines 225/241-244; owner decision on `unknown`; "no verdict" must map to `unknown`; uv-PATH problem and three remedies; `setsid`/HOME escapes; humans restricted by `unknown`; `publish()` not reusable unchanged; ownership check; three byte-identical copies and entry point | Shared sub-choice 2; Section 7; Phase 1.2-1.4, 2.1, 2.5-2.6, 7.4, 7.6; OQ-1 to OQ-6 |
| 02 L1 coverage | L1 is advisory and text-only; no `.git/hooks` token at 706; `LL_GIT` gate at 525/532; underscore command-position bypass; curl/library/config.worktree misses; stale texts at 80/95; rely on server-side protection | Section 7 bypass table; Phase 5; Options Comparison row "L1 protection of the hook file today" |
| 03 claim code | `l2_status` shape and folding; W-L2-ABSENT lines; `cmd_launch` order; one-line refusal; D19-16/D19-18 contradictions; `install_hooks.py` user-global only; natural install point; absent 19.6 artifacts; crashing test policy | Phase 2.7, 4.1-4.4, 6.4, 6.6, 7.7; OQ-7 to OQ-9 |
| 04 empirical git | Field 3 authoritative; empty stdin; fetch-first delivered; one exit aborts whole push; dry-run runs hook; env passes through; every bypass E14-E17, E29, E31; common-dir placement and worktree removal; `refs/heads/ma` reaches hook | Option A evidence; Section 7; Phase 1.5-1.8, 2.2-2.3, 6.2-6.5, 7.2 |
| web-01 [EXTERNAL] | githooks contract; field 3 by code; skipped statuses; EPIPE tolerated; 6-field record (G5) contradicting design 19.3; G1-G4; `--config-env`/`GIT_CONFIG_*`; `config.worktree` precedence; `--path-format=absolute --git-path`; `git hook run --to-stdin`; future hook config; J10 tools table; line-520 verdict; version table; recommendations 1-8 | Section 7; Phase 1.5-1.7, 2.2-2.3, 2.6, 5.4, 6.2, 6.10, 7.1-7.3 |
| web-02 [EXTERNAL] | `find_hook` uses only `access(X_OK)`; fail-open for missing, non-executable, wrong-owner or noexec hooks; primitives table; `O_TMPFILE` ENOTSUP here; `fchmod` not masked; sandbox step 8 `publish_exec`; recommendations 1-8 | Shared sub-choice 1; Phase 2.1, 2.4-2.5, 4.1, 6.4 |
| gaps-and-questions | G-1 to G-43 and the tag table | Gap mapping; Open Questions |

Nothing from the Summaries or Key Takeaways was excluded.
