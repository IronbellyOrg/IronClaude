56f171c140f4a92de9d2342f644276d8438e8920
Review one task for spec compliance.

Task brief: Align monitoring and operator guidance with the repaired behavior

Depends on: Task 4

Update only completion-related guidance in `docs/swarm/monitoring-patterns.md` (implementation warning and Pattern 1 scope), `docs/swarm/observability-procedure.md` (marker introduction/table, Layer 4, triage, absence explanations and affected verdict-reading recipes/use-case map), and `docs/swarm/operator-runbook.md` (resume artifact comparison). Align these passages with the reference docs from Task 4 and the actual marker behavior from Tasks 1-3. Preserve unrelated diagnostic recipes, command examples and kill semantics; correct inline-absence comments and the old negative-test citation only where this fix invalidates them.


Acceptance criteria:
T5.AC1: Polling guidance supports completed foreground/resume/detached-child jobs with effective marker policy enabled and fresh per-job output directories; it does not promise marker appearance for opt-out or failures before reduction/terminal persistence. State/contract inspection remains available when publication is disabled. Do not introduce a new polling feature or broadly redesign the runbook.
T5.AC2: Observability guidance no longer describes default inline marker absence as expected or restricts marker verdict reading to detached/resumed jobs. It retains the distinction between terminal completion and success, and between a result contract path and the killed marker's empty path.
T5.AC3: The operator-runbook no longer says resume uniquely adds artifacts now also emitted on a fresh completed reduction. The existing limitation on arbitrary original resume runtime overrides is stated consistently with Tasks 2 and 4, without changing persistence behavior.
T5.AC4: A targeted search across all six updated completion documents finds no remaining only-kill/default-inline-never claim or citation to `test_quickstart_does_not_emit_done_sentinel`; inspect hits in context, do not blindly replace matches. Retain search results and link checks in `./artifacts/monitoring-doc-check.txt`.
T5.AC5: Run `uv run pytest tests/swarm/test_e2e_user_guide.py tests/swarm/test_tmux_fallback.py` and save results in `./artifacts/monitoring-doc-check.txt`. The documentation's marker field names, status values, policy conditions and ordering agree with the parsed CLI evidence already captured; no new diagnosis is needed.
Global constraints: - Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.
Current-conversation instruction from the user at 2026-11-23T20:53:20Z: "go ahead and include the launcher change and finish the fix". This explicitly supersedes only the restriction excluding the detached launcher output-directory handoff in commands.py. It is not acceptance of missing behavior. The pinned plan and source remain unchanged; all original AC and other exclusions still apply.
Start sha: 56f171c140f4a92de9d2342f644276d8438e8920
Diff against the start snapshot: diff --git a/docs/swarm/monitoring-patterns.md b/docs/swarm/monitoring-patterns.md
index e6d281ac8..16450cc45 100644
--- a/docs/swarm/monitoring-patterns.md
+++ b/docs/swarm/monitoring-patterns.md
@@ -3,12 +3,13 @@
 > 📚 Part of the [swarm documentation](./README.md). New here? Start with the
 > [User Guide](./user-guide.md).
 >
-> ⚠️ **Implementation status.** Wave 3 reduce now runs on a fresh `swarm run`
-> (it writes `return-contract.yaml` before the state flips to `terminal`), but
-> `done.json` is still written only by `swarm kill --output`. Pattern 1 below
-> therefore never sees the sentinel on a normal run. Watch `.swarm-state.json`
-> instead, with Pattern 3 (`swarm status --watch`, which exits once the phase
-> reaches `terminal`).
+> **Completion scope.** Foreground runs, resumed runs and detached children publish
+> `done.json` after the result contract and terminal state are persisted when their
+> effective `runtime.on_completion.write_done_sentinel` policy is enabled (the default).
+> Explicit `false`, early errors, no completed reduction or persistence failure can
+> leave no new marker. In those cases inspect `.swarm-state.json`, the contract and
+> logs rather than waiting indefinitely. Use a fresh output directory per job;
+> a marker left from an earlier attempt does not prove a resumed attempt finished.
 
 Three durable monitoring patterns are supported against any running
 swarm job. All three read the **caller-agnostic** observability artifacts
@@ -36,9 +37,19 @@ criteria (three monitoring patterns demonstrated).
 
 Use when the caller needs to **block until the job finishes** (success,
 partial, failed, or killed) but does not need to stream intermediate
-events. The sentinel is written atomically (tmp + `os.replace`) once
-`SwarmState.state` flips to `terminal`, so a `[ -f done.json ]` test is
-sufficient — there is no half-written window.
+events. For a completed reduction with marker policy enabled, the contract is saved
+first, terminal state second, and `done.json` atomically last (tmp + `os.replace`).
+With a fresh per-job output directory, `[ -f done.json ]` is sufficient to observe
+that publication; there is no half-written marker. This applies to foreground,
+resumed and detached-child completion, not just killed jobs. The marker contains
+`atomic_write: true`, the actual `success` / `partial` / `failed` result in
+`terminal_status`, and the absolute `contract_path`; completion is not necessarily
+success. Kill retains its separate `killed` status and empty contract path.
+
+The poll below assumes the run reaches completed reduction with publication enabled.
+It does not detect early launcher/executor failure or opt-out. Use state/contract/log
+inspection for those cases. Resume uses the effective rehydrated policy; arbitrary
+original runtime overrides, including completion opt-out, are not guaranteed to survive.
 
 ### Paste-ready commands (pattern 1)
 
diff --git a/docs/swarm/observability-procedure.md b/docs/swarm/observability-procedure.md
index 7f7981ccb..d985a32d2 100644
--- a/docs/swarm/observability-procedure.md
+++ b/docs/swarm/observability-procedure.md
@@ -20,15 +20,16 @@ event stream, and the human-readable Markdown log. These **three** are
 regardless of whether the run was driven by a skill, a human operator, or a CI
 subprocess, so the same procedure applies everywhere.
 
-A fourth artifact — the terminal **done sentinel** (`done.json`) — is **not**
-universal: it is emitted only on the paths that wire the on-completion sentinel
-step (the detached/resume completion path) and by `swarm kill` (which writes a
-`terminal_status=killed` sentinel). **A default inline `swarm run` does NOT emit
-`done.json`** (`reduce_wave3` does not write it; verified by
-`tests/swarm/test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel`).
-For an inline run, treat an **absent `done.json` as expected, never as a failure
-symptom**: the canonical completion signal is `.swarm-state.json` reaching
-`terminal` **AND** `return-contract.yaml` being present — not `done.json`.
+A fourth artifact, the terminal **done sentinel** (`done.json`), is published by
+completed foreground and resumed reductions, and by detached children, when the
+effective `runtime.on_completion.write_done_sentinel` policy enables it (the default).
+The executor persists the result contract first, terminal state second, then the
+atomic marker. The positive default-inline regression is
+`tests/swarm/test_e2e_user_guide.py::test_quickstart_emits_done_sentinel`.
+An absent marker can mean opt-out, an early failure, no completed reduction or a
+persistence error; it is not automatically expected just because the run is inline.
+Inspect state, contract and logs. `swarm kill --output` retains its separate
+`terminal_status=killed` marker with an empty contract path.
 
 OPS-003 / R-152 (`phase-9-tasklist.md:78-111`) requires this doc to map each
 artifact to a debugging workflow and to cover the common failure modes
@@ -47,15 +48,15 @@ swarm CLI actually emits.
 | State file | `.swarm-state.json` | `SWARM_STATE_FILENAME` | Coarse wave-level phase (DM-014), atomically rewritten on each transition. |
 | Structured log | `execution-log.jsonl` | `EXECUTION_LOG_JSONL_FILENAME` | Append-only, lock-coordinated event stream (DM-015), one JSON record per line. |
 | Human log | `execution-log.md` | `EXECUTION_LOG_MD_FILENAME` | Human-readable Markdown mirror of the JSONL stream. |
-| Done sentinel | `done.json` | `DONE_SENTINEL_FILENAME` | Atomic terminal marker (DM-017): `terminal_status` + `contract_path`. **Emitted only on the detached/resume completion path and by `swarm kill`; absent after a default inline `swarm run`.** |
+| Done sentinel | `done.json` | `DONE_SENTINEL_FILENAME` | Atomic marker (DM-017): `atomic_write: true`, actual result in `terminal_status`, absolute `contract_path`. Published after contract and terminal state by foreground/resume/detached-child completion with effective policy enabled; kill writes `killed` with an empty path. |
 
 Two supporting artifacts complete the run's on-disk record and are referenced by
 the recipes below:
 
 | Supporting | Filename | Source | What it holds |
 |---|---|---|---|
-| Result contract | `return-contract.yaml` | `RESULT_CONTRACT_FILENAME` (`commands.py`) | The final caller-facing contract; present only once state reaches `terminal`. |
-| Manifest | `manifest.json` | written by `preflight.py` (string literal, not a `*_FILENAME` constant) | Preflight-resolved job spec (INV-001 / INV-016); the run is recoverable from it alone. |
+| Result contract | `return-contract.yaml` | `RESULT_CONTRACT_FILENAME` (`commands.py`) | Caller-facing result, persisted by reduction before terminal state; a diagnostic failure contract alone does not establish completion. |
+| Manifest | `manifest.json` | written by `preflight.py` (string literal, not a `*_FILENAME` constant) | Preflight/lens snapshot used for resume (INV-001 / INV-016); arbitrary original runtime overrides are not fully restored. |
 
 ### Layer 1 — `.swarm-state.json` (coarse phase)
 
@@ -94,26 +95,27 @@ A Markdown rendering of the same event stream, one bullet per event in the shape
 pipe JSONL through `jq` — it is the default surface `swarm logs` dumps (JSONL is
 opt-in via `--jsonl`).
 
-### Layer 4 — `done.json` (terminal sentinel) — run-mode-dependent
+### Layer 4: `done.json` (terminal sentinel), policy-dependent
 
-When emitted, it is written atomically once the run reaches a terminal state and
-carries `terminal_status` (e.g. `success`, `partial`, `failed`, or `killed`) and
-`contract_path` (empty for killed jobs, since an interrupted executor never
-emitted a `return-contract.yaml`).
+Completed foreground and resumed reductions persist the result contract, then
+terminal state, then atomically publish `done.json` when the effective
+`runtime.on_completion.write_done_sentinel` policy is enabled (the default).
+Detached launchers only start their child; that child owns completion publication.
+The marker has exactly `atomic_write: true`, `terminal_status` matching the actual
+contract result (`success`, `partial` or `failed`), and the absolute `contract_path`.
+A marker means terminal completion, not that every worker succeeded.
 
-**Crucially, `done.json` is NOT a universal "job finished" signal.** It is
-emitted **only** on the paths that wire the on-completion sentinel step — the
-**detached/resume completion path** — and by `swarm kill` (which writes a
-`terminal_status=killed` sentinel). The **default inline `swarm run` does NOT
-emit it** (`reduce_wave3` does not write it; the on-completion step is not wired
-on the inline path —
-`tests/swarm/test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel`).
+Explicit opt-out suppresses the completion marker without suppressing the contract
+or terminal state. Early errors, no completed reduction and failed contract/state
+persistence do not produce a new completion marker. Inspect the state, contract and
+logs rather than treating marker absence as either success or a hang. Resume uses
+the effective rehydrated policy; arbitrary original runtime overrides, including
+opt-out, are not guaranteed to survive resume.
 
-Therefore: **only use `[ -f done.json ]` as a completion signal for detached /
-resumed / killed jobs.** For an inline run, an absent `done.json` is expected and
-is **not** a failure symptom — the completion signal is `.swarm-state.json`
-reaching `terminal` **AND** `return-contract.yaml` being present (its
-`status` field carries the verdict that `done.json.terminal_status` would carry).
+Use fresh per-job output directories. An existing marker in a reused job directory
+does not by itself prove a new resume attempt completed. `swarm kill --output`
+retains its separate `terminal_status=killed` marker and empty `contract_path`;
+that empty path must not be treated as a result-contract filename.
 
 ---
 
@@ -128,22 +130,23 @@ export OUT=/path/to/job/output
 
 ### Recipe 0 — Triage: which layer first?
 
-First, know your run mode — it changes the completion signal:
+First, check the completion policy and the job's output directory:
 
-- **Inline run** (default `swarm run`, no `--resume`): completion = state file at
-  `terminal` **AND** `return-contract.yaml` present. **`done.json` is expected to
-  be ABSENT — its absence is NOT a failure.**
-- **Detached / resumed / killed job**: completion = `done.json` present (with
-  `terminal_status`).
+- **Foreground / resumed / detached-child completion, policy enabled:** a new
+  `done.json` records the actual terminal result after contract and state persistence.
+- **Policy disabled or marker absent:** inspect `.swarm-state.json` and
+  `return-contract.yaml` together, then the logs; do not assume completion or a hang
+  from marker presence/absence alone in a reused directory.
+- **Killed job:** `done.json` has `terminal_status=killed` and an empty contract path.
 
 ```bash
-# Snapshot the layers. For an inline run, done.json is expected to be absent.
+# Snapshot the layers. Marker absence can reflect policy or incomplete execution.
 ls -la "$OUT"/.swarm-state.json "$OUT"/execution-log.jsonl \
        "$OUT"/execution-log.md "$OUT"/return-contract.yaml "$OUT"/done.json 2>&1
 jq -r '.state' "$OUT/.swarm-state.json" 2>/dev/null   # coarse phase
-# Inline-run verdict: state==terminal + contract present → read the contract.
+# Any run: state==terminal + a current contract lets you inspect the result.
 [ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
-# Detached/resume/kill verdict only: done.json carries terminal_status.
+# Any published marker carries terminal_status; kill uses the separate killed value.
 [ -f "$OUT/done.json" ] && jq -r .terminal_status "$OUT/done.json"
 ```
 
@@ -151,10 +154,10 @@ jq -r '.state' "$OUT/.swarm-state.json" 2>/dev/null   # coarse phase
   (env-missing).
 - **State stuck at `dispatching`/`normalizing` (not `terminal`) and no
   `return-contract.yaml`** → the run hung mid-wave; Recipe 2 (timeout) or
-  Recipe 3 (parse-error). (Do **not** infer a hang from a missing `done.json` on
-  an inline run — that file is expected to be absent there.)
-- **State `terminal` + `return-contract.yaml` present, `status != success`** (or,
-  for detached/killed jobs, `done.json.terminal_status != success`) → it finished
+  Recipe 3 (parse-error). A missing `done.json` alone does not establish a hang;
+  check policy and whether reduction and terminal persistence completed.
+- **State `terminal` + `return-contract.yaml` present, `status != success`** (or
+  a current marker with `terminal_status != success`) → it finished
   but degraded; Recipe 4 reads the per-worker stream to find which slots failed.
 
 ### Recipe 1 — env-missing (run never started)
@@ -165,8 +168,8 @@ pattern + the preflight artifact:
 
 ```bash
 # Symptom: no execution-log.* and no return-contract.yaml; manifest may also be
-# absent. (done.json is absent here, but it is also absent on a healthy inline
-# run, so its absence is not by itself an env-missing signal.)
+# absent. Marker absence alone is not an env-missing signal: opt-out or an
+# incomplete reduction can also leave no new done.json.
 ls "$OUT" 2>&1
 # If a manifest exists, it captures the preflight-resolved spec; if it is
 # missing too, preflight aborted before resolution (the env-missing signature).
@@ -215,9 +218,9 @@ jq -c 'select(.event_type=="worker_done" and .status=="parse_error")
        | {worker_index, status}' "$OUT/execution-log.jsonl"
 
 # Confirm the run wrapped up and read the downgraded verdict.
-# Inline run: the verdict is the contract's status field.
+# Any completed reduction: the verdict is the contract's status field.
 [ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
-# Detached/resume/kill: the verdict is done.json.terminal_status.
+# With marker policy enabled, any run also publishes done.json.terminal_status.
 [ -f "$OUT/done.json" ] && jq -r '.terminal_status' "$OUT/done.json"
 ```
 
@@ -233,13 +236,13 @@ grep -E 'wave_transition|worker_done' "$OUT/execution-log.md"
 
 When the verdict is `partial` or `failed`, the structured stream tells you
 *which* workers dragged it down, and the result contract carries the
-caller-facing detail. Read the verdict from the contract on an inline run, or
-from `done.json` on a detached/resumed/killed job:
+caller-facing detail. Read the verdict from the contract in any run mode, or
+from its published `done.json`; killed markers have no contract path:
 
 ```bash
-# Inline run: the contract is the verdict surface (status + per-worker detail).
+# Any completed reduction: the contract holds status + per-worker detail.
 [ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
-# Detached/resume/kill: done.json carries terminal_status + contract_path.
+# Any published marker: terminal_status + contract_path (empty for killed).
 [ -f "$OUT/done.json" ] && \
   jq -r '.terminal_status + " contract=" + .contract_path' "$OUT/done.json"
 
@@ -247,7 +250,7 @@ from `done.json` on a detached/resumed/killed job:
 jq -r 'select(.event_type=="worker_done") | .status' \
    "$OUT/execution-log.jsonl" | sort | uniq -c
 
-# The final contract (present once state == terminal).
+# The result contract, when present; a killed marker need not have one.
 cat "$OUT/return-contract.yaml"
 ```
 
@@ -265,8 +268,9 @@ stream directly rather than trusting the coarse phase.
 
 | Question | Layer | Read |
 |---|---|---|
-| Did an **inline** run finish, and how? | State file + contract | `.swarm-state.json` (`state==terminal`) + `return-contract.yaml` (`status`) |
-| Did a **detached/resumed/killed** job finish? | Done sentinel | `done.json` (`terminal_status`) — absent on inline runs |
+| Did a **foreground/resumed/detached-child** job finish with marker policy enabled? | Done sentinel | A new `done.json` with actual result in `terminal_status` and absolute `contract_path` |
+| Is reduction complete when marker publication is disabled? | State file + contract | `.swarm-state.json` (`state==terminal`) + current `return-contract.yaml` (`status`) |
+| Was the job killed? | Done sentinel | `done.json` with `terminal_status=killed` and empty `contract_path` |
 | Which coarse wave is it in / did it die in? | State file | `.swarm-state.json` (`state`) |
 | Which worker failed, and why? | Structured log | `execution-log.jsonl` (`event_type`, `status`) |
 | Quick human eyeball of the run | Human log | `execution-log.md` |
diff --git a/docs/swarm/operator-runbook.md b/docs/swarm/operator-runbook.md
index ea00c4c68..575e3fb39 100644
--- a/docs/swarm/operator-runbook.md
+++ b/docs/swarm/operator-runbook.md
@@ -215,10 +215,15 @@ uv run superclaude swarm run --resume lens-bare-review-ab12cd34 --output out --f
 `--stdin` / `--lens` / `--detached`), `--force-relens` (requires `--resume`),
 `--output`, `--transport`.
 
-**Resume emits more than a fresh run.** Because it re-runs Wave 2/3, a resumed
-`<DIR>` additionally contains `return-contract.yaml`, `done.json`, the
-per-worker normalized outputs, and `merged.md` when
-`amalgamation_mode == normalize+merge` — see the
+**Resume regenerates the same result artifacts as a fresh completed reduction.**
+It re-runs Wave 2/3 to regenerate `return-contract.yaml`, per-worker normalized
+outputs and `merged.md` when `amalgamation_mode == normalize+merge`. After the
+contract and terminal state are persisted, it publishes `done.json` when the
+effective rehydrated `runtime.on_completion.write_done_sentinel` policy enables it.
+Explicit opt-out suppresses the marker, not the result or terminal state; arbitrary
+original runtime overrides are not fully restored from the manifest, so an original
+opt-out is not guaranteed to survive resume. Neither early failure nor absent
+completed reduction implies a new marker. See the
 [run artifacts reference](./command-reference.md#run-artifacts) and
 [observability-procedure.md](./observability-procedure.md) (OPS-003).
Codegraph context
index_state: fresh
checked_at: 2026-11-23T20:14:00Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
call codegraph only when index_state: fresh, never to widen scope
Documentation context: Markdown is not indexed, so Q1a/Q2b use Read/Grep. Related links and current completion call sites were Read; Task 5 owns monitoring, observability and operator guidance. Context never widens the AC.

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
