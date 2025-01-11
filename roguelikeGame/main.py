import pgzrun

WIDTH = 600
HEIGHT = 600
TILE_SIZE = 60

game_state = "menu"
music_on = True

buttons = [
    {"text": "Oyuna Başla", "x": WIDTH // 2 - 100, "y": 200},
    {"text": "Müziği Aç/Kapat", "x": WIDTH // 2 - 100, "y": 300},
    {"text": "Çıkış", "x": WIDTH // 2 - 100, "y": 400},
]

game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 'S', 0, 0, 1, 0, 0, 'E', 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

player_sprites = ["hero_walk1", "hero_walk2", "hero_walk3"]
enemy_sprites = ["enemy_walk1", "enemy_walk2"]

player_animation_index = 0

player_pos = {"x": 1, "y": 8}
enemies = [
    {"x": 5, "y": 3, "dx": 1, "dy": 0, "animation_index": 0},
    {"x": 3, "y": 6, "dx": 0, "dy": -1, "animation_index": 0},
]

frame_counter = 0
enemy_speed = 20

def draw():
    screen.clear()

    if game_state == "menu":
        screen.fill((245, 239, 220))
        screen.draw.text("Ana Menü", (WIDTH // 2 - 100, 50), fontsize=50, color="darkblue")
        for button in buttons:
            screen.draw.text(button["text"], (button["x"], button["y"]), fontsize=40, color="darkgreen")
    
    elif game_state == "playing":
        draw_game()
    elif game_state == "won":
        screen.fill("lightgreen")
        screen.draw.text("Kazandınız!", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color="black")
        screen.draw.text("Tekrar Oyna", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="darkblue")
    elif game_state == "lost":
        screen.fill("red")
        screen.draw.text("Kaybettiniz!", center=(WIDTH // 2, HEIGHT // 3), fontsize=50, color="white")
        screen.draw.text("Tekrar Oyna", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="darkblue")


def draw_game():
    global player_animation_index

    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if cell == 1:
                screen.draw.filled_rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), "gray")
            elif cell == 'S':
                screen.draw.filled_rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), "blue")
            elif cell == 'E':
                screen.draw.filled_rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), "green")
            else:
                screen.draw.filled_rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), "white")
    
    player_x = player_pos["x"] * TILE_SIZE
    player_y = player_pos["y"] * TILE_SIZE
    current_player_sprite = player_sprites[player_animation_index]
    screen.blit(current_player_sprite, (player_x, player_y))

    for enemy in enemies:
        enemy_x = enemy["x"] * TILE_SIZE
        enemy_y = enemy["y"] * TILE_SIZE
        current_enemy_sprite = enemy_sprites[enemy["animation_index"]]
        screen.blit(current_enemy_sprite, (enemy_x, enemy_y))


def update():
    global frame_counter

    if game_state == "playing":

        frame_counter += 1
        if frame_counter >= enemy_speed:
            move_enemies()
            frame_counter = 0
        
        check_collisions()


def move_enemies():
    for enemy in enemies:
        x, y = enemy["x"], enemy["y"]
        dx, dy = enemy["dx"], enemy["dy"]
        new_x, new_y = x + dx, y + dy

        if game_map[new_y][new_x] == 1: 
            enemy["dx"] *= -1
            enemy["dy"] *= -1
        else:
            enemy["x"], enemy["y"] = new_x, new_y

        enemy["animation_index"] = (enemy["animation_index"] + 1) % len(enemy_sprites)


def check_collisions():
    global game_state

    for enemy in enemies:
        if player_pos["x"] == enemy["x"] and player_pos["y"] == enemy["y"]:
            game_state = "lost"
            return

    if game_map[player_pos["y"]][player_pos["x"]] == 'E':
        game_state = "won"


def reset_game():
    global player_pos, enemies, game_state
    player_pos = {"x": 1, "y": 8}
    enemies = [
        {"x": 5, "y": 3, "dx": 1, "dy": 0, "animation_index": 0},
        {"x": 3, "y": 6, "dx": 0, "dy": -1, "animation_index": 0},
    ]
    game_state = "playing"


def toggle_music():
    global music_on
    if music_on:
        music.stop()
    else:
        music.play("menu_music")
    music_on = not music_on


def on_key_down(key):
    sounds.btn.play()
    global player_pos, player_animation_index

    if game_state == "playing":
        x, y = player_pos["x"], player_pos["y"]

        if key == keys.LEFT and game_map[y][x - 1] != 1:
            player_pos["x"] -= 1
            player_animation_index = (player_animation_index + 1) % len(player_sprites)
        elif key == keys.RIGHT and game_map[y][x + 1] != 1:
            player_pos["x"] += 1
            player_animation_index = (player_animation_index + 1) % len(player_sprites)
        elif key == keys.UP and game_map[y - 1][x] != 1:
            player_pos["y"] -= 1
            player_animation_index = (player_animation_index + 1) % len(player_sprites)
        elif key == keys.DOWN and game_map[y + 1][x] != 1:
            player_pos["y"] += 1
            player_animation_index = (player_animation_index + 1) % len(player_sprites)


def on_mouse_down(pos):
    global game_state

    if game_state == "menu":
        for button in buttons:
            bx, by = button["x"], button["y"]
            if bx <= pos[0] <= bx + 200 and by <= pos[1] <= by + 50:
                if button["text"] == "Oyuna Başla":
                    reset_game()
                elif button["text"] == "Müziği Aç/Kapat":
                    toggle_music()
                elif button["text"] == "Çıkış":
                    exit()
    elif game_state in ["won", "lost"]:
        if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 - 20 <= pos[1] <= HEIGHT // 2 + 20:
            reset_game()

if music_on:
    music.play("menu_music")

pgzrun.go()