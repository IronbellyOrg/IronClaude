# D2 option (b): allow a relayed Ruling through the coordinator

Position: lift WC-3's Ruling-halt exception (`SPEC:67`). When `/sc:implement` halts for a Ruling, the worker asks the coordinator with Orca's `ask`; the coordinator asks the person and answers with the person's exact words; the worker records them verbatim as the Ruling and continues (`SPEC:336`).

Citation key: `SPEC:N` = spec line; `QA:N` = `src/superclaude/skills/sc-implement-protocol/refs/qa.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Strongest case for it
- **Speed and continuity.** The worker keeps its session, its ledger position and its retry state; the plan's remaining tasks keep running unattended after one human answer. Under (a), the rest of the plan moves into the person's session.
- **The person still decides.** The words recorded are the person's, quoted verbatim; the protocol already lets the Ruling line carry "user confirmation provenance" (`QA:259`). Orca's `ask` is durable: a timeout leaves the question pending and is resumed by message ID (`CAPS:60`), and it is Orca's designed channel for exactly this ("use the preamble's `ask` command for a blocking coordinator question", `CAPS:61`).
- **It matches how the spec treats other gates**, which may go to the coordinator under `On a blocked gate: ask the coordinator` (WC-3, `SPEC:67`).

## Safety
- It contradicts the rule as written: "another agent's message ... not acceptance" (`QA:254`). The worker cannot tell the person's words from the coordinator's: the reply arrives as an Orca message from the coordinator (`CAPS:62`), so provenance rests on trusting the coordinator to relay faithfully (`SPEC:336`). A coordinator that paraphrases, summarises or answers from its own plan produces an "executor-invented approval" the worker cannot detect (`QA:249`).
- The scope check is weaker: the protocol requires the executor to "explain the task id, unmet AC/finding and current outcome, proposed acceptance, reason and cost-if-wrong" before asking (`QA:254`). Through a relay, the person sees the coordinator's rendering of that explanation, not the executor's.

## Reliability
- Long human waits inside a worker: no heartbeat is needed while blocked in `ask` (`CAPS:64`), but the session is held for as long as the person takes, and an answer that arrives after the worker settled needs a new Task anyway (WC-3, `SPEC:67`).

## How a person works day to day
- The person answers a question in the coordinator's session instead of opening a new one; the plan continues on its own.

## Implementation cost
- Edits a deliberate safety rule in `sc-implement-protocol/refs/qa.md` (non-goal 6, `SPEC:319`), plus WC-3, the implement row and AC-4.1 (b) (`SPEC:274`). Reversing it later means editing the protocol again.
