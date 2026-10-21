# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""Ratify rule blocks. See tools/RULES.md.

    python3 tools/ratify.py --list          # what is proposed, and what each catches
    python3 tools/ratify.py <id> [<id>...]  # ratify, after confirming each

Ratifying is one word and a date, so editing the block by hand is a perfectly good
way to do it. This exists to date it for you, to refuse rules that have no checker,
and to show you what each one catches before you say yes.

**A session runs it**, with `--yes`, when Daniel has said yes to the rule's sentence
in conversation. The ratification is his answer; this records it. An earlier
version refused without a TTY, which made him do by hand what he had already done
by answering. In a terminal without `--yes` it still asks per rule.
"""

from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import CHECKS, ROOT, rules  # noqa: E402


def show(r) -> str:
    fn = CHECKS.get(r.fields.get("check", ""))
    caught = "NO CHECKER WRITTEN" if fn is None else f"catches {len(fn())} today"
    return f"{r.render()}\n    {caught} — {r.file}:{r.line}\n    evidence: {r.fields.get('evidence', '—')}"


def set_status(r, value: str) -> None:
    path = ROOT / r.file
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    for i in range(r.line - 1, min(r.line + 20, len(lines))):
        if re.match(r"^status:\s", lines[i]):
            lines[i] = re.sub(r"^status:(\s*).*", rf"status:\1{value}", lines[i])
            path.write_text("".join(lines), encoding="utf-8")
            return
    raise SystemExit(f"could not find the status line of {r.id} near {r.file}:{r.line}")


def main(argv: list[str]) -> int:
    by_id = {r.id: r for r in rules()}

    if not argv or argv[0] in {"--list", "-l"}:
        for r in sorted(rules(), key=lambda r: (r.ratified, r.id)):
            print(show(r), "\n")
        return 0

    yes = "--yes" in argv
    argv = [a for a in argv if a != "--yes"]
    if not yes and not sys.stdin.isatty():
        print("ratify.py: pass --yes to record a ratification Daniel gave in conversation.",
              file=sys.stderr)
        return 2

    today = _dt.date.today().isoformat()
    unknown = [a for a in argv if a not in by_id]
    if unknown:
        print(f"no such rule: {', '.join(unknown)}", file=sys.stderr)
        print(f"known: {', '.join(sorted(by_id))}", file=sys.stderr)
        return 2

    ratified = 0
    for rid in argv:
        r = by_id[rid]
        if r.ratified:
            print(f"{rid} is already {r.fields['status']}\n")
            continue
        if r.fields.get("check") not in CHECKS:
            print(f"{rid} has no checker, so ratifying it would fail the suite. Skipped.\n")
            continue
        print(show(r))
        if yes or input("    ratify? [y/N] ").strip().lower() in {"y", "yes"}:
            set_status(r, f"ratified {today}")
            ratified += 1
            print(f"    ratified {today}\n")
        else:
            print("    left proposed\n")

    print(f"{ratified} ratified. Run the suite: uv run --with pytest pytest tools/ -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
