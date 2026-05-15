# Critique 3 — QA Position

## QA Position (Steelman)

A merge orchestration prompt is only as good as its weakest failure-mode branch. The source prompt is a clean happy-path script — read this, run that, hand off — but it treats every external call (Agent tool, /sc:analyze, /sc:adversarial, /sc:reflect, /sc:spec-panel, prd skill) as if it will return cleanly, terminate cleanly, and never contradict its neighbors. Real orchestrations don't behave that way.

The QA position is: the prompt must encode (1) what to do when a call returns non-terminal, errors, or violates a threshold; (2) what to do when proposals exceed the adversarial protocol's 2-10 file limit; (3) what to do when expert revisions contradict the conflict rule the prompt is built around; (4) what to do when the conflict rule itself doesn't have an answer for a given mechanism; and (5) how to make the test/acceptance language in Phase 6 observable instead of aspirational. Without these, the prompt produces deliverables whose quality cannot be verified post-hoc, and silently swallows partial failures into the PRD.

Variant 3 keeps the source's high-level shape (eight phases, same skills, same anchor document) but adds: a global failure-mode contract (retry budgets, halt-or-degrade artifacts, decision gates, freshness-hook discipline, no-invented-flags rule), an extended four-case conflict rule, a defense process for conflicting expert revisions, an observable Acceptance Criteria section in the release spec that propagates to the PRD, an explicit handling rule for INPUT_SPEC (because the prd skill does not recognize that field by name), and per-phase failure branches with named state artifacts. The cost is verbosity. The benefit is that every phase has a documented exit path — PASS, DEGRADED, or HALT — and every exit path leaves an evidence file that a human or downstream agent can act on.

## Critique of Source (Baseline)

Failure-mode diff points, indexed Q-NNN:

- **Q-001. Phase 4 file-count overflow has no merge logic.** The source says "Mode A requires 2-10 files; batch in passes if needed" but never specifies how batches are merged into a single convergence verdict. If Phase 3 produces 11+ proposals, the prompt fragments into N parallel adversarial runs with no acceptance criteria for combining them. Variant 3 fixes this by capping Phase 3 at 10 proposals with a deterministic merge rule before Phase 4 begins.

- **Q-002. Phase 4 convergence < 0.80 has no branch.** The `--convergence 0.80` flag is set but the prompt is silent on what happens if the adversarial protocol reports a sub-threshold result. Phase 5's `/sc:reflect` is not documented as a convergence-catcher in its command file (the reflect command does task/session/completion validation, not adversarial threshold enforcement). Variant 3 adds an explicit Phase 4 decision gate with three options (exclude lowest-scoring proposal, re-run at lower depth, or mark DEGRADED) and surfaces the failure to the user rather than letting it slide into Phase 5.

- **Q-003. Phase 7 conflicting-revision defense is undefined.** The source says "defend it with FINAL-REPORT evidence and accept only revisions that respect it" — but how? Is the spec rolled back? Are conflicting revisions silently accepted? Is there a rejection log? Variant 3 specifies a five-step deterministic defense process (classify, identify-invariant, cite, decide, escalate) with named rejection/override/escalation state files, plus a rejection-rate threshold that triggers a user prompt rather than silent acceptance.

- **Q-004. `/sc:reflect --type task` non-terminal return has no retry/escalation.** The reflect command's flags are documented as `--type task|session|completion`, `--analyze`, `--validate`. None of these guarantee a terminal verdict. If the call returns "still pending" or any non-terminal status, the source prompt has nothing to say. Variant 3 specifies one retry with `--type completion`, then DEGRADED + manual signoff requirement.

- **Q-005. Phase 1 empty-bucket branch is missing.** Bucket F is the only one that depends on existing live release specs under `.dev/releases/current/`. In a fresh repo or on a first run, this bucket can return EMPTY. The source prompt does not say whether to halt or skip. Variant 3 declares Buckets A-E mandatory (halt if any returns EMPTY/DEGRADED) and Bucket F degrade-acceptable (substitute the template-only path).

- **Q-006. Conflict rule is one-sided.** "Task-builder wins" is a complete answer only when task-builder has a stance. The prompt does not cover: neither has a stance, task-builder is silent on an additive /sc:tasklist mechanism, both have partial overlap. Variant 3 introduces a four-case rule (CASE-A authoritative, CASE-B additive, CASE-C deferred, CASE-D partial-with-invariant-check) with explicit decision branches.

- **Q-007. Acceptance criteria are not observable post-PRD.** Phase 6 mentions "test plan" but does not require observable behavior, verification method, and negative criteria. Variant 3 mandates an `## Acceptance Criteria` section per accepted proposal with all three fields, propagating to Phase 7 review and Phase 8 PRD mirror-check.

- **Q-008. `INPUT_SPEC` is not a documented prd skill input.** The prd SKILL.md (lines 33-43) documents WHAT / WHY / WHERE / OUTPUT only. Passing `INPUT_SPEC` as a literal field has no guarantee of being read. Variant 3 routes the release-spec path into the WHAT and WHERE fields the skill actually parses, with `INPUT_SPEC` left as optional forward-compatibility, and adds a post-invocation acceptance-criteria mirror check.

- **Q-009. Freshness-hook compatibility is implicit.** New file creation under `.dev/releases/current/task-builder-merge/` may trigger the freshness hook on first write. Variant 3 makes the touch+Read pattern explicit in the Global Failure-Mode Contract (item G4) so no phase silently fails on first file emission.

- **Q-010. No pipeline-state tracking artifact.** Without a per-phase log, debugging a failed run requires re-deriving what happened from scattered outputs. Variant 3 mandates `state/pipeline-log.md` with phase id, timestamps, outcomes, and output paths.

- **Q-011. `--focus structure,completeness` is suspect in Phase 4.** The /sc:adversarial command documents `--focus` as a single focus area (the command file lists focus values, not comma-list semantics). The source prompt's comma-list usage is not verifiable against the ground truth provided. Variant 3 splits this into two sequential passes (`completeness` first, then `correctness` if needed) using only single-value invocations to stay inside verified-flag territory. (Note: this is conservative — the actual /sc:adversarial command may well accept lists; without ground-truth confirmation, the safe option is sequential passes.)

- **Q-012. Phase 4 output-directory missing case is not handled.** If `/sc:adversarial` runs but fails to write the `--output` directory, Phase 5 has nothing to reflect on. Variant 3 adds an explicit halt condition on missing adversarial output.

## Acknowledged Weaknesses of My Variant

- **Verbosity.** The Global Failure-Mode Contract plus per-phase branches roughly doubles the prompt length. This is the dominant cost. Argument: the verbosity is in lookup-tables and state-artifact paths, not in repeated instructions, and is mostly skim-past on a clean run.

- **Sequential `--focus` passes in Phase 4.** Variant 3 conservatively assumes `--focus` is single-valued; if /sc:adversarial actually accepts comma-lists, this doubles the adversarial wall-clock for no benefit. Mitigation: leave a note that this is conservative and revertible once the flag semantics are confirmed against the command file.

- **Four-case conflict rule adds Phase 3 overhead.** Every proposal now needs a case classification. For a 5-proposal run that's 5 extra header fields; for 10 proposals, 10. Not enormous but non-zero. The benefit is that CASE-C (deferred) and CASE-D (partial) proposals are no longer silently auto-classified as CASE-A.

- **State artifact proliferation.** A run that hits multiple failure branches can produce 10+ state files. Without a top-level summary, a human reader still has to chase them. Variant 3 mitigates with `pipeline-log.md` as the single index, but a fully clean dashboard is out of scope.

- **Phase 7 defense process is sequential and Phase 7 may be slow.** Five-step classification per conflicting revision, with FINAL-REPORT lookups, is not free. Acceptable for a high-stakes spec; would be excessive for a quick iteration. Variant 3 does not provide a "fast mode" toggle.

- **Manual signoff escape valves create review burden.** Several DEGRADED branches require human signoff in a named file. If runs frequently hit these branches, signoff fatigue is a real risk. The alternative — silently proceeding — is worse, but the friction is real.

## Critical Failure Modes the Source Ignores

Ranked HIGH / MEDIUM / LOW by likelihood-times-impact:

**HIGH**

- **H-1. Convergence-below-threshold silent pass.** /sc:adversarial reports a sub-0.80 convergence, the source prompt's Phase 5 reflect call may or may not catch it (reflect's documented `--type` values don't promise convergence enforcement), and the release spec is drafted from a weakly-converged proposal set. The PRD inherits the weakness without any signal that the floor was missed. This is the highest-impact failure: the deliverable looks complete but is built on disagreement that was never surfaced.

- **H-2. Conflicting expert revision silently accepted.** Phase 7 says "defend it" with no defense process. A panel expert recommends a change that contradicts the conflict rule; the orchestrator either applies it (violating the rule the rest of the spec is built on) or rejects it without a logged rationale (no audit trail). Either way, the spec's coherence with its own stated rule is at risk. The downstream PRD then inherits an internally-inconsistent spec.

- **H-3. Proposal-count overflow with no merge logic.** Eleven proposals come out of Phase 3. The source says "batch in passes if needed." How are batched convergence results combined? Are proposals from batch 1 and batch 2 directly comparable? The source is silent. Likely outcome: the orchestrator picks one batch, ignores the rest, and the dropped proposals show up nowhere in the audit trail.

- **H-4. INPUT_SPEC silently ignored by prd skill.** The prd skill's documented inputs are WHAT/WHY/WHERE/OUTPUT. Passing INPUT_SPEC may produce a PRD that doesn't reference the release spec at all, because the skill never read the field. The merger work then has a PRD describing the WHAT in the abstract rather than describing what was actually accepted in the spec. High impact because the PRD is the deliverable.

**MEDIUM**

- **M-1. Conflict rule has no answer for "neither has a stance."** A /sc:tasklist mechanism the source prompt is silent on, that task-builder is also silent on, hits Phase 3 with no decision rule. Likely outcome: the orchestrator either invents a stance (drifting from evidence) or drops the mechanism (under-coverage). Either way the FINAL-REPORT's full inventory is not represented.

- **M-2. /sc:reflect non-terminal return.** Reflect can plausibly return "still pending" or a status the orchestrator doesn't know how to interpret as PASS/FAIL. Source prompt has no retry, no escalation. Phase 6 may proceed on a non-validated adversarial outcome.

- **M-3. Empty Bucket F.** Likely on a fresh repo or first run. Source prompt does not say whether to halt or skip. Likely outcome: agent returns empty digest, downstream phases skip "shape reference" entirely, the release spec drifts from the template's intended shape.

- **M-4. Phase 6 acceptance criteria are aspirational.** "Test plan" is mentioned, but the source does not require observable behavior or verification methods. The deliverable can pass Phase 6 with a test plan that says "tests will verify the implementation works." Variant 3's mandate makes the criteria concrete.

- **M-5. Phase 4 output directory not created.** /sc:adversarial errors before writing files. Phase 5 reflect has nothing to read. Source prompt does not check. Likely outcome: Phase 5 proceeds on stale or missing data.

**LOW**

- **L-1. Cross-bucket contradictions from Phase 1 agents.** Two parallel agents return conflicting cross-references (Bucket A says file X exists in Bucket C's scope; Bucket C reports no such file). Source prompt does not check. Low impact because Phase 2 /sc:analyze should catch most file-existence issues; still a missed coverage point.

- **L-2. Freshness-hook failure on first file write.** Hook may complicate first writes to `.dev/releases/current/task-builder-merge/`. Source prompt does not mandate touch+Read. Low likelihood given the parent dir already exists, but a single hook failure could blow up a phase emission.

- **L-3. Invented-flag drift.** A future revision of the source prompt could add a flag that doesn't exist in the command files (e.g., `--retry`, `--strict`, `--max-iterations` if not actually present). Source prompt has no rule against this. Variant 3's no-invented-flags item (G5) closes this.

- **L-4. State-artifact proliferation without an index.** A run that exercises multiple DEGRADED branches scatters state files across `state/`. Without an index, a human reading the post-mortem hunts through directories. Variant 3 adds pipeline-log.md as the index; not a complete dashboard, but enough to find the relevant DEGRADED file.

- **L-5. Phase 7 rejection-rate runaway.** If experts overwhelmingly contradict the conflict rule, every revision goes through the rejection process and the spec barely moves. Source prompt has no signal for this; variant 3 adds a rejection-rate threshold that asks the user before continuing.
