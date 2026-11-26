# Task 3 draft wording (evidence only; no test reads this file)

Applied to `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, lines 168 to 172 of the pre-change file. The `advice-3-b.md` bullet (line 168) already states the prefix rule correctly and is left as it is. Two blocks change: the "Every GPT adviser" bullet (line 169) and the "Escalation 2" paragraph (line 172).

## Replacement for the bullet at line 169

- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model: the first T1 id (the id of `T1Model01`, else `T1Model02`) that starts with `gpt-` and is not the executor's own id, else the same T1 model.

Why this wording: the old bullet gave "`T1Model01` when the executor is not already on it, else `T1Model02`, else the same T1 model", which equates `T1Model01` with a GPT model. In the observed workspace `T1Model01` is a Claude id and `T1Model02` is the GPT id. The new bullet keeps the same selection order and the same fallback to the same model, but picks by the `gpt-` prefix rule of the `advice-3-b.md` bullet instead of by variable name.

## Replacement for the paragraph at line 172

Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example, described by the family of each id and by rung position: an executor whose id starts with neither `claude-` nor `gpt-` gets adviser A on the top rung and adviser B on whichever of the Claude top rung and the GPT T1 model is not adviser A's family; a Claude executor below the top rung gets adviser A one Claude rung up and adviser B on the GPT T1 model; a GPT executor gets adviser A on the GPT T1 model and adviser B on the Claude top rung; escalation 2 is then 2 on the top rung in each case. Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`. Worked example with the fallback ladder:

Why this wording: the old example called an executor on `T2Model02` a Claude executor and named `T1Model01` as the GPT T1 model. In the observed workspace `T2Model02` is neither family and `T1Model01` is a Claude id. The new example follows the escalation structure of lines 167 and 168 unchanged (adviser A one rung up in the executor's family, or the top rung when the executor is on top, neither-family or unknown; adviser B from the other family; escalation 2 on the top rung), adds no spawn and no rule, and states the launch rule once with the exact sentence the plan requires.

## Rules check

| Rule | Where met |
|---|---|
| GPT T1 model picked by the prefix rule; executors and picks described by family and rung position, not a fixed variable name | bullet at line 169 (prefix rule, no variable named as the executor's rung); paragraph at line 172 (no executor named by variable) |
| Escalation structure unchanged; no new spawn or rule | paragraph keeps A one rung up in the executor's family (top rung when on top, neither-family or unknown), B from the other family, escalation 2 on the top rung |
| The exact sentence, once | paragraph at line 172: "Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`." |
| Lead-in kept as the last words before the table; the four rung names reachable; the `T2Model01` sentence untouched | paragraph ends "Worked example with the fallback ladder:"; line 162 untouched |
| No `halt`, `Ruling`, `claude-gw-tier`, no new line starting `GPT spawn path: `, no model-id literal | none present in the new text |
