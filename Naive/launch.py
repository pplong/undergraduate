from naive_kai import gen
workflow = gen()
task = workflow[0]
from skyline import gen_node_list
a = gen_node_list(task)
for node in a:
	node.printf()