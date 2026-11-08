import os, re, glob, json, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_ops import tr_expr, tr_ops  # noqa (runs its own checks on import)

ROOT = os.path.join(HERE, '..', 'source')

def parse_props(lines):
    """parse leading property lines (until first blank line outside a JS block)"""
    props, i, n = {}, 0, len(lines)
    while i < n and lines[i].strip() != '' and not lines[i].startswith('='):
        m = re.match(r'^([a-z-]+):\s*(.*)$', lines[i])
        if not m:
            i += 1; continue
        key, val = m.group(1), m.group(2)
        if val.startswith('{!') and '!}' not in val:
            buf = [val]
            i += 1
            while i < n and '!}' not in lines[i]:
                buf.append(lines[i]); i += 1
            buf.append(lines[i] if i < n else '')
            val = '\n'.join(buf)
        props[key] = val
        i += 1
    return props, i

def code_of(val):
    if val is None: return ''
    if val.startswith('{!'):
        return 'JS:' + val.strip()[2:-2]
    return 'OPS:' + tr_ops(val)

scenes = []
for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.scene.dry'), recursive=True)):
    rel = os.path.relpath(f, ROOT)
    if not any(p in rel.split(os.sep) for p in ('events', 'party_affairs', 'government_affairs', 'advisors')):
        continue
    text = open(f, encoding='utf-8').read()
    base = os.path.basename(f).replace('.scene.dry', '')
    # split on subscene markers
    chunks = re.split(r'^@([A-Za-z_][A-Za-z0-9_]*)\s*$', text, flags=re.M)
    head = chunks[0].split('\n')
    props, _ = parse_props(head)
    tags = [t.strip() for t in props.get('tags', '').split(',')]
    kind = 'event' if 'event' in tags else ('card' if ('party_affairs' in tags or 'govt_affairs' in tags) else ('advisor' if 'advisor' in tags else ('shuffle' if base.startswith('shuffle') else None)))
    if not kind: continue
    opts = []
    for i in range(1, len(chunks), 2):
        oid, body = chunks[i], chunks[i + 1].lstrip('\n').split('\n')
        p, _ = parse_props(body)
        opts.append(dict(id=oid, choose=tr_expr(p['choose-if']) if 'choose-if' in p else None, code=code_of(p.get('on-arrival'))))
    scenes.append(dict(id=base, kind=kind, view=tr_expr(props['view-if']) if 'view-if' in props else 'true',
                       maxv=int(props['max-visits']) if 'max-visits' in props else 0,
                       prio=int(props.get('priority', '0')), code=code_of(props.get('on-arrival')), goto=props.get('go-to', ''), opts=opts))

js = open(os.path.join(HERE, 'sim_driver.js'), encoding='utf-8').read()
data = json.dumps(scenes)
path = os.path.join(HERE, '_sim_run.js')
open(path, 'w').write('const SCENES = %s;\n%s' % (data, js))
n = sys.argv[1] if len(sys.argv) > 1 else '60'
policy = sys.argv[2] if len(sys.argv) > 2 else 'random'
r = subprocess.run(['node', path, n, policy], capture_output=True, text=True, cwd=HERE)
print(r.stdout[-5000:]); print(r.stderr[-2500:])
os.unlink(path)
