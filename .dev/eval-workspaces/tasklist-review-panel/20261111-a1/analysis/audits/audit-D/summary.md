# Audit D: merge and ledger integrity (eval 20261111-a1)
Read-only. Scripts: /tmp/audit-D/audit.py, audit2.py, mk.py. Flags: /tmp/audit-D/flags.tsv (438 lines). Per-row EXCLUDE list: /tmp/audit-D/exclude-list.txt.
Examined: 89 rows (batch-10 i1-/i2-, contaminated, superseded, quarantine skipped) x 3 packages = 264 merged-1.md. All 264 loaded; all use ledger round 1 only.

## Counts (severity: EXCLUDE / WARN)
- C1 panel/paths: 10 EXCLUDE (catfix path 4, report missing 6), 6 WARN (panel vs files present).
- C2 block ok false: 80 EXCLUDE (reviewer-level; see cause below).
- C3 conservation: 10 EXCLUDE (>50% of reviewer's findings dropped), 78 WARN (some dropped). 49 dropped findings were BLOCKING.
- C4 blocking consistency: 0 row or verdict inconsistencies inside ledger.json / merged-1.md. 6 WARN only because the report changed after the merge (see C5).
- C5 stale: 16 EXCLUDE (n2-terra x3 pkgs t2-1+t4-1; r2-sol design t2-1+t4-2: report re-run after merge, sha256 differs from ledger report_sha256), 4 WARN stale-r1 dirs (n5-sol, n5-terra; designSpec+alias). Ledger doc sha == candidate.md sha in all 264 (0 mismatches).
- C6 model: resolution model == meta expected_model in all; 51 WARN t4-2 observed 'grok-4.7-build' vs expected 'grok-4.7' (label only). tier/alias present everywhere.
- Extra: 83 WARN megacluster rows, 45 WARN missing merge-stdout.txt.

## Main finding: block ok false is NOT the category bug any more
Cause measured by replaying findings.py parse rules (_check_finding) on every report: the merge keeps the parsable lines and drops the invalid ones.
Dropped findings by reason (all rows): anchor >200 chars 56, anchor2 >200 chars 18, claim >300 chars 14, bad severity 3, refs-bad 1. 'unpassable-ac' category: only in c2-haiku-grok/c5-glm-haiku raw .md (4 files, fixed by .catfix.md copies, see below).
By model (dropped-finding reasons): gpt-6-luna 30 (27 anchor, 2 anchor2, 1 claim); muse-ember-1.0 33 (24/7/2); muse-wonder-1.0 14 (5/8/1); glm-5.3 7 (all claim>300); claude-haiku-5-5 7 (claim 3, bad-severity 3, refs 1); grok-4.7 1 (anchor2); sonnet 0; terra 0; sol 0.
Findings kept/raw in ledger (counted over every listed report incl. stale): haiku 1085/1108, sonnet 446/446, glm 86/93, luna 356/386, sol 8/8, terra 103/103, grok 205/207, ember 834/867, wonder 275/289.
Impact: a long-anchor reviewer (luna, ember, wonder) silently loses its finding even when it is blocking. 49 blocking findings dropped in total.
VERDICT FLIPS (dropped blocking finding left the ledger with no blocking row, so merged verdict is PASS where the reviewer said FAIL): g3-sonnet-luna-ember-r3/alias t4-1 F1; g5-ember2-luna-r2/alias t4-1 F1; n5-sonnet-ember/design t4-1 F1+F2 (all anchor >200). Also total-loss merges: g1-ember-luna2-r4/alias t3-1, g7-haiku-luna2-r4/designSpec t4-1 (6/6 dropped), n4-sonnet-ember/design t4-1 (8/8), h1-haiku-luna2-ember2-r2/designSpec t4-2, h1-...-r3/designSpec t4-1.

## Other EXCLUDE causes
- n5-sol and n5-terra (3 pkgs each): merged-1.md lists t4-1, resolution.json lists t4-1, but reviews/combos/n5-sol|n5-terra has NO t4-1.md (t4-1 now only under the -superseded-20261112 dir). Merge used a report that is not in the current row dir: UNVERIFIED which version, EXCLUDE t4-1. stale-r1 dirs exist for these merges (re-merge).
- c2-haiku-grok (alias: t4-1, t4-2), c5-glm-haiku (alias+designSpec t4-1): merged-1.md cites t4-1.md.catfix.md, not the final t4-1.md (which still has 'unpassable-ac': 2 or 3 occurrences). The catfix copy differs by ~6 bytes (category rename), so content is the intended fix; flagged EXCLUDE only because path is not the final report. Lead decision: treat as OK if catfix is the accepted version.
- n2-terra (all 3 pkgs): t2-1 and t4-1 reports are newer than merged-1.md by 683-2589 s and sha differs. r2-sol/design: t2-1 (+89 s) and t4-2 (+60 s). Merge built from an older report version.
- 45 merges (c2, c5, n2-*, n4-*, r2-*, r5 rows) have no merge-stdout.txt: merge warnings for them UNVERIFIED (drop reasons were recomputed, same pattern).

## Extra checks (brainstormed)
X1 Clustering of unrelated findings: findings.py cluster() is union-find over same_defect (same section+refs fingerprint OR spans within 3 lines when refs intersect/empty), so chains grow. Replayed it: 195 of 1398 rows with >=3 members are chains where not every pair is a direct match; 144 span >60 lines of the candidate; 83 rows have >=8 members or >=4 sections (e.g. r2-sonnet-ember/designSpec L1: 19 members across 8 sections, 142/171 pairs unrelated; n2-terra/design L1: 14 members; n4-terra/design L1: 13). Row anchor/claim = first member only, so scoring a row against ground truth can match or miss the wrong defect, and one mega blocking row counts as ONE blocking row. Verdict unaffected, but row counts, overlap confidence ('overlap' set by any 2 reviewers) and per-row recall are inflated/hidden. Also g1-ember-luna2-r1/design: L1 merges t4-1 F1 (mode-label vs two-writes contradiction) with the artifacts-path findings. WARN only (83 flagged).
X2 Anchor-resolution failure: 46 rows have span null (anchor not found in candidate after flatten) and 13 of those are blocking; they are kept but cannot cluster by span, so duplicates stay separate rows. WARN, not flagged per row.
X3 One reviewer's block parsed as another's: checked (reviewer_id,fid) of every ledger member against that reviewer's own report: 0 mismatches except stale-report cases above.
X4 Round-number reuse / same-row-name overwrite: all ledgers have rounds=[1]; no listed report path points to another row dir; no identical ledger.json sha across rows; only 1 merge (n4-sonnet/alias) has merged-1.md 25 min after resolution.json (has firstmerge/ dir, reports older than merge) = OK.
X5 Blocking/verdict logic: row blocking == any member blocking, md table == ledger.json, verdict FAIL iff blocking row: 0 violations over 264 merges (apart from the dropped-finding effect above).
X6 Row blocking uses 'current' call only on re-merge; irrelevant at round 1.

## EXCLUDE list (row: reviewer[cause:pkgs]) causes B=block ok false, P=path not final/missing, S=stale after merge, C=>50% dropped, V=verdict flip; DS=designSpec AL=alias DE=design
b4-sonnet-luna2: t4-1[B:AL]
b4-terra-luna-muse: t2b-1[B:DS], t4-1[B:DE]
b4-terra-muse-haiku: t2b-1[B:AL/DE]
c2-haiku-grok: t4-1[P:AL], t4-2[P:AL]
c5-glm-haiku: t4-1[B:DS P:AL/DS]
e6-haiku-ember2: t3-1[B:DS C:DS]
g1-ember-luna2-r2: t2b-1[B:DS], t3-1[B:DE]
g1-ember-luna2-r3: t2b-1[B:DS], t3-1[B:AL]
g1-ember-luna2-r4: t3-1[B:AL C:AL], t4-1[B:DE]
g2-sonnet-ember-r3: t2b-1[B:AL]
g2-sonnet-ember-r4: t2b-1[B:DS]
g3-sonnet-luna-ember-r3: t4-1[B:AL C:AL V:AL]
g3-sonnet-luna-ember-r4: t2b-1[B:AL/DS]
g4-haiku-ember-terra-r1: t2b-1[B:AL]
g4-haiku-ember-terra-r2: t4-1[B:AL]
g5-ember2-luna-r1: t4-1[B:DE]
g5-ember2-luna-r2: t3-1[B:AL], t4-1[B:AL C:AL V:AL]
g5-ember2-luna-r4: t2b-1[B:AL/DS], t4-1[B:DE]
g6-luna2-ember2-r1: t2b-1[B:DE], t4-1[B:DE]
g6-luna2-ember2-r2: t2b-1[B:AL/DS], t4-2[B:AL]
g6-luna2-ember2-r3: t4-1[B:DE]
g7-haiku-luna2-r1: t3-1[B:AL/DE]
g7-haiku-luna2-r3: t4-1[B:DS]
g7-haiku-luna2-r4: t3-1[B:DE], t4-1[B:DS C:DS]
g8-ember-terra-r2: t2b-1[B:DS]
g8-ember-terra-r4: t2b-1[B:DS]
g9-ember-luna-r1: t4-1[B:AL]
g9-ember-luna-r2: t2b-1[B:AL], t4-1[B:DE]
h1-haiku-luna2-ember2-r1: t2b-1[B:DE], t3-1[B:DS], t4-1[B:DE]
h1-haiku-luna2-ember2-r2: t2b-1[B:AL/DS], t4-2[B:DS C:DS]
h1-haiku-luna2-ember2-r3: t2b-1[B:DS], t3-1[B:AL], t4-1[B:DS C:DS], t4-2[B:AL]
h2-sonnet-luna2-ember2-r1: t4-2[B:DE]
h2-sonnet-luna2-ember2-r2: t3-1[B:DS], t4-1[B:AL], t4-2[B:DE]
h2-sonnet-luna2-ember2-r3: t2b-1[B:DS C:DS]
h2-sonnet-luna2-ember2-r4: t2b-1[B:AL]
n2-muse-haiku-grok: t2b-1[B:AL]
n2-muse-haiku-grok-src: t4-2[B:DE]
n2-sol: t2b-1[B:AL]
n2-sonnet: t2b-1[B:AL]
n2-terra: t2-1[S:AL/DE/DS], t2b-1[B:AL], t4-1[S:AL/DE/DS]
n3-muse-luna-grok-src: t2b-1[B:AL]
n4-muse-glm-haiku: t3-1[B:AL]
n4-sol: t2b-1[B:AL], t3-1[B:DE]
n4-sonnet-ember: t4-1[B:DE C:DE]
n5-muse-luna-src: t2b-1[B:AL]
n5-sol: t3-1[B:AL/DE], t4-1[P:AL/DE/DS]
n5-sonnet-ember: t2b-1[B:DS], t4-1[B:DE C:DE V:DE]
n5-terra: t2b-1[B:AL], t4-1[P:AL/DE/DS]
r1-haiku-luna2-src: t3-1[B:DE]
r2-haiku2-grok: t4-1[B:AL]
r2-sol: t2-1[S:DE], t3-1[B:AL], t4-2[S:DE]
r2-sonnet-ember: t2b-1[B:AL]
r5-glm-haiku2: t3-1[B:AL]
terra-luna-muse-ember: t4-1[B:AL]
