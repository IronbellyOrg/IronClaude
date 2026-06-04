# Agent 2 — Intra-agent comms & handoff: agent-mail vs .md vs prompts

## STEP-0 Finding (source-grounded)

Handoff today is prompt-injection of directory PATH refs only plus a one-line CONTINUE/HALT result file. The richer content handoff functions exist but are dead code with test-only callers. No mailbox infra.

**Source evidence:**

- `process.py:147-167`
- `process.py:257-385`
- `executor.py:1076-1115`
- `pipeline/process.py:134-143`

## Options

### mailbox

**Pros:**
- typed payloads and addressing enable swarm
- ordering and ack make lost messages detectable

**Cons:**
- highest cost none today
- killed agent loses in-process messages unless persisted first

_Best when:_ only swarm with durable sends

### md

**Pros:**
- crash-survivable
- mtime ordering without a broker

**Cons:**
- unstructured without schema
- parallel writers race

_Best when:_ best floor surviving a killed subprocess

### prompt

**Pros:**
- zero marshalling
- cheapest to enrich

**Cons:**
- captures nothing upward
- no fan-in across siblings

_Best when:_ best downward leg quick win

## Roadmap Proposals (3)

### Lean  `[lean]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1 inject content | wire build_task_context into build_prompt | round-trip and dropped-result warn-continue |

### Moderate  `[moderate]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1 per-task bus | versioned envelope plus seq-ordered index | ordering concurrency lost-message |

### Robust  `[robust]`

| Phase | Goal | Test strategy |
|---|---|---|
| P1 swarm pilot | mailbox write-through plus flagged swarm | chaos kills no silent loss recovery |

## Recommendation

Start Lean: the richest handoff functions are built but unwired. Markdown-on-disk is the durable floor since it alone survives a killed subprocess. Prompt-injection is the downward leg, pair with disk. Mailbox only as an ack veneer over the disk bus at the swarm stage, never standalone.
