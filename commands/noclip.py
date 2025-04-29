def execute(console, parts, globals):
    if parts[1] == "true" and globals['Cheats']:
        globals['NoClip'] = True
    elif parts[1] == "false" and globals['Cheats']:
        globals['NoClip'] = False

    console.history.append(f"Set NoClip mode to: {globals['NoClip']}")
