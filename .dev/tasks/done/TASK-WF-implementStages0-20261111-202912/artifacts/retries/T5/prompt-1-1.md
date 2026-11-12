de3e1017f3520a2e09a01240b6e43423dcdd693a
Review one task for spec compliance.

Task brief: ## Task 5: Produce the 50-pair cluster check sheet and its scorer

Depends on: Task 2, Task 3

Create `scripts/reflect_cluster_pairs.py` and `tests/review/test_reflect_cluster_pairs.py`. The script samples 50 finding pairs from the converted recorded cards (25 that `cluster_v2` merges, 25 it keeps apart, drawn with a fixed seed, mixing same-file and cross-file pairs; sample min(25, available) per side, write the shortfall in the sheet header, and report fewer than 50 rows as INSUFFICIENT PAIRS, never as a pass), writes `./artifacts/cluster-pairs-50.csv` with blank `human_same_defect` column, and has a `score` mode that reads the filled sheet and reports precision, recall and the confusion counts of `cluster_v2` against the labels.

Acceptance criteria:
- `./artifacts/cluster-pairs-50.csv` exists with exactly 50 rows when 25 merged and 25 separate pairs are available (otherwise the shortfall rule of the description applies), each carrying both claims, both citations and the `cluster_v2` verdict; the label column is empty for the owner.
- A unit test fills a synthetic sheet and checks the score output; scoring an unfilled sheet fails with a message naming the missing labels.


AC ids (T5.ACk in source order):
T5.AC1: `./artifacts/cluster-pairs-50.csv` exists with exactly 50 rows when 25 merged and 25 separate pairs are available (otherwise the shortfall rule of the description applies), each carrying both claims, both citations and the `cluster_v2` verdict; the label column is empty for the owner.
T5.AC2: A unit test fills a synthetic sheet and checks the score output; scoring an unfilled sheet fails with a message naming the missing labels.

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
Start sha: de3e1017f3520a2e09a01240b6e43423dcdd693a
Diff against the start snapshot: Full unified diff against the start snapshot saved at /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T5-diff-1-1.patch ; read it in full. Touched files: scripts/reflect_cluster_pairs.py tests/review/test_reflect_cluster_pairs.py .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/cluster-pairs-50.csv
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
