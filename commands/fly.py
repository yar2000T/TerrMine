def execute(console, parts, globals):
    if len(parts) == 2 and globals['Cheats']:
        if parts[1] == "true":
            globals['FLY'] = True
        elif parts[1] == "false":
            globals['FLY'] = False

        console.history.append(f"Set fly mode to: {globals['FLY']}")
