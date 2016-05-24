#from random import uniform
from naive import service
from random import uniform
from random import choice
from random import sample

global count
count = 0
#---------modify the definition of class service---------
def new_init(self,name,QoS,next,next_number):
	self.name = name
	self.QoS = QoS
	self.sum = sum(QoS)
	self.next = next #add
	self.next_number = next_number

def printf(self):
	print "service: ",self.name
	print self.QoS
	print self.sum
	print self.next_number

service.__init__ = new_init
service.printf = printf
#--------------------------------------------------------

class route(object):
	#-----------fobbiden input []--------------
	def __init__(self, pro_route, QoS_sum = 0):
		self.pro_route = pro_route
		self.QoS_sum = QoS_sum
		self.last = pro_route[-1]  #caution

	def printf(self):
		i = 1
		print "--------------------------------------"
		print "route QoS_sum:",self.QoS_sum
		for service_instance in self.pro_route:
			print "task ",i," chosed:"
			service_instance.printf()
			i = i + 1

	def adapt_dfs_search(self,end_list):
		global count
		if self.last.next != []:
			for next in self.last.next:##### need to add skyline algorithm
				count = count + 1
				route(self.pro_route + [next] , self.QoS_sum + next.sum).adapt_dfs_search(end_list)
		else:
			if len(self.pro_route) == 10 and int(self.pro_route[-1].name) in end_list:
				#self.printf()
				count = count + 1


def random_choice(lists):
	num = choice(range(1,len(lists)+1))
	return sample(lists, num)

def gen():
	workflow = []
	for i in [9-n for n in range(0,10)]: #10 tasks
		service_list = []
		for j in [9-n for n in range(0,10)]: #each task have 10 services
			QoS = [uniform(0,1) for k in range(10)]
			if i >= 9:
				service_list = [service(str(j),QoS,[],[])] + service_list
			else:
				selected = sorted(random_choice(range(10)))
				next_service_list = []
				for pp in selected:
					next_service_list.append(workflow[0][pp])
				service_list = [service(str(j),QoS,next_service_list,selected)] + service_list
		workflow = [service_list] + workflow
	return workflow


if __name__ == '__main__':
	workflow = gen()
	start = sorted(random_choice(range(10)))
	end = sorted(random_choice(range(10)))
	print start,end

	for index in start:
		start_service = workflow[0][index]
		test = route([start_service])
		test.adapt_dfs_search(end)
		print count

