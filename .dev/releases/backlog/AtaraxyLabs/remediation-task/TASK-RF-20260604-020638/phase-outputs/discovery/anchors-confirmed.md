# Phase 1 — Anchor Confirmation (anchors-confirmed.md)

**Task:** TASK-RF-20260604-020638
**Target file:** `.dev/releases/backlog/AtaraxyLabs/merged-requirements.md` (286 lines, read in full)
**Date:** 2026-06-04
**Method:** Full Read of target (286 lines) for line-based anchors; Bash `grep -niE` for absence-based anchors (dedicated Grep tool unavailable in this environment).
**Verdict:** All 11 anchors accounted for. **No anchor drifted. No anchor absent.** The file is unmodified since the audit — Phase 2/3 edits can target the audit's original line numbers directly.

---

## Per-finding anchor status

| Finding | Expected anchor (from research note) | Confirmed location | Status |
|---------|--------------------------------------|--------------------|--------|
| **H1 §3** | "weave S0 blocked until inspect S4 live + KEEP" @ L95-96 | L95-96: `**Between-tool gate:** inspect S0 blocked until sem reaches S4 live + KEEP; weave S0 blocked until inspect S4 live + KEEP.` | ✅ present, not drifted |
| **H1 §8.2** | "inspect KILL does not block weave" @ L200 | L200: `*KILL* if precision ≈33% native AND complementarity below threshold AND FP noise above budget. inspect KILL does **not** block weave.` | ✅ present, not drifted |
| **H2** | `grep -i owner` / `grep -i raci` → NO match (not yet applied) | Bash `grep -niE "owner|raci"` → NO MATCH | ✅ absent as expected (H2 unapplied) |
| **H3** | `grep -i "security\|egress\|secret"` → NO match (not yet applied) | Bash `grep -niE "security|egress|secret"` → NO MATCH | ✅ absent as expected (H3 unapplied) |
| **H4 §7** | blind-adjudication language assuming a panel | L173-174: `**Blind adjudication:** hide tool source from judge; dedupe findings before precision/recall; require evidence citation; label severity ...` | ✅ present, not drifted |
| **H5 §2 G0-1** | corpus gate + §7 tiered minimums | L66 (G0-1 Corpus row: "Inventory ≥20 PRs + ≥10 merges (stratified) OR documented synthetic-backfill plan"); §7 tiered minimums L181-183 | ✅ present, not drifted |
| **H6 §4** | ~10 harness components, no runner contract | L116-118: `**Harness components:** corpus manifest · baseline runners · tool runners · token meter · latency meter · output normalizer (JSON) · finding deduplicator · adjudicator scoresheet · scorecard generator · decision-record template.` (10 components, no I/O contract) | ✅ present, not drifted |
| **M1** | generalization "gated behind native success" / "optional" @ L13/245/280 | L13 (frontmatter `eval_scope: ... generalization gated behind native success`); L245-246 (§11 "**generalization** ... gated behind native success"); L280 (§14 step 5 "**Generalization appendix** (optional)") | ✅ present, not drifted |
| **M2** | "vs Auggie" @ L125/136/190, no isolation method | L125 (`finding recall (%, vs Auggie pass)`); L136 (`prompt-input token delta (vs Auggie)`); L190 (`token reduction ≥30% vs Auggie`) | ✅ present, not drifted |
| **M3** | §7 tiered minimums (5PR/3merge vs 20PR/10merge), no interpolation | L181-183 (Tiered minimum evidence: shadow = 5 PRs + 3 merges; graduation = 20 PRs + 10 merges ...) | ✅ present, not drifted |
| **M4** | §8.3 weave `.md`/git ambiguity | L203-207 (§8.3 weave plan; `>1MB/binary/unsupported fallback` at L204, no explicit Python-only framing) | ✅ present, not drifted |
| **M5** | CP-1 / §12 `.md`-substrate risk buried | L229-231 (CP-1 post-sem substrate halt); L261 (§12 risk row "sem-core weak on Markdown/`.md` skill files \| High") | ✅ present, not drifted |

---

## Notes for downstream items

- **No drift:** every Phase 2/3 edit may use the line numbers above directly; the target file has not changed since the audit captured them.
- **H2 / M5 coupling:** the tie-break resolver is defined ONCE in §5 by H2 and merely *referenced* by M5 at CP-1/§12 — confirmed both anchor sites exist (§5 scorecard at L120-141; CP-1 at L229-231).
- **H3 insertion point:** no existing security section — H3 inserts a NEW "Security & Data-Handling" section; the research note suggests placement adjacent to the risk register (§12, L248) for coherence.
- **No fabricated line numbers:** every line citation above corresponds to content read directly from the 286-line target file in this session.
- **No blockers logged** — all anchors confirmed present/absent as expected.
