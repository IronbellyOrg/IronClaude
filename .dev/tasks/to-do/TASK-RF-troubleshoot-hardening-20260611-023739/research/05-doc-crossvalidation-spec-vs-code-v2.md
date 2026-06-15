# Research: Doc Cross-Validation v2 — RELEASE-SPEC claims vs ACTUAL code

- **Topic type**: Documentation Staleness / Spec-vs-Code cross-validation
- **Scope**: `sc-troubleshoot-protocol` skill on disk + RELEASE-SPEC §4.1/§4.2 file tables
- **Spec under test**: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` (v1.1.0)
- **Status**: Complete
- **Date**: 2026-06-11

Tags: [CODE-VERIFIED] confirmed by reading actual file · [CODE-CONTRADICTED] code differs · [UNVERIFIED] not found.

---

## Findings (appended incrementally per file)

### A. Directory inventory (`ls` + `git check-ignore`, 2026-06-11)

`src/superclaude/skills/sc-troubleshoot-protocol/` contains `SKILL.md` (55634 bytes, mtime Jun 4) and `refs/` with 8 existing files: `calibrator-eval-cases.md`, `diagnosability-audit.md`, `doc-discovery.md`, `escalation-rubric.md`, `hypothesis-card-template.md`, `remediation-handoff.md`, `report-template.md`, `triage-checklist.md`.

**Claim 1 — MODIFIED files exist NOW (spec §4.2):**
- `SKILL.md` — **[CODE-VERIFIED]** exists (55634 bytes).
- `commands/troubleshoot.md` — **[CODE-VERIFIED]** exists (13293 bytes).
- `refs/report-template.md` — **[CODE-VERIFIED]** exists (16909 bytes).
- `refs/remediation-handoff.md` — **[CODE-VERIFIED]** exists (5434 bytes).

**Claim 2 — NEW ref files do NOT already exist (spec §4.1)** — all 6 confirmed ABSENT (builder must CREATE, never overwrite):
- `pipeline-hardening-closure.md` · `runtime-entrypoint-verification.md` · `contract-enumeration.md` · `unmask-and-sweep.md` · `effective-input-proof.md` · `hardening-output-contract.md` — **[CODE-VERIFIED absent]** (none in the `refs/` listing).

**Claim 4 — `tests/troubleshoot/` directory** — **[CODE-CONTRADICTED]**: directory does NOT exist (`ls: cannot access 'tests/troubleshoot/'`). All 7 spec test files are net-new; builder must CREATE the dir + `__init__.py` + 7 files (`test_hardening_h0.py`, `_h1`, `_h2`, `_h3`, `_h4`, `_verdict.py`, `_output_contract.py`). Sibling pytest dirs exist (`tests/skills/`, `tests/contracts/`, `tests/roadmap/`, etc.).

**Claim 5 — `.claude/` dev mirror gitignored** — **[CODE-VERIFIED]**: `.claude/skills/sc-troubleshoot-protocol/` exists as the mirror; `git check-ignore .claude/skills/sc-troubleshoot-protocol/SKILL.md` → IGNORED-CONFIRMED. `.gitignore` lines 120-121: `.claude/*` then `!.claude/settings.json`. Builder edits ONLY `src/superclaude/`, then `make sync-dev`.

### B. `commands/troubleshoot.md` — thin command (Claim 1)

**[CODE-VERIFIED thin]**. Behavioral Summary (lines 60-67) explicitly: "The full multi-wave protocol lives in the skill. The command file performs only: 1. Parse arguments 2. Validate environment 3. Hand off to the skill 4. On skill return, surface...". Activation section (lines 78-82) mandates `Skill sc:troubleshoot-protocol`.

**Where the one advertise sentence goes (FR-1 / NFR-5 thin-command):**
- The "Three tiers under the hood" table (lines 71-75) — add a row or a sentence noting pipeline-hardening mode auto-triggers on boundary topology when `applicable=true`. Most natural: a sentence in **Behavioral Summary step 4** ("surface ... and (if applicable) the Pipeline Hardening Closure verdict + evidence paths") and a line in **Boundaries → Will** (lines 158-169).
- The argument-hint (line 8) needs NO new flag (spec §5.1: "no new CLI flags"; FR-1 triggers by topology, not a flag). **Do NOT add a `--hardening` flag** — that contradicts §5.1 + NFR-5.

### C. `refs/report-template.md` — closure section (Claims 1, 6)

**[CODE-VERIFIED]** exists. Structure: a fenced ```` ```markdown ```` template block (lines 7-203) then post-template `## ` rule sections.

- **Existing post-template `## ... rule` sections** (the pattern the new closure section follows): `## Rendering rules` (line 205), `## Test-is-wrong rule` (line 212), `## Behavior-is-documented rule` (line 233). FR-13's `Pipeline Hardening Closure` section + its rendering rules should be added in this same post-template region and inside the template block as a new `## Pipeline Hardening Closure` section (after `## Audit`, line 196, or after Risk+Rollback — builder's choice; spec §4.2 just says "add a `Pipeline Hardening Closure` section").
- **Existing header verdict/status fields** (template lines 13-21): `**Status**: <success|partial>`, `**Tier reached**`, `**Test is wrong**: <true|false>`, `**Behavior is documented**: <true|false|n/a>`. The Diagnosability Context section uses `**Verdict**: <sufficient | partial | insufficient | unknown>` (line 54).
- **`Closure verdict` markdown block / verdict enum** — **[CODE-CONTRADICTED]**: NO existing `Closure verdict` block and NO `pass|blocked|advisory` enum anywhere in report-template.md. The spec's verdict enum is net-new. (Existing sibling enums use lowercase pipe-delimited tokens: `success|partial`, `sufficient|partial|insufficient|unknown` — consistent with the spec's `pass|blocked|advisory|not_applicable` style.)
- **`NOT PROVEN` language** (FR-13) — net-new; current template's strongest hedge is `status: partial` + "Grounding Gaps". No `NOT PROVEN` token present today.

### D. `refs/remediation-handoff.md` — handoff payload (Claim 1, FR-12)

**[CODE-VERIFIED]** exists. The handoff payload that must carry the hardening verdict + waiver latch:
- **The user offer block** (lines 9-28) — verbatim prompt; would gain a line surfacing hardening verdict / `waiver_status=latched` blocker before offering Tier 3.
- **`BUILD_REQUEST` block** (lines 42-56) — the structured payload handed to `task-builder`. FR-12 requires `pipeline_hardening_verdict` + `waiver_status` ride here so a downstream `task-builder`/`sc:reflect`/`adversarial` stage cannot re-green a `blocked`/`advisory`. Today it carries TEMPLATE/GOAL/WHY/WHERE/ACCEPTANCE_CRITERIA/REFERENCES only — no hardening fields. **[CODE-CONTRADICTED for hardening fields: absent today, must be ADDED.]**
- **Gating note**: handoff is "Loaded only when `--fix` is set and Wave 5 produced a `success` (not `partial`) report" (line 3). FR-12's downstream no-override rule interacts with this `success`-gate — the §5.4 `success_with_hardening_blocker` rendering must be reconciled with this `success`-only precondition (builder note: a `blocked`/`advisory` hardening verdict should prevent a plain-`success` handoff).

### E. `SKILL.md` — Tier structure, insertion point, result schema (Claims 1, 3, 6)

**[CODE-VERIFIED]** Structure (heading line numbers):
- `## Output Contract` (line 37) — the structured result dict (table lines 41-61).
- `## Wave Structure` (line 77) — pipeline map (lines 79-91).
- Waves: `Wave 0 Parse+Validate` (97), `Wave 1 Tier 1 Real-Code Grounding` (135), `Wave 1.5 Documentation Grounding` (158), `Wave 1.6 Diagnosability Audit` (196), `Wave 1.7 Tier 1 Hypothesis Formation` (251), `Wave 2 Confidence Gate` (271), `Wave 3 Tier 2 Parallel Hypotheses` (291), `Wave 4 Tier 2 Adversarial Fix Debate` (356), `Wave 5 Synthesis + Report` (385), `Wave 6 Tier 3 Remediation Chain` (437).

**Exact insertion point "after Tier 1 diagnosis, before report closure" (spec §2 / §4.2):**
- "Tier 1 diagnosis" completes at **Wave 1.7 (Tier 1 Hypothesis Formation, line 251)**; the **Wave 2 Confidence Gate (line 271)** decides escalation. Report closure is **Wave 5 (line 385)**.
- The hardening mode (H0-H5) is a NEW wave inserted **after Wave 1.7 / around Wave 2, before Wave 5**. Most consistent with the existing scheme: add a new wave (e.g. **"Wave 4.5 / Wave 5.0: Pipeline Hardening Closure"** between Wave 4 and Wave 5, OR a sub-wave gated on `pipeline_hardening_applicable`) that the **Wave 5 report composition (lines 392-402) then renders** as the closure section. Builder must wire: (a) a trigger after Tier-1 diagnosis, (b) the H0-H5 statuses into the Output Contract, (c) the verdict into Wave 5 report composition list (currently lines 393-402, which must gain a "Pipeline Hardening Closure" bullet).
- **Anchor caution**: line numbers WILL drift once edits land. Builder should anchor on heading text (`### Wave 5: Synthesis + Report`, `### Wave 1.7: Tier 1 — Hypothesis Formation`, `## Output Contract`) not raw line numbers.

**Claim 3 — EXISTING Output Contract result fields** (SKILL.md lines 41-61, so FR-13 additive fields append without breaking NFR-6):
`status` (string: success|partial|failed), `tier_reached` (int), `report_path`, `audit_log_path`, `confidence` (float), `escalation_reason`, `test_is_wrong` (bool), `test_file_path` (string|null), `behavior_is_documented` (bool), `doc_context_card_path` (string|null), `hypothesis_cards` (list[path]), `adversarial_artifacts_dir`, `task_file_path`, `remediation_offered` (bool), `remediation_accepted` (bool), `diagnosability_verdict` (string), `diagnosability_context_card_path` (string|null), `diagnosability_tasklist_path` (string|null), `diagnosability_hard_stop` (bool).

- **Existing `*_card_path` / `*_path` field style** — snake_case, suffix `_path` (e.g. `doc_context_card_path`, `diagnosability_context_card_path`, `report_path`, `task_file_path`). Spec's new `runtime_entrypoint_card_path` / `contract_ledger_path` / `unmask_sweep_path` / `effective_input_card_path` **match this convention exactly** — [CODE-VERIFIED consistent].
- **`string | null` nullability style** is the existing idiom (e.g. `test_file_path`, `doc_context_card_path` are `string | null`). Spec's "nullable before HN" maps cleanly.
- **No `contract_version` field today** — net-new (FR-13). No existing version field on the result dict.

**Claim 6 — verdict-enum style check** (grep across skill+refs):
Existing `*_verdict` fields: `diagnosability_verdict` (enum `sufficient|partial|insufficient|unknown`, SKILL.md line 58), `reachability_verdict` and `currency_verdict` (in refs/diagnosability-audit.md / doc-discovery.md). All use lowercase, pipe-or-comma-delimited token lists. The spec's `pipeline_hardening_verdict` enum `pass|blocked|advisory|not_applicable` is **stylistically consistent** with these. **advisory is MANDATED by the spec (§4.5, §5.4 rows 5-6, FR-13) — do NOT drop it** even though no sibling enum currently has an `advisory` token. (`not_applicable` mirrors existing `n/a`/`unknown` escape tokens.)

### F. Sync model + lint gates (Claim 5)

**[CODE-VERIFIED]:**
- `Makefile` targets: `sync-dev:` (line 109), `verify-sync:` (line 166), `lint:` (line 48 → `lint-architecture`), `format:` (line 53). Matches spec §4.6 step 7 ("make sync-dev + make verify-sync") and §9 rollback.
- **markdownlint**: `.markdownlint.json` = `{default:true, MD024 siblings_only, MD013 false, MD029 false, MD036 false, MD033 false}`. Pre-commit hook `markdownlint-cli@v0.38.0` with `args:['--fix']` (`.pre-commit-config.yaml` lines 70-82).
  - **CRITICAL nuance**: the markdownlint `exclude:` regex (lines 76-82) excludes `\.dev/.*` — so research/spec files under `.dev/` are NOT linted, but the **target skill files under `src/superclaude/skills/sc-troubleshoot-protocol/*.md` (and `.claude/` mirror) ARE linted**. The 6 new refs + SKILL.md/command/report-template/remediation-handoff edits MUST be markdownlint-clean (MD024 siblings-only means duplicate headings under different parents are OK; watch MD025 single-H1, MD040 fenced-code-language).
- **Test convention** (sibling `tests/skills/test_task_builder_merge.py`): content-level assertion tests over **source-of-truth markdown** — `REPO_ROOT = Path(__file__).resolve().parents[2]`, asserting markers in `src/superclaude/skills/.../SKILL.md`. This is the established pattern the spec's `tests/troubleshoot/*.py` markdown-contract validators should follow (assert on `src/` side; `.claude/` agrees post-sync). `tests/conftest.py` provides shared fixtures + a `collect_ignore` for optional-dep tests.

## Summary — items the builder MUST heed

**[CODE-CONTRADICTED] / NET-NEW (builder must CREATE, not edit):**
1. `tests/troubleshoot/` does NOT exist — CREATE dir + `__init__.py` + 7 test files. Follow `tests/skills/` pattern (content-assertions over `src/` markdown; `REPO_ROOT = parents[2]`).
2. All 6 new refs under `refs/` are ABSENT — CREATE, never overwrite.
3. `report-template.md` has NO existing `Closure verdict` block / `pass|blocked|advisory` enum / `NOT PROVEN` token — all net-new.
4. `remediation-handoff.md` BUILD_REQUEST + user-offer carry NO hardening fields today — ADD `pipeline_hardening_verdict` + `waiver_status`. Reconcile FR-12 no-override with the existing "loaded only on `success`" gate (line 3).
5. SKILL.md Output Contract has NO `contract_version` and NO hardening fields — append additively (NFR-6 backward-compat).

**[CODE-VERIFIED] safe assumptions:**
- All 4 §4.2 MODIFIED files exist at the spec-claimed paths.
- New `*_card_path`/`*_path` + `string|null` field naming matches existing snake_case `_path` idiom exactly.
- Existing verdict enums (`diagnosability_verdict`, `reachability_verdict`, `currency_verdict`) use the same lowercase pipe-delimited style as the spec — `pass|blocked|advisory|not_applicable` is consistent; **advisory is mandated, keep it**.
- Command is genuinely thin (parse/validate/handoff/surface) — add ONE advertise sentence in Behavioral Summary step 4 + a Boundaries→Will line; **add NO new CLI flag** (§5.1/NFR-5).
- `make sync-dev` / `make verify-sync` targets exist; `.claude/` mirror is gitignored (`git check-ignore` confirmed). Edit `src/` only, then sync.

**Anchor / drift warnings for the builder:**
- Insertion point "after Tier 1 diagnosis, before report closure" = after `### Wave 1.7: Tier 1 — Hypothesis Formation` / around `### Wave 2: Confidence Gate`, before `### Wave 5: Synthesis + Report`. Wave 5 report-composition bullet list (currently composes Header/Summary/Diagnosis/...) must gain a "Pipeline Hardening Closure" bullet. **Anchor on heading TEXT, not line numbers — they drift after edits.**
- markdownlint applies to the target `src/superclaude/skills/...*.md` (NOT `.dev/`). Keep new refs MD-clean: single H1 (MD025), fenced-code language tags (MD040), MD024 is siblings-only.
