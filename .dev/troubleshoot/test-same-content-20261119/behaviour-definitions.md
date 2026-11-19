# Behaviour definitions

| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | `filecmp.cmp(f1, f2, shallow=False)` (Python 3.11.15 stdlib) | returns a cached outcome keyed on (paths, file type, size, mtime) before comparing bytes | function body of `filecmp.cmp` and `filecmp._sig` in the stdlib source | the code that implements "returns a cached outcome keyed on file signature before comparing bytes" | fetched:raw-source (printed with `inspect.getsource` in the same shell; rows pasted in tier1-observation.md) |

Returned lines (verbatim):

```
s1 = _sig(os.stat(f1))
s2 = _sig(os.stat(f2))
if s1[0] != stat.S_IFREG or s2[0] != stat.S_IFREG:
    return False
if shallow and s1 == s2:
    return True
if s1[1] != s2[1]:
    return False

outcome = _cache.get((f1, f2, s1, s2))
if outcome is None:
    outcome = _do_cmp(f1, f2)
    ...
    _cache[f1, f2, s1, s2] = outcome
return outcome

def _sig(st):
    return (stat.S_IFMT(st.st_mode), st.st_size, st.st_mtime)
```
