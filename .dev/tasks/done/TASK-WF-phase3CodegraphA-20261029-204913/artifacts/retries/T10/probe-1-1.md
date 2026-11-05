20102b06ed08be4761a8b916cb1f42b720338644
family=brief-shape-conflict
defect form: a brief addition that does not say which existing brief section holds it, against a closed section list
command: grep -n -F -e "exactly these three sections" -e "codegraph run state" -e "NOT a fourth brief section" -- src/superclaude/skills/sc-reflect-protocol/SKILL.md src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
before:
src/superclaude/skills/sc-reflect-protocol/SKILL.md:299:**Step 3B.0 (materialize per-reviewer brief packages).** Before spawning N reviewers
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:33:A reviewer brief MUST contain exactly these three sections, in this orde
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:53:**FR-4 verification-results hunk.** When §6.1 steps 5 and 5.5 ran the v
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:55:**D13 spec-body hunks (UC-1).** In UC-1 runs, the SPEC BODY ITSELF is in
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:57:**FR-RSR.9 runtime-surface ledger hunk.** On a Tier-2 UC-2 run with a no
coupled sites: src/superclaude/skills/sc-reflect-protocol/SKILL.md Step 3B.0 (d); src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md "## Grounding hunks" add-on paragraphs (FR-4, D13, FR-RSR.9 use the NOT-a-fourth-section sentence)

after:
src/superclaude/skills/sc-reflect-protocol/SKILL.md:299:**Step 3B.0 (materialize per-reviewer brief packages).** Before spawning N reviewers
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:33:A reviewer brief MUST contain exactly these three sections, in this orde
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:53:**FR-4 verification-results hunk.** When §6.1 steps 5 and 5.5 ran the v
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:55:**D13 spec-body hunks (UC-1).** In UC-1 runs, the SPEC BODY ITSELF is in
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:57:**FR-RSR.9 runtime-surface ledger hunk.** On a Tier-2 UC-2 run with a no
src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:59:**Codegraph run-state entry (every persona).** The first entry of this `
