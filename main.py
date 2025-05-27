import json
from classes import Character, Lightcone, Stat, Trace, Attack, Talent
from calculation import calculate_pre_combat_stats, calculate_expected_damage

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def parse_character(data):
    base_stat = Stat(
        hp = data["base_stat"]["hp"],
        atk = data["base_stat"]["atk"],
        def_ = data["base_stat"]["def_"],
        spd = data["base_stat"]["spd"],
        crit_rate = data["base_stat"]["crit_rate"],
        crit_dmg = data["base_stat"]["crit_dmg"],
        e_dmg = data["base_stat"]["e_dmg"],
        energy = data["base_stat"]["energy"]
    )
    trace = [
        Trace(
            t["stat"],
            t["boost_type"],
            t["value"]
        ) for t in data["trace"]
    ]
    attack = [
        Attack(
            a["name"],
            a["multiplier"],
            a["scaling_stat"],
            a.get("target_type", "single"),
            a.get("blast_multiplier", 1.0),
            a.get("boost", [])
        ) for a in data["attack"]
    ]
    talent = [
        Talent(
            t["stat"], 
            t["boost_type"], 
            t["value"], 
            t["condition"]
        ) for t in data.get("talent", [])
    ]
    return Character(data["name"], base_stat, trace, attack, talent)

def parse_lightcone(data):
    base_stat = Stat(
        hp = data["base_stat"]["hp"],
        atk = data["base_stat"]["atk"],
        def_ = data["base_stat"]["def_"],
        spd = data["base_stat"]["spd"],
        crit_rate = data["base_stat"]["crit_rate"],
        crit_dmg = data["base_stat"]["crit_dmg"],
        e_dmg = data["base_stat"]["e_dmg"],
        energy = 0
    )
    return Lightcone(data["name"], base_stat)

# Main execution
def main():
    characters = load_json("data/character.json")
    lightcones = load_json("data/lightcone.json")
    
    character = parse_character(characters[0])
    lightcone = parse_lightcone(lightcones[0])
    
    # Pre-Combat Stats
    pre_combat_stat, combined_base_stat, percentage_boost, flat_boost = calculate_pre_combat_stats(character, lightcone)
    
    # Calculation for each Attack
    results = []
    for attack in character.attack:
        expected_damage = calculate_expected_damage(
            combined_base_stat,
            percentage_boost,
            flat_boost,
            attack
        )
        results.append((attack.name, expected_damage))
       
    # Results
    print(f"Character: {character.name}")
    print(f"Lightcone: {lightcone.name}")
    print("\nPre-Combat Stats:")
    print(f"HP: {pre_combat_stat.hp:.2f}")
    print(f"ATK: {pre_combat_stat.atk:.2f}")
    print(f"DEF: {pre_combat_stat.def_:.2f}")
    print(f"SPD: {pre_combat_stat.spd:.2f}")
    print(f"Crit Rate: {pre_combat_stat.crit_rate:.2%}")
    print(f"Crit DMG: {pre_combat_stat.crit_dmg:.2%}")
    print(f"Elemental DMG: {pre_combat_stat.e_dmg:.2%}")
    print(f"Energy: {pre_combat_stat.energy:.2f}")
    
    print("\nExpected Damage Outputs:")
    for attack_name, expected_damage in results:
        print(f"{attack_name}:")

        if isinstance(expected_damage, dict):
            for target, dmg in expected_damage.items():
                print(f"  {target} - {dmg:.2f}")
        else:
            print(f"  {expected_damage:.2f}")

if __name__ == "__main__":
    main()