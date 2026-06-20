# Cross-Validation Report — TFEP /sc:forensic → /sc:troubleshoot Migration Research

**Analysis type:** completeness-verification (cross-validation lens)
**Date:** 2026-06-16
**Files analyzed:** 4 (01-file-inventory.md, 02-troubleshoot-surface.md, 03-integration-and-sync.md, 04-template-and-examples.md)
**Lens focus:** Verify the four research files AGREE on overlapping claims. Flag contradictions in: TFEP line numbers (R1 vs R3), troubleshoot Output Contract fields vs missing TFEP fields (R2 vs R3), return-contract.yaml gap (R2 vs R3), report-template/sync contract (R3 vs R4).

---

## Method

For each overlap area the spawn prompt named, I extracted the concrete claim from
each file, compared them, and spot-checked both against the actual source files
(`sc-task-protocol/SKILL.md`, `sc-troubleshoot-protocol/refs/report-template.md`)
to confirm the agreement is grounded in fact, not in two agents sharing the same
mistake. Ground-truth Reads performed this turn: SKILL.md lines 130–264;
report-template.md lines 144–159.

---

## Overlap 1 — TFEP / forensic line numbers (R1 vs R3)

**R1 claim:** TFEP section = lines **133–261** (133 = `### 4.5` heading; whole section
through 261). Forensic occurrences enumerated at 172, 205, 206, 212, 213, 215, 216,
250, 253, 258, 259; context.yaml at 203; return-contract.yaml read at 216; consumer
field reads at 219–222, 225.

**R3 claim:** "the TFEP block, lines **172–261**" (headline #1, §1, Summary). Load-bearing
lines enumerated at 172, 205, 206, 208–210, 212, 213, 215, 216, 219–222, 225, 237–253
(incl. 250, 253), 255–261 (incl. 258, 259).

**Apparent discrepancy:** R1 says the block is `133–261`; R3 says `172–261`.

**Verdict: AGREE — reconciled, not contradictory.** Ground-truth Read confirms line 133
is the `### 4.5 Test Failure Escalation Protocol (TFEP)` heading and line 172 is the
first `forensic` string (`**Escalation gradient ... for future forensic integration**`).
R1 is describing the **whole structural section** (heading-to-end = 133–261); R3 is
describing the **live forensic mutation surface** (first forensic string to end of the
escalation budget = 172–261). R3 itself says "the TFEP block, lines 172–261" in the
context of "the ONLY live load-bearing `/sc:forensic` surface" — i.e. the forensic
content, which begins at 172, exactly matching R1's own observation that the earliest
forensic occurrence is line 172. The two framings are consistent and every shared
per-line anchor matches byte-for-byte. Both also agree the section ends at 261
(line 262 blank, 263 = `### 5. Feedback Collection`).

**Per-line anchor cross-check (R1 ∩ R3), all verified against source:**

| Anchor | R1 | R3 | Source-verified |
|---|---|---|---|
| `Escalation gradient ... forensic integration` | 172 | 172 | 172 ✓ |
| `**Step 3: Invoke forensic**` | 205 | 205 | 205 ✓ |
| `Determine the forensic tier` | 206 | 206 | 206 ✓ |
| `/sc:forensic ... --caller task-unified --context ... --depth quick` (dispatch) | 212 | 212 | 212 ✓ |
| `forensic pipeline runs ... returns a structured return contract` | 213 | 213 | 213 ✓ |
| `**Step 4: Consume forensic results**` | 215 | 215 | 215 ✓ |
| `Read the forensic return contract from {output_dir}/return-contract.yaml` | 216 | 216 | 216 ✓ |
| status/test_is_wrong/recommended_escalation handling | 219–222 | 219–222 | 219–222 ✓ |
| `Read tasklist_insertion_path` | 225 | 225 | 225 ✓ |
| `Forensic artifacts: {path to output_dir}` | 250 | 250 | 250 ✓ |
| `committed to git alongside other forensic artifacts` | 253 | 253 | 253 ✓ |
| Escalation Budget `/sc:forensic` lines | 258, 259 | 258, 259 | 258, 259 ✓ |
| `context.yaml` write | 203 | 203 (§4) | 203 ✓ |

Zero conflicts. (Minor non-conflict: R3 additionally cites the tier-mapping block
208–210 that R1 folds into the Step-3 body 205–213; complementary, not contradictory.)

---

## Overlap 2 — Troubleshoot Output Contract fields vs missing TFEP fields (R2 vs R3)

**R2 claim (B3, lines 41–72 of troubleshoot SKILL.md):** 30-field Output Contract
enumerated. Direct donors to TFEP: `status` (43), `test_is_wrong` (49),
`test_file_path` (50), `behavior_is_documented` (51). **MISSING** as structured fields:
`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`/block-path,
`root_cause_summary`, `solution_summary`.

**R3 claim (§4):** Troubleshoot returns a dict with `status` (matches!), `tier_reached`,
`report_path`, `audit_log_path`, `confidence`, `escalation_reason`, `test_is_wrong`
(matches!), `test_file_path`, `behavior_is_documented`, `task_file_path`, etc.
Task-protocol consumer reads `test_is_wrong`, `status`, `recommended_escalation`,
`tasklist_insertion_path`. **MISSING:** `tasklist_insertion_path` (closest =
`task_file_path`, Tier-3-only, + `diagnosability_tasklist_path`); `recommended_escalation`
(closest = `escalation_reason`/`tier_reached`).

**Verdict: AGREE.** Both files independently identify the SAME matching donors
(`status`, `test_is_wrong`) and the SAME missing fields with the SAME closest-analog
reasoning:

| Field | R2 finding | R3 finding | Agree? |
|---|---|---|---|
| `status` | donor present (line 43); enum may differ | "matches!"; success\|partial\|failed | YES |
| `test_is_wrong` | donor present (49) + `test_file_path` (50) | "matches!" | YES |
| `recommended_escalation` | MISSING; closest `escalation_reason`(48)/`tier_reached`(44) | MISSING; closest `escalation_reason`/`tier_reached` | YES |
| `tasklist_insertion_path` | MISSING; closest `diagnosability_tasklist_path`(60)/`task_file_path`(55) | MISSING; closest `task_file_path`/`diagnosability_tasklist_path` | YES |
| `remediation_target`/block | PARTIAL; no single structured field | surfaced via new `## TFEP Consumer` block (`remediation_target`) | YES (consistent) |
| `root_cause_summary` | MISSING (prose only in REPORT.md) | (implied via incident-report re-source, §4.5) | YES (consistent) |
| `solution_summary` | MISSING (prose only) | (implied via incident-report re-source) | YES (consistent) |

The two agents reached identical conclusions about which fields exist, which are
missing, and what the nearest fallback donors are. No divergent field lists.

**Minor scope note (not a contradiction):** R2 enumerates all 30 contract fields with
exact line numbers (41–72); R3 lists a representative subset "etc." R3's subset is a
strict subset of R2's full enumeration with no conflicting field name or type. R2 is
the authoritative donor enumeration; R3 is consistent with it.

---

## Overlap 3 — return-contract.yaml gap (R2 vs R3)

**R2 claim:** Troubleshoot today emits NO `return-contract.yaml`. It returns the Output
Contract as a dict and a machine-readable `SC:TROUBLESHOOT:SUMMARY` footer (B6, lines
446–455). To bridge: add a conditional Wave 5 emission step (~step 4.5, after footer
ending 457, before surface step 459) writing `<output-dir>/return-contract.yaml` only
when `caller=task-unified`. Skill emits the file; command only surfaces the path
(thin-command NFR-5, command line 169).

**R3 claim (headline #2, §4.2):** "The `sc-troubleshoot-protocol` skill ... emits no
`return-contract.yaml`." Adapter must either (a) make troubleshoot write that file, or
(b) rewrite task-protocol Step 4 to read troubleshoot's dict/REPORT.md instead. The
task-protocol consumer reads `{output_dir}/return-contract.yaml` at SKILL.md L216.

**Verdict: AGREE.** Both files state, in identical terms, that:
1. Troubleshoot does NOT currently emit `return-contract.yaml` (it returns a dict).
2. The TFEP consumer (task-protocol) reads `{output_dir}/return-contract.yaml`.
3. The fix is to make the troubleshoot **skill** write that file (R2 strongly recommends
   option (a) emission at Wave 5; R3 lists (a) as its first option). R3's option (b)
   (rewrite the consumer instead) is an *additional* alternative R3 raises, not a
   contradiction of R2 — R2 and R3 both endorse option (a) as the primary path.

**Emission location — agreement on WHERE:** Both place the emission in the troubleshoot
**skill's Wave 5**, not the command. R2 pins it to a new step ~4.5 between the footer
(ends line 457) and the surface step (line 459) and reinforces "skill emits, command
surfaces" via NFR-5. R3 §3/§4 keeps all emission logic in `src/superclaude/skills/
sc-troubleshoot-protocol/` and treats the command as a thin surface. No disagreement
on where `return-contract.yaml` is emitted.

---

## Overlap 4 — Where `--context` / `--caller` is parsed (R2 vs R3)

**R2 claim (B1):** `--context`/`--caller` parsing must be added to **Wave 0 step 1,
SKILL.md line 115** (the `Optional:` flag-parse sentence), with a resolve sub-step after
line 139, and to the command-side parse step `commands/troubleshoot.md:64` + argument-hint
line 8 + Options table after line 58. Skill is where ingestion is *parsed*; command is
the thin advertiser.

**R3 claim (§4):** Troubleshoot's accepted flags are at **SKILL.md L115** (`--type`,
`--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`,
`--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`)
— "No `--caller`, `--tier`, `--intent`, `--context`." So the migration must add them.

**Verdict: AGREE.** Both files cite **SKILL.md line 115** as the canonical flag-parse
location and both quote the SAME existing optional-flag enumeration. Both agree
`--context`/`--caller` are currently ABSENT and must be ADDED there. R2 adds the
command-side parse anchors (line 64, line 8, table line 58) consistent with the
thin-command/thick-skill split; R3 does not contradict this — it focuses on the skill
flag list and explicitly defers cross-ref/command sync to R2 ("R2 owns the troubleshoot
command/flag/contract surface", R3 §5). Complementary ownership, identical factual claim
about where parsing lives (line 115).

**Bonus consistency — the argument-hint vs flag-list partial-ness:** R2 (A1) flags that
`commands/troubleshoot.md:8` argument-hint is ALREADY missing the three diagnosability
flags that exist at SKILL.md:115, and says "R3 owns cross-ref sync; flag here only."
R3 §4 independently lists those same three diagnosability flags as present at L115.
The two are consistent and even cross-reference each other's ownership boundary
correctly.

---

## Overlap 5 — Report-template / sync contract (R3 verification vs R4)

**R3 claim (§2):** Report-template `## Next Steps` at line 146 (body 146–154);
`### Hard-stop variant` at line 156; NO `## TFEP Consumer` block exists yet; insert the
new machine-readable block **after line 154, before line 156**. R4 owns the block's
exact field set / fencing; R3 pins only the anchor + field-name reconciliation.

**R4 claim:** R4 explicitly defers the report-template block mechanics — its scope is
Template-02 MDTM mechanics + a worked example. R4 does not assert its own competing
report-template line numbers; it confirms (PART B, §M4 discussion) that template-derived
blocks gate on M4 fidelity and that the builder authors them. R4 §SUMMARY item 5 lists
"reference-completeness, no-orphaned-forensic-refs, command-name-accuracy" lenses that
align with R3's `## TFEP Consumer` block needing field-name reconciliation.

**Verdict: AGREE — clean ownership handoff, no overlap conflict.** R3 owns the
report-template insertion ANCHOR; R4 owns the MDTM TASK-FILE mechanics. These are two
different artifacts (the troubleshoot `refs/report-template.md` vs the generated MDTM
tasklist), so there is no shared claim to contradict. Where they touch — R3 saying "R4
owns the mechanics of the `## TFEP Consumer` block" and R4 deferring template-block
authoring to the builder — they agree on the boundary. Ground-truth Read confirms R3's
report-template anchors exactly (Next Steps = 146, list end = 154, Hard-stop variant =
156).

**Sync/verification contract (R3 vs R4) — AGREE:** Both independently state the same
SoT discipline: edit `src/superclaude/...`, then `make sync-dev`, then `make verify-sync`;
NEVER stage any `.claude/` path except `settings.json` (CLAUDE.md ABSOLUTE RULE). R3 §3
sources it from the Makefile (sync-dev L109–163, verify-sync L166+) and CLAUDE.md; R4
§SUMMARY item 7 states the identical rule ("Skill-dir edits MUST `make sync-dev` then
`make verify-sync` and MUST NOT stage `.claude/`"). Identical, no divergence.

---

## Additional cross-file consistency checks (beyond the 5 named overlaps)

- **`--caller task-unified` literal.** R1 (D/§E), R2 (PART C), and R3 (§1A L212, §1D)
  all agree the only LIVE `task-unified` string is the `--caller task-unified` literal at
  `sc-task-protocol/SKILL.md:212`, and R3 adds (consistently with R1) that it is a stale
  caller-id to reconsider. No conflict.
- **return-contract.yaml name collision.** R3 §1D explicitly distinguishes the TFEP
  `return-contract.yaml` from the unrelated swarm-CLI artifact of the same name. R2 only
  ever discusses the TFEP one. No contradiction — R3's disambiguation does not conflict
  with R2's narrower scope.
- **Output-dir / context path.** R1 (line 203 `context.yaml`, line 212 `--context
  {context_path}`) and R3 (§4: `--context {context_path}` is a `context.yaml` written at
  L203) agree exactly on where the context package is written and passed.

---

## Status / completeness note (not a contradiction, but flagged for the gate)

- **R4 header says `Status: In Progress` (line 3) but its final line (169) says
  `Status: Complete`.** This is an internal inconsistency WITHIN R4, not a cross-file
  contradiction, so it does not affect this cross-validation verdict. It is flagged here
  for the completeness-verification gate: R4's opening status line should be reconciled to
  `Complete` to match its closing status and the substantive completeness of its content.
  This does not introduce any factual conflict with R1/R2/R3.

---

## VERDICT: PASS

The four research files **AGREE** on every overlapping claim the lens targeted:

1. **TFEP line numbers (R1 vs R3):** AGREE. R1's `133–261` (whole section) and R3's
   `172–261` (live forensic surface) are reconciled framings of the same block; all
   shared per-line anchors match each other and the source byte-for-byte.
2. **Output Contract fields vs missing TFEP fields (R2 vs R3):** AGREE. Identical
   donor set (`status`, `test_is_wrong`), identical missing-field set
   (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`,
   `root_cause_summary`, `solution_summary`), identical closest-analog reasoning.
3. **return-contract.yaml gap (R2 vs R3):** AGREE. Both confirm troubleshoot emits no
   such file today, both place the new emission in the troubleshoot **skill's Wave 5**,
   both keep the command thin (surface-only).
4. **Where `--context`/`--caller` is parsed (R2 vs R3):** AGREE. Both cite SKILL.md
   **line 115** as the parse location and the same existing optional-flag enumeration;
   both confirm the two flags are currently absent.
5. **Report-template / sync contract (R3 vs R4):** AGREE. Clean ownership handoff (R3 =
   report-template anchor, R4 = MDTM mechanics); identical SoT/sync/no-`.claude`-staging
   rule. R3's report-template anchors (146/154/156) verified against source.

**Contradictions found: NONE.**

**Non-blocking observations (do not affect PASS):**
- R4 internal status inconsistency (`In Progress` at line 3 vs `Complete` at line 169) —
  reconcile R4's opening status line; no cross-file impact.
- R3 raises an alternative option (b) "rewrite the consumer to read the dict" alongside
  R2's preferred option (a) "emit the yaml"; both endorse (a) as primary, so this is an
  additive alternative, not a divergence.

The overlapping claims are mutually consistent and grounded in the actual source files.
The research set is internally coherent and safe to proceed to synthesis on the
cross-validation dimension.
