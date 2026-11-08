import os, re, glob, json, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', 'source')
KW = {'and': '&&', 'or': '||', 'not': '!', 'true': 'true', 'false': 'false'}

def tr_expr(e):
    parts = re.split(r'("[^"]*")', e)
    out = []
    for p in parts:
        if p.startswith('"'):
            out.append(p); continue
        p = re.sub(r'(?<![<>!=])=(?!=)', '==', p)
        p = re.sub(r'[A-Za-z_][A-Za-z0-9_]*', lambda m: KW.get(m.group(0), 'Q.' + m.group(0)), p)
        out.append(p)
    return ''.join(out)

def tr_ops(line):
    js = []
    for stmt in line.split(';'):
        stmt = stmt.strip()
        if not stmt: continue
        body, _, cond = stmt.partition(' if ')
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(\+=|-=|\*=|/=|=)\s*(.+)$', body)
        s = 'Q.%s %s %s;' % (m.group(1), m.group(2), tr_expr(m.group(3)))
        if cond: s = 'if (%s) { %s }' % (tr_expr(cond), s)
        js.append(s)
    return ' '.join(js)

def main():
    items = []   # (file, label, kind, code)
    for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.scene.dry'), recursive=True)):
        t = open(f, encoding='utf-8').read()
        rel = os.path.relpath(f, ROOT)
        # JS blocks that are on-arrival (not text injection)
        for m in re.finditer(r'^on-arrival: \{!(.*?)^!\}', t, re.M | re.S):
            items.append((rel, 'js', m.group(1)))
        for m in re.finditer(r'^on-arrival:[ ]*(?!\{!)(.*)$', t, re.M):
            if m.group(1).strip() and not m.group(1).strip().startswith('{!'):
                items.append((rel, 'ops', tr_ops(m.group(1))))
        for m in re.finditer(r'^(view-if|choose-if):\s*(.*)$', t, re.M):
            items.append((rel, 'expr', tr_expr(m.group(2))))
        for m in re.finditer(r'^go-to:\s*(.*)$', t, re.M):
            for part in m.group(1).split(';'):
                _, _, cond = part.strip().partition(' if ')
                if cond: items.append((rel, 'expr', tr_expr(cond)))
        t2 = re.sub(r'\{!.*?!\}', '', t, flags=re.S)
        for m in re.finditer(r'\[\?\s*if\s+(.*?)\s*:', t2):
            items.append((rel, 'expr', tr_expr(m.group(1))))

    lines = ["global.window = undefined;", "require('./sd_lib.js');", "const SD = global.SD;",
             "function fresh(mode){ const Q = {}; SD.init(Q); SD.refresh(Q); if (mode==='mid'){ Q.year=2021; Q.month=6; Q.time=90; Q.dem_president=0; Q.president_party='R'; Q.maga_strength=55; Q.farright_strength=22; Q.farleft_strength=25; Q.left_relation=30; Q.subversion_progress=9.95; SD.refresh(Q);} return Q; }",
             "const fakeThis = { achieve(){}, game:{scenes:{}}, state:{qualities:{}, currentHands:{main:[]}, visits:{}, lastPlayedCard:{id:'x'}}, _compileChoices(){ return [{title:'Continue...'}]; } };",
             "const dendryUI = {dendryEngine:{state:{qualities:{}}}};",
             "let bad = 0, n = 0;",
             "function chk(Q, label){ for (const k in Q){ const v = Q[k]; if (typeof v === 'number' && !isFinite(v)) { console.log('NaN/Inf', k, 'after', label); bad++; } } }"]
    for i, (rel, kind, code) in enumerate(items):
        label = json.dumps('%s [%s #%d]' % (rel, kind, i))
        for mode in ('start', 'mid'):
            if kind == 'js':
                body = 'fakeThis.state.qualities = Q; (function(){ %s }).call(fakeThis);' % code
                lines.append('try { const Q = fresh("%s"); %s chk(Q, %s); n++; } catch (e) { console.log("EXC", %s, e.message); bad++; }' % (mode, body, label, label))
            elif kind == 'ops':
                lines.append('try { const Q = fresh("%s"); %s chk(Q, %s); n++; } catch (e) { console.log("EXC", %s, e.message); bad++; }' % (mode, code, label, label))
            else:
                lines.append('try { const Q = fresh("%s"); const r = (%s); if (typeof r === "undefined") { console.log("UNDEF", %s); bad++; } n++; } catch (e) { console.log("EXC", %s, e.message); bad++; }' % (mode, code, label, label))
    lines.append('console.log("checked", n, "snippets; problems:", bad);')
    path = os.path.join(HERE, '_ops_test.js')
    open(path, 'w').write('\n'.join(lines))
    r = subprocess.run(['node', path], capture_output=True, text=True, cwd=HERE)
    print(r.stdout[-6000:]); print(r.stderr[-1500:])
    os.unlink(path)


if __name__ == '__main__':
    main()
