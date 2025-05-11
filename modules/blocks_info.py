def load(globals):
    globals['block_hardness'] = {
        1: 0.5,   # Dirt
        2: 0.6,   # Grass
        3: 1.5,   # Stone
        4: 2.0,   # Brick
        5: 5.0,   # Diamond block
        6: 3.0,   # End bricks
        7: 1.0,   # Oak Planks
        8: 0.2,   # Oak Leaves
        9: 2.0,   # Oak Log
        10: 2.0,  # Stone Brick
        11: 0.1,  # Torch
        12: 0.2,  # Ladder
        13: 0.5,  # TNT
        14: 1.0,  # Private
        15: 0.3,  # Glass
        16: 2.0,  # Acacia Log
        17: 2.0,  # Big Oak Log
        18: 2.0,  # Birch Log
        19: 2.0,  # Spruce Log
        20: 0.7,  # Magma
        21: 0.2,  # Mushroom Block Inside
        22: 0.2,  # Mushroom Red Skin
        23: 0.2,  # Mushroom Brown Skin
        24: 0.5,  # Hay Block
        25: 2.5,  # Crafting Table
        26: 1.0,  # Pumpkin
        27: 0.1,  # Debug
        28: 0.1,  # Debug 2
        29: 0.2,  # Red Mushroom (item)
        30: 0.2,  # Brown Mushroom (item)
        31: 3.0,  # Diamond Ore
        32: 3.0,  # Emerald Ore
        33: 3.0,  # Gold Ore
        34: 3.0,  # Iron Ore
        35: 2.0,  # Nether Brick
        36: 3.0,  # Redstone Ore
        37: 2.5,  # Coal Ore
        38: 0.0,  # Diamond (item)
        39: 0.0,  # Emerald (item)
        40: 0.0,  # Gold Ingot (item)
        41: 0.0,  # Iron Ingot (item)
        42: 0.0,  # Netherbrick (item)
        43: 0.0,  # Redstone Dust (item)
        44: 0.0,  # Charcoal (item)
        45: 5.0,  # Coal Block
        46: 5.0,  # Iron Block
        47: 1.2,  # Cobblestone
        48: 0.0,  # Gunpowder (item)
        49: 0.0,  # Sand
        50: 0.0,  # Stick (item)
        51: 1.3,  # Cobblestone mossy
        52: 1.0,  # Chest
        53: 1.3,  # Furnace
        54: 1.0,  # Trapdoor (closed)
        55: 1.0,  # Trapdoor (opened)
        100: 9999.0,  # Bedrock (unbreakable)
    }

    globals['ores'] = [
        {"id": 31, "min_y": 560, "max_y": 615, "chance": 0.002, "cluster": 3},  # Diamond: very rare, bottom 60 rows
        {"id": 32, "min_y": 500, "max_y": 600, "chance": 0.003, "cluster": 3},  # Emerald: rare, also deep
        {"id": 33, "min_y": 400, "max_y": 580, "chance": 0.006, "cluster": 4},  # Gold: mid-deep
        {"id": 34, "min_y": 300, "max_y": 590, "chance": 0.005, "cluster": 5},  # Iron: common, wide range
        {"id": 36, "min_y": 350, "max_y": 600, "chance": 0.008, "cluster": 5},  # Redstone: mid-deep
        {"id": 37, "min_y": 100, "max_y": 580, "chance": 0.007, "cluster": 6},  # Coal: most common, large vertical range
    ]

    globals['rarities'] = {
        38: {"rarity": 0.02, "max_count": 1},  # Diamond (item)
        39: {"rarity": 0.02, "max_count": 1},  # Emerald
        40: {"rarity": 0.05, "max_count": 2},  # Gold Ingot
        41: {"rarity": 0.06, "max_count": 3},  # Iron Ingot
        42: {"rarity": 0.07, "max_count": 3},  # Netherbrick
        43: {"rarity": 0.08, "max_count": 5},  # Redstone Dust
        44: {"rarity": 0.08, "max_count": 5},  # Charcoal
        48: {"rarity": 0.10, "max_count": 4},  # Gunpowder
        50: {"rarity": 0.12, "max_count": 6},  # Stick
        29: {"rarity": 0.15, "max_count": 3},  # Red Mushroom
        30: {"rarity": 0.15, "max_count": 3},  # Brown Mushroom
        13: {"rarity": 0.05, "max_count": 1},  # TNT
    }