# Calculate the execution time on each processor.

timetable = {0: 1,
         1: 2,
         2: 3,
         3: 4,
         5: 5,
         6: 6}


schedule = {0: [0, 1],
			1: [2, 3],
			2: [4, 5],
			3: [6]}


graph = { 0: [1],
		  1: [2],
		  2: [3],
		  3: [4],
		  4: [5],
		  5: [6]}

# Recursion.
calc(task, timetable, schedule, graph):
	