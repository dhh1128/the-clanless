#!/usr/bin/env python3
"""Vendored from ~/code/me/novel-method/tools at commit b21b9af (edition-1). Accept an approved file that changed only under commits citing a ruling; optionally restamp it.

usage: approval_cited.py [-C <repo>]            # report stale approved files and whether each is cited
       approval_cited.py [-C <repo>] --write    # restamp the cited ones

Runbook B1, edition 1 (Q-QFMG): keep the body hash, automate the stamp. A file whose
`approval: approved <hash>` no longer matches its body has changed since Daniel read it. It
passes here when every commit that changed it after its marker was set names, in its message,
the tag of the ruling it enacts (`Q-xxxx` or `D-xxxx`). It fails when any such commit names
none, or when the file has uncommitted changes, because an edit nothing attributes to a ruling
is exactly what the hash exists to catch.

What this cannot check: that the cited tag is a ruling he gave, rather than a session's
paraphrase of one (tensions.md `rulings`). The citation makes the claim auditable; it does not
make it true.

A novel vendors this file into its `tools/` (adopt.md: first docstring line names the
novel-method commit it came from) and calls `check()` from its suite in place of, or in front
of, its plain staleness check. The body hash is the same as Cretaceous `tools/checks.py`
`body_hash`, so markers stamped by either agree. Standard library only.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

MARKER = re.compile(r"^approval: approved ([0-9a-f]{8})$")
RULING_TAG = re.compile(r"\b[QD]-[0-9A-HJKMNP-TV-Z]{4}\b", re.I)


def _body(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 8)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    return "\n".join(l.rstrip() for l in lines).strip()


def body_hash(text: str) -> str:
    return hashlib.sha256(_body(text).encode("utf-8")).hexdigest()[:8]


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def marker_commit(repo: Path, path: str, h: str) -> str | None:
    """The newest commit whose version of the file carries this marker on line 2."""
    for sha in git(repo, "log", "--format=%H", "-G", f"^approval: approved {h}$", "--", path).split():
        try:
            line2 = git(repo, "show", f"{sha}:{path}").splitlines()[1]
        except (RuntimeError, IndexError):
            continue
        if line2.strip() == f"approval: approved {h}":
            return sha
    return None


def check(repo: Path) -> list[tuple[str, bool, str]]:
    """(path, accepted, reason) for every approved markdown file whose body no longer matches."""
    out = []
    dirty = set(git(repo, "diff", "--name-only", "HEAD").split())
    for path in git(repo, "ls-files", "*.md").split():
        p = repo / path
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        m = MARKER.match(lines[1]) if len(lines) > 1 else None
        if not m or body_hash(text) == m.group(1):
            continue
        if path in dirty:
            out.append((path, False, "uncommitted changes; commit them citing the ruling"))
            continue
        base = marker_commit(repo, path, m.group(1))
        if not base:
            out.append((path, False, f"no commit sets marker {m.group(1)}"))
            continue
        log = git(repo, "log", "--format=%H%x00%B%x01", f"{base}..HEAD", "--", path)
        uncited = []
        for rec in filter(str.strip, log.split("\x01")):
            sha, _, msg = rec.strip().partition("\x00")
            if not RULING_TAG.search(msg):
                uncited.append(sha[:7])
        if uncited:
            out.append((path, False, f"changed by commits citing no ruling: {', '.join(uncited)}"))
        else:
            out.append((path, True, "every change since approval cites a ruling"))
    return out


def restamp(repo: Path, path: str) -> str:
    p = repo / path
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    h = body_hash(text)
    lines[1] = f"approval: approved {h}\n"
    p.write_text("".join(lines), encoding="utf-8")
    return h


def main(argv: list[str]) -> int:
    repo = Path(".")
    if argv[:1] == ["-C"]:
        repo, argv = Path(argv[1]), argv[2:]
    repo = Path(git(repo, "rev-parse", "--show-toplevel").strip())
    results = check(repo)
    for path, ok, why in results:
        if ok and "--write" in argv:
            print(f"restamped {path} -> {restamp(repo, path)} ({why})")
        else:
            print(f"{'cited  ' if ok else 'UNCITED'} {path}: {why}")
    return 1 if any(not ok for _, ok, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
