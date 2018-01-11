# TavernBot - [Ideas and Suggestions Welcome!](https://github.com/JakeRunsDnD/tavernbot/issues)

This is a generator bot for Game Masters of D&D. Initially, this will just be a
Discord bot, but it will soon break apart into multiple modules - notably,
the dungeonary directory will live as its own project on NPM as a catchall
multi-use RPG lib, with multiple build commands for use as a bot or as
a web page plugin.

But the general idea is that is would be hella dope to have a really good D&D bot for discord, yeah?

I think so. So here's my shot at it.

For dungeon world content:
https://www.npmjs.com/package/dungeonworld-data


## Additional Notes:Discord Bot Thoughts and Ideas
---
Throttle max rolls to 100. If more, mutiply to match and throw another 100 on it.
Cap dice types at 5 instances of 'd'? "Error: Too complex"?
I want to roll this '1d20 + 5, 2d6 + 2d8 + 3'

Voice API https://discord.js.org/#/docs/main/stable/topics/voice

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

