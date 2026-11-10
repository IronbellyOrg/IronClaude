# Revise 2: REVISE prompt, IDS = B1

Brief: `~/.claude/rules/prompts/document_review_loop_prompts.md` REVISE prompt (lines 60-62), read in full (lines 1-67). Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Input report: `.dev/orca-command-refactor/review/round2.md` (`review: 2 of 3`, Reviser brief lists B1 only). Confirmed by `.dev/orca-command-refactor/review/verify-2.md` (`confirmed: B1`), which the brief names as the VERIFY reply.
Inputs read: the candidate, `.dev/orca-command-refactor/README.md`, `.dev/orca-command-refactor/inventory/commands-b.md` (`:57-65` for `/sc:load`), and the candidate's sections 2.2, 3.2, 6, 7.3 and Decisions. `specs/history/spec-v1.md` was not edited and not needed.
Not checkable here: `src/superclaude/commands/load.md` (cited as `cmd/load.md`). Its citations are carried from `commands-b.md` and are marked UNVERIFIED where they are only quoted there.

## Hashes and size

| Item | Value |
|---|---|
| Candidate sha256 before (`bddecb0d...`, as in `round2.md:6` and `verify-2.md`) | `bddecb0d53d012639197cb333a623b97ec5dd535120f7fee296fb97a980e41db` |
| Candidate sha256 after | `d7bacfaaecc8fff9a059e1e70fe785b1e6c52aecb2a57c161ca8d51cdcb3aa3c` |
| Size before | 60031 bytes, 288 lines |
| Size after | 60339 bytes, 288 lines |
| Net change | +308 bytes (added 643, deleted 335, from the four edits below; 643 - 335 = 308, matching the size change) |

Line numbers did not move: the three edited rows stay at `spec:112`, `spec:159` and `spec:268`.

## Byte accounting per finding id

| Id | Edit (location after revise) | Bytes deleted | Bytes added |
|---|---|---|---|
| B1 | `specs/orca-worker-contract-spec.md:112`, load row, Unattended text | 102 | 162 |
| B1 | `specs/orca-worker-contract-spec.md:112`, load row, Phase column | 41 | 71 |
| B1 | `specs/orca-worker-contract-spec.md:159`, P1 row, load entry | 23 | 82 |
| B1 | `specs/orca-worker-contract-spec.md:268`, Decisions row, `/sc:load` handling | 169 | 328 |
| total | | 335 | 643 |

No other line changed. WC-4 (`spec:62`), AC-1.1 (`spec:196`) and the rest of section 3 are unchanged.

## Finding rows

| Id | Disposition | Where | Reason (with cite) |
|---|---|---|---|
| B1 (= M8) | Applied | `spec:112` (load row), `spec:159` (P1 row), `spec:268` (Decisions row) | Chose option 1 of the round-2 Reviser brief, not option 2. Option 1 gives load a contract with `status`, `command` and `artifacts: []`, so the load row now meets WC-4 (`spec:62`, which lists `artifacts` without an "if any" qualifier). The P1 row now adds load's `## Unattended mode` section, so AC-1.1 (`spec:196`, which covers every command in 3.2 and load is in 3.2 at `spec:112`) can pass. The Decisions row (`spec:268`) now agrees with both. Option 2 (an exception in WC-4 and AC-1.1) would have edited two more texts that the finding does not name, so it was not used. The empty `artifacts` list needs no WC-4 change: the list covers "every other file written", and load writes none (`.dev/orca-command-refactor/inventory/commands-b.md:65`, "writes no file"). |
| R2-1 | Not revised | none | Medium, outside IDS (`round2.md:88`). The brief says leave Medium and minor findings alone. |
| R2-2 | Not revised | none | Medium, outside IDS (`round2.md:89`). |
| R2-3 | Not revised | none | Medium, outside IDS (`round2.md:90`). |
| R2-4 | Not revised | none | Medium, outside IDS (`round2.md:91`). |
| R2-5 | Not revised | none | Medium, outside IDS (`round2.md:92`). |
| R2-6 | Not revised | none | Minor note, outside IDS (`round2.md:93`). |
| M2, M4, M7, M9, M10 | Not touched | none | Resolved in `round2.md:63-68`; not in IDS. |
| M1, M3, M5, M6, M11, M12 | Not touched | none | Noted, unactioned (`round2.md:127-136`); not in IDS. |

## Self-check (fixed-string grep on the candidate)

Each new text is found in the candidate, once per edited row:

- `contract under \`--unattended\` with \`status\`, \`command\` and \`artifacts: []\``: `spec:112`
- `P1 (usage line; \`## Unattended mode\` section) [B1]`: `spec:112`
- `load (usage line, and the \`## Unattended mode\` section that AC-1.1 requires) [B1]`: `spec:159`
- `writes a contract with \`status\`, \`command\` and \`artifacts: []\` and no report file [B1]`: `spec:268`
- `because load writes no file (\`INV-B:65\`)`: `spec:268`

The string `M8` no longer appears in the candidate (`grep -c` returns 0), so the old wording is gone from every edited row.

## Observation for the coordinator (not a finding, not actioned)

The load row now writes a contract under `--unattended`, but the same row says load is "not its own Task" and the inventory says it is "better used as a step inside a worker brief" (`commands-b.md:65`). A contract written by a step inside a brief has no coordinator reader. This is a small consistency point, not a conflict with the blocking text: WC-4 and AC-1.1 both hold. If the coordinator wants it closed, it is a Medium-grade item for the next panel, not this revise.

## Verdict for this revise

Revise completed for B1 only. No other blocking id was in the brief, so no other text was edited. This output is not a PASS: the next step is the re-review the loop prescribes, which the coordinator runs.
