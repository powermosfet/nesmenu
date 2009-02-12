import sys, pickle, os, init, menu, joystick

list = []

def rescan():
    global list
    list = []
    joystick.display("Please wait...")
    file = init.requireFile("collections.conf")
    lines = file.readlines()
    for x in lines:
        line = x.split(":: ")
        name = line[0]
        conf = eval(line[1])
        list.append(menu.Menu(name))
        list[-1][0] = menu.Menu("Favourites")
        list[-1][1] = menu.ColMenu("All games")
        scan = os.walk(conf["path"])
        for folder in scan:
            for file in folder[-1]:
                suffix = file.split(".")[-1]
                if suffix == conf["filetype"]:
                    gameName = file[:-1-len(suffix)]
                    list[-1][1][gameName] = menu.Exe(gameName, conf["emulator"]+' "'+folder[0]+"/"+file+'"')
    init.getMenu()
    menu.Menu.path[-1].enter()
    

def get():
    global list
    try:
        list = pickle.load(open(os.getenv("HOME") + "/.nesmenu/collections.dat", 'rb'))
    except:
        list = []

def save():
    #print list
    #try:
    pickle.dump(list, open(os.getenv("HOME") + "/.nesmenu/collections.dat", 'wb'))
    #except:
    #    print "Could not save collections database. Sorry!"
