# V15 Byte-Anchor Snapshot (NFR-2 reversibility reference)

- **Captured:** 2026-06-09 (Step 1.1)
- **task-start `git rev-parse`:** `015e7285`; **NFR-2 / Phase-6 POST `<BASE>` (real pre-my-edits HEAD):** `ab2dae1a`
  (a second sibling commit `ab2dae1a` landed at/after task start; both touched SKILL.md but NEITHER altered this item's body).
- **Source (live @ `ab2dae1a`):** `src/superclaude/skills/task-builder/SKILL.md:2019-2024` — the sibling's **halt arm**
  item, which is BYTE-IDENTICAL to the pre-sibling legacy POST item captured in research
  `01-post-gate-anatomy.md` Surface 5 (pre-sibling `:1994-1999`). (Verified byte-identical ×3 by the rf-qa post-sibling
  re-gate §3: `diff` empty/exit-0 vs this snapshot AND vs research 01.)
- **Drift note:** Sibling `015e7285` relocated this item `:1994-1999`→`:2014-2019` (wrapped under a
  `**Halt arm (POST_REFLECT_MODE: halt / unset — default):**` subheading); sibling `ab2dae1a` pushed it a further +5 to
  `:2019-2024`. NEITHER altered one byte of the item body. The **Phase-5 V15 diff must target live `:2019-2024`.**

## Verbatim byte-anchor (6 lines: header + Context + Action + Output + Verification + Completion gate)

```text
- [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING` to this file's frontmatter, then STOP and surface this paste-ready command for the operator to run in a NEW session: `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` — where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset), `{DEPTH}` is floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`), and the spawned reflect agent uses the default subagent model. The gate command uses `/sc:reflect` and never the `sc:task` execution command.
  - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command surfaced for a fresh session.
  - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect` command. The item does NOT self-resolve.
  - **Completion gate**: Operator has run `/sc:reflect --mode post` in a fresh session and recorded its verdict (`reflect_post: {verdict, run_id, report}`) in frontmatter. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

## Byte-exactness requirements (NFR-2 / V15)

- Title keeps "Independent post-execution **reflection** gate (**fresh session**, HALT)" (full word "reflection").
- Em-dash `—` (U+2014) in title and Action.
- `[--spec {SPEC_PATH}]` square-bracket-optional syntax.
- `<BASE>` angle-bracket literal (operator substitutes) — distinct from §6.3 Mode-2 `{BASE}` curly-brace.
- `{DEPTH}` floored-at-standard clause "per O4 (the POST gate NEVER runs `--depth quick`)".
- HALT clause cites `feedback_human_decision_items_must_halt`.
- `2-degraded-halt` variant: appends EXACTLY one `<!-- wrapper-absent: degraded from Mode 2 -->` comment to the Context; gate text otherwise byte-identical.
