//All the custom stuff, this might be one library eventually
//All the custom stuff, separated by converns
const tavernlib = require('./tavernlib')
const discordlib = require('./discordlib')
const { token, botkey, defaultChannel, gameStatus } = require("./config.json")

let msgs = [
  { "content": "!coin", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!d 20", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!roll 1d20 + 5", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook low", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook hi", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook cy", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook st", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook spa", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!hook mod", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!spell", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } },
  { "content": "!monster", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } }
]

for (msg of msgs){
  // Let's hook it up for a default channel and DMs
  if ( msg.channel.name == defaultChannel || msg.channel.recipient ){
    //Make sure we care, and that we're not making ourselves care
    if ( !msg.content.trim().startsWith(botkey) || msg.author.bot) return
    //Remove botkey and break it up into clean not-mixed-cased parts.
    let parts = msg.content.trim().toLowerCase().substring(1).split(/\s+/)
    let cmd = parts[0]
    let input = parts[1] ? parts.slice(1).join(' ') : '' //Some cmds have no input, this lets us use if(input)
    //From here, we check each lib until we find a match for execution, or we let the user know it's a no-go
    if ( cmd in tavernlib ) {
      console.log( 'Found '+cmd+' in tavernlib, running with input='+input+' for requestor='+msg.author.username )
      msg.reply( tavernlib[cmd]( input ) )
    } else if ( cmd in discordlib ) {
      console.log( 'Found '+cmd+' in tavernlib, running with input='+input+' for requestor='+msg.author.username )
      msg.reply( discordlib[cmd]( input, msg, client ) )
    } else {
      msg.reply("I'm sorry Dave, I'm afraid I can't do that")
    }
  }
}
