from sensors import TemperatureReader
import time
import sys

# usage: python templogger.py filename.txt duration dt

tempreader = TemperatureReader()
t = time.time()
tot_t = 0

if len(sys.argv) == 1:

    filename = 'logs/log_test.txt'
    duration = 1 * 60
    dt = 5

else:
    filename = 'logs/' + sys.argv[1]
    duration = int(sys.argv[2])
    dt = int(sys.argv[3])

    
with open(filename, 'w') as f:

    print('\nLogging temperatures in file \'' + filename + '\' for ' + str(duration) + ' seconds...\n')
    
    while tot_t <= duration:
        temps = tempreader.get_temperatures()
        s = str(round(tot_t, 2)) + ',' + str(temps['1']) + ',' + str(temps['2']) + ',' + str(temps['3']) + '\n'
        f.write(s)
        print(s)
    
        time_passed = (time.time() - t)
        t = time.time()
        tot_t += time_passed
        
        if dt > time_passed:
            time.sleep(dt - time_passed)
