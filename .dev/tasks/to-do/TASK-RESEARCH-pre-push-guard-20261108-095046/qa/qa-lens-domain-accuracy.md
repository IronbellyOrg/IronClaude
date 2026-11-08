## Domain-Accuracy QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md`
**Lens:** Domain-Accuracy (phase: report-lens-domain-accuracy)
**Date:** 2026-11-08
**Fix authorization:** false (report only; the report was not modified)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | IMPORTANT | §2.5(c) (line 384); §2.6 row 3 (line 466) vs §4 G-26 (line 662), §8 (line 1184), §9 R9 (line 1331) | The report contradicts itself on whether `git rev-parse --path-format=absolute --git-path hooks/pre-push` was verified on git 2.47.3, and leaves the `[CONTRADICTION]` marker at line 384 open. Line 466 lists it as unverified, while lines 662, 1184 and 1331 mark it resolved. Fact: web-01 D3a and D3d ran it locally on 2.47.3; only research/04 did not (04 lines 1655, 2251). This QA re-ran it in a `/tmp` sandbox on 2.47.3: it returns `<common-dir>/hooks/pre-push` from both the main checkout and a linked worktree, and `<worktree-root>/myhooks/pre-push` when `core.hooksPath=myhooks`. | Close the marker at line 384. State that the flag was verified locally on 2.47.3 by web-01 D3 (not by 04), and change §2.6 row 3 to resolved, citing web-01 D3, so it agrees with lines 662, 1184 and 1331. |
| 2 | IMPORTANT | §8.6 Phase 6.7 (line 1140) vs §9 rows 7, 8, 29 | The `[CONTRADICTION]` about which L1 test file to extend is left open. Phase 6.7 names `tests/hooks/test_launch_level_guard_with_identity.py`; rows 7, 8 and 29 name `tests/hooks/test_launch_level_guard.py`. Both files exist, so an implementer gets two different targets for the same work. | Pick one file (or split the work explicitly, for example token tests in `test_launch_level_guard.py` and identity-bound cases in `..._with_identity.py`), use it in Phase 6.7 and rows 7, 8 and 29, and remove the marker. |
| 3 | MINOR | §9 row 27 (line 1304) vs §2.2 (line 191) | Row 27 describes design §19.1 actor selection as "by process ancestry (B-CTX)". §2.2 says, correctly per `launch-job-identity.sh` (lines 263, 332, 338), that the selector matches the kernel session id (field 6 of `/proc/<pid>/stat`) with no ancestry walk. A reader could take row 27 as describing current behaviour. Graded minor because row 27 paraphrases the design, not the code. | Reword row 27: "the design's B-CTX wording describes ancestry; the shipped selector matches the kernel session id (§2.2)". |
| 4 | MINOR | §2.4 (line 298); §4 G-20 (line 656) | `install_hooks.py` is cited as "612 lines"; the file has 611. The claim it supports (no git-hook installer, no `subprocess`) is true. | Change "612" to "611" in both places. |
| 5 | MINOR | §2.2 (line 191) | Says `launch-job-identity.sh` "publishes jobs/<sid>.json (line 301)". Line 301 builds the name; the `publish(jobs, name, record)` call is at line 305. `os.setsid()` at line 292 is correct. | Cite lines 301-305, or line 305 for the publish. |
| 6 | MINOR | §9 row 1; §9.4 | Cites "04 line 1530 (an absolute uv path)" as the superseded claim, but 04 line 1530 now contains the Gate-1 correction (an absolute uv path is not enough). The citation points at the corrected text as if it were the error. | Say "the pre-Gate-1 text of 04 line 1530", or cite the corrected sentence as the source of the correction. |
| 7 | MINOR | §9 (line 1316) | Says the home filesystem is "ext4". `stat -f /home/coder` reports `ext2/ext3`, which cannot tell the ext versions apart. No cited evidence shows ext4. | Say "an ext-family filesystem (`stat -f` reports ext2/ext3)", or cite `findmnt` or `/proc/mounts` evidence for ext4. |

**Checklist coverage (Domain-Accuracy lens)**

- **(a) Architecture vs code.**
  - `launch-level-guard.sh` (747 lines) matches at every cited line: 56, 59, 80, 95, 257-273, 394, 417, 428-437, 486-534, 549, 556-557, 637-669, 706, 710-711 and 722-741.
  - `launch-job-identity.sh` (566 lines) matches, except finding 5: 4, 20-26, 52-53, 263, 292, 332, 338, 536, 564 and 566. A draft finding about the exit-2 "except no-arg/hook mode" row (line 166) was withdrawn: lines 25-30 show that no-arg mode falls back to `jq` or `exit 0` when `uv` is missing, so the report is correct.
  - `orca_worktree.py` matches: `l2_status` at 1012-1029 with `--git-path` at 1020, plus 1287-1334, 1376 and 789-804.
  - `install_hooks.py` matches, except finding 4: 42-94, 251-290 and `chmod 0o755` at 284-285.
- **(b) Capabilities.**
  - No L2 hook and no git-hook installer exist today. A grep of `src/` for `hooksPath`, `worktreeConfig` and `pre-push` hits only the `l2_status` and W-L2-ABSENT text and comments in `pr_submit/fsm.py`. `.git/hooks/pre-push` is absent.
  - The report labels the L2 hook and installer as proposed, never as current. This check passed.
- **(c) Versions.**
  - `git --version` gives 2.47.3, and `uname -r` gives 6.8.0-147-generic.
  - The `rev-parse --git-path` behaviour honours `core.hooksPath` from 2.10.0, which matches the RelNotes cited in web-01 (line 122).
  - The one version-related error is the D3 status, finding 1.
- **(d) Integration points**, checked against research/04 and a sandbox re-run:
  - **Arguments:** argv is the remote name and URL, observed as `origin | /tmp/.../remote.git`.
  - **Hook location:** a linked worktree resolves the hook in the common dir, and a relative `core.hooksPath` resolves per worktree root. Both were observed and match report lines 279, 324 and 381.
  - **Exit status:** a nonzero exit aborts the push (observed rc=1), and `--no-verify` bypasses the hook (observed).
  - **Exec bit:** with the exec bit cleared, the hook is skipped with an `ignoredHook` hint and the push succeeds. This was observed and matches line 369.
  - **Stdin:** the format follows 04 E-series. The 6-field record comes from web-01 G5. The sandbox dry-run sent no record because the ref was already up to date, so this QA did not re-observe the record format.
  - **Push → hook → identify flow:** this matches 04 lines 204-220 and 1531.

**Self-Audit**

- **(a) Reliance:** none. No Inherited Structural Verdict was supplied, so every cited line was opened directly.
- **(b) Independent checks:**
  - Read all four code files at every cited line.
  - Read research/04 and web-01 at the cited lines.
  - Ran a `/tmp` sandbox with a local bare remote, as described under (d). The directory was removed afterwards (`CLEANED=yes`), and nothing was pushed to a real remote.
- **Tool engagement:** Tavily and web tools were not used, because no external lookup was needed.

### Summary

- Total findings: 7
- Critical: 0
- Important: 2
- Minor: 5

Verdict: FAIL
