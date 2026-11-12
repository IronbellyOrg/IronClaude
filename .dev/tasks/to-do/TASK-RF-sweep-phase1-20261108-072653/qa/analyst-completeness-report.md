# Research Completeness Verification (task-builder track 1)

**Topic:** issue #339 Phase 1 (read-only `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-14, routing rows R1-R8, `.gitignore`), with design fixes R3-B1, R3-B2, R3-B3 first
**Date:** 2026-11-08
**Analysis type:** completeness-verification, lens: completeness (breadth)
**Files analyzed:** 01-file-inventory.md, 02-patterns-conventions.md, 03-integration-points.md, 04-design-fixes-r3.md, 05-test-verification.md, 06-template-examples.md
**Scope map:** ../research-notes.md

---

(Findings are appended below as the review proceeds.)

**Depth tier:** Deep (per research-notes.md line 6)

## Verdict: FAIL (1 IMPORTANT gap, 9 minor)

The six files cover almost every area in the scope map with strong `file:line` evidence. One area the scope map names has no research coverage: the content and source of the step 1.0b owner decisions GQ-10, GQ-35, GQ-61 and GQ-63, and `.dev/orca-command-refactor/decisions/APPROVED.md`. The fix is one small gap-fill read.

---

## Coverage Audit (scope map versus research files)

| Scope item (research-notes.md) | Covered by | Status |
|---|---|---|
| Design section 7 (7.1 to 7.6) interfaces, models, allowlists, JSON, report, command and skill | 01 B1 to B8 (signatures with design lines 357-657) | COVERED |
| Design section 8 WC-14 and pins | 01 C2, C11; 03 IP-1, IP-2 | COVERED |
| Design section 9 routing rows R1 to R8 | 01 C3 to C9; 03 IP-4 | COVERED |
| Design section 10 `.gitignore` | 01 C10; 03 IP-6; 05 section 8 | COVERED |
| Design section 11 test plan | 01 B9 to B16; 05 section 10 | COVERED |
| Design section 15 step map (1.0a to 1.29) | 01 section D | COVERED |
| Design sections 12, 13 (D9), 17 (items 2, 4, 5, 19, 22, 23), 18 | 04 sections 2 to 4 | COVERED (only the items R3 needs) |
| Design section 3 report publication (3.2 `_publish`) | 02 section 7 (precedents, design lines 99-117); 01 B6 defers it to researcher 4, who did not read it | PARTIAL (minor) |
| Design sections 2 (GQ resolutions), 4, 5, 6, 16 | Cited by line only (01 A, 02, 04 GQ-103(3)) | PARTIAL (minor) |
| `orchestrator-mode-review-3.md` R3-B1, R3-B2, R3-B3 | 04 (exact edits, fixtures, per-finding gate) | COVERED |
| `inv-005-orca-index-lock.md` | 04 section 1.4 | COVERED |
| Every existing file to modify (11 files) | 01 C1 to C11, anchors CONFIRMED; 03 | COVERED |
| Every new file (package, command, skill, 7 tests, command test) | 01 B1 to B16; 05 adds `tests/sweep/__init__.py` | COVERED |
| Template 02 rules A3, B2, L, M3, M4, I19 to I22; POST reflect skill form | 06 | COVERED |
| Gap: R3-B1 Dispatch time fields | 04 section 2 (static Orca bundle read) | COVERED |
| Gap: R3-B2 tie-break | 04 section 3 | COVERED |
| Gap: R3-B3 FR-010 fixtures | 04 section 4 | COVERED |
| Gap: line anchors still hold | 01 C1 to C11, 03 IP-4 | COVERED |
| Gap: encoding human-gated items 1.0a and 1.0b | 06 section 9 (pattern only) | COVERED (pattern) |
| Step 1.0b decision content: GQ-10, GQ-35, GQ-61, GQ-63, and `.dev/orca-command-refactor/decisions/APPROVED.md` (design line 907) | none | **GAP (IMPORTANT)** |
| Step 1.0a capture items 1 to 13 (design lines 866-898) | 01 A (range only); 04 uses items 3, 4, 8, 10, 13 | PARTIAL (minor) |
| Step 1.16a "#409 diff check" (design line 925) | 01, 06 cover the `gh pr view 422` half only | PARTIAL (minor) |
| Gap: test infrastructure (marker, mocking, AST, snapshot) | 05 sections 1 to 8 | COVERED |
| Patterns: Click registration, thin command plus skill, `~/.claude` paths, sync and lint | 02; 03 IP-7; 05 section 9 | COVERED |

## Criteria

### 1. Source files identified with paths and exports: PASS

01 names every new file with the interface signatures copied from design 7.1 (for example `classify.py` functions at design lines 405-419, `probes.py` constants at 518-543) and every existing file with its CONFIRMED anchor (for example `main.py:559-561`, `WORKER-CONTRACT.md:23`, `.gitignore:254`). 02 and 05 name the precedent files to copy with lines.

### 2. Output paths and formats clear: PASS

New file paths come from design 7.1 and 11 (01 B and D). Step artifacts are listed (01 line 210: `readonly-probe.md`, `owner-decisions.md`, `sweep-live-check-1.4.json`, `sweep-help-pipx.txt`). 06 section 6 gives the QA report paths and warns that M3 and M4 default names collide across five gates, recommending a `qa/<gate>/` prefix.

### 3. Logical breakdown of phases and steps: PASS

01 section D lists steps 1.1 to 1.29 with file and action. 03 "Consolidated ordering constraints" gives seven ordering rules. 04 section 5 gives one gate per R3 finding. 06 section 11 gives the order B1 edit, B1 gate, B2 edit, B2 gate, B3 edit, B3 gate, before step 1.1.

### 4. Patterns and conventions with examples: PASS

02 gives each pattern with a `file:line` example (registration `main.py:551-561`, lazy `__getattr__` `recommend/__init__.py:12-20`, seam mocking `tests/cli/reflect/conftest.py:58-80`, AST guard `tests/swarm/test_concurrency_python_only.py:39-80`, Activation block `graph.md:41-46`). 05 adds test patterns (real git `tests/unit/test_eval_runner_master_checkout.py:22-48`, command pins `tests/commands/test_impact_command.py`).

### 5. MDTM template notes with rule references: PASS

06 cites T02 and TB lines for A3/A4, B2/B3/B5, E1 to E4, F2, J1 to J3, I14 to I22, L1 to L7, M3, M4, Execution Context, anti-orphaning (TB:2363) and the skill-mode POST reflect item (TB:2215-2235). It also names four template conflicts the builder must resolve.

### 6. Granularity for one item per file or component: PASS, with one exception

01 section D and its per-file edit counts are checklist-ready. 04 gives fixture names per test file. The exception is step 1.0b, where the builder cannot write one record item and one HALT item per decision without the decision text (see the IMPORTANT gap).

### 7. Doc-sourced claims tagged: PASS (minor format issue)

Claims are tagged, but in a house vocabulary rather than the literal tags: "CONFIRMED" (01, 03), "UNVERIFIED" or "Unverified" (01 B2, B4, B9; 02 section 3 and 8.1; 04 sections 2.5, 3.6, 4.5; 05 sections 2, 5; 06 sections 1, 3), and "DESIGN GAP" (03 IP-2). No file uses `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]` or `[UNVERIFIED]` literally. A grep-based downstream check for those tags would miss them. Minor.

### 8. Solution research evaluated approaches: PASS

04 is labelled Solution Research. For R3-B1 it reads the Orca 1.4.245 bundle statically and finds `dispatch.dispatchedAt`, `completedAt`, `status`, and rejects editing the cycle 2 revision row in favour of a new Fix cycle 3 table, giving the reason. For R3-B2 it measures how likely overlap is (insert guards at bundle offsets 1629916 and 1630095) before writing one order-independent rule. For R3-B3 it flags its own `orca worker-list <run>` source name as a design choice that needs gate approval. 02 section 7 weighs reusing an atomic-write helper and rejects it with evidence.

### 9. Unresolved ambiguities documented: PASS

Documented and not skipped: `ClassifiedRow` fields (01 B2); step 1.4a test before `conftest.py` (01 B9); CHANGELOG heading form (01 C9, 03 R8); `Bash(...:*)` versus space-star (02 section 8.1); the fifth pin (03 IP-2); the subprocess guard and the `/integration/` auto-marker (05 section 2); B2 single paragraph versus TB 5-field form, Blocked emoji, Post-Completion section (06 sections 1, 3, 8); POST reflect `--diff BASE..HEAD` missing uncommitted work (06 section 12); every live-capture unknown (04 sections 2.5, 3.6, 4.5).

---

## Contradictions Found

1. **Test location.** 02 section 9 proposes `tests/cli/sweep/`. 01 B9 to B15, 05 section 3 and the design (section 11, line 726) use `tests/sweep/`. 02 marks its own row as inferred and defers to researcher 5. Resolved in favour of `tests/sweep/`. Minor.
2. **Number of pin edits in `tests/skills/test_worker_contract.py`.** 01 C11 and section D list four edits (lines 155, 254, 545, 865). 03 IP-2 shows a fifth, required one: `RULE_PHRASES["never-as-worker"]` at `test_worker_contract.py:86-92` pins the old line 23 text word for word, so `test_contract_states_rule[never-as-worker]` fails unless `:89` changes in the same commit. A builder working from 01 section D alone would miss it. 03 also notes the design's section 8 lists only four pins, so this is a fourth design defect; 04 does not pick it up as a design fix. Minor as a coverage item, because 03 gives the exact edit, but the builder must use 03's count of five.
3. **Test rename.** 05 section 6 calls renaming `test_never_as_worker_list_names_all_seven_commands` "optional". The design (line 679), 01 C11 and 03 IP-2 require the rename. Follow the design. Minor.

---

## Compiled Gaps

### Critical gaps (block synthesis)

- None.

### Important gaps (blocking for this gate)

- **G-1. Step 1.0b decision content is not researched.** Source: research-notes.md lines 39 and 66; design line 907 (`Owner decisions GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, and sign-off on the D9 narrowing of SP-29; read .dev/orca-command-refactor/decisions/APPROVED.md`) and open item 20 (design line 988). No research file says what GQ-10, GQ-35, GQ-61 or GQ-63 ask, what their options are, or which build steps each one gates. Only GQ-11 (gates 1.17 to 1.19, 03 IP-2) and D9 (gates 1.3, 01 B3) are mapped. None of the files reads `APPROVED.md` (it exists, with `RECOMMENDATIONS.md` beside it). The GQ IDs are defined in `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md` and the research report there; the design and the SPEC (`merged-requirements.md`, no GQ-10/35/61/63 match) do not define them. Why it matters: 06 section 9 asks for one OQ-N record item per decision with "the options verbatim" and for every dependent item to cite its OQ ID (TB-Add-3). Without the decision text and the step each decision gates, the builder must research during the build or guess, which is the invented-decision risk the human gate exists to stop. Fix: a gap-fill read of `gaps-and-questions.md` for GQ-10, GQ-35, GQ-61, GQ-63 (question, options, recommendation, which steps it gates) and of `APPROVED.md` (whether any of them are already decided).

### Minor gaps (notes; do not block)

- M-1. Step 1.0a capture items 1 to 13 (design lines 866-898) are cited as a range but not listed one by one (01 A; 04 uses items 3, 4, 8, 10, 13). The builder can copy them from the design.
- M-2. The "#409 diff check" half of step 1.16a (design line 925) is not explained; 06 section 9 covers only `gh pr view 422 --repo IronbellyOrg/IronClaude`.
- M-3. Design section 3.2 `_publish` (lines 99-130): 01 B6 hands it to researcher 4, who did not read it. 02 section 7 covers the precedents and quotes the design's `O_EXCL` and `.<stem>.<pid>.tmp` detail, so the builder has enough.
- M-4. Design sections 4, 5, 6 and 16 are cited by line only; deviations D1 to D8 and open items other than 2, 4, 5, 18 to 23 are not listed. 04 section 5 keeps the totals (9 deviations, 23 open items) as a gate check.
- M-5. Verification tags use CONFIRMED / UNVERIFIED / DESIGN GAP, not the literal `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]`.
- M-6. No file has separate "Gaps and Questions" or "Key Takeaways" headings; each has Status: Complete and a Summary that holds its gaps.
- M-7. Step 1.29 (manual `superclaude sweep --help` under pipx) and open item 18 (`uv run --frozen --no-sync` effect) have no verification recipe in 05.
- M-8. Contradictions 1 and 3 above (test location, rename "optional").
- M-9. Contradiction 2 above: the fifth pin is a design section 8 defect that the design-fix phase does not yet include; the builder should either add it as a design edit beside R3-B1 to R3-B3 or record it as a deviation.

---

## Depth Assessment

**Expected depth:** Deep (data flow traces, integration mapping, pattern analysis).
**Actual depth achieved:** Deep for the areas covered. 03 maps each integration point to the test that pins it and the ordering it forces. 04 traces the Dispatch time fields from the Orca SQLite schema through the runtime handler to the `worker-show` JSON. 05 traces the auto-marker risk through `pytest_plugin.py:216-222`. 01 re-reads every anchor.
**Missing depth elements:** step 1.0b decision content (G-1).

## Recommendations

1. Run one gap-fill researcher on G-1: read `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md` (and the research report if needed) for GQ-10, GQ-35, GQ-61, GQ-63, plus `.dev/orca-command-refactor/decisions/APPROVED.md`. Write the question, options, recommendation, current status and gated steps for each into a short research file (for example `research/07-owner-decisions.md`).
2. Tell the builder to take the `test_worker_contract.py` edit count from 03 (five pins), not 01 section D (four), and to decide whether the missing fifth pin becomes a design edit next to R3-B1 to R3-B3 (M-9).
3. Tell the builder to use `tests/sweep/` with an empty `tests/sweep/__init__.py` (05 section 3) and to rename the never-as-worker test as the design says.

VERDICT: FAIL

Structured gap list:
- G-1 | IMPORTANT | Step 1.0b owner decisions GQ-10, GQ-35, GQ-61, GQ-63 and APPROVED.md not researched (question, options, status, gated steps) | source: research-notes.md:39,66; design:907,988 | fix: gap-fill read of TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md and .dev/orca-command-refactor/decisions/APPROVED.md
