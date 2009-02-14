import pygame, os, init, pickle, time, sys, db, copy, joystick

class Item(object):
    def __init__(self, name):
        self.name = name
        self.starred = False

class Menu(dict, Item):
    path = []

    def __init__(self, name, data = {}):
        dict.__init__(self, data)
        Item.__init__(self, name)
        self.start = self.selected = 0
        self.fontHeight = init.config['font'].get_height()
    
    def enter(self):
        if (not Menu.path) or (not Menu.path[-1] is self):
            Menu.path.append(self)
        itemList = self.keys()
        itemList.sort()
        init.config['screen'].fill(init.config['bgColor'])
        text = init.config['font'].render(self.name, 1, init.config['textColor'])
        textRect = text.get_rect()
        textRect.centerx = init.config['screen'].get_rect().centerx
        textRect.top = self.fontHeight
        init.config['screen'].blit(text, textRect)
        startY = 3.5 * self.fontHeight
        if init.config['itemsPerPage'] > len(self):
            itemsToDisplay = len(self)
        else:
            itemsToDisplay = init.config['itemsPerPage']
        for i in range(itemsToDisplay):
            text = init.config['font'].render("   " + self[itemList[self.start + i]].name, 1, init.config['textColor'])
            textRect = text.get_rect()
            textRect.topleft = (0, startY + i*self.fontHeight*init.config['linespace'])
            init.config['screen'].blit(text, textRect)
        text = init.config['font'].render(" >" , 1, init.config['textColor'])
        textRect = text.get_rect()
        textRect.topleft = (0, startY + (self.selected - self.start)*self.fontHeight*init.config['linespace'])
        init.config['screen'].blit(text, textRect)
        text = init.config['font'].render("*" , 1, init.config['textColor'])
        textRect = text.get_rect()
        for x in range(init.config['itemsPerPage']):
            textRect.topleft = (0, startY + x*self.fontHeight*init.config['linespace'])
            if (self.start + x) < len(itemList) and self[itemList[self.start + x]].starred:
                init.config['screen'].blit(text, textRect)
        pygame.display.flip()

    def left(self):
        if len(Menu.path) > 1:
            Menu.path.pop()
            Menu.path[-1].enter()
        
    def up(self):
        if self.selected == 0 and len(self) > 0:
            self.selected = len(self) - 1
            if len(self) < init.config['itemsPerPage']:
                self.start = 0
            else:
                self.start = len(self) - init.config['itemsPerPage']
        elif self.selected > 0 and len(self) > 0:
            self.selected -= 1
            if self.selected < self.start:
                self.start = self.selected
        self.enter()

    def down(self):
        self.selected += 1
        if self.selected >= len(self):
            self.start = self.selected = 0
        else:
            if self.selected >= self.start + init.config['itemsPerPage']:
                self.start = self.selected - init.config['itemsPerPage'] + 1
        self.enter()

    def pgup(self):
        self.start -= init.config['itemsPerPage']
        if self.start < 0: self.start = 0
        self.selected = self.start
        self.enter()

    def pgdn(self):
        self.start += init.config['itemsPerPage']
        if self.start > len(self) - init.config['itemsPerPage']:
            self.start = len(self) - init.config['itemsPerPage']
        self.selected = self.start
        self.enter()

    def toggleFav(self):
        pass

class Func(Item):
    def __init__(self, name, func):
        Item.__init__(self, name)
        self.func = func

    def enter(self):
        eval(self.func)
        
class Exe(Item):
    def __init__(self, name, command):
        Item.__init__(self, name)
        self.command = command

    def enter(self):
        if joystick.joyObject:
            joystick.joyObject.quit()
        pygame.joystick.quit()
        pygame.font.quit()
        pygame.display.quit()
        os.system(self.command)
        time.sleep(1)
        pygame.display.init()
        init.startDisplay()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        pygame.joystick.init()
        if joystick.joyObject:
            joystick.joyObject.init()
        Menu.path[-1].enter()

class ColMenu(Menu):
    def toggleFav(self):
        itemList = self.keys()
        itemList.sort()
        self[itemList[self.selected]].starred = not self[itemList[self.selected]].starred
        if self[itemList[self.selected]].starred and not self.path[-2][0].has_key(itemList[self.selected]):
            Menu.path[-2][0][itemList[self.selected]] = copy.copy( self[itemList[self.selected]] )
            Menu.path[-2][0][itemList[self.selected]].starred = False
        if not self[itemList[self.selected]].starred and Menu.path[-2][0].has_key(itemList[self.selected]):
            del( Menu.path[-2][0][itemList[self.selected]] )
        self.enter()
