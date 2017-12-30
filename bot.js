//All the custom stuff, loaded as global functions. i.e. d20() is now global. Like it should be.
require('./lib/dicelib')
require('./lib/roleslib')
require('./lib/hooklib')

/**
 *     TODO
 * X require discord
 * load discord conf
 * init client
 */

const Discord = require("discord.js");
const client = new Discord.Client();
const config = require("./config.json"); // Should contain token and botkey, a character that prefixes commands

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  // msg = { "content": "!adventure", "author": { "bot": false }, "reply": console.log }; //Test item, do not use

  //Verify that we care, and that we're not making ourselves care
  if ( msg.content.startsWith(config.botkey) && (!msg.author.bot) ){
    //Remove botkey and break it up
    let pieces = msg.content.substring(1).split(' ');
    let cmd = pieces[0];
    let input = pieces[1] || null;  //Some cmds are just the cmd
    console.log('Recieved request to ['+cmd+'] for input ['+input+']');

    //From here, we're just using dicelib/roleslib/etc functions
    if ( cmd == 'roll' ) {
      if ( input ){
        msg.reply( customRoll(input) );
      } else {
        msg.reply('A d20 skitters across the table, you rolled a ' + d(20) );
      }
    } else if ( cmd == 'coin' ) {
      msg.reply( "The botcoin landed on " + coin() );
    } else if ( cmd == 'd' && input && parseInt(input) ) {
      let diceSize = parseInt(input);
      msg.reply( "Your custom die rolls a " + d(diceSize) );
    } else if ( cmd == 'rank' && input ) {
      msg.reply( addRole(client, msg.author, input) );
    } else if ( cmd == 'ranks' ) {
      msg.reply( listRoles(client, msg.author, input) );
    } else if ( cmd == 'remove' && input ) {
      msg.reply( removeRole(client, msg.author, input) );
    } else if ( cmd == 'members' && input ) {
      msg.reply( listUsersInRole(client, input) );
    } else if ( cmd == 'adventure' ) {
      msg.reply(generateAdventure(false));
    }
  }
});

console.log('Rolling initiative: ' + d(20) );
client.login(config.token);
console.log('I\'ll be back');
