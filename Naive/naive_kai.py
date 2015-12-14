#from random import uniform
from naive import service
from random import uniform

#---------modify the definition of class service---------
def new_init(self,name,QoS,next):
	self.name = name
	self.QoS = QoS
	self.sum = sum(QoS)
	self.next = next #add

service.__init__ = new_init
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

	def adapt_dfs_search(self):
		if self.last.next != []:
			for next in self.last.next:
				route(self.pro_route + [next] , self.QoS_sum + next.sum).adapt_dfs_search()
		else:
			if len(self.pro_route) == 10:
				self.printf()




if __name__ == '__main__':
	service_list = []
	for j in [99-n for n in range(0, 100)]:
		QoS = [uniform(0,1) for k in range(10)]
		if j >= 90:
			service_list = [service(str(j),QoS,[])] + service_list
		else:
			service_list = [service(str(j),QoS,[service_list[j-90]])] + service_list
	for i in range(10):
		test = route([service_list[i]])
		test.adapt_dfs_search()


