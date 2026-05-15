# Research: FR-CONV.3 (PR-04) Inherited Structural Verdict + Self-Audit Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** B (sc:tasklist has passthrough mechanism; task-builder is silent — no conflict)
**Conflict-register row:** NONE (CASE-B correctly omitted)
**Protected invariant:** zero-trust QA (anti-inflation rule at rf-qa-qualitative.md:766-775 MUST NOT be weakened)
**Lands:** 3rd of 6 FRs

---

## 1. Verified-Current Insertion Points

### Site A — task-builder SKILL.md A.10.5 (PRD-cited `SKILL.md:923-1000`)

**File:** `src/superclaude/skills/task-builder/SKILL.md` (1709 lines total)
**Verified range:** lines 923-1000 (`sed -n '920,1002p'`). PRD-cited range is current — no drift.

Verbatim excerpt (anchor + key spawn-prompt segment that must receive the `## Inherited Structural Verdict` block):

```
923  ### A.10.5: Task File Qualitative Validation
924
925  After structural QA passes, validate that the task file would actually succeed
     if executed. This step catches operational issues that structural QA cannot:
     gates that will fail, function signatures that don't match the described
     modifications, downstream dependencies not updated, tests that exercise
     stubs instead of real artifacts, and runtime paths that break partway
     through.
926
927  **Spawn rf-qa-qualitative:** Use the Agent tool with
     `subagent_type: "rf-qa-qualitative"`, `mode: "bypassPermissions"`.
...
939  **QA prompt:**
940  ```
941  QA_PHASE: task-qualitative
942  fix_authorization: true
943
944  TASK FILE: [path to the task file]
945  RESEARCH DIR: ${TASK_DIR}research/
946  TRACK GOAL: [goal for this track]
...
967  **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to
     find what was missed, not confirm everything is fine. Verify every claim
     exhaustively. A verdict of 0 issues requires evidence you thoroughly
     checked.
968
969  INSTRUCTIONS:
970  Apply the 15-item Task File Qualitative Review checklist from your agent
     definition. For each checklist item that requires reading source code,
     read the ACTUAL target files — do not rely on research file summaries alone.
...
997  OUTPUT FILE: ${TASK_DIR}qa/qa-qualitative-review.md
998
999  Write the file IMMEDIATELY with a header, then append findings incrementally.
1000 ```
```

**Insertion-point analysis:** The `## Inherited Structural Verdict` block must be injected into the spawn-prompt body (the fenced block between lines 940 and 1000) **after** the `TARGET FILES` enumeration and **before** the `INSTRUCTIONS:` directive — i.e. between current line 966 and current line 969. This positions the inherited verdict as a referenceable context block the rf-qa-qualitative agent reads BEFORE applying its 15-item checklist, allowing it to skip structural re-checking for PASS items and flag FAIL items HIGH.

The orchestrator (task-builder skill itself, executing A.10.5) is the responsible party for: (a) reading rf-qa's emitted `task-integrity` verdict report, (b) extracting the Items Reviewed table verbatim, (c) splicing it into the spawn-prompt template with the prompt-directive language, and (d) on fix-cycle reruns, re-extracting the NEW (cycle-N) verdict and re-injecting it (INV-002 reinjection rule, see §3).

### Site B — rf-qa-qualitative.md insertion site (PRD-cited `rf-qa-qualitative.md:794`)

**File:** `src/superclaude/agents/rf-qa-qualitative.md` (794 lines total — line 794 is end-of-file)
**Verified range:** lines 790-794 (`sed -n '790,794p'`). PRD-cited line 794 = EOF — drift-free, but the insertion point is structurally "append a new section at end-of-file" (or alternatively: insert ABOVE one of the lower-numbered anchor sections — see analysis).

Verbatim excerpt of the end of the file (the structural anchor that bounds the insertion):

```
780  ### Prohibited Behaviors  (← line 766 in actual file, repeated for context;
                                  see §7 anti-inflation verbatim)
...
794  11. **You complement rf-qa, not replace it** — rf-qa checks structural
     correctness (section numbers, cross-references, evidence citations,
     template conformance). You check whether the content makes sense. Don't
     re-verify section numbering or file existence — focus on whether the
     content is correct, complete, logical, and appropriately scoped.
[EOF]
```

**Insertion-point analysis:** The PRD-cited line `794` refers to the trailing section of rf-qa-qualitative.md ("Critical Rules" block, items 1-11 ending at line 794). The Inherited Structural Verdict handling instructions (how the agent should treat the inherited verdict block when it appears in the spawn prompt, and how it must produce the `## Self-Audit` section in its output) are added as a NEW section appended after line 794. Recommended new section heading: `### Handling the Inherited Structural Verdict` (sibling of the existing items 1-11 list, or alternately a top-level `## ...` section under whichever H2 contains "Critical Rules").

A second touch point inside rf-qa-qualitative.md is the output-template section (the agent's output report schema, parallel to rf-qa.md:320-365 verdict template) — the `## Self-Audit` section must be added to the rf-qa-qualitative output schema so the agent produces it on every run. This is a SECOND insertion point co-located with the existing output template; the PRD calls out only the line-794 site, but a complete FR-CONV.3 landing edits both: (1) the handling-rule prose near EOF and (2) the output-schema block.

### Site C — Anti-inflation rule (PRD-cited `rf-qa-qualitative.md:766-775` — MUST NOT WEAKEN)

**File:** `src/superclaude/agents/rf-qa-qualitative.md`
**Verified range:** lines 766-775 (`sed -n '766,780p'`). Drift-free.

Verbatim excerpt (this rule is the **protected invariant** for FR-CONV.3):

```
766  ### Prohibited Behaviors
767  - NEVER adjust confidence based on subjective feeling — it is COMPUTED
     from the checklist
768  - NEVER report confidence without the raw numbers
769  - NEVER claim VERIFIED without citing specific tool output (file path,
     line number, grep result)
770  - NEVER mark an item VERIFIED if you only read about it in another
     report — that is RELIANCE, not VERIFICATION
771  - NEVER issue a PASS verdict without meeting the threshold
772  - NEVER make generic tool calls to inflate engagement counts — each tool
     call must directly verify a specific checklist item. A Read call must
     target the file being verified, a Grep must search for the specific claim
     being checked. Tool calls that don't map to specific verifications are
     padding, not evidence.
773
774  ### Tool Engagement Minimum
775  If your total (Read + Grep + Glob) calls < TOTAL checklist items, the
     review is automatically suspect. You cannot have verified more items than
     you made tool calls. Flag this in your report.
```

This block is the **anti-inflation rule** referenced by the FR-CONV.3 negative criterion and NFR-CONV.9 (zero-trust QA invariant). FR-CONV.3 MUST add semantics ON TOP of this rule (the Inherited Verdict ENABLES skipping structural re-checking; it does NOT permit marking semantic checks VERIFIED without an independent tool call). See §7 below.

---

## 2. Inherited Structural Verdict Block Schema (PRD §25.2)

Per FR-CONV.3 acceptance criterion (PRD §14.1 / extraction §FR-CONV.3 line 100):

The injected block has three required components:

### 2.1 `rf_qa_table_verbatim`

The full **Items Reviewed** table emitted by rf-qa during the `task-integrity` QA phase, copied byte-for-byte from rf-qa's verdict report (template at `rf-qa.md:328-330`, output file path conventionally `${TASK_DIR}qa/qa-task-integrity.md`).

The verbatim table schema (from `rf-qa.md:328-330`):

```
## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | [check name] | PASS / FAIL | [what you verified and how] |
...
```

Plus the **Overall Verdict** line (`## Overall Verdict: [PASS / FAIL]`, from `rf-qa.md:327`) and the **Summary** counts (from `rf-qa.md:332-336`). The orchestrator MUST extract these contiguous sections verbatim — no paraphrase, no reformatting, no field-renaming.

### 2.2 `prompt_directive`

Verbatim directive language (from PRD §FR-CONV.3, extraction line 97):

> "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."

This directive is appended **immediately after** the verbatim rf-qa table inside the spawn prompt. It tells rf-qa-qualitative how to **consume** the inherited verdict: structural PASS items are off the table for re-verification (saves redundant tool calls); structural FAIL items become HIGH-severity flags in the qualitative report (the qualitative agent doesn't re-prove the structural defect — rf-qa already did — but its presence makes adjacent semantic checks suspect).

### 2.3 `reinjection_rule`

Verbatim (from PRD §FR-CONV.3, extraction line 100, INV-002):

> "On a fix-cycle re-run, the orchestrator re-injects the NEW verdict."

The orchestrator (task-builder A.10.5) MUST, on every spawn (cycle 1, 2, 3, ... up to the rf-qa-qualitative 3-fix-cycle limit), re-read the **current** rf-qa task-integrity report and re-extract the table. Stale verdicts from prior cycles are forbidden. See §3 for the cycle-N+1 mechanism.

### 2.4 Block formatting (recommended template)

```
## Inherited Structural Verdict

The following table is rf-qa's task-integrity verdict for THIS cycle, copied
verbatim from ${TASK_DIR}qa/qa-task-integrity.md. Treat as machine-verified:

<verbatim rf-qa Overall Verdict line>
<verbatim rf-qa Items Reviewed table>
<verbatim rf-qa Summary counts>

DIRECTIVE: PASS items machine-verified — skip structural re-checking; FAIL items
machine-verified defects — flag HIGH. Focus on semantic quality.
```

---

## 3. INV-002 — Cycle-N+1 Reinjection Rule

**Statement (verbatim from PRD extraction §FR-CONV.3 line 100):** "on a fix-cycle re-run, the orchestrator re-injects the NEW verdict (INV-002); ... no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions."

**Operational mechanism:**
1. Cycle 1: rf-qa task-integrity emits verdict V1 → orchestrator extracts V1 → injects `## Inherited Structural Verdict` block containing V1 into rf-qa-qualitative spawn-1.
2. If qualitative spawn-1 returns FAIL, fixes are applied (either by rf-qa-qualitative in-place per A.10.5 `fix_authorization: true`, or by user).
3. Cycle 2: rf-qa is re-spawned (task-integrity re-runs over fixed task file) → emits verdict V2 → orchestrator extracts V2 → injects V2 into rf-qa-qualitative spawn-2. **V1 is discarded.** Orchestrator MUST NOT carry V1 forward into spawn-2.
4. Cycle 3 (final permitted): same pattern. After cycle 3 unresolved → HALT (rf-qa-qualitative.md "Maximum 3 fix cycles" rule at line 793 item 10).

**Implementation invariant:** The orchestrator's extraction step MUST re-read the rf-qa verdict file on every spawn (no caching). Equivalently: the rf-qa report file path is read at A.10.5 entry on every cycle, never memoized from a prior cycle's read.

**Verification:** Synthetic 2-cycle fixture (per PRD verification method, extraction line 101) — `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N for both cycles; the block content for cycle 2 byte-matches V2 (NOT V1).

---

## 4. INV-010 — Dynamic Checklist Enumeration Rule

**Statement:** The rf-qa task-integrity checklist size is computed dynamically from the TB-Add catalogue at spawn time. FR-CONV.3's inherited-verdict consumer therefore richens automatically when FR-CONV.1's TB-Add items go live.

**Ordering dependency:** This is the architectural reason FR-CONV.1 must land **1st** (it adds the TB-Add catalogue entries that the rf-qa checklist enumerates) before FR-CONV.3 lands **3rd** (it consumes the verdict whose row-count is determined by the TB-Add catalogue size).

**Operational mechanism:**
- rf-qa task-integrity checklist is not a fixed-length list — it enumerates over the TB-Add catalogue (TB-Add-1 through TB-Add-N). When FR-CONV.1 adds new TB-Add items (e.g., TB-Add-7 cross-validation, TB-Add-8 hidden-input guard), rf-qa's task-integrity phase automatically grows its row count.
- The `## Inherited Structural Verdict` block size in FR-CONV.3's spawn injection is therefore a function of the TB-Add catalogue: 6 TB-Add items → 6+ rows; 12 TB-Add items → 12+ rows. No source-code edit to FR-CONV.3's mechanism is required when FR-CONV.1 grows; the verdict-extraction logic is already row-agnostic (it copies the table verbatim).
- This decoupling is why the PRD prescribes FR-CONV.3 to land **after** FR-CONV.1 — landing in reverse order would mean FR-CONV.3 ships with a half-empty verdict table.

**Verification (PRD extraction line 100):** "the spawn prompt's checklist enumeration is dynamic (auto-picks up TB-Add catalogue from FR-CONV.1, INV-010)."

---

## 5. INV-019 — Self-Audit Mandate

**Statement (verbatim from PRD extraction §FR-CONV.3 line 100):** "rf-qa-qualitative's first run after FR-CONV.3 lands produces a `## Self-Audit` entry listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019)."

**K-003 audit target:** The first **5** real runs of rf-qa-qualitative after FR-CONV.3 lands MUST produce a `## Self-Audit` entry that:
1. Lists every rf-qa PASS item the qualitative agent relied on (i.e. items the qualitative agent skipped structural re-checking for, per the directive in §2.2).
2. Includes **≥1 semantic check** where the rf-qa PASS verdict is **insufficient** — i.e. a check the qualitative agent performed independently because structural PASS does not imply semantic correctness (e.g. "rf-qa PASS confirms the function signature exists; qualitative re-checked whether the function's behavior matches the checklist item's claim about its effect on downstream consumers").

**Why the ≥1 floor matters:** It enforces that the qualitative agent does NOT degenerate into a verdict-rubber-stamp. If a qualitative run's Self-Audit contains 0 semantic-beyond-PASS entries, the qualitative agent has effectively just echoed rf-qa — a violation of "You complement rf-qa, not replace it" (rf-qa-qualitative.md:794).

**Output-schema location:** The `## Self-Audit` section is added to rf-qa-qualitative's output template (parallel placement to existing schema sections at `rf-qa.md:325-368`). It is co-located with the report's verdict in the same output file (`${TASK_DIR}qa/qa-qualitative-review.md`).

**Self-Audit section template (recommended):**

```
## Self-Audit

### Relied-on rf-qa PASS items (structural re-check skipped)
- [item N from rf-qa Items Reviewed table]: relied on rf-qa PASS for [aspect];
  did not re-verify because [reason — typically: structural-only concern]

### Semantic checks beyond inherited PASS
- [semantic check K]: rf-qa PASS confirms [structural fact]; qualitative
  independently verified [semantic claim] by [tool call + evidence].
  Tool engagement: [Read|Grep|Glob] target [file:line] returned [result].

[≥1 entry required]
```

**Auditability:** Per K-003, the first 5 runs of rf-qa-qualitative post-FR-CONV.3 are subject to audit. The audit verifies (a) `## Self-Audit` section is present, (b) at least 1 entry exists under "Semantic checks beyond inherited PASS", and (c) each such entry cites a tool call with evidence (no entries without tool-output citation — that would violate the anti-inflation rule at line 770).

---

## 6. Acceptance Criteria (PRD §14.1 FR-CONV.3)

Per PRD extraction lines 100-102:

### 6.1 Observable behavior
- rf-qa-qualitative's spawn prompt contains a section literally headed `## Inherited Structural Verdict`.
- The block under that heading byte-matches rf-qa's emitted Items Reviewed table verbatim.
- On a fix-cycle re-run, the orchestrator re-injects the **NEW** (cycle-N) verdict — not the stale (cycle-N-1) verdict.
- The spawn prompt's checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010).
- rf-qa-qualitative's first run after FR-CONV.3 lands produces a `## Self-Audit` entry listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).

### 6.2 Verification method
- Capture the rf-qa-qualitative spawn-prompt log (the verbatim prompt sent to the Agent tool at A.10.5 spawn).
- `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N.
- The block immediately below matches rf-qa's emitted verdict table byte-for-byte (diff against `${TASK_DIR}qa/qa-task-integrity.md` should show the Items Reviewed table as a contiguous identical substring).
- On a synthetic 2-cycle fixture, the second cycle's spawn log shows the NEW (cycle-2) verdict, not the stale (cycle-1) verdict.
- The same fixture's rf-qa-qualitative output contains a `## Self-Audit` section with ≥1 entry per category in §5.

### 6.3 Negative criteria (Out of scope / Must not break)
- rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing.
- Anti-inflation rule `rf-qa-qualitative.md:766-775` MUST NOT be weakened, removed, or rephrased.
- No stale verdict from a prior fix cycle is permitted to govern current-cycle decisions.

---

## 7. Anti-Inflation Rule Verbatim Quote and Why FR-CONV.3 Must NOT Weaken It

### Verbatim quote (rf-qa-qualitative.md:766-775, sed-verified)

```
### Prohibited Behaviors
- NEVER adjust confidence based on subjective feeling — it is COMPUTED from the checklist
- NEVER report confidence without the raw numbers
- NEVER claim VERIFIED without citing specific tool output (file path, line number, grep result)
- NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION
- NEVER issue a PASS verdict without meeting the threshold
- NEVER make generic tool calls to inflate engagement counts — each tool call must directly verify a specific checklist item. A Read call must target the file being verified, a Grep must search for the specific claim being checked. Tool calls that don't map to specific verifications are padding, not evidence.

### Tool Engagement Minimum
If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is automatically suspect. You cannot have verified more items than you made tool calls. Flag this in your report.
```

### Why FR-CONV.3 must NOT weaken this rule

The rule line **770** is the load-bearing constraint:

> "NEVER mark an item VERIFIED if you only read about it in another report — that is RELIANCE, not VERIFICATION"

FR-CONV.3 introduces a deliberately-permitted RELIANCE channel (the `## Inherited Structural Verdict` block). On its face, this looks like it could be read as relaxing the rule. **It does not.** The mechanism splits responsibilities:

- **Structural checks** (cited rf-qa's domain — section numbering, cross-reference syntax, evidence-citation presence, file-existence): rf-qa is the authoritative verifier. Once rf-qa emits PASS for a structural item, the inherited-verdict mechanism lets rf-qa-qualitative **skip structural re-checking** without flagging it as RELIANCE. This is safe because rf-qa is treated as a machine-verifier (no semantic judgement was deferred).
- **Semantic checks** (rf-qa-qualitative's domain — whether claims make sense, whether function behavior matches stated effect, whether scope is appropriate): rf-qa-qualitative MUST verify these **independently with its own tool calls**. The anti-inflation rule continues to apply: every VERIFIED semantic claim must cite a Read/Grep/Glob with file path + line number + result.

The Self-Audit mandate (INV-019, §5) operationalises this split. By forcing rf-qa-qualitative to **list** the rf-qa PASS items it relied on, and **separately** list ≥1 semantic check where rf-qa PASS is insufficient, the Self-Audit makes RELIANCE auditable — and makes the "semantic checks beyond inherited PASS" category a non-bypassable floor. A run with 0 entries in that category is a violation, not a clean run.

**NFR-CONV.9 cross-reference (extraction line 187):** "FR-CONV.3 inherited verdict does NOT mark items VERIFIED in absence of independent semantic check." This is the gate test for FR-CONV.3 acceptance — a synthetic fixture with 1 LOW finding must still FAIL the gate (zero-trust QA preserved), and the inherited-verdict mechanism must not provide a backdoor PASS.

**Implementation safeguard:** The "Handling the Inherited Structural Verdict" section added near rf-qa-qualitative.md:794 (Site B in §1) MUST contain explicit language re-affirming the anti-inflation rule applies to semantic checks. Recommended wording: "The Inherited Structural Verdict permits skipping STRUCTURAL re-checks (rf-qa's domain). It does NOT permit marking SEMANTIC items VERIFIED without an independent tool call. Items 770 and 772 of Prohibited Behaviors apply unchanged to all semantic verification."

---

## 8. Dependencies on Other FRs

### 8.1 Dependency on FR-CONV.1 (TB-Add catalogue lands 1st)

- **What FR-CONV.1 delivers:** New TB-Add catalogue entries (TB-Add-7, TB-Add-8, etc.) that rf-qa's task-integrity checklist enumerates.
- **How FR-CONV.3 consumes it:** The `## Inherited Structural Verdict` block contains the rf-qa Items Reviewed table verbatim. The table's row count is the TB-Add catalogue size at runtime. When FR-CONV.1 grows the catalogue, FR-CONV.3's injected block grows automatically (INV-010 dynamic enumeration, §4).
- **Why order matters:** If FR-CONV.3 lands before FR-CONV.1, the verdict block ships with only the pre-existing checklist rows — the new TB-Add semantics aren't yet in scope. Worse, the rf-qa-qualitative agent has no `## Inherited Structural Verdict` machinery to consume new TB-Add findings the day FR-CONV.1 lands. Landing FR-CONV.1 first ensures the consumer (FR-CONV.3) richens automatically when activated.

### 8.2 Dependency on FR-CONV.2 (Execution Context — TB-Add-7 cross-validation runs at A.10 before A.10.5 spawn)

- **What FR-CONV.2 delivers:** Execution context enforcement at A.10 (rf-qa task-integrity spawn) — specifically, TB-Add-7's cross-validation between BUILD_REQUEST inputs and the generated checklist.
- **How FR-CONV.3 consumes it:** TB-Add-7's cross-validation produces a verdict row in rf-qa's Items Reviewed table at A.10. Because A.10.5 (FR-CONV.3's injection point) runs **after** A.10, that row is already in the verdict by the time FR-CONV.3 extracts and injects it. FR-CONV.3 therefore relies on FR-CONV.2 having executed earlier in the pipeline; no additional plumbing is needed in FR-CONV.3.
- **Why order matters:** FR-CONV.2 lands 2nd of 6, FR-CONV.3 lands 3rd. This ordering guarantees TB-Add-7 cross-validation evidence is part of the inherited verdict table from FR-CONV.3's first activation. If FR-CONV.3 landed before FR-CONV.2, the verdict-injection mechanism would work, but the cross-validation evidence would be missing from the injected table until FR-CONV.2 caught up.

### 8.3 Independence from later FRs

- FR-CONV.4 (Five Adversarial Axes overlay, PR-07): consumes rf-qa-qualitative output, not rf-qa task-integrity verdict. FR-CONV.4 lands 4th and composes cleanly with FR-CONV.3 per INV-013 (PRD extraction line 125: "5 axes apply to items NOT covered by inherited PASS — composition is clean").
- FR-CONV.5, FR-CONV.6: no direct dependency on FR-CONV.3 mechanism.

---

## 9. Gaps and Questions

### 9.1 Resolved during research
- **PRD-cited line `SKILL.md:923-1000`** — verified current; no drift; A.10.5 section spans this range. ✅
- **PRD-cited line `rf-qa-qualitative.md:794`** — verified as end-of-file; insertion is append-at-end (or new section before EOF). ✅
- **PRD-cited line `rf-qa-qualitative.md:766-775`** — verified verbatim; anti-inflation rule is current. ✅

### 9.2 Open questions for TDD authors
- **Q1 (output schema):** Is the `## Self-Audit` section added to rf-qa-qualitative's existing output template (alongside Overall Verdict / Items Reviewed / Summary), or as a SEPARATE block appended after the main verdict? Recommendation: integrate into the existing template at the same level as "Issues Found" — keeps the output schema cohesive. Confirm during TDD.
- **Q2 (extraction tool):** Does the orchestrator (task-builder A.10.5) extract the rf-qa verdict via a Read+regex of `${TASK_DIR}qa/qa-task-integrity.md`, or via a structured handoff (rf-qa emits a separate `*.verdict.json` artefact)? The current rf-qa template is markdown-only; recommend Read+regex extraction (no schema change to rf-qa) to keep FR-CONV.3 self-contained. Confirm during TDD.
- **Q3 (negative-test fixture):** The PRD verification method (extraction line 101) prescribes a synthetic 2-cycle fixture. Who builds it — task-builder repo test suite (`tests/...`) or a one-off `.dev/eval-workspaces/` artefact? Default: `tests/skills/task_builder/test_inherited_verdict.py` plus a fixture under `tests/fixtures/inherited-verdict-2-cycle/`. Confirm during TDD.
- **Q4 (audit visibility for K-003):** Per INV-019, the first 5 real runs after landing are audited. Where is the audit log retained — committed to repo under `docs/audits/`, or ephemeral session artefacts? Defer to TDD; current `.dev/` model suggests `.dev/audits/fr-conv-3-k003/`.

### 9.3 Conflict-register clarification
PRD §FR-CONV.3 distribution row is **CASE-B** (extraction line 225: "PR-04 B"). CASE-B = sc:tasklist already has a passthrough mechanism; task-builder is silent. Therefore NO conflict-register row is generated for FR-CONV.3 (conflict register has exactly 5 rows for CASE-D proposals). This is correct and intentional — no remediation needed.

---

## 10. Stale Documentation Found

None. All three PRD-cited line ranges (`SKILL.md:923-1000`, `rf-qa-qualitative.md:794`, `rf-qa-qualitative.md:766-775`) are verified current with no drift.

**Note on `[NEEDS-VERIFICATION-IN-PHASE-2]` markers in PRD extraction:** The PRD extraction file (`00-prd-extraction.md` line 97, 102, 106) flags all three sites as `[NEEDS-VERIFICATION-IN-PHASE-2]`. This document fulfils that Phase-2 verification — all three line references are confirmed accurate as of 2026-05-14.

**Note on rf-qa.md known-drift:** PRD extraction line 187 (NFR-CONV.9) cites `rf-qa.md:140-142` for the "zero-trust QA" stance and acknowledges drift to `rf-qa.md:144-146`. This drift is outside FR-CONV.3's edit footprint (rf-qa.md, not rf-qa-qualitative.md) and does not affect FR-CONV.3 landing.

---

## 11. Summary

FR-CONV.3 (PR-04) lands the Inherited Structural Verdict + Self-Audit mechanism by editing two files: `src/superclaude/skills/task-builder/SKILL.md` (A.10.5 spawn prompt at lines 923-1000, insertion at line ~966 inside the spawn-prompt fenced block) and `src/superclaude/agents/rf-qa-qualitative.md` (append handling-rule section after line 794 and add `## Self-Audit` to the output schema). All three PRD-cited line ranges are verified current; no drift was found, resolving the `[NEEDS-VERIFICATION-IN-PHASE-2]` markers. The protected invariant — the anti-inflation rule at rf-qa-qualitative.md:766-775 — must remain verbatim; FR-CONV.3 layers RELIANCE-permission on top of it (for structural items only, via the inherited verdict) while INV-019's Self-Audit mandate makes the structural-vs-semantic split auditable, with K-003 enforcing audit of the first 5 real runs. Sequencing dependencies hold: FR-CONV.1 must land 1st (TB-Add catalogue feeds INV-010 dynamic enumeration), FR-CONV.2 must land 2nd (TB-Add-7 cross-validation contributes to the verdict table FR-CONV.3 injects), then FR-CONV.3 lands 3rd, consuming both. CASE-B classification (sc:tasklist already has passthrough; task-builder silent) is correct — no conflict-register row.

**Status:** Complete
