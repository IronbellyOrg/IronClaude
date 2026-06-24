# QA Report — Research Depth (research-depth lens)

**Topic:** Pipeline Hardening Closure (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** research-depth
**Lens:** Is the research deep enough to build a high-quality MDTM tasklist without re-reading sources?
**Fix authorization:** false (report-only)
**Adversarial stance:** Assume research is superficial until proven otherwise.

---

## Overall Verdict: PASS

The research is **deep enough** to build a high-quality MDTM tasklist for Pipeline Hardening Closure (H0-H5) **without re-reading the RELEASE-SPEC or re-deriving facts from code**. Both focus files (07, 05-v2) survive adversarial verification: every spot-checked claim is accurate against the actual spec and the actual codebase. No CRITICAL, IMPORTANT, or MINOR depth gaps found that would force a builder back to sources.

---

## Depth Checklist (5 items from spawn lens) — Results

| # | Depth question | axis-of-doubt probed | Result | Evidence |
|---|----------------|----------------------|--------|----------|
| 1 | Can a builder write each new ref's content from 07 + spec — EXACT schema fields + truth-table rows — without re-deriving? | "07 just lists section names" (superficial) | **PASS** | 07 §5 reproduces all 5 artifact schemas (H0 boundary scan, H1 card, H2 ledger, H3 sweep, H4 manifest) field-by-field WITH the `Required` flag per field (07 L263-321). §5.4 truth table all 7 rows verbatim (07 L207-216). §5.5 all 10/11 fields with type/required/default/nullability/producer/consumer-if-missing (07 L243-255). This is content, not a TOC. |
| 2 | Does 05-v2 give concrete insertion ANCHORS (heading text) for SKILL/report-template/remediation-handoff — not just "file exists"? | "the file exists" hand-wave | **PASS** | 05-v2 §E gives exact heading anchors: `### Wave 1.7`, `### Wave 2`, `### Wave 5`, `## Output Contract` (verified at SKILL.md lines 251/271/385/37). §C names `## Audit` (196), `## Rendering rules` (205), `## Test-is-wrong rule` (212) as the post-template region for the closure section (verified). §D names the `BUILD_REQUEST` block (L42-56) + user-offer block (L9-28) in remediation-handoff. It also warns "anchor on heading TEXT, not line numbers — they drift after edits" (§E L66, §F L103). |
| 3 | Are test specs detailed enough (name, file, assertion, FR/escape) to write one checklist item per test? | "tests listed by count only" | **PASS** | 07 §9 gives all 12 unit + 5 integration + 6 E2E tests with exact test name, target file (`tests/troubleshoot/test_hardening_h{0..4}.py`, `_verdict.py`, `_output_contract.py`), and what each validates (FR + adversarial escape F-N3/F-SC1/F-D1/F-S1/F-A1). Plus explicit FR→test (§9.4), escape→test (§9.5), NFR→test (§9.6) maps. One checklist item per test is directly writable. |
| 4 | Is the advisory invariant + §5.4 blocked-vs-advisory distinction + one-way waiver latch explained well enough to encode the DISTINCTION (not just list tokens)? | "lists tokens, loses semantics" | **PASS** | 07 §3.0 flags the 4-token enum and that ROWS 5+6 emit `advisory` (verified verbatim against spec L392-400). §3.1 reproduces priority ordering (FAIL sticky outranks advisory; latch checked before downstream success). §3.2 H5 decision→status mapping (4 rows). §3.3 backtest-vs-verdict (3 rows). Downstream no-override rule verbatim incl. `success_with_hardening_blocker/advisory` rendering (07 L227 = spec L411). §4.5 latch semantics: `none`→`latched` one-way, forces verdict ∈ {blocked, advisory} (07 L161,L168). The DISTINCTION is encoded, not just the token list. |
| 5 | Are edge cases / failure modes documented (empty ledger FAIL, wrong-surface fail-closed, N/A-without-rationale → blocked, downstream no-override)? | "happy path only" | **PASS** | 07 §7.1 reproduces the §5.2 guard boundary table (6 rows): H2 empty ledger→FAIL, H2 dead/legacy needs unreachability proof, H3 substring→word-boundary, H4 wrong-surface→FAIL-closed, H4 empty→FAIL-closed, H5 waived→latch. §3.1 truth-table row 4 = N/A-without-rationale→blocked. Phase-contract YAML (§7.2) encodes `# FAIL if unclassified>0 OR ledger empty`, `# FAIL closed if !surface_correct`, `# never upgraded post-latch`. All five named failure modes present. |

**5/5 depth checks PASS.**

---

## Adversarial Verification — claims independently re-tested against ground truth

The spawn demanded I assume superficiality until proven otherwise. I re-tested the most load-bearing claims directly:

### Cross-validation claims (05-v2) — all CONFIRMED against actual code
- 6 new refs ABSENT — **CONFIRMED** (`ls refs/` shows 8 existing files; none of the 6 spec §4.1 names present).
- `tests/troubleshoot/` does NOT exist — **CONFIRMED** (`ls` → No such file or directory).
- 4 modified files exist at claimed byte sizes — **CONFIRMED** (SKILL.md 55634, troubleshoot.md 13293, report-template.md 16909, remediation-handoff.md 5434 — all exact).
- SKILL.md heading anchors — **CONFIRMED at exact lines** (## Output Contract:37, ## Wave Structure:77, ### Wave 1.7:251, ### Wave 2:271, ### Wave 5:385).
- report-template post-template rule sections — **CONFIRMED** (## Audit:196, ## Rendering rules:205, ## Test-is-wrong rule:212, ## Behavior-is-documented rule:233).
- `NOT PROVEN` / `pass|blocked|advisory` enum absent in report-template today (net-new) — **CONFIRMED** (grep returns nothing).
- `diagnosability_verdict` sibling enum style — **CONFIRMED** (SKILL.md:58 `sufficient|partial|insufficient|unknown`).

### Spec-extraction claims (07) — all CONFIRMED verbatim against the spec
- §5.4 truth table 7 rows incl. advisory on rows 5+6 — **CONFIRMED byte-for-byte** (spec L392-400). 07's "advisory removed is FALSE" defensive warning protects a REAL invariant.
- Downstream no-override rule + `success_with_hardening_*` rendering — **CONFIRMED verbatim** (spec L411).
- FR-6 GAP (only indirect test coverage today) — **CONFIRMED**: no `test_h2_sibling*` in spec; FR-6 appears only as §3 FR + in the E1 traceability row. The proposed NEW test `test_h2_sibling_sweep_required_when_concept_shared` in `tests/troubleshoot/test_hardening_h2.py` (G-PRE-1) is correctly targeted.
- OI correction to task brief — **CONFIRMED**: spec §11 marks OI-1/OI-4/OI-6 "Resolved in §5.4/§5.7"; OI-2/OI-3/OI-5 defer to Roadmap M2 / G1 approval. 07's correction (HALT items are OI-2/OI-3/OI-5, NOT OI-1/4/6) is accurate and prevents a builder error.
- §10 line-596 sc:tasklist guidance (per-FR atomic tasks, DoD = AC + unit test, FR-12 highest-risk paired with NFR-4) — **CONFIRMED verbatim**.

### Depth of the 4 non-focus research files
01 (157 lines / 23 structured), 02 (197/33), 03 (316/52), 04 (223/21), 06 (148/5). 03 and 04 are heavily-tabled (refs-conventions + MDTM template/examples); 06 is shorter but its substance (sync model + lint gates) is duplicated and cross-verified in 05-v2 §F. No file reads as a thin placeholder.

---

## Builder-readiness extras the research already supplies (beyond the 5 lens items)
- §4.6 7-group implementation order with explicit parallelism note (group 3 = H1+H2+H4 parallel; H3 sequenced after) — gives ordered phasing for free.
- §4.7 6 validation components mapped to ref + test file — gives the executable-validation checklist items.
- G1-HALT constraint (07 §12): implementation halted pending G1; NO `src/` or `.claude/` skill/command edits pre-approval. Builder must gate implementation items behind G1 — research flags this explicitly (aligns with memory `feedback_human_decision_items_must_halt.md`).
- markdownlint scope nuance (05-v2 §F): `.dev/` excluded but target `src/superclaude/skills/...*.md` ARE linted; MD025 single-H1, MD040 fenced-language, MD024 siblings-only — directly actionable for the new refs.
- `.claude/` sync discipline (05-v2 §A claim 5, §F): edit `src/` only → `make sync-dev` → `make verify-sync`; do NOT stage `.claude/` mirrors — aligns with the ABSOLUTE rules in CLAUDE.md.

---

## Issues Found

None of any severity. The research is genuinely deep, not surface-level. The one item worth a builder NOTE (not a defect — the research already calls it out): the FR-6 NEW-test (G-PRE-1) and the FR-12↔NFR-4 pairing are reflect-pre additions on top of the spec's own §8 plan; the builder must include them as first-class checklist items even though they are not in the spec's literal §8.1 table. 07 §10 documents both explicitly, so this is covered.

---

## Self-Audit

**(a) Reliance list — claims I did NOT re-verify (relied on research assertion):**
- Relied on 05-v2's `string|null` nullability idiom claim and the full SKILL.md Output Contract field enumeration (lines 41-61) without re-reading all 61 lines — but I DID verify the load-bearing `diagnosability_verdict` enum and the heading anchors that the insertion logic depends on.
- Relied on 07's §5.6 per-field `Required` flags for H1/H3/H4 schemas without re-reading spec L456-506 line-by-line — but I verified the §5.4 truth table (the single highest-risk invariant) verbatim, which is the strongest signal of faithful extraction.

**(b) Independent semantic checks (≥1 required) — where research assertion was insufficient and my own tool work was required:**
- **File-existence ground truth** — verified by `ls` of `refs/` and `tests/troubleshoot/` + `ls -la` byte sizes of 4 modified files (not trusting 05-v2's [CODE-VERIFIED] tags).
- **Anchor-line accuracy** — verified by `grep -nE` of SKILL.md and report-template.md heading anchors against the exact line numbers the research cites (251/271/385/37 and 196/205/212/233 — all exact).
- **§5.4 verbatim fidelity** — verified by `sed -n '388,420p'` of the actual spec; all 7 rows + H5 mapping + downstream-no-override match 07 byte-for-byte.
- **FR-6 GAP truth** — verified by `grep` of the spec for `test_h2_sibling`/`FR-6`/`sibling_sweep`; confirmed no dedicated FR-6 test exists, so the proposed NEW test is genuinely net-new, not a duplicate.
- **OI open-vs-resolved status** — verified by `sed -n '600,610p'` of spec §11; confirmed OI-1/4/6 = "Resolved", OI-2/3/5 = deferred, validating 07's correction of the task-brief framing.

**Why trust this PASS:** I made 4 Read/Bash verification batches mapping to all 5 depth-lens items plus the 2 highest-risk builder pitfalls (advisory-enum drop, OI HALT-item misframing). Every independently re-tested claim held. A research set that survives this many ground-truth probes without a single contradiction is deep, not superficial.

---

## Confidence
Verified: 5/5 depth checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 2 | Grep (via Bash): 6 grep invocations | Glob: 0 | Bash: 4

(Tool-call count exceeds the 5 depth-checklist items; each Bash batch targeted specific claims — file existence, heading anchors, §5.4 verbatim, FR-6/OI status — no padding.)

## Web research
None performed. All verification was local (spec file + skill source + Makefile/config). Tavily not invoked; no fallback needed.

## QA Complete
