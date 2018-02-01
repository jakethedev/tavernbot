// All commands should have the signature:
//    f(input:String, message:discord.js#message, client:discord.js#client)

//Given a rolename as input, add it to the requestor if it doesn't result in new privileges
exports.addrole = function(input, message, client) {
  //TODO Ensure requestor is admin or the user, then add role to user
  // if ( role.position < bot.role.position ) { ok }
  return 'a role has no name';
}

//List the requestor's roles
exports.roles = function(input, message, client) {
  //TODO Return a list, could be empty so return something pleasant
  return 'your role is to butter toast';
}

//Self-remove a role
exports.unrole = function(input, message, client) {
  //TODO Ensure requestor is admin or the user. Then remove role if exists.
  return 'by your decree, we have banished you from the cool kids club';
}

//Number of people in a given role
exports.rolesize = function(input = '', message, client) {
  if (!input) return 'there are many members with many roles, give me a role and I\'ll give you an answer';
  if (message.guild.available) { //Docs recommend this check

    //Make input easier to search with, comb the roles, and return the size of the role if it's found
    input = input.trim().toLowerCase();
    let roleResult = message.guild.roles.find(role => role.name.toLowerCase() === input);
    if (roleResult) {
      let roleCount = roleResult.members.size;
      return `there are ${roleCount} members in ${roleResult.name}`;
    } else {
      return 'role not found - enter the role\'s full name to get you a member count';
    }
  } else {
    return 'there was a temporal anomaly, I believe I need my oil changed';
  }
}

samplecode = function() {
  // get role by name
  let myRole = message.guild.roles.find("name", "Moderators");

  // assuming role.id is an actual ID of a valid role:
  if (message.member.roles.has(role.id)) {
    console.log(`Yay, the author of the message has the role!`);
  } else {
    console.log(`Nope, noppers, nadda.`);
  }

  //Other basics


  // Let's pretend you mentioned the user you want to add a role to (!addrole @user Role Name):
  let member = message.mentions.members.first();

  // or the person who made the command: let member = message.member;

  // Add the role!
  member.addRole(role).catch(console.error);

  // Remove a role!
  member.removeRole(role).catch(console.error);

  //Docs https://anidiotsguide.gitbooks.io/discord-js-bot-guide/information/understanding-roles.html
}