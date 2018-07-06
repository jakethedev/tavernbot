const spells5th = require('./5e/spells.json')

//First, we create a bunch of search functions. Then we map them to their systems in 'validGames'
//On input, we can search for the system the user asks for, then if we have that system,
//search the srd for the spell they wanted and spew out some info

get5eSpell = function() {
  //something with the spells5th constant
  return "A fiery doomy fireball of doom."
}

validGames = {
  '5e': get5eSpell
}

// Search function for available spell data per system.
exports.spell = function(inputSpell, gameSystem = '5e') {
  if (inputSpell.toLowerCase() == 'help') return `help for spellbook`
  if (!gameSystem in validGames) {
    return "Sorry, I currently only have SRD spell archives for: " + validGames.join(", ");
  }
  //TODO Search and return
  return validGames[gameSystem]();
}
