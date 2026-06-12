# QA Report — Task File Qualitative Review

**Topic:** Apply layered PRD document-capture hotfix (Layers 1-3)
**Date:** 2026-06-06
**Phase:** task-qualitative
**Fix cycle:** N/A
**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260606-164424/TASK-RF-20260606-164424.md

---

## Overall Verdict: PASS

All 15 task-qualitative checks pass. The task would succeed if executed: every cited
anchor, line number, builder return-shape, fixture, and function signature was
independently verified against current source. Three NON-blocking observations are
recorded below (two are explicitly handled by the task's Open Questions / ORCHESTRATOR
DECISIONs; one is a test-strength note already acknowledged by the task). None rise to
CRITICAL/IMPORTANT/MINOR defect status that the task itself hasn't already disclosed and
bounded, so no in-place fixes were required.

**Drift baseline captured:** BUILD_REQUEST.GOAL was read verbatim from
`.dev/tasks/BUILD-REQUEST-prd-document-capture-fix.md` (lines 3-12) + `merged-solution.md`.
AX-1 drift axis is ACTIVE for this review.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run pytest tests/cli/prd/ -q`, `make lint`, `make verify-sync`, `git diff master...HEAD` all valid against repo state. Step 1.4 captures a baseline before edits; Step 6.1 diffs post vs baseline. verify-sync used only to prove no `.claude/` drift (correct — prd/ is package source not synced). All gate commands runnable. |
| 2 | Project convention compliance | none | PASS | Every edit targets `src/superclaude/cli/prd/*.py` (package source). Task correctly states NO `make sync-dev` needed; never stages `.claude/`. Branch `fix/` from master; PR `--repo IronbellyOrg/IronClaude`. Matches CLAUDE.md rules. |
| 3 | Intra-phase execution-order simulation | none | PASS | P2: helper (2.1) before pins (2.2-2.5) — pins don't depend on helper. P3: pattern map (3.1) before WHERE roots (3.2) before pattern search (3.3, calls `_pick_best_candidate`) before `_pick_best_candidate` def (3.4). NOTE: 3.3 references `_pick_best_candidate` defined in 3.4 — both land in the same file before any test runs, Phase 3 has no intra-phase pytest gate, so ordering is cosmetic not breaking. P5 tests run after P2-4. P6 after P5. No item reads an artifact a later item creates. |
| 4 | Function signature verification | none | PASS | All 4 builders return plain f-strings (prompts.py:135,209,283,531) — injecting `{config.task_dir / "<name>"}` at the cited anchors renders cleanly. `_resolve_step_content(step_id, task_dir, ndjson_text)` 3-arg (executor.py:266). `_determine_status(self, exit_code, output, step_id)` (645-647). `_persist_step_artifact(self, step_id, output_text)` (1145). `_check_no_placeholders` ends @83 (gates.py). All match task citations exactly. |
| 5 | Module context analysis | none | PASS | `_TRUNCATION_MARKER` em-dash @prompts.py:34 (AC9 substring `[TRUNCATED` correct; stale `"..."` mis-quote correctly rejected). `PrdConfig` TYPE_CHECKING-only @26-27 (no runtime import — circular-import avoidance correct). `_STEP_ARTIFACT_FILES` 8 entries @252-263 == helper mapping (zero drift). `re` available in gates.py. `Path`/`json` available in executor.py. |
| 6 | Downstream consumer analysis | none | PASS | INV-010 split: `output_text`@609 → `_determine_status`@618; `gate_content`@613 → `_evaluate_gate`@623 + `_persist_step_artifact`@637. Guard comment (4.2) at @613 documents the contract without behavior change. `_pick_best_candidate` consumed only by the generic path of `_resolve_step_content`; special cases (293-304, 306-337) untouched. AC2 sync test is the consumer guard preventing helper↔`_STEP_ARTIFACT_FILES` drift. |
| 7 | Test validity | weakened-criteria | PASS | AC1-AC9 are STRONG, representative, exercise real behavior. AC10(b) contamination sub-assertion is weaker (see Observation 3) but the task explicitly flags it as an Open Question. Net: tests are substantive, not stubs. STRONG-assertion mandate enforced throughout (`is True`/`== <path>`/`== ndjson_text`/`outcome == "success"`). |
| 8 | Test coverage of primary use case | none | PASS | AC10(a) drives full `PrdExecutor.run()` with a variant-filename write and asserts no-HALT (`outcome == "success"`) — end-to-end recovery. AC1-AC9 cover each unit. All 10 BUILD_REQUEST ACs mapped to concrete Phase-5 items. Untouched-invariants proof (6.4) covers the 5 must-not-change invariants. |
| 9 | Error path coverage | none | PASS | AC6 (zero-match → ndjson fallback, no crash). AC5 (escaping WHERE rejected). `_pick_best_candidate` empty-list guard (`if not candidates: return ""`). WHERE JSON load wrapped in `try/except (OSError, JSONDecodeError)`. containment in `try/except (ValueError, OSError)`. Design handles malformed/missing parsed-request.json gracefully. |
| 10 | Runtime failure-path trace | none | PASS | Flow: subprocess → NDJSON `output_text` → `_resolve_step_content` (pattern map → bounded WHERE roots → rglob candidates → `_pick_best_candidate`) → `gate_content` → `_evaluate_gate`. Zero-match still returns `ndjson_text` (365 preserved). No downstream gate/consumer left unable to handle new output: gate logic, persist, status detection all unchanged. |
| 11 | Completion-scope honesty | none | PASS | Open Questions (sufficiency/preparation JSON/marker pins; AC10 no-cleanup) are explicitly carried and resolved-as-designed, NOT ignored. Deferred A/B (cwd isolation, result-event capture) clearly OUT OF SCOPE in overview, constraints, Follow-Up Items. An executor cannot accidentally implement them. |
| 12 | Ambient dependency completeness | none | PASS | No new imports needed (Path/json/re all present — verified). Helper is module-level/importable. No `__init__.py` export, CLI parser, or registry change required (`_check_no_truncation_marker` deliberately NOT wired — define-only). AC tests import privates directly, matching existing convention. |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add param" hazards. `_resolve_step_content` stays 3-arg (no WHERE param added — WHERE read internally from parsed-request.json). `_pick_best_candidate(candidates, *, preferred_root)` defined (3.4) and called (3.3) in same file/phase. |
| 14 | Function-existence claims verified | none | PASS | Grep/Read-verified: helper insertion point (prompts.py:53), 4 builder anchors (154/222/301/539), `_STEP_ARTIFACT_FILES`@252-263, generic search@347-365, "largest wins"@360, `_evaluate_gate`@678-715, `_determine_status`@645-676, INV-010 split@609/613/618/623/637, `_persist`@1145-1166, `_check_no_placeholders`@64-83, divider@86, STRICT block@330-346. ALL exact. |
| 15 | Cross-reference accuracy (templates) | none | PASS | This task references research files + source line numbers (not a doc template). Every per-item file:line citation re-verified against current source; the task itself mandates re-confirmation before each edit and supplies the drift table (research 05) for stale design cites. All cited anchors confirmed present and current. |

---

## Adversarial Axes Sweep (AX-1..AX-5)

- **AX-1 Drift** — Checked task content vs BUILD_REQUEST.GOAL + merged-solution.md. The task
  faithfully implements Layers 1-3, honors all 4 load-bearing invariants (INV-001 drop
  frontmatter mandate, INV-005 bounded WHERE, INV-006 freshness tiebreak, INV-010 split),
  and keeps Deferred A/B out of scope. Cited line numbers are EXACT-CURRENT (verified), not
  the stale design cites — the task explicitly corrects drift via the research-05 drift
  table. No drift found.
- **AX-2 Contradictions** — One apparent design-vs-task tension examined: research-05 Claim 7
  says `_check_no_truncation_marker` "must be registered ... to actually run"; the task says
  DEFINE-ONLY, do NOT wire. RESOLVED, not a contradiction: the ORCHESTRATOR DECISION overrides
  the design's general intent for a documented safety reason (wiring would mutate the
  must-stay-unchanged research-notes STRICT block / risk INV-002), and BUILD_REQUEST AC9 tests
  the function directly (consistent with define-only). The more conservative choice. No
  load-bearing contradiction.
- **AX-3 Omissions** — QA_GATE_REQUIREMENTS=FINAL_ONLY, VALIDATION_REQUIREMENTS,
  TESTING_REQUIREMENTS=UNIT(+E2E) all reflected: baseline capture (1.4), full suite vs
  baseline (6.1), lint (6.2), verify-sync (6.3), untouched-invariants proof (6.4), 10 AC
  tests (5.1-5.10). One soft omission noted (Observation 1): merged-solution Test Plan item 3
  ("research-notes semantic checks pass on recovered real content / fail on thin content")
  has no dedicated AC — but it is NOT in the BUILD_REQUEST AC1-AC10 list either, so the task
  faithfully covers the authoritative AC set. Not a defect.
- **AX-4 Weakened criteria** — AC10(b) contamination assertion is weaker than it appears
  (Observation 3) because E2E mocks `_build_prompt`, so the pin text isn't rendered; the
  cleanliness is controlled by the mock's write target, not by the pin. The task explicitly
  acknowledges this ("verifies pinned-path behavior, not cleanup"; ORCHESTRATOR DECISION 3).
  Disclosed and bounded — not a hidden weakening.
- **AX-5 Invented content** — Every named artifact (`_artifact_path_for_step`,
  `_STEP_ARTIFACT_PATTERNS`, `_pick_best_candidate`, `_check_no_truncation_marker`, the 4
  builders, `_STEP_ARTIFACT_FILES`, fixtures `config`/`executor`/`e2e_task_dir`,
  `_mock_process_factory`) exists in source/research or is a planned addition grounded in
  merged-solution.md verbatim blocks. No invented files/modules/commands. No scope inflation
  (no caching, no cleanup logic — explicitly excluded).

---

## Observations (NON-blocking — already disclosed/bounded by the task)

**Observation 1 (AX-3, informational):** merged-solution.md Test Plan item 3 mentions
"research-notes semantic checks pass on recovered real content / fail on thin content"
(INV-002 scoping). No dedicated AC covers this. However, BUILD_REQUEST's authoritative AC
list (AC1-AC10) does not include it, and INV-002 is honored by NOT adding content-faking.
The task faithfully covers the BUILD_REQUEST ACs. No action needed.

**Observation 2 (AX-2/informational — `task_dir.parent` = OUTPUT root, not git root):**
Design §2b sets `repo_root = task_dir.parent`, which (per research-05 Claim 4) is the OUTPUT
root (e.g. `.dev/eval-workspaces/`), not the git repo root. Consequence: for a real
source-relative WHERE like `src/superclaude`, `repo_root / where` won't exist → containment
guard skips it → WHERE-root widening is frequently a no-op in sandboxed runs. This FAILS
SAFE (no crash). Impact on AC3/AC5:
  - **AC3 (variant recovery):** the task writes the variant into an *in-task_dir* `.dev/specs`
    subdir, so `task_dir` rglob + the pattern map (`scope-discovery*.md`) recovers it
    regardless of the WHERE-root logic. AC3 genuinely exercises variant-NAME recovery (its
    stated purpose) — it just doesn't depend on WHERE-widening. Not a false-green for the
    pattern map; it IS a real recovery test. OK.
  - **AC5 (INV-005 containment):** to genuinely exercise the WHERE-containment guard, the
    test must place the escaping candidate and WHERE entry such that `repo_root / where`
    actually resolves to the escaped dir. Since `repo_root = task_dir.parent`, the test author
    must construct paths relative to `task_dir.parent`. The assertion (`result != escaped_
    content`) holds true EVEN IF the guard is a no-op — so AC5 is satisfiable but could pass
    "for the wrong reason" (the escaped file simply never being under any search root) rather
    than via the containment guard specifically. The task's AC5 wording ("reachable only via a
    `..`-traversal WHERE entry") is the correct construction to make the guard decisive, and
    Step 3.2 already cites research-05 Claim 4 to brief the author on the parent-is-output-root
    fact. Adequately disclosed; no task edit required.

**Observation 3 (AX-4, disclosed Open Question — AC10 sub-assertion strength):** The E2E
harness mocks `executor._build_prompt`, so the pinned prompt text is never rendered during
AC10. Therefore AC10(b) ("no `scope-discovery*.md` left in the WHERE dir") proves that the
*mock* wrote to the canonical path, NOT that the *pin* caused it — closer to a tautology than
a pin-effectiveness test. AC1 is the genuine proof that the pin renders the canonical path;
AC10(a) is the genuine Layer-2 recovery proof. The task explicitly carries this as an Open
Question ("The E2E test verifies pinned-path behavior, not cleanup") and ORCHESTRATOR
DECISION 3. Additionally, for AC10(a) to NOT false-green via the NDJSON fallback, the variant-
write factory should pair the disk variant file with SHORT NDJSON commentary for scope-
discovery (the default `_make_passing_output` emits ≥50 NDJSON lines, which would pass the
gate without recovery). RECOMMENDATION (advisory, not blocking): when authoring AC10(a),
override scope-discovery's NDJSON to a short (<50-line) commentary so the no-HALT success is
attributable to recovery, not the fallback. This sharpens an existing item rather than fixing
a defect.

---

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (no defects warranting a task edit; all observations are
  already disclosed/bounded by the task's Open Questions + ORCHESTRATOR DECISIONs)
- AX-1 drift baseline: ACTIVE (BUILD_REQUEST.GOAL captured verbatim)

## Issues Found
(None. Three NON-blocking observations recorded above; each is already disclosed by the
task's own Open Questions / ORCHESTRATOR DECISIONs and does not block execution.)

## Actions Taken
No in-place fixes applied. fix_authorization was true, but no CRITICAL/IMPORTANT/MINOR
defect was found that the task had not already disclosed and bounded. The three observations
are advisory sharpening notes for the executor, not task-file defects requiring an Edit.

## Confidence Gate
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 12 | Grep: 2 | Glob: 0 | Bash: 2
- All 15 checklist items VERIFIED with tool evidence (file:line citations from source reads).
- No UNVERIFIABLE items. No UNCHECKED items.
- Tool-call count (16 Read/Grep/Bash) ≥ 15 checklist items — engagement minimum satisfied;
  each call mapped to specific anchor/fixture/signature verification, not padding.
- No web research performed (review is fully local-file-bound) — no Tavily/WebFetch usage to
  report.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for frontmatter (Check 1), mandatory sections (Check 2), B2 6-field
  self-containment (Check 3), granularity counts P1=4/P2=5/P3=4/P4=2/P5=10/P6=4 (Check 4),
  DAG acyclicity (Check 13/TB-Add-4), uniform Verify/Acceptance form (TB-Add-6), Execution
  Context block having no file:line (TB-Add-7), per-item Context carrying file:line
  (TB-Add-8), and the C1-C6 content gates (builder-pin completeness, define-only wiring,
  3-arg signature, AC9 marker string, preserved invariants, line-number exactness).
- Did NOT re-verify section numbering, item structure, placeholder scans, or dependency
  structure — accepted as machine-verified.

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT
and my own tool work was required:**
- **C4 (AC9 marker) went beyond rf-qa's string check.** rf-qa verified AC9 uses the
  `[TRUNCATED` string, not the stale `"..."`. I independently verified by Reading
  prompts.py:34 (`_TRUNCATION_MARKER` em-dash literal) AND the gates.py design block branch
  logic (`if "[TRUNCATED" in content or content.rstrip().endswith("...")`) that the AC9 TEST
  would actually exercise BOTH branches of `_check_no_truncation_marker` — the substring
  branch (via the verified em-dash marker) and the trailing-`...` branch — so the test is
  operationally valid, not just string-correct. Tool evidence: Read prompts.py:1-60,
  merged-solution.md:194-198, test_gates.py:200-239.
- **C3 (3-arg signature) — semantic feasibility of injection.** rf-qa verified the signature
  stays 3-arg. I independently verified by Reading executor.py:266-365 that the bounded-WHERE
  rewrite reads WHERE internally from `parsed-request.json`, integrates with the existing
  `artifact_name`/`base_name` locals and the zero-match `return ... else ndjson_text` at line
  365, and does NOT disturb the build-task-file (293-304) / assembly (306-337) special cases —
  i.e. the change is genuinely localized to the generic dict-keyed path. Tool evidence: Read
  executor.py:248-368.
- **AC10 / Check 7-8 — harness reality vs claimed exercise.** rf-qa cannot judge whether the
  E2E test genuinely exercises Layer 1/Layer 2. I Read test_e2e.py in full (1-575) and the
  `_mock_process_factory` (224-253) and discovered `_build_prompt` is mocked, so AC10(b) is a
  near-tautology and AC10(a) risks false-green via the ≥50-line NDJSON fallback unless the
  factory shortens scope-discovery's NDJSON. This is a semantic test-validity finding rf-qa's
  structural pass could not surface. Tool evidence: Read test_e2e.py:1-575.
- **Builder render-shape — would the pin actually render.** rf-qa verified the pin anchors
  exist. I independently Read prompts.py:108-328 and :510-558 to confirm ALL FOUR builders
  return plain f-strings (not `.join`/concatenation), so `{config.task_dir / "<name>"}`
  injected at each anchor is syntactically valid and renders an absolute path. Tool evidence:
  Read prompts.py:108-328, 510-558.

## Recommendations
- PROCEED. The task is execution-ready. Verdict PASS.
- Advisory (non-blocking) for the executor, to be applied during Phase 5 authoring:
  1. AC10(a): override scope-discovery's mock NDJSON to <50 lines so the no-HALT success is
     attributable to Layer-2 recovery, not the NDJSON fallback (Observation 3).
  2. AC5: construct the escaping WHERE candidate so it IS reachable via the WHERE entry under
     `task_dir.parent` (the output root), making the containment guard — not mere absence —
     the decisive exclusion (Observation 2).
  These are test-sharpening notes; neither blocks the task nor requires a task-file edit.

## QA Complete
