from classes import Character, Lightcone, Stat, Trace, Attack

def calculate_pre_combat_stats(character, lightcone):
    # Combined Base Stats
    combined_base_stat = Stat(
        hp = character.base_stat.hp + lightcone.base_stat.hp,
        atk = character.base_stat.atk + lightcone.base_stat.atk,
        def_ = character.base_stat.def_ + lightcone.base_stat.def_,
        spd = character.base_stat.spd + lightcone.base_stat.spd,
        crit_rate = character.base_stat.crit_rate + lightcone.base_stat.crit_rate,
        crit_dmg = character.base_stat.crit_dmg + lightcone.base_stat.crit_dmg,
        e_dmg = character.base_stat.e_dmg + lightcone.base_stat.e_dmg,
        energy = character.base_stat.energy
    )

    # Boosts
    percentage_boost = Stat(**{k: 0 for k in ['hp', 'atk', 'def_', 'spd', 'crit_rate', 'crit_dmg', 'e_dmg', 'energy']})
    flat_boost = Stat(**{k: 0 for k in ['hp', 'atk', 'def_', 'spd', 'crit_rate', 'crit_dmg', 'e_dmg', 'energy']})

    # Traces (update the json files after adding stuff!)
    for trace in character.trace:
        if trace.boost_type == "percentage":
            if trace.stat == "hp":
                percentage_boost.hp += trace.value
            elif trace.stat == "atk":
                percentage_boost.atk += trace.value
            elif trace.stat == "def_":
                percentage_boost.def_ += trace.value
            elif trace.stat == "crit_rate":
                percentage_boost.crit_rate += trace.value
            elif trace.stat == "crit_dmg":
                percentage_boost.crit_dmg += trace.value
            elif trace.stat == "e_dmg":
                percentage_boost.e_dmg += trace.value
        elif trace.boost_type == "flat":
            if trace.stat == "spd":
                flat_boost.spd += trace.value

    # Relics - to be added later

    # Pre-Combat Stats
    pre_combat_stat = Stat(
        hp = combined_base_stat.hp * (1 + percentage_boost.hp) + flat_boost.hp,
        atk = combined_base_stat.atk * (1 + percentage_boost.atk) + flat_boost.atk,
        def_ = combined_base_stat.def_ * (1 + percentage_boost.def_) + flat_boost.def_,
        spd = combined_base_stat.spd + flat_boost.spd,
        crit_rate = combined_base_stat.crit_rate + percentage_boost.crit_rate,
        crit_dmg = combined_base_stat.crit_dmg + percentage_boost.crit_dmg,
        e_dmg = combined_base_stat.e_dmg + percentage_boost.e_dmg,
        energy = combined_base_stat.energy
    )

    return pre_combat_stat, combined_base_stat, percentage_boost, flat_boost

def get_scaling_value(attack_stat, scaling_stat_name):
    if scaling_stat_name == "atk":
        return attack_stat.atk
    elif scaling_stat_name == "hp":
        return attack_stat.hp
    elif scaling_stat_name == "def_":
        return attack_stat.def_
    else:
        raise ValueError(f"Unsupported scaling stat: {scaling_stat_name}")

def handle_target_type(base_damage, attack):
    if attack.target_type == "single":
        return {
            "Single Target": base_damage
        }

    elif attack.target_type == "blast":
        return {
            "Main Target": base_damage,
            "Adjacent Targets": base_damage * attack.blast_multiplier,
        }

    elif attack.target_type == "aoe":
        return {
            "All Targets": base_damage
        }

    else:
        raise ValueError(f"Unknown target type: {attack.target_type}")
    
def calculate_basic_attack(base_stat, attack_stat, attack):
    base_damage = base_stat * attack.multiplier * \
                  (1 + attack_stat.crit_rate * attack_stat.crit_dmg) * \
                  (1 + attack_stat.e_dmg)
    return handle_target_type(base_damage, attack)

def calculate_skill(base_stat, attack_stat, attack):
    base_damage = base_stat * attack.multiplier * \
                  (1 + attack_stat.crit_rate * attack_stat.crit_dmg) * \
                  (1 + attack_stat.e_dmg)
    return handle_target_type(base_damage, attack)

def calculate_ultimate(base_stat, attack_stat, attack):
    base_damage = base_stat * attack.multiplier * \
                  (1 + attack_stat.crit_rate * attack_stat.crit_dmg) * \
                  (1 + attack_stat.e_dmg)
    return handle_target_type(base_damage, attack)

attack_dispatcher = {
    "Basic Attack": calculate_basic_attack,
    "Skill": calculate_skill,
    "Ultimate": calculate_ultimate,
    "Enhanced Basic Attack": calculate_basic_attack,
    "Enhanced Skill": calculate_basic_attack,
    "Counter": calculate_basic_attack
}

def calculate_expected_damage(
        combined_base_stat,
        percentage_boost,
        flat_boost,
        attack: Attack
    ):
    
    attack_percentage_boost = Stat(**percentage_boost.__dict__)
    attack_flat_boost = Stat(**flat_boost.__dict__)

    for boost in attack.boost:
        if boost["boost_type"] == "percentage":
            if boost["stat"] == "hp":
                attack_percentage_boost.hp += boost["value"]
            elif boost["stat"] == "atk":
                attack_percentage_boost.atk += boost["value"]
            elif boost["stat"] == "def_":
                attack_percentage_boost.def_ += boost["value"]
            elif boost["stat"] == "crit_rate":
                attack_percentage_boost.crit_rate += boost["value"]
            elif boost["stat"] == "crit_dmg":
                attack_percentage_boost.crit_dmg += boost["value"]
            elif boost["stat"] == "e_dmg":
                attack_percentage_boost.e_dmg += boost["value"]
        elif boost["boost_type"] == "flat":
            if boost["stat"] == "hp":
                attack_flat_boost.hp += boost["value"]
            elif boost["stat"] == "atk":
                attack_flat_boost.atk += boost["value"]
            elif boost["stat"] == "def_":
                attack_flat_boost.def_ += boost["value"]
            elif boost["stat"] == "spd":
                attack_flat_boost.spd += boost["value"]

    # Attack-Specific Stats
    attack_stat = Stat(
        hp = combined_base_stat.hp * (1 + attack_percentage_boost.hp) + attack_flat_boost.hp,
        atk = combined_base_stat.atk * (1 + attack_percentage_boost.atk) + attack_flat_boost.atk,
        def_ = combined_base_stat.def_ * (1 + attack_percentage_boost.def_) + attack_flat_boost.def_,
        spd = combined_base_stat.spd + attack_flat_boost.spd,
        crit_rate = combined_base_stat.crit_rate + attack_percentage_boost.crit_rate,
        crit_dmg = combined_base_stat.crit_dmg + attack_percentage_boost.crit_dmg,
        e_dmg = combined_base_stat.e_dmg + attack_percentage_boost.e_dmg,
        energy = combined_base_stat.energy
    )
    
    base_stat = attack_stat.atk if attack.scaling_stat == "atk" else attack_stat.hp
    
    calculator = attack_dispatcher.get(attack.name, calculate_basic_attack)

    return calculator(base_stat, attack_stat, attack)
