import sys,os;sys.path.insert(0,'.')
from glyphs import text_path,font
MW='fonts/Merriweather-900.ttf';M7='fonts/Montserrat-700.ttf'
NAVY='#12294A';CREAM='#FCF9EF'
GOLDS={'original-gold':'#E6B262','site-gold':'#C08A2E'}
def fit(fp,text,cap_target_w,size,cx,base):
    # choose tracking so the word spans cap_target_w
    _,w0=text_path(fp,text,size,cx,base,0)
    tr=(cap_target_w-w0)/(size*(len(text)-1))
    return text_path(fp,text,size,cx,base,tr)[0]
def H(cx,top,bottom,widthscale=1.12):
    # Merriweather H scaled to height (cap height) and widened slightly like the original
    from fontTools.pens.boundsPen import BoundsPen
    f=font(MW);gs=f.getGlyphSet();n=f.getBestCmap()[ord('H')];bp=BoundsPen(gs);gs[n].draw(bp)
    x0,y0,x1,y1=bp.bounds; s=(bottom-top)/(y1-y0); sx=s*widthscale
    from fontTools.pens.svgPathPen import SVGPathPen;from fontTools.pens.transformPen import TransformPen
    pen=SVGPathPen(gs);tp=TransformPen(pen,(sx,0,0,-s,cx-(x0+x1)/2*sx,bottom+y0*s));gs[n].draw(tp);return pen.getCommands()
def rings(gold,navy,bg,outer=True):
    s=f'<circle cx="500" cy="500" r="500" fill="{bg}"/>' if bg else ''
    return s+f'<circle cx="500" cy="500" r="466" fill="none" stroke="{gold}" stroke-width="30"/><circle cx="500" cy="500" r="422" fill="none" stroke="{navy}" stroke-width="11"/>'
def badge(gold,navy=NAVY,bg=CREAM,ink=None):
    ink=ink or navy
    h=H(500,195,535,1.3)
    w1=fit(M7,'HANNIE',556,134,500,692)
    w2=fit(M7,'CONSULTANTS',556,62,500,786)
    return rings(gold,navy,bg)+f'<g fill="{ink}"><path d="{h}"/><path d="{w1}"/><path d="{w2}"/></g>'
def mark(gold,navy=NAVY,bg=CREAM,ink=None):
    ink=ink or navy
    return rings(gold,navy,bg)+f'<path fill="{ink}" d="{H(500,262,738,1.3)}"/>'
def svg(body,w=1000,h=1000,title='Hannie Consultants'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><title>{title}</title>{body}</svg>\n'
def lockup(gold,navy=NAVY,bg=CREAM,ink=None,textink=None):
    ink=ink or navy;textink=textink or navy
    m=f'<g transform="translate(0,0) scale(0.4)">{mark(gold,navy,bg,ink)}</g>'
    w1,_=text_path(M7,'HANNIE',150,0,0,0.06)
    # left-align: compute and shift
    from fontTools.pens.boundsPen import BoundsPen
    _,wa=text_path(M7,'HANNIE',150,0,0,0.06)
    a,_=text_path(M7,'HANNIE',150,460+wa/2,250,0.06)
    b=fit(M7,'CONSULTANTS',wa,66,460+wa/2,358)
    return svg(m+f'<g fill="{textink}"><path d="{a}"/><path d="{b}"/></g>',int(460+wa+20),400,'Hannie Consultants')
os.makedirs('svg',exist_ok=True)
for name,g in GOLDS.items():
    open(f'svg/hannie-consultants-badge-{name}.svg','w').write(svg(badge(g)))
    open(f'svg/hannie-consultants-mark-{name}.svg','w').write(svg(mark(g)))
    open(f'svg/hannie-consultants-lockup-{name}.svg','w').write(lockup(g))
open('svg/hannie-consultants-badge-navy-one-colour.svg','w').write(svg(badge(NAVY,NAVY,None)))
open('svg/hannie-consultants-badge-white-reversed.svg','w').write(svg(badge('#FFFFFF','#FFFFFF',None)))
print(os.listdir('svg'))
