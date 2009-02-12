#! /usr/bin/env python

import sys, pygame, time, os, init, menu, joystick
from pygame.locals import *

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            init.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            init.exit()
        elif ( event.type == KEYDOWN and event.key == K_DOWN ) or joystick.checkEvent(event, "down"):
            menu.Menu.path[-1].down()
        elif ( event.type == KEYDOWN and event.key == K_UP ) or joystick.checkEvent(event, "up"):
            menu.Menu.path[-1].up()
        elif ( event.type == KEYDOWN and event.key == K_RIGHT ) or ( event.type == KEYDOWN and event.key == K_RETURN ) or joystick.checkEvent(event, "enter"):
            list = menu.Menu.path[-1].keys()
            list.sort()
            if len(list) > 0: menu.Menu.path[-1][list[menu.Menu.path[-1].selected]].enter()
        elif ( event.type == KEYDOWN and event.key == K_LEFT ) or joystick.checkEvent(event, "back"):
            menu.Menu.path[-1].left()
        elif ( event.type == KEYDOWN and event.key == K_f ) or joystick.checkEvent(event, "favourite"):
            menu.Menu.path[-1].toggleFav()
        elif ( event.type == KEYDOWN and event.key == K_PAGEUP ) or joystick.checkEvent(event, "pgup"):
            menu.Menu.path[-1].pgup()
        elif ( event.type == KEYDOWN and event.key == K_PAGEDOWN ) or joystick.checkEvent(event, "pgdown"):
            menu.Menu.path[-1].pgdn()
        elif event.type == KEYDOWN and event.key == K_w:
            pygame.display.toggle_fullscreen()
    if sys.argv[-1] != "--no-joystick" and not pygame.joystick.get_count():
        init.exit()