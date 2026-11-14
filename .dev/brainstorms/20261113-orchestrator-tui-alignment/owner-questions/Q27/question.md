# Q27: May SW-02's own `/sc:workflow` plan package be committed inside PR #539?

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q27 (line 554).

> May SW-02's own `/sc:workflow` plan package be committed inside PR #539? (new, R25-INV-012)

## The spec's recommended answer (verbatim)

> Yes: it is not a program, collector, key or sidecar; probe R25-INV-012 counts 921 `.dev/tasks/to-do/*` files already in #539

## Default if unanswered (verbatim)

> The package is written in the coordinator home (Q26) and referenced by absolute path; #539 commits stage named code and test paths only

## What it gates (in words)

- SW-02, "implement the owner's INV-008 ruling inside PR #539" (INV-008 is the finding that the sweep's `git status` can run commands that a repository's git configuration defines), and only its plan package (`merged-requirements.md:191`, criterion (5)). SW-02 itself waits mainly on the owner's ruling (Q1).
- Wave: W1 (the second wave); asked "when the item is next" (`merged-requirements.md:523`).

## Facts the question depends on

1. Project hard limit: work that needs more than 5 edits or touches more than one source file must go through a written plan, normally `/sc:workflow` (level 3); "Direct command selection does not waive the written-plan requirement" (`~/.claude/CLAUDE.md`, "Hard limit"). SW-02 under a fix ruling changes `probes.py`, at least three test files and the allow-list; under the accept-with-caveats ruling it edits at least 16 text locations across several files (`merged-requirements.md:191`; probe `adversarial/adversarial/invariant-probe.md:20`).
2. `/sc:workflow` always writes its package as `.dev/tasks/to-do/<id>/` in the checkout it runs in; its `--output` flag is retired (`~/.claude/skills/sc-workflow-protocol/SKILL.md:47`, `:105`).
3. Project rule: `.dev/tasks/` is always staged, never left untracked; staging is not committing (project `CLAUDE.md`).
4. Inside PR #539, rule A-004 forbids a new program, collector, JSON key, sidecar or report file, and every program artifact of this alignment work; "SW-02's own plan package is a separate question: first check whether an adequate existing plan covers SW-02; if a new one is needed, it enters #539 only under Q27" (`merged-requirements.md:978`, rule 5). The #539 checkout stages named files only, and "the only `.dev/tasks/` package allowed there is SW-02's own, under Q27" (`merged-requirements.md:988`, rule 15).
5. Measured 2026-11-14 (`gh api repos/IronbellyOrg/IronClaude/pulls/539/files`, GET only): PR #539 has 1003 files; 921 are under `.dev/tasks/to-do/`: 764 in `TASK-RF-sweep-phase1-20261108-072653` (the task file that built the sweep, frontmatter `status: "🟢 Done"`) and 157 in `TASK-RESEARCH-orchestrator-supervision-20261107-073942`.
6. The existing sweep task package is an MDTM task file (the checklist format run by `/task`) marked Done; it is not a `/sc:workflow` plan, and it does not plan SW-02 (read 2026-11-14).
7. The default's "coordinator home" exists only after Q26 is answered; if Q26 is left at its default, no coordinator home exists (`merged-requirements.md:553`).
8. `/sc:implement` writes its progress ledger inside the package and, on completion, moves the package to `.dev/tasks/done/` (`~/.claude/skills/sc-implement-protocol/SKILL.md:188`, `:196`). Which checkout's `done/` it uses when the package sits in a different checkout from the code is UNVERIFIED.
9. The #539 author (named under Q33) applies SW-02 by hand-pushed commits that stage named paths only (`merged-requirements.md:191`).
