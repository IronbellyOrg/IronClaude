<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (Proposal B) -->
<!-- Merge date: 2026-11-14T17:20:12Z -->

# Merged resolution: slot C-11 (rfqa-first-step-and-readonly-scope)

<!-- Source: Base (original, modified) — header lines of variant-2-original.md:3-6; tag legend extended with [RUN-VERIFIED] as used by both Round 2 advocates; citation shorthand from round2-advocate-B.md:7 -->
Slot: C-11. Slug: rfqa-first-step-and-readonly-scope. Conflict IDs: CO-30, CO-31 (first change), FX-8, FX-20. Base: Variant B (Proposal B, `adversarial/variant-2-original.md`); merged with Variant A (Proposal A, `adversarial/variant-1-original.md`) per `adversarial/refactor-plan.md` (11 changes). Code state of the variants: HEAD 50d4d2b9d, worktree `brainstorm-reflect-panel`.
Tags: [CODE-VERIFIED] read at the cited path:line in the session that made the claim; [RUN-VERIFIED] observed by a read-only script over local Claude Code transcripts in the session that made the claim; [CODE-CONTRADICTED]; [UNVERIFIED]. Tags are kept as the variants and the advocates used them; the merge re-ran nothing.
Citation shorthand: `A:n` = `variant-1-original.md` line n; `B:n` = `variant-2-original.md` line n; `A-R1`, `B-R1`, `A-R2`, `B-R2` = `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`; `FF` = `round2.5-fault-finder-raw.md`; `r13` = `research/13-future-pr-review-and-rfqa.md`, `GQ-n` = `gaps-and-questions.md`. Paths are relative to the repo root unless they start with `.dev/tasks/` or `/home/`.
Label rules of this merge: where the two advocates' final texts differ, both are shown, labelled `Variant A text` and `Variant B text`; where Advocate B's Round 2 amends an item that Advocate A never answered (no Round 3 at depth standard), the text is labelled `B amendment, not answered by A`. A `Correction note` marks every place where a base statement was changed, naming the diff point and who conceded.

## Merged outcome

<!-- Source: base-selection.md (Combined Scoring, Selected Base); debate-transcript.md (Convergence Assessment); invariant-probe.md (Invariant Probe Gate) -->
- Base: Variant B. Combined score A 0.8809, B 0.9167; margin 3.58% (below the 5% threshold); tiebreaker level 1 (debate performance): Variant B won 9 diff points outright against 3 for Variant A; base = Variant B.
- Winner shape (C-001 hybrid, 88%, same text in both Round 2 tables): the first rf-qa change is lens-level: one new read-only lens-reviewer agent definition plus a replay oracle; no panel engine (`resolve`/`merge`/`ledger`) is wired into any rf-qa gate.
- Its only gate edit is conditional: the standard lens dimensions at `/task` steps 3-4 switch to the new agent only if arm 1a meets the pre-registered rule before merge AND the owner answers Q3 yes; otherwise `task/SKILL.md` stays byte-identical (section 3.3).
- Convergence: 83.3% (25 of 30 diff points agreed at text level; 30 of 30 on outcome label); threshold 80%.
- Status: BLOCKED_BY_INVARIANTS. Six HIGH invariants stay UNADDRESSED (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017; section 6.3). Five points stay unresolved in wording (C-002, C-006, C-008, A-001, A-004; section 10). No Round 3 exists at depth standard.
- Status of this resolution: partial. It records the agreed shape and both texts where the advocates split; it decides none of the unresolved points and resolves none of the HIGH invariants.

## 1. Consistency with the adjudicated slots C-01, C-02, C-03

<!-- Source: Variant A, Section 0 (table form) merged with Base Section 4 (dependency statements) — moved to the front per Change 2 (S-001 hybrid 85%, S-003 hybrid 85%); X-006 per debate-transcript.md Scoring Matrix -->
Both variants were written after reading the `ADJUDICATION-RESULT.md` of C-01, C-02 and C-03 and both declare consistency with all three (diff-analysis.md Metadata). The merged first change wires no panel engine into any gate (C-001 hybrid), so most dependencies on the three slots attach to a later engine step (open condition (ii), section 10), not to the first change.

| Slot outcome (as adjudicated) | What this resolution does with it |
|---|---|
| C-01 (`core-shape-and-finding-contract/ADJUDICATION-RESULT.md`): hybrid on Variant B's base: thin shared contract, per-module engines; spec loop on v1 `findings.py`/`ledger.py`/`review-ledger/1`; reflect on the v2 kernel; locator-agnostic `annotate`, citation-keyed ledger rows, the v2 clustering for new ledgers and a typed re-review line withdrawn; convergence to one engine only on triggers T-a (a module needs re-review rounds over citation-located findings from several reviewers), T-b (the pre-registered measurement shows citations resolve at least as often as anchors locate) or T-c, with the `same_defect_v2` anchor-span precondition (B:53) | Consistent. The first change edits nothing under `src/superclaude/cli/review/` and wires no engine, so it fires no trigger. Dependency kept from B: a `/task` gate step over citation-located findings across files with re-review rounds (verification round and fix cycles, `task/SKILL.md:256-258`) is the situation T-a describes; whether T-a fires there depends on whether lens reviewers can return text anchors per file [UNVERIFIED], and the M-B4 anchor probe (section 7, step 6) runs before any later engine step. If it fires, the C-01 debate's recorded path is Variant A's one-engine design after the anchor-span precondition, and that precondition (and C-01's unresolved INV-003, HIGH: repair step versus pinned limit tests at `tests/review/test_review_findings.py:113, 117`) comes before that later step (B:53). X-005 (hybrid 90%): B's statement holds for the whole gate, A's for a Half 2 limited to document outputs; Half 2 is not in the first change. |
| C-01 condition 4 and INV-003 (the repair step and the limits pins) | Not touched: no parser, ledger, clustering or report-render edit (A:16, A:92). |
| C-02 (`ledger-clearing-and-verdict-authority/ADJUDICATION-RESULT.md`): Variant B as base with Variant A's quorum gate: explicit per-row verification, quorum over `block_ok` reviewers typing `prior <lid> resolved` with `need = min(Q, requested)`, silence never clears, typed `blocking` plus a CRITICAL floor, `defer` terminal and counted open, verdict derived on read (B:55) | Consistent; no ledger is used in the first change. Dependencies inherited by any later engine step and not resolved here: the `--resolution`-absent fallback is OPEN; C-02's HIGH items INV-001 (`min(Q, requested)` can be 0), INV-002 and INV-003 (an exit-code-only caller runs an empty reviser when `brief_ids` is empty and `verify_ids` is not; `next` is only in `ledger verdict` JSON). Any later caller of the loop must read `next` and pass `--resolution` (B:55; A:17, A:106). Variant A's note that the `/task` verification round already asks explicit per-finding verification (`task/SKILL.md:256`) from a fixed set of two agents (A:17) stays a fact about the prose gate. C-02 says "no effect on reflect holds for this slot only"; the first change does not make reflect a consumer of the review ledger. |
| C-03 (`merge-verdict-policy-and-quorum/ADJUDICATION-RESULT.md`): Variant A's union default as a pluggable policy, quorum as a merge-time refusal (floor `min(2, requested)`), fail-closed claimed only in profiles that set `degrade`; v1 rows cannot feed an rf-qa confidence gate from support flags until findings-v2 reaches the ledger (condition 7) (B:57; A:18) | Consistent. The `degrade` profile and floor 2 apply to a later engine step only (B used them for its document gate, which left the first change; section 2 correction note). The prose floors 6/8/10/12 of the `/task` gate (`task/SKILL.md:196-201`; "fewer than 6 agents total ... is a violation", `task/SKILL.md:203`) stay as they are (C-011, B 95%), so no `min_complete` or floor-owner decision (C-03 INV-003) is forced. Variant A's honest note, restated: the `/task` floor of 6 is higher than C-03's `min(2, requested)` (A:18); the merged first change does not reconcile them because it adds no panel at any gate. X-006 (Variant A outcome, 95%; B conceded, `round1-advocate-B.md` Concession 3): the confidence of the Confidence Gate is computed per reviewer from its own checklist rows (`rf-qa.md:505`), not from ledger support flags, so C-03 condition 7 does not bind the new agent, which carries that gate in its body (section 3.2); B's conditional dependency on findings-v2 reaching the ledger (B:57) therefore does not apply to this design. |

Disagreement with any of the three outcomes: none. Dependencies on them: C-01 (single-document v1 engine stays; withdrawn items stay withdrawn; T-a probe before any later engine step), C-02 (explicit verification, `next`, `--resolution` for any later caller), C-03 (`degrade` profile and floor 2 for any later engine step; prose floors stay now).

## 2. The position in one paragraph

<!-- Source: Base (original, modified) — Base Section 1 rewritten as the hybrid position per Change 1 (C-001 hybrid 88%; C-006, C-007, C-009 hybrids) and Change 7 (Q3, conditional switch); texts from round2-advocate-A.md and round2-advocate-B.md "Proposed resolution" items 1, 6, 7, 8; Variant A Section 1 and Section 7 part 2 (Half 1 / Half 2) -->
The first rf-qa change is lens-level: it adds one new mechanically read-only lens-reviewer agent definition and a replay oracle, and wires no panel engine (`resolve`/`merge`/`ledger`) into any rf-qa gate; B's single-document panel module and A's `/task` Half 2 (resolve, merge and ledger at the `/task` gate for document outputs) are both later steps (item 1 of both resolutions). Mechanical read-only enforcement applies to every new reviewer from its first line, and the control is the agent's `tools` allowlist, not `permissionMode` or the spawn `mode` (X-004, B 92%). The existing `rf-qa`, `rf-qa-qualitative` and `rf-analyst` agent files, the ten primitives that carry the S1-S3 cap text, `pr_submit` and `cli/reflect` stay byte-identical. Owner question Q3 (whether the lens agents are made read-only in the first change) goes to the owner with the evidence of the transcript audit and the oracle; the recommendation is yes for the standard eight lens dimensions only (item 6 of both resolutions). The only gate edit is conditional: the standard lens dimensions at `/task` steps 3-4 switch to the new agent in the first change only if arm 1a passes the pre-registered rule before merge AND the owner answers Q3 yes; otherwise `task/SKILL.md` stays byte-identical (section 3.3). Hardening the skill-embedded and task-file gate items, where the only observed overwrite (N1) occurred, and any gate engine swap are later, separate changes (section 10).

The position keeps three separable clauses (S-002, B 93%), each with its own deciding measurement (section 7):
- **B-1.** The first step wires no gate engine (no `resolve`/`merge`/`ledger` at any rf-qa gate) and is lens-level: not a document-gate module and not the `/task` engine.
- **B-2.** The document-type input survives only as the replay oracle's seeded single-document input (seeded single documents with clean twins); the document-gate module leaves the first change (no host skill).
- **B-3.** The standard lens dimensions at `/task` steps 3-4 switch to the new read-only agent in the first change only conditionally (arm 1a passes AND the owner answers Q3 yes); `rf-qa.md` stays unedited; skill-embedded and task-file gate items keep their agent.

What the first change does not change is listed in section 4.

<!-- Source: Base (original), Base Section 1 clauses as first written — kept visible as a correction note per Change 1 and the plan's "Changes in the opposite direction" -->
Correction note (C-001, C-002; conceded by Advocate B). Variant B as first written said: "B-1 the first step is not the `/task` gate; B-2 it is a document type (or, as the weaker alternative inside the same position, a skill's spawn sites); B-3 the `/task` lens agents' tools and mode are not changed in the first change", with "one single-document gate (a document type that rf-qa-qualitative already reviews, for example PRD, TDD, technical reference or README)" as the first step (B:10). Changes: (1) the document-gate module as the first step with no host skill was conceded in Round 1 (`round1-advocate-B.md` Concession 6) and again in Round 2 ("The document-gate module leaves the first change", B-R2 response 3); (2) B-3 as stated is refuted by N1 under B's own class-(b) rule ("B-3 as stated is refuted", B-R2 "Verification of N1-N3"), and B's pre-commitment (B:84, B:105) moves "an agent-definition split only, without the panel" into the first change; (3) Variant A's first text ("The first rf-qa replacement change starts at the `/task` phase-gate QA", with Q3 "answered yes", A:22) is also not carried: Advocate A moved C-001 off A (A-R2 response 1) and conceded that A:22 "answered yes" oversteps the owner boundary (A-R2 response 7).

## 3. Design consequence for the shared core and the named modules

### 3.1 Shared core (`src/superclaude/cli/review/`)

<!-- Source: Base (original, modified) — Base Section 2 "Shared core", opening replaced per Change 3 (a); C-003, C-004, C-011 B 95% -->
- No edit: the first change edits nothing under `src/superclaude/cli/review/` (kept from B). The core stays the thin shared contract of the C-01 hybrid (ids, limits constants, one repair step, `refs_norm`, hashing) with the v1 engine serving single-document review. The first change does not need: a per-slot `lens` key (the lens travels as free text in the brief, which is the `persona_lens` pattern, `src/superclaude/agents/reflect-reviewer.md:56`, and is M5 of r13 section 8; C-003, Advocate A withdrew the key, A-R2 response 9), a checklist and confidence output mode with a completion predicate (M9; C-004, withdrawn by Advocate A), a partitioning or agent-count-floor rule (R3; C-011), or a multi-file ledger.
- Panel templates keep the closed slot key set `{"slot_id","tier","count","strategy","seed"}` (`src/superclaude/cli/review/panel.py:46`; unknown keys are errors at `panel.py:215-216` [CODE-VERIFIED]). There are 8 packaged templates (`src/superclaude/cli/review/data/review-panel.*.json`: default, live7 and six reflect files [CODE-VERIFIED by `ls`]; X-007). Adding `lens` would edit no template and change no `template_sha256` (`panel.py:46, 214-216, 692`); it is deferred because no first-change consumer needs the core, not the brief, to know the lens.

<!-- Source: Base (original), variant-2-original.md:16 — kept visible as a correction note per Change 4 -->
Correction note (X-002, Variant A outcome 95%; conceded by Advocate B, `round1-advocate-B.md` Concession 1). Variant B as first written said: "Adding `lens` is a schema change over all 8 packaged templates ... and their `validate` tests" (B:16). Code: `template_sha256 = sha256_json(panel)` (`panel.py:692`) hashes the template object and `_SLOT_KEYS` is an accept-list, so widening it edits no template file and changes no hash; B's count of 8 templates stands (X-007).

### 3.2 New deliverables of the first change

<!-- Source: round2-advocate-A.md and round2-advocate-B.md "Proposed resolution" items 2-4; Variant A Section 2 items 1-4; merged per Change 3 (b)-(e); A-002 hybrid 82%, A-004 hybrid 70%, X-004 B 92% -->
(a) One new read-only lens-reviewer agent definition (agreed text, item 2 of both resolutions): its `tools` list is Read, Grep, Glob and the read-only search tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections; it names other primitives by installed path (`~/.claude/agents/<name>.md`, with the project `.claude/agents/<name>.md` as the dual surface); `make sync-dev` and `make verify-sync` run. Standard lenses get pre-computed counts in the brief where they used Bash (agreed text of A-004).
- B amendment, not answered by A: the `tools` list is exactly Read, Grep, Glob and the read-only search and codegraph tools of `reflect-reviewer.md:5`.
- B amendment, not answered by A: any S1-S3 severity or cap text the agent restates is copied verbatim (`test_c_s1_s3_copied_verbatim`). The fault-finder notes that `test_c_s1_s3_copied_verbatim` is parametrized over a fixed 10-file tuple (`tests/skills/test_review_severity_rule.py:181-197`) and does not reach a new file (INV-013, MEDIUM, UNADDRESSED).
- B amendment, not answered by A: the report's first line states the dispatched lens and slot (read by the lens-identity check of section 3.3).
- Recorded next to this item, not resolved: INV-016 (HIGH, UNADDRESSED): arm 0 and arm 1a differ in more than the tool list; content lenses run `rf-qa-qualitative` in arm 0, a different body, and "zero-trust section" does not exist as a section in `rf-qa.md` (the only body occurrence is `rf-qa.md:418`, inside "QA Phase: Fix Cycle"), so the body is not pinned. INV-017 (HIGH, UNADDRESSED): pre-computed counts exist in the oracle, authored by the oracle builder, not at a production gate; no changed gate step adds a pre-computation step. INV-014 (MEDIUM, UNADDRESSED): `rf-qa.md:540` and the installed SubagentStart hook tell agents to write their output file, which pushes a read-only agent to write or to return only a pointer.

(b) A guard test that the agent's allowlist is a subset of a named read-only set (A-002 hybrid), plus a negative fixture. The mutators named:
- Variant A text: Agent, Task, SendMessage, Bash, Write, Edit, NotebookEdit.
- Variant B text: Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit, NotebookEdit (B adds TaskOutput, TaskStop and MultiEdit; `rf-qa.md:22-23` lists TaskOutput and TaskStop).
- Shared ground: `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` at `tests/cli/reflect/test_reviewer_readonly_tools.py:30` omits `Agent` and `SendMessage`, which `rf-qa.md:20-24` grants (N4, [CODE-VERIFIED] by both advocates). The fault-finder rates the mutator-set item ADDRESSED (INV-005, LOW): a subset test rejects any unlisted name, including `Skill`, `TeamCreate` and `AskUserQuestion`. INV-004 (MEDIUM, UNADDRESSED): the guard reads the source file, while at runtime agents resolve from the project `.claude/agents/` first, then `~/.claude/agents/`; and the reflect guard parses only the inline `tools: a, b` form, while `rf-qa.md:6-34` uses the YAML-list form.
- The runtime write-probe that goes with the guard is split in form (A-001); both texts are in section 7, step 4.

(c) The replay oracle, built before any gate text changes (section 7, step 3).

<!-- Source: Base (original), variant-2-original.md:17 and :20-22 — kept visible as correction notes per Change 3 (d) and Change 1 -->
Correction note (A-R1 weakness 2; conceded by Advocate B, B-R2 response 2). Variant B as first written described the new reviewer as "a plan-mode agent without Write, Edit or Bash, of the `reflect-reviewer` kind" (B:17). Replaced by "an agent whose `tools` list is a subset of a named read-only set": the spawn `mode` is ignored and the tools allowlist is the control (X-004, B 92%; N5 shows allowlist refusals in practice). `reflect-reviewer.md:5-8` (tools Read/Grep/Glob plus search, `permissionMode: plan`; "the orchestrator persists them") [CODE-VERIFIED] stays the pattern.

Correction note (C-001; conceded by Advocate B, `round1-advocate-B.md` Concession 6 and B-R2 response 3). Variant B's named modules "New: one thin document-gate module profile, per rf-qa-qualitative document type, on the existing loop (reviewers return text, the orchestrator persists it, `review merge --doc <one file>`, `--cap 3`)" (B:20) and its "Additive by construction" reading of a panel run beside the existing gate (B:22) are not in the first change. The shadow reading survives as an open condition for any later engine swap: it "runs in shadow with rf-qa as authority until a replay says otherwise" (item 11 of both resolutions; section 10). B's "Untouched in the first change" list (B:21) moves to section 4.

### 3.3 The conditional switch at `/task` steps 3-4

<!-- Source: round2-advocate-A.md Proposed resolution items 6-7 and Final position table (C-002, C-006, C-008, A-003, A-004); round2-advocate-B.md Response items 6-7 and Proposed resolution items 6-7 — merged per Change 7 (C-002, C-006, C-008 hybrid 70%; A-003 hybrid 78%; A-004 hybrid 70%) -->
Owner question Q3 (agreed text, item 6 of both resolutions): Q3 goes to the owner with the evidence of the transcript audit and the oracle (section 7, steps 2-3); the recommendation is yes for the standard eight lens dimensions only.
- B amendment, not answered by A: the owner is also told that the only class-(b) event occurred at a task-file gate item of a non-standard lens that the switch does not reach, and that no standard-lens spawn through `/task` steps 3-4 was observed (N2, NB2; section 5.5).

Agreed core (item 7 of both resolutions, common part): IF arm 1a meets the registered rule for a standard lens dimension before merge AND the owner answers Q3 yes, `/task` steps 3-4 switch that dimension to the new agent; the executor persists each returned report unedited to the dispatched slot's path and records its sha256; step 10 is rewritten to check executor-persisted files; otherwise `task/SKILL.md` stays byte-identical.

Splits, side by side (none is decided here):
- (i) Step-8 verification pair. Variant A text: switches together with the standard lenses on the strength of arm 1a ("at `/task` steps 3-4 (and the step-8 verification pair)", A-R2 item 7). Variant B text: switches only if a verification-pair arm passes (B-R2 item 7); B's NB6: 24 of 169 non-fix verifier transcripts ran pytest or `sed -i` on scratch copies.
- (ii) Edited steps of `task/SKILL.md` if the switch lands. Variant A text: steps 3, 4, 8 and 10. Variant B text: steps 3, 4 and 10, with step 8 only after its own arm passes; NB8: no cap row (C-105..C-113, `tests/skills/fixtures/review_severity_cap_edits.yaml:871-943`) sits in steps 3, 4, 8 or 10, so the pins that matter are "no minimum count" (`task/SKILL.md:233`) and the worker-contract paragraph.
- (iii) Lens-identity blocker. B amendment, not answered by A: a report whose first line names a lens other than the dispatched one is a blocker, and step 10 checks files, hashes and lens lines (B-R2 item 7; reason NB3: executor persistence keyed by slot would turn N1 from a detected loss into a silent coverage gap).
- (iv) Exclusion scope. Variant A text: domain and skill-embedded lens spawn sites are excluded; "domain lenses that run mutation tests are excluded from the switch" (A-R2 item 8, A-004). Variant B text: "every lens or verifier that runs tests or mutates scratch copies is excluded from the switch", and the exclusion is named "skill-embedded and task-file gate items", where N1 occurred (B-R2 items 8 and A-004).
- (v) Pre-computed counts. Agreed text of A-004: standard lenses get pre-computed counts in the brief where they used Bash. The fault-finder rates its transfer to production HIGH UNADDRESSED (INV-017).

The fault-finder rates four parts of this block HIGH and UNADDRESSED; this resolution does not resolve them:
- INV-002: the identity check is undefined for a first line that names no lens; across 517 reflect-reviewer returns only 37 start with the mandated heading; identity is self-declared.
- INV-015: the sha256 is computed over the executor's own write, so it proves later non-clobber, never equality with the returned text.
- INV-009: "the dispatched slot's path" is not unique for partition instances of one lens (`task/SKILL.md:264, 273-275`); no slot id exists in `/task` once the per-slot key was withdrawn.
- INV-012: step 10 runs after consolidation (step 6), fix (step 7), verification (step 8) and the proceed decision (step 9), so its checks come too late.

## 4. Out of the first change

<!-- Source: round2-advocate-A.md and round2-advocate-B.md "Proposed resolution" item 8; Base Section 2 "Untouched in the first change" (B:21); refactor-plan.md "Changes NOT Being Made" — new section per Change 11 (C-003, C-004, C-011 B 95%; C-001 hybrid 88%) -->
Out of the first change (agreed text, item 8 of both resolutions): per-slot `lens` key; checklist completion predicate; any `/task` panel template; floor parameter; skill-embedded and task-file gate items; `rf-qa.md`; `rf-qa-qualitative.md`; `rf-analyst.md`; the ten S1-S3 files; `pr_submit`; `cli/reflect`. The two texts differ only in one label: Variant B text "skill-embedded and task-file gate items" (used above, because it names where N1 occurred); Variant A text "domain and skill-embedded lens spawn sites".

Also untouched (B:21): `src/superclaude/skills/task/SKILL.md` (lines 188-286 are the gate) except under the conditional switch of section 3.3; the other six skills that copy the gate; everything under `src/superclaude/cli/reflect/`.

Plugin mirror: rf-* agents are absent from `plugins/superclaude/agents/` (`ls`, first 20 entries show no rf-* name, alphabetical order [CODE-VERIFIED]; Variant B only, `variant-2-original.md:74`), so no plugin parity pin is touched by leaving them alone. Variant A (section 6) reports by Glob that `plugins/superclaude/agents/` holds neither `rf-qa`, `rf-qa-qualitative`, `reflect-reviewer` nor `evidence-validator`, and lists whether the plugin ships the `task` skill as not verified. If the first change adds an agent that is also meant for the plugin, the plugin decision (M14) comes with it (B:74).

Variant A items not carried (refactor-plan.md "Changes NOT Being Made"):

| Diff point | Variant A approach | Why it is not in the first change |
|---|---|---|
| C-003 | Optional `lens` key in `_SLOT_KEYS` (`panel.py:46`) | Withdrawn by Advocate A in Round 2 (no first-change consumer; the lens travels as free text, `reflect-reviewer.md:56`); B 95% |
| C-004 | New `checklist.py` and a completion predicate (UNCHECKED > 0 is not complete for the quorum) | Withdrawn by Advocate A (C-03 did not conclude that state; the formula stays in the agent body, `rf-qa.md:484-534`); B 95% |
| C-011 | Floor as a module-supplied parameter; one panel template for the 6 and 8 tiers | No panel at any gate in the first change; prose floors stay (`task/SKILL.md:196-201`); B 95% |
| C-001, C-007, C-009 | Half 2 (resolve, merge, ledger at the `/task` gate for document outputs) in the first change; the "selectable branch" of steps 6-9 | Moved out of the first change by both advocates (one-candidate merge `ledger.py:107`; blast radius `task/SKILL.md:192, 286`); hybrid 88-92% |
| X-001 | "The one place" and "every lens reviewer of every phase gate" | Code check: 93 markers in 8 skill files; `task/SKILL.md:250` spawns embedded lenses as written; conceded by Advocate A; B 95% |
| X-004 | A static check that the gate text no longer says `mode: "bypassPermissions"` | Guards text, not behaviour (spawn `mode` ignored); conceded by Advocate A; B 92% |
| X-007 | A's M2 golden listing "the seven reflect files" (9 templates) | 8 packaged templates; M2 is dropped with the `lens` key; B 95% |

Variant B items not carried: the document-gate module as the first step with no host skill (`round1-advocate-B.md` Concession 6); B-3 as first stated (refuted by N1); the "plan-mode agent" wording (conceded); the "two implementations" argument (withdrawn, B-R2 response 4); M-B2 as written, which changed engine, prompt and permissions together (conceded, B-R2 response 8). Each has a correction note where the base text stood.

## 5. Evidence

Evidence is keyed by clause (Variant B) with Variant A's claim/evidence/tag rows inside each clause (S-003 hybrid 85%). Subsections 5.1-5.4 are code evidence; 5.5 is run evidence from the transcript audit.

### 5.1 B-3: making the `/task` lens agents read-only is an agent-protocol change, not a flag

<!-- Source: Base (original, modified) — Base Section 3.1, corrected in place per Change 4 (A-006 A 95%; X-003 B 95%) -->
1. The lens agent and the fix agent are the same agent type. Lens agents are spawned as `subagent_type: "rf-qa"` / `"rf-qa-qualitative"`, `mode: "bypassPermissions"`, `fix_authorization: false` (`src/superclaude/skills/task/SKILL.md:225, 241`); the single fix agent is `subagent_type "rf-qa"` with `fix_authorization: true` (`task/SKILL.md:254`) [CODE-VERIFIED]. "Report-only" is a prompt parameter on a write-capable agent. Both agent files declare `permissionMode: bypassPermissions` and the tools Read, Write, Edit, Bash, Glob, Grep (`src/superclaude/agents/rf-qa.md:5-10`, `rf-qa-qualitative.md:4-10`) [CODE-VERIFIED]. Making the lens role mechanically read-only therefore cannot be done by editing `rf-qa.md` (the fix role would lose Write/Edit) and needs a second agent definition per agent type (or the panel's reviewers). Install cost: `_assert_present` (`tests/unit/test_cli_install.py:502-506`) fails only on a missing listed name; the real cost is `make sync-dev` / `verify-sync` (INV-K); A-006.
2. The lens agents write their own report files, and the gate checks that those files exist. Step 3/4 give each agent a report path `${TASK_DIR}qa/qa-structural-[lens-name]-report.md` or `qa-content-[lens-name]-report.md` (`task/SKILL.md:238`), and step 10 reads: "Check that each lens agent wrote its report to the expected path. If any reports are missing, the agent may have failed silently" (`task/SKILL.md:260`) [CODE-VERIFIED]. An agent without Write cannot do that; the `reflect-reviewer` model returns text and "the orchestrator persists" it (`reflect-reviewer.md:3`). So making the lens agents read-only changes the persistence step and the missing-report check of the gate, in the same change as the agent switch (X-003, B 95%: Half 1 rewrites persistence and step 10, with no panel code).
3. rf-qa uses Bash and web lookup as verification surface. "Local Read/Grep/Glob/Bash remain the primary verification surface" (`rf-qa.md:133`); the mandatory report line is "Read: [N] | Grep: [N] | Glob: [N] | Bash: [N]" (`rf-qa.md:518`) [CODE-VERIFIED]. A read-only reviewer of the `reflect-reviewer` kind has no Bash and no Tavily tool (r10 Q5 asks the same for the E2 recipes: "reflect-reviewer has no Bash"). The "Numbers and metrics" lens (`task/SKILL.md:243`, counts match between sections) and the callee-truth / caller-liveness rule (`task/SKILL.md:277-282`, `rf-qa.md:102`) are written for agents that can run commands; whether Grep/Read alone reach the same recall is not measured anywhere [UNVERIFIED]. Run evidence on how lenses used Bash is in section 5.5 (N3, NB5-NB7).
4. The gate is mandatory for every phase of every MDTM task ("No exceptions", `task/SKILL.md:286`; Phase 2 and later, `:192`) [CODE-VERIFIED]. (Variant B's next sentence, "It is the highest-traffic QA path in the repository" (B:31), is qualified by N2: no observed standard-lens spawn used the steps 3-4 path pattern; Advocate A drew the same conclusion for its own "most-run gate" premise, A-R2 response 1.) Its halt behaviour is a pinned worker contract: `tests/skills/test_worker_contract.py:1716-1730` asserts the paragraph that names "Phase-Gate QA step that halts after the second fix cycle", "returns the open blocking findings" and "writes its blocked worker contract" [CODE-VERIFIED]. `task/SKILL.md` is also classified a named reflect consumer (`tests/review/test_reflect_consumer_inventory.py:97-100`) [CODE-VERIFIED; the classification is a test fixture, the INV-M consequence is B's inference].
5. Pins exist for part of the gate and not for the rest. Pinned: the independent stance in `rf-qa.md`, `rf-qa-qualitative.md` and `agent_template_qa.md` (`tests/skills/test_review_prompt_overrides.py:256-268`); the words "no minimum count" in `task/SKILL.md` and four other files (`:271-283`); the S1-S3 cap text in ten files including both rf-qa agent files (`tests/skills/test_review_severity_rule.py:181-192`) [CODE-VERIFIED]. Unpinned: the floors 6/8/10/12, the eight lens names, the single fix agent, the verification round (a repository grep of `tests/` for `qa-structural|qa-content|Minimum Agent Counts|1-2 agent QA|consolidated-findings|callee-truth|caller-liveness` finds only `tests/unit/test_cli_install.py` and `tests/skills/fixtures/review_severity_cap_edits.yaml`) [CODE-VERIFIED]; the confidence gate is unpinned (r13 section 5, grep over `tests/` for `UNVERIFIABLE|VERIFIED / \(TOTAL|confidence gate` returned no files [carried]).
6. Whether a `fix_authorization: false` lens agent has ever modified a file: see the correction note below and section 5.5 (N1).

<!-- Source: Base (original), variant-2-original.md:28 and :33 — kept visible as correction notes per Change 4 -->
Correction note (A-006, Variant A outcome 95%; conceded by Advocate B, `round1-advocate-B.md` Concession 2). Variant B as first written said a new agent file "must be installed (`tests/unit/test_cli_install.py:64` lists the rf-* agent files, r13 section 5 [carried, [UNVERIFIED] line re-read])" (B:28). Code: the table is the member list of the 4.3.5 baseline wheel and `_assert_present` (`test_cli_install.py:502-506`) fails only on a missing listed name, so an unlisted new agent passes.

Correction note (C-002, C-010; conceded by Advocate B, B-R2 response 1 and "Verification of N1-N3"). Variant B as first written said: "I found no evidence in the repository that a `fix_authorization: false` lens agent has ever modified a file. I also found no test or run that would show it. [UNVERIFIED]" (B:33). The transcript audit since found one report-only lens that overwrote another lens's report in a real gate run (N1, [RUN-VERIFIED] by both advocates; section 5.5). It falls in B's own class (b), so B-3 as first stated is refuted.

<!-- Source: Variant A, Section 3.1 rows E2, E5, E6, E7 and Section 3.3 — inserted as claim/evidence/tag rows per Change 4 (S-003 hybrid) -->
Claim/evidence/tag rows from Variant A for this clause:

| # | Claim | Evidence | Tag |
|---|---|---|---|
| E2 | The lens reviewers are "report-only" by prompt only: spawned with `mode: "bypassPermissions"` and `fix_authorization: false`; the agents' frontmatter grants Write, Edit and Bash | `task/SKILL.md:225, 241`; `rf-qa.md:4-12` | [CODE-VERIFIED]; matches r13 R1 and GQ-186 |
| E5 | The target reviewer pattern exists, is read-only by allowlist, takes a free-text lens in its brief and has a static guard test | `agents/reflect-reviewer.md:5-8, 38-40, 56-57`; `tests/cli/reflect/test_reviewer_readonly_tools.py:30-66, 78-103` | [CODE-VERIFIED] |
| E6 | `evidence-validator` is a second shipped read-only reviewer (Read, Grep, Glob; `permissionMode: plan`) | `agents/evidence-validator.md:5-8` | [CODE-VERIFIED] |
| E7 | The checklist and confidence gate is already a pure computation from counted items, "never self-assessed" | `rf-qa.md:486, 503-509` | [CODE-VERIFIED] |
| A 3.3 | Only the reflect-side reviewers are mechanically read-only today; `auggie-reviewer` has Bash and no plan mode; rf-qa, rf-qa-qualitative and rf-analyst are `bypassPermissions` with Write and Bash | FX-8; `rf-qa.md:4-12`; `reflect-reviewer.md:5-8` | [CODE-VERIFIED for the two files A read; the rest from r13 section 2.2, [UNVERIFIED] by A] |
| A 3.3 | The E2 harness disallows only Edit, Write and NotebookEdit and leaves Bash open; a reviewer with Bash can write files, so "report-only" by prompt is not a safety property on any path that has Bash | S06 FX-8 row citing S02:581; r04:79 | [UNVERIFIED by A] |
| A 3.3 | Every lens agent writes into the same `qa/` folder, and "No other agent modifies files during this step" is a convention until the lens agents lose Write | `task/SKILL.md:238, 254` | untagged in Variant A; N1 (section 5.5) is the observed case |

A 3.3's statement that "one edit of one section changes the safety property for every lens reviewer of every phase gate" (A:69) is not carried (X-001, B 95%; section 5.2).

### 5.2 B-1: the `/task` gate is a pattern copied into seven skills, not "the one place"

<!-- Source: Base (original, modified) — Base Section 3.2; the "two implementations" consequence kept as a correction note per the plan's "Changes in the opposite direction" -->
- `fix_authorization: false` occurs 93 times in 8 files under `src/superclaude/skills/`: task-builder 20, tech-research 15, readme 14, roadmap 11, tech-reference 11, operational-guide 11, task 10, sc-reflect-protocol 1 (Grep count, sum 93) [CODE-VERIFIED]. `fix_authorization: true` occurs 43 times in 9 files (including `prd` and `tdd` build-request templates) [CODE-VERIFIED]. The report-only lens agents plus one fixer plus a verification round is the common shape of those seven skills' gates, not a property of `/task`. r13 section 8 / Q2 and synth-05 6.11 ("The `/task` gate is the one place that already separates read-only lens agents from one fix agent", `synth-05-options.md:839`) hold only for the prompt-level separation and only if the seven copies are ignored. [CODE-CONTRADICTED in part: the separation is replicated, with different counts per skill; for example `src/superclaude/skills/readme/SKILL.md:459-460` has a 7-agent and an 11-agent final gate, and `:449-464` lite/standard/full variants with "Max 1 fix cycle" at lite].
- `/task` step 5 says domain-specific lens prompts "are embedded in the task file's QA gate items by the skill that created the task file. The executor spawns them exactly as written" (`task/SKILL.md:250`), so an edit of `/task` steps 3-4 does not reach those spawns (X-001, B 95%, conceded by Advocate A). Run evidence: no observed first prompt used the step-3/4 path pattern with a standard lens name (N2, section 5.5).

Correction note (C-007; withdrawn by Advocate B, B-R2 response 4). Variant B as first written drew the consequence: "a first step that replaces the `/task` gate leaves six more copies of the same pattern with the old agents, the old pins and the old permission mode, so the repository then runs two implementations of one gate. A first step at the shape level (a document gate) leaves one pattern to be replaced everywhere later by the same module" (B:38). Advocate B withdrew it as a reason: "Any staged migration runs two implementations for an interval, so this argument decides nothing for either side" (B-R2 response 4). The replication fact above stands.

<!-- Source: Variant A, Section 3.1 rows E1, E8, E9 and Section 3.2; round2-advocate-B.md NB8 — inserted as claim/evidence/tag rows per Change 4 (S-003 hybrid) -->
Claim/evidence/tag rows from Variant A for this clause, plus B's NB8:

| # | Claim | Evidence | Tag |
|---|---|---|---|
| E1 | The gate separates many parallel lens reviewers, one consolidation, ONE fix agent, a verification round and a cap of 2 fix cycles (3 reviews) | `task/SKILL.md:225, 241, 252, 254, 256, 258` (read in full, lines 186-286) | [CODE-VERIFIED] |
| E8 | The first review's merge rule in the gate is a union with "highest severity when duplicates disagree", and a missing lens report is a blocker | `task/SKILL.md:252, 260` | [CODE-VERIFIED] |
| E9 | The gate's agent-count floors, lens names, single-fix-agent rule and verification round are not asserted by any test; only template filenames match | Grep over `tests/`: matches only `tests/unit/test_cli_install.py:353` and `tests/skills/fixtures/review_severity_cap_edits.yaml:203`, both the filename `qa-consolidated-findings_template.md` | [CODE-VERIFIED]; agrees with r13 section 5 |
| A 3.2 | Nine cap rows C-105..C-113 name `task/SKILL.md`; `test_e_every_cap_edits_row_holds` requires each row's `new` text present and `old` text absent; row C-107 requires "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (present at `task/SKILL.md:258`); `test_d_at_cap_clause_present_where_cap_rows_add_it` requires the clause in every file whose cap row adds it | `tests/skills/fixtures/review_severity_cap_edits.yaml:871-943`; `tests/skills/test_review_severity_rule.py:261-265, 233-246` | [CODE-VERIFIED] (A's looser-reading correction of r13: [CODE-CONTRADICTED] that the gate text is wholly pin-free) |
| A 3.2 | `test_review_prompt_overrides.py` requires "no minimum count" in `task/SKILL.md` | `tests/skills/test_review_prompt_overrides.py:271-283` | [CODE-VERIFIED] |
| A 3.2 | The unattended-caller paragraph must contain "Phase-Gate QA step that halts after the second fix cycle" and "returns the open blocking findings" | `tests/skills/test_worker_contract.py:1715-1729` (A's range; B cites `:1716-1730`, item 4 of 5.1; both as written) | [CODE-VERIFIED] |
| A 3.2 | The ten `S1_S3_FILES` are `rf-qa.md`, `rf-qa-qualitative.md`, `agent_template_qa.md`, `skill_template.md`, the two MDTM workflow templates and four `rules/prompts/*_qa_prompt.md` files; `task/SKILL.md` is NOT among them | `test_review_severity_rule.py:181-192` | [CODE-VERIFIED] |
| NB8 | The cap rows for `task/SKILL.md` do not touch steps 3, 4, 8 or 10; a conditional edit of those steps meets only the "no minimum count" pin (`:233`) and the worker-contract paragraph | rows C-105..C-113 (`review_severity_cap_edits.yaml:871-943`); C-107's text now at `task/SKILL.md:258`; spawn text `task/SKILL.md:225, 241`, step 8 `:256`, step 10 `:260` | [CODE-VERIFIED] (B-R2) |

### 5.3 B-2: a document type fits the settled engine; a phase output does not

<!-- Source: Base (original) — Base Section 3.3; role restated per Change 1 (B-2 now names only the oracle input) -->
After Change 1 this evidence supports two parts of the merged position: no engine is wired at any gate in the first change (C-001, C-007), and the oracle's input is seeded single documents (C-005).
- The settled engine takes one candidate. `review merge --doc` is one file (`src/superclaude/cli/review/merge_cmd.py:29-35`: `type=click.Path(exists=True, dir_okay=False)`, "The candidate reviewed in this round"); `ledger.merge_round(ledger, doc_text, n, reviewers)` takes one `doc_text` (`src/superclaude/cli/review/ledger.py:107`); `annotate` locates `finding["anchor"]` in that text (`src/superclaude/cli/review/findings.py:346-349`) [CODE-VERIFIED]. The `/task` gate reviews a phase output of one to many files with partitioning above six files (`task/SKILL.md:264`) and section ranges above 3000 lines (`:266-275`) [CODE-VERIFIED]. A multi-file phase output has no single candidate text.
- rf-qa-qualitative reviews single documents by type: PRD, report, TDD, tech-ref, ops-guide, README, task file, doc (headings at `rf-qa-qualitative.md:144, 244, 295, 366, 433, 504, 571, 754`, r13 section 4.1 [carried]). A single-document final gate already exists in the skills (README: 4 structural + 4 content + 3 domain lenses on one file, `readme/SKILL.md:27, 460`) [CODE-VERIFIED].
- Only two consumers drive the findings, ledger and panel machinery today (spec-panel loop and the reflect shadow path); every other review path, rf-qa and `/task` included, does not touch `cli/review` (r12 line 178 [CODE-VERIFIED for the grep scope, as stated there]). Spec-type documents already fit the loop contract unchanged (r12 line 136, a design inference tagged as such).

<!-- Source: Variant A, Section 3.1 rows E3, E4 and Section 3.5 — inserted as claim/evidence/tag rows per Change 4 (S-003 hybrid) -->
Claim/evidence/tag rows from Variant A for this clause (they bound any later engine step; none applies to the first change):

| # | Claim | Evidence | Tag |
|---|---|---|---|
| E3 | The panel's loop contract has the same shape as the gate: reviewers return reports, one Reviser reads the blocking ids, cap 3 reviews, then escalate | `spec-panel.md:261, 263`; `ledger.py:37-38, 96` (`cap_reviews` default 3; REVISE below the cap, ESCALATE at it) | [CODE-VERIFIED] |
| E4 | The cap text is identical: "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings" | `rf-qa.md:110`; `task/SKILL.md:258`; `spec-panel.md:261`; pinned in `tests/skills/test_review_severity_rule.py:215-219` | [CODE-VERIFIED] |
| A 3.5 | `total reviewers must be 1..8` (`panel.py:247-248`), a slot `count` is 1..4 (`panel.py:229-231`), exactly one slot is `fixed` (`panel.py:245-246`); the gate floors are 6, 8, 10 and 12 agents (`task/SKILL.md:196-201`); one template covers only the two lowest tiers | as cited | as cited in Variant A section 3.5 |
| A 3.5 | `ledger.new_ledger(doc, cap)` and `merge_round(ledger, doc_text, n, reviewers)` take one document; a phase with several output files is several ledgers; a finding that spans two documents cannot be located in one (the T-a case) | `ledger.py:37-38, 107`; `task/SKILL.md:264` | as cited in Variant A section 3.5 |
| A 3.5 | Heterogeneous models per slot come from the tier file; the dispatch for read-only reviewers is the Agent tool by class word, so the first change does not depend on the C-07 outcome about raw-id launchers | `panel.py:615, 665` | as cited in Variant A section 3.5 |

### 5.4 What r13 itself leaves open

<!-- Source: Base (original, modified) — Base Section 3.4, cross-reference renumbered (section 6 -> section 7) per Change 2; Variant A Section 3.4 rows added per Change 4 -->
- r13 R8 and R12: a full replacement needs a document-type lens pack for 8 types and an rf-analyst analogue (intermediate gates use 2 rf-analyst agents, `task/SKILL.md:209-213`), and calls both "not needed for the first step". That sentence says the first step can be small; it does not say the first step must be the `/task` gate. r13 Q2 and Q3 are open owner questions (GQ-181, GQ-186 resolved only as a doc-intent gap) and r13's own recommendation ("replacing rf-qa starts at the `/task` gate", r13 section 4.3 Key Takeaways) is a reading, not a measurement (synth-06 CO-30 row: "no test or run decides").
- r13 R10 says "build a replay oracle before replacing". Both variants agree on the oracle (A-008, STATED); the debate settled where it is built: seeded single documents with clean twins, arm 0 against arm 1a (C-005 hybrid 80%; section 7, step 3).

| # | Claim | Evidence | Tag |
|---|---|---|---|
| A 3.4 | rf-qa has about 23 files of static pins and no behavioural oracle: 449 occurrences of `rf-qa\|rf_qa\|rf-analyst` in 36 test files, 23 files excluding fixtures; the assertions are text pins and test-side re-implementations | `tests/skills/test_review_severity_rule.py:11` "Enforcement type: STATIC"; `tests/audit/test_nfr_conv_9_zero_trust.py:99-100` | [CODE-VERIFIED by r13 section 5 with the Greps stated; the two cited lines not re-opened by A, [UNVERIFIED] by A] |
| A 3.4 | The confidence gate has no test: a Grep over `tests/` for `UNVERIFIABLE\|VERIFIED / \(TOTAL\|confidence gate\|Confidence Gate\|tool.engagement` returns no file | r13 section 5 | [CODE-VERIFIED by r13]; not re-run by A |

### 5.5 Run evidence from the local transcript audit

<!-- Source: round1-advocate-B.md Strengths 3-5 (pilot); round2-advocate-A.md "New evidence" N1-N6 and "Pilot re-check"; round2-advocate-B.md "New evidence" NB1-NB8 and "Verification of N1-N3"; round2.5-fault-finder-raw.md INV-005, INV-006, INV-008, INV-011 — new subsection per Change 4 (X-001, X-003, X-007 B 95%; X-002, A-006 A 95%; C-010 hybrid 80%) -->
Method (as the advocates stated it): read-only `uv run --no-project python` scripts over `/home/coder/.claude/projects/**/subagents/*.meta.json` and the sibling `.jsonl` files, scratch only under `mktemp -d /tmp/...` directories removed by exit traps; tool calls de-duplicated by `tool_use` id and results matched by `tool_use_id` (Round 2 and the fault-finder; Round 1 counts were raw log records). Transcript rule: every transcript whose text contains the run-1 task id or the queued-run file name was skipped before parsing: 117 rf-qa / rf-qa-qualitative transcripts (rf-qa 74, rf-qa-qualitative 43; INV-011), the same number for both advocates and the fault-finder. All transcripts are from one machine; retention is unknown.

What each corpus count counts:
- 366: Advocate B's Round 1 count of report-only transcripts (204 rf-qa + 162 rf-qa-qualitative), selected on the literal `fix_authorization: false` and not `true`, without the skip rule. Not reproduced; B's Round 1 figure is not quoted as a current count.
- 278: the same selection after the 117-transcript skip rule (155 + 123), reproduced by Advocate A and accepted by Advocate B as "the count to quote" (B-R2).
- 571: non-fix rf-qa / rf-qa-qualitative transcripts selected by excluding `fix_authorization: true` and fix-like descriptions (both advocates' Round 2 rule and the fault-finder). Advocate A's note on the literal selection: it misses 155 lens-like rf-qa transcripts that carry neither literal; they show 0 writes outside QA/report/`/tmp` paths [RUN-VERIFIED] (A-R2).
- 517: reflect-reviewer transcripts (N5).

Pilot figures (Advocate B Round 1, raw) against Advocate A's de-duplicated re-check (Round 2), counts within the 278/366 report-only selection:

| Measure | B Round 1 (raw records) | A Round 2 (de-duplicated by `tool_use` id) | Verdict in the re-check |
|---|---|---|---|
| Write/Edit to QA/report paths | 3,146 | 1,306 (1,009 to a path named in the agent's prompt, 297 to QA/report paths not named there) | reproduced in shape; magnitudes about halved |
| Write/Edit to `/tmp` | 147 | 69 | as above |
| Edit on `/dev/null` | 2 (both errors) | 1 (error) | as above |
| Write/Edit to any other path | 0 | 0 | "0 other" holds only because one agent's write into ANOTHER lens's report sits in the QA/report bucket (N1) |
| Bash calls | 5,261 | 3,198 | not reproduced as a count; no repository-mutating Bash found in what was read; full classification [UNVERIFIED] |
| issue-331 lens agents that wrote mutation harnesses under `/tmp` | 4 of 16 | 2 confirmed (security-invariants, Gate D and Final); denominator 16 not reproduced (A counts about 20) | partly reproduced |

N1. A report-only lens overwrote another lens's report in a real gate run [RUN-VERIFIED by both advocates]. Worktree `issue-331-github-issue-watcher`, task `TASK-RF-issue-watcher-20261107-150955`, Gate C (task-file items 7.G2-7.G7).
- `agent-a00026ccf75eb50ac.jsonl` (rf-qa-qualitative, "Gate C lens design-correctness", `fix_authorization: false`) created `qa/gate-c/qa-content-design-correctness-report.md` at 2026-11-08T00:07:51Z (final: "FAIL, 3 blocking findings (C-1 to C-3), 9 minor notes").
- `agent-abed84d24b847251c.jsonl` (rf-qa-qualitative, "Gate C lens security-invariants", prompt "fix_authorization: false (report-only)" and "Modify no file except your report") ran Write on the same path at 00:12:07Z (result "The file ... has been updated") and four successful Edits to 00:12:51Z (00:12:23, 00:12:24, 00:12:26, 00:12:51Z). It never Read the file before the Write.
- Count: the only path written successfully by two distinct non-fix agents in the corpus (571 non-fix transcripts) [RUN-VERIFIED].
- Correction 1 from B's verification (damage): the first report was restored byte for byte from the first agent's transcript by the orchestrator (00:17:41-44Z; "restored 15855", 96 lines, verdict FAIL with C-1..C-3); 3 blocking findings were replaced by 1 for about 5.6 minutes (00:12:07Z to 00:17:44Z); the stray was kept as `-run2.md`; the security-invariants lens was re-run (`agent-ad808ee6d7eb36624.jsonl`, 00:17:48Z, PASS with notes, 0 blocking). The damage count is unsettled: Advocate A says two blocking findings were lost (A-R2), Advocate B says 3 were replaced by 1 and could not confirm whether the stray's single finding duplicates one of the three (2 or 3 blocking findings).
- Correction 2 from B's verification (cause): partly the dispatch, partly the agent. The dispatch named "Step 7.G7 (task file lines 546-547)" (instructions by line reference); the agent printed lines 540-550, which hold items 7.G5, 7.G6 and 7.G7, and took the first paragraph (design-correctness) (NB1). The damage mechanism is Write access plus self-persistence into a shared `qa/gate-c/` folder.
- Spawn site (NB2): task-file gate items written by task-builder ("lens agent 4/5/6 (part of the parallel batch of Step 7.G2)"), spawned by `/task` step 5 "exactly as written" (`task/SKILL.md:250`), not `/task` steps 3-4. The orchestrator's actual cure was at the dispatch prompt: the re-spawn names the lens, says "do NOT rely on line numbers", names "Your ONLY output file" and lists the files it must never write.
- Detection (NB3): the main session waited for the security-invariants report, found 5 files instead of 6, listed `qa/gate-c` with timestamps, then restored the original. Detection relied on the missing file, which executor persistence keyed by slot would not leave missing (the consequence is B's inference).
- Path state (NB4): the overwritten path was in the worktree and untracked at the time (`?? .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-c/` in the agent's own `git status` at 00:12:55Z).
- Step 10 of the gate would not have caught it: it checks that each report exists (`task/SKILL.md:260`) [CODE-VERIFIED]; it would flag the missing security-invariants report but not the lost content of the design-correctness report (A-R2).

N2. `/task` steps 3-4, as written, are not where standard-lens traffic is observed [RUN-VERIFIED, prompt regex]. First prompts that contain `qa-(structural|content)-` followed by a standard lens name: 0. Standard-lens-named transcripts (descriptions such as "Gate 3 template-conformance lens"): 118 by A's regex, 107 by B's regex; they are spawned from skill or task-file items. Attribution by description is heuristic [UNVERIFIED beyond the regex].

N3. Bash use splits by lens kind [RUN-VERIFIED; classifier regexes are coarse, counts are screens]:

| Measure | Advocate A (A-R2) | Advocate B re-check (B-R2) |
|---|---|---|
| Non-fix transcripts | 571 | 571 |
| With any Bash | 437 | 437 |
| Bash limited to simple read commands | 50 | not re-checked |
| pytest | 74 | 77 |
| `sed -i` / `perl -pi` | 28 | 28 |
| Write/Edit under `/tmp` | 15 | 15 |
| Standard-lens-named subset: n / any Bash / simple reads only / pytest / `sed -i` / `/tmp` writes | 118 / 86 / 18 / 1 / 1 / n.a. | 107 / 79 / not re-checked / 2 / 1 / 0 |

A's reading: standard lenses use Bash mainly for computing over files (counts, line lengths, parsing), which pre-computed evidence in the brief or Grep/Read can cover; mutation testing is a domain-lens activity.

NB5. The misdirected lens of N1 is an executing lens [RUN-VERIFIED]: between 00:06:36Z and 00:10:05Z it wrote and ran `/tmp/gatec-probe/probe1.py` .. `probe7.py` against the package code and removed them at 00:12:55Z. A read-only switch at that spawn site would remove the capability the lens used.

NB6. Verifiers execute about as often as non-standard lenses [RUN-VERIFIED, coarse regex]: non-fix transcripts whose description contains "verif": 169, of which 24 ran pytest or `sed -i`/`perl -pi`; all other non-fix: 402, of which 58 did; standard-lens-named subset (B's regex): 107, of which about 3 did.

NB7. Every `sed -i` by a non-fix agent targeted a scratch or variable path [RUN-VERIFIED screen]: 28 agents; targets such as `$W/m/src/...`, `$M/m2/$S`, `$d/tree/tests/...`, `$F`. Executing lenses include non-domain-named skill lenses (sc:sweep QA: command-contract, skill-contract, primitive-path, read-only-claims) and verifiers, not only test-adequacy and security-invariants. Variables were not resolved.

N4 and nested spawns. The current lens agent can spawn and message other agents: `rf-qa.md:5-24` lists `permissionMode: bypassPermissions` and tools including Write, Edit, Bash, NotebookEdit, Agent, Task, TaskOutput, TaskStop, SendMessage [CODE-VERIFIED]. The fault-finder found it used: across rf-qa / rf-qa-qualitative transcripts (fix and non-fix) 15 successful `Agent` calls, 9 `SendMessage`, 4 `Skill`, 18 `TaskStop`; among non-fix lens transcripts 3 spawned children, one of which ("Phase 3.1 gaps QA p2") spawned a write-capable `rf-qa` child [RUN-VERIFIED] (INV-005). Per-transcript classification does not attribute a child's writes to the lens (INV-008).

N5. The runtime refuses tools outside the allowlist [RUN-VERIFIED]. 517 reflect-reviewer transcripts; de-duplicated tool calls Read 7,110, Grep 5,139, Glob 655, codegraph node 53, callers 6, search 6, explore 1 (A-R2; B's Round 1 raw counts were Read 11,512, Grep 9,410, Glob 1,117). Refused calls: Advocate A counts two (`mcp__razor_culture__pool_Write` and a malformed `pool_Read_placeholder`); the fault-finder counts 7, not 2: `pool_Read` x4, `mcp__razor_culture__pool_Write` x1, `pool_Read_placeholder` x1 and `mcp__codegraph__codegraph_explore` x1, the last a read-only tool refused only because it is not on the list (INV-006). The `reflect-reviewer.md:5` allowlist with `permissionMode: plan` (`:8`) is the working pattern [CODE-VERIFIED].

N6. An isolation precedent exists for reviewers that need execution [CODE-VERIFIED by A; not verified by B]: `src/superclaude/cli/reflect/models.py:94-100` defines `isolate_reviewers`, "PINNED OFF by default", which grounds reviewers "in a `git worktree` snapshot" (`runner.py:721-740`). It is a grounding root for the reflect CLI's own review children, not a write barrier for Agent-tool subagents; its suitability for executing lenses is [UNVERIFIED]. Named only as an open path (section 10).

Classifier caveat (INV-008, MEDIUM, UNADDRESSED): write and Bash calls also appear under renamed tool names (`wrestle_Bash` 19, `wrestle_Bash_placeholder` 35, `cook_Write` 2, `fever_Edit` 2, `mcp__razor_culture__bash_placeholder` 2); all 66 were refused or errored, but a classifier keyed on the literal names would miss a successful renamed call; the evidence counts are regex-dependent and already diverge between advocates.

## 6. Invariants

<!-- Source: Base (original) — Base Section 5 opening line (S-004, B 90%: synth-06 ids) -->
Definitions are those of `synthesis/synth-06-conflict-log.md` 6.12.0 (INV-A to INV-N, lines 54-67). The Round 2.5 fault-finder's own ids (INV-001 to INV-018) are a separate series, listed in section 6.3.

### 6.1 Preserved

<!-- Source: Base (original, modified) — Base Section 5 "Preserved"; INV-J and INV-K/INV-N lines updated per Change 5; INV-C/INV-D, INV-I and INV-L lines adjusted to follow Change 1 (no engine, no panel run in the first change) -->
- INV-A (reflect contract 1.8.0, 110 stable and 27 telemetry names, `merge_method` pair) and INV-B (`derive_verdict` map, exit codes 0/10/11/2, the 36-test matrix): the first change edits nothing under `src/superclaude/cli/reflect/` or the contract module; checkable by `git diff --stat` listing no such path.
- INV-C and INV-D: v1 line grammar, `review merge`, `review-ledger/1` and the `ledger` group are not touched; the first change wires none of them into a gate (modified: Variant B used them "as they are" for its document gate, which left the first change).
- INV-E: `pr_submit` is not touched.
- INV-F: a new primitive must name other primitives by installed path (`~/.claude/agents/<name>.md`, `~/.claude/skills/<name>/SKILL.md`), with the dual-surface rule of the repo CLAUDE.md; checkable with `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`.
- INV-I: fail-closed behaviour (merge refuses zero valid blocks) is inherited from the loop by any later engine step; the first change uses no merge (modified per Change 1).
- INV-J: the ten S1-S3 files (`tests/skills/test_review_severity_rule.py:181-192`) are not edited. `task/SKILL.md` stays byte-identical unless the conditional switch of section 3.3 lands; if it lands, the edited steps (Variant A text: 3, 4, 8, 10; Variant B text: 3, 4, 10, step 8 only after its own arm) must keep the pinned strings: the cap rows C-105..C-113, "no minimum count" and the worker-contract paragraph (`test_worker_contract.py:1716-1730`), and the three pinned suites pass with no test edited (C-008, wording split). A new primitive that restates the cap or severity rule must copy it verbatim (`test_c_s1_s3_copied_verbatim`, `:196-203`); the fault-finder notes that this pin does not reach a new file (INV-013, MEDIUM, UNADDRESSED).
- INV-L: shadow mode and legacy authority: rf-qa stays the authority; any later gate engine swap runs in shadow with rf-qa as authority until a replay says otherwise (item 11 of both resolutions; modified: Variant B's "the panel run is additive in the reading of section 2" referred to its document gate, which left the first change).
- INV-M: the `reflect_status` enum and headless output directories are not touched.
- INV-K and INV-N: a new agent file requires `make sync-dev` and `make verify-sync`; no install-table entry is needed (`_assert_present`, `test_cli_install.py:502-506`, fails only on a missing listed name; A-006). Plugin mirror: see section 4 (rf-* agents absent from `plugins/superclaude/agents/`, so no plugin parity pin is touched by leaving them alone; if the new agent is also meant for the plugin, the plugin decision (M14) comes with it).

### 6.2 Endangered or left unmet

<!-- Source: Base (original, modified) — Base Section 5 "Endangered or left unmet"; INV-G line replaced per Change 5 (C-002 hybrid 70%); Variant A Section 4.2 rows added per Change 5 (C-007, C-008); fault-finder residuals INV-018, INV-007 from invariant-probe.md -->
- INV-G (HIGH): "Reviewers are mutually blind and mechanically read-only". Held for every new reviewer from its first line; for the standard-lens spawns at `/task` steps 3-4 held only if arm 1a passes and the owner answers Q3 yes; unmet for skill-embedded and task-file gate items (where N1 occurred) and for executing lenses and verifiers (for the step-8 verification pair this follows Variant B text; under Variant A text the pair switches with the standard lenses, section 3.3 split (i)). That is a known, visible, stated exposure, not a closed one (GQ-181 stays open until the owner answers Q3).
- Residuals named by the fault-finder (MEDIUM, UNADDRESSED), which leave lens spawns on `rf-qa` even if the switch lands: INV-018: the post-completion standard-lens spawns (`task/SKILL.md:307, 320`) and the Serialized Fix Protocol verification (`:365`) are named by neither resolution; INV-007: the extra lenses of the 10 and 12 agent tiers ("Additional structural lenses as needed for the tier", `:230, :246`) are not standard dimensions, have no arm 1a and keep `rf-qa` with self-persistence; at the 6 tier only 6 of the 8 standard dimensions run.
- INV-J (HIGH): endangered only if the first change adds new prose that restates the cap or severity rule without copying it verbatim; the existing pins fail loudly for the ten listed files, but not for a new file (INV-013).
- INV-K (MEDIUM): a new agent definition adds a sync step; a miss is caught by `verify-sync`.
- INV-H (MEDIUM): any later document-gate module must not put document text in telemetry (convention only, r15:48-56 per synth-06) (modified: the module left the first change).

<!-- Source: Variant A, Section 4.2 rows "Availability of every MDTM task run" and "The pinned strings of task/SKILL.md" — added per Change 5, conditioned on the switch (C-007, C-008) -->
Rows from Variant A, applicable only if the conditional switch lands:

| Invariant or property | How it is endangered | Severity (Variant A's own view) |
|---|---|---|
| Availability of every MDTM task run | The gate runs after every phase except Phase 1 (`task/SKILL.md:192`) and a task cannot go past it ("No exceptions", `task/SKILL.md:286`). A defect in the new gate path stops every task, not one skill. Mitigation in the merged design: no engine swap; the switch is guarded by arm 1a and the unedited pinned suites (C-007 hybrid 90%); Variant A's "selectable branch" of steps 6-9 is dropped (section 9) | HIGH |
| The pinned strings of `task/SKILL.md` | An edit of the switched steps that rewrites the cap or halt sentences, or drops "no minimum count", fails `test_e_every_cap_edits_row_holds`, `test_d_at_cap_clause_present_where_cap_rows_add_it`, `test_lens_prompts_state_no_minimum_count` or `test_task_skill_returns_the_qa_halt_to_an_unattended_caller` | MEDIUM (caught by existing tests) |

Variant A's other endangered rows (A:104-107) attach to parts that left the first change or were settled: the panel size cap and C-02 INV-003 (exit-code-only callers) bind a later engine step; the installed-roster pin was settled by A-006; the reviewer-capability risk (Bash items become UNVERIFIABLE and shrink the confidence denominator, `rf-qa.md:505`) is carried by the UNVERIFIABLE-share metric of section 7, step 3, and by INV-010.

### 6.3 Round 2.5 findings

<!-- Source: invariant-probe.md (18 rows and Summary); round2.5-fault-finder-raw.md — new subsection per Change 5. No item is resolved here. -->
Independent fault-finder, probing the emerging consensus of the two Round 2 resolutions. 18 findings: INV-005 and INV-011 ADDRESSED; 16 UNADDRESSED: HIGH 6 (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017), MEDIUM 9 (INV-001, INV-003, INV-004, INV-007, INV-008, INV-010, INV-013, INV-014, INV-018), LOW 1 (INV-006). Convergence is BLOCKED_BY_INVARIANTS; no Round 3 exists at depth standard, so the items are carried as unaddressed. This resolution resolves none of them.

| ID | Severity | Status | One-line description |
|---|---|---|---|
| INV-001 | MEDIUM | UNADDRESSED | Arm 0 in the oracle may not behave like production lens agents: what it may write depends on the permission mode of the session that runs the oracle and on the installed hooks, neither pre-registered. |
| INV-002 | HIGH | UNADDRESSED | The lens-identity check is undefined for a first line that names no lens, model compliance with a first-line rule is unmeasured (37 of 517 reflect-reviewer returns start with the mandated heading), and identity is self-declared. |
| INV-003 | MEDIUM | UNADDRESSED | The tree-hash check's scope is unspecified: arm 0 legitimately writes its own report into `qa/`, excluding `qa/` blinds the check to N1's class, and a working-tree hash misses git-state changes. |
| INV-004 | MEDIUM | UNADDRESSED | The allowlist guard reads the source file, not the agent that runs (project `.claude/agents/` or `~/.claude/agents/`), and the reflect guard parses only the inline `tools:` form. |
| INV-005 | LOW | ADDRESSED | The mutator set must include spawn and message tools; confirmed used (15 `Agent`, 9 `SendMessage`, 4 `Skill`, 18 `TaskStop`); the subset formulation excludes them all. |
| INV-006 | LOW | UNADDRESSED | Over 517 reflect-reviewer transcripts 7 calls were refused, not 2, including the read-only `codegraph_explore`; the read-only set needs a rule for adding read-only tools. |
| INV-007 | MEDIUM | UNADDRESSED | "The standard eight lens dimensions switch" does not map one-to-one onto the tiers (6 of 8 at the 6 tier; extra non-standard lenses at 10 and 12), and eight per-dimension decisions have no multiplicity control. |
| INV-008 | MEDIUM | UNADDRESSED | The per-transcript audit misses writes by nested child agents and successful calls under renamed tool names; the counts are regex-dependent. |
| INV-009 | HIGH | UNADDRESSED | "The dispatched slot's path" is not unique for partition instances of one lens, so a second executor write overwrites the first; a partition index is needed in the path and in step 10's list. |
| INV-010 | MEDIUM | UNADDRESSED | The Confidence Gate formula divides by zero when TOTAL = UNVERIFIABLE and rewards capability loss near the boundary; no production cap on UNVERIFIABLE exists in either resolution. |
| INV-011 | LOW | ADDRESSED | An empty corpus gives no verdict (B-R2 item 5); the 117-transcript skip set reproduces; the audit stays blind to the skipped runs. |
| INV-012 | HIGH | UNADDRESSED | Step 10 runs after consolidation, fix, verification and the proceed decision, so hash and lens-line checks there come too late; step-5 lenses stay write-capable in the same `qa/` folder. |
| INV-013 | MEDIUM | UNADDRESSED | `test_c_s1_s3_copied_verbatim` and other pins iterate fixed file lists and do not reach a new agent file; an `rf-*` name would also trigger the Tavily parity pins. |
| INV-014 | MEDIUM | UNADDRESSED | `rf-qa.md`'s Critical Rule 1, its Completion Protocol and the installed SubagentStart hook push the agent to write a file or return only a pointer, not its full report. |
| INV-015 | HIGH | UNADDRESSED | The sha256 is taken over the executor's own write, so it proves later non-clobber, not fidelity to the returned text; report volume and the return-to-write window add loss risk. |
| INV-016 | HIGH | UNADDRESSED | Arm 0 and arm 1a differ in more than the tool list (content lenses change body; "zero-trust section" is a fix-cycle passage of `rf-qa.md`), so arm 1a measures read-only plus a different prompt. |
| INV-017 | HIGH | UNADDRESSED | Pre-computed counts exist in the oracle but no production gate step computes them, so arm 1a's result may not transfer; single-document seeds cannot exercise multi-file checks. |
| INV-018 | MEDIUM | UNADDRESSED | The switch does not name the post-completion lens spawns (`task/SKILL.md:307, 320`) or `:365`; a step-8 switch without the fix-cycle section drops the verifier's halt guards. |

## 7. Measurements: one ordered pipeline

<!-- Source: Variant A Section 5 (ordered pipeline M1-M5, right/wrong rule) merged with Base Section 6 (M-B1..M-B4, clause labels); round2-advocate-A.md Proposed resolution items 3-5, 9; round2-advocate-B.md Response items 3-5 and Proposed resolution items 3, 4, 5, 9 — replaces Base Section 6 per Change 6 (S-005 hybrid 92%; C-005 hybrid 80%; C-010 hybrid 80%; A-001 hybrid 72%, probe form split; A-005 hybrid 92%) -->
One ordered list (Variant A's order), each step labelled with the clause of section 2 it decides (Variant B's labelling). Steps 1-4 run before any gate text changes ("built first, before any `/task` text changes", A:111).

1. **Static guards (decide whether the B-1 deliverable is mechanically read-only).** The subset guard of section 3.2 (b) with its negative fixture (mutator list: Variant A text and Variant B text as stated there). The unedited pinned suites pass: `tests/skills/test_review_severity_rule.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py`.
2. **Transcript audit, full M-B1 (decides B-3: whether leaving the agents as they are is acceptable; feeds Q3).** Runs before merge. Agreed text (A-R2 item 5): de-duplicated by `tool_use` id; own report or `/tmp` scratch = neutral; another agent's report or any other repository working-tree path = class (b), which refutes leaving the agents as they are; a git state change in the reviewed repository = class (c), which refutes; the issue-331 Gate C overwrite is recorded as the first class-(b) event. B amendments, not answered by A: "a report whose lens differs from its dispatched lens" is also class (b); an empty or unreadable corpus gives no verdict; run-1 transcripts are skipped; counts are kept per spawn source (`/task` steps 3-4, task-file gate items, skill gates); the first event is recorded with its cause (dispatch by line reference into a window holding three lens prompts). Fault-finder notes, UNADDRESSED: nested child spawns and renamed tool names escape per-transcript classification (INV-008, MEDIUM).
3. **Replay oracle (decides the B-3 switch condition, arm 1a; B-2 names its input).** Seeded single documents with clean twins; arm 0 (current `rf-qa` / `rf-qa-qualitative` lens agents) and arm 1a (the new agent, same lens text, prose consolidation) per standard lens dimension; a tree-hash no-mutation check on every replay run; the UNVERIFIABLE share; a pre-registered repeat count, variance bound and decision rule (A-005); metrics: per-lens recall of the seeded defect in a blocking row, wrong blockers on clean twins, tokens and wall-clock. The fault-finder adds INV-003 (MEDIUM, UNADDRESSED: the tree-hash scope and the git-state blind spot), INV-001 (arm 0's oracle conditions not pre-registered), INV-016 and INV-017 (HIGH, UNADDRESSED; section 6.3). The deterministic arm is split:
   - Variant A text: "a deterministic no-model arm" (A-R2 item 4).
   - Variant B text: "a pytest of the oracle's scoring script on frozen reports (a seeded defect matched in a blocking row; no blocker on a clean twin)"; and "a verification-pair arm (fixed document, applied fix, the pair asked to confirm it) runs only if step 8 is to switch" (B-R2 response 4 and item 4; reason: no engine code exists to replay, and verifiers execute, NB6).
4. **Runtime write-probe (decides whether the allowlist holds at runtime for the new agent; A-001).** Agreed part: rely on the `tools` allowlist, not `permissionMode`, and keep the tree-hash check on every replay. The form is split:
   - Variant A text: "one runtime write-probe test for the new lens agent" / "one runtime write-probe in a `tmp_path` repository" (A-R2 A-001 and item 3).
   - Variant B text: "one runtime write-probe run (a Write attempt in a scratch repository) is recorded once with its transcript kept in the task package; it is not part of `uv run pytest`", because a pytest cannot spawn a Claude Code subagent (B-R2 response 3 and A-001).
   - The fault-finder's remark: a single probe, in any form, covers one harness, one permission mode and one installed copy only (INV-001, INV-004).
5. **Mechanical scope check, M-B3 (decides B-1 and the B-3 boundary after the change).** Agreed text (item 9 of both resolutions): `git diff --stat` names only the new agent file, its tests, the oracle script and tests, and (only under the conditional switch) `task/SKILL.md`, the one allowed edited pinned file; it shows no edits to `src/superclaude/agents/rf-qa*.md`, `rf-analyst.md`, the ten `S1_S3_FILES`, `src/superclaude/cli/reflect/`; and `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_worker_contract.py tests/review -q` passes with no test edited. The fault-finder notes that "no test edited" and a new file's verbatim pin conflict (INV-013).
6. **T-a anchor probe, M-B4 (decides nothing in the first change; gates any later engine step).** Before any later engine step: ask one lens reviewer per file of a real phase output to return v1 text anchors, and count anchor-status `found` in the merged report (`annotate`, `findings.py:346-352`). A high rate would weaken the claim in section 1 that a `/task` gate step needs the one-engine path (C-009 hybrid 92%: any later `/task` Half 2 is limited to document outputs, and M-B4 runs before it is widened).

Shown right or wrong, rewritten for the merged first change:
- The switch (B-3) is shown right for a standard lens dimension if, under the registered rule, arm 1a is not worse than arm 0 on recall and wrong blockers, mutates nothing, and keeps the UNVERIFIABLE share within the registered bound. It is shown wrong if the read-only arm loses recall because lens work needs Bash, if the UNVERIFIABLE share exceeds the bound, or if per-gate cost exceeds the bound (A:123, arm 1 read as arm 1a; Variant A's criterion on typed `prior` compliance in the verification pair belongs to Half 2 and leaves with it). Arm 0 is itself the first behavioural oracle rf-qa has ever had (A:123).
- Leaving the agents as they are (B-3 as first written) is refuted by any class-(b) or class-(c) event in the audit; N1 is such an event (section 5.5).

<!-- Source: Base (original), variant-2-original.md:84 and :86 — kept visible as correction notes per Change 6 and the plan's "Changes in the opposite direction" -->
Correction note (C-005, C-010; conceded by Advocate B, B-R2 response 8 and response 1). Variant B's M-B2 as first written ran "the existing lens gate (real agents) and the panel gate on the same set" (B:86), which changed engine, prompt and permissions together; Advocate B adopted Variant A's arm 0 against arm 1a, which isolates read-only (subject to INV-016). Variant B's first M-B1 rule ("zero writes outside the agent's own report path ... supports leaving `bypassPermissions`; one write to a reviewed output file shows B-3 wrong", B:84) is replaced by the three-class rule of step 2 (B's own Round 1 Concession 5 introduced the classes).

## 8. Effect on future PR code review and rf-qa replacement

<!-- Source: Base (original, modified) — Base Section 7 updated per Change 8 (C-012 hybrid 90%, same text in both Round 2 tables); Variant A Section 6 -->
PR code review: the first change gives PR review the read-only reviewer definition and the replay fixture (r13 M5, M13); the per-slot lens and the checklist mode (r13 M4, M9) wait, because they left the first change with C-003 and C-004 (C-012 hybrid). `Finding`, `Severity`, the FSM and the 50 `tests/pr_submit` files are untouched (INV-E); the adapter path of r13 P1/P13 stays open. The first change adds none of the M3 passthrough keys (`in_diff`, `confidence`, `original_line`, `reviewer`) and no per-slot lens, and neither is needed for the adapter. The PR module needs file:line citations, so for PR the C-01 trigger T-a is the gate, not this change (A:127).

<!-- Source: Base (original), variant-2-original.md:94 — kept visible as a correction note per Change 8 -->
Correction note (C-012; both Round 2 tables). Variant B as first written said "PR code review: no effect in the first change" and placed the reviewer pattern on "a document gate" (B:94); Variant A as first written said the first change delivers M4, M5, M9 and M13 (A:127). The hybrid keeps M5 and M13 only.

<!-- Source: Base (original, modified) — Base Section 7 "rf-qa replacement" with prerequisites (a)-(f) adjusted per Change 8; cross-references renumbered per Change 2 -->
rf-qa replacement: the first change closes no route to it, and orders the route. After the first change the `/task` gate remains replaceable, with its prerequisites named and checkable:
- (a) the arm 0 / arm 1a oracle exists (section 7, step 3);
- (b) the owner answers Q2 (the first rf-qa target) and Q3 (GQ-181);
- (c) the read-only reviewer and fixer split with executor persistence and the rewritten step 10 (`task/SKILL.md:260`), subject to INV-009, INV-012 and INV-015 (section 6.3);
- (d) the C-03 floor owner (C-03 INV-003: who owns `min_complete`), because the 6/8/10/12 floors are agent-count rules;
- (e) the C-01 T-a/T-b evaluation, because a multi-file gate is the T-a case (M-B4, section 7, step 6);
- (f) a v2-to-ledger path for a confidence mode (C-03 condition 7), if a later step feeds a confidence gate from ledger rows.

The six other skills that copy the gate (section 5.2) become module consumers one by one afterwards; the 175-line spawn census (`r13` section 4.2, line-level count, pattern given there; the slice figure 185 is [UNVERIFIED]) is the migration inventory (B:96). What the first change leaves open for later steps, none of which it blocks (A:129): the document-type checks of `rf-qa-qualitative` (8 types, r13 R8), `rf-analyst` at the intermediate gates (r13 R12), the one "reviewer failed" finding in five files (r13 R5), the regression and monotonicity halts (r13 R7), and the 44 structured and about 175 prose spawn lines in 7 skills (r13 section 4.2).

What the first change costs (rewritten for the lens-level first change): it wires no engine and, unless the conditional switch lands, replaces nothing that rf-qa does today, so its user-visible value is small (B:98). What it buys: a mechanically read-only lens-reviewer definition with a guard, an oracle whose arm 0 is the first behavioural oracle rf-qa has had (A:123), a measured answer to Q3 and a stable engine boundary before the `/task` gate's engine is touched.

## 9. The strongest objections and the answers

### 9.1 Variant B's objection: INV-G is violated now on the gate that runs after every phase

<!-- Source: Base (original, modified) — Base Section 8 objection kept; answer updated by N1 per Change 9 (C-007 hybrid 90%) -->
Objection (B:102): "The `/task` lens agents are the one known place where the mechanical read-only requirement (INV-G, HIGH; r13 R1 HARD) is violated today, on a gate that runs after every phase. Leaving them on `bypassPermissions` in the first change keeps a known HIGH exposure alive and delays the fix, while the oracle and the panel work could include it. A document-type start also tests little: spec-panel already reviews spec-like documents, so the first step adds nothing the repository lacks."

Answer, as the debate left it:
1. The exposure is no longer unproven. Variant B's first answer ("The exposure is real in design and unproven in practice ... If M-B1 finds a write, B-3 is wrong and I would move the hardening in", B:105) was tested: the audit found N1, a class-(b) event (section 5.5). B-3 as first stated is refuted (B conceded), and the hardening enters the first change as the new read-only lens-reviewer definition plus the conditional switch (sections 3.2-3.3). N1 itself occurred at a task-file gate item of a non-standard, executing lens (NB2, NB5), which the switch does not reach; that site gets, per Variant B text, a no-clobber check and explicit dispatch prompts in a separate change (section 10).
2. The fix is still not small, which is why the switch is conditional. It needs a second agent definition (the fixer shares the file with the lens agents), executor-side report persistence plus a rewritten missing-report check, and loss of Bash and web tools that `rf-qa.md:133` and `:518` name as verification surface (B:106; X-003, B 95%). Done together with an engine-boundary decision (C-01 T-a) and a quorum-owner decision (C-03 INV-003), it would couple open questions in one change to a mandatory gate; the merged first change wires no engine, so those two decisions stay out (C-007 hybrid).
3. The document-type step left the first change (correction note in section 2); its seeded single-document input survives as the oracle input (B-2).

### 9.2 Variant A's objection: largest blast radius and weakest oracle

<!-- Source: Variant A, Section 7 — objection and answer as the debate left them, merged per Change 9 (C-007 hybrid 90%; X-005 hybrid 90%) -->
Objection (A:133): the `/task` gate is the place with the largest blast radius and the weakest oracle. Every MDTM task passes the gate after every phase but the first (`task/SKILL.md:192, 286`), so a fault in the new path stops all task execution; the v1 engine fits worst there (one document per ledger, `ledger.py:37-38, 107`; reachability rules need file:line, `task/SKILL.md:277-284`; panel max 8 against floors of 10 and 12, `panel.py:247-248`, `task/SKILL.md:196-201`); and nothing measured says a panel gate finds more than the lens agents do.

Answer, as the debate left it:
1. No engine swap at any gate in the first change; the only gate edit is the conditional standard-lens switch, guarded by arm 1a and the unedited pinned suites (C-007 hybrid, same text in both Round 2 tables). The engine-fit part of the objection is accepted as a boundary of Half 2, which is not in the first change.
2. Variant A's mitigation "the current prose consolidation, fix and verification text (steps 6-9, run by the executor) must remain as a selectable branch until the oracle result is in" (A:102) is dropped: Advocate B showed it is a second gate path to keep in sync, and Advocate A conceded (A-R2 response 4; C-007).
3. X-005 (hybrid 90%): B's T-a statement holds for the whole gate, A's for Half 2 limited to document outputs; Half 2 is not in the first change.
4. Residual that neither answer removes (A:145): whether lens items that need Bash are many enough that read-only reviewers lose recall. Only the oracle (section 7, step 3) can show it, subject to INV-016 and INV-017.

<!-- Source: Base (original), variant-2-original.md:109 — kept visible as a correction note per Change 1 -->
Correction note (C-001; conceded by Advocate B). Variant B's closing paragraph accepted that B-2 had two variants (document type, skill spawn sites) and kept "the spawn-site variant only as a fallback if no document type has a usable seeded-defect set" (B:109). With the document-gate module out of the first change, B-2 now names only the oracle's seeded single-document input; the fallback has no role in the first change.

## 10. Unresolved points and open conditions

<!-- Source: debate-transcript.md Convergence Assessment and Scoring Matrix; round2-advocate-A.md and round2-advocate-B.md Final position tables and Proposed resolution items 10-12; invariant-probe.md / round2.5-fault-finder-raw.md Summary — new section per Change 10 -->
### 10.1 Unresolved points

Convergence 83.3% (25 of 30 diff points agreed at text level); status BLOCKED_BY_INVARIANTS. The five points below carry the same outcome label (hybrid) in both Round 2 tables but contradicting texts. Advocate B spoke last and Round 3 does not exist at depth standard, so Advocate A never answered B's amendments. None is decided here.

| Point | Variant A text | Variant B text |
|---|---|---|
| C-002 (read-only scope of the existing lens agents; 70%) | "domain and skill-embedded lens agents keep their agent files in the first change; the standard eight lens dimensions at `/task` steps 3-4 switch to the read-only agent with executor persistence in the first change only if arm 1a passes the pre-registered rule before merge and the owner answers Q3 yes" | "the standard eight lens dimensions at `/task` steps 3-4 switch to the read-only agent only if arm 1a passes and the owner answers Q3 yes, with executor persistence that checks the report's lens line against the dispatched lens; the step-8 verification pair, non-standard lenses and skill or task-file gate items keep their agent" |
| C-006 (separability; 70%) | "Half 1 (agent swap, executor persistence, step 10 rewrite) is separable from Half 2 (engine), is limited to the standard eight lenses, and lands only after arm 1a; Half 2 is not in the first change" | "Half 1 is separable from Half 2 and limited to the standard eight lenses at steps 3-4; the step-8 pair is excluded unless its own arm passes; Half 2 is not in the first change" |
| C-008 (pinned strings of `task/SKILL.md`; 70%) | "`task/SKILL.md` stays byte-identical unless the standard-lens switch lands; then only steps 3, 4, 8 and 10 change and `test_review_severity_rule.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py` pass with no test edited" | "`task/SKILL.md` stays byte-identical unless the standard-lens switch lands; then only steps 3, 4 and 10 change (step 8 only with a passed verification arm) and the three pinned suites pass with no test edited" |
| A-001 (runtime enforcement of the allowlist; 72%) | "rely on the tools allowlist, not `permissionMode`, add one runtime write-probe test for the new lens agent, and keep the tree-hash check on every replay" | "rely on the `tools` allowlist, not `permissionMode`; record one runtime write-probe run (transcript kept in the task package, not a pytest) and keep the tree-hash check on every replay" |
| A-004 (instruction body of the new agent; 70%) | "the new lens agent's body is rf-qa's verification, zero-trust and Confidence Gate sections without the fix sections, standard lenses get pre-computed counts in the brief where they used Bash, and domain lenses that run mutation tests are excluded from the switch" | "the new agent's body is rf-qa's verification, zero-trust and Confidence Gate sections without the fix sections, standard lenses get pre-computed counts where they used Bash, and every lens or verifier that runs tests or mutates scratch copies is excluded from the switch" |

The debate groups them into two clusters (debate-transcript.md Convergence Assessment). Cluster 1 (C-002, C-006, C-008, A-004): does the step-8 verification pair switch together with the standard lenses, and is the exclusion scope "domain lenses" (A) or "every lens or verifier that runs tests or mutates scratch copies" (B). Cluster 2 (A-001): runtime write-probe as a test (A) or a recorded run (B). The fault-finder reads them as three disputes and remarks, without deciding them: INV-018 supports B's "own arm" condition for the step-8 pair and adds a body condition; INV-005 and INV-008 support B's wider exclusion scope; INV-001 and INV-004 show a single runtime probe in any form covers one harness only.

Other items where B's Round 2 amended A's text and A did not answer, but the debate scored the texts as agreed (additive): C-005 (the deterministic arm as a pytest of the scoring script), C-010 (lens-mismatch as class (b), counts per spawn source), A-002 (the longer mutator list), A-003 (the lens-identity blocker). They are shown with their labels in sections 3.2, 3.3 and 7.

### 10.2 Open conditions

(i) Executing reviewers.
- Variant A text (A-R2 item 10): "Open condition, domain lenses: they keep their agent until a read-only path for mutation testing (pre-computed evidence, or an isolated execution such as the reflect `--isolate-reviewers` snapshot pattern, suitability [UNVERIFIED]) is measured against arm 0 on the same oracle."
- Variant B text (B-R2 item 10): "lenses and verifiers that run tests or mutate scratch copies keep their agent until a read-only path is measured against arm 0".
- B amendment, not answered by A: "skill-embedded and task-file gates get, in a separate change, a no-clobber check (each report's sha256 recorded when its owner returns and re-checked at consolidation; a mismatch is a blocker) and dispatch prompts that name lens and report path explicitly, not by line reference." Variant A's item 10 names domain lenses only.

(ii) Engine (agreed text, item 11 of both resolutions): any gate engine swap (B's document gate or A's Half 2) waits for the C-01 T-a probe (M-B4), the C-03 floor-owner answer and C-02's `next`/`--resolution` caller rules, and runs in shadow with rf-qa as authority until a replay says otherwise.

(iii) Evidence quality (item 12 of both resolutions): the transcript audit covers one machine and unknown retention; the "eight lens" set meant by Q5 stays an owner decision. B amendment, not answered by A: the N1 damage count (2 or 3 blocking findings) is unsettled.

(iv) Invariants: the six HIGH UNADDRESSED invariants of section 6.3 (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017) stand; they bear on the executor-persistence and arm-1a parts (base-selection.md, Selection Rationale). The nine MEDIUM and one LOW UNADDRESSED items stand as well.

## 11. What was not verified

<!-- Source: Base (original, modified) — Base Section 9 kept at the end per Change 2; union with Variant A Section 8 last bullet and the fault-finder's "Not verified" line per Change 10; items answered by the debate carry a note -->
From Variant B (section 9):
- Whether any `fix_authorization: false` lens agent ever wrote a file (M-B1). Note: the audit pilot since found one class-(b) event on one machine (N1, section 5.5); the full audit of step 2 of section 7 has not run.
- Whether Read/Grep/Glob alone give lens reviewers the same recall as with Bash and Tavily (no measurement exists).
- Whether the `Agent` tool's `mode: "bypassPermissions"` argument is effective in the harness or the agent frontmatter alone decides; the session's tool schema describes `mode` as ignored, which is a harness fact outside the repository and is [UNVERIFIED] for the target runtime (X-004 records the schema reading).
- Which document type is best for the first gate (now moot for the first change: no document gate is in it).
- `tests/unit/test_cli_install.py:64` and r13's `rf-qa-qualitative.md` heading lines were taken from r13 and not re-read by B (the install question was settled by A-006 from `test_cli_install.py:502-506`).

From Variant A (section 8, last bullet), "Not verified in this session":
- That `tests/review` has no whole-dict equality on a resolved reviewer (moot while no `lens` key is added).
- Whether a new agent file needs entries in `tests/unit/test_cli_install.py:53-67` or `S1_S3_FILES` (the install-table part settled by A-006; the `S1_S3_FILES` part is INV-013).
- The spawn-line census numbers.
- Whether the plugin ships the `task` skill.
- The count 36 of the verdict matrix.

From the Round 2.5 fault-finder ("Not verified"):
- Claude Code's behaviour when a `subagent_type` does not resolve.
- Whether reflect-reviewer briefs overrode the mandated first line (41 of 517 briefs mention a YAML fence or an output format).
- The content of the 3 non-fix nested spawns beyond their descriptions.

This merge re-ran no script and no test; every figure is copied from the variants and the debate artifacts.

Document status: Complete (all eleven sections written). Resolution status: partial (see Merged outcome).
