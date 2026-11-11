# Gate 5 anti-omission fix log, cycle 2

**Status:** Complete
**Date:** 2026-11-08

---

Input: `qa/qa-anti-omission-consolidated-findings-cycle2.md` (BLOCKING_COUNT 3, rows 1 to 3; Notes section MINOR, not acted on). Only the report and this log were edited. Evidence re-read first: report l.867, 1526, 1542, 121, 406, 681, 910; `research/web-01-claude-code-user-skills-hooks-and-live-reload.md` l.125-163; `ui.js` l.795-875 (partial-seed branch 807-837, default branch 838-861).

## Row 1 - Section 8 step 5.3 case (d) (report l.1542): FIXED

- Cause confirmed: step 3.2 condition 3 (report l.1465) counts `bmad-*` entries other than `bmad-os-*`, so the `bmad-os-x` fixture is a first use and the install runs, which changes P.
- Edit: "(c), (d), (e) leave P byte-identical" became "(c), (e) and the `bmad-x` fixture of (d) leave P byte-identical"; added that the `bmad-os-x` fixture is a first use, asserts the creation as in (a) with the user's `bmad-os-x` entry preserved, not byte-identical, and that under the stricter glob (Section 9 row 20) P stays byte-identical. "Byte-identical" remains only for the cases where it holds. Other "byte-identical" hits (l.613, 1556, 1559, 1572) concern other cases and were left unchanged.

## Row 2 - `--output-folder` "every command" wording (l.406, 681, 910): FIXED

- l.406 (Section 2.5): now "must stay in every first-use command that passes `--user-name`; the flagless `--yes` alternative passes none of the four core flags and needs no `--output-folder` (step 3.1, Section 9 row 20)".
- l.681 (Section 4.2, SC-04): same qualification.
- l.910 (Section 5.2): same qualification.
- Grep for "every command" / "every first-use command" afterwards: l.121, 406, 568, 681, 910, 1438 all qualified; no unqualified wording left. l.68, 192, 1056 only quote the manual command and make no rule.

## Row 3 - Section 5.1 W01-18 (l.867) and step 4D.4 (l.1526): FIXED

- Cause confirmed: web-01:127 quote is about `-p` runs; web-01:155 says `-p` already treats the folder as trusted. The earlier conclusion "the hold-back does not gate it" was an unlabelled inference.
- l.867: replaced with what web-01 states (doc-only, UNVERIFIED - doc-only), the `-p` limit, UNVERIFIED for a user-level stub, and the further step labelled `[synthesis inference: ...]` and UNVERIFIED - doc-only. The "source disagrees with itself" claim was reworded to what web-01 actually shows.
- l.1526 (step 4D.4): same treatment; the sentence "so 'no hook option escapes the hold-back' would be wrong" was removed in favour of the labelled inference.
- Other mentions (l.864, 985, 1713) say skills are not gated by workspace trust per web-01:157 and were left unchanged.

## Counts

- Fixes applied: 3
- Rows not fixed: 0
- 3 + 0 = BLOCKING_COUNT 3. Q1 and Q2 remain unanswered; no owner decision invented; existing `[synthesis inference: ...]` labels kept.
