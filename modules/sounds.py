import os


def load(pygame, BASE_DIR, globals):
    globals['explosion_sound'] = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets\\sound_effects\\explosion.mp3"))