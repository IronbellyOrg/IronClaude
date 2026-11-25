# Position A: Keep Task sub-agents (harden, do not re-platform)

## Claim
Do not refactor /sc:brainstorm to spawn Orca processes. The current design already gives parallelism, per-agent model choice, and a clean return contract. The refactor cost is high and most of the benefit is available more cheaply.

## Case
1. **The spawned work is small and text-in, text-out.** Advocates run with `max_turns: 5` and receive their inputs as text (`SKILL.md:1021-1028`). Variant generation is one prompt over a seed brief (`SKILL.md:2211-2218`). A full Claude Code session per proposal is far more machinery than the work needs.
2. **Blast radius.** Parallel dispatch lives inside `sc-adversarial-protocol` (2985 lines), which other commands also call. Changing S2-S5 changes roadmap, troubleshoot, reflect and spec-panel behavior too. Brainstorm alone owns only S1.
3. **Portability.** CLAUDE.md requires installed primitives to work in other projects. Orca may be absent there. Every Orca path therefore needs a Task fallback, so we maintain two dispatch paths forever.
4. **Lost guarantees.** Task returns results inline and reports usage; the hard-kill rule (`1.25 x estimate`, `SKILL.md:240`) and `token_usage.wave_3` depend on it. Process workers return through files and polling, so the budget guard needs a new design. Known Orca failure modes (receipt is not proof of work, resumes need screen checks) add real operational risk.
5. **Cost.** Each worker boots a full session and loads this user's large global CLAUDE.md, hooks and memory. For 3 proposals plus 3 advocates plus rebuttals that is many cold starts.
6. **Real gap is narrower than it looks.** The one genuine weakness is that "model diversity" is three Claude tiers. That can be fixed without Orca (see `sc-bare-review`, which already dispatches to external models through an OpenAI-compatible proxy, per the skill listing).

## What to do instead
- Keep Task dispatch.
- Add optional external-model proposers via the existing bare-review mechanism if cross-family diversity is wanted.
- Fix small spec issues found during review: the `SKILL.md:238-239` token thresholds (500K/650K, 80K per proposal) disagree with `refs/agent-spec-builder.md:146-153` (250K/350K, 8K per proposal), and the command file says "5-wave" while listing six steps.
