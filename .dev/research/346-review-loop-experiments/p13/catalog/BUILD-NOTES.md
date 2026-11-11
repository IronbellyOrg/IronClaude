# BUILD-NOTES (defect-catalog/1, built by pn3, version 1)

Method: extract.py (C9.3 parsing, mechanical) -> anchor.py (quote > first cited group > none) -> cluster.py (union-find) ->
hand adjudication (adjudication.py) -> build_catalog.py. Scripts: `$AB/offline/`. Reviewed documents: the original spec for R1 sources, the run's final spec for audits.

## Counts
- Sources: 36 (15 first reviews: 12 primary + 3 arm-1 sensitivity; 15 first audits; 6 second audits). Blocking findings extracted: 81. All 24 rows of the C9.3 expected-theme table (12 runs x R1 and first audit) reproduce exactly.
- Anchored by quote: 71; by cited line: 10; none: 0. Revision-introduced (set by adjudication, quote in the final spec and not in the original): 2. Unanchored: 0.
- Clusters: mechanical 17 -> adjudicated 22. Overrides: 22 (splits, merges, multi-membership moves, revision-introduced).
- Memberships after adjudication: 88 (a finding that names two wrong outcomes is a member of both; 8 findings are, listed in `overrides` with action move).
- Confirmed clusters (>= 2 distinct sources): 12 of 22.

## Deviations and judgement calls (read before using the catalog)
1. Arm-1 reports are formatted differently from C9.3 expects: a1-r2 and a1-r3 list their findings as table rows and give no machine-readable id line, so their blocking ids are set by an explicit override (a1-r2: F1..F7; a1-r3: 1..14), and find_section got a bracket-id and a start-line extension, used only for arm 1.
2. The mechanical anchor takes the FIRST quote that locates in the original (literal to the plan). That is often a generic phrase (for example `--unattended` or `## Unattended mode`), which is why the mechanical clusters M1 and M2 pool 30+ findings each; adjudication splits them.
3. Cluster anchors are one quote per cluster chosen by hand and asserted to locate exactly once in the original; they are not the members' own spans.
4. Two audit findings (a3-r6/AUD F-01, a3-r6/AUD2 B2) rest on text the revisions added and are listed under revision_introduced, not clustered.
5. Adjudication was done by one reader (the implementer) in one pass; there is no second independent adjudicator.
6. No `unanchored` findings. The 36-source universe includes arm-1 first reviews (a different instrument, original briefs that called every finding blocking), so the arm-1-only clusters inflate S_ref relative to what the 12 primary occasions could find.

## Re-check of a 20% random sample of memberships (random.Random(0), 18 of 88)
Each sampled (finding, cluster) pair was re-read a second time against the finding's heading and body. Result: 18/18 agree; one is borderline (a3-r2/AUD2 B-1 -> D12: the finding is mainly a command-count mismatch, load is one of its two causes).
Sample: D10<-a1-r3/R1:3, D12<-a1-r3/R1:1, D1<-a2-r2/R1:B2, D3<-a2-r4/AUD:F-1, D12<-a3-r2/AUD2:B-1, D12<-a2-r3/AUD:REQ-1, D11<-a1-r3/R1:11, D4<-a1-r1/R1:F-04, D12<-a3-r6/R1:REQ-2, D8<-a1-r1/R1:F-08, D19<-a2-r1/R1:B-1, D3<-a1-r3/R1:2, D12<-a3-r2/AUD:F-02, D1<-a3-r3/AUD2:B2, D3<-a3-r1/AUD2:F2, D1<-a2-r4/AUD:F-2, D19<-a2-r2/AUD:F-02, D3<-a2-r3/AUD:REQ-2.
