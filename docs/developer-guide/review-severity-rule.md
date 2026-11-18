# Review Severity and the 2-Fix-Cycle Cap (Design Note)

This note explains the review rule IronClaude applies to every review loop (it came in with 5.0.0): how findings are graded, how many fix cycles a loop may run, where the rule is written, how it reaches every agent, which protocol keeps its own model, and the static test that stops the old wording from coming back. It is for maintainers who write or change a review gate in a command, skill, agent, template or CLI pipeline. It was written for 5.0.0 and re-read at tag v6.0.0: the wording of the grading bullets (S1, S2, S5) and the guard test changed after 5.0.0. Every line number below is from tag v6.0.0, except those into 5.0.0 records (`docs/releases/v5.0.0.md`, `.dev/releases/current/v5.0.0/DECISIONS.md`).

For the user-facing summary, see the 5.0.0 release notes, "Change 4: review loops stop after 2 fix cycles" (`docs/releases/v5.0.0.md:212-214`).

## Contents

1. [The rule](#the-rule)
2. [Decisions behind it](#decisions-behind-it)
3. [How the rule reaches every agent](#how-the-rule-reaches-every-agent)
4. [Where the rule applies](#where-the-rule-applies)
5. [The `/sc:implement` exception](#the-scimplement-exception)
6. [The guard test](#the-guard-test)
7. [Open questions](#open-questions)
8. [Changing the rule](#changing-the-rule)

## The rule

The source of truth is five bullets in the Pragmatic output style, `src/superclaude/output-styles/pragmatic.md:240-244`, placed right after the binary-verdict bullet ("Every review agent MUST produce a binary verdict: PASS or FAIL", `pragmatic.md:239`). The guard test calls them S1-S5 by position. In 5.0.0 they were lines 225-229.

| # | Rule (as of 6.0.0) | Line |
|---|---|---|
| S1 | Grade every finding as blocking or minor, by what changes if the flawed text is corrected. A finding is blocking only when one of three holds, and the finding says which: Decision (correcting the text would change a named decision, recommendation, required behaviour, acceptance check or quoted number that something rests on), Missing (a required deliverable, section or step is absent in substance) or Safety (following the text would lose or expose data or a secret, break a safety boundary or act outside the declared scope; never downgraded). | `pragmatic.md:240` |
| S2 | Minor findings never fail a review. They are recorded as notes, the verdict is PASS (with notes), and work proceeds. A real defect in substance that nothing named rests on is Medium; a defect of form only (wording, formatting, a wrong label or line number on a true statement) is a Note. The label a reviewer used is information, not the grade. Only blocking findings produce FAIL; Medium and Note findings are not rechecked in later rounds and never start a fix pass. | `pragmatic.md:241` |
| S3 | A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalates to the user with the open blocking findings. Never a fourth review, never a pass with open blocking findings. | `pragmatic.md:242` |
| S4 | A protocol that defines its own severity model, such as `/sc:implement`, applies that model and its own escalation path. | `pragmatic.md:243` |
| S5 | On a CRITICAL / IMPORTANT / MINOR scale the label is information, not the grade: grade by the rule above, so an IMPORTANT finding that is only wording is a Note. A finding whose consumer cannot be established keeps the reviewer's own label and is tagged `consumer-unknown`. | `pragmatic.md:244` |

5.0.0 graded by a shorter definition (blocking was "a real defect"; minor was "cosmetic"). The three-reason definition, the Medium and Note levels and `consumer-unknown` came later. Other bullets near S1-S5 changed too. Before the verdict bullet, "review from an adversarial position" and "a review with zero issues is suspect" were replaced by "review as an independent reader" and "a zero-finding result is valid, and must say what it checked" (`pragmatic.md:236-237`). After S5 two bullets were added: Medium findings are listed as follow-up candidates and the user is asked once per run whether to open an issue, and the `/sc:spec-panel` scale (`pragmatic.md:245-246`). The guard test pins only S1-S5, by position and opening phrase.

What a loop looks like under S3:

```text
review 1 -> FAIL (blocking) -> fix 1 -> review 2 -> FAIL (blocking) -> fix 2 -> review 3
                                                                              |
                         PASS (maybe with minor notes) <------- no blocking --+-- blocking still open
                                                                                   -> HALT, escalate to the user
```

## Decisions behind it

The rule was a 5.0.0 release blocker decided by the user and recorded in `.dev/releases/current/v5.0.0/DECISIONS.md:12-19`. The evidence was the QA-loop investigation: long review loops came from "any finding of any severity fails" rules with no round cap (`docs/releases/v5.0.0.md:187`).

| Decision | What it settled | Line |
|---|---|---|
| B1 | A review that fails only on minor findings notes them and proceeds: no recheck, no FAIL. Every "any severity" rule is removed and review loops are limited to 2 rounds. At the cap with blocking findings open, stop and escalate; never pass them silently. | `DECISIONS.md:12` |
| B2 | "2 rounds" means 2 fix cycles, so at most 3 reviews (review, fix, re-review, fix, re-review), then escalate. Existing "Max 2 fix cycles" stay; "Max 3" and uncapped loops drop to 2. | `DECISIONS.md:13` |
| B3 | Inside `/sc:implement`, the second A2 in-place repair is removed (A1 review, fix, A2 re-review, one repair, re-review = 2 fix cycles). Retry-adviser attempts A3-A5, the halt contract, the saved reviewer prompt and FINAL are unchanged. | `DECISIONS.md:14` |
| B5 | When the rule's own plan hit the cap with 10 blocking findings, they were added and implemented without a fourth plan review, with a safeguard: one recorded search for every wording of the old rule (`.dev/review-severity-rule/site-sweep.md`), a static test that fails CI if any wording survives, and text anchors instead of line numbers in acceptance checks. | `DECISIONS.md:19` |

Decision R1 (`DECISIONS.md:17`) only replaced a stalled worker during the implementation; it does not change the rule.

## How the rule reaches every agent

- **Output style.** `superclaude install` copies `src/superclaude/output-styles/` to `~/.claude/output-styles/` (`src/superclaude/cli/install_user_setup.py:186-201`). A plain install keeps a file that already exists and names it when it differs from the shipped one; `--force` saves a differing file as `<name>.bak.<UTC time>` and then replaces it (`install_user_setup.py:68-109`, `install_keep.py:36-46`). An existing installation therefore gets the current rule only after `superclaude install --force`.
- **SubagentStart hook.** `src/superclaude/hooks/hooks.json:169-176` registers `node "$HOME/.claude/hooks/pragmatic-subagent.js"` (timeout 5 s) on SubagentStart, and `install_hooks.py:67-68` installs the script. The script reads `~/.claude/output-styles/pragmatic.md`, strips its frontmatter and returns it as `additionalContext` prefixed with `PRAGMATIC MODE ACTIVE` (`src/superclaude/hooks/scripts/pragmatic-subagent.js:7-18`). So every subagent, reviewers included, receives S1-S5 even when the parent session uses another output style.
- **Failure mode.** If the style file is missing or unreadable, the script writes `Failed to load Pragmatic instructions from <path>` to stderr and exits 1 (`pragmatic-subagent.js:19-21`); the subagent then starts without the rule. The hook needs `node` on `PATH` (`install_hooks.py:67`).
- **Copies in primitives.** Eleven tracked files carry S1-S3 word for word, and six of them also carry S5, so the rule holds where a primitive is read without the hook (for example by a CLI pipeline): `rf-qa.md`, `rf-qa-qualitative.md`, the QA agent and skill templates, both MDTM task templates, four legacy QA rule prompts, and (added after 5.0.0) `reflect-reviewer.md`, whose grade bullets a separate test pins (`tests/skills/test_review_severity_rule.py:181-204`, `:214-228`).

## Where the rule applies

The 5.0.0 changelog lists the scope (`CHANGELOG.md:278-282`, in the `[5.0.0]` section that starts at line 256). Representative sites:

| Area | What changed | Where to look |
|---|---|---|
| Pragmatic output style | S1-S5 replace "any issue of ANY severity fails" | `src/superclaude/output-styles/pragmatic.md:240-244` |
| rf-qa, rf-qa-qualitative, rf-analyst, rf-team-lead agents; QA and skill templates; both MDTM templates | PASS allows minor findings as notes; FAIL needs a blocking finding; fix agents receive, apply and recheck blocking findings only | `CHANGELOG.md:279`; copies pinned by `test_review_severity_rule.py:181-204` |
| prd, tdd, tech-reference, tech-research, readme, operational-guide, task, task-builder skills | Same rule; task-builder's gate passes with minor findings as notes and HALTs at the cap | `src/superclaude/skills/task-builder/SKILL.md:867,875` |
| At-cap behaviour everywhere | HALT and escalate the open blocking findings instead of turning them into Open Questions and proceeding | `CHANGELOG.md:280` |

## The `/sc:implement` exception

S4 exists for `/sc:implement`, which grades findings with its own model: the reviewer answers four factual checklist questions per finding, and the parent derives `blocking`, `minor` or `note` mechanically and reads each cited anchor back (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:37-56,81`). Inside `/sc:implement` that model takes precedence over the output style, including the copy the SubagentStart hook injects; only `blocking` findings may fail an attempt, halt or prompt the user (`qa.md:93`).

The 2-fix-cycle cap reaches it through decision B3: an attempt gets at most one in-place repair, and A2 gets one repair at most (`refs/retry.md:141-142`; `qa.md:267`). The retry-adviser attempts A3-A5 are unchanged (`CHANGELOG.md:33`). `tests/skills/test_implement_severity_static.py` pins this model and imports S1-S5 from the guard test (`test_implement_severity_static.py:12`); the guard test's old-cap check skips `sc-implement-protocol` files (`test_review_severity_rule.py:338-343`).

## The guard test

`tests/skills/test_review_severity_rule.py` is a static test over tracked text. CI runs it with the rest of the suite (the `Run tests` step, `.github/workflows/test.yml:40-47`). Run it locally with:

```bash
uv run pytest tests/skills/test_review_severity_rule.py -v
```

| Check | What fails it | Lines |
|---|---|---|
| (b) canonical bullets | S1-S5 missing, out of order, or not directly after the binary-verdict bullet in `pragmatic.md` | `66-107` |
| (a) any-severity wording | Phrases such as "any issue of any severity", "regardless of severity", "must still be fixed" in `src/`, `plugins/`, `commands/`, `agents/` | `112-176` |
| (c) copies | S1-S3 (and S5 where required) not verbatim in the eleven-file set; the `reflect-reviewer.md` grade bullets missing | `181-228` |
| (d) cap text | The canonical cap text or the at-cap HALT clause missing | `233-264` |
| (e), (j) edit tables | Any of the 140 cap-edit or 125 sweep-edit rows (counted by their `old:` keys; fixtures in `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml`) not applied | `279-301` |
| (f) old caps | A review-loop cap above 2 ("Max 3 fix cycles", "after 3 failed cycles", ...) outside `sc-implement-protocol` and two allowlisted lines | `306-357` |
| (g) verdict suffixes | "Only PASS or FAIL — no conditional pass." removed from the listed skills | `362-383` |
| (h) plugin twins | `plugins/superclaude/skills/sc-implement-protocol/` not byte-equal to `src/` | `389-403` |
| (i) site sweep | Old fix-loop wordings ("If findings exist", "logged for human review", ...) that would send minor findings to a fix pass | `408-482` |
| (k) zero tolerance | "zero tolerance" without a qualifier such as fabrication, verification or blocking | `487-538` |

## Open questions

These are known gaps or unclear intent, not rule violations. Each needs an owner decision.

- **`sc-cli-eval-protocol` "max 3 fix loops".** The create pipeline allows 3 fix loops for manifest loader errors before reporting blocked (`src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:213`; `refs/create-pipeline.md:50`). The guard test allowlists both lines as "not a review loop" (`test_review_severity_rule.py:312-322`); whether non-review fix loops should follow the 2-cycle cap is not decided.

## Changing the rule

1. Edit S1-S5 in `src/superclaude/output-styles/pragmatic.md` and keep each bullet's opening phrase, which the guard test checks (`test_review_severity_rule.py:69-75`).
2. Update the copies in the eleven-file set (`test_review_severity_rule.py:181-193`), and the edit-table fixtures if a pinned row changes.
3. A new review loop in any primitive states blocking versus minor, caps at 2 fix cycles, and HALTs with the open blocking findings at the cap. A protocol that needs its own severity model says so explicitly, as `/sc:implement` does (`qa.md:93`).
4. Run `make sync-dev`, `make verify-sync` and `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -v`.
5. Existing installations pick up a changed style only after `superclaude install --force` (see [How the rule reaches every agent](#how-the-rule-reaches-every-agent)).
