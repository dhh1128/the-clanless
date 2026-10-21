---
approval: unapproved
---

# Rule blocks — how an AI proposes a rule Daniel can ratify

A **rule** is an invariant over the corpus, written in a fenced ` ```rule ` block inside the file it governs. An AI writes the block. Daniel reads one generated English sentence and either ratifies it or does not. Nothing else is asked of him.

Only **ratified** rules are enforced. A proposed rule is reported, never failed — and it is reported together with everything it would currently catch, because a rule that would flag forty things is telling you something the sentence cannot.

## The block

````
```rule
id:       example-one-showcase
shape:    cardinality
every:    item row in `plan/<layer>.md` §3
has:      at most 2 scenes
evidence: `plan/<layer>.md` §6 — the sentence that argues for the budget
check:    example_showcase_count
status:   proposed
```
````

renders as

> **example-one-showcase** — Every item row in `plan/<layer>.md` §3 has at most 2 scenes. *(proposed)*

The example is schematic and inherited from Cretaceous, where it was a species budget. The one live rule block in this repo today is `categorical-cites-something` in `AGENTS.md` §6.

**Where a block goes: in the file the rule is about**, beside the prose that argues for it, usually in that file's `## Rules` section. Not in a central registry — a rule collected away from what it governs is a summary file, and `AGENTS.md` §6 records what those do here.

## The fields

| field | what it holds |
|---|---|
| `id` | kebab-case, unique across the corpus. What a violation is reported under |
| `shape` | one of the five below. Fixes how the sentence renders and what a checker must do |
| `every` | the subject: what is being quantified over, and where it lives |
| `has` | the predicate: what must be true of each subject |
| `evidence` | **what the rule cites.** See below — this field decides whether the rule may exist at all |
| `check` | the function in `tools/checks.py` that enforces it. Absent means nobody has written one yet |
| `status` | `proposed`, `ratified <date>`, or `retired <date>` and a reason |

## The five shapes

| shape | renders as | example |
|---|---|---|
| `cardinality` | Every A has {at most / at least / exactly} N B | one showcase per item |
| `uniqueness` | No A appears in more than one B | a sensory item is owned by one scene |
| `bijection` | Every A has a matching B, and every B a matching A | no plant without a payoff, no payoff without a plant |
| `membership` | Every A is drawn from B | every scene a pointer names is a scene the list has |
| `ordering` | Every A comes before its B | a capability is taught before it is exploited |

Five is a guess at the right number, not a law. If a rule genuinely will not fit, add a shape and say so — but check first that it is not a cardinality in disguise, because most of them are.

## `evidence` is the field that matters

`AGENTS.md` §6: *"Preferences inflate into laws. Something Daniel said once comes back as never or one per act, and a model obeys grammar. A categorical rule keeps its force only if it cites something: a ruling, a measurement against his novels, or a physical fact."*

So: **a rule with no evidence is a guideline and must not become a test.** Do not write a block for it. Enforcing a bare preference is how a quota gets spent against like a budget, and the corpus has already been damaged that way.

Evidence is a citation to something outside the rule itself — a measurement, a physical constraint, a ruling Daniel made, a failure that cost real work. A rule inherited from Cretaceous may cite its ratification there as evidence, but that is evidence the rule worked in another book, not that Daniel wants it in this one; it is still `proposed` here until he says so. *"It seems right"* and *"the other files do it"* are not evidence. Neither is a prior AI session having written it down.

## What an AI may and may not do

**May:** add a block with `status: proposed`, anywhere, at any time. Write the checker for it. Report what it catches.

**Should:** when proposing, run the checker first and bring the violation list with the sentence. A rule is much easier to judge against what it actually flags.

**May not:** set `status: ratified`. Only Daniel does that, and the date he does it is the date that goes in. A session that ratifies its own rule has built the same trapdoor the approval frontmatter had — *unless he has just said so in conversation*, in which case the session is recording his answer, which is the only evidence this project accepts for anything.

## Ratifying

```
python3 tools/ratify.py --list          # every rule, its evidence, and what it catches today
python3 tools/ratify.py <id> [<id>...]  # confirm each, then stamp it with today's date
```

Ratifying is one word and a date, so editing the block by hand is a perfectly good way to do it. The script exists to date it, to refuse a rule whose checker does not exist, and to show what each rule catches before you answer.

**A session runs it, with `--yes`, once Daniel has said yes to the rule's sentence in conversation.** The ratification is his answer; the script records it. What stops a session ratifying its own proposal is that it may only run the script on his yes, not that it lacks a terminal.
