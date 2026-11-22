<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (default model) -->
<!-- Merge date: 2026-11-11 -->

# Recommendation: should /sc:brainstorm spawn Orca processes instead of sub-agents?

<!-- Source: Base (original, modified) - verdict added at the top as the merge instruction requires; built from the base Claim, Changes 1 to 3 -->
## Verdict

Do NOT refactor the brainstorm skills to call Orca. Keep the Task sub-agent fan-out inside the command. If you want separate processes, a live view, other model families or crash survival, get them from the coordinator layer: a coordinator session you open runs one `/sc:brainstorm --unattended` worker per Task (see "Where Variant B's benefits are available without refactoring").

Both debate advocates reached this independently. Four secondary points stayed open (C-002, C-004, C-008, C-009) and do not change it. Size labels below (Small, Medium, Large) are rough, not time or money estimates.

<!-- Source: Variant B / debate A-004, C-003 (Change 1), replacing base Case point 3 "two dispatch paths forever" (Base, modified: wrong reason) -->
## The layering rule

Task fan-out stays in the command. Orca fan-out belongs to a coordinator session the person opened. The worker contract (`~/.claude/WORKER-CONTRACT.md`) says so:

- WC-7: a command's own Agent-tool fan-out "stays as it is".
- WC-8: "A command never calls `worker-start`, `dispatch` or `task-create`".
- WC-13: the worker session never does either.
- Its fan-in rule names "N workers, then `/sc:adversarial --compare`".

So the skill would hold no Orca code. That means Variant B as written (`worker-start` inside the skill, behind `--runtime orca`) cannot ship, and the earlier worry about maintaining "two dispatch paths forever" does not apply. Both advocates rejected in-skill spawning at 90%. The reasons B's other claims fail are in "Claims rejected".

<!-- Source: Base (original, modified) - skill names added to the file:line cites for clarity; point 3 replaced by the layering rule (Change 1); numbering restarts -->
## Why the skills keep Task sub-agents

1. **The spawned work is small and text-in, text-out.** Advocates run with `max_turns: 5` and get text inputs (`sc-adversarial-protocol/SKILL.md:1021-1028`). Variant generation is one prompt over a seed brief (`sc-adversarial-protocol/SKILL.md:2211-2218`). A full Claude Code session per proposal is more machinery than the work needs.
2. **Blast radius.** Parallel dispatch (S2 to S5) lives in `sc-adversarial-protocol` (2985 lines), which roadmap, troubleshoot, reflect and spec-panel also call. Brainstorm alone owns only S1. Rough size of a refactor: the shared adversarial skill Large, the brainstorm skill Medium, the other primitives Small, plus a new reference file.
3. **Lost guarantees.** Task returns results inline and reports usage. The hard-kill rule (`1.25 x estimate`, `sc-brainstorm-protocol/SKILL.md:240`) and `token_usage.wave_3` ("measured from Task notification", `:371`) depend on it. The Orca help text shows no token field (UNVERIFIED whether one exists elsewhere), and counting transcript size does not satisfy the 1.25x rule. Known Orca failure modes add risk: a `turn_started` receipt is not proof of work, and resumes need a screen check.
4. **Cost.** Each worker boots a full session and loads this user's large global CLAUDE.md, hooks and memory. That is unmeasured (see the measurement gate in "What to do instead").

<!-- Source: Variant B points 2, 3, 4 and debate A-001 (agreed 80%), Change 2 -->
## Where Variant B's benefits are available without refactoring

The unit to spawn is the whole command, not each proposer or advocate. A coordinator session runs one `/sc:brainstorm --unattended` worker per Task. The Task fan-out stays inside that worker. WC-10 accepts the resulting heartbeat gap. `/sc:adversarial` also has `--unattended` and `--report-dir`.

- **Context isolation.** Each worker writes files and a `return-contract.yaml` on every outcome (WC-4), with handoff files (WC-15). The coordinator holds paths. It opens the result file itself, because Orca does not check it (WC-4). Inside one run, `Skill sc-adversarial-protocol` still runs in the worker's own session, so debate, scoring and merge text stay in that worker's context.
- **Observability and control.** Orca shows each worker live, and `worker-stop` stops one without killing the others.
- **Retry and resume.** Under WC-6 a failed worker is retried as a NEW Task that carries a resume note. `--retry-of` is not used.
- **Status of the `--unattended` section (UNVERIFIED on master).** The installed `~/.claude/commands/sc/brainstorm.md` has an `## Unattended mode` section (7 matches). `src/superclaude/commands/brainstorm.md` on branch `docs/409-orca-dashboard-designs` has none (0 matches). Whether master has it is UNVERIFIED. Until the source copy has it, this route is not usable from this checkout.

<!-- Source: Base point 6 replaced with Variant A point 6, Variant B point 1 and debate C-004 (Change 3); C-004 stayed unresolved, lean A -->
## Cross-family model diversity: two routes

The real weakness is that "multi-model" brainstorm today is three Claude tiers (opus, sonnet, haiku): one vendor, correlated blind spots. Two routes fix it. C-004 stayed open, leaning toward Route 1.

### Route 1: sc-bare-review (no Orca)

`sc-bare-review` already dispatches to external models through an OpenAI-compatible proxy. Whether it can generate proposals is UNVERIFIED: it is described as producing reviews.

### Route 2: a coordinator, one worker per model family

Orca `worker-start --agent codex|cursor|opencode --model <id>` runs other model families. A coordinator runs one worker per family, then `/sc:adversarial --compare`. Whether a non-Claude worker can run `/sc:` commands is UNVERIFIED.

<!-- Source: Base (original) bullets 1 and 3, spec defects (U-001); Change 4 appends the measurement gate (debate A-003, agreed 80%); bullet 2 Base (original, modified): now points to the two routes -->
## What to do instead

- Keep Task dispatch inside the brainstorm skill.
- If cross-family diversity is wanted, try Route 1 first, after confirming it can generate proposals (UNVERIFIED).
- Fix two spec issues found during review. The `sc-brainstorm-protocol/SKILL.md:238-239` token thresholds (500K/650K, 80K per proposal) disagree with `refs/agent-spec-builder.md:146-153` (250K/350K, 8K per proposal). The command file says "5-wave" while listing six steps.
- Measurement gate: before any decision to use workers for brainstorm, measure worker cold-start time and cost. Neither variant has latency or cost numbers.

<!-- Source: Debate X-001, X-002, A-004, C-005; Variant A U-001; Variant B points 4, 5, 6 and mitigation (Change 5) -->
## Claims rejected

| Claim (from Variant B unless noted) | Why it fails |
|---|---|
| `--runtime orca` flag on S2, `worker-start` inside the skill | Violates WC-8 and WC-13 (A-004, 90%) |
| "S2 to S3 failures today can only be retried whole" (X-001) | False: a single failed advocate is retried once, then N-1 proceeds (`sc-adversarial-protocol/SKILL.md:1065-1072`) |
| Staged S2-only plan keeps the parent context small (X-002) | The skill runs in-session, so debate, scoring and merge still pass through the parent |
| Retry one worker with `--retry-of` | WC-6: every retry is a new Task, `--retry-of` is not used |
| `--resume-from` reattaches to finished proposals | `--resume-from` resumes only the seed brief today |
| Token accounting by transcript size or word count | Does not satisfy the 1.25x kill rule (C-005, 78%) |
| Merge enrichment into each proposer (point 5) | Low value, and it uses the same mechanism WC-8 forbids |
| Variant A: "two dispatch paths forever" | Void: the skill would hold no Orca code (A-004) |

Left open, not decisive: C-002, C-004, C-008, C-009.
