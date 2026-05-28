# Discovery 04 — Verification Tool Choice (Bash vs Glob)

**Sources:**
- Research file 02 §11 (Sibling-Artifact Naming Recommendation: Glob vs Bash)
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` L75-L121 (independent observation)
- Global memory: `feedback_no_multiline_paste.md`

**Date:** 2026-05-27

## Chosen tool: **Bash** (with Glob as an optional pre-step)

This is a single-tool commitment — no "either/or" undecided outcome.

## Rationale tied to the 7-condition Calibration Report minimum-parse check

Per research-02 §8, the gate's verification must enforce:

1. **File exists** at `<output-dir>/tier2-<agent-name>-calibration.md` AND is non-empty.
2. **Starts with** `# Calibration Report` (first non-blank line).
3. **Contains** `## Per-dimension scores` heading.
4. **Contains** `## Confidence` heading.
5. **Contains** `## Escalation recommendation` heading.
6. **Contains** `**Verdict**:` followed by `STOP` or `ESCALATE` (case-sensitive, may be backtick-wrapped).
7. **Contains** `**Calibrated (this report)**:` followed by a parseable float in `[0.0, 1.0]`.

**Why Glob alone is insufficient:**
- Glob can enumerate `<output-dir>/tier2-*-hypothesis.md` (condition adjacent to 1, before we check siblings).
- Glob can pattern-match `<output-dir>/tier2-*-calibration.md` to list existing siblings.
- Glob CANNOT do **sibling pairing** (for each hypothesis card, derive its `-calibration.md` sibling path and verify existence) — that's a per-pair check.
- Glob CANNOT do **content parsing** — conditions 2-7 require reading file contents and matching strings.

**Why Bash is sufficient:**
- A single `for f in <output-dir>/tier2-*-hypothesis.md` loop iterates over hypothesis cards.
- Per-iteration, `sibling="${f%-hypothesis.md}-calibration.md"` derives the expected sibling path (pure string substitution — no extra tool).
- `[[ -f "$sibling" ]]` checks file existence (condition 1).
- `grep -q "^# Calibration Report" "$sibling"` checks condition 2.
- `grep -q "^## Per-dimension scores" "$sibling"` checks condition 3.
- `grep -q "^## Confidence" "$sibling"` checks condition 4.
- `grep -q "^## Escalation recommendation" "$sibling"` checks condition 5.
- `grep -qE '\*\*Verdict\*\*:\s+\`?(STOP|ESCALATE)\`?' "$sibling"` checks condition 6.
- `grep -qE '\*\*Calibrated \(this report\)\*\*:\s+0\.[0-9]+|1\.0' "$sibling"` checks condition 7.
- Emit `calibration: missing card=<path>` to audit.log on any check failure.

All seven conditions resolve in a single Bash invocation. No markdown parser, no Python helper, no auxiliary tool.

## Independent observation of existing skill patterns (L75-L121)

Verified by reading the file:

- **Wave 0 Step 4 (L107):** "create `<output-dir>/`" — implicit Bash (mkdir-style); no explicit tool named.
- **Wave 0 Step 5 (L108-L121):** "Open audit log; emit machine-readable header:" — an HTML-comment-style fenced block. The mechanism is unspecified (implicit Bash or Write append).
- **No explicit Bash filesystem-verification pattern** appears in any Wave (0, 1, 1.5, 1.7, 2 covered in L75-L121 scope).
- **Wave 1 (L140 — observed in earlier grep):** "fall back to `Glob` + `Grep` on the issue keywords" — Glob/Grep used for **search/fallback**, NOT verification gates.
- **Wave 5 (L331 — earlier observation):** `evidence-validator` agent reads-and-parses citations — this is a closer-spirit precedent to Change F's verification (read-and-parse content), and is implemented as an agent dispatch, not a single tool call.

**Conclusion:** Bash is the right choice because (a) no existing Wave uses Glob for verification gates (only for search/fallback), (b) the spec's wording ("Verification command (run before publishing)") implies a single command, which is Bash idiom, and (c) content parsing requires capabilities Glob lacks.

## Recommended verification command structure for the Phase 2 insertion

A multi-line Bash block embedded in the SKILL.md body. **Multi-line Bash is acceptable INSIDE the skill body** because:
- Claude reads the skill, not the user; the global memory `feedback_no_multiline_paste.md` is about the user's TERMINAL pasting limitations.
- The skill body IS the orchestrator's narrative — it can include illustrative multi-line code blocks that Claude executes/follows.

However, for Change F's specific insertion, a **plain-prose English instruction** referencing the verification approach is more consistent with the existing Wave 3 style (research-03 §5.2 confirms Wave 3 uses bolded paragraph headers + MUST inline imperatives + prose, NOT fenced code blocks for instructions). The exact Bash one-liner does NOT need to be transcribed verbatim into the SKILL.md — instead, the gate text should:

1. **Describe** the verification semantics in prose ("for each `tier2-*-hypothesis.md`, assert a matching `*-calibration.md` exists and contains the Calibration Report markers...").
2. **Enumerate** the 5-7 required Calibration Report markers as inline single-backtick code references.
3. **Specify** the failure-handling ladder (the 3-step retry-then-force-degrade).
4. **Leave** the literal tool implementation to the orchestrator (Bash with the structure described above is implied by the prose semantics).

This matches the existing Wave 1 and Wave 5 styles where the skill prescribes WHAT to verify but leaves WHICH tool to use to the orchestrator's judgment (consistent with the skill's allowed-tools list including both Bash and Glob).

## Confirmation

Single-tool commitment to Bash (with optional Glob pre-step for enumeration). Recommended structure is concrete enough to be transcribed into the Phase 2 insertion as prose with inline-backticked markers. Multi-line Bash in skill body is acceptable per memory clarification.
