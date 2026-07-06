# Reflect Pre-Execution Audit — Phase 4: Tests & Verification

| Field | Value |
|---|---|
| Mode | UC-1 (pre-execution coverage/gap audit) |
| Invocation | `/sc:reflect --mode pre --depth standard --tier auto` |
| Spec | `.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/merged-requirements.md` |
| Tasklist | `.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-4-tasklist.md` |
| Tasks audited | T04.01–T04.05 (3 work tasks + 1 checkpoint + 1 reflect) |
| Assigned roadmap items | R-008, R-009, R-012 |
| Tier reached | **1** (rubric STOP — §5.3 rule 1) |
| Coverage (assigned roadmap items) | **3 / 3 = 1.00** |
| Spec test coverage (§4, 15 tests) | **15 / 15 assigned** |
| Calibrated confidence | **0.90** |
| Citations (total / dropped / inferred) | 4 / 0 / 0 |
| **VERDICT** | **PASS** |

## 1. Coverage Matrix (spec → task)

| Spec requirement | Roadmap | Task | Grounding (verified) | Status |
|---|---|---|---|---|
| FR-9 / §4 unit+regression suite (no live CLI/Node/key) | R-009, R-012 | T04.01 | no existing tavily/mcp test module → greenfield; `tests/cli/` exists (natural home); `_run_command`/`prompt_for_api_key`/`check_mcp_server_installed` are mockable seams at `:113`/`:492`/`:470` | ✅ mapped |
| FR-8 map/crawl tool-surface verification (optional integration) | R-008 | T04.02 | docs/test smoke; skip-by-default when prerequisites absent | ✅ mapped |
| §4 final validation commands (UV) + sync checklist | R-009 | T04.03 | `uv run pytest <module> -v` per project rule | ✅ mapped |

### §4 fifteen-test assignment

| # | Test | Owning task |
|---|---|---|
| 1 registry token `@latest` | T04.01 |
| 2 no stale `0.1.x` pin in active source | T04.01 (+ T03.03 parity) |
| 3 fresh install command grammar | T04.01 |
| 4 stale install → remove-then-add | T04.01 |
| 5 current install → skip | T04.01 |
| 6 dry-run stale intent (no subprocess) | T04.01 |
| 7 dry-run fresh add, no remove | T04.01 |
| 8 API-key env via `-e` | T04.01 |
| 9 API-key display redaction | T04.01 |
| 10 docs-installer parity | T03.03 (authored) → exercised by suite |
| 11 dormant config cleanup | T03.03 (authored) → exercised by suite |
| 12 transport default stdio | T04.01 |
| 13 command-ordering regression | T04.01 (relies on T01.02 seam) |
| 14 installed-check handles empty/None stdout | T04.01 |
| 15 optional live map/crawl surface | T04.02 |

## 2. Gaps & Observations

No blocking coverage gaps. All assigned roadmap items and all 15 spec tests have an owning task.

- **[MEDIUM] O-1 — Ownership overlap on tests #10/#11 between T03.03 and T04.01.** T03.03 (Phase 3, D-0009) is defined as the docs/config **parity regression guard** (tests 10+11). T04.01 (Phase 4, D-0010) lists "docs parity, config cleanup" among its cases too. Both reference `tests/`. Risk: duplicate/competing assertions or a "which task writes this?" ambiguity at execution. *Cross-task interaction* (§4 Wave 1B.3 class). **Recommend** stating one canonical owner — e.g. T03.03 authors the parity/cleanup tests in the shared Tavily module, and T04.01 imports/extends rather than re-authoring. Non-blocking but should be disambiguated before execution to avoid drift between two phases.
- **[LOW] O-2 — Test #2 ("no `0.1.x` in active source") spans phases.** The repo-wide stale-pin scan is logically the same assertion the T03.03 parity guard makes; T04.01 also claims it. Same canonical-owner remedy as O-1. Grounding confirms exactly one live pin (`install_mcp.py:80`) and the dormant configs carry `mcp-remote` (not `0.1.x`), so the scan's exclusion list (active vs historical) per T03.03 step 2 must be set so the parity test does not false-positive on this audit bundle's own quoted `0.1.2` strings.
- **[LOW] O-3 — `<PHASE_4_START_SHA>` placeholder** in frontmatter + T04.05 reflect gate; resolved at execution by the wrapper (T04.05 step 1). Confirm the resolver before the post-reflect gate runs.
- **[INFO] O-4 — Test-module path is a free choice (`tests/cli/test_install_mcp_tavily.py` *or* `tests/mcp/test_tavily_upgrade.py`).** Grounding: `tests/cli/` exists, `tests/mcp/` does not. T04.01 step 1 defers the choice to existing organization; `tests/cli/` is the lower-friction landing. No gap.

## 3. Tier Decision (rubric — §5.3)

`--tier auto` + `--depth standard`. Inputs: C≈0.90, S_scope≈1–2 files (new test module + optional smoke), S_domains=1 (tests), S_dev_density≈0, coverage=1.00 → **rule 1 STOP at T1**. Matches depth-map (`complexity_score: 5`, `deterministic_tier: auto`). The one STRICT task (T04.01) raises rigor but not multi-domain/regression escalation triggers; O-1 is a coordination note, not a regression candidate.

## 4. Grounding & Honesty

- Grounding via native `Read`/`Grep`/`Bash` (`degraded_components: ["mcp-reviewer-ensemble"]`, inline calibration).
- Evidence-validator: inline re-Read of all 4 citations; **0 dropped** (`zero-drop-flag: true`).

## 5. Recommendation

**PASS — Phase 4 is execution-ready.** Resolve O-1 (canonical owner for the shared docs/config parity tests #2/#10/#11 across T03.03 ↔ T04.01) before execution to prevent duplicate or drifting assertions. This is the highest-value pre-execution tightening in the bundle; still non-blocking.
