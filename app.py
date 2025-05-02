from perlin_noise import PerlinNoise
import pywintypes
import importlib
import win32con
import win32api
import pygame
import pickle
import random
import time
import math
import json
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)

COMMANDS_DIR = os.path.join(BASE_DIR, "commands")

command_map = {}


def load_commands():
    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            command_name = filename[:-3]
            module_name = f"commands.{command_name}"
            try:
                spec = importlib.util.spec_from_file_location(command_name, os.path.join(COMMANDS_DIR, filename))
                command_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(command_module)
                command_map[command_name] = command_module.execute
                print(f"Command '{command_name}' loaded successfully.")
            except Exception as e:
                print(f"Error loading command '{command_name}': {e}")


load_commands()
VERSION = "1.8.0"

os.environ["SDL_VIDEO_CENTERED"] = "1"

# NAME = "Yaroslav"
NAME = "Malyku"

with open(os.path.join(BASE_DIR,"config.json"), "r") as file:
    settings = json.load(file)

RESOLUTION = tuple(settings["resolution"])


def reset_resolution():
    win32api.ChangeDisplaySettings(None, 0)


try:

    pygame.init()
    pygame.mixer.init()

    info = pygame.display.Info()
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    TILE_SIZE = 30
    PLAYER_SIZE = 30
    ROWS = 620
    COLS = 1000

    ground_level = 250

    TORCH_COLOR = (255, 200, 100, 150)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    BROWN = (139, 69, 19)
    FOG_COLOR = (0, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (252, 3, 3)

    DEBUG_MENU = False
    FLY = False
    GOD = False
    SafeZone = False
    GameMode = 0
    NoClip = False
    Cheats = False
    Settings = False
    last_toggle_time = 0
    cooldown_time = 0.3
    CRAFTING_OPEN = False
    INVENTORY_CRAFTING_OPENED = False
    CRAFTING_GRID = [[None for _ in range(3)] for _ in range(3)]
    INVENTORY_CRAFTING_GRID = [[None for _ in range(2)] for _ in range(2)]
    CRAFTING_OUTPUT = None
    dragging_item = None
    dragging_from_inventory = False
    dragging_from_grid = False
    dragging_pos = None
    chests = []
    current_open_chest = None
    dragging_from_chest = False
    inventory_open = False
    inventory_slots = 27
    inventory_chest = [[None for _ in range(9)] for _ in range(3)]
    selected_item = None
    PAUSED = False
    world_name = ""
    FPS = 60
    FURNACE_OPEN = False
    current_open_furnace = None

    INVENTORY_CRAFTING_RECIPES = {
    }
    CRAFTING_RECIPES = {
    }
    SMELT_RECIPES = {
    }

    for filename in os.listdir(os.path.join(BASE_DIR, "recipes", "furnace")):
        if filename.endswith(".json"):
            filepath = os.path.join(BASE_DIR, "recipes", "furnace", filename)
            with open(filepath, 'r') as f:
                data = json.load(f)

            for input_id_str, recipe in data.items():
                input_id = int(input_id_str)
                output_id = recipe["result"]
                smelt_time = recipe["smelt_time"]

                SMELT_RECIPES[input_id] = {
                    "result": output_id,
                    "smelt_time": smelt_time
                }

    for filename in os.listdir(os.path.join(BASE_DIR, "recipes", "inventory_crafting_table")):
        if filename.endswith(".json"):
            filepath = os.path.join(os.path.join(BASE_DIR, "recipes", "inventory_crafting_table"), filename)
            with open(filepath, 'r') as f:
                data = json.load(f)

            recipe = tuple(tuple(cell if cell is not None else None for cell in row) for row in data["recipe"])
            output = tuple(data["output"].values())

            INVENTORY_CRAFTING_RECIPES[recipe] = output

    for filename in os.listdir(os.path.join(BASE_DIR, "recipes", "crafting_table")):
        if filename.endswith(".json"):
            filepath = os.path.join(os.path.join(BASE_DIR, "recipes", "crafting_table"), filename)
            with open(filepath, 'r') as f:
                data = json.load(f)

            recipe = tuple(tuple(cell if cell is not None else None for cell in row) for row in data["recipe"])
            output = tuple(data["output"].values())

            CRAFTING_RECIPES[recipe] = output

    screen = pygame.display.set_mode((800, 600))
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    pygame.display.set_caption("TerrMine")

    font1 = pygame.font.Font(os.path.join(BASE_DIR, "assets\\font\\Minecraftchmc-dBlX.ttf"), 50)
    font1_ = pygame.font.Font(os.path.join(BASE_DIR, "assets\\font\\Minecraftchmc-dBlX.ttf"), 20)
    layer_font = pygame.font.Font(os.path.join(BASE_DIR, "assets\\font\\Minecraftchmc-dBlX.ttf"), 30)
    font2 = pygame.font.Font(os.path.join(BASE_DIR, "assets\\font\\MinecraftTen-VGORe.ttf"), 100)

    menu_background = pygame.image.load(os.path.join(BASE_DIR, "assets\\menu_background.png"))
    menu_background2 = pygame.image.load(os.path.join(BASE_DIR, "assets\\menu_background2.png"))

    player_textures = {
        "idle": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\idle.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "jump": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\jump.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "down": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\down.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "walk-1": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\walk-1.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "walk-2": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\walk-2.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "walk-3": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\walk-3.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
        "walk-4": pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\player\\walk-4.png")).convert(screen),
            (PLAYER_SIZE, PLAYER_SIZE)),
    }

    textures = {
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\dirt.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\grass.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\stone.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\brick.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        5: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\diamond.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        6: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\end_bricks.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        7: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\planks_oak.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        8: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\leaves_oak.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        9: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_oak.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        10: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\stonebrick.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        11: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\torch_on.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        12: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\ladder.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        13: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\tnt.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        14: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\private.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        15: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\glass.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        16: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_acacia.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        17: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_big_oak.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        18: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_birch.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        19: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_spruce.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        20: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\magma.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        21: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_inside.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        22: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_skin_red.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        23: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_skin_brown.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        24: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\hay_block_side.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        25: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\crafting_table_front.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        26: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\pumpkin_face_off.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        27: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\debug.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        28: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\debug2.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        29: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_red.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        30: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_brown.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        31: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\diamond_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        32: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\emerald_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        33: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\gold_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        34: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\iron_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        35: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\nether_brick.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        36: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\redstone_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        37: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\coal_ore.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        38: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\diamond.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        39: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\emerald.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        40: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\gold_ingot.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        41: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\iron_ingot.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        42: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\netherbrick.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        43: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\redstone_dust.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        44: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\charcoal.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        45: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\coal_block.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        46: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\iron_block.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        47: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\cobblestone.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        48: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\gunpowder.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        49: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\sand.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        50: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\stick.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        51: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\cobblestone_mossy.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        52: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\chest.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        53: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\furnace\\furnace_front_off.png")).convert(),(TILE_SIZE, TILE_SIZE)),
        54: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\trapdoor\\closed.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        55: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\trapdoor\\opened.png")).convert_alpha(),(TILE_SIZE, TILE_SIZE)),
        100: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\bedrock.png")).convert(),(TILE_SIZE, TILE_SIZE)),
    }

    destruction_textures = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_0.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_1.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_2.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_3.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_4.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_5.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_6.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_7.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_8.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\destroy_stages\\destroy_stage_9.png")).convert_alpha(screen),
            (TILE_SIZE, TILE_SIZE)),
    ]

    fire_stages = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_1.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_2.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_3.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_4.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_5.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_6.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_7.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_8.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_9.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_10.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_11.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_12.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_13.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
        pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\fire_stages\\fire_stage_14.png")).convert_alpha(
                screen),
            (TILE_SIZE, TILE_SIZE)),
    ]

    def load_and_scale(path, scale_factor):
        image = pygame.image.load(path).convert_alpha(screen)
        width, height = image.get_size()
        return pygame.transform.smoothscale(image, (int(width * scale_factor), int(height * scale_factor)))


    arrow_stages = [
        load_and_scale(os.path.join(BASE_DIR, f"assets\\arrow_stages\\arrow_stage_{i}.png"), 1.8)
        for i in range(1, 24)
    ]

    block_hardness = {
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
        51: 1.3,
        100: 9999.0,  # Bedrock (unbreakable)
    }

    ores = [
        {"id": 31, "min_y": 560, "max_y": 615, "chance": 0.002, "cluster": 3},  # Diamond: very rare, bottom 60 rows
        {"id": 32, "min_y": 500, "max_y": 600, "chance": 0.003, "cluster": 3},  # Emerald: rare, also deep
        {"id": 33, "min_y": 400, "max_y": 580, "chance": 0.006, "cluster": 4},  # Gold: mid-deep
        {"id": 34, "min_y": 300, "max_y": 590, "chance": 0.005, "cluster": 5},  # Iron: common, wide range
        {"id": 36, "min_y": 350, "max_y": 600, "chance": 0.008, "cluster": 5},  # Redstone: mid-deep
        {"id": 37, "min_y": 100, "max_y": 580, "chance": 0.007, "cluster": 6},  # Coal: most common, large vertical range
    ]

    rarities = {
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

    FUEL_BURN_TIMES = {
        7: 10,  # Oak Planks
        44: 40,  # Coal
        50: 5  # Stick
    }

    furnaces = [] # {"x": int, "y": int, "fuel": [id, count], "input": [id, count], "output": [id, count], "burn_time": float, "smelt_progress": float}

    loot_counts = {item_id: 0 for item_id in rarities}

    dead = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\You died!.png")).convert_alpha(screen),
                                  (SCREEN_WIDTH, SCREEN_HEIGHT))

    grayscale_textures = {}
    for tile, tex in textures.items():
        gray = tex.copy()
        overlay = pygame.Surface(tex.get_size(), pygame.SRCALPHA)
        overlay.fill((180, 180, 180, 50))
        gray.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        grayscale_textures[tile] = gray

    crosshair = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR,"assets\\crosshair.png")).convert_alpha(screen),
                                       (TILE_SIZE, TILE_SIZE))
    shield = pygame.image.load(os.path.join(BASE_DIR,"assets\\player\\shield.png")).convert_alpha(screen)

    explosion_sound = pygame.mixer.Sound(os.path.join(BASE_DIR,"assets\\sound_effects\\explosion.mp3"))
    explosion_img = pygame.image.load(os.path.join(BASE_DIR,"assets\\explosion.png")).convert_alpha()

    world = [[]]
    torches = []
    private_blocks = []
    homes = []
    damage_tracker = {}
    player = pygame.Rect(SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT // 2 - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    player.y = 140
    scroll_x = 0
    scroll_y = -6000
    health = 10
    SURVIVAL = False
    IMMNUNE_TIME = 10
    IMMNUNE_TIMER = time.time() + 10
    seed = None


    def show_progress(screen, font, message, percent):
        screen.fill((0, 0, 0))
        text = font.render(f"{message} ({percent}%)", True, (255, 255, 255))
        rect = text.get_rect(center=(400, 300))
        screen.blit(text, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    def random_loot_item(loot_counts, rng):
        if rng.randrange(0, 3) == 2:
            available_items = [
                item_id for item_id in rarities
                if loot_counts[item_id] < rarities[item_id]["max_count"]
            ]

            if not available_items:
                return 0

            weights = [rarities[item]["rarity"] for item in available_items]
            chosen = rng.choices(available_items, weights=weights, k=1)[0]
            loot_counts[chosen] += 1
            return chosen
        else:
            return 0


    def generate_world(sid, screen=None):
        global seed

        seed = sid
        noise = PerlinNoise(octaves=5, seed=sid)
        world = [[[0, 1] for _ in range(COLS)] for _ in range(ROWS)]
        font = pygame.font.SysFont("Arial", 30)

        scale = 50
        amplitude = 10
        dirt_thickness = 7
        tree_density = 0.08
        min_tree_distance = 5
        cave_noise = PerlinNoise(octaves=2, seed=sid + 999)
        cave_scale = 40
        cave_threshold = -0.25

        ground_positions = []

        rng = random.Random(sid)

        # ---------- 1. Generate Terrain ----------
        total_steps = COLS - 1
        for i, x in enumerate(range(1, COLS)):
            ground = int(ground_level + noise(x / scale) * amplitude)
            ground_positions.append((x, ground))

            for y in range(ground):
                world[y][x][0] = 0
            if ground < ROWS - 1:
                world[ground][x][0] = 2
            for y in range(ground + 1, min(ground + 1 + dirt_thickness, ROWS - 1)):
                world[y][x][0] = 1
            for y in range(ground + 1 + dirt_thickness, ROWS - 1):
                world[y][x][0] = 3

        if screen:
            show_progress(screen, font, "Generating terrain", 30)

        # ---------- 2. Place Trees ----------
        last_tree_x = -min_tree_distance
        for x, ground in ground_positions:
            if x - last_tree_x >= min_tree_distance and ground < ROWS - 6 and rng.random() < tree_density:
                tree_block = rng.choice([9, 16, 17, 18, 19])
                for y in range(ground - 1, ground - 5, -1):
                    if y >= 0:
                        world[y][x][0] = tree_block
                        world[y][x][1] = 2
                for ly in range(ground - 7, ground - 3):
                    for lx in range(x - 2, x + 3):
                        if 0 <= ly < ROWS and 0 <= lx < COLS:
                            dist = ((lx - x) ** 2 + (ly - (ground - 5)) ** 2) ** 0.5
                            if dist <= 2.5 and world[ly][lx][0] == 0:
                                world[ly][lx][0] = 8
                                world[ly][lx][1] = 1
                last_tree_x = x

        if screen:
            show_progress(screen, font, "Placing trees", 40)

        for y in range(ROWS):
            world[y][0][0] = 0
            world[y][0][1] = 3  # Special collision layer
            world[y][COLS - 1][0] = 0
            world[y][COLS - 1][1] = 3  # Special collision layer

        for x in range(COLS):
            world[ROWS - 1][x][0] = 100
            world[10][x][0] = 0
            world[10][x][1] = 3

            # ---------- 3. Generate Ores ----------
        ore_total = len(ores)
        for oi, ore in enumerate(ores):
            for y in range(ore["min_y"], ore["max_y"]):
                for x in range(1, COLS - 1):
                    if world[y][x][0] == 3 and rng.random() < ore["chance"]:
                        for _ in range(ore["cluster"]):
                            dx = x + rng.randint(-1, 1)
                            dy = y + rng.randint(-1, 1)
                            if 0 <= dx < COLS and 0 <= dy < ROWS and world[dy][dx][0] == 3:
                                world[dy][dx][0] = ore["id"]
            if screen:
                progress = 40 + int(((oi + 1) / ore_total) * 30)
                show_progress(screen, font, "Generating ores", progress)

        ground_dict = dict(ground_positions)

        # ---------- 4. Generate Caves ----------
        for y in range(100, ROWS - 1):
            for x in range(1, COLS - 1):
                ground_y = ground_dict.get(x, ground_level)
                if y > ground_y + 3:
                    nx = x / cave_scale
                    ny = y / cave_scale
                    value = cave_noise([nx, ny])
                    if value < cave_threshold:
                        world[y][x][0] = 100500
            if screen and y % 10 == 0:
                progress = 70 + int(((y - 100) / (ROWS - 101)) * 30)
                show_progress(screen, font, "Carving caves", min(progress, 99))

        # ---------- 5. Place Structure in Stone Layer ----------
        structure = [
            [51, 51, 51, 51, 51, 51, 51, 51],
            [51, 0, 0, 0, 0, 0, 0, 51],
            [51, 0, 52, 0, 0, 52, 0, 51],
            [51, 51, 51, 51, 51, 51, 51, 51],
        ]

        struct_w = len(structure[0])
        struct_h = len(structure)

        attempts = COLS // 100

        for _ in range(attempts):
            rand_x = rng.randint(1, COLS - struct_w - 1)
            ground_y = dict(ground_positions).get(rand_x, ground_level)
            rand_y = rng.randint(ground_y + 1, ROWS - struct_h - 1)

            for sy in range(struct_h):
                for sx in range(struct_w):
                    block_id = structure[sy][sx]
                    wx = rand_x + sx
                    wy = rand_y + sy
                    world[wy][wx][0] = block_id

                    if block_id == 52:
                        loot_counts = {item_id: 0 for item_id in rarities}

                        items = []
                        for _ in range(18):
                            item_id = random_loot_item(loot_counts, rng)
                            items.append([item_id, rng.randint(1, 3)])

                        chests.append({
                            "x": wx,
                            "y": wy,
                            "layer": 1,
                            "items": items
                        })

        if screen:
            show_progress(screen, font, "Placing structure", 90)

        if screen:
            show_progress(screen, font, "World generation complete!", 100)

        return world


    class Console:
        def __init__(self):
            self.is_open = False
            self.input_text = ""
            self.history = []
            self.font = pygame.font.SysFont("consolas", 20)
            self.max_history = 10

        def toggle(self):
            self.is_open = not self.is_open

        def handle_event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.execute_command(self.input_text)
                    self.input_text = ""
                else:
                    self.input_text += event.unicode

        def execute_command(self, command):
            self.history.append(command)
            if len(self.history) > self.max_history:
                self.history.pop(0)

            command_parts = command.split()

            if len(command_parts) > 0:
                command_name = command_parts[0].lstrip("/").lstrip("//")

                command_func = command_map.get(command_name)

                if command_func:
                    command_func(self, command_parts, globals())
                else:
                    self.history.append(f"Unknown command: {command_name}")

        def draw(self, screen):
            if not self.is_open:
                return

            console_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            console_surface.fill((0, 0, 0, 150))

            screen.blit(console_surface, (0, SCREEN_HEIGHT - SCREEN_HEIGHT))

            input_surface = self.font.render(self.input_text, True, (255, 255, 255))
            screen.blit(input_surface, (10, SCREEN_HEIGHT - 30))

            for i, line in enumerate(reversed(self.history)):
                history_surface = self.font.render(line, True, (200, 200, 200))
                screen.blit(history_surface, (10, SCREEN_HEIGHT - 60 - i * 20))


    class PlayerStats:
        def __init__(self):
            self.max_health = 10
            self.health = self.max_health
            self.fall_threshold = 10  # Damage starts after falling 10 units (adjust this value)
            self.fall_damage_rate = 0.5  # 1 damage per block fallen
            self.fall_distance = 0  # Track how far the player has fallen
            self.is_falling = False

            self.full_heart = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR,"assets\\heart\\full.png")).convert_alpha(screen),
                                                     (14, 12))
            self.half_heart = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR,"assets\\heart\\half.png")).convert_alpha(screen),
                                                     (14, 12))
            self.empty_heart = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR,"assets\\heart\\empty.png")).convert_alpha(screen),
                                                      (14, 12))

        def draw_hearts(self, screen):
            heart_x = SCREEN_WIDTH * 0.5 - 200
            heart_y = SCREEN_HEIGHT - 80

            heart_spacing = 16

            for i in range(self.max_health):
                if self.health >= i + 1:
                    screen.blit(self.full_heart, (heart_x, heart_y))
                elif self.health > i:
                    screen.blit(self.half_heart, (heart_x, heart_y))
                else:
                    screen.blit(self.empty_heart, (heart_x, heart_y))

                heart_x += heart_spacing

        def draw_ui(self, screen):
            if SURVIVAL:
                self.draw_hearts(screen)


    class FakeButton:

        def __init__(self, text, x, y, width, height):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)

        def draw(self, screen):
            pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
            text_surf = font1.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def check_click(self, pos):
            pass


    class Button:

        def __init__(self, text, x, y, width, height, action):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.action = action

        def draw(self, screen):
            pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
            text_surf = font1.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def check_click(self, pos):
            if self.rect.collidepoint(pos):
                self.action()


    class Inventory:
        def __init__(self):
            if not SURVIVAL:
                self.items = [[54, 1], [1, 1], [2, 1], [3, 1], [47, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
                              [9, 1], [16, 1], [17, 1], [18, 1], [19, 1], [10, 1], [11, 1], [12, 1],
                              [13, 1], [14, 1], [15, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1],
                              [25, 1], [26, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1],
                              [35, 1], [36, 1], [37, 1], [45, 1], [46, 1], [49, 1], [51, 1], [52, 1],
                              [53, 1], [0, 1]]

                self.max_items = len(self.items)
            else:
                self.items = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
                self.max_items = 10

            self.selected_index = 0
            self.scroll_index = 0

        def scroll(self, direction):
            self.selected_index += direction
            if self.selected_index < 0:
                self.selected_index = len(self.items) - 1
            elif self.selected_index >= len(self.items):
                self.selected_index = 0

            if len(self.items) > max_items_per_row:
                if self.selected_index < self.scroll_index:
                    self.scroll_index = self.selected_index
                elif self.selected_index >= self.scroll_index + max_items_per_row:
                    self.scroll_index = self.selected_index - max_items_per_row + 1

        def get_selected_block(self):
            return self.items[self.selected_index][0]

        def append_new_item(self, block_id, amount=1):
            MAX_STACK = 64

            for i in range(len(self.items)):
                slot_id, quantity = self.items[i]
                if slot_id == block_id and quantity < MAX_STACK:
                    space_left = MAX_STACK - quantity
                    to_add = min(space_left, amount)
                    self.items[i][1] += to_add
                    amount -= to_add
                    if amount <= 0:
                        return

            for i in range(len(self.items)):
                slot_id, quantity = self.items[i]
                if slot_id == 0:
                    to_add = min(MAX_STACK, amount)
                    self.items[i] = [block_id, to_add]
                    amount -= to_add
                    if amount <= 0:
                        return

            if len(self.items) < self.max_items:
                to_add = min(MAX_STACK, amount)
                self.items.append([block_id, to_add])
                amount -= to_add
                if amount <= 0:
                    return

            if amount > 0:
                # print(f"Inventory full! Could not add {amount}x block ID {block_id}")
                pass

        def delete_block(self, block_id, amount=1):
            for i in range(len(self.items)):
                slot_id, quantity = self.items[i]
                if slot_id == block_id:
                    if quantity >= amount:
                        self.items[i][1] -= amount
                        if self.items[i][1] <= 0:
                            self.items[i] = [0, 0]
                        return True
                    else:
                        amount -= quantity
                        self.items[i] = [0, 0]
            return False

        def has_block(self, block_id):
            for slot_id, quantity in self.items:
                if slot_id == block_id and quantity > 0:
                    return True
            return False


    class Dynamite:
        def __init__(self, x, y, countdown=3):
            self.x = x
            self.y = y
            self.countdown = countdown
            self.placed_time = None
            self.exploded = False
            self.explosion_time = None
            self.blink_interval = 0.2
            self.last_blink = time.time()
            self.blink_state = False
            self.falling = True

        def update(self, world):
            if self.exploded:
                if self.explosion_time is not None and time.time() - self.explosion_time > 0.5:
                    dynamites.remove(self)
                return

            if self.falling:
                if self.y + 1 < ROWS and world[self.y + 1][self.x][0] in [0, 100500]:
                    self.y += 1
                else:
                    self.falling = False
                    self.placed_time = time.time()
            else:
                elapsed = time.time() - self.placed_time

                if elapsed >= self.countdown - 1:
                    if time.time() - self.last_blink >= self.blink_interval:
                        self.blink_state = not self.blink_state
                        self.last_blink = time.time()

                if elapsed >= self.countdown:
                    self.explode(world)

        def explode(self, world):
            explosion_sound.play()
            explosion_radius = 3
            cx, cy = self.x, self.y

            for dx in range(-explosion_radius, explosion_radius + 1):
                for dy in range(-explosion_radius, explosion_radius + 1):
                    dist = math.sqrt(dx ** 2 + dy ** 2)
                    if dist <= explosion_radius:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < COLS and 0 <= ny < ROWS:
                            if world[ny][nx][0] != 100:
                                world[ny][nx][0] = 100500

                            for pb in private_blocks:
                                pb_x, pb_y, owner, layer = pb
                                if pb_x == nx and pb_y == ny:
                                    private_blocks.remove(pb)
                                    # console.history.append(f"Private block at ({nx}, {ny}) destroyed!")
                                    break

            self.exploded = True
            self.explosion_time = time.time()

        def draw(self, screen, textures):
            if self.exploded:
                screen.blit(explosion_img, ((self.x * TILE_SIZE + scroll_x) - explosion_img.get_width() // 2,
                                            (self.y * TILE_SIZE + scroll_y) - explosion_img.get_height() // 2))
            else:
                tnt_texture = textures[13].copy()
                if self.blink_state:
                    tnt_texture.set_alpha(150)
                    screen.blit(tnt_texture, (self.x * TILE_SIZE + scroll_x, self.y * TILE_SIZE + scroll_y))
                else:
                    screen.blit(textures[13], (self.x * TILE_SIZE + scroll_x, self.y * TILE_SIZE + scroll_y))


    class InputBox:
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = pygame.Color('gray')
            self.text = text
            self.txt_surface = font1_.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = pygame.Color('lightgray') if self.active else pygame.Color('gray')
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        return self.text
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = font1_.render(self.text, True, pygame.Color('white'))
            return None

        def update(self):
            width = max(200, self.txt_surface.get_width() + 10)
            self.rect.w = width

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


    class WorldSelectionMenu:
        def __init__(self):
            self.worlds = []
            self.scroll_offset = 0
            self.selected_world = None
            self.load_button = Button("Load", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, self.load_selected)
            self.back_button = Button("Back", 50, 50, 100, 40, self.back)
            self.refresh_worlds()

        def refresh_worlds(self):
            if not os.path.exists("saves"):
                os.makedirs("saves")
            self.worlds = [f for f in os.listdir("saves") if f.endswith(".trrm")]

        def back(self):
            global MENU, load_world_active
            MENU = True
            load_world_active = False

        def load_selected(self):
            global running, world_name
            if self.selected_world:
                world_name = self.selected_world.replace(".trrm", "")
                load_world(os.path.join("saves", self.selected_world))
                running = False

        def draw(self, screen):
            screen.blit(menu_background2, (0, 0))

            title = font1.render("Select World", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            self.back_button.draw(screen)

            visible_worlds = self.worlds[self.scroll_offset:self.scroll_offset + 5]
            for i, world in enumerate(visible_worlds):
                y_pos = 150 + i * 60
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 50)

                color = (100, 100, 100) if world != self.selected_world else (150, 150, 150)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)

                name = world.replace(".trrm", "")
                name_text = font1_.render(name, True, WHITE)
                screen.blit(name_text, (rect.x + 10, rect.y + 15))

            if len(self.worlds) > 5:
                if self.scroll_offset > 0:
                    pygame.draw.polygon(screen, WHITE, [
                        (SCREEN_WIDTH // 2, 130),
                        (SCREEN_WIDTH // 2 - 10, 140),
                        (SCREEN_WIDTH // 2 + 10, 140)
                    ])

                if self.scroll_offset < len(self.worlds) - 5:
                    pygame.draw.polygon(screen, WHITE, [
                        (SCREEN_WIDTH // 2, 450),
                        (SCREEN_WIDTH // 2 - 10, 440),
                        (SCREEN_WIDTH // 2 + 10, 440)
                    ])

            self.load_button.draw(screen)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.back_button.check_click(event.pos)
                self.load_button.check_click(event.pos)

                visible_worlds = self.worlds[self.scroll_offset:self.scroll_offset + 5]
                for i, world in enumerate(visible_worlds):
                    y_pos = 150 + i * 60
                    rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 50)
                    if rect.collidepoint(event.pos):
                        self.selected_world = world

                if event.button == 4:
                    if self.scroll_offset > 0:
                        self.scroll_offset -= 1
                elif event.button == 5:
                    if self.scroll_offset < len(self.worlds) - 5:
                        self.scroll_offset += 1


    class PauseMenu:
        def __init__(self):
            self.buttons = [
                Button("Resume", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, self.resume),
                Button("Main Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 50, self.main_menu),
                Button("Exit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50, self.exit_game)
            ]

        def resume(self):
            global PAUSED
            PAUSED = False

        def main_menu(self):
            global PAUSED, running, MENU
            save_map(world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y, player, SURVIVAL,
                     inventory_chest, chests, inventory.items, furnaces)
            PAUSED = False
            running = False
            MENU = True

        def exit_game(self):
            global running
            save_map(world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y, player, SURVIVAL,
                     inventory_chest, chests, inventory.items, furnaces)
            running = False

        def draw(self, screen):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            title = font1.render("Game Paused", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

            for button in self.buttons:
                button.draw(screen)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(event.pos)


    def damage_block(x, y):
        global world
        if SURVIVAL:
            key = (x, y)
            block_id = world[y][x][0]
            hardness = block_hardness.get(block_id, 1.0)

            if key not in damage_tracker:
                damage_tracker[key] = 0

            damage_tracker[key] += 0.5 / hardness

            if damage_tracker[key] >= len(destruction_textures):
                del damage_tracker[key]
                return 1
            return 0
        else:
            return 1


    def show_play_menu():
        global MENU
        MENU = False


    def play_game():
        global running, world, inventory, world_name, input_box, worldname_box

        inventory = Inventory()

        if input_box.text.isdecimal():
            sid = int(input_box.text)
        else:
            sid = random.randrange(11111111, 99999999)

        world_name = worldname_box.text.strip() or f"World_{int(time.time())}"

        world = generate_world(sid, screen)
        running = False


    def quit_game():
        pygame.quit()
        sys.exit()


    def open_settings():
        global Settings
        Settings = True


    def set_system_resolution(width, height):
        devmode = pywintypes.DEVMODEType()
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

        result = win32api.ChangeDisplaySettings(devmode, 0)
        if result == 0:
            # print(f"Resolution changed to {width}x{height}")
            pass
        else:
            print("Failed to change resolution")


    class Resolutions:
        def set_resolution(self, res):
            global RESOLUTION
            RESOLUTION = res
            print(f"Resolution set to: {RESOLUTION}")
            with open(os.path.join(BASE_DIR, "config.json"), "w") as file:
                data = json.dumps({
                    'resolution': [RESOLUTION[0], RESOLUTION[1]],
                    'fullscreen': True
                })
                file.write(data)
                file.close()
                del data


    def back():
        global Settings
        Settings = False


    def change_mode():
        global play_buttons, SURVIVAL
        if play_buttons[0].text == "Mode: Survival":
            play_buttons[0].text = "Mode: Creative"
            SURVIVAL = False
        else:
            play_buttons[0].text = "Mode: Survival"
            SURVIVAL = True


    def show_worlds():
        global load_world_active, MENU
        MENU = False
        load_world_active = True


    load_world_active = False

    res_obj = Resolutions()
    world_selection = WorldSelectionMenu()

    buttons = [
        Button("Play", 180, 200, 200, 50, show_play_menu),
        Button("Load World", 430, 200, 200, 50, show_worlds),
        # Button("Connect", 300, 300, 200, 50, conn_multiplayer_game),
        FakeButton("Connect", 300, 300, 200, 50),
        Button("Settings", 300, 400, 200, 50, open_settings),
        Button("Quit", 300, 500, 200, 50, quit_game)
    ]

    SURVIVAL = True

    play_buttons = [
        Button("Mode: Survival", 300, 200, 200, 50, change_mode),
        Button("Generate", 300, 500, 200, 50, play_game),
    ]
    input_box = InputBox(300, 350, 200, 50, "Enter SID")
    worldname_box = InputBox(300, 420, 200, 50, "Enter World Name")

    settings_buttons = [
        Button("Back", 50, 50, 150, 40, back),
        Button("VGA (640x480)", 50, 150, 330, 40, lambda: res_obj.set_resolution((640, 480))),
        Button("SVGA (800x600)", 50, 200, 330, 40, lambda: res_obj.set_resolution((800, 600))),
        Button("XGA (1024x768)", 50, 250, 330, 40, lambda: res_obj.set_resolution((1024, 768))),
        Button("HD (1280x720)", 50, 300, 330, 40, lambda: res_obj.set_resolution((1280, 720))),
        Button("WXGA (1366x768)", 400, 150, 330, 40, lambda: res_obj.set_resolution((1366, 768))),
        Button("HD+ (1600x900)", 400, 200, 330, 40, lambda: res_obj.set_resolution((1600, 900))),
        Button("Full HD (1920x1080)", 400, 250, 330, 40, lambda: res_obj.set_resolution((1920, 1080))),
        Button("QHD (2560x1440)", 400, 300, 330, 40, lambda: res_obj.set_resolution((2560, 1440))),
        Button("4K UHD (3840x2160)", 200, 350, 330, 40, lambda: res_obj.set_resolution((3840, 2160))),
    ]


    def save_map(world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y, player, SURVIVAL, inventory_chest,
                 chests, inventory_items, furnaces):
        global world_name
        if not os.path.exists("saves"):
            os.makedirs("saves")

        player_world_x = player.x - scroll_x
        player_world_y = player.y - scroll_y

        if not world_name:
            world_name = f"World_{int(time.time())}"

        save_path = os.path.join("saves", f"{world_name}.trrm")
        print(f"Saving to {save_path}...")

        with open(save_path, "wb") as file:
            pickle.dump(
                (world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y,
                 player_world_x, player_world_y, SURVIVAL, inventory_chest, chests,
                 inventory_items, furnaces, world_name), file)


    def load_world(filepath):
        global world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y, player, SURVIVAL, inventory_chest, chests, inventory, world_name, furnaces

        inventory = Inventory()

        with open(filepath, "rb") as file:
            try:
                data = pickle.load(file)
                print(f"Loading {filepath}...")

                if len(data) == 15:
                    world, torches, private_blocks, homes, GameMode, saved_scroll_x, saved_scroll_y, player_world_x, player_world_y, SURVIVAL, inventory_chest, chests, inventory.items, furnaces, world_name = data
                if len(data) == 14:
                    world, torches, private_blocks, homes, GameMode, saved_scroll_x, saved_scroll_y, player_world_x, player_world_y, SURVIVAL, inventory_chest, chests, inventory.items, world_name = data
                elif len(data) == 13:
                    world, torches, private_blocks, homes, GameMode, saved_scroll_x, saved_scroll_y, player_world_x, player_world_y, SURVIVAL, inventory_chest, chests, inventory.items = data
                    world_name = os.path.basename(filepath).replace(".trrm", "")
                elif len(data) == 10:
                    world, torches, private_blocks, homes, GameMode, saved_scroll_x, saved_scroll_y, player_world_x, player_world_y, SURVIVAL = data
                    world_name = os.path.basename(filepath).replace(".trrm", "")

                scroll_x = saved_scroll_x
                scroll_y = saved_scroll_y

                player.x = player_world_x + scroll_x
                player.y = player_world_y + scroll_y
            except (ValueError, EOFError) as e:
                print(f"Error loading world: {e}")


    running = True
    MENU = True
    while running:
        if Settings:
            screen.blit(menu_background2, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_ in settings_buttons:
                        button_.check_click(event.pos)

            for button3 in settings_buttons:
                button3.draw(screen)
        else:
            if MENU:
                screen.blit(menu_background, (0, 0))
                text_surf = font2.render("TERRMINE", True, BLACK)
                screen.blit(text_surf, (170, 80))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button2 in buttons:
                            button2.check_click(event.pos)

                for button1 in buttons:
                    button1.draw(screen)

            elif load_world_active == True:

                screen.blit(menu_background2, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        world_selection.handle_event(event)

                world_selection.draw(screen)
            else:
                screen.blit(menu_background2, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button in play_buttons:
                            button.check_click(event.pos)

                    worldname_box.handle_event(event)
                    input_box.handle_event(event)

                input_box.update()
                worldname_box.update()
                label_sid = font1.render("Enter SID", True, WHITE)
                label_world = font1.render("World Name", True, WHITE)

                screen.blit(label_sid, (500, 350))
                screen.blit(label_world, (500, 420))

                input_box.draw(screen)
                worldname_box.draw(screen)

                for button4 in play_buttons:
                    button4.draw(screen)

        pygame.display.flip()


    def check_ladder_collision(player, world, scroll_x, scroll_y):
        player_x = (player.x - scroll_x) // TILE_SIZE
        player_y = (player.y - scroll_y) // TILE_SIZE

        # for dx in [-1, 0, 1]:
        #     for dy in [-1, 0, 1]:
        #         tile_x = player_x + dx
        #         tile_y = player_y + dy
        #
        #         if 0 <= tile_x < len(world[0]) and 0 <= tile_y < len(world):
        #             if world[tile_y][tile_x] == 12:
        #                 return True
        try:
            if world[player_y][player_x][0] == 12:
                return True
        except IndexError:
            return False
        return False


    def check_crafting_result(grid):
        grid_tuple = tuple(tuple(row) for row in grid)

        for recipe_pattern, result in CRAFTING_RECIPES.items():
            match = True
            for y in range(3):
                for x in range(3):
                    grid_block = grid[y][x][0] if grid[y][x] else None
                    recipe_block = recipe_pattern[y][x]

                    if grid_block != recipe_block:
                        match = False
                        break
                if not match:
                    break

            if match:
                return result

        return None


    def check_inventory_crafting_result(grid):
        grid_tuple = tuple(tuple(row) for row in grid)

        for recipe_pattern, result in INVENTORY_CRAFTING_RECIPES.items():
            match = True
            for y in range(2):
                for x in range(2):
                    grid_block = grid[y][x][0] if grid[y][x] else None
                    recipe_block = recipe_pattern[y][x]

                    if grid_block != recipe_block:
                        match = False
                        break
                if not match:
                    break

            if match:
                return result

        return None


    def trigger_key():
        global CRAFTING_OPEN, console, current_open_chest
        if not console.is_open and not CRAFTING_OPEN and current_open_chest is None and not inventory_open and stats.health > 0:
            return True
        return False


    def get_chest_slot_rect(i):
        return pygame.Rect(
            chest_rect.x + 20 + (i % 6) * (TILE_SIZE + 10),
            chest_rect.y + 20 + (i // 6) * (TILE_SIZE + 10),
            TILE_SIZE, TILE_SIZE
        )


    def get_inventory_slot_rect(i):
        return pygame.Rect(
            50 + i * (TILE_SIZE + 5),
            SCREEN_HEIGHT - 50,
            TILE_SIZE,
            TILE_SIZE
        )


    def update_furnaces():
        global FPS
        for furnace in furnaces:
            if furnace["burn_time"] > 0:
                furnace["burn_time"] -= 1 / FPS
                if furnace["input"] and furnace["input"][0] in SMELT_RECIPES:
                    recipe = SMELT_RECIPES[furnace["input"][0]]
                    furnace["smelt_progress"] += 1 / FPS
                    if furnace["smelt_progress"] >= recipe["smelt_time"]:
                        furnace["input"][1] -= 1
                        if furnace["input"][1] <= 0:
                            furnace["input"] = None
                        if furnace["output"] is None or furnace["output"][0] == recipe["result"]:
                            if furnace["output"]:
                                furnace["output"][1] += 1
                            else:
                                furnace["output"] = [recipe["result"], 1]
                        furnace["smelt_progress"] = 0
            elif furnace["fuel"]:
                fuel_id = furnace["fuel"][0]
                if fuel_id in FUEL_BURN_TIMES:
                    furnace["burn_time"] = FUEL_BURN_TIMES[fuel_id]
                    furnace["fuel"][1] -= 1
                    if furnace["fuel"][1] <= 0:
                        furnace["fuel"] = None


    def draw_furnace_ui(screen, furnace):
        ui_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 200, 150)
        pygame.draw.rect(screen, (50, 50, 50), ui_rect)
        pygame.draw.rect(screen, WHITE, ui_rect, 2)

        input_rect = pygame.Rect(ui_rect.x + 20, ui_rect.y + 20, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (80, 80, 80), input_rect)
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        if furnace["input"]:
            screen.blit(textures[furnace["input"][0]], input_rect.topleft)
            qty_text = font1_.render(str(furnace["input"][1]), True, WHITE)
            screen.blit(qty_text, (input_rect.right - 12, input_rect.bottom - 18))

        fuel_rect = pygame.Rect(ui_rect.x + 20, ui_rect.y + 100, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (80, 80, 80), fuel_rect)
        pygame.draw.rect(screen, WHITE, fuel_rect, 2)
        if furnace["fuel"]:
            screen.blit(textures[furnace["fuel"][0]], fuel_rect.topleft)
            qty_text = font1_.render(str(furnace["fuel"][1]), True, WHITE)
            screen.blit(qty_text, (fuel_rect.right - 12, fuel_rect.bottom - 18))

        output_rect = pygame.Rect(ui_rect.x + 130, ui_rect.y + 65, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (80, 80, 80), output_rect)
        pygame.draw.rect(screen, WHITE, output_rect, 2)
        if furnace["output"]:
            screen.blit(textures[furnace["output"][0]], output_rect.topleft)
            qty_text = font1_.render(str(furnace["output"][1]), True, WHITE)
            screen.blit(qty_text, (output_rect.right - 12, output_rect.bottom - 18))

        arrow_x = ui_rect.x + 70
        arrow_y = ui_rect.y + 65

        if furnace["input"] and furnace["burn_time"] > 0:
            recipe = SMELT_RECIPES.get(furnace["input"][0])
            if recipe:
                progress = furnace["smelt_progress"] / recipe["smelt_time"]
                stage_index = 23 - int(progress * 22)
                stage_index = max(1, min(stage_index, 23))
                screen.blit(arrow_stages[stage_index - 1], (arrow_x, arrow_y))
        else:
            screen.blit(arrow_stages[22], (arrow_x, arrow_y))

        if furnace["burn_time"] > 0:
            burn_percent = furnace["burn_time"] / FUEL_BURN_TIMES.get(furnace["fuel"][0], 1)
            stage_index = int((1 - burn_percent) * (len(fire_stages) - 1))
            fire_img = fire_stages[stage_index]
            screen.blit(fire_img, (ui_rect.x + 20, ui_rect.y + 60))

        if dragging_item and dragging_pos:
            screen.blit(textures[dragging_item[0]],
                        (dragging_pos[0] - TILE_SIZE // 2, dragging_pos[1] - TILE_SIZE // 2))
            if dragging_item[1] > 1:
                qty_text = font1_.render(str(dragging_item[1]), True, WHITE)
                screen.blit(qty_text, (dragging_pos[0] + 5, dragging_pos[1] + 5))


    set_system_resolution(RESOLUTION[0], RESOLUTION[1])
    screen = pygame.display.set_mode(
        RESOLUTION,
        pygame.FULLSCREEN if settings["fullscreen"] else 0
    )
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    console = Console()
    pause_menu = PauseMenu()
    player_vel_y = 0
    gravity = 0.5
    jump_strength = -10
    grounded = False
    ZONE_RADIUS = 1
    LIGHT_RADIUS = 6
    clock = pygame.time.Clock()
    nearby_blocks = set()
    current_texture = player_textures["idle"]
    cycle = 1
    last_cycle_timer = time.time()
    rotate = False
    dynamites = []
    players = {}
    fall_distance = 0
    stats = PlayerStats()
    ActiveLayer = 1
    max_items_per_row = SCREEN_WIDTH // TILE_SIZE
    pygame.mouse.set_visible(False)
    cursor_img = pygame.image.load(os.path.join(BASE_DIR, "assets\\cursors\\cursor.png")).convert_alpha()
    CRAFTING_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 200)
    INVENTORY_CRAFTING_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 75, 200, 150)
    player_x = (player.x - scroll_x) // TILE_SIZE
    player_y = (player.y - scroll_y) // TILE_SIZE
    last_space_press_time = 0
    space_press_count = 0
    double_press_delay = 0.3

    running = True
    while running:

        fog_surface.fill((0, 0, 0, 0))
        screen.fill(BLUE)
        update_furnaces()

        # fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # fog_surface.fill(FOG_COLOR)
        light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and CRAFTING_OPEN:
                    CRAFTING_OPEN = False
                elif event.key == pygame.K_ESCAPE and inventory_open:
                    inventory_open = False
                elif event.key == pygame.K_ESCAPE and current_open_chest:
                    current_open_chest = None
                elif event.key == pygame.K_BACKQUOTE:
                    console.toggle()
                elif event.key == pygame.K_ESCAPE and FURNACE_OPEN:
                    FURNACE_OPEN = False
                    current_open_furnace = None
                elif event.key == pygame.K_e and trigger_key() and not console.is_open:
                    INVENTORY_CRAFTING_OPENED = not INVENTORY_CRAFTING_OPENED
                    CRAFTING_OPEN = False
                elif event.key == pygame.K_F10 and not console.is_open:
                    DEBUG_MENU = not DEBUG_MENU
                elif event.key == pygame.K_i and not console.is_open:
                    inventory_open = not inventory_open
                elif event.key == pygame.K_ESCAPE and not console.is_open and not CRAFTING_OPEN and not inventory_open and current_open_chest is None:
                    current_time = time.time()
                    if current_time - last_toggle_time >= cooldown_time:
                        PAUSED = not PAUSED
                        last_toggle_time = current_time
                elif event.key == pygame.K_SPACE:
                    current_time = time.time()
                    if current_time - last_space_press_time <= double_press_delay:
                        space_press_count += 1
                    else:
                        space_press_count = 1

                    last_space_press_time = current_time

                    if space_press_count == 2 and not SURVIVAL:
                        FLY = not FLY
                        player_vel_y = 0
                        space_press_count = 0

            if PAUSED:
                pause_menu.handle_event(event)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and not console.is_open and stats.health > 0:

                    if event.button == 4:
                        inventory.scroll(1)  # Scroll up
                        continue
                    elif event.button == 5:
                        inventory.scroll(-1)  # Scroll down
                        continue

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x = (mouse_x - scroll_x) // TILE_SIZE
                    world_y = (mouse_y - scroll_y) // TILE_SIZE

                    player_x = (player.x - scroll_x) // TILE_SIZE
                    player_y = (player.y - scroll_y) // TILE_SIZE

                    if event.button == 3:
                        if world[world_y][world_x][0] == 25:
                            CRAFTING_OPEN = not CRAFTING_OPEN
                            continue
                        elif world[world_y][world_x][0] == 52:
                            for chest in chests:
                                if chest["x"] == world_x and chest["y"] == world_y and chest["layer"] == ActiveLayer:
                                    current_open_chest = chest
                                    break
                            continue
                        elif world[world_y][world_x][0] == 53:
                            for furnace in furnaces:
                                if furnace["x"] == world_x and furnace["y"] == world_y and furnace["layer"] == ActiveLayer:
                                    current_open_furnace = furnace
                                    FURNACE_OPEN = True
                                    break
                            continue

                    if CRAFTING_OPEN and event.button == 1:
                        mx, my = pygame.mouse.get_pos()

                        for i, item_data in enumerate(visible_items):
                            item_index = inventory.scroll_index + i
                            item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                            if item_rect.collidepoint(mx, my):
                                dragging_item = inventory.items[item_index]
                                dragging_from_inventory = True
                                dragging_pos = (mx, my)
                                break

                        for y in range(3):
                            for x in range(3):
                                rect = pygame.Rect(CRAFTING_RECT.x + 40 + x * TILE_SIZE,
                                                   CRAFTING_RECT.y + 60 + y * TILE_SIZE,
                                                   TILE_SIZE, TILE_SIZE)
                                if rect.collidepoint(mx, my) and CRAFTING_GRID[y][x] is not None:
                                    dragging_item = CRAFTING_GRID[y][x]
                                    dragging_from_grid = True
                                    dragging_pos = (mx, my)
                                    CRAFTING_GRID[y][x] = None
                                    CRAFTING_OUTPUT = check_crafting_result(CRAFTING_GRID)
                                    break

                        output_rect = pygame.Rect(CRAFTING_RECT.x + 200, CRAFTING_RECT.y + 85, TILE_SIZE, TILE_SIZE)
                        if output_rect.collidepoint(mx, my) and CRAFTING_OUTPUT:
                            block_id, amount = CRAFTING_OUTPUT
                            inventory.append_new_item(block_id, amount)
                            CRAFTING_GRID[:] = [[None for _ in range(3)] for _ in range(3)]
                            CRAFTING_OUTPUT = None

                    if FURNACE_OPEN and current_open_furnace and event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        fx = SCREEN_WIDTH // 2 - 150
                        fy = SCREEN_HEIGHT // 2 - 75

                        input_rect = pygame.Rect(fx + 20, fy + 20, TILE_SIZE, TILE_SIZE)
                        fuel_rect = pygame.Rect(fx + 20, fy + 100, TILE_SIZE, TILE_SIZE)
                        output_rect = pygame.Rect(fx + 130, fy + 65, TILE_SIZE, TILE_SIZE)

                        furnace = current_open_furnace

                        # Output slot (take only)
                        if output_rect.collidepoint(mx, my):
                            if dragging_item is None and furnace["output"]:
                                dragging_item = furnace["output"]
                                furnace["output"] = None

                        # Input slot
                        elif input_rect.collidepoint(mx, my):
                            if dragging_item:
                                if dragging_item[0] in SMELT_RECIPES:  # Only allow smeltable items
                                    if furnace["input"] is None:
                                        furnace["input"] = [dragging_item[0], dragging_item[1]]
                                        dragging_item = None
                                    elif furnace["input"][0] == dragging_item[0]:
                                        total = furnace["input"][1] + dragging_item[1]
                                        transfer = min(64 - furnace["input"][1], dragging_item[1])
                                        furnace["input"][1] += transfer
                                        dragging_item[1] -= transfer
                                        if dragging_item[1] <= 0:
                                            dragging_item = None
                            else:
                                if furnace["input"]:
                                    dragging_item = [furnace["input"][0], furnace["input"][1]]
                                    furnace["input"] = None

                        # Fuel slot
                        elif fuel_rect.collidepoint(mx, my):
                            if dragging_item:
                                if dragging_item[0] in FUEL_BURN_TIMES:
                                    if furnace["fuel"] is None:
                                        furnace["fuel"] = [dragging_item[0], dragging_item[1]]
                                        dragging_item = None
                                    elif furnace["fuel"][0] == dragging_item[0]:
                                        total = furnace["fuel"][1] + dragging_item[1]
                                        transfer = min(64 - furnace["fuel"][1], dragging_item[1])
                                        furnace["fuel"][1] += transfer
                                        dragging_item[1] -= transfer
                                        if dragging_item[1] <= 0:
                                            dragging_item = None
                            else:
                                if furnace["fuel"]:
                                    dragging_item = [furnace["fuel"][0], furnace["fuel"][1]]
                                    furnace["fuel"] = None

                        # Inventory slots
                        visible_items = inventory.items[
                                        inventory.scroll_index:inventory.scroll_index + max_items_per_row]
                        inventory_y = SCREEN_HEIGHT - TILE_SIZE - 30
                        inventory_x = SCREEN_WIDTH // 2 - (len(visible_items) * TILE_SIZE) // 2

                        for i, item in enumerate(visible_items):
                            index = inventory.scroll_index + i
                            slot_rect = pygame.Rect(
                                inventory_x + i * TILE_SIZE,
                                inventory_y,
                                TILE_SIZE,
                                TILE_SIZE
                            )
                            if slot_rect.collidepoint(mx, my):
                                if dragging_item is None:
                                    if inventory.items[index][0] != 0:
                                        dragging_item = [inventory.items[index][0], inventory.items[index][1]]
                                        inventory.items[index] = [0, 0]
                                else:
                                    if inventory.items[index][0] == 0:
                                        inventory.items[index] = [dragging_item[0], dragging_item[1]]
                                        dragging_item = None
                                    elif inventory.items[index][0] == dragging_item[0]:
                                        total = inventory.items[index][1] + dragging_item[1]
                                        if total <= 64:
                                            inventory.items[index][1] = total
                                            dragging_item = None
                                        else:
                                            inventory.items[index][1] = 64
                                            dragging_item[1] = total - 64

                    elif event.type == pygame.MOUSEBUTTONDOWN and inventory_open:
                        mx, my = pygame.mouse.get_pos()

                        chest_x = SCREEN_WIDTH // 2 - (9 * TILE_SIZE) // 2
                        chest_y = SCREEN_HEIGHT // 2 - 100

                        for row in range(3):
                            for col in range(9):
                                slot_rect = pygame.Rect(
                                    chest_x + col * TILE_SIZE,
                                    chest_y + row * TILE_SIZE,
                                    TILE_SIZE,
                                    TILE_SIZE
                                )

                                if slot_rect.collidepoint(mx, my):
                                    item = inventory_chest[row][col]

                                    if event.button == 1:
                                        if dragging_item is None:
                                            if item and item[0] != 0:
                                                dragging_item = item
                                                inventory_chest[row][col] = [0, 0]
                                                dragging_from_chest = True
                                                dragging_from_inventory = False
                                        else:
                                            if item is None or item[0] == 0:
                                                inventory_chest[row][col] = dragging_item
                                                dragging_item = None
                                            elif item[0] == dragging_item[0]:
                                                total = item[1] + dragging_item[1]
                                                if total <= 64:
                                                    inventory_chest[row][col][1] = total
                                                    dragging_item = None
                                                else:
                                                    inventory_chest[row][col][1] = 64
                                                    dragging_item[1] = total - 64
                                            dragging_from_inventory = False
                                            dragging_from_chest = False

                                    elif event.button == 3:
                                        if dragging_item:
                                            if item is None or item[0] == 0:
                                                inventory_chest[row][col] = [dragging_item[0], 1]
                                                dragging_item[1] -= 1
                                                if dragging_item[1] <= 0:
                                                    dragging_item = None
                                            elif item[0] == dragging_item[0] and item[1] < 64:
                                                inventory_chest[row][col][1] += 1
                                                dragging_item[1] -= 1
                                                if dragging_item[1] <= 0:
                                                    dragging_item = None

                                elif event.button == 3:
                                    if dragging_item:
                                        try:
                                            if item[0] == 0:
                                                inventory.items[i] = [dragging_item[0], 1]
                                                dragging_item[1] -= 1
                                                if dragging_item[1] <= 0:
                                                    dragging_item = None
                                            elif item[0] == dragging_item[0]:
                                                inventory.items[i][1] += 1
                                                dragging_item[1] -= 1
                                                if dragging_item[1] <= 0:
                                                    dragging_item = None
                                        except TypeError:
                                            pass

                        visible_items = inventory.items[inventory.scroll_index:inventory.scroll_index + max_items_per_row]
                        inventory_y = SCREEN_HEIGHT - TILE_SIZE - 30
                        inventory_x = SCREEN_WIDTH // 2 - (len(visible_items) * TILE_SIZE) // 2

                        for i, item in enumerate(visible_items):
                            index = inventory.scroll_index + i

                            slot_rect = pygame.Rect(
                                inventory_x + i * TILE_SIZE,
                                inventory_y,
                                TILE_SIZE,
                                TILE_SIZE
                            )

                            if slot_rect.collidepoint(mx, my):
                                if event.button == 1:
                                    if dragging_item is None:
                                        if item[0] != 0:
                                            dragging_item = item
                                            inventory.items[index] = [0, 0]
                                            dragging_from_inventory = True
                                            dragging_from_chest = False
                                    else:
                                        if item[0] == 0:
                                            inventory.items[index] = dragging_item
                                            dragging_item = None
                                        elif item[0] == dragging_item[0]:
                                            total = item[1] + dragging_item[1]
                                            if total <= 64:
                                                inventory.items[index][1] = total
                                                dragging_item = None
                                            else:
                                                inventory.items[index][1] = 64
                                                dragging_item[1] = total - 64
                                        dragging_from_chest = False
                                        dragging_from_inventory = False

                                elif event.button == 3:
                                    if dragging_item:
                                        if item[0] == 0:
                                            inventory.items[index] = [dragging_item[0], 1]
                                            dragging_item[1] -= 1
                                            if dragging_item[1] <= 0:
                                                dragging_item = None
                                        elif item[0] == dragging_item[0]:
                                            inventory.items[index][1] += 1
                                            dragging_item[1] -= 1
                                            if dragging_item[1] <= 0:
                                                dragging_item = None

                    elif current_open_chest and event.button == 1:
                        mx, my = pygame.mouse.get_pos()

                        for i in range(18):
                            rect = get_chest_slot_rect(i)
                            if rect.collidepoint(mx, my):
                                shift_held = pygame.key.get_mods() & pygame.KMOD_SHIFT
                                chest_item = current_open_chest["items"][i]

                                if shift_held:
                                    for j in range(len(inventory.items)):
                                        inv_item = inventory.items[j]
                                        if inv_item[0] == 0:
                                            inventory.items[j] = chest_item
                                            current_open_chest["items"][i] = [0, 0]
                                            break
                                        elif inv_item[0] == chest_item[0] and inv_item[1] < 64:
                                            space = 64 - inv_item[1]
                                            transfer = min(space, chest_item[1])
                                            inventory.items[j][1] += transfer
                                            current_open_chest["items"][i][1] -= transfer
                                            if current_open_chest["items"][i][1] <= 0:
                                                current_open_chest["items"][i] = [0, 0]
                                            break
                                elif chest_item[0] != 0:
                                    dragging_item = chest_item
                                    current_open_chest["items"][i] = [0, 0]
                                    dragging_from_chest = True
                                    dragging_pos = (mx, my)
                                break

                        if not dragging_item:
                            for i, item_data in enumerate(visible_items):
                                item_index = inventory.scroll_index + i
                                item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                                if item_rect.collidepoint(mx, my):
                                    dragging_item = inventory.items[item_index]
                                    inventory.items[item_index] = [0, 0]
                                    dragging_from_inventory = True
                                    dragging_pos = (mx, my)
                                    break

                    elif INVENTORY_CRAFTING_OPENED and event.button == 1:
                        mx, my = pygame.mouse.get_pos()

                        for i, item_data in enumerate(visible_items):
                            item_index = inventory.scroll_index + i
                            item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                            if item_rect.collidepoint(mx, my):
                                dragging_item = inventory.items[item_index]
                                dragging_from_inventory = True
                                dragging_pos = (mx, my)
                                break

                        for y in range(2):
                            for x in range(2):
                                rect = pygame.Rect(
                                    INVENTORY_CRAFTING_RECT.x + 30 + x * TILE_SIZE,
                                    INVENTORY_CRAFTING_RECT.y + 40 + y * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE
                                )
                                if rect.collidepoint(mx, my) and INVENTORY_CRAFTING_GRID[y][x] is not None:
                                    dragging_item = INVENTORY_CRAFTING_GRID[y][x]
                                    dragging_from_grid = True
                                    dragging_pos = (mx, my)
                                    INVENTORY_CRAFTING_GRID[y][x] = None
                                    inventory_output = check_inventory_crafting_result(INVENTORY_CRAFTING_GRID)
                                    break

                        out_rect = pygame.Rect(INVENTORY_CRAFTING_RECT.x + 155, INVENTORY_CRAFTING_RECT.y + 65, TILE_SIZE,
                                               TILE_SIZE)
                        if out_rect.collidepoint(mx, my) and inventory_output:
                            block_id, amount = inventory_output
                            inventory.append_new_item(block_id, amount)
                            INVENTORY_CRAFTING_GRID[:] = [[None for _ in range(2)] for _ in range(2)]
                            inventory_output = None

                    elif event.button != 1 and (
                            not INVENTORY_CRAFTING_OPENED or not CRAFTING_OPEN or not current_open_chest is None):
                        if world_x == player_x and world_y == player_y:
                            continue

                        distance = math.sqrt((world_x - player_x) ** 2 + (world_y - player_y) ** 2)

                        if distance > 4:
                            break

                        block_to_place = inventory.get_selected_block()

                        block_nearby = False
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                nx = world_x + dx
                                ny = world_y + dy
                                if 0 <= nx < COLS and 0 <= ny < ROWS:
                                    if not world[ny][nx][0] in [0, 100500]:
                                        block_nearby = True
                                        break
                            if block_nearby:
                                break

                        can_place = True
                        for pb_x, pb_y, owner, layer in private_blocks:
                            if abs(world_x - pb_x) <= 10 and abs(world_y - pb_y) <= 10 and owner != NAME:
                                can_place = False
                                break

                        if world[world_y][world_x][0] == 54:
                            world[world_y][world_x][1] = 2
                            world[world_y][world_x][0] = 55
                        elif world[world_y][world_x][0] == 55:
                            world[world_y][world_x][1] = 1
                            world[world_y][world_x][0] = 54

                        try:
                            if block_nearby and world[world_y][world_x][0] in [0, 100500]:
                                if not block_to_place in [38, 39, 40, 41, 42, 43, 44, 48, 50]:
                                    if block_to_place == 11:
                                        torches.append((world_x, world_y, ActiveLayer))
                                    elif block_to_place == 13:

                                        dynamites.append(Dynamite(world_x, world_y, ActiveLayer))
                                    elif block_to_place == 14:
                                        private_blocks.append((world_x, world_y, NAME, ActiveLayer))

                                    if block_to_place == 52:
                                        chests.append({
                                            "x": world_x,
                                            "y": world_y,
                                            "layer": ActiveLayer,
                                            "items": [[0, 0] for _ in range(18)]
                                        })

                                    if block_to_place == 53:
                                        furnaces.append({
                                            "x": world_x,
                                            "y": world_y,
                                            "layer": ActiveLayer,
                                            "fuel": None,
                                            "input": None,
                                            "output": None,
                                            "burn_time": 0,
                                            "smelt_progress": 0
                                        })

                                    if block_to_place != 13:
                                        world[world_y][world_x][0] = block_to_place
                                        if block_to_place != 54:
                                            world[world_y][world_x][1] = ActiveLayer
                                        else:
                                            world[world_y][world_x][1] = 1

                                    if SURVIVAL and block_to_place not in [0, 100500]:
                                        inventory.delete_block(block_to_place)
                        except IndexError:
                            pass

                elif event.type == pygame.MOUSEBUTTONUP and dragging_item is not None and not inventory_open:
                    if CRAFTING_OPEN:
                        mx, my = pygame.mouse.get_pos()

                        for y in range(3):
                            for x in range(3):
                                rect = pygame.Rect(CRAFTING_RECT.x + 40 + x * TILE_SIZE,
                                                   CRAFTING_RECT.y + 60 + y * TILE_SIZE,
                                                   TILE_SIZE, TILE_SIZE)
                                if rect.collidepoint(mx, my):
                                    if dragging_from_inventory:
                                        if CRAFTING_GRID[y][x] is None:
                                            CRAFTING_GRID[y][x] = (dragging_item[0], 1)
                                            inventory.delete_block(dragging_item[0], 1)
                                    elif dragging_from_grid:
                                        if CRAFTING_GRID[y][x] is None:
                                            CRAFTING_GRID[y][x] = dragging_item
                                    break

                        for i, item_data in enumerate(visible_items):
                            item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                            if item_rect.collidepoint(mx, my) and dragging_from_grid:
                                inventory.append_new_item(dragging_item[0], 1)
                                break

                        CRAFTING_OUTPUT = check_crafting_result(CRAFTING_GRID)
                        dragging_item = None
                        dragging_from_inventory = False
                        dragging_from_grid = False

                    elif current_open_chest and dragging_item:
                        mx, my = pygame.mouse.get_pos()

                        for i in range(18):
                            rect = get_chest_slot_rect(i)
                            if rect.collidepoint(mx, my):
                                slot = current_open_chest["items"][i]

                                if slot[0] == 0:
                                    current_open_chest["items"][i] = dragging_item
                                    dragging_item = None
                                elif slot[0] == dragging_item[0] and slot[1] < 64:
                                    space = 64 - slot[1]
                                    to_add = min(space, dragging_item[1])
                                    current_open_chest["items"][i][1] += to_add
                                    dragging_item[1] -= to_add
                                    if dragging_item[1] <= 0:
                                        dragging_item = None
                                break

                        for i, slot in enumerate(visible_items):
                            item_index = inventory.scroll_index + i
                            item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                            if item_rect.collidepoint(mx, my):
                                if inventory.items[item_index][0] == 0:
                                    inventory.items[item_index] = dragging_item
                                elif inventory.items[item_index][0] == dragging_item[0] and inventory.items[item_index][
                                    1] < 64:
                                    space = 64 - inventory.items[item_index][1]
                                    transfer = min(space, dragging_item[1])
                                    inventory.items[item_index][1] += transfer
                                    dragging_item[1] -= transfer
                                    if dragging_item[1] <= 0:
                                        dragging_item = None
                                        break
                                break

                        dragging_item = None
                        dragging_from_inventory = False
                        dragging_from_grid = False
                        dragging_from_chest = False

                    elif INVENTORY_CRAFTING_OPENED:
                        mx, my = pygame.mouse.get_pos()

                        for y in range(2):
                            for x in range(2):
                                rect = pygame.Rect(
                                    INVENTORY_CRAFTING_RECT.x + 30 + x * TILE_SIZE,
                                    INVENTORY_CRAFTING_RECT.y + 40 + y * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE
                                )
                                if rect.collidepoint(mx, my):
                                    if dragging_from_inventory:
                                        if INVENTORY_CRAFTING_GRID[y][x] is None:
                                            INVENTORY_CRAFTING_GRID[y][x] = (dragging_item[0], 1)
                                            inventory.delete_block(dragging_item[0], 1)
                                    elif dragging_from_grid:
                                        if INVENTORY_CRAFTING_GRID[y][x] is None:
                                            INVENTORY_CRAFTING_GRID[y][x] = dragging_item
                                    break

                        for i, item_data in enumerate(visible_items):
                            item_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)
                            if item_rect.collidepoint(mx, my) and dragging_from_grid:
                                inventory.append_new_item(dragging_item[0], 1)
                                break

                        inventory_output = check_inventory_crafting_result(INVENTORY_CRAFTING_GRID)
                        dragging_item = None
                        dragging_from_inventory = False
                        dragging_from_grid = False

                    elif event.type == pygame.MOUSEBUTTONUP and dragging_item is not None:
                        if FURNACE_OPEN:
                            if (not input_rect.collidepoint(event.pos) and
                                    not fuel_rect.collidepoint(event.pos) and
                                    not output_rect.collidepoint(event.pos)):
                                inventory.append_new_item(dragging_item[0], dragging_item[1])
                                dragging_item = None

                elif event.type == pygame.MOUSEMOTION and dragging_item is not None:
                    dragging_pos = event.pos

                elif not event.type == pygame.MOUSEBUTTONDOWN and stats.health > 0:
                    damage_tracker.clear()

                elif event.type == pygame.MOUSEWHEEL and trigger_key:
                    if len(inventory.items) > max_items_per_row:
                        if event.y > 0:
                            inventory.scroll_index = max(0, inventory.scroll_index - 1)
                        else:
                            max_scroll = len(inventory.items) - max_items_per_row
                            inventory.scroll_index = min(max_scroll, inventory.scroll_index + 1)
                    inventory.scroll(1 if event.y > 0 else -1)

                if trigger_key:
                    console.handle_event(event)
                    continue

        keys = pygame.key.get_pressed()
        player_movement = [0, 0]
        if keys[pygame.K_t] and trigger_key and not inventory_open:
            current_time = time.time()
            if current_time - last_toggle_time >= cooldown_time:
                ActiveLayer = 1 if ActiveLayer + 1 > 2 else ActiveLayer + 1
                last_toggle_time = current_time

        # if keys[pygame.K_p] and current_open_chest is None and trigger_key and not inventory_open:
        #     save_map(world, torches, private_blocks, homes, GameMode, scroll_x, scroll_y, player, SURVIVAL, inventory_chest, chests, inventory.items)

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and current_open_chest is None and trigger_key and not inventory_open:
            player_movement[0] -= 5
            rotate = True

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and current_open_chest is None and trigger_key and not inventory_open:
            player_movement[0] += 5
            rotate = False

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[
            pygame.K_UP]) and current_open_chest is None and trigger_key and not inventory_open:
            if not FLY:
                if grounded:
                    player_vel_y = jump_strength
                    grounded = False
            else:
                player_movement[1] -= 5

        if (keys[pygame.K_s] or keys[
            pygame.K_DOWN]) and FLY and current_open_chest is None and trigger_key and not inventory_open:
            player_movement[1] += 5

        if check_ladder_collision(player, world, scroll_x, scroll_y):
            if keys[pygame.K_UP] or keys[pygame.K_w] and trigger_key:
                player_movement[1] -= 5  # Move up
            elif keys[pygame.K_DOWN] or keys[pygame.K_s] and trigger_key:
                player_movement[1] += 5  # Move down
        else:
            if not FLY:
                if not grounded and time.time() - IMMNUNE_TIMER < 0:
                    fall_distance += abs(player_vel_y)

                player_vel_y += gravity
            player_movement[1] += player_vel_y

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and stats.health > 0 and trigger_key and current_open_chest is None and not inventory_open:
            if abs(world_x - player_x) <= ZONE_RADIUS and abs(world_y - player_y) <= ZONE_RADIUS:
                for dx in range(ZONE_RADIUS - 1, ZONE_RADIUS):
                    for dy in range(ZONE_RADIUS - 1, ZONE_RADIUS):

                        can_destroy = True
                        for pb_x, pb_y, owner, layer in private_blocks:
                            if abs(world_x - pb_x) <= 10 and abs(world_y - pb_y) <= 10 and owner != NAME:
                                can_destroy = False
                                break

                        if not can_destroy:
                            # console.history.append("You can't destroy blocks in this protected area!")
                            pass
                        else:
                            nx = world_x + dx
                            ny = world_y + dy

                            if 0 <= nx < COLS and 0 <= ny < ROWS:
                                dist = math.sqrt(dx ** 2 + dy ** 2)
                                if dist <= 4:
                                    if world[ny][nx][0] != 0 and world[ny][nx][1] == ActiveLayer and (
                                            GOD or world[ny][nx][0] != 100):
                                        dstr = damage_block(nx, ny)
                                        if dstr == 1:
                                            if world[ny][nx][0] in [31, 32, 33, 34, 35, 36, 37]:
                                                inventory.append_new_item(world[ny][nx][0] + 7)
                                            elif world[ny][nx][0] == 3:
                                                inventory.append_new_item(47)
                                            else:
                                                inventory.append_new_item(world[ny][nx][0])

                                            torch_positions = set(torches)
                                            for pb in torch_positions:
                                                pb_x, pb_y, layer = pb
                                                if pb_x == nx and pb_y == ny:
                                                    torches.remove(pb)
                                                    break

                                            for pb in private_blocks:
                                                pb_x, pb_y, owner, layer = pb
                                                if pb_x == nx and pb_y == ny:
                                                    private_blocks.remove(pb)
                                                    # console.history.append(f"Removed private block at {nx}, {ny}")
                                                    break

                                            if world[ny][nx][0] != 13:
                                                world[ny][nx][0] = 100500
                                                world[ny][nx][1] = 1

        if player_vel_y == 0.5 and player_movement[0] == 0:
            current_texture = player_textures["idle"]
            cycle = 1
        elif player_movement[0] != 0 and player_movement[1] == 0.5:
            current_texture = player_textures[f"walk-{cycle}"]
            if time.time() - last_cycle_timer > 0.1:
                cycle += 1
                last_cycle_timer = time.time()

            if cycle > 4:
                cycle = 1
        elif player_vel_y < 0.5:
            current_texture = player_textures["jump"]
        elif player_vel_y > 0:
            current_texture = player_textures["down"]

        start_x = max(0, -scroll_x // TILE_SIZE)
        end_x = min(COLS, (SCREEN_WIDTH - scroll_x) // TILE_SIZE + 1)
        start_y = max(0, -scroll_y // TILE_SIZE)
        end_y = min(ROWS, (SCREEN_HEIGHT - scroll_y) // TILE_SIZE + 1)

        player.y += player_movement[1]

        grounded = False

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                dist = math.dist((player.x, player.y), (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
                if dist < TILE_SIZE * 5:
                    nearby_blocks.add((x, y))

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                try:
                    tile = world[y][x][0]
                    if tile == 0:
                        continue

                    block_rect = pygame.Rect(x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y, TILE_SIZE, TILE_SIZE)
                    block_x, block_y = block_rect.topleft

                    is_exposed = all(world[i][x][0] in [0, 100500] for i in range(y))
                    player_dist = math.dist((player.centerx, player.centery), (block_x, block_y))
                    in_light_radius = dist <= LIGHT_RADIUS * TILE_SIZE

                    if player_dist <= LIGHT_RADIUS * TILE_SIZE:
                        in_light_radius = True

                    for torch_x, torch_y, layer in torches:
                        torch_dist = math.dist(
                            (torch_x * TILE_SIZE + scroll_x, torch_y * TILE_SIZE + scroll_y),
                            (block_x, block_y)
                        )

                        if torch_dist <= LIGHT_RADIUS * TILE_SIZE:
                            in_light_radius = True
                            break

                    if is_exposed or in_light_radius:
                        if tile in textures and tile != 13:
                            if world[y][x][1] == 1 or world[y][x][0] == 55:
                                screen.blit(textures[tile], block_rect)
                            elif world[y][x][1] != 3:
                                screen.blit(grayscale_textures[tile], block_rect)

                            key = (x, y)
                            if key in damage_tracker and damage_tracker[key] > 0:
                                screen.blit(destruction_textures[round(damage_tracker[key] - 1)], block_rect)

                    elif not is_exposed:
                        pygame.draw.rect(fog_surface, FOG_COLOR, block_rect)

                    if not NoClip:
                        if not block_rect.x in nearby_blocks and not block_rect.x in nearby_blocks:
                            if tile not in [100500, 11, 12, 29, 30] and world[y][x][1] in [1,3]:
                                if tile == 54:
                                    trapdoor_rect = pygame.Rect(
                                        block_rect.x,
                                        block_rect.y,
                                        TILE_SIZE,
                                        10
                                    )
                                    if player.colliderect(trapdoor_rect):
                                        if player_movement[1] > 0:
                                            player.bottom = trapdoor_rect.top
                                            player_vel_y = 0
                                            grounded = True
                                        elif player_movement[1] < 0:
                                            player.top = trapdoor_rect.bottom
                                            player_vel_y = 0
                                        elif player_movement[0] > 0:
                                            player.right = trapdoor_rect.left
                                        elif player_movement[0] < 0:
                                            player.left = trapdoor_rect.right
                                else:
                                    if player.colliderect(block_rect):
                                        if player_movement[1] > 0:
                                            player.bottom = block_rect.top
                                            player_vel_y = 0
                                            grounded = True
                                        elif player_movement[1] < 0:
                                            player.top = block_rect.bottom
                                            player_vel_y = 0
                                        elif player_movement[0] > 0:
                                            player.right = block_rect.left
                                        elif player_movement[0] < 0:
                                            player.left = block_rect.right

                except IndexError:
                    pass

        player.x += player_movement[0]

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                try:
                    tile = world[y][x][0]
                    if tile == 0:
                        continue

                    block_rect = pygame.Rect(x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y, TILE_SIZE, TILE_SIZE)

                    if not NoClip:
                        if not block_rect.x in nearby_blocks and not block_rect.x in nearby_blocks:
                            if player.colliderect(block_rect) and tile not in [100500, 11, 12, 29, 30] and world[y][x][1] in [1, 3]:
                                if player_movement[0] > 0:
                                    player.right = block_rect.left
                                elif player_movement[0] < 0:
                                    player.left = block_rect.right
                except IndexError:
                    pass

        screen.blit(fog_surface, (0, 0))

        if player.x > SCREEN_WIDTH // 2:
            scroll_x -= player.x - SCREEN_WIDTH // 2
            player.x = SCREEN_WIDTH // 2

        if player.x < SCREEN_WIDTH // 2:
            scroll_x -= player.x - SCREEN_WIDTH // 2
            player.x = SCREEN_WIDTH // 2

        if player.y > SCREEN_HEIGHT // 2:
            scroll_y -= player.y - SCREEN_HEIGHT // 2
            player.y = SCREEN_HEIGHT // 2

        if player.y < SCREEN_HEIGHT // 2:
            scroll_y -= player.y - SCREEN_HEIGHT // 2
            player.y = SCREEN_HEIGHT // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = (mouse_x - scroll_x) // TILE_SIZE
        world_y = (mouse_y - scroll_y) // TILE_SIZE

        try:
            if 0 <= world_x < COLS and 0 <= world_y < ROWS:
                # highlight_rect = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                # highlight_rect.fill((255, 255, 255, 100))
                # screen.blit(highlight_rect, (world_x * TILE_SIZE + scroll_x, world_y * TILE_SIZE + scroll_y))
                screen.blit(crosshair, (world_x * TILE_SIZE + scroll_x, world_y * TILE_SIZE + scroll_y))
        except IndexError:
            pass

        if not inventory_open:
            inventory_width = min(len(inventory.items), SCREEN_WIDTH // TILE_SIZE) * TILE_SIZE
            inventory_x = (SCREEN_WIDTH - inventory_width) // 2
            inventory_y = SCREEN_HEIGHT - 60

            visible_items = inventory.items[inventory.scroll_index:inventory.scroll_index + max_items_per_row]

            for i, item_data in enumerate(visible_items):
                item_index = inventory.scroll_index + i
                block_id, quantity = item_data
                inventory_rect = pygame.Rect(inventory_x + i * TILE_SIZE, inventory_y, TILE_SIZE, TILE_SIZE)

                if block_id in textures:
                    screen.blit(textures[block_id], inventory_rect)

                if quantity > 1 and block_id not in [0, 100500]:
                    quantity_text = font1_.render(str(quantity), True, WHITE)
                    screen.blit(quantity_text, (inventory_rect.x + 4, inventory_rect.y + TILE_SIZE - 18))

                pygame.draw.rect(screen, WHITE, inventory_rect, 2)

                if item_index == inventory.selected_index:
                    pygame.draw.rect(screen, (255, 0, 0), inventory_rect, 3)

        if SafeZone:
            for pb_x, pb_y, owner, layer in private_blocks:
                top_left_x = (pb_x - 10) * TILE_SIZE + scroll_x
                top_left_y = (pb_y - 10) * TILE_SIZE + scroll_y

                width = 21 * TILE_SIZE
                height = 21 * TILE_SIZE

                pygame.draw.rect(screen, (255, 0, 0), (top_left_x, top_left_y, width, height), width=9)

        stats.draw_ui(screen)

        layer_text = layer_font.render(f"Layer:{ActiveLayer}", True, pygame.Color('white'))

        screen.blit(layer_text, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT - 90))

        if rotate:
            screen.blit(pygame.transform.flip(current_texture, True, False), player)
        else:
            screen.blit(current_texture, player)

        for dynamite in dynamites:
            dynamite.update(world)
            dynamite.draw(screen, textures)

        if time.time() - IMMNUNE_TIMER < 10:
            screen.blit(shield, (player.x - 16, player.y - 16))

        text = font1.render(VERSION, True, WHITE)
        screen.blit(text, (0, SCREEN_HEIGHT - 40))

        console.draw(screen)

        if stats.health <= 0:
            screen.blit(dead, (0, 0))

        if CRAFTING_OPEN:
            pygame.draw.rect(screen, (184, 191, 204, 200), CRAFTING_RECT)

            for y in range(3):
                for x in range(3):
                    rect = pygame.Rect(CRAFTING_RECT.x + 40 + x * TILE_SIZE, CRAFTING_RECT.y + 60 + y * TILE_SIZE,
                                       TILE_SIZE, TILE_SIZE)
                    item = CRAFTING_GRID[y][x]
                    if item:
                        screen.blit(textures[item[0]], rect)

                    pygame.draw.rect(screen, WHITE, rect, 2)

            pygame.draw.rect(screen, WHITE, (CRAFTING_RECT.x + 195, CRAFTING_RECT.y + 80, 40, 40), 2)

            if dragging_item is not None and dragging_pos:
                try:
                    screen.blit(textures[dragging_item[0]],
                                (dragging_pos[0] - TILE_SIZE // 2, dragging_pos[1] - TILE_SIZE // 2))
                except KeyError:
                    pass

            out_rect = pygame.Rect(CRAFTING_RECT.x + 200, CRAFTING_RECT.y + 85, TILE_SIZE, TILE_SIZE)
            if CRAFTING_OUTPUT:
                screen.blit(textures[CRAFTING_OUTPUT[0]], out_rect)
                qty_text = font1_.render(str(CRAFTING_OUTPUT[1]), True, WHITE)
                screen.blit(qty_text, (out_rect.x + 3, out_rect.y + TILE_SIZE - 17))
                pygame.draw.rect(screen, WHITE, out_rect, 2)

                if out_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (0, 255, 0, 100), out_rect, 3)

        if INVENTORY_CRAFTING_OPENED:
            pygame.draw.rect(screen, (184, 191, 204, 200), INVENTORY_CRAFTING_RECT)

            for y in range(2):
                for x in range(2):
                    rect = pygame.Rect(
                        INVENTORY_CRAFTING_RECT.x + 30 + x * TILE_SIZE,
                        INVENTORY_CRAFTING_RECT.y + 40 + y * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE
                    )
                    item = INVENTORY_CRAFTING_GRID[y][x]
                    if item:
                        screen.blit(textures[item[0]], rect)

                    pygame.draw.rect(screen, WHITE, rect, 2)

            pygame.draw.rect(screen, WHITE, (INVENTORY_CRAFTING_RECT.x + 150, INVENTORY_CRAFTING_RECT.y + 60, 40, 40),
                             2)

            inventory_output = check_inventory_crafting_result(INVENTORY_CRAFTING_GRID)

            out_rect = pygame.Rect(INVENTORY_CRAFTING_RECT.x + 155, INVENTORY_CRAFTING_RECT.y + 65, TILE_SIZE,
                                   TILE_SIZE)
            if inventory_output:
                screen.blit(textures[inventory_output[0]], out_rect)
                qty_text = font1_.render(str(inventory_output[1]), True, WHITE)
                screen.blit(qty_text, (out_rect.x + 3, out_rect.y + TILE_SIZE - 17))

                if out_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (0, 255, 0, 100), out_rect, 3)

            if dragging_item is not None and dragging_pos:
                try:
                    screen.blit(textures[dragging_item[0]],
                                (dragging_pos[0] - TILE_SIZE // 2, dragging_pos[1] - TILE_SIZE // 2))
                except KeyError:
                    pass

        if current_open_chest:
            chest_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 300, 150)
            pygame.draw.rect(screen, (50, 50, 50), chest_rect)
            pygame.draw.rect(screen, WHITE, chest_rect, 3)

            for i in range(18):
                item = current_open_chest["items"][i]
                slot_rect = get_chest_slot_rect(i)

                pygame.draw.rect(screen, (80, 80, 80), slot_rect)
                pygame.draw.rect(screen, WHITE, slot_rect, 2)

                if item[0] != 0:
                    screen.blit(textures[item[0]], slot_rect)
                    if item[1] > 1:
                        amt_surf = font1_.render(str(item[1]), True, WHITE)
                        screen.blit(amt_surf, (slot_rect.right - 12, slot_rect.bottom - 18))

            if dragging_item and dragging_pos:
                try:
                    screen.blit(textures[dragging_item[0]],
                                (dragging_pos[0] - TILE_SIZE // 2, dragging_pos[1] - TILE_SIZE // 2))
                    if dragging_item[1] > 1:
                        amt_surf = font1_.render(str(dragging_item[1]), True, WHITE)
                        screen.blit(amt_surf, (dragging_pos[0] + 12, dragging_pos[1] + 12))
                except KeyError:
                    pass

        if inventory_open:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))

            chest_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - (9 * TILE_SIZE) // 2,
                SCREEN_HEIGHT // 2 - 100,
                9 * TILE_SIZE,
                3 * TILE_SIZE
            )
            pygame.draw.rect(screen, (59, 47, 47), chest_rect)
            pygame.draw.rect(screen, (100, 100, 100), chest_rect, 3)

            chest_label = font1_.render("Inventory Chest", True, WHITE)
            screen.blit(chest_label, (chest_rect.x, chest_rect.y - 30))

            for row in range(3):
                for col in range(9):
                    selected_item = (row, col)
                    slot_rect = pygame.Rect(
                        chest_rect.x + col * TILE_SIZE,
                        chest_rect.y + row * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    pygame.draw.rect(screen, (80, 80, 80), slot_rect)
                    pygame.draw.rect(screen, (150, 150, 150), slot_rect, 2)

                    item = inventory_chest[row][col]
                    if item and item[0] != 0:
                        screen.blit(textures[item[0]], slot_rect.topleft)
                        if item[1] > 1:
                            qty_text = font1_.render(str(item[1]), True, WHITE)
                            screen.blit(qty_text, (
                                slot_rect.right - qty_text.get_width() - 2,
                                slot_rect.bottom - qty_text.get_height() - 2
                            ))

                    pygame.draw.rect(screen, (255, 255, 255), slot_rect, 1)

            visible_items = inventory.items[inventory.scroll_index:inventory.scroll_index + max_items_per_row]
            inventory_y = SCREEN_HEIGHT - TILE_SIZE - 30
            inventory_x = SCREEN_WIDTH // 2 - (len(visible_items) * TILE_SIZE) // 2

            for i, item in enumerate(visible_items):
                slot_rect = pygame.Rect(
                    inventory_x + i * TILE_SIZE,
                    inventory_y,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pygame.draw.rect(screen, (80, 80, 80), slot_rect)
                pygame.draw.rect(screen, (150, 150, 150), slot_rect, 2)

                if item[0] != 0 and item[0] != 100500:
                    screen.blit(textures[item[0]], slot_rect.topleft)
                    if item[1] > 1:
                        qty_text = font1_.render(str(item[1]), True, WHITE)
                        screen.blit(qty_text, (
                            slot_rect.right - qty_text.get_width() - 2,
                            slot_rect.bottom - qty_text.get_height() - 2
                        ))

                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 2)

                if inventory.selected_index == i + inventory.scroll_index:
                    pygame.draw.rect(screen, (255, 0, 0), slot_rect, 2)

        if dragging_item and dragging_pos:
            try:
                screen.blit(
                    textures[dragging_item[0]],
                    (dragging_pos[0] - TILE_SIZE // 2, dragging_pos[1] - TILE_SIZE // 2)
                )
                if dragging_item[1] > 1:
                    qty_text = font1_.render(str(dragging_item[1]), True, WHITE)
                    screen.blit(qty_text, (dragging_pos[0] + 5, dragging_pos[1] + 5))
            except KeyError:
                pass

        if DEBUG_MENU:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x = (mouse_x - scroll_x) // TILE_SIZE
            tile_y = (mouse_y - scroll_y) // TILE_SIZE

            debug_font = pygame.font.SysFont("consolas", 18)

            fps = int(clock.get_fps())
            world_seed = seed
            player_tile_x = (player.x - scroll_x) // TILE_SIZE
            player_tile_y = (player.y - scroll_y) // TILE_SIZE

            debug_lines = [
                f"FPS: {fps}",
                f"Seed: {world_seed}",
                f"Player Pos (tile): {player_tile_x}, {player_tile_y}",
                f"Target Block (tile): {tile_x}, {tile_y}",
                f"Layer: {ActiveLayer}",
                f"Gamemode: {'Survival' if SURVIVAL else 'Creative'}",
            ]

            for i, line in enumerate(debug_lines):
                text_surf = debug_font.render(line, True, (255, 255, 255))
                screen.blit(text_surf, (10, 10 + i * 20))

        if FURNACE_OPEN and current_open_furnace:
            draw_furnace_ui(screen, current_open_furnace)

        if PAUSED:
            pause_menu.draw(screen)

        screen.blit(cursor_img, pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)

    reset_resolution()
    pygame.quit()
finally:
    reset_resolution()
    pygame.quit()