exports.sass = function(input) {
  return 'ain\'t nobody got time for that'
}

exports.summon = function(input, message) {
  //TODO Consider a ring of :fire: and actually tagging summoned user
  if (message.mentions.users && message.mentions.users.size > 0) {
    let targetToSummon = message.mentions.users.first()
    let response = `your wish is my command.
    COME FORTH ${targetToSummon}! \`\`\`
             %%%    %%%
        %%%              %%%

    %%%                      %%%

   %%%                         %%%
          ${targetToSummon.nickname}
   %%%                         %%%

   %%%                        %%%

      %%%                  %%%

            %%%     %%%\`\`\``
    return response
  }
  return "you can't just summon nothing, that's not how this works!"
}