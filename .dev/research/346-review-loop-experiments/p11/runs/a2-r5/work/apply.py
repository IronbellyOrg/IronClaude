import sys, re, difflib, json
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
before = len(s.encode())
E = []
def e(fid, old, new): E.append((fid, old, new))

e('B-1', "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`).",
 "In unattended mode the command writes `<contract-dir>/return-contract.yaml`, where `<contract-dir>` is the directory the brief passes as `--contract-dir <dir>`. When the command's `--output` / `--output-dir` is already a directory and `--contract-dir` is absent, that directory is `<contract-dir>`; for every other command (a file-valued output flag, no output flag, or a generated or fixed location) the brief must pass `--contract-dir` (B-1).")
e('B-1', "the output directory, so the report path is known before dispatch (WC-4);",
 "the contract directory (`--contract-dir`), so the report path is known before dispatch (WC-4, B-1);")
e('B-1', "\"Contract\" means the WC-4 file `<output-dir>/return-contract.yaml`.",
 "\"Contract\" means the WC-4 file `<contract-dir>/return-contract.yaml`.")
e('B-1', "the worker reports the named file until Phase 1 adds the contract.",
 "the worker reports the named file until Phase 1 adds the contract; from Phase 1 the brief also passes `--contract-dir <dir>` (WC-4, B-1).")
e('B-1', "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)",
 "Write the contract at `<contract-dir>/return-contract.yaml` (WC-4) instead of the unnamed, inconsistent path (P1, B-1)")
e('B-1', "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1)",
 "Also write the contract to `<contract-dir>` on every outcome, pre-creation STOPs included (WC-4); the package copy stays (P1, B-1)")
e('B-1', "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate);",
 "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate) and the directory-valued `--contract-dir` (B-1);")
e('B-1', "`test -s <contract>` and",
 "`test -s <contract>` (`<contract>` = `<contract-dir>/return-contract.yaml`, WC-4) and")
e('B-1', "7.2 live check on each P1 command with `--unattended --output <dir>`",
 "7.2 live check on each P1 command with `--unattended --contract-dir <dir>` (B-1)")
e('B-1', "(for example `/sc:tdd \"auth\" --unattended --output <file>` with a bare topic;",
 "(for example `/sc:tdd \"auth\" --unattended --output <file> --contract-dir <dir>` with a bare topic;")
e('B-2', "its report path is the WC-4 contract path.",
 "its report path is the WC-4 contract path. In P0, before the contract exists, the command's existing report file stands in for it: `--outcome` follows WC-5 applied to that report and the report path is that file (B-2).")
e('B-2', "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1.",
 "steps 1-3 and 5-7 pass, with the existing report file standing in for the contract in step 3 (B-2); step 4 is `test -s` on that file, since the contract arrives in P1.")

tot = {}
def toks(x): return re.findall(r'\s+|\S+', x)
for fid, old, new in E:
    assert s.count(old) == 1, (fid, old[:60], s.count(old))
    s = s.replace(old, new)
    a, b = toks(old), toks(new)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    d = i = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ('delete', 'replace'): d += len(''.join(a[i1:i2]).encode())
        if op in ('insert', 'replace'): i += len(''.join(b[j1:j2]).encode())
    t = tot.setdefault(fid, [0, 0, 0]); t[0] += i; t[1] += d; t[2] += len(new.encode()) - len(old.encode())
open(p, 'w', encoding='utf-8').write(s)
print(before, len(s.encode()), json.dumps(tot))
