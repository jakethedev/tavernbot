# TavernBot - The Ultimate RPG Discord Bot for D&D, Pathfinder, and beyond!
### [Ideas and Suggestions Welcome!](https://github.com/jakethedev/tavernbot/issues)

The idea: Wouldn't it be great to have a really good D&D bot for discord? I think so. And this is the start of that solution.

TavernBot is a generator bot for Game Masters of D&D. This project is a Discord bot wrapper for the [Dungeonary](https://www.npmjs.com/package/dungeonary), and several other useful discord functions such as roles and eventually music/ambience in a voice channel.

This is currently an 0.x release - I will document features and such here as they're finished up and as we close in on 1.0, but for now, I'm pouring molten free time into this project to try and forge something awesome. Check the code for now if you want to know more.

## Development

Fork this project, then follow these steps to get up and running! Make sure you have node 8+, with an appropriate npm, and a Discord bot token. Go to [this link](https://discordapp.com/developers/applications/me) to set up a bot account, add the token to config.json in the project root, then invite the bot to a server for testing. And don't forget npm install.

'npm run devbot' will set you up with a hot-reloading bot instance, and 'npm test' should run quietly with no issues if everything's set up correctly. 'npm run verbosetest' will show you the npm test output, which should look like Discord-formatted responses.

### Expectations and how it loads

The bot is set up to load a list of local libs, grab every exported function, and drop the functions + a bit of metadata into a global commander object. That said, this means it calls all functions exactly the same way - and if you need more parameters for some reason, perhaps we should chat. For your new commands to drop in and immediately work, they must have the following signature: `f(input:String, message:discord.js#message, client:discord.js#client)` - input will be everything after your commands name in the message to the bot (like '!commandname input is all this stuff'), the message will be the full message object [per the Discord.js api](https://discord.js.org/#/docs/main/stable/class/Message), and the client is [from Discord.js too](https://discord.js.org/#/docs/main/stable/class/Client).

### Writing new commands

If you just want to just *add a relevant command* to a library, you only need *step 4*. But if you have commands to add that don't seem to fit with the theme of functions in a particular file, follow all of these steps to add a new library folder to the bot:

1. Make a new directory
2. Add your new directory to the MODULES array in bot.js
3. Copy index.js from discordlib or gravemind into your new lib as a handy piece of boilerplate
4. Write exported functions in your library (Note: The bot ignores the default export!)
5. Update the index.js in your library so it loads a file you create in your new lib
6. Run it! You've now added functionality to the bot!

## Development triage:

### ImportError: no module compiler.ast:

If you see the above issue during 'npm install', just run 'sudo apt install python-dev'. I'm as upset as you are that we need python for npm, but, c'est la vie.

### Vague "app crashed" error

An issue with the bot, while testing new commands, is that you have to be very aware of what might throw an error. I don't have error handling set up correctly yet, even though I'm following the recommended client.on('error', callback) approach, so I apologize if this bites you. If you know a way to make node/discord.js run in a hella verbose way, I'd gladly add that to the `npm run devbot` script

---

Below is a sort of notepad, and generally contains nothing useful. If you have ideas or features that you think this bot should support, [let me know on Github](https://github.com/jakethedev/tavernbot/issues) and we'll get it prioritized :D

Source for dungeon world content: https://www.npmjs.com/package/dungeonworld-data

Voice API https://discord.js.org/#/docs/main/stable/topics/voice

Character stats implementation needs PHB spread w/stat priority per class

Keep last 128 roll macros? 256?

Find a good base of Character Sheet JSON

Possibly useful for inspiration https://github.com/opendnd

