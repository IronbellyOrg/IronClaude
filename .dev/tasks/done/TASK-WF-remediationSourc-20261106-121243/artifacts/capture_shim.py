"""Run the unchanged repository shim, recording the native HTTP body before routing."""
import io
import json
import os
from pathlib import Path
import runpy
import sys

skill = Path(os.environ['CCSESSION_DIR'])
sys.path.insert(0, str(skill))
module = runpy.run_path(str(skill / 'local-gateway-alias-proxy.py'))
Handler = module['Handler']
original = Handler.do_POST


def capture(self):
    body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
    with open(os.environ['BOUNDARY_CAPTURE'], 'a') as log:
        log.write(json.dumps({'path': self.path, 'body': json.loads(body)}) + '\n')
    self.rfile = io.BytesIO(body)
    return original(self)


Handler.do_POST = capture
server = module['ThreadingServer'](module['LISTEN'], Handler)
server.serve_forever()
