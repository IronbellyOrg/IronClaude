# Rubric pass 2 (reverse order: V3, V2, V1)

Scope: the ORIGINAL option cards only (variant-1/2/3-original.md), not the Round 1 advocates' proposed merges. Source facts: `context.md` and `../M-major-versions/context.md`. Orchestrator evidence used: `src/superclaude/cli/install_codegraph.py` lines 328-330 check a download only against the pinned `SHA256` table, so whatever hashes a merged pin carries are the only check at install time.

Source requirements used for Comp1: (a) class 1 integrity failures, (b) class 2 behaviour failures, (c) never put or merge unverified bytes, (d) a person gets a next action, (e) idempotency across daily runs, (f) testable number of code paths, (g) class 3 infrastructure case.

Scoring: MET = 1, NOT MET = 0, no partial credit. Every MET quotes the variant.

## Variant 3 (Option C: split by failure class)

| Dimension | Criterion | Verdict | Evidence |
|---|---|---|---|
| Completeness | 1 covers all requirements | NOT MET | Covers (a) "Integrity failure ... issue only", (b) "Behaviour failure ... DRAFT PR", (c) "never put unverified hashes on a branch", (d) "so a person can push a fix", (f) "three paths to test", (g) "Infrastructure failure: neutral exit". Requirement (e) is missing: no rule for the next daily run when the issue or draft PR already exists (diff C-004). |
| Completeness | 2 edge cases and failure scenarios | MET | All three failure classes are handled, including the transient case: "Infrastructure failure: neutral exit with a step summary and `::warning::`, no issue (retries next schedule)". |
| Completeness | 3 dependencies and prerequisites | NOT MET | Uses "labelled `needs-codegraph-proof`", which does not exist in IronClaude (`context.md`), and never says the label is created or which token permissions each path needs. |
| Completeness | 4 success or completion criteria | NOT MET | No statement of when a failure artifact is resolved or closed (diff A-004). |
| Completeness | 5 out of scope | NOT MET | No out-of-scope statement. |
| Correctness | 1 no factual errors | MET | "neutral exit with a step summary ... as Coder does" matches `context.md` ("exits neutral with a step summary when the upstream API is unreachable"). No claim is contradicted. |
| Correctness | 2 feasible | MET | Each path uses capabilities the context confirms: Actions may create PRs (`context.md`), issues reach the owner. The missing label is a one-time setup, not a blocker. |
| Correctness | 3 terminology consistent | MET | "Integrity failure", "Behaviour failure", "Infrastructure failure" map one to one onto context classes 1, 2, 3 and are used the same way throughout. |
| Correctness | 4 no internal contradictions | MET | Rule "issue only, no branch" for integrity agrees with the rationale "keeps unverified bytes off branches". |
| Correctness | 5 claims supported by rationale | MET | "(possible tampering; never put unverified hashes on a branch)" and "so a person can push a fix (for example an `MCP_TOOLS` or entry change) onto it". |
| Structure | 1 logical ordering | MET | Bullets run integrity, behaviour, infrastructure, then rationale, then cost. |
| Structure | 2 consistent hierarchy | MET | One heading, flat bullets, each class one bullet. |
| Structure | 3 separation of concerns | MET | One bullet per failure class; rationale and cost are separate bullets. |
| Structure | 4 navigation aids or cross-references | NOT MET | No reference to `context.md`, the class numbers, or the code file; "as Coder does" names a source without pointing to it. |
| Structure | 5 option card conventions | MET | Rule bullets, then "Rationale:", then "Cost:". |
| Clarity | 1 unambiguous language | NOT MET | The integrity and infrastructure triggers overlap: "hash mismatch or attestation failure" versus "GitHub API or download unavailable". A truncated download gives a hash mismatch and `gh attestation verify` fails when the API is down, so the same event fits both rules (diff X-003). Draft PR title is also not given. |
| Clarity | 2 concrete actions | MET | "push the branch and open a DRAFT PR labelled `needs-codegraph-proof` with the failed stage and log tail". |
| Clarity | 3 each part has a clear purpose | MET | Each bullet names a class and its artifact; rationale and cost each state one point. |
| Clarity | 4 terms as in context | MET | "install, index, tools/list, drift" repeats the class 2 list in `context.md`. |
| Clarity | 5 actionable next steps | MET | "so a person can push a fix (for example an `MCP_TOOLS` or entry change) onto it". |
| Risk coverage | 1 at least 3 risks | NOT MET | Two risks named: "possible tampering" and "three paths to test". |
| Risk coverage | 2 mitigation per risk | NOT MET | Tampering is mitigated ("issue only, no branch"); the test-burden cost has no mitigation. |
| Risk coverage | 3 failure modes and recovery | MET | Recovery stated per path: "retries next schedule" (infra) and "a person can push a fix ... onto it" (behaviour). |
| Risk coverage | 4 external dependency failure | MET | "Infrastructure failure: ... GitHub API or download unavailable" is handled explicitly (stated in context, handled by "neutral exit"). |
| Risk coverage | 5 monitoring or detection | NOT MET | The infra path relies on "a step summary and `::warning::`", and `context.md` says "Nobody watches IronClaude Actions run summaries". The card names no notification for the other paths. |
| Invariants and edge cases | 1 collection boundaries | NOT MET | Nothing on zero versus an already open issue or draft PR. |
| Invariants and edge cases | 2 state across runs | NOT MET | "retries next schedule" is stateless; no rule for existing branch, PR or issue on the next run (diff C-004, A-002). |
| Invariants and edge cases | 3 guard condition gaps | NOT MET | The integrity versus infrastructure guard gap (X-003) is not identified or closed. |
| Invariants and edge cases | 4 count divergence | NOT MET | No handling of artifact count drifting from failure count (for example a new draft PR per daily run). |
| Invariants and edge cases | 5 interaction effects between paths | NOT MET | No rule for a version that fails integrity one day and behaviour the next, or for an infra failure inside the attestation step. |

## Variant 2 (Option B: issue only)

| Dimension | Criterion | Verdict | Evidence |
|---|---|---|---|
| Completeness | 1 covers all requirements | NOT MET | Covers (a) and (b) by one issue path, (c) "No branch, no PR", (d) "the commands to reproduce locally", (e) "idempotently by title", (f) one path. Requirement (g), class 3 infrastructure, is not addressed (diff C-003). |
| Completeness | 2 edge cases and failure scenarios | MET | Handles the repeat-run edge case: "Open (or comment on, idempotently by title) one issue", and carries the failing "stage" in the title. |
| Completeness | 3 dependencies and prerequisites | NOT MET | No mention of the `issues: write` permission or other prerequisites. |
| Completeness | 4 success or completion criteria | NOT MET | No rule for closing the issue when a later run passes (diff A-004). |
| Completeness | 5 out of scope | NOT MET | No out-of-scope statement. |
| Correctness | 1 no factual errors | MET | "issues notify the owner" matches `context.md` ("issue and PR notifications reach the owner"). |
| Correctness | 2 feasible | MET | Opening or commenting on an issue needs only standard workflow permissions; no new label is required. |
| Correctness | 3 terminology consistent | MET | "stage", "proof log tail", "run URL" are used consistently. |
| Correctness | 4 no internal contradictions | MET | Rule "No branch, no PR" agrees with the rationale "nothing mergeable is ever created". |
| Correctness | 5 claims supported by rationale | MET | "nothing mergeable is ever created from failed or unverified bytes; issues notify the owner". |
| Structure | 1 logical ordering | MET | Rule, then "Rationale:", then "Cost:". |
| Structure | 2 consistent hierarchy | MET | One heading, three flat bullets. |
| Structure | 3 separation of concerns | MET | Rule, rationale and cost are separate bullets. |
| Structure | 4 navigation aids or cross-references | NOT MET | No reference to context, class numbers, or code. |
| Structure | 5 option card conventions | MET | Rule bullet, "Rationale:", "Cost:". |
| Clarity | 1 unambiguous language | MET | The title is fully specified: "codegraph vX.Y.Z bump failed: <stage>", and the dedup key is named ("by title"). |
| Clarity | 2 concrete actions | MET | "Open (or comment on ...) one issue ... with the run URL, the stage, the proof log tail and the commands to reproduce locally". |
| Clarity | 3 each part has a clear purpose | MET | Each bullet states one thing: rule, why, cost. |
| Clarity | 4 terms as in context | MET | "proof", "stage" used as in `context.md`. |
| Clarity | 5 actionable next steps | MET | "the commands to reproduce locally"; cost line "they must re-run the script by hand". |
| Risk coverage | 1 at least 3 risks | NOT MET | One risk named: "the reviewer has no diff to inspect or push fixes onto". |
| Risk coverage | 2 mitigation per risk | NOT MET | The no-diff risk is not mitigated; reproduce commands only cover the re-run half. |
| Risk coverage | 3 failure modes and recovery | MET | Failure is reported by stage and recovery is stated: "commands to reproduce locally", "re-run the script by hand". |
| Risk coverage | 4 external dependency failure | NOT MET | GitHub API or download unavailability is not mentioned. |
| Risk coverage | 5 monitoring or detection | MET | "issues notify the owner", which `context.md` confirms reaches the owner. |
| Invariants and edge cases | 1 collection boundaries | MET | "Open (or comment on, idempotently by title) one issue" covers the zero-existing and one-existing cases. |
| Invariants and edge cases | 2 state across runs | MET | "idempotently by title": a later run comments on the existing issue instead of opening another. |
| Invariants and edge cases | 3 guard condition gaps | NOT MET | The title includes "<stage>", so the same version failing at a different stage opens a second issue; the card does not note this gap. |
| Invariants and edge cases | 4 count divergence | NOT MET | No handling of a newer release superseding an older open issue (diff A-003). |
| Invariants and edge cases | 5 interaction effects between paths | NOT MET | Single path; interaction with the PASS path (closing the issue) or with infra failures is not stated. |

## Variant 1 (Option A: draft PR with a label)

| Dimension | Criterion | Verdict | Evidence |
|---|---|---|---|
| Completeness | 1 covers all requirements | NOT MET | Covers (a) "Integrity failures (class 1) are treated the same way", (b) draft PR, (d) partly, (f) one path. Fails (c): its own cost says it "pushes a branch whose pin points at unverified bytes". No (e) idempotency, no (g) infrastructure. |
| Completeness | 2 edge cases and failure scenarios | NOT MET | Names classes 1 and 2 only; no edge cases (repeat runs, infra, existing PR). |
| Completeness | 3 dependencies and prerequisites | NOT MET | Uses label `needs-codegraph-proof`, which does not exist (`context.md`), with no step to create it and no permissions listed. |
| Completeness | 4 success or completion criteria | NOT MET | No rule for when the draft is made ready, closed or replaced. |
| Completeness | 5 out of scope | NOT MET | No out-of-scope statement. |
| Correctness | 1 no factual errors | MET | "draft cannot be merged; proven in Coder" matches `context.md` (Coder opens a DRAFT PR, "the only hard non-mergeable state available"). The cost line agrees with the installer evidence: lines 328-330 trust the pinned table, so unverified pin hashes would be trusted at install. |
| Correctness | 2 feasible | MET | The Coder monitor already runs this pattern (`context.md`); creating the label is a one-time step. |
| Correctness | 3 terminology consistent | MET | "class 1" and "proof log" match `context.md`. |
| Correctness | 4 no internal contradictions | MET | Rationale "draft cannot be merged" and cost "pushes a branch whose pin points at unverified bytes" are a stated trade-off, not a contradiction. |
| Correctness | 5 claims supported by rationale | MET | "one artifact holds the diff and the evidence; draft cannot be merged; proven in Coder". |
| Structure | 1 logical ordering | MET | Rule, integrity note, "Rationale:", "Cost:". |
| Structure | 2 consistent hierarchy | MET | One heading, flat bullets. |
| Structure | 3 separation of concerns | MET | Rule, class 1 handling, rationale and cost are separate bullets. |
| Structure | 4 navigation aids or cross-references | NOT MET | "(the Coder pattern)" names a source but gives no pointer to it, to `context.md`, or to code. |
| Structure | 5 option card conventions | MET | Rule bullets, "Rationale:", "Cost:". |
| Clarity | 1 unambiguous language | NOT MET | The title is elided: "titled \"... [proof failed]\"", so the actual title is not defined. |
| Clarity | 2 concrete actions | MET | "Push the bump branch, open a DRAFT PR ... with label `needs-codegraph-proof`, the failed stage and the tail of the proof log in the body". |
| Clarity | 3 each part has a clear purpose | MET | Each bullet states one thing. |
| Clarity | 4 terms as in context | MET | "Integrity failures (class 1)" uses the context numbering. |
| Clarity | 5 actionable next steps | NOT MET | The body carries evidence (stage, log tail) but the card states no action for the person. |
| Risk coverage | 1 at least 3 risks | NOT MET | Two risks named in the cost line: unverified bytes on a branch ("possible tampering") and "the draft looks like routine work in the PR list". |
| Risk coverage | 2 mitigation per risk | NOT MET | Neither named risk is mitigated; both are accepted as cost. |
| Risk coverage | 3 failure modes and recovery | NOT MET | No recovery step is stated for either failure class. |
| Risk coverage | 4 external dependency failure | NOT MET | Infrastructure unavailability is not mentioned. |
| Risk coverage | 5 monitoring or detection | NOT MET | No notification is stated, and the card itself says "the draft looks like routine work in the PR list". |
| Invariants and edge cases | 1 collection boundaries | NOT MET | Nothing on an already open draft PR or branch. |
| Invariants and edge cases | 2 state across runs | NOT MET | No rule for re-pushing the branch on the next daily run (diff A-002). |
| Invariants and edge cases | 3 guard condition gaps | NOT MET | No guards stated. |
| Invariants and edge cases | 4 count divergence | NOT MET | No handling of duplicate draft PRs across runs or versions. |
| Invariants and edge cases | 5 interaction effects between paths | NOT MET | Classes 1 and 2 are merged; no interaction with PASS or infra paths. |

## Summary

| Dimension | V3 (C) | V2 (B) | V1 (A) |
|---|---|---|---|
| Completeness | 1 | 1 | 0 |
| Correctness | 5 | 5 | 5 |
| Structure | 4 | 4 | 4 |
| Clarity | 4 | 5 | 3 |
| Risk coverage | 2 | 2 | 0 |
| Invariants and edge cases | 0 | 2 | 0 |
| Total (out of 30) | 16 | 19 | 12 |

MET criteria:

- V3 (C): Comp2, Corr1, Corr2, Corr3, Corr4, Corr5, Str1, Str2, Str3, Str5, Clar2, Clar3, Clar4, Clar5, Risk3, Risk4
- V2 (B): Comp2, Corr1, Corr2, Corr3, Corr4, Corr5, Str1, Str2, Str3, Str5, Clar1, Clar2, Clar3, Clar4, Clar5, Risk3, Risk5, Inv1, Inv2
- V1 (A): Corr1, Corr2, Corr3, Corr4, Corr5, Str1, Str2, Str3, Str5, Clar2, Clar3, Clar4
