import os, re, sys, subprocess, tempfile, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source')
files = sorted(glob.glob(os.path.join(ROOT, '**', '*.dry'), recursive=True))
errors, warns = [], []

def err(f, msg): errors.append('%s: %s' % (os.path.relpath(f, ROOT), msg))

# ---------------------------------------------------------------- known variables
lib = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sd_lib.js'), encoding='utf-8').read()
known = set(re.findall(r'Q\.([A-Za-z_][A-Za-z0-9_]*)\s*=', lib))
classes = ['working', 'suburban', 'educated', 'rural', 'minority', 'young']
parties = ['dem', 'gop', 'left', 'farright', 'nonvote']
factions = ['progressive', 'establishment', 'labor', 'moderate', 'abundance', 'populist']
for c in classes:
    known.add(c)
    for p in parties:
        known.add('%s_%s' % (c, p))
for f in factions:
    known |= {f + '_strength', f + '_dissent'}
timers = re.search(r"Q\.timers = \[(.*?)\];", lib, re.S).group(1)
for t in re.findall(r"'([a-z_]+)'", timers):
    known.add(t + '_timer')
for b in ['blue_core', 'rust_belt', 'heartland_swing', 'sun_belt', 'red_core']:
    known |= {b + '_lean', b + '_margin', 'el_' + b}
for p in ['dem', 'gop', 'left', 'farright']:
    known |= {p + '_votes', p + '_normalized'}
for m in ['month', 'year', 'time']:
    known.add(m)
dry_text = {f: open(f, encoding='utf-8').read() for f in files}
for f, t in dry_text.items():
    known |= set(re.findall(r'Q\.([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|\+=|-=)', t))
    for m in re.finditer(r'^on-arrival:\s*(?!\{!)(.*)$', t, re.M):
        for stmt in m.group(1).split(';'):
            mm = re.match(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:\+|-|\*|/)?=', stmt)
            if mm: known.add(mm.group(1))
    for m in re.finditer(r'^on-arrival: \{!(.*?)^!\}', t, re.M | re.S):
        known |= set(re.findall(r'Q\.([A-Za-z_][A-Za-z0-9_]*)', m.group(1)))
known |= set(re.findall(r'Q\.([A-Za-z_][A-Za-z0-9_]*)', lib))
derived = set()
for k in list(known):
    derived |= {k + '_r', k + '_n', k + '_d', k + '_2'}
known |= derived
KW = {'and', 'or', 'not', 'if', 'true', 'false', 'D', 'R'}
adv_flags = set()

def idents(expr):
    expr = re.sub(r'"[^"]*"', '', expr)
    return {w for w in re.findall(r'[A-Za-z_][A-Za-z0-9_]*', expr) if w not in KW}

def check_expr(f, ctx, expr):
    for w in idents(expr):
        if w not in known:
            err(f, 'unknown variable "%s" in %s: %s' % (w, ctx, expr.strip()[:90]))

# ---------------------------------------------------------------- scenes & structure
scene_ids = set(); tags = set(); children = {}
for f, t in dry_text.items():
    base = os.path.basename(f).replace('.scene.dry', '').replace('.qdisplay.dry', '').replace('.dry', '')
    if f.endswith('.scene.dry'):
        scene_ids.add(base); children[base] = set()
        for m in re.finditer(r'^@([A-Za-z_][A-Za-z0-9_]*)\s*$', t, re.M):
            scene_ids.add('%s.%s' % (base, m.group(1))); children[base].add(m.group(1))
        for m in re.finditer(r'^tags:\s*(.*)$', t, re.M):
            tags |= {x.strip() for x in m.group(1).split(',')}
BUILTIN = {'backSpecialScene', 'root.start'}
all_top = {i for i in scene_ids if '.' not in i}

def resolve(f, owner, target):
    if target in BUILTIN or target in scene_ids: return True
    if '%s.%s' % (owner, target) in scene_ids: return True
    return False

for f, t in dry_text.items():
    if not f.endswith('.scene.dry'): continue
    owner = os.path.basename(f).replace('.scene.dry', '')
    # JS blocks
    for i, m in enumerate(re.finditer(r'\{!(.*?)!\}', t, re.S)):
        code = m.group(1)
        if '<p class' in code or '</p>' in code or '<div' in code or '</div>' in code:
            continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tf:
            tf.write('(function(Q,window,document,dendryUI,toggleNews){\n' + code + '\n});')
            path = tf.name
        r = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        os.unlink(path)
        if r.returncode != 0:
            err(f, 'JS syntax error in block %d: %s' % (i, r.stderr.strip().splitlines()[-3:] if r.stderr else ''))
    # strip JS blocks for text-level checks
    t2 = re.sub(r'\{!.*?!\}', '{!JS!}', t, flags=re.S)
    if t2.count('[?') != t2.count('?]'):
        err(f, 'unbalanced [? ?]: %d vs %d' % (t2.count('[?'), t2.count('?]')))
    if t2.count('[+') != t2.count('+]'):
        err(f, 'unbalanced [+ +]: %d vs %d' % (t2.count('[+'), t2.count('+]')))
    for lineno, line in enumerate(t2.splitlines(), 1):
        m = re.match(r'^-\s+@([A-Za-z_][A-Za-z0-9_.]*)', line)
        if m and not resolve(f, owner, m.group(1)):
            err(f, 'line %d: choice target not found: @%s' % (lineno, m.group(1)))
        m = re.match(r'^-\s+#([A-Za-z_][A-Za-z0-9_]*)', line)
        if m and m.group(1) not in tags:
            err(f, 'line %d: no scene has tag #%s' % (lineno, m.group(1)))
        m = re.match(r'^go-to:\s*(.*)$', line)
        if m:
            for part in m.group(1).split(';'):
                tgt, _, cond = part.strip().partition(' if ')
                tgt = tgt.strip()
                if tgt and not resolve(f, owner, tgt) and tgt != 'jumpScene':
                    err(f, 'line %d: go-to target not found: %s' % (lineno, tgt))
                if cond: check_expr(f, 'go-to', cond)
        m = re.match(r'^(view-if|choose-if):\s*(.*)$', line)
        if m: check_expr(f, m.group(1), m.group(2))
        m = re.match(r'^on-arrival:\s*(.*)$', line)
        if m and not m.group(1).startswith('{!'):
            for stmt in m.group(1).split(';'):
                stmt = stmt.strip()
                if not stmt: continue
                body, _, cond = stmt.partition(' if ')
                mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(\+=|-=|\*=|/=|=)\s*(.+)$', body)
                if not mm:
                    err(f, 'line %d: bad op statement: %s' % (lineno, stmt)); continue
                check_expr(f, 'on-arrival rhs', mm.group(3))
                if cond: check_expr(f, 'on-arrival cond', cond)
        for mm in re.finditer(r'\[\?\s*if\s+(.*?)\s*:', line):
            check_expr(f, 'text cond', mm.group(1))
        for mm in re.finditer(r'\[\+\s*([A-Za-z_][A-Za-z0-9_]*)(?:\s*:\s*([A-Za-z_]+))?\s*\+\]', line):
            if mm.group(1) not in known: err(f, 'unknown variable in [+ +]: %s' % mm.group(1))
    # every non-special scene must have a title
    if not re.search(r'^title:', t, re.M): err(f, 'missing title')

# sanity: card ids and timers
for f, t in dry_text.items():
    base = os.path.basename(f).replace('.scene.dry', '')
    if re.search(r'^is-card: true', t, re.M) and re.search(r'^tags: (party_affairs|govt_affairs)', t, re.M):
        if (base + '_timer') not in known: err(f, 'card has no timer variable %s_timer' % base)

print('files checked:', len(files), '| scenes:', len(scene_ids))
for w in warns: print('WARN', w)
if errors:
    print('ERRORS (%d):' % len(errors))
    for e in errors[:80]: print(' ', e)
    sys.exit(1)
print('OK: no errors')
