---
approval: unapproved
---

# tools — the consistency suite

Answers one question: **does anything in the corpus disagree with anything else in the corpus?** It is blind to the other question — whether any of it is Daniel's — and a green run must never be read as approval. See `AGENTS.md` §1.

```
uv run --with pytest pytest tools/              # the fast suite, about a second
uv run --with pytest pytest tools/ -k approval  # one category
python3 tools/report.py                         # the same checks as a markdown change set
python3 tools/report.py file_refs               # one check
python3 tools/questions.py                      # what is open, and what was answered and never landed
```

`pytest` is not installed on this box and no `pyproject.toml` or venv is wanted in a novel repo, so `uv run --with pytest` supplies it per invocation. Everything else needs only the standard library.

**The suite reads `git ls-files`, so an untracked file is invisible to it.** `git add` a new map or layer before trusting a green run on it; the suite comes back falsely green on anything git does not know about. Other sessions' uncommitted new files are likewise out of scope until they are added.

Ported from `~/code/me/cretaceous/tools/` at the commit `AGENTS.md` names. The generic checks came across with their reasoning; the ones about Cretaceous's world did not (see "What was left behind" below). Where a docstring tells an incident, the incident happened in Cretaceous, and it is kept because that reasoning is what stops a later session deleting the check.

## The files

`checks.py` holds the logic as plain functions returning violations. `test_consistency.py` is a thin pytest front end and `report.py` is a second front end for the document Daniel reads and strikes. `ratify.py` is how a proposed rule becomes an enforced one and `approve.py` is how a file's contents get Daniel's marker; the session runs both, with `--yes`, only on his yes in conversation. `restamp.py` rewrites only line 2 of a file. `measure.py` measures drafted prose and imports nothing from the suite. `questions.py` is described below. Logic never goes in the test methods — a suite that can say something is wrong but not what to change is half a tool.

**One test per invariant, not per violation, and the test name states the claim.** `test_every_file_reference_resolves` fails once, listing every dangling pointer, rather than once per pointer. The failing line reads as a sentence and needs no docstring to decode, and the failure count means what it looks like it means: an earlier Cretaceous version parametrized per violation and reported thirteen pointers plus seven stray dates as *"20 failed"*, which reads as twenty problems and is two. The instances go in the message as `file:line — what`, which is the change-set row.

**A check that cannot run yet skips and says why** rather than passing silently. `checks.SKIPS` holds the reason for each, and both front ends print it.

## The two rules that govern what may be written here

**A check asserts a relationship, never a value.** *"Every scene a pointer names exists"* is a check. *"The ship is 40 m long"* is a second copy of canon wearing a test costume: it freezes a number into a new location, and if that number was never approved the suite now enforces an invention. This is the failure the Cretaceous corpus suffered, and it is the one thing that would make the suite worse than nothing.

**Anything the corpus declares about itself is read from the corpus at runtime.** In this port that means:

- **The scene-id scheme** comes from the `AGENTS.md` §5 line carrying `@WF-scene.id.scheme`, generalized from the backticked example on that line. `07.2` becomes two-digit chapter, any scene. Cretaceous hardcoded `D\d+\.\d+` in five checks; nothing here names either scheme, so a renumber is one edit to `AGENTS.md`.
- **The retired claims** come from the table in `AGENTS.md` §7.
- **The closed vocabulary list** is whichever file the `AGENTS.md` line carrying `@WF-lingo.closed: true` names.
- **The scope of `categorical_uncited`** is the backticked paths in its own rule block's `every` field.
- **The IN schema for scene maps** comes from methodology-theory §4a. `AGENTS.md` cites that file in Cretaceous rather than copying it, so that it has one owner, and the suite follows the citation; a tracked `process/methodology-theory.md` would take precedence if this repo ever grows one.
- **External files** — the published book, Cretaceous's method files — resolve because the corpus cites them by full path, not because a list here names them.

A check that hardcodes one of those is the seventh copy of a fact, and it will drift.

## The checks, and why each exists

| check | asserts | why it exists |
|---|---|---|
| `file_refs` | every `` `file.md` `` the corpus points at exists | In Cretaceous thirteen pointers survived into files deleted in a restructure, and each still read as authority. A reference by absolute or home path is resolved on disk; a bare name resolves to a tracked file, or to an external file the corpus cites by full path elsewhere. |
| `section_refs` | every `` `file.md` `` §N citation resolves to a heading numbered N | Renumbering one Cretaceous file's sections silently broke four citations, and nobody noticed for a day. External files are read from disk. |
| `frontmatter` | every file carries exactly one of the three approval values | `AGENTS.md` §2. The scheme is worthless if a file can quietly carry no marker. |
| `approval_not_stale` | every approved file's body still hashes to what its marker records | Markers carry an eight-character body hash, not a date. **Cretaceous went through three designs, and the first two both asked chronological questions and got the wrong answer.** A hand-written date has day granularity, and that corpus was written, approved and committed inside one day. Commit ordering then counted a formatting migration as an edit to every approved file at once. A hash is a comparison: immune to reformats, immune to commit churn, and it sees uncommitted edits. |
| `approval_stated_once` | a file's approval state appears in its own frontmatter and nowhere else | Cretaceous's README carried a second copy and was wrong about five files. It matches claim phrases — *is approved*, *are recent and unapproved* — not the bare word, so *"No approved prose exists yet"* does not fire. A file named by full path belongs to another repo and is ignored. It will also miss a trailing *"Both are unapproved"* whose files were named a sentence earlier. |
| `dated_provenance` | knowledge files (`plan/`, `kb/`) carry what is true, not how it got approved | `AGENTS.md` §2: no dates, no "Daniel's ruling", no "struck on". The pattern deliberately does not match the bare name, because *"that is a note for Daniel, not a license"* is instruction, not history. |
| `us_english` | no British spellings, in prose or in filenames | `AGENTS.md` §5. A literary register pulls toward them and they keep coming back. Filenames count because Cretaceous's `humour-plan.md` survived for days when only line content was read. Blockquotes are exempt as verbatim quotation. The list is `tools/british-english.txt`, vendored with a LOCAL override block. |
| `closed_list_uncounted` | nobody states how many terms the closed vocabulary holds | The terms are canon and the count is incidental. Four Cretaceous files carried a number that had been wrong since the list was created. A fact nothing depends on only drifts, so the number is deleted rather than corrected. **Narrowed in the port**: a count is a number attached to a unit word (*terms*, *words*, *entries*) near *closed*, because Cretaceous's pattern — any number word within forty characters after *closed* — fired here on *"from day one"*. |
| `rules_wellformed` | every ` ```rule ` block parses, carries its fields, has evidence, and is not ratified without a checker | The rule formalism, checked by the suite it feeds. See `tools/RULES.md`. |
| `retired_claims` | no tracked file contains a phrase in `AGENTS.md` §7's table | A ruling applied by memory across many files misses some: in Cretaceous, five rulings made in one sitting were still contradicted in live files hours later, two of them in files the session believed it had fixed. A line carrying `[retired]` is exempt, per line. `AGENTS.md` is exempt because the table must name what it forbids; `content/superseded/` and `content/rejected/` are exempt because rewording a kept draft falsifies the record. **Matching is bounded at word ends**, which Cretaceous's was not: this table starts with a four-letter name, and a substring match on `Lena` fires on *Helena*. |
| `claims_agree` | no `<!-- @WF-key: value -->` key holds two values anywhere; no two keys differ by one character | **The detector for the class nothing else reaches: two well-formed assertions that are jointly false.** Nothing has to be recognized, because the line declares its own claim. Inline rather than a register, because a register restates what a sentence says and a second copy drifts. An annotation that lies is worse than none, so they stay tiny, adjacent, and never say more than the sentence beside them. Key by the proposition, never by the number. |
| `shared_figures_owned` | a figure with a unit, stated in two or more files, has a row in the owners register | A proposition stated once cannot contradict itself; repetition is the drift surface, and it is mechanically discoverable. **Skips until `plan/figure-owners.md` is tracked** — see below. |
| `word_figures` | a figure written in words, repeated across files, carries a claim shadowing it at every site | The blind spot of `shared_figures_owned`, which needs a leading digit. **Report-only**, as in Cretaceous: enforced only by ratifying a rule block that names it. **Skips until `plan/figure-owners.md` is tracked.** |
| `categorical_uncited` | a line in its scope saying never, always, must not or do not cites something | `AGENTS.md` §6: preferences inflate into laws. **Finds wording, not judgment** — the remedy is a reason or a counterweight, never a mechanical softening. Report-only until the `categorical-cites-something` rule in `AGENTS.md` §6 is ratified. |
| `requires_resolve` | every `[requires <scene>.<move> — payload]` names an address in the declared scheme, a scene the scene list holds, a move a mapped scene has, and carries a payload | **An unresolved `requires` is not a violation; it is the work queue** — a pointer at an unmapped scene says what to map next. Scene membership is checked only once `plan/scene-list.md` exists, because without a list a pointer at an unmapped scene cannot be told from a pointer at a scene that does not exist. The payload is checked for presence, never for truth. |
| `plants_resolve` | every `[plants → X]` in a map names an address in the declared scheme, and a listed scene once a list exists | The forward twin of `requires_resolve`. |
| `requires_open_choice` | no `[requires]` names a move carrying `[-]` | `AGENTS.md` §2: a `[-]` choice stops qualifying the moment something depends on it, and then it goes on a ledger. |
| `scene_map_in_complete` | every map's IN block answers every field the schema requires | A mapper cannot enumerate what he did not notice. In Cretaceous the first map of a night camp in three days of rain had no light in it across four moves that needed the POV to see. **Skips while `plan/scene-maps/` holds no tracked map.** |
| `scene_map_ids` | every map file is named by a scene id in the declared scheme | A map's filename is its address; `requires_resolve` finds a move by it, so a map named any other way is one no pointer reaches. New in the port. |

### What "a scene exists" means here

Cretaceous had a scene list with a fixed entry format, and every scene check read it. This repo has none yet, so the port does not invent one. A scene is known if it opens a line of `plan/scene-list.md` (after any heading marks), names a tracked map in `plan/scene-maps/`, or names a tracked file in `content/`. Until `plan/scene-list.md` exists, scene-membership checks are off and only the shape of an address is checked.

### The figure register does not exist yet

`shared_figures_owned` and `word_figures` both read `plan/figure-owners.md` — a `The owners` table whose first cell states each owned figure, and a `Word-form figures` table of word-figures declared not to be shared, each with its reason. Cretaceous's register is `~/code/me/cretaceous/plan/figure-owners.md`. Until that file is tracked here, both checks skip and say so; the register is a planning layer and Daniel's to approve, so the suite does not create it.

## What was left behind, and why

Each of these asserts something about Cretaceous's world or its own scene-list format, and porting one would be the suite enforcing a decision nobody made here.

- **The calendar and day checks** — `day_tokens`, `calendar_owns_distances`, `scenes_per_day`, `scene_day_tags`, `scenes_in_day_order`, `biome_covers_every_day`. Cretaceous is day-structured; this book's structure is undecided.
- **The species and biome allocation** — `reserved_species_unspent`, `species_showcase_count`, `allocation_day_agreement`, `allocation_covered`, `allocation_off_day`, `taxa_in_research`.
- **The scene-list entry format** — `scene_entry_complete`, `act_composition`, `pov_run_length`, `every_scene_moves_a_ladder`, `ending_distribution`. The ending-distribution *idea* is worth keeping: endings checked against the shape measured from Daniel's own novels for each scene's job. It needs a purpose table measured from Viking first.
- **The foreshadow ledger** — `plant_payoff_bijection`, `overt_plant_budget`, `cross_book_plants_land`, `payment_order`. They read a ledger format that does not exist here; rebuild against this repo's ledger when it does.
- **Cretaceous's renumber and id spaces** — `no_legacy_addresses`, `eliminated_unit_word`, `epigraph_count`, `identifiers_resolve`.
- **`scene_addresses_resolve`**, which checked every `D<day>.<n>` anywhere in the corpus. With a numeric scheme like `07.2` the same pattern matches every decimal in the prose, so only addresses inside `[requires]` and `[plants]` are checked.
- **`scene_map_cites_obligations`**, which reads `@D3.2`-style tags that no layer here carries yet.

## The lens tier

Not built. When it is: `@pytest.mark.llm`, deselected by default, because if the fast loop stops being instant it stops being run. Results cached by a hash of the input so a pass re-checks only what changed. Cheap seats do extraction, a frontier model does judgment, and every finding gets one short refutation call to a **different model family** before it reaches Daniel — agreement inside one family is weak evidence.
