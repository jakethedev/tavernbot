# Dungeonary - The Ultimate Gamemaster and D&D Utility Lib
###Ideas or suggestions? [Drop an issue on Github](https://github.com/JakeRunsDnD/tavernbot/issues) and I'll do my best to add it!

It's like a library but magic!

This is a core component of the [TavernBot](https://github.com/JakeRunsDnD/tavernbot) project. This library is constantly being updated with fresh SRD content for various RPGs, and is
intended as a general-use RPG library. Dungeonary is made up of the following pieces:

### Working Components:
- adventuregen.js: An adventure hook generator, a lazy GM's best frienst! It has content and solid adventure
generation for high fantasy adventures, and it has stubs for Low Fantasy, Modern, Space, Cyberpunk, and Steampunk
settings. I plan to implement them all and continually update the options available.

### In-progress Components:
- diceroller.js: Pretty straightforward, my goal here is the smallest and fastest comprehensive
dice roller. It will be able to handle queries like "2d20k1+5, 5d6+5-2d4" as a single input, and return
output in array and sum form
- beastiary.js: Monster lookup! I currently have SRD info for 5e and Pathfinder, but I still have
to get searching and formatting complete. Then we'll have a great monster lookup tool that can be
implemented anywhere, from Discord to a Blog!
- spellbook.js: Same thing as beastiary.js but with spells.

### Future Components:
- quest.js: For general and flexible session-sized-adventure generation! When you have an arc and
you're grasping at straws for what an NPC needs the PCs to do, quest.js will be there to help
- pc.js: Gimme characters! This will initially support simple 5e level 1 generation based on the
official SRD, and will expand to include Pathfinder and other systems. This will also support
creation of [funnel characters!](https://rpg.stackexchange.com/a/51229/31197)
- npc.js: Gimme npcs! Always a handy tool, no rpg library is complete without a proper npc generator.
This library will also handle name generation
- feats.js: A feat lookup system could be neat
- Dungeon world/Fate/Other System support: I'd like to add srd support for fate, DW, and several other
systems in the spell and monster lookup and character generation

Note: This is currently an 0.x release, expect in-progress components to be fully fleshed out by 1.0. I'm pouring free time into this project, so hopefully that's soon :)
