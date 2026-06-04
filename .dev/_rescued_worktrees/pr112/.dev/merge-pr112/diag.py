import re, pathlib, importlib.util, sys, tempfile, os, subprocess

fx = pathlib.Path("tests/roadmap/fixtures/recurrence/id_containment/milestone_id_case.md").read_text()
m = re.search(r'^## spec\b(.*?)^## ', fx, re.S | re.M)
spec_txt = m.group(1)

def load(blob, name):
    d = tempfile.mkdtemp()
    p = os.path.join(d, name + ".py")
    open(p, "w").write(blob)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def stage(ref):
    return subprocess.check_output(["git", "show", ff"{n}:src/superclaude/cli/roadmap/spec_parser.py"], text=True)

resolved = open("src/superclaude/cli/roadmap/spec_parser.py").read()
cases = [("OURS", stage("HEAD")), ("THEIRS", stage("origin/master")), ("RESOLVED", resolved)]
for label, blob in cases:
    try:
        mod = load(blob, "sp_" + label.lower())
        ids = mod.extract_requirement_ids(spec_txt)
        print(f"{label:10} d_ids={list(ids.get('D', []))}  md_ids={list(ids.get('MD', []))}")
    except Exception as e:
        print(f"{label:10} ERROR: {type(e).__name__}: {e}")
print("EXPECTED   d_ids=[]  md_ids=['M1-D01','M1-D02','M2-D01','M2-D02','M3-D01']")
