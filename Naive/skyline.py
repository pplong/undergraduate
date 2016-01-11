## -*- coding: utf-8 -*-
from naive_kai import service,route
from naive_kai import gen,random_choice
import copy

global count
count = 0
global best
best = 0
global best_route
best_route = None


def adapt_dfs_search(self,end_list,node_map):
	global count
	if len(self.pro_route) == 9:#登龙门，还有一步成功

		sers = [i for i in self.last.next if int(i.name) in end_list]#取sers和可取end的交集
		sers.sort(key = lambda service: service.sum)#按Q排列，大的在后
		if sers != []:
			done = route(self.pro_route + [sers[-1]] , self.QoS_sum + sers[-1].sum)
			
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
		if len(self.pro_route) < 8:
			sers = disable(sers)
		for next in sers:
			count = count + 1
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

	
#---------------最終アルゴリズム----------------
def disable(service_list1):
	service_list = copy.deepcopy(service_list1)
	service_list.sort(key = lambda service : -service.sum)
	used = []
	used_number = []
	for i in range(len(service_list)):
		temp = service_list[i]
		next = diff(temp.next,used)
		next_number = diff(temp.next_number,used_number)
		used  = used + next
		used_number = used_number + next_number
		service_list[i].next = next
		service_list[i].next_number = next_number

	return service_list
#---------------最終アルゴリズム----------------


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

if __name__ == "__main__":
	workflow = gen()
#-----------add-------------
	node_map = map(lambda x: gen_node_list(x),workflow)
#---------------------------
	start = sorted(random_choice(range(10)))
	end = sorted(random_choice(range(10)))
	print start,end


	for index in start:
		start_service = workflow[0][index]
		test = route([start_service],start_service.sum)
		test.adapt_dfs_search(end,node_map)
		print count

	print best
	if best_route != None: 
		best_route.printf()



