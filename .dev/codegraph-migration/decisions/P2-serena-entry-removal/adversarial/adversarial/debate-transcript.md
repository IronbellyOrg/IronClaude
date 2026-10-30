# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe)
- Convergence achieved: 100% (18 of 18 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (V1 Option A: architect lens; V2 Option B: backend lens; V3 Option C: qa lens; all on the current model; Mode A, no --agents)
- Invocation: skill-direct; advocates were read-only general-purpose agents; transcripts condensed here by the orchestrator, keeping every verdict and concession

## Round 1: Advocate Statements

### Variant 1 Advocate (Option A)
- Position: A, as written, fails the hard requirement (X-002 off Coder; X-003 applies to A as well, because `./update.sh` on Coder leaves the entry). A's structural strengths should be grafted onto B.
- Steelman B: only IronClaude's registry (`install_mcp.py:59`) and Coder's declared mirror write that argv; once codegraph is verified, removal is a replacement; the failure branch never leaves neither; moving the bundle stop earlier is safe (handoff §5 item 4). Steelman C: each repo removes what its own installer wrote; no churn.
- Strengths: no Phase 1 module edit; keeps D2's provenance rule; exact-argv idempotent Coder migration also covers workspaces where install never reruns (`ironclaude/install.sh:88-95`), plus uv tool and markers; one `jq -e` expression for both names.
- Critique: B's "gone after the slug run" is false (slug order; X-001); B removes a user's deliberate re-registration made from Phase 1 §3.4's hint (A-004). C fails on the user's own workspace (X-003) and couples to a Coder path.
- Concessions: the new requirement overrules Tier K as an accepted exception (Phase 1 D2); A depends entirely on another repo.
- Verdicts: S-001 B, S-002 B, C-001 B, C-002 B, C-003 B, C-004 A/C, C-005 B, C-006 graft, C-007 B+A, C-008 B; X-001 valid vs B, X-002 conceded, X-003 valid vs C and A.
- Shared assumptions: A-001 QUALIFY (state uv tool and user data in acceptance text); A-002 REJECT (binary gate keeps the kind-B entry); A-004 QUALIFY; A-005 ACCEPT; A-006 REJECT.

### Variant 2 Advocate (Option B)
- Position: B is the only option meeting "absent after `./update.sh`" wherever IronClaude acts, including this workspace; Phase 1 §3.6 itself names the bundle stop as the condition for moving the row to Tier R.
- Steelman A: debated provenance rule (0.877), never removes another writer's entry, never flip-flops. Steelman C: each repo removes its own; non-Coder clean at once.
- Strengths: never leaves neither (guard); one exact-match rule, no environment probe; U-001 safe early bundle stop (research 5.2 row C).
- Concession on X-001: wrong as written. Correction: (1) Coder bundle stops registering and installing Serena in Phase 2 §8 step 2 (gate for steps 3-4); (2) adopt A/C's exact-argv Coder migration as backstop; (3) Coder clean after the pin-bump boot when step 2 includes the stop.
- Verdicts: S-001 B, S-002 tie, C-001 B, C-002 B, C-003 B, C-004 A/C, C-005 B/C, C-006 corrected B, C-007 B+A, C-008 B; X-001 conceded, X-002 vs A, X-003 vs C.
- Shared assumptions: A-001 QUALIFY; A-002 REJECT (apply the same replacement rule to the kind-B registration; binary stays a disclosed leftover); A-004 QUALIFY (hint uses another name, e.g. `serena-local`); A-005 ACCEPT; A-006 REJECT.

### Variant 3 Advocate (Option C)
- Position: C fails the hard requirement on the user's own workspace (X-003); B's rule is the core; C contributes the exact-argv Coder migration and the two-branch test matrix; drop the provenance check.
- Steelman A and B as above.
- Critique: A fails off Coder (X-002, CRITICAL); B alone has X-001 and A-004.
- Concessions: X-003 decisive; the provenance check couples IronClaude to another repo and adds a code path with no benefit.
- Verdicts: S-001 B, S-002 C (minus provenance branch), C-001 B, C-002 B, C-003 B, C-004 A/C, C-005 B/C, C-006 B + migration, C-007 combine all three, C-008 B; X-001 vs B alone, X-002 vs A, X-003 conceded.
- Shared assumptions: A-001 QUALIFY (state kept data in acceptance text and CHANGELOG); A-002 REJECT (needs a removal rule and `! command -v codebase-memory-mcp` as user coder); A-004 QUALIFY; A-005 ACCEPT with a Coder test; A-006 REJECT.

## Round 2: Rebuttals

### Variant 1 Advocate
- Accept corrected B with fixes: amend Phase 1 texts in the same merge (Phase 2 file table row saying Phase 2 does not edit `install_retired_mcp.py`; Phase 1 §3.2 Tier K row 1; the sandbox expectation "Legacy Serena registration kept"; D2; handoff §2.4 "Coder must remove it itself"). Coder migration ships in step 2 with the bundle stop.
- Guard: a state predicate (user `codegraph` entry present and its command executable), so `install --list` and `doctor` agree with `install`; keep two-branch tests.
- A-004: rename the hint to `serena-local` (one token + test); reject a marker (new state). A-004 now ACCEPT.
- A-002: kind-B registration in scope (same predicate); binary escalated (removing it reopens D2's rejection of prompt-free upstream uninstall).

### Variant 2 Advocate
- Accept amending Phase 1 texts in the same merge.
- Reject an unguarded step-2 migration: under the old pin no codegraph exists, so it would remove Serena with no replacement. The migration is a backstop; it ships in step 5, or in step 2 only with the same guard. The bundle stop and the `spec2-health.sh`/test-57 edits stay in step 2.
- Predicate must reuse the codegraph phase's own pass check (expected or owned entry at the pinned version, or a user-managed entry whose command resolves), evaluated after the phase in the same run, and called by `install --list`/`doctor`; the weaker "command executable" passes a broken or wrong-version binary. Residual: a later remove-then-add of codegraph killed by Coder `timeout 60` after Serena is gone leaves neither until the next boot; mitigated by §2.9 (no registry change when the entry matches).
- A-002 final: registration in scope; binary not removed; print the upstream uninstall; acceptance text and CHANGELOG state this and A-001; escalate.
- Changed: S-002 to C; C-004 guarded backstop; C-007 all layers; C-008 via Phase 1 edits.

### Variant 3 Advocate
- Accept corrected B with the stronger predicate and a guarded step-2 migration (inactive under the old pin; closes the X-001 window). Caveat: Coder cannot call IronClaude's predicate unless a read-only CLI exists (UNVERIFIED); otherwise Coder needs its own check.
- Minimum tests: unit (codegraph failed keeps Serena and exits 1; predicate table: owned pinned, user-managed resolving, user-managed not resolving, wrong version; near-miss shapes kept; `serena-local` never removed; idempotent; install/list/doctor share one function; no registry change when codegraph matches); layer-2 (seed current-pin serena + kind-B cbm, assert both absent; same seed with codegraph failing keeps Serena); Coder (step-2 image on old pin; pin-bump boot; second boot unchanged).
- New gap: project/local-scope Serena entries; at least report them.
- Binary escalated; until decided the plan records the requirement as unmet where the program exists (kind-B and the baked Coder copy).

## Round 2.5: Invariant Probe
14 findings (see `invariant-probe.md`): 2 HIGH UNADDRESSED (INV-001, INV-002), 8 MEDIUM, 4 LOW; 2 ADDRESSED.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | V2 | 90% | All three prefer B's explicit failure branch |
| S-002 | L1 | V3 | 75% | B and C advocates moved to C's two-branch tests by Round 2; A said B |
| C-001 | L3 | V2 | 95% | Unanimous; removal must live in the code `./update.sh` runs |
| C-002 | L3 | V2 (refined) | 92% | Unanimous; codegraph-ready guard, strengthened in Round 2 to the phase's own pass check; C's provenance guard fails X-003 |
| C-003 | L3 | V2 | 92% | Unanimous; bundle stop in step 2 (research 5.2 row C) |
| C-004 | L2 | V1/V3 | 80% | Migration adopted by all; majority (A, C, B conditionally) ships it guarded in step 2 |
| C-005 | L3 | V2 | 95% | B and C meet it; A conceded |
| C-006 | L3 | V2 (corrected) | 85% | All accept corrected B plus the migration |
| C-007 | L2 | V2 (combined) | 85% | B layers + C two-branch tests + A `jq -e` + `command -v` checks |
| C-008 | L2 | V2 | 88% | Unanimous; applied by amending Phase 1 texts in the same merge |
| X-001 | L3 | resolved vs V2 | 95% | B conceded; fixed by C-003 and C-004 |
| X-002 | L3 | resolved vs V1 | 100% | A conceded |
| X-003 | L3 | resolved vs V3 | 100% | C conceded |
| A-001 | L2 | QUALIFY (all) | 90% | Keep user data; state it in acceptance text and CHANGELOG |
| A-002 | L3 | REJECT (all) | 90% | Kind-B registration in scope under the same predicate; binary escalated |
| A-004 | L3 | ACCEPT with `serena-local` hint (all, Round 2) | 90% | Hint renamed; no marker |
| A-005 | L3 | ACCEPT (all) | 95% | Slug order and SHA-change rerun cited |
| A-006 | L3 | REJECT (all) | 100% | This Coder workspace runs `./update.sh` |

## Convergence Assessment
- Points resolved: 18 of 18
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 2, L2 5, L3 11 (all levels covered)
- Invariant gate: CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-001, INV-002. Both are outside what any variant can fix inside IronClaude: a root-owned image binary, and an IronClaude-installed upstream binary with companions whose automatic removal Phase 1 D2 rejected. They are escalated to the coordinator as unmet exceptions, not resolved.
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement CONVERGED); force-selected by score per FR-006.
- Unresolved points: none among diff points; escalated invariants INV-001, INV-002.
