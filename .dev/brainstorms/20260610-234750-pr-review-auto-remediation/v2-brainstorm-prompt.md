# V2.0 Brainstorm — paste-ready prompt (run in a parallel session)

Paste this single line into a fresh Claude Code session (it's one line so it pastes cleanly):

```
/sc:brainstorm "V2.0 of the PR auto-remediation system (V1.0 spec: @/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-requirements.md). V2.0 is a MENTION-TRIGGERED headless remediation bot, NOT automatic. Trigger: a user (or anyone authorized) replies to a comment on a GitHub PR and @-mentions the bot with free-form instructions. A server-side/headless process detects the mention, extracts the mentioned/parent comment body as opComment, and runs a headless 'claude -p' session executing e.g. /sc:troubleshoot \"${opComment}\" --depth deep --fix, where opComment is the original Augment-Code (or any) comment text being replied to. The headless session proposes, validates, implements, pushes fixes to the PR branch, and replies to the thread. Design the execution host (GitHub Actions workflow vs detached daemon vs webhook listener), the mention-detection + comment-parsing pipeline, AUTHORIZATION (who may invoke the bot — repo-collaborator allowlist), command-injection / prompt-injection safety on the untrusted comment body passed into claude -p, headless auth + secrets handling, the autonomy/approval model, and loop-safety. Reuse the V1.0 severity rubric, fork-only --repo IronbellyOrg/IronClaude targeting, and reply-to-thread+resolve mechanics. Out of scope: re-deriving V1.0's in-session monitor." --depth deep --strategy enterprise --handoff none
```

## Why these flags
- `--depth deep` — V2.0 is genuinely novel (headless host, untrusted-input → `claude -p`,
  authz, prompt-injection); it warrants the full deep dialogue + adversarial debate.
- `--strategy enterprise` — security/devops/architect-heavy persona set; enterprise implies
  deep debate. The security surface (arbitrary comment text → headless agent with push rights)
  is the crux and deserves adversarial pressure.
- `--handoff none` — produce merged requirements first; decide tasklist/task afterward.

## Reference architecture for the host (grounded prior art)
Anthropic's official `code-review` plugin runs **in CI** via `anthropics/claude-code-action@v1`
on `pull_request: [opened, synchronize]`, installing plugins through `plugin_marketplaces` +
`plugins` and invoking a skill from the action's `prompt` input. V2.0's headless host should
**start from `claude-code-action@v1`** (mention-triggered variant) rather than a bespoke daemon.
The brainstorm prompt above already says "GitHub Actions vs daemon vs webhook" — weight the
adversarial debate toward the Actions path given this first-party precedent.

## The single most important thing V2.0 must solve
Passing an **untrusted PR comment body** straight into `/sc:troubleshoot "${opComment}" --fix`
inside a headless `claude -p` that can **push code** is a command-/prompt-injection sink.
Anyone who can comment on (or fork-PR into) the repo could attempt to steer the agent. The V2.0
brainstorm MUST center authorization (collaborator allowlist), input sanitization, and a
constrained tool/permission surface for the headless session.
