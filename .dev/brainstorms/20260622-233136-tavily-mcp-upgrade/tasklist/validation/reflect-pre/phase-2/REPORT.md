# Reflect Pre-Execution Audit — Phase 2: Migration & Redaction

| Field | Value |
|---|---|
| Mode | UC-1 (pre-execution coverage/gap audit) |
| Invocation | `/sc:reflect --mode pre --depth deep --tier 2` |
| Spec | `.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/merged-requirements.md` |
| Tasklist | `.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/tasklist/phase-2-tasklist.md` |
| Tasks audited | T02.01–T02.05 (3 work tasks + 1 checkpoint + 1 reflect) |
| Assigned roadmap items | R-004, R-005, R-010 |
| Tier reached | **2** (forced by `--depth deep` / `--tier 2`; also justified — High-risk migration task T02.01, §5.3 rule 3 logic) |
| Coverage (assigned roadmap items) | **3 / 3 = 1.00** |
| Calibrated confidence | **0.89** |
| Citations (total / dropped / inferred) | 6 / 0 / 0 |
| **VERDICT** | **PASS** |

## 1. Coverage Matrix (spec → task)

| Spec requirement | Roadmap | Task | Grounding (verified) | Status |
|---|---|---|---|---|
| FR-3 stale Tavily reconciliation (detect 0.1.x install, remove-then-add, dry-run intent) | R-004 | T02.01 | name-only `check_mcp_server_installed()` at `install_mcp.py:470`; short-circuit in `install_mcp_server()` at `:536` — name-only today, stale not detected (premise valid) | ✅ mapped |
| FR-4 redact API-key values in displayed commands | R-005 | T02.02 | no redaction/mask token anywhere in `install_mcp.py`; command echo at `:622` (premise valid) | ✅ mapped |
| FR (Migration §5) back-compat across 5 user states | R-010 | T02.01 + T02.03 | spec §5 table (no-install / stale / current / AIRIS gateway / missing key); `prompt_for_api_key()` at `:492` anchors missing-key state | ✅ mapped |

## 2. Deep-Pass Findings (Tier 2 — adversarial lens applied)

The Tier-2 escalation exists to defeat single-frame confirmation. Three independent lenses were applied (correctness, secret-exposure, migration-safety). Findings below are graded by whether they block execution.

- **[MEDIUM] F-1 — FR-4 AC#2 redaction must cover an output path the current code does not yet emit.** Spec FR-4 AC#2 requires masked env display "e.g. `TAVILY_API_KEY=***`". Grounding shows the human-facing echo at `:622` (`Running: claude mcp add --transport {transport} {server_name} -- {command}`) currently **omits the `-e KEY=VALUE` env args entirely** — the env args are appended to the argv list (~`:597–620`) but not to the displayed string. So the redaction helper (T02.02) must redact the *dry-run* path AND any newly-added env echo, not just filter an existing leak. T02.02 step 1 ("identify all installer command echo/dry-run output paths") covers this, but the task does not explicitly note that today's echo omits env — an executor could "verify no leak" against the current echo and under-build. **Recommend** T02.02 explicitly enumerate: (a) dry-run output, (b) the `-e` env echo if/when added, (c) the `tavilyApiKey=` URL query form. *Non-blocking* — the deliverable list already names "env values and Tavily API-key URL query forms".
- **[MEDIUM] F-2 — FR-4 URL-query redaction target lives in a Phase-3-deleted artifact.** The only `tavilyApiKey=` occurrence in the repo is in the dormant JSON configs (`src/superclaude/mcp/configs/tavily.json:7`, `plugins/...:7`), which Phase 3 (T03.02) deletes. FR-4 AC#3 ("any future URL query form … is redacted before display") is therefore *forward-looking* (remote HTTP is a future path). T02.02 correctly treats it as a display-helper rule, not a live code path. No conflict, but the executor should not expect a live URL echo to redact today. Noted so the redaction test is written as a unit test of the helper, not an integration assertion against current output.
- **[LOW] F-3 — `claude mcp get` fallback is a spec implementation note (§6), absent from T02.01 ACs.** Spec §6 says stale detection via `claude mcp get` must "gracefully fall back if that subcommand is unavailable; tests can mock both success and unavailable cases." T02.01 ACs assert remove-before-add and current-skip but do not name the `mcp get` unavailable-fallback case. The matching test (T04.01 / spec test-list) should cover it; recommend T02.01 or T02.03's matrix add the "stale-detection-probe-unavailable" row so it is not silently dropped.
- **[LOW] F-4 — `start_commit: "<PHASE_2_START_SHA>"` placeholder.** Frontmatter and the T02.05 reflect gate carry an unresolved `<PHASE_2_START_SHA>`. By design the wrapper resolves it at execution (T02.05 step 1). Confirm the resolver is wired before running the post-reflect gate; otherwise the `--base` ref will be literal. Low severity (execution-time concern, not a coverage gap).

## 3. Tier Decision (rubric — §5.3)

`--tier 2` is a §5.1 hard override → escalate. Independently warranted: T02.01 is the bundle's only **High-risk** task (risk drivers: credentials, migration), and migration/secret-handling is the asymmetric-cost surface where ensemble pressure is correct. `n_high_risk: 1`, `complexity_score: 10` in the depth-map agree.

## 4. Grounding & Honesty

- Grounding via native `Read`/`Grep`/`Bash`. The full heterogeneous multi-model reviewer ensemble + `sc-adversarial-protocol` merge was **not** separately spawned in this interactive run; the three lenses above were applied inline by the orchestrator. Recorded honestly as `t2_model_class_diversity: degraded`, `merge_method: single-reviewer-fallback`, `degraded_components: ["mcp-reviewer-ensemble","adversarial-merge"]`. Per §11.0 the anti-confirmation guarantee is therefore "ensemble pressure applied," not "self-confirmation neutralised."
- Evidence-validator: inline re-Read of all 6 citations; **0 dropped** (`zero-drop-flag: true`).

## 5. Recommendation

**PASS — Phase 2 is execution-ready.** No blocking gaps. Before execution, fold F-1 (enumerate all redaction output paths) and F-3 (`mcp get` unavailable fallback row) into the T02.02 / T02.03 acceptance criteria so they are not lost during implementation. These are tightening edits, not new scope.
