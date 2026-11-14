# Round 1 advocate statement: Variant 1 (proposal A), security persona

## Position summary

Variant 1 sets the watcher to `--pipeline none` and declines, for now, to accept a permission-free session that reads untrusted issue text, so FU-1 waits. From a trust-boundary view it is the only variant that does not rest on the unstated assumption that a permission-free session makes only the writes the claim intends (A-002). As a neutral reviewer, though, I would not recommend it as written: a hardened Variant 3 bounds the same risk and still lets FU-1 settle facts that only a live run can settle.

## Steelman

**Variant 2 (keep `worktree`, record it as a deliberate chain, gate it on the ship gates, accept the risk for both sessions).** Its strongest form: the second agent is the most governed process in the chain. It starts only after the IR-4 preflight passes, which checks that the L1 launch-level guard is installed and registered on `UserPromptSubmit` and `PreToolUse`. It stops at a plan boundary that a person must approve (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:120`, `:140`). Variant 2 is also the only variant that names the claim command's ship gates as explicit FU-1 preconditions (U-003, `claim.md:131`), and FU-1 would then test the whole chain a later handoff design needs data about (U-002). It needs no watcher code change now.

**Critique.**
1. It doubles the permission-free surface. Both sessions run under TB-PERM (`merged-requirements.md:631`), and the first session is the same one as in Variant 3 (question.md fact row 6, ADJ line 477).
2. The second agent's own defence is thinner than it looks. The L2 pre-push refusal is "switched off (owner decision), so the claim only warns and the launch goes ahead" (`claim.md:129`), which leaves pushes limited by the L1 guard alone whenever L2 is not `owned`.
3. It amends owner decision D2, quoted verbatim as an owner decision in `docs/designs/issue-watcher.md:39` and `:44`, to fit code that contradicts it. That reverses the authority order.
4. Its gate list mixes gates. OB-H1 item 1, OB-H2 and OB-H3 apply to governed claims (`worktree` or `full`); only OB-H1 item 5 applies "before a claim at any level" (`claim.md:131`).
5. Each approval creates an agent in an `issue-<N>` worktree, and no coordinator owns those agents (Variant 2, "What stays unresolved"). Agents that nobody owns, running permission-free, are a standing attack surface.

**Variant 3 (`--pipeline none`, accept permission-free running in writing for the one test issue only).** Its strongest form: the acceptance is narrow and recorded. It says "for the test issue only", it authorises no later issue (`merged-requirements.md:572`, U-004), and FU-1 must record both permission variables and the real argv (ADJ line 272, action 2 (c)). The issue text is the main untrusted input, and the owner can write the test issue's text, so the prompt-injection risk at FU-1 is largely under the owner's control. FU-1 is the only way to settle facts that block later work: whether `agent launch` creates a Run, what the agent row holds, and the real operation-id path, which today is "a guess pinned by four `_assumed_shape` fixtures" (ADJ line 272 (f)). Variant 3 also names the one ship gate that applies at `none`: OB-H1 item 5.

**Critique.**
1. "FU-1 can run" ("What it unlocks") contradicts Variant 3's own risk note that OB-H1 item 5 may hold it (X-001).
2. It omits three hard gates on FU-1 that the spec lists: `GRANT(WA-04,live-test)`, ORCA-AVAILABLE and Q20 (`merged-requirements.md:719`, `:811`). The probe found Orca unreachable on 2026-11-13 (`:604`).
3. It treats the FU-1 write list as the full set of possible effects (A-002). That list records the expected writes; it does not bound them.

## Strengths claimed

1. **It does not rely on A-002.** On this host the default ccsession flags are `--dangerously-skip-permissions --allowedTools=Grep` (`src/superclaude/skills/ccsession-tag/ccsession:137`). `--allowedTools=Grep` is not a restriction: it brings Grep and Glob back (`ccsession:119-123`). So the first session has the full tool set with no prompts. It runs the accuracy check over untrusted issue text and repo text (TB-UNTRUSTED, `merged-requirements.md:632`). Design decision D3 protects only the prompt (`issue-watcher.md:45`), not what the session then reads.
2. **It removes the design contradiction the right way.** The code changes to match owner decision D2 (`issue-watcher.md:44`); the owner decision is not changed to match the code. The change is one small PR that can be undone and shares no file with #539 (ADJ line 271, action 1).
3. **It keeps the consent decision honest.** The spec itself says `--pipeline none` alone does not make a watcher claim safe (`merged-requirements.md:1158`). Variant 1 treats the permission mode as a separate trust decision rather than a formality.
4. **It points to a real control (U-001).** A permission-on mode exists: `CCSESSION_PERMISSIONS=default` drops `--dangerously-skip-permissions` (`ccsession:138`; `src/superclaude/skills/ccsession-tag/README.md:578`).

## Weaknesses identified in other variants

1. **Variant 2** doubles the permission-free sessions per approval. Its second agent's push limits can fall to the L1 guard only, because the L2 refusal is switched off (`claim.md:129`). It amends an owner decision to fit the code (`issue-watcher.md:39`, `:44`). Its FU-1 depends on the status of four gates, none of which is verified (question.md fact row 4).
2. **Variant 2** does not say whether a test issue counts as a "real issue" under the ship gate (`claim.md:131`). If it does not, Variant 2's gating is weaker than it claims. That reading is UNVERIFIED.
3. **Variant 3** is internally inconsistent on X-001. It also omits `GRANT(WA-04,live-test)`, ORCA-AVAILABLE and Q20 (`merged-requirements.md:719`, `:811`, `:604`).
4. **Variant 3** accepts a mode controlled by more inputs than it records. Orca's own default `--dangerously-skip-permissions` option still applies whatever `CCSESSION_PERMISSIONS` says (`README.md:578`), and FU-1's precondition (c) records only the two variables and the argv (ADJ line 272). The real argv would show the effect; the acceptance text should name the source.
5. **Variants 2 and 3** both treat the expected-write list (ADJ line 272 (i)) as if it bounded a permission-free session. It does not.

## Concessions

1. Variant 1 blocks all downstream work: WA-05, WA-06, SW-10, SW-13 and WA-07, plus the facts only FU-1 settles. A security posture that prevents learning has a cost.
2. Running with permission checks on may be impossible without someone attending. The claim makes GitHub writes that would raise prompts with nobody to answer them (Variant 1 says so itself; UNVERIFIED).
3. Variant 1's step 4 names only two permission knobs. `README.md:578` shows a third: flags the caller passes, such as Orca's default `--dangerously-skip-permissions`, still apply. Running the watcher with permission checks on may therefore also need an Orca-side change. UNVERIFIED.
4. For FU-1, the owner can author the test issue, which shrinks the untrusted-input risk that Variant 1 is guarding against. Declining protects little more at the test, and the real risk sits in later, non-test issues, which need a new owner decision anyway (`merged-requirements.md:572`).
5. Variant 1, like the others, omits `GRANT(WA-04,live-test)`, ORCA-AVAILABLE and Q20.

## Shared assumption responses

- **A-001 (FU-1's outward writes are covered by Q2 alone): REJECT.** The spec requires a separate grant. FU-1 is "a bounded test under `GRANT(WA-04,live-test)` with the owner's consent" (`merged-requirements.md:331`), and the dependency row lists `GRANT(WA-04,live-test)` beside Q2 (`:719`, `:811`). Every variant needs one more owner step.
- **A-002 (a permission-free session makes only the intended writes): REJECT.** The session runs with `--dangerously-skip-permissions` and a full tool set (`ccsession:119-123`, `:137`) over untrusted text (TB-UNTRUSTED). The FU-1 write list is the expected set, not a limit. The rejection is softened only if the test issue's text is written by the owner.
- **A-003 (Orca is reachable and Q20 is answered): QUALIFY.** Both are real hard preconditions (`merged-requirements.md:604`, `:811`: `Q20 -> WA-03 -> WA-04`). Assuming they hold is wrong: the probe found Orca unreachable on 2026-11-13, and Q20 is open. FU-1 cannot run under any variant until both are true.

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie | 50 | The section sets are identical by the brief's design. |
| C-001 | V1 = V3 | 85 | `none` matches owner decision D2 and has one permission-free session, not two. |
| C-002 | V3 | 60 | A narrow written acceptance with an owner-authored test issue is a bounded risk, and declining blocks all learning. |
| C-003 | V3 | 60 | Only OB-H1 item 5 applies at `none` (`claim.md:131`), and V3 names it. V2's gate list mixes gates. |
| C-004 | V1 = V3 | 75 | A small reversible PR makes the code match the owner decision. V2 rewrites the decision instead. |
| C-005 | V3 | 75 | It is the only variant that unblocks WA-05, SW-10, SW-13 and WA-07. |
| C-006 | V1 = V3 | 80 | Owner decision D2 is the authority (`issue-watcher.md:39`), so the code should change. |
| X-001 | V2 | 65 | V2 says plainly that FU-1 waits on gates. V3 contradicts itself, and none of the variants lists every gate. |
| X-002 | V1 = V3 | 80 | The owner already chose "claim-only" (D2). |
| X-003 | V3 | 60 | One session for one owner-controlled test issue is acceptable with recorded scope. Two sessions (V2) widen it. |
| A-001 | None (all share the gap) | 85 | `GRANT(WA-04,live-test)` is required (`merged-requirements.md:331`, `:719`). |
| A-002 | V1 | 75 | It is the only variant that does not treat the expected writes as a bound. |
| A-003 | None (all share the gap) | 85 | ORCA-AVAILABLE and Q20 hard-gate FU-1 under every variant. |

## Overall

As a neutral reviewer I would recommend **Variant 3, hardened**, with **70** confidence. The added conditions are:

1. The owner writes the test issue's text and the issue receives no other comments before the claim.
2. `GRANT(WA-04,live-test)` is recorded.
3. ORCA-AVAILABLE is read back as true and Q20 is answered.
4. OB-H1 item 5's status is confirmed.
5. The acceptance text names Orca's caller-passed permission flag as well as the two variables.
6. The acceptance stays "for the test issue only".

Variant 1's lasting contribution is the fallback rule: if any of these conditions cannot be met, FU-1 waits, as Variant 1 says. Variant 2 should be rejected: it doubles the permission-free surface and overrides an owner decision.
