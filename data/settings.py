import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

GAME_TITLE = "OPERATION:\nBELIEVE IN THE SCIENCE\nOR ELSE"
TITLE_FONT_SIZE = 60 

FONT_SIZE = 45

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)  
RED = (255, 0, 0)
ORANGE = (255, 165, 0)  

DIRECTION_DICT = {
            "up": 0,
            "down": 180,
            "right": 270,
            "left": 90,
            "up_right": 315,
            "up_left": 45,
            "down_right": 225,
            "down_left": 135
        }

WALL_THICKNESS = 10
WALL_OPENING_SIZE = 150