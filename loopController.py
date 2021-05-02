import Adafruit_DHT
import time
import sys
import json
import _thread
import matplotlib.pyplot as plt

sensor = Adafruit_DHT.DHT11

# Carico il file di configurazione passato da input
if len(sys.argv) != 2:
    raise ValueError('Bisogna passare il file di configurazione.')
    
pathFile = sys.argv[1]

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
	while humidity is None and temperature is None:
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
	try:
		controlla()
	except:
		print('Errore. Chiudo')

main()
