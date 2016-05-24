from random import uniform
from random import choice
from random import sample
import copy

total_task, total_ser = 10, 10
( ALPHA, BETA, RHO, Q ) = ( 1.0, 2.0, 0.5, 100.0 )
(ant_num, iter_max ) = ( 50, 1000 )

class service(object):

	def __init__(self,task_num,ser_num,next):
		self.task_num = task_num
		self.ser_num = ser_num
		self.QoS = uniform(0,1) #One-dimensional QoS,float range: (0,1)
		self.next = next #e.g: [(1, 1.0), (2, 1.0), (4, 1.0), (5, 1.0), (6, 1.0)]

	def printf(self):
		print "task_num: ", self.task_num
		print "ser_num: ", self.ser_num
		print "QoS: ", self.QoS
		print "next: ", self.next
		print "--------------------"

class ant(object):

	def __init__(self, ID):
		self.ID = ID
		self.path = []#e.g: [1,5,2,5,2,4,2,4,5,3]
		self.total_QoS = 0.0
		#don not forget to choose first service or it will be error!
	
	def __choice_next_ser(self):
		next_ser = -1
		current_task_num = len(self.path)-1
		current_ser_num = self.path[-1]

		candidates = dot_graph[current_task_num][current_ser_num].next #warning: depend on global "dot_graph" in "__main__"
		#e.g: [(1, 1.0), (2, 1.0), (4, 1.0), (5, 1.0), (6, 1.0)]
		select_sers_prob = [ 0.0 for i in candidates ]
		total_prob = 0.0

		for i in range(len(candidates)):
			#calculate every candidate pheromone
			candidate = candidates[i]
			select_sers_prob[i] = pow( candidate[1], ALPHA ) *\
				pow( dot_graph[current_task_num + 1][candidate[0]].QoS , BETA ) #need to rewrite here. QoS
			total_prob += select_sers_prob[i]
			
		# select ser by way of roulette
		if total_prob > 0.0:
			temp_prob = random.uniform( 0.0, total_prob )
			for i in range(len(candidates)):
				total_prob -= select_sers_prob[i]
				if temp_prob < 0.0:
					next_ser = candidates[i][0]
					break

		return next_ser #number

	def __move(self, next_ser):
		self.path.append(next_ser)
		task_num = len(self.path) - 1
		self.total_QoS += dot_graph[task_num][next_ser].QoS

	def search_path(self, end):#end set -> out function
		while len(self.path) < total_task:
			if len(self.path) < total_task - 1:
				next_ser = self.__choice_next_ser()
				self.__move(next_ser)
			else:
				#choose a best QoS from end
				last = [i for (i,j) in dot_graph[total_task-2][self.path[-1]].next]
				candidates = [i for i in last if i in end]
				if candidates == []:
					print "--------------------------"
					print "ant: ", self.ID," can not find a path"
					return -1#do not undate pheromone

				candidates_sers = [dot_graph[total_task-1][i] for i in candidates] #sers_list
				candidates_sers.sort(key = lambda service: service.QoS)
				next_ser = candidates_sers[-1].ser_num
				self.__move(next_ser)

				print "--------------------------"
				print "ant: ", self.ID," find a path"
				print self.path
				print self.total_QoS
				return 1#update pheromone

class ACO(object):
	def __init__(self):
		self.ants = [ ant( ID ) for ID in xrange( ant_num ) ]
		self.best_ant = ant( -1 )
		self.best_ant.total_QoS = 1 << 31

	def search_path(self):
		#manipulate all ants
		for i in range(iter_max):
			for ant in self.ants:
				if_pheromone = ant.search_path()
				#maybe should make a list
				if ant.total_QoS < self.best_ant.total_QoS:
					self.best_ant = copy.deepcopy(ant)

			self.__update_pheromone_graph()

	def __update_pheromone(self):
		#renew pheromone in dot_graph





def random_choice(lists):
	num = choice(range(1,len(lists)+1))
	return sample(lists, num)


if __name__ == "__main__":
	dot_graph = []
	#generate graph randomly
	for i in range(total_task):
		temp = []
		for j in range(total_ser):
			next_car = sorted(random_choice(range(total_ser)))
			next = [(i,1.0) for i in next_car]

			temp.append(service(i, j, next))
		dot_graph.append(temp)

"""
	for i in dot_graph:
		for j in i:
			j.printf()
"""






#----------------------example-----------------------
