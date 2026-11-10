# Revise 1: orca-worker-contract-spec.md

- Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (REVISE section, "Repair only the blocking findings ... Report the byte size before and after, and the bytes added and deleted per finding id").
- Blocking ids (from `.dev/orca-command-refactor/review/round1.md`, Reviser brief): F1, F2 and only those.
- Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (no other file touched except this one).
- Citation shorthand: `spec:N` = line N of the candidate (line numbers unchanged by the edits: 285 lines before and after). `round1:N` = `.dev/orca-command-refactor/review/round1.md`.
- Evidence checkable in the workspace: `spec:154,158,159,182,183,194-196` (read), `spec:112,265` (read), `round1` Reviser brief. The F1 and F2 repairs rest only on these lines; no outside citation is relied on.

## Byte accounting

| | Bytes | Lines | sha256 |
|---|---|---|---|
| Before | 57763 | 285 | `d3cdbe578...25200d` (full: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`) |
| After | 57973 | 285 | `d1f34e4bb75f645e00e9b421dc8abdf0366d981ef45c7dfcc8f6689db8833a6a` |
| Net | +210 | 0 | |

| Finding | Lines touched | Bytes added | Bytes deleted |
|---|---|---|---|
| F1 | `spec:182`, `spec:194` | 97 + 41 = 138 | 0 |
| F2 | `spec:195`, `spec:196` | 53 + 19 = 72 | 0 |
| Total | | 210 | 0 |

Added bytes equal the net size change (57763 + 210 = 57973); nothing was deleted because each repair narrows an existing condition by appending a qualifier.

## One row per finding id

| Id | Disposition | Where applied | What changed |
|---|---|---|---|
| F1 | Applied | `spec:182` (7.2 step 3 pass condition) and `spec:194` (AC-0.4 pass condition) | Step 3 now reads: `--outcome` matches the contract's `status` under WC-5 "(in P0, the worker's own account of the result)"; report path is the WC-4 contract path "(in P0, the command's existing report file)". AC-0.4 now says "steps 1-3 and 5-7 pass, with step 3 read by its P0 wording; step 4 uses the command's existing report file, since the contract arrives in P1." The WC-4 wording is unchanged and applies from P1 on. This removes the contradiction round1 named (step 3 required a contract that `spec:158` says P0 cannot create and `spec:159` says P1 creates), so the P0 gate in `spec:154` can pass. No rule, mechanism or section added. |
| F2 | Applied | `spec:195` (AC-1.1) and `spec:196` (AC-1.2) | AC-1.1 now quantifies "every command in sections 3.1-3.2 except `load` (usage-line fix only, no contract; F2)". AC-1.2 now reads "each P1 command except `load` (F2)". `load` keeps its stated Decision (`spec:265`: no report file, usage-line fix only) and its row (`spec:112`); no report file or section is added to it. This is the first option in round1's F2 recommendation (exempt `load` in one clause). |

## Not changed, deliberately

- `spec:159` still lists `load` under the P1 blanket "`--unattended` accepted by every command in sections 3.1 and 3.2". Round1 gave `spec:112` and `spec:159` only as an alternative scope; the chosen repair (AC exemption) makes AC-1.1 and AC-1.2 passable without touching it, and no acceptance check tests that clause for `load`. Left alone to avoid an addition no listed finding calls for.
- Medium findings F3-F14 and minor notes N1-N8 are untouched, as the Reviser brief requires (`round1` Reviser brief, "Leave Medium and minor findings alone").
- I did not run the spec-panel and make no claim that the repaired candidate passes; that is for the re-review.
