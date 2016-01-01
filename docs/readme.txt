------------------------------------------------------------------------------
naive.py: 
for each workflow, 10 tasks are generated.
for each tasks, there exists 10 services.
for each service,there are 10 QoSs
no concern on the type of inputs and outputs
one-way workflow: no branch
------------------------------------------------------------------------------
naive_kai.py:
import from naive
modified:
concern on type:
	type: for one service, only a part of service in the next task can be connected to
	(self.next = type [service,service,...])

add:class route

every service sholud possess a attribute which idenify its task.([])

so service should also be modified

should delete or modify class task and system

dfs full search
no concern on the relationship between type and type (like Inclusion)

------------------------------------------------------------------------------
12-21
Try to add relationship between type and type


------------------------------------------------------------------------------
12-21
skyline_naive:
modified naive_kai.py into use naive skyline(in task) version

------------------------------------------------------------------------------
12-22
task:
send section sentence to ishikawa

finish 12-21 task

------------------------------------------------------------------------------
how to cluster the services in the task:
	count every service  

------------------------------------------------------------------------------
12-26更新：
	生成属性树：
		inpurt：［ser，ser，，，］
		output: [node,node,...]
	先确定node个数。
	对于每个node，找之前的

------------------------------------------------------------------------------
12－29
为了方便：launch.py

from naive_kai import gen
workflow = gen()
task = workflow[0]
from skyline import gen_node_list
a = gen_node_list(task)
for node in a:
	node.printf()
------------------------------------------------------------------------------
12-30更新：
node树已完成
开始考虑skyline的算法
------------------------------------------------------------------------------
1-1更新：
skyline.py完成
launch.py更新。以确认完全正常解

目标：ぶれバージョン
------------------------------------------------------------------------------











