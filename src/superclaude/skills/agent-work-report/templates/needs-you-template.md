<!-- One "Needs you" entry: one agent session that has stopped with its work not done and is waiting on Clay
     to answer a question, approve something or unblock it (CLAY, 2026-11-05: "agents that are currently
     stopped and not completed that need me to do something"). Nothing else goes here: an assignment, a pull
     request review, a ClickUp ask or a design question stays in its item's own "Needs you" part. An entry is
     made for every session whose status is "waiting on you", and for no other. Bullets only, never a
     paragraph (CLAY, 2026-11-05); each bullet one or two plain sentences starting with a capital letter. The
     page shows every bullet with no click, and the ClickUp DM and the session summary carry the heading and
     every bullet but the options. check.py fails an entry whose heading does not start with its session's
     link, whose session is not waiting on you, that does not link the issue or pull request the session works
     on, or that lacks a bullet, the three escalation lines (`Why this reaches you:`, `Low-stakes options:`
     and `If you do not answer:`, spec 5.6) included. An issue the orchestrator holds has no entry here: its
     escalation lines are part of its own entry in the item's "Needs you" part. -->
### [{{session name}}](orca://session/{{session id}}): {{what the session needs from you, in a few plain words}}
- **What it is:** {{the linked issue or pull request the session works on, and what that work is, in plain words}}
- **Where it stands:** {{what the session did, and where it stopped}}
- **Question:** {{the exact thing it waits on you for, in plain English}}
- **Why this reaches you:** {{one row of the escalation table, in words, with its number}}
- **Low-stakes options:** {{the numbers of the options a typed bare number may answer, or "none"}}
- **Options:**
  - **{{option}}:** {{what choosing it does}}
- **Recommendation:** {{my recommendation and why}}
- **If you do not answer:** {{what stays blocked until you answer; never a default, a timer or "will proceed"}}
- **Answer on:** [{{where}}]({{link}})
