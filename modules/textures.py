import os


def load(pygame, BASE_DIR, PLAYER_SIZE, TILE_SIZE, screen, SCREEN_WIDTH, SCREEN_HEIGHT, globals):

    globals['menu_background'] = pygame.image.load(os.path.join(BASE_DIR, "assets\\menu_background.png"))
    globals['menu_background2'] = pygame.image.load(os.path.join(BASE_DIR, "assets\\menu_background2.png"))

    globals['player_textures'] = {
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

    globals['textures'] = {
        1: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\dirt.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        2: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\grass.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        3: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\stone.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        4: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\brick.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        5: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\diamond.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        6: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\end_bricks.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        7: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\planks_oak.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        8: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\leaves_oak.png")).convert_alpha(),
                                  (TILE_SIZE, TILE_SIZE)),
        9: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_oak.png")).convert(),
                                  (TILE_SIZE, TILE_SIZE)),
        10: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\stonebrick.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        11: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\torch_on.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        12: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\ladder.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        13: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\tnt.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        14: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\private.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        15: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\glass.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        16: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_acacia.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        17: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_big_oak.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        18: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_birch.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        19: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\log_spruce.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        20: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\magma.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        21: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_inside.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        22: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_skin_red.png")).convert(),
            (TILE_SIZE, TILE_SIZE)),
        23: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_block_skin_brown.png")).convert(),
            (TILE_SIZE, TILE_SIZE)),
        24: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\hay_block_side.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        25: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\crafting_table_front.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        26: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\pumpkin_face_off.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        27: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\debug.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        28: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\debug2.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        29: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_red.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        30: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\mushroom_brown.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        31: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\diamond_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        32: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\emerald_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        33: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\gold_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        34: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\iron_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        35: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\nether_brick.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        36: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\redstone_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        37: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\coal_ore.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        38: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\diamond.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        39: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\emerald.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        40: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\gold_ingot.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        41: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\iron_ingot.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        42: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\netherbrick.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        43: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\redstone_dust.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        44: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\charcoal.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        45: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\coal_block.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        46: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\iron_block.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        47: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\cobblestone.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        48: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\gunpowder.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        49: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\sand.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        50: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\items\\stick.png")).convert_alpha(),
                                   (TILE_SIZE, TILE_SIZE)),
        51: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\cobblestone_mossy.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        52: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\chest.png")).convert(),
                                   (TILE_SIZE, TILE_SIZE)),
        53: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\furnace\\furnace_front_off.png")).convert(),
            (TILE_SIZE, TILE_SIZE)),
        54: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\trapdoor\\closed.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        55: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\trapdoor\\opened.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        56: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_acacia.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        57: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_birch.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        58: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_jungle.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        59: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_oak.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        60: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_roofed_oak.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        61: pygame.transform.scale(
            pygame.image.load(os.path.join(BASE_DIR, "assets\\saplings\\sapling_spruce.png")).convert_alpha(),
            (TILE_SIZE, TILE_SIZE)),
        100: pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\bedrock.png")).convert(),
                                    (TILE_SIZE, TILE_SIZE)),
    }

    globals['destruction_textures'] = [
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

    globals['fire_stages'] = [
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

    globals['arrow_stages'] = [
        load_and_scale(os.path.join(BASE_DIR, f"assets\\arrow_stages\\arrow_stage_{i}.png"), 1.8)
        for i in range(1, 24)
    ]

    globals['dead'] = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\You died!.png")).convert_alpha(screen),
                                  (SCREEN_WIDTH, SCREEN_HEIGHT))

    for tile, tex in globals['textures'].items():
        gray = tex.copy()
        overlay = pygame.Surface(tex.get_size(), pygame.SRCALPHA)
        overlay.fill((180, 180, 180, 50))
        gray.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        globals['grayscale_textures'][tile] = gray

    globals['crosshair'] = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR,"assets\\crosshair.png")).convert_alpha(screen),
                                       (TILE_SIZE, TILE_SIZE))
    globals['shield'] = pygame.image.load(os.path.join(BASE_DIR,"assets\\player\\shield.png")).convert_alpha(screen)

    globals['explosion_img'] = pygame.image.load(os.path.join(BASE_DIR,"assets\\explosion.png")).convert_alpha()

    globals['trapdoor_stab'] = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "assets\\stabs\\trapdoor.png")).convert_alpha(screen),
        (TILE_SIZE, TILE_SIZE))

    button_img = pygame.image.load(os.path.join(BASE_DIR, "assets/ui/button.png")).convert_alpha()
    button_hover_img = pygame.image.load(os.path.join(BASE_DIR, "assets/ui/button_hover.png")).convert_alpha()

    globals['button_img'] = pygame.transform.scale(button_img, (250, 50))
    globals['button_hover_img'] = pygame.transform.scale(button_hover_img, (250, 50))