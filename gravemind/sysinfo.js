// Simple version, bug link, and release notes output
exports.version = function() {
  let response = `I am Tavernbot v**${process.env.npm_package_version}**!\n\n`
  response += `**Release notes**\n${process.env.npm_package_releasenotes}\n\n`
  response += `**Bug or feature request? Drop it here!**\n${process.env.npm_package_bugs_url}\n`
  return response
}

// Util calls for the github issues link
exports.bug = function() {
  return `if you found a bug, please report it here: ${process.env.npm_package_bugs_url}`
}

exports.feedback = exports.request = exports.feature = function() {
  return `got a feature idea or some feedback? Awesome! Let me know here: ${process.env.npm_package_bugs_url}`
}

exports.memory = function() {
  return "I have no memory of this place"
}