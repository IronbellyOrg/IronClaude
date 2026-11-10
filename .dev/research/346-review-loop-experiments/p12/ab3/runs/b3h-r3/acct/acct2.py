import sys
sys.path.insert(0, '.')
from pairs import P
tot = {}
for fid, old, new in P:
    # trim common prefix and suffix to get the true changed region
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]: i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1-j] == new[-1-j]: j += 1
    d = old[i:len(old)-j] if j else old[i:]
    a = new[i:len(new)-j] if j else new[i:]
    add, dele = len(a.encode()), len(d.encode())
    t = tot.setdefault(fid, [0, 0, 0])
    t[0] += add; t[1] += dele; t[2] += 1
    print(fid, 'add', add, 'del', dele)
print()
for k in sorted(tot): print(k, 'edits', tot[k][2], 'added', tot[k][0], 'deleted', tot[k][1], 'net', tot[k][0]-tot[k][1])
print('ALL added', sum(v[0] for v in tot.values()), 'deleted', sum(v[1] for v in tot.values()), 'net', sum(v[0]-v[1] for v in tot.values()))
