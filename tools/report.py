# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""The second front end: the same checks, emitted as a markdown change set.

    python3 tools/report.py              # everything, grouped by check
    python3 tools/report.py file_refs    # one check

pytest answers "is the corpus consistent." This answers "what would I have to
change," in the shape Daniel reads and strikes. It also lists the checks that are
not tested directly -- `categorical_uncited` and `word_figures`, enforced only once
a rule naming them is ratified -- so what they would catch is visible before
anyone is asked to ratify them.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks import (CHECKS, check_approval_not_stale, corpus, rules,  # noqa: E402
                    scene_id_pattern, skip_reason)


def main(argv: list[str]) -> int:
    wanted = argv[1:] or list(CHECKS)
    unknown = [w for w in wanted if w not in CHECKS]
    if unknown:
        print(f"unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"available: {', '.join(CHECKS)}", file=sys.stderr)
        return 2

    skipped = {name: skip_reason(name) for name in wanted}
    results = {name: ([] if skipped[name] else CHECKS[name]()) for name in wanted}
    total = sum(len(v) for v in results.values())
    scheme = scene_id_pattern()

    print("# Consistency report\n")
    print(f"{total} violations across {sum(1 for v in results.values() if v)} of "
          f"{len(results)} checks. Scene ids: "
          + (f"`{scheme[0]}`, generalized from `AGENTS.md:{scheme[1]}`." if scheme
             else "**no scheme declared** in `AGENTS.md`.") + "\n")

    for name, violations in results.items():
        doc = (CHECKS[name].__doc__ or "").strip().splitlines()[0]
        if skipped[name]:
            print(f"## {name} — skipped\n\n{doc}\n\nSkipped: {skipped[name]}.\n")
            continue
        if not violations:
            print(f"## {name} — clean\n\n{doc}\n")
            continue
        print(f"## {name} — {len(violations)}\n\n{doc}\n")
        print("| file:line | what |")
        print("|---|---|")
        for v in violations:
            print(f"| `{v.file}:{v.line}` | {v.message} |")
        print()

    if rules():
        print("## rules\n")
        print("Ratified rules are enforced by the suite. Proposed rules are listed with what they "
              "would catch today, so a rule can be judged against its violations rather than its "
              "sentence. Only Daniel ratifies -- see `tools/RULES.md`.\n")
        for r in sorted(rules(), key=lambda r: r.id):
            fn = CHECKS.get(r.fields.get("check", ""))
            caught = "no checker written yet" if fn is None else f"catches {len(fn())} today"
            print(f"- {r.render()} — {caught} — `{r.file}:{r.line}`")
        print()

    stale = {v.file for v in check_approval_not_stale()}
    c = corpus()
    marked = [p for p in sorted(c)
              if len(c[p]) > 1 and c[p][1].startswith("approval: ")
              and c[p][1] != "approval: unapproved"]
    if marked:
        print("## approval\n")
        print("Markers carry a hash of the body, not a date — see `AGENTS.md` §2. A file whose "
              "body no longer hashes to its marker has changed since he read it. "
              "`python3 tools/approve.py --list` is the same table; `approve.py <file>` re-stamps one.\n")
        print("| file | marker | changed since approval |")
        print("|---|---|---|")
        for path in marked:
            print(f"| `{path}` | {c[path][1].removeprefix('approval: ')} | "
                  f"{'**yes**' if path in stale else 'no'} |")
        print()

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
