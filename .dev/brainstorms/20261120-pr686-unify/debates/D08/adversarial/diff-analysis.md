# Diff Analysis: Position-paper Comparison (D08 naming and identity of the primitive)

## Metadata
- Generated: 2026-11-20 (Step 1, Mode A compare, depth standard)
- Variants compared: 2
  - Variant 1 (OURS, owner's line, one word "coordinator"): /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/adversarial/variant-1-original.md
  - Variant 2 (CLAY, "orchestrator" and /sc:orchestrator): /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D08/adversarial/variant-2-original.md
- Verification base: read-only snapshots under /home/coder/.cache/ic-snap-20261120/ (master, pr-a, pr-p), the ZS-REQ file, and `orca skills get orchestration`. Items marked UNVERIFIED could not be checked without GitHub access or without the primary file.
- Total differences found: 45 (plus 10 promoted [SHARED-ASSUMPTION] diff points, 55 in all)
- Categories: structural (6), content (14), contradictions (11), unique (14)
- Shared assumptions: 15 (A-001 to A-015): STATED 4, UNSTATED 10 (promoted as SA-001 to SA-010), CONTRADICTED 1

## Structural Differences

| # | Area | Variant 1 (OURS, coordinator) | Variant 2 (CLAY, orchestrator) | Severity |
|---|------|-------------------------------|--------------------------------|----------|
| S-001 | Heading skeleton | Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right | Same six headings in the same order | Low |
| S-002 | Cited-fact count and order | 9 facts. Opens with the owner decision (R10, 2026-11-18), then installed contract, routing guide, platform, 63-file collision, Clay's own spec lineage | 8 facts. Opens with the merged design (D:65, D:133), then vocabulary counts, owner tracker, R10 scope, then Clay's deployed `coordinator` tag | Medium (the order encodes which authority each side ranks first: owner ruling vs merged design text) |
| S-003 | Placement of the R10-scope doubt | R10 is fact 1 (used as settled). The doubt that "everywhere" may be too wide sits last, in "What it risks", first bullet | The doubt is fact 4 inside the main evidence, stated as a reason R10 does not bind | Medium |
| S-004 | Nesting of 339, 423, 444 | Claim names the three issues. "What it gets right" points to "the nesting table in the verdict", but the variant has no such table (dangling reference) | Nesting is given as one sentence in Claim and again as fact 8. No table | Medium (neither variant gives a standalone, checkable nesting structure; V1's pointer is to a table that is not in the file) |
| S-005 | Evidence base | master snapshot, ZS-REQ file, design doc (D). Mentions pr-a and pr-p only inside fact 8 | master, pr-a (PR 686) and the design doc. ZS-REQ appears only inside fact 4 | Low |
| S-006 | Balance of costs and risks | Costs: rename, issue titles, report-session name. Risks: two bullets, both about the owner-ruling reading and authority hiding. No risk about the owner's reaction or the topology decision | Costs: two nouns, 63-file collision, contradiction with R10 and 516. Risks: owner reads it as a reversal, topology collapse makes the second noun overhead, GitHub text and master text diverge | Low |

## Content Differences

| # | Topic | Variant 1 (OURS, coordinator) | Variant 2 (CLAY, orchestrator) | Severity |
|---|-------|-------------------------------|--------------------------------|----------|
| C-001 | Session role noun | One genus noun "coordinator" for every session role, including Clay's per-repo issue-polling session ("a coordinator of a particular kind (script-woken, with grants)") | "Orchestrator" for the per-repo issue-polling session. "Coordinator" stays what the installed contract says: a session a person opened | High |
| C-002 | Command, skill and surface names | `/sc:coordinator` and `sc-coordinator-protocol`. Says the command does not exist yet, so nothing is renamed | `/sc:orchestrator`, `sc-orchestrator-protocol`, flags `--wake --hourly --resume --take`, verbs `superclaude orchestrator ...`, state folder `.orchestrator/`, tag `orchestrator-<short>-<n>` (OQ5, D:133) | High |
| C-003 | How the authority difference is carried | Qualifiers on one noun: "project coordinator" (`COORD-<RepoName>`), "sub-coordinator" (444 `--sub`), "report session". WORKER-CONTRACT section 4 gets a named case for the script-started coordinator | A second noun, plus a new contract section "Orchestrated issue flow" (ADD1) that defines the orchestrator as a separate party | High |
| C-004 | The daily report session | Renamed in prose to "report session" and "stops being called a coordinator". V1 itself lists the cost: the live tag and two automations are called `coordinator` (D:714) | Kept as `coordinator` (tag, automations `coordinator-morning-wake`, `coordinator-missed-check`, state `.dev/coordinator/`). Named as the "third thing" and kept apart | Medium |
| C-005 | Nesting of 339, 423, 444 | Titles stay "orchestrator". Glossary says "orchestrator in an issue title means the coordinator role or the program around it". 339 = the owner's epic for one session that manages all sessions. 444 `--sub` = sub-coordinator, evaluation only. 423 = knowledge layer | 339 = the general orchestrator for all sessions, a separate later job. This design = the issue-polling orchestrator. 444 `--sub` = sub-orchestrator. 423 = later knowledge layer for orchestrators. One family under one word | High |
| C-006 | What R10 (ZS-REQ line 41) covers | Treats "the term is 'coordinator', not 'orchestrator', everywhere" as an owner decision that reaches the command name; concedes it may only cover branch, worktree and session name, then falls back on facts 2 and 5 | Treats R10 as written in a row about the watcher's worktree and branch only, and as a paraphrase of an unread Coder issue (516). Adds that the owner never renamed 339, 423 or 444 afterwards | High |
| C-007 | Reading of Clay's own design lines (D:799, D:902) | Both lines show the design already treats "coordinator" as the genus ("this spec's coordinator", "standing-grant coordinator") | The same D:799 line shows a separate party that needs its own noun so no coordinator rule leaks in | Medium |
| C-008 | Size of the rename | Cheap. Nothing built carries the name. Persistent identifiers are few (six listed). PR 686 unmerged, design doc disposition open (D14) | Does not call it cheap or expensive in numbers, but counts 759 uses in the design and 1179 to 1816 uses in src and tests, a merged forward reference in master, and says "a rename leaves GitHub text and master text disagreeing" | High |
| C-009 | The 63 installed files that already use "orchestrator" for a parent session | Evidence for avoiding the word: a command named `/sc:orchestrator` puts both meanings in one sentence; the word choice removes a collision | Listed as a cost, but also as support: "the orchestrator is the session that runs a wave-based protocol and delegates the work" in this repository, so the new sense fits the old one | Medium |
| C-010 | Platform (Orca) vocabulary | Orca's `orchestration` skill classifies sessions as "Coordinator", "Dispatched worker", "Handoff owner": layer is "orchestration", role is "coordinator" | Orca's layer is "orchestration", so "orchestrator" is the natural "-or" agent noun for the session that drives it | Medium |
| C-011 | Status of issue 444 | Never approved the name: command "proposed", criterion 4 "without assuming that implementation has been approved", title says "Sub-Orchestrator or Coordinator mode". Design admits "how it joins is UNVERIFIED" | The owner's own tracker "proposed this very command first": body says "the proposed `/sc:orchestrator` command" | Medium |
| C-012 | Owner-conflict handling | Uses the owner decision as a main support and names no risk of the owner reading the merge as a reversal | States a "visible contradiction" with R10 and 516 and says the debate weighting rule is "decisive unless there is a separable benefit" | Medium |
| C-013 | Dependence on session topology (D07) | None stated. Asserts Clay's session is a coordinator "not a new kind of thing" whatever D07 decides | Conditional: "If the owner's coordinator and Clay's orchestrator end up as one session per repo (D07), the second noun names nothing and is pure overhead" | Medium |
| C-014 | Provenance of the name `/sc:orchestrator` | "Clay took the name while recording that the collision was unresolved" (U19); design 1.3 calls the join UNVERIFIED | "The merged design fixes the names ... its decisions are marked 'Decided' (D:1146 and following)" | High |

## Contradictions

Each row quotes both variants. "Check" gives what the snapshot or primary file shows.

| # | Point of Conflict | Variant 1 Position (quote) | Variant 2 Position (quote) | Check against snapshot | Impact |
|---|-------------------|----------------------------|----------------------------|------------------------|--------|
| X-001 | Whether the name `/sc:orchestrator` is a settled decision | "Clay took the name while recording that the collision was unresolved." and "the command does not exist yet, so nothing has to be renamed" | "The merged design fixes the names" and "its decisions are marked 'Decided' (D:1146 and following)" | Master design: D:65 says "how it joins is UNVERIFIED". The OQ5 row (D:133) has Owner column "no". D:1146 starts section 10 "Owner decisions" (OD1 to OD15) and none of its rows is about the command name (OD8 is the repo name). So OQ5 is Clay's own resolved open question, not an owner decision. V2's "Decided" refers to a table that does not contain the name. V2 is right that the design text fixes the file names. | High |
| X-002 | Reach of the owner rule R10 | "the term is 'coordinator', not 'orchestrator', everywhere" (fact 1; V1 later concedes in Risks that the owner "meant only the branch, worktree and session name" is possible) | "R10 sits in a row about the name of the watcher's worktree and branch" and its "everywhere" is "a requirements-file paraphrase of a Coder issue (516) whose text could not be read" | ZS-REQ line 41 (R10) confirms the quoted sentence exists as its own sentence inside a row about the worktree and branch name. Line 40 (R9) says that "Today the coordinator for IronClaude is the session ORCH-IronClaude", which neither variant mentions. Primary text of Coder 516 UNVERIFIED. Reach to the command name is unresolved. | High |
| X-003 | What the design line D:799 proves | "D:799 says 'The orchestrator is a standing-grant coordinator and not a worker (ADD1)'. So the design itself treats coordinator as the genus." | "resolves them by adding a section that defines 'the orchestrator' as a separate party (D:799: 'a standing-grant coordinator and not a worker')" | D:799 contains the quoted sentence verbatim. Both quote it correctly and draw opposite conclusions. D:902 (C4) also reads "The orchestrator, which is this spec's coordinator". The text supports "orchestrator is a kind of coordinator" in Clay's own words, which favours V1's reading but does not decide the command name. | Medium |
| X-004 | Size of the rename | "Nothing built carries the name yet, so the rename is cheap." | "PR 686 raises the word's count in `src` and `tests` from 1179 to 1816" and "a rename leaves GitHub text and master text disagreeing until the owner edits them" | Counts of "orchestrator" in src and tests: master 1179, pr-a 1816 (both reproduced exactly). Design file: 759 "orchestrator", 121 "coordinator" (reproduced). V2's file counts 237 to 279 not reproduced: I count 195 to 237 (case-insensitive) or 185 to 227 (case-sensitive); the delta of 42 matches, the base differs (UNVERIFIED scope). V1's "13 uses" of `orchestrator_tier`: I count 15 lines (10 src, 5 tests). | High |
| X-005 | Name of the daily report session | "report session for Clay's daily report session, which stops being called a coordinator" | "the report session ... tag `coordinator`" stays; "Calling the new per-repo session a coordinator too would put two different sessions under one tag family" | D:93, D:714 and D:122 confirm tag `coordinator`, two `coordinator-` automations, and "unchanged". D:1157 (OD6) records an owner ruling that the report session `coordinator` stays one session. So V1 proposes renaming something an owner-ruled design row keeps (ruling text itself UNVERIFIED, RULINGS.md not read). | Medium |
| X-006 | What one shared noun does to the installed rules | "One genus noun lets every installed rule that already says 'coordinator' apply or be narrowed by name, instead of two nouns that leave the rules silent about the second." | "Giving it the same noun would silently apply or silently contradict every coordinator rule. A second noun forces the contract to say what the second role may do" | WORKER-CONTRACT.md on master: "coordinator" on 80 lines (104 occurrences), "orchestrator" 0. Line 70: "These bind the coordinator: an Orca coordinator session the person opened." So the contract does define coordinator as person-opened; V1's genus needs section 4 edited, V2's needs a new section. Both agree on one contract edit (ADD1). | High |
| X-007 | Identity of the per-repo issue-polling session | "Clay's per-repo issue-polling session is a coordinator of a particular kind (script-woken, with grants), not a new kind of thing." | "Two roles with two authority models get two nouns." | R9 (ZS-REQ line 40) says the owner's coordinator "carries the issue-pipeline duties from a standard install", so the owner's coordinator may do the same job as Clay's orchestrator. Which of the two readings is right depends on D07 (topology), which V2 flags and V1 does not. | High |
| X-008 | Whether the 63-file "orchestrator" usage argues for or against the word | "It removes a collision with 63 installed files rather than adding to it." | "'Orchestration' (Orca's layer name ...) plus '-or' is the natural agent noun ... in this repository 'the orchestrator' is the session that runs a wave-based protocol and delegates the work." | 63 files verified (`grep -rli orchestrator` over commands, skills, agents, core). Line counts verified: reflect 23, troubleshoot 20, evidence-validator 18, qa.md:56 "The parent orchestrator". Both agree on the facts; V1 reads them as a collision, V2 as a precedent. | Medium |
| X-009 | What the Orca vocabulary implies | "'Orchestration' is the layer, 'coordinator' is the role." | "'Orchestration' ... plus '-or' is the natural agent noun for the session that drives it." | `orca skills get orchestration` shows a role table with "Coordinator" and "Handoff owner" rows (lines 38 and 40) and no "Orchestrator" role. Installed ~/.claude/skills/orchestration/SKILL.md has 0 hits for "orchestrator". V1's reading matches the platform text; V2's is an inference. | Medium |
| X-010 | Meaning of issue 444 for the command name | "Issue 444 never approved the name ... criterion 4 reads 'Consider `--sub` as a possible interface without assuming that implementation has been approved'" | "Issue 444 ... proposed this very command first ... its body says 'the proposed `/sc:orchestrator` command'" | Local copies of 444, 339 and 655 are absent (only .dev/issues/423 exists); both quotes UNVERIFIED. They are compatible quotes; the conflict is the inference (open proposal vs owner's own name). | Medium |
| X-011 | V2's own claim against V2's own fact | "'Coordinator' stays what it already is in the installed contract: a session a person opened." (V2 Claim and Mechanism) | Fact 3 quotes issue 339: "main session goes into orchestrator mode ... that session will be permanently flagged as the Orchestrator" | A person-opened main session is called "coordinator" by the contract and "Orchestrator" by 339, so V2's two-noun split puts the owner's own person-opened session in both families. V2 handles it by calling 339 a separate "general orchestrator" without saying how it differs from the coordinator. Quote of 339 UNVERIFIED (no local copy). | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Platform-vocabulary evidence: Orca's own `orchestration` skill names the supervising role "Coordinator" and the layer "orchestration" (verified through `orca skills get orchestration`) | High |
| U-002 | V1 | Clay's own spec lineage: design C4 (D:902) rewrites "agent-coordinator" as "The orchestrator, which is this spec's coordinator". The design describes the new session in terms of the old role name (verified) | High |
| U-003 | V1 | A qualifier scheme that answers the nesting question without new nouns: project coordinator, sub-coordinator, report session | High |
| U-004 | V1 | An inventory of persistent identifiers a rename would touch: `.orchestrator/` (3 files in src/tests), `orchestrators.json` (7 files), `orchestrator-wake` and `orchestrator-wake-ack` file names, `orchestrator_tier`, the tag `orchestrator-<short>-<n>`, and the repo `IronOrchestrator`. Partly verified: `IronOrchestrator` is in the design doc only (D:95, D:866), not in pr-a src or tests | High |
| U-005 | V1 | Owner alignment program wording (open-decisions.md lines 12 and 15, Q26 final.md line 6) defining "coordinator" and "#423 is a layer, not the role". The file was not found at the path under /home/coder/workspaces/IronClaude (UNVERIFIED) | Medium |
| U-006 | V1 | Quote of 444 criterion 4 ("without assuming that implementation has been approved") as evidence the name was never approved (UNVERIFIED, no local 444) | Medium |
| U-007 | V1 | Claim that issue 655's first paragraph itself says it replaces "the coordinator handoff" (UNVERIFIED, no local 655) | Medium |
| U-008 | V2 | Clay's deployed `coordinator` surface: tag `coordinator`, automations `coordinator-morning-wake` and `coordinator-missed-check`, state folder `.dev/coordinator/`, spec file name `SPEC-AGENT-WORK-COORDINATOR-20261027.md` (D:93, D:714, D:862, D:122 verified). This is a real tag-family collision for V1's genus | High |
| U-009 | V2 | The conditional on topology: if D07 makes the owner's coordinator and Clay's orchestrator one session per repo, the second noun is pure overhead | High |
| U-010 | V2 | An explicit statement that the choice contradicts R10 and Coder 516's `COORD-<RepoName>` and that the debate weighting rule makes that decisive without a separable benefit | Medium |
| U-011 | V2 | Other owner-tracker usage: issues 431 and 462 (closed) say "Orchestrator waits on quiet workers" and "Orchestrator-spawned sessions default to Opus" (UNVERIFIED, no local copies) | Low |
| U-012 | V2 | Notes that OQ5's own check (name free) holds "for file names" only, and records U19 (D:1277, verified) that the owner reconciles 444 later | Medium |
| U-013 | V2 | Lists the specific contract conflicts the design resolves (WORKER-CONTRACT lines 23, 244, 239 to 246) as the reason a separate section is needed. ADD1 (D:135) cites lines 23 and 244, verified; range 239 to 246 not re-read | Medium |
| U-014 | V2 | The "-or" derivation from Orca's layer name as the naming argument for "orchestrator" | Low |

## Shared Assumptions

### Agreement points found (where both variants converge)

- AP-1: Clay's per-repo issue-polling session has a different authority model from the person-opened coordinator in WORKER-CONTRACT (script-woken, standing grants). Both say WORKER-CONTRACT must name it (ADD1).
- AP-2: Nothing named `/sc:orchestrator` or `/sc:coordinator` exists yet as a command file (verified absent on master, pr-a, pr-p).
- AP-3: "Orchestrator" already means "parent session that fans out to subagents" in 63 installed files (verified).
- AP-4: The debate cannot edit issues 339, 423, 444 or 655 (no GitHub writes). A glossary line is the bridge.
- AP-5: R10 contains the words "coordinator, not orchestrator, everywhere", and Coder 516's primary text is unread.
- AP-6: How issue 444's `--sub` mode joins is open (design U19, D:1277).
- AP-7: The question is answered by choosing between the two nouns already on the table.

### Assumption table

| # | Precondition (what both variants rely on) | Behind agreement point | Class | Evidence | Impact |
|---|-------------------------------------------|------------------------|-------|----------|--------|
| A-001 | The command, skill, verbs, state folder and tags must all carry the same word as the role. The topic asks for "one name for the session role, one for the command" | AP-7 | UNSTATED | V1: "The command and skill that put a session into that role are `/sc:coordinator`". V2: "The command, skill, verbs ... state folder ... and tag all follow from the one word". Neither argues why the role noun and the command noun could not differ (for example `coordinator` for the role and a differently named command, or the reverse) | High |
| A-002 | Naming the family must use one noun for the genus, or two unrelated nouns for two roles. A genus noun with a different-noun species (for example "coordinator" as genus, "orchestrator" as the defined name for the script-woken species) is not considered | AP-1, AP-7 | UNSTATED | V1 uses qualifiers on the same noun. V2 uses two nouns with no genus. Neither mentions a layered name | High |
| A-003 | The command must exist at all as a slash command, and a role is entered through a command. The person-opened coordinator needs no command (WORKER-CONTRACT line 70), while Clay's session "runs `/sc:orchestrator`" (D:93) | AP-2 | UNSTATED | Neither variant asks whether the script-woken session could start from a skill, an automation prompt or an existing command | Medium |
| A-004 | An owner ruling like R10 binds later naming choices, and its scope can be read from the ZS-REQ row | AP-5 | STATED | V1 fact 1 and Risks; V2 fact 4 and Risks ("the debate weighting rule makes that decisive") | High |
| A-005 | R10 (2026-11-18) supersedes the owner's earlier usage of "orchestrator" in issues 339 (2026-11-01) and 444 (2026-11-08). V2 uses those titles as evidence of the owner's vocabulary without noting they predate R10 | AP-5 | UNSTATED | V2 fact 4: "The owner did not rename issues 339, 423 and 444 afterwards". Neither states whether a later ruling overrides earlier wording or whether untouched titles show intent | Medium |
| A-006 | Whether Clay's per-repo session and the owner's per-project coordinator session are two sessions or one. ZS-REQ R9 says the owner's coordinator "carries the issue-pipeline duties" from a standard install, with session `COORD-<RepoName>`, and that today's coordinator is the session `ORCH-IronClaude` | AP-1 | UNSTATED (V1); STATED (V2, only as a D07 dependency) | V1 treats them as one genus without a topology condition; V2 flags "D07 decides topology". Neither mentions that the owner's own session name today starts with `ORCH-` | High |
| A-007 | The authority model (who starts the session, whether it holds standing grants) is the axis on which a naming split should be drawn, rather than function (polls issues, supervises workers) or lifetime (per repo, all sessions) | AP-1 | UNSTATED | V1 and V2 both reason from WORKER-CONTRACT line 70 ("the person opened") | Medium |
| A-008 | The cost of renaming is measured in text edits to Clay's design and PR 686 only. It leaves out retraining readers and agents, hooks and tests that pin names, the Orca automation and ccsession tag names that exist today, and the owner's own session names | AP-4 | UNSTATED (the measure); CONTRADICTED (the size: V1 "cheap", V2 implies entrenched) | See X-004. Tag families in play today: `coordinator`, `orchestrator-<short>-<n>`, `COORD-<RepoName>`, `ORCH-IronClaude` | High |
| A-009 | The merged design (PR 681) and the open PR 686 are fixed text vs editable text | AP-2 | CONTRADICTED | V1: "mechanical edits on a PR that is unmerged and a design doc whose disposition D14 decides". V2: "merged design fixes the names" | Medium |
| A-010 | The debate cannot change GitHub text, so issue titles 339, 423, 444, 655 stay as they are during this decision | AP-4 | STATED | V1: "no GitHub write is allowed here". V2: "cannot be edited by this debate". Neither makes "owner renames the three titles" a candidate action | Low |
| A-011 | A glossary line in the spec and in HOW-WE-WORK.md is enough to bridge title and text vocabulary for readers and agents. HOW-WE-WORK.md on master has 0 hits for "orchestrator" today, so no glossary exists yet | AP-4 | UNSTATED (that it suffices) | V1: "A glossary line ... covers the gap". V2: "a glossary line in HOW-WE-WORK.md and the contract" | Medium |
| A-012 | The counts quoted ("hits", "uses", "times") measure how entrenched a word is and are comparable between variants | AP-3 | UNSTATED | Both mix line counts and occurrence counts: WORKER-CONTRACT "80 hits" is lines (104 occurrences); `agent-work-report` "23 times" is lines (31 occurrences); sweep skill "6 hits" is lines (8 occurrences). The metric is never defined | Low |
| A-013 | Issue 339's "orchestrator mode" (one person-opened session that runs and manages all sessions) is a distinct role from both the person-opened coordinator and the per-repo session. V1 calls it "the owner's epic"; V2 calls it "the general orchestrator". Neither says where it sits in its own family | AP-6 | UNSTATED | V2 fact 3 quotes 339 as "main session goes into orchestrator mode" (the person-opened session) while its Claim keeps "coordinator" for person-opened sessions (see X-011) | High |
| A-014 | Following the platform's (Orca's) vocabulary is a reason to pick an IronClaude noun | AP-3 | STATED | V1 fact 4; V2 fact 6. Opposite deductions (X-009) | Medium |
| A-015 | The overlap of "orchestrator" with the parent-session meaning in 63 files is a real reader and agent collision | AP-3 | STATED | V1 fact 5 and "What it gets right"; V2 "What it costs" second bullet. Verified count 63. Weight differs (X-008) | Medium |

### Promoted [SHARED-ASSUMPTION] diff points

Each UNSTATED precondition above becomes a synthetic diff point so the debate in Step 2 must address it. Classification CONTRADICTED rows (A-009) are already covered by X-001 and X-004.

| # | Tag | Diff point to debate | Source | Impact |
|---|-----|----------------------|--------|--------|
| SA-001 | [SHARED-ASSUMPTION] | Must the command name equal the role name? Decide role name and command name separately | A-001 | High |
| SA-002 | [SHARED-ASSUMPTION] | Can the family have a genus noun and a differently named species or command (layered name) | A-002 | High |
| SA-003 | [SHARED-ASSUMPTION] | Does the script-woken session need a slash command at all | A-003 | Medium |
| SA-004 | [SHARED-ASSUMPTION] | Does R10 (2026-11-18) override the earlier "orchestrator" wording in 339 and 444, and does an untouched title show intent | A-005 | Medium |
| SA-005 | [SHARED-ASSUMPTION] | Are the owner's per-project coordinator (`COORD-<RepoName>`, carries issue-pipeline duties, today `ORCH-IronClaude`) and Clay's per-repo orchestrator the same session, decided before naming (D07) | A-006 | High |
| SA-006 | [SHARED-ASSUMPTION] | Is authority model the right axis for splitting names | A-007 | Medium |
| SA-007 | [SHARED-ASSUMPTION] | What the rename cost really includes (tags, automations, pinned tests, session names, reader retraining), and not only text edits | A-008 | High |
| SA-008 | [SHARED-ASSUMPTION] | Does a glossary line bridge the title gap in practice | A-011 | Medium |
| SA-009 | [SHARED-ASSUMPTION] | Define the count metric (lines or occurrences) before using counts as weight | A-012 | Low |
| SA-010 | [SHARED-ASSUMPTION] | Where does the all-sessions role of issue 339 sit relative to the person-opened coordinator and the per-repo session | A-013 | High |

## Verification Log

Checked against /home/coder/.cache/ic-snap-20261120/{master,pr-a,pr-p} unless stated. No GitHub or Orca write was made.

| Claim (source) | Result |
|----------------|--------|
| WORKER-CONTRACT.md "coordinator" 80 and "orchestrator" 0 (V1 fact 2) | Verified as line counts: 80 lines, 104 occurrences; 0 "orchestrator". Lines 3, 5, 70, 287 ("WC-16. Coordinator loop"), 299 ("5. Coordinator brief template") match |
| HOW-WE-WORK.md lines 355 and 359 (V1 fact 3) | Verified. File has 0 hits for "orchestrator" |
| sweep skill 6 and command 3 (V1 fact 3) | Verified as lines (skill 8 occurrences, command 3) |
| No `commands/orchestrator.md`, no `sc-orchestrator*` skill on master, pr-a, pr-p (V1 fact 8, V2 fact 1) | Verified absent in all three |
| `agent-work-report/SKILL.md:12` text, "coordinator" 23 times (V2 fact 5) | Line 12 verified. 23 is the line count (31 occurrences) |
| Design D:65, 93, 133 (OQ5), 135 (ADD1), 714, 799, 862, 902, 1277 (U19) | All verified with the quoted words. D:1146 is "10. Owner decisions". OQ5 Owner column is "no" |
| Design word counts 759 and 121 | Verified exactly |
| src+tests "orchestrator" 1179 (master) and 1816 (pr-a) | Verified exactly. Difference 637 against V1's "about 640" |
| Files containing the word 237 to 279 (V2 fact 2) | Not reproduced: 195 to 237 (case-insensitive) or 185 to 227 (case-sensitive). Delta 42 matches. UNVERIFIED scope |
| `orchestrator_tier` 13 uses (V1 fact 8) | I count 15 lines in pr-a (10 src, 5 tests). Minor discrepancy |
| `IronOrchestrator` as an identifier PR 686 adds (V1 fact 8) | 0 hits in pr-a src and tests; appears in the design doc (D:95, D:866). Not a code identifier |
| 63 installed files use "orchestrator" (both) | Verified: 63. reflect 23, troubleshoot 20, evidence-validator 18 verified as line counts. qa.md:56 "The parent orchestrator" verified |
| ZS-REQ R9 (line 40) and R10 (line 41) (both) | Verified. R10 quote exact. R9 adds `COORD-<RepoName>` and that today's coordinator is `ORCH-IronClaude` |
| Orca role table "Coordinator", "Handoff owner" (V1 fact 4) | Verified through `orca skills get orchestration` (lines 38 and 40). "Ask the coordinator a question" wording not checked (UNVERIFIED) |
| open-decisions.md lines 12 and 15, Q26 `final.md` (V1 fact 7) | File not found at the stated path. UNVERIFIED |
| Issues 339, 444, 655, 431, 462, 516, PR 681 merge time (both) | UNVERIFIED. Only .dev/issues/423 exists locally; its description.md says "orchestrator mode / skill", "Orchestrator v2 - Proactive Holistic", "each Orchestrator catalogues", "after the v1 orchestrator is completed", consistent with V2's quote |
| OD6 and "rulings 1 and 8" (D:1157) | Row verified; underlying RULINGS.md not read. UNVERIFIED |

## Summary
- Total structural differences: 6
- Total content differences: 14
- Total contradictions: 11
- Total unique contributions: 14
- Shared assumptions: 15 (STATED 4, UNSTATED 10 and promoted as SA-001 to SA-010, CONTRADICTED 1)
- Highest-severity items: X-001 (the name `/sc:orchestrator` is not an owner decision: OQ5 Owner column is "no", and none of OD1 to OD15 covers it); X-002 (R10 "everywhere" reaches the command name or not, plus unmentioned R9 fact that today's coordinator session is `ORCH-IronClaude`); X-006 and X-007 (one noun leaves rules silent vs two nouns; per-repo session is a kind of coordinator or a new role; depends on D07 topology); X-004 (rename cost: counts agree exactly, inference opposite); SA-001 and SA-002 (neither variant separates the role name from the command name, or considers a layered name); SA-005 and SA-010 (topology of owner coordinator vs Clay orchestrator vs issue 339 is assumed, not decided).
- Unverifiable inputs: primary text of issues 339, 444, 516, 655, 431, 462; owner alignment files (open-decisions.md, Q26 final.md); RULINGS.md; PR 681 merge time. V2's file counts 237 to 279 and V1's `orchestrator_tier` 13 are slightly off from the snapshot counts.
