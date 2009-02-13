import init, pygame, pickle, os, time, menu
from pygame.locals import *

joyObject = None
joyCount = 0

def joyInit():
    global joyObject
    joyCount = detectJoy()

    try:
        returnConfig = pickle.load(open(os.getenv("HOME") + "/.nesmenu/joysetup", 'rb'))
    except:
        returnConfig = {}
        events = [ "up", "down", "enter", "back", "pgup", "pgdown", "favourite" ]
        for x in events:
            returnConfig[x] = None
    return returnConfig

def detectJoy():
    """Quit and init must be called constantly because pygame caches the 
    number of joysticks on init().  So you cannot detect an unplug event
    w/o quitting the joystick module
    """
    global joyObject
    if joyObject != None:
       joyObject.quit()

    pygame.joystick.quit()
    pygame.joystick.init()
    simpleCount =  pygame.joystick.get_count()
    if simpleCount > 0:
        joyObject = pygame.joystick.Joystick(pygame.joystick.get_count()-1)
        joyObject.init()

	return simpleCount

def display(message):
    init.config['screen'].fill(init.config['bgColor'])
    text = init.config['font'].render(message , 1, init.config['textColor'])
    textRect = text.get_rect()
    textRect.centery = init.config['screen'].get_rect().centery
    textRect.centerx = init.config['screen'].get_rect().centerx
    init.config['screen'].blit(text, textRect)
    pygame.display.flip()    

def joySetup():
    global joystick
    if not pygame.joystick.get_count():
        return joyInit()
    joystick = {}
    events = [ "up", "down", "enter", "back", "pgup", "pgdown", "favourite" ]
    for event in events:
        display("Please press " + event)
        e = waitForEvent()
        joystick[event] = {}
        if e.type == JOYAXISMOTION:
            joystick[event]["type"] = "axis"
            joystick[event]["joy"] = e.joy
            joystick[event]["axis"] = e.axis
            joystick[event]["value"] = e.value
        elif e.type == JOYBUTTONDOWN:
            joystick[event]["type"] = "button"
            joystick[event]["joy"] = e.joy
            joystick[event]["button"] = e.button
        display("OK!")
        time.sleep(1)
    try:
        pickle.dump(joystick, open(os.getenv("HOME") + "/.nesmenu/joysetup", 'wb'))
    except:
        print "Could not save joystick settings... Sorry!"
    menu.Menu.path[-1].enter()

def waitForEvent():
    returnEvent = None
    pygame.event.clear()
    while 1:
        for event in pygame.event.get():
            print event
            if event.type == JOYBUTTONDOWN:
                returnEvent = event
            elif event.type == JOYAXISMOTION and ( event.value > 0.5 or event.value < -0.5 ):
                returnEvent = event
        if returnEvent:
            return returnEvent
                
def checkEvent(event, command):
    if joystick[command] and event.type == JOYBUTTONDOWN and joystick[command]["type"] == "button" and joystick[command]["joy"] == event.joy and joystick[command]["button"] == event.button:
        return True
    if joystick[command] and event.type == JOYAXISMOTION and joystick[command]["type"] == "axis" and joystick[command]["joy"] == event.joy and joystick[command]["axis"] == event.axis:
        if event.value == 0:
            return False
        #check strength of pads
        if event.value > 0 and  joystick[command]["value"] > 0 and joystick[command]["value"] <= event.value:
            #print  joystick[command]["value"], event.value
            return True

        if event.value < 0 and  joystick[command]["value"] < 0 and joystick[command]["value"] >= event.value:
            print joystick[command]["value"],  event.value
            return True
    return False
    
joystick = joyInit()
