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
launch.py:z全探索とskylineを用いたバージョン。効果覿面

目标：ぶれバージョン
------------------------------------------------------------------------------
1-2更新：
目标：ぶれバージョン

skyline_bure.pyブレバージョン
launch1.py:ブレとブレではないバージョンの比較

from skyline_bure import strong,one_strong ,weak ,bure

#ans0 = strong() 
ans0 = [[6, 7, 9, 8, 1, 3],
 [6],
 [6, 7, 9, 8, 1, 5, 4],
 [6],
 [6, 7, 9, 1],
 [6],
 [],
 [6],
 [6],
 [6]]
ans = one_strong(ans0)

ans1 = weak(ans)

one_strong,one_weak = bure([1,2],ans,ans1)

ブレ　完了：結果良さそう

p = [[1,2,3],[3],[3],[]]

one_strong(p)



----------------------------------------------------------------------------
1-3更新：
将strong的定义从1段强 修改强的无上限。

修改了bug：最后的task的service选择错误

修改了bug：one_strong和strong的生成关系
----------------------------------------------------------------------------
1-11更新：
version4完成：
	优化部分：
	只要是将start和end合并运算：
		start的f s w中各选skyline然后合并作为发射start
		写入end中时注意尽可能留下fsw中最大的。



