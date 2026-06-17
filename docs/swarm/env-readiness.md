# MultiModelSwarm Environment Readiness Checklist

> **Scope:** OPS-002 / roadmap row **R-151** (`tasklist/phase-9` T09.02). The
> environment-readiness checklist an operator runs **before** the first
> `superclaude swarm run` on a fresh, **non-Anthropic T2 proxy** host. The
> swarm dispatches every worker through an OpenAI-compatible proxy
> (`OpenAICompatTransport`); no Anthropic / native host-vendor credentials are
> required, consulted, or accepted by this surface.
>
> **Companion preflight script:** [`scripts/swarm_env_readiness.sh`](../../scripts/swarm_env_readiness.sh)
> — authored separately under OPS-002. It asserts each prerequisite below and
> exits non-zero with a clear missing-prerequisite diagnostic. Run it first;
> this document is the human-readable contract behind it.
>
> **Sources of truth:**
> `src/superclaude/cli/swarm/transports/openai_compat.py` (`read_env` /
> `TransportEnvError`) for the env-var contract;
> `src/superclaude/cli/swarm/config.py` for the variable-name constants and
> the `T2_MODEL_MAX_SLOTS = 9` bound.

---

## 1. Prerequisite checklist

Run [`scripts/swarm_env_readiness.sh`](../../scripts/swarm_env_readiness.sh) to
assert all of these automatically. The table is the manual equivalent.

| # | Prerequisite | Requirement | Severity |
|---|---|---|---|
| 1 | Python | **>= 3.10** (the package's `requires-python`). | **Required** — fail |
| 2 | UV | The repo standardizes on UV for every Python operation (`uv run …`). | **Required** — fail |
| 3 | `httpx` | Transport HTTP client (`OpenAICompatTransport` issues every request through `httpx.Client`). | **Required** — fail |
| 4 | Click | CLI framework backing the `superclaude swarm` verb. | **Required** — fail |
| 5 | Rich | Terminal UI / progress rendering for the swarm pipeline. | **Required** — fail |
| 6 | tmux | Needed **only** for `swarm run --detached`. Inline `swarm run` never consults tmux. | **Optional** — warn-only |
| 7 | T2 proxy env vars | `T2ProxyUrl`, `T2ProxyKey`, and at least one `T2Model0N` slot (see §2). | **Required** — fail |

**Severity contract:**

- **Required (fail):** the preflight script exits non-zero. The swarm cannot
  run until the prerequisite is satisfied.
- **Optional (warn-only):** tmux absence is a non-fatal warning. The default
  inline pipeline runs to completion without tmux; only `--detached` requires
  it (and surfaces its own `EXIT_USAGE` diagnostic when tmux is missing).

Python deps (3, 4, 5) are declared in the package and installed by the
project's standard `uv` / editable install; the readiness script verifies they
are importable rather than re-installing them.

---

## 2. T2 proxy environment variables

These are the **only** environment variables the swarm CLI consumes for
worker dispatch. They are read at Wave 0 by
`read_env()` in
`src/superclaude/cli/swarm/transports/openai_compat.py` and validated against
the constants in `src/superclaude/cli/swarm/config.py`
(`T2_PROXY_URL_ENV`, `T2_PROXY_KEY_ENV`, `T2_MODEL_ENV_PREFIX`,
`T2_MODEL_MAX_SLOTS`).

| Variable | Purpose | Required |
|---|---|---|
| `T2ProxyUrl` | Base URL of the OpenAI-compatible proxy (e.g. `https://proxy.example.com/v1`). `read_env` strips trailing whitespace; `/chat/completions` is appended at send time. | **Yes** |
| `T2ProxyKey` | Bearer token sent as `Authorization: Bearer <key>`. | **Yes** |
| `T2Model01` | Model identifier for worker slot 1. **At least one populated slot is mandatory.** | **Yes** (>= 1 slot) |
| `T2Model02` .. `T2Model09` | Model identifiers for worker slots 2-9. Empty slots are skipped; the resolved `models` tuple stays dense and ordered by slot index. | Optional |

**Slot semantics (per `read_env` / `config.py`):**

- Slot names are `T2_MODEL_ENV_PREFIX` (`"T2Model0"`) concatenated with a
  1-based index — i.e. `T2Model01` .. `T2Model09`.
- The probe is bounded by `T2_MODEL_MAX_SLOTS = 9` (single-digit suffix).
- Values are read verbatim from `os.environ`; surrounding whitespace is
  stripped and whitespace-only values are treated as **absent**.
- At least one non-empty `T2Model0N` slot must resolve, or the contract is
  incomplete (see §3).

### Minimal happy-path environment

```bash
export T2ProxyUrl="https://proxy.example.com/v1"
export T2ProxyKey="your_t2_proxy_key_here"
export T2Model01="gpt-5-codex"
```

### Multi-slot deployment

```bash
export T2ProxyUrl="https://proxy.example.com/v1"
export T2ProxyKey="your_t2_proxy_key_here"
export T2Model01="gpt-5-codex"
export T2Model02="mistral-large-2407"
export T2Model03="qwen2.5-coder-32b"
```

> **No Anthropic / host-vendor credentials.** This surface addresses only the
> OpenAI-compatible proxy. There is **no** `ANTHROPIC_API_KEY` (or any
> native host-vendor credential) in the swarm env contract; `read_env` neither
> reads nor requires one. The proxy presents an OpenAI-compatible surface
> backed by whatever upstream providers it is configured with; routing lives
> at proxy-config time, not in this checklist.

See also the full AC-017 contract in
[`runbook.md` — T2 Proxy Env Contract](runbook.md).

---

## 3. INV-007 env-missing failure path

The readiness checklist exists to catch a missing T2 contract **before**
dispatch. If a required variable is absent at runtime, the failure surfaces
through the **INV-007 empty-pool failure path** rather than as an opaque HTTP
error.

**What happens when a required var is absent:**

1. At Wave 0, the dispatcher calls `read_env()`
   (`src/superclaude/cli/swarm/transports/openai_compat.py`).
2. `read_env` collects every missing mandatory name in a single pass — it
   appends `T2ProxyUrl` if the URL is unset/empty, `T2ProxyKey` if the key is
   unset/empty, and `T2Model01..T2Model09` if **no** model slot resolves.
3. If the `missing` list is non-empty, `read_env` raises
   **`TransportEnvError`**, whose message is:

   > `T2 proxy env contract incomplete; missing: <names>. Set T2ProxyUrl,
   > T2ProxyKey, and at least one T2Model01..9 slot.`

   The exception carries the full list of missing names on
   `TransportEnvError.missing` so the operator can fix the entire contract in
   one pass instead of discovering each gap by trial and error.
4. This structured diagnostic is the **Wave-0 anchor the dispatcher feeds into
   the INV-007 empty-pool failure path** (Phase-2 tasklist T02.11). The job
   does not proceed to dispatch with an empty / partial worker pool; it fails
   fast with the missing variable names surfaced verbatim.

**Why fail-fast here matters:** without this gate, a missing `T2ProxyKey`
would not be caught until httpx returned a `401`, and a missing `T2ProxyUrl`
until a connection error — both far less actionable than the up-front
"contract incomplete; missing: …" message. INV-007 ensures the empty/partial
pool is reported as a configuration failure at Wave 0, not as a downstream
transport error.

**Cross-reference:** the failure contract is INV-007 (Phase-2 tasklist
`T02.11`), consumed from the structured `TransportEnvError.missing` diagnostic.
The companion script
[`scripts/swarm_env_readiness.sh`](../../scripts/swarm_env_readiness.sh) mirrors
this contract by exiting non-zero with the same missing-variable enumeration
before any worker is dispatched.

---

## 4. References

- **OPS-002 / R-151** — `tasklist/phase-9` T09.02 (this deliverable).
- **INV-007** — empty-pool failure path, Phase-2 tasklist `T02.11`.
- **AC-017** — T2 proxy env-var contract (see [`runbook.md`](runbook.md)).
- Source of truth: `src/superclaude/cli/swarm/transports/openai_compat.py`
  (`read_env`, `TransportEnvError`) and
  `src/superclaude/cli/swarm/config.py` (env-var name constants,
  `T2_MODEL_MAX_SLOTS`).
- Companion preflight:
  [`scripts/swarm_env_readiness.sh`](../../scripts/swarm_env_readiness.sh).
