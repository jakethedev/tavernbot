##############
# All the data
##############

normal_places = [
        "a backalley",
        "the market district", 
        "the road out of town",
        "the shop",
        "the tavern", 
        "their quarters",
        "town hall",
        ]

npc_events = [
        "greets the party",
        "has a messenger deliver a summons to the party",
        "limps briskly up to the party",
        "quietly motions for the party to follow, then turns and sneaks away", 
        "runs up to the party",
        "sends for the party by raven",
        "stumbles in behind them mortally wounded",
        ]

npcs = [
        "family member",
        "farmer",
        "foreign ranger",
        "holy man",
        "hooded traveller",
        "known key NPC",
        "local bartender",
        "local shopkeep",
        "longtime friend",
        "member of local leadership",
        "priestess",
        "raving madman",
        "renowned warrior",
        "retired adventurer",
        "royal arcanist",
        "soldier's widow",
        "soldier's widower",
        "unknown key NPC",
        "wearied traveller",
        ]

# Array of dicts; used for randvill.name, random(randvill.events)
villains = [{
            'name': 'mysterious fey creature', 
            'events': [
                    'a fey-like series of monster attacks on the material plane',
                    ],
            'consequences': [
                'fey0',
                'fey1',
                'fey2',
                'fey3',
                'fey4',
                'fey5',
                'fey6',
                'fey7',
                'fey8',
                'fey9',
                ]
            },{
            'name': 'mighty dragon', 
            'events': [
                'a dragon razed a nearby village', 
                'a mother dragon was teaching her young to hunt by preying on local livestock and farmers',
                ],
            'consequences': [
                'dragon0',
                'dragon1',
                'dragon2',
                'dragon3',
                'dragon4',
                'dragon5',
                'dragon6',
                'dragon7',
                'dragon8',
                'dragon9',
                ]
            },{
            'name': 'dangerous warlord', 
            'events': [
                'a warlord has taken a nearby village', 
                'a vicious warmonger has threatened the capitol and plans to take it',
                ],
            'consequences': [
                'warlord0',
                'warlord1',
                'warlord2',
                'warlord3',
                'warlord4',
                'warlord5',
                'warlord6',
                'warlord7',
                'warlord8',
                'warlord9',
                ]
            },]

wild_places = [
        "deep into the earth through a recently torn chasm",
        "into the deep woods",
        "into the frozen wastes of the north",
        "straight into the sky until it vanished",
        "to the dense jungles of the tropics"
        "to the nearby mountains",
        "to the river",
        "towards the ocean",
        ]

compass = [
        "north",
        "northwest",
        "west",
        "southwest",
        "south",
        "southeast",
        "east",
        "northeast",
        ]
