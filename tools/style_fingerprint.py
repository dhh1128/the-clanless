# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Fingerprint Cordimancy, segmented by channel (dialogue / narration / italic) and by POV.

    python3 tools/style_fingerprint.py ~/code/me/cordimancy/cordimancy.md

Adapted from the Deep Resonance tool, which fingerprints Viking by side. Changed here: the body runs
from the line `1` (chapter one's number) to the last scene's last line, before the end matter; a
chapter starts at a bare-number line; each chapter's italic subtitle (`*topic ~ POV*`) is dropped;
SIDES assigns each scene its POV. Channel rules, sentence splitting and attribution fragments are
unchanged:
- A paragraph is one non-empty source line.
- Dialogue = text inside straight double quotes. A paragraph with an odd number of quotes leaves its
  last quote open to end of paragraph (multi-paragraph speech).
- Italic channel = `*...*` spans of three or more words outside quotes (quoted thought, Gitam's
  words). Shorter italic spans are emphasis and stay in their channel.
- Narration = what remains after removing dialogue and italic-channel spans.
- Sentences split after . ! ? or … followed by whitespace. Words = whitespace tokens.
- Attribution fragment = a narration sentence of six words or fewer, in a paragraph that carries
  dialogue, containing a speech verb (list below). Reported, but excluded from narration rates.
"""
from __future__ import annotations
import re, sys, statistics as st
from collections import Counter

# scene start line -> POV. Each scene runs to the next start. From a scene-by-scene reading of
# Cordimancy (the-clanless .ignored/hand-maps, turn 67): T = Toril, M = Malena, K = Kinora,
# O = outside narrator, G = italic scenes with Gitam, P = the tale Paka narrates.
SIDES = {
 38:'T',133:'T',199:'M',253:'T',280:'T',336:'T',411:'M',432:'M',509:'M',594:'T',701:'M',750:'T',
 762:'T',804:'T',846:'M',918:'T',949:'T',1009:'T',1040:'M',1089:'T',1133:'T',1177:'K',1259:'T',
 1274:'T',1293:'T',1341:'T',1348:'T',1374:'T',1434:'T',1467:'O',1473:'T',1517:'O',1522:'M',1555:'G',
 1577:'M',1608:'T',1656:'T',1701:'T',1716:'G',1724:'T',1746:'K',1812:'T',1849:'M',1938:'M',1954:'M',
 1984:'M',2043:'M',2118:'M',2159:'M',2258:'M',2272:'M',2327:'T',2394:'M',2411:'M',2443:'T',2487:'K',
 2529:'G',2556:'M',2588:'M',2610:'M',2636:'T',2677:'K',2712:'T',2758:'T',2782:'T',2823:'T',2840:'T',
 2852:'M',2872:'T',2900:'T',2924:'M',3002:'M',3042:'M',3115:'K',3141:'T',3244:'M',3252:'M',3321:'M',
 3392:'T',3435:'T',3485:'T',3522:'K',3551:'T',3593:'M',3644:'M',3708:'M',3803:'M',3863:'T',3899:'P',
 3997:'T',4012:'T',4062:'T',4085:'M',4148:'M',4169:'K',4214:'T',4242:'T',4253:'T',4277:'M',4333:'T',
 4363:'M',4408:'M',4449:'M',4466:'M',4552:'T',4571:'T',4653:'M',4669:'M',4686:'M',4703:'M',
}
KEYS = 'TMKOGP'
VERBS = r"said|says|asked|replied|whispered|muttered|murmured|gasped|sneered|snarled|added|began|continued|wheezed|grunted|mumbled|shouted|called|answered|offered|prodded|interpreted|responded|hissed|snapped|groaned|breathed|cried|yelled|laughed|demanded|insisted|admitted|repeated|announced|protested|agreed|suggested|explained|chuckled|sighed|croaked|rasped|wondered|growled|barked|retorted|observed|declared|stammered|blurted|exclaimed|moaned|pleaded|urged|joked|quipped|teased|cut in|went on|spoke"
VERB = re.compile(rf"\b(?:{VERBS})\b", re.I)
SENT = re.compile(r"(?<=[.!?…])\s+")
ITAL = re.compile(r"\*([^*]+)\*")
CONTR = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.I)

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
    start = next(i for i, l in enumerate(L) if l.strip() == '1')
    end = 4753  # last line of the last scene; end matter follows (cordimancy.md at 64b2f69)
    starts = sorted(SIDES)
    data = {k: dict(words=0, dw=0, iw=0, nw=0, narr=[], narr_final=[], dia=[], attrib=0, paras_n=[], paras_d=[],
                    spoken=0, said=Counter(), semi=0, colon=0, nq=0, nexcl=0, one_sent_paras=0, paras=0,
                    short_iso=0, short_final=0, short_inner=0, short_init=0, slots_final=0, slots_init=0, slots_all=0, ital_s=[], asif=0, emdash=0, ellip=0, chap=set(), exchange=[], run=0, contr=0, bare=0, beat=0, tagged=0, chapw=Counter())
            for k in KEYS}
    side = None; chap = None
    for idx in range(start, end):
        ln = idx + 1; l = L[idx]
        if re.fullmatch(r'\d+', l.strip()):
            chap = l.strip()
            for k in data:
                data[k]['exchange'].append(data[k]['run']); data[k]['run'] = 0
            continue
        if ln in SIDES: side = SIDES[ln]
        if not l.strip() or re.fullmatch(r'\*[^*]+ ~ [^*]+\*', l.strip()):
            continue
        if side is None: continue
        d = data[side]; d['chap'].add(chap)
        p = l.strip()
        nt, dia, ital = split_para(p)
        w = words(p); d['words'] += w; d['paras'] += 1
        dw = sum(words(x) for x in dia); iw = sum(words(x) for x in ital)
        d['dw'] += dw; d['iw'] += iw; d['chapw'][chap] += w
        d['contr'] += sum(len(CONTR.findall(x)) for x in dia)
        if dia:
            rest = [x for x in sents(nt)]
            if not rest: d['bare'] += 1
            elif any(VERB.search(x) and words(x) <= 10 for x in rest): d['tagged'] += 1  # a tag: speech verb in a short narration sentence
            else: d['beat'] += 1
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
        cw = sum((data[k]['chapw'] for k in keys), Counter())
        b, bt, tg = (sum(data[k][f] for k in keys) for f in ('bare','beat','tagged'))
        tot = max(1, b + bt + tg)
        print(f"  dialogue paras: bare {pct(b,tot):.0f}%, action beat only {pct(bt,tot):.0f}%, speech verb {pct(tg,tot):.0f}%; contractions/k dialogue words {1000*sum(data[k]['contr'] for k in keys)/max(1,agg['dw']):.1f}; chapter words in this segment, median {st.median(cw.values()):.0f}")
        exs = [e for e in ex if e > 0]
        if exs: print(f"  exchanges (consecutive dialogue paras): n={len(exs)} median {st.median(exs)} max {max(exs)}")
    row('WHOLE BOOK', KEYS); row('TORIL', 'T'); row('MALENA', 'M'); row('KINORA', 'K')
    row('OUTSIDE NARRATOR', 'O'); row('GITAM (italic scenes)', 'G'); row("PAKA'S TALE", 'P')

if __name__ == '__main__':
    main(sys.argv[1])
