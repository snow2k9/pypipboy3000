import pygame
import json
import gui
# from gui import header

CONFIG = json.loads(open("config/config.json","r").read())

pygame.init()
pygame.font.init()

pygame.mouse.set_visible(False)

if CONFIG["fullscreen"] == True:
    displayInfo = pygame.display.Info()
    displaySize = (displayInfo.current_w,displayInfo.current_h)
    display = pygame.display.set_mode(displaySize, pygame.FULLSCREEN)

else:
    displaySize = (1000,500)
    display = pygame.display.set_mode(displaySize)

pygame.display.set_caption("Pipboy 3000")
clock = pygame.time.Clock()

color = CONFIG["color"]

menu = gui.menu(display, displaySize, color, CONFIG)

SELECTION = {
  "menu_wheel": 0,
  "submenu_wheel": 0,
  "selector": 0
}

DISPLAY_DELAY = 100

MAX_MENU_WHEEL = 4
MIN_MENU_WHEEL = 0
MIN_SUBMENU_WHEEL = 0
MIN_SELECTOR = 0
MAX_SELECTOR = 5

def updateDisplay():
    display.fill(CONFIG["background"])
    menu.update(SELECTION)
    pygame.display.update()

def menuLoop():
    isRunning = True
    while isRunning:
        clock.tick(10)
        pygame.time.delay(DISPLAY_DELAY)

        keyPressed = False
        navKeys = pygame.key.get_pressed()

        if navKeys[pygame.K_ESCAPE]:
            keyPressed = True
            isRunning = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

        if navKeys[pygame.K_1]:
            keyPressed = True
            SELECTION["selector"] -= 1

        if navKeys[pygame.K_2]:
            keyPressed = True
            SELECTION["selector"] += 1

        if navKeys[pygame.K_LEFT]:
            keyPressed = True
            SELECTION["submenu_wheel"] -= 1

        if navKeys[pygame.K_RIGHT]:
            keyPressed = True
            SELECTION["submenu_wheel"] += 1

        if navKeys[pygame.K_UP]:
            keyPressed = True
            SELECTION["menu_wheel"] += 1
            SELECTION["submenu_wheel"] = 0

        if navKeys[pygame.K_DOWN]:
            keyPressed = True
            SELECTION["menu_wheel"] -= 1
            SELECTION["submenu_wheel"] = 0

        if SELECTION["selector"] < MIN_SELECTOR:
            SELECTION["selector"] = MIN_SELECTOR

        if SELECTION["selector"] > MAX_SELECTOR:
            SELECTION["selector"] = MAX_SELECTOR

        if SELECTION["menu_wheel"] > MAX_MENU_WHEEL:
            SELECTION["menu_wheel"] = MAX_MENU_WHEEL

        if SELECTION["menu_wheel"] < MIN_MENU_WHEEL:
            SELECTION["menu_wheel"] = MIN_MENU_WHEEL

        if SELECTION["submenu_wheel"] > len(menu.submenu[menu.menu[SELECTION["menu_wheel"]]]) - 1:
            SELECTION["submenu_wheel"] = len(menu.submenu[menu.menu[SELECTION["menu_wheel"]]]) - 1

        if SELECTION["submenu_wheel"] < MIN_SUBMENU_WHEEL:
            SELECTION["submenu_wheel"] = MIN_SUBMENU_WHEEL

        if keyPressed == True & CONFIG["debug"] == True:
            print(SELECTION)

        updateDisplay()


menuLoop()

pygame.quit()
