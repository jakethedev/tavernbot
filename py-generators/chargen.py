#!/usr/bin/python

#Sourced from:
# http://rollmeapc.adventuresinnerdliness.net/

# IMPORT THE TWO PORTIONS OF random THAT ARE USED
from random import randint
from random import choice

# THIS VARIABLE IS USED TO DETERMINE IF THE TWEET IF <= 140 CHARACTERS. IT IS SET TO True (MEANING TWEET > 140 CHARACTERS) TO START THE LOOP. ONCE THE TWEET IS COMPOSED, ITS LENGTH IS DETERMINED, AND IF IT IS <= 140, verify IS CHANGED TO False AND THE LOOP IS BROKEN. IF TWEET > 140 verify REMAINS True AND PROCESS STARTS OVER.
verify = True

# ROLLS 3D6 RATHER THAN 3-18, AS THAT PROVIDES A MORE ACCURATE DISTRIBUTION
while (verify is True):
    s = str(randint(1,6) + randint(1,6) + randint(1,6))    # STRENGTH     - CONVERTED TO STRING
    i = str(randint(1,6) + randint(1,6) + randint(1,6))    # INTELLIGENCE - CONVERTED TO STRING
    w = str(randint(1,6) + randint(1,6) + randint(1,6))    # WISDOM       - CONVERTED TO STRING
    d = randint(1,6) + randint(1,6) + randint(1,6)         # DEXTERITY    - REMAINS INTEGER
    acb = d                                                # AC BONUS     - USED LATER TO DETERMINE ARMOR CLASS
    d = str(d)                                             # CONVERTS DEXTERITY TO STRING
    c = randint(1,6) + randint(1,6) + randint(1,6)         # CONSTITUTION - REMAINS INTEGER
    hpb = c                                                # HP BONUS     - USED LATER TO DETERMINE HIT POINTS
    c = str(c)                                             # CONVERTS CONSTITUTION TO STRING
    ch = str(randint(1,6) + randint(1,6) + randint(1,6))   # CHARISMA     - CONVERTED TO STRING
    gp = (randint(1,6) + randint(1,6) + randint(1,6)) * 10 # DETERMINES STARTING GOLD

    # DEFINE CLASSES, ALIGNMENTS, AND GENDERS
    classes = ["cleric","dwarf","elf","fighter","halfling","magic-user","thief"]
    alignment = ["L","N","C"]
    gender = ["female","male"]
    # DEFINE MAGIC-USER/ELF SPELLS
    spells = ["charm person","detect magic","floating disc","hold portal","light","magic missile","protection from evil","read languages","read magic","shield","sleep","ventriloquism"]
    # COIN FLIP FOR SHIELD
    hasshield = [True,False]

    # DETERMINE CLASS, ALIGNMENT, GENDER
    charclass = choice(classes)
    charalign = choice(alignment)
    sex = choice(gender)

    # DEFINE FIRST NAMES BASED ON RACE
    #hf = ["Amberlyn","Taryn","Brynn","Amy","Theresa","Lucretia","Arden"]
    with open('./femalehuman.txt') as lines:
        hf = lines.read().splitlines()
    #hm = ["Darius","Edgar","Ivan","Reginald","Carlos","Viggo","Ras","Pik","Pepto"]
    with open('./malehuman.txt') as lines:
        hm = lines.read().splitlines()
    #dm = ["Thorryn","Durgin","Odo"]
    with open('./maledwarf.txt') as lines:
        dm = lines.read().splitlines()
    #df = ["Alice","Vera","Ada"]
    with open('./femaledwarf.txt') as lines:
        df = lines.read().splitlines()
    #em = ["Kimber","Silverleaf"]
    with open('./maleelf.txt') as lines:
        em = lines.read().splitlines()
    #ef = ["Brynn","Aja"]
    with open('./femaleelf.txt') as lines:
        ef = lines.read().splitlines()
    #hfm = ["Bilbo","Frodo"]
    with open('./malehalfling.txt') as lines:
        hfm = lines.read().splitlines()
    #hff = ["Annie","Gertie"]
    with open('./femalehalfling.txt') as lines:
        hff = lines.read().splitlines()

    # DEFINE LAST NAMES BASED ON CLASS
    #clericlast = ["the Wise","the Pure","the Chaste","the Beautiful","God's Hammer",", Beloved of the Goddess","the Zealous","Ravenclaw"]
    with open('./clericlast.txt') as lines:
        clericlast = lines.read().splitlines()
    #dwarflast = ["Stonehand","Bearheart","Oakenshield","Goldfinder","Treetrunk"]
    with open('./dwarflast.txt') as lines:
        dwarflast = lines.read().splitlines()
    #fighterlast = ["the Brave","the Foolish","the Dashing","the Deadly","Hammerhand","Darkvale","Ravenclaw"]
    with open('./fighterlast.txt') as lines:
        fighterlast = lines.read().splitlines()
    #elflast = ["Swiftrunner","Willowfeather","Moondancer","the Fey","Lightstep","Greenleaf","Sparrowhawk"]
    with open('./elflast.txt') as lines:
        elflast = lines.read().splitlines()
    #halflinglast = ["Baggins","Boggins","Barefoot","Toejam","Tuggins","Fraggle"]
    with open('./halflinglast.txt') as lines:
        halflinglast = lines.read().splitlines()
    #magicuserlast = ["the White","the Black","the Grey","the Vile","the Mysterious","Whiteplume","the Mystical","Darkvale","the Abyssmal"]
    with open('./magicuserlast.txt') as lines:
        magicuserlast = lines.read().splitlines()
    #thieflast = ["the Swift","Back Biter","Lightstep","the Lucky","Redhand","the Rat","the Dandy","the Creeper","the Lurker"]
    with open('./thieflast.txt') as lines:
        thieflast = lines.read().splitlines()

    #charclass = "elf"
    #sex = "male"

    # PICKS A NAME BASED ON CLASS AND GENDER
    if charclass == "halfling":
        if sex == "female":
            first = choice(hff)
        else:
            first = choice(hfm)
        last = choice(halflinglast)
    elif charclass == "elf":
        if sex == "female":
            first = choice(ef)
        else:
            first = choice(em)
        last = choice(elflast)
    elif charclass == "dwarf":
        if sex == "female":
            first = choice(df)
        else:
            first = choice(dm)
        last = choice(dwarflast)
    else:
        if sex == "female":
            first = choice(hf)
        else:
            first = choice(hm)
        if charclass == "fighter":
            last = choice(fighterlast)
        elif charclass == "cleric":
            last = choice(clericlast)
        elif charclass == "magic-user":
            last = choice(magicuserlast)
        else:
            last = choice(thieflast)
    # CONSTRUCTS NAME AS STRING
    charname = first + " " + last + "\n"
    
    #Name source:
    #Some of the random names come from the following:
    #"List of Hobbit" at Wikipedia, taken from the Tolkein books. Most first and last names are from here.
    #Khordaldrum (Dwarven) Name Generator at The Red Dragon Inn
    #Sylvari (Elven) Name Generator at The Red Dragon Inn

    # USE CONSTITUTION SCORE TO DETERMINE HIT POINT MODIFIER
    if hpb == 3:
        hpb = -3
    elif hpb == 4 or hpb == 5:
        hpb = -2
    elif hpb == 6 or hpb == 7 or hpb == 8:
        hpb = -1
    elif hpb == 9 or hpb == 10 or hpb == 11 or hpb == 12:
        hpb = 0
    elif hpb == 13 or hpb == 14 or hpb == 15:
        hpb = 1
    elif hpb == 16 or hpb == 17:
        hpb = 2
    else:
        hpb = 3

    # USE CHARACTER CLASS AND HIT POINT MODIFIER TO DETERMINE HIT POINTS
    if charclass == "dwarf" or charclass == "fighter":
        hp = randint(1,8) + hpb
    elif charclass == "magic-user" or charclass == "thief":
        hp = randint(1,4) + hpb
    else:
        hp = randint(1,6) + hpb
    if hp < 1:
        hp = 1
    hp = "HP:" + str(hp)

    # USE DEXTERITY SCORE TO DETERMINE ARMOR CLASS MODIFIER
    if acb == 3:
        acb = 3
    elif acb == 4 or acb == 5:
        acb = 2
    elif acb == 6 or acb == 7 or acb == 8:
        acb = 1
    elif acb == 9 or acb == 10 or acb == 11 or acb == 12:
        acb = 0
    elif acb == 13 or acb == 14 or acb == 15:
        acb = -1
    elif acb == 16 or acb == 17:
        acb = -2
    else:
        acb = -3

    # SELECT ARMOR FROM WHAT IS AVAILABLE TO THE CLASS, AND SEE IF CHARACTER HAS A SHIELD IF ALLOWED
    if charclass == "thief":
        armors = ["none","leather"]
        armor = choice(armors)
        shield = False
    elif charclass == "magic-user":
        armor = "none"
        shield = False
    else:
        armors = ["none","leather","chain","plate"]
        armor = choice(armors)
        shield = choice(hasshield)

    # DETERMINE BASE ARMOR CLASS
    if armor == "none":
        ac = 9
    if armor == "leather":
        ac = 7
    if armor == "chain":
        ac = 5
    if armor == "plate":
        ac = 3
    # ADJUST FOR SHIELD
    if shield == True:
        ac = ac -1
    # ADJUST FOR DEXTERITY
    ac = ac + acb
    # CONVERT TO STRING FOR TWEET
    ac = "AC:" + str(ac) + " ("
    # ADD ARMOR TYPE TO TWEET
    if armor == "none" and shield is False:
        ac = ac + "cloth"
    if armor != "none":
        ac = ac + armor
    # IF ARMOR AND SHIELD, INCLUDE "/", IF SHIELD ONLY, EXCLUDE "/"
    if armor != "none" and shield:
        ac = ac + "/"
    if shield:
        ac = ac + "shield"
    ac = ac + ")"

    # BUILD ARMOR CLASS AND HIT POINTS STRING FOR TWEET
    achp = ac + " " + hp + "\n"

    # IF ARCANE SPELL CASTER, ADD SPELLBOOK AND SELECT RANDOM SPELL
    if charclass == "magic-user" or charclass == "elf":
        spellbook = "Spellbook: " + choice(spells) + "\n"
    else:
        spellbook = ""

    # PAY FOR ARMOR
    if shield:
        gp = gp - 10
    if armor == "leather":
        gp = gp - 20
    if armor == "chain":
        gp = gp - 40
    if armor == "plate":
        gp = gp - 60

    # SELECT WEAPON BASED ON CLASS AVAILABILITY LIST
    # IF CHARACTER HAS A SHIELD, EXCLUDE TWO HANDED WEAPONS
    if charclass == "magic-user":
        weapons = ["dagger","silver dagger"]
        weapon = choice(weapons)
    elif charclass == "halfling":
        if shield is False:
            weapons = ["hand axe","crossbow w/30 quarrels","short bow w/20 arrows","dagger","silver dagger","short sword","sword","mace","club","sling w/30 stones","spear","war hammer"]
        if shield:
            weapons = ["hand axe","dagger","silver dagger","short sword","sword","mace","club","sling w/30 stones","spear","war hammer"]
        weapon = choice(weapons)
    elif charclass == "cleric":
        weapons = ["mace","club","sling w/30 stones","war hammer"]
        weapon = choice(weapons)
    else:
        if shield is False:
            weapons = ["battle axe","hand axe","crossbow w/30 quarrels","long bow w/20 arrows","short bow w/20 arrows","dagger","silver dagger","short sword","sword","two-handed sword","mace","club","pole arm","sling w/30 stones","spear","war hammer"]
        if shield:
            weapons = ["hand axe","crossbow w/30 quarrels","long bow w/20 arrows","short bow w/20 arrows","dagger","silver dagger","short sword","sword","mace","club","sling w/30 stones","spear","war hammer"]
        weapon = choice(weapons)

    # IF CHOSEN WEAPON IS RANGED, CHARACTER IS ALSO GIVEN A CLUB
    weapon2 = ""
    if weapon == "crossbow w/30 quarrels" or weapon == "long bow w/20 arrows" or weapon == "short bow w/20 arrows" or weapon == "sling w/30 stones":
        weapon2 = "club"
        gp = gp - 3
        weapon2 = ", club"

    # PAY FOR WEAPON
    if weapon == "battle axe":
        gp = gp - 7
    elif weapon == "hand axe":
        gp = gp - 4
    elif weapon == "crossbow w/30 quarrels":
        gp = gp - 40
    elif weapon == "long bow w/20 arrows":
        gp = gp - 45
    elif weapon == "short bow w/20 arrows":
        gp = gp - 30
    elif weapon == "dagger":
        gp = gp - 3
    elif weapon == "silver dagger":
        gp = gp - 30
    elif weapon == "short sword":
        gp = gp - 7
    elif weapon == "sword":
        gp = gp - 10
    elif weapon == "two-handed sword":
        gp = gp - 15
    elif weapon == "mace":
        gp = gp - 5
    elif weapon == "club":
        gp = gp - 3
    elif weapon == "pole arm":
        gp = gp - 7
    elif weapon == "sling w/30 stones":
        gp = gp - 2
    elif weapon == "spear":
        gp = gp - 3
    elif weapon == "war hammer":
        gp = gp - 5
    else:
        gp = gp

    # DEFINE EQUIPMENT
    equipmentlist = ["backpack","flask of oil","hammer","12 spikes","lantern","mirror","iron rations","rations","50' rope","small sack","large sack","tinder box","6 torches","water skin","wine skin w/wine","wolfsbane","10' pole"]

    # IF YOU ARE A THIEF, YOU BUY THIEVE'S TOOLS
    if charclass == "thief":
        equipment = "thieve's tools"
        gp = gp - 25
    # IF YOU ARE A CLERIC YOU BUY A HOLY SYMBOL
    elif charclass == "cleric":
        equipment = "holy symbol"
        gp = gp - 25
        # IF YOU ARE A CLERIC AND STILL HAVE > 25GP, BUY HOLY WATER
        if gp > 25:
            equipment = equipment + ", holy water"
            gp = gp -25
    # OTHER CLASSES BUY A RANDOM PIECE OF EQUIPMENT THAT EXCLUDES THOSE ABOVE
    else:
        equipment = choice(equipmentlist)
    # CHOOSE ANOTHER ITEM. IF THE SAME ITEM IS PICKED AS ABOVE, PICK ANOTHER
    equipment2 = choice(equipmentlist)
    while (equipment2 == equipment):
        equipment2 = choice(equipmentlist)
    # BUILD EQUIPMENT STRING
    equipmentlist = equipment + ", " + equipment2

    # PAY FOR EQUIPMENT
    if equipment == "backpack":
        gp = gp - 5
    elif equipment == "flask of oil":
        gp = gp - 2
    elif equipment == "hammer":
        gp = gp - 2
    elif equipment == "12 spikes":
        gp = gp - 1
    elif equipment == "lantern":
        gp = gp - 10
    elif equipment == "mirror":
        gp = gp - 5
    elif equipment == "iron rations":
        gp = gp - 15
    elif equipment == "rations":
        gp = gp - 5
    elif equipment == "50' rope":
        gp = gp - 1
    elif equipment == "small sack":
        gp = gp - 1
    elif equipment == "large sack":
        gp = gp - 2
    elif equipment == "tinder box":
        gp = gp - 3
    elif equipment == "6 torches":
        gp = gp - 1
    elif equipment == "water skin":
        gp = gp - 1
    elif equipment == "wine skin w/wine":
        gp = gp - 2
    elif equipment == "wolfsbane":
        gp = gp - 10
    elif equipment == "10' pole":
        gp = gp - 1
    else:
        gp = gp
    
    if equipment2 == "backpack":
        gp = gp - 5
    elif equipment2 == "flask of oil":
        gp = gp - 2
    elif equipment2 == "hammer":
        gp = gp - 2
    elif equipment2 == "12 spikes":
        gp = gp - 1
    elif equipment2 == "lantern":
        gp = gp - 10
    elif equipment2 == "mirror":
        gp = gp - 5
    elif equipment2 == "iron rations":
        gp = gp - 15
    elif equipment2 == "rations":
        gp = gp - 5
    elif equipment2 == "50' rope":
        gp = gp - 1
    elif equipment2 == "small sack":
        gp = gp - 1
    elif equipment2 == "large sack":
        gp = gp - 2
    elif equipment2 == "tinder box":
        gp = gp - 3
    elif equipment2 == "6 torches":
        gp = gp - 1
    elif equipment2 == "water skin":
        gp = gp - 1
    elif equipment2 == "wine skin w/wine":
        gp = gp - 2
    elif equipment2 == "wolfsbane":
        gp = gp - 10
    elif equipment2 == "10' pole":
        gp = gp - 1
    else:
        gp = gp
        
    # IF GOLD SPENT > STARTING GOLD, SET GOLD TO ZERO
    if gp < 1:
        gp = 0

    # BUILD TWEET
    tweet = charname + sex + " #" + charclass + " (" + charalign + ")\nS:" + s + " I:" + i + " W:" + w + " D:" + d + " C:" + c + " Ch:" + ch + "\n"+ achp + spellbook + weapon + weapon2 + ", " + equipmentlist + "\n" + str(gp) + "gp\n#DnD"

    # DETERMINE CHARACTER LENGTH OF TWEET
    oneforty = len(tweet)

    # IF TWEET IS TOO LONG, START OVER UNTIL IT IS AN APPROPRIATE LENGTH
    if oneforty < 141:
        verify = False

# DISPLAY TWEET AS IT SHOULD APPEAR
print(tweet)

# USE Twython TO TWEET CHARACTER
from twython import Twython
from xxxxxxxx import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
twitter.update_status(status=tweet)
