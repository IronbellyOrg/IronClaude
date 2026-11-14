b3bad51ece7137be7a6bbfd0ee7c21cd2bf669a1
A1 r1-1 F1.2 note src/superclaude/cli/sweep/probes.py:679 ac=scope amiss:n,false:n,harm:n,constraint:n last_record_ts is None when the last complete record has no timestamp, matching SP-15 "when that record carries one, else the file mtime"; classify falls back to mtime.
A1 r1-1 F1.4 note src/superclaude/cli/sweep/probes.py:1109 ac=scope amiss:n,false:n,harm:n,constraint:n declaration order differs from the DESIGN 7.1 listing; no functional effect.
A1 r1-1 F1.5 note src/superclaude/cli/sweep/probes.py:264 ac=scope amiss:n,false:n,harm:n,constraint:n OrcaResult.data for ok holds the envelope result object (run-current: the Run id), recorded in Phase 8 Findings; tests from the design text must match it.
