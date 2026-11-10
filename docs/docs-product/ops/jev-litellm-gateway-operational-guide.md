---
id: "GFXAI-JEV-LITELLM-GATEWAY"
title: "Jev through the LiteLLM gateway: provisioning, key handling and rollback"
description: "How to expose TypeSafe Jev to Coder workspaces through the LiteLLM gateway, where each piece is provisioned, and how to verify, rotate and roll back."
version: "0.4"
status: "🟡 Draft"
type: "📘 Operational Guide"
priority: "▶️ Medium"
created_date: "2026-11-11"
updated_date: "2026-11-11"
assigned_to: "platform"
tags:
- operational-guide
- jev
- litellm
- coder
template_schema_doc: ".claude/templates/documents/operational_guide_template.md"
---

# Jev through the LiteLLM gateway

> **WHAT:** Provision TypeSafe Jev (model `jev-1.14.0`) for Coder workspaces behind the LiteLLM gateway, with the vendor key held only by the gateway.
> **WHY:** The #346 experiments used Jev with a vendor key on one machine. A shared setup must not copy that key into every workspace, and must be switchable off.
> **HOW TO USE:** Platform owners follow Phases 1 to 5 once; workspace users need only Phase 3's two variables. Read the evidence-status legend first: several gateway facts are **unverified** because the LiteLLM and Coder configuration is not in this repository.

**Evidence-status legend.** `[CODE-VERIFIED]` = read in our client code or probe output. File citations such as `config.py:2` are relative to `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` (probe output: `.../p15/jev/probe-result.json`; privacy scrub: `.../p19/ab6/seamlib.py`). `[UNVERIFIED]` = taken from a web search summary or general knowledge; the page could not be opened from the authoring session (`docs.litellm.ai` was unreachable). Confirm every `[UNVERIFIED]` line against your deployed LiteLLM version before relying on it.

## Document Information

| Field | Value |
|---|---|
| Guide Type | Setup / operations |
| Target Environment | LiteLLM gateway host; Coder template; developer workspaces |
| Maintained By | platform |
| Budget owner | Ryan Wiancko (company-wide Jev budget) |
| Last Verified Against System | not verified against the live gateway |
| Prerequisites Guide | none |
| Next Guide | none |

---

## 1. Overview

### 1.1 What Jev is, as our code uses it

| Item | Value | Status |
|---|---|---|
| Endpoint | `https://api.typesafe.ai/v1/systemone` | `[CODE-VERIFIED]` `jevlib/config.py:2` |
| Model id sent | `jev-1.14.0` (aliases are never sent) | `[CODE-VERIFIED]` `config.py:3` |
| Auth | `Authorization: Bearer <key>` | `[CODE-VERIFIED]` `client.py:148` |
| Request | `{"model", "state", "questions"}`; question types `noul` (true/false) or `choice` (2 to 255 options) | `[CODE-VERIFIED]` `questions.py:53-90` |
| Response check | returned `model` must equal the requested model, else `model_mismatch`; choice probabilities must sum to 1 within 0.02 | `[CODE-VERIFIED]` `validate.py:32`, `config.py:15` |
| Key variable | `JEV_API_KEY` (owner rule; the vendor's own variable name is not used by our client) | `[CODE-VERIFIED]` `config.py:4` |
| Cost and latency | about $0.00005 and 160 to 380 ms per call in the probe | `[CODE-VERIFIED]` `probe-result.json` |
| Privacy guard | client refuses packets with owner names, absolute home paths or GitHub URLs | `[CODE-VERIFIED]` ab6 `seamlib.py` scrub rules |
| Streaming | not offered | `[UNVERIFIED]` |

Jev is a decision API, not a chat model: it returns typed answers with probabilities, so it does not go through `/chat/completions`.

### 1.2 Where Jev is provisioned (decision)

Jev is a hosted API, so there is nothing to "install". Three separate things exist and each has one home:

| Piece | Home | Why |
|---|---|---|
| Vendor key and upstream URL | **LiteLLM gateway** (secret env var on the gateway host) | One copy, rotated in one place, never in a workspace |
| Per-user access, budget, revocation | **LiteLLM virtual keys** | Same mechanism the model tiers already use |
| `JEV_API_URL` (template) and `JEV_API_KEY` (per-user Coder secret holding the virtual key), plus the egress rule | **Coder template** and **Coder user secrets** | Matches how `LITELLM_API_KEY` and the gateway URL already work; Jev is on only for users who create the secret |
| Client code that reads those variables | **superclaude package** (shipped by `superclaude install`, once a consumer exists) | Versioned with the repo; it holds no key |

Not in the installer: `superclaude install` copies commands, agents, skills, hooks and templates; it must never write a key.

### 1.3 Ship it OFF by default

- Nothing in `src/` calls Jev today; the client exists only in the experiment tree.
- Evidence from #346: three Jev seams were tried; two were dropped and the third (A2, acceptance-check observability) was labelled blind by three Opus 5.5 agents: Jev's `cannot_pass` was right on 6 of 24 sampled packets (25%) and did not separate flawed from sound checks (Fisher p = 0.72). See `.dev/research/346-review-loop-experiments/p20/label/RESULTS-A2-LABELS.md`.
- So: provision the gateway route and the opt-in template parameter now, leave it unset in the default template, and enable it per team when a consumer with a measured benefit exists.

---

## 2. Prerequisites

| # | Check | How to Verify |
|---|---|---|
| 1 | You own the vendor account and have a TypeSafe API key for `jev-1.14.0` | the vendor console lists the model; do not paste the key into chat, tickets or this repo |
| 2 | Admin access to the LiteLLM gateway (config file or admin UI, master key) | `curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" "$GATEWAY/health/liveliness"` returns OK `[UNVERIFIED]` |
| 3 | Record the gateway's LiteLLM version | The gateway was updated the week before 2026-11-11 (owner statement), so the native Jev provider, reported to need `v1.103.0-rc` or later `[UNVERIFIED]`, is likely present. Confirm: `GET $GATEWAY/health/readiness` or the admin UI shows the version; write it here: ______ |
| 4 | Edit access to the Coder template repo (`IronbellyOrg/Coder`, `templates/VSCode-AIDev02`) | you can open a PR there |
| 5 | The gateway host can reach `api.typesafe.ai:443` | `curl -sS -o /dev/null -w '%{http_code}\n' https://api.typesafe.ai/` from the gateway host returns an HTTP code (any) |

---

## 3. Phase 1: Add the Jev route to the gateway

Try A first: the gateway was updated recently, so native support is likely (confirm the version in Prerequisite 3). Use B if A is missing or cannot pin the model id. Both keep the key on the gateway.

### Step 1.1: Store the vendor key as a gateway secret

Set `TYPESAFE_API_KEY` in the gateway's environment or secret store (the name LiteLLM's native provider is reported to read `[UNVERIFIED]`; using it for option B too means moving from B to A needs no secret change). Do not put it in `config.yaml`.

Expected: `printenv TYPESAFE_API_KEY | wc -c` on the gateway process shows a non-zero length (never print the value).

### Step 1.2A: Native provider (preferred when available)

LiteLLM's provider list reportedly includes TypeSafe Jev (example model `typesafe/jev-latest`, routes `/v1/systemone` and `/v1/decisions`) `[UNVERIFIED]`. Follow the LiteLLM page `pass_through/typesafe` for the exact config entry of your version; do not copy a snippet from this guide.

> **Important:** configure the route so requests carry the model id `jev-1.14.0`, not `jev-latest`. Our client rejects any response whose `model` differs from the one it asked for (`validate.py:32`), so a gateway that rewrites or aliases the model name will make every call fail with `model_mismatch`. If the gateway cannot return the pinned id, either relax the check deliberately in the client or use option B.

### Step 1.2B: Generic pass-through (fallback)

LiteLLM's generic pass-through lets the gateway forward a path to an upstream URL and attach the upstream key `[UNVERIFIED]` (shape from general knowledge; confirm field names in your version's docs):

```yaml
general_settings:
  pass_through_endpoints:
    - path: "/jev/v1/systemone"
      target: "https://api.typesafe.ai/v1/systemone"
      headers:
        Authorization: "bearer os.environ/TYPESAFE_API_KEY"
        content-type: "application/json"
      auth: true            # require a LiteLLM virtual key on this route
```

Reload the gateway after editing (method depends on how it is deployed).

### Step 1.3: Smoke-test from the gateway host

Use any valid virtual key (Phase 2 creates a scoped one; a temporary admin key works for this one test). Replace `$ROUTE` with `/jev/v1/systemone` (B) or the native route (A):

```bash
curl -sS "$GATEWAY$ROUTE" \
  -H "Authorization: Bearer $VIRTUAL_KEY" -H "Content-Type: application/json" \
  -d '{"model":"jev-1.14.0","state":{"order":{"promised":"2026-01-10","arrived":"2026-01-12"}},
       "questions":{"arrived_late":{"type":"noul","instructions":"Did the order arrive after the promised date?",
       "criteria":{"true":"The arrival date is later than the promised date.","false":"The arrival date is on or before the promised date."}}}}'
```

Expected: HTTP 200; JSON with `"model": "jev-1.14.0"` and an answer for `arrived_late` with a true probability near 1. Note the request uses synthetic data only.

### Phase 1 Verification Checkpoint
- [ ] Gateway has `TYPESAFE_API_KEY` and no copy of the key exists in the repo or any workspace
- [ ] The smoke test returned 200 with the pinned model id
- [ ] A request with no `Authorization` header returns 401 or 403, not a Jev answer

---

## 4. Phase 2: Virtual keys with budgets

### Step 2.0: Set the company budget

The Jev budget is company-wide and owned by Ryan Wiancko. Put the cap where LiteLLM enforces it above the keys (a team or organisation budget whose members are the team keys below `[UNVERIFIED]` for your version), so no single key can exceed it and the total stays under the company figure. At about $0.00005 a call the dollar cap is rarely the binding limit; set an alert threshold at 50% and 80% of the cap, sent to the budget owner.

### Step 2.1: Create a key per team (or per user)

```bash
curl -sS "$GATEWAY/key/generate" -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"key_alias":"jev-<team>","max_budget":5,"budget_duration":"30d","metadata":{"purpose":"jev"}}'
```

Fields `key_alias`, `max_budget`, `budget_duration` and `metadata` are standard LiteLLM key options `[UNVERIFIED]`. Record the returned key in the team's secret store, not in chat.

### Step 2.2: Confirm the key reaches only what it should

- A call with this key to the Jev route succeeds (Phase 1 smoke test).
- A call to a model route the team should not use returns 401/403, if you restrict models on the key. Restricting pass-through routes per key may need route permissions rather than model lists `[UNVERIFIED]`; test it, do not assume.

### Step 2.3: Check that spend is recorded

Open the gateway's spend or request log for the key. Expected: the smoke-test request appears. For a pass-through route the cost may need a per-request cost setting to show non-zero `[UNVERIFIED]`; at about $0.00005 a call, budgets are better enforced by request count or an alert than by dollars.

### Phase 2 Verification Checkpoint
- [ ] Key exists with a budget and alias
- [ ] Spend or request log shows the test call
- [ ] Revoking the key (`/key/delete`) makes the Jev route return 401 `[UNVERIFIED]`

---

## 5. Phase 3: Coder template wiring (opt-in)

Implemented in `IronbellyOrg/Coder` PR #496 (branch `jev-gateway-url-346`), following that repository's rule that the gateway URL is template configuration and secrets are Coder user secrets (no new workspace parameter).

### Step 3.1: What the template does and what each user does

| Variable | Set by | Value |
|---|---|---|
| `JEV_API_URL` | Template (`llm-env.tf`, `coder_env.jev_api_url`) for every workspace | `${local.litellm_base_url}${local.jev_api_route}` = `http://192.168.133.101:4000/cli/v1/systemone` today; never the vendor host |
| `JEV_API_KEY` | The user, as a Coder secret: `printf %s "$JEV_API_KEY" \| coder secret create jev --env JEV_API_KEY` | the user's Jev virtual key from Phase 2 (a secret, never in the template) |

> **Note:** `JEV_API_KEY` in a workspace is a gateway virtual key, not the vendor key. If it leaks, revoke it in the gateway (Phase 4 rollback); the vendor key is untouched. A user with no `jev` secret has the URL but no key, so the client refuses to call (`KeyMissing`): Jev is off per user by default.

> **Important:** `jev_api_route` (`/v1/systemone`) must equal the route you configured in Phase 1. The path is unverified against the live gateway. If the gateway uses another path (for example `/jev/v1/systemone` from option B), change `jev_api_route` in `llm-env.tf` and the pin in contract test 60 together.

### Step 3.2: Client override (done)

The experiment-tree client now honours `JEV_API_URL`: unset or empty keeps the vendor URL; a set value must be https (http only for a loopback or private-range IP literal, since the internal gateway is plain http on a private address), with no user info, query or fragment, otherwise the client raises `ValueError` and sends nothing (it never falls back to the vendor). The model-id check and the privacy scrub are unchanged, so a gateway that rewrites the model is still rejected. Code: `p15/jev/jevlib/config.py` (`api_url`), tests: `p15/jev/tests/test_api_url.py`. When the client moves into the superclaude package, carry the override and its tests with it.

### Step 3.3: Egress

Workspaces should reach the gateway only. If workspace egress is allow-listed, do not add `api.typesafe.ai`.

### Phase 3 Verification Checkpoint
- [ ] A new workspace of a user without the `jev` secret has `JEV_API_URL` but no `JEV_API_KEY` (`env | grep '^JEV_'` prints one name)
- [ ] A workspace of a user with the secret has both, and the Phase 1 smoke test works from inside the workspace using `$JEV_API_URL` and `$JEV_API_KEY`
- [ ] From the workspace, a direct call to `https://api.typesafe.ai/v1/systemone` is blocked or has no key to use

---

## 6. Verification

### 6.1 End-to-end
1. In a workspace with the parameter set, run the Phase 1 smoke test against `$JEV_API_URL`. Expect 200 and `model` equal to `jev-1.14.0`.
2. Run it with a deliberately wrong key. Expect 401 or 403.
3. Run it from a workspace of a user without the `jev` secret. Expect `JEV_API_URL` only and no way to call.

### 6.2 Key hygiene check
Run the repo's key scan (`p15/jev/keyscan.py` in the experiment tree) over any directory you put experiment output in; it must report nothing.

### All-Green Checklist
- [ ] Phase 1 to 3 checkpoints pass
- [ ] Wrong key rejected; no-parameter workspace has no Jev variables
- [ ] Budget alert or limit configured on the team key

---

## 7. Troubleshooting

| Symptom | Cause | Solution |
|---|---|---|
| Client raises `model_mismatch` | The gateway returned a different model id (alias such as `jev-latest`) | Pin `jev-1.14.0` on the route, or use option B (Step 1.2) |
| 401 or 403 from the route | Missing or revoked virtual key, or the route requires auth and the key lacks permission | Check the key in the admin UI; regenerate (Phase 2) |
| 404 from the route | Route path differs from the one the client builds (option A route names vs option B `path`) | Align `JEV_API_URL` with the configured path exactly |
| 502/504 from the gateway | Gateway cannot reach `api.typesafe.ai` or the upstream timed out | Prerequisite 5; client timeout is 20 s with one retry (`config.py:10-12`) |
| 400 from upstream | Request not accepted: positional option names, more than 255 options, or a malformed `state` | Client-side validation covers these (`questions.py:53-90`); reproduce with the Step 1.3 body |
| Calls succeed but spend shows 0 | Pass-through cost is not computed by default `[UNVERIFIED]` | Use request counts or a per-request cost setting; see Step 2.3 |
| Privacy-guard refusal in the client | Packet contained an owner name, home path or GitHub URL | Fix the packet; do not disable the guard |

---

## 8. Maintenance & Operations

### 8.1 Key rotation
1. Generate a new vendor key at the vendor console.
2. Update `TYPESAFE_API_KEY` on the gateway and reload it. Workspaces keep working: they only hold virtual keys.
3. Run the Phase 1 smoke test. Then revoke the old vendor key.
4. Virtual keys rotate independently: create a new one, update the team secret, delete the old one.

### 8.2 Rollback (switch Jev off)
- Per user or team: `coder secret delete jev` (or `update` it) and restart workspaces; delete the virtual key in the gateway.
- Everywhere: remove the route from the gateway config and reload. The vendor key can stay on the gateway or be removed.
- No package rollback is needed while no consumer ships.

### 8.3 Routine
- Review the Jev spend or request log monthly.
- Re-verify the model id on the vendor's models page before moving off `jev-1.14.0`; update `config.py` and the route together.

---

## 9. Quick Reference

| Item | Value |
|---|---|
| Upstream | `https://api.typesafe.ai/v1/systemone`, bearer key |
| Model id | `jev-1.14.0` |
| Gateway secret | `TYPESAFE_API_KEY` |
| Workspace variables | `JEV_API_URL` (template, Coder PR #496), `JEV_API_KEY` (user's `jev` Coder secret, virtual key) |
| Default | off |
| Evidence | `.dev/research/346-review-loop-experiments/p20/label/RESULTS-A2-LABELS.md` |

## 10. Next Steps and open items

- [ ] Confirm the LiteLLM version and the native Jev route against `docs.litellm.ai` (blocked for the authoring session; the gateway was updated recently).
- [x] Budget owner: Ryan Wiancko, company-wide.
- [ ] Budget owner to set the monthly cap and alert thresholds (Step 2.0).
- [x] `JEV_API_URL` override added to the client (Step 3.2).
- [x] Coder template change: IronbellyOrg/Coder PR #496 (review and merge).
- [ ] Verify the gateway route path against `jev_api_route` (Step 3.1).
- [ ] Re-evaluate enabling Jev only after a seam passes a precision gate against independent labels.

## Document History

| Date | Version | Author | Changes |
|---|---|---|---|
| 2026-11-11 | 0.1 | Claude Code | Initial draft; gateway facts unverified |
| 2026-11-11 | 0.2 | Claude Code | Record recent LiteLLM update, company-wide budget owner, budget step |
| 2026-11-11 | 0.3 | Claude Code | Client `JEV_API_URL` override implemented |
| 2026-11-11 | 0.4 | Claude Code | Coder wiring implemented as template URL plus per-user secret (Coder PR #496) |
