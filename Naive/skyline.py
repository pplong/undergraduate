## -*- coding: utf-8 -*-f
from naive_kai import service


class node(object): #在计算到这个task的时候自动生成。或者还是一开始就生成比较好？起码node内合并还是到了再用比较好。

	def __init__(self,service_list,task_down,name):
		self.name = name #node name
		self.service_list = service_list #一般是一个单元素集，复数的时候，将QoS强的放在最后（计算的时候靠它来代表计算）
		#self.IL = []
		#---------------
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



#def task_launch(task):



#def take_ser_by_str(a_str,task):
#	for ser in task:
#		if a_str == ser.name:
#			return ser		
#	return None

def diff(a, b): #output := a-b
	return list(set(a)-set(b))

def issub(a,b): #return True if a is b's subset
	return set(a).issubset(set(b))


def gen_node_list(service_list): #input := [ser,ser,...], output := [node, node]
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
				if issub(ser.next_number , pp.next_number):
					ser_task_down.append(pp)
			fin = fin + [node(sers,ser_task_down,str(len(fin)))]

	return fin



