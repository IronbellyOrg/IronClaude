# Code Review: PR #64 — feat(skills): add sc-auggie-review-protocol

**Target**: [PR #64](https://github.com/IronbellyOrg/IronClaude/pull/64)
**Reviewer**: `/sc:auggie-review` (depth=standard, focus=all)
**Generated**: 2026-05-20 21:30 UTC
**Base ↔ Head**: master ↔ feature/sc-auggie-review-protocol (head SHA `36df860`)
**Stats**: 11 files, 1369 lines, 10 findings (0 dropped during grounding) + 1 cross-cutting observation
**Auggie version**: 0.27.2 (commit 23e29db5), single-pass invocation, --max-turns 16

---

## Summary

**Verdict: Approve with comments.** Zero Critical, zero High after rubric remap. Four Medium findings worth addressing in this PR (cheap fixes); four Low + two Nits that can be follow-ups or accepted.

Top three concerns to address before merge:

1. **`PostToolUse` matcher fires `jq` on every Bash invocation** — the hook is unconditionally invoked for every Bash tool call in the session and runs `jq` four times before the early-exit regex check on line 29. Real perf cost, low risk, but easy to mitigate with a fast string check before the first `jq`.
2. **SKILL.md line 166 documents an incomplete extraction pipeline** — the snippet omits the `tail -n +2` preamble strip that line 167 says is mandatory under `--max-turns`. A reader who copies the line 166 example without reading line 167 will hit `jq` parse errors. (This is the meta-finding: this very review caught it because our own pipeline starts with `tail -n +2`.)
3. **`evals/evals.json` has empty `assertions: []` for all three scenarios** — the validation history says "100% pass" but there is no programmatic assertion logic to back that up. For a 362-line advanced-tier skill with external dependencies, this is a real regression-coverage gap.

The remaining findings are defense-in-depth (XML escaping, jq-availability check), style (regex escaping inside `[...]`), or pre-existing patterns this PR follows rather than introduces.

## Findings

### 🟡 Medium (fix in this PR if cheap, otherwise file followup)

#### M1. `PostToolUse` matcher `"Bash"` fires the hook on every Bash invocation; `jq` runs unconditionally before the regex early-exit

- **File**: [`.claude/settings.json:18`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/.claude/settings.json#L18)
- **Category**: performance
- **Source**: auggie
- **Evidence**:

  ```json
  "matcher": "Bash",
  ```

- **Why this matters**: Claude Code's PostToolUse `matcher` is a regex against the tool **name**, so `"Bash"` matches every Bash invocation in the session — `git status`, `auggie`, `jq`, `grep`, every probe. The hook script's first action ([`offer-pr-review.sh:20`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L20)) is a `jq` call, and three more `jq` calls (lines 23, 34, 39) may run before the `gh pr create` regex on line 29 short-circuits. With a 3 s per-invocation timeout × hundreds of Bash calls per session, this is measurable overhead even on the happy path.
- **Recommendation**: Add a pre-`jq` substring check at the top of the script — `case "$INPUT" in *'"command"'*'gh'*'pr'*'create'*) ;; *) exit 0;; esac` — so the hook returns in microseconds for the 99% of Bash calls that aren't `gh pr create`. Reserve `jq` parsing for the one-in-a-hundred case that actually matches. (Note: the suggested matcher-side narrowing — `"Bash(gh *)"` — is permissions syntax, not hook-matcher syntax, so the fix has to live in the script.)

#### M2. `SKILL.md` Wave 2 documents an incomplete JSON-extraction pipeline that fails under `--max-turns`

- **File**: [`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:166`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md#L166)
- **Category**: correctness (docs/recipe)
- **Source**: auggie
- **Evidence**:

  ```text
  Recommended: `sed -n '/^```json$/,/^```$/p' auggie-raw.json | sed '1d;$d' | jq '.'` or equivalent.
  ```

- **Why this matters**: Line 167 (the next pitfall bullet) correctly states that under `--max-turns` Auggie prepends `Applying --max-turns override: N over agentMaxIterations=500` as the first stdout line, and that the strip recipe must begin with `tail -n +2`. But the example on line 166 omits that prefix, so anyone who copies line 166 in isolation hits `jq: parse error: Invalid numeric literal at line 1`. The verified working pipeline (used in `.dev/eval-workspaces/sc-auggie-review/iteration-3/VERIFICATION.md` and re-confirmed by this very review) is `tail -n +2 <file> | jq -r '.result' | sed -n '/^```json$/,/^```$/p' | sed '1d;$d' | jq '.'`. The recipe also needs the `jq -r '.result'` extraction from the outer envelope, which is missing entirely from line 166.
- **Recommendation**: Replace the line 166 snippet with the full verified pipeline, or rewrite it to forward-reference line 167: `Recommended (when --max-turns is in use): see the next bullet for the full strip recipe including the preamble line.` Better still, consolidate Wave 2's `Common pitfalls` block into a single contiguous recipe block followed by an annotated checklist of failure modes.

#### M3. `offer-pr-review.sh` has non-trivial parsing logic but no test coverage

- **File**: [`src/superclaude/hooks/scripts/offer-pr-review.sh:1`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L1) (whole file, 70 lines)
- **Category**: tests
- **Source**: auggie
- **Evidence**: No `tests/hooks/test_offer_pr_review*.{sh,py}` exists; no entry in `tests/cli/eval/` covers this script.
- **Why this matters**: The hook does JSON parsing (4 × `jq`), bash regex matching of the command (line 29 — a non-trivial pattern), conditional PR-URL/number extraction (lines 40–41), and XML generation that Claude Code parses (lines 56–67). Each of those is a potential silent failure surface. The other project-local hook (`reject-workspace-writes.sh`) is exercised by the `cliEval` `hook_adapter.py` infrastructure on the in-progress `fix/prd-path-resolution-and-templates` branch; this hook gets no equivalent coverage. If the regex on line 29 or the bash `[[ =~ ]]` portability breaks on a future bash version, there's no automated tripwire.
- **Recommendation**: Add `tests/hooks/test_offer_pr_review.py` (or `.sh`) that pipes 4–6 synthetic hook payloads to the script — a matching `gh pr create` success, a `gh pr view` (must not match), a `gh pr create` with `tool_response.error` set (must not fire), a payload with no `command` field, and one with a malformed PR URL. Assert exit 0 in all cases and assert the `<sc-auggie-review-offer>` block appears only for the success case. Model after the `hook_adapter.py` pattern already in the repo.

#### M4. `evals/evals.json` has `"assertions": []` for every scenario; the PR claims "100% pass" without programmatic verification

- **File**: [`src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json:10`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/skills/sc-auggie-review-protocol/evals/evals.json#L10)
- **Category**: tests
- **Source**: auggie
- **Evidence**:

  ```json
  "assertions": []
  ```

  (lines 10, 18, 26 — all three scenarios)
- **Why this matters**: The PR body cites "iter-1: 3 evals × 2 configs, 6 runs, 100% pass" but every assertion array is empty. The iteration-3 verification log (`.dev/eval-workspaces/sc-auggie-review/iteration-3/VERIFICATION.md`) describes a one-off manual verification, not automation. Without assertions, future regressions to (a) the `REVIEW.md` structure, (b) the file:line grounding contract, (c) the severity-rubric remap, or (d) the `gh pr review --comment` posting will pass silently. The skill is exactly the kind that the rubric (and the project's own `evals.json` schema) targets for automated coverage: advanced complexity, external CLI dependency, structured-output contract.
- **Recommendation**: Populate `assertions` for each scenario with at least: (i) `os.path.exists(<REVIEW.md path>)`, (ii) markdown header presence (`# Code Review:`, `## Findings`, `## Audit`), (iii) for every `(file, line)` cited under `### 🔴 Critical` or `### 🟠 High`, assert the file exists and the line range is in-bounds (this is the anti-hallucination tripwire — exactly the property the skill claims as non-negotiable). For the per-PR scenario also assert the report's `Stats` line matches the actual PR file count. This is ~30 lines of assertion code and prevents the entire class of silent-format-drift bugs.

### 🟢 Low (nice-to-have)

#### L1. `offer-pr-review.sh` has no `jq`-availability check; failure mode is silent no-op

- **File**: [`src/superclaude/hooks/scripts/offer-pr-review.sh:20`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L20)
- **Category**: error-handling
- **Why this matters**: `jq -r '...' 2>/dev/null` returns empty string when `jq` is missing or fails, and the subsequent `[ "$TOOL_NAME" = "Bash" ] || exit 0` happily exits 0 — so on a host without `jq` the hook never fires and the user never sees the offer, with zero log trail. The hook is documented as "fail-open" (header comment line 6), which is the right policy, but a one-line diagnostic on first jq failure (written to `~/.claude/logs/offer-pr-review.log` or similar) would prevent the "why isn't the offer firing?" debugging session.
- **Recommendation**: Add `command -v jq >/dev/null 2>&1 || { echo "[offer-pr-review] jq not on PATH; hook disabled" >&2; exit 0; }` near the top. Stderr goes to Claude Code's hook-error sink; the user sees it once and knows what's wrong.

#### L2. `cat <<EOF` block interpolates `$TARGET_HINT` without XML-escaping; trusts `gh` stdout shape

- **File**: [`src/superclaude/hooks/scripts/offer-pr-review.sh:57`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L57) (range 57–67)
- **Category**: security (defense-in-depth)
- **Why this matters**: The XML block emitted to stdout is parsed by Claude Code; if a malicious or malformed `gh pr create` stdout produced a `TARGET_HINT` containing `</sc-auggie-review-offer>` or `<` characters, the block would be malformed. The attack surface requires control over `gh pr create`'s stdout, which is low — but the cost of escaping is also low.
- **Recommendation**: Either escape `&`, `<`, `>` in `TARGET_HINT` before interpolation, or wrap the dynamic content in a CDATA section, or — simplest — change the offer to a non-XML-parsed format (plain text with a `[OFFER]` prefix) and have Claude pattern-match on the prefix instead of relying on XML parsing.

#### L3. `_FRESHNESS_SCRIPTS` registry conflates global-install scripts with project-local hooks; pre-existing pattern, but this PR reinforces it

- **File**: [`src/superclaude/cli/install_hooks.py:75`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/cli/install_hooks.py#L75) (Auggie cited L179 — remapped to the actual `"offer-pr-review.sh",` line)
- **Category**: architecture
- **Why this matters**: `_FRESHNESS_SCRIPTS` triggers `superclaude install` to copy the script into every end-user's `~/.claude/hooks/`, but `offer-pr-review.sh` (like `reject-workspace-writes.sh` before it) is only registered project-locally via `$CLAUDE_PROJECT_DIR/.claude/settings.json`. End-users get a copy of a script that never runs. The PR's own comment block (lines 67–74) acknowledges this and says it's "harmless when unregistered" — true, but the convention now has two scripts following it, which is enough to formalize.
- **Recommendation** (follow-up, not blocking): Introduce a second registry `_PROJECT_LOCAL_SCRIPTS = [...]` in `install_hooks.py` that the `_copy_scripts` step skips. Update the `=== Installer Registration ===` `make verify-sync` gate to recognize both registries. Defer to a follow-up PR — pre-existing pattern, no new debt from this change beyond making the pattern more conspicuous.

#### L4. `.gitignore` convention change has no in-repo documentation

- **File**: [`.gitignore:118`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/.gitignore#L118)
- **Category**: docs
- **Why this matters**: `!.claude/settings.json` codifies a new convention — "everything in `.claude/` is gitignored sync-dev output except `settings.json`". The convention is explained in the PR description and in the contributor's session memory, but a future contributor reading just the repo will see only the bare directive. `CLAUDE.md` documents the `src/` source-of-truth rule but doesn't mention the `settings.json` exception.
- **Recommendation**: Either (a) add a comment immediately above the line — `# Exception: settings.json is project-local hook + permission config and IS committed.` — or (b) add a paragraph to `CLAUDE.md`'s "Component Sync" section. (a) is the minimum; (b) is the durable fix.

### 💬 Nits

- **N1.** [`offer-pr-review.sh:41`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L41) — `PR_NUM` is extracted from `PR_URL` via `grep -oE '[0-9]+$'`, but the URL on line 40 is already required to end in `/pull/[0-9]+`, so `PR_NUM` can only be empty when `PR_URL` is also empty. The branch on lines 48–50 is unreachable. Either remove the dead branch or harden the line-40 regex enough that the branch becomes reachable on a real failure mode. (Auggie filed this as Medium; reduced to Nit because the unreachable-branch consequence is cosmetic, not behavioral.)
- **N2.** [`offer-pr-review.sh:29`](https://github.com/IronbellyOrg/IronClaude/blob/feature/sc-auggie-review-protocol/src/superclaude/hooks/scripts/offer-pr-review.sh#L29) — The character class `[[:space:]\;\&\|]` contains literal backslashes as class members (the `\` before `;`, `&`, `|` is not needed inside `[...]`). The class ends up matching `[<space>\;&|]`, which includes backslash. In practice no shell command starts with `\gh`, so no impact, but the escaping is misleading. Use `[[:space:];&|]` instead.

## Architectural / Cross-Cutting Observations

### CC1. Project-local vs global hook registration pattern is under-documented and the install-time copy of project-local scripts creates dormant payload on every user install

- **Affected files**: `src/superclaude/cli/install_hooks.py`, `.claude/settings.json`, `src/superclaude/hooks/scripts/offer-pr-review.sh`, `src/superclaude/hooks/scripts/reject-workspace-writes.sh`
- **Category**: architecture
- **Why this matters**: Same root cause as L3, but worth surfacing as cross-cutting because it now affects 2/9 entries in `_FRESHNESS_SCRIPTS` and there's no policy preventing #3 from being added later. The `_FRESHNESS_SCRIPTS` list reads like "scripts the global installer manages," but two of them are project-local dormants. The `=== Installer Registration ===` `make verify-sync` gate enforces "every script in `src/superclaude/hooks/scripts/*.sh` must appear in `_FRESHNESS_SCRIPTS`," which prevents drift in one direction but encourages the project-local-script-as-global-copy pattern in the other.
- **Recommendation**: Split the registry as in L3, then update the verify-sync gate to allow `src/superclaude/hooks/scripts/*.sh` to satisfy "in `_FRESHNESS_SCRIPTS` **or** in `_PROJECT_LOCAL_SCRIPTS`." Document in the docstring at the top of `install_hooks.py`. This is a small piece of architecture work that pays for itself the next time someone adds a project-local hook.

(Auggie additionally proposed two more cross-cutting observations — "inconsistent testing strategy across skills" and "Auggie CLI invocation docs duplicated." Both were dropped as duplicates: the first folds into M4; the second folds into M2.)

## Audit

- **Auggie chunks**: 1 (succeeded, no retries, no skips) — diff was 1369 lines / 11 files, under the 1500-line single-pass threshold
- **Findings dropped during grounding**: 0
- **Findings remapped**:
  - 2 findings downgraded from Auggie's `severity_hint` per the rubric:
    - M1 (matcher Bash): `severity_hint: high` → Medium (performance ceiling is High only with measured impact; jq-on-every-Bash is intuitive but unmeasured)
    - M4 (evals no assertions): `severity_hint: high` → Medium (tests floor is Medium for critical-path skills; the skill is critical-path but the gap is structural, not breaking)
  - 1 finding upgraded:
    - none
  - 1 finding remapped from Medium to Nit:
    - N1 (PR_NUM validation): `severity_hint: medium` → Nit (the unreachable-branch consequence is cosmetic; the regex on line 40 prevents the failure mode Auggie posited)
- **Cross-source agreement**: N/A (standard depth, no independent Claude-side pass)
- **Persona cross-check**: disabled (depth=standard)
- **File:line cited but mismatched** (and remapped):
  - `install_hooks.py` finding cited line 179; actual line for the `offer-pr-review.sh` entry is line 75. Remapped.
  - All other file:line citations match exactly.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 4 low: 4 nit: 2
dropped: 0
auggie_chunks: 1
duration_sec: ~60
-->
