import re
from Arknights.addons.contrib.common_cache import load_game_data
import logging


logger = logging.getLogger(__name__)


recruit_database_bak = [
    ("Lancet-2", 0, ["Medic", "Ranged", "Healing", "Support"]),
    ("Castle-3", 0, ["Guard", "Melee", "Support", "Support"]),
    ("Yato", 1, ["Vanguard", "Melee", "Starter"]),
    ("Noir Corne", 1, ["Defender", "Melee", "Starter"]),
    ("Rangers", 1, ["Sniper", "Ranged", "Starter"]),
    ("Durin", 1, ["Caster", "Ranged", "Starter"]),
    ("12F", 1, ["Caster", "Ranged", "Starter"]),
    ("Fang", 2, ["Vanguard", "Melee", "DP-Recovery"]),
    ("Vanilla", 2, ["Vanguard", "Melee", "DP-Recovery"]),
    ("Plume", 2, ["Vanguard", "Melee", "DPS", "DP-Recovery"]),
    ("Melantha", 2, ["Guard", "Melee", "DPS", "Survival"]),
    ("Beagle", 2, ["Defender", "Melee", "Defense"]),
    ("Kroos", 2, ["Sniper", "Ranged", "DPS"]),
    ("Adnachiel", 2, ["Sniper", "Ranged", "DPS"]),
    ("Lava", 2, ["Caster", "Ranged", "AoE"]),
    ("Hibiscus", 2, ["Medic", "Ranged", "Healing"]),
    ("Ansel", 2, ["Medic", "Ranged", "Healing"]),
    ("Steward", 2, ["Caster", "Ranged", "DPS"]),
    ("Orchid", 2, ["Supporter", "Ranged", "Slow"]),
    ("Haze", 3, ["Caster", "Ranged", "DPS", "Debuff"]),
    ("Gitano", 3, ["Caster", "Ranged", "AoE"]),
    ("Jessica", 3, ["Sniper", "Ranged", "DPS", "Survival"]),
    ("Meteor", 3, ["Sniper", "Ranged", "DPS", "Debuff"]),
    ("Shirayuki", 3, ["Sniper", "Ranged", "AoE", "Slow"]),
    ("Scavenger", 3, ["Vanguard", "Melee", "DP-Recovery", "DPS"]),
    ("Vigna", 3, ["Vanguard", "Melee", "DPS", "DP-Recovery"]),
    ("Dobermann", 3, ["Guard", "Melee", "DPS", "Support"]),
    ("Matoimaru", 3, ["Guard", "Melee", "Survival", "DPS"]),
    ("Frostleaf", 3, ["Guard", "Melee", "Slow", "DPS"]),
    ("Estelle", 3, ["Guard", "Melee", "AoE", "Survival"]),
    ("Mousse", 3, ["Guard", "Melee", "DPS"]),
    ("Gravel", 3, ["Specialist", "Melee", "Fast-Redeploy", "Defense"]),
    ("Rope", 3, ["Specialist", "Melee", "Shift"]),
    ("Myrrh", 3, ["Medic", "Ranged", "Healing"]),
    ("Perfumer", 3, ["Medic", "Ranged", "Healing"]),
    ("Matterhorn", 3, ["Defender", "Melee", "Defense"]),
    ("Cuora", 3, ["Defender", "Melee", "Defense"]),
    ("Gummy", 3, ["Defender", "Melee", "Defense", "Healing"]),
    ("Earthspirit", 3, ["Supporter", "Ranged", "Slow"]),
    ("Shaw", 3, ["Specialist", "Melee", "Shift"]),
    ("Ptilopsis", 4, ["Medic", "Ranged", "Healing", "Support"]),
    ("Zima", 4, ["Vanguard", "Melee", "DP-Recovery", "Support"]),
    ("Texas", 4, ["Vanguard", "Melee", "DP-Recovery", "Crowd-Control"]),
    ("Indra", 4, ["Guard", "Melee", "DPS", "Survival"]),
    ("Specter", 4, ["Guard", "Melee", "AoE", "Survival"]),
    ("Blue Poison", 4, ["Sniper", "Ranged", "DPS"]),
    ("Platinum", 4, ["Sniper", "Ranged", "DPS"]),
    ("Meteorite", 4, ["Sniper", "Ranged", "AoE", "Debuff"]),
    ("May", 4, ["Supporter", "Ranged", "Summon", "Crowd-Control"]),
    ("Silence", 4, ["Medic", "Ranged", "Healing"]),
    ("Warfarin", 4, ["Medic", "Ranged", "Healing", "Support"]),
    ("Nearl", 4, ["Defender", "Melee", "Defense", "Healing"]),
    ("Projekt Red", 4, ["Specialist", "Melee", "Fast-Redeploy", "Crowd-Control"]),
    ("Liskarm", 4, ["Defender", "Melee", "Defense", "DPS"]),
    ("Croissant", 4, ["Defender", "Melee", "Defense", "Shift"]),
    ("Vulcan", 4, ["Defender", "Melee", "Survival", "Defense", "DPS"]),
    ("Provence", 4, ["Sniper", "Ranged", "DPS"]),
    ("Firewatch", 4, ["Sniper", "Ranged", "DPS", "Nuker"]),
    ("Cliffheart", 4, ["Specialist", "Melee", "Shift", "DPS"]),
    ("Pramanix", 4, ["Supporter", "Ranged", "Debuff"]),
    ("Istina", 4, ["Supporter", "Ranged", "Slow", "DPS"]),
    ("Manticore", 4, ["Specialist", "Melee", "DPS", "Survival"]),
    ("FEater", 4, ["Specialist", "Melee", "Shift", "Slow"]),
    ("Exusiai", 5, ["Sniper", "Ranged", "DPS"]),
    ("Siege", 5, ["Vanguard", "Melee", "DP-Recovery", "DPS"]),
    ("Ifrit", 5, ["Caster", "Ranged", "AoE", "Debuff"]),
    ("Shining", 5, ["Medic", "Ranged", "Healing", "Support"]),
    ("Nightingale", 5, ["Medic", "Ranged", "Healing", "Support"]),
    ("Hoshiguma", 5, ["Defender", "Melee", "Defense", "DPS"]),
    ("Saria", 5, ["Defender", "Melee", "Defense", "Healing", "Support"]),
    ("SilverAsh", 5, ["Guard", "Melee", "DPS", "Support"]),
    ("Sora", 2, ["Sniper", "Ranged", "AoE"]),
    ("Midnight", 2, ["Guard", "Melee", "DPS"]),
    ("Beehunter", 3, ["Guard", "Melee", "DPS"]),
    ("Nightmare", 4, ["Caster", "Ranged", "DPS", "Healing", "Slow"]),
    ("Skadi", 5, ["Guard", "Melee", "DPS", "Survival"]),
    ("Ch'en", 5, ["Guard", "Melee", "DPS", "Nuker"]),
    ("Swire", 4, ["Guard", "Melee", "DPS", "Support"]),
    ("Greyy", 3, ["Caster", "Ranged", "AoE", "Slow"]),
    ("Popukar", 2, ["Guard", "Melee", "AoE", "Survival"]),
    ("Spot", 2, ["Defender", "Melee", "Defense", "Healing"]),
    ("THRM-EX", 0, ["Specialist", "Melee", "Nuker", "Support机械"]),
    ("Schwarz", 5, ["Sniper", "Ranged", "DPS"]),
    ("Hellagur", 5, ["Guard", "Melee", "DPS", "Survival"]),
    ("Glaucus", 4, ["Supporter", "Ranged", "Slow", "Crowd-Control"]),
    ("Astesia", 4, ["Guard", "Melee", "DPS", "Defense"]),
    ("Sussurro", 3, ["Medic", "Ranged", "Healing"]),
    ("Myrtle", 3, ["Vanguard", "Melee", "DP-Recovery", "Healing"]),
    ("Magallan", 5, ["Supporter", "Ranged", "Support", "Slow", "DPS"]),
    ("Executor", 4, ["Sniper", "Ranged", "AoE"]),
    ("Vermeil", 3, ["Sniper", "Ranged", "DPS"]),
    ("Mostima", 5, ["Caster", "Ranged", "AoE", "Support", "Crowd-Control"]),
    ("Waai Fu", 4, ["Specialist", "Melee", "Fast-Redeploy", "Debuff"]),
    ("Purestream", 3, ["Medic", "Ranged", "Healing", "Support"]),
    ("May", 3, ["Sniper", "Ranged", "DPS", "Slow"]),
    ("Blaze", 5, ["Guard", "Melee", "DPS", "Survival"]),
    ("GreyThroat", 4, ["Sniper", "Ranged", "DPS"]),
    ("Reed", 4, ["Vanguard", "Melee", "DP-Recovery", "DPS"]),
    ("Broca", 4, ["Guard", "Melee", "AoE", "Survival"]),
    ("Ambriel", 3, ["Sniper", "Ranged", "DPS", "Slow"]),
    ("Aak", 5, ["Specialist", "Ranged", "Support", "DPS"]),
    ("Hung", 4, ["Defender", "Melee", "Defense", "Healing"]),
    ("'Justice Knight'", 0, ["Sniper", "Ranged", "Support", "Support"]),
    ("Ceobe", 5, ["Caster", "Ranged", "DPS", "Crowd-Control"]),
    ("Leizi", 4, ["Caster", "Ranged", "DPS"]),
    ("Bagpipe", 5, ["Vanguard", "Melee", "DP-Recovery", "DPS"]),
    ("Sesa", 4, ["Sniper", "Ranged", "AoE", "Debuff"]),
    ("Utage", 3, ["Guard", "Melee", "DPS", "Survival"]),
    ("Cutter", 3, ["Guard", "Melee", "Nuker", "DPS"]),
    ("Shamare", 4, ["Supporter", "Ranged", "Debuff"]),
    ("Phantom", 5, ["Specialist", "Melee", "Fast-Redeploy", "Crowd-Control", "DPS"]),
]


def get_all_recruit_characters():
    recruit_re = re.compile(r"(★+)\n(.*?)(\n|$)")
    recruit_detail = load_game_data("gacha_table")["recruitDetail"].replace(
        "Justice Knight", "'Justice Knight'"
    )
    # print(recruit_detail)
    result = recruit_re.findall(recruit_detail, re.MULTILINE)
    return parse_match_groups(result)


def parse_match_groups(groups):
    result = []
    for group in groups:
        # star_count = len(group[0])
        characters = []
        for character in group[1].split(" / "):
            characters.append(character.replace("<@rc.eml>", "").replace("</>", ""))
        result += characters
        # print(star_count, characters)
    return result


def get_character_name_map():
    characters = load_game_data("character_table").values()
    result = {}
    # position = set()
    # profession = set()
    for character in characters:
        result[character["name"]] = character
    #     position.add(character['position'])
    #     profession.add(character['profession'])
    # print(position)
    # print(profession)
    return result


profession_map = {
    "MEDIC": "Medic",
    "WARRIOR": "Guard",
    "PIONEER": "Vanguard",
    "CASTER": "Caster",
    "SPECIAL": "Specialist",
    "SUPPORT": "Supporter",
    "TANK": "Defender",
    "SNIPER": "Sniper",
}
position_map = {
    "MELEE": ["Melee"],
    "RANGED": ["Ranged"],
    "ALL": ["Melee", "Ranged"],
}


def get_recruit_database_by_game_data():
    all_recruit_characters = get_all_recruit_characters()
    character_name_map = get_character_name_map()
    result = []
    for character_name in all_recruit_characters:
        character = character_name_map.get(character_name)
        if not character:
            logger.warning("character not found: %s", character_name)
            continue
        tag_list = [profession_map.get(character["profession"])]
        tag_list += position_map.get(character["position"], [])
        tag_list += character["tagList"]
        # print((character_name, character['rarity'], tag_list))
        if character["rarity"] == 0:
            tag_list.append("Support")
        result.append((character_name, character["rarity"], tag_list))
    return result


def check_data():
    recruit_database = get_recruit_database_by_game_data()
    recruit_database_map = {}
    for character_name, rarity, tag_list in recruit_database:
        recruit_database_map[character_name] = (rarity, tag_list)
    old_recruit_database_map = {}
    for character_name, rarity, tag_list in recruit_database_bak:
        old_recruit_database_map[character_name] = (rarity, tag_list)
    print("=" * 20, 1)
    check_data_map(recruit_database_map, old_recruit_database_map)
    print("=" * 20, 2)
    check_data_map(old_recruit_database_map, recruit_database_map)


def check_data_map(data_map1, data_map2):
    for character_name in data_map1:
        data1 = data_map1[character_name]
        data2 = data_map2.get(character_name)
        if not data2:
            print("no backup data:", character_name, data1)
            continue
        if data1[0] != data2[0]:
            print("rarity not match:", character_name, data1, data2)
        if data1[1][:2] != data2[1][:2]:
            print("position/profession not match:", character_name, data1, data2)
        if sorted(data1[1][2:]) != sorted(data2[1][2:]):
            print("tag_list not match:", character_name, data1, data2)


try:
    recruit_database = get_recruit_database_by_game_data()
except Exception as e:
    logger.exception(e)
    recruit_database = recruit_database_bak


__all__ = ["recruit_database"]


if __name__ == "__main__":
    check_data()
