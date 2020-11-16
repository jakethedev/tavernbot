const os = require('os')
const MBinB = 1048576
const rand = require('../randomUtil')
const config = require('../config')

// Simple version, bug link, and release notes output
exports.version = function() {
  let response = `I am Tavernbot v**${config.version}**!\n\n`
  response += `**Release notes**\n${config.releasenotes}\n\n`
  response += `**Bug or feature request? Drop it here!**\n${config.issuelink}\n`
  return response
}

exports.feedback = function() {
  return `got feedback, ideas, or bugs? Awesome! Let me know on github at ${config.issuelink}`
}

exports.serverstats = function() {
  if (randIntMinOne(50) == 50) {
    return rand.choice([`I have no memory of this place`, `get me out of here!`, `life's good, the kids are well. How are you?`, `there has been an anomaly`])
  } else {
    let load = os.loadavg().map((val) => val.toPrecision(2))
    let free = Math.round(os.freemem() / MBinB)
    let max = Math.round(os.totalmem() / MBinB)
    let uptime = Math.round(os.uptime() / 3600.0)
    let desire = rand.choice(['raise', 'smoothie', 'piece of cake', 'chocolate pie', 'massage', 'day off', 'new manager', 'good D&D session', 'new set of dice'])
    return `I've been awake for ${uptime} hours, my workload looks like ${load}, I've got ${free} MB free of ${max}, and I really want a ${desire} - thanks for asking.`
  }
}