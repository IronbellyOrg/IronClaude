4e41a3a186101050b758fc1d6d23f99d39739b1c
A1 r1-1 F1.1 note src/superclaude/cli/sweep/models.py:245 ac=T168.AC1 amiss:n,false:n,harm:n,constraint:n SweepResult has an extra context field (SweepContext) beyond the design's carried header data from SweepInput; logged in Phase 8 Findings.
A1 r1-1 F1.2 note src/superclaude/cli/sweep/models.py:240 ac=T168.AC1 amiss:n,false:n,harm:n,constraint:n SweepResult.summary is a mutable dict inside a frozen dataclass; the design does not constrain its type.
