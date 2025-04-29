def execute(console, parts, globals):
    if len(parts) == 3 and globals['Cheats']:
        try:
            x_tile = int(parts[1])
            y_tile = int(parts[2])
            globals['player.x'] = x_tile * globals['TILE_SIZE'] + globals['scroll_x']
            globals['player.y'] = y_tile * globals['TILE_SIZE'] + globals['scroll_y']
            console.history.append(f"Teleported to {x_tile}, {y_tile}")
        except ValueError:
            console.history.append("Invalid coordinates.")