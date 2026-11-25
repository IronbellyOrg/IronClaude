06ccf7288c46958c354806c28c54ed8695f301fe
Review one task for spec compliance.

Task brief: Update the run artifact reference and user guidance

Depends on: Task 3

Update only the completion-related passages in `docs/swarm/README.md` (opening summary, What a run emits table/count and resume note), `docs/swarm/command-reference.md` (Run artifacts table and fresh/resume publication text), and `docs/swarm/user-guide.md` (Pattern C completion caveat and No done.json troubleshooting row). Derive the replacement claims from Tasks 1-3 evidence and the real `run_cmd` / `_run_resume_branch` behavior, not from historical release prose. The existing quickstart absence test in `tests/swarm/test_e2e_user_guide.py` is replaced by Task 1; use its actual new name if linking to it.


Acceptance criteria:
T4.AC1: These three documents describe enabled default marker publication after persisted contract and terminal state for completed foreground and resumed reduction, and child-owned publication for detached execution. They explain explicit opt-out and preserve the separate killed result; no unconditional only-kill or inline-never statements remain in the affected sections.
T4.AC2: The artifact table includes the existing three marker fields and explains that terminal_status is the actual success/partial/failed result, not a guarantee that all workers succeeded. Update the documented default stub output count from observed Task 1 artifacts, not a guessed number.
T4.AC3: Scope qualifiers are truthful: early errors/no completed reduction do not imply a new completion marker; effective resume policy is used, with original runtime override recovery not guaranteed. No claim of full detached runtime verification is made when Task 3 recorded a skip.
T4.AC4: Run `uv run pytest tests/swarm/test_e2e_user_guide.py` against the updated docs/test contract and record the result and a targeted completion-claim search across these three files in `./artifacts/reference-doc-check.txt`. Existing related links resolve, and no unrelated setup, transport, metadata or stdout documentation is rewritten.
Global constraints: - Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.
Current-conversation instruction from the user at 2026-11-23T20:53:20Z: "go ahead and include the launcher change and finish the fix". This explicitly supersedes only the restriction excluding the detached launcher output-directory handoff in commands.py. It is not acceptance of missing behavior. The pinned plan and source remain unchanged; all original AC and other exclusions still apply.
Start sha: 06ccf7288c46958c354806c28c54ed8695f301fe
Diff against the start snapshot: diff --git a/docs/swarm/README.md b/docs/swarm/README.md
index 0f091c271..19cf00bf0 100644
--- a/docs/swarm/README.md
+++ b/docs/swarm/README.md
@@ -9,7 +9,9 @@ the CLI substrate behind the multi-model review/troubleshoot/spec workflows.
 > preflight → Wave 1 dispatch → Wave 2 normalize → Wave 3 reduce**. Besides the
 > observability files it writes the per-worker outputs, `merged.md` (in the
 > `normalize+merge` mode every bundled lens uses) and `return-contract.yaml`. The
-> `done.json` sentinel is written only by `swarm kill <job_id> --output <dir>`. See
+> `done.json` completion marker is then written after the result contract and terminal
+> state when `runtime.on_completion.write_done_sentinel` is enabled (the default).
+> Detached children, not their launchers, publish completion. See
 > [What a run emits](#what-a-run-emits).
 
 ---
@@ -109,19 +111,32 @@ contains:
 | `merged.md` | All worker outputs merged (Wave 3; written when `amalgamation_mode` is `normalize+merge`, the default for every bundled lens) | same |
 | `return-contract.yaml` | Run status (`success` / `partial` / `failed`), worker counts, output paths, recommended next command | same |
 
-A stub `bare-review` run, for example, leaves 12 entries: the four observability files,
-three `bare-review-0N-lens-default-model-0.final.md` + `.meta.json` pairs, `merged.md`
-and `return-contract.yaml`.
+| `done.json` | Atomic completion marker: `atomic_write: true`, `terminal_status` matching the actual result (`success` / `partial` / `failed`), and `contract_path` pointing to the absolute persisted contract path | same |
 
-**Not** emitted by a run: `done.json`. Only `swarm kill <job_id> --output <dir>` writes
-it (with `terminal_status=killed`). (A missing proxy env contract fails the run at
+A default stub `bare-review` run, for example, leaves 13 entries: the four observability
+files, three `bare-review-0N-lens-default-model-0.final.md` + `.meta.json` pairs,
+`merged.md`, `return-contract.yaml` and `done.json`.
+
+**Completion policy.** Foreground and resumed runs publish `done.json` after the
+contract and terminal state are persisted; detached children use the same completion
+path. Setting `runtime.on_completion.write_done_sentinel=false` suppresses the marker,
+not the contract or terminal state. A marker means completion, not that every worker
+succeeded. Early errors, no completed reduction, or a persistence exception do not
+produce a new completion marker. Use a fresh output directory per job so an old marker
+cannot be mistaken for this job's completion.
+
+`swarm kill <job_id> --output <dir>` keeps its separate `terminal_status=killed`
+marker with an empty `contract_path`. (A missing proxy env contract fails the run at
 transport construction with a clear `missing: …` diagnostic and exit `1`, writing only
 `manifest.json` + `.swarm-state.json` — see
 [User Guide §6c](user-guide.md#6c-if-the-env-is-missing).)
 
 > **Resume mode.** `swarm run --resume` skips succeeded workers, re-dispatches the rest,
 > re-runs Wave 2 normalize on them and Wave 3 reduce (`reduce_wave3(resume=True)`),
-> regenerating `merged.md` and `return-contract.yaml`. See
+> regenerating `merged.md` and `return-contract.yaml`, then publishing the marker
+> when the effective rehydrated completion policy enables it. Arbitrary original
+> runtime overrides are not fully restored from the manifest, so an original opt-out
+> is not guaranteed to survive resume. See
 > [User Guide §8](user-guide.md#8-resuming-a-partial-job) and
 > [Command Ref → run artifacts](command-reference.md#run-artifacts).
 
diff --git a/docs/swarm/command-reference.md b/docs/swarm/command-reference.md
index 851973973..49c78114e 100644
--- a/docs/swarm/command-reference.md
+++ b/docs/swarm/command-reference.md
@@ -250,8 +250,8 @@ missing, nested tmux, illegal `JOB_ID`, or `--output` not a directory).
 ## Run artifacts
 
 After a successful **fresh** `swarm run … --output <DIR>` (stub or proxy), `<DIR>`
-contains the four observability files, the per-worker outputs, `merged.md` and
-`return-contract.yaml`:
+contains the four observability files, the per-worker outputs, `merged.md`,
+`return-contract.yaml` and, with the default completion policy, `done.json`:
 
 | File | Format | Key fields |
 |---|---|---|
@@ -264,13 +264,25 @@ contains the four observability files, the per-worker outputs, `merged.md` and
 | `merged.md` | Markdown | Wave 3 merge of the worker outputs; written when `amalgamation_mode` is `normalize+merge` (the default for every bundled lens). |
 | `return-contract.yaml` | YAML | `status` (`success`/`partial`/`failed`), `job_id`, `lens`, `workers_requested` / `workers_succeeded` / `workers_failed`, `output_files` (per-worker paths), recommended next command. |
 
-**Not** emitted by a run: `done.json`. Only [`swarm kill JOB_ID --output DIR`](#swarm-kill)
-writes it (with `terminal_status=killed`). Preflight also writes `return-contract.yaml`
-(`status: failed`, `reason: env-missing`) on the INV-007 env-missing path.
+| `done.json` | JSON | Exactly `atomic_write` (`true`), `terminal_status` (the actual contract's `success` / `partial` / `failed` result), and `contract_path` (absolute persisted contract path). Completion does not guarantee all workers succeeded. |
+
+**Completion ordering and policy.** Foreground runs persist the contract, then terminal
+state, then atomically publish `done.json`. Detached launchers only start the child;
+the child owns those writes. `runtime.on_completion.write_done_sentinel` defaults to
+`true`; explicit `false` suppresses only the completion marker. Early errors, absent
+completed reduction, and failed contract or terminal-state persistence do not produce
+a new marker. Use a fresh per-job output directory to avoid reading an old marker.
+[`swarm kill JOB_ID --output DIR`](#swarm-kill) retains its separate
+`terminal_status=killed` marker with an empty `contract_path`. Preflight also writes
+`return-contract.yaml` (`status: failed`, `reason: env-missing`) on the INV-007
+env-missing path; a failure contract alone is not a completion marker.
 
 **`--resume`** re-dispatches only the workers that did not succeed, re-runs Wave 2
 normalize on them and Wave 3 reduce (`reduce_wave3(resume=True)`), regenerating
-`merged.md` and `return-contract.yaml`.
+`merged.md` and `return-contract.yaml`, then persists terminal state and publishes
+`done.json` when the effective rehydrated policy enables it. Arbitrary original
+runtime overrides are not fully restored from the manifest; do not assume an
+original completion opt-out survives resume.
 
 Full schemas: [Lens Catalog](lens-catalog.md) and the dataclass definitions in
 `cli/swarm/models.py`.
diff --git a/docs/swarm/user-guide.md b/docs/swarm/user-guide.md
index 600b503c9..21c2fbf19 100644
--- a/docs/swarm/user-guide.md
+++ b/docs/swarm/user-guide.md
@@ -404,11 +404,17 @@ re-binds your terminal, `kill <job_id>` tears it down. tmux is **optional** —
 never need it, and `--detached` without tmux exits `2` with a clear error rather than
 silently falling back.
 
-> **Caveat — `done.json`:** a run does **not** write the `done.json` sentinel; only
-> `swarm kill <job_id> --output <dir>` writes it. The `until [ -f done.json ]` poll in
-> [Monitoring Patterns](monitoring-patterns.md) therefore only fires for killed jobs.
-> Poll `.swarm-state.json` reaching `terminal` via `status` instead: the state flips to
-> `terminal` only after `merged.md` and `return-contract.yaml` are on disk.
+> **Completion marker:** the detached child, not the launcher, writes `done.json`
+> after the result contract and terminal state are persisted. Foreground and resumed
+> runs also publish it when their effective `runtime.on_completion.write_done_sentinel`
+> policy is enabled (the default). Explicit `false` suppresses the marker; arbitrary
+> original runtime overrides, including opt-out, are not guaranteed to survive resume.
+> The marker contains `atomic_write: true`, the actual `success` / `partial` / `failed`
+> result in `terminal_status`, and the absolute `contract_path`. Completion is not
+> necessarily success. `swarm kill <job_id> --output <dir>` keeps its separate `killed`
+> marker with an empty contract path. Use a fresh per-job output directory and see
+> [Monitoring Patterns](monitoring-patterns.md) for polling. Early errors or no completed
+> reduction do not produce a new marker; inspect state and contract when opting out.
 
 ---
 
@@ -521,7 +527,7 @@ only** — no scoring, deduping, or reordering (AC-011).
 | `run` exits 0 but no files on disk | Spec-file mode without the `--output` **flag**. | Always pass `--output <dir>`; the flag (not `spec.output.dir`) wires artifacts. |
 | `cannot construct 'openai_compat' transport … incomplete; missing: …` (exit 1) | `openai_compat` with `T2ProxyUrl` / `T2ProxyKey` / `T2Model0*` slots unset. | Export the [env contract](#6a-set-the-env-contract); the `missing:` list names exactly what's absent. |
 | `--detached` exits 2 | tmux not installed / nested in tmux. | Install tmux, or run inline (no `--detached`). |
-| No `done.json` after a normal run | Expected — only `swarm kill <job_id> --output <dir>` writes it. | Poll `swarm status` for `phase=terminal` (§7); see [README](README.md#what-a-run-emits). |
+| No `done.json` after a run | Completion policy disabled, no durable output, or execution failed before reduction and terminal-state persistence completed. | Check effective `runtime.on_completion.write_done_sentinel`, the output directory, `.swarm-state.json` and `return-contract.yaml`; an enabled completed reduction should publish a marker. See [README](README.md#what-a-run-emits). |
 | `VIRTUAL_ENV … will be ignored` warning | Benign uv/venv notice. | Ignore, or filter with `grep -v VIRTUAL_ENV`. |
 
 See also the [Command Reference](command-reference.md) for per-command exit-code tables
Codegraph context
index_state: fresh
checked_at: 2026-11-23T20:14:00Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
call codegraph only when index_state: fresh, never to widen scope
Dependents outside this diff: CLI registration; resume continuation; detached child; unchanged writer and kill callers; existing TUI/input/status tests. Source call sites were Read in implementation context. These are context, not extra requirements.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
