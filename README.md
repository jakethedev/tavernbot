# DungeonBot

A generator bot for Game Masters of D&D. Multiple run modes include 
a flask API (WIP), a discord bot (WIP), and a CLI for 'that' GM (aka me).

---

## Notes from before:

Need to implement this:
https://github.com/Rapptz/discord.py#discordpy

This bot is twinkle in the eye of a bud of a work in progress.

But the idea is that is would be hella dope to have a D&D bot for discord, yeah?

I think so. So here's an attempt at building that.
 
# Todo List ('scuse the shorthand)

Main Func
- Run script for bot
- Run script for server
  - Combine?
- local main, enum param for what to make
  - enum: adventure, quest, hook, bbeg, bg, npc, party

Major Tasks
- Hook randomizing
  - Fall into dungeon
  - Witness crime
  - Npc informant found out defector
- Villain and subvillains
  - Create subvillain generation
  - Have 2-3 allies for main villain
- Creating NPC/PC 
  - class+spec (title only, no powers)
  - race+sub (include stat mods)
  - background from table
  - profs
  - stats
  - 2 knives by default
    - Knife table
- Create party
  - param: size, stats=random,spread
  - gen (size) pc's, roll/spread stats
  - size-1 bonds for each pc
    - set up a bond table to roll on


