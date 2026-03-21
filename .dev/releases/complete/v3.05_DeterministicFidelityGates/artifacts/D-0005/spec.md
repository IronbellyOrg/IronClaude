# D-0005: Section Splitter API

**Module**: `src/superclaude/cli/roadmap/spec_parser.py`
**Implements**: FR-5

## SpecSection Dataclass
Fields: `heading`, `heading_path`, `level`, `content`, `start_line`, `end_line`

## split_into_sections(text) -> list[SpecSection]
- Splits on `^#{1,6} ` pattern
- YAML frontmatter: level=0, heading="frontmatter"
- Preamble (pre-heading content): level=0, heading="preamble"
- heading_path: slash-joined hierarchy (e.g. "FR-1/FR-1.1/Acceptance Criteria")
- Round-trip verified: split -> reassemble matches original byte-for-byte

## Dimension-to-Section Mapping
| Dimension | Section Patterns |
|---|---|
| signatures | FR-1, FR-2, 3. Functional Requirements |
| data_models | 4.1, 4.2, 4.3, 4. File Manifest |
| gates | FR-7, FR-8, 5.1 |
| cli | 5.1, CLI, Commands |
| nfrs | 6., NFR, Non-Functional |
