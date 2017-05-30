import os
import time
import pprint
import threading
import RPi.GPIO as GPIO
import serial


class TemperatureReader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # Initiate one-wire functionality
        os.system('modprobe w1-gpio && modprobe w1-therm')

        
        self.sensors = {'1': '28-000008a9c53d',
                        '2': '28-000008a9d54c',
                        '3': '28-000008a712b6',
                        '4': '28-000008a72c10',
                        '5': '28-000008a938f4',
                        '6': '28-000008a9a79f',
                        '7': '28-000008a9b23a',
                        '8': '28-000008a9393a'}

        self.temperatures =   { '1': 0.0,
                                '2': 0.0,
                                '3': 0.0,
                                '4': 0.0,
                                '5': 0.0,
                                '6': 0.0,
                                '7': 0.0,
                                '8': 0.0}

        self.start()


    def run(self):
        while True:
            self.read_temperatures()


    def get_temperatures(self):
        return self.temperatures
        

    def read_temperatures(self):

        for sensor_name in self.sensors:

            sensor_addres = self.sensors[sensor_name]
            path = '/sys/bus/w1/devices/' + sensor_addres + '/w1_slave'

            try:
                with open(path, 'r') as f:

                    tempstring = f.read()
                    temp = float(tempstring.split('\n')[1].split(' ')[9][2:]) / 1000
                    

            except: #FileNotFoundError:
                temp = -9999

            self.temperatures[sensor_name] = temp

        #print('TemperatureReader has read temperatures!')


class FlowSensor(threading.Thread):

    def __init__(self, channel):
        threading.Thread.__init__(self)

        self.channel = channel

        self.pulses = 0
        self.time_at_last_count = time.time()
        self.flows = ContinousQueue(10)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=self.count_pulse)

        self.start()
        

    def run(self):

        while True:
            self.flows.put(self.read_flow())
            time.sleep(0.1)


    def count_pulse(self, arg):
        self.pulses += 1


    def get_flow(self):
        return self.flows.mean()
        

    def read_flow(self):
        pulses = self.pulses
        self.pulses = 0

        delta_time = (time.time() - self.time_at_last_count)
        self.time_at_last_count = time.time()
        
        flow = 0.00225 * pulses / delta_time * 60

        # justera för fel
        flow_adjusted = max((0.1847*flow - 0.2548) + flow, 0)

        return flow_adjusted



class ContinousQueue():

    def __init__(self, size):
        self.size = size
        self.queue = []

        for i in range(size):
            self.queue.append(0)

    def put(self, element):
        del self.queue[0]
        self.queue.append(element)

    def mean(self):
        return sum(self.queue) / self.size



class LevelReader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.h1 = self.h2 = self.h3 = 0

        # start a serial connection
        serial_port = '/dev/ttyACM0'
        self.ser = serial.Serial(serial_port, 9600, timeout=10)

        self.start()


    def run(self):

        while True:
            self.read_levels()
            #print('Level reader here: just read the levels ;)')
            #time.sleep(10)
            
                
    def read_levels(self):
        self.ser.write(b'h')
        response = str(self.ser.readline())

        if 'H' in response:
            self.h1 = float(response.split(' ')[1]) / 100 # m
            self.h2 = float(response.split(' ')[2]) / 100
            self.h3 = float(response.split(' ')[3][:-5]) / 100

        else:
            self.h1 = self.h2 = self.h3 = -9999


    def get_levels(self):
        return self.h1, self.h2, self.h3

    
if __name__ == '__main__':
    #temp_reader = TemperatureReader()
    #temps = temp_reader.read_temperature()
    #pprint.pprint(temps)

    flow_reader = FlowReader()



    
