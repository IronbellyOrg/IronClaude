# Reflect REPORT — Pre-execution audit of the BUILT Tavily 0.2.x tasklist

- **Mode:** UC-1 (pre-execution coverage/gap audit)
- **Tier reached:** 2 (forced by `--depth deep`)
- **Spec:** `.dev/brainstorms/CONSOLIDATED-tavily-0.2.x-upgrade.md`
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-tavily-mcp-0-2-x-20260623-010952/TASK-RF-tavily-mcp-0-2-x-20260623-010952.md`
- **Coverage (parsed + inferred union):** ≈ 0.97
- **Calibrated confidence:** 0.90
- **Verdict: PASS — clear to execute.** No missing requirements; findings are refinement notes on already-covered items.

> Context: a PRIOR pre-reflect (`pre-tavily-upgrade-20260623003519`, coverage 0.88) audited the driving **plan** and BLOCKED on B1 (a conflicting `@latest` plan). B1 is now **resolved by the user** (pin exact `0.2.20`) and H1–H4/M1–M5 are folded in. This run re-audits the **built tasklist** against the spec.

---

## Verdict summary

The tasklist is structurally sound, dependency-ordered (C1 first → C2 → C7 → C3-C6 → C8 → tests/QA/reflect), and **every reflect fix from the prior audit is faithfully encoded**. All load-bearing file:line citations re-Read against the live tree resolve exactly. There are **zero missing requirements**. Four low-severity refinement notes (one MINOR worth acting on pre-execution) are below.

---

## Coverage matrix (spec → tasklist item)

### Files to change (21 file-level requirements — all mapped)

| Spec change | Tasklist item | Grounded? |
|---|---|---|
| `install_mcp.py` version + `default_parameters` + `-e DEFAULT_PARAMETERS` | 2.1 | ✓ `install_mcp.py:80` = `npx -y tavily-mcp@0.1.2` (registry L76-84) |
| DELETE `src/.../configs/tavily.json` | 2.2 | ✓ exists (226B, git-tracked) |
| `main.py` no-change | 2.1 (confirm) | ✓ |
| `real.yaml` capability + `E-tavily-search` | 4.2 | ✓ `optional_capabilities:` L36-40 |
| `capabilities.py` `_CapabilitySpec` row (MANDATORY/M2) | 4.1 | ✓ `_DEFAULT_CAPABILITY_SPECS` L184; mcp_server rows L218/226/234 |
| `models.py` docstring `mcp.tavily`→`mcp_server.tavily` | 4.3 | ✓ `models.py:317,322` |
| `RESEARCH_CONFIG.md` | 3.1 | ✓ exists |
| `deep-research-agent.md` | 3.2 | ✓ exists |
| `deep-research.md` | 3.3 | ✓ exists |
| `MCP_Tavily.md` (canonical + M4 divergence) | 3.4 | ✓ exists |
| `MODE_DeepResearch.md` | 3.5 | ✓ exists |
| `deep_research_workflows.md` | 3.6 | ✓ exists |
| `research.md` (C3) | 5.1 | ✓ exists |
| `sc-brainstorm-protocol/SKILL.md` (C4) | 5.2 | ✓ exists |
| `sc-troubleshoot-protocol/SKILL.md` (C5) | 5.3 | ✓ exists |
| `sc-reflect-protocol/SKILL.md` (C5) | 5.4 | ✓ exists |
| 8 RF agents no-change (C6) | 5.5 (confirm) | ✓ |
| `mcp-servers.md` (@latest, Node, pointer) | 6.1 | ✓ `:273` `tavily-mcp@latest`; `:138` Node 16+ |
| `comprehensive-features.md` (broaden, drop tavily.json) | 6.2 | ✓ `:98` `- tavily.json`; `:75` cap line |
| `core/FLAGS.md` + sync | 6.4 | ✓ exists |
| `docs/eval/retry.md` token | 6.3 | ✓ `:139` `- mcp.tavily` (bare token, not URL) |

### Invariants X1–X7 — all threaded
X1 (2.1/6.1) · X2 (2.2) · X3 (2.1/3.1/3.4) · X4 (4.1/4.3/6.3) · X5 (3.x guards + 5.5 + parity test) · X6 (5.1/5.6/6.6) · X7 (3.2/3.3/3.8).

### Reflect fixes B1, H1–H4, M1–M5 — all folded faithfully
- **B1** pin `0.2.20` threaded everywhere; superseded `@latest` plan noted in Open Questions (line 327). ✓
- **H1** parity glob `src/superclaude/{agents,skills}/**/*.md` parsing BOTH `tools:`+`allowed-tools:` → 3.8; sc-recommend no-change confirm → 5.5. ✓
- **H2** plugins/ provenance discovery → 1.3; conditional delete → 2.2. (**Grounding confirms both `src/` and `plugins/` copies are git-tracked → the discovery is real and load-bearing.**) ✓
- **H3** version drift test scoped `src/`+`docs/`, excludes `.dev/`/`.claude/`/`dist/` → 6.6. ✓
- **H4** stale-token test word-boundary, excludes `mcp.tavily.com`, runs after C7 fix → 6.6. ✓
- **M1** compact `json.dumps(separators=(",",":"))` + masked key echo → 2.1; asserted → 2.3. ✓
- **M2** `capabilities.py` registration MANDATORY + regression test → 4.1/4.4. ✓
- **M3** assertions (default_parameters dict; `search_depth: advanced` in troubleshoot) → 2.3/5.8. ✓
- **M4** document C5 advanced divergence in MCP_Tavily.md → 3.4. ✓
- **M5** enumerate 6 no-change mentions → 6.5. ✓

### Tests (8 files — all mapped)
T1 install→2.3 · T2 parity→3.8 · T3 research_config→3.7 · T4 research_command→5.6 · T5 brainstorm→5.7 · T6 tier2_consistency→5.8 · T7 doc_alignment→6.6 · T8 eval-capability→4.4 (authorized expansion of the spec's 7-file table per M2).

---

## Findings (refinement notes — none block execution)

### MINOR-1 [Drift-risk] — `mcp-servers.md` Node-version edit lacks line scope
- **Where:** Step 6.1 instructs `change "Node.js 16+" → "Node.js 18+"` with no line qualifier.
- **Evidence:** `grep` shows **7** `Node.js 16+` lines (`mcp-servers.md:48,63,78,93,108,138,171`). The spec scopes this to **L138 only** (the Tavily requirements line). A naive replace-all would wrongly bump the other 6 servers, and **no test guards the Node version** (T7 checks version pin + tokens, not Node).
- **Recommendation:** scope Step 6.1 to the Tavily requirements line (`mcp-servers.md:138`) explicitly. Cheap to fix pre-execution; cheap for the executor to honor if the instruction names the line.

### MINOR-2 [Cosmetic] — "four edited C5 files" phrasing in Step 5.8
- **Where:** Step 5.8 calls `commands/troubleshoot.md`, `SKILL`, `commands/reflect.md`, `SKILL` "the four edited C5 files."
- **Reality:** only the two SKILLs are edited (5.3/5.4); `commands/troubleshoot.md` is "optional one clause" (dropped) and `commands/reflect.md` is no-change per spec. The **test behavior is correct** (it reads all four for tool-id parity / no-extract-map-crawl). Only the wording is inaccurate. No functional impact.

### LOW-1 — `git add -A` breadth in Step 7.4 (POST reflect wrapper prep)
- `git add -A` before the wrapper is broad. It is safe w.r.t. the `.claude/` ABSOLUTE RULE because `.claude/` (except `settings.json`) is gitignored, so `make sync-dev` output from 6.4 cannot be staged. The wrapper audits the working-tree diff and does **not** commit, so staging is transient. Note (not block): in a shared-index scenario `git add -A` can capture unrelated work — but this is an isolated worktree.

### LOW-2 — `plugins/` mirror outside drift-test scope
- T7 (`test_no_tavily_json_references`, version single-pin) is scoped to `src/`+`docs/` only (correct per H3). If 1.3's verdict is `TRACKED-HAND-MAINTAINED` and 2.2 deletes the `plugins/` copy, nothing guards a future reintroduction under `plugins/`. `plugins/` is build territory; acceptable to leave unguarded, but worth an Open-Questions note.

---

## What the tasklist got right (verified this pass)
- `mcp_server.tavily` token correction (X4) — grounded: `real.yaml` declares `mcp_server.serena` (L40) but `capabilities.py` `_DEFAULT_CAPABILITY_SPECS` lists only auggie/auggie-mcp/airis (L218/226/234) → M2 "register in BOTH" is the correct, evidence-backed strengthening.
- Dependency ordering (C1 establishes X1/X2/X3 before all consumers inherit).
- Per-phase validation gates (2.4/3.9/4.5/5.9/6.7) + full-suite gate (7.1) + executor-disjoint POST reflect wrapper (7.4, base from frontmatter `start_commit`).
- CI-safety discipline: every live exercise capability-gated/`skipif(not TAVILY_API_KEY)`.

## Grounding gaps
None. All citations re-Read; zero dropped. (UC-1 pre with file-evidence present — not a vacuous pass.)

## Recommendation
**Proceed to `/task`.** Optionally apply MINOR-1 first (scope the Node-version edit to `mcp-servers.md:138`) — a 1-line instruction tightening that removes the only real over-edit risk in the plan.
