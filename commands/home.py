def execute(console, parts, globals):
    for nx, ny, name in globals['homes']:
        if name == parts[1]:
            globals['scroll_y'] = ny
            globals['scroll_x'] = nx
            console.history.append(f"Teleported to home {parts[1]}")
