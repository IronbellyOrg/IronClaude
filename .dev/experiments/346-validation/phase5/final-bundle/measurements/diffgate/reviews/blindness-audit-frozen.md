# Frozen endpoint: independent specification panel audit
review: 1 of 3

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/history/spec-v3-after-round2.md
  comparison_original: .dev/orca-command-refactor/specs/history/spec-v1-draft.md
  review_date: '2026-11-09'
  instrument: 'sc:spec-panel-armb --mode critique --focus requirements,architecture'
  review_kind: independent first review of the full frozen endpoint
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
  endpoint_sha256: 75a628e35b00eb23bde80d0190f6cf735f3b298c8f3b228caf05f65ee094ac9a
  original_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
  hash_check: both matched before review
quality_assessment:
  overall_score: 6.5
  clarity: 8
  completeness: 6
  testability: 6
  consistency: 5
  architecture: 7.5
  scoring_note: 'Qualitative panel estimates, not a measured benchmark.'
  findings_total: 4
  blocking_findings: 4
  critical_count: 0
  major_count: 4
  minor_count: 0
  classifications: {fix_written: 2, present_since_original: 2, unverified: 0}
critical_issues:
  - {id: 1, category: requirements, severity: MAJOR, expert: Wiegers, issue: 'All-command first-phase promise precedes later gate and safety conversion', recommendation: 'Align flag eligibility and acceptance with actual per-command delivery phases'}
  - {id: 2, category: architecture, severity: MAJOR, expert: Fowler, issue: 'Nested reflect calls lack newly mandatory per-child report directories', recommendation: 'Specify distinct report-directory forwarding for each child'}
  - {id: 3, category: requirements, severity: MAJOR, expert: Adzic, issue: 'Universal blocked gate test conflicts with safe-default continuations', recommendation: 'Assert the actual resolution branch for each command'}
  - {id: 4, category: architecture, severity: MAJOR, expert: Nygard, issue: 'Retry relocation leaves archived report pointers targeting reused paths', recommendation: 'Preserve report and artifact pointer identity across output relocation'}
expert_consensus:
  - 'Keep Orca coordination outside commands and preserve standalone defaults.'
  - 'The four open MAJOR findings have concrete incorrect outcomes and block this review.'
  - 'No new orchestrator, nesting-depth change, cloud infrastructure or implementation is required by this audit.'
improvement_roadmap:
  immediate: ['Resolve findings 1-4 in a separately authorized revision, not in this audit.']
  short_term: ['Validate phase eligibility, nested report isolation, default-resolved gate results and archived pointer resolution during the existing rollout checks.']
  long_term: ['No additional program or speculative feature recommended.']
adversarial_analysis:
  findings_section: 'Adversarial Analysis'
  methodologies_applied: ['Zero/Empty', Divergence, 'Sentinel Collision', Sequence, Accumulation]
  guard_table: 'Guard Condition Boundary Table'
  quantity_flow: 'Quantity flow analysis'
```

## Scope and evidence discipline
The endpoint and original are the two frozen files named in the metadata. Both SHA-256 checks matched the assigned values before the skill was invoked. The full endpoint is reviewed as a first review, not as a limited re-review: no previous findings or review-count history informed selection. The original is used only for the requested direct anchor comparisons, not as a source of expected defects. The current live specification, earlier review reports, the partial blindness audit and the diffgate-loop directory were not opened.

The governing report format is the installed Arm B command at `/home/coder/.claude/commands/sc/spec-panel-armb.md`, whose standard-format YAML keys are retained above. Its critique rules, numbered findings and mandatory markdown boundary-table template govern the sections below. The header and entire section skeleton were written before gathering findings, then populated in place. The panel uses 11 simulated expert perspectives through native reasoning, not 11 independent people or model calls. This is an audit only: no implementation, improved specification, fix cycle or external publication is authorized.

Evidence aliases throughout this report: **E** = `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md`; **O** = `.dev/orca-command-refactor/specs/history/spec-v1-draft.md`. A citation such as `E:159` names that exact repository-relative file and line, not the live spec. Findings also include full paths. CRITICAL and boundary-table GAP findings are blocking; other MAJOR findings are blocking only when a concrete wrong result is shown. MINOR notes do not fail the review. Textual origin labels describe the compared anchors only, not proof that a particular earlier revision caused the defect.

## Expert review in instrument order
The following are simulated analytical lenses, applied in the instrument's fixed sequence. They are not quotations from the named real experts.

| Order | Expert lens | Review contribution and interaction |
|---|---|---|
| 1 | Karl Wiegers, requirements | Traced universal unattended promises into phase scopes and acceptance checks. The first-phase all-command surface does not align with later gate/safety delivery (finding 1). The explicit worker_status vocabulary and standalone invariants are otherwise substantially clearer than inferred behavior. |
| 2 | Gojko Adzic, examples | Ran the cleanup example with an allowed import and a deferred fixture, and the research planning example. These expose a test that demands blocked even for default-resolved gates (finding 3). Distinguished a failed audit verdict from failed execution as the contract requires. |
| 3 | Alistair Cockburn, actors/use cases | Separated coordinator dispatch/retry, worker lifecycle, command work and human Ruling authority. Kept the user's decisions genuinely separate from implementation. Checked that the recommended coordinator-only PR choice is compatible with what earlier phases require; it is not yet fully consistent (finding 1). |
| 4 | Martin Fowler, architecture | Supported keeping commands independent of Orca and retaining a shared contract. Followed the new mandatory report parameter through the existing tasklist-to-reflect call; one added switch is not a complete call migration (finding 2). |
| 5 | Michael Nygard, reliability | Examined retries only after proven stop, same-message ask resumption and fixed report locations. Found that rename-and-reuse preserves file bytes but not archived evidence references (finding 4). No live runtime fault injection was performed. |
| 6 | James Whittaker, adversarial probing | Applied empty/missing report arguments, default-versus-blocked divergence, quoted-switch sentinel collision, retry sequence and N-child accumulation attacks. Preserved the now-explicit quoted-data distinction rather than reporting a defect already excluded by endpoint text. |
| 7 | Sam Newman, interface evolution | Confirmed separate worker_status avoids reusing existing status semantics. Challenged whether the generic shared contract alone cures phase timing and nested argument wiring: it states the invariant, but does not reconcile the conflicting rollout or supply the missing child argument allocation (findings 1 and 2). |
| 8 | Gregor Hohpe, message/data flow | Traced report pointers from command through worker_done to coordinator reads and then across retry relocation. A path reused for another attempt is not a stable identity for archived evidence (finding 4). Retained top-level-only lifecycle ownership. |
| 9 | Lisa Crispin, testability | Cross-checked six boundary classes for each enumerated predicate family and mapped every GAP to a concrete finding. Rejected a universal blocked assertion for safe-default branches (finding 3); noted that static wording assertions alone cannot prove complete unattended behavior. |
| 10 | Janet Gregory, quality practice | Kept the distinct tests for missing-answer block, safe default and forbidden-mode refusal separate. Confirmed no need to reopen user decisions or request a new fix round during this audit. The report recommends changes but changes no specification. |
| 11 | Kelsey Hightower, operations | Checked operator-visible outcomes, report paths, liveness, placement and finite waits. Accepted local-only scope and deferred remote/model tuning as explicit non-goals; no cloud infrastructure or new orchestration program is needed to address these findings. |

**Collaboration and limits of consensus:** The panel agrees with the coordinator/command boundary and does not recommend the rejected nested-Orca alternative. It tested the strongest contrary readings: universal contract rules can guide a careful implementer to supply missing child arguments or convert gates early, but those inferred repairs exceed the specific rollout/caller instructions, which is why the affected findings are MAJOR incompleteness/consistency defects, not claims of an already observed runtime failure. Similarly, knowing the archive suffix allows a human to locate old files manually, but does not make the archived report's original pointers correct. No separate minor wording/citation finding is counted. The declared pre-baseline direct-run evidence gap remains a stated gap, not an invented new defect.

## Guard Condition Boundary Table
| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| Mode token | E:51,146,228 | Zero/Empty | No unattended token | false | Preserve attended defaults | OK |
| Mode token | E:51 | One/Minimal | One unquoted standalone `--unattended` | true | Select unattended contract | OK |
| Mode token | E:51,62 | Typical | Quoted topic plus unquoted switch and report directory | true | Run unattended and write contract | OK |
| Mode token | E:51 | Maximum/Overflow | Many data arguments, switch still standalone | true | Selection depends on token position, not topic length | OK |
| Mode token | E:51 | Sentinel Value Match | Topic contains quoted `--unattended` | false | Treat text as data | OK |
| Mode token | E:51 | Legitimate Edge Case | Quoted switch text plus a separate unquoted switch | true | Separate standalone token selects mode | OK |
| Lifecycle authority | E:50,65-66,213-219 | Zero/Empty | No preamble | false | Ordinary session sends no lifecycle message | OK |
| Lifecycle authority | E:50,65 | One/Minimal | One top-level worker with Task and Dispatch | true | Worker owns its lifecycle messages | OK |
| Lifecycle authority | E:65-66 | Typical | Worker command internally uses Agent helpers | false for helpers | Helpers do work, top-level worker reports | OK |
| Lifecycle authority | E:33,66,250-252 | Maximum/Overflow | Depth-1 worker tries another Orca worker | false | Command must not dispatch; depth remains 1 by default | OK |
| Lifecycle authority | E:65 | Sentinel Value Match | Agent helper has copied lifecycle identifiers | false | Copying identifiers does not make it top-level | OK |
| Lifecycle authority | E:50,65 | Legitimate Edge Case | Person uses an Orca tab without a Dispatch | false | Ordinary session, no worker lifecycle | OK |
| Startup prompt limit | E:59 | Zero/Empty | No startup prompt | false | Startup may reach readiness directly | OK |
| Startup prompt limit | E:59 | One/Minimal | Prompt falls back promptly | true | Automatic fallback, no indefinite person wait | OK |
| Startup prompt limit | E:59 | Typical | Documented 30-second fallback | true | Readiness succeeds in cited observation | OK |
| Startup prompt limit | E:59 | Maximum/Overflow | Prompt waits beyond readiness budget | true | Not allowed by launch contract | OK |
| Startup prompt limit | E:59 | Sentinel Value Match | Default 60-second readiness limit | true | Fallback must occur well inside it | OK |
| Startup prompt limit | E:59 | Legitimate Edge Case | Above about 45 seconds in cited test | true | Recorded failure, not a promised safe fallback | OK |
| Gate resolution | E:60,95 | Zero/Empty | Needed answer absent, no documented default | true | Write blocked report and exact question; stop | OK |
| Gate resolution | E:60 | One/Minimal | Caller supplies required value | false | Continue without local prompt | OK |
| Gate resolution | E:60 | Typical | Documented safe default exists | false | Use that default | OK |
| Gate resolution | E:60 | Maximum/Overflow | Multiple unmet person gates | true | First unresolved gate stops with question | OK |
| Gate resolution | E:60 | Sentinel Value Match | Would call AskUserQuestion or STOP AND WAIT | true | Replace with default, caller value or blocked report | OK |
| Gate resolution | E:60,63 | Legitimate Edge Case | Audit completes with negative verdict | false | Completed audit need not be a blocked run | OK |
| Ask continuation | E:61 | Zero/Empty | No coordinator answer yet | true | Wait in ask, not a local prompt | OK |
| Ask continuation | E:61 | One/Minimal | One answer received | false | Reinvoke or resume using answer as a flag | OK |
| Ask continuation | E:61 | Typical | First ask times out with message ID | true | Resume same message ID | OK |
| Ask continuation | E:61 | Maximum/Overflow | Repeated timeouts | true | Continue same question, no duplicate asks | OK |
| Ask continuation | E:61 | Sentinel Value Match | Timeout or disconnect | true | Neither creates a new question | OK |
| Ask continuation | E:61 | Legitimate Edge Case | Long blocking ask exceeds heartbeat interval | true | Ask itself supplies liveness, no heartbeat needed | OK |
| Report-directory prerequisite | E:62 | Zero/Empty | Unattended switch, report directory absent | true | No work, no file, error names missing flag | OK |
| Report-directory prerequisite | E:62 | One/Minimal | One valid report directory | false | Create directory if needed and write contract | OK |
| Report-directory prerequisite | E:62 | Typical | Output and report directories differ | false | Command output semantics stay separate | OK |
| Report-directory prerequisite | E:62,122 | Maximum/Overflow | N reflect children receive only unattended switch | true for each child | Every child stops before audit; caller passes no child report directory (finding 2) | GAP |
| Report-directory prerequisite | E:62 | Sentinel Value Match | Report absent after missing-flag stop | true | Worker reports failed under outcome mapping | OK |
| Report-directory prerequisite | E:62,87,90 | Legitimate Edge Case | Command output is a file, report location is a directory | false | Keep both distinct | OK |
| Existing-contract coexistence | E:62 | Zero/Empty | No existing command contract | false | Write worker contract separately | OK |
| Existing-contract coexistence | E:62 | One/Minimal | Existing contract at worker report path | true | Add top-level worker fields, preserve existing fields | OK |
| Existing-contract coexistence | E:62 | Typical | Existing contract elsewhere | false | Preserve it; write separate worker contract listing it | OK |
| Existing-contract coexistence | E:62 | Maximum/Overflow | Many artifact files | false | List every other file in artifacts | OK |
| Existing-contract coexistence | E:62 | Sentinel Value Match | Existing status uses command-specific vocabulary | true | Use distinct worker_status field | OK |
| Existing-contract coexistence | E:62 | Legitimate Edge Case | Stop before main deliverable exists | false | Worker contract still written when report directory was supplied | OK |
| Result/outcome mapping | E:62-63 | Zero/Empty | No report exists | true for failure | Send failed outcome | OK |
| Result/outcome mapping | E:62-63 | One/Minimal | Command result success | false for failure | worker_status succeeded, succeeded outcome | OK |
| Result/outcome mapping | E:62-63 | Typical | Command result partial | false for failure | Preserve partial in report, succeeded lifecycle outcome | OK |
| Result/outcome mapping | E:62-63 | Maximum/Overflow | Stop value outside successful result set | true for failure | Other stop values map to failed | OK |
| Result/outcome mapping | E:62-63 | Sentinel Value Match | WC-2 gate produces blocked | true for failure | blocked report, failed lifecycle outcome | OK |
| Result/outcome mapping | E:63 | Legitimate Edge Case | Successful audit, verdict FAIL | false for failure | Report negative audit verdict but succeeded lifecycle outcome | OK |
| Retry/resume path | E:64,73,76 | Zero/Empty | Initial failed attempt has no output | false for existing-output rename | Re-run can start clean; no earlier deliverable to preserve | OK |
| Retry/resume path | E:64 | One/Minimal | One failed non-resumable attempt with output | true | Rename its report and output before retry | OK |
| Retry/resume path | E:64 | Typical | Resumable attempt and resume flag | false for output relocation | Resume disk state, archive worker report | OK |
| Retry/resume path | E:64 | Maximum/Overflow | Several positively failed retries | true | Dispatch-qualified archive names keep attempts apart | OK |
| Retry/resume path | E:64 | Sentinel Value Match | Archived contract still names original output path | true | Output is renamed but contract pointers are not rebound; after retry they select new evidence (finding 4) | GAP |
| Retry/resume path | E:64 | Legitimate Edge Case | Answer continuation inside same Dispatch | false for new attempt | Replace blocked report in same directories | OK |
| Skill loading | E:65,184 | Zero/Empty | Command names no skill | false | Execute command's own protocol | OK |
| Skill loading | E:65 | One/Minimal | Command names one skill | true | Load with Skill tool before command work | OK |
| Skill loading | E:65,184 | Typical | Worker brief wraps slash command | true | Explicit Skill invocation still required | OK |
| Skill loading | E:65 | Maximum/Overflow | Command has its own many helpers | true at worker entry | Keep internal fan-out but invoke entry skill top-level | OK |
| Skill loading | E:65 | Sentinel Value Match | Read command and imitate protocol from memory | true | Does not satisfy top-level invocation requirement | OK |
| Skill loading | E:65,184 | Legitimate Edge Case | Skill call appears after first command output | true | Transcript acceptance fails | OK |
| Outward authorization | E:67,100,113-114,121,244-247 | Zero/Empty | No explicit authorization flag | false | Outward defaults off | OK |
| Outward authorization | E:67,245 | One/Minimal | One action named by user and flagged in brief | true under recommended choice | Only that task's action authorized | OK |
| Outward authorization | E:67,100 | Typical | PR review without explicit post flag | false | No GitHub posting in unattended mode | OK |
| Outward authorization | E:67,245 | Maximum/Overflow | Many action flags, no matching user instruction | false under recommended choice | Coordinator may not invent authority | OK |
| Outward authorization | E:246 | Sentinel Value Match | User chooses never authorize worker outward actions | false | Coordinator or person performs them | OK |
| Outward authorization | E:139,240-241 | Legitimate Edge Case | User keeps pr-submit coordinator-only | false for worker eligibility | No pr-submit changes in final phase, conflicting with all-command first-phase coverage (finding 1) | GAP |
| Work-wait splitting | E:68,104,114,210 | Zero/Empty | No long tool wait | false | Heartbeat on normal cadence | OK |
| Work-wait splitting | E:68 | One/Minimal | One wait under four minutes | false | Can heartbeat between calls | OK |
| Work-wait splitting | E:114,210 | Typical | PR polling uses short iterations totaling 600 seconds | true for cumulative monitoring, false for one long call | Heartbeat between iterations | OK |
| Work-wait splitting | E:68,104 | Maximum/Overflow | Eval would hold one call for 3600 seconds | true | Split eval waits to at most four minutes | OK |
| Work-wait splitting | E:68 | Sentinel Value Match | One ordinary call longer than five minutes | true | Must split; PR-specific acceptance additionally caps at 240 seconds | OK |
| Work-wait splitting | E:61,68 | Legitimate Edge Case | Blocking ask, not command computation | false | Ask provides liveness independently | OK |
| Parallel write ownership | E:69,85,119 | Zero/Empty | One writer, no overlap | false | Normal command writes | OK |
| Parallel write ownership | E:69 | One/Minimal | Two writers with distinct slugs | false for collision | Distinct output files | OK |
| Parallel write ownership | E:69,119 | Typical | Two save workers | true for shared-key protection | Write only per-session files | OK |
| Parallel write ownership | E:69,85 | Maximum/Overflow | Two cleanup audits in one worktree | true | One audit per worktree at a time | OK |
| Parallel write ownership | E:69 | Sentinel Value Match | Single-owner memory key | true | Never write in unattended mode | OK |
| Parallel write ownership | E:69,73 | Legitimate Edge Case | Source edits would overlap despite distinct reports | true | Invariant forbids shared-file writes; exact placement/serialization remains a planning obligation, not a new defect finding | OK |
| Follow-up/fencing | E:70 | Zero/Empty | Empty check | false | Continue task | OK |
| Follow-up/fencing | E:70 | One/Minimal | One coordinator follow-up | false for fence | Check at checkpoint and process task direction | OK |
| Follow-up/fencing | E:70 | Typical | Worker reaches final checkpoint | false for fence | Check before worker_done | OK |
| Follow-up/fencing | E:70 | Maximum/Overflow | Multiple checkpoints | false for fence | Keep checking while working | OK |
| Follow-up/fencing | E:70 | Sentinel Value Match | consumer_fenced | true | Stop without worker_done | OK |
| Follow-up/fencing | E:70 | Legitimate Edge Case | Fence arrives just before completion | true | No completion from fenced worker | OK |
| Interactive-mode refusal family | E:83-84,89,102-103,108,110,118,123 | Zero/Empty | No interactive switch, no socratic/interactive mode, no watch | false | Default finite non-interactive path | OK |
| Interactive-mode refusal family | Same locations | One/Minimal | One forbidden switch or mode | true | Refuse it in unattended mode | OK |
| Interactive-mode refusal family | Same locations | Typical | Ordinary noninteractive command with report directory | false | Continue using its row's rules | OK |
| Interactive-mode refusal family | Same locations | Maximum/Overflow | Many forbidden switches together | true | Refusal remains required, no local prompt or unending watch | OK |
| Interactive-mode refusal family | Same locations | Sentinel Value Match | `--interactive`, business socratic, explain interactive, or test watch | true | Apply the corresponding command-specific refusal | OK |
| Interactive-mode refusal family | E:146 | Legitimate Edge Case | Same switch in attended run | false for new refusal | Preserve standalone behavior | OK |
| Required-answer family | E:89-91,104-105,109,115,117,120 | Zero/Empty | Required answer/context absent | true | Block with exact question, not a local prompt | OK |
| Required-answer family | Same locations | One/Minimal | Smallest caller-supplied sufficient answer | false | Continue past that gate | OK |
| Required-answer family | Same locations | Typical | Valid full context and required flags | false | Run normal unattended path | OK |
| Required-answer family | Same locations | Maximum/Overflow | Several unanswered gates or three cli-portify approvals | true | Stop at an unresolved gate with review artifact/question | OK |
| Required-answer family | Same locations | Sentinel Value Match | Release custom scope/tasklist confirmation, TDD topic-only/nested question, troubleshoot deep short-input/fix offer, cli-eval missing suite/safety/W0/$1, any cli-portify approval, implement halt, recommend clarification, translation context, or TDD target_release | true | Corresponding per-command rule is blocked | OK |
| Required-answer family | E:61,109,232-236 | Legitimate Edge Case | Implement Ruling requested from another agent | true under recommended choice | Preserve deliberate Ruling prohibition; person resumes | OK |
| Required-output family | E:62,83-84,87,90,99,101-102,106-108,111,113,120,123 | Zero/Empty | Report directory absent | true | Missing report-directory error before work | OK |
| Required-output family | Same locations | One/Minimal | Report directory plus required file/directory output | false | Write both appropriate deliverable and worker contract | OK |
| Required-output family | Same locations | Typical | File-valued tdd/init-lite output | false | Never interpret output file as report directory | OK |
| Required-output family | Same locations | Maximum/Overflow | Many output artifacts, including document inline edits | false | Artifacts enumerates every other written file | OK |
| Required-output family | E:83,92 | Sentinel Value Match | Adversarial nested contract or generated workflow package | false | Preserve command contract and separate worker report as needed | OK |
| Required-output family | E:112,265 | Legitimate Edge Case | Load used inside another brief | false for independent report duty | No separate load worker or report | OK |
| Cleanup/improve approval | E:103,110 | Zero/Empty | No cleanup candidates | false | No approval-required edits | OK |
| Cleanup/improve approval | E:103,110 | One/Minimal | One item already allowed automatically | false | Apply and list changed file | OK |
| Cleanup/improve approval | E:103,110 | Typical | Mixed auto-fix and approval-required candidates | true for restricted items | Apply allowed items; list restricted ones unapplied | OK |
| Cleanup/improve approval | E:103,110 | Maximum/Overflow | All candidates require approval | true | Defer all, report them, do not prompt | OK |
| Cleanup/improve approval | E:103,110 | Sentinel Value Match | Item belongs to Approval Required category | true | Leave unapplied | OK |
| Cleanup/improve approval | E:103,110,146 | Legitimate Edge Case | Person explicitly uses interactive mode without unattended | false for new rule | Preserve existing approvals | OK |
| Research strategy pin | E:116 | Zero/Empty | Strategy flag omitted | true | Pin planning strategy | OK |
| Research strategy pin | E:116 | One/Minimal | One research topic | true | Planning does not clarify locally | OK |
| Research strategy pin | E:116 | Typical | Fully specified research request | true | Produce report and contract | OK |
| Research strategy pin | E:116 | Maximum/Overflow | Many research subtopics | true | Strategy remains planning, not a new person gate | OK |
| Research strategy pin | E:116 | Sentinel Value Match | Caller would otherwise select interactive strategy | true | Unattended pins planning | OK |
| Research strategy pin | E:116,146 | Legitimate Edge Case | Attended run without unattended switch | false | Preserve normal strategy selection | OK |
| Reflect remediation/promotion | E:88,151 | Zero/Empty | No remediate flag | false for authoring offer | Audit-only path | OK |
| Reflect remediation/promotion | E:88 | One/Minimal | Unattended remediate, auto-fixable findings | true | Reuse headless authoring auto-accept | OK |
| Reflect remediation/promotion | E:88 | Typical | Coordinator owns package moves | true for promotion suppression | Pass no-promote | OK |
| Reflect remediation/promotion | E:88,151 | Maximum/Overflow | Human-required remediation register | false for automatic repair | Reused headless rule preserves human-decision stop | OK |
| Reflect remediation/promotion | E:151 | Sentinel Value Match | Existing print-mode headless invocation | true for old rule | Behavior retained, not replaced | OK |
| Reflect remediation/promotion | E:88,151 | Legitimate Edge Case | Attended remediate invocation | false for unattended override | Original yes/no prompt retained | OK |
| Roadmap resume | E:118,205 | Zero/Empty | No resume flag, no state | false | Start fresh | OK |
| Roadmap resume | E:118,205 | One/Minimal | Existing session memory but no resume flag | false | Start fresh, no Resume prompt | OK |
| Roadmap resume | E:118 | Typical | Explicit resume flag with saved state | true | Resume after command/skill interface reconciliation | OK |
| Roadmap resume | E:118,205 | Maximum/Overflow | Many prior runs left state, but no resume flag is passed | false | Start fresh without the Resume prompt; no claim about choosing among competing state files | OK |
| Roadmap resume | E:118 | Sentinel Value Match | Resume? [Y/n] | false for unattended prompt | Replace with explicit flag | OK |
| Roadmap resume | E:118,146 | Legitimate Edge Case | Person runs without unattended | false for override | Existing standalone prompts remain | OK |
| Task confidence/tiers | E:121 | Zero/Empty | Confidence 0 | true for block | Report blocked | OK |
| Task confidence/tiers | E:121 | One/Minimal | Confidence 0.69 | true for block | Report blocked | OK |
| Task confidence/tiers | E:60,121 | Typical | Confidence 0.90, normal permitted work | false | Continue; any remaining gate still obeys generic resolution rule | OK |
| Task confidence/tiers | E:121 | Maximum/Overflow | TFEP tier with present-to-user or FULL STOP | true for block | Block instead of waiting locally | OK |
| Task confidence/tiers | E:121 | Sentinel Value Match | Confidence exactly 0.70 | false for below-threshold predicate | Below-0.70 block does not fire; other gates still apply | OK |
| Task confidence/tiers | E:121 | Legitimate Edge Case | EXEMPT commit/push or TFEP report commit | true for outward restriction | EXEMPT action needs authorization; TFEP report is not committed unattended | OK |
| Tasklist child invocation | E:122 | Zero/Empty | No-reflect set | false | Skip reflection stage | OK |
| Tasklist child invocation | E:62,122 | One/Minimal | One phase, child gets only unattended | true | Child lacks required report directory and does no work (finding 2) | GAP |
| Tasklist child invocation | E:62,122 | Typical | Multiple phase reflects, parent has report directory | true | Parent report directory is not specified as uniquely forwarded per child (finding 2) | GAP |
| Tasklist child invocation | E:69,122 | Maximum/Overflow | N parallel children reuse one report directory | true for collision | Distinct worker report files are required, but child allocation is not stated (finding 2) | GAP |
| Tasklist child invocation | E:122,146 | Sentinel Value Match | No unattended flag at parent | false | Stage 10.5 unchanged | OK |
| Tasklist child invocation | E:122 | Legitimate Edge Case | Child audit returns PARTIAL/FAIL | true for parent bookkeeping | Existing child verdict reporting remains; missing child audit is not a verdict substitute | OK |
| Workflow handoff/early stop | E:62,92 | Zero/Empty | Source missing before package creation | true for stop | Worker contract still written when report directory supplied | OK |
| Workflow handoff/early stop | E:92 | One/Minimal | Small change and handoff none | false for automatic execution | Generate package without execution handoff | OK |
| Workflow handoff/early stop | E:92 | Typical | Generated package plus separate report directory | false for location collision | Write own contract and worker contract | OK |
| Workflow handoff/early stop | E:62,92 | Maximum/Overflow | Many generated files | false | Enumerate artifacts | OK |
| Workflow handoff/early stop | E:92 | Sentinel Value Match | Retired output flag | true for legacy rejection | Never pass that flag in worker brief | OK |
| Workflow handoff/early stop | E:194 | Legitimate Edge Case | Initial live baseline before report flags exist | false for new flags | Use original report without unattended/report-directory flags | OK |
| Save key ownership | E:69,119,207 | Zero/Empty | No existing shared-key files | true for shared-write prohibition | Do not create single-owner keys | OK |
| Save key ownership | E:119 | One/Minimal | One session | false for per-session write | Write session-qualified memory file | OK |
| Save key ownership | E:119,207 | Typical | Two concurrent save workers | false for per-session writes | Two new per-session files | OK |
| Save key ownership | E:69,119 | Maximum/Overflow | Many concurrent save workers | true for shared-key protection | Never overwrite single-owner keys | OK |
| Save key ownership | E:119,207 | Sentinel Value Match | pm_context/last_session/next_actions | true | Preserve shared files | OK |
| Save key ownership | E:119,146 | Legitimate Edge Case | Attended save | false for override | Existing standalone memory behavior retained | OK |
| Worker eligibility and report exceptions | E:112,127-139,195 | Zero/Empty | Load alone as requested Task | false | Use as context step, not independent worker | OK |
| Worker eligibility and report exceptions | E:127-137 | One/Minimal | One of agent/git/help/pm/spawn/swarm-wizard | false | Coordinator/person only, no unattended section | OK |
| Worker eligibility and report exceptions | E:75-125 | Typical | Other section-3 worker candidate | true, subject to its rollout phase | Add report/contract according to scope | OK |
| Worker eligibility and report exceptions | E:139,240 | Maximum/Overflow | Several PRs, user retains recommended coordinator-only choice | false for pr-submit worker | Do not create PR-monitor worker surface | OK |
| Worker eligibility and report exceptions | E:241 | Sentinel Value Match | User explicitly chooses pr-submit worker | true after final-phase changes | Require authorization and finite monitoring | OK |
| Worker eligibility and report exceptions | E:124-125 | Legitimate Edge Case | validate-roadmap/validate-tests still have their listed worker-blocking defects | false | Resolve stated report/tool/target defects before treating command as ready | OK |
| Cleanup all-pass selection | E:85 | Zero/Empty | No all-pass selection; brief supplies pass 1 | false | Single-pass report | OK |
| Cleanup all-pass selection | E:85 | One/Minimal | One selected pass | false | Single-pass report, one audit per worktree | OK |
| Cleanup all-pass selection | E:85 | Typical | Explicit all-pass selection | true | Name the final all-pass report in the required repair | OK |
| Cleanup all-pass selection | E:85 | Maximum/Overflow | All passes requested, not just one | true | All-pass report naming applies; no invented numeric maximum | OK |
| Cleanup all-pass selection | E:85 | Sentinel Value Match | `--pass all` | true | Fixed final report name is required by the first-phase repair | OK |
| Cleanup all-pass selection | E:85 | Legitimate Edge Case | Another single pass N rather than all | false | Per-pass summary and checkpoint semantics remain | OK |
| Index update selection | E:86 | Zero/Empty | No mode=update | false | Normal index creation path | OK |
| Index update selection | E:86 | One/Minimal | One existing index and mode=update | true | Use command's update mechanism | OK |
| Index update selection | E:86 | Typical | Existing index updated explicitly | true | Update rather than an invented resume flag | OK |
| Index update selection | E:86 | Maximum/Overflow | Many previous updates, mode=update still selected | true | Update remains the named continuation mechanism | OK |
| Index update selection | E:86 | Sentinel Value Match | `mode=update` | true | Update existing index | OK |
| Index update selection | E:86 | Legitimate Edge Case | Existing index but no update selection | false | No automatic resume behavior is added by the spec | OK |
| Init marked-report overwrite | E:87 | Zero/Empty | No prior marked report at selected output | false | Initial report write | OK |
| Init marked-report overwrite | E:87 | One/Minimal | One prior marked report at selected output | true | Re-run overwrites its marked report | OK |
| Init marked-report overwrite | E:87 | Typical | Repeat invocation at same marked-report location | true | Overwrite as documented, not directory-based resume | OK |
| Init marked-report overwrite | E:87 | Maximum/Overflow | Many prior re-runs of the same marked report | true | Same overwrite behavior; no invented retry-count limit | OK |
| Init marked-report overwrite | E:87 | Sentinel Value Match | Command's own marked report is the existing file | true | Marked-report overwrite applies | OK |
| Init marked-report overwrite | E:87 | Legitimate Edge Case | Caller selects a different, unused output file | false | Initial write at explicit output; old report is not this target | OK |
| Knowledge-base unattended path | E:111 | Zero/Empty | No knowledge-base mode selected | false | Other index mode, generic unattended rules still apply | OK |
| Knowledge-base unattended path | E:111 | One/Minimal | Knowledge-base mode with one item, unattended | true | Required repair states it does not wait | OK |
| Knowledge-base unattended path | E:111 | Typical | Knowledge-base mode, unattended, normal repository | true | No person wait; output/contract required | OK |
| Knowledge-base unattended path | E:111 | Maximum/Overflow | Many knowledge-base entries, same mode | true | Still no person wait; no capacity limit invented | OK |
| Knowledge-base unattended path | E:111 | Sentinel Value Match | Knowledge-base mode selected under unattended | true | No-wait rule applies | OK |
| Knowledge-base unattended path | E:111,146 | Legitimate Edge Case | Person selects knowledge-base mode without unattended | false | No change to attended behavior; current waiting behavior remains explicitly UNVERIFIED | OK |
| Post-release prerequisites | E:113 | Zero/Empty | Neither command output nor pre-tag choice supplied | false | Block for missing prerequisites | OK |
| Post-release prerequisites | E:113 | One/Minimal | Only command output supplied | false | Block for missing pre-tag choice | OK |
| Post-release prerequisites | E:113 | Typical | Explicit command output and explicit pre-tag choice | true | Prerequisites satisfied; outward steps still separately gated | OK |
| Post-release prerequisites | E:113 | Maximum/Overflow | Many other flags supplied, pre-tag choice still absent | false | Other flags do not satisfy pre-tag prerequisite | OK |
| Post-release prerequisites | E:113 | Sentinel Value Match | Only pre-tag choice supplied, output absent | false | Block for missing output | OK |
| Post-release prerequisites | E:113 | Legitimate Edge Case | Both supplied but no outward authorization | true | Prerequisites met; skip unauthorized outward steps | OK |
| PR-monitor-one refusal | E:114 | Zero/Empty | No monitor-1 selection | false | This particular refusal does not fire; other PR rules apply | OK |
| PR-monitor-one refusal | E:114 | One/Minimal | Unattended monitor 1 selected | true | Refuse monitor 1 | OK |
| PR-monitor-one refusal | E:114 | Typical | Another monitor mode explicitly selected | false | No refusal from equality-to-1 predicate | OK |
| PR-monitor-one refusal | E:114 | Maximum/Overflow | Many PR workers each select monitor 1 | true for each | Refuse each, irrespective of worker count | OK |
| PR-monitor-one refusal | E:114 | Sentinel Value Match | `--monitor 1` | true | Forbidden unattended mode | OK |
| PR-monitor-one refusal | E:114,146 | Legitimate Edge Case | Person selects monitor 1 without unattended | false | Preserve attended behavior | OK |
| Translation implementation default | E:117 | Zero/Empty | No instruction to implement | true for default skip | Phase 7 defaults to skip implementation | OK |
| Translation implementation default | E:117 | One/Minimal | One audit-only translation request | true for default skip | Produce audit files without implementing | OK |
| Translation implementation default | E:117 | Typical | Context confirmed, implementation not requested | true for default skip | Audit can continue; implementation still skipped | OK |
| Translation implementation default | E:117 | Maximum/Overflow | Many findings, no implementation request | true for default skip | Finding count does not change the skip default | OK |
| Translation implementation default | E:117 | Sentinel Value Match | Phase 7 default branch | true for default skip | Skip implementation | OK |
| Translation implementation default | E:117,146 | Legitimate Edge Case | Attended run without unattended switch | false for new unattended default | Original attended workflow retained | OK |
| Improved-spec request | E:120 | Zero/Empty | No improved-spec request | false | Improved-spec step off | OK |
| Improved-spec request | E:120 | One/Minimal | Brief explicitly asks for improvement | true | Improved-spec step may run within authorized scope | OK |
| Improved-spec request | E:120 | Typical | Review-only brief with TDD release supplied | false | Review does not authorize improved spec | OK |
| Improved-spec request | E:120 | Maximum/Overflow | Many review findings but no improvement request | false | Finding count does not turn improvement on | OK |
| Improved-spec request | E:120 | Sentinel Value Match | Explicit request to create improved specification | true | Caller has asked for the step | OK |
| Improved-spec request | E:120 | Legitimate Edge Case | Caller supplies output directory but asks only for review | false | Output location is not improvement authorization | OK |
| Cli-portify checkout eligibility | E:105 | Zero/Empty | No IronClaude checkout available | false | Do not dispatch cli-portify there | OK |
| Cli-portify checkout eligibility | E:105 | One/Minimal | One IronClaude checkout is the worker location | true | Checkout restriction satisfied | OK |
| Cli-portify checkout eligibility | E:105 | Typical | Authorized worker in this project's checkout | true | May proceed to its other approval/report prerequisites | OK |
| Cli-portify checkout eligibility | E:105 | Maximum/Overflow | Many unrelated repositories, none is IronClaude | false | Number of other repositories does not satisfy eligibility | OK |
| Cli-portify checkout eligibility | E:105 | Sentinel Value Match | Actual IronClaude checkout | true | Required checkout type matches | OK |
| Cli-portify checkout eligibility | E:105 | Legitimate Edge Case | Unrelated project has similar file names | false | Similar names are not the required checkout | OK |
| Adversarial pipeline resume | E:83 | Zero/Empty | No pipeline-resume request | false | No pipeline continuation requested | OK |
| Adversarial pipeline resume | E:83 | One/Minimal | Pipeline mode and pipeline-resume request | true | Pipeline resume permitted | OK |
| Adversarial pipeline resume | E:83 | Typical | Pipeline checkpoint resumed in pipeline mode | true | Use existing pipeline resume mechanism | OK |
| Adversarial pipeline resume | E:83 | Maximum/Overflow | Several non-pipeline outputs exist, caller asks to resume | false | Non-pipeline mode has fresh-dir re-run, not pipeline resume | OK |
| Adversarial pipeline resume | E:83 | Sentinel Value Match | pipeline-resume flag used for a non-pipeline mode | false | Pipeline-only restriction forbids applying that resume mechanism | OK |
| Adversarial pipeline resume | E:83 | Legitimate Edge Case | Existing output from a non-pipeline comparison | false | Retry uses fresh-output policy rather than treating it as a pipeline checkpoint | OK |
| Reflect promotion-only resume | E:88 | Zero/Empty | No promotion-resume flag | false | Audit has fresh-dir re-run policy | OK |
| Reflect promotion-only resume | E:88 | One/Minimal | Promotion-resume flag supplied | true | Covers promotion only, not resuming the audit | OK |
| Reflect promotion-only resume | E:88 | Typical | Prior audit exists and promotion alone is resumed | true | Do not interpret as audit continuation | OK |
| Reflect promotion-only resume | E:88 | Maximum/Overflow | Many audit files exist, promotion-resume selected | true | Still only promotion resume; audit re-run remains fresh-dir | OK |
| Reflect promotion-only resume | E:88 | Sentinel Value Match | `--promote-resume` | true | Promotion-only meaning is preserved | OK |
| Reflect promotion-only resume | E:88 | Legitimate Edge Case | Failed audit with no promotion-resume request | false | Audit cannot be resumed through absent or promotion-only flag | OK |
| Explicit command-output prerequisite | E:83-84,87,90,107,113 | Zero/Empty | Report directory valid, required command output absent | false | Required explicit output is not satisfied; report directory is separate | OK |
| Explicit command-output prerequisite | Same locations | One/Minimal | Report directory valid and one explicit command output supplied | true | Output prerequisite satisfied | OK |
| Explicit command-output prerequisite | E:87,90,107 | Typical | Explicit document output or tdd/init-lite file output plus report directory | true | Preserve command-specific file/output semantics | OK |
| Explicit command-output prerequisite | Same locations | Maximum/Overflow | Many other flags and valid report directory, command output absent | false | Other flags do not satisfy explicit-output requirement | OK |
| Explicit command-output prerequisite | Same locations | Sentinel Value Match | Only `--report-dir` supplied as attempted output substitute | false | Report directory does not replace command output | OK |
| Explicit command-output prerequisite | E:107,113 | Legitimate Edge Case | Valid explicitly supplied output path contains spaces | true | It remains an explicit output argument; no new path restriction is stated | OK |
| Standalone/additive boundary | E:146-151,172-176 | Zero/Empty | No unattended or new output flag | false for new report | Existing output/prompt defaults preserved | OK |
| Standalone/additive boundary | E:148 | One/Minimal | Explicit new output flag without unattended | true for requested report | May write requested new report | OK |
| Standalone/additive boundary | E:149 | Typical | Command edit not listed as a defect repair | true for additive constraint | Add section/flags without deleting existing lines | OK |
| Standalone/additive boundary | E:149-150 | Maximum/Overflow | Multi-file mirror updates | true for source discipline | Source files authoritative; generated .claude copies not staged | OK |
| Standalone/additive boundary | E:147,172 | Sentinel Value Match | Worker-contract core file | true for Orca-example exception | Caller-channel examples allowed only there under stated check | OK |
| Standalone/additive boundary | E:149 | Legitimate Edge Case | Edit repairs the explicitly named explain-tool defect | true for named-defect exception | Listed defect repair may change existing lines while preserving standalone behavior | OK |
| Phase readiness/decision dependency | E:154,159-162,195 | Zero/Empty | No earlier-phase acceptance | false for proceeding | Later phase does not start | OK |
| Phase readiness/decision dependency | E:159-160 | One/Minimal | Phase 1 complete, first Phase 2 gate not yet converted | true for exposed flag | Every command accepts flag before promised gate behavior is implemented (finding 1) | GAP |
| Phase readiness/decision dependency | E:154,162 | Typical | Earlier checks pass, final safety decisions unanswered | false for final phase | Wait for user decisions | OK |
| Phase readiness/decision dependency | E:159,195,240 | Maximum/Overflow | All-command Phase 1 requirement includes commands user later keeps coordinator-only | true for conflicting obligations | Requires unattended section before decision can remove those changes (finding 1) | GAP |
| Phase readiness/decision dependency | E:158,194 | Sentinel Value Match | Initial baseline phase | true for baseline exception | No command edits, original report paths, no new flags | OK |
| Phase readiness/decision dependency | E:159-162 | Legitimate Edge Case | No-gate command ready before other commands | true only for that command's implemented surface | Per-command phase scoping needed to avoid premature promise (finding 1) | GAP |
| Gate-trigger acceptance outcome | E:60,199-201 | Zero/Empty | Required answer genuinely absent, no default | true for blocked | Blocked contract and failed lifecycle outcome are consistent | OK |
| Gate-trigger acceptance outcome | E:103,110,200 | One/Minimal | One approval-required cleanup item | false for whole-run block | Row says defer item and report; acceptance demands blocked for every command (finding 3) | GAP |
| Gate-trigger acceptance outcome | E:100,200 | Typical | PR review without authorization to post | false for whole-run block | Row says disable posting and complete review; blanket blocked expectation conflicts (finding 3) | GAP |
| Gate-trigger acceptance outcome | E:116,200 | Maximum/Overflow | Several research topics with unattended planning pin | false for whole-run block | Pin planning and produce report, not a clarification stop (finding 3) | GAP |
| Gate-trigger acceptance outcome | E:60,200 | Sentinel Value Match | Gate has documented default instead of missing answer | false for blocked | Default branch must be tested as default branch, not forced blocked (finding 3) | GAP |
| Gate-trigger acceptance outcome | E:201 | Legitimate Edge Case | Happy path with complete flags | false for blocked | Successful completed run expected | OK |

**Enumeration and construction notes.** Each named guard/family above has six concrete input rows. Shared truth tables are used only for the same resolution rule: forbidden interactive modes, missing required answers, and the common report-location rules. The interactive family maps to adversarial/brainstorm/release-split/cleanup/improve/roadmap interactive switches, business-panel socratic, explain interactive format and test watch. The required-answer family maps to release-split custom scope/tasklist confirmation, tdd topic-only/nested task questions, troubleshoot short deep input/fix offer, cli-eval missing suite/safety/W0/$1, each cli-portify approval, implement halts, recommend clarification, translation context and TDD release selection. These rows evaluate the common question-missing versus answer/default-present predicate; they do not claim distinct underlying command parsers were executed.

Separate families evaluate the non-equivalent predicates: cli-portify checkout eligibility, adversarial pipeline-only resume, reflect promotion-only resume, explicit command output versus worker report directory, cleanup all-pass selection, index update selection, init marked-report overwrite, knowledge-base no-wait behavior, post-release prerequisites, PR monitor-1 refusal, translation default skip and improved-spec opt-in. The explicit command-output family includes the otherwise easy-to-miss case where a worker report directory exists but document's required output does not. Commands adding output flags without a distinct new gate remain covered by required-output and report-contract families; their file-writing mechanics are planning obligations, not invented runtime rules.

Nygard constructed the normal, missing-value and failed-attempt branches; Crispin checked the endpoint's contract, section-3 command predicates, standalone exceptions, phase gates and acceptance branches against this mapping; Whittaker probed token/data collisions, reordered retries and nested fan-out. Numeric overflow is tested only where the spec has a numeric threshold; for boolean guards Maximum/Overflow means many instances, not an invented capacity. Roadmap's many-prior-runs row tests the specified no-resume-flag branch and makes no unsupported claim about choosing among conflicting state files. Existing argument validation remains in force. Each GAP cell maps to a MAJOR blocking finding below, with repeated cells consolidated. The initial draft's table-coverage overstatement was corrected before final certification; the final table is the basis of synthesis.

## Quantity flow analysis
Fowler's count trace, checked with Whittaker's divergence/accumulation probes:

```text
43 inventoried commands
  -> classify: 10 ready + 27 change-needed + 6 coordinator-only = 43
  -> retain section-3 candidates: 37
  -> exclude context-only load from independent report Tasks: 36
  -> if user also retains pr-submit as coordinator-only: 35 eventual worker candidates
  -> dispatch eligible Tasks: K
  -> each authoritative Task attempt: one worker contract, one worker_done

Tasklist phase files: N
  -> Stage 10.5 dispatches N reflect agents
  -> each consumes one phase and its spec
  -> expected N individual verdict records
  -> aggregate pass + partial + fail = N when all child audits produced verdicts
```

The section-3 grouping intentionally includes context-only load and conditionally includes pr-submit; it is not itself a hidden cardinality error. There is no count-changing data filter followed by a consumer incorrectly assuming the original count, so no separate CRITICAL dimensional-analysis finding is asserted. Finding 2 concerns missing mandatory invocation arguments before child audits begin; its N-child failure trace is recorded in Adversarial Analysis rather than presented as a new, independent filtering defect. Count labels are analysis of the frozen specification, not measurements from dispatched smoke runs.

## Numbered findings
### === REQUIREMENTS ANALYSIS ===
#### 1. First-phase all-command support precedes the gates and safety decisions it promises

- **Severity:** MAJOR, blocking. **Experts:** Wiegers, Cockburn, Newman. **Priority:** High. **Endpoint sections:** 6 (first-phase scope versus later phases), 7.3 (first-phase static acceptance), 9 (PR-worker choice).
- **Finding:** The first reporting phase requires `--unattended` to be accepted by every command in sections 3.1 and 3.2, and its static test requires their unattended sections. Gate conversion is nevertheless assigned to the next phase, shared-state repair to the following one, and implement/post-release/pr-submit safety behavior to the decision-gated final phase. There is no temporary rejection or eligibility rule for a command whose flag is already exposed but whose gates have not yet been converted.
- **Concrete wrong outcome:** An implementer completes the first-phase flag/report additions and exposes unattended auggie-review while leaving its posting and remediation-offer changes for their assigned next phase. A PR-target invocation can still post or wait locally, contradicting unattended no-prompt/no-outward-default rules. Alternatively the implementer must silently do later-phase work early to honor the shared contract. The conflict is particularly explicit for pr-submit: the first phase must add its unattended section, but the recommended user choice says no pr-submit changes in the final phase and retains coordinator-only execution.
- **Evidence:** `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:159-162`, `:195`, `:60`, `:67`, `:100`, `:240`. The existing posting default was independently read in `src/superclaude/commands/auggie-review.md:51-54`; the outcome above is a specification implementation trace, not a live posting experiment.
- **Recommendation and rationale:** Scope flag acceptance and its static coverage to commands whose complete unattended contract ships in that phase, or explicitly reject later-phase commands until their full conversion and decisions are complete. This removes an unsafe intermediate interface without accelerating safety decisions or weakening standalone behavior.
- **Quality impact:** Makes each independently useful phase actually satisfy the advertised unattended contract; prevents a static first-phase pass from advertising unsupported behavior.
- **Textual classification:** **present since original**, using the unchanged first-phase scope anchor. Direct quotes and both locations appear in the comparison section.

#### 3. The gate-trigger test demands blocked results from branches designed to continue safely

- **Severity:** MAJOR, blocking. **Experts:** Adzic, Crispin, Gregory. **Priority:** High. **Endpoint sections:** 2.2 (three permitted gate resolutions), 3.2 (safe defaults), 7.3 (gate-trigger acceptance).
- **Finding:** The acceptance check requires a gate-trigger run for every second-phase command to return `worker_status: blocked` and a failed lifecycle outcome. But several rows intentionally resolve their gates by a safe default, not by stopping: cleanup/improve defer approval-required items, auggie-review disables posting/offers, and research pins planning.
- **Concrete wrong outcome:** Give cleanup one automatically permitted unused import and one approval-required fixture. Its row requires applying the first and reporting the second unapplied, without a local question. A faithful implementation can complete that report successfully or partially, but the blanket gate test rejects it for not being blocked. For unattended research, selecting planning removes clarification entirely; inventing a blocking question solely to satisfy this test violates the pinned strategy's purpose. This prevents the phase from passing under its own intended behavior, or pushes implementers to add spurious failure paths.
- **Evidence:** `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:60`, `:100`, `:103`, `:110`, `:116`, `:200-201`. Approval-required and automatic cleanup categories were independently read in `src/superclaude/commands/cleanup.md:107-127`.
- **Recommendation and rationale:** Parameterize the gate-trigger expectation by the row's resolution: assert blocked only for unresolved required answers; assert completion plus the safe default/deferred action for default-resolved gates; assert deterministic refusal for forbidden modes. Keep the happy-path checks separate.
- **Quality impact:** Restores a satisfiable acceptance gate and verifies the actual safety behavior instead of forcing every safe refusal/default into a question.
- **Textual classification:** **present since original**, using the unchanged universal gate-trigger scope and failed-outcome anchors, not the renamed status field. Direct comparisons appear below.

### === ARCHITECTURE ANALYSIS ===
#### 2. The newly mandatory report-directory argument is not wired into tasklist's reflect calls

- **Severity:** MAJOR, blocking. **Experts:** Fowler, Hohpe, Whittaker. **Priority:** High. **Endpoint sections:** 2.2 (report prerequisite and write isolation), 3.2 (tasklist child invocation).
- **Finding:** The report rule now makes unattended execution without `--report-dir` stop before any work, even when the command already has an output directory. Tasklist's specific integration change forwards `--unattended` to every reflect child, but specifies neither a child `--report-dir` nor a per-child allocation. Its parent brief's report directory does not automatically become a distinct argument on each nested invocation.
- **Concrete wrong outcome:** Run tasklist unattended with one phase, a parent report directory and reflection enabled. Apply the listed Stage 10.5 change to the existing reflect command: append `--unattended`, retaining its existing per-phase `--output`. The child must now stop for missing `--report-dir`, so no pre-reflect audit occurs. Blindly forwarding the parent's report directory instead makes N parallel children target the same `return-contract.yaml`, violating parallel write isolation and overwriting reports. This is a caller/callee integration omission, not a claim that the current source already implements the new switch.
- **Evidence:** `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:62`, `:69`, `:122`. The actual nested invocation is `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1620-1629`, which already passes a distinct per-phase output but has no report-directory argument; its completion accounting at `:1631-1635` expects a verdict per phase.
- **Recommendation and rationale:** Extend the tasklist integration instruction to pass a distinct report directory for each reflect child, using the existing per-phase output namespace, and require child report/verdict existence before recording the stage complete. Do not share the parent report filename with children.
- **Quality impact:** Preserves every requested child audit and prevents N concurrent children from clobbering one report file.
- **Textual classification:** **fix-written** for the primary anchor: the missing-report-directory hard stop at endpoint line 62 is new versus original line 62. The tasklist caller at line 122 is unchanged in both snapshots. This label describes the changed callee requirement, not proof of authorship or revision timing for the unchanged caller.

#### 4. Renaming retry outputs leaves archived report pointers selecting the next attempt

- **Severity:** MAJOR, blocking. **Experts:** Nygard, Hohpe, Newman. **Priority:** High. **Endpoint sections:** 2.2 (retry preservation), 2.3 (coordinator archive duties), 3.2 (non-resumable commands).
- **Finding:** The retry procedure renames the failed attempt's worker contract and output location, then reuses the original brief and paths for the next attempt. It never rebases the archived contract's `report_path` and `artifacts` pointers or specifies a relocation mapping for its consumer. Keeping the old file bytes is not enough to keep that report pointing to that attempt's evidence.
- **Concrete wrong outcome:** A failed non-resumable auggie-review has output directory `review/a`, report directory `worker/a`, and `report_path` naming `review/a/REVIEW.md`. The coordinator renames the worker contract to `worker/a/return-contract.ctx-old.yaml` and output to `review/a.ctx-old`. Before retry the archived pointer is dangling. After the retry writes `review/a/REVIEW.md`, opening the archived failed contract selects the new attempt's review, falsely attributing it to the old attempt. Relative pointers from a separate report directory have the same problem; this case does not depend on co-locating reports and outputs.
- **Evidence:** `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:62` (report and artifact pointers), `:64` (the mandated rename and original-path reuse), `:73` (coordinator duty), `:100` (non-resumable review with separate output directory). The actual review contract defines an absolute main report path in `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:55`.
- **Recommendation and rationale:** State how archived contracts resolve to archived output locations, for example by rebasing report/artifact pointers when outputs are relocated or recording and applying an explicit old-to-new location map. Validate that an archived contract still opens the old evidence after a retry finishes. Preserve the same Task/brief/circuit-breaker rules.
- **Quality impact:** Keeps failed-attempt evidence readable and prevents a retry from silently replacing the evidence reached through an older report.
- **Textual classification:** **fix-written**: the coordinator rename and original-path-reuse procedure at endpoint line 64 differs directly from original line 64, which instead required each non-resumable run to write a fresh directory. Quotes appear below.

## Adversarial Analysis
1. **Sequence Attack, MAJOR, blocking (finding 1).** I can break this specification by **Sequence Attack**. The invariant at **section 6 first-phase rollout and section 2 unattended promises** fails when **a caller invokes a later-phase command after the first phase exposed its flag but before gate conversion**. Concrete attack: **before: only flag/report additions have shipped; invoke unattended PR review; after: unconverted posting/offer path remains reachable, or later-phase conversion must be pulled forward outside its assigned phase**. Priority High; resolve by aligning eligibility and phase scope.

2. **Zero/Empty Attack, MAJOR, blocking (finding 2).** I can break this specification by **Zero/Empty Attack**. The invariant at **section 3.2 tasklist's Stage 10.5 integration** fails when **the nested reflect report-directory argument is empty**. Concrete attack: **before: one valid generated phase and a parent report directory exist; append only the specified unattended flag to the existing reflect call; after: the child exits for missing report directory before producing its audit**. Priority High; supply a distinct child report directory explicitly.

3. **Divergence Attack, MAJOR, blocking (finding 3).** I can break this specification by **Divergence Attack**. The invariant at **section 7.3 universal gate-trigger acceptance** fails when **a gate takes the documented safe-default branch rather than the blocked branch**. Concrete attack: **before: cleanup sees one permitted import removal and one approval-required fixture; after: permitted edit applied and fixture deferred in a completed report; the phase test still requires blocked and rejects the faithful result**. Priority High; assert the intended result of each branch.

4. **Sequence Attack, MAJOR, blocking (finding 4).** I can break this specification by **Sequence Attack**. The invariant at **section 2 retry preservation** fails when **an output directory is renamed but an archived report's pointers are not relocated**. Concrete attack: **before: old contract points to review/a/REVIEW.md; archive output to review/a.ctx-old; old pointer dangles; retry repopulates review/a; after: old contract opens new attempt's review instead of old evidence**. Priority High; preserve reference identity across relocation.

5. **Accumulation Attack, MAJOR, blocking (same finding 2, not a fifth finding).** I can break this specification by **Accumulation Attack**. The invariant at **section 2 parallel-safe reports and section 3.2 reflect fan-out** fails when **N children are given a copied parent report directory instead of N allocated locations**. Concrete attack: **before: N=2 phase audit children and one report filename; both write that filename; after: at most one child's final report survives there**. This probes the tempting but incorrect repair to the missing argument, not a claim that the spec explicitly instructs shared child directories.

6. **Sentinel Collision Attack, no new finding.** Before: a person's quoted topic includes the literal unattended-switch text. The explicit standalone-token rule leaves mode off, so the ordinary-session behavior is preserved. Adding a separate unquoted switch correctly turns mode on. The endpoint states the distinction, so reporting this case as a defect would ignore the frozen evidence.

The no-prompt contract is not a reason to turn all gates into failure. The audit intentionally distinguishes missing answers, safe defaults, explicit authorization and completed negative audit verdicts. All attack outcomes above are static traces from requirements and current call definitions, not claims that a live worker, PR post or filesystem rename was executed.

## Direct anchor comparisons with the original
| Finding | Endpoint anchor | Original anchor | Classification | Textual comparison |
|---|---|---|---|---|
| 1 | E:159 | O:159 | present since original | Same all-command flag-acceptance sentence; later-phase conversion remains separate in both |
| 2 | E:62, dependent E:122 | O:62, dependent O:122 | fix-written | New missing-report-directory hard stop differs; caller forwarding sentence is unchanged |
| 3 | E:200 | O:200 | present since original | Universal per-command gate-trigger scope and failed-outcome expectation unchanged; status key rename is not the defect anchor |
| 4 | E:64 | O:64 | fix-written | Explicit rename-and-reuse procedure replaces fresh-output-per-run requirement |

### Finding 1: same scope anchor, both locations quoted

Endpoint `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:159`:
> The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands.

Original `.dev/orca-command-refactor/specs/history/spec-v1-draft.md:159`:
> The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands.

The relevant phase-2 conversion and phase-4 decision split are also unchanged at E:160-162 and O:160-162. The endpoint static-check exception for load does not repair this all-other-commands timing conflict. Classification is about the identical scope sentence, not about whether the static-test line changed.

### Finding 2: changed report prerequisite, unchanged nested caller

Endpoint `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:62`:
> If `--unattended` is given without `--report-dir`, the command does no work, writes nothing and stops with an error naming the missing flag; the worker then has no report, so WC-5 sends `--outcome failed` (R1.1).

Original `.dev/orca-command-refactor/specs/history/spec-v1-draft.md:62`:
> In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`).

The original has no separate required report-directory argument or missing-argument hard stop in this requirement. The consumer sentence is identical at endpoint `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:122` and original `.dev/orca-command-refactor/specs/history/spec-v1-draft.md:122`:

Endpoint:
> under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so the headless rule applies; without `--unattended` Stage 10.5 is unchanged (SA-1); `--no-reflect` is ready today

Original:
> under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so the headless rule applies; without `--unattended` Stage 10.5 is unchanged (SA-1); `--no-reflect` is ready today

Thus **fix-written** is supported for the changed report prerequisite. A claim that the caller sentence itself was written in a fix would be false. Which earlier review or author caused the change is not established and is not asserted.

### Finding 3: unchanged universal test scope and outcome

Endpoint `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:200`:
> Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate

Original `.dev/orca-command-refactor/specs/history/spec-v1-draft.md:200`:
> Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate

Both locations also contain the exact expected lifecycle result:
> `worker_done --outcome failed`

The report's field name changed from original `status: blocked` to endpoint `worker_status: blocked`, but the requirement to block every command in this test did not. The cleanup, auggie-review and research resolution rows are unchanged at O/E:100,103,110,116. Classification is **present since original**, not fix-written merely because an unrelated identifier on the long table row changed.

### Finding 4: changed retry storage procedure

Endpoint `.dev/orca-command-refactor/specs/history/spec-v3-after-round2.md:64`:
> The coordinator, not the command, therefore keeps attempts apart: before it runs `worker-start --retry-of <dispatch_id>`, it renames the failed attempt's `<report-dir>/return-contract.yaml` to `return-contract.<dispatch_id>.yaml` and, for a command without resume, renames that attempt's output location to `<location>.<dispatch_id>`, using the failed Dispatch's ID.

Same endpoint location:
> The retry then writes the paths the brief recorded before dispatch into a location that holds no earlier output, and the first attempt's files stay intact under the new names (R1.3).

Original `.dev/orca-command-refactor/specs/history/spec-v1-draft.md:64`:
> A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean.

The original does not prescribe moving an already-referenced output and then repopulating its old path. The primary procedure anchor differs, so **fix-written** is supported without inferring the content of any previous review.

**Classification totals:** 2 fix-written (2, 4), 2 present since original (1, 3), 0 UNVERIFIED textual classifications. These are anchor comparisons only. No causal attribution to a particular review round is claimed.

## Evidence checks and limits
### Observed checks

- Both frozen input hashes matched before the panel instrument was invoked and again after the initial assembled audit. Endpoint: `75a628e35b00eb23bde80d0190f6cf735f3b298c8f3b228caf05f65ee094ac9a`. Original: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`. These were real `sha256sum` results, not hashes inferred from Git history. The original was read directly from its overlay file; git show was not used.
- The Arm B skill was invoked with the assigned frozen endpoint, critique mode and requirements/architecture focus. Its installed command definition was read before the report skeleton was written. No TDD/PRD release-scoping output or specification improvement was requested or generated.
- Direct reads checked the current tasklist Stage 10.5 invocation, auggie-review posting defaults and absolute report-path contract, cleanup approval categories, workflow contract semantics, brainstorm contract vocabulary, index-repo output names, reflect precondition statuses and headless-remediation rule. These supporting reads ground selected integration examples; this was not a second verification of every historical citation carried by the endpoint.
- Context7 supplied generic required-property and enum-validation documentation for comparison with contract testability: `https://json-schema.org/understanding-json-schema/reference/object` and `https://json-schema.org/understanding-json-schema/reference/enum`. No source content was sent in those generic documentation queries. This supplement did not override repository evidence or introduce a schema implementation requirement.
- The version-matched Orca orchestration guide and check help were read for this worker's own reporting duties. Coordinator checks returned no follow-ups at the observed checkpoints, and the bounded wait expired without a message. These are worker-management observations, not smoke tests of the proposed command contract.
- `git status --short --untracked-files=normal` still showed only the pre-existing untracked `.dev/orca-command-refactor/` overlay and no tracked modifications. This coarse status does not prove that every untracked file elsewhere in the overlay is byte-identical; the stronger ownership evidence is that this task's Write/Edit targets were exclusively this report, plus both frozen-source hashes remaining unchanged.

### Independent report-quality gate

A fresh read-only audit-validator context checked the new report, the frozen endpoint/original, the installed instrument and selected cited source locations. Its initial verdict was **FAIL for report completeness**, not rejection of the four specification findings: it confirmed the exact anchor quotations, the four classifications and the MAJOR grading, but found missing guard distinctions, four non-boolean table results and an unsupported roadmap multiple-state-selection assumption. Those report defects were corrected in this file only: distinct eligibility/resume/output/default predicates were added, the mixed branch row was separated, results were made explicit, the invented selection behavior was removed and the coverage statement narrowed. No specification revision or extra review/fix round was started.

**Initial completion check: FAIL. Targeted correction verification: PASS.** The same independent validator re-read only the changed table span and enumeration notes and confirmed that all three requested report corrections were addressed: 12 distinct replacement families each have six populated rows; the previously non-boolean entries now have evaluated results; and the roadmap row no longer claims unsupported state selection. The initial table contained 30 six-row families; replacing one mixed family with 12 yields 41 six-row families (246 rows). The validator preserved its previously verified finding quotations and classifications. It did not repeat the full source sweep on the correction check. The unchanged findings plus independently checked report-only corrections establish completion of this audit artifact, while its specification verdict remains FAIL.

### Negative evidence and limits

- The first Edit attempt was blocked by the freshness hook because the newly written stub had not yet been read. The report was then read with Read and the edit retried through Edit; no alternate write mechanism bypassed the hook.
- The environment inspection exited 1 because the optional executable-selection variables were unset; it did return this managed terminal's handle. The guide's managed-terminal rule selected the preamble's Orca executable, which worked. No alternate runtime was substituted.
- The independent validator did not recompute input hashes or independently establish the historical order of this session's Skill/Write calls. Hash and construction-order evidence comes from this worker's actual tool receipts, not that validator's narrative.
- No live command execution, eval, test suite, PR post, retry rename, installation or implementation was run. All failure examples are requirement-level state traces. The frozen spec explicitly says implementation is not present, so these are not measured runtime bugs.
- The live specification and prohibited prior-review/loop sources were not opened. Existing memories or review-like claims inside the frozen source were not treated as prior findings to adopt. No commits, pushes, GitHub posts, external report publication or source/test changes were made.
- The report verdict below is the specification's review verdict. Successful completion of the requested audit is a separate lifecycle result and does not mean that specification passed.

## Reviser brief
Blocking finding IDs: **1, 2, 3, 4**. This brief is an output required by the review instrument, not authorization to revise anything during the present task. If a revision is separately authorized, revise only the text named by these blocking findings; add no rule, mechanism or section that no blocking finding calls for; cite its finding ID in each added paragraph or table; report the specification byte size before and after. Do not revise minor notes or expand into a new implementation or fix round here.

verdict: FAIL
