# Synthesis Quality Review — synth-01..04 (Tech Reference §1-2, §3-4, §5.1-5.3, §5.4-5.8)

**Analysis type:** synthesis-review (ADVERSARIAL STANCE)
**Date:** 2026-06-03
**Reviewer:** rf-analyst
**Code baseline for spot-checks:** HEAD `9e864860` (confirmed via `git rev-parse HEAD`)
**Files reviewed:** 4

| File | Target sections | Header Status field |
|------|----------------|---------------------|
| synth-01-overview-architecture.md | §1 Overview, §2 Architecture | Complete |
| synth-02-directory-dataflow.md | §3 Directory, §4 Data Flow | **In Progress** (top) / **Complete** (bottom) — MISMATCH |
| synth-03-subsystems-existing.md | §5.1-5.3 (built) | **In progress** (top) / **Complete** (bottom) — MISMATCH |
| synth-04-subsystems-target.md | §5.4-5.8 (target/external) | Complete |

**Inputs cross-referenced:** `technical_reference_template.md` v1.0.2; `00-evidence-index.md` (243 evidence rows).

---

## Overall Verdict: FAIL — 4 issues (0 critical / 2 important / 2 minor)

The synthesis content is of high quality: evidence density is excellent, every spot-checked `[CODE-VERIFIED]` path:line claim is accurate at HEAD `9e864860`, the PROPOSED framing is stated up-front, and no `[DESIGN]` claim is presented as built. The FAIL is driven by an **un-whitelisted fourth tag** introduced in synth-04 that breaks the demarcation contract the task pins ("EVERY architectural claim carries exactly one [CODE-VERIFIED]/[DESIGN — UNBUILT]/[EXTERNAL-VERIFIED] tag") and by **status-field self-contradictions** in two files. Both are surfaced regardless of severity per the gate's "any gap = FAIL" rule. None block assembly conceptually, but both must be fixed before the fragments are assembled into the canonical document.

---

## Per-File Review

### synth-01-overview-architecture.md — Verdict: PASS

| # | Check | Result | Evidence / Issue |
|---|-------|--------|------------------|
| 1 | Headers match template | PASS | §1 Overview with What/Who/Where/Key numbers; §2 with 2.1 High-Level, 2.2 Subsystem Map, 2.3 Key Design Decisions — matches template §1-2 structure. |
| 2 | Table column structure | PASS | Subsystem Map (#/Subsystem/Purpose/Primary area/Tag) and Key Design Decisions (Decision/What/Rationale/Tag) coherent; Tag column is an intentional demarcation-driven extension. |
| 3 | No fabrication beyond research | PASS | All claims trace to evidence-index rows (5.1-01..5.1-44, 5.4-16, XC-02, XC-11) or named source docs. |
| 4 | Evidence cites real paths | PASS | `pipeline/executor.py:41-60`, `process.py:73-95` cited; spot-checked accurate (see Spot-Check table). |
| 5 | Options ≥2 w/ pros/cons | N/A | Options analysis belongs to §6-8 (synth-05/06), not this fragment. |
| 6 | Implementation plan specific | N/A | Belongs to §12-14 fragment. |
| 7 | Cross-section consistency | PASS | Subsystems 5.1-5.8 enumerated here align with synth-03/04 subsection numbering. |
| 8 | No doc-only in Architecture/API | PASS | Architecture is built-side `[CODE-VERIFIED]` (kernel) + clearly-marked `[DESIGN]`/`[EXTERNAL]` bands; the BUILT band cites code path:line. |
| 9 | Stale findings surfaced | PASS | Tag legend (1.1) flags spot-check-over-research precedence (R4); design-vs-built demarcation explicit. |
| **+** | **Built-vs-design demarcation** | PASS | §1 opens with bold "CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE" + full tag legend table (1.1). Reads as a design reference, not a feasibility reformat. Every claim carries exactly one of the three sanctioned tags. |

### synth-02-directory-dataflow.md — Verdict: FAIL (Issue #2)

| # | Check | Result | Evidence / Issue |
|---|-------|--------|------------------|
| 1 | Headers match template | PASS | §3 (3.1 existing tree, 3.2 proposed layout, 3.3 naming), §4 (4.1 flow, 4.2 sources, 4.3 transformations) match template §3-4. |
| 2 | Table column structure | PASS | Data Sources (Source/Type/Location/Description/Tag) and Transformations (Transformation/Input/Output/Location/Tag) match template, plus Tag. |
| 3 | No fabrication beyond research | PASS | All adapter dirs explicitly `[DESIGN — UNBUILT]`; existing tree cites real files. |
| 4 | Evidence cites real paths | PASS | `sprint/config.py:374-492`, `pipeline/process.py:24-244`, `executor.py:23-35` — accurate. |
| 7 | Cross-section consistency | PASS | Contracts 1-4 referenced here align with synth-04 §5.6 contract table. |
| 8 | No doc-only in Architecture | PASS | Existing-tree facts table all `[CODE-VERIFIED]` with path:line; proposed layer clearly `[DESIGN]`. |
| 9 | Stale findings surfaced | PASS | `superclaude pipeline` not-a-root-command (5.7-32) surfaced in tree comment + facts table. |
| **+** | **Demarcation** | PASS | Strong CRITICAL banner; every hop tagged. |
| **—** | **Status field integrity** | **FAIL** | Header line 6 says `**Status:** In Progress`; closing line 264 says `**Status: Complete**`. Self-contradiction (Issue #2). |

### synth-03-subsystems-existing.md — Verdict: FAIL (Issue #3)

| # | Check | Result | Evidence / Issue |
|---|-------|--------|------------------|
| 1 | Headers match template | PASS | 5.1/5.2/5.3 each follow Purpose → Key Files → How It Works → Public Interface → Dependencies → Consumers → Conventions (template §5 structure). |
| 2 | Table column structure | PASS | Key Files (File/Purpose), Dependencies (Depends On/Type/Description), Consumers (Used By/How) all match template §5.1. |
| 3 | No fabrication beyond research | PASS | All claims map to evidence-index 5.1-*/5.2-*/5.3-* rows; spot-check labels (spot-01/02/03) cited. |
| 4 | Evidence cites real paths | PASS | Spot-checked `executor.py:41-60`, `process.py:134`, `_verify_checkpoints` :1519, CERTIFY callsites — all accurate. |
| 8 | No doc-only in Subsystem Ref | PASS | Every built fact carries path:line; `[DESIGN]` port-mapping bullets clearly fenced. |
| 9 | Stale findings surfaced | PASS | CERTIFY_GATE unwired, WIRING trailing→blocking, deviation classifier unwired, Path-A checkpoint skip, stubbed status/logs, `rerun-tasks` absent — all surfaced for §14. |
| 10 | Subsystem depth budget 40-200 | PASS | 5.1 ≈ 88 lines, 5.2 ≈ 73, 5.3 ≈ 85 — within the 40-200 band. |
| **+** | **Demarcation** | PASS | Built subsystems all `[CODE-VERIFIED]`; port mappings explicitly `[DESIGN — UNBUILT]` "not implemented." |
| **—** | **Status field integrity** | **FAIL** | Line 10 says `**Status: In progress**`; closing line 266 says `**Status: Complete**`. Self-contradiction (Issue #3). |

### synth-04-subsystems-target.md — Verdict: FAIL (Issue #1, #4)

| # | Check | Result | Evidence / Issue |
|---|-------|--------|------------------|
| 1 | Headers match template | PASS | 5.4-5.8 each follow the §5 subsystem structure. |
| 2 | Table column structure | PASS | Capability tables (Capability/Detail/Source URL), ownership matrix, dependency/consumer tables all coherent. |
| 3 | No fabrication beyond research | PASS | All external facts carry source URLs matching web-01..04 / evidence-index §5.7-5.8. |
| 4 | Evidence cites real paths/URLs | PASS | `[CODE-VERIFIED]` rows (counts 42/39/24/12; `sprint/models.py:692-777`) accurate; `[EXTERNAL]` rows carry URLs. |
| 8 | No doc-only in Architecture | PASS | 5.4 built facts carry path:line; 5.5/5.6/5.8 explicitly `[DESIGN]`; 5.7 explicitly `[EXTERNAL]`. |
| 9 | Stale findings surfaced | PASS | Beads Dolt-first correction, Backlog MCP additionalProperties:false, Mastra EE-licensing, `/sc:forensic` gap, plugins-mirror drift all surfaced. |
| 10 | Subsystem depth budget 40-200 | PASS | 5.4 ≈ 45, 5.5 ≈ 56, 5.6 ≈ 49, 5.7 ≈ 60, 5.8 ≈ 40 — within band. |
| **+** | **Tag whitelist (exactly one of 3)** | **FAIL** | Introduces a **fourth tag** `[DESIGN — NOT PROVIDED]` (legend line 5; used in 5.5 consumer row, throughout 5.8). Task requires EVERY claim carry exactly one of `[CODE-VERIFIED]`/`[DESIGN — UNBUILT]`/`[EXTERNAL-VERIFIED]`. The 4th tag is not whitelisted (Issue #1). |
| **+** | **Built-vs-design (substance)** | PASS | No `[DESIGN]`/`[NOT PROVIDED]` claim is presented as built; reading rule at top (line 6) is explicit and correct. The defect is taxonomy-only, not a built-vs-design confusion. |
| **—** | **5.7 inline path:line in an `[EXTERNAL]` subsystem** | NOTE | 5.7 "How It Works" folds `[CODE-VERIFIED]` seam citations (`pipeline/process.py:73-147`, `sprint/config.py:379-384`) into the external subsystem under a combined `[EXTERNAL-VERIFIED] + [CODE-VERIFIED]` tag (Issue #4 — borderline; see below). |

---

## Issues Requiring Fixes

| # | File | Severity | Check | Issue | Required Fix |
|---|------|----------|-------|-------|--------------|
| 1 | synth-04 | Important | Tag whitelist | A fourth tag `[DESIGN — NOT PROVIDED]` is defined (legend line 5) and used in the 5.5 "Consumers" governance-plane row and pervasively in 5.8 (CRITICAL banner line 230, key-components header line 234, dependencies/consumers rows 256/259). The task pins exactly three tags: `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]`. An out-of-contract tag breaks downstream tag-consistency tooling and the "exactly one of {3}" invariant. | Replace every `[DESIGN — NOT PROVIDED]` with `[DESIGN — UNBUILT]` (a not-provided control plane is a special case of unbuilt design). Preserve the "none of the 3 components supplies it" meaning in prose, not in the tag token. Remove the 4th-tag row from the synth-04 legend (line 5). Re-confirm no other synth file imported the token. |
| 2 | synth-02 | Important | Status field | Header `**Status:** In Progress` (line 6) contradicts closing `**Status: Complete**` (line 264). An "In Progress" header can wrongly signal to the assembler that the fragment is unfinished. | Set the header Status field (line 6) to `Complete` to match the verified-complete body, OR if genuinely incomplete, finish the fragment and update the footer. Body content IS complete (§3.1-3.3, §4.1-4.3 all present), so the correct fix is header → `Complete`. |
| 3 | synth-03 | Minor | Status field | Line 10 `**Status: In progress**` contradicts closing line 266 `**Status: Complete**`. Same failure mode as Issue #2; lower severity because the body is unambiguously complete and the inconsistency is a single stale token. | Set line 10 to `**Status: Complete**`. |
| 4 | synth-04 | Minor | Tag precision (5.7) | 5.7 is declared an all-`[EXTERNAL-VERIFIED]` subsystem (note line 169), but its "How It Works" paragraph (line 213) embeds two `[CODE-VERIFIED]` seam citations under a combined `[EXTERNAL-VERIFIED] + [CODE-VERIFIED]` tag. This is defensible (the sentence genuinely bridges external capability to the current seam) but the combined tag technically violates "exactly one tag per claim." | Split the bridging sentence so the `ClaudeProcess`/`sprint/config.py` seam facts sit in their own `[CODE-VERIFIED]` clause and the substrate-capability facts keep `[EXTERNAL-VERIFIED]`. Low priority — acceptable to leave if the combined tag is an accepted convention, but flag for the assembler. |

---

## Spot-Check Evidence (sample of `[CODE-VERIFIED]` claims vs source at HEAD `9e864860`)

12 distinct `[CODE-VERIFIED]` path:line claims verified against actual source. **All 12 CONFIRMED.**

| # | Claim (source synth) | Cited path:line | Verdict | What source shows |
|---|----------------------|-----------------|---------|-------------------|
| 1 | StepRunner protocol is the seam (synth-01/03) | `pipeline/executor.py:41-60` | CONFIRMED | `class StepRunner(Protocol)` with `__call__(step, config, cancel_check) -> StepResult`; docstring states runner NOT responsible for retry/gate/ordering. |
| 2 | `_gate_target()` prefers `.compressed.md` sidecar (synth-03) | `pipeline/executor.py:23-35` | CONFIRMED | Function returns sidecar `{stem}.compressed.md` when it exists, else original. |
| 3 | `ClaudeProcess` sole `subprocess.Popen` (synth-03) | `pipeline/process.py:134` | CONFIRMED | `self._process = subprocess.Popen(self.build_command(), **popen_kwargs)` at line 134; stdin-prompt rationale follows. |
| 4 | `build_command()` exact argv (synth-03/04) | `pipeline/process.py:73-95` | CONFIRMED | Produces `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>` + optional `--model`. |
| 5 | CERTIFY_GATE unwired; certify comment unbacked (synth-03) | `roadmap/executor.py:2205`; `build_certify_step`/`check_certify_resume` callsites | CONFIRMED | DAG terminates at `remediate` (:2196-2204); comment at 2205 claims dynamic construction; grep for the two builders returns ZERO non-definition callsites. |
| 6 | Path A skips checkpoints; sole `_verify_checkpoints` call (synth-03) | `sprint/executor.py:1519` | CONFIRMED | Only real callsite is :1519 (Path B); :1579 is a comment, :1811 is the def. No Path-A invocation. |
| 7 | `sprint rerun-tasks` ABSENT (synth-03) | tree-wide grep | CONFIRMED | `grep -rn "rerun-tasks\|rerun_tasks" src/superclaude/cli/sprint/` returns zero matches. |
| 8 | Trailing-gate failures advisory/warning-only (synth-03) | `pipeline/executor.py:175-186` | CONFIRMED | End-of-pipeline collects pending with `timeout=max(30.0, grace_period)`; failures hit `_log.warning(...)` only, never converted to FAIL StepResult. |
| 9 | `grace_period == 0` coerces TRAILING→BLOCKING (synth-03) | `pipeline/executor.py:211-214` | CONFIRMED | `if config.grace_period == 0: effective_mode = GateMode.BLOCKING`. |
| 10 | Harness counts 42/39/24/12 (synth-01/04) | dir listings | CONFIRMED | commands 42 `.md`, agents 39 `.md`, skills 24 `SKILL.md`, core 12 `.md`. |
| 11 | Tasklist exposes only `validate` (synth-02/03) | `tasklist/commands.py:31-82` | CONFIRMED | Single `@tasklist_group.command()` → `def validate(...)`; no `generate` subcommand. |
| 12 | `PipelineConfig.grace_period` default 0 (synth-03) | `pipeline/models.py:232` | CONFIRMED | `grace_period: int = 0`. |

> No fabricated, drifted, or contradicted `[CODE-VERIFIED]` citation was found in the spot-check sample. Citation hygiene across the fragments is strong.

---

## Summary

- Files passed: **1** (synth-01)
- Files failed: **3** (synth-02, synth-03, synth-04)
- Total issues: **4** — 0 critical / 2 important (#1 tag whitelist, #2 status) / 2 minor (#3 status, #4 5.7 combined tag)
- Critical issues (block assembly): **0**
- Spot-checked `[CODE-VERIFIED]` claims: 12/12 accurate at HEAD `9e864860`

**Assembly readiness:** Content is assembly-ready in substance. The 4 issues are taxonomy/metadata defects, not content defects — no fabrication, no built-vs-design confusion, no depth-budget violation, no missing evidence. Fix Issues #1-#3 (mechanical: one token-replace + two status-field edits) before assembly; Issue #4 is optional polish. After those fixes, re-run is expected to PASS.

**Demarcation verdict (task-specific check):** PASS on substance — the document reads as a PROPOSED design reference with up-front framing and tag legends (synth-01 §1 + 1.1); no `[DESIGN]` claim is dressed as built; every `[CODE-VERIFIED]` spot-check resolves to real `path:line`; every `[EXTERNAL]` claim carries a URL. The ONLY demarcation defect is the un-whitelisted `[DESIGN — NOT PROVIDED]` token (Issue #1), which is a vocabulary violation, not a built-vs-design integrity failure.
