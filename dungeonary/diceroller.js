// Ref: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
// Random number inclusive of both values, defaults to 1 -> max. Core dice function, 1dX where X is any integer
exports.d = function(sides, min = 1) {
  return Math.floor(Math.random() * (sides - min + 1)) + min;
}

//For those tricky decisions
exports.coin = function(){
  return 'the botcoin landed on ' + ( exports.d(2) == 1 ? 'heads' : 'tails' );
}

// The crazy custom roll parser.
exports.roll = function(rollInput = '') {
  //Have a default
  if (!rollInput) return "a d20 skitters across the table, you rolled a " + exports.d(20)

  let response = '\n';
  for ( rollSegment of rollInput.split(',') ) {
    //Smash response together with each result
    let sum = 0
    for ( rollComponent of rollSegment.split('+') ) {
      // console.log(rollComponent);
    }
    response += `Results for ${rollInput}: ${sum}\n`
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
