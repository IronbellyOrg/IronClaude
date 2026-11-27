# Table provenance

Completed by the build agent after the table was applied. Evidence file: `table/table-answers.jsonl` (30 rows).

- Method (one of: a person reading the prose, or executing the skill): a person reading the prose. The reader is an AI sub-agent (a general-purpose Claude agent, fresh context) that read the quoted table and the six application rules in `table/table-procedure.md` and applied them to each prompt by hand. It did not execute the skill. This is an AI reading the prose, not a human; that is a limit of the measurement.
- Source revision, the commit (`git rev-parse HEAD`): `8d0d73a120ca02327b1fa3a1f1353623c2d04541`
- Source revision, the blob of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` at that time (`git hash-object <that file>`): `76bcb3d94182371250ffe99a7b60b9124b05c368`
- Who applied the table (a name, or a session id): a fresh general-purpose sub-agent spawned by the build agent (Agent-tool task a7c5607bfc9074b53)
- Date applied (UTC): 2026-11-27T04:25Z
- The applier was a different person or session from the labeller (yes or no): yes. The labeller was the IronFlow session (Claude); the applier was a separate sub-agent with a fresh context. The build agent that started it had read the labels (it built `corpus.jsonl` from the filled sheet) and did not edit the sub-agent's answers.
- The applier received prompts only, with no label and no Jev answer (yes or no): yes. It was given only `/tmp/sc611/table-input/prompts.jsonl` (id and text for each of the 30 prompts) and a copy of `table/table-procedure.md`, was told to open nothing else, and reported that it opened exactly those two files. That the agent could not be mechanically stopped from reading other files is a limit; its own report is the evidence.
- Gate 1 had passed before the table was applied (yes or no, and the time of the `gate1` event): yes, `gate1` event at 2026-11-27T04:24:08+00:00 (`events.jsonl`).

## Only when the method was executing the skill

Not applicable: the method was a reading of the prose, not an execution of the skill.

- The copy that was loaded: not applicable
- The SHA-256 of that copy: not applicable
- The actual tool-loading trace or transcript that shows it loaded: not applicable
