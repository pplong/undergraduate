#from random import uniform
from naive import service, task, system, gen

class route(object):
	
	def __init__(self):
		self.pro_route = []
		self.last = None

	def add(self, service):
		if self.last == None:
			self.pro_route = 


		



def gen_kai():
	workflow = []
	for i in range(10):
		service_list = []
		for j in range(10):
			QoS = [uniform(0,1) for k in range(10)]
			service_list.append(service(str(j),QoS))
		workflow.append(task(str(i),service_list))
	return workflow


if __name__ == '__main__':
	workflow = gen_kai()
	system(workflow).select()