# Research (light): worker supervision prior art

## Method and quality tier

- **quality_tier: fallback_1.** The `sc:research-protocol` skill was not available in this session (Skill tool returned "Unknown skill"), so this used 12 WebSearch queries plus 3 WebFetch reads (Claude Code hooks reference, Temporal activity failure detection, Kubernetes probes). Date: 2026-11-07.
- Search-result summaries were used where no page was fetched; each claim carries its URL. Devin is not covered: no primary source was found (UNVERIFIED).

## Progress heartbeats with details (e.g. Temporal activity heartbeats and heartbeat timeout, Celery/Sidekiq)

- **Temporal** splits timers. The Heartbeat Timeout is the "maximum time between" heartbeats; missing it fails that attempt and the retry policy decides what runs next. Start-To-Close bounds one attempt, and Schedule-To-Start bounds queue wait ([Temporal docs](https://docs.temporal.io/encyclopedia/detecting-activity-failures)).
- Heartbeats carry **details** (progress payloads). A retried attempt must read the last details itself to resume; resume is not automatic ([long-running activity pattern](https://github.com/temporalio/documentation/blob/main/docs/design-patterns/long-running-activity.mdx), [TS API](https://typescript.temporal.io/api/namespaces/activity/classes/Context)). The SDK throttles heartbeats, so some work repeats after a retry ([community thread](https://community.temporal.io/t/activity-restarts-from-beginning-of-the-processs-on-heartbeattimeout-and-on-acitivitynotexistsexcpetion/8225)).
- Cancellation reaches an activity only "when they Heartbeat": the heartbeat is also the control channel back to the worker ([Temporal docs](https://docs.temporal.io/encyclopedia/detecting-activity-failures)).
- **Celery**: with `acks_late`, a task still gets acknowledged when its child process dies. Redelivery needs `task_reject_on_worker_lost`, and the docs warn about crash loops ([Celery tasks guide](https://github.com/celery/celery/blob/main/docs/userguide/tasks.rst)). On Redis or SQS, a task that runs past `visibility_timeout` can be delivered again while it is still running ([Celery Redis docs](https://docs.celeryq.dev/en/latest/getting-started/backends-and-brokers/redis.html), [Airflow Celery provider](https://apache.googlesource.com/airflow/%2B/HEAD/providers/celery/src/airflow/providers/celery/get_provider_info.py)).
- Sidekiq: not researched (UNVERIFIED).

## Liveness vs readiness vs startup probes (Kubernetes) and what maps to agent sessions

- **Liveness** catches a "deadlock, where an application is running, but unable to make progress". After `failureThreshold` consecutive failures the kubelet kills the container. **Readiness** failure removes the pod from traffic, and "the container is not restarted". **Startup** probes hold off the other two until initialization succeeds ([Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)).
- The mapping to agent sessions below is this report's own inference (UNVERIFIED as prior art):
  - Liveness means "the session is making progress", not "the process exists". A timer heartbeat is a process-exists signal. That is why it kept arriving while the worker was stuck at context exhaustion.
  - Readiness means "the session is at an input prompt and can take a new task". A worker idle after ending its turn is ready but not live-on-task. Treat it as a separate state, not a failure.
  - Startup covers session boot and resume. Give it its own grace period so a slow start does not trip the stall detector.

## Supervisor trees and restart intensity limits (Erlang/OTP) — restart budgets

- An OTP supervisor allows at most `intensity` (MaxR) restarts in `period` (MaxT) seconds; the defaults are 1 and 5. Past that budget it terminates all children and then itself, which escalates the failure upward ([Erlang supervisor](https://www.erlang.org/doc/apps/stdlib/supervisor.html)).
- Strategies: `one_for_one`, `one_for_all`, `rest_for_one` and `simple_one_for_one` ([Erlang supervisor](https://www.erlang.org/doc/apps/stdlib/supervisor.html)). Intensity sets how big a burst is tolerated; period sets the sustained rate. For example, `intensity 5, period 3600` allows 5 restarts per hour ([design principles](https://beta.erlang.org/docs/26/design_principles/sup_princ.html)).
- For workers: give each task a restart budget, and when it is spent escalate to the human instead of restarting forever. The same idea appears in the SQS dead-letter queue advice below.

## Message delivery acknowledgement and at-least-once with idempotency (e.g. SQS visibility timeout, MQTT QoS, read receipts)

- **SQS**: receiving a message does not delete it. If the consumer does not delete it before the visibility timeout ends, another consumer can receive it. Standard queues can deliver duplicates even inside the timeout, so consumers must be idempotent. AWS recommends dead-letter queues for messages that keep failing ([SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)).
- **SQS heartbeat**: for variable processing times, extend visibility on a schedule with `ChangeMessageVisibility`, for example extending a 2-minute timeout every minute. Extensions are capped at 12 hours from the original receive ([best practices](https://docs.aws.amazon.com/en_en/AWSSimpleQueueService/latest/SQSDeveloperGuide/best-practices-processing-messages-timely-manner.html), [API](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ChangeMessageVisibility.html)).
- **MQTT**: QoS 1 is `PUBLISH → PUBACK`, at least once; the sender keeps the message until it is acknowledged and may send duplicates. QoS 2 adds `PUBREC → PUBREL → PUBCOMP` for exactly once, at higher cost ([Eclipse Paho QoS](https://eclipse-paho.github.io/paho.mqtt.c/MQTTClient/html/qos.html), [HiveMQ Edge QoS](https://github.com/hivemq/hivemq-edge/blob/master/Q0S.md)).
- Read receipts: no primary source was gathered (UNVERIFIED). The inference here is that "delivered to the mailbox" is like PUBACK from the broker, not from the reader. A real read acknowledgement has to come from the worker after it acts on the message.

## LLM agent orchestrators: how Claude Code, OpenHands, SWE-agent, Devin-like systems, LangGraph or AutoGen detect stuck/idle agents, context exhaustion, and checkpoint/resume (cite sources)

- **Claude Code** hook events ([hooks reference](https://code.claude.com/docs/en/hooks)):
  - `Notification` fires with matcher types including `permission_prompt`, `idle_prompt`, `agent_needs_input` and `agent_completed`. It cannot block anything.
  - `Stop` fires "When Claude finishes responding", once per turn rather than at session end. Exit code 2 keeps the session working.
  - `PreCompact` (`manual` or `auto`) fires "Before context compaction" and can add instructions for the compaction summary.
  - `SessionStart` reports a source of `startup`, `resume`, `clear`, `compact` or `fork`.
  - `TeammateIdle` fires when a teammate "is about to go idle".
  - The part of the page that was read gives no timing for `idle_prompt` (UNVERIFIED).
  - One report says `Notification` did not fire in the VS Code extension while it worked in the terminal ([issue #79881](https://github.com/anthropics/claude-code/issues/79881)).
- **OpenHands**: the `StuckDetector` scans up to 20 recent events for repeated action–observation pairs, repeated action–error pairs, monologues and alternating loops, ignoring IDs and metrics ([stuck_detector.py](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/conversation/stuck_detector.py)).
  - Thresholds were 4 identical pairs, 3 errors or 3 agent messages in a row. They produced false positives on legitimately repetitive work ([#762](https://github.com/OpenHands/software-agent-sdk/issues/762)).
  - It now sends one corrective nudge before declaring the agent stuck ([#4331](https://github.com/OpenHands/software-agent-sdk/issues/4331)).
  - A `STUCK` run stops with `interrupted` and does not recover on its own ([#4380](https://github.com/OpenHands/software-agent-sdk/issues/4380)).
- **SWE-agent**: `ContextWindowExceededError` ends the run with exit status `exit_context`, and a cost limit ends it with `exit_cost`. Both try to save the current patch before stopping ([agents.py](https://github.com/SWE-agent/SWE-agent/blob/main/sweagent/agent/agents.py), [exceptions](https://swe-agent.com/latest/reference/exceptions/)). Context exhaustion is a named terminal state, not a silent hang.
- **LangGraph**: checkpointers save state at super-step boundaries per `thread_id`. Reusing a thread with new input starts over; `invoke(None, config)` retries unfinished work. The `sync`, `async` and `exit` durability modes trade crash recovery against speed ([checkpointers](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx)). An interrupted node restarts from its beginning ([interrupts](https://langchain-ai.github.io/langgraph/concepts/breakpoints/)).
- **AutoGen**: `MaxMessageTermination` and `TimeoutTermination` are checked after each agent response, not continuously ([termination](https://microsoft.github.io/autogen/0.4.5/user-guide/agentchat-user-guide/tutorial/termination.html)). Teams expose `save_state()` and `load_state()` for resume ([state](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)).
- **Devin-like systems**: no source found (UNVERIFIED).

## Takeaways for a coordinator supervising terminal-based agent workers

These are synthesized from the sources above; the mapping to this system is inference.

1. **Liveness has to mean progress, not that the process exists.** Follow Temporal: heartbeats carry progress details (step, last tool call, context use), and the coordinator checks whether those details change. A timer heartbeat with unchanged details is a stall. This covers the context-exhaustion case.
2. **Make each blocked state its own signal.** Claude Code already emits `idle_prompt`, `permission_prompt`, `Stop`, `PreCompact` and `SessionStart(resume|compact)`. Forward them to the coordinator as typed events rather than inferring them from silence. They map to the Kubernetes split: ready (idle), blocked (permission), live (progressing) and starting (resume).
3. **Use explicit, application-level read acknowledgement.** Treat mailbox delivery like an SQS receive or an MQTT PUBACK from the broker, not proof that the worker read the message. Require the worker to acknowledge by message ID after acting on it, and redeliver or escalate if no acknowledgement arrives in time. Make every message idempotent, because at-least-once delivery means duplicates.
4. **Wait on every terminal type.** AutoGen-style composable termination (`A | B`) and SWE-agent's named exit statuses suggest that a wait should match every terminal and blocked kind, plus a catch-all for unknown types, never one filtered type. This covers the missed closing message.
5. **Budget restarts and resume from a checkpoint.** Allow OTP-style MaxR restarts in MaxT seconds per worker or task, then escalate, like a dead-letter queue. Resume from recorded progress (Temporal heartbeat details, a LangGraph checkpoint), and expect the interrupted step to run again. Nudge once before restarting, as OpenHands does.
