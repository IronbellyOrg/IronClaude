# Revise 1 (REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
input report: .dev/orca-command-refactor/review/round1.md (`review: 1 of 3`, `verdict: FAIL`), its Reviser brief
IDS (blocking, confirmed by VF1): M2, M4, M6, M7, M8, M9
baseline (before revision): sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d, 57763 bytes, 285 lines (matches the candidate hash in round1.md)
candidate (after revision): sha256 6f240e27e8d58d66b8256a439936eb55132bda0b917254aa463c5abc36931750, 60372 bytes, 309 lines
Inputs read: README.md (shared context), round1.md, the full spec, inventory/commands-a.md, commands-b.md (cited lines only). Cited `cmd/` and `sk/` files are outside the workspace; citations to them are carried from the spec and marked UNVERIFIED below.

## Byte accounting

Method: word-level diff of each changed line pair against the baseline (changed tokens only, whitespace-only separators not counted), and whole-line counts for rows or blocks that were removed or inserted. Bytes exclude line terminators. Each finding is counted only on the lines or tokens its edit changed. Lines that serve two findings are split by the clause each finding owns; the one shared Decisions row is split by its clauses (the counts below are the split).

| Finding | Bytes added | Bytes deleted | Where (candidate lines) |
|---|---:|---:|---|
| M2 | 210 | 46 | init-lite row in 3.1 (line 86) |
| M4 | 300 | 51 | AC-0.4 cell (line 218) |
| M6 | 803 | 193 | 2.3 cleanup-audit sentence (line 73, +146); 3.1 heading count (line 78, 4 deleted, 3 added); intro count (line 76, 5 deleted, 1 added); index-repo row removed from 3.1 (baseline line 86, 163 deleted) and added to 3.2 (line 111, +317); P0 phase text (line 159, 11 deleted, 29 added); Decisions "Inventory verdicts" row (line 292, index-repo clauses and "Keep" wording: 10 deleted, 307 added) |
| M7 | 650 | 305 | load row removed from 3.2 (baseline line 112, 249 deleted); note under the 3.2 table (lines 126-127, +432); paragraph before section 4 (line 140, 24 deleted, 91 added); intro load clause (line 76, 3 deleted, 69 added); Decisions row load clauses and "recommend" wording (line 292, 29 deleted, 58 added) |
| M8 | 349 | 62 | WC-4 row (line 62, +131); intro "Contract" clause (line 76, 36 deleted, 95 added); AC-1.4 cell (line 222, 26 deleted, 123 added) |
| M9 | 1417 | 496 | AC-C1 row (line 173, 232 deleted, 179 added); AC-C4 row (line 176, 91 deleted, 65 added); AC-C5 row (line 177, 86 deleted, 65 added); fenced block after the 7.1 table (lines 179-193, +845); AC-0.3 row (line 217, 87 deleted, 66 added); fenced block after the 7.3 heading (lines 206-211, +197) |
| Total | 3729 | 1153 | token-level net +2576 |

Reconciliation: 60372 - 57763 = +2609 bytes. Token-level net is +2576. The remaining +33 is +24 line terminators (285 to 309 lines) and about 9 bytes of separating spaces that the word-level count does not include.

No edit was made for M1, M3 or M5. The verifier rejected these, so they are not blocking, and their text (the WC-4 "directory the coordinator passed" wording, WC-5 mapping, and the P1 `--unattended` row) is unchanged. The WC-4 change at line 62 adds a sentence after the unchanged text.

## Findings

| ID | Status | Applied where, or rejected with reason |
|---|---|---|
| M1 | not actioned (verifier rejected; noted) | Not in IDS. Not revised. Still a noted, unactioned follow-up for the next re-review. The WC-4 text it cites is unchanged apart from the appended M8 sentence. |
| M2 | applied | 3.1 init-lite row (line 86): brief becomes `--output <dir>` after P1, Resume becomes "Fresh dir per run (WC-6)", and Small fix becomes a P1 per-run output directory, so a retry does not overwrite the first `context-audit.md`. Source: `INV-A:55` ("a marked report is overwritten on re-run", `sk/sc-init-lite-protocol/SKILL.md:66`, cited in the row). |
| M3 | not actioned (verifier rejected; noted) | Not in IDS. WC-5 is unchanged. |
| M4 | applied | AC-0.4 cell (line 218). Steps 1, 2, 5, 6, 7 unchanged. P0 step 3 is restated for P0 (exactly one `worker_done`; `--outcome` matches the status the existing report states; the report path is the existing report). Step 4 is removed from P0 and runs first in P1 (AC-1.2). The "uses the command's existing report file" wording is deleted. Section 7.2 is not edited. |
| M5 | not actioned (verifier rejected; noted) | Not in IDS. Section 3 row for auggie-review and the P1 scope (line 160) are unchanged. |
| M6 | applied | (a) Section 2.3 (line 73): cleanup-audit coordinator rule, one cleanup-audit per worktree (WC-11). (b) index-repo moved from 3.1 (ready) to 3.2 (needs a change, line 111) with an `--output <dir>` requirement in P1; counts changed to 3.1 "(9)" (line 78), intro "9 ready today ... 27 needing a change ... 6 coordinator-only ... load" (line 76). (c) P0 "Uses only the 9 ready commands (section 3.1)" (line 159). (d) Decisions row (line 292) records the move. Reason for deviating from the inventory: `INV-A:53` gives index-repo a ready verdict with default `PROJECT_INDEX.md` at the repo root (location "implied, UNVERIFIED"), and WC-11 (line 69) requires a timestamped or coordinator-passed slug. The move follows the blocking finding's recommendation ("move index-repo to needs-change"). |
| M7 | applied | `/sc:load` removed from the 3.2 table (its row was baseline line 112). A note after the table (lines 126-127) gives its status: no contract, no Unattended mode section, used as a brief step, and its usage-line fix stays in P1 (SA-4). Paragraph at line 140 now points to that note. AC-1.1 needs no text change because it covers sections 3.1-3.2 only. Decisions row (line 292) records the removal. Recommendation chosen: the first of the two options in the finding ("remove load from the section 3.2 table and from AC-1.1"). |
| M8 | applied | WC-4 (line 62): after the unchanged "directory the coordinator passed" text, the contract path is the path section 3 names for that command, with adversarial (section 3.1) as the exception. Section 3 intro (line 76): "Contract" means the WC-4 file at the path WC-4 gives, default `<output-dir>/return-contract.yaml`. AC-1.4 (line 222): checks adversarial's SKILL against the section 3.1 path `<output>/adversarial/return-contract.yaml`, and no other path. The adversarial row in 3.1 is unchanged, since it already names that path. |
| M9 | applied | AC-C1, AC-C4, AC-C5 (lines 173, 176, 177) and AC-0.3 (line 217) now name a command in a fenced block, so the pipes are plain `|` in the raw text. The fenced blocks are at lines 180-193 (common checks, with a new AC-C1 positive control that must print a planted `orca-ide worktree list` line, per the finding's recommendation) and lines 206-211 (AC-0.3). The `\|` escapes are gone from every check. |

## Notes for the reviewer

- Scope: edits are limited to text a listed finding names, plus the count and note consequences that follow directly (section 3 counts, P0 phase text, the Decisions rows for inventory verdicts). Every added sentence or cell carries its finding id in square brackets, as the REVISE prompt asks. No new mechanism was added.
- Sections 1, 4, 5, 8, 9 and the UNVERIFIED list were not changed.
- The Decisions row "Inventory verdicts" (line 292) now records the index-repo move and the load removal. Its earlier claim that nothing read contradicted a verdict is removed.
- Citations: `INV-A:53`, `INV-A:55`, `INV-A:60` and `INV-B:65` were read in `inventory/commands-a.md` and `commands-b.md` and match the claims above. Citations to `cmd/*.md` and `sk/*.md` lines are outside the workspace and are UNVERIFIED here; they were carried from the spec unchanged. The WC-4 and adversarial path claims (M8) also rest on `commands-a.md:60`, which I read, and on the PR #329 contract files outside the workspace (UNVERIFIED).
- The baseline copy used for the byte accounting is kept at `.../runs/b1h-r4/baseline-spec.md` outside the workspace. No other file was changed.
