import pygame
import math
import sys

# ------------------------------
# Element data (first 30)
# ------------------------------
elements = {
    1: ("Hydrogen", "H", 1),
    2: ("Helium", "He", 4),
    3: ("Lithium", "Li", 7),
    4: ("Beryllium", "Be", 9),
    5: ("Boron", "B", 11),
    6: ("Carbon", "C", 12),
    7: ("Nitrogen", "N", 14),
    8: ("Oxygen", "O", 16),
    9: ("Fluorine", "F", 19),
    10: ("Neon", "Ne", 20),
    11: ("Sodium", "Na", 23),
    12: ("Magnesium", "Mg", 24),
    13: ("Aluminium", "Al", 27),
    14: ("Silicon", "Si", 28),
    15: ("Phosphorus", "P", 31),
    16: ("Sulfur", "S", 32),
    17: ("Chlorine", "Cl", 35),
    18: ("Argon", "Ar", 40),
    19: ("Potassium", "K", 39),
    20: ("Calcium", "Ca", 40),
    21: ("Scandium", "Sc", 45),
    22: ("Titanium", "Ti", 48),
    23: ("Vanadium", "V", 51),
    24: ("Chromium", "Cr", 52),
    25: ("Manganese", "Mn", 55),
    26: ("Iron", "Fe", 56),
    27: ("Cobalt", "Co", 59),
    28: ("Nickel", "Ni", 59),
    29: ("Copper", "Cu", 64),
    30: ("Zinc", "Zn", 65)
}

# ------------------------------
# Electron shell calculation
# ------------------------------
def electron_shells(electrons):
    shells = []
    shell_limits = [2, 8, 18]
    for limit in shell_limits:
        if electrons > 0:
            shells.append(min(electrons, limit))
            electrons -= limit
    return shells

# ------------------------------
# Pygame setup
# ------------------------------
pygame.init()
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultra-Realistic Atomic Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
nucleus_font = pygame.font.SysFont(None, 28)

# Colors
shell_colors = [(255, 50, 50), (255, 165, 0), (0, 255, 0), (0, 0, 255)]
electron_color = (0, 255, 255)
nucleus_color = (255, 215, 0)
bg_color = (10, 10, 30)
button_color = (70, 130, 180)
button_hover = (100, 160, 210)
text_color = (255, 255, 255)

# ------------------------------
# Input Box for atomic number
# ------------------------------
def get_atomic_number():
    input_box = pygame.Rect(WIDTH//2-150, HEIGHT//2-30, 300, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.isdigit() and 1 <= int(text) <= 30:
                            return int(text)
                        else:
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(bg_color)
        prompt = font.render("Enter Atomic Number (1-30) and press Enter:", True, text_color)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2-90))
        txt_surface = font.render(text, True, text_color)
        width_box = max(300, txt_surface.get_width()+10)
        input_box.w = width_box
        screen.blit(txt_surface, (input_box.x+10, input_box.y+15))
        pygame.draw.rect(screen, color, input_box, 3)
        pygame.display.flip()
        clock.tick(30)

# ------------------------------
# Initialize element
# ------------------------------
def init_element(atomic_number):
    name, symbol, mass = elements[atomic_number]
    shells = electron_shells(atomic_number)
    protons = atomic_number
    neutrons = mass - atomic_number
    angles = [0] * len(shells)
    tilts = [math.radians(0), math.radians(25), math.radians(50), math.radians(75)]
    speeds = [0.04/(i+1) for i in range(len(shells))]
    electron_trails = [[] for _ in shells]
    return {
        'name': name, 'symbol': symbol, 'mass': mass,
        'shells': shells, 'protons': protons, 'neutrons': neutrons,
        'angles': angles, 'speeds': speeds, 'tilts': tilts, 'electron_trails': electron_trails
    }

# Initial element
atomic_number = get_atomic_number()
element = init_element(atomic_number)

# Button
button_rect = pygame.Rect(WIDTH-260, 20, 240, 60)

# ------------------------------
# Main loop
# ------------------------------
running = True
while running:
    screen.fill(bg_color)
    cx, cy = WIDTH//2, HEIGHT//2 + 50
    radius_base = 140  # Bigger base radius

    # Draw glowing nucleus
    pygame.draw.circle(screen, (255, 215, 50, 50), (cx, cy), 100)  # glow layer
    pygame.draw.circle(screen, nucleus_color, (cx, cy), 100)
    total = element['protons'] + element['neutrons']
    for i in range(total):
        angle = 2*math.pi*i/total
        r = 50
        px = cx + int(r*math.cos(angle))
        py = cy + int(r*math.sin(angle))
        color = (255, 0, 0) if i < element['protons'] else (150, 150, 150)
        pygame.draw.circle(screen, color, (px, py), 10)  # bigger dots

    # Draw shells and electrons with 3D tilt and trails
    for i, electrons in enumerate(element['shells']):
        radius = radius_base + i*100
        tilt = element['tilts'][i % len(element['tilts'])]
        pygame.draw.circle(screen, shell_colors[i%len(shell_colors)], (cx, cy), radius, 3)

        for j in range(electrons):
            angle = element['angles'][i] + (2*math.pi/electrons)*j
            ex = cx + int(radius * math.cos(angle))
            ey = cy + int(radius * math.sin(angle) * math.cos(tilt))

            # electron trails
            element['electron_trails'][i].append((ex, ey))
            if len(element['electron_trails'][i]) > 25*electrons:
                element['electron_trails'][i] = element['electron_trails'][i][-25*electrons:]
            for k, pos in enumerate(element['electron_trails'][i][-25:]):
                alpha = int(255*(k+1)/25)
                trail_surface = pygame.Surface((14,14), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (*electron_color, alpha), (7,7), 7)
                screen.blit(trail_surface, (pos[0]-7, pos[1]-7))

            # Draw electron
            pygame.draw.circle(screen, electron_color, (ex, ey), 12)

            # Hover info
            mouse_pos = pygame.mouse.get_pos()
            if math.hypot(mouse_pos[0]-ex, mouse_pos[1]-ey) < 12:
                info_text = font.render(f"Electron in shell {i+1}", True, (255,255,0))
                screen.blit(info_text, (mouse_pos[0]+15, mouse_pos[1]))

        element['angles'][i] += element['speeds'][i]

    # Display element info
    info = f"{element['name']} ({element['symbol']})  |  Atomic Number: {atomic_number}  |  Mass: {element['mass']}"
    config = "Electron configuration (K,L,M,...): " + " ".join([str(e) for e in element['shells']])
    screen.blit(font.render(info, True, text_color), (10, 10))
    screen.blit(font.render(config, True, text_color), (10, 50))

    # Draw change element button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover, button_rect)
    else:
        pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Change Element", True, text_color)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 15))

    pygame.display.flip()
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                atomic_number = get_atomic_number()
                element = init_element(atomic_number)

pygame.quit()