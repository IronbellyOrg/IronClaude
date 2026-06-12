# Why-it-escaped hypothesis card: E5-Reflect-post-diff-wrong-base

## Lens

Verification-artifact / off-path-review lens.

## Escape summary

The escape was not that `/sc:reflect` was absent. The verification artifact existed, but its audited surface could diverge from the work surface. Generated POST-reflect items used a commit range rooted at `start_commit` (`/sc:reflect --mode post --diff <start_commit>..HEAD`). In the common `/task` execution mode, task work remains uncommitted, so that commit range can exclude the actual working-tree changes. If unrelated commits land after task start, the same range can include foreign work instead.

## Independent hypothesis

E5 escaped review because the review system treated POST-reflect as an assurance artifact whose mere presence and PASS result were meaningful, while failing to make the artifact prove its own effective diff. The off-path review was wired into task-builder/sc:tasklist and had documented dogfood evidence, but the verification packet did not require a blocking invariant of the form: “the audited diff contains the task files changed by this task and excludes unrelated commits.”

As a result, reviewers saw high-ceremony evidence: PRE/POST reflect wiring, task frontmatter, reports, deviation ledgers, QA passes, and later self-run reflect behavior. Those artifacts demonstrated that a review path existed, not that the path was reviewing the same files an operator had just changed under `/task` runtime semantics.

## Evidence chain

1. The defect table records the precise escape: the generated POST-reflect item used `/sc:reflect --mode post --diff <start_commit>..HEAD`; this missed uncommitted task work and could include unrelated commits. It also states that the wiring in #138/#144 missed actual `/task` runtime semantics and that the correct catching pipeline should have edited the working tree without committing, then verified the effective diff contained task files and excluded foreign commits. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `REFLECT-E01-wrong-diff`.

2. The PR #153 summary shows the live failure mode was not hypothetical. While auditing the PRD `--file` fix, `start_commit` pointed before an unrelated sprint-recovery commit and the PRD work was uncommitted on top, so the requested range covered only the foreign commit. The reflect run had to be manually retargeted to the working-tree diff. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` section `# 153`.

3. The timeline places the correction after the escape was observed: PR #153 changed POST-reflect to use a merge-base working-tree diff after the wrong-base behavior was found while auditing #151. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` PR #153 entry.

4. The pipeline artifact audit identifies the meta-level false-audit risk: post-reflect corrected the diff target from `ac80f176..HEAD` to the actual working-tree PRD diff, preventing another false audit. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` runtime-entrypoint verification section.

5. The review-value artifacts show why the escape could survive despite apparent rigor. The `sc:reflect` review says reflect delivered value but depended on whether it corrected its own scope before auditing; it also says the initial wiring had an empty supplied diff and recommended a later commit-range rerun, which became the same class of E5 failure. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/stage-value-sc-reflect.md`.

6. The task-builder review explains the upstream verification-artifact failure: #144 had four independent QA PASSes and documented the POST-reflect self-run adaptation, but those passes did not prevent the wrong-diff escape. It characterizes the stage as strong at routing/auditability but weak at proving runtime-entrypoint correctness. Evidence: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/stage-value-task-builder.md`.

## Why review missed it

- **Artifact-presence substitution:** Reviewers accepted “POST-reflect is wired and has a report/deviation ledger” as evidence of independent review, without requiring the report to demonstrate that its `effective-diff.patch` covered the actual task work.
- **Commit-centric mental model:** The generated command assumed completed work would be represented by commits between `start_commit` and `HEAD`. The `/task` runtime commonly leaves work uncommitted, so the proof model did not match the operator workflow.
- **Off-path review blindness:** The review was executor-disjoint in name, but not necessarily work-surface-disjoint. It could inspect a real diff that was nevertheless the wrong diff.
- **QA pass masking:** PR #144’s carry-forward evidence and multiple QA passes validated schema/template consistency and intended self-run behavior, but not the diff/base invariant that would make the self-run review meaningful.
- **Missing negative fixture:** There was no dogfood e2e where the task deliberately changed files in the working tree without committing while an unrelated commit existed or could be simulated. That fixture would have made a `<start_commit>..HEAD` review visibly empty or contaminated.

## Root cause hypothesis

The root cause was a verification contract gap: POST-reflect was specified as a review step, but not as an evidence-producing step with a mandatory effective-diff proof. The process verified that review machinery existed; it did not verify that the machinery’s selected diff matched `/task` runtime state.

## Counterfactual catch

A dogfood task-builder/self-run POST-reflect e2e would likely have caught this before escape if it required all of the following:

1. make task changes only in the working tree;
2. leave those changes uncommitted;
3. include or simulate an unrelated commit after task start;
4. run the generated POST-reflect item exactly as emitted;
5. assert the effective audited diff includes the task files;
6. assert the effective audited diff excludes the unrelated commit.

The absence of that fixture allowed a review artifact to pass while auditing either no relevant work or the wrong work.

## Confidence

High. The artifact set independently agrees on the same failure pattern: the wrong diff base was documented in the defect table, observed live in the PR #153 summary, placed on the timeline as the remediation trigger, and characterized by stage-value reviews as an off-path review/proof-scope failure rather than a missing-reflect-wiring failure.
