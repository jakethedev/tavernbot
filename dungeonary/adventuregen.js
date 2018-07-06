//Preload all the things
require('../randomUtil')
const highFantasyData = require('./original/highFantasyArcs.json')
//const lowFantasy... etc

/****************************
 * Start of the generators
 ****************************/
genHighFantasy = function() {
  let data = highFantasyData;
  //Pick the actual stuff from the randomized input
  let encLocation = choice(data.normal_places);
  let npcs = shuffleArray(data.npcs);
  let questnpcs = shuffleArray(npcs);
  let informEvent = choice(data.npc_events);
  let villainType = choice(data.villainTypes);
  let villain = data.villains[villainType];
  let vname = villain.name;
  let vEvent = choice(villain['events']);
  let quests = shuffleArray(villain['consequences']);
  let vDxn = choice(data.compass);
  let wildLoc = choice(data.wild_places);
  //Throw it at the user
  let response = `<<< The Hook >>>
When the party enters ${encLocation}, a ${questnpcs[0]} ${informEvent}.
The party is told that ${vEvent} - they were last seen to the ${vDxn}, heading ${wildLoc}.
<<< Quests and Complications >>>
Shortly after their meeting with the ${questnpcs[0]}, the party is contacted by a ${questnpcs[1]}.
They are informed that ${quests[0]} ${quests[1]} and ${quests[2]}, and their help is needed in any way possible.
The party is unaware that a ${questnpcs[2]} they pass on the street is connected to the ${vname}.
The ${questnpcs[2]} was promised riches/safety/glory for work as a spy`;

  return response;
}

genLowFantasy = function() {
  //TODO
  return "You start in a tavern and a fight breaks out over the last crumb of bread"
}

genModern = function() {
  //TODO
  return "You're walking through the woods. There's no one around you, and your phone is dead"
}

genSpace = function() {
  //TODO
  return "A long long time ago, in a galaxy far far away, there were daddy issues"
}

genSteampunk = function() {
  //TODO
  return "The gears of society have ground to a halt, and a grinding hulk of mechanized doom lurches toward you"
}

genCyberpunk = function() {
  //TODO
  return "He takes a long drag from a vaporfuse, slams another adrenaline patch on his arm, and rushes you"
}

/****************************
 * End of the Generators
 ****************************/


// Magic table of generators. We search through the keys of this to determine
// which generator the user is trying to use
const validSettings = {
  'highfantasy': genHighFantasy,
  'lowfantasy': genLowFantasy,
  'modern': genModern,
  'spaceage': genSpace,
  'steampunk': genSteampunk,
  'cyberpunk': genCyberpunk
}

// Default to high fantasy hooks, and prefix-search validSettings for the right generator.
// So the user doesn't have to type '!cmd highfantasy' every time, just '!cmd hi'
exports.hook = function(setting = '') {
  setting = (setting ? setting.toLowerCase() : 'highfantasy')
  if (setting.toLowerCase() == 'help') return `help for hook`
  const validSettingNames = Object.keys(validSettings);
  let firstMatch = validSettingNames.filter((name) => name === setting || name.startsWith(setting))[0]
  if (!firstMatch || !validSettings[firstMatch]) {
    return "Sorry, I only have ideas for these settings: " + Object.keys(validSettings).join(", ") +
      ". Protip: you can prefix search - 'hig' will return 'highfantasy' hooks!";
  }
  return validSettings[firstMatch]();
}