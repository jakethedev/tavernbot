# DungeonBot - [Ideas and Suggestions Welcome!](https://github.com/JakeRunsDnD/dungeonbot/issues)
### (Soon to be renamed... Tavernbot? RPGBot? TBD)

This is a generator bot for Game Masters of D&D. Initially, this will just be a
Discord bot, but it will soon break apart into multiple modules - notably,
the tavernlib directory will live as its own project on NPM as a catchall
multi-use RPG lib, with multiple build commands for use as a bot or as
a web page plugin.

But the general idea is that is would be hella dope to have a really good D&D bot for discord, yeah?

I think so. So here's my shot at it.

Note to Self: Figure out what's up with these. Contact ThreeToes and see
if they'd consider updating their npm package name

https://github.com/ThreeToes/dice-lib
https://github.com/mrprim/random-rpg-stuff
https://github.com/guumaster/rpgen
https://github.com/hogart/rpg-tools
https://github.com/ara-ta3/node-quest
https://github.com/photonstorm/phaser
https://www.npmjs.com/package/dungeonworld-data
https://www.npmjs.com/package/rpg-names
https://www.npmjs.com/package/rpgparser
https://www.npmjs.com/package/fabrico
https://www.npmjs.com/package/the-npm-rpg
https://www.npmjs.com/package/rpg-helper

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

Additional Notes:Discord Bot Thoughts and Ideas
------------------------------
Throttle max rolls to 100. If more, mutiply to match and throw another 100 on it.
Cap dice types at 5 instances of 'd'? "Error: Too complex"?
I want to roll this '1d20 + 5, 2d6 + 2d8 + 3'

LOOK UP https://discord.js.org/#/docs/main/stable/topics/voice

Good Practices
- package.json for sanity
- Build out functionality as an npm project?

Funnel Character generator
- PHB spread w/stat priority per class
- 4d6k3
- Colville method
- 6 + 2d6

Keep last 128 macros?
Find a good base of Character Sheet JSON

Might be good to steal from https://github.com/opendnd
Great dice roller: https://github.com/NickMele/node-dice
Other sources:
  https://github.com/jhamlet/dice-js
  https://github.com/thebinarypenguin/droll

Code from Slack-dnd that might help parser:
if(parsed.pathname === '/roll'){
  var diceData = parsed.query.text.split('d');
  var echoChannel = parsed.query.channel_id;
  var numDice = parseInt(diceData[0] || 1, 10);
  var diceType = parseInt(diceData[1], 10);
  var results = [];
  var roll = 0;

  console.log('request', req.url);

  if(!isNaN(numDice) && !isNaN(diceType)){
    console.log('valid request, rolling dice');
    numDice = numDice > 10 ? 10 : numDice;
    diceType = diceType > 20 ? 20 : diceType;
    for(var i = 0; i < numDice; i++){
      roll = rollDie(diceType);
      results.push(roll);
    }
  }
  etc;
}

