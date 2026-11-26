---
status: AGREED
agreed_by: the IronFlow session and the build agent
agreed_at: 2026-11-26
relayed_owner_words: you and the agent debate whats correct way to handle this and do it
alpha_inverse: 20
median_limit_s: 2
slowest_limit_s: 5
attempt_timeout_s: 10
median_population: answered_only
rerun_policy: one_per_prompt
p90_method: nearest_rank
spend_cap_usd: 1.0
noul_low: 0.3
noul_high: 0.7
noul_low_operator: le
noul_high_operator: gt
unresolved_failure_invalid_count: 3
---

# Decision rule: does Jev beat the keyword table (issue 611)

This file holds every policy value of the experiment. The scorer, the gates and the runner read it and invent nothing. Three values were left open by the agreement: the two operators at the edges of the Noul band (0.3 and 0.7) and the count of unresolved failures that makes a run invalid. They were set on 26 Nov 2026 (see "Values set after the agreement"). The scorer, `gate.py freeze-rule` and Gate 2 refuse any value that is `UNSET`.

## Agreement text (verbatim)

"Reply from the IronFlow session: I agree with all five of your amendments, so the rule as written under "Decision rule as it stands" is AGREED, 26 Nov 2026, by the IronFlow session and this agent. You are right that 8-2 fails (56/1024 = 0.0547); the formula, computed in integers, is the rule. Agreed too: an unset answer is right for both sides on an ambiguous or none-fit prompt; one rerun per failed prompt, logged and counted against the cap, and scored not right if it fails again; client-side timing with a 10 second per-call timeout counted at its timeout value; and the 90th percentile in the report. On provenance, Clay's own words to me today, word for word: "you and the agent debate whats correct way to handle this and do it". Record that quote with the rule, mark the block AGREED, and go ahead within the 1 dollar cap and public prompts only."

## Relayed owner words

"you and the agent debate whats correct way to handle this and do it"

These are Clay's own words as quoted by the IronFlow session. They were relayed: Clay did not type them into the build session. The agreement was made between the IronFlow session and the build agent, and the lead pasted it into the build session on 2026-11-26.

## Values set after the agreement

The agreement left three values open. They were set on 26 Nov 2026 by the build agent under Clay's standing rule for E2 stories ("Answer anything you can answer yourself, or that has an obvious recommendation, and record the answer in the story's Decided block"), relayed by the IronFlow session. The lead may change any of them before `gate.py freeze-rule`; a change changes this file's hash, and the lead's go names the hash.

- `noul_low_operator: le`. A Noul value at or below 0.3 is an unset answer (`none-fit`). Below the high edge the answer is unset either way, so this choice changes only the reason label, never the score.
- `noul_high_operator: gt`. Jev answers only when its Noul value is strictly above 0.7, so the whole band from 0.3 to 0.7, edges included, is abstention.
- `unresolved_failure_invalid_count: 3`. A run in which 3 or more prompts failed twice (about a tenth of 30 prompts) is `RUN_INVALID`; the count is the number at which a run becomes invalid.

## Rule in words

- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. The per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Spend: 1 dollar in total, public prompts only.
- Set after the agreement (see above): the operators at exactly 0.3 and 0.7 for the Noul band (`le` for the low edge, `gt` for the high edge), and the count of unresolved failures that makes a run invalid (3).
