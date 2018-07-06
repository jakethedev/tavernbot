// TO PROGRAMMERS: commands should have the signature:
//    f(input:String, message:discord.js#message, client:discord.js#client)

getManagedRoles = function(client) {

}

exports.newrole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `help for newrole`
  if (!message.member) return `you don't even live here, stop messing with things (err: not a server member)`
  // if (message.member.permissions.includes 'icandothings'){
  //   discord.addNewRole(name: input)
  //   return `mission accomplished - your role called "${input}" is ready to rock`
  // }
  return `put that back, you're not allowed to touch it. (err: ain't got permission pal)`
}

//Given a rolename as input, add it to the requestor if it doesn't result in new privileges
exports.addrole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `help for addrole`
  //TODO Ensure requestor is admin or the user, then if the role is a managed role, add role to user
  // let validRoles = message.guild.roles.filter((role) => role.id < )
  // if (role.position < bot.role.position) {
  //   member.addRole().catch(console.error)
  //   console.log('Requesting ' + role + ' and it\'s lower ranked than the bot role, so we good')
  // }
  return `a role has no name`
}

//List the requestor's roles.
//TODO Use this, list a target's roles; let targetToSummon = message.mentions.users.first()
exports.roles = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `help for roles`
  const userRolesRaw = message.member.roles
  let roleResults = []
  // Stash the results, strip any @ symbols to avoid pinging @everyone every single time
  userRolesRaw.forEach(role => roleResults.push(role.name.replace('@', '')))
  if (roleResults[0]) {
    return `here are your roles: [${roleResults.join(', ')}]`
  } else {
    return `your purpose is to butter toast. (no roles found)`
  }
}

//Self-remove a role, after verifying that the author is a member (role-bearer)
exports.unrole = function(input, message, client) {
  if (!input || input.toLowerCase() == 'help') return `!unrole [rolename]: Removes rolename from your roles if you have it`
  if (!message.member) return `this is not the command you're looking for (you're not a member here, sorry mate)`
  let userRoles = message.member.roles
  if (userRoles.size == 0)
    return `it seems that you have no roles, and that's really funny`
  let roleResult = userRoles.find(role => role.name.toLowerCase() === input.toLowerCase())
  if (!roleResult)
    return `we cannot remove what does not exist (role "${input}" not found on your account)`

  //TODO VERIFY THIS ROLE IS LOWER THAN BOT ROLE OR IT DIES. async promise this shit?
  console.log(`Verify the role is below bot role or (chuckles) I'm in danger`)

  message.member.removeRole(roleResult)
  return `as you wish - you have cast thyself from the family of "${input}"!`
}

//Number of people in a given role
exports.rolesize = function(input = '', message, client) {
  if (!input) return `give me a role and I'll give you an answer`
  if (input.toLowerCase() == 'help') return `help for rolesize`
  if (message.guild.available) { //Docs recommend this check

    //Make input easier to search with, comb the roles, and return the size of the role if it's found
    input = input.trim().toLowerCase()
    let roleResult = message.guild.roles.find(role => role.name.toLowerCase() === input)
    if (roleResult) {
      let roleCount = roleResult.members.size
      return `there are ${roleCount} members in ${roleResult.name}`
    } else {
      return `role not found - gimme the role's full name, and I'll get you a member count`
    }
  } else {
    return `there was a temporal anomaly, I believe I need my oil changed`
  }
}

//List people in a given role
exports.rolemembers = function(input = '', message, client) {
  if (!input) return `give me a role and I'll give you an answer`
  if (input.toLowerCase() == 'help') return `help for rolemembers`
  if (message.guild.available) { //Docs recommend this check
    //TODO Copy rolesize function but list names
    return 'blame jake for this message'
  } else {
    return 'there was a temporal anomaly, I believe I need my oil changed'
  }
}

samplecode = function() {
  // get role by name
  let myRole = message.guild.roles.find("name", "Moderators")

  // assuming role.id is an actual ID of a valid role:
  if (message.member.roles.has(role.id)) {
    console.log(`Yay, the author of the message has the role!`)
  } else {
    console.log(`Nope, noppers, nadda.`)
  }

  //Other basics


  // Let's pretend you mentioned the user you want to add a role to (!addrole @user Role Name):
  let member = message.mentions.members.first()

  // or the person who made the command: let member = message.member;

  // Add the role!
  member.addRole(role).catch(console.error)

  message.guild.roles.find("name", "Moderators")
  // Remove a role!
  member.removeRole(role).catch(console.error)

  //Docs https://anidiotsguide.gitbooks.io/discord-js-bot-guide/information/understanding-roles.html
}
