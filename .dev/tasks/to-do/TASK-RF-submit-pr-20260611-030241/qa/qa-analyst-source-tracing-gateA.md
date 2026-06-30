# QA Analyst Report — Phase Gate A — Lens: SOURCE-TRACING

**Generated:** 2026-06-11
**Lens:** SOURCE-TRACING
**fix_authorization:** false (report-only)
**Stance:** ADVERSARIAL (assume ≥5 invented/mis-traced elements; trace exhaustively)

**Spec:** `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
- §7 (lines 473–507) — Detection-Contract Design
- §11.3 (lines 718–733) — Run-Log Event envelope & types
- §12.1 (lines 754–776) — Write-ahead push ordering & crash-window resume

**Artifacts under trace:**
- `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`
- `src/superclaude/pr_submit/models.py`
- `src/superclaude/pr_submit/classifier.py`
- `src/superclaude/pr_submit/detection.py`

---

## Trace 1 — models.py 33rd event `push_aborted_or_not_landed` → §12.1 line 771

**Element:** `models.py:70` — `PUSH_ABORTED_OR_NOT_LANDED = "push_aborted_or_not_landed"`
**Spec citation:** §12.1 line 771 — `push_aborted_or_not_landed{recovered:true}` (the "not reachable" crash-window branch).

**Verdict:** TRACED. The enum value string `"push_aborted_or_not_landed"` is byte-exact with the event name emitted at spec line 771. The module docstring (`models.py:3-4`, `models.py:69`) explicitly attributes it to "§12.1 line 771 — the crash-window not-landed branch." Citation is correct and the line number stated in the code comment matches the spec. No finding.

---

## Trace 2 — The 32 base events → §11.3 lines 724–731

**Method:** Enumerate the spec event list (lines 724–731) and the `EventType` members (`models.py:29-68`, excluding the 33rd from Trace 1). Cross-check (a) every spec event appears in the enum, (b) every enum base member appears in the spec list, (c) no invented name.

| # | Spec event (line) | Enum member (models.py line) | Match |
|---|---|---|---|
| 1 | run_started (724) | RUN_STARTED (29) | ✓ |
| 2 | environment_check (724) | ENVIRONMENT_CHECK (30) | ✓ |
| 3 | pr_create_attempted (724) | PR_CREATE_ATTEMPTED (31) | ✓ |
| 4 | pr_created (724) | PR_CREATED (32) | ✓ |
| 5 | monitor_armed (724) | MONITOR_ARMED (33) | ✓ |
| 6 | baseline_captured (725) | BASELINE_CAPTURED (34) | ✓ |
| 7 | poll_attempt (725) | POLL_ATTEMPT (36) | ✓ |
| 8 | poll_result (725) | POLL_RESULT (37) | ✓ |
| 9 | api_backoff (725) | API_BACKOFF (38) | ✓ |
| 10 | classifier_unknown_shape (725) | CLASSIFIER_UNKNOWN_SHAPE (39) | ✓ |
| 11 | review_detected (726) | REVIEW_DETECTED (40) | ✓ |
| 12 | findings_normalized (726) | FINDINGS_NORMALIZED (41) | ✓ |
| 13 | finding_verified (726) | FINDING_VERIFIED (43) | ✓ |
| 14 | finding_unverified (726) | FINDING_UNVERIFIED (44) | ✓ |
| 15 | round_incremented (726) | ROUND_INCREMENTED (46) | ✓ |
| 16 | route_decision (726) | ROUTE_DECISION (47) | ✓ |
| 17 | troubleshoot_started (727) | TROUBLESHOOT_STARTED (49) | ✓ |
| 18 | troubleshoot_completed (727) | TROUBLESHOOT_COMPLETED (50) | ✓ |
| 19 | fix_applied (727) | FIX_APPLIED (51) | ✓ |
| 20 | validation_started (727) | VALIDATION_STARTED (53) | ✓ |
| 21 | validation_completed (728) | VALIDATION_COMPLETED (54) | ✓ |
| 22 | push_decision (728) | PUSH_DECISION (56) | ✓ |
| 23 | push_initiated (728) | PUSH_INITIATED (57) | ✓ |
| 24 | push_completed (728) | PUSH_COMPLETED (58) | ✓ |
| 25 | reply_posted (728) | REPLY_POSTED (60) | ✓ |
| 26 | thread_resolved (729) | THREAD_RESOLVED (61) | ✓ |
| 27 | idempotency_skip (729) | IDEMPOTENCY_SKIP (62) | ✓ |
| 28 | terminal_clean (729) | TERMINAL_CLEAN (64) | ✓ |
| 29 | terminal_timeout (729) | TERMINAL_TIMEOUT (65) | ✓ |
| 30 | terminal_max_rounds (729) | TERMINAL_MAX_ROUNDS (66) | ✓ |
| 31 | terminal_halted (730) | TERMINAL_HALTED (67) | ✓ |
| 32 | terminal_failed (730) | TERMINAL_FAILED (68) | ✓ |

**Counts:** Spec list = 32 distinct events. Enum base members (excluding `PUSH_ABORTED_OR_NOT_LANDED`) = 32. Total enum = 33, matching the manifest's "EXACTLY 33 members" criterion.

**Invented-event check:** No enum member exists that is absent from the spec list. **Spec-event-missing check:** No spec event is absent from the enum. The line-732 sentence ("`push_decision`, `push_initiated`, `push_completed` are the write-ahead push triad") is descriptive prose, not a separate event, and is correctly not counted.

**Verdict:** TRACED. All 32 base events map 1:1 to §11.3 lines 724–730, byte-exact, no invented or missing event. No finding.

---

## Trace 3 — classifier bot-login keying → §7 consequence 1 (lines 496–498)

**Element:** `classifier.py` — three-state classifier keyed on `contract.augment_bot_login`, never a literal.
**Spec citation:** §7 consequence 1 (lines 496–498): "The parser is generic. It contains `if login == contract.augment_bot_login`, never a literal string. The login lives in data."

**Evidence (classifier.py):**
- `classify` reads the login from the contract: `classifier.py:70` — `bot_login = getattr(contract, "augment_bot_login", None)`.
- Equality is keyed on that value, not a literal: `classifier.py:43` — `[e for e in entries if isinstance(e, dict) and _login_of(e) == bot_login]`. This is the spec's `if login == contract.augment_bot_login` shape.
- No literal Augment login string ("augment-code[bot]", "augment-code", etc.) appears anywhere in `classifier.py`. (The only `augment-code[bot]` literal in the whole package is `detection.py:139`, inside `poll_augment_review`'s default-contract fallback for the empty-reviews "polling" path — NOT in the classifier, and NOT used as a hard-coded match against payload data. It seeds a default contract object; classification still keys on `contract.augment_bot_login`.)
- Behaviour matches consequence 1's named test mappings: different bot login → "review not detected" (T-211, `classifier.py:60-77`); interleaved Augment+human → only Augment author parsed (T-212, `classifier.py:80-86` via `_augment_entries`).

**Adversarial probe:** Checked whether the `detection.py:139` literal `"augment-code[bot]"` constitutes a "literal bot-login in the classifier" violation of §7 consequence 1 or manifest AC ("classifier never embeds a literal bot-login"). It does not: (a) it is in `detection.py`, not `classifier.py`; (b) it populates a default `DetectionContract` for the no-data polling seam, not a comparison constant; (c) the live arming path loads the locked contract upstream (T-210) and does not use this default — documented at `detection.py:137-139`. This is a seam default, not a hard-guessed detection constant. Noted, not a finding.

**Verdict:** TRACED. The classifier keys on `contract.augment_bot_login` exactly as §7 consequence 1 prescribes, embeds no literal login, and the cited T-211/T-212 behaviours are present. No finding.

---

## Trace 4 — detection-contract.md YAML schema → §7 YAML block (lines 481–492), field-by-field

**Element:** The fenced YAML block in `detection-contract.md:14-25`.
**Spec citation:** §7 YAML block, lines 481–492.

| Field | Spec value (line) | Ref value (detection-contract.md line) | Match |
|---|---|---|---|
| augment_bot_login | `"<PROBE-LOCKED>"` (483) | `"<PROBE-LOCKED>"` (16) | ✓ |
| augment_author_association | `["NONE", "CONTRIBUTOR"]` (484) | `["NONE", "CONTRIBUTOR"]` (17) | ✓ |
| augment_app_slug | `"augment-code"` (485) | `"augment-code"` (18) | ✓ |
| emission_shape | `"<review\|issue_comment\|check_run>"` (486) | same (19) | ✓ |
| findings_locus | `"<reviews[].body\|comments[]\|check_run.output>"` (487) | same (20) | ✓ |
| severity_field_path | `"<jsonpath-or-null>"` (488) | same (21) | ✓ |
| review_completeness_signal | `"<state==COMMENTED\|presence-of-summary-marker>"` (489) | same (22) | ✓ |
| probe_evidence | `"<abs-path to captured gh json>"` (490) | same (23) | ✓ |
| locked | `false` (491) | `false` (24) | ✓ |

**Field count:** 9 fields in spec; 9 fields in ref. Manifest AC requires "9 fields … `locked` is `false` … NO hard-guessed bot login (`augment_bot_login` stays `<PROBE-LOCKED>`)." All satisfied.

**Adversarial probes:**
- **Value drift:** Each ref value is byte-exact against the spec value. The ref adds trailing inline `# comment` annotations (e.g. "lives in data", "observed associations of the Augment author", "GitHub App slug (confirm via probe)") that do NOT change any value. No value invented or altered.
- **Field invention:** No field exists in the ref that is absent from the spec block. No spec field omitted.
- **Lock state:** `locked: false` preserved (ships unlocked, as required — `detection-contract.md:24`, prose at lines 11-12 and 34-39). The T-210 lock-gate note is present (`detection-contract.md:10-12`, consequence 2 at lines 34-39), satisfying the manifest's "notes T-210 enforces the lock gate."
- **DetectionContract loader parity (`detection.py:50-58`):** The dataclass exposes all 9 fields with matching names — `augment_bot_login`, `augment_author_association`, `augment_app_slug`, `emission_shape`, `findings_locus`, `severity_field_path`, `review_completeness_signal`, `probe_evidence`, `locked`. `from_yaml` (`detection.py:61-73`) maps all 9. No schema-loader divergence from the ref.

**Verdict:** TRACED. The YAML schema traces field-by-field to §7 lines 481–492 with byte-exact values, correct field count, `locked:false`, and `<PROBE-LOCKED>` retained. No finding.

---

## Cross-cutting adversarial sweep (beyond the 4 named traces)

To satisfy the "0 findings requires exhaustive evidence" bar, I additionally probed for source-tracing violations the 4 prompts did not name:

- **NFR-6 `gh`/`git` token purity** (manifest AC for classifier.py/detection.py/models.py): grep-equivalent read of all three. `models.py` — zero `gh`/`git` tokens (confirmed; docstring `models.py:9-11` claims this and the body bears it out). `classifier.py` — zero command tokens; mentions `gh pr view --json reviews` and REST paths only in a docstring comment (`classifier.py:24-27`) describing payload SHAPE, not invoking a command. `detection.py` — zero `gh`/`git` invocation; references `scripts/poll-augment-review.sh` as the out-of-core fetch seam (`detection.py:8-9`, 110-113). No seam leakage. Consistent with §7 consequence 4 / AC-9.
- **`anthropic` import purity** (manifest AC "imports NO `anthropic`"): none of the four files import `anthropic`. Confirmed.
- **MonitorState `S4_HALT_BEFORE_PUSH` rename** (`models.py:101`): the Python identifier drops the spec's prime (`S4'_HALT_BEFORE_PUSH` → `S4_HALT_BEFORE_PUSH`). This is OUTSIDE the 4 assigned traces (§5.1, not §7/§11.3/§12.1) and is self-documented as a spec-faithful adaptation (`models.py:88-91`). Not in scope for a SOURCE-TRACING finding against the assigned spec sections; flagged here only for completeness, not as a finding.
- **`from_yaml` default for `locked`** (`detection.py:72`): `bool(data.get("locked", False))` — defaults to `False` (unlocked) when absent, which is the spec-correct fail-closed behaviour for the T-210 gate (§7 consequence 3, lines 500-503). Correct, not a finding.

---

## Findings Summary

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| IMPORTANT | 0 |
| MINOR | 0 |
| **Total** | **0** |

**Exhaustiveness evidence:** Every one of the 4 named traces was carried to byte-level value comparison with explicit spec line citations (Traces 1–4 tables). The adversarial assumption of ≥5 invented/mis-traced elements was actively pursued via: (a) full 32+1 event enumeration with bidirectional missing/invented checks; (b) literal-login leakage hunt across all four files (the lone `augment-code[bot]` literal at `detection.py:139` was run down and shown to be a polling-seam default, not a classifier match constant); (c) field-by-field YAML value-drift check including inline-comment annotations; (d) NFR-6 `gh`/`git`/`anthropic` purity sweep. No invented, untraceable, or mis-traced element was found in the assigned scope. The single benign literal and the `S4_HALT_BEFORE_PUSH` rename are documented adaptations outside the four assigned traces and do not constitute source-tracing findings.

## VERDICT: PASS
