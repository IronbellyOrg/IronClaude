---
id: "GFXAI-JEV-LITELLM-GATEWAY"
title: "Jev through the LiteLLM gateway: provisioning, key handling and rollback"
description: "How to expose TypeSafe Jev to Coder workspaces through the LiteLLM gateway, where each piece is provisioned, and how to verify, rotate and roll back."
version: "0.5"
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

**Evidence-status legend.** `[CODE-VERIFIED]` = read in our client code or probe output. File citations such as `config.py:2` are relative to `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` (probe output: `.../p15/jev/probe-result.json`; privacy scrub: `.../p19/ab6/seamlib.py`). `[LITELLM TEXT]` = from the LiteLLM TypeSafe Jev text the owner pasted on 2026-11-11 (route, key variable, pricing, behaviour); not yet exercised against our gateway. `[UNVERIFIED]` = general knowledge or a web summary; confirm against your deployed LiteLLM version.

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
| Endpoint | `https://api.typesafe.ai/v1/systemone` (through LiteLLM: `<proxy>/typesafe/v1/systemone`) | `[CODE-VERIFIED]` `jevlib/config.py:2`; gateway route `[LITELLM TEXT]` |
| Model id sent | `jev-1.14.0` (aliases are never sent) | `[CODE-VERIFIED]` `config.py:3` |
| Auth | `Authorization: Bearer <key>` | `[CODE-VERIFIED]` `client.py:148` |
| Request | `{"model", "state", "questions"}`; question types `noul` (true/false) or `choice` (2 to 255 options) | `[CODE-VERIFIED]` `questions.py:53-90` |
| Response check | returned `model` must equal the requested model, else `model_mismatch`; choice probabilities must sum to 1 within 0.02 | `[CODE-VERIFIED]` `validate.py:32`, `config.py:15` |
| Key variable | `JEV_API_KEY` (owner rule; the vendor's own variable name is not used by our client) | `[CODE-VERIFIED]` `config.py:4` |
| Cost and latency | $0.042 per 1M input tokens, no output charge (matches `config.py` and `[LITELLM TEXT]`); about $0.00005 and 160 to 380 ms per call in the probe | `[CODE-VERIFIED]` `probe-result.json` |
| Privacy guard | client refuses packets with owner names, absolute home paths or GitHub URLs | `[CODE-VERIFIED]` ab6 `seamlib.py` scrub rules |
| Streaming | not described in the LiteLLM text; our client does not stream | `[UNVERIFIED]` |

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
- So: provision the gateway route and the template URL now; Jev stays off for every user who has not created the `jev` secret, and you issue keys per team when a consumer with a measured benefit exists.

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

LiteLLM has a native TypeSafe Jev pass-through `[LITELLM TEXT]` (launched in `v1.103.0-rc`; the gateway was updated recently, so it should be present). Clients call the gateway with a LiteLLM virtual key only; the TypeSafe key is set once on the proxy.

### Step 1.1: Set the vendor key on the gateway

Set `TYPESAFE_API_KEY` in the gateway's environment or secret store and restart or reload the proxy `[LITELLM TEXT]`. No `config.yaml` entry is described for the native route. Do not put the key in a config file or in this repository.

Expected: `printenv TYPESAFE_API_KEY | wc -c` in the gateway process shows a non-zero length (never print the value).

### Step 1.2: Find the route prefix

The native route is `<proxy>/typesafe/v1/systemone`; any path under `/typesafe/` is forwarded, so `GET <proxy>/typesafe/v1/models` lists the available models `[LITELLM TEXT]`. Our workspaces reach the gateway as `http://192.168.133.101:4000/cli`; whether `/cli` also fronts `/typesafe/...` is **unverified**. Use a free call to find out (a virtual key from Phase 2, or a temporary admin key):

```bash
GW=http://192.168.133.101:4000
for pfx in /cli ""; do
  printf '%s -> ' "$pfx"
  curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $VIRTUAL_KEY" "$GW$pfx/typesafe/v1/models"
done
```

Expected: one prefix returns 200. Use that prefix in `JEV_API_URL`: today the Coder template builds `http://192.168.133.101:4000/cli/typesafe/v1/systemone` (Coder PR #496); if only the empty prefix works, change `llm-env.tf` and test 60 together.

### Step 1.3: Smoke-test the decision route

Replace `$BASE` with the working prefix from Step 1.2. This uses synthetic data only:

```bash
curl -sS "$GW$BASE/typesafe/v1/systemone" \
  -H "Authorization: Bearer $VIRTUAL_KEY" -H "Content-Type: application/json" \
  -d '{"model":"jev-1.14.0","state":{"order":{"promised":"2026-01-10","arrived":"2026-01-12"}},
       "questions":{"arrived_late":{"type":"noul","instructions":"Did the order arrive after the promised date?",
       "criteria":{"true":"The arrival date is later than the promised date.","false":"The arrival date is on or before the promised date."}}}}'
```

Expected: HTTP 200 and TypeSafe's own, unchanged response `[LITELLM TEXT]` with `"model": "jev-1.14.0"` and a `true` probability near 1. The LiteLLM example sends `"model": "jev-latest"`; our client pins `jev-1.14.0` instead and rejects any response whose `model` differs (`validate.py:32`). If your gateway returns a different id, stop and decide whether to relax that check deliberately.

> **Note:** LiteLLM logs spend under the versioned model TypeSafe reports (`typesafe/jev-1.13.0` in its text, even for `jev-latest`) `[LITELLM TEXT]`; expect the log entry under whatever the vendor reports for the id you sent.

### Fallback: generic pass-through

Only if the native route is missing. LiteLLM's generic pass-through forwards a path to an upstream URL and attaches the key `[UNVERIFIED]` (confirm field names in your version's docs):

```yaml
general_settings:
  pass_through_endpoints:
    - path: "/typesafe/v1/systemone"
      target: "https://api.typesafe.ai/v1/systemone"
      headers:
        Authorization: "bearer os.environ/TYPESAFE_API_KEY"
        content-type: "application/json"
      auth: true
```

Using the same `/typesafe/v1/systemone` path keeps `JEV_API_URL` unchanged.

### Phase 1 Verification Checkpoint
- [ ] Gateway has `TYPESAFE_API_KEY` and no copy of the key exists in the repo or any workspace
- [ ] `GET .../typesafe/v1/models` returned 200 on one prefix and the smoke test returned 200 with the pinned model id
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

Open the gateway's spend or request log for the key. Expected: the smoke-test request appears, with cost tracked at $0.042 per 1M input tokens and logged under the versioned model TypeSafe reports `[LITELLM TEXT]`. At about $0.00005 a call, the dollar cap is rarely the binding limit; keep the alert thresholds from Step 2.0.

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
| `JEV_API_URL` | Template (`llm-env.tf`, `coder_env.jev_api_url`) for every workspace | `${local.litellm_base_url}${local.jev_api_route}` = `http://192.168.133.101:4000/cli/typesafe/v1/systemone` today (prefix to confirm, Step 1.2); never the vendor host |
| `JEV_API_KEY` | The user, as a Coder secret: `printf %s "$JEV_API_KEY" \| coder secret create jev --env JEV_API_KEY` | the user's Jev virtual key from Phase 2 (a secret, never in the template) |

> **Note:** `JEV_API_KEY` in a workspace is a gateway virtual key, not the vendor key. If it leaks, revoke it in the gateway (Phase 4 rollback); the vendor key is untouched. A user with no `jev` secret has the URL but no key, so the client refuses to call (`KeyMissing`): Jev is off per user by default.

> **Important:** `jev_api_route` is `/typesafe/v1/systemone` (LiteLLM's native route `[LITELLM TEXT]`). Whether the `/cli` prefix in `litellm_base_url` also fronts it is checked in Step 1.2. If only the unprefixed path works, change `llm-env.tf` (and the pin in contract test 60) in the same PR.

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
1. In a workspace of a user with the `jev` secret, run the Phase 1 smoke test against `$JEV_API_URL`. Expect 200 and `model` equal to `jev-1.14.0`.
2. Run it with a deliberately wrong key. Expect 401 or 403.
3. Run it from a workspace of a user without the `jev` secret. Expect `JEV_API_URL` only and no way to call.

### 6.2 Key hygiene check
Run the repo's key scan (`p15/jev/keyscan.py` in the experiment tree) over any directory you put experiment output in; it must report nothing.

### All-Green Checklist
- [ ] Phase 1 to 3 checkpoints pass
- [ ] Wrong key rejected; a user without the `jev` secret has no `JEV_API_KEY`
- [ ] Budget alert or limit configured on the team key

---

## 7. Troubleshooting

| Symptom | Cause | Solution |
|---|---|---|
| Client raises `model_mismatch` | The response `model` differs from the id sent (the LiteLLM text says the response is TypeSafe's own, so check what you sent and what the vendor lists at `GET .../typesafe/v1/models`) | Send an id the vendor lists; update `MODEL` in `config.py` only deliberately |
| 401 or 403 from the route | Missing or revoked virtual key, or the route requires auth and the key lacks permission | Check the key in the admin UI; regenerate (Phase 2) |
| 404 from the route | Wrong prefix (`/cli` or none) or path | Re-run Step 1.2; align `JEV_API_URL` (and the Coder template) with the prefix that returns 200 |
| 502/504 from the gateway | Gateway cannot reach `api.typesafe.ai` or the upstream timed out | Prerequisite 5; client timeout is 20 s with one retry (`config.py:10-12`) |
| 400 from upstream | Request not accepted: positional option names, more than 255 options, or a malformed `state` | Client-side validation covers these (`questions.py:53-90`); reproduce with the Step 1.3 body |
| Calls succeed but spend shows 0 | The LiteLLM text says cost is tracked ($0.042 per 1M input tokens); a zero means the call did not go through the native route | Confirm the URL uses `/typesafe/` and the proxy has `TYPESAFE_API_KEY`; see Step 2.3 |
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
| Gateway route | `<proxy>/typesafe/v1/systemone` (list models: `GET <proxy>/typesafe/v1/models`) |
| Model id | `jev-1.14.0` |
| Gateway secret | `TYPESAFE_API_KEY` |
| Workspace variables | `JEV_API_URL` (template, Coder PR #496), `JEV_API_KEY` (user's `jev` Coder secret, virtual key) |
| Default | off |
| Evidence | `.dev/research/346-review-loop-experiments/p20/label/RESULTS-A2-LABELS.md` |

## 10. Next Steps and open items

- [ ] Record the gateway's LiteLLM version (needs `v1.103.0` or later for native Jev `[LITELLM TEXT]`).
- [x] Budget owner: Ryan Wiancko, company-wide.
- [ ] Budget owner to set the monthly cap and alert thresholds (Step 2.0).
- [x] `JEV_API_URL` override added to the client (Step 3.2).
- [x] Coder template change: IronbellyOrg/Coder PR #496 (review and merge).
- [ ] Run Step 1.2 to confirm the `/cli` prefix before merging Coder PR #496.
- [ ] Re-evaluate enabling Jev only after a seam passes a precision gate against independent labels.

## Document History

| Date | Version | Author | Changes |
|---|---|---|---|
| 2026-11-11 | 0.1 | Claude Code | Initial draft; gateway facts unverified |
| 2026-11-11 | 0.2 | Claude Code | Record recent LiteLLM update, company-wide budget owner, budget step |
| 2026-11-11 | 0.3 | Claude Code | Client `JEV_API_URL` override implemented |
| 2026-11-11 | 0.4 | Claude Code | Coder wiring implemented as template URL plus per-user secret (Coder PR #496) |
| 2026-11-11 | 0.5 | Claude Code | Route corrected to LiteLLM's native `/typesafe/v1/systemone` from the owner-supplied LiteLLM text; prefix check added |
