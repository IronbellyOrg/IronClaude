# Merge Execution Log

<!-- RESUME MARKER: none (run complete; all 66 Changes applied) -->

## Metadata
- Base: Variant V1 (opus:architect), `variant-1-opus-architect.md`
- Plan: `refactor-plan.md` (66 Changes; Merge-executor instructions and acceptance checks A1-A15 binding)
- Executor: merge-executor agent (Step 5)
- Output: `../merged-spec.md` (`.dev/brainstorms/20261113-orchestrator-tui-alignment/adversarial/merged-spec.md`)
- Changes applied: 66 of 66 (46 APPLIED, 20 APPLIED-WITH-DEVIATION, 0 SKIPPED, 0 FAILED)
- Status: success (post-merge validation a-h PASS)
- Timestamp (start): 2026-11-13T20:51:25Z
- Timestamp (finish): 2026-11-13T21:35:02Z
- Step 1 done: base copied with `cp variant-1-opus-architect.md ../merged-spec.md` (751 lines).
- Order: Changes applied in plan order (1 to 66), one log entry each, written after the Change lands.

## Changes Applied

### Change 1: PR actor model; no worker runs `/sc:pr-submit` (R25-INV-001; fixes D4)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1/V2/V3; `WORKER-CONTRACT.md:23`, `:41`, `:243`; `sc-pr-submit-protocol/SKILL.md:19`, `:47` (as re-checked in the plan)
- **Target**: Base SW-07, SW-08, SW-10, OB-06, OB-07, WA-01, WA-03, XC-07 ("runs in" and pr-submit criteria); XC-09 (3); TB-UPSTREAM row; 5.1 W1 L-watch and W2 L-flip; 6.2; 6.3 Coordinator, Worker and new PR session rows; 6.4 rule 2; 7.2 Interaction rows; section 3 new Q25 row
- **Before**: workers opened their own PRs with `/sc:pr-submit --monitor 3`; XC-09 (3) created worktrees with `--agent` and then dispatched `worker-start` into them
- **After**: a worker stops at `worker_done`; an owner-designated top-level PR session (Q25) runs `/sc:pr-submit` after `worker_done` is admitted and the worker's session ended; a worktree gets its agent from `worker-start` or `worktree create --agent`, never both; the coordinator never runs the poll loop
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-001 - merged per Change 1 -->` (placed at section level in the provenance pass, Change 65)
- **Deviation**: (1) also edited the W1 and W2 wave cells and the TB-UPSTREAM row that named `/sc:pr-submit`, so acceptance check A11 holds (not in the Change's target list); (2) the Q25 DEC edges and `GRANT(<item>,pr-submit)` GATE edges are drawn in the edge table built by Change 19, not as a separate edit here; (3) SW-14 does not exist yet; it receives the same text when Change 42 adds it.
- **Validation**: Structural integrity PASS | References PASS (Q25 row defined in section 3) | Contradictions PASS (`grep pr-submit` shows no worker PR duty left)

### Change 2: Coordinator home and the ledger's branch (R25-INV-002; fixes D3 with Change 45)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V2, R3-V3 (recommended answer), R3-V1 (owner alternative); project CLAUDE.md
- **Target**: Base XC-01 Location and runs-in, XC-09 blocked-by, runs-in and Q, 5.4 (new coordinator-home row), 6.1 Decision ledger row, 6.2 (rule sentence), 6.4 rule 3 (replaced, `.claude/` sentence kept), section 3 new Q26 row
- **Before**: ledger path PLAN INFERENCE under this debate's folder inside the #539 checkout; coordinator in "a checkout the owner chooses"
- **After**: ledger package `.dev/tasks/<program-package>/` in the coordinator home on the branch named in Q26; never the #539 checkout; committed only on request; coordinator never switches branches; Q26 asked at W0 with its default (XC-09 does not start; ruling still recorded on the Codex thread)
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V2, R3-V3), R25-INV-002 - merged per Change 2 -->`
- **Validation**: Structural integrity PASS | References PASS (Q26 defined) | Contradictions PASS (no ledger path under the #539 checkout remains in XC-01, 6.1)

### Change 3: Skip rule for the hard publication order, with withheld-slot semantics (R25-INV-003; fixes IC-V1-2)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1, R3-V2 (mechanical skip), R3-V3 (skipped is not completed; content dependencies); ADJ line 442
- **Target**: Base XC-02 (new criterion 6), section 3 Default cells of Q2, Q3, Q20, 6.5 row "A gated Q is unanswered", WA-02 (new criterion 7)
- **Before**: hard order with no skip semantics; Q3's default stalled OB-08, SW-09, V2-01
- **After**: defaulted links recorded as `skipped (default Qn, date)`; next link eligible; skipped satisfies only the order edge; defaulted #450 edits omitted, set posts once
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-003 - merged per Change 3 -->`
- **Note**: the PROC edges WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01 are typed in the edge table of Change 19. No owner question added (plan "not made" row 24).
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (Q3 default now consistent with the hard order)

### Change 4: Widen the INV-008 requirement to effective executable paths (R25-INV-004)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1/V2/V3; `invariant-probe.md` R25-INV-004 (git 2.47.3 `gitattributes(5)`, documentation only)
- **Target**: Base 0.1 (appended "Channels in scope" paragraph), SW-01 (new (4)), SW-02 (1) (replaced), 4.1 TB-GIT row (replaced), 7.2 Guard row, 7.3 first row (replaced), section 3 Q1 row (part (b) added)
- **Before**: requirement and test named only `core.fsmonitor` and `filter.*.clean`; other channels were a PLAN INFERENCE aside
- **After**: outcome-worded requirement; test fails on `.process` too; ruling states scope of `include.path`/`includeIf` and `GIT_*`/`GIT_CONFIG_*`; TB-GIT satisfied only when the test covers the ruled set; no code fix specified; Q1 default unchanged
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-004; git 2.47.3 gitattributes(5) (documentation only) - merged per Change 4 -->` (inline above the 0.1 paragraph)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (INV-008 still UNRESOLVED; no fix design)

### Change 5: No monitored PR tool on #539 before the ruling is applied (R25-INV-005)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1 and R3-V3 (V2's thread-exclusion rule not adopted, plan "not made" row 25)
- **Target**: Base SW-02, SW-03, SW-05 (criteria and runs-in), 6.3 #539 author row (replaced), 6.5 new stop row, 6.9 new bullet, section 3 new Q28 row
- **Before**: nothing limited `/sc:pr-submit` on #539; the tool could design and push its own INV-008 fix
- **After**: hand pushes of named paths until SW-02 lands the ruling and the owner's reply closes the Codex thread; then `--monitor 3` only under the #539 GRANT row; ruling-needing findings stop the run; Q28 asked with default "no pr-submit on #539"
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1, R3-V3), R25-INV-005 - merged per Change 5 -->`
- **Note**: Q28 row placed after Q26; Q27 (Change 12) is inserted between them.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Runtime capability gate SWEEP-RUNNABLE (R25-INV-006)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1/V2/V3; probe R25-INV-006 (`superclaude sweep --help` "No such command 'sweep'"); `sc-sweep-protocol/SKILL.md:23-24` (re-checked in the plan)
- **Target**: Base 7.3 row 2 (replaced), 6.6 bullet 2 (replaced), 4.1 new node SWEEP-RUNNABLE (inline provenance comment), 6.5 new stop row, XC-04 blocked-by (appended), SW-06 (2) (fallback row added), section 3 new Q29 row
- **Before**: "`superclaude install` or `make sync-dev`" was taken to make `/sc:sweep` available after SW-05
- **After**: SWEEP-RUNNABLE gate defined once in 4.1; duty "not runnable" until it holds; XC-04 held; no in-place reinstall; Q29 asked (default: duty not runnable, XC-04 held)
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-006 - merged per Change 6 -->`
- **Validation**: Structural integrity PASS | References PASS (SWEEP-RUNNABLE defined in 4.1; Q29 defined) | Contradictions PASS

### Change 7: JOIN after the merge, from a named runner, root and destination (R25-INV-007; fixes D2 with Change 35)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1, R3-V2 (timing), R3-V3 (record fields); V3's pre-merge option not adopted ("not made" row 9)
- **Target**: Base XC-04 (criterion (4) replaced, blocked-by, runs in), 5.1 W1 L-live lane and W1 exit (XC-04 removed), W3 gate (SWEEP-RUNNABLE), W3 L-note lane (XC-04 before XC-07), W3 serial and exit, 5.4 this-checkout row (pre-merge sweep run removed)
- **Before**: JOIN in W1, possibly running the unfixed sweep from the #539 head
- **After**: JOIN in W3 after SW-05, SWEEP-RUNNABLE and a TB-GIT-ROW entry, on master code, record names actor, revision, `--root`, report destination and the same-sitting `dispatchId` list; CAP (XC-03) stays in W1
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2), R25-INV-007, X-002 - merged per Change 7 -->`
- **Note**: TB-GIT-ROW is referenced here and defined in 4.1 by Change 16.
- **Validation**: Structural integrity PASS | References PENDING (TB-GIT-ROW defined at Change 16) | Contradictions PASS (no W1 cell schedules XC-04)

### Change 8: OB-04 names its target Run and actor (R25-INV-008)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1, R3-V2, R3-V3 (disposable representative Run)
- **Target**: Base OB-04 (criteria, blocked-by, runs in, Q replaced), 6.3 Live reader row (amended), section 3 new Q30 row
- **Before**: OB-04 "as OB-03", from a terminal that holds no Run, target Run unnamed
- **After**: OB-04 after OB-03 in the holder terminal of an owner-approved disposable representative Run, never the alignment coordinator's own; record names Run id, terminal, lost questions, usability; held if no such Run; Q30 asked (default: OB-04 held, OB-06 not opened)
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-008 - merged per Change 8 -->`
- **Note**: the Q30 -> OB-04 DEC and `GRANT(OB-04,live-read)` GATE edges are drawn in the Change 19 edge table.
- **Validation**: Structural integrity PASS | References PASS (Q30 defined; GRANT family defined at Change 13) | Contradictions PASS

### Change 9: ORCA-AVAILABLE prerequisite and stop trigger (R25-INV-009)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1/V2 (stop trigger, retry once per WC-16 interval, ask once), R3-V3 (intake and resume prerequisite; reopen only on a successful read)
- **Target**: Base 4.1 new node ORCA-AVAILABLE (inline provenance comment), 6.5 new stop row, OB-03, OB-04, WA-04 blocked-by (appended)
- **Before**: no rule for "Orca app not reachable"
- **After**: live lanes held, one ledger row, retry at most every 5 minutes, ask the owner once, non-live lanes continue, reopen only on a successful read; the probe's outage is not claimed current
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-009 - merged per Change 9 -->`
- **Note**: XC-03 and XC-04 blocked-by gain ORCA-AVAILABLE in Changes 36 and 35; the XC-10 exit check and the 5.6 interruption rule carry it in Changes 51 and 20; edges drawn in Change 19.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Cadence record replaces "no extra scheduler" (R25-INV-010; owner confirms)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1/V2/V3; `WORKER-CONTRACT.md:288`; owner memory `coordinator-never-stop-polling.md` (lowest source tier)
- **Target**: Base 6.6 (cadence table inserted above the base bullets, which are kept as notes), base bullet 4 "GitHub state ... not on a timer" (replaced), section 3 new Q31 row
- **Before**: bullet list; "GitHub state ... not on a timer"
- **After**: cadence record table (WC-16 re-arm, `/sc:sweep` once SWEEP-RUNNABLE, observer 15 s, watcher cron after FU-2, PM 30 min, GitHub at gates and wakes, owner's recurring read-only check whose status is Q31); GitHub-timer question left to Q31
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-010; Base (V1) 6.6 bullets kept as notes - merged per Change 10 -->` (inline)
- **Deviation**: the plan's target "base-selection preserved strength 9 (amend)" is in `base-selection.md`, which this executor may not write (read-only except the two outputs). Not edited; the merged spec carries the corrected rule instead.
- **Validation**: Structural integrity PASS (H3 6.6 kept; table added) | References PASS (Q31 defined) | Contradictions PASS (no categorical "no scheduler" left in 6.6)

### Change 11: F3 caveat inventory by grep, not four texts (R25-INV-011)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1, R3-V2 (grep pattern), R3-V3 (reviewed inventory, mirrors equal); probe R25-INV-011
- **Target**: Base 0.1 F3 option, SW-02 F3 branch, section 3 "What the first four answers do", 7.1 INV-010 row
- **Before**: F3 = caveat four texts
- **After**: F3 = caveat every statement found by `git grep -n -i -E 'read-only|changes nothing'` over #539's file list (at least 16 locations), or list it in the PR body with the reason; plugin mirror byte-equal
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-011 - merged per Change 11 -->`
- **Deviation**: also corrected two base sentences the plan did not list but that repeated the "four" count: 2.1 Risks (F2 bullet) and 7.4 edge case 2. The Q1 row in section 3 itself did not contain "four caveats" (its decision text names F3 only), so only the "What the first four answers do" paragraph changed there.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (`grep -i 'four texts|four caveats'` = 0 hits)

### Change 12: Where SW-02's own plan package lives (R25-INV-012)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1/V2/V3 (all PARTLY); A-004
- **Target**: Base 6.4 rule 5 and 6.9 bullet (replaced with A-004's exact scope), SW-02 (new (5)), section 3 new Q27 row (inserted before Q28); SW-05 (4) kept unchanged
- **Before**: "No JSON key, file or sidecar inside PR #539"
- **After**: A-004 scope = no new program, collector, JSON key, sidecar, report file or program artifact in #539; SW-02's plan package decided by Q27 (default: written in the coordinator home, referenced by path; named-path commits only)
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-012 - merged per Change 12 -->`
- **Deviation**: SW-02 (4) said "no file is added", which would contradict the plan package under Q27; narrowed to "no JSON key, sidecar or report file is added" to match A-004's scope as this Change states it.
- **Validation**: Structural integrity PASS | References PASS (Q27 defined) | Contradictions PASS

### Change 13: GRANT records replace a single approval node (R25-INV-013; part of D5)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V1 (rows keyed by PR or issue and action), R3-V2 (fields), R3-V3 (repository, actor, scope, validity, revocation)
- **Target**: Base 6.8 (grant table appended, inline provenance), XC-01 (new (5)), 4.1 new node kind GRANT(<item>,<action>) (inline provenance), 6.3 Owner row (replaced)
- **Before**: "approves every outward post"; V3 M-APPROVAL imported as one boolean (S-005)
- **After**: grant table with 11 fields and 9 actions; `GRANT(<item>,<action>)` nodes satisfied only by a matching row; void on a changed Q; M-APPROVAL not a node
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-013 - merged per Change 13 -->`
- **Note**: the GRANT edges for every outward item are drawn in the Change 19 edge table.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: The pr-submit grant lists every write the tool makes (R25-INV-014; part of D5)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1/V2/V3; `sc-pr-submit-protocol/SKILL.md:70`, `:241` (plan re-check), `:234`, `:306` (probe)
- **Target**: 6.8 grant-table paragraph "What a `pr-submit` row lists" (inline provenance), 6.4 rule 2 (appended), PR items SW-07, SW-08, SW-10, OB-06, OB-07, WA-01, WA-03, XC-07 (criterion "run under GRANT(<item>,pr-submit)")
- **Before**: per-PR scope listed push, reply and resolve only
- **After**: a `pr-submit` row lists create or attach, fix commits and troubleshoot artifacts, push, replies and resolves, re-trigger comments, draft toggle (or `--merge-guard off`), resume effects; merge never included; unseen worker changes shown to the person before a push (`WORKER-CONTRACT.md:244`)
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-014 - merged per Change 14 -->`
- **Deviation**: also appended `Q25; GRANT(<item>,pr-submit)` to each PR item's blocked-by cell (the register half of Change 1's "Graph" line), so check A3 (every blocked-by endpoint exists) and the edge table agree. Done here because this Change touches the same rows.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: Who commits a worker's change (R25-INV-015)
- **Status**: APPLIED
- **Source**: Round 3 rules R3-V2, R3-V3 (no worker commits by default), R3-V1 (per-Task wording as the owner's option); `WORKER-CONTRACT.md:42`, `:244`
- **Target**: Base 6.3 Worker row (amended), 6.4 new rule 13, section 3 new Q32 row; the worker-brief requirement is carried into 6.10 by Change 30
- **Before**: no rule on who commits
- **After**: workers leave changes uncommitted by default; the PR session commits named paths after the person has seen unseen changes; a worker commit only with a word-for-word quoted owner instruction recorded as `GRANT(<item>,commit)`; Q32 asked when the first code-changing worker is dispatched
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V2, R3-V3), R25-INV-015 - merged per Change 15 -->`
- **Note**: rule numbered 13 now; Change 66 inserts the build-string rule as 13 (per the Change 61 map) and this rule moves to 14 then.
- **Validation**: Structural integrity PASS | References PASS (Q32 defined) | Contradictions PASS

### Change 16: TB-GIT as a ledger eligibility row before every sweep run (R25-INV-016)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: Round 3 rules R3-V1/V2/V3; `ls .dev/sweeps/` (four reports, re-checked in the plan)
- **Target**: Base 4.1 new node TB-GIT-ROW (inline provenance), XC-04 (new (5)), 6.4 rule 1 (appended), 7.4 new edge case 11
- **Before**: TB-GIT was an instruction only; old sweep reports unlabelled
- **After**: TB-GIT-ROW ledger row before any sweep run (procedural guard, not a mechanical block); four old reports marked "pre-INV-008, not JOIN evidence"; no program sweep before SW-05
- **Provenance tag**: `<!-- Source: Round 3 rule (R3-V1/V2/V3), R25-INV-016 - merged per Change 16 -->`
- **Deviation**: executor instruction step 10 lists five new 7.4 edge cases; four were added here in one block (11 old reports, 12 Orca down, 13 sweep command missing, 14 skipped link posted later) because they belong to Changes 16, 9, 6 and 3, all already applied. The fifth (a Q answer changes after drafts exist) is added with Change 60.
- **Validation**: Structural integrity PASS | References PASS (TB-GIT-ROW now defined; resolves Change 7's pending reference) | Contradictions PASS

### Change 17: Skeleton: V1 sections plus V2 weak points and V3 interface blocks (S-001)
- **Status**: APPLIED
- **Source**: V1 sections 0-7; V2 Weak point blocks; V3 per-system interface, failure and runbook blocks
- **Target**: Base 2.1 to 2.6, after each "Risks" list
- **Before**: per-system sections ended at "Risks"
- **After**: each of 2.1 to 2.6 has a "Weak points" and an "Interface contracts" sub-block (bold labels, not headings, so no H3 is renumbered), each with a provenance comment; content placeholders are HTML comments that Changes 57 and 58 replace
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) Weak point blocks - merged per Change 17 (skeleton) and Change 57 (content) -->`; `<!-- Source: Variant V3 (haiku:backend) interface, failure and runbook blocks - merged per Change 17 (skeleton) and Change 58 (content) -->`
- **Validation**: Structural integrity PASS (all H2 kept in order) | References PASS | Contradictions PASS; scaffolding to be removed by Changes 57 and 58 (checked in post-merge validation)

### Change 18: Keep V1's register and ids; add four ids (S-002)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 4.1 register (46 items)
- **Target**: Base 4.1 "Work items" line
- **Before**: "Work items (46)" with V1 ranges
- **After**: "Work items (50)": SW-01 to SW-14, V2-01 to V2-05, XC-01 to XC-11; V1 ids unchanged; four new ids named
- **Provenance tag**: `<!-- Source: Base (V1) 4.1 register, count updated - merged per Change 18 -->`
- **Deviation**: the four new register rows are appended by the Changes that define their content (V2-05 by Change 28, SW-14 by Change 42, XC-10 by Change 51, XC-11 by Change 59), not here, so no row is written twice. Count consistency is checked in post-merge validation (Change 61 check (d)).
- **Validation**: Structural integrity PASS | References PENDING until Changes 28, 42, 51, 59 add the rows | Contradictions PASS

### Change 19: Replace the text graph with an evidence-tagged edge table (S-003)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V2 4.2 (70 edges, re-keyed through the Change 61 map), V2 4.4; V1 4.2 edges V2 lacks; debate changes (C-003, X-005, X-006, X-007, X-002/R25-INV-007, GRANT and Q25-Q33 edges)
- **Target**: Base section 4 intro (kinds legend, also Change 56), 4.1 owner-decision line (Q1 to Q33), 4.2 (text graph replaced by a numbered table of 123 rows `# | From | To | Kind | Evidence | Provenance`), 4.3 (checks re-derived from the table, item 7 added), new 4.4 text graph (summary view generated from the table), new 4.5 differences from ADJ (V2 4.4 updated)
- **Before**: ASCII text graph with `->` and `~>`, no kinds or evidence per edge
- **After**: authoritative edge table with kind, evidence and provenance per row; dropped V2 edges and raised kinds stated above the table; summary text graph; differences table with the "Demoted to SOFT" row dropped and "TB-GIT, SWEEP-RUNNABLE -> XC-04", "no XC-05 -> OB-06" and "kept hard" rows
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 4.2 edge table ..., Base (V1) 4.2 edges V2 lacks, and debate changes - merged per Change 19 (...) -->`
- **Deviation**: (1) Numbering: the plan puts the text graph at 4.3 and the checks at 4.4; the binding executor instruction "never renumber an existing H3" keeps V1's 4.3 Graph checks at 4.3, so the text graph is 4.4 and the differences are 4.5. (2) The table is built once and already holds the edges of later Changes (21 TB nodes, 28 V2-05, 35 JOIN gate, 36 CAP, 40 no XC-05 -> OB-06, 42 SW-14, 46 merge grant, 51 XC-10, 59 XC-11), so those Changes verify the table rather than edit it. (3) Added edges the plan implies but does not list: per-item `GRANT(<item>,merge)` on every PR item (Change 44 "merges ... each need their own grant"), `GRANT(V2-03,issue-write)` (V2-03 links its handoff on #423), Q2 -> SW-13 (from section 3's gate column), XC-03 ~> SW-06 as SOFT (V1's XC-03 "blocks SW-06" cell would otherwise point backward from W1 to W0; see Change 48). (4) The 4.3 roots and sinks lists are re-derived from the table and re-checked by script in post-merge validation.
- **Validation**: Structural integrity PASS (4.1 to 4.5 in order) | References: checked by script in post-merge validation (checks b, c) | Contradictions PASS

### Change 20: Waves: V1 schedule, V2 lists, V3 interruption and concurrency rules (S-004)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 5.1-5.4; V2 section 5 lists; V3 "Lockstep and concurrency rules" 1, 3, 4, 8 and "Wave interruption rule"
- **Target**: Base 5.2 (rewritten into three lists recomputed from 4.2 hard edges), new 5.5 Concurrency rules, new 5.6 Wave interruption rule; 5.1 row amendments are made by Changes 7, 9, 28, 51, 59 and checked by Change 48
- **Before**: one "may run today" paragraph
- **After**: three lists (today / waits for #539: 17 items / never waits: 32 items; with SW-05 = 50); 5.5 four concurrency rules re-keyed (V3 OB-04 = merged OB-08; V3 XC-03 draft = merged XC-05); 5.6 interruption rule incl. ORCA-AVAILABLE read-back
- **Provenance tag**: `<!-- Source: Variant V3 (haiku:backend) ... - merged per Change 20 -->` and `<!-- Source: Base (V1) 5.2, modified; Variant V2 (opus:analyzer) section 5 lists; recomputed from the 4.2 hard edges - merged per Change 20 -->`
- **Deviation**: (1) Change 9 names the interruption rule "5.5"; Change 20 and executor step 8 name it 5.6 with concurrency rules at 5.5; followed Change 20. (2) The recomputed "may run today" list is shorter than V1's: SW-06 now waits for XC-02 (Change 37), worker items wait for XC-09 and Q26 (Change 2), SW-03's push waits for Q33 (Change 52). Stated in the list itself. (3) A stray HTML comment briefly placed inside the 5.4 table was removed in the same Change.
- **Validation**: Structural integrity PASS (5.1 to 5.6 in order) | References PASS | Contradictions PASS; list membership re-checked by reachability script in post-merge validation

### Change 21: Boundary and contract node set (S-005)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 TB and K names; V2 TB-3, TB-6; V3 B-EDIT, B-WRITE, B-IDENTITY
- **Target**: Base 4.1 TB table (four rows appended; changed-rows comment above the table); gate nodes ORCA-AVAILABLE, SWEEP-RUNNABLE, TB-GIT-ROW and the GRANT family already added by Changes 6, 9, 13, 16
- **Before**: six TB nodes
- **After**: ten TB nodes (TB-REMOTE, TB-RELAY, TB-EDIT, TB-WRITE added); M-APPROVAL not a node
- **Provenance tag**: `<!-- Changed rows: TB-GIT (Change 4), TB-UPSTREAM (Change 1); new rows TB-REMOTE (V2 TB-3, V3 B-IDENTITY), TB-RELAY (V2 TB-6), TB-EDIT (V3 B-EDIT), TB-WRITE (V3 B-WRITE) - merged per Change 21 -->`
- **Deviation**: the integration edges (TB-REMOTE -> CO-03, CO-04; TB-RELAY -> V2-04, OB-09; TB-EDIT -> every issue write incl. SW-06 and the SW-01 thread reply; TB-WRITE -> SW-12, WA-07, OB-09) were already drawn in the Change 19 table (rows 3, 18, 27, 33, 57, 62, 67, 75, 79, 81, 82, 85, 96). The register blocked-by cells were not extended with the new TB names; the section 4 intro states the edge table is authoritative.
- **Validation**: Structural integrity PASS | References PASS (every TB node used in 4.2 is now defined) | Contradictions PASS

### Change 22: Table conventions: named worktrees, "Observe:", wave column, decision lifetime (S-006)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V2 "Observe:" clauses (verbatim through the id map); V1 named worktrees and "Wave needed by"
- **Target**: Base 0.5 (Observe rule paragraph, inline provenance), all 46 existing acceptance cells in section 2
- **Before**: acceptance cells without an observation method
- **After**: every acceptance cell ends with "Observe: ..."; V2 text verbatim where V2 has the same item, adapted where a merged rule changed it (F3 "caveated texts" not "four texts"; "the PR opened by the PR session"; WA-04's record for V2's WA-05; OB-06 for V2's OB-05; `--repo` added to XC-02's `gh issue view` per the project fork rule); written from the criterion for SW-13, CO-02, CO-04, XC-07, XC-09 (no V2 equivalent). Decision lifetime is carried by Change 60.
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 0.3 and section 2 "Observe:" convention - merged per Change 22 -->`
- **Deviation**: (1) WA-01 (3) "test directory name UNVERIFIED" replaced by `tests/issue_watch/` (OBS-NOW `ls`, diff-analysis SC-24 CONFIRMED), so the criterion and its Observe line agree. (2) Correction to Change 11's text: the grep pattern's pipe inside a table cell is now escaped (`read-only\|changes nothing`) so the SW-02 row does not split. (3) The four new items get their Observe line when their rows are added (Changes 28, 42, 51, 59).
- **Validation**: awk check over register rows: no row without "Observe:" (output above this entry in the run); Structural integrity PASS | References PASS | Contradictions PASS

### Change 23: INV-008 requirement and regression test detail (C-001)
- **Status**: APPLIED
- **Source**: V2 0.1 requirement sentence; V2 SW-02 test detail; V3 "ruling separate from apply; ruling must not await ledger creation"; ADJ line 206 (as cited in the plan, R2-V1 fix 11)
- **Target**: Base 0.1 (requirement paragraph inserted before the Change 4 channels paragraph), SW-02 (1) (V2 test detail merged into the Change 4 wording), SW-01 (1) (ruling recorded on the Codex thread first, ledger row when the ledger exists)
- **Before**: no two-branch requirement sentence; test described as "both keys set once"
- **After**: requirement (a) no repo-config command runs, or (b) owner accepts with caveats in the same PR; test names `core.fsmonitor`, `filter.probe.clean`, `filter.probe.process`, `* filter=probe`; ruling separate from apply and never waits for the ledger; no code fix named
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 0.1 requirement sentence - merged per Change 23 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no fix design added)

### Change 24: Chain to target: root cause column and contract completion rule (C-002)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V2 section 1 "Root cause of the gap" column and "After this first release the chain is still broken at L1 and L3"; V3 "Contract completion rule"
- **Target**: Base 1.1 table (new column after "Evidence", four cells; L1 row cites the existing research package per Change 34), 1.2 (sentence appended), new 1.5
- **Before**: no root-cause column; no completion rule
- **After**: root cause per link (V2 text verbatim); first-release limit sentence; 1.5 with V3's two paragraphs; V1's "What the near-term waves deliver instead" column kept
- **Provenance tag**: `<!-- Source: Variant V3 (haiku:backend) section 1 "Contract completion rule" - merged per Change 24 -->`; column comment above the 1.1 table
- **Deviation**: 1.2 also carries V3's first-release acceptance statement ("aligned contracts, accurate roadmaps and gated reads", V3 section 1) in one sentence with an XC-11 pointer, so the release scope matches XC-11's two scopes (Change 59).
- **Validation**: Structural integrity PASS (1.1 table now 7 columns in header, separator and all four rows) | References PASS | Contradictions PASS (no link claimed built)

### Change 25: Keep the seed-before-live guard flip sequence (C-003; keep)
- **Status**: APPLIED (no text edit needed)
- **Source**: V1 OB-03 -> OB-04 (hard) -> OB-05 -> OB-06
- **Target**: Base OB-03 to OB-06 kept; edge table row 41 types OB-03 -> OB-04 as GATE
- **Before / After**: unchanged sequence; OB-04's content changed only by Change 8; OB-06's XC-05 edge removed by Change 40
- **Provenance tag**: none new (base kept); edge row 41 provenance "V2 e19 (SOFT raised to GATE); V1 4.2"
- **Validation**: `grep '^| 41 | OB-03 | OB-04 | GATE'` = 1 hit (shown in run output) | PASS

### Change 26: Keep seven watcher items and one #450 edit set; add watcher contracts (C-004; keep)
- **Status**: APPLIED (no text edit needed here)
- **Source**: V1 WA-01 to WA-07; V3 launch interface contract and interruption runbook (V3:167, :171)
- **Target**: Base 2.3 kept (7 WA rows; `grep -c '^| WA-0[1-7] | '` = 7); the interface block is filled by Change 58
- **Before / After**: unchanged; V2's split #450 writes not imported ("not made" row 2)
- **Provenance tag**: none new
- **Validation**: PASS

### Change 27: One Coder#477 reply carrying the Q4 line; audit reconciliation (C-005)
- **Status**: APPLIED
- **Source**: V1 CO-01 (2); V3:198 (CO-02 idempotency and operation note)
- **Target**: Base CO-01 kept; CO-03 new criterion (5)
- **Before**: CO-03 had no read-audit rule
- **After**: CO-03 (5): a status read may append a read-audit event but changes no other observable state; no-write criterion reconciled with the read-audit requirement in the design. V2's separate owner one-liner not imported ("not made" row 14)
- **Provenance tag**: inline citation "(V3 CO-02 idempotency note)"; row listed in the 2.4 table's changed-rows comment (Change 65 pass)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 28: #423 decomposition: gated brainstorm, ungated research (C-006)
- **Status**: APPLIED
- **Source**: V2 V2-03 (brainstorm, gated) and V2-04 (research, "runs any time"); ADJ line 710
- **Target**: Base V2-03 criterion (2) (replaced by a "moved to V2-05" note, so V2-03 (3) keeps its number for the id map), V2-04 blocked-by (V2-05 added), new register row V2-05 after V2-04
- **Before**: one gated V2-03 holding both brainstorm and the early research
- **After**: V2-03 brainstorm and design (blocked by V2-02 and XC-05, unchanged); V2-05 research ungated (V2-01 SOFT), in its own master-based worktree `issue-423-research` (PLAN INFERENCE) created by the coordinator with `--agent`, path in the ledger, #423 link only under `GRANT(V2-05,issue-write)`; blocks V2-03 (SOFT) and V2-04 (GATE)
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) V2-04 (research) -> merged V2-05 (new) - merged per Change 28 -->` (listed in the 2.5 table's changed-rows comment, Change 65 pass)
- **Note**: the 5.1 W1 lane and the 1.1 L3 cell are added by Change 41; edges are rows 93, 95, 99, 100 of the Change 19 table.
- **Validation**: Structural integrity PASS | References PASS (V2-05 now defined) | Contradictions PASS

### Change 29: Contract note: early draft, test after merge, full content list (C-007)
- **Status**: APPLIED
- **Source**: V1 XC-05/XC-06/XC-07; V3 "Contract-note content" list (V3:250-267) and the 9-row word mapping table (V3:269-281)
- **Target**: Base XC-05 acceptance (sentence appended before Observe), section 2.6 (content list and mapping table inserted after the XC table, before Risks)
- **Before**: XC-05 listed content in one cell; no word mapping table
- **After**: 16-item content list and 9-row mapping table; V3 ids re-keyed (V3 XC-04 -> XC-06, V3 SW-05 -> XC-04); V1 timing kept (draft W1; test and links after SW-05); never committed in the #539 checkout
- **Provenance tag**: `<!-- Source: Variant V3 (haiku:backend) "Contract-note content" list (V3:250-267), re-keyed ... - merged per Change 29 -->` and `<!-- Source: Variant V3 (haiku:backend) "Required word mapping" table (V3:269-281) - merged per Change 29 -->`
- **Validation**: Structural integrity PASS (lists placed after the XC table; XC-10 and XC-11 rows will be appended to the table above them) | References PASS | Contradictions PASS

- **Correction to the Change 29 entry above**: the first insertion attempt failed (anchor text not found because the XC-09 row has further cells after its acceptance); the entry was written before the failure showed. The insertion was re-done with the anchor `| Q26 | yes (close session) |` and now lands after the XC table (verified: one hit for the list heading). Status stays APPLIED.

### Change 30: Orchestrator session: verified map, V3 roles, evidence handoff and resume (C-008)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 6.4 and 6.5; V2 6.2 worktree map verified by `git worktree list` (SC-27); V3 role contract (read-capture operator, seed-test operator), concurrency rule 8, "Evidence handoff and resume" (V3:547-551), guardrail 1 and the map note (V3:500)
- **Target**: Base 5.4 (rebuilt: V2 verified rows incl. `issue-394-launch-level-hook`, plus V1 proposed rows, new "Rule" column), 6.2 (paragraph appended), 6.3 (Live reader row split into Read-capture operator and Seed-test operator; PR session row already added by Change 1), new 6.10 (worker brief, handoff, resume)
- **Before**: V1 map without paths, heads or rules; one "Live reader" role; no handoff or resume rule
- **After**: one map with real paths and heads for existing worktrees, PLAN INFERENCE names for new ones, a rule per row; two operator roles with separate grants `GRANT(XC-03,live-read)`, `GRANT(XC-04,live-read)`, `GRANT(OB-04,live-read)`, `GRANT(OB-03,seeded-write)`; a launch receipt or self-reported done is not acceptance
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 6.2 verified rows ... - merged per Change 30 -->`, `<!-- Source: Variant V3 (haiku:backend) "Evidence handoff and resume" ... - merged per Change 30 -->`
- **Deviation**: (1) 5.4 also gains the `issue-423-research` row (V2-05, Change 28) and SW-14 in `sweep-534-followups` (Change 42), and XC-10 in "ledger only" (Change 51), so the map lists every item once; (2) V3's role letters are not used (S-006); (3) the worker-brief commit requirement of Change 15 is placed in 6.10 as the plan says.
- **Validation**: `grep -i 'live reader'` after the edit lists the remaining hits (run output above); Structural integrity PASS (5.4 table 6 columns) | References PASS | Contradictions PASS

### Change 31: Invariants section: severity map, check column, load gap, gate (C-009)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 7.1 severity map; V2 7.1 "how a reviewer checks it" column (I-xx rows, re-keyed) and V2 7.4 gap row; V3 XC-08 gate (carried by XC-11, Change 59)
- **Target**: Base 7.2 (new "Check" column, all 19 rows), 7.1 header (pointer to the R25-INV appendix), 7.1 INV-032 row
- **Before**: no check method per invariant; INV-032 gap not stated
- **After**: each 7.2 row has a check (V2 command or record where V2 has the invariant, otherwise written from the guard); 7.1 says R25-INV rows live in the appendix; INV-032 is an explicit gap
- **Provenance tag**: `<!-- Changed column: "Check" added (Variant V2 (opus:analyzer) 7.1 ...) - merged per Change 31 -->`
- **Deviation**: 7.1 already had an INV-032 row; it was amended into the explicit-gap row instead of adding a duplicate row with the same id.
- **Validation**: Structural integrity PASS (7.2 header, separator and rows now 5 columns) | References PASS | Contradictions PASS

### Change 32: Keep V1's owner-decision gate mapping (C-010; keep)
- **Status**: APPLIED (no text edit needed)
- **Source**: V1 section 3 Gates column
- **Target**: Base section 3 kept; V2's and V3's wider gate sets not imported
- **Before / After**: unchanged (Q11 gates nothing; Q21 gates SW-10; #409 pass gated by Q8 and Q16, not Q2). The Change 19 table drops V2 e29 (Q2 to the #409 pass) and the Q9 and Q18 parts of V2 e6 and e48 on this basis
- **Provenance tag**: none new
- **Validation**: `grep '^| Q2 |'` Gates cell unchanged except the Change 3 default wording | PASS

### Change 33: Evidence basis: OBS-NOW convention (C-011)
- **Status**: APPLIED
- **Source**: V2 0.2-0.3 OBS-NOW; DEBATE `diff-analysis.md` SC-nn; probe R25-INV-026; plan naming conventions 1-5 (executor step 3)
- **Target**: Base 0.2 (new DEBATE source row; WC row notes the plan's re-checked lines; markers OBS-NOW, UNRESOLVED-EXTERNAL, two id spaces, owner questions, edge kinds and gate nodes, new ids, provenance comments), 0.3 Source cells of seven rows (OBS-NOW evidence with SC id or probe id) and a changed-rows comment
- **Before**: V1's Glob-based statements without per-row evidence; no OBS-NOW marker
- **After**: every 0.3 row where a check ran cites the command and its SC or probe id (dated 2026-11-13 in the marker definition)
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 0.2-0.3 OBS-NOW convention; refactor-plan naming conventions 1-5 - merged per Change 33 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 34: Both task packages exist (X-001; fixes D1)
- **Status**: APPLIED
- **Source**: V2 L1 row and 6.1; V3 section 6 inputs; SC-01, SC-02; plan `ls -d` re-run
- **Target**: Base 0.4 item 5 (replaced), 6.1 (new input row), SW-12, SW-13 (new (4)), WA-07 (new (6)) ("read the existing package first", V3 rule 10); the 1.1 L1 row already cites the package (Change 24)
- **Before**: "not found in this checkout ... UNVERIFIED"
- **After**: both packages exist (contents not read); later phases read them first
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) L1 row and 6.1; DEBATE SC-01, SC-02; plan re-check - merged per Change 34 -->`
- **Validation**: `grep -c 'not found in this checkout'` = 0 (run output above) | References PASS | Contradictions PASS

### Change 35: JOIN never runs the unfixed sweep (X-002; fixes D2)
- **Status**: APPLIED
- **Source**: V2 TB-1 -> XC-05 edge and R-XC4 (re-keyed to merged XC-04)
- **Target**: Base XC-04 blocked-by (TB-GIT, ORCA-AVAILABLE, `GRANT(XC-04,live-read)` appended to the SWEEP-RUNNABLE, SW-05, TB-GIT-ROW of Changes 6, 7, 16); edge table rows 105-106 (built in Change 19); wave move done in Change 7
- **Before**: XC-04 blocked by Q24 and LIVE only, in W1
- **After**: XC-04 blocked by Q24, LIVE, SWEEP-RUNNABLE, SW-05, TB-GIT-ROW, TB-GIT, ORCA-AVAILABLE and its live-read grant; runs in W3 on master code
- **Provenance tag**: listed in the 2.6 table's changed-rows comment (Change 65 pass): "XC-04 (Changes 7, 16, 35)"
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (`grep 'XC-04'` in the 5.1 W1 row shows only "(XC-04 moved to W3, Change 7)")

### Change 36: CAP stays early and separate from JOIN (X-003)
- **Status**: APPLIED
- **Source**: V1 XC-03 and V2 XC-06; ADJ graph `CAP -> {...}` with no `P539m` (SC-35); R25-INV-022
- **Target**: Base XC-03 blocked-by (ORCA-AVAILABLE and `GRANT(XC-03,live-read)` added; explicit "no TB-GIT"); XC-03 stays in W1
- **Before**: blocked by Q24 and LIVE
- **After**: blocked by Q24, LIVE, ORCA-AVAILABLE and its live-read grant (XC-10 added by Change 51); no TB-GIT edge; V3's merge gate not imported
- **Provenance tag**: listed in the 2.6 table's changed-rows comment
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 37: #534 table written now; source edits after merge (X-004)
- **Status**: APPLIED
- **Source**: V1 SW-06 (W0, "logged there now"); V2 Weak point W1 (ADJ A-004 against A-005, SC-36)
- **Target**: Base SW-06 (new criterion (4); blocked-by "none" -> "XC-02 (pin rule); GRANT(SW-06,issue-write)"), 2.1 Weak points block (W1 inserted with the ADJ tension flagged by a contradiction marker); SW-07 and SW-08 unchanged (post-merge)
- **Before**: SW-06 blocked by nothing; no record of the ADJ tension
- **After**: SW-06 posted by the single editor under the pin rule and its grant, outside the five-link order; W1 states the ADJ contradiction and the settling evidence, re-keyed (V2 SW-07 = merged SW-06, V2 SW-06 = merged SW-05)
- **Provenance tag**: inline "(... Variant V2 W1, merged per Change 37)" inside the 2.1 Weak points block (block comment from Change 17)
- **Validation**: Structural integrity PASS | References PASS | Contradictions: the ADJ tension is carried with a contradiction marker, not resolved silently

### Change 38: Keep the hard cross-issue order (X-005; keep)
- **Status**: APPLIED (no text edit needed)
- **Source**: V1 XC-02 (3) and the chain WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01; ADJ line 442
- **Target**: Base kept; edges typed PROC in the Change 19 table (rows 26, 56, 77, 84); skip rule from Change 3 (XC-02 (6))
- **Before / After**: unchanged order; V2's soft order not imported ("not made" row 1)
- **Provenance tag**: none new
- **Validation**: PASS

### Change 39: Keep one #450 edit set (X-006; keep)
- **Status**: APPLIED (no text edit needed)
- **Source**: V1 WA-02
- **Target**: Base WA-02 kept (one write, one `updatedAt` re-read); defaulted edits omitted per Change 3 (WA-02 (7))
- **Before / After**: unchanged; V2's three #450 writes not imported ("not made" row 2); R25-INV-025 residual accepted
- **Provenance tag**: none new
- **Validation**: PASS

### Change 40: The guard flip does not wait for the note draft (X-007)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V2 Weak point W2 and OB-05 blocked-by
- **Target**: Base OB-06 blocked-by ("XC-05 (for (e))" removed; Q23 added, matching OB-06's Q column and edge row 46), XC-05 blocks cell ("OB-06 (e)" removed), W2 gate cell in 5.1 ("XC-05 draft" removed), 2.2 Weak points (W2 inserted, re-keyed); 4.2 has no XC-05 -> OB-06 row (Change 19); OB-06 (e) kept disjunctive
- **Before**: OB-06 waited for the XC-05 draft
- **After**: the flip is independent of the note draft; (e) may be met in the observer spec
- **Provenance tag**: inline "(... Variant V2 W2, merged per Change 40)" in the 2.2 Weak points block
- **Deviation**: the XC-05 "blocks" cell was also corrected (plan lists only OB-06's side), so both ends of the removed edge agree.
- **Validation**: `grep 'XC-05 (for (e))|XC-05 draft;'` = 0 hits and edge-table rows `| XC-05 | OB-06 |` = 0 (run output above) | PASS

### Change 41: #423 research may start early (X-008)
- **Status**: APPLIED
- **Source**: V2 V2-04 (merged V2-05); ADJ line 710
- **Target**: 5.1 W1 lanes (new lane "L-research (new `issue-423-research`): V2-05") and W1 exit (V2-05 path or deferral recorded); 1.1 L3 row "near-term" cell (mentions V2-05); the item itself was added by Change 28
- **Before**: research held inside the gated V2-03
- **After**: V2-05 scheduled from W1 on its own lane
- **Provenance tag**: listed in the 5.1 table's changed-rows comment (Change 65 pass) and in the 1.1 column comment (Change 24)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 42: Q14's gate: capture recorded versus `working` class restored (X-009)
- **Status**: APPLIED
- **Source**: V2 Weak point W5, V2 SW-13 (conditional; merged SW-14), V2 N3
- **Target**: section 3 Q14 row (widened; default "capture recorded" labelled PLAN INFERENCE default; gates SW-14), V2-02 (3) (replaced) and blocked-by (SW-14 conditional), new register row SW-14 after SW-13, 2.5 Weak points (W5 inserted)
- **Before**: V2-02 (3) read the gate as "class restored" without an item to restore it
- **After**: V2-02 passes only if every part of the owner's Q14 answer is met; SW-14 (blocked by XC-03, SW-05, SW-06, Q14; PR under Q25 and `GRANT(SW-14,pr-submit)`; runs in `sweep-534-followups`, PLAN INFERENCE; undo revert) exists for the "restored" reading; wave W4 set by Change 48
- **Provenance tag**: inline "(... Variant V2 W5, merged per Change 42)"; SW-14 listed in the 2.1 table's changed-rows comment
- **Validation**: `grep -c '^| SW-14 | '` = 1 (run output above) | References PASS | Contradictions PASS

### Change 43: Keep the "Phase 2" contradiction marker (X-010; keep)
- **Status**: APPLIED (no text edit needed)
- **Source**: V1 1.4
- **Target**: Base 1.4 kept; SW-12 and SW-13 stay separate; the 1.1 L1 gate names "SW-13 (#444 design)" and the L2 row names "SW-12 (research-report Phases 2 to 5)"; V2's "SW-12 (Phase 2 of #339)" wording not imported ("not made" row 15)
- **Before / After**: unchanged
- **Provenance tag**: none new
- **Validation**: `grep -c 'CONTRADICTION MARKER (numbering)'` = 1 | PASS

### Change 44: Outward writes: per-PR, per-action grants replace the blanket rule (X-011; fixes D5)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: debate consensus; `WORKER-CONTRACT.md:243`; project CLAUDE.md (`/sc:pr-submit --monitor 3` pushes, replies and resolves without asking)
- **Target**: Base XC-02 (4) (replaced), 6.4 rule 2 (new wording appended), 6.9 bullet 1 (replaced), 6.3 Owner row (done in Change 13) and Coordinator row ("posts without owner approval" -> "posts without a matching grant row")
- **Before**: "every post is owner-approved" / "never post, reply or merge without approval" beside a mandated tool that pushes, replies and resolves without asking
- **After**: the plan's wording: each outward action granted separately; a `pr-submit` grant covers only its listed writes on that PR; merges, issue posts, the INV-008 ruling reply and live tests each need their own grant; the coordinator never merges and never posts without a matching grant
- **Provenance tag**: inline "(X-011)" in 6.4 rule 2; rows listed in the changed-rows comments (Change 65 pass)
- **Deviation**: also replaced the W0 wave cell "owner-approved post" for SW-06 with its grant and pin rule, and the Coordinator row wording, so no blanket-approval phrase is left (re-grep: remaining "owner-approved" hits are an owner-approved Run, an owner-approved reinstall, and a sweep runbook phrase, none a blanket post rule).
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 45: Ledger and program files never in the #539 checkout (X-012; fixes D3)
- **Status**: APPLIED (edits made in Change 2; verified here)
- **Source**: V3 "no extra sidecar is placed in #539"; V1 XC risk (V1:332); Change 2
- **Target**: Base XC-01 Location and 6.1 Decision ledger row (both rewritten in Change 2)
- **Before**: PLAN INFERENCE ledger path `.dev/brainstorms/.../decision-ledger.md` under the #539 checkout
- **After**: "the home and branch named in Q26"; never the #539 checkout
- **Provenance tag**: as Change 2
- **Validation**: `grep -c 'decision-ledger.md'` = 0 | PASS

### Change 46: Who merges #541 (X-013)
- **Status**: APPLIED
- **Source**: V1 SW-04 "owner merges"; V3 "authorized maintainer"
- **Target**: Base SW-04 blocked-by (replaced), 4.1 OWNER-MERGE note (amended); edge row 11 drawn in Change 19
- **Before**: "none (owner merges)"
- **After**: "`GRANT(SW-04,merge)`: the owner merges, or records approval for a named merger"; V2's "not owner-gated by any source" not imported
- **Provenance tag**: inline "(X-013; merged per Change 46)" in 4.1
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 47: No new coordinator work clock; cadence per Change 10 (X-014)
- **Status**: APPLIED (carried by Change 10)
- **Source**: V1 6.6; `WORKER-CONTRACT.md:288`
- **Target**: Base 6.6 per Change 10; V3's 5-minute ledger reconciliation tick not imported ("not made" row 3)
- **Before / After**: the 6.6 cadence record states that no row is a new work clock for the coordinator (X-014)
- **Provenance tag**: as Change 10
- **Validation**: `grep -c 'reconciliation every 5 minutes'` = 0 | PASS

### Change 48: Reconcile register, graph and waves (X-015; fixes D6)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: debate consensus; IC-V1-1, IC-V1-2
- **Target**: Base 5.1 rows W0 to W5 (with a changed-rows comment), 5.3 (two serial rows added), XC-03 "blocks" cell
- **Before**: W1 scheduled XC-04 before the merge; W2's OB-06 gate named the XC-05 draft; no slot for XC-10, V2-05, SW-14, XC-11; XC-03 "blocks SW-06" pointed from W1 back to W0
- **After**: re-checked every wave row against the 4.2 table by hand (the scripted check runs in post-merge validation (f)): W0 gains XC-10 (before XC-09 and SW-03) and XC-01 -> XC-02 -> SW-06 serial; W1 loses XC-04, gains V2-05 and the serial pairs XC-05 -> CO-02 -> CO-01; W2's OB-06 gate has no XC-05 and SW-05 names its grants; W3 gains SWEEP-RUNNABLE, XC-04 before XC-07, XC-06 before XC-07 and XC-11 (first-release) last; W4 gains SW-14 (conditional) before V2-02; W5 gains V2-05 in V2-04's gate, SW-12 before V2-04 when relaying, and XC-11 end-to-end last. 5.3 gains the JOIN chain and the intake chain.
- **Provenance tag**: `<!-- Changed rows: W0 ... W5 ... - re-checked against the 4.2 edge table per Change 48 -->`
- **Deviation**: (1) XC-10 and XC-11 enter the waves here, before Changes 51 and 59 add their register rows (the plan lists them as known fixes of this Change). (2) The XC-03 "blocks" cell now marks the SW-06 `working`-class row, the XC-05 attention row and OB-05 as SOFT and adds SW-14 and OB-09 (hard edges from the table), so the register and the edge table agree and no hard edge points from W1 back to W0. V2's and V3's own schedule mismatches are not imported ("not made" row 21).
- **Validation**: scripted in post-merge validation (f)

### Change 49: `/sc:sweep` availability caveat, corrected (A-001; keep and fix)
- **Status**: APPLIED (carried by Change 6)
- **Source**: V1 6.6 and 7.3 (no `/sc:sweep` on master before SW-05; SC-06)
- **Target**: Base 6.6 and 7.3 per Change 6
- **Before**: "`superclaude install` or `make sync-dev`" made `/sc:sweep` available
- **After**: SWEEP-RUNNABLE replaces the install claim; V1's availability caveat kept
- **Provenance tag**: as Change 6
- **Validation**: `grep -c 'the ledger records the install step'` = 0 | PASS

### Change 50: The mandated PR tool and owner approval (A-002; part of D5)
- **Status**: APPLIED
- **Source**: debate consensus (same root as X-011)
- **Target**: section 3, new "Authority not granted by these questions" list (created here; Change 60 adds V3's entries and the runbook and lifetime blocks)
- **Before**: no list
- **After**: "A `pr-submit` grant on one PR does not authorize a merge, an issue write, the INV-008 ruling reply, or the tool on any other PR"
- **Provenance tag**: `<!-- Source: Debate consensus A-002 (NEITHER) - merged per Change 50 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 51: W0 intake item XC-10 confirms the live reader (A-003)
- **Status**: APPLIED
- **Source**: debate consensus (A-003, A-004, A-007; R25-INV-002, R25-INV-009); V3 W0 exit
- **Target**: new register row XC-10 after XC-09 (2.6); blocked-by cells of XC-09 (XC-10 (3), ORCA-AVAILABLE), SW-02, SW-03, SW-05 (XC-10 (2); SW-05 also TB-GIT, Q28, `GRANT(SW-05,merge)` to match edge rows 15-17), XC-03 and OB-03 (XC-10 (1), (4); OB-03 also `GRANT(OB-03,seeded-write)` to match edge row 40); 5.1 W0 lane and exit (done in Change 48)
- **Before**: ADJ's Q24 default names "the 409 session" with no liveness check; no named #539 author; no intake
- **After**: XC-10 records seven intake parts or holds each with a reason; Q: Q24, Q25, Q26, Q31, Q33; runs in the ledger only
- **Provenance tag**: `<!-- Source: Debate consensus (A-003, A-004, A-007), R25-INV-002, R25-INV-009 -> XC-10 (new) - merged per Change 51 -->` (listed in the 2.6 changed-rows comment, Change 65 pass)
- **Validation**: XC-10 row directly follows XC-09 inside the table (run output above) | References PASS | Contradictions PASS

### Change 52: The owner names the #539 author session (A-004)
- **Status**: APPLIED
- **Source**: debate consensus; V1 6.3 "#539 author (UNVERIFIED which)"
- **Target**: Base 6.3 #539 author row ("UNVERIFIED which" replaced), SW-02, SW-03, SW-05 blocked-by (Q33 appended; SW-02 also Q27 for its plan package), section 3 new Q33 row
- **Before**: the critical path Q1 -> ruling -> fix -> merge had no named actor
- **After**: "named by the owner at W0 (Q33); a top-level session, not a worker, because it pushes"; Q33 default: SW-02, SW-03 and SW-05 pushes are held; V2's "the worker" not imported
- **Provenance tag**: listed in the 6.3 and 2.1 changed-rows comments (Change 65 pass)
- **Validation**: Q rows present in order Q1..Q33 (run output above) | References PASS | Contradictions PASS (the 5.4 map row keeps "UNVERIFIED which; named at W0, Q33", consistent)

### Change 53: Program files out of #539; named-file staging (A-005)
- **Status**: APPLIED
- **Source**: debate consensus; SC-42; R25-INV-027 (`/sc:pr-submit` stages only changed paths)
- **Target**: Base 6.4 new rule (numbered 14 now; Change 66 renumbers when it inserts the build-string rule as 13)
- **Before**: no staging rule for the #539 checkout
- **After**: named-file staging only; the only `.dev/tasks/` package there is SW-02's own under Q27; no program artifact created there; existing untracked files neither deleted nor moved
- **Provenance tag**: inline "(A-005; R25-INV-027)"; rule listed in the 6.4 provenance comment (Change 66)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 54: Owner latency is the critical path; per-wave question batches (A-006)
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: V1 "Wave needed by" column; V2 Q1 "longest-lead item"; V3 "Decision runbook"
- **Target**: section 3 intro (ask-order paragraph appended; the old "Q1 to Q4 first" sentence reworded to point at it), 5.1 W0 L-owner lane, XC-01 (1) and (2); "Wave needed by" cells for Q25 to Q33 were filled when each row was added (Changes 1-15, 52)
- **Before**: "Ask in this order: Q1 to Q4 first"
- **After**: "Q1 first; then Q33, Q26, Q2, Q3, Q4, Q25, Q31; then each wave's questions; Q27, Q28, Q29, Q30, Q32 when their item is next"
- **Provenance tag**: `<!-- Source: Base (V1) "Wave needed by" column; Variant V2 Q1 "longest-lead item"; Variant V3 "Decision runbook" - merged per Change 54 -->`
- **Deviation**: the plan says "append"; the base's own ask-order sentence and the W0 lane and XC-01 (2) were also reworded, because leaving "Q1 to Q4 first" beside the new order would contradict it. XC-01 (1) now lists Q1 to Q33.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 55: ADJ live facts are historical; re-read at W0 and each gate (A-007)
- **Status**: APPLIED
- **Source**: V3 (ADJ facts treated as historical; "Fresh correct-fork PR evidence"; V3:466); probe R25-INV-026
- **Target**: Base 0.3 heading, all six per-system "Current state" labels (2.1 to 2.6), 6.1 Live state row, 2.1 first bullet (probe re-read appended with an inline provenance comment); also 6.8 "Rows for Q1 to Q33" (count follow-up of Change 54)
- **Before**: ADJ facts presented as current
- **After**: labelled "as of ADJ, 2026-11-13; historical: re-read at W0 by XC-10 and at each gate"; #539 OPEN, head `873599d59`, 1003 files, UNSTABLE; #541 OPEN, head `779e58b17`, CLEAN (as of 2026-11-13)
- **Provenance tag**: `<!-- Source: invariant-probe R25-INV-026 - merged per Change 55 -->`
- **Validation**: `grep -c 'as of ADJ, 2026-11-13'` = 7 expected (0.3 heading + six sections); run output above | PASS

### Change 56: Edge kinds with evidence; PROC for the publication order (U-004)
- **Status**: APPLIED (with Change 19)
- **Source**: V2 0.3 kind definitions; V2 4.2
- **Target**: Base section 4 intro (V1's `->`/`~>` legend replaced by the six kinds; `~>` = SOFT); applied in the Change 19 edit
- **Before**: two arrow kinds
- **After**: FILE, PIN, GATE, DEC, PROC, SOFT; SOFT never blocks a wave; the cross-issue order typed PROC
- **Provenance tag**: `<!-- Source: Variant V2 (opus:analyzer) 0.3 edge kinds - merged per Change 56 (applied with Change 19) -->`
- **Validation**: PASS

### Change 57: Weak points W1 to W6 (U-005)
- **Status**: APPLIED
- **Source**: V2 Weak points W1 to W6 (W7, W8 withdrawn)
- **Target**: "Weak points" sub-blocks (Change 17): W1 in 2.1 (Change 37), W2 and W3 in 2.2 (W2 via Change 40), W6 in 2.3, W5 in 2.5 (Change 42), W4 in 2.6; 2.4 states that none is carried (W7 withdrawn)
- **Before**: skeleton placeholders
- **After**: each weak point re-keyed through the id map (e.g. V2 SW-06 -> SW-05, OB-05 -> OB-06, WA-04 -> WA-02, WA-05 -> WA-04, XC-04 -> XC-05, XC-06 -> XC-03, SW-13 -> SW-14) and naming the evidence that would settle it
- **Provenance tag**: inline "(... Variant V2 Wn, merged per Change nn)" on each bullet, under the Change 17 block comment
- **Validation**: placeholders left `grep -c 'filled by Change 57'` = 0; each of W1..W6 appears once (run output above) | PASS

### Change 58: Interface, failure, retry and idempotency contracts (U-010)
- **Status**: APPLIED
- **Source**: V3 sweep (V3:116-124), snapshot and question read (:142-148), launch, store, interruption and live-test blocks (:167-175), remote read and failure (:194-200), catalogue, operational and communication contracts (:218-226), issue edit (:283), PR merge (:285)
- **Target**: "Interface contracts" sub-blocks of 2.1 to 2.6 (Change 17 skeleton)
- **Before**: placeholders
- **After**: per-system contracts with failure, retry and idempotency; re-keyed through the id map (V3 SW-07 -> SW-12, OB-02 -> OB-03/OB-04, WA-05 -> WA-07, CO-02 -> CO-03, V2-03 -> V2-03 (3)/V2-04); the PR-merge writer is "the owner or a named merger under `GRANT(<item>,merge)`"; PR submission named as the PR session's
- **Provenance tag**: Change 17 block comment `<!-- Source: Variant V3 (haiku:backend) interface, failure and runbook blocks - merged per Change 17 (skeleton) and Change 58 (content) -->` plus the V3 line range in each block label
- **Validation**: `grep -c 'filled by Change 5'` = 0 (run output above) | References PASS | Contradictions PASS

### Change 59: XC-11 independent invariant and coverage gate, two scopes (U-011)
- **Status**: APPLIED
- **Source**: V3 XC-08 and V3:248
- **Target**: new register row XC-11 after XC-10 (2.6); 5.1 W3 exit (first-release scope) and W5 (end-to-end scope) done in Change 48; edge rows 122-123 drawn in Change 19
- **Before**: no independent gate item
- **After**: XC-11 with two scopes; INV-008 unresolved means FAIL; first-release PASS never relabelled end-to-end; CO-03 not-selected under Q3 = close recorded as such; runs in an independent read-only context
- **Provenance tag**: `<!-- Source: Variant V3 (haiku:backend) XC-08 -> XC-11 (new) - merged per Change 59 -->` (listed in the 2.6 changed-rows comment, Change 65 pass)
- **Validation**: XC-10 and XC-11 rows contiguous in the XC table (run output above) | References PASS | Contradictions PASS

### Change 60: Decision runbook, lifetime and authority not granted (U-012)
- **Status**: APPLIED
- **Source**: V3:319-323
- **Target**: section 3 after the table and the "What the first four answers do" paragraph: "Decision runbook", "Decision lifetime", "Authority not granted" (V3's five entries plus Q25, Q28, Q30, Q31; Change 50's entry kept); 7.4 new edge case 15 (executor step 10)
- **Before**: no runbook, lifetime or authority limits
- **After**: one question at a time, no assent by recommendation; a changed answer voids drafts, plans and dependent GRANT rows; nine authority limits plus the A-002 entry
- **Provenance tag**: `<!-- Source: Variant V3 (haiku:backend) section 3 "Decision runbook", "Decision lifetime", "Authority not granted" (V3:319-323), extended - merged per Change 60 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 61: Appendix: old-to-new id map, and its validation (X-015, S-002, R25-INV-021)
- **Status**: APPLIED
- **Source**: the plan's map table (built from V2 and V3 register ids and titles)
- **Target**: new H2 "Appendix: old-to-new id map" appended after section 7 (written to `/tmp/merge-appendix-61.md`, then `cat >>`)
- **Before**: no map
- **After**: the plan's 48-row map verbatim, the XC-10 note and the validation definition (a)-(d); 4.3 item 7 points to it
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 61 (built from the V2 and V3 register ids and titles) - merged per Change 61 -->`
- **Validation**: map checks (a)-(d) are run in post-merge validation (b)

### Change 62: Appendix: invariant coverage table R25-INV-001 to R25-INV-028
- **Status**: APPLIED
- **Source**: `invariant-probe.md` and Changes 1-16
- **Target**: new H2 "Appendix: invariant coverage R25-INV-001 to R25-INV-028" (written to `/tmp/merge-appendix-62.md`, then `cat >>`); 7.1 points to it (Change 31)
- **Before**: no coverage table for this debate's probe
- **After**: 28 rows `Id | Severity | Status after merge | Rule | Sections and items`; rows 001-016 point to Changes 1-16; 017-028 record where the merged spec keeps them; R25-INV-018 = ADJ INV-008, UNRESOLVED-EXTERNAL with the owner
- **Provenance tag**: `<!-- Source: DEBATE invariant-probe.md (Round 2.5) and Changes 1-16 of refactor-plan.md - merged per Change 62 -->`
- **Note**: appended now; Change 63 inserts the owner-questions appendix before it so the required appendix order holds.
- **Validation**: 28 R25-INV rows (run output above); section pointers checked in post-merge validation (d)

### Change 63: Appendix: owner questions Q1 to Q24 and Q25 to Q33
- **Status**: APPLIED
- **Source**: section 3 of this spec; the plan's label mapping
- **Target**: new H2 "Appendix: owner questions Q1-Q24 (from the adjudicated doc) and Q25-Q33 (new from this debate)", inserted with Edit before the invariant-coverage appendix so the executor's appendix order holds
- **Before**: none
- **After**: index of 33 rows `Q | one-line title | origin | section 3 row`; no answer, default or recommendation restated (single source of truth); Round 3 labels N1-N10 mapped, not carried as ids
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 63 (index only; section 3 is the single source ...) - merged per Change 63 -->`
- **Validation**: appendix order = id map, owner questions, invariant coverage (run output above) | PASS

### Change 64: Appendix: provenance and deviations
- **Status**: APPLIED
- **Source**: the plan's content items (1)-(6)
- **Target**: new H2 "Appendix: provenance and deviations" (written to `/tmp/merge-appendix-64.md`, then `cat >>`)
- **Before**: none
- **After**: the six plan items, plus (7) a pointer to this log for per-Change deviations; item 1 keeps "not verified" as in the plan
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 64 - merged per Change 64 -->`
- **Validation**: H2 order: eight base sections then the four appendices (run output above) | PASS

### Change 65: Frontmatter, provenance header, Part A label, INV-008 first
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: the plan; template Section 6 (Merged Output Provenance Format)
- **Target**: Base lines 1-17 (frontmatter, header, H1, 0.1), 6.1 "This spec" row; section-level provenance pass over every H2 and H3 and the changed-rows comments above each changed table
- **Before**: V1 frontmatter (`variant: 1`, status "INV-008 UNRESOLVED"); no provenance header
- **After**: `variant: merged`; status "BLOCKED_BY_INVARIANTS (INV-008 UNRESOLVED-EXTERNAL; owner decision Q1; carried, not waived)"; `base`, `merged_from`, `plan`, `merged` fields; four header comments (Provenance, Base, Merge date, Plan); the Part A line; 0.1 stays first, heading "(UNRESOLVED-EXTERNAL)", first sentence names owner decision Q1, keeps "does **not** specify the code fix", states the requirement and F1/F2/F3, and adds "R25-INV-018 in this debate's probe is the same finding; it stays UNRESOLVED-EXTERNAL with the owner"; 6.1 points at `merged-spec.md`; `Source: Base (original)` on 0.6, 1.3, 1.4, 6.7, 7.5 and `Base (original, modified) - reason` on the changed sections; changed-rows comments above the six register tables, the section 3, 6.1, 6.3, 6.5, 7.1, 7.3, 5.3 and 0.2 tables
- **Provenance tag**: the header block itself
- **Deviation**: the plan says to add the header comments "after the H1"; template Section 6 and executor step 2 put them at the top after the frontmatter, before the H1. Followed the template and step 2; the Part A line is after the H1 as the plan says.
- **Validation**: counts of Source tags and changed-rows comments in the run output above | PASS

### Change 66: Project rules and honest-limit statements in one place
- **Status**: APPLIED-WITH-DEVIATION
- **Source**: project CLAUDE.md (fork-only PRs, upstream ban, `.claude/` staging, `.dev/tasks/` staging, Orca worktrees); WC-13; V2 XC-09 (build-string rule)
- **Target**: Base 6.4 (consolidated; provenance comment), 0.4 (item 7 added; item 1 now says "stages nothing")
- **Before**: project rules spread across rules 2, 3 and 4 with partial wording; no build-string rule; 0.4 silent on L1 and L2
- **After**: 6.4 states once each: rule 2 PRs only via `/sc:pr-submit --monitor 3` to the fork, every `gh` call names the fork (or `IronbellyOrg/Coder` for #477), no upstream interaction of any kind, URL checked and a wrong URL stops the session; rule 3 never stage `.claude/` (only `.claude/settings.json` tracked; edit `src/superclaude/` and run `make sync-dev`), `.dev/tasks/` always staged and staging is not committing; rule 4 Orca-only worktrees at the default location (`--agent` or `worker-start`), never `EnterWorktree`, raw `git worktree add`, `.claude/worktrees/` or `.dev/worktrees/`, and WC-13; new rule 13 the Orca build string at every live record's exit (V2 XC-09). Rule 1 now says UNRESOLVED-EXTERNAL. 0.4 keeps "It changes nothing ... posts nothing" and adds "No section claims that the watcher-to-orchestrator link (L1) or the orchestrator-manages-work link (L2) exists."
- **Provenance tag**: `<!-- Source: Base (original, modified) - project rules consolidated so each is stated once (Change 66); ... -->`
- **Deviation**: (1) the commit rule (Change 15) and the #539-checkout rule (Change 53) were renumbered 14 and 15 so the build-string rule is 13 as the Change 61 map says; references in 6.3 and 6.10 were updated. (2) 0.4 item 1 gained "stages nothing" so acceptance check A10 (changes, posts and stages nothing) holds; the plan did not list that word.
- **Validation**: Structural integrity PASS | References PASS (`grep '6.4 rule 1[345]'` re-checked) | Contradictions PASS

## Post-Merge Validation

All checks are read-only. Scripts: `/tmp/merge-validate/validate.py` (checks a-f, h) and `/tmp/merge-validate/roots.py` (4.3 roots and sinks), run with `uv run --no-project python -I <script> merged-spec.md`; greps for the map and contradiction checks as shown.

### Run 1 (2026-11-13, after Change 66)
- Script crashed (IndexError): the register parser also read the appendix id-map rows (53 "register" rows). Script bug; fixed by parsing section 2 only.

### Run 2
- (a) PASS; (c) PASS (50 of 50 items in the edge table); (d) PASS (28 R25 rows; every section pointer is an existing H3); (e) PASS (33 Q referenced, 33 appendix rows, 33 section 3 rows); (h) PASS.
- (b) FAIL: (1) real defect: edge row 60 named V2's id `OB-10` in its evidence text outside the map; fixed in the spec ("V2's reviewer-asks item is folded into OB-09; appendix id map"). (2) script bug: it split `GRANT(SW-01,thread-reply)` on the comma; fixed to split only on commas outside parentheses.
- (f) FAIL: script bug: the serial-cell parser split sentences only on ". ", so the W5 cell "WA-07 after ...; V2-04 after ...; XC-11 end-to-end after ..." was read as one sentence. Fixed to split on ";" too. No spec change.

### Run 3 (final)
```
(a) headings: 56 real headings, H2=12, H3=43
register rows: 50
(b) ids used outside map/comments: 50; register endpoints checked: 296
edge rows: 123
(c) items in edge table: 50 of 50
(d) R25 rows: 28; existing H3 numbers: 43
(e) Q referenced: 33; appendix rows 33; section 3 rows 33
(f) hard item-to-item edge pairs checked: 113; W0..W5 assignment parsed from the 5.1 lanes column (W5 from its gate column)
(h) first H3: line 28 '0.1 First action: INV-008 (UNRESOLVED-EXTERNAL)'
CHECK a..f, h: PASS
```
- `roots.py`: roots [OB-01, OB-02, SW-01, SW-04, XC-01, XC-08, XC-10]; sinks [CO-03, CO-04, OB-07, SW-08, SW-11, WA-05, WA-06, XC-11]. 4.3 item 3 had listed WA-01, WA-03 and XC-05 as roots, but edge row 119 (XC-09 -> them) is hard; 4.3 item 3 was corrected. Sinks matched. Final validate run after the fix: all PASS.

### Check details
- **(a) Heading hierarchy**: PASS. One H1; no level jump; the eight base H2s in order, then the four appendices in the executor's order; H3 numbers strictly increasing inside each H2 (new H3s 1.5, 4.4, 4.5, 5.5, 5.6, 6.10; no existing H3 renumbered).
- **(b) Ids defined; endpoints exist**: PASS. Every `(SW|OB|WA|CO|V2|XC)-nn` outside the id-map appendix and HTML comments is one of the 50 defined ids; the defined set equals V1's 46 plus SW-14, V2-05, XC-10, XC-11; 296 register blocked-by/blocks tokens and every edge-table From/To resolve to an item, Q1-Q33, a K or TB node, a gate node or `GRANT(<defined item>,<listed action>)`. Map checks: (b) V1 titles unchanged (`diff` of id and title columns shows only the four added rows); (c) every V2/V3 id in a provenance comment (V2 V2-04, V3 CO-02, V3 SW-05, V3 XC-04, V2 SW-13, V2 XC-09, V3 XC-08) resolves through the map; (d) count 50.
- **(c) Graph mentions every item**: PASS (50 of 50 appear as From or To in 4.2).
- **(d) R25 coverage**: PASS. R25-INV-001 to R25-INV-028 each have a row; every numeric section pointer is an existing H3; every item pointer is defined.
- **(e) Owner questions**: PASS. Q1 to Q33 each defined in the section 3 table and the owner-question appendix; no other Q referenced.
- **(f) Waves vs edges**: PASS, by script. For each of the 113 hard item-to-item edge pairs (kind not SOFT), the From item's wave is earlier, or both share a wave and the serial column orders them (directly or transitively, "before"/"after"/"last"). XC-11 is treated as W3 for first-release edges and W5 for end-to-end edges. Every wave exit check names only items scheduled in that wave or earlier; every gate cell names only scheduled items. Two W1 wording mentions of XC-04 were reworded to "the JOIN comparison" before the run so the parser does not schedule XC-04 in W1.
- **(g) Contradiction re-scan** (grep): workers running `/sc:pr-submit`: 0 (the three `pr-submit` lines without "PR session"/"GRANT" are the 4.4 summary `[G pr-submit, merge]` grant notation twice and R25-INV-027's staging fact); "not found in this checkout": 0; JOIN before the INV-008 requirement: 0 (no pre-merge sweep wording; XC-04 not in W1 lanes); "no scheduler" without the cadence record: 0 (the only hit is the cadence record's own sentence pointing to Q31); ledger inside the #539 checkout by default: 0 (hits for "ledger" plus "this checkout" are the TB-GIT-ROW definition and the W0 lane, neither a ledger location). Placeholders (`RF_PLACEHOLDER`, "filled by Change"): 0. Bare probe ids for Round 2.5 findings: 0 (the three regex hits are `probes.py` lines citing ADJ's INV-015, INV-012, INV-006).
- **(h) INV-008 first**: PASS. Frontmatter status names INV-008 UNRESOLVED-EXTERNAL and owner decision Q1; 0.1 is the first H3, says UNRESOLVED-EXTERNAL and owner decision Q1, keeps "does **not** specify the code fix", and states only the requirement and options F1, F2, F3; the first "first action" text is INV-008's.

### Structural Integrity
- Heading hierarchy: PASS
- Section ordering: PASS
- Document flow: PASS (Weak points and Interface contracts follow each Risks list; contract-note lists follow the XC table)

### Internal References
- Register endpoints: 296 checked, 0 broken; edge rows 123, 0 broken endpoints; R25 pointers 28 rows, 0 broken; Q references 33, 0 broken

### Contradiction Re-Scan
- New contradictions introduced: 0 found by the greps above. Known carried contradiction: the ADJ A-004/A-005 tension on the #534 table is kept visible with a contradiction marker (2.1 Weak point W1), not resolved silently.

## Summary
- Total changes planned: 66
- Applied: 66 (46 APPLIED, 20 APPLIED-WITH-DEVIATION: Changes 1, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22, 24, 30, 31, 40, 44, 48, 54, 65, 66; each reason is in its entry)
- Failed: 0
- Skipped: 0 (Changes 25, 26, 32, 38, 39, 43, 45, 47, 49, 56 needed no new text or were carried by an earlier Change; recorded as APPLIED with the verifying grep)
- Out-of-scope target not edited: `base-selection.md` preserved strength 9 (Change 10), because this executor may write only the two output files
- Post-merge validation: PASS (a, b, c, d, e, f, g, h)
- Output: `merged-spec.md`, 1345 lines; finished 2026-11-13T21:35:02Z

## FIX CYCLE 1 (independent QA `qa-merged-spec.md`: FAIL with blocking B1, B2 and minor M1-M10)

### FIX CYCLE 1 - B1: TB-GIT gate cycle on SW-01
- **Status**: FIXED
- **Source**: QA B1 (edge 2, SW-01 blocked-by, 4.4 line, 4.3 items 2-3); TB-GIT definition in 4.1 (unchanged in substance)
- **Before**: edge 2 `TB-GIT -> SW-01 (GATE)`; SW-01 blocked-by "Q1; TB-GIT"; 4.4 "Q1, TB-GIT -> SW-01"; 4.3 "No cycle" checked only item edges. TB-GIT is satisfied only after SW-02 (or an F3 record by SW-01), so the first action waited on its own output.
- **After**: edge 2 is `SW-01, SW-02 -> TB-GIT (GATE)`: the ruling decides TB-GIT's scope and never waits for it; TB-GIT still gates SW-05 (row 15) and every sweep run (row 106, TB-GIT-ROW). SW-01 blocked-by is "Q1 only (the owner)" plus its own thread grants when someone else acts; SW-01 and SW-02 blocks gain TB-GIT; 4.1 TB-GIT row says it gates SW-05 and every sweep run, never SW-01; 4.4 shows `{SW-01, SW-02} -> TB-GIT -> {SW-05, XC-04}`; 4.3 items 2-3 now cover gate nodes and say SW-01 waits for the owner only. Wave table unchanged (TB-GIT is satisfied by W1's SW-02 and gates W2's SW-05 and W3's XC-04).
- **Script**: `validate.py` gained check (f2): every hard edge in a graph whose nodes include gate and boundary nodes; DFS for cycles; a required-satisfaction check (TB-GIT must have an edge from SW-02, SWEEP-RUNNABLE from SW-05, so the implicit prose condition that hid B1 is now enforced; the pre-fix table would have failed it); gate-node wave = latest wave of its item predecessors, successors must be later. Output: `(f2) full graph nodes 145, cycles found 0; item-satisfied gate nodes {'TB-GIT': 1, 'SWEEP-RUNNABLE': 2, 'K-NOTE': 3}; gate-to-item edges checked 3` (TB-GIT W1 -> SW-05 W2, XC-04 W3; SWEEP-RUNNABLE W2 -> XC-04 W3; K-NOTE has no item successor). `roots.py`: roots [OB-01, OB-02, SW-01, SW-04, XC-01, XC-08, XC-10].

### FIX CYCLE 1 - B2: per-action grants for #539 pushes and the thread resolve
- **Status**: FIXED
- **Source**: QA B2; 6.4 rule 2 per-PR per-action rule; WC-9 `WORKER-CONTRACT.md:41`
- **Before**: action vocabulary of nine actions without `push`; 6.8 mentioned "a push grant"; no GRANT edge for the #539 author's hand pushes (SW-02, SW-03, SW-05 (1)) or the Augment-thread resolve (SW-03 (4)); SW-03's push scheduled in W0 with no grant
- **After**: actions `push` and `thread-resolve` added in 4.1 and 6.8 (eleven actions); 6.8 says a `push` row covers a hand push outside `/sc:pr-submit` on one PR, the tool's pushes stay in that PR's `pr-submit` row, neither satisfies the other, and `thread-resolve` is separate from `thread-reply`; "a push grant satisfies neither a merge, an issue write, a thread resolve nor a live test"; edges: row 3 adds `GRANT(SW-01,thread-resolve)` (only when someone other than the owner resolves the Codex thread), row 8 `GRANT(SW-02,push)`, row 10 `GRANT(SW-03,push)` and `GRANT(SW-03,thread-resolve)`, row 17 `GRANT(SW-05,push)`; matching blocked-by cells of SW-02, SW-03, SW-05 and criteria text SW-02, SW-03 (4)-(5), SW-05 (1); 6.3 #539 author row, 6.4 rule 2 (hand pushes and thread resolves each need their own grant; naming the author in Q33 is not a grant), W0 and W1/W2 L-539 lanes, 4.4 lines. No grant widened; merge stays its own grant; pr-submit rows unchanged.
- **Validation**: `GRANT(...,push|thread-resolve)` nodes present for SW-01, SW-02, SW-03, SW-05; check (b) accepts the two new actions and finds 0 undefined endpoints (316 register endpoints, 124 edge rows).

### FIX CYCLE 1 - minor notes
- **M1 (cells vs edges)**: FIXED. SW-07 blocks XC-07; XC-07 blocked-by SW-07 and blocks OB-09, XC-11; OB-08 and V2-03 blocked-by XC-08; XC-08 blocks V2-03; SW-05 blocks SW-11, SW-14, XC-04, XC-06, SWEEP-RUNNABLE; new edge row 124 `XC-08 -> V2-01, OB-09` from V1's XC-08 "blocks" cell (XC-08 (2), OB-09 (4)); 5.1 W2 gate for OB-08 adds XC-08; 4.4 lines updated. Wave check re-run: still no backward edge.
- **M4**: FIXED. 6.1 Live state row now writes `gh pr view <N> --repo IronbellyOrg/IronClaude`.
- **M7**: FIXED. 4.3 item 4: "XC-07 feeds K-NOTE, OB-09 and XC-11".
- **M8**: FIXED. 7.4 item 1 lists SW-14, OB-09, WA-07, XC-04 and XC-11 (5.2's waiting list).
- **M9**: FIXED with source. Mode 0600 cited at `export.py:260` (ADJ's `:26` noted); `NOTE_DUPLICATE_DISPATCH` defined at `classify.py:76`, used at `:898` (ADJ's `:893-896` noted; DEBATE SC-16 and QA); join basis cites `classify.py:891` and notes `probes.py:435` reads `dispatchId` (QA read).
- **M10**: FIXED. SW-04 runs-in names #541's branch `fix/claude-md-worktree-rule-test` (QA's `gh pr view 541 --repo IronbellyOrg/IronClaude`).
- **Skipped (need a decision or by design)**: M2 (ledger package naming rule: an owner or coordinator decision; Q26 names the home and branch only); M3 (whether the coordinator creates or binds its own Orca Run and records its id: a design decision the plan does not make); M5 (XC-11 in W3 and W5 is the plan's two-scope design, Change 59); M6 (section 6 not last: the plan's fixed H2 order, A15).

### FIX CYCLE 1 - re-run of validation a-h (2026-11-13T21:53Z)
```
(a) headings: 56 real headings, H2=12, H3=43
(b) ids used outside map/comments: 50; register endpoints checked: 316; edge rows: 124
(c) items in edge table: 50 of 50
(d) R25 rows: 28; existing H3 numbers: 43
(e) Q referenced: 33; appendix rows 33; section 3 rows 33
(f) hard item-to-item edge pairs checked: 115; (f2) full graph nodes 145, cycles found 0
(h) first H3: line 28 '0.1 First action: INV-008 (UNRESOLVED-EXTERNAL)'
CHECK a, b, c, d, e, f, h: PASS
```
- (g) re-scan: TB-GIT into SW-01: 0; worker runs `/sc:pr-submit`: 0 (remaining hits are the 4.4 `[G pr-submit, merge]` grant notation and R25-INV-027); "not found in this checkout": 0; old ledger path: 0; XC-04 in W1 lanes: 0; scheduler claims: only the cadence record line. PASS.
- Output now 1347 lines.
