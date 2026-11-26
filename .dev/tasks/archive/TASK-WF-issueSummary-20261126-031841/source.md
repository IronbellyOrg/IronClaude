# Summary: #610 Jev preflight step 1: add missing performance phrases to the troubleshoot keyword table (sub-issue of #609)

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/610
- Type: feature
- Complexity: simple (rubric: `refs/claim.md`; one troubleshooting-classification area, no new subsystem)
- Effort estimate: 2 hours
- spec-route: design — Simple issue with explicit acceptance criteria for all three phrases, the leak decision, an observed sample run and synchronization verification.

## What the issue asks for

Extend the troubleshooting protocol's performance keyword row with “too long to load”, “takes forever” and “hangs”, so everyday wording such as “ccsession is taking too long to load” selects the performance type without an explicit flag. Decide and document why “leak” remains listed under both performance and security, or how it should be handled, without silently sending security-sensitive leak reports only to performance. Record an observed manual run for the exact sample, follow the source-to-development-copy synchronization process, and extend a test only if existing tests already cover this table; otherwise record the manual verification. This is step 1 of #609, supplies the improved baseline required by #611, and does not include a Jev call, comparison, preflight component or gateway change.

The accuracy verdict is **current** at `3cf7e22597a0aa8e35860a5860542dcc1bd82c82`: the requested phrases remain absent. The 2-hour estimate covers the local row amendment and written leak rationale, checking existing coverage, observing the exact sample and representative leak wording, synchronization and recording evidence; it fits the rubric's limit of four hours in one area. It assumes retaining the existing ambiguity rule or making only a narrowly bounded clarification, not redesigning security classification or implementing the parent feature.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | Canonical change target. Wave 0 at lines 145-183 contains the keyword rows at 152-159: performance is unchanged, and leak appears under both performance and security. Ambiguity already leaves the type unset. |
| Wave 0 completion output and audit header in the same skill | Provides observable type evidence: the completion line reports `type=<type>` and the target header records the type. Source-text inspection is not the required observed manual result. |
| Wave 3 specialist selection in the same skill | Performance type influences specialist lenses only if escalation reaches Tier 2; the phrase fix does not force agents to run. |
| `src/superclaude/commands/troubleshoot.md` | Existing command entry point and `--type` interface; inspect for consistency, but no command-file change is currently required by the issue. |
| `~/.claude/skills/sc-troubleshoot-protocol/SKILL.md` and project `.claude/skills/sc-troubleshoot-protocol/SKILL.md` | Runtime/development copies, not source-edit targets. The installed keyword rows match the source when read. The project skill directory is absent in this worktree; synchronization must populate it before verifying. Do not stage generated `.claude/` copies. |
| `Makefile` | `sync-dev` copies source primitives into development mirrors; `verify-sync` checks for absent/different copies. Implementation must run both and record the observed result; neither ran in this check. |
| `tests/troubleshoot/` and broader `tests/` | Existing protocol contract/replay tests exist. Bounded searches found no dedicated assertion for these phrase-to-type rules; preserve the issue's conditional test requirement rather than inventing a new test system. |
| #609, #611 and #612 | Parent sequencing and comparison dependency were verified from live bodies. #611 waits for this baseline; #612 waits for a favorable #611 result. Formal GitHub dependency edges were not checked. |
| `.dev/iterations/iteration-3/stories/610.md` | Current story instructions and later decision handoff; merged documentation does not establish implementation. The orchestrator handles the story's decision-append step separately. |
| `.dev/issues/610/accuracy-check.md` | Detailed claim checks, relevant PR/commit effects and limitations. All 117 saved PR entries were screened; 24 individual file lists have 100 entries and may omit further paths. Current integration source and focused path history support the verdict independently. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.

Auggie and codegraph tools were unavailable; inspection used Read, Grep, Glob and read-only git/GitHub queries. No manual troubleshooting run, test execution or synchronization verification was performed. Those remain implementation acceptance work, not claimed passes.

## Decided for this work (iteration 3)

- Nothing to decide: build what the issue asks for, within its own scope.
