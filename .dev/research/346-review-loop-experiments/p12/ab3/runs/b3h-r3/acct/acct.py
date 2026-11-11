import difflib, sys
before = open(sys.argv[1], encoding='utf-8').read()
after = open(sys.argv[2], encoding='utf-8').read()
sm = difflib.SequenceMatcher(None, before, after, autojunk=False)
rows = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    rows.append((tag, before[i1:i2], after[j1:j2]))
tot_add = tot_del = 0
for tag, d, a in rows:
    da, dd = len(a.encode()), len(d.encode())
    tot_add += da; tot_del += dd
    print(f"{tag:8s} del={dd:4d} add={da:4d} | del={d[:70]!r} | add={a[:70]!r}")
print("total added", tot_add, "total deleted", tot_del, "net", tot_add - tot_del)
print("size before", len(before.encode()), "after", len(after.encode()))
