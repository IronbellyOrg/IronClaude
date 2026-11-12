de3e1017f3520a2e09a01240b6e43423dcdd693a
## family missing-claim-text
defect form: a sheet row is written although a finding has no converted claim text (a placeholder stands in for the claim).
command: grep -nE 'no claim text|claim' scripts/reflect_cluster_pairs.py
before:
26:Row text: claim_a and claim_b are the converted claims; a finding whose card gives no claim text the converter reads
27:(for example a markdown table without a claim column) gets "(no claim text after conversion; read finding <id> in
88:    "claim_a",
93:    "claim_b",
158:                claim = f.get("claim") or (
159:                    f"(no claim text after conversion; read finding {f.get('id')} "
162:                by_key.setdefault((card.stem, f.get("id")), {**f, "claim": claim})
188:                        "claim_a": a["claim"],
193:                        "claim_b": b["claim"],
coupled sites: the candidate-pool builder, the sheet header (shortfall/comment lines), the generated-sheet test at tests/review/test_reflect_cluster_pairs.py:443 and the docstring sentences about claims.

after:
26:No claim text: a finding whose card gives no claim text the converter reads (for example a markdown table without a
27:claim column; a claim that is missing or only whitespace) stays in the clustering, but every pair it is
28:part of is left out of the candidate pool, so no row carries a placeholder claim. The header line "no claim text:"
32:Row text: claim_a and claim_b are the converted claims. citations_a and citations_b list each citation as
44:claim text, candidate and sampled counts by file relation, status, label vocabulary), then one CSV header row and the data rows; the column
92:    "claim_a",
97:    "claim_b",
131:def _has_claim(finding: dict) -> bool:
132:    claim = finding.get("claim")
133:    return isinstance(claim, str) and bool(claim.strip())
137:    """Every drawable pair (see "Pair", "Verdict" and "No claim text"), the runs that could not be read and the
138:    number of pairs left out because a finding has no claim text."""
147:    no_claim = 0
185:                if not (_has_claim(a) and _has_claim(b)):
186:                    no_claim += 1
198:                        "claim_a": a["claim"],
203:                        "claim_b": b["claim"],
207:    return pairs, problems, no_claim
215:    pairs: list[dict], seed: int = SEED, no_claim: int = 0
217:    """The sampled rows (numbered, sorted) and the counts the sheet header states; no_claim is the third value
236:        "no_claim": no_claim,
287:        f"no claim text: {stats['no_claim']} pairs left out (a finding has no claim text after conversion)",
426:        pairs, problems, no_claim = candidates(root)
427:        rows, stats = select(pairs, no_claim=no_claim)
