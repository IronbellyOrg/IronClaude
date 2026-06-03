# Research 06 — Cross-Spec Dependency + Open-Question Probes (Integration Points + Doc Cross-Validator)

**Status:** Complete
**Date:** 2026-06-02
**Track:** FR-RV3-MED.1–4 (4 Medium-Complexity Serena Adoptions)
**Scope:** low-spec task folder, live Serena MCP surface, SKILL.md §10.4/§14.5.2/§4.0, spec's 10 OQs (OQ-M1..M10)

---

## LIVE SERENA SURFACE PROBE (this environment) — [CODE-VERIFIED via runtime probe]

I invoked `mcp__serena__get_current_config` against the activated `IronClaude` project in THIS
environment. Verbatim return shape (load-bearing for OQ-M1/M3/M5 and for the low-spec OQ-4):

```
Serena version: 1.5.4.dev0
Active project: IronClaude
Language backend: LSP (global default: LSP)
Active context: claude-code
Active modes: editing, interactive
Available but not active modes: no-memories, no-onboarding, onboarding, one-shot, planning, query-projects
Active tools (after all exclusions): activate_project, delete_memory, edit_memory, find_declaration,
  find_implementations, find_referencing_symbols, find_symbol, get_current_config,
  get_diagnostics_for_file, get_symbols_overview, initial_instructions, insert_after_symbol,
  insert_before_symbol, list_memories, onboarding, read_memory, rename_memory, rename_symbol,
  replace_content, replace_symbol_body, safe_delete_symbol, write_memory
Available but not active tools: create_text_file, delete_lines, execute_shell_command, find_file,
  get_diagnostics_for_symbol, insert_at_line, jet_brains_debug, jet_brains_find_declaration,
  jet_brains_find_implementations, jet_brains_find_referencing_symbols, jet_brains_find_symbol,
  jet_brains_get_symbols_overview, jet_brains_inline_symbol, jet_brains_list_inspections,
  jet_brains_move, jet_brains_rename, jet_brains_run_inspections, jet_brains_safe_delete,
  jet_brains_type_hierarchy, list_dir, list_queryable_projects, open_dashboard, query_project,
  read_file, remove_project, replace_lines, restart_language_server, search_for_pattern, serena_info
```

**Direct consequences for the FRs in THIS environment (the eval/dev surface):**

| Tool | Status here | FR impact |
|---|---|---|
| `get_current_config` | **ACTIVE** | FR-7 substrate is callable; its return-shape (above) is now CODE-VERIFIED, not inferred. |
| `prepare_for_new_conversation` | **ABSENT** (not in active OR available-but-not-active lists; not in my MCP tool surface) | FR-3 (medium) → OQ-M1 stays **[RUNTIME-PROBE-REQUIRED]**; the tool is genuinely not surfaced. |
| `type_hierarchy` (LSP) | **ABSENT**; only `jet_brains_type_hierarchy` exists (available-but-not-active) | FR-1 (medium) → OQ-M3 confirmed: LSP backend has NO `type_hierarchy`; JetBrains-only here. |
| `execute_shell_command` | present but **CONTEXT-EXCLUDED** (available-but-not-active under `claude-code` context) | FR-4 (medium) → confirms the "context-excluded detection" path (FR-4.4) is the live default; verification triangle would degrade-and-continue in THIS context. |
| `onboarding` | **ACTIVE** | FR-2 (medium) → `onboarding_available: true` here. |

Backend here is **LSP**, version **1.5.4.dev0** (≥ v1.5 floor). This is the dev/eval surface; the
production operator surface may differ, which is exactly why the spec keeps Wave-0 probes.

---

## OQ-M5 — Cross-spec FR-RV3-LOW.7 `get_current_config` dependency status (MOST IMPORTANT)

**Classification: [RESOLVED] — the low-spec FR-7 substrate is BUILT and concrete; the medium task
should CONSUME it, with a thin derivation shim (NOT a duplicate probe).**

### Is FR-RV3-LOW.7 defined/built? YES — it is a fully-authored MDTM task.

The low-spec is NOT just a spec — it is a **built task file** at
`.dev/tasks/to-do/TASK-RF-20260602-135209/TASK-RF-20260602-135209.md`. FR-7 ships in its **Phase 2**
(co-shipped with FR-6 as the Wave-0 calibration pair; invariant A2 = "FR-7 ships here and ONLY here").
[CODE-VERIFIED against the task file, lines 160, 164-180.]

The low-spec FR-7 build items are concrete:
- **Step 2.1** (task:164): inserts `mcp__serena__get_current_config` into SKILL.md `allowed-tools`
  serena cluster (after `mcp__serena__activate_project,`, before `mcp__context7__resolve-library-id`).
- **Step 2.2** (task:168): adds Wave-0 outline line `0.5c get_current_config probe (active
  context/modes/version fingerprint)`.
- **Step 2.3** (task:170): authors the §4.0 detailed `**Step 0.5c (active-project config probe).**`
  prose block: invokes `get_current_config` at Wave 0; defensive field-presence checks for **active
  context, active modes, loaded tools list, and version**; extracts three-valued `serena_version` ∈
  `{<v1.5, >=v1.5, unknown}`; fail-open → `degraded_components: ["get_current_config"]` +
  `serena_version: unknown`.
- **Step 2.5** (task:180): adds §9.2 telemetry fields `serena_version`,
  `serena_config_snapshot_path`, `serena_active_context`, `serena_active_modes`, `onboarding_status`.

### What fields does its Wave-0 snapshot expose?

The low-spec FR-7 snapshot consumes/exposes exactly these raw inputs (task:170, research
06-serena-surface §OQ-4, matrix:399): **active context, active modes, loaded tools list,
language-backend selection, version**. Telemetry surface = `serena_active_context`,
`serena_active_modes`, `serena_version` (three-valued), `serena_config_snapshot_path`
(→ the full snapshot artifact). [CODE-VERIFIED against low-spec task:170,180.]

### Does the medium task need its own minimal inline probe, or can it consume FR-7?

**It can CONSUME FR-7 — but the medium's four derived fields are NOT 1:1 with FR-7's telemetry
fields.** The medium spec's minimal probe contract (spec §4.5, lines ~359-369) requires exactly:

```yaml
backend: jetbrains | lsp | none                 # gates FR-1 type_hierarchy
execute_shell_command_available: <bool>         # gates FR-4 (context-excluded detection)
onboarding_available: <bool>                    # gates FR-2 (context-excluded detection)
read_only: <bool>                               # FR-4.7 read_only:true → verification disabled
```

Mapping each medium field to the low-spec FR-7 snapshot:

| Medium probe field | Source in low-spec FR-7 snapshot | Derivation | Status |
|---|---|---|---|
| `backend` | "language-backend selection" (verified: `Language backend: LSP`) | direct parse → `lsp` \| `jetbrains` \| `none` | **derivable from FR-7** |
| `execute_shell_command_available` | "loaded tools list" (verified: present-but-excluded → not in active list) | membership test on the ACTIVE-tools list | **derivable from FR-7** |
| `onboarding_available` | "loaded tools list" (verified: `onboarding` IS active) | membership test on the ACTIVE-tools list | **derivable from FR-7** |
| `read_only` | **NOT in FR-7's enumerated field set** | NOT exposed by `get_current_config` output (it shows context+modes+tools+version+project, not the project `read_only` flag) | **GAP — see below** |

**The `read_only` gap is the load-bearing finding of OQ-M5.** The live `get_current_config` output
does NOT surface a `read_only` boolean. `read_only` is a Serena *project-config* setting
(`read_only: true` in the project's `.serena/project.yml`), and the `get_current_config` text dump
in this environment does not print it. The low-spec FR-7 telemetry set (task:180) likewise does NOT
include `read_only`. Therefore:

- The medium task **CANNOT** obtain `read_only` purely by consuming the low-spec FR-7 telemetry. It
  must derive `read_only` from a separate signal. Two evidenced options (the task-builder must pick
  one and the eval must assert it):
  1. **Behavioral inference** — if `execute_shell_command` AND all mutating tools are absent from the
     active list while the context is not read-only-named, that is ambiguous; not reliable.
  2. **Explicit project-config read** — read `read_only` from `.serena/project.yml` (or the active
     context/mode set; some Serena configs encode read-only as a context/mode). This is the robust
     path and is a SMALL addition the medium FR-4 Wave-0 step must own.

### Dependency contract (what the medium task-builder must encode)

1. **Consume, do not duplicate.** The medium FR-1/FR-2/FR-4 Wave-0 probe MUST consume the low-spec
   FR-7 `serena_config_snapshot_path` artifact and derive `backend`,
   `execute_shell_command_available`, `onboarding_available` from it (membership tests +
   backend-string parse). Field names are a strict subset → non-breaking swap (spec §4.5 last para).
2. **`read_only` is the one field FR-7 does NOT provide.** The medium FR-4 task MUST add a small
   `read_only` derivation (project-config read), since `get_current_config` does not surface it
   (CODE-VERIFIED: absent from the live output). This is the only genuinely-new probe surface the
   medium adds on top of FR-7.
3. **Merge-order contingency.** If the low-spec Phase 2 is NOT merged before the medium FR-4 PR, the
   medium ships the **minimal inline probe** (spec §4.5) computing all four fields directly from a
   `get_current_config` call + the project-config `read_only` read, then reconciles to FR-7 at merge.
   Because the medium needs `read_only` (which FR-7 omits), the inline probe is NOT pure duplication
   even post-merge — the `read_only` derivation persists either way.

**Evidence tags:** low-spec FR-7 build = [CODE-VERIFIED] (task file). `get_current_config` return
shape including ABSENCE of `read_only` = [CODE-VERIFIED] (live runtime probe, above). Medium probe
contract = [CODE-VERIFIED] (spec §4.5).

---

## OQ-M8 — Return-contract location (inline SKILL.md §9 vs refs/return-contract.yaml)

**Classification: [RESOLVED] — contract is INLINE in SKILL.md §9, NOT a separate
`refs/return-contract.yaml`.** [CODE-VERIFIED]

- `ls src/superclaude/skills/sc-reflect-protocol/refs/` returns 11 files: `cost-profile.yaml`,
  `coverage-mapping.md`, `deviation-taxonomy.md`, `grader-extensions.md`, `input-resolution.md`,
  `ops-integration.md`, `promotion-adapters.md`, `reflection-rubric.md`, `remediation-handoff.md`,
  `report-template.md`, `reviewer-spec.md`. **No `return-contract.yaml`.** [CODE-VERIFIED — confirmed
  in the low-spec research file `03-refs-and-inline-contract.md:10-19` and `06-...:212-236`, both of
  which ran the `ls` directly.]
- The stable contract is inline at **SKILL.md §9.1 (line 491)**; telemetry inline at **§9.2 (line
  601)**. [CODE-VERIFIED — anchors re-confirmed this session via grep at 491/601/689/704.]
- Medium-spec consequence: the medium §5 file-change matrix row
  `refs/return-contract.yaml *(if present — see OQ-M6)*` (spec line 294) is a **NO-OP / strike it**.
  All medium contract additions (`verification_ran`, `verification_invocations`,
  `verification_failures`, `verification_regressions_detected`, `regression_present`) land in
  **SKILL.md §9.1/§9.2 inline**, NOT a YAML file.

**Action for task-file:** route every medium contract/telemetry edit to SKILL.md §9 inline; strike
the conditional `return-contract.yaml` row. (Note OQ-M6 contract-version coordination: the low-spec
already bumps `1.0 → 1.1.0` at 3 sites — SKILL.md:491,494,599; if the low-spec lands 1.1.0 first, the
medium must bump to **1.2.0**, per spec line 454/532. This is a contract-version-collision follow-on,
not part of OQ-M8.)

---

## OQ-M1 — `prepare_for_new_conversation` signature (live MCP surface probe)

**Classification: [RUNTIME-PROBE-REQUIRED] — confirmed absent from THIS environment; signature
genuinely unknown.** [CODE-VERIFIED that it is absent here.]

- `prepare_for_new_conversation` is **NOT exposed** in this environment's Serena surface. It appears
  in neither the ACTIVE tools list nor the "available but not active tools" list of the live
  `get_current_config` output (see the probe section above), and there is no
  `mcp__serena__prepare_for_new_conversation` in this agent's MCP tool surface. [CODE-VERIFIED]
- Because the tool is not surfaced, **its signature/parameter shape cannot be determined here.** The
  spec's characterization (spec line 197-215, matrix:181-184,194,369: "the largest research gap") is
  upheld — OQ-M1 remains an unresolved runtime probe.
- **For the medium FR-3 (`prepare_for_new_conversation` Tier-3 handoff bridge):** FR-3 ships THIRD,
  Wave 6 only, value scales with `--remediate` frequency. The spec already encodes the correct guard:
  FR-3.6 (spec line 208) directs the implementer's MDTM to **OQ-M1 resolution before
  parameter-dependent wiring**, with a `write_memory` fallback (spec line 448) covering the
  tool-missing case. The live-absence here is direct evidence that the `write_memory` fallback is the
  realistic default for FR-3 in a `claude-code`-context Serena.

**Adjacency probe (also requested) — `onboarding`, `type_hierarchy`, `execute_shell_command` in THIS env:**
- `onboarding` → **ACTIVE** (exposed + active). FR-2 (`--onboard`) is live-runnable here.
- `type_hierarchy` → **ABSENT for LSP**; only `jet_brains_type_hierarchy` exists (available-but-not-active).
  See OQ-M3.
- `execute_shell_command` → **present but context-excluded** (available-but-not-active under
  `claude-code`). FR-4's verification triangle is OFF-by-context here → degrade-and-continue (FR-4.4).

**Action for task-file:** keep OQ-M1 as a **merge-precondition runtime probe** for the FR-3 phase
(probe the live Serena surface at adoption time; the dev/eval surface here proves the tool may be
entirely absent). Wire `write_memory` fallback as the default; do NOT hard-code any assumed
parameter shape. Mark FR-3 the LAST/lowest-priority adoption.

---

## OQ-M3 — LSP `type_hierarchy` coverage

**Classification: [RUNTIME-PROBE-REQUIRED] — but THIS environment yields a strong negative data
point: the LSP backend exposes NO `type_hierarchy` tool at all.** [CODE-VERIFIED for this env.]

- Live `get_current_config` (LSP backend, Serena 1.5.4.dev0): there is **no `type_hierarchy` in
  either the active or available tool list**; the ONLY hierarchy tool present is
  `jet_brains_type_hierarchy` (a JetBrains-backend tool, available-but-not-active). [CODE-VERIFIED]
- This **corroborates the spec's "JetBrains-only" reading** (spec line 161,176; matrix:64-66,69 —
  news entry dates the JetBrains-side tool to 2026-01-11) and **contradicts the README capability
  table's "LSP: yes"** that the spec flagged as the OQ-M3 contradiction (spec line 528). On the live
  LSP backend in this env, `type_hierarchy` is simply not a tool.
- The spec's empirical-probe plan stands (spec line 528): run `type_hierarchy` against
  **Python / Java / TypeScript** test projects and record per-language success. This env only proves
  the *tool-presence* gate (LSP → absent here); per-language LSP support (where the tool IS present
  on other LSP builds) still needs the empirical matrix.

**Action for task-file:** FR-1 (`type_hierarchy`, ships LAST) keeps `--with-hierarchy` **default-OFF
on `lsp`** and **unavailable on `none`** until the OQ-M3 empirical probe confirms per-language LSP
support. The Wave-0 `backend` field (from OQ-M5/FR-7) is the gate. Carry OQ-M3 as an
eval-authoring/empirical-probe item, with this env's "LSP→no type_hierarchy tool" recorded as the
baseline negative.

---

## OQ-M2 — `execute_shell_command` timeout + `--rerun-tests` migration

**Classification: [DECISION-DEFERRED] (timeout) + [RESOLVED] (migration surface is small).**

**`rerun-tests` migration surface — [CODE-VERIFIED]:** `grep -n "rerun-tests\|rerun_tests"
src/superclaude/skills/sc-reflect-protocol/SKILL.md` returns **exactly ONE hit**:

> **SKILL.md:725** — "A test that previously passed now fails after the diff (detect via task log or
> by re-running tests if `--rerun-tests` set)." (inside §10.4 Regression Detection signals)

That is the **only** reference to `--rerun-tests` in SKILL.md. The migration surface is therefore
minimal: FR-4 makes verification default-on and `--rerun-tests` a deprecated alias. The single SKILL.md:725
sentence is the one detection-signal site to update so the §10.4 Regression detector reads from the
new default-on `execute_shell_command` verification path instead of the opt-in `--rerun-tests` gate.

**Deprecation approach (per spec line 85,301,406,414,453):** `--rerun-tests` becomes a **deprecated
alias for "verification on" (the default)**, emitting a deprecation WARN; `--no-verify` is the new
opt-out. Single source of truth = "verification default-on". No flag removal (backward-compatible).

**Timeout — [DECISION-DEFERRED]:** Serena's tool-level default timeout is unverified (matrix:269).
The spec resolves this consumer-side regardless: wrap every command as `timeout <N> <cmd>` with
**default 120s, max 600s** (spec FR-4 envelope (d), line 228; OQ-M2 resolution line 527). This is a
consumer-side decision the task encodes, not a Serena fact to discover.

**Action for task-file:** (1) update the SINGLE SKILL.md:725 sentence to source the
previously-passing-test signal from the default-on verification path (alias `--rerun-tests`);
(2) add the `--rerun-tests` deprecated-alias WARN copy; (3) hard-code the consumer-side
`timeout 120` wrap (max 600) in the FR-4 envelope.

---

## OQ-M9 — Exit-code taxonomy completeness

**Classification: [DECISION-DEFERRED] (full table resolved in FR-4 eval-authoring) — the FR-4 default
mapping IS consistent with the existing §10.4 Regression definition.** [CODE-VERIFIED consistency.]

§10.4 Regression (SKILL.md:718-730) defines Regression via three detection signals (SKILL.md:722-726):
diff contradicts a spec criterion; **"a test that previously passed now fails after the diff"**
(line 725); a documented invariant violated. The FR-4 exit-code taxonomy maps cleanly onto this:

| FR-4 mapping | §10.4 consistency | Verdict |
|---|---|---|
| `pytest` exit 1 (test failed) → Regression candidate → `regression_present: true` | EXACTLY the SKILL.md:725 "previously-passing test now fails" signal | **consistent** |
| `pytest` exit 2/3 (collection/internal error) → Grounding Gap (§10.6) | not a behavioral contradiction → correctly NOT Regression | **consistent** (routes to §10.6, SKILL.md:736) |
| `pytest` exit 5 (no tests collected) → Drift/coverage (§10.3) | claimed-added test absent → Drift, not Regression | **consistent** (§10.5 precedence by evidence) |
| `ruff`/`mypy` exit 1 (lint/type finding) → `S_dev_density` signal only | not a contradiction of a passing commitment | **consistent** (rubric input, not Regression) |
| any exit 124 (timeout, FR-4.6) → Grounding Gap + `verify_timeout_hit` | insufficient evidence, not a contradiction | **consistent** |

The mapping does NOT alter the §10.4 definition; it provides a deterministic exit-code → class
function feeding the existing detector. The §10.5 precedence (Regression > Drift > Necessary >
Authorized, SKILL.md:732-734) is respected "by evidence, not by assignment" (spec line 240).

**Additional tools needing mapping (the OQ-M9 completeness gap):** the FR-4 table covers
`pytest`/`ruff`/`mypy`. The spec (OQ-M9, line 530) flags `make`, `cargo test`, `npm` as
**unmapped** — and mandates the conservative default: **an unmapped exit code defaults to Grounding
Gap, NEVER silently to Regression.** Concretely the task should enumerate during eval-authoring:
- `make <target>` non-zero — ambiguous (wraps any tool) → default Grounding Gap unless the wrapped
  tool is itself classified.
- `cargo test` (exit 101 = test failure) → Regression candidate (analogous to pytest 1).
- `npm test` / `tsc` (non-zero) → tool-dependent; `tsc` non-zero = type findings → `S_dev_density`.

**Action for task-file:** carry OQ-M9 as an **eval-authoring** completeness item (NOT a build-time
blocker). The build-time guarantee is the conservative default ("unmapped → Grounding Gap"); the full
per-tool table is enumerated when the FR-4 eval cases are written. Verb allowlist already gates which
tools can run (spec FR-4 envelope (b): pytest, ruff, mypy, make, uv, npm, tsc, cargo).

---

## OQ-M10 — Input-hash artifact exclude set

**Classification: [RESOLVED] — FR-4.8's concern is REAL; the exclude-glob set is determinable now.**
[CODE-VERIFIED against §4.0.]

**The concern is real (CODE-VERIFIED).** §4.0 Step 0.4 (SKILL.md:174) constructs the input tree as,
for UC-2 work-unit inputs, **"every file under that directory tree (`find <work-unit-dir> -type f`)"**
— an unfiltered `find -type f`. SKILL.md:193 then re-reads and recomputes `input_tree_sha256`
**"Before Wave 5 synthesis AND at Wave 7 step 7.2"**; if it differs ("any file added, removed,
modified, or renamed"), the run **STOPs with `input_drift` flag** → `status: partial`.

A verification command run at the new §6.1 step 5.5 (FR-4) executes inside / adjacent to the
work-unit subtree. Tools like `pytest` emit `.pytest_cache/`, `__pycache__/`, `*.pyc`, `.coverage`
**into the input tree**. The unfiltered `find -type f` at the Wave-5 recompute WILL pick these up as
"added files" → `input_tree_sha256` changes → spurious `input_drift` STOP. **This is exactly the
M-COR2 hazard (spec risk line 443).** The concern is confirmed real against the live §4.0 construction.

**Exact exclude-glob set needed (per spec OQ-M10 line 532 + FR-4.8 line 257):**

```
__pycache__/        *.pyc           *.pyo           *.pyd
.pytest_cache/      .coverage       .coverage.*     htmlcov/
.mypy_cache/        .ruff_cache/
node_modules/.cache/   .tsbuildinfo
target/             # cargo/rust build artifacts
.hypothesis/        # pytest-hypothesis DB
*.egg-info/         __pycache__ (nested)
```

The spec's OQ-M10 enumeration (line 532) names: `__pycache__`, `.pytest_cache`, `.coverage`,
`*.pyc`, `node_modules/.cache`, `.mypy_cache`, `target/`. FR-4.8 (line 257) names the eval-asserted
subset `__pycache__`, `.pytest_cache`, `.coverage`, `*.pyc`. The list above is the union plus the
adjacent artifacts the verb-allowlist tools (`ruff`→`.ruff_cache`, `tsc`→`.tsbuildinfo`,
hypothesis→`.hypothesis`) emit.

**Where the exclude must be applied:** the `find <work-unit-dir> -type f` in SKILL.md:174 AND the
Wave-5/Wave-7 recompute in SKILL.md:193 must BOTH apply the same exclude set (a `-prune`/glob filter),
or the snapshot and recompute will disagree even without a real edit. FR-4.8 should edit §4.0 to
introduce a named `VERIFICATION_ARTIFACT_EXCLUDES` glob set applied consistently at both
construction (line 174) and recompute (line 193).

**Action for task-file:** FR-4.8 edits SKILL.md §4.0 (lines 174 + 193) to apply the exclude-glob set
above at BOTH input-tree construction and the Wave-5/Wave-7 recompute. Eval: a fixture whose tests
emit cache artifacts must NOT trip `input_drift`/STOP (FR-4.8 acceptance, line 257).

---

## §9.3 Consumer Field Map — `regression_present` load-bearing confirmation

**Classification: [RESOLVED / CODE-VERIFIED] — `regression_present` is ALREADY a load-bearing
consumer field; FR-4 tightens its SOURCE without a contract break.**

§9.3 Consumer Field Map (SKILL.md:620-636). The relevant row, quoted verbatim (SKILL.md:626):

> | **`sc-troubleshoot-protocol` Wave 6 (Phase B/D)** | Skill-to-skill invocation | `status`,
> `tier_reached`, `confidence_calibrated`, **`regression_present`**, `needs_human_decision` |
> `status: failed` halts troubleshoot; **`regression_present: true` forces Tier-3 troubleshoot
> path**; `needs_human_decision: true` surfaces to user before continuing. |

`regression_present` is also load-bearing in:
- the §14.5.2 condition-4 promotion gate (SKILL.md:1097, the false-PASS path FR-4 closes),
- `sc-task-protocol` end-of-task (`deviation_count_by_class.regression`, SKILL.md:628),
- `superclaude sprint run` TurnLedger (`deviation_class == regression` → rollback, SKILL.md:627),
- and the §12.5 falsifier assertion (SKILL.md:959-960,1502).

**Why this is a non-breaking tightening (CODE-VERIFIED):** FR-4 does NOT add `regression_present` to a
consumer's load-bearing row (it is already there) and does NOT change its type (`bool`, SKILL.md:557).
FR-4 only changes the **evidence that SETS it**: today §10.4 sets it from "task log or `--rerun-tests`"
(SKILL.md:725); FR-4 makes a Regression-classified non-zero `execute_shell_command` exit
(`verification_regressions_detected ≥ 1`) an additional, default-on source. Per §9.3's own rule
(SKILL.md:622) "adding a field to a consumer's load-bearing row requires a contract version bump" — FR-4
adds NO field to that row, so **no §9.3 table edit is forced and no contract break occurs.** The new
`verification_*` scalars are additive §9.1/§9.2 fields (minor bump, already covered by the low-spec's
1.1.0 → medium's 1.2.0 per OQ-M6).

**Action for task-file:** FR-4 wires `verification_regressions_detected ≥ 1` → `regression_present:
true` as a NEW source for the EXISTING field; no §9.3 row edit; confirm the §10.4 detector and §14.5.2
condition-4 gate read the tightened source. This is the C2 false-PASS closure (spec line 70,249).

---

## SUMMARY TABLE — OQ classifications + actions

| OQ-id | Classification | Evidence | Action-for-task-file |
|-------|----------------|----------|----------------------|
| **OQ-M5** (cross-spec FR-7) | **[RESOLVED]** — consume FR-7; one derivation gap (`read_only`) | low-spec task BUILT (task:160,164-180) [CODE-VERIFIED]; live `get_current_config` shows backend/tools/version but NOT `read_only` [CODE-VERIFIED] | Consume low-spec FR-7 `serena_config_snapshot_path`; derive `backend`/`execute_shell_command_available`/`onboarding_available` via parse+membership. **`read_only` is NOT in FR-7 — medium FR-4 must add a project-config `read_only` read.** Inline-probe fallback if low-spec unmerged. |
| **OQ-M8** (contract location) | **[RESOLVED]** — inline SKILL.md §9, no YAML | `ls refs/` = 11 files, no `return-contract.yaml` [CODE-VERIFIED]; §9.1@491, §9.2@601 | Route all contract/telemetry edits to SKILL.md §9 inline; STRIKE the `return-contract.yaml` matrix row (spec:294). |
| **OQ-M1** (`prepare_for_new_conversation` sig) | **[RUNTIME-PROBE-REQUIRED]** — tool ABSENT here | not in active OR available tool lists in live probe [CODE-VERIFIED absent]; not in MCP surface | Keep as FR-3 merge-precondition runtime probe; wire `write_memory` fallback as default; no assumed params; FR-3 ships LAST. |
| **OQ-M3** (LSP `type_hierarchy`) | **[RUNTIME-PROBE-REQUIRED]** — LSP has NO tool here (strong negative) | live LSP backend: only `jet_brains_type_hierarchy` present, no LSP `type_hierarchy` [CODE-VERIFIED]; corroborates "JetBrains-only", contradicts README "LSP yes" | FR-1 `--with-hierarchy` default-OFF on `lsp`, unavailable on `none`; gate on Wave-0 `backend`; empirical Py/Java/TS probe in eval-authoring. |
| **OQ-M2** (timeout + flag migration) | **[RESOLVED]** (migration surface small) + **[DECISION-DEFERRED]** (timeout) | `grep rerun-tests` = 1 hit only @ SKILL.md:725 [CODE-VERIFIED] | Update the single SKILL.md:725 sentence; `--rerun-tests` → deprecated alias + WARN; `--no-verify` opt-out; hard-code consumer-side `timeout 120` (max 600). |
| **OQ-M9** (exit-code taxonomy) | **[DECISION-DEFERRED]** (full table) — FR-4 defaults CONSISTENT with §10.4 | §10.4 Regression signal SKILL.md:725 ≡ pytest-exit-1 mapping [CODE-VERIFIED consistent] | FR-4 default table consistent; unmapped exit → Grounding Gap (conservative); enumerate make/cargo/npm/tsc in eval-authoring. |
| **OQ-M10** (input-hash excludes) | **[RESOLVED]** — concern REAL; glob set determinable now | §4.0 uses unfiltered `find -type f` @ SKILL.md:174; recompute+STOP @ :193 [CODE-VERIFIED] | FR-4.8 adds `VERIFICATION_ARTIFACT_EXCLUDES` glob set (`__pycache__/`,`*.pyc`,`.pytest_cache/`,`.coverage*`,`.mypy_cache/`,`.ruff_cache/`,`node_modules/.cache/`,`target/`,`.hypothesis/`,`.tsbuildinfo`) applied at BOTH :174 construction and :193 recompute. |
| **§9.3** (`regression_present`) | **[RESOLVED / CODE-VERIFIED]** — already load-bearing; FR-4 tightens source, no break | SKILL.md:626 row (sc-troubleshoot Wave 6) lists `regression_present` [CODE-VERIFIED]; type unchanged @ :557 | FR-4 wires `verification_regressions_detected ≥ 1` → existing `regression_present`; NO §9.3 row edit; no contract break. |

### Cross-cutting notes for task-builder

- **Doc claims checked:** spec §4.5 inline-probe contract [CODE-VERIFIED]; spec line 294 `return-contract.yaml` row [CODE-CONTRADICTED — file absent]; spec "JetBrains-only `type_hierarchy`" [CODE-VERIFIED on live LSP]; spec FR-4 exit-code/§10.4 consistency [CODE-VERIFIED]; spec OQ-M10 `find -type f` hazard [CODE-VERIFIED].
- **One genuinely-new probe surface beyond FR-7:** `read_only` (FR-7's `get_current_config` does NOT emit it). Every other medium Wave-0 field is derivable from FR-7. This is the single most actionable cross-spec finding.
- **Ship order (spec §4.6, reverse of FR numbering):** FR-4 first (largest; verification triangle), then FR-2/FR-6-pair already in low-spec, then FR-3 (signature OQ-M1), FR-1 (`type_hierarchy`) LAST (highest backend risk).

---

**Status: Complete**
