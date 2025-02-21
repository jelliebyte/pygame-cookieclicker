import pygame
import json

pygame.init() # initializes pygame

running = True
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #setting up screen
pygame.display.set_caption("Cookie Clicker") #set window caption
clock = pygame.time.Clock()
cookies_per_second = 0
AUTO_INCRIMENTAL = 1000
last_auto_incrimental = pygame.time.get_ticks()
score = 0
num_upgrades = 0


font = pygame.font.SysFont("Ariel", 30)

class GenericButton():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

button = GenericButton(400, 300, 150, 50)

def isInside(x,y,width,height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if (x <= mouse_x <= x + width and
        y <= mouse_y <= y + height):
        return True

cookie_image = pygame.image.load("images\cookie.png")
cookie_size = (100, 100) # set size of cookie PNG
cookie_image = pygame.transform.scale(cookie_image, cookie_size) # scales cookie down

cookie_x = 250
cookie_y = 150

background_image = pygame.image.load("images\spacedust.png")
background_size = (600,500)
background_image = pygame.transform.scale(background_image, background_size)

button_color = (255,0,0)

cookie_state = {"scale": 1.0, "direction": 1}

def save_game(score,num_upgrades,cookies_per_second):
    save_data = {
        "score": score,
        "cookies_per_second": cookies_per_second,
        "num_upgrades": num_upgrades
    }
    with open("save_file.json", "w") as save_file:
        json.dump(save_data, save_file)

def load_game():
    try:
        with open("save_file.json", "r") as save_file:
            return json.load(save_file)
    except FileNotFoundError:
        return None
saved_data = load_game()
if saved_data:
    score = saved_data["score"]
    cookies_per_second = saved_data["cookies_per_second"]
    num_upgrades = saved_data["num_upgrades"]

while running: # while running is true
    upgrade_cost = int(50 * (1.2 ** num_upgrades))  # Base cost grows exponentially
    # incriment cookies per second
    current_time = pygame.time.get_ticks()
    if current_time - last_auto_incrimental >= AUTO_INCRIMENTAL:
        score += cookies_per_second
        last_auto_incrimental = current_time

    # change upgrade button states
    if (score >= upgrade_cost):
        button_color = (0,200,0)
    else:
        button_color = (255,0,0)
    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if an event is equal to pygame quit
            running = False # running if false
        #cookie & button clicks + cookie animation states
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if isInside(cookie_x, cookie_y, cookie_size[0], cookie_size[1]):
                score += 1
                cookie_state["direction"] = -1
            elif isInside(button.x, button.y, button.width, button.height):
                if score >= 50:
                    score -= 50
                    num_upgrades += 1
                    cookies_per_second += 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s:
                save_game(score,num_upgrades,cookies_per_second)
    screen.fill((69, 69, 69)) # fill background
    score_text = font.render(f"Score: {score}", True, (255,255,255)) # renders text, applies antialias, and updates color
    screen.blit(background_image, (0,0)) # draw background image
    screen.blit(score_text, (10,10)) # draw score on screen at x = 10, y = 10
    if (cookie_state["direction"] != 0):
            cookie_state["scale"] += 0.05 * cookie_state["direction"]
    if cookie_state["scale"] <= 0.9:
            cookie_state["direction"] = 1  # Start expanding
    elif cookie_state["scale"] >= 1.0:
            cookie_state["direction"] = 0  # Stop bouncing
    scaled_cookie = pygame.transform.scale(cookie_image, (int(cookie_size[0] * cookie_state["scale"]), int(cookie_size[1] * cookie_state["scale"])))
    screen.blit(scaled_cookie, (cookie_x, cookie_y))
    pygame.draw.rect(screen, button_color, (button.x, button.y, button.width, button.height)) # new button
    cost_text = font.render(f"Cost: {upgrade_cost}", True, (255,255,255))
    button_text = font.render(f"Upgrade", True, (255, 255, 255)) # adds button font
    upgrades_text = font.render(f"Upgrades: {num_upgrades}", True, (255,255,255))
    screen.blit(button_text, (button.x + 20, button.y + 5)) # draws button to screen
    screen.blit(cost_text, (button.x + 20, button.y + 30))
    screen.blit(upgrades_text, (button.x + 20, button.y - 30))
    pygame.display.flip() # constantly update screen
    clock.tick(60) # limits FPS to 60 FPS a second
pygame.quit()
