// =====================================================================
// Troubleshoot-Efficacy Pipeline (re-runnable Workflow) — RUN #2 (-2 isolation)
// =====================================================================
// This is a CONCURRENT-RUN copy of
//   .dev/troubleshoot/meta-efficacy-pipeline/troubleshoot-efficacy.workflow.js
// with all output isolated under the -2 directory so it cannot collide with
// the parallel run #1. Two deltas vs the original:
//   * EFFICACY-REPORT.md  -> .dev/troubleshoot/meta-efficacy-pipeline-2/
//   * rollback worktree   -> /tmp/prd-rollback-<commit>-2
//   * meta.name           -> troubleshoot-efficacy-2 (distinct in /workflows)
// Everything else is byte-identical to the original pipeline logic.
//
// PURPOSE
//   Determine how much of our debug -> task-build -> reflect -> validate
//   stack is THEATRE vs net value, root-cause WHY subsequent bugs kept
//   slipping through, derive ISSUE-AGNOSTIC remediations, refactor the
//   sc:troubleshoot pipeline to embody them, and PROVE the refactor by
//   rolling the PRD code back to the pre-whack-a-mole commit and replaying
//   the new pipeline against the known-miss ground-truth set (loop <= 3).
//
// REPO   /config/workspace/IronClaude   (the PRD pipeline + sc:troubleshoot live here)
// =====================================================================

export const meta = {
  name: "troubleshoot-efficacy-2",
  description:
    "Forensic audit of why the debug/task/reflect stack let PRD bugs through; generalized remediation; sc:troubleshoot refactor; rollback-replay validation (<=3 rounds). [concurrent run #2, -2 isolated output]",
  whenToUse:
    "Run when a long whack-a-mole debugging episode suggests the review pipeline is theatre, to root-cause the misses and harden the troubleshoot pipeline generally.",
  phases: [
    { title: "Forensic Timeline", detail: "parallel readers over git + .dev + session seed -> miss registry + theatre score" },
    { title: "Hypotheses", detail: "x2 diverse hypotheses per miss (why it slipped through review)" },
    { title: "Adversarial Merge (per miss)", detail: "steelman/score/merge the 2 hypotheses -> validated root cause" },
    { title: "Systemic Synthesis", detail: "merge per-miss root causes -> the few structural causes" },
    { title: "Generalized Remediation", detail: "x2 issue-agnostic remediations per cause -> adversarial merge -> one strategy" },
    { title: "Troubleshoot Refactor", detail: "concrete sc:troubleshoot refactor + would-have-caught matrix" },
    { title: "Rollback Replay", detail: "worktree @ pre-whack-a-mole; replay refactor vs ground truth; loop <=3" },
  ],
};

// ---------------------------------------------------------------------
// GROUND TRUTH — the known-miss registry (seed). Phase 1 RE-DERIVES and
// EXTENDS this from git + .dev artifacts; it is embedded so (a) agents are
// grounded and (b) Phase 7 has a fixed oracle to score replay coverage
// against. Each miss = a bug that a PRIOR review pass (troubleshoot /
// task-builder / reflect) should plausibly have caught but did not — it was
// instead surfaced by RUNNING the pipeline, one gate at a time.
// ---------------------------------------------------------------------
const ROLLBACK_COMMIT = "ac80f176"; // PRD state immediately BEFORE PR #151 (start of whack-a-mole)
const WORKTREE = `/tmp/prd-rollback-${ROLLBACK_COMMIT}-2`; // -2 isolation: own worktree, no collision with run #1

const GROUND_TRUTH = `
KNOWN-MISS REGISTRY (PRD pipeline, 2026-06-08..10). Each was caught only by
running the pipeline further, not by the review pass that preceded it.

M1  cloud-flag misuse: PRD pipeline passed LOCAL paths to 'claude --file' (a
    cloud download flag needing a session token) -> scope-discovery exit 1.
    Fix PR #151 (7601ad25). Sibling pipelines already forbade --file
    (FR-003/FR-023) -> the contract existed; the review never cross-checked it.
M2  _check_parallel_instructions enforced the parallel keyword on EVERY phase
    >=2, incl. the sequential completion phase -> halt at build-task-file
    "Phase 7 missing parallel...". Fix PR #154 (e97aa4fd). Never exercised
    during the #151 work (run never reached build-task-file before #151).
M3  After #154, the same regex matched Task-Log "### Phase N - ... Findings"
    placeholder headings; exempting the real final phase UNMASKED it -> halt
    "Phase 2 missing...". A downstream/unmasking effect the #154 design +
    adversarial debate did not predict.
M4  *** THE THEATRE EXEMPLAR *** We made the parallel check advisory and fixed
    pipeline.gates.gate_passed (PR #155, eb9a2633) + "verified" it by calling
    gate_passed. But the PRD executor NEVER calls gate_passed — it uses its own
    evaluator PrdExecutor._evaluate_gate. The fix targeted an UNUSED code path
    and the verification exercised the SAME unused path -> false green; the run
    still halted. Real fix: PR #158 (_evaluate_gate advisory). A full
    design->spec->test->merge cycle that fixed nothing.
M5  _check_verdict_field (gates research-qa, synthesis-qa, structural-qa,
    sufficiency-review) rejected well-formed decorated verdicts
    ("## Verdict: PASS", "- **Verdict:** ✅ **PASS**") -> halt at research-qa.
    A brittle-parser CLASS fixed per-instance, never generalized; a prior
    "tightening" of the regex had over-corrected.
M6  Resume step-ID mismatch: execution log / internal step id is "research-qa"
    but 'prd resume' validates against "qa-research-gate" -> "Unrecognised
    resume step ID". Surfaced live; uncommitted.

REVIEW-STACK CONTEXT: each miss was preceded (for the active fix) by some of:
sc:troubleshoot diagnosis, task-builder MDTM build with multi-agent QA gates,
sc:reflect PRE (coverage) + POST (deviation) gates, and an adversarial debate.
None of these caught M2..M6 before runtime did. The recurring shapes:
  (a) the fix/verification reasons about the SYMPTOM in isolation, never
      against an end-to-end RUN of the real runtime path;
  (b) verification can target the artifact-under-design rather than the actual
      executed path (M4) — wrong-oracle / representational bias;
  (c) fixing gate X UNMASKS gate Y; no blast-radius/unmasking analysis (M3);
  (d) per-instance fixes never recognise the brittle-parser CLASS (M5);
  (e) gates downstream of the first failure are never EXERCISED, so a single
      run reveals bugs strictly one-at-a-time (whack-a-mole) (M2,M5,M6).
`.trim();

// ---------------------------------------------------------------------
// Schemas (force structured agent returns)
// ---------------------------------------------------------------------
const MISS_REGISTRY_SCHEMA = {
  type: "object",
  required: ["misses", "theatre_scorecard"],
  properties: {
    misses: {
      type: "array",
      items: {
        type: "object",
        required: ["id", "title", "root_cause", "fix_ref", "surfaced_by", "should_have_caught", "did_catch"],
        properties: {
          id: { type: "string" },
          title: { type: "string" },
          root_cause: { type: "string" },
          fix_ref: { type: "string", description: "commit/PR/branch" },
          surfaced_by: { type: "string", description: "what actually exposed it (e.g. runtime gate halt)" },
          should_have_caught: { type: "array", items: { type: "string" }, description: "review steps that plausibly should have caught it" },
          did_catch: { type: "array", items: { type: "string" }, description: "review steps that actually caught it pre-runtime (often empty)" },
          evidence: { type: "array", items: { type: "string" }, description: "file:line / commit / artifact citations" },
        },
      },
    },
    theatre_scorecard: {
      type: "array",
      description: "per review step: how many misses it should-have vs did catch",
      items: {
        type: "object",
        required: ["review_step", "should_have_caught", "did_catch", "theatre_ratio"],
        properties: {
          review_step: { type: "string", description: "sc:troubleshoot | task-builder | sc:reflect-PRE | sc:reflect-POST | adversarial" },
          should_have_caught: { type: "integer" },
          did_catch: { type: "integer" },
          theatre_ratio: { type: "number", description: "1 - did/should; 1.0 = pure theatre for this miss class" },
          notes: { type: "string" },
        },
      },
    },
  },
};

const HYPOTHESIS_SCHEMA = {
  type: "object",
  required: ["miss_id", "lens", "claim", "mechanism", "evidence", "falsifier"],
  properties: {
    miss_id: { type: "string" },
    lens: { type: "string", description: "the analytic lens this agent argued from" },
    claim: { type: "string", description: "one-sentence root-cause claim for why review missed it" },
    mechanism: { type: "string", description: "the causal mechanism, step by step" },
    evidence: { type: "array", items: { type: "string" } },
    falsifier: { type: "string", description: "what observation would disprove this" },
  },
};

const MERGED_CAUSE_SCHEMA = {
  type: "object",
  required: ["miss_id", "root_cause", "confidence", "loser_grafts", "rejected"],
  properties: {
    miss_id: { type: "string" },
    root_cause: { type: "string" },
    confidence: { type: "number" },
    loser_grafts: { type: "array", items: { type: "string" }, description: "valid points kept from the weaker hypothesis" },
    rejected: { type: "array", items: { type: "string" }, description: "claims dropped, with why" },
  },
};

const SYSTEMIC_SCHEMA = {
  type: "object",
  required: ["systemic_causes"],
  properties: {
    systemic_causes: {
      type: "array",
      items: {
        type: "object",
        required: ["id", "name", "statement", "covers_misses", "why_review_blind"],
        properties: {
          id: { type: "string" },
          name: { type: "string" },
          statement: { type: "string" },
          covers_misses: { type: "array", items: { type: "string" } },
          why_review_blind: { type: "string", description: "the structural reason the current pipeline cannot see this class" },
        },
      },
    },
  },
};

const REMEDIATION_SCHEMA = {
  type: "object",
  required: ["cause_id", "name", "principle", "mechanism", "generality_proof", "applies_to_misses", "cost"],
  properties: {
    cause_id: { type: "string" },
    name: { type: "string" },
    principle: { type: "string", description: "the ISSUE-AGNOSTIC principle (must NOT mention PRD/parallel/verdict specifics)" },
    mechanism: { type: "string", description: "how it is operationalised in any troubleshoot pipeline" },
    generality_proof: { type: "string", description: "argue it helps in >=2 unrelated systems, not just this one" },
    applies_to_misses: { type: "array", items: { type: "string" } },
    cost: { type: "string" },
  },
};

const REFACTOR_SCHEMA = {
  type: "object",
  required: ["summary", "changes", "would_have_caught"],
  properties: {
    summary: { type: "string" },
    changes: {
      type: "array",
      description: "concrete edits to sc:troubleshoot command/skill/protocol/agents",
      items: {
        type: "object",
        required: ["target", "change", "implements_remediation"],
        properties: {
          target: { type: "string", description: "file/section in the sc:troubleshoot surface" },
          change: { type: "string" },
          implements_remediation: { type: "string" },
        },
      },
    },
    would_have_caught: {
      type: "array",
      description: "for EACH known miss M1..Mn: which new mechanism catches it, and at which wave",
      items: {
        type: "object",
        required: ["miss_id", "caught", "mechanism", "wave"],
        properties: {
          miss_id: { type: "string" },
          caught: { type: "boolean" },
          mechanism: { type: "string" },
          wave: { type: "string" },
        },
      },
    },
  },
};

const REPLAY_SCHEMA = {
  type: "object",
  required: ["round", "caught", "missed", "coverage_pct", "gaps"],
  properties: {
    round: { type: "integer" },
    caught: { type: "array", items: { type: "string" } },
    missed: { type: "array", items: { type: "string" } },
    coverage_pct: { type: "number" },
    gaps: {
      type: "array",
      description: "for each missed miss: the mechanism gap to feed back into remediation",
      items: {
        type: "object",
        required: ["miss_id", "why_still_missed", "needed_mechanism"],
        properties: {
          miss_id: { type: "string" },
          why_still_missed: { type: "string" },
          needed_mechanism: { type: "string" },
        },
      },
    },
  },
};

// =====================================================================
// PHASE 1 — Forensic timeline + miss registry + theatre scorecard
// =====================================================================
phase("Forensic Timeline");
log("Phase 1 [run #2]: fanning out forensic readers (git, .dev artifacts, session seed).");

const READERS = [
  {
    label: "git-forensics",
    prompt: `You are a git forensic analyst in repo /config/workspace/IronClaude. Reconstruct the PRD-pipeline whack-a-mole timeline from git ONLY.
Run (read-only): \`git log --oneline -40 origin/master | grep -iE 'prd|--file|parallel|advisory|verdict|gate'\`, then \`git show --stat\` + \`git show\` for each PRD fix (#151 7601ad25, #154 e97aa4fd, #155 eb9a2633, and any #158 / verdict / resume commits). For EACH fix extract: the bug, the root cause, the diff, and — critically — whether the fix that FOLLOWED it was caused/unmasked by it. Map each commit to the GROUND_TRUTH miss ids where they correspond, and FLAG any bug present in git that the seed registry omitted.
GROUND TRUTH (verify, extend, do not blindly trust):\n${GROUND_TRUTH}`,
  },
  {
    label: "review-artifact-forensics",
    prompt: `You are a review-process forensic analyst in /config/workspace/IronClaude. Read the .dev artifacts that the review stack produced for the PRD fixes: \`.dev/troubleshoot/*\`, \`.dev/reflect/post-prd-*\`, \`.dev/specs/prd-*\`, and \`.dev/tasks/**\` related to prd-local-file / parallel-gate / advisory / verdict. For EACH known miss (M1..M6) determine which review steps RAN before the bug surfaced (sc:troubleshoot REPORT.md, task-builder MDTM + its QA gates, sc:reflect PRE coverage + POST deviation, adversarial debate) and what they CONCLUDED. The key question: did any of them flag the issue, or did they all sign off on work that runtime then rejected? Cite the artifact paths.
GROUND TRUTH:\n${GROUND_TRUTH}`,
  },
  {
    label: "session-live-forensics",
    prompt: `You are analysing the live debugging session that produced these fixes. From the GROUND_TRUTH registry below, characterise the issues that were caught LIVE (by running the pipeline) rather than by any review artifact — especially M4 (verification targeted the unused gate_passed path while the runtime uses _evaluate_gate) and M6 (resume step-ID mismatch). For each, state the exact moment/mechanism of discovery (a runtime halt, a functional check against the wrong path, a CLI error) and what review mechanism, had it existed, would have caught it pre-runtime. Do NOT read code you don't need; reason from the registry + cite the named symbols.
GROUND TRUTH:\n${GROUND_TRUTH}`,
  },
];

const readerFindings = await parallel(
  READERS.map((r) => () => agent(r.prompt, { label: r.label, phase: "Forensic Timeline" }))
);

const registry = await agent(
  `You are the forensic aggregator. Merge the three reader findings below into ONE canonical miss registry + a theatre scorecard.
For EACH miss: id, title, root_cause, fix_ref, what surfaced it, which review steps SHOULD have caught it, which DID (usually none pre-runtime), and evidence citations.
Then build the theatre_scorecard: for each review step (sc:troubleshoot, task-builder, sc:reflect-PRE, sc:reflect-POST, adversarial) compute should_have_caught vs did_catch across the misses, and a theatre_ratio (1 - did/should). This quantifies "theatre vs value".
Reconcile disagreements between readers; prefer git/artifact evidence over the seed when they conflict; keep any NEW miss a reader found.

READER FINDINGS:\n${readerFindings.filter(Boolean).map((f, i) => `\n--- ${READERS[i].label} ---\n${f}`).join("\n")}\n\nGROUND TRUTH SEED:\n${GROUND_TRUTH}`,
  { label: "aggregate-registry", phase: "Forensic Timeline", schema: MISS_REGISTRY_SCHEMA }
);

const misses = (registry && registry.misses) || [];
log(`Phase 1 done: ${misses.length} misses; theatre scorecard computed.`);

// =====================================================================
// PHASES 2-3 — per-miss: x2 hypotheses -> adversarial merge (no barrier)
// =====================================================================
phase("Hypotheses");

const LENSES = [
  "process-design lens: what STRUCTURAL property of the review pipeline (ordering, gating, oracle choice) made this invisible",
  "epistemics lens: what FALSE BELIEF/assumption the reviewers held (wrong-oracle, representational bias, 'the code looks right') and why it went unchallenged",
];

const mergedCauses = await pipeline(
  misses,
  (miss) =>
    parallel(
      LENSES.map((lens, i) => () =>
        agent(
          `Propose a root-cause hypothesis for WHY our review pipeline failed to catch this miss before runtime did. Argue strictly from the ${lens}.
MISS: ${JSON.stringify(miss)}
Be concrete and falsifiable. This is about the REVIEW PROCESS failure, not the code bug itself.`,
          { label: `hyp:${miss.id}:${i === 0 ? "process" : "epistemic"}`, phase: "Hypotheses", schema: HYPOTHESIS_SCHEMA }
        )
      )
    ),
  (hyps, miss) =>
    agent(
      `Run an adversarial Mode-A merge over these TWO competing root-cause hypotheses for review-miss ${miss.id}.
Steelman BOTH before critiquing. Score each on: evidence strength, mechanism completeness, falsifiability, and generality (does it explain OTHER misses too). Then MERGE into the single strongest validated root cause, grafting any valid point from the weaker one and recording what you rejected and why.
MISS: ${JSON.stringify(miss)}
HYPOTHESES: ${JSON.stringify((hyps || []).filter(Boolean))}`,
      { label: `merge:${miss.id}`, phase: "Adversarial Merge (per miss)", schema: MERGED_CAUSE_SCHEMA }
    )
);

const causesClean = (mergedCauses || []).filter(Boolean);
log(`Phases 2-3 done: ${causesClean.length} per-miss validated root causes.`);

// =====================================================================
// PHASE 4 — systemic synthesis (barrier: needs ALL per-miss causes)
// =====================================================================
phase("Systemic Synthesis");
const systemic = await agent(
  `Synthesise the per-miss validated root causes into the FEW systemic causes (aim 2-4) that explain the whole episode — the structural reasons the debug/task/reflect pipeline is theatre for this class. For each: id, name, one-paragraph statement, which misses it covers, and the precise structural reason the current pipeline is blind to it.
PER-MISS ROOT CAUSES: ${JSON.stringify(causesClean)}
THEATRE SCORECARD: ${JSON.stringify((registry && registry.theatre_scorecard) || [])}`,
  { label: "systemic-synthesis", phase: "Systemic Synthesis", schema: SYSTEMIC_SCHEMA }
);
const causes = (systemic && systemic.systemic_causes) || [];
log(`Phase 4 done: ${causes.length} systemic causes.`);

// =====================================================================
// PHASE 5 — per systemic cause: x2 GENERALIZED remediations -> adversarial merge
// =====================================================================
phase("Generalized Remediation");
const remediationStrategies = await pipeline(
  causes,
  (cause) =>
    parallel(
      [
        `mechanism-first: a concrete, GENERIC pipeline mechanism (a new wave/gate/oracle) that structurally prevents this cause in ANY troubleshooting context`,
        `incentive/contract-first: a GENERIC discipline/contract (what evidence a fix must produce before it can pass) that makes this cause impossible to sign off on, in ANY system`,
      ].map((angle, i) => () =>
        agent(
          `Propose ONE issue-agnostic remediation for this systemic cause, from the ${angle}.
HARD CONSTRAINT: the remediation must be GENERALIZED — it must NOT reference PRD, --file, parallel-instructions, verdict, or any specifics of this episode. State it as a principle + mechanism that would help in unrelated systems. Then show it still resolves THIS cause's misses.
SYSTEMIC CAUSE: ${JSON.stringify(cause)}`,
          { label: `rem:${cause.id}:${i}`, phase: "Generalized Remediation", schema: REMEDIATION_SCHEMA }
        )
      )
    ),
  (rems, cause) =>
    agent(
      `Adversarial Mode-A merge of these TWO generalized remediations for systemic cause ${cause.id}. Steelman both; score on: structural-prevention strength, generality (helps >=2 unrelated systems), cost, and false-positive risk; MERGE into the single strongest issue-agnostic remediation, grafting the best of the loser. Re-assert the no-specifics constraint in the merged output.
CAUSE: ${JSON.stringify(cause)}
REMEDIATIONS: ${JSON.stringify((rems || []).filter(Boolean))}`,
      { label: `rem-merge:${cause.id}`, phase: "Generalized Remediation", schema: REMEDIATION_SCHEMA }
    )
);
const strategy = (remediationStrategies || []).filter(Boolean);
log(`Phase 5 done: ${strategy.length} merged generalized remediation strategies.`);

// =====================================================================
// PHASE 6 — sc:troubleshoot-ONLY refactor + would-have-caught matrix
// =====================================================================
phase("Troubleshoot Refactor");
const refactor = await agent(
  `Produce a CONCRETE refactor of the sc:troubleshoot surface ONLY (the command file, the sc:troubleshoot-protocol skill, its waves, and its agents — do NOT refactor task-builder or reflect) that embodies the merged generalized remediations. Read the current surface under /config/workspace/IronClaude/src/superclaude/{commands,skills,agents} for sc:troubleshoot before proposing edits, so changes cite real sections.
Then build the would_have_caught matrix: for EVERY known miss (M1..Mn from the registry), state whether the refactored pipeline catches it, BY WHICH new mechanism, and at WHICH wave. A remediation that leaves any miss uncaught is incomplete — note it.
MERGED REMEDIATIONS: ${JSON.stringify(strategy)}
MISS REGISTRY: ${JSON.stringify(misses)}`,
  { label: "troubleshoot-refactor", phase: "Troubleshoot Refactor", schema: REFACTOR_SCHEMA }
);
log(`Phase 6 done: ${(refactor && refactor.changes || []).length} refactor changes; would-have-caught matrix built.`);

// =====================================================================
// PHASE 7 — rollback replay validation loop (MAX 3 rounds)
// =====================================================================
phase("Rollback Replay");
log(`Phase 7: replay vs ground truth at ${ROLLBACK_COMMIT} (max 3 rounds); worktree ${WORKTREE}.`);

let currentRefactor = refactor;
let lastReplay = null;
for (let round = 1; round <= 3; round++) {
  lastReplay = await agent(
    `ROLLBACK-REPLAY round ${round}. A git worktree of /config/workspace/IronClaude at commit ${ROLLBACK_COMMIT} represents the PRD pipeline BEFORE any whack-a-mole fix (it still contains the original M1..Mn defects). Set it up read-only if not present: \`git -C /config/workspace/IronClaude worktree add ${WORKTREE} ${ROLLBACK_COMMIT}\` (skip if it exists).
Now SIMULATE running the REFACTORED sc:troubleshoot pipeline (below) against that code state, starting ONLY from the first symptom ("headless prd run --spec halts at scope-discovery: Session token required"). For EACH known miss M1..Mn, decide: would the refactored pipeline's new mechanisms have SURFACED it in this single pass (before runtime), and at which wave? Be adversarial and honest — a mechanism only "catches" a miss if you can name the concrete artifact/check that would have flagged it. Verify your reasoning against the actual code in the worktree where needed.
Output caught[], missed[], coverage_pct, and for each missed miss the gap + the needed mechanism.
REFACTORED PIPELINE: ${JSON.stringify(currentRefactor)}
GROUND-TRUTH MISSES: ${JSON.stringify(misses)}`,
    { label: `replay:r${round}`, phase: "Rollback Replay", schema: REPLAY_SCHEMA }
  );
  log(`  round ${round}: coverage ${Math.round((lastReplay && lastReplay.coverage_pct || 0) * 100)}% (missed: ${(lastReplay && lastReplay.missed || []).join(", ") || "none"}).`);
  if (lastReplay && (lastReplay.missed || []).length === 0) break;
  if (round === 3) break;
  currentRefactor = await agent(
    `Round ${round} replay still missed: ${JSON.stringify(lastReplay.gaps)}. Propose the ADDITIONAL generalized sc:troubleshoot mechanism(s) that close these gaps (still issue-agnostic), and emit an UPDATED refactor (same schema) that now catches them while keeping prior coverage. Cite the sc:troubleshoot sections changed.
PRIOR REFACTOR: ${JSON.stringify(currentRefactor)}
MISS REGISTRY: ${JSON.stringify(misses)}`,
    { label: `refine:r${round}`, phase: "Rollback Replay", schema: REFACTOR_SCHEMA }
  );
}

// =====================================================================
// FINAL — efficacy report (written into the -2 isolated directory)
// =====================================================================
const report = await agent(
  `Write the final efficacy report (markdown) to /config/workspace/IronClaude/.dev/troubleshoot/meta-efficacy-pipeline-2/EFFICACY-REPORT.md. Sections:
1) Executive verdict: how much of the debug/task/reflect stack was theatre vs net value (use the theatre scorecard, with numbers).
2) The miss timeline (M1..Mn) and per-miss validated root cause.
3) The 2-4 systemic causes.
4) The merged GENERALIZED remediation strategy (issue-agnostic).
5) The sc:troubleshoot refactor + the would-have-caught matrix.
6) Rollback-replay result: final coverage %, which misses (if any) still slip after <=3 rounds, and the residual-gap analysis.
7) A blunt bottom line: would the refactored troubleshoot pipeline have caught ALL of M1..Mn in one shot at ${ROLLBACK_COMMIT}? If not, what is irreducibly un-catchable by static troubleshooting alone (and therefore needs a runtime/exercise mechanism).
INPUTS: registry=${JSON.stringify(registry)} ; systemic=${JSON.stringify(systemic)} ; strategy=${JSON.stringify(strategy)} ; finalRefactor=${JSON.stringify(currentRefactor)} ; finalReplay=${JSON.stringify(lastReplay)}`,
  { label: "efficacy-report", phase: "Rollback Replay" }
);

return {
  misses: misses.length,
  systemic_causes: causes.length,
  remediations: strategy.length,
  final_coverage_pct: lastReplay && lastReplay.coverage_pct,
  still_missed: (lastReplay && lastReplay.missed) || [],
  report,
};
