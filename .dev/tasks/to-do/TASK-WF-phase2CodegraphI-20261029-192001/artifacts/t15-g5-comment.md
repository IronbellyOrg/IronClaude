**G5 report: Phase 2 PR is open and green. DO NOT MERGE yet (Coder step 2 is missing).**

PR: https://github.com/IronbellyOrg/IronClaude/pull/329 (head `cf4e0f1b`, base `master`)

**Review (`/sc:pr-submit --monitor 3`)**
- Augment found 1 medium issue: the digest test only checked the format of the four pinned checksums. I confirmed it was valid, then fixed it in `184482fe`. `test_u2_pin_integrity` now compares all four pins to the real v1.6.2 release checksums (`.dev/codegraph-migration/evidence/P2-release-SHA256SUMS.txt`). All four already matched, and a one-character change to a pin now fails the test. Thread replied to and resolved.
- Augment's re-review of `184482fe` came back clean.
- CI first failed on `ruff format --check` for `src/superclaude/cli/install_mcp.py` (my formatting miss). Fixed in `cf4e0f1b`.

**CI on `cf4e0f1b`: all 6 checks pass**, including SuperClaude Doctor Check and Test on Python 3.10 (9m12s).

**Merge gate (the three commands from the plan, run against Coder `main` just now)**
| Check | Result |
|---|---|
| 1. `Dockerfile.coder` has the pinned linux-x64 hash | PRINTS (Coder PR #420 merged) |
| 2. `test-57-catalogue-configure.sh` asserts the codegraph registration | DOES NOT PRINT |
| 3. bundle `install.sh` no longer installs Serena | DOES NOT PRINT (`SERENA_PIN=1.7.0` at line 19 and `uv tool install ... serena-agent` at line 161 are still there) |

No open Coder PR exists for step 2 (searched for "323" and "serena"). **Do not merge until all three lines print.** Coder step 2 still needs to be written and merged first.

Note: the force-with-lease push earlier in this work rewrote branch history, so commit SHAs in the earlier G0-G4 and task comments on this issue are stale. The current history is the PR's commit list.
