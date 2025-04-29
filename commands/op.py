def execute(console, parts, globals):
    if len(parts) == 1:
        globals['Cheats'] = True
        console.history.append("Cheats enabled")
