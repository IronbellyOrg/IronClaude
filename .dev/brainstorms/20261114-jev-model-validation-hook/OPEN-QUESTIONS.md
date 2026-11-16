# Model-policy hook (version 1): open questions and decisions left (2026-11-15)

## Context for someone arriving with no history

**The problem.** IronClaude is a framework of commands and hooks for Claude Code. The owner has a standing rule: the most expensive model tier (Opus, `claude-opus-5-5`) is reserved for blind scoring and judging; everything else uses Sonnet or Haiku (and never Fable or any Tier 0 model). During a long evaluation on 2026-11-13 and 2026-11-14 that rule lived only as a sentence in the conversation, so nothing checked it, and about 4.2 million Opus output tokens were spent on brainstorm, design and implementation sessions. A second case was found on 2026-11-15: a Sonnet-launched `/sc:workflow` session ran its plan review with opus-class reviewers and debaters chosen inside the command's own protocol, which a check on the launch command alone would have missed.

**What the owner asked for (version 1).** Not a smarter model choice. Only this: **the model that was requested or defined is always the model used, and any attempt to use a different one is rejected.** Choosing the best, fastest or cheapest model for a job is **version 2** (may use a small judgment model, "Jev"), for places configured for dynamic choice. No version 2 issue exists yet.

**Where things are.**
- Incident and requirements: IronClaude issue #546 (https://github.com/IronbellyOrg/IronClaude/issues/546), with a comment dated 2026-11-15 recording the second case.
- Follow-up with the restrictions the hook would impose and where it is wanted: issue #551 (https://github.com/IronbellyOrg/IronClaude/issues/551).
- The version 1 design (a brainstorm, not a design document): `merged-requirements.md` in this folder. It has 63 numbered requirements, an 8-step plan and a list of unverified facts (its section 10). Four layers: a floor in the platform's own settings, one deterministic hook (no Jev call), one in-process helper that the Python launchers call, and a detective check after the fact. Observe mode first, except a literal forbidden model, which is blocked from day one. Nothing is implemented.
- Other files in this folder: `seed-brief.md`, `enrichment/codebase-context.md`, `proposals/proposal-{A,B,C}.md`, `nested/adversarial-1/adversarial/` (debate rounds and tallies). The adversarial session timed out before its merge; a second session finished the merge from saved artifacts, so the convergence score of 1.0 is the debate script's own tally, not an independent check.

**Rules for anyone working on this.** Push only to the fork `origin` (IronbellyOrg/IronClaude), only when the owner asks; never touch `SuperClaude-Org`. Edit under `src/superclaude/` and run `make sync-dev`; never stage `.claude/` paths other than `.claude/settings.json`. Python through `uv`. Open pull requests only with `/sc:pr-submit --monitor 3`. Implementation goes through a written plan (`/sc:workflow`, then `/sc:implement`), not ad hoc edits.

## Owner decisions recorded November 16, 2026

These decisions were given by Ryan during the November 16 review. They supersede conflicting recommendations in the historical table below. This update records decisions only; it does not implement or enable a hook, change policy/configuration, run an evaluation, or claim runtime validation.

| Item | Owner decision | Remaining boundary |
|---|---|---|
| 1 | Approved evaluation scripts may select from their declared model list. Block unknown or mistyped models, selections outside that list, and known models used outside permitted stages. The principal concern is agents spawning models. | A variable/table-driven selection is not itself forbidden. The exact approval mechanism and implementation remain to be designed. |
| 2 | An unattended job proceeds within its pre-approved job, model, stage and budget scope rather than stopping for live approval mid-run. | This does not authorize expanded scope or settle grant expiry, interruption or resume semantics. |
| 3 | An explicit user's model choice in an interactive session overrides ordinary agent model policy. | Do not infer expanded permissions for agent-spawned children or an override of unrelated security controls. |
| 4 | If a subagent's inherited model cannot be determined, run without that inheritance check. | This is not removal of the other model/list/stage checks. |
| 5 | When a launch omits the model needed for its job or stage, automatically fill in the most appropriate model for that job. When required information or files are unavailable, use the user's default model as fallback; apply this logic to applicable open questions. | Preserve known stage requirements and existing restrictions. No specific default model was named, and conflicts between a stage requirement, default, declared evaluation list or other restrictions were not resolved. |
| 6 | Protect installed policy files while allowing normal edits to repository source files. | This narrows the tamper-protection boundary; it does not authorize changing installed policy or implementing protection. |
| 7 (policy-file availability only) | If the model-policy file is missing or unreadable, continue with a warning. Apply the default-model fallback above where the required information/files are unavailable. | Missing `jq`, oversized scripts, hook timeouts and other failure cases in item 7 remain undecided; do not generalize this answer to disabling every guard. |

Ryan decided that the model policy applies uniformly by default everywhere IronClaude is used. Configurable developer strictness is a possible future option, not part of the current scope. This settles the uniform default; it does not approve an implementation or remove the previously recorded explicit-user and pre-approved-job exceptions.

Ryan also approved starting the safeguard in observation mode. This records the rollout-mode decision only; his answer did not separately approve the proposed immediate blocking of explicitly forbidden models, and does not authorize implementation.

Items 8, 9 and 11 remain open, along with the unresolved portions and boundaries above. Item 10's scope is superseded by the uniform-default decision above; configurable developer strictness is deferred. The version 2 issue and exact child-stage inheritance/logging mechanism also remain open. No code or policy implementation is authorized by this decision-record update.

Ryan suggested that a decision model such as Jev may suit this job. Assess that possibility only; this is not approval to integrate Jev, make model calls or implement a change. The existing version 1 no-Jev design remains the historical baseline pending assessment and a further decision.

## Original decision questions and design recommendations

The table below preserves the November 15 proposal for context. It is not a statement that the decisions recorded above are still unanswered.

These are the restrictions the design would impose on legitimate work (full text in #551). For each: keep, narrow or drop.

| # | Restriction | Why it matters | Recommendation of the design |
|---|---|---|---|
| 1 | Models that are not in a tier table (for example `gpt-6-luna`, `muse-ember-1.0`) are denied, and launchers that take the model from a variable are denied as "dynamic" | It would block the multi-model evaluation harness itself | Give every model the harness uses a tier; allow table-driven launchers by a grant tied to the script's hash |
| 2 | Approving a restricted tier needs a typed `yes` at a real terminal, and the agent's shell has none | Unattended runs cannot be approved; they stop | Decide whether a pre-approved, time-limited grant file made by the owner is enough |
| 3 | A person's own `/model` or `/sc:` command could be blocked if the prompt event fires | The rule is meant to constrain agents, not the owner's explicit choice | Do not block the owner's own switch; unverified whether the event fires at all |
| 4 | Subagent calls that name no model are blocked in a session whose start model is unknown (for example after `/clear`) | Noisy in ordinary use | Allow with a log line, or record the model another way |
| 5 | A launch with no `--model` is blocked when the stage requires one | Scripts that rely on the default break until pinned | Accept, in observe mode first |
| 6 | The "tamper" rule blocks edits to the policy, grants, settings, the hook and its installer in every mode | It would also block maintainers and the implementing agent editing those files in this repository | Narrow the match to the installed locations, or give the owner a bypass |
| 7 | Fail-closed paths (missing `jq`, oversize script, unreadable policy, hook timeout) block launch-shaped commands | A broken policy file stops all model-choosing calls | Keep, documented |
| 8 | Scanning (second pass, one-level script scan) may block scripts that only mention a launch | False positives | Observe mode first; measure before enforcing |
| 9 | A fifth hook process on every Bash call | Latency (target: 95th percentile at most 50 ms; unmeasured) | Measure before rollout |
| 10 | Project files may only tighten the policy | Project owners cannot loosen it themselves | Intended |
| 11 | The check is by requested name, not by the model actually served; the gateway can serve a different model behind an id | Over-trusting it is a risk | State the limit; use the platform floor and the after-the-fact check |

Also open: should a **version 2** issue (dynamic routing, may use Jev) be opened now, and should the policy cover children started by skills and commands (the second incident) through an inherited stage variable and per-source logging in observe mode?

## Facts nobody has checked (cheapest check in section 10 of `merged-requirements.md`)

- Does the platform's prompt-submit event fire for `/model` and for typed `/sc:` commands?
- Does the hook's environment equal the session's (alias values, stage variable)?
- What does the platform do when a hook runs past its timeout?
- Does exit code 2 block a prompt, or only the JSON form? Is the hook's stderr shown to the person?
- Is the Bash tool ever given a terminal? (Observed once: no.)
- Can `--settings` inject a per-child list of allowed models?
- What the gateway serves behind each model id (the Haiku alias has answered as `gpt-6.1-sol` on this host; `claude-gw-tier3` is unmapped).
- Whether the existing literal-check tests scan `.json.example`; how the installer merges one command registered four times.
- All latency figures are estimates.

## Next steps once the owner decides

1. Record the decisions above in #551.
2. Run the cheap checks on the unverified facts (the design's step 1) and record the results.
3. Write the design document, then a checked plan (`/sc:workflow`), then implement (`/sc:implement`) in observe mode with the always-enforced cases.
4. After 7 days of logged would-block events, enforce class by class as in section 8.4 of the merged file.
