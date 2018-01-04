// Generic adventure hook generator, extendable for various settings
const validSettings = {
  'highFantasy': generateHighFantasy
}

//https://stackoverflow.com/a/12646864/6794180 - No native shuffle functions. Bummer.
shuffle = function(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

generateHighFantasy = function(){
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

generateAdventure = function(setting = 'highFantasy'){
  if (!setting in validSettings){
    return "Sorry, I only have ideas for these settings: " + validSettings.join(", ");
  }
  return validSettings[setting](); //Fingers crossed
}

module.exports = [ generateAdventure ];
console.log('adventuregen loaded!');
