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

// The crazy custom roll parser. It's a good parser, and it deserves more composition, but mehhhh
exports.dice = exports.d = exports.roll = function(rollInput = '') {
  //Handy simple default
  if (!rollInput) return "a d20 skitters across the table, you rolled a " + randIntMinOne(20)
  if (rollInput == 'help') return `!dice XdY rolls a dY X times, you can sum varied dice, add constants, and comma separate rolls to have them all rolled at once!`
  if (rollInput.includes('-')) return `sorry, reverse math is not supported yet`

  let response = `here you go:\n`;
  for (rollSegment of rollInput.split(',')) {
    //Smash response together with each mathy result, ignore non numeric stuff entirely so people can label rolls
    let sum = 0, parseSuccess = false
    for (rollValue of rollSegment.trim().split(/[+\t ]+/g)) {
      // TODO Use capture groups like a grownup
      if (rollValue.match(/^\d*d\d+$/)) { //XdY or dY format
        parseSuccess = true
        let [numRolls, diceSize] = rollValue.split('d')
        numRolls = numRolls ? parseInt(numRolls) : 1
        diceSize = parseInt(diceSize)
        while (numRolls-- > 0) // Subtraction happens after comparison
          sum += randIntMinOne(diceSize)
      } else if (rollValue.match(/^\d+$/)) { // A constant num
        parseSuccess = true
        sum += parseInt(rollValue)
      } else {
        // Assume we hit a comment or some other nonsense text
        console.log(`Hit a weird spot. Old segment: ${rollSegment}`)
        rollSegment = rollSegment.substring(0,rollSegment.indexOf(rollValue)).trim()
        if(!rollSegment)
          break
        console.log(`New segment: '${rollSegment}'`)
        // break
      }
    }
    if (parseSuccess) {
      response += `${rollSegment}: **${sum}**\n`
    }
    parseSuccess = false
  }
  /**
   * Remaining potential here:
   *    roll(2d20 - 5)                Multiple sub const
   *    roll(2d20 - d6)               Multiple sub dice
   *    roll(2d20 + 1d12 + 1d6 + 7 - 1d4)   Long series
   *    roll(2d20, best)              Multiple take best
   *    roll(2d20, worst)             Multiple take worst
   */
  return response
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