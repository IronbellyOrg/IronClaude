---
name: sc-bare-review
description: Infrastructure skill that dispatches 2-4 bare (unscaffolded) reviews of a target file in parallel to diverse EXTERNAL models via an OpenAI-compatible proxy, normalizes each into a compressed-markdown template carrying suspect:true, and returns a contract handing the files to /sc:adversarial --suspect-source. Delegate-only — no slash command.
allowed-tools: Read, Bash
model: sonnet
---

# sc-bare-review — T2 Bare-Reviewer Adjunct

<!-- meta (not parsed): category infrastructure | personas [analyzer, qa] | delegate-only, suspect-by-construction | spec .dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md (v1.3.0-draft §3,§4,§7,§8,§9.1) | roadmap M9 / R-135 / FR-029 / COMP-033 | migration M8/M9: now a thin caller over `superclaude swarm run --lens bare-review`; legacy bundled scripts retired in WS-C of the corrective task. -->

## Purpose & Identity

`sc-bare-review` turns a target file into 2-4 independent "bare" reviews — each from a *different
external model*, prompted with no protocol scaffolding so the model reviews with native instinct.
Bare reviews surface edge cases structured reviewers miss, **but their hallucinations are
predictable enough to gate against** — so every output is tagged `suspect: true` and flows into
`/sc:adversarial --suspect-source`, never trusted directly. **Compliance tier:** STANDARD.

- **IS:** a pure delegation target invoked as `Skill sc-bare-review …` by caller commands
  (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:adversarial`);
  a **thin caller over `superclaude swarm run --lens bare-review`** — the swarm CLI owns preflight,
  parallel fan-out, normalization, and the return contract.
- **IS NOT:** user-invoked (no `/sc:bare-review` command); a judge (never scores/filters — raw
  forwarding); Anthropic-routed (T2 external by design).

## Invocation (§3.2 input → swarm flags; delegate-only entry)

Caller flags map 1:1 onto `swarm run --lens bare-review`: `--target <path>` (REQUIRED),
`--output <dir>` (REQUIRED), `--reviewers <N>` (2-4, default 3), `--target-line-cap <N>` (default
4000), `--timeout-sec <N>` (default 180), `--label <str>`. (`--c7*` are accepted at the skill
boundary but are a no-op, NOT forwarded to `swarm run`.) For `--transport openai_compat` the swarm
preflight requires `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N` and STOPs naming any missing var; `--transport stub` is a hermetic dry run. Invoke once and relay the contract:

```bash
superclaude swarm run --lens bare-review --target <target> --output <output-dir> \
  [--reviewers <N>] [--target-line-cap <N>] [--timeout-sec <N>] [--label "<label>"] \
  --transport openai_compat
```

- **Non-zero exit → STOP**; surface stderr verbatim. Empty-target (IMM-4) and env-missing fail at
  preflight before any reviewer dispatches.
- On success, `Read` `<output-dir>/return-contract.yaml` and relay it. The CLI fans out the N
  reviewers internally (no manual single-message dispatch), normalizes each into the §4 template,
  writes `bare-review-NN-<model>.md`, and emits the contract.

## Return Contract (§3.3) — written on every invocation including failure

```yaml
contract_version: "1.0"
status: success | partial | failed   # IMM-5 success-first: M==N→success; 2≤M<N→partial; M<2→failed
target: <absolute>; target_checksum: <sha256>; reviewers_requested: <N>; reviewers_succeeded: <M>
output_files: [ { path, model_id, status: success|timeout|parse_error|proxy_error }, … ]
suspect: true   # always — suspect by construction
recommended_next_command: "/sc:adversarial --compare <existing-review>,<bare1>,… --suspect-source <bare1>,…"
```

## Failure Modes (§8) & Boundaries (§3.4)

| Scenario | Behavior |
| --- | --- |
| Env var (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`) unset | STOP at preflight naming the missing var |
| `--reviewers` out of `[2,4]` / target missing / <50 non-ws bytes (IMM-4) | STOP, no dispatch |
| Proxy 5xx | retry once after 2s, then `proxy_error`, continue |
| Proxy 4xx / timeout / parse fail | per-reviewer status, continue (parse_error → §7.4 salvage) |
| `M < 2` / `2 ≤ M < N` | `failed` (do NOT proceed) / `partial` (only successful files listed) |

**Will:** read target; N parallel reviews; per-reviewer hard timeout; continue on partial success
(≥2); always `suspect: true`; emit `recommended_next_command`; write only inside `--output`.
**Will NOT:** judge/score/filter; retry beyond one 5xx; route to Anthropic; write outside `--output`.

## Acceptance Pointers (§9.1)

AC-1.1..1.12 (env STOP, `[2,4]` reviewers, per-reviewer timeout, `suspect:true`, IMM-5 status,
`recommended_next_command` with literal `--suspect-source`) are enforced by the swarm CLI and
guarded by `tests/swarm/test_bare_review_parity.py` (CLI-vs-frozen-golden), `test_recipe_bare_review.py`, `test_e2e_user_guide.py`, and the IMM suite.

---

*M8/M9 — thin caller over `superclaude swarm run --lens bare-review`. Source of truth `src/superclaude/`; run `make sync-dev` after edits — never edit the `.claude/` mirror directly.*
