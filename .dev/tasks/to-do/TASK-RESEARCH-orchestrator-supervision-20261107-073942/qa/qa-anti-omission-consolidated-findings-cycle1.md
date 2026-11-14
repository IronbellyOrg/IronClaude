# Consolidated findings: Phase 6 anti-omission gate, cycle 1 (fix pass 2, the last one)

- Sources: `qa/qa-anti-omission-verification.md` (structural, PASS, |F_1| = 0, 5 MINOR notes), `qa/qa-anti-omission-verification-qualitative.md` (qualitative, FAIL, 1 new blocking finding NB-1, MINOR notes M-1 to M-6)
- Previous: |F_0| = 18 (`qa/qa-anti-omission-consolidated-findings.md`), fix log `qa/qa-anti-omission-fix-log.md`. Both verifiers: AO-01 to AO-18 all RECOVERED, none JUSTIFIED, none OPEN.
- |F_1| = 1
- Gate status: FAIL
- Regression: none (cycle 0 had no verification; no item had PASS before)
- Monotonicity: |F_1| = 1 < |F_0| = 18, no halt
- Merge rule: union of the open and new blocking findings of both verifiers. The structural verifier found none; the qualitative verifier found NB-1, introduced by fix pass 1. Line numbers are as of the 1760-line report; locate each spot by its quoted text.
- Constraints for the fix agent: keep the NB-4 exception record (about `:13`, `:1644`) and both [CONTRADICTION] markers with their resolutions (`grep -c CONTRADICTION` stays 6, `grep -c NB-4` stays 23). Do not reopen AO-01 to AO-18 or findings resolved by the lens and fidelity gates. Label every new field or signature as "plan decision, new design". Targeted Edits only.

## Blocking findings

| ID | Severity | Location | Issue | Required fix | Disposition |
|---|---|---|---|---|---|
| NB-1 | IMPORTANT | Step 1.2 (about `:1243`) vs step 1.3 rules (i)-(iii) (about `:1244`), step 1.5 (about `:1246`) and step 1.9 tests (about `:1255`); 3.1 "One package in two worktrees" (about `:421`), "Context-only Dispatches" (about `:411`), "Package states" (about `:412`) | Fix pass 1 added step 1.3 rules (i) one package in two worktrees, (ii) context-only Dispatches (`unsupervised`, terminal state `retained`) and (iii) archive-blocked / `.archiving` packages, plus step 1.9 tests, but did not extend the step 1.2 data model or the step 1.5 renderer they depend on. `safe_to_close(row: SessionRow, worktree: WorktreeState \| None)` sees one worktree and `WorktreeState` carries no package ids, so rule (i) cannot be computed; `WorktreeState` has no archive-state field and step 1.5 names no place where "archive-blocked", "interrupted archive" or the two-worktree pair print; `OrcaObservation` has no `unsupervised` or terminal-state field for rule (ii). The step 1.9 tests cannot pass against the specified types and renderer. | In step 1.2 add the fields the rules read, labelled plan decision, new design: `WorktreeState.package_ids: tuple[str, ...]`, `WorktreeState.archive_state: str \| None` ("archive-blocked" / "interrupted archive" / None), `OrcaObservation.unsupervised: bool \| None` and `OrcaObservation.terminal_state: str \| None` (used for the safe-to-close half only, never to set the class). In step 1.3 state that the two-worktree check is a pre-pass over all `WorktreeState` records before `safe_to_close` (or widen the signature to take the full worktree list; pick one and use it in 1.3, 1.8 and 1.9). In step 1.5 name where the package state prints (a Worktrees column or a Retained problems line) and add "interrupted archive" and the two-worktree pair to the Retained problems rendering. Keep 3.1 consistent with the chosen wording. | RECOVER |

## MINOR notes (not fixed, not rechecked)

- Structural verifier: 5 MINOR notes in `qa/qa-anti-omission-verification.md` (header does not print `scope.source`; worker-show verdict outranks the worker-list row not restated; weak-signal list not given as one list; no row-total check against `page.total`; coordinator placement map not used to join Tasks to worktrees).
- Qualitative verifier: M-1 to M-6 in `qa/qa-anti-omission-verification-qualitative.md`. M-2 is useful for the plan stage: rule (iv) (peer ownership) has no fixture or test although fix log row 33 says so, and `linked: true` comes from `reference find`, which is not on the step 1.4 allowlist, so in Phase 1 every peer Owner prints "unknown".

## Cycle control

- Anti-omission gate, own counter. Cycle 0: |F_0| = 18, FAIL, fix pass 1. Cycle 1: |F_1| = 1, FAIL, fix pass 2 (last). A failing cycle-2 review HALTs.
