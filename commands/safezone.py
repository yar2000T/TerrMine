def execute(console, parts, globals):
    if len(parts) == 2 and globals['Cheats']:
        if parts[1] == "true":
            globals['SafeZone'] = True
        elif parts[1] == "false":
            globals['SafeZone'] = False

        console.history.append(f"Set SafeZone mode to: {globals['SafeZone']}")
