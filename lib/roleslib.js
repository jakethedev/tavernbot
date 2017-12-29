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
}

module.exports = [ addRole, listRoles, removeRole, listUsersInRole ]
console.log('roleslib loaded!')
