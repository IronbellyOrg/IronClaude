# Revise 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy). Blocking ids: B-1, B-2, B-3 (`review/round1.md`, Reviser brief). Medium and minor findings left alone. No PASS is claimed.

## Byte accounting (candidate `specs/orca-worker-contract-spec.md`)
- Before: 57,763 bytes. After: 58,197 bytes. Net +434.
- Per finding id (net bytes; edits are almost all insertions, deletions are a few characters of rewording):

| Id | Added | Deleted | Net |
|---|---|---|---|
| B-1 | about 152 | about 6 | +146 |
| B-2 | 235 | 0 | +235 |
| B-3 | about 59 | about 6 | +53 |

## Findings
| Id | Disposition | Where (candidate line, after edit) | What changed |
|---|---|---|---|
| B-1 | Applied (narrowing) | P1 scope in section 6, line 159; AC-1.1, line 195; AC-1.2, line 196 | The P1 `--unattended` scope now says "each command named in this row" instead of "every command in sections 3.1 and 3.2", and says `/sc:load` gets the flag and usage-line fix only, no contract (matches the load row, line 112, and its Decisions row, line 265). AC-1.1 asserts the section only for the P1-row commands except `/sc:load`, and that no section-4 command and no later-phase command has it yet. AC-1.2 excludes `/sc:load`. P2-P4 commands (including pr-submit, implement, post-release) stay deferred, consistent with D3 (a) (line 240) and line 154. |
| B-2 | Applied | WC-4, line 62; section 2.3, line 73; spec-panel row, line 120 | One rule: when the output flag is file-valued (tdd, init-lite, spec-panel) the contract is `<that file path>.return-contract.yaml`, beside the file; the directory rule is unchanged otherwise. Section 2.3 says the brief states the file path in that case. The spec-panel row now reads "add `--output <file>`; contract beside it". The tdd and init-lite rows (lines 87, 90) need no edit: WC-4 names them. Note: the sandbox `command.md:22-24,460-461` uses a separate `--report-dir`; the spec row cites `cmd/spec-panel.md:22`, which cannot be checked here (UNVERIFIED), and INV-B:43 records no output path for spec-panel, so the row was kept as an added `--output` rather than rewritten to `--report-dir`. |
| B-3 | Applied (narrowing) | AC-0.4, line 194 | Steps 3 and 4 now use the command's existing report file for the path and outcome comparison; steps 1, 2 and 5-7 must pass. Round 1 recommended changing step 3; step 4 was already covered by the existing sentence. |

## Not changed (noted)
Section 3 intro (line 76) still says every changed command gains the `## Unattended mode` section; B-1 does not name that sentence and the load exception is stated in the P1 row, so it was left alone. All citations added are spec-internal line references or finding ids; `cmd/`/`sk/` citations remain UNVERIFIED in this sandbox as before.
