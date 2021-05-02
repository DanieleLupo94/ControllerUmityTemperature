import numpy as np
import matplotlib.pyplot as plt
import json

def getMisureFromFile():
	nomeFile = 'test.json'
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


while True:
	misure = getMisureFromFile()
	plt.plot(range(0, len(misure['h'])), misure['h'])
	plt.pause(5)

plt.show()
