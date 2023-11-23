import math
import tkinter as tk

WIDTH, HEIGHT = 1280, 650
TILE_SIZE = 30
FOV = math.pi / 3
NUM_RAYS = 200
MOVEMENT_SPEED = 20
ROTATION_SPEED = 0.1
collidingWall = False
anim_frame = 0

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def lerp(a, b, t):
    return (1 - t) * a + t * b
    
player_pos = [2.5 * TILE_SIZE, 2.5 * TILE_SIZE]
player_angle = 0

root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(side=tk.LEFT)

hand_image = tk.PhotoImage(file="hand.png")
mini_map_canvas = tk.Canvas(root, width=200, height=120, bg="black")
mini_map_canvas.place(relx=0.81, rely=0.05)

class NPC:
    def __init__(self, position):
        self.position = position
        self.speed = 0.5

    def update(self, player_pos, player_angle, maze):
        dx = player_pos[0] - self.position[0]
        dy = player_pos[1] - self.position[1]
        distance_to_player = math.sqrt(dx**2 + dy**2)

        # Calculate the angle between player and NPC
        angle_to_player = math.atan2(dy, dx)

        # Calculate the relative position of the NPC based on player's movement
        dx = self.position[0] - player_pos[0]
        dy = self.position[1] - player_pos[1]
        player_dx = math.cos(player_angle) * 0.1
        player_dy = math.sin(player_angle) * 0.1

        # Update the NPC's position based on the player's movement
        #self.position[0] -= player_dx
        #self.position[1] -= player_dy

        # Adjust the angle considering the player's angle
        angle_difference = angle_to_player - player_angle
        if angle_difference < -math.pi:
            angle_difference += 2 * math.pi
        if angle_difference > math.pi:
            angle_difference -= 2 * math.pi

        # Update NPC's position based on angle difference and distance to player
        if distance_to_player > 50:  # Threshold for stopping
            if abs(angle_difference) > 0.1:  # Tolerance for smooth movement
                # Move in the direction opposite to the player's rotation
                self.position[0] += math.cos(angle_to_player) * self.speed
                self.position[1] += math.sin(angle_to_player) * self.speed

            # Check for collisions with walls
            tile_x = int(self.position[0] // TILE_SIZE)
            tile_y = int(self.position[1] // TILE_SIZE)

            if maze[tile_y][tile_x] == 1:
                # If there's a wall, move back
                self.position[0] += math.cos(angle_to_player) * self.speed
                self.position[1] += math.sin(angle_to_player) * self.speed

npc = NPC([1.5 * TILE_SIZE, 1.5 * TILE_SIZE])  # Initial NPC position


def cast_rays(player_pos, player_angle, npc_pos):
    global collidingWall, distance_to_wall, ray_angle
    rays = []
    ray_angle = player_angle - FOV / 2

    for _ in range(NUM_RAYS):
        ray_dx = math.cos(ray_angle)
        ray_dy = math.sin(ray_angle)

        distance_to_wall = 0
        hit_wall = False

        while not hit_wall and distance_to_wall < 1000:
            distance_to_wall += 1
            test_x, test_y = int(player_pos[0] + ray_dx * distance_to_wall), int(player_pos[1] + ray_dy * distance_to_wall)

            if maze[test_y // TILE_SIZE][test_x // TILE_SIZE] == 1:
                hit_wall = True

        rays.append((distance_to_wall))
        ray_angle += FOV / NUM_RAYS

    # Calculate NPC position relative to player
    npc_dx = npc_pos[0] - player_pos[0]
    npc_dy = npc_pos[1] - player_pos[1]
    npc_distance = math.sqrt(npc_dx**2 + npc_dy**2)

    # Check if NPC is hit by a ray
    npc_hit = False
    if npc_distance < distance_to_wall:
        npc_hit = True

    return rays, npc_hit

def on_key_press(event):
    global player_pos, player_angle, collidingWall, distance_to_wall, anim_frame
    new_x, new_y = player_pos[0], player_pos[1]

    if event.keysym == 'w' or event.keysym == 's':
        ray_dx = math.cos(player_angle)
        ray_dy = math.sin(player_angle)

        if event.keysym == 'w':
            new_x = player_pos[0] + MOVEMENT_SPEED * ray_dx
            new_y = player_pos[1] + MOVEMENT_SPEED * ray_dy
            anim_frame += 1
        elif event.keysym == 's':
            new_x = player_pos[0] - MOVEMENT_SPEED * ray_dx
            new_y = player_pos[1] - MOVEMENT_SPEED * ray_dy
            anim_frame += 1

        test_x, test_y = int(new_x), int(new_y)

        if maze[test_y // TILE_SIZE][test_x // TILE_SIZE] == 0:
            collidingWall = False
        else:
            collidingWall = True
            new_x, new_y = player_pos[0], player_pos[1]

    if event.keysym == 'a':
        player_angle -= ROTATION_SPEED
    elif event.keysym == 'd':
        player_angle += ROTATION_SPEED

    player_pos[0] = lerp(player_pos[0], new_x, 0.2)
    player_pos[1] = lerp(player_pos[1], new_y, 0.2)

root.bind("<KeyPress>", on_key_press)

def draw_mini_map():

    mini_map_canvas.delete("all")

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                mini_map_canvas.create_rectangle((x * TILE_SIZE // 4) + 1, (y * TILE_SIZE // 4) + 1, (x + 1) * TILE_SIZE // 4, (y + 1) * TILE_SIZE // 4, fill="#c3cb6e")
            else:
                mini_map_canvas.create_rectangle((x * TILE_SIZE // 4) + 1, (y * TILE_SIZE // 4) + 1, (x + 1) * TILE_SIZE // 4, (y + 1) * TILE_SIZE // 4, fill="#707037")

    # Draw player on the mini-map
    player_x = int(player_pos[0] // TILE_SIZE)
    player_y = int(player_pos[1] // TILE_SIZE)
    mini_map_canvas.create_oval(player_x * TILE_SIZE // 4, player_y * TILE_SIZE // 4, (player_x + 1) * TILE_SIZE // 4, (player_y + 1) * TILE_SIZE // 4, fill="white")

    # Draw NPC on the mini-map
    npc_x = int(npc.position[0] // TILE_SIZE)
    npc_y = int(npc.position[1] // TILE_SIZE)
    mini_map_canvas.create_rectangle(npc_x * TILE_SIZE // 4, npc_y * TILE_SIZE // 4, (npc_x + 1) * TILE_SIZE // 4, (npc_y + 1) * TILE_SIZE // 4, fill="red")

def update():
    global ray_angle, anim_frame
    canvas.delete("all")

    for i in range(int(HEIGHT)):
        r = int(lerp(120 - 1.55 * i, 0.6, 0))
        g = int(lerp(110 - 1.35 * i, 0.6, 0))
        b = int(lerp(60 - 1 * i, 0.6, 0))

        ceiling_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        if ceiling_color.find('-') != -1:
            ceiling_color = "#000000"
        
        canvas.create_polygon(0, 0 + 5 * i, WIDTH, 0 + 5 * i, WIDTH, 0 + (11 * i), 0, 0 + (11 * i), fill=ceiling_color, outline=ceiling_color)

    for i in range(int(HEIGHT/2)):
        r = int(lerp(0, 0 + (1 * i), 1.45))
        if r > 145:
            r = 145
        g = int(lerp(0, 0 + (1 * i), 1.33))
        if g > 133:
            g = 133
        b = int(lerp(0, 0 + (1 * i), .7))
        if b > 70:
            b = 70

        floor_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        if floor_color.find('-') != -1:
            floor_color = "#000000"
        
        canvas.create_polygon(0, HEIGHT/2 + (5 * i), WIDTH, HEIGHT/2 + (5 * i), WIDTH, HEIGHT/2 + (10 * i), 0, HEIGHT/2 + (10 * i), fill=floor_color, outline=floor_color)

    npc.update(player_pos, player_angle, maze)

    rays, npc_hit = cast_rays(player_pos, player_angle, npc.position)


    for i, (ray_length) in enumerate(rays):
        corrected = ray_angle - player_angle
        if corrected < 0:
            corrected += 2 * math.pi
        if corrected > 2 * math.pi:
            corrected -= 2
        ray_length *= 1.5*math.cos(corrected)

        wall_height = HEIGHT / ray_length * TILE_SIZE

        max_wall_height = HEIGHT
        wall_height = min(wall_height, max_wall_height)

        shadow_intensity = 1 - 5 * min(1, ray_length / 1000)

        if ray_length > 250:
            wall_color = "black"
        else:
            wall_color = "#{:02X}{:02X}{:02X}".format(
                int(145 * shadow_intensity),
                int(133 * shadow_intensity),
                int(70 * shadow_intensity)
            )

        fog_intensity = 1 - min(1, ray_length / 1000)

        r = int(lerp(0, 145, fog_intensity) * shadow_intensity)
        g = int(lerp(0, 133, fog_intensity) * shadow_intensity)
        b = int(lerp(0, 70, fog_intensity) * shadow_intensity)

        wall_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        if wall_color.find('-') != -1:
            wall_color = "#000000"

        canvas.create_rectangle(i * (WIDTH / NUM_RAYS), HEIGHT / 2 - wall_height / 2, (i + 1) * (WIDTH / NUM_RAYS), HEIGHT / 2 + wall_height / 2, fill=wall_color, outline=wall_color)

    npc.update(player_pos, player_angle, maze)

    rays, npc_hit = cast_rays(player_pos, player_angle, npc.position)

    # If NPC is hit, render it in the 3D world
    if npc_hit:
        npc_dx = npc.position[0] - player_pos[0]
        npc_dy = npc.position[1] - player_pos[1]
        npc_distance = math.sqrt(npc_dx ** 2 + npc_dy ** 2)

        # Calculate angle between player's view and NPC
        angle_to_npc = math.atan2(npc_dy, npc_dx)
        angle_difference = abs(player_angle - angle_to_npc)
        if angle_difference > math.pi:
            angle_difference = 2 * math.pi - angle_difference

        # Set a threshold angle for NPC rendering based on the field of view
        threshold_angle = FOV / 2  # Adjust this angle to fit your desired range

        # Calculate the size of the NPC based on angle difference for perspective effect
        size_multiplier = 1 + (threshold_angle - angle_difference) / threshold_angle

        # Check if the NPC is within the field of view to render it with perspective
        if npc_distance < distance_to_wall and angle_difference < threshold_angle:
            # Render NPC with perspective using raycaster
            corrected_npc_angle = math.atan2(npc_dy, npc_dx)
            if corrected_npc_angle < 0:
                corrected_npc_angle += 2 * math.pi
            if corrected_npc_angle > 2 * math.pi:
                corrected_npc_angle -= 2 * math.pi
            npc_ray_length = npc_distance * math.cos(corrected_npc_angle - player_angle)
            npc_wall_height = (HEIGHT / npc_ray_length * TILE_SIZE * size_multiplier)/2

            # Render NPC with adjusted size
            npc_width = npc_wall_height/2  # Set the width equal to the height

            npc_dx = npc.position[0] - player_pos[0]
            npc_dy = npc.position[1] - player_pos[1]
            npc_screen_x = WIDTH / 2 + npc_dx
            npc_screen_y = HEIGHT / 2 + npc_dy

            # Adjust NPC's rendering position on the screen based on relative position
            npc_render_x = (WIDTH / 2 - npc_width / 2) + npc_dx
            npc_render_y = (HEIGHT / 2 - npc_wall_height / 4)

            # Render NPC with adjusted position
            canvas.create_rectangle(npc_render_x, npc_render_y, npc_render_x + npc_width, npc_render_y + npc_wall_height / 2, fill="#800000", outline="#800000")

    draw_mini_map()

    if anim_frame % 5 == 0:
        canvas.create_image(WIDTH/2, HEIGHT-145, image=hand_image)
    else:
        canvas.create_image(WIDTH/2, HEIGHT-135, image=hand_image)

    root.after(16, update)

update()
root.mainloop()
