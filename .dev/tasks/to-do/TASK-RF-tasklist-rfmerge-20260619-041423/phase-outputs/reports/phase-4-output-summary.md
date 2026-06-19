# Phase 4 (P3 — DNSP Synthetic Findings) Output Summary

**Generated:** 2026-06-19 (Step 4.G1) for the M3 lens-based QA gate.
**Proposal:** P3 — Stage-7 synthetic-dnsp finding on some-vs-zero agent failure, reusing task-builder DM-003 VERBATIM.
**Spec:** FR-RFMERGE.3. **Pins:** research/08 R-1 (`retry-1` exhaust-point), R-16 (7-field framing). PRE-advisory OQ-PRE-1 (synthetic excluded from P2 F_k) folded in as a forward note.
**Reuse source:** task-builder DM-003 / DNSP Synthetic Finding Protocol (`task-builder/SKILL.md:877-911`).

## Files touched / created

| File | Change | Verbatim edit location |
|------|--------|------------------------|
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | P3 merge step (Step 4.1) | New merge step `1a.` at **line 1340** in the Stage-7 `**Orchestrator merge and deduplication**:` list (between "collect" step 1 and "dedup" step 2). Emits the DM-003 7-field record VERBATIM: `severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range` (byte-for-byte fan-out slice), `evidence` (never blank), `recommendation` (`Manual review required — partition agent failed twice`, em-dash), `dedup_key` `["<stage7_affected_range>", "retry-1"]`, `found_n_times: 1`. Normal-stream Markdown block, strictly additive, HIGH non-overridable; includes the OQ-PRE-1 forward note (non-patchable synthetic excluded from P2's patchable `F_k`). |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | P3 some-vs-zero gate (Step 4.2) | `**Stage gate (some-vs-zero success branch — P3):**` at **line 1367**, replacing the old binary "Zero agent failures" gate. ≥1-success-AND-≥1-fail → synthesize + PROCEED (Stage 8 not blocked); ZERO-success → existing escalation (R-122 Path A analogue, MAPPED), NO synthetic. Notes no `StageError` symbol exists (typed error would be a NEW decision, not a reuse claim). |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | P3 short-circuit guard (Step 4.3) | `**Synthetic-dnsp short-circuit guard (P3):**` at **line 1389**, after the Stage-8 zero-finding short-circuit. A synthetic IS a finding → short-circuit MUST NOT fire when one is present; FAIL-until-manual-review; gap-fill MUST NOT auto-resolve. Genuine zero-finding short-circuit unchanged. |
| `tests/tasklist/test_tasklist_cli.py` | P3 tests (Steps 4.6/4.7) | `class TestP3DnspSyntheticFindings` at **line 438**: `test_dnsp_synthetic_provenance` (441 — asserts DM-003 fields + em-dash literal + `retry-1` dedup_key + found_n_times) and `test_dnsp_all_agents_fail_escalates` (458 — some-vs-zero branch + NO-synthetic-on-zero + no-StageError-reuse). |
| `tests/skills/test_task_builder_merge.py` | P3 reuse-not-fork test (Step 4.8) | `TASKLIST_SKILL_PATH` constant + `tasklist_skill_text` fixture (top); `class TestTasklistDnspMapsDM003::test_tasklist_p3_reuses_dm003_contract` at **line 547** — asserts the fixed DM-003 values appear in BOTH task-builder (SoT) and the tasklist generator (mirror) + `retry-1` pin, confirming consumer/mirror not fork. |

## Handoff artifacts

- `test-results/p3-sync-dev.txt`, `p3-verify-sync.txt` — both clean.
- `test-results/p3-pytest.txt` + `p3-pytest-summary.md` — 151 passed (+3 new, zero regressions).

## What the lens agents must verify (acceptance criteria from Steps 4.1-4.8)

1. **DM-003 contract-reuse fidelity:** all 7 fields; `severity: HIGH` + `source: "synthetic-dnsp"` fixed/exact; `recommendation` byte-exact with em-dash (NOT hyphen, NO `on this range` suffix); `dedup_key` 2-element list, 2nd = `retry-1` from closed vocab; `found_n_times` default 1; normal-stream Markdown (no sideband); HIGH non-overridable; strictly additive.
2. **Branch logic / internal-consistency:** ≥1-success-AND-≥1-fail → emit+proceed; zero-success → NO synthetic + escalation; retry-once primitive preserved; Stage-8 short-circuit guard fires only when synthetic present and doesn't break the genuine zero-finding short-circuit; the three edits are mutually consistent.
3. **Evidence-quality / test-coverage:** tests assert source-of-truth `src/superclaude/...`; each DM-003 field/value (incl. byte-exact recommendation + `retry-1`) exists; all-agents-fail test pins the NO-synthetic zero-success guard; non-vacuous; zero regressions.
4. **Silent-pass prevention:** a single post-retry agent failure (≥1 sibling success) can no longer ship unvalidated content silently — forces HIGH into Stage 8; short-circuit cannot swallow it; FAIL-until-manual-review preserved.
5. **No-fork / map-not-copy:** P3 reuses the per-agent emission/merge WIRE contract verbatim but legitimately MAPS `affected_range` to the Stage-7 2N fan-out unit (not a copy of partition-cohort R-122/INV-021 machinery); any typed-error mention framed as NEW decision, not a `StageError` reuse claim.
6. **Domain-accuracy:** matches spec FR-RFMERGE.3 + R-1 (`retry-1`) + R-16 (7-field framing); no requirement dropped; no behavior beyond spec.
