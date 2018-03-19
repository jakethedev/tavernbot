exports.sass = function(input) {
  return 'ain\'t nobody got time for that'
}

exports.summon = function(input, message) {
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