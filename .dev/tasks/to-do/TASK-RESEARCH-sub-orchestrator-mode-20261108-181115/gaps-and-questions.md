# Sub-Orchestrator Research Gaps and Questions

**Date:** 2026-11-09
**Template:** Task Step3.5 specifies the gap and stale-documentation tables.
**Research gate:** qa/qa-gate-phase3-final-verdict.md PASS (cycle1)

## Interpretation and source mapping
Deduplicated union of every research01-08 Gaps/Stale section, original returned JSON gap registers, crossvalidation1 U1-U10/crossvalidation2 gapfamilies, both gap-review reports and Phase3consolidation. R01-R08 below denote research/01-contract-authority-model.md,02-liveness-and-reporting-stack.md,03-orca-mechanics.md,04-hooks-guards-identity.md,05-precedents-session-launchers.md,06-decision-history-and-trigger-evidence.md,07-blast-radius-per-option.md,08-orchestrator-issues-requirements.md in order; their exact full registers are retained in research/returned/NN-returned-findings.json text. CV1/CV2=qa/analyst-cross-validation-report-1.md/2.md; GQ1/GQ2=qa/qa-research-gaps-report-1.md/2.md; C3=qa/qa-consolidated-findings-phase3.md. Alias maps in each R file resolve original cited files/functions/lines.

Severity is research-gate disposition: Minor means explicitly documented uncertainty/prerequisite or stale-source issue is not a missing research answer. It does NOT grade safety of implementing absent authority/recovery as minor. No new product fix is authorized. All live-mutating experiments excluded. For a source-answered fact with unresolved live behavior, the row keeps live scope open instead of pretending no source evidence exists. Policy/authority questions need a decision, not necessarily a live run.

User approved current-source/tests/distributed-copy inventory for R07:867archival lines/274paths remain unread, not missing scope. Later R04/R05/R07 B1/B2 addenda govern immutable original returns. Current installed-source R03 mechanics outrank historical guesses and slice-local unknowns, without proving live success. Source-level contradictions and unimplemented future contracts are preserved, not silently corrected into working features.

## Gaps and questions
| # | Gap or question | Source file(s) | Severity | Tag | Status | Needs a live Orca run |
|---|---|---|---|---|---|---|
| G01 | Universal agent compliance with policy, timing/sweeps/token/ack/handoff/chain; text tests do not prove behavior | R01G1,R02G2,CV1U1,R05,R06,R08 | Minor | [UNVERIFIED] | open | yes |
| G02 | Launched nonworker's classification/coordinator eligibility and owner-vs-person-opened definition | R01G2,G12,R04role,R05,R07,R08F1 | Minor | open question | open | no |
| G03 | Autonomous composite brief, bounded child planning/dispatch scope, helper count/question budget/aggregate contract absent; command chains not such permission | R01G3,R06,R08,CV1U2 | Minor | [UNVERIFIED]/[CODE-CONTRADICTED if asserted existing] | open | no |
| G04 | Aggregate own-vs-child progress/final result, partial/blocked/failure reduction/admission | R02G5,R01G3,R05,R08 | Minor | open question | open | no |
| G05 | Parent/helper mixed whole-batch scheduling, delivery ack vs applied ack, who consumes/fences/acks which stream | R01G6,R02G6,R06,R07,R08 | Minor | open question | open | yes |
| G06 | Child ownership/monitoring when parent blocks/asks/fenced/exits/exhausts/replaced, selected-mail handback not full takeover and excludes heartbeat | R01G10,R02G7,R03G3,R05,R08 | Minor | [UNVERIFIED] | open | yes |
| G07 | Cross-level retry/cancellation/settlement/lineage-budget/freeze/cleanup ownership and orphan recovery | R01G10,R02G4,G7,R06,R08 | Minor | open question | open | no |
| G08 | L5 reaches actual human, parent reply not human Ruling; relay ack/deadlines retain provenance | R01G15,R02G8,R06D2,R08 | Minor | open question | open | no |
| G09 | <=40-line supervisor handoff adequacy: helper roster/budgets/pending batches/admission/applied messages/ownership | R02G9,R01WC15 | Minor | open question | open | no |
| G10 | Qualifying unforeseen runtime split plus Task identity and material measured extra round-trip cost not found in bounded notes search | R01G9,R02G10,R06trigger,R08,CV1U6 | Minor | [UNVERIFIED] | open; no global-absence claim | no |
| G11 | SPEC405 omits REC49 mailbox prerequisite: deliberate waiver vs summarization loss not established | R06§2,R07,R08,CV1C8,CV2 | Minor | open question | open | no |
| G12 | Current local-helper source routing/fan-in/reply/creator settlement/fence paths established by R03, but live startup/delivery/restart/settlement recovery untested | R01G4-6,R02G1,G6,R03G3,R06,R07,R08 | Minor | [UNVERIFIED live] | open live scope; source reconciled R03 | yes |
| G13 | Remote federation separate-Run helper workflow/full authority/depth guarantees not certified | R03G4,R02G1,CV1U4 | Minor | [UNVERIFIED] | open | yes |
| G14 | Effective active maximum/runtime storage vs stored profile1, reload after external edit, complete profile propagation | R01G8,R02G1,R03G1,R06,R07,R08 | Minor | [UNVERIFIED] | open | yes |
| G15 | Safe lowering while deeper work/questions exist, rollback/recovery behavior | R03G2,R01G8,R06,R07,R08 | Minor | [UNVERIFIED] | open | yes |
| G16 | Public per-Run override not found by R03 CLI/schema; universal absence/internal APIs and all-profile-machine blast radius not proven | R01G8,R03D5item5,R06,R07,R08F4 | Minor | [UNVERIFIED universal] | open bounded-absence scope | no |
| G17 | All-current-entrypoint depth classifications source-verified R03; historical bundle/symbols changed; actual session identity/refusal receipts not live-tested | R01G4-5,R03G3,R06,R08F3,CV1U7 | Minor | [UNVERIFIED live] | open live scope; current static classification reconciled | yes |
| G18 | Universal absence of Agent-tool provider/adapter limits not proven merely from Dispatch-only fence | R03G5,R01O5,CV1U7 | Minor | [UNVERIFIED] | open | no |
| G19 | Full ordinary-launch owner -> Run -> workers -> upward liveness/report/completion lifecycle and correlation absent | R03G6,R02G17,R05,R06,R07,R08 | Minor | open question | open | no |
| G20 | Exact installed/development whole-build equivalence not certified despite corroborated specific routing paths | R02G1,R03,CV1 | Minor | [UNVERIFIED] | open | no |
| G21 | Raw historical P0 worker transcript observations not independently replayed; absence of forbidden calls not tested rejection | R03G8,R06P0,R08P0 | Minor | [UNVERIFIED historical] | open | no |
| G22 | Workspace-lineage backing writer/table not found; schema/projection/host-instance validation known, not merely cosmetic | R03G9,G13 | Minor | [UNVERIFIED backing] | open | no |
| G23 | Default check wait wake, missed-answer cause, attention categories/detection delay, typed input during active tool and concurrent mailbox consumers | R01G7,R02G11-15,K196-200 | Minor | [UNVERIFIED] | open each five subjects | yes |
| G24 | Complete backend validation of referenced report files not traced; coordinator must read returned contracts/artifacts | R02G16,R05receipt | Minor | [UNVERIFIED] | open | no |
| G25 | #431 historical eight incidents actually eliminated/timing bounds met, not proved by merged procedural #434 | R02G3,R08#431 | Minor | [UNVERIFIED] | open | yes |
| G26 | v2 C10-C14 monitor/hooks/dashboard/context/persistent-budget mechanisms delivery elsewhere not audited; future-tense not stale solely absent | R02G20,CV1U1 | Minor | [UNVERIFIED] | open | no |
| G27 | Trusted role/parent/scope capability absent in hook binding records, no authority from names | R04role,R01G12,R07,R08 | Minor | open question | open | no |
| G28 | U7 Orca preamble visibility/authoritativeness to hooks; actual subagent parent/session envelope | R04rows1,3,R02,CV1U9 | Minor | [UNVERIFIED] | open | yes |
| G29 | U28 Orca hooks/L2 pre-push installation is separate from preamble question, runtime resolution not investigated | R04row2,D377,457 | Minor | [UNVERIFIED] | open | no |
| G30 | Concurrent whole-input hook rewrite ordering/live cwd/job identity behavior; Linux same-user process selection not sandbox/daemon-proof | R04rows4,10 | Minor | [UNVERIFIED] | open | yes |
| G31 | Complete claim-to-binding/first-tool timing and child environment effectiveness not proved by claim-process preflight | R04row5,R05I1314-1320/IS92 | Minor | [UNVERIFIED] | open | yes |
| G32 | Whole-copy parity/universal installed freshness vs targeted token/hash groups; no sync/build/install/test runs | R04row9,R05,R07G13,R08 | Minor | [UNVERIFIED universal] | open | no |
| G33 | D1-D4/git and exact WC13 were unverified only within mechanics/hooks slices, established package-wide R01/R06 records; not missing live tests | R03G7,R04row6,R06 | Minor | [UNVERIFIED slice-local]/open question | open only extension/permission decision; existing policy established | no |
| G34 | Task-specific user commit grants not inheritable, outward owner/PR/human Ruling cannot be inferred from delegated role/token; new transitive policy absent | R01G11,G15,R06,R08 | Minor | open question | open extension, existing prohibition applies | no |
| G35 | Orca-calling orchestrator entrypoint exception/packaging command vs session-role vs wrapper; ordinary command universal description conflicts actual claim helper | R01G16,R07G9,R08 | Minor | open question/[CODE-CONTRADICTED universal implementation] | open | no |
| G36 | D3 ordinary PR-session automatic/consistent placement not demonstrated | R05L4/gaps | Minor | [UNVERIFIED] | open | yes |
| G37 | PM/agent/issue helper role/output/tier compliance and PM always-active startup registration not verified | R05L2,L5,L7/gaps | Minor | [UNVERIFIED] | open | yes |
| G38 | Watcher launch reply operation-ID fields/unknown-error string and lost-response assumptions explicitly not verified | R05WL39-48 | Minor | [UNVERIFIED] | open | yes |
| G39 | Sprint isolation env not hard filesystem/authority sandbox, subprocess permission bypass not safe authority precedent | R05SE/PP/gaps | Minor | [UNVERIFIED] | open | no |
| G40 | Actual held-message permission-mode matching/sender bypass identification/inbound interception or script-file fallback validator | R08R20-24,R30-32 | Minor | [UNVERIFIED] | open; allocated web01 | no |
| G41 | Typed protocol fixed types/IDs/worktree/branch/inert detail not established; existing Orca type set differs and body format gives no settlement | R08R22-24,R03types | Minor | [UNVERIFIED] | open | no |
| G42 | Grant library choice/macaroons-vsBiscuit/CaMeL claims, offline chain/attenuation/expiry/session/replay nonce/destructive caveats not established | R08R25-29,R33-34 | Minor | [UNVERIFIED] | open; allocated web03 | no |
| G43 | Existing Dispatch capability forwarding exists but semantics/attenuation/fit for new grants not traced; no-capability claim would overstate | R08SEND-CODE59-60 | Minor | [UNVERIFIED suitability] | open | no |
| G44 | #339 unimplemented scale10-20 target, persistent registry,6hsweep/attention3-5min/staticreport/server/push+closed-session cleanup predicates;40h estimate not measured | R08R01-17,R35 | Minor | [UNVERIFIED] | open proposal, not validated capacity | no |
| G45 | #423 knowledge-sharing release distinct from hierarchy; administrative v2 numbering decision not found | R08§3,R01-35classification | Minor | open question | open administrative only; semantic distinction established | no |
| G46 | #409 remote prototype/code/tests/version/schema/live collector absent locally/unverified; observer not controls, synthetic scale not capacity | R08#409 | Minor | [UNVERIFIED] | open | no |
| G47 | #446 lock experiment/environment claims not rerun and requested bounded wait absent; remaining #326 Git/submodule/per-task commit work not established | R08#446/#326 | Minor | [UNVERIFIED] | open independent followups | no |
| G48 | P2 merged static conversion not P2 live acceptance; live phase report not found in bounded search | R06P2,R08PR422 | Minor | [UNVERIFIED] | open | no |
| G49 | Security-literature/benchmark assertions in issue sketch not independently validated | R08R33/gaps | Minor | [UNVERIFIED] | open; allocated web02/03 | no |
| G50 | Universal automation/disposable reports/universal worktree creation/table replacement/supervisedfanout proposals conflict current protections | R08conflicts,R05 | Minor | [CODE-CONTRADICTED] | open scope/policy decisions, no code changes authorized | no |
| G51 | General ownership wording not a full runtime role/authority/reporting protocol and diagrams' orchestrator/worker labels not Orca supervisor proof | R01,R04,R05,R07,R08 | Minor | [UNVERIFIED role]/[CODE-CONTRADICTED interpretation] | open | no |
| G52 | Guard executable coverage and required unlisted supervision probes had overbroad research claims; actual literalorca scope/read list now explicit | R04/05/07B1B2,qa/qa-phase-2-fix-log.md,phase2verifiers | Minor | [CODE-CONTRADICTED old research claim] | resolved in Phase2fixcycle1; source policy-design questions still open | no |
| G53 | Archived residual867lines/274paths unread; search counts/notes are provenance not independently read runtime observations | R07ledger/supplements | Minor | [UNVERIFIED background] | open archival background outside approved current inventory | no |
| G54 | Earlier summary's no-local-routing/current-six-routeunknown and lifecycle-vocabulary imprecision/transaction wording require using strongest source and rawcorrect detail | CV1/CV2,C3M3/M5,R03,R06 | Minor | open question/[STALE DOC index wording] | open notes only; actual source facts established | no |

## Stale documentation found
| # | Source statement | Source file(s) | What current code or policy shows | Status |
|---|---|---|---|---|
| S01 | Original D5option-b:3,22 command-owned workers/command rewrite | R01,R06 (D5B/REC/merged aliases) | Final scopedREC48/D5merged76 uses worker-session helpers/no command edits; command ban remains | open historical interpretation, not current permission |
| S02 | D5option-b:13 raise removes fence | R01,R06,R03 | Installed depth helper retains configurable positive max/invalid fallback; raising2 not disabling | open stale wording |
| S03 | D5REC:3 spec not edited | R06,R07 | AppliedSPEC81,405/currentWC13 exists | open historical-only drafting status |
| S04 | D5REC:64 none edits applied | R01,R06,R07 | SPEC81,98,276,315,386/disposition48-58 application | open historical-only drafting status |
| S05 | REC67-72 other decisions running/git stub | R01,R06 | APPROVED8-13/SPEC401-407/currentcontract settles D1-D5/git | open historical status |
| S06 | REC9 coordinator precondition never stated | R06 | SPEC386,405/contract69 person-opened | open old diagnosis |
| S07 | REC10 worker session lacks rule | R06 | Current contract62 explicit WC13 | open old diagnosis |
| S08 | CR01:3 not applied | R06 | SPEC79,88/currentcontract47,220-225 applied placement/isolation | open historical status |
| S09 | D5-A19 P0smokeruns trigger | R06 | SPEC405 composite brief AND material runtime-only split; D5plan95-105 replaces | open superseded trigger |
| S10 | REC20,48 brief only one command | R06,R07 | SPEC86/contract204-216,288-289 multiCommand chains; disposition105 D1 layout wins; still not helper-authorizing brief | open historical cost premise |
| S11 | REC oldSPEC79/350-354 references | R01,R06 | CurrentSPEC79 WC11,84-86brief,405D5 | open shifted anchors |
| S12 | AppliedSPEC88/CR01:24 defaultsetup-run | R01,R06,R08 | Newer contract221 setupskip default/specific user authorization | open doc discrepancy, no setup execution authorized |
| S13 | AppliedSPEC61 never-worker list omits issue | R01 | Currentcontract23 includes issue; current testset authoritative | open old inventory |
| S14 | CR01:19 PRworker trigger/per-PR workeroptin | R06,R08 | Currentcontract23,232 PR neverworker; APPROVED18 drops optin | open historical proposal |
| S15 | CR01:15 unconditional issue/PR metadata links | R06 | Currentcontract230 fork/no Orca links while upstreamidentity, disposition102 drops text | open historical guidance |
| S16 | EVAL326:80 depth1 stops workers starting workers broadly | R03,R06 | Fence counts Dispatch generations, ordinary agent/worktree launch outside; independent coordinator authority task-create still applies | open narrowed interpretation |
| S17 | D5REC48,69,84 local helper questions defaultrootRun prediction | R03 | Current installedB640/2677/2698 active creatorDispatch/default then Run fallback, local only; remote separate | source-reconciled, live remains untested |
| S18 | CAPS103/Scope03:108,121 unresolved task-create depth | R03 | Current taskCreate CU authority/createTask no depthcheck, source settles without mutation | source-reconciled |
| S19 | Scope02:83 onlyWC13 fence for creatingTask in Run | R03 | Current coordinator ownership check independent depth | source-reconciled overbroad permission |
| S20 | Scope03 lineage onlycosmetic | R03 | Host/instance validity checks source verified; still not lifecycle authority | source-reconciled |
| S21 | InstalledCLI specsorchestration78-80/askhelp owningRun default blanket | R03 | Native local-helper creatorDispatch exception implemented | open help discrepancy |
| S22 | P0trace historical bundle/symbol/helperline anchors | R01,R03,R06,R08 | Recorded oldbundle absent; current helper default/root at7/9 validation21-26 not11/13/30-35; R03 freshly reconfirmed broad source classifications | open historical-citation limit, not erased trace |
| S23 | OlderSPEC78-84 complete current liveness model | R02 | Currentcontract58-65,95-200 includes WC14/15,pending_ack,S11; tests199-252 phrasepin | open spec incompleteness |
| S24 | LivenessdesignCtable547-557 oldanchors WC10:44/WC12:59/WC11:45 | R02 | Currentcontract46/61/47 | open citation drift |
| S25 | Issue446 lock rule pointer44 | R02,R06,R08 | Currentcontract45; substance immediateblock remains, requestedwait not implemented | open citation drift |
| S26 | D5history originalP1report8FAIL treated final | R06 | APPROVED79-83 laterPASS/acceptedexceptions; Skillinvocation currentcontract60 | open historical-disposition qualification |
| S27 | DEV-GUIDE985 P0emptyunattended inventory as current | R07,R08 | PopulatedUNATTENDED_EXPECT/frozenset746;31headings31files;contract303-304=16+15; historicalAtP0 canremain | open current-state summary stale |
| S28 | issue-watcherdesign68 WC13 at61 | R07 | Currentcontract61 WC12,62 WC13 | open citation drift |
| S29 | #339accuracyC4 PR422 open/unmerged | R08 | Forkread merged2026-11-07T14:15:58Z, static not live | open historical state claim |
| S30 | #339accuracy oldlivenessbaseline | R08 | Currentcontract95-200/tests199-253 newer procedural supervision; not actual incident elimination | open baseline qualification |
| S31 | DEV-GUIDE980 universal no-Orca implementation description | R08 | Actual coordinator-only claim helper subprocesses create/agent-launch; worker prohibition remains | open architectural boundary tension |
| S32 | CORE55-59 universal atomic create-with-agent | R05,R08 | Claim script intentional two-stagecreatewithoutagent then launch; ordinary exception not workerpermission | open universal wording qualification |
| S33 | Spawn176-182 execution-oriented prose vs192-210boundary | R05 | Explicit command stops after decomposition, no persistentlauncher established | open candidate ambiguity, not verified absent elsewhere |
| S34 | DP/DI diagram orchestrator/worker interpreted layeredOrca supervisor | R05,R08 | Skill orchestrator/Agenthelpers, ordinary external launch not Task/Dispatch delegation | interpretation source-reconciled, no new productfeature |
| S35 | PriorF1 every agent-launched no-preamble session automaticallyordinary/coordinator | R08,R01 | Contract11 explicitly describes USER-started ordinary,69 person-opened coordinator; other role classification undefined | interpretation corrected |
| S36 | Guard all-executables/allreadoperations blocked/allowed categories blanket in research | R04/05/07B1B2;Phase2fixlog | Literalorca recognition and explicit allowedreads differ; worker-list/read/worktreeps required but not listed; other classifications maydeny, no bypassproof | resolved researchaddenda Phase2cycle1, immutable originals retained |
| S37 | Nine lifecycletypes / beforetransaction compressedindexprecision | CV1,C3M5/R03 | Nine supported MESSAGE types; source begins transaction, resolves depth before COMMIT/rollsback. Rawreturn correctlyqualified | open minor index wording, no separatefix |
| S38 | Currentinventory remains incomplete because old07closingstatus says partial | CV2,R07approval | User narrowed to current sources/tests/copies; activeinventorycomplete, archivedresidualunverified | scope precedence resolved; historicalwords retained |

Not stale solely absent or unimplemented: U7preamble/U28installation resolution, ownership role words as instructions, future C10-C14 proposals, intentional D5restriction. Do not mark their runtime capabilities implemented; their exact uncertainty and design questions are in G02/G26-G30/G51. No confirmed stale designESCAPE-list claim in original04inspected passages, but classifier executable ceiling and missing-probe integration are established separately.

## External research allocation and carry-forward controls
Phase4 allocations: web01 ClaudeCode sender/receiver permission classes/held messages/inbound hooks (G40-G41); web02 hierarchical/supervision design value/failure/cost tradeoffs (G04-G09,G25-G26,G44,G49); web03 macaroon/Biscuit/CaMeL narrowing/verification/library feasibility (G34,G42-G43,G49); web04 Orca public nested-depth/helper evidence and current guide discrepancies (G12-G18,G23,G29). External sources supplement, never override current code. User approved read-only research only, no live experiments/setting/model-tier changes.

All54gaprows and38stale/interpretationrows are semantic dedup groups, not54+38independent defects. Every original gapregister/QA family is covered by these groups or specifically noted as package-source-resolved with remaining live uncertainty. Exact raw tables/source aliases/line evidence remain referenced in each originating research file and qa/returned records. Synthesis must use currentB1B2addenda and source hierarchy. Future implementation risks are not minimized by research-gate Minor grading. Existing evidence of native local creator routing is a current source fact; lack of live proof is a distinct unresolved question. Final decision and quality gates remain pending; this log compiles evidence, does not implement conclusions.
