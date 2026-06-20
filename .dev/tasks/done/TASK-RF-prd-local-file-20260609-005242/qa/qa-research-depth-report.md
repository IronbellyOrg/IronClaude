# QA Adversarial Gate — Research-Depth Lens

**Task:** TASK-RF-prd-local-file-20260609-005242 (remove PRD pipeline `--file` local-path misuse; inline spec content)
**Lens:** research-depth — can an editor produce per-item checklist actions WITHOUT re-reading source?
**Mode:** read-only, adversarial (assume shallow until proven deep)
**Research evaluated:** `research/01-process-py-file-args.md`, `research/02-prompts-and-siblings.md`, `research/03-template-and-tests.md`
**Driving spec cross-checked:** `.dev/specs/prd-local-file-delivery-fix.md`
**Source spot-checks performed:** `src/superclaude/cli/prd/process.py`, `src/superclaude/cli/prd/prompts.py`, `tests/cli/prd/test_spec_flag.py`, `src/superclaude/cli/prd/models.py`

---

## Method

For each of the four evaluation axes I (1) read the relevant research section, (2) read the corresponding spec section, and (3) opened the actual source/test files to confirm the research's line anchors and quoted bodies are accurate — not merely internally consistent. The research is treated as shallow unless it gives an editor enough to act without re-opening source.

---

## Axis 1 — R2: Is the new `_authoritative_specs_block` body shape fully specified?

**Question:** Per-spec header format, how to combine with the MUST-Read instruction, truncation handling.

**Finding: PARTIALLY DEEP — one genuine shallow spot (header format), the rest is fully actionable.**

What R2 gives concretely (verified against `prompts.py:120-138`, `:42-47`, `:34`, `:507-568`):
- The exact function to change, verbatim current body, and that signature stays `list[str] | None`. ✔ (matches source exactly)
- The primitive to reuse: `_read_file(Path(p), max_bytes=50_000)` returning `content[:max_bytes] + _TRUNCATION_MARKER`; marker text verified verbatim (`"\n\n[TRUNCATED — file exceeds 50KB inline limit]"`). ✔ Truncation is therefore fully handled by reuse — the editor does NOT decide truncation behavior, it inherits it. **This axis of the question is fully resolved.**
- The empty-input contract to preserve (`if not spec_paths: return ""`, no leading whitespace, `\n\n` lives inside the non-empty branch). ✔
- A concrete header idiom to mirror: `build_task_file_prompt` (`:507-524` read / `:546-568` interpolate) uses `Label:\n---\n{content}\n---`. R2 explicitly names this as "the exact pattern to mirror for per-spec headers."

**Shallow spot (minor, spec-level not research-level):** Neither R2 nor the spec (§5.2 says only "a clearly-delimited per-spec header") pins the EXACT header string/fence the new block must emit (e.g. does each spec get `Spec: {path}\n---\n{content}\n---`? does the `- {path}` bullet list survive alongside content?). R2 supplies a proven template to copy and the locked substrings the tests require (`"AUTHORITATIVE SPECIFICATIONS"`, `"MUST Read each one IN FULL"`), so an editor can author a passing implementation without re-reading source — but the precise header wording is a design choice left to the implementer. This is consistent with the spec deliberately leaving format open, so it is acceptable latitude, not a research gap. **Not a blocker.**

> Note on the MUST-Read wording: the track goal phrases it "MUST Read IN FULL **if truncated**" but the existing locked test substring is `"MUST Read each one IN FULL"` (no "if truncated"). R2 flags this collision explicitly (§6a item 1) and instructs preserving the matchable substring. Good — the editor is warned, not surprised.

---

## Axis 2 — R1: Exact lines/methods to delete vs keep (no editor judgment)?

**Finding: DEEP. Fully actionable.**

Verified against `process.py:165-210` (read directly):
- Two `--file` emission sites named to the line: `:199` (refs branch) and `:204` (spec branch), with verbatim surrounding bodies. ✔ Confirmed exact.
- Method span `_build_file_args` `:169-206`; wiring at `:154-155` (call) and `:166` (`extra_args=file_args`). ✔ Confirmed.
- Dead-constant determination with per-constant grep evidence: `_PHASE_ALLOWED_REFS` (:95), `_FILE_SIZE_THRESHOLD` (:115), `_SPEC_FILE_STEPS` (:121) each shown to have their ONLY references inside the removed method, zero test references. ✔
- The empty-`extra_args` no-op proof through base `pipeline/process.py:63` + `:94 cmd.extend(self.extra_args)` — establishes that "remove method" and "keep method returning `[]`" are behaviorally identical. ✔
- Every docstring line to edit: module `:4`, `:11`; class `:133` (full block `:132-135` quoted); in-method comments that vanish with the method. ✔
- Acceptance grep with current 2-hit output and the post-fix 0-hit target. ✔

**Decision-openness check:** R1 surfaces the remove-vs-keep choice and correctly attributes it to spec §5.1 ("verdict left to implementation, but no `--file` may remain"). This is an authorized degree of freedom, not an unresolved gap — R1 proves BOTH paths are safe and gives the exact edits for each. An editor needs no further source reading.

---

## Axis 3 — R3: Concrete test-writing pattern precise enough to author assertions?

**Finding: DEEP. Fully actionable.**

Verified against `tests/cli/prd/test_spec_flag.py` and `models.py:180-199` (read directly):
- `PrdConfig` is a dataclass; R3 lists the exact constructor fields. Confirmed against `models.py`: `user_message`, `product_name`, `product_slug`, `tier`, `task_dir`, `skill_refs_dir`, `spec_files` all exist as stated. ✔
- Helper signatures `_scope_config(task_dir)` (`:63-71`) and `_spec_config(tmp_path, spec_files)` (`:465-474`) quoted accurately — confirmed verbatim. ✔
- `PrdClaudeProcess` is NOT instantiated; `_build_file_args` called as a staticmethod `PrdClaudeProcess._build_file_args(cfg, "scope-discovery")`. ✔ Confirmed at the cited lines.
- `tmp_path` write idiom for real spec files: `a = tmp_path / "a.md"; a.write_text("# A\n", encoding="utf-8")` (`:85-89`). ✔
- The exact tests to invert/delete with current assertions quoted (`:487`, `:497-498`, `:506/510/515`) and the import line for `_authoritative_specs_block` (`:36`). ✔
- The new-test recipe for §7.2 (write `UNIQUE_MARKER` content to a real `tmp_path` spec, bind into `parsed["SPECS"]`, assert content-in-prompt) is spelled out with the fixture scaffolding to reuse (`_write_parsed`, `_PARSED_BASE`, `_scope_config`). An editor can author the new assertions directly. ✔
- 100KB prompt-ceiling invariant (`test_prompts.py:160-246`) and the `_read_file` truncation lock (`:249-277`) flagged as "do not break" with sizing caveat for multiple large specs. ✔ — a real downstream risk surfaced, good depth.

R3 also correctly disambiguates which test files are IN scope (`test_spec_flag.py`) vs UNRELATED (`tests/roadmap/test_prd_prompts.py` — different module) and confirms no prd-local `conftest.py`. No judgment left to the editor.

---

## Axis 4 — Is the missing-path decision RESOLVED or left open?

**Finding: LEFT OPEN — and this is the single most important shallow spot. But it is well-flagged, and the openness originates in the SPEC, not the research.**

The research is unambiguous and consistent that this is unresolved:
- R2 §2 calls it out three times: "`_read_file` does NOT handle a missing path … will raise `FileNotFoundError`," and "**This is the one real design decision for the upgrade**."
- R2 §6a items 1, 2, 4, 6 show the existing injection-test fixtures bind NON-EXISTENT paths (`/abs/SPEC_A.md`, `/abs/SPEC_B.md`, `/abs/SPEC.md`) — confirmed verbatim at `test_spec_flag.py:251-265`. Under unconditional `_read_file(Path(p))` these tests raise `FileNotFoundError`. R2 gives the two remediation options: (a) guard with `path.is_file()`/try-except, or (b) migrate fixtures to real `tmp_path` files.
- R1 and R3 echo the same.

I cross-checked the **spec** to see whether the research merely failed to relay a resolution that exists upstream. It did not: `grep -niE 'missing|is_file|FileNotFound|guard|exist'` over `.dev/specs/prd-local-file-delivery-fix.md` returns nothing in §5.2/§7, and §5.2 says only "embed `_read_file(Path(p))` content … Preserve the empty-input contract." **The spec itself does not decide missing-path behavior.** So the research accurately reflects an open decision; it did not invent or hide one.

**Why this matters for a research-depth gate:** the task is a *task-builder* input. An editor authoring checklist items can proceed on either remediation path R2 names, and the existing-test breakage is fully characterized, so work is NOT blocked. But "the one real design decision" being unresolved means the generated task MUST make this an explicit decision/checklist item rather than assuming. R2 does flag it loudly enough that a competent builder will not miss it.

**Verdict on this axis:** Acceptable for PASS because the research (a) identifies the decision precisely, (b) enumerates the concrete remediation options, (c) names every test fixture that forces the decision, and (d) correctly traces the openness to the spec. It is the editor's/builder's job to pick — the research has de-risked that pick completely. A research file cannot unilaterally resolve a spec-level design choice; surfacing it with options IS the deep-enough behavior. **Recommendation: the generated task file should carry an explicit item that decides missing-path handling (guard vs. real-temp-fixtures) — do not leave it implicit.**

---

## Cross-cutting accuracy audit

Every load-bearing anchor I spot-checked against live source was correct:
- `process.py` `_build_file_args` body, `:199`/`:204` emissions, constants `:95/:115/:121` — exact.
- `prompts.py` `_authoritative_specs_block` `:120-138`, `_read_file` `:42-47`, `_TRUNCATION_MARKER` `:34` — exact (marker em-dash confirmed).
- `test_spec_flag.py` helpers `:63-71`/`:465-474`, non-existent-path fixtures `:251-265`, imports `:33-40` — exact.
- `PrdConfig` fields in `models.py:180-199` — exact.

No fabricated line numbers, no quoted bodies that diverge from source. (Where research gave a range like ":169-206" the `def` is at `:170` under a `:169` decorator — a 1-line label nuance, not an error; R1 explicitly notes the decorator/def split.)

---

## Shallow-spot summary

| # | Spot | Severity | Blocks action? |
|---|------|----------|----------------|
| 1 | Exact per-spec header string/fence not pinned (R2 gives a proven template to mirror + locked substrings) | Minor | No — design latitude, spec leaves it open too |
| 2 | Missing-path behavior unresolved (R2: "the one real design decision") | Notable | No — options enumerated, fixtures characterized; builder must make it an explicit item |
| 3 | MUST-Read wording collision ("if truncated" vs locked substring "MUST Read each one IN FULL") | Minor | No — R2 flags it; preserve the substring |

None of the three rises to "too vague to act on." Spots 1 and 2 are bounded design choices the research has fully scoped with options; spot 3 is a flagged phrasing constraint. An editor can author every checklist item — process.py deletions, prompts.py body upgrade, test inversions, new tests, grep guard, sync/verify — without re-opening source, provided the generated task makes the missing-path handling an explicit decision item (which R2's framing already demands).

---

VERDICT: PASS
