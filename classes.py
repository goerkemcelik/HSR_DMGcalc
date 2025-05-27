class Character:
    def __init__(self, name, base_stat, trace, attack, talent=None):
        self.name = name
        self.base_stat = base_stat
        self.trace = trace
        self.attack = attack
        self.talents = talent or []

class Lightcone:
    def __init__(self, name, base_stat):
        self.name = name
        self.base_stat = base_stat

class Stat:
    def __init__(self, hp, atk, def_, crit_rate, crit_dmg, spd, e_dmg, energy):
        self.hp = hp
        self.atk = atk
        self.def_ = def_
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.spd = spd
        self.e_dmg = e_dmg
        self.energy = energy

class Trace:
    def __init__(self, stat, boost_type, value):
        self.stat = stat
        self.boost_type = boost_type
        self.value = value

class Attack:
    def __init__(self, name, multiplier, scaling_stat, target_type, blast_multiplier, boost=None):
        self.name = name
        self.multiplier = multiplier
        self.scaling_stat = scaling_stat
        self.target_type = target_type
        self.blast_multiplier = blast_multiplier
        self.boost = boost or []

class Talent:
    def __init__(self, stat, boost_type, value, condition):
        self.stat = stat
        self.boost_type = boost_type
        self.value = value
        self.condition = condition  # "ally_ability_target", "during_ultimate", etc.
