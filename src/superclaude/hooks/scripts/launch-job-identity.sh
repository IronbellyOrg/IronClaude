#!/bin/bash
# Linux same-user job identity, not a sandbox or controller-PID binding.
# prepare SESSION COMMAND [TOOL_USE_ID] prints a single-use token; run TOKEN
# waits for the main bash AND ordinary non-zombie descendants, returning bash's
# status. identify [PID] prints governed/ordinary/unknown, never command text.
# Release is deletion of sessions/SESSION; malformed live state is unknown.
# shortcut: deliberate setsid/daemonization escapes selection; upgrade to OS
# containment if hostile isolation is required. Killing the supervisor leaves
# unknown stale state, not trusted human identity. Monitor/pipelines unsupported.
# With no arguments, adapt documented PreToolUse Bash JSON on stdin only.
# The hook emits execute SESSION TOOL_ID_OR_EMPTY COMMAND, never a ticket.
# Accepted execution creates and immediately consumes one private request.
# Unverifiable/oversized envelopes are unsupported, not proof of human identity.
# updatedInput replaces the WHOLE input; omit permissionDecision so ordinary
# permission checks still apply. Other hooks' rewrite ordering is unspecified.
# Each call uses a fresh bash: cd is local, and completion waits for ordinary
# background descendants. Always use an explicit cwd/cd in each governed call;
# persistent Claude Bash cwd tracking and live auto-mode rewrites need Task4.
# Missing ordinary state must not require UV or create any launch state.
if [[ $# == 0 || ( $# == 1 && $1 == hook ) ]]; then
    if [[ -z ${HOME:-} || ! -e "$HOME/.claude/state/launch-level" && ! -L "$HOME/.claude/state/launch-level" ]]; then
        exit 0
    fi
fi
if ! command -v uv >/dev/null 2>&1; then
    if [[ $# == 0 || ( $# == 1 && $1 == hook ) ]]; then
        # A stale store is not binding authority. With no Python runtime, jq
        # may establish only an exact top-level Bash session and owned record.
        # No parser means unavailable adaptation, never proof of a human actor.
        command -v jq >/dev/null 2>&1 || exit 0
        fallback_sid=$(jq -ers '
            select(length == 1) | .[0] | select(type == "object") |
            select(.tool_name == "Bash") | .session_id |
            select(type == "string") |
            select(test("\\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\\z"))
        ' 2>/dev/null) || exit 0
        [[ ${HOME:-} == /* ]] || exit 0
        fallback_dir=${HOME%/}
        [[ -d $fallback_dir && -O $fallback_dir ]] || exit 0
        ancestor=$fallback_dir
        while [[ -n $ancestor && $ancestor != / ]]; do
            [[ ! -L $ancestor ]] || exit 0
            ancestor=${ancestor%/*}
        done
        for part in .claude state launch-level sessions; do
            fallback_dir=$fallback_dir/$part
            [[ -d $fallback_dir && -O $fallback_dir && ! -L $fallback_dir ]] || exit 0
        done
        fallback_record=$fallback_dir/$fallback_sid
        [[ -f $fallback_record && -O $fallback_record && ! -L $fallback_record ]] || exit 0
    fi
    printf '%s\n' 'launch job: UV is required for this invocation' >&2
    exit 2
fi
IFS= read -r -d '' launch_identity_code <<'PY'
import ctypes
try:
    import fcntl
except ImportError:
    fcntl = None
import json
import os
import re
import shlex
import signal
import stat
import sys
import time
import uuid

LIMIT = 65536
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z')
TOKEN = re.compile(r'[0-9a-f]{32}\Z')
LEVELS = {b'worktree', b'full', b'full-submit'}


def valid_id(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None


def private(st, directory=False):
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if not kind(st.st_mode) or st.st_uid != os.geteuid() or st.st_mode & 0o077:
        raise ValueError('unsafe state')


def directory(parts):
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in parts:
            if part in ('', '.', '..'):
                raise ValueError('invalid state path')
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise


def store():
    home = os.environ.get('HOME', '')
    if not home.startswith('/'):
        raise ValueError('invalid home')
    fd = directory(home.strip('/').split('/'))
    try:
        st = os.fstat(fd)
        if st.st_uid != os.geteuid() or st.st_mode & 0o022:
            raise ValueError('unsafe home')
        for name in ('.claude', 'state', 'launch-level'):
            nxt = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
            st = os.fstat(fd)
            if st.st_uid != os.geteuid() or st.st_mode & 0o022:
                raise ValueError('unsafe store')
        private(st, True)
        return fd
    except BaseException:
        os.close(fd)
        raise


def subdir(root, name, create=False):
    if create:
        try:
            os.mkdir(name, 0o700, dir_fd=root)
        except FileExistsError:
            pass
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
    try:
        private(os.fstat(fd), True)
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_file(parent, name, consume=False):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    try:
        if consume:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        st = os.fstat(fd)
        private(st)
        if st.st_nlink != 1 or st.st_size > LIMIT:
            raise ValueError('invalid state file')
        data = os.read(fd, LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('oversized state')
        if consume:
            current = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if (st.st_dev, st.st_ino) != (current.st_dev, current.st_ino):
                raise ValueError('changed request')
            os.unlink(name, dir_fd=parent)
        return data
    finally:
        os.close(fd)


def publish(parent, name, value):
    tmp = '.' + uuid.uuid4().hex
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(json.dumps(value, separators=(',', ':')).encode())
            out.flush()
            os.fchmod(out.fileno(), 0o400)
        os.link(tmp, name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
    finally:
        os.unlink(tmp, dir_fd=parent)


def governed(root, sid):
    if not valid_id(sid):
        raise ValueError('invalid session')
    fd = subdir(root, 'sessions')
    try:
        data = read_file(fd, sid)
        if data not in LEVELS and not (data.endswith(b'\n') and data[:-1] in LEVELS):
            raise ValueError('invalid level')
    finally:
        os.close(fd)


def request(value):
    if not isinstance(value, dict) or set(value) != {'session_id', 'tool_use_id', 'command'}:
        raise ValueError('invalid request')
    if not valid_id(value['session_id']):
        raise ValueError('invalid session')
    if value['tool_use_id'] is not None and not valid_id(value['tool_use_id']):
        raise ValueError('invalid tool identity')
    command = value['command']
    if not isinstance(command, str) or '\0' in command or len(command.encode()) > 32768:
        raise ValueError('invalid command')
    return value


def proc(pid):
    if type(pid) is not int or pid <= 0:
        raise ValueError('invalid process')
    with open('/proc/%d/stat' % pid) as source:
        fields = source.read().rsplit(')', 1)[1].split()
    return fields[0], int(fields[3]), int(fields[19])


def boot():
    with open('/proc/sys/kernel/random/boot_id') as source:
        return str(uuid.UUID(source.read().strip()))


def identify(pid):
    root = None
    jobs = None
    try:
        _, sid, _ = proc(pid)
        try:
            root = store()
            jobs = subdir(root, 'jobs')
            raw = read_file(jobs, str(sid) + '.json')
        except FileNotFoundError:
            return {'status': 'ordinary'}
        value = json.loads(raw)
        if not isinstance(value, dict) or set(value) != {'pid', 'start', 'boot', 'kernel_sid', 'session_id'}:
            raise ValueError('invalid record')
        if type(value['pid']) is not int or value['pid'] != sid or type(value['kernel_sid']) is not int or value['kernel_sid'] != sid:
            raise ValueError('invalid supervisor')
        if type(value['start']) is not int or not valid_id(value['session_id']):
            raise ValueError('invalid identity')
        state, actual_sid, start = proc(value['pid'])
        if state == 'Z' or actual_sid != sid or start != value['start'] or boot() != value['boot']:
            raise ValueError('stale supervisor')
        if os.stat('/proc/%d' % sid).st_uid != os.geteuid():
            raise ValueError('foreign supervisor')
        try:
            governed(root, value['session_id'])
        except FileNotFoundError:
            return {'status': 'ordinary', 'reason': 'released'}
        return {'status': 'governed', 'session_id': value['session_id']}
    except (OSError, ValueError, IndexError, TypeError, RecursionError, AttributeError):
        return {'status': 'unknown'}
    finally:
        for fd in (jobs, root):
            if fd is not None:
                os.close(fd)


def members(sid):
    found = []
    # No bounded ancestry walk or truncated scan is interpreted as ordinary.
    for name in os.listdir('/proc'):
        if not name.isdecimal() or int(name) == os.getpid():
            continue
        try:
            state, current, start = proc(int(name))
        except FileNotFoundError:
            continue
        except ProcessLookupError:
            continue
        if current == sid and state != 'Z':
            found.append((int(name), start))
    return found


def forward(live, sid, signum):
    libc = ctypes.CDLL(None, use_errno=True)
    for pid, start in live:
        fd = -1
        try:
            # Pin the process before checking: PID reuse cannot hit outsiders.
            # Some UV Python builds omit os.pidfd_open; libc provides it.
            fd = libc.pidfd_open(pid, 0)
            if fd < 0:
                raise OSError(ctypes.get_errno(), 'process handle unavailable')
            state, current, actual = proc(pid)
            if current == sid and actual == start and state != 'Z':
                if libc.pidfd_send_signal(fd, signum, None, 0) < 0:
                    raise OSError(ctypes.get_errno(), 'process signal failed')
        except ProcessLookupError:
            pass
        except FileNotFoundError:
            pass
        finally:
            if fd >= 0:
                os.close(fd)


def supervise(value, jobs, old_mask):
    os.setsid()
    sid = os.getpid()
    # Linux prctl.h: PR_SET_CHILD_SUBREAPER = 36; adopted orphans can be reaped.
    if ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
        raise OSError('subreaper unavailable')
    _, kernel_sid, start = proc(sid)
    forward([(sid, start)], sid, 0)  # verify pidfd support before any command
    record = {'pid': sid, 'start': start, 'boot': boot(), 'kernel_sid': kernel_sid,
              'session_id': value['session_id']}
    name = str(sid) + '.json'
    pending = []
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
        signal.signal(sig, lambda signum, frame: pending.append(signum))
    publish(jobs, name, record)
    shell = None
    status = None
    deadline = None
    try:
        signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        if pending:
            return 128 + pending[0]
        shell = os.fork()
        if shell == 0:
            for name in ('SIGINT', 'SIGTERM', 'SIGHUP', 'SIGQUIT', 'SIGPIPE', 'SIGXFZ', 'SIGXFSZ'):
                if hasattr(signal, name):
                    signal.signal(getattr(signal, name), signal.SIG_DFL)
            try:
                os.execv('/bin/bash', ['bash', '-c', value['command']])
            except OSError:
                os._exit(126)
        while True:
            while True:
                try:
                    child, code = os.waitpid(-1, os.WNOHANG)
                except ChildProcessError:
                    break
                if child == 0:
                    break
                if child == shell:
                    status = os.waitstatus_to_exitcode(code)
            live = members(sid)
            if pending:
                forward(live, sid, pending.pop(0))
                deadline = time.monotonic() + 1 if deadline is None else deadline
            if deadline is not None and time.monotonic() >= deadline:
                forward(live, sid, signal.SIGKILL)
            if status is not None and not live:
                return status if status >= 0 else 128 - status
            time.sleep(0.03)
    finally:
        # Only this job's session is ever signalled, including error cleanup.
        try:
            forward(members(sid), sid, signal.SIGKILL)
            # Reap even children that became zombies during the final scan.
            until = time.monotonic() + 2
            while time.monotonic() < until:
                try:
                    child, _ = os.waitpid(-1, os.WNOHANG)
                except ChildProcessError:
                    break
                if child == 0:
                    if not members(sid):
                        break  # intentionally detached children are unsupported
                    time.sleep(0.03)
        finally:
            # Failed cleanup retains stale evidence: survivors select unknown.
            if not members(sid):
                os.unlink(name, dir_fd=jobs)


def run(token):
    if not TOKEN.fullmatch(token):
        raise ValueError('invalid token')
    root = store()
    requests = subdir(root, 'requests')
    jobs = None
    try:
        value = request(json.loads(read_file(requests, token, consume=True)))
        governed(root, value['session_id'])
        jobs = subdir(root, 'jobs', True)
        # Block cancellation until both sides have installed their handlers.
        signals = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT)
        old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, signals)
        # A dedicated child always can setsid, even when the caller is a leader.
        child = os.fork()
        if child == 0:
            try:
                code = supervise(value, jobs, old_mask)
            except (OSError, ValueError, IndexError, TypeError, RecursionError, AttributeError):
                print('launch job: supervisor failed', file=sys.stderr)
                code = 2
            os._exit(code)
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
            def relay(signum, frame):
                try:
                    os.kill(child, signum)
                except ProcessLookupError:
                    pass
            signal.signal(sig, relay)
        signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        _, code = os.waitpid(child, 0)
        result = os.waitstatus_to_exitcode(code)
        return result if result >= 0 else 128 - result
    finally:
        for fd in (jobs, requests, root):
            if fd is not None:
                os.close(fd)


def json_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate JSON field')
        value[key] = item
    return value


def json_constant(value):
    raise ValueError('non-JSON constant')


def hook():
    # Parse enough for a bounded, positively identified size error. Beyond this
    # hard cap no identity is inferred; arbitrary text never supplies authority.
    raw = sys.stdin.buffer.read((1 << 20) + 1)
    if len(raw) > 1 << 20:
        return 0
    try:
        event = json.loads(raw)
    except (ValueError, RecursionError):
        return 0
    if not isinstance(event, dict):
        return 0
    tool = event.get('tool_name')
    if isinstance(tool, str) and tool != 'Bash':
        return 0  # Monitor and other named tools have no adapter here
    sid = event.get('session_id')
    if not valid_id(sid):
        return 0  # do not guess from agent_id, parent fields, cwd or environment
    home = os.environ.get('HOME', '')
    if not home.startswith('/'):
        return 0
    path = os.path.join(home, '.claude', 'state', 'launch-level', 'sessions', sid)
    if not os.path.lexists(path):
        return 0
    # Existence is only a reason to validate or block, never rewrite authority.
    root = None
    try:
        root = store()
        governed(root, sid)
        json.loads(raw, object_pairs_hook=json_object, parse_constant=json_constant)
        if tool != 'Bash' or event.get('hook_event_name') != 'PreToolUse':
            raise ValueError('unsupported bound event')
        if len(raw) > LIMIT:
            raise ValueError('oversized bound event')
        for field in ('agent_id', 'agent_type'):
            if field in event and not isinstance(event[field], str):
                raise ValueError('unsupported subagent shape')
        inputs = event.get('tool_input')
        if not isinstance(inputs, dict):
            raise ValueError('invalid tool input')
        value = request({'session_id': sid, 'tool_use_id': event.get('tool_use_id'),
                         'command': inputs.get('command')})
        script = os.path.realpath(sys.argv[1])
        # Reserve runner invocations, without pretending shlex parses Bash.
        reserved = re.escape(os.path.basename(script)) + r'''[\x27\x22]?(?:\s+(?:run|hook|execute)(?:\s|$)|\s*$)'''
        if re.search(reserved, value['command']):
            raise ValueError('conflicting job wrapper')
        if sys.platform != 'linux' or fcntl is None:
            raise ValueError('unsupported platform')
        _, kernel_sid, start = proc(os.getpid())
        boot()
        forward([(os.getpid(), start)], kernel_sid, 0)
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:
            raise OSError('subreaper unavailable')
        if not os.path.isfile(script) or not os.access(script, os.R_OK):
            raise ValueError('runner unavailable')
        if not os.access('/bin/bash', os.X_OK):
            raise ValueError('startup dependency unavailable')
        # No ticket exists during permission evaluation. Only accepted execution
        # enters execute(), which creates and immediately consumes its request.
        command = shlex.join(['/bin/bash', script, 'execute', sid,
                              value['tool_use_id'] or '', value['command']])
        updated = dict(inputs)
        updated['command'] = command
        output = json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PreToolUse', 'updatedInput': updated,
            'additionalContext': 'Launch identity: this call uses a fresh Bash shell and waits for ordinary background descendants. Internal cd does not persist to later Bash calls; use an explicit working directory in each call. Normal permission checks still apply; concurrent hook rewrite ordering and live auto-mode behavior are unverified.'}})
        print(output, flush=True)
        return 0
    except (OSError, ValueError, IndexError, TypeError, RecursionError, AttributeError):
        print('launch job: governed Bash call cannot be wrapped safely', file=sys.stderr)
        return 2
    finally:
        if root is not None:
            os.close(root)


def execute(sid, tool_id, command):
    value = request({'session_id': sid, 'tool_use_id': tool_id or None, 'command': command})
    root = store()
    requests = None
    published = False
    token = uuid.uuid4().hex
    try:
        governed(root, sid)
        requests = subdir(root, 'requests', True)
        def cancel(signum, frame):
            raise SystemExit(128 + signum)
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
            signal.signal(sig, cancel)
        old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT))
        try:
            publish(requests, token, value)
            published = True
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
        return run(token)
    finally:
        try:
            if published:
                try:
                    os.unlink(token, dir_fd=requests)
                except FileNotFoundError:
                    pass  # run consumed it already
        finally:
            for fd in (requests, root):
                if fd is not None:
                    os.close(fd)


def main(args):
    if not args or args == ['hook']:
        return hook()
    if len(args) == 4 and args[0] == 'execute':
        return execute(*args[1:])
    if args and args[0] == 'identify' and len(args) in (1, 2):
        try:
            pid = os.getpid() if len(args) == 1 else int(args[1])
            result = identify(pid)
        except ValueError:
            result = {'status': 'unknown'}
        print(json.dumps(result))
        return 0
    if args and args[0] == 'prepare' and len(args) in (3, 4):
        value = request({'session_id': args[1], 'command': args[2],
                         'tool_use_id': args[3] if len(args) == 4 else None})
        root = store()
        requests = None
        try:
            governed(root, value['session_id'])
            requests = subdir(root, 'requests', True)
            token = uuid.uuid4().hex
            publish(requests, token, value)
            print(token)
            return 0
        finally:
            for fd in (requests, root):
                if fd is not None:
                    os.close(fd)
    if len(args) == 2 and args[0] == 'run':
        return run(args[1])
    raise ValueError('invalid invocation')


try:
    sys.exit(main(sys.argv[2:]))
except (OSError, ValueError, IndexError, TypeError, RecursionError, AttributeError):
    # Do not echo exceptions: file names and JSON can contain command secrets.
    print('launch job: invalid invocation or unavailable private state', file=sys.stderr)
    sys.exit(2)
PY
exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"
