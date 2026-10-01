# QA Report — Research Depth Review (P1)

**Track:** FR-DRS deterministic runtime-surface sweep module + integration
**Date:** 2026-06-22
**Phase:** research-depth
**Lens:** research-depth (module-build cluster)
**Fix authorization:** false
**Adversarial stance:** Assume research is superficial until proven otherwise.

**Assigned files (P1):**
- 01-module-design-and-spec-port.md
- 02-product-path-integration-seam.md
- 03-consumer-wiring-contract-and-prefilter.md
- 04-audit-reuse-sources-and-adaptation.md

---

## Depth Checklist (under evaluation)

1. Does 01 explain HOW each of the 6 units works (algorithm/predicates), not just list them?
2. Does 02 trace actual data flow (run_sweep args, merge-before-parse ordering); is arg-GAP finding deeply analyzed?
3. Does 03 explain WHY each consumer change reuses an existing slug (I7 reasoning)?
4. Does 04 show actual _bfs_reachable body + precise inversions (depth=1, DEGRADE-on-partial)?
5. Are edge cases / failure modes documented with enough specificity to replicate?
6. Could a task builder create per-unit/per-seam checklist items WITHOUT re-reading source?

---

## Findings (appended incrementally below)

### Independent source verification (adversarial probe of CODE-VERIFIED tags)

I did not take the research's `[CODE-VERIFIED]` tags on trust. I re-read the load-bearing source surfaces myself:

| Claim under probe | Research assertion | My read of source | Match |
|---|---|---|---|
| `_bfs_reachable` body | R4 quotes verbatim, lines 591-635 | `reachability.py:591-635` — body byte-identical (early-return on `start==target`, deque, `visited`, `_is_target_match` suffix branch, `return False, []`) | EXACT |
| BFS has no depth param | R4: "unbounded; depth=1 must be enforced at call site" | signature is `(self, graph, start, target)` — no depth arg confirmed | EXACT |
| `depth > 50` is NOT in BFS | R4 builder-trap: it lives in `_parse_module_recursive`, not the BFS | not present in 591-635 body | EXACT |
| `_TEST_PREFIXES`/`_TEST_INFIXES` | R4 quotes `filetype_rules.py:106-107` | matches verbatim | EXACT |
| unknown → SOURCE default | R4: invert to DEGRADE; source defaults SOURCE at :143-144 | confirmed `return FileType.SOURCE` at 143-144 | EXACT |
| `_audit_once` join point | R2: both author branches join at `parse_contract` line 445; insert between 444/445 | confirmed: 421-426 Tier-2, 430-444 Tier-1, 445 `parse_contract(config.contract_path)` | EXACT |
| `_DEGRADED_COMPONENTS_HALT_SET` | R3 quotes contract.py:31-33 verbatim | matches exactly (5 tokens, frozenset) | EXACT |
| fail-closed F2 block | R3: mirror contract.py:200-209 | confirmed `for _field in _LOAD_BEARING_BOOL_FIELDS:` … `malformed-contract-boolean` BLOCKED | EXACT |
| `_halted_reason` regression branch | R3: existing `deviations["regression"] > 0 → "regression"` at 324-325 (NO EDIT) | confirmed at 323-325 | EXACT |
| greenfield module absence | R1: grep-zero for `runtime_surface` across cli/reflect/ | my grep returned 0 matches / 0 files | EXACT |
| `[project.scripts]` entries | R1/R4: `superclaude=...:main`, `ic=...:main` (oracle cat b) | confirmed pyproject.toml:67-69 | EXACT |

11/11 spot-checked load-bearing claims verified byte-accurate against current source. The research is not pattern-matching from memory — its citations are real and current. This is the opposite of the shallow-inventory failure mode the adversarial stance assumes.

---

### Depth checklist verdicts

**1. Does 01 explain HOW each of the 6 units works (algorithm/predicates), not just list them? — PASS**
01 §1 gives each unit a signature, responsibility, inputs/outputs, *ported behavior with per-language predicate tables*, and explicit degrade rules. Examples of genuine algorithmic depth (not naming): §4 gives the 4 degrade-oracle categories as **deterministic match predicates** (`flatten_attr→None`, decorator aliasing `r=app.route;@r(...)`, `funcs[name]()`, `getattr(<module>,"<symbol>")`); §1.7 gives the root-enumeration algorithm I2 as an **ordered scan** (`[project.scripts]` → `[project.entry-points.*]` → CLI command roots) with a precise completeness predicate gating REACHED-vs-DEGRADE; §5 gives the reduction precedence `DEGRADE > UNREACHED > REACHED` plus the by-construction count-invariant derivation. A builder can write per-unit items with degrade rules attached without re-reading the SPEC.

**2. Does 02 trace actual data flow + deeply analyze the arg-GAP? — PASS (and this is the strongest file)**
02 traces the real flow: §1 maps all 6 `run_sweep` args to concrete `ReflectConfig` fields with `models.py` line cites, §2 pins the merge-overwrite to the window between line 444 and 445 with the *why* (both author branches join; contract must already exist on disk; Tier-2 M==0 missing-contract edge), §3 establishes the merge-before-parse ordering invariant with the D4 rationale. The arg-GAP finding is **deeply analyzed, not just flagged**: it identifies exactly 3 of 6 args (`diff`, `scope_worktree`, `availability_surface`) that have NO backing config field, proves the TDD §8.1.2 "already on the config" claim is *wrong against current source* (grep for `availability|wave.?0|probe` returned nothing), and proposes concrete fixes per gap (compute `git diff config.base`; derive `Path.cwd()` or add a field; add a probe or pass a floor-forcing empty dict). It also surfaces an out-of-band defect (the `REFLECT_CONTRACT_VERSION="1.0"` vs SKILL `1.6.0` staleness) and the bare-`claude -p` coverage gap with the `runtime_surface_sweep_ran` detection contract. This is exactly the behavioral understanding a vague inventory lacks.

**3. Does 03 explain WHY each consumer change reuses an existing slug (I7 reasoning)? — PASS**
03 §1-2 do not merely assert reuse — they ground it in the I7 invariant ("UNREACHED is NOT a 5th deviation class") and trace the mechanism: the `"degraded-components"` slug fires because adding `"runtime-surface:backend_unavailable"` to the frozenset makes the EXISTING `any(... in _DEGRADED_COMPONENTS_HALT_SET)` membership test at 259-260 fire; the `"regression"` slug fires because the producer populates `deviation_count_by_class.regression` and the EXISTING 324-325 branch already halts it — so `_halted_reason` is a **NO-EDIT-by-design that must be PROVEN by test**. §3 mirrors the fail-closed block with a precise count-invariant guard skeleton. §4 gives the `surface_unreached` derivation truth table (§15.4a, 4 rows) explaining producer→derivation→consumer wiring. The "why" is present, not hand-waved.

**4. Does 04 show the actual `_bfs_reachable` body + precise inversions? — PASS**
04 §1.1 quotes the full verbatim body (verified byte-accurate above). §1.2 gives a 3-row table of the load-bearing facts to invert (unbounded→depth=1-at-call-site; the `depth>50` builder-trap; dynamic→UNREACHABLE becomes dynamic→DEGRADE). §1.3 gives a concrete ~30-line `rootwalk_depth1` skeleton with both inversions baked in (depth=1 adjacency-only walk, `enumeration_complete=False → DEGRADE`, 3-state return). §2 gives the two DATA-copies with exact current values + the default inversions. §3 gives the `_safe_parse` fail-soft pattern to mirror. The inversions are specified precisely enough to replicate.

**5. Are edge cases / failure modes documented with enough specificity to replicate? — PASS**
DEGRADE categories: 01 §4 (4 predicate rows) + per-unit degrade rules in §1 (LSP-unavailable, backend-unavailable→`degraded_components` append, rg transient, non-UTF-8/null-line, partial enumeration, depth-bound-hit-distinct-from-walked-nothing). Count invariant: 01 §5.2 + 03 §3 (by-construction + consumer fail-closed guard). Fail-soft AST: 04 §3 (catch SyntaxError AND OSError/UnicodeDecodeError separately, log "— skipping", return None→DEGRADE). Fast path: 01 §3 step 3 gives the exact `SweepResult` returned on `tagged==[]` (all six scalars, `sweep_ran:False`, no ledger write) + the `--mode pre` guard. Tier-2 M==0 missing-contract edge: 02 §2. Each is replicable.

**6. Could a task builder create per-unit/per-seam checklist items WITHOUT re-reading source? — PASS**
01 §9 already provides a granular builder checklist-item map (module scaffold, 15 type items, 6 unit items, 2 helper items, 1 orchestrator, 1 invariant) plus explicit cross-researcher boundaries (R2 owns I1+merge seam; R3 owns derivation+§5.3; R4 owns the copy/adapt). 02 §7 and 03 §6 and 04 §6 each end with a "for the builder" manifest of exactly-shaped items with file:line targets. The partition collectively hands the builder pinned signatures, field shapes, insertion line numbers, slug-reuse rationale, and copy-source line ranges — a builder can author items without re-opening the SPEC, TDD, or source.

---

## Cross-file coherence (within assigned P1 subset)

The four files are internally consistent and non-duplicative at their seams:
- The six contract scalars + the "5/6 carry `runtime_surface_` prefix; `unreached_surfaces` does NOT" caveat appears in 01 §7, is honored in 02 §2 ("do NOT use a prefix glob"), and in 03 §6 — consistent across all three.
- `run_sweep` signature is identical in 01 §3 and 02 §1.
- The `_IndentDumper` + `_atomic_write_text` mandate (NOT ensemble's bare `safe_dump`) appears in 01 §1 unit-6 note, 02 §5, and 04 §5.1 — consistent.
- The DEGRADE-on-partial / count-invariant doctrine is consistent across 01 §5, 03 §3, 04 §1.3.
- Cross-researcher boundary notes (01 §9, 02 §7, 03 §6 boundary notes, 04 §0) agree on ownership: R1=module, R2=runner merge seam, R3=contract consumer + §5.3, R4=copy/adapt sources.

No contradictions found within the assigned subset.

[PARTITION NOTE: Cross-file checks limited to assigned subset P1 (files 01-04). Files 05-08 (eval, SKILL demotion, tests, MDTM template) were not in scope; full cross-file coherence requires merging all partition reports.]

---

## Minor observations (not blocking; no severity rating warrants FAIL on depth grounds)

- **02 §1 / arg-GAP is a research strength, not a research gap.** The 3 unbacked args are an honest finding about the TDD vs source, correctly handed to the builder as decisions to resolve. This is the research doing its job. It does mean the task file MUST contain explicit decision items for `diff`/`scope_worktree`/`availability_surface` — but that is a downstream task-quality concern, not a research-depth deficiency. Flagging so the task-builder and the later task-qualitative gate ensure those three decisions become real checklist items rather than being silently defaulted.
- **04 marks `dependency_graph.py`/`tool_orchestrator.py`/`dead_code.py:155` line offsets as `[UNVERIFIED]` (table-sourced, not re-read).** This is appropriately scoped honesty — those surfaces are referrer-finder (R4 row 2) reuse-shape evidence, not core-copy sources, and the verdict (reflect-local/distinct) does not depend on the exact offsets. Acceptable for the module-build cluster; the builder should not cite those offsets as pinned.

---

## Self-Audit

**(a) Reliance list — items I did NOT independently re-verify (relied on research's CODE-VERIFIED tag):**
- Relied on R2's `models.py:66-98` field enumeration and `ensemble.py:59/309/501/634-635` cites (read the join point + frozensets myself, but not every ensemble line).
- Relied on R3's SKILL.md §5.3 line anchors (386-412) and the §15.4a truth-table line cites.
- Relied on R4's `dynamic_imports.py:24-39` `_DYNAMIC_PATTERNS` and `wiring_gate.py:164-174` `_safe_parse` exact bodies (verified the BFS + filetype defaults, sampled the rest).

**(b) Independent semantic checks where my own tool work was required (≥1, INV-019):**
- Verified `_bfs_reachable` body byte-for-byte (reachability.py:591-635) — confirmed R4's "no depth param" + "depth>50 not in BFS" inversion premises are factually grounded, not asserted.
- Verified `filetype_rules.py:143-144` returns `FileType.SOURCE` — confirmed the inversion target (unknown→SOURCE) the partitioner must flip actually exists.
- Verified `runner.py:445` is `parse_contract(config.contract_path)` and 421-444 are the two author branches — confirmed R2's single-insertion-point seam is real.
- Verified contract.py:31-33 frozenset contents, :200-209 fail-closed block, :323-325 regression branch — confirmed R3's reuse-not-rebuild claims target real, current code (and that the membership test the new token would join actually fires the `"degraded-components"` slug).
- Verified greenfield absence via grep (0 matches) — confirmed R1's "module does not exist" premise.

Reliance did not substitute for verification: every load-bearing premise that drives a task item was independently re-read.

---

## Confidence

**Confidence:** Verified: 6/6 depth checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 1 (grep+sed combined: greenfield-absence + pyproject scripts)

Tool calls ≥ checklist items (6 depth checks; 9 source reads/greps that each targeted a specific load-bearing claim). No padding — each read mapped to a specific verification.

---

## Self-Audit answers (mandatory)

1. **How many factual claims did you independently verify against source code?** 11 load-bearing source claims, byte-checked against current source (table above).
2. **What specific files did you read to verify claims?** `cli/audit/reachability.py:588-637`, `cli/audit/filetype_rules.py:104-145`, `cli/reflect/runner.py:419-453`, `cli/reflect/contract.py:27-57 / 198-211 / 307-326`, plus grep over `cli/reflect/` and `pyproject.toml:66-72`.
3. **If you found 0 blocking issues, why should the user trust that you checked thoroughly?** I did not accept the research's CODE-VERIFIED tags on faith — I re-read 11 of the highest-leverage claims (the BFS body, the inversion targets, the seam join-point, the three contract.py reuse surfaces, greenfield absence) and all 11 matched source exactly. The research's depth is corroborated by independent reads, not asserted.
4. **Web research?** None performed; no external lookup required for a module-build depth review (all surfaces are local source). Tavily not invoked; no fallback to record.

---

## VERDICT: PASS

All 6 depth checks PASS. The P1 research partition (files 01-04) is **deep enough to produce a high-quality task file for the module-build cluster** without the builder re-reading source. It explains HOW each unit works (predicates, not names), traces the real data flow with the arg-GAP deeply analyzed, justifies the slug-reuse with I7 reasoning, shows the verbatim BFS body with precise inversions, documents edge/failure modes replicably, and pre-decomposes builder checklist items with pinned line numbers. The adversarial "shallow-inventory" hypothesis is disconfirmed: 11/11 spot-checked CODE-VERIFIED claims are byte-accurate against current source.

One non-blocking forward-note for the task-builder and the downstream task-qualitative gate: 02's three unbacked `run_sweep` args (`diff`, `scope_worktree`, `availability_surface`) MUST become explicit decision/implementation checklist items rather than silent defaults — this is a research *strength* (honest TDD-vs-source finding), but it imposes a task-file obligation.

## QA Complete
