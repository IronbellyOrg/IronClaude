# PLAN-E5: evidence-sufficiency (assurance) routing: prove headroom before paying for a router

Question (report E5): after a provisional PASS, once every decision fixed by hashes, records, caps and policy is removed, does any independently labelable semantic signal remain that a router (Jev or conventional) could exploit better than a static rule? Zero paid calls first; Jev only in shadow and only if headroom exists; no audit skipping, no autonomous PASS, no global-clean score. The end-to-end stage needs an explicit owner amendment (cap-neutral scope) and is BLOCKED without it. Read this file, `$SP/p15/plans/SHARED-CONTRACT.md` (binding) and PLAN-0 section 4.4 (`p15common.analysis`, `write_results`, `update_matrix`). PLAN-0 should be READY; if it is not, write `results.json` directly in the contract J12.1 schema and run `$SP/central/build_matrix.py` when it exists.

## 0. Rules and roles

Contract J1-J3, J11 apply; you never call Jev; `uv run --no-project` only; write only under `$E5` and your clone. **Session 1 (implementer):** zero-call headroom analysis, complete; it ends with the E5 verdict for the zero-call stage (no coordinator phase needed). **Session 2 (implementer, only if HEADROOM):** probe tooling and 24 scenarios -> READY-P. **Coordinator phase P:** labeling + `probe.py --live` -> replay or NO-GO. End-to-end: BLOCKED until the owner amends the scope.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export JEV=$SP/p15/jev E5=$SP/p15/e5 CLONE=$SP/p15/clones/jev5 BR=346Claude-jev-e5-assurance-headroom
```

## 1. Background and the pre-registered prediction

In our loop (contract J0 baseline) a provisional PASS is a re-review (or first review) with verdict PASS before the cap of 3 reviews / 2 fix cycles; today it is delivered. An assurance router could choose, at that point: deliver, or spend the one remaining review slot on a whole-document assurance review, or escalate. The static comparator (report): "full review when possible, else escalate". The frozen audits of the delivered specs say how often more assurance was needed: in the Sonnet baseline 11 of 12 audits FAIL (only a3-r5's first audit PASSes; its second FAILs); in the Haiku baseline every available audit FAILs; arm 2 has one PASS audit (a2-r6, single audit). With a residual-blocker base rate this high, "always use the remaining slot" is already the best rule, and a router can only lose: **prediction: NO-GO-OFFLINE** (no demonstrated Jev role, a valid completed result). The plan still computes it exactly from the files.

## 2. Session 1: zero-call headroom (code only; 0 workers, $0)

### 2.1 Packets (`$E5/packets.py`)

Enumerate every run with a completed loop and at least one audit, frozen as of the analysis time and listed in `offline/packets.json`:
- `$SP/p11/runs/{a1,a2,a3}-r*` (Stage 2; audit 1 in `aud/ws/<AUD_OUT>`; for a3 also `$SP/p12/baseline-audit2/a3-rK/ws/<AUD_OUT>`);
- `$SP/p14/haiku-baseline/runs/a3-r*` (audit 1; `aud2` if present by then);
- completed runs (both audits present) of `$SP/p12/ab{1,2,3}/runs/*` and `$SP/p13/ab{1,2}/runs/*` at analysis time, tagged with their design (other designs, still valid provisional-PASS states; reported as a separate stratum).

One packet per provisional PASS state: `{"run", "design", "stratum", "review_k": k, "slots_remaining": 3 - k, "fix_cycles_used", "spec_sha_at_pass", "changed_since_last_whole_review": bool, "open_blockers": n, "followups": n, "verdict_source": path}` (from `state.json` logs and the review reports; `score_themes.verdict_of`, `ids_from`). Runs that ended FAIL at review 3 (escalated) give no provisional PASS and are counted separately.

### 2.2 Code-determined actions (remove them first)

For each packet, the action is code-determined when: `slots_remaining == 0` (cap: deliver as is, or escalate if a blocker is open; no router choice), `open_blockers > 0` (not a PASS), the spec hash equals the hash already reviewed whole with no change since (no new evidence), or a mandatory policy fixes it (none in our baseline; listed as such). Remaining packets are **eligible**.

### 2.3 Independent labels (no Jev, no author): from the frozen audits

`needs_assurance = yes` when ANY available audit of the delivered spec reports a blocking finding (`len(blocking_findings()) > 0`), else `no` (adequate). Primary label = this strict rule (a delivered spec with any audit blocker needed more assurance). Sensitivity (reported, never decides): adequate when at least one audit PASSes. Single-audit packets are flagged.

Minimum required route per eligible packet: `needs_assurance = yes` -> assurance review (use the slot); `no` -> deliver. Static route: assurance review whenever a slot remains. **Headroom packets** = eligible packets whose minimum route differs from the static route (adequate specs on which static spends a review). A router cannot do better than static on any other packet: it can only skip assurance, and skipping is wrong when `needs_assurance = yes`.

### 2.4 Rule (pre-registered in `$E5/decision.toml [zero_call]`)

- **NO-GO-OFFLINE** (STOP, valid result) when headroom packets < 2, or headroom packets / eligible packets < 0.10 (the replay gate asks >= 12/120 groups that correctly avoid unnecessary broad reading), computed on the frozen-baseline packets (p11 + p14). Other-design packets are reported, not decisive.
- **HEADROOM** otherwise -> session 2.
- Also report: eligible counts by reason, the base rate of `needs_assurance`, the sensitivity result, the stratum of other designs.

### 2.5 Files and tests

```text
$E5/decision.toml      # J10.6 common sections + [zero_call] min_headroom_packets = 2, min_headroom_fraction = 0.10, label_rule = "strict-any-audit-blocker"
$E5/packets.py  $E5/labels_from_audits.py  $E5/headroom.py   # headroom.py writes offline/headroom.md, offline/headroom.json, results.json; calls update_matrix()
$E5/tests/test_e5.py
```

Tests (`uv run --no-project --with pytest pytest $E5/tests -q`): `test_packet_enumeration_on_fixture_runs`, `test_code_determined_reasons` (cap, open blocker, unchanged hash), `test_strict_and_sensitivity_labels`, `test_headroom_definition` (static vs minimum route), `test_rule_no_go_and_headroom`, `test_results_json_schema` (NO-GO, HEADROOM, BLOCKED rows), `test_real_files_smoke` (runs on the real p11/p14 files and prints the counts).

### 2.6 Results records (always written)

- Zero-call gate row: `{"arm": "E5-zero-call", "stratum": "offline", "role": "offline-gate", "verdict": "NO-GO-OFFLINE" | "PENDING", "rule": "headroom <h>/<eligible> (<pct>) < 0.10 or < 2 packets" | ..., "design_metrics": {"packets", "eligible", "code_determined_by_reason", "needs_assurance_rate", "headroom", "sensitivity_headroom"}}`.
- Live rows `k5j` (Jev router), `k5r` (conventional router), `k5s` (static routing): verdict `BLOCKED`, rule "zero-call headroom absent" or "owner cap-neutral scope amendment missing".
- `blocked_downstream`: E5 probe/replay/live when NO-GO.

### 2.7 READY / final report (session 1)

```text
E5 DONE-S1 | branch 346Claude-jev-e5-assurance-headroom @ <sha> | pushed yes/no
Packets: <n> (p11 <n>, p14 <n>, other designs <n>); escalated (no PASS) <n>; code-determined <n> (cap <n>, open blocker <n>, unchanged hash <n>); eligible <n>
needs_assurance rate (strict) <x>; headroom <h> (<pct>); sensitivity headroom <h2>
Verdict zero-call: NO-GO-OFFLINE | HEADROOM ; matrix updated: yes/no
Tests: <n> passed. Contract deviations: <none | list>
```

Snapshot/commit/push per contract J11.

## 3. Session 2 (only if HEADROOM): shadow probe

- 24 independent synthetic scenarios (`synthetic`; 12 that need more assurance, 12 adequate/clean), each a versioned evidence packet: the named unresolved question, the review/re-review summaries as code facts, and the evidence passages; x 4 transformations (original, option reorder, neutral paraphrase, misleading prior-PASS claim inside the evidence) = 96 decisions; transformations share their scenario's group. Labels per contract J8 (L1 sonnet, L2 haiku, ADJ; 3 batches of 8 scenarios).
- Questions (`QSET_VERSION = "e5-q1"`): `evidence_relation` Choice over `answered` ("The evidence states an answer to `question.text` that covers the case it names."), `conflicting` ("Two passages of the evidence give different answers to `question.text`."), `not_answered` ("The evidence discusses the topic of `question.text` but does not settle it.") plus companion Noul `evidence_relevant` ("Does `evidence` address `question.text` at all?"; true: "At least one passage of `evidence` is about the situation `question.text` names."; false: "No passage of `evidence` is about the situation `question.text` names."). Report brief (shadow) is the design reference, not a prompt: Jev cannot declare PASS, close findings, skip audits, alter grades or reset counts.
- Truth table (`policy.py`): DOWN-ROUTE (deliver without the assurance review) only when `evidence_relevant >= 0.7` and `evidence_relation` top option is `answered` with probability >= 0.7 and no code guard is active (open blocker, unchanged hash, single-audit history, mandatory policy); everything else -> the static route. A later dependent call may select an already-allowed destination only. Shadow: decisions are recorded, never applied.
- Probe advance (pre-registered): zero unsafe down-routes (DOWN-ROUTE on a scenario labeled needs-assurance, any transformation), API failures <= 5%, decision flips under reorder/paraphrase <= 2 of 48, misleading-claim transformations add no DOWN-ROUTE -> REPLAY (120 calibration + 120 held-out groups x 4; replay advance: zero unsafe down-routes or guard violations, >= 12/120 held-out groups correctly avoid unnecessary broad reading, >= 15% expected-cost improvement over static in loop-only output tokens (the saved assurance review at the baseline re-review cost, about 30k tokens), fallback <= 60%, API failures <= 5%, thresholds frozen on calibration). Else NO-GO-OFFLINE.
- Jev ceiling $5 / 30M tokens, reserved up front (contract J4); probe cost negligible (96 calls).

## 4. End-to-end (never without the owner)

Only if the replay advances AND the owner signs an explicit cap-neutral scope amendment (at most ONE remaining operational review slot used for assurance, inside 3 reviews / 2 fixes, no review 4, fallback source-reading consumes the same slot, review 3 with an unresolved assurance need escalates). Then a session 3 builds `k5j`/`k5r`/`k5s` on `p15common.harnesslib` (6 Sonnet + 4 Haiku each; interpretation needs >= 4/6 eligible routing states per treatment; advance only with no attributable safety regression, no higher false-PASS or residual-blocker counts than both controls, >= 2 useful lower-cost choices in 6 runs and >= 15% loop-only cost reduction vs static). Until then the live rows stay `BLOCKED`.

## 5. Estimates

Session 1: 1 Sonnet implementer, 0 workers, 0 Jev, about 1-2 hours. Session 2 (unlikely): 1 implementer + ~7 offline workers + 96 Jev calls (< $0.01). Replay (unlikely): ~70 offline workers, < $0.05. Live: BLOCKED (would be ~70 Sonnet + ~50 Haiku workers).

## 6. Risks

1. Audit-derived labels make "needs assurance" depend on the frozen audit (sonnet first review, noisy: a3-r5 PASS then FAIL); the strict rule and the sensitivity are both reported.
2. Few packets (about 15-20 frozen-baseline provisional PASS states); the result is a feasibility statement, not an estimate.
3. Identical evidence packets cannot separate documents with different hidden defects (report); our packets come from runs on the same spec, which makes this worse.

## 7. Decisions taken

1. Independent labels for the zero-call stage come from the frozen audits (two blinded audits per final where available), not from labeler workers: they are the independent measurement already on disk and cost nothing.
2. Primary label rule is strict (any audit blocker = more assurance needed); sensitivity reported.
3. The decisive packet set is the frozen baseline (p11 + p14); packets from still-running designs are reported separately.
4. The Choice in the probe has three mutually exclusive relations plus a companion relevance Noul (the report's fourth option `irrelevant` becomes the companion; contract J7).
5. Without the owner's cap-neutral amendment no E5 live arm is built, even after a passing replay.
