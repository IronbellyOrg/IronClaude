"""Offline artifact checks, not operational Orca tests."""
import json
import re
import sys
import unittest
from pathlib import Path
from wcwidth import wcswidth
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fixtures import fixture, metrics, normalize_events
from canvas import Canvas, clip, sanitize
from render import designs, screen

class Semantics(unittest.TestCase):
    def test_scale_matrix(self):
        for o in (5,8,10):
            for n in (50,80,100):
                f=fixture(o,n);m=metrics(f)
                self.assertEqual(len(f['orchestrators']),o)
                self.assertEqual(m['total'],n);self.assertEqual(m['worktrees'],n)
                self.assertEqual(m['running']+m['settled']+m['unknown'],n)
                self.assertEqual(len({s['id'] for s in f['sessions']}),n)
                self.assertTrue(all(s['owner'] in {v['id'] for v in f['orchestrators']} for s in f['sessions']))
    def test_declared_relationships(self):
        for o in (5,8,10):
            for n in (50,80,100):
                for variant in ('base','uneven'):
                    f=fixture(o,n,variant);by_id={s['id']:s for s in f['sessions']}
                    for e in f['edges']:
                        self.assertTrue(all(by_id[sid]['owner']==e['to'] for sid in e['sessions']))
                    self.assertEqual(len({by_id[sid]['owner'] for sid in f['requests'][0]['affected']}),4)
    def test_source_age_matches_timestamp(self):
        from datetime import datetime
        for variant in ('base','source-loss'):
            f=fixture(variant=variant);now=datetime.fromisoformat(f['as_of'])
            for src in f['sources'].values():
                self.assertEqual((now-datetime.fromisoformat(src['observed_at'])).total_seconds(),src['age_s'])
    def test_mapping_not_assumed(self):
        m=metrics(fixture(variant='shared-unmapped'))
        self.assertEqual(m['total'],80);self.assertEqual(m['worktrees'],78);self.assertEqual(m['unmapped'],1)
        self.assertEqual(m['inventory_worktrees'],80)
    def test_history_separate(self):
        m=metrics(fixture(variant='historical'));self.assertEqual(m['total'],80);self.assertEqual(m['historical'],1)
    def test_evidence_is_not_admission(self):
        f=fixture();s=f['sessions'][7]
        self.assertNotEqual(s['revision'],s['check_revision']);self.assertEqual(s['tests'],'passed')
        self.assertEqual(s['admission'],'not admitted')
        self.assertTrue(any(s['result']=='partial' and s['admission']=='not admitted' for s in f['sessions']))
        self.assertTrue(any(t['dirty'] and t['policy']=='not frozen' for t in f['worktrees']))
    def test_partial_subtotal(self):
        f=fixture();m=metrics(f)
        self.assertEqual(m['cost_measured'],60);self.assertEqual(m['total'],80)
        self.assertEqual(m['cost'],round(sum(s['cost_usd'] or 0 for s in f['sessions']),2))
    def test_events_idempotent(self):
        self.assertEqual(normalize_events(fixture()['events']),normalize_events(fixture(variant='duplicate-out-of-order')['events']))
    def test_filter_denominators(self):
        f=fixture(variant='uneven');m=metrics(f,'O01');self.assertLess(m['total'],m['global_total']);self.assertEqual(m['global_total'],80)
    def test_empty(self):self.assertEqual(metrics(fixture(variant='empty'))['total'],0)

class SafeText(unittest.TestCase):
    def test_control_injection(self):
        hostile='visible\x1b]52;c;attack\x07\x1b[2J\r\x9b31m‮text'
        s=sanitize(hostile);self.assertEqual(s,'visibletext')
        self.assertNotIn('\x1b',s);self.assertNotIn('\r',s)
    def test_width(self):
        for t in ['normal','漢字'*20,'é'*20,'👩‍💻'*10]:
            for width in (1,5,20):self.assertLessEqual(wcswidth(clip(t,width)),width)
    def test_ascii(self):self.assertTrue(clip('╭─漢字→✓',20,True).isascii())
    def test_no_color(self):
        c=Canvas(80,42);c.text(2,2,'Attention','warn',True)
        self.assertEqual(c.ansi(True),c.plain())
        self.assertEqual(re.sub(r'\x1b\[[0-9;]*m','',c.ansi()),c.plain())
    def test_html_escape(self):
        c=Canvas(80,42);c.text(0,0,'<script>');self.assertNotIn('<script>',c.html());self.assertIn('&lt;script&gt;',c.html())

class Layouts(unittest.TestCase):
    def test_all_scenarios_widths(self):
        cases=[fixture(o,n) for o in (5,8,10) for n in (50,80,100)]
        cases += [fixture(variant=v) for v in ('uneven','shared-unmapped','historical','long-identifiers','source-loss','missing-fields','duplicate-out-of-order','empty','injection')]
        ds={**designs(),**designs(2)};self.assertEqual(len(ds),20)
        for f in cases:
            for slug,spec in ds.items():
                for w in (160,144,116,80):
                    with self.subTest(scenario=f['variant'],concept=slug,width=w):
                        c=screen(spec,f,w)
                        self.assertTrue(all(wcswidth(line)==w for line in c.plain().splitlines()))
                        self.assertIn('SYNTHETIC',c.plain());self.assertNotIn('\x1b',c.plain())
                        self.assertTrue(c.plain().splitlines()[-2].strip().startswith('j/k select'), 'Navigation footer overwritten')
                        self.assertEqual(c.plain(),screen(spec,f,w).plain())
                        self.assertTrue(screen(spec,f,w,True).plain().isascii())
    def test_quilt_identifiable_base(self):
        f=fixture()
        for width in (160,116):
            text=screen(designs()['fleet-quilt'],f,width).plain()
            for s in f['sessions']:
                self.assertRegex(text,re.escape(s['id'])+r' [RSFP?]')
    def test_cost_missing_is_not_zero(self):
        f=fixture()
        for s in f['sessions']:s['cost_usd']=None
        for width in (160,116,80):
            text=screen(designs()['budget-engine'],f,width).plain()
            self.assertNotIn('$0.00',text);self.assertNotIn('$  0.00',text)
            self.assertIn('unknown',text.lower())
    def test_export_manifest(self):
        for root in (ROOT, ROOT/'agent-focus'):
            p=root/'manifest.json'
            self.assertTrue(p.exists(), 'Exports missing: '+str(p))
            data=json.loads(p.read_text());self.assertEqual(len(data['concepts']),10)
            for item in data['concepts']:
                for w in (160,116,80):
                    base=root/item['exports'][str(w)]
                    for suffix in ('.txt','.ascii.txt','.ansi','.png','.svg'):
                        self.assertTrue(base.with_suffix(suffix).exists())
                    self.assertEqual(re.sub(r'\x1b\[[0-9;]*m','',base.with_suffix('.ansi').read_text()),base.with_suffix('.txt').read_text())
            self.assertTrue((root/'portfolio.pdf').read_bytes().startswith(b'%PDF'))

if __name__=='__main__':unittest.main(verbosity=2)
