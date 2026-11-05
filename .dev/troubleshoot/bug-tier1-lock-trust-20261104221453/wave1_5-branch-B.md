# Wave 1.5 Branch B (architectural docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

| doc_path | currency_verdict | reason |
|---|---|---|
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md | unknown | :82-90 step 5 precheck, checkout --ours uv.lock, uv lock, uv lock --check, git add, with no pyproject read; :94 a uv failure aborts `sync_merge_failed`; :296 `sync_tier3` raised at steps 5-6 (Tier 2 escalation), Tier 1 not named |
| (same) section 4 | unknown | :46-52 Tier 3 HALT template at :50 "HALT (`<reason>`): merging `origin/<base>`@<base_sha> into `<HEAD_BRANCH>` needs a human decision. File <k>/<n>: `<path>` (`<class>`)..."; :52 intent sentences omitted when classification stopped before reading content |
| (same) sections 6, 9, 11 | unknown | :126-133 VAL runs `uv lock --check`, `uv run pytest`, `make test` on the merged tree; :223 abort when Tier 3 found mid-way or a uv failure; :271 prohibited operations list is git-safety only |
| src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md | unknown | :12 any stop condition aborts and halts `sync_tier3` with the Tier 3 template; Tier 2 only (:3, :9) |
| src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md | unknown | :175-178 conflict push authorized by `evaluate_sync_decision`; :179-181 Tier 3 never enters the FSM; silent on trust |
| src/superclaude/skills/sc-pr-submit-protocol/SKILL.md | unknown | :219 "1 also regenerate a conflicted root `uv.lock` (Tier 1)"; :275 fork head allowed only below L3; :309 Will Do; :311-320 Will Not Do (no trust item); :329-330 error rows for conflict_tier3 and sync_* |
| src/superclaude/commands/pr-submit.md | unknown | :54 `--conflict-max-tier` default 1; :28-30 STOP preconditions, no trusted-collaborator precondition |
| SECURITY.md | unknown | :456-475 general guidance; :467 "Use safe defaults and explicit opt-in for risky functionality" |

Placement: halt template conflict-mechanical.md:46-52; `sync_tier3` row :296 gains the Tier 1 step 5 pyproject trigger; the check sits in step 5 after the precheck and before `uv lock`, aborting through section 9 (:216-223); trust note in SKILL.md Will Not Do (:311-320) or near :219-221, mirrored in commands/pr-submit.md (:28-30 or :54), plus a line in conflict-mechanical.md section 6 (VAL also runs project tests on the merged tree).
