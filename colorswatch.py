"""
SWATCH USE
As variables: in any argument requiring a color value,
indicate the name of the color and its dictionary key.
This library can be used for any project that requires
colors to be called through RGB or HEX.

Library configured specifically for PyGame or tKinter
use. However, Values can be changed from "pygame" to 
"RGB", etc. if necessary.


Simply run:
    import colorswatch

Call Example:
    import colorswatch as cs

    pygame:
        import pygame
        pygame.draw.rect(display, cs.blue["pygame"], [x,y,sizeX,sizeY])
    tkinter:
        from tkinter import *
        something = label(root, text="Something", fg=cs.puke["tk"], bg=cs.cornflower_blue["tk"])

Call on help() to see the list of functions and callings for this library.


ADDING NEW COLORS:
Go to https://www.colorspire.com/rgb-color-wheel/ and select a color on the color wheel.
Make your entry in one of the categories below, define as a DICTIONARY.
Use both RGB and HEX to define your custom color. PYGAME module uses RGB in a Tuple. 
tKinter uses HEX in a string. 

Example: some_color = {"pygame": (###,###,###), "tk": "#AAAAAA"}
New color will be automatically added to the list of colors to be searched/parsed though

©2022 Michael Yamazaki-Fleisher. OPEN SOURCE! Feel free to distribute even for your
own commercial projects. Inquiries can be made to mbfleish1105@live.com .

"""

#####################################################
# COLORS  ###### ADD YOUR CUSTOM COLORS HERE ###### #
#####################################################

# Blues
blue = {"pygame": (0,0,255), "tk": "#000FF"}
cornflower_blue = {"pygame": (100,149,237), "tk": "#6495ED"}
sky_blue = {"pygame":(51,153,255), "tk": "#3399FF"}
neon_blue = {"pygame": (107,255,221), "tk": "#6BFFDD"}
purple_rain = {"pygame": (106,77,255), "tk": "#6A4DFF"}
deep_purple = {"pygame": (1, 6, 92), "tk": "#01068E"}

# Yellows
golden_shower = {"pygame": (204,204,0), "tk": "#CCCC00"}
mustard = {"pygame": (255,255,77), "tk": "#FFE14D"}
gold = {"pygame": (204,170,0), "tk": "#CCAA00"}
yellow = {"pygame": (255,255,0), "tk": "#FFFF00"}

# Greens
green ={"pygame": (0,255,0), "tk": "#00FF00"}
bile = {"pygame": (0,102,17), "tk": "#006611"}
puke = {"pygame": (68,102,0), "tk": "#446600"}

# Reds
tangelo = {"pygame": (249,77,0), "tk": "#F94D00"}
red ={"pygame": (255,0,0), "tk": "#FF0000"}
fuchsia = {"pygame": (255,25,255), "tk": "#FF19FF"}

# Browns
brown = {"pygame": (165, 139, 86), "tk": "#A48B56"}
shit = {"pygame": (77,51,0), "tk": "#4D3300"}


# MONOCRHOME GRAYSCALE
white = {"pygame": (255,255,255), "tk": "#FFFFFF"}
light_gray = {"pygame": (220,220,220), "tk": "#DCDCDC"}
medium_gray = {"pygame": (197, 199, 199), "tk": "#C5C7C7"}
gray = {"pygame": (175,176,176), "tk": "#AFB0B0"}
dark_gray = {"pygame": (134,135,135), "tk": "#868787"}
night_gray = {"pygame": (91,92,92), "tk": "#5B5C5C"}
black = {"pygame": (0,0,0), "tk": "#000000"}


#############################
# ####### FUNCTIONS ####### #
#############################

def define_color(color, mod = None):
    # Returns the value of a particular color
    try:
        if mod == None:
            print(color)
        else:
            print(color[mod])
    except KeyError:
        print("Error: Key not found")


def list_scale():
    # Lists the scales
    scales = ["blue", "yellow", "green", "red", "brown", "monochrome"]
    for i in range(0, len(scales)):
        print(scales[i])


def list_color(scale = None):
    # Lists the colors. If scale specified, only the scale 
    # associated with those colors will be displayed
    blue = ["blue", "cornflower_blue", "sky_blue", "neon_blue"]
    yellow = ["golden_shower", "mustard", "gold", "yellow"]
    green = ["green", "bile", "puke"]
    red = ["tangelo", "red", "purple_rain", "fuchsia"]
    brown = ["shit", "brown"]
    monochrome = ["white", "light_gray", "medium_gray", "gray", "dark_gray", "night_gray", "black"]

    if scale == None:
        for i in range(0, len(blue)):
            print(blue[i])
        for i in range(0, len(yellow)):
            print(yellow[i])
        for i in range(0, len(green)):
            print(green[i])
        for i in range(0, len(red)):
            print(red[i])
        for i in range(0, len(brown)):
            print(brown[i])
        for i in range(0, len(monochrome)):
            print(monochrome[i])

    if scale == "blue":
        for i in range(0, len(blue)):
            print(blue[i])
    elif scale == "yellow":
        for i in range(0, len(yellow)):
            print(yellow[i])
    elif scale == "green":
        for i in range(0, len(green)):
            print(green[i])
    elif scale == "red":
        for i in range(0, len(red)):
            print(red[i])
    elif scale == "brown":
        for i in range(0, len(brown)):
            print(brown[i])
    elif scale == "monochrome":
        for i in range(0, len(monochrome)):
            print(monochrome[i])

    else:
        print("Error: Color scale not found")


def help():
    print("Functions: define_color(color, mod = None) - 1 required argument, 1 optional argument")
    print('                        mod = "tk" or mod = "pygame"')
    print(" Declare a mod for a specific value, declare nothing to get all values for that color.")
    print("           list_scale() - 0 arguments")
    print("           list_color(scale = None) - 1 optional argument")
    print('                        scale = "blue"')
    print(" Declare nothing for a full list of colors. Declare a color scale as a string for specific")
    print(" colors in that scale.")


## END OF FILE ##