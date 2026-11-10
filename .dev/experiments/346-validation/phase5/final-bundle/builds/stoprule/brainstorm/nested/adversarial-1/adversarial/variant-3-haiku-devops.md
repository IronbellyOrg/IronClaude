# Stoprule: fail-closed, auditable specification review

## 1. Problem and evidence

- S1 control ended with mean 6.0 critical+major findings and 63.5% growth; neither replicate passed.
- PR 427 cut growth to 29.7%, but left 6/5 critical+major findings; its flags produced 6/1 and 30.0% growth.
- In 427, 89% of R2 and 100% of R3 new findings were tagged changed-line: a ratchet does not remove fix-induced defects.
- Evidence: supplied seed/context and AB-REPORT, ARMB-REPORT, DECISIONS; n=2 per arm is a large-effect screen, not production proof.
- Choice: an additive command with a disk-backed controller, blinded confirmation, restricted fix packets, and explicit terminal escalation.

## 2. Mechanism

### 2.1 Authority and frozen rubric

All paths and script interfaces introduced below are PROPOSED, not existing features.
The command retains PR 427's critique/re-review shape and expert panel.
The companion skill defines the controller protocol; its standard-library script owns state,
quote checks, diff provenance, derivation, cap enforcement, and rendered verdicts.
The script does not call a model; the coordinator makes the bounded agent calls it requests.
This avoids storing provider credentials or inventing an installed model-transport CLI.

Store the following exact UTF-8 block in `refs/rubric.txt`, version `stoprule-v1`:

```text
FROZEN stoprule-v1
CRITICAL: The quoted instruction permits irreversible data loss, credential exposure,
unauthorized privileged action, or an unrecoverable production outage in the stated example.
MAJOR: Following the quoted text produces a concrete incorrect required outcome,
or two permitted implementations produce incompatible required outcomes on the stated input.
MINOR: Wording, completeness, preference, speculative risk, or an inferable detail
without a concrete incorrect required outcome demonstrated by the quote and example.
Blocking requires a verbatim quote and a concrete wrong outcome or failing example.
A GAP, blank boundary-table cell, expert disagreement, or severity label is not itself blocking.
Missing context is not evidence of a blocking defect; answer minor when it is insufficient.
```

Copy these bytes unchanged into every reviewer, grader, and reviser brief.
Persist their SHA-256 in the run manifest and every round envelope.
Reject a brief/rubric hash mismatch before dispatch; never revise the rubric mid-run.
These definitions override the variant's FR-8/FR-9 severity floors and FR-10 synthesis gate.
Keep boundary tables as diagnostic output; an incomplete table does not override the verdict.
Changing the rubric requires a new version and a new, explicitly separate experiment.

### 2.2 Begin and snapshot

1. Require critique mode for the controlled loop; other modes retain copied behavior
   but cannot claim a stoprule verdict or enter its fix controller.
2. Resolve one real target document and one operator-declared run directory.
   First use creates state exclusively; subsequent invocations must use that state.
   The companion protocol supplies this directory, not a new unverified slash-command flag.
3. Lock the run exclusively; snapshot exact target bytes before review N.
   Bind run id, canonical target path, target hash, command hash, skill/script hashes,
   rubric hash, reviewer/grader model identifiers, and monotonic start time.
4. Reserve review N durably before dispatch. N starts at 1 and cannot exceed 3.
   A crashed review consumes its reservation; recovery may complete its existing slot,
   but may not obtain a fresh reviewer call under the same slot.
5. For N>1, require the previous completed round and saved pre-fix baseline.
   Validate any supplied `--re-review` and `--baseline` against these records.
   Never downgrade missing state into a new first review for a known run.
   The variant discovers its prior state even when historical briefs omit these flags.
6. Compute changed line ranges from previous reviewed snapshot to current snapshot.
   Use line-based diff after collapsing whitespace runs and trimming line ends;
   preserve raw lines and line mappings for exact quote validation.
   Whitespace-only edits create no new eligible ranges; insertions/replacements do.
   Deletions use an old-side quote and deletion hunk anchor, not invented current text.

### 2.3 Reviewer input and finding-file contract

A reviewer gets the snapshot, copied rubric, prior finding statuses, and changed ranges.
It produces findings and resolution evidence, never a verdict or a revised document.
Each finding must quote the document, not a reviewer-generated boundary table.
For an omission, quote the requirement or guard whose promised behavior is incomplete.
The round's `reviewer.json` has this illustrative schema; comments are outside JSON:

```json
{
  "schema": 1, "run_id": "opaque", "round": 2,
  "target_sha256": "64 lowercase hex", "rubric_sha256": "64 lowercase hex",
  "prior_status": [{"id": "R1-F01", "status": "open", "evidence": "trace"}],
  "findings": [{
    "id": "R2-F01", "claimed_severity": "MAJOR",
    "anchor": {"side": "current", "start_line": 41, "end_line": 42},
    "quote": "exact snapshot text", "wrong_outcome": "specific failing trace",
    "prior_id": null, "suggested_fix": "smallest correction"
  }]
}
```

Required envelope fields are schema/run/round/hashes/findings/prior_status.
`claimed_severity` is CRITICAL, MAJOR, or MINOR; findings cannot contain a verdict.
Finding evidence fields may be null or empty: that is a valid evidence-poor finding,
mechanically minor, not permission to discard an otherwise valid round.
Reject invalid JSON, duplicate keys/ids, unknown fields, unsupported types or enums,
non-UTF-8, more than 100 findings, or an input larger than 1 MiB as infrastructure ERROR.
Require exactly one status for every previously open blocking id; omitted ids remain open
and make the round incomplete rather than silently resolving them.
Status enum is `resolved|open|regressed`; `resolved` requires a concrete resolution trace.
No-change re-review keeps prior blockers open regardless of a claimed resolution.
Resolution truth remains semantic reviewer work; record that residual risk explicitly.

### 2.4 Evidence gate, ratchet, independent confirmation

The script processes every claimed CRITICAL/MAJOR finding as follows:

1. Check a nonempty exact quote at the declared raw snapshot span and nonempty outcome.
   Missing evidence or quote mismatch => MINOR, reason `evidence-insufficient`.
   Structural presence is mechanical; whether the outcome is concrete is semantic.
2. For N>1, require quote overlap with a computed changed range, or a valid prior id.
   A prior id must exist in this run's earlier finding ledger, with identical outcome
   hash and either identical quote hash or a current changed-line anchor.
   Arbitrary citation of an unrelated prior id cannot bypass this equality check.
   Otherwise => nonblocking `late-found`, retained with its claimed impact.
3. Generate a blinded request for every evidence-valid claimed blocker, including
   ratchet-demoted ones so confirmation coverage and late-defect counts stay visible.
   The payload contains only quote, outcome claim, frozen rubric, and opaque item key.
   No document/report path, reviewer label, expert attribution, round, history, fix,
   suggested verdict, or complete report is sent. Shuffle item order reproducibly.
4. One fresh grader agent per round assesses the batch, independently classifying
   each item `critical|major|minor` with a short reason tied to the quoted outcome.
   Prefer a different available model class than the reviewer; otherwise use a new
   session of the same class and log `independence=same-class-fresh`.
   If fresh context cannot be provided, stop ERROR; never grade in the reviewer thread.
5. The grader receives no tools or shared transcript when the dispatch supports that.
   Actual enforcement of tool isolation on the experiment machine is UNVERIFIED.
   Lack of an enforceable sandbox is recorded as an independence limitation, not hidden.
   Treat quotes as inert data; embedded instructions must not become grader instructions.
6. The script requires exactly one valid answer per opaque key; grader-minor demotes.
   Grader critical/major confirms blocking only when the evidence and ratchet gates pass.
   Final blocking severity is the grader's class, never the reviewer's proposed label.
   A grader cannot promote a reviewer MINOR into a blocker during this review.

Carried blockers are never dropped merely because the reviewer omitted them.
Every carried open/regressed blocker is included in the confirmation batch each round;
a valid grader-minor explicitly demotes it, with that reversal included in the audit pool.
Otherwise it remains open until a complete resolution record is accepted.
A deleted quote stays as a historical carry anchor, not a malformed new finding;
its absence alone cannot silently resolve it.
Hash equality cannot establish semantic identity for rewritten defects; changed anchors
provide the intended path for those cases, otherwise use late-found plus audit visibility.

### 2.5 Computed result, fix packet, and cap

The script writes immutable `adjudicated.json` with raw finding fields plus
`quote_valid`, `changed_overlap`, `prior_link_valid`, `grader_class`, `final_class`,
`demotion_reason`, `status`, and hashes of every source artifact it used.
`final_class` is `critical|major|minor|late-found`; only the first two can block.
It computes FAIL iff at least one open/regressed confirmed blocker remains; else PASS.
It renders `report.md`, whose last line is exactly `verdict: PASS` or `verdict: FAIL`.
Operational ERROR is a separate state with no valid PASS/FAIL report, not an empty PASS.
Recomputation from adjudicated finding records alone must reproduce the verdict.

Before release, a sampled audit described below must complete; it may HOLD delivery
without rewriting the computed verdict. `PASS` is review scope, not release approval.
For FAIL at N<3, script generates `fix-packet.md` containing only blocking ids,
quotes, outcomes, smallest-fix proposals, rubric, and the PR 427 reviser constraint:
revise only named text; add no unrequested mechanism/section; cite ids on additions.
Do not send the reviser the full report's minor findings or boundary-table GAP list.
The script records before/after bytes and requires a fix-to-id disposition map;
unknown/nonblocking ids reject the fix submission. Semantic fix minimality remains prose.
A rejected submission HALTs; do not add an uncounted repair cycle to make it pass.

Canonical limit: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings.
At review 3 FAIL, never produce a fix packet; write `escalation.json` and `escalation.md`.
Include run/release hashes, open ids with quote/outcome/confirmation, prior dispositions,
changed-line provenance, late-found/minor counts, audit disagreements, costs, and reason.
The user receives artifact paths plus choices to accept a scoped risk, abandon, or
commission separate work. No fourth review, minor cleanup, extra boundary-table pass,
or automatic new loop is permitted; a new user-authorized run preserves the old run id as parent.

### 2.6 On-disk audit trail

Suggested run root: adjacent to the reviewed source, `.spec-panel-stoprule/<run-id>/`;
the operator may instead supply an experiment output directory. Do not use a global cache.
Proposed artifacts, all under that root:

```text
manifest.json                 pinned code/model/rubric hashes and target identity
state.json                    next transition, reserved rounds, terminal reason
rubric.txt                    exact frozen bytes for this run
round-1/ ... round-3/          allocated once, never silently reused
  input.md                    raw immutable snapshot
  changes.json                old/new ranges, normalized diff algorithm/version
  brief.md                    actual dispatched reviewer brief and rubric
  reviewer.json               raw response; raw-response.txt if not valid JSON
  grader-request.json         blinded items and opaque-to-finding mapping kept separate
  grader-map.json             local mapping; never dispatched to grader
  grader-response.json        raw structured decisions
  adjudicated.json            complete normalized finding ledger, computed classes
  report.md                   script-rendered narrative and verdict
  fix-packet.md               FAIL before cap only
  disposition.json            applied ids plus actual byte/line delta, if fixed
  audit.json                  sample seed, selected ids, outcomes, disagreement
  result.json                 verdict, audit hold, duration, counts, exit status
  events.jsonl                timestamped state transitions and errors
escalation.json / .md          terminal handoff on cap, ERROR, or audit hold
```

Events contain schema version, run/round, UTC timestamp, monotonic duration, event name,
artifact hashes, status/error code, model id, and observed agent/tool/token usage.
Use `null` for unavailable tokens/cost, never a fabricated zero.
Write temporary files in the same directory, flush, fsync, then atomically rename;
commit result/state last under the lock. A partial round is never considered complete.
Do not claim tamper-proof storage: hashes detect accidental drift, not a malicious owner.
Private quotes may contain sensitive content: restrictive directory/file permissions,
no quote text in summary logs, no external telemetry by default, operator retention policy.
Keep artifacts for the enterprise pilot for 30 days unless project policy requires longer;
cleanup is a separately authorized operation and never rollback's implicit side effect.

## 3. Exact changes

This section names proposed maintainer source locations, not runtime lookup paths.
No implementation or installation is performed by this document.

| File | Exact scope |
|---|---|
| `src/superclaude/commands/spec-panel-stoprule.md` (NEW) | Copy current spec-panel; rename title/usage/self examples; replace Review Loop; adjust conflicting FR-8/9/10 gates and output-verdict ownership only. |
| `src/superclaude/skills/sc-spec-panel-stoprule/SKILL.md` (NEW) | Dispatch, state transitions, independent grader, audit and incident runbook; announce skill base. |
| `src/superclaude/skills/sc-spec-panel-stoprule/refs/rubric.txt` (NEW) | Exact frozen block in section 2.1; no per-round variations. |
| `src/superclaude/skills/sc-spec-panel-stoprule/scripts/stoprule.py` (NEW) | Standard-library parser, snapshots, diff, gate, state, render, and recompute. |
| `tests/skills/test_spec_panel_stoprule.py` (NEW) | Executable helper tests plus narrow command/skill text assertions. |
| `docs/designs/spec-panel-stoprule.md` (NEW, implementation deliverable) | Deployment, rollback, schema, runbook, measurement definitions and results link. |

The existing original command, its tests, and installer implementation stay unchanged.
Plugin mirror inclusion is UNVERIFIED until its packaging contract is inspected;
if shipping through that surface, include matching additive command and skill files only.
Runtime text must never direct installed agents to a maintainer source path.
The new command's first blocking operation is this proposed instruction:

```text
Load skill sc-spec-panel-stoprule before review work. Resolve its installed SKILL.md
in ~/.claude/skills/sc-spec-panel-stoprule/ first, else .claude/skills/sc-spec-panel-stoprule/.
If neither exists, stop E-SKILL-MISSING; do not fall back to spec-panel.
This variant's frozen rubric and computed gate override other severity floors.
```

Helper invocation follows the verified managed-workspace pattern:
`uv run --no-project python "<skill base>/scripts/stoprule.py" <operation> <arguments>`.
Proposed operations: `init`, `prepare`, `adjudicate`, `record-fix`, `finish`, `recompute`.
These are design interfaces, not existing CLI flags; implement their help and tests together.
The helper accepts explicit paths, rejects traversal/symlink escapes from the run root,
uses a Linux advisory lock, and never executes target text or interpolates it into shell code.
It never modifies the specification: only a separately authorized reviser can do that.

Script outline: parse strict JSON -> validate pinned inputs -> load reserved slot ->
check quotes/diff/prior ids -> validate grader output -> derive classes -> append carried
blockers -> compute verdict -> render report -> bind audit -> commit terminal/next state.
`finish` refuses missing audit or inconsistent hashes; recompute makes no model calls.
Exit contract: 0=completed PASS, 1=completed FAIL, 2=ERROR, 3=audit HOLD.
At the cap, FAIL is still exit 1 with terminal `CAP_HIT`, never an automatic retry signal.

Tests must cover exact/no/duplicate quotes; omission anchors; old-side deletions;
whitespace changes; shifted lines; legitimate and forged prior links; grader-minor;
missing/extra grader keys; invalid JSON; hash drift; empty diff; missing prior status;
script crash between each commit boundary; lock contention; stale result reuse;
cap reservation after crash; fourth-review refusal; and unchanged original command hash.
Also test that recomputation ignores prose severity/verdict and that all-minor is PASS.
An install smoke test exercises only the additive file set in an isolated HOME.
Text tests prove rubric/brief instructions exist, not that a model obeys them.

## 4. Variant command name and install note

The additive name is `/sc:spec-panel-stoprule`.
Experiment brief substitution, and no other review-brief edit:
`/sc:spec-panel` -> `/sc:spec-panel-stoprule`.
The experiment harness supplies the same declared target/run-root mapping each round;
this variant persists its own baselines, so omitted historical re-review flags do not reset it.
Log that persistence as treatment behavior, not as an unchanged feature of PR 427.

Deploy exactly two additive surfaces on the experiment machine:
- `~/.claude/commands/sc/spec-panel-stoprule.md`.
- `~/.claude/skills/sc-spec-panel-stoprule/`, including rubric and helper.
Never edit, replace, rename, restore, or overwrite `~/.claude/commands/sc/spec-panel.md`.
`make sync-dev` alone is not activation: supplied reports observed personal command precedence.
The command installer discovers additive names and skips existing files without force;
its code was checked, but the skill installer's current behavior is UNVERIFIED.
Therefore do not run a machine-wide force install for this experiment.

Deployment procedure, to be implemented as an explicit additive-file installation:
1. Owner authorizes only these two destinations; record original command SHA-256.
2. Build/review a manifest of the new files and hashes; ensure destinations are absent.
   If a destination exists, stop instead of guessing ownership or overwriting it.
3. Stage the skill directory beside its destination and verify every manifest hash.
4. Publish the skill first, command last; use no-clobber publication on the same filesystem.
5. Start a fresh worker; verify the actual loaded command and skill hashes in its receipt.
   A textual copy on disk alone does not prove that a cached session loaded it.
6. Smoke-test malformed input, grader failure and cap behavior against copied documents.
   Compare the original command hash again before admitting the experiment.
7. During each round, recheck variant/rubric/helper hashes and original command hash;
   drift stops the run, because mixed versions destroy comparison validity.

Rollback runbook: stop dispatching the variant and join active writers first.
Move only the manifest-owned variant command out of command discovery, then its skill,
into an operator-declared quarantine directory; do not delete run artifacts.
Verify hashes before removal; changed or foreign files require owner intervention.
Restart/fresh-load workers, restore the original brief invocation, verify original hash.
If the original hash changed, report external drift; do not overwrite someone else's install.
Partial deployment has no command until the skill is ready; missing skill always fails closed.
Rollback means withdrawal of this experiment, not reversal of specification edits.
Any source-document revert needs separate user approval and the saved snapshot comparison.
No deployment, rollback, or experiment commands are run by this spec-writing task.

## 5. Measurement plan on scenario S1

Use S1's same 57,763-byte Orca worker-contract starting spec, T-pinned repository,
same verbatim review/fix briefs, reviewer model, step order, and two independent replicates.
Only substitute the command name; log actual loaded hashes and blinded grader model.
Use supplied control metrics as historical comparators; prefer contemporaneous unchanged
controls if separately authorized. Do not claim a randomized production trial.
Apply the same M1-M5 definitions: rounds to PASS/cap, blocking counts, changed-line share,
bytes/lines/growth, and tokens/tool calls where observable. Keep origin/master peeks visible.

**PREDICTED, not measured:** R3 confirmed critical+major = 2 and 3 (mean 2.5),
versus control mean 6.0 and bar <=3 in each replicate.
**PREDICTED, not measured:** growth after two fixes = 22% and 28% (mean 25%),
versus control mean 63.5% and bar <=44.4% in each replicate.
Prediction assumes most severity inflation is rejected without hiding genuine defects;
it does not assume changed-line defects disappear. PASS before R3 counts as early stopping,
not a fabricated observed R3 zero. Report final open count and actual cycles separately.
If early-stopped, report growth at stop; do not run gratuitous fixes to obtain cycle-two data.
Keep raw reviewer critical+major, confirmed blocking, and audited true-defect counts separate.
D10/D11's raw proxy is not directly equivalent to this filtered count: publish both,
and do not announce improved defect quality from a relabeling-only improvement.
Require the effect to exceed the larger within-arm spread and preserve per-replicate bars.

Audit 25% of ALL nonblocking dispositions each round, rounded up, minimum two or all
when fewer exist; stratify across grader-minor, evidence-insufficient, and late-found.
Use deterministic sampling from a seed committed before grader responses, and record
inclusion probabilities; sample at least one from every nonempty demotion stratum.
Also sample 25% of confirmed blockers, minimum two or all when fewer exist, as the
true-blocker comparison stratum; keep both samples blinded and weight by inclusion rate.
This estimates accuracy among reported findings, not recall of unreported defects.
One separate fresh audit agent sees the full snapshot, original quote/claim, and rubric,
not reviewer/grader labels or report. It judges blocking truth, then receives the gate reason
for attribution. A human adjudicates disagreement before any delivery is accepted.
Report weighted false-demotion fraction among demotions and fraction of audited true
blockers demoted, with numerator/denominator and uncertainty; small samples prove little.
Acceptance ceiling: <=10% of audited true blockers demoted, zero missed CRITICAL.
Any audited wrongly demoted blocker causes HOLD even below that ceiling; no silent waiver.
Require at least 20 audited true blockers across later pilots before general rollout;
S1 alone may leave this quality bar NOT ESTABLISHED. Audit all claimed-critical demotions
as a safety supplement, reporting that nonrandom stratum separately.
Falsification: either replicate exceeds a numeric bar, audit ceiling fails, a true critical
is demoted, recomputation differs, or the system passes only by hiding audited defects.
Infrastructure ERROR/HOLD is not a successful convergence result and stays in reliability totals.

## 6. Risks, costs, and failure modes

Budget per review: one existing reviewer, one extra blinded grader batch, and one extra
sampled-audit agent; skip an empty grader/audit batch and log why. No per-finding sessions.
Full loop maximum: 3 reviewers + 2 revisers + 3 graders + 3 auditors = 11 agent calls,
6 above the five-call review/fix baseline, plus the existing coordinator; human disputes
are escalations, not hidden free agent calls. No grader/reviewer automatic retry.
Expect 5-7 extra helper tool invocations per review for snapshot/gate/audit/finalization;
actual tool and token costs are recorded, not inferred from the number of model calls.

Proposed hard admission budgets: reviewer 15 min, grader 3 min, audit 5 min, helper
work 1 min per round; each fix 10 min. Full loop deadline is 92 min excluding human wait.
These are proposed ceilings, not measured latency predictions or existing CLI flags.
The coordinator enforces transport cancellation if available; capability is UNVERIFIED.
The script always checks persisted monotonic deadlines before accepting any next result;
late responses are quarantined and cannot revive a terminal run. This bounds accepted work,
not billed provider execution when cancellation cannot be enforced. No dispatch after expiry.

| Failure | Fail-safe result and operator action |
|---|---|
| Helper crash, ENOSPC, broken permissions | No committed result => ERROR; preserve partial artifacts, restore storage, recompute the same slot only if raw inputs already exist. |
| Malformed reviewer envelope | ERROR, save raw response, escalate; never parse only the convenient findings or treat missing JSON as zero blockers. |
| Valid finding missing evidence | MINOR with explicit reason; sampled audit detects suppressed real defects. |
| Grader unavailable, timeout, malformed/missing decisions | ERROR with pending candidates preserved; no demotion, PASS, or fix dispatch. |
| Auditor unavailable or real blocker found | HOLD delivery; retain computed verdict, explain disagreement, escalate without another automatic review. |
| Hash drift, target edited during review, lock collision | ERROR; keep snapshots; ask owner to reconcile, never resnapshot silently. |
| Deadline/cap exhausted | Terminal escalation; no fourth review, retry storm, or fallback to unconfirmed reviewer verdict. |

Proposed pilot SLOs: 100% verdict reproducibility; zero accepted fourth reviews;
100% nonempty candidate batches independently graded; zero infrastructure failures shown
as PASS; >=95% valid rounds finalized within 24 minutes, excluding fix and human time.
Latency/error denominators include unavailable graders and crashes. S1 is too small to
claim these SLOs met; export counts from result/events files, not a new monitoring service.
Page/escalate immediately on original-command drift, false PASS, or audited critical loss;
ordinary grader outages stop this workflow, not the enterprise's unrelated deployments.
Any downstream release gate must require terminal PASS AND completed audit without HOLD.

Severity drift is constrained mechanically, not eliminated semantically; rubric judgment
can still drift. Missing evidence and late discovery can hide real defects; audits trade
extra latency and false HOLDs for visibility. New mechanisms and minor fixes are reduced
by filtered packets/id checks, but semantic patch minimality is still prose.
Fix-induced defects on changed lines remain eligible and may still consume all reviews.
The absent mechanical stop is removed for cooperating controller users; a model bypassing
the helper or starting a new run is outside this script's enforcement boundary.
Enterprise admission must check its signed-off result artifact; hashes alone are not signatures.

## 7. Open questions

- Which transport on the experiment host can guarantee fresh, tool-restricted graders
  and cancellation? UNVERIFIED; test this before claiming enforced independence.
- Does the reduced quote-only context cause unacceptable false demotion? Audit decides;
  do not silently expand the grader input to the whole report to rescue the experiment.
- Can the host provide a genuinely different model class? Same-class fresh is allowed
  but must be reported separately, never pooled as equivalent independence evidence.
- Are enterprise document retention and provider data-handling rules compatible with
  storing/sending verbatim quotes? Owner approval is required before sensitive use.
- How often does the late-found rule suppress a real pre-existing defect? Track that
  separately; reuse elsewhere waits for evidence rather than assuming safety.

## 8. Reuse by other review commands

Reuse the strict envelope, hash-bound snapshots, provenance, blinded grading requests,
computed result and audit trail as a library-shaped contract, not a framework migration.
The initial script remains inside its companion skill; do not create a shared service yet.
`/sc:reflect` can later adapt evidence to its deviation categories; preserve its own verdicts
and authorization rules rather than replacing them with this specification's severity names.
rf-qa agents can emit the finding envelope while their parent owns the helper and cap;
a read-only reviewer must not gain permission to mutate delivery files or final results.
The `/sc:implement` final review already derives severity from checklist answers and
read-back; it deliberately lacks a second model pass. Keep that behavior unchanged here.
Its current QA model also allows late BLOCKERs to block, so importing stoprule's late-found
demotion would be a policy change, not harmless reuse. Final archive/release gates must
not hide a proven data-loss/security defect merely because it was discovered late.
Use separate opt-in experiments and adapter tests before adopting any part in these tools.
No claim is made that this additive variant addresses the four other incident toolchains.
