# QA Report: R5 gate, completeness lens

**Topic:** OQ-1 / R5 (`worktree ps --agent-wait` allowed) applied to `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** fix-cycle / completeness review (fix_authorization: false)
**Fix cycle:** N/A (first review)

All evidence below was read from disk in this session. The producer's `r5-mechanical.md` was used only as a pointer; every claim was re-run.

## Findings

No BLOCKING or MAJOR finding.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `docs/designs/orchestrator-mode.md` (git status `??`, untracked, along with review-1 to review-3) | The DESIGN file is untracked. Outside this lens, and the `.dev/tasks/` staging rule does not cover `docs/designs/`. | None needed for this gate; stage it when the PR is built. |
| F2 | MINOR | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:132, 143, 301, 310, 323, 500, 504, 510, 562, 619` | The SPEC still says "never `--agent-wait`", "seven-verb" and "eight templates". D10 (DESIGN:837) records this as a deviation, so DESIGN is consistent. The SPEC text itself is stale until someone updates it. | Optional: add an R5 note to SPEC section 13 in a later change. |
| F3 | MINOR | `DESIGN:679` (WC-16) | Says `/sc:sweep` "does not ... run the `worktree ps --agent-wait` listing". True and consistent with "not called in Phase 1" (DESIGN:535-536); it is not a prohibition. | None. |

## Completeness evidence

- OQ-1 file (`.../phase-outputs/plans/OQ-1-agent-wait-decision.md`):
  - line 5 `status: RESOLVED`
  - line 19 "OPERATOR DECISION: allow."
  - line 20 chosen: allow `worktree ps --agent-wait` with and without `--json`
  - line 21 "Decided by: the owner, 2026-11-08."
  - line 22 source quotes: "Allow it, no conditions needed."
  - lines 26-30 state what stays in force: pin, version-scoped claim, `--include-remote` forbidden.
- Two templates, DESIGN:535 `("worktree", "ps", "--agent-wait")` and DESIGN:536 `("worktree", "ps", "--agent-wait", "--json")`. The tuple has 10 entries (lines 527-536), and line 537 reads `# 10 templates, 7 verbs (NFR-014)`.
- DESIGN:539 `FORBIDDEN_TOKENS = frozenset({"--include-remote"})`: one token.
- DESIGN:837 is D10. D1 to D10 are all present as row ids (828-837). DESIGN:839 is `Total: 10 deviations.` and is the only `Total: N deviations` line. D10's SPEC line list (132, 143, 310, 323, 500, 504, 510, 562, 619) matches the SPEC lines where `agent-wait` occurs: 132 143 310 323 500 504 510 562 619.
- DESIGN:221 (section 4 extension-point rule): "a new template in `ALLOWED_ORCA` (only after a capture or a recorded owner decision (R5, 2026-11-08), and never a write verb)".
- DESIGN:66 (GQ-109 row): "`--include-remote` is the only forbidden token ... `worktree ps --agent-wait` is allowed (R5, owner 2026-11-08)".
- DESIGN:555 (7.3 M3 note): "since R5 (owner 2026-11-08), ten templates (NFR-014)".
- Section 11 (DESIGN:759): "exact-set pin of the ten templates" and "a positive case that both `worktree ps --agent-wait` templates (with and without `--json`) are accepted".
- Section 12 (DESIGN:815): `NFR-014 | ALLOWED_ORCA ten templates (7.3)`.
- Section 15.1 (DESIGN:895): ten templates; step 1.0a issues only templates 1 to 8; `--agent-wait` "is allowed by R5 but is not run in step 1.0a". Its negative list no longer names `--agent-wait`, only `--include-remote`. DESIGN:851 also reads "templates 1 to 8 of the ten".
- Diagram: DESIGN:181 `ALLOWED_ORCA (10)` and DESIGN:196 `10 read templates`.
- R5 row: DESIGN:1047, inside `### Fix cycle 3` (starts at line 1037). It says RESOLVED, quotes the owner, lists the templates added, the token removed and D10, and says the pin and the version-scoped claim (Orca 1.4.245) are kept.
- No stale text: `eight`/`8 templates` appears only in the D10 row (837), where it says "ten, not eight". No "nine deviations" or "9 deviations". No em dash (count 0). No TODO or TBD. `Total: 23 open items.` is unchanged (DESIGN:1015).
- WORKER-CONTRACT line 110:
  - `git diff -- src/superclaude/core/WORKER-CONTRACT.md` gives 0 lines.
  - `git diff --cached --stat` is empty.
  - Line 110 on disk equals `HEAD` line 110 (diff of the two printed `SAME110`).
  - The line still reads "one prompt-wait listing (`worktree ps --agent-wait`)".
- research/07 line 117: "one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11)". It confirms the sweep paragraph (`:110`) runs the listing, so the R5 premise holds.
- SPEC section 13 (INV-005 sign-off): lines 487-504 give condition 1, with item 5 "`worktree ps` (never with `--agent-wait`)", and line 504 "negative tests for `--include-remote` and `--agent-wait` (NFR-014)". NFR-014 is at line 143. D10 names exactly these.
- r5-mechanical.md (90 lines) reports 12 of 12 PASS. Its commands 5 to 10 match what I re-ran.
- The gate folder `qa/r5/` existed and was empty before this report.

## Checks

| id | Check | Result |
|---|---|---|
| C1 | OQ-1 file `status: RESOLVED` | PASS |
| C2 | OQ-1 records the allow decision (with and without `--json`) | PASS |
| C3 | OQ-1 names the owner as decider (2026-11-08) | PASS |
| C4 | OQ-1 source quotes "Allow it, no conditions needed." | PASS |
| C5 | Two `worktree ps --agent-wait` templates exist in 7.3 (with and without `--json`) | PASS |
| C6 | `FORBIDDEN_TOKENS` holds one token (`--include-remote`) | PASS |
| C7 | D10 exists, D1 to D10 are all present, and `Total: 10 deviations.` exists once | PASS |
| C8 | D10 SPEC line list matches the SPEC lines carrying `agent-wait` | PASS |
| C9 | Section 4 extension-point rule (line 221) names the recorded owner decision (R5, 2026-11-08) | PASS |
| C10 | Section 7.3 count comments say 10 templates and 7 verbs; the M3 note is reworded | PASS |
| C11 | Section 11 reworded: ten-template pin plus a positive `--agent-wait` case | PASS |
| C12 | Section 12 NFR-014 row says ten templates | PASS |
| C13 | Section 15.1 reworded (ten templates, templates 1 to 8 run, `--agent-wait` allowed but not run) | PASS |
| C14 | GQ-109 row reworded | PASS |
| C15 | `### Fix cycle 3` R5 row exists (line 1047) | PASS |
| C16 | No stale "eight templates" or "9 deviations" text; diagram labels say 10 | PASS |
| C17 | `git diff -- src/superclaude/core/WORKER-CONTRACT.md` is empty and line 110 equals `HEAD` | PASS |
| C18 | research/07 line 117 and WORKER-CONTRACT line 110 agree that the sweep runs the listing | PASS |
| C19 | SPEC section 13 INV-005 sign-off and NFR-014 (line 143) are what D10 and R5 cite | PASS |
| C20 | No em dash, no TODO or TBD, and the open-item total (23) is unchanged | PASS |

Confidence: Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 7 | Grep: 4 | Glob: 0 | Bash: 5 (read-only `grep`, `sed -n`, `diff`, `git diff`, `git status`, `git log`, `ls`)

Verdict: PASS
Blocking count: 0
