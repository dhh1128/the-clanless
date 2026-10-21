# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Fingerprint Viking, segmented by channel (dialogue / narration / italic speech) and by side.

    python3 tools/style_fingerprint.py ~/code/me/viking/viking.md

Method (also described in `prompts/style-canon.md` §0):
- Body = from the `## 1` heading to the line before `### About the Author`. Headings and `§` lines dropped.
- A paragraph is one non-empty source line.
- Dialogue = text inside straight double quotes. A paragraph with an odd number of quotes leaves its
  last quote open to end of paragraph (multi-paragraph speech).
- Italic channel = `*...*` spans of three or more words outside quotes (implant speech, quoted thought,
  pufferbelly speech). Shorter italic spans are emphasis and stay in their channel.
- Narration = what remains after removing dialogue and italic-channel spans.
- Sentences split after . ! ? or … followed by whitespace. Words = whitespace tokens.
- Attribution fragment = a narration sentence of six words or fewer, in a paragraph that carries
  dialogue, containing a speech verb (list below). Reported, but excluded from narration rates.
- Sides assigned per scene by reading (SIDES below): E = Erisa, human POV; T = Earth;
  P = pufferbelly (1291) POV; F = Julie inside Rafa's feed (Earth body, Erisa senses).
"""
from __future__ import annotations
import re, sys, statistics as st
from collections import Counter

# scene start line -> side. Each scene runs to the next start or chapter end.
SIDES = {
 22:'E',98:'E',226:'T',244:'T',266:'T',358:'T',396:'T',420:'T',530:'E',568:'E',600:'E',718:'E',
 784:'T',956:'T',972:'E',1028:'E',1084:'E',1118:'T',1206:'E',1254:'P',1286:'T',1390:'E',1524:'E',
 1550:'E',1590:'E',1646:'T',1716:'T',1762:'E',1840:'F',1888:'T',2010:'T',2114:'T',2158:'T',2198:'T',
 2276:'T',2314:'E',2488:'E',2554:'E',2628:'E',2656:'T',2934:'P',2948:'E',3038:'E',3246:'E',3502:'T',
 3774:'E',3886:'E',3918:'T',3988:'T',4052:'T',4108:'P',4130:'E',4184:'E',4280:'E',4360:'E',4440:'T',
 4550:'T',4626:'T',4726:'T',4848:'E',4874:'E',4928:'E',4966:'T',5018:'E',5072:'E',5170:'T',5282:'E',
 5510:'T',5548:'E',5668:'E',5696:'P',5744:'E',5820:'T',5848:'T',5868:'T',5978:'E',6002:'E',6036:'E',
 6076:'E',6088:'E',6106:'E',6142:'T',6166:'E',6196:'E',6216:'E',6232:'E',6268:'P',6294:'T',6330:'T',
 6344:'T',6358:'E',6398:'E',6492:'T',6518:'E',
}
VERBS = r"said|says|asked|replied|whispered|muttered|murmured|gasped|sneered|snarled|added|began|continued|wheezed|grunted|mumbled|shouted|called|answered|offered|prodded|interpreted|responded|hissed|snapped|groaned|breathed|cried|yelled|laughed|demanded|insisted|admitted|repeated|announced|protested|agreed|suggested|explained|chuckled|sighed|croaked|rasped|wondered|growled|barked|retorted|observed|declared|stammered|blurted|exclaimed|moaned|pleaded|urged|joked|quipped|teased|cut in|went on|spoke"
VERB = re.compile(rf"\b(?:{VERBS})\b", re.I)
SENT = re.compile(r"(?<=[.!?…])\s+")
ITAL = re.compile(r"\*([^*]+)\*")

def words(s): return len(s.split())

def split_para(p):
    """Return (narration_text, [dialogue segments], [italic segments])."""
    # dialogue
    parts = p.split('"')
    narr, dia = [], []
    for i, seg in enumerate(parts):
        (dia if i % 2 else narr).append(seg)
    # odd quote count: last segment after an opening quote is already in dia by parity
    narr_text = ' '.join(narr)
    ital = []
    def sub(m):
        if words(m.group(1)) >= 3:
            ital.append(m.group(1)); return ' '
        return m.group(1)
    narr_text = ITAL.sub(sub, narr_text)
    dia = [ITAL.sub(lambda m: m.group(1), d) for d in dia if d.strip()]
    merged = []
    for d in dia:
        if merged and not re.search(r"[.!?…]['’]?\s*$", merged[-1].strip()):
            merged[-1] = merged[-1].rstrip() + ' ' + d.strip()
        else:
            merged.append(d)
    dia = merged
    return narr_text, dia, ital

def sents(text):
    out = []
    for s in SENT.split(text.strip()):
        s = s.strip(" ,;—-*")
        if s and re.search(r"\w", s): out.append(s)
    return out

def main(path):
    L = open(path).read().split('\n')
    start = next(i for i, l in enumerate(L) if l.strip() == '## 1')
    end = next(i for i, l in enumerate(L) if l.startswith('### About the Author'))
    starts = sorted(SIDES)
    data = {k: dict(words=0, dw=0, iw=0, nw=0, narr=[], narr_final=[], dia=[], attrib=0, paras_n=[], paras_d=[],
                    spoken=0, said=Counter(), semi=0, colon=0, nq=0, nexcl=0, one_sent_paras=0, paras=0,
                    short_iso=0, short_final=0, short_inner=0, short_init=0, slots_final=0, slots_init=0, slots_all=0, ital_s=[], asif=0, emdash=0, ellip=0, chap=set(), exchange=[], run=0)
            for k in 'ETPF'}
    side = None; chap = None
    for idx in range(start, end):
        ln = idx + 1; l = L[idx]
        if l.startswith('## '):
            chap = l[3:]
            for k in data:
                data[k]['exchange'].append(data[k]['run']); data[k]['run'] = 0
            continue
        if ln in SIDES: side = SIDES[ln]
        if not l.strip() or l.strip() == '§':
            continue
        if side is None: continue
        d = data[side]; d['chap'].add(chap)
        p = l.strip()
        nt, dia, ital = split_para(p)
        w = words(p); d['words'] += w; d['paras'] += 1
        dw = sum(words(x) for x in dia); iw = sum(words(x) for x in ital)
        d['dw'] += dw; d['iw'] += iw
        d['spoken'] += len(dia)
        d['emdash'] += p.count('—'); d['ellip'] += p.count('…')
        if dia or ital:
            d['run'] += 1
        else:
            d['exchange'].append(d['run']); d['run'] = 0
        for x in dia:
            d['dia'] += [words(s) for s in sents(x)]
        ns = sents(nt)
        kept = []
        for s in ns:
            if dia and words(s) <= 6 and VERB.search(s):
                d['attrib'] += 1
                for v in VERB.findall(s): d['said'][v.lower()] += 1
                continue
            kept.append(s)
        if kept:
            nw = sum(words(s) for s in kept); d['nw'] += nw
            d['narr'] += [words(s) for s in kept]
            d['semi'] += nt.count(';'); d['colon'] += nt.count(':')
            d['nq'] += sum(s.endswith('?') for s in kept); d['nexcl'] += sum(s.endswith('!') for s in kept)
            d['asif'] += len(re.findall(r"\bas (?:if|though)\b", nt, re.I))
            if len(kept) > 1:
                d['slots_all'] += len(kept); d['slots_final'] += 1; d['slots_init'] += 1
            for j, s in enumerate(kept):
                if words(s) <= 5:
                    if len(kept) == 1: d['short_iso'] += 1
                    elif j == len(kept) - 1: d['short_final'] += 1
                    elif j == 0: d['short_init'] += 1
                    else: d['short_inner'] += 1
        for x in ital:
            d['ital_s'] += [words(s) for s in sents(x)]
        if not dia and not ital:
            d['paras_n'].append(w)
            if len(kept) == 1: d['one_sent_paras'] += 1
        elif dia:
            d['paras_d'].append(w)
    for k in data: data[k]['exchange'].append(data[k]['run'])

    def row(name, keys):
        agg = {}
        for f in ['words','dw','iw','nw','attrib','spoken','semi','colon','nq','nexcl','one_sent_paras','paras','short_iso','short_final','short_inner','short_init','slots_final','slots_init','slots_all','asif','emdash','ellip']:
            agg[f] = sum(data[k][f] for k in keys)
        narr = sum((data[k]['narr'] for k in keys), []); dia = sum((data[k]['dia'] for k in keys), [])
        pn = sum((data[k]['paras_n'] for k in keys), []); pd = sum((data[k]['paras_d'] for k in keys), [])
        said = sum((data[k]['said'] for k in keys), Counter())
        ex = sum((data[k]['exchange'] for k in keys), [])
        chaps = set().union(*(data[k]['chap'] for k in keys))
        allsent = narr + dia
        pct = lambda a, b: 100 * a / max(1, b)
        nshort = sum(x <= 5 for x in narr)
        print(f"\n### {name}  ({len(chaps)} chapters touched)")
        print(f"words {agg['words']}; dialogue {pct(agg['dw'],agg['words']):.1f}%; italic channel {pct(agg['iw'],agg['words']):.1f}%; narration {pct(agg['nw'],agg['words']):.1f}%")
        print(f"spoken segments/kw {1000*agg['spoken']/agg['words']:.1f}; attribution fragments {agg['attrib']} ({1000*agg['attrib']/agg['words']:.1f}/kw); top tags {said.most_common(8)}")
        for lab, xs in (('narration', narr), ('dialogue', dia), ('blended', allsent)):
            if not xs: continue
            print(f"  {lab:9} n={len(xs):5} mean {st.mean(xs):5.1f} median {st.median(xs):4.1f} <=5 {pct(sum(x<=5 for x in xs),len(xs)):5.1f}% >=30 {pct(sum(x>=30 for x in xs),len(xs)):4.1f}%")
        print(f"  narration <=5 incl. attribution: {pct(nshort+agg['attrib'], len(narr)+agg['attrib']):.1f}%")
        print(f"  short narration position: isolated(1-sentence para) {agg['short_iso']}, final {agg['short_final']}, initial {agg['short_init']}, middle {agg['short_inner']}; chance share of final slots in multi-sentence paras {pct(agg['slots_final'],agg['slots_all']):.1f}%, observed {pct(agg['short_final'],agg['short_final']+agg['short_init']+agg['short_inner']):.1f}%")
        it = sum((data[k]['ital_s'] for k in keys), [])
        if it: print(f"  italic-channel n={len(it)} mean {st.mean(it):.1f} median {st.median(it)} <=5 {pct(sum(x<=5 for x in it),len(it)):.1f}%")
        print(f"  narration-only paras n={len(pn)} mean {st.mean(pn):.1f} median {st.median(pn)}; one-sentence {pct(agg['one_sent_paras'],len(pn)):.1f}%")
        if pd: print(f"  dialogue-bearing paras n={len(pd)} mean {st.mean(pd):.1f} median {st.median(pd)}")
        print(f"  narration ; : {agg['semi']}:{agg['colon']}; narration ? {agg['nq']} ({1000*agg['nq']/max(1,agg['nw']):.1f}/k narr words); ! {agg['nexcl']}; as-if/though {agg['asif']}; em-dash/kw {1000*agg['emdash']/agg['words']:.1f}; ellipsis/kw {1000*agg['ellip']/agg['words']:.1f}")
        exs = [e for e in ex if e > 0]
        if exs: print(f"  exchanges (consecutive dialogue paras): n={len(exs)} median {st.median(exs)} max {max(exs)}")
    row('WHOLE BOOK', 'ETPF'); row('ERISA (human POV)', 'E'); row('EARTH', 'T'); row('PUFFERBELLY', 'P'); row('FEED (ch17)', 'F')

if __name__ == '__main__':
    main(sys.argv[1])
