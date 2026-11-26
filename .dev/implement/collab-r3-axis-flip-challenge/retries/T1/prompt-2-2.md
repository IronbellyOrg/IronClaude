7dabb5fbd744c8030ba69f59cd84a173825b5fde
Review one task for spec compliance.

Task brief: T1 is the whole of .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/DESIGN.md (an informal design with no enumerable task list; the whole document is the task). Its AC are the acceptance criteria table of DESIGN.md section 15.6: T1.AC1 = AC-1, T1.AC2 = AC-2, ..., T1.AC15 = AC-15 (read DESIGN.md lines 870-888 for their exact text). The orchestrator's instructions for this run (quoted under Global constraints) are explicit task instructions; in particular the final deliverable .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md must give: what was built (file list), how to run one panel on all three packages (exact command for each of ember + 2x luna, sonnet + 2x luna and haiku + 2x luna, plus PANEL_COLLAB=0), test results with counts, spike and smoke-test results, and every requirement or acceptance criterion that is not met, with the reason. An AC that the orchestrator's instructions prevent (for example one that needs full panel runs or Spike 4) is met when IMPLEMENTATION.md truthfully reports it as not met with the reason.
Global constraints: "Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ (plus the ledger folder .dev/implement/collab-r3-axis-flip-challenge/ and scratch under /tmp/evalsb-collab-r3/ and /tmp/collab-r3/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push." "Use uv for all Python (uv run pytest, uv run --no-project python -I). Run every unit and fault-injection test the design lists and fix failures." "Run the Gate 0 spikes and the one-package smoke test the design lists, but no full panel runs (the orchestrator runs those). Any step that launches reviewer or judge model sessions must hold the shared lock: wrap it as flock /tmp/collab-gateway.lock <command>, so at most one implementer uses the gateway at a time. Models allowed: muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus (claude-opus-5-5) only as the blind judge; never Qwen or glm; NOFALLBACK=1."
Start sha: 7dabb5fbd744c8030ba69f59cd84a173825b5fde
Diff against the start snapshot: Every touched file is new and untracked (git diff 7dabb5fbd744c8030ba69f59cd84a173825b5fde shows nothing for them); read each one in full: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/DESIGN.md .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/cleanup-sessions.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/launch-panel.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/catalogue.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/fallback-frame.txt .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/packages.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/panels.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/phase1-brief.txt .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/phase2-frame.txt .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/pins.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/reask-frame.txt .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/config/routing.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/lib/common.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/lib/package.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/lib/reviewer.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/__init__.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/cli.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/digest.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/findings_io.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/metrics.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/paths.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/values.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/results/smoke.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/README.md .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/after.sha256 .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/after.time .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/before.sha256 .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/before.time .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/after.sha256 .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/after.time .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/after2.sha256 .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/before.sha256 .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/before.time .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/g0-h3.out .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/ruff.log .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/smoke-c0.out .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/tests-final.log .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/tests.log .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-hooks/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-route/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/NOTES.md .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/result-starting-regex.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-haiku-5-5/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/claude-sonnet-5-5/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill20/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill25/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/fresh.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/fresh.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/killed.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/killed.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/resume.err .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/resume.stream.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/muse-ember-1.0/transcript.jsonl .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s3/result.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/test-run.log .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/conftest.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/fakes/claude .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/fakes/fake_claude.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/fakes/pgrep .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_anon.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_combine.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_command_diff.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_config.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_deal.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_gap.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_guards.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_h2.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_judge_path.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_metrics.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_model_allowlist.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_msg.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_n.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_phase1_brief.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_result.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_router.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_salvage.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_sandbox.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_select.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_summary.py .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_values.py 
Run directories of the smoke runs (evidence, new; the last one, el2-c0-20261113T221655Z-2f0d, ran in the resume session): .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/runs/el2-c0-20261113T210437Z-169d/ , .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/runs/el2-c0-20261113T221655Z-2f0d/ , .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/runs/el2-c1-20261113T210019Z-b40c/ , .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/runs/el2-c1-20261113T214437Z-42fb/ ; scoring under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/scoring/. Spike and AC-14 records of the resume session: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/ac14/resume/ and .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-partial20/.
Codegraph context
index_state: fresh
checked_at: 2026-11-13T22:09:09Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: no existing symbol's definition, signature or behaviour changed (every file is new and outside src/); no dependents to list.
Delta diff from the previous reviewed tree (empty on the first review): Whitespace-insensitive stat of lib/, r3lib/, tests/, bin/, config/ and ruff.toml (the resume session ran `ruff format` over r3lib/ and tests/), then the diff of the edited files; IMPLEMENTATION.md was rewritten in full, read it live.
 .../r3-axis-flip-challenge/r3lib/cli.py            | 190 +++++--
 .../r3-axis-flip-challenge/r3lib/digest.py         | 140 ++++-
 .../r3-axis-flip-challenge/r3lib/findings_io.py    |  56 +-
 .../r3-axis-flip-challenge/r3lib/metrics.py        | 567 +++++++++++++++++----
 .../r3-axis-flip-challenge/r3lib/values.py         |  88 +++-
 .../r3-axis-flip-challenge/ruff.toml               |   7 +
 .../r3-axis-flip-challenge/tests/conftest.py       | 203 ++++++--
 .../tests/fakes/fake_claude.py                     |  81 ++-
 .../r3-axis-flip-challenge/tests/test_anon.py      |  18 +-
 .../r3-axis-flip-challenge/tests/test_combine.py   |  28 +-
 .../tests/test_command_diff.py                     |  52 +-
 .../r3-axis-flip-challenge/tests/test_config.py    |  32 +-
 .../r3-axis-flip-challenge/tests/test_deal.py      |   8 +-
 .../r3-axis-flip-challenge/tests/test_faults.py    | 433 +++++++++++++---
 .../r3-axis-flip-challenge/tests/test_gap.py       |  17 +-
 .../r3-axis-flip-challenge/tests/test_guards.py    |  60 ++-
 .../r3-axis-flip-challenge/tests/test_h2.py        |   9 +-
 .../tests/test_judge_path.py                       |  31 +-
 .../r3-axis-flip-challenge/tests/test_metrics.py   | 123 ++++-
 .../tests/test_model_allowlist.py                  |  46 +-
 .../r3-axis-flip-challenge/tests/test_msg.py       |  30 +-
 .../tests/test_phase1_brief.py                     |  25 +-
 .../r3-axis-flip-challenge/tests/test_result.py    |  41 +-
 .../r3-axis-flip-challenge/tests/test_router.py    |  21 +-
 .../r3-axis-flip-challenge/tests/test_salvage.py   |  20 +-
 .../r3-axis-flip-challenge/tests/test_sandbox.py   |  87 +++-
 .../r3-axis-flip-challenge/tests/test_select.py    |  14 +-
 .../r3-axis-flip-challenge/tests/test_summary.py   |  39 +-
 .../r3-axis-flip-challenge/tests/test_values.py    |  19 +-
 29 files changed, 2034 insertions(+), 451 deletions(-)

diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/metrics.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/metrics.py
index fe7a6c553..9ffbf5f04 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/metrics.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/r3lib/metrics.py
@@ -21,6 +21,7 @@ _WORD = re.compile(r"[a-z]{3,}")
 
 # ------------------------------------------------------------ 9.2, 9.3
 
+
 def task_of(candidate: str, anchor: str) -> str | None:
     spans = F.locate(candidate, anchor)
     if not spans:
@@ -40,18 +41,32 @@ def _jacc(a: set, b: set) -> float | None:
 
 
 def mean_pair_jaccard(sets: dict) -> float | None:
-    vals = [j for x, y in itertools.combinations(sorted(sets), 2) if (j := _jacc(sets[x], sets[y])) is not None]
+    vals = [
+        j
+        for x, y in itertools.combinations(sorted(sets), 2)
+        if (j := _jacc(sets[x], sets[y])) is not None
+    ]
     return sum(vals) / len(vals) if vals else None
 
 
 def own_line_jaccard(findings_by_rid: dict, candidate: str) -> float | None:
-    sets = {r: {t for f in fs if f.get("origin", "own") == "own" and (t := task_of(candidate, f["anchor"]))}
-            for r, fs in findings_by_rid.items()}
+    sets = {
+        r: {
+            t
+            for f in fs
+            if f.get("origin", "own") == "own"
+            and (t := task_of(candidate, f["anchor"]))
+        }
+        for r, fs in findings_by_rid.items()
+    }
     return mean_pair_jaccard(sets)
 
 
 def all_line_jaccard(findings_by_rid: dict, candidate: str) -> float | None:
-    sets = {r: {t for f in fs if (t := task_of(candidate, f["anchor"]))} for r, fs in findings_by_rid.items()}
+    sets = {
+        r: {t for f in fs if (t := task_of(candidate, f["anchor"]))}
+        for r, fs in findings_by_rid.items()
+    }
     return mean_pair_jaccard(sets)
 
 
@@ -76,7 +91,9 @@ def echo_rate(p2_by_rid: dict, slots_by_rid: dict, source_claims: dict):
                     continue
                 mapped += 1
                 src = source_claims.get((s["source_rid"], s["source_finding_id"]), "")
-                if (j := _jacc(_words(f.get("claim", "")), _words(src))) is not None and j > 0.6:
+                if (
+                    j := _jacc(_words(f.get("claim", "")), _words(src))
+                ) is not None and j > 0.6:
                     echoes += 1
                 break
     return "n/a" if mapped == 0 else echoes / mapped
@@ -84,8 +101,17 @@ def echo_rate(p2_by_rid: dict, slots_by_rid: dict, source_claims: dict):
 
 # ------------------------------------------------------------ 9.1
 
-MIDRUN_NULL = ["first_delivery_t", "stop_blocks", "hook_calls", "hook_error", "hook_ms_p95",
-               "snapshot_missing", "late", "over_cap", "finish_signal_t"]
+MIDRUN_NULL = [
+    "first_delivery_t",
+    "stop_blocks",
+    "hook_calls",
+    "hook_error",
+    "hook_ms_p95",
+    "snapshot_missing",
+    "late",
+    "over_cap",
+    "finish_signal_t",
+]
 
 
 def _j(p: Path, default=None):
@@ -116,18 +142,34 @@ def collab_json(pkgdir) -> dict:
         p2m = _j(rv / f"{rid}.p2.meta.json", {}) or {}
         comb = _j(rv / f"{rid}.combine.json", {}) or {}
         dg = _j(pkgdir / "board" / f"{rid}.digest.json")
-        nl = next((e.get("reason") for e in ev if e.get("rid") == rid and e.get("ev") == "no_launch"), None)
+        nl = next(
+            (
+                e.get("reason")
+                for e in ev
+                if e.get("rid") == rid and e.get("ev") == "no_launch"
+            ),
+            None,
+        )
         revs[rid] = {
-            "model": role["model"], "msgs_sent": 0, "msgs_received": 1 if p2m.get("t_launch") else 0,
+            "model": role["model"],
+            "msgs_sent": 0,
+            "msgs_received": 1 if p2m.get("t_launch") else 0,
             "seal_t": (meta["seal_t"] - T0) if meta.get("seal_t") else None,
-            "resume_fallback": bool(p2m.get("resume_fallback", False)), "phase2_s": p2m.get("phase2_s"),
-            "reask_s": meta.get("reask_s"), "p2reask_s": p2m.get("p2reask_s"), "attempts": meta.get("attempts"),
-            "retry_s": meta.get("retry_s"), "retry_isolated": bool(meta.get("retry_isolated", False)),
+            "resume_fallback": bool(p2m.get("resume_fallback", False)),
+            "phase2_s": p2m.get("phase2_s"),
+            "reask_s": meta.get("reask_s"),
+            "p2reask_s": p2m.get("p2reask_s"),
+            "attempts": meta.get("attempts"),
+            "retry_s": meta.get("retry_s"),
+            "retry_isolated": bool(meta.get("retry_isolated", False)),
             "phase2_timeout": bool(p2m.get("phase2_timeout", False)),
             "p2_lines_salvaged": comb.get("p2_lines_salvaged", 0),
-            "n_planned": (dg or {}).get("n_planned"), "n_launched": p2m.get("n_launched", 0) if p2m else 0,
-            "hang_kill": meta.get("state") == "hang_kill", "no_launch_reason": nl,
-            "output_tokens_all": int(meta.get("output_tokens_all", 0) or 0) + int(p2m.get("output_tokens_all", 0) or 0),
+            "n_planned": (dg or {}).get("n_planned"),
+            "n_launched": p2m.get("n_launched", 0) if p2m else 0,
+            "hang_kill": meta.get("state") == "hang_kill",
+            "no_launch_reason": nl,
+            "output_tokens_all": int(meta.get("output_tokens_all", 0) or 0)
+            + int(p2m.get("output_tokens_all", 0) or 0),
             "session_ids": meta.get("session_ids", []) + p2m.get("session_ids", []),
             "state": meta.get("state"),
         }
@@ -148,31 +190,57 @@ def collab_json(pkgdir) -> dict:
     slots = []
     for rid, ss in slots_by.items():
         for s in ss:
-            slots.append({"rid": rid, "j": s["j"], "slot_type": s["slot_type"], "move": s["move"],
-                          "source_rid": s["source_rid"], "source_finding_id": s["source_finding_id"],
-                          "deal_r": s.get("deal_r"), "card_form": None, "deal_c": None})
+            slots.append(
+                {
+                    "rid": rid,
+                    "j": s["j"],
+                    "slot_type": s["slot_type"],
+                    "move": s["move"],
+                    "source_rid": s["source_rid"],
+                    "source_finding_id": s["source_finding_id"],
+                    "deal_r": s.get("deal_r"),
+                    "card_form": None,
+                    "deal_c": None,
+                }
+            )
     vals = pj.get("values", {})
     B = pj["B_f"]
     elapsed = (max(ends) - T0) if ends else None
-    crit = [r["rid"] for r in pc["readers"]] if pc["critical_role"] == "readers" else [pc["searcher"]["rid"]]
+    crit = (
+        [r["rid"] for r in pc["readers"]]
+        if pc["critical_role"] == "readers"
+        else [pc["searcher"]["rid"]]
+    )
     pv = vals.get("pkg", {})
     fin_at = pv.get("panel_finish_offset_s")
     seal_ts = [revs[r]["seal_t"] for r in crit]
     would = bool(fin_at is not None and any(s is None or s > fin_at for s in seal_ts))
     ledger = _j(pkgdir / "merged" / "ledger.json", {}) or {}
     cj = {
-        "arm": "A3" if run["collab"] == 1 else "A1", "panel": pj["panel"], "run_id": pj["run_id"], "pkg": pj["pkg"],
-        "values_sha256": pj.get("values_sha256"), "values_status": pj.get("values_status"),
-        "reviewers": revs, "slots": slots,
+        "arm": "A3" if run["collab"] == 1 else "A1",
+        "run_id": pj["run_id"],
+        "pkg": pj["pkg"],
+        "values_sha256": pj.get("values_sha256"),
+        "values_status": pj.get("values_status"),
+        "reviewers": revs,
+        "slots": slots,
         "panel": {
-            "T0": T0, "elapsed_s": elapsed, "baseline_elapsed_s": B,
+            "T0": T0,
+            "elapsed_s": elapsed,
+            "baseline_elapsed_s": B,
             "overhead_pct": (elapsed / B - 1) if elapsed is not None else None,
-            "k": pv.get("k"), "panel_finish_at": fin_at, "finish_would_fire": would,
+            "k": pv.get("k"),
+            "panel_finish_at": fin_at,
+            "finish_would_fire": would,
             "slo_breach": bool(pj.get("slo_breach", False)),
             "own_line_jaccard": own_line_jaccard(own_f, cand) if own_f else None,
             "pairwise_task_jaccard": all_line_jaccard(all_f, cand) if all_f else None,
-            "echo_rate": echo_rate(p2_f, slots_by, src_claims) if run["collab"] == 1 else "n/a",
-            "ledger_rows": len(ledger.get("rows", [])) if isinstance(ledger.get("rows"), list) else None,
+            "echo_rate": echo_rate(p2_f, slots_by, src_claims)
+            if run["collab"] == 1
+            else "n/a",
+            "ledger_rows": len(ledger.get("rows", []))
+            if isinstance(ledger.get("rows"), list)
+            else None,
             "challenges_real": sum(1 for s in slots if s["slot_type"] == "real"),
             "challenges_gap": sum(1 for s in slots if s["slot_type"] == "gap"),
             "gt_anchor_overlap": None,
@@ -185,8 +253,15 @@ def collab_json(pkgdir) -> dict:
 
 # ------------------------------------------------------------ 9.4 audit
 
-FORBIDDEN = ["ground-truth", "/eval-workspaces/", ".dev/reflect", "20261113-collab", "merged-requirements",
-             "/brainstorms/", "/.claude/projects/"]
+FORBIDDEN = [
+    "ground-truth",
+    "/eval-workspaces/",
+    ".dev/reflect",
+    "20261113-collab",
+    "merged-requirements",
+    "/brainstorms/",
+    "/.claude/projects/",
+]
 
 
 def _tool_inputs(obj, out: list):
@@ -222,20 +297,52 @@ def audit(pkgdir) -> dict:
     rv = pkgdir / "reviews"
     viol, ignored = [], ""
     repo = Path(pj["sb_pkg"]) / "repo"
-    st = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True)
+    st = subprocess.run(
+        ["git", "-C", str(repo), "status", "--porcelain"],
+        capture_output=True,
+        text=True,
+    )
     if st.returncode != 0 or st.stdout.strip():
-        viol.append({"check": "sandbox_dirty", "detail": st.stdout.strip()[:2000] or st.stderr.strip()[:500]})
-    ig = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--ignored", "--untracked-files=all"],
-                        capture_output=True, text=True)
+        viol.append(
+            {
+                "check": "sandbox_dirty",
+                "detail": st.stdout.strip()[:2000] or st.stderr.strip()[:500],
+            }
+        )
+    ig = subprocess.run(
+        [
+            "git",
+            "-C",
+            str(repo),
+            "status",
+            "--porcelain",
+            "--ignored",
+            "--untracked-files=all",
+        ],
+        capture_output=True,
+        text=True,
+    )
     ignored = ig.stdout.strip()
-    for p, key in ((Path(pj["cand_sb"]), "cand_sha256"), (Path(pj["cand_eval"]), "cand_sha256")):
+    for p, key in (
+        (Path(pj["cand_sb"]), "cand_sha256"),
+        (Path(pj["cand_eval"]), "cand_sha256"),
+    ):
         if values.sha256_file(p) != pj[key]:
             viol.append({"check": "candidate_changed", "detail": str(p)})
-    files = list(rv.glob("*.json")) + list(rv.glob("*.jsonl")) + list(rv.glob("sessions/**/*.jsonl"))
+    files = (
+        list(rv.glob("*.json"))
+        + list(rv.glob("*.jsonl"))
+        + list(rv.glob("sessions/**/*.jsonl"))
+    )
     own_copy_prefix = str(Path(pj["sb_pkg"]) / "p1") + "/"
     source_read = {}
     for f in sorted(set(files)):
-        if f.name.endswith(".meta.json") or f.name.endswith(".cost.json") or f.name.endswith(".combine.json") or f.name.endswith(".h2.json"):
+        if (
+            f.name.endswith(".meta.json")
+            or f.name.endswith(".cost.json")
+            or f.name.endswith(".combine.json")
+            or f.name.endswith(".h2.json")
+        ):
             continue
         rid = f.name.split(".")[0] if f.parent == rv else None
         if rid is None:
@@ -247,11 +354,23 @@ def audit(pkgdir) -> dict:
         for s in ins:
             for bad in forbidden:
                 if bad in s:
-                    viol.append({"check": "forbidden_read", "file": str(f.relative_to(pkgdir)), "pattern": bad})
+                    viol.append(
+                        {
+                            "check": "forbidden_read",
+                            "file": str(f.relative_to(pkgdir)),
+                            "pattern": bad,
+                        }
+                    )
                     break
             for m in re.finditer(re.escape(own_copy_prefix) + r"[^\s\"']+", s):
                 if not (rid and m.group(0).endswith(f"/{rid}.p1.md")):
-                    viol.append({"check": "forbidden_read", "file": str(f.relative_to(pkgdir)), "pattern": m.group(0)})
+                    viol.append(
+                        {
+                            "check": "forbidden_read",
+                            "file": str(f.relative_to(pkgdir)),
+                            "pattern": m.group(0),
+                        }
+                    )
             if pj["src_sb"] in s and rid:
                 source_read[rid] = True
     for dj in sorted((pkgdir / "board").glob("*.digest*.jsonl")):
@@ -267,7 +386,13 @@ def audit(pkgdir) -> dict:
         mj = _j(m, {}) or {}
         for sess in mj.get("sessions", []):
             if sess.get("used") and sess.get("model_ok") is False:
-                viol.append({"check": "model_identity", "file": m.name, "session": sess.get("session_id")})
+                viol.append(
+                    {
+                        "check": "model_identity",
+                        "file": m.name,
+                        "session": sess.get("session_id"),
+                    }
+                )
     # dedupe
     seen, uniq = set(), []
     for v in viol:
@@ -278,7 +403,9 @@ def audit(pkgdir) -> dict:
     out = {"violations": uniq, "ignored_writes": ignored, "source_read": source_read}
     paths.write_json(pkgdir / "audit.json", out)
     if uniq:
-        (pkgdir / "QUARANTINE").write_text("\n".join(json.dumps(v) for v in uniq) + "\n")
+        (pkgdir / "QUARANTINE").write_text(
+            "\n".join(json.dumps(v) for v in uniq) + "\n"
+        )
     return out
 
 
@@ -293,8 +420,17 @@ def _rid_of_session(pkgdir: Path, f: Path) -> str | None:
 
 # ------------------------------------------------------------ 10.1 anonymiser
 
-RESIDUE = ["P2-", '"origin"', "evalsb-collab", "20261113-collab", "/board/", "digest.jsonl", "p1norm",
-           "/runs/", "/reviews/"]
+RESIDUE = [
+    "P2-",
+    '"origin"',
+    "evalsb-collab",
+    "20261113-collab",
+    "/board/",
+    "digest.jsonl",
+    "p1norm",
+    "/runs/",
+    "/reviews/",
+]
 
 
 def anonymise(text: str) -> tuple[str, dict]:
@@ -308,9 +444,19 @@ def anonymise(text: str) -> tuple[str, dict]:
             fmap[old] = f"f{len(fmap) + 1}"
         return fmap[old]
 
-    text = re.sub(r"^(####\s+\S+\s+)\(([^)\s]+)\)", lambda m: f"{m.group(1)}({fid(m.group(2))})", text, flags=re.M)
+    text = re.sub(
+        r"^(####\s+\S+\s+)\(([^)\s]+)\)",
+        lambda m: f"{m.group(1)}({fid(m.group(2))})",
+        text,
+        flags=re.M,
+    )
     text = re.sub(r"\bP2X?-F\d+\b", lambda m: fid(m.group(0)), text)
-    text = re.sub(r"^candidate: \S+ sha256", "candidate: <candidate file> sha256", text, flags=re.M)
+    text = re.sub(
+        r"^candidate: \S+ sha256",
+        "candidate: <candidate file> sha256",
+        text,
+        flags=re.M,
+    )
     text = re.sub(r"report [^\s,]+", "report <redacted>", text)
     text = re.sub(r"/tmp/evalsb-collab-r3[^\s,)]*", "<sandbox>", text)
     text = re.sub(r',\s*"origin"\s*:\s*"(own|peer)"', "", text)
@@ -323,25 +469,47 @@ def anonymise(text: str) -> tuple[str, dict]:
 
 # ------------------------------------------------------------ 10.4 results row
 
-TARGETS = {"TASK-WF-designSpec-20261107-075614": {"GT1": "B1", "GT2": "B2", "GT5": "B5", "GT6": "I1", "GT9": "I4", "GT10": "I5"},
+TARGETS = {
+    "TASK-WF-designSpec-20261107-075614": {
+        "GT1": "B1",
+        "GT2": "B2",
+        "GT5": "B5",
+        "GT6": "I1",
+        "GT9": "I4",
+        "GT10": "I5",
+    },
     "TASK-WF-makeTheAliasOnly-20261105-051649": {"GT1": "B6", "GT3": "B8", "GT4": "I6"},
-           "TASK-WF-design-20261108-041415": {"GT1": "I7"}}
+    "TASK-WF-design-20261108-041415": {"GT1": "I7"},
+}
 CONTROL = "TASK-WF-design-20261108-041415"
 
 
 def score_fields(scores: dict, gts: dict) -> dict:
     """scores: pkg -> score.json; gts: pkg -> ground-truth.json."""
-    out = {"found14": 0, "real_blocking8": 0, "judge_blocking": 0, "wrong_blockers": 0,
-           "control_found2": 0, "control_wrong_blockers": 0, "reach": False, "target_hits": []}
+    out = {
+        "found14": 0,
+        "real_blocking8": 0,
+        "judge_blocking": 0,
+        "wrong_blockers": 0,
+        "control_found2": 0,
+        "control_wrong_blockers": 0,
+        "reach": False,
+        "target_hits": [],
+    }
     for pkg, s in scores.items():
         if s is None:
             continue
-        anyc, blk = set(s.get("gt_covered_any", [])), set(s.get("gt_covered_blocking", []))
+        anyc, blk = (
+            set(s.get("gt_covered_any", [])),
+            set(s.get("gt_covered_blocking", [])),
+        )
         if pkg == CONTROL:
             out["control_found2"] = len(anyc)
             out["control_wrong_blockers"] = int(s.get("wrong_blockers", 0))
         else:
-            real = {it["id"] for it in gts[pkg]["items"] if it.get("blocking_in_implement")}
+            real = {
+                it["id"] for it in gts[pkg]["items"] if it.get("blocking_in_implement")
+            }
             out["found14"] += len(anyc)
             out["judge_blocking"] += len(blk)
             out["real_blocking8"] += len(blk & real)
@@ -354,7 +522,12 @@ def score_fields(scores: dict, gts: dict) -> dict:
 
 
 def _gt_subs(gts: dict) -> list[str]:
-    return [F.flat(it.get("plan_quote") or "") for g in gts.values() for it in g["items"] if len(F.flat(it.get("plan_quote") or "")) >= 12]
+    return [
+        F.flat(it.get("plan_quote") or "")
+        for g in gts.values()
+        for it in g["items"]
+        if len(F.flat(it.get("plan_quote") or "")) >= 12
+    ]
 
 
 def _has_12(hay: str, quotes: list[str]) -> bool:
@@ -380,8 +553,19 @@ def gt_leak_counts(digest_lines: list[str], gts: dict) -> tuple[int, int]:
 
 def judge_ok(d: Path) -> bool:
     s = _j(d / "score.json")
-    keys = {"label", "combo", "package", "gt_total", "gt_covered_any", "gt_covered_blocking", "ledger_rows_total",
-            "ledger_rows_blocking", "blocking_rows_gt_matched", "wrong_blockers", "notes"}
+    keys = {
+        "label",
+        "combo",
+        "package",
+        "gt_total",
+        "gt_covered_any",
+        "gt_covered_blocking",
+        "ledger_rows_total",
+        "ledger_rows_blocking",
+        "blocking_rows_gt_matched",
+        "wrong_blockers",
+        "notes",
+    }
     if not isinstance(s, dict) or not keys <= set(s):
         return False
     jj = d / "judge.json"
@@ -404,11 +588,24 @@ def result_row(rundir) -> dict:
         ok = judge_ok(d)
         jok = jok and ok
         scores[k["kind"]][k["pkg"]] = _j(d / "score.json") if ok else None
-    invalid, toks_by, elapsed, overhead, slo, coll = [], {}, {}, {}, {}, {}
+    invalid, toks_by, elapsed, overhead, slo = [], {}, {}, {}, {}
     contaminated = False
-    tot = {"challenges_real": 0, "challenges_gap": 0, "n_planned": 0, "n_launched": 0, "resume_fallback": 0,
-           "phase2_timeout": 0, "p2_lines_valid": 0, "p2_lines_salvaged": 0, "p2_lines_dropped": 0,
-           "p2_dupe_dropped": 0, "p2_self_reference": 0, "retry_isolated": 0, "hang_kill": 0, "reask_count": 0}
+    tot = {
+        "challenges_real": 0,
+        "challenges_gap": 0,
+        "n_planned": 0,
+        "n_launched": 0,
+        "resume_fallback": 0,
+        "phase2_timeout": 0,
+        "p2_lines_valid": 0,
+        "p2_lines_salvaged": 0,
+        "p2_lines_dropped": 0,
+        "p2_dupe_dropped": 0,
+        "p2_self_reference": 0,
+        "retry_isolated": 0,
+        "hang_kill": 0,
+        "reask_count": 0,
+    }
     echo, olj, lrows, fwf = {}, {}, {}, {}
     leak = overlap = 0
     p2tok = reasktok = 0
@@ -422,8 +619,17 @@ def result_row(rundir) -> dict:
         cj = _j(pd / "collab.json")
         if cj:
             pan = cj["panel"]
-            elapsed[p], overhead[p], slo[p] = pan["elapsed_s"], pan["overhead_pct"], pan["slo_breach"]
-            echo[p], olj[p], lrows[p], fwf[p] = pan["echo_rate"], pan["own_line_jaccard"], pan["ledger_rows"], pan["finish_would_fire"]
+            elapsed[p], overhead[p], slo[p] = (
+                pan["elapsed_s"],
+                pan["overhead_pct"],
+                pan["slo_breach"],
+            )
+            echo[p], olj[p], lrows[p], fwf[p] = (
+                pan["echo_rate"],
+                pan["own_line_jaccard"],
+                pan["ledger_rows"],
+                pan["finish_would_fire"],
+            )
             tot["challenges_real"] += pan["challenges_real"]
             tot["challenges_gap"] += pan["challenges_gap"]
             toks_by[p] = 0
@@ -435,9 +641,17 @@ def result_row(rundir) -> dict:
                 tot["phase2_timeout"] += int(r["phase2_timeout"])
                 tot["retry_isolated"] += int(r["retry_isolated"])
                 tot["hang_kill"] += int(r["hang_kill"])
-                tot["reask_count"] += int(bool(r["reask_s"])) + int(bool(r["p2reask_s"]))
+                tot["reask_count"] += int(bool(r["reask_s"])) + int(
+                    bool(r["p2reask_s"])
+                )
                 cb = _j(pd / "reviews" / f"{rid}.combine.json", {}) or {}
-                for k in ("p2_lines_valid", "p2_lines_salvaged", "p2_lines_dropped", "p2_dupe_dropped", "p2_self_reference"):
+                for k in (
+                    "p2_lines_valid",
+                    "p2_lines_salvaged",
+                    "p2_lines_dropped",
+                    "p2_dupe_dropped",
+                    "p2_self_reference",
+                ):
                     tot[k] += int(cb.get(k, 0) or 0)
                 p2m = _j(pd / "reviews" / f"{rid}.p2.meta.json", {}) or {}
                 p2tok += int(p2m.get("output_tokens_all", 0) or 0)
@@ -455,24 +669,83 @@ def result_row(rundir) -> dict:
     if leak:
         contaminated = True
     full = score_fields(scores["full"], gts)
-    row = {"schema": "r3-result/1", "run_id": run["run_id"], "panel": run["panel"], "collab": run["collab"],
-           "arm": "A3" if run["collab"] == 1 else "A1", "values_sha256": run.get("values_sha256"),
-           "values_status": run.get("values_status"), "smoke": bool(run.get("smoke")), "tag": run.get("tag", ""),
-           **{k: full[k] for k in ("found14", "real_blocking8", "judge_blocking", "wrong_blockers", "control_found2",
-                                   "control_wrong_blockers", "reach", "target_hits")},
-           "output_tokens": {"total": sum(toks_by.values()), "by_pkg": toks_by, "phase2": p2tok, "reask": reasktok},
-           "elapsed_s": elapsed, "overhead_pct": overhead, "slo_breach": slo}
+    row = {
+        "schema": "r3-result/1",
+        "run_id": run["run_id"],
+        "panel": run["panel"],
+        "collab": run["collab"],
+        "arm": "A3" if run["collab"] == 1 else "A1",
+        "values_sha256": run.get("values_sha256"),
+        "values_status": run.get("values_status"),
+        "smoke": bool(run.get("smoke")),
+        "tag": run.get("tag", ""),
+        **{
+            k: full[k]
+            for k in (
+                "found14",
+                "real_blocking8",
+                "judge_blocking",
+                "wrong_blockers",
+                "control_found2",
+                "control_wrong_blockers",
+                "reach",
+                "target_hits",
+            )
+        },
+        "output_tokens": {
+            "total": sum(toks_by.values()),
+            "by_pkg": toks_by,
+            "phase2": p2tok,
+            "reask": reasktok,
+        },
+        "elapsed_s": elapsed,
+        "overhead_pct": overhead,
+        "slo_breach": slo,
+    }
     if run["collab"] == 1:
         sf = score_fields(scores["sealed"], gts)
-        row["sealed"] = {k: sf[k] for k in ("found14", "real_blocking8", "judge_blocking", "wrong_blockers",
-                                             "control_found2", "control_wrong_blockers", "reach")}
-        row["collab"] = {**tot, "echo_rate": echo, "own_line_jaccard": olj, "ledger_rows": lrows,
-                         "finish_would_fire": fwf, "gt_anchor_overlap": overlap, "gt_text_leak": leak}
+        row["sealed"] = {
+            k: sf[k]
+            for k in (
+                "found14",
+                "real_blocking8",
+                "judge_blocking",
+                "wrong_blockers",
+                "control_found2",
+                "control_wrong_blockers",
+                "reach",
+            )
+        }
+        row["collab"] = {
+            **tot,
+            "echo_rate": echo,
+            "own_line_jaccard": olj,
+            "ledger_rows": lrows,
+            "finish_would_fire": fwf,
+            "gt_anchor_overlap": overlap,
+            "gt_text_leak": leak,
+        }
     else:
-        row["sealed"] = {k: 0 for k in ("found14", "real_blocking8", "judge_blocking", "wrong_blockers",
-                                        "control_found2", "control_wrong_blockers")} | {"reach": False}
-        row["collab"] = {**{k: 0 for k in tot}, "echo_rate": {p: None for p in pkgs}, "own_line_jaccard": olj,
-                         "ledger_rows": lrows, "finish_would_fire": fwf, "gt_anchor_overlap": overlap, "gt_text_leak": leak}
+        row["sealed"] = {
+            k: 0
+            for k in (
+                "found14",
+                "real_blocking8",
+                "judge_blocking",
+                "wrong_blockers",
+                "control_found2",
+                "control_wrong_blockers",
+            )
+        } | {"reach": False}
+        row["collab"] = {
+            **{k: 0 for k in tot},
+            "echo_rate": {p: None for p in pkgs},
+            "own_line_jaccard": olj,
+            "ledger_rows": lrows,
+            "finish_would_fire": fwf,
+            "gt_anchor_overlap": overlap,
+            "gt_text_leak": leak,
+        }
     row["judge_ok"] = bool(jok and keys) if not run.get("no_judge") else False
     row["invalid_pkgs"] = invalid
     row["contaminated"] = contaminated
@@ -493,81 +766,156 @@ def result_row(rundir) -> dict:
 
 # ------------------------------------------------------------ 10.5 summary
 
+
 def fisher_one_sided(a_hits, a_n, b_hits, b_n) -> float:
     """P(X >= b_hits) for the B arm under the hypergeometric null."""
     K, N = a_hits + b_hits, a_n + b_n
     tot = math.comb(N, b_n)
-    return sum(math.comb(K, x) * math.comb(N - K, b_n - x) for x in range(b_hits, min(K, b_n) + 1)) / tot
+    return (
+        sum(
+            math.comb(K, x) * math.comb(N - K, b_n - x)
+            for x in range(b_hits, min(K, b_n) + 1)
+        )
+        / tot
+    )
 
 
 def summarize(rows: list[dict], panel: str, b_f: dict | None = None) -> dict:
     rows = [r for r in rows if r.get("panel") == panel]
     for r in rows:
         if r.get("values_status") != "frozen":
-            raise SystemExit(f"refused: row {r.get('run_id')} values_status={r.get('values_status')}")
+            raise SystemExit(
+                f"refused: row {r.get('run_id')} values_status={r.get('values_status')}"
+            )
     arms = {}
     for arm in ("A1", "A3"):
         rs = [r for r in rows if r["arm"] == arm]
-        good = [r for r in rs if not r["invalid_pkgs"] and r["judge_ok"] and not r["contaminated"]]
+        good = [
+            r
+            for r in rs
+            if not r["invalid_pkgs"] and r["judge_ok"] and not r["contaminated"]
+        ]
         m = {}
-        for k in ("found14", "real_blocking8", "judge_blocking", "wrong_blockers", "control_found2"):
+        for k in (
+            "found14",
+            "real_blocking8",
+            "judge_blocking",
+            "wrong_blockers",
+            "control_found2",
+        ):
             xs = [r[k] for r in good]
-            m[k] = {"mean": statistics.fmean(xs) if xs else None, "min": min(xs) if xs else None, "max": max(xs) if xs else None}
+            m[k] = {
+                "mean": statistics.fmean(xs) if xs else None,
+                "min": min(xs) if xs else None,
+                "max": max(xs) if xs else None,
+            }
         per_pkg = {}
         for r in rs:
             for p, e in r["elapsed_s"].items():
                 if e is not None:
                     per_pkg.setdefault(p, []).append(e)
-        arms[arm] = {"runs": len(rs), "quality_runs": len(good),
+        arms[arm] = {
+            "runs": len(rs),
+            "quality_runs": len(good),
             "slo_breach": sum(1 for r in rs if any(r["slo_breach"].values())),
             "invalid": sum(1 for r in rs if r["invalid_pkgs"]),
             "judge_not_ok": sum(1 for r in rs if not r["judge_ok"]),
             "contaminated": sum(1 for r in rs if r["contaminated"]),
-                     "means": m, "median_elapsed": {p: statistics.median(v) for p, v in per_pkg.items()},
-                     "elapsed": per_pkg, "reach": sum(1 for r in good if r["reach"]),
-                     "hard_credits_per_run": statistics.fmean([len(r["target_hits"]) for r in good]) if good else None}
+            "means": m,
+            "median_elapsed": {p: statistics.median(v) for p, v in per_pkg.items()},
+            "elapsed": per_pkg,
+            "reach": sum(1 for r in good if r["reach"]),
+            "hard_credits_per_run": statistics.fmean(
+                [len(r["target_hits"]) for r in good]
+            )
+            if good
+            else None,
+        }
     out = {"panel": panel, "arms": arms}
     a1, a3 = arms["A1"], arms["A3"]
     cap = {}
     for p, b_c in a1["median_elapsed"].items():
         xs = a3["elapsed"].get(p, [])
-        cap[p] = {"B_c": b_c, "median_A3": statistics.median(xs) if xs else None,
+        cap[p] = {
+            "B_c": b_c,
+            "median_A3": statistics.median(xs) if xs else None,
             "median_ok": (statistics.median(xs) <= 1.35 * b_c) if xs else None,
-                  "over_135": sum(1 for x in xs if x > 1.35 * b_c), "over_150": sum(1 for x in xs if x > 1.5 * b_c)}
+            "over_135": sum(1 for x in xs if x > 1.35 * b_c),
+            "over_150": sum(1 for x in xs if x > 1.5 * b_c),
+        }
     out["cap_check"] = cap
     if b_f:  # baseline_drift = B_c / B_f, band [0.963, 1.10]
-        out["baseline_drift"] = {p: {"drift": c / b_f[p], "in_band": 0.963 <= c / b_f[p] <= 1.10}
-                                 for p, c in a1["median_elapsed"].items() if b_f.get(p)}
+        out["baseline_drift"] = {
+            p: {"drift": c / b_f[p], "in_band": 0.963 <= c / b_f[p] <= 1.10}
+            for p, c in a1["median_elapsed"].items()
+            if b_f.get(p)
+        }
     a1_rows = [r for r in rows if r["arm"] == "A1"]
     a3_rows = [r for r in rows if r["arm"] == "A3"]
-    oj = [v for r in a1_rows for v in (r["collab"].get("own_line_jaccard") or {}).values() if isinstance(v, (int, float))]
-    lr = [v for r in a1_rows for v in (r["collab"].get("ledger_rows") or {}).values() if isinstance(v, (int, float))]
+    oj = [
+        v
+        for r in a1_rows
+        for v in (r["collab"].get("own_line_jaccard") or {}).values()
+        if isinstance(v, (int, float))
+    ]
+    lr = [
+        v
+        for r in a1_rows
+        for v in (r["collab"].get("ledger_rows") or {}).values()
+        if isinstance(v, (int, float))
+    ]
     oj_m = statistics.fmean(oj) if oj else None
     lr_m = statistics.fmean(lr) if lr else None
     conv = 0
     for r in a3_rows:
-        ojs = [v for v in (r["collab"].get("own_line_jaccard") or {}).values() if isinstance(v, (int, float))]
-        lrs = [v for v in (r["collab"].get("ledger_rows") or {}).values() if isinstance(v, (int, float))]
-        if (oj_m is not None and ojs and statistics.fmean(ojs) > oj_m + 0.15) or (lr_m and lrs and statistics.fmean(lrs) < 0.8 * lr_m):
+        ojs = [
+            v
+            for v in (r["collab"].get("own_line_jaccard") or {}).values()
+            if isinstance(v, (int, float))
+        ]
+        lrs = [
+            v
+            for v in (r["collab"].get("ledger_rows") or {}).values()
+            if isinstance(v, (int, float))
+        ]
+        if (oj_m is not None and ojs and statistics.fmean(ojs) > oj_m + 0.15) or (
+            lr_m and lrs and statistics.fmean(lrs) < 0.8 * lr_m
+        ):
             conv += 1
     out["convergence"] = conv
-    out["echo"] = sum(1 for r in a3_rows for v in (r["collab"].get("echo_rate") or {}).values() if isinstance(v, (int, float)) and v > 0.30)
-    out["fisher_p_reach"] = fisher_one_sided(a1["reach"], a1["quality_runs"], a3["reach"], a3["quality_runs"]) if a1["quality_runs"] and a3["quality_runs"] else None
+    out["echo"] = sum(
+        1
+        for r in a3_rows
+        for v in (r["collab"].get("echo_rate") or {}).values()
+        if isinstance(v, (int, float)) and v > 0.30
+    )
+    out["fisher_p_reach"] = (
+        fisher_one_sided(
+            a1["reach"], a1["quality_runs"], a3["reach"], a3["quality_runs"]
+        )
+        if a1["quality_runs"] and a3["quality_runs"]
+        else None
+    )
     return out
 
 
 def summary_table(s: dict) -> str:
-    lines = ["| Arm | runs | quality runs | found14 mean | real_blocking8 mean | wrong_blockers mean | reach | SLO breach | invalid | contaminated |",
-             "|---|---|---|---|---|---|---|---|---|---|"]
+    lines = [
+        "| Arm | runs | quality runs | found14 mean | real_blocking8 mean | wrong_blockers mean | reach | SLO breach | invalid | contaminated |",
+        "|---|---|---|---|---|---|---|---|---|---|",
+    ]
     for arm, a in s["arms"].items():
         m = a["means"]
-        lines.append(f"| {arm} | {a['runs']} | {a['quality_runs']} | {m['found14']['mean']} | {m['real_blocking8']['mean']} | "
-                     f"{m['wrong_blockers']['mean']} | {a['reach']} | {a['slo_breach']} | {a['invalid']} | {a['contaminated']} |")
+        lines.append(
+            f"| {arm} | {a['runs']} | {a['quality_runs']} | {m['found14']['mean']} | {m['real_blocking8']['mean']} | "
+            f"{m['wrong_blockers']['mean']} | {a['reach']} | {a['slo_breach']} | {a['invalid']} | {a['contaminated']} |"
+        )
     return "\n".join(lines)
 
 
 # ------------------------------------------------------------ 9.5 transcript capture
 
+
 def _session_ids(pkgdir: Path) -> set:
     rv = pkgdir / "reviews"
     ids = set()
@@ -578,9 +926,17 @@ def _session_ids(pkgdir: Path) -> set:
                 ids.add(j["session_id"])
             ids.update(s for s in (j.get("session_ids") or []) if s)
         elif isinstance(j, list):
-            ids.update(e.get("session_id") for e in j if isinstance(e, dict) and e.get("session_id"))
+            ids.update(
+                e.get("session_id")
+                for e in j
+                if isinstance(e, dict) and e.get("session_id")
+            )
     for s in list(rv.glob("*.stream.jsonl")):
-        ids.update(e.get("session_id") for e in findings_io.read_stream(s) if e.get("session_id"))
+        ids.update(
+            e.get("session_id")
+            for e in findings_io.read_stream(s)
+            if e.get("session_id")
+        )
     return {i for i in ids if i}
 
 
@@ -610,7 +966,9 @@ def _first_user_text(p: Path) -> str | None:
                     if isinstance(c, str):
                         return c
                     if isinstance(c, list):
-                        return "".join(x.get("text", "") for x in c if isinstance(x, dict))
+                        return "".join(
+                            x.get("text", "") for x in c if isinstance(x, dict)
+                        )
                     return None
     except OSError:
         return None
@@ -631,7 +989,9 @@ def capture_sessions(pkgdir) -> dict:
             continue
         rid = am.name.split(".")[0]
         brief_f = rv / f"{rid}.brief.txt"
-        brief = brief_f.read_text(encoding="utf-8").strip() if brief_f.exists() else None
+        brief = (
+            brief_f.read_text(encoding="utf-8").strip() if brief_f.exists() else None
+        )
         for cand in root.glob("*/*.jsonl"):
             fe = _first_entry(cand)
             ts = (fe or {}).get("timestamp")
@@ -649,6 +1009,7 @@ def capture_sessions(pkgdir) -> dict:
         paths.write_json(am, m)
     manifest = []
     import shutil
+
     for sid in sorted(ids):
         for f in root.glob(f"*/{sid}.jsonl"):
             dest = rv / "sessions" / sid / f.name
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml
new file mode 100644
index 000000000..9cdb00635
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/ruff.toml
@@ -0,0 +1,7 @@
+# Lint config for this redesign folder: the repo's ruff settings, minus four naming rules.
+# The code uses the design's own symbols (T0, B, B_f, T_report_p90, R, K, N, S) and "F" for the
+# findings module (DESIGN.md sections 4, 6.5, 14); renaming them would make the code differ from the design text.
+extend = "../../../../../pyproject.toml"
+
+[lint]
+extend-ignore = ["N802", "N803", "N806", "N812"]
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py
index de0c9d543..98c842f72 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py
@@ -3,14 +3,25 @@
 import json
 import os
 import subprocess
-import sys
 import time
 from pathlib import Path
 
 import pytest
-
-from conftest import (CONTROL, R3, SCORE, default_rules, finding, fixture_file, jload, launch, mini_sandbox,
-                      plan_state, report, write_plan, write_values)
+from conftest import (
+    CONTROL,
+    R3,
+    SCORE,
+    default_rules,
+    finding,
+    fixture_file,
+    jload,
+    launch,
+    mini_sandbox,
+    plan_state,
+    report,
+    write_plan,
+    write_values,
+)
 from superclaude.cli.review import findings as F
 
 pytestmark = pytest.mark.slow
@@ -24,7 +35,10 @@ def setup(env, B=40.0, rules=None, **kw):
 
 
 def events(rd):
-    return [json.loads(x) for x in (rd / CONTROL / "board/events.jsonl").read_text().splitlines()]
+    return [
+        json.loads(x)
+        for x in (rd / CONTROL / "board/events.jsonl").read_text().splitlines()
+    ]
 
 
 def ev_of(rd, rid, name):
@@ -43,23 +57,49 @@ def p2_rule(text=None, **action):
 
 def with_p2(env, action, resume=True, extra=()):
     rules = default_rules(env)
-    rules = [r for r in rules if "Second pass" not in r["match"].get("prompt_contains", "")]
-    return list(extra) + [{"match": {"resume": resume, "prompt_contains": "Second pass"}, "action": action}] + rules
-
-
-P2_OK = "## Findings block\n```findings-v1\n" + json.dumps(finding("C1", "mustnot", claim="new peer-free finding")) + "\n```\nverdict: PASS\n"
+    rules = [
+        r for r in rules if "Second pass" not in r["match"].get("prompt_contains", "")
+    ]
+    return (
+        list(extra)
+        + [
+            {
+                "match": {"resume": resume, "prompt_contains": "Second pass"},
+                "action": action,
+            }
+        ]
+        + rules
+    )
+
+
+P2_OK = (
+    "## Findings block\n```findings-v1\n"
+    + json.dumps(finding("C1", "mustnot", claim="new peer-free finding"))
+    + "\n```\nverdict: PASS\n"
+)
 
 
 def test_fake_startup_under_2s(env):
     write_plan(env, [{"match": {}, "action": {"text": "hi"}}])
     t = time.time()
-    subprocess.run(["claude", "-p", "--model", LUNA, "--output-format", "json"], input="x", env=env["env"],
-                   capture_output=True, check=True, text=True)
+    subprocess.run(
+        ["claude", "-p", "--model", LUNA, "--output-format", "json"],
+        input="x",
+        env=env["env"],
+        capture_output=True,
+        check=True,
+        text=True,
+    )
     assert time.time() - t < 2.0
 
 
 def test_f1_resume_fallback(env):
-    rules = [{"match": {"resume": True, "prompt_contains": "Second pass"}, "action": {"resume_fail": True}}] + default_rules(env)
+    rules = [
+        {
+            "match": {"resume": True, "prompt_contains": "Second pass"},
+            "action": {"resume_fail": True},
+        }
+    ] + default_rules(env)
     setup(env, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
     m = jload(rv(rd, "t4-1.p2.meta.json"))
@@ -69,24 +109,47 @@ def test_f1_resume_fallback(env):
     fresh = [x for x in st["log"] if x["resume"] is None and x["fmt"] == "stream-json"]
     assert fresh  # the fresh fallback session ran
     assert ev_of(rd, "t4-1", "resume_fallback")
-    assert "Earlier you reviewed the candidate" in (rd / CONTROL / "board/t4-1.fallback.prompt.txt").read_text()
+    assert (
+        "Earlier you reviewed the candidate"
+        in (rd / CONTROL / "board/t4-1.fallback.prompt.txt").read_text()
+    )
 
 
 def test_f1b_fallback_n_zero(env):
-    rules = [{"match": {"resume": True, "prompt_contains": "Second pass"}, "action": {"resume_fail": True}}] + default_rules(env)
+    rules = [
+        {
+            "match": {"resume": True, "prompt_contains": "Second pass"},
+            "action": {"resume_fail": True},
+        }
+    ] + default_rules(env)
     setup(env, B=12.0, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
-    nl = [e for e in events(rd) if e["ev"] == "no_launch" and e.get("reason") == "deadline_after_fallback"]
+    nl = [
+        e
+        for e in events(rd)
+        if e["ev"] == "no_launch" and e.get("reason") == "deadline_after_fallback"
+    ]
     assert nl, [e["ev"] for e in events(rd)]
 
 
 def test_f2_phase2_killed_at_deadline(env):
-    c1, c2 = json.dumps(finding("C1", "mustnot", claim="one")), json.dumps(finding("C2", "cmd", claim="two"))
-    act = {"stream_lines": [c1 + "\n", c2 + "\n", c1[:30]], "sleep_s": 60, "no_result": True}
+    c1, c2 = (
+        json.dumps(finding("C1", "mustnot", claim="one")),
+        json.dumps(finding("C2", "cmd", claim="two")),
+    )
+    act = {
+        "stream_lines": [c1 + "\n", c2 + "\n", c1[:30]],
+        "sleep_s": 60,
+        "no_result": True,
+    }
     setup(env, B=10.0, rules=with_p2(env, act))
     r, rd = launch(env, extra=["--no-judge"])
     pj = jload(rd / CONTROL / "pkg.json")
-    launched = [rid for rid in ("t4-1", "t3-1", "t2b-1") if rv(rd, f"{rid}.p2.meta.json").exists()]
+    launched = [
+        rid
+        for rid in ("t4-1", "t3-1", "t2b-1")
+        if rv(rd, f"{rid}.p2.meta.json").exists()
+    ]
     assert launched
     for rid in launched:
         p = rv(rd, f"{rid}.p2.meta.json")
@@ -102,8 +165,20 @@ def test_f2_phase2_killed_at_deadline(env):
 def test_f3_phase2_reask_fits(env):
     bad = dict(finding("C1", "mustnot", claim="fixed claim"), severity="HIGH")
     good = finding("C1", "mustnot", claim="fixed claim")
-    body = lambda o: "## Findings block\n```findings-v1\n" + json.dumps(o) + "\n```\nverdict: PASS\n"
-    extra = [{"match": {"resume": True, "prompt_contains": "findings parser"}, "action": {"text": body(good)}}]
+
+    def body(o):
+        return (
+            "## Findings block\n```findings-v1\n"
+            + json.dumps(o)
+            + "\n```\nverdict: PASS\n"
+        )
+
+    extra = [
+        {
+            "match": {"resume": True, "prompt_contains": "findings parser"},
+            "action": {"text": body(good)},
+        }
+    ]
     setup(env, rules=with_p2(env, {"text": body(bad)}, extra=extra))
     r, rd = launch(env, extra=["--no-judge"])
     m = jload(rv(rd, "t4-1.p2.meta.json"))
@@ -114,10 +189,17 @@ def test_f3_phase2_reask_fits(env):
 
 def test_f4_phase2_reask_does_not_fit(env):
     bad = dict(finding("C1", "mustnot", claim="bad line"), severity="HIGH")
-    body = "## Findings block\n```findings-v1\n" + json.dumps(bad) + "\n```\nverdict: PASS\n"
-    setup(env, B=10.0, rules=with_p2(env, {"text": body, "sleep_s": 4}))
+    body = (
+        "## Findings block\n```findings-v1\n"
+        + json.dumps(bad)
+        + "\n```\nverdict: PASS\n"
+    )
+    # B 10 gives P2_DEADLINE T0+13; phase 2 starts about T0+1.5 and ends about T0+9.5, so under 7.5 s (6 + turn) remain
+    setup(env, B=10.0, rules=with_p2(env, {"text": body, "sleep_s": 8}))
     r, rd = launch(env, extra=["--no-judge"])
-    assert not [e for e in events(rd) if e["ev"] == "proc_start" and e.get("kind") == "p2reask"]
+    assert not [
+        e for e in events(rd) if e["ev"] == "proc_start" and e.get("kind") == "p2reask"
+    ]
     assert [e for e in events(rd) if e["ev"] == "p2_lines_dropped_no_reask"]
     m = jload(rv(rd, "t4-1.p2.meta.json"))
     assert m["p2reask_s"] is None
@@ -128,8 +210,13 @@ def test_f4_phase2_reask_does_not_fit(env):
 
 
 def test_f5_phase2_cannot_rewrite_phase1(env):
-    p2 = ("## Findings block\n```findings-v1\n" + json.dumps(finding("F1", "never", claim="withdrawn and changed")) + "\n" +
-          json.dumps(finding("C1", "mustnot", claim="new one")) + "\n```\nverdict: PASS\n")
+    p2 = (
+        "## Findings block\n```findings-v1\n"
+        + json.dumps(finding("F1", "never", claim="withdrawn and changed"))
+        + "\n"
+        + json.dumps(finding("C1", "mustnot", claim="new one"))
+        + "\n```\nverdict: PASS\n"
+    )
     setup(env, rules=with_p2(env, {"text": p2}))
     r, rd = launch(env, extra=["--no-judge"])
     fs = F.parse_block(rv(rd, "t4-1.md").read_text())["findings"]
@@ -141,19 +228,38 @@ def test_f5_phase2_cannot_rewrite_phase1(env):
 
 def test_f6_no_qualifying_anchor(env):
     surf = "The artifact path artifacts/out.md is outside the edit scope."
-    p1 = {EMBER: [finding("F1", "only", "unpassable-check", claim=surf)],
-          LUNA: [finding("F1", "never", "missing-requirement", claim=surf)]}
+    p1 = {
+        EMBER: [finding("F1", "only", "unpassable-check", claim=surf)],
+        LUNA: [finding("F1", "never", "missing-requirement", claim=surf)],
+    }
     setup(env, p1=p1)
     r, rd = launch(env, extra=["--no-judge"])
     cj = jload(rd / CONTROL / "collab.json")
     assert cj["panel"]["challenges_real"] == 0 and cj["panel"]["echo_rate"] == "n/a"
-    assert cj["panel"]["challenges_gap"] >= 1
+    # gap draws are random per run; check every draw instead of requiring one: real draws stay empty,
+    # every gap draw is filled (the control candidate always has an eligible gap pool)
+    for rid in ("t4-1", "t3-1", "t2b-1"):
+        f = rd / CONTROL / f"board/{rid}.digest.json"
+        if not f.exists():
+            continue
+        dg = jload(f)
+        assert all(s["slot_type"] == "gap" for s in dg["slots"])
+        assert all(e["slot_type"] == "real" for e in dg["log"].get("slot_empty", []))
 
 
 def test_f7_two_blocks(env):
-    p1 = {EMBER: [finding("F1", "only", "unpassable-check")], LUNA: [finding("F1", "never")]}
+    p1 = {
+        EMBER: [finding("F1", "only", "unpassable-check")],
+        LUNA: [finding("F1", "never")],
+    }
     rules = default_rules(env, p1=p1)
-    rules[0]["action"]["report"] = fixture_file(env, "two.md", report([finding("F1", "only", "unpassable-check"), finding("F2", "cmd")], blocks=2))
+    rules[0]["action"]["report"] = fixture_file(
+        env,
+        "two.md",
+        report(
+            [finding("F1", "only", "unpassable-check"), finding("F2", "cmd")], blocks=2
+        ),
+    )
     setup(env, rules=rules)
     r, rd = launch(env, collab=0, extra=["--no-judge"])
     assert r.returncode == 0, r.stderr
@@ -164,13 +270,21 @@ def test_f7_two_blocks(env):
 
 def test_f8_phase1_hang(env):
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": LUNA, "resume": False, "nth": 1}, "action": {"sleep_s": 60, "text": "x"}})
+    rules.insert(
+        0,
+        {
+            "match": {"model": LUNA, "resume": False, "nth": 1},
+            "action": {"sleep_s": 60, "text": "x"},
+        },
+    )
     setup(env, B=10.0, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
     pj = jload(rd / CONTROL / "pkg.json")
     hk = [e for e in events(rd) if e["ev"] == "hang_kill"]
     assert len(hk) == 1 and pj["slo_breach"] is True and pj["valid"] is False
-    end = max(e["t"] for e in events(rd) if e["ev"] == "proc_end" and e["rid"] == hk[0]["rid"])
+    end = max(
+        e["t"] for e in events(rd) if e["ev"] == "proc_end" and e["rid"] == hk[0]["rid"]
+    )
     assert end <= pj["HANG_AT"] + 5.5
     assert (rd / CONTROL / "merged/merged-1.md").exists()
     assert r.returncode == 2 and jload(rd / "result.json")["invalid_pkgs"] == [CONTROL]
@@ -178,51 +292,116 @@ def test_f8_phase1_hang(env):
 
 def test_f9_retry_isolated(env):
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "times": 1, "action": {"text": "review with no block\nverdict: PASS\n"}})
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "times": 1,
+            "action": {"text": "review with no block\nverdict: PASS\n"},
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
     m = jload(rv(rd, "t2b-1.meta.json"))
     assert m["attempts"] == 2 and m["retry_isolated"] is True
     assert ev_of(rd, "t2b-1", "no_launch")[0]["reason"] == "retry_isolated"
     assert not (rd / CONTROL / "board/t2b-1.digest.jsonl").exists()
-    reals = [s for rid in ("t4-1", "t3-1") for s in jload(rd / CONTROL / f"board/{rid}.digest.json")["slots"] if s["slot_type"] == "real"]
+    reals = [
+        s
+        for rid in ("t4-1", "t3-1")
+        for s in jload(rd / CONTROL / f"board/{rid}.digest.json")["slots"]
+        if s["slot_type"] == "real"
+    ]
     assert all(s["source_rid"] == "t2b-1" for s in reals)
     cj = jload(rd / CONTROL / "collab.json")
-    starts = [e["t"] for e in events(rd) if e["ev"] == "proc_start" and e["rid"] == "t2b-1"]
-    assert len(starts) == 2 and cj["panel"]["elapsed_s"] >= max(starts) - cj["panel"]["T0"]
+    starts = [
+        e["t"] for e in events(rd) if e["ev"] == "proc_start" and e["rid"] == "t2b-1"
+    ]
+    assert (
+        len(starts) == 2 and cj["panel"]["elapsed_s"] >= max(starts) - cj["panel"]["T0"]
+    )
 
 
 def test_f10_wrong_model_no_fallback(env):
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "action": {"observed_model": "gpt-6.1-sol",
-                     "report": fixture_file(env, "e.md", report([finding("F1", "only", "unpassable-check")]))}})
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "action": {
+                "observed_model": "gpt-6.1-sol",
+                "report": fixture_file(
+                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
+                ),
+            },
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env)
     m = jload(rv(rd, "t2b-1.meta.json"))
     assert m["model_ok"] is False and m["state"] == "failed"
-    calls = [x for x in plan_state(env)["log"] if x["model"] != EMBER and x["model"] not in (LUNA, "claude-opus-5-5")]
-    assert not calls and len([x for x in plan_state(env)["log"] if x["model"] == EMBER]) == 2
+    calls = [
+        x
+        for x in plan_state(env)["log"]
+        if x["model"] != EMBER and x["model"] not in (LUNA, "claude-opus-5-5")
+    ]
+    assert (
+        not calls
+        and len([x for x in plan_state(env)["log"] if x["model"] == EMBER]) == 2
+    )
     assert not list(rd.glob(f"{CONTROL}/reviews/*fallback.log"))
     res = jload(rd / "result.json")
     assert res["invalid_pkgs"] == [CONTROL] and r.returncode == 2
-    assert "t2b-1" not in (rd / CONTROL / "merged/merged-1.md").read_text().split("## Ledger")[0].split("reviewers:")[1]
+    assert (
+        "t2b-1"
+        not in (rd / CONTROL / "merged/merged-1.md")
+        .read_text()
+        .split("## Ledger")[0]
+        .split("reviewers:")[1]
+    )
 
 
 def test_f11_phase1_reask_then_seal(env):
-    bad = [dict(finding("F1", "only"), severity="HIGH"), dict(finding("F2", "never"), category="nope")]
+    bad = [
+        dict(finding("F1", "only"), severity="HIGH"),
+        dict(finding("F2", "never"), category="nope"),
+    ]
     good = [finding("F1", "only"), finding("F2", "never")]
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": True, "prompt_contains": "findings parser"},
-                     "action": {"report": fixture_file(env, "good.md", report(good))}})
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "action": {"report": fixture_file(env, "bad.md", report(bad))}})
+    rules.insert(
+        0,
+        {
+            "match": {
+                "model": EMBER,
+                "resume": True,
+                "prompt_contains": "findings parser",
+            },
+            "action": {"report": fixture_file(env, "good.md", report(good))},
+        },
+    )
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "action": {"report": fixture_file(env, "bad.md", report(bad))},
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env)
     p1 = rv(rd, "t2b-1.p1.md")
-    ra = [e for e in events(rd) if e["rid"] == "t2b-1" and e["ev"] == "proc_end" and e.get("kind") == "reask"]
+    ra = [
+        e
+        for e in events(rd)
+        if e["rid"] == "t2b-1" and e["ev"] == "proc_end" and e.get("kind") == "reask"
+    ]
     assert ra and p1.stat().st_mtime >= ra[0]["t"] - 0.01
     assert oct(p1.stat().st_mode & 0o777) == "0o444"
     import hashlib
-    assert hashlib.sha256(p1.read_bytes()).hexdigest() == rv(rd, "t2b-1.p1.sha256").read_text().strip()
+
+    assert (
+        hashlib.sha256(p1.read_bytes()).hexdigest()
+        == rv(rd, "t2b-1.p1.sha256").read_text().strip()
+    )
     assert len(F.parse_block(p1.read_text())["findings"]) == 2
 
 
@@ -238,8 +417,20 @@ def test_f12_cleanup_two_runs(env):
     plan2.write_text(json.dumps(rules2))
     write_plan(env, default_rules(env))
     e2 = dict(env["env"], FAKE_CLAUDE_PLAN=str(plan2), PANEL_COLLAB="1")
-    p2 = subprocess.Popen(["bash", str(R3 / "bin/launch-panel.sh"), "el2", "--pkgs", CONTROL, "--no-judge"], env=e2,
-                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
+    p2 = subprocess.Popen(
+        [
+            "bash",
+            str(R3 / "bin/launch-panel.sh"),
+            "el2",
+            "--pkgs",
+            CONTROL,
+            "--no-judge",
+        ],
+        env=e2,
+        stdout=subprocess.PIPE,
+        stderr=subprocess.PIPE,
+        text=True,
+    )
     time.sleep(3)
     r1, rd1 = launch(env, extra=["--no-judge"])
     c1 = jload(rd1 / CONTROL / "cleanup.json")
@@ -258,13 +449,25 @@ def test_f12_cleanup_two_runs(env):
 def test_f13_sandbox_write(env):
     sb = Path(env["env"]["R3_SB_ROOT"]) / CONTROL / "repo"
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "action": {"write_file": str(sb / "x.txt"),
-                     "report": fixture_file(env, "e.md", report([finding("F1", "only", "unpassable-check")]))}})
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "action": {
+                "write_file": str(sb / "x.txt"),
+                "report": fixture_file(
+                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
+                ),
+            },
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env)
     au = jload(rd / CONTROL / "audit.json")
     assert any(v["check"] == "sandbox_dirty" for v in au["violations"])
-    assert (rd / CONTROL / "QUARANTINE").exists() and jload(rd / "result.json")["contaminated"] is True
+    assert (rd / CONTROL / "QUARANTINE").exists() and jload(rd / "result.json")[
+        "contaminated"
+    ] is True
     assert r.returncode == 3
     r2, _ = launch(env)
     assert r2.returncode == 1 and "E_SANDBOX_DIRTY" in r2.stderr
@@ -272,22 +475,43 @@ def test_f13_sandbox_write(env):
 
 def test_f14_ground_truth_read(env):
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "action": {
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "action": {
                 "tool_use_input": {"command": f"cat /x/{CONTROL}/ground-truth.json"},
-        "report": fixture_file(env, "e.md", report([finding("F1", "only", "unpassable-check")]))}})
+                "report": fixture_file(
+                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
+                ),
+            },
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env)
     au = jload(rd / CONTROL / "audit.json")
-    assert any(v["check"] == "forbidden_read" and v["pattern"] == "ground-truth" for v in au["violations"])
+    assert any(
+        v["check"] == "forbidden_read" and v["pattern"] == "ground-truth"
+        for v in au["violations"]
+    )
     assert jload(rd / "result.json")["contaminated"] is True and r.returncode == 3
 
 
 def test_f14b_peer_transcript_read(env):
     proj = env["env"]["R3_CLAUDE_PROJECTS"]
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "action": {
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "action": {
                 "tool_use_input": {"command": f"cat {proj}/-tmp-x/0000.jsonl"},
-        "report": fixture_file(env, "e.md", report([finding("F1", "only", "unpassable-check")]))}})
+                "report": fixture_file(
+                    env, "e.md", report([finding("F1", "only", "unpassable-check")])
+                ),
+            },
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
     au = jload(rd / CONTROL / "audit.json")
@@ -297,8 +521,18 @@ def test_f14b_peer_transcript_read(env):
 
 def test_f14b_killed_attempt_read(env):
     rules = default_rules(env)
-    rules.insert(0, {"match": {"model": EMBER, "resume": False}, "times": 1, "action": {
-        "tool_use_input": {"command": f"cat /x/{CONTROL}/ground-truth.json"}, "no_stdout": True, "exit": 1}})
+    rules.insert(
+        0,
+        {
+            "match": {"model": EMBER, "resume": False},
+            "times": 1,
+            "action": {
+                "tool_use_input": {"command": f"cat /x/{CONTROL}/ground-truth.json"},
+                "no_stdout": True,
+                "exit": 1,
+            },
+        },
+    )
     setup(env, rules=rules)
     r, rd = launch(env, extra=["--no-judge"])
     a1 = jload(rv(rd, "t2b-1.attempt1.meta.json"))
@@ -309,8 +543,16 @@ def test_f14b_killed_attempt_read(env):
 
 
 def test_f15_merge_refusal(env):
-    rules = [{"match": {"prompt_contains": "review 1 of 3"}, "action": {"text": "no block here\nverdict: PA
[truncated at 60000 characters; read the live files]

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC3 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/result.json:14 anchor="G0-H3, G0-HOOKS, S2 (luna resume and streaming), S3 and G0-SURF pass" chk=y,n,n,n family=spike-s2-luna-kill fix=redesign the kill check or get an owner decision first=A1 origin=new: luna kill-mid-answer check fails (no text before kill at 12 s and 20 s).
F1.2 sev=blocking trigger=B2 ac=T1.AC3 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:39 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna/result.json:14 chk=n,y,n,n family=spike-record-verdict fix=add the kill-text condition to pass and regenerate first=A1 origin=new: result.json pass:true contradicts the design pass rule.
F1.3 sev=blocking trigger=B2 ac=scope at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md:89 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/s2/gpt-6-luna-kill12/result.json:10 chk=n,y,n,n family=report-accuracy fix=state the true ranges first=A1 origin=new: fresh/resume ranges wrong.
F1.4 sev=blocking trigger=B2 ac=T1.AC3 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/NOTES.md:6 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-surf/result.json:13 chk=n,y,n,n family=report-accuracy fix=say 17 matches first=A1 origin=new: 20 matches claimed, 17 present.
F1.5 sev=blocking trigger=B1 ac=T1.AC14 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_guards.py:23 anchor="proving `r3_assert_writable` refuses `REPO/src`, `EVAL` and the four other redesign folders" chk=y,n,n,n family=guard-test-coverage fix=test all four folders first=A1 origin=new: only r1-move-radar tested.
F1.6 sev=blocking trigger=B1 ac=T1.AC14 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md:109 anchor="identical before and after building, testing and one smoke run" chk=y,n,n,n family=ac14-evidence fix=record a bracketing manifest pair under R3 first=A1 origin=new: manifests do not bracket build and tests and are not on file.
F1.7 sev=blocking trigger=B2 ac=scope at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh:45 anchor=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/runs/el2-c1-20261113T210019Z-b40c/TASK-WF-design-20261108-041415/audit.json:3 chk=n,y,n,n family=sandbox-parity fix=git add -A -f in the snapshot first=A1 origin=new: tracked-but-ignored base files dropped from the snapshot and later cleaned, so arms reviewed different sandboxes.
F2.1 sev=blocking trigger=B1 ac=T1.AC5 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md:17 anchor="The smoke test of 15.5 passes in both modes" chk=y,n,n,n family=smoke-c0-evidence fix=rerun the PANEL_COLLAB=0 smoke on the rebuilt sandbox inside an AC-14 manifest pair covers="Then the same command with `PANEL_COLLAB=0` passes the same checks without phase 2" first=A1 origin=late: the only c0 smoke ran on the pre-fix sandbox and outside any AC-14 manifest pair.
F2.2 sev=blocking trigger=B1 ac=T1.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_faults.py:150 anchor="`uv run --project \"$REPO\" pytest -p no:cacheprovider \"$R3/tests\"` passes with 0 failures and 0 skips" chk=y,n,n,n family=flaky-f6 fix=make F6 deterministic first=A1 origin=late: test_f6 asserts challenges_gap >= 1 although gap draws are random per run_id; the reviewer's full run failed it.
F1.1 sev=blocking trigger=B1 ac=T1.AC3 (open since r1-1): luna writes no text before a kill (4 tries); empirical, not fixable in code.
Saved-probe re-check hit locations (may be empty): spike-s2-luna-kill: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:37 | spike-record-verdict: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:41; .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/spike-s2.sh:42; .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh:22; .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/spikes/g0-h3/run.sh:24 | report-accuracy: no hits | guard-test-coverage: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/test_guards.py:35 | ac14-evidence: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/IMPLEMENTATION.md:112 | sandbox-parity: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/bin/build-sandbox.sh:46; .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r3-axis-flip-challenge/tests/conftest.py:166

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
