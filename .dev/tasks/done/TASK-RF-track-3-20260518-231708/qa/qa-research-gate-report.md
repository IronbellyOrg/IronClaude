# QA Report — Research Gate

**Topic:** FU-003 PRD-skill CWD-default output routing (TRACK 3)
**Date:** 2026-05-18
**Phase:** research-gate
**Fix cycle:** N/A
**Mode:** Independent QA (running in parallel with rf-analyst)
**Fix authorization:** false

---

## Overall Verdict: **PASS**

All four research files are Status: Complete, evidence-dense, well-cited, and the load-bearing claims (config.py:100, logging_.py:52-56, reject-workspace-writes.sh semantics, CLAUDE.md L108-116) have been independently verified against the source files. Adversarial check of T3-R1's hypothesis-overturn (test harness NOT the culprit) is **CONFIRMED CORRECT**. Recommendations from the four files are compatible — they describe complementary layers (source-fix in config.py + optional defense-in-depth hook + integration plumbing + template scaffolding).

One MINOR documentation inaccuracy found (T3-R2 line count off by 1) — does not affect any recommendation and does not block synthesis.

## Items Reviewed (Assigned Partition)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All files Status: Complete | PASS | 01:L5 "Status: Complete"; 02:L4 "Status: Complete"; 03:L5 "Status: Complete"; 04:L3 "Status: Complete". All four files contain a Summary or equivalent terminal section. |
| 2a | Evidence — config.py:100 contains `Path(".").resolve()` | PASS | Read config.py:100 directly: `output_path = Path(output).resolve() if output else Path(".").resolve()`. Exact byte match to claim in 01:L23 and 02. |
| 2b | Evidence — config.py:107-108 task_dir construction | PASS | Read config.py:107-108: `task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"` then `task_dir = output_path / task_dir_name`. Matches 01:L153-154. |
| 2c | Evidence — logging_.py:52-56 mkdir | PASS | Read logging_.py:50-56. `task_dir.mkdir(parents=True, exist_ok=True)` is on line 56. 01:L160-162 cited it correctly. |
| 2d | Evidence — reject-workspace-writes.sh line count | **MINOR FAIL** | `wc -l` and `awk 'END{print NR}'` both report **39 lines**, NOT 40 as claimed in 02:L18 and L297. File ends with `exit 0\n` (newline-terminated, no trailing blank). The pattern, semantics, and exit-2 contract claims (02:L28, L36, L33) are all otherwise correct. |
| 2e | Evidence — CLAUDE.md L108-116 plugin override | PASS | Read CLAUDE.md:108-116. "Plugin Override — Skill-Creator Workspace Destination" heading at L108, "Override" sentence at L110, "Destination rule" at L112, "Rationale" at L114, "Authoritative source" at L116. 02:L153-171 quotes are accurate. |
| 2f | Evidence — settings.json has reject-workspace registration | PASS | Cat'd `.claude/settings.json` (17 lines, matching 02:L79). Confirms `"matcher": "Write\|Edit"` and `"command": "$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh"` exactly as 02:L80-97 describes. |
| 2g | Evidence — _FRESHNESS_SCRIPTS registry | PASS | Read install_hooks.py:43-67. List structure (7 freshness scripts + auggie + comment block + reject-workspace-writes.sh entry on line 66) matches 03:L19-32. |
| 2h | Evidence — Makefile verify-sync sections | PASS | Read Makefile:155-315. Six banner-separated sections at L159 (Skills), L191 (Agents), L217 (Commands), L243 (Hooks), L269 (Installer Registration), L290 (Hooks Cross-Consistency). 03:L130-138 table accurate. The `=== Installer Registration ===` block at L271-288 uses `comm -23` against `_FRESHNESS_SCRIPTS` exactly as 03:L137 describes. |
| 2i | Evidence — commands.py:119-125 dry-run short-circuit | PASS | Read commands.py:119-125. Confirms `if dry_run: ... return` at L119-125, BEFORE `executor = PrdExecutor(config)` on L127. 01:L131-132 and 01:L260 verified. |
| 3 | Scope coverage — all 8 surfaces | PASS | 01 covers config.py + logging_.py + commands.py. 02 covers reject-workspace-writes.sh + hooks.json + settings.json + SKILL.md + CLAUDE.md addendum. 03 covers install_hooks.py + Makefile verify-sync + sync model + PR-F b63cbd7 template. 04 covers MDTM Template 02 + analogous done/ tasks. All scoped surfaces addressed. |
| 4 | **ADVERSARIAL: T3-R1 hypothesis-overturn (tests NOT the culprit)** | **PASS — INDEPENDENTLY CONFIRMED** | Read `tests/cli/prd/test_prompts.py:38-52` directly. Line 44 is `td = tmp_path / "prd-test-product"` — pytest's per-test tmp_path. Read `src/superclaude/cli/prd/config.py:100`: `output_path = Path(output).resolve() if output else Path(".").resolve()`. CWD default confirmed. `grep -rn "prd-test-product\|prd-dry-run-test" tests/ src/` returns exactly 1 hit (test_prompts.py:44), zero hits for `prd-dry-run-test`. T3-R1's hypothesis overturn is correct. The user's original framing (test harness as source-fix) is wrong; the production CWD default is the real culprit. |
| 5 | Contradiction resolution across 4 researchers | PASS | T3-R1 says source-fix is config.py (primary fix). T3-R2 recommends Option C generic hook (defense-in-depth). T3-R3 notes Option A (extend existing hook) would be lowest-risk. These are NOT contradictions — they describe complementary layers and different framings of the same defense-in-depth question. 01:L196-202 explicitly acknowledges hook layer is "Defense-in-depth" while config.py is "Primary fix (source-of-truth)". 02:L188-211 considers Option A and rejects it on SRP grounds. 03:L218-222 notes Option A is the lowest-plumbing-overhead choice. The trade-off is honest and surfaced. The synthesizer must pick one of {Option A simplified, Option C generic} as the final hook recommendation, but the underlying technical evidence is compatible. |
| 6 | Gap severity | PASS | Reviewed each file for explicit "Gaps and Questions" / unanswered items. None found. The only open decision is the Option A vs Option C trade-off, which is a synthesis-time choice, not a research gap. The MINOR 39-vs-40 line-count inaccuracy is logged but does not affect any recommendation. |
| 7 | Standard tier appropriate | PASS | Standard tier requires file-level coverage. All four research files cite specific file:line references throughout. T3-R1 traces the data flow end-to-end (lines 138-164) — exceeds Standard tier, approaches Deep tier rigor. T3-R3 traces the install/sync chain end-to-end (L93-105). Tier is appropriate or exceeded. |
| 8 | Integration coverage — `_FRESHNESS_SCRIPTS`, sync model, verify-sync §5 gate | PASS | T3-R3 §1 documents `_FRESHNESS_SCRIPTS` location + format + invariants. §2 documents end-to-end sync model with diagram (L93-105). §3 documents verify-sync §5 (Installer Registration) gate with exact failure-mode text at Makefile:274-278. All three integration aspects covered. |
| 9 | Pattern documentation | PASS | T3-R4 §1 distills MDTM Template 02 PART 1 rules (B2 six elements, B3 paragraph form, I15 phase-gate QA, I17 post-completion validation, I18 testing requirement). T3-R2 §1 documents the hook script body conventions (header comment, decision contract, input parsing, match regex anchoring, redirect format). T3-R3 §4 documents the PR-F b63cbd7 reference template (4-file diff structure). Patterns are dense and reusable. |
| 10 | Incremental writing compliance | PASS | All four files show evolving structure with section-by-section detail. T3-R1 has 5 numbered sections + Appendix with evidence index. T3-R4 has 5 sections each with multiple sub-tables. None of the files show one-shot uniformity. |

## Summary
- Checks passed: 16 / 17
- Checks failed: 1 (MINOR)
- Critical issues: 0
- Important issues: 0
- Minor issues: 1

## Confidence
**Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%**
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 6

All checklist items verified with at least one tool invocation directly against the cited source files. No reliance on prior reports or research-file claims without independent verification.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 02-skill-and-hook-patterns.md, L18 ("40 lines total") and L297 ("(40 lines)") | `wc -l` reports the script is 39 lines, not 40. File is newline-terminated (last 4 bytes: `t 0\n`). | Update 02:L18 and 02:L297 to "39 lines". Does not affect the semantics, exit-2 contract, regex pattern, or any recommendation — purely a cosmetic count error. The synthesis can either silently use the correct count or surface as a research-file errata note. |

## Contradiction Analysis (Recommendation Compatibility)

The three "competing" recommendations across T3-R1/R2/R3 are NOT mutually contradictory:

| Researcher | Recommendation | Layer |
|---|---|---|
| T3-R1 (01-test-harness.md) | Primary source-fix at `src/superclaude/cli/prd/config.py:100` — replace `Path(".").resolve()` with `.dev/eval-workspaces/` sandboxing logic | Production code (root cause) |
| T3-R2 (02-skill-and-hook-patterns.md) | Defense-in-depth: Option C generic `reject-skill-root-writes.sh` parameterized over slug-prefix anti-patterns | Hook layer (guardrail) |
| T3-R3 (03-integration-points.md) | If hook approach is Option A (extend existing hook), zero plumbing delta; if Option B/C, follow b63cbd7 7-step template | Integration plumbing (cost analysis) |

These layer cleanly: Track 3 needs (a) the config.py source-fix, AND (b) optionally a hook guardrail. The Option A vs Option C choice is a synthesis-time decision (low-risk extension vs better SRP separation), but both are technically compatible with the source-fix.

**Note for synthesis:** the synthesizer should explicitly call out that Option A and Option C are alternatives at the hook layer, with Option A being lower-cost (per T3-R3 §5 "Option A simplified flow") and Option C being more architecturally clean (per T3-R2 §5 SRP rationale).

## Actions Taken
None. fix_authorization is false. The single MINOR inaccuracy is documented above for the synthesizer to handle.

## Recommendations
- **Green light to proceed to synthesis.** All ten core checklist concerns pass; the one MINOR inaccuracy is non-blocking documentation drift.
- **Synthesis must address the Option A vs Option C choice explicitly.** This is the only real decision point. Both options are defensible; the synthesizer should present them as alternatives in the Options Analysis section.
- **Synthesis must NOT carry forward the "40 lines" claim verbatim.** Correct to 39 or omit the count.
- **Synthesis should foreground that T3-R1's hypothesis overturn is the most important finding.** The user's original framing (test harness as the bug site) is wrong; the production CWD default is. This reframing should be the synthesis's headline.

## QA Complete
