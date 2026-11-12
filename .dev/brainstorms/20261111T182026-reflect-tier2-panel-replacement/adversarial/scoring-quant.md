# Quantitative Scoring

Folder: `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/adversarial`. Variants: V1 = `variant-1-opus-architect.md`, V2 = `variant-2-sonnet-analyzer.md`, V3 = `variant-3-haiku-backend.md`. All three variants were read in full. SR, DC, SC and the claim counts come from one script run with `uv run python -` (rules below). RC and the contradiction list are manual and cite headings and quotes.

## Results table

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC requirement_coverage | 0.30 | 1.0000 (15/15) | 1.0000 (15/15) | 1.0000 (15/15) |
| IC internal_consistency | 0.25 | 0.9955 (2 in 446) | 0.9853 (5 in 341) | 0.9948 (1 in 194) |
| SR specificity_ratio | 0.15 | 0.9991 (1066 / 1067) | 1.0000 (775 / 775) | 0.9965 (286 / 287) |
| DC dependency_completeness | 0.15 | 1.0000 (107/107) | 1.0000 (51/51) | 1.0000 (2/2) |
| SC section_coverage | 0.15 | 1.0000 (12/12) | 1.0000 (12/12) | 1.0000 (12/12) |
| **quant_score** | | **0.9987** | **0.9963** | **0.9982** |

All three variants share the same twelve H2 headings and each addresses all 15 required items, so the gaps between them are small. The only metrics that separate them are IC and SR.

## RC

Fixed list of 15 items. A variant matches an item when a section or table substantively addresses it. Cited as `Heading` for each variant.

| # | Item | V1 | V2 | V3 |
|---|---|---|---|---|
| 1 | Q1 takeover/lacks/stays | `Answers to Q1-Q7` > Q1 (table) | `Answers to Q1-Q7` > Q1 (table) | `Answers to Q1-Q7` > Q1 |
| 2 | Q2 finding format | `Answers to Q1-Q7` > Q2 and `Finding format` | same | same |
| 3 | Q3 merge/debate fate, pre and post separately | Q3 ("Pre-execution." and "Post-execution." bullets) | Q3 ("pre-execution" and "post-execution" lists) | Q3 ("For pre-execution" and "For post-execution" paragraphs) |
| 4 | Q4 engine | Q4 | Q4 | Q4 |
| 5 | Q5 pre-execution end to end | Q5 and `Adapter sketches` | Q5 and `Adapter sketches` | Q5 and `Adapter sketches` |
| 6 | Q6 rounds/ledger/revise | Q6 | Q6 | Q6 |
| 7 | Q7 cost and when a full panel is not worth calling | Q7 and `Cost model` ("When a full panel ... is not worth calling") | Q7 and `Cost model` ("When a full panel is not worth calling") | Q7 ("Do not call a full panel ...") |
| 8 | at least 3 candidate architectures including leave-as-is | `Candidate architectures` (A-E, A = leave as is) | `Candidate architectures` (A-D, A = leave as is) | `Candidate architectures` (table, 4 rows, first = leave reflect as is) |
| 9 | chosen architecture with reasons | `Chosen architecture and reasons` | same heading | same heading |
| 10 | pre and post adapter sketches | `Adapter sketches` (Pre-execution and Post-execution adapters) | same | same (Pre-execution adapter, Post-execution adapter later) |
| 11 | staged migration, pre-execution behind a flag first | `Staged migration` (Stage 2 `--t2-engine shadow`, off by default) | `Staged migration` (Stage 1 `--panel-resolve`, off by default) | `Staged migration` (Stage 2 `--review-backend shared`, off by default) |
| 12 | 1.8.0 contract mapping: merge_method, convergence score, null-score rules, gate condition 9, reflect_post, consumers | `Return-contract 1.8.0 mapping` (table, "Null-score rules", "Gate condition 9", "`reflect_post` frontmatter", "Consumer by consumer") | same heading (field table, "Null-score rules", "Promotion gate condition 9", "`reflect_post` frontmatter", "Consumers, one by one") | same heading (table, "Null-score rules", "Gate condition 9", "`reflect_post`", "Consumer-by-consumer commitment") |
| 13 | cost model | `Cost model` | `Cost model` | `Cost model` |
| 14 | main risks | `Risks` (8) | `Risks` (10) | `Risks` (9) |
| 15 | first measurement | `First measurement` | `First measurement` | `First measurement` |

Counts: V1 15/15 = 1.0, V2 15/15 = 1.0, V3 15/15 = 1.0.

## IC

**Claim counting rule (script).** Take every body line, excluding frontmatter, heading lines and the ``` fence marker lines. Split table rows on `|` into cells, and other lines into sentences on `(?<=[.;:!?])\s+`. A unit counts as a scorable claim if it has at least 20 characters and matches `\d|`|\bmust\b|\bnever\b|\balways\b|\bonly\b|\bat least\b|\bat most\b` (case-insensitive). Claim counts: V1 446, V2 341, V3 194. Each is above the 60-claim minimum.

**Contradictions.** Only pairs of passages in the same variant that cannot both hold are counted.

V1 (2):
1. Pre-execution cost range for the chosen design.
   - "**Cost:** pre about 34-66k (about 30% below A); post about the same as A." (`Candidate architectures` > C; the comparison table and Q7 also say 34-66k)
   - "| **total (default)** | | **about 35-68k** (12+16.5+4+0+2.4 ≈ 35; 20+31.5+8+0+8 ≈ 68) |" (`Cost model`)
2. Contract change under option E.
   - "**Keeps:** the 1.8.0 contract with no version change at all." (`Candidate architectures` > E)
   - "| Contract change | none | major | 1.9.0 additive, then 2.0.0 enum widening, pre only | none | 1.9.0 additive |" (`Comparison` table, last column is E)

V2 (5):
1. Net cost of the chosen design.
   - "Net about neutral, between 5k saved and 3k added (see Cost model)." (`Candidate architectures` > C)
   - "Net: 0 to -2k. The assumption on debate size is the weak point. If the debate does not shrink, the cost is +3k" (`Cost model`; the best case is 2k saved, not 5k)
2. Saving from dropping the debate (C2).
   - "| C2. C without debate | needs 1.9.0 | -8k to -15k more |" (`Comparison` table)
   - "Saving against stage 2 is 5k-4k, so small. This is why C2 is optional." (`Cost model`)
3. Stage 5 total.
   - "total 30k-63k" (`Cost model`, same sentence)
   - "39+12+6+7 = 64, rounded; treat as about 30k-64k" (same sentence; the high end is stated as 63k and then computed as 64k)
4. Post-execution debate scope.
   - "Debate on clusters whose members disagree on `deviation_class` or `blocking`, and on any single-source blocking cluster." (`Adapter sketches` > Post, step 7)
   - "Stage 4 keeps the full cluster-table debate; C2 later narrows it." (same step: a debate scoped to those clusters is not the full cluster-table debate)
5. Swarm use for pre-execution.
   - "The swarm `reflect-review` lens and `run_tier2_ensemble` serve post-execution only." (Q4, "Facts I read")
   - "`launch` null (gateway models): run a swarm worker." (Q4 rule) and "Dispatch, per reviewer by `launch`: agent session (`reflect-reviewer`) or swarm worker." (`Adapter sketches` > Pre, step 4)

V3 (1):
1. Debate-free variant cost.
   - "Planning estimate 31k–43k output tokens for a three-reviewer pass" (`Candidate architectures` table, deterministic kernel row)
   - "A hypothetical debate-free three-reviewer experiment subtracts 6–10k from the shared band, yielding **31k–46k**" (`Cost model`)

Noted, not counted:
- V3 gives 37k–53k in the candidate table and 37k–56k in `Cost model` for the shared kernel. The file explains the difference itself ("target versus allowance"), so there is no contradiction.
- V1 and V2 refer to "six recorded runs" in places and "5 recorded T2 runs" in others. The files do not show these are the same population, so a contradiction cannot be demonstrated.

IC = 1 - contradictions / claims:
- V1: 1 - 2/446 = 1 - 0.004484 = 0.995516
- V2: 1 - 5/341 = 1 - 0.014663 = 0.985337
- V3: 1 - 1/194 = 1 - 0.005155 = 0.994845

## SR

**Scope.** All lines except frontmatter and heading lines (lines starting with `#`). Fenced code lines are included.

**Concrete indicators.** One non-overlapping left-to-right scan with this alternation, first alternative wins at each position. Each match counts once.
- `` `[^`\n]+` `` (backticked name, path, field or value)
- `\b[\w./-]+\.(?:py|md|json|yaml|yml|ts|sh)(?::\d+(?:-\d+)?)?\b` (file name or file:line cite)
- `(?<![\w])\d+(?:[.,]\d+)*(?:[kKM]|%|x)?(?![\w])` (number, with k/M/%/x suffix)
- `\b(?:[A-Z]{1,4}-\d+|[KQP]\d|INV-\d+|A-\d)\b` (id codes)
- `\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b` (snake_case field name)
- `≥|≤|>=|<=` (thresholds)

**Vague indicators** (case-insensitive, counted over the same lines): `\bappropriate(?:ly)?\b`, `\bas needed\b`, `\bshould consider\b`, `\bmight\b`, `\bvarious\b`, `\betc\b\.?`, `\bbest[- ]practices?\b`.

| Variant | Concrete | Vague | Vague matches | SR = c / (c + v) |
|---|---|---|---|---|
| V1 | 1066 | 1 | `best-practice` (a proposed category value in the findings-v2 table; counted because the regex is mechanical) | 1066 / 1067 = 0.999063 |
| V2 | 775 | 0 | none | 775 / 775 = 1.000000 |
| V3 | 286 | 1 | `might` (once) | 286 / 287 = 0.996516 |

The seven-regex vague list is narrow. All three variants are close to 1.0, so SR carries little discriminating power. V3 has far fewer concrete tokens (286 against 775 and 1066), but the ratio does not reflect that.

## DC

**Reference types counted** (body lines only, headings excluded). Each is resolved against the same file.
- `Stage N` and `Stages N-M`: resolved when a table row starts with `| N.` or `| N:` (optionally bolded).
- `Q1`..`Q7`: resolved when a `### QN` heading exists.
- `K1`..`K4`: resolved when a `**KN` definition exists.
- `A-1`..`A-9` outside the Assumptions section: resolved when the id appears inside `## Assumptions and UNVERIFIED items`.
- `architecture|candidate|option X` for X in A-E, with an optional digit: resolved by a `### X.` heading or a `| X.` table row.
- `step N` and `steps N-M`: resolved when a numbered list item `N.` exists.
- `candidate|comparison|mapping table`: resolved when a heading contains that word.
- Named-section refs `<heading words> section|below|above` (candidate architectures, chosen architecture, finding format, adapter sketches, staged migration, cost model, risks, first measurement, assumptions and unverified items, summary, mapping): resolved when some heading contains the words.
- Quoted refs `see|under "X"`: resolved when a heading contains X or X contains the heading.

External references (`SKILL.md:NNN`, `§9.4`, `findings.py:NNN`, "enrichment section 4", "seed brief", `F2` or `F3` path) are excluded.

| Variant | Internal refs by type | Total | Resolved | Unresolved | DC |
|---|---|---|---|---|---|
| V1 | K 72, Stage 20, section 5, step 5, arch 2, Q 1, A 1, table 1 | 107 | 107 | none | 1.0000 |
| V2 | Stage 42, section 2, quoted 2, Q 1, A 1, arch 1, step 1, table 1 | 51 | 51 | none | 1.0000 |
| V3 | A 1, table 1 | 2 | 2 | none | 1.0000 |

V3 uses almost no labelled internal references. Its DC of 1.0 rests on 2 references, so it is a weak result.

## SC

Count of lines starting with `## `. Each variant has Summary, Candidate architectures, Chosen architecture and reasons, Answers to Q1-Q7, Finding format, Adapter sketches, Staged migration, Return-contract 1.8.0 mapping, Cost model, Risks, First measurement, and Assumptions and UNVERIFIED items.

| Variant | H2 count | SC = count / max (12) |
|---|---|---|
| V1 | 12 | 1.0000 |
| V2 | 12 | 1.0000 |
| V3 | 12 | 1.0000 |

## quant_score

quant_score = RC x 0.30 + IC x 0.25 + SR x 0.15 + DC x 0.15 + SC x 0.15

- V1: 1.0 x 0.30 + 0.995516 x 0.25 + 0.999063 x 0.15 + 1.0 x 0.15 + 1.0 x 0.15 = 0.300000 + 0.248879 + 0.149859 + 0.150000 + 0.150000 = **0.998738**
- V2: 1.0 x 0.30 + 0.985337 x 0.25 + 1.000000 x 0.15 + 1.0 x 0.15 + 1.0 x 0.15 = 0.300000 + 0.246334 + 0.150000 + 0.150000 + 0.150000 = **0.996334**
- V3: 1.0 x 0.30 + 0.994845 x 0.25 + 0.996516 x 0.15 + 1.0 x 0.15 + 1.0 x 0.15 = 0.300000 + 0.248711 + 0.149477 + 0.150000 + 0.150000 = **0.998188**

Order: V1 (0.9987) > V3 (0.9982) > V2 (0.9963). The spread is 0.0024, so the quantitative layer cannot decide between the variants and the qualitative layer must carry the ranking.

**Determinism.** SR, DC, SC and the claim counts come from fixed regexes over the three files, so re-running gives identical numbers. RC and the contradiction list are manual judgements. Their evidence is quoted above so a second reader can check each one.
