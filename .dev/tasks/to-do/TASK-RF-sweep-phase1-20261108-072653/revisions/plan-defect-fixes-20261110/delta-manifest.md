# Delta manifest: second bounded revision (plan-defect fixes F-01 to F-10)

Date: 2026-11-10. Baseline: `baseline/task-before-rev2.md` (sha256 f52e43a57ba6d3f3dc25120da937e1b7bf666782c732e5b042d2b938eb966855, 3020 lines). Edited plan sha256 (after all edits, before any later fix cycle): recorded in `build-state.json`.

Authority: owner answer "Fix the plan first" (see `BUILD-REQUEST.md`). Basis: `../chat-output-exception-20261109-133150/reflect/pre/adversarial/merged-verdict.yaml`.

Machine check: `qa/preservation_check.py` -> `qa/preservation-check.json` (355 headers identical, 137 completed items untouched, only Context/Action/Output/Verification/Completion-gate lines changed, only in the 85 allowed labels, ledger/item map/DESIGN hashes unchanged).

## Edits by finding (task-file lines after the edit; line count unchanged at 3020)

| Finding | Severity | Lines changed | What changed |
|---|---|---|---|
| F-01 | HIGH | 1293, 1299, 1306, 1307, 1313, 1320, 1327, 1328, 1334, 1341, 1348, 1363, 1369, 1376, 1391, 1397, 1404, 2572 | Decision count uses `OQ-[1-8]-*-decision.md` (expect 8); each existing OQ-17/OQ-18 file is checked separately (skip if absent); the `does NOT authorize adoption` grep has an expected value for OQ-17/OQ-18; the lens-input phrase now names the eight prerequisite records plus any OQ-17/OQ-18 record; 7.22 row count and 7.25 match rule allow one extra row per resolved optional decision; 14.19 names the optional decisions |
| F-02 | HIGH | 2265, 2267 | Item 13.1 quotes the DESIGN row R2 bullet (`runs /sc:sweep on every wake ... beside "The sweep."`), verified with `grep -nF`; placement check kept; ticked 5.2 untouched |
| F-03 | MEDIUM | 1210 | Item 7.10 embeds the addendum clauses (assignment must be explicit, table request or word coordinator does not assign, loaded skill/style do not assign, same-message case, exclusions incl. blockers/parse errors/missing output/unsuccessful Reads, "Formatting never authorizes advice the sweep skill prohibits", chat-presentation only, eligibility is a loaded-instruction contract not a detector); 11.4 pins check presence, never absence |
| F-04 | MEDIUM | 1210, 1211, 1293 | The step-7.10 result file gets a first-written `## Execution authorization (verbatim)` section; 7.20 checks it with a command (expect 1) and a read; executor-written quote is a record, not independent evidence |
| F-05 | LOW | 1982 | 11.4 repair routes: sweep.md/SKILL.md defect -> owning item 11.1/11.3 then re-run this item; style defect -> HALT with a named blocker, no retry of ticked 7.10 |
| F-06 | LOW | 58 Context lines (all labels in the table above except 7.10) | Stale "not an implemented exception" sentence replaced by the pre-7.10 wording; 7.10 keeps the original (count of the literal is now 1) |
| F-07 | LOW | 1363, 1391 | sha256 of addendum, both revision BUILD-REQUESTs and the OQ-6 record recorded before the fix agent spawns and re-checked after |
| F-08 | LOW | 1293, 1363, 1391 | `grep -c 'Except for the sweep chat-summary exception above,' src/superclaude/output-styles/pragmatic.md` (expect 6) |
| F-09 | LOW | 1210 | Pointer: this item's Branches replace the Phase 7 preamble Branches 1 and 2; task stays Blocked until the Completion gate |
| F-10 | LOW | 1551, 1812 | GQ-63 governs only the sweep skill chat reply; GQ-35 governs the report layout |

## A.10 fix cycle 1 (three further line-stable edits, after the first structural round failed)

| Finding | Lines | What changed |
|---|---|---|
| B2-1 | 1293 (7.20) | The execution-authorization quote is compared with the `## Authorization (direct, by the owner)` section of the R2 `BUILD-REQUEST.md`, or with a later dated owner message supplied with the fresh reports |
| B2-2 | 1363, 1391 (7.30, 7.34) | Full OQ-17 and OQ-18 paths written into both items |
| S16-1 | 1550 (8.19 Context) | Evidence-absence comment appended (sweep modules and tests do not exist at plan time) |

Also F-03 touched line 1980 (11.4 Action: pins check presence, never absence). Plan sha256 after cycle 1: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99 (see `build-state.json`). Changed lines: 73 in 64 labels.

## Not changed

Headers, titles, order, checkboxes, addresses, frontmatter (including the `reflect_pre` block), constraints 157-168, completed bodies (137), the Execution Log, the ledger, `item-map.tsv`, Q0 refs, owner decisions, research files, DESIGN, addendum, every earlier QA/reflect artifact, and every product, style, test, skill, installed or mirror source.

## Sign-off status

All R1 sign-offs (structural, alignment, qualitative, PRE) name the old plan hash and are history. Fresh checks against the edited plan are listed in `build-state.json`.
