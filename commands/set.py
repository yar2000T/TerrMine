import time


def execute(console, parts, globals):
    if len(parts) == 3 or len(parts) == 2 and globals['Cheats']:
        if parts[1] == "health":
            if parts[2] == "max":
                globals['stats'].health = globals['stats'].max_health
            else:
                globals['stats'].health = int(parts[2])

            console.history.append(f"Set health to {globals['stats'].health}")
        elif parts[1] == "shield":
            globals['IMMNUNE_TIMER'] = time.time() + int(parts[2])
            console.history.append(f"Set shield effect for {parts[2]}s")
        elif parts[1] == "block":
            block_to_place = globals['inventory'].get_selected_block()

            mouse_x, mouse_y = globals['pygame'].mouse.get_pos()
            world_x = (mouse_x - globals['scroll_x']) // globals['TILE_SIZE']
            world_y = (mouse_y - globals['scroll_y']) // globals['TILE_SIZE']

            if block_to_place == 11:
                globals['torches'].append((world_x, world_y, globals['ActiveLayer']))
            elif block_to_place == 13:
                globals['dynamites'].append(globals['Dynamite'](world_x, world_y, globals['ActiveLayer']))
            elif block_to_place == 14:
                globals['private_blocks'].append((world_x, world_y, globals['NAME'], globals['ActiveLayer']))

            if block_to_place != 13:
                globals['world'][world_y][world_x][0] = block_to_place
                globals['world'][world_y][world_x][1] = globals['ActiveLayer']

            console.history.append(f"Placed block at x:{world_x}, y:{world_y}")
        elif parts[1] == "light":
            globals['LIGHT_RADIUS'] = int(parts[2])
            console.history.append(f"Set light radius to {globals['LIGHT_RADIUS']}")
