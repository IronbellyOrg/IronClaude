# QA Report: R5 gate, cycle 1 verification (rf-qa-qualitative, fix-cycle)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after the cycle-1 fix of R5-F1
**Date:** 2026-11-09
**Phase:** fix-cycle
**Fix cycle:** 1 (second review of the gate)
**fix_authorization:** false. No file edited except this report.

Method: I read the consolidated findings, the fix log, the ledger and all nine cycle-0 lens reports, then re-checked each claim against the files on disk now: DESIGN (1047 lines, `wc -l`), OQ-1 record, `r5-mechanical.md` (regenerated 2026-11-09T00:22:03Z, 1047 lines), `WORKER-CONTRACT.md` (95-135 and line 110), research/07, SPEC (lines 132, 143, 144, 477-515 and a grep of `agent-wait`), the task file. I did not trust the fix log. The DESIGN is untracked, so I compared the three edited lines (555, 759, 1047) by reading them and compared headings against `artifacts/design-base.md`. No `orca` command and no network call.

## Totals held (re-run now)

| Item | Required | Found on disk |
|---|---|---|
| `Total: 10 deviations.` | 1 hit | `docs/designs/orchestrator-mode.md:839`; D1 to D10 rows at 828-837 |
| `Total: 23 open items.` | 1 hit | `docs/designs/orchestrator-mode.md:1015`; 23 numbered rows in 991-1013 |
| Em dash | 0 | `grep -c` gives 0 (en dash also 0) |
| TODO or TBD | none | `grep -nwE 'TODO\|TBD\|FIXME'` prints nothing (exit 1) |
| `FORBIDDEN_TOKENS` | only `--include-remote` | `docs/designs/orchestrator-mode.md:539` |
| `ALLOWED_ORCA` templates | 10 | tuples at `:527-536`; comment `# 10 templates, 7 verbs (NFR-014)` at `:537` |
| Line count | 1047 | `wc -l` gives 1047 |

## Finding re-check

### R5-F1 (MAJOR): RESOLVED

The cycle-0 defect: "not called in Phase 1" for the two `--agent-wait` templates had no test (`:535-536`, `:679`, `:833`, `:895`), so a `probes.py` developer could add a `worktree ps --agent-wait` call with every listed test green.

Now on disk:

- `docs/designs/orchestrator-mode.md:555` (section 7.3, M3 paragraph): "The NFR-003 full-sweep recording test asserts zero argv for both, and also for both `worktree ps --agent-wait` templates, so all four templates marked "not called in Phase 1" are never issued by a sweep. That wording is a design statement; R5 only allowed the two `--agent-wait` templates."
- `docs/designs/orchestrator-mode.md:759` (section 11, `tests/sweep/test_probes_allowlist.py` row): "zero argv for all four templates marked "not called in Phase 1" (`worktree list`, `worktree current` and both `worktree ps --agent-wait` forms, with and without `--json`)". The same row still holds the exact-set pin "of the ten templates" and the positive case that both `--agent-wait` templates are accepted. The negative list (`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `run-list`) is unchanged.
- `docs/designs/orchestrator-mode.md:1047` (R5 row): the owner portion ends "...the allowlist pin and the version-scoped claim (Orca 1.4.245) are kept." and a separate sentence "Gate fixes: ..." records the new assertion. The owner quote and the owner's decision are not extended.

The four templates marked "not called in Phase 1" in the code block are exactly `:533`, `:534`, `:535`, `:536`, so "all four" is correct. The fix is the smallest fix AC A1 and the other lenses proposed. Rows 759 and 1047 still have 4 unescaped pipes (awk); row 759 has the same cell count as rows 774-820.

No BLOCKING or MAJOR finding is open.

## Reader pass: the developer of `probes.py` and its tests

Passages read: the 7.3 paragraph (`:555`), the section 11 `test_probes_allowlist.py` row (`:759`), and the R5 row (`:1047`) in the context of `:523-551`.

What the reader can now do without guessing: write the recording assertion (the count of recorded argv equal to each of four templates is zero), keep the positive acceptance test for the two `--agent-wait` forms (call the validator directly, as for the other positive cases), and keep the exact-set pin at ten. The text does not say the owner decided "not called"; it says the opposite in so many words ("a design statement; R5 only allowed the two"). I found no overclaim of the owner decision.

Where the reader still has small gaps (all MINOR; none blocks work; recorded as notes):

- V-N1 (MINOR, wording). `:555` says the four templates "are never issued by a sweep". Master's coordinator sweep (`src/superclaude/core/WORKER-CONTRACT.md:110`) does issue `worktree ps --agent-wait`. Elsewhere the DESIGN says `/sc:sweep` for the command and "The sweep." for master's (`:674`, `:679`). A coordinator-minded reader could read "a sweep" as master's. The surrounding words ("full-sweep recording test", `probes.py`) make `/sc:sweep` the likely reading. Smallest fix: write "never issued by `/sc:sweep`".
- V-N2 (MINOR, placement). The two new sentences sit inside a paragraph titled "Decision on `worktree list` and `worktree current` (M3)". Its last sentence, "The decision is revisited after step 1.0a only if `worktree ps --json` lacks the worktree path field", still means the list/current decision, but it now follows agent-wait text. Smallest fix: start it "The list/current decision is revisited...".
- V-N3 (MINOR, completeness). `:288` ("`worktree list` and `worktree current` are not called in Phase 1") and the section 4 counts table row `:342` ("0 in Phase 1 | NFR-003 recording test") name only two templates, while `:759` now pins zero for four. Both lines stay true as written; the fix log records the choice not to edit `:342`. A reader of section 4 does not learn that the `--agent-wait` pair also has a pinned zero. Smallest fix: add the pair to `:342`.
- V-N4 (MINOR, form). `:1047` now ends "...for all four templates (7.3, 11) (2.2, 4, 7.3, 11, 12, 13, 15.1)": two parenthetical lists in one cell, the first a subset of the second. The cell count and the closing section list are intact. Smallest fix: drop "(7.3, 11)".

The earlier notes R5-F2 to R5-F23 (for example "each template" at `:914` and `:1000`, the `R5` label overlap, SPEC line 301 missing from D10) are unchanged and stay notes by instruction; they are not rechecked.

## New BLOCKING or MAJOR findings

None. V-N1 to V-N4 are wording or completeness notes on true statements.

(Checks table follows.)
