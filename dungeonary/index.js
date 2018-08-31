// List all local components here
const components = [
  './adventuregen',
  './beastiary',
  './diceroller',
  './spellbook'
]

// Go through each chunk of the library and set each exported
// function as its own export of this module
for (sublib of components) {
  let lib = require(sublib)
  for (operation in lib) {
    exports[operation] = lib[operation]
  }
  console.log(sublib + " loaded!")
}
exports.helptext = () => "RPG Helper (Dungeonary) Commands"