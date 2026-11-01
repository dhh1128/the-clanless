---
approval: unapproved
---

# Style canon

Verbatim passages from *Cordimancy*, the book *The Clanless* continues, with a measured fingerprint. This is the primary voice instrument for drafting (`~/code/me/novel-method/runbook.md` A2). It is built from Cordimancy alone. Viking, which the Cretaceous canon (`~/code/me/cretaceous/prompts/style-canon.md`) weights two to one over Cordimancy, is a different book in a different register and drops out here.

Source: `~/code/me/cordimancy/cordimancy.md` at cordimancy commit `64b2f69`. Citations are `:LINE` in that file and point at the first line of the passage; every line in the source is one paragraph. Quotations were extracted from the source by script, not retyped, and `[...]` marks an elision. Front matter (lines 1–33) and the end matter after line 4753 are not prose and are excluded from everything below.

The passages are the instrument. The numbers are diagnostics for checking a draft after it exists, and none of them is a target to write toward. The scene-level analysis behind the sections is in nine hand-maps of Cordimancy scenes, `plan/hand-maps/`, summarized in `plan/hand-maps/SYNTHESIS.md`.

---

## 0. The fingerprint

### Method, so it can be rerun

The numbers come from `python3 tools/style_fingerprint.py ~/code/me/cordimancy/cordimancy.md`. The method is in the script's docstring: dialogue is text inside straight double quotes; the italic channel is any `*...*` span of three or more words outside quotes; narration is what remains; sentences split after `.`, `!`, `?` or `…`; attribution fragments (a narration sentence of six words or fewer, beside dialogue, with a speech verb) are counted and kept out of the narration rates. Each chapter's subtitle line is dropped. Scenes are assigned a POV by reading (`SIDES` in the script): Toril, Malena, Kinora, the outside narrator (`:1467`, `:1517`), the three italic scenes with Gitám, and the tale Paka narrates (`:3899`).

### Numbers — diagnostics, not targets

| | whole book | Toril | Malena | Kinora |
|---|---|---|---|---|
| words | 125,783 | 54,570 | 56,477 | 9,466 |
| dialogue share of words | 32.1% | 34.3% | 28.5% | 38.0% |
| **narration** sentence mean / median | 12.2 / 11 | 12.3 / 11 | 12.0 / 10 | 12.7 / 11 |
| **narration** ≤5 words | 22.5% | 22.3% | 23.3% | 21.2% |
| narration ≥30 words | 3.9% | 4.2% | 3.7% | 2.9% |
| **dialogue** sentence mean / median | 9.3 / 7.5 | 9.2 / 8 | 9.1 / 7 | 10.3 / 8 |
| **dialogue** ≤5 words | 35.5% | 35.1% | 36.9% | 32.5% |
| narration-only paragraph, mean / median words | 29.5 / 24 | 29.5 / 24 | 28.5 / 23 | 29.9 / 24 |
| narration-only paragraphs that are one sentence | 39.1% | 37.6% | 41.0% | 39.5% |
| dialogue-bearing paragraph, mean / median words | 28.2 / 22 | 27.6 / 22 | 27.8 / 21 | 35.8 / 29 |
| attribution fragments per 1,000 words | 7.3 | 7.9 | 7.1 | 5.9 |
| narration questions per 1,000 narration words | 5.6 | 4.9 | 6.6 | 3.3 |
| contractions per 1,000 dialogue words | 47 | 45 | 52 | 44 |
| chapter length, median words | 2,210 | 2,158 | 2,304 | 1,006 |

Other measures, whole book: semicolons to colons in narration **379 : 11**; em-dashes 4.4 per 1,000 words; ellipses 2.2 per 1,000; *as if* / *as though* 40 times. `said` 448, `asked` 107, `whispered` 50, `sighed` 24. Of dialogue-bearing paragraphs, about half carry a speech verb in a short narration sentence, a quarter carry an action beat only, and a quarter carry nothing but the speech. A run of consecutive dialogue paragraphs has a median of 2 and a longest of 24. Across 110 scenes, the median scene is 983 words with 31% dialogue; nine scenes have no dialogue and twelve more have under 5%.

### What the numbers say

**The three POVs are close.** Toril and Malena differ less than Viking's two sides do. Malena runs a little more interior (28.5% dialogue against Toril's 34.3%) and asks herself more questions (6.6 per thousand narration words against 4.9). Kinora's chapters are half the length and talk more. The voice differences between the POVs live in what they notice and how they reason (§1–§3), not in sentence statistics.

**Tags are plain, and present only when the reader needs them.** Daniel: *"I tend to tag mostly when I feel it's necessary for clarity … The use of plain words is absolutely deliberate; using colorful words for tags is a distraction and a tic, I think. Tags should be mostly invisible, just enough to help the reader follow the conversation with confidence. When they're not needed, they should be dropped. (Cordimancy may be imperfect in this respect, but that's my aim.)"* Cordimancy carries 7.3 attribution fragments per thousand words, against 1.9 for Viking by the Deep Resonance canon's count, but the rate is not the lesson: it may only mean that Cordimancy's conversations have more speakers, or speakers who are harder to follow. The lesson is the choice of verb (`said` 448, `asked` 107, the colorful ones rare) and the test for each tag: does the reader need it to know who is speaking?

**Short narration sentences do not cluster at paragraph ends.** Of 1,510 narration sentences of five words or fewer, 567 are a paragraph of their own. Inside multi-sentence paragraphs they take the final slot 28.8% of the time, below the chance rate of 33.1%; they open paragraphs more often than they close them. The Cretaceous canon's §0 claims short sentences cluster at paragraph ends as closers. That claim does not hold for Cordimancy.

**Action has two rhythms** (`plan/hand-maps/SYNTHESIS.md`, RHYTHM). Where a body grapples a body, narration runs long, 14–17 words a sentence, with one verb carrying a chain of consequences (§8). Where the POV perceives a group fight in poor visibility, it runs 9–10 words, one event per sentence (§9). Daniel calls it intuition, not a rule he holds (Q-GXBE).

**Gitám does not contract** (§10): 7.5 contractions per thousand words of his speech, against 47 for the book. That is deliberate and belongs to Gitám, not to every Speaker (Q-ZG39).

**Discrepancies with earlier figures.** The Cretaceous canon gives Cordimancy as 124,545 words, mean sentence 11.0 / median 9, ≥30 words 2.2%, semicolons to colons 474 : 18, `said` 492, `asked` 124. This run gives 125,783 words and a blended 11.1 / 9, ≥30 2.9%, narration semicolons 379 : 11, `said` 448 in attribution fragments. The differences are method: this count drops chapter subtitles, counts semicolons in narration only, and counts `said` only in attribution fragments. The edition is the same.

## 1. Toril's interior

Toril thinks in questions, argues with himself, and catches himself out. In these passages his interior is a chain of reasoning that turns on itself, not a summary of his feelings.


**[reasoning that turns on itself]** `:1812`

> Toril made it through two switchbacks before he turned around. By then rational thinking had penetrated the anger knotting his gut.
>
> Barely.
>
> No hoofbeats from the old couple or the priest had sounded at his back. He'd listened for them, but been too proud to look over his shoulder, or even to glance downhill at each pivot in the switchbacks, to see who might be following.
>
> Nobody, that's who.
>
> Of course Malena wouldn't have changed her mind.
>
> They were all going to charge off into the wilderness on a fool's errand.
>
> It was a losing proposition for everyone—the children, who stood almost no chance of rescue; the soldiers headed to a battle that was worse than unnecessary; the families of the men who would die…
>
> Following Malena would be a disaster for the reputation of Hasha, for the parijan, and for Toril, personally. He'd be demonstrating a lack of judgment, a willful disregard for the wellbeing of the clan, a cavalier intransigence in dealing with Gorumim and the raja.
>
> He'd told Vasari that only Malena's imminent death kept him from putting an end to Rovin's stupid warmongering. He'd said he wasn't afraid of confronting his rival.
>
> And now he was supposed to run in the opposite direction? Nobody would see altruism in that course…
>
> Besides, if Malena was right about her sister being among the missing children, then what his wife wanted would further endanger her, as well.
>
> In a day or a week, when they'd definitively failed, would Malena turn around and blame him for listening to her?
>
> Would he be able to forgive himself?
>
> Why couldn't Malena set aside her own preconceived notions long enough to consider the possibility that he had the same goal she did, and that his judgment was worth respecting?
>
> A little voice in Toril's head picked up on that last thought, and repeated his words dripping with irony. Had *he* been willing to set aside *his* preconceived notions? Or was he just as dismissive of his spouse's reasoning as she had been?

Anger first, then the case for his side in one-line paragraphs (*"Barely."* *"Nobody, that's who."*), then a run of questions, then the turn: *"A little voice in Toril's head picked up on that last thought."* The self-correction is the move. He doesn't decide in this passage; the decision comes later in the chapter.


**[grief in a burial garden, by way of a bird]** `:1259`

> Blinking to clear smoke from his eyes, Toril trudged back through the warren of streets on the hillside north of the durga. He'd been carrying corpses all day, making piles and dousing them with tar, then summoning flame with his torch to consume the death. The stench was in his hair and lungs; his thighs and the small of his back ached in protest.
>
> Was Malena awake? Would she be any better when he reached his quarters?
>
> Rounding a corner, he saw a ruby-throated yellowtail chirping on a remnant of thatch, and paused to observe. The contrast between dull scorch and extravagant feather, mute death and birdsong, struck a chord in his heart. He felt a glimmer of hope. Even here, even now, life flew and trilled…
>
> He whistled.
>
> The bird cocked its head for a moment, warbled, then fluttered away.
>
> He lowered his head and walked on.

Exhaustion in the body, two questions about Malena, then a small living thing that gives him hope and flies away. *"He lowered his head and walked on."* The feeling is in the bird's leaving, not in a sentence about hope.


**[waking heavy, consoled by a place]** `:4012`

> Hours later, Toril kneaded neck muscles and inhaled as he yawned, gathering cool air into his lungs. His body and mind felt refreshed, if not exactly energetic. Yet a sort of weariness still lurked. Would he feel… quick, or carefree, or… buoyant, ever again? Or would the awfulness he'd seen in recent days weigh on his heart and his bones forever?
>
> Morning sunshine had blanketed the glade as Toril and his companions closed their eyes. Now the four stars that formed the lips of The Maiden were dropping behind the mist at the west edge of the glade, and sky in the east was graying. Toril's stomach twisted again with hunger. He hadn't expected such a long hiatus. He felt uneasy about it.
>
> Shivi had wakened him, not Paka. Who else had played the sentry while he snored? Had Oji?
>
> He should have planned better. But he hadn't been thinking clearly…
>
> He tightened his belt and stood.
>
> In pre-dawn dark, the oak emitted a silver glow from every vein and stem in its leaves. Though no breeze blew, he thought he caught a rustle from the branches as well—a musical murmur of peace.
>
> Such a tree! Such beauty, in the very center of wasteland…

A question about his own heart, practical worry (*"Who else had played the sentry while he snored?"*), self-reproach in four words, and then the oak. Interior moves to place without a transition.


## 2. Malena's interior

Malena's interior is quicker and more self-accusing than Toril's, and she argues against her own unfairness. Her narration asks 6.6 questions per thousand words, the most of the three POVs.


**[arguing herself out of blaming him]** `:2419`

> Part of it, she thought, was the way he'd jumped in to rescue, when she had asked him not to. It felt patronizing, offended her expectation for independence. Wasn't she capable of deciding what was best for herself? What gave him the right to meddle? Did she want a husband who ran rough-shod over her feelings like that?
>
> He'd caused this mess in the first place, by leaving her alone and provoking Gorumim to strike.
>
> She shook her head. No, that wasn't fair. Wasn't even accurate. She might be angry at how he'd tried to fix things, but he had not been negligent. She didn't really even believe he'd been prideful—just battered by a whirlwind of malice, the same as her.
>
> Could she really believe in the wrongness of Toril's rescue, even? If he'd left her to die, who would be trying to rescue children now? What hope would Tupa have? She'd reproached herself for cowering in the stable; wasn't her embracing death a similar form of hiding? Was it cruel of this unfamiliar man to pull her back into life, with all its tears and demands—or was it just… what had to be done?
>
> Maybe what hurt her most was his motivation. Yes, he'd sacrificed to yank her back from the brink of death—but had he really done it unselfishly? Now he expected her thanks, her closeness. Her future. Her partnership…
>
> Her body.

She builds a grievance, then dismantles it: *"No, that wasn't fair. Wasn't even accurate."* Then she finds the real one, and it is two words long: *"Her body."*


**[the truth she can't say]** `:2428`

> She had been counting days. She had not meant to begin; the number had simply been there one morning, and it had not gone away since.
>
> Perhaps it meant nothing. She had bled little and eaten less, and her body had been hauled back out of death by a magic that nobody understood—surely that was enough to throw off any rhythm a woman kept. Perhaps the sickness in her belly was only fear. She had swallowed fear by the mouthful for days.
>
> Perhaps.
>
> She pressed the heel of her hand beneath her ribs and made herself finish the thought, because refusing to finish it had never once made it smaller. If she was carrying, it was not her husband's.
>
> There was no version of that she could say aloud. Not to Shivi. Not to Toril. Not, in daylight, to herself.
>
> So she would not say it. Not yet.
>
> She studied the shadows the moon cast across her husband's face. The shadow below one cheekbone gave him a gaunt look. The muscles of his lips and cheeks slumped in a mask of exhaustion, dead to the world. His head rested on the shoulder of one outstretched arm. It made a poor pillow; his neck bent at an angle that augured stiffness in the morning.
>
> Impulsively, she reached for one of her knee-high boots. Her hands worked the leather into a roll with the sole inside. She leaned, slid fingers beneath Toril's ear, lifted his head, and inserted the makeshift cushion.

The pregnancy is approached by counting, then *"Perhaps."* three times, then finished *"because refusing to finish it had never once made it smaller."* And then the boot under his head: tenderness as an act, with no thought attached.


**[her mother's heartstone]** `:4116`

> The heartstone her mother wore was a gaudy ruby, Malena knew. She'd never seen it, of course, but her mother had dropped hints. "Your father's treasure box holds only half our net worth, Malena," she'd said. "I only know one jewel finer," she'd said. "A man shows his priorities by what kind of stone he hangs," she'd said. "Your father mortgaged an entire estate to buy it. Nobody could believe his extravagance."
>
> As a girl, Malena had been impressed. The biggest, most precious gemstone in all the Sumago Mountains hung at her mother's heart.
>
> Later she heard loneliness and self-doubt in her mother's proud whispers, and Malena grieved for it. She allowed herself to hope for a better tenderness from the man who hung his heartstone around *her* neck.
>
> Yet when she'd found exactly that, she'd thrown it away.

Her mother's voice in fragments, each tagged *"she'd said"*; the girl impressed, the woman grieving for her mother; then one line that turns the whole memory on herself.


## 3. Kinora

A child's words and a child's reasoning, and the narration stays inside both without correcting them (Daniel: *"Not only does she speak like a child, she also thinks like one"*). Kinora's chapters are the shortest in the book, median 1,006 words, and her scenes have the most dialogue, 38%.


**[naming him]** `:2688`

> "You were making a funny noise last night while you slept," she murmured, forcing a curve onto her lips. "Sort of a snore with a little chirp at the end. I liked it. Can I hold you tonight and let you be my little cricket?"
>
> *How could he go so long without blinking? Why wasn't he responding at all?* His arms and legs were limp.
>
> "You have to sit up," she hissed. "If you won't, they'll just…" She swallowed. "And then I won't have my cricket tonight."
>
> She sniffled. The distant rushing of the river filled her ears. Dappled shadows from the trees slid back and forth. Overhead, an eagle's cry faded into the wind.

She names the boy after a sound he makes in his sleep, and asks his permission. The stakes come in a child's form: *"And then I won't have my cricket tonight."*


**[asking a mute child to be brave]** `:3120`

> "Just a little blink?"
>
> Coffee-colored eyes continued to stare.
>
> Kinora put a hand over the boy's half-open lips and waited so long that her heart began to pound. At last, his chin lifted slightly. His nostrils were too crusted with dried mucus to route air; he needed his mouth uncovered. A faint wheeze of inhalation ensued.
>
> "That's better," she sighed, parting the tangles above his eyebrow.
>
> She peered through the reeds again.
>
> "Can you be brave, little Cricket?" she asked, without turning her head. "Can you?"

Testing his breath by covering his mouth is competence, not childishness. The asks get smaller as her fear grows: a blink, a little blink, bravery.


## 4. Pressure in company

Family and clan press on someone in front of witnesses. The pressuring party is sympathetic, the refusal is carried as much by the body as by words, and the anger is held until it breaks.


**[a signet refused by stillness]** `:228`

> Her father crossed the room and put his hands on Malena's shoulders. "Good," he said softly. "I've worked all my life to get us here. We're not flirting with poverty anymore. We're a respected family. It's been twelve generations since the line of Shavir held the staff of clan chief; you can restore us to the status we deserve. I'm proud of you, and of the match you've made."
>
> "I understand."
>
> He straightened, thrust a hand into the gap at the split of his *kurta*, and pulled out a pouch that hung beside his heart. When he upended it, an ornate ring dropped into the palm of his hand. He held it out to Malena.
>
> She stared at the gold band. It was a man's ring, bulky rather than delicate—meant for fingers thicker and longer than her own. A square emerald the size of a thumbnail was bracketed in the metal, diamonds studding either side. The band itself had a serpentine inlay of lighter gold alloy that circled the ring. It was a precious heirloom.
>
> She did not move.
>
> "Take it!"
>
> Still Malena stared straight ahead.
>
> Her father stepped to the chest that servants had carried in and laid at the foot of Malena's bed. He threw back the lid, tossed some clothing aside, and puffed as he dragged the chest into Malena's field of view. A shaft of green porcelain lay on velvet, protruding from a burst of white petal shapes and a disc that had been painted daisy yellow. Beside the flower sat an ocarina. The instrument—also ceramic—sparkled with the fire of mica-enhanced glaze, but it had been repaired. Its body was cracked and worn.
>
> "This is what you propose to offer as an antechild?" her father demanded. "Instead of Shavir's signet? What can you be thinking?"

The father at his best (*"I'm proud of you"*) immediately before the refusal. *"She did not move." "Take it!" "Still Malena stared straight ahead."* Three short paragraphs carry the turn.


**[the vote]** `:820`

> "I'm ready to vote," said one man.
>
> "Yes, let's get this over with," agreed another.
>
> "Who will heed my call?" the shimsal asked.
>
> One by one, Toril heard men stab knives into the spruce.
>
> "Kelun?" the shimsal said.
>
> When the silence became deafening, Toril opened his eyes. No one had kept their dagger sheathed. They were all staring at him.
>
> Toril swallowed. "My answer is no," he said, a faint unsteadiness in his voice. "Kelun might muster men for other plans, but not this one. In a crisis, pre-emptive harshness will just deepen the misery of our neighbors and make them permanent enemies."

Isolation by sound before sight: the daggers go in one by one while his eyes are shut. *"Kelun?"* is two words of dialogue; the silence before his answer is a full paragraph.


**[the break, and the apology]** `:834`

> "Don't blame me for a burden that you are eager to carry!" Toril shouted. He saw the shocked looks on the faces of his peers and suspected he'd gone too far, but the anger he'd tried so hard to repress came tumbling out. "You arranged this conference at the worst possible time, hoping Kelun wouldn't come at all—or that if we did, it would be in the form of some puppet whose strings you could pull. You've given rumors of a threat, not proof. And you want an irrevocable commitment to an open-ended war. Well, Kelun does not dance at your bidding!"
>
> Toril stopped.
>
> He listened to his breathing against the silence around the table, and grew sick.
>
> He cleared his throat. "I am sorry. My feelings got the better of me. I have no wish to be defiant, only careful and kind. I trust the raja to understand that when he hears me out."

The longest paragraph in the scene, then two words: *"Toril stopped."* The apology is immediate and unforced. The reader has watched him swallow his anger three times before this.


## 5. Talk on the road

Found family is built in argument and teasing. Each speaker has an idiolect, the point is often shown rather than argued, and the theme may be stated if a character with standing says it to one person.


**[Oji's speech]** `:2332`

> "Not enough time to live?" said Oji, raising a hand in a gesture of disbelief. "I day-live more than you week-live."
>
> "You eat lots of meals. You sleep several times. That's not the sort of living that I mean."
>
> "It's not the living I mean, either. We live faster, human. As you bounce once in the saddle, my heart beats half a dozen times, and my thoughts fly apace. It is tiresome to speak to you, when you dawdle to choose thoughts and word-put them."

Oji fuses compound verbs (*"day-live," "week-live," "word-put"*) and calls Toril *"human"* and *"stonecaster."* He is impatient, and funny about it.


**[shown, not argued]** `:2358`

> "What color do you see?" Oji demanded. "What color are the petals?"
>
> Toril looked back, decided the group was too spread out anyway, and swung out of the saddle, groaning a little at muscles stiff from hours of riding. "White?"
>
> Oji waited.
>
> "With a splash of yellow and blue in the center."
>
> Still Oji waited.
>
> "I don't see what you're getting at." He'd seen their like many times before; they were nothing remarkable.
>
> Although he'd had to hunt for the yellow. Dust, he decided, and the flatness of the afternoon light.
>
> "My people call these speckled lilies. They're fleck-covered the color that rainbow-follows violet."
>
> Toril stared at the triplet oval clusters. Was Oji inventing this just to prove a point? He saw no speckles. Wasn't violet at the edge of a rainbow? His eyebrows knit. He had felt an amazing sensory burst long ago, when he'd braved the river and tasted the fork of the half lives for a while. But it seemed hazy and a bit hard to credit, now.
>
> Oji laughed at his puzzlement. "Did you think the sata were the only ones experience-trading years? I may not have your lifespan, but I can smell these flowers or a beautiful woman a hundred paces away. And I will not dotage-linger like you; I will snuff suddenly, like a candle at its wax end. Is that such a bad trade?"

The argument has no winner until Oji stops and makes Toril look. *"Oji waited." "Still Oji waited."* The waiting is the pressure. The answer is a flower and a laugh, then the arithmetic of his short life.


**[a gift that doesn't fit]** `:2396`

> She approached the older woman and held out the woven rushes she'd been working since morning.
>
> "It's not much of a hat, I'm afraid," Malena said. "You of all people would know that."
>
> Shivi looked from Malena's hands to her face and smiled warmly. "The shade will be welcome tomorrow. Thank you." She ran fingertips along the brim and pursed her lips. "You used the plowman's weave here."
>
> Malena nodded. "I tried, anyway."
>
> "It's a good choice for holding an edge together; the twist locks the bend when it dries. But it's not a common technique in Kelun mountains. Did someone teach you?"
>
> Malena shrugged. "I saw it in some baskets when I was young. It was interesting, so I found the pattern in a book and practiced until it looked right. But this is the first time I've done it for other eyes."
>
> "You practiced well," said Shivi, allowing the hat to settle on her head.
>
> It sank over her eyebrows.
>
> "I guess I should have measured first," Malena said, feeling that her gift was every bit as ridiculous as Shivi looked.
>
> Behind her, Paka had ceased humming and laid aside his sitar with a plunk. Now he transformed a snort into a cough.
>
> "Don't mind him," Shivi said primly, as she bent a coil of her silver braid into Malena's clumsy hat to take up space. "Every weaver makes mistakes. I know I've made plenty."
>
> Paka put a hand on Malena's shoulder. The corner of his eyes crinkled, and his beard lifted at the edges of his mouth.
>
> "Actually," he said, leaning over to kiss the tip of his wife's nose. "I was thinkin' that with a brim like that, my wife can get away with all the steamy winkin' she wants, and nobody but me the wiser."
>
> And he turned and coughed again.

Comedy carried by kindness: the hat sinks over Shivi's eyebrows, she bends her braid into it to make it fit, and Paka turns his snort into a cough and then a joke about winking. Nobody mocks Malena; the warmth is the joke.


## 6. The marriage

Toril and Malena talk, and get each other wrong out loud. What each cannot say is the largest thing in the scene. Tenderness is often an act done while the other is asleep.


**[care while he sleeps, and after]** `:2262`

> Toril curled nearby, surrounded by mounds of pine needles. His face looked pale, weary; a bare sole half-poked into the light. Hika lay on one side of him, his staff on the other, endcap glinting.
>
> Why did she find herself able to feel empathy or good will for her husband more when he was asleep?
>
> "Lavender tea?" Oji suggested. "Shivi told me to keep it warm." He extended a tin cup.
>
> Malena curled her fingers around the hot metal and sipped gratefully.
>
> When her fingertips had lost their pink, and her belly gurgled with warmth, she worked her boots off and hung them upside down on sticks jammed in the dirt near the fire. She was just finishing when she remembered that her bedding was in the saddlebags.
>
> She winced in regret. The rough footwraps she wore could scarcely get wetter, but the ground was muddy and full of pine cones and rocks. And at last she was not cold. Was it worth pulling the boots back on again?
>
> Oji's voice caught her as soon as she stood and stepped away. "He already laid out your stuff."
>
> Malena rotated on her heel, eyes scanning the margins of the firelight. Beyond the boots, in the overhang of another spruce, she saw a beige blur with cream along the edge.
>
> The sheepskin was spread on a knee-deep bed of dry needles. When she pulled it back, the aroma of toasted spruce tickled her nose. Two melon-sized stones nestled in the piles of padding, still radiating heat from the fire. Atop one lay a pair of clean, dry footwraps.

Her empathy comes *"more when he was asleep."* Then Oji tells her what Toril did, and she finds it: dry needles, hot stones, clean footwraps. His care is shown entirely through objects.


**[a small yes]** `:4050`

> "I can't… reciprocate," Malena choked out, leaning her head sideways. "I just… can't."
>
> "Not even a smile, now and then?"
>
> Malena's face went white. "You think I haven't tried? What do you think it costs me to sit next to you, speak to you in a calm tone of voice, *sleep* next to you?"
>
> Toril leaned back and blinked several times. "I don't understand why it should 'cost' you anything. I'm only talking about simple courtesy."
>
> "You're *not* talking about courtesy! You don't want polite nods and respectful conversation between strangers; you want a wife."
>
> "Well, of course I want a wife," Toril said, his voice rising. "Why do you think I got married?" He could hear the tremble in his tone. "Why did you?" He heard his own volume, swallowed, and took a breath. "I don't pretend to be a perfect spouse, but I haven't been cruel or evil. And I've stayed at your side. You think that was easy for me?"
>
> Malena's reply, when it came, sounded forlorn.
>
> "No." She averted her gaze and sat for so long that Toril almost thought she had ended the conversation. At last she continued in a husky murmur, "No. Not easy."
>
> Toril reached out, hesitated, placed a hand on her shoulder. At first she stiffened; then he sensed a gradual relaxing. It wasn't a moment of warmth, exactly—but at least it wasn't a rejection.
>
> "I can try to be friends, Toril," she said, her voice scarcely audible. "Can we just start there?"
>
> Toril stood, not speaking, not removing his hand, gazing with Malena into the wall of darkness at the edges of the glade. He felt tears of his own brimming. This woman would *consent to try* to be his friend?

She goes white: *"What do you think it costs me to sit next to you, speak to you in a calm tone of voice, sleep next to you?"* He doesn't know why it should cost her anything; the reader does. The scene ends on *"consent to try,"* and his tears.


**[the wrong gift]** `:4068`

> "Didn't you hear what I just said?" Malena asked, her voice tense. The undercurrent of anger in her tone was unmistakable, and Toril felt confusion and hurt swirl.
>
> He opened his mouth, but no words emerged.
>
> She grabbed the heartstone out of his hands and held it up near his nose, the chain dangling. Her hand was trembling.
>
> "This isn't just jewelry, Toril, and I can't ignore the traditions around it. It isn't a token of friendship! It's a symbol of marriage—*consummated* marriage. Intimacy in every sense of the word. The very thing I'm afraid of. The exact pain…"
>
> Her voice broke.
>
> "I just want to feel more connected to you," Toril ventured.
>
> "We're *not* connected! And if you keep pushing, we'll *never* be connected!" Malena yelled. She attempted to yank the stone; when the chain caught on his fingers, she jerked a second time, wild with anger. Toril felt a sting at his hand as the chain broke.
>
> Her eyes had gone somewhere else.
>
> He had seen that look once before—on the road outside Two Forks, over the point of a dagger she could not stop pushing toward his heart. By the time he understood what he was seeing, it was too late.
>
> Malena flung the stone away.
>
> Green flicked from his eyes. He heard clatter fade into billowing haze.
>
> Malena looked up, registered his stare, and seemed to realize the import of what she'd just done. Her face contorted. She looked toward where the stone had vanished. Then, before Toril could stop her, she darted away, disappearing into the same darkness.

*"The exact pain…"* breaks off, and the scene leaves it unfinished. Her dissociation is shown by her eyes and by the memory of the dagger. The stone's loss is a color and a sound: *"Green flicked from his eyes. He heard clatter fade into billowing haze."*


## 7. A hard truth told with love

Someone with standing refuses both the comforting lie and the cruel one.


**[shame, and a palm on the cheek]** `:4321`

> "No." Shivi shook her head. "Of course you didn't." She waited for a while, allowing her words to sink in. Then she reached up and put a wet hand on Malena's chin, fingers demanding, turning her face and pulling her forward until their two faces were closer. "Let's not have any misunderstanding, though. You might not have intended harm, but you knew you were being selfish and stubborn. And it was doubly hurtful to repeat the same mistake all over again just now. Shame on you for that." She tugged on Malena's jaw for emphasis, then released her grip and laid a palm tenderly against her cheek.
>
> It was such an odd comment—sharp but lacking all rancor—and the hand at the end was so different from the fingers at the beginning, that Malena jerked her head in surprise. Shivi's hand found her cheek again.
>
> "What?" Shivi asked. "You thought I would say not to feel guilty? Not to worry? That it didn't matter?"
>
> Malena opened her mouth, then closed it again. She didn't know how to respond. What was Shivi saying?
>
> "Claiming you killed someone is a lie, Lena. It isn't fair. Gorumim—and those pishachas—killed someone. They might have done it regardless of your choices; we'll never know. On the other hand, saying you didn't hurt us would be a lie, too," Shivi said. She pushed hair out of Malena's eyes, then returned to stroking her shoulder. Malena felt a warmth spreading up her neck. "And saying I forgive you because it wasn't so bad would be a counterfeit forgiveness. It would ring hollow in your heart, and mine, and cheat us both. Forgiveness isn't finding a way to minimize what someone else has done. It's not offering them cheap absolution, or talking yourself into some weird way of seeing things that pretends the pain is not a problem."
>
> "I… don't understand," said Malena, shivering both from emotion and from the cool water.
>
> "Forgiveness is refusing to let the darkness have the final say in your heart. It opens its eyes completely, willing to see the good, the bad, and the ugly as they really are. And then it chooses to love anyway. Like Paka did. Like this." And Shivi wrapped her arms around Malena, squeezing fiercely.

*"Shame on you for that"*, and then a tender hand: both halves at once. Shivi refuses *"you killed someone"* and *"you didn't hurt us"* in one breath, then names *"counterfeit forgiveness."* The theme is stated, and enacted in the last sentence.


## 8. Action, grappling

Where a body is grappling a body, sentences run long, and one verb carries a chain of consequences in a single breath. Short paragraphs are held for the reversals. Daniel calls this intuition, not a rule he holds (Q-GXBE).


**[the rakshasa]** `:1018`

> The caterwaul this time almost burst Toril's eardrums. The beast threw back its head and rolled sideways, hooking a tusk on the staff and levering Toril off his feet in the process, spattering an oily orange serum across Toril's clothes, and making matchwood of two stall partitions.
>
> Before the rakshasa could curl into a defensive ball, Toril was upright again, after it. His wrists still vibrating from the blow of the tusks, he swung the staff once more, this time aiming for a forearm.
>
> The blow went wide.
>
> Toril staggered when nothing checked his swing, slipped on loose straw, and fell on his shoulders, breath escaping at the impact. The back of his head hammered the floor, and he tasted blood from his tongue. He rolled sideways, even as his lungs fought to re-inflate.
>
> Meanwhile, the rakshasa had batted Hika over Toril's head and launched itself from a crouch. It landed with one massive foot across Toril's shin.
>
> Never keen of sight and now blind in one eye as well, it did not seem to realize where its leap had carried it or how it had Toril pinned. It batted at the blaze and roared, its claws trenching the dirt.
>
> Then it felt Toril try to free his leg.

Narration in this scene averages 17.3 words a sentence, against 12.2 for the book. *"The blow went wide."* and *"Then it felt Toril try to free his leg."* are the short ones, and they come at the turns.


**[the wolf]** `:1965`

> The impact of the wolf threw her to the ground, knocking the wind out of her. She felt her head thud and her shoulder bend as fangs seized her forearm and crushed down. Claws raked her chest and pinned her; she squirmed but could not get loose. With her free hand, she dug fingernails into the beast's snout, tearing as deeply as she could manage. No air would enter her lungs, but hot breath blew bellow-like as she stared into eyes pressing steadily closer.
>
> The wolf released her arm without warning and made a lightning snap for exposed throat. Exerting all her strength, Malena used her clawing hand to skew the movement. Her wrist bent as teeth clicked a finger's breadth from her skin. A drop of saliva blossomed above her collarbone.
>
> A dark streak slammed into the wolf's head and flitted away again. Malena saw the shape of the skull deform with the blow, robbing life from the beast's gaze. It slumped at her side without a sound, a trickle of red swelling from below its ear.

*"She felt her head thud and her shoulder bend as fangs seized her forearm and crushed down."* Several things happen to the body in one sentence, faster than they can be separated.


## 9. Action, perceived in fragments

Where the POV perceives a group fight in poor visibility, the prose breaks into fragments, one sense at a time. The Rift's fights run 9–10 words a sentence.


**[pishachas in the haze]** `:3660`

> For a moment, she thought the attackers had two heads. Then she saw Oji slash at a shadow with his shortsword, and realized that he'd dismounted some sort of… rider. Its body sagged into a grotesque heap at her feet. It had a broad, flat face with no nose, and an underbite emphasized by jutting canines. Outsized, all-black eyes glimmered beneath a horny crest. Its skin seemed to consist of jointed plates that glinted green around the edges, but brilliant orange in the middle. Spindly legs and a swollen body gave it a beetle-like appearance. A puddle of molasses-colored blood seeped toward her toe.
>
> Pishacha.
>
> She recoiled in disgust.
>
> The thing it had been riding vanished. Flickers of color faded.
>
> Silence brooded.
>
> She heard ragged breathing and realized it was her own.

A single word as a paragraph (*"Pishacha."*), a two-word one (*"Silence brooded."*), and her own breathing noticed late.


**[the charge]** `:3677`

> One shape raised its spear as a signal of some kind.
>
> A whistle sounded, followed by a chorus of hoarse cries.
>
> Inky shapes surged.
>
> The horse screamed and reared.

*"Inky shapes surged. / The horse screamed and reared."* Each sentence is one event, heard or half-seen.


## 10. Speakers and magic

Gitám does not contract (7.5 per thousand words against 47 for the book's dialogue; deliberate, and his idiolect rather than a rule for all Speakers, Q-ZG39). He repeats one word rather than reach for a synonym, and he answers with a question, a story or silence.


**[Gitám on names]** `:1443`

> "A wise name is a name worth having. It is a name for which you can, and do, sacrifice deeply. It is one that can be forged into truth through your effort, with raw materials of your own supply. I provide sparks, but the wood and the hammer and much of the working of the bellows must come from you, else the name is not your own. This is not an ordeal about *my* names."
>
> "Are we talking about my self-name, then? The one I took before?"
>
> "With people, all true names are self-names. Whether the one you took before was a wise choice is for you to decide."
>
> Toril bit his lip. "How do I keep the name?"
>
> "If you choose well, I will teach you what your name truly means, and you will mourn. Names of great worth are forged at a price; the ordeal is to continue to choose the name when you understand its cost."

*Name* in nearly every sentence. Short aphorisms: *"With people, all true names are self-names."* Toril's questions are short and plain against them.


**[the parable]** `:1422`

> "No? Tell me why First Woman cried yesterday."
>
> "That was a mistake," First Man said, after a long pause. "She asked if I liked her singing. I laughed because I thought the answer was obvious."
>
> "She sought to name herself 'Beautiful Singer.' You gave her a different name instead. Her heart was wounded."
>
> "All I did was laugh."
>
> "Search your heart. You're naming all the time—even in the way you answer me. Just now, you reached into possibility and summoned forth a word, and filled it with blameless ignorance. You named your action 'mistake'. Do you like the way that name shapes your soul?"
>
> First Man was silent for a long time. At last he shook his head. "It is only a partly true name," he said in a small voice.
>
> "Choose the truest. That is one of the tests on the path to joy."

The parable inside the ordeal is the key the scene later turns on. Gitám teaches by asking what First Man's word *"mistake"* does to his soul.


**[spoken magic]** `:1016`

> Toril used the distraction to exchange bow for staff. "*Bulen zhová!*" he shouted, spitting on the brass endcap and touching the metal to the nearest pile of straw. Flames rose, and the rakshasa, who was again preparing to lurch forward, raised a hand and blinked at the sudden light.

Lip magic is a word and spit on brass, told in one sentence and used once in the fight. The incantation is italic and not translated.


## 11. Grief

Grief is carried by the body and by an act, and is seldom named. Physical work gives the mind somewhere to go.


**[the children, and Paka]** `:4242`

> They found four slight figures, motionless and waxy, laid out like spokes around the center of a pit filled with remnants of fire. The ash radiated heat; the children, and the puddles of blood beneath their necks, were cold. The only color was a hint of blue petals in one girl's hair; somehow, the adornment made her gaunt cheeks and staring eyes even more heartbreaking.
>
> Horror bound their tongues. Toril felt tears fill the corner of his mouth. He swallowed, gagged, turned his head, blinked.
>
> He recognized all of them. One was the daughter of a saddlemaker that he'd visited last summer. He'd held her on his lap, once, while her father repaired a harness. And there was a little boy that he'd often seen toddling near the mill at the edge of town, and the son of one of his father's guards, and the granddaughter of the cook who'd worked in their kitchens for years…
>
> Through a saline blur he saw Malena walk the circle, scanning faces. When she was done, she stumbled a few steps, buried her face in her hands, and fell to her knees, shoulders heaving.
>
> Time passed—a hundred heartbeats, or maybe a thousand.
>
> A pebble cascaded down the path that had brought them to the clearing, and he looked up to see Shivi reeling drunkenly, a hand over her mouth.
>
> They'd left her caring for Paka while they rushed ahead to the children; she wouldn't have left his side unless…
>
> Oji reached her before Toril did. He eased her into a sitting position on a nearby log.
>
> "Paka?" he said.
>
> Shivi shook her head. Then she shook her head again, bowed it, and began to wail like a child.

He recognizes each child and gives one detail of each. Malena falls to her knees. *"Time passed—a hundred heartbeats, or maybe a thousand."* Shivi's news is one word from Oji and a head shaken twice.


**[the pyre]** `:4253`

> They built a pyre on a rise overlooking the river. The pit they'd found would have been an easier place to burn the dead, but repurposing a place that had served such foul ends was out of the question. Besides, the physical labor of carrying Paka and the children, fetching stones, and gathering firewood gave their minds somewhere to go.
>
> Fire from the setting sun glinted off the water by the time they were done.
>
> Paka lay in the center, propped by the wood beneath his shoulders. At Malena's suggestion, they arranged the children across his lap and beneath his encircling arms. "Like a grandpa," she whispered hoarsely.
>
> Shivi, whose wails had faded into stony silence as they worked, nodded in mute approval.

*"The physical labor … gave their minds somewhere to go."* Malena's idea is three words: *"Like a grandpa."*


## 12. Comedy

Comedy carries exposition and relief, and in these passages it comes from character rather than from a quip inserted for effect. Daniel: *"I worked hard on those."*


**[Tupa's firecrackers]** `:213`

> "Will I get to come back for a visit when you have a child?" Tupa asked.
>
> Malena snorted. Heaven's Fist! How many conversational firecrackers would her sister lob? Had Malena been this clueless about proper conversation when she was eleven?
>
> "You're assuming there'll *be* a baby," she said, pulling out the pin that bound her hair into a clasp at her neck. "That sort of thing isn't something you schedule. Anyway, you'll be in fosterage in a few months. Decisions about travel will be up to your near parents."
>
> "Don't start with the 'it happens when it happens' bit," said Malena's father, grunting as he pulled at his boots from the far side of the chamber. "The timing's not that mysterious, and it's under your control."
>
> Malena's face reddened again.
>
> "The timing *is* mysterious," said Malena's mother. "Look how widely spaced your own daughters are. Five my witness, you and I tried hard enough for more."
>
> "Can we please change the subject?" Malena said. "Something besides the details of childbearing?"

Tupa's question exposes the family's pressure about children. Malena's exasperation is in the narration (*"How many conversational firecrackers would her sister lob?"*), and the father uses the opening to press harder.


**[blackberry tarts]** `:575`

> "They make me take lots of baths. And I hate brushing out my hair. But I guess it's nice."
>
> "And do they have you sing in the kitchen?"
>
> "Cook says to sing every time she makes blackberry tarts, and Semya says he can tell whether my song is good by how sweet his dessert is. But I think he's teasing me, 'cause cook always uses the same cup of honey."

Right after Kinora describes her stepfather. Her theory of Toril's teasing is a child's logic, and it's right.


## 13. Conventions, as observed


- **Chapter subtitles.** Every chapter opens with an italic line *topic ~ POV* under its number (`:36`, `:197`, `:251` …). Only chapter 2 adds a time note (*"a decade later"*).
- **One POV per scene**, close third. Chapters can change POV at a scene break (ch 4, ch 56). Two short passages have an outside narrator (`:1467`, `:1517`), and three italic scenes are Toril's ordeal with Gitám, told out of order (`:1555`, `:1716`, `:2529`).
- **Thought in italics**, short and direct: *"Gitám, let this work!"* (`:1378`), *"Luim was Oji's father? How could he have failed to mention that detail?"* (`:2732`).
- **Untranslated speech** of magic, in italics: the invocation (`:1390`–`1393`), *"Bulen zhová!"* (`:1016`), *"Maurozh"* (`:611`).
- **Ellipses in speech** for trailing off, and in narration for a thought left open (`:1261`, `:1269`, `:4248`).
- **Pet names** carry intimacy: *Lena*, *Pak'ita*, *Shiv*.

