import Adafruit_DHT
import time
import sys
import json
import _thread
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")
sensor = Adafruit_DHT.DHT11
line1 = []

# Carico il file di configurazione passato da input
if len(sys.argv) != 2:
    raise ValueError('Bisogna passare il file di configurazione.')
    
pathFile = sys.argv[1]

def live_plotter_xy(x_vec,y1_data,line1,identifier='',pause_time=0.01, yLabel='y', xLabel='x', epsilon=10):
    if line1==[]:
        plt.ion()
        fig = plt.figure(figsize=(20,10))
        ax = fig.add_subplot(111)
        line1, = ax.plot(x_vec,y1_data,'g:.',alpha=0.8)
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)
        plt.title('{}'.format(identifier))
        plt.show()
        
    line1.set_data(x_vec,y1_data)
    plt.xlim(np.min(x_vec) - epsilon, np.max(x_vec) + epsilon)
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])

    plt.pause(pause_time)
    
    return line1

def getConfigurazione():
    fileConfig = open(pathFile)
    configurazioni = {}
    for line in fileConfig.read().splitlines():
        configurazioni[line.split(' = ')[0]] = line.split(' = ')[1]
        if configurazioni[line.split(' = ')[0]] == 'True':
            configurazioni[line.split(' = ')[0]] = True
        if configurazioni[line.split(' = ')[0]] == 'False':
            configurazioni[line.split(' = ')[0]] = False
    return configurazioni

def controlla():
	configurazione = getConfigurazione()
	pin = configurazione["pin"]
	pin = int(pin)
	humidity = None
	temperature = None
	while (humidity is None and temperature is None) or humidity > 100:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	t = 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
	print(t)
	salvaLogPlot(temperature, humidity)
	
	time.sleep(int(configurazione["secondiAttesa"]))
	controlla()

# Salvo i valori in un file in formato json per poi usarli nei grafici
def salvaLogPlot(temperatura, umidita):
	configurazione = getConfigurazione()
	nomeFile = configurazione["fileLogPlot"]
	
	misure = getMisureFromFile()
	
	misure['h'].append(float(umidita))
	misure['t'].append(float(temperatura))
	
	with open(nomeFile, "w+") as outfile:
		json.dump(misure, outfile)
	
	global line1
	line1 = live_plotter_xy(range(0, len(misure['h'])), misure['h'], line1, identifier='Umidità', xLabel='Numero di misurazioni', yLabel='Valori registrati', epsilon=3)
	

def getMisureFromFile():
	configurazione = getConfigurazione()
	nomeFile = configurazione["fileLogPlot"]
	try:
		infile = open(nomeFile)
		infile.seek(0)
		if not infile.read(1):
			# File vuoto
			raise FileNotFoundError
		else:
			# Leggo le "vecchie" notizie dal file
			infile.seek(0)
			misure = json.load(infile)
		infile.close()
	except FileNotFoundError:
		misure = {}
		misure['h'] = []
		misure['t'] = []
	return misure
 
def main():
	line1 = []
	return controlla()
	try:
		controlla()
	except:
		print('Errore. Chiudo')

main()
