import pygame, sys, math, random

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Minecraft - Master Realism (Blue Sky)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16, bold=True)

# Lock Mouse
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# --- WORLD GEN ---
world_size = 32
world_map = [[0 for _ in range(world_size)] for _ in range(world_size)]
noise_map = [[random.uniform(0.8, 1.2) for _ in range(world_size)] for _ in range(world_size)]
stars = [(random.randint(0, width), random.randint(0, height // 2)) for _ in range(60)]

for x in range(world_size):
    for y in range(world_size):
        if x == 0 or x == world_size-1 or y == 0 or y == world_size-1:
            world_map[y][x] = 3 # Stone Wall
        else:
            calc = math.sin(x * 0.4) * math.cos(y * 0.4)
            if calc > 0.2: world_map[y][x] = 1   # Grass
            elif calc < -0.3: world_map[y][x] = 2 # Dirt

# --- PLAYER ---
px, py, pz = 16.5, 16.5, 0.0
v_angle = 0.0
p_pitch = 0.0
v_z = 0.0
walk_bob = 0.0
game_mode = "SURVIVAL"
is_flying = False
last_jump = 0
selected_block = 1

# --- REAL COLORS (Green/Blue) ---
BLOCK_COLORS = {
    1: (34, 180, 34),   # Bright Green Grass
    2: (139, 69, 19),   # Brown Dirt
    3: (100, 100, 100), # Grey Stone
    4: (0, 255, 255),   # Cyan Diamond
    5: (255, 69, 0)     # Orange Lava
}

game_time = 0.0
day_len = 2000.0

while True:
    game_time += 1
    cycle = (math.sin(game_time / 300) + 1) / 2
    
    # Sky: Blue to Black
    sr, sg, sb = int(100*cycle), int(180*cycle), int(255*cycle)
    screen.fill((max(10, sr), max(10, sg), max(20, sb)))

    # Stars (Night)
    if cycle < 0.4:
        for sx, sy in stars:
            if random.randint(0,10) > 2: pygame.draw.circle(screen, (255,255,255), (sx, sy), 1)

    # Sun/Moon
    sun_x = int((game_time % day_len) / day_len * width * 4) % (width + 200) - 100
    sun_y = 100 + int(math.sin(game_time / 200) * 50) + int(p_pitch * 0.5)
    sun_col = (255, 255, 0) if cycle > 0.5 else (220, 220, 220)
    pygame.draw.circle(screen, sun_col, (sun_x, sun_y), 50)

    # Ground
    fg = int(80 * cycle)
    pygame.draw.rect(screen, (10, max(20, fg), 10), (0, height//2 + int(p_pitch), width, height//2 - int(p_pitch)))

    # --- EVENTS ---
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.event.set_grab(False); pygame.mouse.set_visible(True)
            if event.key == pygame.K_c: 
                game_mode = "CREATIVE" if game_mode == "SURVIVAL" else "SURVIVAL"
                is_flying = (game_mode == "CREATIVE")
            if event.key == pygame.K_SPACE:
                if game_mode == "CREATIVE":
                    if current_time - last_jump < 300: is_flying = not is_flying; v_z = 0
                    else: 
                        if is_flying: pz += 0.5 
                        else: v_z = 2.0
                    last_jump = current_time
                else:
                    if pz <= 0: v_z = 2.0
            if event.key >= pygame.K_1 and event.key <= pygame.K_5:
                selected_block = event.key - pygame.K_0

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.event.get_grab():
            tx, ty = int(px + math.cos(v_angle)*1.5), int(py + math.sin(v_angle)*1.5)
            if 0<=tx<32 and 0<=ty<32:
                if event.button == 1: world_map[ty][tx] = 0
                elif event.button == 3 and world_map[ty][tx] == 0: world_map[ty][tx] = selected_block

    # --- INPUT ---
    if pygame.event.get_grab():
        mx, my = pygame.mouse.get_rel()
        v_angle += mx * 0.0035
        p_pitch -= my * 0.8; p_pitch = max(-300, min(300, p_pitch))

    keys = pygame.key.get_pressed()
    speed = 0.2 if is_flying else 0.08
    if keys[pygame.K_LSHIFT]: speed *= 1.8
    if keys[pygame.K_w] or keys[pygame.K_s]: walk_bob += 0.25
    else: walk_bob = 0

    ca, sa = math.cos(v_angle), math.sin(v_angle)
    dx, dy = 0, 0
    if keys[pygame.K_w]: dx += ca; dy += sa
    if keys[pygame.K_s]: dx -= ca; dy -= sa
    if keys[pygame.K_d]: dx -= sa; dy += ca
    if keys[pygame.K_a]: dx += sa; dy -= ca

    if dx!=0 or dy!=0:
        if 0<=int(px+dx)<32 and world_map[int(py)][int(px+dx)]==0: px += dx
        if 0<=int(py+dy)<32 and world_map[int(py+dy)][int(px)]==0: py += dy

    if is_flying:
        if keys[pygame.K_SPACE]: pz += 0.15
        if keys[pygame.K_LCTRL]: pz -= 0.15
    else:
        pz += v_z * 0.04; v_z -= 0.15
        if pz <= 0: pz, v_z = 0, 0

    # --- RENDER ---
    for i in range(120):
        ra = (v_angle - 0.5) + (i/120) * 1.0
        dist = 0; hit = 0; b_type = 0; tx, ty = 0, 0
        sr, cr = math.sin(ra), math.cos(ra)
        
        while hit == 0 and dist < 20:
            dist += 0.05
            cx, cy = int(px + cr*dist), int(py + sr*dist)
            if cx < 0 or cx >= 32 or cy < 0 or cy >= 32: hit, b_type = 1, 3
            elif world_map[cy][cx] > 0: hit, b_type = 1, world_map[cy][cx]; tx, ty = cx, cy
        
        dist = max(0.1, dist * math.cos(ra - v_angle))
        h = int(height / dist)
        ch = int(pz * (height/2) / dist) + int(p_pitch)
        
        base = BLOCK_COLORS.get(b_type, (255,255,255))
        grit = noise_map[ty][tx] if hit else 1
        br = max(0.2, cycle)
        fog = max(0.1, 1 - dist/16)
        c = (min(255, int(base[0]*grit*fog*br)), min(255, int(base[1]*grit*fog*br)), min(255, int(base[2]*grit*fog*br)))
        
        pygame.draw.rect(screen, c, (i*(width/120), (height//2 - h//2) + ch, width/120 + 1, h))

    # --- HAND ---
    hc = BLOCK_COLORS[selected_block]
    off = math.sin(walk_bob) * 10
    pygame.draw.rect(screen, hc, (width-200, height-200+off, 60, 200))
    
    # --- HUD ---
    for i in range(1, 6):
        c = BLOCK_COLORS[i]
        rx = width//2 - 150 + (i*60)
        if selected_block == i: pygame.draw.rect(screen, (255,255,255), (rx-4, height-64, 58, 58))
        pygame.draw.rect(screen, c, (rx, height-60, 50, 50))

    screen.blit(font.render(f"MODE: {game_mode}", 1, (255,255,255)), (20,20))
    pygame.draw.circle(screen, (255,255,255), (width//2, height//2), 3)
    pygame.display.flip(); clock.tick(60)
