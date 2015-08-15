#Tiletype
"""
9 - end of enemy path (you lose life if they make it here)
8 - start of enemy path
7 - non building area (UI)
6 - capacitors?
1 - path
0 - background
"""
TILETYPE = ["background","path","weapon","unused","unused","unused","capacitors","nobuild","pathstart","pathend"]

#TODO: move to config file
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CELL_SIZE = 64
BOARD_WIDTH = 16
BOARD_HEIGHT = 12

BGCOLOR = (0,160,0)
PATHCOLOR = (150,150,0)
UIBGCOLOR = (125,125,125)
BLACK = (0,0,0)
PATHSTARTCOLOR = (0,0,255)
PATHENDCOLOR = (255,0,0)

HEALTH_TXT = "DATA! DATA! DATA!"
