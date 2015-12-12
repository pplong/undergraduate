from random import uniform

class service(object):

	def __init__(self,name,QoS):
		self.name = name
		self.QoS = QoS
		self.sum = sum(QoS)

	def printf(self):
		print "service: ",self.name
		print self.QoS
		print self.sum

class task(object):

	def __init__(self,name,service_list):
		self.name = name
		self.service_list = service_list

	def compare(self):
		print "------------------"
		print "task ",self.name," selected:"
		sorted(self.service_list, key=lambda a_task: a_task.sum)[0].printf()


class system(object):

	def __init__(self,workflow):
		self.workflow = workflow

	def select(self):
		for task in self.workflow:
			task.compare()

def gen():
	workflow = []
	for i in range(10):
		service_list = []
		for j in range(10):
			QoS = [uniform(0,1) for k in range(10)]
			service_list.append(service(str(j),QoS))
		workflow.append(task(str(i),service_list))
	return workflow

if __name__ == '__main__':
	workflow = gen()
	system(workflow).select()

