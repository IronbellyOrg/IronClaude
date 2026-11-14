# Round 1: Advocate for Variant B (Proposal B, `variant-2-original.md`), slot C-11

Status: Complete

Debate: sc:adversarial, slot C-11 `rfqa-first-step-and-readonly-scope`, Round 1 of 2 (blind). Focus: correctness, risk, test-coverage.
Tags: [CODE-VERIFIED] read in this session at the cited path:line; [RUN-VERIFIED] observed by a read-only script run in this session; [UNVERIFIED] carried or not checked. Paths are relative to the repo root unless absolute.

## Position summary

The first rf-qa change should be a single-document gate for one rf-qa-qualitative document type, run beside the existing gate, with every new reviewer mechanically read-only; the `/task` lens agents keep their agent files and tools in that change, and hardening them is a separate, smaller item triggered by a measured write, not by assumption. A read-only pilot of the M-B1 transcript audit run for this statement found zero Write/Edit calls to any reviewed output across 366 report-only rf-qa / rf-qa-qualitative transcripts, and found that report-only lens agents use Write and Bash for mutation testing on scratch copies, which a read-only reviewer would lose.

## Steelman of Variant A

The strongest version of Variant A:

1. **It closes a HIGH invariant now, on the path where it matters most.** INV-G ("reviewers are mutually blind and mechanically read-only") is HIGH in the C-11 row (`phase-outputs/discovery/undecidable-conflicts.md:28`). The `/task` lens agents are report-only by prompt only: `mode: "bypassPermissions"` and `fix_authorization: false` (`src/superclaude/skills/task/SKILL.md:225, 241`) on an agent whose frontmatter grants Write, Edit and Bash with `permissionMode: bypassPermissions` (`src/superclaude/agents/rf-qa.md:5-10`) [CODE-VERIFIED]. The gate runs after every phase of every MDTM task (`task/SKILL.md:192, 286`) [CODE-VERIFIED]. If any surface deserves the mechanical guarantee first, it is the highest-traffic reviewer surface. Variant B leaves that exposure open for an interval and says so.
2. **The target shape is already there.** Many parallel report-only reviewers, one consolidation, ONE fix agent ("No other agent modifies files during this step", `task/SKILL.md:254`), a verification round (`:256`) and the cap "After 2 fix cycles (3 reviews), HALT" (`:258`) [CODE-VERIFIED]. That is the panel loop's shape (reviewers, one Reviser, cap 3). Starting where the shape already exists minimises conceptual translation.
3. **The read-only reviewer pattern exists and is runtime-backed.** `reflect-reviewer.md:5, 8` (tools Read/Grep/Glob plus search, `permissionMode: plan`) [CODE-VERIFIED], with a static guard test (A cites `tests/cli/reflect/test_reviewer_readonly_tools.py:30-66`). My own pilot below even supports A here: the runtime refused a Write attempt by a reflect-reviewer.
4. **The two halves are separable (A section 7 part 2).** Half 1 (agent swap, executor persists, prose consolidation kept) needs no panel code; Half 2 (merge/ledger) is limited to document outputs, which keeps it outside C-01 trigger T-a. That is a genuinely good decomposition (diff U-001, High).
5. **Its oracle is the first behavioural oracle rf-qa has ever had, on the gate that matters.** Arm 0 measures the current lens agents; a deterministic no-model arm and a model arm with a tree-hash mutation check and an UNVERIFIABLE-share metric (A section 5, M4-M5). The UNVERIFIABLE-share metric is exactly the right instrument for the capability-loss risk B raises.
6. **It touches none of the ten S1-S3 files** (A section 3.2) and keeps the pinned step-9 cap sentence, "no minimum count" and the unattended-caller paragraph word for word, so the existing pins guard its edit.
7. **A document-type start tests little that is new**: spec-panel already reviews spec-like single documents (B section 8 records this objection itself).

What A genuinely gets right: the exposure is real by design; Half 1/Half 2 separability; the checklist formula's undefined case TOTAL = UNVERIFIABLE (U-002); the UNVERIFIABLE-denominator risk (U-003); the hash mechanism (X-002); and that a per-slot `lens` key is cheap.

## Strengths claimed (Variant B)

1. **The "one place" premise of Variant A is contradicted by the code, and B's start does not depend on it.** `fix_authorization: false` occurs 93 times in 8 files under `src/superclaude/skills/` (task-builder 20, tech-research 15, readme 14, roadmap 11, tech-reference 11, operational-guide 11, task 10, sc-reflect-protocol 1) [CODE-VERIFIED, Grep count this session]. `/task` step 5 says domain-specific lens prompts "are embedded in the task file's QA gate items by the skill that created the task file. The executor spawns them exactly as written" (`task/SKILL.md:250`) [CODE-VERIFIED]. The README skill's final gate alone runs 3/7/11 agents by intensity with "Max 1 fix cycle" at lite (`src/superclaude/skills/readme/SKILL.md:458-460`) [CODE-VERIFIED]. The diff analyst's code check on X-001 also "Supports B". A shape-level first step leaves one pattern to replace everywhere later; a `/task`-gate first step leaves two implementations of the same gate.

2. **B's first step fits the settled engine with no new locator.** `review merge --doc` takes one file (`src/superclaude/cli/review/merge_cmd.py:30-33`, `click.Path(exists=True, dir_okay=False)`), `new_ledger(doc, cap=3)` and `merge_round(ledger, doc_text, n, reviewers)` take one document (`ledger.py:37, 107`) [CODE-VERIFIED]. The `/task` gate reviews one-to-many files with partitioning above 6 files (`task/SKILL.md:264`) and section ranges above 3000 lines (`:266-275`) [CODE-VERIFIED]. The panel caps reviewers at 8 (`panel.py:248`, "total reviewers must be 1..8") [CODE-VERIFIED] against `/task` floors of 6/8/10/12 (`task/SKILL.md:196-201`) [CODE-VERIFIED]. A single-document gate meets none of these limits; the `/task` gate meets all three. C-01's adjudicated hybrid keeps the spec loop on v1 one-document machinery; B is a module of exactly that.

3. **The current exposure is now measured, not assumed (M-B1 pilot) [RUN-VERIFIED].** Method: read-only scripts (`uv run --no-project python`, private `/tmp` dir removed on exit) over the local Claude Code transcripts in `/home/coder/.claude/projects/**/subagents/`. Each subagent transcript has a sibling `.meta.json` with `agentType`. Selection: `agentType` in {`rf-qa`, `rf-qa-qualitative`}, first user message contains `fix_authorization: false` and not `fix_authorization: true`. Result: 204 rf-qa + 162 rf-qa-qualitative = **366 report-only transcripts**. Their Write/Edit/MultiEdit/NotebookEdit calls: 3,146 to QA/report paths, 147 to `/tmp`, 2 Edit calls on `/dev/null` (both returned an error), and **0 to any other path**. Counts are of log records and can include duplicated records of one call. Bash: 5,261 calls; a tight screen for `sed -i`, `git stash|checkout|restore|reset|commit|add|apply|clean`, `perl -pi` and `cp ... src|tests|.dev/` outside `/tmp` gave 78 candidates; I read the first 30 and every one either targets a scratch copy (`$M`, `$W`, `$D`, `$T` variables set to `/tmp` dirs) or is `echo`/`grep` text; the one `git checkout -q -b feat/review-panel` ran in a `git init` repo under `mktemp -d /tmp/b2qa-reftest.XXXXXXXX` (transcript `agent-a819ed2a6069ae76e.jsonl`, agentType `rf-qa`). The remaining 48 Bash candidates were not read [UNVERIFIED]. So in every observed run, "report-only by prompt" held for file tools; this is the evidence B-3 asked for before choosing, and it supports keeping the legacy agents unchanged in the first change.

4. **Hardening the lens agents removes a verification capability that lens agents use in practice [RUN-VERIFIED].** In the one task whose lens prompts name `qa-structural-*`/`qa-content-*` report paths (worktree `issue-331-github-issue-watcher`, 16 lens transcripts), 4 of 16 lens agents (`test-adequacy` x2, `security-invariants` x2) wrote mutation-testing harnesses with Write/Edit (`/tmp/secinv-harness/mutate.py`, `/tmp/ironclaude-mut-harness.sh`, `/tmp/mutwork-tadq*/driver*.py`, `/tmp/iw-mut-harness/driver.py`), copied `src/` into `/tmp`, mutated the copies with `sed -i`, ran tests, then removed the copies and checked `git status --short -- tests src`. A Read/Grep/Glob reviewer cannot do any of that. This is the concrete form of B section 3.1 item 3 (`rf-qa.md:133` "Local Read/Grep/Glob/Bash remain the primary verification surface") and of the A-004 assumption; Variant A's Half 1 would remove it from the standard lenses on day one, before its own M5 arm can measure the loss.

5. **The new-reviewer pattern B relies on is enforced by the runtime, not only by a static test [RUN-VERIFIED].** Across 517 `reflect-reviewer` transcripts the tool calls were Read 11,512, Grep 9,410, Glob 1,117 plus codegraph search/node/callers/explore; the only write attempt (`mcp__razor_culture__pool_Write` on a `reviewer-cards/reviewer-1-card.md` path, logged twice) returned `Error: No such tool available`. So "every NEW reviewer is mechanically read-only" (B's INV-G scope) is achievable today by an agent definition; B does not need the legacy agents to prove it.

6. **Zero edits to pinned files, checked mechanically.** B keeps `task/SKILL.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the ten `S1_S3_FILES` byte-identical and checks it with `git diff --stat` plus the named suites run unedited (B M-B3). `task/SKILL.md` holds pinned strings (cap rows C-105..C-113, "no minimum count", the unattended-caller paragraph `tests/skills/test_worker_contract.py:1716-1730`) and is a named reflect consumer (`tests/review/test_reflect_consumer_inventory.py:97-100`) [CODE-VERIFIED by B; diff U-013 verified]. Not editing it is cheaper and safer than editing around its pins.

7. **B respects the owner boundary the C-11 row sets.** The row says "whether the lens agents are made read-only in the first change (Q3) and which 'eight lens' set is meant are owner decisions" (`undecidable-conflicts.md:28`) [CODE-VERIFIED, read this session]. A answers Q3 itself ("answered yes", A line 22). B leaves Q3 to the owner and supplies the measurement (M-B1, now piloted) that informs the answer.

8. **B adds no state the adjudicated slots did not conclude.** No per-slot `lens` key, no checklist completion predicate, no `min_complete` owner decision (C-03 INV-003), no T-a evaluation forced before the first step (C-01). A adds a completion state on top of C-03's "block valid" (A line 29 says so) and makes the floor a module parameter, which C-03 did not conclude.

## Weaknesses identified (Variant A)

1. **A's safety claim does not reach the agents that actually used write tools.** A says "one edit of one section changes the safety property for every lens reviewer of every phase gate" (A line 69). Step 5 domain lenses are spawned "exactly as written" from the task file (`task/SKILL.md:250`) [CODE-VERIFIED], so an edit of steps 3-4 does not reach them (diff X-001). In the pilot, every lens agent that used Write/Edit outside its report (`test-adequacy`, `security-invariants`) carried a domain lens name, not one of the standard 8 [RUN-VERIFIED]. A's Half 1 therefore hardens the standard lenses, which showed no out-of-report writes, and leaves the domain lenses, which showed the writes, unchanged.

2. **Half 1 is not "an agent-type change at the spawn sites" (A line 139).** The lens agents persist their own reports: 3,146 Write/Edit calls to QA/report paths in 366 report-only transcripts [RUN-VERIFIED]. Moving that to the executor rewrites step 3/4's report-path instruction (`task/SKILL.md:238`) and step 10's "Check that each lens agent wrote its report" (`:260`) [CODE-VERIFIED]. The diff analyst's code check on X-003 "Supports B on scope". A itself concedes the persistence change at A line 38.

3. **Half 1 removes a used capability before A's oracle can measure the loss.** A's M5 arm 1 measures UNVERIFIABLE share against arm 0, but only on seeded documents; real lens agents run mutation tests and scratch-repo experiments with Write and Bash (strength 4) [RUN-VERIFIED]. A read-only `test-adequacy` lens cannot run a mutant. A's own risk table rates "Reviewer capability" MEDIUM (A section 4.2) without evidence of how often lenses need it; the pilot shows 4 of 16 in one task.

4. **Largest blast radius, by A's own rating.** The gate runs after every phase of every MDTM task (`task/SKILL.md:192`) and "No exceptions" (`:286`) [CODE-VERIFIED]; A rates availability HIGH (A section 4.2). A mitigates by keeping steps 6-9 as a "selectable branch", which is a second gate path to keep in sync, not a removal of risk.

5. **The engine and panel limits bite at the gate A chose.** Panel max 8 reviewers (`panel.py:248`) against floors 10 and 12 (`task/SKILL.md:200-201`) [CODE-VERIFIED]: A's template covers 2 of the 4 tiers (A section 3.5). One-document merge (`merge_cmd.py:30-33`, `ledger.py:107`) [CODE-VERIFIED] against multi-file phase outputs: A needs one ledger per file plus partition merging, and code-output phases stay on Half 1 indefinitely (A section 7 part 2).

6. **One of A's static guards checks a control the harness ignores.** A's M1 asserts the gate text no longer says `mode: "bypassPermissions"`. This session's Agent tool schema says the spawn `mode` is "Deprecated; ignored. Subagents inherit the parent session's permission mode; agent-definition frontmatter may override it" (diff X-004). That check guards text, not behaviour. (A's first M1 check, on the tools allowlist, is the right one.)

7. **A goes past the adjudicated slots and the owner boundary.** It answers owner question Q3 (A line 22) although the C-11 row reserves it for the owner (`undecidable-conflicts.md:28`); it adds a checklist completion predicate on top of C-03's "block valid" (A line 29); it makes the 6-agent floor a module parameter where C-03 left the owner open (A section 0).

8. **Internal count error in A's M2 golden.** A line 28 counts 8 packaged templates; A line 115 lists "default, `live7`, the seven reflect files" (9). Glob finds 8: default, live7 and six reflect files (diff X-007) [carried from the diff analyst's Glob]. Minor, but it is in the test plan.

9. **A changes the panel core for one consumer.** Adding `lens` to `_SLOT_KEYS` (`panel.py:46`) [CODE-VERIFIED] is cheap (X-002), but the lens already travels as free text in the brief (`persona_lens`, `reflect-reviewer.md:56`) [CODE-VERIFIED]; no consumer yet needs the core to know it.

## Concessions

1. **X-002: B is wrong on the hash.** `template_sha256` hashes the template object and `_SLOT_KEYS` (`panel.py:46`) is an accept-list checked at `panel.py:215-216` [CODE-VERIFIED]; widening it edits no template file and changes no hash. B's "schema change over all 8 packaged templates and their validate tests" overstated the cost. B's reason to defer `lens` is now only "no consumer needs it yet", not cost.
2. **A-006: B's install sentence is wrong.** B said a new agent "must be installed (`tests/unit/test_cli_install.py:64` lists the rf-* agent files)". The table is the member list of the 4.3.5 baseline wheel (`test_cli_install.py:46-53`) and `_assert_present` fails only on a missing listed name (`:502-506`) [CODE-VERIFIED]. An unlisted new agent passes. The real cost is `make sync-dev` / `verify-sync` (INV-K).
3. **X-006: B's C-03 condition-7 dependency does not apply to A's design.** A computes confidence per reviewer from its own checklist rows (`rf-qa.md:505`), not from ledger support flags.
4. **INV-G stays unmet for the legacy lens agents in B's first change.** The pilot shows no out-of-report file-tool write to a repo path in 366 runs, but Bash was screened, not fully classified (48 of 78 candidates unread), the transcripts cover this machine only, and retention is unknown. Absence in the sample is not a mechanism.
5. **M-B1's decision rule as written has a gap.** "Zero writes outside the agent's own report path" supports B; "one write to a reviewed output file" refutes it. The pilot found 147 `/tmp` scratch writes, which satisfy neither clause. The rule needs three classes fixed before the full audit: (a) own report path or `/tmp` scratch: neutral; (b) any repository working-tree path other than the own report: refutes B-3; (c) git state changes in the reviewed repository: refutes B-3.
6. **B's first change is not literally "touches no existing file".** Some skill must call the new document gate (for example `readme/SKILL.md` or the PRD skill); B names no document type and no host file. That host edit must also leave its own pinned strings intact. The PRD skill already runs "intentional, acceptable double QA" with `/task` (`src/superclaude/skills/prd/SKILL.md:423`) [CODE-VERIFIED], so an additive panel run adds a third QA pass and its cost.
7. **C-012: A advances future PR review further** (per-slot lens, checklist mode, replay fixture); B delivers only the read-only reviewer and persistence pattern.
8. **User-visible value of B's first step is small**, as B section 7 says, and spec-panel already reviews spec-like single documents.
9. **A's Half 1/Half 2 split is a real contribution** (U-001). If the owner answers Q3 "yes", B's own fallback should be A's Half 1 limited to an agent split plus orchestrator persistence, without the panel.

## Shared assumptions

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

## Per-point positions

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

## What I did not verify

- The 48 unread Bash candidates of the pilot screen; the full Bash classification of 5,261 calls.
- Whether transcripts on other machines or older, deleted transcripts would change the M-B1 count.
- Whether every standard-lens spawn prompt carries `fix_authorization: false` in its first message (the selection rule depends on it).
- Augment search tool side effects (A-002); target-runtime enforcement beyond the one refused call (A-001).
- No repository file other than this statement was written; no test was run; no git command mutated anything.
