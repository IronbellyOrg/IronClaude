# Research: Change surfaces per option

**Investigation type:** Architecture Analyst
**Scope:** Rule pins and mentions, source and installed copies, sync conventions and developer-guide staleness
**Status:** Complete under user-approved current-source inventory scope (historical archival residual remains unread/unverified)
**Date:** 2026-11-09
**Delivery:** User-approved adaptation: researcher returns findings; coordinator writes this file. No model-tier change.

---

## Delivery status and complete evidence

**Authorized scope resolution, 2026-11-09 11:22:** The user approved limiting the change-impact inventory to current source, tests and distributed copies, keeping historical matches explicitly unverified and continuing the checks. The following partial-status history remains for provenance; it does not override this later approval. Active inventory is complete under the narrowed scope. No claim is made that unread archives were subsequently read. Remaining source/QA checks are unchanged.

**Partial:** Active editing surfaces and six options verified, but exhaustive original archival-match rereads not complete. The coverage ledger is now preserved. The execution attempt can be checked off only as partial with an explicit blocker log per task error handling, never as successful exhaustive research. Exact first return preserved in `returned/07-returned-findings.json`, field `text`, including F01-F17/T01-T09/C01/D01-D05/B01-B05/A01-A02 register, six per-option tables, all counts and uncapped capture paths. Downstream reviewers must read complete returned text alongside this index. An append-only archival supplement is being preserved separately; it is not a new active-rule finding.

## 1. Active sources and pins

Paths relative worktree unless global:

| Surface | Verified locations |
|---|---|
| Ownership words | Root CLAUDE.md:312; src/superclaude/core/CLAUDE.md:58; /home/coder/.claude/CLAUDE.md:58; source/dev/global ccsession-tag/README.md:242 |
| Worktree hook ownership | Source/plugin/dev/global require-orca-worktree-agent.sh:354; message352-355; actual track/fin94-103 and Bash342-357 |
| Contract | source/global WORKER-CONTRACT.md WC8:40/WC13:62/coordinator:69; worker:11/mode12/never-list23/nested24-25; ownership220-246/brief283-304 |
| Routing guide | source core, plugin sc-recommend refs, global HOW-WE-WORK.md:396-405 (person opened400); same source/plugin packaged under .venv/.../_src and _plugins; no project .claude HOW-WE-WORK found |
| Exact ownership-message pin | tests/hooks/test_require_orca_worktree_agent.py:31-38,128-133. Governed test:31-56 pins prefix/example, NOT exact owner sentence |
| Role/parity pin | tests/core/test_orca_session_launch_guidance.py:44-59 roles plus paragraph equality; exact under-another phrase NOT required |
| Contract pins | tests/skills/test_worker_contract.py:123 WC8,155 WC13; NEVER_AS_WORKER382-391; UNATTENDED_EXPECT438-742/derived746; list checks765-771,831-839; source-section scan869-886; positive907-913/negative1044-1051; never-worker negative1081-1090; WC8 delimiter1237 |
| Guard behavior | src/superclaude/hooks/scripts/launch-level-guard.sh:458-478,737; tests/hooks/test_launch_level_guard.py:3093-3111 external ESCAPE /3131-3148 read-only |
| Registration/install/parity | tests/cli/test_install_hooks.py:827-881 registration, source/plugin byte parity849-857, install860-881 |
| Guide mirrors/install | tests/commands/test_routing_plugin_parity.py:29-38; tests/cli/test_how_we_work_install.py:23-33 |
| Mutation warning | tests/cli/test_verify_sync_hooks.py:1-24 tests mutate real checkout; inspected NOT run |
| Dev guide | docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md coordinator978/stale985/never-list993; WC8 mentions336,469,483,802,1005,1025,1177,1286 |
| Other design | docs/designs/issue-watcher.md:68 WC13 anchor61 stale (now62); applied spec385-407; D5 recommendation3,48-50,64; approval8-20 |
| Sync/packaging | Makefile68-86 plugin,108-157 dev sync,165-184/253-269 verify; scripts/build_superclaude_plugin.py:15-18,69-76 copies PLUGIN input, not source synchronizer; core install32-78 skip existing70-72; hook install251-290 skip279-281; pyproject78-87 wheel includes both |
| Internal-helper precedent | adversarial command145-163 activates backing skill; sc-adversarial-protocol/SKILL.md:1050-1079 dispatch/collection/failure,1966-1977 merge executor |

[CODE-VERIFIED] Scanner is not WC8/WC13 role enforcement. Guard independent all-level ESCAPE. Ownership wording edits confer no authority. Static test pins are not live mailbox/depth proof.

**Key Takeaways:** exact-message versus role/parity tests differ; active/copies/history not interchangeable; no tests/sync/build/install run.

## 2. Search counts and archival coverage

Uncapped files_with_matches/count searches, then narrow content. Explicit dev-copy search supplements ordinary root search. Counts describe initial snapshot, not current growing self-mentions.

| Term | Root files | Matching lines |
|---|---|---|
| coordinator under another orchestrator | 41 | 104 |
| WC13 | 276 | 701 |
| WC8 | 127 | 346 |
| person[ -]opened | 53 | 131 |
| NEVER_AS_WORKER | 17 | 26 |
| Selected full hook message fragments | 7 | 23 |

Frozen `.dev` union:332 files,1094 matching lines; path/line/term capture1516 entries includes repeated terms on one source line, not independent evidence. Captures under `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-fix-flaky-parallel-thread-test/952cee73-732b-4629-bd21-afa7a36058dd/tool-results/`:
- `call_25d4f84924964fde84384a6c1dd3686c.txt` original path/line/term.
- `call_70b584e0ac584c3198ea0273159a402f.txt` file list.
- `call_19d64d1d820348199f8ed311879166ee.txt` counts.

Initial original-file rereads covered active locations only. First continuation added54 fully covered matched-file sets plus1 partial research-notes file. Classification: historical snapshots (decisions/scoring/spec/reviews), copied reviewer prompts/grounding, adversarial debate transcripts (NOT worker execution), own generated research mentions; no new active runtime pin. Old D5 source/r1/r2 statements repeated in transcript count once as evidence lineage, even if inventory lists each physical file. Coverage and remaining capture ranges preserved in exact supplement evidence; still not complete.

**Key Takeaways:** raw discovery is not original-source reread; historical copies don't supply more independent runtime evidence; unfinished archive scope remains explicit.

## 3. Per-option change surfaces (evidence, not sequence)

### O1 keep two tiers, clarify owner words

| Files | Conditional change / pin |
|---|---|
| Root CLAUDE:312; core CLAUDE:55-59; source ccsession README239-243 | Wording correction if selected; source pair parity/role tests; no exact root pin identified |
| Source+plugin hook354; exact message test31-38 | Message only, scanner unchanged; exact stderr and byte-mirror tests |
| Launch-guidance test44-59 | May NOT need change if both orchestrator/coordinator roles retained; two mandatory test edits not established |
| Dev/global README/hook/global core | Generated refresh, not independent canonical edits |
| Contract/routing guides/current pins | No policy edit inherent to O1 |
| Dev guide985 | Independent stale rollout correction, not caused by O1 |

### O2 person-opened peers

| Files | Conditional change / pin |
|---|---|
| Contract69,220-246/global | Clarify independent Task ownership only if needed; does not authorize shared inbox |
| source/plugin/global/packaged guide396-405 | Peer routing clarification; plugin/install byte parity |
| Root/core/README/hook ownership copies | Only if O2 selected as ambiguous phrase resolution; hook mechanics not inherently change |
| Dev guide978-981,1005,1013,1025 | Distinguish independent peers/internal helpers/supervised workers |
| Contract23/NEVER_AS_WORKER382-391 | No list change for peers alone; NEW coordinator-only command separate decision |
| Guard458-478,737/tests | Only if launching peers from governed session demanded; ordinary peers not automatic exception |
| Spec405/approval12 | No depth-policy reversal inherent |

### O3 supervised worker with helpers

| Files | Required/conditional surface |
|---|---|
| Contract11-25,53-69,101-110,204-216,220-246,283-304/global | Role/brief/authority/completion/questions/result/retry/placement changes; WC13 and related phrase pins |
| Contract40 and section-code detectors in tests123,843-886 | WC8 CAN remain if session-only; command-owned dispatch additionally changes rule/test rejection |
| Contract23/tests NEVER_AS_WORKER / UNATTENDED_EXPECT / set checks | Eligibility/new command declaration conditional, not automatically all never-worker rules relaxed |
| Guide all source/plugin/global/packaged | Person-opened-only definition/routing change, parity |
| Dev guide336,469,483,802,978-1025,1177,1286 | Clarify session exception vs command permission |
| Core/root/README source/dev/global | Explicit supervised-worker-create prohibition revised only by new decision; parity |
| Worktree hook copies | Clarification not necessarily scanner change; no bounded-grant/count enforcement in current scanner |
| Launch-level guard/tests | Independent governed-session allowance decision, external paths currently ESCAPE |
| Spec385-391,405-407; D5/approved records | New decision amendment referencing original history, not rewriting history as prior permission |

### O4 ordinary handoff-owner middle

| Files | Surface |
|---|---|
| Contract11,62,69,220-246/global | New role not automatically worker or authorized coordinator |
| Contract53-65,101-110; dev guide1011-1026 | Ordinary upward reporting distinct from lifecycle settlement |
| Contract41-45,227-246 | No inherited push/PR/merge/Ruling/grant from ownership |
| Ownership core/root/README/hook copies | Exact meaning/launch distinctions; message/parity tests |
| Guides/dev guide978-981 | Agent-opened coordinator new eligibility case |
| Guard/tests | Agent launch/worktree ESCAPE unchanged by naming handoff |
| Contract23/list tests/dev guide991-993 | NEW coordinator-only command never-worker classification conditional |
| Spec/approval D1-D5/git | New person-opened-owner assumption/decision, no verified upward-channel test found |

### O5 internal Agent-tool fanout

| Files | Surface |
|---|---|
| Contract22-25,46,60/global | No change for existing helpers; lifecycle remains top-level |
| Adversarial command/protocol | Existing actual helper dispatch/collection/merge instructions reuse; runtime execution not proved |
| Guides/dev-guide internal-subagent sections | Optional clarification not Orca nesting |
| tests UNATTENDED_EXPECT/heading equality/nested validation | New wrapper only, not expansion inherent to current fanout |
| Worktree/launch-level hooks | No ordinary local-helper launch exception inherent; must not claim Orca Task/Dispatch records |
| Ownership words | Separate cleanup, O5 alone doesn't define external role |

### O6 defer with explicit gates

| Files | Surface |
|---|---|
| Spec405/D5 recommendation49 | Expose composite/measured-need/trace and omitted-mailbox divergence |
| Contract246 | Already records follow-up Tasks/extra time; existence not satisfactory notes evidence |
| Contract/guides/test pins | No nested policy change inherent |
| Ownership copies/tests | Separate wording decision if bundled, not required for defer alone |
| Dev guide985 | Independent current-state correction |
| Guard/tests | No relaxation required |

**Key Takeaways:** O3/O4 much broader than owner sentence or depth number; do not relax WC8 merely for session-level helpers; internal helper option already has primitives.

## 4. Distribution dependency map

Makefile112-143 copies skills/hooks to .claude, verify171-184/253-269 compares. It does NOT copy root/core CLAUDE/contract/routing guide to global install. Source/plugin hook equality is pinned test_install_hooks849-857; source guide/plugin refs full-byte equality test_routing_plugin_parity29-38. Plugin builder reads plugins tree (build script15-18,69-76), so packaging stale mirror possible: plugin build is not source->plugin synchronizer. Core installer32-78 and hook installer251-290 skip existing without force. Wheel pyproject85-87 includes packaged source/plugin copies; they are environment artifacts not canonical edit targets.

Per option: O1 hook/README dev refresh plus installed core/README/hooks; O2 no behavior sync inherent, guide clarifications mirrored/installed; O3/O4 changed distributed command/skill/hooks need dev copies, core role docs separately installed, worker-visible both command surfaces validated by brief guard CONTRACT16-19,216; O5 no sync for mere selection, only new wrapper/protocol; O6 no behavior distribution inherent except separately adopted words/gates. No actual sync/install/build/test performed. verify_sync_hooks tests mutate repository (T09:7-15), excluded from read-only work.

## 5. Stale developer-guide inventory verified

DEV-GUIDE:985: "At P0 no command accepts `--unattended` or `--report-dir`, and `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py` is empty."

[CODE-CONTRADICTED as CURRENT inventory] TEST:438-742 dictionary populated, :746 frozenset(UNATTENDED_EXPECT); :831-839 actual heading-set equality. Uncapped `^## Unattended mode` count31 in31 source commands: adversarial, analyze, auggie-review, brainstorm, build, business-panel, cleanup, cleanup-audit, cli-eval, cli-portify, design, document, explain, graph, impact, improve, index, index-repo, init-lite, recommend, reflect, release-split, research, review-translation, spec-panel, task, tasklist, tdd, test, troubleshoot, workflow. Actual adversarial argument declaration70-71/behavior153-163 read; CONTRACT303-304 lists16+15 commands. Historical At P0 may remain but not current readiness claim; none of31 commands executed.

**Key Takeaways:** current count31 not0; dictionary-derived set not placeholder; historical qualification not denial P0 existed.

## Gaps and Questions

[UNVERIFIED] Exhaustive archival original ranges incomplete (keep Step2.7 open); runtime depth/profile/handoff-root/reload not traced in this slice; O4 upward identity/channel; nested mailbox ownership; satisfied D5 trigger not investigated here; new orchestrator packaging command vs role vs wrapper consequential; governed exception policy; ownership phrase meaning not enforcement; execution test/sync/build/install results absent. [CODE-CONTRADICTED] Dev-guide empty set; old D5 unapplied status and one-command rationale; issue-watcher.md:68 WC13 anchor61 now62. No runtime conclusion rests on unread archive matches.

## Stale Documentation Found

- [STALE DOC] DEV-GUIDE985 current rollout impression vs current31 headings/populated expectation.
- [STALE DOC] D5 recommendation3,64 unapplied vs current contract62/spec405.
- [STALE DOC] D5:48 single-command premise vs CONTRACT204-216,288-289 chain; chain still not helper-authorizing composite.
- D5:49 vs SPEC405 mailbox divergence preserved, governing intent unresolved in this slice.
- [STALE DOC] issue-watcher.md68 old WC13 line61 now62.
- Ownership copies ambiguous not complete hierarchy proof; explicit worker prohibition remains.

## Archival completion ledger after final gap-fill

Exact supplements: `returned/07-archival-supplement-1.json` and `returned/07-archival-supplement-2.json`. Frozen captures copied into `returned/inventory-captures/`; exact unread list is `bw1hpg0xz.txt` lines25-298, with reconciliation assertion299. These are machine captures, not source reread evidence.

| Metric | Count |
|---|---|
| Frozen paths | 332 |
| Unique matching original lines | 1094 |
| Term occurrences before same-line dedup | 1465 |
| Fully covered paths | 58 |
| Partially covered paths | 3 |
| Wholly unread paths | 271 |
| Covered matching lines | 227 |
| Unread matching lines | 867 |
| Paths with unread matches | 274 |

Reconciliation58+3+271=332 and227+867=1094 passed. Five expanded-query-only lines excluded, not silently added (OwnerP T1 patch427,470,472; T2 patch470; scope01:115). Count-capture SHA256481f215ed9f5c7a774c8e5441723ff169dc04d6f707b247b5c6f9c77c87581af; location-capture SHA2567f4ea2dbf0f8782f77e5dab0ce471bc8e981c8e6037ebef5e135193258d9690b.

Second continuation read only10 original lines in2 saved specs (spec-v3-after-round2:57,71,204,309,396; spec-v2-after-round1:56,70,203,305,385), not the residual. Partial paths are applied spec (covered386,405; unread59,76,81,244,292,299,315,368,374,440), this task file (covered198,202; exact unread list in capture), research-notes (covered12; unread26,27,35,36,38,47,48,55,72,73,83,84,86,115,121,159). The exact274-row residual remains unread/unclassified. Earlier active source reads are valid only at their explicitly reported locations. New accumulating self-mentions were excluded to preserve frozen scope. After2 gap-fill rounds this is a real completion limitation, not a runtime source contradiction; do not assert exhaustive inventory or infer classification from directory names.

## Phase-2 correction addendum — B1/B2 dependency

Research04's B1/B2 addendum qualifies this inventory's guard-behavior entry, §1 guard conclusion and O2/O3/O4 guard rows. All-level ESCAPE denial remains source-established, but Orca-branch coverage requires a positively bound session and recognized literal `orca` basename (guard:450-478,737); research03 records `orca-ide`, which does not match that branch. Neither spelling nor ownership wording confers authority, and no live success is established.

For O1-O4 supervision inside a bound session through recognized `orca`, required worker-list/worker-read/worktree ps probes are an additional policy-design surface: the current sweep/L1 cannot run unchanged although worker-show is listed. This qualification does not apply categorically to all sessions and does not recommend automatic allowlist expansion. Existing role-policy and launch/reporting decisions remain separate.

This correction does not alter the user-approved current-source inventory scope, archival ledger, unread-history disclosures, distribution map or O5 capability assessment. Immutable returns remain unchanged and must be interpreted with this addendum.

## Summary

Canonical ownership words reach root/core/README/source-plugin hook, dev/global copies and exact/parity tests. O3/O4 additionally touch role eligibility, lifecycle/admission, grants, worktrees and launch-level policy; O5 has existing internal delegation. Sync/dev/plugin/install are distinct relationships, not one automatic distribution step. Current unattended inventory31 contradicts guide's present P0-empty implication. Active-surface analysis is ready as partial input, but archival source-reread condition remains incomplete and cannot be called done.

