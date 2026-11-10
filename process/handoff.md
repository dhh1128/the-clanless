---
approval: unapproved
---

# Handoff pointer

The handoff a new session loads is `~/code/me/the-clanless/.ignored/continuation.md`: what is done and approved, what comes next, and the open questions. The handoff itself stays in `.ignored/` because it quotes working material and changes at every break. This tracked file is what makes it findable, as novel-method runbook D9 requires (edition 1, Q-RXPW).

**At every handoff**, which is every natural break (a layer approved, a day's maps approved, a day drafted) rather than a guess at how much context is left:

1. Rewrite `~/code/me/the-clanless/.ignored/continuation.md` for a session that shares none of this one's context. If the handoff moves to another path, change it here in the same commit as the work it hands off.
2. Run the flywheel capture, which writes Daniel's turns from this session (including those typed while it was busy) and his hand-edit commits to `.ignored/captures/`:

   ```
   python3 ~/code/me/novel-method/tools/capture.py /home/daniel/code/me/the-clanless
   ```

   The transcript defaults to the newest one Claude Code keeps for this directory, which is the running session; `--session <id-prefix>` picks another.
3. At the retro, classify each correction, delight and hand edit in the capture as canon, method, craft, tool or friction. Canon stays here. File each non-canon item as a tick in `~/code/me/novel-method` with his exact words, the session id and the timestamp (`~/code/me/novel-method/adopt.md`, "The flywheel", steps 2 and 3).
