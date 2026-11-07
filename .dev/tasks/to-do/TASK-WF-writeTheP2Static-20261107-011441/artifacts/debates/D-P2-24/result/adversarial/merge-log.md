# Merge Log

## Metadata
- Base variant: Variant 1 (option-a-recommended), `adversarial/variant-1-original.md`
- Non-base variant: Variant 2 (option-b-alternative) and the debate findings
- Refactoring plan: `adversarial/refactor-plan.md` (4 planned changes)
- Merge date: 2026-11-07
- Output: `merged-decision.md`
- Executor: merge-executor

## Changes Applied

### Change 1: Correct the weakness claim
- **Status**: Applied
- **Source**: Debate transcript Round 1 (A-001 / X-002, both advocates REJECT); `analyze.md:3`
- **Target**: Base "Claimed weakness" paragraph (replaced)
- **Before**: "release-split Part 4 loses the richer `sc:analyze` verification when a coordinator would have liked it; reflect `--depth deep` loses its research enrichment."
- **After**: Part 4 loses an optional `sc:analyze` pass a coordinator might sometimes want; reflect `--depth deep` loses research enrichment. The "richer verification" claim is dropped, with the reason (`analyze.md` line 3 is code analysis; Part 4's checks come from `refs/verification-protocol.md` and Behavioral Instructions 1-3 whichever way Part 4 is delegated).
- **Provenance tag**: `<!-- Source: Base (original, modified) - Claimed weakness sentence replaced per Change 1 ... -->`
- **Validation**: Kept the true part of the weakness and removed the unsupported premise, as the plan's integration point requires. No other base sentence touched.

### Change 2: State the section 2.1 reading
- **Status**: Applied
- **Source**: Spec section 2.1; Variant B item 1; debate X-001 (A wins, 76%)
- **Target**: New section "Why this respects the spec"
- **Before**: (section did not exist)
- **After**: One paragraph: the rule fires on an invocation; inline verification invokes nothing; the skip-and-record clause applies to callees that do not accept the flag (`tech-research`), not to Part 4.
- **Provenance tag**: `<!-- Source: Variant 2 / debate, Change #2 ... -->`
- **Validation**: Wording matches the section 2.1 quotation in the debate transcript (X-001 row and Variant 1 advocate point 2). Placed after the base's judging block (see Note on placement).

### Change 3: Cost of the rejected option
- **Status**: Applied
- **Source**: Variant B item 1 and its claimed weakness; diff-analysis C-003; debate cost list
- **Target**: New section "Option B rejected because"
- **Before**: (section did not exist)
- **After**: Bullet list of five places B would touch: spec nested list; `EXPECTED_NESTING` (test line 1388, entry 1391); second hard-coded copy (test line 1461, entry 1466); `UNATTENDED_EXPECT["release-split"]["nested"]` (block line 472, nested near 482); `release-split.md:119` and `SKILL.md:330-331`. Plus the extra `analyze-report.md` artifact (analyze.md:98).
- **Provenance tag**: `<!-- Source: Variant 2 / debate, Change #3 ... -->`
- **Validation**: Line numbers were checked by Grep against `tests/skills/test_worker_contract.py` (read-only): 472, 1388, 1391, 1461, 1466 exist as stated. The plan gave 1388 and 1461 and the transcript gave 1391 and 1466; they are consistent (block start versus release-split entry) and both are cited accordingly. Line 482 is taken from the plan and was not re-read.

### Change 4: Part 4 has one path; record residual risk
- **Status**: Applied
- **Source**: Variant B item 1 (fallback), diff-analysis C-004; B advocate strength 1 (independence)
- **Target**: New section "Decision and residual risk"
- **Before**: (section did not exist)
- **After**: Decision = option A for both release-split Part 4 and reflect Wave 1B; edits needed in command or skill files = none (Part 4 inline at `SKILL.md:331` and `release-split.md:119`; reflect skips `tech-research` at `SKILL.md:640`); Part 4 has one path so no failure fallback is needed; independence recorded as unproven, unrefuted residual risk.
- **Provenance tag**: `<!-- Source: Variant 2 / debate, Change #4 ... -->`
- **Validation**: Facts match the plan and the debate transcript (A-002 row for reflect; orchestrator check on B strength 1). `SKILL.md:331` was confirmed by Grep for release-split; `SKILL.md:640` for reflect was taken from the transcript and not re-read.

### Note on placement
The base's "How to judge" block stays in its original position. The three new sections are appended after it, so "Decision and residual risk" is the final section. Change 2's integration point ("after the two numbered sites") is met in that the section follows them; it is not directly adjacent.

## Changes Failed or Skipped
None. The four rows in the plan's "Changes NOT Being Made" table (C-001, C-003, C-004, B weakness 1) were not applied, as the plan states.

## Post-Merge Validation

### Structural integrity (heading hierarchy)
- Headings: one H1; four H2 ("How to judge", "Why this respects the spec", "Option B rejected because", "Decision and residual risk"). No level gaps. **PASS**
- Section order: title and sites, strengths, weakness, judging block, then the three appended sections. **PASS**

### Internal references
- The merged text has no references to its own sections or numbered items that could dangle. The numbered sites 1 and 2 are unchanged. External references (spec section 2.1, D-P2-1, `refs/verification-protocol.md`, file:line anchors) were checked as noted under Changes 3 and 4; the unchecked ones (`SKILL.md:640`, test line 482, `analyze.md:3/98`) are taken from the plan and transcript. **PASS**

### Contradiction re-scan
- Base strengths (nested list stays as written; no new test pin) agree with the new sections. The replaced weakness no longer conflicts with the "How to judge" criteria or with "Option B rejected because". The spec reading in Change 2 agrees with the "How to judge" wording of section 2.1. No new contradiction with the base. **PASS**

### Summary
- Changes planned: 4; applied: 4; failed: 0; skipped: 0
- Validation: PASS (3 of 3 checks)
- Unverified items: test line 482, `SKILL.md:640`, `analyze.md:3` and `:98` (cited from the plan and transcript)
