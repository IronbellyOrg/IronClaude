# sc:reflect UC-1 pre-execution report (run 2): orchestrator-mode Phase 1 tasklist, final edited file

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 105                 # distinct cited ranges in this report
citations_revalidated: 105           # evidence-validator, full_reread
citations_dropped: 0                 # zero-drop-flag: true (validator re-checked and gave a self-audit)
citations_inferred: 3
citation_budget_policy: full_reread  # --depth deep forces full_reread
coverage_degraded: null
```

## Run context

- **Spec:** `docs/designs/orchestrator-mode.md` (1013 lines).
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (2896 lines, 355 items).
- **What this run audits:** the FINAL task file after the coordinator-approved hand edits: N-01, the R5 allow decision, alignment fixes B-1 to B-4, and Phase 7 N-1 and N-2.
- **Superseded run:** run 1 (`reflect/pre/REPORT.md`, run id `reflect-pre-20261108T095922Z-TASK-RF-sweep-phase1`) audited the pre-edit file. This run replaces it. Run 1's HIGH findings are listed for context only: F-01 (every owner gate deadlocks a correct run), F-02 (the 8.3 count check gives wrong results both ways) and F-03 (7.16 forbids the commands its own step (6) runs). No run 1 finding is reused here. The F-ids below are new and refer to the final file.
- **Mode:** pre (UC-1). **Tier reached:** 2. `artifacts/tier_decision.yaml` records `selected_tier: 2`, forced by the `--depth deep` override (section 5.1). The rubric would also have escalated: S_domains is 5 (rule 4), and the Tier-1 self-reported C of 0.84 is below 0.85 (rule 6). Composite score 8.0; S_dev_density 0.079.
- **Input drift:** none. `input_tree_sha256` daaca8ba3f4f971b641dcacf75f80ee6942775b6f3f0483a7af68eb06f8eccf4 over 40 files (`artifacts/input-snapshot.yaml`) was recomputed in Wave 5 and matched (audit.log steps 0.4 and 5.x).
- **Tier-1 card:** `reflection-card-t1.yaml`, written by requirements-analyst: 0 HIGH, 6 MEDIUM, 7 LOW. Self C was 0.84; the calibrator (sonnet) set C to 0.82 after checking 48 citations with 0 failures, and recommended escalation.
- **Reviewers (Tier 2, agent type reflect-reviewer, read-only):**

| Reviewer | Role | Alias (slot) | Self C | Calibrated C | Calibrator | Citations checked / failed | Candidate verdicts |
|---|---|---|---|---|---|---|---|
| R1 | analyzer | claude-gw-tier1b (sonnet) | 0.72 | 0.71 | opus | 78 / 41 (the 41 are second row refs, discarded by the merge, S-004) | 0 HIGH, 3 MEDIUM, 6 LOW (1 refuted, 3 weakened) |
| R2 | qa | claude-gw-tier2 (haiku) | 0.90 | 0.81 | opus | 29 / 0 | 6 HIGH, 1 MEDIUM, 2 LOW (calibrated to 1 HIGH: R2-G1) |
| R3 | refactorer | claude-gw-tier1a (opus) | 0.75 | 0.79 | sonnet | 36 / 0 | 0 HIGH, 3 MEDIUM, 8 LOW (4 weakened) |

- **Diversity:** `t2_model_class_diversity: full`. `t2_vendor_diversity: single` (all three aliases are Anthropic gateway models), a warning only. `calibrator_diversity: degraded`: each card was calibrated by a class other than its own reviewer's, but every calibrator class was also a reviewer. `executor_class_resolved: false`: UC-1 runs before execution, so there is no executor.
- **Adversarial merge:** sc-adversarial-protocol Mode A over 3 variants, at standard depth. The base is variant-2 (combined scores V2 0.798, V1 0.792, V3 0.698). The margin of 0.006 is below 0.05, so the level-1 tiebreaker decided: V2 won 12 debate points, V1 won 9. `convergence_score: 1.00`: all 50 diff points were agreed after Round 2 (58 of 58 counting sub-points; Round 1 had 0.94). `convergence_status: BLOCKED_BY_INVARIANTS`: invariants INV-006 and INV-021 were HIGH and not addressed by the debate. The merge folded INV-006 into F-02 and INV-021 into F-03, and recorded neither as accepted risk. The plan review first returned FAIL (B-01), then PASS after one fix cycle; minor notes N-01 to N-06 were carried as notes on the findings. The merge applied 30 of 30 changes, re-read 93 evidence refs and 28 locations, and found 0 broken and no new contradictions.
- **Status:** `partial`. The adversarial return contract reports `status: partial` because convergence is BLOCKED_BY_INVARIANTS, not because a merge or validation step failed. The Wave 5 evidence-validator re-read all 105 cited ranges and dropped none (a zero-drop result, re-checked by the validator and logged with `zero-drop-flag: true`), so the status stays `partial` for the convergence reason only.

Citation aliases (from `adversarial/merged-verdict.yaml` `path_aliases`, plus two used by single findings):

| Alias | Path |
|---|---|
| TL | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` |
| DESIGN | `docs/designs/orchestrator-mode.md` |
| coverage-matrix | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/coverage-matrix.yaml` |
| OQ-1-decision | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-1-agent-wait-decision.md` |
| reflection-card-t1.yaml | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/reflection-card-t1.yaml` |
| config.py | `src/superclaude/cli/reflect/config.py` |

## Verdict summary

Do not run the tasklist as written. Two HIGH findings mean a correct run fails its own checks:

1. **F-01:** the item 8.3 `grep -c` name count rejects a conforming `models.py`.
2. **F-02:** the item 6.2 check expects one grep hit, but the pattern already matches 3 lines before 6.2 runs and 4 after a correct append.

The merged verdict has 28 findings: HIGH 2, MEDIUM 13, LOW 13. The most consequential MEDIUM finding is F-03, which carries INV-021: step 1.0a can end in two outcomes that have no owner route, and an owner approval has no follow-up path. Coverage after Tier 2 is high: 0.960 of parsed rows and 0.914 of the union. The problems are in how the checks and gates are written, not in missing requirements. The best-practice grade is 3 of 5 and calibrated confidence is 0.77. Evidence validation is pending.

## Coverage

| Measure | Tier 1 (matrix, coverage-matrix:41-58) | Tier 2 (traced, merged) |
|---|---|---|
| Parsed rows | 122 of 126 = 0.968 | 121 of 126 = 0.960 |
| Union (126 parsed + 26 inferred) | 140 of 152 = 0.921 | 139 of 152 = 0.914 |
| Union rows not covered | 12 | 13 |

**Why Tier 2 is one row lower.** In this run the Tier-1 matrix was re-verified by reading each delivering item against the current tasklist, with range expansion for "X to Y" and "X..Y". The literal ID pass is `artifacts/match_ids.py`. Tier-2 tracing changed one parsed row: step-1.0a dropped to partial (X-005). INF-019 also went from covered in substance to partial in V2's card (X-001, X-005), but the matrix already counted INF-019 as not covered, so the union difference is step-1.0a alone.

Merged ledger (152 unique rows, no overlap between the three disjoint card slices): covered 109, covered in substance 30, partial 10, missing 3, false match 0. By scope: parsed rows 97 / 24 / 5 / 0 / 0, inferred rows 12 / 6 / 5 / 3 / 0. Per card: V1 76 rows, V2 44, V3 32.

Rows not fully covered:

| Row | Kind | Merged status | Finding |
|---|---|---|---|
| GQ-111 | parsed | partial | F-04 |
| GQ-112 | parsed | partial | F-04 |
| GQ-113 | parsed | partial | F-04 |
| SP-28 | parsed | partial | F-05 |
| step-1.0a | parsed | partial | F-03 |
| INF-001 | inferred | missing | F-04 |
| INF-008 | inferred | missing | F-06 |
| INF-024 | inferred | missing | F-05 |
| INF-005 | inferred | partial | F-06 |
| INF-017 | inferred | partial | F-18, F-19 |
| INF-018 | inferred | partial | F-06 |
| INF-019 | inferred | partial | F-03 |
| INF-020 | inferred | partial | F-03 |

Caveats from the merged ledger:

- A delegated row is covered only if the delegate item runs as written.
- V1's rows were checked item by item, but their second refs were unreliable (41 discarded, S-004).
- [INFERRED] 21 of V3's covered rows rest only on the Tier-1 matrix row and were not independently confirmed.
- The slices are disjoint by brief, so per-card row counts measure brief width, not reviewer quality (S-001).
- F-07 adds a requirement (DESIGN:636) that has no matrix row, so the 152-row union leaves it out.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | "`/task-builder` must copy the same rule into the task file: cite GAPS line 138 for counts and never edit the REPORT." | DESIGN:80 | Tier 1: missing (none). Tier 2: missing (F-04) |
| INF-002 | "`report.py` keeps only pure code: `sanitize`, `render`, `SECTIONS`, the fixed strings and `CHECKED_ORCA_VERSION`. No `write_report` exists." | DESIGN:88 | Tier 1: covered (containment, 8.12). Tier 2: covered |
| INF-003 | "Decision: write a temp file in the output directory, `fsync` it, then publish it under the report name with `os.link`, which fails when the name exists." | DESIGN:101 | Tier 1: covered (containment, 9.1). Tier 2: covered |
| INF-004 | "`_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` have succeeded, so a usage error or an internal error in those steps never reaches the filesystem." | DESIGN:103 | Tier 1: covered (containment, 9.1). Tier 2: covered |
| INF-005 | "B1: imports go one way, `commands -> {probes, classify, report} -> models`." | DESIGN:215 | Tier 1: partial (containment, 8.4, 8.12). Tier 2: partial (F-06) |
| INF-006 | "B3: the read allowlist lives only in `probes.py`. Phase 2 `/sc:close` gets its own package, seam and allowlist; nothing in this package grows a write verb (FR-021)." | DESIGN:217 | Tier 1: covered in substance (none; 8.10, 10.3). Tier 2: covered |
| INF-007 | "B4: the command and skill are thin: no parsing, no classification, no file writes." | DESIGN:218 | Tier 1: covered in substance (none; 11.1, 11.3). Tier 2: covered |
| INF-008 | "B5: no type is redeclared from `superclaude.contracts`." | DESIGN:219 | Tier 1: missing (none). Tier 2: missing (F-06) |
| INF-009 | "R1, R2 and R3 land in one commit. Editing R1 or R2 without R3 fails the parity test." | DESIGN:705 | Tier 1: covered in substance (none; 13.1, 13.2, 13.4). Tier 2: covered |
| INF-010 | "R1 and R6 avoid the words stop, retry, release, merge and removal in the sweep's description." | DESIGN:707 | Tier 1: covered (containment, 13.2, 13.5). Tier 2: covered |
| INF-011 | "No `.claude/` path is staged; `make sync-dev` then `make verify-sync` (step 1.25) refresh the dev copies." | DESIGN:708 | Tier 1: covered (containment, 14.1). Tier 2: covered |
| INF-012 | "The pattern names `.dev/sweeps/` only. It does not cover `.dev/tasks/`, which stays tracked and always staged (CLAUDE.md rule)." | DESIGN:719 | Tier 1: covered (containment, 8.6, 13.7). Tier 2: covered |
| INF-013 | "An autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`. It steps aside only for a test carrying the existing `integration` marker, which is used by exactly one test, the real-git test below." | DESIGN:731 | Tier 1: covered (containment, 8.8, 10.8). Tier 2: covered |
| INF-014 | "Where the REPORT text and this design differ, this design wins (section 13, REPORT differences)." | DESIGN:902 | Tier 1: covered in substance (containment; Execution Context and Phase 8 preamble). Tier 2: covered |
| INF-015 | "They go into step 1.4a because the real-git test created there copies the repository `.gitignore`, so its FR-025 check-ignore assertions fail until the line exists." | DESIGN:942 | Tier 1: covered (containment, 8.6, 8.9). Tier 2: covered |
| INF-016 | "`worker-show` and `task-list` are each run once before and once after all other reads. The two outputs must be identical apart from timestamps; that is the only live check that these reads change nothing (M4)." | DESIGN:875 | Tier 1: covered (containment, 7.16). Tier 2: covered (see F-25) |
| INF-017 | "It is a manual, pre-implementation capture run by the person or the coordinator, never by a test, and it writes only its own notes file." | DESIGN:868 | Tier 1: partial (containment, 7.16). Tier 2: partial (F-18, F-19) |
| INF-018 | "The report holds no action control, no command to paste and no advice to delete anything under `.dev/tasks/`." | DESIGN:638 | Tier 1: partial (containment, 8.12, 10.5). Tier 2: partial (F-06) |
| INF-019 | "If the step 1.0a capture shows it needs `--json` for a parseable result, that is a template change and needs the same owner note as any other allowlist change; until then the parser reads the captured plain shape." | DESIGN:550 | Tier 1: partial (containment, 7.16, 7.17). Tier 2: partial (F-03) |
| INF-020 | "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)." | DESIGN:552 | Tier 1: partial (containment, 7.17, 8.10, 10.3). Tier 2: partial (F-03) |
| INF-021 | "The skill prints no recommendation, proposes no action and never edits, stages or deletes a file." | DESIGN:654 | Tier 1: covered (containment, 11.3, 11.4). Tier 2: covered |
| INF-022 | "Every function is pure over `SweepResult`; no function reads a clock, a file or an environment variable." | DESIGN:594 | Tier 1: covered (containment, 8.12). Tier 2: covered |
| INF-023 | "All edits are to existing files; no new doc file. Rows and bullets are added, none removed or reworded." | DESIGN:690 | Tier 1: covered in substance (none; 13.1, 13.2, 13.3, 13.5, 13.6). Tier 2: covered |
| INF-024 | "The limits apply as proposed and are marked proposed in `probes.py`" | DESIGN:987 | Tier 1: missing (none). Tier 2: missing (F-05) |
| INF-025 | "Only `commands.run` calls `sys.exit` or raises `click` exit types." | DESIGN:445 | Tier 1: covered (containment, 9.1). Tier 2: covered |
| INF-026 | "No cleanup sweep: a later run never deletes a file it did not create." | DESIGN:147 | Tier 1: covered in substance (none; 9.1, 10.7). Tier 2: covered |

"Tier 2: covered" means covered or covered in substance in the merged ledger. Inferred-scope totals match exactly between Tier 1 and Tier 2: covered 12, covered in substance 6, partial 5, missing 3.

POSTSCRIPT: the evidence-validator matched all 26 verbatim quotes to their DESIGN lines (and to coverage-matrix:202-227). No INF row was dropped, so `coverage_pct_union` (0.914), `unmapped_requirements_union` and `S_dev_density` stand unchanged.

## Deviations

Classification note: UC-1 runs before execution, so there is no executed work to sort into the four deviation categories (authorized, necessary, drift, regression). Each block gives the merged verdict's gap class and marks the category n/a (UC-1). Wave 5 does not re-judge any finding. D-nn matches F-nn.

### HIGH (correct delivery fails the check)

### Deviation D-01 (F-01): The 8.3 name count rejects a correct models.py

- **Severity:** HIGH. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1436
- **Mapped tasklist item:** 8.3
- **Spec section:** DESIGN section 7.2, data model (DESIGN:454, DESIGN:459, DESIGN:466)
- **Finding:** Item 8.3 uses `grep -c` to count every occurrence of each model name, not its definitions. Correct field annotations repeat names such as OrcaObservation, TranscriptTail and ClassifiedRow, and the 8.3 builder decision for ClassifiedRow repeats SessionRow, Classification and SafeToClose. The rule that each name "appears once" therefore rejects a conforming `models.py`.
- **Evidence:**
  - TL:1436: "every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name)"
  - TL:1433: "`ClassifiedRow` is `row: SessionRow`, `classification: Classification`, `policy: str | None`"
  - DESIGN:454: "orca_rows: tuple[OrcaObservation, ...]"
  - DESIGN:459: "| `SessionRow` | SPEC list (line 235)"
  - DESIGN:466: "rows: tuple[ClassifiedRow, ...]"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G1, calibrated HIGH and confirmed; debate C-012 and U-001, conceded by V1 and V3, consensus rank 1; merge Change 1; INV-020 (sufficiency_challenge, ADDRESSED): 8.3 is the only item that counts names, so this fix alone is enough. The consensus phrase "R2-G1 is the only HIGH of the run" was removed because F-02 is a second HIGH.
- **Default remediation:** Replace the occurrence count in 8.3 with a definition count (R-01).
- **[INFERRED] notes:** none.

### Deviation D-02 (F-02): The 6.2 check can never return one hit on a correct run

- **Severity:** HIGH. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:993
- **Mapped tasklist item:** 6.2
- **Spec section:** n/a. The check is internal to the tasklist; the governing rule is the Execution Log rule at TL:2804.
- **Finding:** The pattern `grep -n 'OQ-1 (R5) RESOLVED' <TL>` matches 3 lines before 6.2 runs (TL:991, TL:993 and TL:2802) and 4 after a correct append. A correct run cannot give the "one hit" the check expects.
- **Evidence:**
  - TL:991: "Append one line to `### Execution Log`: "OQ-1 (R5) RESOLVED by the owner 2026-11-08:"
  - TL:993: "`grep -n 'OQ-1 (R5) RESOLVED' .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` returns one hit."
  - TL:2802: "| 2026-11-08T12:20Z | 6.1-6.4 | Build-time hand edit (coordinator msg_d95a87e312e1, msg_6ee5998d0874) | OQ-1 (R5) RESOLVED by the owner 2026-11-08:"
  - TL:2804: "Every HALT line, every owner decision (OQ-n, chosen option, decider, source) and every resume is appended here as one row."
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; the defect lies outside the 50 diff points. It comes from invariant probe INV-006 (guard_conditions, HIGH, UNADDRESSED), one of the two blockers behind BLOCKED_BY_INVARIANTS, and was merged as a new finding by Change 2 (caller ruling (a)). On 2026-11-08 the orchestrator ran the proposed command: it printed 0 against the current TL and 1 against a temporary copy with one such row appended. The merge executor's re-run printed 0.
- **Default remediation:** Append a four-column Execution Log row in 6.2 and count only rows whose Item column is 6.2 (R-02).
- **[INFERRED] notes:** none.

### MEDIUM

### Deviation D-03 (F-03): Two step 1.0a outcomes have no owner route

- **Severity:** MEDIUM. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:1265-1269
- **Mapped tasklist items:** 7.16, 7.17, 8.10, 10.3; DESIGN 7.3, 11, 12 and 15.1.
- **Spec section:** DESIGN section 7.3 (DESIGN:550, DESIGN:552); section 17 open items 3 and 5 (DESIGN:971, DESIGN:973).
- **Finding:** Step 1.0a can end in two outcomes that have no owner route. (a) A captured worker-list cursor field conflicts with the ten-template pins, and the 7.17 Branch fires only when a field name differs, so it cannot fire for this. (b) On the CLOSED path of open item 3, a `run-current --json` need has no owner route, and TL:1259 forbids the `--json` probe. INV-021 shows that adding an owner-routing branch is not enough on its own. If the owner approves an 11th template or `run-current --json`, DESIGN 7.3, 11, 12 and 15.1, the 7.16 forbidden list (TL:1259, TL:1262), 8.10 (TL:1482, TL:1485) and 10.3 (TL:1793) still pin the old state, and nothing re-gates a second allowlist edit. Severity is MEDIUM because the result is a stalled or conflicted build, not wrong code shipped (X-002).
- **Evidence:**
  - TL:1267: "Branch: if a live field name differs from the name DESIGN section 7.2 or 7.3 uses, apply the HALT rule"
  - TL:1482: "`ALLOWED_ORCA` (exactly 10 templates after item 6.3)"
  - TL:1482: "From the 1.0a facts: the field names, the time format, `RUN_ID_RE`, `DISPATCH_ID_RE`, the cursor field."
  - TL:1485: "a count of `ALLOWED_ORCA` entries is 10"
  - TL:1793: "exact-set pin of the ten templates (DESIGN 7.3 after item 6.3)"
  - TL:1259: "any `git stash`, and `run-current --json`"
  - DESIGN:552: "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)."
  - DESIGN:971: "a `--json` need goes to the owner as an allowlist change"
  - DESIGN:973: "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template"
  - TL:1142: "Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule with the `blocker_reason` the item names and STOPS"
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R1-G1 (claim) and R2-G5 (cursor half only); debate C-001, C-002, X-001, X-002, X-005, A-001, A-001c and A-001d; merge Change 3 (caller ruling (b)). INV-021 (sufficiency_challenge, HIGH, UNADDRESSED) is folded in by widening the remedy, not by raising the severity (X-002). INV-016 stays in the provenance because remedy step 3 contrasts with it. R1-G1's gate-bypass label was dropped in favour of describing the outcomes as unrouted (A-001). Rows step-1.0a, INF-019 and INF-020 point here.
- **Default remediation:** Add a named 7.17 branch that writes a PENDING decision file, HALTs before step 1.2 and states what an approval triggers (R-03, verbatim wording).
- **[INFERRED] notes:** none.

### Deviation D-04 (F-04): Key Constraints does not carry the DESIGN:80 builder rule

- **Severity:** MEDIUM. Gap class `traceability`. Tag Grounded.
- **Location:** TL:157-167
- **Mapped tasklist item:** Key Constraints
- **Spec section:** DESIGN section 2.3 (DESIGN:78, DESIGN:80)
- **Finding:** No Key Constraints bullet tells the executor to cite GAPS line 138 for counts and never to edit the REPORT. The narrower rule at TL:365, that a design-fix agent never edits a research file, does not cover this. This is a missing preventive bullet, not an observed breach.
- **Evidence:**
  - DESIGN:80: "- `/task-builder` must copy the same rule into the task file: cite GAPS line 138 for counts and never edit the REPORT."
  - DESIGN:78: "113 rows, 88 open, 25 resolved"
  - TL:365: "never edits a research file"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G2, self-rated HIGH, calibrated MEDIUM (weakened); V2 conceded HIGH (consensus rank 3); debate C-013; merge Change 4. Rows GQ-111, GQ-112 and GQ-113 (partial) and INF-001 (missing) point here.
- **Default remediation:** Add one Key Constraints bullet that carries DESIGN section 2.3 (R-04).
- **[INFERRED] notes:** none.

### Deviation D-05 (F-05): The byte limits are not marked "proposed", and open item 19 has no closing disposition

- **Severity:** MEDIUM. Gap class `traceability`. Tag Grounded.
- **Location:** TL:1482-1486
- **Mapped tasklist items:** 8.5, 8.10, closing follow-ups
- **Spec section:** DESIGN section 17 open item 19 (DESIGN:987, DESIGN:993) and DESIGN:852
- **Finding:** Item 8.10 implements the byte limits but does not mark them "proposed" in `probes.py`, as DESIGN requires, and no item checks for that marking. Open item 19 (the rationale) has no tracked closing disposition. The task does not release, so the before-release deadline is not breached; the immediate gap is the missing marking in the source.
- **Evidence:**
  - DESIGN:852: "The byte limits stay "proposed"; the rationale required before release is an open item"
  - DESIGN:987: "The limits apply as proposed and are marked proposed in `probes.py`"
  - TL:1483: "Append these names to `src/superclaude/cli/sweep/probes.py` in DESIGN order."
  - DESIGN:993: "Total: 23 open items."
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G3, self-rated HIGH, calibrated MEDIUM (weakened); debate C-014, consensus rank 4; merge Change 5. INV-003 (state_variables, LOW, UNADDRESSED): the closing disposition must keep 23 rows, or the same edit must update all four pins (TL:269, TL:454, TL:784, TL:1005). Rows SP-28 (partial) and INF-024 (missing) point here.
- **Default remediation:** Mark the limits proposed in source, check the marking, and carry open item 19 into the closing follow-ups (R-05).
- **[INFERRED] notes:** none.

### Deviation D-06 (F-06): No check covers the probes.py import boundary, B5, or the renderer bans

- **Severity:** MEDIUM. Gap class `test-plan`. Tag Grounded.
- **Location:** TL:1481-1507
- **Mapped tasklist items:** 8.10, 10.2, 10.5
- **Spec section:** DESIGN section 4 boundary rules (DESIGN:211, DESIGN:219); section 7.5 (DESIGN:638)
- **Finding:** No planned check covers three DESIGN constraints: the `probes.py` side of the one-way import boundary, B5's ban on redeclaring types from `superclaude.contracts`, and the renderer's ban on action controls, pasteable commands and advice to delete task files. Item 10.2 checks only the imports of `classify.py` and `report.py`. A grep for the absence of an import cannot prove B5, because a copied type does not need to import its original module. These are missing checks, not proven breaches.
- **Evidence:**
  - DESIGN:211: "| `probes.py` | `models`, `subprocess`, `os`, `json`, `time` | `classify`, `report`, `click` |"
  - DESIGN:219: "- B5: no type is redeclared from `superclaude.contracts`."
  - DESIGN:638: "- The report holds no action control, no command to paste and no advice to delete anything under `.dev/tasks/`."
  - TL:1787: "The AST test parses `classify.py` and `report.py` with `ast` and checks their imports."
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G4, self-rated HIGH, calibrated MEDIUM (weakened); debate C-015, consensus rank 5; merge Change 6. Rows INF-005 and INF-018 (partial) and INF-008 (missing) point here.
- **Default remediation:** Extend the boundary check to `probes.py`, add a B5 declaration comparison, and add a renderer-content check (R-06).
- **[INFERRED] notes:** none.

### Deviation D-07 (F-07): The set-union session-count wording has no coverage row

- **Severity:** MEDIUM. Gap class `traceability`. Tag Grounded.
- **Location:** coverage-matrix:201-227
- **Mapped tasklist items:** 8.12; coverage-matrix
- **Spec section:** DESIGN section 7.5 (DESIGN:636); section 12 FR-011 row (DESIGN:765)
- **Finding:** Every session count must print the distinct-affected-session set-union wording. The FR-011 row covers only heading order and sorting, and no inferred row captures this rule. Item 8.12 refers to section 7.5 broadly, so the requirement may still be delivered by delegation, but the matrix cannot show it.
- **Evidence:**
  - DESIGN:636: "Every count over sessions prints `Distinct affected sessions: <N> (set union, not a sum)`."
  - DESIGN:765: "| FR-011 | `SECTIONS` order and the (a) sort (7.5) | `sweep/test_report.py` |"
  - coverage-matrix:25: "inferred: requirement-shaped MUST/never/only statements outside every parsed span; verbatim quote, max 2 sentences"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G6, calibrated MEDIUM (confirmed); this was V2's only recall pass beyond the matrix. Debate C-016; merge Change 7.
- **Default remediation:** Add an inferred row for DESIGN:636 mapped to 8.12 and name the rule in 8.12 (R-07).
- **[INFERRED] notes:** none.

### Deviation D-08 (F-08): The D10 row and the R5 history line under-report the SPEC departure

- **Severity:** MEDIUM. Gap class `traceability`. Tag Grounded.
- **Location:** TL:998
- **Mapped tasklist item:** 6.3
- **Spec section:** DESIGN section 13 D10 row (written by 6.3); SPEC NFR-003 and NFR-014
- **Finding:** The D10 SPEC cell leaves out NFR-003 and the two other SPEC lines that forbid the flag. The Design cell does not say that the NFR-014 exact-set pin grows from eight templates to ten. The Section cell and the step (7) list leave out sections 2.2 and 12, which 6.3 edits.
- **Evidence:**
  - TL:998: "| D10 | NFR-014 and SPEC lines 310, 500, 504, 562 and 619: \`worktree ps\` never carries \`--agent-wait\` |"
  - TL:998: "the allowlist pin and the version-scoped claim (Orca 1.4.245) are kept (7.3, 11, 13, 15.1) |"
  - TL:999: "DESIGN sections 7.3, 11, 12 (NFR-014 row), 13, 15.1, the GQ-109 row and the `### Fix cycle 3` table updated."
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R3-G1 and R3-G7 merged into one finding (both confirmed); debate C-017; merge Change 8. INV-018: once section 4 is edited, the R5 row and the D10 "where" cell must list section 4 too, or this defect returns.
- **Default remediation:** Rewrite the D10 SPEC, Design and Section cells and the step (7) list (R-08).
- **[INFERRED] notes:** [INFERRED] The SPEC line numbers (132, 143, 310, 323, 500, 504, 510, 562 and 619) are V3's reads of `merged-requirements.md`; the merge executor did not re-read the SPEC.

### Deviation D-09 (F-09): DESIGN:221 still requires a capture before adding a template

- **Severity:** MEDIUM (open in substance; LOW is defensible). Gap class `authorized-expansion`. Tag Grounded.
- **Location:** DESIGN:221
- **Mapped tasklist items:** 6.3; DESIGN section 4
- **Spec section:** DESIGN section 4, extension-point rule (DESIGN:221)
- **Finding:** R5 authorizes templates 9 and 10, but the section 4 extension-point rule still allows a new `ALLOWED_ORCA` template only after a capture, and no 6.3 step reaches DESIGN:221. Item 7.16 does not run the agent-wait forms. This is an authorized expansion with an incomplete record, not scope creep.
- **Evidence:**
  - DESIGN:221: "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)"
  - TL:1259: "(`worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a)"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G5, first remedy only (confirmed; the calibrator noted MEDIUM is arguable); debate C-020, X-006 and A-005; merge Change 9; INV-018. The severity stays open (consensus Part 4 item 7) and this merge does not settle it. V3's second remedy was withdrawn. See D-12 for the review gap.
- **Default remediation:** Reword DESIGN:221 in item 6.3 to accept a recorded owner decision (R-09).
- **[INFERRED] notes:** none.

### Deviation D-10 (F-10): The 6.4 rule needs a 15.1 hit that 6.3 removes

- **Severity:** MEDIUM. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1005
- **Mapped tasklist items:** 6.3, 6.4
- **Spec section:** DESIGN section 15.1 (DESIGN:873)
- **Finding:** The 6.4 pass rule requires a 15.1 hit that allows `--agent-wait`, but 6.3 step (4) removes the only 15.1 agent-wait hit and adds no sentence that allows it. The rule is ambiguous and costs a fix loop via TL:1007.
- **Evidence:**
  - TL:1005: "the hits in 7.3 (the two `ALLOWED_ORCA` templates), 11, 13 (D10) and 15.1 allow it"
  - DESIGN:873: "no `--include-remote`, no `--agent-wait`, and no `git stash` in any form"
  - TL:1007: "On a FAIL, fix the edit in item 6.3 and re-run this item"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G6, 15.1 half (weakened); debate C-021; merge Change 10; INV-022 (ADDRESSED): this one-clause fix alone is enough. V3's wording is kept, not V1's "cannot pass" (open in substance, Part 4 item 7). The D10 half of R3-G6 is not carried; its re-run risk is D-27.
- **Default remediation:** Write the TL:1259 allowance sentence into 15.1 in 6.3 step (4) (R-10).
- **[INFERRED] notes:** none.

### Deviation D-11 (F-11): The Phase 7 preamble points at item 6.2, which has no HALT procedure

- **Severity:** MEDIUM. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:1142
- **Mapped tasklist items:** Phase 7 preamble, 7.15, 14.7
- **Spec section:** n/a (the tasklist HALT procedure at TL:194 and TL:1142)
- **Finding:** The Phase 7 preamble says every HALT item follows the item 6.2 procedure, but item 6.2 is titled "no HALT" and holds no HALT procedure. The impact is smaller than the card states because TL:1142 spells out both Branches itself. What remains: Branch 2 of items 7.15 and 14.7 does not require the owner's quoted words before `status: RESOLVED` is set.
- **Evidence:**
  - TL:1142: "Every HALT item below follows the item 6.2 procedure"
  - TL:989: "**6.2 — Log the OQ-1 decision (L3, no HALT)**"
  - TL:1244: "Branch 2: set `status: RESOLVED`, log the Run id in `### Execution Log`, reset the task status"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G2, calibrated MEDIUM (confirmed); debate C-003, consensus rank 10; merge Change 11.
- **Default remediation:** Point the preamble at the TL:194 HALT rule, and require a quote and a named decider in Branch 2 of 7.15 and 14.7 (R-11).
- **[INFERRED] notes:** none.

### Deviation D-12 (F-12): The section 4 edits from D-09 and D-20 land outside every review

- **Severity:** MEDIUM. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:999
- **Mapped tasklist items:** 6.3, 6.4, 6.5 to 6.13
- **Spec section:** DESIGN section 4 (DESIGN:157-221)
- **Finding:** The F-09 remedy (DESIGN:221) and the F-20 remedy (DESIGN:181, DESIGN:196) both edit section 4. Section 4 is outside the 6.3 Context and Output, the 6.4 checks (TL:1005) and every R5 gate input list (TL:1011, TL:1018). As worded, these edits would land with no review.
- **Evidence:**
  - TL:999: "DESIGN sections 7.3, 11, 12 (NFR-014 row), 13, 15.1, the GQ-109 row and the `### Fix cycle 3` table updated."
  - TL:1011: "as edited by item 6.3 (sections 7.3, 11, 12 (NFR-014 row), 13 (D10) and 15.1, the GQ-109 row, and the `### Fix cycle 3` table)"
  - DESIGN:221: "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)"
  - DESIGN:181: "ALLOWED_ORCA (8)"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-018 (interaction_effects, MEDIUM, UNADDRESSED); merge Change 12 (caller ruling (c)). The fix widens the R5 gate inputs, which every later 6.x lens reads. Cross-references D-08, D-09 and D-20.
- **Default remediation:** Add section 4 to the 6.3 Output, the 6.4 checks, the 6.5 to 6.13 inputs, and the R5 and D10 rows (R-12).
- **[INFERRED] notes:** none.

### Deviation D-13 (F-13): A resumed 7.17 HALT has no follow-up item

- **Severity:** MEDIUM. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:1267
- **Mapped tasklist items:** 7.17; the HALT rule at TL:194
- **Spec section:** n/a (the HALT resume rule at TL:194 and TL:1142)
- **Finding:** Branch 2 at TL:1142 only records RESOLVED and resets the status. The existing 7.17 branch halts with "the design needs a fix before step 1.2", but no item carries out that design fix or re-pins the downstream checks, so a resumed HALT has no follow-up item. This is independent of R1-G1; INV-021 is the HIGH case of the same gap and is handled in D-03.
- **Evidence:**
  - TL:1267: "the design needs a fix before step 1.2"` and STOP."
  - TL:1142: "Branch 2 (all four lines filled, the source quoting the owner's words) sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status`"
  - TL:194: "fill `blocker_reason` with the halt line, append the halt line to `### Execution Log`, STOP"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-005 (state_variables, MEDIUM, UNADDRESSED); merge Change 13 (caller ruling (c)). Must not contradict F-03 step 2.
- **Default remediation:** State in the TL:1267 branch what a resume requires, using the same wording as R-03 step 2 (R-13).
- **[INFERRED] notes:** none.

### Deviation D-14 (F-14): The 7.16 forbidden-token grep can fail an honest capture

- **Severity:** MEDIUM. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1262
- **Mapped tasklist item:** 7.16
- **Spec section:** DESIGN section 15.1 (DESIGN:874)
- **Finding:** The forbidden-token grep scans the whole `readonly-probe.md`, but TL:1260 also puts stdout, stderr and a "what it settles" line into that file. Capture item 2 is about whether `run-current` needs `--json`, so an honest note names it, and real Task text can mention stash or inbox. An honest capture can therefore fail the check.
- **Evidence:**
  - TL:1262: `grep -n 'worker-read\|gate-list\|inbox\|include-remote\|stash\|run-current --json' .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md`
  - TL:1260: "the exact command, exit code, stdout and stderr (paths, session ids and user names may be shown in full here, as the file stays in the task package), and what it settles"
  - DESIGN:874: "Whether `run-current` needs `--json` is answered by reading its plain output"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-008 (guard_conditions, MEDIUM, UNADDRESSED); merge Change 14 (caller ruling (c)). The consensus kept only the missing-sentence half (C-007), which does not cover this. Cross-references D-16 and D-03 step 2.
- **Default remediation:** Limit the grep to the recorded command lines (R-14).
- **[INFERRED] notes:** none.

### Deviation D-15 (F-15): With zero Dispatch rows, the Dispatch half of open item 2 stays unverified

- **Severity:** MEDIUM. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:1269
- **Mapped tasklist items:** 7.15, 7.16, 7.17, 8.10
- **Spec section:** DESIGN section 17 open item 2 (DESIGN:970)
- **Finding:** With zero Dispatch rows, 7.16 step (1) learns no ids, template 3 never runs, and capture items 4 and 13 are empty. Open items 1, 6, 22 and 23 and the DISPATCH_ID_RE half of open item 2 stay unverified. The 7.17 HALT text is ambiguous when only the Run sample exists, yet 8.10 needs DISPATCH_ID_RE.
- **Evidence:**
  - TL:1269: "Step 1.0a: no Run or Dispatch id sample; steps 1.4 and 1.6 cannot start (DESIGN 17 item 2)"
  - TL:1260: "Run template 2 (`orca-ide orchestration worker-list --run <run> --json`) once to learn the Dispatch ids"
  - TL:1482: "`RUN_ID_RE`, `DISPATCH_ID_RE`, the cursor field"
  - DESIGN:970: "| 2 | `RUN_ID_RE` and `DISPATCH_ID_RE` | Step 1.0a item 10 | Steps 1.4 and 1.6 do not start; no placeholder can match |"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-015 (collection_boundaries, MEDIUM, UNADDRESSED); merge Change 15 (caller ruling (c)). The consensus covered only "live Orca access assumed" (A-007b).
- **Default remediation:** Require a Run with at least one Dispatch row in 7.15 and an explicit HALT in 7.17 (R-15).
- **[INFERRED] notes:** none.

### LOW

### Deviation D-16 (F-16): The 7.18 grep matches bare "coder", and 7.16 expects a sentence no Action writes

- **Severity:** LOW. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1276
- **Mapped tasklist items:** 7.16, 7.18
- **Spec section:** n/a (tasklist checks)
- **Finding:** The 7.18 grep searches for bare "coder", which also matches longer words such as encoder, so the check can pass or fail for the wrong reason. The 7.16 Verification expects a forbidden-list sentence that the 7.16 Action never tells the executor to write.
- **Evidence:**
  - TL:1276: "`grep -rn '/home/coder\|coder' tests/sweep/fixtures/` returns nothing"
  - TL:1262: "finds only the forbidden-list sentence"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G5 (confirmed); debate C-007, consensus rank 11; merge Change 16. V1's SOURCES.md extension is [INFERRED] and not carried. Cross-reference D-14.
- **Default remediation:** Anchor the 7.18 pattern, and either write the sentence in the 7.16 Action or drop the expectation (R-16).
- **[INFERRED] notes:** none.

### Deviation D-17 (F-17): The 7.16 Verification does not allow the step (6) echo and ls

- **Severity:** LOW. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1262
- **Mapped tasklist item:** 7.16
- **Spec section:** n/a (tasklist check)
- **Finding:** The Verification says every command in the capture file is one of the eight templates or a file read, but Action step (6) runs echo and `ls -la`, which are neither. A literal reader fails the check.
- **Evidence:**
  - TL:1260: "Resolve the tab-map folder with `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"`, record the printed path, then list that folder with `ls -la <printed path>`"
  - TL:1262: "every command in the file is one of the eight templates or a file read"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G6, first sentence only (confirmed); debate C-008, consensus rank 12; merge Change 17. V1's second (agent-wait) sentence was withdrawn.
- **Default remediation:** Reword the 7.16 Verification to allow the step (6) commands (R-17).
- **[INFERRED] notes:** none.

### Deviation D-18 (F-18): Item 7.16 does not name who runs the capture

- **Severity:** LOW. Gap class `design-fix`. Tag [INFERRED].
- **Location:** TL:1249-1263
- **Mapped tasklist item:** 7.16
- **Spec section:** DESIGN section 15.1 (DESIGN:868)
- **Finding:** [INFERRED] The plan does not establish whether the executor running 7.16 is acting as the person or the coordinator that DESIGN 15.1 requires. This asks for the actor to be named; it does not claim an unauthorized actor has run a capture. Whether the executor is the coordinator is unknown, not shown false.
- **Evidence:**
  - DESIGN:868: "It is a manual, pre-implementation capture run by the person or the coordinator, never by a test, and it writes only its own notes file."
  - TL:1249: "Run the step 1.0a read-only Orca capture"
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R2-G8 (confirmed LOW) and R1-G4 (confirmed); debate C-005 (V2 framing preferred at 80%), A-002 and A-002a; merge Change 18. Row INF-017 (partial) points at F-18 and F-19.
- **Default remediation:** Name the coordinator as the capture actor in 7.16, or add a hand-off (R-18).
- **[INFERRED] notes:** the finding itself carries the [INFERRED] tag in the merged verdict; see the Finding line.

### Deviation D-19 (F-19): The INF-017 matrix note cites card F11 instead of F12

- **Severity:** LOW. Gap class `traceability`. Tag Grounded.
- **Location:** coverage-matrix:218
- **Mapped tasklist item:** coverage-matrix INF-017 row
- **Spec section:** n/a
- **Finding:** The INF-017 note points the capture-actor question at Tier-1 card F11, but the actor finding is F12; F11 concerns the R4 historical-section wording.
- **Evidence:**
  - coverage-matrix:218: "who counts as the coordinator is not stated; card F11"
  - reflection-card-t1.yaml:274-276: "- id: F12 / severity: LOW / category: Fidelity question on who runs step 1.0a"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G9 (confirmed); debate C-006 at 95%; merge Change 19.
- **Default remediation:** Correct the INF-017 note to cite F12 (R-19).
- **[INFERRED] notes:** none.

### Deviation D-20 (F-20): The 6.3 count grep misses "(8)" and "8 read", and templates 9 and 10 have no zero-argv pin

- **Severity:** LOW. Gap class `unsound-check`. Tag Grounded.
- **Location:** DESIGN:181
- **Mapped tasklist items:** 6.3, 10.3; DESIGN section 4
- **Spec section:** DESIGN section 4 (DESIGN:181, DESIGN:196)
- **Finding:** The 6.3 grep for `eight\|8 templates` misses DESIGN:181 and DESIGN:196, so the section 4 count can stay stale. No item pins zero argv for templates 9 and 10; item 10.3 pins it only for `worktree list` and `worktree current`. Severity is LOW because 8.10 states "exactly 10", so the code is not misled.
- **Evidence:**
  - DESIGN:181: "ALLOWED_ORCA (8)"
  - DESIGN:196: "8 read templates"
  - TL:1000: "`grep -n 'eight\|8 templates' docs/designs/orchestrator-mode.md` shows no hit that says the allowlist has eight templates"
  - TL:1793: "zero argv for `worktree list` and `worktree current`"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G2 (confirmed); debate C-018 at 95%, re-verified by V1 and V3; merge Change 20; INV-011 and INV-012 confirm LOW. Cross-reference D-12.
- **Default remediation:** Widen the 6.3 grep and add zero-argv assertions for templates 9 and 10 in 10.3 (R-20).
- **[INFERRED] notes:** none.

### Deviation D-21 (F-21): Item 5.11 places section 13 hits in section 14

- **Severity:** LOW. Gap class `traceability`. Tag Grounded.
- **Location:** TL:838
- **Mapped tasklist items:** 5.11, 5.3
- **Spec section:** DESIGN sections 13 and 14 (DESIGN:835, DESIGN:837)
- **Finding:** The 5.11 row text places the draft-name markers in sections 13 and 14, but both hits (D6 and the 1.17 row) are in section 13. Section 14 starts at DESIGN:837.
- **Evidence:**
  - TL:838: "marked the SPEC and REPORT draft names in 13 and 14"
  - DESIGN:837: "## 14. Panel notes carried into the design"
  - DESIGN:835: "| 1.17 | The REPORT's WC-14 draft | The SPEC section 10 text plus D6 (section 8) |"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G4 (confirmed); debate C-019; merge Change 21. Verified by V3 only (single source, Part 4 item 8).
- **Default remediation:** Change "in 13 and 14" to "in 13", and drop 14 from the 5.3 list (R-21).
- **[INFERRED] notes:** none.

### Deviation D-22 (F-22): Item 8.5 does not cite the reflect _git seam it reuses

- **Severity:** LOW. Gap class `traceability`. Tag Grounded.
- **Location:** TL:1447
- **Mapped tasklist item:** 8.5
- **Spec section:** n/a (Source Areas, TL:148)
- **Finding:** Source Areas names the reflect `_git` seam as the pattern, but the 8.5 Context does not cite config.py:64-78. TL:1448 already states `check=False` and `GitCallFailed`, so only the citation is missing.
- **Evidence:**
  - TL:148: "`superclaude.cli.reflect` (the `_git` seam pattern)"
  - TL:1448: "`check=False`; non-zero exit, timeout or output over `OUTPUT_LIMIT` raise `GitCallFailed` with a reason"
  - config.py:64: "def _git(cwd: Path, *args: str) -> str:"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G9 (confirmed), narrowed by V3's own new evidence, with the "missing reuse" framing dropped; debate C-023; merge Change 22.
- **Default remediation:** Cite config.py:64-78 in the 8.5 Context (R-22).
- **[INFERRED] notes:** none.

### Deviation D-23 (F-23): Item 9.1 counts five helpers where DESIGN 7.1 has four

- **Severity:** LOW. Gap class `traceability`. Tag Grounded.
- **Location:** TL:1627
- **Mapped tasklist item:** 9.1
- **Spec section:** DESIGN section 7.1 (DESIGN:438-442)
- **Finding:** Item 9.1 counts five helpers plus `_publish`, but DESIGN 7.1 lists `run`, four helpers and `_publish`. The wrong count invites the executor to invent a fifth helper.
- **Evidence:**
  - TL:1627: "the five helpers and `_publish`"
  - DESIGN:438-442: "def _parse_window ... def _find_root ... def _check_output ... def _check_run_ids ... def _publish"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G10 (confirmed); debate C-024; merge Change 23; INV-013 confirms.
- **Default remediation:** Name the four helpers and `_publish` in 9.1 (R-23).
- **[INFERRED] notes:** none.

### Deviation D-24 (F-24): OQ-16 says no fixture covers templates 9 and 10, but 10.3 has a unit case

- **Severity:** LOW. Gap class `test-plan`. Tag Grounded.
- **Location:** TL:2881
- **Mapped tasklist item:** OQ-16
- **Spec section:** n/a (open-question record)
- **Finding:** OQ-16 says no fixture covers templates 9 and 10, but item 10.3 has a positive unit case for both agent-wait templates. The record contradicts the plan; this is a wording fix.
- **Evidence:**
  - TL:2881: "step 1.0a runs only templates 1 to 8 and no fixture covers templates 9 and 10"
  - TL:1793: "with a positive case that both `worktree ps --agent-wait` templates are accepted"
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G11 (weakened); debate C-025 at 90%; merge Change 24.
- **Default remediation:** Reword OQ-16 to separate the live capture from the unit cases (R-24).
- **[INFERRED] notes:** none.

### Deviation D-25 (F-25): Item 7.16 does not say which fields count as timestamps

- **Severity:** LOW. Gap class `design-fix`. Tag Grounded.
- **Location:** TL:1260
- **Mapped tasklist item:** 7.16
- **Spec section:** DESIGN section 15.1 (DESIGN:875)
- **Finding:** Item 7.16 compares the before and after reads with timestamps removed, but does not say which fields count as timestamps. On a Run with live workers, status, liveness or agentWait can change between the reads and trigger the HALT. The stop is safe, not silent.
- **Evidence:**
  - TL:1260: "Compare before and after outputs with timestamps removed."
  - TL:1262: "If the before and after reads differ apart from timestamps, apply the HALT rule"
  - DESIGN:875: "A difference stops the build and goes to the owner."
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G3, clarification only (weakened); debate C-004; merge Change 25; INV-009 (ADDRESSED). This is not a "no strip rule" claim: TL:1260 and TL:1262 already strip timestamps, and V1 conceded.
- **Default remediation:** Name the fields that the comparison ignores or treats as timestamps (R-25).
- **[INFERRED] notes:** none.

### Deviation D-26 (F-26): Open reading of "every hit justified" for the 168 pre-existing hits

- **Severity:** LOW. Gap class `traceability`. Tag Grounded.
- **Location:** TL:2467-2472
- **Mapped tasklist item:** 14.5
- **Spec section:** DESIGN step 1.28 (DESIGN:939)
- **Finding:** Open reading only: it is unclear whether "every hit justified" covers the 168 pre-existing hits, which item 14.5 checks only by count. Both card mechanisms (base drift and same-count concealment) are defeated. The question is open, and LOW either way.
- **Evidence:**
  - DESIGN:939: "every hit justified"
  - TL:2468: "the full-tree count must stay 168"
  - TL:2471: "re-run the full count at that base reading only"
  - TL:2472: "0 scoped hits and an unchanged full-tree count"
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R1-G9 and R2-G7 (both weakened), merged into one note; debate C-011, X-003 and A-004c; merge Change 26. Base drift is defeated by the recount at the recorded base (TL:2471); same-count concealment is defeated by the scoped check.
- **Default remediation:** State in 14.5 which hits DESIGN:939 covers (R-26).
- **[INFERRED] notes:** none.

### Deviation D-27 (F-27): Re-running 6.3 after step (6) matches the D10 ban quote

- **Severity:** LOW. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:998
- **Mapped tasklist items:** 6.3, 6.4
- **Spec section:** DESIGN section 13 D10 row and the Fix cycle 3 table (both written by 6.3)
- **Finding:** TL:1007 re-runs 6.3 on a FAIL. If step (5) runs again after step (6) has written D10, it matches D10's second cell, which quotes the agent-wait ban as the SPEC text being departed from, and the Fix cycle 3 R5 row.
- **Evidence:**
  - TL:998: "(5) Reword every other DESIGN sentence that says `worktree ps` never carries `--agent-wait`"
  - TL:998: "| D10 | NFR-014 and SPEC lines 310, 500, 504, 562 and 619: \`worktree ps\` never carries \`--agent-wait\` |"
  - TL:1007: "On a FAIL, fix the edit in item 6.3 and re-run this item"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-007 (guard_conditions, LOW, UNADDRESSED); merge Change 27 (caller ruling (c)). The consensus dropped the D10 half of C-021 because a reader sees D10 as history, but that does not cover a re-run. Cross-reference D-10.
- **Default remediation:** Exclude the D10 row and the Fix cycle 3 table from step (5) (R-27).
- **[INFERRED] notes:** none.

### Deviation D-28 (F-28): The 6.3 tuple count can exceed 3 on a correct edit

- **Severity:** LOW. Gap class `unsound-check`. Tag Grounded.
- **Location:** TL:1000
- **Mapped tasklist item:** 6.3
- **Spec section:** DESIGN section 7.3 code block (DESIGN:527) and section 11
- **Finding:** The 6.3 check `grep -c '("worktree", "ps"'` expects 3, but step (3) asks for a section 11 positive case for both agent-wait templates. If that case is written in tuple syntax, the count becomes 4 or 5 and a correct edit fails. Severity is LOW because the executor can avoid it through wording.
- **Evidence:**
  - TL:1000: "`grep -c '("worktree", "ps"' docs/designs/orchestrator-mode.md` prints 3"
  - DESIGN:527: "("worktree", "ps", "--json"),"
  - TL:998: "add a positive case that both `--agent-wait` templates are accepted"
- **Classification:** n/a (UC-1).
- **Classification rationale:** no card and no debate point; invariant probe INV-010 (guard_conditions, LOW, UNADDRESSED); merge Change 28 (caller ruling (c)).
- **Default remediation:** Count only within the DESIGN 7.3 code block (R-28).
- **[INFERRED] notes:** none.

## Gap registry

| ID | Severity | Gap class | Affected items | Coverage rows touched | Recommendation |
|---|---|---|---|---|---|
| F-01 | HIGH | unsound-check | 8.3 | none | R-01 |
| F-02 | HIGH | unsound-check | 6.2 | none | R-02 |
| F-03 | MEDIUM | design-fix | 7.16, 7.17, 8.10, 10.3, DESIGN 7.3, 11, 12, 15.1 | step-1.0a, INF-019, INF-020 | R-03 |
| F-04 | MEDIUM | traceability | Key Constraints | GQ-111, GQ-112, GQ-113, INF-001 | R-04 |
| F-05 | MEDIUM | traceability | 8.5, 8.10, closing follow-ups | SP-28, INF-024 | R-05 |
| F-06 | MEDIUM | test-plan | 8.10, 10.2, 10.5 | INF-005, INF-008, INF-018 | R-06 |
| F-07 | MEDIUM | traceability | 8.12, coverage-matrix | none (no row yet) | R-07 |
| F-08 | MEDIUM | traceability | 6.3 | none | R-08 |
| F-09 | MEDIUM | authorized-expansion | 6.3, DESIGN 4 | none | R-09 |
| F-10 | MEDIUM | unsound-check | 6.3, 6.4 | none | R-10 |
| F-11 | MEDIUM | design-fix | Phase 7 preamble, 7.15, 14.7 | none | R-11 |
| F-12 | MEDIUM | design-fix | 6.3, 6.4, 6.5 to 6.13 | none | R-12 |
| F-13 | MEDIUM | design-fix | 7.17, HALT rule | none | R-13 |
| F-14 | MEDIUM | unsound-check | 7.16 | none | R-14 |
| F-15 | MEDIUM | design-fix | 7.15, 7.16, 7.17, 8.10 | none | R-15 |
| F-16 | LOW | unsound-check | 7.16, 7.18 | none | R-16 |
| F-17 | LOW | unsound-check | 7.16 | none | R-17 |
| F-18 | LOW | design-fix | 7.16 | INF-017 | R-18 |
| F-19 | LOW | traceability | coverage-matrix INF-017 row | INF-017 | R-19 |
| F-20 | LOW | unsound-check | 6.3, 10.3, DESIGN 4 | none | R-20 |
| F-21 | LOW | traceability | 5.11, 5.3 | none | R-21 |
| F-22 | LOW | traceability | 8.5 | none | R-22 |
| F-23 | LOW | traceability | 9.1 | none | R-23 |
| F-24 | LOW | test-plan | OQ-16 | none | R-24 |
| F-25 | LOW | design-fix | 7.16 | none | R-25 |
| F-26 | LOW | traceability | 14.5 | none | R-26 |
| F-27 | LOW | unsound-check | 6.3, 6.4 | none | R-27 |
| F-28 | LOW | unsound-check | 6.3 | none | R-28 |

## Not carried

The merge dropped or narrowed these items (21 entries, from `not_carried` in the merged verdict):

- R1-G7 (9.3 does not read OQ-8 or halt): refuted by calibration and withdrawn by V1 in both rounds (C-009, U-010). INV-019 confirms no later item relies on it.
- R1-G8 and R3-G3 (the template count in the Key Constraints line is wrong): the wording is accurate, or at worst ambiguous; both claimants withdrew (C-010, A-003).
- R3-G8 (edit the D6 row to cite SPEC lines): superseded by item 5.4, which already cites those lines and forbids other D6 edits (C-022).
- R3-G5 second remedy (add agent-wait to the capture): withdrawn by V3 (C-020). Only the DESIGN:221 rewording survives, as F-09.
- R3-G6 D10 half: conceded, because a reader sees D10 as history (C-021). The re-run risk is carried separately as F-27 (INV-007).
- R1-G6 second sentence (agent-wait): withdrawn by V1 (C-008). The first sentence survives as F-17.
- R2-G5 `run-current` narrowing, and V2's covered-in-substance verdict for INF-019: V2 conceded that its delegation reading covers only the STILL UNVERIFIED path (X-001, X-005). INF-019 becomes partial, and the cursor half of R2-G5 is folded into F-03.
- The gate-bypass label on R1-G1: dropped by consensus in favour of describing the outcomes as unrouted (A-001).
- V2's original HIGH labels on R2-G2, R2-G3, R2-G4, R2-G5 and R2-G7: calibrated to MEDIUM or LOW, because each card text says correct delivery is not blocked (X-002, X-004, A-009).
- R1-G9 base-drift mechanism and R2-G7 same-count mechanism: defeated (C-011, X-003, A-004). Only the open reading of DESIGN:939 survives, as F-26.
- V1's SOURCES.md extension of R1-G5: [INFERRED] and not checked by any grep (C-007).
- V1's 41 failed second refs and two "Section 8 gate" refs: they failed calibration and V1 conceded (S-004). V1's row verdicts are kept and these refs are discarded.
- "R2-G1 is the only HIGH of the run": wrong after INV-006 (F-02).
- INV-006's other two fixes (grep under the heading and expect 2; drop the append): the first still counts the build-time row, and the second leaves 6.2 with no action to check. The anchored-row check in F-02 is used instead.
- Raising F-03 to HIGH because of INV-021: the plan defect is a stall, not wrong code shipped (X-002). INV-021 is cleared by widening the remedy instead.
- INV-004 (the 6.1 `grep -c` counts lines, not distinct parts): ADDRESSED, LOW; the decision file is complete today.
- INV-001 (the Fix cycle 3 table and its row order): ADDRESSED, LOW, no gap.
- INV-002 (the deviation total is 9 before 6.3 and 10 after it): ADDRESSED, LOW, no gap. Review note N-05: the Phase 5 pin is in item 5.8, not 5.10; the conclusion holds.
- INV-017 (zero-hit greps and an unavailable Orca): ADDRESSED, LOW, no gap.
- Ranking the card grades 4, 3 and 4 against each other: the cards use different scales, and the merged grade is set fresh on V3's written scale (A-007, S-008).

## Best-practice grade

**Grade: 3 of 5** on V3's written scale (0 = unusable, 5 = executable as written with no rework; S-008). Card grades V1 4, V2 3 and V3 4 are recorded but not ranked (A-007). The card grades of 4 were set before INV-006 was found.

Reasons (from the merged verdict):

- Plus: owner gates and HALT rules are explicit, and the R5 edit has its own review gate.
- Plus: the design-fix items anchor on headings and pinned counts.
- Minus: two checks fail correct work (F-01, F-02), so the plan needs rework before it can run as written.
- Minus: an owner approval at step 1.0a has no follow-up path today (F-03, INV-021).

**Calibrated confidence: 0.77**, the mean of the three calibrated card confidences: V1 0.71, V2 0.81 and V3 0.79 (2.31 / 3 = 0.7700). F-01 comes from one card and was confirmed by all three advocates. F-02 comes from the probe alone, but its evidence is mechanical: a grep count re-checked by both the orchestrator and the merge executor. The Tier-1 card was calibrated at 0.82 and escalated.

## Evidence-validator results

Mode `full_reread` (depth deep). 105 distinct cited ranges re-Read: 105 revalidated, 0 dropped, 0 corrected, 0 INF rows dropped. Full result: `evidence-validation.yaml`. No grounding gap was raised, so the Grounding Gaps heading is removed as the template requires.

A zero-drop pass is treated as suspect (section 11.2), so it is logged with `zero-drop-flag: true`. The validator re-checked the riskiest claims and recorded a self-audit:

| Check | Result |
|---|---|
| D-02 (F-02) | `OQ-1 (R5) RESOLVED` occurs on exactly TL 991, 993 and 2802; the anchored 6.2 row pattern matches 0 lines today |
| D-01 (F-01) | TL:1433, TL:1436 and the repeated names at DESIGN:454, 459 and 466 confirmed |
| D-03 (F-03) | TL:1142, 1259, 1262, 1267, 1482, 1485 and 1793, and DESIGN:550, 552, 971 and 973 confirmed |
| INF rows | all 26 quotes match their DESIGN lines |
| D-08 [INFERRED] SPEC lines | merged-requirements.md lines 132, 143, 310, 323, 500, 504, 510, 562 and 619 all carry the agent-wait text; NFR-003 on 132 and NFR-014 on 143 confirmed |

The validator did not recount the 105 ranges independently; it re-read every range it met and carried the report's own count.

## Inferred-claim audit

- `citations_inferred: 3` (the D-18 finding, the D-08 SPEC line-number note, and the coverage caveat about 21 V3 rows)
- Inferred fraction: `3 / 105` = 0.03

The WARN block is not triggered: inferred claims are far below half of all citations.

## Recommendations

R-nn matches D-nn. R-29 is the cross-cutting P0 recommendation, so it sits at the end of the P0 band.

### Recommendation R-01: Count definitions, not occurrences, in 8.3

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Replace the occurrence-count clause in item 8.3 (TL:1436) with a definition-count check, using anchored class declarations and constant assignments or an AST inspection. Count constants by their definition too (for example `^CLASSES =`), not only `^class`. Note that `^class Classification` does not prefix-match `ClassifiedRow`. The four field greps at TL:1436 stay at 1 each.
- **Verifier:** Re-Read TL:1436 to confirm the definition-count wording. Success: the check requires one definition per name and still allows references to those names in annotations, so a conforming `models.py` passes.
- **Linked deviation(s):** D-01
- **Priority:** P0

### Recommendation R-02: Append a 6.2 table row and count only that row

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Make the two edits to item 6.2 (TL:991, TL:993) exactly as the merged verdict words them:

```text
Two edits to item 6.2:
  1. Action: append one row to the `### Execution Log` table in its four-column form (`| <timestamp> | 6.2 | <event> | OQ-1 (R5) RESOLVED by the owner 2026-11-08: ... |`), as the TL 2804 rule requires for every owner decision, instead of a bare line.
  2. Verification: count only appended Execution Log table rows whose Item column is 6.2, for example `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED' <TL>` returns 1. The leading-pipe anchor excludes TL 991 and TL 993 (they start with "  - **"), and the Item-column anchor excludes TL 2802 (its Item cell is `6.1-6.4`).
Success test: before 6.2 runs the command prints 0; after one correct append it prints exactly 1; a second append prints 2 and fails.
```

  Check command, exact copy: `grep -c '^| [^|]* | 6\.2 | .*OQ-1 (R5) RESOLVED' <TL>`

  Notes from the merged verdict: run the pattern with plain grep (basic regex), never `grep -E`; under `-E` the leading `^|` becomes an empty alternative and matches every line. The appended row must put a space on each side of every pipe; a row written as `|...|6.2|...|` gives 0. Review note N-04: keep the example row inline in the Action text (on its own line starting with `|`, a correct append would count 2), and change the 6.2 Output field (TL:992) from "line" to "row". Review note N-06: read "as the TL 2804 rule requires" as "in the four-column row form TL 2804 uses".
- **Verifier:** Run the check command against the TL: it prints 0 before 6.2 runs and exactly 1 after one correct append. The orchestrator confirmed 0 today and 1 on a temporary copy.
- **Linked deviation(s):** D-02
- **Priority:** P0

### Recommendation R-29: Re-run the pre-execution reflection after the P0 fixes

- **File:** n/a
- **Change:** After R-01 and R-02 land, run `/sc:reflect --mode pre --depth deep` again on the same spec and tasklist, and let the Wave 5 evidence-validator finish.
- **Verifier:** The new merged verdict has no HIGH finding, `convergence_status` is not BLOCKED_BY_INVARIANTS, and the evidence-validator results are recorded.
- **Linked deviation(s):** none
- **Priority:** P0
- **Provenance:** an orchestrator synthesis addition (Wave 5), as in run 1, not a merged-verdict finding.

### Recommendation R-03: Route both step 1.0a outcomes to the owner and name the follow-up

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Edit item 7.17 (TL:1265-1269) with this branch wording, copied exactly from the merged verdict:

```text
Recommendation, in this order:
  1. Add a named branch to item 7.17 covering both outcomes, (a) a cursor field captured and (b) open item 3 CLOSED with `run-current` needing `--json`. The branch first writes a decision file `phase-outputs/plans/OQ-<n>-<topic>-decision.md` under the task folder (`<n>` the next unused OQ number) in the TL 1142 form: `needs_human_decision: true`, `status: PENDING`, the question quoted, the options quoted, the recommendation line and the steps it blocks, and the empty block `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`. It then appends one PENDING row for item 7.17 to the `### Execution Log` table (TL 2804), naming the decision file, and HALTs before step 1.2 under the TL 1142 Branch 1 rule (PENDING or empty `Chosen:`).
  2. In the same branch, state what an owner approval triggers. Either (option A) name the follow-up work: a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate; the 8.10 and 10.3 count source changed from the literal 10 to the approved count recorded in the 1.0a facts file; the 7.16 forbidden list and its grep (TL 1259, TL 1262) updated to allow the approved argv and a re-capture of it; and a re-run of the R5 review gate (6.5 to 6.22) over the new edit. Or (option B) state that an approval means re-planning before step 1.2, and that no later item runs until the plan is rebuilt.
  3. An owner answer, approval or refusal, is recorded by filling the four lines of the step 1 decision file (`Chosen:`, `Decided by:`, `Decision source:` quoting the owner's words, and `OPERATOR DECISION:`). The resume then follows the TL 1142 Branch 2 rule over that file: it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to Doing as TL 1142 states, and clears `blocker_reason`. An approval resumes into the step 2 follow-up. A refusal resumes with the allowlist unchanged, and the same step records the refusal in `phase-outputs/discovery/1.0a-facts.md` as "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies". This matters because 8.10 reads "From the 1.0a facts: ... the cursor field" (TL 1482): with that line recorded, 8.10 keeps `ALLOWED_ORCA` at exactly 10 (TL 1482, TL 1485), does not page by the captured cursor field, and treats a full page of `WORKER_LIST_PAGE` rows as truncated with a lower-bound total (DESIGN 973). The refusal path is justified by INV-021's own sentence "If the owner declines, the plan works", not by INV-016, which covers only the separate case where step 1.0a finds no cursor field.
Success test: a grep of item 7.17 finds the new branch naming both outcomes; the decision file path `phase-outputs/plans/OQ-<n>-<topic>-decision.md` with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines; the PENDING Execution Log row; the HALT before step 1.2; a resume step that names that decision file; the refusal line for `1.0a-facts.md`; and either the four follow-up targets (DESIGN edit, 8.10 and 10.3 count source, 7.16 forbidden list, review re-run) or the re-planning sentence. When the branch fires, the check confirms that the decision file exists with `status: PENDING`, that the Execution Log holds exactly one PENDING row for item 7.17 naming that file, and that the task is halted (status and `blocker_reason` set by the HALT rule) before any step 1.2 item runs. No consumer listed in INV-021 is left pinned to ten templates with no named updater.
```

  Review notes from the merged verdict, to apply together with the branch:
  - N-01: the HALT rule at TL:194 already appends the halt line to the Execution Log, so a firing branch leaves two 7.17 rows. Either count the HALT row in "exactly one PENDING row", or drop step 1's own row. Name a `blocker_reason`, for example `"Step 1.0a: <outcome> needs an owner allowlist decision; see phase-outputs/plans/OQ-<n>-<topic>-decision.md (PENDING)"`. End the recommendation line with "This recommendation does NOT authorize adoption." as TL:1142 requires.
  - N-02: for outcome (b), record the refusal as "`run-current` needs `--json`; owner declined; the DESIGN 971 behaviour applies: FR-002 fourth test and FR-026 case 4 stay gated".
  - N-03: when both outcomes fire, write one decision file per outcome, each with its own OQ number and PENDING row. The next unused number is OQ-17.
- **Verifier:** The success test in the block above.
- **Linked deviation(s):** D-03, D-13 (keep the step 2 wording identical)
- **Priority:** P1

### Recommendation R-04: Carry the DESIGN section 2.3 rule into Key Constraints

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Add one Key Constraints bullet (TL:157-167) that carries DESIGN section 2.3: never edit REPORT; use GAPS line 138 for gaps counts; keep the 113/88/25 figures and the GQ-113 interpretation.
- **Verifier:** `grep -c 'GAPS line 138'` on the TL returns 1, and the hit sits inside Key Constraints. A reader can find the complete rule without opening DESIGN.
- **Linked deviation(s):** D-04
- **Priority:** P1

### Recommendation R-05: Mark the byte limits proposed and carry open item 19

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (items 8.5, 8.10 and the closing follow-ups)
- **Change:** Add the "proposed" marking to the limit declarations delivered by 8.5 and 8.10 (TL:1482-1486), with a source-content check that covers every relevant declaration. Carry open item 19 into the closing follow-ups unless its rationale is recorded in the task package. Keep 23 open items, or update all four pins (TL:269, TL:454, TL:784, TL:1005) in the same edit.
- **Verifier:** After 8.10, a grep of `src/superclaude/cli/sweep/probes.py` finds a "proposed" marking on each limit declaration. The closing record either cites the rationale or keeps the before-release obligation, and the four pins still agree with DESIGN:993.
- **Linked deviation(s):** D-05
- **Priority:** P1

### Recommendation R-06: Add checks for the probes.py boundary, B5 and the renderer bans

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (items 8.10, 10.2, 10.5)
- **Change:** Extend the AST boundary check (TL:1787) to `probes.py` and its full set of import restrictions (DESIGN:211). For B5 (DESIGN:219), add a bounded type-declaration comparison or a documented source review instead of banning imports of `superclaude.contracts`. Add a renderer-content check for all three section 7.5 prohibitions (DESIGN:638).
- **Verifier:** Each of the three constraints has a named delivering item and a check whose failure condition tests that constraint directly. Re-Read 10.2 and 10.5 to confirm.
- **Linked deviation(s):** D-06
- **Priority:** P1

### Recommendation R-07: Add a coverage row for the set-union wording

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/coverage-matrix.yaml` and the TL (item 8.12)
- **Change:** Add an inferred row for DESIGN:636, map it to 8.12, and name the set-union rule in the 8.12 delivery or acceptance text.
- **Verifier:** `grep -n 'set union'` on the coverage matrix returns the new row, and a re-Read of 8.12 shows the rule. A reader can trace DESIGN:636 to a delivering item without relying on the FR-011 ordering row.
- **Linked deviation(s):** D-07
- **Priority:** P1

### Recommendation R-08: Complete the D10 cells and the step (7) list

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** In 6.3 (TL:998), change the D10 SPEC cell to name NFR-003 (line 132), NFR-014 (line 143) and SPEC lines 310, 323, 500, 504, 510, 562 and 619. Add "the NFR-014 exact-set pin covers ten templates, not eight" to the Design cell. Set the Section cell to "2.2, 4, 7.3, 11, 12, 15.1" and the step (7) list to "(2.2, 4, 7.3, 11, 12, 13, 15.1)".
- **Verifier:** Re-Read TL:998 and TL:999 to confirm the four cell and list values.
- **Linked deviation(s):** D-08, D-12
- **Priority:** P1

### Recommendation R-09: Reword DESIGN:221 to accept a recorded owner decision

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (item 6.3, which edits `docs/designs/orchestrator-mode.md`)
- **Change:** Add a 6.3 step that rewords DESIGN:221 to "only after a capture or a recorded owner decision (R5, 2026-11-08)".
- **Verifier:** After 6.3 runs, a grep of DESIGN for "recorded owner decision (R5, 2026-11-08)" returns the section 4 sentence. Review it under R-12.
- **Linked deviation(s):** D-09, D-12
- **Priority:** P1

### Recommendation R-10: Write an allowing agent-wait sentence into 15.1

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** In 6.3 step (4), write the TL:1259 sentence into 15.1: "`worktree ps --agent-wait` is allowed by R5 but is not run in step 1.0a", so the 6.4 rule (TL:1005) has a 15.1 hit to match.
- **Verifier:** After 6.3, an agent-wait grep of DESIGN 15.1 returns that sentence, and 6.4 passes without a TL:1007 fix loop.
- **Linked deviation(s):** D-10
- **Priority:** P1

### Recommendation R-11: Point the Phase 7 preamble at the HALT rule and tighten Branch 2

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Point the TL:1142 preamble at the QA Gate Protocol HALT rule (TL:194) or at its own Branch text, not at item 6.2. In 7.15 (TL:1244) and 14.7, make Branch 2 require a quote of the owner's or person's own words and a named decider before `status: RESOLVED` may be set.
- **Verifier:** Re-Read TL:1142 to confirm no "item 6.2 procedure" pointer remains, and re-Read Branch 2 of 7.15 and 14.7 to confirm the quote and decider clauses.
- **Linked deviation(s):** D-11
- **Priority:** P1

### Recommendation R-12: Put section 4 under the 6.3 to 6.13 reviews

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Add section 4 (DESIGN:157-221) to the 6.3 Output (TL:999), the 6.4 checks (TL:1005) and the 6.5 to 6.13 input lists (TL:1011, TL:1018), and list section 4 in the R5 row and the D10 row.
- **Verifier:** A grep of 6.3, 6.4, TL 1011 and TL 1018 finds "section 4" (or "4,") in each list.
- **Linked deviation(s):** D-12, D-09, D-20, D-08
- **Priority:** P1

### Recommendation R-13: State what a resumed 7.17 HALT requires

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** In the existing TL:1267 branch, state what a resume requires: a named DESIGN edit item with its own gate, or re-planning before step 1.2, using the same wording as R-03 step 2 so the two branches agree.
- **Verifier:** Re-Read TL:1267 and the new R-03 branch; both name the same follow-up or the same re-planning sentence.
- **Linked deviation(s):** D-13, D-03
- **Priority:** P1

### Recommendation R-14: Grep only the recorded command lines in 7.16

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Limit the 7.16 forbidden-token grep (TL:1262) to the recorded command lines of `readonly-probe.md`, not its stdout, stderr or "what it settles" text.
- **Verifier:** An honest capture whose notes mention `run-current --json` passes, and a recorded command line that uses a forbidden token fails.
- **Linked deviation(s):** D-14, D-16
- **Priority:** P1

### Recommendation R-15: Require a Dispatch row and HALT when its sample is missing

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Make item 7.15 name a Run with at least one Dispatch row, and make 7.17 treat a missing Dispatch sample as an explicit open-item-2 HALT (TL:1269).
- **Verifier:** Re-Read 7.15 for the Dispatch-row requirement, and TL:1269 for a HALT that names the Dispatch sample separately from the Run sample.
- **Linked deviation(s):** D-15
- **Priority:** P1

### Recommendation R-16: Anchor the 7.18 grep and align the 7.16 sentence check

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Anchor the 7.18 pattern (TL:1276) with word boundaries or the full path segment. Either add the forbidden-list sentence to the 7.16 Action, or drop that expectation from TL:1262.
- **Verifier:** By reading: the 7.18 pattern is anchored, and every string 7.16 greps for is written by an Action step.
- **Linked deviation(s):** D-16
- **Priority:** P2

### Recommendation R-17: Allow the step (6) commands in the 7.16 Verification

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Reword the 7.16 Verification (TL:1262) to allow "an Orca template from the allowlist, a file read, or the step (6) echo and ls on the tab-map path".
- **Verifier:** By reading: every command in the 7.16 Action (TL:1260) is allowed by the Verification sentence.
- **Linked deviation(s):** D-17
- **Priority:** P2

### Recommendation R-18: Name the 7.16 capture actor

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Add one sentence to 7.16 (TL:1249) naming the coordinator as the capture actor, or a hand-off to the person or coordinator as item 14.8 Branch B does.
- **Verifier:** The actor restriction in DESIGN:868 can be checked from the item text alone.
- **Linked deviation(s):** D-18
- **Priority:** P2

### Recommendation R-19: Fix the INF-017 card reference

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre-run2/coverage-matrix.yaml`
- **Change:** Change "card F11" to "card F12" in the INF-017 note (coverage-matrix:218), and refresh its copied brief excerpt.
- **Verifier:** `grep -n 'card F12'` on the matrix returns the INF-017 row, which resolves to reflection-card-t1.yaml:274-276.
- **Linked deviation(s):** D-19
- **Priority:** P2

### Recommendation R-20: Widen the 6.3 count grep and pin zero argv for templates 9 and 10

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Widen the 6.3 grep (TL:1000) so it also catches "(8)" and "8 read", for example `'eight\|(8)\|8 read\|8 templates'`, and add zero-argv assertions for templates 9 and 10 to 10.3 (TL:1793).
- **Verifier:** After 6.3, the widened grep shows no hit saying the allowlist has eight templates, including DESIGN:181 and DESIGN:196. A re-Read of 10.3 shows zero-argv cases for both agent-wait templates.
- **Linked deviation(s):** D-20, D-12
- **Priority:** P2

### Recommendation R-21: Correct the 5.11 section list

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Change "in 13 and 14" at TL:838 to "in 13", and remove 14 from the 5.3 section list, unless a section 14 hit is shown.
- **Verifier:** Re-Read TL:838 and item 5.3.
- **Linked deviation(s):** D-21
- **Priority:** P2

### Recommendation R-22: Cite the reflect _git seam in 8.5

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Cite config.py:64-78 in the item 8.5 Context (TL:1447) as the seam shape that is reused.
- **Verifier:** `grep -n 'config.py:64-78'` on the TL returns the 8.5 Context line.
- **Linked deviation(s):** D-22
- **Priority:** P2

### Recommendation R-23: Name the four helpers in 9.1

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Change TL:1627 to "the four helpers (_parse_window, _find_root, _check_output, _check_run_ids) and _publish".
- **Verifier:** Re-Read TL:1627 against DESIGN:438-442.
- **Linked deviation(s):** D-23
- **Priority:** P2

### Recommendation R-24: Reword OQ-16

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Reword OQ-16 (TL:2881) to "no live capture covers templates 9 and 10; the allowlist test in item 10.3 covers them as unit cases".
- **Verifier:** Re-Read TL:2881 and confirm it agrees with TL:1793.
- **Linked deviation(s):** D-24
- **Priority:** P2

### Recommendation R-25: Name the fields the 7.16 comparison ignores

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Name the fields (for example status, liveness, agentWait) that the before-and-after comparison at TL:1260 ignores or treats as timestamps.
- **Verifier:** Re-Read TL:1260 and TL:1262 and confirm the field list.
- **Linked deviation(s):** D-25
- **Priority:** P2

### Recommendation R-26: State the scope of "every hit justified" in 14.5

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** State in item 14.5 (TL:2467-2472) whether DESIGN:939 applies to the 168 pre-existing hits or only to new ones, and keep the scoped zero-hit check as it is.
- **Verifier:** Re-Read 14.5 and confirm the sentence.
- **Linked deviation(s):** D-26
- **Priority:** P2

### Recommendation R-27: Exclude the D10 row and the Fix cycle 3 table from step (5)

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** In 6.3 step (5) (TL:998), exclude the section 13 D10 row and the Fix cycle 3 table.
- **Verifier:** Re-Read TL:998 for the exclusion. A re-run of 6.3 after a TL:1007 FAIL leaves D10's quoted ban unchanged.
- **Linked deviation(s):** D-27, D-10
- **Priority:** P2

### Recommendation R-28: Count tuples only in the DESIGN 7.3 code block

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Limit the 6.3 tuple count (TL:1000) to the DESIGN 7.3 code block.
- **Verifier:** Re-Read TL:1000 for the scoped count. A section 11 positive case written in tuple syntax does not change the result of 3.
- **Linked deviation(s):** D-28
- **Priority:** P2
