# Vendored from ~/code/me/deep-resonance/tools at commit 3b6911f (see ~/code/me/novel-method/adopt.md); a local change here is filed as novel-method feedback.
"""The fast suite. Every test here is a thin front end over a function in checks.py.

    uv run --with pytest pytest tools/              # everything deterministic
    uv run --with pytest pytest tools/ -k approval  # one category

**One test per invariant, not per violation.** The test name states the claim it
exercises, so a failing line reads as a sentence and needs no docstring to decode.
The count of failures is then the count of broken invariants rather than the count
of instances, and the instances go in the failure message as `file:line — what`,
which is the change-set row.

Inherited from Cretaceous, where an earlier version parametrized each violation
into its own case. It gave tidy test ids and a badly misleading headline: thirteen
dangling pointers and seven stray dates reported as "20 failed", which reads as
twenty problems and is two.

**The suite reads `git ls-files`.** An untracked file is invisible to it, so a
green run says nothing about a map or layer that has not been `git add`ed.
"""

from __future__ import annotations

import sys

import pytest

from checks import CHECKS, rules, skip_reason


def holds(name: str) -> None:
    """Pass silently, skip with the reason the check cannot run yet, or fail once
    with every violation listed."""
    reason = skip_reason(name)
    if reason:
        pytest.skip(f"{name}: {reason}")
    violations = CHECKS[name]()
    if violations:
        listing = "\n".join(f"  {v.file}:{v.line} — {v.message}" for v in violations)
        pytest.fail(f"{len(violations)} violations:\n{listing}", pytrace=False)


_ADVISED = False

WORD_FIGURE_ADVICE = """
─── NOTE FOR THE AI READING THIS OUTPUT ───────────────────────────────────────
`shared_figures_owned` only sees figures written as DIGITS — `6 m`, `206 years`.
A figure written in WORDS is caught by `word_figures` instead, which wants the
line to carry an inline `<!-- @WF-key: value -->` claim whose value repeats the
number.

**So when you state a figure in words in this corpus, annotate the line.** The
key names the PROPOSITION and never the number — `@WF-route.overland: 80km`, not
`@WF-eighty` — because `claims_agree` fails on one key holding two values, and
keying by digits would collide unrelated facts that share a number.

**If a word-figure is genuinely not a shared figure, it does not get annotated —
it gets a row in `plan/figure-owners.md`'s word-form table with a reason.**
Annotating those would assert they are one fact, which is worse than leaving
them alone. Suggest that table to Daniel before you suggest a claim.
───────────────────────────────────────────────────────────────────────────────
"""


def _advise_on_word_figures(capsys) -> None:
    """Say the quiet part on every green run, once, where capture cannot eat it.

    `capsys.disabled()` and not a bare write to `sys.stderr` or even
    `sys.__stderr__`: pytest's default `--capture=fd` redirects the file
    descriptors themselves, so both are swallowed on a passing run -- which is
    exactly the run this needs to survive. Suspending capture is the only spelling
    that reaches a terminal."""
    global _ADVISED
    if _ADVISED:
        return
    _ADVISED = True
    with capsys.disabled():
        sys.stderr.write(WORD_FIGURE_ADVICE)
        sys.stderr.flush()


# --- pointers resolve ------------------------------------------------------

def test_every_file_reference_resolves():
    """Every `file.md` the corpus points at exists."""
    holds("file_refs")


def test_every_section_citation_resolves():
    """Every `file.md` §N finds a heading numbered N in that file."""
    holds("section_refs")


# --- approval is recorded in exactly one place -----------------------------

def test_every_file_carries_an_approval_marker():
    """One of exactly three values, per AGENTS.md §2."""
    holds("frontmatter")


def test_no_file_changed_after_it_was_approved():
    """A file whose body no longer hashes to its marker has changed since he read it."""
    holds("approval_not_stale")


def test_approval_is_stated_only_in_frontmatter():
    """A second copy of approval state drifts; in Cretaceous it was wrong about five files."""
    holds("approval_stated_once")


def test_no_knowledge_file_carries_approval_history():
    """Knowledge files hold what is true; git holds how it got there."""
    holds("dated_provenance")


# --- house style -----------------------------------------------------------

def test_no_british_spellings():
    holds("us_english")


def test_no_count_is_stated_for_the_closed_vocabulary():
    """The terms are canon; a count is decoration that drifts."""
    holds("closed_list_uncounted")


# --- rulings and claims ----------------------------------------------------

def test_no_retired_claim_survives():
    """AGENTS.md §7. A ruling applied by memory across many files misses some."""
    holds("retired_claims")


def test_no_claim_key_is_asserted_two_ways():
    """Two assertions that are each well-formed and jointly false; nothing else sees these."""
    holds("claims_agree")


def test_every_figure_stated_twice_has_an_owner(capsys):
    """A proposition stated once cannot contradict itself; repetition is the drift surface.

    Skips until `plan/figure-owners.md` is tracked. This check is blind to half
    the drift surface, so it says so on the way past -- see the note it prints."""
    holds("shared_figures_owned")
    _advise_on_word_figures(capsys)


# --- the rule formalism checks itself --------------------------------------

def test_every_rule_block_is_wellformed():
    """Parses, carries its fields, has evidence, and is not self-ratified."""
    holds("rules_wellformed")


def _ratified():
    found = [r for r in rules() if r.ratified and r.fields.get("check") in CHECKS]
    return found or [None]


@pytest.mark.parametrize("rule", _ratified(), ids=lambda r: r.id if r else "none-ratified")
def test_ratified_rule_holds(rule):
    """Each rule Daniel has ratified. Proposed rules are reported, never failed.

    Parametrized over rules rather than violations: a rule is an invariant, so one
    case per rule keeps the failure count meaningful."""
    if rule is None:
        pytest.skip("no rules ratified yet — see python3 tools/report.py")
    holds(rule.fields["check"])


# --- scenes and scene maps -------------------------------------------------

def test_every_requires_pointer_names_a_scene_that_can_exist():
    """The address half is checkable; the payload is checked for presence, never for truth."""
    holds("requires_resolve")


def test_every_plant_names_a_scene_that_can_exist():
    holds("plants_resolve")


def test_no_backward_pointer_leans_on_an_open_choice():
    """A `[-]` choice that something depends on has acquired a consequence and needs a ledger."""
    holds("requires_open_choice")


def test_every_scene_map_answers_every_field_the_schema_requires():
    """A mapper cannot enumerate what he did not notice; IN is a form for that reason."""
    holds("scene_map_in_complete")


def test_every_scene_map_is_named_by_a_scene_id():
    """A map's filename is its address; a map named otherwise is one no pointer reaches."""
    holds("scene_map_ids")
