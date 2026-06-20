# R1 — File Inventory: sc-bare-review SKILL.md + 3 scripts + refs

**Status: Complete**
**Researcher:** R1 (File Inventory)
**Scope:** `src/superclaude/skills/sc-bare-review/` — legacy SKILL.md + 3 scripts + refs/.
**Goal:** Document exact current structure so a builder can plan a ~60-line thin-caller rewrite that delegates to the already-built swarm CLI (`swarm run --lens bare-review`).

All paths relative to repo root `/config/workspace/IronClaude`.

---

## 0. Directory inventory (with sizes / line counts)

```
src/superclaude/skills/sc-bare-review/
├── SKILL.md                         231 lines / 11185 B   (legacy thick orchestrator)
├── scripts/
│   ├── t2_preflight.sh              219 lines /  9976 B   (Wave A+B)
│   ├── t2_dispatch.sh               112 lines /  5068 B   (Wave C, one reviewer)
│   ├── t2_normalize.py              316 lines / 10429 B   (Wave D+E)
│   └── __pycache__/                 (build artifact — not migration-relevant)
└── refs/
    ├── prompts.md                   101 lines /  4457 B   (system+user prompt SoT)
    ├── output-template.md            99 lines /  4373 B   (per-reviewer §4 template SoT)
    └── templates/
        └── bare-review-output.md    134 lines /  5749 B   (★ ALREADY points at swarm CLI recipe)
```
Evidence: `ls -la` of skill dir + `wc -l` on all scripts/refs.

**MIGRATION HEADLINE:** The swarm CLI replacement already exists and is referenced from within the skill's own `refs/templates/bare-review-output.md`:
- Recipe: `src/superclaude/cli/swarm/recipes/bare_review_v1.py` (`BareReviewV1` class) — verified present.
- Lens: `src/superclaude/cli/swarm/lenses/bare_review.py` — verified present.
- Entry: `swarm run --lens bare-review` (R2's scope; `--lens` plumbing in `src/superclaude/cli/swarm/commands.py:913-979`).
So the thin-caller rewrite drops the 3 scripts and their bash/curl/jq/Python transport, and instead shells out to the swarm CLI lens. R1 confirms the legacy surface; R2 confirms the CLI surface that replaces it.

---

## 1. SKILL.md (231 lines) — section structure + what a ~60-line thin caller keeps vs drops

### 1.1 Frontmatter (lines 1-6)
- `name: sc-bare-review` (L2)
- `description:` (L3) — "dispatches 2-4 bare reviews … via OpenAI-compatible proxy, normalizes into compressed-markdown … returns a contract handing files to /sc:adversarial --suspect-source. Delegate-only — no slash command."
- `allowed-tools: Read, Glob, Grep, Bash, Write` (L4)
- `model: sonnet` (L5)

**KEEP (rewrite):** name, delegate-only framing, suspect-by-construction identity, hand-off to `/sc:adversarial --suspect-source`. **DROP/REVISE:** `allowed-tools` likely narrows to `Read, Bash` (no Write/Glob/Grep needed if a single `swarm run` call owns all file I/O). `model: sonnet` stays (still deterministic orchestration).

### 1.2 Extended metadata comment (lines 10-19)
HTML-comment block: `category: infrastructure`, `personas: [analyzer, qa]`, `delegate-only: true`, `suspect-by-construction: true`, plus **spec/roadmap pointers** (L17-18): spec `merged-requirements.md (v1.3.0-draft §3,§4,§7,§8,§9.1)`, `roadmap: M9 / R-135 / FR-029 / COMP-033`. **KEEP** (cheap provenance) — but the migration should add an M8/M9 "now delegates to swarm CLI" note.

### 1.3 Purpose & Identity (lines 21-46)
- L23-28 native-instinct framing + suspect:true gating → **/sc:adversarial --suspect-source**. **KEEP** (core identity, model-agnostic).
- L30-37 "What this skill IS": (a) pure delegation target wired in Phase 3 callers (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:adversarial`); (b) **"thin orchestrator over three bundled scripts"** — L35-37. **THIS LINE IS THE MIGRATION TARGET** — must change from "three bundled scripts" to "thin caller over `swarm run --lens bare-review`."
- L39-44 "What this skill IS NOT": not user-invoked, not a judge, not Anthropic-routed. **KEEP** (still true post-migration).
- L46 Compliance tier STANDARD. **KEEP.**

### 1.4 Required Input (§3.2) (lines 48-59) — THE CALLER-FACING OPTION SURFACE
This is the caller-facing flag contract the thin caller must preserve (or re-map onto swarm CLI flags):

| Flag (L) | Semantics | Default |
|----------|-----------|---------|
| `--target <path>` (L52) | File to review | REQUIRED |
| `--reviewers <N>` (L53) | Count, 2-4 | 3 |
| `--output <dir>` (L54) | Output directory | REQUIRED |
| `--target-line-cap <N>` (L55) | Truncate target to first N lines | 4000 |
| `--timeout-sec <N>` (L56) | Per-reviewer hard timeout | 180 / `T2Timeout` |
| `--label <string>` (L57) | Optional context label baked into prompt | (empty) |
| `--c7 / --c7-libs / --c7-query-cap` (L58) | accepted by callers, no-op here (Phase 1.5) | n/a |

**KEEP all 6 primary flags** — callers already pass these. The thin caller's job is to MAP them onto the swarm CLI lens flags (R2 owns the target flag names). The `--c7*` no-op trio (L58) can stay documented as accepted-but-no-op.

### 1.5 Triggers (lines 61-64), Prerequisites (lines 66-70)
- Triggers: delegate-only, no slash trigger. **KEEP.**
- Prereqs (L68-70): `T2ProxyUrl` + `T2ProxyKey` env + `curl`+`jq` on host; preflight STOPs with actionable msg; points at `docs/t2-proxy-setup.md`. **MIGRATION:** env vars (`T2ProxyUrl`/`T2ProxyKey`/`T2Model01..04`/`T2Timeout`/`T2Temperature`) likely still required but now consumed by the swarm CLI, not the bash preflight. The `curl`+`jq` host requirement DROPS if the swarm CLI uses a Python transport (R2 to confirm transport).

### 1.6 Behavioral Protocol (lines 72-133) — ★ THE BULK OF WHAT GETS DELETED
- L74-80 `SKILL_DIR` resolution (installed-vs-dev `$HOME/.claude` fallback to `src/`). **DROP** if the swarm CLI is invoked as `superclaude swarm run` (no script-dir resolution needed); KEEP a minimal variant only if scripts are retained.
- **Wave A+B — Preflight** (L82-99): runs `t2_preflight.sh`; non-zero→STOP+relay stderr; exit-3 empty-target relays `failed` contract; on success Read `manifest.json` for `reviewers[]` (index, model_id, model_label, raw_path, meta_path, final_path) + timeout_sec/temperature/prompts_dir. **DROP** — swarm CLI internalizes preflight.
- **Wave C — Parallel dispatch** (L101-121): the **MANDATORY single-message N-Bash-call structural assertion (AC-1.5 / IMM-3)** (L103-108), then one `t2_dispatch.sh` per reviewer (L112-118). **DROP** the entire manual parallel-dispatch ceremony — the swarm CLI does fan-out internally. *This is the single biggest deletion and the main reason the file shrinks from 231→~60 lines.*
- **Wave D+E — Normalize + contract** (L123-133): `uv run python t2_normalize.py --manifest …`; writes `bare-review-NN-<model>.md`, emits `return-contract.yaml`, prints contract. **DROP** — swarm CLI emits the contract.

### 1.7 Return Contract (§3.3 Wave E) (lines 135-160) — ★ KEEP (it is the skill's output contract)
- L137-154 the YAML schema: `contract_version, status (success|partial|failed), target, target_checksum, target_truncated, reviewers_requested, reviewers_succeeded, output_files[] (path/model_id/model_label/bytes/status/elapsed_ms), suspect:true (always), recommended_next_command`.
- L156-158 status rule **IMM-5 success-first:** `M==N`→success; `2≤M<N`→partial; `M<2`→failed; `M==N==2`→success.
- L160 write-on-failure (contract written on every invocation).
**KEEP this section verbatim** — it is the caller-facing output the swarm CLI must reproduce. Migration-critical: the builder must verify the swarm CLI emits a byte-compatible contract (status enum, success-first rule, suspect:true, recommended_next_command with literal `--suspect-source`).

### 1.8 Failure Modes (§8) (lines 162-177)
13-row table mapping each failure → behavior (env unset→STOP; reviewers out of [2,4]→STOP; target missing→STOP; <50 non-ws bytes IMM-4→STOP+`failed`/`target-too-small`, no dispatch; curl/jq missing→STOP; 5xx→retry-once-then-proxy_error; 4xx→no-retry proxy_error; timeout; parse_error+salvage; M<2→failed; 2≤M<N→partial; adversarial-fails-later→artifacts preserved). **KEEP the behavioral contract** (these are guarantees callers rely on) but **the "where enforced" column shifts** from scripts to swarm CLI. The curl/jq row (L168) likely DROPS.

### 1.9 Boundaries (§3.4) (lines 179-186)
Will / Will-NOT lists (read target, N parallel calls, per-reviewer hard timeout, continue ≥2, always suspect:true, emit recommended_next_command, write only inside --output / NOT judge/filter/score/retry-beyond-one-5xx/route-Anthropic/write-outside-output). **KEEP** — behavioral, model-agnostic.

### 1.10 MCP Integration (188-193), Model Recommendation (195-198), Acceptance Criteria §9.1 (200-216), Acceptance Pointers (218-225), footer (227-231)
- MCP (L188-193): Phase-1 = Bash+curl+jq; MCP transport Phase 5. **REVISE** post-migration (transport now owned by swarm CLI).
- AC §9.1 (L200-216): **AC-1.1..AC-1.12** — these are the acceptance contract. **KEEP** (they define correctness) but AC-1.1 (L202-203 "Skill at src/…/SKILL.md; make sync-dev copies to .claude/") and AC-1.5 (L207-208 single-message dispatch) need migration-aware rewording: AC-1.5's "single message" assertion is meaningless once the CLI fans out internally.
- Acceptance Pointers (L218-225): test pointers to `tests/swarm/test_imm_suite.py`, `test_imm3_parallel.py`, `test_imm4_empty_target.py`, `test_imm5_status.py`, `test_imm6_atomic_write.py`, and **parity `tests/swarm/test_bare_review_parity.py`** (L224-225). **MIGRATION-CRITICAL** — R3 owns the parity test; the thin caller must keep these guarantees green. (Note: the swarm template ref also cites `test_recipe_bare_review.py` byte-identity parity — §1.11 / R3.)
- Footer (L227-231): "v1.0 — Phase 1 … Bash+curl reference transport … Source of truth: src/…; run make sync-dev." **REVISE** version/phase note for the migration.

### 1.11 Quantified KEEP-vs-DROP for the ~60-line thin caller
| SKILL.md region | Lines | ~count | Disposition |
|---|---|---|---|
| Frontmatter | 1-6 | 6 | KEEP (revise allowed-tools) |
| Extended metadata | 10-19 | 10 | KEEP (+M8/M9 note) |
| Purpose & Identity | 21-46 | 26 | KEEP, but **L35-37 "three bundled scripts" → "swarm CLI lens"** |
| Required Input §3.2 | 48-59 | 12 | KEEP (map flags onto swarm lens) |
| Triggers + Prereqs | 61-70 | 10 | KEEP (drop curl/jq host req) |
| **Behavioral Protocol Waves A/B/C/D/E** | **72-133** | **~62** | **DROP almost entirely → one `swarm run --lens bare-review …` invocation block (~6-10 lines)** |
| Return Contract §3.3 | 135-160 | 26 | KEEP verbatim (CLI must reproduce) |
| Failure Modes §8 | 162-177 | 16 | KEEP behavior, shift enforcement col |
| Boundaries §3.4 | 179-186 | 8 | KEEP |
| MCP / Model / AC / Pointers / footer | 188-231 | ~44 | KEEP AC + pointers; REVISE MCP/phase/footer |

**Net:** the ~62-line Behavioral Protocol (Waves A→E, incl. the AC-1.5 single-message assertion and 3 script invocations) is the migration-relevant deletion. Everything else (identity, flag surface, return contract, failure modes, boundaries, ACs, test pointers) is **boilerplate-to-preserve**: it describes WHAT the skill guarantees, which the swarm CLI must continue to honor. A ~60-line thin caller = preserved sections + a single `swarm run --lens bare-review` call replacing the 4 wave blocks.

---

## 2. The 3 scripts — CLI arg surface, behavior, exit-code contract (what the swarm CLI must already replicate)

### 2.1 `scripts/t2_preflight.sh` (219 lines) — Wave A (prereqs) + Wave B (target ingestion)
**CLI flags** (parse loop L28-38):
- `--target <path>` REQUIRED (L30, validated L45)
- `--reviewers <2-4>` REQUIRED (L31, validated L46,49-50 integer + range AC-1.4)
- `--output <dir>` REQUIRED (L32, validated L47)
- `--target-line-cap <N>` default `4000` (L33; default L25; applied L91-96)
- `--timeout-sec <N>` default `T2Timeout` else `180` (L34; resolved L74)
- `--label <str>` optional (L35; prompt injection L172)
- Unknown arg → `die "unknown argument"` (L36).

**What it does (2 sentences):** Validates args+env (`curl`+`jq` present L41-42; `T2ProxyUrl`+`T2ProxyKey` set L53-54), resolves the N reviewer models with defaults (`T2Model01..04` → `deepseek-v4-pro`/`qwen3.6-plus`/`kimi-k2.6`/`glm-5.1`, L57-67; caps N≤configured L70-71), reads + truncates the target to the line-cap (L88-96), computes the 12-hex SHA-256 provenance checksum (L101, AC-1.10), enforces the IMM-4 empty-target guard (<50 non-whitespace bytes → writes `failed`/`target-too-small` `return-contract.yaml` and exits 3, L109-125), builds the shared `system.txt`+`user.txt` reviewer prompts under `<output>/.prompts/` (L128-176), and emits `<output>/manifest.json` with per-reviewer `{index, model_id, model_label, raw_path, meta_path, final_path}` plus `timeout_sec/temperature/prompts_dir/contract_path/caller_label` (L178-216).

**Exit-code contract** (documented L13-16):
- `0` = proceed to dispatch (manifest written) — success line L218-219.
- non-zero (default `1` via `die`) = STOP, message on stderr.
- `3` = IMM-4 empty-target — a `failed` `return-contract.yaml` is written FIRST (L111-123) then `die "Target too small …" 3` (L124).
- `set -euo pipefail` (L20) → any unguarded failure aborts non-zero.

### 2.2 `scripts/t2_dispatch.sh` (112 lines) — Wave C, ONE reviewer (invoked N× in parallel)
**CLI flags** (parse loop L23-33):
- `--model <id>` REQUIRED (L25; checked L52-53)
- `--prompt-dir <dir>` REQUIRED (L26; checked L52-53)
- `--raw-out <path>` REQUIRED (L27; checked L52-53)
- `--meta-out <path>` REQUIRED (L28; checked L52-53)
- `--timeout <sec>` default `180` (L29)
- `--temperature <float>` default `0.2` (L30)
- Unknown arg → stderr + **`exit 2`** (L31).

**What it does (2 sentences):** Builds an OpenAI-compatible chat-completions JSON body from `<prompt-dir>/system.txt`+`user.txt` (target JSON-escaped via `jq --arg`, never shell-interpolated — L57-65), POSTs it to `${T2ProxyUrl%/}/chat/completions` with `--max-time <timeout>` (L67-80), retries ONCE after 2s on HTTP 5xx and never on 4xx (§8, L88-92), extracts `.choices[0].message.content` (L104), and writes the review markdown to `<raw-out>` plus a `<meta-out>` sidecar carrying `{status, http_code, elapsed_ms, attempts, model_id}` (write_meta L37-50).

**Exit-code contract** (documented L15-16): **Always exits 0 after writing meta.json** — reviewer status lives in the sidecar `status` field, not the exit code (so siblings never abort, AC-1.7). Status enum written to meta: `success` (L111), `timeout` (curl rc 28, L84/91), `proxy_error` (non-2xx / transport error / missing env, L55/99), `parse_error` (2xx but no extractable content, L107). **Exception:** `exit 2` only for missing-required-flags / unknown-arg (L31, L53) — a usage error, before any network work.

### 2.3 `scripts/t2_normalize.py` (316 lines) — Wave D (normalize) + Wave E (return contract)
**CLI flags** (argparse L264-266):
- `--manifest <path>` REQUIRED (`required=True`, L265) — points at `<output>/manifest.json`.
- (No other flags; everything else read from the manifest.)

**What it does (2 sentences):** Reads the manifest, and per reviewer reads its `.raw` + `.meta.json`, strips any model-emitted frontmatter, parses the findings table / verdict / notes (`parse_findings` L87-107, `extract_section` L110-119), applies §7.4 parse_error salvage (promotes a recoverable `parse_error` body to `success`, L200-205), and atomically writes (`atomic_write` tmp+`os.replace`, IMM-6, L149-158) the final `bare-review-NN-<model>.md` with authoritative frontmatter (schema_version/tier/suspect:true/checksum/elapsed_ms/generated/finding_count, L207-221). Then it computes aggregate status via the IMM-5 success-first rule (L284-290: `M==requested`→success; `M>=2`→partial; else failed), builds `recommended_next_command` = `/sc:adversarial --compare <existing-review>,<bare…> --suspect-source <bare…>` (L292-295), and emits the Wave-E `return-contract.yaml` always (write-on-failure, `emit_contract` L233-260).

**Exit-code contract** (documented L8-9, L311-312): **Always exits 0** — "status lives in the contract; M<2 is a domain outcome, not a crash" (L311). Aggregate `status` (success/partial/failed) is carried in the YAML contract, not the process exit code. (Stdlib-only, no third-party deps, L14.)

**Cross-script normalization domain (migration parity surface):** severity alias map `SEV_ALIASES` (L25-40, unknown→`med`), empty-cite set `EMPTY_CITE` (L41, →`none`), finding-id regex `^f-?\d+$` (L42), claim ≤120 chars + newline-flatten (L96), conf clamp 0-100 (L80-84), verdict cap 300 / notes cap 200 (L197-198), `yaml_str` C0-control escaping (L49-61). **These exact semantics are what the swarm `BareReviewV1` recipe must reproduce byte-identically** (see §3 — the swarm template ref already documents the same alias map / caps and pins a byte-identity parity test).

---

## 3. refs/ + templates — which survive migration

### 3.1 `refs/prompts.md` (101 lines) — system + user prompt source of truth
- System prompt SoT (L25-73) instantiated by preflight into `<output>/.prompts/system.txt`; user prompt SoT (L83-90) → `user.txt`. Documents the bare-framing rationale, the `<<<TARGET>>>…<<<END TARGET>>>` injection guard (§11.5, L13-17/L31-35), and the `jq --arg` dispatch-time escaping defense (L97-102).
- **MIGRATION STATUS:** The PROMPT CONTENT survives — but ownership moves. The swarm recipe/lens needs the identical system/user prompt text. **R1 flag:** the builder must confirm whether the swarm lens reads these prompts from `refs/prompts.md` or carries its own copy (parity risk if duplicated). Currently `prompts.md` is consumed only by `t2_preflight.sh` (L86, L127); once that script is gone, `prompts.md` is orphaned UNLESS the lens references it.

### 3.2 `refs/output-template.md` (99 lines) — per-reviewer §4 template + field semantics
- Documents the §4.1 template + §4.2 field-ownership table + findings-column semantics + normalizer contract (L92-99). Consumed conceptually by `t2_normalize.py`.
- **MIGRATION STATUS:** Documentation survives (the output SHAPE is unchanged post-migration). But it describes the LEGACY normalizer. The authoritative template post-migration is `refs/templates/bare-review-output.md` (§3.3). **R1 flag:** these two template docs overlap; builder should decide whether `output-template.md` is demoted/cross-linked to the swarm version or kept for the legacy pipeline. Its own provenance section in the sibling file (below) already calls it "kept in place for the legacy bash/Python pipeline under scripts/" — i.e. it becomes dead once scripts are removed.

### 3.3 `refs/templates/bare-review-output.md` (134 lines) — ★ THE MIGRATION BRIDGE (already swarm-aware)
This file is **already written for the post-migration world** and is the strongest single piece of migration evidence in R1's scope:
- L2-10 declares it "Canonical Wave-2 output template for the `bare-review-v1` recipe (`src/superclaude/cli/swarm/recipes/bare_review_v1.py`) and the `bare-review` bundled lens (`src/superclaude/cli/swarm/lenses/bare_review.py`)." Pinned by `merged-requirements.compressed.md §12`. Validator **U-008 (T02.16)** asserts the path resolves; **`BareReviewV1.normalize` emits a byte-identical body** to the placeholders.
- L49-92 maps every frontmatter/findings/section placeholder to its recipe owner (`args[...]`), re-states the same `normalize_sev`/`normalize_cite`/`parse_conf` semantics and verdict-300/notes-200 caps as the legacy `t2_normalize.py` — i.e. the recipe is a faithful port.
- L96-101 AC-011 boundary (recipe MUST NOT score/dedupe/reorder) enforced by `tests/swarm/test_recipe_no_judging.py` (T04.14).
- L119-122 cites **`tests/swarm/test_recipe_bare_review.py` byte-identity parity gate against legacy `t2_normalize.py` (TEST-003 / M8 gate)** — confirms the M8 parity milestone.
- L126-133 Provenance: legacy parent template (`refs/output-template.md`) "kept in place for the legacy bash/Python pipeline under scripts/"; Wave-2 recipe = `bare_review_v1.py`.
- **MIGRATION STATUS:** SURVIVES and becomes primary. After the scripts are removed, this is the live template doc; `output-template.md` (§3.2) becomes legacy/dead.

### 3.4 `__pycache__/`
`scripts/__pycache__/` is a Python bytecode build artifact — not migration-relevant; will disappear when `t2_normalize.py` is removed.

---

## 4. R1 summary for the builder

1. **The replacement already exists.** `swarm run --lens bare-review` + `bare_review_v1.py` recipe + `bare_review.py` lens are present and the skill's own `refs/templates/bare-review-output.md` documents them as the canonical Wave-2 path, with an M8 byte-identity parity gate (`tests/swarm/test_recipe_bare_review.py`). The migration is "make SKILL.md a thin caller over that CLI and delete the 3 scripts," not "build new transport."

2. **The ~62-line Behavioral Protocol (SKILL.md L72-133, Waves A→E)** is the deletion target — including the AC-1.5 single-message parallel-dispatch ceremony (L101-121) and the 3 script invocations (L88-92, L112-118, L126-127). Replace with one `swarm run --lens bare-review …` block.

3. **Preserve as the skill's external contract:** the §3.2 flag surface (L48-59: `--target`/`--reviewers`/`--output`/`--target-line-cap`/`--timeout-sec`/`--label`, mapped onto swarm lens flags — R2 owns target names), the §3.3 Return Contract (L135-160: status enum + IMM-5 success-first + suspect:true + `recommended_next_command --suspect-source`), the §8 Failure Modes behavior (L162-177), the §3.4 Boundaries (L179-186), and the §9.1 ACs + test pointers (L200-225, incl. parity `tests/swarm/test_bare_review_parity.py`).

4. **3 scripts replicate exactly what the CLI must already do** (parity surface): preflight (args/env validation, model resolution w/ `T2Model01..04` defaults, line-cap truncation, 12-hex sha256, IMM-4 <50-byte guard→exit 3 + `failed` contract, prompt build, manifest); dispatch (per-reviewer OpenAI proxy call, 5xx-retry-once/4xx-no-retry, always-exit-0 status-in-sidecar); normalize (sev alias map / cite normalization / conf clamp / verdict-300 / notes-200 / §7.4 salvage / atomic IMM-6 write / IMM-5 status / write-on-failure contract / always-exit-0).

5. **refs disposition:** `refs/templates/bare-review-output.md` SURVIVES (becomes primary, swarm-aware). `refs/output-template.md` + `refs/prompts.md` are LEGACY-tied to the scripts — builder must decide cross-link vs delete, and **must verify the swarm lens carries identical prompt text** (parity risk if `prompts.md` is orphaned while the lens duplicates the prompt).

**Status: Complete**
