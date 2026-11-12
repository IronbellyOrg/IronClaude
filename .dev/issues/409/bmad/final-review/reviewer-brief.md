# Shared brief for step-5 reviewers (orca-observer)

Project: the Orca read-only terminal observer dashboard (IronClaude issue 409), slug `orca-observer`.
Repo root (Coder worktree): /home/coder/workspaces/worktrees/Coder/dashboard-bmad  (call it ROOT)

## Artifacts (all under ROOT)
- SPEC: _bmad-output/specs/spec-orca-observer/ : SPEC.md, acceptance-tests.md, adapter-contract.md, owner-decisions-and-risks.md, release-gates.md, rendering-rules.md, snapshot-export-schema.md, stack.md, unverified-register.md, write-back-future-stage.md (ARCHITECTURE-SPINE.md there is an identical copy of the architecture spine; review it only as ARCH)
- PRD: _bmad-output/planning-artifacts/orca-observer/prd.md, addendum.md
- UX: _bmad-output/planning-artifacts/orca-observer/ux-designs/ux-orca-observer-2026-11-08/DESIGN.md, EXPERIENCE.md (fix-log.md is the change log, context only)
- ARCH: _bmad-output/planning-artifacts/orca-observer/architecture/ARCHITECTURE-SPINE.md (AD-1..AD-20, CD-1..CD-16)

## Sources of truth (rank: issue body and owner decisions > snapshot contract > spec > PRD > UX > ARCH; a derivative never overrides its source)
- Issue body: ROOT/_bmad-output/planning-artifacts/orca-observer/final-review/inputs/issue-409-body.md
- Owner decisions: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/owner-decisions-20261108.md
- Snapshot contract fields: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/architecture-options.md

## Owner decisions that BIND (never flag these as defects; flag any document that contradicts them)
1. Staged releases: R1 = Signal Bridge's worker ledger on the verified `worker-list` source, carrying Attention Ledger's "question source UNVERIFIED" notice; Attention Ledger after the QUESTION-OBSERVATION gate; Decision Desk behind the QUESTION-LINK gate.
2. Stack for R1: Python + Rich, a `superclaude observe` subcommand in IronClaude; R1 also writes a versioned, additive-only JSON snapshot with a schema test for a later read-only Go screen in TUIBBS; the key-reader spike is the first task (Textual switch rule).
3. Read-only for R1; write-back from the BBS is a FUTURE stage needing an explicit boundary change and an amendment of TUIBBS rule FR-X-13.
4. TUIBBS (AGPL-3.0, private) is background only; licence opinion open.
5. Unknown is never zero or false. Keep every evidence label; unchecked things are UNVERIFIED; never invent an Orca API field.
6. Open owner questions (OQ-1..15, UX-OQ-1..8) are NOT defects just for being open. Do not resolve them.

## Rules for you
- READ ONLY. Never edit any artifact or source. Write exactly one output file: the path given in your task. No git, no gh writes, no network except reading local files.
- Read files in ranges of at most 150 lines (grep -n headings first). Never open images or binaries.
- Cite every finding as `relative/path:line` (relative to ROOT, or absolute for IronClaude files). Cite the source line when you claim a contradiction.
- Assume defects exist. Prefer real defects (wrong behaviour, false claim, contradiction with a source or another document, missing required content, security/data-loss risk) over style nits, but list both.
- For each finding give `proposed_grade`: BLOCKING (wrong behaviour, false claim, missing required deliverable, contradiction between documents or with a source, security/data-loss risk) or MINOR (wording, style, nit, citation format, moved line number on a true claim).
- Output file format: a JSON object `{"reviewer": "...", "artifact": "...", "verdict": "PASS|FAIL", "self_audit": "what you checked (required if zero BLOCKING)", "findings": [{"id": "...", "location": "path:line", "other_side": "path:line or null", "finding": "one or two sentences", "evidence": "short quote(s) <= 30 words", "proposed_grade": "BLOCKING|MINOR", "suggested_fix": "one sentence"}]}`. verdict FAIL if any BLOCKING.
- Your final reply (and nothing else): the output path, then a 3-line verdict (verdict; counts BLOCKING/MINOR; the single worst finding). Never paste findings.
