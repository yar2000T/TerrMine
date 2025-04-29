def execute(console, parts, globals):
    globals['homes'].append([globals['scroll_x'], globals['scroll_y'], parts[1]])
    console.history.append(f"Home {parts[1]} set")
