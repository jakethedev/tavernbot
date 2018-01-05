const spells5th = require('./data/5e-spells.json')

get5eSpell = function(){
  //something with the spells5th constant
  return "FIREBALLLLL";
}

validGames = {
  '5e': get5eSpell
}

// Search function for available spell data per system.
exports.searchSrdForSpell = function(monsterName, gameSystem){
  if (! gameSystem in validGames ) {
    return "Sorry, I currently only have SRD spell archives for: " + validGames.join(", ");
  }
  //TODO Search and return
  return "A fiery doomy fireball of doom."
}

console.log('spellbook loaded!')
