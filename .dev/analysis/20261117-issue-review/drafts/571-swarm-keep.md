@clayphi Owner decision on swarm, replacing my earlier comment above that recommended removing it (given in chat 2026-11-17):

**Keep swarm in 6.0.0, together with the skills attached to it. Drop PR 3 (3a and 3b) from the removal list.**

The owner's note: "I was unaware of how much swarm had been integrated into this recent work. It is a valuable engine for multi-model workflows that we should keep. If we are keeping it, we may as well keep the other skills that are attached to it."

**What stays:** `src/superclaude/cli/swarm/` (engine, the 8 lenses, the recipes, tmux and TUI), `/sc:swarm-wizard` and the `sc-swarm-wizard-protocol` skill, the `sc-bare-review` skill, `docs/swarm`, `tests/swarm`, and the swarm CI jobs (`swarm-marker-matrix`, `boundary-guard`).

**Why (checked on origin/master; I did not run tests):**
1. **It is the engine under the review panel.** `cli/reflect/ensemble.py` (lines 41-61) imports swarm's `dispatch_wave1`, `normalize_wave2`, `reduce_wave3`, `emit_done_sentinel`, the transports, `preflight`, `config` and the `reflect_review` lens; its docstring says the Tier-2 path "invokes the swarm run surface". `cli/reflect/fallback.py` (lines 15-28) and `_diversity.py:5` use it too. The panel is where the last two weeks went (#519, #581, and the open #520 and #531).
2. **It does what Claude subagents cannot.** It sends one prompt to several models from different vendors through an OpenAI-compatible proxy, then normalizes and merges the answers, with resume and a return contract.
3. **Moving it is the riskiest step in the release.** Your measured table gives PR 3 as 218 files deleted and 41 edited outside swarm, and 3a would edit reflect while reflect is under active work. The move only exists because swarm is being deleted.
4. **The headless-Claude reason does not apply.** This plan says swarm does not launch headless Claude; it calls models through the proxy. The only reason left for removal was cleanup.
5. **Cost of keeping it is low.** About 12 commits touched it in five months, the last standalone change was the 2026-10-20 cleanup, and it stays a frozen backlog area. #540 stays open as backlog (the other swarm QA findings, #555 and #557, I did not re-check).
6. **Its extras are cheap once the engine stays.** The wizard, `sc-bare-review` and the other lenses sit on the same engine, so deleting them saves little. I found no other in-repo user of them, but I have no usage data, so that is UNVERIFIED.

**Effect on the plan (for Clay to apply):**
- Remove PR 3a and PR 3b. PR 4 onward keeps its numbers or is renumbered, Clay's call.
- G8 check (c) (`swarm-marker-matrix` and `boundary-guard.yml` no longer name swarm) and check (e) (reflect and issue_watch tests after the swarm decoupling) no longer apply.
- `sprint/aienv.py` still imports `swarm.config`; that is only a problem if PR 11 removes sprint while swarm stays, so PR 11 must keep or move `T2_MODEL_ENV_PREFIX` and `T2_MODEL_MAX_SLOTS` use correctly. Please check this one in step 2.
- The retire step (PR 12) must not list swarm items among the removed names.
- Wave 1 (PRs 1, 2, 5) is unaffected and stays approved.

Posted by Claude Code on the owner's instruction, 2026-11-17.
