98e6950ddbe32b85adc2ceb852b750ab48c85dae
# T15 family probe 1-1 (finding F1.1, family aug-phrase-verbatim)

defect form: the full-form AUG phrase ("Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` ...); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.") was reordered so the parenthetical comes before "call", to put both tool names on one line for the line-based guard. The Constraints require the phrase verbatim.

probe: grep -rn -F 'Codebase search (' src/superclaude plugins/superclaude

before:
src/superclaude/agents/eval-docs-loader.md:29:exact lines to cite. Codebase search (`repo_owner`/`repo_name` from `git remote get-url origin`,
src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:49:**Status signal:** harder to read directly. Look for frontmatter, presence of a `synthesis.md` or `report.md`, and file mtimes. Codebase search (`mcp__litellm__augment_code-augment_code_search`, else `mcp__auggie__codebase-retrieval`) is useful here.
src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md:33:   promote on success, **drop and log** on failure (`:209`). Codebase search (`repo_owner`/`repo_name`

coupled sites: src/superclaude/agents/eval-docs-loader.md (lines 29-32) and src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md (lines 33-36). The pipelines.md:49 hit is the short form inside a sentence (not the full form, not reordered) and is out of this family.

fix: restore the start-snapshot word order in both files and join the phrase onto one line (as sc-auggie-review-protocol/SKILL.md, rf-team-lead.md and sc-validate-roadmap-protocol/SKILL.md already do); finding-verify.md keeps its "the PR head branch; it sees pushed commits only" wording.
after:
src/superclaude/skills/sc-crash-recovery/refs/pipelines.md:49:**Status signal:** harder to read directly. Look for front
