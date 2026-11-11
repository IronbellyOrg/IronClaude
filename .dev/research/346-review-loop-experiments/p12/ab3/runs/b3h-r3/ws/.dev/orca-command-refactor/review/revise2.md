# Revise pass 2: Orca worker contract spec

- Prompt: REVISE, from `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox path `home/.claude/rules/prompts/document_review_loop_prompts.md`, REVISE section).
- Input report: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`). Its Reviser brief lists one blocking id: F-19 (`review/round2.md:168-172`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Brief scope: repair only F-19. F-20, F-21, F-22 and N-1 are Medium or minor and are left alone (`review/round2.md:170`).

## Byte accounting

| Item | Before | After |
|---|---|---|
| Candidate size (bytes) | 58893 | 58948 |
| Candidate sha256 | `b4832d456dbf9b742b18a39e1442803bd1c9b0e19aafedbf70079e7911d839c2` (matches `review/round2.md:9`) | `d7b701458ccab1292a94ee6f2c84881cfc91dbf20d522f329d407123b072388d` |
| Line count | 285 | 285 (only line 62 changed) |

Net change: +55 bytes, all on line 62 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62`).

| Finding id | Bytes added | Bytes deleted | Where |
|---|---|---|---|
| F-19 | 55 (28 for ` that accepts \`--unattended\``, 27 for ` (\`load\` is excluded, F-19)`) | 0 | `specs/orca-worker-contract-spec.md:62` |
| F-20, F-21, F-22, N-1 | 0 | 0 | not touched |
| Total | 55 | 0 | |

## Per-finding rows

| Finding | Disposition | Where applied or reason |
|---|---|---|
| F-19 (BLOCKING) | Applied | `specs/orca-worker-contract-spec.md:62`. The sentence "Every command in section 3 writes to this one path" now reads "Every command in section 3 that accepts `--unattended` writes to this one path (`load` is excluded, F-19)". The exclusion matches `:52` (`load` excluded from the Unattended mode section, F-05), `:112` (`load` row, no gate, no unattended mode), `:159` and `:195` (AC-1.1 excludes `load`), and `:265` (Decisions: a report file for `/sc:load` is an unrequested addition). No other text was changed. The rest of the WC-4 sentence, including the output-directory flag clause (F-03), is unchanged. |
| F-20 (MEDIUM) | Rejected for this pass | Out of scope: the brief names only F-19 and says to leave Medium findings alone (`review/round2.md:170`). Not edited. |
| F-21 (MEDIUM) | Rejected for this pass | Out of scope, same reason (`review/round2.md:170`). Not edited. |
| F-22 (MEDIUM) | Rejected for this pass | Out of scope, same reason (`review/round2.md:170`). Not edited. |
| N-1 (minor) | Rejected for this pass | Out of scope: minor findings are left alone under the brief (`review/round2.md:170`). Not edited. |

## Consistency check of the edit

- Other sentences that restate the every-command rule already exclude `load`: `:52`, `:159` (P1 row, "except `load` (F-05)"), `:195` (AC-1.1), and `:265` (the `/sc:load` handling row). The narrowed `:62` now agrees with them.
- The per-command rows that name `return-contract.yaml` (`:83`, `:84`, `:88`, `:92`, `:116`) are unchanged. None of them names `load`.
- No rule, mechanism, or section was added. The only addition is the two parenthetical scope qualifiers above, each citing F-19.

## Coverage

- Read: `review/round2.md` (Reviser brief at `:168-172`, F-19 at `:103-112`, the Step 1 evidence block), `specs/orca-worker-contract-spec.md` (`:55-70`, `:110-116`, `:155-160`, `:193-197`, `:263-267`, and line 62 in full), and `README.md` (shared context, `README.md:1-38`). The README's output table names `review/disposition.md` for the revise step; this run's brief names `review/revise2.md`, and the brief was followed.
- Not checked: the files under `inventory/`, since the F-19 fix depends only on text inside the spec and round2. Citations into `CAPS:`, `INV-A:`, `INV-B:` and `sk/` are inherited text and were not re-verified; they are UNVERIFIED in this sandbox.
- Spec-panel was not run. No PASS is claimed. Per the brief, this is one candidate return with no self-awarded verdict.
