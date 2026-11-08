import os, textwrap

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source')

# --- colour helpers (same spirit as the original's inline spans) -----------------
def D(t='**Democrats**'):   return '<span style="color: #1a5fb4;">%s</span>' % t
def R(t='**Republicans**'): return '<span style="color: #c01c28;">%s</span>' % t
def GOP(): return '<span style="color: #c01c28;">**GOP**</span>'
def DEM(): return '<span style="color: #1a5fb4;">**Democrats**</span>'
MAGA = '<span style="color: #b5651d;">**MAGA**</span>'
LEFT = '<span style="color: #26a269;">**Left**</span>'

def write(relpath, text):
    p = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text.rstrip('\n') + '\n')

def js(block):
    return '{!\n' + block.strip('\n') + '\n!}'

def card(id, title, deck, view_if, timer, intro, options, kind='card', discard=True, extra=''):
    """options: list of dicts with keys id,label,sub,choose,unavail,fx,text"""
    out = []
    out.append('title: %s' % title)
    out.append('new-page: true')
    out.append('is-card: true')
    out.append('tags: %s' % deck)
    if view_if:
        out.append('view-if: %s' % view_if)
    if timer:
        out.append('on-arrival: %s_timer = %d' % (id, timer))
    if extra:
        out.append(extra)
    out.append('')
    out.append('= %s' % title)
    out.append('')
    out.append(intro.strip())
    out.append('')
    for o in options:
        out.append('- @%s: %s' % (o['id'], o['label']))
    if discard:
        out.append('- @easy_discard')
    out.append('')
    for o in options:
        out.append('@%s' % o['id'])
        if o.get('sub'):
            out.append('subtitle: %s' % o['sub'])
        if o.get('unavail'):
            out.append('unavailable-subtitle: %s' % o['unavail'])
        if o.get('choose'):
            out.append('choose-if: %s' % o['choose'])
        fx = o.get('fx', '').strip().rstrip(';')
        fx = (fx + '; ' if fx else '') + 'month_actions += 1'
        out.append('on-arrival: %s' % fx)
        out.append('')
        out.append(o['text'].strip())
        out.append('')
    return '\n'.join(out)

def opt(id, label, fx='', text='', sub='', choose='', unavail=''):
    return dict(id=id, label=label, fx=fx, text=text, sub=sub, choose=choose, unavail=unavail)

def event(id, title, view_if, intro, options=None, fx='', priority=1, subtitle='', max_visits=1, go_to='', extra=''):
    out = ['title: %s' % title]
    if subtitle:
        out.append('subtitle: %s' % subtitle)
    out.append('new-page: true')
    out.append('tags: event')
    out.append('view-if: %s' % view_if)
    out.append('priority: %d' % priority)
    if max_visits:
        out.append('max-visits: %d' % max_visits)
    if fx:
        out.append('on-arrival: %s' % fx)
    if go_to:
        out.append('go-to: %s' % go_to)
    if extra:
        out.append(extra)
    out.append('')
    out.append('= %s' % title)
    out.append('')
    out.append(intro.strip())
    out.append('')
    if options:
        for o in options:
            out.append('- @%s: %s' % (o['id'], o['label']))
        out.append('')
        for o in options:
            out.append('@%s' % o['id'])
            if o.get('sub'):
                out.append('subtitle: %s' % o['sub'])
            if o.get('choose'):
                out.append('choose-if: %s' % o['choose'])
            if o.get('unavail'):
                out.append('unavailable-subtitle: %s' % o['unavail'])
            if o.get('fx'):
                out.append('on-arrival: %s' % o['fx'].strip().rstrip(';'))
            out.append('')
            out.append(o['text'].strip())
            out.append('')
    return '\n'.join(out)
