# R2 — Troubleshoot Surface (Patterns & Conventions / Integration)

**Status: Complete**

Scope: exact anchors + conventions for TFEP pipeline changes 2 (return-contract adapter) and 3 (`--context`/`--caller` ingestion).

Files analyzed (both read in full):
- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md` (203 lines)
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (588 lines)

Citations are `file:line` against the SoT `src/superclaude/` copies. Edits must land in `src/` then `make sync-dev` (CLAUDE.md SoT rule). The `.claude/` mirror is gitignored.

---

## PART A — `commands/troubleshoot.md` anchors (change 3: flag ingestion + surface)

### A1. Frontmatter `argument-hint` (line 8)

```
8: argument-hint: "[<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp]"
```
- This hint is the canonical flag list advertised to the user. `--context <path>` and `--caller <name>` must be appended here too. NOTE: this hint is already MISSING `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds` (those exist in the SKILL Wave 0 parse list at SKILL line 115) — the command frontmatter is already partial vs the protocol. Decide whether to add the two new flags only, or also reconcile. R3 owns cross-ref sync; flag here only.

### A2. Options table — line range and exact row format (lines 48–58)

Table header + separator:
```
48: | Flag | Default | Description |
49: |------|---------|-------------|
```
Existing rows (each row = `| `\`--flag\`` | `\`default\`` | prose. |`):
- line 50: `| `--type` | auto-detect | ... |`
- line 51: `| `--depth` | `standard` | ... |`
- line 52: `| `--scope` | (none) | ... |`
- line 53: `| `--no-escalate` | `false` | ... |`
- line 54: `| `--fix` | `false` | ... |`
- line 55: `| `--models` | (agent defaults) | ... |`
- line 56: `| `--output-dir` | `.dev/troubleshoot/<slug>-<timestamp>/` | ... |`
- line 57: `| `--no-doc-discovery` | `false` | ... |`
- line 58: `| `--no-mcp` | `false` | ... |` ← **last data row of the table**

**Exact row format to mirror** (canonical shape from line 57): `| ` + backticked flag + ` | ` + backticked default (or `(none)` unbackticked for absent — see line 52) + ` | ` + sentence ending in `.` + ` |`.

**Insertion point for new flag rows**: after line 58 (`--no-mcp`), as new rows 59+. Proposed:
```
| `--context` | (none) | Path to a caller-supplied context file (e.g. TFEP `return-contract.yaml` consumer brief). Ingested in Wave 0; recorded in the audit-log header and echoed in the Wave 5 return. |
| `--caller` | (none) | Name of the invoking pipeline/command (e.g. `task-unified`). When set, Wave 5 emits a `return-contract.yaml` adapter and the audit header records `caller:`. |
```
Default sentinel for "absent" matches line 52 `--scope`'s `(none)` (unbackticked).

### A3. `## Usage` fenced examples (lines 37–44) / `## Examples` (lines 104–154)

Optional: a programmatic-call example showing `--context`/`--caller` could be added in the `## Usage` block (lines 37–44) or `## Examples` (104–154). Not load-bearing for the contract; R4 owns template mechanics, R3 owns examples consistency. Flag only.

### A4. Activation handoff line to the skill (lines 77–82)

```
77: ## Activation
79: **MANDATORY**: Before executing any protocol steps, invoke:
80: > Skill sc:troubleshoot-protocol
82: Do NOT proceed with protocol execution using only this command file. The full behavioral specification — wave structure, escalation rubric, agent selection, file:line validation, hallucination contract, remediation chain — is in the protocol skill.
```
- The handoff is a bare `> Skill sc:troubleshoot-protocol` (line 80); it does NOT pass args explicitly — flags flow implicitly. No change strictly required for ingestion, but line 82's enumerated "full behavioral specification" list could gain "caller/context ingestion" + "TFEP return-contract emission" for discoverability. Optional.

### A5. "On skill return, surface:" behavioral list (lines 60–67) — change 2 + 3 surface anchor

```
60: ## Behavioral Summary
62: The full multi-wave protocol lives in the skill. The command file performs only:
64: 1. **Parse arguments** → resolve `--type` (auto-detect if absent), `--scope`, `--depth`, etc.
65: 2. **Validate environment** → at least one of MCPs is available (or `--no-mcp` is set); output dir is writable.
66: 3. **Hand off to the skill** via the Activation section below.
67: 4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, (if `--fix`) the Tier 3 remediation offer, and (if `pipeline_hardening_applicable`) the Pipeline Hardening Closure verdict + evidence-card paths.
```

- **Line 64** is the command-side parse step: `--context`/`--caller` must be added to the "resolve ... etc." enumeration (e.g. `..., --scope, --depth, --context, --caller, etc.`).
- **Line 67** is the EXACT "On skill return, surface:" behavioral list — where the TFEP return surface is advertised. Convention is the parenthetical-conditional style already used: `(if --fix) the Tier 3 remediation offer`, `(if pipeline_hardening_applicable) the Pipeline Hardening Closure verdict`. Mirror it: `..., and (if caller=task-unified) the emitted return-contract.yaml path.` This pattern is the convention to reuse for change 2's surface too.

### A6. `## Boundaries` (lines 156–193) and `## Related Commands` (lines 195–203)

- "Will:" list lines 158–169; "Will Not:" lines 172–181. If a TFEP caller should change behavior (auto-set defaults, never auto-apply when caller=task-unified), a Will/Will-Not bullet belongs here. The thin-command NFR-5 bullet is **line 169** (`...the skill computes the verdict + evidence paths and the command only advertises/surfaces them (thin command, NFR-5)`) — same "thin command advertises/surfaces, skill computes" convention should govern return-contract emission (skill emits the yaml, command only surfaces the path).
- `## Related Commands` (195–203) lists `task-builder` (line 200), `/sc:reflect --type task` (line 199). A `task-unified`/TFEP cross-ref row would slot here. R3 owns cross-refs.

---

## PART B — `sc-troubleshoot-protocol/SKILL.md` anchors

### B1. Wave 0 "Parse + Validate Input" — line range + exact flag-parse sentence (lines 109–143) — change 3

Wave 0 header at line 109. Steps block lines 113–139. Exit/STOP at 141–143.

**The exact flag-parse sentence (line 115)** — where `--context`/`--caller` parsing must be added:
```
115:    1. Parse flags. Required: issue description OR `--scope`. Optional: `--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`, `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`.
```
Add `--context`, `--caller` to the `Optional:` enumeration (backticked, comma-separated, sentence ends `.`).

Suggested new RESOLVE sub-step after step 5 (step 5's audit-header block is lines 126–139; new step 6 after line 139):
> 6. If `--caller` is set, record it in the audit header `caller:` field (see B2). If `--context <path>` is set, read it (caller brief) and resolve to an absolute path; STOP if unreadable. When `caller=task-unified`, set Wave 5 to emit `return-contract.yaml` (see B5).

**Other Wave 0 steps for context**: line 116–123 step 2 `--type` auto-detect table; line 124 step 3 resolve `--scope`; line 125 step 4 output slug + create `<output-dir>/`; line 126 step 5 "Open audit log; emit machine-readable header:" → header block lines 128–139.

**Exit criteria (line 141)**: `input validated, output dir created, audit log opened. Emit "Wave 0 complete: type=<type> depth=<depth>".` — could append `caller=<caller>` for traceability.

**STOP conditions (line 143)**: `missing input, conflicting flags (--depth quick with --fix), --depth deep on under-specified input, --output-dir not writable.` — add `--context path unreadable` if context ingestion should hard-fail.

### B2. Audit-log header block where `caller:` is recorded (lines 128–137) — change 3

```
128: <!-- SC:TROUBLESHOOT:TARGET
129: issue: <first 80 chars>
130: type: <type|auto>
131: depth: <quick|standard|deep|auto>
132: scope: <path|symbol|none>
133: fix_authorized: <bool>
134: no_escalate: <bool>
135: mcps_available: <auggie|serena|context7|tavily|sequential|none>
136: output_dir: <abs-path>
137: -->
```
**Insertion point for `caller:`**: a new line after line 136 (`output_dir:`) and before line 137 (`-->`). Proposed:
```
caller: <name|none>
context_path: <abs-path|none>
```
Convention: lowercase key, `: `, `<placeholder|sentinel>` with `none` as absent sentinel (matches `scope: <path|symbol|none>` at line 132).

### B3. Output Contract table — DONOR FIELD SET (full enumeration, lines 41–72) — change 2

Header lines 41–42:
```
41: | Field | Type | Description |
42: |-------|------|-------------|
```
**Every field already emitted (Field | Type | line):**

| # | Field | Type | line |
|---|-------|------|------|
| 1 | `status` | string (`success`/`partial`/`failed`) | 43 |
| 2 | `tier_reached` | int (1/2/3) | 44 |
| 3 | `report_path` | string (abs path to REPORT.md) | 45 |
| 4 | `audit_log_path` | string (abs path to audit.log) | 46 |
| 5 | `confidence` | float 0.0–1.0 | 47 |
| 6 | `escalation_reason` | string | 48 |
| 7 | `test_is_wrong` | bool | 49 |
| 8 | `test_file_path` | string \| null (repo-relative) | 50 |
| 9 | `behavior_is_documented` | bool | 51 |
| 10 | `doc_context_card_path` | string \| null (repo-relative) | 52 |
| 11 | `hypothesis_cards` | list[path] | 53 |
| 12 | `adversarial_artifacts_dir` | string | 54 |
| 13 | `task_file_path` | string (Tier 3) | 55 |
| 14 | `remediation_offered` | bool | 56 |
| 15 | `remediation_accepted` | bool | 57 |
| 16 | `diagnosability_verdict` | string (`sufficient`/`partial`/`insufficient`/`unknown`) | 58 |
| 17 | `diagnosability_context_card_path` | string \| null (repo-relative) | 59 |
| 18 | `diagnosability_tasklist_path` | string \| null (repo-relative) | 60 |
| 19 | `diagnosability_hard_stop` | bool | 61 |
| 20 | `contract_version` | semver string (default `1.0.0`) | 62 |
| 21 | `pipeline_hardening_applicable` | bool | 63 |
| 22 | `pipeline_hardening_verdict` | enum `pass\|blocked\|advisory\|not_applicable` | 64 |
| 23 | `waiver_status` | enum `none\|latched` | 65 |
| 24 | `backtest_status` | enum `not_run\|partial\|complete` | 66 |
| 25 | `off_path_review_decision` | enum `required\|performed\|waived_with_rationale\|not_required` | 67 |
| 26 | `runtime_entrypoint_card_path` | string \| null (abs) | 68 |
| 27 | `contract_ledger_path` | string \| null (abs) | 69 |
| 28 | `unmask_sweep_path` | string \| null (abs) | 70 |
| 29 | `effective_input_card_path` | string \| null (abs) | 71 |
| 30 | `known_escapes_caught` | list of `{escape_id,wave,card_path,status}` | 72 |

Two derivation-rule prose blocks follow the table: `test_is_wrong` rule lines 74–82; `behavior_is_documented` rule lines 84–86 (Case A/B/C decomposition at line 84).

**Mapping donor fields → TFEP forensic-style return-contract.yaml needs:**

| TFEP-needed field | Donor present? | Source line / gap |
|-------------------|----------------|-------------------|
| `status` | YES — `status` (43). Value set differs: troubleshoot = `success\|partial\|failed`; TFEP forensic enum likely differs → adapter must map. | 43 |
| `test_is_wrong` | YES — `test_is_wrong` (49) **plus** `test_file_path` (50) as remediation target when true. Direct donor; already asymmetric-cost (line 49 prose: downstream MUST NOT auto-apply code fix). | 49–50 |
| `recommended_escalation` | **MISSING** — closest is `escalation_reason` (48, *why Tier 2 ran*) + `tier_reached` (44). Neither is forward-looking "what caller should do next." Adapter must synthesize from `status`+`tier_reached`+`confidence`+Wave 5 Next Steps (SKILL line 434). |
| `tasklist_insertion_path` | **MISSING** as named. Closest donors: `diagnosability_tasklist_path` (60, instrumentation tasklist) and `task_file_path` (55, Tier 3 MDTM file). Neither is a "where in the TFEP tasklist to insert" pointer. Adapter must repurpose `task_file_path` or add a new field. |
| `remediation` block (target + block path) | **PARTIAL** — donors: `task_file_path` (55), `test_file_path` (50), prose Proposed Fix (Wave 5, SKILL line 431). Asymmetric-cost flags `test_is_wrong`/`behavior_is_documented` (49/51) already encode *which* target (test vs code vs docs). But NO single structured `remediation_target`/`remediation_block_path` field. Adapter must compose: target = test (if test_is_wrong) / docs (if behavior_is_documented) / code (else); block path = `test_file_path` / Proposed Fix file. |
| `root_cause_summary` | **MISSING** as structured field — prose only in REPORT.md Diagnosis (Wave 5, SKILL line 429) + Summary (426). Adapter must extract from REPORT.md or chosen hypothesis card. |
| `solution_summary` | **MISSING** as structured field — prose only in REPORT.md Proposed Fix (SKILL line 431). Adapter must extract. |

**Adapter design implication**: donor set is RICH for asymmetric-cost gating (`test_is_wrong`, `test_file_path`, `behavior_is_documented`, `diagnosability_*`) but THIN for the forensic TFEP's forward-looking/summary fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`). These 5 are absent and must be either (a) newly ADDED to the Output Contract table (additive — bump `contract_version` from `1.0.0` per the line-62 convention; line 62 already documents the additive-versioning + NFR-6 backward-compat discipline), or (b) synthesized by an adapter shim at Wave 5 emission time from existing fields + REPORT.md prose. Recommend (a) for fields the TFEP parses, mirroring the existing additive-field pattern (lines 62–72 are themselves an additive Pipeline-Hardening block stamped by `contract_version`).

### B4. `contract_version` additive-versioning convention (line 62) — change 2 governance

```
62: | `contract_version` | semver string | Output-contract semver, default `1.0.0`. Additive version stamp for the Pipeline Hardening Closure fields below (FR-13); existing consumers reading only the prior fields are unaffected (NFR-6). Distinct from `target_release`. |
```
Precedent: the H0–H5 hardening fields (63–72) were added additively and stamped by `contract_version`. Any new TFEP fields should follow the same pattern: append to the table, bump default `contract_version`, cite NFR-6 backward-compat. This is the EXACT in-file convention governing change 2's field additions.

### B5. Wave 5 "Synthesis + Report" — return-contract.yaml emission anchor (lines 417–466) — change 2 + 3

Wave 5 header line 417. Steps:
- line 423: step 1 load `refs/report-template.md`.
- lines 424–441: step 2 compose REPORT.md (Header/Summary/Documentation Context/Diagnosability Context/Diagnosis/Evidence/Proposed Fix/Alternatives/Risk+Rollback/Next Steps/Pipeline Hardening Closure). **Prose donors for the B3 missing summary fields**: Summary line 426, Diagnosis line 429, Proposed Fix line 431, Next Steps line 434.
- lines 442–443: step 3 evidence-validator file:line validation pass.
- lines 444–457: step 4 append machine-readable footer (`<!-- SC:TROUBLESHOOT:SUMMARY ... -->`, block lines 446–455). **Natural sibling location** to also emit a `caller`/`return_contract_path` line; precedent for machine-readable structured emission at Wave 5.
- lines 459–465: step 5 "Surface to the user in chat" list (one-paragraph summary, REPORT.md path, chosen fix, tier+confidence, next-step recommendation).
- line 466: **Exit criteria** — `REPORT.md written, audit log finalized, user notified. If --fix is not set, return the output contract and STOP.`

**Where the `return-contract.yaml` emission (when caller=task-unified) is added**: a new Wave 5 step between step 4 (footer, ends line 457) and step 5 (surface, line 459), OR a conditional sub-bullet under step 4. Proposed new step:
> 4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` mapping the Output Contract fields to the TFEP-consumed schema (`status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`/block path, `root_cause_summary`, `solution_summary`). Source asymmetric-cost gates from `test_is_wrong`/`test_file_path`/`behavior_is_documented`; source summaries from the REPORT.md Diagnosis (step 2) + Proposed Fix sections. Record `return_contract_path` in the audit footer.

**Exit criteria (line 466)** should gain: `when caller=task-unified, return-contract.yaml is written and its path returned.` **Step 5 surface list (459–465)** should add the return-contract.yaml path bullet (ties to command line 67, see A5).

### B6. `SC:TROUBLESHOOT:SUMMARY` footer block (lines 446–455) — change 3 emission sibling

```
446: <!-- SC:TROUBLESHOOT:SUMMARY
447: status: <success|partial>
448: tier_reached: <1|2|3>
449: confidence: <float>
450: escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent>
451: hypothesis_count: <N>
452: adversarial_invoked: <bool>
453: fix_authorized: <bool>
454: duration_sec: <N>
455: -->
```
A `caller: <name|none>` and `return_contract_path: <abs-path|none>` line slot after line 454 (`duration_sec`) before line 455 (`-->`), mirroring the B2 header convention.

---

## PART C — STOP conditions & caller=task-unified default interactions (change 3)

### C1. `--no-doc-discovery` skip semantics
- Command Options row: **line 57** (`--no-doc-discovery | false`).
- SKILL Wave 1.5 precondition + skip: **line 174** (`When --no-doc-discovery IS set, skip this entire wave, record doc_context_card_path: null ... surface a Grounding Gaps line`).
- Failure table line 198; Error Handling line 540.
- Implication: when set, `doc_context_card_path: null` and diagnosis is NOT weighted against documented behavior → `behavior_is_documented` degrades to `not_applicable`/`no_docs_found`. **If `--caller task-unified` wants `behavior_is_documented` meaningful, it should NOT auto-set `--no-doc-discovery`** (leave doc-discovery ON).

### C2. `--no-diagnosability-audit` skip semantics
- Command Options table: **NOT present** (gap — see A1; flag exists only in SKILL).
- SKILL Wave 1.6 precondition + skip: **line 216** (`When IT IS set: skip the wave entirely, emit diagnosability_verdict: unknown, diagnosability_context_card_path: null, diagnosability_hard_stop: false. The bypass is logged in REPORT.md's header AND in the audit log`).
- Failure table line 252; Error Handling line 550.
- Hard-stop behavior: **line 232** (`insufficient AND non-trivial AND NOT --no-escalate → hard-stop ... jump to Wave 5 with status partial (Waves 1.7-4 skipped)`).
- Soft-warn downgrade: **line 233** (`insufficient AND non-trivial AND --no-escalate → soft-warn ... continue to Wave 1.7`).
- **Caller-default tension**: a TFEP `task-unified` caller needing full diagnosis-with-remediation likely does NOT want the Wave 1.6 hard-stop to short-circuit to `status: partial`. Options for `--caller task-unified` defaults: (a) auto-set `--no-diagnosability-audit` to suppress the hard-stop (but `diagnosability_verdict: unknown` → weaker signal); or (b) leave audit ON and rely on the existing `--no-escalate` soft-warn (line 233) to prevent the hard-stop while preserving the verdict. **Recommend (b) / documenting that `--caller task-unified` does NOT auto-set diagnosability skips** unless TFEP explicitly wants the hard-stop suppressed — decision belongs to R1 (consumer side) / task author.

### C3. Other STOP conditions touching ingestion (Wave 0, line 143)
- `conflicting flags (--depth quick with --fix)` — if `--caller task-unified` auto-sets `--fix`, ensure it does NOT also pass `--depth quick`.
- `--output-dir not writable` — caller-supplied `--context`/`--output-dir` must be validated; add `--context path unreadable` as a new STOP (see B1).

---

## SUMMARY (for parent agent)

**Change 3 (`--context`/`--caller` ingestion) anchors:**
1. `commands/troubleshoot.md:8` — add flags to `argument-hint`.
2. `commands/troubleshoot.md:48–58` — Options table; insert two new rows after line 58 (`--no-mcp`); mirror row format of line 57; default sentinel `(none)` per line 52.
3. `commands/troubleshoot.md:64` — add `--context, --caller` to command-side parse step enumeration.
4. `commands/troubleshoot.md:67` — "On skill return, surface:" list; add parenthetical-conditional `(if caller=task-unified) return-contract.yaml path` (reuse `(if --fix)` / `(if pipeline_hardening_applicable)` convention).
5. `SKILL.md:115` — add `--context`, `--caller` to Wave 0 step 1 `Optional:` flag-parse sentence; add a resolve sub-step after line 139.
6. `SKILL.md:128–137` — audit-log `SC:TROUBLESHOOT:TARGET` header; insert `caller:` / `context_path:` after line 136 (`output_dir:`).
7. `SKILL.md:141` exit emit + `SKILL.md:143` STOP conditions — optionally append caller traceability + `--context unreadable` STOP.

**Change 2 (TFEP return-contract adapter) anchors:**
1. `SKILL.md:41–72` — Output Contract is the DONOR set (30 fields enumerated above with line numbers).
   - Direct donors: `status` (43), `test_is_wrong` (49), `test_file_path` (50), `behavior_is_documented` (51).
   - **MISSING TFEP fields**: `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`/block-path, `root_cause_summary`, `solution_summary` — none exist as structured fields; closest analogs are `escalation_reason`(48)/`tier_reached`(44), `diagnosability_tasklist_path`(60)/`task_file_path`(55), and prose-only REPORT.md sections.
2. `SKILL.md:62` — `contract_version` additive-versioning convention is the precedent for adding the 5 missing fields (append to table, bump semver, cite NFR-6).
3. `SKILL.md:417–466` — Wave 5; add a conditional emission step (~step 4.5, after the footer block ending line 457, before surface step at line 459) writing `return-contract.yaml` when `caller=task-unified`; extend Exit criteria (line 466) and surface list (459–465).
4. `SKILL.md:446–455` — `SC:TROUBLESHOOT:SUMMARY` footer; add `caller:`/`return_contract_path:` lines (sibling machine-readable emission precedent).
5. Prose donors for summary fields: REPORT.md Summary (line 426), Diagnosis (429), Proposed Fix (431), Next Steps (434).

**Default-interaction caveats (for R1 / task author):**
- `--caller task-unified` should NOT auto-set `--no-doc-discovery` (would null `doc_context_card_path` and weaken `behavior_is_documented`; skip at SKILL line 174).
- `--caller task-unified` hard-stop tension with Wave 1.6 (`--no-diagnosability-audit` skip at line 216; hard-stop at line 232 → `status: partial`). Prefer relying on `--no-escalate` soft-warn (line 233) over auto-skipping the audit, to keep `diagnosability_verdict` meaningful.

**Convention notes:**
- Command is a THIN advertiser (NFR-5, command line 169): the skill EMITS the return-contract.yaml; the command only SURFACES the path. Keep emission logic in SKILL.md, surface-only in troubleshoot.md.
- SoT: edit `src/superclaude/`, then `make sync-dev` (never edit `.claude/` directly).
- Command `argument-hint` (line 8) is already partial vs SKILL Wave 0 flag list (line 115) — 3 diagnosability flags missing from the command. R3 owns reconciling; noted here only.
