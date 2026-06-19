# sc:reflect V3 — Serena Adoption Research: Conversation Context

This file is the contextual envelope around `01-matrix-low-complexity.md` and `02-matrix-medium-complexity.md`. It captures the framing, prior usage, posture clarifications, and excluded items required to interpret those matrices correctly. The research agents appended below the BEGIN markers in the two matrix files should be read with this context in mind.

---

## 1. Originating question

The investigation began with:

> *"Explain to me all the ways that sc:reflect uses Serena MCP and what value that represents"*

It evolved into:

> *"Research the Serena documentation and latest updates and create a list of all of the features and functionality available to use that we are not currently using. Then evaluate that list against the objectives of the sc:reflect command and create a matrix."*

The two matrices in this directory are the filtered output of that evaluation — they are not the full superset, but the actionable subset bucketed by (complexity × value).

---

## 2. sc:reflect's current Serena footprint

Declared in `src/superclaude/skills/sc-reflect-protocol/SKILL.md:19`:

```yaml
mcp-servers: [serena, auggie, context7, tavily, sequential]
```

Frontmatter `allowed-tools` lists explicitly:

- `mcp__serena__find_symbol`
- `mcp__serena__find_referencing_symbols`
- `mcp__serena__get_symbols_overview`
- `mcp__serena__get_diagnostics_for_file`
- `mcp__serena__read_memory`
- `mcp__serena__write_memory`
- `mcp__serena__list_memories`
- `mcp__serena__search_for_pattern`
- `mcp__serena__activate_project`

Plus three scripted `think_about_*` checkpoints (`§6.4`) that are **deliberately NOT in `allowed-tools`** — they are logged to `<output>/serena-checkpoints.log` as 200-token nudges but do not gate ship. The evidence-validator gates ship.

### Five structural roles Serena fills today

1. **Project activation & session bootstrap** (Wave 0): `activate_project`, `list_memories` (also as sc-adversarial-protocol existence probe at Wave 5 Step 5.0)
2. **Symbol-anchored evidence chain** (Wave 1A, §6.1): `get_symbols_overview` → `find_symbol` → `find_referencing_symbols` → `get_diagnostics_for_file` → re-Read. This **replaces** Serena's own `think_about_collected_information` as the load-bearing grounding mechanism.
3. **Cross-task interaction-effects scan** (Wave 1B.3, UC-2 only, ≥3 completed tasks): `find_symbol` over diff hunks + `find_referencing_symbols` to confirm symbol-overlap edges are genuine vs. name collisions. Top-30 cap; severity scales with referencing call-site count.
4. **Per-project deviation memory** (Wave 0 hydrate / Wave 5 persist, §6.3): `read_memory` / `write_memory` against `reflect/last-pass-{slug}` and `reflect/deviation-patterns-{slug}` with 90-day TTL and 20-entry retention.
5. **Scripted `think_about_*` audit checkpoints** (deliberately non-load-bearing, §6.4): three nudges captured to audit, used only as a cheap upward bias on `S_dev_density` when they surface gaps.

### Architectural bet

§1414 of SKILL.md makes the bet explicit: **Serena's symbolic chain is the load-bearing grounding mechanism**; `think_about_*` is demoted to scripted nudges; everything is fail-open so Serena being down degrades depth rather than breaking the skill.

---

## 3. Posture clarification (the read-only boundary)

A correction landed during this investigation that meaningfully changed one matrix entry. Verbatim:

> *"`Conflicts with sc:reflect's read-only audit posture` — this should be amended, there is no strict read-only posture in this context. Read only means that reflect should not write and fix issues it finds in the code and in the project but it absolutely should be able to run tests and write to logs and report files as needed."*

**Operational meaning:**

- ❌ sc:reflect **does not** mutate project source code, configuration, or tests. Source-code edits are the **Tier 3 remediation handoff** target (task-builder → MDTM), not sc:reflect itself.
- ✅ sc:reflect **does** write `audit.log`, `serena-checkpoints.log`, `reviewer-briefs/`, the final report, return-contract YAML, and Serena memory blobs.
- ✅ sc:reflect **may** execute non-mutating verification commands — `pytest`, `ruff`, `mypy`, `make test`, `uv run`, build steps — and consume their exit codes / output as audit signal.
- ❌ sc:reflect **may not** execute `git commit`, `git push`, file edits outside its own `<output>/`, package installs, or any side-effecting state change to the project or environment.

**Why this matters:** this is the line that decides whether `execute_shell_command` is "policy conflict" (no) or "core verification capability" (yes). The matrices reflect the corrected interpretation.

---

## 4. The 4-category deviation taxonomy (UC-2 audit target)

sc:reflect classifies every divergence from spec/tasklist under one of four classes (`refs/deviation-taxonomy.md`). The matrices reference these by name; here is the canonical glossary:

| Class | Definition | Example failure mode |
|---|---|---|
| **Authorized expansion** | Divergence pre-approved or explicitly justified in-flight. | "Added rate-limiting middleware — operator approved scope expansion in turn 7." |
| **Necessary deviation** | Divergence forced by upstream constraint (dep version, platform behavior, spec ambiguity). | "Spec said `requests` but project pinned `httpx`; behavioral equivalence preserved." |
| **Drift** | Divergence with no explicit approval and no forcing function — silent scope migration. | "Tasklist said `auth.py`; PR also touched `session.py` and `cookies.py` without justification." |
| **Regression** | Divergence that breaks previously-working behavior or invariants. | "Tests claim PASS but `pytest` shows 3 failures in `test_auth.py`." |

The features in the matrices map to deviation classes they help detect (each row's value description explicitly cites this).

---

## 5. Items deliberately excluded from both matrices (with rationale)

For research-agent context: do **not** re-research these. They were evaluated and excluded.

| Feature | Why excluded |
|---|---|
| `list_dir`, `find_file`, `read_file` | Serena-native filesystem ops are worse than native `Read`/`Grep`/`Glob` for sc:reflect — they introduce a freshness re-verification gap relative to the CLAUDE.md S1 "Context freshness discipline" rule, with no offsetting benefit. |
| Dashboard / built-in audit log surface | Duplicates information already captured in sc:reflect's own `audit.log` + `serena-checkpoints.log`. |
| HTTP/SSE transport + multi-agent shared instance | High infrastructure cost; cross-skill platform work, not sc:reflect-local. Defer to a separate platform initiative. |
| `initial_instructions` | Marginal — adds ~1K tokens to each subagent for marginally better tool-use accuracy. Better invested in `refs/reviewer-spec.md` specificity. |
| `restart_language_server` | Pure resilience; cheap insurance but low impact. Acceptable to wire in as an unobtrusive fallback retry; does not warrant its own research depth. |
| `switch_modes` + custom Contexts/Modes | Medium-high cost (new `.serena/contexts/sc-reflect.yml`, drift risk vs. upstream Serena evolution) for only Medium value. |
| Symbolic editing tools — `insert_before_symbol`, `insert_after_symbol`, `replace_symbol_body`, `rename_symbol`, `safe_delete_symbol`, `replace_content` | **Mutate project source code.** Out-of-scope for sc:reflect under the posture clarification in §3. Route to **Tier 3 task-builder** as the remediation execution surface — research these as part of task-builder enhancement, not sc:reflect. |

---

## 6. Cross-references

- **Skill source of truth:** `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (then `make sync-dev`).
- **Refs directory:** `src/superclaude/skills/sc-reflect-protocol/refs/` — `deviation-taxonomy.md`, `reflection-rubric.md`, `reviewer-spec.md`, `report-template.md`, `promotion-adapters.md`, `input-resolution.md`, `grader-extensions.md`.
- **Eval workspace:** `.dev/eval-workspaces/sc-reflect/` — `SPEC.md`, `cases/`, `evals/`, `grader.py`, `aggregate_iteration.py`.
- **Brainstorm source:** `.dev/brainstorms/sc-reflect-rebuild/` — `merged-requirements.md`, `seed-brief.md`, `integration-analysis.md`, `spec-panel-review.md`.

---

## 7. Sources consulted

Primary references used to compile the two matrices:

- [Serena CHANGELOG (oraios/serena)](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — v1.5.x feature additions including `search_deps` semantics and tool-search-friendly descriptions.
- [Serena MCP — feature catalog (mcpservers.org)](https://mcpservers.org/servers/serena-mcp-server) — retrieval / refactoring / memory taxonomy.
- [Serena tool list (LobeHub mirror of llms.txt)](https://lobehub.com/mcp/oraios-serena) — complete tool inventory.
- [Serena onboarding & memory docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md).
- [Serena client/context/modes docs](https://oraios.github.io/serena/02-usage/030_clients.html).
- [Serena MCP user guide — execute_shell_command, prepare_for_new_conversation](https://vibetools.net/posts/serena-mcp-complete-guide).
- This session's `mcp__serena__*` tool surface as the ground truth of what's actually exposed in the current Serena MCP version.

---

## 8. Expected research-agent output shape

For each row in `01-matrix-low-complexity.md` and `02-matrix-medium-complexity.md`, the research agents should append (below the `<!-- BEGIN: research-agent appended content -->` marker in each file) a structured deep-dive containing at minimum:

1. **Canonical documentation** — official Serena docs reference (URL + section), context7 retrieval where available.
2. **Tool signature** — exact parameter shape, return type, error modes.
3. **Best-practice usage patterns** — what the Serena maintainers and adopters recommend.
4. **Failure modes / gotchas** — known issues, language-server quirks, version dependencies.
5. **Sample use case(s) tied to sc:reflect** — concrete invocation showing how the feature would integrate into a specific wave (Wave 0 / 1A / 1B.3 / 5) of sc:reflect. Code/CLI snippets welcome.
6. **Interaction with other sc:reflect mechanics** — rubric inputs affected, audit-log fields emitted, return-contract additions, fail-open behavior.

The point of the research pass is to produce a document that a future sc:reflect-V3 task-builder can lift directly into an MDTM task file. Be implementation-precise.
