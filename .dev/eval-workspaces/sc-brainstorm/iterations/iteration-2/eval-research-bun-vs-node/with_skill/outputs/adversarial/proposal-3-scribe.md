---
proposal_id: 3
persona: scribe
model: haiku
lens: policy clarity, decision documentation, stakeholder framing
---

# Proposal 3 — Scribe: The Deliverable Is the Decision Document, Not the Pilot

## Position

The other two proposals are arguing about *how* to pilot. I want to start one layer up: **what does the platform team actually deliver to the WebSocket gateway team in 6 weeks?** A pilot is a means, not an end. The end is a decision document that the WebSocket team can read, the engineering leadership can sign off on, and the next team (and the next, and the next) can use without re-running this debate. If the pilot is the work, the document is the artifact. Optimize for the artifact.

## What the artifact looks like

A single Markdown document, `docs/platform/runtime-allowlist.md`, with these sections (sketched, but the structure is load-bearing):

```
# Runtime Allowlist
## Current allowlist
| Runtime | Status | Conditions | Owner | Last reviewed |
| Node 20 LTS | allow | none | platform-team | 2026-Q1 |
| Node 22 LTS | allow | none | platform-team | 2026-Q2 |
| Bun 1.2.x | pilot-only-with-conditions | <see below> | <named individual> | 2026-Q2 |

## Bun 1.2.x: pilot-only-with-conditions
### Why this status (3 paragraphs, evidence-cited)
### Conditions for pilot proposal
### Conditions for graduation
### Conditions for removal
### Native-dep compatibility matrix
### Observability parity statement
### Revert playbook (link)
### Open questions

## Process to update
1. Service team proposes...
2. Platform team reviews...
3. Engineering leadership signs off if status changes...
```

This is what the analyzer's "evidence" and the architect's "governance" actually become when written down. A single document that any engineer can read in 15 minutes, and any platform team in the future can update with a PR.

## Failure mode 1: implicit policy

The biggest failure mode of runtime decisions is **the decision exists but nobody knows what it is**. The WebSocket gateway team comes back in 6 weeks asking "what's the answer?" If the answer is in a Slack thread, a planning doc, or a verbal "well, we talked about it," the next team will re-litigate. The artifact is the answer. Without it, this brainstorm produces no durable output.

## Failure mode 2: observability gap that hides degradation

(This is also the analyzer's R2 / NFR5 — flagging from a documentation-clarity angle.) The observability parity statement must be a *list*, not a paragraph. Specific instrumentations, specific status, specific shim links if applicable. If a future engineer reads "observability works on Bun" and ships a service that loses 30% of its traces because of a known gap that wasn't documented, that's a documentation failure, not a runtime failure. Mandatory enumeration.

## Failure mode 3: undefined removal trigger

If we pilot and the pilot reveals a problem, what gets us back to "disallow"? "We'll know it when we see it" is not a removal trigger. It must be specific: one SEV-2 attributable to runtime; one customer escalation traceable to a Bun-only gap; one native-dep regression that breaks prod. Documented in the policy. Otherwise the pilot drifts into permanent "still piloting" status, which is the worst of both worlds.

## Stakeholder framing

**For the WebSocket gateway team**: The policy says "pilot-only with conditions; you can apply to be the pilot, here's the rehearsal + evidence we need first." This is a yes-but, not a no.

**For engineering leadership**: The policy says "we are evaluating Bun in a bounded, reversible way; here's the risk register, here's the revert playbook, here's the cost; sign off on the pilot."

**For other service teams in Q3/Q4**: The policy says "Bun is in pilot; if pilot succeeds, expect general-allow in 2026-Q4; if pilot fails, expect disallow with documented rationale." Predictable, repeatable.

**For the next platform engineer**: The policy is the durable artifact. They don't need to remember any of this conversation. They read the doc.

## What I'd push back on

The architect's proposal is governance-heavy and underspecifies the deliverable artifact. The analyzer's proposal is evidence-heavy and underspecifies how that evidence becomes a *decision people can act on*. Both proposals are necessary inputs to the document I'm describing. The document is what the platform team actually owes the rest of the engineering org.

## Cost

The document itself is ~1 engineering day to write after the pilot data lands. The investment is making sure the pilot work feeds *into* the document — that the observability statement, native-dep matrix, and revert playbook are written as policy fragments from day one, not assembled at the end.

## What I want to see in the merged requirements

1. The deliverable is named: `docs/platform/runtime-allowlist.md` (or equivalent).
2. The structure is specified (sections enumerated).
3. The observability gap discipline is mandatory (enumerated list, not prose).
4. The removal trigger is specific (not "we'll know").
5. The next-review date is bounded (≤2 quarters).
