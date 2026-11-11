# Revise round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. IDS = B-1. Source of blocking ids: `review/round1.md` Reviser brief ("Blocking finding ids: B-1").
- Note: `~/.claude/rules/prompts/document_review_loop_prompts.md` does not exist under the sandbox home, so the REVISE prompt itself could not be read (UNVERIFIED). I followed the Reviser brief in `review/round1.md` (section "Reviser brief") and the coordinator brief instead. Spec-panel not run.
- README read: `.dev/orca-command-refactor/README.md:1-38`.

## Byte accounting (spec file)
- Before: 57763 bytes. After: 57867 bytes (`wc -c`). Net +104.
- Per finding: B-1 added 104 bytes (three short qualifiers), deleted 0 bytes. No other finding touched.

## Findings
| id | disposition | where / reason |
|---|---|---|
| B-1 | applied (narrowest repair named in round1.md Reviser brief) | `/sc:load` excluded from the P1 flag requirement at spec:159, from AC-1.1 at spec:195, and from AC-1.2 at spec:196, each with a "(B-1 ...)" tag. The AC-1.2 text cites `INV-B:65` (load "writes no file", cited also at spec:265) as the reason. Load stays in the P1 command list for its usage-line fix only (spec:112, spec:159 "load (usage line only)"). Section 3 row and Decisions table unchanged, since they already say load writes no report (spec:112, spec:265). |
| M-1 to M-16, N-1 to N-3 | not applied | Medium, minor and note items; the Reviser brief says "Leave Medium and minor findings alone". |
