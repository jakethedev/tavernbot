/*
Note to any readers:

I don't, for one second, think this is a substitute for unit testing.
I just wanted a way to continue bolting down code and ensuring it all
works smoothly during intense construction and refactoring, and this
is surprisingly maintainable for the moment.

When it gets hairy, I'll bring on chai + mocha. Which will probably be soon.
*/


const dungeonary = require('./dungeonary')
const discordlib = require('./discordlib')
require('./randomUtil')
const {
  token,
  botkey,
  botRole,
  activeChannels,
  gameStatus
} = require("./config.json")

let msgs = [
  { "content": "!coin", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!coin 20", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook low", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook hi", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook cy", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook st", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook spa", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook mod", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!spell", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!monster", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats 4d6k3", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats 2d6+6", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats colville", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats funnel", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!rollstats 3d6", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 1d20 + 5", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 2d20 + 5d4", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 50d20 + d6 + 9", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll d6+d6+d6", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll -7+1d6", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 1d6 for schwiiing", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 1d20+5 to hit, 2d6+3 dmg, 1d6 poison, 1d20-1 con save", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 49d32 + 3d6 + 9 + 7 - 2 for meteor shower", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll FIREBALL", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 1d20 + 5 + 2d6, 9d8 + 1, d6 + d6 + d6 + d6", "author": { 'username': "testuser" }, "reply": console.log, "channel": { "name": "golemworks" } }
]

for (msg of msgs) {
  // Let's hook it up for a default channel and DMs
  if (activeChannels.includes(msg.channel.name.toLowerCase()) || msg.channel.recipient) {
    //Make sure we care, and that we're not making ourselves care
    if (!msg.content.trim().startsWith(botkey) || msg.author.bot) return
    //Remove botkey and break it up into clean not-mixed-cased parts.
    let parts = msg.content.trim().toLowerCase().substring(1).split(/\s+/)
    let cmd = parts[0]
    let input = parts[1] ? parts.slice(1).join(' ') : '' //Some cmds have no input, this lets us use if(input)
    let execTime = new Date(Date.now()).toLocaleString() + ': ';
    //From here, we check each lib until we find a match for execution, or we let the user know it's a no-go
    if (cmd in dungeonary) {
      console.log(execTime + 'running dungeonary.' + cmd + '(' + input + ') for ' + msg.author.username)
      msg.reply(dungeonary[cmd](input))
    } else if (cmd in discordlib) {
      console.log(execTime + 'running discordlib.' + cmd + '(' + input + ') for ' + msg.author.username)
      msg.reply(discordlib[cmd](input, msg, client))
    } else {
      msg.reply("I'm sorry " + msg.author.username + ", I'm afraid I can't do that")
    }
  }
}
