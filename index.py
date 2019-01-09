import pygame as pg
import time
import random

# 6th videos is running

# game initialization
pg.init()

display_height = 600
display_width = 800

black = (0,0,0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

car_width = 73

# setting game display
gameDisplay = pg.display.set_mode((display_width,display_height))

pg.display.set_caption('a bit racy')
clock = pg.time.Clock()

# loading car img
carImg = pg.image.load('racecar.png')

def game_intro():
    intro = True

    while intro:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pg.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = text_object("a bit racey", largeText)
        textRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(textSurf, textRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("QUIT!", 550, 450, 100, 50, red, bright_red, "quit")

        pg.display.update()
        clock.tick(15)

def things_dodged(count):
    font = pg.font.SysFont(None, 25)
    text = font.render(f"dodged: {str(count)}", True, black)
    gameDisplay.blit(text, (0,0))

# things
def things(thingx, thingy, thingw, thingh, color):
    pg.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# car object
def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def text_object(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pg.font.Font('freesansbold.ttf', 115)
    textSurf, textRect = text_object(text, largeText)
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)
    pg.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('You Crashed')

def button(msg, x, y, w, h, iColor, aColor, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(gameDisplay, aColor, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
            # if action == "play":
            #     game_loop()
            # elif action == "quit":
            #     pg.quit()
            #     quit()
    else:
        pg.draw.rect(gameDisplay, iColor, (x, y, w, h))

    smallText = pg.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ((x+(w/2)), y+(h/2))
    gameDisplay.blit(textSurf, textRect)


def gameQuit():
    pg.quit()
    quit()


# main game loop
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0
    gameExit = False

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    dodged = 0
# main game loop start 
    while not gameExit:
        # checking event occur
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            # keypressing event
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_change = -5
                if event.key == pg.K_RIGHT:
                    x_change = 5
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    x_change = 0

        x += x_change
        
        # display white background
        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        # car crash logic
        if x > display_width - car_width or x < 0:
            crash()
        
        # things start reappearing when they cross the total y-axis and start with random x-axis
        if thing_starty > display_width:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1

        # collosion of thing 
        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash()

        pg.display.update()
        clock.tick(60)

game_intro()
game_loop()
pg.quit()