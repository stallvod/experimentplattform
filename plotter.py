from matplotlib import pyplot as pp

time = []
t1 = []
t2 = []
t3 = []

with open('logs/log_test.txt', 'r') as f:
	for line in f:
		data = line.split(',')
		time.append(float(data[0]))
		t1.append(float(data[1]))
		t2.append(float(data[2]))
		t3.append(float(data[3]))
		
		
pp.plot(time, t1, 'k', label='Tank 1')
pp.plot(time, t2, ':k', label='Tank 2')
pp.plot(time, t3, '--k', label='Tank 3')

pp.xlabel('Tid [s]')
pp.ylabel('Temperatur [C]')

pp.grid()
pp.legend(loc='best')

pp.show()
