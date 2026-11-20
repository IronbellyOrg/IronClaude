43ff47bcec029cacef98c8c1013fd6ede6f31d63
Review one task for spec compliance.

Task brief: ## Task 10: Point reflect's plan route at Wave 4R

Depends on: Task 6, Task 7

Edit `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`: Phase B (the paragraph that says findings never edit the tasklist and a refactor re-runs Phase A as a new package) points at workflow's Wave 4R so one routing rule applies; Phase A step 4 reads the contract of the package workflow reports as final (its `plan_path`), follows `superseded_by` when the contract it read names one, and never emits an archived or `review_verdict: FAIL` plan as `remediation_plan_path` (it emits `null` and surfaces the open blockers); the rule that the plan route archives the package it replaces is stated; the headless-wrapper paragraph says the wrapper runs `/sc:implement` on the final placed package and that a refusal is a non-zero apply that the wrapper already handles fail-closed. `src/superclaude/cli/reflect/runner.py` is read to confirm the claim and is not edited.

Acceptance criteria:
- Phase B and Phase A step 4 name Wave 4R, `superseded_by` and `review_verdict: FAIL`.
- `src/superclaude/cli/reflect/runner.py` is unchanged (`git diff --stat` shows no entry for it).
- `grep -n 'src/superclaude' src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` prints only the existing `runner.py` pointer, if any.
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: 43ff47bcec029cacef98c8c1013fd6ede6f31d63
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md b/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md
index 837b11bf7..d0ea4f9e0 100644
--- a/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md
+++ b/src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md
@@ -71,14 +71,15 @@ There is one route. `--depth` never changes it, and an auto-escalation to Tier 2
    **Flatten list syntax.** Anything copied verbatim into this source (the REPORT.md summary, register rows, test names) must first be flattened: rewrite every numbered line (`1.`, `1)`) and every checkbox line (`- [ ]`, `- [x]`, `* [ ]`) as a plain `- ` bullet or a prose sentence, keeping its full text (never delete a line). A single leftover list line makes the `sc:workflow` gate fail with `E-GATE` (or makes `sc:implement` enumerate it as a task).
 3. Invoke `Skill sc:workflow-protocol` with `<output-dir>/remediation-source.md --depth standard --handoff none`. Never pass `--handoff implement`: that auto-invokes `sc:implement`, which edits product code, and the execution gate (Phase C) is always user-initiated. Do not pass `--output` (retired in `sc:workflow`; it STOPs `E-LEGACY`). The package is always created at `.dev/tasks/to-do/<slug>/`.
    Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) pass `--unattended --report-dir <report-dir>/nested/workflow-<n>/ --handoff none` (`<n>` counts from 1 and is never reused), list the nested contract in `artifacts`, also when the call failed, and read the plan path from that nested worker contract's `report_path` in step 4 instead of `<pkg>/return-contract.yaml`.
-4. Read `<pkg>/return-contract.yaml` (contract 1.1). `status: success` → resolve the absolute tasklist path (`<pkg>` + `plan_path`, which is package-relative `./<slug>.md`), record it as `plan_path` in `audit.log` and emit it as the `remediation_plan_path` contract field (§9.1, 1.8.0). Any other status (for example `E-GATE`) → surface it, record `plan_path=null`, do not retry automatically.
+4. Read `<pkg>/return-contract.yaml` (contract 1.1) of the package workflow reports as final. `status: success` → resolve the absolute tasklist path (`<pkg>` + `plan_path`, which is package-relative `./<slug>.md`). When the contract you read names a `superseded_by` package (workflow's Wave 4R replaced it), follow it: read that package's contract and use its `plan_path` instead, repeating until a contract names none. Never emit an archived plan (one under `.dev/tasks/archive/`) or a plan whose contract says `review_verdict: FAIL` as `remediation_plan_path`: record `plan_path=null`, emit `remediation_plan_path: null`, and surface the contract's `open_blockers`. Otherwise record the path as `plan_path` in `audit.log` and emit it as the `remediation_plan_path` contract field (§9.1, 1.8.0). Any other status (for example `E-GATE`) → surface it, record `plan_path=null`, do not retry automatically.
 5. `<pkg>/source.md` is the byte-exact snapshot of `remediation-source.md`, so the `## Reflect Verdict State` section is already carried there. Verify the tasklist `<slug>.md` also carries the `needs_human_decision` / `regression_count` lines; if missing, append the section to the tasklist verbatim, keeping it free of checkbox and numbered-list lines. (`sc:workflow` has no such field of its own, so reflect owns this carry.)
 
 ### Phase B — Consume the built-in pre-review
 
 `sc:workflow` already runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<slug>.md` as its Wave 4 (advisory, read-only). Reflect does **not** make a separate call on the plan; it consumes that result. Read `reflect_status` and `reflect_report_path` from `<pkg>/return-contract.yaml` and surface both with the tasklist path.
 
-- Findings never edit the tasklist (`sc:workflow` forbids it). To change the plan, append the recommendation to `<output-dir>/remediation-review-notes.md` (append-only; Phase A step 2 rewrites `remediation-source.md` from scratch each pass and re-includes these notes as `## Review Feedback`, so they are never lost) and re-run Phase A; that creates a NEW package.
+- Reflect itself never edits the tasklist. The routing of findings belongs to `sc:workflow`'s Wave 4R (`~/.claude/skills/sc-workflow-protocol/refs/remediation.md`; project `.claude/skills/sc-workflow-protocol/refs/remediation.md` second), so one rule applies: Wave 4R repairs blocking findings surgically in place, or regenerates the plan as a new package that supersedes the old one. A refactor you request below still re-runs Phase A and builds a new package; do not hand-edit a placed plan. To carry a recommendation into that new package, append it to `<output-dir>/remediation-review-notes.md` (append-only; Phase A step 2 rewrites `remediation-source.md` from scratch each pass and re-includes these notes as `## Review Feedback`, so they are never lost).
+- The plan route archives the package it replaces: when Wave 4R or a re-run of Phase A supersedes a package, that package moves to `.dev/tasks/archive/` and its contract carries `superseded_by`. Read the final package through Phase A step 4, never the archived one. If Wave 4R leaves blockers open, the final contract says `review_verdict: FAIL`: treat it as a blocker here (surface `open_blockers`, no `remediation_plan_path`).
 - `reflect_status: skipped|failed` (`reflect_report_path: null`) → say so and fall back to spawning the `self-review` agent on `<pkg>/<slug>.md`.
 - Coverage caveat: the tasklist is read as a free-form file; exact-ID matching (`R-`, `REQ-`, `SPEC-`, `T-` tokens) will not fire on `## Task N:` headings, so spec rows match through the Pass-2 containment rule only. Treat `coverage_undefined` as a surfaced warning, not a silent pass.
 - Interactive outcomes: no findings → proceed to Phase C. Findings or a blocker → surface them and ask "refactor the plan before running, or proceed as-is? [refactor / proceed]"; on `refactor`, re-run Phase A as above. A blocker → STOP and do not advance to Phase C until the user resolves it.
@@ -141,7 +142,7 @@ If no: the report at <report_path> is the final deliverable.
 
 ## Headless auto-accept under `--print` (FR-9)
 
-**One route.** `superclaude reflect run --fix` (`src/superclaude/cli/reflect/runner.py`) passes `--depth <d> --remediate`. At every depth reflect authors a plan and emits `remediation_plan_path`; the wrapper's auto-fix loop runs `/sc:implement <remediation_plan_path>` and fails closed on a non-zero apply rc.
+**One route.** `superclaude reflect run --fix` (`src/superclaude/cli/reflect/runner.py`) passes `--depth <d> --remediate`. At every depth reflect authors a plan and emits `remediation_plan_path`; the wrapper's auto-fix loop runs `/sc:implement <remediation_plan_path>` on the final placed package (the one Phase A step 4 resolved after any `superseded_by` hop) and fails closed on a non-zero apply rc. `/sc:implement` refuses an archived plan and a plan with `review_verdict: FAIL`; that refusal is a non-zero apply, which the wrapper already handles fail-closed (no re-audit, terminal HALT), so no wrapper code change is needed.
 
 The opt-in prompt above is for **interactive** runs. When reflect runs **non-interactively**
 (the reflect-wrapper launches it as `claude --print`, with **no TTY** — `--print` mode is the


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
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
