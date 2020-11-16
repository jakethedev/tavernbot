//Requires that randomUtil has loaded already.
const rand = require('../randomUtil')
const mathOps = "+-"

//For those tricky decisions
exports.coin = function(input = 1) {
  if (`${input}`.toLowerCase() == 'help') return `'coin [optional num of coins]' will flip as many coins as you want, up to as many coins as I have`
  if (isNaN(input) || input <= 1) {
    return 'the botcoin landed on ' + ['heads!', 'tails!'][rand.randIntMinZero(1)]
  } else if (input > 1024) {
    return `I don't get paid enough coin for that, I've got about a thousand copper in the bank`
  } else {
    let flipsDone = 0
    let results = [0, 0] //Same indexing as the faces array
    while (flipsDone++ < input) {
      results[rand.randIntMinZero(1)]++
    }
    return `we flipped a total of ${results[0]} heads and ${results[1]} tails`
  }
}

function diceRegexMatcher(rollInput) {
  // Turns '1d20+5+ 1d6 - 3d4 for fighting' into
  //      ['1d20', '+', '5', '+', '1d6', '-', '3d4']
  let diceRegex = /(\d*d?\d+)|[-\+]/g
  let matches = []
  while (match = diceRegex.exec(rollInput)) {
    if (mathOps.includes(match[0])){
      // + and - are external to capture groups but need to be matched for math stuff
      matches.push(match[0])
    } else {
      matches.push(match[1])
    }
  }
  return matches
}

// The crazy custom roll parser. It's a good parser, and it deserves more composition, but mehhhh
exports.roll = function(rollInput = '') {
  //Handy simple default
  if (!rollInput) return "a d20 skitters across the table, you rolled a " + rand.randIntMinOne(20)
  if (rollInput == 'help') return `'roll X, XdY, XdY +/- Z, XdY for stealth' - I can roll just about anything, make sure to use the XdY format, as 'roll 20' will just spit out 20. \nComments and subtraction as supported, and you can split up mutliple rolls with commas!`

  // Split up the input, regex-capture the right pieces, math them, and report the result
  let response = `here you go:\n`
  for (rollSegment of rollInput.split(',')) {
    let diceMatches = diceRegexMatcher(rollSegment)
    let segmentTotal = 0, subtractNextValue = false
    for (rollValue of diceMatches) {
      let tempSum = 0
      // Can be one of '+', '-', 'XdY', or 'X'.
      // If subtract, just note it for the next value.
      if (rollValue == '-') {
        subtractNextValue = true
        continue
      }
      // The actual rolling of dice
      if (rollValue.includes("d")) { //XdY or dY format
        let [numRolls, diceSize] = rollValue.split('d')
        numRolls = numRolls ? parseInt(numRolls) : 1
        diceSize = parseInt(diceSize)
        while (numRolls-- > 0) // Subtraction happens after comparison
          tempSum += rand.randIntMinOne(diceSize)
      } else if (rollValue.match(/^\d+$/)) { // A constant num
        tempSum += parseInt(rollValue)
      }
      // Complete subtract contract
      if (subtractNextValue){
        tempSum *= -1
        subtractNextValue = false
      }
      segmentTotal += tempSum
    }
    response += `${diceMatches.join(' ')}: **${segmentTotal}**\n`
  }
  /* Remaining potential:
   *    roll(2d20, best)              Multiple take best
   *    roll(2d20, worst)             Multiple take worst
   */
  return response
}

// Stat roller function. Uses an approved method and reports results cleanly
// TODO This should go in a character gen lib eventually
exports.rollstats = function(methodInput = '4d6k3') {
  const validMethods = ['4d6k3', '2d6+6', 'colville', 'funnel', '3d6']
  if (methodInput.toLowerCase() == 'help') return `'rollstats [method]' will give you a bunch of D&D-compatible stats, valid methods: [${validMethods.join(', ')}]`
  const method = validMethods.includes(methodInput) ? methodInput.toLowerCase() : validMethods[0]
  let stats = { 'STR': 0, 'DEX': 0, 'CON': 0, 'INT': 0, 'WIS': 0, 'CHA': 0 }

  // Build each stat based on the chosen method
  if (method == '4d6k3') {
    for (const statName of Object.keys(stats)) {
      var lowest = 6
      for (var i = 0; i < 4; i++) {
        singleRoll = rand.randIntMinOne(6)
        lowest = singleRoll < lowest ? singleRoll : lowest
        stats[statName] += singleRoll
      }
      stats[statName] -= lowest
    }
  } else if (method == '2d6+6') {
    for (const statName of Object.keys(stats))
      stats[statName] += rand.randIntMinOne(6) + rand.randIntMinOne(6) + 6
  } else if (method == 'colville') {
    // Roll 4d6k3 until two 15+ stats have been achieved. This happens in order
  } else if (method == 'funnel' || method == '3d6') {
    for (const statName of Object.keys(stats))
      stats[statName] += rand.randIntMinOne(6) + rand.randIntMinOne(6) + rand.randIntMinOne(6)
  }

  let [header, footer] = ['', '']
  for (stat in stats) {
    header += stat + ' '
    footer += stats[stat] + ' '
    while (footer.length < header.length) footer += ' '
  }
  return `the ${method} method has blessed you with: \n\`\`\`${header}\n${footer}\`\`\``
}