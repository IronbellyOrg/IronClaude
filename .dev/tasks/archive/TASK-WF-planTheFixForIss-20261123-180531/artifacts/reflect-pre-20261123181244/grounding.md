# Grounding record

## Source locations
- Source request and full plan Read; immutable pre-review hashes in artifacts/input-snapshot.yaml.
- LENS outline from codegraph, body Read at refactor_find.py:29-59: stale template :53, suspect=False :51, stability=experimental :58, default_workers=3 :49.
- commands.py:2121-2159 Read: shared defaults build compare_files with literal existing-review; setdefault keeps caller substitutions. reducer receives existing inline_job template. Planned edit is restricted to this block.
- commands.py:918-938 Read: lens default spec has template :929 and empty substitutions :930. preflight.py:539-545 Read: copy default only for empty template. Caller overrides therefore need preservation at post-normalization builder, not a global new validator.
- tests/swarm/test_commands_run.py:507-554 Read: real deterministic stub pattern clears target byte floor and dispatches three workers, no reducer monkeypatch. Proposed test uses public CLI group; not asserting that existing test already does.
- src/superclaude/commands/adversarial.md:15,39 Read: comma-separated existing-file interface, 2-10. Active skill SKILL.md:60-62 confirms readability. Does not provide an apply-refactor flag.
- Current four docs occurrences Read: docs/swarm/README.md:67; lens-catalog.md:25,49; user-guide.md:200. Historical release note mention intentionally excluded.

## Impact and limits
run_cmd graph depth1 impact returns 70 symbols in registration, commands, crash recovery, resume, TUI, status, input and tmux tests. This is a dependent list, not 70 confirmed direct call sites. Codegraph has no dispatch-proof claim here. Existing production path and registration were verified during planning; this review refreshes changed-block evidence. No inheritance/polymorphic surface is being added; eligible class kind guard did not fire, implementation coverage is null. No new component proposed, so no pre reuse sweep needed. No external-library claim requires Context7 in this internal planning review.

## Negative evidence and skips
No matching memory file found in either inventory. No paid/model-backed swarm, code edit, new regression execution or repaired CLI run occurred. Those are future task acceptance conditions, not missing current-planning deliverables. UC2-only verification, runtime reachability, interaction-effects and promotion do not apply. Input references to future artifacts are not substituted with fabricated files.
