from tkinter import *
from tkinter import font
import math


def color_from_temp(temperature):

    # min_temp -> (0, 0, 255), max_temp -> (255, 0, 0)
    min_temp = 10
    max_temp = 50

    if temperature < min_temp:
        temperature = min_temp
    elif temperature > max_temp:
        temperature = max_temp

    red = int(temperature * 255 / max_temp)
    blue = int((max_temp - temperature) * 255 / max_temp)

    color = '#%02x%02x%02x' % (red, 0, blue)

    return color


class Exchanger:

    GRAY = '#666'
    BLUE = '#ccf'

    FONT = None

    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        Exchanger.FONT = font.Font(family='Courier', size=13, weight='bold')
        
        self.t_hot_in = 50
        self.t_hot_out = 30
        self.t_cold_in = 10
        self.t_cold_out = 45
        self.t_m = 30

        self.draw()


    def draw(self):
        offset = 20
        arrow_len = 75
        dash = (5, 3)
        
        mid_x, mid_y = self.x + self.width / 2, self.y + self.height / 2
        x1, y1 = self.x, self.y
        x2, y2 = x1, self.y + self.height
        x3, y3 = self.x + self.width, y2
        x4, y4 = x3, y1
        x5, y5 = x1, y1 + offset
        x6, y6 = x2, y2 - offset
        x7, y7 = x3, y3 - offset
        x8, y8 = x4, y4 + offset

        color = color_from_temp(self.t_m)
        color_hot_in = color_from_temp(self.t_hot_in)
        color_cold_in = color_from_temp(self.t_cold_in)
        color_hot_out = color_from_temp(self.t_hot_out)
        color_cold_out = color_from_temp(self.t_cold_out)

        # hot in
        self.canvas.create_line(x5-arrow_len, y5, x5, y5, width=3, fill=color_hot_in)
        self.canvas.create_line(x5, y5, x5-10, y5-10, width=2, fill=color_hot_in)
        self.canvas.create_line(x5, y5, x5-10, y5+10, width=2, fill=color_hot_in)
        self.canvas.create_text(x5-40, y5-20, text=str(round(self.t_hot_in, 1)) + ' °C', font=Exchanger.FONT, fill=Exchanger.GRAY)

        # cold in
        self.canvas.create_line(x6-arrow_len, y6, x6, y6, width=3, fill=color_cold_in)
        self.canvas.create_line(x6, y6, x6-10, y6-10, width=2, fill=color_cold_in)
        self.canvas.create_line(x6, y6, x6-10, y6+10, width=2, fill=color_cold_in)
        self.canvas.create_text(x6-40, y6-20, text=str(round(self.t_cold_in, 1)) + ' °C', font=Exchanger.FONT, fill=Exchanger.GRAY)

        # hot out
        self.canvas.create_line(x7, y7, x7+arrow_len, y7, width=3, fill=color_hot_out)
        self.canvas.create_line(x7+arrow_len, y7, x7-10+arrow_len, y7-10, width=2, fill=color_hot_out)
        self.canvas.create_line(x7+arrow_len, y7, x7-10+arrow_len, y7+10, width=2, fill=color_hot_out)
        self.canvas.create_text(x7+40, y7-20, text=str(round(self.t_hot_out, 1)) + ' °C', font=Exchanger.FONT, fill=Exchanger.GRAY)

        # cold out
        self.canvas.create_line(x8, y8, x8+arrow_len, y8, width=3, fill=color_cold_out)
        self.canvas.create_line(x8+arrow_len, y8, x8-10+arrow_len, y8-10, width=2, fill=color_cold_out)
        self.canvas.create_line(x8+arrow_len, y8, x8-10+arrow_len, y8+10, width=2, fill=color_cold_out)
        self.canvas.create_text(x8+40, y8-20, text=str(round(self.t_cold_out, 1)) + ' °C', font=Exchanger.FONT, fill=Exchanger.GRAY)

        # rectangle
        #self.canvas.create_rectangle(x1, y1, x3, y3, fill=color, outline='', stipple='gray25')
        self.canvas.create_line(x5, y5, x7, y7, width=2, fill=Exchanger.GRAY, dash=dash)
        self.canvas.create_line(x6, y6, x8, y8, width=2, fill=Exchanger.GRAY, dash=dash)
        self.canvas.create_rectangle(x1, y1, x3, y3, fill='', width=3, outline=Exchanger.GRAY)
                

    def update_exchanger(self, thi, tho, tci, tco):
        self.t_hot_in = thi
        self.t_hot_out = tho
        self.t_cold_in = tci
        self.t_cold_out = tco
        dt_1 = self.t_hot_in - self.t_cold_out
        dt_2 = self.t_hot_out - self.t_cold_in
        delta_t = dt_1 - dt_2
        #if delta_t != 0 or delta_t != 1:
            #self.t_m = math.fabs(delta_t) / math.log(math.fabs(delta_t))
        self.draw()
        

class Tank:

    GRAY = '#666'
    BLUE = '#ccf'

    FONT = None

    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        Tank.FONT = font.Font(family='Courier', size=13, weight='bold')
        #fonts = font.families()
        #for f in fonts:
        #    print(f)

        self.volume = 10
        self.level = self.height * (1 - self.volume / 20)

        self.temperature = 0

        self.draw()

    def draw(self):
        mid_x, mid_y = self.x + self.width / 2, self.y + self.height / 2
        x1, y1 = self.x, self.y
        x2, y2 = x1, self.y + self.height
        x3, y3 = self.x + self.width, y2
        x4, y4 = x3, y1
        level_y = self.y + self.level

        color = color_from_temp(self.temperature)
        self.canvas.create_rectangle(x1, level_y, x3, y3, fill=color, outline='', stipple='')

        self.canvas.create_text(mid_x, level_y - 30, text=str(round(self.volume, 1)) + ' l', font=Tank.FONT, fill=Tank.GRAY)
        self.canvas.create_text(mid_x, level_y - 10, text=str(round(self.temperature, 1)) + ' °C', font=Tank.FONT, fill=Tank.GRAY)

        self.canvas.create_line(x1, y1, x2, y2, width=3, fill=Tank.GRAY)
        self.canvas.create_line(x2, y2, x3, y3, width=3, fill=Tank.GRAY)
        self.canvas.create_line(x3, y3, x4, y4, width=3, fill=Tank.GRAY)

        exit = 15
        self.canvas.create_line(mid_x, y2, mid_x, y2 + exit, width=3, fill=Tank.GRAY)
        self.canvas.create_line(mid_x, y2 + exit, x3 + exit, y2 + exit, width=3, fill=Tank.GRAY)
        self.canvas.create_line(x3 + exit, y2 + exit, x3 + exit, y2 + 2*exit, width=3, fill=Tank.GRAY)

    def update_tank(self, volume, temperature):
        self.volume = volume
        self.level = self.height * (1 - self.volume / 20)
        self.temperature = temperature
        self.draw()
