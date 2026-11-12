899d63c1792e090ec3f76d4691057618edb155d6
Review one task for spec compliance.

Task brief: ## Task 3: Implement cluster_v2 (path-aware, with the chained guard)

Depends on: Task 1

Create `src/superclaude/cli/review/cluster.py` and `tests/review/test_review_cluster.py`. Implement the pure function `cluster_v2(reviewer_records, snapshot_file_list) -> clusters`, where a reviewer record is `(reviewer_id, ordinal, findings_v2_block, calibration_map)` and `calibration_map` is `{finding_id: finding_confidence}` (possibly empty), exactly as "Multi-file identity (K4 cluster_v2)": citation tuple `(role, path, line_start, line_end)` verified against the snapshot file list (a path not in the list is `unresolved` and never joins a cluster by span); primary citation rule; `same_defect_v2` (deviation classes compatible, `refs_norm` sets intersect or both empty using the normalization of `findings.py:321-337`, and some citation of each on the same path with spans within 3 lines; equal `sha256("v2|"+role+"|"+path+"|"+section+"|"+refs+"|"+class)` fingerprints with non-empty refs also match; for a citation-only finding `section` is the empty string, pinned by a test); union-find components with `chained: true` for any cluster holding two members that do not match pairwise. Implement `cluster_agreement` and the `disputed` flag per "`cluster_agreement` and clustering semantics": support from calibrated confidences joined from `calibration.per_finding[id].finding_confidence` (a finding with no calibration entry has no support value, and its cluster is listed as `uncalibrated`), representative claim from the highest-confidence member (ties by resolution order), `chained` clusters excluded from agreement counts and listed, and a second pass `clusters_kept` over findings the evidence validator kept. Do not import or alter `findings.cluster`.

Acceptance criteria:
- Tests (positive and negative): two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines with equal refs cluster; a chain A-B-C with A and C unequal is `chained`; an unresolved path never clusters by span.
- A test proves `review merge` output on v1 reports is byte-identical with and without importing the new module.
- `cluster_agreement` is 1.0 when there are no blocking clusters and at least 2 valid blocks; it is `null` when fewer than 2 valid blocks exist; the field is named `cluster_agreement` everywhere and `panel_agreement_score` appears nowhere.


AC ids (T3.ACk in source order):
T3.AC1: Tests (positive and negative): two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines with equal refs cluster; a chain A-B-C with A and C unequal is `chained`; an unresolved path never clusters by span.
T3.AC2: A test proves `review merge` output on v1 reports is byte-identical with and without importing the new module.
T3.AC3: `cluster_agreement` is 1.0 when there are no blocking clusters and at least 2 valid blocks; it is `null` when fewer than 2 valid blocks exist; the field is named `cluster_agreement` everywhere and `panel_agreement_score` appears nowhere.

Global constraints: - Requirement text lives in `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (sha256 recorded in `./source.md`). Section names below refer to that file. Items it marks PROPOSED are new names to create; items it marks UNVERIFIED must be checked in code before relying on them.
- Return contract stays `1.8.0` with no new stable field and no new legal value (`merge_method` stays `adversarial` or `single-reviewer-fallback`). Panel data lives only in `<out>/panel/*` and the non-stable telemetry block.
- The `/sc:adversarial` debate stays authoritative in pre-execution. K4 clustering, the citation pre-check and the findings block never drop a citation, never feed the debate and never route anything.
- Default behavior of every existing command is unchanged: with no new flag, `superclaude review panel resolve`, `review merge`, `review ledger` and the spec-panel loop produce byte-identical output.
- Plan decision: in Stage 2 the flag accepts only `legacy` and `shadow`; the value `panel` is rejected with a plain message saying it ships in Stage 3. The post-execution path, the swarm lens, `--panel-resolution` and the headless `citations_dropped` change are Stage 5 and are not touched.
- Plan decision: the prose coordinator of the reflect skill cannot import Python, so the manifest gets a minimal `superclaude review manifest` CLI (init, advance, validate) instead of hand-written JSON.
- Edit installed primitives only under `src/superclaude/` and run `make sync-dev` afterwards. Never edit or add files under `.claude/` by hand. Installed primitives reference other primitives by installed path or the `superclaude` CLI, never by a `src/superclaude/...` path.
- All Python runs through `uv run`. Fable and Tier 0 never appear in a new template and are rejected by validation. Opus appears only in the uses the source's "Opus uses" section lists (third reviewer of the parity templates (pre and post) and of the enterprise template, backfill in the x2 templates when the executor class is removed, calibrator); no new Opus use is added.
- Human-supplied inputs are not fabricated: the 50-pair cluster labels (Task 5) and the 20 real shadow runs (Task 20) are produced by the owner and by normal use after merge. The tasks deliver the sheets, scorers and aggregators that judge them.
- Plan decision: Stage 1 and Stage 2 code is built dormant (default `legacy`, nothing enabled) before the Stage 0 exit is met. Task 7 records the Stage 0 exit as PENDING until the owner's labelled sheet is scored, and this plan does not claim the Stage 1 entry or the Stage 2 exit. Merging or enabling later stages stays the owner's decision.
- Task-owned evidence goes under `./artifacts/` in this package.
Start sha: 899d63c1792e090ec3f76d4691057618edb155d6
Diff against the start snapshot: Full unified diff against the start snapshot saved at /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T3-diff-2-1.patch ; read it in full. Touched files: src/superclaude/cli/review/cluster.py tests/review/test_review_cluster.py
Delta diff from the previous reviewed tree (empty on the first review): Delta diff from the previous reviewed tree saved at /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T3-delta-2-1.patch (context beside the full diff)
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/cli/review/cluster.py:330 anchor=Implement `cluster_agreement` and the `disputed` flag per "`cluster_agreement` and clustering semantics" chk=n,n,n,y family=support-denominator fix=divide support by the sum the source names (merged-requirements.md:347), or record the count-of-reviewers reading as a plan decision and test it covers=merged-requirements.md:347 first=A1 origin=new: support(c) divides by the number of complete reviewers while the source section divides by the sum of calibrated confidences of all complete reviewers; this changes support, disputed and cluster_agreement whenever confidences are below 1
Saved-probe re-check hit locations (may be empty): support-denominator family hits after the fix:
13:  finite number from 0 to 1 (not a bool); a finding with no usable entry has no support value.
39:- support(c) = sum, over the distinct reviewers in c, of the highest calibrated confidence of that reviewer's members
40:  in c, divided by the sum of w(r) over all complete reviewers. support is at most 1, and is 1 when c holds, for every
42:- support is None, and the cluster is listed in uncalibrated, when a member has no calibrated confidence. When a
44:  denominator is unknown: every cluster has support None and is listed in uncalibrated.
48:- disputed: support below 0.5, or members disagree on blocking, or members carry two different non-null
51:  mean support over blocking clusters that are not chained and have a support value, or None when no such cluster
333:            best[m["reviewer_id"]] = max(
337:    support = None if uncalibrated else sum(best[r] for r in reviewers) / total
348:        (support is not None and support < 0.5)
372:        "support": support,
404:    counted = [c for c in blocking if not c["chained"] and c["support"] is not None]
411:            sum(c["support"] for c in counted) / len(counted) if counted else None

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
