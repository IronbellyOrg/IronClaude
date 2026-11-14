<!-- variant 2: reviewer 2 card, blind-calibrated confidence 0.86 (see reviewer-cards/reviewer-2-card-calibrated.yaml); copied verbatim from reviewer-cards/reviewer-2-card.md -->
<!-- Parent-persisted from the returned message of reflect-reviewer agent ad87516d8c0398eef (read-only agent, cannot write files). Content is the reviewer's own. The agent reported its model as "ChatGPT (exact model identifier unavailable)"; the recorded model is taken from the subagent transcript (see the audit log). Self-reported confidence 0.89. -->
# Reviewer card
reviewer: 2   persona: qa   model: ChatGPT (exact model identifier unavailable)
findings:
- id: R2-F1  severity: HIGH  tag: Grounded
  claim: Item 7.17 still requires PENDING records, empty decision fields and a halted task at Verification, although its successful resume fills those fields, resolves the records and clears the halt, so the optional-decision path cannot satisfy its literal completion checks.
  evidence:
    - ref: TL:1272
      quote: "An owner answer, approval or refusal, is recorded by filling the four lines of the step 1 decision file"
    - ref: TL:1272
      quote: "it sets `status: RESOLVED`, appends the decision to `### Execution Log`"
    - ref: TL:1274
      quote: "When the owner allowlist branch fires, confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines"
    - ref: TL:1275
      quote: "The facts file is written with no open HALT."
  fix: Split 7.17 Verification into first-halt and resolved-resume checks. Preserve the initial PENDING event as historical evidence; at completion require RESOLVED, filled owner-decision fields, the applicable approval follow-up or refusal record, and no open HALT. Item 7.17 is outside the present 85-label edit surface, so this needs a bounded authorization extension.
  verifier: Walk no-optional, resolved-refusal and resolved-approval cases; each completed case must satisfy Verification and Completion together, while a still-PENDING optional record must prevent completion.

- id: R2-F2  severity: HIGH  tag: Grounded
  claim: The decisions safety lens still rejects correctly approved optional allowlist changes because it unconditionally requires ten templates and bans run-current --json, despite 7.17 requiring the approved count, approved argv and a re-capture.
  evidence:
    - ref: TL:1271
      quote: "the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file"
    - ref: TL:1271
      quote: "the 7.16 forbidden list and its grep (item 7.16 Context and Verification) updated to allow the approved argv and a re-capture of it"
    - ref: TL:1321
      quote: "that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run"
    - ref: TL:1321
      quote: "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10"
    - ref: TL:1321
      quote: "Each breach is BLOCKING."
    - ref: DESIGN:559
      quote: "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)."
  fix: Make 7.24 check the approved post-7.17 allowlist and capture contract, retaining ten templates and the original forbidden argv when no approved change applies. Apply the same qualification to the reused R5 review inputs. Keep rejection of every unapproved addition.
  verifier: Walk unchanged/refused, approved-cursor and approved-run-current-json cases; the safety lens must PASS each correctly authorized case and FAIL an identical argv/count change without owner approval.

f_closure:
  F-01: partial - The requested count, optional-file expectations, twelve input lists and owner-row repair rules are corrected, but the optional branch still encounters the independent producer and safety-lens contradictions above; TL:1293, TL:1307, TL:1328, TL:1274, TL:1321.
  F-02: fixed - Item 13.1 copies the revised DESIGN wording and uses a correctly single-quoted fixed-string grep while retaining the placement check; TL:2265-2267.
  F-03: fixed - The substantive assignment, same-message, failure-exclusion and presentation-only clauses are embedded, and 11.4 explicitly requires presence checks rather than forbidden-word absence checks; TL:1210, TL:1980.
  F-04: fixed - The authorization section is written before the style edit, preserved before appended results, and checked against a named authority source rather than treated as independent evidence; TL:1210-1211, TL:1293.
  F-05: fixed - Command/skill defects have an in-place correction and checking-item rerun route; style defects explicitly halt rather than retry ticked 7.10; TL:1982.
  F-06: fixed - The exact replacement sentence occurs on 58 Context lines, the old literal remains only at pre-edit 7.10, and the replacement is true after successful 7.10; TL:1209, TL:1292.
  F-07: fixed - Both fixers specify four authority hashes before spawning and comparison after return, hashing only OQ-6 among decision records; TL:1363, TL:1391.
  F-08: fixed - The six-restatement grep has expected value 6 in the mechanical check and both fixer rechecks; TL:1293, TL:1363, TL:1391.
  F-09: fixed - The item explicitly overrides the generic Phase 7 branches and retains Blocked status until its Completion gate; TL:1210.
  F-10: fixed - Both affected items now assign report layout to GQ-35 and chat presentation only to GQ-63, consistent with the actual decision records; TL:1551, TL:1812.

self_audit: |
  Grounding root: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode.
  TL denotes the task file under .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/. DESIGN denotes docs/designs/orchestrator-mode.md.

  Read both briefs completely, the ten-finding basis and invariant probe, revision request/manifest/addendum, earlier QA reports, all six existing decision files, and the assigned Phase 7 consumers through 8.1. Read the specified 8.19, 10.5, 11.4 and 14.19 bodies and relevant baseline/design/style ranges. Searched task-wide decision references and both old/new anchor wordings. The two reported contradictions predate R2; neither is claimed as newly introduced by its 73 changed lines.

  Independently evaluated shell semantics without running commands:
  - Eight prerequisite records alone: required-file count 8; both optional checks SKIP.
  - Plus one or both resolved optional records: required-file count remains 8; each present optional status count is at least 1.
  - Missing or unresolved prerequisite: count falls below 8. Present unresolved optional: its count is 0 and fails.
  - The bracket glob excludes OQ-17/OQ-18. An unmatched prerequisite glob produces no matching filenames and count 0, not a false PASS.
  - The recommendation grep is judged per filename: OQ-1/OQ-8 expect 0; OQ-2 through OQ-7 and present optional files expect at least 1. Zero-match exit status is not itself a failure where expected content is 0.

  Traced owner-row counts through the panel: 7.13 correctly writes seven rows before optional records exist; 7.22/7.25 now require seven, eight or nine as applicable. Adding missing optional rows in 7.30/7.34 no longer contradicts the earlier seven-row check or inherently trips 7.33 regression/monotonicity. The 7.37-to-8.1 leg does not recount optional files; 8.1 checks eight explicit prerequisite names. All twelve revised input lists and 14.19 include optional decisions.

  Checked the authorization-heading grep, six-restatement expected value, fixed-string routing grep, hash comparison expectations, presence-only test pins and both named 11.4 repair routes. Did not elevate or repeat the existing MINOR notes without a demonstrated blocking case.

  Limits: no shell, tests, live captures, hash recomputation, installed activation or model-behaviour checks were performed. OQ-7/OQ-8 and optional records are future outputs, so their cases were traced from producing instructions, not observed executions. The task-wide reference search was complete; not every repeated downstream Context outside the assigned consumers was read in full. The optional-branch contradictions need correction before this is an end-to-end clean plan.
confidence: 0.89
