# Summary: #765 Stop Claude Code from killing the coordinator's message watch under low memory

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/765
- Type: feature
- Complexity: medium (rubric: `refs/claim.md`)
- Effort estimate: 8 hours
- spec-route: design — Medium with explicit acceptance criteria: the new coordinator process starts with the switch set, launch tests cover the chosen scope, and live proof verifies the environment and message delivery.

## What the issue asks for

The owner's [final scope decision](https://github.com/IronbellyOrg/IronClaude/issues/765#issuecomment-7169970492) makes this Part 1 only: start every coordinator's Claude process with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in its initial environment, so Claude Code's low-memory background-command cleanup cannot kill its message watch. Change the ccsession launcher, record whether protection covers coordinators only or all ccsession launches, document the session-wide effect and the need to launch a new process, and verify fresh and resumed launches. Part 2 is dropped entirely, including research, guard, sampler, browser stops and the eight plan problems; none belongs in this plan or estimate. Use `origin/integration`, not the old body's `master`; the exact switch is absent throughout `src/` at `a6fec24480e8cc65abbb16b194625e2ea52238c7`.

Recommend all ccsession launches because there is no verified coordinator-role signal in the launcher; human/agent name origin is not that signal. The plan must record its decision and ensure a conflicting inherited or env-file value cannot leave a protected coordinator without `=1`; do not treat earlier suggestions to respect overrides as owner approval to weaken the final requirement. Direct `ic` and bare Claude launches bypass ccsession, so verify the actual coordinator launch route rather than claiming universal coverage.

Estimate breakdown: 2 hours to trace the real route and record scope/override policy, 1 hour for the shared export and README, 2 hours for branch/configuration regression tests, 1 hour for checks and synchronization, and 2 hours for live launch/message evidence and recording limitations. This is one launch subsystem, over 4 and at most 16 hours: medium. The earlier 32-hour complex estimate included the now-dropped research and no longer applies; live access availability is Not known yet.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/ccsession-tag/ccsession:1080-1086,2365-2369,2412-2451,2498-2519` | User env is sourced first, then tier/profile setup; the shared pre-exec location after 2438 and before 2440 reaches all six Claude exec sites. Cover untagged/raw-resume, labeled resume and new-label launches, both with and without an explicit model. |
| `src/superclaude/skills/ccsession-tag/ccsession:2423-2438` | `CCSESSION_ORIGIN` tracks who chose a name, not coordinator role. No coordinator-only predicate was found; do not infer roles from labels. |
| `src/superclaude/skills/ccsession-tag/ccsession-orca:2-17,258-263` | Configured Orca Claude launches reach ccsession through either named or untagged wrapper exec. Verify the coordinator's actual configuration during live proof. |
| `src/superclaude/skills/ccsession-tag/README.md:404-423` | Documents Orca command configuration and coordinator launches. Add scope, session-wide effect, override behavior, bypasses and treatment of existing sessions. |
| `tests/unit/test_ccsession_tag.py:100-145,191-228,1450-1462` | Existing fake-Claude harnesses and fresh/resumed label tests can capture only the named non-secret switch. Add coverage for unset/conflicting shell and env-file values, new/resumed and tagged/untagged launches, and the chosen scope. |
| `tests/unit/test_ccsession_tiers.py:389-445` | Tier fake-Claude launch environment. Extend targeted capture to prove tier/model/profile selection does not remove protection. Keep tests isolated from developer environment values. |
| `tests/unit/test_install_ccsession.py:28-62` | Installed launcher/wrapper symlink regression surface. Run alongside the two launch-test files; installer changes are not required by the recommended launch-only approach. |
| `src/superclaude/cli/user_settings_defaults.json:10-14` | No existing protection switch. Settings timing is unproven and is not the requested launch-environment solution; no settings change is planned. |
| `src/superclaude/scripts/ic:128-130` | Direct Claude exec bypasses ccsession. Document this boundary; do not expand this issue into unrelated launcher work without a scope decision. |
| `src/superclaude/core/WORKER-CONTRACT.md:100-104` | Coordinator wait lists nine event types and a 300000 ms timeout without `--json`. Preserve the contract; the fix is launch-time environment, not automatic watch restart. |
| Live coordinator Claude PID and Orca inbox | Check only the exact switch in `/proc/<pid>/environ`, never the full environment; verify receipt and watch renewal across at least two five-minute cycles. Do not force memory pressure on the shared host. This check has not run these experiments or re-proved the installed Claude runtime gate. |
| `make sync-dev`, `make verify-sync`, pytest and Ruff | Implement in `src/`, not generated `.claude/` mirrors. Run the three targeted test files, the required broader regression/lint/format gates and sync checks; no passing result is claimed by this read-only review. |
| PR #824 and PR #833 | #824 corrects base-branch assumptions to integration. #833 updates stage-specific claim routing at integration's `src/superclaude/skills/sc-issue-protocol/refs/claim.md:79-80`; it does not implement launch protection. |

## Analysis

- [Part 1 code analysis](analysis/analyze-ccsession.md): no-depth `/sc:analyze` procedure applied to the integration launcher, wrapper, README and launch tests. Includes severity-rated gaps, launch-branch coverage, scope recommendation, validation steps and evidence limits.
- [Accuracy check](accuracy-check.md): current source citations, superseded claims and relevance checks for every scouted pull request. These local evidence files open on GitHub only after someone commits and pushes them; this worker did neither.
