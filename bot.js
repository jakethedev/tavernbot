//All the custom stuff, loaded as global functions for pragmatism
require('./lib/dicelib')
require('./lib/roleslib')
require('./lib/hooklib')

const Discord = require("discord.js");
const client = new Discord.Client();
const config = require("./config.json"); // Should contain token and botkey, a character that prefixes commands

// In case something happens, we'll want to see logs
client.on("error", (e) => console.error(e));

// Startup callback
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
  client.user.setPresence({
    "status":"online",
    "game": { "name" : config.gameStatus }
  });
});

// Command central
client.on('message', msg => {
  // msg = { "content": "!adventure", "author": { "bot": false }, "reply": console.log }; //Test item, do not use

  // Let's hook it up for a default channel and DMs
  if ( msg.channel.name == config.defaultChannel || msg.channel.recipient ){
    //Make sure we care, and that we're not making ourselves care
    if ( !msg.content.trim().startsWith(config.botkey) || msg.author.bot) return;

    //Remove botkey and break it up into clean pieces
    let parts = msg.content.trim().substring(1).split(/\s+/);
    let cmd = parts[0];
    let input = parts.slice(1);
    if (input === []) input = null; //Some cmds are just the cmd
    //From here, we're just using dicelib/roleslib/etc functions
    console.log( msg.author.username +' requested ['+cmd+'] for input ['+input+']');
    if ( cmd == 'roll' ) {
      if ( input ){
        msg.reply( customRoll(input) );
      } else {
        msg.reply('a d20 skitters across the table, you rolled a ' + d(20) );
      }
    } else if ( cmd == 'coin' ) {
      msg.reply( "the botcoin landed on " + coin() );
    } else if ( cmd == 'd' && input && parseInt(input) ) {
      let diceSize = parseInt(input);
      msg.reply( "your custom die rolls a " + d(diceSize) );
    } else if ( cmd == 'rank' && input ) {
      msg.reply( addRole(client, msg.author, input) );
    } else if ( cmd == 'ranks' ) {
      msg.reply( listRoles(client, msg.author, input) );
    } else if ( cmd == 'remove' && input ) {
      msg.reply( removeRole(client, msg.author, input) );
    } else if ( cmd == 'members' && input ) {
      msg.reply( listUsersInRole(client, input) );
    } else if ( cmd == 'rpghook' ) {
      msg.reply(generateAdventure(false));
    }
  }
});

// Turning the key and revving the bot engine
console.log('Rolling initiative...');
client.login(config.token);
