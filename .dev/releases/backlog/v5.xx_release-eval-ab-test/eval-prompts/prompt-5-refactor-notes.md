# Prompt 5 Refactor Notes

## Date: 2026-03-19

## Change Applied: Explicit Rate-Limiting / Stagger Interval

### What changed

Added two operational directives to Phase 1:

1. **Launch stagger schedule**: Agents now launch at T+0s, T+30s, T+60s, T+90s instead of simultaneously. The phase heading was updated from "Spawn 4 parallel eval runners" to "Spawn 4 eval runners (staggered launch)" to signal the behavioral change.

2. **Rate-limit recovery protocol**: Added explicit retry instructions -- exponential backoff starting at 30s, max 5 retries, with logging. Agents that exhaust retries are marked FAILED and remaining agents continue.

3. **Context section alignment**: Updated the Pipeline Architecture bullet from vague "staggered, not simultaneous" to specify the 30-second stagger interval, ensuring context and prompt instructions agree.

### Why this improvement was selected

Of the three improvements evaluated via adversarial debate, this one had the highest impact-to-risk ratio:

- **Highest impact**: Rate limiting is the most probable operational failure mode. Four `roadmap run` invocations spawning ~10 Claude subprocess calls each (40 total) will reliably hit API rate limits if launched without pacing. This is not theoretical -- it is the expected behavior of the Claude API under burst load.

- **Lowest risk**: The change adds ~8 lines of text to the prompt. It does not alter the prompt's structure, output paths, or dependencies. The 30-second interval is framed as a minimum, not a rigid constraint, so it adapts to different API tiers. The retry protocol is standard engineering practice.

### What was rejected and why

1. **Staggered worktree creation with locking**: Rejected because git's internal lock file mechanism handles concurrent `worktree add` reliably, and the proposed fix (write to worktree-local paths, copy back after completion) introduced a new failure mode and significant prompt complexity.

2. **Content-discriminator tests in scoring framework**: Adopted in debate but ranked second. While valuable, the adversarial review in Phase 3 already targets this gap ("measures v3.0 changes vs generic health?"), providing a safety net. The rate-limiting fix addresses a failure mode with no existing safety net.
