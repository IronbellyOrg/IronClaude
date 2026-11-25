"""Render synthetic, terminal-cell design sketches; no Orca connection or controls."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "visual-v2"
ROOT.mkdir(exist_ok=True)
COLS, ROWS = 144, 57
CW, CH, PAD = 11, 22, 24
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 17)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 17)
COLORS = {"bg":"#111b26", "panel":"#172534", "text":"#e4edf5", "muted":"#9aafc1", "line":"#426077", "accent":"#70c9e6", "warn":"#fab219", "bad":"#ef8b8b", "good":"#83d4ab"}
# Colors carry semantic state, not categorical series. Words retain every meaning.
MODULES = [
 ("01  DECISION YIELD", "warn", [
  "What would your next answer unblock?", "",
  "SCHEMA STRATEGY     12 tasks   45m", "DEPLOY WINDOW        5 tasks   20m", "REVIEW OWNERSHIP     2 tasks   10m", "",
  "14 unique affected tasks", "Impact overlaps: do not add 12+5+2.", "", "NEXT  Decide schema strategy.", "Basis: demo dependency + request joins"]),
 ("02  WAITING DEBT", "warn", [
  "280 worker-min in recorded waits", "Last 60m / 8 workers with wait history", "", "Window average  35m per worker", "Requests         3 observed open", "Oldest          45m schema strategy", "", "No spend estimate: usage unavailable.", "", "NEXT  Clear the oldest root blocker.", "Basis: summed demo wait intervals"]),
 ("03  HANDOFF GAPS", "bad", [
  "Delivered is not answered.", "", "Billing -> coordinator -> YOU", "  45m  schema question / no reply seen", "QA -> reviewer", "  22m  handoff / no acceptance seen", "UI -> coordinator", "  10m  review owner not assigned", "", "NEXT  Claim the orphaned review.", "Basis: sampled threads; not full inbox"]),
 ("04  OVERLAPPING WORK", "warn", [
  "Potential collisions, not proven faults", "", "billing/schema.py", "  migration + compatibility + tests", "  3 active tasks touch this file", "", "Two task briefs request the same", "API retry policy. Similarity inferred.", "", "NEXT  Compare scope before more work.", "Basis: demo diffs + inferred brief match"]),
 ("05  RETRY LOOPS", "bad", [
  "Repeated effort without new evidence", "", "payments-contract test", "  attempt 1  FAIL  same assertion", "  attempt 2  FAIL  same assertion", "  attempt 3  FAIL  same assertion", "", "No changed diagnosis recorded.", "Signature match is a heuristic.", "NEXT  Ask for a different hypothesis.", "Basis: demo attempts + failure signatures"]),
 ("06  BLOCKING CHAIN", "accent", [
  "Your decision has downstream reach.", "", "SCHEMA CHOICE [YOU]", "  ├─ migration", "  │   ├─ compatibility checks", "  │   └─ integration tests", "  └─ API rollout", "      └─ release review", "12 descendants total / tree excerpt", "NEXT  Answer at the root, not leaves.", "Basis: demo graph; no completion ETA"]),
 ("07  READY BUT UNASSIGNED", "accent", [
  "Work that can move without your answer", "", "Docs updates             3 tasks", "Isolated unit tests      2 tasks", "Release notes            1 task", "                         ───────", "                         6 ready", "No dependency or gate outstanding", "in this synthetic task inventory.", "NEXT  Ask coordinator to route work.", "Basis: readiness + active-attempt joins"]),
 ("08  VERIFICATION DRIFT", "bad", [
  "Reported complete is not current proof.", "", "2 tasks: passing checks on OLD revision", "1 task: worker says done; no review", "", "billing     tested a71 -> current b92", "api-client  tested c18 -> current d04", "", "No current pass claimed for either.", "NEXT  Re-run checks on current heads.", "Basis: demo revision-bound evidence"]),
 ("09  SIGNAL DIGEST", "good", [
  "Since your last visit / 15 minutes", "", "864 routine events sampled", "  7 distinct issue candidates", "  3 human requests observed", "",
  "+ retry loop detected", "+ review ownership missing", "= schema decision still waiting", "NEXT  Read issues, not the raw stream.", "Basis: demo event grouping; coverage partial"]),
]
NAMES = ["Decision Bridge", "Copper Patchbay", "Signal Observatory", "Evidence Console", "Coordination Desk", "Dependency Atlas", "Review Workbench", "Waiting Room", "Quiet Command", "Incident Mosaic"]
ORDERS = [list(range(9)), [5,0,2,3,4,7,1,6,8], [8,0,1,2,5,7,3,4,6], [7,4,0,2,3,5,1,6,8], [2,0,8,5,3,7,1,4,6], [5,0,6,2,1,4,3,7,8], [7,0,3,4,2,6,5,1,8], [1,0,2,5,6,8,3,4,7], [0,2,7,5,1,6,3,4,8], [4,3,7,0,2,5,1,6,8]]

# Nine panels in every layout. x/y/w/h are exact terminal cells, not browser cards.
def boxes(kind):
    if kind == 0: return [(1+c*48,5+r*16,46,15) for r in range(3) for c in range(3)]
    if kind == 1: return [(1,5,94,15),(97,5,46,15)] + [(1+c*48,21+r*16,46,15) for r in range(2) for c in range(3)] + [(97,53,46,3)]
    if kind == 2: return [(1,5,46,15),(49,5,94,15)] + [(1+c*48,21+r*16,46,15) for r in range(2) for c in range(3)] + [(1,53,94,3)]
    return [(1+c*48,5+r*16,46,15) for r in range(3) for c in range(3)]

# Layouts 1/2 use a compact ninth ticker; it preserves the digest's useful content.
def build(index):
    chars=[[" " for _ in range(COLS)] for _ in range(ROWS)]
    inks=[["text" for _ in range(COLS)] for _ in range(ROWS)]
    bold=[[False for _ in range(COLS)] for _ in range(ROWS)]
    occupied=set()
    def put(x,y,text,color="text",strong=False,maxlen=None):
        if maxlen is not None and len(text)>maxlen: text=text[:maxlen-1]+"…"
        assert 0 <= y < ROWS and 0 <= x and x+len(text)<=COLS, (x,y,text)
        for n,ch in enumerate(text): chars[y][x+n]=ch; inks[y][x+n]=color; bold[y][x+n]=strong
    def frame(x,y,w,h,title,color,heavy=False):
        glyphs=("┏","━","┓","┃","┗","┛") if heavy else ("╭","─","╮","│","╰","╯")
        a,b,c,d,e,f=glyphs
        for yy in range(y,y+h):
            for xx in range(x,x+w):
                assert (xx,yy) not in occupied, (xx,yy)
                occupied.add((xx,yy))
        put(x,y,a+b*(w-2)+c,color)
        put(x,y+h-1,e+b*(w-2)+f,"line")
        for yy in range(y+1,y+h-1): put(x,yy,d,"line"); put(x+w-1,yy,d,"line")
        put(x+2,y," "+title+" ",color,True,w-4)
    put(2,0,"◈  "+NAMES[index].upper(),"accent",True)
    put(78,0,"SYNTHETIC DESIGN  /  OBSERVER ONLY", "warn")
    put(2,2,"DECIDE 3 observed    UNBLOCK 14 unique tasks    READY 6    VERIFY 3", "text",True)
    put(2,3,"local host  ·  inbox PARTIAL  ·  no live connection  ·  demo as-of 15:00 UTC", "muted")
    bs=boxes(index%3)
    for slot,(x,y,w,h) in enumerate(bs):
        mid=ORDERS[index][slot]
        title,color,lines=MODULES[mid]
        frame(x,y,w,h,title,color,heavy=(slot==0 or index in (1,9)))
        if h==3:
            # Dedicated compact digest/readiness strip, not silently clipped detail.
            text={8:"864 events / 7 issues / 3 asks; partial",6:"6 ready: docs 3 / tests 2 / notes 1",7:"2 stale checks / 1 missing review"}.get(mid,title[4:])
            put(x+2,y+1,text,"muted",False,w-4)
            continue
        for j,line in enumerate(lines):
            ink = color if j==0 or line.startswith("NEXT") else ("muted" if line.startswith("Basis:") else "text")
            put(x+2,y+2+j,line,ink,j==0,w-4)
        if w>60:
            # Decorative patch leads with a labelled selected focus, not fake charts.
            put(x+49,y+4,"◉  SELECTED INSIGHT",color,True)
            put(x+49,y+6,"┃",color)
            put(x+49,y+7,"╰━━▶ evidence → next action", "muted")
            put(x+49,y+10,"↵ inspect   / filter", "muted")
    if index%3==0:
        put(2,54,"Proposed keys: tab widget  ↵ evidence  / filter  p freeze view  ? help", "muted")
        put(2,55,"Counts overlap except named worker buckets. Inferences are labelled. Nothing sends commands.","muted")
    else:
        put(2,56,"No live controls · proposed analytics require history, task links and revision evidence", "muted")
    return chars,inks,bold

artifacts=[]
for i,name in enumerate(NAMES):
    chars,inks,bolds=build(i)
    plain="\n".join("".join(row).rstrip() for row in chars)+"\n"
    assert "SYNTHETIC" in plain and "PARTIAL" in plain
    path=ROOT/f"{i+1:02d}-{name.lower().replace(' ','-')}"
    path.with_suffix('.txt').write_text(plain)
    ansi=[]
    for y,row in enumerate(chars):
        previous=None
        for x,char in enumerate(row):
            style=(inks[y][x],bolds[y][x])
            if style!=previous:
                rgb=tuple(int(COLORS[style[0]][n:n+2],16) for n in (1,3,5))
                ansi.append(f"\033[0;{'1;' if style[1] else ''}38;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
                previous=style
            ansi.append(char)
        ansi.append("\033[0m\n")
    path.with_suffix('.ansi').write_text("".join(ansi))
    image=Image.new('RGB',(COLS*CW+2*PAD,ROWS*CH+2*PAD),COLORS['bg'])
    draw=ImageDraw.Draw(image)
    for y,row in enumerate(chars):
        for x,char in enumerate(row):
            if char!=' ': draw.text((PAD+x*CW,PAD+y*CH),char,font=BOLD if bolds[y][x] else FONT,fill=COLORS[inks[y][x]])
    image.save(path.with_suffix('.png'))
    artifacts.append((name,path.name,image))
# Contact sheet: 2 columns, 5 rows. Individual full-resolution files retain readable detail.
thumbw=792
thumbh=round(artifacts[0][2].height*thumbw/artifacts[0][2].width)
sheet=Image.new('RGB',(thumbw*2, (thumbh+42)*5),COLORS['bg'])
sd=ImageDraw.Draw(sheet)
for i,(name,stem,image) in enumerate(artifacts):
    x=(i%2)*thumbw;y=(i//2)*(thumbh+42)
    sd.text((x+16,y+8),f"{i+1:02d}  {name}",font=BOLD,fill=COLORS['text'])
    sheet.paste(image.resize((thumbw,thumbh)),(x,y+42))
sheet.save(ROOT/'contact-sheet.png')
assert len(artifacts)==10
print(f"Rendered 10 colored mockups, each with 9 widgets, at {COLS} columns.")
print(ROOT/'contact-sheet.png')
