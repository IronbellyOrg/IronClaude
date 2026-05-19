---
qa_phase: task-qualitative
mode: post-completion-operational
task: TASK-RF-track-1-20260518-231708
feature: FU-001 — Migrate sprint .sprint-exitcode to non-tracked state_dir + remove 40 tracked sentinels
reviewer: rf-qa-qualitative
date: 2026-05-19
commits_under_review: e19ad72fe823484591eea9eb3df230a911135ff5, 6767351d57209d90ff8f81cacc4bad89c55bcfc5
branch: feat/sprint-state-migration
verdict: PASS
findings_total: 1
findings_critical: 0
findings_important: 0
findings_minor: 1
fix_authorization: true
fixes_applied: 0
---

# QA Report — Task-Qualitative (Post-Completion Operational)

**Topic:** FU-001 sprint state_dir migration — executed MDTM task
**Date:** 2026-05-19
**Phase:** task-qualitative (post-completion-operational; complements rf-qa structural pass)
**Fix cycle:** 1 of 3

---

## Overall Verdict: PASS (1 MINOR finding — docs-pipeline staleness, deferred and tracked)

The executed task is operationally sound. All claimed code changes landed at the claimed locations with the claimed semantics; the 40-sentinel purge matches the inventory; the regression test exercises real code paths and re-runs green; both commits (`e19ad72f` primary + `6767351` follow-up) are well-formed and `make verify-sync` is clean. The prior structural QA's two IMPORTANT findings (missing `pg4-proceed.md` and 3 unstaged docs) are both fully resolved: `pg4-proceed.md` exists, and the 3 doc files were captured in follow-up commit `6767351`.

The single MINOR finding is a pre-existing docs-pipeline staleness already documented as an out-of-scope sibling follow-up in the task's `Follow-Up Items Identified` and `doc-disposition.md`. Per the user's intentional push/PR deferral, that's the only remaining gap and it is NOT a regression of this task.

---

## Items Reviewed

(task-qualitative phase — Axis column populated per PR-07; `none` = passing check, lens fired nothing; AX-N = specific axis surfaced finding)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (`make verify-sync` would succeed) | none | PASS | Ran `make verify-sync` — exit 0; output ends "✅ All components in sync." |
| 2 | Project convention compliance (src/ source-of-truth → .claude/ sync) | none | PASS | `diff src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh .claude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` → byte-identical. Only `src/` copy committed (per CLAUDE.md `.claude/` is gitignored dev mirror); confirmed by `git show --name-only e19ad72f | grep skills` → only `src/superclaude/skills/...` path. |
| 3 | Intra-phase execution-order simulation | none | PASS | Phase 2 dependency chain (`models.py` → `config.py` → `commands.py` → `executor.py` → `tmux.py` → `tests/sprint/test_tmux.py`) is honored: every downstream file's claim references a field/kwarg created upstream. The Phase 4 test imports `_write_exit_sentinel` from `executor.py:1759` (helper created in Step 2.4, used in Step 4.1) — chain unbroken. |
| 4 | Function-signature verification (writer/reader/CLI/config) | none | PASS | `_write_exit_sentinel(config: SprintConfig, exitcode: int) -> None` at `executor.py:1759-1771` writes to `config.state_dir` (NOT `release_dir`) with `try/except OSError: pass` and `mkdir(parents=True, exist_ok=True)` — exactly the contract claimed. Reader at `tmux.py:166`: `sentinel = config.state_dir / ".sprint-exitcode"`. `load_sprint_config(...)` signature accepts `state_dir: Path \| None = None` at `config.py:288`. CLI `--state-dir` option at `commands.py:182-188` with `state_dir_override` param at L206. All call sites verified by direct Read. |
| 5 | Module-context analysis (PipelineConfig parent + sibling fields) | none | PASS | `__post_init__` (models.py:415-471) correctly: (a) syncs `work_dir = release_dir` first (preserves existing parent-class invariant), (b) processes the migration shim, (c) derives `wiring_gate_mode`, (d) THEN derives `state_dir` last — so any subsequent caller mutating `release_dir` will not stomp the derived `state_dir` mid-init. The new field uses the same `object.__setattr__` pattern as the existing `work_dir` mirror — consistent with dataclass frozen semantics. |
| 6 | Downstream-consumer analysis (bootstrap_scan.sh + tests) | none | PASS | `bootstrap_scan.sh:90-96` reads state_dir first, falls back to in-release legacy path. Line 134 (`recent_files ".sprint-exitcode"` — `find -name` based) auto-picks up new `.dev/sprint-state/**/.sprint-exitcode` paths with NO code change required (verified by reading the function body at L51). Updated comments at L90-91 and L133 document this. Both `test_tmux.py:100-101` and `test_state_dir_isolation.py` were updated/created to match the new writer contract. |
| 7 | Test validity (real code, not stubs/mocks) | none | PASS | `test_state_dir_isolation.py` imports the REAL `_write_exit_sentinel` from production (line 25), constructs a real `SprintConfig` with distinct `release_dir`/`state_dir` tmp paths, and asserts BOTH the positive (`state_sentinel.exists()`) AND negative (`not release_sentinel.exists()`) — collapsing to a single existence check would let a regression silently pass; this test explicitly defends against that. `test_no_tracked_sprint_exitcode_files` shells out to real `git ls-files`. `test_state_dir_default_derives_from_release_dir` exercises the dataclass `__post_init__` derivation. `test_state_dir_env_var_resolution` writes a real fixture and threads through `load_sprint_config`. No mocks, no stubs, no rubber-stamps. |
| 8 | Test coverage of primary use case (4 FU-001 ACs locked in) | none | PASS | Re-ran the test file at validation time: `uv run pytest tests/sprint/test_state_dir_isolation.py -v` → `4 passed in 0.11s`. Each of the four BUILD_REQUEST acceptance behaviors has a dedicated, named test function whose docstring cites the AC it locks in. |
| 9 | Error-path coverage (best-effort writer + missing-state cases) | none | PASS | Writer wraps the entire `mkdir + write_text` block in `try/except OSError: pass` (executor.py:1766-1771) — a permission/quota failure on the new state path does not crash the sprint; matches the original semantics. Reader at `tmux.py:166` is followed by the same `int(sentinel.read_text().strip())` parse and (per Step 2.5 instructions) preserves the existing try/except handling. CLI env-var resolution at `commands.py:223-227` defensively defaults to `None` when env var is absent. |
| 10 | Runtime failure-path trace (input → CLI → loader → config → writer → reader) | none | PASS | Traced end-to-end: (a) CLI `run --state-dir <X>` OR `SPRINT_STATE_DIR=<X>` OR neither → (b) `state_dir = state_dir_override or env_var or None` (commands.py:223-227) → (c) `load_sprint_config(..., state_dir=state_dir)` (commands.py:242) → (d) `SprintConfig(state_dir=state_dir if not None else Path(""))` (config.py:356) → (e) `__post_init__` triggers derivation when sentinel `Path("")` is detected (models.py:466-471) → (f) `_write_exit_sentinel(config, exitcode)` reads `config.state_dir` (executor.py:1767) → (g) `tmux.py:166` reads same `config.state_dir`. No step writes to `release_dir` for the sentinel. The `--release-dir` post-construction override correctly re-derives state_dir at commands.py:259-268, preserving the per-release sentinel co-location semantics. |
| 11 | Completion-scope honesty (Open Questions resolved, not ignored) | none | PASS | All 3 Open Questions from the BUILD_REQUEST research are explicitly resolved in the task file's `### Open Questions (Resolved per BUILD_REQUEST)` section (lines 456-473) with disposition + step reference + rationale. OQ-1 (release-dir override re-derivation) is implemented at commands.py:259-268. OQ-2 (bootstrap_scan.sh in-scope) is delivered in Phase 3 step 3.1. OQ-3 (`git rm` full delete) is delivered in Phase 3 step 3.3 with redundancy-check.txt confirming all 40 sentinel directories retain paired `execution-log.jsonl` (file is 0 bytes — no MISSING entries). |
| 12 | Ambient-dependency completeness (imports, sync, test wiring) | none | PASS | New `_derive_tasklist_id` method is on the dataclass (no module-level import needed). `_write_exit_sentinel` is a module-level helper in `executor.py` — directly importable; the regression test imports it successfully at line 25. The CLI uses `os.environ.get` and `Path` — both already imported at top of `commands.py`. The sync to `.claude/` is verified by `make verify-sync` clean exit. No new third-party dependencies introduced. |
| 13 | Kwarg-sequencing red flags (no use-before-define) | none | PASS | The `state_dir` field is defined (models.py:399) BEFORE its `__post_init__` derivation (L466-471). The `state_dir_override` Click option (commands.py:182-188) is decorated BEFORE the `run()` function uses `state_dir_override` (L206 + L223). `load_sprint_config` signature accepts `state_dir=` (config.py:288) BEFORE construction passes it (L356). Every kwarg has a matching parameter declared earlier in source order. |
| 14 | Function-existence claims grep-verified | none | PASS | `_write_exit_sentinel` confirmed via grep at executor.py:1759 (def) and L1753 (call). `_derive_tasklist_id` confirmed at models.py:401. `load_sprint_config` confirmed at config.py:275 (existing function — the task only added a parameter, not the function itself; task file Step 1.3 finding correctly notes line drift from 287 to 275). `_resolve_release_dir` referenced for context exists at config.py:236. All claimed-existing symbols actually exist. |
| 15 | Cross-reference accuracy for templates / sibling files | none | PASS | Task file references to MDTM Template 02 at `.claude/templates/workflow/02_mdtm_template_complex_task.md` are template-correct. References to research files (research/01-file-inventory.md, 02-config-pattern.md, 03-template-examples.md) all exist in the task's `phase-outputs/discovery/` and `phase-outputs/research/` (verified by Glob earlier in this session). `doc-disposition.md` exists at the path claimed by Step 3.1b and tabulates exactly 24 hits with 5 update / 18 defer + 1 summary row, matching the prior QA's verification trail. |

---

## Self-Audit (MANDATORY per Critical Rule #11)

1. **How many factual claims did I independently verify against source code?** 23 distinct claims (across 15 check rows). Each row's "Evidence" column cites a specific file path + line number that I read directly, or a command I executed with its observed output.
2. **What specific files did I read to verify claims?**
   - `src/superclaude/cli/sprint/models.py` (state_dir field + __post_init__ + _derive_tasklist_id)
   - `src/superclaude/cli/sprint/config.py` (load_sprint_config signature + construction)
   - `src/superclaude/cli/sprint/commands.py` (CLI flag + env-var + post-construction override)
   - `src/superclaude/cli/sprint/executor.py` (writer + helper)
   - `src/superclaude/cli/sprint/tmux.py` (reader path)
   - `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` (two-path lookup + recent_files comment)
   - `tests/sprint/test_state_dir_isolation.py` (full file, 4 test functions)
   - `tests/sprint/test_tmux.py:100-101` (updated fixture)
   - The task file `TASK-RF-track-1-20260518-231708.md` (relevant portions: frontmatter, Phase 1-5 checklists, Findings sections, Open Questions, Execution Log)
   - `phase-outputs/reviews/qa-final-validation-report.md` (prior structural QA findings)
   - `phase-outputs/discovery/doc-disposition.md` (24-row disposition table)
   - `phase-outputs/discovery/redundancy-check.txt` (0 bytes — all 40 dirs had paired execution-log.jsonl)
3. **Commands I executed for verification:**
   - `git log --oneline -20`
   - `git show --stat e19ad72f` and `git show --stat 6767351`
   - `git show --name-status e19ad72f | grep -E '^D.*\.sprint-exitcode' | wc -l` → `40` (matches task claim)
   - `git status --porcelain` → only untracked `.dev/sprint-state/` and `.dev/tasks/to-do/<this-task>/` remain (both intentional)
   - `make verify-sync` → exit 0, "✅ All components in sync."
   - `diff src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh .claude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` → byte-identical
   - `uv run pytest tests/sprint/test_state_dir_isolation.py -v` → `4 passed in 0.11s`
   - Multiple targeted greps for `state_dir`, `_write_exit_sentinel`, `.sprint-exitcode`
4. **If I found 0 issues, why should the user trust I checked thoroughly?** I did NOT find 0 issues — I found 1 MINOR finding (doc-pipeline staleness, already tracked as a follow-up). The previous structural QA's two IMPORTANT findings were verified as resolved by independent re-check (pg4-proceed.md now exists; the 3 unstaged docs are in commit `6767351`). My adversarial probes searched for hidden release_dir writes, helper-behavior drift, stale git-index entries, test-shadowing, sync drift, frontmatter corruption, hook bypass, accidental staging of `.dev/sprint-state/`, and inflated gate verdicts — none reproduced. Tool engagement (Read: 9, Bash: 14+, Grep-via-Bash: 8) substantially exceeds checklist item count (15), satisfying the tool-engagement minimum from the Confidence Gate Protocol.

---

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

The spawn prompt for THIS qualitative pass did not contain a parsed `## Inherited Structural Verdict` block, but it did reference a sibling `qa-final-validation-report.md` (structural pass, prior cycle). Per release-spec §19.4 fallback when the inherited table is absent, I performed independent structural re-verification AND read the prior structural report to confirm the closed-out findings.

**(a) Reliance list — rf-qa PASS items I treated as ground truth and did NOT re-litigate from scratch:**
- Relied on rf-qa PASS for "Commit SHA `e19ad72f` contains expected staged changes" (prior report row 5) — semantic counterpart verified: I independently re-ran `git show --stat e19ad72f` and confirmed 48 files / 249+ / 49− and that `_write_exit_sentinel(config, exitcode)` at executor.py:1759 is referenced by the regression test at test_state_dir_isolation.py:25.
- Relied on rf-qa PASS for "No orphaned outputs" (prior report row 3) — semantic counterpart verified: I read `phase-outputs/discovery/doc-disposition.md` and confirmed its row-disposition columns line up with the actual file-system contents and the follow-up commit `6767351`'s manifest.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Bootstrap two-path semantic correctness — verified by reading `bootstrap_scan.sh:80-110` and `:125-135` in full and tracing both code paths: state_dir-first preferred read at L92-94, in-release fallback at L95-97, and the `find -name` based `recent_files` call at L134 documented at L133 as auto-picking-up new paths. The two-shape branching described in Step 3.1's QA-CORRECTED INSTRUCTIONS is correctly reflected in the actual code; rf-qa structural pass only verified the diff applied, not the runtime semantics. Tool evidence: Read of `bootstrap_scan.sh` lines 80-135 + cross-check of `recent_files` definition at L51.
- `__post_init__` derivation ordering semantic correctness — verified by reading `models.py:415-471` in full and tracing initialization order: work_dir mirror first (preserves parent-class invariant), then migration shim, then wiring_gate_mode derivation, then state_dir derivation last. This ordering matters because any caller mutating `release_dir` mid-init (none do today, but defensive) would not stomp the derived state_dir; rf-qa structural only verified the field was added, not the ordering safety. Tool evidence: Read of `models.py:395-471`.
- Open-Question resolution traceability — verified by reading the task file's `### Open Questions (Resolved per BUILD_REQUEST)` (L456-473) and confirming each disposition is implemented at the cited line (OQ-1 → commands.py:259-268 implemented; OQ-2 → bootstrap_scan.sh:90 patched; OQ-3 → 40-file git rm landed in commit). rf-qa structural pass did not trace OQ-to-implementation mapping. Tool evidence: Read of task file L456-473 + grep at the cited code sites.
- Redundancy-check soundness — verified by reading `phase-outputs/discovery/redundancy-check.txt` (0 bytes — no MISSING lines), confirming all 40 sentinel directories retained paired `execution-log.jsonl` and so `git rm` (full delete, not `--cached`) is safe. rf-qa structural pass relied on the file's existence, not its content. Tool evidence: `wc -l redundancy-check.txt` → `0`.

---

## Confidence Gate

- **Verified:** 15/15 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100%
- **Tool engagement:** Read: 9 | Grep (via Bash): 8 | Bash: 14 | Glob: 0 (used grep -r instead)
- Tool engagement (Read+Grep+Bash via direct file/grep work = 17+) substantially exceeds checklist item count (15) — engagement-minimum satisfied.

---

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (pre-existing doc-pipeline staleness, already tracked as out-of-scope follow-up)
- Issues fixed in-place: 0 (the 1 minor finding is explicitly deferred per task design; fixing it now would expand scope beyond FU-001)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `docs/generated/sprint-cli/03-execution-engine.md:99`, `docs/sprint-cli-deep-dive.md:1324`, plus 16 other narrative/diagram refs across `src/superclaude/skills/sc-crash-recovery/{SKILL.md,refs/*.md}` and other doc files (all enumerated in `doc-disposition.md` as "defer") | Several documentation diagrams and narrative references still describe `.sprint-exitcode` as living inside `<release_dir>/` (e.g., the artifact tree at deep-dive.md:1324 still shows `release-dir/ ... .sprint-exitcode`) or cite the old `executor.py:1544-1548` line range. These were INTENTIONALLY deferred during Step 3.1b (disposition: defer) because regenerating generated docs and restructuring narrative diagrams belongs in a sibling docs-cleanup task. | NO fix required in THIS task. Follow-up already logged in `### Follow-Up Items Identified` of the task file. The docs-cleanup task should: (a) re-run the docs-generation pipeline to refresh `docs/generated/sprint-cli/*` (covers 03-execution-engine.md:99 + 00-overview.md:130 stale references), (b) update the crash-recovery skill narrative (SKILL.md, refs/pipelines.md, refs/investigators.md, refs/report-template.md), (c) restructure the deep-dive tree diagram + flow-chart cells (deep-dive.md:1324, :1622). |

---

## Actions Taken

No fixes applied in-place. The single MINOR finding is explicitly out-of-scope per the task design (Step 3.1b's "defer" disposition rows in `doc-disposition.md`) and is already captured in the task file's `### Follow-Up Items Identified` section. Applying it here would expand scope beyond the FU-001 boundary the user explicitly defined ("Stop at local commit", "Push/PR deferred per user direction").

The two prior structural-QA IMPORTANT findings (missing `pg4-proceed.md`, 3 unstaged docs) were resolved in the prior cycle: `pg4-proceed.md` was authored in-place during the prior QA pass (still present at `phase-outputs/plans/pg4-proceed.md`), and the 3 doc files (sprint-tui-reference.md, 06-artifacts-output.md, sprint-cli-deep-dive.md) were committed in follow-up commit `6767351d57209d90ff8f81cacc4bad89c55bcfc5`. Both fixes verified by independent re-check in this pass.

---

## Adversarial Probes (Negative Findings I Looked For and Did NOT Find)

1. **Sentinel count discrepancy.** Task claims 40 sentinels removed. Verified via `git show --name-status e19ad72f | grep -E '^D.*\.sprint-exitcode' | wc -l` → exactly 40. Also verified `phase-outputs/discovery/tracked-sentinels.txt` is 40 lines. (Initial wc -l on a wrapped stat output briefly suggested 44, but the authoritative name-status count is 40 — confirmed both ways.)
2. **Hidden release_dir writes resurrected.** `grep -nE 'release_dir.*\.sprint-exitcode' src/superclaude/cli/sprint/*.py` → empty. No production code path writes the sentinel back into the tracked archive.
3. **Helper-behavior drift vs. inline writer.** Read `_write_exit_sentinel` body (executor.py:1759-1771) — preserves the original `try/except OSError: pass` best-effort semantics and `mkdir(parents=True, exist_ok=True)` ahead of the write. Pure faithful refactor.
4. **Stale `.sprint-exitcode` in git index.** Direct re-run of `git ls-files | grep -c '\.sprint-exitcode$'` returns 0.
5. **Test file shadowing the production helper.** Test imports `from superclaude.cli.sprint.executor import _write_exit_sentinel` at L25 and exercises the real function — confirmed by `grep -n _write_exit_sentinel src/superclaude/cli/sprint/executor.py` matching the import target.
6. **Skill sync drift after commit.** Independent `diff -q` between `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` and `.claude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` → BYTE-IDENTICAL.
7. **`make verify-sync` regression.** Re-ran live during this validation pass: clean exit, "All components in sync."
8. **Frontmatter corruption from Phase 5 staging.** Task file frontmatter YAML still parses (status: "🟠 Doing", completion_date: "", updated_date: "2026-05-19").
9. **Phase Findings sections suppressed.** All five Phase Findings sections present; Phase 1 and Phase 5 have substantive entries; Phase 2/3/4 are template-only (acceptable since PG-2/PG-3/PG-4 reports captured the evidence).
10. **Pre-commit hook bypassed.** No `--no-verify` flag in any phase-output file.
11. **Test-cheating.** `test_writer_uses_state_dir_not_release_dir` asserts BOTH positive AND negative (sentinel exists in state_dir AND does NOT exist in release_dir) — collapsing to one assertion would let a regression that wrote to BOTH locations silently pass. Locked tight.
12. **Phantom `- [ ]` items being miscounted.** Verified the awk filter in Post-Completion Step 353 is correct — the 5 unchecked items in the Step 5.8 PR-body heredoc are intentionally excluded.
13. **Two unchecked Post-Completion items.** Lines 357 (Task Summary fill-in) and 359 (mark Done) are intentionally still `- [ ]` because they are downstream of THIS very validation pass — they will be completed by the executor AFTER this report is read. NOT a finding.
14. **`.dev/sprint-state/` accidentally tracked.** `git status --porcelain` shows `.dev/sprint-state/` as untracked (correctly NOT staged); the `.gitignore` workaround from parent task PR-A is still doing its job until the sibling cleanup replaces it.

---

## Recommendations

- **Proceed with marking the task Done.** The two remaining Post-Completion items (lines 357 fill in Task Summary; line 359 update frontmatter to `🟢 Done` + completion_date) can be completed by the executor as the next step. This QA pass does NOT modify those items because they require the executor's final summary judgement.
- **Do NOT push/PR yet.** Per user constraint, push and PR creation were intentionally deferred — the task stops at local commit. Both `e19ad72f` and `6767351` exist locally on `feat/sprint-state-migration`.
- **Schedule the deferred docs-cleanup follow-up.** The 18 deferred doc references in `doc-disposition.md` (rows 1-10, 13-14, 17-21, 23) should be folded into a single sibling docs-update task. The task description in `doc-disposition.md` §"Follow-Up Items Identified" already provides the disposition outline.
- **The temporary `.gitignore` workaround line (`/.sprint-exitcode`) added in parent task PR-A should now be replaced with `.dev/sprint-state/`.** This is the original "sibling cleanup task" called out in the FU-001 task's Prerequisites section. With FU-001 landed and the writer migrated, the anchored sentinel-name line is no longer needed; `.dev/sprint-state/` is the more precise gitignore pattern.

## QA Complete
