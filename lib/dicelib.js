// Ref: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
// Random number inclusive of both values, defaults to 1 -> max. Core dice function, 1dX where X is any integer
d = function(sides, min = 1) {
  return Math.floor(Math.random() * (sides - min + 1)) + min;
}
coin = function(){
  return (d(2) == 1 ? "heads" : "tails");
}

// The crazy custom roll parser.
customRoll = function(rollInput, player) {
  let response = 'Rolling ' + rollInput + '...';
  for ( rollSegment of rollInput.split(',') ) {
    //This should add results to 'response' as it goes
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
  return 'This was a triumph'; // TODO: Parse input, roll dice, return reasonable output chunk
}

module.exports = [d, coin, customRoll]

console.log('dicelib loaded!')

