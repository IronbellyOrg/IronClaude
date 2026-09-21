# 07 — Gap-Fill Reconcile (Round 3 of 3)

**Status:** Complete
**Date:** 2026-09-19
**Authority:** This file SUPERSEDES `07-gap-fill-decisions.md` and `07-gap-fill-test-harness.md` wherever they conflict. Where it is silent, those two files stand as written (pointers in §Z). The builder reads THIS file first; it is the single decision surface for task-file synthesis.
**Inputs:** `../qa/analyst-gap-closure-round2-report.md` (OPEN list, X-1..X-5, X-12), `../qa/qa-research-evidence-round2-report.md` (rows 1.3, 1.4, 1.8), the two 07 files, v2 R-01/R-03/R-04/R-06/R-09/R-10/R-14 (`merged-report-v2.md:208-231, 249-308, 346-355, 399-420, 422-431, 463-471`), repo re-reads listed per item. All repo line numbers re-read 2026-09-19 in this pass.

Abbreviations: `SKILL` = `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`; `da` = `refs/diagnosability-audit.md`; `RT` = `refs/report-template.md`; `HCT` = `refs/hypothesis-card-template.md`; `CAL` = `src/superclaude/agents/confidence-calibrator.md`; `VAL` = `src/superclaude/agents/evidence-validator.md`; `harness` = `07-gap-fill-test-harness.md`; `D<n>` = `07-gap-fill-decisions.md` item.

---

## X-1 — C6 flag name: `bracket_unproven` — DECISION

One name, everywhere: **`bracket_unproven`**. The harness is canonical because T2 (`C6 ⇒ cap==0.3`), the C6 fixtures (`expected_flags: [bracket_unproven, uncited]`, harness §4.3 :1637-1700) and T13 execute it. D13's `bracket_uncited` is withdrawn. Sites that carry the name: the §X-3 table (ref), the two agents and the SKILL fallback lines (cite the ref, §X-3), `tests/troubleshoot/_assertions.py` `FLAGS["C6"].flag == "bracket_unproven"`, and every C6 pos fixture.

## X-2 — C6 severity: calibrated cap 0.3 — DECISION

Adopt the harness reading (harness §1.2 I-9 resolution; `CAL:55` names six dimensions, none is "evidence quality"; `RUB:20` untouched per R-14 Must-NOT). C6 is a **calibrated-output cap of 0.3** applied after the formula, exactly like C7/C8's 0.5 cap (`CalibratorResult.cap = min(caps fired)`). It is NOT a dimension override. D13's "Evidence grounding := 0.0 (nearest legal value ≤0.3; 03 I-9)" cell is withdrawn. Corrected row (also present verbatim in the §X-3 table):

```markdown
| C6 | numeric threshold or bracket asserted in the headline without a bracket= line in bracket.md | `bracket_unproven` | calibrated ≤ 0.3 (cap, applied after the formula) |
```

## X-3 — Canonical assertion table (`refs/agent-assertions.md`) — DECISION

**Canonical trigger text = harness §1.2 trigger column**, regenerated below with columns `id | trigger | flag | severity`. **No cell contains a `|` character** (checked by eye and by the T13 `ROW` regex, which uses `[^|]+?` for the trigger cell). The builder copies the trigger column of THIS table into `_assertions.FLAGS[*].trigger` from the same clipboard; T13 assertion 1 compares `(id, trigger, flag)` byte-identical after `str.strip()`.

**Where it lands:**
- `refs/agent-assertions.md` — the table below, verbatim, inside the D13 skeleton (replace D13's two tables with this single one; keep D13's lead paragraph, `## Output shape`, and `## Loading discipline` footer).
- `VAL` responsibility 2b and `CAL` step 5b — **the single cite line** `See refs/agent-assertions.md (passed as assertions_path).` — NOT a copy. T13 accepts a cite (`CITE = re.compile(r"refs/agent-assertions\.md")`). A verbatim copy is permitted but must be byte-identical; a copy is drift bait, so the default is the cite.
- `SKILL:282` and `SKILL:452` fallback bullets — cite line (§X-4 gives the appended sentences). T13 assertion 3 ("name coverage") is satisfied by the cite.

```markdown
| id | trigger | flag | severity |
|---|---|---|---|
| A1 | definite enum token in Summary/Diagnosis and (max calibrated < 0.50 or token in Grounding Gaps with unobserved/deduced/pending or token absent from every artifact and job-*.log) | `deduced_headline` | partial |
| A2 | diff touches a collector or invocation site and no falsifier sentence names a row | `instrumentation_without_falsifier` | partial |
| A3 | Timestamp/Date/pushed_at later than artifact mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop that line |
| A4 | pipeline_hardening_verdict not in {pass, blocked, advisory, not_applicable, blocked-on-authorization} | `verdict_not_in_contract` | partial |
| A5 | candidate-fixes.md says consensus and adversarial_invoked is false and a card with evidence_class in {source_static, doc_static, none} makes a dynamic claim | `consensus_on_unobserved` | partial |
| A6 | Reference-context value is not a single literal (matches if, only, /, or comma) | `reference_value_not_literal` | FAIL |
| A7 | RUN-SITE is pending-producers at finalize while producers.md has at least one producer row | `run_site_unresolved` | FAIL |
| A8 | OBSERVE-VIA is artifact-file and no job-*.log exists for the failing arm at finalize | `ci_verdict_unobserved` | status blocked; Diagnosis begins UNDETERMINED — CI verdict unobserved |
| A9 | Reference-context value differs from the value observed in the reference context | `probe_suspect` | probe row suspect; Grounding Gap; outcome table skipped (no status change) |
| A10 | capability-verdict is blocked without an Emitter search block recording emitters-found: 0 and already-read-files: 0 | `capability_block_unproven` | partial |
| C1 | headline enum token and calibrated < 0.50 | `headline_definite_low_confidence` | verdict forced ESCALATE |
| C2 | card excludes an enum without a file:line for that enum's exit statement | `unproven_exclusion:<token>` | Runtime check := 0.0 |
| C3 | control arm cited without CONTROL-PROOF: yes | `control_unproven` | Symptom coverage ≤ 0.5 |
| C3b | runs-in is unknown | `locus_unknown` | Runtime check ≤ 0.5 |
| C4 | instrumentation row without both falsifier values | `no_prereg_falsifier` | Fix directness ≤ 0.5 |
| C5 | Timestamp later than card_mtime + 5 min or equal to T00:00:00Z | `timestamp_invalid` | drop that line; timestamp not load-bearing |
| C6 | numeric threshold or bracket asserted in the headline without a bracket= line in bracket.md | `bracket_unproven` | calibrated ≤ 0.3 (cap, applied after the formula) |
| C7 | card names an environment property without citing a 2x2 row | `uncited` | calibrated ≤ 0.5 (cap) |
| C8 | behaviour-definition: row N missing or the row's Status is empty | `behaviour-cite: missing` | calibrated ≤ 0.5 (cap); audit.log line behaviour-cite: missing |
```

Notes for the builder:
- Row order in the ref is A1..A10 then C1..C8 with C3b after C3 (matches `VALIDATOR_IDS` + `CALIBRATOR_IDS` in harness §1.1). One table, not two, so `parse_flag_table` sees all 19 keys in one pass; the D13 sub-headings "Calibrator (C-rules)" / "Validator (A-rules)" become prose sentences above the table, not table splits.
- Severity cells are prose for humans; T13 never parses them (ROW captures `id`, `trigger`, `flag` only). Harness §1.3's enum (`partial, blocked, FAIL, drop-line, probe-suspect, dim, cap, verdict`) is the Python-side `Flag.severity`; the mapping is obvious per row and is not compared.
- `_assertions.FLAGS` is written by hand from this table (19 `Flag(...)` literals). It is NOT parsed from the ref at import time (D13's last paragraph is withdrawn): parsing would make the registry depend on a markdown file's presence and defeat T13's purpose of catching drift.

## X-4 — CAL gets `locus_path`; final kwargs at all three spawn sites — DECISION

D12 omitted `locus_path` for CAL; C3 (`CONTROL-PROOF: yes` lives in the locus card) cannot run without it. Add it. Final paste-ready lines (these replace D12's three "append" fragments in full):

**`SKILL:281`** — after `` `output_path=<output-dir>/tier1-calibration.md` `` append:

```
, `card_mtime=<ISO-8601 mtime of card_path from `date -u -r <card_path> +%Y-%m-%dT%H:%M:%SZ`>`, `behaviour_definitions_path=<output-dir>/behaviour-definitions.md`, `tasklist_path=<output-dir>/diagnosability-tasklist.md`, `locus_path=<output-dir>/execution-locus.md`, `assertions_path=<skill-dir>/refs/agent-assertions.md`
```

**`SKILL:345`** — after `` `output_path=<output-dir>/tier2-<agent-name>-calibration.md` `` append:

```
, plus the same `card_mtime` (per card), `behaviour_definitions_path`, `tasklist_path`, `locus_path`, and `assertions_path` inputs as Wave 1.7 step 2
```

**`SKILL:451`** — after `` `allow_command_reexec=false` `` append (includes §X-5's `output_dir`):

```
, `calibration_paths=[<output-dir>/tier1-calibration.md, <output-dir>/tier2-*-calibration.md]`, `diff_path=<path of the instrumentation or fix diff written this run, else null>`, `artifact_mtimes={<abs path>: <ISO-8601 mtime>}` for every `<output-dir>` file the draft cites (from the single `ls` of Wave 5 step 3 persist-on-receipt), `producers_path=<output-dir>/producers.md`, `tasklist_path=<output-dir>/diagnosability-tasklist.md`, `locus_path=<output-dir>/execution-locus.md`, `output_dir=<output-dir>`, `assertions_path=<skill-dir>/refs/agent-assertions.md`
```

**CAL Inputs block** (insert after `CAL:51` `` - `output_path`: where to write your calibration report ``) — D12's four lines plus one:

```markdown
- `assertions_path` (optional): absolute path to `refs/agent-assertions.md`. Absent ⇒ skip step 5b entirely; Stage-2 row `structural_flags | skipped | no assertions_path`.
- `card_mtime` (optional): ISO-8601 mtime of `card_path` supplied by the orchestrator (you have no Bash). Absent ⇒ C5 evaluates only the `T00:00:00Z` clause; record `input_absent: card_mtime` in Notes.
- `behaviour_definitions_path` (optional): absolute path to `<output-dir>/behaviour-definitions.md`. Absent or file missing ⇒ C8 skipped; record in Notes.
- `tasklist_path` (optional): absolute path to `<output-dir>/diagnosability-tasklist.md`. Absent ⇒ C4 and C7 evaluate against the card text only; record in Notes.
- `locus_path` (optional): absolute path to `<output-dir>/execution-locus.md`. Absent ⇒ C3 skipped (a control arm cannot be proven or disproven without the card); record `assertion_skipped: C3 (locus_path)` in Notes.
```

Default-on-absent precedent for all of these is **`CAL:57`** (`2a. **Resolve claim_class ... If claim_class is absent, default to runtime_behavior (fail-safe)`), not `CAL:56` (which is `2. **Read the card**`). This corrects D12 and 05 (G-10 / I-02).

**Fallback-bullet sentences** (D13 gave a phrase; here is the text). Append to the end of `SKILL:282` (after `mark `calibration: inline-fallback` in the audit log.`):

```
 The inline path applies the identical C-rule list in `refs/agent-assertions.md` (C1-C8, C3b) with the same inputs the spawn would have received and records `structural_flags: <fired flags or none>` beside the `calibration: inline-fallback` audit line.
```

Append to the end of `SKILL:452` (after `The inline path is the fallback — never ship without validation.`):

```
 The inline path applies the identical A-rule list in `refs/agent-assertions.md` (A1-A10) with the same inputs the spawn would have received and writes the same `## Structural assertions` table into `<output-dir>/evidence-validation.md`.
```

## X-5 — VAL `output_dir`: add, optional, default None — DECISION

Both files were half right: A8 needs a directory listing (harness `files_present`); D12's `Glob` under `dirname(report_draft_path)` is the fallback when it is absent. Add to the VAL Inputs block (D12's five lines; append this sixth line after the `producers_path`, `tasklist_path`, `locus_path` line):

```markdown
- `output_dir` (optional, default none): absolute path of `<output-dir>`. When given, A8 lists `job-*.log` under it; when absent, A8 globs `job-*.log` under the directory of `report_draft_path`. Never required.
```

Harness §1.2 I-11 sentence now reads (supersedes): "the R-14 build item adds `locus_path` and `output_dir` (optional) to VAL inputs and `locus_path` (optional) to CAL inputs." The `SKILL:451` kwarg line in §X-4 already carries `output_dir=<output-dir>`.

## D4 fix — R-04 step 4 runs BEFORE the verdict branch — DECISION (supersedes D4's `SKILL:241` text)

Root cause of the round-2 FAIL (evidence 1.8): D4 put the run-rows + S14 re-evaluation inside the `insufficient ∧ non-trivial ∧ ¬--no-escalate` arm, so `partial` (including trigger-forced `partial`, v2:295), `insufficient ∧ trivial` and `--no-escalate` never ran rows. Fix: the discriminator work is a pre-branch step on `SKILL:240`; the `:241` bullet only describes the hard-stop.

**Edit 1 — `SKILL:240`.** Insert immediately BEFORE the unique anchor `` Branch on `(verdict × complexity)`: `` (grep count 1):

```markdown
**Discriminator trigger (evaluated before the branch)**: set the audit line `discriminator-required=yes` when `producers.md` has ≥2 `surviving=yes` rows, OR the observed datum is absent from every captured output of the failing run including `job-*.log`, OR `producer-count=unknown` (including the zero-surviving re-open of S1.6.0b step 3); otherwise `discriminator-required=no`. A `NameError` with one producer never enters this step. When `yes`: (i) if `verdict ∈ {sufficient, unknown}` then `verdict := partial` so the tasklist is emitted (`insufficient` unchanged); (ii) write `## Discriminator rows` in `diagnosability-tasklist.md` per refs/diagnosability-audit.md Section 7 — one `<name>-exact` / `<name>-ref` pair per `surviving=yes` producer (probe-form from refs/primitive-differential.md, at most 8 pairs, nearest to the exit statement first, overflow ⇒ header `probe-rows-truncated: <n>`), one control row (`CONTROL-PROOF: yes` arm, else the table's control column), `value-if-<claim>-true | value-if-false` on every row, and at least one pair that differs between any two surviving causes (add at most two rows; still indistinguishable ⇒ header `indistinguishable: <a>,<b>`); (iii) if `OBSERVE-VIA ≠ nobody`, run the rows now via that venue, record their outputs in `tier1-observation.md`, and re-evaluate S14 against the new observations, recomputing `diagnosability_verdict` (the datum may now be observed); if `OBSERVE-VIA = nobody`, the rows stay in the tasklist — never halt for approval. Only then branch.
```

**Edit 2 — `SKILL:241` bullet, replaced in full** (current text begins `` - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop**: emit `` and ends `No hypothesis work happens in the same turn as the instrumentation patch.`):

```markdown
   - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop** (when `discriminator-required=yes`, this arm is reached only if the rows could not run or `OBSERVE-VIA = nobody` — the rows were already attempted above): emit `diagnosability-tasklist.md` in the section order of refs/diagnosability-audit.md Section 7 ("Hard-stop tasklist composition"), set `diagnosability_hard_stop=true`, jump to Wave 5 (Waves 1.7-4 skipped). No hypothesis work happens in the same turn as the instrumentation patch. Every tasklist row carries `value-if-<claim>-true | value-if-false`; a row without both is invalid. The tasklist MUST contain the `## Emitter search` block (refs/diagnosability-audit.md Section 7, constraint 5); `capability-verdict: blocked` may appear only after that block records `emitters-found: 0` and `already-read-files: 0`. Status precedence: emitters found ∧ `re-run permitted: no` ⇒ `pipeline_hardening_verdict: blocked-on-authorization`, `status: blocked`; emitters found ∧ `re-run permitted: yes|unknown` ⇒ task rows, `status: partial`; no emitter ∧ no eligible already-read file ⇒ `capability-verdict: blocked`, `status: blocked`.
```

Satisfies: R-04 trigger + steps 1-4 before the branch for every verdict value (v2:295, v2:302); R-03 emitter block + three-way precedence (v2:284); R-06 both-columns sentence verbatim (v2:351). `SKILL:530` still untouched (D4's rationale stands). The T10/T17 fixtures (`discriminator-required: yes` with `partial` verdicts) are consistent with this flow.

## gap-7 — Composed texts for (b) `da:263`, (c) `SKILL:248` + `da:284`, (d) `SKILL:266` / `:570` — DECISION

**(b) `da:263` tasklist skeleton header.** Anchor (unique, grep 1 — `da:204` has `**Round**` without the `**Verdict**` prefix): `` **Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3 ``. Replace with one line:

```markdown
**Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3  **re-run permitted**: yes|no|unknown  **discriminator-required**: yes|no  **capability-verdict**: blocked|n/a
```

Then add directly below it (new line, part of the same skeleton block):

```markdown
<!-- append to the same line only when they apply: **indistinguishable**: <a>,<b> (S1.6.4 step (ii) gave up)  **probe-rows-truncated**: <n> (more than 8 pairs) -->
```

Form matches the harness tasklist fixtures (`procedures/tasklist/*.md`, harness :2144-2175). **Harness erratum the builder must apply:** P19, P20 and P23 regexes in harness §2 are written as `re-run permitted:\s*`, `discriminator-required:\s*yes`, `probe-rows-truncated: <n>` — the bold header form has `**` before the colon, so write them as `re-run permitted\**:\s*(yes|no|unknown)`, `discriminator-required\**:\s*yes`, `probe-rows-truncated\**:\s*(\d+)`, `indistinguishable\**:` (the A10 regex in §1.2 already does this).

**(c) Counter prose with the venue-neutral key.** `SKILL:248` (unique line starting `**Per-defect patch-round counter**:`) — replace in full:

```markdown
**Per-defect patch-round counter**: the Wave 1.6 orchestrator maintains `<output-dir>/diagnosability-rounds.json` keyed `<branch>:<repro-venue-id>` — `<branch>` is the current git branch name; `<repro-venue-id>` is the failing arm's label as written in the issue or matrix (job name, or the repro command) with digits stripped. The counter increments once per emitted tasklist that carries `discriminator-required=yes`; bracket rounds (refs/primitive-differential.md) have their own cap and never touch it. At 3 rounds for the same key the tasklist is **still written**; the report renders the 3-round cap message (refs/report-template.md hard-stop variant + cap prose) with `status: blocked`; the cap suppresses the re-run recommendation, not the file. Reset via `--reset-diagnosability-rounds`.
```

`da:284` (unique line starting `The orchestrator maintains a per-defect counter`) — replace in full:

```markdown
The orchestrator maintains a per-defect counter at `<output-dir>/diagnosability-rounds.json` keyed `<branch>:<repro-venue-id>` (`<branch>` = current git branch; `<repro-venue-id>` = the failing arm's label as written in the issue or matrix — job name or repro command — digits stripped, so re-numbered runs of the same venue share one key). The counter increments once per emitted tasklist with `discriminator-required=yes`; bracket rounds keep their own cap and never touch this file. After 3 rounds for the same key the orchestrator still writes the tasklist, emits the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose) with `status: blocked`, and suppresses the re-run recommendation until `--reset-diagnosability-rounds` is set by the user — escalating from instrumentation iteration to structural change (the diagnosis problem is no longer "we lack signal"; it is "we cannot localize the failure with any reasonable signal").
```

**(d) Cap rows `SKILL:266` and `SKILL:570`** (byte-identical today; re-verified). New row text, identical at both sites:

```markdown
| 3-round diagnosability cap reached for a counter key | Per-defect counter at `<output-dir>/diagnosability-rounds.json` reached 3 tasklists with `discriminator-required=yes` for the same `<branch>:<repro-venue-id>` | Write the tasklist anyway; emit the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose) with `status: blocked`; suppress the re-run recommendation (not the file) until `--reset-diagnosability-rounds` is set |
```

How to edit: preferred — ONE `Edit` with `replace_all=true` and `old_string` = the current row (`| 3-round diagnosability cap reached for an `issue_slug` | Per-defect counter at ... is set |`, exactly 2 occurrences). If editing per site, disambiguate by including the row four lines above, which differs between the two tables: `SKILL:262` reads `` | Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per `refs/diagnosability-audit.md` Section 2 | `` (backticked path) while `SKILL:566` reads `| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per refs/diagnosability-audit.md Section 2 |` (no backticks) — so an `old_string` spanning `:262-266` (resp. `:566-570`) is unique. The Heisenbug row directly above (`:265`/`:569`) is identical at both sites and does NOT disambiguate.

## depth-4 (R-10) — `refs/report-template.md` Diagnosis-section template — DECISION

Anchor: the `## Diagnosis` section is `RT:65-73` (`:65` `## Diagnosis`, `:67` `The single chosen hypothesis. Format:`, `:69` `**Root cause**: <one-line>`, `:71` `**Cause class**: <from the triage checklist>`, `:73` `**Detailed explanation**: 1–2 paragraphs. Why this code produces the observed symptom. Reference the evidence section, don't restate it.`; `:75` `## Evidence`). Two edits:

**Edit 1** — replace `RT:67` `The single chosen hypothesis. Format:` (unique) with:

```markdown
The single chosen hypothesis — or the UNDETERMINED form below when the headline-confidence coupling fires. The word "probable" before an enum value is forbidden anywhere in this section. Format:
```

**Edit 2** — insert after `RT:73` (anchor: `Reference the evidence section, don't restate it.`, unique), before `## Evidence`:

```markdown
**UNDETERMINED form** (mandatory when calibrated confidence < 0.5 — missing or non-numeric counts as 0.0 — OR the headline value fails `grep -F` against every artifact and every `job-*.log`; `root_cause_summary` is then the empty string):

**Root cause**: UNDETERMINED — among {<every `surviving=yes` row of `<output-dir>/producers.md`, as `file:line`, comma-separated; `indistinguishable: <a>,<b>` from the tasklist header when present>}

**Cause class**: <from the triage checklist, unchanged>

**Falsifiers** (one line per `## Discriminator rows` entry of `<output-dir>/diagnosability-tasklist.md`, verbatim from its `value-if-<claim>-true | value-if-false` cells):
- The report stays `partial` until `<row>=<value-if-true>` (then `<claim>` holds) or `<row>=<value-if-false>` (then it is refuted).

**Detailed explanation**: which rows were run this round (`tier1-observation.md`) and which remain; no mechanism narrative for a producer that has not been discriminated.
```

Satisfies v2:427-429 (`UNDETERMINED — among {…}`, falsifier sentences from the tasklist, "probable" forbidden, empty `root_cause_summary` per `SKILL:76`). Agent backstop unchanged (A1/C1). The `SKILL:450` insert (R-10 Wave 5 step 2 rule) stays as 03's card gives it; this ref text is its rendering side.

## M1 — HCT anchors for `runs-in=`, `behaviour-definition: row N`, `environment-property:` — DECISION

Re-read `HCT:9-33` and `:38-44`. Three new card lines, two anchors, both unique (grep 1 each):

**Anchor 1 — `HCT:32`** `` **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found> `` (last frontmatter field inside the template code block). Insert AFTER it:

```markdown
runs-in=<RUN-SITE label from <output-dir>/execution-locus.md, or unknown>
environment-property: <the OS / runtime / feature-flag / network / data-state property the claim depends on>
```

with these two explanatory lines added to `## Filling the card` (`HCT:118-123`, append after its last bullet):

```markdown
- `runs-in=`: mandatory whenever the execution-locus card derives `SAME-ENV ≠ yes`; a card without it is returned unread (same rule as `consistency_with_docs`). `unknown` is legal — the calibrator then caps Runtime check ≤ 0.5 (`locus_unknown`). Written as a plain `runs-in=<label>` line, not bold, so the mechanical check (`^runs-in[=:]`) matches.
- `environment-property:`: include the line ONLY when the claim names an environment property (typically `claim_class: environment_dependent`); omit it otherwise. A card that carries it must cite a 2x2 row (`## Discriminator rows` of the tasklist or the refs/primitive-differential.md differential) or the calibrator caps calibrated confidence at 0.5 (`uncited`, C7). Plain line, not bold (`^environment-property:` is the check).
```

Why plain lines: harness C3b (`^runs-in[=:]\s*unknown\b`), P11 (`^runs-in[=:]\s*\S+`) and C7 (`^environment-property:`) are line-anchored and would miss `**Runs-in**:`. v2 itself writes `runs-in=` (v2:224, :226). The C7 field is deliberately optional because the C7 predicate fires on the mere presence of the line.

**Anchor 2 — `HCT:44`** `` - `path/to/test_file.py:88` — the failing test that exercises this code path `` (last bullet of the template's `## Evidence` example list). Insert AFTER it:

```markdown
- behaviour-definition: row <N> — required when the mechanism sentence asserts what a primitive does (row written by Wave 3 step 1 / S1.6.4 step 1b to `<output-dir>/behaviour-definitions.md` before the fetch); a missing row or empty Status caps calibrated confidence at 0.5 (`behaviour-cite: missing`, C8)
```

C8's regex (`behaviour-definition:\s*row\s*(\d+)`) is unanchored, so a bullet is fine. The worked example (`HCT:127-154`) is left unchanged (it lacks `Consistency with docs` today too — 01 §4).

## G-07 — ORDERING LEDGER (the task file follows this) — DECISION

**Rules (state verbatim in the task file preamble):**
1. Phase 1 freezes a **naming ledger** (`discovery/naming-ledger.md`) before any edit: every new file, field, header key, enum token, audit-line key and flag name. Sources: §X-3 flags (19), `runs-in=`, `environment-property:`, `behaviour-definition: row N`, `execution_locus_card_path`, `status: blocked`, `blocked-on-authorization`, `split_pending`, `cosmetic_overrun`, `discriminator-required`, `re-run permitted`, `capability-verdict`, `indistinguishable`, `probe-rows-truncated`, `optional_ref_absent`, `<branch>:<repro-venue-id>`, `contract_version 1.2.0`, `HC0-HC5`, the four new ref paths, the 20 test filenames, `_assertions.py`, `_procedures.py`. No edit may introduce a name absent from the ledger.
2. **R-16 enum before R-17 rename** — in every file both touch (`hardening-output-contract.md`, `SKILL:64/420/444`, `test_hardening_verdict.py`), the enum edit lands first, then the rename, in separate items.
3. **R-01 before R-02** (R-02 step 4 overwrites R-01's `pending-producers` sentinel), and R-02 before R-04/R-10 (03 §4 items 1-3).
4. **New ref + its Refs-table row before any wave text cites it** (`primitive-differential.md`, `agent-assertions.md`, `environment-deltas.md`, `probe-packs/read-parse.md` → `SKILL:600` rows → then the waves).
5. **Bottom-up within SKILL.md** for the remaining edits: Wave 5 → Wave 4.5 → Wave 3 → Wave 1.7 → Wave 1.6 → Wave 1 → Output Contract → wave map. The Refs-table rows are the highest-numbered seam AND a prerequisite (rule 4), so they are done in group C, before the waves; that is the only deviation from strict top-of-file-last order and it is deliberate.
6. All edits anchor on quoted `old_string`, never on line numbers; line numbers in this file are hints re-verified 2026-09-19.

**Edit groups (numbered; each group completes before the next starts):**

| # | Group | Files : anchors |
|---|---|---|
| 1 | Naming ledger + anchor inventory + preserve-baseline (Phase 1) | `discovery/naming-ledger.md`, `discovery/insertion-anchors.md`, `discovery/preserve-baseline.md` |
| 2 | R-16 enum | `refs/hardening-output-contract.md` enum row(s) in `:43-48` + `:68` `{blocked, advisory}` kept; `SKILL:64` (`pipeline_hardening_verdict` enum + `Contract v1.2.0+`), `SKILL:444`, `SKILL:420` (H5 statuses text); `tests/troubleshoot/test_hardening_verdict.py:51` (5-token string) |
| 3 | R-17 rename | `SKILL:63,67-71` (description column), `:104`, `:408`, `:410`, `:414-420`, `:444`, `:595-600`; `refs/hardening-output-contract.md` (D11 list, verbatim-keeps honoured); `refs/pipeline-hardening-closure.md`; `refs/report-template.md:230-235,316`; `refs/unmask-and-sweep.md`; `refs/runtime-entrypoint-verification.md:1,3,7,9,11,28`; `refs/contract-enumeration.md`; `refs/effective-input-proof.md`; `tests/troubleshoot/test_hardening_h1.py:46`; run the D11 guard → `GUARD OK` |
| 4 | New refs + Refs rows + status/contract plumbing | NEW `refs/primitive-differential.md` (R-05), `refs/agent-assertions.md` (§X-3), `refs/environment-deltas.md` (D9), `refs/probe-packs/read-parse.md` (R-05 optional); `SKILL:600` four rows (D10); `SKILL:62` (D3), `SKILL:77` new row (D3/R-01), `SKILL:73` (D2), `SKILL:43` (D2); `refs/hardening-output-contract.md:13,25` (D3); `refs/report-template.md:161` (D2) |
| 5 | Agents (R-14) | `CAL:51` Inputs (§X-4), `CAL:57` precedent unchanged, `CAL:62` step 5b cite line, `CAL:88-96` Stage-2 `structural_flags` row, `CAL:108` `split_pending` (D8), `CAL:111-115` Notes; `VAL:44` Inputs (§X-4 + §X-5), `VAL:55` → 2b cite line, `VAL:63-97` `## Structural assertions` output table (harness §6 shape), `VAL:72` (D2), `VAL:99-103` (D2) |
| 6 | Other refs (bottom-up per file) | `da:338` unchanged; `da:284` (gap-7c); `da:263` (gap-7b); `da:255` (D5 — was cited `:253`); `da:260-278` skeleton Task 6 (D5); `da:247` constraint 5 (R-03); `da:242-247` R-06 falsifier constraint; `da:150` S14 row (R-03); `da` complexity signal (R-15); `RT:73` + `RT:67` (depth-4); `RT` rendering rules (R-13); `HCT:118-123` filling bullets, `HCT:91`, `HCT:80-82` (R-07), `HCT:44`, `HCT:32` (M1); `refs/triage-checklist.md:44` (D6) + refuse clause + cause-class row (R-15); `refs/escalation-rubric.md:69` (D8) |
| 7 | SKILL.md waves, bottom-up | `:582` (D7) → `:545` Will-Not ×4 (D7) + R-13 bullet → `:570` cap row (gap-7d, or `replace_all` with `:266`) → `:529` (D2) → `:515` `Bash` row Tier 1 cell gains "repro via `OBSERVE-VIA`; job-log fetch; S1.6.4 discriminator rows when `OBSERVE-VIA ≠ nobody`" → `:512` `Task` row: Tier 1 cell `root-cause-analyst + confidence-calibrator (C-rule structural assertions via assertions_path)`, Tier 2 cell `… evidence-validator at Wave 5 (A-rule structural assertions)` → `:509` context7 row Tier 2 cell gains "; behaviour-definition fetch (Wave 3 step 1; fallback `WebFetch` → `gh api`)" → `:462` footer `cosmetic_overrun` (D7) → `:460` reasons (D8) → `:457` status (D2) → `:452` (§X-4 sentence) → `:451` kwargs (§X-4) → `:450` R-10 insert → Wave 5 step 3 persist-on-receipt (R-11) + timestamps (R-13) per 03 cards → `:439` self-consistency (R-07) → `:381`, `:372`, `:358` (R-08/R-07 per 03) → `:348` step 4.5 (R-08) → `:346` → `:345` kwargs (§X-4) → `:342` menu-equality (R-02 step 6) → `:336` R-09 sub-bullet → `:282` (§X-4 sentence) → `:281` kwargs (§X-4) → `:280` "returned unread" analogy for `runs-in=` (R-01) → `:266` cap row (gap-7d) → `:255` exit line gains `discriminator-required=<yes|no>` → `:248` (gap-7c) → `:241` (D4 fix Edit 2) → `:240` (D4 fix Edit 1) → `:230` S1.6.0b (R-02) → `:168` (R-01 OBSERVE-VIA) → `:167/168` step 1b insert (R-01) → `:106` (D2) → `:97` (R-01 wave-map label) |
| 8 | Command file | `commands/troubleshoot.md:103` Bash bullet → `:69` on-return sentence (R-18) |
| 9 | Sync + gate | `make sync-dev` → `make verify-sync` (D1-a scoped check, or full in the D14 worktree) → markdownlint (gap-6) → preserve-baseline byte-compare → M3 gate |
| 10 | Phase 3 (tests) | `_procedures.py` → `_assertions.py` → fixtures (harness §4-§5) → T1..T19 + T5b + T14 + `test_hc_rename_guard.py` → `uv run pytest tests/troubleshoot/ -v` → `uv run pytest -q` → ruff → post-merge note for `agent_grounding_drift` suite |

**Consolidated Phase 2 seam list (deduped, file:anchor pairs — 103 entries = 100 edit seams + 3 explicit no-edit markers):**

- `SKILL.md` (49): `:43`, `:62`, `:63`, `:64`, `:67-71`, `:73`, `:77`, `:97`, `:104`, `:106`, `:167/168`, `:168`, `:230`, `:240`, `:241`, `:248`, `:255`, `:266`, `:280`, `:281`, `:282`, `:336`, `:342`, `:345`, `:346`, `:348`, `:358`, `:372`, `:381`, `:408`, `:410`, `:414-420`, `:439`, `:444`, `:450`, `:451`, `:452`, `:457`, `:460`, `:462`, `:509`, `:512`, `:515`, `:529`, `:545`, `:570`, `:582`, `:595-600`, `:600`
- `refs/diagnosability-audit.md` (9): `:150`, `:242-247`, `:247`, `:255`, `:263`, `:260-278` (Task 6), `:284`, complexity-signal seam (R-15), `:338` (no edit; loading-discipline unchanged)
- `refs/hypothesis-card-template.md` (5): `:32`, `:44`, `:80-82`, `:91`, `:118-123`
- `refs/report-template.md` (6): `:67`, `:73`, `:161`, `:230-235`, `:316`, rendering rules (R-13)
- `refs/triage-checklist.md` (3): `:44` (D6), refuse clause, cause-class row (R-15)
- `refs/escalation-rubric.md` (1): `:69`
- `refs/hardening-output-contract.md` (4): `:13`, `:25`, enum rows `:43-48`, rename set (D11)
- Rename-only refs (5): `pipeline-hardening-closure.md`, `unmask-and-sweep.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `effective-input-proof.md`
- New refs (4): `primitive-differential.md`, `agent-assertions.md`, `environment-deltas.md`, `probe-packs/read-parse.md`
- `agents/confidence-calibrator.md` (6): `:51`, `:62`, `:88-96`, `:108`, `:111-115`, (`:127-134` untouched)
- `agents/evidence-validator.md` (6): `:44`, `:55`, `:63-97`, `:72`, `:99-103`, (`:5` tools unchanged)
- `commands/troubleshoot.md` (2): `:69`, `:103`
- Tests touched in Phase 2 (2): `test_hardening_verdict.py:51`, `test_hardening_h1.py:46`
- Config (1): `.pre-commit-config.yaml:77-83` markdownlint `exclude` (gap-6)

**Recomputed counts:** Markdown files changed in Phase 2 = **19** (15 edited: SKILL, 7 substantive refs, 5 rename-only refs, 2 agents, 1 command; 4 new refs, of which 2 optional) — not 06's "11/12". Untouched by design: `refs/calibrator-eval-cases.md`, `refs/doc-discovery.md`, `refs/remediation-handoff.md`. M3 gate tier (06 P10): changed lines will exceed 500 (SKILL alone ~45 seams + 4 new refs + 2 agents) → "500-1500 → 4+4 = 8 agents, N=10"; if the fixture/test phase is gated in the same M3 pass (88 + 31 fixtures, 22 Python files) it is >1500 → "5+5 = 10, N=15". State the tier in the gate preamble.

## gap-6 — markdownlint item — DECISION

Verified in repo: `.markdownlint.json` exists (`default: true`, `MD024 siblings_only`, `MD013/MD029/MD036/MD033` off); `.pre-commit-config.yaml:72-83` runs `igorshubovych/markdownlint-cli` **v0.38.0** with `args: ['--fix']` and `exclude` = `CHANGELOG.md | node_modules | *.min.md | .dev/.* | tests/swarm/fixtures/bare_review_v1/golden/.*`. No `make markdownlint` target; `pre-commit` is installed at `/config/.local/bin/pre-commit`; `npx` at `/usr/bin/npx`. Pre-commit does NOT run `verify-sync` (`.pre-commit-config.yaml:102,117` say so explicitly — this is the G-17 correction for `research-notes.md:44`, orchestrator-owned).

**Task-file item (Phase 2 group 9, before `make sync-dev`):**

```bash
cd /config/workspace/IronClaude
pre-commit run markdownlint --files \
  src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \
  src/superclaude/skills/sc-troubleshoot-protocol/refs/{diagnosability-audit,hypothesis-card-template,report-template,triage-checklist,escalation-rubric,hardening-output-contract,pipeline-hardening-closure,unmask-and-sweep,runtime-entrypoint-verification,contract-enumeration,effective-input-proof,primitive-differential,agent-assertions,environment-deltas}.md \
  src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md \
  src/superclaude/agents/confidence-calibrator.md \
  src/superclaude/agents/evidence-validator.md \
  src/superclaude/commands/troubleshoot.md
# fallback without pre-commit: npx markdownlint-cli@0.38.0 --config .markdownlint.json --fix <same files>
```

Expected: exit 0 with no file rewritten (the hook's `--fix` mutates in place — run `git diff --stat` afterwards; any rewrite must be re-read before `make sync-dev`).

**Required companion edit (one line, `.pre-commit-config.yaml` `exclude` block, after `tests/swarm/fixtures/bare_review_v1/golden/.*|`):** add `tests/troubleshoot/fixtures/.*|`. Reason: the hook's `--fix` would otherwise rewrite the 88 assertion fixtures (frontmatter `---` blocks and `--- file: ---` separators trip MD022/MD032/MD041) and the 9 vendored regression files, whose sha256 the T15 MANIFEST pins — a silent fixture mutation would fail T15 at commit time. Precedent: the existing golden-fixture exclusion on the line above.

## depth-3 — Test function names (20 spec files + guard) — DECISION

One row per file; parametrized functions carry the harness §3 `ids=` case names. Counts match harness §8.

| T | file | `def test_...` |
|---|---|---|
| T1 | `test_validator_assertions.py` | `test_validator_fixture_fires_expected_flags(fixture_path)` (46 ids, e.g. `A7-io-neg-empty-producers`); `test_validator_status_mapping()` (§1.3: FAIL > blocked > partial > None) |
| T2 | `test_calibrator_assertions.py` | `test_calibrator_fixture_fires_expected_flags(fixture_path)` (42 ids); `test_c1_forces_escalate()`; `test_c2_zeroes_runtime_check()`; `test_c6_caps_calibrated_at_0_3()`; `test_c7_c8_cap_calibrated_at_0_5()` |
| T3 | `test_producers_enumeration.py` | `test_producers_md_header_columns_and_row_count(src, value, var, expect_unknown)` (2 ids `io`, `nonio`); asserts inside: zero-surviving ⇒ `surviving=re-opened`, `## Mechanism rows` not counted |
| T4 | `test_primitivegrep_targeting.py` | `test_primitive_grep_targets_only_sink_and_overwrites_sentinel()` (4 asserts) |
| T5 | `test_locus_card.py` | `test_complete_card_ok()`; `test_missing_run_site_fails_wave1()`; `test_same_env_derivation(name, expect)` (3 ids `one-env`, `two-env`, `no-env`); `test_card_without_runs_in_is_returned()` |
| T5b | `test_verdict_source.py` | `test_verdict_from_log(log, expect)` (3 ids `marker`, `no-marker`, `conclusion-only`) |
| T6 | `test_discriminator_form.py` | `test_form_parses_and_exactly_one_row_matches(form, vector, winner)` (2 ids `io`, `nonio`); reference-mismatch ⇒ A9 asserted inside the same case |
| T7 | `test_threshold_bracket.py` | `test_bracket_result(results, n, expect)` (3 ids `monotone`, `non-monotone`, `absorbed-82-85`); trigger clauses + counter-file-untouched asserted inside `monotone` |
| T8 | `test_cosmetic_counter.py` | `test_cosmetic_counter_fires_exempts_and_resets()` (expects `[5, 14, 19]`) |
| T9 | `test_counter_key.py` | `test_counter_key_and_round_cap(tmp_path)` (digits stripped; only `discriminator-required: yes` increments; round 3 ⇒ still written + `blocked`) |
| T10 | `test_hardstop_verdicts.py` | `test_hardstop_verdict(name, expect_key)` (4 ids `authorized`, `refused`, `no-emitter-no-file`, `source-only-read`); A10 asserted inside `authorized` |
| T11 | `test_headline_threshold.py` | `test_threshold_separates_pos_and_neg_fixtures()`; `test_missing_confidence_is_undetermined()` |
| T12 | `test_timestamp_tolerance.py` | `test_timestamp_tolerance(delta, ok)` (2 ids `+4m59s`, `+5m01s`); `test_midnight_always_fails()` |
| T13 | `test_inline_fallback_parity.py` | `test_flag_table_parity_across_surfaces()` (§6 assertion 1); `test_evaluator_matches_every_fixture_expectation()` (assertion 2, loops all fixtures + regression params); `test_skill_fallback_names_every_flag_or_cites_ref()` (assertion 3) |
| T14 | `test_calibrator_eval_cases.py` | `test_ref_pins_expectation(substring)` (~16 ids F1-F9, P1-P5, suite ×2); `test_rubric_fixture_case(case)` (F1-F9); `test_rubric_property_grid(eg, rc)`; `test_rubric_determinism()`; `test_caps_layer_after_formula()` |
| T15 | `test_regression_sysbox.py` | `test_regression_manifest_and_expected_ids(param)` (3 ids `GLM-RUN2`, `Fable-D3`, `Astra-A3`; sha256 check + expected id set + Astra `runs-in` return via P11) |
| T16 | `test_primitive_differential.py` | `test_differential_decision(section, expect)` (3 ids `substituted`, `all-unobserved`, `single-env`) |
| T17 | `test_discriminator_rows.py` | `test_discriminator_rows(name, expect)` (4 ids `distinguishing`, `indistinguishable`, `exact-only`, `overflow`) |
| T18 | `test_behaviour_definition_row.py` | `test_behaviour_row(name, expect)` (3 ids `fetched`, `recalled`, `missing`) |
| T19 | `test_menu_equality.py` | `test_menu_equality(prompt, ok, tmp_path)` (2 ids `equal`, `missing-one`) |
| extra | `test_hc_rename_guard.py` | `test_no_h_tokens_outside_allow_list()` |

## Cite fixes — DECISION

- **D5** anchor is `da:255` (`- **Add env override OR add fixture wrapper OR wrap subprocess.run**: …`), not `:253` (`- **Invocation site**: …`). Text unique; edit lands either way.
- **D12** default-on-absent precedent is `CAL:57` (`2a. **Resolve claim_class…** If claim_class is absent, default to runtime_behavior`), not `CAL:56` (`2. **Read the card**`). Same off-by-one 05 had (G-10 / I-02) — do not propagate to the task file.
- **X-12 / D10 footer:** `## Loading discipline` footers are YES on `refs/agent-assertions.md` (D13 skeleton keeps it; three consumers) and YES on `refs/primitive-differential.md` (multi-section); NO on `refs/environment-deltas.md` and `refs/probe-packs/read-parse.md`. D10's Summary line "footer only on primitive-differential.md" is corrected to "footers on primitive-differential.md and agent-assertions.md".

---

## Z — Carry-forward pointers (round-2 items NOT changed here; read them in the two 07 files as written)

- D1 (verify-sync scoped gate; D1-b OPEN QUESTION default "leave orphans") — `07-gap-fill-decisions.md` §D1, unchanged.
- D2 (`status: blocked` eight sites; `blocked ⇒ halt`; no sc-task edit) — §D2, unchanged; owner R-16 task.
- D3 (`contract_version` 1.2.0; `HOC:13,25`) — §D3, unchanged.
- D5 body (five task shapes + skeleton Task 6) — §D5, unchanged except the `:255` cite above.
- D6 (triage `## Producer citation` section after `:44`) — §D6, unchanged.
- D7 (four Will-Not bullets; `cosmetic_overrun` audit line + footer; `:582` sentence) — §D7, unchanged.
- D8 (`split_pending` rule after `RUB:69`; `CAL:108`; `SKILL:460`) — §D8, unchanged.
- D9 (`environment-deltas.md` 22-line body) — §D9, unchanged.
- D10 (four Refs rows after `SKILL:600`) — §D10, rows unchanged; footer rule corrected above.
- D11 (R-17 rename/stay sets, guard script, `test_hardening_h1.py:46`, `test_hardening_verdict.py:51`) — §D11, unchanged.
- D12 VAL Inputs five lines — unchanged, plus the `output_dir` sixth line (§X-5); CAL Inputs superseded by §X-4.
- D13 lead paragraph, `## Output shape`, `## Loading discipline` — unchanged; tables superseded by §X-3; "parsed from this ref" sentence withdrawn.
- D14 (worktree recipe; D14-b OPEN QUESTION default "skip") — §D14, unchanged.
- D15 (`01:409` correction; `tests/troubleshoot/` exists) — §D15, unchanged.
- Harness §0 (06 3.x superseded), §1.1 API, §1.3, §1.4, §2 P1-P25 (with the bold-header regex erratum in gap-7b), §3, §4.1-4.4 fixture bodies, §5 MANIFEST + expected ids, §6 T13, §7 T14, §8 commands/baseline, §9 ruff — unchanged. §1.2 unchanged except I-11 wording (§X-5).
- G-17 / gap-11 (`research-notes.md:44` "pre-commit runs verify-sync" is false — `.pre-commit-config.yaml:102,117`) — orchestrator-owned; evidence supplied in gap-6 above.
- gap-13 (TS-01 label on R-19 critique constraints), M5 (06 skeleton 2.6 "Wave 4 (R-14 wiring)" → "Wave 4 (R-08)"), G-11/I-03 (agent line counts 141/128), G-14 (`VAL:51-58` tag) — cosmetic; builder applies when writing the task file, no further research.

---

## Status: Complete

**Resolved in this file:** X-1, X-2, X-3, X-4, X-5, X-12, D4 (R-04 step-4 placement), gap-7 (b)(c)(d), depth-4 (R-10 Diagnosis template), M1 (three HCT anchors), G-07 (ordering ledger + 100-seam list + recomputed 19-file count), gap-6 (markdownlint command + fixture exclusion), depth-3 (test function names), D5/D12 cite fixes, G-06 `SKILL:512` (+ `:509`, `:515`) rows.

**Still OPEN for the user (unchanged defaults apply if unanswered):**
- D1-b — delete the six pre-existing `.claude/`-only orphans locally? Default: no.
- D14-b — fast-forward local `master` 17 commits in the dirty tree? Default: no.
- gap-6 companion — adding `tests/troubleshoot/fixtures/.*` to the markdownlint `exclude` is a `.pre-commit-config.yaml` edit outside the skill/agent/test dirs; it is required for T15 integrity (reason above). Default: include it in this PR.
