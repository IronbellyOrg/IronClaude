# Session proxy effort recovery architecture analysis

Template: loaded `/sc:analyze` output sections; skeleton adopted from `.dev/issuecleanup/g2/468/report-template.md`.

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/517/analyze`.

Date: 2026-11-24. Worktree: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. HEAD and the existing local `origin/master` both resolve to `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`; no fetch was performed. This is a static architecture pass, not a runtime or security audit.

Codegraph: index_state=fresh, checked_at=2026-11-24T02:43:43Z; degraded: graph:truncated, graph:unresolved. Access: mcp. The default callee query showed 20 of 22 rows; its unrelated `scripts/worktree_cleanup.py` `unavailable` result was excluded as an unresolved dynamic-name match. Relevant call sites and findings were checked directly in source.
## Architecture and metrics
- One shared route handles tier aliases and named models: `_post` calls `_forward_tier` at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:698-706`. Codegraph identifies three affected symbols: `_forward_tier`, `_post`, and `do_POST`; this is not a count of all runtime users.
- The selected method occupies lines 823-993. It walks eligible models, skips models on cooldown, changes `obj["model"]`, and serializes the otherwise unchanged object (`:839-847`). Both streamed and non-streamed requests use this route; only the initial reply timeout differs.
- Error classes are separate: usage/availability matches in `SWITCH_RULES` (`:396-414`) invoke `cool_down` (`:914-932`); temporary server errors increment a failure counter (`:933-944`); oversized backups advance without treating size as usage (`:948-955`); image rejection advances without parking (`:956-961`). Other request errors are returned unchanged (`:962`).
- The existing tests run the real proxy against a scripted stand-in gateway (`tests/unit/test_ccsession_tiers.py:847-907`), already support extra request fields, and cover unrelated errors (`:1039-1060`), backup size (`:1075-1087`), and non-parking image rejection (`:1104-1149`).
## Severity-rated findings
### Medium: the effort rejection still terminates the request instead of using the tier

For the exact HTTP 400 in issue #517, `This model always engages in thinking and cannot be disabled; please use low, high, or max`, no switch rule matches (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:396-433`), no effort rewrite occurs before forwarding (`:839-847`), and neither the server-error condition nor either request-specific exception applies (`:933-962`). It therefore reaches the unchanged-error return at line 962 without asking the next model. This establishes the source-level defect, not present-day provider behavior.

### Medium: fixing this with an ordinary switch rule violates the no-parking requirement

Every nonempty switch reason invokes `cool_down` (`:914-927`). That helper stores a model-keyed timestamp in `_cooldowns` (`:471-475`), using the configured default when Retry-After is absent. The default is 3,600 seconds (`:123`). A working model must not become unavailable to other efforts or tiers because one request has an incompatible effort. PR #738 already provides a request-specific no-parking branch for images, but its match and final response wording are image-specific; it does not fix effort rejection.

### Coverage gap

Search of the ccsession test filenames under `tests/` for `effort` and `always engages in thinking` found only launcher settings-preservation assertions, not the issue's proxy recovery case. Existing unmatched-400 and image tests constrain a repair but do not prove effort recovery. No test was executed in this static pass.
## Recommendations and roadmap
1. Keep issue #517 open. The shared proxy repair is not implemented.
2. Smallest complete repair: recognize only the specific effort-incompatibility 400, advance this request to the next eligible model without entering usage/server failure accounting, and preserve an accurate terminal error if no compatible model answers. Reuse the existing list walk and the no-parking approach of PR #738, not its image-specific wording. A capability cache, provider-wide rewrite framework, and tier configuration changes are unnecessary for this bounded fix.
3. Add regression cases using the existing shim fixture: medium-effort 400 reaches a successful backup; the same first model is tried again and serves the following high-effort request; unrelated first-model 400s pass through; oversized backups retain their exception; usage/server cooldown semantics remain unchanged; no-backup/all-incompatible replies do not falsely claim quota exhaustion. Cover streamed and non-streamed requests and the shared named-model route.
4. No changes were made. Security weaknesses and performance measurements are not established by this quick architecture pass. The existing image rejection demonstrates a rejected-round-trip cost; cost and latency for effort recovery remain UNVERIFIED until tested.
## Verification limits
Static source review only: no gateway calls, tests, builds, configuration changes, source edits, staging, commits or GitHub writes. Present-day live gateway acceptance, actual workspace slots, traffic counts and cross-tier operational impact are UNVERIFIED; the issue's November 12 measurements are historical evidence attributed to its author, not new measurements. GitHub PR search for both effort and proxy returned only merged workaround #516; the open ccsession PR search returned zero. Search results are bounded and do not prove no unpushed work exists.

Process exceptions retained for transparency: one read-only `gh api` call fetched the issue timeline despite the brief allowing only issue/pr view/list; no GitHub mutation occurred and no further API calls were made. Initial report Edit attempts were refused because the freshness hook requires Read even for a newly written stub; both stubs were then Read and edits continued through Edit. The full worker contract and analyze file were initially read above the worker's 80-line chunk limit; subsequent unknown-size file reads used bounded pieces. These exceptions do not change the source findings.
