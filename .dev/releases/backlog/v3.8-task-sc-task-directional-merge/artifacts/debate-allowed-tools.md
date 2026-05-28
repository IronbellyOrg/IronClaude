# Adversarial Debate — Declared `allowed-tools` Frontmatter (D01)

**Task:** T04.03 — `/sc:adversarial` debates: MCP, persona, allowed-tools, compliance gating, triggering surface
**Roadmap Item:** R-013
**Source feature characterization:** `feature-allowed-tools.md` (Phase 2 / T02.03)
**Constraint inputs:** `extension-point-contracts.md` (T03.02); INV-01..INV-05 labels from `extension-point-contracts.md:13-17`
**Donor catalog tag:** D01 = **ADAPTABLE** — re-tagged from DUPLICATE-OF-EXISTING during T01.03 pointer audit (`donor-feature-catalog.md:47, 115`). The original DUPLICATE pointer at `src/superclaude/skills/task/SKILL.md:4` was invalid (line 4 is the closing `---` of frontmatter; the `/task` skill has no `allowed-tools` slot). Conceptual analog is Critical Rule 6 at `src/superclaude/skills/task/SKILL.md:337` — a runtime tool-selection prescription, differently shaped from a declarative loader-enforced gate.
**Phase 1 net-upgrade question (forwarded by T01.03 / `donor-feature-catalog.md:47`):** "Would adding a declarative `allowed-tools` frontmatter slot to the skill complement Critical Rule 6, or duplicate it less precisely?" — this debate is the answer.
**Generated:** 2026-05-15
**Note on Phase 3 input:** `invariant-bounds.md` (T03.01) was not produced — see `checkpoints/CP-P03-END.md`.

---

## Position A — Steelman for Inclusion (net-upgrade framing per R-RULE-06 for DUPLICATE-OF-EXISTING-adjacent features)

D01 is a partial-match donor feature (`donor-feature-catalog.md:115`): the conceptual analog Critical Rule 6 exists on the recipient side at `src/superclaude/skills/task/SKILL.md:337`, but the *shape* differs — Critical Rule 6 is prescriptive prose, the donor's `allowed-tools` is a declarative loader-enforced gate. The question is whether the *shape difference* is a net upgrade, not whether the rough capability already exists.

**Three concrete net-upgrades over Critical Rule 6:**

1. **Loader-enforced denial vs prose discipline.** Critical Rule 6 says "do NOT use bash `find/grep/cat/head/tail/rg/awk`" (`src/superclaude/skills/task/SKILL.md:337`). Enforcement is the LLM following the instruction. The donor's `allowed-tools` allowlist (`src/superclaude/commands/task.md:6`) is denied *at the framework boundary* — if a tool isn't on the list, the dispatch is refused regardless of LLM intent (`feature-allowed-tools.md:59`). This shifts safety from "LLM compliance" to "framework refusal." For a skill whose F1 loop spawns many subagents over many turns, even a small per-turn probability of off-list tool use compounds. The declarative gate eliminates that compounding.
2. **Capability-discovery surface.** A reviewer / capability auditor / docs generator can answer "what can `/task` touch?" by reading a single frontmatter line — `feature-allowed-tools.md:60`. Critical Rule 6 is buried at line 337 of a 350+ line SKILL.md, mixed with 13 other rules. Discoverability of the contract matters when the skill is one of many in a marketplace.
3. **Explicit exclusion of dangerous tools.** Critical Rule 6 is positive ("use these") + negative ("not bash find/etc."); it does not explicitly exclude `WebFetch`, `WebSearch`, `NotebookEdit`, the `mcp__*` namespace, `Monitor`, `CronCreate`, `PushNotification`, `EnterPlanMode/ExitPlanMode`. The donor's allowlist excludes all of them by omission (`feature-allowed-tools.md:13`). For a skill that runs in `bypassPermissions` mode and spawns subagents that inherit some envelope of trust, narrowing the tool surface to nine well-understood tools is a real safety boundary against, e.g., `WebFetch` exfiltration or `NotebookEdit` corruption.

**Integration sketch:**
- **Attach point:** extension-point row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`). Add `allowed-tools:` as an *optional* frontmatter field on `/task`'s SKILL.md (`src/superclaude/skills/task/SKILL.md:1-4`). The Skill loader's recognition of the key must be verified or built. Row 13's admit criteria — "new required-metadata fields validated by row 1's pre-loop validator … evaluated before loop entry" — extend cleanly to optional fields.
- **Recommended list:** `Read, Glob, Grep, Edit, Write, Bash, Task, TodoWrite` — the donor list minus `Skill` (a Skill cannot dispatch another Skill in the recipient's model). Calibrated against `/task`'s actual tool use: subagent dispatch via `Task`/`Agent`, file reads via `Read`/`Glob`/`Grep`, edits via `Edit`, task-file mutation via `Edit`/`Write`, test runs via `Bash`, progress tracking via `TodoWrite`.
- **Coexistence with Critical Rule 6:** the frontmatter gate handles *what is dispatchable*; Critical Rule 6 handles *which dispatchable tool to prefer* (e.g., `Glob` over `Bash find`). The two stop competing once their scopes are clarified — Critical Rule 6 retitles itself from a tool-exclusion rule to a tool-preference rule, the allowlist owns exclusion.

**Trade-off acknowledgment (R-RULE-04 anti-sycophancy):**
- **Critical Rule 6 must be edited.** The recipient's "Critical Rules are inviolable" framing means editing one is a high-cost change (`feature-allowed-tools.md:79, 85`). The cost is not zero; the recipient is committing to a rule change.
- **The allowlist is leaky because `Bash` is on it.** `Bash` can do everything the user's shell can (`curl` substitutes for `WebFetch`, `jupyter nbconvert` for `NotebookEdit`, `mcp_client` calls for the MCP namespace) (`feature-allowed-tools.md:68`). The gate restricts a few high-level tools but does not actually contain capability — for `/task` (which legitimately needs `Bash` for tests), the allowlist excludes convenience tools but leaves the universal-purpose escape hatch wide open.
- **No override path is documented.** If a legitimate `/task` item needs `WebFetch` (e.g. fetch a linked GitHub issue), the user has no flag-level escape hatch (`feature-allowed-tools.md:70`). The donor offers none; the recipient inherits the rigidity. Per-item `WebFetch` would have to be re-encoded as a Bash `curl` call (preserving the leak hole above) or the item must fail closed.
- **Skill-loader recognition of `allowed-tools` is not yet verified for the Skill namespace.** The `sc:task-protocol` skill carries `allowed-tools` (`src/superclaude/skills/sc-task-protocol/SKILL.md:4`), which is suggestive but not conclusive — the recipient must verify the Skill loader honors the key with deny-by-default semantics, not just parses it.
- **Calibration risk.** The recipient's spawned subagents have heterogeneous needs; an item that researches an external library legitimately needs `WebFetch`. The donor's prompt-driven model has narrower per-turn variance and gets away with a fixed allowlist; `/task`'s item-driven model has wider variance.

---

## Position B — Steelman for Rejection (net-upgrade framing — REJECT if no net upgrade per R-RULE-06)

**There is a net upgrade in shape, but it is narrow and the cost is real.** This is not a DUPLICATE-OF-EXISTING (Phase 1 corrected the tag), but the *operating concept* (constrain which tools fire in this skill) is already discharged by Critical Rule 6. The marginal value of the loader-enforced shape over the prose-prescribed shape must clear the bar set by R-RULE-06 ("absorb patterns, not implementation mass") AND the four coupling burdens enumerated at `feature-allowed-tools.md:73-85`. It does not clear that bar.

**Four coupling burdens, with one direct conflict:**

1. **A new frontmatter slot in `/task`'s SKILL.md, plus loader-recognition verification** (`feature-allowed-tools.md:77`). Skill-loader recognition of the key has not been verified for `/task`'s namespace. If the Skill loader does not honor the key with deny-by-default semantics, the slot is inert — a `mcp-servers`-style ceremony failure mode (`feature-mcp-declarations.md:91`). The recipient is betting on loader semantics that are unverified.
2. **Direct conflict with Critical Rule 6** (`feature-allowed-tools.md:79`). Critical Rule 6 is *prescriptive runtime guidance* (positive: "use Glob/Grep/Read/codebase-retrieval"; negative: "do NOT use bash find/grep/cat/head/tail/rg/awk"). The donor's mechanism is the inverse shape — declarative allowlist enforced by the loader. Adopting the donor without rewriting Critical Rule 6 produces two sources of truth for "what tools may fire," and they would inevitably drift. The recipient must commit to rewriting Critical Rule 6 — a high-cost edit per the recipient's "Critical Rules are inviolable" framing.
3. **A tool-list calibration step** (`feature-allowed-tools.md:81`). The recipient must validate the donor list item-by-item against `/task`'s legitimate operating envelope. The donor list omits `WebFetch, WebSearch, NotebookEdit, Monitor, CronCreate, PushNotification, EnterPlanMode/ExitPlanMode`, `ReadMcpResourceTool, ListMcpResourcesTool`, and the entire `mcp__*` namespace. `/task` items legitimately vary — research items want `WebFetch`, code items want `Read/Edit`, test items want `Bash`. The donor's prompt-driven model has narrower variance and accepts the rigidity; `/task` does not.
4. **An override / weakening path for legitimate exceptions** (`feature-allowed-tools.md:83`). Since `/task` is item-driven, per-item action types vary widely. The recipient must either (a) accept that any item needing an excluded tool fails closed, (b) add a per-item "tool-grant" annotation (extends task-file schema *and* the loader contract), or (c) make the list maximally permissive (dilutes safety value back toward zero). The donor offers no guidance — its prompt model has no analogous variance to manage.

**Realistic failure mode #1 (the Bash leak):** A `/task` item reads "Fetch the failing CI log from PR #123 and analyze it." Under Critical Rule 6 today, the LLM uses `WebFetch` or a `gh` Bash call — either works, both are tracked, and Critical Rule 6's prescriptive guidance prefers `WebFetch`. Under the donor's allowlist, `WebFetch` is excluded; the LLM falls back to `Bash gh` or `Bash curl`. The allowlist *appeared* to contain the capability but in practice routed it through the unrestricted `Bash` hole (`feature-allowed-tools.md:68`). Safety value collapses; the allowlist's only effect was to *route around itself*.

**Realistic failure mode #2 (loader-asymmetry surprise):** A new contributor reads `/task`'s SKILL.md frontmatter, sees `allowed-tools: Read, Glob, Grep, ...`, and infers the same deny-by-default semantics as the donor command. They write a test that expects `WebFetch` to be rejected. The test passes for the wrong reason — the Skill loader does not actually enforce the key — and the contributor publishes a skill that fails to contain `WebFetch` calls in production. This is the canonical ceremony failure: the *appearance* of a contract without the contract existing.

**Realistic failure mode #3 (Critical Rule 6 drift):** The recipient adopts the allowlist but does not rewrite Critical Rule 6. Over six months, the allowlist gains `MultiEdit` (a hypothetical new tool); Critical Rule 6 is not updated. A reader trying to answer "may I use `MultiEdit` in this skill?" gets contradictory signals — the allowlist says yes, Critical Rule 6 does not mention it. The drift was inevitable from the moment two sources of truth coexisted (Position B's central duplication argument).

**Net-upgrade reasoning per R-RULE-06 (the load-bearing question for D01):** The donor catalog explicitly forwards the net-upgrade question to Phase 4 (`donor-feature-catalog.md:47`): "would adding a declarative `allowed-tools` frontmatter slot to the skill complement Critical Rule 6, or duplicate it less precisely?" The answer Position B advances: it duplicates less precisely. Critical Rule 6 (a) handles preference *between* dispatchable tools (which the donor allowlist does not), (b) is observable from the rule listing, (c) carries the rationale ("for file search, content search, file reading, semantic code search"). The allowlist would discharge only the *exclusion* aspect, leaving the preference aspect to Critical Rule 6 — splitting the contract into two surfaces that must coordinate, with no documented coordination rule.

**The R-RULE-06 question for DUPLICATE-OF-EXISTING-adjacent features:** "argue the *net upgrade* over `/task`'s existing capability, not raw value." Position A's three net-upgrades:
- **Loader-enforced denial vs prose discipline:** real, but undermined by the `Bash` leak (`feature-allowed-tools.md:68`) and by the unverified Skill-loader recognition.
- **Capability-discovery surface:** real, but solvable inside Critical Rule 6 (move the negative list to frontmatter as a *comment*, not a loader-enforced slot — gets discoverability without coordination cost).
- **Explicit exclusion of dangerous tools:** real, but Position A's own list of "dangerous" tools (`WebFetch, NotebookEdit, mcp__*`) is the right list whether or not we adopt the donor's mechanism — the recipient could ship that exclusion list in Critical Rule 6's prose with zero coupling burdens.

Two of three "net upgrades" are achievable without adopting D01. The remaining one (loader-enforced denial) is materially weakened by the `Bash` leak.

---

## Evidence-Based Weighing

**Position A's strongest point (loader-enforced vs prose-enforced):** Framework refusal beats LLM compliance for a safety-critical contract. Even a small per-turn probability of off-list tool use compounds over many F1 iterations.

**Position B's answer:** Accepted as a *partial* upgrade, with three offsetting limits: (1) `Bash` is on the list and substitutes for everything excluded (`feature-allowed-tools.md:68`); (2) Skill-loader recognition of the key with deny-by-default semantics is unverified for the recipient's namespace (`feature-allowed-tools.md:77`); (3) the upgrade does not compose cleanly with Critical Rule 6, forcing a Critical Rules edit (`feature-allowed-tools.md:79`). The framework-refusal-vs-LLM-compliance argument is real but the realized upgrade after accounting for the leak hole is much smaller than the framing suggests.

**Position B's strongest point (Critical Rule 6 duplication + Bash leak + unverified loader semantics):** The donor mechanism does not survive co-existence with Critical Rule 6 unmodified, and Critical Rule 6's edit cost is high. The `Bash` leak materially diminishes the realized safety value. Skill-loader semantics are not yet verified.

**Position A's answer:** Concedes the `Bash` leak — but argues that *narrowing the high-level tool surface* still helps, because not every off-list tool has a fluent Bash substitute (`NotebookEdit` does, but `Monitor` and `EnterPlanMode/ExitPlanMode` and the `mcp__*` namespace do not — those would be hard to route around). On the Critical Rule 6 edit: argues for a *retitling*, not a deletion — Critical Rule 6 becomes the *preference* rule (Glob over Bash find), and the allowlist becomes the *exclusion* rule. The two-surface coordination cost is real but defines a clean split. On Skill-loader semantics: agrees this must be verified pre-adoption; if verification fails, D01 is REJECT regardless. Position A's response is partial — it offers a plan but does not pre-pay the verification.

**Unanswered point against Position A:** Position B's failure mode #1 (the Bash leak in practice) is unrefuted. Position A acknowledges `Bash` is leaky but does not show that the actual day-to-day use of `/task` would *not* route around the allowlist via Bash. The realistic estimate, given `/task`'s heavy `gh`-and-`curl`-via-Bash usage in research items, is that most off-list capabilities will be Bash-substituted; the realized safety value is closer to the prose-prescribed Critical Rule 6 than Position A's framing claims.

**Unanswered point against Position B:** Position B's failure mode #3 (Critical Rule 6 drift) assumes the recipient adopts the allowlist but does not rewrite Critical Rule 6. The recipient is free to bind the two — either rewrite Critical Rule 6 as a *companion* to the allowlist (preference layer on exclusion layer), or rewrite it as a comment-only documentation block. The drift hazard exists only if the recipient is sloppy; it is not intrinsic to D01.

**Net effect:** D01 is a real partial-upgrade over Critical Rule 6 (loader enforcement + capability discoverability + explicit dangerous-tool exclusion). The realized value is reduced by the `Bash` leak and unverified Skill-loader semantics. The coupling cost is dominated by a Critical Rules edit (cost #2). Two of the three "net upgrades" are achievable without adopting D01 at all (capability discoverability via frontmatter comment; explicit exclusion list inside Critical Rule 6 prose).

R-RULE-06's net-upgrade test (for DUPLICATE-OF-EXISTING-*adjacent* features): the net upgrade after accounting for the alternatives is the *unique* upgrade attributable to D01. That uniquely-attributable upgrade is: loader-enforced denial on tools that cannot be Bash-substituted (`Monitor`, `EnterPlanMode/ExitPlanMode`, `mcp__*`, `CronCreate`, `PushNotification`, `ListMcpResourcesTool`, `ReadMcpResourceTool`, `WebSearch` where Bash substitutes via search APIs are awkward, `NotebookEdit` if no `jupyter` CLI substitute is available). That is a *real* upgrade and not free elsewhere — but it is narrow.

---

## Scored Verdict

| Component | Score | Rationale |
|---|---|---|
| **V (Value, 1–5)** | **2** | Net-upgrade per R-RULE-06: real but narrow. Loader-enforced exclusion is uniquely attributable to D01 for tools without fluent Bash substitutes (`Monitor`, `mcp__*`, `CronCreate`, `EnterPlanMode`, etc.). Capability discoverability and explicit dangerous-tool listing are achievable inside Critical Rule 6 prose at zero coupling cost. The `Bash` leak (`feature-allowed-tools.md:68`) materially reduces realized value for the tools that *do* have Bash substitutes (`WebFetch ↔ curl`, `NotebookEdit ↔ jupyter`). |
| **C (Complementarity, 1–5)** | **3** | Attaches at row 13 (Required frontmatter schema slot, C5; `extension-point-contracts.md:169-175`) — additive optional field, no F1 change. C-band would be C5 *except* the integration forces a rewrite of Critical Rule 6 (a separate skill surface, not an extension point in the row inventory) — that elevates the structural cost into C3 territory: "extension surface exists but must be widened with a new hook" (`extension-point-contracts.md:25`), where the new hook is the coordination contract between the allowlist (exclusion) and Critical Rule 6 (preference). No INV collision — the gate is at the Skill loader, pre-execution; INV-01..INV-05 are not touched. |
| **K (Cost, 1–5)** | **3** | Four burdens (`feature-allowed-tools.md:73-85`): new frontmatter slot + loader verification, Critical Rule 6 rewrite, tool-list calibration, override path. Critical Rule 6 rewrite is the dominant cost (touches the recipient's "Critical Rules are inviolable" framing). No new mechanism beyond the slot itself if the Skill loader honors the key. |
| **Net = (V × C) / K** | **(2 × 3) / 3 = 2.0** | |

**Verdict: DEFER** (Net = 2.0 falls in the DEFER band, `1.5 ≤ Net < 3`).

**Rationale for DEFER over ADAPT:**
- The verdict is *contingent* on two pre-conditions that the recipient has not yet paid: (a) verifying the Skill loader honors `allowed-tools:` with deny-by-default semantics for `/task`'s namespace; (b) committing to a Critical Rule 6 retitling/rewrite that splits exclusion from preference cleanly.
- If both pre-conditions land cheaply, V rises to 3 (the loader-recognized gate becomes real), Net rises to (3 × 3) / 3 = 3.0 — right at ADAPT.
- If either fails, V collapses to 1 (the slot is inert ceremony; R-RULE-06 fires; REJECT).
- DEFER is the right disposition: do not adopt yet, run the verification + alignment step first, then re-score in Phase 5 against the verified pre-conditions.

**Verdict: DEFER.**

**Stack-rank inputs (for T04.05):**
- D01: V=2, C=3, K=3, Net=2.0, **DEFER** (contingent on Skill-loader-semantics verification + Critical Rule 6 split commitment).

**Phase 5 forwarded questions:**
1. **Skill-loader-semantics verification:** Does Claude Code's Skill loader honor an `allowed-tools` frontmatter key with deny-by-default semantics, or only parse it as metadata? If the latter, D01 collapses to ceremony.
2. **Critical Rule 6 split:** Can Critical Rule 6 be retitled as a *preference* rule (Glob over Bash find) while a new frontmatter `allowed-tools` slot owns *exclusion*? If yes, the duplication risk dissolves and D01 ADAPTs cleanly.
3. **Per-item override:** Does `/task`'s item-driven model need a per-item `tool-grant` annotation for items that legitimately need excluded tools (e.g., a research item needing `WebFetch`)? If yes, extend the task-file schema; if no, accept fail-closed semantics.

**Note on missing T03.01 evidence:** `invariant-bounds.md` is absent (Phase 3 checkpoint Fail). D01's verdict does not depend on a worked INV failure-mode example — the gate is at the Skill loader (pre-execution), and `extension-point-contracts.md:13-17` is sufficient to establish that no INV-01..INV-05 is touched. The verdict relies on the Critical Rule 6 conflict and the R-RULE-06 net-upgrade test, both of which are independently sourced.
