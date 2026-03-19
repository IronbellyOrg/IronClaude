# Reflect: Prompt 4 -- Eval Validation Gate

**Date**: 2026-03-19
**Prompt under review**: `prompt-4-eval-validation.md`
**Role**: Validation gate / immune system of the 6-prompt eval suite

---

## Three Proposed Improvements

### Improvement 1: Add a TIMEOUT / MINIMUM EXECUTION DURATION criterion to CRITICAL criteria

**What**: Add a 5th CRITICAL criterion requiring that the eval's wall-clock execution time exceeds a minimum threshold (e.g., 60 seconds) and that Claude API call logs show at least N distinct completions. This catches "warm-cache evals" and "checkpoint evals" (identified in the Known Escape Hatches section) where execution technically happens but is trivially fast because nothing meaningful is being processed.

**Why**: The current criteria check for real execution (criterion 1) and real artifacts (criterion 2), but neither catches the case where `superclaude roadmap run` is invoked with a trivial 2-line spec that completes in 3 seconds and produces technically-valid but empty-content artifacts. A duration floor + API call count floor closes this gap.

### Improvement 2: Add ARTIFACT CONTENT VALIDATION to criterion 2 (REAL ARTIFACTS)

**What**: Extend criterion 2 from checking file existence to requiring minimum content thresholds: each artifact must contain at least N non-empty lines (e.g., extraction.md >= 20 lines, roadmap.md >= 50 lines, debate-transcript.md >= 30 lines), must not be identical across runs, and must contain domain-specific keywords proving they were generated from the input spec (not from a template). Add a check: `diff artifact_v3 artifact_master` must show non-trivial differences.

**Why**: The current criterion 2 only checks that files "exist" on disk. A file containing a single line `# extraction` or a boilerplate template passes criterion 2 today. This is the "Potemkin pipeline" escape hatch explicitly called out in the Critical Lessons section but not actually blocked by any criterion. The prompt identifies the threat but doesn't defend against it.

### Improvement 3: Make criterion 6 (NO MOCKS) a CRITICAL criterion instead of REQUIRED

**What**: Promote criterion 6 from REQUIRED to CRITICAL, so that any mock/stub/fake usage in eval scripts is an immediate BLOCKER, not a "fix before proceeding" item.

**Why**: The entire reason this prompt exists is the rejected 168-pytest-unit-test approach, which was fundamentally a mocking problem. If mocks are detected, the eval is structurally identical to the rejected approach. Allowing it as merely REQUIRED (fixable without re-running Prompt 3) understates the severity -- mocks in eval scripts mean the eval is not an eval at all.

---

## Adversarial Debate

### Improvement 1: TIMEOUT / MINIMUM EXECUTION DURATION

**Advocate**: This directly addresses two of the five named escape hatches (warm-cache evals and Potemkin pipelines with trivial specs). The current criteria have a blind spot: criterion 1 checks that the pipeline is invoked, criterion 2 checks artifacts exist, but neither checks that the pipeline did substantial work. A 3-second run that produces skeleton files passes both. Duration + API call count is a cheap, objective signal that real work happened.

**Critic**: Duration thresholds are fragile and environment-dependent. A fast machine with cached models might legitimately complete faster. More importantly, this conflates "how long" with "how good" -- a slow, broken pipeline also takes time. The real problem (trivial specs producing empty artifacts) is better solved by content validation (Improvement 2) which checks output quality directly rather than using duration as a proxy. Adding a duration criterion also creates a maintenance burden: every time the pipeline gets faster through optimization, the threshold needs updating. This is a proxy metric when a direct metric exists.

**Verdict**: **SKIP**. The Critic is right -- duration is a proxy for content quality, and Improvement 2 addresses the same escape hatches more directly and robustly. Duration thresholds would also create false failures as the pipeline matures and gets faster.

---

### Improvement 2: ARTIFACT CONTENT VALIDATION

**Advocate**: This is the single highest-impact change possible. The prompt's own Critical Lessons section identifies "Potemkin pipelines" as a known escape hatch, yet criterion 2 only checks file existence -- it literally does not defend against the threat it names. Adding minimum line counts, domain-keyword checks, and cross-run diff requirements closes the gap between "files exist" and "files contain real pipeline output." This transforms criterion 2 from a filesystem check into a content integrity check. Without this, an eval could `touch` all the required filenames and pass every CRITICAL criterion.

**Critic**: Minimum line counts are arbitrary and could become stale as the pipeline evolves. What's the right minimum for extraction.md -- 20 lines? 50? If the pipeline legitimately produces a 15-line extraction for a simple spec, we'd get a false FAIL. Domain-keyword checks add complexity and couple the validation prompt to specific pipeline output formats, making it brittle. The existing criterion 4 (ARTIFACT PROVENANCE) with timestamp checks already provides some defense -- files must post-date eval start. Combined with criterion 1 (real execution verified by grepping for subprocess calls), the Potemkin risk is already substantially mitigated.

**Advocate (rebuttal)**: The Critic's concern about arbitrary thresholds is valid but easily addressed: instead of hard line-count minimums, require that artifacts are "non-trivially populated" -- specifically, that each artifact exceeds 10 non-empty lines and contains at least one section heading (`##`) and one substantive paragraph. This is format-stable across pipeline evolution. The Critic's claim that criteria 1+4 mitigate Potemkin risk is wrong: criterion 1 checks that subprocess calls exist in code (static analysis), not that they produced meaningful output. Criterion 4 checks timestamps, not content. An empty file created by a real subprocess call at the right time passes both. Content validation is the missing layer.

**Verdict**: **APPLY**. The Advocate's rebuttal is decisive. The prompt explicitly names Potemkin pipelines as a threat but has no content-level defense. The refined version (non-trivially populated with section headings + substantive paragraphs, not hard line counts) avoids the brittleness concern while closing the most dangerous gap in the validation gate.

---

### Improvement 3: Promote NO MOCKS to CRITICAL

**Advocate**: The origin story of this entire prompt is a rejected eval that was 168 mocked tests. Mocks in eval scripts are the original sin. Making NO MOCKS merely REQUIRED sends the wrong signal -- it says "you can have mocks, just fix them before moving on, no need to re-run anything." That's too lenient for the exact failure pattern this prompt was designed to catch. Promoting to CRITICAL ensures mocks are treated with the same severity as fake execution or missing artifacts.

**Critic**: Criterion 6 is already quite strict -- it greps for a comprehensive list of mock-related tokens and fails on any hit. The difference between CRITICAL and REQUIRED is procedural, not substantive: CRITICAL means "re-run P4 after fixing," REQUIRED means "fix before proceeding to P5." In practice, both block forward progress until resolved. The separation exists so that truly structural failures (criteria 1-4) trigger a full re-validation loop, while surface-level issues (a stray `mock` import left in a utility) get fixed inline. Promoting criterion 6 means a single `from unittest.mock import Mock` comment in a helper file triggers a full re-validation cycle, which is disproportionate overhead for a low-risk issue.

**Verdict**: **SKIP**. The Critic makes a valid procedural distinction. The current REQUIRED classification already blocks forward progress. The severity difference (re-run P4 vs. fix-and-continue) is appropriate: a stray mock import is less structurally dangerous than "no real execution at all." The existing classification is correct.

---

## Final Decision

**Winner: Improvement 2 -- ARTIFACT CONTENT VALIDATION**

**Impact-to-risk ratio**: Highest of the three. It closes the most explicitly-identified threat (Potemkin pipelines) with a targeted, non-brittle addition to an existing criterion. Risk is low because the addition uses format-stable checks (non-empty lines, section headings, substantive content) rather than brittle line-count thresholds.

**Implementation**: Extend criterion 2 (REAL ARTIFACTS) to require content validation beyond file existence. Each artifact must contain non-trivial content: more than 10 non-empty lines, at least one markdown section heading, and content that references the input spec's domain terms. Additionally, artifacts from v3.0 and master runs must not be byte-identical (which would indicate template/copy artifacts).
