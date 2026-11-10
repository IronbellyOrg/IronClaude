# Research Completeness Verification

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Analysis type:** completeness-verification (single instance, no partition)
**Files analyzed:** 5 (research-notes.md plus 4 research files: 01, 02, 03, 04)
**Depth tier:** Standard
**Fix authorization:** false (report only; no research file was modified)
**Method:** every file read in full (file 04, 2262 lines, read in pages 1-2262). Counts below come from Grep counts over the research files (citation-pattern lines, tag occurrences, command blocks) plus manual reading; they are approximate where marked "approx.".

---

## Verdict: FAIL (0 Critical, 2 Important, 14 Minor)

The research is strong overall. Every key file and sub-questions a-d are covered, the file 04 sandbox safety record is complete, and no cross-file contradiction was found. The gate still fails on two Important gaps:

1. **I-1:** `04-empirical-git-prepush-experiments.md` has no Key Takeaways section. Checklist item 4 requires one, and it is the only research file without it.
2. **I-2:** The "push via other tools" part of sub-question (b) is not answered. Whether pygit2/libgit2, dulwich, GitPython or JGit run the client-side pre-push hook was left [UNVERIFIED] by file 02 (Gap 6, line 264; line 190 says it "belongs to the L2 hook-semantics research"). File 04 did not test it: its "other tools" coverage is `git send-pack` only (E17). Nobody routed it to Phase 4 either. File 04's only web-01 route is D19-30's hosting-API part (line 2250), and the web-01 source list in research-notes.md (line 73) contains only git-scm documentation, which does not cover these libraries.

Both gaps can be fixed cheaply (see Recommendations). The Minor items are notes and do not block synthesis.

## Safety Record Check (file 04)

| Requirement | Main sandbox | Follow-up sandbox | Status |
|---|---|---|---|
| `mktemp -d` directory under /tmp | line 11: `SANDBOX=$(mktemp -d /tmp/prepush-research.XXXXXXXX)` printed `/tmp/prepush-research.ERbSguv9` | line 1801: `mktemp -d /tmp/prepush-followup.XXXXXXXX` printed `/tmp/prepush-followup.0OZWoyIi` | OK |
| `git remote -v` shows only local paths | lines 47-49: `origin /tmp/prepush-research.ERbSguv9/remote.git` (fetch/push). E22 SHA-256 clone: lines 1168-1169, local `remote256.git` only | lines 1872-1874: `origin /tmp/prepush-followup.0OZWoyIi/remote.git` (fetch/push) | OK |
| Sandbox removed, with verbatim evidence | "Sandbox removal" lines 1701-1712: `rm exit=0`, `ls: cannot access ... No such file or directory`, `ls exit=2` | "Follow-up sandbox removal" lines 2217-2229: `rm rc=0`, `ls rc=2` | OK |
| Isolation of git config | line 11: `export HOME=$S/home GIT_CONFIG_NOSYSTEM=1` on every call; line 13 discloses the ambient `GIT_CONFIG_COUNT` credential variables | line 1801 (same exports); `ls -a $S/home` is empty (lines 1886-1888) | OK |
| Logging hook and runner recorded | hook script at line 83, runner `x.sh` at line 127 | hook heredoc at line 1808, runner at line 1826 | OK |

No safety finding against file 04. Files 01 and 03 also ran /tmp experiments. Their safety is only self-attested in prose (see Minor m-1).

## Coverage Audit

| Scope Item (research-notes.md EXISTING_FILES / sub-questions) | Covered By | Status |
|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines) | 02 (sections 1-9; the §8 coverage table gives file:line for 35 candidates) | COVERED |
| `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines) | 01 (identify/proc/members/supervise/publish with line numbers, plus the real-git experiment in §7) | COVERED |
| `docs/designs/sc-issue-launch-level-hook.md` §19 (lines 489-578) | 03 (83 claims D19-1..83, all tagged); 04 Step 2.5 re-checks 16 git claims (lines 1773-1797); 01 checks §19.7 (line 296) | COVERED |
| `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (l2_status 1012-1029, REMEDY 789, L2_ABSENT_WHY 796, call 1311) | 03 §2-§3 (lines 70-112); 01 lines 236 and 244 | COVERED |
| `src/superclaude/cli/install_hooks.py` | 03 (confirms there is no git-hook install path) | COVERED |
| (a) stdin record format, argv, empty stdin, create/update/delete/force/HEAD:main/multi/--mirror/--all/--tags | 04 E1-E13, E19-E27, E22 (SHA-256), F1, F3; Results table lines 1718-1771 | COVERED |
| (b) paths that skip pre-push: --no-verify, core.hooksPath=/dev/null or other dir, send-pack, other tools | 04 E14-E17, E29, E31; 02 §8 (L1 view); **other tools (libraries) not covered** | PARTIAL: see I-2 |
| (c) hook lookup in linked worktrees: common dir, --git-path, core.hooksPath, extensions.worktreeConfig | 04 E1, E18, E30a-d, E31a-b, F2 | COVERED (`--path-format=absolute` not exercised, m-9) |
| (d) process ancestry and environment from a linked worktree | 04 E1, E18, E28a-c; 01 §3 (lines 120-136) and §7 (lines 138-173) | COVERED |
| (e) atomic no-replace publication; executable bit | Codebase part: 01 `publish()` analysis (lines 236-258) and 04 E29 (a non-executable hook fails open and the hint can be suppressed). Linux link(2)/O_EXCL/renameat2 semantics are deferred to web-02 | PARTIAL by design (Phase 4) |
| (f) version history; installed git version | git 2.47.3 measured (research-notes line 16; 04 line 41 and line 1866). Version history is deferred to web-01 | PARTIAL by design (Phase 4) |

Every key file is covered. Sub-questions (a), (c) and (d) are fully covered. (b) is covered except for library and tool pushes (I-2). (e) and (f) are Phase 4 topics. The codebase contributes the `publish()` pattern and its limits (mode 0400 is not executable, no fsync, not importable; 01 lines 236-240), the fail-open E29 result and the measured git version.

## Evidence Quality

"Citation lines" counts the Grep hits for line-number citation patterns (`line N`, `.sh:N`, `:NNN`, `ow:N`, `jid:N`). "Unsupported" counts claims I found during reading that have no code citation and no verbatim output (approx.).

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|---|---|---|---|
| 01-identity-selector-ancestry.md | approx. 115 citation lines; every code claim names a function and line (for example `identify` at 215, `proc()` at 202-207, `setsid` at 292, `publish()` at 164-174) | approx. 12. The §7 experiment rows (lines 146-155) and the direct-call results (line 157) are given as tables with no verbatim command or output. The stale-record PID-reuse consequence (line 165) is declared as inferred. The git `access(X_OK)` behaviour (line 236) has no tag, though 04 E29 confirms it | Adequate |
| 02-l1-guard-push-bypass-coverage.md | approx. 131 citation lines; each §8 row gives the deciding regex and file:line | approx. 3. The §9 evasions are static and not executed (declared, line 244 and Gap 13). `remote.origin.push` mapping (line 250, Gap 4) rests on git-push docs, not code (E20 later confirms it). Section 7 library verdicts are partial | Strong |
| 03-design-and-claim-code-crossvalidation.md | approx. 95 citation lines; all 83 claims carry a tag plus a code path (`ow:`, `jid:`, test file:line) | approx. 2. The /tmp `l2_status` observations have no verbatim command or output | Strong |
| 04-empirical-git-prepush-experiments.md | 31 experiments (E0-E31) plus F0-F4, each with a verbatim `Command block` and `Output` (103 command/output markers by Grep); remote refs before and after recorded per run; Results table with 52 rows | approx. 2, both tagged [UNVERIFIED]: the stdin order rule (E24, line 1339) and case folding (E25, line 1370). Ref listings are abridged and declared (E15-E17, E20, E21, E23-E29, for example lines 1079, 1247, 1307) | Strong |

Checklist requirement for file 04 ("every empirical claim cites the exact command and its verbatim output"): **met.** Every E and F section that states an observed result has its command block and output block. Abridgement covers only unchanged ref listings and is declared each time, and the runner's `REMOTE-REFS-CHANGED` line plus the diff are kept verbatim. The E28 `GIT_*` blocks for E28b/E28c are summarised as "identical to E28a, 13 lines" (lines 1507, 1519). This is declared, so it is Minor.

## Documentation Staleness

| Claim | Source Doc | Verification Tag | Status |
|---|---|---|---|
| D19-1..83 (all §19 claims) | design lines 489-578 | 83/83 tagged in 03 (89 tag occurrences) | OK |
| D19-16 foreign hook reports `W-L2-ABSENT` with a reason | design line 514 | [CODE-CONTRADICTED] (03 line 167) | OK. Reported as a gap and question (03 line 294), not as current fact. 01 line 252 repeats design 514 as a future installer requirement without noting the contradiction (m-12) |
| D19-18 / IR-7 governed launch refused when L2 absent | design lines 355, 514 | [CODE-CONTRADICTED] + [STALE DOC] (03 lines 169, 317) | OK. Nowhere reported as current fact |
| D19-47 up-to-date/non-ff refs never reach pre-push | design line 534 | 03: UNVERIFIED-GIT; 04: [CODE-CONTRADICTED] in part (table line 1791, Gaps line 2247) but "None contradicted ... incomplete, not stale" in Stale Doc (lines 2254-2255) | FLAG (Minor m-4): inconsistent label inside 04 |
| 14 UNVERIFIED-GIT claims in 03 (D19-2, 20, 21, 22, 23, 25, 28, 30, 33, 35, 41, 42, 47, 48) plus the git parts of D19-27 and D19-29 | design lines 493-534 | all resolved by 04 Step 2.5 (lines 1779-1797): 15 rows confirmed, 1 contradicted in part, 1 routed (D19-30 API part) | OK; 03's table is now superseded (m-11) |
| LL-UNKNOWN Why text | launch-level-guard.sh line 80 | [STALE DOC]/[CODE-CONTRADICTED] (02 line 276) | OK |
| LL-TAMPER Blocked text | launch-level-guard.sh line 95 | [CODE-CONTRADICTED] partial (02 line 277) | OK |
| LL-PUSH-FORM Why text | launch-level-guard.sh line 56 | [CODE-VERIFIED] with addition (02 line 278) | OK |
| identity script header "ordinary non-zombie descendants" | launch-job-identity.sh line 4 | [CODE-CONTRADICTED] wording only (01 line 291) | OK |
| design §19.7 selector claims | design lines 549-561 | checked, no stale doc (01 line 296) | OK |
| git-push docs: `remote.<remote>.mirror` makes `--mirror` default | external git-push doc (02 Gap 11, line 269) | [UNVERIFIED] | OK (tagged); not tested, not routed (m-7) |
| git-push docs: `remote.origin.push` maps a source to `refs/heads/main` | external git-push doc (02 line 250, Gap 4) | untagged in 02 | Minor: confirmed independently by 04 E20 (line 1104) |
| git runs a hook only if `access(X_OK)`; `advice.ignoredHook` hint | git source/doc knowledge (01 line 236) | untagged in 01 | Minor (m-13): confirmed independently by 04 E29 (lines 1551-1582) |
| 04 tags empirical git observations as [CODE-VERIFIED] | n/a (observations, not code) | [CODE-VERIFIED] used for runtime results | Minor terminology (m-2) |

No [CODE-CONTRADICTED] claim is reported as current fact anywhere, so there is no CRITICAL staleness flag.

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-identity-selector-ancestry.md | Complete (line 4) | Y (line 300) | Y (line 281, 10 items) | Y (8 per-section blocks, for example lines 48, 86, 131, 169, 196, 254, 276) | Complete |
| 02-l1-guard-push-bypass-coverage.md | Complete (line 4) | Y (line 282) | Y (line 257, 14 items) | Y (per-section, for example lines 31, 55, 172, 192, 238, 253) | Complete |
| 03-design-and-claim-code-crossvalidation.md | Complete (line 5) | Y (line 323) | Y (line 273) | Y (lines 24, 72, 110, 132, 266) | Complete |
| 04-empirical-git-prepush-experiments.md | Complete (line 5) | Y (line 2257) | Y (line 2233) | **N**: no "Key Takeaways" heading or block anywhere (Grep finds 0). Per-experiment "Observed:" lines and the Summary partly stand in for it | **Incomplete (I-1)** |

## Cross-References

| Pair | What each file says | Consistent? | Explicit link? |
|---|---|---|---|
| 01 setsid / session selection vs 04 ancestry | 01: `identify` picks the job by kernel session; a `setsid` child or a different HOME is ordinary; no uv on PATH gives exit 2. 04 E1/E18/E28: the hook runs as a child of `git push` in the caller's session, with the caller's environment passed unchanged; uv is missing from PATH when the caller's PATH lacks `/usr/local/bin` | Yes. 04's observed parentage and environment match the inputs 01's selector relies on, and 04's PATH observation matches 01's exit-2 case | No. Neither file cites the other (m-6) |
| 02 L1 bypass verdicts vs 04 bypass experiments | 02 §8: `--no-verify`, `-c core.hooksPath=...`, `send-pack` forms are caught or missed by named regexes. 04 E14-E17, E29, E31: the same forms really skip pre-push at the git level, plus the non-executable hook (E29) and per-worktree hooksPath (E31), which no L1 regex covers | Yes. 04 confirms that each form 02 lists is a real L2 bypass. E29 and E31 add bypasses that 02 does not list as L1 gaps, which the synthesis must carry | No (m-6) |
| 03 design claims vs 04 observations | 03 tags 14 git claims plus parts of D19-27/29 UNVERIFIED-GIT. 04 Step 2.5 (lines 1773-1797) re-checks each one against its experiments | Yes, apart from D19-47 (contradicted in part by E23a), which 04 labels inconsistently (m-4) | Yes. 04 Step 2.5 names each D19 id |

## Contradictions Found

- **Across files: none.** Where two files describe the same behaviour (non-executable hook skipped: 01 line 236 and 04 E29; `remote.origin.push` mapping: 02 line 250 and 04 E20; design D19-16/D19-18: 03 and 01), they agree on the facts.
- **Inside 04 (Minor, m-4):** the Step 2.5 table (line 1791), the Gaps list (line 2247) and the Summary tag D19-47 as contradicted in part ("fetch first" non-fast-forward still reaches the hook, E23a). The Stale Doc section (lines 2254-2255) says "None contradicted ... incomplete, not stale". A reader of the Stale Doc section alone would miss the contradiction.
- **Inside 04 (Minor, m-5):** Gaps lines 2241-2242 still list `refs/heads/ma` look-alikes and worktree removal as UNVERIFIED, though F3 and F2 resolved them; line 2248 acknowledges this, but the stale bullets were not struck.
- **Between design and code (already reported by 03):** D19-16 and D19-18 are CODE-CONTRADICTED. 01 line 252 restates design line 514 as a requirement without that context (m-12). This is a framing risk, not a contradiction of facts.

## Compiled Gaps

### Critical Gaps (block synthesis)

- None.

### Important Gaps (affect quality)

- **I-1:** 04 has no Key Takeaways section (checklist item 4). Source: 04. The synthesis would have to derive takeaways from 52 result rows and the Summary itself.
- **I-2:** Sub-question (b) "push via other tools" is open. Whether pygit2/libgit2, dulwich, GitPython (shells out to git) or JGit run pre-push is [UNVERIFIED] in 02 (Gap 6, line 264; line 190), untested in 04 (only `send-pack`, E17), and not routed to Phase 4 (the web-01 source list, research-notes line 73, holds only git-scm docs). Source: 02, 04, research-notes.

### Minor Gaps (notes; do not block synthesis)

- **m-1:** 01 §7 and the 03 /tmp `l2_status` observations have no verbatim command, output or `git remote -v` record; their safety is self-attested. Source: 01, 03.
- **m-2:** 04 tags runtime git observations [CODE-VERIFIED]; an empirical tag would be more accurate. Source: 04.
- **m-3:** Ref listings in E15-E17, E20, E21, E23-E29 and the E28b/E28c `GIT_*` blocks are abridged (declared). Source: 04.
- **m-4:** D19-47 label inconsistent inside 04 (see Contradictions). Source: 04.
- **m-5:** Stale UNVERIFIED gap bullets at 04 lines 2241-2242. Source: 04.
- **m-6:** No explicit cross-references between 01 and 04 or between 02 and 04 (content consistent). Source: 01, 02, 04.
- **m-7:** `remote.<name>.mirror` making `--mirror` the default (02 Gap 11) is untested and unrouted; it is testable in a local sandbox. Source: 02.
- **m-8:** `refs//heads/main` (02 Gap 9) is testable locally but untested. Source: 02.
- **m-9:** `git rev-parse --git-path hooks --path-format=absolute` not exercised (relative output was). Source: 04.
- **m-10:** Network transports (ssh/https), case-folding filesystems and the stdin record order rule are UNVERIFIED (E24, E25). Source: 04.
- **m-11:** 03's UNVERIFIED-GIT rows are superseded by 04 Step 2.5; the synthesis must use 04's results, not 03's tags. Source: 03, 04.
- **m-12:** 01 line 252 cites design line 514 (`W-L2-ABSENT` with reason) without noting 03's D19-16 CODE-CONTRADICTED. Source: 01.
- **m-13:** External git claims are untagged in 01 (line 236, `access(X_OK)`) and 02 (line 250, `remote.origin.push`); both are confirmed by 04 (E29, E20). Source: 01, 02.
- **m-14:** (e) Linux publication semantics and (f) version history depend on Phase 4 (web-02, web-01); 01's stale-record PID-reuse consequence (line 165) is inferred, not reproduced. Source: 01, research-notes.

## Depth Assessment

**Expected depth:** Standard (file-level understanding with key function documentation).
**Actual depth achieved:** Exceeds Standard. 01 and 02 document each relevant function and regex with line numbers; 03 checks all 83 design claims against code; 04 runs 31 experiments plus 4 follow-ups with verbatim evidence, including SHA-256, `--atomic`, `--dry-run`, worktree-config and fail-open cases.
**Missing depth elements:** the library/tool pre-push question (I-2) and a synthesised takeaway block for 04 (I-1). Nothing else expected at Standard is missing.

## Recommendations

1. **Fix I-1:** add a Key Takeaways section to 04 (5-10 bullets: field 3 is authoritative; empty stdin cases; one nonzero exit aborts the whole push; `--dry-run` runs the hook; the bypass set including E29 fail-open and E31 per-worktree hooksPath; common-dir hook placement; environment passthrough and the uv PATH gap).
2. **Fix I-2:** either add pygit2/libgit2, dulwich, GitPython and JGit pre-push behaviour to the web-01 (or web-02) brief with their own documentation sources, or test locally in a `mktemp -d` sandbox if those packages are already available offline (`uv run python ...` only; no installs from the network unless authorised). Record the result as a (b) row in 04 or a new file.
3. Reconcile the D19-47 label in 04's Stale Doc section with line 1791 and line 2247 (m-4), and strike or update the resolved bullets at lines 2241-2242 (m-5).
4. Add one-line cross-references from 01 §3/§7 to 04 E1/E18/E28 and from 02 §8 to 04 E14-E17/E29/E31 (m-6).
5. Optional, cheap in the existing sandbox pattern: test `remote.<name>.mirror` (m-7), `refs//heads/main` (m-8) and `--path-format=absolute` (m-9).
6. Tell the synthesis agent to take git facts from 04 Step 2.5, not from 03's UNVERIFIED-GIT tags (m-11), and to state D19-16/D19-18 as contradicted wherever 01 line 252 is used (m-12).

## Findings

| # | Severity | File | Finding | Remediation |
|---|---|---|---|---|
| I-1 | Important | 04 | No Key Takeaways section | Add a Key Takeaways block summarising the 52 results |
| I-2 | Important | 02, 04, research-notes | Library/tool pushes (pygit2/libgit2, dulwich, GitPython, JGit) and pre-push: untested and unrouted | Route to web-01/web-02 with library doc sources, or test locally offline in a `mktemp -d` sandbox |
| m-1 | Minor | 01, 03 | /tmp experiments lack verbatim command/output and `git remote -v` record | Add command and output blocks, or mark the results as unrecorded |
| m-2 | Minor | 04 | [CODE-VERIFIED] used for runtime observations | Use an empirical tag or define the usage in the header |
| m-3 | Minor | 04 | Ref listings and E28b/E28c env blocks abridged (declared) | None required; keep the declarations |
| m-4 | Minor | 04 | D19-47 "None contradicted" in Stale Doc vs contradicted in part elsewhere | Align the Stale Doc section with line 1791 |
| m-5 | Minor | 04 | Gap bullets at 2241-2242 already resolved by F2/F3 | Strike or update them |
| m-6 | Minor | 01, 02, 04 | No explicit cross-links for the 01↔04 and 02↔04 pairs | Add one-line references |
| m-7 | Minor | 02 | `remote.<name>.mirror` default untested, unrouted | Test in the sandbox |
| m-8 | Minor | 02 | `refs//heads/main` untested | Test in the sandbox |
| m-9 | Minor | 04 | `--path-format=absolute` not exercised | Test in the sandbox |
| m-10 | Minor | 04 | Network transports, case folding, record order UNVERIFIED | Carry as open questions in the synthesis |
| m-11 | Minor | 03, 04 | 03's UNVERIFIED-GIT tags superseded by 04 Step 2.5 | Synthesis uses 04's verdicts |
| m-12 | Minor | 01 | Line 252 cites design 514 without D19-16 context | Note the CODE-CONTRADICTED status at that line |
| m-13 | Minor | 01, 02 | Untagged external git claims (01 line 236, 02 line 250) | Tag them, citing 04 E29/E20 |
| m-14 | Minor | 01, research-notes | (e)/(f) depend on Phase 4; PID-reuse consequence inferred | Confirm web-01/web-02 cover them; mark the PID-reuse point inferred in the synthesis |
