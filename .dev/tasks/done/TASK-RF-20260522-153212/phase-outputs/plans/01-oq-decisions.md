# OQ Decisions — TASK-RF-20260522-153212

**Date recorded:** 2026-05-22
**Recorded during:** Step 1.5 (Phase 1, Preparation & Discovery)
**Authority:** User decisions made in the chat session that produced this task file (post adversarial-debate analysis). Resolutions are binding; later items follow these branches verbatim.

---

## OQ-1 — CC1 Regex Consolidation

**DECISION: Rename + Promote + Import (synthesis approach).**

### Verbatim resolution

1. In `src/superclaude/cli/eval/artifact_layout.py`: rename `_EVAL_ID_RE` → `_EVAL_ID_PATH_SAFETY_PATTERN`. Add docstring explaining "Path-safety regex — NOT the FR-SCH2 schema (see EVAL_ID_PATTERN below for that)."
2. In `artifact_layout.py`: **promote** a new public `EVAL_ID_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$")` constant with docstring `"""FR-SCH2 schema contract — see schemas/suite.schema.json. Promoted from loader.py per CC1 to a single source of truth."""`.
3. In `loader.py`: REPLACE the local `re.compile(...)` definition with `from .artifact_layout import EVAL_ID_PATTERN as EVAL_ID_REGEX`. The `EVAL_ID_REGEX` alias remains in `loader.__all__` so `tests/cli/eval/test_eval_id_regex.py:32` (`from superclaude.cli.eval.loader import EVAL_ID_REGEX`) continues to resolve unchanged.

### Why this synthesis (not naive merge)

Defense-in-depth at regex boundaries is genuinely valuable. The two regexes enforce different invariants — path-safety vs FR-SCH2 schema. Naive consolidation would tighten path-safety (rejecting valid YAML) or loosen schema (letting path-traversal through). The "Rename + Promote + Import" approach eliminates the **schema regex duplication** (which is the real CC1 finding) while preserving the **two-layer defense** (which the Pragmatist correctly identified during adversarial debate).

### Affected items

- **Step 5.1** (CC1 implementation): execute the 3-step rename/promote/import sequence
- **Step 5.2** (T8 test): pins the SoT contract — `EVAL_ID_PATTERN is loader.EVAL_ID_REGEX` AND `_EVAL_ID_PATH_SAFETY_PATTERN is not EVAL_ID_PATTERN` + semantic-invariants check
- **Step 6.1 GATE 3 expectation**: TWO `re.compile()` entries in artifact_layout.py (path-safety + schema); ZERO in loader.py for eval-id patterns

---

## OQ-2 — CC2 Exit-Code Consolidation

**DECISION: 4 canonical values in new `exit_codes.py` + 11 module-level re-exports preserving descriptive names.**

### Verbatim resolution

1. **CREATE** `src/superclaude/cli/eval/exit_codes.py` with exactly 4 canonical module-level constants:

   ```python
   """cliEval canonical exit codes (Click/POSIX/BSD sysexits hierarchy)."""
   SUCCESS: int = 0
   FAILURES: int = 1            # one or more eval failures
   USAGE_ERROR: int = 2         # operator misuse / config error (Click convention)
   INTERRUPTED: int = 130       # SIGINT / Ctrl-C (POSIX signal+128)
   ```

2. Each of the 11 `*_EXIT_CODE = 2` declarations becomes a single-line re-export preserving its descriptive name: `from .exit_codes import USAGE_ERROR as <NAME>_EXIT_CODE`. See Step 5.3 for the full 11-site enumeration.
3. Also re-export SUCCESS/FAILURES/INTERRUPTED for symmetry at the `RUN_CLEAN_EXIT_CODE` / `RUN_FAILURES_EXIT_CODE` / `RUN_INTERRUPTED_EXIT_CODE` sites in commands.py.

### Why 4 canonical values (not 11)

The 11 named constants happen to share the value `2` because they're all Click usage/operational errors. Consolidating to 4 canonical values makes future convention shifts (Click 9.0, BSD sysexits) a one-file change rather than an 11-site coordinated diff. The descriptive local names are preserved via re-export, so call-site readability is unchanged.

### Affected items

- **Step 5.3** (CC2 implementation): create exit_codes.py with 4 values + edit 11 declaration sites into re-exports
- **Step 5.4** (T9 test): pins the "no magic exit codes" contract — no literal `sys.exit(N)` calls anywhere; no `*_EXIT_CODE: int = <literal>` outside exit_codes.py; exit_codes.py contains exactly 4 canonical declarations
- **Step 6.1 GATE 5 expectation**: ZERO `*_EXIT_CODE = <literal-int>` declarations outside exit_codes.py

---

## OQ-3 — M1 Deferral

**DECISION: DROP M1 from scope per source spec §4 rationale. No HALT, no ⚪ Blocked state.**

### Verbatim resolution

M1 (`commands.py:1335-1343` — `_default_output_dir()` uses `Path.cwd()`) was classified by the source spec §4 as "flag for follow-up not bundled — existing tests depend on the relative behavior". The builder over-bundled M1 into Phase 5; that was a mistake. Implementation:

1. **Step 5.8 (M1 implementation) is DELETED.** The Phase 5 sequence renumbers: former Step 5.9 (phase verification) becomes Step 5.8.
2. The Key Objective entry referencing M1 is rewritten to enumerate M2-M6 only.
3. **M1 moves to `### Follow-Up Items Identified`** in the Task Log with: spec citation (§4), defect description (`_default_output_dir()` CWD-binding), and deferral rationale (no current invariant broken; H1 anchors layout invariant regardless of root choice; the "right" anchor — repo root vs `$XDG_DATA_HOME` vs cwd — needs an operator-experience decision not made here; trivial workaround via `--output-dir`).
4. The Phase 6 AC matrix records M1 as `DEFERRED-SPEC §4` with the same rationale.

### Why drop, not block

All three deferral conditions hold:

1. No current invariant is broken (H1 anchors layout regardless of root choice; FR-G4 preserved).
2. The "right" fix requires an unmade product decision (cwd vs repo-root vs `$XDG_DATA_HOME`).
3. The workaround is trivial (one `--output-dir` flag).

Deferring is correctly scoped engineering, not technical debt accumulation. The qualitative QA's defensive HALT-state default was reasonable as a safety measure but is not the right response now that the user has explicitly resolved the question.

### Affected items

- **Phase 5 enumeration**: phase description, Key Objective #5 — both rewritten to exclude M1
- **Step 5.8** (formerly the M1-HALT item): DELETED; former Step 5.9 verification renumbered to 5.8
- **Step 6.4 AC matrix**: M1 row carries `DEFERRED-SPEC §4` status with rationale + reference to Follow-Up Items
- **Follow-Up Items**: M1 entry includes spec §4 quote + recommended next-step (separate task pinning the anchor choice)

---

## Resolution authority

All three resolutions were chosen by the user after I (the agent) presented adversarial-debate analyses comparing the alternatives. The deliberation is preserved in the chat transcript that produced this task file. If during execution any evidence contradicts a resolution (e.g. an import error during the OQ-1 Rename step), the executor MUST STOP and surface the conflict in `### Phase 1 Findings` rather than silently switching branches.
