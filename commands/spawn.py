def execute(console, parts, globals):
    console.history.append("Player teleported to spawn")
    globals['scroll_y'] = -6000
    globals['scroll_x'] = 0
