# QA Report: task-integrity, lens task-research-alignment

**Task file:** .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Inputs:** research/research-notes.md, BUILD-REQUEST.md, .dev/troubleshoot/untyped-bmad-and-ponytail-are-only-20261107072723/REPORT.md
**Status:** Complete
**Date:** 2026-11-07

---

## Blocking findings

| # | Sev | Where in task file | Finding | Fix |
|---|-----|--------------------|---------|-----|
| 1 | IMPORTANT | Key Constraints (line 128), Step 2.1 prompt (line 192), Open Question 3, Builder Note 7 | Unsupported provenance claim. The task says this worktree's `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*` are "the output of a real `bmad install --yes --modules bmm --tools claude-code --output-folder _bmad-output`" and tags rows OBSERVED-FROM-EXISTING-INSTALL. research-notes.md (Workspace facts) says only "a project where BMAD was installed". Checked: `_bmad/_config/manifest.yaml` lines 2, 7, 14 show version 6.10.0 (not 6.9.0), installDate 2026-04-18; git log on it: "upgrade BMad framework and add Rigorflow agents", "sync bmad-* skills + config"; all three trees are tracked (17, 237 and 577 files) and `_bmad-output` holds project brainstorms, PRDs and specs, not installer output. | Delete the claim. Tell agent 01 to read the manifest version and tag rows as observed from a 6.10.0, hand-maintained project, or derive what a fresh install creates from installer code only and mark the rest UNVERIFIED. |
| 2 | IMPORTANT | synth-03 (Step 5.3) comparison criteria, synth-04 (Step 5.4), Step 6.8 criteria | Edge cases from the notes live only in the research-agent prompts (2.3, 2.4) and never reach a verification clause downstream. (a) The whole-HOME snapshot oracle (test-57:448-450, `snap "${H}"`) is not a comparison row or plan check, so nothing forces the report to say which options write inside it. (b) Survival across reboot and `superclaude install` (the clobber risk for options B and D) and HOME persistence are not criteria either. Only Gate 4/5 meaning-checks could catch their loss. | Add rows "writes inside the whole-HOME snapshot" and "survives reboot and superclaude install" to synth-03; add both to the Step 6.8 checklist. |
| 3 | IMPORTANT | synth-04 doc list (Step 5.4), Step 6.8 criterion 8 | README edit constraints from the prior diagnosis are dropped. Grep finds zero hits for markdownlint, `releases.json` or "upstream GitHub CLI". README :241 appears only in the agent 05 scope, not in the plan's document list or the checklist. REPORT.md: edit :241, leave :308, keep the "upstream GitHub CLI release v" anchor (`.github/upstream-monitor/releases.json:113`), stay markdownlint-clean, name the manual command because the build context is not visible to users. | Name README :241 and :308 in synth-04; add the anchor and markdownlint constraints to the plan; add them to criterion 8. |

## Notes (MINOR)

- Gates 4 and 5 use 3 agents, not the BUILD-REQUEST's 2. SKILL.md lines 556 and 563 allow 3-4 above 1000 lines, and Builder Note 5 records it. No action.
- Step 2.1 says to use "help text via `bmad install --help`" but also "do NOT run `bmad install`". Say that `--help` is allowed, or read options from commands/install.js.
- `gaps-and-questions.md` is compiled at Step 3.14, before web research, and never refreshed; synth agents read "to be answered by web research" statuses that are stale by then.
- REPORT.md's observability follow-up (seedless boot prints "install ok"/"installed." and the /tmp log is truncated each boot) is not carried; it bears on what a user sees on first use.
- Line 105 edits the BUILD-REQUEST GOAL (drops `:133-144`) but is labelled as quoting it.
- Scope added beyond the notes (root README, CHANGELOG, SECURITY, `.github/workflows`, PROJECT_INDEX numbering check) is traceable to the project index. Not fabrication.

## Cross-validation results

- Covered: 5 research agents, 2 web agents, options A-F in synth-03, both owner questions (Open Questions 1 and 2 to Section 9), feasibility stop-condition (synth-03, synth-04, criterion 16, Step 3.14), `global_target_dir` no-consumer check (Steps 2.1, 3.2, synth-02 rule), test-57, test-startup-boot, test-46, test-19, test-49, test-52, catalogue README, OD-1 / memlog / SPEC documents.
- Spot-checked against files: test-57:448-452, install.sh:18,24,42,58-60 all match the notes.
- Phase order is sound (research, gate, gaps, web, synth with synth-04 after synth-03, assembly, gates).
- No Ponytail research: only the exclusion statements at lines 133 and 586; other hits are the worktree path.
- No installer run is instructed; line 128 forbids it.

VERDICT: FAIL (3 blocking: 3 IMPORTANT, 0 CRITICAL; 6 MINOR notes)
