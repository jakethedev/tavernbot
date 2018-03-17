// Ref: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
// Random number inclusive of both values, defaults to 1 -> max. Core dice function, 1dX where X is any integer
exports.d = function(sides, min = 1) {
  return Math.floor(Math.random() * (sides - min + 1)) + min;
}

//For those tricky decisions
exports.coin = function(input = 1) {
  if (isNaN(input) || input <= 1) {
    return 'the botcoin landed on ' + ['heads!', 'tails!'][exports.d(2) - 1]
  } else if (input > 1024) {
    return `I literally don't have enough coins for that, looks like I only have about a thousand copper in the bank`
  } else {
    let flipsDone = 0
    let results = [0, 0] //Same indexing as the faces array
    while (flipsDone++ < input) {
      results[exports.d(2) - 1]++
    }
    return `we flipped a total of ${results[0]} heads and ${results[1]} tails`
  }
}

// The crazy custom roll parser.
exports.dice = function(rollInput = '') {
  //Have a default
  if (!rollInput) return "a d20 skitters across the table, you rolled a " + exports.d(20)

  let response = '\n';
  for (rollSegment of rollInput.split(',')) {
    //Smash response together with each result
    let sum = 0
    for (rollComponent of rollSegment.split('+')) {
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

// Stat roller function. Uses an approved method and reports results cleanly
// TODO This should go in a character gen lib eventually
exports.rollstats = function(methodInput = '4d6k3') {
  const validMethods = ['4d6k3', '2d6+6', 'colville', 'funnel', '3d6']
  const method = validMethods.includes(methodInput) ? methodInput.toLowerCase() : validMethods[0]
  let stats = { 'STR': 0, 'DEX': 0, 'CON': 0, 'INT': 0, 'WIS': 0, 'CHA': 0 }
  if (method == '4d6k3') {
    for (const statName of Object.keys(stats)) {
      var lowest = 6
      for (var i = 0; i < 4; i++) {
        singleRoll = exports.d(6)
        lowest = singleRoll < lowest ? singleRoll : lowest
        stats[statName] += singleRoll
      }
      stats[statName] -= lowest
    }
  } else if (method == '2d6+6') {

  } else if (method == 'colville') {
    // Roll 4d6k3 until two 15+ stats have been achieved. This happens in order
  } else if (method in ['funnel', '3d6']) {

  }
  let [header, footer] = ['', '']
  for (stat in stats) {
    header += stat + ' '
    footer += stats[stat] + ' '
    while (footer.length < header.length) footer += ' '
  }
  return `the ${method} method has blessed you with: \n\`\`\`${header}\n${footer}\`\`\``
}