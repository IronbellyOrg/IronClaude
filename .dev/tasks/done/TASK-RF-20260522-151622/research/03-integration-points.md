# Research: Integration Points (Downstream Wiring)

**Topic type:** Integration Points
**Scope:** SKILL.md Waves 1/3/4/5, hypothesis-card-template, report-template
**Status:** In Progress
**Date:** 2026-05-22
---

## Wiring 1: Wave 1 brief gets the Doc Context Card path

**Current location:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, Wave 1 section, lines 121-145.

The Wave 1 brief construction is on line 137 — the orchestrator spawns `root-cause-analyst` via `Task`:

> Line 137: `3. **Form one hypothesis** — spawn the`root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from step 1, the observation from step 2, and `--scope` if any. The agent's job is to produce one hypothesis card (template in `refs/hypothesis-card-template.md`) — not three, not the full tree.`

The triage-checklist (refs/triage-checklist.md, line 1: "Passed to the `root-cause-analyst` agent as part of the Tier 1 brief") is referenced in the Refs table at SKILL.md:380:
> `|`refs/triage-checklist.md`| Wave 1 (passed to root-cause-analyst as part of the brief) |`

**Recommended modification to line 137:** Append "the Documentation Context Card at `<output-dir>/doc-context.md` (from Wave 1.5; if `--no-doc-discovery` was set, pass `null` and instruct the analyst to set `consistency_with_docs: not_applicable`)" to the brief contents. The card path joins the symptom/grounding/observation/scope list. Suggested replacement clause: "...the symptom, the grounding from step 1, the observation from step 2, the Documentation Context Card path (`<output-dir>/doc-context.md`, or `null` when Wave 1.5 was skipped via `--no-doc-discovery`), and `--scope` if any."

**Hypothesis card field requirement:** Line 137 also references `refs/hypothesis-card-template.md`. The brief must additionally include the instruction: "The analyst's hypothesis card MUST set the new `consistency_with_docs` field (see template) to one of `aligned | conflicts | not_applicable | no_docs_found`."

**Refs table edit (line 380):** Add row `|`refs/triage-checklist.md`| Wave 1 (passed to root-cause-analyst as part of the brief) |` should be unchanged; add a new row above or below for `refs/doc-discovery-card-template.md` (if created by Researcher 4 / template work) — wave loaded at 1.5 and consumed at Wave 1/3/4/5.

---

## Wiring 2: hypothesis-card-template field extension

**File:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (107 lines).

**Current top-level metadata block** (lines 10-16, inside the template fence):

```markdown
# Hypothesis: <one-line claim, ...>

**Agent**: <agent-name>
**Tier**: <1|2>
**Timestamp**: <ISO 8601>
**Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
```

**Current section list** (verbatim headers from the template):

- L17: `## Claim`
- L21: `## Evidence`
- L29: `## Proposed Fix`
- L41: `## Confidence` (sub-fields lines 43-52)
- L54: `## Risks`
- L58: `## If I'm wrong, it's probably because...`
- L62: `## Alternatives considered`
- L66: `## Grounding gaps`

**Slot recommendation: top-level metadata block (lines 10-16), inserted as a sibling to `**Cause class**`.**

**Justification:**

- Putting it near `## Confidence` (L41-52) would mix a categorical doc-alignment verdict with numeric/per-dimension scores — semantically distinct.
- Putting it near `## Proposed Fix` (L29) would imply the field describes the *fix's* alignment, not the *hypothesis's* alignment with documented behavior.
- Putting it at the top alongside `**Cause class**` keeps it as a categorical classifier of the hypothesis (parallel to "what kind of bug is this?" → "does the documented behavior support this hypothesis?"). It also lets the calibrator and Wave 4 adversarial debate read the flag without scanning the body.

**Exact field definition to add (after line 16, before line 17's blank line):**

```markdown
**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

And under the worked example (lines 80-107), append after `**Cause class**: Missing/wrong import` at line 86:

```markdown
**Consistency with docs**: not_applicable
```

(or `aligned` for the worked example — choose whichever the worked-example narrative supports; "Missing import" has no doc-behavior implication, so `not_applicable` is the honest value).

**Filling rules addition (after line 76):** Add a new bullet to the "Filling the card" list:
>
> - **Consistency with docs** is mandatory. If the Documentation Context Card path was null (--no-doc-discovery), set `not_applicable`. If the card had no relevant refs, set `no_docs_found`. Otherwise score `aligned` or `conflicts` based on whether documented behavior supports or contradicts the proposed hypothesis.

---

## Wiring 3: Wave 3 per-agent brief gets the same card

**Current location:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, Wave 3 section, lines 167-216.

The Wave 3 per-agent brief construction is on lines 192-197:

> Lines 192-197:
> `2. **Spawn hypothesis agents** in parallel via`Task`(single message with multiple Task calls). Each agent receives:`
> `- The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)`
> `- The MCP enrichment results`
> `- The output path for their own hypothesis card:`<output-dir>/tier2-<agent-name>-hypothesis.md``
> `- An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, and a one-line "if I'm wrong it's probably because...".`
> `- Use the agent's default model. If`--models` overrides per-tier, apply (e.g. `hypothesis:opus`forces all hypothesis agents to opus).`

**Recommended modification:** Insert a new bullet between lines 193 (Tier 1 hypothesis card) and 194 (MCP enrichment) — the card is logically part of the Tier 1 grounding hand-off:

```markdown
   - The **Documentation Context Card** at `<output-dir>/doc-context.md` (the same single card produced by Wave 1.5 — agents do NOT re-run discovery). If `--no-doc-discovery` was set, this path is `null` and agents set `consistency_with_docs: not_applicable` in their hypothesis cards.
```

**And amend line 195 (output path bullet) is unchanged; amend line 196 (the instruction)** to add the field requirement:
> "...claim, evidence (cited file:line or command output), proposed fix, confidence, risks, **`consistency_with_docs` (see hypothesis-card-template.md)**, and a one-line 'if I'm wrong it's probably because...'."

**Note on single-invocation contract:** Add a sentence at the end of Wave 3 step 2 (after line 197) clarifying:
> "All 2-4 spawned agents receive the SAME card produced by the single Wave 1.5 invocation; the card is not re-derived per agent. This keeps the doc-context view consistent across hypotheses so cross-agent comparison in Wave 4 is apples-to-apples."

---

## Wiring 4: Wave 4 adversarial weighting + doc-update-bundle output

**Current location:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, Wave 4 section, lines 219-244.

The `/sc:adversarial` invocation is on lines 228-238:

> Lines 228-238:
> `2. **Invoke`/sc:adversarial` in compare mode** via `Skill`:`
>
> ```
> Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \
>     --depth quick (when source signals are strong) | standard (default) \
>     --focus correctness,risk,test-coverage \
>     --output <output-dir>/adversarial/
> ```
>
> `- Use`--depth quick`if all proposals share the same diagnosis and only differ in the fix mechanism (fast debate is sufficient).`
> `- Use`--depth standard`otherwise.`

The merged-output collection is on line 239:
> `3. **Collect adversarial output** —`<output-dir>/adversarial/`will contain the standard 6 artifacts (`diff-analysis.md`,`debate-transcript.md`,`base-selection.md`,`refactor-plan.md`,`merge-log.md`,`merged-output.md`). The merged output is the **chosen fix proposal**.`

**Recommended modifications:**

**(a) Add a `--context-file` flag** to the `/sc:adversarial` invocation (lines 230-235). The skill already accepts `--focus`; the Restrictions section is a weighting input not a focus area. Replacement block:

```markdown
   ```

   Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \
       --depth quick (when source signals are strong) | standard (default) \
       --focus correctness,risk,test-coverage,documented-constraints \
       --context-file <output-dir>/doc-context.md \
       --output <output-dir>/adversarial/

   ```
```

(`--context-file` lets the adversarial skill load the Documentation Context Card's Restrictions section as a weighting input. The `documented-constraints` focus tag tells the debate to apply it.)

**(b) Add a weighting instruction** as a new bullet after line 238 (the `--depth standard` bullet):
>
> - **Weighting rule**: the adversarial debate MUST treat any documented constraint in the Restrictions section of `<output-dir>/doc-context.md` as a hard preference: a fix that violates a documented constraint is either rejected outright, or wrapped as a **documentation-update + fix bundle** (see step 3 output mode).
> - When `--no-doc-discovery` was set (no card produced), omit `--context-file` and `documented-constraints` from the invocation; the debate runs against correctness/risk/test-coverage alone.

**(c) Extend the merged-output description** (line 239) to add the bundle case:
> Replace the trailing sentence "The merged output is the **chosen fix proposal**." with:
> "The merged output is the **chosen fix proposal**. If the debate flagged that the winning proposal requires a doc update to remove or rewrite a documented constraint, the merged output is structured as a **doc-update + fix bundle**: the bundle lists the doc file(s) to update alongside the code change(s), and Wave 5's Proposed Fix section renders both atoms."

---

## Wiring 5: Wave 5 REPORT.md Documentation Context section

**Current location:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, Wave 5 section, lines 248-289.

REPORT.md composition is on lines 254-263 (the section list filled in):

> Lines 255-263:
> `2. Compose`REPORT.md`filling in:`
> `- Header (target, tier reached, confidence, escalation reason)`
> `- Summary (2-4 sentence executive summary)`
> `- Diagnosis (the chosen hypothesis — from Tier 1 alone, or from the adversarial merge)`
> `- Evidence (cited`file:line`and command outputs)`
> `- Proposed Fix (the recommended change)`
> `- Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)`
> `- Risk + Rollback (what to watch after applying)`
> `- Next Steps (...)`

**REPORT template section order** (from refs/report-template.md):

- L8: Header (frontmatter-style)
- L23: `## Summary`
- L29: `## Diagnosis`
- L39: `## Evidence`
- L49: `## Proposed Fix`
- L65: `## Alternative Fixes Considered`
- L76: `## Risk + Rollback`
- L86: `## Follow-up tasks`
- L98: `## Grounding Gaps`
- L108: `## Next Steps`
- L118: `## Audit`

**Insertion-point recommendation: between `## Summary` (L23-27) and `## Diagnosis` (L29-37), as a new `## Documentation Context` section.**

**Rationale:**

- Summary is a 2-4 sentence answer; Diagnosis is the chosen hypothesis. The reader is in "set the stage" mode here.
- Documentation Context tells the reader "here is the documented behavior these findings were judged against" — that primes them to evaluate the Diagnosis correctly.
- Placing it after Diagnosis (between Diagnosis and Evidence) would read as "here's the answer, and oh by the way here's the docs we checked" — out of order.
- Placing it after Proposed Fix would let a reader skim the fix without seeing the documented constraints it had to honor — defeats the purpose.
- Placing it between Evidence and Proposed Fix would split the "what is the bug" → "how do we fix it" flow with a context detour — wrong cut.
- Summary → Documentation Context → Diagnosis preserves the "frame → evaluate the answer" flow.

**Section template to add (insert after line 27 in report-template.md, before line 29):**

```markdown
## Documentation Context

A ≤6-line summary of the Documentation Context Card produced by Wave 1.5. Format:

- **Relevant refs**: <comma-separated file paths, or "None found">
- **Documented behavior**: <one-line summary of what the docs say about the affected surface>
- **Restrictions honored**: <one-line list of doc-cited constraints the chosen fix respects>
- **Restrictions overridden**: <one-line list of doc-cited constraints the chosen fix violates; cite the doc-update + fix bundle if applicable, otherwise "None">
- **Card path**: <output-dir>/doc-context.md

If `--no-doc-discovery` was set, omit this section entirely and add a line to **Grounding Gaps**: "Documentation grounding skipped by --no-doc-discovery."
```

**SKILL.md Wave 5 step 2 edit (line 256-263):** Insert a new bullet between line 257 (Summary) and line 258 (Diagnosis):
> `- Documentation Context (≤6-line summary of the Wave 1.5 Documentation Context Card; omit and record in Grounding Gaps if --no-doc-discovery was set)`

---

## Wiring 6: report-template.md `behavior_is_documented` field

**Current `test_is_wrong` field in refs/report-template.md** (lines 16-17, header block, verbatim):

> Line 16: `**Test is wrong**: <true|false> <!-- See "Test-is-wrong rule" below. When true, surface`Test file to update`on its own line and DO NOT recommend code changes as the primary fix. -->`
> Line 17: `**Test file to update**: <absolute or repo-relative path when test_is_wrong=true, otherwise omit this line>`

The semantic mirror: `test_is_wrong=true` → fix the test, not the code. `behavior_is_documented=true` → the diagnosed behavior is documented as intended, so recommend a spec/docs change (or a discussion with stakeholders) rather than a code change.

**Recommended mirror entry to add (immediately after line 17, before the blank line at L18-19):**

```markdown
**Behavior is documented**: <true|false> <!-- See "Behavior-is-documented rule" below. When true, the observed behavior matches the documented contract — the report recommends a SPEC/DOCS change (or an explicit "won't fix") rather than a code change as the primary remediation. Mutually exclusive with `Test is wrong: true`. -->
**Doc context card**: <repo-relative path to <output-dir>/doc-context.md, or `null` when --no-doc-discovery was set>
```

**Section recommendation (mirroring lines 134-153 "Test-is-wrong rule"):** Add a new top-level `## Behavior-is-documented rule` section after line 153, mirroring the structure of "Test-is-wrong rule". Trigger conditions:

1. Wave 1.5 produced a Documentation Context Card with a `Documented behavior` entry that matches the observed symptom (not the user's expected behavior).
2. The hypothesis card's `consistency_with_docs` field is `aligned` (the bug IS the documented behavior).
3. The fix would require a change to either the documented behavior (spec/docs update) or a stakeholder-level discussion about whether the doc should change.

**Companion rendering rules to add** (mirroring lines 144-150):

- The Summary section MUST open with "The reported issue is the documented behavior — a code change would regress the documented contract."
- The Proposed Fix section's `Files to change` list MUST contain ONLY the doc/spec file(s) — not code.
- A `## Files that MUST NOT change` subsection MUST appear listing every code file a careless remediation might touch.
- Alternative Fixes Considered MUST include "modify the code to change the documented behavior" with rejection reason "**This is the DANGEROUS wrong answer** — would silently break the documented contract for downstream consumers."

---

## Wiring 7: Output Contract dict extension

**Current location:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Output Contract table, lines 41-55.

**Verbatim `test_is_wrong` and `test_file_path` rows (lines 49-50):**

> Line 49: `|`test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |`
> Line 50: `|`test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g.,`tests/api/test_foo.py`), resolved against the repo root containing`.git/`.`null`otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |`

**Recommended new rows (insert immediately after line 50, before `hypothesis_cards` at line 51):**

```markdown
| `behavior_is_documented` | bool | `true` when the diagnosis concludes the reported behavior is the documented behavior (i.e., a code change would regress the documented contract). Set independent of tier; mutually exclusive with `test_is_wrong=true`. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a code fix when this is `true`; the remediation target is the spec/docs file(s), or a stakeholder-level discussion. Derived from the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concluding the observed symptom IS the documented behavior. |
| `doc_context_card_path` | string \| null | When Wave 1.5 ran, the **repo-relative** path of the Documentation Context Card (e.g., `.dev/troubleshoot/bug-foo-20260522/doc-context.md`). `null` when `--no-doc-discovery` was set OR when Wave 1.5 produced no relevant docs (`no_docs_found`). Format is repo-relative, same convention as `test_file_path`. |
```

**Conditional-presence rules:**

- `behavior_is_documented` is always present (bool, default `false`). It is set independently of tier.
- `doc_context_card_path` is always present (string OR null). When `--no-doc-discovery` was set, it is `null`. When Wave 1.5 ran but produced an empty card, it is the path to the empty card (NOT null) — the card existing as evidence of "we looked and found nothing" is itself signal.
- Mutual-exclusion enforcement: if `behavior_is_documented=true` AND `test_is_wrong=true`, Wave 5 MUST resolve to ONE primary remediation target (typically the spec/docs change, since the test's role is downstream of the doc). Add this rule in the synthesis prose.

**Derivation rule to add** (mirroring lines 57-65 for `test_is_wrong`):

> **`behavior_is_documented` derivation rule** (applied during Wave 5 synthesis): set `behavior_is_documented=true` when the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concludes the observed symptom IS the documented behavior (not the user's expected behavior). If the docs say the system should do X and the user reports it does X but expected Y, the bug is in the user's expectation (or the docs) — set the flag and recommend a spec change or stakeholder discussion. If `consistency_with_docs=conflicts`, the docs side with the user — keep the flag false and proceed with normal code remediation.

---

## Wiring 8: --no-doc-discovery → Grounding Gaps

**Current `## Grounding Gaps` section** in refs/report-template.md (lines 98-106, verbatim):

> Line 98: `## Grounding Gaps`
> Line 99: (blank)
> Line 100: `What the skill could **not** verify. If`status: partial`, the items here explain why. Examples:`
> Line 101: (blank)
> Line 102: `- "Reproducer not available in sandbox — relied on user-pasted stack trace"`
> Line 103: `- "MCP`auggie` was unavailable; grounding used `Grep`/`Glob`only"`
> Line 104: `- "Hypothesis card from`quality-engineer`cited line 88 of test_foo.py but that file is only 60 lines long — citation dropped"`
> Line 105: (blank)
> Line 106: `If there are no gaps, write "None."`

**Recommended skip-record line** to add as a new example bullet between lines 103 and 104:

```markdown
- "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions; consumer should re-run without `--no-doc-discovery` if doc-alignment matters."
```

**Also recommended** (as another example after L104):

```markdown
- "Wave 1.5 documentation discovery ran but found no relevant docs for the affected surface (`<surface>`) — `consistency_with_docs` set to `no_docs_found` across all hypothesis cards; downstream weighting fell back to correctness/risk/test-coverage alone."
```

**SKILL.md Wave 5 verification:** SKILL.md line 257 (the Wave 5 composition list) refers to Summary/Diagnosis/Evidence/Proposed Fix/Alternative Fixes Considered/Risk + Rollback/Next Steps. It does NOT explicitly list "Grounding Gaps" — the section is in the template (refs/report-template.md L98) but not enumerated in SKILL.md line 256-263. The template covers it implicitly via "Load `refs/report-template.md`" on line 255.

**SKILL.md Wave 5 amendment** (also covered in Wiring 5 above): when the new Documentation Context bullet is added at line 257.5, also append to step 2:
> "If `--no-doc-discovery` was set, omit the Documentation Context section AND populate the Grounding Gaps section with: 'Documentation grounding skipped by `--no-doc-discovery`.'"

This makes the skip-record behavior explicit in the orchestrator's wave logic, not just hidden inside the template.

---

## Wiring 9: triage-checklist ripple verdict

**Verdict: NO CHANGE NEEDED to refs/triage-checklist.md.**

**Evidence (full sweep of the 65-line file):**

The triage-checklist's "Pre-investigation grounding" section (lines 5-14) lists what the agent should have read before forming a hypothesis:
> Line 9: `- [ ] The exact code at the location named in the stack trace (or`--scope`if no trace)`
> Line 10: `- [ ] The auggie retrieval result that the skill provided in the brief`
> Line 11: `- [ ] The serena symbol overview / surrounding function definitions`
> Line 12: `- [ ] At least one test that exercises the suspect code path (or noted that no test exists)`

These are positioned as items the **brief provides** — they are skill-side inputs, not agent-derived ones. The Documentation Context Card is the same shape: provided by the skill (Wave 1.5) and read by the agent (Wave 1).

The "Fix sketch" section (lines 46-54) says:
> Line 48: `The Tier 1 hypothesis card includes one proposed fix. It does **not** need to be the final patch — just enough to:`

This is neutral with respect to doc-grounding — the fix sketch is described as part of the card, and the new `consistency_with_docs` field is added in the card template (Wiring 2), not the checklist.

The "When to refuse Tier 1" section (lines 56-65) lists refusal triggers. None of them mention documentation. The new doc-grounding flow does not create new refusal triggers (the absence of docs is `no_docs_found`, not a refusal).

**Why the checklist stays neutral:** The phrase "before forming a hypothesis" (line 7) does NOT enumerate doc-grounding; it lists *code/test* grounding inputs. The Documentation Context Card is a peer input to those four bullets, conceptually. An optional follow-up enhancement (not required for this task) would be to add a fifth bullet:
> `- [ ] The Documentation Context Card at the path provided in the brief (or noted "card was null due to --no-doc-discovery")`

But this is **not a blocker** — the checklist functions as a guide-rail for the analyst, and the new `consistency_with_docs` field in the hypothesis card template (Wiring 2) plus the explicit brief instruction (Wiring 1) together force the analyst to consult the card. The checklist remains correct as-is; expanding it is optional polish, not required wiring.

**Recommendation:** Skip editing refs/triage-checklist.md in this task. Note the optional 5th-bullet enhancement in the task file's "Future Enhancements" section if one exists; otherwise no action required.

---

## Summary

Downstream edit points required for Wave 1.5 Documentation Context Card integration:

- **SKILL.md L137** — Wave 1 brief: append Documentation Context Card path + `consistency_with_docs` field requirement to the root-cause-analyst brief construction.
- **SKILL.md L192-197** — Wave 3 per-agent brief: insert new bullet for the Documentation Context Card path (single Wave 1.5 invocation, shared across 2-4 agents); amend instruction to require `consistency_with_docs` field.
- **SKILL.md L228-238** — Wave 4 adversarial: add `--context-file <doc-context.md>` and `documented-constraints` focus tag to the `/sc:adversarial` invocation; add weighting-rule bullet; cover `--no-doc-discovery` fallback.
- **SKILL.md L239** — Wave 4 output: extend merged-output description to include the doc-update + fix bundle case.
- **SKILL.md L256-263** — Wave 5 composition: insert "Documentation Context" bullet between Summary and Diagnosis; add explicit `--no-doc-discovery` → Grounding Gaps clause.
- **SKILL.md L49-50 (Output Contract)** — add `behavior_is_documented` (bool) and `doc_context_card_path` (string|null) rows immediately after `test_file_path`; add derivation rule mirroring lines 57-65.
- **SKILL.md L380** — Refs table: ensure new `refs/doc-discovery-card-template.md` row added (loaded Wave 1.5, consumed Wave 1/3/4/5).
- **refs/hypothesis-card-template.md L16** — add `**Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>` to the top metadata block (sibling to Cause class); also update worked example (L86) and Filling rules (L76).
- **refs/report-template.md L17** — add `**Behavior is documented**` and `**Doc context card**` header rows immediately after `Test file to update`; add new top-level `## Behavior-is-documented rule` section after L153 mirroring the Test-is-wrong rule (L134-153).
- **refs/report-template.md L27/L29 boundary** — insert new `## Documentation Context` section between Summary and Diagnosis (≤6-line summary format defined in Wiring 5).
- **refs/report-template.md L98-106** — add two new example bullets to Grounding Gaps covering the `--no-doc-discovery` skip case and the `no_docs_found` case.
- **refs/triage-checklist.md** — NO CHANGE required (verdict: Wiring 9). Optional 5th-bullet polish noted but not required.

**Status: Complete**
