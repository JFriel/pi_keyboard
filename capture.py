import json
import string
from getch import getch
from colour import Color
from blinkt import show, clear, set_brightness, set_pixel
layer_lookup = {
        "_LAYER_0":0,
        "_LAYER_1":1
    }

LAYER = 0
NULL_CHAR = chr(0)

def write_report(report):
    with open("/dev/hidg0","rb+") as fd:
        fd.write(report.encode())
        fd.write(NULL_CHAR*8) #release key


def action_to_report((keycode,modifier)):
    #turn the lookup action into a usable report
    if modifier:
        print(keycode)
        #it uses the other keyboard item ie capital
        return chr(32)+NULL_CHAR+chr(keycode)+NULL_CHAR*5
    else:
        return NULL_CHAR*2+chr(keycode)+NULL_CHAR*5


def get_hid(char):
    if char in hid_lookup.keys():
        return hid_lookup[char], False
    elif ord(char) in range(1,64):
            #ctrl
            print("ctrl",char,ord(char))
    elif ord(char) in range(65,96):
      #shift
      return hid_lookup[chr(ord(char)+32)],True
    else:
        return NULL_CHAR, False


def lookup(keycode):
    global LAYER
    #this should lookup the correct keyocde/action based on a config file
    if keycode is 120: # x is the exit handler for now
        exit()

    mapped_keycodes = []
    hids = []
    
    char = unicode(chr(keycode))
    if char in config[str(LAYER)]['mapping'].keys():
        char = config[str(LAYER)]['mapping'][char]
        if(char in layer_lookup.keys()):
            LAYER = layer_lookup[char]
            set_color(config,LAYER)
            return hids
        for c in char:
            mapped_keycodes.append(c)
    else:
        mapped_keycodes.append(char)
    for keycode in mapped_keycodes:
        hids.append(get_hid(keycode))
    return hids


def set_color(config,layer):
   clear()
   if "blinkt_colour" in config[str(layer)]['settings'].keys():
       layer_colour = config[str(layer)]['settings']['blinkt_colour']
       r,g,b = Color(layer_colour).rgb
       set_brightness(0.1)
       set_pixel(0,r,g,b)#todo make this the actual color
   show()

if __name__ == '__main__':
    with open("./hids.json") as hid:
      hid_lookup = json.load(hid);
      config = json.loads(open("config.json").read())
      set_color(config,LAYER)
      while True:
              actions = lookup(ord(getch()))
              for action in actions:
                  report = action_to_report(action)
                  write_report(report)
