# Research: Integration Points (cross-file consumers)

**Topic type:** Integration Points
**Scope:** whole `/config/workspace/IronClaude/` repo EXCLUDING `.claude/` (gitignored mirror), `node_modules`, `.venv`, `__pycache__`
**Spec:** `merged-report-v2.md` §(d) R-01..R-19
**Status:** Complete
**Date:** 2026-09-19

---

## 1. References to target ref filenames OUTSIDE the skill dir

Grep: `rg -n -e 'triage-checklist' -e 'diagnosability-audit' -e 'hypothesis-card-template' -e 'escalation-rubric' -e 'hardening-output-contract' -e 'report-template' -e 'calibrator-eval-cases' -e 'runtime-entrypoint-verification' -e 'primitive-differential'` (excluding `.claude/`, `.dev/`, and the skill dir itself).

| Ref file | External hit (file:line) | Nature | Break risk from R-01..R-19 |
|---|---|---|---|
| `triage-checklist.md` | none | — | none |
| `diagnosability-audit.md` | none | — | none |
| `hypothesis-card-template.md` | none | — | none |
| `escalation-rubric.md` | `src/superclaude/commands/troubleshoot.md:163` | prose pointer (`refs/escalation-rubric.md`) | none (filename unchanged) |
| `escalation-rubric.md` | `src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md:53` | **line-number citation** `escalation-rubric.md:60-61` (the `--depth deep` → forced escalation rule; verified currently at `escalation-rubric.md:60-61`) | goes stale if any edit inserts/removes lines ABOVE line 60 of escalation-rubric.md. Cosmetic only (no test reads it). |
| `escalation-rubric.md` | `src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:22` | same `escalation-rubric.md:60-61` citation | same as above |
| `escalation-rubric.md` | `src/superclaude/agents/confidence-calibrator.md:48` | input `rubric_path` → `refs/escalation-rubric.md` | none (this file is a target file — file-inventory covers it) |
| `hardening-output-contract.md` | `tests/troubleshoot/test_hardening_output_contract.py:17` (read), `:65-77` asserts | test reads file; asserts backtest-status table strings | see §2/§3 for exact strings |
| `hardening-output-contract.md` | `tests/troubleshoot/test_hardening_verdict.py:18` (read), `:23-102` | test asserts §5.4 truth table, latch, enum | see §3 |
| `hardening-output-contract.md` | `tests/troubleshoot/backtest/_impl_guard.py:28` | existence-gate (`_FOUNDATION_REFS`) | none as long as the file exists |
| `hardening-output-contract.md` | `tests/troubleshoot/backtest/test_waiver_regreen.py:25,33` | loose lowercase asserts (`waiver_status`, `latch`, `blocked`, `advisory`, `success_with_hardening_*`) | none unless those tokens are removed |
| `report-template.md` (troubleshoot) | `tests/troubleshoot/test_hardening_output_contract.py:18` (read), `:84-98` | asserts `## Pipeline Hardening Closure`, verdict enum string, `NOT PROVEN` | **R-16 risk** — see §3 |
| `report-template.md` (OTHER skills, same basename) | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:707,880,1144,1820`; `src/superclaude/skills/sc-crash-recovery/SKILL.md:83,89,125` | these point at `sc-reflect-protocol/refs/report-template.md` and `sc-crash-recovery/refs/report-template.md` (both exist, verified via `ls`) — NOT the troubleshoot one | none; false positives on basename |
| `calibrator-eval-cases.md` | `src/superclaude/skills/confidence-check/SKILL.md:20` | prose pointer to the full path | none (filename unchanged; content additions in R-14/R-15 don't affect it) |
| `runtime-entrypoint-verification.md` | `tests/troubleshoot/test_hardening_h1.py:15` (read), `:19-48` | asserts 12 card field tokens + phrases `negative witness`, `fix reverted`, `never been observed to fail`, `satisfy h1`, `helper construction` | **must keep all these tokens** if R-xx edits this file |
| `runtime-entrypoint-verification.md` | `tests/troubleshoot/backtest/test_backtest_e1.py:78,81,85,88` | skip-gate + loose asserts (`negative witness`, `--file`/`runtime`/`entrypoint`) | none |
| `runtime-entrypoint-verification.md` | `tests/troubleshoot/backtest/test_catch_rate_aggregation.py:40`; `fixtures/catch_rate/valid_full.json:11`, `all_catch_missing_witness.json:11` | string `card_path` values in fixtures — not file reads | none |
| `primitive-differential.md` | **zero hits** anywhere (src/, tests/, docs/) | — | new file; nothing references it yet. Only `SKILL.md` refs table + any test the builder adds. |

Other hardening refs NOT in the spec edit list but read by tests (do not touch, or keep tokens): `pipeline-hardening-closure.md` (`test_hardening_h0.py:16`), `contract-enumeration.md` (`test_hardening_h2.py:16`, `test_backtest_e4.py:97`), `unmask-and-sweep.md` (`test_hardening_h3.py:16`, `test_backtest_e2.py:90`, `test_backtest_e3.py:103`), `effective-input-proof.md` (`test_hardening_h4.py:16`, `test_backtest_e5.py:70`), `remediation-handoff.md` (`test_hardening_verdict.py:61`).

**External consumer count for item 1: 4 non-test files** (`commands/troubleshoot.md`, `sc-pr-submit-protocol/refs/severity-routing.md`, `sc-pr-submit-protocol/refs/troubleshoot-dispatch.md`, `confidence-check/SKILL.md`) + **7 test modules** under `tests/troubleshoot/`.

## 2. Hardening labels `\bH[0-5]\b` and `HC[0-5]` (R-17 rename)

**`HC[0-5]`: zero hits** in src/, tests/, docs/ (`rg -n '\bHC[0-5]\b' src tests docs` → empty). The new label space is free.

**`\bH[0-5]\b`: 100+ files hit, but almost all are unrelated** — markdown heading levels (`H1`/`H2`/`H3` in `cli/roadmap/cosmetic_remediator.py`, `sc-adversarial-protocol/SKILL.md:670-672`, `sc-reflect-protocol/refs/reviewer-spec.md:45`, `sc-cli-portify-protocol/refs/pipeline-spec.md:184`), eval-pipeline hardening item IDs (`docs/user-guide/eval-pipeline.md:236,238,261`, `cli/sprint/executor.py:194,1428`, `tests/cli/eval/*`), MDTM template rule IDs (`templates/workflow/02_mdtm_template_complex_task.md:490-494`), tasklist finding IDs (`sc-tasklist-protocol/SKILL.md:1448-1480`). None of these are troubleshoot hardening gates — **do not rename them**.

`rg -ln 'pipeline.hardening|Pipeline Hardening|H0–H5|H0-H5' docs src tests` excluding the skill dir and `tests/troubleshoot/` → **empty**. The hardening-gate vocabulary lives ONLY in the skill dir + `tests/troubleshoot/`.

### 2a. Troubleshoot-domain hits, classified

| File:line | Text | Class | R-17 action |
|---|---|---|---|
| `SKILL.md:63` | "Wave 4.5 H0 classifies … Set exactly once by H0" | (a) protocol prose in Output Contract *description* column | rename H0→HC0 (field name `pipeline_hardening_applicable` unchanged) |
| `SKILL.md:64` | "aggregation of the H0–H5 statuses" | (a) | rename |
| `SKILL.md:67-71` | "Wave 4.5 H5 …", "H1 runtime-entrypoint card", "H2 …", "H3 …", "H4 …" | (a) prose in description column; (b) field names `off_path_review_decision`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path` must NOT change | rename prose only |
| `SKILL.md:104` | "runs gates H0-H5" | (a) | rename |
| `SKILL.md:408,410` | "gates H0–H5", "H0 sets …", "skip H1–H5" | (a) | rename |
| `SKILL.md:414-420` | Wave 4.5 step list "**H0 — …**" … "**H5 — …**", "H1–H5 cannot be silently skipped" | (a) | rename |
| `SKILL.md:444` | "the H0–H5 evidence-card paths" | (a) | rename |
| `SKILL.md:595-600` | refs table "(H0 applicability …)", "(H1 runtime-entrypoint card…)", … | (a) | rename |
| `refs/hardening-output-contract.md:3` | "the H5 decision-to-status mapping" | (a) | rename |
| `refs/hardening-output-contract.md:14-23` | schema table "Wave" column values `H0`, `H1-H5 / FR-12`, `H5`, `H1`…`H4`, `H0/closure` | (a) prose column; (b) field-name column (`pipeline_hardening_applicable`, `waiver_status`, `off_path_review_decision`, `runtime_entrypoint_card_path`, `contract_ledger_path`, `unmask_sweep_path`, `effective_input_card_path`, `known_escapes_caught`) must NOT change | rename Wave column only |
| `refs/hardening-output-contract.md:29,33,34,36,38,39` | truth table "evaluated after H0–H5", "H0 has reason", "Any H1-H5 status is `FAIL`" … | (a) | rename. **Keep verbatim**: `NOT PROVEN — failed hardening wave: <wave>`, `ADVISORY — closure relies on waived/substituted proof`, `ADVISORY — scoped closure with rationalized N/A`, `| No |` ×7 (asserted by `test_hardening_verdict.py:76-83`) |
| `refs/hardening-output-contract.md:43-48` | "## H5 decision-to-status mapping", "H5 Decision \| H5 Status" | (a) | rename. **Keep verbatim** the 4 rows `` `performed` \| `PASS` \| `none` `` etc. (`test_hardening_verdict.py:36-39`) |
| `refs/hardening-output-contract.md:58,69` | "run-level H0–H5 closure verdict", "set exactly once by H0; if `true`, H1–H5 must run" | (a) | rename |
| `refs/report-template.md:230-235` | "- **H0 Applicability + Boundary Scan**: <PASS\|FAIL\|N/A>" … "- **H5 Off-Path Reviewer + Waiver**" | (a)/(d) rendered report prose | rename (no test asserts these lines) |
| `refs/report-template.md:316` | "(any H1–H5 `FAIL`, …)" | (a) | rename; **keep** `NOT PROVEN` token (`test_hardening_output_contract.py:98`) |
| `refs/runtime-entrypoint-verification.md:1,3,7,9,11,28` | "# Runtime-Entrypoint Verification (H1)", "H1 proves…", "H1 **FAILs**", "does **not** satisfy H1" | (a) | rename — **BUT `test_hardening_h1.py:46` asserts `"satisfy h1" in low`** → renaming line 28 "satisfy H1" → "satisfy HC1" BREAKS that test unless the test is updated in the same change (or the phrase "satisfy H1" is retained somewhere). |
| `refs/pipeline-hardening-closure.md` (19 hits), `refs/contract-enumeration.md` (5), `refs/unmask-and-sweep.md` (7), `refs/effective-input-proof.md` (4) | gate names | (a) | in scope of R-17 if it says "protocol-side"; not in the spec's edit list per the brief — file-inventory owns the decision. Tests for these (`test_hardening_h0/h2/h3/h4.py`) assert field tokens + lowercase phrases, none of which contain `h[0-5]` except `test_hardening_h2.py:48` message text (not an assertion of file content). |
| `refs/calibrator-eval-cases.md:49` | "Replays actual H2 card from T4" | **HYPOTHESIS card label** (H2 = hypothesis #2), NOT a hardening gate | **do NOT rename to HC** — this is the collision R-17 is resolving; keep as H-hypothesis. |
| `refs/calibrator-eval-cases.md:54` | "Replays actual H1 card from T4" | hypothesis label | keep |
| `refs/escalation-rubric.md:35` | "(the H3 0.95-REFUTE case)" | hypothesis label | keep |
| `agents/confidence-calibrator.md`, `agents/evidence-validator.md`, `agents/root-cause-analyst.md`, `commands/troubleshoot.md` | **zero** `\bH[0-5]\b` hits | — | nothing to do |

### 2b. Test-side hits (class (c))

| File:line | What | Effect of R-17 |
|---|---|---|
| `tests/troubleshoot/test_hardening_h1.py:46` | `assert "satisfy h1" in low` against `runtime-entrypoint-verification.md` | **BREAKS** if "satisfy H1" is renamed. Must update test to `"satisfy hc1"` in the same commit (or keep phrase). |
| `tests/troubleshoot/test_hardening_h0.py:50`, `h1.py:38`, `h2.py:37,48`, `h3.py:63`, `h4.py:48` | f-string assertion *messages* ("H0 boundary-scan field missing") | cosmetic only; no content dependency |
| `tests/troubleshoot/backtest/catch_rate.py:52,79-80,96`; `git_replay.py:35-44`; `schemas/catch_rate.schema.json:98-101` | `wave: str` free-form field, docstrings say "H0..H5"; schema has **no enum** on `wave` | no break; labels are self-contained Python/JSON data |
| `tests/troubleshoot/backtest/test_catch_rate_schema.py:77-82,130,167,179,218,238,261,299,315-318,351`; `test_backtest_status_separation.py:43`; `test_git_replay_unit.py:85` (`escape_by_id("E4").wave == "H2"`) | `EscapeResult("E1","H1",…)` literals | self-contained; **not** read from the refs. Optional cosmetic follow-up to HC; not required. |
| `tests/troubleshoot/backtest/fixtures/catch_rate/valid_full.json:11-15`, `all_catch_missing_witness.json:11-12`, `invalid_bad_verdict.json:11` | `"wave": "H1"` fixture values | self-contained; no break |
| `tests/troubleshoot/e2e-backtest-scenarios.md` (15 hits) | scenario doc | (d) docs; goes stale, no test reads it |

### 2c. docs/ (class (d))
No `docs/` file references the troubleshoot hardening gates (verified by the `pipeline.hardening` grep above). Nothing goes stale in `docs/` from R-17.

## 3. `pipeline_hardening_verdict` / `not_applicable` / `blocked_pending` / `waiver_status` / `latched` (R-16 adds `blocked-on-authorization`)

**Outside the skill dir + `tests/troubleshoot/`: zero hits** for `pipeline_hardening_verdict`, `waiver_status`, `latched`, `blocked_pending`, `blocked-on-authorization`, `blocked_on_authorization` (grep across `.` excluding `.claude/`, `.dev/`). `not_applicable` outside the skill/tests: zero hits. **No external consumer reads the hardening verdict** (sc-pr-submit / sc-task / task-unified do not touch it — see §4).

`blocked_pending`: **zero hits anywhere** (not even in the skill). If the spec references it as a pre-existing token it is not in this repo.

### 3a. In-skill enum sites (all must be edited together for R-16)

| File:line | Current text |
|---|---|
| `SKILL.md:64` | `enum \`pass \| blocked \| advisory \| not_applicable\`` (Output Contract table) |
| `SKILL.md:420` | `pipeline_hardening_verdict ∈ \`pass \| blocked \| advisory \| not_applicable\`` |
| `SKILL.md:444` | `(\`pass\`/\`blocked\`/\`advisory\`/\`not_applicable\`)` |
| `refs/hardening-output-contract.md:5` | "the **four-token** enum `pass \| blocked \| advisory \| not_applicable`" |
| `refs/hardening-output-contract.md:15` | schema row `enum \`pass\|blocked\|advisory\|not_applicable\`` |
| `refs/hardening-output-contract.md:31-39` | 7-row truth table (priority order) |
| `refs/report-template.md:223` | `<pass\|blocked\|advisory\|not_applicable>` |
| `refs/report-template.md:315` | "Closure verdict is the four-token enum `pass \| blocked \| advisory \| not_applicable`" |
| `refs/pipeline-hardening-closure.md:13` | "four-token enum `pass \| blocked \| advisory \| not_applicable`" |
| `refs/remediation-handoff.md:35,69` | `<pass \| blocked \| advisory \| not_applicable>` in BUILD_REQUEST |

### 3b. Test assertions that pin the enum string — R-16 BREAK RISK

| Test | Assertion | Breaks if… |
|---|---|---|
| `tests/troubleshoot/test_hardening_verdict.py:51` | `assert "pass \| blocked \| advisory \| not_applicable" in OC` (exact substring) | the token is inserted INSIDE the enum string in `hardening-output-contract.md` (e.g. `pass \| blocked \| blocked-on-authorization \| advisory \| not_applicable`). Safe if appended at the END (`… \| not_applicable \| blocked-on-authorization`) or if the 4-token string is left intact somewhere in OC. |
| `tests/troubleshoot/test_hardening_output_contract.py:92-95` | `"pass\|blocked\|advisory\|not_applicable" in RT or "pass \| blocked \| advisory \| not_applicable" in RT` | same — report-template.md:223 or :315 must retain one of the two exact 4-token forms as a substring (append-at-end keeps it). |
| `tests/troubleshoot/test_hardening_verdict.py:66-67` | `for n in range(1, 8): assert f"\| {n} \|" in OC` — 7 rows | still passes if an 8th row is ADDED (`\| 8 \|` is not asserted); passes if rows are renumbered as long as 1-7 all exist. |
| `tests/troubleshoot/test_hardening_verdict.py:71` | `OC.count("\`blocked\`") >= 3` | a `\`blocked-on-authorization\`` backtick token does **not** match `` `blocked` `` (trailing backtick), so count is unaffected either way. |
| `tests/troubleshoot/test_hardening_verdict.py:83` | `OC.count("\| No \|") >= 7` | a new row must also carry `\| No \|` in the Downstream-Override column to keep the "every row No" invariant meaningful (>=7 still passes regardless). |
| `tests/troubleshoot/test_hardening_verdict.py:29` | `"{blocked, advisory}" in OC` | if R-16 makes the latch force `{blocked, blocked-on-authorization, advisory}` and rewrites that literal, this breaks. Keep the `{blocked, advisory}` literal or update test. |
| `tests/troubleshoot/test_hardening_verdict.py:36-39` | 4 H5 mapping rows verbatim | unaffected unless the H5 table is touched. |
| `tests/troubleshoot/test_hardening_output_contract.py:78,82` | `"advisory\` even if \`pipeline_hardening_verdict=pass\`"`, `"May mirror \`pipeline_hardening_verdict\`"` | backtest-status table rows — unaffected by R-16. |
| `tests/troubleshoot/backtest/test_waiver_regreen.py:36-48` | lowercase loose (`waiver_status`, `latch`, `blocked`, `advisory`, `success_with_hardening_*`) | unaffected. |

**Note on the four-token language:** `hardening-output-contract.md:5`, `report-template.md:315`, `pipeline-hardening-closure.md:13` and `test_hardening_output_contract.py:87,95` / `test_hardening_verdict.py:50` all describe a "FOUR-token" / "4-token" enum. R-16 makes it five; the prose "four-token" must be updated in those three refs (tests only assert the substring, not the word "four", so prose drift is cosmetic but misleading).

## 4. Callers of `/sc:troubleshoot` / `sc-troubleshoot-protocol` and the return-contract fields they consume (R-01 `execution_locus_card_path`, R-18 on-return list)

Grep: `rg -l -e 'sc:troubleshoot' -e 'sc-troubleshoot-protocol' -e 'troubleshoot\.md' src tests docs` minus the skill dir and `tests/troubleshoot/` → 55 files; only the ones below actually **consume** something. The rest are mentions (help.md, docs listings, swarm lens name `troubleshoot-hypothesis`, research docs).

### 4a. Real callers and consumed fields

| Caller | file:line | Invocation | Return-contract fields consumed | Impact of R-01 / R-18 |
|---|---|---|---|---|
| **sc-task-protocol (TFEP)** | `src/superclaude/skills/sc-task-protocol/SKILL.md:217` | `/sc:troubleshoot --caller task-unified --context … --output-dir … --depth …` (no `--fix`) | `:221` reads `{output_dir}/return-contract.yaml`: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`; `:262` `report_path`, `audit_log_path` | **None** — it reads named fields only; an additive `execution_locus_card_path` is ignored. Does not read `hypothesis_cards`, `diagnosability_*`, or hardening fields. |
| **sc-pr-submit-protocol (C3b)** | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:93`; `refs/troubleshoot-dispatch.md:1-49`; `refs/state-machine.md:28,81`; `refs/severity-routing.md:48-55`; `refs/finding-verify.md:4,21,36` | `> Skill sc:troubleshoot-protocol` with `--fix` / `--depth deep --fix`, `--scope`, `--type` | **No return-contract fields consumed** (it "treats troubleshoot as a black box", `troubleshoot-dispatch.md:4-6`; it owns edit application itself, `:44-49`). Consumes the **flag surface** (`--depth`, `--fix`, `--scope`, `--type`, quick+fix conflict) and the `evidence-validator` agent (`finding-verify.md:36`). | **None** unless flags are removed/renamed. |
| `src/superclaude/pr_submit/fsm.py:358-365` | `seed_troubleshoot(finding)` builds the invocation seed dict (`--scope`, `--type`, depth) | none | none |
| **commands/troubleshoot.md** (the thin command) | `src/superclaude/commands/troubleshoot.md:60,69` | `:69` "On skill return, surface: REPORT path, tier reached, confidence, chosen fix, (if `--fix`) the Tier 3 remediation offer, (if `pipeline_hardening_applicable`) the Pipeline Hardening Closure verdict + evidence-card paths, (if `caller=task-unified`) the emitted `return-contract.yaml` path." | this IS the R-18 on-return list; nothing else reads it | R-18 edits `:69`; no downstream consumer of that sentence. |
| **sc-reflect-protocol** (reverse direction) | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:976` | troubleshoot Wave 6 (Phase B/D) *invokes reflect*; reflect lists troubleshoot as a consumer of reflect's `status`, `tier_reached`, `confidence_calibrated`, `regression_present`, `needs_human_decision` | reflect does not read troubleshoot's contract | none |
| task-builder | `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md:35,69-71` (BUILD_REQUEST carries `pipeline_hardening_verdict`, `waiver_status`) | troubleshoot → task-builder handoff | task-builder receives the BUILD_REQUEST prose; `rg pipeline_hardening_verdict src/superclaude/skills/task-builder` → zero hits, so task-builder does not parse those fields | R-16 new token flows through as prose only |

`src/superclaude/commands/task-unified.md` does **not exist** (`rg` error: No such file); the TFEP caller is `sc-task-protocol/SKILL.md`. `sc-bare-review/SKILL.md:21` and `sc-recommend/refs/delegation-vs-native-heuristics.md:40` only name `/sc:troubleshoot` in a list.

### 4b. Line-number citations INTO the troubleshoot skill from sc-pr-submit-protocol (already stale; will drift further)

| Citing file:line | Cites | What is actually there now |
|---|---|---|
| `sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:7` | `sc-troubleshoot-protocol/SKILL.md:103` (flag surface) | `SKILL.md:103` = "Wave 4: Tier 2 — Adversarial Fix Debate" |
| `troubleshoot-dispatch.md:18` | `SKILL.md:104-111` (auto-detect) | `:104` = Wave 4.5 line; `:111` blank |
| `troubleshoot-dispatch.md:29`, `severity-routing.md:48` | `SKILL.md:131` (quick+fix conflict) | `:131` = "Open audit log; emit machine-readable header" |
| `troubleshoot-dispatch.md:46` | `SKILL.md:445-448`, `refs/remediation-handoff.md:78-92` | `:445` blank; `remediation-handoff.md:78-92` = template-selection bullets + Phase B (roughly still on topic) |
| `finding-verify.md:21` | `SKILL.md:24` (drop-not-downgrade) | `:24` = "Hallucination contract" — still on topic |
| `finding-verify.md:36` | `SKILL.md:409` (evidence-validator spawn) | `:409` blank |
| `severity-routing.md:53`, `troubleshoot-dispatch.md:22` | `escalation-rubric.md:60-61` | still correct today (`:60` "Forced escalation", `:61` `--depth deep` → ESCALATE) |

These are **pre-existing drift** (no test reads them). Out of scope to fix; listed so the builder knows R-xx line insertions will not newly break anything.

### 4c. Non-troubleshoot tests that READ the target files (content gates outside `tests/troubleshoot/`)

| Test | Reads | Asserts | Risk from R-01..R-19 |
|---|---|---|---|
| `tests/skills/test_tier2_tavily_consistency.py:15-16,28-34` | `commands/troubleshoot.md`, `sc-troubleshoot-protocol/SKILL.md` | `mcp__tavily__tavily_search` present; `tavily-extract`/`tavily-map`/`tavily-crawl` absent | keep those strings in both files |
| same `:56-60` | `SKILL.md` | regex `≤2\|at most 2 quer\|2 queries` (Tier-2 rate cap) | keep |
| same `:63-68` | `SKILL.md` | `fail-open` / `fail open` / `degrad` (lowercase) | keep |
| same `:73-76` | `SKILL.md` | `search_depth: advanced` | keep |
| `tests/agents/test_tavily_tool_parity.py:24-34,47-80` | **every** `*.md` under `src/superclaude/agents/` and `src/superclaude/skills/` (rglob) | for files whose frontmatter has `tools:`/`allowed-tools:`, body `mcp__tavily__tavily_*` ids must equal declared set | new `refs/primitive-differential.md` and edited agents are scanned. Refs have no frontmatter → skipped. Agents (`confidence-calibrator.md`, `evidence-validator.md`) DO have frontmatter — if R-14 adds prose mentioning a `mcp__tavily__*` tool it must also be declared in `tools:`. |
| `tests/pr_submit/test_finding_verify.py:8` | mocks the evidence-validator spawn | does not read the agent file | none |

**External consumer count for item 4: 2 real callers** (sc-task-protocol, sc-pr-submit-protocol) + 1 command wrapper + 2 out-of-dir test modules that content-gate `SKILL.md`/`troubleshoot.md`.

## 5. Other spawners of `confidence-calibrator` / `evidence-validator` (R-14 new inputs `card_mtime`, `calibration_paths`, `diff_path`, `artifact_paths`)

### 5a. Current declared input contracts (what callers rely on today)

- `src/superclaude/agents/confidence-calibrator.md:46-50` — Inputs: `card_path`, `rubric_path` (→ `refs/escalation-rubric.md`), `card_tier`, `flags_context`, `output_path`. Step 2a (`:56`) already documents a **default-on-absent** pattern for frontmatter fields ("If `claim_class` is absent, default to `runtime_behavior` … Record all defaults in Notes (preserves backward-compat with v1.0 cards)") — the precedent to follow for new optional inputs.
- `src/superclaude/agents/evidence-validator.md:37-44` — Inputs: `report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec` (default `false`). Output Format headers at `:64-92`: `**Dropped**: <N>`, `**Suggested report status**: <success | partial>`, `## Dropped citations`, verdict tokens `verified` / `line-mismatch` / `file-missing` / `snippet-mismatch` (`:53`).

### 5b. Spawners outside sc-troubleshoot-protocol

| Spawner | file:line | Agent | Inputs it passes | Outputs it consumes | What breaks if R-14 inputs become REQUIRED |
|---|---|---|---|---|---|
| **sc-reflect-protocol** Waves 1D, 3C | `SKILL.md:158,163,624,1221`; `refs/reflection-rubric.md:136` | `confidence-calibrator` | No explicit arg list in the skill; §11.3 says "The card itself is its only input"; uses the **5-dim reflection rubric** (not troubleshoot's 6-dim escalation rubric) | calibrated confidence; `calibration: inline-fallback` marker on failure (`SKILL.md:1447`) | reflect does not pass `card_mtime` / `calibration_paths`. If the agent STOPs or errors on their absence, reflect degrades to inline fallback (`SKILL.md:392,1447`) — functional but silently downgrades every reflect run. **Inputs must be optional with documented defaults.** |
| **sc-reflect-protocol** Wave 5 | `SKILL.md:628,677,1208`; `refs/input-resolution.md:22` | `evidence-validator` | not enumerated in skill prose; relies on the agent's declared 4 inputs | drop count → `citations_dropped`, `status: partial` forcing (`SKILL.md:1524`, `refs/report-template.md:37`) | does not pass `diff_path` / `artifact_paths`. If required → inline fallback + forced `status: partial` (`SKILL.md:1448`). **Must be optional.** |
| **sc-pr-submit-protocol** Wave 3 (C3a) | `SKILL.md:92`; `refs/finding-verify.md:6,36-38`; `refs/auggie-fallback.md:55` | `evidence-validator` | `allow_command_reexec=false` explicitly; report draft = finding list | `verified` / `unverified` per finding | does not pass new inputs. Same requirement: optional. |
| **sc-cli-eval-protocol** create W6 (optional) | `SKILL.md:111,180`; `refs/create-pipeline.md:58`; `refs/integration-map.md:57-59` | `evidence-validator` | unspecified | cite resolution | optional path; same. |
| **eval suite `agent_grounding_drift.yaml`** (nightly meta-eval, not pytest) | `src/superclaude/cli/eval/suites/agent_grounding_drift.yaml:96-100,155-159` | `evidence-validator` | **exactly** `report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec: false` | `:107` `contains: "Dropped**: 0"`, `:111` `"Suggested report status"`, `:166` `"file-missing"`, `:170` `"partial"`, `:174` `"## Dropped citations"` | (1) if new inputs are required the spawn fails; (2) if R-14 renames any of those **output headers/verdict tokens** the suite's `contains:` expectations fail. Keep `**Dropped**:`, `**Suggested report status**:`, `## Dropped citations`, `file-missing`, `partial` verbatim. Comment at `:11,14,22-23` cites `evidence-validator.md:48,55,128` and `confidence-calibrator.md:49,118` line numbers (will drift; cosmetic). |
| `pr_submit/fsm.py:700` | Python | evidence-validator | injected/mocked; core never shells out | none | none |
| `tests/pr_submit/test_finding_verify.py:8` | pytest | mocks the spawn | — | — | none |
| `agents/reuse-auditor.md:185`, `agents/reflect-reviewer.md:138` | prose mentions only | — | — | — | none |

`root-cause-analyst` is also spawned by sc-reflect Wave 1C (`SKILL.md:157,621,1449`) with a `deviation_class` field expectation; only prose mentions elsewhere (`docs/user-guide/agents.md`, `commands/reflect.md:135,166`). If R-xx edits `root-cause-analyst.md` inputs, the same optional-with-default rule applies.

**Conclusion for R-14:** every external spawner passes only the currently-declared inputs (or none explicitly). New inputs `card_mtime`, `calibration_paths`, `diff_path`, `artifact_paths` **must be optional** with the absence behaviour documented in the agent (mirror `confidence-calibrator.md:56` "if absent, default … record in Notes"). The eval suite pins evidence-validator's output-format tokens.

**External spawner count for item 5: 4 skills** (sc-reflect-protocol, sc-pr-submit-protocol, sc-cli-eval-protocol, + commands/reflect.md wrapper) **+ 1 eval suite** with hard `contains:` expectations.

## 6. Makefile `sync-dev` / `verify-sync` mechanics

### 6a. What `sync-dev` copies (`Makefile:109-163`)

| Source | Target | Mechanism | Line |
|---|---|---|---|
| `src/superclaude/skills/<name>/**` (every file; skips `__*` dirs, `__init__.py`, `__pycache__`) — only dirs with `SKILL.md`/`skill.md` | `.claude/skills/<name>/<same rel path>` | `find … -exec cp`, preserves subdirs (so `refs/primitive-differential.md` is copied automatically) | `:112-125` |
| `src/superclaude/agents/*.md` (skips `README.md`) | `.claude/agents/<name>` | flat `cp` | `:126-130` |
| `src/superclaude/commands/*.md` (skips `README.md`, `__init__.py`) | `.claude/commands/sc/<name>` | flat `cp` | `:131-136` |
| `src/superclaude/hooks/scripts/*.sh`, `src/superclaude/scripts/session-init.sh` | `.claude/hooks/` | `cp` + `chmod +x` | `:137-147` |
| `src/superclaude/templates/**` (skips `agent-memory/`, `__pycache__`) | `.claude/templates/<rel>` | `find … cp` | `:148-157` |

`sync-dev` is **copy-only**; it never deletes stale files in `.claude/`. A ref deleted/renamed in src leaves an orphan in `.claude/skills/<name>/refs/`.

### 6b. Does `verify-sync` fail on extra / missing files? (`Makefile:166-352`)

- **Skills** (`:171-200`): `diff -rq --exclude='__init__.py' --exclude='__pycache__' src/…/<name> .claude/skills/<name>` (`:178`). `diff -rq` reports **"Only in"** lines for files present on only one side, so drift=1 for BOTH (a) a new ref existing only in `src/` before sync (`Only in src/…/refs: primitive-differential.md`) and (b) an orphan existing only in `.claude/` after a src-side delete. Also fails if a `.claude/skills/<name>` has no `src/` counterpart (`:188-200`).
- **Agents** (`:203-226`): per-file `diff -q` + reverse pass → MISSING/DIFFERS either direction → drift=1.
- **Commands** (`:229-252`): same shape, both directions.
- **Hooks / Templates / Installer Registration / Hooks Cross-Consistency** (`:255-347`): both directions.
- Exit: `:348-352` — `exit 1` if `drift != 0`.

**Answer:** yes — `verify-sync` fails on extra files in `.claude/` AND on files present only in `src/`. The new `refs/primitive-differential.md` must be followed by `make sync-dev` before `make verify-sync` passes. Since `sync-dev` never deletes, any ref the spec *removes* from src would need a manual `rm` under `.claude/skills/sc-troubleshoot-protocol/refs/` (the brief lists no deletions, so N/A).

### 6c. Does the pre-commit hook run `verify-sync`?

**No.** `.pre-commit-config.yaml:100-113` runs `scripts/precommit_block_claude_mirrors.sh` (rejects staged `.claude/{skills,agents,commands,hooks,templates}/` paths, AC11) and `:115-128` a narrowed bare-review parity check (`files: '^src/superclaude/skills/sc-bare-review/'` only). The comment at `:101-103,116-118` states full drift checking is delegated to CI: `.github/workflows/quick-check.yml:47-53` runs `make sync-dev` then `make verify-sync` (`test.yml:52,103` also `make sync-dev`). `git config core.hooksPath` is unset and `.git/hooks/` holds only `.sample` files — no native hook. `tests/cli/test_verify_sync_hooks.py` exercises only the Hooks/Installer sections via subprocess, not the skills section.

Practical consequence: the builder must run `make sync-dev` locally after editing (Claude Code reads `.claude/` at runtime — `CLAUDE.md` "Component Sync"), must NOT stage `.claude/**` (pre-commit blocks it), and CI regenerates the mirror itself so a stale local mirror cannot fail CI.

## 7. docs/ pages describing `/sc:troubleshoot` internals (list only; no fix needed)

Grep: `rg -n -i -e 'Wave 1\.6' -e 'Wave 1\.5' -e 'Wave 4\.5' -e 'diagnosab' -e 'hypothesis card' -e 'confidence-calibrator' -e 'return-contract' docs`.

**No `docs/` page describes the troubleshoot wave structure (Wave 1.5/1.6/4.5, diagnosability, Tier-1 hypothesis card, hardening gates).** Every docs hit for those tokens belongs to other subsystems (reflect CLI guide, swarm, sprint, git standards). What docs DO say about `/sc:troubleshoot` is already a stale legacy surface, unaffected by R-01..R-19:

| Page:line | Content | Status |
|---|---|---|
| `docs/user-guide/commands.md:573-597` | "`/sc:troubleshoot [issue] [--type bug\|build\|performance\|deployment] [--trace] [--fix]`" + 4 bullet feature list | pre-existing stale (no `--depth`, `--scope`, `--caller`, waves); unchanged by this track |
| `docs/user-guide/commands.md:1020,1027` | reflect legacy grammar "preserved for `/sc:troubleshoot` Wave 6" | mentions Wave 6 only (remediation → reflect); R-18 does not touch Wave 6 |
| `docs/user-guide/flags.md:106-112` | Troubleshoot flag table: `--type`, `--trace`, `--fix` | pre-existing stale |
| `docs/user-guide/flags.md:161` | same Wave 6 legacy-grammar note | as above |
| `docs/user-guide/agents.md:457-463,825,838` | root-cause-analyst description; `/sc:troubleshoot` → root-cause-analyst | generic; no wave detail |
| `docs/eval/suites-guide.md:388-409` | `agent_grounding_drift` suite description; cadence "on edits to `.claude/agents/evidence-validator.md` or `.claude/agents/confidence-calibrator.md`" | **goes stale in spirit**: R-14 edits those agents, so per this page the nightly suite should be re-run after the change (see §5b eval-suite `contains:` pins) |
| `docs/reference/basic-examples.md:68-79,391-422`; `docs/reference/examples-cookbook.md`; `docs/reference/advanced-workflows.md`; `docs/reference/integration-patterns.md:256` | usage examples only | no wave detail |
| `docs/developer-guide/technical-architecture.md:58` | file tree listing `root-cause-analyst.md` | none |
| `docs/generated/cleanup-sc-prefix-reference-index.md:119,166` | path index | none |
| `tests/troubleshoot/e2e-backtest-scenarios.md` (not docs/, but documentation) | E1-E5 scenarios naming H1-H4 gates (`:12` "against H1 (Runtime-Entrypoint Verification)") | goes stale under R-17 label rename; not pytest-collected (`:5`) |

---

## Status: Complete

### Summary

- **Item 1 (ref filenames):** 4 non-test external consumers (`commands/troubleshoot.md:163`, `sc-pr-submit-protocol/refs/severity-routing.md:53`, `sc-pr-submit-protocol/refs/troubleshoot-dispatch.md:22`, `confidence-check/SKILL.md:20`) — all prose pointers, none break. 7 test modules under `tests/troubleshoot/` read `hardening-output-contract.md`, `report-template.md`, `runtime-entrypoint-verification.md` by exact tokens. `primitive-differential.md`: zero references anywhere. `report-template.md` hits in sc-reflect / sc-crash-recovery are different files with the same basename.
- **Item 2 (H0-H5 → HC0-HC5):** `HC[0-5]` is unused. Hardening-gate `H[0-5]` vocabulary exists ONLY in the skill dir + `tests/troubleshoot/`; all other repo hits are markdown heading levels / unrelated IDs. `calibrator-eval-cases.md:49,54` and `escalation-rubric.md:35` use H1/H2/H3 as HYPOTHESIS labels — keep. **One hard test break:** `tests/troubleshoot/test_hardening_h1.py:46` asserts `"satisfy h1"` in `runtime-entrypoint-verification.md:28`. Backtest `wave` fields are free strings, self-contained.
- **Item 3 (verdict enum, R-16):** zero external consumers. `blocked_pending` does not exist anywhere. Enum literal is pinned by `test_hardening_verdict.py:51` and `test_hardening_output_contract.py:92-95` as the exact substring `pass | blocked | advisory | not_applicable` — append the new token at the END or keep the 4-token substring intact; also `{blocked, advisory}` literal at `test_hardening_verdict.py:29`. 10 in-skill sites list the enum (§3a); "four-token" prose in 3 refs needs updating.
- **Item 4 (callers):** 2 real callers — `sc-task-protocol/SKILL.md:217-262` (reads named fields only; additive `execution_locus_card_path` is safe) and `sc-pr-submit-protocol` (black-box, flag surface + evidence-validator only). `commands/troubleshoot.md:69` is the only on-return list (R-18). `commands/task-unified.md` does not exist. sc-pr-submit's `SKILL.md:103/104-111/131/409/445-448` line citations are already stale. Out-of-dir content gates: `tests/skills/test_tier2_tavily_consistency.py` (SKILL.md + troubleshoot.md tokens) and `tests/agents/test_tavily_tool_parity.py` (rglob over all agents/skills .md, incl. the new ref).
- **Item 5 (agents):** 4 external spawners (sc-reflect-protocol W1D/3C/5, sc-pr-submit-protocol W3, sc-cli-eval-protocol W6, `commands/reflect.md`) + nightly eval suite `cli/eval/suites/agent_grounding_drift.yaml:96-100,155-159` which spawns evidence-validator with exactly the 4 current inputs and pins output tokens `**Dropped**:`, `**Suggested report status**`, `## Dropped citations`, `file-missing`, `partial`. R-14 inputs MUST be optional with defaults (precedent: `confidence-calibrator.md:56`).
- **Item 6 (Makefile):** `sync-dev` (`:109-163`) copies skills recursively (new ref auto-included), agents/commands flat; never deletes. `verify-sync` (`:166-352`) uses `diff -rq` → fails on files present on only ONE side (src-only new ref before sync, or `.claude/`-only orphan). Pre-commit does NOT run verify-sync (only blocks staging `.claude/` mirrors, `.pre-commit-config.yaml:100-113`); CI does (`quick-check.yml:47-53`).
- **Item 7 (docs):** no docs page describes troubleshoot waves; `docs/user-guide/commands.md:573-597` and `flags.md:106-112` are pre-existing stale legacy flag docs. `docs/eval/suites-guide.md:408-409` says re-run the grounding suite when the two agents change.

**Total distinct external consumers found: 11** (4 ref-pointer files + 2 callers + 1 command wrapper + 4 agent spawners/suites) **+ 9 test modules** that content-gate target files (7 in `tests/troubleshoot/`, `tests/skills/test_tier2_tavily_consistency.py`, `tests/agents/test_tavily_tool_parity.py`).
