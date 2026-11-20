<!-- One item in the daily report: every GitHub issue or pull request, ClickUp task and agent session that is
     Clay's. The merge of the two formats Clay set (CLAY, 2026-11-04): the item card of his open-work page
     (state and priority, who opened it, who has it, owner, board, Next, what it asks for or does, current
     state, done with evidence, still to do, why this priority, activity) and this report's entry (linked
     identifier, what changed, what happened, recommendation, Needs you, ClickUp tasks, agent sessions, how I
     know). The page shows every part of it, as bullets, with no click (CLAY, 2026-11-05).
     Rules: every part, every time, "N/A" where one has nothing to say. One-line parts are one or two plain
     sentences. "Done, with evidence", "Still to do" and "What happened since the previous report" are bullets
     only, one point per bullet ("- N/A" when empty), never a paragraph. Every line starts with a capital letter.
     {{...}} is filled by script; {{RF_PLACEHOLDER:...}} is written by the model. For an issue the orchestrator
     holds, `run.py refresh` fills every written part from its entry file instead, and the header line also
     names the orchestrator (the `Orchestrator` line, 5.4). Each day render.py stubs every
     item from this file: an unchanged item gets yesterday's written parts back, a changed one gets them back
     with an update marker to work through, a new one gets empty slots; check.py fails any item that does not
     follow it. -->
<!-- PRIORITY PROTOCOL (CLAY, 2026-11-05; levels as in his open-work priorities). A priority set on GitHub (its
     board's Priority field or a priority:* label), on the ClickUp task, by Clay through the helper, or by
     Clay in the item's text or a comment always wins, and the script fills it in. Nothing goes without one
     (CLAY, 2026-11-17: ALL require it). An item with none gets a suggested level written here, from what the
     run files show about it; a level someone else wrote in the item's text or a comment (activity.md lists
     those lines) is that suggestion when it plainly gives this item's level, and "Why this priority" says who
     wrote it and when:
       Urgent: breaking daily work now, a data-loss or security risk, or a ready fix for one of those.
       High:   a defect hit regularly, a blocker for other planned work, or someone waiting on Clay to move.
       Medium: a useful improvement, or partly done with a defined remainder.
       Low:    idea stage, parked, blocked, or only needs closing or moving.
     For a suggested level the status line reads "Suggested <level>" and "Why this priority" says which rule
     fits, in one sentence. The report lists everything, "Needs you" included, by level (set or suggested),
     then within a level by state (Waiting on you first, then Needs work, Blocked, Waiting on others, In
     progress, Ready to merge, Not started, Can close, Done). -->
<!-- ITEM -->

#### {{identifier_link}}: {{title}}
{{RF_PLACEHOLDER:state}} · {{priority}} · {{change}}

**Opened by:** {{author}} · **Assigned to:** {{assignees}} · **Owner:** {{owner}} · **Board:** {{board}}{{orchestrator_part}}

**Next:** {{RF_PLACEHOLDER:next}}
<!-- The next step and who takes it, in one sentence. -->

- **What it is:** {{RF_PLACEHOLDER:what}}
  <!-- What it asks for (an issue or task) or what it does (a pull request or session), in plain words, not
       the title again. -->
- **Current state:** {{RF_PLACEHOLDER:state_text}}
- **Done, with evidence:**
  {{RF_PLACEHOLDER:done}}
  <!-- Bullets: each finished piece and where that shows (a merged pull request, a passing check, a file). -->
- **Still to do:**
  {{RF_PLACEHOLDER:todo}}
  <!-- Bullets: each open piece and who does it. -->
- **What happened since the previous report:**
  {{RF_PLACEHOLDER:happened}}
  <!-- Bullets: one event each, with who and when; "- Nothing since <date>." when quiet. -->
- **Recommendation:** {{RF_PLACEHOLDER:recommend}}
  <!-- My own judgment on what to do and why. -->
- **Needs you:** {{RF_PLACEHOLDER:needs}}
  <!-- What Clay must do on this item (answer, review, approve, decide), or "N/A". Only an agent session on
       this item that has stopped waiting on him also gets an entry in "Needs you" at the top of the report,
       led by that session's link (CLAY, 2026-11-05). An issue the orchestrator holds (it has an entry file in
       .dev/coordinator/orchestrated/) never gets an entry at the top: its escalation is written here, in its
       own entry, as the question, every option with one line on what it does, the key facts, the
       recommendation and why, and these three lines, in this order (spec 5.6): `Why this reaches you:` (one
       row of the escalation table, in words), `Low-stakes options:` (the numbers of the options a bare number
       may answer, or "none") and, after what happens after each answer, `If you do not answer:` (what stays
       blocked; never a default, a timer or "will proceed"). -->
- **ClickUp tasks:** {{clickup_links}}
- **Agent sessions:** {{session_lines}}
- **Why this priority:** {{priority_why}}
  <!-- Filled by script when a priority is set. When none is set, the status line's priority reads
       "Suggested {{RF_PLACEHOLDER:suggested}}" and this part is the model's one sentence naming the protocol
       rule that fits ("Leandro and Will are waiting on your review to start testing."). -->
- **How I know:** {{RF_PLACEHOLDER:how}}
  <!-- What was read and its limits. -->
