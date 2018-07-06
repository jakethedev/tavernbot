//Requires that randomUtil has loaded already.
require('../randomUtil')

//For those tricky decisions
exports.coin = function(input = 1) {
  if (`${input}`.toLowerCase() == 'help') return `help for coin`
  if (isNaN(input) || input <= 1) {
    return 'the botcoin landed on ' + ['heads!', 'tails!'][randIntMinZero(1)]
  } else if (input > 1024) {
    return `I don't get paid enough coin for that, I've got about a thousand copper in the bank`
  } else {
    let flipsDone = 0
    let results = [0, 0] //Same indexing as the faces array
    while (flipsDone++ < input) {
      results[randIntMinZero(1)]++
    }
    return `we flipped a total of ${results[0]} heads and ${results[1]} tails`
  }
}

// The crazy custom roll parser.
exports.dice = exports.d = function(rollInput = '') {
  //Nice defaults
  if (!rollInput) return "a d20 skitters across the table, you rolled a " + randIntMinOne(20)
  rollInput = rollInput.toLowerCase()
  if (rollInput == 'help') return `!dice XdY rolls a dY X times, you can sum varied dice, add constants, and comma separate rolls to have them all rolled at once!`
  if (rollInput.includes('-')) return `sorry, reverse math is not supported yet`

  rollInput = rollInput.replace(/\s/g, '') //Cut space, much easier to parse
  let response = 'the dice have fallen...\n';
  for (rollSegment of rollInput.split(',')) {
    //Smash response together with each result
    let sum = 0
    for (rollComponent of rollSegment.split('+')) {
      if (rollComponent.split('d').length === 2) { //XdY or dY format
        let [numRolls, diceSize] = rollComponent.split('d')
        numRolls = numRolls ? parseInt(numRolls) : 1
        diceSize = parseInt(diceSize)
        while (numRolls-- > 0) // Subtraction after comparison, trick from C
          sum += randIntMinOne(diceSize)
      } else if (!isNaN(rollComponent)) { // X format, crude yet effective
        sum += parseInt(rollComponent)
      } else {
        return `there was a problem parsing '${rollComponent}', make sure that it's in XdY or X format`
      }
    }
    response += `${rollSegment}: **${sum}**\n`
  }
  /**
   * Remaining potential here:
   *    roll(2d20 - 5)                Multiple sub const
   *    roll(2d20 - d6)               Multiple sub dice
   *    roll(2d20 + 1d12 + 1d6 + 7 - 1d4)   Long series
   *    roll(2d20, best)              Multiple take best
   *    roll(2d20, worst)             Multiple take worst
   */
  return response; // TODO: Parse input, roll dice, return reasonable output chunk
}

// Stat roller function. Uses an approved method and reports results cleanly
// TODO This should go in a character gen lib eventually
exports.rollstats = function(methodInput = '4d6k3') {
  if (methodInput.toLowerCase() == 'help') return `help for stats`
  const validMethods = ['4d6k3', '2d6+6', 'colville', 'funnel', '3d6']
  const method = validMethods.includes(methodInput) ? methodInput.toLowerCase() : validMethods[0]
  let stats = { 'STR': 0, 'DEX': 0, 'CON': 0, 'INT': 0, 'WIS': 0, 'CHA': 0 }

  // Build each stat based on the chosen method
  if (method == '4d6k3') {
    for (const statName of Object.keys(stats)) {
      var lowest = 6
      for (var i = 0; i < 4; i++) {
        singleRoll = randIntMinOne(6)
        lowest = singleRoll < lowest ? singleRoll : lowest
        stats[statName] += singleRoll
      }
      stats[statName] -= lowest
    }
  } else if (method == '2d6+6') {
    for (const statName of Object.keys(stats))
      stats[statName] += randIntMinOne(6) + randIntMinOne(6) + 6
  } else if (method == 'colville') {
    // Roll 4d6k3 until two 15+ stats have been achieved. This happens in order
  } else if (method == 'funnel' || method == '3d6') {
    for (const statName of Object.keys(stats))
      stats[statName] += randIntMinOne(6) + randIntMinOne(6) + randIntMinOne(6)
  }

  let [header, footer] = ['', '']
  for (stat in stats) {
    header += stat + ' '
    footer += stats[stat] + ' '
    while (footer.length < header.length) footer += ' '
  }
  return `the ${method} method has blessed you with: \n\`\`\`${header}\n${footer}\`\`\``
}