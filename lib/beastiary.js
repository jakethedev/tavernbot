const monsters5th = require('./data/5e-monsters.json')

validGames = {
  '5e': monsters5th
}

// Search function for available monsters per system.
exports.findMonsterInSrd = function(monsterName, gameSystem){
  if (! gameSystem in validGames ) {
    return "Sorry, I currently only have SRD beastiaries for: " + validGames.join(", ");
  }
  //TODO Search and return
  return "It's a dragon. It's always a dragon."
}

console.log('beastiary loaded!')
