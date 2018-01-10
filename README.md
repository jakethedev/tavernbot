# DungeonBot

A generator bot for Game Masters of D&D. Initially, this will just be a
Discord bot, but it will soon break apart into multiple modules - notably,
the tavernlib directory will live as its own project on NPM as a catchall
multi-use RPG lib, with multiple build commands for use as a bot or as
a web page plugin.

But the general idea is that is would be hella dope to have a really good D&D bot for discord, yeah?

I think so. So here's my shot at it.

## Todo List in JakeShorthand(TM)

Key: - todo, > in progress, X done, ? maybe

```
Main Func
X Run script for bot
- Run script for web build
  ? Combine?
- local main, enum param for what to make
  > enum: adventure, quest, hook, bbeg, bg, npc, party, addrole, listroles, removerole, listallinrole
X Run script for test
  - Actually make this dynamic or something instead of hardcoded mocks

Major Tasks
- Port all tasks from here and Trello into Github issues
> Dice roller
  X Basic dice function for arbitrary dice sides
  - Dice query parser for + and - and varied dice
    - Addition/subtraction
    - Comma sep chunks reported as separate rolls
    ? macros
> Role management
  - Add role
  - Remove role
  - List roles for user
  - List users with role
> Hook randomizing
  - Fall into dungeon
  - Witness crime
  - Npc informant found out defector
> Villain and subvillains
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
```


