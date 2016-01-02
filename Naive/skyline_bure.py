## -*- coding: utf-8 -*-
from naive_kai import service,route
from naive_kai import gen,random_choice
from random import uniform
import copy

global count
count = 0
global best
best = 0
global best_route
best_route = None


def adapt_dfs_search(self,end_list,node_map):

	if len(self.pro_route) == 9:#登龙门，还有一步成功

		sers = [i for i in self.last.next if int(self.last.name) in end_list]#取sers和可取end的交集
		sers.sort(key = lambda service: service.sum)#按Q排列，大的在后
		if sers != []:
			done = route(self.pro_route + [sers[-1]] , self.QoS_sum + sers[-1].sum)
			global count
			count = count + 1
			#------add--------
			global best
			global best_route
			if done.QoS_sum > best:
				best = done.QoS_sum
				best_route = done
			#-----------------
		else:
			pass

	elif self.last.next != []:#非空，所以这里不可能是最后一个，pro_route长度不会等于10
		sers = skyline_service_select(self.last.next,len(self.pro_route),node_map) #add: skyline algorithm
		for next in sers:
			route(self.pro_route + [next] , self.QoS_sum + next.sum).adapt_dfs_search(end_list,node_map)

route.adapt_dfs_search = adapt_dfs_search


class node(object): #在计算到这个task的时候自动生成。或者还是一开始就生成比较好？起码node内合并还是到了再用比较好。

	def __init__(self,service_list,task_down,name):
		self.name = name #node name
		self.service_list = service_list #一般是一个单元素集，复数的时候，将QoS强的放在最后（计算的时候靠它来代表计算）
		#self.IL = []
		#---------------
		#self.current_ser = service_list[0] #初始化的时候将Qos最弱的一个当成当前的ser。

		name_list = [] #包含的名字集
		for ser in service_list:
			name_list.append(ser.name)

		self.name_list = name_list
		#--------------- 
		self.next = service_list[0].next #自己向右能连接的的集。与service的next一致
		self.next_number = service_list[0].next_number #自己向右能连接的的集的番号。与service的next_number一致
		#self.SC = [] #?向下
		#self.OL_ALL = [] #?向下能连接到的（包括自己的）？？实际上感觉这个有用
		#self.task_up = [] #在task中自己可以支配的
		self.task_down = task_down #在task中能支配自己的node集合。根据next推出。求这个是这个脚本的主要工作
		#---------------
		task_down_number = []
		for node in task_down:
			task_down_number.append(node.name)
		
		self.task_down_number = task_down_number
		#---------------

	def printf(self):
		print "---------------"
		print "This is node :",self.name 
		print "This node have services: ",self.name_list
		print "The service it can connect to next task: ", self.next_number
		print "This node is dominated by ",self.task_down_number," in this task"

def unique(service_list):
	temp = service_list

	while(temp != []):
		ser = temp[0]
		sers = [i for i in temp if i.next == ser.next]
		temp = diff(temp,sers)
		sers.sort(key = lambda service: service.sum)
		service_list = diff(service_list,sers[:-1])

	service_list.sort(key = lambda service: service.name)
	return service_list

#想法，先去除相同的next的service（弱的去了）。然后用map找到对应的node.(现在手上有serlist和nodelist，位置对应)
#（直接指向）找到之后看node属性。通过node的属性，得到需要去除的service的位置，然后去除（可以两边同步进行）

def leave_sers(ser_and_node):#通过node之间的关系，搞明白要留下的ser_list
	
	node_list = ser_and_node.keys()
	ser_list = ser_and_node.values()

	ans = []#[ser,ser...]应该被选中的ser
	for node in node_list:
		if node.task_down_number == []:#如果没有能支配这个node的，添加。这代表此node为局部功能最强。实际上应该去掉没用的node，不过这里算了
			ans.append(ser_and_node[node])
		else:
			flag = True#要不要添加的flag
			for anthor_node in node_list:
				if anthor_node.name in node.task_down_number:#如果node被another_node支配了的话
					if ser_and_node[node].sum < ser_and_node[anthor_node].sum:#并且node的Q还比another还低的话
						flag = False#果断舍弃
						break
			if flag:
				ans.append(ser_and_node[node])
	return ans


def skyline_service_select(service_list,task_number,node_map):

	this_node_map = node_map[task_number] #------------当前node参照图------------

	#-------------生成node------------
	service_list = unique(service_list)#unique之后的ser，之后只用它。按照name顺序

	def ser_to_node(ser):
		for node in this_node_map:
			if ser.name in node.name_list:
				return node
		return None

	node_list = map(ser_to_node,service_list)#返回的 利用的node map
	ser_and_node = dict(zip(node_list,service_list))
	ans = leave_sers(ser_and_node)#留下的sers
	ans.sort(key = lambda service : service.name)
	return ans

	


def diff(a, b): #output := a-b
	return list(set(a)-set(b))

def issub(a,b): #return True if a is b's subset
	return set(a).issubset(set(b))

def gen_node_list(service_list1): #input := [ser,ser,...], output := [node, node]
	service_list = copy.deepcopy(service_list1)
	service_list.sort(key = lambda service: len(service.next_number))
	fin = [] #output := [node,node,...]
	while(service_list != []):
		max_len = max(map(lambda x: len(x.next_number), service_list))
		waitinglist = [i for i in service_list if len(i.next_number) == max_len]
		#从末尾找到第一集团。它们之间不可能有互相关系(除非相同)。待处理
		service_list = diff(service_list,waitinglist)

		while(waitinglist !=[]):
			sers = [i for i in waitinglist if i.next_number == waitinglist[0].next_number] #继续抽取next完全相同的
			waitinglist = diff(waitinglist,sers)
			sers.sort(key = lambda service: service.sum) #按照Qsum从小到大排列
			ser = sers[-1] #选择Qsum大的当代表
			ser_task_down = []
			for pp in fin: #pp is node
				if issub(ser.next_number , pp.next_number):#计算从属关系
					ser_task_down.append(pp)
			fin = fin + [node(sers,ser_task_down,str(len(fin)))]

	return fin

#----------------add to skyline.py--------------------
def gen_for_start_end():
	workflow = []
	for i in [1-n for n in range(0,2)]: #10 tasks
		service_list = []
		for j in [9-n for n in range(0,10)]: #each task have 10 services
			QoS = [uniform(0,1) for k in range(10)]
			if i >= 1:
				service_list = [service(str(j),QoS,[],[])] + service_list
			else:
				selected = sorted(random_choice(range(10)))
				next_service_list = []
				for pp in selected:
					next_service_list.append(workflow[0][pp])
				service_list = [service(str(j),QoS,next_service_list,selected)] + service_list
		workflow = [service_list] + workflow
	return workflow

def strong():#output := [[1,2,3],[3,2,4],...]
	start_or_end = gen_for_start_end()[0]#type:[ser,ser,...]
	this_map = gen_node_list(start_or_end)
	#Need to expand
	ans = range(10)
	for node in this_map:
		for name in node.name_list:
			temp = []
			for dom_node in node.task_down:
				temp = temp + dom_node.name_list
			ans[int(name)] = map(int,temp)

	for i in range(len(ans)):
		sers1 = ans[i]
		for j in range(len(ans)):
			sers2 = ans[j]
			if issub(sers1,sers2) and set(sers1) != set(sers2):
				ans[j] = diff(sers2 , sers1)

	return ans


def weak(strong_list):#input:strong_list
	ans = [[]] * len(strong_list)
	for i in range(len(strong_list)):
		wait_list = strong_list[i]
		for connect in wait_list:
			ans[connect] = ans[connect] + [i]
	return ans


def bure(chosed,strong_list,weak_list):
	one_strong , one_weak = [] , []
	for ser_number in chosed:
		one_strong = one_strong + strong_list[ser_number]
		one_weak= one_weak + weak_list[ser_number]
	one_strong = diff(one_strong , chosed)
	one_weak = diff(one_weak , chosed)
	return  one_strong, one_weak


#-----------------------------------------------------
def run(start,end,node_map):
	print start,end
	global best
	best = 0
	for index in start:
		start_service = workflow[0][index]
		test = route([start_service],start_service.sum)
		test.adapt_dfs_search(end,node_map)
		print count

	print best
	#global best_route
	#if best_route != None: 
	#	best_route.printf()




if __name__ == "__main__":
	workflow = gen()
#-----------add to naive_kai-------------
	node_map = map(lambda x: gen_node_list(x),workflow)
#----------------------------------------
	start = sorted(random_choice(range(10)))
	end = sorted(random_choice(range(10)))

	print "------------------------------fixed------------------------------"
	run(start,end,node_map)

#----------------add to skyline.py--------------------
	#先生成全图，之后参照
	start_strong_list , end_strong_list = strong(), strong()
	start_weak_list , end_weak_list = weak(start_strong_list) , weak(end_strong_list)
	##need to modify after
	start_one_strong, start_one_weak = bure(start,start_strong_list,start_weak_list)
	end_one_strong, end_one_weak = bure(end,end_strong_list,end_weak_list)
	print "----------------------one_strong,one_strong------------------------"
	run(start_one_strong,end_one_strong,node_map)
	print "----------------------one_strong,one_weak------------------------"
	run(start_one_strong,end_one_weak,node_map)
	print "----------------------one_weak,one_strong------------------------"
	run(start_one_weak,end_one_strong,node_map)
	print "----------------------one_weak,one_weak------------------------"
	run(start_one_weak,end_one_weak,node_map)








#-----------------------------------------------------