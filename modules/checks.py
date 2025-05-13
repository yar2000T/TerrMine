import random


def check_crafting_result(grid, glob):
    for recipe_pattern, result in glob['CRAFTING_RECIPES'].items():
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


def check_inventory_crafting_result(grid, glob):
    for recipe_pattern, result in glob['INVENTORY_CRAFTING_RECIPES'].items():
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


def check_ladder_collision(player, world, scroll_x, scroll_y, TILE_SIZE):
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


def update_saplings(glob):
    current_time = glob['time'].time()
    growable_saplings = []

    for sapling in glob['saplings'][:]:

        if current_time - sapling["plant_time"] >= glob['random'].randrange(120, 360):
            growable_saplings.append(sapling)
            glob['saplings'].remove(sapling)

    for sapling in growable_saplings:
        x, y, sapling_type = sapling["x"], sapling["y"], sapling["type"]

        if (0 <= y < glob['ROWS'] and 0 <= x < glob['COLS'] and
                glob['world'][y][x][0] == sapling_type and
                glob['world'][y + 1][x][0] == 2):

            tree_type = glob['SAPLING_TO_TREE'][sapling_type]
            tree_height = glob['random'].randrange(4, 7)

            for dy in range(tree_height):
                new_y = y - dy
                if 0 <= new_y < glob['ROWS']:
                    glob['world'][new_y][x][0] = tree_type
                    glob['world'][new_y][x][1] = 2

            leaf_radius = 2
            for ly in range(y - tree_height - leaf_radius, y - tree_height + leaf_radius + 1):
                for lx in range(x - leaf_radius, x + leaf_radius + 1):
                    if (0 <= lx < glob['COLS'] and 0 <= ly < glob['ROWS'] and
                            (lx - x) ** 2 + (ly - (y - tree_height)) ** 2 <= leaf_radius ** 2 and
                            glob['world'][ly][lx][0] == 100500):
                        glob['world'][ly][lx][0] = 8
                        glob['world'][ly][lx][1] = 1