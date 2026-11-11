# Prompt 00: dispatch probe (run first, in the live gateway session)

You are the coordinator of a model-evaluation run. Before any evaluation is spent, find out which models can actually be launched as sub-agents from this session and how.

Inputs: `p20/live-evals/combos.json` (its `models` list; skip `claude-opus-5-5` unless the owner approved it).

For EACH model id, do the following and record the result in `probe.json` next to this file:
1. Launch one sub-agent on that model with the mechanism available here. Try, in order, and record which one worked: (a) the Agent tool with `model` set to the gateway alias for the model's tier (the tier file's `alias`, for example `claude-gw-tier3[1m]`, or the plain alias `sonnet`/`haiku`/`opus` where the ccsession launcher remaps it); (b) a Bash call to the CLI with `--model <alias or model id>`; (c) any model picker entry the session offers. Never use Fable / Tier 0.
2. Give it this task and nothing else: "Reply with exactly two lines. Line 1: the name of the model you are running as. Line 2: the sum of 17 and 25."
3. Record `served_model` from the transcript or gateway log (what actually answered), not from the reply text alone, and the reply's second line.
4. Record `{model, mechanism, alias_or_flag_used, served_model, answer_ok, error}`.

A model counts as launchable only when the sub-agent answered `42` AND the served model matches the requested one (a silent fallback to another model is a failure, record it).

Also record, for the whole session: how many sub-agents can run at once without errors (try 4, 8, 12), and whether sub-agents can write files to a sandbox directory outside the repository.

Final reply: the path of `probe.json` and one line: `launchable: <n> of <m>; not launchable: <ids>; max parallel: <k>`. Do not start any evaluation.
