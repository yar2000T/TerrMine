import os

globals_var = None


def load(globals):
    global globals_var
    globals_var = globals


class Console:
    def __init__(self):
        self.is_open = False
        self.input_text = ""
        self.history = []
        self.font = globals_var['pygame'].font.SysFont("consolas", 20)
        self.max_history = 10

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event):
        if event.type == globals_var['pygame'].KEYDOWN:
            if event.key == globals_var['pygame'].K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == globals_var['pygame'].K_RETURN:
                self.execute_command(self.input_text)
                self.input_text = ""
            else:
                self.input_text += event.unicode

    def execute_command(self, command):
        self.history.append(command)
        if len(self.history) > self.max_history:
            self.history.pop(0)

        command_parts = command.split()

        if len(command_parts) > 0:
            command_name = command_parts[0].lstrip("/").lstrip("//")

            command_func = globals_var['command_map'].get(command_name)

            if command_func:
                command_func(self, command_parts, globals_var)
            else:
                self.history.append(f"Unknown command: {command_name}")

    def draw(self):
        if not self.is_open:
            return

        console_surface = globals_var['pygame'].Surface((globals_var['SCREEN_WIDTH'], globals_var['SCREEN_HEIGHT']), globals_var['pygame'].SRCALPHA)
        console_surface.fill((0, 0, 0, 150))

        globals_var['screen'].blit(console_surface, (0, globals_var['SCREEN_HEIGHT'] - globals_var['SCREEN_HEIGHT']))

        input_surface = self.font.render(self.input_text, True, (255, 255, 255))
        globals_var['screen'].blit(input_surface, (10, globals_var['SCREEN_HEIGHT'] - 30))

        for i, line in enumerate(reversed(self.history)):
            history_surface = self.font.render(line, True, (200, 200, 200))
            globals_var['screen'].blit(history_surface, (10, globals_var['SCREEN_HEIGHT'] - 60 - i * 20))


class PlayerStats:
    def __init__(self):
        self.max_health = 10
        self.health = self.max_health
        self.fall_threshold = 10  # Damage starts after falling 10 units (adjust this value)
        self.fall_damage_rate = 0.5  # 1 damage per block fallen
        self.fall_distance = 0  # Track how far the player has fallen
        self.is_falling = False

        self.full_heart = globals_var['pygame'].transform.scale(
            globals_var['pygame'].image.load(os.path.join(globals_var['BASE_DIR'], "assets\\heart\\full.png")).convert_alpha(globals_var['screen']),
            (14, 12))
        self.half_heart = globals_var['pygame'].transform.scale(
            globals_var['pygame'].image.load(os.path.join(globals_var['BASE_DIR'], "assets\\heart\\half.png")).convert_alpha(globals_var['screen']),
            (14, 12))
        self.empty_heart = globals_var['pygame'].transform.scale(
            globals_var['pygame'].image.load(os.path.join(globals_var['BASE_DIR'], "assets\\heart\\empty.png")).convert_alpha(globals_var['screen']),
            (14, 12))

    def draw_hearts(self):
        heart_x = globals_var['SCREEN_WIDTH'] * 0.5 - 200
        heart_y = globals_var['SCREEN_HEIGHT'] - 80

        heart_spacing = 16

        for i in range(self.max_health):
            if self.health >= i + 1:
                globals_var['screen'].blit(self.full_heart, (heart_x, heart_y))
            elif self.health > i:
                globals_var['screen'].blit(self.half_heart, (heart_x, heart_y))
            else:
                globals_var['screen'].blit(self.empty_heart, (heart_x, heart_y))

            heart_x += heart_spacing

    def draw_ui(self):
        if globals_var['SURVIVAL']:
            self.draw_hearts()


class FakeButton:

    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = globals_var['pygame'].Rect(x, y, width, height)

    def draw(self):
        globals_var['pygame'].draw.rect(globals_var['screen'], globals_var['GRAY'], self.rect, border_radius=10)
        text_surf = globals_var['font1'].render(self.text, True, globals_var['BLACK'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        globals_var['screen'].blit(text_surf, text_rect)

    def check_click(self, pos):
        pass


class Button:

    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = globals_var['pygame'].Rect(x, y, width, height)
        self.action = action

    def draw(self):
        globals_var['pygame'].draw.rect(globals_var['screen'], globals_var['GRAY'], self.rect, border_radius=10)
        text_surf = globals_var['font1'].render(self.text, True, globals_var['BLACK'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        globals_var['screen'].blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


class Inventory:
    def __init__(self):
        if not globals_var['SURVIVAL']:
            self.items = [[54, 1], [1, 1], [2, 1], [3, 1], [47, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
                          [9, 1], [16, 1], [17, 1], [18, 1], [19, 1], [10, 1], [11, 1], [12, 1],
                          [13, 1], [14, 1], [15, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1],
                          [25, 1], [26, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1],
                          [35, 1], [36, 1], [37, 1], [45, 1], [46, 1], [49, 1], [51, 1], [52, 1],
                          [53, 1], [0, 1]]

            self.max_items = len(self.items)
        else:
            self.items = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
            self.max_items = 10

        self.selected_index = 0
        self.scroll_index = 0

    def scroll(self, direction):
        self.selected_index += direction
        if self.selected_index < 0:
            self.selected_index = len(self.items) - 1
        elif self.selected_index >= len(self.items):
            self.selected_index = 0

        if len(self.items) > globals_var['max_items_per_row']:
            if self.selected_index < self.scroll_index:
                self.scroll_index = self.selected_index
            elif self.selected_index >= self.scroll_index + globals_var['max_items_per_row']:
                self.scroll_index = self.selected_index - globals_var['max_items_per_row'] + 1

    def get_selected_block(self):
        return self.items[self.selected_index][0]

    def append_new_item(self, block_id, amount=1):
        MAX_STACK = 64

        for i in range(len(self.items)):
            slot_id, quantity = self.items[i]
            if slot_id == block_id and quantity < MAX_STACK:
                space_left = MAX_STACK - quantity
                to_add = min(space_left, amount)
                self.items[i][1] += to_add
                amount -= to_add
                if amount <= 0:
                    return

        for i in range(len(self.items)):
            slot_id, quantity = self.items[i]
            if slot_id == 0:
                to_add = min(MAX_STACK, amount)
                self.items[i] = [block_id, to_add]
                amount -= to_add
                if amount <= 0:
                    return

        if len(self.items) < self.max_items:
            to_add = min(MAX_STACK, amount)
            self.items.append([block_id, to_add])
            amount -= to_add
            if amount <= 0:
                return

        if amount > 0:
            # print(f"Inventory full! Could not add {amount}x block ID {block_id}")
            pass

    def delete_block(self, block_id, amount=1):
        for i in range(len(self.items)):
            slot_id, quantity = self.items[i]
            if slot_id == block_id:
                if quantity >= amount:
                    self.items[i][1] -= amount
                    if self.items[i][1] <= 0:
                        self.items[i] = [0, 0]
                    return True
                else:
                    amount -= quantity
                    self.items[i] = [0, 0]
        return False

    def has_block(self, block_id):
        for slot_id, quantity in self.items:
            if slot_id == block_id and quantity > 0:
                return True
        return False


class Dynamite:
    def __init__(self, x, y, countdown=3):
        self.x = x
        self.y = y
        self.countdown = countdown
        self.placed_time = None
        self.exploded = False
        self.explosion_time = None
        self.blink_interval = 0.2
        self.last_blink = globals_var['time'].time()
        self.blink_state = False
        self.falling = True

    def update(self, world):
        if self.exploded:
            if self.explosion_time is not None and globals_var['time'].time() - self.explosion_time > 0.5:
                dynamites.remove(self)
            return

        if self.falling:
            if self.y + 1 < globals_var['ROWS'] and world[self.y + 1][self.x][0] in [0, 100500]:
                self.y += 1
            else:
                self.falling = False
                self.placed_time = globals_var['time'].time()
        else:
            elapsed = globals_var['time'].time() - self.placed_time

            if elapsed >= self.countdown - 1:
                if globals_var['time'].time() - self.last_blink >= self.blink_interval:
                    self.blink_state = not self.blink_state
                    self.last_blink = globals_var['time'].time()

            if elapsed >= self.countdown:
                self.explode(world)

    def explode(self, world):
        explosion_sound.play()
        explosion_radius = 3
        cx, cy = self.x, self.y

        for dx in range(-explosion_radius, explosion_radius + 1):
            for dy in range(-explosion_radius, explosion_radius + 1):
                dist = math.sqrt(dx ** 2 + dy ** 2)
                if dist <= explosion_radius:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < globals_var['COLS'] and 0 <= ny < globals_var['ROWS']:
                        if world[ny][nx][0] != 100:
                            world[ny][nx][0] = 100500

                        for pb in private_blocks:
                            pb_x, pb_y, owner, layer = pb
                            if pb_x == nx and pb_y == ny:
                                private_blocks.remove(pb)
                                # console.history.append(f"Private block at ({nx}, {ny}) destroyed!")
                                break

        self.exploded = True
        self.explosion_time = globals_var['time'].time()

    def draw(self, textures):
        if self.exploded:
            screen.blit(explosion_img, ((self.x * TILE_SIZE + scroll_x) - explosion_img.get_width() // 2,
                                        (self.y * TILE_SIZE + scroll_y) - explosion_img.get_height() // 2))
        else:
            tnt_texture = textures[13].copy()
            if self.blink_state:
                tnt_texture.set_alpha(150)
                screen.blit(tnt_texture, (self.x * TILE_SIZE + scroll_x, self.y * TILE_SIZE + scroll_y))
            else:
                screen.blit(textures[13], (self.x * TILE_SIZE + scroll_x, self.y * TILE_SIZE + scroll_y))


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = globals_var['pygame'].Rect(x, y, w, h)
        self.color = globals_var['pygame'].Color('gray')
        self.text = text
        self.txt_surface = globals_var['font1_'].render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == globals_var['pygame'].MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = globals_var['pygame'].Color('lightgray') if self.active else globals_var['pygame'].Color('gray')
        if event.type == globals_var['pygame'].KEYDOWN:
            if self.active:
                if event.key == globals_var['pygame'].K_RETURN:
                    return self.text
                elif event.key == globals_var['pygame'].K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = globals_var['font1_'].render(self.text, True, globals_var['pygame'].Color('white'))
        return None

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        globals_var['pygame'].draw.rect(globals_var['screen'], self.color, self.rect)
        globals_var['screen'].blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class WorldSelectionMenu:
    def __init__(self):
        self.worlds = []
        self.scroll_offset = 0
        self.selected_world = None
        self.load_button = Button("Load", globals_var['SCREEN_WIDTH'] // 2 - 100, globals_var['SCREEN_HEIGHT'] - 100, 200, 50, self.load_selected)
        self.back_button = Button("Back", 50, 50, 100, 40, self.back)
        self.refresh_worlds()

    def refresh_worlds(self):
        if not os.path.exists("saves"):
            os.makedirs("saves")
        self.worlds = [f for f in os.listdir("saves") if f.endswith(".trrm")]

    def back(self):
        global MENU, load_world_active
        MENU = True
        load_world_active = False

    def load_selected(self):
        global running, world_name
        if self.selected_world:
            world_name = self.selected_world.replace(".trrm", "")
            globals_var['load_world'](os.path.join("saves", self.selected_world))
            running = False

    def draw(self, screen):
        globals_var['screen'].blit(globals_var['menu_background2'], (0, 0))

        title = globals_var['font1'].render("Select World", True, globals_var['WHITE'])
        globals_var['screen'].blit(title, (globals_var['SCREEN_WIDTH'] // 2 - title.get_width() // 2, 50))

        self.back_button.draw()

        visible_worlds = self.worlds[self.scroll_offset:self.scroll_offset + 5]
        for i, world in enumerate(visible_worlds):
            y_pos = 150 + i * 60
            rect = globals_var['pygame'].Rect(globals_var['SCREEN_WIDTH'] // 2 - 200, y_pos, 400, 50)

            color = (100, 100, 100) if world != self.selected_world else (150, 150, 150)
            globals_var['pygame'].draw.rect(globals_var['screen'], color, rect)
            globals_var['pygame'].draw.rect(globals_var['screen'], globals_var['WHITE'], rect, 2)

            name = world.replace(".trrm", "")
            name_text = globals_var['font1_'].render(name, True, globals_var['WHITE'])
            globals_var['screen'].blit(name_text, (rect.x + 10, rect.y + 15))

        if len(self.worlds) > 5:
            if self.scroll_offset > 0:
                globals_var['pygame'].draw.polygon(globals_var['screen'], globals_var['WHITE'], [
                    (globals_var['SCREEN_WIDTH'] // 2, 130),
                    (globals_var['SCREEN_WIDTH'] // 2 - 10, 140),
                    (globals_var['SCREEN_WIDTH'] // 2 + 10, 140)
                ])

            if self.scroll_offset < len(self.worlds) - 5:
                globals_var['pygame'].draw.polygon(globals_var['screen'], globals_var['WHITE'], [
                    (SCREEN_WIDTH // 2, 450),
                    (SCREEN_WIDTH // 2 - 10, 440),
                    (SCREEN_WIDTH // 2 + 10, 440)
                ])

        self.load_button.draw()

    def handle_event(self, event):
        if event.type == globals_var['pygame'].MOUSEBUTTONDOWN:
            self.back_button.check_click(event.pos)
            self.load_button.check_click(event.pos)

            visible_worlds = self.worlds[self.scroll_offset:self.scroll_offset + 5]
            for i, world in enumerate(visible_worlds):
                y_pos = 150 + i * 60
                rect = globals_var['pygame'].Rect(globals_var['SCREEN_WIDTH'] // 2 - 200, y_pos, 400, 50)
                if rect.collidepoint(event.pos):
                    self.selected_world = world

            if event.button == 4:
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1
            elif event.button == 5:
                if self.scroll_offset < len(self.worlds) - 5:
                    self.scroll_offset += 1


class PauseMenu:
    def __init__(self):
        self.buttons = [
            Button("Resume", globals_var['SCREEN_WIDTH'] // 2 - 100, globals_var['SCREEN_HEIGHT'] // 2 - 100, 200, 50, self.resume),
            Button("Main Menu", globals_var['SCREEN_WIDTH'] // 2 - 100, globals_var['SCREEN_HEIGHT'] // 2 - 30, 200, 50, self.main_menu),
            Button("Exit", globals_var['SCREEN_WIDTH'] // 2 - 100, globals_var['SCREEN_HEIGHT'] // 2 + 40, 200, 50, self.exit_game)
        ]

    def resume(self):
        global PAUSED
        PAUSED = False

    def main_menu(self):
        global PAUSED, running, MENU
        globals_var['save_map'](globals_var['world'], globals_var['torches'], globals_var['private_blocks'], globals_var['homes'],
                                globals_var['GameMode'], globals_var['scroll_x'], globals_var['scroll_y'], globals_var['player'],
                                globals_var['SURVIVAL'], globals_var['inventory_chest'], globals_var['chests'],
                                globals_var['inventory.items'], globals_var['furnaces'])
        PAUSED = False
        running = False
        MENU = True

    def exit_game(self):
        global running
        globals_var['save_map'](globals_var['world'], globals_var['torches'], globals_var['private_blocks'], globals_var['homes'],
                                globals_var['GameMode'], globals_var['scroll_x'], globals_var['scroll_y'], globals_var['player'],
                                globals_var['SURVIVAL'], globals_var['inventory_chest'], globals_var['chests'],
                                globals_var['inventory.items'], globals_var['furnaces'])
        running = False

    def draw(self):
        overlay = globals_var['pygame'].Surface((globals_var['SCREEN_WIDTH'], globals_var['SCREEN_HEIGHT']), globals_var['pygame'].SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        globals_var['screen'].blit(overlay, (0, 0))

        title = globals_var['font1'].render("Game Paused", True, globals_var['WHITE'])
        globals_var['screen'].blit(title, (globals_var['SCREEN_WIDTH'] // 2 - title.get_width() // 2, globals_var['SCREEN_HEIGHT'] // 2 - 150))

        for button in self.buttons:
            button.draw()

    def handle_event(self, event):
        if event.type == globals_var['pygame'].MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)