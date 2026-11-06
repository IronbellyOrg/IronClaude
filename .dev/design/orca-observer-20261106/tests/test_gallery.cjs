// Headless DOM-contract test, not a browser-rendering or physical-keyboard test.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const file=process.argv[2]||path.join(__dirname,'../gallery.html');
const html=fs.readFileSync(file,'utf8');
const data=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script=html.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
function element(tag='DIV'){return {tagName:tag,children:[],value:'',checked:false,textContent:'',innerHTML:'',dataset:{},attrs:{},listeners:{},classList:{toggle(){}},append(x){this.children.push(x)},replaceChildren(){this.children=[]},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.listeners[k]=v}};}
const ids={};for(const id of ['data','concepts','width','scenario','mono','ascii','hold','next','state','title','question','terminal','screen','tradeoff','owner','search','count','records','detail'])ids[id]=element();
ids.data.textContent=data;ids.width.value='160';ids.scenario.value='base';
const doc={listeners:{},getElementById:id=>ids[id],createElement:t=>element(t.toUpperCase()),querySelectorAll:()=>ids.concepts.children,addEventListener(k,fn){this.listeners[k]=fn}};
const ctx={document:doc,console};vm.createContext(ctx);vm.runInContext(script,ctx,{timeout:30000});
assert.equal(ids.concepts.children.length,10);assert(ids.screen.innerHTML.includes('SYNTHETIC'));
const first=ids.title.textContent;doc.listeners.keydown({target:{tagName:'DIV'},key:'ArrowRight',preventDefault(){}});assert.notEqual(ids.title.textContent,first);
ids.width.value='80';ids.width.listeners.input();assert(ids.screen.innerHTML.length>0);
ids.ascii.checked=true;ids.ascii.listeners.input();assert(/^[\x00-\x7f]*$/.test(ids.screen.textContent));
ids.owner.value='O01';ids.owner.listeners.input();assert(ids.count.textContent.includes('10 inspector records / 80 global records'));
ids.hold.onclick();ids.next.onclick();assert(ids.state.textContent.includes('HELD'));assert(ids.state.textContent.includes('queued'));
ids.hold.onclick();assert(!ids.state.textContent.startsWith('HELD'));assert(ids.state.textContent.includes('Applied latest queued'));
ids.scenario.onchange({target:{value:'empty'}});assert(ids.detail.textContent.includes('not an all-clear'));
assert(!html.includes('fetch('));assert(!html.includes('setInterval('));
console.log('PASS: script syntax; ten concepts; design navigation; width/ASCII; filtered/global counts; hold/queue/resume; empty state; no network/polling. DOM simulation only.');
