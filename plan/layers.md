---
approval: unapproved
---

# The layers: candidate list

This is runbook A3's list, for Daniel to approve before any layer is written (`~/code/me/novel-method/runbook.md` A3). Each candidate says what it owns, its grain, and which of the three directions put it on the list:

- **G**, a goal in `plan/brief.md`;
- **F**, a known failure, from `~/code/me/novel-method/charter.md` ("The failures it was designed against") or `~/code/me/novel-method/tensions.md`;
- **H**, a dependency that recurs across the hand-maps (`plan/hand-maps/SYNTHESIS.md`).

A candidate is a layer only if it allocates something to specific positions in specific scenes, or owns facts that several scenes share. Anything else is reference and goes in the knowledge base, listed at the end. Every entry is a proposal `[?]`.

## Layers

| # | layer | owns | grain | from |
|---|---|---|---|---|
| L1 | **Arcs and dilemmas** | Each principal's starting posture at the end of Cordimancy (canon), the rungs of their arc, and the scene where each conscious dilemma comes due and each blind spot is exposed. Draws on `plan/truth-profiles/`. Owns the failure *"too much or too little movement from the emotional posture/maturity of characters at the end of Cordimancy."* L1 owns what a break means; L5 owns the count before it. | book | G (arcs, moral texture), F (failure list in the brief) |
| L2 | **Labels and names** | Per character: each label pinned on them, by whom and where; the name they hold; and the rung they're on, scene by scene, up to the exiles taking *clanless* as a name. After that rung, each scene where the outside world's use of the label presses on someone, so the inversion is enacted and not declared once. | book | G (*"Labels are imposed; names are chosen and held"*), H (LABELS AND NAMES) |
| L3 | **The band** | Who is in the clanless group in each scene, when and why each joins or leaves, and the unstated principle that holds them, *"love even at extremely high cost."* The group as a unit, apart from the pairs. Two fields per scene: who still feels outside inside the band (*"the feelings of isolation need to be real"*); and whether a welcome in that scene reads as wages for usefulness, which would confirm Kinora's and Oji's blind spots instead of answering them. | book | G (*"the title's meaning inverts"*) |
| L4 | **Relationship score** | Runbook A7: per day, each relationship's state, what carries it, the backstory items spent, and the threads that travel: the acorn, the antechild's shards, the staff, Cricket's name, as relationship carriers (L10 owns their plants and payoffs). Day grain is the runbook's default; whether a road book needs scene grain is open. | day | G (costly loving relationships), H (OBJECTS that travel) |
| L5 | **Pressure** | What each character holds down (anger, a secret, a defense), since which scene, how many times it's been swallowed, and where it breaks. | book | H (PRESSURE), F (`withholding`) |
| L6 | **Knowledge ledger** | Who knows what, and when, for every load-bearing fact: Malena's pregnancy and its father, Rovin's frame of the priest, the indenture, the frozen estate, Luim's fate. Reader, each POV, and the clan. Rotation as a source of irony (ruling, Q-XV7A) lives here. | scene | F (logic, `intensity`), H (READER) |
| L7 | **Journey, bodies and resources** | Calendar and geography of the road north into winter; food, cold, horses, money (the freeze and the money outside Kelun, `plan/truth-profiles/corim.md`); the months of Malena's pregnancy and little Paka's birth; days of Oji's life burned in each aiki trance. | day | F (logical impossibility, scenes that don't join) |
| L8 | *(folded into L9, see below)* | | | |
| L9 | **Stakes, hooks, relief and crises** | The stakes curve; a hook per chapter built from approved material, chained so each deepens the last; relief and comedy placed per scene, so the book doesn't turn bleak. For each crisis, what decides it (a choice, a sacrifice, love, or force and magic), keeping *"the power that matters is not the talent anyone was renowned for"* true. Per chapter, the share given to magic and plot against relationship beats. For the climax, the order in which each principal's payoff lands. | chapter; relief by scene | G (*"weep in frustration and worry as stakes mount"*, not bleak), F (`hooks`, `relief`) |
| L10 | **Plants and payoffs** | Each plant, its payoff, and the plants for book 3 (`plan/sequels.md`). | book | G (*"we don't set up book 3 well enough"* is a failure), H (plants in every map) |
| L11 | *(moved to reference, see below)* | | | |
| L12 | **Milieu allocation** | Runbook A5's fourth product: per-scene sensory and species budgets, one showcase per thing, so the same details don't recur. Waits for the scene list. | scene | F (same adjectives and milieu details), G (*"a rich milieu"*) |
| L13 | **The clan and its antagonists** | Every action the clan takes against the band, and why it is logical from inside: Rovin's freeze, the indenture, the clanless sentence. The trap each antagonist is in, and the scene where the reader sees it (*"trapped in their own bad assumptions, not deeply evil"*). Those who stay inside the clan, Veshumi above all, and the scene that makes each one *"understandable, and heart-rending."* Gorumim's trajectory on and off the page toward book 3. | book |

## Reference, not layers

These own facts but allocate nothing, so they go in `kb/` or stay where they are:

- the cast register (`plan/cast.md`) and the backstory register (`plan/backstory.md`);
- the truth profiles (`plan/truth-profiles/`), which L1 and L2 draw on;
- the closed vocabulary (`kb/worldbuilding/lingo.md`);
- the magic system, with each capability's cost and limit, and the mythology, separating what is true from what is believed (runbook A5);
- Kelun's law of clans, property and indenture, including whether Two Forks is under Kelun's law (open);
- the style canon (`prompts/style-canon.md`);
- **voices**, formerly L11: each speaker's idiolect and register (Oji's compound verbs, Gitám's uncontracted speech, ruling Q-ZG39, Kinora's child's words and reasoning, the pet names). It is static across the book, so it is reference. A change, such as a pet name earned or the word *daughter*, goes in L2 or L4;
- rites and liturgy (the naming rite, Gitám's invocation, the blood-brother rite for book 3), with each use tracked in L10.

## What the hand-maps put in the scene-map form, not in a layer

SUBTITLE, NEGATIVE SPACE (shape approved, Q-ZN70), OBJECTS (meaning to each person in this scene), TRUTH (which profile behavior the scene enacts), and RHYTHM. These belong to one scene each. They go to A4.

## The outside-model check

Run with two seats from different labs, DeepSeek (`ds`) and Gemini (`gemini`), given the brief, this list and `plan/sequels.md`, and asked to refute it. Their answers are summarized here with what was done.

- **Both: nothing owned the antagonists, the clan's pressure, or those who stay.** Adopted as L13.
- **Both: the band coheres too early, and isolation stops being real.** Adopted as a field of L3.
- **Gemini: belonging written as wages.** A survival plot invites scenes where Kinora or Oji earns a place by usefulness or by burning life, which would confirm their blind spots (`plan/truth-profiles/kinora-and-tupa.md`, `plan/truth-profiles/oji.md`). Adopted as a field of L3.
- **DeepSeek: the inversion declared once in dialogue and then dropped.** Adopted as a field of L2.
- **DeepSeek: magic and plot occupying scenes, and climax payoffs scattering.** Adopted as fields of L9.
- **Both, on scope.** L8 folded into L9, since a book has few crises. L11 moved to reference, since an idiolect is static. L4's traveling objects belong to L10 for plants and payoffs. Relief in L9 is placed per scene, not per chapter.
- **Declined: folding L2 and L5 into L1 and L4** (Gemini). The three count different things: arc rungs, label rungs, and swallowed pressure. Their boundaries are now stated in L1 instead.
- **Declined for now: a per-scene POV field in L6** (Gemini). POV is assigned in the scene list.
- **Open: L4 at day or scene grain** (Gemini). Left as the runbook's default until the scene list shows how days and scenes relate.
