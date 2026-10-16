# QA Report: Fix Cycle 3 (final) for IronClaude Quick Guide (adversarial, report-only)

**Target:** `IRONCLAUDE-QUICK-GUIDE.md` (116 lines, read in full; not edited)
**Prior report:** `09-qa-fix-cycle-2.md` (open: R-F1b, N2, N3, N4)
**Source truth checked:** `IronClaude-tier-tools` (HEAD `50a8c7f4`, `git rev-list --left-right --count origin/master...HEAD` = `0 0`), its `src/superclaude/` and `.claude/` copies, `IC-Harness/.claude/`, the installed pipx `superclaude` 4.2.0
**Date:** 2026-10-01
**Phase:** fix-cycle
**Fix cycle:** 3 of 3 (final)

---

## Overall Verdict: FAIL

All four open items from `09` were applied word for word, and R-F1b, N2, and N3 are now correct against source. N4 was applied, but the wording `09` recommended for it is itself wrong: it tells the user to "confirm the tier it reports before it fans out", and neither `/tech-research` nor `/roadmap` reports a tier or stops for confirmation. That is 1 remaining issue (N5). Cycle 2 had 4, so the count went down and no `[HALT-MONOTONICITY]` fires. No regressions. This was the third and last fix cycle, so per the 3-cycle cap: **HALT and ask the user** how to handle N5 (apply the replacement below without another QA cycle, or authorize a fourth cycle).

## Prior Findings Status

| ID | Status | New guide text (quoted) | Verification |
|---|---|---|---|
| R-F1b | RESOLVED | Line 77: "Use levels 1 and 2 only from inside `IronClaude-tier-tools`, where they need no setup. In IC-Harness (June copy) they do not work: they stop with "probe first", and the code they need is not in your installed CLI (4.2.0). Always pass `--monitor`; the default is 2." Line 113: "Pushes on its own. Use 0; use 1 or 2 only inside `IronClaude-tier-tools`. No `--monitor` means 2." | Master `src/superclaude/commands/pr-submit.md:26,47` (default 2), `:37-39` (L1 = "arm + poll + propose (no edits)", L2 = "fix locally, HALT before push", L3 = push), `:66` ("No R1 probe is required"). The tier-tools `.claude/commands/sc/pr-submit.md` and `.claude/skills/sc-pr-submit-protocol/SKILL.md` are byte-identical to `src/` (`diff -q` silent). The previously unchecked item is now checked: inside tier-tools, `uv run python -c "import superclaude.pr_submit, superclaude.pr_submit.ci"` succeeds (resolves to `src/superclaude/pr_submit/__init__.py`), and `gh pr checks --help` lists `--json` (CI-wait preflight, master `SKILL.md:89-94`). IC-Harness: `.claude/commands/sc/pr-submit.md:29,61` ("run the R1 probe first", "fresh clone safely HALTs ("probe first")"). Installed CLI: `superclaude --version` = 4.2.0; pipx python `import superclaude.pr_submit` gives `ModuleNotFoundError`. |
| N2 | RESOLVED | Line 18: "at least 6 separate reviewers (3 structural, 3 content), then a fix and a re-check, repeated up to 3 times before it stops and asks you." | `IC-Harness/.claude/skills/task/SKILL.md:117` (minimum 6: 3 rf-qa + 3 rf-qa-qualitative, then Serialized Fix Protocol), `:254` (verification round after fix), `:256` ("repeat Steps 6-8 ... Maximum 3 fix cycles total ... HALT ... ask for guidance"), `:359,361` (same for post-completion). |
| N3 | RESOLVED | Line 31: "Same. Deep is picked on its own at this size; to force it, say "deep dive" or "thorough"". Line 42: "(Standard by default; Deep on its own for 20+ files or several subsystems, or say "deep dive" or "thorough")". | `IC-Harness/.claude/skills/task-builder/SKILL.md:132` (default Standard; large = 20+ files, multiple subsystems), `:138`, `:143` ("thorough", "comprehensive", or "deep dive": always Deep), `:145` (multiple subsystems: always Deep). Lines 128-148 identical on master (`diff` = SAME). |
| N4 | APPLIED, BUT THE APPLIED WORDING IS WRONG (now N5) | Line 32: "To get the Quick tier, say so explicitly and confirm the tier it reports before it fans out". Line 34: "For the document only (Quick tier) or document plus build requests (Standard tier), say so explicitly and confirm the tier it reports". | The default-deep and size-based parts are correct (`tech-research/SKILL.md:97,105-109`; `roadmap/SKILL.md:102,110-114`). The "say so explicitly and confirm the tier it reports" part has no source support. See N5. |

## Remaining Issue

### N5 (MINOR, introduced by the `09` replacement for N4). "Confirm the tier it reports before it fans out" describes a step that does not exist

- **Quoted text (line 32):** "To get the Quick tier, say so explicitly and confirm the tier it reports before it fans out"
- **Quoted text (line 34):** "For the document only (Quick tier) or document plus build requests (Standard tier), say so explicitly and confirm the tier it reports"
- **Problem:**
  - (a) **Neither skill reports the tier to you or stops for confirmation.** `/tech-research` picks the tier inside Stage A after scope discovery (`tech-research/SKILL.md:230` "Select depth tier (default: Deep)"), writes it only into `research/research-notes.md` (`:276` "**Depth Tier:**"), then goes straight on: A.5 gate, A.6 template triage, A.7 build request and `/task-builder`, then "Proceed directly to Stage B" (`:598-601`). The only user question allowed is about genuine intent ambiguity (`:213`). `/roadmap` is the same (`roadmap/SKILL.md:249,267,314`; `DEPTH_TIER` is copied into the build requests at `:603,647-650,1804`). The project's own rule 16 and line 10 of this guide ("it runs end to end") also say it does not pause. So there is nothing to "confirm" unless you interrupt it.
  - (b) **Fan-out can happen before the tier exists.** Scope discovery itself spawns parallel agents for inputs over about 1000 lines (`tech-research/SKILL.md:245-249`, "6000+ lines: 5-10+ parallel agents"), and the tier is chosen after that (`:229-230`). "Before it fans out" is not something you can act on.
  - (c) **Asking explicitly is not a documented switch.** There is no tier flag or override (`grep` for `--depth`, `--tier`, `argument-hint` in both SKILL.md files: no match). Only QA intensity has "Override allowed? Yes" (`tech-research/SKILL.md:113-121`, `roadmap/SKILL.md:118-126`). The documented way to get Quick is a genuinely narrow request: "Only use Quick for genuinely narrow questions ("what function handles X?")" (`tech-research/SKILL.md:108`) and "Only use Quick for genuinely simple requests ("plan how to add a single endpoint")" (`roadmap/SKILL.md:112`).
  - All cited lines are identical on master (`diff` of the "Depth Tiers" section to "Output Locations" in both skills: SAME).
- **Replacement (line 32, the whole parenthetical):** "(it defaults to deep and picks the tier itself from the question's size; there is no setting to force Quick, and it does not stop to show you the tier. The word "quick" on its own only lowers QA. For a small run, ask a narrow question, such as "what function handles X?")"
- **Replacement (line 34, from "defaults to deep" to the closing parenthesis):** "defaults to deep and many agents and picks the tier itself from the input's size; there is no setting to force the Quick tier (document only) or Standard tier (document plus build requests), and it does not stop to show you the tier. The word "quick" on its own only lowers QA)"
- **Check after applying:** line 110 ("the Quick tier gives the document only, and Standard adds build requests") stays correct and does not need to change; it describes what each tier produces, not how to choose one.

## Whole-Guide Read (lines 1-116)

| Check | Result |
|---|---|
| Line 77 vs line 113 vs line 115 (pr-submit levels, where they work) | Consistent: all three say use the newer behavior from inside `IronClaude-tier-tools`. |
| Line 18 (6-agent check) vs line 44 (lite still gets a 6-agent check per phase from phase 2 on) vs line 48 | Consistent with `task/SKILL.md:117-118`. |
| Line 31 / line 42 (task-builder Deep) vs line 43 ("4-8 researchers") | Consistent: Standard 4-5, Deep 6-8 (`task-builder/SKILL.md:136-138`). |
| Line 32 / 34 vs line 10 ("it runs end to end") | **Contradiction:** "confirm the tier it reports" implies a pause the guide itself says does not happen. Covered by N5. |
| Line 34 vs line 110 (roadmap tiers) | Consistent once N5 is applied. |
| Line 114 (tier words) vs line 17 | Consistent. |
| No other contradiction found. | |

## Dash Check

- `grep -n $'\xe2\x80\x94' IRONCLAUDE-QUICK-GUIDE.md`: exit 1 (no U+2014).
- `grep -n $'\xe2\x80\x93' IRONCLAUDE-QUICK-GUIDE.md`: exit 1 (no U+2013).
- The N5 replacements contain neither character.

## Summary

| Status | Count | IDs |
|---|---|---|
| Resolved | 3 | R-F1b, N2, N3 |
| Applied but wrong (replaced by new finding) | 1 | N4 (now N5) |
| New | 1 | N5 (MINOR; came from `09`'s own replacement wording) |
| Regressions | 0 | none |

- Remaining issues: 1 (cycle 2: 4; cycle 1: 5; cycle 0: 11). Strictly shrinking, so no `[HALT-MONOTONICITY]`.
- Fix cycles used: 3 of 3. Cap reached with 1 issue open: **HALT and ask the user.** Do not turn N5 into an open question.
- Issues fixed in place: 0 (report-only by instruction).
- For the third time, an error came from wording a QA report recommended (`08` for N2 and N4, `09` for N5). The N5 replacement makes only claims cited above; check it against those lines before applying.

## Confidence Gate

- **Confidence:** Verified: 4/4 prior items, 1 new finding with source lines, 6 whole-guide consistency checks, 2 dash greps, plus the `09` unchecked item (tier-tools `uv run` import) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (coverage of the review, not a quality score for the guide)
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 11 (sed, grep, diff, ls, find, git, gh, `uv run` and pipx python import tests, against the cited files) | Write: 1 | Edit: 4. No web research was performed. Read + Grep + Glob (2) is below the item count because the source checks were done through Bash `grep`/`sed`/`diff`; each Bash call targeted a specific cited line range.
- **Not checked:** whether the Augment bot is installed on `IronbellyOrg/IronClaude` (tier-tools origin), which level 1 needs to get a review at all. This does not affect any claim in the guide.

## QA Complete
