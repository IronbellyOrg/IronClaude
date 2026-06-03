# Research Completeness Verification

**Topic:** task-builder — sc-recommend lookup-cache layer
**Date:** 2026-06-03
**Files analyzed:** 6 (01-file-inventory, 02-pattern-templates, 03-eval-harness-reuse, 04-classifier-and-dispatch, 05-template-and-examples, 06-tests-sync-registration)
**Analysis type:** completeness-verification (9-criterion)

---

## Coverage Audit (assigned scope vs research files)

| Scope Item | Covered By | Status |
|-----------|-----------|--------|
| sc-recommend skill package (SKILL.md + 3 refs) | 01 §1, 04 §1 (full Read) | COVERED |
| commands/recommend.md (+ `--eval` flag insertion) | 01 §1 (L42-46) | COVERED |
| .gitignore cache region (2-region edit) | 01 §2, 06 §4 | COVERED |
| cli/ module layout + new module placement | 01 §3 (tasklist mirror), 06 §3.1 | COVERED (path conflict — see Contradictions) |
| main.py registration | 01 §4 (L400-426), 06 §3.1 | COVERED |
| Atomic-write / YAML I/O patterns | 02 §1, §3 | COVERED |
| install_mcp precondition checks | 02 §2, 04 §2.7 | COVERED |
| Classifier (closed-enum, top-2 delta) | 02 §4, 04 §3 | COVERED |
| Agent model-override (`model: haiku`) | 02 §5 | COVERED |
| Eval-harness reuse (cli/eval vs .dev) | 03 (entire) | COVERED |
| Cold-path runbook condensation | 04 §1.8 | COVERED |
| Python-vs-prose boundary evidence | 04 §4 (both-sides) | COVERED |
| Template-02 rules (A3/A4/B2/L1-L6/M1/M2/I15-I18) | 05 §1, §2 | COVERED |
| PENDING/HALT item shapes | 05 §3 (3A + 3B) | COVERED |
| Tests conventions + verify-sync gates | 06 §1, §2 | COVERED |
| Registration surfaces (EXPECTED_TOP_LEVEL_COMMANDS, _FRESHNESS_SCRIPTS, settings.json) | 06 §3 | COVERED |
| Closed-enum key vocabulary | 04 §3 | COVERED (derived — flagged) |

No assigned-scope item is uncovered. All 6 files read in full.

---

## Criterion-by-Criterion Verdict

### Criterion 1 — Source files identified with paths and exports? **PASS**
Evidence: File 01 §1 enumerates all 5 primary edit targets under `src/superclaude/` with line counts (verified `wc -l`) and per-file purpose/exports. File 01 §3 catalogs the entire `cli/` peer-module set with file lists. File 01 §4 cites exact registration block (`main.py:400-426`) with verbatim idiom. File 02 anchors every pattern to file:line (convergence.py:104-136/304-317/63-71; install_mcp.py:470-489/156-164; eval/run_report.py:358-363; ORCHESTRATOR.md; task-builder/SKILL.md:787-791). File 04 §1 re-Reads SKILL.md + 3 refs in full. File 06 §6 supplies a cross-reference path table. Markdown skills correctly noted as having "no Python exports."

### Criterion 2 — Output paths/formats clear or reasonably inferred? **PASS**
Evidence: New module layout `src/superclaude/cli/recommend/` with 6-file skeleton mirroring `cli/tasklist/` (01 §3, L91-103). Cache YAML location `.claude/cache/sc-recommend-lookup.yaml` + `-plugin.yaml` + `-events.jsonl` (06 §4, 04 §2.5-2.8). Eval-runs dir `.claude/cache/eval-runs/iteration-<N>/row-<key>-results.json` (03 §4, 04 §2.9). YAML format precedent fully resolved (02 §3b: `safe_dump(sort_keys=False, default_flow_style=False, allow_unicode=True)`). NOTE: the module-path token differs across files (`recommend/` vs `sc_recommend/`) — format/location is clear, the *name* is contradictory (see Contradictions; does not fail this criterion since both resolve to a CLI submodule under `cli/`, but the builder needs one canonical name).

### Criterion 3 — Logical phase/step breakdown mapping the 12-step Implementation Order? **PASS**
Evidence: File 01 maps spec Implementation Order #2 (YAML reader/writer), #4 (cold-path runbook), #6 (telemetry), #7 (`--eval`/flag), #8 (plugin-eval gate) to concrete files. File 04 §2.2 reproduces the 10-step HOT-PATH and §2.3 the 6-step COLD-PATH verbatim with line anchors. File 03 §4 decomposes the `--eval` pipeline (mode matrix → fan-out → grade → aggregate → best_model). File 04 §4.1 gives a per-step Python-vs-prose home table. The 12-step order is traceable across 01/03/04; granularity is per-component.

### Criterion 4 — Patterns/conventions documented with examples? **PASS**
Evidence: File 02 is the dedicated pattern file — 5 patterns each VERBATIM: (1) DeviationRegistry atomic-write→YAML adaptation with derived code, (2) install_mcp checks, (3) YAML safe_dump house style + the bare-`yaml.dump` anti-pattern call-out, (4) closed-enum classifier (5 structural elements), (5) Agent block + `model: haiku` override with alias-validation. All convergence/install_mcp/classifier/model-override anchors present and the builder is told "reuse, don't reimplement."
**Independently verified:** convergence.py:save L304-317 (schema_version:1, os.replace) and install_mcp checks (L470, L156) exist as claimed.

### Criterion 5 — MDTM template-02 notes with rule references? **PASS**
Evidence: File 05 §1 documents EVERY relevant Section A-M rule with line anchors: A1 (workflow-doc omission — correctly notes sc-recommend has no `.gfdoc` → omit WORKFLOW-DEPENDENT), A3 (granular breakdown), A4 (iterative pre-enumerate/process/consolidate), B2 (6-element self-contained item, verbatim completion-gate sentence), B5 (forbidden shapes), E1-E4 (flat structure), F2a (parallel-spawn exception), I15-I18 (phase gates, post-completion, code-test, I18), L1-L6 + L7 selection guide, M1/M2 (phase-gate composite + applicability: research-gate + task-integrity for task-building tasks), J1 blocker clause. The `## Execution Context` block is correctly flagged as NOT in the template but an established live convention (05 §4, with `**References:**`/`**Source areas:**`/`**Key constraints:**` and the "Source areas MUST NOT carry file:line" rule).

### Criterion 6 — Granularity sufficient for per-file/per-component checklist items? **PASS**
Evidence: File 01 §3 gives a per-file skeleton (6 files + cache.py/telemetry.py). File 06 §3 gives discrete registration items (main.py add_command + EXPECTED_TOP_LEVEL_COMMANDS + _FRESHNESS_SCRIPTS + settings.json — each a separable item). File 03's master REUSABLE-vs-NEW table is per-capability (portable into one item each). File 05 §5 surveys 4 done tasks with item/phase counts as granularity calibration. The builder can author one B2 item per file/surface.

### Criterion 7 — Doc/spec-sourced claims that touch real code tagged or evidence-backed with file:line? **PASS**
Evidence: This is the strongest dimension. Files 01/02/04/06 anchor virtually every code-touching claim to `file:line` (verified `wc -l`, `nl -ba`, `Read in full this turn`). File 04 explicitly self-corrects a doc-vs-code discrepancy: SKILL.md is 227 lines actual vs the brief's stated 226 (04 §1, L14) — exactly the [CODE-VERIFIED]-style cross-validation expected. File 03 verifies on disk that `generate_review.py` does NOT exist and `EvalOutcome` has no token/model field (`models.py:337-345`), contradicting an aspirational round-4 claim — a proper [CODE-CONTRADICTED] surfacing. No untagged doc-only architectural claim was found being passed off as code-fact. **Independent spot-check confirms** the gitignore lines, main.py L400-426, EXPECTED_TOP_LEVEL_COMMANDS L31, _FRESHNESS_SCRIPTS L43, convergence L304-317, settings.json L16-21, pyyaml L38, anthropic-ban L200-210 are all accurate.

### Criterion 8 — Eval-harness reuse-vs-new clearly resolved (cli/eval vs .dev tension)? **PASS**
Evidence: File 03 is dedicated to this and resolves it decisively. §1 frames the TWO systems (heavyweight cli/eval PTY harness vs lightweight `.dev` Python grader). §1 + §3 give the verdict: per-row `--eval` reuses the **`.dev` lightweight model** (ported into the package), NOT cli/eval; the round-4 plugin path *aspires* to cliEval but practically also lands on `.dev`-style because `EvalOutcome` carries no token/model axis. The decision basis is evidence-backed (`models.py:337-345`, `config.py` scratch-root allowlist excludes `.claude/cache/eval-runs/`). The remaining conflict (merged-requirements §259-269 vs round-4 §16,24,54) is explicitly surfaced as a builder decision point (§1, §5 flag 1) — NOT silently resolved.

### Criterion 9 — Unresolved ambiguities documented? **PASS (with one gap — see below)**
Evidence: The 4 needs_human_decision items are all present:
- Python-vs-prose boundary — File 04 §4 (both-sides evidence, Resolution H vs P, "DO NOT DECIDE").
- The eval-reuse merged-requirements-vs-round-4 conflict — File 03 §1, §5 flag 1.
- anthropic-SDK-ban constraint — File 06 §5 (L209, independently confirmed at pyproject L200-210).
- Closed-enum key vocabulary (only `spec-generation` spec-confirmed; 9 derived) — File 04 §3.2-3.3 marked DESIGN PROPOSAL / needs-human-review.
- Few-shot coverage gap (only 4 of ~10 keys have eval examples) — File 04 §3.3, §5 flag 3.
- `allowed-tools` expansion (Edit/Write/Agent/Task missing) — File 04 §1.1, §5 flag 1.

**GAP (CRITICAL — premise mismatch, independently verified against the spec):** The track goal instructs the builder to author "OQ1-OQ3 ... as needs_human_decision halt items (write PENDING and halt)." NO research file extracted what OQ1/OQ2/OQ3 actually are, and my direct read of `merged-requirements.md` shows the premise is WRONG:
- **OQ1 is already RESOLVED** (L358): "Auto-eval on cold-path insert — **REJECTED by user (OQ1 round-3 resolution)**." It is a closed decision, not an open question.
- **OQ2 is already RESOLVED** (L378): "Plugin install failures... **Mitigation (user-confirmed, OQ2 round-3 resolution)**... HARD-BLOCK... This is option (a) from OQ2." Closed decision.
- **OQ3 does not exist** in `merged-requirements.md` (grep for OQ3/round-3-open/TBD/deferred/needs_human returns only the two resolved items + schema/provenance lines). There is no third open question in the spec.
- The spec is `revision: round-3 (user feedback merge)` (L6) — the OQ's were the round-2→round-3 questions that the user has SINCE answered. They survive in the text only as resolution annotations.

File 05 §3 compounds this by documenting OQ-item *shape* using a DIFFERENT precedent task (TASK-RF-20260517-213436's OQ-1/2/3), implicitly treating this feature's OQ1-3 as still-open — they are not. **Consequence for the builder:** authoring three PENDING/HALT items for OQ1-OQ3 would halt on decisions that are already made (OQ1, OQ2) or invent a nonexistent one (OQ3). This is the inverse failure mode of memory `feedback_human_decision_items_must_halt.md` — halting where no halt is warranted. The builder MUST reconcile the track-goal premise against the spec: only the **Python-vs-skill-prose boundary** (genuinely undecided per File 04 §4) is a true needs_human_decision item. The eval-reuse merged-vs-round-4 conflict (File 03) is a second genuine builder-decision. The "OQ1-OQ3 as 3 halt items" instruction is not supported by the spec and must be corrected to "document OQ1/OQ2 as already-resolved (cite L358/L378), drop OQ3 as nonexistent" — NOT three HALT items.

---

## Special-Attention Items (per spawn prompt)

### SA-1 — Python-vs-skill-prose boundary evidence sufficient for a HALT item (not a silent decision)? **YES — PASS**
File 04 §4 is exemplary. It (a) presents a per-step Python-vs-prose home table (§4.1, 16 steps), (b) gives evidence FOR Python-heavy (§4.2) and FOR prose-heavy (§4.3), (c) isolates the genuine tension (§4.4: line-113 table-inlining → prose vs line-414 ~150 LoC dispatch → Python), (d) names two coherent resolutions (Resolution H Haiku-heavy / Resolution P Python-heavy), and (e) explicitly states "DO NOT DECIDE — surfaced as evidence per task instructions." The decision-maker has enough to choose; the builder can author a true HALT item with both options stated. This is the ONE genuine needs_human_decision item the spec supports.

### SA-2 — .gitignore two-region edit (line 103 + after 118, last-match-wins) unambiguous? **YES — PASS**
File 06 §4 is precise and INDEPENDENTLY CONFIRMED against the live file: line 103 (`.claude/cache/`), line 117 (`.claude/` broad), line 118 (`!.claude/settings.json`). §4.3 states the load-bearing git semantics correctly: (a) negations must come AFTER the broad line-117 ignore (last-match-wins); (b) `!.claude/cache/` dir-re-include MUST precede per-file negations (parent-exclusion rule); (c) `.claude/cache/sc-recommend-events.jsonl` re-ignore MUST be LAST; (d) `eval-runs/` then `eval-runs/**` both needed. File 01 §2 corroborates and adds the line-103-is-redundant-but-harmless note + the CLAUDE.md user-authorization checkpoint. The builder has an unambiguous, git-correct edit recipe.

### SA-3 — Registration surfaces concrete enough for individual checklist items? **YES — PASS**
All three INDEPENDENTLY CONFIRMED:
- `main.py:400-426` — eval is the last group (L424-426), `if __name__` at L429; new lines go after 426. File 01/06 idiom (deferred import + `# noqa: E402,I001` + `main.add_command(recommend_group, name="recommend")`) matches the verbatim tasklist/eval precedents.
- `EXPECTED_TOP_LEVEL_COMMANDS` at `tests/cli/test_cli_registration.py:31` — frozen frozenset; `recommend` absent → must be added or `test_top_level_command_roster_unchanged` fails. Confirmed.
- `_FRESHNESS_SCRIPTS` at `install_hooks.py:43`; `sc-recommend-phase0.sh` at L85. settings.json `matcher: "Skill"` at L16, command at L21. All confirmed. Each is a separable, concrete checklist item.

---

## Contradictions Found

1. **Module name conflict (IMPORTANT).** Files 01 + 06 recommend `src/superclaude/cli/recommend/` (group name `recommend`, mirrors `tasklist`). Files 03 + 04 (and 03's "Files Touched" framing) use `src/superclaude/cli/sc_recommend/`. INDEPENDENTLY CONFIRMED: NEITHER exists on disk — both are greenfield. The builder must pick ONE canonical name. `recommend/` is better-supported (06 §3.1 ties it to `EXPECTED_TOP_LEVEL_COMMANDS` + the `recommend` command-group registration; the command name is `recommend`). The `sc_recommend/` token in 03/04 appears to be an unanchored choice. RECOMMEND the builder standardize on `cli/recommend/`. Surface, do not silently merge.

2. **SKILL.md line count (MINOR, already self-flagged).** File 01 says 226 lines; File 04 says 227 (and explicitly flags "brief says 226, actual 227"). Not a substantive conflict — File 04 already cross-validated. Use 227.

---

## Compiled Gaps

### Critical Gaps (block faithful task-building)
- **G1 — OQ1-OQ3 premise mismatch (Criterion 9).** Track goal says "OQ1-OQ3 = 3 needs_human_decision HALT items." Spec shows OQ1 (L358) and OQ2 (L378) are already user-RESOLVED round-3 decisions, and OQ3 does not exist. No research file caught this. Builder must NOT author 3 HALT items; correct to "Python-vs-prose boundary is the sole genuine HALT item; eval-reuse conflict is a second builder-decision; OQ1/OQ2 are resolved (document + cite); OQ3 is nonexistent (drop)."

### Important Gaps (affect quality)
- **G2 — Module name conflict** (`cli/recommend/` vs `cli/sc_recommend/`). Builder must canonicalize before authoring per-file items. RECOMMEND `cli/recommend/`.
- **G3 — Eval-reuse conflict unresolved (by design).** merged-requirements §259-269 (`.dev` scripts) vs round-4 §16,24,54 (cliEval harness). File 03 surfaces it as a builder decision point but does not resolve it — correct per scope, but it IS a decision the builder must make or HALT on.
- **G4 — Few-shot / classifier-key coverage gap.** Only 4 of ~10 proposed closed-enum keys have iteration-1 eval examples (File 04 §3.3). Keys 5-10 are surface-derived PROPOSALS needing human review / synthetic few-shots. The closed-enum membership is itself a `needs_human_decision`-adjacent design choice (spec L368 "deliberate human-reviewed expansion").

### Minor Gaps (must still be addressed)
- **G5 — `allowed-tools` frontmatter expansion.** Current SKILL.md:4 lacks `Edit`/`Write`/`Agent`/`Task`; hot path needs Agent + parent needs Write. File 04 §1.1/§5 flags it; builder must author an item.
- **G6 — Atomic-write temp-name choice.** convergence.save uses a FIXED `.tmp` name (concurrent-writer collision risk); File 06 §1.3 recommends the `install_hooks.py` randomized-temp variant for the worktree-concurrency risk (merged-req Risk #12), MVP punts to last-write-wins. Builder should note which variant.
- **G7 — Line-count drift (227 vs 226)** — use 227 per File 04's cross-validation.

---

## Depth Assessment
**Expected depth:** Deep (complex template-02 task, ~700 LoC feature, 6 parallel researchers).
**Actual depth achieved:** Deep. Data-flow traces (hot/cold path 10+6 steps, 04 §2.2-2.3), integration-point mapping (registration surfaces, 06 §3), pattern analysis (5 verbatim patterns, 02), reuse-vs-new master tables (03 §summary), per-step Python/prose home table (04 §4.1). Evidence is consistently file:line-anchored and several claims are code-cross-validated (the 227-vs-226 catch, the `generate_review.py`-does-not-exist catch, the `EvalOutcome`-has-no-token-field catch).
**Missing depth elements:** Only the OQ1-OQ3 substance (G1) — a gap of *extraction from the spec*, not a gap of investigation depth. The 6 files did not read merged-requirements.md's Risk section (L358/L378) closely enough to notice the OQs were resolved.

---

## Recommendations (before spawning the builder)
1. **Resolve G1 (Critical):** Re-scope the track goal's "OQ1-OQ3 = 3 HALT items" against the spec. The builder prompt MUST state: OQ1 (auto-eval) and OQ2 (plugin-precondition HARD-BLOCK) are round-3 RESOLVED (cite merged-requirements L358, L378) — document them as decided, do NOT halt; OQ3 does not exist — drop it. The genuine needs_human_decision items are: (a) Python-vs-skill-prose boundary (File 04 §4, HALT/Shape-3A since it gates implementation), and (b) eval-harness reuse conflict (File 03, builder-decision or soft-defer). Classifier-key membership (G4) is a third candidate human-review item.
2. **Resolve G2 (Important):** Canonicalize the module name to `cli/recommend/` and ensure all per-file items, the registration item, and tests reference it consistently.
3. Carry G3 (eval-reuse) and G4 (classifier keys) into the task as explicit decision/PENDING items per File 05's Shape 3A/3B guidance.
4. Author G5 (allowed-tools), G6 (atomic temp-name), G7 (use 227) as concrete items.
5. The pattern/registration/gitignore/template foundations (Criteria 1-8) are solid and code-verified — the builder can proceed on those without rework.

---

## VERDICT: FAIL

**Rationale:** 8 of 9 completeness criteria PASS with strong, code-verified evidence; the research is unusually rigorous (multiple self-caught doc-vs-code discrepancies). However, Criterion 9 surfaces a CRITICAL premise mismatch (G1): the track goal's "OQ1-OQ3 as three needs_human_decision HALT items" is contradicted by the spec, where OQ1/OQ2 are already round-3 RESOLVED and OQ3 does not exist — and NO research file caught this. Per the gate rule (any gap regardless of severity = FAIL, and a Critical gap that would cause the builder to author HALT items for already-decided/nonexistent questions), this is a FAIL. The fix is cheap and surgical (re-scope the OQ instruction + canonicalize the module name), not a re-research of the codebase surfaces, which are sound.

**Gap count:** 1 Critical (G1), 3 Important (G2-G4), 3 Minor (G5-G7). 2 contradictions (module name, line count).

---

_End of report._
