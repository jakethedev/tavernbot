require('../randomUtil')

exports.sass = function(input, message) {
  if (input.toLowerCase() == 'help') return `yeah, I bet you need help`
  let sassings = [
    `ain't nobody got time for sassposts`,
    `I don't get paid enough to sass you`,
    `*don't you have a bot for that?*`,
    `your father was an elderberry`,
    `your mother smelt of hamsters`,
    `here, I gift you a sass. It is all yours now, take good care of it`,
    `sass is the only dish on the menu and you just got spoonfed`,
    `today's main course is sassage with a side of sassbrowns and you just got **served**`,
    `and then, a good *sassing*!`,
    `I think we've had enough, check please`,
    `it's like checkmate, jenga, yahtzee, touchdown, and a three-pointer all at once when I sass you`
  ]
  return choice(sassings)
}

exports.summon = function(input, message) {
  if (input.toLowerCase() == 'help') return `'summon tag-a-user' will spontaneously generate a summoning circle for your user of choice`
  if (message.mentions.users) {
    if (message.mentions.users.size == 1) {
      let summoned = message.mentions.members.first()
      // The summon circle is ~36 chars wide, 18 or 19 is the mid point
      let padding = ' '.repeat(18 - (summoned.displayName.length / 2))
      return `your wish is my command...

COME FORTH ${summoned}! \`\`\`
             %#%    %#%
        %#%              %#%

    %#%                      %#%

   %#%                         %#%
${padding + summoned.displayName}
   %#%                         %#%

    %#%                      %#%

        %#%              %#%
             %#%    %#%\`\`\``
    }
  }
  return "you can't just summon nothing, that's not how this works!"
}