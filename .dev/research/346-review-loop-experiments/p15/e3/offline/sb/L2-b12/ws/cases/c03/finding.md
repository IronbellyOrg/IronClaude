**M7. The research row pins `--strategy planning` on a persona file the inventory did not verify.** Expert: Cockburn (behavior under the pin).
- SPEC:116 says `--unattended` pins `--strategy planning`, citing `src/superclaude/agents/deep-research-agent.md:40-56`, which INV-B:127-135 read.
- INV-B:316 (UNVERIFIED item 3) says it is not known whether the frontmatter persona loads that file at run time. The spec does not mention this, and the pin depends on it.
- Recommendation: add the UNVERIFIED item to section 9 or the UNVERIFIED list, or pin the strategy in the brief as well.
- Priority: Medium.
