//Preload all the things
const highFantasyData = require('./data/highFantasyArcs.json')
//const lowFantasy... etc

//https://stackoverflow.com/a/12646864/6794180 - No native shuffle functions. Bummer.
//Needed to smash up our data arrays for randomness
shuffle = function(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

/****************************
* Start of the generators
****************************/
genHighFantasy = function(){
  let data = highFantasyData;
  //Pick the actual stuff from the randomized input
  let encLocation = shuffle(data.normal_places)[0];
  let npcs        = shuffle(data.npcs);
  let questnpc1   = npcs[0];
  let questnpc2   = npcs[1];
  let defector    = npcs[2];
  let informEvent = shuffle(data.npc_events)[0];
  let villainType = shuffle(data.villainTypes)[0];
  let villain     = data.villains[villainType];
  let vname       = villain.name;
  let vEvent      = shuffle(villain['events'])[0];
  let quests      = shuffle(villain['consequences']);
  let vDxn        = shuffle(data.compass)[0];
  let wildLoc     = shuffle(data.wild_places)[0];
  //Throw it at the user
  let response = `<<< The Hook >>>
When the party enters ${encLocation}, a ${questnpc1} ${informEvent}.
The party is told that ${vEvent} - they were last seen to the ${vDxn}, heading ${wildLoc}.
<<< Quests and Complications >>>
Shortly after their meeting with the ${questnpc1}, the party is contacted by a ${questnpc2}.
They are informed that ${quests[0]} ${quests[1]} and ${quests[2]}, and their help is needed in any way possible.
The party is unaware that a ${defector} they pass on the street is connected to the ${vname}.
The ${defector} was promised riches/safety/glory for work as a spy`;

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
exports.rpghook = function(setting = 'highfantasy'){
  const validSettingNames = Object.keys(validSettings);
  let firstMatch = validSettingNames.filter((name) => name.startsWith(setting))[0]
  if (!firstMatch || !validSettings[firstMatch]){
    return "Sorry, I only have ideas for these settings: " + Object.keys(validSettings).join(", ") +
      ". Protip: you can prefix search - 'hig' will return 'highfantasy' hooks!" ;
  }
  return validSettings[firstMatch](); //Fingers crossed
}
