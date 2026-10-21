# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Consistency checks over the Deep Resonance corpus.

Every check is a plain function taking no arguments and returning a list of
Violations. The pytest suite in test_consistency.py is a thin front end over these;
report.py is a second front end that emits a markdown change set.

Ported from `~/code/me/cretaceous/tools/checks.py`, keeping the checks that say
nothing about Cretaceous's world and leaving out the ones that do (its calendar,
its species allocation, its scene-list entry format, its ladders, its epigraphs).
`tools/README.md` lists what was dropped and why. Where a docstring tells an
incident, the incident happened in Cretaceous and is the reason the check exists;
it is kept because that reasoning is what stops a later session deleting the check.

Two rules govern what may be written here, and both exist because the Cretaceous
corpus was damaged by their opposites:

1. A check asserts a RELATIONSHIP, never a VALUE. "Every scene a pointer names
   exists" is a check. "The ship is 40 m long" is a second copy of canon wearing a
   test costume, and it would freeze an unapproved number into a new authority.
   The only literals permitted are spelling blacklists and the shapes of citations.

2. Anything the corpus declares about itself is read FROM the corpus at runtime --
   the scene-id scheme from AGENTS.md §5, the retired claims from AGENTS.md §7, the
   closed vocabulary list's location from AGENTS.md §5, the scope of
   `categorical_uncited` from its own rule block. A check that hardcodes one of
   those is the seventh copy of a fact, and it will drift.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories whose contents are working notes or machinery, not corpus.
SKIP_DIRS = {".ignored", ".git", "tools"}

# Drafts kept as evidence of what was written, never as a place anyone navigates
# from. Neither directory exists yet; the exemptions cost nothing until one does.
EVIDENCE_DIRS = ("content/superseded/", "content/rejected/")

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}


@dataclass(frozen=True)
class Violation:
    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


# --------------------------------------------------------------------------
# corpus loading
# --------------------------------------------------------------------------

@cache
def tracked_md() -> tuple[str, ...]:
    """Tracked markdown only. **An untracked file is invisible to every check**, so
    `git add` a new map or layer before trusting a green run on it -- the suite
    comes back falsely green on anything git does not know about."""
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return tuple(p for p in out
                 if not any(p.startswith(d + "/") for d in SKIP_DIRS)
                 and (ROOT / p).is_file())


@cache
def corpus() -> dict[str, list[str]]:
    """path -> list of lines, 0-indexed (so line numbers are index + 1)."""
    return {p: (ROOT / p).read_text(encoding="utf-8").splitlines() for p in tracked_md()}


def lines_of(path: str) -> list[str]:
    return corpus().get(path, [])


def iter_lines():
    for path, lines in corpus().items():
        for i, line in enumerate(lines, start=1):
            yield path, i, line


def section(path: str, heading_re: str, lines: list[str] | None = None) -> list[tuple[int, str]]:
    """Lines of the section whose heading matches, up to the next heading of the
    same or shallower depth. Returns (line_number, text) pairs."""
    lines = lines_of(path) if lines is None else lines
    start = depth = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#+)\s", line)
        if start is None:
            if m and re.search(heading_re, line):
                start, depth = i, len(m.group(1))
        elif m and len(m.group(1)) <= depth:
            return [(n + 1, lines[n]) for n in range(start + 1, i)]
    if start is None:
        return []
    return [(n + 1, lines[n]) for n in range(start + 1, len(lines))]


def table_rows(body: list[tuple[int, str]]) -> list[tuple[int, list[str]]]:
    """Markdown table rows in a section, minus header and separator.

    Assumes one table per section: everything before the last separator is
    discarded. Use `tables` where a section may hold several."""
    rows = []
    for n, line in body:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            rows = []           # separator: everything before it was the header
            continue
        rows.append((n, cells))
    return rows


def tables(body: list[tuple[int, str]]) -> list[list[tuple[int, list[str]]]]:
    """Every markdown table in a section, separately.

    `table_rows` keeps only the rows after the last separator it sees, so a second
    table later in a section silently shadows the first. In Cretaceous that made
    the figure register read as empty the moment a second table was added."""
    out, rows = [], []
    for n, line in body:
        if not line.strip().startswith("|"):
            if rows:
                out.append(rows)
                rows = []
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            rows = []
            continue
        rows.append((n, cells))
    if rows:
        out.append(rows)
    return out


def plain(cell: str) -> str:
    return re.sub(r"[*`]", "", cell).strip()


# --------------------------------------------------------------------------
# what the corpus declares about itself, parsed rather than restated here
# --------------------------------------------------------------------------

AGENTS = "AGENTS.md"


@cache
def british_spellings() -> dict[str, str]:
    """British -> American, from tools/british-english.txt. Vendored, with a LOCAL
    block of overrides that survives a refresh.

    Inherited from Cretaceous, where this replaced a hand-written list of 25 words
    in AGENTS.md. That list caught recurrences and nothing else: every word on it
    was there because someone had already made the mistake, which is why a file
    named `humour-plan.md` sat in that tree for days. A real difference list
    catches a first occurrence."""
    pairs, allowed = {}, set()
    for line in (ROOT / "tools" / "british-english.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("!"):
            allowed.add(line[1:].split()[0].lower())
        elif line and not line.startswith("#") and "\t" in line:
            b, a = line.split("\t", 1)
            pairs[b.lower()] = a.strip()
    return {b: a for b, a in pairs.items() if b not in allowed}


SCHEME_CLAIM = re.compile(r"@WF-scene\.id\.scheme\b")
EXAMPLE_ID = re.compile(r"`([A-Za-z]*\d+(?:\.\d+)+)`")


@cache
def scene_id_pattern() -> tuple[str, int] | None:
    """(regex source for one scene id, AGENTS.md line) from AGENTS.md §5, or None.

    The scheme is declared once, on the line carrying the `@WF-scene.id.scheme`
    claim, with a worked example in backticks -- `07.2` here, `D2.3` in
    Cretaceous. The pattern is generalized from the example's shape: letters stay
    literal, a zero-padded digit run keeps its width, any other digit run is
    `\\d+`. So `07.2` gives two-digit chapter, any scene; `D2.3` gives `D`, any
    day, any scene. Nothing in this file names either scheme.

    Cretaceous hardcoded `D\\d+\\.\\d+` in five checks, and it is the reason this
    function exists: a scheme hardcoded here is a second copy that a renumber
    cannot see."""
    for n, line in enumerate(lines_of(AGENTS), start=1):
        if not SCHEME_CLAIM.search(line):
            continue
        m = EXAMPLE_ID.search(line)
        if not m:
            return None
        parts = []
        for tok in re.findall(r"[A-Za-z]+|\d+|\.", m.group(1)):
            if tok == ".":
                parts.append(r"\.")
            elif tok.isdigit():
                parts.append(rf"\d{{{len(tok)}}}" if len(tok) > 1 and tok.startswith("0") else r"\d+")
            else:
                parts.append(re.escape(tok))
        return "".join(parts), n
    return None


def scene_address() -> re.Pattern | None:
    """A scene id, optionally followed by `.<move>`.

    The trailing guard must NOT reject a following period, or an address at the
    end of a sentence is invisible -- `07.2.` would pass while `see 07.2` fails.
    Cretaceous hit that hole twice in one day and lost eighteen references to it.
    Reject only a following digit, which is what distinguishes a move from a full
    stop."""
    decl = scene_id_pattern()
    if decl is None:
        return None
    return re.compile(rf"(?<![\w.])({decl[0]})(?:\.(\d{{1,3}}))?(?![\w])(?!\.\d)")


# --------------------------------------------------------------------------
# pointers resolve
# --------------------------------------------------------------------------

FILE_REF = re.compile(r"`([\w./~-]+\.md)`")


def _on_disk(ref: str) -> Path | None:
    """A reference that names its file by absolute or home path, resolved on disk."""
    if ref.startswith(("/", "~")):
        return Path(os.path.expanduser(ref))
    return None


@cache
def external_names() -> frozenset[str]:
    """Basenames of files outside the repo that the corpus cites by full path.

    Cretaceous hardcoded `viking.md` and `cordimancy.md`. Here the corpus says it
    instead: once some file cites `~/code/me/viking/viking.md` and that file exists,
    a bare `viking.md` elsewhere is a pointer to it. The cost is a loophole -- a bare
    name meaning a local file that happens to share a basename with a cited
    external one will resolve -- and that is cheaper than a hand-kept list."""
    out = set()
    for _, _, line in iter_lines():
        for ref in FILE_REF.findall(line):
            p = _on_disk(ref)
            if p is not None and p.is_file():
                out.add(p.name)
    return frozenset(out)


def check_file_refs() -> list[Violation]:
    """Every file the corpus points at exists.

    Inherited from Cretaceous, where thirteen pointers survived into files deleted
    in a restructure, and each still read as authority. A reference by absolute
    or home path is resolved on disk, because this repo cites its parent project
    and the published book by path, and a moved file there dangles here just as
    surely. A bare name resolves to a tracked file anywhere in the repo, or to an
    external file the corpus cites by full path elsewhere."""
    known = set(tracked_md()) | {Path(p).name for p in tracked_md()} | external_names()
    out = []
    for path, n, line in iter_lines():
        for ref in FILE_REF.findall(line):
            p = _on_disk(ref)
            if p is not None:
                if not p.is_file():
                    out.append(Violation(path, n, f"points at `{ref}`, which does not exist"))
                continue
            if ref in known or Path(ref).name in known:
                continue
            out.append(Violation(path, n, f"points at `{ref}`, which does not exist"))
    return out


SECTION_REF = re.compile(r"`([\w./~-]+\.md)`\s*(?:§|section\s*)(\d+(?:\.\d+)?)")


def check_section_refs() -> list[Violation]:
    """Every `file.md` §N citation resolves to a heading numbered N in that file.

    Inherited from Cretaceous, where renumbering one file's sections silently
    broke four citations and nobody noticed for a day. External files cited by
    full path are read from disk."""
    by_name = {Path(p).name: p for p in tracked_md()}
    out = []
    for path, n, line in iter_lines():
        for ref, num in SECTION_REF.findall(line):
            p = _on_disk(ref)
            if p is not None:
                if not p.is_file():
                    continue                  # check_file_refs owns that failure
                target_lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            else:
                target = by_name.get(Path(ref).name) if ref not in corpus() else ref
                if target is None:
                    continue                  # check_file_refs owns that failure
                target_lines = lines_of(target)
            # Headings are variously "## 1. Title" and "### **1.2 Title**", so strip
            # emphasis before matching.
            heads = "\n".join(re.sub(r"[*_]", "", l) for l in target_lines if l.startswith("#"))
            if not re.search(rf"^#+\s*{re.escape(num)}[.\s]", heads, re.M):
                out.append(Violation(path, n, f"cites `{ref}` section {num}, which has no such heading"))
    return out


# --------------------------------------------------------------------------
# approval is recorded in exactly one place
# --------------------------------------------------------------------------

FRONTMATTER = re.compile(r"^approval: (unapproved|(?:provisional|approved) [0-9a-f]{8})$")


def _body(text: str) -> str:
    """Everything after the frontmatter block, normalized for trailing whitespace."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 8)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    return "\n".join(l.rstrip() for l in lines).strip()


def body_hash(text: str) -> str:
    """Eight hex characters over the body, ignoring the frontmatter and trailing space.

    The marker carries this instead of a date. A date had day granularity, which
    this work defeats routinely, and it had to be typed and bumped by hand. A hash
    is written by tooling, is exact, survives any reformat of the frontmatter, and
    makes staleness a comparison rather than an argument about commit ordering.
    Re-approval is expressible, which a bare `approved` marker could not do:
    approved-to-approved is a no-op and git cannot see it."""
    return hashlib.sha256(_body(text).encode("utf-8")).hexdigest()[:8]


def check_frontmatter() -> list[Violation]:
    """Every file carries one of exactly three approval values (AGENTS.md §2).

    The scheme is worthless if a file can quietly carry no marker."""
    out = []
    for path, lines in corpus().items():
        if len(lines) < 3 or lines[0] != "---":
            out.append(Violation(path, 1, "no frontmatter block"))
            continue
        if not FRONTMATTER.match(lines[1]):
            out.append(Violation(path, 2, f"approval line is {lines[1]!r}; must be unapproved, "
                                          "or approved/provisional plus an eight-character body hash"))
    return out


def check_approval_not_stale() -> list[Violation]:
    """A file whose body no longer hashes to what its marker records has changed
    since Daniel read it. No git, no dates, and uncommitted edits are visible.

    Three designs in Cretaceous, and the first two both asked chronological
    questions and got the wrong answer. A hand-written date has day granularity,
    and that corpus was written, approved and committed inside one day. Commit
    ordering then counted a formatting migration as an edit to every approved file
    at once. A hash is a comparison: immune to reformats, immune to commit churn,
    and it sees uncommitted edits, which neither chronological version could."""
    out = []
    for path, lines in corpus().items():
        if len(lines) < 2:
            continue
        m = re.match(r"^approval: (?:approved|provisional) ([0-9a-f]{8})$", lines[1])
        if not m:
            continue
        now = body_hash((ROOT / path).read_text(encoding="utf-8"))
        if now != m.group(1):
            out.append(Violation(path, 2, f"body is {now}; the marker records {m.group(1)}"))
    return out


# A claim phrase, not the bare word: "is approved", "are recent and unapproved",
# "is itself unapproved". This deliberately misses "No approved prose exists yet"
# and "four [provisional] names", which are not claims about a file's marker --
# and it will also miss a trailing "Both are unapproved" that names its files a
# sentence earlier. A narrower net with no false alarms beats a wider one nobody
# trusts; see tools/README.md.
APPROVAL_WORD = re.compile(
    r"\b(?:is|are|was|were|remains?|stays?|both are|it is|itself)\s+(?:\w+\s+){0,3}(?:un)?approved\b",
    re.I)


def check_approval_stated_once() -> list[Violation]:
    """A file's approval state is stated in its own frontmatter and nowhere else.

    Inherited from Cretaceous, whose README carried a second copy and was wrong
    about five files. This check exists so the copy does not come back."""
    names = {Path(p).name for p in tracked_md()} | set(tracked_md())
    out = []
    for path, n, line in iter_lines():
        if path == AGENTS or n <= 3:
            continue              # AGENTS.md defines the scheme; line 2 is the marker itself
        if not APPROVAL_WORD.search(line):
            continue
        # A file named by full path lives in another repo, and its approval state is
        # that repo's business -- this corpus cannot hold a second copy of it.
        named = [r for r in FILE_REF.findall(line)
                 if _on_disk(r) is None and (r in names or Path(r).name in names)]
        if named:
            out.append(Violation(path, n, f"states an approval state for {', '.join(named)}; "
                                          "the frontmatter of that file is the only place it belongs"))
    return out


def check_dated_provenance() -> list[Violation]:
    """Knowledge files carry what is true, not how it got approved (AGENTS.md §2).

    No dates, no "Daniel's ruling", no "struck on". The pattern deliberately does
    not match the bare name, because "that is a note for Daniel, not a license"
    is instruction, not history. Only `plan/` and `kb/` are knowledge files; the
    method files in `process/` legitimately carry their own history. Dates in
    `kb/research/` are skipped, because there a date is a fact about the world --
    when a standard was published, when a preprint was withdrawn -- not a record
    of approval; the phrases still count there. It exempts only the frontmatter
    fence."""
    pattern = re.compile(
        r"\b(20\d{2}-\d{2}-\d{2}"
        r"|Daniel(?:'s)?\s+(?:ruling|approval|correction|decision)"
        r"|(?:struck|approved|reverted|added|removed|moved)\s+(?:on|in)\s+20\d{2})", re.I)
    out = []
    for path, n, line in iter_lines():
        if not (path.startswith("plan/") or path.startswith("kb/")):
            continue
        if n <= 3:
            continue
        for m in pattern.finditer(line):
            if path.startswith("kb/research/") and m.group(0)[:2] == "20":
                continue
            out.append(Violation(path, n, f"dated provenance in a knowledge file: {m.group(0)!r}"))
    return out


# --------------------------------------------------------------------------
# house style
# --------------------------------------------------------------------------

def check_us_english() -> list[Violation]:
    """US English everywhere, in prose and in filenames (AGENTS.md §5).

    Filenames count: in Cretaceous `plan/humour-plan.md` survived for days because
    this check only ever read line content. A blockquote is exempt, because it is a
    verbatim quotation -- the style canon is built from passages of Daniel's own
    novels, and correcting one would falsify the source."""
    spellings = british_spellings()
    pattern = re.compile(rf"\b({'|'.join(sorted(spellings, key=len, reverse=True))})\b", re.I)
    out = []
    for path in corpus():
        for m in pattern.finditer(Path(path).name.replace("-", " ")):
            out.append(Violation(path, 1, f"British spelling in the filename: "
                                          f"{m.group(0)!r} → {spellings[m.group(0).lower()]!r}"))
    for path, n, line in iter_lines():
        if line.lstrip().startswith(">"):
            continue
        for m in pattern.finditer(line):
            out.append(Violation(path, n, f"{m.group(0)!r} → {spellings[m.group(0).lower()]!r}"))
    return out


CLOSED_CLAIM = re.compile(r"@WF-lingo\.closed\s*:\s*true", re.I)


@cache
def closed_list_path() -> str | None:
    """The closed vocabulary list's path, from the AGENTS.md line declaring it closed."""
    for line in lines_of(AGENTS):
        if CLOSED_CLAIM.search(line):
            refs = FILE_REF.findall(line)
            if refs:
                return refs[0]
    return None


_NUM = "|".join(list(NUMBER_WORDS) + [r"\d+"])
_TERMS = r"(?:terms?|words?|entries|items|nouns)"
# A count is a number attached to the list's unit word, near "closed", on either
# side: *a closed list of sixteen terms*, *the sixteen-word closed list*.
# Cretaceous matched any number word within forty characters after "closed", and
# here that fired on the first line it met -- *a closed list for them is worth
# having from day one*. The unit word is what makes a number a count.
CLOSED_COUNT = (
    re.compile(rf"closed\D{{0,40}}?\b({_NUM})[\s-]+(?:\w+[\s-]+)?{_TERMS}\b", re.I),
    re.compile(rf"\b({_NUM})[\s-]+(?:\w+[\s-]+)?{_TERMS}\b\D{{0,20}}?closed", re.I),
)


def check_closed_list_uncounted() -> list[Violation]:
    """Nobody states how many terms the closed vocabulary holds.

    The terms are canon; the count is incidental. In Cretaceous four files carried
    a number that had been wrong since the list was created -- `git show` returned
    sixteen at every commit that ever touched it. A fact nothing depends on is a
    fact that only drifts, so the number is deleted rather than corrected. Which
    file is the closed list is read from the AGENTS.md line carrying the
    `@WF-lingo.closed` claim."""
    path = closed_list_path()
    if path is None:
        return []
    stem = Path(path).stem
    out = []
    for p, n, line in iter_lines():
        if stem not in line and p != path:
            continue
        for pattern in CLOSED_COUNT:
            for m in pattern.finditer(line):
                out.append(Violation(p, n, f"states a count for the closed list ({m.group(1)}); "
                                           "the list is closed, and its length is nobody's business"))
    return out


# --------------------------------------------------------------------------
# rule blocks -- see tools/RULES.md
# --------------------------------------------------------------------------

SHAPES = {
    "cardinality": "Every {every} has {has}.",
    "uniqueness": "No {every} appears in more than one {has}.",
    "bijection": "Every {every} has a matching {has}, and every {has} a matching {every}.",
    "membership": "Every {every} is drawn from {has}.",
    "ordering": "Every {every} comes before {has}.",
}
REQUIRED = ("id", "shape", "every", "has", "evidence", "status")
RULE_BLOCK = re.compile(r"^```rule\n(.*?)^```", re.M | re.S)


@dataclass(frozen=True)
class Rule:
    file: str
    line: int
    fields: dict[str, str]

    @property
    def id(self) -> str:
        return self.fields.get("id", "<no id>")

    @property
    def ratified(self) -> bool:
        return self.fields.get("status", "").startswith("ratified")

    def render(self) -> str:
        tmpl = SHAPES.get(self.fields.get("shape", ""))
        try:
            body = tmpl.format(**self.fields) if tmpl else "<unrenderable: unknown shape>"
        except KeyError as e:
            body = f"<unrenderable: no {e.args[0]!r} field>"
        return f"**{self.id}** — {body} *({self.fields.get('status', '?')})*"


@cache
def rules() -> tuple[Rule, ...]:
    found = []
    for path, lines in corpus().items():
        text = "\n".join(lines)
        for m in RULE_BLOCK.finditer(text):
            line = text[: m.start()].count("\n") + 1
            fields = {}
            for raw in m.group(1).splitlines():
                if ":" in raw:
                    k, v = raw.split(":", 1)
                    fields[k.strip()] = v.strip()
            found.append(Rule(path, line, fields))
    return tuple(found)


def check_rules_wellformed() -> list[Violation]:
    """Every rule block parses, carries the required fields, uses a known shape, has a
    unique id, has evidence, and -- if ratified -- names a checker that exists.

    Daniel ratifies; a session that ratifies its own rule has rebuilt the trapdoor
    the approval frontmatter had. A rule with no evidence is a guideline and must
    not become a test (`tools/RULES.md`)."""
    out, seen = [], {}
    for r in rules():
        for key in REQUIRED:
            if key not in r.fields:
                out.append(Violation(r.file, r.line, f"rule {r.id}: no {key!r} field"))
        if r.fields.get("shape") not in SHAPES:
            out.append(Violation(r.file, r.line, f"rule {r.id}: unknown shape {r.fields.get('shape')!r}"))
        if r.id in seen:
            out.append(Violation(r.file, r.line, f"rule id {r.id!r} is already used at {seen[r.id]}"))
        seen[r.id] = f"{r.file}:{r.line}"
        if not r.fields.get("evidence"):
            out.append(Violation(r.file, r.line, f"rule {r.id}: no evidence, so it is a guideline and must not be a test"))
        if r.ratified and r.fields.get("check") not in CHECKS:
            out.append(Violation(r.file, r.line, f"rule {r.id} is ratified but its checker {r.fields.get('check')!r} does not exist"))
    return out


# --------------------------------------------------------------------------
# retired claims — a ruling that is not checkable is a ruling that gets re-made
# --------------------------------------------------------------------------

RETIRED_EXEMPT_FILES = (AGENTS,)


@cache
def retired_claims() -> tuple[tuple[str, str], ...]:
    """(phrase, what is true instead), read from AGENTS.md §7's table at runtime."""
    out = []
    for _, cells in table_rows(section(AGENTS, r"Retired claims")):
        if len(cells) >= 2 and cells[0].startswith("`"):
            out.append((plain(cells[0]), plain(cells[1])))
    return tuple(out)


def _phrase_pattern(phrase: str) -> re.Pattern:
    """Case-insensitive, and bounded at any end that is a word character.

    Cretaceous matched substrings. That was safe for its phrases, which were long;
    this table starts with a four-letter given name, and a substring match on
    `Lena` fires on *Helena* and *plenary*. A boundary at a word-character end
    loses nothing real -- *Lena's* still matches."""
    lead = r"\b" if phrase[:1].isalnum() or phrase[:1] == "_" else ""
    tail = r"\b" if phrase[-1:].isalnum() or phrase[-1:] == "_" else ""
    return re.compile(lead + re.escape(phrase) + tail, re.I)


def check_retired_claims() -> list[Violation]:
    """No tracked file states a claim Daniel has retired.

    The failure this exists for is not that a ruling is ignored -- it is that a
    ruling is *applied by memory*, across many files, and memory misses some. In
    Cretaceous five rulings made in one sitting were still contradicted in live
    plan files hours later, two of them in files the session believed it had fixed.

    A line carrying `[retired]` is exempt, which is how a file cites a retired
    claim in order to correct it. Per line, so a paragraph cannot be quietly
    excused. AGENTS.md is exempt because the table must name what it forbids, and
    drafts kept as evidence are exempt because rewording one would falsify the
    record."""
    claims = [(phrase, instead, _phrase_pattern(phrase)) for phrase, instead in retired_claims()]
    out = []
    for path, n, line in iter_lines():
        if path in RETIRED_EXEMPT_FILES or path.startswith(EVIDENCE_DIRS):
            continue
        if "[retired]" in line:
            continue
        for phrase, instead, pat in claims:
            if pat.search(line):
                out.append(Violation(path, n, f"retired: {phrase!r} — {instead[:88]}"))
    return out


# --------------------------------------------------------------------------
# inline claims: the prose declares what it asserts, and two values collide
# --------------------------------------------------------------------------

# `WF-` for world fact. Two letters, because when a letter is contested between
# id spaces both sides take two letters: seeing a bare `C` you do not know which
# space you are in until the second character, and that is the whole objection.
CLAIM = re.compile(r"<!--\s*@(WF-[a-z][a-z0-9_.]*)\s*:\s*([^>]*?)\s*-->", re.I)


def check_claims_agree() -> list[Violation]:
    """No claim key is asserted with two different values anywhere in the corpus.

    **This is the detector for the class the other instruments cannot reach:
    two positive assertions that are each well-formed and jointly false.** The
    figures register finds a number repeated across files; the retired-claims
    table finds a phrase that may no longer appear. Neither can see *the mill
    turns* against *there is no mill*, because one side carries no number and
    neither side is a banned phrase.

    **The trick is that nothing has to be recognized.** An annotation means the
    prose *declares* its own claim, so the check collects keys and reports any key
    holding two values. Extraction was the whole difficulty and this removes it.

    **Why inline rather than a register file.** A register restates what a
    sentence says, and Cretaceous deleted six files that restated other files,
    because a second copy drifts and then a drafter believes whichever one they
    read last. An annotation lives on the line it describes, so a rewrite that
    contradicts it appears in the same diff as the rewrite.

    **The one real hazard: an annotation that lies is worse than none**, because
    it reads as authoritative and the check will happily agree with it. So they
    stay tiny, they stay adjacent, and they never carry anything the sentence
    beside them does not already say. Key by the proposition, never by the
    number."""
    seen: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    for path, n, line in iter_lines():
        for m in CLAIM.finditer(line):
            seen[m.group(1).lower()].append((path, n, m.group(2)))
    out = []
    for key, sites in sorted(seen.items()):
        values = {v for _, _, v in sites}
        if len(values) > 1:
            where = "; ".join(f"{p}:{n} says {v!r}" for p, n, v in sites)
            out.append(Violation(*sites[0][:2], f"@{key} is asserted {len(values)} ways — {where}"))

    # A mistyped key does not collide; it becomes a new key with one value and
    # passes. There is no registry of keys on purpose -- a registry means two edits
    # per claim, at exactly the moment the thing has to be frictionless -- so
    # instead any two keys within one character of each other are reported as
    # probably one key.
    keys = sorted(seen)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if abs(len(a) - len(b)) > 1 or a == b:
                continue
            diff = sum(1 for x, y in zip(a, b) if x != y) if len(a) == len(b) else 1
            if len(a) != len(b):
                short, long = (a, b) if len(a) < len(b) else (b, a)
                diff = 0 if any(long[:j] + long[j + 1:] == short for j in range(len(long))) else 2
            if diff <= 1:
                out.append(Violation(*seen[b][0][:2],
                                     f"@{b} is one character from @{a}; one of them is a typo"))
    return out


# --------------------------------------------------------------------------
# shared figures: a number stated twice needs an owner
#
# Both checks below need `plan/figure-owners.md`, the register naming each shared
# figure and the file that owns it. Until that file is tracked they skip, and say
# so -- see `skip_reason`. The register is a planning layer and Daniel's to approve;
# the suite does not create it.
# --------------------------------------------------------------------------

FIGURES = "plan/figure-owners.md"
FIGURE = re.compile(
    r"\b(\d[\d,]*(?:\.\d+)?)\s*"
    r"(years?|months?|weeks?|days?|hours?|kilometers?|km|meters?|centimeters?|cm|"
    r"kilograms?|kg|tonnes?|degrees?|°C|percent|%|people|"
    r"generations?|million|light-years?|AU|W\b|mm)\b", re.I)
# Craft measurement and method history are not world facts; drafted and rejected
# prose is the record of what was written and not a place anyone cites from.
FIGURE_SKIP = ("tools/", "process/", "prompts/") + EVIDENCE_DIRS


def figure_register_reason() -> str | None:
    if FIGURES not in corpus():
        return (f"`{FIGURES}` is not tracked yet; the register owns this job, "
                "and until it exists there is nothing to check against")
    return None


def _norm(value: str, unit: str) -> tuple[str, str]:
    u = unit.lower().rstrip("s")
    u = {"°c": "degree", "kilometer": "km", "centimeter": "cm", "kilogram": "kg",
         "meter": "m", "percent": "%"}.get(u, u)
    return value.replace(",", ""), u


@cache
def owned_figures() -> set[tuple[str, str]]:
    """Every (value, unit) the register declares, read from its `The owners` table.

    Anchored on that heading rather than on the file's title, because a second
    table later in the section would otherwise shadow this one and the register
    would read as empty. In Cretaceous it did, the moment the word-form table was
    added."""
    out = set()
    for rows in tables(section(FIGURES, r"The owners")):
        for _, cells in rows:
            if not cells:
                continue
            m = FIGURE.search(plain(cells[0]))
            if m:
                out.add(_norm(*m.groups()))
    return out


def check_shared_figures_owned() -> list[Violation]:
    """A figure stated in two or more files has a row in the owners register.

    **A proposition stated once cannot contradict itself.** The surface that can
    drift is not the fact count, it is the repetition count -- and repetition is
    mechanically discoverable, which is what makes this cheap. In Cretaceous one
    span of years sat in twelve files and twenty-four places with no owner.

    **The register is not maintained by remembering.** This fails on the *second*
    mention, so an untabled repeat cannot be created: the act of creating it is
    what stops the suite.

    **What it cannot do.** It sees numbers with units. It does not see a
    proposition carried entirely in words -- that is `word_figures` for figures
    and `claims_agree` for everything else."""
    if figure_register_reason():
        return []
    owned = owned_figures()
    if not owned:
        return [Violation(FIGURES, 1, "the register declares no figures; it owns that job")]
    where: dict[tuple[str, str], set[str]] = defaultdict(set)
    for path, _, line in iter_lines():
        if path.startswith(FIGURE_SKIP) or path == FIGURES:
            continue
        # **A claim annotation is not a mention.** It shadows the figure in the
        # prose beside it and carries the numeric form on purpose, so counting it
        # would make every annotated word-figure register here as a digit-figure
        # needing its own owner row -- each system manufacturing work for the other.
        for m in FIGURE.finditer(CLAIM.sub(" ", line)):
            where[_norm(*m.groups())].add(path)
    out = []
    for key, files in sorted(where.items()):
        if len(files) >= 2 and key not in owned:
            shown = ", ".join(sorted(files)[:4]) + (" …" if len(files) > 4 else "")
            out.append(Violation(FIGURES, 1,
                                 f"{key[0]} {key[1]} is stated in {len(files)} files "
                                 f"and the register does not own it: {shown}"))
    return out


# **The numeral has to be captured whole or the grouping is a fiction.** A pattern
# that takes only the word before the unit collapses *sixty-six million years*,
# *seven million years* and *a million years* into one bucket -- three unrelated
# propositions reported as one repeated figure, which is worse than not looking.
SMALL = ("nineteen|eighteen|seventeen|sixteen|fifteen|fourteen|thirteen|twelve|eleven|ten|"
         "nine|eight|seven|six|five|four|three|two|one")
TENS = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
SCALE = "hundred|thousand|million"
NUMWORD = rf"(?:(?:{TENS})(?:[-\s](?:{SMALL}))?|(?:{SMALL}))"
WORD_NUM = rf"(?:(?:{NUMWORD}[\s-])?(?:{SCALE})(?:[\s-]and[\s-]{NUMWORD})?|{NUMWORD})"
UNIT = (r"years?|months?|weeks?|days?|hours?|kilometers?|km|meters?|centimeters?|cm|"
        r"kilograms?|kg|tonnes?|degrees?|percent|people|"
        r"generations?|watts?|millimeters?|mm|light-years?")
WORD_FIGURE = re.compile(rf"\b({WORD_NUM})[\s-]+({UNIT})\b", re.I)

_ONES = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen".split())}
_TENS = {w: (i + 2) * 10 for i, w in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety".split())}
_SCALE = {"hundred": 100, "thousand": 1000, "million": 1_000_000}


def word_to_int(phrase: str) -> int | None:
    """`sixty-six million` -> 66000000. None if it does not parse cleanly.

    Used to shadow-check an annotation against the words beside it: a claim whose
    value does not contain the number the sentence states is worse than no claim,
    because it reads as authoritative and agrees with itself."""
    total = run = 0
    seen = False
    for w in re.split(r"[\s-]+", phrase.lower()):
        if w == "and":
            continue
        if w in _ONES:
            run += _ONES[w]
        elif w in _TENS:
            run += _TENS[w]
        elif w in _SCALE:
            run = (run or 1) * _SCALE[w]
            total += run
            run = 0
        else:
            return None
        seen = True
    return total + run if seen else None


@cache
def exempt_word_figures() -> set[tuple[str, str]]:
    """(number-words, unit) pairs the register declares are not shared figures.

    Read from the register's `Word-form figures` table, and a row carries its
    reason in prose because the reason is the entire justification -- *two days*
    can be twenty-nine unrelated statements, and that is not recoverable from a
    bare exemption."""
    out = set()
    for rows in tables(section(FIGURES, r"Word-form figures")):
        for _, cells in rows:
            if len(cells) < 2:
                continue
            for phrase in re.split(r"·", plain(cells[0])):
                m = WORD_FIGURE.search(phrase.strip())
                if m:
                    out.add((re.sub(r"\s+", " ", m.group(1).lower()), m.group(2).lower().rstrip("s")))
    return out


def _shadows(value: str, n: int) -> bool:
    """Does a claim's value carry the number the sentence beside it states?

    Exact digits, except that a whole number of millions may be written as its
    significand."""
    digits = re.sub(r"[,_\s]", "", value)
    if str(n) in digits:
        return True
    return n >= 1_000_000 and n % 1_000_000 == 0 and str(n // 1_000_000) in digits


def check_word_figures() -> list[Violation]:
    """Figures written in words, repeated across files, with no claim annotation.

    `shared_figures_owned` requires a leading digit, so it sees `6 m` and is blind
    to *six meters* -- which is how one animal's length came to sit in seven
    Cretaceous files unnoticed. This is the gap, and it cannot be closed by growing
    that regex: *three people* in an ordinary sentence is structurally
    indistinguishable from *three people* as a world figure.

    **So the line declares itself.** A figure written in words carries the numeric
    form in an inline claim, and the claim then buys the stronger guarantee --
    ownership says a row exists, agreement says every site matches. A word-figure
    that is genuinely not a shared figure gets a row in the register's word-form
    table with a reason, not an annotation.

    **Not tested directly**, as in Cretaceous: a false positive in an enforcing
    check is a broken build, so this is enforced only through a ratified rule
    block naming it, and is otherwise a worklist in `report.py`. Only repeats are
    reported, and only where some site is unannotated."""
    if figure_register_reason():
        return []
    exempt = exempt_word_figures()
    where: dict[tuple[str, str], list[tuple[str, int, bool]]] = defaultdict(list)
    for path, n, line in iter_lines():
        if path.startswith(FIGURE_SKIP) or path == FIGURES:
            continue
        # A heading restates what the section below it says, so the claim belongs on
        # the assertion and not on the label.
        if line.lstrip().startswith("#"):
            continue
        for m in WORD_FIGURE.finditer(line):
            key = (re.sub(r"\s+", " ", m.group(1).lower()), m.group(2).lower().rstrip("s"))
            if key in exempt:
                continue
            value = word_to_int(m.group(1))
            shadowed = value is not None and any(
                _shadows(c.group(2), value) for c in CLAIM.finditer(line))
            where[key].append((path, n, shadowed))

    out = []
    for (num, unit), sites in sorted(where.items()):
        files = {p for p, _, _ in sites}
        bare = [(p, n) for p, n, ok in sites if not ok]
        if len(files) < 2 or not bare:
            continue
        shown = ", ".join(f"{p}:{n}" for p, n in bare[:4]) + (" …" if len(bare) > 4 else "")
        out.append(Violation(*bare[0], f"'{num} {unit}' is stated in {len(files)} files and "
                                       f"{len(bare)} site(s) carry no claim shadowing it: {shown}"))
    return out


# --------------------------------------------------------------------------
# categorical lines that cite nothing — a preference wearing a law's grammar
# --------------------------------------------------------------------------

# An instruction, not a description: the categorical word opens a sentence,
# a bullet or a bold run ("Never say", "**Do not**"), or is one of the phrases
# that only ever appear as rules. "Rivers here do not swell" is a fact and is
# not matched; "Do not write the sway" is an order and is.
CATEGORICAL_RE = re.compile(
    r"(^|[*>.:;—-]|\| ) *(\*\*)?(Never|Always|Do not|Don't)\b"
    r"|\bmust not\b|\bnot ever\b|\bunder no circumstances\b"
)
# A reason counts as a citation: the complaint is a rule with nothing under it,
# and "because" is something under it.
CITATION_RE = re.compile(
    r"`[^`]+\.(md|py)`|§|@WF-|\[retired\]|[Hh]is words|Daniel|\bbecause\b|\bwhich is why\b|\bso that\b|\bor else\b"
)


@cache
def categorical_scope() -> tuple[str, ...]:
    """The paths the rule naming `categorical_uncited` governs, from its `every` field.

    The scope is declared in the rule block in AGENTS.md §6, so it is read from
    there: the backticked paths in `every`. Restating them here would be a second
    copy of the rule."""
    for r in rules():
        if r.fields.get("check") == "categorical_uncited":
            return tuple(re.findall(r"`([^`]+)`", r.fields.get("every", "")))
    return ()


def check_categorical_uncited() -> list[Violation]:
    """A line that says never, always, must not or do not cites something.

    `AGENTS.md` §6: preferences inflate into laws, and the test is whether the
    rule cites anything — a ruling, a measurement, a physical fact. Daniel's words
    on why this matters, from Cretaceous: rules are in tension and most choices
    are tradeoffs, so a categorical rule with no reason under it gets obeyed past
    the point where it was right.

    A paragraph is one line in this corpus (nothing is hard-wrapped), so the
    citation is looked for on the same line. **This finds wording, not
    judgment**: a flagged line may be a characterization rather than a rule, and
    the remedy is a reason or a counterweight, never a mechanical softening. The
    line that is legitimately absolute cites what makes it so and passes.

    Enforced only once its rule is ratified; until then `report.py` lists what it
    would catch. If no rule names this check, the scope is undeclared and the
    check reports nothing."""
    scope = categorical_scope()
    out = []
    for path, n, line in iter_lines():
        if not any(path == s or (s.endswith("/") and path.startswith(s)) for s in scope):
            continue
        if line.lstrip().startswith(("```", "|---")):
            continue
        m = CATEGORICAL_RE.search(line)
        if m and not CITATION_RE.search(line):
            out.append(Violation(path, n, f"categorical, cites nothing: …{line[max(0, m.start() - 40):m.end() + 60].strip()}…"))
    return out


# --------------------------------------------------------------------------
# scenes and scene maps: pointers, IN as a form, open choices
#
# Every check here degrades to silence when there is nothing to check: no maps in
# `plan/scene-maps/`, no `[requires]` anywhere, no scene list. None of them
# invents a scene registry the corpus has not got.
# --------------------------------------------------------------------------

MAPS_DIR = "plan/scene-maps/"
SCENE_LIST = "plan/scene-list.md"
REQUIRES = re.compile(r"\[requires\s+([^\]]*)\]")
PLANTS = re.compile(r"\[plants\s*(?:→|->)\s*([^\]\s—]+)")
PAYLOAD_SEP = re.compile(r"\s(?:—|--)\s*")


def scene_maps() -> list[tuple[str, list[str]]]:
    """(path, lines) for every tracked forward map, in id order."""
    return sorted((p, l) for p, l in corpus().items() if p.startswith(MAPS_DIR) and p.endswith(".md"))


def _map_id(path: str) -> str:
    return Path(path).stem


@cache
def known_scenes() -> frozenset[str] | None:
    """Every scene the corpus says exists, or None if nothing says.

    The union of three declarations: entries in `plan/scene-list.md` (a line that
    opens, after any heading marks, with an id in the declared scheme), the stems
    of tracked maps, and the stems of tracked prose in `content/`. **None, not an
    empty set, when there is no scene list**: without a list, a pointer at an
    unmapped scene cannot be told from a pointer at a scene that does not exist,
    and the first is the work queue rather than a defect."""
    if SCENE_LIST not in corpus():
        return None
    addr = scene_address()
    ids: set[str] = set()
    if addr is not None:
        for line in lines_of(SCENE_LIST):
            m = addr.match(re.sub(r"^\s*#*\s*\**", "", line))
            if m:
                ids.add(m.group(1))
    ids |= {_map_id(p) for p, _ in scene_maps()}
    ids |= {Path(p).stem for p in corpus() if p.startswith("content/") and not p.startswith(EVIDENCE_DIRS)}
    return frozenset(ids)


def _map_moves() -> dict[str, dict[int, str]]:
    """scene id -> move number -> the move's text, for every tracked map."""
    moves: dict[str, dict[int, str]] = {}
    for path, lines in scene_maps():
        cur, found = None, {}
        for line in lines:
            m = re.match(r"^(\d+)\. ", line.strip())
            if m:
                cur = int(m.group(1))
                found[cur] = line
            elif line.startswith("#"):
                cur = None
            elif cur is not None and line.strip():
                found[cur] += "\n" + line
        moves[_map_id(path)] = found
    return moves


def check_requires_resolve() -> list[Violation]:
    """Every `[requires …]` pointer names a scene in the declared scheme, and a
    scene and move that exist where that can be known.

    The form is `[requires <scene>.<move> — payload]`, written on the dependent
    move. **The payload matters as much as the address** -- what has to still be
    true at the far end, not just where it lives -- and Cretaceous learned that
    pointer integrity is not semantic integrity. The address is checkable; the
    payload is checked for presence only, because whether the source still
    delivers it is a reading judgment.

    **An unresolved `requires` is not a violation; it is the work queue.** A
    pointer at a scene with no map yet says what to map next. The violations are
    a pointer in no recognizable scene scheme, a pointer at a scene the scene list
    does not hold (checked only once `plan/scene-list.md` exists), a move number a
    mapped scene does not have, and an empty payload. The form's own template
    line, `[requires <scene>.<move> — payload]`, is skipped."""
    addr = scene_address()
    known = known_scenes()
    moves = _map_moves()
    out = []
    for path, n, line in iter_lines():
        for m in REQUIRES.finditer(line):
            body = m.group(1).strip()
            if body.startswith("<"):
                continue
            if addr is None:
                out.append(Violation(AGENTS, 1, "a [requires] exists and AGENTS.md declares no scene-id "
                                                "scheme on a line carrying `@WF-scene.id.scheme`"))
                return out
            a = addr.match(body)
            if not a:
                out.append(Violation(path, n, f"[requires {body[:40]}] names no address in the declared scheme"))
                continue
            target, move = a.group(1), a.group(2)
            if known is not None and target not in known:
                out.append(Violation(path, n, f"[requires {target}] names no scene in `{SCENE_LIST}`"))
            elif move and target in moves and int(move) not in moves[target]:
                out.append(Violation(path, n, f"[requires {target}.{move}]; {target} is mapped and has no move {move}"))
            parts = PAYLOAD_SEP.split(body, maxsplit=1)
            if len(parts) < 2 or not parts[1].strip():
                out.append(Violation(path, n, f"[requires {target}{'.' + move if move else ''}] carries no payload"))
    return out


def check_plants_resolve() -> list[Violation]:
    """Every `[plants → X]` in a map names a scene in the declared scheme, and one
    the scene list holds once a scene list exists. The forward twin of
    `requires_resolve`; a plant into a scene that does not exist pays nowhere."""
    addr = scene_address()
    known = known_scenes()
    out = []
    for path, lines in scene_maps():
        for n, line in enumerate(lines, start=1):
            for m in PLANTS.finditer(line):
                tok = m.group(1).rstrip(".,;")
                a = addr.fullmatch(tok) if addr else None
                if a is None:
                    out.append(Violation(path, n, f"plants into {tok!r}, which is not an address in the declared scheme"))
                elif known is not None and a.group(1) not in known:
                    out.append(Violation(path, n, f"plants into {a.group(1)}, which is not a scene"))
    return out


def check_requires_open_choice() -> list[Violation]:
    """No backward pointer names a move that carries `[-]`.

    `AGENTS.md` §2: `[-]` is a choice with no apparent consequences yet, made by a
    session and never put to Daniel. A `requires` naming it is a consequence
    arriving, so the choice has to leave `[-]` and go on a ledger. Only pointers
    with a move number into a mapped scene can be checked; a scene-level pointer
    names no line."""
    addr = scene_address()
    if addr is None:
        return []
    moves = _map_moves()
    out = []
    for path, n, line in iter_lines():
        for m in REQUIRES.finditer(line):
            a = addr.match(m.group(1).strip())
            if not a or not a.group(2):
                continue
            target, move = a.group(1), int(a.group(2))
            text = moves.get(target, {}).get(move)
            if text and "`[-]`" in text:
                out.append(Violation(path, n, f"requires {target}.{move}, which is marked `[-]`; "
                                              "something now depends on it, so it belongs on a ledger"))
    return out


MAP_FIELD = re.compile(r"^- \*\*`([A-Z]+)`\*\*")
IN_FIELD = re.compile(r"`([A-Z]+)`")
LOCAL_THEORY = "process/map-form.md"


@cache
def map_schema() -> tuple[str, list[str]]:
    """(where the schema was read, the required IN fields).

    The fields are declared under the heading *IN is a form*, as bullets opening
    with a bold backticked field name. This novel owns its form, in
    `process/map-form.md`, because the form is derived from the author's own prose
    and Viking's differs from Cretaceous's; if that file is absent the schema falls
    back to the methodology-theory path AGENTS.md cites. Not restated here: a
    field list in `tools/` would be the suite deciding what a map must contain,
    which is the one thing a check may never do."""
    if LOCAL_THEORY in corpus():
        body = section(LOCAL_THEORY, r"IN is a form")
        return LOCAL_THEORY, [m.group(1) for _, l in body if (m := MAP_FIELD.match(l.strip()))]
    for line in lines_of(AGENTS):
        for ref in FILE_REF.findall(line):
            if ref.endswith("methodology-theory.md"):
                p = _on_disk(ref)
                if p is not None and p.is_file():
                    lines = p.read_text(encoding="utf-8").splitlines()
                    body = section(ref, r"IN is a form", lines=lines)
                    return ref, [m.group(1) for _, l in body if (m := MAP_FIELD.match(l.strip()))]
    return LOCAL_THEORY, []


def check_scene_map_in_complete() -> list[Violation]:
    """Every scene map's IN answers every field the schema requires.

    The fields are not a style preference: each one is a question a real map
    failed to ask, and the reason IN is a form rather than free recall is that
    **a mapper cannot enumerate what he did not notice.** In Cretaceous the first
    map of a night camp in three days of rain had no light in it across four moves
    that needed the POV to see, and the author of that map was the last person who
    could have found it.

    Silent when `plan/scene-maps/` holds no tracked map."""
    maps = scene_maps()
    if not maps:
        return []
    where, fields = map_schema()
    if not fields:
        return [Violation(AGENTS, 1, f"maps exist and no IN schema could be read from `{where}` under the heading *IN is a form*")]
    out = []
    for path, lines in maps:
        body = section(path, r"^## IN")
        if not body:
            out.append(Violation(path, 1, "scene map has no IN block"))
            continue
        present = set(IN_FIELD.findall("\n".join(t for _, t in body)))
        missing = [f for f in fields if f not in present]
        if missing:
            out.append(Violation(path, body[0][0],
                                 f"IN answers no {', '.join(f'`{m}`' for m in missing)}"))
    return out


def check_scene_map_ids() -> list[Violation]:
    """Every map in `plan/scene-maps/` is named by a scene id in the declared scheme.

    The map's filename is its address -- `requires_resolve` finds a move by it --
    so a map named any other way is one no pointer can reach."""
    addr = scene_address()
    out = []
    for path, _ in scene_maps():
        if addr is None or not addr.fullmatch(_map_id(path)):
            out.append(Violation(path, 1, f"map filename {_map_id(path)!r} is not a scene id in the "
                                          "scheme AGENTS.md §5 declares"))
    return out


# --------------------------------------------------------------------------
# the registry
# --------------------------------------------------------------------------

CHECKS = {
    "file_refs": check_file_refs,
    "section_refs": check_section_refs,
    "frontmatter": check_frontmatter,
    "approval_not_stale": check_approval_not_stale,
    "approval_stated_once": check_approval_stated_once,
    "dated_provenance": check_dated_provenance,
    "us_english": check_us_english,
    "closed_list_uncounted": check_closed_list_uncounted,
    "rules_wellformed": check_rules_wellformed,
    "retired_claims": check_retired_claims,
    "claims_agree": check_claims_agree,
    "shared_figures_owned": check_shared_figures_owned,
    "word_figures": check_word_figures,
    "categorical_uncited": check_categorical_uncited,
    "requires_resolve": check_requires_resolve,
    "plants_resolve": check_plants_resolve,
    "requires_open_choice": check_requires_open_choice,
    "scene_map_in_complete": check_scene_map_in_complete,
    "scene_map_ids": check_scene_map_ids,
}

# A check that cannot run yet says why, rather than passing silently. Each entry
# returns a reason, or None when the check has what it needs.
SKIPS = {
    "shared_figures_owned": figure_register_reason,
    "word_figures": figure_register_reason,
    "scene_map_in_complete": lambda: None if scene_maps() else f"no tracked map in `{MAPS_DIR}` yet",
}


def skip_reason(name: str) -> str | None:
    fn = SKIPS.get(name)
    return fn() if fn else None


def run_all() -> dict[str, list[Violation]]:
    return {name: fn() for name, fn in CHECKS.items()}
