# May v2 push corrections into sessions that are not Orca workers (owner question 15)

## Question in one sentence
Must the planned v2 knowledge layer ever send a course correction directly into a session that is not an Orca worker, or should it only report to you or the coordinator?

## Why you are being asked
Issue #423 (v2) says it should "relay them to affected agents". That would mean pushing content into sessions the current rules say are never messaged. The answer sets v2's design and decides whether the unbuilt trust layer becomes a v2 prerequisite. It is a trust-boundary call.

## Background you need
- Orca is the local agent-orchestration app. A worker is a session Orca starts for one task; a coordinator is the person-opened session that supervises workers.
- Other sessions: ones you start yourself, ones the issue watcher starts (they may run unattended), and ones with no Orca run.
- Today the coordinator corrects a worker only by leaving a message the worker picks up itself (rule WC-12). Person-started sessions "are never messaged".
- No known channel delivers a message into a non-worker session. Signing messages does not stop harmful content inside them.
- v2 is planned and advisory; nothing of it exists.

## Your options
1. **Report only, with a condition for ever reopening** (recommended)
   - If you pick this: v2 reports to you or the coordinator; for workers, the coordinator decides whether to send a follow-up. The question is reopened only once a channel, a threat model for harmful content, a rule on whether you approve each correction, and a shared grant vocabulary exist.
   - Upside: no new way into your sessions; no trust layer needed for v2; easy to widen later.
   - Downside: narrows #423's "relay to affected agents"; unattended watcher-launched sessions are never corrected automatically.
2. **Never, as a standing rule for every program**
   - If you pick this: same v2 behaviour, but written as a permanent rule for all future programs.
   - Upside: the strongest boundary.
   - Downside: binds future designs nobody has researched; reopening means overriding a standing rule.
3. **Yes eventually, behind the trust layer**
   - If you pick this: the first release reports only, but v2 plans to deliver into non-worker sessions once the #339 trust layer exists, which moves that unbuilt work onto v2's path.
   - Upside: keeps #423's purpose; could correct unattended sessions.
   - Downside: no channel is known; opens a way into sessions that are never messaged today; longer path.

## What the debate found
- All three advocates, asked what they would pick if unassigned, picked option 1.
- For every release actually planned, options 1 and 2 behave the same; option 1 avoids binding the future.
- The real gap is unattended watcher-launched sessions; it is recorded as an open case.

## Recommendation and confidence
Option 1, 82 percent.

## If you do not answer
Report only (the same v2 behaviour as option 1, without the reopening condition).

## What this answer does not authorize
No edit to issue #423 or to the worker contract, no new message channel, and no v2 work; each needs its own grant or answer.

## How to answer
Type: "Q15: option 1" (or "Q15: option 2" or "Q15: option 3").
