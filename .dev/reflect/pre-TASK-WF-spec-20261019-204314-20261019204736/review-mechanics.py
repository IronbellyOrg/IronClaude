"""Read-only input accounting; writes review artifacts only beside this script."""
import hashlib, json, os, re
from pathlib import Path
ROOT = Path('/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP')
OUT = Path(__file__).parent
SPEC = ROOT / '.dev/tasks/to-do/TASK-WF-spec-20261019-204314/source.md'
PLAN = SPEC.with_name('TASK-WF-spec-20261019-204314.md')
def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot():
    paths = {SPEC, PLAN}
    unresolved = []
    for token in sorted(set(re.findall(r'(?:src/|tests/|docs/|\./)[A-Za-z0-9_./-]+\.[A-Za-z0-9]+|\bREADME\.md', PLAN.read_text()))):
        p = (PLAN.parent / token if token.startswith('./') else ROOT / token).resolve()
        if p.is_file():
            paths.add(p)
        else:
            unresolved.append(token)
    rows = [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)} for p in sorted(paths)]
    tree = hashlib.sha256(json.dumps([(r['path'], r['sha256']) for r in rows], separators=(',', ':')).encode()).hexdigest()
    return {'input_tree_sha256': tree, 'file_list': rows, 'file_count': len(rows), 'unresolved_proposed_or_artifact_paths': unresolved, 'serialization': 'JSON pairs, separators comma/colon, UTF-8'}
if not (OUT / 'artifacts/input-snapshot.yaml').exists() or '--rebuild-coverage' in os.sys.argv:
    if not (OUT / 'artifacts/input-snapshot.yaml').exists():
        save('artifacts/input-snapshot.yaml', snapshot())
        save('artifacts/environment.json', {k: os.environ.get(k) for k in ['ANTHROPIC_DEFAULT_OPUS_MODEL','ANTHROPIC_DEFAULT_SONNET_MODEL','ANTHROPIC_DEFAULT_HAIKU_MODEL','EXECUTOR_MODEL_CLASS']})
    spec = SPEC.read_text()
    plan = PLAN.read_text()
    tasks = [(m.group(1), m.group(2)) for m in re.finditer(r'^## Task (\d+):([^\n]*\n.*?)(?=^## Task |^## Phase |\Z)', plan, re.M | re.S)]
    stopwords = set('a an the and or but if then than of to in on at by for from with without as is are was were be been being do does did not no must shall should can may will would it its this that these those only also any each all both before after using use into rather through same new existing'.split())
    def words(text):
        return set(re.findall(r'[a-z0-9]+', text.casefold())) - stopwords
    lines = spec.splitlines()
    # Normative sections only; factual baseline is contextual, not additional requirements.
    selected = [12,14,20,22,52,54,55,56,57,58,59,60,61,63,67,76,78,80,82,86,90,91,92,93,94,95,96,98,102,106,108,109,110,111,112,113,114,115,117,123,124,125,126,127,128,129,130,132,136,*range(138,150),151,155]
    rows = []
    for ln in selected:
        text = lines[ln-1]
        boundaries = [0] + [m.end() for m in re.finditer(r'[.!?](?:\*\*)?\s+(?=[A-Z`])', text)] + [len(text)]
        for start in range(0, len(boundaries)-1, 2):
            quote = text[boundaries[start]:boundaries[min(start+2, len(boundaries)-1)]].strip()
            w = words(quote)
            scores = [(len(w & words(body))/len(w) if w else 0, tid) for tid, body in tasks]
            ratio, tid = max(scores, key=lambda x: (x[0], -int(x[1])))
            rows.append({'requirement_id': f'INF-{len(rows)+1:03d}', 'source': 'inferred', 'quote': quote, 'citation': f'{SPEC}:{ln}', 'matched_task_ids': [f'Task {tid}'] if ratio >= .6 else [], 'match_method': 'containment' if ratio >= .6 else 'none', 'containment_ratio': round(ratio, 6)})
    parsed = re.findall(r'\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b', spec)
    assert not parsed, parsed
    summary = {'parsed_total': 0, 'inferred_total': len(rows), 'task_count': len(tasks), 'coverage_pct': None, 'coverage_pct_union': round(sum(bool(r['matched_task_ids']) for r in rows)/len(rows),4), 'unmapped_requirements': [], 'unmapped_requirements_union': [r['requirement_id'] for r in rows if not r['matched_task_ids']], 'coverage_degraded': 'parsed-sparse', 'coverage_undefined': False, 'stopwords': sorted(stopwords), 'tokenization': '[a-z0-9]+ unique set, casefold', 'matrix': rows}
    save('artifacts/coverage-matrix.yaml', summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('matrix','stopwords')}))
    print('UNMAPPED')
    for r in rows:
        if not r['matched_task_ids']:
            print(r['requirement_id'], r['citation'].rsplit(':',1)[1], r['containment_ratio'], r['quote'])
else:
    old = json.loads((OUT / 'artifacts/input-snapshot.yaml').read_text())
    new = snapshot()
    result = {'before': old['input_tree_sha256'], 'after': new['input_tree_sha256'], 'input_drift_detected': old['input_tree_sha256'] != new['input_tree_sha256'], 'file_count': new['file_count'], 'quote_mismatches': []}
    for row in json.loads((OUT / 'artifacts/coverage-matrix.yaml').read_text())['matrix']:
        ln = int(row['citation'].rsplit(':',1)[1])
        if row['quote'] not in SPEC.read_text().splitlines()[ln-1]:
            result['quote_mismatches'].append(row['requirement_id'])
    save('artifacts/input-recheck.yaml', result)
    print(json.dumps(result))
