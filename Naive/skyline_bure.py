## -*- coding: utf-8 -*-
from naive_kai import service,route
from naive_kai import gen,random_choice
from random import uniform
import copy
import csv
global count
count = 0
global best
best = 0
global best_route
best_route = None
global version4_ans
version4_ans = [0]*9


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
			count = count + 1  #add
			route(self.pro_route + [next] , self.QoS_sum + next.sum).adapt_dfs_search(end_list,node_map)

route.adapt_dfs_search = adapt_dfs_search


def adapt_dfs_search_kai(self,end_list,node_map,start,start_strong,start_weak,end,end_strong,end_weak):

	global count
	if len(self.pro_route) == 9:#登龙门，还有一步成功

		sers_kai = []
		def takelist(l):
			sers = [i for i in self.last.next if int(i.name) in l]#取sers和可取end的交集
			sers.sort(key = lambda service: service.sum)#按Q排列，大的在后
			if sers != []:
				sers_kai.append(sers[-1])
		takelist(end)
		takelist(end_strong)
		takelist(end_weak)
		#-----------------
		#保证endfsw至少有一个
		
		#-----------------
		for ser in sers_kai:
			done = route(self.pro_route + [ser] , self.QoS_sum + ser.sum)
			
			count = count + 1

			#------add--------
			global version4_ans
			put_in(done.QoS_sum,int(done.pro_route[0].name),int(done.pro_route[-1].name),start,start_strong,start_weak,end,end_strong,end_weak)
			#-----------------

		else:
			pass

	elif self.last.next != []:#非空，所以这里不可能是最后一个，pro_route长度不会等于10
		sers = skyline_service_select(self.last.next,len(self.pro_route),node_map) #add: skyline algorithm
		if len(self.pro_route) < 8:
			sers = disable(sers)
		for next in sers:
			count = count + 1  #add
			route(self.pro_route + [next] , self.QoS_sum + next.sum).adapt_dfs_search(end_list,node_map,start,start_strong,start_weak,end,end_strong,end_weak)






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
	return ans

def one_strong(ans1):
	ans = copy.deepcopy(ans1)
	for i in range(len(ans)):
		ser1 = ans1[i]
		temp = map(lambda x: ans1[x] + [x], ser1) #ok
		#print temp
		for m in range(len(temp)):
			sers2 = temp[m]
			for n in range(len(temp)):
				sers3 = temp[n]
				if issub(sers2,sers3) and set(sers2) != set(sers3):
					ans[i][m] = -1
	def del_m1(l):
		return [i for i in l if i != -1]

	#print ans
	return map(del_m1, ans)






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



def run_original(start,end,node_map,workflow):
	#print start,end
	global best
	best = 0
	global count
	count = 0

	global best_route	
	best_route = None

	start = skyline_service_select([workflow[0][i] for i in start],0,node_map) #add: skyline algorithm
	#start = disable(start)
	for index in start:
		#print "start from service: ",index.name
		start_service = index
		test = route([start_service],start_service.sum)
		test.adapt_dfs_search(end,node_map)
		#print count

	#print best

	if best_route != None: 
		pass
		#print "start from: ",best_route.pro_route[0].name ," end at: ",best_route.pro_route[-1].name
	#------------add-------------
	return best
	#------------add-------------

def run(start,end,node_map,workflow,original_best_QoS):
	#print start,end
	global best
	best = 0
	global count
	#count = 0

	global best_route	
	best_route = None

	start = skyline_service_select([workflow[0][i] for i in start],0,node_map) #add: skyline algorithm
	#start = disable(start)
	for index in start:
		#print "start from service: ",index.name
		start_service = index
		test = route([start_service],start_service.sum)
		test.adapt_dfs_search(end,node_map)
		#print count

	if best > original_best_QoS:
		pass
		#print best
		#print "start from: ",best_route.pro_route[0].name ," end at: ",best_route.pro_route[-1].name

	else:
		pass
		#print "Nothing good than fixed"
	#------------add-------------
	return best
	#------------add-------------

def union(a,b):
	return list(set(a).union(set(b)))

def union3(a,b,c):
	return union(union(a,b),c)


def put_in(done_QoS,done_start,done_end,start,start_strong,start_weak,end,end_strong,end_weak):
	global version4_ans

	def change(model):
		model_start, model_end, model_QoS = model
		if done_start in model_start and done_end in model_end:
			if done_QoS > model_QoS:
				return (model_start,model_end,done_QoS)
			else:
				return model
		else:
			return model


	start_fsw = [start,start_strong,start_weak]
	end_fsw = [end,end_strong,end_weak]

	l = []
	for i in range(len(start_fsw)):
		s = start_fsw[i]
		for j in range(len(end_fsw)):
			e = end_fsw[j]
			l.append((s,e,version4_ans[i*3+j]))
	new_l = map(change,l)
	#print new_l
	#print version4_ans
	version4_ans = [c for (dummy1,dummy2,c) in new_l]



def run_kai(start,start_strong,start_weak,end,end_strong,end_weak,node_map,workflow):

	#-----------------------
	#保证startfsw的必有一个

	#-----------------------
	def sers_to_number(sers):
		ans = []
		for ser in sers:
			ans.append(int(ser.name))
		return ans
	def number_to_sers(number):
		ans = []
		for num in number:
			ans.append(workflow[0][num])
		return ans

	start1 = sers_to_number(skyline_service_select([workflow[0][i] for i in start],0,node_map))
	start_strong1 = sers_to_number(skyline_service_select([workflow[0][i] for i in start_strong],0,node_map))
	start_weak1 = sers_to_number(skyline_service_select([workflow[0][i] for i in start_weak],0,node_map))

	union_start = union3(start1,start_strong1,start_weak1)
	#print union_start
	union_start = number_to_sers(union_start)
	#union_start = disable(union_start)
	union_end  = union3(end,end_strong,end_weak)
		
	#print union_start,union_end
	global best
	best = 0
	global count
	count = 0

	global best_route
	best_route = None

	global version4_ans
	version4_ans = [0] * 9

	#union_start = skyline_service_select([workflow[0][i] for i in union_start],0,node_map) #add: skyline algorithm

	for index in union_start:
		#print "start from service: ",index.name
		start_service = index
		test = route([start_service],start_service.sum)
		test.adapt_dfs_search(union_end,node_map,start,start_strong,start_weak,end,end_strong,end_weak)  ###modify
		#print count

#-----------------------------------------------------






if __name__ == "__main__":
	workflow = gen()
#-----------add to naive_kai-------------
	node_map = map(lambda x: gen_node_list(x),workflow)
#----------------------------------------
	start = sorted(random_choice(range(10)))
	end = sorted(random_choice(range(10)))

	version3_ans = [0]*9

	#print "---------------------------------version3---------------------------------"
	#print "------------------------------fixed------------------------------"
	version3_ans[0] = run_original(start,end,node_map,workflow)
	original_best_QoS = best

#----------------add to skyline.py--------------------
	#先生成全图，之后参照
	start_strong_list , end_strong_list = strong(), strong()#ここのstrongは、自分たちよりstrongのすべて
	temp1 , temp2 = one_strong(start_strong_list) , one_strong(end_strong_list)#これは自分たちより一段と強い
	start_weak_list , end_weak_list = weak(temp1) , weak(temp2)#自分より一段と弱い
	##need to modify after
	start_strong, start_one_weak = bure(start,start_strong_list,start_weak_list)
	end_strong, end_one_weak = bure(end,end_strong_list,end_weak_list)

	#print "----------------------fixed,strong------------------------"
	version3_ans[1] = run(start,end_strong,node_map,workflow,original_best_QoS)
	#print "----------------------fixed,one_weak------------------------"
	version3_ans[2] = run(start,end_one_weak,node_map,workflow,original_best_QoS)
	#print "----------------------strong,fixed------------------------"
	version3_ans[3] = run(start_strong,end,node_map,workflow,original_best_QoS)
	#print "----------------------strong,strong------------------------"
	version3_ans[4] = run(start_strong,end_strong,node_map,workflow,original_best_QoS)
	#print "----------------------strong,one_weak------------------------"
	version3_ans[5] = run(start_strong,end_one_weak,node_map,workflow,original_best_QoS)
	#print "----------------------one_weak,fixed------------------------"
	version3_ans[6] = run(start_one_weak,end,node_map,workflow,original_best_QoS)
	#print "----------------------one_weak,strong------------------------"
	version3_ans[7] = run(start_one_weak,end_strong,node_map,workflow,original_best_QoS)
	#print "----------------------one_weak,one_weak------------------------"
	version3_ans[8] = run(start_one_weak,end_one_weak,node_map,workflow,original_best_QoS)
	

	writer = csv.writer(file('experiment2.csv', 'a+'))
	#writer.writerow(['fixed', 'fixed-strong', 'fixed-one_weak','strong-fixed','strong-strong','strong-one_weak','one_weak-fixed','one_weak-strong','one_weak-one_weak'])
	line = version3_ans
	writer.writerow(line)


	#print version3_ans
	#print count
	version3_count = count
	#print "---------------------------------version4---------------------------------"
	version4_ans = [0]*9
	route.adapt_dfs_search = adapt_dfs_search_kai
	#print "------------------------------------------------run_kai---------------------------------------------------------------"
	run_kai(start,start_strong,start_one_weak,end,end_strong,end_one_weak,node_map,workflow)
	#print version4_ans
	#print count
	writer = csv.writer(file('experiment3.csv', 'a+'))
	#writer.writerow(['version3_count', 'version4_count', 'is_equal'])
	line = [version3_count,count,version3_ans == version4_ans]
	writer.writerow(line)

#-----------------------------------------------------
