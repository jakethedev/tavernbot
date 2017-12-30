const data = require('./arcdata.json') //relies on ./arcdata.json as a flatfile db. No reason for anything more robust.

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

generateAdventure = function(printToConsole = true){
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
  let response = `    === Setting the Hook ===
When the party enters ${encLocation}, a ${questnpc1} ${informEvent}.
The party is told that ${vEvent}.
The ${vname} was last seen heading ${vDxn}, retreating ${wildLoc}.
    === Quests and Complications ===
Shortly after their meeting with the ${questnpc1}, the party is contacted by a ${questnpc2}.
They are informed that ${quests[0]} ${quests[1]} and ${quests[2]}, and their help is needed in any way possible.
Unfortunately, are unaware that a ${defector} they pass on their way out of town is strongly alligned with the ${vname}.
The ${defector} was promised riches and safety for information and support`;
  if (console){
    console.log(response);
  } else {
    return response;
  }
}

module.exports = [ generateAdventure ];
console.log('advgen loaded!');
