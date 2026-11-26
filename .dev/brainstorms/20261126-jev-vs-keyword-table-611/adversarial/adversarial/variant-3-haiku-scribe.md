---
type: spec
status: draft; live execution blocked pending owner inputs
---

# Jev versus the keyword table: research requirements

## Purpose and scope

Determine whether Jev, pinned to `jev-1.14.0`, clearly improves problem-type selection over the corrected troubleshooting keyword table sufficiently to justify building issue 612. The experiment compares both arms on the same approximately 30 public prompts, with human labels frozen before either arm runs.

The six types are `bug`, `build`, `performance`, `deployment`, `security`, and `test`. Ambiguous and none-fit cases must also be represented. This is a research comparison, not a production classifier, command, hook, gateway rewrite, depth comparison, scope comparison, or table improvement. No private repository material is permitted. No changes under `src/` are permitted.

The lead has already approved sending approximately 30 public prompts to TypeSafe using the `TYPESAFE_API_KEY` environment variable, with a total spend cap of 1 dollar. That approval does not supply the two outstanding decision thresholds or release the run gate. This document authorizes no live calls during specification drafting.

## Functional requirements

**FR-001 — Corpus and provenance.** Before either arm runs, create a corpus with stable prompt identifiers, exact submitted text, public source references, and a recorded public-only review. Record its exact size and coverage of all six types, ambiguous cases, and none-fit cases. Explain any departure from approximately 30 prompts. A prompt without verifiable public provenance must be excluded before freezing.

**FR-002 — Human labels.** A named human labeler must assign every reference label before seeing either arm’s output. Record the labeling instructions, allowed labels, treatment of ambiguity and none-fit cases, labeler identity, and rationale for difficult cases. Resolve the reference-label scheme before freezing; no unresolved label may enter the comparison.

**FR-003 — Freeze evidence.** Before running either arm, record a dated freeze manifest identifying the corpus, labels, question file, table reference, and scoring/decision rule by content digest. Include who approved the freeze. Later verification must demonstrate that the same bytes were used. A changed frozen input invalidates that run’s eligibility for the planned decision; it must not silently replace the original.

**FR-004 — Baseline fidelity.** Apply the corrected prose keyword table as written, including structural cues and its rule to leave the type unset when unclear. Preserve the deliberate appearance of “leak” under both performance and security. Do not substitute first-match parsing or an improved classifier. Pin the baseline revision to `37765a800d0b232cc231cf58b796fec23b26f8a8` and table blob to `76bcb3d94182371250ffe99a7b60b9124b05c368`. Record the chosen application method and enough execution evidence to audit each table answer.

**FR-005 — Jev contract.** Use only `jev-1.14.0`. For each prompt, make one request containing a Choice over the six types and a companion Noul question asking whether any type fits. Keep all question wording in one frozen file. Values strictly between 0.3 and 0.7 leave the type unset. Exact-boundary behavior at 0.3 and 0.7 must be resolved in the frozen rule, not improvised during execution. Validate service details at authorized execution time without assuming they are already verified.

**FR-006 — Failures are distinct.** Preserve failed calls, malformed responses, and timeouts as errors, never as “no,” none-fit, or ordinary abstentions. Before the run, document their scoring treatment, timing treatment, and any retry policy. A retry must remain separately identifiable and count toward the spend cap; it must not erase the failed attempt.

**FR-007 — Paired records.** Produce one comparison record per frozen prompt, linked by identifier to its reference label, table answer, Jev answer, returned probability/Noul value, latency, call status, and attributed cost or explicitly marked cost uncertainty. Distinguish a returned candidate from the final answer after the Noul rule. Use explicit statuses for unset, error, and not attempted rather than ambiguous blanks.

**FR-008 — Recomputable summary.** Report accuracy and abstention rate for each arm, paid cost, median and slowest Jev latency, and all disagreements. State denominators, units, exclusions, error counts, and completion counts. Define the metrics before execution, including how an unset answer matches an ambiguous or none-fit reference. Mark local table cost and timing separately from remote-call measurements; do not imply unmeasured latency is zero.

**FR-009 — Chronological audit trail.** Record dated events for owner input receipt, corpus/label freeze, decision-rule freeze, gate approval, first live request, run completion or stop, scoring, and verdict. Link each event to its evidence. The first-request event must reference the exact pre-run manifest, allowing a reader to establish ordering without trusting a later narrative alone.

**FR-010 — Decision and issue record.** Derive the verdict from the frozen rule without post-result threshold changes. Record the comparison, rationale, limitations, and evidence links on issues 611 and 609; update issue 612 to build or close as not justified when the evidence supports the planned decision. An incomplete or invalid run must instead be recorded as inconclusive, with no unsupported build/close claim. Preserve the text and resulting issue references in the experiment record.

## Non-functional requirements

- **Cost cap:** Total experiment spend must stay at or below 1 dollar, including failed attempts and retries. Before each paid request, verify that incurred spend plus reserved outstanding liability plus a defensible upper bound for that request fits within the cap. If pricing, limits, or remaining liability cannot be bounded, stop before sending. The quoted approximate per-call cost is not a verified spending safeguard.
- **Privacy:** Transmit only frozen, reviewed public prompt text and required fixed questions. Do not send private repository context, credentials, personal additions, or unrelated local files. Public availability alone does not excuse including a secret found in a public source; reject such material.
- **Key secrecy:** The eventual live runner may obtain the key only from `TYPESAFE_API_KEY`. Never print, persist, copy into artifacts, or include it in command arguments, logs, errors, issue text, or request dumps. Record only a credential-availability status. Offline tests must not read the real environment or key.
- **Reproducibility:** Preserve exact inputs, baseline identifiers, question wording, service/model identifier, execution method, relevant settings, metric definitions, scoring implementation version, and timestamps. Reproduction means independently recomputing the report from saved non-secret evidence; it does not promise identical future service responses or require another paid run.

## Run gate and decision rule

Two required owner inputs remain **PENDING**:

1. The margin Jev must win by, including whether it is a prompt count or share.
2. The acceptable median latency, including its unit.

The lead must type both owner-provided inputs into the terminal. Before the first live call, preserve each input **word for word**, with receipt time and attribution, in the pre-run record. Keep the original wording alongside any machine-readable interpretation. An absent, ambiguous, unitless, or contradictory input blocks the gate; seek clarification rather than choosing a value. No suggested, inferred, or default number is permitted for either input.

Before either arm runs, freeze an executable or unambiguous written decision rule specifying the accuracy comparison, margin calculation, inequality/equality behavior, latency calculation and comparison, missing/error treatment, and validity conditions. Record why these definitions answer the build decision. The rule must require both the owner’s winning margin and acceptable median latency to be satisfied for a “clearly beats” verdict.

No comparison or live call may begin until the two verbatim inputs, their confirmed interpretation, the frozen labels, and the complete rule exist. Before the first live request, verify their digests, chronological ordering, public-only review, model pin, and budget safeguard. Persist a pass/fail gate result. Failure means zero live requests. Approval already given for public prompts and the budget must not bypass this check.

After results exist, do not revise labels, thresholds, or scoring to obtain a preferred verdict. Document discovered defects and invalidate the affected decision; any replacement experiment needs a separate pre-run record and renewed budget accounting.

## Artifacts and where they live under .dev/

Choose and record one experiment directory under `.dev/` before freezing; its final name remains open. It must contain:

- Corpus, provenance, labeling instructions, reference labels, and difficult-case rationales.
- One question file and the baseline application-method record.
- Pre-run owner quotations, normalized interpretation, decision rule, and freeze manifest.
- Gate result and chronological event log.
- Non-secret per-attempt evidence, paired results, cost accounting, and stop reasons.
- Aggregate report, disagreement list, verdict rationale, and issue-update references.
- Any offline scoring code, fixtures, and verification results required for recomputation.

Separate pre-run evidence from observed results. Retain originals and identify amendments rather than overwriting them. These are required future run artifacts, not claims that measurements already exist.

## Test obligations (offline, no live API)

Use synthetic fixtures and a fake transport only. Tests must make no network requests, use no live credentials, and incur no spend. Verify:

- Missing either owner input, unclear units, missing freeze evidence, or changed frozen bytes blocks every attempted live request.
- Verbatim owner wording survives recording unchanged, and event ordering exposes a late freeze.
- All six types, ambiguity, none-fit, interior Noul values, and both exact boundaries follow the frozen policy.
- Errors remain distinct from negative answers and abstentions; retries remain visible.
- Known paired fixtures yield exact accuracy, abstention, disagreement, median, and maximum calculations.
- Cost reservations stop before exceeding the cap, including failed calls and uncertain liability.
- Synthetic credential markers do not reach files, logs, errors, or summaries.

## Risks and mitigations

A small corpus can make a narrow advantage unstable: publish counts and disagreements and limit conclusions to the measured sample. Label leakage or changed thresholds can manufacture success: preserve pre-run digests and event ordering. Human baseline interpretation can drift: freeze the method and retain per-prompt rationale. Service failures can distort accuracy or latency: predefine treatment and expose completion status. Uncertain billing can breach the cap: refuse unbounded requests. Existing table tests do not establish Jev accuracy or latency: keep those claims unverified until measured.

## Open questions

- Owner’s winning margin and acceptable median latency: both PENDING; no values proposed.
- Who labels, how prompts are selected, and which reference labels represent ambiguous/none-fit cases?
- How are exact Noul boundaries and failed calls scored?
- Is the baseline applied by a person or by the actual troubleshooting procedure?
- Is live execution scripted or manual, and how will it enforce the same gate and cost controls?
- What is the final experiment directory under `.dev/`?
