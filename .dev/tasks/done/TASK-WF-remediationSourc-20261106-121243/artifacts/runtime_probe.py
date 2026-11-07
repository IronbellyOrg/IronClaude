"""Installed Claude controls and actual native→unchanged shim→local synthetic gateway.
No provider inference, real credentials, user settings, or original diagnosis artifacts.
Run with: uv run python <this file>. All evidence stays beside this script.
"""
from pathlib import Path
import http.server
import json
import os
import runpy
import select
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
NATIVE = '/opt/nvm/versions/node/v24.22.2/bin/claude'
WORK = HERE / ('runtime-work-' + (sys.argv[1] if len(sys.argv) > 1 else '1'))
HELPERS = runpy.run_path(str(ROOT / 'tests/unit/test_ccsession_tiers.py'))
MODELS = HELPERS['models']
SKILL = HELPERS['SKILL_DIR']
ENV_KEYS = ['ANTHROPIC_BASE_URL', 'ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN',
            'ANTHROPIC_DEFAULT_OPUS_MODEL', 'ANTHROPIC_DEFAULT_SONNET_MODEL',
            'ANTHROPIC_DEFAULT_HAIKU_MODEL', 'ANTHROPIC_CUSTOM_MODEL_OPTION',
            'ANTHROPIC_CUSTOM_MODEL_OPTION_NAME', 'ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION',
            'CLAUDE_CODE_MAX_CONTEXT_TOKENS', 'CLAUDE_CODE_AUTO_COMPACT_WINDOW',
            'CLAUDE_AUTOCOMPACT_PCT_OVERRIDE', 'CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY']


def synthetic(self):
    body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
    self.server.gateway.calls.append((self.path, body))
    if self.path.endswith('/count_tokens'):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"input_tokens":1}')
        return
    message = {'id': 'msg_local', 'type': 'message', 'role': 'assistant', 'content': [],
               'model': body['model'], 'stop_reason': None, 'stop_sequence': None,
               'usage': {'input_tokens': 1, 'output_tokens': 0}}
    self.send_response(200)
    self.send_header('Content-Type', 'text/event-stream')
    self.end_headers()
    events = [('message_start', {'type': 'message_start', 'message': message}),
              ('content_block_start', {'type': 'content_block_start', 'index': 0, 'content_block': {'type': 'text', 'text': ''}}),
              ('content_block_delta', {'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': 'local synthetic reply'}}),
              ('content_block_stop', {'type': 'content_block_stop', 'index': 0}),
              ('message_delta', {'type': 'message_delta', 'delta': {'stop_reason': 'end_turn', 'stop_sequence': None}, 'usage': {'output_tokens': 1}}),
              ('message_stop', {'type': 'message_stop'})]
    for name, value in events:
        self.wfile.write(f'event: {name}\ndata: {json.dumps(value)}\n\n'.encode())
    self.wfile.flush()


def native(case, launch, selected=None, request=False):
    folder = WORK / case
    home = folder / 'native-home'
    home.mkdir(parents=True, exist_ok=True)
    env = {'PATH': os.environ['PATH'], 'HOME': str(home), 'TERM': 'dumb',
           'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1', **launch['env']}
    argv = launch['argv']
    settings = argv[argv.index('--settings') + 1]
    model = selected or argv[argv.index('--model') + 1]
    cmd = [NATIVE, '--bare', '--restricted', '--setting-sources', '', '--strict-mcp-config',
           '--mcp-config', '{"mcpServers":{}}', '--tools', '', '--disable-slash-commands',
           '--no-session-persistence', '--system-prompt', 'Local boundary control.',
           '--model', model, '--settings', settings, '--print', '--verbose',
           '--input-format', 'stream-json', '--output-format', 'stream-json']
    replies = []
    buffer = b''
    log = (folder / 'native-stderr.log').open('w')
    proc = subprocess.Popen(cmd, cwd=home, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log)

    def wait_for(predicate):
        nonlocal buffer
        deadline = time.monotonic() + 40
        while time.monotonic() < deadline:
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                if not line.strip():
                    continue
                item = json.loads(line)
                replies.append(item)
                if predicate(item):
                    return item
            if not select.select([proc.stdout], [], [], 0.5)[0]:
                if proc.poll() is not None:
                    raise RuntimeError(f'{case}: native exited {proc.returncode}')
                continue
            chunk = os.read(proc.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError(f'{case}: native EOF')
            buffer += chunk
        raise TimeoutError(case)

    controls = {}
    try:
        for name in ('initialize', 'list_models', 'get_context_usage'):
            msg = {'type': 'control_request', 'request_id': name, 'request': {'subtype': name}}
            proc.stdin.write((json.dumps(msg) + '\n').encode())
            proc.stdin.flush()
            item = wait_for(lambda i: i.get('type') == 'control_response' and i.get('response', {}).get('request_id') == name)
            assert item['response']['subtype'] == 'success', item
            controls[name] = item['response'].get('response', {})
        result = None
        if request:
            msg = {'type': 'user', 'message': {'role': 'user', 'content': 'Return the local synthetic reply.'}}
            proc.stdin.write((json.dumps(msg) + '\n').encode())
            proc.stdin.flush()
            result = wait_for(lambda i: i.get('type') == 'result')
            assert not result.get('is_error'), result
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        log.close()
        (folder / 'responses.json').write_text(json.dumps(replies, indent=2))
        (folder / 'command.json').write_text(json.dumps(cmd, indent=2))
    usage = controls['get_context_usage']
    return {'case': case, 'selected': model,
            'models': [{k: row.get(k) for k in ('value', 'displayName', 'description', 'resolvedModel')} for row in controls['list_models'].get('models', [])],
            'context': {k: usage.get(k) for k in ('model', 'maxTokens', 'rawMaxTokens', 'autocompactSource', 'autoCompactThreshold')},
            'local_result': result and result.get('result'),
            'responses': str((folder / 'responses.json').relative_to(HERE))}


def main():
    work = WORK
    work.mkdir(exist_ok=True)
    gateway = HELPERS['StandInGateway']()
    gateway.server.gateway = gateway
    gateway.server.RequestHandlerClass.do_POST = synthetic
    env = {'PATH': os.environ['PATH'], 'HOME': str(work), 'CCSESSION_MODELS_REFRESH': '0',
           'XDG_CACHE_HOME': str(work / 'model-cache'), 'CCSESSION_DIR': str(SKILL),
           'AIDEV_AI_DEFAULTS_PATH': str(HELPERS['_defaults'](work)),
           'GW_PROXY_UPSTREAM': gateway.url, 'BOUNDARY_CAPTURE': str(work / 'shim-requests.jsonl')}
    port = HELPERS['_free_port']()
    while MODELS.shim_upstream_problem(gateway.url, port):
        port = HELPERS['_free_port']()
    env['GW_PROXY_PORT'] = str(port)
    shim_log = (work / 'shim-stderr.log').open('w')
    shim = subprocess.Popen([sys.executable, str(HERE / 'capture_shim.py')], env=env, cwd=ROOT, stderr=shim_log)
    import urllib.request
    base = f'http://127.0.0.1:{port}'
    output = {'native_version': subprocess.check_output([NATIVE, '--version'], text=True).strip(),
              'provider_inference': False, 'pipeline_hardening_verdict': 'advisory', 'waiver_status': 'latched', 'cases': []}
    try:
        for _ in range(100):
            try:
                with urllib.request.urlopen(base + '/__ccsession_shim', timeout=0.5) as response:
                    json.load(response)
                break
            except OSError:
                if shim.poll() is not None:
                    raise RuntimeError('shim exited before health')
                time.sleep(0.05)
        else:
            raise TimeoutError('shim health')
        rows = json.load(urllib.request.urlopen(base + '/v1/models'))['data']
        output['actual_shim_rows'] = rows
        for case, args, selected, expected, request in [
            ('tier0', ['--model', 'claude-gw-tier0'], None, 850000, False),
            ('tier1a', ['--model', 'claude-gw-tier1a[1m]'], None, 850000, False),
            ('tier1b', ['--tier', '1b'], None, 850000, False),
            ('tier2', ['--tier', '2'], None, 500000, False),
            ('compact-override', ['--tier', '0'], None, 300000, False),
            ('alias-opus', ['--tier', '2'], 'opus', 850000, True),
            ('alias-sonnet', ['--tier', '2'], 'sonnet', 850000, True),
            ('alias-haiku', ['--tier', '2'], 'haiku', 500000, True),
            ('bare-route', ['--tier', '1a'], 'claude-gw-tier1a', 200000, True),
        ]:
            folder = work / case
            folder.mkdir(exist_ok=True)
            launch_env = HELPERS['_launch_env'](folder, ANTHROPIC_BASE_URL=gateway.url,
                        CC_SHIM_PORT=str(port), ANTHROPIC_API_KEY='local-probe-not-a-secret',
                        ANTHROPIC_AUTH_TOKEN='local-probe-not-a-secret',
                        CCSESSION_MODELS_REFRESH='0', CCSESSION_COMPACT_WINDOW='300000' if case == 'compact-override' else '',
                        AIDEV_AI_DEFAULTS_PATH=env['AIDEV_AI_DEFAULTS_PATH'],
                        CCSESSION_ENV_FILE=str(folder / 'no-session.env'))
            for key in ('CODER_WORKSPACE_OWNER_NAME', 'CODER_WORKSPACE_OWNER_ROLES', 'CCSESSION_ACCESS', 'CCSESSION_TIER_RULES', 'CCSESSION_TIERS', 'CCSESSION_COOLDOWN_SECONDS', 'CCSESSION_FIRST_BYTE_TIMEOUT', 'CCSESSION_SHOW_ALL_MODELS', 'CCSESSION_GATEWAY_URL', 'CCSESSION_SHIM_URL', 'ANTHROPIC_MODEL'):
                launch_env.pop(key, None)
            launch_env['CCSESSION_PERMISSIONS'] = 'default'
            (folder / 'curl').write_text('#!/bin/sh\nexec /usr/bin/curl "$@"\n')
            (folder / 'claude').write_text('#!/usr/bin/env python3\nimport json,os,sys\njson.dump({"argv":sys.argv[1:],"env":{k:os.environ[k] for k in '+repr(ENV_KEYS)+' if k in os.environ}},open(os.environ["SEEN_FILE"],"w"))\n')
            proc = subprocess.run([str(SKILL / 'ccsession'), 'work', *args], cwd=folder, env=launch_env, capture_output=True, text=True, timeout=60)
            (folder / 'launch-stderr.log').write_text(proc.stderr)
            assert proc.returncode == 0, proc.stderr
            launch = json.loads((folder / 'seen.json').read_text())
            before = len(gateway.calls)
            item = native(case, launch, selected, request)
            assert item['context']['maxTokens'] == expected, item
            expected_rows = ['default', *[r['id'] for r in rows]]
            if selected is None:
                assert [m['value'] for m in item['models']] == expected_rows, item
            else:
                assert [m['value'] for m in item['models']] == [*expected_rows, selected], item
                item['native_selected_row_readded'] = selected
            item['upstream_models'] = [b['model'] for _, b in gateway.calls[before:]]
            if request:
                assert item['upstream_models'], item
                assert not any('[1m]' in m or m.startswith('claude-gw-') for m in item['upstream_models']), item
            output['cases'].append(item)
            (HERE / 't4-runtime.json').write_text(json.dumps(output, indent=2))
            print(case, item['context']['maxTokens'], item['upstream_models'], flush=True)
        captured = [json.loads(line) for line in (work / 'shim-requests.jsonl').read_text().splitlines()]
        output['native_to_shim'] = [{'path': row['path'], 'model': row['body'].get('model')} for row in captured]
        expected_bare = {'claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2'}
        assert expected_bare <= {r['model'] for r in output['native_to_shim']}, output
        assert not any('[1m]' in (r['model'] or '') for r in output['native_to_shim']), output
        output['boundary_observed'] = True
        output['outcome'] = 'success_with_hardening_advisory'
        (HERE / 't4-runtime.json').write_text(json.dumps(output, indent=2))
    finally:
        shim.terminate()
        shim.wait(timeout=5)
        shim_log.close()
        gateway.close()


if __name__ == '__main__':
    main()
