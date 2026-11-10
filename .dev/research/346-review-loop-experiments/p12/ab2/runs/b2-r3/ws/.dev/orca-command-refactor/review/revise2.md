# Revise 2: orca-worker-contract-spec.md

Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (IDS = B-2). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Inputs read: `review/round2.md` (Reviser brief, lines 142-147), the spec, `inventory/commands-b.md`, `inventory/commands-a.md`. Citation keys: S:N = spec line N; INV-A/INV-B = inventory files. Orca guides and `cmd/*`, `sk/*` paths are UNVERIFIED here and used only through inventory lines.

## Byte accounting

| item | bytes |
|---|---|
| before | 57803 |
| after | 58026 |
| net | +223 |

Per finding id: B-2 added 223, deleted 0 (two insertions, listed below). No other finding id touched.

## Findings

| id | disposition | where | reason |
|---|---|---|---|
| B-2 | applied | S:62 (WC-4): after "(`--output` / `--output-dir`)" added ", or, for a command whose `--output` is a file (init-lite, tdd), that file's parent directory, which the coordinator dedicates to this one run (B-2)" (+148 bytes). S:200 (AC-2.2): after "with a bare topic" added ", so the contract is read from the parent directory of `<file>` (WC-4, B-2)" (+75 bytes). | Defect: WC-4 defined `<output-dir>` as the `--output` value while S:87 (init-lite) and S:90 (tdd) pass a file, so the contract path would sit beneath a regular file. Inventories confirm the file meaning: INV-B:47 and INV-B:222 (tdd `--output` is the TDD), INV-A:55 (init-lite `--output` is a file). Narrowest repair per round2 "Narrowest repair" (a one-sentence WC-4 rule): the rows at S:87 and S:90 already say `--output <file>` and are now consistent unchanged; step 4 of 7.2 (S:183) takes the contract path from WC-4 so it needs no edit. No new flag, mechanism or section added. |

Edit sizes: WC-4 insertion 148 bytes, AC-2.2 insertion 75 bytes, total 223 (matches `wc -c` 57803 to 58026).

## Left alone

M-15, N-6, N-7 and all Medium and minor findings (round2.md:144). Not run: spec-panel. No PASS claimed.
