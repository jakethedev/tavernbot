require('../randomUtil')

exports.sass = function(input, message) {
  if (input.toLowerCase() == 'help') return `yeah, I bet you need help`
  let raresassings = [
    `you just lost the game`,
    `I wish you a lifetime of flowers that say "she loves me not"`,
    `you're my favorite person besides every other person I've met`,
    `ah, you scared me, that must be one of those faces that only a mother can love`,
    `you're impossible to underestimate`,
  ]
  let sassings = [
    `seems to be up to no good, now I want to ban them from my neighborhood`,
    `you smell like you sleep outside`,
    `well aren't *you* delightful`,
    `oh no, its you`,
    `you know, you should probably be working`,
    `sorry, I was distracted by your weird hair, what?`,
    `I hope you get banned`,
    `get lost`,
    `ain't nobody got time for sassposts`,
    `I don't get paid enough to sass you`,
    `*don't you have an app for that?*`,
    `your father was an elderberry`,
    `your mother smelt of hamsters`,
    `sass is the only dish on the menu and you just got SERVED`,
    `today's main course is sassage with a side of sassbrowns`,
    `and then, a good *sassing*!`,
    `I think we've had enough, check please`,
    `nah`
  ]
  let sassindex = randIntMinOne(1000)
  if (sassindex < 20) {
    return choice(raresassings) + ' /r'
  } else {
    return choice(sassings)
  }
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
