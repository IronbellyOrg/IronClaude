# Revise round 1: Orca worker contract spec

- Brief: REVISE prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, `REVISE prompt`, lines 53-55).
- Candidate revised: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place, once).
- Review input: `.dev/orca-command-refactor/review/round1.md`, `Reviser brief` (lines 189-191) lists F-01 to F-05 as the only blocking ids.
- Ids repaired: F-01, F-02, F-03, F-04, F-05. Medium findings F-06 to F-18 and minor notes N-1 to N-3 are not touched (`review/round1.md:181-187`).
- No PASS is awarded here. The candidate is returned for the next review.
- Scope check: the candidate is 285 lines before and after, so every line number in the original (`SPEC:n`) is unchanged. Edits are inside the lines listed in the rows below.

## Byte accounting

| | Bytes | sha256 |
|---|---|---|
| Before (round 1 candidate, `review/round1.md:6`) | 57763 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| After (revised candidate) | 58893 | `b4832d456dbf9b742b18a39e1442803bd1c9b0e19aafedbf70079e7911d839c2` |
| Net change | +1130 | |

Per finding id (UTF-8 bytes; added and deleted are the changed characters per edit, counted from the common prefix and suffix of each replacement):

| Finding | Edits | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| F-01 | 3 | 323 | 69 | +254 |
| F-02 | 2 | 168 | 0 | +168 |
| F-03 | 4 | 567 | 144 | +423 |
| F-04 | 3 | 336 | 139 | +197 |
| F-05 | 4 | 88 | 0 | +88 |
| **Total** | **16** | **1482** | **352** | **+1130** |

The total net change equals the file size difference (58893 - 57763 = 1130). No edit was made outside a finding's row below.

## Rows, one per blocking finding

| Id | Disposition | Where applied (after-edit line numbers) | Bytes +/- | Reason and citations |
|---|---|---|---|---|
| F-01 | Applied | `SPEC:73` (section 2.3, new coordinator rule); `SPEC:85` (cleanup-audit row, small fix); `SPEC:86` (index-repo row, small fix) | +323 / -69 | The two ready-today rows write fixed paths (`INV-A:42` cleanup-audit `.claude-audit/`, `INV-A:53` index-repo `PROJECT_INDEX.md`). WC-11 (`SPEC:69`) forbids two workers writing one file in one worktree. Fix: the coordinator runs at most one such worker per worktree until P1 adds a per-slug output flag. Rows stay ready today, so the 10 / 27 / 6 split at `SPEC:76` is unchanged. Workers share the current worktree by default (`CAPS:115`, `[G:placement]`). |
| F-02 | Applied | `SPEC:61` (WC-3, answer limits); `SPEC:234` (D2 option (a), no Ruling in an answer) | +168 / 0 | WC-3 let an `ask` answer re-invoke the command with an outward flag, which WC-9 (`SPEC:67`) and D4 (`SPEC:245`) reserve for the brief or the person. WC-3 now says an answer never carries an outward flag, and never a Ruling unless the user chooses D2(b). D2(a) states that no answer carries a Ruling. The `ask` call itself (`CAPS:58`, `[H:ask]` line 3) and the pull rule (`CAPS:61`) are unchanged. |
| F-03 | Applied | `SPEC:62` (WC-4, one path for every command, plus output-directory flag rule); `SPEC:83` (adversarial, contract moved to `<output>/return-contract.yaml`); `SPEC:92` (workflow, `--output-dir` for the contract); `SPEC:116` (research, `--output-dir` added) | +567 / -144 | Workflow's contract sits in `.dev/tasks/to-do/<id>/` where the run creates `<id>` (`INV-B:52`, `INV-B:272`), so it is unknown before dispatch. Research's file name is generated at run time (`INV-B:132`). Adversarial nested its contract under `adversarial/`. WC-4 now requires one path, `<output-dir>/return-contract.yaml`, and gives each command that lands elsewhere an output-directory flag. The `worker_done --report-path` fallback is not used, because Orca's handling of the file is UNVERIFIED (`CAPS:79`). Research keeps its P2 phase (`SPEC:156-162`) rather than moving to P1; the finding allowed either. |
| F-04 | Applied | `SPEC:147` (SA-2, exempt file named); `SPEC:158` (P0, HOW-WE-WORK Orca section written in prose); `SPEC:172` (AC-C1, exempts only `src/superclaude/core/WORKER-CONTRACT.md`) | +336 / -139 | AC-C1 (`SPEC:172`) matched the `orca orchestration` form that SA-2 allowed in the contract (`CAPS:58`, the form of the `ask` example). The chosen fix exempts that one file in AC-C1 and makes the HOW-WE-WORK Orca section prose-only, so AC-C1 still covers it. The exemption grep is a text edit; its run result is UNVERIFIED here because `src/` is absent from this sandbox. |
| F-05 | Applied | `SPEC:52` (section 2.1, contract file adds `## Unattended mode` except `load`); `SPEC:76` (section 3 intro, same exception); `SPEC:159` (P1, `--unattended` flag not required for `load`); `SPEC:195` (AC-1.1, `load` exempt) | +88 / 0 | `load` is in section 3.2 with report "none" and a usage-line fix only (`SPEC:112`, `INV-B:65`). The Decisions table says a report file for `load` "would be an unrequested addition" (`SPEC:265`). AC-1.1 (`SPEC:195`) required an `## Unattended mode` section for it. The chosen fix narrows the requirement to exclude `load`, which the finding allowed. `load` stays in 3.2 and the row (`SPEC:112`) is unchanged, so the 27 count is unchanged. |

## Checks made

- Every new or changed sentence carries its finding id, as the brief requires.
- Inventory citations used in the new text were read in this sandbox: `inventory/commands-a.md:42,53`, `inventory/commands-b.md:52,65,132,272`, `inventory/orca-capabilities.md:58,61,67,73,79,90,115`. Each matches the claim it supports.
- Source citations (`src/superclaude/...`, `sk/...`, `cmd/...`, `CLAUDE.md`, `pyproject.toml`) are carried from the spec and were not re-read here; they are UNVERIFIED in this sandbox. No new source citation was added.
- The grep in AC-C1 (`SPEC:172`) was not run, for the same reason. Its exemption is a text change only.
- No section outside rows F-01 to F-05 was altered; the byte totals above account for every change.
- The candidate was returned once. No review was run and no PASS is claimed.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| F-01: keep ready-today rows and add a one-per-worktree rule | Move cleanup-audit and index-repo to needs-change; keep ready and add a rule | The rule keeps the 10 / 27 / 6 split and the brief's "narrow, do not widen" scope. The per-slug flag still lands in P1 (`SPEC:159`, `SPEC:85-86`). |
| F-03: keep research in P2 | Move research to P1 | The finding allowed either. Moving phases would change the P1 and P2 command lists (`SPEC:159-160`), which the brief did not ask for. |
| F-04: exempt one file and keep HOW-WE-WORK prose-only | Rewrite the example so it does not match; exempt the HOW-WE-WORK section | Exempting one file is the smallest text change. Prose-only HOW-WE-WORK keeps the grep meaningful for the routing guide. |
| F-05: exempt `load` | Move `load` to section 4 | Exempting `load` leaves its row and count unchanged. The finding allowed either. |
