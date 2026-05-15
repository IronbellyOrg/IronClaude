# S5 Adversarial Debate — Severity Reclassification

**Reviewer role:** adversarial (S5 candidate solution).
**Subject:** `solutions/S5-severity-reclassification.md` proposing demotion of
`nfrs.security_missing` and `nfrs.threshold_contradicted` (no-match arm) from
HIGH to MEDIUM, with co-occurrence-based escalation.

Code evidence anchors (verified this turn, not from memory):

- `src/superclaude/cli/roadmap/structural_checkers.py:42-67` — `SEVERITY_RULES`
  table. Current entries:
  `("nfrs","threshold_contradicted"): "HIGH"`,
  `("nfrs","security_missing"): "HIGH"`.
- `src/superclaude/cli/roadmap/structural_checkers.py:518-655` — `check_nfrs`.
- `src/superclaude/cli/roadmap/structural_checkers.py:159-161` — `_section_text`
  concatenates section content; **heading_path of the originating section is
  discarded before regex scanning.**
- `src/superclaude/cli/roadmap/spec_parser.py:74-81` — `SpecSection` *does*
  carry `heading_path`, but check_nfrs runs regex over the joined blob, so each
  match has no link back to a section.
- `src/superclaude/cli/roadmap/gates.py:193` — `_high_severity_count_zero`
  gate. Convergence is HIGH-driven; MEDIUM is rendered/counted but not
  blocking.

---

## Round 1 — Attack on the original proposal

### Attack A — "Reclassification hides real defects"

If `task-builder-merge` is, in fact, a spec that wants encryption-at-rest and
the roadmap silently omits it, demoting the finding to MEDIUM lets a real
security gap slip past the convergence gate. The original S5 wording
("Not every spec NFR primitive needs to materialise as a roadmap row")
is a value judgement, not a checker fact, and the checker has no signal to
distinguish "spec mentions `auth` in a sentence about pytest fixtures" from
"spec has an entire `## Security NFRs / Encryption Requirements` section."
Blanket demotion treats both the same way.

**Defender counter:** the *current* failure mode is also wrong — every spec
that mentions the word `encryption` anywhere in an NFR-tagged section produces
a HIGH unless the roadmap echoes the exact word. That is keyword bingo, not
fidelity. The defect is checker over-eagerness, not roadmap negligence. The
verdict (sustained): blanket demotion is the wrong fix, but so is the
status quo. We need a **context-aware** rule.

### Attack B — "Co-occurrence in same heading_path"

The original S5 says findings stay MEDIUM unless they co-occur with ≥1 HIGH
in the same `heading_path`. **Code evidence falsifies this as written.**
`_section_text` (lines 159-161) joins every NFR-tagged section's content
into one string before any regex runs. The regex match (lines 579-584)
produces a `term` only — there is no carrier for `heading_path` on the way
back out. To make co-occurrence work, `check_nfrs` would need to be
restructured to iterate per-section, preserve the section reference on each
match, and join by `heading_path`. That is non-trivial and not scoped in S5's
"~50 LOC, 1 h" estimate.

**Verdict:** the original mechanism is structurally impossible without a
parser-level refactor. Either expand scope honestly or pick a different
context signal.

### Attack C — "Will MEDIUM findings still appear or get suppressed?"

`spec-fidelity.md` frontmatter carries `medium_severity_count` and the gate
in `gates.py:193` only checks HIGH, so MEDIUM findings are **rendered and
counted but not blocking**. So demotion does not suppress; it just unblocks
the gate. That is a real benefit — the user still sees the finding under
"Soft Deviations" or similar. **Status:** original S5 is correct on this
point.

### Attack D — "If a real spec marks encryption P0, demotion is dangerous"

Confirmed. A hard-coded `SEVERITY_RECLASS` dict is a one-way ratchet — every
spec, regardless of how it phrases its security requirements, gets the same
treatment. The correct shape is **a configuration surface**: either a
per-release YAML allowlist that *specific* NFR primitives can be exempt
in a specific spec context, OR a context-aware rule in the checker that
inspects the section the term came from.

---

## Round 2 — Refactor direction

Three combined refactor moves are defensible:

1. **Context-aware severity, not blanket demotion.** Inside `check_nfrs`,
   iterate `spec_sections` individually (not the joined blob). For each
   match, record the originating `SpecSection.heading_path`. If the path
   contains a strong-signal token (`security`, `critical`, `must`,
   `p0`, `requirement`, `nfr-`), keep HIGH. Otherwise emit MEDIUM. This
   uses information that already exists in the parser output (line 81)
   and adds about 30 LOC, not 50.

2. **YAML-driven per-release allowlist.** Read
   `<output_dir>/roadmap/fidelity-allowlist.yaml` (optional). Entries name
   `(dimension, mismatch_type, location_pattern)` triples and a justification
   string. Allowlisted findings are demoted to LOW and tagged
   `deviation_class: PRE_APPROVED` (an existing value in
   `models.py:18`). This gives the human an escape hatch without the
   checker silently lying.

3. **Keep the registry honest.** `SEVERITY_RULES` continues to mark
   `security_missing` and `threshold_contradicted` as HIGH at the
   *definition* layer. Demotion happens only in the per-finding emission
   path, where the section context is available. Static reads of
   `SEVERITY_RULES` (tests, audits) still see the strict baseline.

This combination addresses Attack A (keeps real security gaps HIGH when the
spec frames them as security), Attack B (uses an actually-preserved field),
Attack C (MEDIUM still surfaces), Attack D (allowlist is per-release, not
baked into code).

---

## Confidence on refactored S5

- **Standalone:** ~70 %. Even with context-awareness, the heading-token
  heuristic is fuzzy; some specs use weird headings. The YAML allowlist
  is a safety net, but if no allowlist file exists the heuristic carries
  the load.

- **Combined with S1 (sanitize-file-path) and S6 (skip-unfixable):** ~88 %.
  The combination drops the `src/x.py:88\`` HIGH, drops well-typed unfixable
  HIGHs, and demotes the 4 NFR softs. That leaves at most the 5 legitimate
  `file_missing` HIGHs, which are the real problem the roadmap pipeline
  exists to surface and should be fixed by editing the roadmap, not the
  checker.

**Recommendation:** rewrite S5 to context-aware demotion + YAML allowlist,
keep SEVERITY_RULES baseline HIGH, scope the per-section refactor honestly
(~1.5 h, not 1 h).
