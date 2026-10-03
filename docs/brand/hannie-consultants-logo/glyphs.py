from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer
_cache={}
def font(path, wght=None):
    k=(path,wght)
    if k not in _cache:
        f=TTFont(path)
        if 'fvar' in f and wght: f=instancer.instantiateVariableFont(f,{'wght':wght})
        _cache[k]=f
    return _cache[k]
def text_path(path, text, size, cx, baseline, tracking=0.0, wght=None):
    """Return (svg path d, width) for text centred on cx. tracking in em."""
    f=font(path,wght); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=size/upm; names=[cmap[ord(c)] for c in text]
    adv=[gs[n].width*s for n in names]
    total=sum(adv)+tracking*size*(len(text)-1)
    x=cx-total/2; d=[]
    for n,a in zip(names,adv):
        pen=SVGPathPen(gs); tp=TransformPen(pen,(s,0,0,-s,x,baseline)); gs[n].draw(tp)
        d.append(pen.getCommands()); x+=a+tracking*size
    return ' '.join(d), total
def bounds(path,text,wght=None):
    from fontTools.pens.boundsPen import BoundsPen
    f=font(path,wght);gs=f.getGlyphSet();n=f.getBestCmap()[ord(text)];bp=BoundsPen(gs);gs[n].draw(bp);return bp.bounds,f['head'].unitsPerEm
