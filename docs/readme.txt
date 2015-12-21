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





