"""Verify byte identity of deleted case-colliding docs against retained paths."""
import pathlib,subprocess,json,os
os.environ['GIT_OPTIONAL_LOCKS']='0'
p=pathlib.Path(__file__).resolve().parent
rev='ab0bb0f5'

def blob(spec):
    r=subprocess.run(['git','rev-parse','--verify',spec],capture_output=True,text=True)
    return r.stdout.strip() if r.returncode==0 else None

raw=subprocess.check_output(['git','diff','--name-status','--no-renames',rev+'^',rev],text=True)
rows=[]
for line in raw.splitlines():
    status,path=line.split('\t',1)
    if status!='D':continue
    parts=path.split('/'); canonical='/'.join([parts[0],parts[1].lower(),*parts[2:]])
    old=blob(rev+'^:'+path); retained=blob(rev+':'+canonical)
    rows.append(dict(deleted=path,canonical=canonical,old_blob=old,retained_blob=retained,byte_identical=old==retained,current_canonical_exists=pathlib.Path(canonical).is_file()))
assert len(rows)==43
assert all(r['old_blob'] for r in rows)
lines=['# Documentation case cleanup content verification','','Method: compare Git blob IDs at ab0bb0f5^:<deleted path> and ab0bb0f5:<lowercase directory counterpart>. No content normalization.','']
for r in rows:
    lines.append(f"{r['deleted']} -> {r['canonical']} | byte_identical={r['byte_identical']} | current_canonical_exists={r['current_canonical_exists']} | old_blob={r['old_blob']} | retained_blob={r['retained_blob']}")
lines += ['',f"Total deleted uppercase-directory paths: {len(rows)}",f"Byte-identical retained lowercase counterparts: {sum(r['byte_identical'] for r in rows)}",f"Canonical counterparts currently present: {sum(r['current_canonical_exists'] for r in rows)}"]
(p/'foundation-case-evidence.md').write_text('\n'.join(lines)+'\n')
(p/'foundation-case-evidence.json').write_text(json.dumps(rows,indent=2)+'\n')
print('\n'.join(lines))
