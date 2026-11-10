# Revise 2: Orca worker-contract spec

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51`. Citation keys: `spec:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` after this revision (no line added or removed, 285 lines before and after). `r2:N` = line N of `.dev/orca-command-refactor/review/round2.md`. `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md`. Read first: `.dev/orca-command-refactor/README.md` (binding shared context).

Scope: only the blocking id in the Reviser brief (`r2:237`): NEW-1. REQ-1, REQ-2 and ARCH-1 are resolved and not touched. Medium and minor items (M-1 to M-13, N-1 to N-8) were left alone. Edited file: the spec only. No spec-panel was run. No PASS is claimed.

## Byte accounting

| Item | Value |
|---|---|
| Candidate size before | 59765 bytes (285 lines), sha256 `cf9b3e748906ea7675896ba4ee5a7993c98b0ab7a8ec22a0e9311df04e7ebb69` (equals the "after" hash recorded in `revise1.md`) |
| Candidate size after | 59941 bytes (285 lines), sha256 `83f24502ee791d296bebd644adce8eba84b0a7bccbb076f090415ba276880733` |
| Net | +176 bytes (176 added, 0 deleted; a single insertion, checked with `diff` on line 73 only) |

| Finding | Bytes added | Bytes deleted |
|---|---|---|
| NEW-1 | 176 | 0 |
| Total | 176 | 0 |

## Disposition per finding

| Id | Disposition | Where applied | What changed | Why this and not more |
|---|---|---|---|---|
| NEW-1 | Applied | `spec:73` (section 2.3) | After "a `--retry-of` retry included" the sentence now continues "unless that retry resumes (WC-6) from state kept in that directory (roadmap: `.session-memory.md`), in which case its brief passes that directory with the resume flag (NEW-1)". The ban on reusing a directory now yields to WC-6's first branch, so a stalled roadmap retry is briefed with `--resume --output D1` and finds `D1/.session-memory.md` (`r2:158-168`; state file location `INV-B:153`, spec:205) instead of an empty D2. | This is the narrowing recommended at `r2:174`: one clause in the one sentence the finding names (spec:73), no new rule, mechanism or section. WC-6 (spec:64) needed no edit: its first branch ("resumes from its on-disk state when given its resume flag") already requires the resume, and its second branch (no resume flag, distinct directory) stays correct. The existing exceptions list (cleanup-audit, workflow) is unchanged. Commands whose resume input is an explicit file path (tdd, brainstorm, release-split) are not hit and keep the distinct-directory rule (`r2:172`). AC-2.2's retry case (spec:200) still holds for commands without a resume flag and was not edited. Inline note: I did not rewrite the roadmap row (spec:118), because the clause is enough for the reading and the finding does not call for more. |

## Residual notes (not fixed, outside the blocking id)

- The new clause is stated generally ("unless that retry resumes") with roadmap as the named case. Whether adversarial `--pipeline-resume` keeps its manifest inside `--output <dir>` is not stated in the inventory (`r2:166`); if it does, the same clause already covers it. UNVERIFIED.
- Under the clause a resume retry rewrites the contract in the same directory, so AC-2.2's "leaves the first contract unchanged" applies only to the no-resume-flag case; the wording of that AC was left as is (Medium or lower, not a blocking id).
- Only `spec:`, `r2:`, `INV-B:153` and the prompts file were checked here; no citation to files outside the sandbox was added.
