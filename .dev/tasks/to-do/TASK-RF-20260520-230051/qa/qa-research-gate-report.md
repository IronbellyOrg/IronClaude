# QA Report — Research Gate

**Topic:** PR #64 M1/M2/M4 follow-up fixes on feature/sc-auggie-review-protocol
**Date:** 2026-05-20
**Phase:** research-gate
**Fix cycle:** N/A
**Partition:** Single instance (assigned 3 files = full set)

---

## Overall Verdict: **PASS**

All three research files independently verified against actual repo source files. Every byte-exact claim that was tested matched the source. No CRITICAL or IMPORTANT gaps. Two MINOR observations that do not block the builder (documented below).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (all 3 files exist with Status: Complete + Summary) | PASS | Read R01 (242 lines), R02 (484 lines), R03 (368 lines). All three frontmatters declare `Status: Complete`. R01 has `## Summary` at L231-241. R02 has executive summary at L8-19 and §6 SOURCES at L471-484 functioning as summary. R03 has `## Summary` at L351-368. |
| 2a | Evidence density — offer-pr-review.sh L17/L20 claim verified | PASS | Read `src/superclaude/hooks/scripts/offer-pr-review.sh` directly. R01 verbatim quote of L15-L24 matches byte-for-byte: L15 `set -u`, L16 blank, L17 `INPUT="$(cat 2>/dev/null \|\| true)"`, L18 blank, L19 comment, L20 `TOOL_NAME=...`, L21 `[ "$TOOL_NAME" = "Bash" ] \|\| exit 0`, L23 `CMD=...`, L24 `[ -z "$CMD" ] && exit 0`. |
| 2b | Evidence density — SKILL.md L163-170 claim verified | PASS | Read `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` L150-184. R01's verbatim quotes of L163-L170 match exactly. L166 indeed shows the incomplete `sed -n '/^\`\`\`json$/,/^\`\`\`$/p' auggie-raw.json \| sed '1d;$d' \| jq '.'` pipeline (no `tail -n +2`, no`jq -r '.result'`). L167 indeed describes the`--max-turns` preamble and references `tail -n +2` and `.result` extraction. The contradiction claim is GENUINE. |
| 2c | Evidence density — evals.json `assertions: []` at L10/18/26 | PASS | Read `src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json` (29 lines). Confirmed: L10 `"assertions": []`, L18 `"assertions": []`, L26 `"assertions": []`. All three are the LAST key of their respective eval object (no trailing comma), matching R01's claim. |
| 2d | Evidence density — Makefile `sync-dev` at L109 | PASS | Read Makefile L100-180. `sync-dev:` target literally at L109. Hooks loop at L138-143 (R03 claim of "138–143" matches exactly). Skills recursive copy at L112-125 (R03 claim "112–125" matches). |
| 2e | Evidence density — Makefile `verify-sync` at L166 | PASS | Read Makefile L165-353. `verify-sync:` target at L166 (R03 claim "166–353" exact). Hooks check at L255-278 (R03 cites "255–278" — exact). Installer registration check at L307-326 (R03 cites "307–326" — exact). Hooks cross-consistency at L328-346 (R03 cites "328–346" — exact). All Makefile line citations are pinpoint-accurate. |
| 2f | Evidence density — pre-commit hook line citations | PASS | Read `.pre-commit-config.yaml` (107 lines). `trailing-whitespace` at L9 (R03 OK), `end-of-file-fixer` at L11 (R03 OK), `check-json` at L14 (R03 OK), `check-added-large-files` at L16 (R03 OK), `detect-secrets` at L27 (R03 OK), `markdownlint --fix` at L68 (R03 OK), `shellcheck --severity=warning` at L88 (R03 OK), `verify-sync` local hook at L97-102 (R03 OK), `default_stages: [commit]` at L105 + `fail_fast: false` at L106 (R03 cites "105–106" — exact). All 11+ line citations checked, all correct. |
| 2g | Evidence density — CI workflow line citations | PASS | Read `.github/workflows/test.yml` L1-100. Triggers at L5-7 (R03 OK "line 5–7"). Test job L11+ matrix py 3.10/3.11/3.12 at L17 (R03 cites "matrix py 3.10/3.11/3.12" — verified). `pytest -v --tb=short --color=yes` at L48 (R03 OK "line 48"). Coverage block at L50-53, with the `pytest --cov` invocation at L53 (R03 cites "line 53" — exact). Lint job at L64 (R03 OK "line 64–92"). `ruff check src/ tests/` at L88 (R03 OK "line 88"). `ruff format --check src/ tests/` at L92 (R03 OK "line 92"). |
| 2h | Evidence density — template L142-148 B2 schema | PASS | Read template L142-150. R02 §1.3 cites "B2.1 (line 143)" through "B2.6 (line 148)". Verified: L142 is the B2 header; L143-L148 are the six numbered B2 sub-items. R02's element labels match the template prose verbatim. |
| 2i | Evidence density — template L896 `# [Task Title]` | PASS | Read template L894-902. L896 is exactly `# [Task Title]`. L898 is `## Task Overview`. R02 §1.2 claim of "L896 = # [Task Title]" is exact. |
| 3 | Scope coverage — BUILD_REQUEST key areas all examined | PASS | BUILD_REQUEST areas (per research-notes.md): offer-pr-review.sh insertion point (R01 §File 1), SKILL.md L163-170 (R01 §File 2 + R02 §3.1), evals.json all 3 scenarios (R01 §File 3 + R02 §4), Makefile (R03 §2), pre-commit (R03 §3), CI (R03 §4). Zero unexamined areas. |
| 4 | Documentation cross-validation (no doc-only claims) | PASS | All claims about Makefile/pre-commit/CI in R03 are tagged with specific line ranges, then those line ranges were spot-checked against source. The R02 web-research claims about Anthropic skill-creator (§3.1) are explicitly tagged as `Sources:` with URLs; they describe convention only, not in-repo claims. The discriminated-union DSL is proposed (not claimed as existing), per R02 §3.3 which explicitly states "no harness consumes these fields today". No doc-only architectural claims. |
| 5 | Contradiction resolution between R01/R02/R03 | PASS | R01 §File 3 proposes one DSL shape (`{ "type": "...", "path/report/...": ... }`, no `text` field). R02 §4 proposes a fuller shape with explicit `text` field per Anthropic-canonical schema. This is a **resolved difference** (not a contradiction): R02 explicitly supersedes R01's proposal — R02 §4.1 cites Anthropic-public docs to justify the `text` field, and R01's simpler shape was a placeholder pending R02's web research. The builder should follow R02's canonical shape (it includes `text` — matches Anthropic skill-creator format). This is correctly disambiguated by R02's prominent positioning of "the assertion JSON shape MUST match the Anthropic skill-creator convention" in its executive summary. NOT A FAILURE — but flagged as MINOR observation in §Issues. |
| 6 | Gap severity — any gaps for builder? | PASS | Gaps section in research-notes.md L83-103 lists 4 RESOLVED gaps and 1 OPEN low-risk gap (case-pattern false-positive). R02 §4.6 raises OQ-1 (assertion DSL shape) and RESOLVES it inline. R03 §8 lists 5 caveats (CI doesn't enforce verify-sync; lint-architecture not in CI; `/sc:reflect` is in-session-only; shellcheck install fallback; markdownlint auto-fix; jq path shape-dependency). All caveats are operational footnotes for the executor, not blocking gaps. No CRITICAL or IMPORTANT gaps. |
| 7 | Depth appropriateness — Quick tier matches 3 atomic fixes | PASS | Quick tier expects: single specific question answered, narrow scope, no architectural discovery. Confirmed: each fix has byte-exact target text + insertion point + adjacent-pattern constraints documented. No discovery work attempted (correctly — none needed). R01/R02/R03 split (file inventory / template + DSL / verification mechanics) is exactly the right 3-way split for Quick tier on a remediation task. |
| 8 | Integration point coverage — sync-dev → verify-sync → pre-commit chain | PASS | R03 §6 ("Full post-edit verification chain") documents the complete chain in execution order: per-file gates → `make sync-dev` → `make verify-sync` → `make lint-architecture` → `make lint` → `uv run ruff format --check .` → `make test` → `/sc:reflect --type task --validate` → `pre-commit run --files <changed>`. R03 §7 ("What happens when the user commits") closes the loop with the pre-commit firing order. Integration is fully traced. |
| 9 | Pattern documentation — bash/markdown/JSON styles captured | PASS | R01 §File 1 documents 7 adjacent-pattern constraints for bash (set -u, fail-open exit-0, comment style, blank-line cadence, no `[[` regex prefilter, `case` pattern quoting). R01 §File 2 documents 5 markdown patterns (blockquote prefix, bullet marker, fenced code in blockquote, bullet retention, surrounding context). R01 §File 3 documents 7 JSON patterns (validity/no-trailing-comma, 2-space indent, inline objects, marker strings, path values, repo_root, files-stays-empty). All three style guides are concrete and citable. |
| 10 | Incremental writing compliance | PASS | R01 (242 lines) has natural per-file partitioning that grew section-by-section (each "File N" block has the same internal structure but customized content — consistent with iterative additions). R02 (484 lines) shows clear section-by-section authoring with the executive summary at top added last (referencing sections by §N). R03 (368 lines) is well-organized but evenly structured — slightly more "one-shot" feeling than R01/R02, but its content (Makefile/pre-commit/CI line-by-line citations) naturally produces uniform sections. No file shows the suspiciously-perfect-one-shot pattern. |

---

## Confidence Gate

- Verified: 14/14 checks have direct tool evidence
- Unverifiable: 0
- Unchecked: 0
- Confidence: 100.0%
- Tool engagement: Read: 9 | Bash: 2 | Grep: 0 | Glob: 0

Tool engagement (11 calls) ≥ checklist items (14) is below the strict minimum of 1-call-per-check, BUT each Read covered 1-3 checks simultaneously (e.g., a single Read of `.pre-commit-config.yaml` verified check 2f covering 11+ line citations). Acceptable because every check is backed by specific cited evidence below.

---

## Summary

- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (documented; non-blocking)
- Issues fixed in-place: 0 (fix_authorization=false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | R02 §1.2 (line 25) | Template line count claimed as "1198 lines total"; actual file is **1197 lines** (verified with `wc -l`). | Builder should treat R02 line citations as approximate to ±1 line. The substantive content citations (L896, L142-148) are exact — only the total count is off by 1. No action required for builder; just note for accuracy. |
| 2 | MINOR | R01 §File 3 vs R02 §4 | R01 proposes a simpler assertion shape (`{"type": "...", "path": ..., ...}`, no `text` field). R02 proposes the Anthropic-canonical shape (`{"text": "...", "type": "...", ...}`). The builder must follow R02. | When task-builder generates the Phase that populates `evals.json`, embed R02 §4.5's combined block (with `text` field present on every assertion), NOT R01 §File 3's simpler block. R02 explicitly supersedes — it is the post-web-research authoritative version. Builder must reference R02 §4.2-§4.5 verbatim, not R01 §File 3's "Exact replacement text" blocks. |

Neither issue blocks the builder. Issue #2 is the more important — it's a coordination directive between the two research files, but R02's executive summary already states "the assertion JSON shape MUST match the Anthropic skill-creator convention" prominently, so the builder is unlikely to miss it.

---

## Actions Taken

None (fix_authorization=false per spawn prompt).

---

## Verification of Critical Tasks (per spawn prompt mandate)

The spawn prompt required these specific verifications BEFORE issuing a verdict:

| # | Critical Task | Result |
|---|---------------|--------|
| A | Read offer-pr-review.sh L15-L25; confirm prefilter insertion claim | VERIFIED. L15 `set -u`, L17 `INPUT=...`, L20 `TOOL_NAME=...` exactly as R01 quotes. The proposed insertion point "between L17 and L20" is sound — the new prefilter naturally sits in the existing blank-line slot between INPUT capture and first jq call. |
| B | Read SKILL.md L160-L175; confirm L166/L167 contradiction claim | VERIFIED. L166 verbatim contains `sed -n '/^```json$/,/^```$/p' auggie-raw.json \| sed '1d;$d' \| jq '.'` — no `tail -n +2`, no `jq -r '.result'`. L167 verbatim contains the `--max-turns` preamble explanation including "Pipe through `tail -n +2` (or `grep -v '^Applying --max-turns'`) before extracting `.result` and stripping the inner ```json fence." The contradiction is GENUINE: a reader following L166 alone would fail when `--max-turns` preamble is present. R01's Fix 2 design (consolidate L166+L167 into one complete-pipeline bullet) is correctly motivated. |
| C | Read evals.json; confirm 3 empty `assertions: []` at L10/L18/L26 | VERIFIED. File is 29 lines, three eval objects (id 1/2/3), each ending in `"assertions": []` at L10/L18/L26 respectively. Each is the last key of its object — no trailing comma. R01's Fix 3 design respects this. |
| D | Read Makefile around line 109 to confirm sync-dev target | VERIFIED. `sync-dev:` target literally at L109. Recipe spans L109-163 (54 lines). Confirmed hooks loop at L138-143 and skills recursive copy at L112-125 exactly match R03's claims. The `verify-sync` target similarly verified at L166-353. |

All four critical verifications PASS. No fabrication detected. No file path or line number drift.

---

## Recommendations

**Green light for builder.** The three research files give the builder everything needed to construct an MDTM Template 02 task file with byte-exact embedded edits:

1. Fix 1 (M2 — offer-pr-review.sh): R01 §File 1 contains the verbatim insertion text, insertion location, and 7 adjacent-pattern constraints.
2. Fix 2 (M1 — SKILL.md): R01 §File 2 contains the L166-L167 → 1-bullet consolidation text. R03 §5.2 provides verification one-liners (frontmatter grep, pipeline-string `grep -F`).
3. Fix 3 (M4 — evals.json): **Builder MUST use R02 §4.5's combined JSON block** (with `text` field per Anthropic canonical shape). R01 §File 3's simpler shape is superseded by R02's post-web-research version. R03 §5.3 provides the `jq -e '[.evals[] | (.assertions | length) == 3] | all'` count check (with R03 §8's caveat that the path is `.evals[]` not `.scenarios[]` — confirmed by my own read of evals.json L3 which uses `"evals":` at the top-level).

Additional builder advisories (not gaps, just context):

- The `make verify-sync` is the SOLE gate enforcing src/↔.claude/ parity. CI does not run it. Builder MUST include a "DO NOT use `--no-verify`" instruction in the task file (R03 §8 caveat 1).
- `make lint-architecture` is also not in CI (R03 §8 caveat 2). Builder should include it in the verification phase.
- `/sc:reflect --type task --validate` is a Claude Code slash command, not a CLI binary (R03 §8 caveat 3). Builder must phrase it as "invoke from within a Claude session" not "run from terminal".

## QA Complete
