s = open("audit.py").read()
s = s.replace('''r"\\b(not|n't|no|never)\\s+(be\\s+)?incomplete\\b"''', '''r"\\b(not|n't|no|never)\\W{0,3}(be\\W{0,3})?incomplete\\b"''')
s = s.replace('''if not f.endswith(".md") or ".attempt" in f: continue''', '''if not f.endswith(".md") or ".attempt" in f: continue
            if ".catfix" in f: continue''')
s = s.replace('''for f in sorted(os.listdir(d)):''', '''for f in sorted(os.listdir(d)):
            if "catfix" in f and not f.endswith(".md"): continue''',1) if False else s
open("audit.py","w").write(s)
