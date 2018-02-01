exports.sass = function(input){
  return 'ain\'t nobody got time for that'
}

exports.summon = function(input, message){
  if (message.mentions && message.mentions.users.first){
    let targetToSummon = message.mentions.users.first
    let response = `Throwing a salt circle...

  \`\`\`           %%%    %%%
        %%%              %%%

    %%%                      %%%

   %%%                         %%%
          ${targetToSummon}
   %%%                         %%%

   %%%                        %%%

      %%%                  %%%

            %%%     %%%\`\`\``
    return response
  }
  return 'you can\'t just summon nothing, that\'s not how this works!'
}
