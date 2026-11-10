# Revise (gate loop): F-1

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; prompt: REVISE, `~/.claude/rules/prompts/document_review_loop_prompts.md` (IDS = F-1, from `review/gate.md` Reviser brief).
- bytes before: 59339 (matches `review/gate.md` header); bytes after: 59523; net +184.
- Not run: spec-panel. No PASS claimed.

## Byte accounting per finding id
| id | added | deleted |
|---|---|---|
| F-1 (edit 1, section 3.2 cli-portify row, spec line 105) | 99 | 0 |
| F-1 (edit 2, AC-2.3, spec line 201) | 85 | 0 |
Total added 184, deleted 0 (the edits only append inside two table cells).

## Findings
| id | disposition | where / reason |
|---|---|---|
| F-1 | applied (narrowing, no new mechanism) | Chose the review's second option. Line 105 now says no flag pre-approves a gate, so every unattended cli-portify run ends `blocked` until a person approves; line 201 (AC-2.3) excludes cli-portify from the happy-path set, leaving AC-2.2 (gate-trigger, `blocked`) as its acceptance. Removes the contradiction between line 105 and AC-2.3 (gate.md F-1). The first option (an approval flag) was not taken because it adds a flag; the inventory's `--resume` stays unchanged. Evidence: gates always on, `INV-A:45`. Other Medium and minor findings left alone per brief. |
