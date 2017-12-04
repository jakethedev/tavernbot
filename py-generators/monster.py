import os
import sys
import json
import random
import argparse
from itertools import product
from fuzzywuzzy import fuzz


ROOT = os.path.dirname(__file__)
DATADIR = os.path.join(ROOT, 'data')
MONSTERS_PATH = os.path.join(DATADIR, 'monsters.json')
TAGS_PATH = os.path.join(DATADIR, 'tags.json')
TAG_GROUPS_PATH = os.path.join(DATADIR, 'tag_groups.json')
TYPE_GROUPS_PATH = os.path.join(DATADIR, 'type_groups.json')
SUBTYPE_GROUPS_PATH = os.path.join(DATADIR, 'subtype_groups.json')
RELATED_PATH = os.path.join(DATADIR, 'related.json')

# Easy, Medium, Hard, Deadly
XP_THRESH = [
    (0, 0, 0, 0),
    # 1st
    (25, 50, 75, 100),
    (50, 100, 150, 200),
    (75, 150, 225, 400),
    (125, 250, 375, 500),
    # 5th
    (250, 500, 750, 1100),
    (300, 600, 900, 1400),
    (350, 750, 1100, 1700),
    (450, 900, 1400, 2100),
    (550, 1100, 1600, 2400),
    # 10th
    (600, 1200, 1900, 2800),
    (800, 1600, 2400, 3600),
    (1000, 2000, 3000, 4500),
    (1100, 2200, 3400, 5100),
    (1250, 2500, 3800, 5700),
    # 15th
    (1400, 2800, 4300, 6400),
    (1600, 3200, 4800, 7200),
    (2000, 3900, 5900, 8800),
    (2100, 4200, 6300, 9500),
    (2400, 4900, 7300, 10900),
    # 20th!
    (2800, 5700, 8500, 12700),
]

CRS = {
    50: 'CR-1/4',
    100: 'CR-1/2',
    200: 'CR-1',
    450: 'CR-2',
    700: 'CR-3',
    1100: 'CR-4',
    1800: 'CR-5',
    2300: 'CR-6',
    2900: 'CR-7',
    3900: 'CR-8',
    5000: 'CR-9',
    5900: 'CR-10',
    7200: 'CR-11',
    8400: 'CR-12',
}


def scale_enc(num):
    if num == 0:
        return 0.0
    if num == 1:
        return 1.0
    if num == 2:
        return 1.5
    if 3 <= num <= 6:
        return 2.0
    if 7 <= num <= 10:
        return 2.5
    if 11 <= num <= 14:
        return 3.0
    return 4.0


def csv_set(s):
    if not s:
        return None
    if isinstance(s, (list, tuple, set)):
        return set(s)
    if isinstance(s, str):
        return {x.strip().lower() for x in s.split(',')}
    raise ValueError('bad type for splitting on comma: {!r}'.format(s))


class Monster:
    MONSTERS = []
    TAG_GROUPS = {}
    TYPE_GROUPS = {}
    SUBTYPE_GROUPS = {}
    MONSTER_GROUPS = {}
    MONSTER_DATA = []
    MONSTER_D = {}
    TAGS = set()

    def __repr__(self):
        return self.data['name']

    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        if attr in self.data:
            val = self.data[attr]
        else:
            raise AttributeError('{!r} has no {!r}'.format(self, attr))
        if isinstance(val, str):
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except:
                return val
        return val

    def __sub__(self, mon):
        if not isinstance(mon, Monster):
            raise ValueError('cant calculate the difference between anything '
                             'except other monsters')
        s = 0.0
        if self.name == mon.name:
            return 999999
        if self.type != mon.type and not (self.tags & mon.tags):
            return 0.0
        langs = {x for x in self.tags if x.endswith('_lang')}
        mlangs = {x for x in mon.tags if x.endswith('_lang')}
        tags = self.tags - langs
        mtags = mon.tags - mlangs
        s += 2 * len(langs & mlangs)
        areas = {'plains', 'desert', 'mountain', 'swamp', 'forest', 'jungle',
                 'tundra'}
        if tags & mtags & areas:
            s += 1
        for t in {'insect', 'arachnid', 'reptile', 'cave', 'city', 'sea',
                  'fresh', 'fish'}:
            if tags & {t} and mtags & {t}:
                s *= 2
        for t in {'underdark', 'fire', 'ice', 'lightning', 'water', 'earth',
                  'air', 'water', 'hell', 'fly', 'swim', 'were'}:
            if tags & {t} and mtags & {t}:
                s *= 3
        align = {'good', 'evil'}
        if len(align & tags) == 1 and len(align & mtags) == 1:
            if align & tags & mtags:
                s *= 7
            else:
                s /= 7
        if self.type == mon.type:
            if self.subtype and self.subtype == mon.subtype:
                s *= 8
            else:
                s *= 3
        for bad in {'were', 'dragon', 'reptile', 'arachnid', 'insect'}:
            if bad not in tags | mtags:
                continue
            if {bad} & tags & mtags != {bad}:
                s /= 5
            else:
                s *= 5
        return s

    @property
    def tags(self):
        if 'tags' not in self.data:
            return set()
        return set(self.data['tags']) | {self.name.strip().lower()}

    @classmethod
    def load(cls):
        with open(MONSTERS_PATH) as f:
            cls.MONSTER_DATA = json.load(f)
        cls.MONSTERS = [cls(x) for x in cls.MONSTER_DATA]
        cls.MONSTER_D = {m.name.lower().strip(): m for m in cls.MONSTERS}

        with open(TAGS_PATH) as f:
            cls.TAGS = set(json.load(f))

        with open(TAG_GROUPS_PATH) as f:
            tag_groups = json.load(f)
        cls.TAG_GROUPS = {}
        for tag, mon_names in tag_groups.items():
            mons = [cls.get(name) for name in mon_names]
            cls.TAG_GROUPS[tag] = mons

        with open(TYPE_GROUPS_PATH) as f:
            type_groups = json.load(f)
        cls.TYPE_GROUPS = {}
        for typ, mon_names in type_groups.items():
            mons = [cls.get(name) for name in mon_names]
            cls.TYPE_GROUPS[typ] = mons

        with open(SUBTYPE_GROUPS_PATH) as f:
            subtype_groups = json.load(f)
        cls.SUBTYPE_GROUPS = {}
        for typ, d in subtype_groups.items():
            for subtyp, mon_names in d.items():
                if subtyp == 'null':
                    key = (typ, None)
                else:
                    key = (typ, subtyp)
                mons = [cls.get(name) for name in mon_names]
                cls.SUBTYPE_GROUPS[key] = mons

        with open(RELATED_PATH) as f:
            related = json.load(f)
        cls.MONSTER_GROUPS = {}
        for name, mon_names in related.items():
            mons = [cls.get(mname) for mname in mon_names]
            cls.MONSTER_GROUPS[cls.get(name)] = mons

    @classmethod
    def get(cls, name):
        mon = cls.MONSTER_D.get(name.strip().lower())
        if mon:
            return mon
        mons = []
        for mon in cls.MONSTERS:
            ratio = fuzz.ratio(mon.name.lower().strip(), name)
            mons.append((ratio, mon))
        mons = [b for a, b in sorted(mons, key=lambda x: x[0], reverse=True)]
        return mons[0]

    def related(self):
        return Monster.MONSTER_GROUPS[self]

    @staticmethod
    def select_and(grp1, grp2):
        return [x for x in grp1 if x in grp2]

    @staticmethod
    def select_or(grp1, grp2):
        g1 = [x for x in grp1 if x not in grp2]
        g2 = [x for x in grp2 if x not in grp1]
        return g1 + g2

    @classmethod
    def random_encounter(cls, min_xp, max_xp, or_tags=None, and_tags=None,
                         not_tags=None, max_num=10):
        mons = cls.find(or_tags=or_tags, and_tags=and_tags, not_tags=not_tags)
        if not mons:
            raise ValueError('filters too restrictive! no monsters found')
        mons = [x for x in mons if x.xp <= max_xp]
        if not mons:
            raise ValueError('none of these monsters are <= max xp threshold')
        print('found {} possible monsters'.format(len(mons)))

        mon = random.choice(mons)
        mons = cls.select_and(mon.related(), mons)[:6]

        def total_xp(enc):
            xp = 0
            c = 0
            for ct, mon in enc:
                xp += ct * mon.xp
                c += ct
            xp *= scale_enc(c)
            return xp

        print('trying to build with types: {}'
              .format(', '.join([x.name for x in mons])))

        poss = []
        amounts = []
        for _ in mons:
            # maximum of 10 of each monster
            amounts.append(range(max_num))
        print('iterating through {} possible encounter permutations...'.format(
            max_num**len(mons)))

        for cts in product(*amounts):
            if len([x for x in cts if x > 0]) > 4:
                continue
            enc = []
            for i, ct in enumerate(cts):
                if ct == 0:
                    continue
                mon = mons[i]
                enc.append((ct, mon))
            if min_xp <= total_xp(enc) <= max_xp:
                poss.append(enc)

        print('{} of those match allowed XP values'.format(len(poss)))
        if not poss:
            raise ValueError('no possible permutations amount to allowed XP!')
        enc = random.choice(poss)
        return enc, total_xp(enc)

    @classmethod
    def cr_encounters(cls, min_xp, max_xp, max_num=10):
        def total_xp(enc):
            xp = 0
            c = 0
            for ct, mon in enc:
                xp += ct * mon[1]
                c += ct
            xp *= scale_enc(c)
            return xp
        mons = []
        for k, v in CRS.items():
            if k > max_xp:
                continue
            if k < min_xp / 20:
                continue
            mon = (v, k)
            mons.append(mon)
        amounts = []
        for _ in mons:
            amounts.append(range(max_num))
        poss = []
        for cts in product(*amounts):
            if len([x for x in cts if x > 0]) > 3:
                continue
            enc = []
            for i, ct in enumerate(cts):
                if ct == 0:
                    continue
                mon = mons[i]
                enc.append((ct, mon))
            if min_xp <= total_xp(enc) <= max_xp:
                poss.append((enc, total_xp(enc)))
        def summ(enc):
            return sum([e[0] for e in enc])
        return sorted(poss, key=lambda x: (x[1], summ(x[0])))

    @classmethod
    def custom_random_encounter(cls, monsters, min_xp, max_xp, max_num=10):
        mons = []
        for mon in monsters:
            if isinstance(mon, str):
                if '=' in mon:
                    name, xp = mon.split('=')
                    xp = int(xp)
                    mons.append((name, xp))
                else:
                    mon1 = Monster.get(mon)
                    if mon1 is None:
                        raise ValueError(
                            'couldnt find monster from {!r}'.format(mon)
                        )
                    mons.append((mon1.name, mon1.xp))
            elif isinstance(mon, tuple):
                if len(mon) != 2:
                    raise ValueError('got tuple {!r}, shouldve been (name, xp)'
                                     .format(mon))
                if isinstance(mon[1], int):
                    mons.append(mon)
                else:
                    mons.append((mon[0], int(mon[1])))

        def total_xp(enc):
            xp = 0
            c = 0
            for ct, name, _xp in enc:
                xp += ct * _xp
                c += ct
            xp *= scale_enc(c)
            return xp

        poss = []
        amounts = []
        for _ in mons:
            # maximum of 10 of each monster
            amounts.append(range(max_num))
        print('iterating through {} possible encounter permutations...'.format(
            max_num**len(mons)))

        for cts in product(*amounts):
            enc = []
            for i, ct in enumerate(cts):
                if ct == 0:
                    continue
                mon = mons[i]
                enc.append((ct, mon[0], mon[1]))
            if min_xp <= total_xp(enc) <= max_xp:
                poss.append(enc)

        print('{} of those match allowed XP values'.format(len(poss)))
        if not poss:
            raise ValueError('no possible permutations amount to allowed XP!')
        enc = random.choice(poss)
        return enc, total_xp(enc)

    @classmethod
    def find(cls, or_tags=None, and_tags=None, not_tags=None):
        or_tags = csv_set(or_tags)
        and_tags = csv_set(and_tags)
        not_tags = csv_set(not_tags)
        mons = cls.MONSTERS[:]
        if or_tags is not None:
            mons = [x for x in mons if x.tags & or_tags]
        if and_tags is not None:
            mons = [x for x in mons if x.tags & and_tags == and_tags]
        if not_tags is not None:
            mons = [x for x in mons if not bool(x.tags & not_tags)]
        return mons

    def short_output(self):
        print('{} ({}{}) CR:{} XP:{}'.format(
            self.name, self.type, ' ' + self.subtype if self.subtype else '',
            self.challenge_rating, self.xp))
        print('AC:{} HP:{} ({})'.format(self.armor_class, self.hit_points,
                                        self.hit_dice))
        print('S:{} D:{} C:{} I:{} W:{} CH:{}'.format(
            self.strength, self.dexterity, self.constitution, self.intelligence,
            self.wisdom, self.charisma))
        print('Size: {}'.format(self.size))
        print('Speed: {}'.format(self.speed))
        print('Senses: {}'.format(self.senses))
        if self.damage_immunities:
            print('Immune: {}'.format(self.damage_immunities))
        if self.condition_immunities:
            print('Cond.Immune: {}'.format(self.condition_immunities))
        if self.damage_resistances:
            print('Resist: {}'.format(self.damage_resistances))
        if self.damage_vulnerabilities:
            print('Vulnerable: {}'.format(self.damage_vulnerabilities))
        if self.languages:
            print('Langs: {}'.format(self.languages))
        if 'actions' in self.data:
            for act in self.actions:
                print('Action "{act[name]}": {act[desc]}'.format(act=act))
        if 'special_abilities' in self.data:
            for abi in self.special_abilities:
                print('Ability "{abi[name]}": {abi[desc]}'.format(abi=abi))

    def output(self):
        print(self.name)
        for x in (
            'name',
            'challenge rating',
            'xp',
            'type',
            'subtype',
            'alignment',
            'size',
            'hit points',
            'hit dice',
            'armor class',
            'speed',
            'senses',
            'languages'
            'damage immunities',
            'damage resistances',
            'damage vulnerabilities',
            'condition immunities',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
        ):
            if x not in self.data:
                continue
            print('{}: {}'.format(x.title(), self.data[x]))
        print('Tags: {}'.format(', '.join(self.tags)))
        if self.subtype:
            print('Same Subtype: {}'.format(', '.join([
                x.name for x in self.same_subtype()
            ])))
        print('Same Type: {}'.format(', '.join([
            x.name for x in self.same_type()
        ])))
        print('Related: {}'.format(', '.join([
            x.name for x in self.related()[:10]
        ])))
        if 'actions' in self.data:
            print('\nActions:')
            for act in self.actions:
                print('  ' + act['name'])
                print('    ' + act['desc'])
        if 'special_abilities' in self.data:
            print('\nSpecial Abilities:')
            for act in self.special_abilities:
                print('  ' + act['name'])
                print('    ' + act['desc'])

    def same_type(self):
        return self.TYPE_GROUPS[self.type]

    def same_subtype(self):
        return self.SUBTYPE_GROUPS[(self.type, self.subtype or None)]


def calc_threshold(player_levels):
    thresh = [0, 0, 0, 0, 0]
    for lvl in player_levels:
        for i in range(4):
            thresh[i] += XP_THRESH[lvl][i]
    # make deadly span between itself and a new number, 1.5 times diff between
    # the hard and deadly difficulty difference
    d = thresh[3] - thresh[2]
    thresh[4] = int(thresh[3] + (1.5 * d))
    return thresh


def main_monster():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='select a monster by name')
    parser.add_argument('--short', '-s', action='store_true',
                        help='print short stats')
    args = parser.parse_args()
    Monster.load()
    mon = Monster.get(args.name)
    if not mon:
        sys.exit('cant find this monster')
    if args.short:
        mon.short_output()
    else:
        mon.output()


def main_encounter():
    p = argparse.ArgumentParser()
    p.add_argument('--players', '-p', help='the player levels, default 1,1,1,1')
    p.add_argument('--difficulty', '-d', default='medium',
                   choices=('easy', 'medium', 'hard', 'deadly'))
    p.add_argument('--and', '-A', dest='and_tags',
                   help='require monsters have all of these, '
                   'eg: underdark,undercommon_lang')
    p.add_argument('--or', '-O', dest='or_tags',
                   help='only include monsters with one or more, eg: '
                   'dragon,reptile')
    p.add_argument('--not', '-N', dest='not_tags',
                   help='exclude monsters with one of these, eg: undead,fire')
    p.add_argument('--custom', '-c',
                   help='specify custom set of monsters with name=xp notation,'
                   ' eg. elfmage=500,treeperson=1500,goblin,goblinmage=200')
    p.add_argument('--max-num', '-m', type=int, default=10,
                   help='for custom encounters, the maximum number of one type,'
                   'eg. "--max-num 5" if you only want up to 5 of each type, '
                   'default: %(default)s')
    args = p.parse_args()
    Monster.load()
    if args.players:
        players = [int(x.strip()) for x in args.players.split(',')]
    else:
        players = [1, 1, 1, 1]
    thresh = calc_threshold(players)
    diff = {'easy': 0, 'medium': 1, 'hard': 2, 'deadly': 3}[args.difficulty]
    thresh = (thresh[diff], thresh[diff + 1])
    if not args.custom:
        try:
            enc, xp = Monster.random_encounter(
                thresh[0],
                thresh[1],
                or_tags=args.or_tags,
                and_tags=args.and_tags,
                not_tags=args.not_tags,
            )
        except ValueError as e:
            sys.exit(str(e))
        print('XP={} ({} <= xp <= {}):'.format(xp, *thresh))
        for ct, mon in enc:
            print(' - {} {!r}'.format(ct, mon))
        print('')
        for ct, mon in enc:
            mon.short_output()
            print('')
    else:
        mons = [x.strip() for x in args.custom.split(',') if x.strip()]
        try:
            enc, xp = Monster.custom_random_encounter(
                mons, thresh[0], thresh[1], max_num=args.max_num,
            )
        except ValueError as e:
            sys.exit(str(e))
        print('XP={} ({} <= xp <= {}):'.format(xp, *thresh))
        for ct, name, mon_xp in enc:
            print(' - {} {} (xp={})'.format(ct, name, mon_xp))


def main_threshold():
    p = argparse.ArgumentParser()
    p.add_argument('--players', '-p', help='the player levels, default 1,1,1,1')
    args = p.parse_args()
    if args.players:
        players = [int(x.strip()) for x in args.players.split(',')]
    else:
        players = [1, 1, 1, 1]
    thresh = calc_threshold(players)
    print('Easy: {} to {}'.format(thresh[0], thresh[1] - 1))
    print('Medium: {} to {}'.format(thresh[1], thresh[2] - 1))
    print('Hard: {} to {}'.format(thresh[2], thresh[3] - 1))
    print('Deadly: {}+'.format(thresh[3]))


def main_summary():
    p = argparse.ArgumentParser()
    p.add_argument('--players', '-p', help='the player levels, default 1,1,1,1')
    p.add_argument('--difficulty', '-d', default='medium',
                   choices=('easy', 'medium', 'hard', 'deadly'))
    p.add_argument('--max-num', '-m', type=int, default=10,
                   help='for custom encounters, the maximum number of one type,'
                   'eg. "--max-num 5" if you only want up to 5 of each type, '
                   'default: %(default)s')
    args = p.parse_args()
    if args.players:
        players = [int(x.strip()) for x in args.players.split(',')]
    else:
        players = [1, 1, 1, 1]
    diff = {'easy': 0, 'medium': 1, 'hard': 2, 'deadly': 3}[args.difficulty]
    thresh = calc_threshold(players)
    encs = Monster.cr_encounters(thresh[diff], thresh[diff + 1] - 1,
                                 max_num=args.max_num)
    print('XP {} to {}'.format(thresh[diff], thresh[diff + 1] - 1))
    for enc, xp in encs:
        print('XP: {}'.format(xp))
        for ct, mon in enc:
            print(' - {} {} ({})'.format(ct, mon[0], mon[1]))
        print('')
