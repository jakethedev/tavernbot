import re
import math
import yaml
import random
import argparse
from collections import namedtuple, Counter
from .namerator import make_name


def roll_stat():
    nums = [random.randint(1, 6) for _ in range(4)]
    return sum(nums) - min(nums)


class Alignment:

    def __str__(self):
        if (self.law, self.good) == ('neutral', 'neutral'):
            return 'neutral'
        return '{} {}'.format(self.law, self.good)

    def __repr__(self):
        return 'Alignment({})'.format(self)

    def __init__(self, law, good):
        self.law = law
        self.good = good

    @classmethod
    def parse(cls, s):
        if isinstance(s, cls):
            return Alignment(s.law, s.good)
        s = s.lower().strip()
        if s in ('neutral', 'true neutral', 'neutral neutral'):
            return cls('neutral', 'neutral')
        alignment = s.split()
        if len(alignment) != 2:
            raise ValueError('cant parse alignment: {!r}'.format(s))
        if alignment[0] not in ('lawful', 'neutral', 'chaotic'):
            raise ValueError('{!r} is not "lawful", "neutral", or "chaotic"'
                             .format(alignment[0]))
        if alignment[1] not in ('good', 'neutral', 'evil'):
            raise ValueError('{!r} is not "good", "neutral", or "evil"'
                             .format(alignment[1]))
        return cls(*alignment)

    @classmethod
    def random(cls):
        law = random.choice(['chaotic', 'neutral', 'lawful'])
        good = random.choice(['evil', 'neutral', 'good'])
        return cls(law, good)


VALID_SUBRACES = {
    'dwarf': ['hill', 'mountain'],
    'elf': ['high', 'wood', 'dark'],
    'halfling': ['lightfoot', 'stout'],
    'human': ['calishite', 'chondathan', 'damaran', 'illuskan', 'mulan',
              'rashemi', 'shou', 'tethyrian', 'turami'],
    'dragonborn': ['black', 'blue', 'brass', 'bronze', 'copper', 'gold',
                   'green', 'red', 'silver', 'white'],
    'gnome': ['forest', 'rock'],
}

DRAGON_ANCESTRY = {
    'black': ('acid', 'acid breath (5 by 30 ft line, dex save)'),
    'blue': ('lightning', 'lightning breath (5 by 30 ft line, dex save)'),
    'brass': ('fire', 'fire breath (5 by 30 ft line, dex save)'),
    'bronze': ('lightning', 'lightning breath (5 by 30 ft line, dex save)'),
    'copper': ('acid', 'acid breath (5 by 30 ft line, dex save)'),
    'gold': ('fire', 'fire breath (15 ft cone, dex save)'),
    'green': ('poison', 'poison breath (15 ft cone, con save)'),
    'red': ('fire', 'fire breath (15 ft cone, dex save)'),
    'silver': ('ice', 'ice breath (15 ft cone, con save)'),
    'white': ('ice', 'ice breath (15 ft cone, con save)'),
}

HIT_DICE = {
    'barbarian': 12,
    'bard': 8,
    'cleric': 8,
    'druid': 8,
    'fighter': 10,
    'monk': 8,
    'paladin': 10,
    'ranger': 10,
    'rogue': 8,
    'sorcerer': 6,
    'warlock': 8,
    'wizard': 6,
    None: 8,
}

DESIRED_STATS = {
    'barbarian': ('str', 'con'),
    'bard': ('cha', 'dex'),
    'cleric': ('wis',),
    'druid': ('wis',),
    'fighter': ('str', 'con'),
    'monk': ('dex', 'wis'),
    'paladin': ('str', 'cha'),
    'ranger': ('dex', 'wis'),
    'rogue': ('dex',),
    'sorcerer': ('cha',),
    'warlock': ('cha',),
    'wizard': ('int',),
    None: [],
}

RE_ROLL = re.compile(
    r'^(?P<num>\d+)d(?P<sides>\d+)\s*(?:(?P<sign>[+-])\s*(?P<plus>\d+))?$'
)


Stats = namedtuple('Stats', ['str', 'dex', 'con', 'int', 'wis', 'cha'])


def to_feet(ft, inches):
    return ft + (inches / 12)


def to_inches(ft):
    f = int(ft)
    i = round((ft - f) * 12)
    if i == 12:
        return (f + 1, 0)
    return (f, i)


def rand_height(mn, mx):
    r = random.uniform(to_feet(*mn), to_feet(*mx))
    return to_inches(r)


def rand_weight(avg, mn, thresh=2.5):
    return round(
        max(
            min(
                random.gauss(avg, mn),
                avg + mn * thresh
            ),
            avg - mn * thresh
        )
    )


def modifier(stat):
    return math.floor((stat - 10) / 2)


def roll(s):
    if isinstance(s, int):
        return s
    m = RE_ROLL.match(s)
    if not m:
        if s.isdigit():
            return int(s)
        raise ValueError('not a valid roll string (eg "2d8+2"): {!r}'.format(s))
    if m.group('sign') is not None:
        s = int('{}{}'.format(m.group('sign'), m.group('plus')))
    else:
        s = 0
    for _ in range(int(m.group('num'))):
        s += random.randint(1, int(m.group('sides')))
    return s


class Warrior:

    def roll_initiative(self):
        self.initiative = roll('1d20') + modifier(self.dex)

    def roll_attack(self, enemy_ac):
        d20 = roll('1d20') + self.attack
        return d20 >= enemy_ac

    def roll_damage(self):
        return roll(self.damage)

    def is_dead(self):
        return self.current_hp <= 0

    def reset(self):
        self.current_hp = self.hp


class NPC(Warrior):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.load(f)
        players = []
        for p in data['players']:
            players.append(cls(**p))
        return players

    def __init__(self, name=None, klass=None, gender=None, race=None,
                 subrace=None, stats=None, level=1, hp=None, ac=10,
                 damage=None, attack=None, alignment=None):
        if alignment is None:
            self.alignment = Alignment.random()
        else:
            self.alignment = Alignment.parse(alignment)
        self.flaw = self.random_flaw()
        self.bond = self.random_bond()
        self.ideal = self.random_ideal()
        self.trait = self.random_trait()
        self.gender = gender or random.choice(['male', 'female'])
        self.race = race or random.choice([
            'human', 'elf', 'half-elf', 'dwarf', 'gnome', 'half-orc',
            'halfling', 'tiefling', 'dragonborn',
        ])
        self.name = name or make_name(self.race, gender=self.gender)
        self.subrace = subrace
        if self.subrace is None:
            self._random_subrace()
        self.klass = klass
        if stats is None:
            self.roll_stats(klass=klass)
        else:
            self.stats = Stats(**stats)
            attrs = DESIRED_STATS[self.klass]
            self._add_racial_stats(attrs=attrs)
        self.level = level
        self.ac = ac
        self.hp = hp or self._calc_hp()
        self.current_hp = self.hp
        self.damage = damage
        self.attack = attack

    @classmethod
    def random_flaw(cls):
        return random.choice(FLAWS)

    @classmethod
    def random_bond(cls):
        return random.choice(BONDS)

    @classmethod
    def random_trait(cls):
        return random.choice(TRAITS)

    def random_ideal(self):
        ideals = IDEALS['any'][:]
        ideals.extend(IDEALS[self.alignment.law])
        ideals.extend(IDEALS[self.alignment.good])
        return random.choice(ideals)

    def _random_subrace(self):
        if self.race in VALID_SUBRACES:
            self.subrace = random.choice(VALID_SUBRACES[self.race])

    def _calc_hp(self):
        base = HIT_DICE[self.klass]
        auto = (base / 2) + 1
        mod = modifier(self.con)
        hp = base + mod
        if (self.race, self.subrace) == ('dwarf', 'hill'):
            hp += 1
        for _ in range(1, self.level):
            hp += auto + mod
            if (self.race, self.subrace) == ('dwarf', 'hill'):
                hp += 1
        return hp

    def roll_stats(self, klass=None):
        stats = sorted([roll_stat() for _ in range(6)], reverse=True)
        attrs = DESIRED_STATS[self.klass]
        if klass is None:
            random.shuffle(stats)
            self.stats = Stats(*stats)
        else:
            self.stats = self._setup_stats(stats, attrs)
        self.stats = self._add_racial_stats(attrs=attrs)

    def _add_racial_stats(self, attrs=None):
        self.speed = 30
        self.size = 'medium'
        self.profs = set()
        self.abilities = set()
        self.resistances = set()
        self.immunities = set()
        self.advantages = set()
        self.languages = {'common'}
        kwargs = dict(**self.stats._asdict())
        if self.race == 'dwarf':
            self.age = random.randint(25, 300)
            self.height = rand_height((4, 0), (5, 0))
            self.weight = rand_weight(150, 20)
            kwargs['con'] += 2
            self.speed = 25
            self.abilities.add('darkvision')
            self.profs |= {'battleaxe', 'handaxe', 'light hammer', 'warhammer'}
            toolprof = random.choice(["smith's tools", "brewer's supplies",
                                      "mason's tools"])
            self.profs.add(toolprof)
            self.languages.add('dwarvish')
            self.resistances.add('poison')
            self.advantages.add('saving throw vs poison')
            self.abilities.add('stonecunning')
            if self.subrace == 'hill':
                self.abilities.add('dwarven toughness')
                kwargs['wis'] += 1
            elif self.subrace == 'mountain':
                kwargs['str'] += 2
                self.profs |= {'light armor', 'medium armor'}
        elif self.race == 'elf':
            kwargs['dex'] += 2
            self.age = random.randint(50, 700)
            self.height = rand_height((5, 6), (6, 3))
            self.weight = rand_weight(180, 40)
            self.abilities |= {'darkvision', 'trance', 'fey ancestry'}
            self.profs.add('perception')
            self.advantages.add('saving throw vs charm')
            self.immunities.add('sleep')
            self.languages.add('elvish')
            if self.subrace == 'high':
                kwargs['int'] += 1
                self.abilities |= {'free wizard cantrip', 'extra language'}
                self.profs |= {'longsword', 'longbow', 'shortsword', 'shortbow'}
            elif self.subrace == 'wood':
                self.speed = 35
                self.profs |= {'longsword', 'longbow', 'shortsword', 'shortbow'}
                self.abilities |= {'fleet of foot', 'mask of the wild'}
                kwargs['wis'] += 1
            elif self.subrace in ('dark', 'drow'):
                kwargs['cha'] += 1
                self.abilities.remove('darkvision')
                self.abilities |= {'superior darkvision',
                                   'sunlight sensitivity',
                                   'drow magic'}
                self.profs |= {'rapier', 'shortsword', 'hand crossbow'}
        elif self.race == 'halfling':
            kwargs['dex'] += 2
            self.size = 'small'
            self.speed = 25
            self.age = random.randint(16, 120)
            self.height = rand_height((2, 2), (3, 8))
            self.weight = rand_weight(40, 7)
            self.advantages.add('saving throw vs frightened')
            self.abilities |= {'brave', 'lucky', 'halfling nimbleness'}
            self.languages.add('halfling')
            if self.subrace == 'lightfoot':
                kwargs['cha'] += 1
                self.abilities.add('naturally stealthy')
            elif self.subrace == 'stout':
                kwargs['con'] += 1
                self.resistances.add('poison')
                self.advantages.add('saving throw vs poison')
        elif self.race == 'human':
            self.age = random.randint(16, 75)
            self.height = rand_height((5, 2), (6, 6))
            self.weight = rand_weight(200, 50)
            self.abilities.add('extra language')
            for key in kwargs:
                kwargs[key] += 1
        elif self.race == 'dragonborn':
            kwargs['str'] += 2
            kwargs['cha'] += 1
            self.age = random.randint(12, 70)
            self.height = rand_height((6, 0), (7, 6))
            self.weight = rand_weight(250, 50)
            self.languages.add('draconic')
            dtyp, breath = DRAGON_ANCESTRY[self.subrace]
            self.abilities.add('{} draconic ancestry'.format(self.subrace))
            self.abilities.add(breath)
            self.resistances.add(dtyp)
        elif self.race == 'gnome':
            kwargs['int'] += 2
            self.size = 'small'
            self.speed = 25
            self.abilities |= {'darkvision', 'gnome cunning'}
            self.languages.add('gnomish')
            self.advantages.add('saving throw vs magic (int, wis, cha)')
            self.age = random.randint(16, 450)
            self.height = rand_height((3, 0), (4, 2))
            self.weight = rand_weight(40, 7)
            if self.subrace == 'forest':
                self.abilities |= {'minor illusion cantrip',
                                   'speak with small beasts'}
                kwargs['dex'] += 1
            elif self.subrace == 'rock':
                self.abilities |= {'artificer\'s lore',
                                   'tinker'}
                self.profs.add("tinker's tools")
                kwargs['con'] += 1
        elif self.race == 'half-elf':
            kwargs['cha'] += 2
            self.age = random.randint(16, 165)
            self.weight = rand_weight(180, 45)
            self.height = rand_height((5, 0), (6, 2))
            self.abilities |= {'darkvision', 'extra language', 'fey ancestry',
                               '2 extra skill proficiencies'}
            self.advantages.add('saving throw vs charm')
            self.immunities.add('sleep')
            self.languages.add('elvish')
            remaining = {'str', 'dex', 'con', 'int', 'wis'}
            added = 0
            for attr in (attrs or [])[:2]:
                if attr in remaining:
                    kwargs[attr] += 1
                    remaining.remove(attr)
                    added += 1
            while added < 2:
                key = random.choice(list(remaining))
                kwargs[key] += 1
                added += 1
                remaining.remove(key)
        elif self.race == 'half-orc':
            self.age = random.randint(12, 65)
            self.weight = rand_weight(220, 55)
            self.height = rand_height((5, 6), (6, 8))
            self.profs.add('intimidation')
            self.abilities |= {'darkvision', 'relentless endurance',
                               'savage attacks', 'menacing'}
            self.languages.add('orc')
            kwargs['str'] += 2
            kwargs['con'] += 1
        elif self.race == 'tiefling':
            self.age = random.randint(16, 90)
            self.weight = rand_weight(200, 50)
            self.height = rand_height((5, 2), (6, 4))
            self.resistances.add('fire')
            self.abilities |= {'darkvision', 'hellish resistance',
                               'infernal legacy'}
            self.languages.add('infernal')
            kwargs['int'] += 1
            kwargs['cha'] += 2
        self.profs = sorted(self.profs)
        self.resistances = sorted(self.resistances)
        self.abilities = sorted(self.abilities)
        self.languages = ['common'] + sorted(self.languages - {'common'})
        self.immunities = sorted(self.immunities)
        self.advantages = sorted(self.advantages)
        return Stats(**kwargs)

    def _setup_stats(self, stats, attrs):
        stats = sorted(stats, reverse=True)
        kwargs = {}
        for attr in attrs:
            kwargs[attr] = stats[0]
            stats = stats[1:]
        remaining = list(
            {'str', 'dex', 'con', 'int', 'wis', 'cha'} - set(attrs)
        )
        random.shuffle(remaining)
        for key in remaining:
            kwargs[key] = stats[0]
            stats = stats[1:]
        return Stats(**kwargs)

    def __getattr__(self, attr):
        if attr in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            return getattr(self.stats, attr)
        raise AttributeError('no attribute {!r}'.format(attr))

    def _random_appearance(self):
        pass

    def _random_personality(self):
        pass

    def output(self):
        print('Name:      {}'.format(self.name))
        if self.klass:
            print('Level:     {}'.format(self.level))
            print('Class:     {}'.format(self.klass.title()))
        if self.subrace:
            racestr = '{} {}'.format(self.subrace, self.race)
        else:
            racestr = self.race
        print('Race:      {}'.format(racestr.title()))
        print('Alignment: {}'.format(str(self.alignment).title()))
        print('')
        print('Gender:    {}'.format(self.gender.title()))
        print('Age:       {}'.format(self.age))
        print('Height:    {}\'{}"'.format(*self.height))
        print('Weight:    {} lbs'.format(self.weight))
        print('Trait:     {}'.format(self.trait))
        print('Ideal:     {}'.format(self.ideal))
        print('Bond:      {}'.format(self.bond))
        print('Flaw:      {}'.format(self.flaw))
        if self.resistances:
            print('Resist:    {}'.format(', '.join(self.resistances)))
        if self.immunities:
            print('Immune:    {}'.format(', '.join(self.immunities)))
        if self.advantages:
            print('Advantage: {}'.format(', '.join(self.advantages)))
        if self.languages:
            print('Languages: {}'.format(', '.join(self.languages)))
        if self.abilities:
            print('Abilities: {}'.format(', '.join(self.abilities)))
        print('Proficiencies: {}'.format(', '.join(self.profs)))
        print('')
        print('HP:  {}'.format(self.hp))
        print('AC:  {}'.format(self.ac))
        print('SPD: {}'.format(self.speed))
        print('STR: {:2} ({:+})'.format(self.str, modifier(self.str)))
        print('DEX: {:2} ({:+})'.format(self.dex, modifier(self.dex)))
        print('CON: {:2} ({:+})'.format(self.con, modifier(self.con)))
        print('INT: {:2} ({:+})'.format(self.int, modifier(self.int)))
        print('WIS: {:2} ({:+})'.format(self.wis, modifier(self.wis)))
        print('CHA: {:2} ({:+})'.format(self.cha, modifier(self.cha)))


class MonsterEntity(Warrior):

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = yaml.load(f)
        monsters = []
        for m in data:
            for i in range(m['num']):
                mon = cls(**m)
                mon.name = '{}{}'.format(mon.race, i + 1)
                monsters.append(mon)
        return monsters

    def __init__(self, **data):
        self.race = data['name']
        self.stats = Stats(**data['stats'])
        self.hp = roll(data['hp'])
        self.current_hp = self.hp
        self.ac = data['ac']
        self.damage = data['damage']
        self.attack = data['attack']

    def __getattr__(self, attr):
        if attr in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            return getattr(self.stats, attr)
        raise AttributeError('no attribute {!r}'.format(attr))


class TestEncounter:

    def __init__(self, players_path, encounter_path):
        self.players = NPC.load(players_path)
        self.monsters = MonsterEntity.load(encounter_path)
        with open(encounter_path) as f:
            self.monster_data = yaml.load(f)

    def alive_players(self):
        return [x for x in self.players if not x.is_dead()]

    def alive_monsters(self):
        return [x for x in self.monsters if not x.is_dead()]

    def dead_players(self):
        return [x for x in self.players if x.is_dead()]

    def dead_monsters(self):
        return [x for x in self.monsters if x.is_dead()]

    def reset(self):
        for i in self.players + self.monsters:
            i.reset()

    def run(self):
        for i in self.players:
            i.roll_initiative()
        for m in self.monster_data:
            init = roll('1d20') + modifier(m['stats']['dex'])
            for mon in self.monsters:
                if m['name'] == mon.race:
                    mon.initiative = init
        order = sorted(self.players + self.monsters, key=lambda x: x.initiative,
                       reverse=True)
        while bool(self.alive_players()) and bool(self.alive_monsters()):
            for o in order:
                if not self.alive_players():
                    break
                if not self.alive_monsters():
                    break
                if o.is_dead():
                    continue
                if isinstance(o, NPC):
                    enemy = random.choice(self.alive_monsters())
                elif isinstance(o, MonsterEntity):
                    enemy = random.choice(self.alive_players())
                if not o.roll_attack(enemy.ac):
                    continue
                dmg = o.roll_damage()
                enemy.current_hp -= dmg

    def run_many(self, ct):
        c = Counter()
        for _ in range(ct):
            self.reset()
            self.run()
            c.update([
                x.name for x in
                self.dead_players() + self.dead_monsters()
            ])
        for ent, total in c.most_common():
            print('{} died {:.3%} of the time out of {} simulations'.format(
                ent, total / ct, ct,
            ))


BONDS = [
    'I would lay down my life for the people I served with.',
    'By preserving the natural order I ensure the continuation of the good in the world',
    'The goal of a life of study is the betterment of oneself.',
    'Solitude and contemplation are paths toward mystical or magical power.',
    'We have to take care of each other, because no one else is going to do it.',
    "My house's alliance with another noble family must be sustained at all costs.",
    'Peace between individuals is the most pleasant state of affairs.',
    'Performance of one’s duty is the highest honor',
    'I seek to preserve a sacred text that my enemies consider heretical and seek to destroy.',
    "Someone stole my precious instrument, and someday I'll get it back.",
    "There's no good pretending to be something I'm not.",
    "It is each person's responsibility to make the most happiness for the whole tribe.",
    'In life as in war, the stronger force wins.',
    'My stature in regard to myself and others is paramount.',
    'The old order is nothing compared to what will follow.',
    "I've been searching my whole life for the answer to a certain question.",
    'I sponsor an orphanage to keep others from enduring what I was forced to endure.',
    'My city, nation, or people are all that matter.',
    'I protect those who cannot protect themselves.',
    'Emotions must not cloud our logical thinking.',
    'I suffer awful visions of a coming disaster and will do anything to prevent it.',
    'Action against all odds and reality represents the strength of the individual in relation to the world.',
    'If I dishonor myself, I dishonor my whole clan.',
    "I come from a noble family, and one day I'll reclaim my lands and title from those who stole them from me.",
    'I am defined purely by how capable I am.',
    "I seek to prove myself worthy of my god's favor by matching my actions against his or her teachings.",
    'My honor is my life.',
    'I will someday get revenge on the corrupt temple hierarchy who branded me a heretic.',
    'The world is at constant war with itself, and by arbitrating between those parts outside and inside myself, I am more in tune with it',
    'There is no greater shame than a betrayal.',
    'If I do not correctly understand the world, then I cannot realistically engage with it.',
    'If I engage in the world through close examination of my place and my actions within it, I am able to be most fruitful',
    "My town or city is my home, and I'll fight to defend it.",
    'By boldly behaving in a way contrary to expectations, I cause the world to be more exciting.',
    'The rich need to be shown what life and death are like in the gutters.',
    'I would die to recover an ancient artifact of my faith that was lost long ago.',
    'In order for life to remain valuable, there must be obstacles to overcome and problems to face',
    'I have an ancient text that holds terrible secrets that must not fall into the wrong hands.',
    'Nothing and no one can steer me away from my higher calling.',
    'My gifts are meant to be shared with all, not used for my own benefit.',
    'The strongest are meant to rule. ',
    "I hope to one day rise to the top of my faith's religious hierarchy. ",
    'I work hard to be the best there is at my craft.',
    'The most rewarding part of humanoid experience lies exploration and excitement',
    'The thing that keeps a ship together is mutual respect between captain and crew.',
    'The ship is most important--crewmates and captains come and go.',
    'To feel emotions - love, hate, greed, compassion - is the most humanoid thing that the individual can do.',
    "I'm only in it for the money.",
    "I never target people who can't afford to lose a few coins. ",
    'No one should get preferential treatment before the law, and no one is above the law. ',
    "I'm determined to make something of myself.",
    'I will become the greatest thief that ever lived.',
    "I'm going to prove that I'm worthy of a better life.",
    "There's a spark of good in everyone.",
    'Knowledge is the path to power and domination',
    'Nothing is more important that achieving one’s goals.',
    'It is the duty of all civilized people to strengthen the bonds of community and the security of civilization. ',
    'Art should reflect the soul; it should come from within and reveal who we really are.',
    'My loyalty to my sovereign is unwavering.',
    'In order to achieve my ends, I must be able to control the environment around me.',
    'I was cheated of my fair share of the profits, and I want to get my due.',
    'Material goods come and go. Bonds of friendship last forever.',
    'People need to be united so that they do not destroy each other.',
    'We must help bring about the changes the gods are constantly working in the world. ',
    "My life's work is a series of tomes related to a specific field of lore.",
    'I fight for those who cannot fight for themselves.',
    'Someone saved my life on the battlefield. To this day, I will never leave a friend behind.',
    'I do what I must and obey just authority.',
    'When people follow orders blindly they embrace a kind of tyranny.',
    'Emotions must not cloud our sense of what is right and true, or our logical thinking.',
    'The act of living is also the act of changing, and by not changing one denies his very living.',
    'I have a family, but I have no idea where they are. One day, I hope to see them again.',
    'An injury to the unspoiled wilderness of my home is an injury to me.',
    'My talents were given to me so that I could use them to benefit the world.',
    'I worked the land, I love the land, and I will protect the land.',
    'I sold my soul for knowledge. I hope to do great deeds and win it back.',
    'Doing acts that make the world a better place is the best way for me to spend my life.',
    'I owe me life to the priest who took me in when my parents died.',
    'When I perform, I make the world better than it was. ',
    "Someday I'll own my own ship and chart my own destiny. ",
    'I always try to help those in need, no matter what the personal cost.',
    "A powerful person killed someone I love. Some day soon, I'll have my revenge.",
    'In a harbor town, I have a paramour whose eyes nearly stole me from the sea.',
    'Life is like the seasons, in constant change, and we must change with it. ',
    'I owe my guild a great debt for forging me into the person I am today.',
    'The sea is freedom--the freedom to go anywhere and do anything.',
    "I owe everything to my mentor--a horrible person who's probably rotting in jail somewhere.",
    "Somewhere out there I have a child who doesn't know me. I'm making the world better for him or her.",
    'My family, clan, or tribe is the most important thing in my life, even when they are far from me.',
    'I will do anything to protect the temple where I served.',
    'I am a free spirit--no one tells me what to do.',
    "I'm trying to pay off an old debt I owe to a generous benefactor.",
    'Everyone should be free to pursue his or her livelihood.',
    'I will face any challenge to win the approval of my family.',
    'The obscene and the unusual are beautiful.',
    "I help people who help me--that's what keeps us alive.",
    'I entered seclusion to hide from the ones who might still be hunting me. I must someday confront them.',
    'If I can attain more power, no one will tell me what to do. ',
    'People need to be united so that they can all achieve common goals.',
    "I idolize a hero of the old tales and measure my deeds against that person's.",
    "No one else is going to have to endure the hardships I've been through.",
    "I like seeing the smiles on people's faces when I perform. That's all that matters. ",
    'I wish my childhood sweetheart had come with me to pursue my destiny.',
    'True action requires the individual to be sure of their beliefs.',
    'I will do whatever it takes to become wealthy. ',
    'If you know yourself, there’s nothing left to know.',
    'I will bring terrible wrath down on the evildoers who destroyed my homeland.',
    'I would do anything for the other members of my old troupe.',
    'I search for inspiring sights and extraordinary circumstances',
    'The stories, legends, and songs of the past must never be forgotten.',
    'What is beautiful points us beyond itself toward what is true.',
    'The greater community should produce things: art, commerce, experience, etc...',
    "I'm committed to my crewmates, not to ideals. ",
    'I am in love with the heir of a family that my family despises.',
    "I'll always remember my first ship.",
    "I'm only in it for the money and fame. ",
    'People deserve to be treated with dignity and respect.',
    'I am the last of my tribe, and it is up to me to ensure their names enter legend.',
    'I owe my survival to another urchin who taught me to live on the streets.',
    'Should my discovery come to light, it could bring ruin to the world.',
    'Those who fight beside me are those worth dying for.',
    "I'm loyal to my captain first, everything else second.",
    "I'm guilty of a terrible crime. I hope I can redeem myself for it.",
    "I'll never forget the crushing defeat my company suffered or the enemies who dealt it.",
    'If I become strong, I can take what I want--what I deserve.',
    'Respect is due to me because of my position, but all people regardless of station deserve to be treated with dignity.',
    'One day I will return to my guild and prove that I am the greatest artisan of them all.',
    'It is my duty to provide children to sustain my tribe.',
    'I entered seclusion because I loved someone I could not have.',
    'Chains are meant to be broken, as are those who would forge them. Tyrants must not be allowed to oppress the people. ',
    'A proud noble once gave me a horrible beating, and I will take my revenge on any bully I encounter.',
    'One true measure of my accomplishments is the recognition of others',
    'When an act brings another pain or destruction, it must be answered in appropriate proportion.',
    'All people, rich or poor, deserve respect. ',
    'Everything I do is for the common people.',
    'My personal ideals and beliefs are small compared to what I can pdo by devoting myself to a cause or individual',
    'Our lot is to lay down our lives in defense of others.',
    'Life is more enjoyable when it is organized in clearly marked boxes.',
    'The world is in need of new ideas and bold action.',
    'It is my duty to protect my students.',
    'I fleeced the wrong person and must work to ensure that this individual never crosses paths with me or those I care about.',
    'My isolation gave me great insight into a great evil that only I can destroy.',
    'I will do anything to prove myself superior to me hated rival.',
    'I must prove that I can handle myself without the coddling of my family. ',
    "I'm still seeking the enlightenment I pursued in my seclusion, and it still eludes me.",
    'It is my duty to protect and care for the people beneath me. ',
    "I escaped my life of poverty by robbing an important person, and I'm wanted for it.",
    'We all do the work, so we all share in the rewards.',
    'Nothing is more important that the other members of my family.',
    "I'm a predator, and the other ships on the sea are my prey.",
    'Nothing should fetter the infinite possibility inherent in all existence.',
    'I steal from the wealthy so that I can help people in need.',
    'Freedom of action and thought are the primary concerns of any civilized society.',
    'In order to make my life worth living, I must explore who I am and learn about the world',
    "I'm committed to the people I care about, not to ideals. ",
    'Chaotic forces in the universe serve only to disrupt real progress and development.',
    'My tools are symbols of my past life, and I carry them so that I will never forget my roots.',
    'It is my duty to respect the authority of those above me, just as those below me must respect mine.',
    'Live and Let Live. ',
    'I must be able to control myself first if I wish to honestly affect the world.',
    'The workshop where I learned my trade is the most important place in the world to me.',
    'Something important was taken from me, and I aim to steal it back.',
    'I work to preserve a library, university, scriptorium, or monastery.',
    'I want to be famous, whatever it takes.',
    'The natural world is more important than all the constructs of civilization.',
    'Someone I loved died because of a mistake I made. That will never happen again.',
    'I must earn glory in battle, for myself and my clan.',
    'I will get revenge on the evil forces that destroyed my place of business and ruined my livelihood.',
    'The alignment of one’s goals to an established system allows me to do greater things than I could on my own.',
    'By discovering more about Vthe world around me, I am able to more accurately align my views with the reality of the universe.',
    'I owe a debt I can never repay to the person who took pity on me.',
    'There is something pure and honest at the moment when something new is learned or knowledge of the universe is gained',
    'The outcome of my life is less important than how beautiful it was.',
    'My ill-gotten gains go to support my family.',
    'Flights of fancy and listening to a good story are far more important than the physical world.',
    'Nothing is more important than the other members of my hermitage, order, or association.',
    "I don't steal from others in the trade.",
    'Meddling in the affairs of others only causes trouble.',
    'The new and the untimely are beautiful in and of themselves, because they are original creations in the world.',
    'My instrument is my most treasured possession, and it reminds me of someone I love.',
    'The common folk must see me as a hero of the people.',
    'The path to power and self-improvement is through knowledge.',
    'Inquiry and curiosity are the pillars of progress.',
    'I distribute money I acquire to the people who really need it. ',
    'The ancient traditions of worship and sacrifice must be preserved and upheld. ',
    'I never run the same con twice. ',
    "I created a great work for someone, and then found them unworthy to receive it. I'm still looking for someone worthy.",
    "I swindled and ruined a person who didn't deserve it. I seek to atone for my misdeeds but might never be able to forgive myself.",
    'The low are lifted up, and the high and mighty are brought down. Change is the nature of things.',
    "I'm loyal to my friends, not to any ideals, and everyone else can take a trip down the Styx for all I care.  ",
    "I pursue wealth to secure someone's love.",
    'Ruthless pirates murdered my captain and crewmates, plundered our ship, and left me to die. Vengeance will be mine.',
    'My life has meaning because I am able to freely enjoy myself in the world.',
    'Blood runs thicker than water.',
]

IDEALS = {
    'any': [
        "Aspiration. I seek to prove my self worthy of my god's favor by matching my actions against his or her teachings.",
        "Aspiration. I'm determined to make something of myself.",
        'Honesty. Art should reflect the soul; it should come from within and reveal who we really are.',
        'Destiny. Nothing and no one can steer me away from my higher calling.',
        'Aspiration. I work hard to be the best there is at my craft.',
        "Self-Knowledge. If you know yourself, there're nothing left to know.",
        'Family. Blood runs thicker than water.',
        'Glory. I must earn glory in battle, for myself and my clan.',
        "Aspiration. Someday I'll own my own ship and chart my own destiny.",
        'Nation. My city, nation, or people are all that matter.',
        "Aspiration. I'm going to prove that I'm worthy of a better life.",
    ],
    'chaotic': [
        'Change. We must help bring about the changes the gods are constantly working in the world.',
        'Independence. I am a free spirit--no one tells me what to do.',
        'Creativity. I never run the same con twice.',
        'Freedom. Chains are meant to be broken, as are those who would forge them.',
        'Creativity. The world is in need of new ideas and bold action.',
        'Freedom. Tyrants must not be allowed to oppress the people.',
        'Freedom. Everyone should be free to pursue his or her livelihood.',
        'Free Thinking. Inquiry and curiosity are the pillars of progress.',
        'Independence. I must prove that I can handle myself without the coddling of my family.',
        'Change. Life is like the seasons, in constant change, and we must change with it.',
        'No Limits. Nothing should fetter the infinite possibility inherent in all existence.',
        'Freedom. The sea is freedom--the freedom to go anywhere and do anything.',
        'Independence. When people follow orders blindly they embrace a kind of tyranny.',
        'Change. The low are lifted up, and the high and mighty are brought down. Change is the nature of things.',
    ],
    'evil': [
        'Greed. I will do whatever it takes to become wealthy.',
        "Greed. I'm only in it for the money and fame.",
        'Might. If I become strong, I can take what I want--what I deserve.',
        "Greed. I'm only in it for the money.",
        'Power. Solitude and contemplation are paths toward mystical or magical power.',
        'Power. If I can attain more power, no one will tell me what to do.',
        'Might. The strongest are meant to rule.',
        'Power. Knowledge is the path to power and domination.',
        "Master. I'm a predator, and the other ships on the sea are my prey.",
        'Might. In life as in war, the stronger force wins.',
        'Retribution. The rich need to be shown what life and death are like in the gutters.',
    ],
    'good': [
        'Charity. I always try to help those in need, no matter what the personal cost.',
        'Charity. I distribute money I acquire to the people who really need it.',
        'Friendship. Material goods come and go. Bonds of friendship last forever.',
        'Charity. I steal from the wealthy so that I can help people in need.',
        "Redemption. There's a spark of good in everyone.",
        'Beauty. When I perform, I make the world better than it was.',
        'Respect. People deserve to be treated with dignity and respect.',
        'Generosity. My talents were given to me so that I could use them to benefit the world.',
        'Greater Good. My gifts are meant to be shared with all, not used for my own benefit.',
        'Respect. Respect is due to me because of my position, but all people regardless of station deserve to be treated with dignity.',
        'Noble Obligation. It is my duty to protect and care for the people beneath me.',
        "Greater Good. It is each person's responsibility to make the most happiness for the whole tribe.",
        'Beauty. What is beautiful points us beyond itself toward what is true.',
        'Respect. The thing that keeps a ship together is mutual respect between captain and crew.',
        'Greater Good. Our lot is to lay down our lives in defense of others.',
        'Respect. All people, rich or poor, deserve respect.',
    ],
    'lawful': [
        'Faith. I trust that my deity will guide my actions. I have faith that if I work hard, things will go well.',
        'Tradition. The ancient traditions of worship and sacrifice must be preserved and upheld.',
        "Power. I hope to one day rise to the top of my faith's religious hierarchy.",
        "Fairness. I never target people who can't afford to lose a few coins.",
        "Honor. I don't steal from others in the trade.",
        'Tradition. The stories, legends, and songs of the past must never be forgotten.',
        'Fairness. No one should get preferential treatment before the law, and no one is above the law.',
        'Community. It is the duty of all civilized people to strengthen the bonds of community and the security of civilization.',
        'Logic. Emotions must not cloud our sense of what is right and true, or our logical thinking.',
        'Responsibility. It is my duty to respect the authority of those above me, just as those below me must respect mine.',
        'Honor. If I dishonor myself, I dishonor my whole clan.',
        'Logic. Emotions must not cloud our logical thinking.',
        'Fairness. We all do the work, so we all share in the rewards.',
        'Responsibility. I do what I must and obey just authority.',
        'Community. We have to take care of each other, because no one else is going to do it.',
    ],
    'neutral': [
        "People. I'm loyal to my friends, not to any ideals, and everyone else can take a trip down the Styx for all I care.",
        "People. I like seeing the smiles on people's faces when I perform. That's all that matters.",
        "Sincerity. There's no good pretending to be something I'm not.",
        "People. I'm committed to the people I care about, not to ideals.",
        'Live and Let Live. Meddling in the affairs of others only causes trouble.',
        'Nature. The natural world is more important than all the constructs of civilization.',
        'Knowledge. The path to power and self-improvement is through knowledge.',
        "People. I'm committed to my crewmates, not to ideals.",
        "Ideals aren't worth killing for or going to war for.",
        "People. I help people who help me--that's what keeps us alive.",
    ]
}

TRAITS = [
    "I idolize a particular hero of my faith and constantly refer to that person's deeds and example.",
    'I can find common ground between the fiercest enemies, empathizing with them and always working toward peace.',
    'I see omens in every event and action. The gods try to speak to us, we just need to listen.',
    'Nothing can shake my optimistic attitude.',
    'I quote (or misquote) the sacred texts and proverbs in almost every situation.',
    'I am tolerant (or intolerant) of other faiths and respect (or condemn) the worship of other gods.',
    "I've enjoyed fine food, drink, and high society among my temple's elite. Rough living grates on me.",
    "I've spent so long in the temple that I have little practical experience dealing with people in the outside world.",
    'I fall in and out of love easily, and am always pursuing someone.',
    'I have a joke for every occasion, especially occasions where humor is inappropriate.',
    'Flattery is my preferred trick for getting what I want.',
    "I'm a born gambler who can't resist taking a risk for a potential payoff.",
    "I lie about almost everything, even when there's no good reason to.",
    'Sarcasm and insults are my weapons of choice.',
    'I keep multiple holy symbols on me and invoke whatever deity might come in useful at any given moment.',
    'I pocket anything I see that might have some value.',
    'I always have plan for what to do when things go wrong.',
    'I am always calm, no matter what the situation. I never raise my voice or let my emotions control me.',
    'The first thing I do in a new place is note the locations of everything valuable--or where such things could be hidden.',
    'I would rather make a new friend than a new enemy.',
    'I am incredibly slow to trust. Those who seem the fairest often have the most to hide.',
    "I don't pay attention to the risks in a situation. Never tell me the odds.",
    "The best way to get me to do something is to tell me I can't do it.",
    'I blow up at the slightest insult.',
    'I know a story relevant to almost every situation.',
    'Whenever I come to a new place, I collect local rumors and spread gossip.',
    "I'm a hopeless romantic, always searching for that 'special someone'.",
    'Nobody stays angry at me or around me for long, since I can defuse any amount of tension.',
    'I love a good insult, even one directed at me.',
    "I get bitter if I'm not the center of attention.",
    "I'll settle for nothing less than perfection.",
    'I change my mood or my mind as quickly as I change key in a song.',
    'I judge people by their actions, not their words.',
    "If someone is in trouble, I'm always willing to lend help.",
    'When I set my mind to something, I follow through no matter what gets in my way.',
    'I have a strong sense of fair play and always try to find the most equitable solution to arguments.',
    "I'm confident in my own abilities and do what I can to instill confidence in others.",
    'Thinking is for other people. I prefer action.',
    'I misuse long words in an attempt to sound smarter.',
    'I get bored easily. When am I going to get on with my destiny.',
    "I believe that everything worth doing is worth doing right. I can't help it--I'm a perfectionist.",
    "I'm a snob who looks down on those who can't appreciate fine art.",
    'I always want to know how things work and what makes people tick.',
    "I'm full of witty aphorisms and have a proverb for every occasion.",
    "I'm rude to people who lack my commitment to hard work and fair play.",
    'I like to talk at length about my profession.',
    "I don't part with my money easily and will haggle tirelessly to get the best deal possible.",
    "I'm well known for my work, and I want to make sure everyone appreciates it. I'm always taken aback when people haven't heard of me.",
    "I've been isolated for so long that I rarely speak, preferring gestures and the occasional grunt.",
    'I am utterly serene, even in the face of disaster.',
    'The leader of my community has something wise to say on every topic, and I am eager to share that wisdom.',
    'I feel tremendous empathy for all who suffer.',
    "I'm oblivious to etiquette and social expectations.",
    'I connect everything that happens to me to a grand cosmic plan.',
    'I often get lost in my own thoughts and contemplations, becoming oblivious to my surroundings.',
    'I am working on a grand philosophical theory and love sharing my ideas.',
    'My eloquent flattery makes everyone I talk to feel like the most wonderful and important person in the world.',
    'The common folk love me for my kindness and generosity.',
    'No one could doubt by looking at my regal bearing that I am a cut above the unwashed masses.',
    'I take great pains to always look my best and follow the latest fashions.',
    "I don't like to get my hands dirty, and I won't be caught dead in unsuitable accommodations.",
    'Despite my birth, I do not place myself above other folk. We all have the same blood.',
    'My favor, once lost, is lost forever.',
    'If you do me an injury, I will crush you, ruin your name, and salt your fields.',
    "I'm driven by a wanderlust that led me away from home.",
    'I watch over my friends as if they were a litter of newborn pups.',
    "I once ran twenty-five miles without stopping to warn my clan of an approaching orc horde. I'd do it again if I had to.",
    'I have a lesson for every situation, drawn from observing nature.',
    "I place no stock in wealthy or well-mannered folk. Money and manners won't save you from a hungry owlbear.",
    "I'm always picking things up, absently fiddling with them, and sometimes accidentally breaking them.",
    'I feel far more comfortable around animals than people.',
    'I was, in fact, raised by wolves.',
    'I use polysyllabic words to convey the impression of great erudition.',
    "I've read every book in the world's greatest libraries--or like to boast that I have.",
    "I'm used to helping out those who aren't as smart as I am, and I patiently explain anything and everything to others.",
    "There's nothing I like more than a good mystery.",
    "I'm willing to listen to every side of an argument before I make my own judgment.",
    'I...speak...slowly...when talking...to idiots...which...almost...everyone...is...compared ...to me.',
    'I am horribly, horribly awkward in social situations.',
    "I'm convinced that people are always trying to steal my secrets.",
    'My friends know they can rely on me, no matter what.',
    'I work hard so that I can play hard when the work is done.',
    'I enjoy sailing into new ports and making new friends over a flagon of ale.',
    'I stretch the truth for the sake of a good story.',
    'To me, a tavern brawl is a nice way to get to know a new city.',
    'I never pass up a friendly wager.',
    'My language is as foul as an otyugh nest.',
    'I like a job well done, especially if I can convince someone else to do it.',
    "I'm always polite and respectful.",
    "I'm haunted by memories of war. I can't get the images of violence out of my mind.",
    "I've lost too many friends, and I'm slow to make new ones.",
    "I'm full of inspiring and cautionary tales from my military experience relevant to almost every combat situation.",
    'I can stare down a hellhound without flinching.',
    'I enjoy being strong and like breaking things.',
    'I have a crude sense of humor.',
    'I face problems head-on. A simple direct solution is the best path to success.',
    'I hide scraps of food and trinkets away in my pockets.',
    'I ask a lot of questions.',
    'I like to squeeze into small places where no one else can get to me.',
    'I sleep with my back to a wall or tree, with everything I own wrapped in a bundle in my arms.',
    'I eat like a pig and have bad manners.',
    "I think anyone who's nice to me is hiding evil intent.",
    "I don't like to bathe.",
    'I bluntly say what other people are hinting or hiding.',
]

FLAWS = [
    'I judge others harshly, and myself even more severely.',
    "I put too much trust in those who wield power within my temple's hierarchy.",
    'My piety sometimes leads me to blindly trust those that profess faith in my god.',
    'I am inflexible in my thinking.',
    'I am suspicious of strangers and suspect the worst of them.',
    'Once I pick a goal, I become obsessed with it to the detriment of everything else in my life.',
    "I can't resist a pretty face.",
    "I'm always in debt. I spend my ill-gotten gains on decadent luxuries faster than I bring them in.",
    "I'm convinced that no one could ever fool me in the way I fool others.",
    "I'm too greedy for my own good. I can't resist taking a risk if there's money involved.",
    "I can't resist swindling people who are more powerful than me.",
    "I hate to admit it and will hate myself for it, but I'll run and preserve my own hide if the going gets tough.",
    "When I see something valuable, I can't think about anything but how to steal it.",
    'When faced with a choice between money and my friends, I usually choose the money.',
    "If there's a plan, I'll forget it. If I don't forget it, I'll ignore it.",
    "I have a 'tell' that reveals when I'm lying.",
    'I turn tail and run when things go bad.',
    "An innocent person is in prison for a crime that I committed. I'm okay with that.",
    "I'll do anything to win fame and renown.",
    "I'm a sucker for a pretty face.",
    'A scandal prevents me from ever going home again. That kind of trouble seems to follow me around.',
    'I once satirized a noble who still wants my head. It was a mistake that I will likely repeat.',
    'I have trouble keeping my true feelings hidden. My sharp tongue lands me in trouble.',
    'Despite my best efforts, I am unreliable to my friends.',
    'The tyrant who rules my land will stop at nothing to see me killed.',
    "I'm convinced of the significance of my destiny, and blind to my shortcomings and the risk of failure.",
    'The people who knew me when I was young know my shameful secret, so I can never go home again.',
    'I have a weakness for the vices of the city, especially hard drink.',
    'Secretly, I believe that things would be better if I were a tyrant lording over the land.',
    'I have trouble trusting in my allies.',
    "I'll do anything to get my hands on something rare or priceless.",
    "I'm quick to assume that someone is trying to cheat me.",
    'No one must ever learn that I once stole money from guild coffers.',
    "I'm never satisfied with what I have--I always want more.",
    'I would kill to acquire a noble title.',
    "I'm horribly jealous of anyone who outshines my handiwork. Everywhere I go, I'm surrounded by rivals.",
    "Now that I've returned to the world, I enjoy its delights a little too much.",
    'I harbor dark bloodthirsty thoughts that my isolation failed to quell.',
    'I am dogmatic in my thoughts and philosophy.',
    'I let my need to win arguments overshadow friendships and harmony.',
    "I'd risk too much to uncover a lost bit of knowledge.",
    "I like keeping secrets and won't share them with anyone.",
    'I secretly believe that everyone is beneath me.',
    'I hide a truly scandalous secret that could ruin my family forever.',
    "I too often hear veiled insults and threats in every word addressed to me, and I'm quick to anger.",
    'I have an insatiable desire for carnal pleasures.',
    'In fact, the world does revolve around me.',
    'By my words and actions, I often bring shame to my family.',
    'I am too enamored of ale, wine, and other intoxicants.',
    "There's no room for caution in a life lived to the fullest.",
    "I remember every insult I've received and nurse a silent resentment toward anyone who's ever wronged me.",
    'I am slow to trust members of other races',
    'Violence is my answer to almost any challenge.',
    "Don't expect me to save those who can't save themselves. It is nature's way that the strong thrive and the weak perish.",
    'I am easily distracted by the promise of information.',
    'Most people scream and run when they see a demon. I stop and take notes on its anatomy.',
    'Unlocking an ancient mystery is worth the price of a civilization.',
    'I overlook obvious solutions in favor of complicated ones.',
    'I speak without really thinking through my words, invariably insulting others.',
    "I can't keep a secret to save my life, or anyone else's.",
    "I follow orders, even if I think they're wrong.",
    "I'll say anything to avoid having to do extra work.",
    'Once someone questions my courage, I never back down no matter how dangerous the situation.',
    "Once I start drinking, it's hard for me to stop.",
    "I can't help but pocket loose coins and other trinkets I come across.",
    'My pride will probably lead to my destruction',
    'The monstrous enemy we faced in battle still leaves me quivering with fear.',
    'I have little respect for anyone who is not a proven warrior.',
    'I made a terrible mistake in battle that cost many lives--and I would do anything to keep that mistake secret.',
    'My hatred of my enemies is blind and unreasoning.',
    'I obey the law, even if the law causes misery.',
    "I'd rather eat my armor than admit when I'm wrong.",
    "If I'm outnumbered, I always run away from a fight.",
    "Gold seems like a lot of money to me, and I'll do just about anything for more of it.",
    'I will never fully trust anyone other than myself.',
    "I'd rather kill someone in their sleep than fight fair.",
    "It's not stealing if I need it more than someone else.",
    "People who don't take care of themselves get what they deserve.",
]


def main_simulate():
    parser = argparse.ArgumentParser()
    parser.add_argument('players_yml')
    parser.add_argument('encounter_yml')
    parser.add_argument('--count', '-c', type=int, default=100)
    args = parser.parse_args()
    enc = TestEncounter(args.players_yml, args.encounter_yml)
    enc.run_many(args.count)


def main_npc():
    parser = argparse.ArgumentParser()
    parser.add_argument('--class', '-c', dest='klass')
    parser.add_argument('--race', '-r', choices=('human', 'dwarf', 'elf',
                                                 'half-elf', 'half-orc',
                                                 'gnome', 'halfling',
                                                 'tiefling', 'dragonborn'))
    parser.add_argument('--subrace', '-s')
    parser.add_argument('--gender', '-g', choices=('male', 'female'))
    parser.add_argument('--name', '-n')
    parser.add_argument('--alignment', '-a')
    args = parser.parse_args()

    npc = NPC(klass=args.klass, race=args.race, gender=args.gender,
              name=args.name, subrace=args.subrace, alignment=args.alignment)
    npc.output()


def main_roll():
    import sys
    s = ' '.join(sys.argv[1:])
    r = roll(s)
    print(r)
