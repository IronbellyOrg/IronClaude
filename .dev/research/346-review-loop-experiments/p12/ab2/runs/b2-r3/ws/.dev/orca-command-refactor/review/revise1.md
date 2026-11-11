# Revise 1: orca-worker-contract-spec.md

- prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:58-60` (read in full first)
- IDS: B-1 (the only confirmed blocking id; `review/round1.md:2` names it, B-2 is not in IDS and is not touched)
- candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- shared context read first: `.dev/orca-command-refactor/README.md` (rules at README:29-38 applied: planning only, only assigned files written)
- no PASS awarded; the candidate is returned once for the re-review.

## Byte accounting

| item | bytes |
|---|---|
| size before | 57763 (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`; equals the size in `review/round1.md:7`) |
| size after | 57803 (sha256 `5082997e7df1eb90f5c3852b329722d02c4c86bb728e0f29c56b6b9bb7dfa478`) |
| net | +40 |

Per finding id:

| id | bytes added | bytes deleted | where |
|---|---|---|---|
| B-1 | 40 (two insertions of ` except `load` (B-1)`, 20 bytes each) | 0 | spec line 195 (AC-1.1) and spec line 76 (section 3 intro) |
| all other ids | 0 | 0 | not touched |

Sizes were measured with `wc -c` before and after; the +40 equals 2 x 20.

## Findings table

| id | disposition | detail |
|---|---|---|
| B-1 | applied | Chosen option: the narrowing that `review/round1.md:49` prefers ("narrow AC-1.1 to name the exception ... Prefer the narrowing, one clause") instead of changing the load row and Decision. Edit 1, spec line 195 (AC-1.1): "every command in sections 3.1-3.2 except `load` (B-1) has a `## Unattended mode` section ...". Edit 2, spec line 76 (section 3 intro, which `round1.md:47` cites as S:76): "Every changed command except `load` (B-1) also gains the `## Unattended mode` section". Without edit 2 the same contradiction survives in prose: `load` has a changed Usage line (spec line 112, Phase "P1 (usage line only)"), so it is a "changed command" and would be told to gain the section while its row says Report "none (see note)". Text left as it was, because it now agrees with the narrowed scope: load row (spec line 112: Report "none (see note)", Phase "P1 (usage line only)", "use it as a step inside another worker's brief, not as its own Task") and the Decision (spec line 265: "a report file would be an unrequested addition. Only its usage-line defect is fixed."). Support for keeping load without a contract: `inventory/commands-b.md:65` ("it only loads context into the current session and writes no file, so a worker has nothing to report. Better used as a step inside a worker brief than as a dispatched task") and `inventory/commands-b.md:31`. |

Rejected: none.

## Why no other text was changed

- The test clause "and that no section-4 command has one" (spec line 195) is unchanged; adding an assertion that `load` has none would be a new rule no listed finding calls for.
- Spec line 52 (section 2.1, "Each changed command adds a short `## Unattended mode` section") is a general definition and was not named by B-1's brief (`round1.md:189`); section 3's intro, which scopes it per command, now carries the `load` exception. A re-reviewer who reads line 52 alone as binding for `load` would see a residual wording overlap; it was left alone per "Revise only text a blocking finding names" (`round1.md:186`). It is a one-clause follow-up if the re-review wants it.
- Spec line 159 (P1: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)") still includes `load` as a flag-accepting no-op; this is about the flag, not the section, and no blocking finding names it. Left alone.
- B-2 and all Medium and minor findings (M-1 to M-14, N-1 to N-5) are left alone as instructed (`round1.md:186`).

## Verification

- `grep -nF 'except `load` (B-1)'` finds exactly spec lines 76 and 195.
- No section, rule or mechanism was added; every addition carries the id B-1.
