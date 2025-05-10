def check_crafting_result(grid, glob):
    grid_tuple = tuple(tuple(row) for row in grid)

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
    grid_tuple = tuple(tuple(row) for row in grid)

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