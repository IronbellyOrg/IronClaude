0f6bc94ef61d927be950167aa9e21f8393183afb
Review one task for spec compliance.

Task brief: ## Task 17: Add the panel manifest module and CLI

Depends on: Task 11

Create `src/superclaude/cli/review/manifest.py`, `src/superclaude/cli/review/manifest_cmd.py` (command `manifest` with `init`, `advance`, `validate`, registered in `__init__.py`) and `tests/review/test_review_manifest.py` per "Execution contract (both adapters)". The manifest `<out>/panel/manifest.json` carries states `frozen`, `resolved`, `dispatched`, `collected`, `calibrated`, `clustered`, `debated`, `validated`, `published` and terminal `failed`; `frozen` records the reference to `artifacts/input-snapshot.yaml` with `input_tree_sha256`, template, tiers and brief-template sha256, schema ids, `run_id`, `t2_engine_requested` and `t2_engine_effective` (`init` takes both values); each later state records the hashes of its outputs. Idempotency identity is `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`: the same payload hash is a no-op, a different payload under the same identity is rejected, a new attempt supersedes a failed one without adding a vote. Record the counts `reviewers_requested`, `reviewers_resolved`, `reviewers_complete` as top-level manifest keys, and per-attempt completion states. Resume reuses a stage only when dependency hashes match. Publish writes REPORT.md, return-contract.yaml and audit.log to same-directory temporaries, renames them, then commits `published`. In shadow mode the legacy writers stay authoritative for those three files: `advance published` records their hashes after the legacy writers finish and does not rewrite them, and every state from `frozen` to `published` is advanced in order with none skipped.

Acceptance criteria:
- Tests: replaying an identical `advance` is a no-op; a conflicting payload is rejected; an out-of-order state is rejected; a changed plan hash on resume starts a new invocation; a crash between rename and commit leaves a manifest that readers refuse (no `published`).
- A manifest initialised with requested engine `shadow` and effective engine `shadow` carries both values, and `validate` fails when either is missing.
- `superclaude review manifest --help` lists the three subcommands.


AC ids (T17.ACk in source order):
T17.AC1: Tests: replaying an identical `advance` is a no-op; a conflicting payload is rejected; an out-of-order state is rejected; a changed plan hash on resume starts a new invocation; a crash between rename and commit leaves a manifest that readers refuse (no `published`).
T17.AC2: A manifest initialised with requested engine `shadow` and effective engine `shadow` carries both values, and `validate` fails when either is missing.
T17.AC3: `superclaude review manifest --help` lists the three subcommands.

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
Start sha: 0f6bc94ef61d927be950167aa9e21f8393183afb
Diff against the start snapshot: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T17-diff-2-1.patch
Delta diff from the previous reviewed tree (empty on the first review): .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T17-delta-2-1.patch
Earlier blocking findings of this start (empty on the first review): F1.1 publish_files renamed files before checking the manifest state (and did not refuse shadow); F1.2 init ignored --run-id and engine values on an existing manifest; F1.3 (minor) fail() overwrote the reason
Saved-probe re-check hit locations (may be empty): F1.1 and F1.2: confirm fixed with tests (publish refuses before touching any file; init refuses another run id and starts a new invocation on a changed engine). F1.3: fail keeps the first reason.

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
