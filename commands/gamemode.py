def execute(console, parts, globals):
    if parts[1] == "1" and globals['Cheats']:
        globals['SURVIVAL'] = True
    elif parts[1] == "2":
        globals['SURVIVAL'] = False

    console.history.append(f"Changed gamemode to {'SURVIVAL' if globals['SURVIVAL'] else 'CREATIVE'}")
