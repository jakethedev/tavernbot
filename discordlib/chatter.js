exports.sass = function(input) {
  return 'ain\'t nobody got time for that'
}

exports.summon = function(input, message) {
  //TODO Consider a ring of :fire: and actually tagging summoned user
  if (message.mentions.users) {
    if (message.mentions.users.size == 1) {
      let summoned = message.mentions.members.first()
      // The summon circle is 32 chars wide, 16 is the mid point
      let padding = ' '.repeat(18 - (summoned.displayName.length / 2))
      return `your wish is my command...

COME FORTH ${summoned}! \`\`\`
             %%%    %%%
        %%%              %%%

    %%%                      %%%

   %%%                         %%%
${padding + summoned.displayName}
   %%%                         %%%

   %%%                        %%%

      %%%                  %%%

            %%%     %%%\`\`\``
    }
  }
  return "you can't just summon nothing, that's not how this works!"
}