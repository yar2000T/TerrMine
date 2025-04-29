def execute(console, parts, globals):
    if len(parts) == 2 and globals['Cheats']:
        if parts[1] == "true":
            globals['GOD'] = True
        elif parts[1] == "false":
            globals['GOD'] = False

        console.history.append(f"Set god mode to: {globals['GOD']}")
