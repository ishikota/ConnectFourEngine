'''
This is the start point of GA process.
To start GA, execute this file.
'''
import genetic_algorithm
import time
st = time.time()
GA = genetic_algorithm.GA()
GA.start()
ft = time.time()
print 'EXECUTION TIME : '+str(int(ft-st))+'(s)'
