"""Roll a run back to just after VF1, using the clean shadow VF1 output (runs/<run>/vf1-clean). Original kept in runs_superseded/<run>-contaminated."""
import json, shutil, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h
run = sys.argv[1]
rd = h.run_dir(run); bak = rd.parent.parent / "runs_superseded" / f"{run}-contaminated"
bak.parent.mkdir(exist_ok=True)
if not bak.exists(): shutil.copytree(rd, bak, symlinks=True)
w = h.ws(run); rev = w / h.REVIEW; hist = w / h.HIST
shutil.copy(hist / "spec-v1.md", w / h.SPEC)
for p in list(hist.glob("spec-v*.md")):
    if p.name != "spec-v1.md": p.unlink()
for name in ("revise1.md", "round2.md", "revise2.md", "round3.md", "verify-2.md", "verify-3.md", "findings-2.md", "findings-3.md", "round2.orig.md", "round3.orig.md"):
    if (rev / name).exists(): (rev / name).unlink()
for sub in ("vf2", "vf3", "aud", "aud2"):
    if (rd / sub).exists(): shutil.rmtree(rd / sub)
for p in rd.glob("PROMPT-*.md"):
    if p.stem.replace("PROMPT-", "") not in ("R1a", "R1b", "R1c", "VF1"): p.rename(p.with_name(p.name + ".superseded"))
clean = rd / "vf1-clean/ws" / h.REVIEW / "verify-1.md"
shutil.copy(clean, rd / "vf1/ws" / h.REVIEW / "verify-1.md")
st = h.load(run); keep = ["R1a", "R1b", "R1c", "VF1"]
st["done"] = keep[:]; st["prepared"] = keep[:]; st["transitioned"] = keep[:3]
st["launched"] = {k: v for k, v in st["launched"].items() if k in keep}
st["log"] = {k: v for k, v in st["log"].items() if k in keep[:3]}
st["noted_unactioned"] = []; st["loop_end"] = None; st["complete"] = False; st["final_spec"] = None
st["manual"] = [m for m in st.get("manual", []) if m["step"] in keep[:3]]; st["relaunch"] = {}; st["lost"] = False
st["replay"] = {"from": "VF1", "reason": "clean VF1 re-run changed the confirmed set (verifier list contamination)", "backup": str(bak)}
h.save(run, st)
h.ingest(run, "VF1") if hasattr(h, "ingest") else None
print("rolled back", run, "-> VF1 confirmed", h.load(run)["log"]["VF1"].get("confirmed"))
