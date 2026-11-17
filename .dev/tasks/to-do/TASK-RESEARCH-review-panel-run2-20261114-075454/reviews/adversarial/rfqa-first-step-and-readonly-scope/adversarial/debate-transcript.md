# Adversarial Debate Transcript

Slot C-11 (`rfqa-first-step-and-readonly-scope`). Mode A (`--compare`), no `--merge`, no `--interactive`. Variant A = Proposal A (`variant-1-original.md`), Variant B = Proposal B (`variant-2-original.md`). The advocates' own files are included below unabridged (headings demoted two levels); source files: `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, `round2.5-fault-finder-raw.md`.

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel and blind; Round 2 sequential, A then B) plus Round 2.5 (invariant probe). Round 3 does not exist at depth standard.
- Convergence achieved: 83.3% (25 of 30 diff points agreed at text level); outcome-label agreement 100% (30 of 30); Round 1 label agreement 53.3% (16 of 30, upper bound, hybrid wording not compared)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (plus one independent fault-finder at Round 2.5)
- Diff points in the denominator: 30 = S 5 + C 12 + X 7 + A 6 (A-001..A-006; A-007 and A-008 are STATED and not counted)
- Agreement rule used: a point is agreed when both advocates' final positions carry the same outcome label (A / B / HYBRID / NEITHER) AND their final hybrid texts do not contradict each other. Five hybrid points carry a direct contradiction (C-002, C-006, C-008, A-001, A-004; section "Convergence Assessment") and are counted as not agreed. Advocate B spoke last and Round 3 does not exist, so Advocate A never answered B's amendments.
- Taxonomy coverage gate (AD-5): L1 (S-001, S-004, X-007), L2 (14 points) and L3 (13 points) are all addressed in both rounds. No forced round.
- Shared assumptions: both advocates answered A-001..A-008 in both rounds (no omission).
- Debate-level note: Advocate A ran a read-only re-check of Advocate B's transcript pilot in Round 2 and Advocate B verified A's finding N1 and N2/N3 in Round 2; both used local Claude Code transcripts under `/home/coder/.claude/projects/` and skipped 117 transcripts that mention the forbidden run-1 paths.

## Round 1: Advocate Statements

### Variant A Advocate (default model, default persona; Proposal A)
### Round 1: Advocate for Variant A (slot C-11, rfqa-first-step-and-readonly-scope)


Advocate: A (Proposal A, `variant-1-original.md`). Focus: correctness, risk, test-coverage. Round 1 is blind: no `round1-*` file of another advocate was read.
Tags: [CODE-VERIFIED] read at the cited path:line in this session; [CODE-CONTRADICTED]; [UNVERIFIED].

#### Position summary

The first rf-qa change should make the `/task` phase-gate lens reviewers mechanically read-only (a new agent definition whose `tools` allowlist has no Write, Edit, Bash, NotebookEdit or Agent/Task), with the single `rf-qa` fix agent kept as the only writer, because the `tools` allowlist is the only control the runtime honours and the current lens agents run with Write, Edit and Bash on the most-run gate in the repository. Variant A should be narrowed, not abandoned: land the agent swap (Half 1) first and keep the ledger/merge swap (Half 2) for document-output gates behind the oracle, in shadow beside the prose consolidation, with the per-slot `lens` key and the checklist completion predicate moved to Half 2.

#### Steelman of Variant B

The strongest version of Variant B is an argument about ordering under zero outcome evidence:

1. Nothing measured says the panel gate is better than the current lens agents (rf-qa has no behavioural oracle, CO-30, a decided fact), so the first change should be the one whose failure costs least. A single-document gate that runs beside rf-qa (B:22, shadow reading) cannot stop any task; a fault in a new `/task` path stops every MDTM task after Phase 1 ("No exceptions", `task/SKILL.md:286`; Phase 2 and later, `:192`) [CODE-VERIFIED].
2. The settled engine is a one-document engine: `ledger.merge_round(ledger, doc_text, n, reviewers)` (`ledger.py:107`) and `review merge --doc` (one file). A document type fits it without a locator change, so B's first step needs no C-01 trigger and no C-03 floor-owner decision (B:57). That is a genuine decoupling: B's first change opens no open question from the three adjudicated slots.
3. The report-only lens pattern is replicated, not unique to `/task`: `fix_authorization: false` appears 93 times in 8 skill files (diff analysis X-001, code-verified), and `task/SKILL.md:250` says skill-embedded lens prompts are spawned "exactly as written" [CODE-VERIFIED]. A's sentence that one edit "changes the safety property for every lens reviewer of every phase gate" (A:69) is too wide, and B caught it.
4. Hardening the lens role is more than a flag: the lens and fix roles share the `rf-qa` agent file (`rf-qa.md:5-20` grants Write, Edit, Bash, NotebookEdit, Agent) [CODE-VERIFIED], so a second agent definition, orchestrator-side persistence and a rewritten step 10 (`task/SKILL.md:260`, "Check that each lens agent wrote its report") are needed [CODE-VERIFIED]. B also correctly flagged that the spawn-text `mode` argument is not the control (B:115).
5. B's M-B1 is the only measurement in either variant of the CURRENT exposure, and B pre-commits to moving the hardening into the first change if one write is found (B:84). B's three clauses are separable and each has a deciding measurement, which is a cleaner falsification structure than A's single pipeline.

What B gets right, and A should adopt: the shadow reading for any engine swap (rf-qa remains authority until a replay says otherwise), the narrower scope of the "one place" claim, the clause-keyed measurements, and the mechanical scope check M-B3.

#### Strengths claimed (Variant A)

1. **A fixes the exposure where it actually exists, with the control the runtime actually honours.** The Claude Code subagent documentation (fetched this session from `https://code.claude.com/docs/en/sub-agents`) says: "When the main conversation is in `bypassPermissions`, `acceptEdits`, or auto mode, the subagent runs in that same mode and Claude Code ignores the `permissionMode` you set", and that `tools` is the allowlist ("To restrict tools, use the `tools` field as an allowlist"). So neither the spawn argument `mode: "bypassPermissions"` (`task/SKILL.md:225, 241`) nor a frontmatter `permissionMode: plan` is the safety property; only the tools list is. The current lens agents' tools list is `Read, Write, Edit, Bash, Glob, Grep, ... NotebookEdit, Agent` (`rf-qa.md:5-20`) [CODE-VERIFIED]. A's Half 1 changes exactly that control for the standard eight lenses; B leaves it unchanged in the first change (B:10, B-3). [Harness fact from official docs; target-runtime behaviour beyond the docs UNVERIFIED.]
2. **The exposure is concrete in the gate text, not hypothetical.** Every lens agent writes its own report into the same `${TASK_DIR}qa/` folder (`task/SKILL.md:238`) and has Write/Edit on the output files it judges. The gate's own guarantee "No other agent modifies files during this step" (`task/SKILL.md:254`) is prose only. The gate runs after every phase from Phase 2 (`:192`) and is mandatory (`:286`) [CODE-VERIFIED]. It also runs ON TOP of every skill's own gates when a skill hands its task file to `/task`: "/task adds phase-gate QA on top. This results in intentional, acceptable double QA at gate phases" (`tech-research/SKILL.md:616`) [CODE-VERIFIED]. So the `/task` steps 3-4 lens spawns run on every phase of every MDTM task whichever skill built it. This is the narrowed, code-true form of A's "one place" claim.
3. **The agent swap (Half 1) needs no panel code and no open adjudicated question.** Half 1 is a new agent file, three spawn-site edits (steps 3, 4, 8), executor-side persistence and a rewritten step 10 (A:38-39, A:139). It does not touch `cli/review`, does not fire C-01 T-a, does not need C-03's floor owner (the prose floors stay), and does not need C-02's quorum (the prose consolidation and verification stay). The diff analysis agrees "No panel code is needed for Half 1: true in both readings" (X-003). B's coupling argument (B:106, "couples four open questions in one change") applies to Half 2, not Half 1 (U-001, rated High).
4. **A touches the fewest pinned files that still reach the gate.** A edits `task/SKILL.md` but none of the ten `S1_S3_FILES` (`test_review_severity_rule.py:181-192`, per A:64), and keeps the pinned strings: "no minimum count" (`tests/skills/test_review_prompt_overrides.py:283` asserts it) and "Phase-Gate QA step that halts after the second fix cycle" (`tests/skills/test_worker_contract.py:1724`) [CODE-VERIFIED both test lines], and step 9 word for word (`task/SKILL.md:258` contains "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings") [CODE-VERIFIED]. Every one of those pins is an existing test that fails loudly if the edit drifts, so A's edit has a regression net B's untouched file does not need but A's does have.
5. **A's oracle measures the thing in dispute.** The model arm M5 runs arm 0 (current lens agents) and arm 1 (read-only reviewers with the same lens text) on identical seeded documents with clean twins, and includes a tree-hash check that no reviewer changed any file (A:121). That measures both open risks of the read-only swap: lost recall from losing Bash, and mutation. Honest limit: as written, A's arm 1 is "the panel gate with read-only reviewers" (A:121), so it changes engine and permissions together. A's own Half 1 / Half 2 split makes the clean fix available: add arm 1a (Half 1 only: read-only agent, same lens text, prose consolidation unchanged), so arm 0 versus arm 1a isolates read-only and arm 1a versus arm 1 isolates the engine. B's document-level oracle M-B2 has no such decomposition (B:86).
6. **A names the Bash-loss risk and makes it measurable.** Lens items that need Bash become UNVERIFIABLE and shrink the confidence denominator `VERIFIED / (TOTAL - UNVERIFIABLE) * 100` (`rf-qa.md:505`; the formula is at the "Step 3: Compute" line of the Confidence Gate Protocol) [CODE-VERIFIED], so a lost check can hide inside a high percentage (A:105, U-003). A measures the UNVERIFIABLE share arm 1 against arm 0. B names the Bash dependence (B:30) but has no metric for it.
7. **A's per-slot `lens` key is hash-neutral and test-neutral for existing templates.** `_SLOT_KEYS = {"slot_id", "tier", "count", "strategy", "seed"}` (`panel.py:46`) is an accept-list checked per key (`panel.py:214-216`), and `template_sha256` is `sha256_json(panel)` of the template object [CODE-VERIFIED]. Widening the accept-list edits no template file and changes no existing hash (diff analysis X-002 supports A). Golden fixtures already exist to prove it (`tests/review/fixtures/panel-golden-default-live7.json`, `panel-golden-packaged-tiers.json`) [CODE-VERIFIED by Glob].
8. **A's checklist mode is specified to the edge case.** A names the undefined case TOTAL = UNVERIFIABLE (division by zero in `rf-qa.md:505`) and requires the rule to be fixed in a test before the first run (A:117, U-002). The confidence gate has no test today (r13 section 5, carried).

#### Weaknesses identified (Variant B)

1. **B keeps a known, mechanically unenforced write path on the highest-traffic gate for the whole interval, and its decider may be unrunnable.** B states the exposure (B:77, INV-G "left unmet for the existing `/task` lens agents") and relies on M-B1, an audit of session transcripts that are "not in the repository; their location and retention are [UNVERIFIED]" (B:84). If no transcripts survive, M-B1 returns no evidence and B's rule defaults to leaving `bypassPermissions` in place, so absence of logs reads as safety. A past audit also does not bound future behaviour of new model versions. A's tree-hash check runs on every replay going forward.
2. **B's "plan-mode agent" is not the control under a bypass parent.** B describes the new reviewer as "a plan-mode agent without Write, Edit or Bash" (B:17). The official docs say a subagent's `permissionMode` is ignored when the main conversation is in `bypassPermissions`, `acceptEdits` or auto mode. B's design is still safe only because of the tools list, which is the same control A uses; B's wording invites a reviewer definition that relies on `permissionMode: plan` alone. [Docs fact, fetched this session.]
3. **B's first change replaces nothing, so it is not an rf-qa replacement step.** B concedes "the first change replaces nothing that rf-qa does today, and its user-visible value is small" (B:98) and runs the panel "beside the existing gate ... rf-qa remaining the authority" (B:22). It also names no invocation site: the new "document-gate module profile" (B:20) is not wired into any skill, because B keeps every skill and `task/SKILL.md` byte-identical (B:21). Where would it run? The single-document gates B cites (README final gate, `readme/SKILL.md:27, 460`) are skill-embedded items that `/task` spawns "exactly as written" (`task/SKILL.md:250`); reaching them means editing `readme/SKILL.md`, which B keeps untouched.
4. **B's "two implementations" argument applies to B as well.** B argues that replacing the `/task` gate leaves six skill copies on the old agents, "so the repository then runs two implementations of one gate" (B:38). B's own first change adds a document-gate module beside all eight existing gates, which is also a second implementation, and one that runs as a shadow with no authority. A's new read-only agent file is reusable at the skill-embedded spawn sites later by changing one `subagent_type` string per spawn (e.g. `task-builder/SKILL.md` carries 27 `mode: "bypassPermissions"` lines) [CODE-VERIFIED count by grep]; B's doc-gate profile is not.
5. **B's schema-change claim is wrong on the mechanism.** "Adding `lens` is a schema change over all 8 packaged templates ... and their `validate` tests" (B:16). Code: the accept-list widening edits no template, changes no `template_sha256`, and `tests/review/test_review_panel.py` loads only the default template by name (X-002). [CODE-VERIFIED for `panel.py`; the test sweep is the diff analyst's, partial.]
6. **B's reading of C-03 condition 7 does not match A's design.** B says a checklist mode "fed from the ledger depends on" findings-v2 reaching the ledger (B:57). A's confidence is computed per reviewer from its own checklist rows (A:18, A:29; `rf-qa.md:505` is per reviewer), not from ledger support flags (X-006).
7. **B's install cost claim is contradicted by code.** B: a new agent "must be installed (`tests/unit/test_cli_install.py:64` lists the rf-* agent files)" (B:28). The table is the member list of the 4.3.5 baseline wheel (`test_cli_install.py:46-53`) and `_assert_present` fails only on a missing listed name (`test_cli_install.py:502-506`, `missing = [name for name in names if not (root / name).is_file()]`) [CODE-VERIFIED]. An unlisted new agent passes; the real cost is `make sync-dev` / `verify-sync` only.
8. **B's oracle does not test the read-only question at all.** M-B2 compares "the existing lens gate (real agents) and the panel gate" on one document type (B:86). If the panel gate's reviewers are read-only and the existing ones are not, a recall difference cannot be attributed to read-only versus a different engine, prompt or merge rule. B's clause B-3 is decided only by M-B1 (history), never by a controlled arm. (A's arm 1 as written has the same conflation; the difference is that A's split gives it the arm-1a fix, see Strength 5.)

#### Concessions

1. **X-001: "the one place" and "every lens reviewer of every phase gate" are too wide.** Step 5 domain lenses are "embedded in the task file's QA gate items by the skill that created the task file. The executor spawns them exactly as written" (`task/SKILL.md:250`) [CODE-VERIFIED], and the skills' own gates are separate checklist items (`tech-research/SKILL.md:478-566`, all `fix_authorization: false`) [CODE-VERIFIED]. An edit of `/task` steps 3-4 does not reach them. What survives: steps 3-4 govern the standard eight lenses of every `/task` phase gate, which runs on top of every skill's gates (Strength 2). A's text should say that and no more.
2. **X-003: Half 1 is not "only spawn lines".** It also moves report persistence to the executor and rewrites step 10 (`task/SKILL.md:260`). A already says so at A:38, but A:139's "an agent-type change at the spawn sites" understates it. Accepted as B states it, minus the claim that it needs panel code (it does not).
3. **X-004: A's second M1 check guards text, not behaviour.** Removing `mode: "bypassPermissions"` from the spawn text proves nothing; the spawn `mode` is ignored per this session's Agent tool schema, and the docs say a frontmatter `permissionMode` is also ignored under a bypass parent. Only the tools-allowlist guard (A's first M1 check) and a spawn-site check that steps 3, 4 and 8 name the new agent type are meaningful.
4. **The guard A proposes to copy has a hole.** `tests/cli/reflect/test_reviewer_readonly_tools.py:30` defines `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` [CODE-VERIFIED]. It does not contain `Agent`, the current name of the subagent-spawning tool, which `rf-qa.md:20` lists [CODE-VERIFIED]. A reviewer whose allowlist includes `Agent` passes the guard and can spawn a write-capable subagent. A copied guard must add `Agent` (and ideally assert the allowlist is a subset of a named read-only set rather than test a denylist). This is a defect in A's M1 as written, and in B's equivalent if B copies the same guard.
5. **X-007: A's M2 miscounts the templates.** There are 8 packaged templates (default, live7, six reflect files), not "default, live7, the seven reflect files" (A:115).
6. **Blast radius is HIGH and A has no outcome evidence.** A said so (A:102, A:137). The narrowing below (Half 2 in shadow) is a direct concession to B's C-007 argument.
7. **The per-slot `lens` key and the checklist completion predicate are not needed for the first change.** Half 1 carries the lens as free text in the brief (B's `persona_lens` point, `reflect-reviewer.md:56`) [CODE-VERIFIED]. The `lens` slot key and "UNCHECKED > 0 = not complete for the quorum" (A:29, a state C-03 did not conclude) belong to Half 2. B is right that they can wait.
8. **Recall loss from Bash removal is unmeasured.** `rf-qa.md` names "Local Read/Grep/Glob/Bash" as "the primary verification surface" [CODE-VERIFIED]. If arm 1a loses recall on the Numbers or Domain-accuracy lenses, Half 1 is wrong as specified and needs a narrower Bash replacement (pre-computed evidence in the brief, the `reflect-reviewer.md:59` pattern).

#### Shared assumptions

| ID | Response | Reasoning |
|---|---|---|
| A-001 | QUALIFY | Partly settled by the official docs fetched this session: `tools` is documented as the allowlist that restricts a subagent, and `permissionMode` is documented as ignored under a `bypassPermissions` parent. So the tools list is the right control and plan mode is not; the static guard checks only the file text, so a runtime probe (a reviewer asked to write a file in a `tmp_path` repo) is still needed for the target runtime. |
| A-002 | QUALIFY | The remaining tools on `reflect-reviewer.md:5` are search and codegraph reads (the user CLAUDE.md states "codegraph tools are read-only"; Augment search is a query). The real gap is the denylist guard missing `Agent` (Concession 4): the guard should assert a subset of a named read-only allowlist. |
| A-003 | QUALIFY | Absence is checked (a missing return is seen at once); fidelity is not. In Half 2 the merge parser rejects a malformed or truncated findings block, which catches some infidelity; Half 1 should have the executor persist the returned text unedited and record its sha256 next to the file. |
| A-004 | QUALIFY | A names a prompt module (A:37) but not the body. The new lens agent should carry rf-qa's verification sections (zero-trust, Confidence Gate Protocol, the callee-truth/caller-liveness rule at `task/SKILL.md:277-282`) and drop the fix sections; otherwise arm 1a measures "read-only plus a thinner prompt". |
| A-005 | ACCEPT | Neither variant states a repeat count or variance bound. The pre-registration must fix a repeat count per arm and a variance bound before the first run. |
| A-006 | ACCEPT | Code contradicts the assumption: `_assert_present` (`test_cli_install.py:502-506`) fails only on a missing listed name, so a new agent needs no table entry. A's [UNVERIFIED] "may need an entry" should be dropped; INV-K (`sync-dev`/`verify-sync`) is the real cost. |
| A-007 | ACCEPT | Both variants keep `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, `pr_submit` and `cli/reflect` unedited, so the ten S1-S3 files are untouched in either first change. |
| A-008 | ACCEPT | Both require the replay oracle before rf-qa loses authority; under A's narrowing, the arm 0 versus arm 1a comparison runs before Half 1 lands (A's "built first, before any `/task` text changes", A:111), and Half 2 does not take authority until the arm 1 result is in. |

#### Per-point positions

| ID | Preferred | Evidence (one sentence) |
|---|---|---|
| S-001 | NEITHER | Section order (consistency check first or fourth) changes no claim; both cover the same three adjudicated slots. |
| S-002 | B | B's up-front clauses B-1..B-3, each tied to a measurement, make falsification clearer than A's split, which appears only inside the objection answer (A:139). |
| S-003 | NEITHER | Argument-ordered (A) and clause-ordered (B) evidence carry the same tags and citations; neither organisation changes correctness. |
| S-004 | B | B's synth-06 ids INV-A..INV-N are cross-checkable against the conflict log; A's descriptive names are not. |
| S-005 | HYBRID: A's ordered pipeline M1-M5 with B's "this decides clause X" label on each step | A's order (static guards before model runs) is right, B's labelling makes each step's falsifying role explicit (B:84-90). |
| C-001 | A | The `/task` steps 3-4 lens spawns run on every phase of every MDTM task, on top of skill gates (`task/SKILL.md:192, 286`; `tech-research/SKILL.md:616`), so that is where the write exposure is largest. |
| C-002 | A | The runtime ignores the spawn `mode` and, under a bypass parent, the frontmatter `permissionMode` (official sub-agents docs), so only a new tools allowlist removes the Write/Edit/Bash/Agent grant of `rf-qa.md:5-20`; B leaves it in place. |
| C-003 | HYBRID: free-text lens in the brief for Half 1; add the hash-neutral `lens` slot key only when Half 2 lands | `persona_lens` free text already works (`reflect-reviewer.md:56`), and the key is harmless when added (`panel.py:46, 214-216`, X-002) but not needed earlier. |
| C-004 | HYBRID: reviewer emits the checklist block as a recorded line in Half 1; the "UNCHECKED > 0 = not complete" quorum predicate waits for Half 2 and C-03's floor-owner answer | The formula is per-reviewer (`rf-qa.md:505`), but the completion predicate is a state C-03 did not conclude (A:29). |
| C-005 | HYBRID: seeded single-document sets with clean twins (B's cheap input) run through `/task` lens arms 0, 1a and 1 (A's arms) | B is right that one file needs no new locator (`ledger.py:107`); A is right that the arms must be the gate's lens agents to measure the read-only effect. |
| C-006 | A | The diff analysis confirms Half 1 needs no panel code (X-003), so the agent swap is separable from every open engine question (U-001, High). |
| C-007 | HYBRID: Half 1 lands at `/task` after arm 0 versus 1a; Half 2 runs in shadow beside the prose steps 6-9 (B's INV-L reading) until arm 1 is in | Blast radius is HIGH (`task/SKILL.md:286`); shadow removes it for the engine swap, and Half 1's risk is bounded by arm 1a. |
| C-008 | A | A's edit keeps every pinned string, and the pins are live tests (`test_review_prompt_overrides.py:283`, `test_worker_contract.py:1724`, cap rows via `test_review_severity_rule.py`), so drift fails loudly. |
| C-009 | A | Scoping Half 2 to document-output gates keeps it inside the one-document v1 engine (`ledger.py:107`) and leaves code-output gates to C-01 T-a. |
| C-010 | HYBRID: run M-B1 where transcripts exist, and the tree-hash no-mutation check on every replay | M-B1 is the only measure of the current exposure (U-007) but depends on transcripts of UNVERIFIED retention (B:84); the tree hash is mechanical and repeatable. |
| C-011 | HYBRID: prose floors 6/8/10/12 stay in Half 1 (B); the floor becomes a module parameter only with Half 2 | Floors exceed the panel's 1..8 total (`panel.py` "total reviewers must be 1..8" check vs `task/SKILL.md:196-201`), and C-03 INV-003 is open. |
| C-012 | A | A's read-only reviewer is the agent kind a PR panel would dispatch (r13 section 9, carried), and A also produces the per-slot lens and checklist exposures; B gives only the reviewer pattern. |
| X-001 | B | `task/SKILL.md:250` spawns skill-embedded lenses "exactly as written", so A's "every lens reviewer of every phase gate" is too wide; A's narrower steps-3-4 claim survives (Concession 1). |
| X-002 | A | `_SLOT_KEYS` is an accept-list (`panel.py:46, 214-216`) and `template_sha256 = sha256_json(panel)`, so widening it edits no template and changes no hash. |
| X-003 | B | Half 1 also rewrites persistence and step 10 (`task/SKILL.md:238, 260`), though it needs no panel code. |
| X-004 | B | The spawn `mode` is ignored (Agent tool schema) and frontmatter `permissionMode` is ignored under a bypass parent (official docs), so A's text-only check guards nothing. |
| X-005 | HYBRID: B is right for the whole gate, A for Half 2 limited to document outputs; run B's M-B4 anchor probe before widening Half 2 | Both cite the one-candidate merge (`ledger.py:107`); the dispute dissolves once scope is stated per half. |
| X-006 | A | A's confidence is per reviewer from its own rows (`rf-qa.md:505`), not from ledger support flags, so C-03 condition 7 does not bind it. |
| X-007 | B | Glob shows 8 packaged templates (six reflect); A:115's "seven reflect files" is wrong. |
| A-001 | HYBRID: rely on the tools allowlist (documented) not `permissionMode`, plus one runtime write-probe test | Official docs make `tools` the restriction and ignore `permissionMode` under a bypass parent; the static guard cannot prove runtime enforcement. |
| A-002 | HYBRID: guard asserts the allowlist is a subset of a named read-only set, with `Agent` treated as a mutator | `_MUTATORS` at `test_reviewer_readonly_tools.py:30` omits `Agent`, which `rf-qa.md:20` grants. |
| A-003 | HYBRID: executor persists returned text unedited and records its sha256 | Absence is detected in both variants; fidelity is checked only partly, by the merge parser in Half 2. |
| A-004 | HYBRID: new lens agent body = rf-qa's verification and Confidence Gate sections minus the fix sections | Without a stated body, arm 1a would measure a thinner prompt, not read-only. |
| A-005 | NEITHER | Neither variant states a repeat count or variance bound; one must be pre-registered. |
| A-006 | NEITHER | `_assert_present` (`test_cli_install.py:502-506`) fails only on missing listed names, contradicting both A's "may need an entry" and B's "must be installed". |

Tally: A 8 (C-001, C-002, C-006, C-008, C-009, C-012, X-002, X-006); B 6 (S-002, S-004, X-001, X-003, X-004, X-007); HYBRID 12 (S-005, C-003, C-004, C-005, C-007, C-010, C-011, X-005, A-001, A-002, A-003, A-004); NEITHER 4 (S-001, S-003, A-005, A-006). Total 30.


### Variant B Advocate (default model, default persona; Proposal B)
### Round 1: Advocate for Variant B (Proposal B, `variant-2-original.md`), slot C-11


Debate: sc:adversarial, slot C-11 `rfqa-first-step-and-readonly-scope`, Round 1 of 2 (blind). Focus: correctness, risk, test-coverage.
Tags: [CODE-VERIFIED] read in this session at the cited path:line; [RUN-VERIFIED] observed by a read-only script run in this session; [UNVERIFIED] carried or not checked. Paths are relative to the repo root unless absolute.

#### Position summary

The first rf-qa change should be a single-document gate for one rf-qa-qualitative document type, run beside the existing gate, with every new reviewer mechanically read-only; the `/task` lens agents keep their agent files and tools in that change, and hardening them is a separate, smaller item triggered by a measured write, not by assumption. A read-only pilot of the M-B1 transcript audit run for this statement found zero Write/Edit calls to any reviewed output across 366 report-only rf-qa / rf-qa-qualitative transcripts, and found that report-only lens agents use Write and Bash for mutation testing on scratch copies, which a read-only reviewer would lose.

#### Steelman of Variant A

The strongest version of Variant A:

1. **It closes a HIGH invariant now, on the path where it matters most.** INV-G ("reviewers are mutually blind and mechanically read-only") is HIGH in the C-11 row (`phase-outputs/discovery/undecidable-conflicts.md:28`). The `/task` lens agents are report-only by prompt only: `mode: "bypassPermissions"` and `fix_authorization: false` (`src/superclaude/skills/task/SKILL.md:225, 241`) on an agent whose frontmatter grants Write, Edit and Bash with `permissionMode: bypassPermissions` (`src/superclaude/agents/rf-qa.md:5-10`) [CODE-VERIFIED]. The gate runs after every phase of every MDTM task (`task/SKILL.md:192, 286`) [CODE-VERIFIED]. If any surface deserves the mechanical guarantee first, it is the highest-traffic reviewer surface. Variant B leaves that exposure open for an interval and says so.
2. **The target shape is already there.** Many parallel report-only reviewers, one consolidation, ONE fix agent ("No other agent modifies files during this step", `task/SKILL.md:254`), a verification round (`:256`) and the cap "After 2 fix cycles (3 reviews), HALT" (`:258`) [CODE-VERIFIED]. That is the panel loop's shape (reviewers, one Reviser, cap 3). Starting where the shape already exists minimises conceptual translation.
3. **The read-only reviewer pattern exists and is runtime-backed.** `reflect-reviewer.md:5, 8` (tools Read/Grep/Glob plus search, `permissionMode: plan`) [CODE-VERIFIED], with a static guard test (A cites `tests/cli/reflect/test_reviewer_readonly_tools.py:30-66`). My own pilot below even supports A here: the runtime refused a Write attempt by a reflect-reviewer.
4. **The two halves are separable (A section 7 part 2).** Half 1 (agent swap, executor persists, prose consolidation kept) needs no panel code; Half 2 (merge/ledger) is limited to document outputs, which keeps it outside C-01 trigger T-a. That is a genuinely good decomposition (diff U-001, High).
5. **Its oracle is the first behavioural oracle rf-qa has ever had, on the gate that matters.** Arm 0 measures the current lens agents; a deterministic no-model arm and a model arm with a tree-hash mutation check and an UNVERIFIABLE-share metric (A section 5, M4-M5). The UNVERIFIABLE-share metric is exactly the right instrument for the capability-loss risk B raises.
6. **It touches none of the ten S1-S3 files** (A section 3.2) and keeps the pinned step-9 cap sentence, "no minimum count" and the unattended-caller paragraph word for word, so the existing pins guard its edit.
7. **A document-type start tests little that is new**: spec-panel already reviews spec-like single documents (B section 8 records this objection itself).

What A genuinely gets right: the exposure is real by design; Half 1/Half 2 separability; the checklist formula's undefined case TOTAL = UNVERIFIABLE (U-002); the UNVERIFIABLE-denominator risk (U-003); the hash mechanism (X-002); and that a per-slot `lens` key is cheap.

#### Strengths claimed (Variant B)

1. **The "one place" premise of Variant A is contradicted by the code, and B's start does not depend on it.** `fix_authorization: false` occurs 93 times in 8 files under `src/superclaude/skills/` (task-builder 20, tech-research 15, readme 14, roadmap 11, tech-reference 11, operational-guide 11, task 10, sc-reflect-protocol 1) [CODE-VERIFIED, Grep count this session]. `/task` step 5 says domain-specific lens prompts "are embedded in the task file's QA gate items by the skill that created the task file. The executor spawns them exactly as written" (`task/SKILL.md:250`) [CODE-VERIFIED]. The README skill's final gate alone runs 3/7/11 agents by intensity with "Max 1 fix cycle" at lite (`src/superclaude/skills/readme/SKILL.md:458-460`) [CODE-VERIFIED]. The diff analyst's code check on X-001 also "Supports B". A shape-level first step leaves one pattern to replace everywhere later; a `/task`-gate first step leaves two implementations of the same gate.

2. **B's first step fits the settled engine with no new locator.** `review merge --doc` takes one file (`src/superclaude/cli/review/merge_cmd.py:30-33`, `click.Path(exists=True, dir_okay=False)`), `new_ledger(doc, cap=3)` and `merge_round(ledger, doc_text, n, reviewers)` take one document (`ledger.py:37, 107`) [CODE-VERIFIED]. The `/task` gate reviews one-to-many files with partitioning above 6 files (`task/SKILL.md:264`) and section ranges above 3000 lines (`:266-275`) [CODE-VERIFIED]. The panel caps reviewers at 8 (`panel.py:248`, "total reviewers must be 1..8") [CODE-VERIFIED] against `/task` floors of 6/8/10/12 (`task/SKILL.md:196-201`) [CODE-VERIFIED]. A single-document gate meets none of these limits; the `/task` gate meets all three. C-01's adjudicated hybrid keeps the spec loop on v1 one-document machinery; B is a module of exactly that.

3. **The current exposure is now measured, not assumed (M-B1 pilot) [RUN-VERIFIED].** Method: read-only scripts (`uv run --no-project python`, private `/tmp` dir removed on exit) over the local Claude Code transcripts in `/home/coder/.claude/projects/**/subagents/`. Each subagent transcript has a sibling `.meta.json` with `agentType`. Selection: `agentType` in {`rf-qa`, `rf-qa-qualitative`}, first user message contains `fix_authorization: false` and not `fix_authorization: true`. Result: 204 rf-qa + 162 rf-qa-qualitative = **366 report-only transcripts**. Their Write/Edit/MultiEdit/NotebookEdit calls: 3,146 to QA/report paths, 147 to `/tmp`, 2 Edit calls on `/dev/null` (both returned an error), and **0 to any other path**. Counts are of log records and can include duplicated records of one call. Bash: 5,261 calls; a tight screen for `sed -i`, `git stash|checkout|restore|reset|commit|add|apply|clean`, `perl -pi` and `cp ... src|tests|.dev/` outside `/tmp` gave 78 candidates; I read the first 30 and every one either targets a scratch copy (`$M`, `$W`, `$D`, `$T` variables set to `/tmp` dirs) or is `echo`/`grep` text; the one `git checkout -q -b feat/review-panel` ran in a `git init` repo under `mktemp -d /tmp/b2qa-reftest.XXXXXXXX` (transcript `agent-a819ed2a6069ae76e.jsonl`, agentType `rf-qa`). The remaining 48 Bash candidates were not read [UNVERIFIED]. So in every observed run, "report-only by prompt" held for file tools; this is the evidence B-3 asked for before choosing, and it supports keeping the legacy agents unchanged in the first change.

4. **Hardening the lens agents removes a verification capability that lens agents use in practice [RUN-VERIFIED].** In the one task whose lens prompts name `qa-structural-*`/`qa-content-*` report paths (worktree `issue-331-github-issue-watcher`, 16 lens transcripts), 4 of 16 lens agents (`test-adequacy` x2, `security-invariants` x2) wrote mutation-testing harnesses with Write/Edit (`/tmp/secinv-harness/mutate.py`, `/tmp/ironclaude-mut-harness.sh`, `/tmp/mutwork-tadq*/driver*.py`, `/tmp/iw-mut-harness/driver.py`), copied `src/` into `/tmp`, mutated the copies with `sed -i`, ran tests, then removed the copies and checked `git status --short -- tests src`. A Read/Grep/Glob reviewer cannot do any of that. This is the concrete form of B section 3.1 item 3 (`rf-qa.md:133` "Local Read/Grep/Glob/Bash remain the primary verification surface") and of the A-004 assumption; Variant A's Half 1 would remove it from the standard lenses on day one, before its own M5 arm can measure the loss.

5. **The new-reviewer pattern B relies on is enforced by the runtime, not only by a static test [RUN-VERIFIED].** Across 517 `reflect-reviewer` transcripts the tool calls were Read 11,512, Grep 9,410, Glob 1,117 plus codegraph search/node/callers/explore; the only write attempt (`mcp__razor_culture__pool_Write` on a `reviewer-cards/reviewer-1-card.md` path, logged twice) returned `Error: No such tool available`. So "every NEW reviewer is mechanically read-only" (B's INV-G scope) is achievable today by an agent definition; B does not need the legacy agents to prove it.

6. **Zero edits to pinned files, checked mechanically.** B keeps `task/SKILL.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the ten `S1_S3_FILES` byte-identical and checks it with `git diff --stat` plus the named suites run unedited (B M-B3). `task/SKILL.md` holds pinned strings (cap rows C-105..C-113, "no minimum count", the unattended-caller paragraph `tests/skills/test_worker_contract.py:1716-1730`) and is a named reflect consumer (`tests/review/test_reflect_consumer_inventory.py:97-100`) [CODE-VERIFIED by B; diff U-013 verified]. Not editing it is cheaper and safer than editing around its pins.

7. **B respects the owner boundary the C-11 row sets.** The row says "whether the lens agents are made read-only in the first change (Q3) and which 'eight lens' set is meant are owner decisions" (`undecidable-conflicts.md:28`) [CODE-VERIFIED, read this session]. A answers Q3 itself ("answered yes", A line 22). B leaves Q3 to the owner and supplies the measurement (M-B1, now piloted) that informs the answer.

8. **B adds no state the adjudicated slots did not conclude.** No per-slot `lens` key, no checklist completion predicate, no `min_complete` owner decision (C-03 INV-003), no T-a evaluation forced before the first step (C-01). A adds a completion state on top of C-03's "block valid" (A line 29 says so) and makes the floor a module parameter, which C-03 did not conclude.

#### Weaknesses identified (Variant A)

1. **A's safety claim does not reach the agents that actually used write tools.** A says "one edit of one section changes the safety property for every lens reviewer of every phase gate" (A line 69). Step 5 domain lenses are spawned "exactly as written" from the task file (`task/SKILL.md:250`) [CODE-VERIFIED], so an edit of steps 3-4 does not reach them (diff X-001). In the pilot, every lens agent that used Write/Edit outside its report (`test-adequacy`, `security-invariants`) carried a domain lens name, not one of the standard 8 [RUN-VERIFIED]. A's Half 1 therefore hardens the standard lenses, which showed no out-of-report writes, and leaves the domain lenses, which showed the writes, unchanged.

2. **Half 1 is not "an agent-type change at the spawn sites" (A line 139).** The lens agents persist their own reports: 3,146 Write/Edit calls to QA/report paths in 366 report-only transcripts [RUN-VERIFIED]. Moving that to the executor rewrites step 3/4's report-path instruction (`task/SKILL.md:238`) and step 10's "Check that each lens agent wrote its report" (`:260`) [CODE-VERIFIED]. The diff analyst's code check on X-003 "Supports B on scope". A itself concedes the persistence change at A line 38.

3. **Half 1 removes a used capability before A's oracle can measure the loss.** A's M5 arm 1 measures UNVERIFIABLE share against arm 0, but only on seeded documents; real lens agents run mutation tests and scratch-repo experiments with Write and Bash (strength 4) [RUN-VERIFIED]. A read-only `test-adequacy` lens cannot run a mutant. A's own risk table rates "Reviewer capability" MEDIUM (A section 4.2) without evidence of how often lenses need it; the pilot shows 4 of 16 in one task.

4. **Largest blast radius, by A's own rating.** The gate runs after every phase of every MDTM task (`task/SKILL.md:192`) and "No exceptions" (`:286`) [CODE-VERIFIED]; A rates availability HIGH (A section 4.2). A mitigates by keeping steps 6-9 as a "selectable branch", which is a second gate path to keep in sync, not a removal of risk.

5. **The engine and panel limits bite at the gate A chose.** Panel max 8 reviewers (`panel.py:248`) against floors 10 and 12 (`task/SKILL.md:200-201`) [CODE-VERIFIED]: A's template covers 2 of the 4 tiers (A section 3.5). One-document merge (`merge_cmd.py:30-33`, `ledger.py:107`) [CODE-VERIFIED] against multi-file phase outputs: A needs one ledger per file plus partition merging, and code-output phases stay on Half 1 indefinitely (A section 7 part 2).

6. **One of A's static guards checks a control the harness ignores.** A's M1 asserts the gate text no longer says `mode: "bypassPermissions"`. This session's Agent tool schema says the spawn `mode` is "Deprecated; ignored. Subagents inherit the parent session's permission mode; agent-definition frontmatter may override it" (diff X-004). That check guards text, not behaviour. (A's first M1 check, on the tools allowlist, is the right one.)

7. **A goes past the adjudicated slots and the owner boundary.** It answers owner question Q3 (A line 22) although the C-11 row reserves it for the owner (`undecidable-conflicts.md:28`); it adds a checklist completion predicate on top of C-03's "block valid" (A line 29); it makes the 6-agent floor a module parameter where C-03 left the owner open (A section 0).

8. **Internal count error in A's M2 golden.** A line 28 counts 8 packaged templates; A line 115 lists "default, `live7`, the seven reflect files" (9). Glob finds 8: default, live7 and six reflect files (diff X-007) [carried from the diff analyst's Glob]. Minor, but it is in the test plan.

9. **A changes the panel core for one consumer.** Adding `lens` to `_SLOT_KEYS` (`panel.py:46`) [CODE-VERIFIED] is cheap (X-002), but the lens already travels as free text in the brief (`persona_lens`, `reflect-reviewer.md:56`) [CODE-VERIFIED]; no consumer yet needs the core to know it.

#### Concessions

1. **X-002: B is wrong on the hash.** `template_sha256` hashes the template object and `_SLOT_KEYS` (`panel.py:46`) is an accept-list checked at `panel.py:215-216` [CODE-VERIFIED]; widening it edits no template file and changes no hash. B's "schema change over all 8 packaged templates and their validate tests" overstated the cost. B's reason to defer `lens` is now only "no consumer needs it yet", not cost.
2. **A-006: B's install sentence is wrong.** B said a new agent "must be installed (`tests/unit/test_cli_install.py:64` lists the rf-* agent files)". The table is the member list of the 4.3.5 baseline wheel (`test_cli_install.py:46-53`) and `_assert_present` fails only on a missing listed name (`:502-506`) [CODE-VERIFIED]. An unlisted new agent passes. The real cost is `make sync-dev` / `verify-sync` (INV-K).
3. **X-006: B's C-03 condition-7 dependency does not apply to A's design.** A computes confidence per reviewer from its own checklist rows (`rf-qa.md:505`), not from ledger support flags.
4. **INV-G stays unmet for the legacy lens agents in B's first change.** The pilot shows no out-of-report file-tool write to a repo path in 366 runs, but Bash was screened, not fully classified (48 of 78 candidates unread), the transcripts cover this machine only, and retention is unknown. Absence in the sample is not a mechanism.
5. **M-B1's decision rule as written has a gap.** "Zero writes outside the agent's own report path" supports B; "one write to a reviewed output file" refutes it. The pilot found 147 `/tmp` scratch writes, which satisfy neither clause. The rule needs three classes fixed before the full audit: (a) own report path or `/tmp` scratch: neutral; (b) any repository working-tree path other than the own report: refutes B-3; (c) git state changes in the reviewed repository: refutes B-3.
6. **B's first change is not literally "touches no existing file".** Some skill must call the new document gate (for example `readme/SKILL.md` or the PRD skill); B names no document type and no host file. That host edit must also leave its own pinned strings intact. The PRD skill already runs "intentional, acceptable double QA" with `/task` (`src/superclaude/skills/prd/SKILL.md:423`) [CODE-VERIFIED], so an additive panel run adds a third QA pass and its cost.
7. **C-012: A advances future PR review further** (per-slot lens, checklist mode, replay fixture); B delivers only the read-only reviewer and persistence pattern.
8. **User-visible value of B's first step is small**, as B section 7 says, and spec-panel already reviews spec-like single documents.
9. **A's Half 1/Half 2 split is a real contribution** (U-001). If the owner answers Q3 "yes", B's own fallback should be A's Half 1 limited to an agent split plus orchestrator persistence, without the panel.

#### Shared assumptions

| ID | Response | Reasoning |
|---|---|---|
| A-001 | QUALIFY | The pilot supports it: a `reflect-reviewer` write attempt returned "No such tool available" [RUN-VERIFIED], and 517 reflect-reviewer runs show only read and search tools. One refusal is one observation on this harness; any first change should still keep a tree-hash check (A's M5 idea) as the behavioural backstop. |
| A-002 | QUALIFY | Observed reflect-reviewer calls were only Read/Grep/Glob and codegraph search/node/callers/explore [RUN-VERIFIED]; the user's CLAUDE.md states "codegraph tools are read-only". Augment search side effects are [UNVERIFIED]; a static test that lists every allowed tool name explicitly would close it. |
| A-003 | QUALIFY | Real gap for both variants; today the agent writes its own report (3,146 such writes in the pilot), so orchestrator persistence is new behaviour. The new gate should store a hash or byte count of each returned text beside the persisted report; B's single-document gate is a cheaper place to prove that than the `/task` gate. |
| A-004 | REJECT | The pilot shows lens discipline in practice includes Write/Bash work (mutation tests on `/tmp` copies, scratch git repos) [RUN-VERIFIED], so a read-only lens-string reviewer does not keep rf-qa's verification surface. Any arm-1 measurement must state which instruction body the new reviewer carries, or it measures "read-only plus a thinner prompt". |
| A-005 | QUALIFY | Neither variant states repeat counts; real-agent arms need at least a pre-registered repeat count per arm and a variance bound before one comparison decides. |
| A-006 | REJECT | Code contradicts it (concession 2): `_assert_present` (`test_cli_install.py:502-506`) fails only on missing listed names. |
| A-007 | ACCEPT | Both variants leave `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, `pr_submit` and `cli/reflect` unedited; B also leaves `task/SKILL.md` unedited. |
| A-008 | ACCEPT | Both build the oracle before rf-qa loses authority; they differ only on where (C-005). |

#### Per-point positions

| ID | Preferred | Evidence (one sentence) |
|---|---|---|
| S-001 | HYBRID: A's consistency-check-first order plus B's separate "what I did not verify" section | A's order lets a reader check slot consistency before the argument; B's separate list keeps unverified items findable. |
| S-002 | B | Clauses B-1/B-2/B-3 each have their own falsifier, so a judge can accept one and reject another (as the pilot now does for B-3). |
| S-003 | HYBRID: B's clause-keyed structure with A's claim/evidence/tag table per clause | A's E1-E9 table is easier to audit line by line; B's keying ties each item to a decision. |
| S-004 | B | B uses the synth-06 ids INV-A..INV-N that the conflict row and the other slots use. |
| S-005 | HYBRID: A's ordered pipeline (static, deterministic replay, model replay) with each step keyed to the clause it decides | A's no-model deterministic arm is cheap and missing from B; B's clause keying says which result changes which decision. |
| C-001 | B | `/task` is one of 8 skill files carrying 93 report-only spawn markers and step-5 lenses are spawned "exactly as written" (`task/SKILL.md:250`); a single document fits `merge --doc` and `merge_round` without a locator. |
| C-002 | B | 366 report-only rf-qa/rf-qa-qualitative runs show 0 Write/Edit calls to repository paths outside their reports [RUN-VERIFIED], while hardening would remove the Write/Bash mutation testing that 4 of 16 lens agents used. |
| C-003 | B | The lens already travels as free text (`persona_lens`, `reflect-reviewer.md:56`); no first-step consumer needs the core to hold it (cost argument conceded under X-002). |
| C-004 | B | The checklist gate already runs inside `rf-qa.md:484-534`; adding a completion predicate the C-03 adjudication did not conclude is not needed for a first step. |
| C-005 | HYBRID: B's document-level seeded set plus A's deterministic no-model arm, tree-hash check and UNVERIFIABLE-share metric | A single file needs no locator for seeding and scoring, and A's extra metrics catch mutation and capability loss. |
| C-006 | HYBRID: Halves are separable (A), but Half 1's scope includes persistence, step 10 and Bash loss (B), so it runs only when Q3 is answered yes or M-B1 finds a repo write | X-003 code check supports B on scope; U-001 is a real decomposition. |
| C-007 | B | The gate runs after every phase with "No exceptions" (`task/SKILL.md:192, 286`); B edits no existing gate. |
| C-008 | B | Byte-identical files checked by `git diff --stat` are a stronger guarantee than editing steps 3-10 around nine cap rows and two other pins. |
| C-009 | HYBRID: Accept A's document-output scoping for any later `/task` Half 2 and run B's M-B4 anchor probe before it | X-005 shows the two statements are reconcilable (B for the whole gate, A for Half 2). |
| C-010 | B | M-B1 measures the current exposure and is feasible: the pilot ran over 366 real report-only transcripts; A's tree-hash check should be added to future oracle runs. |
| C-011 | B | The panel cap is 8 (`panel.py:248`) against floors 10/12; B's additive run forces no floor-owner decision (C-03 INV-003). |
| C-012 | A | A delivers per-slot lens, checklist mode and replay fixture that r13 lists for PR review; B delivers only the read-only reviewer pattern. |
| X-001 | B | Code check supports B: 93 markers in 8 files, step-5 lenses spawned as written; the pilot's out-of-report writers were domain lenses. |
| X-002 | A | `template_sha256` hashes the template and `_SLOT_KEYS` is an accept-list (`panel.py:46, 215-216`), so no template or hash changes. |
| X-003 | B | Step 10 (`task/SKILL.md:260`) assumes the agent writes, and 3,146 report writes in the pilot show persistence is the lens agents' main write activity. |
| X-004 | B | The harness schema says spawn `mode` is ignored and frontmatter decides, so the control is the agent file. |
| X-005 | HYBRID: B's statement for the whole gate, A's for Half 2 limited to document outputs | Both rest on the one-document merge (`merge_cmd.py:30-33`, `ledger.py:107`). |
| X-006 | A | A's checklist confidence is per reviewer (`rf-qa.md:505`), so C-03 condition 7 does not constrain it. |
| X-007 | B | 8 packaged templates (default, live7, six reflect) per the diff analyst's Glob; A's M2 lists 9. |
| A-001 | HYBRID: Both variants rely on it; add a tree-hash check to every oracle run | The runtime refused a reflect-reviewer Write once [RUN-VERIFIED]; one observation is not a guarantee. |
| A-002 | HYBRID: Add a static test that pins the full allowed tool list of each new reviewer | Observed calls were read-only; Augment search side effects are [UNVERIFIED]. |
| A-003 | HYBRID: Store a hash or byte count of each returned report next to the persisted copy | Agent-side persistence is the current behaviour (3,146 writes), so fidelity of the new path must be checked. |
| A-004 | HYBRID: Name the instruction body of the new reviewer and add an oracle arm with the same body | The pilot shows lens work uses Write/Bash for mutation tests, so prompt body and tools must be measured apart. |
| A-005 | HYBRID: Pre-register a repeat count per arm and a variance bound | Neither variant states one; a single real-agent comparison cannot decide. |
| A-006 | A | A's "may need ... [UNVERIFIED]" is closer to the code; B's "must be installed" is contradicted by `_assert_present` (`test_cli_install.py:502-506`). |

Tally: A 4 (C-012, X-002, X-006, A-006); B 14; HYBRID 12; NEITHER 0. Total 30.

#### What I did not verify

- The 48 unread Bash candidates of the pilot screen; the full Bash classification of 5,261 calls.
- Whether transcripts on other machines or older, deleted transcripts would change the M-B1 count.
- Whether every standard-lens spawn prompt carries `fix_authorization: false` in its first message (the selection rule depends on it).
- Augment search tool side effects (A-002); target-runtime enforcement beyond the one refused call (A-001).
- No repository file other than this statement was written; no test was run; no git command mutated anything.

## Round 2: Rebuttals

### Variant A Rebuttal
### Round 2: Rebuttal of the Variant A advocate (slot C-11, rfqa-first-step-and-readonly-scope)

Advocate: A (Proposal A, `variant-1-original.md`). Round 2, first speaker. Focus: correctness, risk, test-coverage.
Read for this round: `diff-analysis.md`, `variant-1-original.md`, `variant-2-original.md`, `round1-advocate-A.md`, `round1-advocate-B.md`, row C-11 of `phase-outputs/discovery/undecidable-conflicts.md:28`. No other `round2-*` file was read.
Tags: [CODE-VERIFIED] read at the cited path:line in this session; [RUN-VERIFIED] observed by a read-only `uv run --no-project python` script in this session (scratch only under a `mktemp -d /tmp/advA-r2.XXXXXXXX` directory, removed by an exit trap); [UNVERIFIED].
Transcript rule kept: every transcript whose text contains the run-1 task id or the queued-run file name was skipped by the script before parsing (117 rf-qa / rf-qa-qualitative transcripts skipped); none of them is quoted or counted below.
Citation shorthand: `A:n` = `variant-1-original.md` line n; `B:n` = `variant-2-original.md` line n; `B-R1:n` = `round1-advocate-B.md` line n.

#### Response to criticisms

B's "Weaknesses identified (Variant A)" 1-9 (B-R1:46-62), answered one by one.

1. **"A's safety claim does not reach the agents that actually used write tools" (B-R1:46).** Partly conceded, partly turned. Conceded: `/task` steps 3-4 govern only the standard eight lenses; step 5 and skill-embedded lenses are spawned "exactly as written" (`src/superclaude/skills/task/SKILL.md:250`) [CODE-VERIFIED], and my re-check of the transcripts found no prompt that uses the steps 3-4 report-path pattern with a standard lens name (`qa-structural-<template|consistency|evidence|completeness>` or `qa-content-<actionability|numbers|cross-reference|domain-accuracy>`) [RUN-VERIFIED, regex over first prompts]; the standard lens dimensions are spawned in practice from skill or task-file gate items. So A's premise that steps 3-4 are "the most-run gate" is not supported by the observed corpus, and I move C-001 off A. Turned: the one observed write by a report-only lens to a file that was not its own report came from a domain lens and hit another lens's report (New evidence N1). The failure mechanism (every lens self-persists into one shared `qa/` folder, `task/SKILL.md:238`, with Write) is not lens-specific; standard lenses carry it too. The cure is an agent definition that cannot write plus executor-side persistence, which is reusable at every spawn site by a `subagent_type` change.
2. **"Half 1 is not an agent-type change at the spawn sites" (B-R1:48).** Conceded in Round 1 (concession 2, X-003): Half 1 also moves persistence to the executor and rewrites step 10 (`task/SKILL.md:260`, "Check that each lens agent wrote its report to the expected path") [CODE-VERIFIED]. It still needs no panel code.
3. **"Half 1 removes a used capability before A's oracle can measure the loss" (B-R1:50).** The ordering half is wrong: A builds M1-M5 "first, before any `/task` text changes" (A:111) [CODE-VERIFIED in the variant text], so no lens loses Bash before the model arm runs. The capability half is right and now quantified (N3): 437 of 571 non-fix rf-qa / rf-qa-qualitative transcripts used Bash, 74 ran pytest, 28 ran `sed -i`, 15 wrote under `/tmp` [RUN-VERIFIED]. But in the 118 whose description names a standard lens dimension, only 1 ran pytest and 1 ran `sed -i` [RUN-VERIFIED]: mutation testing lives in domain lenses (`test-adequacy`, `security-invariants`), not in the eight standard lenses. I accept the consequence: the first switch covers the standard eight only; domain lenses keep their agent until a read-only replacement for mutation testing is measured.
4. **"Largest blast radius, by A's own rating" (B-R1:52).** Conceded as rated (A:102, HIGH). Answered by scope: in the resolution below no gate engine changes in the first change, and the only gate edit is a conditional agent switch for the standard lenses, guarded by the arm-0 / arm-1a replay and the unedited pinned suites. The "selectable branch" of A:102 is dropped (B is right that it is a second path to keep in sync).
5. **"The engine and panel limits bite at the gate A chose" (B-R1:54).** Accepted for Half 2: panel max 8 (`panel.py:247-248`) against floors 10/12 (`task/SKILL.md:200-201`) [CODE-VERIFIED for `task/SKILL.md`], and one-document merge (`ledger.py:107`). Not relevant to Half 1, which uses no panel. Half 2 leaves the first change entirely.
6. **"One of A's static guards checks a control the harness ignores" (B-R1:56).** Conceded in Round 1 (concession 3, X-004). Additional defect found this round: the allowlist guard must also treat `Agent`, `Task` and `SendMessage` as mutators, because `rf-qa.md:20-24` grants all three to the current report-only lens agents [CODE-VERIFIED], and `_MUTATORS` at `tests/cli/reflect/test_reviewer_readonly_tools.py:30` lists `Task` but not `Agent` or `SendMessage` [CODE-VERIFIED].
7. **"A goes past the adjudicated slots and the owner boundary" (B-R1:58).** Conceded. The C-11 row says "whether the lens agents are made read-only in the first change (Q3) and which 'eight lens' set is meant are owner decisions" (`undecidable-conflicts.md:28`) [CODE-VERIFIED this session]. A:22 "answered yes" oversteps. The resolution puts Q3 to the owner with the pilot evidence and makes the standard-lens switch conditional on the owner's yes. The checklist completion predicate and the floor parameter leave the first change (C-004, C-011 to B).
8. **"Internal count error in A's M2 golden" (B-R1:60).** Conceded (Round 1 concession 5): 8 packaged templates, six of them reflect.
9. **"A changes the panel core for one consumer" (B-R1:62).** Conceded (Round 1 concession 7): the `lens` slot key waits for a consumer; C-003 moves to B.

B's pilot (B-R1 Strengths 3-5) is answered in `## Pilot re-check`. Summary: Strength 5 reproduces exactly; Strength 4 reproduces for the two harnesses I re-opened; Strength 3's headline "0 to any other path" hides one Write plus four Edits by a report-only lens into another lens's report, which under B's own refined decision rule (B-R1:70, class (b): "any repository working-tree path other than the own report: refutes B-3") refutes B-3 as stated.

#### Updated assessment of Variant B

What B's defences established, and I now accept:
- X-001 holds more strongly than the diff analyst showed: not only are lens spawns replicated in 8 skill files, the observed spawns of standard lens dimensions come from skill or task-file gate items, not from `/task` steps 3-4 text (N2).
- The capability argument (A-004) is real and measurable; domain lenses use Write and Bash for mutation testing on `/tmp` copies (N3).
- B-3's cost list (second agent definition, executor persistence, step 10 rewrite, Bash loss) is accurate (B:106).
- The engine-fit argument for any panel engine at a gate (B:42, one candidate per merge) is correct, so no engine swap belongs in the first change.

Where B is weaker than its Round 1 statement says:
- **The pilot's headline is wrong in substance.** "0 to any other path" (B-R1:32) is true only because the bucket "QA/report paths" was not split into own report versus another agent's report. One report-only lens (prompt: "Modify no file except your report") overwrote another lens's report; two blocking findings were lost until the orchestrator noticed and restored the file from the first agent's transcript (N1). This is the exact hazard A named (A:70: every lens writes into the same `qa/` folder; "No other agent modifies files during this step" is a convention) and it shows the prompt convention failing in a real run.
- **B's M-B1 rule now fires.** B's refined rule (B-R1:70) puts "any repository working-tree path other than the own report" in class (b), which "refutes B-3". The overwritten file is under `.dev/tasks/to-do/<task>/qa/gate-c/` in a worktree (a tracked repository path per the project rule that `.dev/tasks/` is always staged). B's own pre-commitment (B:84, B:105) then moves "an agent-definition split only, without the panel" into the first change.
- **B's selection rule misses agents.** It selects on the literal string `fix_authorization: false`; 155 lens-like rf-qa transcripts carry neither literal. They show 0 writes outside QA/report/`/tmp` paths [RUN-VERIFIED], so the conclusion survives, but the denominator is not "all report-only lens runs".
- **B's raw counts double-count.** Each tool call appears twice in many transcripts (once with a timestamp, once without); deduplicated by `tool_use` id the numbers fall by about half (Pilot re-check). B warned of this (B-R1:32); the magnitudes should not be quoted as call counts.
- **B's document gate still has no host** (B-R1:71 concedes it) and replaces nothing (B:98). It remains a weaker first step than shipping the read-only lens agent and its oracle, which every later step (B's included) needs.

Net: B is right that the first change should not swap any gate engine and should not touch domain lenses; A is right that the self-persisting, write-capable lens design has already lost findings in a real run, so the read-only lens agent and executor persistence belong in the first change.

#### New evidence

N1. **A report-only lens overwrote another lens's report in a real gate run** [RUN-VERIFIED]. Worktree `issue-331-github-issue-watcher`, task `TASK-RF-issue-watcher-20261107-150955`, Gate C (task-file items 7.G2-7.G7).
- `agent-a00026ccf75eb50ac.jsonl` (rf-qa-qualitative, "Gate C lens design-correctness", prompt carries `fix_authorization: false`) created `qa/gate-c/qa-content-design-correctness-report.md` at 2026-11-08T00:07:51Z.
- `agent-abed84d24b847251c.jsonl` (rf-qa-qualitative, "Gate C lens security-invariants", prompt carries `fix_authorization: false (report-only)` and "Modify no file except your report") ran Write on the same path at 00:12:07Z (result "The file ... has been updated", i.e. an overwrite), then four successful Edits to 00:12:51Z. Its prompt delegated to the task-file item text, and the agent took the design-correctness lens.
- The orchestrator (main session `c619f49d...`) at 00:17:41-00:17:44Z copied the stray file to `qa-content-design-correctness-report-run2.md`, restored the original from the first agent's transcript, re-spawned the security-invariants lens "with its own explicit report path" (`agent-ad808ee6d7eb36624.jsonl`, 00:17:48Z), and wrote at 00:17:54Z: "The agent I started for the security-invariants lens wrote its report into the design-correctness file and overwrote the first design-correctness report. I restored the original from that agent's saved transcript, byte for byte." The original run had 3 blocking findings, the stray 1.
- Step 10 of the gate would not have caught it: it checks that each report exists (`task/SKILL.md:260`) [CODE-VERIFIED]; it would flag the missing security-invariants report but not the lost content of the design-correctness report.
- Count: this is the only path written successfully by two distinct non-fix rf-qa agents in the corpus scanned (571 non-fix transcripts) [RUN-VERIFIED]. One event; its cause is an ambiguous dispatch prompt; its damage mechanism is Write access plus self-persistence into a shared folder. A read-only reviewer with executor persistence keyed by the dispatched slot would have returned a mislabelled report and destroyed nothing.

N2. **`/task` steps 3-4, as written, are not where standard-lens traffic is observed** [RUN-VERIFIED, prompt regex]. No first prompt in the scanned rf-qa / rf-qa-qualitative transcripts uses the step-3/4 path pattern with a standard lens name; the only task using the `qa-structural-*` / `qa-content-*` pattern is the issue-331 task, with domain lens names. 118 of 571 non-fix transcripts have descriptions naming a standard lens dimension ("Gate 3 template-conformance lens", "Phase 6 lens: template-conformance", "Gate 3 domain-accuracy lens"); they are spawned from skill or task-file items. Attribution by description is heuristic [UNVERIFIED beyond the regex].

N3. **Bash use splits by lens kind** [RUN-VERIFIED]. Non-fix rf-qa / rf-qa-qualitative transcripts (fix agents excluded by description or `fix_authorization: true`): 571; with any Bash 437; Bash limited to simple read commands (wc, grep, ls, cat, head, `sed -n`, awk, find, read-only git) 50; pytest 74; `sed -i` 28; Write/Edit under `/tmp` 15. Standard-lens-named subset (118): any Bash 86, simple reads only 18, pytest 1, `sed -i` 1. So standard lenses use Bash mainly for computing over files (counts, line lengths, parsing), which pre-computed evidence in the brief or Grep/Read can cover; mutation testing is a domain-lens activity. Classifier regexes are coarse [counts are screens, not a full classification].

N4. **The current lens agent can spawn and message other agents** [CODE-VERIFIED]. `src/superclaude/agents/rf-qa.md:5-24`: `permissionMode: bypassPermissions` and tools including Write, Edit, Bash, NotebookEdit, Agent, Task, TaskOutput, TaskStop, SendMessage. A "report-only" lens can start a write-capable subagent. The reflect guard's `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` (`tests/cli/reflect/test_reviewer_readonly_tools.py:30`) would not flag `Agent` or `SendMessage`; a guard copied for the new lens agent must test the allowlist as a subset of a named read-only set.

N5. **The runtime refuses tools outside the allowlist** [RUN-VERIFIED]. 517 reflect-reviewer transcripts (deduplicated tool calls: Read 7,110, Grep 5,139, Glob 655, codegraph node 53, callers 6, search 6, explore 1); two calls outside the allowlist, both refused with "Error: No such tool available" (`mcp__razor_culture__pool_Write` and a malformed `pool_Read_placeholder`). The `reflect-reviewer.md:5` allowlist (Read, Grep, Glob, Augment search, four codegraph tools) with `permissionMode: plan` (`:8`) is the working pattern [CODE-VERIFIED].

N6. **An isolation precedent exists for reviewers that need execution** [CODE-VERIFIED]. `src/superclaude/cli/reflect/models.py:94-100` defines `isolate_reviewers`, "PINNED OFF by default", which grounds reviewers "in a `git worktree` snapshot"; `runner.py:721-740` creates it and points `reviewer_grounding_root` at it. It is a grounding root for the reflect CLI's own review children, not a write barrier for Agent-tool subagents; whether it can serve domain lenses that run mutation tests is [UNVERIFIED]. It is named only as an open path for domain lenses, not as a first-change item.

#### Pilot re-check

Method: three read-only scripts over `/home/coder/.claude/projects/**/subagents/*.meta.json` and sibling `.jsonl`; tool calls deduplicated by `tool_use` id; results matched by `tool_use_id`; transcripts containing the run-1 task id or queued-run file name skipped before parsing. The corpus has grown since B's run (meta counts now: rf-qa 512, rf-qa-qualitative 305, reflect-reviewer 519).

| B claim (B-R1) | Re-check | Verdict |
|---|---|---|
| 366 report-only transcripts (204 rf-qa + 162 rf-qa-qualitative) selected on `fix_authorization: false` and not `true` | 278 (155 + 123) after skipping 117 transcripts under the transcript rule | NOT REPRODUCED exactly; the difference is consistent with the skipped set plus corpus growth, which I cannot confirm without reading the skipped transcripts |
| Write/Edit: 3,146 QA/report, 147 `/tmp`, 2 `/dev/null`, 0 other | Deduplicated: 1,306 QA/report (1,009 to a path named in the agent's prompt, 297 to QA/report paths not named there), 69 `/tmp`, 1 `/dev/null` (error), 0 other | REPRODUCED in shape; magnitudes about halved by deduplication. "0 other" holds only because one agent's write into ANOTHER lens's report sits in the QA/report bucket (N1) |
| Bash 5,261; 78 screened candidates, 30 read, all scratch or text | Deduplicated Bash in the report-only set: 3,198. My broader screen flagged about 600 commands, dominated by false positives (awk comparisons, grep patterns, heredoc report text containing words like `git commit`); the samples I read were text matches or `/tmp`-scoped | NOT REPRODUCED as a count; no repository-mutating Bash found in what I read; full classification [UNVERIFIED] |
| 4 of 16 issue-331 lens agents wrote mutation harnesses under `/tmp` | Re-opened the two security-invariants agents: Gate D `agent-af15a6f5ea41057b3.jsonl` wrote `/tmp/secinv-harness/mutate.py`; Final `agent-a94fd9cd694c0cea1.jsonl` wrote `/tmp/iw-mut-harness/driver.py` and `/tmp/iw-mut/tests/...`. Test-adequacy harnesses not re-opened. I count about 20 lens transcripts in Gates C, D and Final, not 16 | PARTLY REPRODUCED (2 of 4 confirmed); the denominator 16 not reproduced |
| 517 reflect-reviewer transcripts, one refused Write | 517; one refused Write plus one refused malformed call | REPRODUCED (N5) |
| Report-only held for file tools in every observed run | One report-only lens overwrote another lens's report with Write + 4 Edits; 2 blocking findings lost until a manual restore (N1) | CONTRADICTED |

What the pilot implies:
- **C-002 (read-only scope of existing lens agents).** Weakens B-3: the prompt convention failed once with real loss, and B's own class-(b) rule fires. Weakens A's original scope: mutation testing in domain lenses would be lost by a blanket switch. Outcome: switch the standard eight lens dimensions (whose Bash use is read-type, N3) to a read-only agent with executor persistence once arm 1a passes; leave domain lenses until a replacement for mutation testing is measured.
- **C-006 (separability).** Supports A's split and refines it: Half 1 itself splits into standard lenses (switchable now) and domain lenses (not yet).
- **C-010 (what decides hardening).** Supports B's M-B1 as feasible and informative (it found N1, which a forward tree-hash check alone would not have found because the damage was inside a gate artifact, not the reviewed tree); supports A's tree-hash check for the future. The full audit must classify "another agent's report" as class (b) and deduplicate by `tool_use` id.
- **A-004 (instruction body).** Supports B's REJECT for domain lenses and a QUALIFY for standard lenses: arm 1a must carry rf-qa's verification and Confidence Gate sections and pre-computed counts where standard lenses used Bash, or it measures "read-only plus a thinner prompt".

#### Final position table

| ID | Final | Evidence (one sentence) |
|---|---|---|
| S-001 | HYBRID: consistency check against C-01/C-02/C-03 first (A's order) plus a separate "what was not verified" section (B) | Order lets a reader check slot consistency first; a separate list keeps unverified items findable; neither changes a claim. |
| S-002 | B | B's clauses B-1..B-3 each had a falsifier, which is how this round could accept B-1/B-2's "no engine swap" and refute B-3 separately. |
| S-003 | HYBRID: B's clause-keyed evidence with A's claim/evidence/tag table inside each clause | The table is easier to audit line by line; clause keying ties each item to the decision it moves. |
| S-004 | B | The synth-06 ids INV-A..INV-N are the ids the C-11 row (`undecidable-conflicts.md:28`) and the other slots use. |
| S-005 | HYBRID: A's ordered pipeline (static guards, deterministic replay, model replay) with each step labelled with the clause it decides | Both Round 1 statements proposed this same merge. |
| C-001 | HYBRID: the first change starts at the lens-reviewer level (one read-only lens agent definition plus a single-document seeded replay), wires no panel engine into any rf-qa gate, and its only gate edit is the conditional standard-lens switch at `/task` steps 3-4 | N2 shows steps 3-4 are not where lens traffic is observed and B shows no gate engine fits yet, while N1 shows the write-capable self-persisting lens already lost findings. |
| C-002 | HYBRID: domain and skill-embedded lens agents keep their agent files in the first change; the standard eight lens dimensions at `/task` steps 3-4 switch to the read-only agent with executor persistence in the first change only if arm 1a passes the pre-registered rule before merge and the owner answers Q3 yes | N1 refutes "zero exposure" under B's own class-(b) rule; N3 shows standard lenses use Bash for reading while domain lenses use it for mutation tests. |
| C-003 | B | The lens travels as free text (`reflect-reviewer.md:56`); no first-change consumer needs a `lens` slot key. |
| C-004 | B | The computed confidence gate stays inside the agent body (`rf-qa.md:484-534`), carried into the new lens agent; no completion predicate C-03 did not conclude. |
| C-005 | HYBRID: seeded single documents with clean twins (B's input) run through arm 0 (current lens agents) and arm 1a (read-only lens agent, same lens text, prose consolidation), with A's deterministic no-model arm, tree-hash check, UNVERIFIABLE-share metric and a pre-registered repeat count; the panel-engine arm waits for Half 2 | One file needs no locator (`ledger.py:107`), and only lens-level arms isolate the read-only effect. |
| C-006 | HYBRID: Half 1 (agent swap, executor persistence, step 10 rewrite) is separable from Half 2 (engine), is limited to the standard eight lenses, and lands only after arm 1a; Half 2 is not in the first change | X-003 supports B on Half 1's scope; N3 splits Half 1 by lens kind; B-R1:103's own condition (M-B1 finds a repository write) is met by N1. |
| C-007 | HYBRID: no engine swap at any gate in the first change; the only gate edit is the conditional standard-lens switch, guarded by arm 1a and the unedited pinned suites | The gate is mandatory after every phase (`task/SKILL.md:192, 286`), so only a measured agent swap, not an engine swap, is acceptable there first. |
| C-008 | HYBRID: `task/SKILL.md` stays byte-identical unless the standard-lens switch lands; then only steps 3, 4, 8 and 10 change and `test_review_severity_rule.py`, `test_review_prompt_overrides.py`, `test_worker_contract.py` pass with no test edited | B's M-B3 check is kept, with `task/SKILL.md` named as the one allowed pinned file under that condition. |
| C-009 | HYBRID: any later `/task` Half 2 is limited to document outputs, and B's M-B4 anchor probe runs before it is widened | Both rest on the one-candidate merge (`merge_cmd.py` `--doc`, `ledger.py:107`); both Round 1 statements agreed. |
| C-010 | HYBRID: run the full M-B1 audit before merge with B's three classes, "another agent's report" fixed as class (b), and deduplication by `tool_use` id; add the tree-hash no-mutation check to every replay run | The pilot found N1, which a reviewed-tree hash alone would not catch; the tree hash bounds future runs. |
| C-011 | B | With no panel at any gate in the first change, the prose floors 6/8/10/12 (`task/SKILL.md:196-201`) stay and no floor-owner decision (C-03 INV-003) is forced. |
| C-012 | HYBRID: the first change gives PR review the read-only reviewer definition and the replay fixture (r13 M5, M13); per-slot lens and checklist mode (M4, M9) wait | A's original M4/M9 delivery left the first change with C-003 and C-004. |
| X-001 | B | `task/SKILL.md:250` spawns embedded lenses "exactly as written", and N2 shows standard-lens dimensions are spawned from skill or task-file items in practice. |
| X-002 | A | `_SLOT_KEYS` is an accept-list (`panel.py:46, 214-216`) and `template_sha256` hashes the template object; both Round 1 statements agreed. |
| X-003 | B | Half 1 rewrites persistence and step 10 (`task/SKILL.md:238, 260`), with no panel code. |
| X-004 | B | Spawn `mode` is ignored and the tools allowlist is the control (N5: allowlist refusals observed). |
| X-005 | HYBRID: B's statement holds for the whole gate, A's for Half 2 limited to document outputs | Both rest on the one-document merge; both Round 1 statements agreed. |
| X-006 | A | A's confidence is per reviewer (`rf-qa.md:505`), so C-03 condition 7 does not bind it; B conceded (B-R1:68). |
| X-007 | B | 8 packaged templates (default, live7, six reflect); A:115 lists 9. |
| A-001 | HYBRID: rely on the tools allowlist, not `permissionMode`, add one runtime write-probe test for the new lens agent, and keep the tree-hash check on every replay | N5: two out-of-allowlist calls refused across 517 runs; one harness, one observation class. |
| A-002 | HYBRID: the guard asserts the new agent's allowlist is a subset of a named read-only set, with `Agent`, `Task`, `SendMessage`, `Bash`, `Write`, `Edit`, `NotebookEdit` as mutators | N4: `rf-qa.md:20-24` grants Agent/Task/SendMessage; `_MUTATORS` (`test_reviewer_readonly_tools.py:30`) omits Agent and SendMessage. |
| A-003 | HYBRID: the executor persists each returned report unedited to the path of the slot it dispatched and records its sha256 beside it | N1's loss came from agent-chosen paths; executor-keyed paths plus a hash give both uniqueness and fidelity. |
| A-004 | HYBRID: the new lens agent's body is rf-qa's verification, zero-trust and Confidence Gate sections without the fix sections, standard lenses get pre-computed counts in the brief where they used Bash, and domain lenses that run mutation tests are excluded from the switch | N3: standard lenses rarely execute (1 pytest in 118), domain lenses do (B-R1:34, re-checked for 2 agents). |
| A-005 | HYBRID: pre-register a repeat count per arm and a variance bound before the first model run | Neither variant states one; both Round 1 statements agreed. |
| A-006 | A | `_assert_present` (`test_cli_install.py:502-506`) fails only on a missing listed name, so A's "may need ... [UNVERIFIED]" is closer than B's "must be installed"; B's Round 1 chose A here. |

Tally: A 3 (X-002, X-006, A-006); B 9 (S-002, S-004, C-003, C-004, C-011, X-001, X-003, X-004, X-007); HYBRID 18 (S-001, S-003, S-005, C-001, C-002, C-005, C-006, C-007, C-008, C-009, C-010, C-012, X-005, A-001, A-002, A-003, A-004, A-005); NEITHER 0. Total 30.

#### Proposed resolution

1. The first rf-qa change is lens-level: it adds one read-only lens-reviewer agent definition and a replay oracle, and wires no panel engine (`resolve`/`merge`/`ledger`) into any rf-qa gate; B's single-document panel module and A's `/task` Half 2 are both later steps.
2. The new agent's frontmatter lists exactly Read, Grep, Glob and the read-only search tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections; it names other primitives by installed path; `make sync-dev` and `make verify-sync` run.
3. A new guard test asserts the agent's allowlist is a subset of a named read-only set (Agent, Task, SendMessage, Bash, Write, Edit, NotebookEdit are mutators), plus a negative fixture, plus one runtime write-probe in a `tmp_path` repository.
4. The replay oracle (built before any gate text changes) uses seeded single documents with clean twins and runs arm 0 (current rf-qa / rf-qa-qualitative lens agents) and arm 1a (new agent, same lens text, prose consolidation) per standard lens dimension, with a deterministic no-model arm, pre-registered repeat count, variance bound and decision rule; metrics: per-lens recall in a blocking row, wrong blockers on clean twins, UNVERIFIABLE share, tree-hash no-mutation, tokens and wall-clock.
5. The full M-B1 transcript audit runs before merge, deduplicated by `tool_use` id, with classes: own report or `/tmp` scratch = neutral; another agent's report or any other repository working-tree path = refutes leaving the agents as they are; git state change in the reviewed repository = refutes. The issue-331 Gate C overwrite is recorded as the first class-(b) event.
6. Owner question Q3 is put to the owner with items 4-5's evidence; A's recommendation is yes for the standard eight lens dimensions only.
7. If arm 1a meets the registered rule for a dimension before merge and the owner says yes, the first change also switches that dimension at `/task` steps 3-4 (and the step-8 verification pair) to the new agent, moves report persistence to the executor (returned text written unedited to the dispatched slot's path, sha256 recorded), and rewrites step 10 to check executor-persisted files; otherwise `task/SKILL.md` stays byte-identical.
8. Out of the first change: per-slot `lens` key, checklist completion predicate, any `/task` panel template, floor parameter, domain and skill-embedded lens spawn sites, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, the ten S1-S3 files, `pr_submit`, `cli/reflect`.
9. Mechanical scope check: `git diff --stat` names only the new agent file, its tests, the oracle script and tests, and (only under item 7) `task/SKILL.md`; `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_worker_contract.py tests/review -q` passes with no test edited.
10. Open condition, domain lenses: they keep their agent until a read-only path for mutation testing (pre-computed evidence, or an isolated execution such as the reflect `--isolate-reviewers` snapshot pattern, suitability [UNVERIFIED]) is measured against arm 0 on the same oracle.
11. Open condition, engine: any gate engine swap (B's document gate or A's Half 2) waits for the C-01 T-a probe (M-B4), the C-03 floor-owner answer and C-02's `next`/`--resolution` caller rules, and runs in shadow with rf-qa as authority until a replay says otherwise.
12. Open condition, evidence quality: the transcript audit covers one machine and unknown retention; the "eight lens" set meant by Q5 stays an owner decision.


### Variant B Rebuttal
### Round 2: Rebuttal of the Variant B advocate (slot C-11, rfqa-first-step-and-readonly-scope)

Advocate: B (Proposal B, `variant-2-original.md`). Round 2, second speaker. Focus: correctness, risk, test-coverage.
Read for this round: `diff-analysis.md`, `variant-1-original.md`, `variant-2-original.md`, `round1-advocate-A.md`, `round1-advocate-B.md` (mine), `round2-advocate-A.md`, row C-11 of `phase-outputs/discovery/undecidable-conflicts.md:28`. No other `round2-*` file was read.
Tags: [CODE-VERIFIED] read at the cited path:line in this session; [RUN-VERIFIED] observed by a read-only `uv run --no-project python` script in this session (scratch only under `mktemp -d /tmp/advB-r2.XXXXXXXX` directories, each removed by an exit trap); [UNVERIFIED].
Transcript rule kept: every transcript whose text contains the run-1 task id or the queued-run file name was skipped before parsing (117 rf-qa / rf-qa-qualitative transcripts skipped, the same number A reports); none is quoted or counted. The issue-331 main session transcript was checked and contains neither string.
Citation shorthand: `A:n` = `variant-1-original.md` line n; `B:n` = `variant-2-original.md` line n; `A-R1:n` = `round1-advocate-A.md` line n; `B-R1:n` = `round1-advocate-B.md` line n; `A-R2:n` = `round2-advocate-A.md` line n. `T331` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-331-github-issue-watcher/c619f49d-c032-4bb0-b1e5-6781bebedb7c` (main session `.jsonl` beside it, subagents under `subagents/`).

#### Response to criticisms

##### A's Round 1 weaknesses of Variant B (A-R1:37-44)

1. **"Known write path left open; M-B1 may be unrunnable; absence of logs reads as safety" (A-R1:37).** The "unrunnable" half is answered: M-B1 ran in Round 1 and again in Round 2 (278 report-only transcripts under the skip rule, 571 non-fix rf-qa / rf-qa-qualitative transcripts) [RUN-VERIFIED]. The substantive half is CONCEDED: the audit found one event that falls in my own class (b) (N1, verified below), so B-3 as stated ("the `/task` lens agents' tools and mode are not changed in the first change" with no hardening item) is refuted by B's own pre-committed rule (B:84, B-R1:70). I also accept the "absence reads as safety" point as a defect of the rule: an empty or unreadable corpus must give no verdict, not support. That fix is in my resolution, item 5.
2. **"Plan-mode agent is not the control under a bypass parent" (A-R1:38).** CONCEDED. The control is the `tools` allowlist; N5 (two out-of-allowlist calls refused across 517 reflect-reviewer runs) and my Round 1 strength 5 both show the allowlist working. B:17's "a plan-mode agent without Write, Edit or Bash" is replaced by "an agent whose `tools` list is a subset of a named read-only set".
3. **"B's first change replaces nothing and has no host" (A-R1:39).** CONCEDED (B-R1:71, B-R1:73). The document-gate module leaves the first change. What survives of B-2 is the cheap oracle input: seeded single documents with clean twins, which A-R2 adopted (A-R2:93, A-R2:122).
4. **"B's two-implementations argument applies to B" (A-R1:40).** CONCEDED as symmetric. A shadow document gate is a second implementation; so is a new read-only lens agent that coexists with `rf-qa` at every other spawn site under A's resolution. Any staged migration runs two implementations for an interval, so this argument decides nothing for either side and I withdraw it as a reason.
5. **"Schema-change claim wrong on the mechanism" (A-R1:41).** CONCEDED in Round 1 (B-R1:66).
6. **"C-03 condition 7 does not bind A's design" (A-R1:42).** CONCEDED in Round 1 (B-R1:68).
7. **"Install-cost claim contradicted by code" (A-R1:43).** CONCEDED in Round 1 (B-R1:67).
8. **"B's oracle does not test the read-only question" (A-R1:44).** CONCEDED. M-B2 compared "the existing lens gate" with "the panel gate" (B:86), which changes engine, prompt and permissions together. A's arm 0 versus arm 1a (same lens text, prose consolidation, only the agent changes) isolates read-only; I adopt it.

##### A's Round 2 claims about my pilot (A-R2 "Pilot re-check", A-R2:61-78)

| A's claim | My answer |
|---|---|
| 366 not reproduced; 278 under the skip rule | ACCEPTED. Round 1 did not state a skip rule for run-1 transcripts; 278 is the count to quote. I reproduced the same 117 skipped transcripts this round [RUN-VERIFIED]. Which of my 366 were run-1 transcripts I did not re-establish. |
| Magnitudes halved by deduplication by `tool_use` id | ACCEPTED. B-R1:32 warned of duplicated records; counts below are deduplicated. |
| "0 to any other path" hides one Write plus four Edits into another lens's report | ACCEPTED and verified (N1 section): Write at 00:12:07Z plus Edits at 00:12:23, 00:12:24, 00:12:26, 00:12:51Z, all successful. My bucket "QA/report paths" did not split own report from another agent's report; that was a classification defect. |
| Bash count not reproduced; no repository-mutating Bash found | ACCEPTED. My own Round 2 screen of every `sed -i` / `perl -pi` call by non-fix agents (28 agents) found only scratch or variable targets (NB7). |
| 4 of 16 issue-331 lens agents wrote mutation harnesses: 2 confirmed, denominator 16 not reproduced | ACCEPTED as stated; I did not re-count the denominator. N1's own agent adds one more execution case (it ran seven `/tmp/gatec-probe` scripts, NB5). |
| Selection on the literal `fix_authorization: false` misses 155 lens-like transcripts | ACCEPTED. My Round 2 classification selects non-fix agents by excluding `fix_authorization: true` and fix-like descriptions, the same rule A used, and gives 571. |
| Report-only held in every observed run: CONTRADICTED | ACCEPTED. One report-only lens destroyed another lens's report on disk (N1). |

##### A's new evidence N1-N6

- **N1**: VERIFIED with two corrections on cause and damage (see `## Verification of N1-N3`). It falls in my class (b). I concede B-3.
- **N2**: VERIFIED (zero first prompts use the step-3/4 path pattern with a standard lens name). My regex counts 107 standard-lens-named transcripts against A's 118; same shape.
- **N3**: VERIFIED in shape (571 / 437 / 28 / 15 match exactly; pytest 77 against A's 74; standard-lens subset pytest 2, `sed -i` 1, `/tmp` writes 0).
- **N4**: VERIFIED. `src/superclaude/agents/rf-qa.md:20-24` lists Agent, Task, TaskOutput, TaskStop, SendMessage; `tests/cli/reflect/test_reviewer_readonly_tools.py:30` is `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` [CODE-VERIFIED]. The guard must treat Agent, TaskOutput, TaskStop and SendMessage as mutators too.
- **N5**: not re-run by me this round; it matches my Round 1 strength 5 (B-R1:36), so I accept it.
- **N6**: not verified by me (`cli/reflect/models.py`, `runner.py` not opened this round) [UNVERIFIED]. It is only named as an open path, so it moves no decision.

#### Updated assessment of Variant A

What A's Round 2 now gets right:
- N1 is real and is the first observed failure of the "report-only by prompt" convention with on-disk damage; it fires B's own class-(b) rule, so a hardening item belongs in the first change.
- No gate engine belongs in the first change (A-R2:119). A's withdrawal of the per-slot `lens` key, the checklist completion predicate and the floor parameter (A-R2:91-92, A-R2:99) removes every point where A went past C-01/C-03.
- Q3 goes to the owner (A-R2:19, A-R2:124), as the C-11 row requires ("whether the lens agents are made read-only in the first change (Q3) ... are owner decisions", `undecidable-conflicts.md:28`) [CODE-VERIFIED].
- The arm 0 versus arm 1a oracle isolates the read-only effect; the guard must be a subset test, not a denylist.
- The split of Half 1 by lens kind (standard lenses rarely execute; other lenses do) is supported by the corpus.

What remains wrong or unproven:
1. **A's resolution does not reach the only observed class-(b) event.** N1 occurred at task-file gate items 7.G2-7.G7 of a task-builder-built task, at a non-standard lens (security-invariants). A's item 7 switches only `/task` steps 3-4 and the step-8 pair, and A's item 8 puts "domain and skill-embedded lens spawn sites" out of the first change (A-R2:125-126). A's own N2 says no observed spawn used steps 3-4 with a standard lens. So the one gate edit in A's resolution reaches zero observed spawns and none of the observed failure. The agent definition and the oracle are still worth shipping; the claim that the switch "cures" N1 is not supported.
2. **Executor persistence alone turns N1 from a detected loss into a silent coverage gap.** In the real run the orchestrator noticed because the security-invariants report was missing (NB3). If the executor writes each returned text to the dispatched slot's path, a misdirected reviewer's design-correctness review lands at the security-invariants path, step 10's existence check passes, and the gate silently has no security-invariants coverage. A's A-003 fix (path keyed by slot plus sha256) gives uniqueness and fidelity but not identity. A lens-identity check (the report states its lens; a mismatch with the dispatched lens is a blocker) is needed.
3. **The step-8 verification pair executes.** 24 of 169 non-fix verifier transcripts ran pytest or `sed -i` on scratch copies (NB6). A's item 7 switches the verification pair to the read-only agent on the strength of arm 1a, which measures lens reviewers on seeded documents, not verifiers checking that fixes landed.
4. **N1's damage is overstated and its cause is partly the agent.** The first report was restored byte for byte from the first agent's transcript (00:17:41-44Z); the on-disk window was 00:12:07Z to 00:17:44Z. A says "two blocking findings were lost" (A-R2:34); the record shows 3 blocking replaced by 1, and whether the stray's one blocking finding (deadline exit code, `origin_mismatch` instead of `budget_exhausted`) is the same defect as the first report's C-3 ("wrong exit code and reason under a specified con...") I could not settle. The cause: the dispatch named "Step 7.G7 (task file lines 546-547)"; the agent printed lines 540-550, which hold items 7.G5, 7.G6 and 7.G7, and took the first paragraph (NB1). Both the delegation-by-line-reference prompt and the agent's misreading contributed; the damage mechanism (Write plus a shared folder) is as A says.
5. **A's deterministic no-model arm has nothing to exercise once no engine is wired.** A-R2:122 keeps "a deterministic no-model arm"; with no `resolve`/`merge`/`ledger` in the first change and executor persistence written in prose, the only code to test deterministically is the oracle's scoring script. The arm should be named as that.
6. **A's runtime write-probe "in a `tmp_path` repository" (A-R2:121) cannot be a pytest.** A pytest cannot spawn a Claude Code subagent; the probe is a recorded one-time run with its transcript kept, and the static guard is the regression test.

#### New evidence

NB1. **Cause of N1: delegation by line reference into a window holding three lens prompts** [RUN-VERIFIED]. `T331/subagents/agent-abed84d24b847251c.jsonl`: first prompt "fix_authorization: false (report-only). Your complete instructions are the quoted prompt inside the item under "**Step 7.G7:**" (task file lines 546-547) ... Modify no file except your report." First tool call (00:00:02Z) `sed -n '540,550p'` of the task file; its result contains `**Step 7.G5:**` (lens "design-correctness", "Write the report to `.../qa/gate-c/qa-content-design-correctness-report.md`"), `**Step 7.G6:**` (test-adequacy) and `**Step 7.G7:**` (security-invariants). The agent's final message reports the design-correctness path, "FAIL, blocking: 1".

NB2. **N1 is outside every spawn site A's resolution changes** [RUN-VERIFIED for the site; CODE-VERIFIED for the rule]. The spawning items are task-file checklist items (Gate C, "lens agent 4/5/6 (part of the parallel batch of Step 7.G2)"), i.e. gate items written by the skill that built the task. `/task` step 5 spawns such prompts "exactly as written" (`src/superclaude/skills/task/SKILL.md:250`) and step 6 says "Each step below becomes its own `- [ ]` checklist item when encoded in a task file" (`task/SKILL.md:252`) [CODE-VERIFIED]. The orchestrator's actual cure was at the dispatch prompt: the re-spawn (`agent-ad808ee6d7eb36624.jsonl`, 00:17:48Z) names the lens, says "do NOT rely on line numbers", names "Your ONLY output file" and lists the files it must never write.

NB3. **How N1 was detected** [RUN-VERIFIED]. The main session waited for `-s $Q/qa-content-security-invariants-report.md` (00:12:46Z), found 5 files instead of 6 (00:17:16Z), listed `qa/gate-c` with timestamps (00:17:22Z), then copied the stray to `-run2.md`, restored the original (00:17:41-44Z) and re-spawned the lens. Detection relied on the missing file, which executor persistence keyed by slot would not leave missing (consequence is inference).

NB4. **Content restored; damage window about 5.6 minutes** [RUN-VERIFIED]. First report written 00:07:51Z (`agent-a00026ccf75eb50ac.jsonl`, final "FAIL, 3 blocking findings (C-1 to C-3), 9 minor notes"); overwritten 00:12:07Z; restored 00:17:44Z ("restored 15855", 96 lines, verdict FAIL with C-1..C-3). The overwritten path was in the worktree and untracked at the time (`?? .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-c/` in the agent's own `git status` at 00:12:55Z).

NB5. **The misdirected lens is an executing lens** [RUN-VERIFIED]. Between 00:06:36Z and 00:10:05Z the same agent wrote and ran `/tmp/gatec-probe/probe1.py` .. `probe7.py` against the package code and removed them at 00:12:55Z (`rm -rf /tmp/gatec-probe /tmp/gatec-*`). A read-only switch at that spawn site would remove the capability the lens used, so N1's site cannot be cured by the read-only agent without the capability question of A-004.

NB6. **Verifiers execute about as often as non-standard lenses** [RUN-VERIFIED, coarse regex]. Non-fix rf-qa / rf-qa-qualitative transcripts whose description contains "verif": 169, of which 24 ran pytest or `sed -i`/`perl -pi`; all other non-fix: 402, of which 58 did. Standard-lens-named subset: 107, of which about 3 did.

NB7. **Every `sed -i` by a non-fix agent targeted a scratch or variable path** [RUN-VERIFIED screen]. 28 agents; targets such as `$W/m/src/...`, `$M/m2/$S`, `$D/m2/src/...`, `$d/tree/tests/...`, `"$(C M2)"`, `$F`. Executing lenses include non-domain-named skill lenses (sc:sweep QA: command-contract, skill-contract, primitive-path, read-only-claims) and verifiers, not only test-adequacy and security-invariants. Variables were not resolved; classification is by pattern.

NB8. **The cap rows for `task/SKILL.md` do not touch steps 3, 4, 8 or 10** [CODE-VERIFIED]. Rows C-105..C-113 (`tests/skills/fixtures/review_severity_cap_edits.yaml:871-943`) pin cap and at-cap sentences (fixture lines 120, 254, 336, 366, 368, 405, 477, 616 of an older revision; C-107's text is now at `task/SKILL.md:258`). The spawn text of steps 3-4 (`task/SKILL.md:225, 241`), step 8 (`:256`) and step 10 (`:260`) carries no cap row, so a conditional edit of those steps meets only the "no minimum count" pin (`:233`) and the worker-contract paragraph.

#### Verification of N1-N3

Method: four read-only scripts over `/home/coder/.claude/projects/**/subagents/*.meta.json` and the sibling `.jsonl` files, plus the issue-331 main session `.jsonl`; tool calls deduplicated by `tool_use` id; results matched by `tool_use_id`; forbidden transcripts skipped before parsing; scratch in `mktemp -d /tmp/advB-r2.XXXXXXXX`, removed on exit.

**N1: VERIFIED, with corrections.**

| Question | Finding |
|---|---|
| Did the overwrite happen? | Yes. `agent-a00026ccf75eb50ac` (rf-qa-qualitative, "Gate C lens design-correctness") created `qa/gate-c/qa-content-design-correctness-report.md` at 00:07:51Z ("File created successfully"). `agent-abed84d24b847251c` (rf-qa-qualitative, "Gate C lens security-invariants", prompt "Modify no file except your report") ran Write on that path at 00:12:07Z (result "The file ... has been updated") and four successful Edits to 00:12:51Z. It never Read the file before the Write. Across the whole corpus, this is the only path written successfully by two distinct non-fix agents [RUN-VERIFIED]. |
| Was content lost? | Temporarily, on disk only. The first report (3 blocking, C-1..C-3) was replaced by a report with 1 blocking for about 5.6 minutes and restored byte for byte from the first agent's transcript by the orchestrator (00:17:41-44Z); the stray was kept as `-run2.md`; the security-invariants lens was re-run (`agent-ad808ee6d7eb36624`, PASS with notes, 0 blocking). Without the manual restore the gate would have consolidated 1 blocking finding in place of 3. "Two lost" (A-R2:34) assumes the stray's single finding duplicates one of the three; I could not confirm that. |
| Cause | Partly the dispatch (instructions by line reference, "lines 546-547"), partly the agent (it printed lines 540-550 holding three lens prompts and followed the first). The damage mechanism is Write access plus self-persistence into a shared `qa/gate-c/` folder. |
| Does it fall in B's class (b)? | Yes. Class (b) is "any repository working-tree path other than the own report" (B-R1:70). The path is inside the worktree (untracked at the time, NB4) and is another lens's report. B-3 as stated is refuted, and B's pre-commitment (B:84, B:105) moves "an agent-definition split only, without the panel" into the first change. |
| Spawn site | Task-file gate items written by task-builder (NB2), not `/task` steps 3-4. |

**N2: VERIFIED.** First prompts that contain `qa-(structural|content)-` followed by a standard lens name: 0 [RUN-VERIFIED]. Standard-lens-named descriptions: 107 by my regex (A: 118; regex difference).

**N3: VERIFIED in shape.**

| Measure | A (A-R2:53) | B re-check |
|---|---|---|
| Non-fix transcripts | 571 | 571 |
| With any Bash | 437 | 437 |
| pytest | 74 | 77 |
| `sed -i` / `perl -pi` | 28 | 28 |
| Write/Edit under `/tmp` | 15 | 15 |
| Standard-lens-named: n / Bash / pytest / `sed -i` / `/tmp` writes | 118 / 86 / 1 / 1 / n.a. | 107 / 79 / 2 / 1 / 0 |

Not re-checked: A's "simple reads only" sub-counts (50 and 18).

#### Final position table

| ID | Final | Evidence (one sentence) |
|---|---|---|
| S-001 | HYBRID (same as A-R2): consistency check against C-01/C-02/C-03 first (A's order) plus a separate "what was not verified" section (B) | Neither order changes a claim; the separate list keeps unverified items findable. |
| S-002 | B | The separate falsifiers of B-1..B-3 are what let this round keep B-1/B-2's "no engine swap" while refuting B-3 alone. |
| S-003 | HYBRID (same as A-R2): B's clause-keyed evidence with A's claim/evidence/tag table inside each clause | The table is auditable line by line; clause keying ties each item to a decision. |
| S-004 | B | The synth-06 ids INV-A..INV-N are the ids the C-11 row uses (`undecidable-conflicts.md:28`). |
| S-005 | HYBRID (same as A-R2): A's ordered pipeline with each step labelled with the clause it decides | Both advocates proposed this merge in Round 1. |
| C-001 | HYBRID (same as A-R2): the first change is lens-level (one read-only lens agent definition plus a single-document seeded replay), wires no panel engine into any rf-qa gate, and its only gate edit is the conditional standard-lens switch at `/task` steps 3-4 | N1 refutes "no hardening" while N2 and the one-candidate merge (`ledger.py:107`) rule out a `/task` engine start. |
| C-002 | HYBRID, differs from A-R2: the standard eight lens dimensions at `/task` steps 3-4 switch to the read-only agent only if arm 1a passes and the owner answers Q3 yes, with executor persistence that checks the report's lens line against the dispatched lens; the step-8 verification pair, non-standard lenses and skill or task-file gate items keep their agent | N1 fires class (b), but 24 of 169 verifiers and the N1 lens itself executed code (NB5, NB6), and persistence without an identity check would hide N1's failure (NB3). |
| C-003 | B | The lens travels as free text in the brief (`reflect-reviewer.md:56`); A withdrew the slot key (A-R2:91). |
| C-004 | B | The computed confidence gate stays in the agent body (`rf-qa.md:484-534`); A withdrew the completion predicate (A-R2:92). |
| C-005 | HYBRID, amends A-R2: seeded single documents with clean twins run through arm 0 and arm 1a per standard lens dimension with A's tree-hash, UNVERIFIABLE-share and pre-registered repeat count; the deterministic no-model arm is a pytest of the oracle's scoring script on frozen reports; a verification-pair arm is added only if the pair is to switch | No engine is wired, so the scorer is the only deterministic code (Updated assessment, point 5). |
| C-006 | HYBRID, amends A-R2: Half 1 is separable from Half 2 and limited to the standard eight lenses at steps 3-4; the step-8 pair is excluded unless its own arm passes; Half 2 is not in the first change | X-003 and N3 split Half 1; NB6 shows verifiers execute. |
| C-007 | HYBRID (same as A-R2): no engine swap at any gate in the first change; the only gate edit is the conditional standard-lens switch, guarded by arm 1a and the unedited pinned suites | The gate is mandatory after every phase (`task/SKILL.md:192, 286`). |
| C-008 | HYBRID, differs from A-R2: `task/SKILL.md` stays byte-identical unless the standard-lens switch lands; then only steps 3, 4 and 10 change (step 8 only with a passed verification arm) and the three pinned suites pass with no test edited | NB8: no cap row sits in steps 3, 4, 8 or 10, so the pins that matter are "no minimum count" (`:233`) and the worker-contract paragraph. |
| C-009 | HYBRID (same as A-R2): any later `/task` Half 2 is limited to document outputs, and M-B4 runs before it is widened | Both rest on the one-candidate merge (`merge_cmd.py` `--doc`, `ledger.py:107`). |
| C-010 | HYBRID, amends A-R2: full M-B1 audit before merge, deduplicated, counted per spawn source, with "another agent's report" and "a report whose lens differs from its dispatch" in class (b), an empty corpus giving no verdict, and N1 recorded with its cause; the tree-hash check on every replay | N1 was found by the audit and is invisible to a reviewed-tree hash; NB1 shows the cause must be recorded to choose the cure. |
| C-011 | B | No panel at any gate in the first change, so the prose floors (`task/SKILL.md:196-201`) stay and C-03 INV-003 is not forced. |
| C-012 | HYBRID (same as A-R2): the first change gives PR review the read-only reviewer definition and the replay fixture; per-slot lens and checklist mode wait | M4 and M9 left the first change with C-003 and C-004. |
| X-001 | B | `task/SKILL.md:250` spawns embedded lenses "exactly as written"; N2 and NB2 show lens traffic and the one failure at skill and task-file items. |
| X-002 | A | `_SLOT_KEYS` (`panel.py:46`) is an accept-list and `template_sha256` hashes the template object. |
| X-003 | B | Half 1 rewrites persistence and step 10 (`task/SKILL.md:238, 260`), with no panel code. |
| X-004 | B | The spawn `mode` is ignored; the allowlist is the control (N5). |
| X-005 | HYBRID (same as A-R2): B's statement holds for the whole gate, A's for Half 2 limited to document outputs | Both rest on the one-document merge. |
| X-006 | A | A's confidence is per reviewer (`rf-qa.md:505`); conceded in B-R1:68. |
| X-007 | B | 8 packaged templates (default, live7, six reflect). |
| A-001 | HYBRID, amends A-R2: rely on the `tools` allowlist, not `permissionMode`; record one runtime write-probe run (transcript kept in the task package, not a pytest) and keep the tree-hash check on every replay | A pytest cannot spawn a subagent; N5 shows refusals in practice. |
| A-002 | HYBRID, amends A-R2: the guard asserts the allowlist is a subset of a named read-only set, with Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit and NotebookEdit as mutators | `rf-qa.md:20-24` grants the task and message tools; `_MUTATORS` (`test_reviewer_readonly_tools.py:30`) omits Agent and SendMessage. |
| A-003 | HYBRID, amends A-R2: the executor persists each returned report unedited to the dispatched slot's path, records its sha256, and rejects as a blocker a report whose first line names a lens other than the dispatched one | Slot-keyed paths stop N1's overwrite but, without an identity check, hide N1's mis-dispatch (NB3). |
| A-004 | HYBRID, amends A-R2: the new agent's body is rf-qa's verification, zero-trust and Confidence Gate sections without the fix sections, standard lenses get pre-computed counts where they used Bash, and every lens or verifier that runs tests or mutates scratch copies is excluded from the switch | N3, NB5, NB6, NB7. |
| A-005 | HYBRID (same as A-R2): pre-register a repeat count per arm and a variance bound before the first model run | Neither variant states one. |
| A-006 | A | `_assert_present` (`test_cli_install.py:502-506`) fails only on a missing listed name. |

Tally: A 3 (X-002, X-006, A-006); B 9 (S-002, S-004, C-003, C-004, C-011, X-001, X-003, X-004, X-007); HYBRID 18 (S-001, S-003, S-005, C-001, C-002, C-005, C-006, C-007, C-008, C-009, C-010, C-012, X-005, A-001, A-002, A-003, A-004, A-005); NEITHER 0. Total 30. The outcome labels match A-R2 on all 30 points; the hybrid text differs on C-002, C-005, C-006, C-008, C-010, A-001, A-002, A-003 and A-004.

#### Response to A's proposed resolution

1. **ACCEPT.** Lens-level first change, no engine; B's document gate and A's Half 2 are later steps.
2. **AMEND.** Replace with: "The new agent's `tools` list is exactly Read, Grep, Glob and the read-only search and codegraph tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections; any S1-S3 severity or cap text it restates is copied verbatim (`test_c_s1_s3_copied_verbatim`); its report's first line states the dispatched lens and report slot; it names other primitives by installed path; `make sync-dev` and `make verify-sync` run." Reason: the verbatim pin applies to any new primitive that restates the rule (B:71), and the lens line is what the A-003 identity check reads.
3. **AMEND.** Replace with: "A new guard test asserts the agent's allowlist is a subset of a named read-only set (Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit, NotebookEdit are mutators), with a negative fixture; one runtime write-probe run (a Write attempt in a scratch repository) is recorded once with its transcript kept in the task package; it is not part of `uv run pytest`." Reason: A pytest cannot spawn a Claude Code subagent; TaskOutput and TaskStop are on `rf-qa.md:22-23`.
4. **AMEND.** Replace "with a deterministic no-model arm" by "with a deterministic pytest of the oracle's scoring script on frozen reports (a seeded defect matched in a blocking row; no blocker on a clean twin)", and add: "a verification-pair arm (fixed document, applied fix, the pair asked to confirm it) runs only if item 7 is to switch step 8." Reason: no engine code exists to replay; verifiers execute (NB6).
5. **AMEND.** Replace with: "The full M-B1 audit runs before merge, deduplicated by `tool_use` id, skipping run-1 transcripts, and counted per spawn source (`/task` steps 3-4, task-file gate items, skill gates); own report or `/tmp` scratch = neutral; another agent's report, a report whose lens differs from its dispatched lens, or any other repository working-tree path = class (b); a git state change in the reviewed repository = class (c); a class-(b) or class-(c) event refutes leaving the agents as they are; an empty or unreadable corpus gives no verdict. The issue-331 Gate C overwrite is recorded as the first class-(b) event with its cause (dispatch by line reference into a window holding three lens prompts)." Reason: NB1, NB2, and A-R1:37's valid point that absence must not read as safety.
6. **AMEND.** Append: "The owner is also told that the only class-(b) event occurred at a task-file gate item of a non-standard lens that item 7 does not reach, and that no standard-lens spawn through `/task` steps 3-4 was observed." Reason: NB2 and N2; the owner's answer should rest on where the exposure was seen.
7. **AMEND.** Replace with: "If arm 1a meets the registered rule for a standard lens dimension before merge and the owner says yes, the first change switches that dimension at `/task` steps 3-4 to the new agent, persists each returned report unedited to the dispatched slot's path with its sha256, treats a report whose first line names another lens as a blocker, and rewrites step 10 to check the executor-persisted files, their hashes and their lens lines; the step-8 verification pair switches only if the verification-pair arm of item 4 passes; otherwise `task/SKILL.md` stays byte-identical." Reason: NB3 (identity), NB6 (verifiers execute).
8. **ACCEPT**, with the wording "skill-embedded and task-file gate items" in place of "domain and skill-embedded lens spawn sites", so the exclusion names where N1 occurred.
9. **ACCEPT.** The scope check and the unedited suites are B's M-B3.
10. **AMEND.** Replace with: "Open condition, executing reviewers: every lens or verifier that runs tests or mutates scratch copies keeps its agent until a read-only path (pre-computed evidence, or an isolated execution snapshot, suitability [UNVERIFIED]) is measured against arm 0; skill-embedded and task-file gate items, where N1 occurred, get in a separate change a no-clobber check (sha256 of each lens report recorded when its owner returns and re-checked at consolidation; a mismatch is a blocker) and dispatch prompts that name the lens and report path explicitly instead of by line reference." Reason: NB5-NB7 widen "domain lenses"; the no-clobber check and explicit dispatch cure N1's mechanism at its own site without removing capability, as the orchestrator's re-spawn did (NB2).
11. **ACCEPT.**
12. **ACCEPT.**

#### Proposed resolution

1. The first rf-qa change is lens-level: one new read-only lens-reviewer agent definition and a replay oracle; no panel engine (`resolve`/`merge`/`ledger`) is wired into any rf-qa gate; B's document-gate module and A's `/task` Half 2 are later steps.
2. The agent's `tools` list is exactly Read, Grep, Glob and the read-only search and codegraph tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections, copies any S1-S3 severity or cap text verbatim, and makes the report's first line state the dispatched lens and slot; it names primitives by installed path; `make sync-dev` and `make verify-sync` run.
3. A guard test asserts the allowlist is a subset of a named read-only set (Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit, NotebookEdit are mutators) with a negative fixture; one runtime write-probe run is recorded once with its transcript kept in the task package.
4. Before any gate text changes, the oracle runs seeded single documents with clean twins through arm 0 (current lens agents) and arm 1a (new agent, same lens text, prose consolidation) per standard lens dimension, with a pytest of the scoring script on frozen reports, a pre-registered repeat count, variance bound and decision rule, and metrics: per-lens recall in a blocking row, wrong blockers on clean twins, UNVERIFIABLE share, tree-hash no-mutation, tokens, wall-clock; a verification-pair arm runs only if step 8 is to switch.
5. The full M-B1 audit runs before merge (deduplicated by `tool_use` id, run-1 transcripts skipped, counted per spawn source); own report or `/tmp` scratch is neutral; another agent's report, a report whose lens differs from its dispatch, or any other working-tree path is class (b); a git state change is class (c); (b) or (c) refutes leaving the agents unchanged; an empty corpus gives no verdict; the issue-331 Gate C overwrite is recorded as the first class-(b) event with its cause.
6. Owner question Q3 goes to the owner with items 4-5's evidence, including that the only class-(b) event was at a task-file gate item of a non-standard lens and that no standard-lens spawn through `/task` steps 3-4 was observed; the recommendation is yes for the standard eight lens dimensions.
7. If arm 1a passes for a standard dimension and the owner says yes, `/task` steps 3-4 switch that dimension to the new agent; the executor writes each returned report unedited to the dispatched slot's path with its sha256, a report naming another lens is a blocker, and step 10 checks files, hashes and lens lines; step 8 switches only if the verification-pair arm passes; otherwise `task/SKILL.md` stays byte-identical.
8. Out of the first change: per-slot `lens` key, checklist completion predicate, any `/task` panel template, floor parameter, skill-embedded and task-file gate items, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, the ten S1-S3 files, `pr_submit`, `cli/reflect`.
9. Scope check: `git diff --stat` names only the new agent file, its tests, the oracle script and tests, and (only under item 7) `task/SKILL.md`; `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_worker_contract.py tests/review -q` passes with no test edited.
10. Open, executing reviewers: lenses and verifiers that run tests or mutate scratch copies keep their agent until a read-only path is measured against arm 0; skill-embedded and task-file gates get, in a separate change, a no-clobber check (each report's sha256 recorded when its owner returns and re-checked at consolidation; a mismatch is a blocker) and dispatch prompts that name lens and report path explicitly, not by line reference.
11. Open, engine: any gate engine swap waits for the M-B4 anchor probe (C-01 T-a), the C-03 floor-owner answer and C-02's `next`/`--resolution` caller rules, and runs in shadow with rf-qa as authority until a replay says otherwise.
12. Open, evidence quality: the transcript audit covers one machine and unknown retention, the N1 damage count (2 or 3 blocking findings) is unsettled, and the "eight lens" set meant by Q5 stays an owner decision.


## Round 2.5: Invariant Probe (summary; full table in `invariant-probe.md`)

Independent fault-finder, 18 findings: 2 ADDRESSED (INV-005, INV-011), 16 UNADDRESSED. UNADDRESSED by severity: HIGH 6 (INV-002 lens-identity check undefined for a first line that names no lens; INV-009 executor persistence path is not unique for partition instances; INV-012 the hash and lens checks sit in step 10, after consolidation, fix and the proceed decision; INV-015 the sha256 is taken over the executor's own write, not the returned text; INV-016 arm 0 and arm 1a differ in more than the tool list; INV-017 pre-computed counts exist in the oracle but not at a production gate), MEDIUM 9, LOW 1 (INV-006). The invariant-probe gate therefore blocks convergence (BLOCKED_BY_INVARIANTS). The fault-finder's own remark on the three open wording disputes: INV-018 supports B's "own arm" condition for the step-8 pair; INV-005 and INV-008 support B's wider exclusion scope; INV-001 and INV-004 show a single runtime probe in any form covers one harness only.

## Per-Point Tracking

Labels: A = Variant A wins, B = Variant B wins, H = hybrid, N = neither. R1/R2 columns give the Advocate-A label then the Advocate-B label. "Text" = the two final hybrid texts do not contradict each other (Y) or do (N).

| Point | Level | R1 A / B | R2 A / B | Label agreed | Text agreed | Outcome |
|-------|-------|----------|----------|--------------|-------------|---------|
| S-001 | L1 | N / H | H / H | Y | Y | Hybrid |
| S-002 | L2 | B / B | B / B | Y | Y | B |
| S-003 | L2 | N / H | H / H | Y | Y | Hybrid |
| S-004 | L1 | B / B | B / B | Y | Y | B |
| S-005 | L2 | H / H | H / H | Y | Y | Hybrid |
| C-001 | L2 | A / B | H / H | Y | Y | Hybrid |
| C-002 | L3 | A / B | H / H | Y | N | Hybrid (wording split) |
| C-003 | L2 | H / B | B / B | Y | Y | B |
| C-004 | L3 | H / B | B / B | Y | Y | B |
| C-005 | L2 | H / H | H / H | Y | Y | Hybrid |
| C-006 | L3 | A / H | H / H | Y | N | Hybrid (wording split) |
| C-007 | L2 | H / B | H / H | Y | Y | Hybrid |
| C-008 | L3 | A / B | H / H | Y | N | Hybrid (wording split) |
| C-009 | L2 | A / H | H / H | Y | Y | Hybrid |
| C-010 | L3 | H / B | H / H | Y | Y | Hybrid |
| C-011 | L3 | H / B | B / B | Y | Y | B |
| C-012 | L2 | A / A | H / H | Y | Y | Hybrid |
| X-001 | L2 | B / B | B / B | Y | Y | B |
| X-002 | L3 | A / A | A / A | Y | Y | A |
| X-003 | L3 | B / B | B / B | Y | Y | B |
| X-004 | L3 | B / B | B / B | Y | Y | B |
| X-005 | L2 | H / H | H / H | Y | Y | Hybrid |
| X-006 | L3 | A / A | A / A | Y | Y | A |
| X-007 | L1 | B / B | B / B | Y | Y | B |
| A-001 | L3 | H / H | H / H | Y | N | Hybrid (wording split) |
| A-002 | L3 | H / H | H / H | Y | Y | Hybrid |
| A-003 | L3 | H / H | H / H | Y | Y | Hybrid |
| A-004 | L2 | H / H | H / H | Y | N | Hybrid (wording split) |
| A-005 | L2 | N / H | H / H | Y | Y | Hybrid |
| A-006 | L2 | N / A | A / A | Y | Y | A |

Tally of outcomes: B 9, A 3, Hybrid 18 (13 with agreed text, 5 with split wording), Neither 0. A-007 and A-008 (STATED) were accepted by both advocates and are not counted.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Hybrid (A's order: consistency check first, plus B's separate "not verified" list) | 85% | Both Round 2 tables state the same hybrid; no claim depends on it. |
| S-002 | Variant B | 93% | B's clauses B-1..B-3 each had a falsifier; Advocate A conceded in Round 1 and Round 2. |
| S-003 | Hybrid (B's clause-keyed evidence with A's claim/evidence/tag table) | 85% | Same hybrid in both Round 2 tables. |
| S-004 | Variant B | 90% | Synth-06 invariant ids are the ids the C-11 row uses; A conceded. |
| S-005 | Hybrid (A's ordered pipeline, each step labelled with the clause it decides) | 92% | Proposed in Round 1 by both advocates and restated in Round 2. |
| C-001 | Hybrid (lens-level first change; no panel engine wired; only gate edit is the conditional standard-lens switch at /task steps 3-4) | 88% | Same text in both Round 2 tables; rests on N1 (a write-capable lens overwrote another lens's report), N2 (no step-3/4 spawn with a standard lens name observed) and the one-candidate merge (`ledger.py:107`). |
| C-002 | Hybrid (conditional standard-lens switch; domain, skill-embedded and task-file lenses keep their agent) | 70% | Label agreed; step-8 verification pair (A: switches with arm 1a; B: only with its own arm) and the identity check are unresolved wording. |
| C-003 | Variant B | 95% | Advocate A withdrew the per-slot `lens` key (conceded); the lens travels as free text. |
| C-004 | Variant B | 95% | Advocate A withdrew the checklist completion predicate (conceded). |
| C-005 | Hybrid (seeded single documents with clean twins through arm 0 and arm 1a; deterministic arm is a pytest of the scoring script) | 80% | Label agreed; B's amendment (no engine code exists to replay) not answered by A, additive. |
| C-006 | Hybrid (Half 1 separable from Half 2, limited to the standard eight lenses; Half 2 out of the first change) | 70% | Label agreed; the step-8 pair is again split. |
| C-007 | Hybrid (no engine swap at any gate; one conditional agent switch guarded by arm 1a and unedited pinned suites) | 90% | Same text in both Round 2 tables; `task/SKILL.md:192, 286` (gate runs after every phase). |
| C-008 | Hybrid (`task/SKILL.md` byte-identical unless the switch lands) | 70% | Label agreed; edited steps are 3, 4, 8, 10 (A) versus 3, 4, 10 with step 8 only after its own arm (B). |
| C-009 | Hybrid (any later /task Half 2 limited to document outputs; M-B4 anchor probe first) | 92% | Same text; both rest on `merge_cmd.py --doc` and `ledger.py:107`. |
| C-010 | Hybrid (full M-B1 audit with write classes, deduplicated, empty corpus gives no verdict; tree-hash on every replay) | 80% | Label agreed; B's additions (lens-mismatch as class (b), per spawn source) are additive. |
| C-011 | Variant B | 95% | With no panel at any gate the prose floors stay; A conceded. |
| C-012 | Hybrid (first change gives PR review the read-only reviewer and the replay fixture; per-slot lens and checklist mode wait) | 90% | Same text in both Round 2 tables. |
| X-001 | Variant B | 95% | Code check: 93 `fix_authorization: false` markers in 8 skill files; `task/SKILL.md:250` spawns embedded lenses as written; A conceded in Round 1 and Round 2. |
| X-002 | Variant A | 95% | `_SLOT_KEYS` is an accept-list and `template_sha256` hashes the template object; B conceded. |
| X-003 | Variant B | 95% | Half 1 rewrites persistence and step 10 (`task/SKILL.md:238, 260`); A conceded. |
| X-004 | Variant B | 92% | Spawn `mode` is ignored; the tools allowlist is the control; A conceded. |
| X-005 | Hybrid (B's statement for the whole gate, A's for Half 2 limited to document outputs) | 90% | Same text in both Round 2 tables. |
| X-006 | Variant A | 95% | Confidence is per reviewer (`rf-qa.md:505`); B conceded. |
| X-007 | Variant B | 95% | 8 packaged templates (default, live7, six reflect); A:115 lists 9; A conceded. |
| A-001 | Hybrid (rely on the tools allowlist, not permissionMode; one runtime write-probe; tree-hash on every replay) | 72% | Label agreed; probe form unresolved (A: test in a tmp_path repository; B: recorded one-time run, a pytest cannot spawn a subagent). |
| A-002 | Hybrid (guard asserts a subset of a named read-only set; spawn and message tools are mutators) | 82% | Same intent; B's list is a superset (TaskOutput, TaskStop, MultiEdit); `_MUTATORS` at `test_reviewer_readonly_tools.py:30` omits Agent. |
| A-003 | Hybrid (executor persists unedited to the dispatched path with sha256; B adds a lens-identity blocker) | 78% | Additive; the fault-finder rates the identity check and the hash mechanism HIGH UNADDRESSED (INV-002, INV-015). |
| A-004 | Hybrid (agent body = rf-qa verification and Confidence Gate sections without fix sections; executing lenses excluded) | 70% | Label agreed; exclusion scope differs (domain lenses versus every lens or verifier that executes). |
| A-005 | Hybrid (pre-register a repeat count and variance bound per arm) | 92% | Same text in both Round 2 tables. |
| A-006 | Variant A | 95% | `_assert_present` fails only on a missing listed name (`test_cli_install.py:502-506`); both advocates agree. |

## Convergence Assessment
- Points resolved: 25 of 30 (agreed at text level); 30 of 30 on outcome label
- Alignment: 83.3% (text level); 100% (label)
- Threshold: 80%
- Diff-point gate: met (83.3% >= 80%)
- Taxonomy gate: met (L1, L2, L3 all covered)
- Invariant-probe gate: NOT met; 6 HIGH UNADDRESSED invariants (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017)
- Status: BLOCKED_BY_INVARIANTS (agreement at or above threshold and taxonomy covered, but HIGH-severity UNADDRESSED invariants exist). At depth standard there is no Round 3; per FR-006 the debate force-selects by score and flags the non-convergence for user review.
- Unresolved points: C-002, C-006, C-008, A-001, A-004 (hybrid wording splits). Cluster 1 (C-002, C-006, C-008, A-004): does the step-8 verification pair switch together with the standard lenses, and is the exclusion scope "domain lenses" (A) or "every lens or verifier that runs tests or mutates scratch copies" (B). Cluster 2 (A-001): runtime write-probe as a test (A) or a recorded run (B).
- Oscillation: none (no point flipped winner between Round 2 positions; Round 1 to Round 2 movement was toward hybrids on both sides).
