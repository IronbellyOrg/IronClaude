73e3cafd123859e9a454ed39aaeb467e00dbc7d2
## family enforce-rebuild-separator
defect form: rebuild joins units with separators taken from one side only, so a restored or kept unit next to dropped units gets the wrong break (and the tail comes only from the revised side)
command: grep -n -e "seps\[" -e "rtail" src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py
before:
498:    ru, rseps, rtail = units(rev_text)
532:    res.update(regions=regions, moved_b=moved_b, moved_r=moved_r, bu=bu, bseps=bseps, ru=ru, rseps=rseps, rtail=rtail)
786:            out += [rseps[j] + ru[j].raw for j in range(j1, j2)]
790:                out += [bseps[i] + bu[i].raw for i in range(part.i1, part.i2)]
792:                out += [rseps[j] + ru[j].raw for j in range(part.j1, part.j2)]
793:    out.append(res["rtail"])
coupled sites: the three emit sites (786 equal units, 790 reverted base units, 792 kept revised units) and the tail (793) share one separator rule; the whole-baseline fallback in enforce (restored = analyze(...)) hides any error of that rule
## family enforce-depends-closure
defect form: depends: is followed only from findings already marked bad, not from entries reverted because their hunks are unattributed
command: grep -n -e "depends" src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py
before:
207:        m = re.fullmatch(r"(finding|op|old|anchor|new|considered|depends):\s*(.*)", line)
223:        if e.depends:
224:            m = re.fullmatch(r"L([0-9]+)", e.depends)
226:                fail("INPUT", f"L{e.num} depends on an unknown entry {e.depends}")
797:def depends_closure(bad, ledger, per):
798:    """Add every finding with an entry that depends: on an entry of a reverted finding."""
804:            dep = by_num.get(int(e.depends[1:])) if e.depends else None
836:    depends_closure(bad, ledger, per)
848:        depends_closure(bad, ledger, per)
coupled sites: both callers of depends_closure (initial failing set and inside the cycle-cap loop); the parser lines 207-226 only validate depends and need no change
after: (family enforce-rebuild-separator)
after: 505:    ru, rseps, rtail = units(rev_text)
after: 539:    res.update(regions=regions, moved_b=moved_b, moved_r=moved_r, bu=bu, bseps=bseps, btail=btail, ru=ru, rseps=rseps, rtail=rtail)
after: 794:        p, own = prev[side], seps[side][x]
after: 797:        sep = seps[side][p + 1] if p is not None and p < x - 1 and "\n" not in own else own
after: 815:    out.append(res["btail"] if ends_on_base else res["rtail"])
after: (family enforce-depends-closure)
after: 207:        m = re.fullmatch(r"(finding|op|old|anchor|new|considered|depends):\s*(.*)", line)
after: 223:        if e.depends:
after: 224:            m = re.fullmatch(r"L([0-9]+)", e.depends)
after: 226:                fail("INPUT", f"L{e.num} depends on an unknown entry {e.depends}")
after: 819:def depends_closure(bad, ledger, per, stale):
after: 820:    """Add every finding with an entry that depends: on a reverted entry: one of a reverted
after: 827:            dep = by_num.get(int(e.depends[1:])) if e.depends else None
after: 860:    depends_closure(bad, ledger, per, stale)
after: 872:        depends_closure(bad, ledger, per, stale)
