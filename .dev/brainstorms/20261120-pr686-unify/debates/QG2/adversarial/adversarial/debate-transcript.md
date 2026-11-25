# Adversarial Debate Transcript

## Metadata
- Depth: quick (Round 1 only; Round 2, Round 2.5 invariant probe and Round 3 skipped by depth)
- Rounds completed: 1
- Convergence achieved: 66.7% (8 of 12 debate points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (general-purpose agents, model sonnet, read-only, run in parallel)
- Log: Round 2 skipped: depth=quick. Round 2.5 (invariant probe) skipped: --depth quick.
- Orchestrator note: the advocates' statements below are condensed to their decision-relevant content; the full text was returned to the orchestrator in-session (agent ids a51ea68354e611e8e for Variant A, af4dada0d33681348 for Variant B).

## Round 1: Advocate Statements

### Variant A Advocate (OURS, sonnet)
**Position**: A is the safer base: it never lets a wording rule silence a safety escalation and never adopts a rule that no check can enforce and that current practice already breaks. Two separable B benefits are adopted as hybrids: the offline template scan and a capped notice for the three post-merge audit escalations.

**Steelman of Variant B**: B follows the design as written (D:830-832 ruling 15; D:841 handoff line; D:682 and D:686 notice and cap). Refusal matches `escalate` (D:684). A fail-open mask is a bypass that edits trusted text without saying so. The notice is the only way to reach a person who is away, and AU4a, AU4c, AU5 land after the merge on an unprotected `master`. B adds shape rules (one per PR, warnings never reach the person, entry always written, cap never drops an entry).

**Key strengths claimed**:
1. D:847: a worker PR body "cannot be scanned before it is written", so only scope B is mechanically checkable.
2. 25 of the last 30 merged PR bodies carry "Generated with"; B concedes the same count.
3. INV-013: a refused merge-safety escalation fails silently (its file list holds `.claude/settings.json`; the repo is IronClaude).
4. D:692: an unanswered item waits; a silent refusal makes it wait for nobody.
5. Owner memory `orchestration-decision-ledger-only` and named triggers for each deferral.

**Weaknesses identified in Variant B**:
1. Scope A is a prompt convention only for the largest class of writers (D:847).
2. The D:841 handoff line makes today's PR-body practice a violation; D:832 allows only the commit trailer.
3. Fail closed has a named silent failure; "must rewrite the text" is a hope.
4. B calls cap default 0 safe, yet `pr-a/.../repos.py:262-269` treats 0 or unreadable as no cap while the design value is 5 (D:877).
5. The notice sender is not shown built in master (B marks it UNVERIFIED).

**Concessions**:
- D:686, D:877 and D:1170 call the cap settled (ruling 39); the "cap unsettled" argument is weak. (Orchestrator check: D:1177 puts "not ruled on; open" in the question column and "Settled as recommended (ruling 39)" in the decision column; the ruling is Clay's.)
- Ruling 15 literally says scope A.
- Entry lines alone give no push to a person who is away.

### Variant B Advocate (CLAY, sonnet)
**Position**: B follows the design as written (ruling 15, the refusing writer style, the three-way route). Its clearest separable benefits: the handoff line, the notice for post-merge breakage, the cap being settled. A is right on enforcement limits and on the silent-refusal risk.

**Steelman of Variant A**: No mechanical check exists for a worker PR body (D:847). Practice puts the attribution in 25 of 30 bodies. A refusal can leave a held merge unannounced (INV-013). The notice sender is not shown built, and D:825 item 2 names entry lines for AU4a, AU4c, AU5. A ties each deferral to a trigger.

**Key strengths claimed**:
1. B states the rule as ruled; D:832 covers "a worker it started"; D:841 already writes the handoff line.
2. D:684 shows refusal is the design's one style; masking edits text a person reads without saying so.
3. The notice is part of the design (D:682); the audit runs after landing, when a person away from the report most needs a push.
4. The cap is settled (D:686, D:877 default 5, D:1170).
5. A's chatter argument assumes cap 0; the design default is 5; over-cap notices are batched; entries never dropped.
6. Careful escalation shape and a test design (D:825, D:847).

**Weaknesses identified in Variant A**:
1. A cites D:1177 as open; D:686, D:877, D:1170 say settled (orchestrator check: both texts are in D:1177).
2. Fail open writes a masked "[removed]" into text a person relies on; A's condition (never mask a path, sha or number) is unverified against the templates.
3. Entry-lines-only relies on a person opening the report (A's own risk section concedes it).
4. "No check" is not "no rule": the handoff line and tests cover scope A.

**Concessions**:
- INV-013 is real; a refused merge-safety escalation fails silently unless refusal is loud and templates fence paths.
- Scope A makes 25 of 30 PR bodies non-compliant, and the handoff line conflicts with the harness's own PR-body instruction.
- The notice sender is not shown built; D:825 item 2 names entry lines, not the notice, for the audit escalations.

## Per-advocate verdicts and shared assumptions

| Point | Advocate A says | Advocate B says | Agreed |
|-------|-----------------|-----------------|--------|
| S-001 | A | A | yes |
| S-002 | A | A | yes |
| C-001 | A | HYBRID (state at scope A, enforce on two writers) | no |
| C-002 | A | B | no |
| C-003 | A | HYBRID (keep refusal, make it loud, fence paths, rewrite and resend) | no |
| C-004 | HYBRID (entry lines always; notice for AU4a/4c/5 only, cap 5, once a sender is tested) | HYBRID (entry lines always; notice through the existing `escalate` route) | yes |
| C-005 | B (cap settled at 5; align code default) | B | yes |
| C-006 | A | A | yes |
| X-001 | A | A | yes |
| X-002 | HYBRID (adopt offline template scan and fake `launch.effective` test) | A | no |
| A-002 | QUALIFY: the rulings are the design owner's (Clay); the user's practice is not shown bound | QUALIFY: no ironbelly record found | yes |
| A-003 | QUALIFY: entry lines suffice for held items, not for post-merge hits (INV-014) | QUALIFY leaning REJECT: holds for AU1/AU3 only | yes |

## Scoring Matrix

Weighting rule applied (OURS wins unless a clear evidenced CLAY benefit; ties go to OURS; separable benefit adopted as hybrid).

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | A | 60% | Same section set; tie goes to OURS |
| S-002 | A | 60% | Layout only; tie goes to OURS |
| C-001 | A | 70% | D:847 no scan of worker bodies; 25 of 30 (clayphi 17/21, ironbelly 8/9) carry the line; B conceded; ruling 15 is Clay's (A-002) |
| C-002 | A | 65% | Handoff line contradicts the owner's own practice (8 of 9) and the tool convention; no evidenced benefit; owner confirms in chat |
| C-003 | A (with two adoptions from B) | 72% | INV-013 silent failure; D:692; B conceded; adopt B's visible mask marker and fenced paths |
| C-004 | HYBRID | 68% | Both advocates agree; A-003 qualifies; INV-014 post-merge arrival; sender unbuilt (UNVERIFIED) so notice is reserved with triggers |
| C-005 | B on the fact, A on the status | 60% | Design records cap 5 as settled by Clay's ruling 39 (D:686, D:877, D:1170, D:1177); not an owner ruling; code default 0 (`repos.py:262-269`) |
| C-006 | A | 75% | Both agree: run U54 before the rule is switched on |
| X-001 | A | 80% | INV-013; both advocates agree |
| X-002 | HYBRID | 65% | Worker bodies cannot be scanned (D:847); the offline template and fixture scan is scope-independent and is adopted |
| A-002 | Promoted: QUALIFY | 85% | Both: rulings are Clay's as "owner"; no ironbelly record |
| A-003 | Promoted: QUALIFY | 80% | Entry lines suffice for held items, not for post-merge hits |

## Convergence Assessment
- Points resolved: 8 of 12 (S-001, S-002, C-004, C-005, C-006, X-001, A-002, A-003)
- Alignment: 66.7%
- Threshold: 80%
- Status: NOT_CONVERGED (max rounds for depth quick; Round 2 not run)
- Unresolved points: C-001, C-002, C-003, X-002 (resolved by the weighting rule in the scoring matrix, not by advocate agreement)
- Taxonomy coverage: L1 (S-001, S-002, C-006), L2 (C-001, C-002, C-004, C-005, X-002, A-002), L3 (C-003, X-001, A-003) all covered; gate satisfied.
- Invariant probe gate: not applied (skipped at depth quick). The D15 probe items INV-013 and INV-014 already cover this topic and were used as evidence.
