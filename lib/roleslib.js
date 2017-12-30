require('discord.js')

addRole = function(client, user, role){
  //TODO Ensure requestor is admin or the user, then add role to user
}

listRoles = function(client, user, role){
  //TODO Return a list, could be empty so return something pleasant
}

removeRole = function(client, user, role){
  //TODO Ensure requestor is admin or the user. Then remove role if exists.
}

listUsersInRole = function(client, role){
  //TODO Publicly visible, so anyone should be able to do this.
  //Get all with role
  // let roleID = "264410914592129025";
  // let membersWithRole = message.guild.roles.get(roleID).members;
  // console.log(`Got ${membersWithRole.size} members with that role.`);
}

ignorethis = function(){
  // get role by name
  let myRole = message.guild.roles.find("name", "Moderators");

  // assuming role.id is an actual ID of a valid role:
  if(message.member.roles.has(role.id)) {
    console.log(`Yay, the author of the message has the role!`);
  } else {
    console.log(`Nope, noppers, nadda.`);
  }

  //Other basics
  let role = message.guild.roles.find("name", "Team Mystic");

  // Let's pretend you mentioned the user you want to add a role to (!addrole @user Role Name):
  let member = message.mentions.members.first();

  // or the person who made the command: let member = message.member;

  // Add the role!
  member.addRole(role).catch(console.error);

  // Remove a role!
  member.removeRole(role).catch(console.error);
}

module.exports = [ addRole, listRoles, removeRole, listUsersInRole ]
console.log('roleslib loaded!')
