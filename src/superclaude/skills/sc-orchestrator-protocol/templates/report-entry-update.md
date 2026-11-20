<!-- template-note: The entry of one orchestrated issue in the living work report (waves 0, 3, 4, 5, 6, 7, 8).
     The step copies this file first (stub first) and fills it in place. It follows the report skill's
     `item-template.md` part for part, and adds the header block below, which the report scripts read.
     `{{name}}` is filled by a script or by the orchestrator from a file it read. `{{RF_PLACEHOLDER:name}}` is
     written by the model. The step deletes this note. Every part is written every time, "N/A" where a part has
     nothing to say; one-line parts are one or two plain sentences; "Done, with evidence", "Still to do" and
     "What happened since the previous report" are bullets only. The entry is updated at a milestone (plan done,
     blocked or asking, pull request opened, review rounds summarized, pull request ready, merged) and on no
     other worker message or CI change. Where this entry holds an escalation, the part "Needs you" carries the
     lines of `escalation.md` in this issue's own entry and no separate section is written for it. -->
<!-- ORCHESTRATED HEADER: read by the report scripts. -->
**Follow-up state:** {{follow_up_state}}
<!-- One of: working, question, gated, delivered, claimed-missing, stalled, failed, not-started. -->
**Human assignee:** {{human_assignee}}
**Orchestrator:** [{{orchestrator_tag}}](orca://session/{{orchestrator_session_id}}) ({{orchestrator_tier}})
<!-- While the orchestrator is down this line reads "no live session: {{reason}}" followed by its tier. -->
**Agent session:** [{{session_title}}](orca://session/{{session_id}}) ({{worker_tier}})
<!-- While the worker is not running this line reads "no live session: {{reason}}" followed by its tier. -->
**PR and CI state:** {{pr_ci_state}}
**Last update:** {{last_update}}
**Kind:** {{kind}}
<!-- One of: orchestrated, info:<stream>. -->

<!-- ITEM -->

#### {{identifier_link}}: {{title}}
{{RF_PLACEHOLDER:state}} · {{priority}} · {{change}}

**Opened by:** {{author}} · **Assigned to:** {{assignees}} · **Owner:** {{owner}} · **Board:** {{board}}

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
  <!-- What the user must do on this item (answer, review, approve, decide), or "N/A". An escalation here
       carries the lines "Why this reaches you:", "Low-stakes options:" and "If you do not answer:" of
       escalation.md. -->
- **ClickUp tasks:** {{clickup_links}}
- **Agent sessions:** {{session_lines}}
- **Why this priority:** {{priority_why}}
  <!-- Filled by script when a priority is set. When none is set, the status line's priority reads
       "Suggested {{RF_PLACEHOLDER:suggested}}" and this part is the model's one sentence naming the protocol
       rule that fits. -->
- **How I know:** {{RF_PLACEHOLDER:how}}
  <!-- What was read and its limits. -->
