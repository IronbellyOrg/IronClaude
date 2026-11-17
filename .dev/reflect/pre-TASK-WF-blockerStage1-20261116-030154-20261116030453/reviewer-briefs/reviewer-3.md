# Reviewer brief 3 (persona: refactorer; model class: opus)

## T1 card excerpt

**T1 reflection card (UC-1, pre-execution)**

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md` (22 lines: the stage 1 plan request; a byte copy of `stage-requests/stage1-request.md` in the program folder)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, schema workflow-plan/1.2, 226 lines). Cited below as PLAN:<line>.
Author of this card: the reflect orchestrator, a self-review. It did not write the plan; the plan came from a `/sc:workflow` run in another session (executor class unknown). The T2 reviewers exist to break the self-review bias.
Program spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`, cited as SPEC:<line>. Base plan report: `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` (8 blocking findings; F3, F4, F5, F6, F9, F12, F13, F15 touch stage 1).

#### Structural observations

- Constraints say "new files only" (PLAN:20), but Task 12 edits `src/superclaude/cli/review/__init__.py` (PLAN:171) and Task 14 edits `src/superclaude/cli/doctor.py` and `tests/unit/test_cli_doctor.py` (PLAN:197). Wording, not an edit of a carrier.
- Task 10 says `Depends on: Task 9` (PLAN:146) while its body reuses the reader of Task 7 (PLAN:148). `/sc:implement` runs in file order, so no failure follows.
- Task 9 acceptance asks `verdict` to agree with "the sketch" on 6,400 combinations (PLAN:139); the sketch and `truth_table.py` sit in the program folder under `.dev/tasks/to-do/`, which moves to `done/` when archived.
- Task 15 T2 fails on any file holding "a fence opener" without a registry row (PLAN:209); the skill's own other files (SKILL.md, registry.yaml, follow-up-ledger.md) must therefore avoid writing the fence text.

Persona instructions (refactorer): look at structure and sequencing: file and module layout, reuse of existing code, hidden coupling to existing files, tests and make targets that the new files touch but the plan does not mention (check whether any existing test, make target or install inventory would break or need an edit when a task lands), task order, and anything an executor must decide that the plan leaves open.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:11:43Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Every hunk line is shown as `<real file line>: <text>`. The number before the colon is the line number in the real file, not a line of this brief. Cite those numbers; leave the `N: ` prefix out of any quote.

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:106-188
```markdown
106: ## Task 7: Build the follow-up ledger codec, reader and writer
107: 
108: Depends on: Task 4
109: 
110: First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states including `sweep-flagged`). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.
111: 
112: Acceptance criteria:
113: - `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
114: - `./artifacts/reuse-audit-follow-ups.md` exists and the module imports from `ledger.py` only where the audit says to.
115: - Two readers of this ledger do not exist: `grep -rn "follow_ups" src/superclaude/cli/review` shows only the new module and its command wiring.
116: - `make lint` reports no new findings for the module.
117: 
118: ## Task 8: Build the filing state machine
119: 
120: Depends on: Task 7
121: 
122: Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The code takes the `gh` call as an injected function so tests never touch GitHub. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.
123: 
124: Acceptance criteria:
125: - `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
126: - No test or module calls the real `gh` or the network.
127: - Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.
128: 
129: 
130: ## Phase 3: Build the classifier, its inputs, the command and the safety route
131: 
132: ## Task 9: Build the classifier module
133: 
134: Depends on: Task 5
135: 
136: Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.
137: 
138: Acceptance criteria:
139: - `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
140: - No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
141: - A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
142: - `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.
143: 
144: ## Task 10: Build the supplier of the classifier's code-supplied inputs
145: 
146: Depends on: Task 9
147: 
148: Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the `Acceptance criteria:` bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).
149: 
150: Acceptance criteria:
151: - `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
152: - Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
153: - `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).
154: 
155: ## Task 11: Add the classifier tests
156: 
157: Depends on: Task 9, Task 10
158: 
159: Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), T12 (a classifier verdict changes no gate outcome except through the safety route, in a default configuration), and a test that the M, C and E answers are taken only from findings for which `classifier_inputs.py` supplied the matching input, and are UNSET or NA otherwise.
160: 
161: Acceptance criteria:
162: - `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
163: - A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
164: - A test asserts that with default settings no function of the module changes a gate result, so authority stays off (REQ-22).
165: - A test asserts that a finding without a supplied required-item list never gets an M answer from the judge.
166: 
167: ## Task 12: Add the `superclaude review classify` command
168: 
169: Depends on: Task 7, Task 9, Task 10
170: 
171: Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied, writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands. Create `tests/review/test_review_classify_cmd.py`.
172: 
173: Acceptance criteria:
174: - `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
175: - `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
176: - A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
177: - The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.
178: 
179: ## Task 13: Build the safety route
180: 
181: Depends on: Task 7
182: 
183: Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17.
184: 
185: Acceptance criteria:
186: - `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
187: - No function in the module lowers a grade (a test asserts the outcome order never decreases).
188: - Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:193-203
```markdown
193: ## Task 14: Add the install check for digest versions
194: 
195: Depends on: Task 6
196: 
197: Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.
198: 
199: Acceptance criteria:
200: - A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
201: - `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
202: - With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
203: - `make doctor` still runs and exits as before.
```

### src/superclaude/cli/review/__init__.py:1-36
```python
1: """superclaude review: deterministic helpers for document review loops.
2: 
3: Subcommand modules are optional, so branches that add different subcommands
4: merge without touching this file.
5: """
6: 
7: from __future__ import annotations
8: 
9: import importlib
10: 
11: import click
12: 
13: 
14: @click.group(name="review")
15: def review_group() -> None:
16:     """Deterministic helpers for document review loops."""
17: 
18: 
19: for _name in (
20:     "panel_cmd",
21:     "merge_cmd",
22:     "ledger_cmd",
23:     "telemetry_cmd",
24:     "lint_cmd",
25:     "estimate_cmd",
26:     "cluster_cmd",
27:     "verify_cmd",
28:     "manifest_cmd",
29: ):
30:     try:
31:         _module = importlib.import_module(f"{__name__}.{_name}")
32:     except ModuleNotFoundError as _exc:
33:         if _exc.name != f"{__name__}.{_name}":
34:             raise
35:         continue
36:     review_group.add_command(_module.command)
```

### src/superclaude/cli/doctor.py:17-55
```python
17: def run_doctor(verbose: bool = False) -> Dict[str, Any]:
18:     """
19:     Run SuperClaude health checks
20: 
21:     Args:
22:         verbose: Include detailed diagnostic information
23: 
24:     Returns:
25:         Dict with check results
26:     """
27:     checks = []
28: 
29:     # Check 1: pytest plugin loaded
30:     plugin_check = _check_pytest_plugin()
31:     checks.append(plugin_check)
32: 
33:     # Check 2: Agents installed
34:     agents_check = _check_agents_installed()
35:     checks.append(agents_check)
36: 
37:     # Check 3: Skills installed
38:     skills_check = _check_skills_installed()
39:     checks.append(skills_check)
40: 
41:     # Check 4: Configuration
42:     config_check = _check_configuration()
43:     checks.append(config_check)
44: 
45:     checks.append(_check_ccsession())
46: 
47:     checks.append(_check_codegraph())
48: 
49:     checks.append(_check_retired_mcp())
50: 
51:     return {
52:         "checks": checks,
53:         "passed": all(check["passed"] for check in checks),
54:     }
55: 
```

### Makefile:108-125
```makefile
108: # Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev
109: sync-dev:
110: 	@echo "🔄 Syncing src/superclaude/ → .claude/ for local development..."
111: 	@mkdir -p .claude/skills .claude/agents
112: 	@for skill_dir in src/superclaude/skills/*/; do \
113: 		skill_name=$$(basename "$$skill_dir"); \
114: 		case "$$skill_name" in __*) continue;; esac; \
115: 		if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
116: 			mkdir -p ".claude/skills/$$skill_name"; \
117: 			find "$$skill_dir" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' -exec sh -c ' \
118: 				src="$$1"; skill_dir="$$2"; target_base="$$3"; \
119: 				rel=$${src#$$skill_dir}; \
120: 				target_dir="$$target_base/$$(dirname "$$rel")"; \
121: 				mkdir -p "$$target_dir"; \
122: 				cp "$$src" "$$target_dir/" \
123: 			' _ {} "$$skill_dir" ".claude/skills/$$skill_name" \; ; \
124: 		fi; \
125: 	done
```

### Makefile:165-181
```makefile
165: # Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
166: verify-sync:
167: 	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
168: 	@drift=0; \
169: 	echo ""; \
170: 	echo "=== Skills ==="; \
171: 	for skill_dir in src/superclaude/skills/*/; do \
172: 		name=$$(basename "$$skill_dir"); \
173: 		case "$$name" in __*) continue;; esac; \
174: 		if [ ! -d ".claude/skills/$$name" ]; then \
175: 			echo "  ❌ MISSING in .claude/skills/: $$name"; \
176: 			drift=1; \
177: 		else \
178: 			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
179: 			if [ -n "$$changes" ]; then \
180: 				echo "  ⚠️  DIFFERS: $$name"; \
181: 				echo "$$changes" | sed 's/^/      /'; \
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:696-703
```markdown
696: | File | Holds | Read by |
697: |---|---|---|
698: | `SKILL.md` | purpose, who reads which ref, the rule version, "Delegate-only, no slash command" | people and the skill loader |
699: | `refs/rule.md` | the full rule: the three conditions, the two recorded classes, the worked examples, the table-shape rule, the guardrails, and the digest section between its fence lines | unsure reviewers, consolidators, the drift tests |
700: | `refs/scale-map.md` | one row per severity family (section 9.3) | consolidators that receive another scale; the scale-map test |
701: | `refs/follow-up-ledger.md` | the ledger contract (section 6.2), the location rule, the offer wording, unattended behaviour, the filing path | consolidation steps, the top-level session, coordinators |
702: | `refs/classifier-questions.md` | the question text, versioned | the classifier through the `superclaude review` subcommand |
703: | `refs/registry.yaml` | every carrier of the digest (section 9.2) | the drift tests; people planning a change |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:873-885
```markdown
873: ### 10.6 New files and mirrors
874: 
875: | Item | Note |
876: |---|---|
877: | `skills/sc-review-severity/` (6 files) | the shared rule package (section 9.1) |
878: | classifier code: question module, thresholds config, truth table, judge interface | reached only through a `superclaude review` subcommand whose name does not clash with existing `review` commands (REQ-24); module layout is a plan decision |
879: | follow-up ledger reader and writer | one reader and one writer for `follow-ups.md` only (REQ-10); the `reuse-auditor` agent runs first, and a mapping to `review-ledger/1` is a plan decision (section 6.2) |
880: | the `finding-grader` agent in `agents/` | today installed only [V]; needed only if the LLM judge builds on it (OD10) |
881: | a post-fix mechanical-check helper (L2) | the checks used in run 2 were ad hoc [E]; the helper is new |
882: | the final-gate sweep (GR7) | new code; stage 2 |
883: | the install check | a `make doctor` check backed by a pytest test (REQ-27) |
884: | `plugins/superclaude/` twins of `spec-panel.md` and the review-loop prompts, and from stage 4 the skill-folder mirror | hand-maintained; the plugin tree holds none of the other 11 carriers [V] |
885: | project `.claude/` copies | made by `make sync-dev` for skills, agents, commands, hooks and templates, never staged; `core/`, `rules/` and `output-styles/` are not synced [V: LC-15] |
```

## Coverage slice

| Requirement | Card ID (task) | Status | Grounding |
|---|---|---|---|
| INF-002: This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier. (source.md:3) | Constraints | covered | PLAN:20; mechanical rule: none (task 14, ratio 0.556) |
| INF-003: Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.de... (source.md:7) | task numbering | covered | PLAN:31-226 (15 tasks plus the exit task); mechanical rule: none (task 1, ratio 0.25) |
| INF-004: Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier f... (source.md:7) | Constraints | covered | PLAN:19-27; mechanical rule: none (task 10, ratio 0.45) |
| INF-006: State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. (source.md:11) | Constraints, Task 6 | covered | PLAN:20, PLAN:100; mechanical rule: containment (task 6, ratio 0.733) |
| INF-015: Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). (source.md:15) | Task 6 | covered | PLAN:96-100; mechanical rule: containment (task 6, ratio 0.9) |
| INF-016: Say the analysis template is not a carrier row (merge-rule text only in stage 4). (source.md:15) | Task 6 | covered | PLAN:96; mechanical rule: containment (task 6, ratio 0.727) |
| INF-021: Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass c... (source.md:18) | Task 16 | covered | PLAN:221-226; mechanical rule: containment (task 16, ratio 0.838) |
| INF-022: No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. (source.md:22) | Constraints | covered | PLAN:20, PLAN:22; mechanical rule: containment (task 6, ratio 0.647) |
| INF-023: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. (source.md:22) | Constraints | covered | PLAN:22; mechanical rule: none (task 3, ratio 0.529) |
| INF-024: No Jev call, key or account. (source.md:22) | Constraints | covered | PLAN:22; mechanical rule: none (task 8, ratio 0.4) |
