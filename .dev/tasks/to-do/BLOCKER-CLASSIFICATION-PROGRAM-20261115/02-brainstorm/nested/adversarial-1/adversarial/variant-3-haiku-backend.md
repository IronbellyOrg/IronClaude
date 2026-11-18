# Consequence-Based Review Contract

Variant: backend. Requirements and design options only.

## 1. Problem statement

Review gates confuse a true observation with a reason to stop work.
The current default lists a false claim as blocking without testing its consequence.
A label error and a wrong deployment destination can therefore enter the same fix loop.
The replacement must preserve the latter gate without repeatedly repairing the former.

This is a requirements specification, not permission to change the framework.
The source brief requires a checked implementation plan before framework changes.
The intended result is a common decision contract, not a universal severity vocabulary.

Evidence inputs, read in this session:
- `02-brainstorm-context-preamble.md` and `00-issue-description.md` state the owner's intent.
- `02-brainstorm/jev-uses.md` supplies the Jev design research and its limitations.
- `02-brainstorm/enrichment/rule-copies-and-tests.md` supplies the propagation inventory.
- `02-brainstorm/enrichment/severity-models-and-loops.md` supplies model and loop distinctions.
- `02-brainstorm/enrichment/follow-up-and-issue-mechanisms.md` supplies record and filing precedents.

Those input paths are relative to `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/`.
All repository paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`.
New paths are explicitly marked proposed; they are not claims that files exist.

The issue reports Gate 1 regrading from 11 blocking findings to 6.
It reports an additional fix cycle taking about 25 minutes for table formatting.
These are historical observations from the inputs, not independently reproduced measurements.
They motivate the change but do not establish a safe universal threshold.
The requested 35 percent reduction is not a release condition.

## 2. Goals and non-goals

### Goals
1. Stop only for a verified consequence, missing required work, or protected risk.
2. Preserve every non-blocking observation with its evidence and disposition.
3. Offer one clear decision after a loop, not one interruption per finding.
4. Keep unattended workers record-only and make the records discoverable to their caller.
5. Make repeated reviews, resumes and issue filing safe to repeat without duplicates.
6. Separate a judge's language judgments from deterministic gate decisions.
7. Introduce a classifier with visible uncertainty and a usable no-key fallback.
8. Reduce gate time without accepting an increase in escaped consequential defects.

### Non-goals
- No implementation code, framework edits, Git writes or external calls in this proposal.
- No automatic issue creation, automatic acceptance of blockers, or extra review rounds.
- No assumption that all findings called Medium mean the same thing.
- No conversion of missing evidence into proof that a finding is harmless.
- No alteration of specialized protocol halts by an output-style change alone.
- No claim that agreement with three scorers proves real-world correctness.

## 3. Proposed rule in plain words

A finding blocks only when at least one of these three conditions is verified:

| Condition | What must be shown |
|---|---|
| Consequential error | A named decision, recommendation, destination, required behavior, outcome or number the deliverable rests on would be wrong or unsupported if the defect remains. |
| Missing required work | A required deliverable, section, behavior or explicit contractual obligation is absent or contradicted in substance. |
| Protected risk | Following the text or running the changed code creates a security, data-loss or safety-boundary risk. |

Security, data-loss and safety-boundary findings are never downgraded because of a label,
a low classifier score, an inferable intention, a cheap workaround or fix cost.
A reviewer must name the affected action and evidence, not merely write "security".
Unverified protected-risk claims remain unresolved for verification; they are not notes.

A real weakness without these consequences is a follow-up, called Medium where useful.
Cosmetic observations and suggestions are notes, but are still recorded.
A false statement is not automatically harmless or automatically blocking.
Its downstream use decides the first condition; required evidence can satisfy the second.
A wrong number used in an acceptance check blocks even if a recommendation stays the same.
A table defect that changes a destination blocks; a cosmetic pipe defect need not.

Unknown is not no. An unavailable input or ambiguous consequence requires escalation,
or retention of the protocol's existing label, never automatic demotion.
Only confirmed blockers enter fix briefs and blocking counters.
Non-blockers never consume a fix cycle or require a re-review on their own.
Existing regression, monotonicity and hard-cap protections remain in their own protocols.
A user's request to resolve follow-ups starts separately authorized work after the gate.

## 4. Record-and-offer behaviour

### 4.1 Flow and ownership
1. Capture the original finding before consolidation or repair overwrites any report.
2. Read its anchor and evidence; preserve whether verification succeeded.
3. Classify under the named protocol and rule version; retain the original label too.
4. Consolidate repeated observations into one finding identity, not one row per review.
5. Persist follow-ups and notes before declaring a successful non-blocking review.
6. Continue the current task when no blocker remains; do not launch a minor-fix agent.
7. At loop completion, the attended top-level session offers the recorded set once.
8. Record the answer, including no answer; only an explicit filing answer permits GitHub writes.
9. Unattended workers omit the offer, return the ledger, and continue under their contract.

The run owner is the only ledger writer. Gate owners return observations to it.
Nested runs have separate ledgers and contracts; the parent imports references, not copies.
The proposed ledger is `<run-report-dir>/qa/follow-ups.md` when the run has a QA directory,
otherwise `<run-report-dir>/follow-ups.md`. The path is fixed before dispatch.
A header-only ledger is valid and records zero findings, not missing execution.

### 4.2 Ledger contract, version 1

Use one structured Markdown document, not an unrelated tracking service.
It contains metadata and four fixed-column tables described below.
The plan must choose and test one escaping convention for pipes, newlines and backticks.
Rendered layout must not be the only parser test: round-trip the underlying values.
Long evidence stays in the immutable source artifact, referenced by path and content digest.
The ledger must explain a finding even if that artifact later disappears.

Required metadata fields:
| Field | Meaning |
|---|---|
| schema_version | `follow-ups/1`; unsupported major versions are refused, not guessed. |
| run_id | Stable identifier assigned by the caller for this logical run, retained on resume. |
| loop_ids | Stable gate identifiers covered by this run ledger, never review numbers. |
| owner | The sole writer and its report directory. |
| rule_version | Shared rule version and digest, plus specialized protocol version. |
| revision | Increasing integer for each successful atomic rewrite. |
| capture_state | `complete` or `incomplete`, with a reason when incomplete. |

The Items table has exactly these columns:
| Column | Required content |
|---|---|
| id | Run-scoped stable identifier, `FU-000001` upward; never reassigned or recycled. |
| origin | Protocol name and original source finding identifier, or `none`. |
| kind | `follow-up` or `note`; unresolved classifier decisions stay outside this non-blocking set. |
| source_class | Original severity word and optional deviation class, retained verbatim. |
| location | Repository-relative file and stable section or symbol; line number is supplementary. |
| finding | One-sentence defect or suggestion, retaining the original source reference. |
| evidence | Artifact reference, digest, excerpt and `verified` or `unverified`. |
| nonblocking_basis | Which blocking conditions were tested and why none applies. |
| proposed_action | Bounded proposed fix or `none`; no invented owner or deadline. |
| suggested_type | `bug`, `refactor`, `docs`, `observability`, `test` or `unspecified`. |
| status | One of the closed values below. |
| canonical_id | Self unless proven to duplicate another row. |
| issue_url | Verified fork issue URL or `none`; attempted posting is not success. |

The Observations table has exactly these columns:
`observation_id`, `item_id`, `source_report`, `source_id`, `review_id`, `source_digest`, `identity_basis`.
It records every source appearance once; importing the same report twice changes nothing.
`identity_basis` states exact-source match, preserved reviewer identity, confirmed merge,
or `pending-identity`; only the last permits item_id `pending` until reconciliation.
A reviewer changing its local numbering does not create a new item automatically.

The Offers table has exactly these columns:
`offer_id`, `loop_id`, `item_ids`, `set_digest`, `answer`, `answer_source`, `decision_id`, `state`.
`answer` is `resolve`, `file-one`, `leave`, or `none`.
`state` is `pending`, `answered`, `superseded`, or `unattended`.
`answer_source` points to the user's actual instruction, not another agent's approval.
`decision_id` is an audit reference, not a transferable authorization token.

The Filings table has exactly these columns:
`batch_id`, `item_ids`, `set_digest`, `body_digest`, `decision_id`, `state`, `issue_url`, `last_error`.
Its states are `prepared`, `posting`, `reconcile`, `filed`, or `cancelled`.
This table exists even for a single finding so retries use the same contract.

### 4.3 Item states and repeatability

| Status | Meaning and allowed next steps |
|---|---|
| recorded | Stored, not offered; may become offered, resolving, filed, declined, duplicate or superseded. |
| offered | In a pending offer; silence leaves it here without blocking the gate. |
| resolving | Separate work authorized; becomes resolved or recorded after a failed attempt. |
| resolved | Fix verified with evidence; historical observations remain. |
| filed | Remote issue verified; no automatic second issue for this item. |
| declined | User chose to leave recorded; not reoffered on resume. |
| duplicate | Proven alias of canonical_id; excluded from counts and offers. |
| superseded | No longer applies after changed inputs; reason and last evidence preserved. |

Status describes disposition, not severity. Filing does not mean resolved.
A new blocker on a recorded item's text creates a linked escalation in its source report;
it marks the follow-up superseded with reason `escalated`, removes it from pending offers,
and retains the prior classification history. It does not count as resolved.
It never silently deletes that decision or changes a recorded gate verdict.

Identity uses protocol-native stable IDs, with the run and loop namespace.
Otherwise use a digest of target path, stable anchor, normalized claim and stated consequence.
Normalization excludes review number, severity label and moving line numbers.
Keep the full identity tuple to detect digest collisions; never merge on digest alone.
A changed quote after a fix is linked through the prior observation before allocating a new ID.
If wording changes and identity is ambiguous, record an unresolved identity observation,
exclude it from filing and ask the loop owner to reconcile; do not append a guessed new item.
This prevents duplicate item rows across fix cycles rather than merely hiding their count.
Independent defects at the same location remain separate.

Each rewrite checks expected revision, validates all references and replaces atomically.
A stale writer reads the current revision before retrying; it never overwrites newer answers.
A crash leaves either the old complete ledger or the new one, not half a table.
A malformed ledger is preserved and reported as capture failure, never reset to empty.
No successful record-only outcome is reported when recording failed.

### 4.4 Mapping the four existing record shapes

| Existing shape | Mapping into this contract |
|---|---|
| rf-qa issue table | Number plus report digest supplies source identity; Severity becomes source_class; Location, Issue and Required Fix map directly. Add evidence and nonblocking_basis by read-back, not by copying a severity word. |
| implement notes line | Task start, review tag and finding token supply source identity; minor or note becomes kind; path, acceptance-criterion identifier and checklist remain evidence. Superseded tree-chain lines map to superseded, not active offers. |
| troubleshoot follow-up task | Summary becomes finding; Suggested type maps to suggested_type; read evidence back; absent fields stay unknown until enriched. A recommendation alone is not verified non-blocking evidence. |
| reflect deviation block | Deviation ID supplies source identity; classification stays source_class; location, evidence, rationale and default remediation map directly. Export only already non-blocking items under reflect's own gate; do not silently convert Drift or Regression. |

Original artifacts remain authoritative for protocol verdicts.
The ledger is authoritative for identity, offers and issue disposition.
Adapters reject unparseable rows without dropping them from the capture report.

### 4.5 Offer wording and one-issue batching

Proposed wording:
"Review passed with N recorded follow-ups and M notes. They did not block this work.
Resolve the listed follow-ups as separate work, file the selected list as one GitHub issue,
or leave them recorded? Nothing will be filed without your answer. Ledger: <path>."
When blockers remain, replace the first sentence with the actual failed verdict.
Never imply that resolving follow-ups is needed to clear that failed gate.

The offer names exact IDs and snapshot digest; notes are opt-in for filing.
One offer covers the loop's final consolidated set, not each fix cycle.
Resume may display a pending offer but does not issue a fresh question automatically.
New items after an answered offer remain recorded for a later explicit user request.
A changed selected set or materially changed proposed body needs renewed consent.

Verified current capability: `/sc:issue --create` accepts one description or an `@path` file.
It produces one templated issue, not one issue per ledger row.
It accepts depth, feature-or-bug mode and area type, but no ledger or batch input.
It has no repository, preview or dry-run option and can post without another approval prompt.
Its new-material question does not replace the user's initial filing authorization.
It is never dispatched as an unattended worker under the current worker contract.

Recommended v1: after consent, prepare one description containing selected IDs,
findings, verified evidence, proposed actions and a checklist. Pass that description
through the existing create flow from an attended top-level session.
Do not invent a new supported command flag in prompts.
A mixed list gets one issue-level mode, type and depth; preserve per-item types in its body.
Depth currently also chooses Complexity, not independent per-item priority.
Missing capabilities are ledger parsing, write-back, duplicate-safe batches and consent binding.
These belong in a narrow adapter contract, not a new automatic filing service.

The batch ID is a stable digest of repository, run ID, selected canonical IDs and purpose.
The issue body carries that batch ID and item IDs for reconciliation.
Before posting, persist prepared then posting with the approved body digest.
After a timeout or crash, enter reconcile and search for that exact batch marker.
Never retry creation until absence or the existing issue has been established.
Ambiguous lookup stays reconcile and requires a person; it never assumes the post failed.
On success, verify the issue URL, then mark selected rows filed atomically.
Metadata or label failure after creation does not justify a second issue.

Every repository GitHub call must target `IronbellyOrg/IronClaude` explicitly.
Repository commands use `--repo IronbellyOrg/IronClaude`; repository API paths spell that fork.
The existing create lookup's organization-field read must be scoped to IronbellyOrg.
No call, remote, default or returned URL may resolve to the upstream parent.
If origin is not the fork, stop before filing; do not let create pick a default.

### 4.6 Unattended worker return contract

Workers only record. They do not offer, file, invoke the issue command or request API keys.
They also skip direct paid external judge calls under the current no-outward-action contract;
use existing in-session judgments or fixtures, with external experiments owned by the coordinator.
Proposed additive fields are `follow_up_schema`, `follow_up_ledger`, `follow_up_count`,
`note_count`, `follow_up_capture_state` and `follow_up_offer_state`.
The last value is `record-only` under unattended operation.
List the ledger in `artifacts` when eligible under existing tracked-path rules.
Keep `report_path` as the main report; do not replace it with the ledger.
Follow-ups alone do not change worker_status from succeeded to blocked or failed.
Capture failure makes the run partial or failed under its own output-failure contract.
Real unresolved blockers still use the command's documented blocked-question behavior.
The final report says counts, path, capture state and "recorded only, no issue created".
The coordinator reads these fields, not assumes every artifacts entry was inspected.
Nested ledgers appear through nested contracts; do not double-count them.
Unknown additive keys must not change existing status interpretation.

## 5. Classifier concept and Jev use

### 5.1 Decision boundary

A judge supplies language judgments; a local table decides their consequences.
Jev is a candidate judge, not a repository inspector or the gate owner.
The supplied Jev research recommends ten atomic Noul questions, meaning probabilities
that individual conditions hold, rather than the single question "is this blocking?".
No Jev or TypeSafe request is authorized by this specification.

| Question | Meaning in plain words |
|---|---|
| W | Following the quoted text produces a specific wrong result for a named actor. |
| D | A supplied decision, required outcome, destination or number depends on that text. |
| E | The read-back evidence contradicts the statement. |
| M | A required item is missing in substance. |
| S | The described action risks security, data, secrets or a safety boundary. |
| C | The text violates a supplied explicit contractual constraint. |
| T | The substance is true and only the label or pointer is wrong. |
| F | The defect is cosmetic and changes no acted-on meaning. |
| I | Nearby text makes the intended behavior inferable. |
| G | The finding proposes new scope rather than identifies an existing defect. |

T, F, I and G explain follow-up placement; they never cancel S, M or a confirmed obligation.
C maps to missing required behavior or protected risk when the constraint demands it.
Keep C independently blocking in specialized protocols that already require that policy.
Do not quietly add an unlimited fourth default blocking condition through the classifier.

### 5.2 Judge request and response contract

Proposed request fields are schema version, request ID, rule version, question-set version,
judge identity, finding ID, original label, deliverable kind, quote, defective span,
stated wrong outcome, verified evidence excerpt, decision basis, required items and constraints.
Each supplied excerpt carries its artifact digest and verification state.
The judging view omits original labels and author identity to reduce anchoring.
The local audit envelope retains those fields; they are not sent to the judge.
Every quoted field is inert data, never an instruction to the judge.

A judge returns request ID, model identity, question IDs, probabilities where available,
explicit skipped-question reasons, and latency or a typed failure.
Accept only finite probabilities between zero and one and the requested question IDs.
Duplicate IDs, missing required answers, wrong request ID or malformed output are failures.
Boolean reviewer labels stay booleans with unknown calibration, not synthetic confidence 1.0.
A fixture judge supplies recorded answers for offline contract tests.

Local validation checks byte-present anchors, required-section presence and exact counts first.
Absent input makes the relevant question UNSET, meaning not supplied or not answered.
A failed call, unavailable evidence or absent decision basis is never interpreted as no.

| Deliverable | Required source of decision basis |
|---|---|
| Specification | Requirements, acceptance criteria, declared destinations and invariants. |
| Tasklist | Driving spec and the current task's acceptance criteria and constraints. |
| Research report | Recommendation, evidence supporting it, destination tables and quoted headline figures. |
| Code change | Declared API behavior, acceptance checks, affected state invariants and scope boundaries. |
| Other | Caller-supplied basis with evidence; otherwise UNSET and no automatic downgrade. |

### 5.3 Table, confidence and explicit departures from the sketch

Reference the existing design artifact `02-brainstorm/blocker_truth_table_sketch.py`;
implementation must not copy this proposal as untested production logic.
The six decisive inputs are S, M, C, W, E and D; four states yield 4096 combinations.
The sketch is useful precedent, but its current behavior is not the complete safety contract.

Verified disagreement: `jev-uses.md` says wrong is no only when both W and E are no.
The live sketch also returns no when one is no and the other is UNSET.
It can also return FOLLOW_UP with S UNSET because only unsettled S is lifted.
That permits a missing safety answer to look safer than an uncertain answer.
Its monotonicity loop excludes comparisons involving UNSET, so its check is narrower
than an unconditional claim that increasing every input can never lower the verdict.
The code wins as the description of today's sketch, not as the desired policy.

Required policy: verified protected risk blocks; missing work or confirmed obligation blocks;
otherwise a wrong result or contradicted claim combined with dependency blocks.
An irrelevant real weakness is FOLLOW_UP; a cosmetic observation is NOTE.
Missing decisive inputs, unresolved safety or contradictory answers produce SHOW_USER.
In an unattended run SHOW_USER retains the existing protocol label and records uncertainty.
No usable answer after fallback is UNDETERMINED, not PASS.

The supplied ordinary bands, 0.30 and 0.70, and lower safety bands are experimental only.
Thresholds and their inclusive boundaries must be versioned and approved after calibration.
The reported weakest-link score is an uncalibrated routing score, not proven correctness.
The minimum of two probabilities is an upper bound on their conjunction, not a lower bound.
Therefore a high minimum cannot by itself justify confidence that both conditions hold.
For a confirmed W-and-D path, a dependence-safe lower bound is max(0, pW + pD - 1).
For a non-blocking path, upper-bound wrong by min(1, pW + pE), then upper-bound
blocking by min(1, pS + pM + pC + min(wrong-upper-bound, pD)).
One minus that upper bound is a candidate conservative non-blocking routing score.
These bounds still depend on calibrated marginals; they do not prove factual correctness.
Threshold authority requires held-out calibration of the complete decision, not just each question.
Missing decisive probabilities must prohibit downgrade, not contribute artificial certainty.
Return confidence as null for SHOW_USER, UNDETERMINED and reviewer-only fallback.
Never compare raw confidence across judges as if their calibration were identical.

### 5.4 Runtime, privacy and reproducibility

Fallback order is approved Jev, approved independent language-model judge, reviewer label.
Privacy denial skips all unapproved external judges, including the fallback model.
Without a key, fall back immediately; never ask for one inside a review.
Proposed operational bounds are a 10-second attempt, one retry for transient errors,
and a 30-second total classifier budget per finding, including all fallback attempts.
Honor server retry delays only within the remaining budget; then record timeout and fall back.
Authentication failures skip retries; a run-local circuit breaker avoids retrying every finding.
Classifier outage never invents a clean verdict or extends a review's fix-cycle cap.

Cache key includes canonical finding and evidence digest, decision-basis digest, required-item
and constraint digests, question version, rule and threshold version, judge/model version,
privacy/redaction policy and replicate ID. A changed decision basis invalidates the result.
Cache successful validated responses only; negative availability caching is short and run-local.
Keep raw judge responses separately from derived decisions so new thresholds can replay them.
Calibration runs bypass decision caches; repeated samples must not be falsely counted as independent.

The supplied research reports a Bearer key dependency using `TYPESAFE_API_KEY`.
This session did not inspect credentials or verify current vendor terms or availability.
Use a process environment secret, never a repository, prompt, ledger or request-body field.
Logs must exclude authorization headers and redact secrets in errors, including client traces.
Persist the exact approved request body for reproducibility without its authentication material.
Default logs hold digests and metadata, not private finding text.
Full payload logging is explicit opt-in, access-restricted and retention-bounded.
Redacted outbound payloads are the exact payloads logged; never keep a hidden unredacted twin.
Owner approval of data leaving this private fork is required before any external judge is used.

### 5.5 Shadow and later severity scoring

Start shadow-only: record original label, advisory verdict, score, judge, uncertainty and time.
The classifier cannot change a fix brief, gate outcome or promotion while shadow-only.
Use the program's 30-plus blindly scored findings, split by deliverable and consequence type.
Run five independent evaluations and report disagreement and flip counts, not just an average.
Keep a held-out subset and prohibit clauses written to rescue individual examples.
Jev's later five-level Score experiment uses the same human rubric, preserving per-level
probabilities; an average score can hide a mixture of harmless and dangerous outcomes.
No severity-scoring rollout or permission to populate implement's checklist follows automatically.

## 6. Guardrails against hiding real defects

- A concrete wrong result requires read-back evidence, not a persuasive reviewer narrative.
- A safety claim cannot be demoted by labels, model confidence or fix cost.
- Required sections are judged in substance, but an invented requirement cannot create a blocker.
- Unknown grounding stays visible and follows the protocol's existing incomplete-review path.
- A fresh reviewer may challenge a downgrade by naming the violated condition and consequence.
- Escalation records both decisions; it does not erase prior reviewer disagreement.
- Review caps remain fixed; follow-up-only changes never justify another gate round.
- Sample non-blocking items with a reviewer independent of the author and classifier judge.
- Review all protected-risk disagreements, not just a random subset.
- Count unique confirmed blockers consistently across cycles; do not lower counts by relabeling duplicates.
- Preserve regression detection before monotonicity, then the protocol-specific hard cap.
- Report the inspected scope and missing inputs even when there are zero findings.
- Do not accept fewer blockers as evidence of quality without an escaped-defect audit.

## 7. One source of truth and retained severity scales

Proposed canonical authoring file: `src/superclaude/core/REVIEW-SEVERITY.md`.
It defines the three conditions, uncertainty, record-and-offer contract and version identifier.
This is a new proposed file, not an existing repository resource.
Its installed lookup is `~/.claude/REVIEW-SEVERITY.md`, with project `.claude/REVIEW-SEVERITY.md`
as the explicit development surface. Neither currently gains a new file from this proposal.
Plugin-only commands need a generated parity copy under the shipped plugin rules surface.
Consumers name installed and project surfaces; plugin consumers additionally name their fallback.
Installed instructions must never tell a different project to read a source-tree path.

The core installer already globs Markdown files, so fresh copying needs no new glob logic.
However the live development sync omits core, and plugin packaging copies rules but not core.
The implementation plan must add generation and parity checks for these missing surfaces.
A bare promise that a new core document automatically reaches all installations is false.
Existing non-forcing installs can keep stale consumers; mixed versions must be detected.

Prefer short references plus a rule-version marker over eleven hand-edited full definitions.
A drift test checks canonical content, generated byte parity, reference reachability and markers.
A consumer missing the required version retains the old gate and reports a version mismatch;
it does not choose whichever definition gives the easiest PASS.
A running loop pins its rule version; upgrading the rule starts a new loop rather than rewrites history.

| Model family | Recommended boundary |
|---|---|
| rf-qa and general document loops | Adopt the common rule and follow-up contract. |
| spec-panel | Keep expert labels, derive blocking by consequence, preserve its own structural checks. |
| implement | Keep four-checklist derivation, read-back, origin caps and halt path unchanged in v1; export records only. |
| reflect | Keep deviation classes and existing promotion gate unchanged in v1; no automatic Drift downgrade. |
| card converter | Keep word translation for compatibility; do not add an independent classifier here. |
| PR review router | Keep routing tiers and authorized remediation contract; optional report-only export is separate. |
| Code-assigned structural and safety detectors | Keep deterministic checks; do not send them through a language judge. |
| Tasklist validation | Replace label-only Medium blocking only in an explicitly reviewed adapter stage. |

"Framework-wide" means common default and explicit adapters, not accidental repeal of domain policy.
The inherited implement exemption remains explicit until its owner approves a separate change.

## 8. Files and primitives that would change

Live Grep pattern `Grade every review finding as blocking or minor` returns 11 lines
in 11 files under `src/superclaude`, listed below. These are exact definition copies.
The preamble's 21 files and 109 occurrences is not the result of that search.

| Exact-copy path under src/superclaude | Required change |
|---|---|
| `output-styles/pragmatic.md` | Default consequence rule and record-and-offer owner. |
| `agents/rf-qa.md` | Common classification and persistent follow-ups. |
| `agents/rf-qa-qualitative.md` | Same, preserving contradiction discovery and safety checks. |
| `templates/documents/agent_template_qa.md` | Generate references and follow-up return fields. |
| `templates/documents/skill_template.md` | Generate the same contract. |
| `templates/workflow/01_mdtm_template_generic_task.md` | Record-and-offer and blocker-only fix flow. |
| `templates/workflow/02_mdtm_template_complex_task.md` | Same without changing intensity-specific caps. |
| `rules/prompts/automated_qa_workflow_qa_prompt.md` | Reference the common rule. |
| `rules/prompts/doc_code_analyst_qa_prompt.md` | Reference the common rule. |
| `rules/prompts/documentation_expert_qa_prompt.md` | Reference the common rule. |
| `rules/prompts/recruiting_expert_qa_prompt.md` | Reference the common rule. |

Live pattern `at most 2 fix cycles \(3 reviews\)` returns 12 files, adding spec-panel.
Live pattern `follow-up candidates` returns seven matching lines in three source files:
`output-styles/pragmatic.md`, `commands/spec-panel.md`, and
`rules/prompts/document_review_loop_prompts.md`. These all need consistent offer wording.
Live `2 fix cycles` returns 22 files and 120 matching lines, not 120 literal occurrences.
The enrichment's 139 occurrences counts repeated matches within lines, a different measure.

Additional integration sites from those searches and the supplied enrichment:
| Paths under src/superclaude unless stated otherwise | Intended scope |
|---|---|
| `skills/task/SKILL.md`, `skills/task-builder/SKILL.md`, `agents/rf-task-builder.md` | Consolidation, blocker-only fix briefs and ledger ownership. |
| `skills/tech-research/SKILL.md`, `skills/tech-reference/SKILL.md` | Research and document gate exports. |
| `skills/operational-guide/SKILL.md`, `skills/readme/SKILL.md`, `skills/roadmap/SKILL.md` | Same common rule at existing cap sites. |
| `skills/prd/refs/build-request-template.md`, `skills/tdd/refs/build-request-template.md`, `core/HOW-WE-WORK.md` | Consistency checks at cap references; avoid gratuitous cap changes. |
| `core/WORKER-CONTRACT.md` | Additive follow-up fields and coordinator consumption. |
| `commands/issue.md`, `skills/sc-issue-protocol/refs/create.md` | Document or add consent-bound ledger adapter; keep existing create interface truthful. |
| `skills/sc-implement-protocol/refs/qa.md` | Export adapter only, preserving checklist and no-prompt completion. |
| `skills/sc-troubleshoot-protocol/refs/report-template.md` | Export existing follow-up tasks. |
| `skills/sc-reflect-protocol/refs/report-template.md`, `skills/sc-reflect-protocol/SKILL.md` | Export eligible deviations, preserving promotion policy. |
| `skills/sc-tasklist-protocol/SKILL.md` | Explicit adapter for Medium and blocker counting after separate validation. |
| `cli/review/card_convert.py` | Compatibility check only, no planned rule rewrite. |
| `Makefile`, `scripts/build_superclaude_plugin.py`, `cli/install_core.py` | Development/plugin delivery and installed-name visibility checks. |
| `plugins/superclaude/commands/spec-panel.md`, `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` | Parity with source consumers, not assumed automatic generation. |

Installed-only review variants are migration candidates, not assumed source files on this branch.
Their exact full propagation surface remains UNVERIFIED here; inventory before planning changes.
The implementation plan chooses classifier and adapter module paths after examining existing APIs.
This specification deliberately does not invent production paths that have not been selected.

## 9. Tests and acceptance checks

The enrichment identifies eight rule or severity pin modules and two edit-list fixtures.
That count is not exhaustive: live Read also found a transitive PASS/FAIL pin in
`tests/audit/test_invariant_preservation_NFR_6_through_10.py`.
Keep that additional module in the plan's verification surface.

| Existing test path | Required treatment |
|---|---|
| `tests/skills/test_review_severity_rule.py` | Replace positional five-bullet extraction with canonical-document and consumer-reference checks; preserve cap and banned-phrase checks. |
| `tests/skills/test_review_severity_mapping.py` | Update placement-dependent Medium pins; retain explicit consent, unattended record-only and safety assertions. |
| `tests/skills/test_implement_severity_static.py` | Preserve specialized-model exemption and unchanged implement behavior. |
| `tests/skills/test_review_loop_extension.py` | Preserve caps, stable IDs and no extra edits before final review. |
| `tests/skills/test_review_prompt_overrides.py` | Preserve independent stance, no quota and zero-finding validity. |
| `tests/audit/test_nfr_conv_9_zero_trust.py` | Update label-only verdict pins intentionally, not by weakening evidence verification. |
| `tests/audit/test_severity_floor_unweakened.py` | Review the pinned Critical Rules hash and contradiction floor explicitly. |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | Preserve synthetic missing-reviewer failures and cap semantics. |
| `tests/skills/fixtures/review_severity_cap_edits.yaml`, `tests/skills/fixtures/review_severity_sweep_edits.yaml` | Update only approved changed strings; do not bypass historical protections wholesale. |

The contradiction floor currently treats contradictions as IMPORTANT or CRITICAL.
Keep surfacing every contradiction, but separate discovery from consequence-based gating.
Any change to that floor needs explicit approval and behavioral regression evidence.

New acceptance cases must cover:
- The three blocking conditions, cosmetic notes, irrelevant false claims and changed destinations.
- All 4096 decisive state combinations, including missing safety and dependency inputs.
- Monotonicity for known evidence and a separate missing-input rule that forbids downgrade.
- Invalid probability, missing answer, wrong request ID, timeout, denied privacy and no-key fallback.
- Repeated import, changing line numbers, changed reviewer IDs and independent co-located defects.
- Resume after a ledger write, concurrent stale rewrite, corrupt file and unavailable disk.
- No question or GitHub call from unattended workers; correct contract counts and artifact paths.
- No issue before consent; changed set requires new consent; timeout after successful remote creation.
- One batch issue, atomic write-back, metadata failure, wrong-fork URL and ambiguous reconciliation.
- Fresh install, stale install, development lookup and plugin-only lookup of one identical rule.

Static string pins are necessary delivery checks, not evidence that agents obey the flow.
Run behavioral fixture replays and held-out finding evaluation in addition to static tests.
No tests were executed in this specification task.

## 10. Rollout stages

| Stage | Work and exit condition |
|---|---|
| 0: establish evidence | Inventory source and installed variants; validate 30-plus historical findings and three blind scorers; freeze a rubric and held-out split. |
| 1: offline contract | Ledger adapters, table and fixture judge pass missing-input, identity, persistence and filing-reconciliation cases without external calls. |
| 2: shadow | Five evaluations and live shadow observations record disagreement without changing any gate. Jev experiments need separate privacy and key approval. |
| 3: default pilot | Output style and rf-qa family adopt the shared consequence rule for a bounded pilot; classifier still advisory, follow-ups persist and offers are attended only. |
| 4: propagate | Templates and other document loops adopt checked adapters; validate installed and plugin parity. Preserve specialized models as listed. |
| 5: optional classifier authority | Owner explicitly authorizes a calibrated routing policy after audited shadow evidence; never implied by completion of stage 4. |

A checked `/sc:workflow` plan must precede framework edits; this specification is its input.
Do not change the rule mid-loop to achieve a reduction target.
Stop propagation on a failed delivery or contract check, not after copying a partial rollout.

## 11. Metrics and revert triggers

Measure per protocol, rule version, judge and deliverable kind:
- Unique blocker and follow-up counts, not summed reviewer duplicates.
- Fix cycles, extra re-reviews and gate elapsed time before and after adoption.
- Audited non-blockers later judged consequential: counts and denominator.
- All protected-risk disagreement and escape counts, separately from ordinary errors.
- Classifier agreement, abstention, five-run flips, timeout, fallback, latency and cost.
- Ledger capture failures, unresolved identity matches, repeated offers and duplicate issue attempts.
- Completion with records versus silent loss; missing ledgers are operational failures.

Proposed pilot audit: all safety disagreements plus at least ten non-blockers per pilot run,
or all when fewer exist. Report selection and reviewer disagreement; do not call it unbiased accuracy.
Any confirmed protected-risk downgrade, unauthorized issue or wrong-fork post disables the new
routing path immediately and freezes outward retries until the owner resolves the incident.
A confirmed consequential escape pauses automatic demotion and triggers case review.
Duplicate creation or incomplete capture disables filing while keeping local records readable.
Ordinary gate-time regression in two comparable pilots triggers review, not automatic label inflation.
Revert policy and thresholds, never erase ledgers or roll back already created issues blindly.

## 12. Risks and operational failure modes

| Failure | Required response |
|---|---|
| Model unavailable or budget exhausted | Bounded fallback; preserve existing protocol judgment and report source. |
| Network judge denied by privacy policy | Skip it without prompting; no key discovery or secret logging. |
| Missing decision basis | UNSET, no automated demotion; report the missing input. |
| Persuasive but false reviewer narrative | Require source read-back; judge cannot authenticate the world. |
| Ledger write denied, full disk or bad encoding | Preserve old file, expose capture failure and do not claim successful recording. |
| Concurrent writer or resume overlap | Revision conflict; re-read and reconcile, never last-writer-wins. |
| Filing reply lost after remote success | Reconcile batch marker; never blind create retry. |
| Changed evidence after approval | Invalidate digest and consent for changed scope; keep history. |
| Shared rule inaccessible or mismatched | Retain old gate, report mismatch, do not silently bypass. |
| Small historical sample or disputed labels | Report uncertainty and scorer spread; expand cases before gating. |
| Human-approved follow-up grows into a feature | Re-enter normal scope and planning rules, not the old review's fix cycle. |

## 13. Owner decisions and recommendations

| Decision | Recommendation and consequence |
|---|---|
| Accept the three-condition default? | Yes, with explicit required-behavior and uncertainty wording; not every true observation should halt. |
| One issue or one per finding? | Default one issue for the selected set after consent; splitting is a new user request. |
| Change implement or reflect gates now? | No. Export their records first and preserve their current authority. |
| Relax the qualitative contradiction floor? | Separate discovery from gating only by explicit approval; preserve detection and evidence requirements. |
| Send private finding excerpts to TypeSafe or another external judge? | No by default. Approve a bounded experiment only after retention and processing terms are accepted. |
| Supply a key and experiment budget? | Defer until privacy approval; no key request is made here. |
| Allow classifier demotion after shadow? | Separate decision after held-out and live audit results; never enable by installation default. |
| Let the classifier populate implement checklist answers? | No in v1; changing that judge requires separate evidence and approval. |
| Accept proposed timeout and audit budgets? | Use them for the pilot, measure real latency and sample adequacy, then revise explicitly. |
| Resolve the record-only versus offer conflict? | Keep implement internally no-prompt; an attended outer session may offer only after that command completes. |

## 14. Verification and limits

Load-bearing enrichment claims spot-checked directly against live source in this session:
| Claim | Source checked | Result |
|---|---|---|
| Exact shared definition occurs in eleven files | Grep across `src/superclaude` | Confirmed, eleven lines in eleven files. |
| Medium records and user consent already exist | `src/superclaude/output-styles/pragmatic.md` | Confirmed as prose, not a runtime guarantee. |
| Canonical tests assume five adjacent bullets | `tests/skills/test_review_severity_rule.py` | Confirmed positional extraction. |
| Core Markdown is copied automatically | `src/superclaude/cli/install_core.py` | Confirmed glob and keep-existing behavior. |
| Development sync omits core | `Makefile` | Confirmed for the complete sync-dev target read. |
| Plugin build includes rules, not core | `scripts/build_superclaude_plugin.py` | Confirmed directory-copy list. |
| Important and medium are converter non-blockers | `src/superclaude/cli/review/card_convert.py` | Confirmed word sets, not consequence judgment. |
| Implement derives severity from four answers | `src/superclaude/skills/sc-implement-protocol/refs/qa.md` | Confirmed read-back and specialized precedence. |
| Four record formats really differ | rf-qa, implement, troubleshoot and reflect source templates | Confirmed actual tables, notes lines and deviation blocks. |
| Issue create is one description and posts directly | `src/superclaude/commands/issue.md`, create reference | Confirmed, no batch or preview option. |
| Unattended issue filing is forbidden | `src/superclaude/core/WORKER-CONTRACT.md` | Confirmed never-as-worker and no-outward-action rules. |
| Tasklist Medium and reflect Drift currently block | Their source SKILL files | Confirmed; neither can be silently relaxed by the default. |

Corrections to inputs: 21 exact copies and 109 occurrences is not reproducible by the
exact-definition pattern. The sketch treats some UNSET answers as no and does not test
monotonicity across UNSET transitions. The claimed eight pin modules omit an additional
transitive invariant test. These facts narrow the design, not justify weaker safeguards.

Not verified here: vendor documentation, account tier, retention terms, keys, Jev behavior,
latency, price, calibration, actual historical sample labels, mirror byte equality or a live install.
The Jev research is an input report, not a new vendor verification by this variant.
The reported 4096-case execution was not rerun; this session inspected the sketch only.
No external judge, GitHub operation, Git write, source edit or test execution was performed.
Only this specification file was created and incrementally populated.
