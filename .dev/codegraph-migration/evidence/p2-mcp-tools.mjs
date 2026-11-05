import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const [, , bin, dir, out] = process.argv;
const child = spawn(bin, ['serve', '--mcp'], { cwd: dir, env: process.env, stdio: ['pipe', 'pipe', 'inherit'] });
const waiting = new Map(); let buf = ''; let id = 0;
child.stdout.on('data', (d) => {
  buf += d;
  for (let i; (i = buf.indexOf('\n')) >= 0; buf = buf.slice(i + 1)) {
    let m; try { m = JSON.parse(buf.slice(0, i)); } catch { continue; }
    if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
  }
});
const rpc = (method, params) => new Promise((ok, no) => {
  const n = ++id; const t = setTimeout(() => no(new Error('timeout ' + method)), 60000);
  waiting.set(n, (m) => { clearTimeout(t); ok(m); });
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: n, method, params }) + '\n');
});
const bytes = (v) => Buffer.byteLength(typeof v === 'string' ? v : JSON.stringify(v));
const init = await rpc('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'p2-check', version: '0' } });
child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
const tools = (await rpc('tools/list', {})).result.tools;
const ex = await rpc('tools/call', { name: 'codegraph_explore', arguments: { query: 'main' } });
writeFileSync(out, JSON.stringify({
  server: init.result.serverInfo, tools,
  tools_bytes: bytes(tools),
  model_facing_bytes: bytes(tools.map((t) => ({ name: 'mcp__codegraph__' + t.name, description: t.description, inputSchema: t.inputSchema }))),
  instructions_bytes: bytes(init.result.instructions ?? ''),
  per_tool_bytes: Object.fromEntries(tools.map((t) => [t.name, bytes(t)])),
  explore_call_error: Boolean(ex.error || ex.result?.isError),
}, null, 2));
child.kill(); process.exit(0);
