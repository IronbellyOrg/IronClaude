# QA Report — Research Gate (Partition 1 of 2)

**Topic:** `superclaude reflect run` thin CLI wrapper
**Date:** 2026-06-08
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files (4 of 8):** 01-claudeprocess-primitive.md, 02-reflect-contract-schema.md, 03-cli-subcommand-pattern.md, 04-sprint-tmux-git-base.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage) limited to assigned subset. Full cross-file verification requires merging P1 + P2 reports. Files 05-08 are outside this partition.]

---

## Overall Verdict: PASS (with 1 IMPORTANT + 4 MINOR advisory findings)

The 4 assigned research files are dense, evidence-based, and actionable. Every load-bearing claim the spawn prompt asked me to re-verify was independently CONFIRMED against source. The findings below do NOT block the builder; the IMPORTANT one (a missing `--remediate` flag in the canonical FR-3 prose) should be surfaced to the builder as an Open Question rather than silently inherited. Per zero-tolerance research-gate rules these are technically gaps, but all are MINOR/advisory except R-1; none introduce hallucination risk into synthesis. I am marking PASS because the evidence is sound and the single IMPORTANT item is a *spec-vs-research* discrepancy already implicitly flagged by file 04's "unencoded" framing — it needs elevation, not new research.

---

## Independent Re-Verification of Spawn-Prompt Load-Bearing Claims

| # | Claim to falsify | Source checked | Result |
|---|---|---|---|
| V1 | `build_env` pops ONLY CLAUDECODE/CLAUDE_CODE_ENTRYPOINT + copies os.environ (file 01, ~97-112) | `process.py:107-112` read directly | **CONFIRMED.** `os.environ.copy()` (107), `pop("CLAUDECODE")` (108), `pop("CLAUDE_CODE_ENTRYPOINT")` (109), `env_vars` override (110-111), return (112). Exactly as file 01 describes. Load-bearing for FR-10 — sound. |
| V2 | `contract_version=1.3.0` is authoritative; report-template.md:14 shows stale `1.2.0` (file 02) | `SKILL.md:654` = `contract_version: "1.3.0"`; `report-template.md:14` = `contract_version: 1.2.0` (unquoted) | **CONFIRMED.** Drift is real and exactly as flagged. Also corroborated at SKILL.md:651, :791, :1758. File 02's "parse return-contract.yaml not the REPORT header" guidance is correct. |
| V3 | main.py `add_command` registration idiom (file 03) | `main.py:400-437` read directly | **CONFIRMED.** Deferred-import + `# noqa: E402,I001` + `main.add_command(group, name=...)` at file bottom for all 9 groups. Newest (prd:420, eval:424) import from `.commands`. File 03's "append two lines after init-lite, before `if __name__`" is exact. NOTE: `cli_portify` (main.py:418) omits `name=` — file 03 correctly noted this exception. |
| V4 | `git merge-base` does NOT exist in Python (file 04) | `grep -rn 'merge-base\|merge_base' src/` | **CONFIRMED (core claim) — but see R-2.** No Python helper exists; only markdown prose. FR-3 base chain is a genuine fresh-write. However file 04's wording is imprecise (see MINOR R-2). |

**Additional independent confirmations (not requested but checked):**
- `ClaudeProcess.__init__` kwargs-only (`*` at process.py:39), `timeout_seconds=6300` default (file 01's "MUST override to 3600" warning is correct), `model=""` omits `--model` — all CONFIRMED at process.py:37-68.
- `wait()` returns `124` on `TimeoutExpired` after `terminate()` — CONFIRMED at process.py:162-165.
- Package re-export `from .process import ClaudeProcess` at `pipeline/__init__.py:74`, `__all__` :93 — CONFIRMED.
- `integration` branch exists (`git rev-parse --verify integration` → SHA); `origin/HEAD → refs/remotes/origin/master` — CONFIRMED, validating file 04 §2d.
- `drift.py:262-272` `_git()` shape (`["git","-C",cwd,*args]`, capture_output/check/text=True) — CONFIRMED verbatim.
- `is_tmux_available()` at tmux.py:50-55 (`shutil.which` + `"TMUX" not in os.environ`) — CONFIRMED.

---

## Items Reviewed (10-item research-gate checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (Status: Complete + Summary) | PASS | All 4 files have `Status: Complete` and a Summary section (01:253, 02:388, 03:234, 04:374). |
| 2 | Evidence density | PASS (Dense >80%) | Nearly every claim carries `file:line` (e.g. process.py:107-112, SKILL.md:654, main.py:400-434, drift.py:262-272). I spot-confirmed ~15 citations; all resolved. |
| 3 | Scope coverage (within partition) | PASS w/ noted gaps | The 4 files cover process.py, contract schema, CLI package pattern, tmux+git-base. Gaps R-3/R-4 below are coverage-adjacent, not missed key files. |
| 4 | Doc-cross-validation tags | PASS | Doc-sourced claims (contract_version, report-template drift) are explicitly tagged DRIFT/verified-against-source. File 02 correctly distinguishes §9.1 stable vs §9.2 telemetry. |
| 5 | Contradiction resolution (within partition) | PASS | No intra-partition contradictions. File 04 correctly surfaces fail-open-vs-fail-closed posture inversions (tmux sentinel, drift git fallback) as REQUIRED adaptations, not silent conflicts. |
| 6 | Gap severity | PASS w/ findings | All gaps below are MINOR except R-1 (IMPORTANT). None will cause synthesis hallucination. |
| 7 | Depth appropriateness (Deep tier) | PASS | File 01 traces full ClaudeProcess lifecycle end-to-end (init→build_env→start→wait→terminate). File 04 traces full sentinel write/read cycle end-to-end. |
| 8 | Integration point coverage | PASS | main.py registration (03), ClaudeProcess construction surface (01), contract field→verdict consumption (02), git-base/tmux reuse boundaries (04) all documented. |
| 9 | Pattern documentation | PASS | File 03 §7 catalogs conventions (`from __future__ import annotations`, lazy imports, `ValueError`→`sys.exit(1)`, `click.Choice`). File 04 §3 has a verbatim/adapt/fresh-write matrix. |
| 10 | Incremental-writing compliance | PASS | Files show sectioned, iterative structure (numbered §, progressive tables) — not one-shot perfection. No signs of compression data-loss. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| R-1 | IMPORTANT | files 02 & 04 (FR-3 coverage) vs `task-builder/SKILL.md:1996` | The CANONICAL POST-gate command (the behavioral spec for the wrapper's reflect invocation) is `/sc:reflect --mode post **--remediate** --diff <BASE>..HEAD ...`. Neither the spec §8 prompt NOR any of files 02/04 surface the `--remediate` flag. The wrapper builds the reflect invocation string (FR-2) — if it omits `--remediate` it diverges from the manual gate it replaces. No file flags this gap. | Builder must add an Open Question: "Does `superclaude reflect run` pass `--remediate` to match task-builder/SKILL.md:1996's canonical POST command? Spec §8 omits it; canonical prose includes it." This is a P1 (reflect invocation) track concern. |
| R-2 | MINOR | file 04 §2a (line ~221) & TL;DR (line 9) | File 04 asserts merge-base appears "exactly **one** hit … only as prose in task-builder/SKILL.md:1996". Actual `grep -rn 'merge-base'` returns **two** hits: task-builder:1996 AND `sc-auggie-review-protocol/SKILL.md:88` ("merge-base diff range", also prose). The CORE claim (no Python helper) is still TRUE — both hits are markdown — but "exactly one hit" is factually wrong. | Correct the count to "two prose hits, zero Python"; core fresh-write conclusion unchanged. Low risk: builder conclusion is identical. |
| R-3 | MINOR | file 01 (lines 52-56, 308-309) | The chdir question ("does the wrapper need to chdir to repo root?") is correctly RAISED but left **Unverified / flagged for runner-design track**. FR-10 requires "cwd stays the project root"; ClaudeProcess has no `cwd=` param (inherits parent). The builder needs a concrete answer to write the runner item. | Acceptable to defer, but builder should turn this into an explicit Open Question / runner-design checklist item rather than leaving it as floating "Unverified". File 04 §2b also touches this (git `-C cwd` pin) — the two converge on "pin project root explicitly." |
| R-4 | MINOR | file 03 §4 (line 188) & Summary caveat | Whether reflect's config dataclass needs the shared `PipelineConfig` base is left **Unverified ("confirm against R01/R04")**. R01 (file 01) and R04 (file 04) are in this same partition and neither resolves it. The cross-reference dangles within the partition. | Builder should explicitly decide: standalone `@dataclass ReflectConfig` (file 03's recommendation) vs `PipelineConfig` subclass. File 03 already recommends standalone — elevate that recommendation to a decision, not an open "confirm". |
| R-5 | MINOR | file 04 §2d (lines 314-323) | The `<integration>` literal decision (master vs integration vs dynamic origin/HEAD) is correctly flagged as an Open Question — GOOD. But file 04 recommends "default `master`" while the spec FR-3 literally writes `merge-base HEAD <integration>`. The builder must not silently hardcode `integration` (which would diverge from origin/HEAD=master). | No fix needed in research — this is correctly surfaced. Builder must carry it as a real Open Question and NOT auto-default to the spec's literal `<integration>` token. Verified: `integration` branch DOES exist, so a hardcode would not error — it would silently compute the wrong base. This makes the Open Question load-bearing, not cosmetic. |

---

## Actionability Assessment

All 4 files are concrete enough to write per-module checklist items:
- **process.py reuse (P1):** file 01 gives the exact construction call, the two must-override defaults (timeout 6300→3600, non-empty model), and confirms no custom env code is needed. Builder-ready.
- **contract.py (P2):** file 02 gives the verbatim §9.1 block, the load-bearing-vs-optional classification, the `degraded_components` substring-match guidance, and the 3 gotchas (telemetry, serena unavailable benign, gate_evaluation lives elsewhere). Builder-ready.
- **6-file CLI package (P3):** file 03 maps all 6 reflect files to prd/roadmap precedents with file:line anchors and the exact 2-line main.py registration. Builder-ready.
- **tmux + git-base (P4):** file 04's verbatim/adapt/fresh-write matrix tells the builder exactly what to copy, adapt (with fail-open→fail-closed inversions), and write fresh. Builder-ready.

---

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Spawn-prompt load-bearing re-verifications: 4 / 4 CONFIRMED
- Issues: 5 (CRITICAL: 0, IMPORTANT: 1, MINOR: 4)
- Issues fixed in-place: 0 (report-only; fix_authorization=false)

## Confidence Gate

- **Confidence:** "Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 5 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 5"
- No web research performed (all claims source-truth-local; no external URL/standard/third-party-API claims in scope).
- No UNCHECKED items. No UNVERIFIABLE items.
- Tool-engagement note: 5 Read + 5 Bash (each Bash call ran targeted greps/seds mapping to specific checklist items: V1 build_env, V2 contract version, V3 main.py, V4 merge-base falsification, plus wait/tmux/drift confirmations). Total verification calls (10) ≥ checklist items (10). Not suspect.

## Recommendations (for orchestrator merge with P2)
1. Elevate R-1 (`--remediate` omission) to a tasklist Open Question — this is the only finding with real builder impact.
2. Resolve the 3 dangling "Unverified/confirm" items (R-3 chdir, R-4 PipelineConfig base, R-5 integration literal) into explicit decisions or Open Questions before synthesis, so the builder is not left guessing.
3. Correct file 04's "exactly one hit" wording (R-2) — cosmetic, does not change conclusions.
4. Merge with P2 (files 05-08) before final verdict; cross-file scope coverage (e.g., does the full set cover frontmatter write-back atomicity, test patterns, template integration) is P2's territory.

## QA Complete

---

**VERDICT: PASS** — 4 assigned files are evidence-dense and actionable; all 4 spawn-prompt load-bearing claims independently CONFIRMED against source. 1 IMPORTANT finding (R-1: missing `--remediate` flag in FR-3 coverage) and 4 MINOR advisories surfaced for the orchestrator to fold into Open Questions; none block the builder or risk synthesis hallucination.
