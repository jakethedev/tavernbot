from random import choice, shuffle
from arcdata import * #relies on ./arcdata.py as a flatfile db. No reason for anything more robust.

#Var setup, here's the magic
encLocation = choice(normal_places)
shuffle(npcs) # from arcdata
questnpc1   = npcs[0]
questnpc2   = npcs[1]
defector    = npcs[2]
informEvent = choice(npc_events)
villain     = choice(villains) # TODO Make real?
vname       = villain['name']
vEvent      = choice(villain['events'])
quests      = villain['consequences']
shuffle(quests)
vDxn        = choice(compass)
wildLoc     = choice(wild_places)

#main()
print('=== Setting the Hook ===')
print('When the party enters {}, a {} {}.'.format( encLocation, questnpc1, informEvent ))
print('The party is told that {}.'.format( vEvent ))
print('The {} was last heading {}, making its way {}'.format( vname, vDxn, wildLoc ))
print('=== Quests and Complications ===')
print('Shortly after their meeting with the {}, the party is contacted by a {}'.format( questnpc1, questnpc2 ))
print('They are informed that {} {} and {}, and their help is needed in any way possible'.format( quests[0], quests[1], quests[2], quests[3] ))
print('Unfortunately, are unaware that a {} they pass on their way out of town is strongly alligned with the {}'.format( defector, vname ))
print('The {} was promised riches and safety for information and support'.format(defector))

