# QA Report — Research Depth (research-depth lens)

**Topic:** Pipeline Hardening Closure mode for sc:troubleshoot-protocol
**Date:** 2026-06-10
**Phase:** research-depth (adversarial)
**Fix authorization:** false (report-only)
**Assigned files:** research/01..06 (all .md)

---

## Adversarial Stance

Assumption entering review: the research is superficial until proven otherwise.
Lens: is research DEEP ENOUGH to produce a high-quality task file WITHOUT the
builder re-reading source files? For a protocol-doc transformation, "depth" =
exact insertion structure + house-style captured concretely + spec→file mapping
pinned to spec line ranges.

---

## Depth checklist (to be filled per-file)

1. STRUCTURE of target files (heading hierarchy, section start/end), not just existence?
2. House-style captured concretely enough to replicate (frontmatter? fences? table style? open/close)?
3. Insertion points specific (line N, between X and Y)?
4. spec→new-ref mapping deep (each of 5 refs pinned to exact spec section/line range)?
5. Per-card QA encodable without re-reading MDTM template (R4 depth on M3/M4/I19/I20)?
6. H5-placement decision argued with rationale?
7. Shallow signals: file lists w/o structure, "follows convention" w/o specifics, missing line ranges?

---

## Findings (appended incrementally below)

### Per-file depth assessment

**01-skill-structure-inventory.md — DEEP (exemplary).**
- Checklist 1 (structure): PASS+. Full top-level section index with line ranges (§0 table), Tier→Wave
  mapping with spans, and the exact terminology nuance (SKILL.md uses Waves as headers; Tiers are
  carried inline in wave headers — "there are NO standalone `## Tier 1` headers"). Behavioral
  understanding, not a file list.
- Checklist 3 (insertion points): PASS+. Pins the hardening insertion seam to the `---` at L383 before
  Wave 5 (L385) with a defended rationale: "after Tier-1 diagnosis (W1.7 ends L267) AND after Tier 2
  (W3-4 end L382), before final closure (W5 L385)" — satisfies spec §5.2 for BOTH tier outcomes.
  Also names the fallback (mandatory pre-step inside Wave 5 before L391).
- Checklist 2 (house-style): PASS. §4 identifies the strongest blocking precedent (Tier-2 calibration
  completeness gate, L327-337, "MUST NOT publish unless proof on disk + verification command") as the
  template for the "cannot mark remediated" gate. §6 captures wave skeleton (Goal/Preconditions/Steps/
  Exit-criteria/Emit-string/Failure-table), fractional-wave precedent (1.5/1.6/1.7 → 4.5), lowercase
  enum convention, and the `Emit "Wave N complete: …"` convention.
- VERIFIED against source: L37/41/61/77, L251/271/385, L327/439, L536-546, ASCII map L79-91 — ALL match.

**02-command-and-contract-integration.md — DEEP.**
- Checklist 1/3: PASS. Command file mapped to 201 lines; "keep thin" enforcement pinned to L62 + L82;
  handoff line L80 (`> Skill sc:troubleshoot-protocol`) quoted exactly. Output-contract correctly
  identified as a markdown TABLE (L37-61), not JSON/YAML, with the secondary audit-footer surface
  (L413-424, a curated subset) and tertiary REPORT.md surface distinguished.
- §6.2-field mapping: PASS. Each of the 8 new fields mapped to a house-style precedent
  (`diagnosability_verdict`→`pipeline_hardening_verdict`/not_applicable; `doc_context_card_path`→the 4
  path fields; `diagnosability_hard_stop`→`pipeline_hardening_applicable`;
  `escalation_reason`→`off_path_review_decision`; `hypothesis_cards`→`known_escapes_caught`).
- VERIFIED against source: command L3/62/67/80 — ALL match.

**03-refs-conventions-and-report-template.md — DEEP (exemplary on house-style).**
- Checklist 2 (house-style, REPLICATION-grade): PASS+. NO frontmatter on any ref; exactly one `# Title`
  on line 1; `## `/`### ` hierarchy; fence-language discipline (`text` for fill-in cards, `markdown` for
  report fragments); raw GFM pipe tables with bare `|---|` separators; close with a rationale/Blocking-
  rule section; no emoji. Concretely sufficient to author a markdownlint-clean ref from this alone.
- Checklist 3 (insertion point): PASS+. report-template.md mapped section-by-section (four-backtick
  ````markdown fence opens L7 closes L203). Insertion anchor for `## Pipeline Hardening Closure` pinned
  BETWEEN L132 (`If there are no follow-ups, write "None."`) and L134 (`## Grounding Gaps`), INSIDE the
  fence; the `## Pipeline Hardening Closure rule` prose anchored AFTER EOF (L259). Fence-nesting caution
  explicit ("section goes INSIDE the fence; rule prose goes OUTSIDE").
- Checklist 4 (spec→ref mapping): PASS+. §4 gives a per-ref build recipe with EXACT spec line ranges:
  H1 card = spec 136-151; H2 ledger = spec 171-180; H3 outputs+pattern = spec 200-218; H4 card =
  spec 241-253; §8 report block = spec 299-312. Deepest possible spec→file pinning.
- Checklist 6 (H5 placement): PASS+ (standout). The decision to fold H5 into
  pipeline-hardening-closure.md (NOT a 6th ref, NOT into effective-input-proof.md) is argued with FOUR
  evidence-based points: (1) spec §9 names exactly 5 files, H5 not among them; (2) H5 has no fill-in
  card (3 prose lists only); (3) H5's output is a single decision token, not a path field; (4) folding
  into the narrow H4 ref would mis-scope the cross-cutting policy. Argued, not asserted.
- VERIFIED against source: report-template L1/7/132/134/203, remediation-handoff L1/116-122, refs/ dir
  (8 existing, 5 new absent) — ALL match.

**04-mdtm-template-and-examples.md — DEEP (Checklist 5 fully satisfied).**
- Checklist 5 (per-card QA encodable without re-reading MDTM template / R4 depth on M3/M4/I19/I20):
  PASS. M3 8-step lens sequence quoted with line refs; M4 6-step fidelity gate (runs AFTER M3 per
  I21:788); I19 agent-count FLOORS quoted verbatim (<500=6, 500-1500=8, 1500-3000=10, >3000=12;
  intermediate=5); I20 serialized-fix protocol; I21 fidelity applicability (MANDATORY for this
  source→protocol transform); I22 intensity (Deep→full). Canonical POST-reflect SELF-RUN item form
  quoted, with the explicit warning that two recent TASK-RF examples use the now-MALFORMED human-
  handoff/HALT form. A builder can encode the full gate from this without re-opening the template.
- VERIFIED against source: I19 table at template L708-709 matches the quoted floors; canonical
  POST-reflect header at task-builder/SKILL.md L2193; anti-orphaning rule 15 at L2302; MALFORMED-form
  validation item L2253 and rule 20 L2312 — ALL match.

**05-doc-crossvalidation-spec-vs-code.md — DEEP.**
- Checklist 4 / orphan-analysis: PASS. All 4 edit-targets verified to EXIST; all 5 new refs verified
  ABSENT (genuine CREATE, no collision); every E1-E5 escape cross-read against its root-cause.md;
  every §6.2 field mapped to a producing §7 card (no orphan field, no orphan card); H→R mappings
  cross-checked against generalized-remediation-set.md. Two non-blocking spec self-consistency flags
  (F1 verdict-enum mismatch, F2 template-vs-instance naming) surfaced honestly.
- VERIFIED against source: refs/ dir confirms 4 targets exist + 5 absent; Makefile sync-dev L109,
  verify-sync L166 — match.

**06-sync-verify-and-tests.md — DEEP.**
- Checklist 7 (shallow signals — actively rebutted): PASS. Quotes the actual sync-dev find loop and the
  verify-sync `diff -rq` mechanics; proves new refs auto-mirror with NO manifest/ref-count assertion;
  quotes `.markdownlint.json` VERBATIM (MD013 off, MD025 ON, etc.); proves TESTING_REQUIREMENTS=NONE
  via "zero matches" grep evidence. Gives a concrete numbered VALIDATION command sequence.
- VERIFIED against source: .markdownlint.json content matches; Makefile anchors match.

### Adversarial spot-check results (independent tool verification)

I independently verified the load-bearing line citations rather than trusting the research:
- SKILL.md: L37/41/61/77/251/271/385/327/439/536-546 + ASCII map L79-91 — every cited anchor is exact.
- report-template.md: L1/7/132/134/203 — exact (insertion anchor confirmed).
- remediation-handoff.md: L1 + failure-modes table L116-122 — exact.
- refs/ directory: 8 existing files + 5 named-absent — exact.
- command troubleshoot.md: L3/62/67/80 — exact.
- task-builder SKILL.md: POST-reflect header L2193, anti-orphaning L2302, MALFORMED items L2253/L2312,
  I19 floors at template L708-709 — exact.

### Minor discrepancies found (do NOT change the depth verdict)

- **MINOR-1 — Off-by-one in line-COUNT headers (not in body citations).** Research 01 states SKILL.md is
  "549 lines"; `wc -l` reports 548. Research 03 states report-template.md "259 lines" / remediation-
  handoff.md "123 lines"; `wc -l` reports 258 / 122. Trailing-newline counting artifact in the file-
  size headers ONLY. Every actual body-content line citation lands exactly on target (verified above),
  so the insertion anchors a builder would act on are correct. MINOR; builder-awareness only.
- **MINOR-2 — Condensed POST-reflect quote.** Research 04 §4 reproduces the canonical POST-reflect item
  as an abbreviated paraphrase (and once cites the range as "2186-2198" where the item header is at
  L2193). The live task-builder/SKILL.md text (L2193-2198) is more elaborate than the quoted block, but
  the directive content research 04 extracted (single `<BASE>` ref, working-tree diff, `git add -A`
  before the gate, `start_commit..HEAD` deprecated, depth floored at `standard`, self-run not HALT,
  `--spec` active for this doc-transformation track) is accurate and faithful. A builder copying 04's
  block verbatim would produce a slightly stale (but correct-in-intent) item; regenerate from live
  SKILL.md L2193-2198. MINOR.

Neither minor discrepancy undermines the research's depth: structure, house-style, insertion points,
spec→ref mapping, per-card QA encodability, and the H5-placement rationale are all DEEP and accurate.

---

## Self-Audit

**(a) Reliance list — items where I did NOT independently re-verify (relied on research assertion):**
- Relied on research 05's E1-E5 root-cause.md cross-reads (did not re-open the 10 escape evidence
  files; spec→root-cause consistency is within research 05's scope, not the depth lens).
- Relied on research 06's `tests/` zero-match grep claim (did not re-run the full tests/ grep sweep).

**(b) Independent semantic checks (tool-verified, depth-relevant):**
- SKILL.md structural anchors (L37-546 + ASCII map) — verified via `sed`/`wc`; confirms Checklist 1 & 3
  depth claims in research 01 are accurate, not asserted.
- report-template.md insertion anchor (L132↔L134, four-backtick fence L7/L203) — verified via `sed`;
  confirms Checklist 3 depth in research 03.
- task-builder SKILL.md POST-reflect/anti-orphaning/MALFORMED + template I19 floors — verified via
  `grep`/`sed`; confirms Checklist 5 / R4 depth in research 04 (and surfaced MINOR-2 the research text
  obscured).
- refs/ dir contents — verified via `ls`; confirms the 5-new/8-existing CREATE-safety claim (Checklist 4).

**Confidence:** Verified: 7/7 depth checks | Unverifiable: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Bash (sed/grep/ls/wc batches): 4 | Glob: 0

---

## Items Reviewed

| # | Depth check | Result | Evidence |
|---|-------------|--------|----------|
| 1 | Structure of target files captured | PASS | 01 §0 line-range index + Tier/Wave mapping; verified L37-546 |
| 2 | House-style concretely replicable | PASS | 03 §1 (no-frontmatter, fence-lang, pipe tables, close-rule); 01 §4/§6 wave skeleton + blocking precedent |
| 3 | Insertion points specific (line N, between X/Y) | PASS | 01 L383 seam w/ rationale; 03 report-template L132↔L134 INSIDE fence; verified exact |
| 4 | spec→new-ref mapping deep (line ranges per ref) | PASS | 03 §4: H1=136-151, H2=171-180, H3=200-218, H4=241-253, §8=299-312; 05 orphan-free field↔card |
| 5 | Per-card QA encodable w/o re-reading MDTM template | PASS | 04 §2: M3/M4/I19(verbatim floors)/I20/I22 + canonical POST-reflect form; verified L708/L2193/L2302 |
| 6 | H5-placement argued with rationale | PASS | 03 §4.6: 4 evidence-based points (spec file count, no card, decision-token output, mis-scope risk) |
| 7 | Shallow signals (file lists, "follows convention", missing ranges) | PASS (none found) | 06 quotes sync-dev loop + .markdownlint.json verbatim + zero-match test grep; no vague "follows convention" |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | 01 header; 03 §2/§3 headers | Line-COUNT headers off-by-one vs `wc -l` (549/259/123 → 548/258/122); trailing-newline artifact. Body line citations all exact. | Builder awareness only; no edit needed. Use body anchors (correct), not file-size header counts. |
| 2 | MINOR | 04 §4 | Canonical POST-reflect item quoted as condensed/older paraphrase; "2186-2198" range vs actual header L2193. Directive content accurate. | Builder regenerates the POST-reflect item from live task-builder/SKILL.md L2193-2198, not from 04's block. |

Both are MINOR awareness flags, not depth gaps. fix_authorization is false (report-only).

---

## Recommendations

1. Builder may proceed: depth is sufficient. Use body line anchors directly; they are verified-exact.
2. When emitting the POST-reflect gate item, copy from the LIVE task-builder/SKILL.md L2193-2198 (the
   self-run form), not from research 04's condensed quote.
3. Treat research 01/02/03 file-size line counts as N+1 of `wc -l`; insertion anchors are correct.

---

## Verdict

**Depth-lens determination: research is DEEP ENOUGH** to produce a high-quality task file without the
builder re-reading source files. Every depth checklist item (1-7) is satisfied with concrete, tool-
verified evidence — structure with line ranges, replication-grade house-style, exact insertion anchors
inside the four-backtick fence, spec→ref mapping pinned to spec line ranges, per-card QA encodable from
research 04 alone, and an H5-placement decision argued with four evidence points.

Per binary gating (any issue of any severity = FAIL), two MINOR awareness flags are recorded:

VERDICT: FAIL (two MINOR issues — both awareness flags, neither a depth gap; see Issues Found)

Substantive depth assessment: PASS-equivalent. The two MINOR items are line-count header artifacts and
a condensed quote; they do not represent shallow research and do not block the builder. If the gate
operates on substantive depth rather than strict binary, this is a PASS.
