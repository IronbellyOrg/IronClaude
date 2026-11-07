# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant 1 (option-a-recommended.md)
- Incorporating strengths from: Variant 2 (option-b-alternative.md) and the debate findings
- Planned changes: 4
- Risk level: Low (all additive text in a decision note; no source file is touched)

## Planned Changes

### Change 1: Correct the weakness claim (from the debate, A-001 / X-002)
- **Source**: Debate transcript, Round 1, both advocates REJECT A-001; analyze.md:3
- **Target**: Base, "Claimed weakness" paragraph (replace)
- **Rationale**: Both advocates reject the premise that `sc:analyze` verifies more strongly (90% confidence). `analyze.md` describes code analysis; Part 4's checks come from `refs/verification-protocol.md` and Behavioral Instructions 1-3 run whichever way Part 4 is delegated.
- **Integration point**: Keep the true part (a coordinator loses an optional `sc:analyze` pass; reflect `--depth deep` loses research enrichment) and drop "richer verification".
- **Risk**: Low, wording only.

### Change 2: State the section 2.1 reading (from the debate, X-001)
- **Source**: Spec section 2.1, nested propagation rule; Variant B item 1
- **Target**: Base, new section "Why this respects the spec" (append)
- **Rationale**: X-001 won by A at 76%. The rule reads "a command that invokes another ... passes `--unattended` when the invoked command accepts it"; the skill's own alternative (inline verification) invokes nothing. The skip-and-record clause applies to callees that do not accept the flag (tech-research), not to Part 4.
- **Integration point**: Short paragraph after the two numbered sites.
- **Risk**: Low.

### Change 3: Cost of the rejected option (from Variant B, U-003 / C-003)
- **Source**: Variant B item 1 and its claimed weakness; diff-analysis C-003
- **Target**: Base, new section "Option B rejected because" (append)
- **Rationale**: B's own text names the spec row, `EXPECTED_NESTING` and the tests; the debate adds the two hard-coded copies (test lines 1388 and 1461), `UNATTENDED_EXPECT["release-split"]["nested"]` (line 482), release-split.md:119 and SKILL.md:330-331. At least five places for a call no section 3 row names.
- **Integration point**: Bullet list with the file and line for each.
- **Risk**: Low.

### Change 4: Part 4 has one path; record residual risk (from Variant B, U-004 / C-004, and B's surviving argument)
- **Source**: Variant B item 1 (fallback); B advocate strength 1 (independence)
- **Target**: Base, new section "Decision and residual risk" (append)
- **Rationale**: With inline-only Part 4 there is no failure branch to specify. B's independence argument (Part 3 and Part 4 both inline in one context) is unproven but not refuted; recorded so the owner can revisit it later.
- **Integration point**: Final lines, including the edits-needed statement (none) and the reflect site (skip and record, same as B).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|----------------------------|
| C-001 | Nested `sc:analyze --unattended --report-dir <report-dir>/nested/analyze-<n>/` for Part 4 | Inline is already written and pinned; benefit unproven (analyze.md:3) |
| C-003 | Change release-split nested list to brainstorm, adversarial, analyze | At least five edits including two hard-coded test copies |
| C-004 | Inline fallback after a failed nested call | Only needed if the nested call exists |
| B weakness 1 | Add an unattended caveat to SKILL.md:107 and the command's standalone summary | SA-1/SA-4: standalone text stays as is; the override already sits at SKILL.md:331 and release-split.md:119 |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | A wrong sentence in a decision note | Restore the original paragraph |
| 2 | Low | Same | Remove the added section |
| 3 | Low | Same | Remove the added section |
| 4 | Low | Same | Remove the added section |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-07 (local)
