from random import uniform
from random import choice
from random import sample
import copy

total_task, total_ser = 10, 10
( ALPHA, BETA, RHO, Q ) = ( 1.0, 2.0, 0.5, 100.0 )

class service(object):

	def __init__(self,task_num,ser_num,next):
		self.task_num = task_num
		self.ser_num = ser_num
		self.QoS = uniform(0,1) #One-dimensional QoS,float range: (0,1)
		self.next = next
	def printf(self):
		print "task_num: ", self.task_num
		print "ser_num: ", self.ser_num
		print "QoS: ", self.QoS
		print "next: ", self.next
		print "--------------------"

def random_choice(lists):
	num = choice(range(0,len(lists)+1))
	return sample(lists, num)

if __name__ == "__main__":
	dot_graph = []
	#generate dot graph
	for i in range(total_task):
		temp = []
		for j in range(total_ser):
			next = sorted(random_choice(range(total_ser)))
			temp.append(service(i, j, next))
		dot_graph.append(temp)


	#print out graph
"""
	for i in dot_graph:
		for j in i:
			j.printf()
"""



