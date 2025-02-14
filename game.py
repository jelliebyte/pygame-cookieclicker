import pygame

pygame.init() # initializes pygame

running = True #  
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #setting up screen
pygame.display.set_caption("Cookie Clicker") #set window caption
clock = pygame.time.Clock()

font = pygame.font.SysFont("Ariel", 30)

score = 0

cookie_image = pygame.image.load("images\cookie.png")
cookie_size = (100, 100) # set size of cookie PNG
cookie_image = pygame.transform.scale(cookie_image, cookie_size) # scales cookie down

cookie_x = 250
cookie_y = 150

background_image = pygame.image.load("images\spacedust.png  ")
background_size = (600,500)
background_image = pygame.transform.scale(background_image, background_size)

while running: # while running is true
    for event in pygame.event.get(): # gets all pygame events
        if event.type == pygame.QUIT: # if an event is equal to pygame quit
            running = False # running if false
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (cookie_x <= mouse_x <= cookie_x + cookie_size[0] and
                cookie_y <= mouse_y <= cookie_y + cookie_size[1]):
                score += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill((69, 69, 69)) # fill background
    score_text = font.render(f"Score: {score}", True, (255,255,255)) # renders text, applies antialias, and updates color
    screen.blit(background_image, (0,0))
    screen.blit(score_text, (10,10)) # draw score on screen at x = 10, y = 10
    screen.blit(cookie_image,(cookie_x, cookie_y)) # draw cookie on screen
    pygame.display.flip() # constantly update screen
    clock.tick(60) # limits FPS to 60 FPS a second
pygame.quit()
