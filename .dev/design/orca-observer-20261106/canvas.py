"""Exact terminal-cell canvas shared by every export. No operational calls."""
import re
import unicodedata
from html import escape
from wcwidth import wcwidth, wcswidth

PALETTE={"bg":"#101820","panel":"#16232e","ink":"#e1e9ee","muted":"#a5b6c2","line":"#526c80","accent":"#70cde2","warn":"#fab219","bad":"#f08d96","good":"#8bd7af","frozen":"#c2adf2"}
ASCII_MAP=str.maketrans({**{c:"-" for c in "─━═┄┈"},**{c:"|" for c in "│┃║┆┊"},**{c:"+" for c in "┌┐└┘├┤┬┴┼╭╮╰╯┏┓┗┛┣┫┳┻╋╔╗╚╝╠╣╦╩╬"},"█":"#","░":".","▒":":","▓":"#","●":"o","○":"o","◆":"*","◇":"o","◈":"*","◉":"o","✓":"v","✕":"x","×":"x","→":">","←":"<","↵":">","▸":">","▾":"v","…":"~","·":".","▲":"^","▼":"v","━":"-"})

def sanitize(value):
    text=str(value)
    # Full CSI/OSC/DCS sequences, not just their ESC introducer.
    text=re.sub(r"(?:\x1b\]|\x9d).*?(?:\x07|\x1b\\|\x9c|$)","",text,flags=re.S)
    text=re.sub(r"(?:\x1b[P^_]|[\x90\x9e\x9f]).*?(?:\x1b\\|\x9c|$)","",text,flags=re.S)
    text=re.sub(r"(?:\x1b\[|\x9b)[0-?]*[ -/]*[@-~]","",text)
    text=re.sub(r"\x1b[@-_]","",text)
    return "".join(c for c in text if unicodedata.category(c) not in ("Cc","Cf","Cs"))

def clip(text,width,ascii_mode=False):
    text=sanitize(text)
    if ascii_mode: text=text.translate(ASCII_MAP).encode("ascii","replace").decode()
    if wcswidth(text)<=width: return text
    end="~" if ascii_mode else "…"
    out=""; used=0
    for ch in text:
        n=max(0,wcwidth(ch))
        if used+n>max(0,width-1):break
        out+=ch;used+=n
    return out+end if width else ""

class Canvas:
    def __init__(self,width,height=48,ascii_mode=False):
        self.w=width;self.h=height;self.ascii=ascii_mode
        self.cells=[[" " for _ in range(width)] for _ in range(height)]
        self.colors=[["ink" for _ in range(width)] for _ in range(height)]
        self.weights=[[False for _ in range(width)] for _ in range(height)]
        self.regions=[];self.details=[];self.clipped=[]
    def text(self,x,y,text,color="ink",bold=False,width=None):
        assert 0<=x<self.w and 0<=y<self.h,(x,y,self.w,self.h)
        assert color in PALETTE,color
        limit=self.w-x if width is None else min(width,self.w-x)
        clean=sanitize(text)
        if wcswidth(clean)>limit:self.clipped.append(clean)
        clean=clip(clean,limit,self.ascii)
        start=x
        for ch in clean:
            n=wcwidth(ch)
            if n<0:continue
            if n==0:
                if x>start:self.cells[y][x-1]+=ch
                continue
            self.cells[y][x]=ch;self.colors[y][x]=color;self.weights[y][x]=bold
            for k in range(1,n):self.cells[y][x+k]="";self.colors[y][x+k]=color
            x+=n
        return y+1
    def line(self,x,y,width,color="line",heavy=False):self.text(x,y,("━" if heavy else "─")*width,color)
    def panel(self,x,y,w,h,title,color="line",heavy=False):
        assert w>=5 and h>=3 and x>=0 and y>=0 and x+w<=self.w and y+h<=self.h,(x,y,w,h)
        self.regions.append((x,y,w,h,title))
        a,b,c,d,e,f=("┏","━","┓","┃","┗","┛") if heavy else ("╭","─","╮","│","╰","╯")
        self.text(x,y,a+b*(w-2)+c,color)
        self.text(x,y+h-1,e+b*(w-2)+f,color)
        for yy in range(y+1,y+h-1):self.text(x,yy,d,color);self.text(x+w-1,yy,d,color)
        self.text(x+2,y," "+title+" ",color,True,w-4)
    def lines(self,x,y,lines,width,color="ink"):
        for line in lines:
            if y>=self.h:break
            self.text(x,y,line,color,width=width);y+=1
    def bar(self,x,y,value,total,width=20,color="accent"):
        if value is None or total is None or total<=0:self.text(x,y,"unknown", "muted",width=width);return
        n=round(width*max(0,min(1,value/total)))
        self.text(x,y,"█"*n,color);self.text(x+n,y,"░"*(width-n),"line") if n<width else None
    def header(self,title,f,m):
        self.text(2,1,"◈ "+title.upper(),"accent",True,width=self.w-30)
        self.text(self.w-25,1,"SYNTHETIC · READ ONLY","warn",width=23)
        self.text(2,2,f"{len(f['orchestrators'])} owners / {m['total']} sessions / {m['worktrees']} mapped trees",width=self.w-4)
        self.text(2,3,f"08:00 UTC | msgs {f['sources']['messages']['coverage']} | workers {f['sources']['workers']['age_s']}s | checks {f['sources']['checks']['age_s']//60}m", "muted",width=self.w-4)
    def footer(self,text="j/k select · tab pane · / filter · enter evidence · p hold view"):
        self.line(1,self.h-3,self.w-2)
        self.text(2,self.h-2,text,"muted",width=self.w-4)
        self.text(2,self.h-1,"LOCAL FIXTURE · source coverage is not fleet-wide assurance", "muted",width=self.w-4)
    def plain(self):return "\n".join("".join(row) for row in self.cells)+"\n"
    def ansi(self,no_color=False):
        if no_color:return self.plain()
        result=[]
        for y in range(self.h):
            old=None
            for x,ch in enumerate(self.cells[y]):
                if not ch:continue
                style=(self.colors[y][x],self.weights[y][x])
                if style!=old:
                    h=PALETTE[style[0]];r,g,b=[int(h[i:i+2],16) for i in (1,3,5)]
                    result.append(f"\x1b[0;{'1;' if style[1] else ''}38;2;{r};{g};{b}m");old=style
                result.append(ch)
            result.append("\x1b[0m\n")
        return "".join(result)
    def html(self):
        rows=[]
        for y in range(self.h):
            runs=[];old=None;part=""
            for x,ch in enumerate(self.cells[y]):
                style=(self.colors[y][x],self.weights[y][x])
                if style!=old and old is not None:
                    runs.append(f'<span class="c-{old[0]}'+(' strong' if old[1] else '')+'">'+escape(part)+'</span>');part=""
                part+=ch;old=style
            if old:runs.append(f'<span class="c-{old[0]}'+(' strong' if old[1] else '')+'">'+escape(part)+'</span>')
            rows.append("".join(runs))
        return "\n".join(rows)
    def svg(self,cw=10,ch=20):
        out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w*cw+32}" height="{self.h*ch+32}" viewBox="0 0 {self.w*cw+32} {self.h*ch+32}">',f'<rect width="100%" height="100%" fill="{PALETTE["bg"]}"/>','<g font-family="DejaVu Sans Mono, monospace" font-size="16">']
        for y,row in enumerate(self.cells):
            for x,char in enumerate(row):
                if char.strip():out.append(f'<text x="{16+x*cw}" y="{16+y*ch+16}" fill="{PALETTE[self.colors[y][x]]}"'+(' font-weight="bold"' if self.weights[y][x] else '')+'>'+escape(char)+'</text>')
        return "".join(out)+"</g></svg>"


def selected_summary(c,f,y=6):
    q=f["requests"][0] if f["requests"] else None
    if not q:c.text(3,y,"No requests in this fixture; source coverage still matters.","muted",width=c.w-6);return
    c.text(3,y,q["question"],"warn",True,width=c.w-6)
    c.text(3,y+1,f"Owner {q['owner']} | {len(q['affected'])} sessions | {q['age_min']}m observed",width=c.w-6)
    c.text(3,y+2,"Evidence "+q["evidence"],"muted",width=c.w-6)
