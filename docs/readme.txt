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

add:class route

every service sholud possess a attribute which idenify its task.

so service should also be modify

should delete or modify class task and system

mock search
no concern on the relationship between type and type (like Inclusion)

------------------------------------------------------------------------------

pseudocode:

对于 生成的workflow
	生成一个预处理list。
	
	制造一个爬虫， 
		dfs

dfs:
	function 深さ優先探索(v)
    v に訪問済みの印を付ける
    v を処理する(当分のrouteに追加、当分qosを計算)
    for each v に接続している頂点 i do
        if i が未訪問 then
            深さ優先探索(i)


