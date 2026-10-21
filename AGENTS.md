---
approval: unapproved
---

# Working on The Clanless

Start with `README.md`. It says what the novel is and what each folder holds. This file covers only how to work here.

Daniel is the author. You are not.

## 0. The method lives elsewhere

This novel is written under **novel-method** (`~/code/me/novel-method`). Refer to it by its path. Do not copy its doctrine into this repo. Read these before planning or drafting anything:

- `charter.md`: why the method exists, and the governing rule.
- `tensions.md`: the conflicts behind each rule, with the reasoning.
- `runbook.md`: Part A (book setup), Part B (the consistency machinery), Part C (building a scene).
- `~/code/me/novel-method/adopt.md`: how this repo references the method and feeds back to it.

novel-method has not tagged its first edition yet. Until it does, this repo follows novel-method `main` at commit `f8be96a`. Part C follows `~/code/me/cretaceous/process/scene-build-runbook.md` at cretaceous commit `23a2199`.

**Feeding the method back.** When Daniel corrects, rules on or rejects something, record his exact words with the session id and timestamp at that moment. That includes a message he types while you are busy. At each retro, sort each correction as canon, method, craft, tool or friction. Canon stays here. File everything else as a tick in `~/code/me/novel-method`, following `~/code/me/novel-method/adopt.md`, "The flywheel".

## 1. What counts as canon

- **Cordimancy is canon, and nothing else is.** That means `~/code/me/cordimancy/cordimancy.md` at cordimancy commit `64b2f69`. Every `kb/cordimancy/` fact cites it by line.
- **The Gemini files in `prompts/` are not canon and not evidence.** They were written on 2025-11-01, before this method existed, and they make claims about Cordimancy that the text contradicts. For example, the Malena dossier says she knows she is pregnant, but the novel says she only suspects it (`~/code/me/cordimancy/cordimancy.md:4122`). Use them as an index for finding lines and as a list of ideas to put to Daniel one at a time. They stay until he has gone through them, and are then deleted, with git as the archive.
- **The only test of approval is whether he recognizes it** (`~/code/me/novel-method/charter.md`, "The governing rule").

## 2. Approval and asking

Approval markers, `[?]`, `[~]` and `[-]` work as `~/code/me/novel-method/runbook.md` B1 describes. Write `approval: approved <hash>` with `python3 tools/approve.py --yes <file>`, and only after he says yes in conversation. Questions follow `~/code/me/novel-method/tensions.md`, under `questions`. His answer takes a few words, the question carries its full reasoning, and each reply asks one question, on its last line.

## 3b. When Daniel edits a file

A SessionStart hook in `.claude/settings.json` prints any uncommitted changes to the corpus. Before you touch a file, run `git status` on it. An uncommitted change you did not make is his. Commit it first, on its own, as his. Change prose only by exact-match replacement, so that an edit you did not see makes your change fail loudly instead of overwriting it.

## 5. House conventions

- **US English, everywhere.** `tools/british-english.txt` is the list. Verbatim quotations are exempt.
- **Never hard-wrap markdown.**
- **Where things go.**
  - `kb/cordimancy/`: facts from book 1, each with a line citation.
  - `kb/worldbuilding/`: new canon for this book.
  - `kb/research/`: real-world reference.
  - `plan/`: the brief, the layers, the scene list, the relationship score, the truth profiles, and `scene-maps/`.
  - `content/`: prose, one file per scene.
  - `prompts/`: what gets handed to a model.
  - `tools/`: the suite.
  - `.ignored/`: working analyses, which nothing tracked may cite.
- **Do not invent organizing schemes.** Ask before adding a folder or a naming convention.
- **Scene ids are not chosen yet.** Ask Daniel before a scene list exists.
- **`kb/worldbuilding/lingo.md` is a closed list.** <!-- @WF-lingo.closed: true --> Coining world vocabulary while drafting is a defect. Cordimancy's own terms get harvested into it, and a new term reaches the list only after Daniel approves it.

## 6. Standing hazards

**Preferences inflate into laws.** A categorical rule keeps its force only if it cites something: a ruling, a measurement, or a physical fact (`~/code/me/novel-method/tensions.md`, under `absolutes`).

```rule
id:       categorical-cites-something
shape:    membership
every:    line in `plan/`, `prompts/`, `kb/worldbuilding/` or `AGENTS.md` saying never, always, must not, not one or do not
has:      a citation on the same line — a file and section, a `@WF-` claim, or `[retired]`
evidence: ratified in ~/code/me/cretaceous/AGENTS.md §6 on 2026-10-07; a categorical rule is obeyed past the point where it was right because nothing under it said why
check:    categorical_uncited
status:   proposed
```

**Labels stand in for people.** Describe a character by what they believe, what they want and how they handle truth, not by a tag like "barren" or "the Heart". Labels in a plan become labels in the prose (`~/code/me/novel-method/sources/harvest-g4.md`, G4-22; Daniel's essay `~/code/me/sivanea.com/on-lying-and-truth-telling.md`).

[?] **The novel is strict third-person limited, rotating between characters.** <!-- @WF-pov: third-limited-rotating --> Irony comes from a POV character misreading information both they and the reader have, not from giving the reader information the POV character lacks.

## 7. Retired claims

When Daniel rules something out, the forbidden phrase goes into this table, and the suite fails on any tracked file that contains it. A line may cite a retired claim in order to correct it only if it carries the token `[retired]`. This file is exempt, because the table has to name what it forbids. Adding to the table is part of applying a ruling, not a follow-up to it.

| phrase | what is true instead |
|---|---|
