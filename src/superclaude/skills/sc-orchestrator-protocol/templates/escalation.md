<!-- template-note: One escalation (wave 5 and any wave), written by `superclaude orchestrator escalate`.
     The step copies this file first (stub first) and fills it in place. `{{name}}` is filled by a script or by
     the orchestrator from a file it read. `{{RF_PLACEHOLDER:name}}` is written by the model. The step deletes
     this note. The text becomes lines of this issue's own entry in the living work report, in that issue's
     section: no separate section is written for an orchestrated issue. An entry names exactly one row of the
     table below. When in doubt, a case does not reach the user: decide it, record what you decided and why in
     the entry ("Decided by the orchestrator: ..."), and go on. Quoted data in a fence headed "Quoted from the
     issue" or "Quoted from the worker" is skipped by the naming scan; nothing else may name an agent or a
     model. -->
## Escalation: {{issue_link}}

**Row:** {{row}} of the table below (old rule: {{old_rule}})
**Question key:** {{question_key}}
**Decision needed:** {{RF_PLACEHOLDER:decision}}
<!-- One sentence. -->

### The nine rows

An entry names exactly one row. This table is the only list of what reaches the user.

| Row | It reaches the user when it needs | Covers | Old rule |
|---|---|---|---|
| 1 | their own identity | acting or speaking as them where only they can; contact with anyone outside Ironbelly; signing in somewhere as them | rule 1 |
| 2 | a secret | a key, token or login that only they hold or can create or rotate; any request to write a secret anywhere | none (new) |
| 3 | money | spend; pricing; billing; anything that commits money | rule 1 |
| 4 | a legal act | a contract, terms, a filing, a signature, a compliance statement | none (new) |
| 5 | something that cannot be undone, or that changes shared settings | publishing or tagging a release; deleting a shared branch; a force push; a repository settings change; deleting a skill or an agent that the issue does not name | rules 1 and 2 |
| 6 | other people's access or data | giving, removing or changing anyone's access; reading or changing their data | none (new) |
| 7 | a breaking change | a change that the issue, the pull request or a review finding calls breaking: something other people or other systems rely on stops working | none (new) |
| 8 | a decision only they can make | a rule, priority or trade-off that changes what the product does; a scope that creeps into peripheral features beyond the issue's plan; a question still unanswered after the issue, the code, the docs and a web search; merging over a failing check; a pull request that changes a merge-safety file; an audit finding on a merged pull request that leaves the result possibly broken or unreviewed (merged over a person's change request, merged with an unresolved thread, or conflict markers in the merge): revert, or accept | rules 3, 4, 5 and 6 |
| 9 | them because it is stuck and nobody else can unstick it (a stop, not a decision) | a worker that the check-in, the typed key and the approval did not unstick the same day; a failed handoff; a pull request held because a listed review agent never ran or finished; a merge that their rights or the repo's protection forbid; a pull request with a change request still open; a pull request closed without a merge; a closeout that is unclear or failed twice; a hand-back that reached its bound of rounds | rules 7 and 8 |

### How it reaches the user

All three, always, and none is a separate list for an orchestrated issue:

1. Lines of this issue's own entry in the living report, in the section of this issue.
   Needs you entry: {{needs_entry_status}}
   <!-- Value: written. -->
2. An Orca decision gate, where an answer is needed; it is resolved only after a recorded answer from the user.
   Orca gate: {{gate_id}}
3. The notice: a ClickUp message from the report skill, or, when it cannot be sent, an unread mark on the orchestrator's workspace with a note.
   Notice: {{notice_status}}
   <!-- Value: ClickUp DM sent, or: DM failed, Orca unread mark set. -->

### The entry

**Question:** {{RF_PLACEHOLDER:question}}

**Why this reaches you:** {{RF_PLACEHOLDER:why_reaches}}
<!-- One row of the table, in words, with its number. -->

**Low-stakes options:** {{RF_PLACEHOLDER:low_stakes}}
<!-- The numbers of the options that may be answered by typing a bare number, or "none". An option is
     low-stakes only if choosing it is reversible and touches only the orchestrator's own work. No option of
     rows 1 to 7 is ever low-stakes. -->

**Options:**
{{RF_PLACEHOLDER:options}}
<!-- Every option, numbered, with one line on what it does. -->

**Key facts, with evidence:**
{{RF_PLACEHOLDER:facts}}

**Recommendation, and why:** {{RF_PLACEHOLDER:recommendation}}

**What happens after each answer:**
{{RF_PLACEHOLDER:after_each_answer}}

**If you do not answer:** {{RF_PLACEHOLDER:if_not_answered}}
<!-- Say in plain words what stays blocked and what keeps going ("Issue 12 stays held and no worker starts;
     issues 14 and 15 continue"). Never name a default action, a timer or something that "will proceed". Nothing
     that needs the user is decided for them. -->

**Links:** {{RF_PLACEHOLDER:links}}
