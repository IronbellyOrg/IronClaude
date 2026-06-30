# Research Completeness Verification — sc:submit-pr Track 1

**Topic:** Build MDTM task file for `sc:submit-pr` PR review auto-remediation skill
**Date:** 2026-06-11
**Lens:** completeness (BREADTH)
**Files in scope:** 01-component-inventory.md, 02-skill-command-hook-conventions.md, 03-reuse-surfaces.md, 04-test-infra-and-deterministic-core.md, 05-integration-points.md, 06-detection-probe-and-gh-surface.md, 07-mdtm-template-and-examples.md
**Spec:** merged-spec.md (C1–C6, FR-1..7, NFR-1..8, INV-001/007/009/015/016, §3 build DAG, §6.3 21-file test layout)

---

## Status: COMPLETE — VERDICT: PASS (0 critical gaps, 2 minor, 1 cosmetic)

---

## Preliminary: file-completeness scan

| File | Top status | Bottom status | Has Summary | Evidence-cited (file:line) | Note |
|------|-----------|---------------|-------------|----------------------------|------|
| 01-component-inventory.md | Complete | Complete | Yes | Yes (heavy) | Clean |
| 02-skill-command-hook-conventions.md | **In Progress** | Complete | Yes | Yes (heavy) | Stale top marker (minor) |
| 03-reuse-surfaces.md | Complete | Complete | Yes | Yes (heavy) | Clean |
| 04-test-infra-and-deterministic-core.md | Complete | Complete | Yes | Yes (heavy) | Clean |
| 05-integration-points.md | **In Progress** | Complete | Yes | Yes (heavy) | Stale top marker (minor) |
| 06-detection-probe-and-gh-surface.md | Complete | Complete | Yes | Yes (heavy) | Clean |
| 07-mdtm-template-and-examples.md | **In Progress** | Complete | Yes | Yes (heavy) | Stale top marker (minor) |

All 7 files end with "Status: Complete" and a Summary. R2/R5/R7 carry a stale "In Progress" header at line ~3 that was never flipped — a cosmetic inconsistency (Completeness check #4), not a content gap. Every file is evidence-dense with file:line citations. No fabrication detected; claims are grounded in real repo paths or the spec.

---

## Lens checks (10) — PASS/FAIL with evidence

### Check 1 — All C1–C6 component files identified with exists/new status + paths? **PASS**

R1 (01-component-inventory.md) delivers an exhaustive per-component table. Every spec §2 path is mapped:
- C1: `SKILL.md` (NEW) + `refs/state-machine.md` (NEW, core-pure) + `commands/submit-pr.md` (NEW) — rows 1-3, 12.
- DET: `refs/detection-contract.md` (NEW, R1-gated) — row 4, flagged as hard build gate.
- C2: `refs/augment-poll.md` + `scripts/poll-augment-review.sh` (NEW) — rows 5, 10.
- C3/C3a/C3b: `severity-routing.md` / `finding-verify.md` / `troubleshoot-dispatch.md` (NEW) — per-component blocks 7/8/9.
- C4: `refs/thread-reply.md` + `scripts/reply-resolve-thread.sh` (NEW) — rows 8, 11.
- LG: `refs/loop-guard.md` (NEW, core-pure) — row 9.
- C5: `hooks/scripts/offer-pr-review.sh` (EDIT, exists 74 lines/3409B, exec) — row 13, with exact structural anchors (lines 49-58 INVOKE_HINT, 60-72 heredoc).
- C6: `tests/submit_pr/` (NEW, 22 modules + 18 fixtures + conftest/init) — row 15.
- Reuse: `severity-rubric.md` (REUSE, exists 172 lines/10768B) — row 14.

Existence gate verified live: skill dir / command / test dir ABSENT; hook + rubric EXIST. Status accurate. Granular enough for one checklist item per row (the summary table explicitly says "builder → one checklist item per row"). **No gap.**

### Check 2 — Reuse surfaces (severity-rubric, grounding, troubleshoot dispatch) concretely characterized? **PASS**

R3 (03-reuse-surfaces.md) is the strongest reuse characterization:
- **Severity rubric (C3):** exact file `severity-rubric.md` (173 lines), the 5-tier defs (lines 12-61), the 5-step remap algorithm (63-101), category floor/ceiling table (70-87), decision-mode map (163-172). Maps T-301/T-302 to specific rubric rows. Crisp boundary: "rubric = grade; C3 = grade→tier→route" — routing is NEW, not in the rubric.
- **Grounding (C3a):** hallucination contract (`auggie-review SKILL.md:22`), Wave-3 file:line validation pass (`:206-209`), independent-pass cross-check (`:183/215`). Concrete reuse recommendation: **spawn the existing `evidence-validator` agent** (`troubleshoot SKILL.md:409`) rather than author a new verifier. Distinguishes structural-drop (EC-9) from false-positive demote (FR-3.5 delta).
- **Troubleshoot dispatch (C3b):** real flag surface (`troubleshoot SKILL.md:103`), scope-seed contract (`:31/:112/:144`), and a **load-bearing builder warning**: `--depth quick + --fix` is a STOP/conflict (`:131`), so Medium→`--fix` (defaults standard), High/Critical→`--depth deep --fix`, never `--depth quick --fix`. This corrects a latent spec hazard. **No gap.**

### Check 3 — Test architecture resolved (Python core location, --cov path, 21 test files mapped)? **PASS (with a surfaced spec defect, correctly flagged not assumed)**

R4 (04-test-infra-and-deterministic-core.md) resolves the pivotal architecture question decisively:
- **Python core location:** `src/superclaude/submit_pr/` (underscored sibling pkg), NOT the hyphenated skill dir. Justified: hyphen is not a legal Python identifier (verified live: `import superclaude.skills.confidence_check` → ImportError on the `confidence-check` hyphen dir). Mirrors the existing `sc-bare-review` skill ↔ `superclaude.cli.swarm` pkg split. 7-module layout given (fsm/severity/loop_guard/classifier/detection/models/run_log).
- **--cov defect:** spec line 1025 `--cov=superclaude.skills.sc-submit-pr-protocol` is unresolvable (hyphens; coverage only instruments `.py`). Corrected to `--cov=superclaude.submit_pr`. This is a real spec defect surfaced for the builder, not silently assumed away (Check 10 satisfied here too).
- **21 test files mapped:** §C table maps every spec §6.3 test file → primary module(s) + test pattern (1 / 1+mock / 3a / 3b). `run_skill()` driver located in `fsm.py`; free functions re-exported at package top-level.
Evidence is grounded in real test precedents (cli_portify, recommend, swarm parity, hooks). **No gap.**

### Check 4 — Marker + coverage registration covered? **PASS**

R4 §E + §F:
- **Markers:** `pyproject.toml:107-110` sets `--strict-markers`; current registered markers enumerated (`:114-139`). The 5 spec markers `loop_guard`, `autonomy`, `recovery`, `p0`, `loop` are NONE registered → MUST be added to `[tool.pytest.ini_options] markers`, with the exact TOML lines provided. Confirmed pyproject is the single marker registry (no pytest.ini/setup.cfg/pytest_configure). This is a concrete, actionable build item.
- **Coverage:** `[tool.coverage.run] source = ["src/superclaude"]` (`:142-148`) auto-covers the new pkg; `pytest-cov>=4.0.0` declared in dev/test extras; coverage only instruments `.py`. Banned-import landmine flagged (§G: `import anthropic` is ruff-banned repo-wide — the core must not import the SDK). **No gap.**

### Check 5 — DET probe operationality + task-encoding resolved? **PASS (excellent)**

R6 (06-detection-probe-and-gh-surface.md) §1:
- **Operationality:** the probe is 5 concrete `gh`/`gh api` captures (bot login+association+`[bot]` suffix via `pulls/<N>/reviews`; emission_shape/findings_locus across reviews vs `pulls/<N>/comments` vs `issues/<N>/comments` vs `commits/<sha>/check-runs`; severity_field_path; review_completeness_signal; persist probe_evidence). Each command single-line, `--repo`-pinned, absolute-path (NFR-5).
- **Can it run NOW? NO** — verified: zero captured Augment GitHub-App review JSON anywhere in `.dev/` (`find .dev -iname '*augment*'` → empty); the in-repo `/sc:auggie-review` is a *different* thing (in-session retrieval, not the GitHub App). No `upstream` remote.
- **Task-encoding:** encode as a `needs_human_decision` build-step-0 item that writes PENDING + HALTs, NEVER auto-locks — explicitly citing the `feedback_human_decision_items_must_halt` memory and §7 "NOT hard-guessed". Acceptance = `locked: true` + real `probe_evidence`; `grep -q '^locked: true'` programmatic check; T-210 mechanical enforcement; synthetic fixtures (§18.4) unblock everything else, post-probe schema-parity test regenerates from real data. This is exactly the granularity and HALT-discipline the builder needs. **No gap.**

### Check 6 — gh poll/reply/resolve API surfaces documented? **PASS (excellent)**

R6 §2:
- **Poll (FR-2.1):** exact `gh pr view <N> --json number,url,headRefName,headRefOid,baseRefName,reviews,comments` + REST `pulls/<N>/reviews` + `pulls/<N>/comments` (+ `commits/<sha>/check-runs` if check_run shape). Notes `headRefOid` = head SHA for INV-001 attribution. Backoff arithmetic kept in FSM, not the script (NFR-6 purity).
- **Reply (FR-6.1):** CONFIRMED against GitHub REST docs — `POST .../pulls/<N>/comments/<COMMENT_ID>/replies -f body=...`; comment_id MUST be top-level ("replies to replies not supported"); conversation summary via `issues/<N>/comments`. Reply must cite `applied_edits` status (T-603).
- **Resolve (FR-6.2):** GraphQL-ONLY — no native `gh pr` verb (gh 2.45.0, cli/cli#12419 unimplemented). Two `gh api graphql` calls: query `reviewThreads.nodes{id,isResolved,path,line}` to get the thread node id (REST ids ≠ GraphQL thread ids), then `resolveReviewThread(input:{threadId})`. Permissions caveat (needs PR read+write; map 403 to HALT). Idempotency skip if `isResolved:true`. Reply-then-resolve ordering. In-repo prior art cited (`auggie-review SKILL.md:304-314`). **No gap.**

### Check 7 — MDTM template rules (A3/A4/B2/M3/M4/I19-22) + exemplars documented? **PASS**

R7 (07-mdtm-template-and-examples.md):
- **Rules with IDs + line cites:** A3 (`:108-112`), A4 (`:114-133`), A5 (`:135-139`), B1-B5 (`:151-182`), L1-L7 (`:928-1026`), M1 (DEPRECATED `:1034`), M2 (`:1047`), M3 8-step (`:1059-1096`), M4 (`:1098-1121`), I19 floors-by-size (`:699-743`), I20 serialized fix (`:745-757`), I21 fidelity applicability (`:759-788`), I22 intensity levels (`:793-840`), F/C prohibitions. All requested IDs (A3/A4/B2/M3/M4/I19-22) covered, plus more.
- **PART 2 emitted structure:** frontmatter (incl. `reflect_pre`/`reflect_post`/`start_commit`), mandatory `## Execution Context` 5 sub-sections, phase-body conventions, `## Post-Completion Actions` ordering, Task Log Findings sinks.
- **Exemplars:** TWO — Exemplar A (prd-local-file, FINAL_ONLY lite + the load-bearing POST `/sc:reflect` HALT-gate paragraph) and Exemplar B (troubleshoot-hardening, full M3 8-agent + M4 + penultimate working-tree-diff reflect gate). Both with absolute paths and specific line cites. **No gap.**

### Check 8 — Build-order DAG (DET-first) reflected? **PASS**

R7 §4 gives a concrete phase structure that encodes the §3 DAG as a **mechanical L5 contract-verdict gate**, not prose: Phase 2 builds DET first → L3 contract-proof test → L5 conditional gate that withholds Phase 3+ authorization until contract tests PASS. R1 (row 4 / flag 3) and R6 (§1.3) independently reinforce DET as the step-0 hard gate. The DET-first ordering is consistently represented across R1, R6, R7. R6 also notes synthetic fixtures (§18.4) unblock the internal-pure steps 2-5 in parallel with the still-pending probe. **No gap.**

### Check 9 — Granularity sufficient for per-file checklist items? **PASS**

R1's summary table is explicitly "builder → one checklist item per row" (15 rows + a 21-file test breakdown). R4 maps all 21 test files → modules. R3 gives per-ref DEFER-TO contracts. R6 gives per-surface exact command shapes. R7 gives the per-item B2 six-element structure and the EXPLICIT ENUMERATED COMPLETION GATE pattern. Every component, test file, gh surface, and reuse ref is decomposed to an actionable unit. **No gap.**

### Check 10 — Open ambiguities (R1 probe + others) flagged, not silently assumed? **PASS (strong)**

Ambiguities are surfaced, not buried:
- **R1 probe** (R6 §1.2/1.3): cannot run now, encode as HALT/PENDING — explicitly NOT auto-assumed.
- **--cov hyphen defect** (R4 §LEAD + #2): flagged as a spec defect for the builder, with the fix.
- **Markers unregistered** (R4 §E): flagged with exact TOML to add.
- **Troubleshoot won't auto-apply edits** (R5 §6.2 / §2.3): flagged as "the single biggest wiring seam" — `sc:submit-pr` must own edit application at L2/L3 since troubleshoot Tier-3 stops at an MDTM file.
- **Monitor-tool ≠ daemon** (R5 §1.2/§6.1): honest framing preserved; session-close = monitor lost; durability is `--resume`+JSONL, not the tool.
- **hooks sync uncertainty** (R2 §7.2): R2 flagged it as unresolved (did not read the Makefile); **R5 §3.2 resolves** the skills/agents/commands sync (Makefile:112-135) but the specific `hooks/scripts/` → `.claude/hooks/` flattening question is only partially closed — see Minor Gap 2 below.
**No critical ambiguity is silently assumed.**

---

## Cross-cutting coverage audit (spec scope → research)

| Spec area | Covered by | Status |
|-----------|-----------|--------|
| C1 FSM/orchestrator | R1, R4 (fsm.py), R7 (phase struct) | COVERED |
| C2 poller | R1, R6 (§2.1 poll surface), R4 (detection.py) | COVERED |
| DET contract | R1 (row 4), R6 (§1 probe) | COVERED |
| C3 severity router | R1, R3 (rubric reuse), R4 (severity.py) | COVERED |
| C3a verify-before-remediate | R1, R3 (§2 grounding), R4 (classifier) | COVERED |
| C3b troubleshoot dispatch | R1, R3 (§3 flags), R5 (§2 runtime invocation) | COVERED |
| C4 reply/resolve | R1, R6 (§2.2/2.3 REST+GraphQL) | COVERED |
| LG loop-guard (INV-001) | R1, R4 (loop_guard.py) | COVERED |
| VAL validation gates §10 | R5 (§4 gh/git), partially R4 | COVERED (see Minor Gap 1) |
| C5 hook edit | R1 (anchors), R2 (§5 conventions), R6 (§3.1 test) | COVERED |
| C6 tests (21 files + 18 fixtures) | R1, R4 (§C mapping) | COVERED |
| FR-1..7 | R3/R5/R6 (per-FR surfaces) | COVERED |
| NFR-6 core purity | R1, R4, R5 (§4.1) | COVERED |
| INV-001/007/009/015/016 | R4 (loop_guard/models), R6 (SHA attribution) | COVERED |
| §6.3 test layout | R1, R4 | COVERED |
| Run-log §11 / resume §12 | R5 (§5), R4 (run_log.py) | COVERED |
| Marker/cov registration §18 | R4 (§E/§F) | COVERED |
| MDTM template rules | R7 | COVERED |
| Build DAG §3 | R1, R6, R7 | COVERED |
| SoT / PR-target §19 | R2 (§6), R5 (§4) | COVERED |

Every spec component, FR/NFR/INV class, and meta-layer (test infra + template) has at least one research file covering it. No spec area is uncovered.

---

## Contradictions across research files

None material. R2 and R5 touch the same sync/registration question and **agree** (R5 resolves what R2 left open). R3, R4, R5 all independently land on the hyphenated-skill-dir vs underscored-python-pkg split consistently. No two files describe the same component differently.

---

## Compiled gaps

### Critical gaps (block task-building): NONE

The research is sufficient to build the MDTM task file. Every component has a path+status, every reuse surface a DEFER-TO contract, the test architecture is resolved, the DET probe is encoded as a HALT, the gh surfaces are exact, and the template rules + exemplars are documented.

### Minor gaps (must still be fixed, do not block):

1. **Validation-gate (VG-1..VG-6 / §10) command details are thinner than other surfaces.** R5 §4 covers gh/git discipline and R4 covers the FSM `validation_status` consumer, but no single research file enumerates the §10 ordered gate list (VG-1 targeted pytest → VG-2 `make test` escalation → VG-3 `make lint` → VG-4 `ruff format --check` → VG-5 `make verify-sync` → VG-6 PR-target) as a concrete per-gate build surface the way R6 did for the gh surfaces. The spec §10 itself is fully specified, so the builder can lift it directly, but no researcher cross-validated those exact commands against the repo Makefile targets (e.g., confirming `make test` and `make verify-sync` exist as named targets). Low risk — these are well-known repo commands cited throughout CLAUDE.md.

2. **`hooks/scripts/` → `.claude/hooks/` sync-flattening not fully confirmed.** R2 §7.2 raised the question (does `make sync-dev` copy hooks, flattening `scripts/`?). R5 §3.2 documented the Makefile sync for skills/agents/commands (Makefile:112-135) but did NOT explicitly confirm a `hooks/` copy rule. R1 (flag 1) observed `.claude/hooks/scripts/offer-pr-review.sh` is ABSENT and noted hooks may not be mirrored like refs. Net: the C5 hook EDIT is correctly scoped `src/`-only (no `.claude/hooks/` staging — that discipline IS resolved), but whether the edited hook auto-propagates to `.claude/hooks/` via `make sync-dev` (spec build step [6] assumes it) is not definitively answered. Builder should grep the Makefile `sync-dev` target for a hooks copy rule before relying on it. Low risk — the test pattern (R6 §3.1) targets the `src/` source of truth anyway, so tests pass regardless.

3. **Cosmetic: stale "In Progress" top-of-file markers** in R2, R5, R7 (each ends "Status: Complete"). No content impact.

---

## VERDICT: PASS

All 10 lens checks PASS. All 7 assigned research files are Complete, evidence-dense, and free of fabrication. Every spec area (C1–C6, DET, LG, VAL, FR-1..7, NFR-1..8, INV-001/007/009/015/016, §3 build DAG, §6.3 21-file test layout, §10 validation, §11/12 run-log, §18 markers/coverage, §19 SoT, MDTM template) has corresponding research coverage at builder-actionable granularity. Open ambiguities (R1 probe, --cov hyphen defect, unregistered markers, troubleshoot-no-auto-apply seam, Monitor-≠-daemon) are explicitly flagged, not silently assumed. No CRITICAL gaps; 2 low-risk minor gaps (§10 validation-gate command cross-validation, hooks sync-flattening confirmation) + 1 cosmetic. The research corpus is sufficient to proceed to task-building.
