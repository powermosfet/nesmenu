import os, sys, pygame, menu, db, joystick
from pygame.locals import *
pygame.init()
pygame.mouse.set_visible(False)

installDir = "/home/asmund/Dokumenter/programmering/nesmenu2/"

def requireFile(fileName):
    try:
        os.chdir(os.getenv("HOME") + "/.nesmenu")
    except:
        try:
            os.makedirs(os.getenv("HOME") + "/.nesmenu")
        except:
            print "Could not create directory", os.getenv("HOME") + "/.nesmenu", "aborting..."
            sys.exit()
    else:
        try:
            f = open(os.getenv("HOME") + "/.nesmenu/" + fileName, 'r')
        except:
            try:
                shutil.copy(installDir + fileName, os.getenv("HOME") + "/.nesmenu/")
            except:
                print "Could not create file", os.getenv("HOME") + "/.nesmenu/" + fileName, "aborting..."
                sys.exit()
            else:
                print "Copied default file", fileName, "to", os.getenv("HOME")+"/.nesmenu"
        else:
            return f
        
def readConfig():
    localConfig = {}
    configFile = requireFile("config")
    configLines = configFile.readlines()
    for x in configLines:
        splitted = x.split(": ")
        data = eval(splitted[1])
        localConfig[splitted[0]] = data
    return localConfig

def getMenu():
    #print db.list
    menuFile = requireFile("menu.cfg")
    menuLines = menuFile.readlines()
    menu.Menu.path.append(menuParse(menuLines))

def menuParse(lines):
    line = lines[0].split(": ")
    del(lines[0])
    index = 0
    if not line[0].strip() == "menu":
        print "Error parsing menu file. Aborting..."
        sys.exit()
    returnMenu = menu.Menu(line[-1].strip())
    line = lines[0].split(": ")
    while line[0].strip() != ".menu" and len(lines):
        if line[0].strip() == "menu":
            returnMenu[index] = menuParse(lines)
            while lines[0].strip() != ".menu":
                del(lines[0])
            if not len(lines):
                return returnMenu
        elif line[0].strip() == "<db>":
            for x in db.list:
                returnMenu[index] = x
                index += 1
            del(lines[0])
            line = lines[0].split(": ")
            continue
        elif line[0].strip() == "func":
            returnMenu[index] = menu.Func(line[1].strip(), line[2].strip())
        elif line[0].strip() == "exec":
            returnMenu[index] = menu.Exe(line[1].strip(), line[2].strip())            
        del(lines[0])
        line = lines[0].split(": ")
        index += 1
    return returnMenu

def exit():
    db.save()
    sys.exit()

config = readConfig()

os.chdir(installDir)
config['screen'] = pygame.display.set_mode( (0,0) , pygame.FULLSCREEN )
config['font'] = pygame.font.Font(config['font'], config['textSize'])

joystick.display("Initializing...")

db.get()
getMenu()
menu.Menu.path[-1].enter()

