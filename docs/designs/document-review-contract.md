# Prose-first document-review contract

This November 2026 amendment supersedes the grading, resume defaults, boundary-row quota and repair accounting in `spec-panel-review-loop.md`. That older document is historical design evidence, not the current implementation contract. The authoritative instructions are the two active spec-panel command copies and `templates/documents/document-review-coordinator.md`.

Scope: document-review gates only. No new parser, runner or state engine. No migration of PR-submit/CI, reflect, adversarial, tasklist, PRD-generation or implement protocols. Installation and affected-workflow runs are separate decisions. Plugin wording outside the patch retains its pre-existing drift.

## Requirement and expected-result checklist

The following are frozen representative **specification scenarios**, not model-run results or a surrogate executable gate. Static tests pin their instructions and reject historical conflicting text. They cannot establish that an agent detects a defect, follows a budget, or refuses an unauthorized change.

| Case | Given | Required outcome / instruction |
|---|---|---|
| Evidenced zero | All applicable assurances established, no findings | Scoped PASS; no fabricated findings |
| Medium only | Concrete low-impact defect labelled MAJOR | Consequence-based Medium warning, no mandatory fix or restart |
| Severe defect | Confirmed wrong-tenant data exposure with trace | High/Critical blocker, FAIL with evidence |
| Misleading label | Severe data-loss consequence labelled MINOR | Regrade by consequence; label cannot clear blocker |
| Severe uncertainty | Credible security boundary concern, required evidence unavailable | INCOMPLETE; stop dependent step, do not pretend harmless or confirmed |
| Applicable guards | Threshold, sentinel or dependency behavior relevant | Cover relevant cases, no six-row minimum |
| No guards | No applicable conditional behavior in checked scope | Explicit no-guards and checked scope; no manufactured table |
| Deletion control | Proposed narrowing removes required authorization behavior | Do not accept as safe deletion; confirmed severe consequence blocks, unknown required assurance is INCOMPLETE |
| Prior PASS regression | Resolved finding fails again after edit | Retain id, source and resolution history; mark regressed |
| Missing report | Named report missing, empty, unreadable or ambiguous | INCOMPLETE, no fresh first review or false zero |
| Resume | Prior counters or header absent on ongoing loop | Preserve known identity and budget; reconcile missing evidence, never reset |
| Known exhaustion | Three reviews consumed, regardless of last verdict | No fourth review; results and unresolved decisions once |
| Incomplete review | Substantive review completes with unknown required predicate | Consume its slot, stop dependent step |
| Failed delivery | Review output unavailable | Only predeclared bounded delivery recovery, default zero; no free substantive review |
| Empty diff | Prior confirmed blockers and unchanged candidate | Blockers unresolved; review still consumes a slot |
| Prior ledger | Deferred, disputed, withdrawn or duplicate/unknown ids | Retain and explicitly account; missing rows do not mean zero |
| Uncertain mutation | Unclear phase completion or edit owner | Preserve last known identity/budget and stop pending reconciliation |
| Gross edits | Two findings share one added/deleted span | Report gross additions/deletions and net; count shared/uncertain attribution once |
| Scope control | New unrelated mechanism suggested during repair | No repair absent separate authorization; no unrelated scope growth |
| Final audit | F2 frozen, necessity audit suggests changes | Report only; no hidden F3; later repair needs bounded approval |
| Follow-ups | Genuine nonblocking findings remain | Top-level attended optional batched question once; unattended record only |

## Validation limits

`tests/skills/test_spec_panel_review_loop.py` preserves section layout, flags, canonical cap, evidence vocabulary, dual-surface lookup and routing checks, updating the obsolete scope pin. `tests/skills/test_document_review_contract.py` pins new instructions and rejects historical conflict strings. These are static contract regression checks only, not independent semantic demonstrations. No affected IronClaude/Orca/RF/Ponytail workflow is invoked by these tests. Live compliance, convergence and model-mediated severe-defect detection remain untested.

The existing `spec-panel-review-loop.md` force-install advice and legacy resets are superseded; this patch does not authorize installation or recommend overwriting customized files.

## Initial implementation checkpoint (2026-11-09)

Implemented independently of the affected orchestration workflows from baseline `933cf3a4f5fd3e4d8cce8f69c9168a2631574179`, following the GPT Dots roadmap in issue #346.

- P0: document-review scope and representative outcomes recorded above. Other protocol severity migration remains separate.
- P1/T1: command, coordinator and scoped pragmatic exception implemented. Static contract regressions and a separate human-readable semantic trace review cover the listed cases. These are not model-run measurements.
- P2/T2: differing/uncomparable kept-output-style warning implemented and exercised with temporary-home fixtures; existing and customized bytes, unknown files and settings are preserved. No global installation ran.
- P3/T3: narrow combined source/fixture checks performed. This is not an executed review/revision lifecycle or proof of convergence; model-mediated behavior remains untested.
- P4: no efficacy pilot run. Installation, merge and rollout have not occurred.

Independent review reported no confirmed High/Critical defect. A Medium scope mismatch between the pragmatic exception and the command was corrected by applying the exception to document review in every spec-panel mode, without changing other protocol defaults. Failed or missing evidence must not be hidden by calling the package a runtime PASS.
