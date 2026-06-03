# Research: Skill Insertion Points

- Topic type: File Inventory + precise anchors
- Scope: src/superclaude/skills/sc-reflect-protocol/SKILL.md
- Status: Complete
- Date: 2026-06-02
- SKILL.md total length: **1585 lines** (verified `wc -l`)

---

## DRIFT SUMMARY (spec line refs vs. verified current lines)

The spec (`05-spec-medium-complexity.md`) was written earlier; lines have drifted. Verified status of every spec-cited anchor:

| Spec citation | Spec line | Verified line | Status |
|---|---|---|---|
| §6.1 chain | 354-367 | header **354**, chain block **358-365** (numbered 1-6 at **359-364**) | ACCURATE (header+range) |
| `find_referencing_symbols` step 4 | 362 | **362** | ACCURATE |
| `get_diagnostics_for_file` step 5 | 363 | **363** | ACCURATE |
| re-Read step 6 | 364 | **364** | ACCURATE |
| §6.2 re-Read | 369-371 | **369-371** | ACCURATE |
| §6.3 memory persist | 373-383 | **373-383** | ACCURATE |
| §6.5 fail-open | 397-399 | **397-399** | ACCURATE |
| Wave 0 step list | 127-135 | **127-135** | ACCURATE |
| §4.0 detail | 172-225 | **172-225** | ACCURATE |
| Wave 1B.3 | 233-241 | **233-241** | ACCURATE |
| §10.4 Regression | 718-730 | **718-730** | ACCURATE |
| `--rerun-tests` line | 725 | **725** | ACCURATE |
| §14.5.2 gate | 1090-1112 | **1090-1112** | ACCURATE |
| cond 4 (regression==0) | 1097 | **1097** | ACCURATE |
| `regression_present` field | 557 | **557** | ACCURATE |
| §7 task-builder row | 417 | **417** | ACCURATE |
| §8 task-builder row | 458 | **458** | ACCURATE |
| §14 write_memory fail row | 1067 | **1067** | ACCURATE |
| §9.1 contract block | n/a | **491-597** (header 491) | reference |
| §9.2 telemetry | n/a | **601-618** (header 601) | reference |
| `allowed-tools` frontmatter | "~1-60" | **line 5 (single line)** | [CODE-CONTRADICTED] — it is ONE line (5), not a multi-line block in 1-60 |
| `input_tree_sha256` recompute | 174,193 | recompute at **193**; legacy field **194-195** | 193 ACCURATE; 174 is the §4.0 intro para (not the recompute) |

**Net finding:** Nearly all spec line refs are ACCURATE. The single contradiction is the `allowed-tools` shape — it is a single comma-separated line (line 5), NOT a multi-line YAML list across lines 1-60.

---

## SHARED ANCHOR A: Frontmatter `allowed-tools` (line 5) — used by ALL 4 FRs

The builder must add 4 new tools (`type_hierarchy`, `onboarding`, `prepare_for_new_conversation`, `execute_shell_command`) to a **single comma-separated line**, NOT a YAML list. Current verbatim (line 5):

```
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
```

The four additions are `mcp__serena__type_hierarchy`, `mcp__serena__onboarding`, `mcp__serena__prepare_for_new_conversation`, `mcp__serena__execute_shell_command`. Edit target: append to the end of line 5 after `...mcp__sequential-thinking__sequentialthinking`. **Note**: each FR ships as a separate PR, so the builder should plan a single line-5 edit per FR (each appending its own one tool), OR one combined edit — confirm with the per-FR ship order (4→2→3→1).

---

## SHARED ANCHOR B: §6.1 evidence chain (lines 354-367) — FR-1 step 4.5 AND FR-4 step 5.5 both insert here

Both FR-1 (step 4.5) and FR-4 (step 5.5) edit the SAME fenced code block (lines 358-365). Builder must coordinate: two insertions into one ``` block. Verbatim current block:

```
354:### 6.1 Mandatory evidence-gathering chain (Wave 1A)
355:
356:For every touched file in UC-2, or every spec-referenced module in UC-1:
357:
358:```
359:1. mcp__serena__activate_project (once, idempotent at Wave 0)
360:2. mcp__serena__get_symbols_overview <file>            # structural map
361:3. mcp__serena__find_symbol <relevant-symbol>          # symbol body
362:4. mcp__serena__find_referencing_symbols <symbol>      # downstream impact
363:5. mcp__serena__get_diagnostics_for_file <file>        # LSP-level issues
364:6. Re-Read each cited file:line range before quoting    # citation-grounding
365:```
366:
367:The chain replaces "think_about_collected_information" ...
```

- **FR-1 step 4.5** inserts BETWEEN line 362 (step 4) and line 363 (step 5) → new `4.5 mcp__serena__type_hierarchy(...)` line.
- **FR-4 step 5.5** inserts BETWEEN line 363 (step 5) and line 364 (step 6) → new `5.5 mcp__serena__execute_shell_command (scoped verify)` line + envelope note.
- Both also need accompanying prose paragraphs (gating conditions, safety envelope) added after line 367 / in new sub-sections per the spec's §2.2 insertion map.

---

## FR-RV3-MED.1: type_hierarchy — TWO insertion points

### Insertion 1A — §6.1 step 4.5 (between line 362 and 363)
See SHARED ANCHOR B above. Insert a new numbered step `4.5 mcp__serena__type_hierarchy(hierarchy_type=both|subtypes, depth=0)` after line 362, before line 363. Gated on: Wave 0 backend probe = hierarchy-capable AND `--with-hierarchy` AND located symbol is a type (FR-1.1/1.4). Per spec §2.2 map (spec lines 116-117).

### Insertion 1B — Wave 1B.3 (lines 233-241)
Verbatim current Wave 1B.3 (the cross-task interaction-effects scan numbered list):

```
233:**Step 1B.3 (cross-task interaction-effects scan, UC-2 tasklist-scope only).** When mode is UC-2 AND the tasklist contains ≥3 completed tasks, run the symbol-overlap scan:
234:
235:1. For each task in the tasklist, derive its touched symbols via `mcp__serena__find_symbol` against the task's diff hunks.
236:2. Build a symbol-overlap graph: nodes = symbols, edges = "touched by task X and task Y." Cap at top-30 most-touched symbols (heuristic; full enumeration is bounded at 30 to control cost).
237:3. For each overlap edge, query `mcp__serena__find_referencing_symbols` to determine whether the symbol is genuinely shared or just transiently named the same.
238:4. For each confirmed interaction, check whether either task description explicitly cites the other (textual match on task ID). If neither cites the other, **flag as a cross-task interaction risk**.
239:5. Each risk becomes a synthetic invariant probe entry tagged `category: cross_task` ... Severity scales with the symbol's call-site count: HIGH if >5 referencing call sites, MEDIUM if 2-5, LOW if 1.
241:Emit `interaction_effects_scanned: true` in the contract when this step runs ...
```

FR-1.6 insertion: add a `type_hierarchy(subtypes)` lineage-confirm step. Natural anchor = **after step 3 (line 237, the `find_referencing_symbols` shared/collision check)** — the spec wants "shared base-class hotspot flagged HIGH only after type_hierarchy(subtypes) confirms genuine shared lineage (not a name collision)." This refines step 3's name-collision check. Builder inserts either as a new sub-step 3.5 or augments step 3/4. Lines 237-238 are the precise neighborhood.

### FR-1 contract/telemetry field landing
- Contract (UC-1 block, §9.1): `hierarchy_slice_path`, `hierarchy_coverage_pct` → insert in the `# UC-1 specific` block at **lines 503-507** (after `best_practice_grade` line 507).
- Telemetry (§9.2, lines 603-618): `type_hierarchy_invoked`, `hierarchy_backend`, `hierarchy_nodes_examined`, `hierarchy_gaps_found`.

---

## FR-RV3-MED.2: onboarding — Wave 0 step 0.7b

### Insertion 2A — Wave 0 step list (lines 127-135, the ``` block)
Verbatim current Wave 0 ordered step block:

```
127:Wave 0:   Parse + Validate Input + Activate Project + Memory Hydrate
128:            0.1 Parse flags + apply §3.2 mode-selection
129:            0.2 Validate input paths (Read existence)
130:            0.3 Probe sc-adversarial-protocol installation (see §14)
131:            0.4 Compute input_sha256 snapshot (see §4.0 — Change #10)
132:            0.5 Resolve env-var aliases + apply 0/1/2/3+ alias routing table (Change #13/#14)
133:            0.6 Inspect vendor heterogeneity (Change #18 — warn-only)
134:            0.7 Activate Serena project + memory hydrate
135:            0.8 Open audit log + machine-readable header
```

FR-2 inserts new `0.7b onboarding bootstrap` line **between line 134 (0.7) and line 135 (0.8)**. (Spec §2.2 map also references a `0.5c get_current_config` probe from low-spec FR-7 — that is the low-spec's concern / cross-spec dependency; FR-2 itself only adds 0.7b here.)

### Insertion 2B — §4.0 detailed step additions (lines 172-225)
§4.0 ("Wave 0 — Detailed step additions") is the prose home for each Wave 0 sub-step. Current sub-step detail paragraphs present: Step 0.4 (174-195), Step 0.5 (197-211), Step 0.6 (213), Step 0.9 (215-225). **There is NO detailed paragraph for step 0.7 currently** (memory hydrate detail lives in §6.3). FR-2 adds a new **"Step 0.7b (onboarding bootstrap)" detail paragraph**. Cleanest landing = after the Step 0.6 paragraph (line 213) and before Step 0.9 (line 215), OR after the whole §4.0 block (before §4.1 header at line 227). Recommend: insert a new paragraph after line 213 (Step 0.6) to keep step ordering, OR at end of §4.0 (after line 225, before 227). The §4.0 section ends at line 225; §4.1 header begins at 227.

### FR-2 contract/telemetry field landing
- Contract: `onboarding_ran` (top-level). Natural landing near the input-integrity / status block; spec says "top-level." Builder candidate: after line 502 (`escalation_rule_matched`) or within a Wave-0 sub-block. NOTE: there is no existing dedicated Wave-0 contract sub-block; builder should add `onboarding_ran` near the top stable fields (around lines 500-502).
- Telemetry (§9.2): `onboarding_succeeded`, `onboarding_memories_count`, `onboarding_skipped_reason` → insert in §9.2 block (lines 603-618), e.g. after `memory_misses` (line 617).

### FR-2 fail-open / WARN
§6.5 fail-open (397-399) governs; no new error-matrix row strictly required, but a WARN catalog entry (context-excluded) goes to `refs/ops-integration.md` (other researcher's scope: 03/patterns).

---

## FR-RV3-MED.3: prepare_for_new_conversation — Wave 5/6 handoff

### Insertion 3A — §6.3 memory pattern (lines 373-383)
Verbatim §6.3 block:

```
373:### 6.3 Memory pattern (per-project, expiring)
374:
375:```
376:mcp__serena__read_memory  key=reflect/last-pass-{project-slug}      # Wave 0 hydrate
377:mcp__serena__read_memory  key=reflect/deviation-patterns-{slug}     # Wave 1 (recurring deviation signals)
378:mcp__serena__write_memory key=reflect/last-pass-{slug} value=<summary>  # Wave 5 persist
379:mcp__serena__write_memory key=reflect/deviation-patterns-{slug} value=<merged>  # Wave 5 persist
380:mcp__serena__list_memories                                          # Wave 0 inventory
381:```
382:
383:Retention rule: keep last 20 entries per key; expire >90 days. Project slug derived from `pwd` basename.
```

FR-3 adds the `reflect/handoff-{slug}-{timestamp}` schema. Insert a new line inside the ``` block (after line 379, before line 380) for the handoff write, AND/OR a new prose paragraph after line 383 defining the schema + Wave 6 timing. The retention note at line 383 is also where FR-3.7 (M-ARC2) prefix-extension to `reflect/handoff-*` is conceptually anchored (though the actual sweep lives in the low-spec).

### Insertion 3B — Wave 6 task-builder handoff (§7 line 417 + §8 line 458)
The Wave 6 task-builder invocation is referenced in two delegation tables:

- §7 Agent Delegation Map, line **417**: `| task-builder (skill, not agent) | 6 | UC-2 (post-execution remediation) | Generate corrective MDTM task file from reflection findings | None; surface findings without remediation |`
- §8 Cross-Skill Integration, line **458**: `| task-builder | Wave 6 (T3 only) | Generate corrective MDTM task file from reflection findings; gated on user opt-in. |`

FR-3 requires `prepare_for_new_conversation` to fire **BEFORE** the task-builder invoke (FR-3.1). These two table rows are reference anchors; the actual "write handoff before invoke" wiring needs a prose step. There is NO standalone Wave 6 detail section in §4.x currently (Wave 5 detail is §4.5 at line 249; Waves 6/7 have no §4.6). Builder candidate: add a §4.6 Wave 6 detail subsection (after §4.5 line 257, before §5 header at 261) OR extend the §8 row note. Recommend a new §4.6 paragraph.

### Insertion 3C — §14 error matrix write_memory fallback row (line 1067)
Verbatim current row (line 1067):

```
| Serena `write_memory` fails at Wave 5 (disk full, permission denied, serena down) | Continue: report still ships; emit `memory_persist_failed: true` in telemetry; emit WARN: `"deviation-pattern memory not persisted — next reflect run will not benefit from this run's findings."` Memory persistence is best-effort. | None |
```

FR-3.3 extends this row (or adds an adjacent row) to cover the `prepare_for_new_conversation` context-excluded → `write_memory` fallback path. The §14 error matrix is a markdown table; rows run ~1037-1074. Insert a new row adjacent to line 1067, OR amend 1067 to reference the handoff fallback.

### FR-3 contract/telemetry field landing
- Contract (§9.1 Tier 3 block, lines 550-553): `handoff_memory_key` → insert after `task_file_path` (line 553).
- Telemetry (§9.2): `handoff_memory_written`, `handoff_payload_size_bytes`, `handoff_persist_method`, `handoff_persist_failed`.

---

## FR-RV3-MED.4: execute_shell_command — §6.1 step 5.5 + §10.4 + §14.5.2

### Insertion 4A — §6.1 step 5.5 (between line 363 and 364)
See SHARED ANCHOR B. Insert new numbered step `5.5 mcp__serena__execute_shell_command (scoped verify)` after line 363 (step 5 `get_diagnostics_for_file`), before line 364 (step 6 re-Read). Plus the large safety-envelope prose (verb allowlist, metachar rejection, timeout, output cap, cwd scoping, audit) — that prose lands as a new sub-section after §6.1 (after line 367, before §6.2 header at 369) OR as an expanded §6.1 block.

### Insertion 4B — §10.4 Regression detection signals (lines 718-730)
Verbatim §10.4 detection signals (the `--rerun-tests` line is the surgical target):

```
718:### 10.4 Regression
719:
720:**Definition.** A change that *contradicts* an acceptance criterion ...
721:
722:**Detection signals.**
723:
724:- Diff hunk contradicts a spec acceptance criterion (textual contradiction or behavioral contradiction surfaced by `get_diagnostics_for_file`).
725:- A test that previously passed now fails after the diff (detect via task log or by re-running tests if `--rerun-tests` set).
726:- A documented invariant in the spec or in a `@invariant` comment is violated.
727:
728:**Gold-standard reference.** Spec acceptance-criteria section + test-suite state pre/post (from task log or re-run) + invariant comments.
730:**Default remediation.** This is the only class that *unconditionally* triggers a Tier 3 remediation offer ...
```

FR-4 replaces the opt-in `--rerun-tests` semantics at **line 725** with default-on verification feeding `verification_regressions_detected`. Surgical Edit target = line 725 (rewrite to reference default-on `execute_shell_command` verification + `--no-verify` opt-out + exit-code taxonomy). Gold-standard ref at line 728 may also need updating ("re-run" → "verified test-suite state").

### Insertion 4C — §14.5.2 promotion gate condition 4 (line 1097)
Verbatim condition 4 (line 1097):

```
4. **`deviation_count_by_class.drift == 0` AND `deviation_count_by_class.regression == 0`** — Authorized expansion and Necessary deviation are non-blocking; Drift and Regression block. **Exception**: if the only Drift signal is the frontmatter-mismatch from condition 5b AND that mismatch is classifiable as §10.2 Necessary deviation ... it is NOT counted as Drift here — but condition 5b still independently gates promotion. *(maps to `gate_evaluation.no_drift_no_regression`)*
```

FR-4 does NOT change condition 4's text — it **feeds** it. `verification_regressions_detected > 0 → regression_present: true → deviation_count_by_class.regression ≥ 1` which condition 4 already blocks on. So FR-4's relationship to line 1097 is "supply a verified source"; no Edit to 1097 strictly required, though a clarifying note may be added. The load-bearing wiring is that `regression_present` (line 557) gets a verified source.

### Insertion 4D — `regression_present` field (line 557)
Verbatim (line 557, inside the §9.1 "Asymmetric-cost flags" block at 555-562):

```
555:# Asymmetric-cost flags (downstream automation must respect these)
556:cannot_validate_without_user_input: bool
557:regression_present: bool
558:unauthorized_deviation_present: bool
```

`regression_present` is an EXISTING field (line 557). FR-4 makes it verified-sourced. The NEW FR-4 contract fields (`verification_ran`, `verification_invocations`, `verification_failures`, `verification_regressions_detected`, `verification_skip_reason`) land in the §9.1 UC-2 block — natural anchor is after the `deviation_count_by_class` / `grounding_gaps_path` block (lines 509-517) OR adjacent to the asymmetric-cost flags (555-562). Recommend a new `# Verification triangle (FR-4)` sub-block inserted after line 517 (end of `# UC-2 specific` block) or after line 562.

### Insertion 4E — input-hash artifact exclusion (FR-4.8, line 193)
Verbatim (line 193):

```
193:Before Wave 5 synthesis AND at Wave 7 step 7.2 (pre-mutation), re-read the input tree and recompute `input_tree_sha256`. If it differs (any file added, removed, modified, or renamed), STOP with `input_drift` flag, emit BOTH SHAs and the per-file diff into the return contract, and route to `status: partial`.
```

FR-4.8 (M-COR2) requires build/test artifacts (`__pycache__`, `.pytest_cache`, `.coverage`, `*.pyc`) be EXCLUDED from this recompute so a successful verify does not trip `input_drift_detected`. Edit target = line 193 (add an exclusion clause), and/or the file-list construction at lines 178-181 (the tree-hash definition):

```
178:```
179:file_list = sorted([(relative_path, sha256(read(absolute_path))) for path in input_tree])
180:input_tree_sha256 = sha256(serialize_as_json(file_list))    # canonical serialization for reproducibility
181:```
```

Recommend adding an ignore-glob to the `input_tree` construction (around 178-181) AND a note at 193.

### FR-4 telemetry (§9.2, 603-618)
`verify_timeout_hit`, `verify_flaky_suspected`, `verify_timeout_default`, `verify_invocations_path`, `verify_blocked`, `verify_blocked_reason`.

### FR-4 fail-open
§6.5 (397-399) + §14 error matrix. A new error-matrix row for "verification tool unavailable / read_only" may be added near line 1042 (Serena unavailable row) — though FR-4.4/4.7 mostly degrade within step 5.5 itself.

---

## SUMMARY — FR → verified insertion anchor map

All line numbers re-verified against current SKILL.md (1585 lines, 2026-06-02). Spec citations were almost entirely ACCURATE; only `allowed-tools` shape was [CODE-CONTRADICTED].

| FR | Primary anchor (verified line) | Secondary anchor(s) | Contract/telemetry landing |
|---|---|---|---|
| **Shared** | `allowed-tools` **line 5** (single comma-sep line, NOT lines 1-60) | — | add 4 tools to line 5 |
| **FR-1** type_hierarchy | §6.1 step 4.5 — insert between **line 362** (step 4) and **363** (step 5) in the fenced block 358-365 | Wave 1B.3 lineage step — after **line 237** (find_referencing_symbols step 3) within 233-241 | UC-1 block **503-507** (`hierarchy_slice_path`, `hierarchy_coverage_pct`); telemetry **603-618** |
| **FR-2** onboarding | Wave 0 step 0.7b — insert between **line 134** (0.7) and **135** (0.8) in fenced block 127-135 | §4.0 detail paragraph — after Step 0.6 (**line 213**) OR end of §4.0 (**after 225**, before §4.1 at 227) | `onboarding_ran` near top stable fields (~500-502); telemetry **603-618** |
| **FR-3** prepare_for_new_conversation | §6.3 handoff schema — insert in fenced block after **line 379**, + prose after **383** | Wave 6 invoke: §7 row **line 417**, §8 row **line 458** (add new §4.6 detail after §4.5 line 257); §14 fallback row at/adjacent **line 1067** | Tier 3 block **550-553** (`handoff_memory_key` after line 553); telemetry **603-618** |
| **FR-4** execute_shell_command | §6.1 step 5.5 — insert between **line 363** (step 5) and **364** (step 6) in fenced block 358-365 | §10.4 — rewrite `--rerun-tests` at **line 725** (+ gold-std ref 728); input-hash exclusion at **line 193** + tree-hash def **178-181**; §14.5.2 cond 4 **line 1097** (feeds, no edit needed) | `regression_present` EXISTS at **line 557**; new verify fields after UC-2 block (**line 517**) or near 562; telemetry **603-618** |

### Key builder coordination notes
1. **§6.1 fenced block (358-365) receives TWO insertions** (FR-1 step 4.5 + FR-4 step 5.5) — if FRs ship as separate PRs (order 4→2→3→1), FR-4 lands step 5.5 first, then FR-1 lands step 4.5 into the already-modified block. Builder must re-verify line numbers after each PR.
2. **`allowed-tools` line 5 receives a one-tool append per FR** (4 separate PRs) OR one combined edit.
3. **No §4.6 Wave 6 detail section exists** — FR-3 likely needs to create one (after §4.5 at line 257, before §5 at line 261).
4. **No §4.0 Step 0.7 detail paragraph exists** — FR-2 adds the first 0.7-family detail paragraph.
5. **§14.5.2 condition 4 (line 1097) needs NO text edit for FR-4** — it already blocks on `regression == 0`; FR-4 only supplies a verified source via `regression_present` (line 557) ← `verification_regressions_detected`.
6. Per-step audit-row schema is fixed at **line 124** (`{wave, step, timestamp, outcome, evidence_ref}`) — FR-4 per-invocation data must go to `<output>/verify-logs/invocations.yaml` referenced via `evidence_ref`, NOT inlined (M-ARC1).

### refs/* edits (other researchers' scope — 03)
FR-1/3/4 also touch `refs/reflection-rubric.md`, `refs/deviation-taxonomy.md`, `refs/reviewer-spec.md` (cites SKILL.md:245 = §4.3 step 3B.0, verified at **line 245**), `refs/ops-integration.md`, optional `refs/return-contract.yaml`. Out of THIS track's scope; flagged for cross-track stitch.
