// See readme for more info, you can return raw data or a promise and the bot will reply
//    with either the data or the resolution of the promise

exports.newrole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `help for newrole`
  if (!message.member) return `you don't even live here, stop messing with things (err: not a server member)`
  // if (message.member.permissions.includes 'icandothings'){
  //   discord.addNewRole(name: input).copyFrom(everyone).randomColor()
  //   return `mission accomplished - your role called "${input}" is ready to rock`
  // }
  return `put that back, you're not allowed to touch it. (err: you don't have permission)`
}

//Given a rolename as input, add it to the requestor if it doesn't result in new privileges
exports.giverole = exports.addrole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `Usage: addrole/giverole 'the role name' will try to add the role to your user. Optionally, you can tag one person (after the role name) to attempt to give them the role`
  if (!input.trim()) return `you can't just add nothing as a role, that's not how any of this works!`
  let expectedRoleName = input.split('<')[0].toLowerCase().trim() //Expecting only one role, before any mentions
  // Allows us to add a role to someone, pinging them required
  let requestorName = message.member.user.username
  let optionalMention = message.mentions.members.first()
  let targetMember = optionalMention ? optionalMention : message.member
  let targetName = targetMember.user.username
  let roleToAdd = message.guild.roles.find((role) => expectedRoleName == role.name.toLowerCase())
  if (!roleToAdd){
    return `that role does not exist, checkest thy typing or speaketh with thy lord moderators`
  }
  console.log(`Role '${roleToAdd.name}' requested by ${requestorName} for ${targetName}...`)
  return targetMember.addRole(roleToAdd).then(result => {
    // S'gooood. This is idempotent, adding an existing role id a-ok
    return `${targetName} now has (or already had) the role ${roleToAdd.name}!`
  }).catch(err => {
    // Almost certainly a permission error
    return `I can't add ${targetName} to ${roleToAdd.name}, probably not allowed to. Contact an admin if this is unexpected`
  });
}

//List the requestor's roles.
//TODO Use this, list a target's roles; let targetToSummon = message.mentions.users.first()
exports.roles = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `roles will list the roles you have, if any`
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
  return message.member.removeRole(roleResult).then(result => {
    return `you are uninvited from ${input}`
  }).catch(error => {
    return `I'm afraid I can't do that, Dave. Either you don't have that role or a mod needs to handle it`
  })
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
