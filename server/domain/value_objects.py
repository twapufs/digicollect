from enum import Enum


class Role(str, Enum):
    admin = "admin"
    collector = "collector"


class Rarity(str, Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    epic = "epic"
    legendary = "legendary"
