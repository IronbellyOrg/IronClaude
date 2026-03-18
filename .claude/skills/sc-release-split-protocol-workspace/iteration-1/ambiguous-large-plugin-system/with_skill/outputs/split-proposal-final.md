---
adversarial:
  agents: [opus:architect, haiku:analyzer]
  convergence_score: 0.78
  base_variant: opus:architect
  artifacts_dir: null
  unresolved_conflicts: 1
  fallback_mode: true
---

# Adversarial Review — Release Split Proposal

> **Warning**: Adversarial result produced via fallback path (Mode A conceptual roles, not Mode B agent-backed generation).
> Quality may be reduced compared to full agent variant generation. Review the merged output manually before proceeding.

## Original Proposal Summary

The Part 1 discovery proposed splitting v5.0 into two releases along a **local runtime vs. distribution infrastructure** seam. Release 1 would deliver the plugin package format (R1), CLI manager in offline mode (R3 partial), sandboxed execution (R4), lifecycle hooks (R5), and skill migration (R7). Release 2 would deliver the registry (R2), marketplace (R6), CLI registry integration (R3 partial), PDK (R8), analytics (R9), and enterprise policies (R10). Confidence was 0.82.

## Advocate Position (FOR the split)

The dependency graph makes a compelling case. R1 (package format) is the keystone — every other requirement depends on it. If the format design is wrong, the entire distribution layer is built on a broken foundation. Shipping R1 + R4 (sandbox) + R3 (offline CLI) first means:

1. **Real users create real plugins.** This is not a synthetic test. Actual plugin authors will use the format, hit edge cases in the manifest schema, and discover permission model friction. This feedback is priceless before the registry locks in the format.

2. **Sandbox security gets real-world testing.** The sandbox is the highest-risk security component. Exposing it to real plugin execution before the registry enables public distribution reduces the blast radius of sandbox escape vulnerabilities.

3. **The seam is natural, not forced.** The local/distribution boundary already exists in the architecture diagram (Section 3.1). The CLI explicitly supports offline mode (R3). The rollout plan (Section 6) already envisions "Alpha: Plugin format + CLI install from local files." The spec itself suggests this phasing.

4. **Release 1 enables a real validation signal.** After R1 ships, we can answer: "Can users create plugins? Do permissions work? Is the sandbox secure? Does migration preserve skill behavior?" These are the questions whose answers most affect R2's design.

## Skeptic Position (AGAINST the split)

The split has three problems the proposal downplays:

1. **R3 is being torn in half.** The CLI Plugin Manager is a single coherent feature (install, update, remove, list, publish, lockfile, offline mode). Splitting it across releases means building the install engine twice — once for local files, once for registry sources. The proposal acknowledges this risk but handwaves it with "abstract the source interface." Abstractions designed before you know the second use case are frequently wrong. The registry source will have authentication, rate limiting, namespace resolution, dependency resolution against a remote catalog — these are not trivially abstracted behind a generic interface.

2. **R5 (Lifecycle Hooks) in R1 is overreach.** Hooks depend on R4, yes, but they also represent the plugin-to-SuperClaude integration contract. If hooks ship in R1 without the PDK (R8, in R2), plugin authors are building against an undocumented API. When R8 ships with proper type definitions and examples, the hook API may need to change. Deferring R5 to R2 keeps the hook API and its documentation/tooling together.

3. **The "foundation vs. application" framing masks forward-dependency.** The proposal admits R1 must anticipate registry constraints (namespaces, signing). But it goes further: R1's package format must also anticipate the security scanner (R10), the analytics hooks (R9), and the marketplace metadata (R6 needs README, screenshots, categories in the manifest). Designing R1 without R2-R10 fully specified risks a manifest schema that needs breaking changes when R2 ships.

## Pragmatist Assessment

Evaluating against hard criteria:

**Does Release 1 enable REAL-WORLD tests that couldn't happen without shipping it?**
Yes. Local plugin creation, installation, sandbox execution, and migration can only be tested by shipping. Unit tests for format parsing are insufficient. The critical question is: "Do real users successfully create and run plugins?" This requires shipping R1.

**Is the overhead of two releases justified by the feedback velocity gained?**
Marginally yes. The package format and sandbox are the two components where wrong decisions are costliest to fix later. Early feedback on these specifically justifies the split. However, the skeptic is right that R3's split-across-releases increases overhead.

**Are there hidden coupling risks where Release 1 without Release 2 creates a misleading validation signal?**
Partially. R1 validates format + sandbox + local install. But it does NOT validate: dependency resolution against a remote catalog, namespace collision handling, registry-side signature verification, or the install experience for non-technical users (who would use the marketplace, not CLI). R1's validation signal is real but narrower than the proposal implies.

**What is the blast radius if the split decision is wrong?**
Low-medium. If the split proves wrong, the two releases can be merged back. R1's artifacts (format spec, sandbox, CLI) are all needed regardless. The worst case is some R3 rework for registry integration. Estimated reversal cost: 1-2 weeks of integration work.

**What would it take to reverse the decision later?**
Merge R2 scope into R1 and do a single release. Since R1 work is all prerequisite work for R2, nothing is wasted — only the release boundary disappears.

## Key Contested Points

| Point | Advocate | Skeptic | Pragmatist | Resolution |
|-------|----------|---------|------------|------------|
| R3 split across releases | "Abstract the source interface" | "Abstractions without the second use case are wrong" | "Design risk is real but bounded; R3 rework is ~1 week worst case" | **SPLIT-WITH-MODIFICATION**: Design R3's source interface with explicit registry stubs (not a generic abstraction) |
| R5 (Hooks) in R1 or R2 | "Needed for plugins to integrate" | "Without PDK, hook API is undocumented" | "Hooks without docs is worse than no hooks; but basic hooks enable validation" | **UNRESOLVED**: Could go either way. Recommend R1 with MINIMAL hooks (pre-command, post-command only). Defer custom-command and transform-output to R2. |
| Forward-dependency on R2 constraints | "Bake signing/namespaces into R1" | "Can't design for what you haven't specified" | "The manifest schema should include reserved fields for registry metadata" | **RESOLVED**: R1 manifest includes registry-reserved fields with explicit "reserved for R2" markers |
| Validation signal narrowness | "Local validation is real" | "It misses distribution workflows" | "Narrow but sufficient for the foundation" | **RESOLVED**: Acknowledge scope of validation signal in R1 spec |

## Verdict: SPLIT-WITH-MODIFICATIONS

### Decision Rationale

The dependency graph provides a genuine structural seam between local runtime and distribution infrastructure. The foundation components (format, sandbox, permissions) are the highest-risk items where early feedback has the most leverage. The skeptic's concerns about R3 rework and R5 placement are valid but addressable through specific modifications.

### Modifications to Original Proposal

1. **R5 scope reduction in R1**: Release 1 includes only `pre-command` and `post-command` hooks. `custom-command`, `transform-output`, and `on-error` hooks move to Release 2 alongside the PDK.
2. **R3 design constraint**: Release 1's install engine must include explicit registry source stubs (not a generic abstraction). The interface shape should be informed by R2's known API design, even though R2 isn't built yet.
3. **Manifest forward-compatibility**: R1's manifest schema includes reserved fields for registry metadata (categories, screenshots, author-org mapping) marked as "reserved for R2."
4. **Validation signal scoping**: R1's success criteria explicitly state what is and is not validated. R1 does not claim to validate distribution workflows.

### Strongest Argument For

The package format and sandbox are the two components where wrong design decisions are most expensive to fix. They are also the two components that can ONLY be validated by shipping to real users. Deferring their validation until the entire distribution layer is built maximizes the blast radius of design flaws.

### Strongest Argument Against

Splitting R3 across releases creates rework risk. The CLI install engine designed for local files will need modification for registry sources, and the abstraction boundary is being drawn before the second use case (registry) is fully specified. This is a known antipattern.

### Remaining Risks

1. Manifest schema may need breaking changes when R2 constraints are fully specified (mitigated by reserved fields)
2. R3 install engine may need refactoring for registry integration (mitigated by registry stubs)
3. R5 partial delivery means hook API is not battle-tested before R2 adds the rest (mitigated by limiting R1 to basic hooks)
4. Users may perceive R1 as incomplete (mitigated by clear documentation)

### Confidence-Increasing Evidence

- A prototype manifest schema reviewed against R2's registry API requirements would significantly increase confidence in the format's forward-compatibility
- A spike on the R3 install engine's source interface would validate whether the local/registry split is tractable
- User research on whether "local-only plugin system" is perceived as valuable or confusing
