# Coordinator follow-up message (verbatim)

Received by the worker during /sc:workflow on 2026-11-04 (Orca message id msg_a922e035c5d2, created 2026-11-04T16:22:04Z, from the coordinator terminal). Saved here so the plan's scope expansion has a recorded source (reflect finding M-01).

Subject: Retry still skipped summary.md: name the files explicitly

> New evidence for your fix: the protocol's one retry of issue-worker-t2 on #365 used a spawn prompt that stated the input-file exemption explicitly. It then wrote .dev/issues/365/accuracy-check.md but still did NOT write .dev/issues/365/summary.md; the claim stopped with E-WORKER-NO-OUTPUT. The harness line names 'summary' files directly, so a general statement is not enough. The rule you add must name the exact files each worker writes (scout.md, accuracy-check.md, summary.md, analysis/, flags.md, flags-user.md, flags-t1.md, issue-body.md, draft-notes.md), state that writing them with the Write tool is mandatory and that returning their content as text is a failure, and sit early in each agent file (for example right after the opening paragraph), not only in Rules. Consider whether SKILL.md's spawn rule should also tell the orchestrator to restate this in every spawn prompt; that is your plan's call, and if you add it, test it.
