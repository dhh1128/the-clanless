# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Rewrite a stale `approved <hash>` marker to the file's current body hash.

**Only ever touches line 2**, which is where frontmatter lives, and that
restriction is the whole point of the file rather than an implementation
detail. Two attempts at this job used a regex over the whole text and both
rewrote the *example* marker inside `AGENTS.md` §2's documentation fence,
which is a code block explaining what a marker looks like. A marker-shaped
line is not a marker; its position is what makes it one.

This is not `approve.py`, which stamps any file whether or not it was approved
before. This records an answer Daniel has already given in conversation, by hand, for
the edits that enacted it -- see `AGENTS.md` §2.

    python3 tools/restamp.py            # list what is stale
    python3 tools/restamp.py --write    # restamp it
"""

from __future__ import annotations

import re
import sys

from checks import ROOT, body_hash, corpus

MARKER = re.compile(r"^approval: approved ([0-9a-f]{8})$")


def stale() -> list[tuple[str, str, str]]:
    out = []
    for path, lines in corpus().items():
        if len(lines) < 2:
            continue
        m = MARKER.match(lines[1].strip())          # line 2, and nowhere else
        if not m:
            continue
        current = body_hash("\n".join(lines))
        if m.group(1) != current:
            out.append((path, m.group(1), current))
    return out


def main(argv: list[str]) -> int:
    rows = stale()
    if not rows:
        print("every approved marker matches its body")
        return 0
    write = "--write" in argv
    for path, old, new in rows:
        print(f"{path:38} {old} -> {new}")
        if write:
            p = ROOT / path
            lines = p.read_text().split("\n")
            lines[1] = f"approval: approved {new}"
            p.write_text("\n".join(lines))
    if not write:
        print(f"\n{len(rows)} stale. Re-run with --write to restamp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
