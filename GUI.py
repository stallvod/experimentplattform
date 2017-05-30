import time
import math
from random import randint

from tkinter import *

from units import Tank, Exchanger
from sensors import TemperatureReader, FlowSensor, LevelReader


class GUI:

    def __init__(self):

        self.root = Tk()
        #self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.width = 1000
        self.height = 700

        self.temperature_reader = TemperatureReader()

        self.flow_sensor_vv = FlowSensor(24)
        self.flow_sensor_kv = FlowSensor(25)

        self.level_reader = LevelReader()

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.clear_canvas()

        self.tank1 = Tank(self.canvas, 200, 100, 100, 100, )
        self.tank2 = Tank(self.canvas, 300, 250, 100, 100, )
        self.tank3 = Tank(self.canvas, 400, 400, 100, 100, )

        self.ex = Exchanger(self.canvas, 700, 100, 100, 200)

        self.update()

        self.root.mainloop()

    def update(self, parameters=None):

        temperatures = self.temperature_reader.get_temperatures()

        t1 = temperatures['1']
        t2 = temperatures['2']
        t3 = temperatures['3']
        t4 = temperatures['4']
        t5 = temperatures['5']
        t6 = temperatures['6']
        t7 = temperatures['7']
        t8 = temperatures['8']

        flow_vv = self.flow_sensor_vv.get_flow()
        flow_kv = self.flow_sensor_kv.get_flow()

        h1, h2, h3 = self.level_reader.get_levels()

        A = math.pi * (145e-3) ** 2 # m²

        v1 = h1 * A * 1000
        v2 = h2 * A * 1000
        v3 = h3 * A * 1000 
        
        self.clear_canvas()

        self.tank1.update_tank(v1, t1)
        self.tank2.update_tank(v2, t2)
        self.tank3.update_tank(v3, t3)
        self.ex.update_exchanger(t4, t7, t6, t5)

        #print('Updated GUI!')
        #print(flow1)
        #print(flow2)

        self.canvas.create_text(760,400, text='Varmvattenflöde: ' + str(int(flow_vv)) + ' l/min') 
        self.canvas.create_text(750,430, text='Kallvattenflöde: ' + str(int(flow_kv)) + ' l/min')
    
        self.root.update()
        self.root.after(500, self.update)

        

    def clear_canvas(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='#fff', outline='')

        
    

gui = GUI()






