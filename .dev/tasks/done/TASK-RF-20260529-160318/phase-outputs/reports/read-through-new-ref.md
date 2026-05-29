# Step 6.2 — Structural-Twin Read-Through of refs/diagnosability-audit.md

Reviewer: orchestrator (post-Phase-5 read-through, human-loop equivalent that PG.A's structural QA may miss for stylistic drift)
Date: 2026-05-29 17:52
Target (new): `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md` (340 lines)
Twin (baseline): `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md` (182 lines)

## Question-by-question assessment

### (a) Top-of-file framing match (H1 + one-line wave anchor + one-paragraph orientation + `---`)

**Match.** New ref L1-7 mirrors twin L1-7:

```
# Diagnosability Audit Rules                                  (vs # Documentation Grounding Rules)

Wave 1.6 of the sc:troubleshoot protocol. Loaded on demand    (vs Wave 1.5 of the sc:troubleshoot protocol. Loaded on demand
by Wave 1.6 only.                                                  by Wave 1.5 only.)

This ref defines the two parallel audit branches             (vs This ref defines the three parallel discovery branches
(A: log-call inspection ..., B: log-config inspection ...)        (A: release-doc, B: architectural-doc ..., C: semantic-restriction))
the per-branch structured-output schemas, and the                 the per-branch structured-output schemas, and the
synthesised Diagnosability Context Card                           synthesised Documentation Context Card
that Wave 1.7 (hypothesis formation) and Wave 5                   that Waves 1, 3, 4, and 5 consume.
(synthesis + report) consume.

---                                                           (---)
```

Top-of-file framing identical in structure. ✓

### (b) Section-heading convention match (`## Section <N>: <imperative>` numbered; terminal `## Loading discipline` un-numbered)

**Match.** Verified via grep at PG.A inventory:

- Numbered sections in new ref: `## Section 1:` (L9), `## Section 2:` (L47), `## Section 3:` (L78), `## Section 4:` (L120), `## Section 5:` (L163), `## Section 6:` (L192), `## Section 7:` (L238), `## Section 8:` (L288).
- Twin numbered sections: `## Section 1:` (L9), `## Section 2:` (L39), `## Section 3:` (L72), `## Section 4:` (L131).
- Both end with `## Loading discipline` un-numbered (new ref L338; twin L180). ✓

### (c) Fenced code block style match (no language tag for shell + Auggie queries; `json` tag for JSON; `markdown` tag for templates)

**Match.** Verified via PG.A inventory line-citation scan:

- New ref untagged fences (Auggie query bodies + shell fallback bodies) at L17, L27, L33, L43, L53, L61, L67, L72 — matches twin's L17, L25, L33, L45, L53 (Auggie queries + bash currency-check commands, all untagged).
- New ref `json` tags at L84 (Branch A schema), L101 (Branch B schema) — matches twin's L80, L91, L99, L116 (`json` for all branch schemas).
- New ref `markdown` tag at L196 (Diagnosability Context Card template) and L260 (worked tasklist skeleton) — matches twin's L133 (`markdown` tag for Documentation Context Card template).

Pattern conformance verified. ✓

### (d) Placeholders consistently angle-bracketed snake_case (`<failing_component>`, `<scope>`, `<symptom>`)

**Match.** New ref's lead-in paragraph at L11 names all three placeholders: `<failing_component>`, `<scope>`, `<symptom>`. Each appears verbatim in Section 1's branch queries (L17, L27 for Branch A; L33 for Branch B). Twin uses the same convention at L11 (`<issue_description>`, `<scope>`, `<component_paths>`).

Snake_case + angle-bracket pattern preserved. ✓

### (e) Terminal `## Loading discipline` ≤3 paragraphs + enumerates on-entry read set

**Match.** New ref L338-340:

```
## Loading discipline

This ref is loaded by Wave 1.6 only. Other waves do not import it. Wave 1.6 reads Section 1 (query templates), Section 2 (fallback paths), Section 3 (schemas), Section 4 (sufficiency rubric + 3-W's synthesis), Section 5 (complexity gate), Section 6 (Diagnosability Context Card template), Section 7 (tasklist generation rules + hard constraints), and Section 8 (T4 worked example) on entry; the file is not re-read during the wave.
```

Single paragraph (≤3 ✓). Explicitly enumerates Sections 1-8 as the on-entry read set ✓. Closes with "the file is not re-read during the wave" — matching twin's "they do NOT load this entire ref. The synthesised Documentation Context Card from Section 4 is the only artifact consumed by downstream waves" discipline at L182.

### (f) All 13 sufficiency-rubric rows S1-S13 verbatim from merged-output.md §3:171-185

**Match.** Verified independently in PG.A.2 rf-qa pass: all 13 rows present in Section 4 at L138-150 with verbatim signal-combination text and verdict (variant-N provenance phrases correctly stripped per the no-`<!-- Source: -->` discipline; substantive text preserved). ✓

### (g) All 7 complexity-gate signal rows from merged-output.md §4:215-225 + `--type security` override

**Match.** Verified independently in PG.A.2: all 7 rows in Section 5 at L171-177 with verbatim signals and weights; the security override row carries `**Always non-trivial (override)**` as in source. ✓

### (h) All 4 tasklist HARD CONSTRAINTS from merged-output.md §6:265-273

**Match.** Verified independently in PG.A.2: all 4 constraints verbatim in Section 7 at L244-247 (Invocation-site-only / Additive only / Reversible / Revert annotation with the literal annotation string). ✓

### (i) T4 worked example in Section 8 illustrates insufficient+non-trivial hard-stop path

**Match.** Verified independently in PG.A.2: Section 8 at L288-336 covers the worker-hang case with all required elements (failing_component=src/worker/processor.py; logger.info("task_started") at worker.py:42; bare except at worker.py:198; captured_bytes=4096; LOG_LEVEL=INFO; S13 fires; verdict=insufficient, complexity=non-trivial score 3, hard-stop fires; 5-task skeleton: DEBUG env, fixture wrapper, strace, Sentry breadcrumb, CI artifact upload; "What was saved" paragraph contrasts blind-Tier-2 vs instrumentation-first re-run). ✓

## Structural-twin deviation surfaced

**None.** New ref conforms to the doc-discovery.md structural twin across all 9 questions.

## Stylistic notes (informational, not blocker)

1. **Section count**: new ref has 8 numbered sections; twin has 4. Justified — the brainstorm spec §9 explicitly specified an 8-section structure for the new ref (sufficiency rubric, complexity gate, context card, tasklist rules, T4 example are all spec-required content that doc-discovery does not have analogs for).
2. **In-fence headings**: the markdown template at L196-233 (Diagnosability Context Card) and L260-282 (worked tasklist skeleton) contain in-fence `# Diagnosability Context Card` / `# Diagnosability Tasklist` H1 markers. These are intentional (templates render to runtime artifacts with their own H1) and were correctly flagged in PG.A inventory as "expected in-fence headings". Same pattern used by twin at L131-177 for the Documentation Context Card template.

## Verdict

**Phase 6 Step 6.2 — structural-twin conformance: PASS.** No drift surfaced beyond what PG.A already validated. The human-loop read-through corroborates the structural QA result.
