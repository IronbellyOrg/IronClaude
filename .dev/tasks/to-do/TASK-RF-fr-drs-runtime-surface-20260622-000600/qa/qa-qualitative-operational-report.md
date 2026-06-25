# QA Report — task-qualitative (operational-correctness lens)

**Topic:** FR-DRS deterministic runtime-surface sweep + integration
**Date:** 2026-06-22
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (first pass)
**Fix authorization:** true

---

## Overall Verdict: PASS

No CRITICAL/IMPORTANT/MINOR issues found that survive verification. All cited
source surfaces exist (or are correctly greenfield), all runner-wire arg
constructions are operationally sound, the POST reflect gate is runnable, and
every quantitative claim cross-checked against source/research matched. Two
findings investigated adversarially (rootwalk status "partial" vs "DEGRADE";
`_git` source location) resolved to NON-issues with evidence. One MINOR
observation recorded (non-blocking).

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 0 (used `grep -n` via Bash) | Glob: 0 | Bash: 11

No web research was required (all verification was local-file / source-bound);
Tavily MCP was therefore not invoked.

---

## Items Reviewed (15-item task-qualitative checklist, operational-correctness lens)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `superclaude` on PATH (`/config/.local/bin/superclaude`), `reflect_group` registered (main.py:442), `run` cmd has `promote/depth/fix` params (commands.py:164); `make sync-dev`/`make verify-sync` are real targets; ruff scoped to changed files per item text; `rg` resolves (`command -v rg`->exit 0). POST gate exit codes `0/10/11/2` match commands.py:6,185. |
| 2 | Project convention compliance | none | PASS | All edits target `src/superclaude/` (module, runner, contract, SKILL); Step 4.5 runs `make sync-dev`+`make verify-sync` AFTER the SKILL src/ edit (correct order); items explicitly forbid `.claude/` edits; ruff `--check` scoped to changed files only (worktree mass-reformat hazard respected). |
| 3 | Intra-phase execution-order simulation | none | PASS | Phase 1 produces module before tests reference it; Step 1.4 line-anchor map feeds every later code item; Step 1.6 BFS/DATA copies precede Units 1-6; Step 2.1 inserts before 2.2 writes; Step 1.17 xfail un-xfailed at Step 2.3 (forward dependency correctly deferred). Phase serialization (1 BLOCKS 2-5) holds. |
| 4 | Signature/value verification | none | PASS | ReflectConfig genuinely has `base`/`tasklist_path`/`output_dir` and NO `diff`/`scope_worktree`/`availability_surface` (models.py:58-115) -- the 3-clean/3-constructed split is correct. `_audit_once`@394, `parse_contract`@445, `_IndentDumper`@58, `_atomic_write_text`@70 all confirmed. `_bfs_reachable`@591, `_TEST_PREFIXES/_INFIXES`@106-107, `_DYNAMIC_PATTERNS`@24, `_safe_parse`@164 confirmed. |
| 5 | Module context analysis | none | PASS | Step 2.5 count-invariant guard correctly mirrors the existing F2 `_LOAD_BEARING_BOOL_FIELDS` block (contract.py:200) incl. the `not isinstance(_count, bool)` bool-is-int guard (matches research/03 §3 suggested shape); `_make_result`/`Verdict.BLOCKED`/`child_rc` ambient deps exist (contract.py:104-109). Module isolation guardrails (no audit/sprint/roadmap import) baked into Step 1.5/1.6. |
| 6 | Downstream consumer analysis | none | PASS | The six `runtime_surface_*` fields flow producer(module)->runner merge->contract.py consumer->SKILL I6 branch; Step 2.x wires each consumer (token-membership, count guard, surface_unreached derivation); §5.3 pre-filter reads the DERIVED string (AC-4). Final-state Step 545 cross-phase consistency lens confirms agreement. SKILL §5.3/§9.1 consumers verified present (SKILL.md:390-412, 669-734). |
| 7 | Test validity | none | PASS | Tests exercise real units (read implemented signatures first); NFR-003 test scans actual module source; determinism test asserts byte/dict IDENTITY across 3 runs (not "passed"); §15.4a asserts exact STRING `"runtime_surface_unreached"` not truthiness. No `# Test`-style stub asserts. |
| 8 | Test coverage of primary use case | none | PASS | Unit tests (per-unit) + count-invariant N in {0,1,2} + fast-path + Phase-3 end-to-end determinism gate (5 uc2 cases 37-41 through materializer+oracle+grader) + AC-5 safety gate (cases 37/39/40/41). Primary pipeline covered end-to-end. |
| 9 | Error-path coverage | none | PASS | Degrade-to-floor on backend/LSP unavailable (exact `"runtime-surface:backend_unavailable"` token); fail-soft AST parse (None->DEGRADE); unknown-lang->DEGRADE; missing-contract tolerance in merge (Tier-2 M==0); count-invariant divergence->BLOCKED. |
| 10 | Runtime failure-path trace | none | PASS | diff->tag->(fast-path? exit)->find->partition->oracle->rootwalk->reduce->emit->merge-before-parse->consumer. Fast path writes no ledger (`ledger_path=None`). The 6-arg construction (`_git`-style `git diff <base>` + `rev-parse --show-toplevel`, force-floor) yields a real diff against working tree (de-range rule preserved). No downstream gate left un-updated. |
| 11 | Completion-scope honesty | none | PASS | OQ-DRS.1/.2/.3 recorded with RATIFIED markers reflecting actual implementation (force-floor, runner-path-only + SKILL-fallback for bare-path, no version bump); Q4 (ensemble REFLECT_CONTRACT_VERSION 1.0->1.6.0) explicitly KEPT as a carried Open Question, NOT silently closed. Phase 5 ratifies, does not pretend-resolve. |
| 12 | Ambient dependency completeness | none | PASS | `run_sweep` import added to runner.py (Step 2.1); `run_sweep` imported into produce_iteration.py for the eval oracle (Step 3.2); test imports enumerated (Step 1.14); contract.py token added to existing frozenset. No new entrypoint/CLI-arg surface needed (module is called internally). |
| 13 | Kwarg sequencing | none | PASS | No "add kwarg before add param" inversion: `run_sweep` is fully defined (Step 1.13) before it is called (Step 2.1, 3.2); the `surface_unreached` derivation (Step 2.3) lands before its xfail test is un-xfailed in the same step; count guard added after the six fields are merged. |
| 14 | Function-existence claims grep-verified | none | PASS | "runtime_surface.py does NOT exist" CONFIRMED (greenfield); ALL "exists at X" claims grep-confirmed: _audit_once, parse_contract, _IndentDumper, _atomic_write_text, _DEGRADED_COMPONENTS_HALT_SET, _LOAD_BEARING_BOOL_FIELDS, _degraded_reason, _halted_reason, REFLECT_CONTRACT_VERSION (="1.0", Q4), _bfs_reachable, _TEST_PREFIXES/_INFIXES, _DYNAMIC_PATTERNS, _safe_parse, _git (config.py:64), git_cwd (config.py:185), materializer scripts, 5 uc2 cases + 5 case dirs, grader functions. |
| 15 | Cross-reference accuracy for templates/specs | none | PASS | SKILL §6.1 4b'/4b anchors (SKILL.md:465/466/487/489/491), §9.1 `contract_version: "1.6.0"` (line 672, NO-bump claim correct), §5.3 surface_unreached rows (390/391/402/412) all confirmed present. §15.4a truth table in task (0->null,1/2->string,degrade-only->null) byte-matches research/03 §15.4a table. 14 designed types match research/01 §2 exactly. |

---

## Findings detail

### MINOR-1 (non-blocking observation) — POST gate treats exit 11 (degraded) as hard FAIL
- **Axis:** none (observation, not a defect)
- **Location:** Post-Completion item (task line 559)
- **Observation:** The POST reflect wrapper item treats exit 11 ("degraded —
  single-reviewer-fallback") as a HALT-worthy FAIL alongside 10/2. Per project
  memory (`reference_reflect_exit11_degraded_benign.md`), exit 11 can be a
  benign ensemble/calibrator-diversity degrade rather than a content failure,
  judged by `return-contract.yaml` status/regression fields rather than the exit
  code. The task's fail-closed treatment is the SAFER choice for a gate (it will
  HALT and surface the report for human judgement rather than silently pass a
  degraded run), so this is NOT a defect — it is conservative-correct. Recorded
  only so the executor/operator is not surprised by a HALT on a benign degrade;
  the item already instructs surfacing the wrapper report path on non-zero exit,
  which is exactly the right escape hatch. No fix applied (none warranted).

### Adversarially-investigated NON-issues (resolved with evidence)

**NI-1 (candidate AX-2 contradiction — rootwalk status enum mismatch):** research/01
§2 types `RootwalkResult.status` as `Literal["REACHED","UNREACHED","partial"]`
while task Step 1.6(a) + research/04 §1.3 describe the low-level `rootwalk_depth1`
helper returning `Literal["REACHED","UNREACHED","DEGRADE"]`. Investigated:
these are TWO DISTINCT artifacts at two layers — the helper returns the 3-state
DEGRADE form (research/04 §1.3 L98), the public-unit dataclass carries `partial`
(+ `enumeration_complete: bool`) which the reducer resolves to DEGRADE
(research/01 §2 L97: "`partial`/`enumeration_complete==false` -> DEGRADE"). The
task is faithful to both layers. NOT a contradiction.

**NI-2 (candidate AX-1/AX-5 — `_git` source location / runner subprocess ban):**
Step 2.1 says construct `diff` via "the `_git`-style subprocess" and cites "the
`git_cwd` precedent", but `_git` lives in `config.py:64` (not runner.py) and
runner.py:461 bans raw `subprocess.run`. Investigated: (a) the runner ban is
scoped to the reflect-LAUNCH path (ClaudeProcess), NOT a utility `git diff`
(runner.py:9-13 + the `_IndentDumper` "copy private symbol locally" precedent);
(b) research/09 GAP 3 is the AUTHORITATIVE, bound-by-reference source and is
explicit: use the `config.py` `_git(cwd, "diff", config.base)` shape, `git_cwd =
config.tasklist_path.parent`, both CODE-VERIFIED. The item references research/09
GAP 2+3 directly. The only residual ambiguity is copy-vs-import of `_git`, which
is trivially decidable by the executor and bounded by the authoritative research.
NOT a blocker; below MINOR threshold (the research the item cites resolves it).

---

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 1 (non-blocking observation)
- Issues fixed in-place: 0 (none warranted — no defect found)
- Axis lens status: drift axis ACTIVE (BUILD_REQUEST.GOAL "Implement FR-DRS
  deterministic runtime-surface sweep + integration per the TDD" available from
  spawn prompt). All 5 axes applied per row; none fired on any PASS row.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | (none) | — | No CRITICAL/IMPORTANT issue found | — |
| MINOR-1 | MINOR (observation) | task:559 | exit-11 treated as hard FAIL (conservative-correct, see detail) | None — fail-closed is the correct gate posture |

## Actions Taken
No fixes applied. fix_authorization was true, but no defect crossed the
MINOR-or-above threshold that warranted an in-place edit. MINOR-1 is a recorded
observation about a conservative-correct design choice, not a defect. Editing it
to soften the gate posture would REDUCE safety, so no change was made.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

**(a) Reliance list — rf-qa A.10 PASS items I relied on (skipped structural re-check):**
- Relied on rf-qa B2 self-containment PASS — did NOT re-verify the 5 B2 components per item, agent-spawn prompt embedding, or A3 granularity.
- Relied on rf-qa phase-structure PASS — did NOT re-verify frontmatter shape, 5-phase serialization, POST-gate FLAT-wrapper shape, QA-gate agent counts, or TB-Add-* structural checks.

**(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT (my own tool work required):**
- rf-qa confirmed the POST gate is the canonical FLAT wrapper *structurally*; INSUFFICIENT for runnability. I independently verified the `superclaude` binary is on PATH, `reflect_group`/`run` is registered, and the `run` command actually accepts `--depth/--fix/--promote` (commands.py:164) AND that the exit-code contract `0/10/11/2` the item keys off matches commands.py:6,185 — a semantic runnability check structure cannot give.
- rf-qa confirmed item B2 self-containment *structurally*; INSUFFICIENT for arg-construction soundness. I independently grepped models.py to prove ReflectConfig genuinely LACKS `diff`/`scope_worktree`/`availability_surface` (so the 3-constructed split is REQUIRED not optional) and traced `_git`/`git_cwd` to config.py:64/185 to confirm the constructed `diff = git diff <base>` is operationally realizable.
- rf-qa confirmed the count-invariant item exists *structurally*; INSUFFICIENT for correctness. I read contract.py:195-230 to confirm Step 2.5's guard faithfully mirrors the F2 block's bool-is-int handling — a code-compatibility check only source reading surfaces.

## Recommendations
- PROCEED. The task is operationally executable as written. No remediation required.
- (Optional, non-blocking) The executor may, at Step 559, distinguish a benign
  exit-11 degrade from a content failure by reading `return-contract.yaml`
  status/regression before HALTing — but the current fail-closed HALT-and-surface
  posture is acceptable and safer; this is operator discretion, not a task defect.

## QA Complete

---

## Self-Audit

1. **How many factual claims independently verified against source code?** 15
   checklist items, backed by ~30 distinct grep/read verifications across
   models.py, runner.py, contract.py, ensemble.py, config.py, the 4 audit
   sources, SKILL.md, refs/runtime-surface.md, evals.json, grader.py, the 2
   materializer scripts, and research/01/03/04/09. Every "exists at X" and "does
   NOT exist" claim in the task was grep-confirmed.
2. **What specific files did I read/grep to verify claims?** models.py (ReflectConfig
   fields), runner.py (_audit_once/parse_contract/_IndentDumper/_atomic_write_text +
   subprocess ban), contract.py (the 4 named symbols + F2 mirror block + _make_result),
   ensemble.py (REFLECT_CONTRACT_VERSION="1.0"), config.py (_git@64, git_cwd@185),
   commands.py (run cmd flags + exit codes), audit/{reachability,filetype_rules,
   dynamic_imports,wiring_gate}.py, SKILL.md (§6.1/§9.1/§5.3), refs/runtime-surface.md,
   evals.json (cases 37-41), grader.py, the 2 materializer scripts, and research 01/03/04/09.
3. **If I found ~0 blocking issues, why should the user trust the check was thorough?**
   I started adversarially and actively chased two candidate contradictions (NI-1
   rootwalk enum, NI-2 _git location) to ground rather than waving them through —
   both resolved to non-issues only AFTER reading the source/research that
   disambiguates them. I also verified runtime prerequisites that a structural
   pass cannot (binary on PATH, rg present, exit-code contract). The single MINOR
   is an honest conservative-design observation, not a manufactured finding. The
   task is genuinely high-quality because it is tightly bound to authoritative
   research (esp. research/09 superseding the TDD's [CODE-CONTRADICTED] arg claims)
   and every line number is grep-re-anchored at execution by design.
4. **Web research / Tavily?** No external lookup was required — all verification
   was local source/research-bound. Tavily MCP was therefore not invoked; no
   fallback occurred.

---

VERDICT: PASS

No unfixable issues. 15/15 operational-correctness checks PASS; 0 CRITICAL, 0
IMPORTANT; 1 MINOR non-blocking observation (conservative-correct exit-11 gate
posture — no fix warranted). The task is operationally executable as written.
