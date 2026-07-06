# Phase 3 — Output Inventory (classifier/detection + decline classification)

Change-set for the Phase 3 M3 lens gate. FR-9.1, T-1110/T-1111/T-1112, EC-23.

| File | V1.1 delta | FR / T-ID |
|---|---|---|
| `src/superclaude/pr_submit/classifier.py` | Added `STATE_DECLINED = "declined"`; `import re`; new pure fn `is_decline(comment, contract, *, watermark=None)`; `classify()` gained keyword-only `watermark=None` and a decline-first branch scanning Augment comments+reviews BEFORE polling/clean/findings | FR-9.1, T-1110/T-1111/T-1112, EC-23 |
| `src/superclaude/pr_submit/detection.py` | `DetectionContract` gained 3 fields: `decline_phrase_regex` (default `abnormally\s+large`), `decline_retrigger_regex` (default `comment\s+["']?(augment\|auggie\|augmentcode)\s+review["']?`), `accepted_trigger_phrases` (default `["auggie review","augment review","augmentcode review"]`, `field(default_factory=...)`); `from_yaml` reads all 3 via `data.get` | FR-9.1 (§6.2) |
| `src/superclaude/pr_submit/__init__.py` | Re-export `is_decline`, `STATE_DECLINED` (+`__all__`); STATE_POLLING/CLEAN/FINDINGS still NOT re-exported | (test convention) |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md` | Added the 3 new keys to the fenced YAML block with defaults matching detection.py exactly; **stays `locked: false`** (T-210 unaffected) | §6.2 |
| `tests/pr_submit/test_detection_contract.py` | +6 tests (T-1110, T-1110b, T-1111, T-1112, T-1112b, EC-23 watermark), `is_decline` import, `inv` marker | T-1110/T-1111/T-1112, EC-23 |
| `tests/pr_submit/fixtures/decline-comment.json` | schema (a) decline poll payload + `expected` | T-1110 |
| `tests/pr_submit/fixtures/decline-initial-poll.json` | schema (a) initial-poll decline | FR-9.1 |
| `tests/pr_submit/fixtures/stale-decline-pre-watermark.json` | schema (a) stale decline + `watermark` + `expected` | EC-23 |

**Test result:** `pytest test_detection_contract.py` = 14 passed (8 prior + 6 new).
**Canonical regex strings** (must match across detection.py / ref YAML / fixtures):
- phrase: `abnormally\s+large`
- retrigger: `comment\s+["']?(augment|auggie|augmentcode)\s+review["']?`
- accepted_trigger_phrases: `["auggie review", "augment review", "augmentcode review"]`
