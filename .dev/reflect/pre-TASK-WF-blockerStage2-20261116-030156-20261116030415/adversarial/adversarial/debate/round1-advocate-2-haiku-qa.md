# Round 1: Advocate for Variant 2 (reviewer-2, qa, haiku class)

Persisted by the orchestrator from the advocate's returned message.

**Position summary.** V2's strength is separating a demonstrated wrong result from a plan that could still be executed correctly. I defend its restraint on X-001-X-003, but concede that missing command access and unattended handling need blocking findings.

**Steelman of V1.** V1 correctly distinguishes runnable integration from prose naming a function: Tasks 1-2 build a sweep function, then instruct an installed skill to call it without defining its command interface (PLAN:33,50). Its safety-count objection also matches V2's strongest finding: confirmation by a later reviewer or owner is not derivable merely from a ledger (S0:130; PLAN:110). Its explicit earlier-review check is useful, although not proof of complete coverage.

**Steelman of V3.** V3's strongest argument is that integration must work outside this checkout. The repository requires installed primitives to reach package behavior through the CLI, so callable modules alone are insufficient (`CLAUDE.md:95`; S1:110,171; PLAN:33,50). V3 also identifies the historical-evidence limitation: S0 resolves `@E2` through git, whereas S1's supplier reads disk and forbids subprocess use (S0:116; S1:148,153).

**Strengths claimed**
1. V2 exposes unsupported safety counts. Under the proposed definition, "no confirmation supplied" cannot establish "zero misses". Task 7 needs confirmation evidence or an explicit unknown result (S0:130; PLAN:110,114).
2. V2 avoids inventing a regression from omitted tests. The existing test protects "no minimum count"; adding reviewer fields need not remove that text. The omission is a verification gap, not proof of broken behavior (TEST:271-283; PLAN:50,58,67).
3. V2 separates wording from execution. GR12 is explicitly live during shadow mode; qualifying "every gate outcome" preserves the intended exception rather than changing scope (PLAN:20,50; PSPEC:592-594).

**Weaknesses in V1 and V3**
1. V3 overgrades X-001. An executor can record `classifier=unavailable` rather than invent agreement. That is the required fallback, not an impossible implementation; the summary must disclose that agreement is unavailable (S1:176; PSPEC:586; PLAN:110).
2. V3 overgrades X-002. Missing source names warrant repair, but PLAN:19 permits reading prior-stage evidence, and S0:82,96 identifies the populations and consensus. For inaccessible evidence, PLAN:104 expressly permits UNSET/NA.
3. V3's premature-edit claim (R3-5) is not forced. PLAN:20 already forbids starting before the prerequisites; moving checks into the body clarifies order but does not establish an unavoidable unauthorized edit.
4. V1's consolidation ambiguity (R1-8) is credible but not a demonstrated omission. The existing phase consolidation explicitly includes post-completion output (`task/SKILL.md:252,338-340,405`); the plan should name fidelity consolidation too.

**Concessions about V2.** V2 did not examine Tasks 1, 4 and 5 deeply. C-001 and C-002 are blocking: command access is missing, and unconditional halt offers conflict with record-only unattended behavior (PLAN:33,50,57; PSPEC:434-441). Task 4's no-question test does not itself specify the missing skill branch (PLAN:74-79). V2 also overstated the safety-miss definition as settled: S0 marks it proposed for owner acceptance. C-003 remains blocking if that definition is accepted; otherwise an accepted definition must first be established (S0:130,136).

**Per diff point verdicts**

| Point | Winner | Conf. | Verdict |
|---|---|---:|---|
| C-001 | V3 | 97% | Blocking: functions need an installed command interface |
| C-002 | V1 | 96% | Blocking: suppress offers and return unattended results |
| C-003 | V2 | 95% | Blocking under the accepted definition; confirmations need an input |
| C-004 | V1 | 94% | Minor clarification: replicates per judge, preserve blindness |
| C-005 | V2 | 99% | Minor wording: keep "no capture failure" |
| C-006 | V2 | 97% | Minor verification gap, not a demonstrated regression |
| C-007 | V1 | 90% | Minor ambiguity: enumerate consolidation coverage |
| C-008 | V2 | 94% | No forced defect: prerequisite is already a global constraint |
| C-009 | V2 | 94% | No impossible check: mapping exists; signature is an implementation choice |
| C-010 | V2 | 97% | Minor traceability omission |
| X-001 | V1 | 97% | Minor: executor reports unavailable, not fabricated agreement |
| X-002 | V1 | 94% | Minor: recover named-stage sources and disclose unsupplied inputs |
| X-003 | V2 | 99% | Minor: clarify the blanket sentence |

**Shared assumptions**
- A-001: QUALIFY. Acceptance lines govern checks, but global constraints also bind; the executor reads task text before acting.
- A-002: QUALIFY. Prior plans describe expected interfaces, not built facts. Verify prerequisites and accepted definitions before execution (PLAN:20,36-37; S0:130).
- A-003: REJECT as a blanket assurance. Task 5 specifies field-removal and registry-transition tests; Task 4 specifies contract tests but does not close Task 2's unattended integration gap (PLAN:74-89).
- A-004: QUALIFY. The old rule already permits Medium follow-up candidates, so the ledger need not be empty. Native minor labels must not automatically become Medium; preserve family-specific mapping and Note distinctions (`pragmatic.md:229-231`; S1:59; PSPEC:733-738).
