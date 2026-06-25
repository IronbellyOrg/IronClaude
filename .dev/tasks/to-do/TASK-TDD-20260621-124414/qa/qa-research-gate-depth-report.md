# QA Report — Research Gate (Research-Depth Lens)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep (TDD research)
**Date:** 2026-06-21
**Phase:** research-gate (research-depth lens)
**Fix cycle:** N/A
**fix_authorization:** false (report-only)
**Lens:** Adversarial research-DEPTH review — judge whether the 7 research files (00–06) are deep enough to support a Heavyweight TDD, not merely structurally present.

**Files under review:**
- `research/00-prd-extraction.md`
- `research/01-runtime-surface-algorithm.md`
- `research/02-product-path-integration.md`
- `research/03-consumer-surfaces.md`
- `research/04-eval-path-integration.md`
- `research/05-reuse-and-boundaries.md`
- `research/06-skill-prose-demotion.md`
- (context) `research/reuse-audit.yaml`, `research-notes.md`, prior `qa/analyst-research-gate-A-report.md` (partition A, files 00–03, PASS)

**Adversarial mandate:** assume the research is shallower than it looks in at least 5 places. Five targeted depth probes (from spawn):
- (a) Is the 7-step algorithm actually understood and traced, or restated from runtime-surface.md headers?
- (b) Are OQ-DRS.2 invocation-site tradeoffs genuinely analyzed with coverage consequences, or hand-waved?
- (c) Is the reflect→audit import decision substantively argued with coupling cost, or merely named?
- (d) Are the 5 uc2 eval cases each understood (what each asserts), or just listed?
- (e) Does the research surface the real tension that `commands.py`/`_audit_once` covers only `superclaude reflect run`, not bare `claude -p /sc:reflect`?

---

## Overall Verdict: PASS — research is deep enough for a Heavyweight TDD; 6 depth-edge gaps to carry forward (0 CRITICAL, 1 IMPORTANT, 5 MINOR)

The research is genuinely deep on all five targeted probes. Probes (a)-(e) are SUBSTANTIVELY met,
not hand-waved — and I independently verified the load-bearing source claims of all 7 files against
actual source (every SKILL.md/runner.py/ensemble.py/contract.py/reachability.py/filetype_rules.py
line anchor, every `runtime_surface`-absence claim, every import-ban docstring) and every one
checked out EXACTLY. This is not a research set that restates headers; it traces algorithms,
argues tradeoffs with named costs, and catches real cross-file tensions the spec itself did not draw.

An adversarial depth read nonetheless surfaced 6 gaps. Per the no-leniency / ban-N-A rules they are
ALL listed below. None is a CRITICAL "too shallow to build from" defect; the honest read is the
research clears the Heavyweight bar and the gaps are depth-edges the TDD §22/§15/§6.4/§6 must close,
several already self-flagged by the research files as Open Questions or Gaps.

## Items Reviewed
| # | Check (depth probe) | Result | Evidence |
|---|---------------------|--------|----------|
| (a) | 7-step algorithm traced vs restated | PASS (deep) | File 01 traces all 7 stages with per-step Inputs/Decision-logic/Outputs + RS:Lnn citations; correctly decomposes 4b'+4b into 7; nails per-edge-vs-per-symbol reduction + count invariant; HONESTLY flags depth=1 "§4.0 convention" as an unresolved external ref (G&Q#3) and the missing 6th field name (G&Q#1). NOT header restatement. |
| (b) | OQ-DRS.2 invocation tradeoffs analyzed | PASS (deep) | File 02 gives a 4-row coverage matrix (commands.run / _audit_once / ensemble / Wave-1A) with coverage columns AND consequences (commands.py predates authoring → clobbered; _audit_once tier-agnostic chokepoint; ensemble misses Tier-1). Verified runner.py:421/426/445, commands.py:254/266 — exact. |
| (c) | reflect→audit import coupling argued | PASS (deep) | File 05 §7 weighs 3 options with the ACTUAL coupling cost named: audit defaults (UNKNOWN→SOURCE, dynamic→KEEP:monitor, depth>50) are the INVERSE of runtime-surface's asymmetric-cost doctrine → audit drift silently changes reflect gating. Cites runner.py:14-17 copy-over-import precedent + private-symbol risk. Verified import-ban = sprint/roadmap only, NOT audit. |
| (d) | 5 uc2 eval cases each understood | PASS (deep) | File 04 §3 covers each of 37-41 assertion-by-assertion + expected.yaml values + requirement-id map (37→FR-S9-04…41→FR-S9-07) + role distinction. Found the self-consistency-only caveat + target-routing fragility. NOT a list. |
| (e) | bare-skill path coverage tension surfaced | PASS (deep) | Surfaced in THREE files independently: file 02 (matrix — no CLI site covers bare claude-p; only Wave-1A shell-out does), file 03 (sprint consumer unbuilt), file 06 G1 (bare path → 4b/4b' prose CANNOT be fully demoted; needs an LLM-fallback emission branch — a demotion CONSEQUENCE the others didn't draw). |

---

## Findings (incremental)

### Depth Gaps (adversarial — what is thinner than it looks)

| # | Severity | Location | Depth gap | What the TDD must do |
|---|----------|----------|-----------|----------------------|
| DG-1 | IMPORTANT | Files 02/06 (OQ-DRS.2 resolution) | The bare-`claude -p /sc:reflect` coverage tension is SURFACED well but NOT RESOLVED to an actionable recommendation. File 02's matrix shows only a Wave-1A skill shell-out covers the bare path; file 06 G1 says the 4b/4b' prose then "CANNOT be fully demoted ... must retain an LLM-fallback emission branch." But no file commits to a recommended primary invocation site (research-notes Alt-1 lists three; none is ratified). The spec §2 NAMES `commands.py` as the writer — which the research correctly shows covers neither bare-skill NOR even Tier-1-vs-Tier-2 cleanly (the real chokepoint is `_audit_once`, not `commands.py`). This is the single most load-bearing open decision and the research stops at "weighable options," leaving the TDD to both decide AND reconcile the spec's now-shown-wrong `commands.py` naming. | §6.4 + §22: pick a recommended invocation architecture (recommended floor appears to be `_audit_once` for CLI tiers + Wave-1A shell-out for bare path, with a conditional/fallback demotion in SKILL prose), explicitly note the spec's `commands.py` naming is superseded by `_audit_once`, and state which paths get deterministic fields vs remain LLM-emitted. |
| DG-2 | MINOR | File 01 §4 (rootwalk depth=1) | The depth=1 semantics are admitted UNRESOLVED — file 01 G&Q#3 says "depth=1 §4.0 link-following convention is an external reference ... read SKILL §4.0 to confirm whether depth=1 means one referrer hop vs one file hop vs one symbol-edge hop before encoding the constant." The research did NOT actually go read SKILL §4.0 to pin this. For a Heavyweight TDD the rootwalk is a core decision engine and the meaning of its only numeric constant is left open. | §6/§7: read SKILL §4.0 and pin the exact hop semantics of depth=1 (it is the difference between a symbol reachable only via one intermediate being REACHED vs UNREACHED). |
| DG-3 | MINOR | File 01 G&Q#4 / File 05 §5 (root enumeration for non-Python) | Root enumeration is concrete ONLY for Python (`[project.scripts]` from pyproject.toml). For ts/js/rust/go the research explicitly says "command roots / route roots enumeration is undefined — likely a per-language degrade until a concrete enumerator exists." This is honest but leaves a multi-language algorithm with a Python-only spine; the rootwalk's REACHED-rescue cannot fire for 4 of 5 allowlisted languages. The depth here is "we don't know," which is acceptable but must be a TDD decision (degrade-by-default vs partial coverage) not a silent floor. | §6: state explicitly that non-Python rootwalk is degrade-by-default in v1 (REACHED-rescue is Python-only), so reviewers know the multi-language allowlist is aspirational for everything past TAG/PARTITION/ORACLE. |
| DG-4 | MINOR | File 04 §4.2 (Option A/B for deterministic eval) | The eval-determinism design names two options (A new oracle assertion type / B runner materializes contract.yaml) but does not recommend one, and Option A's own §Gaps#3 flags that a non-`target` oracle assertion would be SILENTLY DROPPED by the `target`-prefix bucketing (grader.py:448-449) — i.e. Option A as sketched is partially self-defeating unless the bucketing is extended. The research surfaces the trap but doesn't resolve whether Option A requires a grader change or whether Option B is therefore preferred. §15 testing strategy needs a committed approach. | §15: recommend Option A or B; if A, specify the `target`-key (or bucketing extension) the new assertion type needs so it is not dropped. |
| DG-5 | MINOR | File 03 §Gaps#3 (`per_task_verdicts[]` / `budget_forced_tier_downgrade`) | File 03 honestly admits it could NOT locate where `per_task_verdicts[]`, `per_task_validation_strength`, and `budget_forced_tier_downgrade` (cited by the §9.3 sprint consumer row at SKILL:885) are formally DECLARED — "not enumerated in the §9.1 stable block I read; possibly in a telemetry/second block beyond line 876 or in refs/; not confirmed." For a consumer-surfaces investigation feeding §5 requirements, the consumer's own field contract being unlocated is a real depth gap — though mitigated because AC-4's "sprint executor reads scalars" is shown to be entirely unimplemented today anyway (so the gap is bounded by the fact the whole sprint integration is spec-only). | §5/§8: if AC-4 sprint wiring is in scope, locate and cite the `per_task_verdicts[]` declaration; if out of scope, state AC-4 is producer-side-only and the sprint read is deferred. |
| DG-6 | MINOR | File 04 §1 entry-point / materializer (INFERRED chain) | The eval execution model has an unverified link: file 04 reads `grade_eval` reading `eval_metadata.json` but explicitly marks the `evals.json → eval_metadata.json` materializer as "[INFERRED] — no materializer was read this turn" (§1 + §Gaps#2). Option B (runner materializes contract.yaml) would live in exactly that unlocated materializer step. So the eval-path integration's recommended-Option-B hook sits in a component the research never actually read. The deterministic-eval wiring rests on an inferred-but-unverified seam. | §15: locate the materializer (the step that copies cases/uc2-*/ into iterations/iteration-N/eval-*/) before committing to Option B; confirm the hook point exists. |

### Why this is PASS, not FAIL (adversarial honesty check)

The spawn asked me to assume ≥5 places are shallower than they look and find them. I found 6 — but
they are overwhelmingly **honestly-self-flagged open edges** (DG-2/3/4/5/6 are all things the
research files themselves marked as Gaps/Questions/INFERRED), plus ONE genuine
research-stops-short-of-resolution gap (DG-1, the invocation-site decision). None of the 6 is a case
of the research **misrepresenting depth it does not have** — there is no fabricated trace, no
header-restatement masquerading as analysis, no unverified claim presented as verified. I
adversarially re-verified ~30 load-bearing source citations across all 7 files and found ZERO
inaccuracies (the only "stale" findings are the research correctly catching a real `contract_version`
"1.0" vs "1.6.0" mismatch and the line-number drift in the task brief, both of which strengthen
rather than weaken the research). A Heavyweight TDD can be built from this; the 6 gaps are §22/§15/§6
work-items, not research re-dos. That is the correct meaning of "deep enough."

A note on the prior partition-A report: it PASSED files 00-03 with 0 critical / 0 important / 3 minor.
My read concurs on those four files at the structural level and ADDS the depth-lens IMPORTANT (DG-1,
which spans 02+06 and is a cross-file resolution gap a single-partition completeness check would not
frame as a depth defect). I also confirm partition-A's noted Minor: file 01 carries `Status: In
Progress` at line 3 while closing `Status: Complete` at line 281 — presentation defect, file is
substantively complete (carried as a non-scored observation, not a depth gap).

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** ~30 load-bearing
   citations across 4 Bash verification batches: runner.py (`_audit_once`:394, Tier-2:421, rc=0:426,
   parse_contract:445, ClaudeProcess branches), commands.py (:254/:255/:266-267), ensemble.py
   (REFLECT_CONTRACT_VERSION="1.0":59, _emit_reflect_contract:500/508, build_reflect_contract:360),
   `runtime_surface` absence across ALL src/ .py files (zero matches — confirms the greenfield claim
   in files 01/02/03/04), executor.py TurnLedger:42 + no reflect import, SKILL.md anchors (§5.3:402,
   MANDATORY EMISSION:721-730, six fields:731-736, §9.3 advisory:890, §10.9:1055, chain lines
   465/466, self-label 487, §9.4 versioning rule), reachability.py (_bfs_reachable:591, depth>50:460,
   UNREACHABLE:30), filetype_rules.py (_TEST_PREFIXES:106, default-to-source:143-144), reflect
   import-ban docstrings (runner.py:9/config.py:8 = sprint/roadmap only), `_IndentDumper`
   copy-over-import precedent (runner.py:14-17). Every single one matched the research's claim.
2. **What specific files read to verify?** All 7 research files in full; plus source spot-checks via
   Bash grep/sed against: src/superclaude/cli/reflect/{runner,commands,ensemble,contract,config}.py,
   src/superclaude/cli/sprint/executor.py, src/superclaude/cli/audit/{reachability,filetype_rules}.py,
   src/superclaude/skills/sc-reflect-protocol/SKILL.md. Plus research-notes.md and the prior
   partition-A QA report for context.
3. **If 0 issues, why trust the check?** I did NOT find 0 issues — I found 6 depth gaps. But more
   importantly, the adversarial value here is the INVERSE finding: I tried to break the research's
   depth claims by re-verifying ~30 source citations and the research held on every one. The trust
   signal is the verification trail above, not an unexamined "looks good."
4. **Web research?** None performed — every probe was local-file/source-bound (algorithm port,
   invocation sites, import boundary, eval cases, consumer surfaces are all in-repo). No Tavily/
   WebSearch fallback was needed; Tool-engagement summary reflects zero web calls.

## Confidence Gate

- **Confidence:** Verified: 5/5 probes (+ ~30 source citations) | Unverifiable: 0 | Unchecked: 0 |
  Confidence: 100% (all 5 depth probes verified against the research files AND the underlying source;
  the 6 gaps are POSITIVE findings, not unchecked items).
- **Tool engagement:** Read: 9 (7 research files + prior QA report + research-notes; report Read x1
  for freshness) | Grep/Bash: 4 verification batches (~30 grep/sed assertions) | Glob: 0 | Write: 1 |
  Edit: ≥3 (incremental report build).
- Tool-engagement minimum check: Read(9) + Bash-grep(4 batches, ~30 assertions) >> 5 probes +
  7 files. Not suspect — verification volume exceeds the checklist.
- **Web tooling:** none invoked; no Tavily-vs-fallback record needed (no external lookup in scope).

## Summary
- Depth probes passed: 5 / 5 (all SUBSTANTIVELY met, not hand-waved)
- Source citations independently re-verified: ~30 / ~30 accurate (0 inaccuracies)
- Depth gaps found: 6 (0 CRITICAL, 1 IMPORTANT, 5 MINOR)
- Verdict: **PASS** — research is deep enough to support a Heavyweight TDD; carry the 6 gaps into
  §22 (DG-1, DG-2), §6 (DG-3), §15 (DG-4, DG-6), §5/§8 (DG-5) as named work-items.

## Recommendations
1. **DG-1 (IMPORTANT) before TDD §6.4 finalizes:** ratify a recommended invocation architecture and
   explicitly supersede the spec's `commands.py` naming with `_audit_once` + Wave-1A; state per-path
   determinism (which paths get deterministic fields, which stay LLM-emitted).
2. **DG-2/DG-3 (MINOR) in §6/§7:** pin depth=1 hop semantics from SKILL §4.0; declare non-Python
   rootwalk degrade-by-default in v1.
3. **DG-4/DG-6 (MINOR) in §15:** commit to eval Option A or B; if A, specify the `target` key so the
   oracle assertion is not dropped by bucketing; locate the evals.json→eval_metadata materializer
   before relying on Option B's hook.
4. **DG-5 (MINOR) in §5/§8:** locate/cite `per_task_verdicts[]` declaration if AC-4 sprint wiring is
   in scope, else mark AC-4 producer-side-only.
5. **Non-scored:** fix file 01's `Status: In Progress` header (line 3) → `Complete` to match its
   closing line.

## QA Complete
