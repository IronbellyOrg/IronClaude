### Variant 1 Advocate (opus:architect) for OURS

## Position summary

The sweep JSON should be the single fact source, and the observer should be the single screen that reads it. Clay's work report should stay, but as the plain-English work-item layer on top of the sweep, not as a third collector. We adopt the nine-row table and the notice cap as policy now, because nothing built depends on them yet. The living report is adopted as a HYBRID, once it reads session facts from the sweep.

## Steelman of Variant 2

Clay's strongest argument is that his report is the only piece that already gives a person, per issue, a plain-English summary, what is done, what is left, whether it needs them, and a link. Issue 409 asks for exactly that. The sweep records its own gap here: issue 409 item 3 says "the sweep has no per-session summary text", and its Orca allowlist contains no GitHub call (M:src/superclaude/cli/sweep/probes.py:49-56). The report also has three solid safety properties:

- A script gate: `check.py` must pass before anything is delivered (M:src/superclaude/skills/agent-work-report/SKILL.md:24).
- No silent loss: "a failed read carries items, never closes them" (SKILL.md:21).
- A living page that is rebuilt "with no model call" (SKILL.md:16).

Our own paper concedes that the observer-sweep contract note does not exist. So Clay is right that waiting on paper would delay a tool that works today, and right that the nine-row table fills a gap. Our sweep only splits "waiting" by kind, with no list of reasons.

## Strengths claimed

1. **One fact layer with a fixed, read-only surface.** The sweep may call Orca only through a fixed list of command templates (M:src/superclaude/cli/sweep/probes.py:49-58). It uses no model, so it is the only one of the three that can run on the 5-minute cadence of rule WC-16 (M:src/superclaude/core/WORKER-CONTRACT.md:287). Two readers of the same sessions can disagree about a session's state, a risk that Clay's own paper names (variant 2, line 36). One reader removes that risk at its root.
2. **The keys needed to join a session already exist in the sweep.** The sweep's models carry `worktree_path`, a `session_id` on the transcript record, and a `TabMapEntry` linking `session_id` to `terminal_handle` (M:src/superclaude/cli/sweep/models.py:103, 131, 146-148). The report can therefore join on sweep rows instead of re-reading Orca. That makes "sit on top of" a real, buildable dependency direction, not a wish.
3. **The owner's rules are encoded where they matter.** The sweep "will not recommend anything, propose an action, or add advice" (M:src/superclaude/skills/sc-sweep-protocol/SKILL.md:61). The observer's questions panel turns on only against a recorded owner pass (M:src/superclaude/cli/observe/commands.py:63-67). Building the base on these keeps the owner's decided order of watcher, then orchestrator, then dashboard.
4. **The dependency direction fits the owner's own issue.** Issue 409's alignment item 1 says to read "the sweep's JSON, not a second collector" (variant 1, line 14). Clay's direction, where "the sweep and observer feed or read it" (variant 2, line 9), would make a skill tied to one person, which needs a model and writes to outside services, an upstream dependency of zero-token, read-only tools. That reverses the stability gradient: the most stable layer should sit at the bottom.
5. **The notice policy agrees with the owner's standing rule.** "When in doubt, a case does not reach Clay" (M:docs/designs/orchestrator.md:668) and "the cap never drops an entry" (orchestrator.md:686) match the owner's rule to show outstanding decisions only. So both can be adopted without conflict.

## Weaknesses identified in Variant 2

1. **A third collector.** `sessions.py` lists terminals and reads transcripts itself (scripts/sessions.py:1-28, cited in variant 1 line 21). This is a third Orca reader with its own six status words, beside the sweep's eight classes. Variant 2 admits the disagreement risk at line 36.
2. **Tied to one person and not zero-setup.**
   - `config.json` sets `"person": "clayphi"`, `"timezone": "America/Chicago"` and `"session_tag": "coordinator"` (M:src/superclaude/skills/agent-work-report/config.json:2, 6, 11).
   - The skill stops unless `AWR_ROOT` or `orchestrator_repo` is set (M:src/superclaude/skills/agent-work-report/scripts/common.py:35-45).
   - As a base layer for every user, this is a cost the sweep does not have.
3. **Writes and recommendations.** The report's notice is a ClickUp direct message (M:docs/designs/orchestrator.md:666), and its entries carry a "recommendation and why" (orchestrator.md:690). Clay's paper concedes these are "writes the sweep and observer rules forbid" (variant 2, line 37).
4. **Naming drift.** The skill text still says `/sc:orchestrator` and `.dev/coordinator/` (SKILL.md:12, 14). Clay's paper concedes these conflict with the owner's decisions on naming and folder layout (variant 2, line 32).
5. **The cap is not enforced by anything built.** The cap is enforced through the `escalate` verb and the file `asks.json` (orchestrator.md:684-686). Our paper verified that neither exists in master, pr-a or pr-p (variant 1, line 26). So the "settled" cap is text, not code.

## Concessions

- Our unification has not been delivered. `observe/` never reads the sweep, and the contract note has not been written since 2026-11-13 (variant 1, lines 20 and 37).
- Clay's report meets the issue 409 asks today. Ours meets them only after the Decision Desk is built, and it is "NOT BUILT".
- The sweep has no GitHub, ClickUp or summary text. That layer has to come from Clay's code (`collect.py`, `clickup.py`), and it is right to reuse that code rather than rewrite it.
- Clay's script gate and "carry, never close" rules are real strengths the sweep's report could learn from.
- Our paper said nothing about the living report (C-009) or about naming (C-010).

## Shared assumptions

- **A-001: QUALIFY.** A join key exists on our side: `session_id`, `terminal_handle` and `worktree_path` (M:src/superclaude/cli/sweep/models.py:103, 146-148). Neither paper fixes which key is the contract, so the contract note must name it.
- **A-002: QUALIFY.** We adopt the table's structure. Row 1 ("his own identity", M:docs/designs/orchestrator.md:672) and the other rows' "Clay" wording must be made about any user before the table applies stack-wide.
- **A-003: ACCEPT, with the cost stated.** The v1 key set is pinned by a golden test (M:docs/designs/orchestrator-mode.md:605), so adding fields needs a reviewed test edit, which is cheap but not free. The same file shows that additive v1 keys were planned from the start.
- **A-004: ACCEPT** that the assumption is false. `common.py:35-45` exits without `AWR_ROOT` or `orchestrator_repo`. The report is not zero-setup, which is one more reason it should not be the base layer.

## Per-point positions

| Point | Superior | Confidence | Evidence |
|---|---|---|---|
| S-001 | Variant 2 | 65% | Clay describes built code; ours is a partly unbuilt target (the contract note is missing). |
| S-002 | Tie | 50% | Both cite well: Clay on capability, ours on structural cost. |
| C-001 | OURS | 75% | One Orca reader removes the status disagreement; join keys exist (sweep models.py:146-148). The full-transcript read can stay as an enrichment step keyed on sweep rows. |
| C-002 | HYBRID | 70% | Keep Clay's GitHub and ClickUp code, but join it through the contract note, not a parallel stack. |
| C-003 | Variant 2 | 75% | Only the report meets the issue 409 asks today; the Decision Desk is not built. |
| C-004 | OURS | 80% | The sweep refuses to recommend (sc-sweep-protocol SKILL.md:61); the DM and recommendation are confined to the report surface. |
| C-005 | OURS | 70% | Person-specific config (config.json:2, 6); the sweep costs zero tokens. Clay's no-model `refresh` narrows the gap. |
| C-006 | Variant 2, adopted as HYBRID | 70% | Nothing in the sweep gives a reason list; the table gets generic wording before stack-wide use. |
| C-007 | OURS, on enforcement facts | 60% | The cap is written down (orchestrator.md:686), but `escalate` and `asks.json` are unbuilt. Adopt the value of 5 as policy. |
| C-008 | OURS | 70% | Eight proof-based classes with "could not determine" are the stable base; the report's six words should be mapped onto them. |
| C-009 | Variant 2, adopted as HYBRID | 70% | Entry files plus a no-model refresh (SKILL.md:16) are a real capability; feed them sweep facts. |
| C-010 | Variant 2, for honesty | 60% | Clay names the naming drift (SKILL.md:12, 14); the fix follows the owner's naming. |
| X-001 | OURS | 75% | The stable, zero-token, read-only layer belongs at the bottom; the reverse makes the base depend on a single-user skill that writes to outside services. |
| X-002 | Variant 2, in part | 55% | Do not freeze the working report; ship the contract note next, and let the report move to the sweep data afterwards. |
