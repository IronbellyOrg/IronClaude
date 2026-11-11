"""Reproduce offline ANSI/text/SVG/PNG/PDF/gallery designs from synthetic records."""
import argparse
import hashlib
import importlib
import json
import os
import time
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont
from canvas import Canvas, PALETTE
from fixtures import fixture, metrics, write_fixtures

ROOT=Path(__file__).resolve().parent
WIDTHS=(160,116,80)
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
CW,CH,PAD=ImageFont.truetype(FONT_PATH,16).getlength("M"),20,20

def designs(batch=1):
    modules=("layouts.group_a","layouts.group_b") if batch==1 else ("layouts.agent_focus",)
    result={}
    for name in modules:result.update(importlib.import_module(name).DESIGNS)
    return result

def screen(spec,f,width,ascii_mode=False):
    c=Canvas(width,48 if width>=144 else 42,ascii_mode)
    spec["render"](c,f,metrics(f))
    return c

def image(c,no_color=False):
    im=Image.new("RGB",(round(c.w*CW+2*PAD),c.h*CH+2*PAD),PALETTE["bg"])
    draw=ImageDraw.Draw(im)
    normal=ImageFont.truetype(FONT_PATH,16)
    bold=ImageFont.truetype(BOLD_PATH,16)
    for y,row in enumerate(c.cells):
        for x,ch in enumerate(row):
            if ch.strip():draw.text((PAD+x*CW,PAD+y*CH),ch,font=bold if c.weights[y][x] else normal,fill=PALETTE["ink"] if no_color else PALETTE[c.colors[y][x]])
    return im

def exports(batch=1):
    write_fixtures(ROOT)
    out=ROOT if batch==1 else ROOT/"agent-focus"
    out.mkdir(exist_ok=True)
    ds=designs(batch); f=fixture();manifest={"synthetic":True,"as_of":f["as_of"],"batch":batch,"widths":WIDTHS,"concepts":[]}
    pages=[]
    for slug,spec in ds.items():
        entry={k:v for k,v in spec.items() if k!="render"};entry["slug"]=slug;entry["exports"]={}
        for width in WIDTHS:
            folder=out/"exports"/str(width);folder.mkdir(parents=True,exist_ok=True)
            c=screen(spec,f,width);ac=screen(spec,f,width,True);prefix=folder/slug
            prefix.with_suffix(".txt").write_text(c.plain())
            prefix.with_suffix(".ascii.txt").write_text(ac.plain())
            prefix.with_suffix(".ansi").write_text(c.ansi())
            prefix.with_suffix(".svg").write_text(c.svg(cw=CW,ch=CH))
            im=image(c);im.save(prefix.with_suffix(".png"))
            image(c,True).save(folder/(slug+".mono.png"))
            entry["exports"][str(width)]=str(prefix.relative_to(out))
            if width==160:pages.append((slug,spec["name"],im))
        manifest["concepts"].append(entry)
    thumb_w=800;thumb_h=round(pages[0][2].height*thumb_w/pages[0][2].width)
    sheet=Image.new("RGB",(thumb_w*2,(thumb_h+40)*((len(pages)+1)//2)),PALETTE["bg"])
    draw=ImageDraw.Draw(sheet);font=ImageFont.truetype(BOLD_PATH,18)
    for i,(_,title,im) in enumerate(pages):
        x=i%2*thumb_w;y=i//2*(thumb_h+40)
        draw.text((x+16,y+8),title,font=font,fill=PALETTE["ink"])
        sheet.paste(im.resize((thumb_w,thumb_h),Image.Resampling.LANCZOS),(x,y+40))
    sheet.save(out/"contact-sheet.png")
    pdf_pages=[im.convert("RGB") for _,_,im in pages]
    pdf_pages[0].save(out/"portfolio.pdf",save_all=True,append_images=pdf_pages[1:],resolution=120,creationDate=time.gmtime(0),modDate=time.gmtime(0),title="Synthetic Orca observation designs")
    manifest["fixture_sha256"]=hashlib.sha256((ROOT/"fixture.json").read_bytes()).hexdigest()
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    build_gallery(out,ds)
    print(f"Rendered {len(ds)} designs x {len(WIDTHS)} widths into {out}")


def build_gallery(out,ds):
    # Every selectable scenario has actual separately composed screens, no rescaling.
    scenarios={"base":fixture()}
    for p in sorted((ROOT/"scenarios").glob("*.json")):scenarios[p.stem]=json.loads(p.read_text())
    frames={}
    for scenario,f in scenarios.items():
        frames[scenario]={}
        for slug,spec in ds.items():
            frames[scenario][slug]={str(w):{"html":screen(spec,f,w).html(),"ascii":screen(spec,f,w,True).plain()} for w in WIDTHS}
    metadata={slug:{k:v for k,v in spec.items() if k!="render"} for slug,spec in ds.items()}
    payload=json.dumps({"frames":frames,"scenarios":scenarios,"designs":metadata},ensure_ascii=True).replace("<","\\u003c")
    css="""/* Terminal specimen gallery: one observation surface, no operational controls. */
:root{--bg:#101820;--surface:#16232e;--ink:#e1e9ee;--muted:#a5b6c2;--accent:#70cde2;--line:#526c80;--body:system-ui,sans-serif;--display:Georgia,serif;--mono:'DejaVu Sans Mono',monospace;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px}main{max-width:1700px;margin:auto;display:grid;gap:20px;min-width:0}h1{font:2.4rem var(--display);margin:0}h2{font-size:1.15rem}p{max-width:90ch;line-height:1.55}nav,.controls{display:flex;gap:10px;flex-wrap:wrap}button,select,input{font:inherit;background:var(--surface);color:var(--ink);border:1px solid var(--line);padding:8px}button{cursor:pointer}button[aria-current=true]{border-color:var(--accent);font-weight:bold}*:focus-visible{outline:3px solid var(--accent);outline-offset:3px}.terminal{overflow:auto;max-width:100%;border:1px solid var(--line);background:var(--bg)}pre{font:clamp(10px,1vw,15px)/1.4 var(--mono);white-space:pre;margin:0;padding:12px;font-variant-numeric:tabular-nums}.strong{font-weight:bold}.mono pre span{color:var(--ink)!important}.muted{color:var(--muted)}.detail{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:16px}.detail pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}#records{max-height:260px;overflow:auto;display:grid;gap:4px}#records button{text-align:left}a{color:var(--accent)}label{display:flex;gap:8px;align-items:center}#state{font-family:var(--mono);color:var(--muted)}@media(max-width:700px){.detail{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""+"\n".join(f".c-{k}"+"{color:"+v+"}" for k,v in PALETTE.items())
    doc='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Orca Observation Studio</title><style>'''+css+'''</style></head><body><main>
<header><h1>Orca Observation Studio</h1><p>Original terminal compositions for Stably.ai Orca. SYNTHETIC FIXTURES ONLY. No live connections, commands, approvals or worker controls. Shapes, labels and colors come from the same character layout as the ANSI and image exports.</p></header>
<nav id="concepts" aria-label="Design concepts"></nav><div class="controls">
<label>Width <select id="width"><option>160</option><option>116</option><option>80</option></select></label>
<label>Scenario <select id="scenario"></select></label><label><input id="mono" type="checkbox">No color</label><label><input id="ascii" type="checkbox">ASCII</label><button id="hold">Hold view</button><button id="next">Next fixture observation</button></div>
<div id="state" aria-live="polite"></div><section><h2 id="title"></h2><p id="question"></p><div id="terminal" class="terminal" tabindex="0" aria-label="Terminal design preview"><pre id="screen"></pre></div><p id="tradeoff" class="muted"></p></section>
<section><h2>Evidence inspector</h2><p>Filter applies only to the inspector. Overview counts remain global. Full sanitized identifiers remain available here; selecting a record does not acknowledge any message.</p><div class="controls"><label>Owner <select id="owner"><option value="">All owners</option></select></label><label>Find <input id="search" type="search" placeholder="session, branch, mission"></label></div><p id="count"></p><div class="detail"><div id="records"></div><pre id="detail" tabindex="0"></pre></div></section>
<footer><p>Keys: left/right switch design when not editing input; j/k select inspector record; Space holds/resumes the view; Tab moves focus. Scenario changes during hold are queued. No animation or polling. Lifecycle, report outcome, evidence and admission are separate.</p><a href="portfolio.pdf">PDF portfolio</a> · <a href="contact-sheet.png">Contact sheet</a> · <a href="manifest.json">Export manifest</a></footer>
<script id="data" type="application/json">'''+payload+r'''</script><script>
const DATA=JSON.parse(document.getElementById('data').textContent);
const slugs=Object.keys(DATA.designs), scenarios=Object.keys(DATA.scenarios);
let current=slugs[0], scenario='base', selected='S001', held=false, pending=[],notice='';
function clean(v){return String(v).replace(/\x1b\][^\x07\x1b]*(?:\x07|\x1b\\|$)/g,'').replace(/\x1b[P^_].*?(?:\x1b\\|$)/gs,'').replace(/(?:\x1b\[|\x9b)[0-?]*[ -/]*[@-~]/g,'').replace(/[\x00-\x1f\x7f-\x9f‪-‮⁦-⁩]/g,'');}
function inspectRows(f,owner,query){return f.sessions.filter(s=>(!owner||s.owner===owner)&&clean(JSON.stringify(s)).toLowerCase().includes(query.toLowerCase()));}
function changeScenario(value){if(held){pending.push(value);notice='View held; '+pending.length+' fixture observations queued.';}else{scenario=value;notice='';}draw();}
function toggleHold(){held=!held;if(!held&&pending.length){scenario=pending[pending.length-1];pending=[];notice='Applied latest queued fixture; intermediate fixtures not replayed.';}draw();}
function draw(){const d=DATA.designs[current],f=DATA.scenarios[scenario],w=document.getElementById('width').value;
document.getElementById('title').textContent=d.name;document.getElementById('question').textContent=d.question;document.getElementById('tradeoff').textContent='Omits: '+d.omits+' Tradeoff: '+d.tradeoff+' Missing/stale: '+d.missing;
const pre=document.getElementById('screen'),frame=DATA.frames[scenario][current][w];if(document.getElementById('ascii').checked)pre.textContent=frame.ascii;else pre.innerHTML=frame.html;
document.getElementById('terminal').classList.toggle('mono',document.getElementById('mono').checked);document.getElementById('state').textContent=(held?'HELD':'STATIC FIXTURE')+' | '+scenario+' | as-of '+f.as_of+' | '+notice;document.getElementById('hold').textContent=held?'Resume view':'Hold view';document.getElementById('scenario').value=scenario;
for(const b of document.querySelectorAll('#concepts button'))b.setAttribute('aria-current',b.dataset.slug===current?'true':'false');
const owner=document.getElementById('owner').value,query=document.getElementById('search').value;const rows=inspectRows(f,owner,query);document.getElementById('count').textContent=rows.length+' inspector records / '+f.sessions.length+' global records (historical included if present). Overview not filtered.';
const list=document.getElementById('records');list.replaceChildren();if(!rows.some(s=>s.id===selected)){selected=rows[0]?.id||null;notice='Previous selection not in this view.';}
for(const s of rows){const b=document.createElement('button');b.textContent=clean(s.id+'  '+s.owner+'  '+s.label);b.setAttribute('aria-current',s.id===selected?'true':'false');b.onclick=()=>{selected=s.id;draw();};list.append(b);}
const record=rows.find(s=>s.id===selected);document.getElementById('detail').textContent=record?clean(JSON.stringify({session:record,worktree:f.worktrees.find(t=>t.id===record.worktree)||null},null,2)):'No matching records. This is not an all-clear.';}
for(const slug of slugs){const b=document.createElement('button');b.textContent=DATA.designs[slug].name;b.dataset.slug=slug;b.onclick=()=>{current=slug;draw();};document.getElementById('concepts').append(b);}
for(const s of scenarios){const o=document.createElement('option');o.value=s;o.textContent=s;document.getElementById('scenario').append(o);}
for(let i=1;i<=10;i++){const o=document.createElement('option');o.value='O'+String(i).padStart(2,'0');o.textContent=o.value;document.getElementById('owner').append(o);}
for(const id of ['width','mono','ascii','owner','search'])document.getElementById(id).addEventListener('input',draw);
document.getElementById('scenario').onchange=e=>changeScenario(e.target.value);document.getElementById('hold').onclick=toggleHold;document.getElementById('next').onclick=()=>changeScenario(scenarios[(scenarios.indexOf(pending.at(-1)||scenario)+1)%scenarios.length]);
document.addEventListener('keydown',e=>{if(['INPUT','SELECT','TEXTAREA','BUTTON'].includes(e.target.tagName))return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){current=slugs[(slugs.indexOf(current)+(e.key==='ArrowRight'?1:-1)+slugs.length)%slugs.length];e.preventDefault();draw();}else if(e.key===' '){e.preventDefault();toggleHold();}else if(e.key==='j'||e.key==='k'){const rows=inspectRows(DATA.scenarios[scenario],document.getElementById('owner').value,document.getElementById('search').value);if(rows.length){selected=rows[(Math.max(0,rows.findIndex(s=>s.id===selected))+(e.key==='j'?1:-1)+rows.length)%rows.length].id;draw();}}});draw();
</script></main></body></html>'''
    (out/"gallery.html").write_text(doc)

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--batch",type=int,choices=(1,2),default=1);parser.add_argument("--show");parser.add_argument("--width",type=int,default=116);args=parser.parse_args()
    if args.show:
        print(screen(designs(args.batch)[args.show],fixture(),args.width).ansi(no_color="NO_COLOR" in os.environ),end="")
    else:exports(args.batch)
