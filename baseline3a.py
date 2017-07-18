# baseline 3: some compromise or intelligent way to settle this tradeoff
# - 3a: can take jobs from later in the schedule only if they’re accessing a data item already accessed in the suffix
# - 3b: if we schedule a job out-of-sequence and it uses a new data item, then recompute WTMB schedule for the suffix
# 3a is implemented.

