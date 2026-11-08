# Reviewer brief 3 (refactorer, model class opus)

## T1 card excerpt

## Leads for the reviewers (each is a lead, not a verdict)

1. Unmapped rows to judge by reading both documents: T-2 (docs/designs/issue-watcher.md:479, failed entry backoff), INF-009 (the poller never assigns, comments or moves Project items, :44), INF-016 (non-goals NG-1..NG-5, :70), INF-051 (exit precedence 2, 6, 7, 5, 3, 4, :166), INF-089 (project id compared in Python, never in argv, :558), INF-101 (never-keys list, :718), INF-139 (every recorded prompt matches the D3 regex over a hostile corpus, :880), INF-147 (shared-input exit mapping, :888), INF-151 (sleeping stub ends with gh_timeout, :892). The full list is in artifacts/coverage-summary.yaml.
2. Gate divergence: design section 13 lists `make test` and `uv run ruff format --check src/ tests/` (docs/designs/issue-watcher.md:798,800). The tasklist instead uses a named affected subset, a pinned `uvx --offline ruff@0.15.20` and an xdist run, citing research/06 (DF-05, DF-60). Check that every deviation from the design is declared in the tasklist's Open Questions or Deviations section and that the substitute gates are at least as strict.
3. Section 11 of the design says `cli.py` holds "six verbs" (docs/designs/issue-watcher.md:759) while section 4.1 lists five verb names with `reset` split into two forms (:112-119). Check that the tasklist builds exactly the verbs of section 4.1 and the exit codes of section 4.3.
4. The design's UNVERIFIED shapes (docs/designs/issue-watcher.md:829-847) may enter the tasklist only as `_assumed_shape` fixtures. Check that no item states an unverified gh or Orca reply shape as fact.
5. The tasklist asks one local checkpoint commit before the POST reflect gate and forbids push and PR. Check that the commit allowlist, the BASE capture and the stop rules are internally consistent across Phase 10.

## Risk surface

- Structural: the tasklist has 34 gate-agent items; a gate that reports a finding on a pre-existing skipped test (tests/swarm/test_cli_registration.py:127) could force a false halt unless every gate prompt carves it out.
- Untested invariants: at-most-once launch rests on record-before-launch ordering and five crash points; the tasklist must test each point with five reruns.
- No regression candidate is visible in a pre-execution audit (no diff exists).

## Grounding hunks

codegraph run state: index_state=unverified checked_at=2026-11-07T18:46:15Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher  (not verified with the readiness check; use Read, Grep and Glob only)

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md (outline: every phase heading and every step header, with its line number)

```text
68: ## Task Overview
74: ## Key Objectives
85: ## Prerequisites & Dependencies
104: ## Execution Context
152: ## Detailed Task Instructions
154: ### Phase 1: Preflight and Setup
160: **Step 1.1:** Update task status
163: **Step 1.2:** Create handoff and QA directories
166: **Step 1.3:** Record the git baseline (report only; this is NOT the reflect BASE)
169: **Step 1.4:** Record tool versions
172: **Step 1.5:** Re-verify the code anchors that later items cite
175: **Step 1.6:** Create the package marker (source)
178: **Step 1.7:** Create the test package marker
181: **Step 1.8:** Run the P1 checkpoint (gate command G-1, expected exit 5)
184: ### Phase 2: Leaf Modules (runner, predicates, audit) and their tests
190: **Step 2.1:** Create `runner.py`
193: **Step 2.2:** Create `predicates.py`
196: **Step 2.3:** Create `audit.py`
199: **Step 2.4:** Create `conftest.py` part 1 (FakeRunner and FakeClock only)
202: **Step 2.5:** Create `test_runner.py`
205: **Step 2.6:** Create `test_predicates.py` part A (approval and unchanged-since)
208: **Step 2.7:** Append `test_predicates.py` part B (owner, project, marker window, order, helpers)
211: **Step 2.8:** Create `test_audit.py`
214: **Step 2.9:** Check the leaf import boundary
217: **Step 2.10:** Run gate G-1 for Phase 2
220: **Step 2.11:** Run gate G-5 (pinned ruff) on the Phase 2 files
223: ### Phase 3: GitHub Access (github module, assumed-shape fixtures, tests)
229: **Step 3.1a:** Create `github.py` part 1 (constants, jq and GraphQL text, argv builders)
232: **Step 3.1b:** Append `github.py` part 2 (reply classification, rate-limit time, call budget)
235: **Step 3.1c:** Append `github.py` part 3 (typed reads, paging, null and discovery rules)
238: **Step 3.2:** Create fixture group 1 (discovery and own login)
241: **Step 3.3:** Create fixture group 2 (REST events and marker comments)
244: **Step 3.4:** Create fixture group 3 (GraphQL edits and project items)
247: **Step 3.5:** Create fixture group 4 (stderr and GraphQL error classification)
250: **Step 3.6:** Create `test_github.py` part A (argv, constants, classifier, rate-limit time, fixtures)
253: **Step 3.7:** Append `test_github.py` part B (paging, null rules, discovery, budget)
256: **Step 3.8:** Run gate G-1 for Phase 3
259: **Step 3.9:** Run gate G-4 (`make lint`)
262: **Step 3.10:** Run gate G-5 (pinned ruff) on the Phase 3 files
265: **Step 3.11:** Run gate G-8 (no shell)
268: ### Phase 3 Gate A: Quality Verification of Phases 2 and 3 (M3 lens-based QA, standard intensity, 6 agents)
272: **Step 3.G1:** Aggregate the Phase 2 and Phase 3 outputs
275: **Step 3.G2:** Spawn the six Gate A lens agents (PARALLEL BATCH: Steps 3.G2 to 3.G7 are six independent report-only agents that read the same change set and none reads another's output, so the executor MAY spawn all six in th
278: **Step 3.G3:** Gate A lens agent 2 (part of the parallel batch of Step 3.G2)
281: **Step 3.G4:** Gate A lens agent 3 (part of the parallel batch of Step 3.G2)
284: **Step 3.G5:** Gate A lens agent 4 (part of the parallel batch of Step 3.G2)
287: **Step 3.G6:** Gate A lens agent 5 (part of the parallel batch of Step 3.G2)
290: **Step 3.G7:** Gate A lens agent 6 (part of the parallel batch of Step 3.G2)
293: **Step 3.G8:** Consolidate the Gate A findings
296: **Step 3.G9:** Fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
299: **Step 3.G10:** Verification agent 1 of 2, structural (PARALLEL with Step 3.G11: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
302: **Step 3.G11:** Verification agent 2 of 2, content (parallel with Step 3.G10)
305: **Step 3.G12:** Gate A verdict and fix-cycle control (conditional action)
308: **Step 3.G13:** Gate A cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 3.G12 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 3.G13 to 3.G17 are the explicit second fix cycle and are compact cond
311: **Step 3.G14:** Gate A cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
314: **Step 3.G15:** Gate A cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 3.G16: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME messa
317: **Step 3.G16:** Gate A cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 3.G15)
320: **Step 3.G17:** Gate A cycle-2 verdict and hard cap (conditional action; releases Phase 4)
323: ### Phase 4: Store (record module, store fixtures, tests)
329: **Step 4.1a:** Create `record.py` part 1 (errors, dataclasses, validation, migration)
332: **Step 4.1b:** Append `record.py` part 2 (`Store` protocol, `FileStore`, lock protocol)
335: **Step 4.1c:** Append `record.py` part 3 (transitions, sweep, day cap, `init_state`, dry-run helpers)
338: **Step 4.2:** Append `conftest.py` part 2 (`tmp_state` and `CrashingStore`)
341: **Step 4.3:** Create `test_record.py` part A (validation, migration, save, lock, kill switch)
344: **Step 4.4:** Append `test_record.py` part B (transitions and half-open windows)
347: **Step 4.5:** Append `test_record.py` part C (day cap, sweep, init-state, resets, dry-run file)
350: **Step 4.6:** Run gate G-1 for Phase 4
353: **Step 4.7:** Run gate G-5 (pinned ruff) on the Phase 4 files
356: ### Phase 5: Launcher (launch module, Orca fixtures, parity and contract tests)
362: **Step 5.1:** Create `launch.py`
365: **Step 5.2:** Create fixture group 5 (Orca launch replies)
368: **Step 5.3:** Append `conftest.py` part 3 (`FakeLauncher`)
371: **Step 5.4:** Create `test_launch.py` part A (prompt, argv, Orca probe, origin)
374: **Step 5.5:** Append `test_launch.py` part B (launcher outcomes, operation id, agent pin)
377: **Step 5.6:** Create `test_find_orca_parity.py`
380: **Step 5.7:** Create `test_origin_parity.py`
383: **Step 5.8:** Create `test_marker_contract.py`
386: **Step 5.9:** Run gate G-1 for Phase 5
389: **Step 5.10:** Run gate G-4 (`make lint`)
392: **Step 5.11:** Run gate G-5 (pinned ruff) on the Phase 5 files
395: ### Phase 5 Gate B: Quality Verification of Phases 4 and 5 (M3 lens-based QA, standard intensity, 6 agents)
399: **Step 5.G1:** Aggregate the Phase 4 and Phase 5 outputs
402: **Step 5.G2:** Spawn the six Gate B lens agents (PARALLEL BATCH: Steps 5.G2 to 5.G7 are six independent report-only agents that read the same change set and none reads another's output, so the executor MAY spawn all six in th
405: **Step 5.G3:** Gate B lens agent 2 (part of the parallel batch of Step 5.G2)
408: **Step 5.G4:** Gate B lens agent 3 (part of the parallel batch of Step 5.G2)
411: **Step 5.G5:** Gate B lens agent 4 (part of the parallel batch of Step 5.G2)
414: **Step 5.G6:** Gate B lens agent 5 (part of the parallel batch of Step 5.G2)
417: **Step 5.G7:** Gate B lens agent 6 (part of the parallel batch of Step 5.G2)
420: **Step 5.G8:** Consolidate the Gate B findings
423: **Step 5.G9:** Fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
426: **Step 5.G10:** Verification agent 1 of 2, structural (PARALLEL with Step 5.G11: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
429: **Step 5.G11:** Verification agent 2 of 2, content (parallel with Step 5.G10)
432: **Step 5.G12:** Gate B verdict and fix-cycle control (conditional action)
435: **Step 5.G13:** Gate B cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 5.G12 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 5.G13 to 5.G17 are the explicit second fix cycle and are compact cond
438: **Step 5.G14:** Gate B cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
441: **Step 5.G15:** Gate B cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 5.G16: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME messa
444: **Step 5.G16:** Gate B cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 5.G15)
447: **Step 5.G17:** Gate B cycle-2 verdict and hard cap (conditional action; releases Phase 6)
450: ### Phase 6: Cycle (cycle module, deps factory, cycle and SLO tests)
456: **Step 6.1:** Create `cycle.py` part 1 (constants, config, approvers, filesystem check, clock, deadline, deps, exit precedence)
459: **Step 6.2:** Append `cycle.py` part 2 (`run_cycle`)
462: **Step 6.3:** Append `cycle.py` part 3 (`status_report` and `slo_numbers`)
465: **Step 6.4:** Append `conftest.py` part 4 (deps factory and scripted GitHub world)
468: **Step 6.5:** Create `test_cycle.py` part A (configuration, approvers, filesystem check, exit precedence, deadline)
471: **Step 6.6:** Append `test_cycle.py` part B (shared inputs, rate limits, deadline, audit exits)
474: **Step 6.7:** Append `test_cycle.py` part C (per-candidate flow, launch order, dry-run, S1)
477: **Step 6.8:** Append `test_cycle.py` part D (long-run and budget properties)
480: **Step 6.9:** Create `test_slo_helper.py`
483: **Step 6.10:** Run gate G-1 for Phase 6
486: **Step 6.11:** Run gate G-5 (pinned ruff) on the Phase 6 files
489: ### Phase 7: CLI and Registration (cli module, CLI registry edit, CLI tests)
495: **Step 7.1:** Create `cli.py` part 1 (group, shared helpers, `once`, `status`, `check-config`, `init-state`)
498: **Step 7.2:** Append `cli.py` part 2 (`reset`)
501: **Step 7.3:** Register the group in the CLI registry (`main.py`)
504: **Step 7.4:** Create `test_cli.py` part A (group, config path, `check-config`, `once`, `status`)
507: **Step 7.5:** Append `test_cli.py` part B (`init-state` and `reset` with their audit lines)
510: **Step 7.6:** Run gate G-9 (the command list)
513: **Step 7.7:** Run gate G-2 (affected subset, replaces a local `make test`)
516: **Step 7.8:** Run gate G-4 (`make lint`)
519: **Step 7.9:** Run gate G-5 (pinned ruff) on the Phase 7 files
522: ### Phase 7 Gate C: Quality Verification of Phases 6 and 7 (M3 lens-based QA, standard intensity, 6 agents)
526: **Step 7.G1:** Aggregate the Phase 6 and Phase 7 outputs
529: **Step 7.G2:** Spawn the six Gate C lens agents (PARALLEL BATCH: Steps 7.G2 to 7.G7 are six independent report-only agents that read the same change set and none reads another's output, so the executor MAY spawn all six in th
532: **Step 7.G3:** Gate C lens agent 2 (part of the parallel batch of Step 7.G2)
535: **Step 7.G4:** Gate C lens agent 3 (part of the parallel batch of Step 7.G2)
538: **Step 7.G5:** Gate C lens agent 4 (part of the parallel batch of Step 7.G2)
541: **Step 7.G6:** Gate C lens agent 5 (part of the parallel batch of Step 7.G2)
544: **Step 7.G7:** Gate C lens agent 6 (part of the parallel batch of Step 7.G2)
547: **Step 7.G8:** Consolidate the Gate C findings
550: **Step 7.G9:** Fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
553: **Step 7.G10:** Verification agent 1 of 2, structural (PARALLEL with Step 7.G11: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
556: **Step 7.G11:** Verification agent 2 of 2, content (parallel with Step 7.G10)
559: **Step 7.G12:** Gate C verdict and fix-cycle control (conditional action)
562: **Step 7.G13:** Gate C cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 7.G12 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 7.G13 to 7.G17 are the explicit second fix cycle and are compact cond
565: **Step 7.G14:** Gate C cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
568: **Step 7.G15:** Gate C cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 7.G16: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME messa
571: **Step 7.G16:** Gate C cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 7.G15)
574: **Step 7.G17:** Gate C cycle-2 verdict and hard cap (conditional action; releases Phase 8)
577: ### Phase 8: Cross-Cutting Tests (PATH stubs, end-to-end, security, crash, concurrency, AST tests)
583: **Step 8.1:** Append `conftest.py` part 5 (stub-on-PATH fixture and scenario helpers)
586: **Step 8.2:** Create `test_cli_e2e.py`
589: **Step 8.3:** Create `test_security_invariants.py`
592: **Step 8.4:** Create `test_crash_injection.py`
595: **Step 8.5:** Create `test_concurrency.py`
598: **Step 8.6:** Create `test_no_shell.py`
601: **Step 8.7:** Create `test_no_text.py`
604: **Step 8.8:** Create `test_module_boundaries.py`
607: **Step 8.9:** Run gate G-1 for Phase 8
610: **Step 8.10:** Run gate G-3 (xdist, no SKIP)
613: **Step 8.11:** Run gate G-8 (no shell, whole package)
616: **Step 8.12:** Run gate G-5 (pinned ruff) on the Phase 8 files
619: ### Phase 8 Gate D: Quality Verification of Phase 8 (M3 lens-based QA, standard intensity, 6 agents)
623: **Step 8.G1:** Aggregate the Phase 8 outputs
626: **Step 8.G2:** Spawn the six Gate D lens agents (PARALLEL BATCH: Steps 8.G2 to 8.G7 are six independent report-only agents that read the same change set and none reads another's output, so the executor MAY spawn all six in th
629: **Step 8.G3:** Gate D lens agent 2 (part of the parallel batch of Step 8.G2)
632: **Step 8.G4:** Gate D lens agent 3 (part of the parallel batch of Step 8.G2)
635: **Step 8.G5:** Gate D lens agent 4 (part of the parallel batch of Step 8.G2)
638: **Step 8.G6:** Gate D lens agent 5 (part of the parallel batch of Step 8.G2)
641: **Step 8.G7:** Gate D lens agent 6 (part of the parallel batch of Step 8.G2)
644: **Step 8.G8:** Consolidate the Gate D findings
647: **Step 8.G9:** Fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
650: **Step 8.G10:** Verification agent 1 of 2, structural (PARALLEL with Step 8.G11: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
653: **Step 8.G11:** Verification agent 2 of 2, content (parallel with Step 8.G10)
656: **Step 8.G12:** Gate D verdict and fix-cycle control (conditional action)
659: **Step 8.G13:** Gate D cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 8.G12 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 8.G13 to 8.G17 are the explicit second fix cycle and are compact cond
662: **Step 8.G14:** Gate D cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
665: **Step 8.G15:** Gate D cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 8.G16: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME messa
668: **Step 8.G16:** Gate D cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 8.G15)
671: **Step 8.G17:** Gate D cycle-2 verdict and hard cap (conditional action; releases Phase 9)
674: ### Phase 9: Runbook and Final Verification (runbook, full gate run, traces, final M3 gate, M4 fidelity gate)
680: **Step 9.1:** Create the owner runbook `docs/designs/issue-watcher-setup.md`, part 1 (sections 0 to 7)
683: **Step 9.2:** Append the runbook, part 2 (sections 8 to 15)
686: **Step 9.3:** Check the runbook against the document rules
689: **Step 9.4:** Run gate G-1 on the final tree
692: **Step 9.5:** Run gate G-2 on the final tree
695: **Step 9.6:** Run gate G-3 on the final tree (xdist, no SKIP)
698: **Step 9.7:** Run gate G-4 on the final tree (`make lint`)
701: **Step 9.8:** Run gate G-5 on the final tree (pinned ruff, including the full-tree format check)
704: **Step 9.9:** Run gate G-6, part 1 (`make verify-deps`)
707: **Step 9.10:** Run gate G-6, part 2 (`make sync-dev`, preparation)
710: **Step 9.11:** Run gate G-6, part 3 (`make verify-sync`)
713: **Step 9.12:** Run gate G-7 (Python 3.10 grep)
716: **Step 9.13:** Run gate G-8 (no shell)
719: **Step 9.14:** Run gate G-9 (the five commands)
722: **Step 9.15:** Run gate G-10 (nothing outside the design changed)
725: **Step 9.16:** Run gate G-11 (file hygiene)
728: **Step 9.17:** Write the AC-1 to AC-25 trace
731: **Step 9.18:** Write the deviation register with its evidence
734: **Step 9.19:** Write the final gate record
737: ### Phase 9 Final Gate: Final M3 lens-based QA of the whole change set (standard intensity, 7 agents)
741: **Step 9.F1:** Aggregate the final change set
744: **Step 9.F2:** Spawn the seven Final-gate lens agents (PARALLEL BATCH: Steps 9.F2 to 9.F8 are seven independent report-only agents that read the same change set and none reads another's output, so the executor MAY spawn all s
747: **Step 9.F3:** Final-gate lens agent 2 (part of the parallel batch of Step 9.F2)
750: **Step 9.F4:** Final-gate lens agent 3 (part of the parallel batch of Step 9.F2)
753: **Step 9.F5:** Final-gate lens agent 4 (part of the parallel batch of Step 9.F2)
756: **Step 9.F6:** Final-gate lens agent 5 (part of the parallel batch of Step 9.F2)
759: **Step 9.F7:** Final-gate lens agent 6 (part of the parallel batch of Step 9.F2)
762: **Step 9.F8:** Final-gate domain lens agent 7 (part of the parallel batch of Step 9.F2)
765: **Step 9.F9:** Consolidate the Final-gate findings
768: **Step 9.F10:** Fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
771: **Step 9.F11:** Verification agent 1 of 2, structural (PARALLEL with Step 9.F12: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
774: **Step 9.F12:** Verification agent 2 of 2, content (parallel with Step 9.F11)
777: **Step 9.F13:** Final-gate verdict and fix-cycle control (conditional action)
780: **Step 9.F14:** Final gate cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 9.F13 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 9.F14 to 9.F18 are the explicit second fix cycle and are compact 
783: **Step 9.F15:** Final gate cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
786: **Step 9.F16:** Final gate cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 9.F17: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME m
789: **Step 9.F17:** Final gate cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 9.F16)
792: **Step 9.F18:** Final gate cycle-2 verdict and hard cap (conditional action; releases the M4 fidelity gate)
795: ### Phase 9 M4 Gate: Source-Document Fidelity of the whole change set (3 agents, after the Final gate)
799: **Step 9.M1:** Spawn the three fidelity agents (PARALLEL BATCH: Steps 9.M1 to 9.M3 are three independent report-only agents; the executor MAY spawn all three in the SAME message and then mark each item individually as its age
802: **Step 9.M2:** Fidelity agent 2 of 3, spec fidelity (part of the parallel batch of Step 9.M1)
805: **Step 9.M3:** Fidelity agent 3 of 3, cross-source contradiction (part of the parallel batch of Step 9.M1)
808: **Step 9.M4:** Consolidate the fidelity findings
811: **Step 9.M5:** Fidelity fix agent (serialized: exactly one agent may modify files, and only if blocking findings exist)
814: **Step 9.M6:** Fidelity verification agent 1 of 2, structural (PARALLEL with Step 9.M7: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAME message)
817: **Step 9.M7:** Fidelity verification agent 2 of 2, content (parallel with Step 9.M6)
820: **Step 9.M8:** Fidelity gate verdict and fix-cycle control (conditional action)
823: **Step 9.M9:** Fidelity gate cycle 2, consolidate the findings (CONDITIONAL: runs only if Step 9.M8 wrote `CYCLE2=run`; otherwise it completes as skipped; Steps 9.M9 to 9.M13 are the explicit second fix cycle and are compact 
826: **Step 9.M10:** Fidelity gate cycle 2, fix agent (CONDITIONAL on `CYCLE2=run`; serialized: exactly one agent may modify files)
829: **Step 9.M11:** Fidelity gate cycle 2, verification agent 1 of 2, structural (CONDITIONAL on `CYCLE2=run`; PARALLEL with Step 9.M12: the two verifiers are independent and report-only, so the executor MAY spawn both in the SAM
832: **Step 9.M12:** Fidelity gate cycle 2, verification agent 2 of 2, content (CONDITIONAL on `CYCLE2=run`; parallel with Step 9.M11)
835: **Step 9.M13:** Fidelity gate cycle-2 verdict and hard cap (conditional action; releases Phase 10)
838: ### Phase 10: Checkpoint Commit, POST Reflect and Completion
844: **Step 10.1:** Post-completion validation (template I17 items 1 to 4; items 5 and 6 are the Final and M4 gates already passed)
847: **Step 10.2:** Check the branch and capture BASE immediately before the commit
850: **Step 10.3:** Stage the deliverables and run the allowlist check
853: **Step 10.4:** Create the single local checkpoint commit (no push, no PR)
856: **Step 10.5:** Populate the Task Summary
859: **Step 10.6:** Independent POST reflection gate (a dedicated subagent runs the post-execution reflection end to end; penultimate item)
874: **Step 10.7:** Update task status to Done
877: ## Task Log / Notes 📋
978: ### Phase 1 - Preflight and Setup Findings
988: ### Phase 2 - Leaf Modules Findings
990: ### Phase 3 - GitHub Access Findings
992: ### Phase 4 - Store Findings
994: ### Phase 5 - Launcher Findings
996: ### Phase 6 - Cycle Findings
998: ### Phase 7 - CLI Findings
1000: ### Phase 8 - Cross-Cutting Tests Findings
1002: ### Phase 9 - Runbook and Final Verification Findings
1004: ### Phase 10 - Commit and POST Reflect Findings
1006: ### Phase Gate Findings
```

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:104-151

```markdown
## Execution Context

### References

- GOAL (verbatim from the build request): Build an MDTM task file (template 02) that implements the GitHub issue watcher exactly as designed in `docs/designs/issue-watcher.md` (IronbellyOrg/IronClaude issue 331; the design was produced by /sc:design from the finalized spec `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`). Deliverables the task must produce: the `superclaude issue-watch` Click package under `src/superclaude/cli/issue_watch/` (`__init__`, `runner`, `github`, `predicates`, `record`, `launch`, `audit`, `cycle`, `cli`), its two-line registration in `src/superclaude/cli/main.py`, the test suite under `tests/issue_watch/` (per-module unit tests, the cross-cutt [... line truncated in brief; Read the file for the rest]
- WHY (summary): issue 331 asks for an automated watcher that polls GitHub every 5 minutes for approved issues and starts `/sc:issue --claim <N>` in the owner's workspace; the owner decided option A (workspace-side poller), claim-only scope and an integer-only prompt (D1 to D3); this task builds the repo-side part that can be tested with mocks, and research/06 wins wherever the design and the research disagree.
- R-001, the design: `docs/designs/issue-watcher.md`. R-002, the finalized spec: `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`. R-003, the decision register: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`. R-004, the build request in the same folder.
- Legend: "D" is R-001 and "S" is R-002, each followed by line numbers of that document; "DF-nn" is a row of R-003; "G-1" to "G-11" (with a hyphen) are the gate-command rows of R-003 Table 1.2, distinct from the design's GitHub argv ids G1 to G7 (no hyphen); "C1" to "C5" are the crash points of design section 7.6 and "T-1" to "T-13" the transitions of design section 7.4; "AC-n" are the acceptance criteria of design section 17; "M3" is the lens-based QA sequence and "M4" the source-fidelity gate of the MDTM template; "TASK_DIR" in an item means the folder `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/`, which holds this file, `research/`, `qa/` and, after Step 1.2, `phase-outputs/`.

### Source Areas

- The `issue_watch` package inside the CLI package tree (nine files, all created by this task).
- The CLI registry module `main.py` (edited: two registration lines).
- The `tests/issue_watch` suite (all created by this task) and the existing `tests/conftest.py` autouse fixtures it must coexist with.
- The owner runbook under `docs/designs` (created by this task).
- Reused or mirrored existing code, read-only: the swarm `atomic` helper (`write_prepared_bytes`), the `install_user_setup` Orca probe (`_ORCA_CLIS`, `_find_orca`), the `sc-issue-protocol` skill (`origin_repo.py`, `refs/claim.md`, `templates/claim-comment.md`).
- Repository gates: `pyproject.toml`, `Makefile`, `.github/workflows/test.yml`, `.pre-commit-config.yaml`.

### Key Constraints

- UV only for every Python operation (`uv run pytest`, `uv run python`, `uvx --offline ruff@0.15.20`); never `python -m`, bare `pip` or bare `pytest`; no new dependency, no new pytest marker, no `hypothesis`, Python 3.10 floor, tests safe under xdist and writing only under `tmp_path`.
- Every `gh` call names `--repo IronbellyOrg/IronClaude` (or the literal repository inside a GraphQL constant); never `SuperClaude-Org`, never an `{owner}` placeholder; only a validated integer (`type(v) is int`, 1 to 999999999) reaches the launch prompt `/sc:issue --claim <n>`; the poller never writes to GitHub.
- Nothing live: no real `gh`, `orca`, `orca-ide`, `git` or network call in any test, no cron entry, no `gh label create`, no push, no PR; never stage or commit anything under `.claude/` (and never `git add -A` or `--no-verify`); `.dev/tasks` is always staged; the P10 checkpoint commit item HALTs on any commit or hook failure (stop rule) and nothing inside this task retries or works around it.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/`**

Subdirectories:
- `discovery/` - baselines, tool versions, citation anchors
- `test-results/` - raw pytest, lint and gate command output with structured summaries
- `reviews/` - gate verdicts and reviews
- `plans/` - conditional-action outputs (BASE SHA, gate verdicts, commit allowlist check)
- `reports/` - gate change-set aggregations, the AC trace, the deviation register, post-completion validation

QA agents write to `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/` (subfolders `gate-a/`, `gate-b/`, `gate-c/`, `gate-d/`, `final/`, `m4/`). These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user. The POST reflect item records its result into `reflect_post`; the frontmatter carries no `start_commit` and no `executor_model_class` (skill mode).

```

## Coverage slice

| Requirement | Source | Citation | Match | Matched task items | Ratio | Quote |
|---|---|---|---|---|---|---|
| INF-105 | inferred | docs/designs/issue-watcher.md:760-760 | containment | Step 7.3 | 0.867 | `src/superclaude/cli/main.py` / Two lines after line 561, same pattern as `reflect_group` (lines 559 and 561) |
| INF-106 | inferred | docs/designs/issue-watcher.md:761-761 | containment | Step 6.4 | 0.714 | `tests/issue_watch/__init__.py`, `conftest.py` / Package marker (C14); `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` fixtures |
| INF-107 | inferred | docs/designs/issue-watcher.md:762-762 | containment | Step 5.G4 | 0.933 | `tests/issue_watch/test_{runner,github,predicates,record,launch,audit,cycle,cli}.py` / One file per module |
| INF-108 | inferred | docs/designs/issue-watcher.md:763-763 | none | - | 0.364 | `tests/issue_watch/test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py` / Spec-named and desi |
| INF-109 | inferred | docs/designs/issue-watcher.md:764-764 | containment | Step 3.5 | 0.818 | `tests/issue_watch/fixtures/_assumed_shape/*.json` / Assumed `gh` and Orca replies, replaced by FU-1 |
| INF-110 | inferred | docs/designs/issue-watcher.md:765-765 | containment | Step 8.1 | 0.909 | `tests/issue_watch/stubs/gh`, `stubs/orca` / Executable PATH stubs for `test_cli_e2e.py` |
| INF-111 | inferred | docs/designs/issue-watcher.md:766-766 | containment | Step 9.1 | 1.0 | `docs/designs/issue-watcher-setup.md` / Runbook steps 1 to 10 for the owner |
| INF-112 | inferred | docs/designs/issue-watcher.md:768-768 | containment | Step 9.15 | 1.0 | Not changed: `pyproject.toml` (no dependency, no marker, no entry point), `Makefile`, CI, any file under `.claude/`. |
| INF-113 | inferred | docs/designs/issue-watcher.md:772-772 | containment | Step 8.G7 | 0.6 | No test runs a real `gh`, `orca`, `git` or network call. Every external effect goes through a fake or a PATH stub. |
| INF-114 | inferred | docs/designs/issue-watcher.md:784-784 | containment | Step 8.4 | 0.846 | `test_crash_injection.py` / per C1 to C5, run, crash, rerun: total fresh launches per issue ≤ 1 (NFR-005) |
| INF-115 | inferred | docs/designs/issue-watcher.md:785-785 | containment | Step 8.5 | 0.933 | `test_concurrency.py` / two `multiprocessing` processes on one `tmp_path` store: one exits 75 `lock_held`, one launch total |
| INF-116 | inferred | docs/designs/issue-watcher.md:786-786 | containment | Step 6.8 | 1.0 | `test_cycle.py::test_fifty_cycles` / 50 cycles over a changing fixture: `launches` never exceeds 1 per issue |
| INF-117 | inferred | docs/designs/issue-watcher.md:787-787 | containment | Step 6.8 | 0.947 | `test_cycle.py::test_acceptance_property` / for N in {1, 2, 6, 7, 50, 99}: at most 1 launch per cycle; after 24 h of cycles exactly min(N, 6) launched and the rest `day_cap`; after +24 h one more per  |
| INF-118 | inferred | docs/designs/issue-watcher.md:788-788 | containment | Step 8.6 | 1.0 | `test_no_shell.py` / AST: no `shell=True`, no `os.system`, no `subprocess` outside `runner.py` |
| INF-119 | inferred | docs/designs/issue-watcher.md:789-789 | containment | Step 8.7 | 0.714 | `test_no_text.py` / hostile titles, bodies and stderr (`PWNED-TITLE`) never appear in audit, store, prompt or stdout |
| INF-120 | inferred | docs/designs/issue-watcher.md:790-790 | containment | Step 8.8 | 0.8 | `test_module_boundaries.py` / AST import graph matches section 5.3; no module named `select` |
| INF-121 | inferred | docs/designs/issue-watcher.md:791-791 | containment | Step 5.8 | 0.8 | `test_marker_contract.py` / `CLAIM_MARKER` occurs in `refs/claim.md` and `templates/claim-comment.md`, read through the dual surface |
| INF-122 | inferred | docs/designs/issue-watcher.md:797-797 | containment | Step 9.M1 | 0.7 | `uv run pytest tests/issue_watch/ -v` / spec line 366 / fast loop |
| INF-123 | inferred | docs/designs/issue-watcher.md:798-798 | none | - | 0.5 | `make test` / `Makefile:13-15` / CI uses `-n auto` (`test.yml:47`), C11 |
| INF-124 | inferred | docs/designs/issue-watcher.md:799-799 | none | - | 0.435 | `make lint` / `Makefile:48-50` / includes `lint-architecture` (C8); ruff 0.15.20, select `E,F,I,N,W,TID`, line length 88, py310 (`pyproject.toml:54,174-184`) |
| INF-125 | inferred | docs/designs/issue-watcher.md:800-800 | containment | Step 3.G2 | 0.692 | `uv run ruff format --check src/ tests/` / `test.yml:106` / no make target (C10) |
| INF-126 | inferred | docs/designs/issue-watcher.md:801-801 | containment | Step 9.9 | 0.667 | `make verify-deps` / `Makefile:356-358`, `test.yml:123` / passes with no new dependency |
| INF-127 | inferred | docs/designs/issue-watcher.md:805-805 | containment | Step 6.1 | 0.625 | The Python floor is 3.10 (`pyproject.toml:16`, CI `test.yml:22`): no `tomllib`, no `datetime.UTC` (use `timezone.utc`). |
| INF-132 | inferred | docs/designs/issue-watcher.md:870-870 | containment | Step 8.G2 | 0.8 | All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stubs only. |
| INF-133 | inferred | docs/designs/issue-watcher.md:874-874 | containment | Step 6.7 | 0.692 | One `once` runs the FR-001 order; `FakeRunner` sees G1 first and no argv after an exit decision |
| INF-134 | inferred | docs/designs/issue-watcher.md:875-875 | containment | Step 6.6 | 0.818 | Discovery argv equals the FR-003 literal; 100 results or a repeated number exits 4 |
| INF-135 | inferred | docs/designs/issue-watcher.md:876-876 | none | - | 0.538 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason |
| INF-136 | inferred | docs/designs/issue-watcher.md:877-877 | containment | Step 2.7 | 0.7 | Project and owner tables: wrong project, not Backlog, unassigned, other assignee skip |
| INF-137 | inferred | docs/designs/issue-watcher.md:878-878 | containment | Step 6.2 | 0.714 | An own-login marker comment yields `claimed` and no launch |
| INF-138 | inferred | docs/designs/issue-watcher.md:879-879 | containment | Step 6.2 | 0.778 | `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips |
| INF-139 | inferred | docs/designs/issue-watcher.md:880-880 | none | - | 0.545 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises |
| INF-140 | inferred | docs/designs/issue-watcher.md:881-881 | containment | Step 5.1 | 0.769 | Launch argv equals the 12-element list; outcome table maps to `launched`, `failed`, `unknown`, `abandoned` |
| INF-141 | inferred | docs/designs/issue-watcher.md:882-882 | containment | Step 7.4 | 0.889 | No automatic retry; `status` lists the full retry argv for an `unknown` entry |
| INF-142 | inferred | docs/designs/issue-watcher.md:883-883 | none | - | 0.4 | Budget, day cap and `consumed_log` hold through `reset`; acceptance property passes |
| INF-143 | inferred | docs/designs/issue-watcher.md:884-884 | containment | Step 8.5 | 0.75 | Second process exits 75; symlinked or foreign lock exits 6 |
| INF-144 | inferred | docs/designs/issue-watcher.md:885-885 | containment | Step 6.2 | 1.0 | `DISABLED` and `enabled: false` exit 0 before any external call |
| INF-145 | inferred | docs/designs/issue-watcher.md:886-886 | containment | Step 4.3 | 0.818 | Dry-run writes only `dry-run.json` and audit; the real store is byte-identical |
| INF-146 | inferred | docs/designs/issue-watcher.md:887-887 | containment | Step 2.8 | 0.636 | Every exit writes a schema-valid audit line or the stderr fallback; rotation keeps 4 files |
| INF-147 | inferred | docs/designs/issue-watcher.md:888-888 | none | - | 0.5 | Shared-input failures map to exits 2, 3, 5, 6, 7 with the precedence 2, 6, 7, 5, 3, 4 |
| INF-148 | inferred | docs/designs/issue-watcher.md:889-889 | containment | Step 6.6 | 0.625 | Origin mismatch exits 2; parity table agrees with `origin_repo.py` |
| INF-149 | inferred | docs/designs/issue-watcher.md:890-890 | containment | Step 6.1 | 0.8 | Each verb's exit codes match section 4; `check-config` and `status` write nothing |
| INF-150 | inferred | docs/designs/issue-watcher.md:891-891 | containment | Step 6.6 | 0.8 | Rate limit persists `next_permitted_at`, clamps to 3600 s, and `reset --rate-limit` clears it |
| INF-151 | inferred | docs/designs/issue-watcher.md:892-892 | none | - | 0.429 | A sleeping stub ends with `gh_timeout`; no launch starts after 120 s |
| INF-152 | inferred | docs/designs/issue-watcher.md:893-893 | containment | Step 3.6 | 0.667 | Argv prefix scan: only G1 to G7, `--method GET`, no upstream name |
| INF-153 | inferred | docs/designs/issue-watcher.md:894-894 | containment | Step 2.1 | 0.667 | `test_no_shell.py` passes |
| INF-154 | inferred | docs/designs/issue-watcher.md:895-895 | containment | Step 8.G6 | 0.727 | Crash points C1 to C5 and 50 cycles never exceed one launch per issue |
| INF-155 | inferred | docs/designs/issue-watcher.md:896-896 | containment | Step 9.F4 | 0.667 | No new dependency; gates in section 13 pass |
| INF-156 | inferred | docs/designs/issue-watcher.md:897-897 | containment | Step 6.9 | 0.833 | `slo_numbers` returns the four values on a fixture log |
| INF-157 | inferred | docs/designs/issue-watcher.md:898-898 | containment | Step 5.G6 | 0.8 | Module-boundary and parity tests pass |
