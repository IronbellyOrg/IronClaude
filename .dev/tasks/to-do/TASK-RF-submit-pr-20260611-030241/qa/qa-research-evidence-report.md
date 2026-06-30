# QA Report — Research Gate (Evidence-Quality Lens)

**Topic:** Build MDTM task file to implement `sc:submit-pr` per merged spec
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** evidence-quality
**Fix cycle:** N/A
**Fix authorization:** false

---

## Scope

Assigned research files 01..07 in:
`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/research/`

Lens focus: verify every research claim cites real file paths / line numbers / function names that actually exist. Spot-check >=25% of cited paths; verify load-bearing claims R3/R4/R5/R6 by reading real source files.

---

## Verification Log

### Files in scope (all 7 read in full)
| File | Status header | Bytes | Read |
|------|---------------|-------|------|
| 01-component-inventory.md | Complete | 13231 | ✓ full |
| 02-skill-command-hook-conventions.md (R2) | "In Progress" (head) / "Complete" (foot) | 29726 | ✓ full |
| 03-reuse-surfaces.md (R3) | Complete | 17852 | ✓ full |
| 04-test-infra-and-deterministic-core.md (R4) | Complete | 17363 | ✓ full |
| 05-integration-points.md (R5) | "In Progress" (head) / "Complete" (foot) | 22860 | ✓ full |
| 06-detection-probe-and-gh-surface.md (R6) | Complete | 22304 | ✓ full |
| 07-mdtm-template-and-examples.md (R7) | Complete | 20791 | ✓ full |

### Load-bearing claim verification (6 designated + extras)

**R4 — `--cov` hyphen defect & correct package.** VERIFIED.
- Spec line 1025 literally contains `--cov=superclaude.skills.sc-submit-pr-protocol` (read merged-spec.md:1023-1027). Hyphens are illegal Python identifiers → unresolvable as a dotted module. ✓
- Hyphenated skill-dir precedent proven live: `src/superclaude/skills/confidence-check` exists (hyphen). ✓
- Underscored-package convention proven: `superclaude.cli.cli_portify`, `superclaude.cli.recommend`, `superclaude.cli.swarm` all import cleanly (tests/cli_portify/test_cli.py:18, tests/recommend/test_dispatch.py:17 verified verbatim). ✓
- `sc-bare-review` ↔ `superclaude.cli.swarm` split precedent: importlib `spec_from_file_location` at tests/swarm/test_bare_review_parity.py:234-240 verified verbatim. ✓
- Recommendation `src/superclaude/submit_pr/` is sound: spec test bodies (merged-spec.md:649, :882) call `run_skill(...)` and assert `result.round_counter`/`result.push_count` — in-process Python, not satisfiable by markdown/bash. ✓

**R4 — pyproject `--strict-markers` + markers registered + coverage source.** VERIFIED.
- `addopts = ["-v", "--strict-markers", "--tb=short"]` present (pyproject.toml:109-113). ✓
- `markers = [...]` block present; NONE of `loop_guard/autonomy/recovery/p0/loop` registered (must be added) — confirmed by reading the full marker list (pyproject.toml:114-140). ✓
- `[tool.coverage.run] source = ["src/superclaude"]` present (pyproject.toml:142-143), so new pkg auto-covered. ✓
- Ruff `import anthropic` ban (FR-G1) present at pyproject.toml:212-215. ✓ (R4 §G claim confirmed.)

**R3 — `--depth quick` + `--fix` is an explicit STOP.** VERIFIED EXACTLY.
- sc-troubleshoot-protocol/SKILL.md:131: "STOP conditions: ... conflicting flags (`--depth quick` with `--fix`) ...". Line number exact. ✓
- `--depth` values quick|standard|deep at :277-279. ✓

**R3 — severity-rubric schema (tiers + remap algorithm) at cited lines.** VERIFIED.
- "## The five tiers" header at severity-rubric.md:12; "## Severity-remap algorithm" at :63; 5-step pipeline (start-from-hint → category override → confidence adj → diff-locality → cross-source bonus) read at :63-101 — matches R3's description step-for-step. ✓
- Hallucination contract at sc-auggie-review-protocol/SKILL.md:22 verified verbatim. ✓

**R6 — `git remote -v` only origin=IronbellyOrg/IronClaude; no captured Augment JSON.** VERIFIED.
- `git remote -v` → only origin (fetch+push) = https://github.com/IronbellyOrg/IronClaude.git; NO upstream. ✓
- `find .dev -iname '*augment*'` → empty (zero captured Augment GitHub-App review JSON). ✓ DET probe genuinely cannot run now; HALT framing is correct.
- gh 2.45.0 confirmed (no native resolve verb claim is period-consistent). ✓

**R5 — command⇄skill pairing enforced by make lint-architecture; Skill-tool precedent.** VERIFIED.
- `lint-architecture:` at Makefile:362; pairing checks at :369-385; "Check 6: Activation Section Present" at :410-419. ✓
- `lint: lint-architecture` (Makefile:48) → `make lint` runs the architecture gate. ✓
- `sync-dev:` at Makefile:109 copies skills→.claude/skills, commands→.claude/commands/sc/. ✓
- install_skills.py standalone-protocol policy (docstring :12-21, `_has_corresponding_command` :29, strips only `sc-` at :42) verified — no install code change needed. ✓
- install_commands.py:37 `glob("*.md")` verified. ✓
- Skill-tool `> Skill <name>` precedent confirmed in cited files (troubleshoot/auggie-review). ✓

**Extra spot-checks (R1, R6):**
- offer-pr-review.sh: EXISTS, 74 lines, 3409 bytes, executable; INVOKE_HINT if/elif/else at :49-58; `<sc-auggie-review-offer>` heredoc at :60-72 with "Do not auto-invoke" line — all verified verbatim. ✓
- severity-rubric.md: EXISTS, `wc -l`=172 (R1 says 172, R3 says 173 — off-by-one, no trailing newline on final line; immaterial). MINOR.
- auggie SKILL.md:304-314 inline-comment gh-api surface (`-f body -f commit_id -f path -F line -f side=RIGHT`, `-F`-vs-`-f` distinction) verified verbatim. ✓

### Honesty / flagged-item audit
- R2 and R5 both carry a stale `**Status: In Progress**` line at the TOP while their FOOTER says `**Status: Complete**`. Content is complete; this is a cosmetic header-staleness, not an incompleteness. MINOR.
- R3's `evidence-validator` citation says "troubleshoot SKILL.md:409"; the evidence-validator spawn paragraph (`report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec=false`) actually sits a few lines below 409 (the "File:line validation pass (non-negotiable)" numbered step). Substance fully present and accurate; line anchor drifts ~3 lines. MINOR.
- All genuinely-unknown items are honestly flagged: DET probe (R6) marked PENDING/HALT with `needs_human_decision`; R2 §7.2 hook-sync open question; R5 §6 Monitor-tool-≠-daemon and troubleshoot-won't-auto-apply seams all explicitly flagged. No unsupported assertion was found stated as a verified fact.
- Spec defects correctly surfaced as defects (not silently inherited): `--cov` hyphen (R4), unregistered markers (R4), `--depth quick`×`--fix` conflict vs FR-3.2 (R3).

---

## Confidence Gate

- Item categorization: every evidence-quality check below was VERIFIED with tool output (Read/Bash/grep citing file:line).
- **Confidence:** Verified: 7/7 files + 6/6 load-bearing claims + 6 extra spot-checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 7 | Grep: 0 (greps run via Bash) | Glob: 0 | Bash: 6 (each targeting specific cited file:line claims — `ls`/`wc`/`sed`/`grep`/`git remote`/`find`/`gh --version`)
- No UNCHECKED items. No UNVERIFIABLE items. Spot-check coverage well exceeds the 25% requirement (>30 distinct path/line claims independently re-verified across all 7 files).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Claims are evidence-based (file:line / fn names) | PASS | Every research file cites file:line; sampled 30+ refs, all real |
| 2 | >=25% cited paths spot-checked & exist | PASS | 6 Bash verification rounds; all targets resolved |
| 3 | R4 `--cov` hyphen defect & `submit_pr` pkg | PASS | spec:1025 hyphen confirmed; underscored-pkg precedent live |
| 4 | R4 strict-markers / markers / coverage | PASS | pyproject:109-148 read; unregistered markers correctly flagged |
| 5 | R3 `--depth quick`+`--fix` STOP | PASS | troubleshoot SKILL.md:131 verbatim |
| 6 | R3 severity-rubric schema at cited lines | PASS | tiers :12, remap :63-101 read step-for-step |
| 7 | R6 remote=origin only / no Augment JSON | PASS | git remote -v + find both confirm |
| 8 | R5 lint-architecture pairing + Skill precedent | PASS | Makefile:362-419, install_skills.py:12-42 |
| 9 | No unsupported assertions as fact | PASS | spec defects surfaced as defects; seams flagged |
| 10 | [UNVERIFIED]/flagged items honest | PASS | DET HALT, hook-sync OQ, Monitor/troubleshoot seams all flagged |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | 02 (R2) & 05 (R5) top headers | `**Status: In Progress**` at top while footer says Complete | Builder may ignore; flip top header to Complete if regenerating |
| 2 | MINOR | 03 (R3) evidence-validator cite | "troubleshoot SKILL.md:409" anchor drifts ~3 lines from the actual spawn paragraph (substance correct) | Cite the "File:line validation pass" step line; non-blocking |
| 3 | MINOR | 01 (R1) vs 03 (R3) | rubric line count 172 vs 173 (no trailing newline) | Immaterial; either is fine |

None of these block the task builder. All are cosmetic/citation-precision nits; every load-bearing fact a builder would act on is correct and independently verified.

## Recommendations
- Builder may proceed. The four spec defects the research surfaced (hyphen `--cov`, 5 unregistered pytest markers, `--depth quick`×`--fix` conflict, DET-probe HALT gate) MUST be encoded as task items — they are correct and load-bearing.
- DET probe item must be `needs_human_decision` + write PENDING + HALT (never auto-lock) per R6 §1.3 — this is the single highest-stakes correctness item; research handles it correctly.

---

## VERDICT: PASS

Evidence quality is high across all 7 research files. Spot-checking exceeded the 25% requirement (30+ independent re-verifications); all 6 designated load-bearing claims confirmed against real source. Three MINOR cosmetic/citation-precision nits found; zero CRITICAL or IMPORTANT issues. No fabricated paths, no unsupported assertions stated as fact, all genuine unknowns honestly flagged.

## QA Complete
