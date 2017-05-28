from random import uniform
from random import choice
from random import sample
import copy

total_task, total_ser = 10, 10
( ALPHA, BETA, RHO ) = ( 1.0, 1.0, 0.2,)
(ant_num, iter_max ) = ( 500, 1000 )

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

		#print select_sers_prob
		#print total_prob

		# select ser by way of roulette
		#print total_prob
		#print select_sers_prob
		if total_prob > 0.0:
			temp_prob = uniform( 0.0, total_prob )
			for i in range(len(candidates)):
				total_prob -= select_sers_prob[i]
				if total_prob <= 10 ** -5:
					next_ser = candidates[i][0]
					break

		#print next_ser
		return next_ser #number

	def move(self, next_ser):
		self.path.append(next_ser)
		task_num = len(self.path) - 1
		self.total_QoS += dot_graph[task_num][next_ser].QoS

	def search_path(self, end):#end set -> out function
		while len(self.path) < total_task:
			if len(self.path) < total_task - 1:
				next_ser = self.__choice_next_ser()
				self.move(next_ser)
			else:
				#choose a best QoS from end
				last = [i for (i,j) in dot_graph[total_task-2][self.path[-1]].next]
				candidates = [i for i in last if i in end]
				"""
				if candidates == []:
					print "--------------------------"
					print "ant: ", self.ID," can not find a path"
					return -1#do not undate pheromone
				"""
				candidates_sers = [dot_graph[total_task-1][i] for i in candidates] #sers_list
				candidates_sers.sort(key = lambda service: service.QoS)
				next_ser = candidates_sers[-1].ser_num
				self.move(next_ser)

				"""
				print "--------------------------"
				print "ant: ", self.ID," find a path"
				print self.path
				print self.total_QoS
				return 1#update pheromone
				"""

class ACO(object):
	def __init__(self):
		self.ants = [ant(ID) for ID in range(ant_num)]
		self.best_ant = ant(-1)
		self.best_ant.total_QoS = 0.0

	def search_path(self,start,end):
		#manipulate all ants
		for i in range(iter_max):
			#print "----------------------","ROUND: ",i,"----------------------"
			self.ants = [ant(ID) for ID in range(ant_num)]
			for the_ant in self.ants:
				#radom select start ser
				the_ant.move(choice(start))

				if_pheromone = the_ant.search_path(end)#dummy
				#maybe should make a list
				#print the_ant.total_QoS,self.best_ant.total_QoS
				if the_ant.total_QoS >= self.best_ant.total_QoS:
					self.best_ant = copy.deepcopy(the_ant)

			self.__update_pheromone(self.best_ant)

	def __update_pheromone(self,best_ant):
		#renew pheromone in dot_graph
		#print self.best_ant.path
		#print self.best_ant.total_QoS

		for i in range(total_task):
			for j in range(total_ser):
				for k in range(len(dot_graph[i][j].next)):
					if dot_graph[i][j].next[k][1] * (1-RHO) >= 0.2:
						dot_graph[i][j].next[k][1] *= 1-RHO
					else:
						dot_graph[i][j].next[k][1] = 0.2

		for i in range(total_task-1):
			start, end = best_ant.path[i], best_ant.path[i+1]#number

			for j in range(len(dot_graph[i][start].next)):
				if end == dot_graph[i][start].next[j][0]:
					if dot_graph[i][start].next[j][1] + 0.1 <= 1.0:
						dot_graph[i][start].next[j][1] += 0.1
					else:
						dot_graph[i][start].next[j][1] = 1.0
					#best_ant.total_QoS







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
			next = [[i,1.0] for i in next_car]

			temp.append(service(i, j, next))
		dot_graph.append(temp)

	start = [1,3,4,5]
	end = [2,5,7,8]
	test = ACO()
	test.search_path(start,end)

	print test.best_ant.path
	print test.best_ant.total_QoS

"""
	for i in dot_graph:
		for j in i:
			j.printf()
"""






#----------------------example-----------------------
