# Gap Resolution — Round 1

**Source:** `qa-research-gate-report.md` FAIL verdict (1 CRITICAL + 3 IMPORTANT + 4 MINOR).
**Resolution date:** 2026-05-01
**Status:** All 8 findings resolved by orchestrator decision (no new research needed; QA findings were decision-level + cosmetic).

---

## CRITICAL-1 — T-015/T-016 phase reclassification

**QA finding:** R3 placed T-015 (`extra_args` size invariant test) and T-016 (`tool_write_mode × BrokenPipe` cross-product test) in Phase 5 "Defer-with-tracking issues (file as GH issues, do NOT execute as code work)." This violates Phase 5's semantics — they are executable test additions, not deferral records.

**Resolution:** **Move T-015 and T-016 to Phase 2 — SHOULD (polish + mutation-kill tests).** Rationale:
- Both items are NEW-TEST additions to `tests/pipeline/test_process_stdin.py` (append).
- Both are mutation-kill / coverage-gap fixes, the same category as T-013 and T-014 already in Phase 2.
- LOW severity per refactor-plan but still in-PR work, matching Phase 2's "polish" framing.
- The user's BUILD_REQUEST omitted them, but Phase 2 is the correct home — adding them here doesn't violate the user's phase definitions, it completes the unaccounted bucket.

**Final Phase 2 contents** (now 7 items): P-011, P-013, T-012, T-013, T-014, T-015, T-016.

**Builder instruction:** Treat T-015 and T-016 as Phase 2 items. R3's `phase_assignment: 5-Deferred` for those two records is OVERRIDDEN — use `phase_assignment: 2-SHOULD`.

---

## IMPORTANT-2 — `[CODE-VERIFIED]` tag standardization

**QA finding:** R1 and R4 use prose verification verdicts ("VERIFIED at L<n>", "MATCHES verbatim") instead of the explicit `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tags the checklist requires. Semantically equivalent but cosmetically non-conformant.

**Resolution:** **Accepted as-is.** Semantic equivalence is sufficient for the builder's needs — the builder reads the actual verification verdicts (VERIFIED / DRIFT / MATCHES), not the literal tag strings. R1's drift table and R4's reconciliation tables are unambiguous about ground truth.

**Builder instruction:** Treat R1's "VERIFIED at L<n>" as `[CODE-VERIFIED]` and "DRIFT" as `[CODE-CONTRADICTED]`. No translation needed in the task file body — the items only need accurate file:line anchors, which R1 provides.

---

## IMPORTANT-3 — Phase 6 sizing

**QA finding:** R5 recommends Phase 6 contain 6 items (4 verification gates + aggregator + close-out frontmatter update). BUILD_REQUEST suggests 4 items.

**Resolution:** **Use the BUILD_REQUEST's 4 items + 1 close-out item = 5 total.** Rationale:
- The user explicitly listed 4 verification items (pytest, sync gates, pipx install, version check).
- MDTM Template 02 anti-orphaning rule (R5 cites C3/C4) requires the task-completion frontmatter update (status → 🟢 Done) to live INSIDE the final phase, not in a separate post-completion section. So Phase 6 needs at least one close-out item.
- The aggregator/synthesis item R5 proposes is over-engineering for this 18-item scope.

**Final Phase 6 contents** (5 items):
1. Run `uv run pytest tests/pipeline tests/cli_portify -v` — confirm no regressions vs the 1294/1294 baseline + 6 new tests pass.
2. Run `make sync-dev && make verify-sync` — sync clean; pre-existing rf-* / skill-creator drift is acceptable per task-header constraint.
3. Run `uv build && pipx install --force /config/workspace/IronClaude/dist/superclaude-*.whl` — wheel rebuild + pipx reinstall.
4. Verify `superclaude --version` returns "SuperClaude, version 4.2.0" — pipx install succeeded.
5. Update task frontmatter: `status: 🟢 Done`, set `completion_date`, append final summary to `## Task Log / Notes`.

---

## IMPORTANT-4 — R3 type-distribution arithmetic recount

**QA finding:** R3's Status Summary section visibly thrashes through multiple recount attempts. Final per-record YAML blocks are correct, but the summary table is messy.

**Resolution:** **Builder uses the 18 per-record YAML blocks as authoritative. Ignore R3's Status Summary aggregate counts.**

**Authoritative type distribution** (verified by counting per-record `type` fields):
- CODE-FIX: P-006, P-009, P-011, P-012, T-012 = 5
- NEW-TEST: P-007, P-008, P-013, T-013, T-014, T-015, T-016 = 7
- SPEC-AMENDMENT: P-010 = 1
- DEFERRED-WITH-OWNER: P-014, P-015, P-016 = 3 (these are tracking artifacts that get owners but are still in-tree work)
- Total: 16 items + 2 deferred records absorbed by Phase 5 = 18 P/T-NNN entries

**Authoritative owner distribution:**
- branch-author: P-006, P-007, P-009, P-011, P-012, P-013, P-014, P-015, T-012, T-013, T-014, T-015, T-016 = 13
- spec-keeper: P-008, P-010 = 2
- release-engineer: P-016 = 1 (executes; branch-author lands)
- maintainer: 0 (only D-FOLLOW items have maintainer ownership; they're in Phase 5)
- Total: 16 distinct owners (some shared)

---

## MINOR-5 — R1 frontmatter status

**QA finding:** R1 frontmatter says `Status: In Progress` but file is complete.

**Resolution:** Cosmetic. Builder ignores. Will be fixed inline below.

---

## MINOR-6 — P-007 required imports

**QA finding:** R3's P-007 record doesn't enumerate required imports for the new `tests/pipeline/test_prd_process_stdin.py` file.

**Resolution:** Builder uses R2's documented universal test style:
```python
from __future__ import annotations
import logging
import sys
from unittest.mock import patch
import pytest
from superclaude.cli.prd.process import PrdClaudeProcess  # or wherever the class lives
```
Plus any specific imports the test body needs (e.g., `os` for monkeypatching `os.write`).

**Builder instruction:** When constructing P-007's B2 item body, embed the import block above as part of the "After" content for the new file.

---

## MINOR-7 — `spec-keeper` persona

**QA finding:** R3 cites `spec-keeper` owner for P-008/P-010 but no `spec-keeper` agent exists in this repo's pipeline. Informational risk.

**Resolution:** **Treat `spec-keeper` as a role label, not an agent name.** The current branch author handles spec-keeper-tagged items in this delta — there is no separate handoff. The label is preserved for future workflow integration but doesn't trigger a real agent spawn.

**Builder instruction:** Items P-008 and P-010 should embed `Owner: spec-keeper (branch author handles in this delta)` to make this explicit.

---

## MINOR-8 — R4 SUPERSEDED count recount

**QA finding:** R4's prose visibly recounts 12 → 16 SUPERSEDED IDs. Final list correct but messy.

**Resolution:** **Final canonical count is 16 SUPERSEDED + 15 DEFER-TO-BEAT-2 = 31 in BEAT_2_BACKLOG.md.** Builder uses R4's "Builder-Usable Content for P-014" block verbatim.

---

## Inline cosmetic fixes applied by orchestrator

The orchestrator updated:
- `01-source-code-verification.md` Status frontmatter: `In Progress` → `Complete`
- `03-refactor-plan-content-lift.md` Phase 5 records for T-015 and T-016: `phase_assignment: 5-Deferred` → `phase_assignment: 2-SHOULD`

These are mechanical fixes — no semantic change.

---

## Net effect on builder

The builder receives:
- 5 research files (all complete, status normalized)
- This gap-resolution memo (used as authoritative for any conflict between research and orchestrator decisions)
- Final phase distribution: Phase 1=3, Phase 2=7, Phase 3=3, Phase 4=3, Phase 5=1 collapsed item (13 GH issues), Phase 6=5 = 22 checklist items total (or 19 + the Phase 5 collapse).

All 8 QA findings RESOLVED. Re-run gate not required because no new research files were produced — all resolutions are decision-level instructions to the builder.
