9112df4145d87444127a53ac4a5f44312d9f835a
Review one task for spec compliance.

Task brief: ## Task 19: Write the shadow-mode steps, brief line and telemetry into the reflect skill

Depends on: Task 12, Task 13, Task 18

Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`. Under the new T2 engine subsection add the "Pre-execution adapter" steps 3-9 and 11-12 for `--t2-engine shadow` as given in "Adapter sketches" and the "Shadow mode" paragraph: freeze via `superclaude review manifest init` (passing the requested and effective engine); resolve with `superclaude review panel resolve --template @reflect-pre ... --hard-exclude-class <executor class> --strict-distinct` (re-resolve with `@reflect-pre-x2` on `ExclusionExhausted` of the anchor, record `anchor_replaced`), compare the legacy rotation with the resolution and record `panel_parity: true|false` (`panel/resolution.json` is the unmodified output of `review panel resolve`, never rewritten to match the legacy rotation; parity means equal ordered `(persona, model class)` lists of that resolution, with ids mapped through the tier file's `classes`, and of the legacy rotation as run; every shadow reviewer card header carries `persona:`, `model_class:` and `model:` (the resolved id), so `scripts/reflect_shadow_exit.py` recomputes parity from the card headers and `panel/resolution.json` and does not trust the recorded boolean; when parity is false the legacy rotation still runs, the value is recorded and nothing is blocked), with executor-unknown keeping the fail-open path and `executor_class_resolved: false`; add to the brief, only when the effective engine is `shadow` (a legacy run's briefs are unchanged), inside the `## T1 card excerpt` section of `refs/reviewer-spec.md` and not as a fourth section (amend the sentence that calls that excerpt verbatim so it allows this one instruction line), the one line instructing each reviewer to end its card with a `## Findings block` fenced `findings-v2` block (`lens: reflect-pre`, citations with roles plan and spec) and a `reviewer_model_self_report` line; normalize cards with one bounded re-ask of the block only, copying each returned `## Findings block` with its calibration block into `<out>/panel/cards/reviewer-N.md` (the legacy card files and the legacy Wave 4 call stay unchanged; `review cluster` and `review verify-citations` read that directory); run `superclaude review cluster` and `superclaude review verify-citations` as telemetry and flagging (flagged citations join the evidence-validator re-read set, the validator alone decides drops); after the validator, write its kept finding ids to `<out>/panel/kept-ids.txt` and run `superclaude review cluster --kept` for the `clusters_kept` pass; read the installed `sc-adversarial-protocol` return contract to find whether it names a judge; if it does not, record `judge_identity: unknown` and `judge_class_collision: unknown` (never `false`); when a judge id is known, assert it is not Fable or Tier 0 and note a class collision in `<out>/panel/notes.md`; apply the same Fable and Tier 0 filter to the calibrator pick; record `debate_skipped_similar` after the debate; record `identity_source` from Task 14 and compare each `reviewer_model_self_report` with the pin: a mismatch sets `identity_mismatch_suspected: true` in the telemetry and in `panel/notes.md`, and while the identity is requested-pinned or the executor is unknown the panel notes make no claim of verified independence. Call `superclaude review manifest advance` after each step (resolved, dispatched, collected, calibrated, clustered), after the legacy debate (debated), after the evidence validator (validated) and after the legacy writers finish (published). State that the legacy debate, calibration, evidence gate and contract builder are authoritative and unchanged, and that panel artifacts go to `<out>/panel/`. Add the non-stable telemetry fields (`t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `cluster_agreement`, `panel_parity`, `anchor_replaced`, `judge_identity`, `manifest_path`, the three reviewer counts, the Stage 2 counts of 2-of-3 shortfalls and of `executor_class_resolved: false`, and the findings-block compliance rate) to section 9.2 only; leave section 9.1 and the contract version untouched. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- Section 9.1 and `contract_version: 1.8.0` are byte-identical to before; a diff of the skill shows additions only in the flag line, section 4.3a, section 5.4, section 9.2 and `refs/reviewer-spec.md`, measured against the commit before Task 18.
- The brief template still has exactly three sections.
- A shadow reviewer card header carries `persona:`, `model_class:` and `model:`, and `panel/resolution.json` equals the raw output of `review panel resolve` (checked on a fixture run directory).
- `grep -rn 'src/superclaude' src/superclaude/skills/sc-reflect-protocol` shows no hit that was not there before.
- `uv run pytest tests/skills tests/cli/reflect tests/review -q` and `make verify-sync` pass.


AC ids (T19.ACk in source order):
T19.AC1: Section 9.1 and `contract_version: 1.8.0` are byte-identical to before; a diff of the skill shows additions only in the flag line, section 4.3a, section 5.4, section 9.2 and `refs/reviewer-spec.md`, measured against the commit before Task 18.
T19.AC2: The brief template still has exactly three sections.
T19.AC3: A shadow reviewer card header carries `persona:`, `model_class:` and `model:`, and `panel/resolution.json` equals the raw output of `review panel resolve` (checked on a fixture run directory).
T19.AC4: `grep -rn 'src/superclaude' src/superclaude/skills/sc-reflect-protocol` shows no hit that was not there before.
T19.AC5: `uv run pytest tests/skills tests/cli/reflect tests/review -q` and `make verify-sync` pass.

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
Start sha: 9112df4145d87444127a53ac4a5f44312d9f835a
Diff against the start snapshot: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T19-diff-2-1.patch
Delta diff from the previous reviewed tree (empty on the first review): .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/diffs/T19-delta-2-1.patch
Earlier blocking findings of this start (empty on the first review): F1.1 resolved advance lacked --payload; F1.2 collected attempts were recorded before dispatched was advanced; F1.3 findings block copied to panel/cards before calibration
Saved-probe re-check hit locations (may be empty): F1.1, F1.2, F1.3: confirm each fixed in section 4.3a and by the literal-recipe test; confirm t2_floor_unmet in 9.2 is consistent with rule D3

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
