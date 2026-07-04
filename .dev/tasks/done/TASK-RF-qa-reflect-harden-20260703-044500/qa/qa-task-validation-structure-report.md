# QA Report — Task Integrity (Structure + Phase Ordering Lens)

**Topic:** Additively harden RF QA + /sc:reflect vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Items Reviewed (Structure + Phase-Ordering Lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | `uv run python yaml.safe_load` parsed clean. Present + non-empty: id(L2), title(L3), status(L6 "🟡 To Do"), created_date(L9)/updated_date(L10), type(L7), template(L62 "02"), start_commit(L20 `46a787dac39c...`), executor_model_class(L22 "sonnet"), spec_path(L18), reflect_post(L31 ""). reflect_post protocol room-comment at L163 ("DO NOT hand-author…the wrapper writes it"). `tracks` ABSENT — see Issue #5 (N/A for Template 02, noted). |
| 2 | Mandatory Template-02 sections present | PASS | Task Overview(L67), Key Objectives(L86), Prerequisites & Dependencies(L97), Execution Context(L114: References/Source Areas/Key Constraints/Handoff/Frontmatter-Protocol), 5 phases + 3 gates + 2 post-gates, Task Log / Notes(L460) at bottom. |
| 3 | Phase dependencies logical; edit→test→validate; sync-dev before brief-guard tests; per-phase QA | PASS | Linear: P1 setup → P2 FX3/FX5 tests → Gate A → P3 FX7 → Gate B → P4 briefs → Gate C → P5 full-suite → Post(final M3 → M4 fidelity → reflect → Done). Step 4.4 & 5.1 run `make sync-dev` BEFORE the audit/tripwire tests (correct: `.claude/` mirror byte-parity tests need regen). Each impl phase followed by its own 5/6-agent gate. |
| 4 | research/edit → test → validate progression | PASS | Every phase: L1 Discovery inventory → L2 Build → L3 Test(pytest) → L3 lint. e.g. P2: 2.1 inventory→2.2 author FX3→2.3 run→2.4 inventory FX5→2.5/2.6 differentials→2.7 collector→2.8 suite→2.9 ruff. |
| 5 | Task-completion items inside final phase; POST reflect penultimate, Done last | PASS (structure) / see Issue #3 | PC.11 (reflect wrapper) is penultimate checkbox, PC.12 (status→Done) is the LAST checkbox (L458, no checkbox after). Not orphaned. BUT both live under the "M4 Fidelity Gate" header (Issue #3, header-scope nit). |
| 6 | Task Log section at bottom | PASS | `## Task Log / Notes 📋` at L460, after all executable content. |
| 7 | Item count (72) reasonable for scope | PASS | `grep -c '^- \[ \]'` = 72. Per-section: P1=3, P2=9, GateA=9, P3=6, GateB=9, P4=5, GateC=9, P5=3, Post-actions=2, FinalM3=10, M4=7 → sums to 72. Reasonable for 5 fixes + tests + 4 QA gates + M4 fidelity + reflect. |
| 8 | Open Questions / deferred scope documented | PASS | Overview L81-84 lists FX4/FX6/FX8/FX9 exclusions; Open Questions L524-530 documents FX2-surface (RESOLVED Branch A), FX7 exemption fail-safe HALT, FX5 residual risk, deviation-taxonomy zero-tests. |
| 9 | QA gates follow M3 (lens) + M4 (fidelity) | PASS | Gate A/B/C = M3 lens, 5 agents (2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst) each = GA.2/GB.2/GC.2 spawn exactly 5 checkboxes. Final M3 = 6 agents (PC.4 = 6 spawns). M4 fidelity = 3 agents (PC.8 = 3 spawns: 2 fidelity + 1 cross-source). All floors match headers. |
| 10 | TB-Add-1: no TBD/TODO/FIXME; no title-only items | PASS | grep TBD/TODO/FIXME hits ONLY 2 items (2.2, 3.2) where the text INSTRUCTS "contains no placeholder/TODO text" / "no placeholder/TODO remains" — directives, not placeholders. Task Log template `[YYYY-MM-DD]` markers are in the non-checklist scaffold. No title-only item — every item carries context+action+output+"ensuring"+blocker-log+completion gate. |
| 11 | TB-Add-3: blocked items reference blocking Open Question by index | PASS (vacuous) | All Open Questions (L524-530) are RESOLVED design decisions / documented residual risk, not active blockers. No checklist item is blocked-by an open question. Check inactive. |
| 12 | TB-Add-4: item-to-item deps form a DAG | PASS | Flow is linear; only loops are bounded fix-cycles (GA.3-GA.5 max 2, PC.5-PC.7 max 3, PC.9 max 3) — explicit retry ceilings, not data-dependency cycles. No item depends on a later item. |
| 13 | TB-Add-5 / item-10: XL / multi-file items split or justified | **FAIL** | Issue #1 — Step 3.3 (L283) modifies THREE source files (models.py + contract.py + runner.py) in one item; Step 3.2 (L279) makes 4 distinct edits (a/b/c/d) to ensemble.py + call-site threading; Step 2.7 (L231) spans conftest.py + a new coverage module; Step 3.4 (L287) spans 3 test files + fixtures. Multi-file single items exceed item-10 atomicity. |
| 14 | TB-Add-6: uniform Verify/Acceptance form | PASS | All 72 items use the RF self-contained idiom uniformly (embedded "…ensuring X…" verification clause + "If unable…log the specific blocker…" + "Once done, mark this item as complete."). |
| 15 | TB-Add-7: Source areas reappear in items; block has NO file:line | **PARTIAL FAIL** | Positive half PASSES: all 6 named Source Areas (contract_setup pkg, tests/pr_submit, cli/reflect, rf-qa-qualitative, reflect-reviewer, deviation-taxonomy) reappear in ≥1 item Context. Negative half FAILS: the `## Execution Context` block's `### References` subsection (R-002..R-007, L118-123) is saturated with `file.py:NN` citations (questions.py:14-38, ensemble.py:492-568, contract.py:288, candidate.py:47/360, etc.). TB-Add-7 spot-check `grep -cE '\.py:[0-9]+'` on the block > 0. See Issue #2. |
| 16 | TB-Add-8: per-item Context referencing code surface has file:line or evidence-absence | PASS | Items referencing code surfaces embed file:line heavily (2.1→questions.py L14-38/L52-61/L64-76; 3.1→ensemble.py L492-568; 4.1→rf-qa-qualitative :670-676/:639/:660). New-file items cite the source symbols being introspected. Strong body-level evidence binding. |
| — | POST reflect wrapper form (spawn special check) | PASS | PC.11 (L454) = FLAT wrapper: `superclaude reflect run <taskfile> --depth deep --fix --promote` behind `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then …exit 0; fi` recursion guard, exit-code-consumed (0→proceed; 10/11/2→FAIL+Blocked). Uses NO --base, NO --spec, NO --reflect, NO range, NO --max-turns, NO /sc:task, NO subagent/nesting token. NOT a self-run reflect-subagent form, NOT a human-HALT form. WELL-FORMED. |

---

## Overall Verdict: FAIL (near-pass — all issues MINOR/IMPORTANT, none CRITICAL)

The phase **structure and ordering proper are sound** — dependency ordering, edit→test→validate progression, sync-dev-before-mirror-tests, anti-orphaning (reflect penultimate / Done last), item count (72), gate agent floors, YAML frontmatter, and the flat POST-reflect wrapper form all verify clean. The FAIL is driven by two named Structural-Gate-Addition checks (TB-Add-5/item-10 atomicity, TB-Add-7 Execution-Context hygiene) plus cosmetic nits. None block correct execution; remediation is mechanical.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 3.3 (L283); also 3.2/L279, 2.7/L231, 3.4/L287 | **Atomicity (item 10 / TB-Add-5).** Step 3.3 edits three distinct source files (models.py, contract.py `_make_result`, runner.py `_build_reflect_post_value`+`write_sidecar`) in a single checklist item. 3.2 bundles 4 distinct ensemble.py edits + call-site threading; 2.7 spans conftest.py + a new test module; 3.4 spans 3 test files + fixtures. Multiple-file single items exceed the item-10 "single atomic change" bar even though each is self-contained. | Split 3.3 into 3.3a (models.py add defaulted fields), 3.3b (contract.py `_make_result` populate via `c.get`), 3.3c (runner.py writeback + sidecar append). Optionally split 2.7 and 3.2. Each sub-item stays additive + ordered. |
| 2 | MINOR | `## Execution Context` → `### References` (L116-124) | **TB-Add-7 negative half.** The Execution Context block embeds a dense `file.py:NN` citation ledger (R-002..R-007). TB-Add-7 requires the block itself carry NO file:line — per-item Context is the correct venue (and item bodies already mirror these anchors, so the ledger is redundant). NOTE: the `### References` ledger is an established RF Template-02 convention, so this is a convention-vs-strict-rule tension, not a correctness defect. | Either (a) relocate the R-xxx file:line anchors so they live only in per-item Contexts (which already carry them), leaving References as prose pointers to `research/NN.md §X`; or (b) if the RF `### References` ledger is an accepted local exception to TB-Add-7, document that exception so the spot-check is knowingly waived. |
| 3 | MINOR | L434 header vs PC.10/PC.11/PC.12 (L448-458) | **Header-scope inaccuracy.** Task Summary (PC.10), POST-reflect wrapper (PC.11), and status→Done (PC.12) are placed UNDER the `### Post-Completion SOURCE-DOCUMENT FIDELITY Gate (M4…)` heading, but they are not part of the M4 fidelity gate (which logically ends at PC.9). The header misrepresents its trailing contents. Not orphaning — they are inside the last section — but the label is wrong. | Add a `### Finalization (Task Summary → POST reflect → Done)` subheading before PC.10 so the M4-gate header scopes only PC.8-PC.9. |
| 4 | MINOR | Step 4.5 (L347) | **Misplaced/dead command.** Step 4.5 (markdown-lint of the three edited briefs, a Phase-4 brief-editing step) opens with `uv run ruff format --check src/superclaude/cli/reflect/*.py 2>&1; true` "as a no-op guard." cli/reflect Python was NOT edited in Phase 4 (that was Phase 3), so this Python ruff check is out-of-place in the markdown step and the `; true` masks its result — a confusing dead command. | Remove the `ruff format --check …cli/reflect/*.py; true` no-op; keep Step 4.5 scoped to the markdown-lint of the three edited briefs only. |
| 5 | MINOR | Frontmatter (L1-63) | **`tracks` field absent.** The canonical 27-point task-integrity checklist item-1 names `tracks` as mandatory. This task is Template 02 MDTM, whose schema does not use `tracks` (a sprint-tasklist field), so this is almost certainly N/A — flagged for completeness only. | Confirm Template 02 does not require `tracks`; if the schema omits it, no action. Not blocking. |
| 6 | MINOR | Step PC.11 (L454) | **`git add -A` breadth.** PC.11 runs `git add -A` before the reflect wrapper. The item DOES guard-unstage `.claude/{agents,skills}` mirrors, but `-A` in a shared-index worktree also stages the entire `phase-outputs/` + `qa/` report set and any unrelated `.dev/` artifact into the wrapper's diff. The wrapper only needs the FX change set. | Consider scoping the stage to the FX surfaces (`git add tests/pr_submit src/superclaude/cli/reflect src/superclaude/agents src/superclaude/skills`) rather than `-A`; keep the `.claude/` unstage guard. Low risk given the guard. |

## Summary
- Checks passed: 14 / 16 lens checks (+ POST-reflect special check PASS)
- Checks failed: 2 (item-10/TB-Add-5 atomicity; TB-Add-7 Execution-Context file:line)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Actions Taken
None — `fix_authorization: false`. All findings documented above for the orchestrator to route.

## Recommendations
- Before execution, split Step 3.3 (3-file item) into 3 atomic sub-items (Issue #1, IMPORTANT). This is the only finding with real executor-ergonomics impact.
- Resolve the TB-Add-7 References-ledger tension (Issue #2) — relocate anchors to item bodies OR document the RF `### References` exception.
- Cosmetic: relabel the M4-gate header trailing items (Issue #3), drop the dead ruff no-op in Step 4.5 (Issue #4).
- No CRITICAL structural defect exists. Phase ordering, dependency graph, anti-orphaning, agent floors, frontmatter, and the flat POST-reflect wrapper are all correct.

## Confidence Gate
- **Confidence:** "Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 5 | Grep: 3 | Glob: 0 | Bash: 3"
- No UNCHECKED items. No UNVERIFIABLE items. Every lens check was verified by direct Read of the relevant lines or a targeted grep/bash aggregation covering multiple checks at once (per-section counts, YAML parse, Execution-Context ref-scan) — no padding.

## QA Complete
