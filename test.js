//All the custom stuff, this might be one library eventually
const adventuregen = require('./lib/adventuregen')
const beastiary = require('./lib/beastiary')
const diceroller = require('./lib/diceroller')
const discordroles = require('./lib/discordroles')
const spellbook = require('./lib/spellbook')

const Discord = require("discord.js");
const client = new Discord.Client();
const config = require("./config.json"); // Should contain token and botkey, a character that prefixes commands

// This is a test msg, do not use in the actual bot
msg = { "content": "!hook low", "author": { 'username': "TEST INPUT" }, "reply": console.log, "channel": { "name": "golemworks" } };

// Let's hook it up for a default channel and DMs
if ( msg.channel.name == config.defaultChannel || msg.channel.recipient ){
  //Make sure we care, and that we're not making ourselves care
  if ( !msg.content.trim().startsWith(config.botkey) || msg.author.bot) return;
  //Remove botkey and break it up into clean not-mixed-cased parts.
  let parts = msg.content.trim().toLowerCase().substring(1).split(/\s+/);
  let cmd = parts[0];
  let input = parts[1] ? parts.slice(1).join(' ') : null; //Some cmds have no input, this lets us use if(input)
  //From here, we're just using dicelib/roleslib/etc functions
  console.log( msg.author.username +' requested ['+cmd+'] for input ['+input+']');
  if ( cmd == 'roll' ) {
    if ( input ){ //TODO This is buggy, fixme
      msg.reply( diceroller.customRoll(input) );
    } else {
      msg.reply('a d20 skitters across the table, you rolled a ' + diceroller.d(20) );
    }
  } else if ( cmd == 'coin' ) {
    msg.reply( "the botcoin landed on " + diceroller.coin() );
  } else if ( cmd == 'd' && input && parseInt(input) ) {
    let diceSize = parseInt(input);
    if (isNaN(diceSize) || diceSize < 2 ){
      return "You get a nat 1, because that's not a valid dice size."
    }
    msg.reply( "Your custom die rolls a " + diceroller.d(diceSize) );
  } else if ( cmd == 'rank' && input ) {
    msg.reply( discordroles.addRole(client, msg.author, input) );
  } else if ( cmd == 'ranks' ) {
    msg.reply( discordroles.listRoles(client, msg.author, input) );
  } else if ( cmd == 'remove' && input ) {
    msg.reply( discordroles.removeRole(client, msg.author, input) );
  } else if ( cmd == 'members' && input ) {
    msg.reply( discordroles.listUsersInRole(client, input) );
  } else if ( cmd == 'hook' ) {
    msg.reply( adventuregen.generate(input) );
  }
}
