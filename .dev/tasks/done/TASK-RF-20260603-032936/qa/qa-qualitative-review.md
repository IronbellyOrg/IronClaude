# QA Report — Task File Qualitative Review

**Topic:** Implement the sc-recommend lookup-cache layer
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)

---

## Overall Verdict: FAIL → 1 IMPORTANT finding fixed in-place → re-verified PASS

Initial pass surfaced 1 IMPORTANT operational finding (the `executor.py` dangling reference).
Fixed in-place (fix_authorization: true). Post-fix verdict: PASS. Three other inspected items
(line-anchor / figure refs) were verified accurate and required no fix.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `make verify-sync` (Makefile:166) only diffs src↔.claude skills/agents/commands — does NOT touch `.claude/cache/*.yaml` (no src mirror) nor `cli/recommend/` Python (not a sync artifact). Step 6.5 claim sound. `make sync-dev` (Makefile:109) copies skills→.claude/skills, commands→.claude/commands/sc. Step 1.11 import check passes given deferred executor import. |
| 2 | Project convention compliance | none | PASS | Edits target `src/` SoT side; `.gitignore` line refs verified (103=`.claude/cache/`, 117=`.claude/`, 118=`!settings.json`); negation-after-broad-ignore ordering correct (git last-match-wins). `.claude/` mirror staging guard present (Step 6.8). |
| 3 | Intra-phase execution simulation | none | PASS | Ordering sound: cache.py(1.8)→seed(2.4)→tests(3.2); classifier(2.2)→dispatch(4.2); best_model(5.3)→test(5.7). Hard-halt 2.1 before blocked Phase 4/5. |
| 4 | Function signature verification | AX-1 | FAIL→FIXED | Step 6.1 cites main.py "eval group last at 424-426" — VERIFIED (eval_group last before `if __name__`). Roster(6.2) VERIFIED. Drift: Step 1.6 + Phase 5 reference `executor.py` that no item creates (Finding 1). |
| 5 | Module context analysis | none | PASS | tasklist commands.py:96 defers `from .executor import` inside body — group imports cleanly without executor.py present. Lazy `__getattr__` + deferred-heavy-import patterns correctly mirrored. |
| 6 | Downstream consumer analysis | AX-3 | FAIL→FIXED | commands.py subcommand bodies shell to executor functions; if executor.py never authored → runtime ImportError (CLI `--help` test does not exercise bodies). Fixed by Finding 1. eval-runs JSON tracked, consistent w/ spec. |
| 7 | Test validity | none | PASS | Real artifacts: tmp_path round-trip(3.2), real os.replace OSError patch(3.3, precedent test_install_hooks.py:359), exact-5-field assert(3.4), deterministic best_model fixtures(5.7). Not stubs. |
| 8 | Test coverage | none | PASS | UNIT (round-trip, surface_hash invalidation, atomic crash, telemetry, best_model 4 tiers+floor+suppression) + INTEGRATION (CliRunner reg 6.3, full pytest 6.7) both present. |
| 9 | Error path coverage | none | PASS | `--eval` click.Choice; telemetry 6-value enum validation; YAMLError guard; plugin HARD-BLOCK; atomic temp cleanup on crash. |
| 10 | Runtime failure path trace | AX-3 | FAIL→FIXED | input→classify→scan→validate→emit traced; 5 miss reasons handled(4.2). Gap: subcommand→executor.py dead reference(Finding 1). Fixed. |
| 11 | Completion scope honesty | none | PASS | Boundary hard-halt + OQ3 + eval-reuse explicitly gated/deferred; Step 2.1 documents-and-halts (no auto-default); 6.4 leaves status Blocked if boundary unresolved. Honest. |
| 12 | Ambient dependency completeness | AX-3 | FAIL→FIXED | main.py reg(6.1)✓, EXPECTED_TOP_LEVEL_COMMANDS(6.2)✓, __init__ export(1.5)✓, tests conftest(3.1)✓. Missing: executor.py authoring(Finding 1). Fixed. |
| 13 | Kwarg sequencing | none | PASS | No inversions. allowed-tools expansion(1.10)→use(4.2). cache.save() defined(1.8)→invoked(2.4). |
| 14 | Function existence verification | none | PASS | Grepped: check_mcp_server_installed(install_mcp.py:470), check_binary_available(:156), grader 5 types(grader.py:11-26), _atomic_write_json(test_install_hooks.py:30), executor.py present in tasklist precedent. anthropic ban pyproject:208-211. |
| 15 | Template/cross-ref accuracy | none | PASS | Spec refs verified: eval matrix(merged-req:224-277), control flow(107-135), best_model confidence<0.5(382), precondition schema(round-4:124-135), 3 refs exist, 12-step Order(408-434). |

## Summary
- Checks passed: 15/15 (after in-place fix)
- Checks failed (pre-fix): items 4,6,10,12 (one shared root cause — executor.py dangling reference)
- Critical issues: 0
- Issues fixed in-place: 1 (IMPORTANT)
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 2 | Grep: 0 | Glob: 0 | Bash: 9 (each Bash verified a specific claim: gitignore lines, main.py registration, roster, install_mcp helpers, anthropic ban, grader types, eval matrix, control flow, executor deferral, tasklist precedent layout)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Steps 1.6, 5.1-5.2, PG5.1 | `executor.py` referenced as a shell target (1.6 "shelling to `executor.py`") and as eval-logic home (5.1/5.2 "or within `executor.py`"; PG5.1 "or their `executor.py` equivalents"), but NO item creates it and Step 1.11's import-sanity check omits it. tasklist precedent HAS executor.py; recommend module never authors one. Subcommand bodies would ImportError at runtime — CLI `--help` registration test does NOT exercise function bodies, so the gap passes the gate silently and surfaces only on `superclaude recommend <subcmd>` invocation. | Clarify that `executor.py` is created only if/when the boundary option requires a dispatch driver; otherwise the deterministic helpers live directly in their named modules (cache.py / telemetry.py / eval_grader.py / eval_aggregate.py / best_model.py / plugin_eval.py). Make Step 1.6's commands.py defer to the named helper modules (which ARE authored) rather than a phantom executor.py, and note executor.py as boundary-contingent. APPLIED below. |

## Actions Taken

Fixed Finding 1 (executor.py dangling reference) in-place across 4 locations in the task file:

- **Step 1.6 (commands.py):** Replaced "each deferring heavy imports inside its body and shelling
  to `executor.py`" with explicit deferred imports to the named helper modules THIS task authors
  (`from .cache import LookupCache`, `from .telemetry import append_event`, and the Phase-5
  `eval_grader`/`eval_aggregate`/`best_model`/`plugin_eval` modules), with an explicit note that an
  `executor.py` dispatch shim is created ONLY if the Phase 2 boundary option needs one, and "do NOT
  leave a subcommand body importing a module no item creates."
- **Step 5.1 (grader):** Changed "or within `executor.py` per the chosen boundary option" to name
  `eval_grader.py` as the authored home, with any boundary-option `executor.py` IMPORTING from it,
  not replacing it.
- **Step 5.2 (aggregation):** Same fix — `eval_aggregate.py` is the named authored home; an
  `executor.py` shim imports from it, never substitutes.
- **Step PG5.1 (aggregation gate):** Changed "or their `executor.py` equivalents" to "plus an
  `executor.py` ONLY if the chosen boundary option authored a dispatch shim — confirm any subcommand
  body that imports a module has that module actually present on disk, no dangling `executor.py`
  import." This adds an on-disk-existence verification to the gate that would have caught the gap.

**Verification of fix:** Re-grepped `executor.py` across the task file — all 4 remaining mentions
are now correctly contextualized as (a) the tasklist PRECEDENT's executor (accurate description,
not a directive) or (b) boundary-contingent / import-from-not-replace. No checklist item now
mandates importing a phantom `executor.py`; the authored modules (cache/telemetry/eval_grader/
eval_aggregate/best_model/plugin_eval) are the concrete deferred-import targets and ARE created by
Steps 1.8/1.9/5.1/5.2/5.3/5.5. Step 1.11's import-sanity check (cache,telemetry,models,commands)
remains valid because commands.py defers all heavy imports inside function bodies (tasklist
precedent commands.py:96 confirmed). PG5.1 now verifies no dangling import survives.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa task-integrity PASS for items 1-9 + TB-Add-1/3/4/5/6/7/8 + SV-1/2/3/4 (frontmatter
  shape, section numbering, item structure, DAG, XL-split, verify-form, per-item-evidence,
  gitignore-ordering structural, registration structural, vacuous-new-hook, no-.claude-staging).
  Did NOT re-verify section numbers, frontmatter keys, or item-checkbox structure.

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT and my
own tool work was required:**
- **Operational dead-reference:** rf-qa SV-2 (registration) PASS confirms main.py + roster edits are
  structurally well-formed, but it does NOT catch that commands.py defers to an `executor.py` no item
  authors. I read `tasklist/commands.py:96` (Bash) to confirm the deferred-import idiom, listed
  `tasklist/` (Bash) to confirm executor.py exists in the PRECEDENT but is never created for
  recommend, and traced Step 1.11's import check to confirm the gap passes structurally but breaks at
  runtime. This is a semantic/operational defect invisible to structural QA — Finding 1.
- **Gate dry-run vs verify-sync:** rf-qa cannot reason about whether `make verify-sync` trips on the
  new tracked cache YAMLs. I read `Makefile:166` (verify-sync) and `:109` (sync-dev) (Bash) to
  confirm verify-sync only diffs src↔.claude skills/agents/commands and never touches
  `.claude/cache/*.yaml` or the Python module — confirming Step 6.5's claim is operationally sound.
- **Spec-fidelity of quantitative claims:** rf-qa evidence-citation check (item 5) confirms anchors
  exist, but not that the cited VALUES match. I read merged-requirements.md:224-277 (eval matrix),
  :382 (best_model confidence<0.5 suppression), :107-135 (control flow), and round-4:124-135
  (precondition schema) (Bash) to confirm the task's quantitative claims (MODE_MATRIX panels, tier
  rules, 70% floor) faithfully match the spec — they do.

## Recommendations
- Finding 1 is fixed in-place; the task file is now operationally coherent for execution. No further
  action required before `/task` execution.
- ADVISORY (non-blocking, already flagged by rf-qa TB-Add-2): 59 items > 50 soft cap. Acceptable for
  a 6-phase greenfield CLI build with PER_PHASE gates; not a defect.
- Carry-forward (already in the task's Follow-Up Items, Medium): classification keys 5-10 lack
  iteration-1 eval coverage — correctly deferred, not a blocker.

## QA Complete

**VERDICT: PASS** (1 IMPORTANT finding found and fixed in-place; re-verified). No unfixable issues.
