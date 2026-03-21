# ISS-023: prompts.py:build_spec_fidelity_prompt() role undocumented

## Status Check
- Superseded by upstream? **NO** — The frontmatter `relates_to` list includes `prompts.py` (line 12), but no spec section describes what role it plays. FR-7's Gate Authority Model paragraph describes legacy mode behavior without mentioning the prompt builder that powers it. ISS-011 (spec_patch.py omission) is a similar pattern but has no existing resolution to reuse.

## Proposal A: Add parenthetical note in FR-7 legacy mode sentence

The lightest possible fix. Adds a parenthetical to the existing legacy mode sentence in the Gate Authority Model paragraph, clarifying that `SPEC_FIDELITY_GATE` relies on `prompts.py:build_spec_fidelity_prompt()` to generate the LLM report it validates.

**Before** (FR-7, Gate Authority Model, lines 350-352):
> In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
> exactly as in pre-v3.05, validating the LLM-generated report frontmatter.
> The two authorities never coexist in the same execution mode.

**After**:
> In legacy mode (`convergence_enabled=false`), `SPEC_FIDELITY_GATE` operates
> exactly as in pre-v3.05, validating the LLM-generated report frontmatter
> (produced by `prompts.py:build_spec_fidelity_prompt()`). In convergence mode,
> `build_spec_fidelity_prompt()` still generates the human-readable
> `spec-fidelity.md` summary but its output is not gated.
> The two authorities never coexist in the same execution mode.

## Proposal B: Add role annotation in frontmatter `relates_to`

Instead of editing FR-7 body text, annotate the existing `relates_to` entry for `prompts.py` with a comment explaining its role. This mirrors the pattern that ISS-001 Proposal #3 uses for `module_disposition` but is much lighter -- just a YAML comment.

**Before** (frontmatter, line 12):
> ```yaml
>   - src/superclaude/cli/roadmap/prompts.py
> ```

**After**:
> ```yaml
>   - src/superclaude/cli/roadmap/prompts.py  # build_spec_fidelity_prompt(): legacy gate report + convergence-mode human-readable summary
> ```

## Recommendation

Adopt **Proposal A**. It places the documentation exactly where a reader would look for it (the legacy mode description in FR-7) and clarifies the dual role: primary in legacy mode, supplementary in convergence mode. Proposal B is too easy to overlook since YAML comments are not rendered in most spec review flows.

Proposal A's edit surface is small (one sentence expanded, one sentence added) and does not change any acceptance criteria or cross-references.
