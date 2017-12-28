require('./lib/dicelib')
const Discord = require("discord.js");
/**
 * X require discord
 * load discord conf
 * init client
 */

const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  if (msg.content === 'ping') {
    msg.reply('Pong!');
  }
});

console.log('Attempting login...');
client.login('token');
console.log('I\'ll be back');
