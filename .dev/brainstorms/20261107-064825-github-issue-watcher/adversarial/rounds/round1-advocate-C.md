# Round 1 — Advocate C (backend)

## Position summary

C provides the strongest data-integrity contract: consume a durable dispatch slot before external submission, never release it on lease expiry, and distinguish session acceptance from posted claim evidence (C §§1, 4 FR-010–012, 7). Keep that core, but merge B's concrete adapter verification, D's operational controls, and E's candidate-scaled discovery without importing their replay paths (B §4 FR-014; D §8; E §4 FR-008).

## Steelman per opposing variant

- **A:** Its strongest form is a comprehensible, replaceable pipeline with explicit command allowlisting, testable acceptance criteria, offline inspection, and corrupt-record rejection (A §§1, 4 FR-019–020, 5 NFR-003, 7–8). Those are real implementation aids; stage isolation need not mean adopting A's expired-pending retry rule (A §7).
- **B:** Its strongest form connects root causes to mechanisms, verifies worktree origin and executable identity, preserves retry working directory, and explicitly marks unverified fixtures (B §§1.1, 4 FR-002/014/016, 8.3). Its timeout-without-ID handling and non-resetting reapproval counter correctly recognize ambiguity and abuse risks (B §7.3, §10 OD-6).
- **D:** Its strongest form treats unattended polling as an operated batch job: kill switch, offline status/staleness, private state permissions, exit-code actions, and shadow rollout (D §4 FR-018/021, §5 NFR-011, §8). Orphaned pending records deliberately sacrifice availability rather than risk duplicate starts (D §7).
- **E:** Its strongest form bounds both expensive sessions and API work, filters locally before per-issue requests, and avoids whole-Project discovery through issue-local membership queries (E §4 FR-004/008/018, §5). It correctly states that missed dispatch is cheaper than duplicate launch and treats unknown outcomes conservatively (E §7).

## Strengths claimed

1. **A genuine submission invariant.** C commits consumed-slot plus `unknown` before I/O, then forbids ordinary resubmission even after expiry or explicit post-consumption failure. That covers the crash-after-submit/before-reply gap without assuming when a marker arrives (C §7; §5 NFR-002). This is at-most-once submission, not exactly-once execution.
2. **Stable identity throughout the contract.** Repository/issue node IDs anchor uniqueness; account IDs anchor owner and approver identity; label, field, and option IDs anchor policy. Renaming a login or moving worktrees cannot silently create another dispatch key (C §§3, 7). C explicitly acknowledges independent ledgers and cloned backups invalidate this boundary (C §11).
3. **Selection evidence is refreshed, not inferred.** C refreshes ownership, approval provenance, and Project evidence, rejects incomplete evidence, excludes PRs/drafts/archived items, and admits the unavoidable refresh-to-launch race (C §3; §4 FR-006/008). Other variants' issue-only refresh does not prove the Project is still Backlog (A FR-010; D FR-011; E FR-012, all §4).
4. **Data loss is not interpreted as permission.** C requires explicit initialization and rejects corrupt or missing-after-initialization state; transitions and slot consumption share a transaction (C §5 NFR-003; §7). The permanent-suppression trade-off is written down rather than hidden behind a retry counter (C §7).
5. **Operational truth is preserved.** Accepted launch, unknown launch, and recognized posted claim are separate outcomes; assignment alone proves none of them (C §§1, 4 FR-011/012). Backoff survives process exit, and deployment remains blocked until narrative-read risk and permissions are addressed (C §5 NFR-004; §6).

## Weaknesses identified in others

1. **A's lost-reply path reopens the critical window.** Expired `pending` without a marker becomes retryable `failed`; expired `unknown` can also become `failed`. Neither proves a session did not start, so another ordinary submission is possible (A §7 transitions). This cannot support a lifetime at-most-once claim.
2. **B explicitly chooses weaker semantics.** A `launched` issue can launch again after its lease; orphaned `pending` becomes `launched` and inherits that route (B §7.3). Its corrupt-state-as-empty rule also destroys pre-marker exclusion (B §5 NFR-010). These are substantive integrity differences, not notation preferences.
3. **D's success counter is not a submission counter.** `launches` increments on success or recognized unknown, while an “other error” moves to retryable `failed` with zero launches (D §7). Without a complete timeout/malformed-output classification, a possibly started session can follow that retry path. Its recovery instruction to remove an abandoned entry also needs an explicit guarantee-reset warning and evidence checks (D §7).
4. **E's pruning conflicts with durable exclusion.** Removing a 30-day-old `abandoned` record can expose a previously submitted but unmarked issue as new; the claim marker cannot guard an issue whose claim never posted (E §5 NFR-013; §7). “Any other error” becoming `failed` also needs narrowing to proven non-start (E §4 FR-015 versus §7's definition).
5. **Optional Project bypass changes the feature.** A's `off` and B's `--label-only` admit issues without the required Project/Backlog evidence. Explicit opt-in makes degradation visible but does not satisfy the original predicate (A §10 OD-5; B §4 FR-022/§10 OD-5; seed Success Criteria).
6. **Budget certainty exceeds adapter evidence.** E's one-events-call and 33-call arithmetic omit paginated histories; complete approval verification cannot be traded away for a call ceiling (E §4 FR-006; §5). D's observability targets are useful proposals, but SLO success must not obscure unknown submissions or exhausted candidates (D §5 NFR-013; C §5 NFR-005/008).

## Concessions

- **C is less executable as a contract.** It lacks a literal complete launch/reconciliation argv, a configuration schema, stable decision IDs, and a transition-by-transition test table. Borrow A/B's concrete contracts and D's runbook, without copying retry semantics (C §§4, 7–8, 10 versus A §4 FR-012/015; B §4 FR-014/016; D §8).
- **SQLite is a proposal, not a proof.** C does not specify durability settings, initialization evidence outside the lost store, backup/restore discipline, or how to detect a nonpersistent mount. Losing the whole directory defeats a sentinel stored only there; transactional invariants matter more than storage branding (C §5 NFR-003; §§7, 11). A corrected JSON design could satisfy them.
- **C needs one unambiguous ordering.** FR-008 says refresh before reservation; §7 permits refresh from `pending`. Specify reservation, final refresh, atomic consumed-slot commit, submission; stale reservation may cancel, consumed slot never resets (C §4 FR-008/010; §7). Same-operation retry also needs stored invocation context (B §7.2–3).
- **C's stricter policies impose costs.** Sole assignee, account-ID governance, archived-item exclusion, and permanent consumed keys require owner approval and operator support; no source establishes that one authority is technically enforced (C §§3, 7, 10). Accept the missed-work trade-off only explicitly.
- **C should borrow performance and operations, not overbuild them.** E's issue-local Project strategy and local prefiltering, B's assumed-shape fixtures, and D's disable/staleness controls improve C (E §4 FR-004/008; B §8.3; D §4 FR-018/021). All adapter shapes still need the owner-run validation C §9 requires; no live behavior was verified here.

## Shared-assumption responses

A-001: QUALIFY — Local storage is acceptable only with verified persistence and controlled restore; a surviving marker does not protect the pre-marker interval (C §§7, 9, 11).

A-002: QUALIFY — Prompt transport remains an unverified deployment prerequisite, not evidence of slash-command execution; require the controlled owner-run test (C §9; seed Enrichment).

A-003: REJECT — Names are not the durable identity contract: C uses account/node IDs and retains logins for display; approved ID mappings must not silently rebind by matching names (C §§3, 7).

A-004: QUALIFY — One nominated authority is an operational boundary, not distributed exclusion; a second independent ledger invalidates at-most-once guarantees (C §§1, 7, 11).

A-005: QUALIFY — Assignment must exist at eligibility evaluation, not necessarily precede the approval event. An unassigned issue waits until assigned; document that human step and rejection reason (C §3; B §10 OD-1).

A-006: QUALIFY — Clock jumps threaten availability, backoff, and fairness, but must never reopen consumed slots. Add jump tests, monotonic in-process deadlines, and a persisted ordering sequence where appropriate (C §5 NFR-004/007; §7: “Expiry never releases a consumed slot”).

A-007: QUALIFY — Validate locking and transaction behavior on the selected persistent local filesystem; no cross-host guarantee follows from a local lock (C §§7, 11).

A-008: QUALIFY — Actor metadata establishes who applied the label, not their actual decision process. Administratively verify human accounts and approval procedure; a `User`-typed automation account remains a residual (C §3; D §6 T3).

A-009: REJECT — A 60-minute marker deadline is not required for exclusion in C, nor for confirmed `launched` entries in A/D/E: expiry does not authorize their fresh launch. B's lease retry does depend on timely evidence, and A's orphan path is unsafe (C §7; A §7; B §7.3; D §7; E §7).

A-010: QUALIFY — Configuration writers must be explicitly trusted administrators, not necessarily only the workspace owner; enforce protected ownership/permissions and govern updates. C names trusted configuration but leaves these mechanics underspecified (C §§3, 6; D §6 T2).

## Per-point positions

Levels reproduce the diff analysis; confidence concerns the comparative judgment, not production readiness. HYBRID identifies an explicit combination, not a blanket endorsement.

| Point | Level | Superior variant | Confidence % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | NONE | 95 | Every style supplies acceptance criteria; notation alone proves no contract advantage (§§4–5, all variants). |
| S-002 | L1 | NONE | 99 | More numbered requirements do not establish coverage or consistency (§§4–5, all). |
| S-003 | L2 | HYBRID | 93 | B §1.1 explains causes; D §8 supplies operation; E §5 supplies cost; C §2 preserves revisit boundaries. |
| S-004 | L2 | C | 85 | C §8 separates effects, selection, and transactional storage without A §8's speculative replacement interfaces. |
| S-005 | L3 | C | 96 | C §7 couples slot and transition transactionally; initialization/corruption protections require further mechanics. |
| S-006 | L1 | B | 85 | B §10's decision IDs support precise sign-off; C's unnumbered decisions are harder to reference. |
| S-007 | L1 | HYBRID | 88 | C §12 distinguishes proposals from facts; B §12 adds recognizable source identifiers. |
| S-008 | L1 | B | 88 | B §11 provides risk IDs plus impact/mitigation; C §11 is prose, despite the diff calling it a table. |
| C-001 | L3 | C | 95 | C §3 pins label ID, while still proposing display names; name-only equality is weaker identity. |
| C-002 | L3 | C | 96 | C §3 requires trusted account ID, non-bot metadata, and complete history; intent remains administrative. |
| C-003 | L3 | HYBRID | 96 | Combine C §3's field/option identity and exclusions with E §4 FR-008's issue-local Project reads. |
| C-004 | L3 | C | 96 | C §3 anchors sole ownership to account ID and explicitly states its stricter-than-claim policy. |
| C-005 | L3 | HYBRID | 94 | C §7 states unsupported independent authorities; A §10 OD-2 adds disabled-by-default setup protection. |
| C-006 | L3 | HYBRID | 95 | E §4 FR-004 prefilters cheaply; C FR-006 requires complete evidence, not a permanent Project-size ceiling. |
| C-007 | L3 | C | 99 | C §7 makes consumed intent durable before I/O rather than inferring it from reply counters. |
| C-008 | L3 | C | 95 | C §7 separates safe pre-submission attempts from one ordinary submission; numerical defaults remain proposals. |
| C-009 | L3 | C | 98 | C FR-008/010 and §7 preserve final refresh plus atomic consumption; clarify reservation ordering. |
| C-010 | L2 | HYBRID | 96 | A FR-012 supplies fixed argv; B FR-002/014 verifies origin and executable; C needs both (§4). |
| C-011 | L3 | C | 99 | C FR-011 and §7 classify malformed/timeout as unknown; absent ID never licenses fresh retry. |
| C-012 | L3 | HYBRID | 97 | A FR-011 supplies explicit type/range cases; D NFR-001 adds property tests; C §10 fixes the range. |
| C-013 | L3 | C | 94 | C §§3/10 uses trusted account IDs and admission checks; add protected-update mechanics. |
| C-014 | L2 | HYBRID | 97 | C §6 gates narrative-risk acceptance and policy verification; B §10 OD-8 requires explicit bypass-risk acceptance. |
| C-015 | L3 | C | 95 | C NFR-006 separates global integrity/auth failures from candidate-local malformed evidence (§5). |
| C-016 | L3 | HYBRID | 96 | C NFR-004 persists retry timing; E NFR-005 provides a hard call cap; pagination must count (§5). |
| C-017 | L2 | HYBRID | 94 | C §9 checks persistence/shutdown; D §8 adds shadow rollout and observable staleness. |
| C-018 | L3 | HYBRID | 96 | C §7's integrity boundary plus D FR-018's disable-before-effects control is stronger than either alone. |
| C-019 | L2 | HYBRID | 96 | C NFR-005 gives candidate transitions; A NFR-007 closes reasons; D NFR-006 adds runtime context (§5). |
| C-020 | L2 | HYBRID | 94 | Keep C §8's explicit initialization/inspection and D §8's operator actions; avoid unguarded reset semantics. |
| C-021 | L2 | HYBRID | 90 | A §8 JSON configuration plus C §10's ID/authority policy needs one explicit validated schema. |
| C-022 | L2 | HYBRID | 98 | C §8 covers concurrency/rename; B §8.3 marks assumed shapes; E §8 adds repeated-cycle checks. |
| C-023 | L2 | HYBRID | 94 | B §9 validates launch contracts; C §9 checks lifecycle; D §9 adds operational follow-through. |
| C-024 | L3 | C | 96 | C FR-012 distinguishes recognized posted evidence from assignment; §11 denies full-artifact completion proof. |
| C-025 | L2 | HYBRID | 95 | C §6 admits necessary marker inspection; D §3 projects a boolean, minimizing narrative retention. |
| X-001 | L3 | C | 99 | C §7 never releases consumed slots; B §7.3 explicitly relaunches accepted sessions after lease. |
| X-002 | L3 | C | 99 | C §7 separates unconsumed reservation from durable consumed intent; A's lost-reply retry lacks that proof. |
| X-003 | L3 | HYBRID | 99 | C NFR-003, A §7, D NFR-011 reject corruption; B NFR-010 silently resets exclusion (§5). |
| X-004 | L3 | C | 99 | C FR-011 treats timeout/malformed reply as unknown and keeps the slot consumed (§4/§7). |
| X-005 | L3 | HYBRID | 99 | C FR-006, D OD-4, E O-3 refuse Project-free eligibility; A/B's bypasses change the predicate. |
| X-006 | L3 | C | 97 | C NFR-004 honors persisted retry timing across cycles instead of treating five minutes as universal backoff. |
| X-007 | L2 | HYBRID | 92 | C §8 separates unknown-launch attention; D §8 ties codes to actions; choose one mapping, not both. |
| X-008 | L2 | HYBRID | 97 | Preserve all D1–D3; A/B/D §4 fix the agent; C §6 correctly separates marker reads from prompt content. |

