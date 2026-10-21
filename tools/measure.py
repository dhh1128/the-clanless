# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Measure a drafted scene before Daniel reads it.

    python3 tools/measure.py content/D3.2.md [more files...]

Prints, per file: words; narration sentences of five words or fewer, as a share of
narration (target 19-22%, `prompts/style-canon.md` §0 and `AGENTS.md` §4); narration
sentences with two or more `, and` joints (budget two or three a scene,
`prompts/ai-tells-blacklist.md` §30); the count of `nobody` (§29); and manner similes,
*X does Y, the way Z* (§31, at most one a scene), listed, with *as if* / *as though* counted beside them; withheld lines,
narration reporting that someone did not speak (§32, at most one a scene), listed; and
spoken lines per thousand words (Daniel's viking runs about nineteen); the share of
words that are dialogue, and the longest exchange, counted as consecutive paragraphs
carrying speech. Those two are diagnostics and not targets: viking runs 28% dialogue,
30% in its chapters that have any, with a median longest exchange of seven paragraphs
(edition 3.3, `prompts/style-canon.md` §0; Cretaceous's copy says 34% and fifteen, which do not reproduce).
A scene whose map plans `RELATIONS` and whose talk comes out in ones and twos has not
done what the map asked (`process/methodology-theory.md` §4a).

**Narration only.** Quoted speech is removed before sentences are split, because
Daniel's dialogue runs about twice his narration's short-sentence rate and a
blended figure hides both (`AGENTS.md` §4). Attribution fragments left behind by
the removal — `said Teva.`, `he whispered.` — are not counted as short narration.

It lived in /tmp until 2026-10-09, which is reaped on this box, and the scene
procedure depends on it, so it is tracked here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SPEECH = re.compile(r'"[^"]*"')
COMMENT = re.compile(r"<!--.*?-->", re.S)
SENT = re.compile(r"(?<=[.!?])\s+")
MANNER = re.compile(r"\bthe way (?:you|a|an|people|he|she|they|it|someone|anyone|one|his|her|their|everyone|everybody|men|women|children|[A-Z][a-z]+)\b(?! (?:home|back|out|to|through|across)\b)(?!\s(?:\w+\s)?(?:had|have) (?:come|carried)\b)(?!\s(?:\w+\s)?(?:were|was) telling\b)")
WITHHELD = re.compile(r"\b(?:nobody|no one|none of them|neither of them)\b[^.]{0,40}\b(?:said|say|says|spoke|speak|talked|answered|asked|mentioned|remarked|argued)\b|\b(?:said|say) nothing\b|\bdid not say\b|\bdidn't say\b|\bnot say(?:ing)?\b|\bdid not answer\b|\bwithout a word\b|\bnothing to say\b", re.I)
ASIF = re.compile(r"\bas (?:if|though)\b", re.I)
ATTRIB = re.compile(r"^(?:\w+\s+)?(?:said|asked|whispered|breathed|called|shouted|answered)\b[^.!?]*[.!?]?$", re.I)


def measure(path: Path) -> dict:
    text = path.read_text()
    body = text.split("---", 2)[2] if text.startswith("---") else text
    body = COMMENT.sub("", body)
    words = len(body.split())
    narr = []
    for para in body.strip().split("\n\n"):
        for s in SENT.split(SPEECH.sub(" ", para).strip()):
            s = s.strip(" ,—-")
            if not s or ATTRIB.match(s):
                continue
            narr.append(s)
    short = [s for s in narr if len(s.split()) <= 5]
    paras = [p for p in body.strip().split("\n\n") if p.strip()]
    run = longest = 0
    for p in paras:
        run = run + 1 if SPEECH.search(p) else 0
        longest = max(longest, run)
    chains = [s for s in narr if s.count(", and") >= 2]
    return {
        "words": words,
        "narration": len(narr),
        "short": short,
        "chains": chains,
        "nobody": len(re.findall(r"\bnobody\b", body, re.I)),
        "manner": [s for s in SENT.split(body.replace("\n", " ")) if MANNER.search(s)],
        "asif": len(ASIF.findall(body)),
        "withheld": [s for s in SENT.split(SPEECH.sub(" ", body.replace("\n", " "))) if WITHHELD.search(s)],
        "spoken": len(SPEECH.findall(body)),
        "dialogue": sum(len(s.split()) for s in SPEECH.findall(body)),
        "exchange": longest,
    }


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[0])
        return 2
    for name in argv:
        m = measure(Path(name))
        pct = 100 * len(m["short"]) / max(1, m["narration"])
        print(f"{name}: {m['words']} words; narration ≤5 words {pct:.1f}% "
              f"({len(m['short'])}/{m['narration']}); comma-and chains {len(m['chains'])}; nobody {m['nobody']}; "
              f"the-way similes {len(m['manner'])} (max 1); as-if {m['asif']}; "
              f"withheld {len(m['withheld'])} (max 1); spoken {1000*m['spoken']/max(1,m['words']):.1f}/kw (his ~19); dialogue {100*m['dialogue']/max(1,m['words']):.0f}% (viking 28-30); longest exchange {m['exchange']} paras (viking ~7)")
        for c in m["chains"]:
            print(f"    chain: {c[:110]}")
        for s in m["manner"]:
            print(f"    the-way: {s.strip()[:110]}")
        for s in m["withheld"]:
            print(f"    withheld: {s.strip()[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
