// Core bot setup
require('./randomUtil')
const fs = require('fs')
const { token, botkey, activeChannels, gameStatus } = JSON.parse(fs.readFileSync('config.json', 'utf-8'))
const discord = require("discord.js")
const client = new discord.Client()

// Dynamically load all operations we care about into a single commander object
loadAllOperations = function(libNames){
  let allOps = {}, meta = {}
  // Get each lib by name
  for (lib of libNames) {
    meta[lib] = []
    let libOps = require(lib);
    for (op in libOps) {
      // Stash all op names at meta[libname] for help reference
      allOps[op] = libOps[op]
      meta[lib].push(op)
    }
    // These will clobber eachother, this keeps them split up
    meta[lib].helptext = libOps['helptext']()
  }
  return [ allOps, meta ]
}
// Always keep gravemind at the end
const MODULES = [ './discordlib', './dungeonary', './gravemind' ]
const [ commander, metadata ] = loadAllOperations(MODULES)

// In case something happens, we'll want to see logs
client.on("error", (e) => console.error(e))

// Startup callback
client.on('ready', () => {
  if (process.env.NODE_ENV) {
    console.log(`${process.env.NODE_ENV} mode activated!`)
  } else {
    console.log(`NODE_ENV not set, running in dev mode`)
  }
  console.log(`Tavernbot v${process.env.npm_package_version} has logged in as ${client.user.tag}!`)
  client.user.setPresence({
    "status": "online",
    "game": { "name": gameStatus }
  })
})

// Command central
client.on('message', msg => {
  // Contain the bot, and ensure we actually want to act on the command
  let channelName = msg.channel.name ? msg.channel.name.toLowerCase() : "NOT_A_CHANNEL_NAME"
  if (activeChannels.includes(channelName) || msg.channel.recipient) {
    if (!msg.content.trim().startsWith(botkey) || msg.author.bot) return
    // Normalize input
    let parts = msg.content.trim().toLowerCase().substring(1).split(/\s+/)
    let cmd = parts[0]
    let input = parts[1] ? parts.slice(1).join(' ') : '' //Some cmds have no input, this lets us use if(input)
    let execTime = new Date(Date.now()).toLocaleString();
    // If we have the requested op, send it - otherwise, log it quietly
    if (cmd in commander) {
      console.log(execTime + ': running ' + cmd + '(' + input + ') for ' + msg.author.username)
      // Works for a string or a promise return. Sick. https://stackoverflow.com/a/27760489
      Promise.resolve( commander[cmd](input, msg, client) )
        .then(function(result) {
          msg.reply(result)
        })
        .catch(function(err) {
          msg.reply(`your command met with a terrible fate and I nearly died. Have an admin check the logs plz`)
          console.log(`${execTime}: ERR: ${err}`)
        })
    } else if (cmd == 'help') {
      let fullHelp = `these are my powers:`
      // Each library is a string
      for (library in metadata){ // Already overloaded command, oops
        fullHelp += `\n**${metadata[library].helptext}**: \n` // Set in each lib's index.js, saved at :17
        // meta[lib] is a list of ops in that lib
        for (var opName of metadata[library]) {
          if ((opName) != 'helptext')
            fullHelp += `${opName}\n`
        }
      }
      fullHelp += `\nFor any command, run '${botkey}command help' for detailed use info. `
      fullHelp += `If you notice something weird or broken, run **${botkey}feedback** for support info`
      msg.channel.send(fullHelp)
    } else {
      console.log(`${execTime}: NOTICE: can't find ${cmd}(${input}) for ${msg.author.username}`)
    }
  }
});

// Turning the key and revving the bot engine
client.login(token)
