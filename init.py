import os, sys, pygame, menu, db, joystick, shutil
from pygame.locals import *

pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)

installDir = os.path.dirname(os.path.abspath(__file__))

def requireFile(fileName):
    """look in the current dir first, then the home dir
    """
    try:
        f = open(os.path.join( installDir, fileName), 'r')
    except:
        print "no local file ", fileName
        pass

    try:
        os.chdir(os.path.expanduser("~/.nesmenu"))
    except:
        try:
            os.makedirs(os.path.expanduser("~/.nesmenu"))
        except:
            print "Could not create directory", os.path.expanduser("~/.nesmenu"), "aborting..."
            sys.exit()
    finally:
        try:
            f = open(os.path.expanduser("~/.nesmenu/") + fileName, 'r')
        except:
            try:
                shutil.copy(os.path.join(installDir,fileName), os.path.expanduser("~/.nesmenu/"))
            except:
                print "Could not create file", os.path.expanduser("~/.nesmenu/") + fileName, "aborting..."
                sys.exit()
            else:
                print "Copied default file", fileName, "to", os.path.expanduser("~/.nesmenu")
                f = open(os.path.expanduser("~/.nesmenu/") + fileName, 'r')
        finally:
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

def exit(message = ""):
    print message
    db.save()
    sys.exit()

def mergeFlags(c):
    for x in sys.argv:
        if (x.find('--', 0, 2) == -1):
            continue
        k,junk,v = x.replace('--', '').partition('=')
        c[k] = v


def checkConfig(c):
    return 1
    try:
        if (c['warnMissingJs'] == 1 and not "js0" in os.listdir("/dev/input")):
            print "Warning: No joystick connected"
    except KeyError:
        pass 

def startDisplay():
	global config
	displayFlags = 0
	if 'useFullscreen' not in config or config['useFullscreen'] == 0:
		displayFlags = 0
		displaySize = (640, 480)
	else:
		displayFlags |= pygame.FULLSCREEN
		displaySize = (0, 0)

	config['screen'] = pygame.display.set_mode( displaySize , displayFlags )


config = readConfig()

mergeFlags(config)

checkConfig(config)

os.chdir(installDir)

startDisplay()

config['font']   = pygame.font.Font(config['font'], config['textSize'])

joystick.display("Initializing...")

db.get()
getMenu()
menu.Menu.path[-1].enter()

