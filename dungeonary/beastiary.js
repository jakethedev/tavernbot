const monsters5th = require('./5e/monsters.json')
const rand = require('../randomUtil')

validGames = {
  '5e': monsters5th
}

// Search function for available monsters per system.
exports.monster = function(inputMonster, gameSystem = '5e') {
  if (inputMonster.toLowerCase() == 'help') return `'monster name [optional game system]' will try to get you OGL info about the monster for your chosen game system (default: 5e)`
  if (!gameSystem in validGames) {
    return "Sorry, I currently only have SRD beastiaries for: " + validGames.join(", ");
  }
  //TODO Search and return
  return `It's a dragon. It's always a dragon (under construction)`
}
