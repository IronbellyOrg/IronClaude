# QA Report — Synthesis Gate (Flag-Completeness Lens, Phase 3)

**Topic:** Wire `--context` / `--caller` into /sc:troubleshoot — 9-site ingestion completeness
**Date:** 2026-06-16
**Phase:** report-validation (structural flag-completeness lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Adversarial stance:** Assumed ≥5 missing/duplicated sites; searched all occurrences across both files.

---

## Overall Verdict: PASS

Both `--context` and `--caller` are wired at all 9 required ingestion sites, each present exactly once at its required location, with no missing wiring and no unwanted duplicate ingestion site.

## Items Reviewed (9 required sites)

| # | Required site | File | Line | Result | Evidence (verbatim line text) |
|---|---------------|------|------|--------|-------------------------------|
| 1 | command argument-hint (frontmatter) | troubleshoot.md | 8 | PASS | `argument-hint: "... [--no-mcp] [--context <path>] [--caller <name>]"` — both flags terminate the hint string |
| 2 | command Options table (one row each) | troubleshoot.md | 59, 60 | PASS | L59 `\| `--context` \| (none) \| Path to a caller-supplied context file ...`; L60 `\| `--caller` \| (none) \| Name of the invoking pipeline/command ...` — exactly one row each (grep `^\| \`--context\``/`^\| \`--caller\`` = 1 each) |
| 3 | command Behavioral-Summary parse step | troubleshoot.md | 66 | PASS | `1. **Parse arguments** → resolve `--type` (auto-detect if absent), `--scope`, `--depth`, `--context`, `--caller`, etc.` — both present in the single "Parse arguments" step (grep `Parse arguments` = 1 occurrence) |
| 4 | command "On skill return, surface:" return-contract clause | troubleshoot.md | 69 | PASS | `4. **On skill return**, surface: ... and (if caller=task-unified) the emitted return-contract.yaml path.` — the return-contract path clause is wired off `caller` |
| 5 | skill Wave 0 step 1 flag-parse sentence (Optional: enumeration) | SKILL.md | 115 | PASS | `1. Parse flags. Required: issue description OR `--scope`. Optional: ... `--reset-diagnosability-rounds`, `--context`, `--caller`.` — both terminate the Optional enumeration |
| 6 | skill Wave 0 resolve sub-step (new step 6) | SKILL.md | 143 | PASS | `6. If `--caller` is set, record it in the audit header `caller:` field ... If `--context <path>` is set, read it ... resolve it to an absolute path; STOP if the path is unreadable. When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` ...` — confirmed numbered step **6** (sed -n '143p' begins `6.`) |
| 7 | skill Wave 0 STOP conditions (`--context` path unreadable) | SKILL.md | 147 | PASS | `**STOP conditions**: ... `--output-dir` not writable, `--context` path unreadable.` — the `--context` unreadable STOP clause present |
| 8 | skill audit TARGET header (`caller:`, `context_path:`) | SKILL.md | 138, 139 | PASS | TARGET block opens at L129 (`<!-- SC:TROUBLESHOOT:TARGET`); L138 `caller: <name\|none>`; L139 `context_path: <abs-path\|none>` — both inside the TARGET block |
| 9 | skill SUMMARY footer (`caller:`, `return_contract_path:`) | SKILL.md | 460, 461 | PASS | SUMMARY block opens at L451 (`<!-- SC:TROUBLESHOOT:SUMMARY`); L460 `caller: <name\|none>`; L461 `return_contract_path: <abs-path\|none>` — both inside the SUMMARY block |

## Duplicate / over-ingestion audit (adversarial)

Assumed ≥5 duplicates existed; searched every occurrence of both tokens across both files.

| Token | File | Total occurrences | Breakdown | Verdict |
|-------|------|-------------------|-----------|---------|
| `--context` | troubleshoot.md | 3 | argument-hint (L8), Options row (L59), parse step (L66) | One per required site — no duplicate |
| `--caller` | troubleshoot.md | 3 | argument-hint (L8), Options row (L60), parse step (L66) | One per required site — no duplicate |
| `--context` | SKILL.md | 3 | parse sentence (L115), resolve step 6 (L143), STOP clause (L147) | All three are distinct required sites (5, 6, 7) — **not** a duplicate; `--context` legitimately appears in both the parse enumeration and the STOP condition by design |
| `--caller` | SKILL.md | 2 | parse sentence (L115), resolve step 6 (L143) | One per required site — no duplicate |
| `caller:` (header field) | SKILL.md | 2 | TARGET block L138, SUMMARY block L460 | Two **distinct** sites (8 + 9), not a duplicate — confirmed inside different comment blocks |
| `context_path:` | SKILL.md | 1 | TARGET block L139 | Exactly one, in TARGET (site 8) |
| `return_contract_path:` | SKILL.md | 1 | SUMMARY block L461 | Exactly one, in SUMMARY (site 9) |
| argument-hint (frontmatter) | troubleshoot.md | 1 | L8 | Single argument-hint line — no second/competing hint |
| Options row `--context` / `--caller` | troubleshoot.md | 1 each | L59 / L60 | No duplicate table rows |
| "Parse arguments" step | troubleshoot.md | 1 | L66 | No duplicate parse step |

No stray second argument-hint, no duplicate Options row, no second resolve step, no double-resolution path. The two `caller:` lines are the two intended distinct emission points (audit-header ingest + summary-footer echo), not an accidental duplicate.

## Summary
- Required sites verified: 9 / 9 PASS
- Missing wiring: 0
- Unwanted duplicates: 0
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: N/A (report-only)

## Issues Found

None. (Adversarial duplicate/over-ingestion sweep returned zero hits.)

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 4 (grep via Bash — Grep tool unavailable this session; each Bash call directly verified specific sites: site enumeration, site-4 return clause + per-token counts, header/footer block placement, full occurrence sweep + Options-row/argument-hint uniqueness)
- Every site verified against verbatim line text from the source files; no item relied on report claims.

## Recommendations

- Green light for this lens. All 9 ingestion sites are wired exactly once. No remediation required from the flag-completeness perspective.
- Note for orchestrator: this lens verifies PRESENCE + UNIQUENESS of wiring only. It does not verify semantic correctness of the return-contract.yaml adapter emission logic, the `caller=task-unified` gating behavior, or that `--context` ingestion actually feeds Wave 1.5/Wave 5 — those belong to a behavioral/semantic lens.

## QA Complete
