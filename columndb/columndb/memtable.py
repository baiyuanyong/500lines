THRESHOLD = 10


class MEMTable:
    def __init__(self):
        self.mem_table = {}
        self.size = 0

    @property
    def table(self):
    	return self.mem_table
    
    def get(self, key):
    	return self.mem_table.get(key, None)

    def add(self, key, value):
        if not key in self.mem_table:
            self.size += 1
        self.mem_table[key] = value
        if self.size >= THRESHOLD:
            return True
        else:
            return False

    def clear(self):
        self.mem_table = {}
        self.size = 0
