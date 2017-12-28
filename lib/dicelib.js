
// Ref: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random

// Random number inclusive of both values, defaults to 1 -> max
randint = function(max, min = 1) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Basic Dice functions
d = function(x) { return randint(x); }
d100 = function() { return randint(100); }
d20 = function() { return randint(20); }
d12 = function() { return randint(12); }
d10 = function() { return randint(10); }
d8 = function() { return randint(8); }
d6 = function() { return randint(6); }
d4 = function() { return randint(4); }

// More advanced dice stuff
coin = function(){
  let flip = randint(2);
  if (flip === 1) {
    return "Heads";
  } else { 
    return "Tails";
  }
}
roll = function(rollInput, player) {
  for ( rollSegment of rollInput.split(',') ) {
    let sum = 0
    let output = `Rolling ${rollInput} for ${player}:`
    for ( rollComponent of rollSegment.split('+') ) {
      console.log(rollComponent);
    }
  }
  /**
   * Milestones:
   *    roll(d20)                     Base
   *    roll(2d20)                    Multiple
   *    roll(2d20 + 5)                Multiple add const
   *    roll(2d20 - 5)                Multiple sub const
   *    roll(2d20 + d6)               Multiple add dice
   *    roll(2d20 - d6)               Multiple sub dice
   *    roll(2d20 + 1d12 + 1d6 + 7 - 1d4)   Long series
   *    roll(2d20, best)              Multiple take best
   *    roll(2d20, worst)             Multiple take worst
   */
  return 4; // TODO: Parse input, roll dice, return reasonable output chunk
}

module.exports = [randint, d, d100, d20, d12, d10, d8, d6, d4, coin, roll]

console.log('dicelib loaded!')

