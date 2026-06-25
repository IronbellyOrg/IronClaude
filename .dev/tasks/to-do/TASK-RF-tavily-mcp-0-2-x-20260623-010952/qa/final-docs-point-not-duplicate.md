VERDICT: PASS

# QA Report — X6 Anti-Duplication Lens (docs/commands POINT, never duplicate)

**Topic:** Tavily MCP 0.2.x upgrade — TASK-RF-tavily-mcp-0-2-x-20260623-010952
**Date:** 2026-06-23
**Lens:** X6 — canonical homes hold values; everything else points
**Fix authorization:** FALSE (report only)
**Adversarial stance:** Assumed param duplication / broken pointer existed; hunted for it across src + docs.

---

## Overall Verdict: PASS

The literal DEFAULT_PARAMETERS value table `{"search_depth":"basic","max_results":10}` lives in exactly
TWO shipped files (install_mcp.py canonical home + MCP_Tavily.md capability reference) plus the tests.
Every consumer doc/command/skill/mode POINTS to a canonical source rather than restating the value table.
No broken pointers. RESEARCH_CONFIG.md names per-tier routing VALUES (allowed) and points to the baseline.

---

## Checks (all four PASS)

### Check 1 — Literal value table appears ONLY in install_mcp.py + MCP_Tavily.md (+ tests): PASS

`grep -rEn '"search_depth"|max_results' src/superclaude docs` returns exactly:
- `src/superclaude/cli/install_mcp.py:85` — `"default_parameters": {"search_depth": "basic", "max_results": 10}` (CANONICAL home)
- `src/superclaude/mcp/MCP_Tavily.md:59` — `| max_results | integer | search |` (param NAME in capability table, no value)
- `src/superclaude/mcp/MCP_Tavily.md:64` — the value string, explicitly disclaimed as non-canonical (see Check 3)

Broadened sweep for the exact JSON value `"search_depth":"basic"` across the whole repo (excluding `.venv`):
the value appears in shipped code ONLY at `install_mcp.py:85` and `MCP_Tavily.md:64`; in `tests/cli/test_install_mcp_tavily.py:23,37` (allowed test home); and otherwise ONLY under `.dev/` (brainstorms / research / reflect planning artifacts — NOT shipped docs/commands, out of X6 scope). No other shipped doc restates the value table.

### Check 2 — Consumer docs/commands POINT, not duplicate: PASS

| File | Tavily mention | Form | Evidence |
|------|---------------|------|----------|
| research.md | per-tier depth + routing | POINTER | L93 "…see RESEARCH_CONFIG.md Depth Profiles"; L97 "…see deep-research-agent / RESEARCH_CONFIG.md for routing" — no param table |
| mcp-servers.md | capabilities | POINTER | L137 "Capabilities: search, extraction, site-mapping, domain-crawl — see MCP_Tavily.md" — no param table |
| comprehensive-features.md | server + doc list | POINTER | L75 "…— see MCP_Tavily.md"; L80/L106 name MCP_Tavily.md / RESEARCH_CONFIG.md as doc files |
| FLAGS.md | --tavily behavior | POINTER | L72 "Enable Tavily for search/extract/map/crawl — see MCP_Tavily.md" — no param table |
| MODE_DeepResearch.md | capabilities | POINTER-equiv | L50 lists capability NAMES only (search/extraction/site-mapping/domain-crawl); no values |
| sc-brainstorm SKILL.md | research params | POINTER | L189 "Research depth/params are owned by /sc:research and tech-research — see RESEARCH_CONFIG.md" |
| sc-troubleshoot SKILL.md | Tier-2 query | PER-CALL OVERRIDE (X3, allowed) | L335 `search_depth: advanced` per-call arg — explicitly the documented X3 exception (MCP_Tavily.md:73 names this exact override); NOT a baseline restatement |
| sc-reflect SKILL.md | evidence search | POINTER-equiv | L1690 names "DEFAULT_PARAMETERS (C1) baseline" + inheritance behavior, contrasts troubleshoot override; does NOT restate the literal value table |

Confirmed via `grep -rEn 'basic.*advanced\|10 results\|max_results.*10'` over the four consumer files (FLAGS/research/mcp-servers/comprehensive-features): NONE — zero inline param tables.

### Check 3 — RESEARCH_CONFIG.md names per-tier routing VALUES (allowed) but points for the baseline: PASS

- Depth Profiles table (L66-71) legitimately lists per-tier `search_depth`/`extract_depth` = basic/basic/advanced/advanced — this IS the routing spec, explicitly allowed by the lens.
- L61-63 explicitly points for the server-level baseline: "see the install_mcp.py registry and MCP_Tavily.md … canonical values live in install_mcp.py / MCP_Tavily.md — not duplicated here."
- RESEARCH_CONFIG.md does NOT restate the `{"search_depth":"basic","max_results":10}` baseline table. PASS.

### Check 4 — No broken pointers: PASS

Every "see MCP_Tavily.md" / "see RESEARCH_CONFIG.md" / "install_mcp.py registry" reference names a file that exists on disk:
- `src/superclaude/mcp/MCP_Tavily.md` — EXISTS (9428 bytes)
- `src/superclaude/core/RESEARCH_CONFIG.md` — EXISTS (6853 bytes)
- `src/superclaude/cli/install_mcp.py` — EXISTS (32036 bytes)

All pointer references enumerated across src+docs (research.md, mcp-servers.md, comprehensive-features.md, FLAGS.md, RESEARCH_CONFIG.md, MCP_Tavily.md, deep-research.md, deep-research-agent.md, deep_research_workflows.md, sc-brainstorm SKILL.md) resolve to one of the three existing canonical files. No dangling pointer found.

---

## Adversarial Hunt — what I tried to break, and why it held

1. Suspected a second value-table home in a consumer doc → `grep "search_depth|max_results"` over src+docs: only the two canonical homes hit. HELD.
2. Suspected MCP_Tavily.md silently became a competing source-of-truth → it disclaims (L64-65: "canonical value lives in the install_mcp.py registry — it is not restated elsewhere"). HELD.
3. Suspected reflect SKILL.md L1690 restated the baseline → it names the concept + inheritance behavior, NOT the literal `{...}` value table. HELD (pointer-equivalent, allowed).
4. Suspected troubleshoot `search_depth: advanced` was a stray duplication → it is the documented X3 per-call override, cross-referenced at MCP_Tavily.md:73. HELD (intentional, allowed).
5. Suspected RESEARCH_CONFIG.md duplicated the server baseline alongside its routing table → it points for the baseline, names only per-tier routing values. HELD.
6. Suspected a broken "see X.md" pointer → all three targets exist on disk. HELD.

---

## Self-Audit

**(a) Reliance list — structural items NOT re-checked (out of this lens):** section numbering, frontmatter↔prose parity (X7), version-string uniformity (X1), eval token (X4) beyond the one spot-confirm below — these belong to other QA lenses.

**(b) Independent semantic checks (tool-grounded):**
- Literal-value-table sweep — verified by `grep -rEn '"search_depth"|max_results' src/superclaude docs` + a broadened `"search_depth":"basic"` repo sweep; mapped every hit to canonical/test/`.dev`-artifact.
- Pointer-target existence — verified by `ls -la` on all three canonical files (install_mcp.py, MCP_Tavily.md, RESEARCH_CONFIG.md).
- Canonical disclaimer — verified by Reading MCP_Tavily.md:59-66 and grep 'canonical'.
- Per-tier-vs-baseline distinction — verified by Reading RESEARCH_CONFIG.md:59-75 (Depth Profiles + pointer prose).
- Consumer-file cleanliness — verified by Reading research.md, FLAGS.md, mcp-servers.md, comprehensive-features.md, MODE_DeepResearch.md in full + negative grep for inline param tables.
- install_mcp.py canonical home — verified by Reading install_mcp.py:75-94 (the tavily registry entry).
- X4 spot-confirm — retry.md:139 uses `mcp_server.tavily` (correct token, not stale `mcp.tavily`).

**Self-audit answers:**
1. Independently verified ~10 factual claims against source (literal value home count, pointer targets, disclaimer text, per-tier table, consumer cleanliness, eval token).
2. Files read: install_mcp.py (registry slice), MCP_Tavily.md (full), RESEARCH_CONFIG.md (full), research.md (full), FLAGS.md (full), mcp-servers.md (full), comprehensive-features.md (full), MODE_DeepResearch.md (full), sc-brainstorm SKILL.md (full), sc-troubleshoot SKILL.md (partial — L335 confirmed), sc-reflect SKILL.md (L1680-1699 + early sections), retry.md (full).
3. Why trust the PASS: it rests on grep evidence (exact file:line) showing the value table in only 2 shipped files, plus `ls` proof that all 3 pointer targets exist — not on impression.
4. No web research performed (purely local-file-bound lens) — Tavily-first N/A this review.

**Tool engagement:** Read: 11 | Grep/Bash: 5 | Glob: 0
**Confidence:** Verified 4/4 checks | Unverifiable 0 | Unchecked 0 | Confidence 100%

---

## Issues Found

NONE (CRITICAL: 0, IMPORTANT: 0, MINOR: 0).

## Verified List

- install_mcp.py:85 is the sole canonical DEFAULT_PARAMETERS value home (Python dict literal).
- MCP_Tavily.md is the canonical capability reference; disclaims value-canonicity (L64-65), pointing to install_mcp.py.
- RESEARCH_CONFIG.md Depth Profiles name per-tier routing values (allowed); points to install_mcp.py/MCP_Tavily.md for the baseline (L61-63); does not duplicate the baseline table.
- research.md, mcp-servers.md, comprehensive-features.md, FLAGS.md, MODE_DeepResearch.md, sc-brainstorm SKILL.md all POINT; none carry an inline param table.
- sc-troubleshoot SKILL.md:335 `search_depth: advanced` is the documented X3 per-call override (cross-ref MCP_Tavily.md:73), not a baseline duplication.
- sc-reflect SKILL.md:1690 references the baseline concept + inheritance, does not restate the literal value table.
- All "see MCP_Tavily.md" / "see RESEARCH_CONFIG.md" / "install_mcp.py registry" pointers resolve to files that exist on disk.
- Literal value table confined outside shipped docs to tests/ (allowed) and .dev/ planning artifacts (out of scope).

## QA Complete
