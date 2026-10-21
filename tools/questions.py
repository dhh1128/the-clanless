# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""The open-question queue, and the rulings that were answered and never landed.

    python3 tools/questions.py             # both halves, the second one first
    python3 tools/questions.py --open      # only what is unanswered
    python3 tools/questions.py --landed    # only the answered-but-unpropagated check

Ported from `~/code/me/cretaceous/tools/questions.py`. It reads
`plan/open-questions.md`, the invention ledgers in `plan/scene-maps/`, the `[?]`
marks in `plan/` and `kb/`, and the ruling records in `.ignored/`. Every one of
those may be absent or empty, and then the matching half prints a count of zero.

**The second half is the one that exists because of a real failure, so it
prints first.** Inherited from Cretaceous: a question sat in that repo's runbook
marked *unanswered* for five days after Daniel had answered it. The answer was
recorded, some of it was propagated, the rest was not, and the file that asks the
question never learned that it had one. A later session then re-derived the
answer from scratch and got a different one.

**An unanswered question costs a round trip. An answered one that nobody can
find costs the same round trip and his patience with it**, because he knows he
answered and cannot see why it is being asked again.

## How the landing check works, and what it cannot do

Ruling records live under `.ignored/`, which is gitignored and therefore
invisible to `corpus()` -- every other instrument in `tools/` reads
`git ls-files` and so cannot see them at all. This reads the top level of that
directory directly; subdirectories such as `.ignored/seeds/` are not rulings and
are not read.

**Only sections that actually record a decision are examined**, and that
restriction is the whole difference between an instrument and a nuisance. The
first Cretaceous version read every `##` section and reported 148 of them: an
analysis document is not a ruling, its prose was never meant to reach canon, and
a check that cannot tell them apart is one nobody will run twice. A section
qualifies on either of two marks -- a heading that opens with a decision verb, or
a body that quotes him deciding.

Within those, it takes the section's own **emphasized phrases** -- what the
record chose to bold or italicize -- and asks whether each is findable anywhere
in the tracked corpus. A ruling that landed usually left its own words
somewhere.

**That is a lead, not a verdict.** Canon routinely rephrases a ruling rather than
quoting it, so an absent phrase means *go look* rather than *this was dropped*.
The check is tuned to be noisy in the safe direction: a false positive costs one
grep, and a false negative is how five days of an answered question went missing.

## The open half

Gathers what is unanswered from the places it lives -- the register, the
scene-map invention ledgers, and the `[?]` marks -- and groups them by **whose
ground they sit on**, which is the one ordering that can be computed honestly.

**It does not rank them, and the first Cretaceous version did.** That version
scored each item by *reach*: how many tracked files mention something it names.
The number came out measuring how common the words were, so notes about cover art
outscored the scene-ledger items actually blocking work. A proxy that confident
and that wrong is worse than no proxy.

**What can be computed is the ground.** A `[?]` inside an **approved** file is
an exception sitting in settled material, so a reader standing on that page is
currently being told something the author has not agreed to -- those come
first. Everything in an unapproved file is a draft note and can wait. Scene
ledgers sort by whether the scene is mapped, because an unsettled item under a
written map is holding up prose.

**Dependency order is a reader's job and this file will not pretend
otherwise.** Nothing mechanical can see that one question's answer gates
another's; in Cretaceous both such cases were found by reading. Use this to know
what exists; use judgment to know what to ask first.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent))

from checks import ROOT, corpus  # noqa: E402

IGNORED = ROOT / ".ignored"
MAPS = "plan/scene-maps/"
REGISTER = "plan/open-questions.md"

# What a record emphasizes is what it is asserting.
EMPH = re.compile(r"\*\*(.+?)\*\*|(?<!\*)\*([^*\n]{12,}?)\*(?!\*)")
# A ledger row that has been settled is struck through or carries a provenance
# that is not an open one. Anything else is still a question.
# **A ledger row's status lives in its provenance cell, so read the cell.**
# Matching the whole row for a marker word kept getting it wrong in both
# directions: `*(delegated)*` has a parenthesis between the asterisk and the
# word, `*invented · delegated*` has another word in front of it, and `his`
# appears in ordinary prose in the item and proposal cells all day long. The
# row is a table; parse it as one.
SETTLED = re.compile(r"\b(?:his|delegated|done)\b", re.I)
LEDGER_ID = re.compile(r"^\*\*(A\d+)\*\*$")
BACKTICK = re.compile(r"`([^`\n]+)`")
PROPER = re.compile(r"\b([A-Z][a-z]{3,})\b")


def tracked_text() -> dict[str, str]:
    return {p: "\n".join(lines) for p, lines in corpus().items()}


def normalize(s: str) -> str:
    s = re.sub(r"[*`_]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


# --------------------------------------------------------------------------
# answered, and possibly never propagated
# --------------------------------------------------------------------------

# A section records a decision if it says so in its heading, or if the body
# quotes him making one. Both marks are the record's own, not this file's guess.
DECISION_HEAD = re.compile(
    r"^(approved|decided|struck|settled|also settled|locked|changed|restored"
    r"|reverted|done|ruled)\b", re.I)
ATTRIBUTED = re.compile(r"\b(his|daniel'?s) (ruling|words|answer|call)\b", re.I)


def ruling_records() -> list[tuple[str, str, list[str]]]:
    """(record, section heading, emphasized phrases) for every ruling section.

    A ruling, not an analysis. See the module docstring for why that line is
    drawn and what happens when it is not."""
    out = []
    if not IGNORED.is_dir():
        return out
    for path in sorted(IGNORED.glob("*.md")):
        lines = path.read_text(errors="replace").split("\n")
        heading, buf = None, []
        for line in lines + ["## "]:
            if line.startswith("## "):
                body = "\n".join(buf)
                if heading and buf and (DECISION_HEAD.match(heading)
                                        or ATTRIBUTED.search(body)):
                    phrases = []
                    for m in EMPH.finditer(body):
                        p = normalize(m.group(1) or m.group(2) or "")
                        if len(p.split()) >= 3 and not p.startswith("http"):
                            phrases.append(p)
                    if phrases:
                        out.append((path.name, heading, phrases))
                heading, buf = line[3:].strip(), []
            elif heading is not None:
                buf.append(line)
    return out


def unlanded() -> list[tuple[str, str, int, int, list[str]]]:
    """Ruling sections whose own emphasized phrases are missing from canon."""
    blob = "\n".join(normalize(t) for t in tracked_text().values())
    rows = []
    for record, heading, phrases in ruling_records():
        # Match a prefix, not the sentence. Canon routinely keeps a ruling's
        # opening and trims its tail -- in Cretaceous a two-clause ruling
        # landed as its first clause alone, and a whole-sentence test called
        # that a loss. Five words is long enough
        # to be distinctive and short enough to survive an edit.
        missing = [p for p in phrases
                   if " ".join(p.split()[:5]).rstrip(".,;:") not in blob]
        if missing:
            rows.append((record, heading, len(missing), len(phrases), missing))
    # **Count first, fraction second, and the order matters.** Sorting by
    # fraction put a section with three trivial phrases all missing above one
    # with nine substantial assertions missing out of thirteen -- and in
    # Cretaceous the second was the ruling this tool exists because of. What is worth a human's attention is how much is missing,
    # not what share of a short list it happens to be.
    rows.sort(key=lambda r: (-r[2], -(r[2] / r[3])))
    return rows


# --------------------------------------------------------------------------
# unanswered
# --------------------------------------------------------------------------

def open_items() -> list[tuple[str, str, str]]:
    """(where, id, raw text) for everything still open, from all four homes.

    **Raw, not normalized.** The retired `reach()` scorer read backticked paths and proper
    nouns, and `normalize()` strips the backticks and lowercases the capitals
    -- so normalizing here silently zeroed every score and sorted the queue by
    nothing at all. Normalize at the point of display and nowhere earlier."""
    items = []
    for path, lines in sorted(corpus().items()):
        for n, line in enumerate(lines, start=1):
            s = line.strip()
            if path.startswith(MAPS) and s.startswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) < 4:
                    continue
                m = LEDGER_ID.match(cells[0])
                struck = cells[1].startswith("~~")
                if m and not struck and not SETTLED.search(cells[2]):
                    items.append((f"{path}:{n}", m.group(1), cells[1]))
            elif path == REGISTER:
                # The register keeps its questions in tables, one per row,
                # with an id in the first cell. Bullets in it are commentary.
                # Either a plain id (`Q12`) or a tagged-style one (`Q-8HNV`).
                m = re.match(r"^\|\s*\**([A-Z]+\d+|[A-Z]-[0-9A-Z]{4})\**\s*\|\s*(.+?)\s*\|", s)
                if m:
                    items.append((f"{path}:{n}", m.group(1), m.group(2)))
            elif "`[?]`" in line and path.startswith(("plan/", "kb/")):
                items.append((f"{path}:{n}", "[?]", s.replace("`[?]`", "")))
    return items


def approval(path: str) -> str:
    """The file's own marker word. `AGENTS.md` §2: it lives in frontmatter."""
    lines = corpus().get(path, [])
    if len(lines) > 1:
        m = re.match(r"approval:\s*(\w+)", lines[1].strip())
        if m:
            return m.group(1)
    return "unapproved"


def mapped_scenes() -> set[str]:
    return {p[len(MAPS):-3] for p in corpus() if p.startswith(MAPS)}


def ground(where: str, ident: str) -> tuple[int, str]:
    """(band, label). Lower band is more urgent, and the reason is stated."""
    path = where.split(":")[0]
    if ident.startswith("A"):
        sid = path[len(MAPS):-3]
        return (1, f"ledger, {sid} is mapped") if sid in mapped_scenes() \
            else (3, f"ledger, {sid}")
    if ident == "[?]" and approval(path).startswith("approved"):
        return 0, "exception inside an approved file"
    if path == REGISTER:
        return 2, "the register"
    return 4, f"note in an {approval(path)} file"


def main(argv: list[str]) -> int:
    want_open = "--open" in argv or not ({"--open", "--landed"} & set(argv))
    want_landed = "--landed" in argv or not ({"--open", "--landed"} & set(argv))

    if want_landed:
        rows = unlanded()
        print(f"=== ANSWERED, AND THE ANSWER MAY NOT HAVE LANDED — {len(rows)} sections ===")
        print("A lead, not a verdict: canon rephrases. Absent means go and look.\n")
        for record, heading, n_missing, n_total, missing in rows:
            print(f"  {record} — {heading}")
            print(f"      {n_missing} of {n_total} emphasized phrases are in no tracked file")
            for p in missing[:3]:
                print(f"        · {p[:110]}")
            print()

    if want_open:
        items = open_items()
        rows = sorted((ground(w, i), w, i, normalize(x)) for w, i, x in items)
        print(f"=== OPEN — {len(items)} items ===")
        print("Grouped by whose ground each sits on. Not ranked — see the docstring.\n")
        last = None
        for (band, label), where, ident, text in rows:
            if label != last:
                shown = sum(1 for r in rows if r[0][1] == label)
                print(f"  --- {label} ({shown}) ---")
                last = label
            if band <= 2:
                print(f"    {ident:<4} {where}")
                print(f"         {text[:108]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
