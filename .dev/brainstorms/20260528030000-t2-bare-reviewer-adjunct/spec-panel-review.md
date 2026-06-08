# Spec Panel Review — T2 Bare-Reviewer Adjunct

```yaml
specification_review:
  original_spec: /config/workspace/IronClaude/.dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md
  spec_version: 1.0.0-draft
  review_date: 2026-05-28T03:24:00Z
  mode: critique
  format: standard
  focus_areas: [all]                          # default — no --focus flag passed
  auto_suggested_focus: correctness            # 5+ numeric guards + pipeline ops + mutable state triggers suggestion
  iterations: 1
  expert_panel:
    - Karl Wiegers
    - Gojko Adzic
    - Alistair Cockburn
    - Martin Fowler
    - Michael Nygard
    - James Whittaker
    - Sam Newman
    - Gregor Hohpe
    - Lisa Crispin
    - Janet Gregory
    - Kelsey Hightower
  input_classification: design-spec            # not TDD, not PRD
  mandatory_artifacts_produced:
    - guard_condition_boundary_table           # advisory (correctness focus not active, but auto-suggested)
    - pipeline_flow_diagram                     # advisory

quality_assessment:
  overall_score: 7.4
  per_dimension:
    clarity: 8.0                # well-structured, glossary present, terminology consistent
    completeness: 7.5           # most paths specified; observability + idempotency gaps
    testability: 6.5            # 35 ACs but several are qualitative ("verified via task notification timestamps")
    consistency: 8.5            # internal cross-references hold; ID schemes consistent
    correctness: 6.5            # several guard conditions have unspecified boundary behavior
    architectural_soundness: 7.5 # clean separation of skill + adversarial extension + caller plumbing
    operational_readiness: 5.5  # no observability, no deployment model, secret-handling thin
    adversarial_robustness: 6.0 # several Whittaker attack surfaces unaddressed
```

---

## Critical Issues (severity-ordered)

```yaml
critical_issues:
  - id: CI-01
    category: correctness
    severity: CRITICAL
    expert: Whittaker
    issue: |
      The "substantively overlaps (≥60% token overlap)" rule for Corroboration is the load-bearing
      hallucination defense — but two bare reviewers from related-training-distribution models
      (e.g., two MoE models trained on similar synthetic data) can hallucinate the SAME wrong claim
      with high token overlap, achieving false Corroboration without independent grounding.
    recommendation: |
      Corroboration must require either (a) at least one of the corroborating sources be NON-suspect
      (i.e., T1 / Anthropic-model), OR (b) the corroborating SUSPECT sources cite the same verifiable
      file:line (then it's effectively Validated, not Corroborated). Pure-bare-on-bare corroboration
      is insufficient. Update §5.4 algorithm step 2 and §11.3 mitigation.
    priority: High
    quality_impact: 9/10

  - id: CI-02
    category: correctness
    severity: CRITICAL
    expert: Nygard
    issue: |
      §5.4 step 1 ("Validated") uses cite.line ± 5 to verify a claim. This is brittle: an attacker
      (or hallucinator) can name a file:line where coincidental text supports a wrong claim, especially
      in long files. There's no semantic-similarity check between claim_text and the cited region.
    recommendation: |
      Strengthen to require semantic match between claim_text and the cited region (≥40% token overlap
      on substantive terms), OR escalate to Whittaker-style adversarial probe before promoting to
      Validated. Currently a hallucinator that lands ANY syntactically-plausible cite gets the trust badge.
    priority: High
    quality_impact: 9/10

  - id: CI-03
    category: requirements
    severity: MAJOR
    expert: Wiegers
    issue: |
      AC-1.5 "All N reviewers dispatched in a single message (true parallel; verified via task
      notification timestamps)" — the verification mechanism is qualitative. What's the threshold?
      Two dispatches within 100ms? 500ms? What if proxy throttling serializes them server-side?
    recommendation: |
      Specify: "All N tool calls issued in a single Claude message block (structurally verifiable by
      pre-call assertion) — proxy-side serialization is acceptable and out of scope." Drop the
      timestamp-based assertion entirely; assert the message structure instead.
    priority: High
    quality_impact: 7/10

  - id: CI-04
    category: correctness
    severity: MAJOR
    expert: Whittaker
    issue: |
      Zero/Empty attack: target file is empty (0 bytes) or contains only whitespace. Spec does not
      define bare-reviewer behavior. Proxy gets a prompt with empty target — model may emit garbage
      or refusal, parse step may fail or succeed with empty findings table.
    recommendation: |
      Add Wave B guard: "If target content is <50 non-whitespace bytes after truncation, STOP with
      'Target too small for review (<50 bytes). sc-bare-review skipped.'" Or define explicit
      empty-target behavior (e.g., emit a stub report with verdict 'target empty, no review possible').
    priority: High
    quality_impact: 7/10

  - id: CI-05
    category: architecture
    severity: MAJOR
    expert: Fowler
    issue: |
      sc-bare-review skill conflates three concerns: env-var resolution + parallel HTTP dispatch +
      template normalization. The template normalizer in particular (Wave D) is non-trivial — it has
      to parse arbitrary model output and fit it into the compressed-markdown template. This is its
      own component with its own failure modes.
    recommendation: |
      Either: (a) split into sc-bare-review-orchestrator + sc-bare-review-normalizer sub-skills, or
      (b) explicitly scope the normalizer to "lossy best-effort, raw kept on parse_error" and
      document the parse heuristics in a separate refs/template-normalization.md. Currently the
      Wave D pseudo-code hand-waves a hard problem.
    priority: Medium
    quality_impact: 7/10

  - id: CI-06
    category: reliability
    severity: MAJOR
    expert: Nygard
    issue: |
      §8 failure-modes table has no entry for "/sc:adversarial skill itself fails or returns invalid
      contract after suspect tagging." sc-bare-review succeeded, but the downstream merge failed.
      What does the caller do — discard the bare files? Retry? Surface to user?
    recommendation: |
      Add failure-mode row: "Adversarial skill fails after bare-review success → bare-review artifacts
      preserved; caller surfaces /sc:adversarial failure to user; recommended-next-command in
      return-contract preserved for manual retry." Also: bare-review files should have idempotent
      filenames so a retry doesn't double-write.
    priority: High
    quality_impact: 8/10

  - id: CI-07
    category: testing
    severity: MAJOR
    expert: Crispin
    issue: |
      35 ACs but no test plan. AC-2.5 ("Round 2.5 runs new suspect_source_validation category") —
      how do you test that without an end-to-end run of /sc:adversarial? AC-2.7 ("Verdict taxonomy
      applied") — what fixture demonstrates Demoted vs Dropped distinction? §9.4 AC-4.4 mentions
      a "failure-mode test matrix" without enumerating it.
    recommendation: |
      Add §16 Test Plan with: unit fixtures (one per validator verdict), integration scenario
      (full pipeline with seeded suspect file containing 1 of each verdict-triggering claim shape),
      regression suite (each failure mode in §8 reproduced). At minimum, enumerate test cases
      under AC-4.4.
    priority: High
    quality_impact: 8/10

  - id: CI-08
    category: integration
    severity: MAJOR
    expert: Hohpe
    issue: |
      Atomicity of file-based handoff is not specified. If sc-bare-review's curl times out mid-write,
      a partial .md file may exist. /sc:adversarial then reads a corrupted file. No atomic-write
      pattern (write-to-tmp, fsync, rename) is mandated.
    recommendation: |
      Require Wave D step: "Write each output file via write-to-tmp + rename pattern. Partial writes
      MUST NOT leave a corrupt .md visible to downstream consumers." Add Wave A guard:
      "If output dir contains stale .tmp files from prior run, clean before proceeding."
    priority: Medium
    quality_impact: 6/10

  - id: CI-09
    category: requirements
    severity: MAJOR
    expert: Adzic
    issue: |
      Verdict taxonomy (Validated / Corroborated / Demoted / Dropped / Contradicted) lacks worked
      examples. §13 has 3 demo scenarios but none walk through a single suspect claim from
      bare-output → diff-analysis → Round 2.5 → Step 5.5 → annotation. The "happy path" through the
      validator is the most important thing to make concrete.
    recommendation: |
      Add §13.4: walk a single concrete claim ("color regex over-matches inside URLs") through every
      pipeline stage with state snapshots at each step. Include the resulting annotation comment,
      audit-table row, and merged-output excerpt.
    priority: High
    quality_impact: 7/10

  - id: CI-10
    category: operational
    severity: MAJOR
    expert: Hightower
    issue: |
      No observability requirements. Spec mentions "cost telemetry" in §15 but doesn't define what
      gets logged, where, or at what granularity. Per-call latency, token cost, vendor error rates,
      validator verdict distributions — all visible only post-hoc by reading output files.
    recommendation: |
      Add §17 Observability: minimum log lines per invocation (start, per-reviewer-complete with
      elapsed_ms + token_count, end with status + cost-estimate). Define a JSON log line schema.
      Telemetry block already exists in return-contract — formalize it.
    priority: Medium
    quality_impact: 6/10

  - id: CI-11
    category: architecture
    severity: MAJOR
    expert: Newman
    issue: |
      schema_version is declared (template = 1.0, return-contract = 1.0) but no upgrade/migration
      protocol. When schema_version bumps to 2.0, do old consumers fail loudly, fail-soft, or
      ignore? /sc:adversarial reading a v2 bare-review file is unspecified.
    recommendation: |
      Add §18 Versioning policy: "Major bump → consumers MUST validate version and STOP if newer
      than supported. Minor bump → additive only, old consumers ignore new fields. Patch bump →
      bug-fix only, no schema change." Document the validation pattern in sc-bare-review and
      sc:adversarial both.
    priority: Medium
    quality_impact: 5/10

  - id: CI-12
    category: correctness
    severity: MAJOR
    expert: Whittaker
    issue: |
      Sentinel collision: a target file that itself contains `suspect: true` in its frontmatter
      (e.g., reviewing a prior bare-review output, or a test fixture that happens to have that
      flag). Does sc-bare-review treat this as input to be reviewed, or does the propagated
      suspect tag interact with downstream /sc:adversarial logic?
    recommendation: |
      Wave B step: "Strip the input target's frontmatter before passing to the reviewer prompt;
      only the generated review's frontmatter carries suspect: true." Explicitly disallow recursive
      review (a bare-review file as target) via a frontmatter-tier check.
    priority: Medium
    quality_impact: 5/10

  - id: CI-13
    category: requirements
    severity: MINOR
    expert: Cockburn
    issue: |
      No use case form. The spec describes the pipeline but doesn't enumerate "Primary actor:
      caller command. Goal: incorporate diverse-model edge-case findings into a merged review
      without trusting them unverified. Main success scenario: 1. ... 2. ... Extensions: 2a. ..."
      Hard to spot a missing alternate flow without this shape.
    recommendation: |
      Add §3.5 "Use Case View" with primary scenario + extensions (proxy down, partial success,
      validator drops all suspect findings, schema-version mismatch, etc.).
    priority: Low
    quality_impact: 4/10

  - id: CI-14
    category: correctness
    severity: MINOR
    expert: Whittaker
    issue: |
      Accumulation attack: with 4 reviewers × 20 findings each = 80 suspect claims. Suspect-source-audit
      table is then 80+ rows. Validator must Read up to 80 cites, possibly across many files. No
      cap, no batching, no streaming. Worst case latency unbounded.
    recommendation: |
      Add §11.7: cap suspect-claim count per invocation (default 100). Beyond cap, validator
      processes by severity-priority and drops lowest-severity claims with annotation. Document
      worst-case latency budget.
    priority: Low
    quality_impact: 4/10

  - id: CI-15
    category: testing
    severity: MINOR
    expert: Gregory
    issue: |
      No "three amigos" view — product, dev, ops perspectives all collapsed into the spec author's.
      Specifically: no acceptance from a CR-receiving reviewer (the human consumer of merged output)
      that the annotation density is readable, not overwhelming.
    recommendation: |
      Add §19 User-Acceptance Criteria: "A human reviewer presented with the merged output (with
      annotations) reports the suspect-tagging is informative-not-noisy within X minutes of reading"
      — even if heuristic, makes the audience explicit.
    priority: Low
    quality_impact: 3/10
```

---

## Per-Expert Critique (sequenced)

### === REQUIREMENTS ANALYSIS ===

**Karl Wiegers**: "You have 35 ACs which is impressive volume, but volume is not testability. AC-1.5 in particular hand-waves verification — 'true parallel; verified via task notification timestamps' is a hope, not an assertion. AC-3.6 references `SC_DEFAULT_BARE_REVIEWERS` but doesn't define interaction with `--bare-reviewers 0` (explicit zero override). What if SC_DEFAULT_BARE_REVIEWERS=3 but the caller passes `--bare-reviewers 0`? Does the explicit flag win? My read: it must. Make it explicit. Also, AC-2.12 ('STOPs cleanly when 100% of `--compare` files are in `--suspect-source`') needs an error message specified verbatim — 'cleanly' is not testable."

**Gojko Adzic**: "Where are the Given/When/Then scenarios? §13 has three demos but they're command lines, not behavior specifications. Walk me through 'Given a target file containing 50 unique edge-case-rich functions, When 4 bare reviewers run with default temperature, Then the merged output incorporates between N and M validator-Approved findings.' I want measurable expectations, not narrative. Also: §5.4 step 2 ('≥60% token-overlap') needs a worked example. Show me two claims that overlap 65% and two that overlap 55% — and the validator's behavior on each."

**Alistair Cockburn**: "Who is the actor here? The spec doesn't say. Is the primary actor the caller command (/sc:troubleshoot, /sc:reflect)? Is it the human reviewer who consumes the merged output? Is it the SRE setting up the T2 proxy? Each has different goals, different failure tolerances. The spec implicitly serves all three but addresses none explicitly. Goal hierarchy is also unclear: is the strategic goal 'capture diverse-model signal' or 'avoid hallucination contamination'? These are in tension; the spec resolves them via tagging-and-gating, but doesn't say which is the dominant constraint when they conflict."

### === ARCHITECTURE ANALYSIS ===

**Martin Fowler**: "Three concerns are mashed into one skill. Env-var resolution is configuration. Parallel HTTP dispatch is transport. Template normalization is parsing. Each has independent failure modes, independent test surfaces, independent optimization opportunities. I'd split — at minimum logically (refs/ subdivisions), preferably structurally (sub-skill or library). The Wave D template normalizer in particular is hand-waved; in practice it'll be 200+ lines of regex + heuristics + fallbacks, and it deserves its own design discussion. Also: the `--label` flag is out-of-band — it's a passthrough for caller context but it's listed as a peer to `--reviewers` and `--target`. Group it under a `--metadata` namespace or accept that the API surface has a slight smell."

**Michael Nygard**: "Failure modes table in §8 is good but incomplete. The big missing one: /sc:adversarial fails AFTER bare-review succeeds. Now you have N artifacts on disk, a return-contract that says success, and no downstream merge. What's the caller's contract here? Surface to user? Auto-retry? Cache for next invocation? Pick one. Second: proxy circuit breaker. You have a single retry on 5xx — but if I'm running sc-bare-review 50 times an hour and the proxy is degraded, every call burns 4 reviewers × 2 attempts. Add a per-process backoff state (in-memory ok for v1; persistent ledger for v2). Third: timeout is a per-reviewer guard but no overall budget cap. Worst case: 4 reviewers, each just under 180s timeout = 180s wall clock if truly parallel, but adversarial then runs for another 60-120s. Caller's overall latency commitment to user?"

**James Whittaker** *(adversarial-focused, expanded since this spec is correctness-heavy)*:

```yaml
adversarial_analysis:
  - finding_id: ADV-01
    attack_methodology: Zero/Empty Attack
    severity: MAJOR
    invariant_location: "§3.3 Wave B — target ingestion"
    triggering_condition: "Target file is empty or contains only whitespace"
    state_trace: |
      Step 1: Read empty target.
      Step 2: target_line_count == 0; --target-line-cap not exceeded.
      Step 3: SHA-256 hash computed on empty content (deterministic value).
      Step 4: Wave C dispatches N curl calls with prompt containing empty <<<TARGET>>> block.
      Step 5: Proxy model behavior undefined — may emit refusal, empty findings, or garbage.
      Step 6: Wave D parser must handle all three cases. Spec defines none.
    remediation: |
      Add Wave B guard: "If non-whitespace content < 50 bytes after truncation, STOP with
      target-too-small error before any reviewer dispatch."

  - finding_id: ADV-02
    attack_methodology: Sentinel Collision Attack
    severity: MAJOR
    invariant_location: "§5.2 — Suspect frontmatter check"
    triggering_condition: "Target file is itself a prior bare-review output with suspect:true frontmatter"
    state_trace: |
      Step 1: User runs /sc:reflect --bare-reviewers 3 on /tmp/prior-bare-review.md.
      Step 2: sc-bare-review reads target. Frontmatter contains suspect:true.
      Step 3: Prompt sent to proxy includes target frontmatter verbatim.
      Step 4: Model may interpret the suspect:true tag as authoritative ("this is a suspect doc")
              and refuse, OR mirror the structure ("output also suspect").
      Step 5: Downstream /sc:adversarial receives N suspect-tagged reviews of a suspect-tagged target.
              Validator's Corroborated rule requires at least one non-suspect — but the target is suspect.
    remediation: |
      Wave B step: strip frontmatter from target before embedding in prompt; pass content body only.
      AND: caller-side check — if target itself has suspect:true frontmatter, WARN and require
      --force-recursive-suspect flag to proceed.

  - finding_id: ADV-03
    attack_methodology: Divergence Attack
    severity: MAJOR
    invariant_location: "§5.4 step 2 — Corroboration rule"
    triggering_condition: "Exactly 2 SUSPECT reviewers agree on a claim that contradicts the lone non-suspect variant"
    state_trace: |
      Step 1: 3-way compare: 1 non-suspect (V1), 2 suspect bare reviews (B1, B2).
      Step 2: V1 says "the regex is correct."
      Step 3: B1 and B2 both hallucinate "the regex matches digits anywhere in the line"
              (which is false — it requires preceding pipe).
      Step 4: B1 cites "engine.go:42" (a real line, but unrelated text).
      Step 5: Validator runs Validated check on B1's cite — Read engine.go:42 ± 5,
              finds plausible-looking regex syntax, votes Validated.
      Step 6: B2 has no cite. Corroboration check: B2's claim overlaps B1's at >60%.
              Validator votes Corroborated. (Despite V1 contradicting.)
      Step 7: The wrong claim incorporated into merged output with two trust badges.
    remediation: |
      Algorithm fix: when a suspect claim has at least one non-suspect Contradicting source
      in the corpus, the Contradicted verdict takes precedence over Validated/Corroborated.
      Currently §5.4's algorithm doesn't sequence the checks; it should run Contradicted FIRST.

  - finding_id: ADV-04
    attack_methodology: Sequence Attack
    severity: MAJOR
    invariant_location: "§3.3 Wave A → Wave E pipeline"
    triggering_condition: "Target file is mutated between Wave B (Read) and consumer Read"
    state_trace: |
      Step 1: Wave B reads target, computes SHA-256.
      Step 2: Wave C dispatches reviewers (180s timeout each).
      Step 3: During the 180s window, user edits target file on disk.
      Step 4: Reviewers' findings reference the original content.
      Step 5: /sc:adversarial later Reads target for Validation cites — gets new content.
      Step 6: Validator sees citations to "old" content; verifies against "new" content; mismatch
              triggers Demoted on findings that were correct against the original.
    remediation: |
      Wave A step: Read target ONCE; cache content for entire pipeline lifetime; pass content
      (not path) to downstream /sc:adversarial. Adversarial's Validation step uses cached content,
      not re-Reads from disk. Document this as the canonical "snapshot-at-invocation" semantics.

  - finding_id: ADV-05
    attack_methodology: Accumulation Attack
    severity: MINOR
    invariant_location: "§5.4 — Evidence validator"
    triggering_condition: "4 reviewers × 20 findings each → 80 suspect claims, ~80 file Reads needed for Validated check"
    state_trace: |
      Step 1: All 4 reviewers complete (success path).
      Step 2: Diff-analysis tags 80 SUSPECT claims.
      Step 3: Round 2.5 runs suspect_source_validation against 80 entries.
      Step 4: Step 5.5 Read-verifiable check runs up to 80 file Reads.
      Step 5: Even at 100ms per Read, that's 8s of pure I/O on top of model latency.
      Step 6: For large targets, Read window (±5 lines) may need to expand for semantic check —
              compounding latency.
    remediation: |
      Cap suspect_claim count per invocation (default 100). Beyond cap: severity-priority order,
      lowest dropped first with annotation. Batch file Reads (group claims by file, Read each
      file once with widest needed window).
```

### === RELIABILITY & SERVICES ANALYSIS ===

**Sam Newman**: "Versioning is half-done. You have schema_version: 1.0 on the template and contract_version: 1.0 on the return-contract — but no upgrade protocol. When the template adds a column or splits Sev into Sev + Likelihood (semver MINOR? or MAJOR?), what's the consumer behavior? You also have cross-skill version dependency: sc:adversarial protocol must be ≥1.0.0 (mentioned in §10) but no fail-fast version-check on invocation. Add a Wave 0 prerequisite: sc-bare-review reads the protocol version of sc:adversarial-protocol and STOPs if incompatible. Otherwise you'll have a future where a sc-bare-review skill produces a v2 schema that a v1 sc:adversarial silently drops half of."

**Gregor Hohpe**: "This IS an integration spec — file-based handoff is your message queue, frontmatter is your envelope, the `--suspect-source` flag list is your routing key. From that lens, three issues: (1) Atomicity is unspecified — write-to-tmp + rename pattern not mandated, so a timed-out reviewer can leave a partial file that consumers must defend against. (2) Idempotency — re-running sc-bare-review on the same target overwrites silently. Some workflows would prefer append-with-suffix; spec is silent. (3) Delivery guarantee — if Wave D normalization fails after the .raw file is written, what happens? The .raw is preserved but the consumer expects .md. Either auto-promote .raw to .md with a parse_error frontmatter flag, OR delete .raw. Pick one."

### === QUALITY & TESTING ANALYSIS ===

**Lisa Crispin**: "Where's the test plan? 35 ACs are functional assertions but they're not test cases. AC-2.5 ('Round 2.5 invariant probe runs new suspect_source_validation category') — how do I write a test for that? I need a fixture (a specific suspect claim of a specific shape), an expected probe output (specific INV-NNN finding with specific category), and a pass/fail criterion. Same for every AC in §9.2. I'd ask for a §16 Test Plan with at least: one unit fixture per verdict (Validated / Corroborated / Demoted / Dropped / Contradicted), one integration fixture per failure mode in §8, one boundary fixture for each numeric threshold (M=1, M=2, N=2, N=4, overlap=59%, overlap=60%, overlap=61%). About 25-30 fixtures minimum. Also: AC-1.5's 'true parallel' assertion is qualitatively verified; replace with a structural assertion ('the dispatch occurs in a single Claude message block') which IS testable."

**Janet Gregory**: "Who participated in this spec? Reading it, I see: the spec author, the user (3 confirmed answers), and implicit reference to the prior experiment. I don't see: a SRE who'll run the proxy in production, a CR-receiving human reviewer who'll consume the merged output, a security review of the API-key handling. Three amigos failure. Specifically: the human reviewer perspective is missing — how do they tell at a glance whether a finding came from T1 vs T2-Validated vs T2-Corroborated vs T2-Unvalidated-appendix? The provenance comments are HTML comments (`<!-- -->`) — invisible in rendered markdown. Is that intentional? If yes, document why. If no, propose a visible severity-like tag."

### === OPERATIONAL ANALYSIS ===

**Kelsey Hightower**: "Where does the T2 proxy live? Spec says 'OpenAI-compatible proxy / LiteLLM-style router' but no deployment story. On the user's laptop? In the cloud? Per-team? Per-organization? Cost-attribution and secret-rotation answers diverge across these. The env-var model is fine for single-user laptops; it's painful in shared CI (env var leakage in logs) and untenable in regulated environments. Add §17 Deployment Model with at least three documented topologies. Second: observability is absent. No log schema, no metrics, no traces. The telemetry block in the return-contract is a start but it lives in each return contract file — there's no aggregation, no dashboard, no alerting. Even just 'emit a single JSON line per invocation to stderr with {ts, target_checksum, reviewers_succeeded, total_elapsed_ms, validator_verdict_counts}' would be a meaningful step. Third: cost. §11.1 mentions cost but doesn't budget it. Per-invocation cost ceiling? Daily ceiling per user? Hard limit beyond which the skill refuses?"

---

## Mandatory Output Artifacts (advisory — `--focus correctness` not active but auto-suggested)

### Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| `T2ProxyUrl exists` | §3.3 Wave A step 5 | Zero/Empty | `""` or unset | unset | STOP with named-var message | OK |
| `T2ProxyUrl exists` | §3.3 Wave A step 5 | Sentinel collision | `"http://localhost"` (no /v1 suffix) | passes presence check | Behavior unspecified | **GAP** |
| `--reviewers N` | §3.3 Wave A step 4 | Zero/Empty | `0` | rejected | Implicit STOP (range [2,4]) | OK |
| `--reviewers N` | §3.3 Wave A step 4 | One/Minimal | `1` | rejected | Implicit STOP | OK |
| `--reviewers N` | §3.3 Wave A step 4 | Typical | `3` | accepted | Proceed | OK |
| `--reviewers N` | §3.3 Wave A step 4 | Maximum | `4` | accepted | Proceed | OK |
| `--reviewers N` | §3.3 Wave A step 4 | Overflow | `5` | rejected | Implicit STOP | OK |
| `--reviewers N` | §3.3 Wave A step 4 | Negative | `-1` | rejected (range check) | Implicit STOP | OK |
| `M (succeeded count)` | §3.3 Wave E | Zero/Empty | `0` | maps to failed | Skill returns failed | OK |
| `M (succeeded count)` | §3.3 Wave E | One/Minimal | `1` | maps to failed | Caller must NOT proceed | OK |
| `M (succeeded count)` | §3.3 Wave E | Boundary | `2` (==N==2 minimum) | maps to success or partial? | Behavior unspecified | **GAP** |
| `M (succeeded count)` | §3.3 Wave E | Typical | `3` (==N==4) | partial | Proceed with caveat | OK |
| `M (succeeded count)` | §3.3 Wave E | Maximum | `N` | success | Proceed | OK |
| `token overlap ≥60%` | §5.4 step 2 | Boundary minus | `59.9%` | not Corroborated | Demoted or Dropped | OK |
| `token overlap ≥60%` | §5.4 step 2 | Boundary | `60.0%` exactly | Corroborated? | Behavior unspecified (≥ vs >) | **GAP** |
| `token overlap ≥60%` | §5.4 step 2 | Boundary plus | `60.1%` | Corroborated | Incorporate | OK |
| `target line count` | §3.3 Wave B | Zero/Empty | `0` lines | passes truncation | No empty-target guard | **GAP** (per ADV-01) |
| `target line count` | §3.3 Wave B | Boundary | `target-line-cap` | no truncation | Proceed | OK |
| `target line count` | §3.3 Wave B | Maximum | `target-line-cap + 1` | truncated, frontmatter flagged | Proceed with truncated:true | OK |
| `convergence ≥ 0.65 (PASS)` | §5.7 (existing /sc:adversarial logic) | Boundary | exactly `0.65` | PASS | Treated as PASS (≥) | OK |
| `convergence ≥ 0.65 (PASS)` | §5.7 | Boundary plus suspect HIGH demoted | `0.64 with 3 demoted HIGH-SUSPECT` | PARTIAL or PASS? | Spec says demoted doesn't block — promote to PASS? | **GAP** |

**Gap Findings** (FR-8: any GAP automatically = MAJOR severity minimum):

1. **GAP-1**: T2ProxyUrl presence check passes any non-empty string, including malformed URLs. Behavior unspecified when proxy URL is structurally invalid. **Severity MAJOR.**
2. **GAP-2**: M==N==2 boundary — is this `success` (M==N) or `partial` (M==minimum)? §3.3 Wave E status determination says `M==N → success`, so 2/2 is success — but that conflicts with the partial-fallback rationale (2 succeeded out of 2 requested is the same outcome shape as 2/4). Clarify whether `success` requires N>2. **Severity MAJOR.**
3. **GAP-3**: `≥60%` vs `>60%` token overlap. Spec writes "≥60%" — boundary inclusive — but no test fixture validates the boundary. **Severity MAJOR.**
4. **GAP-4** (cross-references ADV-01): target line count == 0 has no guard. **Severity MAJOR.**
5. **GAP-5**: convergence at exactly 0.64 with HIGH-severity SUSPECT-Demoted items — does the demote rule promote convergence to PASS, or does it remain PARTIAL? Existing /sc:adversarial convergence logic doesn't yet know about SUSPECT-Demoted exemptions. **Severity MAJOR.**

### Pipeline Flow Diagram (advisory)

```text
[Caller invocation: target file + --bare-reviewers N]
                    │
                    ▼
[sc-bare-review Wave A: env var resolution]
   N (requested) ──────▶ assert N ∈ [2,4] AND N ≤ count(configured T2ModelNN)
                    │
                    ▼
[sc-bare-review Wave B: target ingestion]
   target ─────────────▶ Read once; SHA-256; truncate if > line-cap
                    │
                    ▼
[sc-bare-review Wave C: parallel dispatch]
   N curl calls ───────▶ proxy
   timeouts independent
                    │
                    ▼
[sc-bare-review Wave D: post-process]
   N .raw files ──────▶ M .md files where M ≤ N (some may parse_error or proxy_error)
                                                          ◀── COUNT DIVERGENCE
                    │
                    ▼
[sc-bare-review Wave E: return contract]
   M files ───────────▶ status = success (M==N) | partial (2≤M<N) | failed (M<2)
                    │
                    ▼
[Caller invokes /sc:adversarial --compare X,bare1..bareM --suspect-source bare1..bareM]
                    │
                    ▼
[adversarial Step 1: diff-analysis]
   M bare files + non-suspect files ▶ K diff points, of which K_suspect tagged SUSPECT
                                                          ◀── COUNT FAN-OUT (K can be 5-30× M)
                    │
                    ▼
[adversarial Step 2: debate + Round 2.5 invariant probe]
   K diff points ─────▶ Each suspect probed by suspect_source_validation
                    │
                    ▼
[adversarial Step 5.5: evidence-validator]
   K_suspect claims ──▶ V verdicts where V == K_suspect
   Per verdict: file Read (Validated path) OR corpus search (Corroborated path)
                                                          ◀── I/O cost ~K_suspect
                    │
                    ▼
[adversarial Step 5: merge]
   Verdicts:
     Validated/Corroborated ──▶ primary body with provenance comment
     Demoted ─────────────────▶ appendix (if policy=annotate) or dropped (if policy=drop)
     Dropped ─────────────────▶ audit only
     Contradicted ────────────▶ audit only
   Merged output count ≤ K (≤ K_suspect Validated/Corroborated + non-suspect findings)
```

**Diagram Findings**:

- DIA-1: Count divergence at Wave D (N → M) and Step 1 (M → K) is acknowledged in spec but no monitoring/alerting on the magnitude. If 4 reviewers each emit 50 findings, K_suspect = 200; downstream cost should be flagged in return-contract telemetry.
- DIA-2: Step 5.5 I/O cost scales linearly with K_suspect — uncapped per ADV-05. Add a cap.

---

## Expert Consensus

```yaml
expert_consensus:
  agreements:
    - "The architectural shape (skill + adversarial extension + caller plumbing) is sound and decomposed appropriately"
    - "The suspect-by-construction frontmatter discipline is the right default"
    - "Validation gate placement inside /sc:adversarial (rather than as a separate validator) is correct — reuses existing evidence-validator infrastructure"
    - "Disabled-by-default (opt-in per call) is the right operational posture"
    - "Cost/latency tradeoffs are honestly stated; not hidden"

  disagreements:
    - subject: "Corroboration sufficiency"
      whittaker_position: "Corroboration must require ≥1 non-suspect source"
      adzic_position: "Corroboration as defined is workable IF the worked example shows it doesn't elevate false claims"
      resolution_path: "Adopt Whittaker's stricter rule; provide Adzic's worked example showing it doesn't over-suppress legitimate findings"
    - subject: "Template normalization scope"
      fowler_position: "Should be a separate sub-skill"
      hohpe_position: "Co-located is fine if the parse heuristics are documented externally"
      resolution_path: "Keep co-located in sc-bare-review for v1; produce refs/template-normalization.md documenting heuristics + escape hatch (raw file preserved on parse_error)"
    - subject: "Observability scope for Phase 1"
      hightower_position: "Minimum JSON-log line per invocation needed before v1"
      crispin_position: "OK to defer to Phase 4 IF test plan exercises the same observation points"
      resolution_path: "Compromise — emit return-contract telemetry block as the canonical observability artifact in Phase 1; structured logging deferred to Phase 4 but test plan asserts the telemetry block is fully populated"

  non_consensus_critical:
    - "Whittaker's CI-01 / ADV-03 finding on Corroboration false-positives is unanimous (Nygard, Adzic, Crispin concurring) — spec MUST be amended before Phase 1 implementation begins"
```

---

## Improvement Roadmap

```yaml
improvement_roadmap:
  immediate:                    # before Phase 1 implementation begins
    - id: IMM-1
      action: "Amend §5.4 Corroboration rule per CI-01: require ≥1 non-suspect source OR cite-shared SUSPECTs"
      experts: [Whittaker, Nygard, Adzic, Crispin]
      blocks_phase: 1
    - id: IMM-2
      action: "Amend §5.4 Validated rule per CI-02: add semantic-match check (≥40% token overlap on substantive terms)"
      experts: [Nygard, Whittaker]
      blocks_phase: 1
    - id: IMM-3
      action: "Fix AC-1.5 per CI-03: replace 'task notification timestamps' assertion with 'single Claude message block' assertion"
      experts: [Wiegers]
      blocks_phase: 1
    - id: IMM-4
      action: "Add Wave B empty-target guard per CI-04 / ADV-01: STOP if <50 non-whitespace bytes"
      experts: [Whittaker]
      blocks_phase: 1
    - id: IMM-5
      action: "Resolve Guard Gap-2: clarify whether M==N==2 is success or partial"
      experts: [Wiegers, Nygard]
      blocks_phase: 1
    - id: IMM-6
      action: "Add adversarial failure-mode entry per CI-06: bare-review succeeds but /sc:adversarial fails"
      experts: [Nygard]
      blocks_phase: 2

  short_term:                   # during Phase 1-2 implementation
    - id: ST-1
      action: "Add §16 Test Plan per CI-07 with unit fixtures per verdict + boundary fixtures for every numeric threshold"
      experts: [Crispin, Gregory]
    - id: ST-2
      action: "Add §13.4 walked-claim demo per CI-09 — single claim through every pipeline stage with state snapshots"
      experts: [Adzic]
    - id: ST-3
      action: "Mandate atomic-write pattern per CI-08 (write-to-tmp + rename)"
      experts: [Hohpe]
    - id: ST-4
      action: "Add Contradicted-first ordering to §5.4 algorithm per ADV-03"
      experts: [Whittaker]
    - id: ST-5
      action: "Snapshot-at-invocation semantics per ADV-04: target content cached, not re-Read"
      experts: [Whittaker, Hohpe]
    - id: ST-6
      action: "Sentinel collision guard per ADV-02 / CI-12: strip target frontmatter; reject recursive bare-on-bare without flag"
      experts: [Whittaker]
    - id: ST-7
      action: "Schema versioning policy per CI-11: document MAJOR/MINOR/PATCH semantics for template + return-contract"
      experts: [Newman]

  long_term:                    # Phase 3+
    - id: LT-1
      action: "Add §17 Observability + §17 Deployment Model per CI-10"
      experts: [Hightower]
    - id: LT-2
      action: "Cap K_suspect per invocation (default 100) per CI-14 / ADV-05"
      experts: [Whittaker]
    - id: LT-3
      action: "Add §3.5 Use Case View per CI-13"
      experts: [Cockburn]
    - id: LT-4
      action: "Add §19 User-Acceptance Criteria per CI-15"
      experts: [Gregory]
    - id: LT-5
      action: "Three-amigos validation: SRE perspective on proxy ops, CR-receiving reviewer perspective on annotation density"
      experts: [Gregory, Hightower]
```

---

## Summary

The spec is **structurally sound, ready for adversarial debate but not yet ready for Phase 1 implementation**. Six issues block implementation start (the IMM-1 through IMM-6 list above). Most others are real but addressable during/after implementation.

**The single most important fix**: CI-01 / ADV-03 — Corroboration must require at least one non-suspect source. Without this, two related-distribution models can hallucinate the same claim and both validation gates wave it through. This is the empirical risk the user explicitly flagged ("hallucinations must undergo rigorous validation") and the current spec under-protects against it.

**Net readiness signal**: 7.4/10. With the six IMM items fixed, would jump to ~8.7/10 — Phase 1 implementation green-light. Long-term items (LT-1 through LT-5) bring it to production-grade ~9.3/10.

*Review produced by /sc:spec-panel — 11-expert panel, critique mode, single iteration, standard format. Correctness focus auto-suggested but not activated; guard table + pipeline diagram included advisorily.*
