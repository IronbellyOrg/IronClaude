# Round 2 advocate for Variant A (slot C-05, consumer-entry-effect-and-delivery)

Tags: [CHECKED] = read in this session at the cited line; [INFERRED] = reasoned from checked lines, not run; [NOT CHECKED] = not read here. Paths are repo-relative. No test was run.

## Responses to criticisms
**B strength 1 (reach behind reflect is narrower than A said): conceded, and it is wider than B's own E4.** [CHECKED] reflect's default `--depth` is `standard` (`src/superclaude/commands/reflect.md:98`); workflow Wave 4 passes "defaults for every other flag" (`sc-workflow-protocol/SKILL.md:89`). So workflow reaches the panel only when the rubric escalates; a rubric stop never reads the engine (`sc-reflect-protocol/SKILL.md:317,327-328`). Tasklist reaches it only for forced-deep phases (`n_cpo >= 1`, `n_strict >= 2`, score >= 10; `sc-tasklist-protocol/SKILL.md:1677-1685`) and rubric escalations of standard phases. My round-1 strength 6 holds only for the quick band: one STRICT task already scores >= 4 (`:1668,1680`), a standard phase the rubric may stop at T1. The gap is real. It is not an argument for a second entry unless it is cheaper to close there than in reflect's depth policy; that is a measurement (my 6.2), not a given.

**B concession 1 (`contract_version`) and what it means.** [CHECKED] `eval_workflow_vs_task_builder.py:1140` and `archive_workspace.py:327` both require `"1.1"`, and `test_workflow_command.py:178` pins the literal. [CHECKED] the archive reader `_kv` (`archive_workspace.py:167-173`) keeps any top-level `key: value` line and ignores the rest; the eval reader needs only `set(CONTRACT_KEYS) <= set(contract)` (`:1163`). So B's additive keys are safe if the version stays `"1.1"`, and the bump is wrong. For A it changes nothing: A adds no key. It does weaken my claim that A is "the only route that keeps the contract intact"; B-add can too.

**(iii) Does B-add rewrite no pin; does a nested panel directory need rule changes?** B is right on pins: [CHECKED] `test_workflow_command.py:246-248` is an `any(...)` and `:255-258` is a substring test, so a second panel line passes (I conceded the point in round 1). New, [CHECKED]: `test_worker_contract.py:528-537` expects workflow's nested list `["reflect"]`, and `_check_nested_text` (`:1477-1482`) only demands that listed kinds appear, so a `nested/panel-<n>/` mention is not pin-forced. What no test catches: the worker contract's `artifacts` rule names only "each file reflect wrote in its `<report-dir>/nested/reflect-<n>/` run directory" (`return-contract.md:52`). A panel directory beside it would be absent from `artifacts` unless that rule is extended by hand. Under A the panel writes under reflect's own `<output>/panel/` (`SKILL.md:311`), inside the directory the rule already covers [INFERRED]. So A strength 4 stands as a correctness point; B strength 3 stands as a test point. Both are true.

**New cost for B that neither paper named.** [CHECKED] the companion eval's permission allow-list names only the workflow and reflect skills (`eval_workflow_vs_task_builder.py:567-573`, mode `dontAsk`) and stages only those two skill directories (`:520`). A new delegate skill needs both edited, or the eval denies the call.

**B weakness 2 (UC-1 is one pass; A discards the loop).** Conceded for UC-1 itself. But B's own concession 4 puts any blocking loop in Stages 7-10, not at Wave 4 or 10.5. [CHECKED] that loop recomputes `F_k` by re-running the full Stage 7 set and carries byte-exact halt strings (`sc-tasklist-protocol/SKILL.md:1604-1614`). A reviewer-feed swap there is a change inside tasklist validation and does not pass through the Wave 4 or Stage 10.5 call. So the entry question and the loop question separate, and A can keep a later direct module on the same core: it closes no door. It is not "B's seam by another name": B's seam at the call sites is advisory anyway.

**(iv) Later direct module on reflect's contract.** Compatible. If added, it needs the items in bullet 5 of my merged resolution; A's "no new keys" is a statement about this release.

**(v) What `--t2-engine panel` must change to reach consumers.** [CHECKED] (a) reflect grammar and rejection text (`SKILL.md:87`), the table rows that say "and `panel` from Stage 3" (`:328-330`), and the authoritative Wave 3/4 text; the Stage 3 code itself is not in `cli/review` (Grep for "Stage 3" there: no match). (b) Fence test: both guards diff against `HEAD` (`test_shadow_skill_contract.py:46-48,53`), so they bind only uncommitted edits and pass on a committed branch [INFERRED, not run]. I withdraw "the fence test must be changed". (c) Call sites: nothing, if reflect's UC-1 default flips; if the call sites append `--t2-engine panel` instead, the substring pin still passes. A default flip changes every UC-1 caller, so it is the INV-L release point and needs the replay first. (d) C-04 (T5 engine) is independent. (e) The companion eval's pool denies Bash, Agent, Task and `mcp__*` (`:66-67`), so it cannot run Tier 2 for either route; it is not the measurement harness.

**B weakness 4 (plugin deferred, not avoided).** Conceded. A defers it deliberately; see C-003 and merged bullet 6.

**B weakness 5 (A's low-phase miss is only measured by A's 6.2).** Conceded; see strength 1.

**B strengths 2, 4, 5, 6.** Agreed on facts: Stage 8-10 blocking exists (`:1614`); a direct call must be delegate-only (`workflow SKILL.md:107`); B does not touch `cli/reflect`; plugin facts. None of them selects the entry.

## Updated assessment of Variant B
B's strongest form is B-add, advisory, with any blocking use confined to the Stage 7 reviewer feed after a replay. That form is honest and I can accept most of it. B's reach argument is correct and sharper than B wrote it. B's withdrawals (version bump, E6, E7) remove three of its weaker supports. What stays against B: no data shows the direct entry beats the reflect entry (B section 9); B-add costs a second review per phase, unmeasured; B's call-site edit is advisory, so the entry change buys reach, not effect; a new skill needs edits the tests do not force (the `artifacts` rule, harness allow-list and staging). Steelman of the B position I reject (B-replace plus a blocking effect at Wave 4): it would give every plan and phase a blind, model-diverse review with a quorum. It is rejected because B itself says its blocking effect is "a hypothesis" until replay (B section 8, answer 3) and the only measured wrong-blocker figures run against it (B E11).

## Concessions and what I still defend
**Conceded:** (1) reach behind reflect is limited to forced-deep phases and rubric escalations, and for workflow to rubric escalations only; (2) the fence tests are a working-tree guard, not a standing constraint; (3) "zero pin changes" was a prediction, and B-add also changes no test pin (but needs unpinned edits); (4) generation-time blocking already exists in Stages 8-10, so X-001 is mixed; (5) a plugin-installed Wave 4 already skips review (shared inference), and A defers that cost; (6) the v2 kernel has no tasklist lens (`findings_v2.py:36` per B, [NOT CHECKED] by me), so reflect reviews coverage under `reflect-pre`, not the five Stage 7 dimensions; (7) my X-002 wording ("cannot work without `sc-reflect-protocol`") is too strong for a delegate skill that brings its own reviewer agent.

**Still defended:** (1) one call shape at Wave 4 and Stage 10.5 for this release: it keeps the closed enum, four readers, the substring pins and the 36-test verdict map with no second verdict authority; (2) advisory at generation, blocking at T5 and the existing structural gates; (3) no plugin copy of a panel skill alone, because delivery has no forcing element once the call sites stay (B section 8.4 admits delivery is inseparable from entry); (4) the engine switch is gated by replay, the contract-compat test and a headless smoke run.

## Shared assumption responses
- **A-002 (panel good enough on consumer artefacts): Neither, unchanged.** Unmeasured through either entry. Agreed condition with B: advisory first; any blocking use waits for replay.
- **A-003 (nested fan-out completes headless, closed enum kept): changed from A to Hybrid.** The existing `nested/reflect-<n>/` kind is covered by the `artifacts` rule (A's advantage); a new `nested/panel-<n>/` kind is not pin-forced and needs a hand edit (B's cost); headless Tier 2 is unrun for both, and the companion eval cannot run it (`eval_workflow_vs_task_builder.py:66-67`). A smoke run is required on either route.
- **A-004 (short or failed panel maps fail-open): Hybrid, agreeing with B.** True for the two advisory calls (`workflow SKILL.md:93`, tasklist `:1640`). A blocking feed must not fail open: Stage 7's some-vs-zero gate escalates a zero-success run (`:1608`).
- **A-005 (plugin Wave 4 already skips): Neither.** Shared inference, not executed.
- **A-006 (parity pins keep meaning; `verify-sync` is the only guard): changed to B.** The parity pin covers `*.md` of one skill and one command only (`test_workflow_command.py:93-103`); any added plugin file needs its own test. Moot under A, accurate as a statement about the assumption.

## Final per-point verdicts
| Point | Winner | Hybrid content or reason |
|---|---|---|
| S-001 | Neither | Section order is cosmetic. |
| S-002 | B | Entry, effect and delivery are separable (B concession 4 and section 8.4); adopt the three-part structure. |
| S-003 | B | Per-row "Keeps / Endangers" is more candid. |
| C-001 | A | Calls stay `/sc:reflect --mode pre`; no B-replace; B-add not in this release; reopen if replay shows the reach gap carries blocking GT items. |
| C-002 | Hybrid | Advisory at Wave 4 and Stage 10.5; any blocking use is a later, separate Stage 7 reviewer-feed change gated on replay. |
| C-003 | A | No plugin copy now; decide plugin delivery as one set (reflect, panel, reviewer agent, CLI availability). |
| C-004 | Hybrid | B is right on the reach fact; the remedy (depth policy versus a direct call) is chosen by the routing-coverage measurement. |
| C-005 | Hybrid | No new keys now; for a later direct module, additive keys, `contract_version` stays "1.1", `reflect_*` unchanged. |
| C-006 | Hybrid | One reflect-side switch gated by replay (A); the fence is only a working-tree guard (B right). |
| C-007 | Hybrid | `reflect-pre` lens for Wave 4 and Stage 10.5; Stage 7 dimensions only for a Stage 7 feed. |
| C-008 | Hybrid | Blocking exists in Stages 8-10 (B); swapping its reviewers touches P2 pins and halt strings and is a separate later module (A). |
| C-009 | A | Wave 4 stays one advisory Skill call; Will Not at `:107` stays true. |
| C-010 | A | A carries no ledger-loop conditions; B carries C-02 INV-001/002/003 and C-03 INV-007. |
| C-011 | Hybrid | A's replay and contract-compat test plus B's loop and cost columns; harness must not be the companion eval. |
| C-012 | Hybrid | Module-declared effect is the right rule for later direct consumers (B); none is added here (A). |
| X-001 | Hybrid | Blocking exists (B); a direct call at Wave 4 or 10.5 adds no loop, a Stage 7 feed swap changes the block's evidence base (A). |
| X-002 | Neither | Both consistent with checked facts; open fact is CLI availability in a plugin install. |
| X-003 | Hybrid | B-add rewrites no test pin; both routes need unpinned edits; A's "zero" was a prediction. |
| X-004 | Hybrid | A adds none; a reviewer swap inside P2 adds no new cycle number, a new loop would. |
| A-002 | Neither | Unmeasured on both sides. |
| A-003 | Hybrid | See assumption response. |
| A-004 | Hybrid | Fail-open for advisory only; zero-success on a blocking feed escalates. |
| A-005 | Neither | Shared inference. |
| A-006 | B | Added plugin files need their own parity tests. |

## Proposed merged resolution
1. **Entry.** Workflow Wave 4 and tasklist Stage 10.5 keep the single call `/sc:reflect --mode pre ...`; no B-replace, and no direct panel call in this release. Condition: the routing-coverage measurement (bullet 4) does not show blocking GT items in phases that never reach the panel.
2. **Engine.** The panel arrives as a reflect Tier-2 engine through one reflect-side switch, released only after the replay, the contract-compat test against the 36-test verdict matrix, and a headless smoke run (INV-L release point).
3. **Effect.** Advisory at Wave 4 and Stage 10.5; blocking stays at T5 and Stages 6-10. A panel result reaches consumers only as reflect's `status`, `coverage_pct`, `tier_reached`.
4. **Reach.** State plainly that behind reflect the panel is reached only on forced-deep phases, rubric escalations, and for workflow rubric escalations only. Measure the share. If it matters, fix it in depth policy (a call-site depth flag or the Stage 10.5 table) before adding a second entry.
5. **Door open.** A later direct module (a Stage 7 reviewer feed, a plan-review) may be built on the same core with `effect` as module data. It needs: additive keys with `contract_version` staying "1.1" and `reflect_*` unchanged; an `artifacts` rule and nested-kind list extended by hand; the companion eval allow-list and staging extended; a parity test per added plugin file; and its own replay.
6. **Plugin.** No panel-only plugin copy. Decide delivery as a set (reflect, panel, reviewer agent, CLI availability); record that plugin Wave 4 skips review today (inference).
7. **Fence.** Document the reflect edit-fence tests as a working-tree guard, not a standing constraint.
8. **Measurement.** A 6.1 entry-effect replay with B's loop and cost columns on the E2 packages plus one held-out package; not run in the companion eval, whose pool denies Bash, Agent and Task.
9. **Pins.** No consumer-side test pin changes are expected; reflect-owned tests change at Stage 3.
10. **Holds while:** C-01 to C-03 outcomes stand (reflect keeps its engine and `shortfall: visible`). Reopen if replay shows the direct path catches materially more blocking GT items per cost, not explained by depth routing, or if the owner chooses plugin parity.

## New evidence and code checks
[CHECKED] this session:
- `src/superclaude/commands/reflect.md:98`: default `--depth` is `standard`. `sc-workflow-protocol/SKILL.md:89`: Wave 4 passes no depth. `sc-reflect-protocol/SKILL.md:87,313-336`: `panel` rejected; D1 and the table.
- `sc-tasklist-protocol/SKILL.md:1604-1615` (P2 loop: full Stage 7 recompute, halt strings, High and Medium blocking), `:1619-1646` (Stage 10.5), `:1668-1685` (score and overrides).
- `scripts/eval_workflow_vs_task_builder.py:66-67` (pool denies Bash, Agent, Task, `mcp__*`), `:520` (stages only workflow and reflect skills), `:567-573` (allow-list), `:1140`, `:1163-1175`.
- `sc-implement-protocol/scripts/archive_workspace.py:167-173,327` (`_kv` tolerates extra keys; version must be "1.1").
- `tests/commands/test_workflow_command.py:178,246-248,255-258`; `tests/skills/test_worker_contract.py:528-537,1477-1482`; `tests/cli/reflect/test_shadow_skill_contract.py:46-48,53` (diff against `HEAD`).
- Grep for "Stage 3" in `src/superclaude/cli/review`: no match.

[INFERRED]: fence tests pass on a committed branch; a `nested/panel-<n>/` directory falls outside the `artifacts` rule; plugin Wave 4 skips.

[NOT CHECKED]: `findings_v2.py:36`; tasklist `:1353-1366` (Stage 7 range split); `tests/tasklist/` pins for the P2 halt strings; `runner.py` (T5); `research/` and the C-01 to C-03 results (relied on both papers' account); the shadow-run reach share; CLI availability in a plugin install.
