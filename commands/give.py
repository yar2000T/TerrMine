def execute(console, parts, globals):
    if len(parts) == 2 and globals['Cheats']:
        try:
            block_id = int(parts[1])
            globals['inventory'].append_new_item(block_id)
            console.history.append(f"Gave block ID {block_id}")
        except ValueError:
            console.history.append("Invalid block ID.")
    elif len(parts) == 3 and globals['Cheats']:
        try:
            block_id = int(parts[1])
            quantity_block = int(parts[2])
            globals['inventory'].append_new_item(block_id, quantity_block)
            console.history.append(f"Gave block ID {block_id} with quantity {quantity_block}")
        except ValueError:
            console.history.append("Invalid block ID.")
