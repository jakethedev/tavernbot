// See readme for more info, you can return raw data or a promise and the bot will reply
//    with either the data or the resolution of the promise

exports.newrole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `'newrole new-role-name' will create a new role with the same permissions as the everybody role`
  if (!message.member) return `you don't even live here, stop messing with things (err: not a server member)`
  // if (message.member.permissions.includes 'icandothings'){
  //   discord.addNewRole(name: input).copyFrom(everyone).randomColor()
  //   return `mission accomplished - your role called "${input}" is ready to rock`
  // }
  return `under construction (nothing to see here)`
  // return `put that back, you're not allowed to touch it. (err: you don't have permission)`
}

//Given a rolename as input, add it to the requestor if it doesn't result in new privileges
exports.giverole = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `Usage: addrole/giverole 'the role name' will try to add the role to your user. Optionally, you can tag one person (after the role name) to attempt to give them the role`
  if (!input.trim()) return `you can't just add nothing as a role, that's not how any of this works!`
  let expectedRoleName = input.split('<')[0].toLowerCase().trim() //Expecting only one role, before any mentions
  // Allows us to add a role to someone, pinging them required
  if (message.guild) {
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
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

// List roles on the server that the bot can assign
exports.allroles = function(input, message, client) {
  if (input.toLowerCase() == 'help')
    return `'roles' will get you a list of the server roles that I can grant you`
  // If we're on a server, get them roles - reply intelligently in unhappy circumstances
  if (message.guild) {
    const roleList = message.guild.roles
                      .filter(role => !role.name.includes('@everyone'))
                      .map(role => `'${role.name}'`)
                      .sort()
                      .join(', ')
    if(roleList) {
      return `a server has many roles:\n${roleList}`
    } else {
      return `a server has no roles, bribe a mod to add one`
    }
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

//List the requestor's roles
exports.myroles = function(input, message, client) {
  if (input.toLowerCase() == 'help') return `'myroles' will list all roles you have here`
  if (message.guild) {
    const userRolesRaw = message.member.roles
    let roleResults = []
    // Stash the results, strip any @ symbols to avoid pinging @everyone every single time
    userRolesRaw.forEach(role => roleResults.push(role.name.replace('@', '')))
    if (roleResults[0]) {
      return `here are your roles: [${roleResults.join(', ')}]`
    } else {
      return `your purpose is to butter toast. (no roles found)`
    }
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

//Self-remove a role, after verifying that the author is a member (role-bearer)
exports.unrole = function(input, message, client) {
  if (!input || input.toLowerCase() == 'help') return `'unrole rolename' will rolename from your roles if you have it`
  if (message.guild) {
    let userRoles = message.member.roles
    if (userRoles.size == 0)
      return `it seems that you have no roles, and that's really funny`
    let roleResult = userRoles.find(role => role.name.toLowerCase() === input.toLowerCase())
    return message.member.removeRole(roleResult).then(result => {
      return `you are uninvited from ${input}`
    }).catch(error => {
      return `I'm afraid I can't do that, Dave. Either you don't have that role or a mod needs to handle it`
    })
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

//Number of people in a given role
exports.rolesize = function(input = '', message, client) {
  if (!input) return `give me a role and I'll give you an answer`
  if (input.toLowerCase() == 'help') return `'rolesize role-name' prints the size of a role - this might go away soon though`
  if (message.guild) {
    let roleResult = getGuildRole(input, message)
    if (roleResult) {
      let roleCount = roleResult.members.size
      return `there are ${roleCount} members in ${roleResult.name}`
    } else {
      return `role not found - gimme the role's full name, and I'll get you a member count`
    }
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

//List people in a given role
exports.rolemembers = function(input = '', message, client) {
  if (!input) return `give me a role and I'll give you an answer`
  if (input.toLowerCase() == 'help') return `'rolemembers role-name' definitely doesn't list the members of a role`
  if (message.guild) {
    let role = getGuildRole(input, message)
    if (role && role.members.size) {
      let roleMemberList = role.members.map(m => m.displayName).join(', ')
      return `${role.name} has the following members:\n${roleMemberList}`
    } else if (role) {
      return `${role.name} is a quiet, empty place with no members`
    } else {
      return `role '${input}' not found - I need the role's full name to get you a roll call`
    }
  } else {
    return `run this command on a server with roles to get a more helpful response :)`
  }
}

////////////////////////////
// Internal Helper Functions
////////////////////////////

// Takes in the name of a role and a discord message
function getGuildRole(input, message) {
  input = input.trim().toLowerCase()
  return message.guild.roles.find(role => role.name.toLowerCase() === input)
}