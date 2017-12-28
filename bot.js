require('./lib/dicelib')
const Discord = require("discord.js");
/**
 * X require discord
 * load discord conf
 * init client
 */

const client = new Discord.Client();
const hotkey = '!'; //This determines what aggravates the bot

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  if (cmd.startsWith(hotkey)){
    let pieces = msg.content.split(' ');
    let cmd = pieces[0];
    let input = pieces[1] || null;  //Some cmds are just the cmd
    console.log('Recieved cmd '+cmd+' for input ['+input+']');
    if (cmd.startsWith( hotkey + 'roll' )) {
      msg.reply('Rolling '+ input + '...');
      msg.reply(roll(input));
    } else if (cmd.startsWith( hotkey + 'rank' )) {
      msg.reply('Rank '+ input + '...');
      msg.reply(rank(input));
    } else if (cmd.startsWith( hotkey + 'ping' )) {
      msg.reply('Pong!');
    }
  }
});

console.log('Rolling initiative: ' + d20() );
client.login('token');
console.log('I\'ll be back');
