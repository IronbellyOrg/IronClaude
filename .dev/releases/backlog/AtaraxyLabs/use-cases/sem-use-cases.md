---
title: "sem (Ataraxy-Labs) — Grounded Use-Case Report for IronClaude"
tool: sem
role: foundation (entity-extraction substrate; gates inspect + weave)
status: use-case-exploration
created: 2026-06-04
grounding: real-file (every use case cites a verified IronClaude path)
language_caveat: "Repo is 8,680 tracked .md vs 759 .py — sem is weakest on Markdown; its real value lands in src/superclaude/ Python (247 .py)."
---

# What sem brings to the table (IronClaude-specific)

IronClaude's review, audit, and reflection surfaces all reason about *line diffs and
whole files*, yet the unit they actually care about is the **entity** — a Python function,
class, or method (and, for the `.md` skill corpus, a heading-delimited section). `sem`
replaces `git diff`'s line view with an entity-aware one: it tells you *which function
changed*, *what depends on it across files* (`sem impact`), *who last touched it*
(`sem blame`), *how it evolved* (`sem log`), and packs *exactly that entity plus its
dependents into a token budget* (`sem context`). For the `src/superclaude/` Python tree —
which holds multi-thousand-line files like `cli/roadmap/executor.py` (3,701 lines) and
`cli/sprint/executor.py` (2,148 lines) where a "10-line diff" can sit anywhere in 40
functions — this entity lens is a genuine precision and token win. The honest ceiling:
the *tracked* repo is ~92% Markdown, sem's weakest language, so its value is **bounded to
the Python surface** and any `.md` use must be treated as best-effort chunking, never a
structural guarantee (this is exactly the CP-1 substrate-trust risk in
`merged-requirements.md`).

---

# Use cases (ranked by value)

## UC-1 — Token-budgeted entity context for `code-review` / `simplify` on big Python files
**Highest value.**

- **Surface:** the built-in `code-review` and `simplify` skills (review/clean the current
  diff), plus the diff-collection step in
  `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` Wave 1
  (`gh pr diff` / `git diff <base>...HEAD` → `diff.patch`).
- **sem command/MCP:** `sem context <entity>` (CLI pre-step) / `sem_context` MCP tool;
  `sem diff` to enumerate the changed entities first.
- **Status-quo pain:** Wave 1 dumps the *whole* `diff.patch` and Wave 2 feeds it to
  Auggie; for a one-function change inside `cli/roadmap/executor.py` (3,701 lines) the
  reviewer pays to carry hunks and surrounding noise it never reasons about. The
  `code-review`/`simplify` skills similarly take the raw diff with no entity scoping.
- **Net value:** `sem context` returns the changed function + its direct
  dependents/dependencies inside a declared token budget — the exact "entity + neighbors"
  payload these skills want. The eval's H-sem-2 target is **≥30% prompt-token reduction vs
  the Auggie pass** at recall within 5pp. On a provider that routes to Claude (~$15/$75 per
  M, per `merged-requirements.md` §6) that is real money; on qwen-default it is advisory
  only.
- **Caveat (honest):** `sem context` **omits the target entity if it exceeds the budget** —
  on a 3,701-line file a single huge function can blow the budget and silently drop the one
  thing under review. The seam must be flag-gated with a byte-identical raw-diff fallback
  (per §8.1 S3), and it only helps for Python/supported-lang diffs — a skill-`.md` edit gets
  no entity scoping.

## UC-2 — Cross-file impact ("what breaks if this changes") for cleanup-audit Pass 2 + troubleshoot regressions
**High value.**

- **Surface:** `src/superclaude/skills/sc-cleanup-audit-protocol/rules/pass2-structural-audit.md`
  — its mandatory 8-field per-file profile requires field 3 **"Who/what references this
  file?"** and a STRUCTURAL-ISSUE check for "dead imports, unused exports, circular deps,"
  with every KEEP/DELETE needing grep-proven references. Also
  `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (regression-after-refactor
  hypotheses).
- **sem command/MCP:** `sem impact <entity>` / `sem_impact`; `sem entities <path>` to
  enumerate before scoring.
- **Status-quo pain:** Pass 2 establishes references with **hand-run grep**, which is
  line/string-based — it can't tell a real call from a comment, misses renames, and can't
  build a directed dependency graph to spot a *transitively* dead entity. Troubleshoot's
  "what else does this refactor touch" is likewise manual.
- **Net value:** `sem impact` gives a real cross-file dependency graph keyed on the symbol,
  so a DELETE recommendation can cite "0 dependents in the impact graph" instead of "grep
  found nothing" — higher-confidence dead-code calls and a fast "blast radius" answer for
  regression triage (the eval's impact-recall ≥70% / precision ≥50% target).
- **Caveat (honest):** impact precision is only gated at ≥50%, so it's a *lead generator*,
  not proof — Pass 2's evidence standard (grep file:line) still has to confirm. And the
  audit's scope is the whole repo including thousands of `.md` skill/doc files where sem
  can't build a symbol graph at all; impact only helps the Python slice.

## UC-3 — Entity-level deviation classification + authorship timeline for `sc:reflect` UC-2 audits
**High value.**

- **Surface:**
  `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` — the UC-2
  post-execution audit classifies every divergence as Authorized / Necessary / Drift /
  Regression, operating on **diff hunks**, with a documented fallback to
  **per-file aggregation once the diff exceeds 100 hunks**.
- **sem command/MCP:** `sem diff` (entity-level units) / `sem_diff`; `sem blame`
  (`sem_blame`) and `sem log` (`sem_log`) for the authorship/evolution timeline that
  anchors the "what was expected" gold standard.
- **Status-quo pain:** hunk-keyed classification fragments a single logical change across
  several hunks, and the >100-hunk fallback collapses to one row *per file* — losing
  per-function resolution exactly when a large refactor most needs it. Establishing "was
  this entity pre-authorized or is it drift" today leans on commit-message narrative, which
  the taxonomy itself flags as untrustworthy.
- **Net value:** `sem diff` makes the natural classification unit a **function/method**, so
  the >100-hunk case can aggregate per-entity (finer than per-file) and `sem blame`/`sem log`
  give an objective "this method last changed in commit X by author Y" timeline to separate
  Authorized expansion from silent Drift — directly strengthening the taxonomy's weakest
  evidence link.
- **Caveat (honest):** reflect audits frequently target **skill/spec `.md` files** (the
  taxonomy's own gold standard is "the driving spec/tasklist"), where sem degrades to
  chunk fallback — so the entity-diff upgrade is real for Python deviations but near-zero
  for the Markdown-spec deviations reflect most often audits.

## UC-4 — Entity-granular freshness gate (fewer false blocks in the parallel-dev / worktree model)
**Medium value (highest novelty).**

- **Surface:** `src/superclaude/hooks/scripts/freshness-pre-edit.sh` — the PreToolUse gate
  that blocks an Edit when the **file** wasn't Read in the last 30 min, documented in
  `docs/user-guide/freshness-hooks.md`. Pairs with the heavy `git worktree` parallel-Claude
  model in `CLAUDE.md`.
- **sem command/MCP:** `sem blame` / `sem_blame` (and `sem diff` against the last-Read
  snapshot) to answer "did *the entity I'm about to edit* change, or just some other
  function in this file?"
- **Status-quo pain:** the gate is **whole-file** granularity. In the worktree model,
  another session (or the same one) can touch an unrelated function in a 2,000-line file;
  today that would force a full re-Read of the whole file to clear the block even though the
  function under edit is untouched. (Note: v1 actually *stripped* external-change detection —
  see `freshness-hooks.md` "Known limitations" — so this is also a path to *restore* that
  capability at entity resolution.)
- **Net value:** an entity-aware check could distinguish "the function you're editing is
  stale" (real block) from "an unrelated entity in the same file changed" (safe to proceed),
  cutting false freshness blocks on the large `executor.py`-class files where many functions
  coexist — fewer forced re-Reads, less churn in parallel sessions.
- **Caveat (honest):** this is a **net-new hook capability, not a drop-in** — the gate is a
  fail-open Bash script with a hard "never pivot to escape the hook" contract
  (`feedback_no_strategy_pivot_to_avoid_hooks.md`); adding a Rust binary to the hot edit path
  risks latency and a new failure mode on every Edit, and it does nothing for `.md` skill
  edits (which are the bulk of edits in this repo). Lowest-ranked because the cost/benefit on
  the edit hot-path is the least certain.

---

# Where sem does NOT help

- **The Markdown majority.** 8,680 of ~12,000 tracked files are `.md` (skills, commands,
  agents, docs, `.dev/` artifacts). sem is explicitly weakest on Markdown and falls back to
  opaque chunking, so every `.md`-centric workflow — most of `sc:roadmap`, `sc:tasklist`,
  the brainstorm/adversarial artifact merges, doc review, and the spec-side of reflect —
  gets little to no structural benefit. CP-1 in `merged-requirements.md` is correct to make
  `.md` substrate trust a hard halt gate.
- **`sc:git` commit-message generation.** `src/superclaude/commands/git.md` is about
  conventional-commit synthesis and staging workflow, not dependency/impact reasoning —
  sem adds nothing here (weave, not sem, is the merge-driver candidate).
- **Roadmap *semantic* layer.** `src/superclaude/cli/roadmap/semantic_layer.py` reasons over
  spec/roadmap *prose* under a 30 KB prompt budget (`MAX_PROMPT_BYTES`) — a natural-language
  comparison problem, not a code-entity-graph problem. sem's structural diff doesn't apply.
- **Pure-text / non-code artifacts:** `.txt` corpora, `.jsonl` execution logs, `.err`
  fixtures, crash-recovery's `manifest.json`/`execution-log.jsonl` scanning — all string/JSON
  scanning where `git diff` + `jq` already suffice.
- **Cheap-provider token economics.** Per G0-2 / §6, if framework review routes to
  qwen3.6-plus (~$0.40/$1.20 per M), the headline token-savings value in UC-1 collapses to
  economically-irrelevant cents/quarter and sem must justify itself on latency/precision
  alone.
