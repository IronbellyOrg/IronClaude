# Fix log: Phase 6 anti-omission gate, fix pass 2 (cycle 1, the last one)

- **Phase:** fix-cycle (fix pass 2 after cycle 1)
- **Input:** `qa/qa-anti-omission-consolidated-findings-cycle1.md` (|F_1| = 1: NB-1, IMPORTANT, RECOVER)
- **Source of the finding:** `qa/qa-anti-omission-verification-qualitative.md:49` (NB-1 row), `:117-118` (verification method)
- **Report edited:** `RESEARCH-REPORT-orchestrator-mode.md` (targeted Edits only; no source file edited)
- **Baseline before edits:** `grep -c CONTRADICTION` = 6, `grep -c NB-4` = 23, 1760 lines
- **Not recovered:** MINOR notes (5 structural, M-1 to M-6), by instruction
- **Rule:** every new field, function or print location is labelled "plan decision, new design".
- **Choice required by NB-1:** the two-worktree check is a **pre-pass** over all `WorktreeState` records before `safe_to_close` (signature of `safe_to_close` unchanged). Used the same way in steps 1.3, 1.8 and 1.9.

## Source evidence re-read before editing

| Rule | Source re-read | Wording confirmed |
|---|---|---|
| (i) one package in two worktrees | `research/scope-01-contract.md:64` (`WORKER-CONTRACT.md:108`) | "It never runs one managed package in two worktrees at once." [CODE-VERIFIED] |
| (ii) context-only Dispatch | `research/scope-02-orca-recovery.md:95`; `research/05-orca-row-schema.md:20`, `:28` | "Context-only Dispatches created by orchestration dispatch are included as unsupervised with terminal state retained." [CODE-VERIFIED]; JSON field not captured |
| (iii) package states | `research/scope-02-orca-recovery.md:192` | "in `to-do/` with all tasks complete = archive-blocked; `.archiving` marker = interrupted archive" |

## Entries

| ID | Report section | Change | Source evidence |
|---|---|---|---|
| NB-1 (rule ii) | 8 Phase 1, step 1.2 `OrcaObservation` | Added `unsupervised: bool \| None`, `terminal_state: str \| None`, `next_action: str \| None`, read by rule (ii) and the terminal-releasable half only, never the class; labelled plan decision, new design. `next_action` added because the existing terminal-releasable rule in step 1.3 reads `nextAction` release and no field held it (same data-model gap) | Consolidated findings row NB-1 (required fix); verifier `qa-anti-omission-verification-qualitative.md:49` break (3); `05-orca-row-schema.md:20` (field not captured); step 1.3 safe-to-close text (`lc17-show-1.json`) |
| NB-1 (rules i, iii) | 8 Phase 1, step 1.2 `WorktreeState` | Added `package_ids: tuple[str, ...]`, `archive_states: tuple[tuple[str, str], ...]` and `shared_package_ids: tuple[str, ...]`; labelled plan decision, new design. Deviation from the suggested `archive_state: str \| None`: a tuple of (package id, state) pairs, because one worktree can hold several packages in different states (reason stated in the report) | Consolidated findings row NB-1; verifier `:49` breaks (1), (2); `scope-02-orca-recovery.md:192`; `scope-01-contract.md:64` |
| NB-1 (rule i) | 8 Phase 1, step 1.3 public functions | Added the pure pre-pass `mark_shared_packages(worktrees: list[WorktreeState]) -> list[WorktreeState]` (returns `dataclasses.replace` copies with `shared_package_ids` set), called once by `commands.py` after the step 1.4 probes and before any `safe_to_close`; `safe_to_close` signature unchanged. Covered by the sentence's existing "plan decision, new design" label | Consolidated findings row NB-1 ("pick one and use it in 1.3, 1.8 and 1.9"); verifier `:117` (signature takes one worktree) |
| NB-1 (rules i-iii) | 8 Phase 1, step 1.3 rules (i), (ii), (iii) | Each rule now names the field it reads: (i) `worktree.shared_package_ids`; (ii) `row.orca.unsupervised` (classify) and `row.orca.terminal_state` (safe_to_close); (iii) `worktree.archive_states`, printed per step 1.5 | `scope-01-contract.md:64`; `scope-02-orca-recovery.md:95`; `05-orca-row-schema.md:20`, `:28`; `scope-02-orca-recovery.md:192` |
| NB-1 (print locations) | 8 Phase 1, step 1.5 section list | Retained problems gains "interrupted archive: <package id> in <worktree path>; marker kept, review" and "one package in two worktrees: <package id> in <path 1> and <path 2>"; Worktrees rows gain the safe-to-close worktree half and a Package state column ("<package id>: archive-blocked" / "<package id>: interrupted archive" / "-"); labelled plan decision, new design | Consolidated findings row NB-1; verifier `:49` break (2), `:118` (no print location in 1.5) |
| NB-1 (fixture) | 8 Phase 1, step 1.8 | Two-root fixture defined as two `WorktreeState` records sharing a `package_ids` entry, passed through `mark_shared_packages` | Consolidated findings row NB-1 (use the choice in 1.8) |
| NB-1 (tests) | 8 Phase 1, step 1.9 | Archive-blocked asserted in the Package state column; interrupted archive in that column and under Retained problems; pre-pass asserted to set `shared_package_ids` on both records (and on neither when ids differ), then both "removable: no" and the pair under Retained problems | Consolidated findings row NB-1 (use the choice in 1.9); verifier `:49` ("tests 1.9 still assert that those strings print") |
| NB-1 (3.1 consistency) | 3.1 "Context-only Dispatches" (411), "Package states" (412), "One package in two worktrees" (421) | 411 names the step 1.2 fields; 412 names the Package state column, `WorktreeState.archive_states` and step 1.5; 421 names the pre-pass `mark_shared_packages`, step 1.2 fields and step 1.5. Source quotes and [CODE-VERIFIED] tags untouched | Consolidated findings row NB-1 ("Keep 3.1 consistent with the chosen wording") |

## Verification after edits

- `grep -c CONTRADICTION` = 6, `grep -c NB-4` = 23 (unchanged from baseline); report still 1760 lines (edits extend existing table rows and bullets only).
- Term placement (grep -n): `mark_shared_packages` at 421, 1244, 1254, 1255; `shared_package_ids` at 1243, 1244, 1246, 1255; `archive_states` at 412, 1243, 1244, 1246; `unsupervised: bool` and `next_action` at 1243; `terminal_state` at 411, 1243, 1244; "Package state column" at 412, 1246, 1255; "one package in two worktrees:" at 1246. Every field rules (i)-(iii) and tests 1.9 read is now defined in step 1.2, and every string 1.9 asserts has a print location in step 1.5.
- No research or synthesis file edited (Read only). AO-01 to AO-18 text not removed; only references appended.

## Result

NB-1 RECOVERED. Open blocking findings after this pass: 0 (pending the cycle-2 review, the last one allowed).
